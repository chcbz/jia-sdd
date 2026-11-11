# JVC-OAI-OPS R16 bounded containment correction

2026-09-05. Implementation-only successor to independently rejected R15; no selector or production action authorized.

## Bound evidence

- Base commit `2fb39b5c476b00c73b73871c8a6f59610609389f`, tree `570d916855dc698f64fad0f46bc5275a045e0a0e`.
- Worktree `.worktrees/juyiting-voice-conversation-ops-r7`; same bounded three-file ownership.
- Independent reviewer `01a07068-7614-78b1-aa38-d945fe4472e9`: REJECT P0/P1/P2=0/1/0. No runtime executed.
- R15 is the first review failure since matrix-bound R15 remediation authorization. R13/R14 history remains in the ledger; this note does not clear it.

## Root cause and acceptance delta

| Finding | Root cause | Required correction |
| --- | --- | --- |
| `self_test.py:1169-1176,1189-1205,1226-1242,1292-1312` | Every reaped outer unshare process sets `_proved_drained`, including supervisor termination before its namespace child establishes parent-death handling. The child can outlive the supervisor; supervisor reaping alone cannot authorize fixture deletion. | Establish exact namespace-init ownership/setup and drained acknowledgement across all startup/abort/exception paths. A negative, missing or ambiguous proof must retain fixture and diagnostic receipt, never `rmtree` or PASS. |

Do not solve this by upgrading host utilities, signalling numeric groups, enumerating host `/proc`, or weakening cleanup assertions. Prefer a small auditable child-control/handshake protocol to another inference from supervisor return code. A separate bounded harness helper is not authorized by this packet without scope update; an embedded Python child controller may be considered. Production files/lib/scripts remain frozen.

Preserve: prelaunch fixture-lifetime registry, aggregation of all current/historical cleanup failures, exact owned-process-only operations, strict six-checkpoint successful route and initial rc=0, eight current-link assertions, failed-terminal digest validation, inventory 131 and two README counts. Any new case must be explicitly justified and count updates stay exact.

Allowed implementation: `ops/juyiting-voice-production/tests/self_test.py`; inventory and README count-only edits only if necessary. Static Python 3.6 parse/diff/scope checks and clean diagnostic commit. No test selector, unshare execution, signal, Gradle, DB, key, flag, build, deployed file, or service operation.

Next gate: fresh independent read-only review of the new exact commit/tree; only 0/0/0 may unlock ONE staged lifecycle focus. A second consecutive failure stops at a frozen root-cause matrix; no blind rerun.
