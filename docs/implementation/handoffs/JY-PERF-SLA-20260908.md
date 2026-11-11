# 聚义厅页面 / 后端性能诊断与 SLA 建议

日期：2026-09-08（Asia/Shanghai）。只读诊断：未重启服务、未修改生产配置、未执行构建或压测。现场采样约 10:41–10:55；访问日志固定窗口 09:46:38–10:46:38。

## 1. 结论与证据边界

当前优先级应是“生产运行资源隔离 → 关键 API / SQL 降本 → 前端渐进加载 → SLO 达标后对外 SLA”，不是继续加长超时。已确认 API 存在秒级至数十秒长尾，Java 与 MySQL 均有大量内存被换出。资源争用是最强的共同原因候选，但尚无逐请求 Trace/GC/缺页关联证据，不能把全部耗时精确归为 Swap 或某条 SQL。

- 已发布前端 source：`567e95378a1840f63d212dbb102ab8a860c1c3b2`，工作树 `/home/isp/wsps/cyf/.worktrees/home-login-20260907`。
- 后端源码参考：`/home/isp/wsps/cyf/api` HEAD `dc039b34d9d24a46714724d5937f2c098f6c6d87`，存在一个本地变更；未证明该源码与当前运行 JAR 字节对应。以下后端代码风险属于待部署版本映射与 Trace 验证的假设，不等同于线上已证实根因。
- 不把 3 次探针推算成月可用性；不把 403、401 或 OPTIONS 的快速返回当作业务成功；不把 2–9 个业务样本的 P95 当作可靠总体分位数。

## 2. 现场数据

### 2.1 访问日志中的成功业务请求

指标是 Nginx `$request_time`，包含请求读取及响应发送，不是纯 SQL/Java 执行时间。只列对应接口的 2xx，取消请求另计；HTTP200 内部业务错误未具备语义识别。

| 接口 | 2xx 样本 | 最小 / 中位 / 最大 | 同窗口 499 |
|---|---:|---|---:|
| GET /agent/map | 5 | 0.148 / 2.977 / 24.054 秒 | 3 |
| POST /agent/roster | 4 | 1.101 / 14.049 / 32.001 秒 | 2 |
| POST /agent/tasks/search | 8 | 0.060 / 3.505 / 11.135 秒 | 1 |
| POST /agent/tasks/status-counts | 9 | 0.135 / 3.072 / 10.967 秒 | 0 |
| GET /agent/personas/catalog | 2 | 2.044 / 4.582 / 7.120 秒 | 4 |
| GET /agent/scenes/juyiting-main/snapshot | 4 | 2.057 / 7.464 / 24.051 秒 | 1 |

整个 API 域窗口记录 426 个请求，其中 15 个 499；这不是用户有效业务请求全集，不能直接作为错误率分母。scene events 的 OPTIONS 有 213 次，日志没有该窗口完成的同路径 GET；可能包含尚未关闭的长连接，不能仅据此认定所有 SSE 建连失败，但必须排查重复预检与重连。

### 2.2 静态入口与本机后端

- 服务器侧经公网 HTTPS 请求首页，3 次 HTTP200 总耗时 41–45ms，压缩传输约 1KB。只证明 HTML 交付，不代表用户侧 LCP、JS 执行或地图首帧。
- 本机 `127.0.0.1:10018/actuator/health` 3 次 HTTP200，耗时 2.983–2.999 秒，响应状态 UP。
- 随后一次本机 `/actuator/health/liveness` 6 秒未收到字节而超时；只是一条异常观测，不据此判定长时间宕机。
- 公开 API 对 curl User-Agent 存在 Nginx 拒绝规则，本次公开 API 的 403 是入口规则命中，不是业务探针成功，也不代表普通浏览器请求被同样拒绝。未绕过鉴权测取用户数据。

### 2.3 资源与日志

- 2 vCPU、约 3.64GiB 内存；现场 MemAvailable 约 594–605MiB，Swap 使用约 1.18–1.20GiB。
- 同机存在 Java、MySQL、Redis、RabbitMQ 与开发/Agent 工作进程。仅多个开发 Agent 进程的常驻内存已占据明显份额；未操作这些进程。
- Java：Xmx384MiB、Metaspace192MiB、Direct64MiB、109 线程。10:55 RSS286664KiB、VmSwap470996KiB；MySQL RSS62272KiB、VmSwap550708KiB。Swap 使用量不是“全部为活跃热页”的证明，但 vmstat 在短时采样窗口观察到 active paging；长期持续性和热页比例尚未证明。
- 短时 vmstat iowait 曾为 72%、35%，部分采样 CPU idle 为 0%；后续有空闲样本，表明有波动，不能把峰值当作持续平均。
- 当前 Java scope CPU quota=-1、throttled=0；memory limit 未设置，不支持“已被 CPU 配额限速”的解释。仅检查该 scope，未穷尽祖先级限制。
- 当前应用日志末 3500 行出现 3 次 Hikari housekeeper starvation/clock-leap 警告，延迟约 47、74、87 秒。是调度/暂停/时钟异常信号，不是某条 SQL 慢 87 秒，也不能单凭它断言数据库锁等待。
- 磁盘当前约 79% 使用、11GiB 可用；不能沿用之前“磁盘几乎满”的旧状态解释本次现场。

## 3. 原因分层及改进

### P0：生产与开发/构建争抢内存及 I/O（强证据，因果需关联）

优先把构建、编码 Agent、测试、压测移出生产机；由各进程所有者协调迁移，不跨线程强停。为 API 和数据库保留真实工作集容量，观测 page-in/out、major faults、JVM GC pause、DB buffer pool 命中和磁盘 await，再定配额。

不直接在当前主机上增大 Xmx、Tomcat 线程、Hikari pool，也不关闭 Swap：这可能把变慢转化为 OOM/连接排队。资源隔离后的 4vCPU/8GiB 可作为单节点性能验证起点而非容量保证；是否扩容应由隔离后的测量和容量测试决定。

### P1：后端列表存在 N+1 和内存分页候选

参考源码：
- `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java:254-270,1561-1597,1674-1724`：map/roster 每个 Agent 构造 DTO 时查 persona，统计阶段再次查 persona，并查询任务集合。具备约 1+3N 次查询形态，实际 SQL 次数须 Trace/缓存行为验证。
- 同文件 `:574-626`：tasks search 先加载匹配集、逐条 enrich、Java keyword 过滤，再内存分页；status counts 也读取任务集合后计数。
- `api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentPersonaDaoImpl.java:13-24`：persona lookup 落到 selectOne。

方案：列表使用批量 persona/统计查询，地图 DTO 只返回地图需要字段；SQL 层按授权作用域过滤、分页、聚合；结合真实 EXPLAIN 和慢查询选择索引，不盲目建索引。公共 persona 元数据可以版本化缓存；租户/用户数据必须按授权范围分别缓存、失效，禁止串用户缓存。保留 map/roster 独立数据流。

### P1：前端首屏请求过多、超时掩盖失败（当前部署源码已确认）

- `web/src/components/world/JuyiHall.vue:734-746,1460-1471`、`web/src/composables/juyiting/useHallData.js:138-231`：进入页面并发请求 map、roster(pageSize100)、catalog、tasks(pageSize30)、counts。不是五条串行；完整刷新状态等待最慢请求，页面 shell 和地图挂载不因此同步阻塞。
- `web/src/composables/useHttp.js:111-162`：普通请求默认 60 秒，包含 token 等待。Nginx 普通 API connect20s/read300s，长尾失败缺少及时反馈。

方案：地图必要数据优先；roster/catalog/counts 随面板/空闲加载；独立模块 loading/error，不用一个总 loading 掩盖部分成功。普通读请求暂定前端总超时5秒、后端总预算3秒；代理可留少量裕度但不是靠 proxy_read_timeout 实现总时限。SSE/聊天独立策略，不套用短超时。仅幂等读取允许最多一次带抖动重试，必须满足剩余 deadline；写接口以幂等键处理而非无条件重试。

### P2：地图体积、SSE 重连和预检放大

- `web/src/game/JuyitingGame.js:196-223,524-579`：TMX下载→解析→地图声明资源→必需sprite→ready 的串行阶段；阶段内可并发。地图目录约18.6MB不是已经证明的首屏下载量，画像目录约80MB也不能直接算进首屏。
- `web/src/composables/juyiting/useHallBackendSceneState.js:65-147,244-277`：scene SSE 固定1秒重连、15秒poll fallback；聊天另有固定重连/补拉。

方案：先记录 Resource Timing / decode / scene-ready 再优化首帧资源、缓存与按需加载；SSE 采用指数退避+jitter、单会话连接去重、隐藏页面暂停、认证失败停止盲重连。预检先核对精确 Origin/Headers 与 Max-Age，不能为省时放开任意来源或鉴权。

## 4. SLI / SLO / SLA 定义与建议目标

SLI 是观测指标，SLO 是内部目标；SLA 是通过验证后对外承诺及违约处理。当前只能提出目标，不能宣称已达到 99.9%。

| 旅程/服务 | 建议内部 SLO | 口径 |
|---|---|---|
| 核心业务请求成功率 | 滚动30天99.9% | 有效业务请求的语义成功率；时间可用性独立观测，不只看HTTP200 |
| 核心普通读 API（后端） | 单接口p95≤1s、p99≤3s；5s内明确成功/失败 | 网关upstream_response_time，并分列connect/header耗时；多次尝试与失败/超时不可隐藏，纯业务执行再用Trace拆分 |
| 核心 API 用户端体验 | 建议p95≤1.5s、p99≤4s | RUM完整请求耗时，按约定网络档位/地域分桶；不与上游计时混算 |
| 认证回调/会话恢复 | p95≤2s | 排除用户输入/外部授权页面停留；自身回调和会话加载仍计入 |
| 竖屏首屏可操作 | p95≤2.5s；基础数据p95≤3s | RUM端到端，冷/热启动、设备、网络分别分桶 |
| 地图可用 | 冷加载p95≤5s、p99≤10s；热返回p95≤1s | 约定中端设备/稳定4G或Wi-Fi测试档位；其他弱网单列；未压测承诺 |
| 典籍阅读 | 首段可读p95≤2s；进度确认p95≤1s | 正文渲染与后端持久化分别记录，未确认不能展示已保存 |
| 实时通道 | 握手/首个应用帧p95≤1s；断线恢复p95≤5s | 单列连接成功率、活跃连接、事件延迟、重连/回退次数，不用长连接总时长作API延迟 |
| AI 聊天 | 请求受理p95≤1s；首字目标p95≤3s | 首字按模型/供应商分别统计；完整生成按任务类型单列，不承诺所有回答3s结束 |

目标需先经基线与隔离环境测试校准；地图5s与AI首字3s尤其需要实际网络/模型能力确认。另记录移动/桌面 LCP、INP、CLS；可采用 LCP p75≤2.5s、INP p75≤200ms、CLS p75≤0.1 的体验目标，不把 HTML curl 耗时当作这些指标。

### 可用性和预算不能混算

- 若采用“30天时间可用性”99.9%，允许不满足窗口为43分12秒；99.95%为21分36秒。只有按时间定义的指标才使用这些分钟数。
- 若采用“有效请求成功率”99.9%，预算为有效请求数的0.1%，不是直接43分12秒。两者分别呈现，不混成一个数字。
- HTTP200业务失败、5xx、超时、合法请求容量型429、有效登录意外失效都需进入对应坏事件。无效凭证/恶意流量可剔除，但不能把所有401/403无条件剔除。
- 499分层：确认用户主动导航取消单列；服务慢导致用户/客户端超时取消，计入用户体验坏事件。原因未知时保留未知桶，不能全部当“客户端责任”排除。
- 第三方依赖在内部归因上单列，但用户实际不可用不能从总体用户旅程里悄悄删除。计划内变更也记录，需明确约定才可从对外合同口径排除。

## 5. 监控、告警、故障与发布

### 最小观测闭环

1. Nginx安全结构化日志：request_id、规范化route、不含query的uri、status、request_time、upstream_connect_time/header_time/response_time、upstream_status。禁止记录token/cookie/正文；当前生效api_safe只有request_time，无法拆Java/DB/网络。
2. API：每路由latency histogram、错误码、inflight、线程池/队列、Hikari active/idle/pending/acquire latency、SQL次数和耗时；引入trace_id关联前端→API→SQL/Redis/外部供应商。常规采样1–5%、错误/慢请求优先保留，敏感数据脱敏。
3. 主机/JVM/DB：CPU/load、swap-in/out、majorfaults、GC/pause、内存工作集、I/O await、锁等待/慢SQL/bufferpool。仅“Swap已使用”不自动触发重启。
4. RUM：navigation、auth-ready、shell-ready、core-data-ready、TMX/resource/decode、map-ready、reader-ready、保存确认；按微信WebView/浏览器和冷/热分桶。
5. 从独立节点做低频只读合成探针，使用专用受控测试身份；入口UA限制需明确为探针配置规则，而不是把403当健康。liveness与readiness分开，DB/供应商故障不自动让liveness触发重启风暴。

### 告警与处置目标（拟定，需排班支撑）

- P1（核心链路不可用、广泛超时）：1分钟内探测、5分钟内确认、15分钟内缓解、30分钟恢复目标；未建立7×24值守前不能对外承诺此响应时限。
- P2（局部长尾）：15分钟确认、1小时内给出缓解计划，次工作日提交原因与改进。
- 99.9%请求SLO采用多窗口burn-rate：1h与5m同时超过14.4倍，或6h与30m同时超过6倍时升级；低流量需最小样本数或合成连续失败佐证，避免单次波动反复告警。
- 错误预算消耗过快时暂停非必要高风险发布，优先性能/稳定性修复。不可把“停止功能发布”替代现场故障处置。
- 生产构建在独立CI产出不可变制品，发布只校验/切换；验证关键旅程，区分上游模型故障。切换或前向修复由明确Owner执行，不跨线程杀进程。

## 6. 实施顺序与验收

| 阶段 | 工作 | 验收 |
|---|---|---|
| P0 / 优先当天 | 协调生产与开发/构建隔离；补upstream计时和最小资源仪表板；核对当前部署SHA | 能解释一条慢请求在网络/API/SQL/GC的主要耗时；不再只看到HTTP200 |
| P1 / 随后1–3工作日 | 批量查询/SQL分页、首屏按需加载、短请求deadline、SSE退避 | 固定数据集下关键接口p95≤1s/p99≤3s，SQL次数不随Agent数量线性膨胀；普通请求5s有结果 |
| P2 / 1周基线 | 独立预发做单用户、5/10/20并发阶梯及持续测试；加入现有SSE连接、缓存冷启动、依赖慢/失败场景 | 获得最大可持续RPS/连接数/错误率，不以简单线程数冒充容量；生产不做未经授权的压测 |
| SLA生效前 | 连续观测一个30天窗口；确定支持时段、依赖边界、故障域和补偿审批流程 | 达标才发布对外SLA；未达标保持内部SLO与实际数据公开 |

如要从单机“目标”升级为有依据的外部99.9%承诺，至少评估跨独立故障域的多API实例、数据库高可用、备份恢复演练与可演练的发布/故障切换；同一台服务器起两个进程不等于高可用。不能以8GB或某个QPS数值直接保证99.99%。

## 7. 本次证据

所有诊断材料仅在 `/var/tmp/cyf-sla-analysis-20260908/`，未复制用户请求正文、Cookie或数据库记录：
- `probes.json`：3组公网静态/受UA阻断的公开API/本机health。
- `business-latency.json`：固定一小时成功业务样本min/median/max，499另列。
- `access-summary.json`：最近2万行的匿名聚合；其小样本分位数仅诊断辅助，不用于SLA承诺。
- `resources.txt`、`api-cgroup.json`、`process-memory.json`：资源、当前scope和进程内存。
- `app-log-summary.json`：日志关键词计数及脱敏调度警告。

公开方法参考：Google SRE Workbook 的 Implementing SLOs / Alerting on SLOs；web.dev 的 Web Vitals。建议下一项可执行任务：只增加安全的 Nginx upstream 计时与前后端 request_id/RUM 标记，并协调将开发/构建负载从生产迁出；不先盲调大堆和连接池。

独立复核：Sol完成只读报告审查；已落实短时换页观察的边界、请求成功率与时间可用性区分、upstream与端侧延迟分开三项措辞修正。未把源码静态权限疑点作为未经版本确认的线上结论；未将全部499排除。
