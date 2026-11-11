# W04 R3 corrected candidate

Clean original-writer handoff `ea1eb579a5329f563bc97ba143c16c855cea2875`, tree `fb32f4592b17941cfd7a746352e88356979dc8d4`, parent `16fe4bd40067ef0894511736481d1eccbea0e364`, `.worktrees/eco-v0-bounty`. Eight changed paths. Main checks exact SHA/tree/clean state. The attributed provider-capacity dispatch recovered; no repeated capacity failure was observed for this source task.

R2 P1: transaction-bound JdbcTemplate connection callback plus one-connection-pool regression. P2: held/refunded escrow_version explicit nonnull in DDL and matching initializer, both adversarial NULL cases and old-catalog rejection. Service fixture replaces substituted ledger/task/event with production collaborators and real two-thread create/guard interleaving, rollback/conservation/replay/aftercommit assertions. Runtime truth remains unproven until tests execute.

Focused selectors: `FundedBountyLegacyGuardRaceRealTransactionTest`, `FundedBountyServiceRealTransactionTest`, `AgentTaskFundingSchemaInitializerMySqlTest`; retain earlier Spring ledger and digest/legacy regression selectors in combined verification. H2 fixture `agent/jia-agent-service/src/test/resources/w04/funded-integration-h2.sql` SHA256 `9a4815f9acfa5df230e9c73251136f446434fbbfae6adcbc543a801f6f6dc644`; funding DDL `728623fd2758eff20b60482b731616146b33a83d821c5fdb4944e8ff7c4233fe`.

No DTO/event changes, no W05 integration or R01 application/economy posting edits. Existing weaker schemas reject rather than silent repair. Independent bounded R3 delta review, then admitted runtime verification; not accepted/deployed.

## Independent source verdict

Original reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **bounded R3 SOURCE ACCEPT P0/P1/P2=0/0/0** on exact SHA/tree above; two R2 blockers closed and actual collaborator/concurrent fixture sources recognized. No runtime executed, so full W04 promotion still waits focused runtime/MySQL evidence. Downstream source can consume the frozen corrected interface; no publication/charging authorized.
