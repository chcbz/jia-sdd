# Independent review of 7701a556

Verdict: **REQUEST_CHANGES**, OD02 development gate only. Independent read-only architect fallback `/root/output_design_review`; preferred adversarial provider unavailable, so this is not cross-model approval.

| Finding | Status | Evidence / remaining requirement |
| --- | --- | --- |
| R01 expected identity denial / transaction poisoning | Closed subcase | Production identity method catches expected AGENT_FORBIDDEN inside its Spring transaction boundary. Real MySQL tests use production DAOs and the proxied identity service; suspended, retired, missing identity, inactive binding, unchanged ACTIVE and unexpected infrastructure are covered. |
| R01 recovery deadline after lock waiting | Open P0 | `authorizePersistedMutation` checks recovery time before potentially waiting on identity/runtime locks, then returns true without refreshing the clock. The run may expire during this wait and still authorize READY. |
| R04 ZIP local/CEN structure | Closed | Exact EOCD/CEN/local layout, one-to-one offsets/names/flags/method/sizes/CRC and descriptor boundaries checked. Prior harmless hidden-local counterexample now rejects; mismatches covered. |
| R06 filter classification | Closed | Actual chain separates 401 credential denial, 403 ACL/operation denial and retryable 503 infrastructure failure, preserving envelope/no-store/request ID. |
| R02/R03/R05/R07/R08 | Remain closed | No regression identified by bounded source review. |

Minimum repair: refresh the clock after identity/runtime locking while the run remains locked. Add a real-MySQL identity-lock barrier crossing recovery expiry; verify REJECTED/OUTPUT_AUTH_REVOKED, no stored-byte transfer and eventual reservation cleanup. Retain ACTIVE success and retryable infrastructure behavior. Original writer is repairing this subcase; OD03 remains gated.

The frozen 7701a556 scoped regression passed **83/83** with no skipped tests, failures or errors. Actual invocation, exit, eight XML reports and source-association limits are in `repair-7701a556-test-results/`. This passing batch lacks the newly identified expiry-during-lock-wait case and does not overrule the finding. Do not add overlapping prior stage totals or relabel this batch as a later candidate run.

## Nonblocking resource follow-up for OD06

Nested ZIP structure checking temporarily reads the bounded nested member into a byte array. The synchronous parser does not retain that array into the next recursion, but allocation still increases heap pressure; concurrent complete requests can invoke verification directly, so the scheduler is not a global concurrency bound. Root has not verified production heap sizing or concurrent maximum-size archives. OD06 must account for this in load/memory checks and use a bounded parser/concurrency repair if needed. This note is not a proof of unbounded per-level retained arrays or a reopening of the reviewed hidden-member correctness finding.
