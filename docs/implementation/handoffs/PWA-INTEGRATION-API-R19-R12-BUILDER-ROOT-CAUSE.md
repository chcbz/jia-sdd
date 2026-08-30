# PWA API R19 R12 builder/package root-cause matrix — 2026-08-30

Exact product source remained unchanged and clean throughout: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

The main controller authorized R12 remediation at `2026-08-30T13:30:48+08:00` for exact writer `01a05125-d62e-76f0-b394-5d6ee828d64c` (`critical_worker`, `writer`) against `PWA-INTEGRATION-API-R19-R11-BUILDER-ROOT-CAUSE.md`. R12 stopped under the second-consecutive-failure policy before `build-r12.py`, staging, package, or any final R12 path was created. No static Review is requested for this failed package.

Sealed failed R12 builder/control evidence: `/var/tmp/cyf-pwa-api-r19-static-verifier-r12-builder-20260830T133558+0800`, root SHA-256 `9bf41b1fabc6a933ee120fedc29b72942c77d77408e2534b04050f0d48367a4d`.

| Failure | Symptom | Root cause | Result / bounded successor remediation |
|---|---|---|---|
| R12 prewrite 1: `r12_prewrite_exact_identity_cardinality_mismatch` | The in-memory deriver expected 20 occurrences of the exact token `cyf-pwa-api-r19-static-verifier-r11`; the immutable R11 generator contained 31 after the exact builder-path edit. | The host probe froze an incorrect exact-token cardinality. | Attributed through `cyf_orchestrator.py fail`; no `build-r12.py`, staging, package, or final path existed. One retry was permitted with cardinality 31 and ledger binding to failure count 1. |
| R12 prewrite 2: `r12_prewrite_multiline_static_anchor_mismatch` | The sole retry stopped at `static_ast_anchor_cardinality`. | A fragile multiline source-text anchor represented the injected Python source literal `\n` as real newline characters, while the immutable generator contains backslash-plus-`n` bytes. The first mismatch was at the literal boundary (`newline` versus `\\`). This was a host deriver defect, not a product or R11 verifier verdict. | Second consecutive failure: stop, owner cleared, gate `blocked_root_cause`. Any fresh successor must use AST/function-scoped insertion or byte-exact escaped anchors, with pre-counted cardinality, instead of this multiline text match. |

## Frozen R12 intent that was not executed

The fresh control plane froze these contracts before implementation:

- No product API/event change; verifier control events only.
- Lock order: `systemd_preflight > mount_activation > orchestrator > /tmp/cyf-gradle.lock > Gradle61019 > evidence_cache`.
- Transaction/publication boundary: stage/validate, freeze `PACKAGE_PATHS`, external static/fault checks, prove zero PREP path delta, publish content, publish activation while unit absent, verify, then atomic non-overwriting unit publication as the sole commit point, followed by post-publication path proof.
- Sensitive allowlist: hashes, test names/counts, placeholder credentials, telemetry, PID/PPID/cgroup/mount facts, donor metadata, and path manifests. Environment dumps, real credentials/tokens, OAuth/PKCE values, DB/Rabbit passwords, and production payloads remain denied.
- Intended Python remediation: Python 3.6 `py_compile.compile(source, cfile=<builder-control>/<digest>.pyc, doraise=True)` with all bytecode/logs outside PREP; no default `python -m py_compile` against PREP scripts.
- Intended fault contract: complete fixture PASS, add one post-snapshot unlisted PREP path and REJECT, remove only the owned fixture, prove exact path-set restoration, complete fixture PASS again.

These intent files are evidence only. The generator was never created or executed, so they do not constitute package PASS evidence.

## Preserved and reverified facts

- R11 sealed builder remained byte-exact and read-only: `/var/tmp/cyf-pwa-api-r19-static-verifier-r11-builder-20260830T131539+0800`; all 391 manifest entries reverified; root remains `a761c9a58a37a3be3a8f812a6efdf3fe18665342c91d64c1c6bd00a3a6772e1b`.
- Exact source worktree remained clean at the bound commit/tree.
- `build-r12.py`, `publish-staging`, R12 PREP, wrapper, sealer, unit, evidence, workspace, incidents, and activation paths are all absent.
- R9 is `loaded/inactive/dead`; R10, R11, and R12 are `not-found/inactive/dead`; every unit has `MainPID=0`, `ControlPID=0`, `NRestarts=0`, and zero journal entries. No daemon reload, start, stop, or restart occurred.
- No Gradle, DB, RabbitMQ, Chromium, production access, deployment, or default `python -m py_compile` execution occurred. Only Python 3.6-compatible in-memory `compile(...)` probes ran.
- R3/R4/R5 contaminated Maven evidence was not accessed for repair and remains non-authoritative.
- No donor, JDK, package, or product-source mutation occurred.

## Ledger and next action

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r12_prewrite_multiline_static_anchor_mismatch`, consecutive failures `2`. Do not transition to Review and do not request `sol_reviewer` for R12.

A main controller may separately authorize only a fresh non-overwriting successor against this matrix. The successor must preserve every R11 contract and first perform Python-3.6-compatible, in-memory, function/AST-scoped edit-cardinality checks before creating its builder script or staging paths.
