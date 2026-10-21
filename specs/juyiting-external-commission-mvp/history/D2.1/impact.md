# D2.1 影响范围与源码依据

核对日期：2026-10-21。原表为D2静态阅读；D2.1生产只读实操与新源码依据见文末§7。未执行外单业务测试。完整 commit/tree/远端查询见 `baseline.json`。以下“已发现”只适用于固定本地源码；“拟改”是设计，不是已完成。

## 1. 核心结论

这是 **API（agent + chat + mapper/security边界）/Web/Runtime 三端联合功能，包含新增持久授权关系与迁移**。UI范围包括统一候选、逐Agent开关和通用任务办理；后端和跨端权限影响较大。最大风险不是按钮状态，而是把 A 的业务数据与 B 的认证身份错误地合并，或只改成功路径遗漏恢复/取消路径。

### 已确认的断点

| 位置（仓库内相对路径） | 已发现 | D2 拟改 |
|---|---|---|
| `web/src/composables/juyiting/useHallData.js`，`canAssign` | `canOperate=false` 拒绝派单 | 保留管理语义；统一候选DTO分开推荐/派单/运行状态，不能用canOperate或能力分数拦外单 |
| `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java`，`to*DTO`、`recommendTaskAssignees`、`lockAssignedRuntime` | canOperate 基于 boundToMe；推荐 findCandidateRosterByOwner；锁目标按当前用户 Owner | 统一候选覆盖本人和已开放外部Agent，能力仅排序；本人/外部派单均移除能力匹配硬门槛。target authority保留真实身份与delegation |
| 同目录 `AgentLegacyTaskCompatibilityService.java`、`AgentTaskExecutionGrantServiceImpl.java` | assignAndGrant 先按任务 Owner resolve Agent；lockTargetAndPersistedInputs 按任务 Owner 锁身份 | assignment/target解析增加可信 AgentPrincipal，任务数据锁保留 A；grant 关联委派 |
| 同目录 `AgentTaskPointAndStartPolicyServiceImpl.java` | 点将开工能力按任务 Owner 查 canonical Agent | D2 外单入口不复用“一键开工”；防止该旧能力误放行或出现引导死路。已有本人行为回归 |
| 同目录 `TaskSkillPolicyServiceImpl.java` | 已从原生 proof 解析 runtimeScope，先验任务 grant | 复用现有分离，验证delegation及本单动作权限，不新增接单技能过滤或第二套registry |
| 同目录 `PersonalWorkspaceExecutionServiceImpl.java`，`create` | protocol4 创建仍 requireOwnedTarget；PWE 的 owner 是任务 Owner | 创建使用解析的双主体 context，executor 持久化，不变更数据 owner |
| 同文件 `runtimeConversationCommandViews` | 查询和候选过滤要求 row.owner=runtime.owner | executor 目标索引 + 委派授权复验 |
| 同文件 `withConversationRoot`、`skillOwner`、`inputContent/startEffect/recordEffect/resume/commitResult` | 多处用 Runtime Owner 查任务、文件和技能业务记录 | 按 execution 解析 TaskOwnerScope；保持 B 的 session fence；重用这一上下文贯穿所有路径 |
| `api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/PersonalWorkspaceExecutionMapper.java` | queued conversation SQL 使用 owner_jiacn 过滤 | 区分 taskOwner 与 executorOwner/binding；避免去掉 owner 后变全表跨租户读取 |
| `api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java` | sendDirectMessageToAgent 使用 row.ownerJiacn 路由 | 从已冻结委派解析 B 通道；row.owner 仍 A |
| `api/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java` | 现有若干回报/会话处理从 sessionJiacn 取得 Owner，注册 runtimeAuth 亦用此身份 | 区分认证 B 与可信关联的任务 A；只能在任务委派消息分支使用 A，注册/presence不变 |
| `api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatActionCapabilityService.java` | installed capability 已部分按 runtimeScope 查询 | 按本单权限解析真实可调用动作，允许多动作；未安装/未授权工具不能伪造可用，但不禁止接任务 |
| `api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatSelectedOutputFinalizationService.java` | 正式成果仍有 request/step/output/会话与版本链 | 延续原真实链路，验证跨Owner生成的结果也能投影；不能仅创建 PWE 后伪造聊天 step 来验收 |
| `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/funding/FundedBountyQuoteClaimServiceImpl.java` | funded 路径存在同 Owner 与预览模型约束 | 明确本轮不改、不调用该路径；不处理交付费用，不能伪造零元funded交易 |

以上文件的完整绝对路径可由 `/home/isp/wsps/cyf/` 加表中路径得到；基线文件保留已核对文件 SHA-256，避免把后续同路径内容误当本次结论。

## 2. 分组件影响

| 组件/层 | 必改或必验范围 | 风险 | 明确不改 |
|---|---|---|---|
| Agent core/api | 政策/委派实体与 DTO、TaskTargetAuthority/DelegatedExecutionContext、错误与回执 | 高：权限类型误用 | 身份注册本身、不改账号所有权 |
| Mapper/DDL | 2张新表；grant/PWE executor关联；队列索引、幂等/版本CAS、迁移 | 高：并发与数据正确性 | 不批量迁移资料、不重写旧 Owner |
| Agent service | 开关、统一候选/推荐、委派、assignment/grant、通用任务与PWE生命周期、继续办理/取消/恢复 | 高：副作用与越权 | 不新增技能专用执行器、不放宽私人资料服务 |
| Chat service | 任务会话准入、outbox去B、回包归A、能力/动作/成果投影、会话代际 | 高：跨用户消息泄漏 | 不开放普通密议、不扩大本人会话搜索 |
| Runtime | 委派上下文解析/原关联回报、thread隔离、受限议事、protocol4输入/输出/恢复回归 | 高：执行者身份与上下文污染 | 不重注册、不改HOME归属、不把密钥交给模型 |
| Web | 原型、独立开关、统一候选/选择承办、通用任务办理、精简接单列表、模型成本展示与账号切换 | 中：错误按钮与迟到响应 | 不重做地图、不修改全局视觉系统、不做通用市场 |
| 发布运维 | 迁移、三端固定版本、默认关闭、试点开通、精确成果与恢复证据 | 高：新旧端不一致 | 本轮无云配置修改/无部署/无服务重启 |

### Web 定向位置

- `/home/isp/wsps/cyf/web/prototypes/juyiting/index.html` 与既有 prototype spec：先原型。
- `/home/isp/wsps/cyf/web/src/components/juyiting/AgentPanel.vue`、`SelectedAgentCard.vue`、`BountyPanel.vue`：新增外单服务/委托入口。
- `/home/isp/wsps/cyf/web/src/composables/juyiting/useHallData.js`、`useHallTaskActions.js`：本人操作与外单委托分离。
- `/home/isp/wsps/cyf/web/src/composables/juyiting/useHallPointAndStart.js`：本人开工不变；外单不误入旧点将自动开工流程。
- `/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue`：任务内选 Agent/会话关联、返回导航、身份代次；避免只改卡片不改父级守卫。
- `/home/isp/wsps/cyf/web/src/composables/juyiting/useHallConversation.js`：如读取 owned 名册来确认目标，须改为任务授权投影；此处是实施前定向审查项，不宣称所有分支已审计。
- 拟新增小型 `useExternalCommission` composable 和服务设置表单，复用统一 HTTP 层、幂等与身份代次，不新增通用框架。

### Runtime 定向位置

源码仓库 `/home/isp/wsps/chcbz/isp-install`；本地 HEAD 不等于本次查询的远端 develop，以下只为本地基线事实。

- `conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs`：`skillSessionBinding` 根据已认证 ACK 构造 B 的 scope，这一安全边界保留。
- `conf/codex-ws-agent/agent-client.mjs`：typed task消息/回报、会话 key、任务隔离策略。现有 `_chatTurnKey` 已含 owner/conversationGeneration；`buildThreadKey` 还有模型/策略/HOME相关维度，不能简化掉原隔离字段。
- `conf/codex-ws-agent/agent-message-wire.mjs`：新 taskAuthorization 的保真/类型校验，不能把任务 Owner 反写 runtimeAuth。
- `conf/codex-ws-agent/skill-executor.mjs`：protocol4 command exact-key parser；默认不加新字段，若实现修改 wire 必须同步。
- `conf/codex-ws-agent/skill-conversation.mjs`：使用原 HTTP queue/lease/effect/result；失败分类、恢复和取消后有限回执必须验证。
- `conf/codex-ws-agent/skill-execution-store.mjs`：已按 Runtime scope digest/executionId 隔离，且验证 immutable command。复用而非复制存储系统。
- `conf/codex-ws-agent/skill-runners/image-provider.mjs`：原 broker 按真实 scope 解析 Provider binding，保持这一行为；一张输入/PNG的技能合同从真实 manifest 固定。

D2 不要求修改每一个列出的文件；这些是必须完成行为检查的最小调用边界。最终改动清单以实现 diff 为准，不能仅靠静态搜索估报文件数或工时。

## 3. 关键风险及控制

1. **只修 assignment、没修取件**：队列按 B 查 A 的 row 导致永远没有命令。用真实双账号创建后从 B native session 领取验证。
2. **只修执行、没修议事**：Chat 向 A 的通道找吴用导致不投递；或者回包写 B 会话。必须验完整 WS→SSE，而非模拟技能 create。
3. **全局取消 owner 检查**：会暴露普通资料、安装、其它租户。采用受委派 TaskTargetAuthority，不改注册/管理认证。
4. **重复动作产生多次付费**：仅 Idempotency-Key 不能挡不同 key/不同 action。同逻辑意图沿既有action/execution/effect链去重；一个委派允许多次合法动作，不能靠整单一次限制代替effect CAS。
5. **关闭政策造成恢复失效**：存量委派读冻结政策；关闭只禁新单。显式逐单撤回另走撤销语义。
6. **取消时外部调用已发生**：先后由同一持久准入决定；不谎称能回收调用，保留结果未知/审计恢复。
7. **A 的结果落 B 空间**：全链路 business owner=A，最后验证下载字节hash和A验收权限，并验证B/C下载拒绝。
8. **B 的私人上下文泄漏**：task thread隔离和工具能力约束，不能只加一行 system prompt；主机管理员边界向A说明。
9. **历史快照/升级破坏恢复**：不回写 frozen digest、不靠当前身份猜旧执行者；切换前盘点非终态并按授权处理。
10. **错误复用历史成功**：旧图片闭环、单账号测试、API health都不是本次外单验收；固定候选和实际授权账号证据。

## 4. 未覆盖/未知项

- 未读取生产数据库、未取凭据、未核对线上吴用实际安装与成本连接，也未发送任务。
- 当前本地 Runtime 与远端 develop 不同；未抓取远端内容或判断差异可直接合入。
- 未扫描全部数据库/WS分支、执行实际锁竞争或所有 UI 守卫；实施清单必须补这些验证。
- “同 tenant/client 的跨用户”不能外推为跨租户SaaS隔离支持。
- 本轮未运行 Gradle/Node应用回归，未证明任何新增接口已经存在。

## 5. D2 独立开关补充（用户明确要求）

“吴用/林冲/chcbz”仅测试展示名。政策原本以agent/binding为键，本次明确多Agent同时开放及逐Agent启停，不新增账号级或Runtime级总开关。前端管理组件必须传当前选中的canonicalAgentId并隔离请求代次；后端每次复核本人绑定和该Agent政策revision。开关无需客户/技能/费用配置；入单只按身份、任务、开关资格判断，能力仅推荐，Runtime状态另作等待/运行投影。AC33–AC38继续验证独立开关，不借此宣布所有Agent都具备任意能力。

## 6. D2 相对旧提案的影响变化

- **删除复杂度**：政策表仅开关与修订，不再保存受众白名单、任务类型、固定技能、成本资格；取消相关UI和错误门禁。不新增报价/结算模块。
- **新增必要覆盖**：统一候选跨本人/外部范围，修改原推荐eligible/validateAbility等造成硬拒单的位置；推荐失败不阻断列表。能力、在线状态、费用不得混为派单权限。
- **通用任务链**：不再只验证图片protocol4。文本/文件/结构化成果、多个动作、返工与新旧授权修订必须贯通；原记录中Owner假设按实际参与路径定向核查，不宣称所有runner已完成审计。
- **排队与运行**：离线/忙碌可先接受委派，沿原durable assignment/outbox/队列等待；检查同Agent多任务、唤醒/恢复和当前任务投影，不新增资源/时间硬门禁或第二套调度器。
- **成本只读**：复用用量/effect记录的成本投影；未知保持UNKNOWN，无法读取不阻断交付。未来基于委派内容估费另作设计，不能将成本直接映射交付金额。
- **真实平台范围**：同平台所有用户均可见开放Agent，但C仍不可读A任务；C可以创建自己的任务使用同一Agent。需核对认证client/tenant是否真正隔离域，不能用技术默认隐藏同平台客户。

D2的业务选择已明确，但这些技术接线和真实数据库/线程/权限测试仍由实施Owner落实；本文不是代码完成证明。


## 7. D2.1 复核新增的必须改/验边界

逐项证据：[design-recheck-20261021.md](design-recheck-20261021.md)，最新文件摘要：`evidence/design-recheck/source-readback.json`。

| 位置 | 新增明确影响 |
|---|---|
| `web/src/components/juyiting/BountyPanel.vue` | assignedAgentForTask、matterCandidates不能再从operableAgents恢复外单目标；新候选/任务target/管理名册分离 |
| `web/src/components/world/JuyiHall.vue` | discussTask、attachAdmittedPointAndStart、taskWorkspaceBinding及恢复守卫；私人密议守卫保持原权限 |
| `web/src/composables/juyiting/useHallAgentProfileCapabilities.js` | Owner-only目录不能给其他用户详情复用；展示公开摘要，不绕过boundToMe |
| `api/agent/.../AgentTaskExecutionGrantServiceImpl.java` | assignForDeliberation/assignLocked强制bootstrap与allTaskMaterials；需底层writer复用、EXPLICIT_INSTRUCTION编排、显式输入集合 |
| `api/chat/.../ChatBountyBootstrapAdmissionService.java`、`ChatBountyConversationService.java` | 准备会话与自动首轮分开；新prepare意图schema/回执、双主体grant验证、换承办generation |
| `api/chat/.../ChatDeliberationOutboxService.java`、`AgentWebSocketHandler.java` | dispatch ACK/receipt/invalid outcome/stop都要B认证→A持久关联；不是只改出站/final |
| `api/agent/.../AgentTaskCancellationServiceImpl.java`、`api/chat/.../ChatBountyExecutionTerminationService.java` | 现有初步取消/单执行放弃非完整撤回；新增委派协调、有限恢复与安全重指派 |
| 政策/委派/PWE/操作回执DDL与DTO | 完整executor tenant/client、平台映射依据、initiationMode/准备意图、原开关/撤回回执查询、公开归属字段 |
| Runtime `chat-runtime.mjs`、`agent-client.mjs` | 新授权上下文不可变摘要、ACK重放、thread/generation与任务隔离；不能删旧fence检查 |

文中`...`为分层定位简称，完整路径由新复核报告及source-readback定位，不用简称作为可执行文件路径。

本轮代码无新外单接口命中；生产仅同账号现有流程，真实跨用户仍未测。Runtime当前查询已与远端develop一致，不沿用原§4的旧分歧结论。其他历史未覆盖项仍保留其原核验边界。
