# UR06 / original E05 STARTED ACK — readonly source diagnosis

Snapshot: 2026-10-09T01:19:30.406640+08:00. Original Owner, support/source_diagnosis; NOT Writer, Reviewer, business acceptance, or permission to cancel current batch.

## 1. Read rules / immutable inputs

Read `/home/isp/wsps/cyf/AGENTS.md` and `/home/isp/wsps/cyf/ops/orchestration/README.md` at this natural continuation. Read targeted frozen-contract continuation and exact sources, not full historical investigation.
Original WT: `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008`; HEAD `c084fb8f498f335e028af534ee7a570536cbc349` / tree `a4e56538969dddab2f4543d095b9a3a7c3b0af10`; clean `True`. No source/doc/ledger writes. No Gradle, SQL/MySQL, pip/install, runtime HTTP, signals, target reads/imports or production operations. Only this private report is written. No fixture/product repair applied.
Fixed payload C `5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b`; inspect with git show at C, NOT harnessD HEAD. Actual installation C1-C4 and six formats PASS are Main evidence, NOT these private static probes. Main actual prerequisite61/compiles/layering PASS remains distinct from business19.

## 2. Actual evidence, not elapsed-time inference

Main snapshot `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur04-identity0-business-failure/live-readback.json` is `LIVE_READONLY_NOT_FINAL` at `2026-10-09T01:12:50.277593+08:00`, session39096. Actual durable recovery code: `STARTED_ACK_NOT_SENT_IN_FIFO`; state `recovery_required`, ledger RECOVERY_REQUIRED, original child marker absent. Worker frames explicitly at UR04 unknown-selector line156 through waitNode/Child.receipt. Five earlier H2 FAILED markers. MySQL foundation7 and M4six have NOT been entered; all19 final XML unavailable.
At my final log read: observed FAILED markers=5 (NOT final JUnit totals), UR04 XML count=0. Observed methods: e05ActualClientHttpCommitsOriginalResultAndTerminalAck() FAILED, e05TerminalAckLostResponseReplaysPriorWithoutWorkRerun() FAILED, e05SourceAndOriginalResultProofStayFailClosed() FAILED, e05PreparedCommitRefencesAndRollbackIsDurable() FAILED, e05LostResultReadbackSurvivesJavaAndNodeRestart() FAILED. First four summarized LAST_OBSERVED have agent0 pending0/inbox1/ledger1/children0/readyfalse and both siblings readytrue; fifth has pending1. All observed lanes passed actual native-three-registration and matched C/source/archive fingerprints first. Short safe-wrapper stack at line183 is the SafeFailure catch, not evidence of production Java compilation failure.
These facts locate failure BEFORE original lease.read/start, workspace/runCodex child, result storage, D06 terminal/report/restart or MySQL. No OOM/resource/network/Python/identity-DDL causal claim. EOF repair worked (PREPARE completed). The consumer's absent previous temporary Gradle tuning is only an input difference, not proof of resource failure.

## 3. Exact fixed C defect: competing flush consumes target then returns false

`/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/codex-ws-agent/agent-client.mjs` at C:
- `runDrain` ~3370/3413-3433 marks STARTED, enqueues its durable ACK, awaits `startedAck.confirmation`, and refuses all execution if `sent`/marker/dequeued is false. The observed exact code selects the `!startedAck.sent` branch.
- `_emitRuntimeAck` ~3616-3625 sets delivery sent/marker/dequeued only if its target flush returns true.
- `_scheduleRuntimeAckFlush` ~3631-3652 sets local `confirmed = !target`. Every scheduled operation may drain EVERY current pending ACK, not only its target; after FIFO is empty it returns its LOCAL `confirmed`.
- A previously scheduled untargeted replay can drain/dequeue the newly enqueued STARTED while the STARTED-targeted operation is still queued in `runtimeAckTail`. The targeted operation later sees empty FIFO; its local flag remains false even though the original exact STARTED was committed by the earlier operation.
- Actual adapter heartbeat invokes `executor.resume()` ~execution-adapter.mjs128-134; resume invokes processor replayAcks ~agent-client6640-6646. runDrain also replays ACKs and ingress emits ACKs. These are real competing scheduling call sites; no independent second engine is required.

This is a proven SOURCE bug/interleaving, and matches pending0 before-child failures. It is NOT yet a proven exact HTTP status/cause for every actual lane. Main's recoveryReason alone can also arise from real HTTP/protocol failure. Do not mislabel the actual ACK403/400/503 or actual confirmed9 without its receipt.

### Private exact-method static probe (NOT business/HTTP acceptance)

Executed `/usr/bin/node --input-type=module` with precisely extracted two original methods via stdin, memory-only outbox/receipt stand-ins and controlled ACK callback. No original engine/target imports, live service, FS checkpoint, installer, Java, DB or provider. Exit0:

| Schedule | confirmation | persisted/sent/marker/dequeued | simulated callback | pending |
|---|---|---|---|---|
| target only | true | true/true/true/true | 1; ADVANCED STARTED v9 | 0 |
| older untargeted flush then target enqueue in same turn | false | true/false/false/false | 1; ADVANCED STARTED v9 | 0 |
| explicit callback rejection403 | false | true/false/false/false | 1; no receipt | 1 |

This demonstrates the false-negative and retains genuine rejection behavior; it does not mock DAO/auth and claim formal acceptance. The second schedule exactly reaches the observed pre-execution safety branch even though its simulated commit succeeded. No weakening of the STARTED-before-execution oracle is warranted.

## 4. Remaining actual HTTP boundary proof, minimal Main-only readonly request

To prove THIS current lane selected the competing-flush bug, Main can aggregate from already owned private durable files only:
- original commandId/messageId matched booleans;
- runtimeAckCommits values kind/status/deliveryVersion, and contextDigest-equals-original-runtimeCommand boolean (NOT full command/body/token);
- ackReceivedEmitted / ackStartedEmitted booleans;
- pending ACK statuses/sequences and ledger fail-closed code;
- if already safely captured, runtimeAckFailure code + numeric HTTP status.
Actual STARTED ADVANCED9 (seed delivery7 -> RECEIVED8 -> STARTED9), certified marker/dequeue and no pending STARTED would confirm false-negative delivery. If receipt is missing/only RECEIVED8, preserve genuine HTTP/protocol-failure alternative; a safe HTTP observer snapshot is needed before asserting a server code. Never change the live protocol input just for diagnosis.
Current Java fixture already observes safe HTTP category/method/status/version but parent discards HTTP_OBSERVED; snapshots retain them only in Java child until requested. On early recovery parent has no lastServer snapshot, so public LAST_OBSERVED omits HTTP and there is currently NO evidence that lease/result was reached. Node fixture intentionally hides arbitrary recovery text/runtimeAckFailure; no secret/body/raw-exception export should be added.

## 5. Confirmed secondary fixture wait defect, both H2 and MySQL bridge

UR04 unknown-selector line156, and UR06 M4 counterpart line356: `waitNode(s -> children(s,0)==1)` has no known recovery/terminal failure check. Main's actual stack + durable recovery + no child verifies the current sixth selector cannot progress normally. This is not old PREPARE EOF deadlock. No elapsed deadline/automatic kill required or authorized.
Other five paths use `awaitRealHeartbeat`, which checks recovery/FAILED/REJECTED BEFORE child. Apply the equivalent negative-state guard to THIS pre-child wait only when newly authorized; preserve its later positive unknown-STARTED-after-restart assertions, original children==1, no rerun, sibling readiness and revoke isolation. A fail-fast assertion on a proven non-executable state strengthens, not weakens, the oracle.

## 6. Minimum prospective repair scope — PROPOSED, not authorized by readonly message

API base `c084fb8f498f335e028af534ee7a570536cbc349` / tree `a4e56538969dddab2f4543d095b9a3a7c3b0af10` in original clean WT:
1. `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java`
2. `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java`
Only pre-child unknown-selector wait gets a known failure-state guard; original full6+7+6 methods/assertions and cleanup remain. Optionally capture existing safe serverSnapshot on an early failure while keeping the original error primary, without touching service behavior; Main must explicitly freeze any diagnostic addition. No SQL/runtime production path needed for this fix.

Client original Knuth scope (new exact clean fixed candidate must be selected by Main, preserving other ongoing work; tested payload source is C, not D):
3. `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/codex-ws-agent/agent-client.mjs`
4. `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/codex-ws-agent/test/agent-client.test.mjs`
Repair exact-target completion shared across serialized flushes: register original immutable queued-record completion before scheduling, let ANY flush resolve it only after exact FIFO commitRuntimeDelivery/ledger marker/dequeue succeeds. The queued target's confirmation must observe THAT certified completion, not which flush happened to consume it. Do NOT infer success from empty queue/ready/latest unrelated receipt, remove STARTED gate, resend business, or hold FS/DB lock over HTTP. Any implementation must preserve record identity/digest/full subject and true negative statuses, fail-closed unknown response, no duplicate execution/replay side effects. A concrete implementation belongs to original client Owner, not this readonly API diagnosis.

Regression requirements in existing client test file: deterministic older-untargeted replay consuming STARTED; repeated heartbeat/replay competition while ACK callback suspended; original matching HTTP commit before exactly-once execution; wrong identity/status/version cannot confirm/dequeue; true403/unknown response retain recovery/no execution; independent restart never reruns unknown STARTED. Existing tests at ~3716 (before side effects),3735(wrong result),3746(unknown STARTED) and existing E05 real Node-fetch ~4247 retained, plus checkpoint/runtime-host suites. No production auth constructor/open permission shortcut.

If C product source changes, new payload commit/tree/full285 blob modes/archive bytes/SHA must be independently accepted and four existing API paired-proof files repinned separately after freeze; no C/A/7594 dual source, no reuse of currently installed target. Current report does not authorize source proof changes or installs.

Official selectors to retain: original mapper5/service48/controller8=61; BOTH UR04+UR06 source compile; ROOTvalidateLayering; original H2 six / UR06 foundation seven / ur06M4MysqlE05 exact six after NEW isolated C1-C4/fullformats + same accepted target callback. Their actual business results are currently NOT_PASS/NOT_RUN as noted above. Main alone controls new39096 cancellation authorization, fixedsource execution and ledger; old92814 cancellation does not grant control over new39096.

## 7. Evidence SHA / handoff boundary

- `/home/isp/wsps/cyf/AGENTS.md` — `6a4b84a551b650d4b82b0a0a6d0fbd3f03a0faa737147e30547005a04b75a510`
- `/home/isp/wsps/cyf/ops/orchestration/README.md` — `3f1f55de860356650f83f8f64f3808d3fa06eedd6ab3dda8d690df7ec68ad388`
- `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur04-identity0-business-failure/live-readback.json` — `ce4e3ef5bb7f170f2d45540555887f3bd8bcef04ff597d82028a6ba22cb541c6`
- `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur04-identity0-business-failure/owned-test-worker-thread-dump.txt` — `f244897d833d999bba757f29e90c877ff322d1f9950f0ee6c1d4b412cba3de42`
- `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur06-identity0-prereqs/main-readback.json` — `a740a9c574484af26db84692a27838bdf66b24ee85f513b1397757d90bd0ea31`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java` — `31b014b70c06604515e40a9f62aedeca54197eb4e84047ea799a5e7c44a0802d`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpFixture.java` — `5f33c08c6ef1aad9c6f1bb8c1781460268c765a42e526f06f96f40bc5cefbd4f`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs` — `c00c1f6f6460c7d34b8d541dee6d3910d731900ac3c5f2d6b31d484ccbe9486b`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java` — `9f5d59505e221359f244471f0fc753630fb0c62c1902f344781cd105d009a5ac`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandAckServiceImpl.java` — `f05c0d3c248e2b50c30e924ea31035d6b7512de1f1c20e69fa81dd55698ba856`
- `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentRuntimeV1ServiceImpl.java` — `c995636bdeac8d150bf6b75f2adf57a484388d5d30d20d38df1c75267f4eec1b`
- Mutable log snapshot `/var/tmp/cyf-ur04-identity0-local-20261009T005126/e05-gradle-sanitized.log`: bytes=18947; SHA256=`baf57175bf827630cf1f252b327a5b7fb9991725814b8f0b9ad80508860dd733`.
- Fixed C git blob `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008` / `conf/codex-ws-agent/agent-client.mjs` @ `5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b`: SHA256=`d7f7cdd5731d712be2e3760ece466de8a855c89240222410de386468c1c762ab`.
- Exactly extracted `_emitRuntimeAck` + `_scheduleRuntimeAckFlush` methods SHA256=`1cdbe97c2c40492c7d8449791d6a6b69bf4fb6ffbb4dcc7f3ab5226e4be35750`.

No source candidate commit produced in this diagnosis. Existing c084/a4e565 source remains clean. This is a source defect + explicit missing live proof + minimal scope handoff, not overall UR06 completion or production release.

## 8. Main subsequent actual durable aggregation (chat handoff; not new file proof)

After initial report snapshot Main reported for the same current agent0:
`ackReceivedEmitted=true`, `ackStartedEmitted=true`, ledger `RECOVERY_REQUIRED`; the one message's latest `runtimeAckCommits` is `{kind:ADVANCED,status:REJECTED,deliveryVersion:10,contextDigest:71d...}`. No credential exported. Latest receipt is overwritten per message, so it is expected NOT to retain intermediate STARTED9; do not demand an archived9 receipt that the original design does not store.

Targeted fixed C source read confirmed:
- `_newEntry` initializes ackStartedEmitted=false; `markAckEmitted` is its setter.
- Native `replayAcks()` always uses `_scheduleRuntimeAckFlush`; `_emitAck` native branch always uses `_emitRuntimeAck`. The legacy synchronous drain setter is not this Runtime lane.
- In Runtime path `commitRuntimeDelivery` calls `ledger.markRuntimeAckCommitted` (exact original runtimeCommand digest + monotonic status/version) BEFORE `markAckEmitted` BEFORE dequeue. Thus actual ackStartedEmitted=true means the original native STARTED matching receipt was durably validated at least once; a blanket 'STARTED HTTP never sent' explanation is inconsistent with it.
- Original server D06 from SENT7 goes RECEIVED8/STARTED9/REJECTED10. Two prior emitted markers + latest matching ADVANCED REJECTED10 support that the client falsely moved a genuinely acknowledged original command to recovery then emitted REJECTED; REJECTED is allowed from STARTED by original state machine. Do NOT alter D06 to hide this client false-negative.

**Attribution precision:** the source race is reproduced deterministically, and actual markers substantially strengthen it as the leading cause. Native commit validation/mark succeeded is confirmed from Main's aggregation; exact live scheduling interleaving is not captured. A storage/marker/dequeue error after validated STARTED (followed by later FIFO recovery) is still a narrower alternative, since mark precedes dequeue and the latest receipt overwrites the prior. No actual send-exception/status/context-error code has been supplied. Report this distinction rather than claiming all live lanes proven solely by a static probe. No generic target-absence=success repair is acceptable.

Minimum repair proposal remains client original engine+existing agent-client tests (Knuth original Runtime Owner), API original two Java pre-child waits (API Owner after explicit freeze). Current3identity-file authorization does NOT authorize these paths or C. No source edit or new-source/install happened. Original6+7+6 remain intact; main actual19 still not final and MySQL groups NOT_RUN.
