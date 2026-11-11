# OPS-RESOURCE-TELEMETRY R7 Review Root Cause

Date: 2026-08-29 CST

Exact candidate:

- commit: `f911f7720549cbd6f2f143e53ee3f5ecf1b4593e`
- tree: `667064603a2e137086eb290ff8f242f7795229fd`
- reviewer: `01a04c0c-f339-7263-a82c-ffd95350a3b1`
- verdict: REJECT, P0/P1/P2=`0/1/1`

## Root-cause matrix

| Finding | Symptom | Root cause | Bounded remediation | Required proof |
|---|---|---|---|---|
| P1 approval path-swap rollback | A pre-link approval path swap can leave the replacement active and original backup present; immediate legal retry fails. | The exception/fail-closed branch before/around link validation does not enter the same rollback/restore contract as later mutation failures. | Make every pre-commit approval/path identity mismatch restore the original active path and remove transient backup/consumed state without weakening nlink/identity checks. | Add an adversarial real-filesystem path-swap test asserting original active `nlink=1`, no backup/consumed residue, and immediate legal retry PASS. |
| P2 operator documentation | README examples invoke stock CLI mutation commands that the documented executor-only capability boundary rejects. | Examples were not updated when mutation authority moved behind the config-pinned controller executor. | Replace rejected stock CLI mutation examples with the exact executor invocation or explicitly label them as rejection probes; keep read-only status examples distinct. | Documentation command audit plus existing config-pinned/capability tests. |

## Constraints

- Preserve K1 review identity across done/integrated transitions.
- Preserve config-pinned executor capability and fail-closed stock CLI behavior.
- Do not add process preemption, kill primitives, or cross-thread process/evidence operations.
- Scope writes to `ops/orchestration/cyf_orchestrator.py`, its direct tests, and `docs/implementation/README.md` only.
- Fresh exact-tree tests and an independent read-only Review are required.
