# UR01 current Python3.11 cfg audit source handoff — 2026-10-08

## Immutable two-commit binding
Payload C: 5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b / tree d3cdc69da62bddc48af0bc86b4f32dbfa9429b60 / parent B 2533381cc79e79d124d8c8630914790f48d3619e. ONLY install.sh.
Standalone harness D: f3ec220d8ea20d25379f47ba61fe22cffb62a28e / tree 2a4da5e4d791bfddf79fe76586d52b9bf8f6d051 / parent C. ONLY runtime-host.test.mjs + clean-target-install.acceptance.mjs. SOURCE uniquely C; D is never payload; no A dual contract.
Archive: 285 tracked regular files, 3635200 bytes, SHA256 9b5d74b27a91579359ad0a18d241f66f19d6df13d376e3cff5dbd45b729b7687, PAX comment=C; complete blob/mode and all Git tree directories PASS. Private proof: /var/tmp/ur01-py311-cfg-fix-source-20261008/payload-C-source-proof.json.
Branch task-only push/readback MATCH, WT clean; no develop/Flow/production operations.

## Exact fix and preserved boundaries
Recognize only cfg command audit final operand for absolute-interpreter -m venv --copies [--without-pip]. Map EXACT stage venv to final venv as raw CPython audit text or one POSIX-quoted operand, not arbitrary replace/strip/execute. Preserve every other cfg byte, home/executable/include-system-site-packages=false, CRLF/no final newline and original mode. Reject unknown/extra command args, foreign stage, duplicate command, stale home/base/body and cfg symlink BEFORE rewriting launchers. Original launcher/trampoline/RECORD/activation behavior retained; validate.sh and six pins exact baseline bytes.

## Owner low-cost evidence (not actual installation)
17 scoped Node PASS, 0 FAIL, 42 selector-excluded out of59 declared. Includes three new cfg test methods (4 raw/POSIX+copies/without-pip handwritten positive variants,11 failure kinds, strict stale reintroduction), prior generated CLI/argv/modes/RECORD, PPTX strict lost/reordered/extra-text, source bindings/local schema and awaited consumer/cleanup/tamper. 74 standalone harness static assertions PASS. bash/Node syntax, exact stdlib snippet AST, cumulative three-path diff-check PASS. Four earlier handwritten cfg/mode+strict validator probes PASS. No real venv/npm/pip/install/import/ABI/Java/MySQL/Provider invoked by Owner.
Preserved first scoped failure: 11pass/6fail/42excluded, all six consumer failures were old archive byte-size literal3624960; final D asserts actual3635200 while retaining complete source/blob/mode/hash checks. No business/installation failure relabelled.

## Main independent actual stdlib supplement / unresolved gap
Main evidence: /home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur01-py311-cfg-source-readback/actual-stdlib-cfg-readback.json.
Actual current3.11 --copies --without-pip simple private-path C relocator + ORIGINAL validator EXIT0, cfgOnlyExactOperandChanged. Single-quote long-parent cfg ALSO changed exactly, but original activation3 scripts include POSIX-quoted stage where raw-stage substring is broken by quoting; old bin filter skips them and ORIGINAL validator correctly exits1. Both roots removed; no packages/actual install. This is NOT C1 install failure/cfg repair failure. Our handcrafted quoted-cfg/activation templates are NOT proof actual current3.11 quoted-venv success. Gap is outside cfg-only scope and remains unresolved; no production helper/pin/validator/activation broadening.

## Remaining / next receiver
Main: independently bind C payload and D harness, have API original Owner update paired C proofs, then NEW normal canonical nonquoted-parent full C1-C4/six-format/import/ABI + one awaited same-target E05 consumer and finally cleanup. All new real checks/consumer6/trueMySQL7+M4 and full release/maintenance/production NOT_RUN. Old13826 C1FAIL/consumer0/rootremoved remains original evidence; its cfg bytes were NOT retained, never substitute the independent probe.
UR05: unchanged paused three-file WIP/checkpoint at /var/tmp/ur05-root-admission-wip-interruption-20261008.json; producer ba88/frozen proposal preserved. Main receives this source stage and reclaims original sole Owner to root-admission WIP; no second Writer/Reviewer and not Goal completed. Last private UR05 units54=53PASS/1pending code-oracle update; no admission commit/push/actual batch.

Exact three source hashes and every log/hash/remote receipt: /var/tmp/ur01-py311-cfg-fix-source-20261008/handoff.json.
