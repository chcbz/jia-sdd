# W06 bounded completion settlement implementation

## Source handoff and ownership

Source implementation can start from clean W05 `fbee6395611837f3f6a08f4b32d762fa65c96037` / tree `dcef936f4c8a0d5350a06e511fd94ec2ecc77850` (W04 R3 source-accepted ancestry). W05 full independent review/runtime acceptance remains a **promotion/release dependency**, not a reason to defer contract-frozen W06 source. Original W05 critical owner takes a separate `eco-v0-bounty-settlement` worktree. Original W04/W05 trees immutable.

Own new/completed funding settlement controller/DTO/service/mapper/DDL and economy bounty-ledger capture support, plus matching tests. Preserve W04 create/cancel and W05 quote/claim semantics. W09 owns separate skill/capability/roster/result paths; no AgentService/roster or skill entitlement-interface edits. No rental/runner/Web changes. Report concrete path conflicts before edits.

## Required V0 behavior

- Authenticated `GET /agent/tasks/{taskId}/settlement`, `POST /agent/tasks/{taskId}/funding/complete` with canonical decimal strings `{expectedTaskVersion,actualComputeMicro}` and canonical UUID Idempotency-Key. Existing pre-start cancel endpoint stays valid. Exact `sub` monetary actor + tenant/client, no fallback identity. Scope/owner/task state enforced under root lock.
- Completion endpoint is explicitly preview orchestration, never an assertion of actual provider token billing. Actual compute is nonnegative and cannot exceed the accepted quote's frozen compute limit or gross budget; reject excess rather than debit more or yield negative payout. Fees and recipient come only from frozen server quote/claim, never caller input.
- Frozen GROSS_INCLUSIVE success: `gross = actualCompute + platformFee + agentPayout`, refund zero. Pre-start cancel: existing full remaining escrow refund, no platform fee. All integers overflow-safe, no double/floating point. No unapproved partial-failure settlement, top-up, new provider/KMS framework.
- Atomic real transaction captures remaining escrow into model/platform/explicit claimed Agent principals; task/funding versions, completed receipt, domain event and ledger commit together. Same exact actor/key/body replays immutable receipt; conflict or stale version writes nothing. Completion/cancel/result interleavings cannot double-spend. Require valid accepted claim and supported task state; arbitrary legacy task mutations cannot bypass monetary settlement.
- GET distinguishes held/settled/refunded and returns canonical scoped audit projection. Never fabricate a settlement before ledger success; unknown transport outcome recovers by same-key replay/readback.
- Keep default-off and existing guard chain. Durable downstream callbacks only after outer transaction commits.

## Focused source proofs

Real ledger/task/event collaborators: successful conservation including zero-compute edge, insufficient/oversized/negative/overflow/noncanonical input, cross-scope/nonowner/wrong state, stale CAS, exactly-once replay and conflicting body, concurrent completion/cancel, outer rollback of ledger/task/receipt/event, immutable readback. Include additive SQL/initializer exactness and nullable CHECK predicates where schema changes. Use real transaction tests, not mock-only success.

Source-only phase: static checks then clean parent/commit/tree, changed-file manifest and fixture SHA256; independent review then admitted verifier. Every Gradle invocation via orchestrator. Do not update root ledger or run DB/build/services as source writer.

## 2026-09-06 inherited W05 correction scope

W05 first full independent review rejected `fbee6395` with 0/3/1; see `ECO-V0-W05-R3-ROOT-CAUSE.md`. To avoid interrupting/restarting the original owner's W06 source work or claiming two tasks for one Agent, this **combined W06-owned slice** also closes the four precisely bounded W05 constructor/runtime-binding/catalog/replay findings in the settlement worktree. Original W05 tree remains frozen; W05 waits for the combined corrected handoff and retains separate review/acceptance evidence. Prepared W05 runtime script is not GO on rejected source. No extra scope outside those findings and required settlement/shared-posting support.

Shared posting coordination: W09 leaves `EconomyPostingServiceImpl.java` untouched and requests minimal `CAPTURE_SKILL`/`REFUND_SKILL` support through existing `EconomyEscrowSettlement` with `SKILL_ORDER` and exact reserveTx/version. Capture destination `SYSTEM/SKILL_STORE/SKILL_STORE`, refund original `USER/AVAILABLE`. W06 owns this shared implementation alongside bounty compute/fee/payout support and matching conservation/replay/rollback tests; W09 owns its order/facade transaction. Report a frozen shared-path/interface handoff for byte-exact integration, preserve W02 and rental behavior.
