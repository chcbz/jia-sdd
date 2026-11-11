# W05 R1 quote / explicit claim candidate

Original bounty writer delivered clean `acc555a2c8596e4044718d39aba3b86c0208acf0`, tree `f16c1b15232ce1315b43ef8613e53069881c25b6`, parent `fb0a499361df3e7415cb8d042a9cc174cada2114`. Main checked clean exact SHA/tree/parent. 29 changed paths. Source/static only; no tests/DB/runtime or independent review. **Non-promotable while W04 parent rejection remains.**

Reports exact quote/claim endpoints, synthetic immutable preview price book (not current provider prices), four-category overflow-safe integer arithmetic, cost/fee/payout/headroom/reasons/expiry/task version, scoped canonical Agent ownership/readiness, actor-key immutable replay and versioned assignment CAS with task members/work-items/events/durable invitation in one REQUIRED transaction. Runtime properties are claims to verify, not established evidence.

`FundedBountySkillEntitlementLookup` is the W09 extension: empty requirements allowed; nonempty requirements fail closed until exact scoped active+installed entitlement facts are implemented. No fake entitlements or W06 settlement.

Claim receipt `{taskId,agentId,quoteId,status,taskVersion,claimedAt}` now documented in `v0-api-contract.md`, distinct from task snapshot. Web must fetch task snapshot after success. Main checked source uses existing `AgentConstants.TASK_STATUS_ASSIGNED="assigned"` for both first receipt and replay; no paid effect from docs alone.

Prepared agent-service selectors: FundedBountyQuoteCalculatorTest, FundedBountyQuoteClaimServiceTest, FundedBountyQuoteRequestDigestTest, FundedBountySkillEntitlementLookupTest. Mapper: AgentTaskBountyQuoteSchemaContractTest. Validate real transaction fixture rather than assuming parallel mock tests establish SQL behavior.

Writer safely transferred back to original W04 bounty worktree for seven findings. W05 claim worktree remains immutable; after correction handoff merge exact W04 correction, resolve only known overlapping funding/controller/digest paths, then independent review and targeted combined verification.
