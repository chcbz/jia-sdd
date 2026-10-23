# Juyi Hall Runbook

This is the short working guide for future 聚义厅/Juyi Hall iterations. Use `docs/juyiting-feature-guide.md` for deeper flow details.
For map masking, prop depth, occluder assets, and future map expansion, use `docs/juyiting-occlusion-system-design.md`.
Historical occlusion implementation sequencing is recorded in `docs/juyiting-occlusion-system-execution-plan.md`; current execution and model routing follow `AGENTS.md` and `docs/implementation/MODEL_ROUTING.yaml`.
Historical occlusion visual findings are recorded in `docs/juyiting-occlusion-visual-review-v0.md`; they do not add a separate Reviewer or release approval gate.

## 同平台Agent接外单（2026-10-22核对）

本节覆盖API `94b4c8a5`（1.16.25/Flow223）、Web `44aa9c71`（1.16.37/Flow283）、Runtime `c11a078e`（1.2.3）的D3.1实现和本轮生产验证；下方其他模块保持各自原核对基线。合同与分层证据见 `specs/juyiting-external-commission-mvp/`。

- 同平台由认证的tenant_id和client_id同时精确相同决定，不由显示名/账号名推断。开关属于单个Agent的当前绑定，默认关闭；只能本人在Agent详情内管理。候选为本人Agent及同平台开启接外单的其他Agent，能力仅用于推荐，不引入收费或任务类型准入。
- 两类承办共用point-and-deliberate：选择不执行，确认委派沿原grant快照和自动首轮执行，不增加订单、待指令或二次开始。关闭只拒绝新外单，本人和存量授权不受该开关影响。
- 数据域A（任务/资料/会话）与执行域B（Agent/绑定/Runtime）分别固定；本人A=B。实时执行、租约、聚合及回报共用task/grant-scoped authority，要求当前ACTIVE grant及完整冻结B/binding。历史冻结身份只用于历史读取，不授权实时执行；缺字段不通过本人fallback掩盖。私域Workspace和原本人团队Plan权限未扩大。
- 正式Flow、安装制品摘要、双账号文本/PNG提交验收和本人恢复后实答已核验；这些是本功能范围证据，不等于平台零故障。运行端通道ready不证明typed/model就绪；本轮本人thread/start超时在精确空闲子进程恢复后复测通过，但超时/重连就绪根因仍未闭环。共享运行端已有其他历史未完成任务时，不重启整个unit、清队列或冒充成功；先定位原记录并按实际授权恢复。细节保留于特性handoff及release-20261022证据，不作为自动恢复策略。

## 开发规范入口

遵循 `AGENTS.md`：聚义厅低于 `2.0.0` 均为内测版本，不考虑旧版本兼容，以最新契约为准；当前串行执行，Owner 自检后进入独立只读 Review，再按用户授权确认。下列数据边界是当前实现契约，变更时同步更新实现、测试与文档；安全、数据操作授权和 Flow 验证不因内测而取消。

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
| Guided onboarding | `web/src/components/juyiting/HallOnboarding.vue`, `web/src/composables/juyiting/useHallOnboarding.js` |
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

### 厅内连续问答：本轮收尾（2026-10-11 18:13，已发布/普通密议两轮实测）

覆盖线上Web1.14.6 `7b14dffd5d9d259df720f84e57a8453424fb0a65`（Flow199）、API1.14.4 `fb8a43b0c1b8774582e520a809e5f52337198c25`（本地同批制品原installer verified）。普通密议已实测同话头连续两问、下一轮解锁和重取历史；不是全场景/图片端到端验收。详设及验收边界见 `docs/implementation/HALL-DISCUSSION-ROUND-CLOSEOUT-DESIGN-20261011.md`、`docs/implementation/handoffs/HALL-ROUND-IMPLEMENTATION-20261011.md`。

- 同一话头一轮结束后再发下一轮：结束request，不关闭conversation，不清历史；没有新增并行提问/自动排队/自动取消。
- 普通CHAT/INSPECT POST在完整权威RequestView覆盖本次全部turn且全部终态后EOF；PARTIAL必须检查子turn。buffer先注册再读快照，单POST订阅关闭不影响会话GET events。typed `/interactions`不走该relay，含EXECUTE/未知step不套CHAT终态谓词。
- public/private前端每次发送持有独立session；终态GET释放本轮reader/发送锁，EOF自身不是业务完成。旧回调、poll、finally和正文恢复不能覆盖新轮/换身份；最终正文加载失败与业务终态分开，不重复POST。
- 本次连续问答无新增表/接口/Runtime改动。正式发布后端205项及分层/freshbootJar通过；前端Flow4403172/Run199 SUCCESS（2917通过、2既有pending、0失败）。线上同一吴用密议两request均COMPLETED，第二轮保留上下文，重取保留4条消息；public多Agent线上未测、浏览器主动收尾不等于独立观测服务器自然EOF，具体边界见handoff。
- 图片链路当前核对（2026-10-11）：Runtime配置根为`/home/isp/conf/cyf-agent-runtime-v1`，Runtime1.0.2/`5b902c1`；仅吴用图片配置已启用，不推断其他Agent。新普通事项445已真实生成蓝鸟→基于首图改红鸟→鉴权预览/下载→正式验收→刷新恢复完成；原图可读、当前交付只取改图。最终验收线上为API1.14.7 `cf1402727466e1e51db0860200dc178eab2096c4` / Web1.14.8 `621b87a1b977e5c8fd0ef9cd22b068d7d0622b42`（Flow201）。生成/编辑发生于前一发布1.14.6/1.14.7，升级后未重复Provider调用。内容保留偏差：红图透明背景而非要求白底，不称视觉内容完全通过。证据与分批边界见 `docs/implementation/HALL-IMAGE-RETEST-20261011.md`。
- 图片识别配置核对（2026-10-12；覆盖吴用、Runtime 源码 `5b902c1bcd3efced9720e015e3b8240d39ce0738`）：图片生成/编辑与 `INSPECT` 分开启用。现用 `/home/isp/conf/cyf-agent-runtime-v1/unified-profiles/wuyong.json` 已补齐 `typedInspection*`；真实模型/载体证据在 `/home/isp/conf/cyf-agent-runtime-v1/inspection-evidence/wuyong-20261012.json`。任务450的正常业务接口已走通 `CHAT → INSPECT`，原PNG的 `LOCAL_IMAGE` 摘要回执与蓝鱼/白底识别答案一致；当日接口验证与页面回读通过；独立的页面发送问题已在下述2026-10-13版本修复并单独复验，不能用此前接口验证替代页面证据。`codexHome` 绝对路径不直接进入识别稳定摘要，二进制身份、模型、Provider与隔离策略仍绑定；迁移后须按最新配置重新测量，不复用旧路径候选或伪造能力证据。完整边界/迁移交接：`/home/isp/state/cyf-diagnostics/hall-image-inspect-20261012/HANDOFF.md`。
- 议事发送前检查核对（2026-10-13；Web修复 `92320bc6c15cd6f0328ee99bbf191da2bc9c32a6`，发布1.14.12 `cb730681570688e0051b5cd79737a3c004817881`）：已有榜文会话不能依赖本浏览器的原点将恢复记录来取得 `assignmentRevision`；缺失时读取 owner 鉴权的 `GET /chat/conversations/{conversationId}/interactions/context`，严格匹配事项、任务版本、目标好汉和会话代际，不从历史成果或 `taskVersion` 猜测指派版本。身份/上下文变化丢弃迟到响应，失败不提交、不清空草稿。指派检查先于成果索引检查；同一上下文并发索引刷新等待同一读取，保留后续刷新与旧读取隔离。任务450只读复现为索引准备成功、指派版本为空而答复刷新失败，并非接口读取慢；原统一提示掩盖了真正原因。本机受影响回归386项通过；补充不部署CI `5263692/Run11` 对精确源码2952项通过、2项pending，构建成功。验收页同步透传索引读取错误，不降级绕过核对；前述为源码验证；正式Flow4403172/Run207对1.14.12完成同批测试、构建与部署，364份安装文件及11份公网资源与制品匹配。全新浏览器任务450真实发送一次HTTP202，自动恢复指派并走通CHAT→INSPECT，原PNG的LOCAL_IMAGE摘要一致，新识别答案在页面自动显示；未重复生图或重置START。发布后已恢复原仅验证配置。证据：`/home/isp/state/cyf-diagnostics/hall-image-inspect-20261012/catalog-send/`与`catalog-release/RESULT.json`（同诊断根目录）。
- 新建事项图片资料场景复核（2026-10-13；线上Web1.14.12 `cb730681570688e0051b5cd79737a3c004817881`；仅诊断、未修复）：办事页选择工作空间PNG可成功提交并绑定固定版本，但新点将回执含 `GENERATE_TEXT_FILE`，现有前端 `hallPointAndStartIntent.js` 的操作集合/普通议事权限精确比对未同步，导致服务端已受理而页面报回执不匹配。任务455按界面提供的林冲实测，识别和显式附图后的改图均返回澄清，无INSPECT/EXECUTE子请求、无图片交付；林冲现用profile未见吴用的识别认证配置，受控图像能力只读返回UNAVAILABLE且无providerBinding。后续消息需要另勾选“随本条消息发送”，任务原图未默认随消息附带。此前任务450吴用的已生成成果识别成功不能推广为全部Agent或新建事项资料流程通过。证据 `/home/isp/state/cyf-diagnostics/hall-upload-inspect-edit-20261013/RESULT.json`；先同步最新点将契约并核验所选Agent真实能力，再回归完整入口，不重复点将或重置原事项。
- 图片现行契约（2026-10-11，覆盖上述API/Web）：已提交输出来源按link/request/step的`OUTPUT_COMMITTED`核验，改图源及验收不能仍要求旧`RUNNING`，不加双状态兼容；保持owner/client/tenant、grant、lineage及bytes/hash核对。媒体回执可含序列化的`messageSource:null`，不能误拒；非null混合来源/未知字段仍拒绝，提交请求契约未放宽。验收成功必须同时核operation completed/TASK_COMPLETED、delivery accepted和task completed；页面刷新只读恢复同operation，不自动重POST。

## Role Portrait Rules

- Role matching is done by `portraitRole(agent)` in `useWaterMarginRoles.js`.
- Role metadata is in `portraitRoles` inside `web/src/constants/juyiting.js`, covering all 108 Water Margin prototypes with rank, star name, name, nickname, palette, and motif.
- If an agent has `agent.avatar`, that wins.
- Per-role assets live under `web/public/juyiting-portraits/`: all 108 prototypes have static SVG fallback portraits, plus realistic PNG portraits as 4 single images and 26 `water-margin-atlas-*.png` 2x2 sheets. Do not place static files under `web/public/juyiting/`, which collides with the `/juyiting` route.
- `useWaterMarginRoles.js` prefers explicit agent avatars, then custom generated SVG for `visualConfig`, then realistic PNG/atlas portraits for matched roles, and finally the static SVG fallback. Do not reintroduce the old 3x2 sprite-grid fallback.

## UI Invariants

- 横屏 `landscape-map` 且 `homeMode=map` 使用沉浸地图：隐藏业务 shell 的 header/toolbar/footer，启用既有 Stage 轻量悬浮 HUD；概览保留业务导航。竖屏仅地图上的“横屏看全景”提供方向入口，不显示工具栏／弹窗方向按钮或地图缩放复位按钮。Stage、打开的面板和草稿在旋转中保持同实例。
- 地图画布采用 cover 裁切，回归检查 Stage 填满容器且 canvas 覆盖四边，不能要求 canvas 与屏幕宽高完全相等；悬浮栏图标须能在已安装 Varlet 图标集中解析。

### 需求入口与事项列表（2026-10-11 源码局部核对）

覆盖Web1.14.9 `a3bceafb53b4bea2545ad3065af058c48400605e`（Flow4403172/203，2026-10-11 21:48 +08:00部署及线上资源核验通过），仅入口/事项列表与取消布局范围，不重标其他基线：默认“提出需求”统一经 `openDefaultRequirementCreate` → `openPrivateDraft` 打开独立 `HallDraftEditor`（draft浮层），宽窄屏及多媒体开关均不再跳到事项内填表。保留现有草稿保存离开保护、返回栈与来源筛选；BountyPanel仅管理既有事项，不再暴露 `openCreateRequirement` 或创建表单/提交事件。已有普通/资金请求结果未知时的核对与原请求恢复入口保留，不代表允许新建。取消区按钮等宽、保留描边次级样式，内部12px间距/上下16px留白；资金展示与撤榜使用原金额校验/事件，普通取消条件和确认逻辑不变。源码与定向证据见 `docs/implementation/handoffs/BOUNTY-TOOLBAR-20261009.md` 的2026-10-11跟进。

- Map filtering and roster filtering are separate. Changing roster status should not remove map agents.
- 厅中实景浮动点将列表用未筛选 `/agent/roster` 的当前用户可操作投影，不用 `mapAgents`；角色型 Agent 还需persona catalog 正向绑定确认，缺失/失败不能把残留 runtime 当作有效绑定。刷新后选中对象按 ID 替换为新 roster/map 对象，不保留旧权限或状态字段。
- `visibleAgents` should derive from `mapAgents`, not from roster state.
- Bounty assignment should receive the target agent from the clicked row or explicit action payload.
- Chat context should preserve selected agent, mentioned agents, selected task, and `scene: 'juyiting'` metadata.
- Keep map controls and fixed-format UI elements dimensionally stable to avoid layout jumps.
- Reader capsule avoidance is in `web/src/components/juyiting/archive/ArchiveReader.vue`: normal/native layouts reserve the right edge; virtual 90-degree landscape reserves the logical left and rotates safe-area mapping. Verify the lazy Juyi Hall CSS, not just index CSS; [Flow 85 release evidence](releases/2026-09-09-reader-flow85.md).
- Onboarding follows the actual `portrait-command` / `landscape-map` experience (including virtual landscape), with separate steps. Keep portrait `data-tour` anchors aligned with their buttons; map steps must use runtime hotspot bounds and canonical map IDs, not fixed screen coordinates. Preserve replay, versioned dismissal, and modal focus restoration.
- Onboarding geometry is isolated in `web/src/components/juyiting/hallOnboardingGeometry.js`; verify it with `web/tests/hall-onboarding.test.mjs` (Node test runner) and `web/tests/juyiting-hall-onboarding-geometry.test.js` (Mocha component tests).

## Mini Program Public Entry

- Cold launch loads `https://kit.chaoyoufan.cn/?nativeOrientation=portrait&entry=direct`; `/` explains the product to guests (valid logged-in sessions follow the existing redirect to `/juyiting`), `/demo` is a local simulation, and `/juyiting` is the authenticated workbench.
- Public links use `web/src/utils/publicEntryNavigation.js` to preserve only portrait context and allowlisted entry markers, never source URL credentials or arbitrary redirects.
- Keep fixed native landscape navigation unchanged. The portrait fallback `entry=fallback` must load `/juyiting`, not the introduction.
- The paired shell is at `C:/Users/Think/WeChatProjects/juyiting`; run paired tests with `MINIPROGRAM_PROJECT` set to that checkout. Release and physical-device acceptance remain separate gates; see `specs/miniprogram-public-entry/acceptance.md`.
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

### 验收状态刷新恢复（2026-10-09核对）

覆盖Web `17ecf1c0b581cab1456acff4db097a6a4d335e3d`（1.14.1）的 `useHallBountyFinalization.js` 与 `BountyExecutionOutputs.vue`：恢复合法本地intent后，按operationId或原幂等键自动一次GET回执，不自动resume/POST。核对中与未知/查询失败不能表述成“验收尚未完成”；服务端任务完成与已校验回执完成分开呈现。身份/会话/任务切换及卸载取消旧请求并忽略迟到响应，完成任务不能再次提交验收。刷新复验应同时核对正式成果正文、回执终态与网络中无重复验收POST。

线上交付证据与范围见 `docs/implementation/UR06_REQUIRED_RUNTIME_CLOSEOUT_DESIGN_20261009.md` 当前交付摘要；此条不代表其他账号或历史任务已验收。

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

For onboarding changes, run the local behavior checks from `web/`:

```bash
node --test tests/hall-onboarding.test.mjs
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter dot --exit tests/juyiting-hall-onboarding-geometry.test.js
```

For behavior changes, also inspect relevant tests under `web/tests/`. Useful search:

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

## Login token lifetime

Access-token TTL 的当前调整目标为 24 小时（PT24H），授权码仍为 5 分钟；配置来自 OAuth client 数据库，不是在前端延长本地缓存。已上线实例使用 `api/user/jia-user-mapper/src/main/resources/db/account-security-access-token-ttl-24h.sql`，先备份并只更新目标 client 的 TTL。只影响新签发 token；本地候选验证与生产生效状态见 `specs/account-security-foundation/acceptance.md` 的 TOKEN-TTL-24H 节。

## 交付与语音诊断

- TASK 正式 PDF 交付依赖显式启用 `agent.personal-workspace-storage`、`agent.task-artifact-storage` 与独立私有根目录；验收看正式交付列表/manifest及内容下载，不以本地 PDF 或上传 201 替代。
- 语音最新契约见 `specs/juyiting-voice-realtime/design.md`；录音实现路径以对应交付 commit 为准，不将历史候选路径当作当前 checkout 的入口。保留明确 Agent/会话、发送与回复关联，网关凭据不进入浏览器；能力证明、发布、生产启用和设备验收分开报告。
- 转写立即返回 `VOICE_UNAVAILABLE/503` 时检查 Redis 准入；已复现的 Redis4 Lua 限制及隔离回归方法见 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`，不操作生产 Redis 数据。STT/TTS 的原生事件、音频终态与 fidelity 要求按最新语音契约验证。
- 历史启用/测试/发布回执见 `docs/implementation/VOICE_REALTIME_ACTIVATION_20260930.md` 和 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`；这些是历史证据，不代表当前线上 commit 或真实设备已验收。当前状态须核对精确 commit、实际 Flow Run 和在线证据。

### 远端自家接应历史实测边界（2026-10-11，李逵；当前文本能力见下文）
- 核对源码：isp-install Runtime1.0.2/`5b902c1bcd3efced9720e015e3b8240d39ce0738`；受测Web1.14.9/`a3bceaf`、API1.14.7/`cf140272`。仅覆盖李逵在173.230.149.118的独立主机统一Runtime（非与本生产机合并进程），既有installation/enroll、两轮文字密议与事项446文字正式验收；未发布Web/API。
- 主机配置在`/home/isp/conf/cyf-agent-runtime-v1`，状态在`/home/isp/state/cyf-agent-runtime-v1/unified`；新服务`cyf-agent-runtime-v1@unified`，该主机旧`codex-ws-agent`已停用。不要重启旧服务形成双实例。
- 远程接入不止需要`/agent/runtime/v1`与WS：原生文件/技能等还有`/internal/agent/`路径。当前公网网关无对应location，李逵Node请求实际444，文件通道尚未通过；不通过开放全部internal或绕过Runtime鉴权处理。页面旧安装文书也尚未更新。文字验收不代表这些能力可用。
- 来源：`/home/isp/wsps/cyf/docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`、`/var/tmp/cyf-likui-selfhost-20261011-8qhccv/business-acceptance-final.json`。历史服务PID和当次过程留handoff，不作为今后在线状态依据。

### 已取消事项成果操作区（2026-10-11 局部源码核对）
- Web `d8b703b9fae877daf224e159850f0f7c97ccf174`：正式成果与验收页的两个“重新读取”入口使用独立描边按钮组，12px间距、44px最小高度，≤600px纵向等宽；仅布局变化，仍走原历史成果/议事文字读取，不恢复办理或验收。当前只完成本机定向诊断，非上线声明；证据见 `docs/implementation/evidence/terminal-history-layout-20261011/`。
- 2026-10-11 补充局部源码核对 `36c447ceb3f067618df37b934cb813e819aa88b3`：正式成果与验收页（formalTaskRef存在，不限状态）不展示标题栏协作工作台按钮；返回普通事项后沿用原开关与subject条件恢复入口，TaskWorkspacePanel未下线。仅本地定向诊断通过，未发布。

### 2026-10-11 公网自家接应：Runtime原生网关

核对API `cf140272`、Runtime1.0.2与根仓网关配置 `f6f34cd0`。本机Runtime直连127.0.0.1:10018不代表远端链路可用；远端需经api.chaoyoufan.cn的原生路径白名单。配置源码位于 `ops/ci/aliyun-flow/host/nginx/`，安装到 `/home/isp/apps/nginx/conf/snippets/` 并由该域名vhost include；后端installation/session/channel/owner/task鉴权仍是唯一授权依据，不代理整个internal，不注入身份头。

李逵173.230.149.118在实际公网轮询已从444恢复200，原Runtime未重启。此结论只覆盖网关：新事项448的通用文本文件请求停在CLARIFY，当前议事动作清单没有通用文件生成适配；不等同全文件/技能/图片流程通过。详细验收边界见 `docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`，该处历史22:19“未改Nginx”已由后续授权部署记录更新。

### 李逵公网自家接应：文本文件正常流程（2026-10-12局部核验）
- 当前核验组合：API1.14.10/`cd1e6d6ebe`、Web1.14.10/`235048e6`（Flow205）、isp-install Runtime1.0.3/`807b86d`；仅覆盖173.230.149.118李逵的无附件UTF-8纯文本生成、上传提交、预览/下载与正式验收。原448的历史CLARIFY结论不代表新版能力；不回填旧grant。
- `GENERATE_TEXT_FILE`为独立EXECUTE操作，必须同时有当前task grant、`nativeConversationTextFileEnabled`配置及实际ready的文本执行器声明；不是普通聊天任意写盘，也不要求开启图片付费能力。输出text/plain必须同时通过配置和数据库`chk_pwex_output_mime`，不可只更新其中之一。
- 文本动作稳定子请求ID与图片动作的域不同；准入与进度投影共用文本requestId计算，不能把“执行关联不一致”当作文件生成失败而重复点将。完成后按既有正式成果finalization验收，保存到工作空间不是前置条件。
- 原事项449真实文件/下载字节SHA与验收选中成果一致，finalization完成且刷新后事项completed；不代表其他格式转换、文件编辑、图片或全体角色验收。当前下载名为系统output_1.txt（议事卡片part_ID.txt），尚不保留用户指定文件名。
- 稳定源码及边界详见`/home/isp/wsps/cyf/docs/implementation/LIKUI-TEXT-FILE-ACTION-20261011.md`；当次验收、失败与发布证据留`/home/isp/wsps/cyf/docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`。历史PID/批次不作为今后在线状态依据。
- 本文上方两项页面局部优化已纳入Web1.14.10/Flow205并发布；其“仅本机诊断/未发布”描述属于2026-10-11历史阶段，而非当前发布状态。

### 自家接应安装交接（2026-10-12 23:38发布核对）
核对已上线API `0fe830d1ea` / Web `aad2ae9`（均1.14.11）、isp-install develop `a39c085`：local文书提供可信Scope的runtimeSetup，不再提供旧API Key/profile或虚构目标机路径。首次接入由目标机prepare工具生成manifest/一次性secret和非秘密handoff；本人页面显式登记六字段摘要，目标机enroll后单实例切换。查询/登记状态不等于在线，不轮询，不在响应未知时重建安装。

程序、配置、状态分别归入apps/cyf-agent-runtime-v1、conf/cyf-agent-runtime-v1、state/cyf-agent-runtime-v1/INSTANCE/agents/SUBJECT/codex-home；使用目标机获授权基目录。已有Runtime升级/目录收口保留身份、授权、完整HOME和SQLite路径索引，不重新登记/enroll。唯一操作入口：`/home/isp/wsps/chcbz/isp-install/docs/cyf-agent-runtime-v1-self-host.md`，迁移见第9节；仓内codex-ws-agent仅为内嵌执行库，不是第二套服务。

正式证据：安装器19项；API175项全过及同本地R2批次安装；前端Flow4403172 Run206成功（2932通过/2 pending），364安装文件及11公网资源匹配，现行API健康UP。tenant0原有限制未放宽；不创建生产installation、不付费，完整新用户登记E2E未执行。现行主机Runtime二进制仍1.0.2，页面不会自动升级远端机器。范围、OOM异常恢复及版本/摘要闭环见`docs/implementation/handoffs/SELFHOST-ONBOARDING-20261012.md`和`specs/runtime-self-host-onboarding/`。

### 本机旧 Agent 目录已退役（2026-10-12 局部运维核验）
- Runtime仍为1.0.2/`5b902c1bcd3efced9720e015e3b8240d39ce0738`原制品；本次只迁路径、没有API/Web/Runtime版本发布。旧`apps/codex-ws-agent`和`apps/codex-ws-agent-instances`完整归档至`/home/isp/baks/runtime-path-unify-20261012/retired`，旧服务masked、旧bin启动脚本已归档，无兼容链接。
- 三静态Agent的codexHome统一为`/home/isp/state/cyf-agent-runtime-v1/unified/agents/{角色}/codex-home`；策略和模型目录文件在`/home/isp/conf/cyf-agent-runtime-v1/`。旧历史数据保留state下history，59个会话索引路径同步；不得再照抄旧HOME或旧policy路径。
- 三静态Agent在线，旧根无活动进程引用；吴用既有图片识别证据不变、无模型调用重测READY。此核验不包括恢复原已离线的托管Agent。内嵌`codex-ws-agent/`执行库仍保留；详见`docs/implementation/handoffs/RUNTIME-PATH-UNIFY-20261012.md`。

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

### 议事输入框不自动填充（2026-10-16源码核对）

覆盖 Web commit `2c8d6703eead623f555029341101cb688b9d448a` 的密议入口、榜文议事及 briefSelectedTask：进入会话不再写入默认开场白，保留已有用户草稿和显式 @ 行为；原权限与上下文绑定不变。仅为源码行为，不代表线上已切换。定向诊断及发布边界见 `docs/implementation/handoffs/DISCUSSION-NO-PREFILL-20261016.md`。

### 资料管理诊断基线（2026-10-16）

本轮只读审计固定Web `2c8d6703eead623f555029341101cb688b9d448a`、API `fc399976710f5b724916013926be2cbff899af8c`。资料版本/元数据revision/byteLength在当前HTTP wire为十进制字符串；组件版本选择不能转为number。资料写操作须保留精确版本前置条件、目标fileId/身份隔离和原意图幂等；不能把gzip表示ETag原样当业务版本、不应在未知结果时换key重传。目录/详情/写回执须分别绑定查询或文件代次。当前实现存在已复现缺陷，不代表这些要求已修复。

本轮覆盖文件生命周期、资料引用、预览/下载和身份/并发边界：前端70项既有回归通过，后端104项中11项HTTP测试失败；源码和隔离复现/生产日志的边界、逐功能矩阵及修复顺序见 `docs/implementation/WORKSPACE-MANAGEMENT-AUDIT-AND-REPAIR-20261016.md`，原始证据保留 `docs/implementation/evidence/workspace-management-audit-20261016/`。无新发布，不以此更新线上版本结论。

### 技能终态与异常停机发布（2026-10-16局部核对）

- 源码覆盖：API `ab379ba8f27a3b1481fc426d6d007ae76b096b2e` 的 PWE 启动校验。`RESULT_COMMITTED` 是协议4技能结果的合法终态；技能终态校验和任务执行校验均须接受它，并继续拒绝缺失/错误协议版本和无效任务、会话授权栅栏。不要把合法结果回写旧状态来让启动通过。
- 现行发布控制器的显式 `stoppedRecovery` 输入用于已经异常停机的 API：`runtimeGeneration=null`，绑定当前 JAR/安装记录、同一 boot、固定候选和真实恢复授权，并重新确认无 canonical Java writer、无10018监听、无运行记录；不从失败的live校验自动回退、不伪造历史PID或正常停机回执。原制品准入、coordinator→release→lifecycle锁、备份、安装、健康和schema检查继续保留。控制源码固定版本 `8dd17271f2206d39a2ebfb0f4fd4e641e7a3ae23`，只覆盖这条新增恢复输入，其余路径沿用既有基线。
- 实际测试/制品/安装与线上核验分别见 `docs/implementation/handoffs/API-STARTUP-RECOVERY-20261016.md`。本节不把健康检查当完整业务验收，也不表示健康监控的自动恢复摘要绑定已修复。
- 发布核验补充（2026-10-16T16:25:40.933551+08:00）：API1.16.6同批本地制品已由原发布器verified，canonical进程/摘要/healthUP及公网未认证鉴权边界已核验；无生产数据重写。完整业务与自动恢复机制不在该上线结论内。

### 点将册技能／本领与响应式详情（2026-10-17局部源码及Web1.16.9线上核验）

覆盖API `b76a1d0aeda572767a6d4734d050121d985bd9c9`、Web `6fbdb6618b1132316a95db87cca9402de83138e8`；仅点将册展示与只读资料接口。API保持1.16.8／Flow152；Web1.16.9经Flow225同Run制品部署，完整应用7视口/36次实际profile GET通过，不外推其它模块或历史删例覆盖。

- **本领**沿用Agent原权威投影：Runtime已上报入库的abilities，只有空白字符串回退persona；字面量`[]`是真正空值。名册、地图、旧Agent详情和能力索引继续保留各自abilities字段，不新增本领存储或第二套回退规则。
- **技能**来自现有安装权益／回执／包摘要核验与当前认证Runtime目录，详情分开展示安装核验和运行状态。已核验安装数不等于目录条数或READY数；`RUNTIME_READY`不授予任务调用权限。任务目录仍需原任务授权，市场权益接口仍负责交易/安装关系，不混入本领。
- 新`GET /agent/{agentId}/profile-capabilities`仅当前拥有者可读非系统Agent，无query/body；单次只读聚合原本领与白名单技能状态，不推进Agent技能版本、不扫描、不重注册、不派单。技能描述源失败时可保留本领并明确技能不可用，不伪造空目录成功。
- Web只在当前可见、owned、非system详情发该GET；手动刷新同一GET，读取最新已入库记录，不能宣称刷新了Runtime工作区。关闭、选人、身份代际变化会取消自身请求并隔离迟到响应；不取消Runtime业务。合法空本领覆盖旧摘要，但不写改派单名册对象。
- ≤720px采用名册→详情层级，返回保留筛选/滚动；同ID重新点选不取消选择。手机详情全宽无内缩卡片，正文16px、头像68px固定且复用缩略图；刷新显示真实读取HH:mm及只读说明。>720px独立分栏滚动；详情内容滚动与底部动作是同级区域，单密议朱红通栏，双动作点将主操作／密议中性次操作，保留原资格及busy控制。关闭为44px点击区的SVG叉号，选择器限定Agent浮层，不影响其他面板。没有全局换肤或派单算法改动。

完整合同见 `specs/juyiting-agent-skill-display/design.md`；当前发布、真实验证及边界见同目录`release-1.16.9.md`、`handoff.md`、`evidence/visual-fix-1.16.9/online/`；1.16.8记录保留原事实。组件早期合成数据截图不是线上证据；95跳过/2 pending与继承84删例按发布记录保留。两条Flow原CI-only配置均已恢复，develop不自动部署。其余模块仍沿原基线。

## Agent断连与健康观察（2026-10-21局部核验）

核验范围：本机unified Runtime源码`134773544c44284064cd8668f501e6de263a7f4f`、制品`runtime-health-1.2.1`及主机`ops/health`巡检。其余功能沿用各自旧基线；远端Runtime未因此升级。

- systemd active不等于可用：必须核对当前MainPID、连接、注册、执行就绪和有效presence回执。本机Runtime每个心跳周期原子写`/home/isp/state/cyf-agent-runtime-v1/unified/host/runtime-health.json`（0600）；监控核验快照和回执均不超过3个配置周期。当前30秒心跳，监控每分钟运行，连续3次失败按既有策略告警。时效用于观察，不中断业务流、不授予身份或重放任务。
- 暂态网络故障（含Undici连接/请求头/响应体超时）和既有可重试HTTP错误沿用指数退避，间隔上限60秒；鉴权撤销、TLS、协议或未知永久错误保留隔离并记录脱敏分类/错误码。隔离必须先修复原因再受控恢复，不靠修改心跳时间或重新登记掩盖问题。
- 主机巡检只覆盖本机已挂载Agent，不代表远端候选全部在线。Agent异常只告警，不自动重启共享Runtime；API沿用可信恢复carrier/生命周期锁/次数预算。carrier的`--check`须在预留次数前校验canonical精确摘要，升级canonical后需审阅并同步固定摘要，禁止自动信任新字节。
- API除安装身份/端口/health外观察当前PID日志末1MiB的OOM/Metaspace错误；历史PID不影响新进程。此检查只告警，不替代类加载/内存根因诊断，也不因这一信号强制重启。
- 本轮在线验证：三个本机静态通道注册和回执健康；实际任务493吴用、林冲可选，未点击承办、未调用模型。远端和历史离线主体不计入本机成功。证据及未闭环项见`docs/implementation/handoffs/REQUIREMENT-EXECUTION-20261016.md`的本轮收口，不以此重标其他任务完成。

### Runtime固定目录与版本查询（2026-10-23本机迁移核验）

- 现用实体程序为 `/home/isp/apps/cyf-agent-runtime-v1/app/`，仅保留一套程序；旧版本目录和`current`链接已退役。历史程序在 `/home/isp/baks/cyf-agent-runtime-v1/20261023-fixed-dir/`，压缩归档均经完整性测试与全量compare。版本号、commit/tree、依赖锁和制品摘要仍保留，不因目录固定取消版本追溯。统一规则见根`AGENTS.md`对应节。
- 本机实际仍运行Runtime **1.2.6**，源码 `7dd120f5d3a61559ebf4347aa63b638f7e6a4153` / tree `a1ad4c9980b962865f2fe50f70e48171549d30df`，仅4个Python venv生成文件的安装路径重定位；应用代码、Node及依赖未更换。新制品清单与来源/转换记录以主机 `release-records/current.json`、`current.manifest.json` 和实际systemd/PID为准；历史 `1.2.6.json` 保留原发布事实，不当作现用路径。
- 安装入口、模板与重定位工具已合入isp-install develop `297272f5e7af49c6bda703b37f0fc8a6a830a4a7`；源码候选1.2.7未部署。原共享源码checkout未切换；适配源码在独立worktree `/home/isp/wsps/chcbz/isp-install-worktrees/runtime-fixed-dir-20261023`，操作以固定源码的self-host指南§2.1/§7.1为准。
- 迁移前完整停写备份含配置、身份、完整HOME/SQLite、static/managed及inbox/outbox；现行配置、manifest、安装授权摘要及原4份RECOVERY_REQUIRED记录核对未变，未重新enroll、清队列或调用付费模型。静态Agent的apps内manifest/runtime-state未迁移，仅旧程序归档；历史吴用嵌套安装内未启用的manifest和空状态目录完整归档，非现行身份。
- 本次停止主进程09:10:26，完整备份/全量比对完成09:57:49，新主进程09:58:15启动；压缩与校验耗时较长，是本次实际成本，不作为常规维护耗时承诺。随后遇并行API启动修复导致10018拒连，未接管或重启API；后端恢复后Runtime原生自动重连，10:31:19确认三个静态通道的新PID注册、ready及新鲜回执。此为当次核验，不是持续健康或全部技能/业务验收承诺；未重跑业务模型。
- 恢复不得直接从备份目录启动、改链接假装回退或用旧状态覆盖新业务事实。完整映射/摘要/恢复和未优化的备份耗时边界见 `docs/implementation/handoffs/RUNTIME-FIXED-DIR-20261023.md` 及私有归档 `RECOVERY.md`。
