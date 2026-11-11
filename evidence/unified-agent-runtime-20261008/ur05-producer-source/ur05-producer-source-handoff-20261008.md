# UR05 local API producer source handoff — 2026-10-08

Receiver: main controller, for source integration and the next UR05 installer slice. No independent Reviewer. This is source complete, NOT UR05 acceptance or deployment completion; ledger remains controller-owned.

## Exact source
- Worktree: /home/isp/wsps/worktrees/ur05-local-backend-package-20261008
- Branch: codex/ur05-local-backend-package-20261008
- Base: 2690fbbf040017083c6783a3cc65ce2eb631e136 / tree 5ca30834e19b11ddb457f3231546175e83bf1e55
- Final commit: ba88d4ed7c635ad4c916d6a9eb2aec97933d6ae3
- Final tree: 36c1e64447f0b24cf9a43b90e6207c5162e4bc66
- Remote task branch readback: MATCH; worktree clean; cumulative diff-check PASS.
- Commits: 8f02e44d106c25c2a2e4e74347f16cfbee9d37ee (producer/init/private units), then ba88d4ed7c635ad4c916d6a9eb2aec97933d6ae3 (keep honest per-report skipped counts while requiring actual executed cases across each required task). No dropped test/skip mask.
- Only three NEW paths; original package-api.py remains byte-for-byte baseline (SHA 165887c1e50d6db286359e7c6de9a04098440634ff542267ba84edf5bc21d84a). No existing installer/API/client/rootdocs/ledger changed.

## Selfcheck scope and evidence
- 33 private synthetic stdlib units / 0fail / 0error / 0skip; includes actual temporary Git clean/readback checks, synthetic Boot ZIP/nested mail/log/XML/proof consistency, version/buildId/source/provenance mismatch, real OpenCV pin rejection, aliases, output races, no-overwrite/atomic publication, evidence tamper, required task presence, cached/failed/stale log rejection, unknown/secret/Flow fields, safe CLI failure, public metadata preservation, and static init scope.
- Unit log: /var/tmp/ur05-producer-final-selfcheck-20261008.log
- Unit log SHA256: e83ec517bfc8ebbcf72c78cf6d5190c74293381b9041d80c30fe23d70c25607d
- Python AST PASS; syntax log /var/tmp/ur05-producer-syntax-20261008.log / SHA ad11ef1c967cda07b97008400325af30312a6cef8c4cc0113f6fffde7d84167b.
- Groovy init checked by static unit selectors only; actual compilation/Gradle execution NOT_RUN.
- Synthetic positive package test explicitly substitutes ONLY its private synthetic dependency pin in memory. Production constant remains unchanged; units are NOT actual OpenCV resolution, real build, actual security verification or release evidence.

## Frozen interface and actual caller requirements
Complete field/CLI contract is /var/tmp/ur05-producer-checkpoint-20261008.md / SHA a64dc74f0072f26c518febf3bef864dec1747f9c4a39e64e9fb1583a5a87b2a8, frozen at 21:45. Actual schemas remain the single frozen `cyf-api-local-*` formats; no legacy Flow receipt aliases.

CLI: package-api-local.py --opt-in --source-root ABS --commit HEX40 --tree HEX40 --version TOKEN --build-id TOKEN --build-root ABS --evidence ABS --evidence-sha256 HEX64 --output ABS.tgz. No build/Gradle/install subprocess. Producer loads only original verify_mail_runtime helper (never Flow main).

Required init env: CYF_LOCAL_RELEASE_OPT_IN=1 plus CYF_LOCAL_RELEASE_SOURCE_ROOT / BUILD_ROOT / VERSION / COMMIT / TREE / BUILD_ID. Init is source/settings-root-bound, root name jia, real BootJar ancestry and :starter:bootJar only. Public four CYF-* metadata inputs are declared at configuration; actual Implementation-Version is preserved (nullable), not derived from the release label. Original bootJar public verifier action is not replaced; proof action is appended after project evaluation and the original doLast. No Test/default/include-build changes or post-build JAR rewriting.

Caller must provide genuine orchestrator actual invocation, not evidence-cache exit zero. Use actual public Gradle argv with --console=plain and explicit required tasks; scoped --tests CLASS/METHOD public patterns supported and retained. No -x / credentials / arbitrary property injection. Each test task has real XML summaries (honest skips retained) and selector/fixture hash; two original starter security/runtime tests remain required. Only bootJar cache/up-to-date is disabled by this init; controller decides original test execution scope and noncached task selection. Ensure fresh external JAR/proof path is absent. No stale JAR deletion to fake freshness.

Producer build-root and output parent must be canonical private directories owned by its effective UID, disjoint from source and each other. Evidence/log/XML/proof are actual physical single-link files. Source is actual API Git top-level, exact and clean before/after; no generated files inside it. Clear PIPELINE_ID/BUILD_NUMBER/CYF_FLOW_GRADLE_ACTIVE rather than fabricating a Flow identity. Local dependency repository/external build routing and original pre-consumption OpenCV verification remain explicit main-controller prerequisites; existing cold-init.gradle cannot be used via fake Flow env. No actual local dependency-init path was authorized/added here.

Stdout success schema: {format:cyf-api-local-package-v1,identity:{version,buildId,commit,tree},package:{path,sha256,size},receiptSha256,applicationJarSha256,dependencyProvenanceSha256,buildEvidenceSha256,productionAuthorized:false}. Exact five archive payload names remain application.jar/application.metadata.json/application.sidecar.json/dependency.provenance.json/receipt.json. Receipt status=packaged, never installed/released/authorized. Package SHA is outside its own receipt/archive; later controller must preserve and pin it independently.

Failure schema: {format:cyf-api-local-package-error-v1,code:SAFE_CODE}, exit1. Allowlist: INPUT_INVALID, PATH_UNSAFE, SOURCE_MISMATCH, SOURCE_DIRTY, EVIDENCE_INVALID, EVIDENCE_TAMPERED, BUILD_NOT_FRESH, TEST_EVIDENCE_INVALID, JAR_INVALID, MAIL_RUNTIME_INVALID, PROVENANCE_INVALID, OUTPUT_EXISTS, IO_FAILURE. No raw exception, argv, env, log/XML or secret values printed. CLI grammar errors are safe too.

## Trust boundary and remaining scope
Consistent JSON/log/ZIP/checksums can still be forged by a malicious builder. Producer consistency is NOT authentication. Trusted root admission must independently bind expected version/buildId/commit/tree, build evidence, receipt/JAR/provenance/archive hash and consumed state. No producer output grants production authority.

Actual Gradle/init compile/tests/validateLayering/fresh BootJar/publicArtifactVerifier/local package remain NOT_RUN. Full root admission/unique durable installation transaction/schema-source wiring and all crash recovery, maintenance/inflight/dynamic identities, cutover, actual three-Agent business and production release remain subsequent UR05 work under main controller authorization. This producer does not clone a second installer state machine, grant DDL/service actions, or inspect active C1-C4/UR04/UR06 work.
