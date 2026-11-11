# WEB R4 source candidate

Terra delivered clean `06875878bd21760ae172bf578afb1ee3889aa923`, tree `b6f892934d96d6c8683fda38471418c3284512fa`, parent `e48246732d5bd0a72025609627cc542a353b882e`, in `.worktrees/eco-v0-web-combined`. R4 updates Hall task actions, BountyPanel and JuyiHall plus focused tests/fixture. Static syntax/whitespace only, **no runtime tests/build/review acceptance/deployment**.

Claims actual quote preview before explicit confirm/cancel, exact Agent/task/version/expiry fences, unknown claim retry exact key, immutable receipt validation then canonical task GET, confirmed-but-refresh-pending state, and no regression of newer snapshots. Four token categories rendered from W05 real DTO; quote POST uses `{agentId}` per W05 source. Claim receipt exactly `{taskId,agentId,quoteId,status:"assigned",taskVersion,claimedAt}`, canonical strings, committed version=submitted+1. Earlier capability/POST-owned-roster gates retained.

Independent reviewer must review entire accumulated corrected combined R2-R4 delta, not only final commit, since no corrected combined source acceptance exists. Original W11/W12 review/rootcause and WEB-R2/R3/R4 packets remain relevant. Do not rereview unchanged accepted unrelated Web baseline.

Focused tests: `funded-bounty-confirmation.test.js`, `economy-wallet-bounty.test.js`, `juyiting-hall-task-actions.test.js`, `juyiting-collaboration-flow.test.js`, plus existing skill-market/silver-amount selectors. New shared `funded-bounty-fixtures.js`. Production build after relevant tests, never with heavy Gradle. R02 rental UI starts in separate worktree at this clean source interface; its promotion waits full R01 and combined Web acceptance.
