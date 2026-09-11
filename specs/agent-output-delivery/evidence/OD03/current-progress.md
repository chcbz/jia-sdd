# OD03 implementation checkpoint

Sole writer remains `/root/od01_source_auth` in the API worktree, based on accepted `a04c2feb634643fc7e52289aa2b4a98ddf61bbb3`. No OD03 candidate is frozen or accepted yet; OD04–OD11 have not started.

Task/chat controllers, shared publication/read/download service, version providers, nullable artifact extensions, chat output persistence/schema, capabilities, write-pause policy and related tests are present as uncommitted implementation. They still require final verification and independent read-only review.

Observed intermediate service regression: 185 tests, 11 failures and 8 skips. Failures were in the legacy H2 `AgentTaskCollaborationServiceRealTransactionTest` and `AgentTaskWorkspaceRepeatableReadTest`, whose fixtures lacked the new nullable artifact columns. The writer repaired only their fixture schemas and reported 13/13 plus 3/3 passing. Failed XML is retained at `/tmp/cyf-od03-evidence/agent-regression-failed/`; repaired XML at `/tmp/cyf-od03-evidence/h2-fixture-repair-pass/`. These are intermediate runs, not final candidate evidence. The unchanged legacy MySQL 8.0.21 prerequisite accounts for the eight skipped cases.

`OutputDeliveryMySqlIntegrationTest` has five passing real-MySQL service cases, including task/chat publication, download, byte-exact source isolation and reference races. Its authorization is mocked, READY objects are seeded and storage is in-memory. Those tests are useful transaction evidence, but do not prove the full production-auth/upload/MinIO/HTTP chain or a connected Agent's offline lifecycle. The writer has been asked to cover the production seams before freezing and keep any connected-client lifecycle gate explicit for OD06.

A worker turn was interrupted by model-provider 503 `auth_unavailable`; root recovered the same writer without replacing or reverting its changes. Work resumed. This was an execution-provider interruption, not a product failure or authorization-review rejection.

Root's extended live HTTP helper is independently approved for tool correctness (`http-probe-review.md`); only synthetic controls have run. It is ready for a numeric-loopback development harness and cannot itself mint trusted runs or establish distinct user identities.

## Continuation on 2026-09-12

The shared root checkout now belongs to another task (`codex/hall-question-history`). Output-delivery coordination resumes in the dedicated root worktree `/home/chc/wsps/cyf-worktrees/output-root`, on `codex/agent-output-delivery` from `eae405d`; API/Web/client worktrees are unchanged. Do not switch or commit unrelated work in the shared root checkout.

Root inspected the real-dependency HTTP harness XML at timestamp `2026-09-11T15:53:46.643Z`: one test, one failure, no skips/errors. The current failure is Spring test-context setup (`BeanFactory not initialized or already closed`, `setUp:270`), superseding the older mapper-reflection failure. The sole writer remains active to repair and rerun it. This is failed intermediate evidence, not an accepted endpoint run. OD03 remains implementing and OD04–OD11 remain pending.
