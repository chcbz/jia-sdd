# JY-HISTORY-DELETE R8 verification root-cause matrix — 2026-09-11

| Attempt | Symptom | Root cause | Scope attribution | Bounded remediation |
|---|---|---|---|---|
| 1 | Combined Agent+Chat invocation ran 1431 Agent tests and failed `C01BTaskEventContractTest` | Gradle task options were effectively bound to the later Chat test task, so the earlier Agent test task ran broadly; its frozen fixture omits pre-existing funding writer classes | Harness scope drift; unrelated to the R8 conversation ACL/relay diff | Split Agent and Chat into separate module-local orchestrator invocations; do not edit the unrelated contract fixture |
| 2 | Chat `compileTestJava` could not resolve three `eq(...)` calls at `AgentWebSocketHandlerTest.java:1251` | The new recipient-isolation test used an unimported Mockito matcher | R8 test-fixture defect; production sources compiled | Replace only those three calls with fully qualified `org.mockito.ArgumentMatchers.eq(...)`, commit a new exact tree, then rerun the same Chat selector |
| 3 | 11 Chat selectors ran; one delete-fence assertion and two strict-Mockito checks failed | The real broker test kept the persistent `isLiveGeneration` mock true after deletion; relay tests retained obsolete `isAgentConnected` snapshot stubs after delivery switched to actual send results | Test fixtures were stale relative to the intended R8 semantics | Make the exact deleted tuple return false and remove obsolete `isAgentConnected` stubs from this relay test class; do not alter production behavior |
| 4 | The full seven-class 86-test regression found seven failures | Two mixed Mockito matcher stubs, one remaining obsolete connection-snapshot stub, missing exact identity/live fixtures, one mismatched recipient id, and one post-delete supplier still modeled the removed in-memory tombstone | Composite test-fixture alignment only; production classes compiled | Apply only the seven enumerated fixture corrections, then rerun the identical 86-test selector and a fresh Agent writable-member selector |

Authorization boundary: remediation is limited to the listed test-fixture alignment. It does not authorize production deployment, API lifecycle changes, push, Provider calls, voice activation, unrelated fixture edits, or broad retries.

## Closure evidence

- Remediation commit: `2ed5da033a7dbd1d2d723a55252a9ea093402a6e`
- Exact tree: `3a41d5dcad5f6a4258a4aa0cc864878e273d5244`
- Seven-class Chat composite: **86 tests, 0 failures, 0 errors, 0 skipped**; evidence key `573969fe418bf810b51d57bc0cecb830fcfabaa91e2f4e44308f9dcc2cc13eec`.
- Forced Agent writable-member ACL rerun: **1 test, 0 failures, 0 errors, 0 skipped**; evidence key `6bc913c9936b1a737254e78d6a721f82ee73f23dc28da8cd6f4af81fd0b07d99`.
- Fresh authoritative review assigned to `01a0909a-df47-7ff3-9701-3a1e7c7a3d82`; merge, push, deployment and runtime changes remain blocked until its verdict.

## Attempt 5 — fresh authoritative review REJECT

- **Exact candidate:** `2ed5da033a7dbd1d2d723a55252a9ea093402a6e` / tree `3a41d5dcad5f6a4258a4aa0cc864878e273d5244`
- **Verdict:** `REJECT`, P0/P1/P2 = `0/2/0`, reviewer `01a0909a-df47-7ff3-9701-3a1e7c7a3d82`.
- **Root cause 1:** `persistedConversationTargetAgentIds()` still rebuilt an empty canonical `target_agent_ids` snapshot from the legacy `target_agent_id`, bypassing the new fail-closed rule.
- **Root cause 2:** final task-conversation delivery validated the sender against current writable membership but broadcast to the historical persisted recipient set without intersecting it with current writable task members.
- **Bounded remediation:** remove the empty-snapshot legacy fallback; for task conversations, intersect final-message recipients with a fresh authoritative writable-member set and fail closed on unavailable/invalid scope; add regressions for empty canonical snapshot plus non-empty legacy target and for a persisted recipient whose task membership is revoked. No broker, migration, relay, or unrelated module changes.
