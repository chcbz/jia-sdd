# PWA-INTEGRATION-WEB-RC R6 review root-cause matrix

Date: 2026-08-29 CST

Exact rejected candidate: `a856cb2e7d63fd6164f43494f6268d8e88edcfef` / tree `0ee40ae6fc7e19fa7ed27eaa829f4dcb2711e47f`.
Authoritative verdict: REJECT P0/P1/P2=`0/1/0`.

| Combined race | R6 behavior | Root cause | Bounded R7 requirement | Required proof |
|---|---|---|---|---|
| Global termination + `terminate()` does not transition readyState + late close | First cleanup marks guard wrapper `invoked=true`, rejects after bounded timeout, clears internal promise; dispose calls the one-shot wrapper and cannot establish a second bounded wait. Socket remains `CLOSING`, no pending cleanup/timer | Guard cleanup wrapper conflates “attempt was invoked” with “resource reached terminal cleanup”; failed cleanup is permanently exhausted | Track terminal cleanup completion separately from in-flight invocation. Concurrent callers share one in-flight operation; a failed/nonterminal attempt remains retryable by dispose/global termination until bounded terminal policy is reached. Never untrack/succeed while socket non-CLOSED | Deterministic cross-race: first check fails, dispose starts/joins a second bounded cleanup, late close converges to CLOSED; no live handle/pending timer; concurrent dispose is idempotent |
| Permanent non-CLOSED handle | One terminate attempt can return without changing state | Exactly-once invocation is insufficient for exactly-once terminal cleanup | Define a finite retry/force policy or explicit process-level fail-closed outcome that cannot report cleanup complete while live handle remains | terminate no-op, terminate throw, error/abort, repeated dispose and no-late-close all settle bounded with no false success |

R7 may modify only `tests/juyiting-preflight-safety.mjs`, `tests/juyiting-public-beta-preflight.mjs`, and direct WebSocket cleanup tests. Preserve accepted SSE/backoff code byte-exact, default feature off, and unrelated generated files. Run focused Node/Mocha and production build; no Gradle or production action. Fresh independent review is mandatory.
