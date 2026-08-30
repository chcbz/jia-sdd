# PWA API R19 R17 builder root-cause matrix — 2026-08-30

Exact product source remained unchanged and clean throughout: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The main controller authorized fresh R17 remediation at `2026-08-30T20:43:30+08:00` for exact writer `01a052b1-fc55-73d3-9f8f-90ea308854a8` (`critical_worker`, `writer`) against durable handoff `docs/implementation/handoffs/PWA-INTEGRATION-API-R19-R16-BUILDER-ROOT-CAUSE.md`, SHA-256 `bfb1d0e1a4ff0dd98a596dfabd5728d6690f84deead743f5b3514d8794614279`. R17 stopped under the second-consecutive-failure policy before any R17 construction helper, template, deriver, `build-r17.py`, publish staging, final package path, activation, or unit existed. No generator executed, no unit was created or started, and no static Review is requested.

Sealed R17 builder/control evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r17-builder-20260830T204630+0800`, 37-file manifest root SHA-256 `18b528b0284ba9a7da7a4c2560fd7123e422323647765eaf89a4621a35d47f39`.

## Authorization, frozen contracts, and inherited-root result

- The ledger prewrite bound exact owner/profile/mode, `remediating`, exact product commit/tree, durable R16 handoff path/SHA, and retained R16/R15/R14 attempts without depending on mutable `blocker.summary`.
- Before design use, R17 independently verified sealed R16 root `ec2aef2b27c17fc33c80a98d98a1ae01d167e3d8ed285d2dc92768dd7915fe43` (47 rows), R15 root `9a7068d638b497b9abd2ad433034e23eda830f27133975d25038587316b0ae7a` (28 rows), and R14 root `f38988ddf2c9a6aca3e43310fb4a978ea16c3e8cb6d4a8011cbf98da23ecf25f` (26 rows).
- R17 froze the product API/event catalog, lock order, transaction/publication boundaries, sensitive-payload allowlist, exact final path set, full package contract, and acceptance-to-static-test mapping before construction work.
- The intended analyzer design corrected statement order: inspect each `For` iterable first, compute current iterable taint, rebind or clear every nested tuple/list target conservatively, and only then inspect body statements in execution order. It retained source self-dependency and operation-aware path aliases. Because both failures occurred in bootstrap construction before publication, no durable R17 deriver or generator was created and these semantics were not promoted as PASS evidence.

## Failure matrix

| Failure | Symptom | Root cause | Safety result / successor boundary |
|---|---|---|---|
| R17 bootstrap 1: `r17_bootstrap_binding_cardinality_assertion` | The in-memory bootstrap rejected the complete candidate because it expected three occurrences of `r16_retry_deriver_failure` but observed five. | The bootstrap used an over-tight source-text cardinality assertion. Five occurrences were legitimate across generated authorization, prewrite authorization, retained-attempt tuples, and proof metadata. | Attributed through `cyf_orchestrator.py fail`. No helper/template/deriver/generator path was published. The sole bounded retry was authorized to use fresh `.retry` paths and structural binding checks. |
| R17 bounded retry preparation: `r17_retry_bootstrap_exact_replacement_mismatch` | The retry transformer could not find an exact escaped source fragment for the generated `derive-r17` SHA record. | The retry attempted to self-transform the first bootstrap source and coupled its edit to a particular escaped newline/quote representation. The actual bootstrap source stored a different escaped form, so the exact-replacement assertion failed. | Attributed through `cyf_orchestrator.py fail`; this was the second consecutive failure. Stop R17. No retry bootstrap, helper, template, deriver, generator, staging, package, activation, or unit was published. |

## Preservation and fail-closed state

- R16 before/after preservation is exact: 60 rows, root SHA-256 `5e12b54e11b4ef1e5669ba87eaabf06de63318a6a9753417e0a9a2b2261810f9`.
- R15 before/after preservation is exact: 41 rows, root SHA-256 `4333a55985f0828900e9f33801a6db87c3b011ca3e08a8fa0c443c0431e75de2`.
- R14 before/after preservation is exact: 39 rows, root SHA-256 `26e22f05e8229948a11f9b5fb7a30be3110e6ade14c618acc110b8ca61bf623f`.
- Complete R13 before/after preservation is exact: 462 rows, root SHA-256 `b2c19013f679706c3394a943ee5672bd703854a683aafa91228ce94a6d3a0cde`.
- No R16/R15/R14/R13 path was edited, deleted, chmod/chown modified, hardlinked, or reused. The historically contaminated R3/R4/R5 Maven inodes were not read, modified, restored, or linked.
- Every R17 final destination, publish staging, construction helper/template/deriver path, and `build-r17.py` is absent. `GENERATOR_EXECUTIONS=0` and `COMMIT_POINT_REACHED=false`.
- Read-only unit queries show R9–R17 inactive/dead or not-found with `MainPID=0`, `ControlPID=0`, `NRestarts=0`, and zero journal lines since R17 authorization.
- No Gradle, DB, RabbitMQ, Chromium, daemon reload, unit start/stop/restart, production access, deployment, or product-source mutation occurred.

## Evidence keys

- R17 builder root: `18b528b0284ba9a7da7a4c2560fd7123e422323647765eaf89a4621a35d47f39` (37 files)
- authorization record: `control/prewrite-authorization.json` in the sealed builder
- first failure: `control/bootstrap-failure-1.txt`, SHA-256 `7ecc2c84cf1f52f4fbf4a57abffb4bc427c395fd0d9149afd57a5a0d3ce8b973`
- second failure: `control/bootstrap-retry-preparation-failure-2.txt`, SHA-256 `d9e900670e5b95749b9d2ad7c572713c5604108a8abd1352215e1abac70bbffd`
- failed first bootstrap source: `control/bootstrap-attempt-1.py` and its adjacent SHA record
- preservation comparison: `control/preservation-comparison.json`
- final-path absence proof: `final-paths.after-second-failure.json`
- unit read-only proof: `control/unit-never-started.json`
- exact source proof: `control/source-exact-after-failure.json`
- ledger terminal proof: `control/ledger-after-second-failure.json`

## Ledger and exact successor boundary

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r17_retry_bootstrap_exact_replacement_mismatch`, consecutive failures `2`. Do not transition R17 to Review and do not appoint a Reviewer.

Only a main controller may separately authorize a fresh non-overwriting successor against this matrix. A successor must:

1. bind authorization to this durable R17 handoff path and its externally computed SHA-256, sealed R17/R16/R15/R14 roots, retained R17/R16/R15/R14 attempts, exact new owner/profile/mode, and exact product commit/tree without depending on mutable `blocker.summary`;
2. preserve every R17/R16/R15/R14/R13 path exactly and avoid all contaminated R3/R4/R5 Maven inodes;
3. construct the complete bootstrap/helper/template/deriver directly from fresh file-backed source, compile each complete source in memory under Python 3.6 before its O_EXCL publication, and never self-transform escaped replacement expressions from a prior failed bootstrap;
4. implement statement-order dataflow so every `For` iterable is analyzed before its nested tuple/list target is rebound or cleared and before its body is inspected in order, while retaining source self-dependency and operation-aware path alias propagation;
5. require actual-source zero violations plus all eight direct/alias read/open/stat/hash negative fixtures before creating the successor generator;
6. retain complete pre-rename destination digest freezing and destination-only post-rename verification;
7. freshly execute all inherited R13 package contracts: external-cfile Python 3.6 compile, zero PREP pycache/pyc/control logs, independent O_EXCL copies, hardlink-negative, donor metadata before/after, JDK 677/676, UID/GID 61019, ONLINE=9/OFFLINE_AUTHORITATIVE=8, exact `PACKAGE_PATHS`, fault injection, fail-closed activation, and unit-last publication;
8. attribute any first successor failure before one bounded retry and stop on a second consecutive failure.
