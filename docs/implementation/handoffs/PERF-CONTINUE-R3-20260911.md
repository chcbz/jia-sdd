# PERF continuation R3 — 2026-09-11

Control-plane execution contract and evidence; current owner/gate only in `TASKS.yaml#runtime_ledger_json`.

## Inventory remediation admission

Main approved the two-P1 PERF-01 R2 matrix; existing root worktree `perf-inventory-20260911`, base `609cd1c46e9fe50a641270e56c0901f36ba634e5` / tree `00b861cdcb7e56be561d33c7d2fb75e8f5f2fe6f`, only `ops/performance/**`. Source Writer implements before an independent verifier and read-only reviewer. Earlier 19-test PASS is not source acceptance. No runtime mappings or full inventory acceptance may be inferred.

## Credential-free module verification admission

PERF-BUILD-01 is a separate verification-only continuation of the known A02 module-build configuration failure, not a reset of its history. Original attempts and exact-source tests remain in PERF-VERIFY-R2-ROOT-CAUSE-20260911.md. No build graph/source repair or production credential access is authorized.

Main approves ONE offline targeted Gradle invocation on clean accepted combined API candidate `5571d183fe7c612f2d5ebb272548aa5bfad77e90` / tree `b993a925464701b5a17c93461cf3f558036f5d13`, worktree `/home/isp/wsps/cyf/.worktrees/perf-api-integration-20260911`:

- Only `:common:jia-common-service:test --tests cn.jia.core.interceptor.HttpRequestLogInterceptorTest`; not starter/full application/full module suite.
- Explicit **non-secret** project properties `-PrepoUsername=perf-offline -PrepoPassword=perf-offline -PsnapshotsRepoUrl=https://example.invalid/snapshots -PreleasesRepoUrl=https://example.invalid/releases` satisfy eager publish configuration. No publish task; `--offline`; never use real credentials.
- JDK `/home/isp/apps/jdk21`; existing cache only; `--no-daemon --max-workers=1`, Gradle JVM `-Xmx384m -XX:MaxMetaspaceSize=256m -Dfile.encoding=UTF-8`. No init-script/source changes unless separately reviewed. Existing project test-memory settings must be inspected before launching.
- Every Gradle invocation through `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle`, with **all orchestrator flags preceding PERF-BUILD-01**, exact tree/selector/fixture and own artifact log. First query evidence cache. Global lock waits are not authorization to affect any other task.
- Dedicated Sol verification-only fallback (`gpt_test_runner_sol_fallback`) due to previously observed unavailable primary verifier; no provider probe/retry.
- Save exact argv, native return code, resource observations and test XML count/results in a new task-owned evidence directory. Zero tests is not PASS. Failure: attribute once, STOP, report bounded next step. No dependency download, service startup, DB, production load, cleanup of other tasks, daemon control or deploy.

Success would prove only the selected test through the actual Gradle dependency graph on the combined tree; failure remains explicit. Neither establishes all APIs <=3 seconds. The inventory repair is independent and must continue even if offline dependencies are unavailable.

## R3 candidate submitted

Root tooling candidate `f2b9e65641c9ac72021666314dcc866568a0dfe4` / tree `414281d47cd0772830dfda1e24464f1416897e90`, parent `609cd1c46e9fe50a641270e56c0901f36ba634e5`. Three changed files only: `ops/performance/inventory.py`, `README.md`, `tests/test_inventory.py`. Writer did not run tests and was explicitly closed after clean committed handoff; independent verification owns the candidate. Schema v3 adds strict input/source/content validation and external inventory/runtime artifact hashes. Source and full inventory acceptance pending.

## Review admission capacity — stop matrix

| Attempt | Attribution | Bounded remediation |
| --- | --- | --- |
| R2 historical admission failure | prior agent handles not addressable while runtime pool reported full; recovered by closing a known-live agent | retain historical failure; no process intervention |
| R3 admission failure | two known-live verifiers occupy available runtime slots; fresh reviewer denied, no reviewer started | STOP admission attempts; finish and explicitly close a known-live verifier before a single new reviewer admission |

Main approves this scheduling-only remediation after a slot has actually been released. Reopen PERF-REVIEW-01 with `authorize-remediation` referencing this matrix; then transfer read-only review mode. This is not a source Writer authorization, no source/test bypass, no foreign process or agent control. Prefer two active subagents maximum for the remainder of this task.

## Independent targeted Gradle result

Verifier `01a08e3e-0ce4-7aa3-b2b8-8c4484b329db` completed the single approved offline invocation on `5571d183fe7c612f2d5ebb272548aa5bfad77e90` / `b993a925464701b5a17c93461cf3f558036f5d13`: native0, BUILD SUCCESSFUL in 11m51s, 12/12 tasks executed; one XML, 6 tests passed, zero failures/errors/skips. Worktree remained clean. No source/build-graph changes, dependency download, credentials, DB, startup or deployment.

Evidence `/var/tmp/cyf-perf-build-r3-fDNNWL`; key `d5ebc5886ad7954f3c6202eb268fafb2255c92dfb779ed97f880c5af3973ce43`; receipt SHA256 `3649bba191b82c211fa7ce4b47044dcb665bfd2178fe3225814517fe51502b16`; manifest SHA256 `4a93fcf1f3229e9f68c800a4ef8bb1ac0362ec0a6cc7a489bbb6585246c978c9`. Main checked all15 SHA256SUMS entries. Separate read-only evidence review pending. Earlier failed configuration attempts remain failures; this new result only proves the selected logging test through the real dependency graph on the combined tree, not metrics/starter/full-module/application/runtime/SLO verification.

The build verifier was explicitly closed, permitting one fresh independent reviewer; the capacity matrix scheduling remediation was authorized and immediately transferred to read-only review mode. No source Writer was admitted by that scheduling gate.

## Independent inventory unit evidence and supplementary admission

`f2b9e656/414281d4`: independent Python3.6.8 unit native0, 25 expected/discovered/executed/PASS, zero skipped, CLIhelp native0; own evidence `/var/tmp/cyf-perf-inventory-r3-yLWLnu`, key `bbbab4da6f2ecfc5f360ccfbff9979c24ec087a2fa6694057e83db4830ee9ff1`, fixture digest `1937259d98844c2ff1bb4cffe2343812d40432a703735a9b03f0e937852e0f4f`; final manifest SHA256 `e9b52e952cab716d05a7cc5acd195b22ff63a8790ec2dadbda698b47ca159041`.

Verifier found coverage gaps, not a native test failure: unknown non-Controller test calls in-process scanner; positive subprocess reconcile uses a hand-built inventory. Main authorizes the same verifier to add ONE supplementary **CLI-only** verification selector in a fresh own evidence subdirectory, no source changes or repeated unit suite: (1) temporary clean Git Java fixture + bound nonempty framework manifest -> real scan -> preserve trusted external hashes/pins -> real reconcile matching synthetic runtime fixture, expected0/ok=true; (2) temporary clean fixture `@GM class OddEndpoint` in non-Controller filename -> real scan, expected2 with fatal unknown declaration diagnostic. Record all artifacts/argv/native exits, fixture digest and counts. Fixtures must be labelled synthetic, not grey/prod capture. Unexpected failure: attribute then STOP; do not repair source or retry. This closes test-evidence gaps only, not full inventory/SLO acceptance.

Supplement dispatch did not execute: the completed verifier ID returned `not_found`. Attributed as `verifier_handle_unavailable`, not code/test failure; existing25unit evidence retained. Do not repeat handle calls or blind spawns. Main permits the already-live independent source reviewer to perform the two tiny synthetic CLI cases as review reproductions in its own throwaway directory (read-only repository, no fixes/preimplementation/heavy resources); these are reviewer observations, not a fabricated independent verifier cache HIT. If a separate verifier remains necessary, complete/close the reviewer first and admit a new verifier once. No source acceptance yet.

## Independent R3 decisions and R4 bounded matrix

Reviewer `01a08e50-01b1-7913-84f9-69c3ace6943e`:

- BUILD-EVIDENCE ACCEPT0/0/0 for PERF-BUILD-01 scoped6test Gradle evidence, all source/manifest/XML identities verified. This slice is eligible for automatic control-plane promotion.
- Tool SOURCE/TEST REJECT0/1/0 despite25unitPASS. External artifact hash is computed from one file open (`inventory.py:1060-1061`, helper465-473); `load_json` reopens the same path at1071-1072. A FIFO/rename/symlink swap can supply trusted bytes to hashing and different coherently forged bytes to parsing. Existing forgery test changes files before invocation, so misses the check/read race.
- Reviewer synthetic CLI observations `/var/tmp/cyf-perf-review-r3-MrpC8p`, manifest `e1551ca8309d2a0bb38ca445862bbf89886b20d7380350fe07c1b53d11c7e96a`: positive real scan→reconcile native0/no diagnostics; non-Controller marker real scan native2/fatalunknown. These close the two earlier CLI coverage gaps but do not address the new race. No production/runtime/SLO proof.

| Failure | Root cause | Approved bounded R4 remediation |
| --- | --- | --- |
| Supplemental verifier handle unavailable | completed ID ceased to be addressable; no supplement executed | used already-live independent reviewer for tiny read-only-source reproductions; no blind dispatch retries |
| R3 source trust-boundary rejection | hashing and JSON parsing use separate opens, permitting TOCTOU substitution | one read per inventory/runtime artifact; hash AND parse the same immutable byte buffer; bounded swap/single-open regression for both artifacts; retain external pins/strict schema and all existing behavior |

Main stops at the second consecutive attributed event before authorizing R4. Approved Writer scope remains the existing `ops/performance/inventory.py`, `tests/test_inventory.py`, and only needed README wording, existing clean tool worktree at `f2b9e65641c9ac72021666314dcc866568a0dfe4` / `414281d47cd0772830dfda1e24464f1416897e90`. No general parser/schema redesign, no new dependency/security/runtime changes. Commit first, then fresh independent stdlib test verification and read-only delta review. No Writer test/build runs. Do not promote the R3 source candidate.

## R4 submitted candidate

`43e0e46f8d9a07797713adb432c3bcab770dd8b0` / tree `e0a9c30fa385c1ff0ae42d2f70f97dd5d87bc3b9`, parent `f2b9e65641c9ac72021666314dcc866568a0dfe4`. Only `ops/performance/inventory.py` and `tests/test_inventory.py`: read each JSON artifact once into immutable bytes, decode and hash those same bytes; deterministic atomic path-replacement test asserts exactly one open for each artifact and only original routes consumed. Production delta17lines, no schema/CLI/other logic change. Writer no tests; diff-check and clean commit only. Independent verifier authorized26test suite once (includes new regression, no redundant focused rerun) plus both synthetic CLI cases before final handoff.

## R4 verifier wrapper failure / metadata-only authorization

Independent verifier ran unit26/26PASS0skip, help0, positive scan0/reconcile0, negative scan expected2 exactly once. Its wrapper mistakenly enabled Bash `errexit` inside the capture function and stopped after expected2, before final output validation/manifest/cache. Attributed `verification_harness_expected_nonzero_handling`; no source failure or retry, logs preserved at `/var/tmp/cyf-perf-inventory-r4-mkXwWD`.

Main approves **metadata-only completion**, not a retry: read existing logs/JSON/native-result files and verify negative fatal diagnostic, validate clean exact source after, hash existing artifacts and record an honest receipt distinguishing wrapper exit from actual command/test results; cache only actually validated scoped results. No test/CLI/build rerun, no source edits and no rewriting failed wrapper evidence. Independent source reviewer must inspect the original raw evidence plus final receipt.

R4 attempted overlap reviewer admission was denied while the single known-live verifier was finalizing metadata; no reviewer started. Attributed `agent_capacity` separately from source/tests. Runtime inaccessible slots make even two-live-agent assumption unreliable: remainder is strictly **finish → explicitly close known-live agent → one next admission**, no overlap or blind retry.

## R4 metadata second failure / final review admission

Metadata-only verifier then matched the substring `skipped` in the passing test name `test_malformed_runtime_records_are_rejected_not_skipped`, falsely classifying it as a skipped result. Attributed `metadata_validator_false_skip_match`; second consecutive verification-side event stopped the metadata loop. No tests/CLI/source rerun or repair occurred. Verifier explicitly closed.

Main-approved recovery is **control-plane evidence audit + independent final delta review**, not another verifier/test/metadata-wrapper retry. Read the original 26 individual `... ok` lines and final `Ran26/OK`, individual native files 0/0/0/0/2, positive reconcile JSON and negative inventory fatal diagnostic; verify current source exact/clean and hash original artifacts into a separate main-audit receipt. Do not change originals or fabricate a successful verifier wrapper/cache HIT. New source reviewer independently checks raw outputs/audit and same-buffer source delta; may accept the bounded tool slice if actual evidence satisfies it. This authorization grants no source writes/heavy execution. Preserve both wrapper failures even if source/tests accepted. Main has directly confirmed raw actual26PASS, expected negative fatal diagnostic, successful synthetic roundtrip and exact clean `43e0e46f/e0a9c30f`.

## Final R4 acceptance and byte-exact promotion

Final independent reviewer `01a08e65-bcc6-7bc0-8c4a-063d1e6e5295` ACCEPT0/0/0 for exact `43e0e46f8d9a07797713adb432c3bcab770dd8b0` / tree `e0a9c30fa385c1ff0ae42d2f70f97dd5d87bc3b9`: same-buffer source fix, deterministic swap regression, actual26unitPASS and real syntheticCLI positive/negative independently sufficient. Reviewer independently matched clean before/after source, raw results and main control audit `/var/tmp/cyf-perf-r4-main-audit-wxj3fs0x` (receiptSHA `90342e89d43860a83027ba827e486c70882e6f818210e46367daa1c6ed8362a3`, raw-artifact manifestSHA `b8fa0f47ce52f056c4e1d5a6dda96106dc3390b32231d3019a78b03c965bcf18`). The missing completed verifier-wrapper manifest/cache is an explicit nonblocking evidence-format gap for this bounded acceptance, not a claimed successful HIT. Both verifier failures remain failures, without rerun.

Tool branch `codex/perf-inventory-20260911` pushed at `43e0e46f...`. Automatically merged into root delivery branch `codex/perf-sdd-20260911`: merge `45f5f07527e70d2fba9cc90f4ace9fdc95333825`, tree `2ffb80ec48a72a6ee172da2aa07bd22879105eed`, parents `63d0c9fafb6db58552f3c649e2fde90137cfbe72` and `43e0e46f8d9a07797713adb432c3bcab770dd8b0`. All4 `ops/performance/**` blobs verified byte-exact to accepted candidate; original-tree evidence reused explicitly, no new merged-tree suite claimed. Final documentation projection follows that merge; only own PERF ledger entries are projected onto branch-baseline ledger, preserving unrelated tasks' dirty main updates.

No push to root master/API develop, no deployment or production load occurred. Accepted API source stays `5571d183...`; this turn adds selected actual Gradle6PASS, not full module/starter/metrics build. Parent PERF-01 still awaits trusted real-profile framework manifests, protected runtime captures and registry100% reconciliation; PERF-02 isolated baseline and hotspot optimization remain ahead. Next executable task: freeze isolated profile/fixture startup inputs and trusted capture artifact provenance, then execute real-profile inventory reconciliation before the six-hotspot baseline. Do not open a hotspot Writer on synthetic-only inventory evidence.
