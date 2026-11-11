# Flow CI backend remediation matrix — pipeline 5260799

**Prepared:** 2026-09-10 (Asia/Shanghai)  
**Scope:** a fresh copied pipeline `5260799` / `cyf-api-kit-ci`; no changes to legacy pipeline `1466118`, no deployment, no local Gradle or npm build.

| Prior attributed failure | Evidence | Why it does not authorize retry | One attributable repair |
| --- | --- | --- | --- |
| Unsupported/inert component nesting produced `step不存在` or an apparent SUCCESS without Gradle activity on pipeline `5256653` | `FLOW-CI-BACKEND-R4-RUN-R2-ROOT-CAUSE.md`; `FLOW-CI-BACKEND-R4-RUN-R5C-FALSE-SUCCESS.md` | The old run IDs and pipeline are not candidates for retry. | Use a newly copied pipeline with one directly declared standard Java build step only, then verify its actual job log contains the expected execution markers. |
| Direct-native update of old pipeline returned platform-level 400/system error | `FLOW-CI-BACKEND-R4-RUN-R6-UPDATE-BLOCK.md` | No schema/credential/build cause was supplied, so re-submitting the same payload is blind retry. | Use a separate pipeline ID (`5260799`) and a new ticket bound to that ID; read back the saved configuration before any run. |
| Copied pipeline had no source association, no encrypted variable-group relation, and a private-credential literal indicator | `FLOW-CI-20260910-cloned-pipeline-5260799-inspection.json` | A cloud build without audited source provenance and encrypted Maven consumer credentials is not admissible. | Add an explicit `sources` YAML declaration for the public Gitee repo/`develop`; attach only variable group `44254`; remove all credential literals. |

## Frozen execution boundary

- API source: `https://gitee.com/chcbz/jia.git`, branch `develop`, commit `903c24edb69ebbd2b126fa3cb620e47114bf30e9`, tree `885453ca2035bb08ba7247966787cae0f268d840`.
- Required cloud gate only: `:common:jia-common-core:test --tests cn.jia.core.security.SensitiveDataSanitizerTest`, `validateLayering`, and `:starter:bootJar`.
- Flow is manual-only; no ECS/OSS deployment stage, no production DB action, no automatic trigger.
- Maven credentials are read only from encrypted variable group `44254`; their values are neither read nor recorded.
- A new ticket must bind organization `5fb7d76ee6f9d07f148529c7` and pipeline `5260799`; its SHA is fixed in the reviewed YAML.
- A run can be called successful only if the same run/job log shows Flow context, real Gradle execution, receipt/final-gate markers, and no truncation ambiguity.
