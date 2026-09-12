# OD03 repair evidence

Candidate `4c292cc35e4d82a23620a85296b721569ff59bd5`, parent `683e8007`; eight changed files. The sole writer fixed R01–R03 and froze a clean worktree.

Corrected single Gradle invocation (`command.txt`) exited 0: **27 tests, 0 failures/errors/skips**, six suites. Root inspected the archived XML and verified all eight changed source hashes against both pre/post execution manifests and candidate Git blobs. Source/report correspondence check passed. Runtime dependency substitutions remain as documented under OD00.

The initial invocation placed test filters after all task names; it was interrupted with exit 130 before test execution according to the writer. Its command/exit are preserved separately and do not contribute to passing evidence. The corrected invocation binds filters to each module task and completed in 5m30s. No unnecessary full-module run is claimed.

`validateLayering` exited 0 (1m46s); command and exit are archived. Original logs stay in `/tmp/cyf-od03-evidence/review-repair-tests`; report copies omit captured logs/properties and retain original hashes. No deployment, production migration, live TCP/proxy test or actual Agent disconnection occurred. Independent repair review pending.
