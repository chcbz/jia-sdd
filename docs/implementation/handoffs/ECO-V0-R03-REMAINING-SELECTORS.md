# Remaining runtime selectors after API combined noDB R2 — 2026-09-06

Static preparation only against API1b3c7d0435d701c811716b8913bc824fb8934dec/tree cac8d686384b553f92a514e45bec95c71e6fe4ff. The frozen W09 noDB wrapper is already running and must not be edited/restarted. Do not treat this inventory as test evidence or execution GO.

## Narrow noDB delta not selected by the running wrapper

- `:agent:jia-agent-service:test --tests cn.jia.agent.service.impl.AgentServiceImplTest.blankModeRetainsLocalBindingWithoutEnteringHostingRentAdmission`
- Same task: `cn.jia.agent.service.impl.AgentServiceImplTest.expiredHostingRejectsAssignmentInLockedPreparationBeforeMutationOrDispatch`
- Same task: `cn.jia.agent.service.impl.AgentWorkItemLeaseServiceImplTest.expiredHostingDeniesNewClaimBeforeCasButDoesNotKillRunningWork`
- `:chat:jia-chat-service:test --tests cn.jia.chat.service.HallActionDispatcherTest.expiredHostingRejectsNewInviteBeforeDurableWriterOrLegacyQueue`
- Same task: `cn.jia.chat.service.JuyitingAgentRelayServiceTest.expiredHostingIsRecheckedAtDeferredSendUsingCapturedScope`

Only these methods, not the entire previously covered classes, are proposed for the supplemental invocation after the current run naturally finishes.

## Still-required real MySQL selectors

- `:agent:jia-agent-service:test`: `cn.jia.agent.config.AgentTaskFundingSchemaInitializerMySqlTest`, `cn.jia.agent.config.AgentTaskBountyQuoteSchemaInitializerMySqlTest`, `cn.jia.agent.config.AgentTaskSettlementSchemaInitializerMySqlTest`.
- `:economy:jia-economy-service:test`: `cn.jia.economy.config.skillapplication.EconomySkillApplicationSchemaMySqlTest`.
- Same task: `cn.jia.economy.config.EconomyHostingRentSchemaInitializerMySqlTest` (nine @Test methods; class conditional on MySQL URL).

The original support report incorrectly said R01 had no remaining MySQL selector. Coordinator checked the tracked exact-tree file and running wrapper, rejected that negative claim, and the support agent explicitly corrected it. R03 records this preparation failure separately; no tests were attempted and no historical test result was changed.

## Fixture boundary to close before DB GO

W04/W05/W06 and rent initializer use `ECO_V0_W02_MYSQL_{URL,USER,PASSWORD,DATABASE_PREFIX,ISOLATED_FIXTURE}`; isolated fixture must be true. W09 uses the corresponding W09 keys. Expected port/datadir keys exist for pinning and should be set when preparing the exact fixture receipt. Do not print credentials in logs. URL is JDBC MySQL and fixture requires MySQL8.0.21*.

W09 corrected fixture registers before CREATE and only removes an owned name after confirmed DROP; timeout overrides are bounded. Older W02-derived fixtures used by bounty and rent still register after CREATE and do not apply W09's timeout override: an unknown CREATE response can leave an unregistered task-owned database. Therefore DB execution still needs either a reviewed bounded outer prefix/timeout/cleanup control or a minimal fixture correction. An isolated prefix alone is not proof of cleanup. Do not sweep other tasks' databases, use unbounded JDBC or repeat old passing schema suites. Freeze the actual fixture digest, selectors, ownership, timeout and cleanup receipts before one orchestrated supplemental Gradle run.

## Bounded outer fixture proposal after3a0f05 (2026-09-06)

Critical Turing read-only preparation confirms five classes above, including nine rent methods. No DB connection or source change. An outer harness can close the old fixture's unknown-CREATE leak without changing production initializers: register a unique validated short lowercase run prefix before execution, require an empty initial catalog for that prefix, record owned names, and reconcile/drop only exact run-prefix names after natural JVM termination; unknown DROP keeps ownership/evidence and is not cleanup PASS. Use a separately owned MySQL8.0.21 endpoint/datadir/account with pinned expected port/datadir; oldW02 wrapper hardcodes3306/canonicaldatadir and is not approved for reuse. Whether a suitable isolated instance currently exists is **not yet verified or allocated**.

Inject both W02/W09 env namespaces, bounded JDBC connect/socket timeouts and reconnect=false. Suggested values from support were10s connect/2400s socket (upper bound proposal, not execution GO); choose an explicit finite run budget before runtime. Do not place passwords/fullcredentialURLs in command output, hashes or receipts. If fixture-internal closure is selected instead, only EconomyMySqlTestFixture.java and three agent schema test classes need test-only changes, optionally a shared AgentSchemaMySqlTestFixture; no production initializer edit is needed. Accepted W09 fixture already registers before CREATE and preserves failed DROP ownership. Separate reviewed harness/fixture and isolated-resource admission remain required before Gradle MySQL selectors.

## Additional noDB coverage gap found during R3 start

R3 wrapper7a20dade omits `cn.jia.economy.config.skillapplication.EconomySkillApplicationMySqlTestFixtureLifecycleTest`. Verifier confirmed no accepted runtime evidence: R5 is source-only; oldR2 stopped in agent-service; W07 lifecycle evidence is a different fixture and cannot substitute. Keep this exact noDB class on the remaining list, to combine with a later admitted supplemental stage. Do not alter or restart running session3658 to add it, and do not claim R3 covers it.
