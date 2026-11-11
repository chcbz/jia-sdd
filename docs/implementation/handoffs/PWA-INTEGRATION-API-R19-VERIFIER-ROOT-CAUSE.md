# PWA-INTEGRATION-API-RC R19 verifier root-cause matrix

Approved by the main controller on 2026-08-29 for one bounded exact-tree remediation cycle.

Exact candidate: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

| Attempt | Symptom | Root cause | Remediation |
|---|---|---|---|
| 1 | Gradle rejected `-Xmx/-Xms/-Xss` as options | Verifier split the `-Dorg.gradle.jvmargs=...` value into multiple argv words | Pass the complete JVM bundle as one quoted argv element |
| 2 | Offline configuration could not resolve Spring Boot Gradle plugin `4.0.1` | The exact workspace cache lacked the plugin marker/artifact; tests never started | Start one bounded official-repository hydration through the external init script |
| 3 | The first hydration downloaded dependencies for about 42 minutes, then the daemon reported client disconnection/stop requested | The detached verifier thread ended before its child process, so hydration was externally terminated before all artifacts were cached | A fresh exact verifier must keep the orchestrator/Gradle command attached and wait for its terminal exit; no process restart while it is active |
| 4 | Offline compile passed plugin resolution but failed resolving many `testRuntimeClasspath` JARs | Attempt 3 left a partially hydrated cache; the explicit init script is now correct, but required test/runtime artifacts remain absent | Authorize one final attached online hydration that resolves the focused test and bootJar configurations through MavenLocal, official Gradle Plugin Portal and Maven Central; then run the frozen compile/selectors and `:starter:bootJar` offline on the unchanged tree |

| 5 | The second attached hydration ran for about 24 minutes, downloaded additional artifacts, then ended without a test verdict; daemon log reports `client disconnection detected, canceling the build`, and the verifier confirmed it manually interrupted the still-running command | An Agent-attached client is not a durable owner for a long Gradle hydration; ending/interruption of that client closes the daemon socket and cancels the build before terminal evidence | Stop attached retries. Run the unchanged exact tree only from a task-owned non-transient static systemd unit with PPID 1, serialized by `/tmp/cyf-gradle.lock`; start only after H06 reaches terminal and resource gates pass, then perform offline focused selectors and `:starter:bootJar` |

No source change, production access, credential output, DB, RabbitMQ, or deployment is authorized. The external init script is verification infrastructure only and remains SHA-256 bound. The fresh verifier must keep the hydration attached until terminal completion. After hydration, authoritative evidence must come from an offline rerun on the unchanged exact tree. Any new failure stops for attribution.

| 6 | Fresh static-verifier package generation stopped before creating any final wrapper/unit/evidence path | The host package generator assumed newer Python APIs: `shlex.join` is unavailable and `subprocess.run(..., text=True)` is unsupported on Python 3.6 | Freeze the failed generator attempt; create a fresh non-overwriting R2 package using a local shell-quote helper and `universal_newlines=True` (or pure shell), then seal and statically verify the complete package. Do not start the unit until H06 is terminal and all shared resource gates pass |

Attempt 6 created none of the intended final paths: `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r1`, `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r1.service`, `/var/tmp/cyf-pwa-api-r19-static-verifier-r1-preparation`, and `/var/tmp/cyf-pwa-api-r19-static-verifier-r1-evidence` were all confirmed absent. No Gradle, DB, RabbitMQ, systemd runtime, production access, or deployment occurred.

## Static package Review failures and authorized R4 matrix

The following two failures are verifier-infrastructure failures; neither unit was launched and neither produced a source/test verdict.

| Attempt | Symptom | Root cause | Bounded remediation |
|---|---|---|---|
| 7 / static R2 | Independent static Review `REJECT 2/4/1`: root candidate execution, user-writable JDK under root, invalid final checksum ordering, unbounded/signalless lifecycle, H06/PWA dependency loop, undeclared candidate-wrapper distribution URL, no external root digest | Detached durability and selector binding were implemented without a complete privilege, toolchain, lifecycle, and self-sealing threat model | Preserve R2 inactive/empty. R3 delegates every Gradle child to UID/GID `61019:61019`, uses task-only writable roots and a direct sealed Gradle distribution, adds bounded signal handling, corrects terminal/checksum ordering, allows the exact owner-null H06 cache-wait state, and roots the static package externally |
| 8 / static R3 | Independent static Review `REJECT 1/3/1`: root orchestrator reopen through an `isp`-writable ancestor, no proof that all cgroup descendants/log writers are gone before final sealing, mutable JDK pre/post-manifest TOCTOU, and no cache bridge covering H06 chat-service dependency hydration | R3 dropped candidate Gradle privilege but did not pin the root control path in a mount namespace, treated direct-child return as cgroup quiescence, reused a mutable host JDK, and isolated the cache without explicitly hydrating the H06 compile path | Preserve R2/R3 inactive and empty. R4 uses a private systemd mount namespace that pins the exact repository/control tree read-only while exposing only the minimum root-owned ledger/evidence directory for orchestrator atomic writes; uses a root-owned immutable JDK snapshot under tmpfs and a root-owned staged Gradle distribution; separates main execution from a root-owned `ExecStopPost` final sealer that runs only after cgroup shutdown and records the cgroup proof; adds one explicit non-authoritative online `chat:jia-chat-service` dependency/compile bridge into the same isolated Gradle home that fresh H06 Attempt19 must reuse; retains 8 authoritative PWA offline steps, delegated UID/GID, official repositories, bounded runtime, first-failure stop, source read-only, external static root, and no production access |

R4 exact safety invariants:

1. R2 and R3 paths/evidence remain byte-exact, inactive, and are never overwritten.
2. R4 uses fresh wrapper, sealer, unit, preparation, runtime-evidence, task-workspace, immutable-JDK and builder paths.
3. No root process reopens executable Python/JDK/Gradle bytes through an unpinned user-writable ancestor. The unit must prove its private mount bindings before any Gradle request.
4. Candidate code always executes as `61019:61019` with empty supplementary groups, task-only `HOME`, Gradle home, external build root, project cache and tmp; source is read-only and not writable to that identity.
5. Final runtime `terminal.marker`, manifest, checksums and root digest are created only by `ExecStopPost` after the main process and all earlier cgroup descendants have ended. No runtime-evidence write follows the root digest.
6. Online hydration is non-authoritative and now includes an explicit H06 chat compile/dependency bridge. Only the unchanged R19 tree's complete offline PWA phase is authoritative for PWA acceptance. H06 remains unaccepted until its own unchanged exact-tree offline selector passes using the same cache.
7. Any R4 preparation, static Review, launch, hydration, offline, seal, or cache-bridge failure stops immediately for attribution. No automatic retry, source change, DB, RabbitMQ, Chromium, production, deployment, or evidence deletion is authorized.

## R4 preparation failures and authorized R5 matrix

R4 remained unlaunched. No Gradle, source test, DB, RabbitMQ, Chromium, production, or deployment action occurred. The source candidate remains exact commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

| Attempt | Symptom | Root cause | Bounded remediation |
|---|---|---|---|
| 9 / R4 preparation 1 | JDK source/snapshot comparison rejected even though all 677 regular-file hashes and symlink targets had zero differences | The comparator included directory `st_size`, which is allocation metadata and differs between ext4 and tmpfs despite identical content | Preserve R4. R5 compares relative path, entry type, mode, owner, regular-file byte size and SHA-256, and symlink target; directory size is excluded while all executable/file identity checks remain exact |
| 10 / R4 preparation 2 | The mandatory static matrix rejected the final-seal ordering although the sealer order was `terminal.marker → SHA256SUMS.runtime → root digest write/fsync/close → os._exit(0)` | A global first-occurrence textual search for `os.write(fd,data)` matched the generic `atomic()` helper rather than the root-digest write inside `seal()` | Preserve R4 inactive and non-overwritten. R5 uses a function-scoped or AST-equivalent unambiguous assertion that binds the root-digest open/write/fsync/close and final `os._exit(0)` ordering inside `seal()`; it must still reject any write after the root digest |

R4 preservation bindings:

- Wrapper SHA-256: `0093a253e9d38c8c0f4443bbba7612037016f120f7d2a9a20927270bfed33cd2`
- Sealer SHA-256: `fc652c6ceed64f774464074cdd3d19df7626d8023e4e6ffb3b5ac46fa8d681a9`
- Unit SHA-256: `6536e60ee1d56d1724b7f54e8447d5a95745df4b76f43d1e478300ccbdb5196f`
- Package manifest SHA-256: `d1d9b1076284cc654b626510b359de9e87c495b847b7779edc2f3a28300a737a` (356 entries)
- Package verification transcript SHA-256: `efee23ece4f2dd8e00fdeaa6f4901bcbeb2040ad755031e74632d76f8fea6dfb`
- Static package root: `455c4dd79abc945c6d24b58a32c60c4a2460cd28b0b7784e201070a4f052ac6a`
- Builder root: `9135610444ab58755982beeb56732e90368b1facdfe251321494aadde9fd053a`
- Builder directory: `/var/tmp/cyf-pwa-api-r19-static-verifier-r4-builder-20260830T002910+0800`
- Immutable JDK content digest: `e0974e4f5a9a480b44bb805d1fff96bec0f5310b791ca4a17aac90595a8c5e1f`

R5 authorization is limited to a fresh, non-overwriting preparation package. It must carry forward every R4 safety invariant and change only the two failed verifier assertions above. It may not edit or start R4, invoke Gradle, access production, or produce a source verdict. A fresh independent static Review is required before any R5 unit launch.

## R5 preparation failures and authorized R6 matrix

R5 remained unlaunched and is frozen byte-for-byte. No Gradle, source test, DB, RabbitMQ, Chromium, production, or deployment action occurred. The source candidate remains exact commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

| Attempt | Symptom | Root cause | Bounded remediation |
|---|---|---|---|
| 11 / R5 preparation 1 | `freeze-prior.py` exited before any R5 final path was created with `IndexError: tuple index out of range` | The FILE evidence formatter declared one excess replacement field | Preserve the failure evidence; correct only the formatter arity in the fresh builder. The successful bounded rerun produced 1,483 prior-preservation records |
| 12 / R5 preparation 2 | R5 package contained 351 items instead of R4's 356 and omitted all six sealed JAI/OpenCV jar/pom files required by the H06 chat compile bridge | The deriver performed blind global lowercase `r4 → r5` replacement, corrupting the immutable donor path component `cyf-h06-r48-...` to nonexistent `cyf-h06-r58-...`; optional donor-copy behavior then silently skipped the missing directory | Preserve R5 inactive and non-overwritten. R6 must replace only exact PWA R5 identifiers/paths, never arbitrary substrings; hard-bind the immutable H06 R48 donor path and six file digests; fail closed before final-path creation unless all six files and the frozen bridge relative-path set are present |

R5 preservation bindings:

- Package root: `ab89d3f477aecb9e1559cae6466425c5c6642e8a579ca03d1d3455bc9e45d29b`
- Builder root: `f1dd6c4f31bc6b0c1aefda0022e200a6e999c14a8c2ff2f9c58660959ce106db`
- Builder directory: `/var/tmp/cyf-pwa-api-r19-static-verifier-r5-builder-20260830T080116+0800`
- Unit state at freeze: `inactive/dead`, `MainPID=0`, `ControlPID=0`
- Rejected package static Review eligibility: false

Immutable H06 R48 donor binding for R6:

- Donor root: `/var/tmp/cyf-h06-r48-jai-opencv-maven-attempt8`
- `com/sun/media/jai_imageio/1.1/jai_imageio-1.1.jar` = `2b40befa9340e15759c68867df08905c6c6400df379ec7802120386325a565d3`
- `com/sun/media/jai_imageio/1.1/jai_imageio-1.1.pom` = `a6505da0f7a01e265e5926c56e3ab6bb951911c8f610312967a632652ea8040c`
- `javax/media/jai_core/1.1.3/jai_core-1.1.3.jar` = `8b696cf067533545f44c2f68339e24ab1a2669153ed2081aa5be8749f4d592bf`
- `javax/media/jai_core/1.1.3/jai_core-1.1.3.pom` = `9fba26708133731e184cc00f33f4ef82a7f270192028d25f7f6f3667a85b4190`
- `org/opencv/opencv/4.5.5/opencv-4.5.5.jar` = `323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4`
- `org/opencv/opencv/4.5.5/opencv-4.5.5.pom` = `786de45db6266b338faf603d0555bdb491357aeece0f9608c3a08d78700dc203`

R6 is authorized only as a fresh, non-overwriting preparation package. It must inherit all R4/R5 safety invariants, use an explicit exact-token replacement allowlist, preserve the literal H06 `r48` path, require the six donor files and digest set above, and verify manifest-count plus relative-path parity against the frozen R4 bridge projection. It may not edit/start R5, run Gradle, access production, or produce a source verdict. A fresh independent static Review is required before any R6 unit launch.

Ledger note: the main controller recorded the same two R5 failures after the exact owner had already persisted them, so the ledger contains duplicate attribution entries and a counter of four. There were exactly two R5 preparation attempts, not four; the duplicate entries are control-plane bookkeeping only and do not represent additional execution or retries. The next `authorize-remediation` resets the active consecutive-failure counter without deleting the preserved duplicate evidence.

## R6 builder-only failures and authorized R7 matrix

R6 stopped before creating any final wrapper, sealer, unit, preparation, evidence, workspace, incidents, or immutable-JDK path. The reconciled generator was never executed. No Gradle, source test, DB, RabbitMQ, Chromium, production, or deployment action occurred. The source candidate remains exact commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

| Attempt | Symptom | Root cause | Bounded remediation |
|---|---|---|---|
| 13 / R6 builder 1 | Exact block replacement stopped with source token count 0 instead of 1 | The matcher used a non-raw Python triple-quoted literal, interpreting source `\\n` characters as real newlines | Preserve evidence. The bounded reconciliation used raw exact literals and successfully created the reconciled generator without executing it |
| 14 / R6 builder 2 | A builder-only static audit stopped because the matrix digest occurred twice while the audit expected once | The digest legitimately appears in both the matrix binding and candidate-binding metadata; the newly added cardinality assertion was not a safety invariant | Preserve R6 builder. R7 must not rederive complex source blocks and must not invent cardinality assertions for unchanged metadata. Use the frozen reconciled generator as the only donor, verify its exact SHA, and patch only explicit full R6 output paths/identifiers via a finite allowlist before one execution |

R6 preservation bindings:

- Builder directory: `/var/tmp/cyf-pwa-api-r19-static-verifier-r6-builder-20260830T082457+0800`
- Reconciled, unexecuted generator: `build-r6-remediation1.py`
- Reconciled generator SHA-256: `882f859b0edad5f5eb26b5771db240f74a729eb5f1eff7cca005e772e7232b21`
- First generated candidate SHA-256: `cdde9625049763d5abfe37bc012abded8357b420b0e05512999e5fa32e677b06`
- Failure-2 attribution SHA-256: `7d7647cacecbae6575d8027eba921300bf545d496de726caf5b34055b8145771`
- Blocked matrix SHA-256: `6eaabc6e6e99702114e341310fbca71f9206c11508587daa635441c70cc31553`
- H06 donor projection digest: `61fc0ecff2cc56043c20de36b1d0dab7cb5d77c230d37bdf5443833a8da0ebc0`
- Final R6 paths: all absent; unit `not-found/inactive/dead`, `MainPID=0`, `ControlPID=0`

R7 authorization is limited to one fresh non-overwriting preparation package. It must:

1. Read only the exact frozen `build-r6-remediation1.py` donor above and verify its SHA before transformation.
2. Avoid all broad/global substring replacement and avoid re-editing embedded source blocks. Transform only a finite allowlist of exact full R6 output path strings, exact unit/service names, exact display labels, and the current matrix digest/binding where required. Every source-token count must be declared and verified; unrelated `r6`, `R6`, H06 `r48`, candidate SHA/tree, donor paths and dependency selectors must remain byte-exact.
3. Retain the six-file H06 donor mandatory digest/parity gate, JDK identity semantics, function-scoped sealer ordering/negative mutation test, ONLINE=9, OFFLINE_AUTHORITATIVE=8, cgroup-final sealing, non-root Gradle child, read-only source, bounded runtime, and all prior security invariants.
4. Execute the transformed R7 generator at most once after all builder-only preconditions pass. Any generator/package/static failure is attributed before one bounded retry; a second stops.
5. Keep R6 absent and all R2–R5 paths byte-exact. Do not run Gradle or start R7. Fresh independent static Review remains mandatory before launch.

## R7 capacity dependency resolution: reuse immutable sealed JDK snapshot

R7's finite-allowlist transformed generator passed builder-only diff classification but correctly refused to execute because copying a third 669,907,755-byte immutable JDK snapshot would violate the memory margin gate. At the gate, `MemAvailable=860,557,312` bytes and the copy requirement was `1,206,778,667` bytes, a 346,221,355-byte shortfall. This is an external capacity wait, not a generator/package failure; execution count remains zero and every final R7 path remains absent.

The controller authorizes a bounded capacity remediation without deleting prior evidence or stopping any process:

1. Reuse the existing immutable root-owned read-only snapshot `/dev/shm/cyf-pwa-api-r19-static-verifier-r5-jdk21` as R7's runtime JDK instead of copying a third snapshot.
2. The reused R5 snapshot and the independently preserved R4 snapshot have identical full sealed identity manifests: 677 entries, SHA-256 `995e2193a455aff46f74d8bdfe9ac3e225df8f14fd867334fa6cc471a305c631` when identity includes relative path/type/mode/uid/gid, regular-file size+SHA-256 and symlink target while excluding directory size.
3. Source JDK, R4 snapshot and R5 snapshot have identical byte-content projection: 676 descendant entries, SHA-256 `ecf40b2b91cbfac66614519e1541c7dd57cfca62e7cb76ee4c7e1cb64d376c15` over relative path/type, regular-file size+SHA-256 and symlink target.
4. R7 must verify the reused snapshot's full sealed identity and byte-content digests immediately before creating any final R7 path, record the proof in its builder/preparation package, bind the unit and runtime manifests directly to that exact reused path, and keep `/home/isp/apps/jdk21` inaccessible at runtime.
5. Reuse is read-only and must not modify, chmod, chown, relink or delete R5. Prior R2–R6 preservation remains mandatory.
6. The capacity-remediated R7 generator may be executed once. No Gradle or unit launch is authorized. Fresh independent static Review remains mandatory after successful preparation.

## R7 capacity-remediation derivation failures and authorized R8 direct-edit matrix

R7's original generator and capacity-reuse proof remain unexecuted; all final R7 paths are absent. The reused immutable R5 JDK proof passed. Two builder-only derivation attempts then failed before creating a capacity-remediated generator:

| Attempt | Symptom | Root cause | Bounded remediation |
|---|---|---|---|
| 15 / R7 capacity derivation 1 | Host writer failed before creating the deriver | Host-side and embedded Python reused the same triple-quote delimiter | Do not generate a generator through nested Python literals; use a normal file copy plus a direct patch file/tool invocation |
| 16 / R7 capacity derivation 2 | Deriver rejected itself with `broad_version_replacement_detected` | A textual self-scan included its own forbidden-pattern literals, making the check tautologically fail | Remove self-text scanning. Validate actual edits from an external before/after diff and, if inspecting Python, inspect only AST call nodes rather than source string literals |

Preserved R7 bindings:

- Builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r7-builder-20260830T085157+0800`
- Original unexecuted generator SHA-256: `29248944d2fcf003a7141bb34479ba29cc4f0c8a13a995759337ea202ad4dde0`
- Capacity proof SHA-256: `2e4977be2844f7ed9f78a92a00527ecc4fa6d85fa6fc2622915ab8cf41e7f384`
- Capacity-proof transcript SHA-256: `44381332ae407d6093c6aa2eed9c908e53d58e423e8b434fd81e0f134ee224b4`
- Capacity derivation failure-2 SHA-256: `5beb56f68ba90c2e6c9908aca8816ddc8374551de2e6a5334d242f0e29f55054`
- Capacity blocked matrix SHA-256: `1206b4abb0bfa8d138a3736a7632a97e2ecc7c8ebfcea936d8f44c97fab980cb`
- Builder root: `f6fc50ae9ad5835b912e968b48b5ac1524b046db0b8bc76c1b2947f61e76fb03`
- Generator execution count: zero; final R7 paths absent; unit not-found/inactive/dead.

R8 is one fresh non-overwriting preparation package using a **direct-edit workflow**, not another nested deriver chain:

1. Copy the exact R7 generator donor once to a fresh R8 builder file, then apply a human-readable unified patch or a simple external exact-block edit. Do not create code whose main purpose is to generate another transformation program.
2. Replace only exact complete R7 output paths/service identifiers with fresh R8 paths. Change the JDK binding to `/dev/shm/cyf-pwa-api-r19-static-verifier-r5-jdk21` and replace the new-snapshot capacity/copy/seal block with direct verification and manifest generation from the reused snapshot.
3. Before final-path creation, verify the preserved JDK full identity `677:995e2193a455aff46f74d8bdfe9ac3e225df8f14fd867334fa6cc471a305c631`, byte projection `676:ecf40b2b91cbfac66614519e1541c7dd57cfca62e7cb76ee4c7e1cb64d376c15`, root ownership/read-only modes, R4/R5 equality, and capacity proof bindings. Never modify the snapshot.
4. Validate the resulting R8 generator with `py_compile`, `git diff --no-index`/equivalent external diff classification and an AST query that examines only actual `str.replace` call arguments. No source-text self-scan and no token-cardinality checks unrelated to a specific edit.
5. Execute the R8 generator at most once. Preserve all R2–R7 paths. No Gradle or unit launch. A fresh independent static Review remains mandatory before any R8 runtime.

## R8 independent static Review and authorized R9 remediation matrix

Exact R8 generator `/var/tmp/cyf-pwa-api-r19-static-verifier-r8-builder-20260830T094706+0800/build-r8.py` (SHA-256 `1d13118e2c0eb3dbfca2ab39ce9468b640ea974f881d97c41c099b3468c73c72`) remains unexecuted; all final R8 paths are absent. Fresh independent `sol_reviewer` `01a05065-8b74-7100-9364-5cfd5f3df2c4` returned **REJECT P0/P1/P2=0/2/1**.

The earlier external AST failure was confirmed to be receiver over-constraint rather than an actual broad `str.replace` mutation: the donor and R8 each contain six actual `str.replace` calls with identical argument catalogs. Nevertheless, three real issues block execution:

| Severity | Finding | Root cause | Required R9 remediation |
|---|---|---|---|
| P1 | Authorization/ledger binding is stale and would fail immediately after a new authorization | R8 hard-codes the previous matrix, owner, notification, failure count `1` and previous failure category, while `authorize-remediation` resets count to `0` and assigns a new owner | R9 binds the new matrix SHA, exact R9 owner and fresh authorization notification, requires gate `remediating`, failure count `0`, and latest historical category `ast_query_receiver_overconstraint`; frozen contract and acceptance notes must agree with executable checks |
| P1 | Six H06 donor files are hard-linked and then chmod/chown'd, mutating donor inode link count/ctime and violating byte+metadata preservation | `os.link(src,dst)` shares donor inodes; later metadata writes act on the same inode | Use independent `O_CREAT|O_EXCL` copies into staging, copy bytes, `fsync`, close, set staged metadata, verify each staged SHA, and compare donor metadata manifests before/after including inode/link count/mode/owner/size/mtime/ctime as appropriate. Never link/chmod/chown the donor |
| P2 | Final-path publication is non-transactional and `preparation.terminal=PASS` is written before all package checks | Final PREP/OUT/WORK/INCIDENT and wrapper/sealer/unit are created incrementally; a later failure leaves partial final paths | Build and validate under fresh root-owned staging paths first. Publish sealed PREP, wrapper, sealer and runtime dirs only after all content/static checks pass; publish the unit and launch-readiness marker last. A failure before the last step must leave no final unit and no false PASS marker. Preserve all prior versions; do not delete prior evidence |

R9 direct-remediation constraints:

1. Use the exact R8 generator as the reviewed donor. Create one fresh R9 builder/generator with a direct readable patch; no nested deriver chain and no source-text self-scan.
2. Use only the corrected AST query that examines actual `str.replace` call arguments. The query is external builder evidence, not a runtime gate embedded through receiver-source comparison.
3. Keep the reused immutable R5 JDK path and its proven identities: full `677:995e2193a455aff46f74d8bdfe9ac3e225df8f14fd867334fa6cc471a305c631`; byte projection `676:ecf40b2b91cbfac66614519e1541c7dd57cfca62e7cb76ee4c7e1cb64d376c15`.
4. Retain all other accepted static properties: exact candidate/tree, H06 six-file digest/path projection, ONLINE=9/OFFLINE=8, source/JDK read-only mount contract, candidate code as UID/GID 61019, direct sealed Gradle, bounded runtime, function-scoped final sealer, cgroup quiescence, post-root-digest negative mutation, and no production.
5. Generator execution remains forbidden until a new authorization has been recorded and the R9 precreation binding matches it exactly. R9 generator executes at most once. No Gradle or unit launch during preparation. Fresh independent static Review is mandatory after successful R9 package generation.
