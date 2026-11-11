# JY-SESSION-AGENT dependency remediation authorization

Native focused test preload failed twice, with zero test cases executed:
1. Dedicated source worktree lacked node_modules; static skill-install-manager import could not resolve yauzl.
2. Writer's symlink selected deployment top-level node_modules, which contains ws but lacks yauzl. This was an incorrect dependency target, not a product assertion failure.

Main independently confirms both yauzl/package.json and ws/package.json exist in the exact active release `/home/isp/apps/codex-ws-agent/releases/20260909102948-3657004/node_modules`.

Authorized remediation: original Writer changes only its own untracked node_modules symlink to that exact immutable release dependency directory (read-only consumption), verifies required imports before retry, then runs only config-runtime.test.mjs. No npm install, production mutation, history cleanup, process operation, or foreign evidence access. On success commit exact candidate for independent Sol review. This is a new matrix-bound remediation, not an unchanged blind retry.
