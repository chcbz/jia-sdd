# UR06 actual compile remediation — source handoff, 2026-10-08

Candidate commit `859546cad74750ea10a87fac389c3f2b9f0e3d42` / tree `cc3c515345f6e791a8052b10a382f84fe089ed4c`.
Base `9c431f3be9c62467cd94b42dead27b4f14cb3909` / tree `13a8cdc7b1be98cb9ad2dbf78bf9ae5f337f121b`.
WT `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008` / branch `codex/ur06-m4-mysql-e05-20261008`; exact remote HEAD match, clean including untracked.

ONLY `/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java` changed. Exactly two lines/two replacements at line611 and670:
- `http(s)` → `Ur06EnrollMysqlAcceptanceTest.http(s)` in new Lane.awaitRealHeartbeat.
- `http(lastServer)` → `Ur06EnrollMysqlAcceptanceTest.http(lastServer)` in new Lane.emitObservedEvidence.

Actual61023 javac type failure was lexical Lane.http(String,int) shadowing outer static http(JsonNode); these explicit qualifications preserve the intended existing observation. No overload/API/oracle/test expectation changes. 90918 kernel OOM remains separate original evidence, not relabeled a source/MySQL/network failure.

Static proof: exact two replacements normalize WHOLE file back to9c431; all original7+6 test methods, 11 oracle methods and EVERY other method byte-equal. All other five original phase files SHA-equal, including original MySQL guards/schema/auth/source C and UR04 proofs. One Java tree-sitter grammar pass and diff check are STATIC ONLY, not typechecking or actual execution.
File SHA256 `c0d66e45e185cb70d3ad865943214962c916d1a94284d9891b95efdc1d453626`.

Static script `/var/tmp/ur06-m4-http-qualification-static-20261008.py` SHA `1da37739c118a63f2e8d4540d85ac14b3d7642677b948a33b71f7654fac3da1f`.
Static result `/var/tmp/ur06-m4-http-qualification-static-20261008.json` SHA `66360d697aa6104c5e77a2f16204abd5973f7f010a318882449dff7e6a023d8f`.

This Writer ran NO Gradle/javac/MySQL/pip/install/Flow/production. Actual compile/root validateLayering/all tests/MySQL/install are NOT_RUN for this new candidate. Main consumes this ONE patch into fresh fixed tree/tuned compile/root layering, then NEW exact C/D full install and single accepted-target awaited callback19 (H2six + foundation7 + M4six). No old target, blind same-input retry, Reviewer, ledger/adapter/root gate changes by Writer. Source repair delivery only; not UR06/Goal acceptance or deployment.
