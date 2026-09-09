# 实施计划、步骤与交付效率 v1.1

状态：计划已制定，未启动业务实现/迁移/部署。依赖 [detailed-design.md](detailed-design.md) 与 [tasks.md](tasks.md) 的逐项任务。

## 1. 交付目标与估算口径

**R1 先解决用户拿不到文件的问题，R2 补正式悬赏验收。** 两者都可独立展示、测试、评审和交付；R1 不需要等完整的新任务协议或资金系统。第一期限定单 Agent 正式交付；原多人任务仍可取显式分享成果。

| 里程碑 | 累计实现、针对性验证和评审工作量 | 用户能得到什么 |
| --- | --- | --- |
| R1 | 7～10 人日 | 对话与悬赏均能分享并下载真实文件，支持断线重试、刷新/离线取件 |
| R2 | 12～18 人日（在 R1 上追加5～7.5） | 新单 Agent 悬赏交付要求、有效租约提交、固定版本验收、返工 |
| 计划缓冲后 | 14～21 人日 | 为存储/扫描器配置、迁移差异、评审返修、移动端联调留2～3人日 |

按一名主要实现者串行工作约3～4个工作周；外部审批/凭据准备/生产发布排队/用户阶段确认的等待时间另计，不把“人日”冒充固定日历日期。12～18 为优化后的工程估计，不是已测量的吞吐；OD00 若发现分库部署、不可用存储/扫描器、无法建立真实 run 或现有租约无法接线，必须重估受影响阶段。

相比原18～28人日：优先让用户约7～10人日看到可用取件；完整本轮范围的估计由共用 HTTP/fixture/组件、单 Agent 验收和推迟增强项压缩。新增身份/GC/状态机检查并未删除。**同等完整范围的总工作量没有凭空消失**：目录浏览、多人正式交付、原生微信桥接等延期项完成时仍需投入。

## 2. 关键路径

```mermaid
flowchart LR
  A[OD00 契约和部署探测] --> B[OD01 来源与run授权]
  B --> C[OD02 对象和上传]
  C --> D[OD03 业务发布与下载]
  D --> E[OD04 客户端采集和恢复]
  E --> F[OD05 共用UI]
  F --> G[OD06 R1集成验收]
  G --> H[OD07 HTTP租约与policy]
  H --> I[OD08 唯一提交事务]
  I --> J[OD09 验收与返工]
  J --> K[OD10 验收UI]
  K --> L[OD11 R2集成验收]
```

每次仅一个活动实现任务和写入者，完成验证后独立只读评审，提交结果供用户按项目规则确认，再进入下一任务。评审者不修改自己评审的代码。不以多 Agent 同时改同一模块或并行 Gradle 构建缩短周期。

## 3. 开始前的半天：OD00

1. 记录 root/API/Web/client commit 和本地改动，定位 AGENTS 与 MODEL_ROUTING；创建实现分支时使用 `codex/agent-output-delivery-*`。
2. 验证当前聚合 starter 加载 agent/chat 且共用 transaction manager；检查 DB 版本、列宽与 collation，确认新 binary scope SQL 与现有精确授权一致。
3. 在授权测试环境探测一个私有 bucket 的 put/get/head/delete、流处理/错误路径及备份策略；确认扫描器健康、资源限额与失败关闭策略。
4. 核对网关 body limit 至少50MiB+请求开销、上传硬超时10分钟、同源 API 地址；不开放公共桶或改造 ISP URI 路由。
5. 用一条私聊、一条榜文命令记录真实派发链路，确认能在服务器创建 source/run；对没有实际转发到 Agent 的普通模型聊天明确禁用产物能力。
6. 将 OpenAPI 请求/响应、manifest、capability 数据载入各仓测试 fixture，校验请求字段名称与字符串版本，先发现契约冲突再写业务。

产出一页 prerequisites 证据，标注 PASS/FAIL/待准备、责任角色、影响里程碑。不需要在本次详设阶段收集生产密钥，也不以未经验证的存储假设宣布可部署。

## 4. 每个实现任务的标准步骤

1. **认领**：任务 ID、写入者角色、分支、基线、文件责任、依赖完成证据；先检查上个任务的 reviewer 结论。
2. **先定可观测例子**：直接使用 fixtures，指定一个正常路径和该任务最危险的失败路径，避免复述实现的无效测试。
3. **实现**：只改任务范围内的 DTO/DAO/service/组件，若共享边界变化同步更新契约；不可暗改新的版本/ACL 语义。
4. **验证**：运行该任务新增的相关测试，涉及事务则真实 MySQL，涉及 bytes 则真实文件 hash；业务前端变更运行 build，文档不跑业务构建。
5. **只读评审**：P0由 critical_worker 写、adversarial_reviewer 评审；常规代码按路由；设计变更可由 architect 先审。发现阻塞由原写入者修复。
6. **交接**：记录 commit、文件、测试命令/结果、剩余风险、下一解锁任务；用户确认点提交具体演示/差异和证据，不提交抽象计划。

每个任务的常规验证/评审已计入估计；出现新修改、失败或未解决风险才扩大重测。可按一个提交一个垂直切片交付，避免先写全部后端再第一次联调。

## 5. R1 的实施顺序

- OD01先让一个认证来源/run走通 ticket 交换，覆盖错误owner、旧binding、tenant=0。此时不开文件写入口。
- OD02打通上传状态与对象验证：手工fixture上传13字节文件 → 校验 → READY，再演示断流重传及旧epoch拒绝。存储写路径真正验证后才接用户数据。
- OD03完成 task/chat的发布/列表/确切版本/代理下载、OWNER_SHARE 与 private区分；用HTTP客户端跑“登记后Agent离线仍下载”。不要等待Web组件才检查取件。
- OD04客户端只接这套已验收HTTP契约；先读固定manifest，再集成CLI执行finish；验证队列在重启后恢复而模型调用次数不增加。
- OD05一个OutputList组件接聊天和榜文详情，支持用户可见状态与下载。近期工作台只有一处复用，不另写下载协议。
- OD06执行R1集成矩阵，演示本地/托管Agent、刷新恢复、跨用户拒绝、微信受限环境的实际可用替代路径。成果分享显示“未正式验收”，不包装成R2。

## 6. R2 的实施顺序

- OD07先补HTTP claim/start/heartbeat/release；只对allowlist新建policy1、单required work item；硬拒绝不支持客户端和所有legacy/direct完成绕过。120秒TTL/40秒心跳在现有max-duration=900000ms默认范围内，测试配置仍需核对。
- OD08复用R1对象/成果版本，实现TaskDeliverySubmissionService一个事务：lease CAS、批次/清单、delivery pin、submitted和事件/receipt一次提交；主动注入中途异常验证全回滚。
- OD09实现accept/request_changes与显式rework派发；返工状态是源码允许的submitted→ready，新run重新claim；用户评价不会自动触发另一次模型执行。旧批次不再可验收。
- OD10在同一榜文详情增加交付要求、批次清单、验收意见与重新执行按钮；分别处理409冲突和结果未知，不重复提交或自动重跑。
- OD11执行R2原子性/负向/回放兼容测试，记录版本/迁移/开关，再提供可审阅发布候选。

## 7. 缩短周期的具体执行措施

| 措施 | 实际做法 | 不可省掉的门槛 |
| --- | --- | --- |
| 一个契约 | OpenAPI、schema-contract和fixtures一起改，三仓同步读取同一版本 | 严格schema与手写ACL/状态机测试 |
| 一个写通道 | 首发HTTP；WS仅auth交换 | 精确身份、幂等回执、run绑定 |
| 两个垂直里程碑 | 先文件可用，再验收；R1不会被资金/租约增强阻塞 | 两个入口都实际下载通过 |
| 一套展示 | 聊天/榜文复用组件和下载工具 | 切换用户/source清除缓存、取消旧响应 |
| 增量数据 | 新表+旧表可空扩展，不重写历史artifact | 无证据历史归属不回填、schema一致性检查 |
| 早期真实依赖验证 | 第一天验证存储/扫描器/事务/实际run | 不用mock结果替代可用性证据 |
| 精准回归 | 每任务相关测试；阶段结束整体验证 | API/Web必需检查和真实数据库并发测试 |
| 每日明确阻碍 | 汇总剩余关键路径、阻碍原因和解法 | 不使用“完成百分比”掩盖未跑通链路 |

## 8. 验证命令与证据保存

这些命令是**实施后的执行模板，本次没有运行**。先由实现者确定匹配的测试类/文件已经存在，避免 --tests 无匹配被误记通过。

```bash
# cwd=/home/chc/wsps/cyf/api；锁覆盖整个Gradle进程
flock /tmp/cyf-gradle.lock ./gradlew :agent:jia-agent-service:test --tests 'cn.jia.agent.output.*'
flock /tmp/cyf-gradle.lock ./gradlew :chat:jia-chat-service:test --tests 'cn.jia.chat.output.*'

# cwd=/home/chc/wsps/isp-install/conf/codex-ws-agent；拟新增文件
node --test test/output-manifest.test.mjs test/output-exporter.test.mjs test/output-queue.test.mjs test/output-http.test.mjs

# cwd=/home/chc/wsps/cyf/web；拟新增文件
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter dot --exit tests/output-delivery.test.js
npm run build
```

后端阶段回归还应包含现有identity、task-result、workspace/replay及legacy兼容相关测试（具体类在任务中记录）；client回归现有agent-client/workspace-manager；Web回归会话切换/任务工作台。持锁的Gradle命令串行执行，测试结果只写真实退出状态。

证据建议写 `specs/agent-output-delivery/evidence/R1/`、`R2/`（实现时创建），包括命令、commit、测试报告索引、下载hash和演示说明。不得保存token、密钥、用户文件正文或含签名URL的网络日志。

## 9. 发布门槛与暂停规则

R1必须满足O01/O03～O12/O19～O23以及O26～O30中适用于文件分享的场景（O20的正式delivery/争议保护部分在R2验证；R1验证普通引用到期、解绑与底层hold互斥）；代码成果O02只承诺manifest指定包/文件，自动完整Git补丁增强另计；微信O21必须完成实际取件路径验证。R2再满足O13～O18/O24/O25/O31～O33和相关回归。

scope越权、错误版本验收、已引用对象误删、legacy绕过任一出现即阻断相应写能力扩大。上传失败率、传输耗时和队列年龄用首批测试数据建立基线，不能尚无样本就编造SLO已达成。建议灰度观察至少一个真实工作日，记录实际结果后再扩大。

存储/扫描器不可用时暂停新发布并保留读取，不以公网链接或未校验对象临时替代。工期压力优先延后未纳入R1/R2的增强项，不降低鉴权、冻结版本和持久回执。
