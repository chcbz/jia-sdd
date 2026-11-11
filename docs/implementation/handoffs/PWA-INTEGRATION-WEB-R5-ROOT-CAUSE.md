# PWA-INTEGRATION-WEB-RC R5 review root-cause matrix

Date: 2026-08-29 CST

Exact rejected candidate: `29d4e0620b453196c266ce6725da37995bd25845` / tree `7f02e7414e7daf3a541790ad549abe46f403e29a`.
Authoritative verdict: REJECT P0/P1/P2=`0/1/0`.

The R5 SSE recovery/backoff finding is closed. R6 is limited to credentialed WebSocket close cleanup.

| Path | R5 behavior | Root cause | Bounded R6 behavior | Required proof |
|---|---|---|---|---|
| Abort during `CLOSING` | Cached `closePromise` rejects; `terminateCalls=0`; socket may remain `CLOSING` | Abort settles the one-shot promise before enforcing terminal socket cleanup | Abort must attempt idempotent `terminate`, then settle only after a bounded CLOSED observation or a fail-closed terminal cleanup outcome | Abort during close: close once, terminate once, no tracked live socket/process handle |
| Close error during `CLOSING` | Error rejects the cached promise and prevents later cleanup from making progress | Error and timeout paths have different cleanup guarantees | Error path uses the same idempotent forced-termination state machine as timeout | Error during close: terminate once; repeated cleanup is idempotent |
| Timeout / terminate throw | Timeout calls terminate, but throw/late close behavior is not comprehensively proven | Cleanup result and socket state are not represented independently from the cached promise | Record cleanup state separately; every caller joins one bounded operation; a terminate throw remains fail-closed and cannot untrack a live socket | timeout, terminate-throw, late-close, repeated cleanup and already-CLOSED tests |
| Close event state | Close event is treated as success without explicit CLOSED proof | Event delivery and readyState terminality are assumed equivalent | Require `readyState === CLOSED` before successful untrack; otherwise force termination/fail closed | Synthetic close event while non-CLOSED cannot succeed |

Do not modify the accepted SSE/backoff implementation except for a directly necessary compatibility fix. Run the exact WebSocket regression matrix, existing TaskWorkspace tests, and production build; no Gradle or production action. Fresh independent review is mandatory.
