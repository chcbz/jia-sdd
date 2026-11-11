# W07 R1 skill schema candidate

Source owner `01a0711c-9391-7e91-b508-5266ddccab93` handed over and released clean commit `138d636d98f021d8b9da84e9dac3d749ead73eea`, tree `cd862676a60b4b7ed46c598c15646366d7f915a3`, parent accepted W03. Main independently checked clean HEAD/tree and diff whitespace. Exactly 24 new skill-specific files; no shared posting/controller/starter/Web/ledger edits. **Not accepted or deployed.**

Seven additive tables: product, product_version, purchase_quote, order, order_receipt, installation, entitlement under `economy_skill_`. DDL SHA256 `4f1e827ab3370da2f06fd5036119e4e71354652d97a7e509b47acb5f3292d625`; mapper SHA256 `2c92da445545a97c8db706fb5a0973931381bf77e1e7950dd3c7320f70756267`. Gate `economy.skill.schema.enabled=false`; no DML/seeds/purchase/financial posting in W07.

## Frozen source-level extension points

- W08: `EconomySkillMarketplaceMapper` insertProduct/selectProductForUpdate/insertProductVersion/selectApprovedProductVersionForUpdate/publishProductVersion/selectPublishedProducts/selectPurchasableProductVersion.
- W09: immutable quote and actor-key order receipt, scoped buyer/explicit canonical target, order version CAS, reserve/capture/refund reference fields; insert/select/mark methods for order, installation and entitlement.
- Order FUNDS_HELD→INSTALLING→ACTIVE or preactivation REFUNDED; installation REQUESTED→INSTALLING→SUCCEEDED/FAILED; entitlement PENDING_INSTALLATION→ACTIVE/FAILED. Zero-priced orders carry no escrow or journal references.
- Entities under `economy/jia-economy-core/src/main/java/cn/jia/economy/entity/skill/` are the internal field contract. This is not a new HTTP field convention: external amounts/versions/times still use canonical decimal strings. W09 must add exact Agent ownership/version validation and transactional ledger composition.
- Immutable versions contain skill key/version, exact price, package SHA256/size, permission manifest/hash and deployment restriction. Seller fixed to SYSTEM:SKILL_STORE; deploy-runner ADMIN_ONLY.

## Verification dispatch

Main operational script `/var/tmp/cyf-eco-control-w07/run-w07-r1-nodb.sh`, selector `eco-w07-r1-no-db-schema-mapper-config`, fixture SHA256(empty), uses orchestrator wrapper options before task ID. Test sources: SkillStateMachineTest, EconomySkillSchemaContractTest, EconomySkillMarketplaceMapperH2Test, EconomySkillMarketplaceConfigurationTest. No MySQL authorization yet. Later narrowly scoped EconomySkillSchemaInitializerMySqlTest uses owned `ECO_V0_W07_MYSQL_*` fixture. Independent source review and runtime evidence remain required.
