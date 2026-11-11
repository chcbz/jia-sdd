# Flow 5260799 Run 5 scanner remediation matrix

**Date:** 2026-09-10 (Asia/Shanghai)  
**Run:** `5260799` / Run `5` / Job `512765812`  
**Scope:** cloud-only backend CI; no deployment, artifact upload, or local Gradle/npm build.

## Evidence and attribution

| Attributed event | Evidence | Root cause | Correct repair | Forbidden continuation |
| --- | --- | --- | --- | --- |
| Ticket-only Flow configuration saved with final-LF normalization | `FLOW-CI-20260910-pipeline-5260799-ticket-only-apply.json`; `...ticket-only-readback.json`; `FLOW-CI-20260910-5260799-TICKET-ONLY-EOF-NORMALIZATION.md` | The controller treated Flow’s EOF-only normalization as a byte mismatch even though semantic readback passed. | Keep the saved configuration; use semantic readback for the normalization exception. | Do not resubmit the same YAML. |
| Run 5 failed after `FLOW_CI_CONTEXT` and before Gradle | `FLOW-CI-20260910-pipeline-5260799-run5-status-002.json`; `...run5-job-log-001.json` | Versioning `ops/ci/aliyun-flow/cold-init.gradle` into the API source made `verify_nested_gradle_absent()` scan its own trusted init script. The script’s intentional `gradle/gradlew` nested-exec guard at line 142 matched the generic source scanner. | Exclude **only** `ops/ci/aliyun-flow/cold-init.gradle` from the source Gradle-blob scan, after `verify_tools()` has already proved its ticket-bound bytes. Continue scanning every other `*.gradle`/`*.gradle.kts` file. Version/push that constrained runner change, issue a fresh ticket, Terra-review, and start one new run. | Do not retry Run 5, broaden the scanner exclusion, disable source scanning, relax the Gradle allowlist, or bypass ticket/tool hash verification. |

## What Run 5 proved

The context-size repair succeeded: Flow executed the JavaBuild user command, cloned the pinned checkout at `f24d3fc090f2ba85bf27fb147d5f61f75a283c49`, emitted `FLOW_CI_CONTEXT`, and reached the runner’s source verifier. Therefore the prior Flow error “流水线上下文数据过大，请减小流水线运行时参数的大小” is no longer the blocking pre-execution failure.
