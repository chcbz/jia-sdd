# OD02 draft findings — repair tracking

These are root integration observations while the sole writer is still implementing OD02. They are not the independent final code review. Final closure requires candidate-associated repair evidence and independent review; interim status is recorded below.

| ID | Finding and evidence | Required observable result |
| --- | --- | --- |
| I01 | Source inspection: `OutputUploadServiceImpl.authorize` always requests `status, receiptReplay=true`, while `requireMutable` checks only the ticket's stored operations. An old full-operation ticket can therefore pass the helper in a terminal run; a receipt miss must not fall through to mutation. | Old full-operation and reissued status-only tickets on CLOSED/RESULT_SUBMITTED can replay an exact existing receipt, but cannot create an upload, start a writer or complete a new operation. New mutation uses dynamic upload authorization inside its transaction. |
| I02 | Source inspection: complete receipt operation is concatenated with uploadId and canonical body omits runId, differing from the agreed fixed-operation envelope. | Fixed `completeUpload` operation and canonical runId/uploadId/operation hash; same key moved to another upload conflicts within the receipt identity. |
| I03 | Source inspection: `complete` writes a 202/VERIFYING receipt, but ultimately calls `status` even after a receipt hit. This can return a later state rather than the original status/body. | Original POST replays its exact persisted response. Later READY/REJECTED changes are obtained by GET. |
| I04 | Actual compiled inspector probe: complete valid UTF-8 passes, but the two-MiB sample ending after the first byte of `中` is rejected even with `complete=false`. See `content-inspector-counterexamples.json`. | An incomplete sample tail does not reject valid text. Full-content validation still rejects genuinely malformed UTF-8. |
| I05 | Actual compiled inspector probe: a 204,994-byte data-descriptor ZIP has initial entry size -1, expands to 210,763,776 bytes and is accepted despite the 200-MiB limit. See the same probe report. | Read each entry under an explicit actual expanded-byte budget; unknown header size cannot bypass the limit or make `getNextEntry` drain unbounded data. |

| I06 | Real local ClamAV with `AlertExceedsMax yes` returns OK for a ZIP with one 61-MiB expanded member while its configured member limit is 60 MiB. Aggregate 110-MiB expansion returns MaxScanSize FOUND. See `clamav-scan-limits.json`. | Application-enforced actual expanded-byte bounds aligned below scanner capacity, with a shared budget for supported nested containers and explicit rejection of unsupported/encrypted/damaged containers; only a successful scan can permit READY. |

The content probe used Temurin 21 javac/java and the current compiled service/API class directories; no Gradle task or product edit was performed. Its retained harness is `content-inspector-probe/ContentCounterexamples.java`, with source/class hashes in the report. Exit 0 means the probe ran and reproduced the defects, not that content validation passed. Repair regressions belong in the API repository and must run independently there.

## Repair observations (2026-09-10)

- I01: writer reports dynamic run-state repair; terminal old/full and reissued/status-only ticket negatives remain pending.
- I02: writer reports canonical complete envelope repair; cross-upload same-key conflict proof remains pending.
- I03: the real-dependency service test now observes the exact original create/complete DTO receipt after READY. Actual HTTP status/filter-chain evidence remains pending.
- I04/I05: both focused content regressions passed (2 tests, no failures/errors/skips), including partial UTF-8 allowance plus full malformed rejection, and actual 201-MiB ZIP expansion rejection. See `content-inspector-test-results/observation.json`; final source/candidate association and review remain pending.
- The real-dependency suite passed 4 tests with actual MySQL, MinIO and ClamAV, including first READY, hash cleanup, scanner retry and concurrent-create quota. Authorization is mocked and retry is same-instance; this is not end-to-end HTTP, real OD01 transaction enlistment or process-restart evidence. See `real-dependencies-test-results/observation.json`.

I06 status: application resource-budget repair design has a narrow independent feasibility review; implementation and repaired negative tests remain pending. A preliminary reviewer source observation attributed the behavior to the ClamAV DEFLATE path, but the expanded source investigation was interrupted by the review tool. The reproducible protocol result is the evidence basis. The completed follow-up review covered defensive resource bounds and supplied source references; the selected 50-MiB member / 90-MiB whole-tree (including root bytes) / 2048 entries / depth-3 policy is recorded in `clamav-limit-review.md` and the detailed design.

## Expanded real-dependency observation

The expanded suite passed 7 tests (no failures/errors/skips), superseding its earlier 4-test run for counting. I02 now has a cross-upload same-complete-key conflict check; I01 has mocked CLOSED/status-only receipt replay plus create/PUT refusal, but old full-operation tickets and actual OD01 authorization remain unproven. The old-writer check uses real MySQL and gated in-memory storage; real MinIO fencing is separate adapter/protocol evidence. GC preserves an ACTIVE held reference, then tombstones and releases quota after explicit reference release; it does not yet isolate hold-only, expiry, or concurrent reference insertion protection. See `real-dependencies-expanded-test-results/observation.json`.

## I06 partial repair evidence (observed 2026-09-11)

`archive-scanner-test-results/observation.json` retains 4 content tests plus 1 controlled-socket scanner-response test. Nested shared budgets, depth rejection and a permitted depth-3 ZIP now have passing focused evidence. The content suite supersedes its earlier 2-test run for counting. I06 remains open for candidate association, per-member/root-inclusive boundary tests, deterministic malformed/encrypted input and temporary-I/O service state behavior; these 5 checks do not prove the entire deployed scanning contract.

GC review blockers G01–G03 are tracked separately in `gc-recovery-review.md`; they are not closed by the earlier 7-test expanded service suite.

## HTTP coexistence and selected authorization enlistment

Three passing tests now load the production output/OAuth/default user chains and the production upload controller. They verify the mocked VERIFYING service result maps to HTTP 202/no-store, session/user bearer cannot replace a run ticket, and resource versus session fallback routes remain isolated. See `security-coexistence-test-results/observation.json`. This supplements the earlier output-only chain suite; it does not execute a complete upload or persisted receipt replay over HTTP.

One selected real-MySQL test now invokes actual ticket issuance/authorization and an upload create transaction, observes revocation pending while create is paused after authorization, then confirms the revocation completes after create and rejects a subsequent mutation. The source authorizer uses a synthetic locked root row; storage/scanner are not involved in create. See `authorization-enlistment-test-results/observation.json`. This is the selected ticket-lock enlistment interaction, not all task/chat ACL paths or the entire concurrency suite. Candidate association and final review remain pending.
