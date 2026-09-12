# Intermediate policy admission and dispatch checks

Not accepted. Root copied the operator's frozen policy-admission-dispatch-r1-xml-1789245063 archive and original logs/exit files without changing bytes or rerunning tests. archive.json records each file's digest. The three XML reports independently total141 tests,1 failure,0 errors/skips: codec9, transport capture5, AgentServiceImpl127 with1 failure.

The failure is canaryAssignmentUsesDurableInviteWithoutLegacyAgentActionDoubleSend, a Mockito PotentialStubbingProblem. Writer traced it to the old five-argument captureTaskInvites stub after implementation added the sixth trusted workItemIds argument. Repair and a subsequent targeted run are pending; do not report this batch as141 passing or combine its passing subset with another run.

Earlier implementation compile rounds are preserved alongside the test run: policy-guards-compile-r1 failed on a missing entity import; compile-test-r2 failed on missing helper references; compile-test-r3 reached compileTestJava then failed on missing Mockito eq imports. These are compilation diagnostics, not business-test results.

Exact commands and final candidate source association remain due. In particular, this run does not close the separately identified ticket/body runId authorization gap. Four-action adapter rejection and real MySQL coverage, feature-off old-schema bootstrap/CRUD, authenticated creation/dispatch/HTTP and policy1 bypass/funding rollback checks remain pending.
