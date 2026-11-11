# Flow 5260799 — JavaBuild candidate still fails before execution

**Observed:** 2026-09-10 Asia/Shanghai  
**Runs:** `2` (trigger mode `1`, not claimed as controller-manual) and `3` (controller-manual trigger mode `4`).

## Confirmed configuration

The JavaBuild-only revision was saved and semantically read back with source branch/filter `develop`, an empty declared source trigger list, no upload/deploy component, and the fixed ticket SHA for pipeline `5260799`. The encrypted Maven variable group remains attached. `SetupJava` and `Command` were removed after the user-supplied enum established that they are invalid components; the only configured build component is `JavaBuild` with JDK 21.

## Failure evidence

- Run 2 / Job `512735713`: `FAIL`, log content empty.
- Run 3 / Job `512742831`: `FAIL`, log content empty.
- Neither job reaches a component banner, Java setup/build, source checkout output, Gradle, Maven/OpenCV, receipt, or final-gate marker.

Run 2 appeared with trigger mode `1` despite the declared empty trigger list. Its origin is not inferred from public API data; it must be checked in the Flow console. Run 3 is the single controller-started manual verification run.

## Attribution and stop

Both failures occur before `JavaBuild` emits any log, so the supplied component enum was a valid configuration repair but does not explain the remaining runtime failure. Public Flow API exposes no scheduler/runner initialization detail. This is the second consecutive same-condition failure; no Run 4, job retry, or configuration retry is authorized.

## Required next evidence

Obtain the Flow console/server-side event for **Run 3 / Job 512742831** (and explain Run 2 trigger mode `1`): runner allocation, image pull/container creation, runner authorization/quota, resource group health, and source-trigger reason. Apply one diagnosis-backed repair only after that evidence and an independent Terra review.
