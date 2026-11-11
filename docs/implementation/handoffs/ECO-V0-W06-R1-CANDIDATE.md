# W06 settlement + inherited W05 correction candidate — 2026-09-06

Clean `eco-v0-bounty-settlement` commit `50b04489b384b40fffb034cc06c2d2a42ea8fad6`, tree `1b0be0504ca5da3096ce6cb6d76112b2874de666`, parent `fbee6395611837f3f6a08f4b32d762fa65c96037`. Main verified clean identity, 29 scoped paths and shared source digest. Static only; no compilation/tests/DB/runtime/deployment.

Writer reports preview complete and GET settlement, accepted-quote cost ceiling, server fee/explicit claimed-Agent payout, atomic capture/task/funding CAS/immutable receipt/events/outer-commit notification. All four W05 full-review findings have authored corrections (constructor injection, runtime-binding consistency, exact catalog, historical quote replay after refund). Original W04 cancel full refund and W02 schema/rent templates preserved. These are candidate claims awaiting independent review; W05 and W06 verdicts must remain distinct.

Single shared production path: `economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyPostingServiceImpl.java`, SHA256 `d03bdcf08935d6362fa9cd5a01f9213cbbfadbbf0396af050cc7737fa678299e`. Existing API/enum signatures unchanged. CAPTURE_SKILL/REFUND_SKILL use ACTIVE SKILL_ORDER escrow, ORDER/<businessId>/ESCROW to SYSTEM/SKILL_STORE/SKILL_STORE or original USER/<principal.id>/AVAILABLE, exact reserveTx/escrowVersion, nonzero balanced lines and immutable actor-key replay. Only bounty capture permits PARTIALLY_CAPTURED continuation. W09 may consume this exact file now, full source integration after its own clean checkpoint; no duplicate shared edits.

Source selectors:
- `cn.jia.agent.service.funding.FundedBountySettlementRealTransactionTest` (includes sharedSkillCaptureAndRefundConserveReplayAndRollBackUsingRealPosting).
- `cn.jia.agent.service.funding.FundedBountyQuoteClaimRealTransactionTest`.
- `cn.jia.agent.service.funding.FundedBountyQuoteClaimServiceTest`.
- `cn.jia.agent.api.funding.AgentBountySettlementControllerTest`.
- `cn.jia.agent.config.AgentTaskSettlementSchemaInitializerMySqlTest`.
- `cn.jia.agent.config.AgentTaskBountyQuoteSchemaInitializerMySqlTest`.

SHA256 inputs:
- W06 H2 migration `64bf619fe431bb0225070b7ddbcd6f5df1a10853b9a35b36d8a1f4e0bc9b1125`.
- Funding DDL `f1c257578943cbf2cab62bc3e26b84f016d7cc70e67739b2b34fa8e6113b953f`.
- Settlement DDL `66a0d2e0c720d0438956b9a799afeb05fdcaaddb2c5b19011939d09bb55df29a`.
- W06 MySQL source `6008574f8dd24c1253628b51e0c215c9ca4f9c1328a0e93a8136725f722283d2`.

Existing W04/W05 HTTP DTOs unchanged. V0 endpoint is preview orchestration, not actual provider billing. Future verifier must use a NEW exact combined tree/selector/fixture script after source review; `/var/tmp/cyf-eco-control-w05/run-w05-r2-nodb.sh` remains a prepared-only script on rejected old fbee source, never run it as new candidate proof. Original candidate trees remain immutable.
