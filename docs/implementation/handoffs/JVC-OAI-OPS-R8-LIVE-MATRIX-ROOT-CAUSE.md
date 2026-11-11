# JVC-OAI-OPS R8 live-matrix root-cause matrix

Date: 2026-09-04
Failed non-promotable snapshot: `eab40999a6be7e46a836b4be555e56acc8d2e024` / tree `e5eb70689449753c2e1ea4229252210b9469fc24`
Status: two consecutive focused-test failures; no production, key, flag, deployment, restart, reload, review, merge, or full-inventory action.

## Failure matrix

| Attempt | Evidence | Root cause | Bounded successor action |
| --- | --- | --- | --- |
| 1 | `TMPDIR=/tmp/jvc-r8-test python3 -I ops/juyiting-voice-production/tests/self_test.py --case r8.entrypoint.live_sensitive_input_every_durable_phase` failed with `ValueError: embedded null byte`. | The matrix harness passed NUL-delimited encoded arguments through a subprocess argv element; NUL is not legal in argv. | Replace the transport with a non-NUL-safe representation/side channel decoded inside the isolated runner. Preserve exact candidate entrypoint arguments and do not rewrite product scripts/modules. |
| 2 | The same selector failed at `phase=sealed_before_staged input=symlinks:current_link`. | Real `current.jar` symlink mutation changed the working-directory ctime. Snapshot validation correctly failed closed before any durable phase record existed, but the test incorrectly required a journal record for this pre-durable cell. | Make expected post-state phase-aware: `sealed_before_staged` failure must permit/require no durable transaction record while still proving no selector transition and exact fail-closed state. Durable phases must retain strict journal/selector assertions. |

## Frozen R9 scope

- A fresh GPT-5.6 Terra owner may modify only `ops/juyiting-voice-production/**` on the exact failed snapshot.
- Only the two matrix-harness defects above may be repaired; preserve R8 production synchronization seams, real live mutations, P1 full-inventory pre-manifest evidence-root closure, R7 replay closures, and R7/R8 identity semantics.
- Run the single live-matrix selector once after the bounded repair. If it passes, run only the focused P1/R7 regression selectors needed to establish no regression; clean pycache and commit an exact candidate.
- Any nonzero result stops and is attributed before another action. Independent read-only review remains mandatory before a full inventory verifier.
- No production/host operation, runtime product-script/module rewrite, key read/install, feature-flag activation, deployment, restart, or reload is authorized.
