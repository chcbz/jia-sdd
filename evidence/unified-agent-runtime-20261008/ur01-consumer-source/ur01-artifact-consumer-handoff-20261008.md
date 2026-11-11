# UR01 guarded consumeArtifact source checkpoint (2026-10-08)

## Exact candidate and scope
- Fixed parent: `13aaec39c0567c049fad63d99b0a32d3e7af237c` / tree `107b2b9544012201588d7290b3c3eca860443732`.
- New independent harness/test commit: **`20742bc1848fdb8ecfb8c90af753ec7f4917bcf7`**.
- Tree: **`da3a31a5e489213134a6f02bd2e83e3104855e6a`**.
- Harness SHA256: **`a47c91f6ae79a205acd5210461503b76c9bff36421ed2b7fa6f44648d2835f20`**.
- Normal task-branch push and remote readback exact20742 MATCH; WT clean.
- Only two existing files:
  - `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs`
  - `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs`
- SOURCE remains **payload `7594fd72251d38b6e1d23a1a3cca184ae0d085e7` / tree `0827ce904179862ab55648fe99b780cea94faf98` /285 files**. Full archive remains3,594,240 bytes, SHA256 `f4dcd014e409b5a0e32f7419cd9500bf1f3e0022492f533736b366cd325f0106`.
- No self-reference pin. Do not archive20742 as payload; main must continue separate payload7594 archive + git-show20742 harness.
- r4 standalone13 candidate unchanged. No install/validate/engine/lib/API/UR04/rootdocs/Flow/production changes.

## Explicit wrapper interface
Import the exact separately supplied harness and call:

```js
const exit = await acceptance(explicitNonsecretEnv, {
  consumeArtifact: async accepted => {
    // Main-owned, opt-in same-Run consumer implementation; not provided here.
    // Await ALL owned Java/Node children and real UR04 selectors to completion.
    // Record detailed safe consumer diagnostics outside installed payload.
    return { status: 'PASS' }; // Only after the actual complete consumer succeeds.
  }
});
process.exitCode = exit;
```

Only an explicit function argument invokes consumption. No env/code loading, eval hook, extra CLI, retention flag, asynchronous background return, artifact copy/mv/rebase or cloud wrapper implementation was added. An absent callback follows original standalone behavior and produces no consumer receipt field. Caller remains bound not to copy/retain or launch unawaited children; arbitrary supplied JavaScript is trusted control code, not sandboxed by this interface.

**Callback return schema, exact plain data / own properties:**
- Success: `{ "status": "PASS" }` ONLY.
- Failure: `{ "status": "FAIL", "code": "CONSUMER_INPUT_REJECTED" }`, or code `CONSUMER_TEST_FAILED` / `CONSUMER_EXECUTION_FAILED` ONLY.
- No messages, headers, logs, env, exceptions, paths or extra fields on return. Detailed safe evidence is main wrapper's separate responsibility.
- Missing/incomplete/extra-field/accessor/symbol/nonplain/unknown-code return => independent `CONSUMER_RESULT_INVALID`, overallFAIL.
- Callback throw/rejection (irrespective of its raw error/code) => `CONSUMER_CALLBACK_THREW`, overallFAIL. Raw exception is never copied to receipt.
- Invalid callback type rejected **before input parse/hash/filesystem side effects** with `CONSUMER_CALLBACK_INVALID`.

## Preconditions, snapshot and post-checks
- All four original acceptance checks must independently be actualPASS. FAIL/NOT_RUN on any C makes zero callback calls, independent consumerNOT_RUN/`CONSUMER_INSTALL_NOT_ACCEPTED`. Original C statuses preserved.
- Original final fixed-source tree/archive readback remains mandatory. Hook additionally reconstructs285-member source tree, reads archive digest, verifies original canonical root+target dev/ino, target-local regular executable Node blob against actual C2/supplied tool proof, all59 runtime/engine members against original fixed-source bytes, and harness blob before callback.
- Re-derive original46-member engine catalog from the fixed adapter source. No fake installed module, Provider or lease acceptance is introduced.
- Capture full installed artifact regular file SHA/bytes/mode/uid/gid/dev/ino, directory facts and internal symlink text/resolve facts; external/unsafe/special paths rejected. No performance/resource threshold.
- Call at most once, `await` settlement before any cleanup. Deeply frozen allowlisted snapshot contains exactly:
  1. `format='ur01-accepted-clean-target-v1'`
  2. `cloudRun`
  3. `target`
  4. `nodeBin`
  5. `nodeSha256`
  6. `source` with ordered `commit,tree,files,archiveSha256,finalReadbackTree`
  7. `harnessSha256`
  8. `checks` with ordered `C1,C2,C3,C4`, all `'PASS'`
  9. `acceptedSnapshotSha256`
- Hash = SHA256 of UTF-8 `JSON.stringify` of the first8 ordered fields, **excluding the hash field itself and without trailing LF**. No receipt/env/config/state/diagnostic object is copied. This is an immutable acceptance-snapshot hash, **not** the finally-written final receipt-file hash.
- Wrapper receives a borrowed same-canonical target. The only permitted newly added target file is the existing UR04-required root-level `ur04-clean-artifact.json`, and it must be regular/non-alias. Hook does not create/parse that proof or implement UR04. All pre-existing target members must remain unchanged. Manifest semantics still belong to the existing UR04 reader/main wrapper.
- After callback PASS/FAIL/throw/invalid result, hook rechecks complete source/tree/archive, target/root identity, Node, original source-bound payload, installed artifact digest and harness. Persistent edits, additional installed files, chmod/link/inode changes or rebase make independent consumerFAIL, never rewrite original C results.
- Original finally still dev/ino/canonical-checks its exclusively-owned root before deletion and writes/syncs final receipt. Default, consumer failure and successful consumption all clean it. Ownership loss fails closed without deleting a foreign replacement; caller cannot request retention.

## Safe receipt codes and control guard
Callback failure-code enum: `CONSUMER_INPUT_REJECTED`, `CONSUMER_TEST_FAILED`, `CONSUMER_EXECUTION_FAILED`.
Internal safe codes:
- `CONSUMER_CALLBACK_INVALID` (pre-effect rejection)
- `CONSUMER_ALREADY_INVOKED` (one-shot closure repeat denial; no production retry path)
- `CONSUMER_INSTALL_NOT_ACCEPTED` (NOT_RUN,0 calls)
- `CONSUMER_CALLBACK_THREW`, `CONSUMER_RESULT_INVALID`
- `CONSUMER_SOURCE_NOT_FIXED`, `CONSUMER_SOURCE_CHANGED`
- `CONSUMER_TARGET_IDENTITY_CHANGED`, `CONSUMER_NODE_CHANGED`
- `CONSUMER_PAYLOAD_CHANGED`, `CONSUMER_ARTIFACT_CHANGED`
- `CONSUMER_PROJECTION_INVALID`, `CONSUMER_HARNESS_CHANGED`
- `CONSUMER_INTEGRITY_CHECK_FAILED` (safe fallback for filesystem/guard error, not raw error.code)

Successful receipt.consumer: `{status:'PASS',calls:1,acceptedSnapshot:<frozen allowlisted data>,integrityReadback:'PASS'}`. FAIL after invocation also has calls1/snapshot and safe code; post-integrity success may still bePASS while consumer itselfFAIL. Pre-gate failure has calls0/no snapshot. Guard failure takes precedence over a callback-returned failure; it cannot turn FAIL intoPASS. Early core/preflight failure may never reach the consumer slot.

Main's new opt-in wrapper must require overall exit0, final receipt.resultPASS, same Run/payload/tree/archive/harness provenance, original C1-C4 allPASS, **consumer.statusPASS/calls1/integrityReadbackPASS**, snapshot digest readback, and original cleanup evidence. Neither the snapshot nor fourC alone proves E05. Consumer outputs/JUnit/diagnostic evidence remain independently bound to its exact API source and six real selectors. Do not reuse standalone13 r4 as though it ran this hook.

## Actual local evidence only
- Exact20742/tree da3a on Node20.20.2.
- Log `/tmp/ur01-consumer-selfcheck-20261008.log`, SHA256 **`9ced2ec3e25c11a775dfd7a39daf9107e0aa8abb57e8ba05d2f410d5b4328b1d`**.
- Node syntax both files PASS; harness --selfcheck **54 static assertions PASS**; --describe `/tmp/ur01-consumer-describe-20261008.json`.
- Exact selector `artifact consumer|PPTX semantic` in existing runtime-host test: **9 PASS,0FAIL**,45 existing tests unselected (Node reports name-filter SKIP; no new skip/default gate).
- Eight hook tests cover type/no-env-loading/zero effects; every C's FAIL/NOT_RUN zero-call gate; exact order/deep freeze/no secret/one-shot/await before original cleanup; callback invalid/throw/whitelisted failure; source/archive/actual target replacement/Node/original payload/catalog/harness pre-negatives; dependency/mode/internal/external-link/source/archive/Node/actual target move/proof-symlink post-negatives; absent callback behavior; exact return-schema allowlist. Original PPTX lost-character/word/reordering regression retained.
- Fixtures use exact fixed source as static git blobs plus a hand-written **SYNTHETIC target**, non-working synthetic Node bytes and synthetic dependency file. Source extraction is stdlib-only. No local installer/npm/pip/venv/Gradle/Java/Runtime/HTTP/DB/UR04 is run or replaced by mocks. Tests execute the exact original final-source/consumer/catch/finally snippet, not a duplicate cleanup implementation. Synthetic prerequisite states are not actual C1-C4 evidence.
- Parent13->candidate cumulative diff--check PASS, source literal unchanged, only2paths, task remoteMATCH, WTclean.

## Remaining boundaries / next step
UR01 source slice complete, no source-side blocker. **New payload actual cloud C1-C4, actual consumeArtifact lane and E05: NOT_RUN.** Main owns standalone r4 timing after API139 terminal/restore, then separate exact newharness/consumer binding. UR04 clientSOURCE pin still374 and must be handled only in its next own checkpoint; not simultaneously claimed or modified here. No deploy, production compiler, secret enrollment, Provider, historical state migration or portable artifact claim.
