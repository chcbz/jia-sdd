# Intermediate lease core checks

Progress evidence only; OD07 API is still being implemented. Root copied original operator logs/exit files and one retained XML without rerunning tests or rewriting bytes; archive.json records their hashes. Exact full commands and final source association remain due in the writer's frozen handoff.

- compile-test-java-r1 failed because an existing BarrierWorkItemDao test adapter lacked the newly added bindDispatchedRun method. Writer fixed it; compile-test-java-r2 exit0. Compilation is not business-test coverage.
- lease-targeted-r2 ran six filters:48 tests,20 failures. Writer traced all20 failures to the old AgentWorkItemLeaseServiceImplTest fixture passing an empty task root where the new validation requires exact scope/version. Its original XML was overwritten by the next same-module test; only original stdout/exit remain. Do not reconstruct its XML or count the other suites as independently archived passes.
- lease-core-r3 ran only AgentWorkItemLeaseServiceImplTest after fixture correction:25 tests,0 failures/errors/skips. Root independently parsed the retained original XML; SHA2561a8c9a284b5fc72096771e1ff248cc35663e2acccf5d57fe4251ab29797ea870. The other five suites still require final stable-candidate verification and immediate XML capture.

This does not establish HTTP filter integration, real authenticated creation/dispatch, all policy1 guards, transaction completeness, log redaction, client behavior or release readiness. The API3343342b migration commit is merely an intermediate baseline; tested code includes later uncommitted work and must not be mislabeled as3343342b acceptance.
