# Flow 5260799 Run 6/7 archive scanner root-cause matrix

**Scope:** backend pipeline `5260799` / `cyf-api-kit-ci`; no deployment, no local Gradle/npm build, no retry of Run 6 or Run 7.

## Terminal evidence

| Run | Exact source/ticket | Gradle/tests | Mandatory bridge result | Attribution |
| --- | --- | --- | --- | --- |
| 6 / job `512770431` | Flow tip `07f5140c…`; stale ticket built `903c24ed…` | `BUILD SUCCESSFUL`, 72 tests | `rc=70`, `bridge_failed`, no artifact; identical old fixture has preserved error `artifact archive inspection limit exceeded` | Historical first scanner-budget failure; stale ticket makes the run non-promotable. |
| 7 / job `513006964` | Flow tip and built commit `07f5140c11078942efdb7486e0db7e8c235443c2`; ticket `6d2a18c…0ee0` | `BUILD SUCCESSFUL in 4m 55s`, Gradle rc 0, four XML suites / 72 tests / 0 failures/errors/skips | `rc=70`, `bridge_failed`, no application artifact; `entry_count configured_limit=100000 prior_total=100000 attempted_total=100001 current_declared_size=5909 depth=1 ordinal=3619` | Current exact-source reproduction proves the remaining blocker is the scanner's global recursive entry counter, not Flow context size, source, Gradle, tests, Maven/OpenCV, or source cleanliness. |

## Root-cause matrix

| Observation | Root cause | Rejected shortcut | Bounded remediation |
| --- | --- | --- | --- |
| Run 7 reaches JavaBuild and completes Gradle/test/bootJar. | The earlier Flow context-size error is resolved by the 9,718-byte ticket-only YAML. | Restore the 58.7–69.6KB inline tool payload. | Keep ticket-only transport; tools remain copied from the pinned checkout and SHA-verified. |
| Failure is `entry_count` at `depth=1`, not `declared_size`. | `verify_export_jar()` shares one 100,000-entry counter across the outer bootJar and every nested dependency JAR. Normal independent dependency archives are incorrectly merged into one logical archive budget. | Raise or disable the global entry cap. | Apply the 100,000-entry cap per archive; retain the 1GiB recursive declared-size cap, max depth 3, and 128MiB nested-archive cap. |
| Per-archive counting alone could permit many tiny nested archives. | Aggregate CPU work needs a second independent bound. | Unbounded recursion or unlimited container count. | Add a fixed nested-archive container-count cap and a bounded metadata/work budget charged per entry, while scanning every raw/inflated member for credential patterns. |
| Exported JAR is copied for downstream deployment. | Ambiguous traversal/symlink/duplicate ZIP members are unsafe even without extraction in this bridge. | Accept ambiguous member layouts because the scanner itself does not extract. | Reject absolute/backslash/`..`/NUL names, Unix symlink entries, and duplicate names inside each archive before opening members. Errors remain numeric/generic and never echo member names or credentials. |
| OpenCV provenance is already independently pinned. | The scanner failure happens after OpenCV resolution/provenance and before artifact packaging. | Skip OpenCV, receipt inspect, unique-JAR, SHA/size, or final rc gates. | Leave all provenance, receipt, unique application-JAR, hash/size/sidecar, clean-source, and no-deploy gates unchanged. |

## Required verification before one new cloud run

1. Terra writer changes only `ops/orchestration/flow_remote.py` and `ops/ci/aliyun-flow/tests/test_flow_remote.py` on a clean worktree based on `origin/develop` `07f5140c…`.
2. Standard-library tests cover: single-archive 100001 rejection; aggregate nested entries over 100000 accepted when each archive is below its cap; nested-container/work-budget rejection; recursive declared-size rejection; nested compressed secret rejection; traversal/symlink/duplicate rejection; existing unique bootJar/OpenCV/receipt gates.
3. Independent Terra read-only review returns no P0/P1/P2 findings.
4. Push one exact tool-only commit, update the ledger to its commit/tree, issue a fresh non-expired ticket and ticket-only YAML, read back pipeline/group/source, then start exactly one new manual no-deploy run.
5. Any new failure is attributed from `FLOW_CI_RECEIPT_SUMMARY`; no blind retry and no threshold-only change.
