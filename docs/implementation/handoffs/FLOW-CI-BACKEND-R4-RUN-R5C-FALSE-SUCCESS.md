# R5c false-success attribution

- Pipeline `5256653`, manual Run `6`, job `512659362`: Flow reported `SUCCESS` at 2026-09-10 09:53 UTC.
- The authenticated job log is empty (`more: false`), the run has no recorded source, and no `FLOW_CI_CONTEXT`, native runner, receipt, or final-gate marker exists. A cold Gradle test plus `bootJar` cannot be accepted from this no-op success.
- R5c used standard top-level `stages` but retained the legacy `execution-component-production@11` / `params.steps` wrapper. Flow accepted the YAML but did not execute that wrapper in the standard pipeline engine.

## One bounded repair

Use the current pipeline's standard top-level `stages -> jobs -> steps` topology directly, with the native registered `stepType: java_build` (not `step: JavaBuild`), direct `CI_RUNTIME_VERSION: jdk21` and `command`, the encrypted variable group, and the existing mandatory inline receipt gate. Issue a fresh ticket and run once only after source/config/group preflight. Do not retry Run 6.
