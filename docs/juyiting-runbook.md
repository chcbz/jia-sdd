# Juyi Hall Runbook

This is the short working guide for future 聚义厅/Juyi Hall iterations. Use `docs/juyiting-feature-guide.md` for deeper flow details.
For map masking, prop depth, occluder assets, and future map expansion, use `docs/juyiting-occlusion-system-design.md`.
Historical occlusion implementation sequencing is recorded in `docs/juyiting-occlusion-system-execution-plan.md`; current execution and model routing follow `AGENTS.md` and `docs/implementation/MODEL_ROUTING.yaml`.
Historical occlusion visual findings are recorded in `docs/juyiting-occlusion-visual-review-v0.md`; they do not add a separate Reviewer or release approval gate.

## 开发规范入口

遵循 `AGENTS.md`：聚义厅低于 `2.0.0` 均为内测版本，不考虑旧版本兼容，以最新契约为准；Owner 自检，无独立 Reviewer。下列数据边界是当前实现契约，变更时同步更新实现、测试与文档；安全、数据操作授权和 Flow 验证不因内测而取消。

## Primary Files

| Area | Files |
| --- | --- |
| Page composition | `web/src/components/world/JuyiHall.vue` |
| Map stage | `web/src/components/juyiting/HallStage.vue` |
| Map character token | `web/src/components/juyiting/AgentToken.vue` |
| Roster panel | `web/src/components/juyiting/AgentPanel.vue` |
| Bounty/task panel | `web/src/components/juyiting/BountyPanel.vue` |
| Chat/command panels | `web/src/components/juyiting/ChatPanel.vue`, `web/src/components/juyiting/CommandPanel.vue` |
| Selected agent summary | `web/src/components/juyiting/SelectedAgentCard.vue` |
| Data loading | `web/src/composables/juyiting/useHallData.js` |
| Conversation/events | `web/src/composables/juyiting/useHallConversation.js` |
| Movement/positioning | `web/src/composables/juyiting/useHallScene.js`, `web/src/game/scenes/HallScene.js`, `web/src/game/entities/HallAgent.js` |
| Role portraits | `web/src/composables/juyiting/useWaterMarginRoles.js` |
| Constants and role metadata | `web/src/constants/juyiting.js` |
| Visual assets | `web/src/assets/juyiting/` |

## Current Data Boundaries

- `mapAgents` is for the map stage and comes from `GET /agent/map`.
- `agents` is for roster, recommendations, ability options, and selected-agent detail surfaces.
- Roster filtering calls `POST /agent/roster`.
- Task search calls `POST /agent/tasks/search`.
- Task assignment calls `POST /agent/tasks/{taskId}/assign` with an explicit `agentId`.
- 宋江首领自动协同 uses `GET /agent/capabilities`, `POST /agent/tasks/{taskId}/recommend`, and `POST /agent/tasks/{taskId}/auto-assign`; recommendation results should remain explainable and manual assignment remains the fallback.
- Runtime abilities are client-owned snapshots: `agent.register` and `agent.presence` may refresh `agent_runtime.abilities`; persona abilities are fallback defaults only.
- Juyi Hall chat sends through `POST /chat/stream` and receives events from `GET /chat/conversation/events`.
- 招贤令 binding calls `POST /agent/personas/{personaCode}/bind`。`mode=server` 沿用租约/预留/intent，最新开发源码接入同一个统一 Runtime，不再通过旧 codex-ws-agent broker 安装；源码与上线边界见下节。`mode=local` 本轮未改，不据此推断其新验收状态。
- Do not use `/agent/active` for Juyi Hall.

### 初步任务取消（2026-10-10源码核对）

覆盖 API `36d9e5452ab8beb64b97e5570da6ede10ec38797`：所属用户调用 `POST /agent/tasks/{taskId}/cancel`，JSON 仅含整数 `expectedTaskVersion`；成功返回 `{taskId,status:"cancelled",taskVersion}`。这是后端接口，未新增前端取消按钮。

- 初步仅支持无悬赏资金事实、未实际开始的普通任务。已点将但成员尚未开始也可取消；当前执行、租约、指令或不支持的资金事实返回409，不部分写入。原 `/funding/cancel` 暂不删除，不通过普通取消绕资金结算。
- 同一事务退出邀请/已接受成员、取消待执行工作项、撤销ACTIVE执行授权、关闭无租约RETRY bootstrap，释放本任务占用；不启停共享Runtime，不清其他任务占用。保留原点将与历史事件/成果，规范终态Provider消费授权不等于悬赏托管资金，不能因此退款或重新付费。
- 已取消的完整终态任务可用原taskVersion重复请求，回读现有结果，不新增事件/版本/退出时间。LEFT/REJECTED的completedAt是原状态服务写入的退出时钟，不应误判为实际开工证据。
- 实现入口为 `api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskCancellationController.java` 与同组件 `service/impl/AgentTaskCancellationServiceImpl.java`；定向回归入口 `:agent:jia-agent-service:initialCancellation`。发布/具体生产操作证据单独见 `docs/implementation/handoffs/GSS-CANCEL-20261010.md`，不以源码核对代替线上成功。

### 统一 Runtime 托管接线（2026-10-10源码与本次生产核对）

覆盖 API `33e2344a2af02bb908a20bec1125ab7c23e8d00d`（1.14.3）、Runtime `80eadc9247132a9d6c6b3b9d7fe7b7f965e094de`；仅此范围更新，不重标其余文档基线。源码实现、安装回执和业务验收分别见下述handoff。

- 原 bind/初租/免费重整接口不变。Reconciler → `UnixManagedHostingProvisioner` 的 `runtime-hosting-v1` 私有 UDS → 同进程 `HostingControl` → 同一个 `RuntimeHost` 的单subject add/recreate；没有第二服务、旧API-key fallback或新付款通道。
- `prepare` 持久化候选而不激活；API短事务精确ensure installation并绑定原initial intent后才`ensure`。新订单通道能力检查位于资金事务外，已提交幂等回执优先回读；保留身份/租约/账本/CAS。
- 初租就绪必须完整operation/installation/host/instance/session证据及API独立`currentRegisteredProof`。进程存在、旧online或持久READY不能单独结算。免费重整沿用installation/授权，产生新session/目标代次，不重新enroll、不改租期/资金、不重启其他角色。
- 新字段：initial intent的`runtime_installation_id`、`runtime_manifest_sha256`、`runtime_provision_generation`；reprovision的`runtime_target_generation`。显式迁移资源`economy/jia-economy-mapper/src/main/resources/db/migration-gss-hosting-runtime-v1-20261010.sql`，本次已执行两ALTER并通过真实MySQL8.0.21精确catalog/触发器验证。应用不自动修补旧/不匹配catalog；新增字段后旧1.14.2 initializer不接受该catalog，本次forward-only，不盲重启旧JAR。
- Runtime配置及唯一installer说明见组件`conf/cyf-agent-runtime-v1/HOSTING-CONTROL.md`：外部私有`hostingControlPath`、独立托管provider模板、`socketGid`与API`socket-group-gid`一致；受限0660 socket与开机tmpfiles父目录。本次路径`/run/cyf-agent-runtime-v1/unified/control.sock`，runnerUid0、socketGroupGid1000。不得复制其他账号HOME/凭据；授权不确定返回RECOVERY_REQUIRED，无自动换钥/遗留锁强占功能。
- 正式后端390通过/分层与fresh bootJar；Runtime157通过/1既有跳过，另桥接2通过。API1.14.3原本地安装器verified/healthUP、Runtime固定release已安装；本次公孙胜原单ACTIVE与一次UI免费重整SERVICE_READY已真生产验收：同installation/session1→2，原租期/钱包/账本不变，三个既有subject/PID/session未重启。旧broker key按原intent精确退役，不批量吊销。
- 完整源码、发布批次、原lease/request、恢复边界与证据见`docs/implementation/handoffs/GSS-REJOIN-20261010.md`。这不是全产品或模型推理验收；未新增订单/任务/赠款，也没有卢俊义账号业务验收。

## Role Portrait Rules

- Role matching is done by `portraitRole(agent)` in `useWaterMarginRoles.js`.
- Role metadata is in `portraitRoles` inside `web/src/constants/juyiting.js`, covering all 108 Water Margin prototypes with rank, star name, name, nickname, palette, and motif.
- If an agent has `agent.avatar`, that wins.
- Per-role assets live under `web/public/juyiting-portraits/`: all 108 prototypes have static SVG fallback portraits, plus realistic PNG portraits as 4 single images and 26 `water-margin-atlas-*.png` 2x2 sheets. Do not place static files under `web/public/juyiting/`, which collides with the `/juyiting` route.
- `useWaterMarginRoles.js` prefers explicit agent avatars, then custom generated SVG for `visualConfig`, then realistic PNG/atlas portraits for matched roles, and finally the static SVG fallback. Do not reintroduce the old 3x2 sprite-grid fallback.

## UI Invariants

- Map filtering and roster filtering are separate. Changing roster status should not remove map agents.
- 厅中实景浮动点将列表用未筛选 `/agent/roster` 的当前用户可操作投影，不用 `mapAgents`；角色型 Agent 还需persona catalog 正向绑定确认，缺失/失败不能把残留 runtime 当作有效绑定。刷新后选中对象按 ID 替换为新 roster/map 对象，不保留旧权限或状态字段。
- `visibleAgents` should derive from `mapAgents`, not from roster state.
- Bounty assignment should receive the target agent from the clicked row or explicit action payload.
- Chat context should preserve selected agent, mentioned agents, selected task, and `scene: 'juyiting'` metadata.
- Keep map controls and fixed-format UI elements dimensionally stable to avoid layout jumps.
- 横屏白屏排查先检查 `JuyiHallEntry` 的 entry/background 明确高度链；反复进入地图时，melonJS 缓存 `loader.load() === 0` 不触发回调，必须处理缓存资源状态并清理等待监听，不能只验证首次横屏。
- melonJS 15 的 `video` 无 `destroy()`：重复挂载还需核对全局 renderer/run loop、当前容器 resize 与输入坐标，不能只测 loader 缓存命中。
- 弹框尺寸由常驻 `useHallExperienceMode.js` 更新，`--hall-visual-height` 仅绑定在 `JuyiHall.vue` 根节点；不要恢复 `HallStage.vue` 的 document 全局高度写入，否则退地图后会残留横屏高度。
- 厅前议事需同时验证 visualViewport-only 键盘缩高与恢复（不改变物理方向）；高度 ≤320px 使用紧凑头部，不能只缩 overlay 而让固定内容遮住输入框。典籍正文、手札各自有界滚动。
- 微信 CSS 全景旋转不是宿主原生横屏；系统键盘方向需在小程序宿主工程处理，不能以 UA 仿真结果宣称真机已修复。
- 典籍从书架进入阅读可复用同实例、身份隔离的目录；必须先读取服务端进度再选取续读章节，不能并发打开卷首并让自动保存覆盖旧断点。
- 典籍进度写入 `PUT /archive/v1/me/progress/{editionId}` 携带 `Idempotency-Key`；跨域排查先验证生产 OPTIONS 的 Allow-Headers。reader 单测必须覆盖真实 `createApi → useHttp → fetch` 边界，不能仅 mock `api.put`。

- 百宝箱执行回执与历史恢复：GET `/agent/personal-workspace/executions` 为 owner/client/tenant 隔离的只读分页，GET `/executions/request` 用原 `Idempotency-Key` 核对；404 不证明在途 POST 未受理。未知意图不能因查看另一条终态记录而被清除，刷新不能自动重复生成。
- Runtime 的精确 `/internal/agent/tasks/{taskId}/runs/{runId}/failure` POST 必须同时具备 Controller 与 native filter 允许路径；客户端 inbox `completed` 不等于交付成功，须看 outcome/服务端终态/可验证产物。见 `specs/juyiting-execution-recovery/`。
- PRIVATE `WORKSPACE_FILE_EXECUTE` 的成功事实是 `OUTPUT_COMMITTED`、owner results manifest 与 owner-safe 文件版本/摘要验证；D03 不发送 legacy `work.result` / `work.result.receipt`，验收不得伪造或要求该回执。

## Backend Areas

| Concern | Backend path |
| --- | --- |
| Agent runtime/persona/task meta | `api/agent/` |
| Juyi Hall conversation type and messages | `api/chat/` |
| General task domain | `api/task/` |

Start backend searches with:

```bash
rg -n "map|roster|tasks/search|assign|AgentRuntime|AgentPersona" api/agent
rg -n "juyiting|conversation_type|chat/stream|conversation/events" api/chat
```

## Verification Checklist

For source changes under `web/`, select the relevant `web/tests/` and run the authoritative test/build on Alibaba Cloud Flow for the exact remote commit. Do not run a local Vite production build by default and do not use local success as release evidence. Develop changes are verified without deployment. Use `4403172 / cyf-web-release` for explicit versioned releases, binding version, commit and same-Run artifact; develop push/merge does not deploy. CI-only is optional for diagnosis, not a required prerequisite; see `AGENTS.md` for build and release policy.

Useful search:

```bash
rg -n "juyiting|JuyiHall|agent/map|agent/roster|agent/active|assign-task" web/tests web/src
```

For visual changes, start the dev server when useful:

```bash
cd web && npm run dev -- --host 0.0.0.0
```

## Documentation Hygiene

- Keep this runbook short and operational.
- Put detailed flow diagrams or long explanations in `docs/juyiting-feature-guide.md`.
- When fixing a repeated issue, add one sentence here under the relevant section so future sessions do not rediscover it.

## 交付与语音诊断

- TASK 正式 PDF 交付依赖显式启用 `agent.personal-workspace-storage`、`agent.task-artifact-storage` 与独立私有根目录；验收看正式交付列表/manifest及内容下载，不以本地 PDF 或上传 201 替代。
- 语音最新契约见 `specs/juyiting-voice-realtime/design.md`；录音实现路径以对应交付 commit 为准，不将历史候选路径当作当前 checkout 的入口。保留明确 Agent/会话、发送与回复关联，网关凭据不进入浏览器；能力证明、发布、生产启用和设备验收分开报告。
- 转写立即返回 `VOICE_UNAVAILABLE/503` 时检查 Redis 准入；已复现的 Redis4 Lua 限制及隔离回归方法见 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`，不操作生产 Redis 数据。STT/TTS 的原生事件、音频终态与 fidelity 要求按最新语音契约验证。
- 历史启用/测试/发布回执见 `docs/implementation/VOICE_REALTIME_ACTIVATION_20260930.md` 和 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`；这些是历史证据，不代表当前线上 commit 或真实设备已验收。当前状态须核对精确 commit、实际 Flow Run 和在线证据。

### 自家接应安装交接（2026-10-12 23:38发布核对）
核对已上线API `0fe830d1ea` / Web `aad2ae9`（均1.14.11）、isp-install develop `a39c085`：local文书提供可信Scope的runtimeSetup，不再提供旧API Key/profile或虚构目标机路径。首次接入由目标机prepare工具生成manifest/一次性secret和非秘密handoff；本人页面显式登记六字段摘要，目标机enroll后单实例切换。查询/登记状态不等于在线，不轮询，不在响应未知时重建安装。

程序、配置、状态分别归入apps/cyf-agent-runtime-v1、conf/cyf-agent-runtime-v1、state/cyf-agent-runtime-v1/INSTANCE/agents/SUBJECT/codex-home；使用目标机获授权基目录。已有Runtime升级/目录收口保留身份、授权、完整HOME和SQLite路径索引，不重新登记/enroll。唯一操作入口：`/home/isp/wsps/chcbz/isp-install/docs/cyf-agent-runtime-v1-self-host.md`，迁移见第9节；仓内codex-ws-agent仅为内嵌执行库，不是第二套服务。

正式证据：安装器19项；API175项全过及同本地R2批次安装；前端Flow4403172 Run206成功（2932通过/2 pending），364安装文件及11公网资源匹配，现行API健康UP。tenant0原有限制未放宽；不创建生产installation、不付费，完整新用户登记E2E未执行。现行主机Runtime二进制仍1.0.2，页面不会自动升级远端机器。范围、OOM异常恢复及版本/摘要闭环见`docs/implementation/handoffs/SELFHOST-ONBOARDING-20261012.md`和`specs/runtime-self-host-onboarding/`。

### 技能包存储与安装摘要（2026-10-13局部源码核对）

覆盖API develop `b62d6e961facae02f0645b91b1072bd688d941b5` 的I04/I05，非完整技能执行/当前线上证明。现网基础切片仍API1.14.12/0833bfe、Runtime1.0.3/6325af1；发布证据见 `specs/juyiting-skill-execution/evidence/release-20261013/summary.json`。

- 唯一新增存储配置 `economy.skill.marketplace.package-store-root`，默认 `/home/isp/state/cyf-skill-packages`；对象按hash不可变寻址。quote/购买/下载在事务外prepare字节，在短事务内复验批准版本/价格/身份；旧版安装不依赖current指针。
- 普通说明包可以无manifest；可执行包安装成功回执的manifestSha256必须绑定批准ZIP内原始字节，缺失或篡改不激活、不结算。已确认不可变回执可在对象退役后重放，仍核验主体/fence/安装身份。
- 运行费用只登记说明，未知费用不影响描述校验；原技能包购买/退款事务不变。维护HTTP发布、目录READY、统一执行、资料识别/修改与结果提交链尚待后续实现，不把对象store.publish或单测通过当成可用技能。
- 定向证据分别在特性目录的i04-proof.json、i05-proof.json；生产目录/配置未在本切片创建或改写。

本小节新增覆盖（2026-10-13，API源码 `16fe9f92e2b7ea64cdf7a710fd284ee528cba155`）：I06的 `agent_skill_execution` 为PWE一对一附属快照/effect记录，不是新任务表；DDL是显式迁移资源，当前未在生产执行，也未接入protocol4写流。CAS只写mutable投影、递增version，终态不重开；RESULT_UNKNOWN不回READY；结果阶段对象manifest支持零文件。I08由agent定义 `SkillCapabilityLookup`、chat提供可信live-session目录索引，代际/断线/主体歧义fail closed；目录事实不授予安装entitlement或任务调用权限，该基线尚未接注册消息或权威可调用join（后续I10源码接线见下节，I11仍待实施）。I06定向130项、I08定向11项与layering均PASS；这两批源码未再次上线，不将单测或空registry当在线技能可用证明。

### 技能目录与认证注册（2026-10-13局部源码核对）

覆盖API源码 `02faad300b8ee27ce706e5720b31b3c221fb8bb8`、Runtime源码 `b79558e4f18b431c1ff698432b3d6a7c07aac8d5` 的I09/I10；双端已合入并push develop，尚未发布这批源码。首批在线版本沿上节发布证据，不把源码接线等同线上技能可用。

- Runtime只从既有持久安装registry/marker核验的可执行manifest测量目录，不扫描任意HOME，不要求普通说明包有manifest。按runner注册表/工具摘要/完整主体provider绑定探测；费用不参与READY。具体runner与binding文件加载尚未接入，无真实适配器不得READY。
- 完整owner scope来自已相关性校验的认证注册回执runtimeAuth，并核对安装session fence；profile、模型消息和presence均不能授予主体或能力。初次测量后额外注册一次，activation等待目录ACK；重复ACK与heartbeat只用缓存。安装变更、断线、暂停或健康撤销失效，旧异步测量不能恢复旧目录。
- API严格解析skillExecution schemaVersion1目录，仅实际认证绑定及回执送达后激活；未知字段、非法摘要/状态、重复版本与重复JSON key不可保留旧目录，缺报告替换旧数据。目录只反映运行事实，I11仍须权威安装entitlement/descriptor及任务权限join，不直接授予调用权。
- I09定向262项；I10 Runtime416项、Java46项及layering PASS。证据 `specs/juyiting-skill-execution/evidence/implementation-20261013/i09-proof.json` 与 `i10-proof.json`。未真实Provider调用/生产DDL/Web发布；上传图片→识别→修改完整业务验收仍NOT_RUN。


### 技能安装与运行能力核对（2026-10-13 局部源码核验）

覆盖API源码 `2fb221ae15797c819b0fcb674880730bca1cf166` 的I11a，已合入/push develop、**未发布**；当前旧action-v3实现不是最终技能执行协议。

- `InstalledSkillDescriptorLookup`/`InstalledSkillDescriptorService`只读真实安装证据：精确Owner/canonical Agent、ACTIVE entitlement/order、SUCCEEDED installation及相同activation epoch、批准权限和包摘要、成功result receipt与安装/host binding。普通说明包明确NOT_EXECUTABLE；结果消息ID不等于安装command ID。包准备仍在事务外；缓存仅不可变内容，权限每目录统一末尾复读，不按技能重复读取全量entitlement。
- `ChatActionCapabilityService.inspectInstalledSkills`只投影安装/Runtime观察：匹配当前scope/fence与manifest/runner/摘要、工具和Provider绑定要求，join后复核live目录；断线、主体歧义、缺依赖、目录切换不能保持旧运行就绪。metadata仅白名单描述/schema/输入/输出/costInfo，没有执行路径或内部主体配置。
- `RUNTIME_READY` **不是任务可调用/执行授权**，也不会因此新增availableActions。任务ACL、目录HTTP和EXECUTE_SKILL baseline/接纳仍待I11b/I16/I18；费用信息不参与本核对，购买/退款链保持。当前receipt按installation读取尚待受控索引/schema接线；未证明生产目录读取性能，不开放未完成的HTTP路由。
- 定向171 tests与layering PASS，包含真实H2安装/回执SQL；不是MySQL catalog/在线识图证据。历史失败、固定输入与最终证明见 `/home/isp/wsps/cyf/specs/juyiting-skill-execution/evidence/implementation-20261013/i11a-proof.json`。完整上传→识别→修改→下载仍NOT_RUN，无新配置、生产DDL、Web或本批API/Runtime发布。

### 图片技能当前运行基线（2026-10-15 局部在线核验）

本节仅更新吴用图片技能与相关协议边界；以上2026-10-13切片说明保留为历史基线，不代表当前线上仍未接线，也不据此宣称全部接口/全部技能完成验收。

- 已上线：Web1.16.1（Flow4403172/Run213，commit `421f628c245b83466cafb70510ff69188180bdee`）；API1.16.5（本地build `cyf-interface-api-release-20261015-r12`，commit `6116a10403e0df250850e6ebb73f8123f5ac9ded`）；Runtime1.2.7（commit `6a9d8d3c1219450c19b3edfbef317e615940ab5d`）。本节不重标历史制品或历史验收。
- 技能目录可调用必须同时满足真实安装权益、当前认证session与测量能力、任务及资料授权。认证回执先在API边界将Receipt显式投影，统一wire使用 `runtimeInstallationId` 和十进制字符串 `sessionGeneration`；Runtime不可按JS Number接收。不能因安装成功或目录不可用而重复购买或直接补数据库记录。
- 技能包 `skillVersion`（如`1.0.0`）是语义版本，不是Long；`factsManifest`及`contextSnapshot.facts`内的action descriptor按其技能契约校验，不能误用通用`*Version`整数校验。其他状态版本/代际及CAS检查保持；取消请求的公开 `expectedStateVersion` 是可选十进制字符串，在API边界严格转Long，不放宽全局JSON类型转换。
- 原生模型output schema按本次冻结的availableActions生成并绑定digest；无可用action时只允许ANSWER/CLARIFY。当前参数投影支持封闭对象、全部属性required的保守子集；可选属性/开放对象/`$ref`等不支持的schema明确报`ACTION_MODEL_SCHEMA_UNSUPPORTED`，不能宣称通用JSON Schema支持或静默删参数。当前image-edit参数为空封闭对象，已真实运行。
- 任务459实际已执行image-edit，Provider结果归档为`RESULT_COMMITTED`，页面预览/下载成功，下载摘要与成果manifest匹配。三角形由蓝变黄，其余形状、文字及相对布局保留；生成图由800×600放大为1448×1086并带轻微纹理，不承诺像素级无损编辑。首次识别形状/颜色/位置正确，但Q7Z5被误读成0725，识别质量不能按“请求完成”判定全通过。
- 费用只登记：本次目录costInfo为UNKNOWN，商品零价不等于Provider运行免费；未新增费用审批或外单功能，认证、资料隔离与第三方回调未放宽。
- 发布/测试证据：`/var/tmp/cyf-interface-api-release-20261015-r12/`、`/var/tmp/cyf-interface-runtime-release-20261015-r8/`。在线成果与下载校验：`/var/tmp/cyf-interface-ui-acceptance-20261015-r2/task459-image-result-manifest.json`、`download-image-verification.json`；完整任务接续仍在`specs/juyiting-skill-execution/handoff.md`。
