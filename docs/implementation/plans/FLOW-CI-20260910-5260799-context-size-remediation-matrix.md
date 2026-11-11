# Flow CI backend context-size remediation matrix — pipeline 5260799

**Prepared:** 2026-09-10 (Asia/Shanghai)  
**Scope:** fresh copied pipeline `5260799` / `cyf-api-kit-ci`, manual cloud-only backend validation. No local Gradle/npm build, deployment, artifact publication, OSS/ECS action, or production database access.

## New attributable root cause

Flow reports: **“流水线上下文数据过大，请减小流水线运行时参数的大小”** (“Pipeline context data is too large; reduce the runtime parameter size”). This is concrete scheduler/initialization evidence for the prior empty JavaBuild logs.

| Failure evidence | Attributed cause | Corrective action | Why this is a materially new diagnosis |
| --- | --- | --- | --- |
| Runs 1–3 ended before JavaBuild emitted a log; public job logs are empty. | The current YAML carries a compressed/base64 payload containing the ticket plus all four runner tools. Its YAML is 69,641 bytes; its runtime payload includes 140,979 bytes of tool content (before base64/compression). | Version the exact four reviewed runner files under the API repository’s `ops/` tree. The Flow command will clone/pin the API source, copy those versioned files to the separate tool root, and transport only the small immutable ticket. | It removes the reported scheduler initialization input rather than retrying the same oversized configuration or relaxing any build gate. |
| Previous ticket was bound to source commit `903c24ed…` and expires at 2026-09-10T16:25:59Z. | The source must change to include the versioned tool bundle, so the old ticket cannot authorize the new source or tool digests. | Push a commit containing only the four versioned CI tool files, update the ledger to its exact source commit/tree, and issue one fresh ticket bound to pipeline `5260799`. | The ticket preserves immutable source/tool provenance and the existing no-deploy Gradle allowlist. |

## Invariants retained

- One supported `JavaBuild` step, JDK 21, source/filter `develop`, `triggerEvents: []`.
- Cloud-only selector remains `:common:jia-common-core:test --tests cn.jia.core.security.SensitiveDataSanitizerTest`, `validateLayering`, and `:starter:bootJar`.
- Maven values stay exclusively in encrypted Flow variable group `44254`; no credential literal, output, or local config is copied.
- No deploy/upload stage or new artifact publication is added.
- The worker still validates exact ticket SHA, source commit/tree, tool hashes, Java identity, Flow identity, credentials presence, receipt integrity, and final native return code.
- Runs 1–3 are immutable evidence and are not retried. A new run may occur only after source push, fresh ticket, exact YAML review/readback, and scheduler-error resolution.
