# PWA API R19 R13 builder/package root-cause matrix — 2026-08-30

Exact product source remained unchanged and clean throughout: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The main controller authorized fresh R13 remediation at `2026-08-30T13:49:35+08:00` for exact writer `01a05137-0089-7151-864a-c485c535d5f7` (`critical_worker`, `writer`) against `PWA-INTEGRATION-API-R19-R12-BUILDER-ROOT-CAUSE.md`. R13 stopped under the second-consecutive-failure policy. No R13 unit was created or started, the activation commit point was not reached, and no static Review is requested.

Sealed R13 builder/control/residual-staging evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r13-builder-20260830T135417+0800`, 50-file manifest root SHA-256 `49b61dc187883b6eeb2065f1c7641087c63f975eab7ff96c59be634ae8d71452`.

| Failure | Symptom | Root cause | Result / bounded successor remediation |
|---|---|---|---|
| R13 prewrite 1: `r13_prewrite_python36_same_line_ast_end_annotation` | The host deriver stopped at `end_lineno_annotation_failed:7` before `build-r13.py`, staging, or final paths. | Python 3.6 has no native AST `end_lineno`. The bounded annotator used the immediately next top-level node, but donor line 7 contains several semicolon-separated `Assign` nodes sharing `lineno=7`, so it computed an invalid span. | Attributed through `cyf_orchestrator.py fail`. The sole retry used the next **strictly greater** top-level line, retained same-line siblings on their physical line, and reran all in-memory gates. |
| R13 generator execution 1: `r13_postpublish_moved_staging_digest_source` | Static compilation, AST negatives, JDK identities, independent donor checks, fault injection, PREP path-set checks, and prepublication proof passed. After content publication, the first postpublish digest check raised `FileNotFoundError` for `publish-staging/wrapper`. | `mappings` stores `(staging_source, final_destination)`. `rename_noreplace` consumed the staging PREP/wrapper/sealer/runtime paths, but the postpublish loop recomputed `sha(src)` instead of using an expected digest frozen before publication. | Sole generator execution stopped fail-closed. Preserve all R13 paths. A separately authorized fresh non-overwriting successor must freeze `expected_digest_by_final_destination` before any rename, compare only final destinations afterward, and add an AST/dataflow negative gate rejecting post-rename reads of consumed staging paths. |

## Passed R13 preparation contracts

- Immutable R11 donor was reverified: 391 manifest entries, sealed root `a761c9a58a37a3be3a8f812a6efdf3fe18665342c91d64c1c6bd00a3a6772e1b`; R12 partial evidence remained preserved and unexecuted.
- Exact identity occurrences were recorded by file, byte offset, line, column, and count before edits. Actual donor counts were: complete verifier identity `32`, init identity `12`, uppercase `R11` `5`, and `build-r11.py` `3`. Each exact old token reached zero and each R13 token retained the matching count. No global lowercase `r11` replacement occurred.
- AST-scoped replacement cardinality passed for one `verify_authorization` function and one top-level default-pycompile loop. The retry bound current ledger failure/count while retaining both exact R12 attempts and the R12 matrix SHA.
- Final builder SHA-256 was `b62671caa65e1e2b7c3e7b03b787bcc92bda1b70d08097612c759640cfddafb0`. Python 3.6 `compile(..., 'exec')` passed; executable AST had zero `sys.excepthook` assignments, hardlink primitives, broad version replacements, or default `python -m py_compile` calls.
- Eight package scripts compiled with explicit external `cfile` values under builder-owned `pycompile-control/`; PREP contains zero `__pycache__` or `.pyc` paths and zero control-log paths.
- Immutable JDK identities passed: full `677:995e2193a455aff46f74d8bdfe9ac3e225df8f14fd867334fa6cc471a305c631`; byte projection `676:ecf40b2b91cbfac66614519e1541c7dd57cfca62e7cb76ee4c7e1cb64d376c15`, root excluded.
- R9-final eight private-plugin donors and six H06 donors remained metadata-exact; staged copies were independent `O_CREAT|O_EXCL` byte copies. R3/R4/R5 Maven evidence remains contaminated/non-authoritative and untouched.
- Runtime catalog remained UID/GID `61019:61019`, `ONLINE=9`, `OFFLINE_AUTHORITATIVE=8`, direct staged Gradle bytes, and read-only source/JDK contracts.
- Negative hardlink test passed. Fault injection passed partial-state rejection, complete activation, wrapper tamper rejection, one post-snapshot unlisted PREP path rejection, owned-fixture removal, and restoration pass.
- Published PREP has exactly 393 bound paths and 367 package-manifest items; `PACKAGE_PATHS` is exact. A read-only activation check against published content plus staged activation/unit returned `ACTIVATION_PASS`.

## Fail-closed preserved state

- Present: final R13 PREP, wrapper, sealer, evidence, workspace, and incidents paths.
- Absent: `/var/tmp/cyf-pwa-api-r19-static-verifier-r13.activation.json` and `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r13.service`.
- Staged only under the sealed builder: `publish-staging/activation.json` and `publish-staging/unit.service`.
- The sole commit point—atomic non-overwriting final-unit publication—was not reached. The partial content is non-startable and must not be repaired, completed, or deleted in place.
- R9 is `loaded/inactive/dead`; R10-R13 are `not-found/inactive/dead`. All have `MainPID=0`, `ControlPID=0`, `NRestarts=0`, and zero journal lines. No daemon reload, start, stop, or restart occurred.
- No Gradle, DB, RabbitMQ, Chromium, production access, deployment, default `python -m py_compile`, or product-source mutation occurred.

## Ledger and next action

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r13_postpublish_moved_staging_digest_source`, consecutive failures `2`. Do not transition R13 to Review and do not request `sol_reviewer`.

Only a main controller may separately authorize a fresh non-overwriting successor against this matrix. It must preserve the partial fail-closed R13 paths, freeze all postpublication expected digests before consuming staging paths, and prove by AST/dataflow inspection that no post-rename verification dereferences a moved staging source.
