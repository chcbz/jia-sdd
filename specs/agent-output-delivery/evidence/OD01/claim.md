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

Candidate evidence association is resolved by final-candidate reruns: seven authorization unit tests and six real MySQL tests passed with no skips; source/report digests are in `candidate-8e009b9d-test-results/observation.json`. Earlier snapshots retain their historical digests. Independent review has separately identified a blocking raw-command byte-exact violation; see `candidate-review-findings.md`. Complete review and writer repair are required before acceptance.
