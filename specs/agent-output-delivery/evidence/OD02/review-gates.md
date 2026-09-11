# OD02 review packet

Candidate is `0ac392156627d231ceb2fcb408e938bd877271b4`; source association now passes for 69 non-skipped output tests. Full regression has one unchanged Rabbit prerequisite failure and 103 skipped service tests. Independent review is REQUEST_CHANGES (`review-0ac3921-findings.md`). This document is a review entrypoint, not an acceptance result. Review a named immutable API commit when supplied, and do not confuse the live worktree with that commit.

## Scope to approve

OD02 implements upload byte objects, quotas, verification/recovery, cleanup/GC and their exact ticket HTTP routes. Assess the OD02 portions of O10/O11/O12/O20/O25/O27/O28 against `../../detailed-design.md`, `../../schema-contract.yaml` and `../../openapi.yaml`.

Client filesystem snapshot/no-follow handling belongs to OD04. Production publication/reference/READ_PIN APIs and owner list/download authorization belong to OD03. UI expiry/download behavior and integrated live deployment are later gates. Do not claim those features are implemented based on OD02 tests; conversely, do not require their complete implementation in order to review OD02's reusable upload and object-lock primitives.

## Required code checks

- Ticket auth and current run/source/identity locks enlist in each mutation transaction. CLOSED/RESULT_SUBMITTED old full-operation and status-only tickets may replay exact receipts but cannot mutate on a miss. Revocation/scope mismatch always rejects.
- Strict request parsing, exact create/complete receipt identity and canonical hash, fixed complete operation, original HTTP status/body replay, no storage identity or token disclosure. Binding errors are permanent client errors, not generic 503.
- Business file reservation versus per-epoch physical reservation, bounded create/attempt counters, concurrency limits, fixed writer deadline/session expiry, late-writer CAS, durable verification retries and idempotent completion.
- Every data PUT is create-only on a never-reused epoch key. Cleanup/GC uses permanent token-bound zero-byte tombstones and acknowledges exact HEAD proof before charge release. Versioned/suspended-versioning buckets and ordinary tombstone expiry are prohibited.
- G01/G02/G03 must be closed: DELETING never returns READY, expired CLAIMED/DELETING work is recoverable, and old-epoch cleanup cannot delete the current object's lifecycle. Quota deltas and finish CAS are atomic; external I/O runs outside SQL transactions.
- ZIP/OOXML resource checks count actual bytes with a shared root-inclusive 90-MiB tree budget, 50-MiB member cap, 2048 entries and depth 3. Nested temporary I/O is retryable; malformed/unsupported/encrypted/limit failures reject. Only exact clamd clean response can pass. Review current code in addition to selected test coverage.
- Schema initialization is opt-in and rejects incompatible/partial structures without completing them silently. Recheck new dependency/module boundaries and no Agent-to-Chat implementation dependency.

## Evidence entrypoints

- `gc-recovery-test-results/observation.json`: 15 selected service cases, supersedes the earlier 7/4-case versions. Real MySQL/MinIO/ClamAV with explicit fault doubles; terminal auth is mocked. New service instances with persisted expired leases model restart. READ_PIN-first ordering is test SQL, not OD03's production reference API.
- `authorization-enlistment-test-results/observation.json`: one selected real-MySQL ticket revocation/upload transaction interaction, actual ticket service with a synthetic locked source boundary.
- `security-coexistence-test-results/observation.json`: actual output/OAuth/default-session chains and production controller, mocked upload service/ticket authority; HTTP 202/no-store and session isolation. The final four-case run in `security-coexistence-final-test-results/observation.json` adds missing-header/body HTTP400 checks.
- `archive-scanner-final-test-results/observation.json`: 7-case component run (6 inspector + 1 scanner), adds member/root-byte boundaries and supersedes earlier component runs for counting.
- `schema-initializer-test-results/observation.json`, `mysql-ddl-contract-execution.md`: actual MySQL schema/metadata/partial/drift observations.
- `storage-adapter-test-results/observation.json`, `minio-protocol-execution.md`, `storage-fence-review.md`: complementary Java SDK and raw-MinIO fence evidence. Their distinct limitations must remain explicit.
- `gc-recovery-review.md`, `in-progress-findings.md`, `clamav-limit-review.md`: findings/repairs and current limits, not final acceptance.

Do not add historical overlapping test runs or raw probe scenarios to a single suite count. Use `../../tools/verify-test-evidence.py` to associate selected reports with the eventual candidate; passing hashes establish correspondence, not coverage by themselves.

OD00's local dependency substitutions remain development-only. Canonical packaging and effective deployed storage/scanner configuration remain OD06/OD11 gates. No production migration or release has occurred.
