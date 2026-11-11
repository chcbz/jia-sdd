# OPS-RESOURCE-TELEMETRY R8 Review Root Cause

Date: 2026-08-29 CST

Exact candidate:

- commit: `6b4e855278dcb69cbbb76ffbac0b1f673dd58b81`
- tree: `221131c32bd6390fa70a104a2bac60eb0c38f502`
- reviewer: `01a04c29-9c39-7a62-9f48-c20f7abd8f8b`
- verdict: REJECT, P0/P1/P2=`0/2/1`

## Root-cause matrix

| Finding | Symptom | Root cause | Bounded R9 remediation | Required proof |
|---|---|---|---|---|
| Original inode mutated in place | After verified descriptor, chmod/content mutation poisons rollback; active is not exact and immediate same-nonce retry fails. | Rollback preserves path/inode but lacks an immutable original snapshot from which exact bytes/uid/gid/mode can be restored. | Before any externally visible consume transition, create a controller-owned exact snapshot with pinned identity/digest/metadata; on failure restore from that snapshot using descriptor-relative operations and revalidate exact retriable state. | Real FS chmod, truncate/content overwrite, uid/mode/size changes after verification all end with original exact active `nlink=1`, no residue, immediate same-nonce legal retry PASS. |
| Directory/path replacements | `unlink` on directory replacement fails; original remains in consumed or temp roots and nonce stays poisoned. | Cleanup assumes every unexpected path object is a regular file/symlink and uses path-level unlink without type-aware quarantine. | Never delete an unowned replacement. Move unexpected objects to a controller-owned collision-proof quarantine inside the same trusted root using descriptor-relative no-follow operations; restore original independently; if safe quarantine cannot be proven, fail without deleting or overwriting the replacement and preserve recoverable original. | Active/stage/consumed path replaced by file, symlink, directory, FIFO variants; no unowned inode deletion, no mistaken restore, exact original recoverable, immediate retry semantics explicitly proven. |
| Replacement destruction | Rollback renames then unlinks replacement without proving ownership. | Ownership/provenance is inferred from path location rather than inode identity created by this consume. | Delete only inodes created by the current operation and recorded by exact `(dev, ino)`; preserve/quarantine every foreign replacement. | Reviewer probe's replacement inode survives byte-exact; controller-created temp files alone are removed. |
| Evidence binding | PASS logs omit exact commit/tree/command/fixture/evidence key and cache has no record for target tree. | Direct unittest runs were not wrapped in a canonical exact-tree evidence envelope. | Generate a manifest/log header binding HEAD/tree, clean status, selector, fixture digest, full argv, artifact SHA; record evidence keys or durable equivalent. | Focused, 5/5, and full suite evidence independently recomputes to the new exact tree and worktree is clean before/after. |

## Constraints

- Preserve K1/K2 identity, config-pinned executor, stock CLI fail-closed, README correctness, and no-preemption behavior.
- Scope remains `ops/orchestration/cyf_orchestrator.py`, direct tests, and only necessary docs/evidence-envelope helper in `ops/orchestration/`.
- No Gradle, production, cross-thread process, or foreign evidence operations.
- Fresh independent Review is mandatory.
