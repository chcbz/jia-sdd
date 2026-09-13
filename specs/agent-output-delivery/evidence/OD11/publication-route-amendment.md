# Pre-release publication route compatibility amendment

Decision confirmed with the sole API writer on2026-09-13 while integrating remote API `e54f579e` into accepted OD07 API `ed2ada84`.

| Operation | Route after amendment | Authority |
| --- | --- | --- |
| Existing published managed artifact upload | `POST /agent/tasks/{taskId}/artifacts` | Existing user JWT + unique `actorAgentId` query parameter and member authorization |
| OD `publishTaskOutput` | `POST /agent/tasks/{taskId}/output-publications` | Current run ticket + exact idempotency key/body |
| OD task output reads | Existing `GET /agent/tasks/{taskId}/artifacts` and version/detail/download routes | Current user JWT + source/version authorization |

The old combined POST mapping would be ambiguous in Spring with output enabled. Separate paths avoid changing the already published client API or selecting an authentication protocol by attacker-controlled body/header shape. Security filters and Controllers must agree on paths. User JWTs must not gain OD publishing permission; run tickets must not become authority for the legacy user API. Policy1 guards must also cover the newly integrated legacy artifact/work-item entrypoints.

The legacy content-download endpoint must reject OD-managed rows rather than interpret its old visibility rules as OD user authorization. Publication must not cross protocol ownership of an existing artifact ID/version. These additional data-boundary checks are required even after HTTP mappings no longer collide; see concurrent-integration-preflight.md.

The OD POST has not been released; update the API and Agent client together before the first release. Do not add fallback from the new route to the old one. `publishTaskOutput` operationId, body/response schemas, exact version semantics and receipt behavior are unchanged. Existing root fixtures contain body examples rather than route URLs, so `fixtures.json` and `lease-fixtures.json` remain byte-for-byte unchanged. Old archived R1 probe reports retain their historical route; they are not rewritten as amended-route evidence.

Root updates OpenAPI, active design and HTTP verification tool. API writer owns mapping/security/tests and product contract snapshots, followed serially by Agent HTTP transport update and affected tests. Web's OD retrieval routes need no path change; the separate preexisting ArtifactTransfer UI retains its contract. Real combined application startup and mixed credential-path rejection are required before release. This document records the contract decision, not implementation or release acceptance.

Root verification after amendment: all21 operation IDs remain unique, all279 internal refs resolve, all36 JSON schemas validate, and all5 requestExamples validate. `test-http-probe-controls.py` passes4 synthetic control tests, including task publication/replay using only the new path with run-ticket credentials. These are contract/tool checks, not live API validation. OpenAPI SHA256 is `e396496872585fa9addfb008ec5748625492b3dc7c2acc7514aca614040ccc30`; unchanged fixtures SHA256 is `453968ce85423aaf091e81d8600f2959fc44efca66793637927a06da54e48f6f`.
