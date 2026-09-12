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
