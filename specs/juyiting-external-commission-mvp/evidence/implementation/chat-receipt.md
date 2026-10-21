# JYT-EXTERNAL-D31-CHAT-20261021 receipt
2026-10-21; Owner external-chat (ledger profile backend). Read root/API AGENTS, orchestration README, MODEL_ROUTING execution_policy, D3.1 design and handoff. Interface /home/isp/wsps/cyf/api/docs/interface-standard.md v1.2 SHA256 7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f verified.
API worktree /var/tmp/cyf-external-chat-20261021; branch codex/external-commission-chat; actual HEAD 510b2937696495b54a9203729784660e62c65082 tree 2c34d7065d760ca77c046860d9f11b5da8cfe271, initially clean. Claim recorded via orchestrator. Own chat/** only; agent/** parent-owned. Remote/latest and production not reverified. No builds/deployment/restarts; formal Gradle delegated to parent Flow.
Scope: persisted-grant routing A data/B runtime, inbound acknowledgements/results/fences, conversation admission and Runtime actual isolation gaps only. Preserve bootstrap. Earliest checks diff/static then added targeted regression tests (Flow NOT_RUN).
Parent authority API received: requireGrantTarget(tenant,client,taskOwner,taskId,grantId,grantVersion) -> Target including owner/agent/binding. No owner fallback/current policy for execution.

## Concrete parent integration needs (coding in progress)
ChatDispatchAuthorityService consumes your exact requireGrantTarget API. NEW admission uses existing currentFollowupContext + resolveFollowupBaseline to freeze exact grant tuple; please ensure both methods no longer require target owner=A and preserve reviewing discussion semantics. Historical callbacks never resolve current grant. Chat-owned outbox adds nullable task_grant_id/task_grant_version (non-task dispatches remain null); new task dispatch writes both. Runtime binding/session fencing remains original authentication service; requireGrantTarget must check grant's frozen executor_binding_id against current identity/binding, not just owner+agent. Parent TaskSkillPolicy runtimeScope resolution must likewise honor B (existing Chat task catalog already consumes runtimeScope).

Runtime scoped rules read from /home/isp/wsps/chcbz/isp-install/AGENTS.md; CYF rules explicitly carried into Runtime. Original worktree observed clean at HEAD 5e8742aac6b9261a8d6cc94f77da1175e8ae74e2 tree 9448db77464f4a01cc07172880f21d332996cc3c. Isolated writer /var/tmp/cyf-external-chat-runtime-20261021 branch codex/external-commission-chat-runtime from that actual baseline. Remote not refreshed; no latest claim. Actual gap: CHAT thread key omitted persisted grant/assignment generation. Added task facts/authority digest; existing A owner/client/tenant/conversation dimensions retained. Existing ACK durable message+dispatch identity and fresh B session binding do not require a new protocol; added replay isolation regression. Candidate Runtime version 1.2.3, not built/released/activated.

## Candidate handoff (2026-10-21)
API commit `a57414cfde704f2ac600f35d1371a11e12941717`, tree `a2fb1367b9826997ab6aef7be7d387766861568f`; 27 scoped chat files, clean worktree after commit.
Runtime commit `c11a078e0fc365c09706d569e0c668bcdb230d9f`; 4 files, clean worktree after commit. Candidate version 1.2.3 only, not released.

The previously proposed extra authority API is NOT needed: historical CHAT freezes requirementRevision along with grantId/grantVersion/assignmentRevision, then calls existing admitFollowupBaseline on that exact tuple under A's task-root lock (current root taskVersion is only a concurrency check, never replacement dispatch authority). This supports discussion/review even when the grant does not contain DELIBERATE. INSPECT retains explicit INSPECT_INPUTS admission. STOP validates the original persisted target/binding but does not require ACTIVE, so revoked work can still be stopped; it never routes to a replacement target. Existing multi-member task transport remains owner-only, outside external single-Agent support. Public conversation read ACL is unchanged. Five-argument PWE authentication scopes are unchanged; no PWE code edited.

### Migration list (NOT EXECUTED)
- API `chat/jia-chat-mapper/src/main/resources/db/chat-external-commission-v1-migration.sql`: add nullable `chat_dispatch_outbox.task_grant_id VARCHAR(100)` / `task_grant_version BIGINT`; index `idx_chat_outbox_dispatch(tenant_id,client_id,dispatch_id,event_type)`; diagnostics for historical bounty dispatches with no provable reference. No latest-active-grant backfill, data deletion, status changes, or startup ALTER for these fields/index.
- API `chat/jia-chat-mapper/src/main/resources/db/chat-deliberation-schema.sql`: same additive definitions for clean-schema provisioning.
- Runtime: no database migration.
- Parent's agent-external-commission-v1-migration.sql is an integration prerequisite, not authored/applied by this slice.

### Verification and remaining risks
- API git diff --check / staged diff --check: PASS; migration text assertions: PASS (not SQL execution).
- API Java compile/tests and SQL/transaction/concurrency tests: NOT_RUN, only parent Flow may run. Integration must include parent authority API/implementation + executor grant fields. Source candidate is not formal acceptance.
- Runtime node --check (both modified production modules): PASS. Targeted `node --test --test-name-pattern='thread key|external task CHAT|one B ACK|persisted CHAT ACK' conf/codex-ws-agent/test/chat-runtime.test.mjs`: 4 pass, 0 fail, 42 skipped. Log `/var/tmp/cyf-external-chat-runtime-20261021-node-check.log`. Existing node_modules reused through an ignored symlink after matching package-lock SHA; no dependency installation/build.
- Runtime task identity digest includes task ID + persisted authority, not ordinary task status/revision changes. ACK protocol unchanged; regression proves A/C messages remain separate while rebinding transport to fresh B session.
- Historical ordinary bounty outbox rows without grant references fail closed and need an explicit cutover disposition by the release owner; migration only diagnoses them. No database was inspected/changed to claim a zero-row backlog.
- No remaining external API-method blocker identified. Formal Flow compile and regression, real DB lock order/concurrency, and authorized migration validation remain required. No builds/deployment/restarts/push performed by this slice.

### Suggested parent Flow selectors (plus layering and impacted regressions)
`ChatDispatchAuthorityServiceTest`, `ChatDeliberationOutboxAuthorityTest`, `ChatExternalCommissionMigrationTest`, `ChatReviewContextAdmissionTest`, `AgentWebSocketHandlerTest`, `JuyitingAgentRelayServiceTest`, `ChatDeliberationOutboxCommitTest`, `ChatBootstrapTransactionBoundaryTest`; mmd regression `ChatInspectionAuthorityServiceTest`, `ChatTypedInspectionSpringTransactionTest`, `ChatBountyExecutionCoordinatorSpringTransactionTest`, `JuyitingWorkflowMySqlTest`.
Grant fixture audit found one Chat fixture factory (`ChatBountyExecutionCoordinatorSpringTransactionTest`), now explicitly persists executorOwner/executorBinding and injects exact grant target into both constructor-based service fixtures. Admission fixtures include frozen requirement revision. API tests are authored/updated, not represented as passing.

### Exact API changed files
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-core/src/main/java/cn/jia/chat/deliberation/ChatDispatchOutboxEntity.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-mapper/src/main/java/cn/jia/chat/deliberation/ChatDeliberationMapper.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-mapper/src/main/java/cn/jia/chat/deliberation/ChatDispatchAuthorityMapper.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-mapper/src/main/resources/db/chat-deliberation-schema.sql`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-mapper/src/main/resources/db/chat-external-commission-v1-migration.sql`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatDeliberationSchemaInitializer.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapAdmissionService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDispatchAuthorityService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatInspectionAuthorityService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatMaterialsInputService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatTypedDeliberationContextService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatTypedDiscussionAdmissionService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatTypedInspectionContextService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/main/java/cn/jia/chat/service/JuyitingAgentRelayService.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/mmdRegressionTest/java/cn/jia/chat/config/JuyitingWorkflowMySqlTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/mmdRegressionTest/java/cn/jia/chat/service/ChatBountyExecutionCoordinatorSpringTransactionTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/mmdRegressionTest/java/cn/jia/chat/service/ChatInspectionAuthorityServiceTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/mmdRegressionTest/java/cn/jia/chat/service/ChatTypedInspectionSpringTransactionTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/test/java/cn/jia/chat/config/ChatExternalCommissionMigrationTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/test/java/cn/jia/chat/handler/AgentWebSocketHandlerTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/test/java/cn/jia/chat/service/ChatDeliberationOutboxAuthorityTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/test/java/cn/jia/chat/service/ChatDispatchAuthorityServiceTest.java`
- `/var/tmp/cyf-external-chat-20261021/chat/jia-chat-service/src/test/java/cn/jia/chat/service/ChatReviewContextAdmissionTest.java`

### Exact Runtime changed files
- `/var/tmp/cyf-external-chat-runtime-20261021/conf/codex-ws-agent/chat-runtime.mjs`
- `/var/tmp/cyf-external-chat-runtime-20261021/conf/codex-ws-agent/agent-client.mjs`
- `/var/tmp/cyf-external-chat-runtime-20261021/conf/codex-ws-agent/test/chat-runtime.test.mjs`
- `/var/tmp/cyf-external-chat-runtime-20261021/conf/cyf-agent-runtime-v1/package.json`
