# W04 R2 second consecutive rejection — bounded remediation matrix

Independent original reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **REJECT0/1/1** on `16fe4bd40067ef0894511736481d1eccbea0e364` / tree `956f1bc510d8103e662f04b12011c7937027ebe8`. Six original findings source-closed. No runtime executed. Second consecutive W04 source rejection stops the loop at `blocked_root_cause` before targeted original-writer authorization; historical attempts retained.

| Severity | Attributed cause | Bounded correction/proof |
| --- | --- | --- |
| P1 | `PersistedFundedBountyLegacyGuard.java:57–70` opens a second connection for metadata while caller holds transaction connection/root lock. N transactions exhaust an N-connection pool; one-connection pool reproduces sequentially. | Reuse transaction-bound JdbcTemplate/connection callback via compatible Spring utility, release correctly; no separate borrowed connection. Add real bounded-one-connection-pool guard test with preview disabled and uninitialized schema, plus funded guard behavior. |
| P2 | funding DDL78–85 and initializer290 still allow `escrow_version=NULL` in held/refunded states through CHECK UNKNOWN. | Add explicit NOT NULL predicates for both state branches and matching catalog normalization; adversarial MySQL tests both held/refunded NULL version cases. |

## Runtime proof closure, without broad scope expansion

Existing test names do not prove full collaborator integration: service fixture substitutes JDBC ledger/task/event implementations and race inserts sequentially. Add bounded source tests using actual transactional posting collaborators and a true two-thread create/legacy-lock interleaving, reusing accepted mapper/TM infrastructure. Verify cancellation/insufficient/late-failure rollback and journal conservation + exactly-once aftercommit. Do not alter W05/W06 or rental application. No Gradle/DB in writer phase; clean candidate, independent bounded rereview then focused runtime selectors.

Only original writer owns `.worktrees/eco-v0-bounty`; W05 remains immutable. The main controller authorizes this concrete correction, not blind repetition of the rejected test/source loop.

## R3 dispatch provider capacity exception

Original writer notification: `Selected model is at capacity. Please try a different model.` Main verified worktree still clean at rejected R2 SHA/tree; no R3 source modification or runtime started. This is provider admission/capacity, not a new source/test result. Preserve original remediation matrix and route (P0 Sol; DeepSeek disabled); one explicitly attributed later dispatch to the same owner is permitted. A repeated capacity failure must stop rather than loop or silently downgrade transaction ownership.
