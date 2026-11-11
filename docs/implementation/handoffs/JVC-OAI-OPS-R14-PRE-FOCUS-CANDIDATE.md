# JVC-OAI-OPS R14 pre-focus candidate

Date: 2026-09-05. No selector has run. Independent read-only review required.

Worktree: `.worktrees/juyiting-voice-conversation-ops-r7`.
Base commit `a543e644c2fc738de34332c339d4c2c8d557dbea`, base tree `a0f2d196b6a3cdac520a7b907b54f4269f25a718`.
Candidate tree reported by writer: `d29fcb2bd2557c9f8a94f78768261c459ddec302` (uncommitted).
Exact tracked binary diff SHA-256: `27ceb0f302e770553ba1316296136b3dae26e2bb80279c1d14f53527fc73fc8d`.

## Exact modified paths

- `ops/juyiting-voice-production/tests/self_test.py`: `dd9ce2eee2db7450f72aaeb0e5fcf149040e55f2fe287c626d310c66cde01e7d`
- `ops/juyiting-voice-production/tests/inventory.tsv`: `78740eed8120166c3f92d6a0724d7f5cfdc425646ae00e06c0332768bd3561ed`
- `ops/juyiting-voice-production/README.md`: `4ab312525c2d392aa5a3e0339bd138bed9f7569b2a2f1494911deeabec6e8f5f`

## Review scope

Verify closure of R13 reviewer 01a06f6a's three P1 findings:
1. Focused staged lifecycle must prove the complete expected route and initial success, not accept early exit.
2. Every invocation retains exact child/session ownership through cleanup failures; never signal reused PGID after reaping. Fixture deletion requires complete owned-group cleanup proof, including E2E, restored/fresh/replay/recovery calls.
3. Inventory and both README counts must equal actual non-comment entries: 131. This corrects the earlier matrix's mistaken 129/130 arithmetic, not test coverage.

Retain all eight current-link assertions and failed-terminal harness-only digest-linked 99-failed.record validation. Production scripts/lib/checkpoints/transaction/snapshot semantics remain unmodified. Existing R11/R12 evidence remains historical; no new runtime PASS is claimed.

On ACCEPT 0/0/0, authorize exactly one staged focused selector, then separately evaluate failed-terminal focus. No full matrix, production configuration/key/flag, deploy/reload/restart is authorized.
