# JVC-OAI-OPS consecutive R15/R16 stop matrix

2026-09-05. **Execution stopped; no R17 implementation or test authorization is issued by this document.** Runtime state remains solely in `TASKS.yaml#runtime_ledger_json`.

## Bound candidates and failures

| Candidate / review | Finding | Root cause | Required closure |
| --- | --- | --- | --- |
| R15 `2fb39b5c476b00c73b73871c8a6f59610609389f` / tree `570d916855dc698f64fad0f46bc5275a045e0a0e`; reviewer `01a07068-7614-78b1-aa38-d945fe4472e9`, 0/1/0 | Reaping outer unshare supervisor incorrectly permits fixture deletion | Supervisor death can precede child PDEATHSIG setup; exact supervisor identity is not namespace drain evidence | Explicit direct-child lifecycle and positive drain acknowledgement; ambiguous proof keeps fixture |
| R16 `0c07d43335601ce680ab16412639cad2b212e4db` / tree `4bd17202f4ef86eca0933b606e367bfbb9598a74`; reviewer `01a07086-9d62-7583-a454-3010fa3b3a0b`, 0/1/0 | Setup-timeout path preserves fixture but can leave a live workload without abort delivery | Outer 5s setup window (`self_test.py:1129,1547-1552`) is shorter than two sequential inner waits (`1158,1362-1366`); abort requires `_setup_proved` (`1561-1567,1627-1640`), so late ready/workload waits on open command pipe (`1263-1267,1372-1378`) | Cancellation must be deliverable from every post-Popen state, including not-yet-ready startup; EOF/error must terminate or positively drain owned namespace rather than leave controller waiting |

R16 is clean and changes only `ops/juyiting-voice-production/tests/self_test.py`; diff SHA256 `f5bfceebcbe16f251733137660cdc1d913e9fdf1e068d6ff61d9a25784680986`. Static outer/embedded Python3.6 parsing and unchanged inventory131/count/suffix are not runtime proof. Neither candidate has run a selector.

## Bounded next remediation plan (requires authorize-remediation)

1. Freeze state transitions for post-Popen/pre-ready/ready/aborting/drained and all pipe ownership/closure paths. Abort transport admission must not depend on successful readiness proof; accepting a drain proof may still require validated identity and setup ordering.
2. Account for late readiness after caller timeout. Deliver abort or close its command endpoint safely, continue consuming bounded terminal acknowledgements, and never allow abandoned open descriptors to leave a live workload waiting.
3. Make setup/abort deadlines consistent and bounded, but do **not** treat merely increasing the outer timeout as the fix. Both timeout and EOF paths must close lifecycle independently of scheduling speed.
4. Preserve the fixture until explicit validated drain proof; failure receipts must remain honest. Retain R16 direct-child control, no unrelated process inspection/signalling, fixture registry, and all checkpoint/current-link/digest/count contracts.
5. Keep source scope to the same harness file; no production, host utility, key, flag, DB, Gradle or service changes. Future successor may run static checks only until fresh independent 0/0/0 review.
6. After review, authorize at most one staged lifecycle focus. Do not restart full matrix or reuse a diagnostic candidate as accepted runtime evidence.

API integration verification is an independent ready task and may continue its already-owned serialized invocation. No other thread process or evidence may be touched to remediate this OPS issue.
