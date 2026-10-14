# MMD discussion/inspect closure — capability matrix

Date: 2026-10-01. Baselines are the exact commits/trees recorded in `01-exact-source-facts.md`. `Actual` means verified in those sources, not inferred from a branch in progress. This matrix is contract input only.

## End-to-end matrix

| User interaction | Client actual | API actual / reusable | Web actual | Missing closure | Permitted side effects |
|---|---|---|---|---|---|
| `DISCUSSION` + `NONE` | A configured Fast CHAT profile can consume the authoritative Context Envelope and return text/deltas. It cannot return a typed planner outcome. | `ChatBountyDiscussionAdmissionService` already locks current task/binding/conversation and admits durable CHAT. Reusable as the zero-reference core. | Ordinary composer can send text, but uses `/chat/stream`, not strict schema 3. | Strict schema-3 identity/body digest, typed outcome persistence, original-key GET, and one Web follow-up lane. | Durable request/message/turn/outbox/event only. **Zero** execution, operation grant, consent, run, command, START, source-byte read, or Provider call. |
| `DISCUSSION` + `AVAILABLE` | Context can carry metadata as untrusted data; no content is materialized. | Bounded `availableRefs` projection exists, but no schema-3 strict source union/snapshot for this interaction. | Browser refs collapse to `{type,id}` and `inspect` is only a label. | Resolve exact ref identities and ACL server-side, freeze metadata-only snapshot, dispatch catalog only. Non-execution limits come from the eventual inspection capability contract, not image execution’s 16-input bound. | Same as DISCUSSION/NONE plus metadata SELECTs. **Zero bytes read** from referenced content. |
| `DISCUSSION` + `INSPECT` | **Unavailable.** `profiles.INSPECT.supported=false`, `enabled=false`; `runReadOnlyInspection` throws `INSPECT_NOT_ENABLED`. | Relay requires materialized input and capability negotiation, but no actual materializer/runtime capability is available. | UI can label a request inspect but cannot prove a fixed manifest or actual byte-reading target. | Exact source resolver, immutable manifest, source ACL, actual media-capable read-only adapter, truthful capability registration, bounded results, and recovery. | Read-only source materialization and an inspection turn only. **Zero** image execution claim/consent/START/Provider generation. |
| `CLARIFICATION_REPLY` + `NONE` | No typed question/reply protocol; app-server user-input RPC is denied and its method-only clarification event is not wired into `runFastChat`. | No pending-question row, reply CAS, clarification revision, or resume fact. | `WAITING_USER` is treated busy; composer is disabled. | Durable pending question, exact `replyTo`, one-time/open-state CAS, reply message, resume event/projection, and replyable WAITING_USER UX. | Reply/request/step/event writes only. Reply itself creates no paid execution authority. |
| `CLARIFICATION_REPLY` + `AVAILABLE` | Can receive catalog metadata only after API adds the strict snapshot. | Same missing reply state plus metadata-only resolver. | No pending context or strict refs UI. | Combine exact pending-question CAS with exact metadata snapshot. AVAILABLE must not become INSPECT. | Clarification/reply persistence plus metadata SELECTs; zero byte reads and zero execution effects. |
| `CLARIFICATION_REPLY` + `INSPECT` | No real INSPECT capability. | No pending reply or materialized-ref closure. | No explicit per-turn inspect authorization UX. | Both closures are required: exact pending reply and actual fixed-manifest INSPECT. A reply mentioning an attachment is not permission to inspect it unless `referenceMode=INSPECT`. | Read-only inspection only after current ACL/capability checks; no image execution consent is consumed. |
| Natural follow-up: “再鲜艳一点” / “换成黄鹂” | Current CHAT returns only text. It cannot emit a machine-verifiable `EXECUTION_PROPOSAL` or `CLARIFY`. | Existing metadata/producer lineage can identify a candidate current-conversation asset, but no typed proposal or causality persistence exists. | Current ordinary send has no structured outcome UI; output-card EDIT bypasses a unified lane and sends a body the API rejects. | Deterministic metadata resolver where exact, otherwise an optional constrained planner that returns a strict typed result. Persist `ANSWER`, `CLARIFY`, or `EXECUTION_PROPOSAL`; never parse prose as authority. | Proposal/question writes only. No consent, operation grant, execution, START, or outbound Provider request until a distinct authorized EXECUTE flow. |
| Initial explicit `GENERATE_IMAGE` from point-and-start | Client controlled v2 path exists separately; source-aware v3 remains disabled. | Initial point-and-start may execute the exact already-authorized first intent when all facts exist. | Existing initial flow can gather explicit point/start authority. | If required generation facts are missing, create pending clarification **before** RESERVED/START. A reply may resume that same unconsumed initial intent after revalidation; it is not a later follow-up grant. | Exactly the initial intent’s frozen authority. No mandatory CHAT/planner preflight. |
| Later `EXECUTE/GENERATE_IMAGE` | Source-aware v3 command parser/runtime exists but sibling declaration is forced disabled and not production scheduled. | Frozen owner v1 EXECUTE contract supplies preview → new consent/operation grant → admit → execution/run → one START. | Follow-up Web implementation is separate and incomplete as a full product. | Explicit user acceptance of the current proposal/intent and actual v3 runtime readiness. | New intent, new keys, new consent, new operation grant, new run/command, exactly one START. |
| Later `EXECUTE/EDIT_IMAGE` | V3 parser requires exactly one current-conversation asset and binds operation/source digest; still disabled. | Frozen owner v1 resolves producer lineage and per-intent EDIT authority; baseline GENERATE grant alone cannot authorize EDIT. | Current output card does not supply a valid authoritative closure. | Unified follow-up lane and actually enabled EDIT-capable controlled adapter after all runtime gates pass. | Same new-per-intent chain as GENERATE. Original asset remains immutable/readable; new output is a new asset. |

## Typed planning and clarification status

The current source graph **cannot receive or persist a typed planning/clarification result**. `runFastChat` sends text/deltas/final only; the app-server adapter’s user-input request is denied; API final-message handling has no typed outcome field; Web has no pending-question/proposal reducer. A natural-language answer that says “I will edit it” is therefore prose, not a proposal, permission, consent, operation grant, execution, or success fact.

The next contract should allow two producers of the same server-validated typed outcome:

1. **Deterministic API metadata routing**, when operation and exact source are unambiguous (for example, an explicit edit action on one exact output asset).
2. **Optional constrained planner**, only when semantic interpretation is needed. It must return a strict sibling typed event/result. Plain text must never be reparsed as authority.

Neither mechanism is mandatory before every discussion or initial authorized execution.

## Metadata-derived proposal boundary

Metadata can establish scope, conversation generation, task/assignment/target, the exact preceding request/step, the set of current-conversation assets, producer lineage, MIME/hash/length, and which asset the UI explicitly selected. It can therefore make an edit proposal source-exact.

Metadata alone does **not** prove the semantic meaning of arbitrary prose. For “再鲜艳一点”, a deterministic proposal is valid only when the current causal focus resolves to exactly one editable current-conversation image. For “换成黄鹂”, the same source resolution can nominate `EDIT_IMAGE`; a constrained planner or explicit UI action may supply the semantic instruction. If there are zero/multiple plausible assets, multiple pending questions, an unsupported media type, or uncertain operation, the result must be `CLARIFY`, not guessed execution.

## Dual-reception differences

| Property | 自家接应 | 山寨安顿 |
|---|---|---|
| Runtime source | Locally installed/configured profile selected in Web | Managed owner/generation-scoped engine/profile |
| Home/workdir | Local profile’s own configured roots | Separate managed home/workdir and generation fences |
| Readiness meaning | Only its registered exact capability | Only its managed instance’s registered exact capability |
| CHAT | Possible only with exact Fast/app-server/read-only-constrained configuration | Same rule; managed label does not imply it |
| INSPECT | Not implemented in current Client | Not implemented merely by managed hosting |
| Controlled image v3 | Disabled sibling, `operations=[]` | Also not implied by managed hosting |
| Cross-profile reuse | Forbidden: no home, manifest, source, binding, claim, or result sharing by label | Forbidden in the opposite direction as well |

## Capability truth rules

- Routing labels, persona names, UI availability, “read-only” wording, approval mode, or a generic Codex executor are not capability proof.
- `AVAILABLE` means catalog metadata only and must not fetch bytes.
- `INSPECT` requires an actual fixed-manifest content reader, source ACL and truthful immutable capability declaration; it must not be advertised before that combination passes.
- Browser preview/playback proves neither Agent content access nor media understanding.
- Image execution’s 0–16 JPEG/PNG source bound remains execution-specific and must not be copied onto ordinary text/audio/file discussion without an independently frozen reason.
