# JVC-OAI-OPS R7 review root-cause matrix

Date: 2026-09-04
Reviewed candidate: `bbd7324f1eea545878f1d8188b16fb3f41a73a7f` / tree `384c90708b2679fde00a3903853b6f556aeebe00`
Review result: REJECT `P0/P1/P2 = 1/1/0`; reviewer was read-only and ran no test, Gradle, credential, flag, host, deployment, reload, or restart action.

## R8 bounded closure

| Priority | Finding | Required exact closure |
| --- | --- | --- |
| P0 | The alleged sensitive-input × all-phase test pre-seeds snapshot phases, mutates the persisted snapshot, then calls `release_state.activate()` directly. It neither enters the unchanged candidate `activate-release.sh` entrypoint nor races actual live passwd/group/NSS/JDK/JAR/unit/env/Nginx/selector/directory/lock inputs at each phase. | Add a deterministic, production-allowed test synchronization contract to the unchanged candidate entrypoint/state path. Execute a real live mutation matrix covering every named sensitive input and each named durable phase. Each cell must prove fail-closed or the explicitly allowed exact recovery outcome, including journal/selector post-state. No runtime product script/module rewrite. |
| P1 | Full inventory `main()` loads controller manifest identity before `seal()` closes the evidence root. | Pre-close/preflight the evidence root on the exact main/inventory path before any controller or external manifest loader can read/use a manifest. Add order-sensitive FIFO/socket/symlink/hardlink tests invoking that real main path. |

## Scope and gates

- A fresh GPT-5.6 Terra writer may modify only `ops/juyiting-voice-production/**` in the existing clean R7 worktree after it is moved to a dedicated R8 branch.
- Preserve the R7 closures already accepted by the reviewer: exact rollback/failed replay, internal seal/verify ordering, and R7 semantic consistency.
- Stop after a clean R8 commit for a new independent read-only review. A full inventory verifier remains forbidden until `P0/P1/P2=0/0/0`.
- No production/host apply, deployment, service restart/reload, key install/read, feature-flag activation, or runtime product-script/module rewrite is authorized.
