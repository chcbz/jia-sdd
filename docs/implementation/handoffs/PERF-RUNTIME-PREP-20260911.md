# PERF real-runtime prerequisite admission — 2026-09-11

Current owner/gates remain solely in TASKS.yaml runtime ledger. Continue from accepted tooling `43e0e46f8d9a07797713adb432c3bcab770dd8b0` and API `5571d183fe7c612f2d5ebb272548aa5bfad77e90` / tree `b993a925464701b5a17c93461cf3f558036f5d13`. Existing26 tool tests and6 selected Gradle tests are reused, not rerun.

## Scope and immediate prerequisites

- PERF-CAPTURE-PREP: read-only source architecture packet: exact profile/controller flags, startup dependencies/side effects, safe protected existing Actuator mapping export versus required bounded source, and admission requirements for real isolated full-application startup. No builds/services/credentials/source edits by preparation agent.
- PERF-BUILD-02: ONE offline `:starter:classes` on the accepted clean API integration worktree. This verifies prerequisite full application main-source graph compilation, **not tests, application startup, runtime mapping capture, deploy or performance**. No bootJar/publish/bootRun or test tasks; no new runtime/profile source yet.
- Bound command: JDK `/home/isp/apps/jdk21`; Gradle through `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle` with all orchestration flags before task ID; `--offline --no-daemon --max-workers=1`, JVM `-Xmx384m -XX:MaxMetaspaceSize=256m -Dfile.encoding=UTF-8`, the previously validated **nonsecret** project values `repoUsername=perf-offline`, `repoPassword=perf-offline`, snapshots/releases URLs under `https://example.invalid/`. Only selector changes from already accepted scoped invocation; retain prior build history.
- Dedicated verification-only Sol fallback due to known unavailable primary runner. Query accepted cache first; no blind provider or Gradle retry. Evidence key uses exact API tree + `:starter:classes` + fixture `N/A`. Record actual executed/up-to-date task counts, native exit, compiler failures and resource observations; test count is explicitly NOT_RUN, never test PASS from a classes task.
- Any failure: attribute once and STOP; no source patch by verifier or dependency download. Main freezes a bounded fix after root cause if necessary. No compile source exclusions as a workaround.

## Runtime containment boundary (not yet launch authorization)

Actual application has scheduling/async and many integration dependencies. No `bootRun` or production-profile startup on host merely to read mappings. Before launch, freeze namespace/mount/PID/network isolation, owned writable/fixture directories, sanitized explicit configuration and route-flag parity, external-service local substitutes, deterministic SQL fixture order, exact process ownership and cleanup. A localhost listening port alone does not isolate outgoing integrations or host Unix sockets. Do not exclude controllers/auto-config wholesale or mock MVC and call it real-profile inventory.

Host read-only prerequisite snapshot: unshare/bwrap/ip/docker present; local MySQL and Redis binaries present; ~1.8GB disk and ~1.68GB available RAM. No fixed admission threshold or foreign process/disk cleanup. Root delivery worktree `perf-sdd-20260911` is a docs-only sparse checkout; tooling blobs exist in its accepted commit but physical code should be read/executed from `perf-inventory-20260911` or a separately owned source worktree. Do not disable sparse checkout or restore other worktrees.

Strictly one known-live subagent at a time: finish and explicitly close before admitting the next role. Completed handles have previously disappeared while still consuming slots; no blind overlap attempts.

## Read-only architecture packet (exact API candidate)

Preparation identified existing grey/prod bundles with route-shaping Rabbit-operations and archive-question controllers disabled, scene-state/scene-events/chat-WebSocket enabled, voice environment-controlled/default-off. Effective environment/external-config precedence is **not frozen**; bundled values alone do not establish deployed-profile parity. Non-Controller `/ws/chat` and `/ws/agent/channel`, `/error`, static and management handlers must be represented explicitly.

Hard startup dependencies/side effects: Druid MySQL; Camunda schema update; Agent/Chat schema initializers performing DDL/checks/persona seeds; AgentStatusMonitor, JobExecutor and WxSchedule background work; unconditional SmsReceiver Rabbit listener despite Agent Rabbit flags disabled. Existing starter test schema is not a complete current Agent startup fixture. Do not substitute H2, mocked MVC or host shared DB/socket.

Prefer **no new runtime Java source**: existing Actuator mappings inside strict owned mount/PID/network isolation, only loopback, own MySQL/Redis/files/logs and explicit sanitized config. Keep controller/Bean-shaping flags equivalent to target manifest, record transport-only SSL override and capture-only `/actuator/mappings` difference. Preparation reports current security chain permits `/actuator/**`; namespace isolation remains mandatory and public exposure is NOT authorized. Dump raw mappings once, retain original bytes, separate framework/management unambiguously, bind all outputs to exact source/profile/config provenance. If those mappings cannot be losslessly normalized by accepted tooling, stop and freeze the narrow missing adapter contract; never drop unsupported records.

Missing runtime prerequisites remain explicit: full MySQL startup migration ordering, accepted100Agent/1000Task/persona/scene fixture+digest, effective-config provenance, genuine user OAuth/JWT bootstrap (not machine-token ACL surrogate), tenant/client/case-variant controls, and eager external-client initialization behavior. Next actual execution is prerequisite compilation, not premature app launch.

### Preparation argv corrections before any execution

The preparation packet proposed an unproven fixture digest and used a directory as `--artifact`; neither is authorized. Main contract remains authoritative: `--fixture-digest N/A` for classes-only, `--artifact "$E/gradle.log"` as a **file**. Use accepted previous invocation structure, all orchestrator flags before taskID, no tee/pipeline that could mask native exits, no random wrapper logic. These are pre-execution review corrections, not failed build attempts. No runtime source changes admitted by this packet.

## BUILD-02 prelaunch harness failure / direct-invocation correction

Verifier used `subprocess.run(text=True)` on host Python3.6.8, which rejects that argument before launching even the cache query. Attributed once; no Gradle/task/test ran. Original evidence `/var/tmp/cyf-perf-build-02-iUHpue` is retained. Main directly ran the approved `evidence-get` CLI and observed expected `EVIDENCE_MISS`/native1. This is not a source or dependency failure.

Main authorizes the **same originally planned one actual Gradle invocation**, now by direct shell command with stdout/stderr redirected to a fresh own log, no Python wrapper, no tee/errexit function. Use exact flags already frozen and native exit captured by plain `rc=$?`. Do not rerun cache query unnecessarily (orchestrator checks again inside lock). No source/harness-file repair or memory/dependency/scope expansion. Any actual Gradle failure is attributed before the next action; two-failure stop remains enforced.

## BUILD-02 actual result (R2 independently accepted)

The sole actual offline `:starter:classes` invocation completed native0 in34m14s:80 actionable tasks,75 executed and5 up-to-date. `:starter:compileJava`, `:starter:processResources`, and `:starter:classes` completed. Tests are **NOT_RUN**. Nonfatal annotation/deprecation/unchecked compiler warnings remain warnings, not corrected source. API commit/tree unchanged; verifier reports clean before/after. No runtime artifact, application startup, DB, mapping capture, deployment, or3-second result is claimed.

- Own evidence: `/var/tmp/cyf-perf-build-02-direct-5hxNYn/` (`gradle.log`, `native-exit.txt`, `task-counts.txt`, `source-after.txt`, `orchestrator-receipt.txt`, `sha256sums.txt`).
- LogSHA256: `41fd4f7b993e5049ac652efabb2812dda095d84a5cea6d299e9b598fd5cba88d`.
- Reuse key: `68feb19828d94bf6a65833732ba425be03373f953b8ef1a1ec3123cc87a2618f` (exact API tree + `:starter:classes` + `N/A`).
- Verifier `01a08e7e-a791-7b10-a50b-bb925c352704` finished and explicitly closed before reviewer admission. Independent reviewer `01a08ea6-a605-7d00-8cf6-33e2adfa0518` is read-only; no repeat Gradle.
- Original Python3.6 prelaunch failure stays in the earlier section and original evidence; success does not rewrite that attempt.

### Next bounded runtime prerequisites

Compilation does not supply a runnable sanitized capture artifact. `starter/build.gradle` disables plain `jar`; `bootJar` additionally runs public-artifact verifier tests and checks forbidden embedded configuration/key material. Do not treat `bootJar` as an already-covered classes task, skip those checks, or use build output containing private development resources as a public artifact.

Before admitting any real startup: freeze artifact/classpath provenance, a minimal-mount owned network/PID namespace launcher and negative-containment checks, explicit sanitized profile/route manifest, and complete fresh MySQL/Redis fixture ordering. Fixture sources include starter test schema, Agent main schema, and **Chat test** `chat/jia-chat-mapper/src/test/resources/db/schema.sql`; Chat main schema.sql does not exist. Never run the existing economy verifier against the shared host MySQL socket. The capture-only launcher must fail closed on missing mounts/config/schema provenance, not fall back to host services. Deterministic100Agent/1000Task data and user-principal authentication follow as separately verifiable baseline prerequisites; machine tokens cannot substitute for user ACL tests.

## BUILD-02 R1 evidence rejection / approved metadata-only remediation

Independent reviewer `01a08ea6-a605-7d00-8cf6-33e2adfa0518` confirmed native0, exact clean source, all log hashes,80 actionable75/5, and no executed test/bootJar/bootRun/publish task. R1 nevertheless REJECT0/1/0: the supplied task-owned packet omitted the existing executed-command cache record and orchestrator provenance. Key(tree,selector,fixture) alone does not bind actual argv. This is an evidence-packaging defect, **not a failed compilation**.

| Attempt | Attributed cause | Preserved evidence | Bounded remedy |
| --- | --- | --- | --- |
| Prelaunch | Python3.6 rejects wrapper text=True; zero Gradle starts | `/var/tmp/cyf-perf-build-02-iUHpue/` | Already corrected by direct invocation; do not repeat |
| Review R1 | Successful invocation's stored command omitted from reviewer packet; script hash not captured before execution | `/var/tmp/cyf-perf-build-02-direct-5hxNYn/`, R1 reviewer response | Export only existing own cache record; snapshot/hash current script with explicit **post-run** provenance; no invented pre-run hash |

Two-failure gate was reached and stopped before repair. Main approves **metadata-only** remediation under this matrix: capture existing task-scoped cache record under the evidence lock into a fresh main-owned immutable packet, assert its task/tree/selector/fixture/artifact and exact nonsecret command match the frozen invocation, retain prior evidence hashes, and snapshot current orchestrator bytes for provenance. The later script hash cannot prove historical execution bytes and must not be labeled pre-run or cryptographic launch attestation. Reuse actual execution evidence; no Gradle, source edit, test, DB, runtime, heap change, download, or old evidence overwrite. Independent R2 review must assess that remaining provenance limitation honestly before any acceptance.

### Metadata admission identity correction

First metadata admission used generic owner `main_orchestrator`, which collided with an unrelated active task and was rejected by ledger validation. No foreign task was modified. The shell did not stop after admission failure and still wrote `/var/tmp/cyf-perf-build-02-main-r2-cszgbjfx/`; retain it explicitly as **pre-admission metadata capture**, not an authorized execution or rewritten build receipt. No Gradle/source/runtime was launched. This control failure is attributed separately. Main approves the bounded correction: use task-scoped controller identity `main_orchestrator:PERF-BUILD-02`, then admit read-only review of the existing supplemental packet without repeating export/build. Future gate-dependent commands must be chained with success checks; generic main identity must not be reused across live tasks.

Supplement: `cache-record.json` SHA256 `0ae5245506c189b6237964cb6a0a723e4b4f278697fdcf4ccee599ca93328b56`; `provenance.json` SHA256 `ecce33fadaa62aae2b77148f514f875bd359cf54780f1791ea803406c037fdcf`; current post-run orchestrator SHA256 `191c137740cd77806af8705ade6460e4ed97549ecd30b68272a0a7a01b2f8490`. Stored actual plain-joined command equals the frozen invocation. JVM argv grouping comes from the frozen controller instruction, not a reversible cache encoding. No pre-run script hash exists; this limitation remains explicit.

## Final bounded acceptance

Independent R2 reviewer `01a08ea6-a605-7d00-8cf6-33e2adfa0518` returned **ACCEPT P0/P1/P2=0/0/0** after inspecting the existing-command supplement. Narrow classes evidence is accepted; missing pre-run script hash and non-reversible joined argv remain disclosed limitations, not invented proof. R1/control/prelaunch failures remain above. Reviewer was explicitly closed; no live PERF verifier/reviewer remains. Main promoted BUILD-02 via the orchestrator. No source changes, new tests, deployment, or runtime work occurred in this continuation.

Next executable work package: implement/review a **no-application-launch containment preflight** in a separately owned tooling worktree; verify namespace/mount denial checks and exact artifact/config/fixture inputs before separately authorizing MySQL/Redis/application startup. Full runtime mapping reconciliation and six-hotspot3-second baseline remain pending.

### Documentation verification note

Post-review docs check attempted host Python `import yaml`, which failed because PyYAML is absent before parsing or writing any file. No dependency was installed and no build evidence/gate was changed. Instead, stdlib checks validated the newly added flat YAML supplement's exact indentation, unique keys, counts, NOT_RUN/pending scope, and relative handoff target; this is **not a claimed full YAML parser run**. PERF-only ledger projection passes existing orchestrator schema checks; unrelated branch tasks remain byte-equivalent as parsed data.
