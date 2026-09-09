# OD02 draft findings — repair tracking

These are root integration observations while the sole writer is still implementing OD02. They are not the independent final code review. Final closure requires candidate-associated repair evidence and independent review; interim status is recorded below.

| ID | Finding and evidence | Required observable result |
| --- | --- | --- |
| I01 | Source inspection: `OutputUploadServiceImpl.authorize` always requests `status, receiptReplay=true`, while `requireMutable` checks only the ticket's stored operations. An old full-operation ticket can therefore pass the helper in a terminal run; a receipt miss must not fall through to mutation. | Old full-operation and reissued status-only tickets on CLOSED/RESULT_SUBMITTED can replay an exact existing receipt, but cannot create an upload, start a writer or complete a new operation. New mutation uses dynamic upload authorization inside its transaction. |
| I02 | Source inspection: complete receipt operation is concatenated with uploadId and canonical body omits runId, differing from the agreed fixed-operation envelope. | Fixed `completeUpload` operation and canonical runId/uploadId/operation hash; same key moved to another upload conflicts within the receipt identity. |
| I03 | Source inspection: `complete` writes a 202/VERIFYING receipt, but ultimately calls `status` even after a receipt hit. This can return a later state rather than the original status/body. | Original POST replays its exact persisted response. Later READY/REJECTED changes are obtained by GET. |
| I04 | Actual compiled inspector probe: complete valid UTF-8 passes, but the two-MiB sample ending after the first byte of `中` is rejected even with `complete=false`. See `content-inspector-counterexamples.json`. | An incomplete sample tail does not reject valid text. Full-content validation still rejects genuinely malformed UTF-8. |
| I05 | Actual compiled inspector probe: a 204,994-byte data-descriptor ZIP has initial entry size -1, expands to 210,763,776 bytes and is accepted despite the 200-MiB limit. See the same probe report. | Read each entry under an explicit actual expanded-byte budget; unknown header size cannot bypass the limit or make `getNextEntry` drain unbounded data. |

The content probe used Temurin 21 javac/java and the current compiled service/API class directories; no Gradle task or product edit was performed. Its retained harness is `content-inspector-probe/ContentCounterexamples.java`, with source/class hashes in the report. Exit 0 means the probe ran and reproduced the defects, not that content validation passed. Repair regressions belong in the API repository and must run independently there.

## Repair observations (2026-09-10)

- I01: writer reports dynamic run-state repair; terminal old/full and reissued/status-only ticket negatives remain pending.
- I02: writer reports canonical complete envelope repair; cross-upload same-key conflict proof remains pending.
- I03: the real-dependency service test now observes the exact original create/complete DTO receipt after READY. Actual HTTP status/filter-chain evidence remains pending.
- I04/I05: both focused content regressions passed (2 tests, no failures/errors/skips), including partial UTF-8 allowance plus full malformed rejection, and actual 201-MiB ZIP expansion rejection. See `content-inspector-test-results/observation.json`; final source/candidate association and review remain pending.
- The real-dependency suite passed 4 tests with actual MySQL, MinIO and ClamAV, including first READY, hash cleanup, scanner retry and concurrent-create quota. Authorization is mocked and retry is same-instance; this is not end-to-end HTTP, real OD01 transaction enlistment or process-restart evidence. See `real-dependencies-test-results/observation.json`.
