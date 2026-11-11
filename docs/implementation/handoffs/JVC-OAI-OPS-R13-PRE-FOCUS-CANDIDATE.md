# JVC-OAI-OPS R13 pre-focus harness candidate

Date: 2026-09-05
Status: read-only conformance review required; no test selector or production action is authorized by this document.

## Authority

- Root-cause/remediation matrix: `docs/implementation/handoffs/JVC-OAI-OPS-R12-STAGED-SYNC-ROOT-CAUSE.md`
- Matrix SHA-256: `5bd3d5213172b5d3194b320d4c75119400c137039bc479f5b81469f795c2ac5c`
- Independent matrix review: `01a06f4d-97ca-74c0-9fd6-6365f7c35cc2`, ACCEPT `P0/P1/P2=0/0/0`
- Committed base: `a543e644c2fc738de34332c339d4c2c8d557dbea`
- Base tree: `a0f2d196b6a3cdac520a7b907b54f4269f25a718`

## Exact frozen tracked candidate

Only the matrix allowlist is modified:

| Path | SHA-256 |
| --- | --- |
| `ops/juyiting-voice-production/tests/self_test.py` | `89ef8ce8ef672f6579d84a29c93f009b4bee5e6fd346d38c20b0bee55e7e9597` |
| `ops/juyiting-voice-production/tests/inventory.tsv` | `78740eed8120166c3f92d6a0724d7f5cfdc425646ae00e06c0332768bd3561ed` |
| `ops/juyiting-voice-production/README.md` | `185f4254a4330a6e6ab0ce475eeb28b4fe32ea5da084742bcfaa37ccf76edf0c` |

`git diff --binary` SHA-256: `de12d250d4291262f511bac90a5d702587148fb255bc3429bc47ca239a2c5031`.

`git diff --check` passes. No `__pycache__` directory is present. No file outside the exact allowlist is modified.

## Candidate intent

The candidate is intended to:

1. retain DEVNULL/`wait()` cleanup and the eight current-link assertions;
2. drive ready/continue files in exact checkpoint order instead of waiting directly for a later checkpoint;
3. bound every test-owned namespace invocation in an owned process group and clean only that group;
4. observe failed terminal state from the harness through nonzero exit and exact `99-failed.record`, without changing `lib/**` or production checkpoints;
5. retain the focused staged lifecycle case, raising inventory and both README counts from 129 to 130.

No focused selector was executed after this implementation. R13 stopped on an incompatible external Python 3.6 static-check invocation; R13b stopped because it correctly detected that the authorized implementation changed the earlier R12 byte identity. Neither stop is product or harness execution evidence.

## Review gate

A fresh read-only reviewer must verify exact matrix conformance, especially ordered checkpoint progression, bounded session/PGID ownership for every invocation, no unrelated process signaling, failed-record observation, unchanged current-link assertions, and exact path scope. Only an ACCEPT `P0/P1/P2=0/0/0` may authorize exactly one `r11.entrypoint.staged_previous_release_sync_lifecycle` focused run. Failed-terminal focus and full matrix remain forbidden.
