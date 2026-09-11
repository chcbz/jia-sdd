# API 3 秒性能治理 design

## 1. SLO 口径

### 1.1 统一时间边界

- **应用耗时：** 从请求体已按契约接收并进入受管应用，到同步/异步请求完成回调；普通 JSON API 必须包含鉴权、业务、数据库、缓存、外部依赖、序列化和响应体写出。
- **网关耗时：** 使用 upstream connect/header/response time；普通 JSON API 以包含完整 upstream 响应的 `upstream_response_time` 为最终服务端 SLI，应用计时用于拆分根因。
- **用户端耗时：** 从浏览器发起到完整 JSON 可用，单独统计，不与服务端分位数混算。
- **成功样本：** HTTP 和业务语义均成功；5xx、超时、容量型 429、服务慢导致的 499 进入坏事件。预期 ACL 拒绝单列，不用于证明业务快。
- **双门禁：** 延迟成功率 `SLI_3s >= 99%` 与有效、已授权请求语义成功率 `>= 99.9%` 必须同时满足；快速 503/504 不能通过性能验收。
- **分位数：** 每个规范化 route 分别统计，不把快接口汇总值用于掩盖慢接口；正式计算使用固定 histogram bucket 和原始样本复核，不使用跨 route 聚合近似值。
- **窗口与样本：** 线上目标窗口为滚动 28 天。隔离基准对首批核心 route 每档预热后运行至少 30 分钟、至少 10,000 个合格样本，连续 3 轮均通过；低流量 route 至少 1,000 个固定合成样本，否则只标 `insufficient`。

### 1.2 接口等级

| 等级 | 类型 | 主要门禁 | 3 秒含义 |
| --- | --- | --- | --- |
| `SYNC_CRITICAL` | health、会话恢复、首屏核心读 | p95 <= 500ms，p99 <= 1s | 1s 内成功或明确失败 |
| `SYNC_STANDARD` | 普通 JSON CRUD/查询/写入 | p95 <= 1s，p99 <= 2.5s | 3s 内完整响应或明确失败 |
| `ASYNC_ACK` | 批处理、作业、可能长于 3s 的命令 | ACK p95 <= 1s，p99 <= 2.5s | 3s 内返回 202/任务 ID/幂等状态 |
| `STREAM_FIRST_EVENT` | SSE、AI 流式 | 握手 p95 <= 1s；握手和首个应用帧 99% <= 3s | 3s 未握手/未首帧必须明确结束；不要求流完整结束 |
| `TRANSFER_TTFB` | 上传、下载、缩略图、大文件 | body 接收完成后 ACK/响应头 99% <= 3s；下载 TTFB 99% <= 3s | 3s 未 ACK/未响应头必须明确结束；完整传输按大小/吞吐单列 |
| `EXTERNAL_REDIRECT` | OAuth/微信等重定向 | 本系统处理 99% <= 3s | 3s 未重定向必须明确失败；排除用户停留和第三方页面时间 |

`endpoint-slo-registry.yaml` 使用 default + exceptions：任何新 route 未登记时默认 `SYNC_STANDARD`，CI 发现动态/未知 route 或例外未登记时失败。

## 1.3 全量 API inventory

PERF-01 必须生成并双向比对两份清单：

1. **声明 surface 清单：** 展开所有 Controller 的 class/method mapping、HTTP method 数组、多 path 数组、继承映射和条件注解；再从 Spring/Actuator 配置、依赖版本和显式 allowlist 生成 management、error、框架 endpoint manifest。同一路由的不同 method 分别计数。
2. **运行时清单：** 对每个可发布 profile（至少 grey、prod）启动 exact candidate，在受保护环境读取 Spring `RequestMappingHandlerMapping` 与 management/Actuator mappings；记录条件 Bean、框架端点、error handler 和实际 context path。

“声明 surface（Controller + framework manifest）”与运行时清单任一方向不一致、profile 间未解释差异、动态 path 无法规范化均为失败。Swagger、静态资源和 CORS `OPTIONS` 可作为非业务 surface 单列，但不得从总 inventory 消失；Actuator/内部运维 endpoint 进入 `OPERATIONAL` 类并具备独立速度和访问控制门禁。inventory 必须绑定 API tree SHA、profile 配置摘要和内容 hash。

## 2. API and data contract

### 2.1 兼容原则

本专题默认不改变现有业务 JSON 字段。需要异步化的长接口采用新增异步 endpoint 或保持原路径但通过版本/feature flag 灰度，不能把已有同步成功响应静默改为 202。

### 2.2 请求标识

- 接受客户端 `X-Request-Id`，仅允许 `[A-Za-z0-9._-]` 且长度 8–128；非法值丢弃并生成新 ID。
- 响应始终返回最终 `X-Request-Id`。
- 日志与指标使用规范化 route，不记录 query、token、Cookie、Authorization 或请求正文。
- OpenTelemetry/trace 能用时，将 request ID 与 trace ID 一并输出；不能用时 request ID 仍独立工作。

### 2.3 预算传播

- 普通同步请求外层预算为 3000ms；内部应用目标为 2500ms，预留网关与序列化余量。
- 每个依赖调用使用 `min(依赖默认预算, 剩余预算 - 安全余量)`；剩余预算不足时不再发起新依赖调用。
- 数据库连接获取、SQL、Redis、LDAP、Elasticsearch、HTTP/AI/SMS/微信等调用不得继续沿用 30–60 秒的无差别等待；禁止在业务代码中临时 `new RestTemplate()` 绕过统一预算。
- 写操作在进入不可取消事务前完成鉴权、参数校验和幂等判断；超时返回必须能区分“未开始”“已受理”“结果未知”。

### 2.4 错误行为

| 场景 | 行为 |
| --- | --- |
| 请求预算耗尽且工作未开始/可安全取消 | 返回 504 风格的统一业务错误，包含 request ID，不回显内部栈 |
| 依赖不可用/连接池饱和 | 快速返回 503 或既有等价业务错误，标记依赖类型 |
| 长任务可异步执行 | 3 秒内返回 202/现有成功包装 + task ID；重复请求返回同一幂等结果 |
| 写事务状态未知 | 不自动重试；返回可查询状态的 operation ID，并记录审计事件 |
| SSE/AI 首帧超时 | 结束连接并返回/发送明确错误事件；客户端指数退避，不固定 1 秒重连 |

### 2.5 统一异步 operation v1 合同

任何从同步转为异步的接口必须新增版本化/显式 opt-in 合同；旧同步响应不能静默变为 202。

- 提交：`POST <versioned-async-route>`，请求头 `Idempotency-Key` 必填。
- 查询：`GET /operations/{operationId}`。已授权且存在返回 HTTP 200；不存在与未授权统一返回相同 HTTP 404/业务 code，禁止通过耗时、正文或状态区分存在性。
- 受理成功：HTTP 202；同一幂等请求若 operation 已存在则返回 HTTP 200 或 202（由当前状态决定）。既有 `JsonResult` data 固定包含 `operationId`、`operationType`、`status`、`version`、`submittedAt`、`startedAt`、`finishedAt`、`updatedAt`、`statusUrl`、`result`、`error`、`retryable`。
- 状态机：`ACCEPTED -> ENQUEUED -> RUNNING -> SUCCEEDED | FAILED | EXPIRED | CANCELLED`；`version` 为单调十进制字符串，状态只能单调前进，终态不可回退。若复用既有 Agent outbox 状态，则保留其原状态名，不做同义转换，并在适配层映射为 operation view。
- ACL：提交和查询都以 byte-exact `(tenant/jiacn, client_id, owner/principal)` 校验；operation ID 不构成授权。
- 幂等：同一 scope + key + payload digest 返回同一 operation；同 key 不同 payload 返回 409；key 保留期不少于 operation 保留期。
- 原子性：受理事务内原子写 operation、命令/业务意图和 outbox；外部调用只在提交后执行。提交已成功但响应超时时，重试必须取回同一 operation。
- 结果：`result` 仅在 `SUCCEEDED` 非空，结构由 `operationType + contractVersion` 冻结；其他状态为 null。`error` 仅在失败终态非空，固定为 `{code, message, retryable}`。时间字段无值时为 null。
- 保留：终态默认保留 7 天；保留期内 `EXPIRED` 仍通过 200 状态 view 返回，删除后不存在/未授权均为相同 404；另保留防重 tombstone 至幂等窗口结束。
- 失败：`error.code` 为有限枚举，保留可重试性；不得把内部栈、凭证或第三方正文写入响应。

现有 `POST /job/execute/async` 仅为待审计候选；在 method/path/响应/状态/ACL/幂等证据完成前，其 registry compliance 为 `pending`，不能凭“异步”自动通过专题验收。

## 3. Observability design

### 3.1 指标

- `http.server.requests`：route、method、status、outcome；SLA 边界至少包含 0.1、0.25、0.5、1、2、2.5、3、5 秒。
- `cyf.http.inflight`、`cyf.http.deadline.exhausted`、`cyf.http.slow`。
- Hikari active/idle/pending/acquire、Tomcat busy/max、JVM GC pause/heap/thread、process CPU。
- SQL count/duration/rows，按 mapper/statement ID，不把 SQL 文本或参数作为标签。
- 外部依赖 latency/error/timeout，标签仅 provider/type/operation 的有限枚举。

### 3.2 慢请求日志

当普通请求 >= 1000ms、失败或预算耗尽时输出一条结构化摘要：timestamp、request_id、trace_id、method、route、status、duration_ms、db_ms/db_calls、cache_ms/cache_calls、external_ms/external_calls、queue_ms、outcome。禁止打印请求参数和敏感正文。

现有 `HttpRequestLogInterceptor` 的逐请求参数序列化、开始/结束两条 INFO 和每次 JVM 内存计算应由新观测链路替代或默认关闭，避免日志 I/O 自身放大长尾。`UriAccessLogFilter` 当前在业务链路前同步调用 `LogService.addLog()` 写审计库，应改为有界异步/after-commit 或至少从健康检查、SSE、静态/大流量路由排除，并保留审计可靠性与失败降级。

## 4. Optimization strategy

### 4.1 P0：基线可信

1. 生成当前全部 Controller/mapping 清单并与 SLO registry 做 100% 覆盖校验。
2. 开启安全 metrics 和 request ID，补 Nginx upstream 分段计时。
3. 将生产运行与构建/测试/Agent 资源隔离；固定预发资源、JDK、MySQL 数据和缓存冷热状态。
4. 收集至少 24 小时路由分位数，输出 top-N 慢接口、SQL 次数、连接等待和外部依赖占比。

### 4.2 P1：聚义厅热点

- `/agent/map`、`/agent/roster`：persona、task/status 统计批量查询；DTO 只取所需列，禁止随 Agent 数量线性追加查询。
- `/agent/tasks/search`：授权、keyword、status、分页下推 SQL；禁止先全量 enrich 再 Java 内存分页。
- `/agent/tasks/status-counts`：数据库按授权范围聚合计数。
- `/agent/personas/catalog`：版本化、有限 TTL 缓存；不缓存用户绑定状态。
- `/agent/scenes/{sceneId}/snapshot`：一次一致性读取，避免请求内重复构造/扫描。

固定 100 Agent、1000 Task、约定 persona/scene 数据集下，以上每路由 SQL 次数应为 O(1) 或固定上界，而非 O(N)。

### 4.3 P2：全模块治理

按 p99、调用量、错误预算消耗排序逐批处理 user/material/isp/wx/sms/task/chat 等模块：

1. 全表读取/内存分页 -> SQL 分页、聚合和投影。
2. 循环 DAO/外部调用 -> 批量接口、join 或受控并发。
3. 静态/公共元数据 -> 有界缓存；权限相关数据 -> 使用无歧义编码的 tenant/jiacn + client_id + task/资源 scope + owner/principal + subject + ACL-policy/data version，全维度 byte-exact。
4. 同步长任务 -> `ASYNC_ACK` + operation status。
5. 事务中网络调用 -> outbox/after-commit/补偿，缩短锁持有时间。
6. 未设上限的批量接口 -> page size、文件大小、条数和并发限制；`JsonRequestPage` 不得以 `Integer.MAX_VALUE` 作为默认 page size。

## 5. Frontend behavior

- 普通 JSON 请求默认总预算 5 秒，后端 3 秒目标留出网络与浏览器余量；UI 在 5 秒内显示成功、可重试失败或明确的离线状态。
- 仅幂等读允许最多一次带 jitter 的重试，且必须服从剩余 deadline；写请求必须使用幂等键或 operation ID。
- 聚义厅优先加载 map/snapshot；roster、catalog、tasks、counts 按面板或 idle 加载，分别维护 loading/error。
- SSE 采用指数退避、jitter、单会话去重、隐藏页暂停；401/403 不盲重连。
- RUM 记录 route template、request ID、duration、network/error class，不记录 URL query 和正文。

## 5.1 聚义厅不可破坏合同

- map 只来自 `/agent/map`，roster 只来自 `/agent/roster`，不得重新引入 `/agent/active` 或合并为隐藏选中状态。
- 任务分配必须传显式目标 Agent；tenant/jiacn、client_id、task/资源 scope、owner/principal、subject、ACL-policy version 与 byte-exact identity 不得因 join、缓存、批量查询而放宽。
- snapshot/workspace 读取保持一致性；版本字段保持十进制字符串、单调递增和 generation fencing。
- SSE 保持 Last-Event-ID、live-before-replay、去重、gap/resync、授权重放、慢消费者/断线清理和有界缓冲。
- Web reducer 必须幂等，旧 generation/重复事件不得覆盖新状态；性能优化不得引入第二套状态源。

## 6. Verification design

### 6.1 测试层次

1. **静态门禁：** 当前 route 与 registry 100% 覆盖；高基数标签和敏感日志规则检查。
2. **单元/集成：** deadline 传播、request ID、错误映射、幂等、事务取消边界、缓存 ACL。
3. **DAO 性能合同：** 固定数据集记录 SQL 次数、分页结果、EXPLAIN 和索引使用。
4. **接口基准：** 预热后按 route 采样，输出 count/p50/p95/p99/max、<=1s/<=3s bucket、语义成功率、error/timeout；首批每档 >=30 分钟且 >=10,000 合格样本，连续 3 轮通过。
5. **容量阶梯：** 1、5、10、20 并发，记录吞吐、排队、连接池、GC 和错误率。
6. **依赖故障：** DB/Redis/LDAP/外部 HTTP 慢、断开、连接池耗尽时必须在 3 秒内明确失败且无未知事务。
7. **持续回归：** 固定 exact tree、test selector、DB fixture digest；未改树复用 evidence。

### 6.2 判定

- 任何 `SYNC_*` 路由 p99 > 2.5s、`SLI_3s < 99%`、语义成功率 <99.9%、存在超 3s 未明确结束或出现未知事务状态，候选不通过。单个环境调度噪声需归因但不能无证据删除样本。
- `STREAM_FIRST_EVENT` 以握手和首个应用事件判定；`TRANSFER_TTFB` 以 body 接收完成后的 ACK/TTFB 判定。
- 样本数不足只标记 insufficient，不得标记 PASS。
- 只有所有 registry 路由有证据、所有豁免有负责人和到期日时，专题才可 accepted。

## 7. Compatibility and rollout

1. metrics/request ID/安全日志先默认开启，deadline 先 shadow 记录不强制。
2. 对热点读接口按 route feature flag 灰度新查询，比较结果一致性和耗时。
3. deadline 从告警模式切为强制前，先验证写事务、幂等和外部依赖失败语义。
4. 逐模块推进，不进行一次性全量大改；每批有独立 commit、测试、Reviewer 和回滚开关。
5. 生产部署必须由明确 runtime Owner 授权；本设计不授权重启、压测或改生产配置。

## 8. Decisions

- “所有 API 3 秒内”采用**默认普通同步完整响应 3 秒，显式例外按 ACK/首帧/TTFB 3 秒**的统一规则。
- 用每路由 p95/p99 和硬上界共同验收，不用全局平均值。
- 首批优化聚义厅热点，因为已有生产长尾证据；全局 registry 和观测先行，避免局部优化后无法证明整体达标。
- 不把简单 `Future.get(3s)` 或代理 timeout 当性能优化；必须修复查询、排队、依赖和资源根因。
