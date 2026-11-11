# Juyi SSE asynchronous authentication — 2026-09-09

## Frozen scope

User requests fixing the misleading failure after a completed private reply. API production/remote baseline is `00681408c4592f1f76eda8eafa554a9191fb0e50`, tree `e15196b94ae289ac85b7210143c5531f5b4f10a5`; installed JAR SHA-256 `cb4284700ebcc344614696063de7ac9f5ad664b4e909ad08d7c4a94b698f3404`. Main API checkout is stale and remains untouched. Runtime state is only in `TASKS.yaml#runtime_ledger_json` under `JY-SSE-ASYNC-AUTH-20260909`.

Sole Writer owns the new `codex/jy-sse-async-auth-20260909` worktree and only:
- `oauth/jia-oauth-resource/src/main/java/cn/jia/oauth/config/ResourceServerConfig.java`
- `oauth/jia-oauth-resource/src/test/java/cn/jia/oauth/config/ResourceServerAsyncSecurityTest.java`

Retain STATELESS, fresh-request JWT validation, session/cookie isolation, and protected ASYNC authorization. No blanket dispatcher `permitAll`, no frontend, DB, Agent client, identity `/resource` semantics, or unrelated edits. Other tasks keep their Gradle leases and runtime custody; no foreign process/evidence operations.

## Diagnosis evidence

The affected private conversation received a full saved Agent reply at 2026-09-09 08:32:59.457; the subsequent dispatch at 08:33:00.260 logged a committed-response error. The original online root exception stack is missing, so occurrence attribution is high-confidence rather than a captured identical stack.

Deployed bytecode confirms NullSecurityContextRepository plus authenticated resource routes including `/chat/**`. An isolated probe using deployed Spring Security jars and a real HttpSecurity-built chain reproduces: authenticated REQUEST -> committed SSE reply -> ASYNC -> AuthorizationDeniedException / response already committed. Changing only to request-attribute security context preserves identity and completes normally, without creating a session. This verifies the configuration defect independently of source-checkout drift.

## Acceptance

1. Actual production resource-chain configuration preserves authenticated identity through committed SSE ASYNC completion.
2. No session is created; fresh missing/invalid/revoked credentials and session-only requests remain denied.
3. Anonymous ASYNC is not granted access; identity `/resource` route keeps its existing contract.
4. Independent read-only review and one exact-tree module test run through the canonical orchestrator. Attribute failures before retry; no repeated full suites for unchanged evidence keys.
5. Immutable SHA-pinned build/release, original runtime-owner coordination, health and anonymous-denial checks. Health alone does not establish a real authenticated private-chat acceptance; no synthesized user credentials or production chat commands.

## Source acceptance

Candidate `9a7d8449cea625f49a4b3a2b0d5c7a4f0d829ba3`, tree `e4668f121038eb8fd631aa34a94bf70b7e312849`: independent Sol review ACCEPT, no P0/P1/P2 findings. General chain changes repository only; identity `/resource` unchanged. Three new tests use actual production config and real SseEmitter committed ASYNC redispatch, plus negative token/session/anonymous-ASYNC cases. The fixture is a GET SseEmitter, not a full production POST Flux/Tomcat/nginx end-to-end claim. Actual module compilation/tests remain required.

## Verification routing failure (not a code/test failure)

The primary `gpt_test_runner` failed before executing any command: provider returned HTTP 502, unknown provider for `gpt-5.4-mini`. No Gradle invocation, test XML, or source failure occurred. Do not retry that model; use a supported independent verifier on the same accepted candidate and retain the original evidence key. This is the first attributed failure for this task, not permission for blind reruns.

## 2026-09-09 14:03 direct recovery snapshot

The preceding wait tool failed to return promptly; user interrupted. Direct read-only inspection finds candidate remains clean at 9a7d8449/e466, no matching Gradle process, and module XML written at 10:15:36: 32 tests, 7 failures, 0 errors/skips. New ResourceServerAsyncSecurityTest passes all 3 cases. All 7 failures are AuthenticationResourceSecurityTest context initialization: duplicate AgentProbeController registration for GET /agent/probe (two bean names, same method). Native Gradle exit receipt has not yet been recovered; XML does not imply module PASS. Production runtime still has original PID/start ticks/JAR SHA.

Root-cause matrix / remediation: (1) prior verifier-provider failure: known unavailable model, do not retry route; (2) current module failure: observed duplicate test-controller mapping, provenance (pre-existing versus new fixture interaction) not yet established; inspect explicit registration/component scanning and baseline source read-only, then authorize a bounded fixture repair by original Writer, independent review, and new-tree orchestrated verification. (3) reporting delay: agent-wait tool remained blocked; use bounded local artifact checks, do not describe tests as running based on stale ledger. Stop automatic test/build/release retries at blocked_root_cause; no production actions authorized by this recovery.

## Bounded remediation and final integration

User resumed; orchestrator authorize-remediation recorded root-cause matrix and replaced unavailable original Writer with Knuth 01a0854b. Baseline006814 and candidate9a7 have byte-identical AuthenticationResourceSecurityTest: duplicate nested @RestController inside @Configuration plus explicit @Bean predates SSE changes. Repair a9f2ee432ed0cc89e7e8b93add4a94374a9ee7d4/treeb871d45a7c46e037168efb0d9a0dd8d57d81cc35 only moves controller outside TestApplication; every assertion and explicit bean retained. No retry before this attributed repair.

Writer merged exact current develop6267f3b16fe7b672a3c8479f058a662d9c75216c/tree936d6e4bcf3d7a4cc23cde62fa0e697be93d659b conflict-free into repair. Final13539ddf688a85c24c1fc56680c167293cc61425/tree911287ecf49ddcab49ae387786877ac7c47f54ea; parents a9f2ee43+6267f3b1. Peer seven paths and our three OAuth paths are disjoint, respective blobs preserved. Frozen new-tree verification pending independent delta review. Peer6267 bootJar currently owns heavy execution; no preemption or production GO.

Own release-input repinned to final13539/911287; Web admission corrected to schema-required PROVISIONAL_DO_NOT_BUILD_OR_DEPLOY (placeholder is not deployed Web identity and API-only task has no Web admission). Accepted b0fc release-tool source unmodified. Runtime actions still require original Owner coordination; old release budget controllers cannot be reused blindly because installed lifecycle/trust contract changed since prior login release.

Independent new Reviewer01a08550 ACCEPT13539/911287: zero P0/P1/P2; baseline duplicate configuration-member registration confirmed; merge-tree equals final tree, every owned-parent blob preserved. Prior verifier Shannon later returned native1 at10:15:44, BUILD FAILED15m9s,18 tasks, clean9a7/e466 before/after; shared evidence /var/tmp/cyf-jy-sse-async-auth-verify-20260909. This closes missing native-exit gap without rerun.

Main's initial new verification wrapper failed before any Gradle invocation because system Python3.6 rejects subprocess text=True. Attributed via fail; changed own wrapper only to universal_newlines=True and new r2 namespace, preserving original script. Candidate unchanged. Unique new module verification submitted16:44:01, orchestrator3847835 queued behind existing peer3831311; receipt/log in own verify-13539ddf688a-r2 directory. No duplicate suite started.

Original runtime Owner Knuth confirms original Main wants6267 release first and SSE next safe window; no parallel runtime controller. Own source includes6267, release input already binds current63a7 before build (schema validation checked). SSE no build/runtime GO yet; next after final-tree module PASS is one immutable bootJar then original-Owner accepted current-contract pin-only release handoff, not preemption of6267.

## Final-tree verification native failure and second bounded matrix

17:03:30 actual13539/911287 native1,32 tests/31PASS/1FAIL,0errors/skips, clean exact source before/after. New SSE3 cases PASS; prior duplicate-registration7 startup failures eliminated. Remaining AuthenticationResourceSecurityTest configuredAgentResourceUsesTheSameAccountGateWithoutSessionOrRequestCache line140 expects stale-token401 but receives200. Its raw AnnotationConfigWebApplicationContext fixture lacks @EnableConfigurationProperties, unlike existing SessionRevocationResourceSecurityTest, EconomyResourceProfileSecurityTest, and new SSE fixture. Without Boot property-binding registration, production ResourceServerConfig's empty resourceUris branch intentionally matches no general route; fixture test route is consequently unprotected. This missing annotation also predates the SSE source change. Runtime source is not to be weakened to satisfy the fixture.

Matrix: wrapper Python3.6 failure was pre-Gradle, attributed/repaired; new actual module failure is a missing configuration-binding fixture prerequsite, observed401/200 mismatch. Fix plan: same scoped original replacement Writer adds Boot configuration-property binding to AuthenticationResourceSecurityTest and a bounded setup guard that proves intended security route/property is active (no relaxed401 assertion). Independent review must inspect whole relevant fixture for additional setup omissions; then exactly one new-tree module verification. Conditional build bridge ended MODULE_NOT_PASS/NO_BUILD_NO_RETRY at17:03:35, no build/deploy occurred. No blind rerun of13539; source-only bounded remediation requires authorize-remediation.

## Second fixture source ACCEPT and new native run

Replacement Writer committed97ae8ef12c0a0306a40a04017f44139e1ca27823/tree9ffcf29061c56eb8135f50c548a8373a0317155c, parent13539. Test-only: @EnableConfigurationProperties plus setup assertion exactly one security chain matches /agent/probe. All existing401 assertions unchanged. Independent Reviewer01a08550 reviewed whole relevant fixture (binding/service/primary decoder/controller/MVC/security/cleanup) and ACCEPT zeroP0/P1/P2; no further setup omission found. This is not yet runtime test PASS.

One new-tree module invocation authorized/submitted17:10:41; own logs/archivedXML/native receipt under verify-97ae8ef12c0a-r2. Prior13539 XML archived with matching SHA manifest before overwrite; native sessions54577 and48252 both consumed exit1, no build occurred. One new conditional bridge only: after exact32PASS/native0/unchangedSHA, accepted b0fc build+artifact verify, no retries/lifecycle. All release pins updated BEFORE build to97ae8/9ffcf/inputaa0959af7f20870db606337a52966cc79ecf84e9044a2e8d90c7e621b7789650, old13539 unbuilt input/controller/log archived. Runtime Owner notified old13539 pins superseded and6267 retains first-window priority.

## 17:21 final module PASS; source promoted, one artifact build executing

Exact97ae8/9ffcf module native0 at17:21:00:32 tests/0failures/errors/skips, new SSE3 and existing authentication7 all PASS, clean exact SHA before/after. Main independently checked all9 archived XML hashes against native receipt84db772c671824126aabb1072aa976c0b8c459c53af07f08a808f7829c23b41e. LogSHA1a061e88bdcd2a7498c657a0da8c1033166705dc1d9611c4f84230cc920c63e7. This resolves both preexisting fixture defects without changing original safety assertions.

Conditional bridge observed receipt/input assertions and launched exactly one b0fc bootJar17:21:08; orchestrator3873873 owns Gradle lock, inputaa0959 remains unchanged. No API lifecycle operation. Source promotion independently fresh-fetched6267, verified ancestor/clean97ae8, nonforce pushed develop and queried remote exact97ae8 native0. This is source promotion, NOT runtime deployment; first6267 runtime window remains original Owner's authorized plan. Original runtime Owner notified new source/test/build status and shared own evidence paths explicitly; no stale13539 build or second runtimecontroller.

## Peer runtime-window abnormality (not an SSE test/build failure)

Original runtime Owner shared reserve-blocked attribution b9868ef6c88ea985e1202e066bd7e856e0529285be519d68153acda31cd74513: peer6267 reserve rc1/Stop, no stop/start/deploy, no newbudget, attempts0/3, oldPID3317276 unchanged; maintenance true retained under original custody. Request-to-terminal32seconds and later stateSHA drift observed, exact failed point not captured. No completed-release notice sent. This Main recorded conflict-alert only, no peer-process/monitor/control operations. Original Main must authorize its exact Owner's bounded fresh continuous submission or maintenance handback; SSE build continues independently, runtime still NOT admitted. Independent small-evidence verifier Shannon01a083da monitors own existing one build only, no extra Gradle/JAR scans.

## 17:54 immutable artifact PASS and independent evidence ACCEPT

One bootJar native0,31m52s,193 tasks(180 executed/13UP-TO-DATE), followed by canonical artifact verification native0; bridge native0 at17:54:09, no deployment. Artifact587a2ffd1d220cc60cee0cbd5a5163f26df68d490cd527189c922a71d9c688d6; metadataa10f7dc666fb357884a28dae703004aff4c5f189cacc4ff0441414037f352595; inputaa0959; tool digest2e6c6500ccc8830b56e41374fd413ab66d99b42c637e0f850896b6e5b89942fb. All immutable artifact files are under own artifacts/api, no input rebinding or metadata derivation.

Independent Shannon01a083da ACCEPT: all four native exits0, exact97ae8/9ffcf/inputaa0959, receipt84db and9archivedXML hashes/counts checked,32/32PASS, actual VERIFY_RELEASE=PASS. Does not authorize deployment.

Optional main bytecode probe initially matched both legitimate resource and resource-starter JAR names by broad prefix; attributed as inspector-selection defect, not artifact corruption, and archived old inspector. Corrected small probe examines exact ResourceServerConfig.class presence and finds one defining JAR: BOOT-INF/lib/jia-oauth-resource-1.1.2-SNAPSHOT.jar. Actual classSHA b1d385e9b3706634447cf9850ddee4fedb0f8aa59f733ab732fa1b4b8eac4b7d is byte-identical to tested workspace compiled class, contains RequestAttribute/Null/STATELESS references; neither test fixture is shipped. Probe PASS without rebuilding/retesting or fullJAR reread.

Original runtime Owner received full real source/input/artifact/metadata pins and explicitly shared own evidence root. Requested current6267 window disposition (combine only if originalMain permits and no in-flight action), then unique originalOwner next-window pin-only PREP and independent delta review. No parallel controller, no own API/monitor operations, no runtimeGO yet. Current stage awaiting_release_window, source/test/build accepted; actual user-authenticated LinChong chat still not exercised.

## 18:08 coordination correction: shared W14 now owns the combined SSE release

An attempted new SSE release-prep owner transition was atomically denied (invalid writer-gate label and originalAgent already W14 owner). No ownership/runtime state changed; alert-only recorded. Immediately reading shared remaining-release§48 and currentW14 ledger establishes that original Main has ALREADY adopted the SAME97ae8/9ffcf/JAR587a combined target, independently checked26refs/32XML/Git ancestor/current immutable artifact, and issued ONE reviewed runtimeGO on controller66c3/samecall6f084/plan3210/inputaa0959. Original6267 failed window maintenance was actually handed back at17:54 with zero lifecycle. Thus requesting a second Owner/controller is unnecessary, NOT a continuing release blocker.

SSE now awaits the combined W14 native outcome under the exact originalOwner. Keep W14 authority intact, no extra handoff/pin review/build or runtime GO from this Main. Required closing proof remains actualCOMMITTED + deployed587a/newPID/health + monitor/budgethandback; approved plan/GO alone is not deployment. The preceding18:08 next_action demanding Owner release is superseded by this verified combined-release fact.
