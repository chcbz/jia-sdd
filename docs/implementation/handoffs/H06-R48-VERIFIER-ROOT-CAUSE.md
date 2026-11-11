# H06 R48 focused-verifier root-cause matrix

Date: 2026-08-29 CST

Exact API candidate: `66f30bc530f9dc2c96960998bc9e089d1220eed7` / tree `56cc82235e51409bea320c3f4cf931448267a366`.

| Attempt | Failure | Root cause | Authorized remediation |
|---|---|---|---|
| 1 | Root build evaluation failed before compile because `repoUsername/repoPassword` were absent | Root publishing configuration eagerly reads those project properties for every task | Supply non-sensitive placeholder project properties; no source change |
| 2 | Offline configuration failed resolving Spring Boot Gradle plugin `4.0.1` | Host cache lacks the plugin marker/artifact required while evaluating `starter` | One persistent static-systemd online hydration/focused run through the official init, followed by an offline exact-tree rerun; do not use an Agent-attached Gradle client |

Authorized verifier contract:

- task-owned non-transient static systemd service, PPID 1, no `PrivateTmp`, global `/tmp/cyf-gradle.lock` visible;
- exact HEAD/tree/clean, official init SHA-256 `118a0a9ff38ba99be8afcee5e26a4626790413e4ebaa32011a3ee62915e5c4a4`, and >=5 GiB free-space gate before start;
- one bounded online `ArchiveContentImporterTest` hydration/execution, then the same selector offline for authoritative evidence;
- the real-MySQL selector may run only if its fixture is self-contained and isolated; otherwise stop and report the required fixture contract;
- each step has a separate log, SHA and terminal marker; first failure stops; no source edits, full H06 runtime, runner-pin update, shared DB operation, production action, or credential output.

## Static verifier attempt 1 — orchestrator argument order (2026-08-29 13:56 CST)

- Unit: `cyf-h06-r48-focused-verifier.service`
- Exact commit/tree: `66f30bc530f9dc2c96960998bc9e089d1220eed7` / `56cc82235e51409bea320c3f4cf931448267a366`
- Preflight PASS: clean tree, PPID=1, exact init digest, 5,432,918,016 bytes available.
- Terminal: FAIL before Gradle/lock/test; online log SHA-256 `6226ef241a74805c19af12fb80259a31a0edcac0c1c415ed0b2bd72c71a3e64b`.
- Root cause: `gradle` uses an argparse `REMAINDER` positional. Putting task id `H06` before orchestrator options caused all later options to be consumed as the Gradle command; required `--tree-sha`, `--selector`, and `--fixture-digest` were therefore absent.
- Bounded remediation: preserve the failed unit/evidence, create a new non-overwriting static unit/evidence root, place all orchestrator options before task id `H06`, syntax-check with a non-executing parser probe, then perform exactly one online focused hydration followed by one offline authoritative selector. First failure stops; no MySQL/full runtime/pin update.

## Static verifier attempt 2 — disk admission drift (2026-08-29 14:05 CST)

- Corrected argparse construction probe PASS; Gradle was not started.
- Available bytes: `5,322,428,416`; required: `5,368,709,120`; deficit: `46,280,704`.
- Root cause: an independent Web R8 build regenerated its ignored `dist/` output between attempt-1 and attempt-2, consuming about 106 MiB and moving the host below the unchanged 5 GiB admission threshold.
- Remediation performed by the main controller: after confirming no Web build process/open use and that `dist/` was Git-ignored and untracked, safely removed only `/home/isp/wsps/cyf/.worktrees/pwa-integration-web-rc-r4/dist`, releasing `106,176,512` bytes. Source, `node_modules`, evidence, sealed artifacts, Gradle caches, and H06 runtime roots were not removed.
- Attempt 3 is permitted only against a new static unit/evidence root, unchanged exact tree/init/parser order, and a fresh 5 GiB preflight. First subsequent failure stops.

## Static verifier attempt 3 — ledger Gradle-gate mismatch (2026-08-29 14:17 CST)

- New static unit/evidence root and exact/disk/parser preflight PASS; free bytes `5,416,960,000`.
- Orchestrator denied before lock/Gradle: `only this task's writer/verifier at a verification gate may run`.
- Root cause: `authorize-remediation` intentionally set H06 to `remediating`, while `gradle_guard` admits only `targeted_verification` or `verifying`; the controller did not perform the required post-remediation gate transition before starting the static unit.
- Bounded remediation: preserve attempt-3 evidence, transition the same exact owner/tree to `targeted_verification`, then create a new non-overwriting attempt-4 unit/evidence root. No source/init/selector change; first failure stops.

## Static verifier attempt 4 — detached Java environment (2026-08-29 14:23 CST)

- Static exact/parser/disk/targeted-verification preflight PASS; global Gradle lock was acquired.
- Gradle wrapper exited before configuration/tests: `JAVA_HOME is not set and no 'java' command could be found in your PATH`.
- Root cause: the host JDK is installed at `/home/isp/apps/jdk21`, but the detached systemd unit inherited only `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin`; unlike the full H06 runner, the focused wrapper/unit did not pin `JAVA_HOME` and prepend the JDK `bin` path.
- Pinned runtime: GraalVM Java 21.0.8, `/home/isp/apps/jdk21/bin/java`, SHA-256 `8cbb4d3a55f0963be02392f8667ef62a51f7cfc68ca81689c83d2f1f4245892d`.
- Bounded remediation: preserve attempt-4 evidence; complete the required root-cause stop; create a new static unit/evidence root that pins `JAVA_HOME=/home/isp/apps/jdk21` and `PATH=/home/isp/apps/jdk21/bin:/usr/local/bin:/usr/bin:/bin`, verifies the Java binary digest/version before Gradle, and otherwise keeps the exact tree/init/selector contract unchanged.

## Static verifier attempt 5 — private OpenCV coordinate not in public repositories (2026-08-29 14:35 CST)

- Exact/parser/gate/JDK/disk/PPID preflight PASS; Gradle lock acquired; Java compile began.
- First build failure: `:common:jia-common-core:compileJava` cannot resolve `org.opencv:opencv:4.5.5` from Maven Local or Maven Central; tests did not start.
- The immutable digest-bound H06 Gradle seed already contains the exact coordinate:
  - seed: `/var/tmp/cyf-h06-gradle-seed-b595a8e4207fbf27e5a57219c05c946f1f5509af34be9edea58d0c6e2bb68092`
  - POM SHA-256: `786de45db6266b338faf603d0555bdb491357aeece0f9608c3a08d78700dc203`
  - JAR SHA-256: `323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4`
  - source is root-owned, mode `0444`, under root-owned read-only seed directories.
- Root cause: the focused hydration init exposed only Maven Local/Central and did not project the already-approved private seed coordinate into a Maven-layout repository. This is verifier repository wiring, not product source failure.
- Bounded remediation: preserve attempt-5 evidence; create a new root-owned non-overwriting local Maven projection containing only the pinned POM/JAR via same-filesystem hardlinks or reflinks; verify source-before/source-after and projection digests; create a new init script that prepends this file repository before Maven Local/Central for project/buildscript/plugin resolution; run attempt 6 on the unchanged exact tree/JDK/gate. First failure stops.

## Static verifier attempt 6 — controller setup telemetry variable (2026-08-29 14:56 CST)

- The pinned OpenCV projection was created successfully and remains immutable:
  - repo `/var/tmp/cyf-h06-r48-opencv-maven-attempt6`
  - POM/JAR hashes match the seed; hardlink count 2; directories `0555`, files `0444`, root-owned.
  - init `/var/tmp/cyf-h06-r48-opencv-attempt6.init.gradle`, SHA-256 `fff892c9532c6e9d1711e4174bdc4f94665a46649592ce27319c36dc8b6f1a77`, prepends the projection for plugin/dependency/buildscript/project repositories.
- Unit was installed but never started. The outer setup shell exited under `set -u` while recording final disk telemetry because it referenced undefined local variable `WT` instead of the already-defined exact worktree variable.
- No Gradle lock/process/test was started; source/projection/init remained unchanged.
- Bounded remediation: complete root-cause stop, reuse the verified immutable projection/init, correct only the controller setup telemetry variable, and start a new non-overwriting attempt-7 static unit/evidence root. First failure stops.

## Static verifier attempt 7 — legacy JAI coordinates absent from Maven Central (2026-08-29 15:42 CST)

- Unit `cyf-h06-r48-focused-verifier-attempt7.service` passed exact HEAD/tree, clean worktree, parser order, Java 21.0.8, PPID=1, immutable OpenCV projection, and startup free-space `5,384,425,472` bytes.
- Online compile acquired the global Gradle lock and reached `:common:jia-common-core:compileJava`; it failed before tests because Maven Central does not serve `com.sun.media:jai_imageio:1.1` or `javax.media:jai_core:1.1.3`.
- Tests executed: `0`; offline authoritative step was not run; lock and Gradle processes were released.
- Evidence root: `/var/tmp/cyf-h06-r48-focused-verifier-attempt7`; online log SHA-256 `ce56c8429b19cac26c3cdcac45200200261f92c6b1eb0f901d33985289394b24`; terminal SHA-256 `b0581a62a3cf5826f91bf70a9bb9d40a860b784af460e04c1498812714e3bb54`; manifest SHA-256 `8458d9b9e5c05939256b25b137722eaedfed94fe3f1b6586d97f5be84fc64870`.
- Root cause: the projection contained only OpenCV. The approved immutable H06 seed contains exact JAI POM/JAR artifacts, but they were not projected into the verifier repository.
- Bounded remediation: preserve attempt-7 evidence; construct a new root-owned read-only Maven-layout projection containing only exact OpenCV plus the two JAI coordinates, verify source-before/source-after and projection digests, retain the same exact source tree/JDK/selector/5 GiB gate, and run one new non-overwriting static attempt. First failure stops.

## Static verifier attempt 8 — authorized prepared state (2026-08-29 17:42 CST)

- Static unit `cyf-h06-r48-focused-verifier-attempt8.service` is installed and remained inactive during preparation.
- Wrapper SHA-256: `75dbaaf76bb988b122a35ac8b0332617bf1c71219d8aedab49622b61d3990f55`.
- Unit SHA-256: `93b09619c7e6fdaaad320507acb051622d171fdaa2eb0c5b69cca345fd31d6fc`.
- Init SHA-256: `addba213c77be7507dd8be60c1ff7106b5e270e8950b739eb6976b3a8a52225f`.
- Projection digest: `61fc0ecff2cc56043c20de36b1d0dab7cb5d77c230d37bdf5443833a8da0ebc0`; six exact POM/JAR files; root-owned read-only hardlinks; seed before/after manifests byte-identical.
- Parser construction and validation PASS; Gradle was not started during preparation.
- Main controller safely removed only the completed, clean, ignored and process-unreferenced Web R10 `node_modules`, releasing `190,355,376` bytes. Evidence: `/var/tmp/cyf-controller-space-release-web-node-modules-20260829T1737`, evidence file SHA-256 `d51130ed6bf4cbcc1e64ae18926a97f4eab364602c4e53f05a51522695f3f494`.
- Fresh available space before authorization: greater than `5,368,709,120` bytes. Attempt 8 may start only after H06 is transitioned to `targeted_verification` with the exact verifier owner/tree; first failure stops.

### Attempt 8 terminal — detached parser tool absent

- The static unit started with MainPID `1228870`, PPID `1`, and reached only the non-executing parser validation.
- It stopped before Gradle, lock acquisition, compile, or tests because line 102 invoked `rg`, while the intentionally pinned detached PATH contains only the JDK and standard system directories.
- Terminal: `FAIL CODE=34 DETAIL=parser_construction_invalid`; tests `0`; product source and immutable projection/init unchanged.
- This is the second consecutive post-authorization verifier failure, so H06 entered `blocked_root_cause` and no blind retry is permitted.
- Authorized attempt-9 remediation is strictly limited to replacing the `rg` parser assertion with absolute `/usr/bin/grep -E` (or an equivalent pinned standard tool), using a new wrapper/unit/evidence root while preserving exact source tree, JDK, projection, init, selector, 5 GiB gate and first-failure stop.

## Attempt 9 terminal attribution (2026-08-29 19:21 CST)

| Symptom | Root cause | Attempt 10 remediation | Required proof |
|---|---|---|---|
| The detached static unit remained in the non-authoritative online hydration invocation for the full `RuntimeMaxSec=90min` and systemd terminated the control group with `Result=timeout`, `ExecMainStatus=15`. The build compiled through multiple modules and reached `:chat:jia-chat-service:compileJava`, while Maven Central downloads continued, but it produced no `BUILD SUCCESSFUL`, test XML, offline invocation, or product verdict. | Exact-tree dependency hydration was progressing but repository transfers were slow and serial enough to exceed the bounded service lifetime. The static service and Gradle serialization worked as designed; the failure is the online hydration lifecycle/runtime budget, not product source, parser, projection, JDK, lock ownership, or test behavior. Repeating the same online phase would be a blind lifecycle retry. | Preserve attempt-9 evidence. Do not repeat online hydration. Treat its populated cache only as preparation provenance, never as PASS evidence. After proving all attempt-9 processes are gone and the global Gradle lock is released, safely remove only abandoned unreferenced Gradle download temporaries and/or ignored H06 build outputs generated by the terminal attempt to restore the unchanged 5 GiB admission threshold. Create a new non-overwriting static attempt that pins the same exact commit/tree, JDK, projection and init digest, then runs only the authoritative `--offline --rerun-tasks` `ArchiveContentImporterTest` selector through the orchestrator. First failure stops. | Fresh preflight proves exact HEAD/tree/clean, unchanged JDK/projection/init digests, no process references to removed regenerable files, free bytes `>=5368709120`, PPID=1/static systemd cgroup and global Gradle lock identity. Offline command contains `--offline --rerun-tasks`, makes zero network dependency access, produces terminal Gradle success plus exact selected test XML with zero failures/errors/skips and accepted exact-tree evidence. |

Attempt-9 terminal evidence:

- Unit: `cyf-h06-r48-focused-verifier-attempt9.service`
- Active interval: `2026-08-29 17:51:25 CST` to `2026-08-29 19:21:27 CST`
- Result: `timeout`, `ExecMainCode=2`, `ExecMainStatus=15`
- Online log: `/var/tmp/cyf-h06-r48-focused-verifier-attempt9/01-online-focused-hydration.log`
- Online log SHA-256: `4b2df9165ace53677ff8668e5615c76557ccf66d3094d493d00528c41210b681`
- Tests started: `0`; offline authoritative phase started: `false`
- Post-terminal descendants: none; global Gradle lock holder: none
- Post-terminal free bytes: `5361127424`, below the unchanged 5 GiB threshold by `7581696` bytes.


## Attempt 10 terminal attribution — stale preparation evidence deletion (2026-08-29 20:18 CST)

- Exact candidate remained clean at `66f30bc530f9dc2c96960998bc9e089d1220eed7` / tree `56cc82235e51409bea320c3f4cf931448267a366`.
- Static unit `cyf-h06-r48-focused-verifier-attempt10.service` ran from `2026-08-29 20:06:07 CST` to `20:18:53 CST`, then exited `Result=exit-code`, `ExecMainStatus=1`.
- No terminal marker or selected-test XML survived, so attempt 10 produced **no product test verdict**. There are no descendants and no holder of `/tmp/cyf-gradle.lock`.
- Authoritative Codex history records preparation Agent `01a04d43-35a1-7e50-806f-7271e86e9280` executing item `call_qlP1M73aZh6hDI4RmlEaqQHB` at `2026-08-29 20:06:21.359 CST`, fourteen seconds after unit start. The command deleted every file/directory in the active evidence root except `manifest.txt`, `parser.sh`, and `preparation.terminal`.
- The running wrapper had already opened `wrapper.log` and redirected the orchestrated Gradle output to `01-offline-command.log`. Unlinking those pathnames did not stop writes to the open inodes, but after the Gradle child returned the wrapper's `sha256sum` of the now-missing log pathname failed under `set -e`. The surviving zero-byte `.sha256` file is not evidence of a test result.
- Root cause category: `stale_preparation_evidence_deletion`; this is a cross-phase evidence lifecycle/control-plane failure, not source, compilation, selector, Gradle, or product-test failure.
- Immutable incident evidence: `/var/tmp/cyf-h06-r48-attempt10-incident-20260829T123257Z-v2` (`SHA256SUMS` verified). The earlier `/var/tmp/cyf-h06-r48-attempt10-incident-20260829T123211Z` is a sealed partial packaging attempt caused by the host Python lacking `zoneinfo`; it is not the authoritative incident root.
- Authorized remediation for attempt 11: close the stale preparation Agent before launch; use a fresh non-overwriting wrapper/unit/evidence root; complete all preparation and static validation before launch; main controller alone performs the ledger transition and start; during runtime all other Agents are read-only; preserve exact commit/tree, immutable JAI/OpenCV projection, offline `--rerun-tasks` selector, global Gradle lock, PPID=1 static systemd and unchanged 5 GiB startup gate. First runtime failure stops.

## Attempt 11 preparation terminal — sealing contract incomplete (2026-08-29 20:45 CST)

- The static unit `cyf-h06-r48-focused-verifier-attempt11.service` remained **inactive**; no Gradle, runtime, DB, Rabbit, Chromium, production read/write, or deployment was started.
- Fresh wrapper SHA-256: `b176d680ed25b0a08c13bde25f7af6d9caf84c380ff3bc1c8f023f2af4bd44cb`; unit SHA-256: `5a77280d7e72c2021e32d47fdc7a109b800f3fe26899f11277dfcbc5f0369a8a`; parser SHA-256: `e0838f1710f01caa49a20eac41dae42e09fcc76700be6cb32c42a328ce154b9e`.
- Preparation reached a nominal `PASS` marker but did not satisfy the wrapper's fail-closed sealed-package contract: `SHA256SUMS.verify` is absent and the `static/` directory remains mode `0755` rather than immutable `0555`. Starting this unit would therefore stop at `sealed_preparation_invalid` before Gradle.
- Preparation encountered two generator defects: the host Python 3.6 runtime does not support `subprocess(..., text=True)`, and the sealing generator constructed an incorrect hash dictionary and raised `KeyError` while attempting to emit the verification manifest.
- Root cause category: `verifier_preparation_sealing`. This is a preparation-package compatibility and sealing failure, not a product, source, compilation, selector, or test verdict.
- Attempt 11 is frozen as invalid preparation evidence and must not be modified, supplemented, or launched.
- Bounded Attempt 12 remediation: use a fresh non-overwriting wrapper/unit/evidence path; use Python 3.6-compatible APIs (`universal_newlines=True`) or pure shell; generate and verify `SHA256SUMS.verify`; seal `static/` as `0555` with exact root ownership and file modes; complete and close the preparation Agent before launch; main controller alone may launch only after the unchanged `>=5368709120` byte startup gate passes. First runtime failure stops.

## Attempt 12 preparation preflight — wrong repository binding (2026-08-29 21:11 CST)

- Preparation Owner correctly stopped before creating any wrapper, unit, or evidence path.
- The assigned path `/home/isp/wsps/cyf/.worktrees/h06-scandir-remediation` is a root/superproject checkout at HEAD `5643e7d1f05bc645b66eb9eb6e459890da39fb79`, tree `e4d6db9273db6c73ec7c13242fd61e7b59f9fe28`, with API gitlink `4c0f4500eef70f410ffd5e9e477d97943c3dce9b`; it is not the exact standalone API candidate and its `api/` directory is empty.
- The clean exact API candidate is `/home/isp/wsps/cyf/.worktrees/h06-r48-api-concurrency`, commit `66f30bc530f9dc2c96960998bc9e089d1220eed7`, tree `56cc82235e51409bea320c3f4cf931448267a366`.
- Root cause category: `candidate_worktree_binding_mismatch`; this was a main-controller assignment error, not source/package/test failure.
- Attempt 12 paths are all absent and must remain absent. Attempt 13 must use the exact standalone API worktree and otherwise retain the sealed-package remediation contract from Attempt 11.

## Attempt 13 preparation pre-write assertion — brittle occurrence count (2026-08-29 21:27 CST)

- Exact standalone API worktree, candidate SHA/tree, clean state, init/projection/JDK/orchestrator hashes, and the 5 GiB disk observation all passed.
- The generator intentionally constructed all content in memory before any write. It stopped at `assert wrapper_text.count('attempt13') >= 10`; the transformed Attempt11 wrapper truthfully contains fewer than ten occurrence strings even though each required exact path/selector/fixture binding can be checked individually.
- This count assertion was a brittle generator self-check unrelated to the runtime contract. All Attempt13 wrapper/unit/evidence paths remain absent and the unit is not found/inactive.
- Root cause category: `preparation_generator_brittle_occurrence_assertion`; no product source, package, Gradle, selector, or runtime verdict exists.
- Attempt 14 remediation: remove the arbitrary occurrence-count check and replace it with explicit assertions for every required exact Attempt14 wrapper/evidence/unit/selector/fixture path plus absence of prior-attempt references. Retain all Attempt11 sealing remediation, exact worktree, immutable dependencies, inactive unit, and unchanged 5 GiB launch gate.

## Attempt 14 preparation pre-write parser assertion — REMAINDER delimiter semantics (2026-08-29 21:42 CST)

- All exact candidate, clean tree, immutable init/projection/JDK/orchestrator, lock visibility, and disk assertions passed; observed free bytes `5,544,783,872`.
- The generator's non-executing argparse probe incorrectly expected the literal `--` delimiter to remain in `args.command`. Python argparse `REMAINDER` consumes that delimiter, so the correct post-parse contract is `args.command[0] == './gradlew'`.
- The assertion failed before the first filesystem write. All Attempt14 paths remain absent and no runtime or product test ran.
- Root cause category: `preparation_generator_argparse_delimiter_expectation`.
- Attempt 15 remediation: preserve the exact argv fixture but assert the parsed command begins with `./gradlew`, contains `--offline` and `--rerun-tasks`, and keeps orchestrator options before task id; do not require the consumed delimiter in `args.command`. Retain all prior sealing and launch gates.

## Attempt 15 sealed preparation — parser awk quoting (2026-08-29 21:50 CST)

- Exact pre-write binding and corrected argparse contract passed. The fresh package was written and all eleven `SHA256SUMS` entries verified.
- The final static parser rejected its generated awk expression because quote escaping was preserved one level too far: generated `$1==\\\"SHA256SUMS_SHA256\\\"{print $2}` instead of shell awk source `$1==\"SHA256SUMS_SHA256\"{print $2}`.
- Root cause category: `preparation_parser_awk_quote_escape`; this is static parser generation, not source/runtime/test failure.
- Attempt15 is a sealed invalid package and must remain immutable and inactive.
- Attempt16 remediation is limited to correcting the awk source quoting and proving the exact parser expression in a temporary pre-write fixture before creating fresh Attempt16 paths. All other bytes/contracts should be derived from the vetted Attempt15 generator output and independently rehashed.

## Attempt 16 preparation pre-write — disk admission drift (2026-08-29 21:54 CST)

- Before the awk fixture or any final-path write, the unchanged 5 GiB gate observed `5,307,842,560` available bytes versus `5,368,709,120` required, a deficit of `60,866,560` bytes.
- All Attempt16 paths remain absent. Attempt15 remains sealed invalid, static, inactive, and immutable.
- Root cause category: `preparation_disk_admission_drift`; this is host-capacity drift while other evidence/session data grew, not a product/package/test failure.
- No retry is authorized until the main controller proves a safe, regenerable, unreferenced cleanup target and restores meaningful margin above the unchanged gate. The Attempt16 awk remediation remains pending for the next fresh package.
