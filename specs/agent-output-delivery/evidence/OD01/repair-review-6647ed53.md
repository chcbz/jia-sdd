# OD01 repair re-review — CHANGES_REQUIRED

Candidate: `6647ed53fac06c8c7478cf58579c4eadf6f689d0`. Independent read-only reviewer: `/root/output_design_review`; no files edited and no Gradle command run. Candidate/report correspondence passed for the five latest groups: 271 tests, zero failures/errors/skips. These tests did not cover the remaining promotion defect below.

The original B1 raw-byte preservation, B2 exact receiving-runtime selection and B3 separation of ticket renewal from dispatch freshness are repaired.

## B4 — enriched MQ-shadow wire cannot promote to canary

`AgentCommandTransportWriterImpl.writeHallAuthorized` now persists trusted `outputContext` in the wire. `validatePromotableShadowOutbox` reconstructs `expectedWire` using the context-free codec overload, then compares it to the enriched stored bytes. Valid output-aware shadow commands therefore always fail promotion during canary cutover.

Required bounded repair:

1. Extract and strictly validate the stored context using the canonical codec.
2. Reconstruct expected bytes with that exact context.
3. Preserve the persisted wire and hash during promotion.
4. Verify successful promotion for enriched and legacy context-free shadow commands, including unchanged bytes/hash and existing tamper rejection.

The original API writer owns this repair and affected writer/promotion/transport verification, starting from `6647ed53`. No unrelated batch rerun is required solely for evidence bookkeeping. A new committed candidate must receive independent read-only review before OD01 acceptance or OD02 starts.

## Nonblocking observation

The batch authorization API accepts multiple producers for one CONVERSATION source although current conversation callers use only singleton requests. The reviewer found no demonstrated deadlock under the existing shared-task-root serialization. Restricting that unused batch shape would make the intended scope clearer; this is recorded as a follow-up constraint, not an additional OD01 blocker. Keep conversation callers singleton in subsequent work.
