# OD01 draft lock-chain review — findings closed; final review pending

Independent read-only architect reviewed the in-progress API worktree, not a committed release candidate. The writer separately reported targeted Agent/Chat compilation passing; successful compilation does not resolve these dynamic SQL and authorization findings. No final OD01 acceptance is implied.

| Finding | Required correction and regression |
| --- | --- |
| Owned conversation mapper accepts `forUpdate` but does not apply a locking SQL clause | Add the locking clause to the exact owned query; prove competing owner/context changes wait and are revalidated. |
| Existing three-argument scoped conversation query references an undeclared `forUpdate` parameter | Restore the existing nonlocking query; put the new locking behavior on the owned method. Execute existing scoped lookup regression against MyBatis. |
| Canonical identity helper returns Agent IDs, while runtime checks compare only runtime preview versus locked runtime binding | Revalidate the locked runtime binding against the currently locked active identity/binding. Reject active identity binding 6 with stale runtime binding 5 even when both runtime reads agree. |
| Task-backed conversation authorizer reads task membership without locking | Discover task ID using an exact nonlocking conversation projection; lock task root/member, then lock/reread conversation and revalidate task ID, owner and target. Do not obtain task-root locks after conversation/output locks. |

The same sole writer owns repairs and focused regression evidence. The architect will recheck the repaired lock chain, including recovered-run origin/source/producer fields and nested helper calls. Final code review remains pending after the candidate commit and tests.

## Independent repair recheck

The architect re-read the repaired working tree and closed all four findings:

- The existing scoped conversation mapper is nonlocking again. The exact owned mapper has its own dynamic locking clause and declared `forUpdate` parameter.
- Task-backed conversations discover the task using an exact nonlocking projection, then lock task/member before conversation. The locked conversation is checked again for scope, owner, target and task identity changes, including null/non-null transitions.
- Both run authorization and capability updates validate the locked runtime binding against the active canonical identity after acquiring binding, identity and runtime locks. The added exact identity recheck introduces no lower-order source/run lock.
- Recovered runs are selected with byte-exact scope/source/producer/origin predicates in the actual locking SQL. Subsequent source/binding/work-item/policy checks introduce no reverse lock. The original runtime remains audit metadata, preserving recovery on a new runtime under the same active binding.

Decision: the reviewed lock-chain blockers are closed and behavioral testing can proceed. This is a working-tree source review, not final OD01 acceptance; actual tests and a committed candidate still require independent final review.
