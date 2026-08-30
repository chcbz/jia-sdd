# PWA API R19 R16 builder root-cause matrix — 2026-08-30

Exact product source remained unchanged and clean throughout: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The main controller authorized fresh R16 remediation at `2026-08-30T20:21:41+08:00` for exact writer `01a0529e-0758-7d03-aaa8-e1360bad01fa` (`critical_worker`, `writer`) against durable handoff `docs/implementation/handoffs/PWA-INTEGRATION-API-R19-R15-BUILDER-ROOT-CAUSE.md`, SHA-256 `57f2dc7b125f427840949c5326051837e2a068aa2d8c3b90bee4555fbe4c6110`. R16 stopped under the second-consecutive-failure policy before `build-r16.py`, publish staging, any final package path, activation, or unit existed. No generator executed, no unit was created or started, and no static Review is requested.

Sealed R16 builder/control evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r16-builder-20260830T202443+0800`, 47-file manifest root SHA-256 `ec2aef2b27c17fc33c80a98d98a1ae01d167e3d8ed285d2dc92768dd7915fe43`.

## Authorization, frozen contracts, and inherited-root result

- The ledger prewrite bound exact owner/profile/mode, current `remediating` gate, exact product commit/tree, durable R15 handoff path/SHA, and the retained R14/R15 failure attempts without depending on mutable `blocker.summary`.
- Before using inherited design facts, R16 independently verified all 28 sealed R15 manifest rows/root `9a7068d638b497b9abd2ad433034e23eda830f27133975d25038587316b0ae7a` and all 26 sealed R14 rows/root `f38988ddf2c9a6aca3e43310fb4a978ea16c3e8cb6d4a8011cbf98da23ecf25f`.
- R16 froze the product API/event catalog, lock order and transaction/publication boundaries, sensitive-payload allowlist, exact final path set, full package contract, and acceptance-to-static-test mapping before deriver work.
- The host deriver was built from a fresh file-backed template. A complete construction helper was explicitly compiled in memory under host Python `3.6.8` before publishing `derive-r16.py`; the deriver itself was also compiled in memory before its fresh `O_EXCL` publication. No generated triple-single-quoted code was embedded inside a triple-single-quoted outer literal.

## Failure matrix

| Failure | Symptom | Root cause | Safety result / successor boundary |
|---|---|---|---|
| R16 prewrite 1: `r16_deriver_prewrite_failure` | The actual-source AST/dataflow gate reported safe postpublication uses of `entries` and `lines` as moved-source reads. | The inherited R14 analyzer propagated staging-source taint through materialized metadata/digest values and treated every later variable load as a path dereference. It therefore over-tainted values that no longer represented source paths. | Attributed through `cyf_orchestrator.py fail`. `build-r16.py`, staging, all final paths, activation, and unit remained absent. The sole retry used a fresh non-overwriting template/deriver and narrowed the analysis to path-preserving aliases plus operation-aware read/open/stat/hash sinks. |
| R16 bounded retry: `r16_retry_deriver_failure` | The corrected gate reported one post-rename `stat` of `WORK` at generated-source line 625. | The retry scanned a `for` statement's body for sink calls **before** rebinding the loop target. Variable `p` retained `WORK` taint from an earlier staging-path loop, so `os.stat(p)` in a later loop over `FINAL_*` metadata paths was falsely classified as a staging-source stat. | Attributed through `cyf_orchestrator.py fail`; this was the second consecutive failure. Stop R16. A successor must bind `For` targets before scanning their bodies, or use equivalent statement-order CFG semantics, while retaining all other R16/R13 gates. |

## Passed R16 preparation facts

- File-backed original and retry templates compiled under Python 3.6. Both complete construction helpers were compiled in memory before their corresponding fresh deriver files were published.
- The corrected retry dataflow design retained rename-source self-dependency through defining assignments and operation-aware source/path-alias propagation for read/open/stat/hash sinks.
- Both derivers retained eight direct/alias fixture definitions covering read, open, stat, and hash through direct source names, source aliases, and derived path aliases. The actual-source gate failed before fixture evidence or generator creation because the fail-closed actual-source check runs first.
- The intended generator remained the exact R13 donor transformation with a complete `expected_digest_by_final_destination` frozen before the first `rename_noreplace`, destination-only post-rename verification, external-cfile compile isolation, independent `O_CREAT|O_EXCL` copies, hardlink-negative, donor metadata preservation, JDK 677/676, UID/GID 61019, ONLINE=9/OFFLINE_AUTHORITATIVE=8, exact `PACKAGE_PATHS`, fault injection, fail-closed activation, and unit-last publication. None of those generator/package rows executed in R16.

## Preservation and fail-closed state

- R15 before/after preservation is exact: 33 entries, root SHA-256 `c2d47e9740bbf6bbef697d2c54cf06411de806645ac5aeb5920f886183883bd4`.
- R14 before/after preservation is exact: 31 entries, root SHA-256 `01ee48157646b3f8bc3d75380fbe4d1ec3854d3e67f1ea066862faa3a129b574`.
- Complete R13 before/after preservation is exact: 461 entries, root SHA-256 `482b09867015ff397048575409df13183af9209f0b4b879f039e5d4644a0b902`.
- No R15/R14/R13 path was edited, deleted, chmod/chown modified, hardlinked, or reused. The historically contaminated R3/R4/R5 Maven inodes were not read, modified, restored, or linked.
- All R16 final destinations, publish staging, and `build-r16.py` are absent. `GENERATOR_EXECUTIONS=0`, `COMMIT_POINT_REACHED=false`, and the state is fail-closed.
- Read-only unit queries show R9–R16 inactive/dead or not-found with `MainPID=0`, `ControlPID=0`, `NRestarts=0`, and zero journal lines since R16 authorization.
- No Gradle, DB, RabbitMQ, Chromium, daemon reload, unit start/stop/restart, production access, deployment, or product-source mutation occurred.

## Evidence keys

- R16 builder root: `ec2aef2b27c17fc33c80a98d98a1ae01d167e3d8ed285d2dc92768dd7915fe43` (47 files)
- authorization record: `d297e5dd0b58a58b7b668a7ad1b47ebac1a687d33339b1b63b3e476236c5f8e8`
- original deriver construction proof: `deriver-construction-proof.json` in the sealed builder
- retry deriver construction proof: `deriver-retry-construction-proof.json` in the sealed builder
- first failure stderr: `29e0adb109a8036ca810189071ea06f3fd66ebb9af6e05bab1f0ea10859a7993`
- second failure stderr: `f2424f9d34296ab581c85836b139e31a8066e6e973b46c25ccf90461305e7eb6`
- preservation comparison: `preservation-comparison.json` in the sealed builder
- final-path absence proof: `final-paths.after-second-failure.txt` in the sealed builder
- unit read-only proof: `unit-never-started.json` in the sealed builder
- exact source-after-failure proof: `source-exact-after-failure.json` in the sealed builder

## Ledger and exact successor remediation

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r16_retry_deriver_failure`, consecutive failures `2`. Do not transition R16 to Review and do not appoint a Reviewer.

Only a main controller may separately authorize a fresh non-overwriting R17 against this matrix. R17 must:

1. bind authorization to this durable R16 handoff path/SHA, the sealed R16/R15/R14 builder roots, retained R16/R15/R14 attempts, exact new owner/profile/mode, and exact product commit/tree without depending on mutable `blocker.summary`;
2. preserve every R16/R15/R14/R13 path exactly and avoid all contaminated R3/R4/R5 Maven inodes;
3. use a file-backed Python-3.6-precompiled construction path and fresh R17 inodes only;
4. fix statement ordering in the AST/dataflow engine so each `For` target is rebound from its current iterable before its body is checked, preventing stale taint while preserving source-variable self-dependency;
5. run the actual-source zero-violation gate and all eight direct/alias read/open/stat/hash negative fixtures before creating `build-r17.py`;
6. retain complete pre-rename destination digest freezing and destination-only post-rename verification;
7. freshly execute every inherited R13 package contract and publish the R17 unit last, without Gradle, DB, RabbitMQ, Chromium, daemon reload/start, production, or deployment;
8. attribute any first R17 failure before one bounded retry and stop again on a second consecutive failure.
