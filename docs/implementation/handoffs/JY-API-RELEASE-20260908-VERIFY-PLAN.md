# JY API release verification plan — 2026-09-08

## Boundary and exact candidate

Preparation only for `JY-UNBIND-ARCHIVE-API-20260908`: API `f2fb244e56439b79515add48fe3a987ccda9b462`, tree `91be8e6cdd1042bfaddf36a90f83c17eed4ef42b`, clean worktree `/home/isp/wsps/cyf/.worktrees/jy-unbind-archive-api-20260908`. Source review remains independent `ACCEPT`; R3 remains rc124/0 XML, not PASS. No Gradle, build, DB, service, process control, deployment, or production DML was run during this preparation. DeepSeek remains disabled.

Frozen behavior is unchanged: `POST /agent/roster`, `DELETE /agent/personas/{personaCode}/bind`, and existing archive reader APIs; no new endpoint/event/schema/migration. Unbind lock order remains binding -> hosted profile -> runtime -> exact-scope durable task row, all before mutation; binding/identity/runtime CAS changes remain one rollback transaction. Offline status publication remains after commit and revalidates a detached runtime in a new read-only transaction. Runtime clear allowlist remains client/owner/persona/binding/endpoint/token/task/error fields plus offline timestamps; no sensitive payload is logged or published. Archive caches only bounded block metadata for 30 seconds and rechecks the active edition every request.

## Bounded diagnosis

- R3 ran 16:34:01–16:44:02 +08:00. Offline configuration passed; the log contains warnings but no dependency-resolution error, compiler error, OOM, or assertion failure.
- Preserved outputs prove forward compilation: common-core first class at 16:41:12 (+431s), then agent-core, common-api, agent-api; common-mapper completed at 16:44:05 during termination lag. There are 339 compiled class files and incremental `previous-compilation-data.bin` for all five modules, but no selected test XML.
- Local runtime is `/home/isp/apps/jdk21/bin/java`, Oracle GraalVM/JDK `21.0.8`, two processors, 1.7 GiB memory available at observation. Root settings configure 47 subprojects plus eager publishing credentials; the exact pre-first-class time is not attributable from the old log.
- Classification: evidence is consistent with a cold/configuration-heavy compile followed by normal compiler progress, not a proven compiler/dependency defect. The remaining uncertainty is bounded to the pre-first-task/configuration and next unfinished task; the new hook makes both explicit.

Static evidence: `/var/tmp/cyf-jy-api-release-20260908/static-diagnosis.json`.

## Frozen acceptance -> selector coverage

| Acceptance | Exact selector |
| --- | --- |
| Active exact-owner roster filtering occurs before pagination; PageInfo metadata survives DTO conversion | `AgentRuntimeMapperContractTest`, `AgentServiceImplTest` |
| Runtime detach is exact CAS, clears the frozen field allowlist, and fails closed on concurrent drift | `AgentRuntimeMapperContractTest`, `AgentHostedBindingTransactionTest` |
| Unbind denies projected or durable active work under exact scope/lock order before mutation | `AgentTaskMetaScopedDaoTest`, `AgentHostedBindingTransactionTest` |
| Rollback emits no status; after-commit publication distinguishes bound from detached/rebound runtime | `AgentHostedBindingTransactionTest` |
| Archive catalog rechecks active edition while caching only bounded block metadata | `ArchiveReaderServiceTest` |

The verification selector remains byte-for-byte the R3 five-class selector; no broader suite or DB fixture is introduced.

## GO-only execution phases

1. **Main admission:** ledger must assign this exact tree to a writer/verifier at a Gradle gate. Main sets the exact one-shot token printed by `verify-5selectors.sh`. Without it the script exits 68 before Gradle.
2. **VERIFY5, one attempt:** run `/var/tmp/cyf-jy-api-release-20260908/verify-5selectors.sh`. It preserves R3 incremental outputs (and refuses if they disappeared), stays `--offline`, uses the same 600-second deadline/JVM/worker bounds and exact five selectors, and adds only `--info`, plain console, and read-only `/var/tmp/cyf-jy-api-release-20260908/phase-timing.init.gradle`. The hook emits settings/projects/task-graph/task start/end durations; it neither changes dependencies nor the task graph.
3. **VERIFY5 pass gate:** require native rc0, unchanged HEAD/tree/clean state, all five XML files present, total tests >0, failures=0, errors=0. Receipt/log are written once under `/var/tmp/cyf-jy-api-release-20260908/`; no overwrite or automatic retry.
4. **Failure stop:** rc124 or any native failure stops before build/deploy. Attribute once through the orchestrator using the receipt. The last unmatched `CYF_PHASE TASK_START`, or time before `TASK_GRAPH_READY`, identifies configuration vs exact compile/test task. Do not extend the timeout, clean outputs, or retry unchanged.
5. **BOOTJAR only after VERIFY5 PASS:** main creates a release input compatible with accepted tool commit `c40805e6d6e9294574beef656402cb0ebbaf4437`, pinning this worktree/ref/head/tree, `gradleTask=:starter:bootJar`, `jarRelativePath=starter/build/libs/starter-1.1.2-SNAPSHOT.jar`, and canonical orchestrator metadata. Main then runs the accepted shared `ops/release/build-api.sh`; external phase timestamps should bracket that command. Do not run a second ad-hoc bootJar.
6. **Artifact/release custody:** main runs accepted `verify-release.sh`, then Knuth/main retains dry-run/deploy/health/rollback custody. This plan does not authorize service control, production deployment, historical Huyanzhuo DML, or endpoint performance claims.

## Pipeline compatibility note / residual risk

Accepted `build-api.sh` already serializes bootJar through the orchestrator and emits immutable artifact metadata, but its Gradle argv uses `--no-build-cache` and does not include `--offline`, `--info`, or this timing hook. Main must explicitly accept that input/metadata/egress difference or arrange a separately reviewed pipeline delta; this preparation does not modify the accepted release tools. BootJar also runs `publicArtifactVerifierTest` and the public-JAR verifier by build contract. No MySQL/concurrency runtime evidence or post-deploy latency evidence exists yet.

## Stopped-loop dependency/complete-compilation remediation — prepared 2026-09-08, not authorized

The second verification terminated natively with rc1 at 17:26:41 +08:00 after 9m39s, before the deadline: 11 tasks executed, all five XMLs absent, source unchanged. The exact failure is `:common:jia-common-test:compileJava` dependency resolution for `org.apiguardian:apiguardian-api:1.1.2`: no cached version was available in offline mode. This is a dependency-cache miss, **not a timeout**, compiler-source error, OOM, test failure, cron deletion, or production-runtime failure. Main records the second failure and stopped-loop attribution before any remediation.

Current own-log proof also invalidates the earlier reuse premise: configuration consumed about 212 seconds, common-core about 90.9 seconds, and Gradle explicitly deleted retained `previous-compilation-data.bin` and classes as stale while traversing a measured 125-task graph. Filesystem presence was not Gradle reuse evidence. Repeating the offline 600-second invocation cannot resolve the missing artifact; merely extending that unchanged command would waste compilation and fail at the same dependency boundary. The 2700-second envelope is separately justified by 11 tasks already consuming 9m39s against the 125-task graph, not by relabeling the native failure as a timeout.

Prepared script: `/var/tmp/cyf-jy-api-release-20260908/verify-5selectors-complete.sh`. It is a surgical derivative of the accepted verifier with only these execution changes:

- own never-overwritten outputs `verify-5selectors-complete.log` and `verify-5selectors-complete-receipt.json`;
- distinct exact GO suffix `VERIFY5COMPLETE`;
- removes the invalid retained-output presence prerequisite but performs no clean/deletion;
- removes **only** `--offline`, allowing normal dependency resolution through the repository configuration already frozen in the exact source/build; it adds no repository URL/init repository, `--refresh-dependencies`, publication task, real credential lookup, secret, or publishing action;
- uses the existing approved API build envelope of 2700 seconds with TERM plus 15-second kill-after cleanup so the measured dependency graph can complete;
- keeps exact tree, exact five selectors, JDK 21, worker 1, 384 MiB heap, 192 MiB metaspace, inert publisher properties, global orchestrator lock, `--info`, XML/source guards, and the byte-unchanged timing hook.

Execution remains forbidden until the native failure receipt/root matrix is final, an independent reviewer accepts this exact delta, and main assigns a fresh exact GO/Gradle gate. This is one reviewed stopped-loop remediation attempt, not permission for any subsequent retry. Any terminal failure stops before bootJar/deploy and is attributed from the phase log. PASS requires unchanged source and all five XMLs with each selected class tests >0, aggregate failures/errors/skipped=0, before the accepted bootJar pipeline.

## Test-only R2 candidate and complete evidence run — prepared 2026-09-08, not authorized

VERIFY5_COMPLETE reached tests and terminated native rc1 at 17:47:01 +08:00: 9 tests, 1 failure, 0 errors/skips. `AgentRuntimeMapperContractTest` ran 2 tests with one false-positive assertion; `AgentTaskMetaScopedDaoTest` ran 7/7 PASS; the three later selected classes did not run. The assertion `set.contains("name = null")` incorrectly matched the required `persona_name = null`; production SQL preserves the independent `name` column and remains unchanged.

Source-only correction commit `74dde4fe44f7ec50e3e513ab05215c4b08602056`, tree `c400dc3121c441c526c09e102535964e546e3dce`, changes only `AgentRuntimeMapperContractTest.java`. It parses comma-delimited SET assignments and tests the exact left-hand column name for `name`, `abilities`, and `tenant_id`; the existing positive assertion still requires `persona_name = null`. No production `src/main` byte changed, so the independent product-source ACCEPT remains reusable subject to reviewer confirmation.

Prepared verifier `/var/tmp/cyf-jy-api-release-20260908/verify-5selectors-complete-r2.sh` is pinned to the new commit/tree and is not execution authority. Differences from the reviewed complete verifier are limited to:

- fresh never-overwritten R2 log/receipt and exact `VERIFY5COMPLETER2` GO token;
- requires sealed prior-XML manifest `/var/tmp/cyf-jy-api-release-20260908/verify5-complete-failed-xml/manifest.json` at SHA-256 `2de4e0aecac4e6f9a3b9dd90d7067748026aa8b108e205ff6534ec160788cac7`;
- accepts the existing first two XMLs only when both live files and sealed archive copies match their manifest hashes; it neither deletes nor relabels them, and requires the later three XMLs absent before execution;
- adds only Gradle `--continue` for the same exact five requested selectors, so a further assertion failure can still yield bounded evidence from independent later test tasks; native rc0 remains mandatory;
- final gate requires every one of the five XMLs present with per-class tests >0 and failures/errors/skipped=0, plus unchanged clean source;
- retains configured dependency resolution, 2700+15-second envelope, JDK 21, 384 MiB, worker 1, global orchestrator, exact timing hook bytes, and no broad tests/build/DB/runtime/deployment.

Main must first record the current failure, bind the new pins/input and evidence namespace, obtain independent review, and issue a fresh exact GO. No Gradle or bootJar is authorized by this preparation.
