# W10 R3 installer candidate

Writer `01a07175-94bd-7652-9b38-c7ae2e8de4f4` preserved and completed the five-file dirty draft, producing clean `bbe0f8a62f430945c441a8b7960ed33d85e727f7`, tree `bc53dbf638536926b857a73d85593990da81fd15`, parent `fefc6aa8ef3dfd57e8794748078f2159bd014f9a`. Main checked exact SHA/tree/parent and clean status. No behavior test, package install, deployment or runtime sync yet; not accepted.

Five-file source scope unchanged: agent-client.mjs, skill-install-manager.mjs, installer/workspace tests, shell/codex_ws_agent_install.sh. Reports origin/profile-scoped persistent state, atomic no-replace activation and generation-bound stale-lock exchange, missing-owner-only empty digest handling, portable archive path rejection, contradictory terminal-result quarantine/reconciliation, bounded result replay/backpressure; release staging before cutover and persistent data/log/config protection. Independent review/tests must establish these properties.

Static checks: four node --check, bash -n and diff/show whitespace passed. Writer static key36a7279d… and provisional test keys are not actual test results. Fixture reference package-lock SHA256 `3197e9c19030098c274ad802c95b0b37a2427bd7c6aa52a4a6d82c2ec328c015`.

Writer reported metadata-only helper failed on Python3.6 unsupported text=; attributed locally, one bounded universal_newlines correction succeeded. It did not execute behavior tests or justify any blind test retry. Host metadata helpers must stay Python3.6 compatible.

Verification selectors from worktree/conf/codex-ws-agent:
- `node --test test/skill-install-manager.test.mjs`
- `node --test --test-name-pattern='installer' test/workspace-manager.test.mjs`

Verifier must confirm fixtures use owned temporary homes/stubs before executing packaging tests; no actual production installer/runtime directory operations. Non-Linux unsupported atomic primitives intentionally fail closed in V0. Production signature/PoP/mTLS/KMS/isolation extras remain deferred. ADR004 source only; deployed Agent data/logs were never touched.
