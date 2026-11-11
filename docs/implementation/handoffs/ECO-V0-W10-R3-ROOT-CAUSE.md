# W10 R3 bounded recovery matrix

Canonical ledger retains both prior failures and `blocked_root_cause`; this note does not clear it or authorize source changes by itself.

Base commit `fefc6aa8ef3dfd57e8794748078f2159bd014f9a`, tree `f1c8b6ac12ef9197fb85ad627aaff5744e3164f0`, worktree `/home/isp/wsps/cyf/.worktrees/eco-v0-agent`.

| Root cause | Existing evidence | Recovery |
| --- | --- | --- |
| Atomic helper treated missing owner evidence as ENOENT although JS uses SHA256(empty) | `/tmp/eco-v0-w10-r2-attempt1-attribution.txt` (ledger reference, not reread this turn) | Catch only `FileNotFoundError` and compare empty digest. Working diff already contains this handling in embedded `owner_digest`; inspect and retain it, do not assume whole diff is accepted. All other failures remain fail-closed. |
| Coordination metadata resolved relative to implementation worktree | `/tmp/eco-v0-w10-doc-path-attribution.txt` (ledger reference, not reread this turn) | Read guidance/ledger from canonical `/home/isp/wsps/cyf`. Do not copy coordination docs into source or modify root metadata from writer. |

## Source preservation and next owner scope

Worktree contains existing uncommitted changes in exactly five paths: `conf/codex-ws-agent/agent-client.mjs`, `skill-install-manager.mjs`, `test/skill-install-manager.test.mjs`, `test/workspace-manager.test.mjs`, and `shell/codex_ws_agent_install.sh`. They total approximately 1,103 additions/143 removals at inspection, including recovery/scope/atomic-exchange work beyond the original missing-owner fix. Canonical ledger has no owner; do not reset these changes or call base commit the current verified tree.

After explicit `authorize-remediation`, assign one critical writer to preserve/inspect these existing changes, finish only frozen V0 installer requirements and already-attributed recovery defects, static-check and commit exact clean candidate. Writer must report all five deltas and any unmet contract. No package installs, deployment, runtime service control, root docs writes or new Git repository. Independent verifier subsequently runs the focused installer/workspace tests and packaging checks under task-owned fixtures, stops on any new failure and records exact tree. Independent review is mandatory before installer activation. Deployment source remains ADR-004; deployed data/logs are never overwritten.

## R3 actual Node behavior failure on bbe0f8a

Exact candidate `bbe0f8a62f430945c441a8b7960ed33d85e727f7`, tree `bc53dbf638536926b857a73d85593990da81fd15`. Verifier-owned log `/tmp/cyf-w10-w10-node-dhfOfV/skill-install-manager.test.log`, main verified SHA256 `1185106bc247d671c207559d42e41c6af2b2729b1eca5a92301abbf39b7bd1f8`. TAP **47 total,46 pass,1 fail**, exit1, duration229978ms. Failure at incomplete stale-owner case (test625, failing initialize692): SKILL_INSTALL_IO_FAILED, undefined `.toString`, _acquireLock1518.

Main read-only attribution found `_assertReclaimableGeneration` line1420 checks `current.st_dev.toString()` on Node `lstatSync(...,{bigint:true})` result; Node Stats uses `dev`, not Python-style `st_dev`. Bounded correction must use the proper device identity property and preserve inode/owner-digest checks, add/retain incomplete-owner recovery regression. No broad lock redesign. Packaging second selector must not run after first-selector failure; no behavior retry yet. Exact verifier still needs to finish cleanup/reap and release immutable tree before writer resumes.

Correction handed over clean `3b337d22ee4ec543b7223d45131bcbf8ee38d41d`, tree `3302bf9f6bbba665f8cd7c96fd9fa50346a1ea24`, parentbbe0f8a. One property replacement only in skill-install-manager.mjs: current.st_dev→current.dev, all other fences unchanged. Main confirmed exact clean source. Attempted same-verifier assignment was rejected before save: global read-only slots are again full. No new Node run authorized yet; wait naturally for admission. No second behavioral failure, no deployment.
