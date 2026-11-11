# Flow CI backend R4 Run remediation R2: unsupported step identifiers

## Evidence

- Pipeline `5256653`, Run `5`, job `512225566` failed before useful job output.
- The Flow console job detail, supplied by the user on 2026-09-10, reports: `step不存在` (step does not exist).
- The R4b/R4c Flow DSL uses `JavaBuild`, `ArtifactUpload`, and `Command` under `step:`. The older successful backend pipeline `1466118` uses the Flow `schema: tb` execution component and built-in step types `java_build` and `tb_oss_upload` instead.

## Attribution

The confirmed immediate cause is unsupported Flow step identifiers in the custom DSL, not Gradle, OpenCV, Maven credentials, or a host deployment action. The old runner/scheduler hypothesis is superseded for this run; no further retry of R4c is permitted.

## Bounded remediation

Construct a new no-deploy candidate for pipeline `5256653` using the known-valid `schema: tb` execution component and `java_build` step type, with JDK 21 and the existing encrypted variable-group credentials. Preserve the pinned ticket, cloud-only source verification, no production DB/deploy actions, and required result/receipt gate. Use only a supported artifact uploader after its exact configuration is independently reviewed. Do not copy any credentials from pipeline `1466118`.

Before one new run: exact candidate review, authenticated readback, fresh ticket if required, and source/branch preflight. Do not change pipelines `1466118` or `4403172`.
