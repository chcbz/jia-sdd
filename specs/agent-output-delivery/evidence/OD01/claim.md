# OD01 claim — source ownership, run binding, WS ticket exchange

- Status: candidate frozen; independent final review in progress; not accepted yet.
- Sole writer: `critical_worker` (`/root/od01_source_auth`). Root writes control-plane evidence only.
- API worktree: `/home/chc/wsps/cyf-worktrees/output-api`.
- Branch: `codex/agent-output-delivery`.
- Base: `f418e3f5bf7afcdbddf9c1ecec1b293f657c977c`.
- Candidate: `8e009b9d241979abb072d4b5b12d42b0476450dc` (67 changed files); API worktree clean and writer paused.
- Final reviewer: existing independent read-only `architect` (`/root/output_design_review`), reused after the earlier adversarial provider failure. Reviewer does not repair code.
- Dependency: OD00 accepted for development; real MySQL/MinIO/ClamAV probes and reviewed Agent/Chat transaction test passed. Canonical packaging and production topology remain release gates.
- Build ownership: OD00 helper released the global Gradle lock/build role; OD01 writer now owns lock-held, memory-bounded targeted builds.

## Scope and acceptance

| Area | Required OD01 evidence |
| --- | --- |
| Source ownership | persisted owner/scope; wrong owner, case variants, tenant=0 and cross-client requests rejected |
| Trusted run | actual conversation and bounty/task dispatch create server-owned source/run context for the explicit target; no client fallback IDs become authority |
| WS ticket | registered bound session, current identity and revocation checks; opaque bearer hash only in storage, unicast receipt, no chat/broadcast/prompt/log leakage |
| Runtime capabilities | separate authenticated CAS snapshot, 90-second freshness, old/absent client unsupported, stale runtime updates and premature R2 capabilities rejected |
| Migration | opt-in additive identity/capability segment, fresh/upgrade/repeat/invalid schema checks on disposable MySQL, no owner backfill |
| Compatibility | default disabled; legacy chat/commands and map/roster separation preserved; file-write endpoints and deferred WS output handlers remain out of scope |

Acceptance IDs: O07, O09, O23, O26. Interfaces must remain compatible with the full v1.1 R1/R2 design; OD01 does not implement OD02 storage/upload/GC or OD03 publication/UI/client work.

The writer must hand off committed code and test evidence for an independent read-only review before OD02. User continuation is already authorized; no repeated routine confirmation is required.

Candidate evidence association is also being checked. Of 88 recorded source digests, 85 match the candidate; three entries refer to earlier versions of `OutputRunAuthorizationServiceImpl.java` and `OutputAuthorizationMySqlConcurrencyTest.java`. Both final files were modified after their most recently archived test reports. The writer has been asked to identify the last changes and any later verification; these mismatches are not silently relabeled as final-candidate test evidence.
