# JVC-OAI-OPS R15 cleanup root-cause matrix

2026-09-05. Two consecutive independent implementation review failures; no new selector execution. No production/key/flag/deployment action.

## Frozen input

Worktree `.worktrees/juyiting-voice-conversation-ops-r7`, base commit `a543e644c2fc738de34332c339d4c2c8d557dbea` / tree `a0f2d196b6a3cdac520a7b907b54f4269f25a718`.
R14 candidate byte identity: see `JVC-OAI-OPS-R14-PRE-FOCUS-CANDIDATE.md` SHA256 `e12426ab94629631b566418b1de72317aa03f957f43cbc4c4fa2cc949dd2b659`; diff SHA256 `27ceb0f302e770553ba1316296136b3dae26e2bb80279c1d14f53527fc73fc8d`.

## Independent failures

| Review | Finding | Root cause | Required closure |
| --- | --- | --- | --- |
| R13 reviewer `01a06f6a-24b6-7e32-b118-2b729d25b43a`, 0/3/0 | All-invocation ownership lost on cleanup exception; numeric group reuse; early success/count defects | Helper lifetime did not cover fixture lifetime | Retain exact invocation owners until cleanup proof, not just helper exit |
| R14 reviewer `01a07051-2546-7072-b833-dc4961d537ba`, 0/2/0 | `_run_namespace` owner is local at lines 1377–1383, but outer finally deletes fixture at 1647–1650 even if cleanup fails; `_session_members` reads all host `/proc/*/stat` at 1188–1196 | Missing fixture-wide owner registry; global census used to compensate for missing containment | Fixture-scoped registry for every child; no deletion unless every owner proved drained; no inspection/signaling outside exactly owned children |

R14 strict full-route/zero-exit focus, all eight current-link assertions, digest-linked failed-record observation, and exact 131-case README count were independently verified. Preserve them.

## Frozen remediation scope

Only `ops/juyiting-voice-production/tests/self_test.py`, optional `tests/inventory.tsv`, and README count-only changes. No production script, `lib/**`, checkpoint, snapshot, journal, systemd, Nginx or credential change.

1. Attach every namespace invocation (including launch failures, initial, helper, E2E, restore, fresh, replay and recovery) to a fixture-wide lifecycle owner. Register ownership before operations that can fail. Never discard an unresolved owner on an exception.
2. Fixture cleanup must aggregate all owners' successful containment/drain proofs. On inability to prove cleanup, preserve fixture and diagnostic receipt; do not call `rmtree` or claim cleanup PASS.
3. Eliminate host-wide `/proc` enumeration. Read only exact owned process identities; no unrelated PID/PGID inspection/signaling and no post-reap numeric-PGID signaling.
4. Prefer a simpler containment design over ad hoc host census. A dedicated PID namespace is an available harness-only option (`unshare --pid`, `--fork`, `--kill-child` are locally supported); the implementation must establish and explain its containment/exit proof and failure semantics, not assume top-level exit alone means cleanup.
5. No selector is authorized during implementation. Python 3.6-compatible parse/diff/count checks only. Commit a scoped clean diagnostic candidate after checks so future byte binding is an actual Git tree, explicitly not accepted runtime evidence.
6. Fresh independent review of ownership failure paths and containment is required before one staged focus. Any execution failure must be attributed before retry. Full matrix/failed focus remain separately gated.

No weakening of the previous snapshot, current-link, exact-checkpoint or evidence contracts is permitted. No changes to user work or other task processes/evidence. Main controller remains coordination-only.
