# OPS-RESOURCE-TELEMETRY R3 review root-cause matrix

Main-controller approved remediation scope, 2026-08-29.

Rejected exact candidate: `ab585b20fbf3f4c74d43e999e2cc49741afdaff5` / tree `eb0d6330dc3aa2fcbf3f49acf1db5218a9b86ebb`.

Authoritative review: REJECT, P0/P1/P2 = 0/3/2.

| Finding | Root cause | Required R4 closure |
|---|---|---|
| Repository file can self-attest remediation approval | Approval source and matrix are both Writer-editable | Bind authorization to a controller-owned, physical, non-symlink external approval record with exact task, blocked attempt digest, matrix SHA, candidate base SHA/tree, intended agent/profile, expiry/one-shot nonce; fail closed on ownership/mode/content mismatch and consume atomically |
| `transition` can erase first failure or self-promote | No owner-aware legal transition graph or terminal authority separation | Add explicit allowed transitions; require exact current owner for active transitions; implementation/verifier cannot enter terminal accepted/done; reviewer cannot repair; blocker clearing only on authorized remediation or controller terminal promotion with matching review evidence |
| Telemetry docs claim kinds CLI cannot represent | Scope changed in prose without matching implementation | Add and test `npm_full_test` and `heavy_disk`, or narrow every contract consistently; no unsupported broad claim |
| M2 docs conflict | Current-state sections were copied without convergence | Make M2/README state descriptions consistent |
| Candidate self-description stale | Tests validate shape but not checkout/task binding | Add truthful non-circular candidate/ledger binding contract and tests; do not claim a commit can contain its own final SHA |

R4 must add adversarial tests reproducing forged approval and first-failure laundering from the review. No Gradle, production, process control, or unrelated task changes.
