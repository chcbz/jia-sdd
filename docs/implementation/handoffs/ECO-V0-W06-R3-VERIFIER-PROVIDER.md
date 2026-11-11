# W06 verifier provider attribution — 2026-09-06

New verification agent `01a074b8-963b-79c3-a33c-604ddad79d07` (gpt_test_runner / gpt-5.4-mini) errored with HTTP502, `unknown provider for model gpt-5.4-mini`, before any reported execution/checkpoint. No Gradle/TAP/XML result was delivered; this is provider routing failure, not a source or test assertion failure. Do not re-spawn the same unavailable route or claim tests ran.

Bounded fallback: close only the errored verification agent after confirming no reported tool execution; release its ledger lease. Use a supported Sol/Terra profile in **verification-only** mode on the same unchanged exact source and frozen wrapper. New verifier must check exact admission/worktree and cache before one invocation; every Gradle still uses orchestrator and global lock. Never restart an existing daemon or interrupt another verifier. Original W10 verifier remains separately owned and is not affected by this fallback.
