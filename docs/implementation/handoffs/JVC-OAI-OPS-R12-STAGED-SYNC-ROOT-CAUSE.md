# JVC-OAI-OPS R12 staged synchronization root-cause matrix

Date: 2026-09-05
Status: frozen `blocked_root_cause`; no implementation, test rerun, full matrix, production action, key/flag change, deployment, reload, or restart is authorized.

## Bound evidence

| Attempt | Evidence | Result |
| --- | --- | --- |
| R11 full live matrix | `/tmp/jvc-oai-ops-r11-live.cEBTsX/live-matrix.log`, SHA-256 `7fb8bc10cd8a552b6e8f70c1091bb19a840f125b39604282b0f09ad4dd9ccc26`; receipt `/tmp/jvc-oai-ops-r11-live.cEBTsX/jvc-oai-ops-r11-live-matrix-post-state.json`, SHA-256 `59f4efda0f0158640c8336536a325af4eaca7d8147277e9fd948f42b145dd1ed` | All 22 `sealed_before_staged` inputs completed with 181 labelled PASS observations, including the frozen current-link assertions. First `staged × files:previous_release` cell failed before assertions. `ValueError: Invalid file object` was emitted by cleanup. |
| R12 focused staged cell | `/tmp/jvc-oai-ops-r12-focused.V5CUWJ/focused-sync-cell.log`, SHA-256 `1458afae5e79702e0ea83193284412f719368bba1af4b5bac8218c049a772aaa`; receipt `/tmp/jvc-oai-ops-r12-focused.V5CUWJ/jvc-oai-ops-r11-live-matrix-post-state.json`, SHA-256 `201aa520b3d684a59d8e0bdba35370047efe6e415b73c18ee4f8d8178b5b5a43` | After replacing PIPE/`communicate()` cleanup with DEVNULL/`wait()`, the same focused cell timed out waiting for `staged.ready`; parent killed the top-level child with return code `-9`. This exposed the primary failure. |

Candidate base remains `a543e644c2fc738de34332c339d4c2c8d557dbea` / tree `a0f2d196b6a3cdac520a7b907b54f4269f25a718`. The exact frozen tracked uncommitted state is byte-bound as follows:

- tracked binary diff (`git diff --binary`): SHA-256 `ed987c0c5c5fde958cb11a49164c5531b7b5cb926519c5c2e3ac964c3281d4c1`;
- `ops/juyiting-voice-production/tests/self_test.py`: SHA-256 `62e585cd6b3c343da37cddcae3d012b420441868f5b1e469a97f9904b44d00ea`;
- `ops/juyiting-voice-production/tests/inventory.tsv`: SHA-256 `78740eed8120166c3f92d6a0724d7f5cfdc425646ae00e06c0332768bd3561ed`.

Untracked `ops/juyiting-voice-production/lib/__pycache__/` and `ops/juyiting-voice-production/tests/__pycache__/` are excluded generated residue, are not part of the candidate or evidence identity, and must be removed before any commit.

## Confirmed root cause

The test parent requests a later phase such as `staged` and waits only for `staged.ready`. Setting `JVC_TEST_SYNC_DIR`, however, enables every activation checkpoint. The child reaches `sealed_before_staged` first and waits for `sealed_before_staged.continue`. The parent never creates that continuation because it is polling only for `staged.ready`. This is a deterministic controller protocol deadlock, not a production activation failure and not primarily namespace setup latency.

Relevant source locations on the frozen worktree:

- Parent waits directly for the requested phase: `ops/juyiting-voice-production/tests/self_test.py:1267-1269`.
- Sync environment is enabled for the whole child invocation: `tests/self_test.py:1097-1106`.
- All checkpoints are active and wait for matching continuation files: `lib/release_state.py:571-616`.
- `sealed_before_staged` is reached before `staged`: `lib/release_state.py:645-680`.
- Parent and child both use approximately `300 × 0.1s` deadlines: `tests/self_test.py:1120-1129`, `lib/release_state.py:596-616`.

R11's `Invalid file object` was secondary masking: timeout cleanup called `communicate()` on pipe objects whose lifecycle had already been consumed/closed. R12's DEVNULL/`wait()` change correctly exposed the underlying checkpoint deadlock and should be retained as a partial harness lifecycle correction.

## Root-cause matrix

| Hypothesis | Verdict | Evidence / falsifier |
| --- | --- | --- |
| Parent waits for a later checkpoint while child blocks at the first checkpoint | **Confirmed primary** | Unconditional checkpoint sequence plus exact failure at the first transition from `sealed_before_staged` to `staged`. A future single-cell diagnostic should observe `sealed_before_staged.ready` first and stop. |
| Equal parent/child 30-second deadlines obscure ownership of timeout | **Confirmed contributor** | R12 records parent SIGKILL `-9`; child was independently approaching its own deadline. Use asymmetric bounded deadlines in the repaired controller. |
| PIPE backpressure is primary | **Ruled out** | R12 used DEVNULL and reproduced the timeout. |
| Namespace/mount setup exceeds 30 seconds | **Low** | R11 reached the first checkpoint successfully 22 times; fixture copy occurs before Popen and packet size is small. |
| Host/chroot sync path visibility is broken | **Very low** | Regular files, not FIFOs, are used; host `root/sync` and chroot `/sync` refer to the same directory. |
| Earlier successful cells contaminate later cells | **Low** | Each cell has a unique root/private mount namespace and waits synchronously for exit. |
| Timeout cleanup can leave descendants | **Medium latent risk** | Current cleanup owns only the top-level `unshare` PID; no dedicated session/process group proves descendants are reaped before root deletion. |

## Additional latent blocker: unreachable `failed.ready`

The matrix maps `failed` to fault `failed-after-rename` (`tests/self_test.py:1065-1066`). In `lib/release_state.py:188-196` and `:702-706`, the fault raises during `atomic_record` before control reaches `test_sync_checkpoint("failed")`. Therefore a controller that correctly advances earlier checkpoints would still never observe `failed.ready`.

This is a test-observation-contract defect. It does **not** justify changing production activation semantics. Before any full matrix, independent review must choose a deterministic test-only observation strategy that preserves failed-phase coverage and remains inert when test controls are absent.

## Invariants that remediation must preserve

1. Normal checkpoint order: `sealed_before_staged → staged → activating → activated → finalizing → finalized`.
2. Rollback order: `sealed_before_staged → staged → activating → activated → rolled_back`.
3. Durable records remain monotonic and digest-linked.
4. Live snapshot verification precedes the first durable staged record.
5. Selector publication remains between activating and activated records.
6. The eight current-link assertions and inode/device-bound snapshot identity remain unchanged.
7. No timeout increase may be accepted as the sole fix.
8. No failed-phase coverage may be removed merely to make the matrix pass.

## Reviewed remediation envelope

The next writer, only after independent matrix acceptance and `authorize-remediation`, has this exact write allowlist:

- `ops/juyiting-voice-production/tests/self_test.py`;
- optionally `ops/juyiting-voice-production/tests/inventory.tsv`;
- optionally count-only corrections in `ops/juyiting-voice-production/README.md`.

Changes to `activate-release.sh`, `lib/**`, systemd/Nginx files, production checkpoint placement, `atomic_record`, `write_phase`, journal ordering, snapshot validation, and every other path are forbidden. Within the allowlist, the writer may:

1. retain DEVNULL/`wait()` lifecycle handling;
2. launch every test-owned `unshare` invocation—including initial, restored-current-link, fresh-transaction, replay, and recovery runs—in its own exactly recorded session/process group;
3. implement an explicit ordered checkpoint controller that advances every exact earlier checkpoint, pauses only at the requested mutation phase, and then advances valid later checkpoints until bounded exit;
4. reject skipped, duplicate, or out-of-order ready files;
5. apply bounded execution and asymmetric per-stage deadlines to every test-owned namespace invocation, retaining compact non-secret diagnostics;
6. on timeout or failure, use bounded termination escalation only against the exact session/PGID created by that cell, reap it, and prove the owned process group is empty before deleting the fixture root; no unrelated PID/PGID may be inspected or signaled;
7. resolve `failed` terminal observation entirely in the harness—for example by requiring child nonzero exit plus exact durable `99-failed.record` validation—without adding, moving, or modifying production checkpoints or production modules;
8. either remove the focused case and retain inventory/README count 129, or retain it and update both README count occurrences (currently lines 33 and 82) to 130; remove generated `__pycache__` before commit.

The first executable gate is exactly one focused `staged × files:previous_release` run proving the ready sequence and full cleanup of every process group it owns. A separate focused failed-terminal reachability gate and independent review are required before a new full-matrix window.

## Forbidden actions

- No third blind full-matrix run.
- No production execution, selector mutation, lock/journal/snapshot cleanup, deployment, reload, or restart.
- No API key or voice feature-flag access/change.
- No weakening inode/device/ACL or byte-exact snapshot comparisons.
- No process inspection or signaling outside the exact future task-owned process group.
- No writer claim or test execution before independent review of this matrix and explicit `authorize-remediation`.

## Independent analysis source

Read-only architect `01a06f42-c2f5-7001-8297-2c8909698d04` confirmed the deterministic checkpoint protocol mismatch, secondary cleanup exception, process-group cleanup risk, unreachable failed checkpoint, and no-production-change decision.
