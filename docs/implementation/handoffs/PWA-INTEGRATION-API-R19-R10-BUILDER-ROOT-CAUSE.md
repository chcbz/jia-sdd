# PWA API R19 R10 builder-only root-cause matrix — 2026-08-30

Exact source remains unchanged and clean: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The authorized fresh R10 package generator was **not executed**. A direct patch of the newly written builder draft failed before staging or final-path creation. Because the ledger retained one consecutive R9 static Review failure, this is the second consecutive task failure and the orchestration stop policy applies. No retry, Gradle, DB, RabbitMQ, Chromium, production access, deployment, or R9/R10 unit start occurred.

Sealed builder evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r10-builder-20260830T125524+0800`, root SHA-256 `d8167af07134fc53ff630d6e8f6736831cfae08e530645387fba76add19d89fd`.

| Finding | Root cause | Required bounded R11 remediation | Acceptance proof |
|---|---|---|---|
| Direct patch helper raised `AssertionError` and applied no edit. | The exact anchor assumed an inline `rr == '.'` root-record block, while the actual draft uses a `names = ['.']` helper loop. The compound shell continued to `py_compile`, so the unchanged draft remained syntactically valid but semantically uncorrected. | Preserve and do not execute or edit the sealed R10 builder. If the main controller authorizes R11, create a fresh builder and use function-scoped AST/direct edits whose target cardinality is computed and recorded before any write. A failed edit must stop immediately under `set -e`. | Pre-write diff/AST evidence proves each intended function-scoped edit exactly once; no generated staging/final path exists before all edits and in-memory contract probes pass. |
| Read-only diagnosis found the unchanged draft would generate the wrong immutable-JDK content projection. | `tree_lines(..., content=True)` still includes the root `.` entry, producing 677 rather than the frozen 676 descendant entries and therefore a digest mismatch. | R11 must construct the full-identity and byte-content projections in memory and compare them against the immutable R5 manifests before creating any staging path. Root is included only in full identity, never in byte projection. | Full identity `677:995e2193...`; byte projection `676:ecf40b2b...`; source/R5 metadata unchanged. |
| Read-only diagnosis found a tautological self-scan. | The draft checks whether its own source text contains `sys.excepthook`; the check literal itself guarantees rejection. | Replace all source-text self-scans with AST queries over executable assignment/call nodes only. Keep the publication contract crash-safe fail-closed and do not use exception cleanup as a safety boundary. | Negative fixture assigning `sys.excepthook` is rejected; the actual builder has no such AST assignment and passes. |

## Preserved state

- R10 final wrapper, sealer, unit, PREP, evidence, workspace, incidents, activation record, and staging root are all absent.
- R9 unit: `loaded/inactive/dead`, `MainPID=0`, `ControlPID=0`, `NRestarts=0`, zero journal lines.
- R10 unit: `not-found/inactive/dead`, `MainPID=0`, `ControlPID=0`, `NRestarts=0`, zero journal lines.
- R3/R4/R5 and R9 attempt1/final remain untouched; no chmod/chown/unlink/relink/metadata restoration was performed.
- The source worktree remains clean and exact.

## R11 boundary if separately authorized

R11 must remain a fresh non-overwriting verifier-package/control-plane remediation only. It must retain the intended R10 contract: R9-final nlink=1 private-plugin files as independent `O_CREAT|O_EXCL` donors with before/after/current metadata equality; H06 six-file independent donor copy; contaminated R3/R4/R5 Maven evidence excluded from acceptance; immutable R5 JDK read-only reuse; UID/GID `61019:61019`; ONLINE=9/OFFLINE=8; direct staged Gradle; mount/cgroup/seal invariants; a mechanically proven **crash-safe fail-closed** activation commit point without crash-atomic overclaim; complete PREP path-set binding; and all control/review logs outside PREP. Fresh independent static Review remains mandatory before any unit start.
