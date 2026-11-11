# JVC-OAI-OPS R6 review root-cause matrix

Date: 2026-09-04
Reviewed candidate: `713dfc488d0445a16f8793f07665cc76299f8b1c` / tree `22d69c58dd985b5a0c8e93783bc3fec937a150ba`
Review result: REJECT `P0/P1/P2 = 2/1/2`; no test, Gradle, production, credential, feature-flag, deployment, reload, or restart action occurred.

## Findings and bounded R7 remediation

| Priority | Finding | Root cause | Required R7 closure |
| --- | --- | --- | --- |
| P0 | Rollback/failed crash-replay coverage does not exercise both before/after-record-rename seams. | `health-failure` writes a completed rollback record; the E2E set does not inject `rollback-before-rename`, `rollback-after-rename`, or `failed-before-rename` at the exact production entrypoint. | Add exact activate-release entrypoint replay cases for rollback-before/after and failed-before/after rename. Each must restart/replay and prove fail-closed or exact recovery without runtime source/module rewriting. |
| P0 | Sensitive snapshot race coverage declares input/phase labels but runs mutations only before a single activation. | The test has no Cartesian execution across each sensitive input and `sealed_before_staged`, `staged`, `activating`, `activated`, `finalizing`, `finalized`, `rolled_back`, and `failed`; lock proof is not a live phase race. | Build and execute an actual per-input × per-phase matrix with deterministic in-entrypoint fault/race hooks. Prove snapshot mismatch is rejected for each state and no unsafe continuation occurs. |
| P1 | Evidence-root nonregular entries are checked only after manifest data is loaded. | `seal()`/`verify()` call external-manifest load/read before `result_names()` rejects FIFO/socket/symlink/hardlink. | Preflight and close the evidence root before any manifest/seal/verify read/use. Add order-sensitive tests proving forbidden entries prevent manifest consumption. |
| P2 | Fixed R6 controller manifest anchor conflicts with schema/fixture `round=R4`. | R6 anchor names were introduced without updating frozen round semantics. | Make the authoritative R7 anchor/schema/fixture round consistent and test it. |
| P2 | README reports R5/116 cases while inventory contains R6/124 cases. | Operational documentation was not advanced with the packet. | Update README/inventory references to the exact R7 contract/count only after the test inventory is finalized. |

## Scope and gates

- A fresh GPT-5.6 Terra writer may modify **only** `ops/juyiting-voice-production/**` in a clean dedicated R7 worktree based on the exact R6 candidate.
- No runtime product-script/module rewrite may be used as a test seam. Test setup may copy the candidate packet but must execute the unchanged candidate entrypoint.
- No host apply, production deployment, key read/install, flag activation, service restart/reload, Nginx action, or full verifier is authorized.
- After a clean exact R7 commit, stop for a fresh read-only independent review. A full inventory verifier is permitted only after review `P0/P1/P2=0/0/0`.
