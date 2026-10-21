# JYT-EXTERNAL-D31-WEB-20261021 — scoped receipt

- Accepted 2026-10-21; Owner d31-web-owner under parent integration Owner.
- Read root AGENTS.md, live web/AGENTS.md, orchestration README, feature design D3.1 §9 and handoff, MODEL_ROUTING execution_policy.
- Interface: /home/isp/wsps/cyf/api/docs/interface-standard.md v1.2; verified SHA256 7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f.
- Product scope ONLY /var/tmp/cyf-external-web-20261021 src/tests, branch codex/external-commission-web; clean initial HEAD 9dbd132e8bc25119c0532cbed672ab7fa4a214b3, tree adacb21c069236c728ecd494f425210495153ee5.
- Authorized exceptions: this receipt and orchestrator claim; update only live prototype external-commission.js/css and specs/prototype-spec.md, preserving existing D2/unrelated changes. Prototype precedes product.
- Implement detail policy GET/PUT/request, unified paginated candidates and recommendation, task assignedTarget continuation; retain owner management/private-chat guards. No standalone card, inbox, wait-for-instruction or extra start button.
- Earliest validation: node syntax checks, scoped existing test infrastructure diagnostics. Formal tests/build/deployment are parent Flow responsibility. No external account/user/model calls.
- Remote develop, tested release and online versions not queried; initial local HEAD is not a claim of latest or deployed source.

## Implementation handoff — 2026-10-21

- Commit `e5192afd2fe799dd38f11ae07c456e72de4694e5`; tree `521493932f5d0fe930a856597f49ace3e98c8d01`. Branch codex/external-commission-web; clean worktree. Orchestrator transitioned to ready_for_integration, writer released. No push/merge/build/deploy.
- Implemented owner detail policy GET/PUT/request with durable original key/body/requestId recovery, identity/auth/binding/visibility fences; failed read never implies false. Unified safe paginated candidates and advisory recommendation, existing inline confirmation disclosure, task assignedTarget continuation independent of owner roster. Private chat/profile management remain owner-only. First definitive point-and-deliberate 409 releases only a never-acknowledged first intent; ambiguous recovery retains original intent.
- Strict five-field candidate DTO; no other-user profile-capabilities requests. Null provider displays “其他用户”; lowercase availability is display-only, not inferred grant revocation. Recommendations expect `.agent.agentId`, taking ranking metadata only for fetched safe candidates.
- Prototype updated FIRST, only live external-commission.js/css and specs/prototype-spec.md: removed inbox/wait-for-instruction/separate confirmation dialog/extra start. Existing inline disclosure and automatic simulated first turn. Reused existing port 18786 preview; local Playwright checks passed at 1440/390/320 (owner switch, no extra dialog/start/inbox, automatic first turn, no overflow/page errors). Live dirty prototype not copied or included in product commit; parent preserves separately.

### Local targeted diagnostics — not formal Flow evidence

Working directory `/var/tmp/cyf-external-web-20261021`; reused ignored node_modules link. Common invocation:
`node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --timeout 10000 --exit --reporter dot <selectors>`

- **199 passing**: tests/{juyiting-external-commission,juyiting-hall-data,juyiting-hall-chat-context,juyiting-agent-panel-actions,juyiting-point-and-start,juyiting-native-bounty-capability,juyiting-bounty-toolbar,juyiting-controlled-image-checkbox,juyiting-agent-profile-capabilities,juyiting-bounty-assignment-context,juyiting-bounty-assignment-read}.test.js. Log `/tmp/d31-web-targeted-final.log`.
- **267 passing**: tests/{archive-reader,juyiting-live-map-preview-integration,juyiting-task-workspace-integration,juyiting-voice-conversation,juyiting-flow-ui,juyiting-requirement-reference-intake,juyiting-five-ui-fixes,juyiting-hosted-point-flow,juyiting-task-workspace-wiring,funded-bounty-public-contract-r7,juyiting-requirement-reference-integration,juyiting-selected-agent-card}.test.js. Log `/tmp/d31-web-harnesses-final.log`.
- **37 passing**: tests/juyiting-component-behavior.test.js with `--grep 'bounty|Bounty|matter|Matter|point|admi|identity|private|conversation|profile|AgentPanel'`. Log `/tmp/d31-web-components-final.log`.
- All 503 ran on final committed bytes. Actual mounted Vue watchers/components and synthetic real-HTTP serialization; no external user/account/model calls. Existing var-dialog/var-icon test-stub warnings remain.
- JS node --check, Vue parse/compileScript, differential ESLint for all 9 touched product files, git diff --check passed. ESLint zero added findings; existing BountyPanel 15/JuyiHall 231/useHallData 3 unchanged; other touched product files zero. Log `/tmp/d31-web-static-final.log`.

### Remaining verification / blockers

No Web implementation blocker. Parent owns real cross-account API/Agent/PWE integration, recommendation safe response compatibility, grant/binding invalidation, authoritative full Flow tests/build on exact integrated SHA, and unified release. Local diagnostics do not constitute formal acceptance. No deployment performed, no API/authority/Agent/PWE writes. Parent retains live prototype separately.

### Committed files (absolute paths)
- /var/tmp/cyf-external-web-20261021/src/components/juyiting/AgentPanel.vue
- /var/tmp/cyf-external-web-20261021/src/components/juyiting/BountyPanel.vue
- /var/tmp/cyf-external-web-20261021/src/components/world/JuyiHall.vue
- /var/tmp/cyf-external-web-20261021/src/composables/juyiting/hallAssigneeCandidates.js
- /var/tmp/cyf-external-web-20261021/src/composables/juyiting/hallPointAndStartIntent.js
- /var/tmp/cyf-external-web-20261021/src/composables/juyiting/useExternalServicePolicy.js
- /var/tmp/cyf-external-web-20261021/src/composables/juyiting/useHallChatContext.js
- /var/tmp/cyf-external-web-20261021/src/composables/juyiting/useHallData.js
- /var/tmp/cyf-external-web-20261021/src/composables/juyiting/useHallPointAndStart.js
- /var/tmp/cyf-external-web-20261021/tests/archive-reader.test.js
- /var/tmp/cyf-external-web-20261021/tests/funded-bounty-public-contract-r7.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-bounty-toolbar.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-component-behavior.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-controlled-image-checkbox.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-external-commission.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-five-ui-fixes.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-flow-ui.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-hall-chat-context.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-hall-data.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-hosted-point-flow.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-live-map-preview-integration.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-native-bounty-capability.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-point-and-start.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-requirement-reference-intake.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-requirement-reference-integration.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-selected-agent-card.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-task-workspace-integration.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-task-workspace-wiring.test.js
- /var/tmp/cyf-external-web-20261021/tests/juyiting-voice-conversation.test.js

## Authorized continuation — API contract tests, 2026-10-21

- Same task JYT-EXTERNAL-D31-WEB-20261021, Owner d31-web-owner; parent explicitly extends scope to two NEW tests only: AgentExternalServicePolicyControllerTest and AgentExternalServicePolicyMySqlTest.
- Independent API worktree `/var/tmp/cyf-external-contract-tests-20261021`, branch `codex/external-commission-contract-tests`; actual base commit `510b2937696495b54a9203729784660e62c65082`, tree `2c34d7065d760ca77c046860d9f11b5da8cfe271`.
- Read live API AGENTS and current uncommitted policy/controller/authority/mapper contracts read-only. No implementation/build.gradle edits; parent registers source sets. Existing HTTP advice and isolated MySQL fixture environment/MyBatis registration patterns reused; no runner.
- Scope: actual Q/R HTTP controller pipeline, boolean enabled/string expectedRevision, JWT owner/client/tenant and unauthorized scope; real MySQL CAS/replay, assignment authority lock versus switch, active binding/alias candidate filtering. No local Gradle, Flow or deployment. Execution evidence remains pending parent integration.

### API test continuation delivery — 2026-10-21

- Independent tests-only commit `20043277200a2333bf1fe0a6f5dfa6970ba34be8`; tree `7711346d886d6d3a5b0d0864098be516970868b3`; base `510b2937696495b54a9203729784660e62c65082`. Branch `codex/external-commission-contract-tests`, worktree `/var/tmp/cyf-external-contract-tests-20261021`, clean after commit. Only the two requested new test files are committed; no build.gradle or implementation changes.
- `/var/tmp/cyf-external-contract-tests-20261021/agent/jia-agent-service/src/test/java/cn/jia/agent/api/AgentExternalServicePolicyControllerTest.java`: 8 test methods. Embedded loopback Tomcat + signed HS256 JWT validated by real resource-server filter + production MVC/controller/Q ApiJsonData/R advice. Service is mocked to isolate wire boundary; real service persistence is covered in companion class. Tests boolean enabled and decimal-string expectedRevision, >2^53 returned revision, original receipt/replay versus current value, closed Q/data shapes, duplicate/malformed input, requestId correlation, owner/client and conflicting tenant claim isolation, 401/404/409, safe 5-field candidate paging/null provider/lowercase availability.
- `/var/tmp/cyf-external-contract-tests-20261021/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentExternalServicePolicyMySqlTest.java`: 9 test methods. Real production mappers, policy/identity/grant DDL, identity/policy transaction proxies, authority service; no mocked SQL/DAO/locks. Covers opposite first-write CAS, concurrent same-key replay, immutable original after later write, scope/key separation, outer rollback, both grant-lock/switch orderings plus absent-policy lock, canonical pagination, active binding/audited legacy alias, foreign open client exclusion, replacement binding default-off, mismatched runtime unavailable projection.
- Grant concurrency is targeted at real TaskAssigneeAuthorityService.lockForAssignment under task-root transaction; it persists the frozen executor using real grant-table SQL, then checks requireGrantTarget/assignedTarget after closing. It is not a full point-and-deliberate/Agent/PWE end-to-end test.
- Reused `JYT_UX_B01B_MYSQL_URL`, `_USER`, `_PASSWORD`, `_DATABASE_PREFIX`, `_ISOLATED_FIXTURE=true`; each test creates/drops only its own random `_external_policy_` database. URL absent => class skipped; malformed/unacknowledged configured fixture => fails closed. Parent must ensure the fixture is provided and tests are actually executed, not count skips as passing.
- Parent source-set wiring: HTTP test needs the same embedded Tomcat/security dependencies already used by executionHistoryHttp plus existing test/Mockito dependencies; MySQL test needs existing MyBatis/MySQL runtime and production mapper SQL resources. No new framework or runner introduced.
- Verification performed: JDK21 JavacTask.parse only (`-proc:none --release 21`), both files parsed with SYNTAX_ERRORS=0; staged git diff --check passed. Log `/tmp/d31-api-contract-tests-syntax.log`. NO dependency/type compilation, JUnit/HTTP/MySQL execution, Gradle, Flow, build or deployment was performed. All 17 tests await parent execution on integrated source.
- Static integration attention: malformed pageSize deliberately asserts HTTP400. Current shared advice has generic handling for non-ErrorResponse exceptions; parent should verify Spring's conversion-exception path does not become HTTP500. This is a contract assertion, not a reported executed failure; no implementation changed.
- Main API was read-only throughout. At final inspection its HEAD was `8273c0994a0b5be0262988ab8fdcfa2dc4ea7bd1`; this does not change the test commit's requested base. Observed contract SHA256: controller `783586b3e9f287edb12f550f1a0f6f665b2bf554b654ff7fe99e62342e03cd70`; policy service `5f163f15877e4a4e6aca569afafeef6f80cfbd2ac94aa65951cac1a6ccb1a0a2`; authority service `09c3c81e9ed688e44d5a60cfba176bda56974f8564eec3fad8da5cd8932bc7fc`; policy mapper `5f7c0d47f1f920827bc1437dc5e4f31b78989e680070693e2d70da850afc22a7`.
- No remaining authoring blocker; parent owns source-set registration, integration and formal test execution. No push/merge/deploy.

### Cloud fixture correction and runtime SQL extension — accepted 2026-10-21

Same task/worktree, resuming from tests commit `20043277200a2333bf1fe0a6f5dfa6970ba34be8` / tree `7711346d886d6d3a5b0d0864098be516970868b3`. Parent confirms Flow 5260799 supplies CYF_REVIEW_MYSQLD, not an external JDBC fixture URL. Replace new MySqlTest's URL gate with the existing JuyitingWorkflowMySqlTest owned temporary MySQL pattern (inline within this test, no runner/cross-source-set inheritance). Add real PersonalWorkspaceExecutionMapper.findForRuntime tests for A-owned execution / B grant executor and PRIVATE/TASK owner isolation. Only new test class files remain writable; no implementation/build.gradle/Gradle/Flow/deployment.

### Cloud correction delivered — 2026-10-21

- Follow-up commit `c1fb52f031dd8975386c744c153ff37ed8e36599`; tree `de8b6a850f5fe8d8d9f072662943629706c2a009`. Applies AFTER tests-only commit `20043277200a2333bf1fe0a6f5dfa6970ba34be8`. Clean independent worktree, same branch. Only AgentExternalServicePolicyMySqlTest.java changed.
- Supersedes the previous external JDBC environment paragraph: class now gates on `CYF_REVIEW_MYSQLD` and uses only its own `@TempDir` data/socket/PID/log paths, loopback ephemeral port, MySQL8.0.21 validation, and random per-test schemas. No external URL/password/fixture acknowledgement needed. Initialization and server Process handles retained and cleaned on startup failure or @AfterAll; only those exact owned handles are terminated/waited. No shell/name/PID-file/port-based kill; no separate runner or inheritance from Chat/test source sets. Startup diagnostic: `CYF_EXTERNAL_POLICY_MYSQL owned=true version=...`.
- Added three real PersonalWorkspaceExecutionMapper.findForRuntime SQL tests (12 MySQL methods total; HTTP remains 8): A-owned CONVERSATION execution with frozen B executor is visible only to B; reject A/C and wrong tenant/client/Agent/task/run/case/padding. Missing/mismatched grant ID/version/owner/client/target/task cannot authorize a read. PRIVATE/TASK remain owner-only, including a negative foreign-grant reference fixture. Added only minimal execution table columns and production mapper registration; no implementation edits.
- Read current committed main API eb2b934422 + Chat8273c0994a. Observed production PersonalWorkspaceExecutionMapper SHA256 `61ad5922b64ed2bd8930f0d821945985c28dfc0c06fc655f2f08e29b6488e651`. Grant status/admission/runtime-account checks outside findForRuntime remain parent service tests, not claimed as covered by this lookup alone.
- JDK21 parse-only syntax check on both new classes: SYNTAX_ERRORS=0; git diff --check passed. Log `/tmp/d31-api-contract-tests-cloud-syntax.log`. No dependency compilation, test/MySQL process execution, Gradle, Flow, build or deployment performed locally. Parent must run the integrated 20 tests with CYF_REVIEW_MYSQLD supplied and verify non-skipped MySQL results. No remaining authoring blocker.
