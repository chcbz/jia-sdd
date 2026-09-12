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

The current5263690 flow mentions cold-init.gradle/bootJar and generates inline configuration, but does not contain the tracked init's credential variable names, origin, coordinates or OpenCV hash; matching the basename alone does not establish equivalence. Flow YAML SHA256984e26604ee34f93364aaa4f28480ecc8dac2a1990285144fd03098c2e87094e. Exact source/configuration and candidate-specific build evidence remain required.

Local .m2 credentials are associated with repo.rdc.aliyun.com; required CYF_MAVEN environment names were absent. Unauthenticated HEAD to the pinned packages.aliyun.com OpenCV JAR returned401. No credentials were forwarded to a different host. No raw Flow YAML, credential file, signed URL or secret-bearing log was archived.

## R2 policy compatibility seam in the concurrent baseline

Original design baseline had no funded-bounty backend; a9d3e741 now contains `FundedBountyQuoteClaimServiceImpl`, `FundedBountySettlementServiceImpl`, `PersistedFundedBountyLegacyGuard` and the economy modules. These must survive OD06 integration. Financial settlement remains outside this output feature; source presence does not authorize new settlement behavior.

OD07's all-entry policy1 protection must explicitly inspect `POST /agent/tasks/{taskId}/funding/complete`: the current settlement service accepts assigned/running tasks, captures funds, then directly calls tasks.updateStatusByVersion(COMPLETED) without a delivery policy/pin check. Also inspect funded quote/claim, which invokes assignResolvedVersioned and dispatches task invites. Preserve policy0 funded behavior, while rejecting any unsupported policy1/funded combination before financial writes, or applying the reviewed formal-delivery invariant if such combination is explicitly designed later. Merely guarding the old AgentService/WS entrypoints would miss these newly integrated routes. Add negative transaction evidence with no status/fund/event mutation for rejected combinations.
