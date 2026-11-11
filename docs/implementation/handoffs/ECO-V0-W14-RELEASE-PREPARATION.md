# Economy V0 release preparation — 2026-09-05

Full scope remains wallet, funded bounty/quote/claim/settlement/refund, six skill products/purchase/Agent activation, and server hosting rent. This is preparation evidence, not a second execution ledger or release approval.

## Confirmed deployment boundary

- `docs/DEPLOYMENT.md` now requires `/opt/cyf/service/api`, runtime user `cyf-api`, and `/usr/local/sbin/cyf-api-kit`. The old `/home/isp/bin/cyf_api_kit_start.sh` only forwards lifecycle commands; it **does not build or deploy source**. Never report its restart as feature deployment.
- Legacy `ops/release/` still requires accepted host adaptation. `JVC-OAI-HOST-ADAPT` has an independent owner; economy emitted `conflict-alert` and will consume the accepted contract rather than duplicate edits or control another thread's services. Every economy Gradle invocation still goes through `cyf_orchestrator.py`.
- Main API/Web workspaces contain unrelated changes and lag their remote-tracking branches. Integrate clean candidate worktrees retaining current accepted features; never reset main workspaces, build dirty API, blindly pull-and-deploy main Web, or bundle unrelated changes.
- Frontend default deploy script hardcodes main Web, pulls and builds. Resolve clean integration/preservation before invoking; do not skip the production build or claim deployment from a source-only candidate.
- Agent installer source remains ADR-004 repository. Preserve deployment `data/` and `logs/`; no new repository.

## Minimum release evidence

1. Exact accepted API/Web/Agent commits and clean integration trees; relevant source review and tests tied to those trees.
2. Fresh combined tests for changed integration paths; reuse unchanged-tree evidence instead of broad repeated suites. Serialize Gradle and Vite heavy stages.
3. Versioned additive schema validation/installation and explicit preview feature configuration; keep live charging disabled until the entire rent flow is verified. Preview issuance remains forbidden under production profile: freeze an isolated preview profile or explicit controlled initial allocation before claiming wallet usability.
4. Immutable build artifact hashes, accepted host-adapt deployment path, configuration scope and narrowly owned runtime authorization.
5. Actual deployment and public HTTP/health checks plus authenticated wallet/bounty/purchase/installation/rent happy-path and rejection checks. A public index 200 alone does not prove economy functionality.
6. Record deployed hashes and user-facing acceptance steps only after success; publish concise blockers truthfully if a gate fails.

## W12 ownership observation

`18c4d59e32c408f828cf0ad0f0d3d500f7ce0215`/tree `2d1f091916a2630bd5bc8fd7f2b31fd865f43276` is clean. Prior writer ID is unavailable via `send_input`; a conflict alert was emitted, not a process action. W11 and W12 have disjoint changed paths since common base `9d205884aaaa07b34aebe5aa6e4191d7dde2aa7e`. Independently review committed inputs and integrate into a separate worktree; retain existing workspaces.

## 2026-09-06 tooling handoff update

Canonical ledger now records **JVC-OAI-HOST-ADAPT accepted** on root commit `9f98694e39498583167ff07133e8596a844cc1d2`, tree `00ae5a9ef66c38e45c6a9fd9ad86865aa67f53dc`: source review 0/0/0 and composed offline coverage accepted. Its `ops/release/build-api.sh` invokes the pinned orchestrator `gradle` wrapper, so the old missing host-adaptation dependency is resolved at source/tooling level. Consume that exact accepted tool lineage during economy integration; do not use the older checked-out pipeline blindly or duplicate the external owner's changes. Tooling acceptance is not economy/API release acceptance. Exact clean economy/API/Web/runner candidates, artifact hashes, environment configuration and authenticated smoke remain required. No economy deployment was performed by this handoff check.

## Preview-runtime boundary confirmed, 2026-09-06

Voice controller confirmed accepted host tooling currently supports only canonical `/opt/cyf/service/api`, runtime `cyf-api`, port10018 and `prod` startup; it is **not** a separate preview-instance deployer. W03 test issuance intentionally rejects `prod`/`production` and requires `dev`/`test`. Do not switch the existing main API to dev, bypass the issuance guard, or call a flags-off deployment a usable economy preview. A separately isolated preview-runtime/configuration/deployment contract remains required before full UAT unless an independently accepted controlled allocation path exists; none was executed here.

No economy process/service/config/DB/installation was changed. The voice controller retains canonical runtime custody; request its explicit final release/custody handoff before any shared-runtime action. Current source-only and scoped test acceptances are not deployment evidence.

## 2026-09-06 14:52 bounded preview preparation result

Turing3 completed formally admitted read-only W14 preparation and released its support slot. The following is a **proposal and gap inventory**, not an accepted deployment contract or execution authorization:

- Exact candidate API `1b3c7d0435d701c811716b8913bc824fb8934dec` / `cac8d686384b553f92a514e45bec95c71e6fe4ff` retains shared-development defaults. `starter/src/main/resources/application-dev.properties` specifies port10018, Redis DB1, and OAuth localhost10018 issuer/JWK/redirect; its MySQL and broker defaults do not prove exclusive preview tenancy. Do not run this profile unchanged. Never print configured credentials in handoffs.
- Actual issuance guard is `economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletService.java:isPreviewEnvironment` (lines99-100): requires dev/test and excludes prod/production. Endpoint implementation is `EconomyWalletController`, not a presumed `EconomyPreviewController` class.
- Accepted root `9f98694e` host adapter still pins canonical API directory, user and port. Agent installation likewise needs a distinct instance boundary rather than invoking the canonical installer against the existing service. Current tooling cannot safely deploy a second preview unchanged.
- Proposed minimum: separate API runtime identity, trusted artifact/config/log/runtime directories and loopback port; explicitly isolated database/user and schema baseline, OAuth client/user/issuer/JWK/redirect, Redis namespace or instance with reviewed isolation proof, both `spring.rabbitmq.*` and `agent.rabbit-broker.*` with dedicated account/vhost; separate Agent service/socket/managed and work roots. Port11018/user `cyf-api-preview` and standalone Redis16379 were preparation suggestions only, **not host allocations**. Reuse current Git repositories.
- Still missing: accepted bounded API/Agent preview adapter, assigned resource/config scope, baseline provisioning and authenticated fixtures, accepted final Web artifact, final API/MySQL/rent integration tests and immutable release artifacts. Do not treat suggested extra instances as already provisioned or mandatory without reviewing actual isolation needs.
- Host available disk was observed at about2.6GiB at14:20; this is a snapshot, not a fabricated test/build failure or an ECO-specific universal threshold. Canonical runtime custody remains voice controller; no service/config/DB/Agent changes were made by ECO.

The final API noDB selected verification has separately started under W09 (session91255, exclusive admitted heavy window); that is not an artifact build, runtime release or a database UAT. Web R8 source correction remains in progress. Latest queried remote Web develop at14:28 was d81b59e2724c45e7af47c60022296b2d20793295; recheck before actual integration/release and do not overwrite Juyi Hall follow-up work.
