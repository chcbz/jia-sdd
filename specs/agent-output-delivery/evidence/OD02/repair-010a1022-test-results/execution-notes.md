# OD02 repair candidate verification

Candidate: `010a102217d105f6e6f5dd94dc3d01a8a4e5ffcc`. Root and writer observed a clean worktree while the final combined run executed. The independent review is tracked separately in `../candidate-010a1022-review.md`.

## Final combined run

- Exact command: `final-combined-command.txt`; working directory `/home/chc/wsps/cyf-worktrees/output-api`.
- Actual process exit: **0**, retained in `final-combined-exit.txt`; output in `final-combined.log`.
- The command invokes the preserved `run-gradle-with-od-env.py` wrapper. It acquires `/tmp/cyf-gradle.lock` around the complete Gradle process, uses the task-owned Java 21, one worker, 512/256 MiB JVM limits, and the previously reviewed development-only dependency init. Credentials are read from private files into process environment, not embedded in arguments or this archive.
- Seven suites: **64 tests, no failures/errors/skips**. Schema MySQL 9; authorization MySQL 9; real MySQL/MinIO/ClamAV upload 20; content inspector 8; authorization unit 11; security configuration/coexistence 7.
- `final-candidate-association.json` is the original writer manifest (SHA-256 `2f953b257668c869d43eb771369002ead085d3ab6c7aeda422e2cfa7edaa3c9d`). Root independently checked its command hash, exit, every XML/hash/count and all 17 changed candidate file hashes against Git.
- `final-combined-results/observation.json` is a derived observation in the root verifier's format. `root-association.json` reports correspondence valid for those 64 tests and 17 changed paths. It is not a full dependency-source closure or coverage verdict.

## Historical stages

Earlier unit/security, schema, authorization and upload runs are retained without adding their overlapping totals. Schema debugging initially rejected normal metadata: MySQL index ordering differed from Java ordering, and the actual JSON column has NULL charset/collation metadata. Failure logs and available debug XML remain intact. The first full schema-failure XML was not present in the handed-off directory; its command, exit and log are retained, and no replacement XML is fabricated.

This focused passing run does not replace the prior failed full-module result: `../full-module-regression-0ac3921/` still records the unchanged exact-Rabbit fixture prerequisite failure and 103 service skips. No unrelated Rabbit service was installed/restarted to make this task green.

All copied files were compared against configured private credential values before archival; no match was found. Developer dependencies, isolated database topology and test doubles retain their documented limits. These tests do not establish owner HTTP download, client restart recovery, UI behavior, effective deployment configuration or production release.
