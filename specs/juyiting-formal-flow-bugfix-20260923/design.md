# 修复设计约束与接口核对清单

状态：draft / 1.13.19 solution_defined；方案见 `docs/implementation/V1_13_19_FORMAL_FLOW_BUGFIX_PLAN_20260923.md`。已核对可复用接口，实施前 Owner 仍须补齐身份、持久派发与能力响应的最小变更合同。

## 当前接口与本轮观察

| 接口 | 业务/关键字段 | 本轮结果 |
| --- | --- | --- |
| POST /agent/hall/drafts | TASK_CREATE 草稿，标题/简述 | 201，保存成功 |
| POST /agent/hall/drafts/{draftId}/submit | 用户确认的同草稿提交；ref.sourceType=TASK，task.taskId/taskVersion | 202，taskId=395 |
| POST /agent/personal-workspace/files | 上传测试 TXT，个人文件固定版本 | 201，随后 operation COMMITTED |
| POST /agent/tasks/{taskId}/assign | 显式 agentId；返回 task + actionDispatchResults | 200 assigned，但 queued/未送达 |
| POST /chat/stream | conversationType/scope/key、taskId、目标 Agent、conversationId/forceNewConversation | 榜文议事 404 CONVERSATION_NOT_FOUND |
| GET /agent/tasks/{taskId} | 主状态、负责人、时间、版本 | assigned，开始/完成时间 null |
| GET /agent/tasks/{taskId}/formal-deliveries | items，交付批次/固定成果版本/验收状态 | 200，items=[] |
| GET /agent/tasks/{taskId}/workspace?actorAgentId=... | 受作用域保护的任务快照 | 503 TASK_WORKSPACE_UNAVAILABLE |
| GET /agent/tasks/{taskId}/events?actorAgentId=... | SSE；sinceVersion / Last-Event-ID 游标 | 503 TASK_EVENTS_UNAVAILABLE |

## 必须保持的身份与异步合同

1. browser 使用测试账户既有登录身份；actor/target Agent 显式指定吴用或林冲。ownerJiacn、tenantId、clientId 不能混用；map/roster 不合并，正式任务和私人事项不按同名推断关联。
2. 先定位真实失败分支，再修复合法范围内的派发和讨论。跨 owner/client、非成员、已撤销绑定等必须继续拒绝；对外错误不泄漏不属于用户的任务信息，内部保留可追踪原因码。
3. taskId → commandId → receipt/run/workItemId → artifact/version/hash → formalDeliveryId/revision → decision 的关联可回查。主状态由权威执行/验收事实驱动，不凭 presence=busy、聊天说“完成”或文件出现在百宝箱便认定完成。
4. 用户一次动作的未知结果必须先核对原意图；重发使用既有幂等语义。事件支持作用域隔离和断线游标重放；轮询仅查询，不触发新执行。拒发不能仅以 queued 标签伪造持久队列。
5. 复用 `/agent/tasks/{taskId}/file-links`（fileId/version/role，INPUT 或 REFERENCE）和 `/agent/personal-workspace/executions` 的 TASK 模式；选材关联不授予 runtime 读权限，明确执行时创建固定输入授权。TASK 模式要求匹配的 conversationId/目标和恰好一个 ready 必需工作项；有效 CAS/lease 领取与 start 不能跳过。没有真实 taskId/fileId/version/授权关联前，不传用户其他个人文件给 Agent。
6. 正式提交保留有效 lease、CAS、固定 artifact/version/hash；submitted ≠ accepted。验收修改产生 changes_requested，明确启动返工后产生新 revision，不静默自动付费重跑。当前单必需工作项限制先如实支持，不扩张多项完成承诺。
7. 资金结算不在本次测试或自动验收副作用内。归档保留原结局，不用归档代替完成。

## 展示/导航

- 展示任务生命周期与派发/执行子阶段、最近真实事件、等待对象及下一步。等待久显示耗时，不凭 SLO 自动取消/失败。
- 主状态一份完整定义供文案/样式/筛选/统计；未知态禁止默认 open。
- 第三级业务选材允许同层详情或局部返回，不强行突破到无限嵌套；保留 originating taskId、文件版本、筛选/滚动。
- 能力未启用与网络故障分别提示；缺工作空间/事件时不能伪造空数据或健康状态。

## 源码核对入口（不是已确认最终根因）

- API `AgentServiceImpl`：assignTaskInternal、listTaskWritableMemberAgentIds、buildTaskBriefingIntent。
- Chat `AgentWebSocketHandler`：publishAgentAction、sendDirectMessageToAgent、resolveTaskMemberAgentIds。
- Chat `ChatController#getOrCreateConversation`、`JuyitingConversationScopeService#authorize`：任务 scope 与受保护 task-thread 路由。
- API `AgentTaskEventsGate`、workspace/events Controller：503 分类、开关及 allowlist。
- Web `useHallConversation.js`、`BountyPanel.vue`、`JuyiHall.vue`、`PersonalWorkspace.vue`、`HallDraftEditor.vue`。
- Runtime 当前部署目录及摘要见证据 manifest；不得因为林冲“在线”便忽略其启动日志 WORKSPACE_POLICY_REQUIRED 警告。此为配置风险，未向林冲派发命令验证，不记作实际执行失败。


## 1.13.22 增量设计（未改变原冻结版本）

- BF-10 不增加HTTP/WebSocket接口，不提高10秒观测阈值，不引入自动重发。`ack_timeout`仅表示慢注册观测；仍保留 messageId/runtimeInstanceId/agentId 精确校验。只有合法回执能建立内存 token，token不落盘不打印；断线、下一次注册、send_failed、rejected 继续使前请求失效。收到迟到回执后沿用既有 poller 和持久 inbox 去重，不直接执行或补发命令。
- BF-11 方案：复用 owner `POST /agent/personal-workspace/executions/{executionId}/revoke-inputs` 的身份、expectedGrantRevision、Idempotency-Key；新增内部“精确过期回收”分支须在同事务内核对持久 task/workItem/assignee/token/version/expiry，不得复用跨任务批量扫描作为测试恢复。运行租约仍走原release；过期租约只回收到ready/failed，不复活。已换租约不得释放新Owner工作；已正式提交不得撤销正式交付。Web提供明确撤销及原请求核对，不在读取/刷新时自动改动或自动重跑。
- BF-12 方案：只有明确 Agent 开工事实才驱动主任务 running 与 startedAt；队列等待、租约领取、Provider调用、输出提交、正式submitted、用户accepted分别显示。先补生产已观察到的assigned/running差异回归，不简单把主任务置running以制造通过。
- runtime服务共享吴用/林冲/卢俊义；当前MainPID1995806不归本任务独占。已发conflict-alert，不操作现有进程或inbox；本地构建授权不推导foreign进程控制权。发布需明确本次服务操作Owner/授权、确认无在途工作、绑定旧PID/start ticks/current与候选摘要；保持可恢复安装。

### 2026-09-24 BF12 native 开工合同补充（候选，未发布）

现有 `pwe_cmd_*` 来自独立工作区队列，并不存在于 D06 command delivery 表；不能把普通 websocket `STARTED` 发出当作主任务状态已落库。新增 native-only `POST /internal/agent/tasks/{taskId}/runs/{runId}/start`，请求 `{commandId,messageId}` 必须匹配持久 execution 派生的精确命令/消息 ID。返回 `{executionId,taskId,runId,state:"STARTED"}`；不是 Provider 成功或交付事实。

- Runtime 下载并校验固定输入后、调用 Provider 前发起一次 start；直连 200 且回执精确匹配后才能继续。未知结果不重发、不调用 Provider，由现有恢复流程处理。
- API 从已认证 runtime 取得 tenant/client/owner/agent/runtime，不接收浏览器身份覆盖。TASK root → execution → 原租约检查；只允许当前 assigned→running（既有 startedAt/版本 CAS/事件服务），同一有效执行且 root 已 running 幂等返回；不恢复 blocked/reviewing/终态，不自动续租或重跑。PRIVATE 仅确认有效执行，不创建公开任务状态。
- 开工状态代表 Agent 已开始处理固定输入后的正式办理，不代表 Provider 已经完成；浏览器创建 QUEUED、只读 GET、下载 GET 均不推进主状态。
- 新客户端需要新 API；先 API，再 runtime；已冻结 runtime release/1.13.22 不改写，新 runtime 候选使用 1.13.23。

### 1.13.25 BF19–BF21
- HTTP读取在真实EsRequestWrapper下只获取一次InputStream，保留64KB上限与严格JSON结构验证；不改ACL或事务。
- 验收POST `/agent/tasks/{taskId}/formal-deliveries/{deliveryId}/decision` 的 expectedDeliveryVersion 来自 deliveryVersion，不是revision。要求修改仅记录验收决定，不自动重调Provider。
- 正式返工面板仅在已确认该榜文议事、唯一已指派Agent且用户明确选择该Agent时读取既有会话成果API；使用服务端正式交付ID、决定版本、文件ID与版本。成功决定后刷新只读成果，显式点击创建返工；不使用私人/其他榜文上下文。
- 本机真实OOM与空间紧张已有证据：测试、构建、浏览器串行；仅对本任务不可变同hash制品/回退副本做保留路径的物理去重。新API部署对旧live JAR建立同文件系统硬链接回退，新的stage以rename替换live，不覆盖旧inode；保留原权限及所有摘要，不触碰其他任务目录。

### BF23：明确返工同时授权精确源文件为INPUT
真实#397 r1要求修改成功后，PDF仅为PUBLISHED执行成果，未存在用户INPUT/REFERENCE链接。返工适配器此前没有建立链接，正常TASK queue因此以NOT_FOUND拒绝。修复复用PersonalWorkspaceTaskLinkService，在原@Transactional/root lock内，正式交付状态/决定版本/owner/固定源版本核验之后创建INPUT，再调用ExecutionService。链接幂等键使用独立命名空间及原返工键SHA-256；执行失败连同链接一并回滚。现有INPUT鉴权不变，不把sourceOutputRef作为绕过门禁的标志。
