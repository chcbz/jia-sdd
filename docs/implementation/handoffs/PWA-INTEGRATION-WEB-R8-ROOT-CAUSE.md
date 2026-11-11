# PWA-INTEGRATION-WEB R8 Review Root Cause

Date: 2026-08-29 CST

Exact candidate:

- commit: `f55a31a6d58840ef44cbe4d7e25c63dc7d8fa14a`
- tree: `1215c6b3afba15c24e6249e50298e6c826baaffc`
- reviewer: `01a04c2a-e365-7c10-b919-2442af3fea88`
- verdict: REJECT, P0/P1/P2=`0/2/0`

## Root-cause matrix

| Finding | Symptom | Root cause | Bounded R9 remediation | Required proof |
|---|---|---|---|---|
| Multiple reentrant cleanup mutual-await | Two cleanups each awaiting `guard.dispose()` wait on the other cleanup task and never converge. | Reentrancy exclusion is task-local; each nested dispose excludes only its own pending task instead of using one shared disposal epoch/context. | Replace per-cleanup mutual waiting with a guard-scoped active disposal epoch/ownership contract: a cleanup reentering the same active dispose must not start or await another disposal fan-out; the outer dispose remains responsible for all cleanup tasks. | Two or more simultaneous reentrant cleanups complete exactly once; outer dispose waits for all; no pending/owner/registry residue; bounded timeout probe. |
| Stale AsyncLocalStorage context fail-open | A detached callback inheriting a completed cleanup context can call dispose and exclude the failed cleanup/error, resolving while an external dispose rejects. | ALS identity is trusted without proving the corresponding cleanup execution token is still active in the current disposal epoch. | Remove ALS dependence if possible, or bind reentrancy to an unforgeable active token/epoch that is revoked in `finally`; stale/detached descendants must take the ordinary external fail-closed path. | Cleanup schedules late callback then fails; late dispose must reject identically to external dispose and must not skip retry/error accounting. |

## Constraints

- Preserve R8 successful terminal untrack and bounded no-late-close behavior.
- Preserve SSE/backoff/default-off byte-exact.
- Writes remain limited to `tests/juyiting-preflight-safety.mjs` and direct cleanup tests.
- Reuse unchanged exact-tree build evidence only if no build-affecting source outside test safety module changes; otherwise run one fresh production build after H06 releases heavy-disk resources.
- Fresh independent Review is mandatory; no Chromium, credentialed network, or production action.
