# JVC-OAI-OPS R18 narrow post-reap ownership correction

2026-09-05. R17 independent reviewer `01a070d6-a977-7203-991a-608f28575bb4`: REJECT0/1/0. Startup cancellation/EOF/pre-start-drain/normal exact-reap paths otherwise close R16. No selector ran.

Base `.worktrees/juyiting-voice-conversation-ops-r7` clean commit `ecb1bdd3dc2c469c1215ddee67174da9fb253c7d`, tree `3f5084beea3371d38751fcba2bf54e9e70da0134`.

P1: `self_test.py:1372` reaps namespace init; abnormal status at1374 passes stale child PID to `controller_failure()` which calls `kill_and_reap_exact()` at1331-1334 and signals numeric PID at1318. Post-reap PID is no longer owned and can be reused.

Authorize only a localized harness correction that revokes signalling authority on exact reap, preserves diagnostics, and cannot pass a reaped PID to any signalling helper. Inspect every caller and error path of this small ownership primitive; no redesign of the now-reviewed startup protocol. Keep one-file scope `ops/juyiting-voice-production/tests/self_test.py`, unchanged inventory131/README/route6+rc0/current-link8/failed digest and production code. Static Python3.6 outer+embedded AST and diff checks only; direct patches, no nested executable replacement helper or temp deletion. Clean diagnostic commit, then fresh closure-only independent review before ONE staged focus. No namespace/signal/test/Gradle/DB/key/flag/build/deploy/service execution.
