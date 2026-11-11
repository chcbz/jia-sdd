# OPS-RESOURCE-TELEMETRY R9 Review Root Cause

Date: 2026-08-29 CST

Exact `bca954d1071e2c72f13c8bb5459d23e85a14f4f4` / tree `3a5c1c43cc8fd00764f5253150f8d8197fd6647e`; reviewer `01a04c54-5c72-7f02-8eba-5cf97da626fa`; REJECT `0/2/1`.

## Bounded R10 matrix

1. **Snapshot unlink race:** before unlinking the named `mkstemp` entry, use its parent descriptor and exact `(dev, ino, regular-type)` identity; if replaced, preserve the foreign entry and safely detach/close only the still-owned snapshot. Add a deterministic replacement-between-create-and-unlink test.
2. **Final active restore race:** treat `RENAME_NOREPLACE/EEXIST` as a recovery loop: preserve/quarantine the foreign active object, retain exact recovery ownership, retry the no-replace restore, then verify exact original and immediate same-nonce retry. Never leave the original hidden under `.recovery-*` while accepting a foreign active record.
3. **Docs/evidence:** update README to preservation/quarantine semantics; strengthen docs tests. Remove only generated `.pyc` files, regenerate focused/5/45 envelopes on a clean exact tree, and register/recompute their cache records.

Preserve K1/K2, executor capability, stock CLI fail-closed, and no-preemption. No Gradle or production.
