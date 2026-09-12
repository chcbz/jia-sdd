# Integration baseline watch — 2026-09-12

Read-only observation; no original checkout or gitlink changed.

| Repository | Concurrent original checkout | Feature baseline / implication |
| --- | --- | --- |
| API | `a9d3e7417447a9f5f59a12523e582a8e8f1818f6`, `codex/hall-question-history` | Merge base with OD03 is `492adc7e8ff386013264c4eef4c0bf67adf34add`; history ACL, recipient checks and other commits must be reconciled before integrated pins. Do not switch the active original checkout. |
| Web | `b31565f8741fdc6f986763dd86442a2c2a4345b0`, `codex/hall-question-history` | Descends from output baseline `77666e8f`; conversation history/deletion overlaps Hall wiring. At OD05 select the accepted integration baseline, preserving the other feature. |
| Client | clean `master` at `f8c731d0cef38956bb3dabaa628c6188c0040bed` | Three commits after original output baseline; session fixes overlap OD04. Refresh the still-clean client feature baseline at OD04 start as described in its preparation. |

Observed branch tips are not themselves release approval. OD06 must integrate the selected accepted API/Web changes in dedicated worktrees, test affected behavior, and record actual candidate commits. Feature-only pins must not silently roll back concurrent accepted changes.

## Dry merge forecast

`git merge-tree --write-tree --name-only --no-messages 683e8007 a9d3e741` in the API worktree returned 1 and reported 10 textual conflicts. It created only an unreferenced Git tree for analysis; no branch, index or working file was changed. Conflict locations: AgentRuntimeMapper, AgentCommandCanonicalCodec, AgentLegacyTaskCompatibilityService, AgentServiceImpl and its test; chat mapper/service build.gradle; ChatConversationMapper; AgentWebSocketHandler; JuyitingAgentRelayService.

These are overlapping runtime/session and exact conversation authorization seams. OD06 needs explicit combined behavior and relevant dispatch/session/ACL regression, not choosing one side wholesale. The forecast uses the frozen OD03 candidate and the observed concurrent branch, not the final reviewed integration candidates.

## Dedicated root pinning boundary

`output-root/api` and `output-root/web` are uninitialized gitlink directories while implementation uses sibling worktrees. Do not run `sddw pin` there yet: `git -C api rev-parse HEAD` can walk upward to the root repository and yield the wrong SHA. At OD06, after accepted integration candidates are selected/pushed, create detached API/Web worktrees at those empty gitlink paths from the existing repositories (no source copies or new node_modules required for pinning). Verify each `--show-toplevel` and HEAD before running pin/verify and staging the gitlinks. Existing implementation worktrees and shared original checkouts stay intact.

Disk observation during OD04 preparation: root filesystem had about 2.1 GiB free; API worktree about72 MiB, client2.2 MiB, Web484 MiB including installed node_modules. These are planning observations, not a reason to remove user caches or unrelated files.

## Build provenance recheck — 2026-09-12 09:52 UTC

Read-only SDK queries using the aliyun-pipeline skill found backend pipeline5260799 (`cyf-api-kit-ci`) now has develop-push source and automatic deployment; run20 was RUNNING and the API source commit was unknown. Do not push develop/master as an incidental build step. Separate5263690 (`cyf-api-kit-develop-ci`) currently has no detected deployment step. Neither was triggered, retried or edited by this work. Historical5260799/run18 SUCCESS useda8489561586400af049eee625d90b6e98e834f04 and is not output candidate validation.

Concurrent APIa9d3e741 includes committed `ops/ci/aliyun-flow/cold-init.gradle` fromf24d3fc0. It builds the settings plugin from a source-relative path and requires the original org.opencv:opencv:4.5.5 JAR (722802 bytes; SHA256323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4) from its fixed packages.aliyun.com repository. Preserve the provenance verification and starter public-artifact verifier. The earlier public replacement probe does not override this accepted path.

Initial substring inspection found cold-init.gradle/bootJar but did not locate credential variable names, origin, coordinates or OpenCV hash. That did not prove a different init or missing credentials; the generic inline-shell-write heuristic was inconclusive. Exact source/configuration was subsequently checked below. Flow YAML SHA256984e26604ee34f93364aaa4f28480ecc8dac2a1990285144fd03098c2e87094e; candidate-specific build evidence remains required.

Local .m2 credentials are associated with repo.rdc.aliyun.com; required CYF_MAVEN environment names were absent. Unauthenticated HEAD to the pinned packages.aliyun.com OpenCV JAR returned401. No credentials were forwarded to a different host. No raw Flow YAML, credential file, signed URL or secret-bearing log was archived.

## R2 policy compatibility seam in the concurrent baseline

Original design baseline had no funded-bounty backend; a9d3e741 now contains `FundedBountyQuoteClaimServiceImpl`, `FundedBountySettlementServiceImpl`, `PersistedFundedBountyLegacyGuard` and the economy modules. These must survive OD06 integration. Financial settlement remains outside this output feature; source presence does not authorize new settlement behavior.

OD07's all-entry policy1 protection must explicitly inspect `POST /agent/tasks/{taskId}/funding/complete`: the current settlement service accepts assigned/running tasks, captures funds, then directly calls tasks.updateStatusByVersion(COMPLETED) without a delivery policy/pin check. Also inspect funded quote/claim, which invokes assignResolvedVersioned and dispatches task invites. Preserve policy0 funded behavior, while rejecting any unsupported policy1/funded combination before financial writes, or applying the reviewed formal-delivery invariant if such combination is explicitly designed later. Merely guarding the old AgentService/WS entrypoints would miss these newly integrated routes. Add negative transaction evidence with no status/fund/event mutation for rejected combinations.

## Confirmed build-only Flow prerequisites — 2026-09-12 10:33 UTC

Read-only SDK inspection confirms5263690 calls the tracked `ops/ci/aliyun-flow/cold-init.gradle` with `./gradlew` and a git rev-parse source guard. Its referenced variable group44254 (`cyf-flow-ci-maven-auth-5256653`) exposes names CYF_MAVEN_USERNAME and CYF_MAVEN_PASSWORD, both marked encrypted. No variable values were accessed by probe logic, printed, persisted, or forwarded to another host. This confirms required variable configuration, not present credential validity or output candidate build success.

The current pipeline has20 existing test filters and no output tests; record actual scoped coverage rather than claiming output regressions from its default suite. Keep local reviewed output tests and execute a candidate-specific canonical package check through a safely selected feature source. No pipeline trigger, retry, edit or push was performed during preparation. The flow text contains no local Gradle lock path; all Gradle commands executed on this host must still hold /tmp/cyf-gradle.lock.

The5263690 script's source guard is exactly `test "$(git rev-parse HEAD)" = "$CI_COMMIT_SHA"`; it sets CYF_FLOW_GRADLE_ACTIVE=1 and a fresh workspace-local CYF_FLOW_BUILD_ROOT, invokes `./gradlew --no-daemon --stacktrace --console=plain --init-script ops/ci/aliyun-flow/cold-init.gradle ... :starter:bootJar`, and checks exactly one resulting bootJar. This validates checkout against platform metadata; root must additionally compare that metadata to the reviewed output candidate when selecting a feature-source run. The script's20 existing targeted tests do not include the output suite.

## Additional original API push trigger — 2026-09-12 10:48–10:56 UTC

Read-only checks of legacy API pipeline1466118 found giteeGit source https://gitee.com/chcbz/jia.git, configured branchmaster, events[push], triggerFilter.*, isBranchMode=false and a nonempty webhook/service connection. The raw API omits isTrigger (confirmed independently of SDK mapping), so absence must not be treated as disabled. Latest listed run167 SUCCESS started1782056719000; historical inactivity does not establish that a feature push is safe. The public GetPipeline API documentation describes triggerFilter only as a trigger filter and does not resolve this combination's effective branch semantics.

Root must resolve the original pipeline's effective feature-branch trigger behavior before any remote API push, even though newer5260799/5263690 are develop-scoped. Do not edit/disable the legacy trigger or start a potentially deploying run incidentally. Continue local implementation/review while this read-only preparation is open. No push or pipeline mutation has occurred.

Read-only Gitee hook inspection using the repository's existing credential helper (credential material kept in memory and used only at gitee.com) found exactly one push hook2096597. Its callback SHA2569ca0d748ff2f2c1f716dc63bb02bb7465523e970876b630c7782b6efb9aa6895 exactly matches pipeline1466118;5260799 has a different callback hash and5263690 has no callback. Thus newer pipeline configuration alone does not describe effective repository push wiring. The hook's last HTTP result is200 with successful=false, errorCode1400003 and the diagnostic “触发失败，代码路径或者代码分支未匹配”; callback URLs/passwords/credential values were not exported. The last delivery's input branch and time are not available in this response, so this historical rejection is not a controlled feature-push validation. No hook was tested, edited, added, removed or triggered.

## Follow-up boundary check — 2026-09-12 11:07–11:12 UTC

Legacy1466118/run167 resolves to master commit982259abfe333439c062f46d047e1e04276d7cdc with a successful deployment job455433046/deployOrder64335028. This confirms the pipeline can deploy but says nothing about a future feature push. Top-level pipeline/config metadata and parsed settings contain no additional observed trigger-disable flag; settings describe cache/concurrency controls. The effective feature-branch trigger remains unresolved. No push, trigger, hook mutation or credential forwarding occurred. Continue local candidate review and isolated live verification; do not hold those independent steps idle for remote packaging.

Integrated compilation initially failed on four obsolete requireId calls in ChatConversationDaoImpl. The sole writer repaired them to the existing requireIdentity helper. Root observed compile-r2 exit0 and BUILD SUCCESSFUL (83 tasks) in /tmp/od06-api-integration-compile-r2.log, while preserving compile-r1 failure evidence. Agent targeted-r1 likewise exited0; candidate/source correspondence and full scope belong to the writer's frozen handoff and independent review. These development-dependency checks do not establish canonical packaging or live R1 acceptance.

## Local canonical-access probe — 2026-09-12 11:19 UTC

To avoid coupling local canonical packaging to an unresolved production push trigger, root read the two configured consumer values from the same project's Flow variable group44254 into memory and attempted one HTTPS GET against the fixed original OpenCV4.5.5 path on packages.aliyun.com:443. The response was403; no redirect was followed, no artifact was accepted, no values were logged/persisted, and the old settings.xml origin's credentials were not forwarded. This records an unsuccessful access attempt, not a diagnosis of credential validity, masking/encryption semantics, repository availability or network policy. See canonical-original-dependency-probe.json. No remote push/pipeline/hook mutation occurred. Local development-dependency live verification remains the next independent step; canonical package acceptance remains open.

## Concrete R2 entrypoint handoff

The integrated AgentController.createTask retains a nonfunded path: requests without grossBountyAmountMicro, settlementPolicy and requiredSkillRequirements call agentService.createTask. Presence of any of those fields (including a nonnull empty requirements list) selects FundedBountyService.create. OD07 must reject unsupported policy1/funding combinations at service level before financial writes, and OD10 must send the intended contract rather than accidentally selecting the funding path.

Exact current source locations: agent/jia-agent-service/src/main/java/cn/jia/agent/api/funding/AgentBountySettlementController.java exposes the /funding/complete route; service/funding/FundedBountySettlementServiceImpl.java directly calls tasks.updateStatusByVersion after capture; service/funding/FundedBountyQuoteClaimServiceImpl.java invokes assignmentService.assignResolvedVersioned. Also inspect service/funding/FundedBountyServiceImpl.java for funded creation/cancellation and PersistedFundedBountyLegacyGuard.java for the inverse legacy guard. These are integration seam notes for the existing OD07 all-entry gate, not authorization to expand deferred financial integration.
