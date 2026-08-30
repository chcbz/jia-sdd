# PWA API R19 R15 builder root-cause matrix — 2026-08-30

Exact product source remained unchanged and clean throughout: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The main controller authorized fresh R15 remediation at `2026-08-30T20:01:28+08:00` for exact writer `01a0528b-6d19-7853-83e5-4a4b325290c4` (`critical_worker`, `writer`) against durable handoff `docs/implementation/handoffs/PWA-INTEGRATION-API-R19-R14-BUILDER-ROOT-CAUSE.md`, SHA-256 `98da293e5ce9201352a04dd1c43400df634ed2fc5aed67c68af62897650bc5fd`. R15 stopped under the second-consecutive-failure policy before `derive-r15.py`, `build-r15.py`, publish staging, any final package path, activation, or unit existed. No generator executed, no unit was created or started, and no static Review is requested.

Sealed R15 builder/control evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r15-builder-20260830T200446+0800`, 28-file manifest root SHA-256 `9a7068d638b497b9abd2ad433034e23eda830f27133975d25038587316b0ae7a`.

## Authorization and inherited-root result

- The initial ledger inspection bound the exact current agent/profile/mode and product commit/tree. The first scripted read-only preflight then failed only because host `/usr/bin/python3` is Python 3.6 and does not support the `subprocess` `text=True` alias.
- That failure was attributed through `cyf_orchestrator.py fail`. The sole bounded retry used `universal_newlines=True` and passed.
- The successful retry bound authorization directly to the durable R14 handoff path and SHA, exact current owner/profile/mode, exact product commit/tree, the retained R14 failure attempts/evidence, and the current R15 retry attempt. It explicitly recorded `blocker_summary_dependency=false`; it did not require a superseded matrix path in mutable `blocker.summary`.
- Before using the corrected design, the retry independently verified all 26 sealed R14 manifest rows and recomputed root `f38988ddf2c9a6aca3e43310fb4a978ea16c3e8cb6d4a8011cbf98da23ecf25f`. The sealed R14 `derive-r14.retry.py` SHA-256 remained `dce63b6060ad326743bc6fa15b5e4d0807b1d58c0f5ae13f9aea2acf01fcb6f1`.
- R15 froze seven pre-implementation contract/catalog files: product API/event catalog, lock and transaction boundaries, sensitive-payload allowlist, final path set, full frozen contract, acceptance-to-static-test coverage, and the bounded-retry contract.

## Failure matrix

| Failure | Symptom | Root cause | Safety result / successor boundary |
|---|---|---|---|
| R15 prewrite 1: `r15_prewrite_python36_subprocess_text_keyword` | A read-only authorization helper exited before writing authorization evidence because `subprocess.check_output(..., text=True)` raised `TypeError`. | The helper used a Python 3.7+ keyword alias on the host Python 3.6 runtime. | Attributed through `cyf_orchestrator.py fail`. No product, R14, R13, staging, final, activation, or unit path was changed. The sole retry used `universal_newlines=True`, passed exact authorization, independently verified the R14 root, and froze the R15 contracts. |
| R15 retry: `r15_deriver_nested_triple_quote_syntax` | The attempted fresh `derive-r15.py` construction command was rejected by the Python parser at line 22 before executing any helper statement. | The construction helper embedded generated `DATAFLOW_FUNCTION=r'''...'''` text inside an outer raw triple-single-quoted Python literal. The nested delimiter terminated the outer literal and made the helper syntactically invalid. | Attributed through `cyf_orchestrator.py fail`; this was the second consecutive failure. `derive-r15.py`, `build-r15.py`, staging, final package, activation, and unit paths all remain absent. Stop R15. |

## Frozen but unexecuted R15 design

The frozen R15 contract retained the required corrected design:

- preserve rename-source self-dependency through source-defining assignments;
- execute direct and alias post-rename negative fixtures before generator creation;
- freeze a complete immutable expected digest catalog before the first `rename_noreplace`;
- after each move, inspect/hash only final destinations against precomputed digests and reject any moved-source or path-bearing-alias read/open/stat/hash;
- retain Python 3.6 external-cfile compilation, zero PREP bytecode/control logs, independent `O_CREAT|O_EXCL` donor copies, hardlink-negative checks, donor metadata preservation, JDK 677/676, UID/GID 61019, ONLINE=9/OFFLINE_AUTHORITATIVE=8, exact `PACKAGE_PATHS`, fault injection, fail-closed activation, and unit publication last.

None of these generator/package acceptance rows executed in R15 because the second failure occurred while parsing the host-side deriver-construction helper. They are unexecuted, not failed product or package tests.

## Preservation and fail-closed state

- Fresh R14 before/after preservation manifests are exact: 31 entries, root SHA-256 `01ee48157646b3f8bc3d75380fbe4d1ec3854d3e67f1ea066862faa3a129b574`.
- Fresh R13 before/after preservation manifests are exact: 461 entries, root SHA-256 `482b09867015ff397048575409df13183af9209f0b4b879f039e5d4644a0b902`.
- No R14/R13 path was edited, deleted, chmod/chown modified, hardlinked, or reused. The historically contaminated R3/R4/R5 Maven inodes were not read, modified, restored, or linked.
- All R15 final destinations, publish staging, `build-r15.py`, and `derive-r15.py` are absent. `GENERATOR_EXECUTIONS=0`, `COMMIT_POINT_REACHED=false`, and the state is fail-closed.
- Read-only unit queries show R9 loaded/inactive/dead and R10-R15 not-found/inactive/dead, all with `MainPID=0`, `ControlPID=0`, `NRestarts=0`, and zero journal lines since authorization.
- No Gradle, DB, RabbitMQ, Chromium, daemon reload, unit start/stop/restart, production access, deployment, or product-source mutation occurred.

## Evidence keys

- R15 builder root: `9a7068d638b497b9abd2ad433034e23eda830f27133975d25038587316b0ae7a` (28 files)
- successful authorization retry: `fa2fff5caec3e6f0c1f69c7595834c48b217895a1ae57157d18d05f6a16b63d5`
- independent R14 verification record: `8b6e770c1a5d80a48754d795f7845932f60808f22a895852fea359a4b9fc6e81`
- first failure: `4c138e254677fba5b5353c9519fa1103d1ce9e3c732be5732f9d81ca6446e958`
- second failure: `8565cfeee5660790c32d70825661dbc66760fc5d0fcc52aa8f2a67091ac48a9c`
- preservation comparison: `0a10722b80d132026eec98e297b5c9a532d82abfaa333214608e9dde289a4e9c`
- final-path absence proof: `1a15211f2da0f3dc734042872e169dd04556b7f6b9feaa80822e590d9738a0f0`
- unit read-only proof: `f5dff0622b2994281164b5260adf93267f11b0a39870ad7935eba023dd79b3f8`
- exact source-after-failure proof: `8c6736c008be361fb1e9bc6d962adf500ea526e1b0660b97baed94a4b17788c6`

## Ledger and exact successor remediation

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r15_deriver_nested_triple_quote_syntax`, consecutive failures `2`. Do not transition R15 to Review and do not appoint a Reviewer.

Only a main controller may separately authorize a fresh non-overwriting R16 against this matrix. R16 must:

1. bind authorization to this durable R15 handoff path and SHA, retained R15/R14 attempts, exact new owner/profile/mode, and exact product commit/tree without depending on mutable `blocker.summary`;
2. independently verify the sealed R15 builder root and the sealed R14 builder root before using any frozen design facts; never modify, complete, chmod/chown, delete, hardlink, or reuse R15/R14/R13 paths;
3. build the deriver with a file-backed template or non-conflicting triple-double-quoted outer literals, and compile the complete construction helper in memory before publishing a fresh deriver file;
4. preserve source-variable self-dependency through defining assignments and run both direct and alias post-rename read/open/stat/hash negative fixtures before generator creation;
5. freeze expected digests for every publication destination before the first rename, verify only final destinations after each rename, and enforce the actual AST/dataflow zero-violation gate;
6. freshly execute every inherited R13 package contract and publish the R16 unit last, without Gradle, DB, RabbitMQ, Chromium, daemon reload/start, production, or deployment;
7. attribute any first R16 failure before one bounded retry and stop again on a second consecutive failure.
