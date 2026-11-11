# Final API combined noDB R2 failure stop — 2026-09-06

Actual immutable input: API1b3c7d0435d701c811716b8913bc824fb8934dec/treecac8d686384b553f92a514e45bec95c71e6fe4ff; wrapper SHA498eb56d43288ee79b2222da75c9ad8d6f87947b101520b006e1e837180f2dc7. Session91255 naturally exited1 at15:30:52+08:00. Verifier confirmed wrapper1555175 and its daemon1555501 are terminated, no new session was launched, and source remained clean. No process was signalled by ECO control.

Read-only evidence, explicitly handed off by Hopper to ECO main and Critical Turing only: `/var/tmp/eco-api-r2-nodb-CpS7Ig`. LogSHA d533908e05d7d9b879d54ff0dfb068387a995314c09969c32ca45ff9785d6088; fixtureSHA9d9de6da88d2170758515b47f66929586af324708487a433a6acdc4ec4753c12. The directory contains cache.json, fixture.txt and gradle.log; do not infer that other daemon/build artifact directories were also shared. Verifier separately reported daemon-log SHA84b5660a1a6a46bbf1fdf0c4207b40510984bd96ab70fc92654f4ddda7dae934, without expanding this read permission.

## Evidence and stop matrix

| Item | Observed fact | Root cause status / next action |
| --- | --- | --- |
| Prior W09 failure | MySQL fixture lifecycle/source review rejection; corrected source independently accepted | Historical failure retained; not a failed MySQL execution. |
| Current service tests | 25 distinct FAILED console markers in agent-service before daemon loss | A failure count from console, **not** final XML totals. Investigate exact failed method/source locations. |
| H2 cluster | BadSqlGrammarException / JdbcSQLSyntaxErrorException in funded legacy guards, W04 real transactions, W05 quote/claim initialization, W06 settlement initialization | Exact SQL/message is absent from preserved default Gradle log; source-based cause must be labelled inference until corroborated. Do not automatically blame production SQL or call all fixtures fixed. |
| Separate NPE | FundedBountyQuoteClaimServiceTest.parallelClaimsHaveAtMostOneWinner, line264 | Inspect precise source/mock setup; no NPE message retained. |
| Separate race assertion | FundedBountyServiceRealTransactionTest.actualCreateHeldBeforeCommitRacesLegacyPrecheckAndRootReservationThenLockedGuardRejects, line378 | Inspect whether earlier SQL failure prevents expected synchronization; do not remove/weaken concurrency assertion. |
| Daemon disappearance | After reported test failures Gradle daemon disappeared; wrapper returned1 | Termination source un-attributed. Do not claim OOM, signal actor or test-root-cause equivalence without evidence. |
| Missing results | No finalized XML; partial binary artifacts reported by verifier | No XML pass/fail/skip totals asserted. Chat/economy/OAuth downstream selected scopes were not reached. No new accepted runtime evidence. |

W09 hit its second consecutive failure and is stopped at blocked_root_cause. R03 Critical support is admitted read-only for a bounded diagnosis/remediation proposal; it must not run Gradle/tests, change source, operate daemons or create DBs. Complete the root matrix and authorize an exact path-owned correction before any new-tree execution. Never rerun the unchanged failed wrapper/tree blindly. Retain prior accepted W03/W07/W10 scoped evidence and the old W06 mapper2 PASS separately; none turns this run into a PASS.

Frontend source progress is independent: final48c79fab/b76b5f50 is source-integration accepted; its separately admitted focused Node verification does not clear this API failure or authorize release/charging.

## Bounded source diagnosis and correction authorization matrix

Critical Turing read-only findings (no probe/test executed):

- **High-confidence inference, not retained SQL text:** 23 SQL-class failures first traverse unary MySQL `BINARY expr` predicates in AgentTaskFundingMapper. W05 setup already reached funding.create at171, so a prior DDL-tail hypothesis is not the observed first failure. Related quote and settlement mappers contain the same dialect pattern. Replace only unary BINARY with the project's existing `CAST(expr AS BINARY)` form in these three mappers; preserve ordinary equality, OCTET_LENGTH fences, scope predicates, parameters, locks and ordering. Independent review must verify unchanged MySQL byte-exact identity semantics and H2 compatibility; do not weaken scope comparison just to pass H2.
- **Source-determined Mockito setup defect:** FundedBountyQuoteClaimServiceTest.parallelClaimsHaveAtMostOneWinner re-stubs an existing Answer with when(...), invoking the prior Answer using null matcher callback. Use doAnswer(...).when(...) in that method only. Keep concurrency behavior and assertions.
- **High-confidence downstream inference:** the W04 race assertion is its10s latch helper, likely never reached because the creator fails in funding SQL first. Do not extend timeouts or weaken race assertions. Re-evaluate its exact method only after the SQL issue is closed.
- Daemon termination remains UNKNOWN_INFRA, with no evidence authorizing an OOM attribution or process operation.

Sole Critical Turing may make a new clean commit on the existing final API release worktree `.worktrees/eco-v0-api-release-r1`, preserving1b3c7d04 as immutable parent (no reset/rebase/amend). Source paths are only `agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/{AgentTaskFundingMapper,AgentTaskBountyQuoteMapper,AgentTaskSettlementMapper}.java` and `agent/jia-agent-service/src/test/java/cn/jia/agent/service/funding/FundedBountyQuoteClaimServiceTest.java` (verify exact tracked package path before editing; no broader test file allowance). Preserve all other source bytes, existing build directories and partial results. This reuses compilation outputs instead of paying another full worktree compilation cost; it is **not** reuse of failed test results as PASS.

The previous verifier must separately archive its exact partial test-result artifacts before any later Gradle invocation. Source editing does not authorize touching those artifacts. No Gradle/DB/tests/build/dependency/runtime operations are authorized by this correction. Independent SQL/delta review and diagnostic-output archival must precede new execution; reuse all unaffected previously accepted scopes, select only actual failures plus previously unreached/missing scopes, and obtain the next heavy-resource window after Web finishes.

## Independent delta review receipt (2026-09-06)

Sol Leibniz01a074ac-4236-71b1-850f-75cc9a05b01f accepted exact3a0f05f40df3a0c6235536584700affeb3747561/tree479e9eed26f1ad6d486f3516326603f09263ed76, clean parent1b3c, four authorized paths. P0/P1/P2=0/0/0 SOURCE/test-design ACCEPT only. Both operands use binary cast; equality/OCTET_LENGTH, scope/identity/version/lock/order preserved. Existing AgentTaskMeta/Workspace mapper and H2 identity fixture provide local contract precedent. Mockito doAnswer preserves rootLock, actual LockedTaskMutation, common start latch, Future exception propagation and exact one winner. No tests/DB/Gradle executed; SQL dynamic confirmation and daemon UNKNOWN_INFRA remain pending. Reviewer released after recording; next verifier must use a new exact wrapper, preserve archived old partials and emit full immediate test exception output.

## R3 runtime start and current observation (17:17 +08:00)

Newexact3a0f05/479e9 wrapper `/var/tmp/cyf-eco-control-api-r3/run-api-r3-bounded-nodb.sh` SHA7a20dadebeb8bd42401498f310dc86b4acdffa0bcb4fbde7cf8cab30abb5fb37; diagnosticinit SHAe95d642b366e2873ef0e6a78eb731154136779e8f36dd20986bf050f91dc70c5; fixture3167c540e7047cc31bad85dccf3257f717194fe2a8acc51ab6db8d086cf0c4e5. Main admitted once after independent review, sealed prior partials, Voice window handoff and lock check. Actual session3658 started16:53:54; orchestrator1638974 acquired lock. Owner Hopper explicitly shared `/var/tmp/eco-api-r3-nodb-HYa2No` read-only with ECO main (not other directories). At17:17 the log had reached agent-service:compileTestJava, no newFAILED marker observed; **still in progress, no final XML/PASS claim**. Verifier continues polling the same session, no rerun.

Voice/monitor controllers separately reported canonical API stopped/10018 absent/public502 at17:06, causeUNKNOWN. Do not attribute it to Gradle or OOM without evidence. ECO emitted conflict-alert, leaves all service/process/capacity remediation to exact owners, and holds new Web Node/Vite admission until this run naturally ends and recovery-resource coordination is resolved. The ongoing owned run is not preempted.
