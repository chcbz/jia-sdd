# R5 TB candidate review record

## Candidate

- YAML: `docs/implementation/plans/FLOW-CI-20260910-cold-r5-tb.yaml`
- SHA-256: `cc6e0f291590109e4eb04f3e7f97a8005d8620c72823acb4b2d8128d5f674141`
- Scope: Pipeline `5256653`; manual CI only; no deploy or artifact publication.

## Structural checks performed

The controller checked that the candidate has exactly one `schema: tb` / `pipeline:` hierarchy, uses `execution-component-production@11`, one `params.steps[]` entry with `stepType: java_build`, `CI_RUNTIME_VERSION: jdk21`, and `buildNodeGroup: K8S-4`. It rejects `sources`, `defaultWorkspace`, `variableGroups`, `JavaBuild`, `ArtifactUpload`, `Command`, and `tb_oss_upload` in the Flow text. The embedded cloud Python and final-gate Python both parsed successfully. The inline gate returns the recorded native runner exit code and requires a successful receipt and inspection result.

## Independent reviewer availability

Three independent read-only reviewer dispatches were attempted on 2026-09-10 and each failed before reading the candidate with provider HTTP 429. No reviewer result is represented as ACCEPT. The candidate is therefore advanced only under the user's existing explicit cloud-CI authorization, with platform YAML acceptance and one manual no-deploy run as the next observable gates. A reviewer must be re-run after provider recovery before any later deployment design or approval.
