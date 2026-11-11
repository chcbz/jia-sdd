# W09 integrated source candidate — 2026-09-06

Original owner delivered clean source checkpoint `91281a1ddc29fc97ae6fb9a48a5136713c024335`, tree `ebe5192cdb4a04fe8be0f050e3f446b60a711822` (56 paths). Then merged W06 to `cf54400c` and corrected W08 to final `9e7b16b617ed16b3485a29e2648dfedd77821fee`, tree `ec250ff1798abd37dc3f24b049775b71cbeb2fe8`. Worktree: `.worktrees/eco-v0-skill-purchase`. Owner reports conflict-free integration and exact W06 29/W08 8 path blobs. Source owner released; no compilation, tests, DB, runtime or deployment.

Implemented candidate scope: explicit scoped target/version CAS, purchase/order+outbox transaction, per-Agent credential and exact registered session, package delivery, installation result handling, activation/capture or preactivation failure/refund, same-wire recovery, six additive application tables and catalog validation. UNKNOWN/no-result holds funds; it is not an automatic timeout refund. Upgrades/repeated orders for the same skill key remain outside the existing W07 unique-history contract.

Focused selectors (unexecuted):
- `:agent:jia-agent-service:test --tests 'cn.jia.agent.skill.*' --tests cn.jia.agent.config.SkillPackageSecurityConfigurationTest --tests cn.jia.agent.service.impl.AgentSkillInstallCommandCodecTest`
- `:chat:jia-chat-service:test --tests cn.jia.chat.handler.AgentWebSocketRawCommandDispatchTest.skillDispatchRequiresExactDedicatedKeyAndCurrentRegistrationNotOwnerWidePresence`
- `:economy:jia-economy-service:test --tests cn.jia.economy.config.EconomySkillApplicationSchemaContractTest`
- Separate owned MySQL fixture: `cn.jia.economy.config.skillapplication.EconomySkillApplicationSchemaMySqlTest`.

Independent full source and actual API/Agent compatibility review precede verification. All Gradle through orchestrator. Source merge does not accept W05/W06/W08/R01 dependencies; feature/config/Rabbit/outbox/installer gates stay off until release acceptance.

## Accepted-test-source integration checkpoint

Clean `.worktrees/eco-v0-skill-integrated` now `ac72b17b0207177eb0118e72703d1b810f790515` / tree `c7911622f2be1a9cd3b1f1cf7570be6b487a9391`, parents `27782150c86095d8f362fcbbf0a7529338bbecdd` + `01037b00b2b35896915948e5f8d8346f8f525102`. Intermediate27782150/tree53b9442b parents9e7b16b6+d56e205c. Exactly five test-only paths added from W07 and W05/W06, source mode/blob exact; remaining2932paths including all production byte-exact to9e7b16b6. No conflicts, tests or deployment. Main verified clean SHA/tree; original candidates unchanged.

Independent Sol reviewer `01a074ac-4236-71b1-850f-75cc9a05b01f` admitted to W09 full source review and its unaccepted R01 application/adapter parent, distinct verdicts required. Integration-only checks never substitute W09 production review; unchanged accepted source scopes are reused.
