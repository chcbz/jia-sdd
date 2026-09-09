# OD01 draft lock-chain review — changes required

Independent read-only architect reviewed the in-progress API worktree, not a committed release candidate. The writer separately reported targeted Agent/Chat compilation passing; successful compilation does not resolve these dynamic SQL and authorization findings. No final OD01 acceptance is implied.

| Finding | Required correction and regression |
| --- | --- |
| Owned conversation mapper accepts `forUpdate` but does not apply a locking SQL clause | Add the locking clause to the exact owned query; prove competing owner/context changes wait and are revalidated. |
| Existing three-argument scoped conversation query references an undeclared `forUpdate` parameter | Restore the existing nonlocking query; put the new locking behavior on the owned method. Execute existing scoped lookup regression against MyBatis. |
| Canonical identity helper returns Agent IDs, while runtime checks compare only runtime preview versus locked runtime binding | Revalidate the locked runtime binding against the currently locked active identity/binding. Reject active identity binding 6 with stale runtime binding 5 even when both runtime reads agree. |
| Task-backed conversation authorizer reads task membership without locking | Discover task ID using an exact nonlocking conversation projection; lock task root/member, then lock/reread conversation and revalidate task ID, owner and target. Do not obtain task-root locks after conversation/output locks. |

The same sole writer owns repairs and focused regression evidence. The architect will recheck the repaired lock chain, including recovered-run origin/source/producer fields and nested helper calls. Final code review remains pending after the candidate commit and tests.
