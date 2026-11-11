# W04 R1 independent review rejection

Reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **REJECT P0/P1/P2=0/5/2**, exact W04 integrated `fb0a499361df3e7415cb8d042a9cc174cada2114`/tree `d49a4782724406935a161a6f0c766387e1259ca4`. Byte-exact merge verified34 W04 +10 R01 paths, overlap0; accepted parents not rereviewed. No runtime/test/artifact/source actions.

| Severity | Root cause / location | Bounded remediation / regression |
| --- | --- | --- |
| P1 | Final FundedBountyLedgerServiceImpl.java38,48,74 requires @Transactional interception but default Boot class proxy cannot subclass it | Remove final/use existing compatible proxy pattern; actual enabled Spring transaction-context regression, not direct constructor/no-op transaction mock. |
| P1 | AgentTaskFundingSchemaInitializer.java92-107,266-279 strips only outer CHECK parentheses, unlike MySQL compound-expression formatting | Canonicalize actual MySQL expression representation consistently with accepted initializer; pristine and repeated isolated MySQL init test. |
| P1 | AgentServiceImpl.java2002-2014 guards permit legacy operations when preview-gated funding service absent | Persisted funded-task guard must remain effective with preview disabled, without forcing schema access in never-initialized legacy deployments; test restart/off flag with FUNDS_HELD assign/auto/cancel. |
| P1 | AgentServiceImpl.java826,844-858 checks funding before task root lock; FundedBountyServiceImpl.java274-276 publication race | Recheck funding under current task-root lock in legacy mutation callbacks (same lock order). Test assignment sees absent task/funding, concurrent funded-create commit, then root acquisition must deny legacy bypass. |
| P1 | Funding initializer74-107 ignores CHECK ENFORCED, index prefix/type/visibility and triggers | Exact owned catalog includes enforcement and unexpected hooks. Reject NOT ENFORCED/same-name incompatible index/unexpected business trigger, no silent repair. |
| P2 | agent-task-funding-v0.sql24-30,74-87 state checks permit UNKNOWN on nullable receipt versions/times/key/hash | Explicit IS NOT NULL in state branches; reject malformed COMPLETED/REFUNDED receipts and cancellation metadata. |
| P2 | FundedBountyRequestDigest.java72-79 UTF8 replaces invalid surrogate title/description/ability, producing same digest for different bodies | Reject malformed surrogates in all hashed input or encode exact validated canonical input without replacement. Test x\\uD800 vs x\\uD801 same key reject; stable stored replay cannot reconstruct changed request data. |

## Essential evidence still missing

Current prepared mocks/no-op transaction tests are **not** proof of transactional reserve/refund. Add real Spring/H2 transaction fixture for funded create/cancel and isolated MySQL initializer/concurrency scenarios: insufficient-balance and late-failure rollback across task plan/items/root/funding/ledger/events; same-key concurrency, changed-body conflicts, conservation and exactly-once aftercommit wakeups; both legacy guard races. Shared refund extension has no separate identified conservation defect, but still needs focused shared-posting/rent regressions when integrated. Do not expand to W05/W06 or full production security.

## Ownership handoff

Original writer is actively implementing separate W05 in `eco-v0-bounty-claim`; do not overwrite that work or casually transfer the task. Main must obtain a safe source checkpoint/handoff before assigning bounded W04 corrections in the original bounty worktree. W05 remains a working-dependency branch, non-promotable until W04 defects/evidence close. No rejected source test retry or deployment.
