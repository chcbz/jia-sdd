# Intermediate bypass guard checks

Failed batch: nine XML suites independently total114 tests,3 failures,0 errors/skips. Root copied the operator's frozen policy-bypass-guards-r1-xml-1789246225 reports and original stdout/exit byte-for-byte; archive.json contains hashes. No rerun or report rewriting occurred. Source association and exact invocation remain due in the frozen handoff.

Failures requiring diagnosis/repair:

- FundedBountyServiceReplayTest expected FUNDED_BOUNTY_CONFLICT but received FUNDED_TASK_CONFLICT.
- AgentLegacyTaskCompatibilityEventTest expected AgentTaskStateException but received AgentTaskCollaborationException.
- AgentTaskStateServiceImplTest.scopeMissIsNotFoundWithoutLeakingOrWritingAcrossScope expected NOT_FOUND but received INVALID_PERSISTED_STATE.

These differences are not automatically harmless fixture problems. Preserve intended scoped not-found behavior and verify rejected requests do not mutate task, funding or events. The whole run remains failed until the affected cases are repaired and verified.

The separately reported adapter suite is5/5 in this batch, including inactiveLeaseOmitsTokenAndExpiryInsteadOfSerializingNulls. Root read the observed test: a release response has ready status, string version and omits both optional token/expiry fields. This establishes the scoped null-omission repair, not a full HTTP/OpenAPI lifecycle or database result. Do not add its count to the previous overlapping adapter run. New actual-MySQL feature-off/entry/cross-run/bypass proofs and independent candidate review still remain due.
