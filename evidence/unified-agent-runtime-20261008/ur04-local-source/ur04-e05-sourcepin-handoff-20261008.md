# UR04 SOURCE7594 / explicit local gate / real mapper beans checkpoint (2026-10-08)

## Immutable source candidate
- Parent: `34d9e2d6c5b9915c8bb259d14a4761d2ff782e89` / tree `8d625893abd35fbadb1a9cf40e271c59660c1b4a`.
- Commit: **`92a3a72b8a7c5574c36edbc01ffee1288e9ad69c`** / tree **`9da54e7bda3860e383126a53f6216d1331988044`**.
- Task branch normal push/readback exact MATCH; WT clean; exact committed blob bytes read back.
- Four changed paths, all within the existing six-file scope:
- `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java`
- `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpFixture.java`
- `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs`
- `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/ur04-e05-http.init.gradle`

Original SQL schema and synthetic child bytes unchanged. No production/client/UR03/rootdocs/ledger/Flow changes.

## Actual changes
1. Only source7594 accepted: commit7594fd72251d38b6e1d23a1a3cca184ae0d085e7/tree0827ce904179862ab55648fe99b780cea94faf98/285/tar3594240/SHAf4dcd014e409b5a0e32f7419cd9500bf1f3e0022492f533736b366cd325f0106. Java CLIENT and boot-tree assertion, Node SOURCE and init description updated. Old374 pre-IO rejection verified; synthetic mismatches of commit/tree/archive/count remain fail-closed. Full tree/archive/installed dependency/Node proof retained, not substituted with source-only evidence.
2. Init's only launcher opt-in is `UR04_LOCAL_ACCEPTANCE=1`, safe failure `UR04_LOCAL_ACCEPTANCE_REQUIRED`; no CYF_FLOW_GRADLE_ACTIVE fallback or spoof. Same five non-sensitive inputs, sourceSet/dependency/settings and included-build isolation, maxParallelForks1 and disabled task cache/up-to-date kept. Parent-created private Node subprocess marker renamed UR04_PRIVATE_CHILD (not an extra caller input). No consumer wrapper or default-test wiring added.
3. Actual BaseDaoImpl has inherited `@Inject protected M baseMapper`. Eleven prior Spring DAO factories preassigned it with reflection but that did not satisfy Spring bean resolution. Native Chat DAO was also assembled outside Spring. Now all12 exact real SqlSessionTemplate mapper proxies are explicit typed @Beans, and all12 real DAO instances are managed for normal injection; native handler gets managed ChatMessageDao. Persona catalog uses its existing actual @Inject setter and existing cache bean. Reflection wire removed; no scans, mocks, fixed permissions or ACL changes. Mapper SQL configuration and original account XML remain intact. This is static source wiring evidence, NOT proof Spring Boot passed.

## Static only selfcheck
- Node20.20.2, both original JS syntax PASS; selfcheck13 assertions; child env9 assertions.
- Static285 real git tree reconstructed; actual git archive length/digest matches pinned7594. This source check is not clean installed artifact proof.
- Original18 JDBC binds,44 constructor arities,19 schema tables/18 business entity maps inspected (no SQL or Java execution).
- All12 instantiated inherited DAO types traced to production BaseDaoImpl and exact mapper Spring bean/source registration; reflection absent.
- Six local-gate equality cases checked statically; whitelist5/settings/sourceSet/no-cache retained. No Groovy/Gradle execution.
- Original six selector names and complete method bodies are BYTE IDENTICAL to34d9. No assertion weakened/skipped or subset substituted.
- Four-path diff-check PASS; exact candidate tracked blobs verified.
- Log `/tmp/ur04-sourcepin-static-selfcheck-20261008.log`, SHA256 `03c4253f986529fb2103876a45f21c55fd21be472504465d57b3fb7ea1ff9987`.
- Reproduction-only temporary static scripts: `/tmp/ur04-sourcepin-static-audit-20261008.py` and `/tmp/ur04-sourcepin-node-static-20261008.mjs`.
- Two temp audit issues before finalPASS were diagnostic tooling only (default Node stdout buffer; Python3.6 subprocess keyword), resolved without source/pin/acceptance changes. Earlier attempt logs retained at `/tmp/ur04-sourcepin-static-selfcheck-attempt1-20261008.log` and `/tmp/ur04-sourcepin-static-selfcheck-attempt2-20261008.log`.

## Six real selectors: all NOT_RUN
- `e05ActualClientHttpCommitsOriginalResultAndTerminalAck`: NOT_RUN
- `e05LostResultReadbackSurvivesJavaAndNodeRestart`: NOT_RUN
- `e05TerminalAckLostResponseReplaysPriorWithoutWorkRerun`: NOT_RUN
- `e05PreparedCommitRefencesAndRollbackIsDurable`: NOT_RUN
- `e05SourceAndOriginalResultProofStayFailClosed`: NOT_RUN
- `e05UnknownStartedNeverRerunsAndSiblingRemainsReady`: NOT_RUN

Java compile, Spring/Tomcat/nativeWS, actual original engine→lease/result/D06, dual-JVM/H2 durability and independent receipt remain NOT_RUN. Synthetic child is explicitly nonpaid and never Provider/model quality proof. Enroll/MySQL/online identities/migration/production also NOT_RUN.

## Remaining exact inputs / main-owned execution
Five unchanged fixture inputs: UR04_API_COMMIT, UR04_CLIENT_ROOT, UR04_CLIENT_COMMIT, UR04_NODE_BIN, UR04_ARTIFACT_ROOT. Main must integrate candidate and bind full clean API commit/tree; provide full SOURCE7594 archive+ur04-client-source.json and the ACTUAL original installed target proven by C1-C4 allPASS, full member/link hashes and Node/toolchain immutable provenance. Must not feed a source-only archive or old artifact as installed target, fake cleanRun, or change evidence to claim it passed.
Main must additionally freeze the actual same-batch local backend artifact consumption/lifetime/receipt binding, before the client harness finally cleanup; no copy/mv/rebase/retain. This source slice does not implement that wrapper. Formal six-selector execution is main-owned via orchestrator only after exact real inputs exist. No source-side blocker for this checkpoint; missing actual artifact/execution contract remains explicit.

Machine handoff: `/tmp/ur04-e05-sourcepin-handoff-20261008.json`.
