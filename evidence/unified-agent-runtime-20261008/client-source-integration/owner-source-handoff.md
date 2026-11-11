# UR-01-20261008 — entry/provisioning source convergence handoff (2026-10-08)

Status: this authorized OFFLINE SOURCE ENTRY slice complete and Owner self-check
passed, committed and task branch pushed. NOT whole UR/M3 acceptance, NOT a
release/cutover, NOT proof that all TASK adapters are complete. No independent
Reviewer is requested. Candidate handed to Main for integration/source-stage
review; no source self-acceptance.

Owner Sol/Knuth: 01a1195e-e058-7ea2-bfc2-1a0e4736cdd4.
Worktree: /home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008
Branch: codex/ur01-unified-agent-runtime-20261008
Baseline: 0d80e588be271891348e38b8892d9b9a9b0bb436
Previously received r2: 95437e9e7dce2a0af900f4d41cfe5e36bcae661d
First provisioning retirement commit: a80b9fab53a0d0787a7eb0c5b89c1f628aad1092
First retirement tree: 9057c6847f6e1cb1d14ca17037ed8ae70601c818
FINAL exact commit: 0d1351ee2c69ff18d189cbd2ec996b524e3fe1fa
FINAL exact tree: aa20c4213acacb8212dc3595b0c39db263c6de71
Worktree clean after commit/push: YES.
Remote refs/heads/codex/ur01-unified-agent-runtime-20261008 read back exact final SHA.
No force push, develop push/merge, deploy, production service/PID action,
credential/state/schema migration, package installation, Gradle or Java/DB test.
Source deletion of old unit files is NOT online service retirement.

## Minimal implemented convergence, not a business engine rewrite

- Delete conf/codex-ws-agent/managed-host.mjs: old API-key ensure/observe broker,
  credential persistence/recovery/template copying and Unix provisioning socket.
  Remove two dead engine broker declarations; no normal model/workspace rewrite.
- shell/codex_ws_agent_install.sh and bin/codex_ws_agent.sh are tiny no-effects
  retired diagnostics: all arguments/envs reject before config/common helpers,
  profile/generation creation, packages, PID/service controls or workspace archive.
  They are NOT auth/execute aliases or silent redirects.
- Root install.sh removes old codex/codex-ws-agent mappings and rejects those
  names even in mixed argument lists before component installs. Agent profile
  selects only cyf-agent-runtime-v1 (no implicit generic Node upgrade); full
  profile replaces only retired Agent entry and preserves other component order.
  All unrelated mappings/installers/common helpers remain. Runtime rejection
  propagates nonzero through the two existing failure-summary branches.
- shell/sh_list.txt and both installation skills name sole latest Runtime entry;
  install-candidate/INSTALL-CANDIDATE.md retains useful provider-contract/audit
  facts, removes runnable old installation/API-key readback recommendations.
- Delete ONLY source systemd/codex-ws-agent.service and @.service. Current unified
  unit templates remain byte-identical and use artifact-local Node/external JSON.
  No installed unit was read/removed/disabled/restarted by this work.
- Execution package is library-only (no npm start). Unified authoritative payload
  catalog excludes old auth env/profile/broker/docs/install tools/offline ACK
  migration/diagnostic probes; rejects their re-injection (including symlinks)
  and start/prestart/poststart/bin entries. Literal import and locked dependency
  closure remain validated. Provider/model auth is not Agent execution auth.
- Old positive provisioning/installer-only tests replaced, not skipped. Preserve
  workspace/lock regression prefix byte-for-byte (54,076 bytes), scoped provider
  ACL/130-character profile tests with explicit non-provisioning fixture, and
  existing actual Runtime child ownership/shutdown/locks. Historical provider
  freeze/readback tests use test-only baseline catalog, not old installer code.
- Main-approved epoch oracle note supports safe Date range INCLUDING zero/negative
  values; projection tests cover those/legal lower bound and invalid bounds in
  both directions. New-execution expiry unchanged; no time-based production fix.
  CHAT/result confirmations, unique checkpoint and r2 raw fingerprint unchanged.

## Exact latest commit paths (11)

M install.sh
M shell/sh_list.txt
M bin/codex_ws_agent.sh
D systemd/codex-ws-agent.service
D systemd/codex-ws-agent@.service
M skills/codex-ws-agent-install/SKILL.md
M skills/install-profile/SKILL.md
M conf/codex-ws-agent/install-candidate/INSTALL-CANDIDATE.md
M conf/codex-ws-agent/test/instance-installer-launcher.test.mjs
M conf/cyf-agent-runtime-v1/README.md
A conf/cyf-agent-runtime-v1/test/install-entry-convergence.test.mjs

Cumulative two-retirement-slice exact 24 paths relative to received95437e9:
/tmp/ur01-entry-retirement-paths-20261008.txt (appended below).
Entire task baseline exact path manifest including inherited earlier milestones:
/tmp/ur01-entry-task-baseline-paths-20261008.txt.
Pre-edit freezes: /tmp/ur01-provisioning-freeze-20261008.md and
/tmp/ur01-entry-freeze-20261008.md; necessary new test paths notified before writes.
No manual control-document or foreign worktree edit.

## Exact final tree Owner self-check (not cloud/cross-end evidence)

1. Entry/installer/guides retirement smallest: 22 PASS / 0 FAIL / 0 SKIP,
   525.669ms; /tmp/ur01-entry-final-small-20261008.log.
   SHA25684533ebab6ad19a07e1d7d75e705030d470bef43d454809f521923ca81b88447.
   Evidence1eb0db9197e36c93bee0f4934a494235761dece1aa6cc05916f386a74a771b7c.
2. FINAL25 touched client suites: 659 PASS / 0 FAIL / 0 CANCELLED / 1 SKIP,
   77.171857s; /tmp/ur01-entry-final-verified-20261008.log.
   SHA25654ff3bfe4b389b9024bb683a85e8d112aab516b673db4769bc9fe652df86457d.
   Evidence4cacc56701e4115dd8a52c989e69d0f6ab1e1e84fe7312b1f589fc35f3403006.
   Exact selectors /tmp/ur01-entry-selectors-20261008.txt (appended below).
   The ONE SKIP is unchanged UR03 actual HTTP ACK/fence/recovery/restart NOT_RUN.
3. Baseline changed38mjs node --check +6sh bash -n, whitespace, exact11 newly
   authorized paths, unrelated source preservation, workspace test-prefix bytes,
   deleted old source entries, unchanged UR03/current units, fixed API fixture
   equality PASS; /tmp/ur01-entry-final-static-20261008.log.
   SHA25649c402e9e66d95ffdeac7bd4e0b3e530ac7e5d67e7b9285d05b4e0d1846aac5e.
   Evidencea1b61b1c2ec7c5d3546008c632ed2a2f5d121b6f954c2c0fbc044866fba6eceb.

Node20.20.2. Existing isolated mocked-egress Python interpreter only; no paid
Provider requests. Evidence input manifest /tmp/ur01-entry-final-evidence-inputs-20261008.txt,
SHA2561a90e3c2ef297f6542c771e4517b0755e2a7e08198479e279ff4b86d9a2e5a21.
Evidence result accepted means test proof ONLY, never task acceptance.

Encountered failure NOT hidden: initial entry suite20pass1fail showed actual nested
Runtime installer rejected wrong Node but root dispatcher returned0. Exact-string
pre-test patch had missed whitespace. Attributed via orchestrator before retry;
assertion-checked two-branch source fix + interactive/non-Agent failure tests changed
candidate. Subsequent22pass and final25suite run pass. No repeated unchanged-input
failure. Failed /tmp/ur01-entry-small-20261008.log (SHA2564d6bd488293172d14990dcf3dfb24d62b0c775b0b3d5cfd8b7014cf1e057021e)
and corrected /tmp/ur01-entry-small-fixed-20261008.log retained.

## Fixed shared inputs and remote proof

API782a76eb53ffdd3411d8a356ccd46a1e0ccbccf6 v2 is BYTE_IDENTICAL to client.
Current v2 SHA2560fcc887699bde04c016b8f986a77d656c0d6e2531ba00c5a46daf418be6372dc.
Raw E05 unchanged SHA256057a4626387846f4bf420cab046d7d0bb4d12cdae6569e90839af00161cbd5a3.
UR03 historical v1 unchanged SHA25656d7c3d31a33191eb23b0209158dd0395c184f661aa694eb7cc29f0942322adb.
Historical baseline catalog SHA256e24c5e2267e023fdeaef74fb5c57547f4d11f04961606141a07be88283e3c845.
The temporary dirty-API-note provenance reported during first slice is now closed
by read-only equality against actual fixed782a76eb committed bytes.
Push log /tmp/ur01-entry-push-20261008.log; final remote ref
/tmp/ur01-entry-remote-after-20261008.log reads exact0d1351ee.
Push is not an artifact/build/Flow/release success.

## Precise residual source/business evidence gap — not concealed by version probe

Directed inspection found NO existing client actorAgentId query or reassignment
lease HTTP caller. API facade /agent/tasks/{taskId}/work-items/{workItemId}/
reassignments/{reassignmentId}/lease(+start/heartbeat) is NOT the existing personal
workspace conversation /internal/agent lease path. Runtime nativeFetch currently
admits only /internal/agent routes. No guessed lease DTO/path/field or synthetic
actor selected from frames was introduced. A future original-implementation
reuse must bind actor exactly to trusted manifest/authenticated full subject.

Current six declarations (TASK_INVITE, WORK_ITEM_EXECUTE, WORK_ITEM_RESUME,
REQUEST_RESPOND, REVIEW_EXECUTE, CONTEXT_REFRESH) use workspaceManager plus
commandAdapterReady, whose probe is codex --version. This is **NOT PROOF** that all
six business adapters or original lease/source/ACL/transaction/result paths are
complete. Local E05 checkpoint/HTTP ACK test uses business stub, not actual TASK
business acceptance. No types were silently removed/hidden or wire amended to get
PASS. Main has assigned Curie read-only original-path localization; must distinguish
reassignment-specific from whole-TASK gap before minimal Owner continuation.

Audit /tmp/ur01-entry-task-lease-readiness-gap-20261008.log;
coverage evidence4ee42316d1de239c03cfbeffecc4ec39e036eb7b2e1adfa4461beabeed39f328
is blocked/not reusable, NOT a passing business-adapter test. Source entry phase
can be handed over without blocking on that separate real evidence gap, but whole
client/M3 is NOT done. Unverified WORK_ITEM_CANCEL remains unadvertised as before;
exact CHAT cancellation remains intact, not replaced by command cancellation.

## Clean-target dependency/ABI gap — explicit, not mocked away

NO successful isolated fresh-target installation/toolchain/relocation test or
client exact-commit Flow artifact proof exists from this Owner. Staging copies
only provided Node20.20.2 binary; local file/ldd shows x86-64 ELF system loader and
external z/brotli/libcrypto.so.1.1/libssl.so.1.1/libstdc++/glibc dependencies, NOT
bundled by installer. Version pin alone does not prove target OS/ABI compatibility.

Python venv --copies does not vendor its base stdlib/shared runtime. Here Python
3.6.8 is shared, stdlib /usr/lib64/python3.6, libdir /usr/lib64,
LDLIBRARY libpython3.6m.so. The six pinned Python distributions (python-docx0.8.11,
python-pptx0.6.23, openpyxl3.1.3, Pillow8.4.0, PyPDF2 1.28.6, reportlab3.6.8) include
native/ABI requirements. Clean target must prove those dependencies, real imports,
health/helper behavior and artifact relocation on the intended OS/architecture;
existing missing-toolchain/failed-stage/lock tests cannot prove that success path.
External Codex CLI/app-server, private model homes and provider configuration also
require actual target evidence; a CLI version probe is not business readiness.

Read-only observation /tmp/ur01-entry-clean-target-abi-gap-20261008.log;
coverage evidenced1bb9fe5ceee59b06a7bb66b82d289404ff307e2a2d3c332766bc5877e911ace
is blocked/not reusable. No packages/OS libs were installed or copied into production
and no portability/source-toolchain redesign was performed to hide this gap.

## Migration/operational gates — no migration executed

README explicitly lists full dynamic/shared identity/installation/maintenance map,
private old association/journal/credential audit preservation, unique verified
mapping into sealed manifests, stopped exact writers, backup+code/format/identity
state plan, inbox/ledger/ACK FIFO/receipt/CHAT/skill/provider unknown-outcome and
worktree/material/inode accounting. No auto persona mapping, fingerprint conversion,
queue clearing, paid replay, credential adoption or binary-only rollback.

Remaining Main/runner gates: actual TASK original adapter/lease closure; real
Java/D06/isolated-MySQL/native/skill cross-end acceptance (UR03 HTTP remains NOT_RUN);
clean target and client Flow/source-artifact binding; all online dynamic identities,
in-flight work and maintenance authorization; stopped-writer migration/recovery
plan; versioned release/cutover and old-authority retirement; three-Agent real
business acceptance. Main owns API Flow123/new782a76eb cloud evidence; this Owner
neither ran Java/DB nor reported a mock as that boundary. No current release is
permitted merely because this source candidate was pushed.

## Appended cumulative retirement paths (95437e9 -> final)
M	bin/codex_ws_agent.sh
M	conf/codex-ws-agent/agent-client.mjs
M	conf/codex-ws-agent/install-candidate/INSTALL-CANDIDATE.md
D	conf/codex-ws-agent/managed-host.mjs
M	conf/codex-ws-agent/package.json
A	conf/codex-ws-agent/test/fixtures/retired-install-payload.baseline-0d80e58.txt
M	conf/codex-ws-agent/test/install-candidate-check.test.mjs
M	conf/codex-ws-agent/test/instance-installer-launcher.test.mjs
M	conf/codex-ws-agent/test/managed-host.test.mjs
M	conf/codex-ws-agent/test/managed-image-scope-config.test.mjs
M	conf/codex-ws-agent/test/workspace-manager.test.mjs
M	conf/cyf-agent-runtime-v1/README.md
M	conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs
M	conf/cyf-agent-runtime-v1/test/canonical-dispatch-r2.test.mjs
M	conf/cyf-agent-runtime-v1/test/fixtures/unified-runtime-wire-v2.redacted.json
A	conf/cyf-agent-runtime-v1/test/install-entry-convergence.test.mjs
M	conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs
M	install.sh
M	shell/codex_ws_agent_install.sh
M	shell/sh_list.txt
M	skills/codex-ws-agent-install/SKILL.md
M	skills/install-profile/SKILL.md
D	systemd/codex-ws-agent.service
D	systemd/codex-ws-agent@.service

## Appended final25 exact test selectors
conf/cyf-agent-runtime-v1/test/runtime-v1.test.mjs
conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs
conf/cyf-agent-runtime-v1/test/unified-runtime-acceptance.test.mjs
conf/cyf-agent-runtime-v1/test/canonical-dispatch-r2.test.mjs
conf/codex-ws-agent/test/agent-client.test.mjs
conf/codex-ws-agent/test/ack-checkpoint.test.mjs
conf/codex-ws-agent/test/registration-ack.test.mjs
conf/codex-ws-agent/test/skill-install-manager.test.mjs
conf/codex-ws-agent/test/config-runtime.test.mjs
conf/codex-ws-agent/test/conversation-native.test.mjs
conf/codex-ws-agent/test/controlled-image-http-runtime.test.mjs
conf/codex-ws-agent/test/controlled-image-gpt-cli-runtime.test.mjs
conf/codex-ws-agent/test/controlled-image-v2-bridge.test.mjs
conf/codex-ws-agent/test/controlled-image-v3-lane.test.mjs
conf/codex-ws-agent/test/controlled-image-v3-runtime.test.mjs
conf/codex-ws-agent/test/managed-image-scope-config.test.mjs
conf/codex-ws-agent/test/mixed-material-api-wire-v3.test.mjs
conf/codex-ws-agent/test/native-bounty-capability.test.mjs
conf/codex-ws-agent/test/typed-inspection-runtime.test.mjs
conf/codex-ws-agent/test/workspace-file-bridge.test.mjs
conf/codex-ws-agent/test/managed-host.test.mjs
conf/codex-ws-agent/test/instance-installer-launcher.test.mjs
conf/codex-ws-agent/test/workspace-manager.test.mjs
conf/codex-ws-agent/test/install-candidate-check.test.mjs
conf/cyf-agent-runtime-v1/test/install-entry-convergence.test.mjs
