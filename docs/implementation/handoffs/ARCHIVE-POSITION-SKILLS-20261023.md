# ARCHIVE-POSITION-SKILLS-20261023

Owner: current chat, serial implementation. CANDIDATE_DELIVERED; ACCEPTANCE_INCOMPLETE (not deployed).
T0: 2026-10-23T23:05:35+08:00. Target: 2026-10-24T03:05:35+08:00.
Scope/acceptance: specs/archive-agent-maintenance/implementation-plan-4h-20261023.md, A01–A12. No production actions.

## Frozen inputs
- Root 2003b0acf21407809c3c524d271a07dddf7b5888
- API 041548f601385a3463fbba06b929991371d93d9c
- Web 638084d26ec9a193240566bf45b33602cef8e0e0
- Client cbc1050825a40378313f283e9f25dc46d44c1ea4
- Worktree: C:/Users/Think/.codex/worktrees/archive-position-skills/cyf-web-kit; Client sibling isp-install.
- Branches: codex/archive-position-skills[-api|-web|-client]. Old feature remains read-only. Original checkout protected.
- Interface authority: api/docs/interface-standard.md v1.2. No old wire fallback.
- Read: AGENTS, project-map, sdd-workflow, juyiting-runbook, MODEL_ROUTING, orchestration README; API/Client AGENTS. User instruction requiring final independent read-only review overrides older no-review routing for this task only.

## P0 observations
- 23:09 managed checkout failed due to Windows long paths; repository-local core.longpaths=true, second creation succeeded. No partial checkout reset or deletion.
- 23:14 SSH read-only host check succeeded; MySQL client and Node available. Installed production Runtime exists but is NOT an authorized test installation.
- 23:14 backend Flow5260799 list succeeded (latest observed Run249 SUCCESS); historical result, not candidate evidence. No Run started or configuration changed.
- Isolated MySQL/Runtime readiness not yet proven. Maven/Gradle and candidate Flow pending.

## Contract supplement
Generic position aggregate is owner/client/tenant-scoped, persisted and row-locked. Only POSITION/GENERAL. Position default skill references are many-to-many; capacity configurable. Active appointment sources determine POSITION desire; GENERAL receives a separately retained entitlement that explicit uninstall can remove. Backend grant availability is separate from installation receipt and from archive task authority. No marketplace orders are manufactured.
Management authority is operator-provisioned, scope/resource-specific DB data; owner JWT alone cannot grant public-library access. Native mutation joins the existing Runtime fence then locks the same position scope as resignation/publication. Missing schema/config/receipt fails closed. Scope mutation, idempotency record and audit commit together. JSON state is versioned domain data, not executable skill code.

## Historical P0 next step (superseded by closeout below)
P1 persistent domain lifecycle, scoped management API, unit/transaction tests. P2 adapters and archive writes. A01–A12 currently NOT_RUN.

## 00:35 checkpoint (not acceptance)
- API candidate 72e454fc446e273eeac6ceaa4bc07d0604682205, tree d9dcad792787cb1286e92bdd5d6bcc163699e662: isolated ARM Gradle core tests, transaction-test compilation, chat compilation and validateLayering PASS. Formal Flow pending.
- Earlier chaoyoufan P1 daemon failed: dmesg confirmed OOM kill, no compile conclusion. Moved diagnostics to owned /mnt/Workspace/aps-20261023 on ARM test host; no installed service changed.
- Client installer Linux 110/110 PASS; parser/native recovery 6/6 PASS. Source still evolving, not final candidate evidence.
- Position lifecycle, native installer, generic source parser, archive DRAFT/AUTO jobs and historical edition backend implemented. New Web prototype verified in browser; product page and reader integration in progress, tests pending.
- Prototype: web/prototypes/juyiting/{interaction-completion.js,production-ui.css,index.html,specs/prototype-spec.md}; third tab, appointment/install separation, GENERAL retention, unknown/recovery. Desktop local HTTP18787 observed. Mobile/product E2E not yet verified.
- Real DB/native HTTP/full Runtime A02-A11, formal CI, independent read-only review and final candidate commits remain incomplete. No production changes.

## Final pinned candidate closeout (2026-10-24T02:29:32.235254+08:00)

- API `4520d81971bbe9b093a89f2ecba4964adb18d1c1` / tree `281dac8fd08c3c5f496b19cb7bda0709d7feb18a`.
- Web `45a217baf80c28b0c33b4da1a85f491323d1c1e0` / tree `86e7168c6a593995e4ebbe8f3632e19ad921a1ac`.
- Client `bade440cccbf835859d790ed05f5f6cdab02ede2` / tree `15807ca593d5a1abb94ee53925405faab613bd41`; Runtime source version1.2.10, NOT installed.
- All three ordinary-pushed to their named candidate branches; full remote SHA readback in `specs/archive-agent-maintenance/verification-20261024/component-remotes.json`. No merge to develop or original old feature branch; original D-drive dirty checkout remains untouched.
- Root gitlinks/current integration.yaml updated to these candidates. Original integration.yaml bytes preserved in integration-d2-baseline-20261023.yaml. Root commit identifies this handoff; no self-referential final SHA.

### Implemented and tested
- Two skill types, many-to-many positions/defaults, configurable capacity and multi-appointments; shared POSITION last-source removal and retained GENERAL entitlement/files. Backend identity/resource authority is independent of Runtime installation.
- Real MySQL + Spring/MyBatis + HTTP + RuntimeV1Client + durable installer/parser: reviewed package download/install/receipt, two new data-only books, shared-position removal, GENERAL retention, default DRAFT, authorized AUTO, historical edition and private bookmark/note isolation, revocation fences, source/operation recovery.
- Signed RSA OAuth JWT through production ResourceServerConfig/AccountSecurityJwtValidator and real user DAO: configure/appoint/create/manual publish/resign and original-key recovery; unauthenticated401, old auth_epoch401, normal-user403, cross-owner404, JWT denied at native routes. No mocked JWT decoder.
- Backend CAS losing AUTO job becomes persisted FAILED/ARCHIVE_EDITION_CONFLICT; explicit retry creates a new fixed-source job against current edition; unrelated books continue. Manual draft CAS still409 without overwriting.
- Final fresh API113/113 (core15 + transaction4 + native/session41 + maintenance13 + reader40), zero failure/error/skip; compile and validateLayering PASS through existing orchestrator and /tmp/cyf-gradle.lock. Runner/result/XML names/hashes and timestamps recorded in api-final-tests.json. API clean and Client source unchanged before/after.
- Final Web100/100; 8-file lint comparison no new findings. Baseline JuyiHall141 errors/108 warnings and reader-test1 error remain. Real ArchiveMaintenance.vue desktop/mobile screenshots use explicit read-only mock API;390px viewport has no horizontal overflow. Screenshot component bytes equal final candidate, not a full product E2E.
- Final Client155+6=161 PASS, zero skip. Input tar is conf/ + systemd/ subset, not full-repo archive;340 file bytes match exact commit, tested source digest matches these bytes. Digest ordering is pathlib component order. Full archive SHA must not be compared as if same scope.

### Failures attributed and fixed (not hidden)
- First server Gradle killed by OOM (dmesg); isolated ARM host used for diagnostics, no production service restart.
- Initial1.1.0 package SKILL identity invalid; immutable1.1.1 prepared instead, originalZIP retained.
- Revoked poll item marked outer transaction rollback-only; moved permission filtering under correct transactional boundary and retested.
- AUTO CAS conflict previously stayed WAITING and retried indefinitely; persisted FAILED plus next-job continuation verified.
- Reader regression sourceSet initially missed ArchiveManifestBundle/ArchiveGoldenSummary; failure attributed through orchestrator, explicit types added, final fresh regression passed.
- Three newly introduced Web lint findings fixed without editing baseline lint debt.

### Package, schema and operations
- Package archive-maintenance1.1.1,3006bytes,SHA2565861b17f8eed7bb71a4c1d3ab93f2ec23a734e2915269f7715413e021d03c780; manifest c5f20d2633fdd5c1fca570a257bb3d9380775fa7ff4d8f6ad6353eecc63c5c07. Prepared only; catalog approval occurred ONLY inside isolated test fixture.
- Controlled SQL: API agent/jia-agent-mapper/src/main/resources/db/agent-position-skills.sql and chat/jia-chat-mapper/src/main/resources/db/archive-maintenance-jobs.sql. Five new tables, no startupDDL/automatic authority; oldD2 archive_maintenance_job left intact.
- Test MySQL processes on chaoyoufan and ARM host and two local preview processes stopped after exact ownership checks; receipts in verification-20261024. Data/logs retained; no destructive directory cleanup, production credentials copied, production changes, paid calls, real LinChong appointment or content release.

### Open gates and next action
1. Existing Flow5260799 and4403172 branch guards do not admit candidate branches (official read-only query00:59+08). No run/config change, no local production build. Need an agreed existing-Flow candidate verification/guard or reviewed integration approach; do not merge just to bypass CI restrictions.
2. Native fixture establishes channel liveness with explicit auth.bind; full installed Runtime WebSocket registration and browser OAuth→appointment→maintenance→reader→resign/recovery remain NOT_RUN. RuntimeHost6 tests are focused, not complete system acceptance.
3. Independent read-only review required by task remains NOT_RUN; no subagent dispatched, Owner self-check not mislabelled as independent review.
4. No complete Romance of the Three Kingdoms source supplied; two structurally different generated text samples prove data-only import, not whole-book acceptance. No OCR/PDF/EPUB/URL importer, job cancellation, package-upgrade migration, or SongJiang natural-language toolchain delivery claimed.
5. Complete A01–A12 gating before acceptance; production migration/deployment/approval remains separate authorization. Old84-case matrix untouched.

### Timing/evidence boundary
T0/target unchanged. Candidate work closed within240minutes; full four-hour objective NOT achieved because mandatory gates remain. Per-phase human time is not independently measured; do not infer performance promises. Raw logs live in owned /mnt/Workspace/aps-20261023/p4complete and client-final-pinned; only sanitized summaries/source hashes/Flow guard snapshots/visuals committed. Root source delivery, diagnostic tests, formal Flow, full Runtime/browser and production acceptance remain separate states.

- Root收口结构检查通过：sddw候选pins及18个导航目标核对，git diff --check通过；仅修复14处历史Linux绝对Markdown链接为相对链接，历史验收状态未改。证据摘要见verification-20261024/README.md；不把结构通过算作业务测试。
