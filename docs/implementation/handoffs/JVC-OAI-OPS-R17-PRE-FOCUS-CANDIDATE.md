# JVC-OAI-OPS R17 diagnostic candidate

2026-09-05. **Static candidate, not runtime acceptance.** See sole runtime ledger for current review owner/gate.

- Worktree `.worktrees/juyiting-voice-conversation-ops-r7`.
- Commit `ecb1bdd3dc2c469c1215ddee67174da9fb253c7d`; tree `3f5084beea3371d38751fcba2bf54e9e70da0134`; parent `0c07d43335601ce680ab16412639cad2b212e4db`.
- Binary diff SHA256 `e9ec2b2a758ba23a7bcd68adbb968f290f37d4d613dc4991d5b687d54cc1c5f6`; source SHA256 `7ed45abb0a98df9f350e24e59e59d39076edf9cb169bee01a3ca43dbb5715c8e`.
- Exactly one changed file `ops/juyiting-voice-production/tests/self_test.py` (258 insertions, 88 deletions); controller checked clean/commit/tree/parent/diff identity.

Writer reports post-Popen cancellation no longer requires ready proof, stdin EOF remains a cancellation fallback, and the supervisor observes cancellation throughout setup and running. Terminal cleanup still requires validated namespace drain plus exact supervisor reap. Outer/embedded Python3.6 AST and preserved route/current-link/digest/count checks passed without execution. Fresh independent review must establish the protocol claim; this handoff does not endorse it.

Prior tooling failures and matrix-bound direct-patch remediation are recorded in `JVC-OAI-OPS-R17-EDIT-TOOLING-ROOT-CAUSE.md`. No namespace, selector, signal, Gradle, host, key, flag or deployment action was executed by the writer.

Only a fresh 0/0/0 review may authorize ONE partial selector `r11.entrypoint.staged_previous_release_sync_lifecycle`, with new verifier-owned TMPDIR/logs and exact candidate identity. Such partial evidence cannot be presented as the full131-case inventory acceptance. Failed-terminal reachability/full matrix remain separate subsequent gates.
