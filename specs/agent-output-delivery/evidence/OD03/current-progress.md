# OD03 implementation checkpoint

Sole writer remains `/root/od01_source_auth` in the API worktree, based on accepted `a04c2feb634643fc7e52289aa2b4a98ddf61bbb3`. Candidate `683e8007dbbde98895d82a391fc7d2a4228f46fa` is now frozen and under independent read-only review; no OD03 acceptance yet. OD04–OD11 have not started.

Task/chat controllers, shared publication/read/download service, version providers, nullable artifact extensions, chat output persistence/schema, capabilities, write-pause policy and related tests are committed in that candidate. The historical observations below precede the final HTTP test. Independent read-only review remains pending.

Observed intermediate service regression: 185 tests, 11 failures and 8 skips. Failures were in the legacy H2 `AgentTaskCollaborationServiceRealTransactionTest` and `AgentTaskWorkspaceRepeatableReadTest`, whose fixtures lacked the new nullable artifact columns. The writer repaired only their fixture schemas and reported 13/13 plus 3/3 passing. Failed XML is retained at `/tmp/cyf-od03-evidence/agent-regression-failed/`; repaired XML at `/tmp/cyf-od03-evidence/h2-fixture-repair-pass/`. These are intermediate runs, not final candidate evidence. The unchanged legacy MySQL 8.0.21 prerequisite accounts for the eight skipped cases.

`OutputDeliveryMySqlIntegrationTest` has five passing real-MySQL service cases, including task/chat publication, download, byte-exact source isolation and reference races. Its authorization is mocked, READY objects are seeded and storage is in-memory. Those tests are useful transaction evidence, but do not prove the full production-auth/upload/MinIO/HTTP chain or a connected Agent's offline lifecycle. The writer has been asked to cover the production seams before freezing and keep any connected-client lifecycle gate explicit for OD06.

A worker turn was interrupted by model-provider 503 `auth_unavailable`; root recovered the same writer without replacing or reverting its changes. Work resumed. This was an execution-provider interruption, not a product failure or authorization-review rejection.

Root's extended live HTTP helper is independently approved for tool correctness (`http-probe-review.md`); only synthetic controls have run. It is ready for a numeric-loopback development harness and cannot itself mint trusted runs or establish distinct user identities.

## Continuation on 2026-09-12

The shared root checkout now belongs to another task (`codex/hall-question-history`). Output-delivery coordination resumes in the dedicated root worktree `/home/chc/wsps/cyf-worktrees/output-root`, on `codex/agent-output-delivery` from `eae405d`; API/Web/client worktrees are unchanged. Do not switch or commit unrelated work in the shared root checkout.

Root inspected the real-dependency HTTP harness XML at timestamp `2026-09-11T15:53:46.643Z`: one test, one failure, no skips/errors. The current failure is Spring test-context setup (`BeanFactory not initialized or already closed`, `setUp:270`), superseding the older mapper-reflection failure. The sole writer remains active to repair and rerun it. This is failed intermediate evidence, not an accepted endpoint run. OD03 remains implementing and OD04–OD11 remain pending.

## Frozen candidate and repaired HTTP harness

Candidate `683e8007` is clean. Root verified the saved real-dependency MockMvc XML: **1 test, 0 failures/errors/skips**, timestamp `2026-09-11T16:55:22.888Z`; the recorded command exited 0. Both task and conversation go through real MySQL, MinIO, ClamAV, RunTicket upload/publication and RSA UserJwt retrieval, comparing the 13-byte payload. The test source digest matches the frozen candidate. See [candidate-683e8007/observation.json](candidate-683e8007/observation.json). Archived XML omits captured logs/properties; its original hash is retained. This supersedes the earlier test-container setup failure.

The candidate also changes OAuth resource handling for streaming ASYNC dispatch; the independent reviewer is explicitly checking its security scope. The preferred review provider failed with `reasoning_content` protocol errors; root assigned an independent read-only architect fallback. No cross-model review approval is claimed. Actual Agent disconnection, live HTTP deployment, client/Web and production gates remain open.

## Independent review result

`683e8007` received **REQUEST_CHANGES**, with three bounded repairs: snapshot pagination, UserJwt read error envelopes and deterministic request-hash collision. See [review-683e8007.md](review-683e8007.md). Original sole writer has resumed these repairs; OD03 remains unaccepted and OD04 has not started.

## Repair candidate frozen

`4c292cc35e4d82a23620a85296b721569ff59bd5` repairs R01–R03. Root verified **27/27** targeted checks, no failures/errors/skips; eight changed source files match pre/post-run and candidate hashes. Layering also exited 0. See [repair-4c292cc3/observation.json](repair-4c292cc3/observation.json). The same independent reviewer is checking the repair; OD04 remains pending.

## Development acceptance

The independent reviewer approved `4c292cc3`; R01–R03 are closed. Root accepted OD03 for development and assigned OD04 to the sole client writer. See [accepted-review-4c292cc3.md](accepted-review-4c292cc3.md). Previous entries above are historical checkpoints. No production/end-to-end release approval is implied.
