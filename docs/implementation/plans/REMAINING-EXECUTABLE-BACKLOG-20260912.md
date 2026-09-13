# Remaining executable backlog — 2026-09-12

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
