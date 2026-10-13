# 聚义厅统一技能执行详设（SE-1）

**核对：2026-10-13；状态：实现合同，不是已上线说明。**

本文固定代码职责、协议、数据增量、事务、恢复和切换方式。后续直接实现与验证，不再安排“制定方案”任务。生产迁移时读回实际 schema/源码是安全核验，不是重新设计。

## 0. 固定源码与已查明事实

精确 HEAD/tree 与已读文件摘要见 `baseline.json`。API/Web 本地受跟踪工作区干净；根仓库已有大量他人修改，只新增本特性目录。未查询远端 develop，也未核验当前线上 API/Web 制品，不把本地 HEAD 称作最新线上版本。

Runtime 源仓库：`/home/isp/wsps/chcbz/isp-install`，模块在 `conf/codex-ws-agent/`；实际安装位于 `/home/isp/apps/cyf-agent-runtime-v1/unified/codex-ws-agent`。已比较六个关键模块，其中 installed `agent-client.mjs` 与源 HEAD 不同：线上文件没有源中的 text-file 接线。其余五个抽查模块字节相同。实施必须保留源 HEAD 的已有 text-file 增量，不能拿 installed 整文件覆盖源码；这不是全 Runtime 同源证明。

已确认耦合点：

- Web `hallPointAndStartIntent.js` 同时硬编码媒体操作白名单和普通议事操作集合。
- `ChatActionCapabilityService.available/appendImageAdapter` 硬编码图片 Provider lane 与文本零资料条件。
- `ChatActionExecutionService.admit` 在图片和文本执行器之间分支。
- `ChatActionFinalService.actionProgress` 按文本/图片重新推导 childRequestId。
- `ChatActionOutcomeContract`、Runtime `juyiting-action-outcome.mjs` 均严格校验旧动作结构，必须同批更新。
- `ChatTypedDiscussionAdmissionService.admit`/`ChatTypedDeliberationContextService.resolve` 只处理本条 selectors；普通后续消息不会自动带入任务资料。
- `ChatConversationAssetSourceResolver.resolveAction` 已有真实来源校验，但受图片 operation 限制。
- `PersonalWorkspaceExecutionServiceImpl` 混合了通用文件、图片 consent、Provider 和固定 MIME。
- `ChatBountyAssetProjector` 才是执行输出→会话资产/消息的关键路径；`AgentTaskArtifactOutcomeServiceImpl` 是成果验收，**不改它的验收状态机**。
- 当前吴用 profile 含 typedInspection 与 controlledImageHttp；林冲、卢俊义没有相应键。装技能本身不会使识图就绪。

## 1. 决策与轻量边界

1. 沿用现有 `CHAT → ACTION_REQUEST → outbox → INSPECT/EXECUTE → output → asset` 链路，不增加第二个调度器。
2. 读取资料保持公共 `INSPECT_INPUTS` 能力；有产物的技能统一 `EXECUTE_SKILL`。PDF、Excel、图片不是平台操作枚举。
3. 沿用现有 `skillKey`/`skillVersion` 命名，不额外引入与安装不一致的 skillId。
4. SKILL.md 说明如何使用，manifest 声明如何执行；二者都不是权限来源。
5. 一个新附属表保存技能执行快照和效果记录；主执行表、输出表、chat outbox/step/link/asset 继续复用。
6. 不引入新守护进程、消息队列、DAG 引擎、插件热部署平台。复用当前轮询/outbox、Runtime 租约与锁。
7. 费用仅 `costInfo` 展示/登记。核心执行路径不能读取费用字段作判定，也不能创建 consent/冻结/预扣记录。
8. 原包购买和悬赏经济业务不变。Provider 帐号余额不足是外部工具真实错误，不转换为平台费用审批。
9. 新技能若采用现有 runner，只新增技能包与安装记录；新 Provider 协议可新增 runner 适配器；新安全边界/预览方式可能需要核心扩展，不承诺永远零代码改动。
10. 已有包大小、消息资料数量、租约等协议边界本次不随意扩大或新设。等待没有性能强制 deadline；保留真实传输超时和身份/用户取消。

## 2. 模块与改动清单

下文目录缩写：

- AS=`api/agent/jia-agent-service/src/main/java/cn/jia/agent`
- AI=`api/agent/jia-agent-api/src/main/java/cn/jia/agent`
- AC=`api/agent/jia-agent-core/src/main/java/cn/jia/agent`
- AM=`api/agent/jia-agent-mapper/src/main/java/cn/jia/agent`
- CS=`api/chat/jia-chat-service/src/main/java/cn/jia/chat`
- RT=`/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent`
- WEB=`web/src/composables/juyiting`

### 2.1 后端

| 文件/类型 | 固定修改 |
|---|---|
| AS/skill/SkillPackages.java | 读取不可变包 manifest，校验声明；缓存按包摘要，不按角色复制 |
| economy/.../skillseed/PlatformSkillPackageCatalog.java | PRODUCTS 硬编码改成 classpath `skill-packages/catalog.json` 加包摘要验证；包加入不修改 Java 分支；首期随应用制品发布，不新增动态仓库 |
| AS/skill/SkillInstallResultService.java | 安装就绪须匹配包/manifest 摘要；Runtime 工具就绪不冒充安装授权 |
| AS/skill/SkillInstallDispatchService.java | 保留安装身份/事务/outbox，不承载执行策略 |
| AS/skill/SkillManifestCodec.java（新增） | 纯函数解析/校验 manifest 与参数子集；无网络、无外部 `$ref` |
| AI/service/SkillCapabilityLookup.java（新增） | agent 模块定义能力查询接口，chat 实现实时 session 适配，避免 agent 反向依赖 chat |
| CS/handler/SkillExecutionSessionRegistry.java（新增） | 注册可信 Runtime 的当前技能目录；断线/代际变化失效 |
| CS/service/ChatActionCapabilityService.java | 合并现有 inspector 和通用技能目录；移除 appendImageAdapter 与 catalog.isEmpty() 文本分支 |
| CS/service/ChatActionOutcomeContract.java、ChatActionFinalValidator.java | action-v4 描述/参数/摘要验证，与 JS 共用正反 fixture |
| CS/service/ChatTypedDiscussionAdmissionService.java、ChatTypedDeliberationContextService.java | 确定本次有效资料上下文、冻结目录与能力快照 |
| CS/service/ChatConversationAssetSourceResolver.java | 提取 resolveAuthorizedSources，按来源类型校验 ACL/lineage，不按 GENERATE/EDIT 分支 |
| CS/service/ChatActionExecutionService.java | 唯一 EXECUTE adapter；按 descriptor 调用通用 createSkillConversation，不再分图片/文本 |
| CS/service/ChatActionDispatchService.java | 保留 outbox claim 和锁序；INSPECT / EXECUTE 两条平台路由不增加 |
| CS/service/ChatBountyExecutionTerminationService.java | 接入protocol4撤销/取消，UNKNOWN不假装安全取消，保持Owner和在途副作用事实 |
| CS/service/ChatActionFinalService.java | 从已持久化 admission/step/link 读 childId，不按技能重新计算；投影执行与归档状态 |
| AS/service/impl/AgentTaskExecutionGrantServiceImpl.java、AgentTaskDeliberationOperationReadServiceImpl.java | 新议事 baseline 为 DELIBERATE/INSPECT_INPUTS/EXECUTE_SKILL；具体技能权限在已安装 entitlement+任务 scope 决定 |
| AI/service/PersonalWorkspaceExecutionService.java、AS/.../PersonalWorkspaceExecutionServiceImpl.java | 增加 createSkillConversation/skillCommand/skillInput 路径，复用 lease/stage/commit/recovery 原语；不访问图片 consent |
| AC/entity/SkillExecutionEntity.java、AM/{dao,mapper}/...（新增） | §7 的附属快照与 CAS 数据访问 |
| AS/api/PersonalWorkspaceConversationRuntimeController.java | 保留既有 conversation endpoints；增加 effect/resume 的通用端点；无图片端点新增 |
| AS/skill/SkillExecutionService.java（新增） | 快照、lease/effect 状态、复验与恢复；不另起调度器 |
| CS/service/ChatBountyAssetProjector.java | 增加 executionId 定向投影入口，复用原事务；定时 pending 扫描只作补偿 |
| CS/archive/conversation/ChatConversationArchiveService.java | 复用素材索引/读权限，只读目录不触发全内容读取/生成 |
| AS/service/impl/PersonalWorkspaceOutputFormatValidator.java | 结构校验器按 MIME 注册；未知安全文件走 opaque 下载，禁止自动 inline/执行 |

不改 `AgentTaskArtifactOutcomeServiceImpl` 的接受/替换/验收语义，不把生成完毕当作正式交付被接受。

### 2.2 Runtime

新增 RT `skill-manifest.mjs`、`skill-registry.mjs`、`skill-executor.mjs`；Provider adapter 从既有图片模块提取，不重写传输实现。

- `skill-install-manager.mjs`：执行 manifest 校验、安装标记绑定摘要；保留 zip 防穿越/包摘要/Owner 锁。
- `agent-client.mjs`：注册 `skillExecution` 声明；接收统一 executionProtocolVersion=4；同一 poll 循环按 descriptor.runner 调用，不为每技能起 lane。
- `chat-runtime.mjs`、`juyiting-action-outcome.mjs`：action-v4 输出与验证；规划回合仍不允许直接运行生成脚本。
- `workspace-file-bridge.mjs`：复用受权输入下载、staged upload/commit，输出不直接写进业务文件表。
- `typed-inspection-runtime.mjs`：保持真实内容载体/证据，不因装图片技能伪报 inspected。
- `controlled-image-http-executor-v3.mjs`：提取 HTTP 编解码/格式校验到 `skill-runners/image-provider.mjs`，去掉 consent/图片专用上层 command；留 Provider 特有限制在适配器。
- `conversation-text-file.mjs`：其已有实现迁为 `skill-runners/native-text-file.mjs`；不覆盖源 HEAD 增量。
- `report-outbox.mjs`、既有恢复留存：记录 manifest/结果回执，服务端确认后才清理本执行临时目录。
- `conf/cyf-agent-runtime-v1/lib/runtime-client.mjs`对应 exact-route 白名单同步新 effect/resume 路由；不得开放 `/internal/**` 全通。

### 2.3 Web

- `hallPointAndStartIntent.js`：投影 schemaVersion=2；校验平台权限结构/基本操作和任务/主体/版本，不要求精确等于两项；不枚举技能名称。未知平台操作仍协议报错，已知 EXECUTE_SKILL 下新 skillKey 可扩展。
- `hallTypedDeliberation.js`、`useHallTypedDeliberation.js`：discussion schemaVersion=2、action-v4、执行状态和技能参数消费。
- `useTaskWorkspaceBinding.js`：TASK_DEFAULT/EXPLICIT/NONE 选择；UI 显示“本任务资料”和“仅本条消息”。
- `bountyOutputCatalog.js`、`bountyOutputRecovery.js`、`useHallBountyRequestCatalog.js`：优先按执行 ID 读取结果，保留成果关联语义，不等全历史页面才能展示新成果。
- `useHallArtifactTransfer.js`：通用下载；`useHallArtifactOutcomes.js` 验收操作不改，只对新数据作回归。
- 删除新流量对 `hallPointAndStartProviderConsent.js`、`useHallPointAndStartCostConsent.js`、`hallControlledImagePointAndStartBridge.js`、`useHallPointAndStartControlledBridge.js` 的依赖；迁完其身份/幂等检查后才删死代码。
- `web/src/components/economy/SkillProductCard.vue`：显示运行费用说明，独立于包购买价；未知费用不显示为 0。

## 3. 技能包声明与参数算法

包：`SKILL.md + manifest.json + 可选 scripts/references`。例见 `examples/image-edit.manifest.json`。

manifest 必需字段：`schemaVersion=1, skillKey, skillVersion, title, description, runner, entrypoint, parametersSchema, inputs, outputs, requirements`；`costInfo` 可省略，读取时规范为 UNKNOWN。

- runner 仅为已登记执行类型：首期 `provider-operation`、`local-script`、`native-file`。每种 runner 内按 adapter 注册表查找，不将脚本、URL、CLI argv 放入模型输出。
- entrypoint 是包内相对路径或维护方登记的 adapter 名；禁止绝对路径、`..`、符号链接逃逸。
- inputs 声明 `minItems/maxItems/acceptedMimeTypes`；min/max 有真实工具依据，平台沿用当前请求最多32来源边界，不凭未来视频推测新限额。
- outputs 声明允许 MIME、是否多文件。只声明格式不是文件真实有效的证明。
- requirements 为工具/Provider alias，凭据不入包。
- costInfo 不参与执行结构校验失败：缺失或费用说明格式错误只显示 UNKNOWN 并记录元数据警告，不让费用数据阻塞合法技能。其可用格式为 `mode=FREE|FIXED|METERED|UNKNOWN`、可空十进制字符串 amount、currency/unit/description/source/updatedAt。未知不等于免费；更新价格不改变已有执行快照。若随包变更需新包版本，不篡改旧摘要。

`parametersSchema` 是明确的 `cyf-params-v1` 子集，不冒称完整 JSON Schema：type(object/array/string/boolean/integer/number，或这些类型的非空无重复数组表示联合类型)、properties、required、additionalProperties=false、items、enum、minimum/maximum、minLength/maxLength。拒绝其他关键字、远程引用、正则执行、默认注入。递归纯数据；重用当前消息/包解析保护，不另设无依据限额。integer 必须 JS safe integer；超大 ID/金额采用字符串。各工具精度规则留参数声明。服务端和 Runtime 两次校验相同 fixtures，Web 不成为权威校验器。

`validateParameters(schema, value)`：先类型→对象必需/未知字段→递归→枚举/数值/长度；不做字符串转数值、去除未知键或 URL 获取；失败返回明确参数路径，无脚本执行。

元数据与 SKILL.md 是受安装完整性保护的能力描述；资料、图片中的文字、历史聊天仍是不可信内容，不得改变工具权限、runner、凭据或文件范围。

## 4. 能力发现、版本和费用

复用 Runtime 注册消息增加：

```json
{"skillExecution":{"schemaVersion":1,"catalogRevision":"7","skills":[
  {"skillKey":"image-edit","skillVersion":"1.0.0","packageSha256":"<64hex>",
   "manifestSha256":"<64hex>","runner":"provider-operation","readiness":"READY",
   "reasonCode":null,"toolchainDigest":"<64hex>","bindingRevision":"4"}
]}}
```

Runtime 报告只能提供运行事实，不能授予安装 entitlement。服务端对照真实安装结果、包摘要、身份 proof、当前 session generation；同一 scope 存在多个不唯一就绪主体则明确不可用，不能任挑一个。

```text
installedDescriptor = package verified by installation receipt
runtimeReady = current session report matches descriptor and available runner/dependency
taskAllowed = actor/task/assignment + installation entitlement + data/network policy
callable = installedDescriptor && runtimeReady && taskAllowed
# 这里没有 costInfo、balance、consent，也不调用计价服务
```

连接建立/包安装/配置重新加载时重新检查，heartbeat 使用缓存；断线、安装变更或 session generation 变化立即失效。调用时重新验证同一绑定。缓存键含完整主体、安装摘要、toolchainDigest、bindingRevision；不永久按“吴用/林冲”缓存。

只向模型提供当前任务可用技能摘要与参数 schema，选中后 Runtime 才加载完整 SKILL.md/资源；不把所有包、全部历史文件塞入上下文。暂不可用技能给 UI 原因，不谎报 READY。

为 UI 增加只读 `GET /agent/tasks/{taskId}/skill-capabilities?targetAgentId=...`，复用 Owner/task ACL，返回 `catalogRevision, items[{skillKey,skillVersion,title,state,reasonCode,costInfo}]`。无任务访问权404，真实目录依赖故障503。价格缺失永远不是503/403原因。API 响应 no-store，不包含 Provider 地址、凭据或内部路径。

## 5. action-v4 与任务资料

### 5.1 动作快照

在 facts.availableActions 中将旧 operation 特例改为：

```json
{"actionId":"act_<digest>","kind":"EXECUTE","operation":"EXECUTE_SKILL",
 "skill":{"skillKey":"image-edit","skillVersion":"1.0.0","packageSha256":"<64hex>","manifestSha256":"<64hex>"},
 "parametersSchema":{"dialect":"cyf-params-v1","type":"object","properties":{},"required":[],"additionalProperties":false},
 "inputMimeTypes":["image/png","image/jpeg"],"minSources":1,"maxSources":1,
 "outputMimeTypes":["image/png"]}
```

发现/结果中的粗粒度 mediaType 继续使用现有 text/image/audio/file；video 等新媒体在没有专用展示时归 file，保留真实 MIME，不为新增格式扩核心枚举。

`INSPECT_INPUTS` 项保持平台 inspect route，skill=null、参数为空对象，附 supported MIME；它不是图片生成能力。

模型只返回 `action:{actionId,instruction,sourceRefIds,parameters}`。skill/version/binding 由服务端从已冻结 facts 解析，不从模型或浏览器接受。请求非法参数直接校验失败；缺必要资料则 CLARIFY；资料存在而未识别应请求 INSPECT，不让模型臆测图片内容。

actionId 取安装描述的稳定摘要；在请求 facts 内唯一。重试读取原 facts，不重新跑当前目录来重建旧 action。packageSha256 是归档包原始字节摘要，manifestSha256 是包内 manifest 原始字节摘要；缺省费用的展示规范化不改变这些摘要。使用现有 canonical JSON 编码与 sha256，数字/字符串规格在 Java/JS fixtures 中固定。

chat action facts/final schemaVersion=4；Runtime 执行协议 executionProtocolVersion=4；manifest 自己的版本=1，三个版本不混用。升级不保留两种新执行生产入口，历史原始回执仍可审计读取。

### 5.2 资料上下文

`POST /chat/conversations/{id}/interactions/discussion` 沿原认证与 Idempotency-Key，body 升级 schemaVersion=2，增加 `materialScope=TASK_DEFAULT|EXPLICIT|NONE`，保留 sourceSelectors。

- TASK_DEFAULT（UI 默认）：当前任务有效资料版本 + 本消息显式选中资料。只自动纳入 TASK 可见且对当前 Agent 合法的 link，不扩展整个个人 workspace。
- EXPLICIT：仅本消息所选，适合“仅本条消息”。
- NONE：不带资料；sourceSelectors 必须空。
- CLARIFICATION_REPLY：父问题资料在其原 MESSAGE/TASK scope 内继续有效，除非用户显式替换/排除。普通下一条消息不继承无关 MESSAGE 临时资料。
- 自动来源上限沿现行32；超出不静默截断、不读取全部正文，保持普通对话可用，返回资料选择提示与分页选择入口。本次执行等待用户缩小范围。

服务端在原 task-root/binding/conversation 锁序内：

```text
先按完整 scope + key 查旧 admission；同 bodyDigest 直接回放
  → 校验当前 task/assignment
  → resolveEffectiveSelectors(command, currentTaskLinks, clarificationParent)
  → 去重：sourceKind + 精确版本身份；保持 deterministic 顺序
  → 逐项查 Owner/ACL/版本/来源关系
  → 冻结 catalog 的 MIME/大小/hash/来源（不信任客户端提供）
  → 生成事实和技能目录快照
  → 请求、快照、admission、outbox 同事务提交
```

明确：bodyDigest 绑定原始用户命令（含 materialScope），requestDigest 绑定解析后的有效资料快照；相同 key 重放不因任务后来添加资料而改变请求。源已撤销不允许新读取，但已持久结果可按当前读权限回放。

`resolveAuthorizedSources` 对 TASK_LINKED_WORKSPACE_VERSION 校验任务 link/版本/当前成员权限，对 CURRENT_CONVERSATION_ASSET 校验 scope/generation/producer step/output 已提交与保留状态。之后才按 skill.inputs 做 MIME/数量校验。

**图片编辑可接受任务上传图或当前会话成果；前者没有虚构 producer。** 只有显式编辑已有成果，才建立 replaces 精确引用；普通上传图编辑产生新成果，不伪造“替换某个已交付成果”。

## 6. 执行接纳：唯一事务入口

`ChatActionExecutionService.admit(BoundAction)` 的具体逻辑：

```java
// 调用方仍为 ChatActionDispatchService.consume 的 MANDATORY 事务
var action = requireActionFromFrozenFacts(bound);
require(action.kind == EXECUTE && action.operation == EXECUTE_SKILL);
var prior = typed.findAdmissionByKey(scope, actionEventId, true);
if (prior != null) return verifyReplayAndReadChild(prior, bound); // 不调用 live runtime/provider
var grant = grants.resolveAndAdmit(scope, task, assignment, agent, "EXECUTE_SKILL", false);
var descriptor = installedSkills.requireExact(action.skill);
var sources = sourceResolver.resolveAuthorizedSources(...);
validateParameters(descriptor.parametersSchema, action.parameters);
validateInputs(descriptor.inputs, sources);
var ready = capabilities.requireExactCurrent(scope, agent, descriptor);
// 不调用费用/consent，不在事务中访问 Provider/存储/启动进程
var snapshot = freeze(descriptor, params, sources, grant, ready.bindingRevision);
var execution = executions.createSkillConversation(scope, stableIds(actionEventId), snapshot);
insertChildRequestAndStepAndLinkAndAdmission(execution, bound);
persistActionStarted(bound, execution.requestId, "EXECUTE");
return execution.requestId;
```

snapshot_json 必含：`schemaVersion=1,skill{key,version,packageSha256,manifestSha256,runner,entrypoint},taskId,conversationId,conversationGeneration,targetAgentId,originalUserMessageId,originalUserContentSha256,parentOutcomeId,parentFinalDigest,actionEventId,instruction,parameters,taskGrant{id,version,assignmentRevision},providerBinding{alias,revision},inputs[],sourceSnapshotDigest,outputs,deliveryRelation,costInfo`。本地技能 providerBinding=null；costInfo 是不影响权限的登记快照。inputs 各项为 `inputRef,sourceKind,sourceIdentity,contentMimeType,byteLength,sha256`；sourceIdentity 保留工作区 file/version/purpose 或会话 generation/asset revision/producer output lineage；不要保存可由其他租户访问的裸URL。初始Runtime session放在lease/效果记录中，不把旧session永久锁死在不可变业务快照以致合法恢复不了。

新 ID 一律按 `sha256(canonical(scope,actionEventId,label))` 派生；request/step 用现有字段可容纳格式，executionId=`pwe_`+前60 hex（64字符，符合既有 chat link），runId=`pwe_run_`+完整64 hex。同 key 不同语义 digest 返回409，不追加任务。

锁序：接纳保持原 task root→binding→conversation→outbox→执行/附属行。注册/目录读取不在此获取反向 Runtime 安装锁；Runtime proof 验证复用既有 fencing API。实际 start/effect/commit 路径沿已有 runtime installation/session→task root→execution 的锁序；跨两域协调采用现有准备/短事务复验，不新增倒序持锁调用。

所有网络/Provider/文件大块读取在短事务外。准备后的 opaque 文件描述只能由服务端产生，提交事务重新检验身份、lease、输入版本及摘要，不从客户端 metadata 推断成功。

## 7. 数据库增量（明确选择：一个附属表）

**不创建第二张任务表或费用表。** 新增 `agent_skill_execution`，与现有 `agent_personal_workspace_execution` 一对一，承载旧通用执行表缺失的技能语义。

| 字段 | 类型/约束 | 用途 |
|---|---|---|
| id | BIGINT AUTO_INCREMENT PK | 延续现有主键风格 |
| tenant_id/client_id/owner_jiacn | VARCHAR(50)，现有 binary scope 语义 | 隔离 |
| execution_id | VARCHAR(100) | 唯一关联 PWE |
| skill_key/skill_version | VARCHAR(64) | 与现有安装标识长度一致 |
| package_sha256/manifest_sha256 | CHAR(64) ascii_bin | 不可变包身份 |
| snapshot_json | JSON NOT NULL | 参数、源描述、来源 lineage、grant/binding/输出要求、skill描述/费用快照；无凭据和绝对存储路径 |
| snapshot_sha256 | CHAR(64) ascii_bin | canonical snapshot 完整性 |
| phase | VARCHAR(24) | READY、RUNNING、WAITING_PROVIDER、RESULT_UNKNOWN、RESULT_READY、ARCHIVING、COMPLETE、FAILED、CANCELLED |
| effects_json | JSON NOT NULL，初值 `{}` | 每个逻辑副作用的持久记录，见§9 |
| result_manifest_json | JSON NULL | 结果摘要，不存字节/临时下载密钥 |
| last_error_code | VARCHAR(64) NULL | 非成功原因；不复用价格不足概念 |
| version | BIGINT NOT NULL DEFAULT 0 | CAS 状态版本 |
| created_at/updated_at | BIGINT NOT NULL | 与项目时间约定一致 |

唯一键 `(tenant_id,client_id,owner_jiacn,execution_id)`；不再创建 idempotency unique，沿 PWE 既有 `uk_pwex_idempotency_scope`。事务同时插入主行/附属行，不留下半条接纳。

DDL 资源新增 `agent-skill-execution-v1.sql`；mapper/DAO 必须保持 exact binary scope 检查。新增 `SkillExecutionSchemaInitializer` 只做已安装 schema 检测/就绪报告，生产 DDL 走既有显式迁移入口，不允许启动时偷偷迁移。

PWE 增量：

- 保留 execution_mode=CONVERSATION 和 execution_state 原四态。新执行写 permitted_operation=EXECUTE_SKILL、execution_protocol_version=4、controlled_consent_id=NULL、operation_grant_id=NULL；原 grant/assignment/lease 完整保留。
- `output_content_mime_type` 允许 NULL；protocol=4 时从 snapshot.outputs 取允许集合，旧非4行保持原非空/原校验。移除对新协议的单一 MIME 枚举限制，SQL CHECK 必须显式 `(execution_protocol_version IS NOT NULL AND execution_protocol_version=4) OR (output_content_mime_type IS NOT NULL AND ...旧约束...)`，不能利用 SQL NULL 三值逻辑意外放行旧行。
- service 新协议不使用旧 image source/consent 表；通用源快照就在附属行 JSON，按 execution 加载，有现有最多32源边界，不新建每格式 source 表。
- PWE 终态仍负责宏观事实：文件提交为 OUTPUT_COMMITTED，撤销为 INPUTS_REVOKED，确定失败为 FAILED；未知外部结果保留 QUEUED 宏观行，由附属 phase=RESULT_UNKNOWN 阻止执行重发。
- `PersonalWorkspaceExecutionMapper.listQueuedConversationsByTarget` 的新协议分支必须 JOIN 附属行，只有 READY 才入新执行队列；RUNNING/WAITING_PROVIDER/RESULT_UNKNOWN/RESULT_READY/ARCHIVING 只进入各自恢复动作，CANCELLED/FAILED/COMPLETE 不再分发。不能仅凭主行 QUEUED 重发。
- phase COMPLETE 只在 output 已提交且会话资产索引投影完成后设置；主行 OUTPUT_COMMITTED 与 phase ARCHIVING 可共存，不虚报完整交付。
- 原 failure_code 固定 AGENT_DELIVERY_FAILED 的 CHECK 不放宽；具体技能错误存附属 last_error_code，并投影到技能状态。

`chk_pwex_execution_protocol` 当前只允许1/2/3，必须显式扩展第四个分支：protocol=4、CONVERSATION、permitted_operation=EXECUTE_SKILL、controlled_consent_id IS NULL、operation_grant_id IS NULL、runtime_input_snapshot_digest IS NOT NULL 且64位hash。`runtime_input_snapshot_digest` 写冻结 source vector 的摘要；完整 snapshot_sha256 另存附属行，二者不混用。保留旧三个分支的历史约束。同步 `ControlledImageFollowupV3SchemaInitializer` 中 execution CHECK 的期望定义和 schema detector，不让旧初始化器恢复旧 CHECK 或把正确新 schema 判为漂移；取消费用链路不能导致通用 schema 检测随图片开关一起关闭。

现有 output STAGED/COMMITTED、文件 storage/manifest、会话 asset 表全部复用。对新 MIME 移除 source 中写死的媒体分类作为存储准入条件，改为格式策略：有可信验证器就验证，无预览器走 application/octet-stream 附件下载（保留声明与检出 MIME），不信任扩展名，不 inline 执行 HTML/SVG。

不批量更改历史费用回执、旧执行摘要、typedInspection 原始证据。新代码与旧数据的审计读取不等于继续保留旧写入入口。

## 8. Runtime HTTP 与命令协议

以已存在 `/internal/agent/tasks` conversation 路由扩展，不另开公网技能执行接口。

| method/path（前缀略） | 行为 |
|---|---|
| GET `/conversation-executions/commands` | 返回 protocol4 命令；分页、只读；排除未知外部结果自动执行 |
| POST `/{task}/runs/{run}/conversation/lease`、`lease/renew` | 复用当前租约；支持 protocol4 身份 |
| POST `/{task}/runs/{run}/conversation/inputs` | 返回附属快照内已授权输入 |
| POST `/{task}/runs/{run}/conversation/inputs/{ref}/content` | 读前复验 lease/ACL，按已固定版本供字节 |
| POST `/{task}/runs/{run}/conversation/effects/{effectId}/start`（新增） | 短事务登记逻辑副作用，返回 NEW/RECORDED/KNOWN/UNKNOWN；不是费用许可 |
| POST `/{task}/runs/{run}/conversation/effects/{effectId}/result`（新增） | 持久化 Provider requestId/状态/不可变请求摘要，幂等 |
| POST `/{task}/runs/{run}/conversation/resume`（新增） | 新 session 同 Owner 同执行恢复 claim；仅返回允许的查询/上传/归档工作，不自动重新生成 |
| POST `/{task}/runs/{run}/conversation/outputs/{output}/content` | 复用分离上传与最终提交 |
| POST `/{task}/runs/{run}/conversation/output-commits/{manifest}` | 字节校验后原子提交，协议4绑定 snapshot digest |
| POST `/{task}/runs/{run}/conversation/result-commits/{manifest}` | 复用已持久结果的恢复；无效旧 session 不绕过认证 |
| POST `/{task}/runs/{run}/conversation/failure` | 仅确定失败/取消，未知副作用走专门 phase，不伪报失败 |

命令 body：`executionProtocolVersion=4,executionId,taskId,runId,conversationId,conversationGeneration,skill{key,version,packageSha256,manifestSha256},snapshotDigest,parameters,instruction,inputRefs,outputs`；授权 scope 和当前 session proof 走已有原生鉴权，不由 body 自报。

effect start body：`executionId,snapshotDigest,leaseFence,effectDigest,providerBindingRevision`；effectId 路径稳定。effectDigest 绑定 adapter、操作、参数、精确 input hashes 和绑定；不含 token。

所有 mutating endpoint 保留当前五个 X-Agent 证明头及租约规则。客户端无权供应 URL/账号/输出路径作为权限。400结构错误、401/403按现有原生认证、404隐藏对象、409状态/摘要/版本/lease冲突、503真实依赖不可用。未登记费用、金额未知不产生拒绝。已有 key 同输入返回原记录；改变输入409。

## 9. 执行、幂等与恢复算法

### 9.1 Runtime 执行伪代码

```js
async function executeSkill(command, ctx) {
  const installed = registry.requireExact(command.skill)
  validateSnapshotAndParams(command, installed)
  const resume = await ctx.claimOrResume(command)
  if (resume.resultManifest) return recoverUploadAndCommit(resume)
  const inputs = await ctx.materializeAuthorizedInputs(command.inputRefs)
  // 精确文件hash；资料不作为shell/配置执行，临时目录仅本execution可见
  const result = await runners.get(installed.runner).run({
    instruction: command.instruction, parameters: command.parameters,
    inputs, descriptor: installed,
    effects: ctx.effects, outputDirectory: ctx.outputDirectory
  })
  const manifest = await verifyAndPersistLocalManifest(result)
  await ctx.stageOutputs(manifest)
  const receipt = await ctx.commitOutputs(manifest)
  await ctx.persistReceipt(receipt)
  // 收到真实持久提交回执后才按现有留存规则清理；不是进程退出即清
  return receipt
}
```

local-script 用 argv 数组、shell=false；entrypoint 包内校验；输入只读、输出执行级目录；环境只传必要值，不继承 Provider token、其他角色 HOME 或数据库凭据。隔离复用现有 bwrap/受控工具环境；不具备所需隔离则不把“不可信脚本”标 READY。首期只安装维护方审核包。不能仅靠提示词承诺不联网。

Provider runner 在受控宿主 broker 内持有凭据；包脚本不能获得原始 token。broker 验证 binding 属于当前主体，网络目的地固定于部署配置，拒绝重定向到未批准目标。脚本请求外部副作用必须经 `ctx.effects.invoke`，不能自行放开网络。

### 9.2 effects_json：避免“通用”破坏副作用恢复

每个 execution 的逻辑 effectId 稳定，例如 `generate`、`upload-reference-1`、`submit-video`。不做通用工作流，多个步骤顺序由技能 adapter 实现；平台只登记与去重。

每项：`effectDigest,bindingRevision,status(START_RECORDED|ACCEPTED|SUCCEEDED|FAILED|UNKNOWN),providerRequestId,providerIdempotencyKey,ownerRuntimeFence,resultDigest`。Provider URL/signed URL/凭据不入公共投影。

1. 准备输入/参数；在 effect start 的短事务内核对最新 scope、lease、撤销、snapshot、binding revision。
2. 不存在 effect：CAS 插入 START_RECORDED，返回仅此 claimant 的 NEW；先 fsync 本地记录再实际发请求。
3. 同 effect 重放已存在：返回 RECORDED/KNOWN/UNKNOWN，不把它重新当 NEW。进程在登记后、发出前崩溃也按“不确定是否发出”处理。
4. 支持 Provider 幂等键且语义经 adapter 证实：恢复可用同一 key/同摘要查询或幂等重发；不支持时不能重发生成，只能查询既有 providerRequestId，无法核实则 RESULT_UNKNOWN。
5. 视频类异步返回任务 ID：记 ACCEPTED，phase WAITING_PROVIDER；后续轮询属于读取，不创建第二个任务。轮询沿实际退避/网络超时，不加业务 deadline。
6. 有 bytes：先持久结果/manifest，再上传登记。上传失败只重传相同 outputId/hash。
7. commit 成功但响应丢失：读回相同 manifest；payload 不同409；从不重复调用生成。
8. 并发两个 claimant：一个 CAS 胜出；另一个只读已有状态。后台恢复也走同一规则。

这里保证的是“本系统不盲目重复发副作用”；对不支持幂等/查询的外部 Provider **不宣称 exactly-once**。

租约到期不能让第二个 Runtime 自动重做有 START_RECORDED 的效果；恢复必须通过 current-session 的 resume 核实原执行归属。撤销后禁止新的资料读取和新副作用；已经发出的 Provider 请求不一定可取消，如实报告，不能声称退款。结果可按服务端隔离留存，但不越权发布。

### 9.3 phase 转移

```text
READY → RUNNING
RUNNING → WAITING_PROVIDER | RESULT_UNKNOWN | RESULT_READY | FAILED
WAITING_PROVIDER → RESULT_READY | RESULT_UNKNOWN | FAILED
RESULT_UNKNOWN → WAITING_PROVIDER | RESULT_READY | FAILED（仅真实查证）
RESULT_READY → ARCHIVING（主输出已经提交）
ARCHIVING → COMPLETE（asset/index登记完成）
READY/RUNNING/WAITING_PROVIDER → CANCELLED（确认取消；无法确认外部副作用则保留UNKNOWN）
```

输出和外部效果可以已经存在而用户不再授权发布；不得把取消投影成“什么都没发生”。所有 CAS 递增 version；终态重放只返回同结果，不退回 READY。

## 10. 输出提交、索引与验收的分离

1. Runtime 对本执行 outputDirectory 做真实路径 containment、symlink拒绝、文件存在、hash/size/格式检查。
2. stage 上传到现有存储；服务端 independently 校验 bytes，不信模型“已生成”。
3. 原提交事务将输出从 STAGED→COMMITTED 与 PWE OUTPUT_COMMITTED 同步，附属 phase=ARCHIVING，写既有 outbox 的定向输出事件。
4. `ChatBountyAssetProjector.projectByExecutionId` 复用原 producer/step/output 校验和 per-output 消息/asset 事务。事件失败沿既有 outbox retry；`pending(afterStepId,limit)` 保持补偿职责，非请求全量扫描。
5. 全部预期 outputId 已投影，phase=COMPLETE；事件/commit回执去重以完整 scope+execution+output+manifest 识别。
6. 下载与执行结果从真实已提交输出读取；预览/缩略图异步，不挡列表返回。没有预览器展示文件卡片+下载。
7. 对话显示“生成中/外部任务处理中/结果待核实/文件已生成，登记中/可下载/失败”。归档未完成不说全部完成。
8. 成果验收/接受/替换仍走原 `AgentTaskArtifactOutcomeServiceImpl` 与交付关联；生成或登记不自动接受成果。

索引只读元数据，分页按稳定游标；点击具体执行只读其输出，避免等待全历史核对。记录 capabilityResolve、materialResolve、provider、outputCommit、assetProjection 各段耗时以定位现有慢点；这些是观测，不是拒绝服务阈值。

## 11. 配置确定方案

继续现行 `/home/isp/conf/cyf-agent-runtime-v1/`，不迁移目录，不恢复旧 apps 链接。

新增**一个**共享 `skill-bindings.json`（schemaVersion=1），保存：

```json
{"schemaVersion":1,"providers":{"image-default":{"adapter":"image-http","endpoint":"<existing-endpoint>","model":"<existing-model>","credentialEnv":"<existing-env-name>","revision":"1"}},
 "subjects":{"<existing-agent-id>":{"providerAliases":{"image":"image-default"}}}}
```

- profile 只新增 `skillBindingsFile` 路径引用；无 `skillsEnabled/imageEnabled/pdfEnabled/...` 一串开关。安装成功且 runner 就绪才可发现。
- provider binding revision 只在端点/模型/凭据引用等有效绑定变化时递增。原始 secret 不写此文件/技能包/日志。
- 安装清单来自既有 receipt/marker，不写第二份 enabledSkills 配置。
- 当前 `controlledImageHttpEndpoint/ModelId/ApiKeyEnv/BindingId/BindingEpoch` 映射到共享 provider；新执行启用后删除 profile 的旧 image enabled/ledger 配置引用，保留旧执行日志/证据，不删历史。
- `workspace-policies.json` 保持 ACL/隔离/输出根职责，不含费用；可共用 workspace policy，但不同身份不能共用可写运行目录。
- `typedInspection*` 保留实际视觉输入/工具链/网络隔离/证据。相同验证元组可复用证据，不因角色名字强绑，也不把吴用 profile 无脑复制给林冲。安装图片技能和检测 inspector 是两回事。
- `SKILL.md` 不绑定 codexHome 绝对路径。Runtime 根据当前 profile 注入相对执行根；缓存/技能包升级不破坏原 typedInspection evidence。
- 运行目录复用当前每角色 HOME 与受控工作目录；临时产物在既有 workspace 根的 executionId 子目录。恢复账本含执行身份，不跨 Owner 扫描目录。
- 原 `ControlledImageProviderOperatorPolicy` 中混合的身份/binding/网络范围迁入通用策略；consent/定价/费用确认条件移除。不能通过跳过整份 policy 实现取消费用审批。

配置工具只生成候选+diff/readback，不修改当前生效 profile、不自动重启共享 Runtime。实际切换随版本化发布窗口执行。

## 12. 历史与切换（无永久双轨）

1. 源代码与 protocol4、前端 action-v4、技能包及配置作为同一发布批次固定；本次不编造版本号/Flow Run。
2. 先做显式增量 DDL；旧列/数据保留，新附属表空，不批量重写历史。
3. 按现有锁协调切换窗口；禁止旧协议新接纳，已有运行自然完成或进入明确可恢复状态；RESULT_UNKNOWN 不强制标成功/失败。窗口尚未满足就不切换，不抢停。
4. 在新写入口开放前，使指定 Runtime 版本、安装技能摘要、API、Web 三端协商全部达到新协议；不为配合新页面伪造 READY。
5. 旧点名任务不需重新点名：仍 ACTIVE 的原 grant 在首次新请求时，在 task-root 下依据当前 assignment/owner 创建新版本 EXECUTE_SKILL baseline 并 supersede 旧 baseline，旧快照只读保留；旧请求 key 仍按原 admission 读回，不重新接纳。新请求来自旧页面返回明确客户端升级错误，不静默翻译旧执行语义。
6. 历史审计读取保留原摘要校验或原有持久投影；历史原始记录不改成 v4。关闭旧写路由（410/明确协议错误），删除新流量不再使用的执行分支；只读历史解析不作为旧版本执行兼容层。
7. 回退：新流量开放前可恢复同批旧制品/配置，增量表保留；开放后不可直接用旧代码消费新执行。先冻结新接纳、处理新执行和效果不确定项，再按恢复批次协调。优先前向修复，绝不恢复 Provider START 来重发。
8. 前端正式验证/制品/部署走 Flow4403172；后端固定干净源码、先读 build.gradle、经现有 orchestrator gradle 串行验证/build/validateLayering；Runtime 走其版本化安装入口。develop push 不自动发布。

### 12.1 协议错误与费用旧路由收口

旧费用 issue/consume/revoke 新请求不再作为技能调用接口；旧账本只读审计，不伪造一个永远通过的 consent。旧费用/图片桥接 UI 入口删除；用户仍可正常撤销执行/资料授权，动作落在通用执行接口。无费用授权不代表执行全部不需用户任务意图：不得凭一张图片中的指令开启与用户任务无关的副作用。

## 13. 首批技能与扩展证明

- `image-generate`：现有图片 HTTP adapter，允许0..工具支持数量的参考图；费用信息 provider-priced 以 METERED/UNKNOWN 描述。
- `image-edit`：同 adapter、不新增核心分支；接受一张任务上传图或精确会话成果。
- `text-file`：将源中已有 native text-file 执行接入，修正“有资料就不提供文本生成”的发现条件。
- `pdf-export`：维护方 local-script 包，复用源中 `toolchain/requirements.txt` 的 reportlab/PyPDF2；依赖锁定在运行环境制品；不在每次请求临时 pip install；输出 PDF 走现有格式校验。
- `xlsx-export`：第三类输出验证（图片/PDF/表格），同 local-script runner，复用现有 openpyxl，不改任务/授权/成果核心。
- 视频本期不做付费实跑；统一协议支持提交 jobId→查询→取结果。接入新视频 Provider 需要实现对应 adapter、依赖及隔离配置，而不是新建视频专用业务流程。

### 13.1 PDF/XLSX 不是重新发明工具链

已查到 RT/toolchain/delivery_tool.py 与 requirements.txt 包含 PDF、XLSX 生成/解析库。首期复用其制品依赖，不另加一套 Python 环境。不过现有 create_pdf 会把内容转 ASCII replacement，不能把这个占位行为作为中文文档验收。

- pdf-export 参数固定为 `title:string, paragraphs:string[]`。脚本用已锁定 reportlab 在包内指定 CJK 字体（`assets/fonts/NotoSansSC-Regular.ttf`，入制品时带实际许可与SHA）绘制真实Unicode文本并分页；字体未就绪则依赖不可用，不能静默替换为问号。默认不执行HTML/JS、不获取外链字体；原始用户“生成要求”不是交付正文。实际正文由Agent参数提供、用户可复核。生成后用已有解析工具检查页数/文本，人工查看中文render fixture。
- xlsx-export 参数固定为 `sheets:[{name:string, rows:[{cells:[{type:'text'|'number'|'boolean'|'formula', value:<对应类型>}]}]}]`；参数子集不能表达的 type/value 联动由脚本业务校验。openpyxl 写入真实值，text 以文字单元格存储，不能让 `=...` 自动变成公式。formula 仅在明确任务意图下采用，拒绝外部工作簿/外部连接；不生成宏。重新加载核验 sheet/cell/value，不以文件存在判通过。
- 这两个技能只是首批受支持的内容范围，不声称覆盖任意复杂排版/财务模型。以后扩展自己的参数与脚本并升包版本，不改变平台接口。

每个包本身的业务生成逻辑与最小 fixture 由实施任务完成；核心接口、费用边界、状态和交付方式已经固定。依赖缺失明确安装/构建，不在运行时擅自下载或回退到高权限环境。

## 14. 实施与证据边界

详见 tasks.md 的直接代码任务及 acceptance.md。每包预计20～30分钟主动工作，非硬超时/完工承诺；超范围拆剩余实现，不再新增规划阶段。首次定向失败先定位；同输入同根因两次后停止盲重试。

本轮只交付设计与本地文档结构校验，没有新增技能、跑 Provider、改生产配置、执行 DDL、构建、发布或停机。Runtime 源/线上差异、远端/线上版本未核验的事实保留在 handoff，不能用设计完成冒充系统已修复。
