# W04 R1 candidate — funded create / pre-start refund

Writer `01a0711a-9b90-71c2-a800-afee3605f963` delivered clean W04 `98a12fa60d55afca16e3f848a8c9b422cdb6e9b1`/tree `89428ff91c6f904e92c04c9654aec3065e180036`, then merged corrected R01 `ae311a1deb74ad4aae3a78e45303766af4124c8f` without overlapping changed paths. Integration HEAD `fb0a499361df3e7415cb8d042a9cc174cada2114`, tree `d49a4782724406935a161a6f0c766387e1259ca4`; main checked clean HEAD/tree/parents. This candidate is **not accepted/tested/deployed**.

W04 34-path delta implements funded task create, stored funding view, strict authenticated principal and actor-scoped receipt replay, additive funding schema, full reserve, pre-start version-CAS cancel/full refund, and legacy assign/auto/group/cancel guards while preserving unfunded flow. Minimal shared `EconomyPostingServiceImpl` refund extension requires independent review. DTO contract remains `v0-api-contract.md`; no W05 quote/claim or W06 settlement completion claim.

Source-only prepared selectors: AgentTaskFundingSchemaContractTest (agent mapper); AgentFundedBountyControllerTest, FundedBountyRequestDigestTest, FundedBountyServiceReplayTest, AgentServiceFundedBountyGuardTest (agent service); FundedBountyLedgerTemplateTest (economy service). Compilation, full transaction/rollback/concurrency evidence and independent review remain pending. R01 domain delta source ACCEPT0/0/0 does not replace its pending runtime verification.

W05 can use frozen W04 DTOs in separate `eco-v0-bounty-claim` worktree at exact integrated candidate, but promotion waits accepted dependencies. Original W04 worktree stays immutable for review/tests; no test repeat on unrelated accepted foundation trees.
