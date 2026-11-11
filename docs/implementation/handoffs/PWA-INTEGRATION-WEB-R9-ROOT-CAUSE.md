# PWA-INTEGRATION-WEB R9 Review Root Cause

Date: 2026-08-29 CST

Exact candidate:

- commit: `b9c3924df7d2a08dcbd910e9b5dcfcf936ad0a07`
- tree: `2fb45fc96dea41e5a21beeefa0d16cfe6b9079ea`
- reviewer: `01a04c3f-712a-7df3-87eb-40749e3d51ec`
- verdict: REJECT, P0/P1/P2=`0/1/1`

## Root-cause matrix

| Finding | Symptom | Root cause | Bounded R10 remediation | Required proof |
|---|---|---|---|---|
| Same-turn detached microtask fail-open | Cleanup queues a detached microtask, then returns/throws; the microtask inherits an active token and its dispose resolves although the outer/external path rejects. | Token revocation happens in Promise `finally`, after already-queued microtasks can run. ALS context alone cannot distinguish synchronous/awaited reentry from detached descendants scheduled before settlement. | Do not authorize reentry based on token lifetime extending to task settlement. Use a synchronous invocation frame/explicit reentry promise contract that is closed before control returns to the microtask queue, or make nested dispose return the current outer disposal promise without excluding errors/retries. Detached descendants must always join ordinary external accounting. | Same-turn `queueMicrotask` after both cleanup success and failure, with/without sibling failure: late dispose result equals ordinary external fail-closed result; required retry occurs; no error skipped. |
| Focused evidence binding | Reviewer reproduced 13/13 but cache has no accepted focused record/artifact for exact tree. | Writer recorded aggregate Node evidence but not the focused selector as its own exact-tree evidence entry. | Persist focused selector log and evidence key bound to new exact tree/selector/fixture/artifact SHA, in addition to aggregate Node/Mocha evidence. | Cache record exists and recomputes exactly; log reports focused pass/fail/skip counts and clean HEAD/tree. |

## Constraints

- Preserve R9 multi-reentrant convergence and all R8 accepted cleanup behavior.
- Preserve SSE/backoff/default-off and build reuse eligibility.
- Writes only to `tests/juyiting-preflight-safety.mjs` and direct cleanup tests.
- No production build unless build inputs outside this test safety module change; no Chromium/network/production.
- Fresh independent Review required.
