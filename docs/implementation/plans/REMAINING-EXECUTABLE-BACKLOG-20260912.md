# Remaining executable backlog — 2026-09-12

## 2026-09-13 12:26 CST delta

- **API38 已发布核验**：develop `741cc3f2`，84 个配置 selector 范围测试和构建成功；部署单 `69522605` 成功、线上 JAR `37fb8ae0` 与同 Run 制品一致，PID `3348479`/10018 健康 UP。交付 E05 有界重试/退避及无伪造终态的 deferral；完整跨 Agent 重派仍未完成。
- **F06 源码已合入并推送 develop `5bfdb2a8`**：22 条路径保持 Owner `8c927ec3` 字节一致；与 E05 路径无交集。88 个 selector 配置已保存并 readback，云端验证尚未取得结果。两张新增表未执行迁移，不能称已启用。
- **继续并行而不是排 Reviewer**：E05 显式目标过期工作项重派、F06 认证成果确认/查询接口分别由独立 worktree Owner 实施；主控做集成、云效及线上核验。精确 Owner 只以 TASKS.yaml 为准。已完成 F06 原 Owner 不再可达，wait/close 返回 not_found，未把它当作运行进程失败。
- **激活前置已查实一部分**：当前 API 的本机 3306 TCP 连接与 MySQL processlist `jia` 对应；已有 artifact/event/workitem/meta 表，F06 两表缺失。仅只读查询，未改 schema/开关/生产数据。真实身份、付费授权与原生客户端业务 ACK 仍不能用部署成功代替。


## 2026-09-13 11:59 CST delta

- E05 corrected741cc3f2/7031b74c is now remote develop; initial00adb ambiguous-timeout FAILED mutation removed before publication.55lightweight policy/readback checks PASS; real service/transaction regressions authored, not locally run. Config84selectorsd3cc saved/readbackAPPLIED. One actual Start returned API38 INIT/sourcepending; observe38only, no duplicateStart. API37 remains lastverified.
- Full E05 explicit different-agent reassignment remains a concrete new-command/lease/API/client packet, not an external user blocker and not completed by bounded retries. Its shared task-event registry paths are currently F06-owned, so coordinate that specific integration rather than reintroducing a global source queue.
- Web99 actual410file/9online proof retained with FlowFAIL. Cache-verifier sourcef2f93 integrated712b65 and installed53070ba8 after20offline checks/readback; sourceOwnerclosed. No synthetic redeploy99/nginxreload. Newhelperproductionuse awaits next genuineWebcandidate.

## 2026-09-13 11:41 CST delta

- **Web99 已安装且线上核验通过，但 Flow FAIL 保留**：develop edace747，2151 PASS / 2 pending，构建和扫描成功；410安装文件/9线上响应匹配同次制品 b57049c1。部署单69521776最后首页校验三次读到旧98，后来独立读取已匹配99。host record仍为installed；没有伪改为online_verified，也不重装掩盖失败。
- 已另派独立 root worktree 修复首页等待校验：当前3次/2秒窗口与Nginx已配置30秒文件缓存不匹配；保留哈希、TLS和取消能力，不把安装成功当线上成功。该修复不阻塞当前已核验页面。
- API loopback health UP，公网未登录 `/agent/map` 返回401（不是502），仅证明连通和认证边界，不证明登录业务。
- E05初候选00adb被主控发现将未确认的SENT终结为FAILED、阻断真实迟到ACK；原Owner已恢复继续做无状态变更的耗尽处理及真实ACK回归，未推送。不同Agent重派仍需新的不可变命令/API契约，不冒充完整E05。F06并行开发。
- 附件存储、工作区、语音启用，以及合法账号/付费上限/六技能真实结果验收仍需分别落实，不因安装完成而归档。

## 2026-09-13 11:16 CST delta

- F02 Web corrected candidate `6d103e81` plus main lint-only `edace747` is now remote develop. Getter/ref rendering and pre-request async identity/cancel races were corrected before push. Owner/main related tests each14 PASS, ESLint PASS. Auto Run99 is RUNNING; source checkout metadata remains pending, so neither exact cloud verification nor deployment is claimed yet. Web98/API37 remain last verified.
- Two independent API Writers continue F06 outcome state and E05 timeout/failure/reassignment policy; no Reviewer/global source queue. Completed Web Owner released.
- Passive client evidence since10:30CST: active PID1183165, three correlated registration ACKs following API37, one earlier ack_timeout retained. Counts alone do not prove unique-profile coverage. Known client default inbox has3skill scopes and0installed/acknowledged-result files; six real skill acceptance is still absent, not replaced by transport ACK. No restart, credential read or paid action performed.
- Current published deployment policy removes unsupported fixed5GiB reserve/time-age failure rules; do not reintroduce historical thresholds from older summaries. Actual byte requirements, mutual exclusion, source/artifact integrity and health evidence remain.

## 2026-09-13 10:56 CST delta

- **API37 已发布并核验**：develop `e54f579e`，79 个配置测试类对应云端构建成功，部署单 69520789 成功；同次制品、线上 JAR/记录一致，PID 3284987 监听 10018，健康 UP。F02 HTTP 上传/下载代码已部署，但文件存储仍默认关闭，真实上传下载验收未完成。
- **Web98 已发布并核验**：develop `441c39fe`，2143 PASS / 2 pending / 0 failures；部署单 69520737，410 个安装文件和 9 个线上响应摘要一致。E08 只读看板代码已部署，任务工作区默认关闭；不冒充已启用或完整协作功能交付。Run97 失败与修复历史保留。
- **并行开发**：F02 Web 上传/下载交互继续实施；新增 F06 accepted/superseded 成果状态独立 API Writer。Owner 自检、主控合入 develop 后云效验证发布，不设独立 Reviewer 或全局 Writer 队列。精确 Owner 只登记在 TASKS.yaml。
- **耗时核验**：两次 API 冷启动约 458/494 秒，GC 暂停约 29/26 秒，不能把全部启动时间归因 GC。只读诊断未改生产；失效的 Mini helper 已释放，不做重复调用。
- 原有身份、明确付费授权、真实 Client/Provider ACK、ES/native 依赖仍有效；这些不阻塞无依赖代码并行开发，也不算已验收。


## 2026-09-13 10:25 CST delta

- F02authenticatedHTTPadapter e54f/4f6fa7ef nowdevelop;13newcontrollertests sourceadded. Config79selectors28ea79APPLIED. OneactualStartreturnedAPI37INIT withsourcepending; neverstartagainformissingmetadata. Actualrequest/upload/downloadcaps24/16/64MiB; storage remainsdefaultOFF,activation/GC/businessnotdone.
- Web441c39f autoRun98sourceverified after71relatedtestsPASS; earlier97FAILretained. API36/Web96remainlastverifiedpair. AllcollectedcodingOwnersclosed; mainobserves37/98inparallelwithoutReviewer. Fullgoal/externalacceptanceboundariesretained.

## 2026-09-13 10:18 CST delta

- API36/5ece9141 SUCCESS:78configuredselectors/build, JAR1c073e3b/receipt3371a3b7, order69520177,PID3257882/10018healthUPandcanonicalrecordmatch. No retry; Run35testfailurerootcausescorrected. E04completiondependencyunlock and F02internalstorage source shipped, notdefaultoffactivation orpublicuploadbusinessacceptance.
- Web97/b33 failed beforedeployment:2136PASS2pending1C07Ca11ybeforeAllimporterror. ExistingSFCtestloader missednewWorkItemBoard import; main441c39f nowloadsactualboard+composable,addsDOMregression,71relatedtestsPASS/configured10000mstimeout,ESLintPASS. Firstlocalno-config2000mstimeoutsandpreexistingglobalcommentlintfailure retained; no assertion/timeoutpolicyweakening. Changedcandidatepushed; observeautoFlowonly.
- F02authenticatedHTTPadapter separateOwner activelyimplementing NEWcontroller/DTO/tests; no overlapwithmainWebrepair. FullE08operations/business/provider/clientACK/ES/nativeexternal andfullA16/M4/M5remainopen. ExactOwners onlyTASKS.yaml; noindependentReviewer.

## 2026-09-13 09:44 CST delta

- Web96 SUCCESS10c4/tree5b1298:2138PASS2pending, artifact3b68e16a, order69519905,410installed/9onlineMATCH. Deployment45s; observed transactiondownload158M->81M, not controlledbenchmark/zeroRPM claim. No separateReviewer.
- API35 failed403service tests/5failed/5skipped beforedeployment. E04 exacttwo-event matcher correction32db ready; F02four failures assigned independentOwner; no unchangedretry. API33 remainslastverified.
- E08 actualworkitemboard/eligibleexistingactions now assigned in independentWebworktree; no waitingforAPI. CurrentOwners onlyTASKS.yaml. FullE08 and authenticated/paid/provider/clientACK/ES/external acceptance not closed.

## 2026-09-13 09:27 CST delta

- E04 authoritative completion unlock17ebb and F02 scoped immutable storagee343 collected and merged, preserving independently pushed login/form/CORS80383. New APIdevelop72f03/tree5c8ff4da is in Run35 (78selectors); prior foreignRun34 built80383 successfully but deployment failed, not current production. API33 remains lastverified until35hostproof.
- Web runtime dependency missing-only9cd7 integrated10c4/tree5b1298b; main18targetedtestsPASS. AutoRun96 nowrunning; no extra manualStart. Alloriginalruntimechecks/packages/GPG/cache retained, actualspeedgain still unproven. Web95 remains lastverified until96hostproof.
- All three Owner candidates are collected with clean worktrees, no independentReviewer. F02 remains defaultOFF/internalservice API only, without publicupload/downloadadapter or automaticorphanGC. E03activation and realbusiness/client/provideracceptance are not closed by these runs. Exactrunmonitors35/96registered; old emailcounters preserved.


## 23:48 CST delta (current verified release pair)

- API develop270ae185 / Run33 SUCCESS: E02 recommendation and stored coordinator projection released; JAR12c29e32, receipt52f23bad, PID2843894/10018 healthUP. Initial disk admission failure69511830 happened before lifecycle; one same-artifact retry69511949 succeeded after clean completed-worktree reclamation. Cold startup533s. Run32's2fixturefailures were corrected, not relabeled green.
- Web develop61007609 / Run95 SUCCESS: 2135passed/2pending/0failed; artifact6f0f6913, order69512210; all410installedfiles and9online hashes match. E03 code and E07 manualpreview/localcoverage released. E03 frontend/backend flags remain OFF, and E07 has no persisted finalteamconfirmation endpoint; neither is full business acceptance.
- Streaming Web deploy helper first real production use is now verified,107s wall time. Initial2homepage polls returned old content, third matched; exact cache mechanism not proven. Run93/94 historical failures retained.
- Parallel source lanes: E04 sameOwner completing actual submitted->completed dependency unlock; F02 immutable scoped artifact file/hash storage newly assigned; Web runtime dependency installer efficiency newly assigned. No independent Reviewer or global source queue. Owners remain solely inTASKS.yaml.
- OuterFlow bootstrap missing-only update286cfcc passed5tests/readback, but Run95 exposed a second fullRPM install in scripts/ci/prepare-runtime.mjs (110downloads/132operations). This is assigned, not falsely declared a measured speedup. The next genuine candidate should validate it; no synthetic re-release of95.
- FullA16/M4/M5, E03 activation, Archive authenticated browser flows, monetary/provider/clientACK and ES realfixture acceptance remain open per original scope. Do not repeat already-shippedsource just because those acceptance inputs are missing. Existing exact-run monitor registration preserved; emaildelivery still unproved.


## 23:00 CST delta (supersedes earlier current-state projections)

- API Run31/f6554168 is now cloud SUCCESS and independently reconciled with installed record, JAR c6fa5726, receipt0f6ba20f, PID2783320/10018 and healthUP. First disk-admission failure69510439 remains recorded; same-artifact retry69510726 succeeded. Login task owned lifecycle; main did not interrupt or duplicate it. A16/E03 default-off technical slices are deployed, not fully activated/business accepted.
- E02 team preview/coordinator projection00db9f07 and E03Web1b3c2dd1 are pushed to develop. Web auto Run94 has exact source and is building. API Run32 was started once after a concurrent display-name-only change invalidated the first pre-write context; exact source metadata is pending. Cloud API config now66selectors, not the65 snapshot used by31. No duplicate Start or local build.
- E04 dependency scheduling and E07 team UI continue in independent worktrees. E07 first candidate8676/6testsPASS needs a bounded same-Owner correction for local override coverage and same-task version invalidation before release. No independent Reviewer/global source queue.
- Two more fully clean completed worktrees were removed without force (branches/commits retained), reclaiming509,734,912 allocated bytes. perf-w04-rum-entry had ignored content and was preserved; shared perf-w04-web dependencies and all active worktrees/evidence/runtime retained. Capacity after was6,051,725,312 bytes.
- Exact run monitors94/32 registered without resetting previous email counters. SMTP acceptance remains unproven; no email-delivery claim. Business/provider/client ACK and activation boundaries in the remaining acceptance record still apply.


## 21:40 CST delta

- A16 root cause reproduced: H2 2.4.240 generated IN retains closed DDL session; equivalent OR also fails, simple CASE succeeds with independent connections on both 2.3.232/2.4.240. Fixture-only correction518a052e retains generated uniqueness guards and all transaction assertions, with added guard regression. No production schema/dependency change. Run28 remains FAIL, not retried.
- E03 backend8501cded collected/Ownerclosed and integrated as5fa6fd14/tree21e7a024 with the H2 fix. Exact develop pushed; API5260799 Run29 build514194885 RUNNING, deploy514194886 INIT. Configuration65selectors7ddf8db6 updated once/readbackAPPLIED; monitor29registered. This is not deployment evidence.
- E02 implementation continues independently. New E03Web Owner in separate worktree implements the frozen suggest/edit/manual-confirm flow and explicit unavailable/CAS/idempotency semantics, not an automatic assignment/provider side channel. No independent Reviewer and no source queue.
- E03 API remains opt-in/default-off; frontend, controlled acceptance and activation are not complete merely because the backend candidate exists.


## 21:18 CST delta

- E02 greedy team recommendation is now independently assigned; E01 prerequisite is releasedRun25. E03 work-item planning has11new source/test files in its own worktree, notyetaccepted orreleased. CurrentexactOwners remain solely inTASKS.yaml.
- A16 Run27 diagnostic exposed H2 first pending-operation insert failure(SQLState90098), after all source/permission checks. No deployment. Minimal standalone exactDDL/JDBC probes pass on H22.3.232 andBoot4.0.1BOM2.4.240, so neither a driverdowngrade nor schemaweakening is justified. Run28 adds full immutable exception-chain logging; it is a diagnostic run, not a fix claim. Source67ac20d5, observe existingRun28 only.
- Current business acceptance boundary reconciled against actualAPI25/Web93 pair in `handoffs/REMAINING-BUSINESS-ACCEPTANCE-20260912.json`: wallet/bounty, sixrealClientACKs, hostingrent, voiceProvider and Archive authenticated flows remain unproven and require their stated identity/authorization inputs. Source ancestry and released foundation code do not close these lanes.

## 20:45 CST delta

- A16 Run26 stopped at cloud tests: service214cases/1failed/5skipped, first async accept in the new real-transaction test. No deployment; original Owner resumed for exact root cause and minimal correction. Run25 remains healthy live.
- Web stream helper candidate1c6e07bc installed as6a6d7c39 after14tests and realRun93single-pass410-file scan passed; oldhelper backed up and no active deployment interrupted. Next production Flow use remains unverified; noRun93rerun.
- E03 implementation continues independently; no global queue or Reviewer introduced.

## 20:36 CST execution update (supersedes dated projections below)

- **E01 source/UI increment live:** API5260799 Run25 SUCCESS, exact develop `ef1a9659` / tree `d36fe144`, JAR `ea9de1bd`, order69508149, PID2659818/10018 and healthUP verified. Stable equal-score order regression fixed; prior Run24 failure retained, not retried.
- **Web93 has a qualified closure, not a green Flow:** exact develop `b58d3727`; 2119 passing/2 pending/0 failures, 410 installed files and 9 online hashes match. Flow remains FAIL because the original final homepage digest check failed at20:23:23. Repeating that same read now matches; transient mechanism unknown. No reinstallation merely to hide this failure. Actual develop push automatically triggered93.
- **A16 final source collected and integrated:** final Owner candidate `0a7eb60e` replaces old `a5a9cea8`; integrated/pushed as `9672b4bc` / tree `4016635a`. Owner released. Next exact Flow pending. This is only default-off async redrive acceptance with an independent disabled switch, not the executor/claim fence or complete A16.
- **Two independent implementation Owners in parallel:** `FLOW-WEB-STREAM-INSTALL-20260912` fixes repeated gzip random seeks and bounded final hash diagnostics; `M4-E03-DECOMPOSE-20260912` implements the bounded work-item decomposition/manual confirmation package. They do not wait for API cloud build, and have disjoint source paths.
- **F03 remains environment-dependent:** default production ES health isolation regression shipped inRun25; real ES health/index acceptance is not demonstrated. Full M4/M5, Archive authenticated acceptance, client ACK and bounded paid/provider validation remain open.
- No independent Reviewer, no global source Writer queue, no local Gradle/Vite production build. Exact current Owners/gates are only in `TASKS.yaml`; these are timestamped facts, not another ledger.
- Evidence: `handoffs/FLOW-API-RUN25-DEPLOYED-20260912.json`, `handoffs/FLOW-WEB-RUN93-ONLINE-WITH-FAILURE-20260912.json`.

## 19:24 CST execution update (supersedes release-pending baseline below)

- **P1 release increment done:** API5260799 Run23 SUCCESS for develop688a3e65/tree608e799; exact JARa5cc9db1, host/order69507020, PID2607082/10018 and loopback UP verified. The Run22 failure/recovery remains history; do not rerun it. WX-specific controlled MySQL/business-delay evidence remains distinct.
- **P2 release done:** Web4403172 Run92 SUCCESS, exact1ac5cb1e, 410 installed files and9 online response hashes match. Current two-component Gitee/develop push+webhook configuration readback confirmed; actual automatic trigger not yet evidenced. No duplicate release.
- **P3 assigned:** PERF-A16-ASYNC-20260912, owner01a09558-6985-74c3-9805-9bd2723858ab; one bounded async route-family source increment, independent worktree. Existing status projection remains partial.
- **P4 foundations assigned in parallel:** M4-E01-CANDIDATE-20260912 owner01a09558-b6dc-7683-bbc2-e8f8e504bfc7; M5-F03-ES-20260912 owner01a09559-0cd2-79c3-af5b-9fabe1431c82. Non-overlapping scoring versus ES paths; downstream E/F/G work is not all claimed or completed.
- **P5/P6 still external acceptance:** legitimate identities/browser/client ACK and explicitly bounded paid/provider authorization required; no fabricated successful acceptance.
- All implementation owners self-check, main integrates candidates into develop and reconciles exact Flow release. No independent Reviewer or global source-write queue. Current owners/gates remain solely in TASKS.yaml; this is a dated projection.
- Evidence: `/home/isp/wsps/cyf/docs/implementation/handoffs/FLOW-API-RUN23-DEPLOYED-20260912.json`.

## Scope and fact baseline

This is a short reconciliation plan, not a runtime ledger, task claim, gate, or reviewer assignment. It does not alter `TASKS.yaml`, status files, contracts, Flow configuration, or production.

Read-only facts used:

- The SDD index still marks performance, Archive Pavilion, economy, voice, and advanced Juyi collaboration as unfinished; released historical features are excluded.
- API `origin/develop` is `a9a43056cad534c0fb6addb666ba2a9e5989c910` (tree to be taken from the API repository at execution). WX integration `8fe0e096735fcd947ca58d43011de894825a0e50` is an ancestor of deployed Run 18 commit `a8489561586400af049eee625d90b6e98e834f04` (`merge-base --is-ancestor` returns 0). The WX-path diff from `8fe0e096` to `a848956` contains only later RequestId-filter additions, so the WX integration paths are retained in the deployed candidate. Old `awaiting_final_verification` wording is not a reason to rewrite or re-release WX source.
- API Flow `5260799` Run 18 deployed `a8489561586400af049eee625d90b6e98e834f04`, proving the retained WX source is deployed but not proving the later A16 `a9a43056` increment. Run 21 tested/built `7ba431dcaedea3c71260717ca7c36b47a781cda1` but stopped before lifecycle because the release lock was busy. API Run 22 has now started with installer `0935738e` and the 58-selector configuration; its terminal exact checkout, test/build, artifact, deployment, and online evidence remain required before any newer-API release claim.
- Web `origin/develop` is `1ac5cb1e4973919bacf054e961b43ff24d47e832`; Flow `4403172` Run 92 is running for that exact commit. It is not release evidence until its exact checkout, tests, artifact, deploy order, and online check are recorded.
- A16 at `a9a43056` adds only `GET /agent/internal/command-operations/v1/operations/{operationId}`: an ACL-scoped, redacted status projection over the pre-existing privileged command audit rows. It does **not** migrate ordinary long-running endpoints to async submission/atomic acceptance/outbox, so it cannot make `ASYNC_ACK` compliance pass globally.
- M4/M5 (`E01–E08`, `F01–F06`, `G01–G08`) remain draft/unclaimed source work. Their product-stage grouping is M4 = `E01–E08,F01,F02,F06`; M5 = `F03–F05,G01–G08` (the historical F03–F05 label discrepancy remains disclosed, not rewritten).

## Executable packages (maximum six)

### P1 — API Run 22 completion plus WX-specific delayed evidence

**Class:** A16/new performance increment has release evidence pending; WX source is already deployed and retains only final specific MySQL/business evidence.

**Minimal scope**

1. Observe the already-started API Run 22 using installer `0935738e` and the 58-selector configuration; reconcile its exact checkout/tree, test/build result, artifact digest, deployment order, and online check. Do not start a duplicate run.
2. Keep WX `8fe0e096` as deployed Run 18 ancestry. Run only its frozen, specific final MySQL/business-delay proof if still required by the WX acceptance contract; do not recreate source, migrations, or a release solely for WX.
3. Keep full A16 separate: its current status projection is not a completed async-operation migration.

**Real dependencies**

- Run 22's terminal Flow record is authoritative for the newer API candidate; it must bind the exact source commit before any A16 release statement.
- WX final selectors must use the retained/deployed source lineage and a controlled isolated MySQL fixture. No production DDL/DML or new paid/business action is implied.
- The specific WX business-delay evidence is distinct from a generic Flow health/build result.

**Independent parallel path**

Run 22 observation is independent of P2, P4, P5, and business-acceptance preparations. WX selector preparation is read-only and can proceed without a new source writer or release queue.

**Minimum Flow verification**

For Run 22: API pipeline `5260799`, exact checkout/tree, 58 configured relevant selectors, `validateLayering`, `:starter:bootJar`, artifact digest, same-run deploy order, and healthy online check. Record the WX final targeted/MySQL/business-delay result separately; neither a generic build nor Run 18's health check replaces that evidence.

---

### P2 — Web Run 92 outcome only

**Class:** implemented source / release evidence pending.

**Minimal scope**

Observe the already-started `4403172` Run 92 for `1ac5cb1e`; reconcile its exact source, test summary, artifact digest, deployment order, and `/` plus `/juyiting` online checks. Do not start a duplicate run or edit feature source unless Run 92 attributes a new source defect.

**Real dependencies**

- Run 92’s own terminal result and exact Flow checkout are authoritative.
- Push-trigger automation remains unverified; a successful manual Run 92 must not be presented as proof that every develop push auto-releases.

**Independent parallel path**

Fully independent of P1 and the API work. It may run alongside P3/P4/P5 because it is evidence collection, not a source queue.

**Minimum Flow verification**

The existing Run 92 must show JavaScript scan, `npm ci`, full test result, Vite build, artifact digest, deployment order, and online verification for `1ac5cb1e`. If it fails, first classify the failed phase before any retry.

---

### P3 — Complete the actual PERF-A16 source contract (not the status projection)

**Class:** genuine backend source gap.

**Minimal scope**

Freeze an endpoint-by-endpoint A16 migration matrix before code: identify only long operations eligible for versioned `ASYNC_ACK`; for each, define the preserved legacy behavior, operation creation/lookup path, idempotency key and replay behavior, ACL/non-enumeration behavior, transaction/outbox boundary, monotonic state/result/error view, and retention. Then implement one bounded route family at a time. The current privileged redrive/reissue status read may be reused only as a projection reference, not as evidence that unrelated routes are asynchronous.

**Real dependencies**

- The frozen A16 contract and registry classification from PERF-01; missing runtime capture/registry evidence means no global compliance claim.
- The responsible owner must perform risk self-checks for any transaction, ACL, idempotency, outbox, or replay change and bind cloud relevant-test evidence. Do not infer those semantics from the current status-only code; this plan creates no independent Reviewer requirement.
- P1 deployment is not a prerequisite for source work, but production `ASYNC_ACK` acceptance requires a released exact candidate plus per-route evidence.

**Independent parallel path**

Can begin with a read-only route inventory/contract matrix immediately, in a separate API worktree, without waiting for P1/P2/P4/P5. Implementations are sequential only where they share the same transaction/outbox paths.

**Minimum Flow verification**

For each bounded route family: targeted API tests covering ACL, idempotent replay/conflict, rollback/no duplicate mutation, status retention/non-enumeration, and old-route compatibility; then the API Flow selectors, `validateLayering`, boot JAR, exact artifact/deploy, and the dedicated async ACK timing/functional evidence. Do not substitute global p99 claims for route evidence.

---

### P4 — M4/M5 real source backlog, split by true prerequisites

**Class:** genuine unimplemented collaboration source work; not recoverable by old M3/WX ledgers.

**Minimal scope**

Start with independently contractable foundations only:

- **M4 foundation:** E01 candidate constraints/scoring; E03 editable work-item decomposition; F02 artifact storage/hash strategy; F06 accepted/superseded outcome state. Preserve existing task/event, Rabbit, ACL, identity, and replay semantics; do not create an automatic dispatch side channel.
- **M4 dependent chain:** E02 follows E01; E04 follows E03; E05 requires accepted D06 semantics; E06 follows E01–E05; E07 follows E01/E02; E08 depends on the existing collaboration UI/event paths. These are separate follow-on packets, not one speculative mega-change.
- **M5 independent start:** F03 Elasticsearch recovery/prod configuration is the only M5 item declared with no dependency. F04 follows F01–F03, F05 follows F04 and D03. G01–G08 remain test/operations/flag/migration/security work with their stated prerequisites; G04/G08 are end-of-chain, not early coding targets.

**Real dependencies**

- E01 depends on B03; E03/E04/E05/E08 depend on the cited B/C/D milestones. The accepted M3 transport is not authorization to change its transaction, ACL, migration, or replay contracts.
- F03 requires a deployable Elasticsearch environment/configuration decision; F04/F05 cannot be completed from mock indexes alone.
- G05–G08 require the feature behavior they validate; G06 is a migration/runbook scope and must not be invented before a schema contract exists.

**Independent parallel path**

Run two non-overlapping preparations in parallel: M4 foundation contract/source work and F03 recovery analysis/source work. Keep each subsequent E/F/G packet in its own worktree/path scope; there is no global writer queue.

**Minimum Flow verification**

Per packet, run only its affected API/Web selectors in Flow. E08/G03 require Web test/build evidence; F03–F05 require API selectors plus a controlled ES health/index fixture; G02 requires a controlled Rabbit recovery environment; G04/G08 require the defined multi-agent/ACL/load acceptance matrix. No production Rabbit activation, migration, or load test is authorized by this plan.

---

### P5 — Archive Pavilion authenticated reader closure

**Class:** source may already be present; actual authenticated adapter/browser acceptance remains unproven.

**Minimal scope**

Use a lawful controlled login to exercise the already-delivered `/archive/v1` path: catalog/chapter read, progress save/read after reopen, bookmark and private note conflict behavior, and two-identity/two-client isolation/404 behavior. Confirm the Web adapter actually sends authenticated requests and only shows saved state after server confirmation. If that exposes a source defect, limit the repair to the adapter/reader path and preserve `/chat/library/search`, `/agent/active` prohibition, server-derived scope, CAS, and idempotency contracts.

**Real dependencies**

- A legitimate controlled authenticated test identity/client and browser session; no fabricated JWT, bypass, or assumed login success.
- Existing API/Web deployed pair and CORS behavior; the CORS patch itself is already evidenced and must not be reimplemented.

**Independent parallel path**

Browser/adapter preparation can proceed independently of P1–P4. The actual two-identity checks may use dedicated test identities and do not require economy balances or Provider calls.

**Minimum Flow verification**

If source changes, run affected Web reader tests/build and affected API selectors in their component Flow runs. The acceptance run additionally needs controlled browser evidence for the five authenticated scenarios above; a health check or mocked adapter ACK is insufficient.

---

### P6 — Authorized real-business and external-provider acceptance lanes

**Class:** deployed/accepted technical slices with deliberately missing business authorization; no source replay or fabricated ACK.

**Minimal scope**

Prepare, but do not execute without explicit authorization, three separately auditable lanes:

1. **Wallet/funded bounty:** controlled authenticated issuance/funding, quote/display/explicit target-Agent claim, settlement or cancel/refund, replay/competition/rollback, and deployed Web readback. W04–W06 are not business-accepted merely because their technical source/deployment evidence exists.
2. **Six skills:** controlled seed/current client purchase/install/activation/result ACK/capture-or-refund and wallet/Web readback. The installed client mapping and mock/static tests do not prove a designated six-package installation or an Agent ACK.
3. **Hosting rent and voice:** rent requires quote → explicit confirmation → debit → managed provision/renew/compensation/readback under the default-off rent contract; voice requires a controlled authenticated STT/TTS call and Provider capability proof. Neither rent nor voice may silently consume funds or Provider quota.

**Real dependencies**

- Explicit user/business authorization for each monetary debit, refund, production DML, and Provider-paid call; legal controlled identity/client/Agent/audio fixtures; a stated spend/rollback boundary.
- Rent must retain server-mode-only charging, explicit confirmation, and default-off flags. Voice requires the runtime/host/allowlist lifecycle prerequisites as well as a Provider-approved call.
- The three lanes can prepare in parallel, but execution touching the same wallet/Agent must be serialized by its frozen idempotency/locking contract.

**Independent parallel path**

All three can independently assemble non-secret test scripts, expected receipts, and readback assertions. They must not share credentials, invent client ACKs, or run paid actions concurrently against the same funding/account scope.

**Minimum Flow verification**

No new Flow run is a substitute for this package’s business evidence. If source changes are found, use the affected API/Web Flow selectors and exact artifact/deploy evidence. Business closure additionally requires controlled authenticated request/response receipts, server and Web readback, ledger/lease/installation/operation state, and the real Agent ACK or real Provider result as applicable.

## Explicit exclusions from new development

- Do not recreate or re-release WX source: `8fe0e096` is an ancestor of deployed Run 18 commit `a848956`; its residual is specific final MySQL/business-delay evidence, not source or deployment work.
- Do not treat Run 18 or Run 21 as evidence for newer A16 commits; use Run 22's terminal exact record. Do not treat Web Run 91 as evidence for newer Web commits.
- Do not mark the economy, skills, rent, or voice work complete from mocks, deployments, health probes, static client mappings, or unverifiable ACKs.
- Do not use the old ledger wording to claim M4/M5, full PERF-A16, Rabbit activation, Archive browser closure, or global 3-second SLO completion.
