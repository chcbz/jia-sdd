# UR06 M4 + single payload C source handoff — 2026-10-08

SOURCE_IMPLEMENTED / STATIC_ONLY. Not a compile, enrollment, MySQL, M4, C1-C4, Provider, production or Goal PASS.

## Fixed source
- Worktree: `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008`
- Branch: `codex/ur06-m4-mysql-e05-20261008`
- Base: `b125d70c79471be0fc9f306cc0f2e9cd85890ee4` / tree `4b875b456573f65865096fb34be7b25544897e46`
- Final candidate: `9c431f3be9c62467cd94b42dead27b4f14cb3909` / tree `13a8cdc7b1be98cb9ad2dbf78bf9ae5f337f121b`
- Exact remote readback matches final candidate; worktree clean (including untracked).
- Three ordered scoped commits (first four-path logic was already committed/pushed when Main delivered C; no rewritten published history):
  - `84b14cc7dd90dc55e26213db44911fe76d3cec81` / tree `16d48b30d247507c444dd542d22edd23e7e73f81` — test(ur06): bridge complete E05 acceptance onto owned MySQL (4 paths).
  - `ec414200db56a3db8f4a5ca15cba4b446ae74b3b` / tree `9d4f80c9909afa3b4a086dcba830d6347cb7ba54` — test(ur06): pin sole M4 and enrollment payload proof to C (2 paths).
  - `9c431f3be9c62467cd94b42dead27b4f14cb3909` / tree `13a8cdc7b1be98cb9ad2dbf78bf9ae5f337f121b` — test(ur04): bind existing paired proofs only to payload C (2 paths).

## Exact six owned files and final SHA-256
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java` — `f1b6bb211d5684d8465907a0895aec3e48c92944b314d01d3201d74c870292bb`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java` — `1591f5604513cb605f549cf6b792b402f80176bd330ff4304544ef35a2587461`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs` — `c30af68e0455f68e77ad01a4146178e1160ca50c5e74b4349a90e0bde6de6512`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle` — `1772f9bdaf6a2d6ebdcf79a5f9d2b1d9457aa93becf274110b2ec295587e1520`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java` — `290bd112f2398ce4b2646d60aade6ca5e4dcbbdd931e08ce3f03a57778317d2e`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs` — `c00c1f6f6460c7d34b8d541dee6d3910d731900ac3c5f2d6b31d484ccbe9486b`

UR04 last commit is ONLY its two originally authorized proof files, 5 changed literal lines. Normalizing only A→C commit/tree/archive SHA/bytes makes BOTH complete UR04 files byte-equal to b125; all original six test methods remain byte-equal. UR04 fixture/child/init and production/DDL/root docs/build.gradle/default tests are untouched.

## Source-only implementation
- Same private Lane/MySql owner, with private FOUNDATION/M4 purpose; no product wire/commands or second business implementation.
- Original 7 foundation methods byte-equal; complete original 6 E05 methods byte-equal, including every multi-lane, mutation and negative branch. 11 original oracle helpers byte-equal. 62 existing real Spring bean methods byte-equal.
- Full original agent schema + full user baseline + account-security DDL; all four original initializers. Fresh M4 applies the FULL original `agent-work-item-reassignment-e05.sql` and FULL `single-tenant-task-owner-ddl.sql` on ONE guarded connection/session. No reduced/H2 table, obsolete A02, baseline constraint deletion or production migration.
- Three explicitly synthetic ACTIVE installations/canonical identities, actual authorization hashes, user700/tenant0/original client scope; persona/binding/identity IDs1000+, ranks200+ do not overlap original seeded personas. Historical E05 receipts/transport use original canonical codec and complete immutable source/fence fields. NOT real enrollment/Rabbit publishing/JWT-created reassignment proof.
- Existing original native WS + Spring/Tomcat/filter/account/auth/real MyBatis/defaultDAOs/lease/result/D06 services remain in use. Transparent prepared observer calls real proceed first and proves no outer transaction before holding; no fake opaque object or alternate auth.
- Actual private MySQL BEFORE INSERT/SIGNAL45000 trigger refuses WORK_ITEM_SUBMITTED only after genuine artifact/work SQL. Transparent guarded JDBC counts successful executes/row receipts; addBatch does not increment, partial executeBatch receipts do not count unattempted tails. SQL/params/token are never public receipts.
- Real committed HTTP200 result/terminalACK responses are held at the Tomcat boundary; exact parent-controlled JVM exit causes actual response loss. No fake fetch/error or deleted ACK record.
- Parent durable observation creates a NEW GuardedDataSource/independent JDBC connection after Java A exits. Java B + Node B reuse same live MySQL/state, initialize=false/no DDL/reseed. No mysqld-crash-restart claim.
- Original tracked API nonpaid child is verified against API HEAD blob + fixed SHA, hash-bound copied inside exclusive root, only interpreter shebang changes. No new child resource, Provider or actual model execution.
- Original MySql owner class and DatabaseSpec process/server guard are wholly byte-equal. Exact process descendants tracked by PID/start, Node/exec child cleanup before all Java/MySQL; all handles attempted, no root deletion if owned handles remain. Full borrowed source/artifact integrity rechecked; neither is copied or deleted.

## Single payload C
- Commit `5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b`, tree `d3cdc69da62bddc48af0bc86b4f32dbfa9429b60`, 285 files; raw archive 3635200 bytes / SHA `9b5d74b27a91579359ad0a18d241f66f19d6df13d376e3cff5dbd45b729b7687`.
- Main independent readback `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur01-py311-cfg-source-readback/payload-C-main-readback.json` SHA `5615f2839d0ec41cf84eb00ec27deff74c468f860ba1392e032d79af2502ff53`.
- Both original Node SOURCE verifiers and both Java CLIENT selectors now select only C; UR04 Java tree expectation also C. No A/7594 fallback. Newly added M4 boot checks the proven PREPARE tree rather than adding another hardcoded source tuple.
- C readback/install-only source checks are NOT a real install/C1-C4/accepted target. Harness D remains Main/Knuth's separate source role; it is not payload C. No accepted artifact currently available; do not use a prior target.

## Static evidence only
- `/var/tmp/ur06-m4-c-source-check-generated-20261008.py` SHA `d435019f816ae3d8d7cbba688e1917fbbf13d73fcefbe06e66a55e7ab7b1f25a`
- `/var/tmp/ur06-m4-c-source-static-20261008.json` SHA `b84fbb7b00a5487aaa823b3b1138a923f294901728fa39ca5d1939685fa3cc02`
- Two Node `--check`, three Java tree-sitter grammar checks, exact scope, git diff check, whole-file normalized SOURCE checks, original7/original6/helper and real bean byte checks: static pass ONLY. No Java typecheck/Gradle/MySQL/pip/install/Flow/production executed by this Writer.

## Exact formal selectors — ALL NOT_RUN for this candidate
Existing same-sourceSet task `:agent:jia-agent-service:ur06EnrollMysql` selects exactly:
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e1OriginalPendingEnrollNestedCredentialDurability` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e2RealNativeRegistrationSeparateJvmGenerationAndSibling` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e3WrongExpiredManifestAndSubjectDeniedWithoutConsumption` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e4IndependentStateConcurrentSecretCasAndReplayDenial` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e5RealCommittedResponseLossRestartNeverReplaysSecret` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.m1OriginalMysqlInitializersRepeatNullableFenceAndConstraints` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.m3NativeCurrentFenceD06ReceiptsRevocationAndSiblingIsolation` — NOT_RUN

New same-sourceSet task `:agent:jia-agent-service:ur06M4MysqlE05` selects exactly:
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05ActualClientHttpCommitsOriginalResultAndTerminalAck` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05LostResultReadbackSurvivesJavaAndNodeRestart` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05TerminalAckLostResponseReplaysPriorWithoutWorkRerun` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05PreparedCommitRefencesAndRollbackIsDurable` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05SourceAndOriginalResultProofStayFailClosed` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05UnknownStartedNeverRerunsAndSiblingRemainsReady` — NOT_RUN

Both tasks: unchanged root/settings guard, seven nonsecret environment inputs, explicit UR06_LOCAL_ACCEPTANCE=1, one fork, noncache/no up-to-date, no default test skip. No implicit per-test credential or DATABASE_URL injection.

## Main next action / remaining acceptance
1. Bind a clean independent WT to final candidate commit/tree; via original orchestrator compile `:agent:jia-agent-service:compileUr06EnrollMysqlJava` and real ROOT `validateLayering` with this init script. Both currently NOT_RUN for this candidate.
2. After exact D harness readback, create a NEW full C installation/C1-C4/all-format batch. Only if actually accepted, consume that SAME canonical target once in an awaited callback, serial original foundation7 + M4 six. Do not reuse old A/B target or rewrite prior failures.
3. Any actual compiler/SQL/HTTP/cleanup failure returns to this same Owner; no Reviewer/new Agent. Full UR06/Goal and production migration/Phase-B/Rabbit/JWT reassignment/mysqld crash/paid Provider/three live Agents remain unaccepted.

No current concrete need to expand source paths; formal type/SQL/runtime proof is deliberately pending Main. Source-phase delivery is not whole-task completion or release/deployment authorization.
