# UR01 Run138 C3/C4 minimal fix — source handoff, 2026-10-08

## Exact source and transport
- WT: `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008`; branch `codex/ur01-unified-agent-runtime-20261008`.
- Fixed parent `fa4e4070060ec30ba2a46eb93561f3a94ce3b507` / tree `a31cc7a100ec2039fdf784236527be874ae09b14`.
- **Payload** `7594fd72251d38b6e1d23a1a3cca184ae0d085e7` / tree `0827ce904179862ab55648fe99b780cea94faf98`: 285 regular tracked files.
- Full no-prefix `git archive --format=tar PAYLOAD`: 3,594,240 bytes; SHA256 `f4dcd014e409b5a0e32f7419cd9500bf1f3e0022492f533736b366cd325f0106`. PAX comment equals payload SHA; all git members mode100644/100755.
- **Independent harness** `13aaec39c0567c049fad63d99b0a32d3e7af237c` / tree `107b2b9544012201588d7290b3c3eca860443732`.
- Harness blob SHA256 `789a1fe56086a5172407ea8fce07da8bedfb7188636ec2bbdf7aa4e1540e75ae`.
- Second commit changes ONLY SOURCE.commit/tree, preserving file count285. Transport must archive payload7594 and git-show harness13aa separately; never label either as old374/d8/7c. Source archive includes its tracked earlier harness bytes; separately supplied harness is intentionally the new pin, no self-reference.
- Normal push to the task branch only; remote readback exact13aa MATCH; WT clean. No develop/Flow/production operations.

## Independent evidence and causes
Read `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/clean-install138/diagnostic.json`; verified JSON SHA256 `7793c53272f1ef3427e64cac740a20737b52f5bbc8c67797cbd132fcdd1bb710` and all58 dependencyLogs content SHA256. Original rawlog outputTruncated=true; not called complete.

1. C3: original installer builds venv under exclusive stage, then mv without relocating generated launchers. Target helper health/imports PASS but six direct Python shebangs/launchers and three activation files retain deleted stage root. No module/Python-devel/pin incompatibility inference. Stale links0.
2. C4: actual helper `create_pptx` calls `wrapped(instruction,40)[:10]`, writes separate paragraphs. Exact synthetic instruction is **48** characters (correcting initial progress-message count), and original stdlib wrapping gives `UR01 synthetic clean-install acceptance` / `material`. Python-pptx shape.text joins paragraphs with newline, so old contiguous substring assertion fails. Reproduced original producer wrapping via runpy/stdlib; no dependency import or fake PPTX result. No demonstrated producer content-loss defect for this material; helper unchanged.

## Four existing affected paths only
- `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/install.sh`
  - Before stage validation/publication: stdlib-only rewriting of recognized venv-generated Python shebangs and distlib shell launchers into relative shell/Python trampolines, preserving actual interpreter basename, script body/mode, argv and quoting. Works in both stage/final target and avoids long absolute shebang limits.
  - Three activation assignments rebound to final target, without leftover stage references. Unknown stage-bearing executable/binary/body/link/activation fails closed while original exclusively-owned stage cleanup remains active.
  - Finalize rewritten script SHA256/size in corresponding installed distribution RECORD before observing stage, preserving stage->target distribution metadata integrity.
- `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/validate.sh`
  - Additional stdlib-only rejection of staging references in bin launchers, activation, symlinks and pyvenv.cfg. No legacy entry/auth fallback, network, activation or service action.
- `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs`
  - Four new offline regressions: synthetic CLI stage/final exec+argv+mode+RECORD+activation after stage deletion; unknown/body/link/activation failclosed; validator stale trampoline/activation/link/config negatives; original PPTX wrapping + full-text equality with lost-character/lost-word/reordered/extra/title-only negatives.
  - Tests execute only extracted original stdlib snippets against hand-written fixture files and explicit synthetic interpreter forwarders. NOT a real installation/venv/format proof.
- `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs`
  - Original C1-C4/complete-source/archive/member hashes/final readback/root cleanup retained. Additional stage/target bin equality and zero stale activation assertion.
  - C3 runs actual installed pip direct CLI after relocation/health checks; requires target-local reported location. This is extra launcher evidence, NOT a substitute for real health, complete relocation checks or six formats.
  - PPTX reopens actual Presentation and requires one whole shape's whitespace-reassembled text to equal the whole instruction in strict order, not substring/prefix. Only layout whitespace is normalized; no letters/words are dropped.
  - Independent second commit only pins SOURCE.

No new repository files. Requirements/pins, production helper, execution-adapter, auth/wire/ACL/lock/service behavior unchanged. Final target remains dependent on supplied base interpreter/stdlib/OS ABI and POSIX shell/dirname; no portable/self-contained-Python claim. The zero-stale assertion is specifically launcher/activation/link/config evidence, not a claim that arbitrary compiled debug metadata or host stdlib lives inside artifact.

## Exact local selfcheck, not cloud acceptance
Log `/tmp/ur01-clean138-fix-selfcheck-20261008.log`; SHA256 `ccdb7e486bca6aa4886aaa3c49ae3dd3192f3742f0b83dc99371fe686f89d7c7`.
- On exact13aa/tree107b: bash -n both shell files; node --check existing test+harness; compile both embedded Python blocks under Python3.6 stdlib; PASS.
- Harness --selfcheck:50 static assertions PASS; --describe emitted `/tmp/ur01-clean138-describe-20261008.json`.
- `node --test --test-name-pattern='venv generated|venv publication|venv validator|PPTX semantic|validator artifact import' .../test/runtime-host.test.mjs`:7 PASS,0 FAIL,39 existing tests excluded by selector (reported Node skip; no new skip/test gate).
- `node --test .../test/install-entry-convergence.test.mjs`:6 PASS,0 FAIL,0 SKIP.
- Cumulative parent->candidate diff--check and pin-only diff--check PASS.
- **New payload clean cloud C1/C2/C3/C4: NOT_RUN.** No local real installer/npm/pip/venv/Gradle, no cloud re-run, no services/state/enrollment/Provider. Run138 historical C1/C2 PASS cannot be relabeled as new-tree C1/C2 PASS.
- csh/fish assignment byte rewrite covered; shells not locally invoked or separately declared operationally validated. Actual signed Alinux3 target Python, distribution/launcher integrity and full six real formats remain next main-controlled cloud lane.

## Read-only consumer proposal — NOT IMPLEMENTED / NOT AUTHORIZED
Exact potential source scope only after main freezes: existing `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs` and existing sibling `runtime-host.test.mjs`. No production installer hook, extra copying/mv, new default lane or env command execution.

Proposed interface: `acceptance(env = process.env, { consumeArtifact } = {})`, explicit async callback supplied only by fixed cloud control wrapper. Default absent callback has unchanged cleanup/return behavior. Validate callback type before effects. Invoke at most once ONLY when original C1-C4 all PASS, sourceInventory final tree==fixed payload and archive finalSHA==fixed input, and same canonical target identity/target-local Node blob readback remains valid, after final-source-readback and before finally.

Pass a deeply frozen allowlisted projection:
`{format:'ur01-accepted-clean-target-v1', cloudRun, target, nodeBin, nodeSha256, source:{commit,tree,files,archiveSha256,finalReadbackTree}, harnessSha256, checks:{C1:'PASS',C2:'PASS',C3:'PASS',C4:'PASS'}, acceptedSnapshotSha256}`.
The hash covers stable JSON of the explicitly ordered projection WITHOUT its own hash. This is an **acceptance snapshot digest**, NOT the eventual final receipt-file SHA (finally adds cleanup/endedAt). No tokens, host config, lease state or arbitrary exception/header data. Wrapper persists the exact snapshot outside source/target, binds its later final receipt SHA separately, and treats target as borrowed until callback settles, never retained or republished.

Main-controlled wrapper can on this same target inventory regular-file SHA and precise artifact-internal symlink/link-text/resolve evidence, then write the already-required `<target>/ur04-clean-artifact.json` (inventory excludes its own manifest exactly as existing UR04 reader). Do not mutate payload members, copy dependencies or move/rebase target. Extract a separate exact full-source sibling from same tar and write its `ur04-client-source.json` there, not inside original sourceInventory root. Bind existing UR04 inputs `UR04_ARTIFACT_ROOT=target`, `UR04_NODE_BIN=target/node/bin/node`, exact new `UR04_CLIENT_COMMIT`, separate `UR04_CLIENT_ROOT`, and main-fixed `UR04_API_COMMIT`.

Current UR04 reader remains hard-pinned374; its exact source-pin update is a subsequent UR04-owner checkpoint, NOT done in this UR01 commit. Java/API controls, signed tool provenance, opt-in cloud task and six selectors remain main scope. Callback returns explicit independent consumer result; failure/throw fails overall lane while retaining truthful C1-C4 PASS and independent consumer failure, never recasts install checks. Original finally always cleans the single exclusively-owned root after callback, including consumer state placed under that root; retains only safe receipt/logs. No deferred background consumer, cleanup bypass or persistent artifact acceptance. A same-run hook does not prove a distributable release artifact or production acceptance.

## UR04 completed source handoff links (not reopened)
- `/tmp/ur04-e05-http-handoff-20261008.md` SHA256 `127ddcb3fded202685b22193bef70f663aaa9f209d55d41f95c91e4743de5aa5`
- `/tmp/ur04-e05-http-handoff-20261008.json` SHA256 `5d78d4c2585ff2e98d76506c39934269e4b84d41be861e9e9c48f524fdf73e3a`
- `/tmp/ur04-e05-http-static-selfcheck-20261008.log` SHA256 `d7899c57cea761098bbe15bd0b519e391185de7a76eadd3a778fecd85ae7137e`
UR04 source34d9/tree8d625 checkpoint complete; Java/real cross-end selectors NOT_RUN; no deploy/full acceptance claim.
