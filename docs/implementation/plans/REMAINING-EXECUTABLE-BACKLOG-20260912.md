# Remaining executable backlog — 2026-09-12

## Scope and fact baseline

This is a short reconciliation plan, not a runtime ledger, task claim, gate, or reviewer assignment. It does not alter `TASKS.yaml`, status files, contracts, Flow configuration, or production.

Read-only facts used:

- The SDD index still marks performance, Archive Pavilion, economy, voice, and advanced Juyi collaboration as unfinished; released historical features are excluded.
- API `origin/develop` is `a9a43056cad534c0fb6addb666ba2a9e5989c910` (tree to be taken from the API repository at execution). It descends from WX integration `8fe0e096735fcd947ca58d43011de894825a0e50`; therefore the old WX wording `awaiting_final_verification` is **not** a reason to rewrite its already integrated source chain.
- The deployed API evidence is Flow `5260799` Run 18 on `a8489561586400af049eee625d90b6e98e834f04`, not `a9a43056`. Run 21 tested/built `7ba431dcaedea3c71260717ca7c36b47a781cda1` but stopped before lifecycle because the release lock was busy. Thus neither Run 18 nor Run 21 proves deployment of WX `8fe0e096` or A16 `a9a43056`.
- Web `origin/develop` is `1ac5cb1e4973919bacf054e961b43ff24d47e832`; Flow `4403172` Run 92 is running for that exact commit. It is not release evidence until its exact checkout, tests, artifact, deploy order, and online check are recorded.
- A16 at `a9a43056` adds only `GET /agent/internal/command-operations/v1/operations/{operationId}`: an ACL-scoped, redacted status projection over the pre-existing privileged command audit rows. It does **not** migrate ordinary long-running endpoints to async submission/atomic acceptance/outbox, so it cannot make `ASYNC_ACK` compliance pass globally.
- M4/M5 (`E01–E08`, `F01–F06`, `G01–G08`) remain draft/unclaimed source work. Their product-stage grouping is M4 = `E01–E08,F01,F02,F06`; M5 = `F03–F05,G01–G08` (the historical F03–F05 label discrepancy remains disclosed, not rewritten).

## Executable packages (maximum six)

### P1 — API candidate release reconciliation: performance batch plus WX

**Class:** implemented source / missing exact release and final targeted verification; no WX source rewrite.

**Minimal scope**

1. Attribute and correct only the bounded API installer release-lock acquisition path that stopped Run 21 before lifecycle.
2. Use a materially changed release-control candidate, then let the normal API Flow validate and deploy the exact API commit containing `8fe0e096` and `a9a43056`.
3. For WX, retain `8fe0e096` as the integrated source baseline; run only the frozen final selectors/MySQL proof required by its accepted source contract on the candidate, rather than recreating its implementation chain.

**Real dependencies**

- The current lock holder must finish or a safe, independently attributable lock remediation must exist; do not kill another owner’s process.
- A new Flow run must be tied to an API commit at or after `a9a43056`; Run 18 and Run 21 cannot be relabeled as proof for it.
- WX final fixture selectors must use the actual accepted source/candidate and a controlled isolated MySQL fixture. No production DDL/DML is implied.

**Independent parallel path**

The release-control repair/Flow path is independent of P2, P4, P5, and all business-acceptance preparations. WX source inspection and selector preparation are read-only and can proceed while the lock is being attributed.

**Minimum Flow verification**

API pipeline `5260799`, exact checkout/tree, configured relevant selectors (currently 58-class configuration for the newer candidate), `validateLayering`, `:starter:bootJar`, artifact digest, same-run deploy order, and healthy online check. Record separately the WX targeted/MySQL result; a successful build alone is not WX business release evidence.

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
- Critical ownership/review is required for any transaction, ACL, idempotency, outbox, or replay change. Do not infer those semantics from the current status-only code.
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

- Do not recreate WX source work: `8fe0e096` is an ancestor of current API develop. Its residual is exact verification/release evidence, not a second implementation.
- Do not treat Run 18, Run 21, or Web Run 91 as evidence for newer commits.
- Do not mark the economy, skills, rent, or voice work complete from mocks, deployments, health probes, static client mappings, or unverifiable ACKs.
- Do not use the old ledger wording to claim M4/M5, full PERF-A16, Rabbit activation, Archive browser closure, or global 3-second SLO completion.
