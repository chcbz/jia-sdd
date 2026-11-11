# W08 R1 seed/package source candidate

Terra delivered clean `086a9ddea30c31d0922b700ef134a4a7521b4f42`, tree `1426b81cccb050c16a2f5a73f21e2309000c82ba`, parent W07 `b4614bd57aa9707412d3855548b2f3e17a325f16`, in `.worktrees/eco-v0-skill-seeds`. Main verified clean SHA/tree/parent. Fourteen new paths only in economy service: five Java implementation/config files, six deterministic ZIP packages, three test files. No shared schema/ledger changes. **Not independently reviewed, runtime-tested, seeded, installed or deployed.**

All six products version `1.0.0`; prices and admin restriction per V0 contract. Default-off `economy.skill.seed` with explicit scope gate; claimed idempotent seeding/immutable-drift rejection awaits tests/review. Writer static ZIP/digest/size/identity checks are not a substitute for installer execution.

W09 can inject `PlatformSkillPackageCatalog` and call `requireProduct(productId)`, `requireProductVersion(productVersionId)`, `requirePackage(productVersionId)` for stable IDs and verified bytes/digest. Actual installed/ACTIVE purchase capability remains W09/W10, not fulfilled by these bundled packages alone.

Focused proposed selectors: `cn.jia.economy.config.EconomySkillSeedConfigurationTest`, `cn.jia.economy.config.skillseed.PlatformSkillPackageCatalogTest`, `cn.jia.economy.config.skillseed.EconomyPlatformSkillSeederTest`. Promotion waits W07 runtime evidence and independent W08 source review. No actual provider pricing or production security claims.
