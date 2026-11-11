# PWA-INTEGRATION-WEB-RC R7 review root-cause matrix

Date: 2026-08-29 CST

Exact rejected candidate: `11ce4c76d1673f12af005e83f540410832539bce` / tree `a6bed8e2a1276f2ece28ba07998f54209d9213ae`.
Authoritative verdict: REJECT P0/P1/P2=`0/1/0`.

| Finding | R7 behavior | Root cause | Bounded R8 requirement | Required proof |
|---|---|---|---|---|
| Successful retry leaves registry residue | Late-close retry reaches CLOSED and clears timer/listener/pending errors, but `guard.cleanups.size=1` | Wrapper marks completion but does not remove itself from the registry; local WebSocket untrack ownership is no longer reachable after the first failed call | Terminal success must atomically remove the wrapper/resource from the registry exactly once regardless of which retry caller observes success | Every late-close/terminate path ends with CLOSED, `cleanups=0`, `pending=0`, listeners/timers=0 |
| Cleanup re-enters `dispose()` | Inner dispose schedules/joins the same in-flight cleanup and waits for a pending set containing the outer task | Dispose has no reentrancy context and can await itself transitively | Detect cleanup-context reentry and make inner dispose bounded/nonblocking with respect to its own task while preserving other cleanup ordering | `cleanup -> await dispose()` converges; no self-cycle; concurrent external dispose still joins |
| Permanent failure | no-late-close remains CLOSING with one cleanup/error | Failure is correctly bounded but registry semantics are ambiguous | Preserve fail-closed error, keep resource tracked for caller-visible failure, but no false completion; repeated external dispose follows a finite documented policy | no-late-close bounded, no false success; registry/error state byte-exact to documented contract |

R8 may modify only preflight-safety/public-beta-preflight and direct cleanup tests. Preserve SSE/backoff code, default feature-off, unrelated generated files. Produce a persistent exact-tree build log/evidence record in addition to focused tests. No Gradle or production action. Fresh independent review is mandatory.
