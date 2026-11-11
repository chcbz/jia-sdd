# R01 credential / W09 fixture correction candidate — 2026-09-06

Clean `.worktrees/eco-v0-api-r5`, commit `d875ccfa0ba31187a29362f7ac454832af3e0e25`, tree `db94618f20e6991aef9b2170cc160d2a1a32610f`, parent `ac72b17b0207177eb0118e72703d1b810f790515`. Coordinator verified identity, clean state and 15-path manifest. Writer Turing completed source work; no tests, Gradle, DB, services or deployment.

Candidate changes: same REQUIRED transaction for R01 refund and exact associated managed-key active→disabled CAS; scope/owner/key-name/intent validation and rollback on mismatch/CAS/error. W09 MySQL fixture registers names before CREATE, retains on failed DROP, removes only after confirmed DROP, and bounds JDBC timeouts/reconnect. Accepted W09 commerce production and separately corrected W06 test bytes untouched. Tests cover credential/reconciler, actual handshake denial, OAuth CAS contract/service rollback and fixture lifecycle. Only build-file change is the explicitly authorized `chat/jia-chat-service` test dependency on `oauth:jia-oauth-api`.

New selectors, in addition to previously unexecuted W08/W09/R01 application selectors:
- `:agent:jia-agent-service:test --tests cn.jia.agent.hosting.ManagedHostingCredentialsTest --tests cn.jia.agent.hosting.HostingRentReconcilerTest`
- `:oauth:jia-oauth-service:test --tests cn.jia.oauth.service.impl.ApiKeyServiceManagedDisableTest`
- `:oauth:jia-oauth-mapper:test --tests cn.jia.oauth.OauthApiKeyManagedDisableContractTest`
- `:chat:jia-chat-service:test --tests cn.jia.chat.config.ApiKeyHandshakeInterceptorManagedRefundTest`
- `:economy:jia-economy-service:test --tests cn.jia.economy.config.skillapplication.EconomySkillApplicationMySqlTestFixtureLifecycleTest`
- Separate isolated MySQL: `cn.jia.economy.config.skillapplication.EconomySkillApplicationSchemaMySqlTest` and rental schema tests.

## Review admission boundary

Writer independently created Sol thread `01a0750c-ae27-79b1-83f4-43dea5565ca8` before main-controller ledger admission. It reports exact clean-tree static-only review and preliminary0/0/0, with no source edits/tests/delegation. This is **preparation only, not an accepted gate**; do not retroactively change that history. Main's forward-only formal admission was denied by the global3/3 read-only capacity. Conflict-alert emitted; no other thread's processes or evidence accessed. Reuse the unchanged preparation after explicit ledger admission and final source verdict rather than repeating full parent review.

Next integration must preserve accepted API baseline `34b67fed` (recheck remote before integration) and merge exact W06 test fix `fb2c7733`. The earlier ac72-bound noDB wrapper is not GO for this changed tree. Prepare one exact final-tree combined selector after source/integration review; no repeated per-worktree hour-long compile or claim of runtime acceptance from source alone.

## Formal forward-only review closure

After voice naturally released a read-only slot, main admitted independent Sol01a0750c at13:09:57. Reviewer rechecked exact clean d875ccfa/db94618f/parentac72 and unchanged15-path scope, reused its static preparation, then issued **R01 SOURCE ACCEPT0/0/0** and **W09 fixture SOURCE ACCEPT0/0/0**. No tests/runtime/writes/delegation occurred. Main recorded closure and released review ownership at13:13. The prior unadmitted preparation and capacity denial remain historical, not retroactively accepted execution.

Turing now owns only the clean latest-baseline source integration under W09 per `ECO-V0-API-RELEASE-INTEGRATION-R1.md`. Full runtime acceptance, isolated MySQL, preview configuration and deployment remain pending.
