# MMD-U2 INSPECT 接线准备（只读，非冻结/非实现）

**依据版本**：API `a21378413366cfe96962ff49adf6b43d8d883d45`；Client `607d25145efe3d13f996e5fbb5e33a01d7bf2195`；Web `ebb664fc8a443845577f356d0823bd6368634dfa`（指定 worktree）。不接受 proposal 未实证的 `limitSet` 阈值；不改 v1。

## 1. 既有 typed/store 与候选 sibling

| 层 | 已有精确事实/可复用 | 边界 |
|---|---|---|
| API typed | `ChatTypedDiscussionAdmissionService.admit` 在单事务、task-root 锁内验证 owner/client/conversation/generation/assignment/唯一 target，持久 `sourceCatalogJson`（55–113）。`ContextService.resolve` 以 exact scope 查 ACTIVE+REFERENCE workspace version 或 conversation asset revision，并排序/哈希 catalog（47–80,97–161）。 | v1 `referenceMode` 固定 `NONE|AVAILABLE`（78–80），Client validator 同样二值（147–156）；不扩展/重释。候选为协商的 versioned `typedInspection` sibling，保持 `typedDeliberation` 字节不变。 |
| API final/store | typed Admission/Outcome/Proposal/Pending 已 exact scope；pending 有 state-version CAS（store 7–45；JDBC 12–18,66–78），typed final 在锁内以 finalDigest 冲突保护（TypedService 32–57）。 | 这些可优先承载 inspection request/inbox/binding/typed pending 及其附加的 versioned authorized snapshot；`sourceCatalogJson` 本身不是读授权。只有现有 durable record 无法同时表达 immutable identity、幂等恢复、撤权重核而又不改变 v1 时，才需单独 persistence model；本文不预定新表或第二状态机。 |
| Client | durable inbox、binding store、`buildThreadKey`、unknown-turn read/reconcile 可复用：key 可绑定 mode/cwd/engine/tool/model/generation（chat-runtime 619–661），adapter 会标记 unknown recovery（439–470）。 | Fast CHAT 固定 `mode:'CHAT'`、empty cwd、JSON input（agent-client 4193–4217）；INSPECT 不可共用 thread key/cwd/fallback。候选 key 另绑定 manifest digest、authorization/request identity、profile。 |
| 协商 | v1 runtime parser 强制 INSPECT `supported/enabled/strict=false`（AgentRuntimeCapabilities 183–195）；Client 同广告不可用 profile（agent-client 3677–3705）；typed declaration 固定 v1 modes/engine/tool policy（12–60）。 | 新 declaration/profile 必为 sibling；不得把 enabled 或 `read-only-constrained` 当 strict no-tools 证明。 |

## 2. 授权、身份、dispatch 与读取

**可复用的权威输入。** admission 已验证认证 human tenant/owner/client、锁定 task binding/assignment、锁定 conversation generation、唯一 target/root agent（53–78）；session registry 要求 exact authenticated scope+agent、current binding、唯一 READY session（25–60）；socket delivery 再核验 session tenant/owner/client/agent 并协商 route capability（WebSocket 2381–2443）。它们可供 INSPECT issuance/dispatch 使用；冻结时才决定 authorized snapshot 的字段与所在 durable record。至少应可关联 purpose=INSPECT、request/dispatch/message、target agent/profile、generation、manifest revisions/digest，且恢复时仍可判定。

**已有下载端点均非 machine INSPECT grant。** workspace content `GET /agent/personal-workspace/files/{fileId}/versions/{version}/content` 是 browser/JWT owner scope（PersonalWorkspaceController 34,93–96,178–183）；conversation asset content 也是 human tenant-owner scope（ChatConversationAssetController 51–103）；output bytes 是 request/step/execution owner-fenced chain（ChatBountyMediaController 97–164），只可帮助 provenance 复核。尚未找到 runtime-agent INSPECT input read endpoint。`WorkspaceFileBridge` 的 exact-origin/header/redirect/length/hash/`O_NOFOLLOW`/0400/no-replace primitives（469–560）可候选复用；其 run-scoped **EXECUTE** `/start` 路径（650–686）不可借作读权限。

因此未来 server contract 需要 inspection-purpose authenticated GET 或等价 capability：读取前在同一授权边界核对 immutable locator、current binding/assignment/generation、target/profile 与 revocation，再开始 streaming。不能以 prompt、cwd、filename、browser endpoint、EXECUTE grant 或 catalog hash 放行。

## 3. manifest、撤权、事务边界

catalog 已有 selector/MIME/hash/byteLength/parent request-step，`sourceRefId` hash 覆盖 scope+catalog item（ContextService 144–161）；admission requestDigest 含 catalog（88–112,156–168），final 重比 catalog/sourceRefId 与 snapshot facts（TypedService 139–155）。这是 manifest canonicalization/provenance 的可复用基础，不等同 receipt 或读授权。

现 catalog SQL 只在 admission 验 ACTIVE/reference、conversation not-deleted/generation、revision（ContextService 97–141）；未见 authorization id、read locator、manifest version/digest 或 GET 时撤权重核。冻结后，issuer transaction 应原子锁/验 binding+conversation+assignment，构造排序/hash manifest，并将 immutable source revisions 与 authorized snapshot 附着到可恢复的 existing durable request/admission/binding（若该模型足够）；再建 dispatch/outbox。读取端必须在 streaming 前重读/锁定 current authority，拒绝 revoked、target/profile changed、generation/assignment/source mismatch。不能只凭 sourceCatalog hash。

generic INSPECT 现仅要求 `authorizedContext.materializedRefs` 非空才 relay（DeliberationService 824–852；Relay 163–177,455–462），未验证 manifest bytes/authorization；它不是 ready source authority。

## 4. 最小候选写集与 Web 实证

| package | 最小未来写集（候选，非授权） | 实际依赖/缺口 |
|---|---|---|
| API | versioned inspection declaration/parser、issuer/read recheck、purpose-scoped machine GET、dispatch fact、focused tests；只为共用 verifier 触及 typed context/admission，不变 v1 wire。 | workspace/asset query、runtime session identity、outbox 已在上列；是否需 migration/独立 store 取决于冻结字段能否附着既有 durable records。 |
| Client | inspection declaration/parser、与现有 inbox/binding/pending 原语兼容的 durable receipt/materializer、distinct key/cwd、safe materializer subset、adapter mapping/tests。 | adapter 当前只送 `threadId/clientUserMessageId/input/cwd/model/effort/approval/sandbox/outputSchema`（442）；未接 `localImage`/`localAudio`/roots/permissions/fallback。 |
| Web | 指定 Web 中 `BountyDiscussionPanel` 已呈 typed status/recovery/followup 并向 `ChatPanel` 转交 typed props/events（10–68）；`ChatPanel` 加载 workspace/task/conversation links（303–324），bounty 仅 ACTIVE `REFERENCE` 进入 `TASK_LINKED_WORKSPACE_VERSION` selector（320–330），且只在 typed bounty send 传 selectors（189–208）。 | 这些可复用作 metadata/source selection，**不是** INSPECT manifest、authority 或 readiness UI；`HallChatComposer` 只是目标 chips/ordinary send（155–189,232–235）。服务器 receipt/state/rejection 与 media/profile contract 冻结后，Web 才候选显示其 authoritative 结果，不可由所选资料推导授权。typed validator 仅两 selector kinds（hallTypedDeliberation 13–40）；adapter 明确只管 frozen discussion/read、无 model/grant/legacy fallback（useHallTypedDeliberation 51–53），并以原键 GET-only recovery（135–192）。proposal 也要求 preview/explicit consent（BountyTypedOutcomeCard 11–15）。 |

**0.159.2 primary schema（仅离线公开 schema 生成）**：manifest 绑定 binary SHA-256 `1748767b…a4a92e`、bundle `7243ba…508c5`。`TurnStartParams` 的 UserInput 有 `text`、`localImage:{path}`、`localAudio:{path}`（544–695），无 generic local-file；`permissions` 是 named profile 且与 `sandboxPolicy` 互斥（875–922）；`runtimeWorkspaceRoots` 仅 sticky roots 描述，非 isolation proof（903–911）。`ThreadStartParams` 有 `allowProviderModelFallback:boolean`、dynamicTools（305–370）。这只证实字段：不证实 no-tools/受限工具、隔离、图像/音频理解或 INSPECT readiness。API metadata 仍仅 text/image/audio/file（ContextService 162）；故 text/image/audio/file 四类的 carrier、model acceptance、no-tool 或受限-tool policy 都尚缺实证，`application/octet-stream`/未测 MIME 不应 dispatch。

## 下一可执行源码包

Main 冻结 sibling wire、authorized snapshot/receipt 字段与存放边界、GET/revocation transaction、carrier/profile/tool/MIME declaration 后：先 **API authority + machine GET + tests**，再 **Client receipt/materializer + adapter mapping + tests**；Web 在 server-ready receipt contract 后跟进。保持单会话、typed atomic final、v1 NONE/AVAILABLE、原键恢复。
