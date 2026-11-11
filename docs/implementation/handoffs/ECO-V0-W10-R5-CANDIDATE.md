# W10 integrated candidate — 2026-09-06

Clean `.worktrees/eco-v0-agent-integrated` commit `4bd0c257abe9a767f8398e5d4474395161cb9364`, tree `7600bc8a53fd04b529895fbcf81eb42bde602d34`, parent R01 runner `af40adbe7d1541b51755107b2c4ba55cfa151bfe`. Coordinator verified clean Git identity and the five-path diff; original owner released.

Changes: strict supported frontmatter subset with mandatory description and metadata.version, duplicate/conflicting/unsupported identity rejection; six exact W08 package fixtures; explicit chmod establishes the packaging test's 0644 precondition despite umask077; staged managed-host.mjs and exact source-byte packaging assertions. No runtime default-off changes, no data/log/runtime sync.

Writer syntax/whitespace and exact fixture byte checks are static only. Fixture SHA256 `1f4fb61418c0f5e0a1b6e13dcbf3dd402e2c5c607e2ec7f0ffa4aee87548662e`. Main read the full five-path delta: no additional blocking delta finding; parent R01 managed-host integration review remains required. Historical installer47PASS is not evidence for this changed tree.

After independent reviewer/verifier admission, execute once sequentially from `conf/codex-ws-agent`, with owned temporary HOME/TMPDIR and umask077 after fixture preflight:
1. `node --test test/skill-install-manager.test.mjs`
2. `node --test --test-name-pattern='installer|copy, npm, or validation failure' test/workspace-manager.test.mjs`
3. `node --test test/agent-client.test.mjs test/managed-host.test.mjs`

Actual exit/log/test counts, cleanup and clean final tree must be recorded; stop and attribute any failure before retry. No production installer or service operations authorized by this candidate packet.

Prepared-only control wrapper: `/var/tmp/cyf-eco-control-w10-r5/run-node.sh`, SHA256 `bddd1e8c9fa3dfd60fc14478d944acd928e65278fec302ccdba44b1305b44600`; syntax checked, never executed by main. It requires the canonical W10 verifier gate, exact clean candidate, own temporary HOME/TMPDIR, locked local dependency setup, sequential per-selector TAP/exit/cleanup checks and cache identity. Admitted verifier must independently preflight before one run.
