# MMD discussion/inspect closure — exact source facts

Date: 2026-10-01. This is read-only L0 contract preparation, not implementation, deployment, Provider acceptance, or permission to spend.

## Clean component baselines

| Component | Absolute worktree | Commit | Tree | Read-only status |
|---|---|---|---|---|
| Client | `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-fusion-main-20261001` | `71b26ce69d25a59f223499854b692e597b57d911` | `9675a2d85bf08a8e1af45d7c8e76106352db55a3` | clean |
| API | `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-fusion-main-20261001` | `8121e8d89ad0be13ddb79012b61955bac5ae8caa` | `e106bfa99b78c97ac2e6a765a7032a1db20dc9bf` | clean |
| Web | `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/web-fusion-main-20261001` | `8b8c951d4902a5927c85a43a3fcede525154509b` | `386d1e002c7fe53c6c9b992d3d669b50e8ea70fe` | clean |
| SDD | `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/sdd` | `357ddc0b03320c97eaf65c5bd29266e5163ad482` | `9481c21402db8c03f84cbe1a8fa2a6113df7fc0a` | foreign untracked fixture files observed and not touched |

## Design inputs actually read

| Document | SHA-256 | Load-bearing lines |
|---|---|---|
| `long-term-followup-authority-design-20261001.md` | `a747e96f4335c439ebfe8890060400c6aa6d9cd1589d9c8a6947fdef71176800` | 24–57 kinds/modes/sources; 59–79 per-intent authority; 89–103 recovery/Web; 117–123 regressions/incompleteness |
| `fusion-detailed-design-v2.md` | `f790ac27b27d12f3d7a8443d3e849b97222ef0b5b9c9de3aa6d6eb04d0149d59` | 8–19 invariants; 21–50 routing and no mandatory LLM preflight |
| `controlled-image-followup-owner-contract-v1.md` | `bcd607f6ccc2396b04371103b7da1930b58295ccb5735c44346c0227020da562` | frozen EXECUTE owner contract; not DISCUSSION/clarification proof |
| `controlled-image-followup-owner-contract-v1.json` | `7a6f91f783bf2dd9d5b5963b859ba0bc4482ef86b566898c3d1a376b4e1a8b17` | machine fixture |
| `controlled-image-followup-owner-context-v1.1.md` | `27491b37b23615958dd90baff1caee61e32e979ea479ae7fa57bc16281a7b602` | read-only current context; not schema-3 intent |
| `controlled-image-followup-owner-context-v1.1.json` | `ef46a9457bc2f3fb8a06bb1ce87c0e2243a218d5f10460301daf499c3b615b21` | machine fixture |
| `multiround-followup-design-notes-v1.md` | `c036c0b6d155b47b768dbbd7ab59be44edc614293b215bff82d8f6a5c0097bc5` | 5–21 gap map; 42–75 causality, WAITING_USER, recovery |

## Client facts

| Source (SHA-256) | Exact lines / symbol | Verified fact |
|---|---|---|
| `conf/codex-ws-agent/codex-profiles.conf` (`597f1b19fbb57253015160556669a3689539dd82b0eac33f696b5f06148a77ea`) | 13–16, 38–44 | Shipped example defaults have fast CHAT/app-server off. No deployed CHAT/INSPECT proof. |
| `agent-client.mjs` (`29734096c1dd2b1f65d589c3372e8d311affd510d6c703389204fbd347623940`) | 557–610 `normalizeProfile` | CHAT readiness is explicit profile configuration, not persona/routing/skill inference. |
| same | 3654–3704 | Only exact fast + app-server + read-only + read-only-constrained advertises CHAT. `strictNoToolsVerified=false`; INSPECT/EXECUTE are disabled. |
| same | 3716–3725 | Runtime CHAT, controlled v2, disabled v3 and credential binding are separate declarations. |
| same | 4137–4197 `runFastChat` | Durable CHAT uses Context Envelope and returns text/deltas. It emits no typed planning/clarification result. |
| same | 4220–4222 | `runReadOnlyInspection` always throws `INSPECT_NOT_ENABLED`. |
| same | 4868–4884 | Managed profiles inherit workspace-file/native switches but explicitly clear controlled-image HTTP config; this function itself adds no CHAT readiness. |
| `managed-host.mjs` (`f7b153145c5b522bd85c5d2cc49e3b8fda2bf4efc7d7dc6da429d665a531e8db`) | 216–230, 369–392 | 山寨安顿 profiles have owner/generation/runtime fences and separate home/workdir. Managed readiness is not INSPECT/Provider readiness. |
| `app-server-adapter.mjs` (`f11a31b90bda33a3f2c48d469bc954824be9473945b024bc3123dd1d8769ee9c`) | 366–420 | App-server starts with approval never, read-only sandbox, network false. Approval never is not strict no-tools proof. |
| same | 483–508 | Text/deltas/final are handled. User-input/tool RPCs are denied; clarification carries only method identity and is not wired by `runFastChat`. No durable typed question/proposal exists. |
| `chat-runtime.mjs` (`9fbb80ac8324ea38a42e81abf96991d1a666fcca53bb351571a58043d37e0e9e`) | 111–145 | Context hash/facts validate. Attachments/inputRefs/files are copied as untrusted data, not byte-materialized. |
| `conversation-native.mjs` (`3b37a364cf16aac6bbe9ac388f4a9894787e30dba8850eb2331187546b4d18db`) | 99–198 | Real content read/materialization is execution-lane only. |
| `controlled-image-bounty-v3-capability.mjs` (`0d1890efdd680bd905f1bf6cd6254686821214d2091fd3c326d951f20d3e4079`) | 1–16 | Source-aware v3 declares `enabled:false`, `operations:[]`. |
| `conversation-reference-inputs-v3.mjs` (`c6d47e0c2dd6356ce761e27cbd4534047187d2016e3d33745eed44c40bf65a48`) | 38–67, 107–149 | GENERATE uses task-linked versions; EDIT uses exactly one current-conversation asset. |
| `conversation-controlled-image-v3.mjs` (`3a1f30e063ef15e854623ae66334c7860fd146040078972306d5360482f0e2cd`) | 46–61, 153–219 | V3 command/START bind operation, source digest, consent/provider tuple and lease. It is not an INSPECT shortcut. |

### Dual reception conclusion

- 自家接应 is a locally installed/configured profile (`PersonaCatalogPanel.vue:180–237`; `useHallData.js:285–300`). Its actual capabilities are exactly what that profile registers.
- 山寨安顿 is a managed owner/generation-scoped engine/profile (`managed-host.mjs:216–230,369–392`) with separate home/workdir/readiness.
- Neither label implies CHAT, INSPECT, Provider credentials or controlled v3 readiness. Each runtime instance must declare and satisfy capability independently. Current immutable capability rejects INSPECT.

## API facts

| Source (SHA-256) | Exact lines / symbol | Verified fact |
|---|---|---|
| `ChatBountyInteractionController.java` (`266e96af4389673256b59d2abe95a5d57911594c842ebd50a61c9b7d1e3414fb`) | 42–97 | Only schema 2. Discussion rejects refs/reply/continuation. Action kind directly maps to operation; no schema-3 kinds/modes/pending question. |
| `ChatBountyDiscussionAdmissionService.java` (`52f6012ff96f0f35a39a23ec09d3e6db5f9d8e6c6a9a662f78c03163b19c6c45`) | 49–114 | Locks task/binding/conversation, fixes one target, admits durable CHAT with no attachments/hint and no execution effects. Reusable for DISCUSSION/NONE. |
| `ChatBountyInteractionAdmissionService.java` (`10d585170bf78a3b86fa994fbbd95e3e54eb8738f3bb569feb3765c17140544e`) | 66–94 | Existing action admission rejects all refs and reply/continuation. |
| same | 95–190 | Persists PLANNING request/step and EXECUTE link. No pending clarification or typed planner outcome. |
| `ChatDeliberationService.java` (`d7883c4968e105af2e56549510efe4f783247beb661746d0c5eac17dd664fba5`) | 745–774 | Legacy refs are two-field conversation/task/message IDs, not workspace/asset source union. |
| same | 800–858 | Reconstructs bounded history/task facts/availableRefs and always empty materializedRefs. No byte inspection. |
| same | 1044–1060 | Available refs/catalog can be metadata-projected. |
| same | 1235–1270 | Request GET rebuilds request/turn/step/execution, but no kind/mode/pendingQuestion/reply/parent/proposal/resume fields. |
| `ChatDeliberationOutboxRelay.java` (`f5312bff00b835b3c3d4c22d62b828951398490cd198c32c9ec3d528eabb6f15`) | 163–177 | INSPECT fails without materialized input; EXECUTE via chat forbidden. |
| same | 207–246 | Hosted dispatch negotiates exact target runtime capability. Labels cannot override disabled/unsupported. |
| same | 350–390 | Built-in CHAT may call its chat model and treats availableRefs as metadata only; not fixed-manifest INSPECT. |
| `AgentRuntimeCapabilities.java` | 57–112, 165–203 | Exact immutable Client capability is enforced; INSPECT stays unsupported/disabled and chat EXECUTE unavailable. |
| `ChatController.java` (`3ae985cf8c340d1065272e92777a98a2ae347ba6f608fac78305e2726cfe6fed`) | 502–518 | Capabilities list inspect vocabulary but say target support is not implied and materialized refs are required. |
| same | 521–562 | Existing GETs are request/turn plus cancel; no baseline interactions/request or context endpoint. |
| `chat-deliberation-schema.sql` (`ff5f6b22ab5fc0e97afb3a39d9834124abc923b010e444a8228181c44d10bb3c`) | 2–181 | Durable snapshot/request/turn/outbox/event/step/execution-link are reusable. No pending clarification/proposal/causality row. |

## Web facts

| Source (SHA-256) | Exact lines / symbol | Verified fact |
|---|---|---|
| `useHallConversation.js` (`bd140d7085b785a0ea50907c3eb0b9c8a2e7301873b59bffa5ccda8449510d42`) | 120–134 | Refs reduce to `{type,id}` metadata. |
| same | 1165–1261 | Ordinary send infers inspect from non-empty refs and posts legacy `/chat/stream`; no actual frozen source/byte authority. |
| same | 1367–1386 | Sends are blocked while awaiting/streaming, so future WAITING_USER cannot reply. |
| `hallDeliberationState.js` (`9ca1a2b020fe7db9c3f018fae0d5916a8541993c85c0be68189f32c51c9457ee`) | 3–16, 113–116 | WAITING_USER has no replyable special case and remains busy. |
| `HallChatComposer.vue` (`a79962979cd42732325eaad7c525e54c109f365a7f7bcd9048bf8dcdc08391d8`) | 87–116 | Composer disables text/send during awaiting; no question/reply context. |
| `hallMultimediaDeliberationUi.js` (`1ad3074d2ab097fbd787940e93f42fc463f6c05d83ece56311f0952f23b61d1b`) | 26–52 | UI recognizes only v2 EXECUTE/INSPECT steps, not typed discussion/proposal/clarification. |
| `BountyExecutionOutputs.vue` (`689807ce6427b4c9a37f0f496f2b19f9a5e4d991a6ca289cf87c5607824a9e53`) | 193–223 | Output EDIT directly posts rejected schema 2 browser tuple/continuation; no authoritative source/resume chain. |
| `useHallChatContext.js` (`8ea76457cc8b0554e91bb00767b5766e32e5045c605b4dc64e8f6bf951564f2f`) | 51–97 | Existing conversation/task/target UI snapshot is reusable; server remains authoritative. |
| `PersonaCatalogPanel.vue` (`96dc9ad67cbdbda133a6882019a6b86afa412637ed84a2197155848f3b5a7134`) | 114–129, 180–237 | Separate server/local choices are UI facts, not equal capabilities. |

## Facts versus inference

**Verified reusable:** durable CHAT, bounded context reconstruction, event/readback, metadata-only available refs, strict capability negotiation, disabled source-aware image v3.

**Verified missing:** real INSPECT adapter/capability, pending clarification persistence, typed planning/proposal, schema-3 kind/referenceMode/reply/resume, WAITING_USER reply UX and unified follow-up recovery.

**Inference for contract freeze:** existing request/turn/event/context substrate can host additive closure without a second conversation system, but new durable rows/projections and exact capability are required. No concurrent API Owner half-finished branch or later commit is counted as implemented fact.
