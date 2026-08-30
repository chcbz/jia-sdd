# PWA API R19 R11 builder/package root-cause matrix — 2026-08-30

Exact source remains unchanged and clean: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

R11 reached one generator execution after the required in-memory gates passed. It stopped before publication; every final R11 path is absent. The R11 unit was never loaded or started, and no Gradle, DB, RabbitMQ, Chromium, production access, deployment, or product-source write occurred.

Sealed R11 builder/staging evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r11-builder-20260830T131539+0800`, root SHA-256 `a761c9a58a37a3be3a8f812a6efdf3fe18665342c91d64c1c6bd00a3a6772e1b`.

| Failure | Root cause | Required bounded remediation if separately authorized | Acceptance proof |
|---|---|---|---|
| Pre-write probe 1 rejected on Python syntax before any R11 path creation. | The host probe used a Python 3.8 assignment expression although the host/runtime is Python 3.6.8. The failure was attributed before the single retry. | Preserve the first attribution. Any successor must use Python-3.6-compatible syntax from its first in-memory probe. | No R11 path existed at failure; ledger attribution `r11_prewrite_python36_walrus_syntax` is retained. |
| Generator execution 1 stopped because the complete staged fault fixture returned `ACTIVATION_REJECT path_set`. | R11 generated `PACKAGE_PATHS.json`, then ran `py_compile` against scripts located inside staged PREP. Python created staged `__pycache__` directories/files after the path-set snapshot. The activation checker correctly rejected those unlisted objects. This is a verifier-package ordering/isolation defect, not a product-source verdict. | Stop under the second-consecutive-failure policy. If a main controller later authorizes a fresh successor, compile package scripts before the PREP path-set snapshot or direct bytecode caches to a fresh control-plane directory outside PREP (for example with an explicit cache prefix), then prove PREP cannot gain paths between snapshot and publication. Do not delete or repair R11 staging. | Fault injection complete state passes without adding/removing PREP objects; full path-set replay reports zero unexpected paths; a negative fixture that creates one post-snapshot cache object is rejected. |

## Passed pre-write safety facts

- Function-level edit cardinality was frozen exactly once for `tree_lines`, `verify_authorization`, and the R10 broad transformer replacement; direct exact-edit cardinalities are recorded in `prewrite-edit-cardinality.json`.
- Immutable R5 JDK full identity passed: `677:995e2193a455aff46f74d8bdfe9ac3e225df8f14fd867334fa6cc471a305c631`.
- Immutable R5 JDK byte projection passed with the root excluded: `676:ecf40b2b91cbfac66614519e1541c7dd57cfca62e7cb76ee4c7e1cb64d376c15`.
- Actual R11 builder AST contained zero executable assignments to `sys.excepthook`; the injected assignment fixture was detected.
- Actual builder AST contained no hardlink/copy helper call and no broad `r9`/`R9`/`r10`/`R10` `str.replace` arguments.
- The R9-final eight private-plugin donors and six H06 donors remained metadata-exact after the failed staging attempt; staged copies were independent `O_CREAT|O_EXCL` byte copies.
- The negative hardlink test passed before the fault-injection stop.

## Preserved state

- All final R11 wrapper, sealer, unit, PREP, evidence, workspace, incidents, and activation paths are absent.
- R11 remains `not-found/inactive/dead`, `MainPID=0`, `ControlPID=0`, `NRestarts=0`, with zero journal lines.
- R9 and R10 were not started, stopped, restarted, edited, or executed.
- R10 sealed builder remains unchanged at `/var/tmp/cyf-pwa-api-r19-static-verifier-r10-builder-20260830T125524+0800`.
- R11 failed staging is preserved read-only under the sealed builder root; no cleanup or retry is authorized.
- R3/R4/R5 Maven evidence remains contaminated/non-authoritative, with no metadata restoration.

The ledger must remain `blocked_root_cause` with no owner. A fresh controller authorization and fresh writer are required for any successor. No static Review request is appropriate for the failed R11 package.
