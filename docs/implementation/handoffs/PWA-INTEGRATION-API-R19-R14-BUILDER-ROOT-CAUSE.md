# PWA API R19 R14 builder root-cause matrix — 2026-08-30

Exact product source remained unchanged and clean throughout: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The main controller authorized fresh R14 remediation at `2026-08-30T19:41:50+08:00` for exact writer `01a05279-9758-7753-9ede-d5e0509cfe0b` (`critical_worker`, `writer`) against `PWA-INTEGRATION-API-R19-R13-BUILDER-ROOT-CAUSE.md`, SHA-256 `3a33a173c389e921c6366f8bff2fd6e47cd6d3dc992078a67d775964363936f6`. R14 stopped under the second-consecutive-failure policy before `build-r14.py`, publish staging, any final package path, activation, or unit existed. No generator executed, no unit was created or started, and no static Review is requested.

Sealed R14 builder/control evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r14-builder-20260830T194356+0800`, 26-file manifest root SHA-256 `f38988ddf2c9a6aca3e43310fb4a978ea16c3e8cb6d4a8011cbf98da23ecf25f`.

## Failure matrix

| Failure | Symptom | Root cause | Safety result / successor boundary |
|---|---|---|---|
| R14 prewrite 1: `r14_prewrite_dataflow_source_identity_overwritten` | The executable AST/dataflow negative fixture `alias=PREP; rename_noreplace(PREP,...); sha(alias)` was not rejected. The deriver stopped before writing `build-r14.py`. | The gate initially seeded every rename-source variable with a self-dependency, but then ordinary source-defining assignments such as `PREP=STAGE+'/preparation'` replaced that dependency with an empty set. Alias propagation therefore lost the staging-source identity before the publication boundary. | Attributed through `cyf_orchestrator.py fail`; all R14 staging/final paths remained absent. The sole retry used a fresh `derive-r14.retry.py` and preserved source-variable self-dependency on assignment. |
| R14 prewrite retry: `r14_retry_authorization_matrix_summary_not_retained` | The retry authorization preflight raised `prewrite_matrix_binding_missing` before reading or transforming the R13 donor into `build-r14.py`. | The first `fail` transition correctly replaced the mutable `blocker.summary` with the new R14 failure summary. The retry incorrectly required the older R13 matrix path to remain in that mutable summary, although matrix authority remained durable in the frozen R14 authorization record, the retained R13 attempt, and the R13 handoff SHA. | Attributed through `cyf_orchestrator.py fail`; this was the second consecutive failure. Stop R14. Preserve the sealed partial builder and all R13 paths. Only a separately authorized fresh non-overwriting successor may continue. |

## Frozen R14 contract and partial implementation facts

- Before source editing, R14 froze the product API/event catalog, control events, lock order, publication/commit boundaries, sensitive-payload allowlist, final path set, and acceptance-to-static-test coverage under the builder root.
- The intended minimal generator change was frozen as: compute a complete immutable `expected_digest_by_final_destination` before the first `rename_noreplace`; after publication inspect/hash only final destinations; never read, open, stat, or hash a consumed staging source.
- `derive-r14.py` SHA-256 is `633bc782c0db5e1835504eeab3e88eb8c1d6ed685c2670047de8a3229bd4cb0b`. Its negative-gate defect was detected before generator creation.
- Fresh non-overwriting `derive-r14.retry.py` SHA-256 is `dce63b6060ad326743bc6fa15b5e4d0807b1d58c0f5ae13f9aea2acf01fcb6f1`. It contains the bounded source-self-dependency correction, but stopped at authorization preflight and is not successful generator evidence.
- The retry did not execute the donor transformation, Python compile gate, JDK gate, package build, fault injection, activation check, or publication. Those acceptance rows remain unexecuted, not failed product tests.
- `build-r14.py`, `publish-staging`, PREP, wrapper, sealer, evidence, workspace, incidents, activation, and R14 unit paths are all absent. `GENERATOR_EXECUTIONS=0`, `COMMIT_POINT_REACHED=false`, and the state is fail-closed.

## Preservation and prohibited-operation evidence

- R13 before/after preservation manifests are byte-exact: 461 entries, root SHA-256 `7d900128c1a2ffc8527f251b83a8a43d8bf2168c09d9cf4711e353a9bacdca20`. Every R13 partial/final/builder path remains preserved; no in-place repair, deletion, chmod/chown, hardlink, or path reuse occurred.
- The historically contaminated R3/R4/R5 Maven inodes were not modified or restored.
- Read-only unit queries for R9 through R14 show no runtime activity after authorization: no MainPID/ControlPID, no restart, and zero new journal lines. No daemon reload, start, stop, or restart occurred.
- No Gradle, DB, RabbitMQ, Chromium, production access, deployment, default `python -m py_compile`, or product-source mutation occurred.
- Evidence keys:
  - builder root: `f38988ddf2c9a6aca3e43310fb4a978ea16c3e8cb6d4a8011cbf98da23ecf25f`
  - R13 preservation root: `7d900128c1a2ffc8527f251b83a8a43d8bf2168c09d9cf4711e353a9bacdca20`
  - first failure stderr: `00bda1c4f0b774149aa8f458cf49c7d8d38c79f718816c0c7e014e3f19a7fee5`
  - retry failure stderr: `31dffaeffbc2adc199e00bc5255ee3a29a6ce6efdb3005dbb29ceb0d348d03fe`
  - final-path absence proof: `e444c2b07c06c824daff0527e6e2bcd322297b346663e2b318515fa7065ec4d0`
  - unit read-only proof: `bfd9dbb40cddecbf10e31674c4fd3a0c548f7710aa5c1c7bf02ccbb1b115b7bd`

## Ledger and exact successor remediation

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r14_retry_authorization_matrix_summary_not_retained`, consecutive failures `2`. Do not transition R14 to Review and do not appoint a Reviewer.

A main controller may authorize only a fresh non-overwriting successor against this matrix. The successor must:

1. bind current authorization to this durable handoff and its SHA, the retained R14 attempt evidence, exact owner/profile/mode, and exact product commit/tree; it must not require a superseded matrix path to remain in mutable `blocker.summary` after failure attribution;
2. independently verify the sealed R14 builder root before using the corrected dataflow design as a donor; never edit, complete, chmod/chown, delete, or reuse any R14 path;
3. retain source-variable self-dependency through source-defining assignments and execute both direct and alias post-rename negative fixtures before creating a generator;
4. freeze every final-destination digest before the first rename and prove by AST/dataflow inspection that no moved staging source or path-bearing alias is read after its move;
5. freshly execute all inherited R13 safety contracts, including external-cfile Python 3.6 compilation, zero PREP bytecode/control logs, independent donor copies and metadata preservation, hardlink-negative, JDK 677/676, UID/GID 61019, ONLINE=9/OFFLINE_AUTHORITATIVE=8, exact `PACKAGE_PATHS`, fault injection, fail-closed activation, and unit publication last;
6. attribute any first failure before one bounded retry and stop again on a second consecutive failure.
