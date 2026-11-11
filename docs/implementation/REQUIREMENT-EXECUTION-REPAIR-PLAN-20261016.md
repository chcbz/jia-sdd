# “提出需求”完整流程复测与修复方案

核对日期：2026-10-16（Asia/Shanghai）。任务：REQUIREMENT-EXECUTION-20261016。Owner：当前 Codex，无委派。**状态：诊断与方案完成，尚未实施修复、发布或完成生产端到端验收。**

## 1. 结论与证据边界

不能把当前问题解释成正常排队，也不能仅修改“等待执行”文案。至少存在三类独立故障：**私人交办没有接入当前 Runtime 的完整执行准入；后端缺少私人执行开始的持久状态；前端可能掩盖已经更新的状态。** 此外，成果提交客户端的回执验证不完整。

本轮确实重新操作了生产 Vue 组件的“填写→选资料→保存→确认授权→提交→核对进展”，并将已安装 API JAR 的实际 DTO/Jackson 序列化结果交给真实前端状态逻辑；同时将实际 API 队列投影交给已安装 Runtime 的真实消费者，分别检查后续文件桥和成果显示。**这是一组隔离分段回放，不是用登录浏览器新建生产需求、真实调用模型的整站演练。** 本轮未取得可复用的已登录浏览器会话；没有为测试接管其他聊天的浏览器、伪造身份或绕过已确认的接单阻塞。

生产侧仅做原事项定向只读核对及日志观测，未重复提交“简历优化”、读取简历正文、调用 Provider、扣费、修改配置、重启服务或部署。后续部分使用合成已完成响应检验消费者，**不等于实际生产过该成果**。没有执行新的 Gradle 验收或前端 Flow；本机检查不作为正式发布证据。

### 固定基线

- Web HEAD/远端 develop：`421f628c245b83466cafb70510ff69188180bdee`。
- API HEAD/远端 develop：`fc399976710f5b724916013926be2cbff899af8c`。
- Runtime 源码 HEAD/远端 develop：`6a9d8d3c1219450c19b3edfbef317e615940ab5d`。
- 以上远端核对时间：2026-10-16 09:45 +08:00，详情见 baseline.json。不能把本地源码 SHA 直接当作线上 API/Web 发布 SHA。
- 真实消费使用已安装 Runtime `runtime-interface-20261015-1.2.7-6a9d8d3`；API 序列化使用生产安装 JAR，SHA-256 `aaaf5667f88d666dfcd369102a7131ad081e47170fa03e9361586292fe68a45c`。本轮未补齐 API/Web 精确线上版本闭包。
- 公共契约：`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2（2026-10-14），SHA-256 `7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f`。功能契约只能补业务字段，不另建公共信封或双协议兼容。

### 原事项真实情况

`简历优化` → case `hpc_45f87e5ca8ec4fd58b87422865e87311` → execution `pwe_7f9e26b1963a496b9592de5df94c340f`。仍为 `PRIVATE / QUEUED / execution protocol 1`，一份 PDF 输入，目标吴用，期望 PDF 输出；本轮查询输出记录为 **0**。

吴用日志持续 `WORKSPACE_FILE_COMMAND_INVALID`。日志没有 executionId，虽该目标此前只查到这一条排队中的 PRIVATE 执行，仍不能将通用日志当成原事项逐请求关联证据。独立真实消费者回放报 `RUNTIME_COMMAND_CONTEXT_REQUIRED`：两者不同，**线上第一处报文拒绝的精确原因仍待补齐**。

## 2. 逐环节复测结果

| 环节 | 本轮实际做到什么 | 判断 |
|---|---|---|
| 入口 | 核对顶部“提出需求”实际打开 PRIVATE 草稿；办事页一句话是 TASK_CREATE，不是同一条执行链 | 两入口语义不同，不能拿正式事项成功替代私人交办成功 |
| 填写与选资料 | 真实 HallDraftEditor，点击填写、选固定版本合成资料、选择 PDF | 隔离组件回放通过；不是生产上传验收 |
| 保存与授权 | 真实 useHallDrafts + 已安装 Java DTO 序列化；保存后确认授权，只有一次 submit | 这段消费逻辑能走到回执；API 响应是合成业务事实，未跑真实数据库事务 |
| 创建原事项 | 对现存原 case/execution/input 做只读关联核验 | 原事项确已创建，不是用户没提交 |
| 取队列与接单 | 实际服务端投影→实际 Runtime 解码→实际 AgentMessageProcessor，带完整合成 Runtime 身份 | stub processor 接受；真实 processor 拒绝，断点成立 |
| 命令能力准入 | 核对 Runtime 真实 readyCommandTypes 及 processor 检查 | 不声明 WORKSPACE_FILE_EXECUTE；仅补字段仍不够 |
| ACK/持久交付 | 核对统一 Runtime ACK→delivery/outbox 校验；私人 queue create 未建立同类记录 | 普通 D06 要求真实 delivery、active outbox、PUBLISHED 等事实，不能伪造元数据跳过 |
| 开始执行 | 核对 PRIVATE start 的真实服务分支 | 仅验证并返回 STARTED，未持久写“已开始”；QUEUED 不能反映是否已开始 |
| 读输入/模型处理 | 跑现有 file bridge 定向回归；未绕过接单阻塞调用模型 | 文件桥局部保护可验证；本场景真实 PDF 阅读与生成仍待验收 |
| 上传与提交成果 | 实际安装 file bridge + 隔离目录；注入合法成功信封但错误 output/manifest 的响应 | 仍返回本地计算的成功 manifest，复现回执验证缺口 |
| 核对进展 | 真实组件+真实状态逻辑收到合成 OUTPUT_COMMITTED，再点击核对 | 旧 QUEUED receipt 优先，仍显示等待且缺少查看成果按钮 |
| 成果展示/预览下载 | 现有生产组件回归覆盖固定成果、不可用版本、预览与下载调用 | 局部消费通过；未发生本场景真实文件生成→鉴权预览→下载校验闭环 |
| 错误呈现 | 组件注入读取失败/已完成状态 | 回执页不显示 drafts.error；已完成标题下仍写“尚未取得成果” |

## 3. 修复项与优先级

### R1 / P0：让 PRIVATE 真正接入受控执行，而不是修饰旧队列

**现状：** API 的私人文件队列投影缺少普通 Runtime D06 所需上下文；Runtime 不声明对应 command type；普通 ACK 又要求真实 delivery/outbox，且当前实现绑定 task aggregate/PUBLISHED。三个条件必须一起看，不是补 correlationId/expiresAt 两个字段就能跑通。

**选定方向：** 保留 PRIVATE 业务语义，接入统一 Runtime 的 **native 执行生命周期**。复用现有 Runtime 会话认证、原生 HTTP 传输、持久 inbox/去重、受控执行器及 WorkspaceFileBridge；增加私人执行的窄业务适配，**不把无正式任务根的私人事项伪装成 D06 正式任务**，不新建模型执行器或第二套公共信封。

实施边界：

1. 沿用私人执行的持久记录和队列入口，将其改为返回经认证的 native 执行描述；保留 executionId/taskId/runId 原绑定，增加服务端分配的 command/attempt 身份、输入快照摘要、授权版本和租约证明。描述的身份来自 session 与数据库，不来自前端指定 owner。
2. 领取通过原子 CAS/事务绑定 installation/runtimeInstance/attempt/fencing token；取列表是发现，不等于领取成功。每个执行仅有一个有效持有者。
3. Runtime 使用明确的 PRIVATE native adapter，不再把该命令送入要求 task-D06 ACK 的普通 processor。复用持久化组件但使用 native 生命周期回执，不删除/放宽普通 `runtimeCommandContext` 检查。
4. start/input/stage/commit/failure/revoke 全部核对完整 tenant/client/owner/agent、固定授权版本、有效 attempt/fence；新会话、旧实例和跨用户回执不得替换原执行身份。
5. 开始 Provider 前持久确认 start；结果未知只查询原操作，不能通过创建新 execution、新 command 或改 idempotencyKey 恢复。
6. 定义单一最新私人 native 业务契约及实际序列化 fixture。公共 protocolVersion 仍为1；执行协议业务版本须在现有1–4库存之外正式分配并冻结，不能随手覆盖已占用值。
7. 切换后移除私人旧队列→D06 的执行路径，不长期保留旧/新消费者并行。存量迁移见第6节。

**不采用的捷径：** 从当前时间临时造 expiry；借用别的事项 command/outbox；假建 task root；把 ACK 当本地日志；把所有 native 请求免检；直接将原 QUEUED 改为成功；把顶部入口悄悄换成正式事项。

**验收：** 实际 API HTTP/数据库→真实已注册 Runtime adapter→持久接单→start；跨身份、旧租约、并发两客户端、重放均受控。不能再用 `handle: async()=>{}` 证明接单成功。

### R2 / P0：持久化真实执行状态和未知结果恢复

目标主路径：`QUEUED → CLAIMED → RUNNING → OUTPUT_STAGED → OUTPUT_COMMITTED`。允许真实失败到 FAILED，撤权到 INPUTS_REVOKED；不可执行的已确认原因要暴露 BLOCKED（或同等明确的业务投影，最终以冻结合同为准）。状态附单调 stateVersion，供前端拒绝迟到回退。

- PRIVATE start 从“校验后回 STARTED”改为原子状态推进、记录 startedAt/attempt；同一 start 重放回原回执，不重复开启 Provider。
- 网络未知结果与业务失败分开：`RECONCILIATION_REQUIRED` 属恢复标识，不能把超时自动判失败，更不能重新发起模型调用。
- 输出提交事务写入文件版本、manifest、执行终态后才报告成果可查看。仅上传临时文件不能宣告完成。
- 失败/协议拒绝记录安全的 stage/reasonCode/requestId/commandId/executionId/attempt 与是否可重试；不记录正文、简历、凭据或模型输入。
- 确定性拒绝不能每3秒重复尝试同一错误输入。保持可观测状态；只有能力/契约/输入实质变化后再恢复。瞬时网络故障退避读取原操作。
- 租约是身份/并发安全机制，不是性能预算；不因等待过久强制终止用户请求或给 Provider 下传硬 deadline。

覆盖执行实体/DAO/SQL、初始化与迁移、Hall case/result/overview/private mark 投影、Runtime持久状态及全部消费者，不能只在前端增加一个 RUNNING 字符串。

### R3 / P1：交办前检查“所选好汉确实能办”

当前 capabilities 只是服务端全局格式配置，requireOwnedTarget 主要核对归属，不证明指定好汉已注册、能读所选输入并交付所选格式。

- 增加 target-scoped PRIVATE 能力投影：supported input/output MIME、native adapter 实测就绪、身份注册有效性、能力版本、不可用原因。直接复用已有能力登记与工具链测量，不能由页面 roster.online 猜测。
- UI 只让用户确认当前真实可用组合；不可用仍可保存草稿，并解释需要上线、配置或换可用格式/好汉。不能无限排队掩盖不支持。
- submit/claim/start 再核验能力与授权快照，避免确认页到提交之间发生变更。
- 费用语义必须明确区分私人文件执行的 Provider 使用与正式悬赏资金；不能因没有悬赏金额就宣称模型免费，也不新增未经确认的扣费。

### R4 / P0：严格核对成果上传/提交回执

当前 bridge 的 stage 主要核对HTTP状态，commit只核对HTTP状态与非空响应体；运行时的通用HTTP解包即使已验证，也不代表业务 manifest 正确。本轮成功信封中的错误成果标识被接受，已独立复现。

- stage 解包后，严格匹配 outputId、sha256、byteLength、STAGED 状态与本次授权执行；需要的业务身份字段在最新合同中明确补全，使用固定 schema。
- commit 解包后，严格匹配 manifestId、COMMITTED 状态、完整且无重复/缺失的 outputs，以及 fileId/fileVersion/MIME/length/hash 等服务端落库事实。
- 对错配、空body、协议错、5xx、断线保留原 manifest/幂等键，按原操作只读查询。没有服务端原回执不能从本地计算值合成成功。
- reportFailure 也要核对失败的原执行和终态回执；读取明确终态后才清理本次临时目录。未知结果保留原所有权/目录恢复证据，不删除其他执行目录。
- 本地终态、后端执行终态、归档文件清单三者一致才确认交付。

### R5 / P1：修正事项页“刷新了但仍等待”的状态优先级

当前 `currentExecution` 优先选 `receipt.execution`，而提交回执永远是当时的QUEUED快照；`loadCase` 更新不会覆盖它。

- 提交回执只证明“创建/交办成功”，不再当实时执行状态。
- 根据当前 case/ref 与 executionId，以服务端最新 stateVersion 的执行投影显示状态；没读取到新投影时才把回执作为标明时间的初始快照。
- 失败读取保留最后一次可信投影并展示“本次核对失败/上次更新时间”，不要先清空后悄悄退回旧QUEUED。
- 区分“本次执行”和“事项最新修订”，不能用另一次执行的结果解锁本次按钮。revision为十进制字符串时按精确整数比较，不依赖减法转换。
- 已完成立即显示查看成果；归档中/受阻/失败提供对应说明。标题和摘要同源派生，删除已完成仍写“尚未取得成果”的矛盾句。
- 回执页面显式呈现读取错误、忙状态、最后确认时间；可见且非终态时适度观察刷新，隐藏/卸载/身份切换停止，保留手动“核对进展”。不增加强制等待截止时间。

**已复现验收反例：** 旧QUEUED回执 + 新OUTPUT_COMMITTED case，应当显示已完成并解锁成果；当前不满足。另覆盖迟到QUEUED、切换用户、换事项、再修订与刷新失败。

### R6 / P1：入口语义、预览下载与修改闭环

- 顶部“提出需求”与办事页一句话入口分别创建PRIVATE/TASK_CREATE，当前后者“开始办事”实际只创建正式任务。明确各自提交是否会开始执行，统一用户可理解的提示；不在未授权的情况下改变私人/正式可见范围。
- 成果按钮使用服务端已提交 manifest 对应的固定 file/version，不取“最新文件”偷换成果；不可用/撤权明确提示，禁止降级到其他版本。
- PDF 实际生成后验证 MIME、文件头、可打开性、页内容、SHA/长度和固定版本预览/下载；界面可点不等于文件真实可用。
- “提出修改”引用原 output/file/version，在同一 case 下创建新修订；原成果可追溯，新执行不能覆盖旧授权或将未确认结果当输入。
- 回归草稿恢复、未保存离开保护、重复点击、授权失效、浏览器刷新及资料撤权，不删除现有保护以缩短路径。

### R7 / P1：把分段单测补成真正跨端验收

现有 frontend 回归与 Runtime queue 测试能通过，但前者主要用替身服务，queue测试用stub processor；两者之间的真实接单失败未被覆盖。

- 固定同批 API/Web/Runtime commit、schema、完整 wire fixture、数据库结构与工具链；禁止手写消费者友好报文代替实际序列化。
- 隔离真实 HTTP/MySQL、真实 Runtime认证和持久存储运行全链；Provider可先用显式标识的确定性替身验证事务/幂等，这只能证明协议，不证明模型能力。
- 再以新建合成资料、明确授权的真实目标好汉做一次真实模型/PDF端到端验收；不要拿原简历反复测试。

## 4. 代码落点

| 范围 | 主要文件/模块 |
|---|---|
| 入口/状态/错误显示 | `/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue`；`/home/isp/wsps/cyf/web/src/components/juyiting/HallDraftEditor.vue`；`/home/isp/wsps/cyf/web/src/components/juyiting/HallOverview.vue`；`/home/isp/wsps/cyf/web/src/composables/juyiting/useHallDrafts.js` |
| 草稿/私人执行/成果 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/HallRequestDraftServiceImpl.java`；`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceExecutionServiceImpl.java` |
| API wire与状态合同 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/PersonalWorkspaceRuntimeFileController.java`；同目录 `WorkspaceExecutionWire.java`、`HallDraftWire.java`、`NativeOutputWire.java`；关联实体/DAO/mapper/schema初始化/overview与private mark投影 |
| Runtime执行与成果校验 | `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs`；`/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/workspace-file-bridge.mjs`；`/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs`；同目录 `runtime-client.mjs` |
| 普通D06必须保护 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentRuntimeV1ServiceImpl.java`；同目录 `AgentCommandAckServiceImpl.java`。不是将普通ACK改为无条件接受PRIVATE |

路径表是影响面，不代表所有文件都要改。实施前沿已有handoff确定精确写集、最新基线和当前并行任务，不能覆盖无关脏修改。

## 5. 实施顺序与验收门槛

1. **冻结最新业务合同与迁移设计**：PRIVATE native 身份/领取/start/输出/终态/恢复与前端投影；建立本轮发现的失败用例。补齐线上首个通用报文错误的安全关联证据。
2. **实现 API + Runtime 真接单和状态闭环（R1/R2/R3）**：从真实producer进入真实adapter，直到确认开始；失败、重放和接单并发先覆盖。此阶段不宣布成果完成。
3. **实现成果闭环（R4）**：真实文件落盘与API stage/commit/readback；先补错回执反例，再验证正确回执。
4. **修复前端显示与恢复（R5/R6）**：可在契约冻结后同Owner并行推进非重叠文件，但不要引入独立Reviewer流程。
5. **精确版本验证与发布**：后端固定干净源码先读build.gradle，经既有orchestrator串行测试/validateLayering/构建；前端正式测试/构建/制品用Flow4403172；Runtime绑定固定制品/工具链。版本化同批制品发布、在线核验，不因develop push自动部署。
6. **开启本次测试执行→观察→再处置原事项**：新建合成案例完成真实链路，证明正确后按第6节恢复旧记录。共享Runtime不得为了本任务抢占或取消其他任务。

### 必须通过的测试矩阵

| 组 | 至少覆盖 |
|---|---|
| 正常路径 | 无附件文本；合成PDF输入→PDF输出；保存再恢复草稿；页面重新进入；成果固定版本预览/下载；基于成果提出一次修改 |
| 接单与身份 | 两Runtime争抢同一执行；错误tenant/client/owner/agent；旧installation/session/attempt/fence；目标未就绪或不支持PDF；确认后能力变化 |
| 幂等与未知结果 | 重复submit；submit已提交但响应丢失；claim/start响应丢失；Provider已启动后Runtime重启；重复stage/commit；提交成功但ACK丢失；同manifest只归档一次 |
| 文件/授权 | 输入版本固定、hash/length不符、撤权发生于领取/读取/生成/提交之间、路径穿越/符号链接、声明PDF实际非PDF、输出集合缺失/重复 |
| 回执/状态 | 200但错误output/manifest、空/错误/越界版本、错误状态；迟到QUEUED覆盖终态；旧receipt与新case矛盾；读取失败可见；跨身份迟到响应丢弃 |
| 旧数据切换 | 原case/execution身份保持；未知Provider结果不重跑；仅一次受控恢复；迁移摘要可追溯；旧消费者停止而非双路并行 |

**最终完成定义：** 同一新建 case/execution 从页面提交，经实际授权接单、实际读取输入、实际模型执行，形成真实可打开PDF，后端manifest与下载bytes/hash一致；页面无需重新提交即可看到成果，刷新仍正确，修改产生新修订且旧成果可追溯。仅测试绿、QUEUED、STARTED回执或本地文件存在都不能算完成。

## 6. 原“简历优化”和存量QUEUED的处置

- 先保留原case/execution、原输入版本及授权，不删除重建、不改成正式事项、不修改原幂等事实。
- **无输出≠从未调用模型。** PRIVATE旧start没有持久开始标志，不能单凭QUEUED/输出数0认定可安全重跑。需对照原Runtime inbox/checkpoint、原操作回执及可用Provider侧证据；未知则维持待核对，不自动重试。
- 切换前盘点所有PRIVATE排队/未知执行，冻结映射和备份；只对本次授权范围进行恢复。发布新adapter不能顺带让全部历史队列突然开始产生费用。
- 确认未开始且授权仍有效的原执行，可在同execution下生成一次新的native attempt绑定并记录迁移关系；有明确终态的仅重放读取；不能确认的由Owner带证据协调处理。
- 迁移保留旧签名/摘要/请求快照的不可变来源；转换生成新版本记录并记录对应关系，不原位篡改历史消息。停止旧PRIVATE消费者后再切换，内测不保留双轨兼容。
- 应用回退仅能回到与数据库/在途协议匹配的已验证制品；不能回退到会重新消费旧消息的版本。先停止**本次范围的新准入**而非停止其他业务，恢复已备份配置/制品并核验身份、锁与健康。

## 7. 本轮证据与可复测入口

证据根目录：`/home/isp/wsps/cyf/docs/implementation/evidence/requirement-execution-20261016/replay/`。

- `baseline.json`：源码/远端/生产JAR指纹。
- `original-case-readonly.tsv`、`runtime-log-summary.txt`：原事项只读快照与安全日志摘要。
- `FlowFixture.java`、`java-flow-fixture.json`、`step-replay.test.js`、`step-replay.log`：生产DTO序列化→真实Vue组件/状态的合成步骤回放，1例；包含唯一一次submit。
- `real-consumer-result.jsonl`：真实队列消费者拒绝，stub接受。原输入与脚本在上级目录 `queue.json`、`consume.mjs`、`Probe.java`。
- `ui-defect-replay.test.js`、`ui-defects.log`：三个缺陷复现（测试为“缺陷存在”断言，不是修复验收）：旧回执覆盖、新完成状态矛盾说明、读取错误隐藏。
- `commit-receipt-probe.mjs`、`commit-receipt-result.json`：实际安装bridge错误回执仍报告成功的反例；无真实HTTP/模型/生产文件写入。
- `frontend-targeted.log`：8个既有前端定向文件，110 passing；是本机诊断，非Flow。
- `runtime-targeted.log`：固定源码隔离副本，使用已安装依赖，按workspace/native queue选择29 passing/199 skipped；不是228项全部通过。
- `bridge-wire-full.log`：file bridge/message-wire两个文件的完整运行，62 passing/0 skipped；与上述选择性测试有重叠，不累加宣称覆盖数。

回放复用项目Mocha、Vue test utils、实际安装Runtime和JAR，没有新增通用runner。Vue证据脚本按原路径导入；复跑时复制到 `/home/isp/wsps/cyf/web/tests/` 下本任务专用临时文件，再用现有Mocha入口并在结束时只移除该文件。普通Vue局部测试的workspace预览/下载服务仍为替身，不能替代真文件验收。临时工具初次运行的目录缺失、测试fixture状态共享等已归因为诊断脚本问题并修正，不计为产品缺陷。

## 8. 未核实项 / 不作承诺

- 线上 `WORKSPACE_FILE_COMMAND_INVALID` 的第一个精确原始报文错误尚未取得逐执行证据；不能把隔离的D06上下文拒绝直接冒充同一错误根因。
- 未进行本场景真实Provider调用、PDF实际语义优化、全新账号/浏览器、生产上传/预览下载验收。
- 未查询和证明线上API/Web精确发布版本闭包；仅记录实际生产JAR hash与安装Runtime路径。
- 不承诺修复工期、模型效果或性能收益；实现与发布等待分别记录，未知计时留空。
