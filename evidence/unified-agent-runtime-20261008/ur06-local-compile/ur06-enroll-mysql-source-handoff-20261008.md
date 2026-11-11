# UR06 enrollment/MySQL source handoff — 2026-10-08 21:27 Asia/Shanghai

## Actual state
- Same original Turing Writer, UR06 four-path source phase only; no Reviewer.
- WT: `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008`; branch `codex/ur06-enroll-mysql-20261008`.
- Baseline `fcac494a5103a7bc1175c96e9df50d2fcc35c182` / tree `6a21c9e61539268d20514db8f80c02f8ce23b043` preserved.
- Candidate `732558494ee082413f8f8e30ad448cc3c6fb7bbc` / tree `95e5409268f9aaee871c3e6d812c3ad61722fbc7`. Task branch push succeeded; `ls-remote` exact SHA matched; worktree clean.
- Exactly four new files, no production/UR03/UR04/build.gradle/client/rootdoc changes. No more source writes planned absent precise formal diagnosis.
- No Gradle/javac/formal compilation, MySQL start, package install, Flow, service/production operations performed. Not claimed compilable or accepted based on grammar alone.

## Owned files / SHA-256
- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java` — `3b361a8bd055be3c07d53c7c311b3bb95b90728690218d7a2f93d2c392df6220`
- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java` — `2974ac2c004f28b5f046f2453ec760cea1259244b2fb6d847cebff770be6b7a7`
- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs` — `f595ed8725d170c193ec087597d2bc3e19fbed5db692c70d941426dd71874bde`
- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle` — `67f3c4ebf0830c5f3225f02931bf4b202393fce2a2b515f4378e575591f433ad`

## Implementation
- Original proxied create(PENDING), original enroll(secret CAS), exact nested JsonResult.data record; original installed RuntimeV1Client default fetch, private authorization file and attempt marker. Wrong/expired/subject/manifest denial, two real concurrent row-lock contenders, replay denial, held-after-commit response followed by exact owned API JVM death and fresh Node/JVM recovery without replay.
- Genuine original engine/executor/WS/registration observer and real supplied Codex CLI version readiness probe, never synthetic version or ready Supplier. No model command dispatch/Provider. Persisted actual session verifier checked privately against actual current proof. A/B JVM restart keeps same MySQL, independent JDBC durability, stale native/WS proof rejection and sibling positive.
- Private actual MySQL8.0.21 binary --no-defaults first for version/init/server. Fresh0700 root/datadir; loopback non3306/33060; mysqlx disabled; owned socket/pid/errorlog/files. Root setup only fixture schema/principal, no global grants to child. Random credentials only inherited private pipes/memory, not args/env/report. Exact pid/start/binary/args/inodes plus real server version/port/datadir/bind/log flags/socket/pidfile verified before JDBC execute/batch/commit. STOP/crash uses only owned exact handles, drains/host/Java/MySQL awaited, cleanup no symlink following.
- Original full agent baseline resource plus full original AgentSchemaInitializer, original user test baseline/security upgrade, original RuntimeV1/fence/transport initializers. Repeat full AgentSchemaInitializer and the three runtime/transport initializers, compare actual full catalog/index/CHECK/trigger/engine/collation fingerprints and legacy NULL-fence row. Real metadata and negative unique/CHECK DML rollbacks; genuine independent JDBC row lock wait observed via own administrative information_schema.innodb_trx.
- Genuine original D06 service/Recovery DAO/mapper transactions; exact ADVANCED/PRIOR statuses and versions8/9/10, first null then [8,8,9,10] last-confirmed request fields, session rotation/reconnect, revoke401 and sibling ACK/ready; malformed version and HASH/LEASE/MESSAGE source denials keep rows/version unchanged. No Rabbit broker publishing/dispatch.
- Native positive transport probe uses existing GET E05 result-commit with syntactically valid missing IDs. Exact source trace: runtime filter → original withNativeFence → real ResultCommit.readRuntimeResult → real withRuntimeResultSource → real owner-scoped locked task root; nonexistent task raises original NOT_FOUND before reassignment lookup, Controller maps404/no-store. Thus no synthetic E05 receipt or new endpoint/table is needed for this missing-result probe; full M4 remains separate.
- UR04 compilation feedback reflected only here: explicit cn.jia.agent.event.AgentEventPublisher import; actual Spring7 ContentCachingRequestWrapper(request,0). Read-only local javap confirms nonpositive cache limit becomes null/no truncation, no arbitrary cache size gate. Empty GET body and non-JSON container failures observed without JSON parsing masking real status.
- Full7594/0827/285/3594240/f4dcd source archive/tree/mode/full artifact inventory/internal links/C1-C4/local buildId/Node20.20.2 proof readback before and after consumption. Artifact not copied/retained. No fake Flow identity.

## Exact execution entry (main only; not executed)
- Init: agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle
- Explicit Gradle task :agent:jia-agent-service:ur06EnrollMysql; source compile task :agent:jia-agent-service:compileUr06EnrollMysqlJava.
- Unique opt-in UR06_LOCAL_ACCEPTANCE=1; seven nonsecret launcher inputs: UR06_API_COMMIT, UR06_CLIENT_ROOT, UR06_CLIENT_COMMIT, UR06_NODE_BIN, UR06_ARTIFACT_ROOT, UR06_MYSQLD_BIN, UR06_CODEX_BIN. Only seven whitelisted inputs passed to JUnit; Node/Java private child env separately allowlisted, no datasource/Provider/SCM/Flow credentials. Runtime secrets private pipe only.
- Actual full installed artifact from same awaited callback after real four C PASS required. Do not launch these selectors on source archive or install target after callback cleanup. Main currently owns other actual live run; no changes made to its session/config.
- Class selector cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest. All seven method selectors below NOT_RUN:
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e1OriginalPendingEnrollNestedCredentialDurability` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e2RealNativeRegistrationSeparateJvmGenerationAndSibling` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e3WrongExpiredManifestAndSubjectDeniedWithoutConsumption` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e4IndependentStateConcurrentSecretCasAndReplayDenial` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e5RealCommittedResponseLossRestartNeverReplaysSecret` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.m1OriginalMysqlInitializersRepeatNullableFenceAndConstraints` — NOT_RUN
- `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.m3NativeCurrentFenceD06ReceiptsRevocationAndSiblingIsolation` — NOT_RUN

## Concrete dependencies / source findings (not runtime results)
1. Genuine Codex CLI: original7594 engine only admits commandAdapterReady after actual codexBin --version returns matching codex-cli version. Runtime artifact contains no Codex CLI. Main must supply canonical real UR06_CODEX_BIN (added within contract's “at least” nonsecret whitelist); no fake codex-cli0.0.0, Node masquerade, appserver or Provider. Already notified09f8527f.
2. Known baseline/initializer conflict: original agent/jia-agent-mapper/src/main/resources/db/schema.sql:871 includes chk_hosted_single_tenant along with state/generation/repair. AgentSchemaInitializer:236-255 strictly expects only3 CHECKs. Full fresh baseline then original initializer is statically incompatible. Fixture does not delete constraints, clone reduced tables, reflect-call only a private sub-initializer or bypass checks. Notification34f386be sent to main/original schema Owner. Safe child reason HOSTED_CHECK_SET_DRIFT added without raw messages. Needs original source contract resolution before a meaningful full boot run; do not blindly retry fcac.
3. Original ACK HTTP rejection gap: AgentCommandAckServiceImpl throws AgentCommandAckRejectedException for source/hash/lease failures; AgentRuntimeV1Controller handles only AgentBizException/IllegalArgumentException, runtime filter lets downstream exceptions propagate. Likely500 instead of required403 for M3 source negatives; NOT_RUN static finding, notified09f8527f. Assertions remain exact403, no fake fixture advice/no production edits. Node now preserves observed500 rather than disguising as0. Resolve with original API Owner if confirmed.
4. Original user test baseline defines account_state without ascii/ascii_bin; original additive security upgrade preserves existing columns and returns a nonzero definition validation SELECT. ResourceDatabasePopulator does not assert SELECT values. Fixture uses that original baseline per Curie seam and does NOT claim full account-security migration certification; its actual account DAO/auth checks remain real. No user column rewrite or production migration here. If main requires foundation DDL validation as prerequisite, exact original user test baseline/upgrade contract needs its Owner, not hidden alteration of this fixture.

## Selfcheck evidence / limits
- node --check of the owned mjs PASS.
- Two owned Java files tree-sitter grammar PASS, Java string illegal-escape scan PASS, Map.of overload arity scan PASS. These are NOT compile/typecheck or Owner runtime results.
- git diff --cached --check PASS before commit; exact four paths PASS; baseline+candidate+remote+clean readback PASS.
- Seven selectors, E1-E5/M1-M3 runtime assertions, original init/schema guards and D06 provenance retained; formal test count0.
- M4 genuine MySQL full E05 NOT_RUN / not implemented in this four-file source phase. Original UR04 full six E05 goals not replaced; production three-Agent, Provider, Rabbit and overall UR06/Goal completion not claimed.
- Next: main freeze/cherry candidate and resolve concrete original source prerequisites, then compile/run via orchestrator in next real same-target callback; route precise failures back to same original Owner. No Reviewer or repeated broad investigation requested.
