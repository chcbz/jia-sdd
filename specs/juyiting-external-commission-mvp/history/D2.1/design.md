# 外单最小闭环详设 D2.1

> 2026-10-21；提案而非现有接口说明。公共规范固定为 `/home/isp/wsps/cyf/api/docs/interface-standard.md` 1.2，SHA-256 `7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f`；公共 `protocolVersion=1`，技能执行仍为 protocol4。原设计基线见 `baseline.json`；本轮复核见 `evidence/design-recheck/` 与 `design-recheck-20261021.md`。§11为D2.1必实施细化，覆盖前文简述中的歧义。源码证据和未核范围见 `impact.md`。

## 0. D2 用户确认与被移除的默认限制

- 逐 Agent 独立开关：chcbz 可独立开关吴用/林冲；任何其他用户对本人 Agent 同理。每单单 Agent，不是系统只能开放一个 Agent。
- 开启即面向同平台所有已认证用户；不做客户名单、任务类型/技能服务目录或费用前置条件。
- 能力仅用于推荐。`canAssign/canCommission` 不得由能力标签、match score、skill readiness、成本是否已知决定。实际能否启动某个动作另作真实运行判断，不伪造工具能力。
- 平台不在本期报价/结算。后续交付费用根据委派内容另行估算；模型调用费用是独立成本信息，不是交付价格。
- D1/D1.1 的 AUTO_ALLOWLIST、IMAGE_EDIT 服务限制、固定接单技能、单主执行/单次效果、拒绝返工和成本确认准入全部撤销。图片保留为验收案例。
- 本文不授权绕过身份、任务归属、资料 ACL、Runtime 凭据、effect 幂等或实际工具权限。业务开放与安全隔离不是同一个维度。

## 1. 为什么不能只改 canOperate

当前 Web 的 `canAssign` 依赖 `canOperate`，后者源于 `boundToMe`；普通派单/推荐、执行 grant 的 target 锁、PWE 创建与 Runtime 领取/输入/输出仍将任务 Owner 与 Agent Owner 混用。技能目录已有 runtimeScope 分离，但不覆盖整条链。另有 ChatDeliberationOutboxRelay 用任务 Owner 选择 WS 通道；只修 HTTP 领取不足以使任务内议事正常工作。

本设计保留现有任务、grant、技能执行、effect、outbox、结果与正式交付；只新增**接单政策和委派关系事实**，不建立第二套任务/订单/执行系统。

## 2. 双主体模型与授权矩阵

### 2.1 服务端类型

- `TaskOwnerScope(tenantId, clientId, ownerJiacn=A)`：任务、会话、需求、资料、执行业务记录、成果归属。
- `AgentPrincipalScope(tenantId, clientId, ownerJiacn=B, canonicalAgentId, bindingId)`：从真实身份注册表解析，负责 Agent/安装/模型连接。
- `RuntimePrincipal`：当前认证的 AgentPrincipal + installation/host/runtimeInstance/sessionGeneration，不从浏览器或模型读取。
- `TaskTargetAuthority`：服务端解析的权限结果；同主任务由 OWNED 权限来源授权，外单由有效 DELEGATED 关系授权。两者进入同一执行系统，不能新增 owner 字段缺省回退或旧版解析分支。
- `DelegatedExecutionContext`：不可变 taskOwnerScope、agentPrincipalScope、delegationId/revision、task/assignment/grant/requirement revisions；动作阶段另冻结真实 skill/source snapshot。只能由可信服务层创建。

`canOperate` 继续表达原管理/本人操作资格，不改成“公开可操作”。统一候选读模型增加 `relation, canAssign, canCommission, assignmentBlockedReason`，能力推荐与实际运行状态另列；任务内继续使用服务端 `actions`/能力裁决，前端判断不授权。

| 操作 | A 下单人 | B 服务方 | 目标 Agent Runtime | 无关 C |
|---|---|---|---|---|
| 接单开关/技能或连接配置 | 否 | 原本人权限 | 原专用管理协议 | 否 |
| 已开放的 Agent 脱敏摘要 | 同平台可见 | 可见自己 | 不适用 | 同平台可见；不因此获得 A 的任务权限 |
| 创建/修改 A 的需求和资料 | 原权限 | 否 | 否 | 否 |
| 委托 A 的任务 | 本人任务＋外部 Agent 已开放 | 开关表示预先接单意愿 | 不自行发单 | 不能操作 A 的任务；可创建自己的任务下单 |
| A 的任务内会话 | 原本人权限 | 默认不可读正文 | 本单有效委派下的必要上下文 | 否 |
| 输入文件 | 原 ACL | 默认无下载权 | grant 指定的 fileId/version/hash | 否 |
| 进度/结果 | 原本人权限 | 精简接单状态，不含客户正文 | 仅自己目标执行的回执/恢复 | 否 |
| 正式验收 | A | 否 | 否 | 否 |
| 取消委派 | A | 可撤回自己服务义务 | 仅确认/报告，不伪装取消人 | 否 |

Runtime 主机管理员可能接触本机处理过的输入；应用 ACL 不等于对宿主机所有者的密码学隔离。委托页须说明资料将交由该 Agent 运行环境及其模型服务处理；不承诺 Provider 零留存。不设置提供方或客户名单，但委托前明确上述信任边界，由用户选择提供方。

### 2.2 通用解析原则

1. JWT 请求先按 A 验证任务/会话权限，再解析目标真实身份 B，验证服务政策/委派。
2. Runtime 请求先验证 B 的当前凭据及 session fence，再按其 canonicalAgentId、bindingId 和执行标识解析持久委派，得到 A；随后在 A 的任务根下复核 grant/assignment/资料。
3. 不接受浏览器/模型声明的 `ownerJiacn`、`executorOwnerJiacn` 作为授权；不允许仅凭 taskId 找到 A 后直接读取。
4. canonicalAgentId 与 binding 必须精确匹配。相同名字、重绑、旧 installation/旧代际都不能继承外单。
5. 所有 owner 比较按既有精确语义，保留真实平台/租户隔离。平台范围由可信认证解析，不由body指定；若同平台用户使用不同OAuth客户端，须核对其映射而不是用登录client差异偷偷限制开放范围。未经可信映射不能放开跨域读取。无任务授权仍不能枚举私有安装、输入或历史。

## 3. 数据变更（逻辑模型，实施时落正式迁移）

### 3.1 新表 agent_external_service_policy

每个真实绑定一条逻辑政策，采用不可变修订行：

- `tenant_id, client_id, agent_id, agent_binding_id, provider_owner_jiacn`：从可信平台域与注册表派生，不信任浏览器自报。
- `state: DISABLED|ENABLED`，`revision: BIGINT`；无行表示 DISABLED/revision=0。
- `idempotency_key, request_hash, mutation_receipt_json, updated_by, created_at`。
- 唯一键 `(tenant,client,agent,binding,revision)` 与 `(tenant,client,providerOwner,idempotencyKey)`。

**不增加 allowed_requesters、service_code、acceptance_mode、skill选择、Provider成本确认等字段**。同平台开放是统一产品规则，不用另一个可配置受众策略偷偷收窄。

取该绑定最大 revision 后判断开关，不能过滤 ENABLED 再误读旧修订。写入先验证本人当前绑定、解析幂等回执，再在原 identity/binding 锁下验证 expectedRevision 并追加修订；首行也由身份锁串行保护。入单和开关更新共享 identity→policy 顺序。开关不依赖技能/模型/Runtime在线/成本描述源，不触发Provider或注册。

### 3.2 新表 agent_task_delegation

本表是双方授权与请求回执事实，不拥有第二套任务生命周期：

- `delegation_id, tenant_id, client_id, task_owner_jiacn, task_id`。
- `target_agent_id, agent_binding_id, executor_owner_jiacn`；入单时冻结真实 B。
- `service_policy_revision, service_policy_snapshot_sha256`：记录接受时的开关事实；不冻结任务类型、技能选择或成本资格。
- `requirement_revision, assignment_revision, grant_id, grant_version`：保存接单时的授权基线；后续执行从原 grant/current-requirement 服务解析最新有效授权，不能把初始grant永远当当前值。
- 接单时的需求/初始输入摘要（允许空列表）；具体执行的 input snapshot 绑定当次 grant/需求修订。原文件字节不复制到此表，后续资料变化生成新修订不覆盖旧快照。
- `state: ACTIVE|REVOKED|COMPLETED`、`revision`；终态不可重开。
- `idempotency_key, request_hash, admission_receipt_json, admitted_by, admitted_at, closed_at, close_reason`。
- 首次撤回的 `revoke_actor, revoke_idempotency_key, revoke_request_hash, revoke_receipt_json`，与撤销状态同事务保存；相同actor/key异body冲突，已终态的新撤回请求仅返回当前状态且无副作用，不覆盖原撤回事实。

唯一约束：`(tenant,client,taskOwner,idempotencyKey)`；`(tenant,client,taskOwner,taskId,assignmentRevision)`；delegationId 唯一。每任务至多一个活动委派，由同任务根锁串行保证，不能仅靠先读后写。不同 key 不能重复创建同一活动委派；合法的新动作可在这一个委派下创建多个 execution，不能把唯一委派误实现为唯一 execution。

### 3.3 扩展既有记录

- `agent_task_execution_grant`：新增可空 `delegation_id`（OWNED 无委派）；grant 的 owner 仍是 A；授权为本单任务上下文与明确授权资料；具体操作仍由已有任务/动作授权服务校验，不限制一个委派只能执行一次，也不以“所有任务类型”授予所有工具。
- `agent_personal_workspace_execution`：新增 `executor_owner_jiacn`、`executor_binding_id`、`delegation_id`；新创建记录必须填真实 executor，原 `owner_jiacn` 保持 A。索引围绕 `(tenant,client,targetAgent,executorBinding,executorOwner,state,createdAt,executionId)`，具体 DDL 以现行列宽和 EXPLAIN 为准，不新增无证据性能门禁。
- 每次动作的技能/非技能执行快照增加服务端授权来源/委派关联，继续用现有 canonical JSON/digest 算法；新生产者和消费者同步切换，不重算已冻结历史 snapshot。
- Chat outbox/入站关联需要保存 taskScope → executorScope 的可信绑定和 delegationId/revision；沿现有持久上下文扩展，不把 B 覆盖进原 A 的 owner 字段。
- 结果、输入、会话、正式交付的 owner 字段不改；不复制 A 的整个工作空间给 B。

## 4. 接单、执行和交付时序

```text
B：选择自己某个 Agent → 开启接外单（不配置客户名单、类型或费用）
A：创建任务 → 统一候选列表选择“我的Agent”或“已开放的他人Agent”
API：按真实归属走 OWNED 或 DELEGATED 授权 → 原事务写入assignment/grant；外单另写delegation
A：进入自己的任务办事页 → 发送需求/补充资料（沿原requestId和任务会话）
Chat：冻结本轮任务上下文 → 路由到执行Agent真实认证通道
Agent：按实际能力回答、澄清、执行工具或多步处理；无法执行则明确报告
API/Runtime：逐动作认证与输入/效果/结果校验 → 结果归A → 原成果/正式验收
旁路：记录实际模型用量和可得成本；不改变接单、执行或验收资格
```

**D2 不做新的“一键委托并开始”跨模块事务。** 入单只保证委派已提交，不宣称模型已启动；现有办事页发送指令是单独的可恢复动作。浏览器在入单后断开，刷新仍可查到“已接单，待发送指令”，不能自动换 key 重新下单。后续一键入口可用既有持久 bootstrap/outbox 扩展，但不纳入本轮。

### 4.1 入单事务

事务外可读取推荐或在线状态作展示，但失败/未知不能阻断入单；真实身份、开关和任务授权来源失败必须拒绝写入。不能调用 Provider 或发送 WS 消息。先解析幂等回执；同 key 同摘要返回原回执，同 key 异摘要冲突。已接单后政策关闭不能让重放变成“重新下单”。

在现有 task-root 事务内复核版本与幂等事实后，按真实共享调用链锁定身份/政策/资料并写入assignment/委派/grant/事件。**D2.1代码复核发现现有assignLocked在task-root下先锁grant-action、bootstrap-action，再进入身份和输入锁；不能将D2简写的task→identity→grant当作已验证全序。新增外单编排必须保留共享前缀并为policy确定无反向边的锁序，覆盖所有admit/撤回/执行分支后再冻结。** 政策管理只锁identity→policy，不扫描并锁住全部任务；不得形成policy→task路径。

提交前复核任务/需求版本、明确输入的资料链接、Agent 非系统且真实绑定有效、外部目标开关已启用、assignment 未被抢先修改。不得要求能力匹配、技能READY、成本已知或Runtime在线。离线/忙碌由现有持久待办/outbox等待调度；先接单不表示执行已开始。任何一步失败整笔回滚；事务物理提交后才允许 outbox 投递。重用 task mutation/assignment writer，不手写一份事件或直接 UPDATE assignedAgentId。

### 4.2 能力、讨论、动作与幂等的分层

- **推荐层**：能力标签、已公开的能力摘要只计算 score/reason，不参与授权。低分、未知或缺标签的 Agent 仍可被手动选中；不能把原 recommendation.eligible 的“能力不足”直接绑定按钮disabled。
- **派单层**：只检查任务可委派、真实目标及外部开关等业务身份/状态条件；不检查任务类型、技能或成本。本人路径也不得继续用 validateAbility 将能力不足当硬门槛。
- **执行层**：availableActions 来自真实安装/当前Runtime能力与本单授权的交集，不按服务政策限定 IMAGE_EDIT。具体工具缺失、凭据失效或资料未授权时，不能执行那个动作，但应返回真实可理解的原因/澄清，不回写“禁止接此类订单”。
- 任务内会话与普通密议权限仍分离；只注入本单上下文与授权资料，不注入 B 私人记忆或全工作空间。实际工具的沙箱/运行权限继续保留；不新增“外单一律禁某runner”的业务名单，也不因开放任务类型自动获得shell/宿主文件权限。
- 同一 delegation 可有多个 action/execution/effect。使用既有 request/turn/actionEventId/operation/effectDigest 链标识逻辑意图；同一意图重投不得产生第二份执行，同 effect 重试不得重复副作用。不能用“整单只执行一次”替代幂等。
- 新一轮明确需求/返工可产生新的动作与效果，但 RESULT_UNKNOWN 不能借新 key 自动重做。业务允许多次执行与禁止盲重放未知副作用并不矛盾。
- 需求/资料变化沿原修订链重新校验授权，生成新快照；旧执行/结果不可覆盖。非终态任务可继续办理；已正式验收的任务按原重新办理/后续任务机制推进，不擅自复活旧终态。
- 文本/结构化回答可以走原 completed-message 正式交付源；文件任务走真实文件结果，不强制所有任务都创建图片/技能 execution，更不能把文本“已完成”冒充请求的文件。

## 5. HTTP 接口提案

新增路由下列字段都是 `data` 内业务对象；使用公共信封、鉴权、十进制字符串 int64 和 `Idempotency-Key`。未知字段/非法状态拒绝。查询无副作用，私有响应 `Cache-Control: private, no-store`。

### 5.1 B 管理接单开关

- `GET /agent/{agentId}/external-service-policy`：仅当前真实绑定拥有者；返回 `agentId,state,revision`。界面说明“开启后同平台所有用户可委派，关闭不取消已接订单”。
- `PUT /agent/{agentId}/external-service-policy`：同权限；`data:{expectedRevision,state}` + Idempotency-Key。只修改该 Agent 开关；状态/版本更新不调用Provider，不依赖技能、客户配置、费用或Runtime在线。返回固定政策回执。
- 不接受 allowedRequesterIds/serviceCode/skillSelection/expectedProviderBindingDigest 旧提案字段，不维护D1兼容分支；新接口尚未实现，不存在生产数据迁移这些字段的需要。
- 关闭只停止新外单，既有外单继续；本人任务也不受接外单开关影响。逐单撤回另行处理，不批量杀进程。

### 5.2 统一候选与推荐

新增 `GET /agent/tasks/{taskId}/assignee-candidates?scope=ALL&cursor=...`；仅任务本人JWT，scope可为 `ALL|OWNED|EXTERNAL`，默认ALL。服务端统一分页合并“本人真实Agent”和“同平台他人已开放Agent”，canonicalAgentId去重；本人条目优先归OWNED，不因开关关闭消失。

返回 `items,nextCursor,taskVersion`，item：
`agentId,displayName,providerDisplayName,relation,externalServiceState,externalPolicyRevision,canAssign,canCommission,assignmentBlockedReason,recommendationScore,recommendationReasons,capabilitySummary,availability,executionReadiness`。

- relation为 `OWNED|EXTERNAL`；本人条目 externalPolicyRevision=null。canAssign表达任务对该Agent的真实派单资格；canCommission只表示外单入口适用且有资格，不用于禁用本人入口。
- recommendationScore未知为null，capabilitySummary只含公开/允许投影的摘要。推荐计算失败仍返回有权查看的候选、标记推荐不可用，不伪造分数/屏蔽Agent。
- 默认可按推荐分排序，但所有合法候选通过分页可达；不能只返回Top5来变相禁止选择低分Agent。稳定排序/游标固定同一查询代次，身份/任务变化使旧页失效。推荐只排序，不自动点将或代替人的选择。
- availability展示在线/离线/忙碌/未知；executionReadiness表示当前运行观察，不影响canAssign。队列/输入/执行故障由相应运行状态表达。
- 不公开内部Owner账号、endpoint/PID/installation/host、当前其他客户任务、凭据或私有完整安装目录。
- 原本人Agent管理名册不扩权。任务承办选择入口改用此DTO；如保留原recommend接口，它也须覆盖同一候选授权范围且不能因能力不足标不可选，不在前端用旧owned列表再次过滤。

### 5.3 A 委托

`POST /agent/tasks/{taskId}/external-commissions`，本人任务 JWT，Idempotency-Key 必填。

```json
{
  "protocolVersion": 1,
  "requestId": "opaque-request-id",
  "data": {
    "targetAgentId": "canonical-agent-id",
    "expectedTaskVersion": "7",
    "requirementRevision": "2",
    "expectedServicePolicyRevision": "3",
    "inputRefs": []
  }
}
```

这是无附件任务的合法示例；inputRefs可为明确的fileId/version列表，不限制图片类型。后端冻结任务、真实主体及已授权输入摘要；技能/模型快照在实际动作创建时冻结，不在接单时选服务类型。浏览器不得提交 taskOwner/executorOwner/providerKey/费用授权。资料需经过原任务链接ACL，上传完成不等于本单授权。

只有EXTERNAL目标调用此入口，OWNED目标沿原本人委派入口，但必须同步移除能力/在线状态硬门槛并验证原durable bootstrap等待路径；不得通过前端伪造relation绕过服务器判定。成功 `201`，同请求重放 `200`：返回 `delegationId, delegationRevision, taskId, taskVersion, assignmentRevision, grantId, grantVersion, targetAgentId, state:"ACTIVE", nextAction:"SEND_TASK_INSTRUCTION"`。ACTIVE 只表示双方授权已接受，不是 RUNNING。响应不包含内部身份或 lease。

- `GET /agent/tasks/{taskId}/external-commissions/request`：A + 原 Idempotency-Key 查询固定回执，无写入。
- `GET /agent/tasks/{taskId}/external-commissions/{delegationId}`：A 的完整业务状态；含既有 execution/交付关联与可用 actions，不暴露内部凭据。

### 5.4 B 接单视角与撤回

- `GET /agent/{agentId}/external-commissions?cursor=...`：绑定拥有者；返回自己的 delegationId、客户脱敏显示标识、接单时间、进度类别、异常码；不返回标题/正文/输入预览/输出下载链接。关闭后的历史范围不能移交给 Agent 新拥有者。
- `POST /agent/external-commissions/{delegationId}/revoke`：仅该委派 A 或冻结的 B 且其管理权限仍有效；`expectedDelegationRevision, reasonCode` + Idempotency-Key，返回当前状态。内部先解析参与关系再进入 A 的任务根事务；不把 B 设为 A 的 JWT context。
- A 通过原任务取消接口取消时，同一状态转换内撤销委派及 grant；与上述接口汇合到一个可信取消服务。

### 5.5 错误与重放

| 场景 | HTTP / 稳定业务码（新增码提案） | 行为 |
|---|---|---|
| 未认证 | 401 / UNAUTHENTICATED | 不查询资源 |
| 非本人任务、真实跨平台/租户、目标不存在 | 404 / EXTERNAL_SERVICE_NOT_FOUND | 避免存在性泄漏 |
| 合法用户请求已变化政策/任务/输入 | 409 / COMMISSION_VERSION_CONFLICT | 刷新后由用户决定，不自动重发新 key |
| 同 key 不同请求 | 409 / IDEMPOTENCY_CONFLICT | 无第二笔副作用 |
| 已有活动委派/不允许任务状态 | 409 / COMMISSION_STATE_CONFLICT | 返回可恢复状态，不改派 |
| 目标关闭外单、绑定撤销或身份失效 | 409 / COMMISSION_TARGET_UNAVAILABLE | 不新建委派；不能把忙碌、离线或能力不足放进该错误 |
| 任务/身份/开关权威来源失败 | 503 / COMMISSION_SOURCE_UNAVAILABLE | 不伪造授权；推荐/成本描述源失败不属于此准入错误 |
| 失效委派/输入/绑定 | 409 / DELEGATION_REVOKED 或原 grant 错误 | 不继续新效果；历史回执可查 |
| 非法字段/请求结构错误 | 400 / COMMISSION_BAD_REQUEST | 不是拒绝某类业务任务 |

接单政策 PUT/撤回/入单的请求摘要必须包含路径资源、操作、版本和规范化 body；requestId 不是幂等凭证。超时先按原 key 查回执；结果未知不能更换 key 再执行。

## 6. Runtime 与 Chat 双向路由

### 6.1 HTTP 执行链

沿用 `/internal/agent/tasks/conversation-executions/commands` 及 `/{taskId}/runs/{runId}/conversation/{lease,inputs,effects,resume,result-commits,...}`。

- 队列 SQL 不再用 `execution.owner_jiacn=Runtime.owner`。按可信 executorOwner/binding/target 精确索引候选，再在事务内复验当前委派和 grant。
- 根据 `taskId/runId` 查执行时必须同时绑定认证目标和 executor identity，不能开放一个“按任意 taskId 查 taskOwner”的接口。
- lease、inputs/content、stage、effect/start、effect/result、resume、commitResult、failure 全部用同一 `DelegatedExecutionContext`；`skillOwner(RuntimeScope)` 这种自动把 Runtime Owner 当数据 Owner 的捷径不能用于外单。
- 文件/输出/skill execution/effect 业务记录以 A 查询；目录/entitlement/provider 绑定以 B 查询；Runtime 会话 fence 仍以 B 验证。
- 现有 protocol4 command 严格 schema 默认不加 owner 字段，客户端无需自行选租户/Owner。身份映射由服务端记录完成。任何确需新增字段必须同步 exact-key parser、digest fixture 和恢复数据，不容忍“多塞字段试试看”。
- `resume` 仅恢复同一执行与真实效果结果。Provider 已开始但结果不确定时保留 RESULT_UNKNOWN，不再次调用来补齐成功。

### 6.2 任务议事 WS

- `ChatDeliberationOutboxRelay` 的数据 Owner 保持 A；从持久委派解析 B 后用 B 的真实 session 发送。
- 出站任务上下文增设 `taskAuthorization:{delegationId,delegationRevision,grantId,grantVersion,assignmentRevision}`（revision 全为十进制字符串），与原 task/conversation/turn/request 绑定。仅服务端生产；不是持有人可任意访问的 bearer token。
- 模型只看必要需求/资料/动作，不把该授权对象变为模型可修改工具参数。
- Runtime 接收后保存原关联并回送事件关联；外层 runtimeAuth 始终是 B，不能用上下文中的 A 覆盖凭据。
- 入站 typed outcome/delta/final 先验证 B 会话，再按待处理 turn/outbox 解析 A 和授权对象，精确匹配原 task、conversationGeneration、目标和 grant；不得信任回包自报 owner。注册/presence/普通上报的 owner 仍必须等于 B，不全局放宽 AgentWebSocketHandler 的 owner 校验。
- 过期 delegation/turn/fence 的迟到结果不写入新会话；取消 ACK 和已开始 effect 的审计回执可按第7节的恢复权限处理。
- 最终 SSE 和消息写入仍是 A 的会话。B 的接单列表只投影精简状态，不订阅 A 的整条 SSE。

### 6.3 任务事件、投影与重放

不新增事件总线。委派写事务在原任务 event/outbox 写入持久事实，提案业务事件为 `DELEGATION_ADMITTED`、`DELEGATION_REVOKED`、`DELEGATION_COMPLETED`；映射的 wire `messageType` 分别为 `task.delegation.admitted`、`task.delegation.revoked`、`task.delegation.completed`。实现须同步原枚举/schema/投影消费者，不发射未登记类型。

事件 `data`：`taskId, delegationId, delegationRevision, assignmentRevision, grantId, grantVersion, state, actorRole, reasonCode`。版本采用十进制字符串；`actorRole` 仅 `REQUESTER|PROVIDER|SYSTEM`，不公开双方内部账号。沿原 task event cursor 有序重放；公共 messageId 在重投时保持不变，恢复游标沿现有流合同，不把 delegationRevision 冒充全流游标。

- A 的任务流按 A 的授权过滤。B 的接单列表 D2 仅 GET/手动刷新，不把 A 的任务流直接转发给 B，也不新增跨用户SSE频道。
- 投影按 messageId 去重，按 task/assignment/delegation revision 拒绝旧事实覆盖；终态不被晚到 progress 改回运行。任务/执行/交付原事件继续有效，委派事件只补充参与授权事实。
- 结果提交、会话成果投影、正式验收仍是不同可恢复阶段；掉线后读取权威任务/成果再接流，不把事件缺失解释为“没有执行”。
- 持久委派 COMPLETED 的写入应在已有正式验收事务内；若现行交付跨事务，通过同一 durable outbox幂等推进，不在HTTP返回后仅靠内存回调更新。

### 6.4 Runtime 本地隔离

- 凭据和 provider binding 仍按 B 的完整认证主体；不创建 A 的 Runtime 注册或假冒 B 的下单人登录。
- 任务会话 thread key 必须包含完整任务数据 scope、taskId、delegationId、conversationId/generation 和 Agent 真实主体；同名/同 ID 恶意碰撞不得串 thread。
- protocol4 本地 store 保持完整 Runtime scope + 全局 executionId + immutable command digest。每次输入/输出/scratch 仅当前 execution；相同 executionId 不同 command 必须拒绝。
- 外单任务议事不复用 B 私聊 thread 或知识库检索权限；输入只经授权 API 材料化，不接受本地路径/远端 URL 指令越权。
- 复用各runner已有权限和隔离边界。image-provider只是一个例子：仅接收授权输入与指令，凭据留在broker；其他真实已实现runner同样按本单授权与实际工具权限运行，不因外单身份自动放开本机目录。

## 7. 状态、取消、并发和成本

不增加平行任务状态机。委派事实 ACTIVE/REVOKED/COMPLETED；面向用户的“待指令/议事中/执行中/待验收/已完成/已取消/异常”由既有任务、turn、execution、delivery 权威状态投影，不能用一个字符串覆盖全部状态。

| 事件/竞态 | 固定规则 |
|---|---|
| B 关闭接外单 | 只阻止新单；既有单按冻结政策继续，若要取消逐单撤回 |
| A/B 撤回发生在 effect/start 前 | 原任务锁内撤销委派/grant、阻止新动作/输入/效果；不触发 Provider |
| 撤回与 effect/start 并发 | 以同一锁/CAS 决定先后。start 已持久准入即可能产生成本，不承诺外部调用可撤销 |
| Provider 调用中撤回 | 停止新工作；明确“取消已受理，外部调用可能仍在执行”；不杀共享 Runtime |
| 撤回后的旧效果回执 | 仅认证原执行者且匹配 start/lease/effectDigest 的审计/恢复写入可接受；不得恢复输入读取、再次 start 或把任务改成功 |
| 撤回后的文件归档 | 仅对撤回前已准入效果，复用受限 stage/commit 恢复权限，写 A 的隔离历史产物，标记取消后到达；不自动正式交付/验收 |
| result commit 与取消并发 | 结果事实可以存在，但正式交付/验收按任务当前版本判定；取消后不得晚到“完成”事件复活任务 |
| 委托请求重复/WS 重投 | 同一逻辑意图返回原事实；不重复创建对应委派/执行/效果；新合法动作不受整单次数限制 |
| 技能/Provider 绑定变化 | 已冻结动作不偷换连接/摘要；新的合法动作重新解析当前真实配置并冻结新快照，不以成本描述变化取消委派 |
| Agent 重绑或身份撤销 | 原委派不能由新主体接管；未开始停止，已开始结果进入身份/恢复规则，无法确认则明确 UNKNOWN |
| 断连 | 保留真实状态，按原恢复链重连；不靠定时自动换 Agent、取消任务或重复调用 |
| 单次执行失败/验收不通过 | 保留失败执行/成果，委派不自动完成；任务非终态可按原修订链继续，取消/换承办由明确操作推进，不静默重试未知效果 |
| 尚未发送指令 | 保持已委派待办理，可继续或由用户取消；不引入自动过期/硬等待deadline |
| 更换承办 | 复用原任务状态转换，撤销旧委派/grant后生成新assignment与委派；旧执行回报不得写入新承办结果 |
| 验收 | A 的既有正式交付事务成功后委派 COMPLETED；Provider 返回/RESULT_COMMITTED 本身不代表任务验收 |

### 7.1 成本展示与未来交付费用分离

- 本期不产生交付报价/应付额，不运行钱包/余额/冻结/扣款/结算，也不把“费用暂不处理”表示成“模型免费”或“交付价格=0”的永久合同。
- 模型沿 Agent 现有真实、获授权连接调用。保持凭据安全和合法运行配置，但不新增“成本承担已确认/报价已确认/预算已批准”的接单或执行门禁。
- 复用既有 usage/effect/调用记录形成成本只读投影：`usage, usageStatus, costAmount, currency, costStatus, source, pricingBasisAsOf`。成本未知为null/UNKNOWN；估算与已获供应商金额明确区分，不能补造价格或把不同币种直接相加。
- 成本按实际调用唯一标识/effect关联去重；一个任务的多次真实调用均记录，传输重放不重复累计。议事调用和技能调用都纳入可得观察范围，不能只数最终一次图片动作。
- A可见本人任务的脱敏用量/成本摘要，B可见自己Agent接单的成本摘要；双方都不能读到他人的全局账单、密钥或私人会话。成本不可得/展示失败不阻断结果提交和验收，继续沿原用量记录与恢复机制，不在本轮新建计费引擎。已有展示直接复用，缺失数据可先UNKNOWN；补齐供应商计价/全量成本采集不是外单主链交付前置条件。
- 未来交付费用另按委派内容（需求、范围、成果要求、修订等）估算。设计只保留taskId/delegationId/requirementRevision的关联，不新增报价表/虚构收费公式，不能将costAmount直接当deliveryFee。

## 8. 前端详细落点

1. **先更新既有原型** `/home/isp/wsps/cyf/web/prototypes/juyiting/index.html` 及规格；离线原型已完成开关位置修正，产品实现未启动。
2. 每个本人Agent详情头像/名称下方直接有独立“接外单”开关行，不新增卡片或名册顶部管理区，说明“开启后同平台所有用户可委派”。不出现白名单、服务类型、价格/成本确认表单。
3. 新建任务后的“选择承办”统一展示“我的Agent＋开启外单的其他Agent”；默认ALL，可筛选我的/其他用户的。标明归属类别、推荐理由和运行状态，不暴露私有配置。
4. 能力不匹配或未知仍可选择，不以低分禁用按钮；忙碌/离线明确显示需等待实际调度。开关和身份在提交时复验。
5. 委托确认显示目标、任务需求/输入版本及资料处理说明；不要求用户选择IMAGE_EDIT/技能包、价格、预算或付款。本人选择沿原入口，外部选择写委派事实，界面不暴露两套底层权限细节。
6. 委托成功进入原任务办事页，显示已接单待指令/待运行而非假称开工；继续使用任务内议事、多步执行、补充资料与返工，普通密议权限不扩大。
7. 复用原文本/文件/结构化成果与正式验收；不是所有任务都有附件或图片。B的精简接单列表不获得客户正文/文件下载权。
8. 成本区域独立标“模型调用成本（非交付费用）”，未知/估算/实际分开；不显示“需支付模型成本后交付”等动作。本期不显示报价/应付/结算入口。
9. 身份/任务/目标切换隔离请求代次和SSE；保留未知结果的稳定幂等key恢复。PC/移动端统一候选选择与返工路径均验证。

## 9. 迁移、切换与恢复

- 新表默认无启用政策；不批量给历史用户开放服务，不修改线上 Agent Owner、不伪造委派/grant。
- 新 executor 字段只对新写入强制完整。历史终态仍按原数据 Owner 只读，不能用当前 binding 猜过去执行者；历史非终态逐项盘点，正常排空或取得明确取消/恢复授权后再切换。不得静默 backfill 已冻结快照/digest。
- 新生产者统一写新契约，不维护双版本执行兼容层。历史不可变记录可读不是保留旧执行通道。
- 迁移先固定候选/备份/校验；所有实际 DDL/生产切换另按授权实施。本轮不执行。
- API/Web 正式测试、构建、不可变制品与部署分别走 Flow5260799/4403172；develop 不自动部署。Runtime 按所属仓现行发布入口固定源码/制品/安装摘要，不假造 Flow run、不擅自新增流水线。
- 先部署就绪的新各端且外单政策默认关闭，验证身份/恢复合同，再由 B 开通试点。分步部署不意味着允许新旧协议同时接外单。
- 回退首选关闭新入单、保留数据和既有单恢复，不直接用旧二进制消费新委派记录。若必须回退代码，先处理活动外单并确认 schema/快照可读；不因回退把 B 改成 A。

## 10. 实施前需要复核但不应伪装已完成的事项

- 真实测试任务与相应已有能力/manifest/运行连接、测试 Agent 的真实 canonicalAgentId/binding（至少覆盖同一用户的两个不同 Agent）、A/B/C 的授权账号：上线前读取并固定，本文不填历史样例 ID。
- 本轮Runtime本地与查询时远端develop一致；实际开工仍从确认的干净基线重新核对，不把查询时点等同于永远最新。
- task-root、身份、policy、grant、conversation、effect 的实际锁偏序及 DB 约束，现有数据量/索引 EXPLAIN 和存量非终态：实施阶段提供证据。
- Task内工具隔离、入站typed report主体分离、文本/文件结果投影、多步/返工/换承办：必须真实测试，不以“目录支持跨Owner”替代。
- 同平台用户的认证tenant/client映射与统一候选API分页需由实施者核对；不把原同client假设冒充用户白名单。本文不新增跨租户授权。
- D2扩大了D1的成功路径覆盖：至少文本、非图片文件、图片和多动作任务；不承诺任意未知工具已经实现，也不能把测试例子固化为产品类型限制。


## 11. D2.1 代码与生产复核后的实施细化（2026-10-21）

依据与逐项源码定位见 [复核报告](design-recheck-20261021.md)。以下是目标合同，不代表现有生产能力。没有增加客户名单、任务类型或费用门禁。

### 11.1 完整双域与候选读模型

- 现有任务`tenant_id/client_id/owner_jiacn`始终为A的数据域；政策表的同名scope属于B。委派及PWE新增并冻结`executor_tenant_id/executor_client_id/executor_owner_jiacn/executor_binding_id`，不能用同一client同时代表A/B；TaskOwnerScope/AgentPrincipalScope分别传递全部字段。
- `platformScopeId`只由可信认证配置/注册表映射，委派持久化映射版本/依据摘要，body不接受它。映射尚未固定时不放行不确定的跨域操作，但必须将“全平台开放尚未实现”列为未完成，不能宣称同client实现已满足产品规则。绝不全局删除tenant/client条件。正式DDL冻结前核对真实多客户端映射与身份唯一性。
- 候选公开字段补`providerDisplayName:string|null`、`externalServiceState:ENABLED|DISABLED|null`；OWNED无需开关启用。公开昵称不是内部owner登录标识；未有可公开昵称显示“其他用户”，不拼接账号/手机号/主体ID。内部relation继续OWNED/EXTERNAL，UI显示“我的 / 其他用户的”。
- 统一候选仅用于**新指派**。既有任务必须返回受任务ACL约束的`assignedTarget`摘要（agentId/displayName/providerDisplayName/relation、持久委派关联、运行观察、actions）；政策关闭/不在当前候选页时仍能打开原任务。重绑后的展示可为历史目标/身份失效，不能以新Owner覆盖冻结事实。
- BountyPanel的assignedAgentForTask/matterCandidates，JuyiHall的discussTask/attachAdmittedPointAndStart、taskWorkspaceBinding等共同切换任务授权投影；私人密议的resolvePermittedConversationAgent、管理名册与profile-capabilities仍保持本人权限。授权目标摘要不伪装成canOperate=true。
- 分页游标绑定平台/认证代次、taskVersion/requirementRevision、筛选与固定排序依据；排序最终用稳定身份键。过期明确409后重读，用户选中目标按ID保留并重新验证，绝不静默选另一人。推荐不可用不遮蔽合法候选。

### 11.2 只接单不启动：明确拆开原bootstrap耦合

现有`assignForDeliberation → assignLocked → ensureBootstrapIntent → ChatBountyBootstrapAdmissionService`会自动提交首轮讨论，外单不得直接调用这条编排再伪称待指令。

1. 新外单服务提供独立编排方法，复用**底层**task-root、canonical target、assignment/grant writer；不复用会强制首轮bootstrap的公开assign-and-start方法。持久授权操作记录增加`initiationMode=AUTO_BOOTSTRAP|EXPLICIT_INSTRUCTION`；新本人点将保持AUTO_BOOTSTRAP业务行为，外单固定EXPLICIT_INSTRUCTION。这是两种明确业务意图，不是旧版兼容通道；后续执行都进入同一typed discussion/effect系统。
2. EXPLICIT_INSTRUCTION入单事务写assignment、delegation、grant及原outbox中的**会话准备意图**，没有CHAT dispatch、step或Provider调用。原grant读取器须按initiationMode校验对应意图，不再对所有grant强求旧“初次执行bootstrap”。不得用假的SENT、requestId、executionId满足旧验证。
3. 扩展现有bootstrap outbox/消费者的显式`intentKind=PREPARE_CONVERSATION`（现有首次动作意图固定`START_INITIAL_ACTION`）。准备消费者只调用`ChatBountyConversationService.ensure`的双主体授权版本，保存真实conversationId/generation准备回执，不调用typedDiscussion.admitPreparedBootstrap。原outbox租约、重投和持久回执机制复用；exact schema、数据库约束和reader同步更新。
4. 入单回执仍nextAction=SEND_TASK_INSTRUCTION，查询增加`conversationPreparation:PENDING|READY|FAILED`、`conversationId/generation`（未准备为null）。PENDING显示“准备议事中，未发送指令”；READY显示“已接单，待发送指令”。失败回读原准备意图，不再入单。准备会话不依赖B在线/技能就绪，不借机发模型请求。
5. A明确点击发送后使用现有task-bound typed discussion接口和稳定key，提交本轮request/turn/outbox。只要该指令已持久受理而执行Agent离线/忙碌，就显示“指令已受理，等待运行”；不得把“待指令”和“已发指令待运行”合成一个难以恢复的状态。
6. 任务继续入口不调用原`adoptBountyBootstrap`去伪造首轮；以任务assignedTarget、准备回执与现有interaction context绑定。首条/后续消息都按真实assignment/grant/conversation代次验证。
7. 本人路径也需允许合法离线/忙碌目标先指派，自动首轮沿原持久bootstrap/outbox等待；不能由Web canAssign(status=online)继续拒绝。执行所需真实安装、托管服务有效性与工具权限仍分层核验，不能把本期不收交付费用扩为免费的托管服务。

### 11.3 明确资料授权与宿主信任提示

- 外单`inputRefs`是本次完整初始文件授权集合；`[]`为无文件授权。即使任务已经有资料，也不得静默调用allTaskMaterials扩展授权；只有用户确认页列出的固定版本可进入grant。
- DTO明确`fileId/version/purpose`，字节hash/length由服务端按任务链接ACL解析，客户端不能提交或伪造hash作为授权。资料目录变更在提交时按明确版本复验；后来新增文件不自动授权旧动作。
- 后续在原任务添加并发送资料时，使用已有资料链接/授权修订服务更新grant，再冻结新的动作快照。文案区分“本单授权资料”与“本条消息引用资料”；未在本条重复引用不代表撤销已给出的本单授权。
- 委托确认必须写明：资料会由该Agent运行环境及其模型服务处理；拥有者可能从其管理的运行环境接触处理内容。应用页面不公开客户正文并不等于宿主管理员无法访问；不承诺供应商零留存。

### 11.4 撤回、取消、换承办的事务语义

- **A取消整个任务**：沿任务取消命令扩展委派协调，原锁下撤销活动委派/grant与未准入动作；在有执行事实时不能简单调用现有仅初始取消服务后吞掉409。
- **A撤销本次委派 / B撤回服务**：只终止该委派，不将A的任务直接设为CANCELLED。保留任务、需求、原成果和议事；projection给`attentionReason=DELEGATION_REVOKED`及安全可用actions。B无修改A需求、发起验收或替A挑选下一人的权限。
- 已准入的外部效果可能继续：禁止新start/新增输入权限，允许精确匹配既有start/fence的有限审计回执与隔离历史归档。复用execution abandonment/stop能力时保持其真实语义，不声称Provider已停止或退款。
- **换承办**是明确用户动作：先完成旧授权撤销，核实没有仍活动或RESULT_UNKNOWN副作用需要处置，然后以任务根锁创建新assignment/delegation/grant。旧事实不删除、不重放；不自动换人。切换事务失败不得留下半个新指派。
- 新assignment同步推进会话授权generation/target binding，阻止旧turn写新会话。A仍能查历史；新承办仅收到当前需求与本次明确授权资料，不默认继承前承办完整thread。generation、assignmentRevision、delegationRevision分别校验，不能互相替代。
- 状态写入复用原task/execution/turn writer和事件，不另建任务状态机；但新增委派协调、actions投影、取消后受限stage/commit路径是**必须实现的范围**，不是已存在能力。

### 11.5 ACK与撤回后的恢复矩阵

| 消息/调用 | 必须解析的scope | 撤回/旧代际后的允许范围 |
|---|---|---|
| chat.dispatch.ack / receipt | 认证B＋dispatchId/messageId→持久A关联 | 可确认原投递审计，不恢复委派 |
| typed delta/final / invalid outcome | B会话fence＋原turn/request/assignment/grant | 旧任务代际不能写新会话；既有副作用状态按旧执行归档 |
| request stop / stop ACK | A原请求授权→B目标通道→原A请求 | 停止回执不可伪装新任务完成 |
| lease / input / start | B→委派→A任务与明确grant | 活动有效委派才允许新工作 |
| result/effect recovery | 原执行者＋已持久准入效果 | 只限原效果的审计/历史归档，不再次调用或正式验收 |

`AgentWebSocketHandler`、`ChatDeliberationOutboxService`、Runtime chat-runtime的ACK持久箱/重放均在此覆盖；不能只改sendDirectMessage或只改final。

### 11.6 开关与前端异常的确定行为

- 默认关闭仅指权威查询确认无政策；加载失败显示“读取失败，重试”，不伪装关闭。开关提交pending禁用**当前Agent**的重复点击，别的Agent不被全局锁住。
- 新增仅Owner可读 `GET /agent/{agentId}/external-service-policy/request`，携原Idempotency-Key返回原变更回执；PUT超时先查原操作，不用GET最新state推定本次成功。404表示暂未发现该key，不能自动换key；用户明确重试仍用原key/原body。撤回亦需同理的原操作回执查询 `GET /agent/external-commissions/{delegationId}/revoke/request`，参与者ACL与POST一致。
- expectedRevision冲突后重新读当前政策并提示，不覆盖他人/另一标签页更新。切换Agent或账号丢弃迟到结果；恢复记录按身份+Agent/任务+操作类型分区，未知原操作未核清前不得换业务入口补发。
- 候选列表：加载中、读取失败可重试、没有开放Agent、只有本人Agent、无本人但有其他用户Agent、推荐不可用、翻页失败均有独立展示。网络错误不删除已选目标；提交时重新校验权威资格。
- 已接单后关闭开关，任务继续入口不消失；只影响新单候选。其他用户的只读摘要不调用Owner-only政策管理/完整技能目录接口。

### 11.7 本轮仍未冻结的技术输入

平台域映射的真实配置来源与A/B/C测试身份、双scope DDL与实际锁序、会话准备意图exact schema/存量非终态迁移需要EX-01/02固定。本文给出了设计方向与行为合同，但没有数据库并发/三端协议回归证明，不把这些标为“仅部署等待”。
