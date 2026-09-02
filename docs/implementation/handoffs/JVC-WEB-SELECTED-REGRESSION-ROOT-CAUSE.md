# JVC-WEB selected regression harness root-cause matrix — 2026-09-02

## Scope and terminal state

- Task: `JVC-WEB`
- Candidate: commit `97c2f8bd439dc6f7876a4d26c91d485ea7750cda`, tree `162fc64e5d8a81a77d85bf40bd50703af38e88f7`
- Purpose: add narrow evidence for orientation, keyboard resize, focus trap and map interaction without rerunning the known-problematic complete component suite
- Gate: `blocked_root_cause` after two consecutive harness failures; neither attempt entered a selected test case
- Existing authoritative evidence remains valid: voice-only 23 passing, production build passing, independent review P0/P1/P2 = 0/0/0.

## Consecutive harness failures

| Attempt | Evidence | Root cause | Outcome |
| --- | --- | --- | --- |
| Selected verifier 1 | Eight intended tests matched, but Mocha `before all` timed out at the default 2,000 ms | The command passed `tests/setup.js` positionally and omitted the known working `--require ./tests/setup.js --timeout 10000` harness | Zero selected tests executed; tracked worktree stayed clean. |
| Selected verifier 2 | `pwd=/home/isp/wsps/cyf`; target worktree contains `node_modules/tsx` and `node_modules/mocha`; orchestration root does not; Node returned `ERR_MODULE_NOT_FOUND` for `tsx` | The verifier inspected the target with `git -C` but executed Node from the orchestration root instead of changing directory to the Web feature worktree | Zero selected tests executed; second consecutive harness failure requires a matrix-bound successor. |

## Authorized successor boundary

One fresh `gpt_test_runner` may execute exactly one selected-test command. It must first change directory to the feature worktree and must not run the complete component suite:

```bash
cd /home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-web && \
node --import tsx ./node_modules/mocha/bin/mocha.js \
  --no-config \
  --require ./tests/setup.js \
  --reporter spec \
  tests/juyiting-component-behavior.test.js \
  --grep "classifies panel layouts for desktop|keeps panel layout a pure experience-mode projection|wires the exact responsive panel class and immediate HallStage interaction lock|focuses and traps a modal panel then restores the prior focus|locks and unlocks map interaction immediately for panels and cleans up on unmount|classifies visual viewport keyboard resizing without fitting the map transform|coalesces resize races, keeps keyboard close classified, and deduplicates rotation|renders HallStage from the supplied experience mode and delegates orientation requests" \
  --timeout 10000 \
  --exit
```

Any failure is terminal for this successor and must be attributed without retry. No source edits, dependency installation, complete combined suite, dev server, deployment or production action is authorized.
