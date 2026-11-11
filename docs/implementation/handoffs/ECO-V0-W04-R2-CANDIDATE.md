# W04 R2 corrected source candidate

Original critical writer handed off clean `16fe4bd40067ef0894511736481d1eccbea0e364`, tree `956f1bc510d8103e662f04b12011c7937027ebe8`, parent `fb0a499361df3e7415cb8d042a9cc174cada2114`, in `.worktrees/eco-v0-bounty`. Main checked SHA/tree and clean status. Fourteen changed paths, no API DTO deviation; corrected R01 foundation remains an ancestor. Source-only, not independently accepted/tested/deployed.

R1 seven-finding mapping: compatible Spring transaction proxy; compound MySQL CHECK normalization; preview-independent persisted legacy guard; recheck under task root; CHECK enforcement/exact index/trigger validation; explicit receipt NOT NULL constraints; reject unpaired UTF16 surrogates before digest. See R1 root-cause packet for authoritative original findings.

New regression sources: `FundedBountyLedgerServiceSpringTransactionTest`, `FundedBountyServiceRealTransactionTest`, `FundedBountyLegacyGuardRaceRealTransactionTest`, `AgentTaskFundingSchemaInitializerMySqlTest`; updated `FundedBountyRequestDigestTest`, `AgentServiceFundedBountyGuardTest`. H2 transaction tests and MySQL selector remain unexecuted. Review actual fixture realism rather than treating test names as proof. MySQL test uses W02 variable names but execution must allocate an exclusively owned W04 namespace, never reuse W02 fixtures.

W05 immutable `acc555a2` awaits corrected-parent integration after W04 acceptance. Independent reviewer to assess delta only plus touched call paths, no repairs or runtime/heavy resources.
