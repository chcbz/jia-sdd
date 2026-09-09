# OD02 claim — object upload, verification, quota and cleanup

- Owner: sole API `critical_worker` (`/root/od01_source_auth`, continuing after OD01 acceptance).
- Branch/worktree: `codex/agent-output-delivery`, `/home/chc/wsps/cyf-worktrees/output-api`.
- Base: `c5330dd50da6c03e55edca0744485a1b95385552`; upstream independent APPROVE is in `../OD01/accepted-review-c5330dd5.md`.
- Root owns specifications, task ledger, evidence and integration coordination; the API writer owns implementation and lock-held Gradle validation. Preserve all other worktrees and unrelated changes.

## Scope and sequence

1. Implement OD02 output object/upload/quota/reference/receipt persistence, exact HTTP ticket routes and transaction boundaries in Agent API/core/mapper/service modules. Reuse OD01 authorization and opt-in migration conventions. Keep Agent independent of Chat implementations.
2. Complete the real fixture path: initialize → immutable staging stream → complete → persisted verification/retry → READY. Reuse the already installed MySQL, MinIO and ClamAV services, not another installation.
3. Verify writer epoch/deadline fencing, quota reservation and release, type/hash/scan rejection, scanner-outage recovery, receipt replay, scoped cleanup and GC reference/hold protection. External storage/scanner calls stay outside SQL transactions.
4. Archive focused real-dependency/filter-chain/transaction results, freeze a candidate and obtain independent read-only review before OD03 publication/download begins.

Use `../../detailed-design.md`, `../../schema-contract.yaml`, `../../openapi.yaml`, `../../fixtures.json` and `../OD01/next-task-handoff.md`. Persistent verification is a required behavior; its internal job representation must be explicit. If bounded leases, retry scheduling, per-binding counters or staging cleanup require schema fields beyond the frozen minimum, report the concrete additions for root contract alignment rather than silently drifting from it.

Current proof is limited to development infrastructure and OD01 authorization. No upload endpoint, ready file, end-to-end retrieval or production release is accepted by this claim. Every Gradle invocation holds `/tmp/cyf-gradle.lock`; retain local dependency-substitution limits and preserve reports before subsequent test tasks replace them.
