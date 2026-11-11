# Local API catalog/roster — remediation matrix (2026-09-17)

## Decision

Resume only with source commit `1938d742cbb846157c268cbe4e02010b169ea194` / tree `a7ad23c35a547a86bf7bdc84ad2684380b42a449`.
No Alibaba Cloud Flow action and no production database write is permitted.

## Attributed attempts

| Attempt | Observed failure | Attribution | Action |
| --- | --- | --- | --- |
| Local Gradle bootstrap | Root filesystem filled while the isolated wrapper downloaded Gradle. | Capacity incident during a real build bootstrap; not a release threshold. | Reused the already present Gradle installation. |
| Offline Gradle retry | Required JUnit platform dependency was absent from the local cache. | Offline cache miss, distinct from capacity. | Allowed one dependency-resolving build. |
| Mapper test task | Pre-existing stale test sources have obsolete mapper method signatures. | Unrelated test-source compilation drift; changed sources compiled. | Do not alter unrelated urgent-release tests; use production boot JAR plus live authenticated regression. |
| Live OAuth+PKCE regression | `GET /agent/personas/catalog` returned business `BAD_REQUEST: tenantId is invalid`. | `AgentController` deliberately canonicalizes the single tenant to `0`; `AgentPersonaDaoImpl.requireExactScope` still rejected `0`. | Remove only that obsolete rejection; retain exact scope validation and add a focused DAO regression test. |

The fourth item is a new production behavior finding, not a retry of the three prior build/test-environment failures. The scoped fix is limited to the catalog DAO guard and its unit coverage. It neither weakens client/owner checks nor changes database data.

## Required exit evidence

1. Local `:starter:bootJar` for the exact source tree through the orchestrator.
2. Atomic local installation with the current JAR preserved as rollback material, then loopback health `UP`.
3. Redacted, real OAuth2 Authorization Code + PKCE regression: catalog succeeds with normal data; roster and map remain successful; CORS preflight remains allowed.

## Packaging remediation observed at 12:39 CST

The failed bootJar had already consumed its 221,386,058-byte output JAR and left only 35,954,688 bytes free. The verifier next needed to materialize `openai-java-core-4.39.1.jar` (42,100,857 bytes) in its private directory, so the capacity observation explains the generic nested temporary-file failure without relaxing the verifier. Two identified generated candidate JARs were removed only after immutable SHA-256 custody was recorded in `/opt/cyf/service/api/release-records/local-build-artifact-reclaim-20260917T1239Z.json`; deployed and rollback JARs, source trees, release records, database, and service process were preserved. The new build invocation differs only by this evidenced artifact cleanup.

## Superseding remediation: retain live v1.6 baseline

The v1.6 release owner completed deployment of `a8e9170873062165176626775d66c92dfc2e7a1a`. The older `1938d742` boot JAR is not installable because it would regress that baseline. Candidate `2c0926a5b4c809b610d93266e7a637268fc49589` / tree `511cdea8568e984c8141938956f10b84b567de0c` is based on a8e91708 and changes only the DAO guard and focused test class. Adds missing/malformed tenant/client rejection coverage. Run the real four DAO tests with an isolated Gradle source set (no production DB), then rebuild and retain public artifact security verification. No full mapper-suite pass is claimed. Source baseline change is the validated remediation for the last blocker.

## 14:23 public regression: foreign-owner SQL projection defect

First v1.6-based candidate `2c0926a5` installed healthy, then real public OAuth+PKCE and TLS-valid requests reproduced `AGENT_FORBIDDEN: Foreign persona binding disclosed durable details`. Roster was E0/4, map E0/5; public CORS correctly allowed kit origin. Root cause is the binding-overlay `CASE ... ELSE 0` returning non-null `agent_reference_valid` for foreign-owner rows whose LEFT JOIN identity is deliberately absent. The service ACL correctly rejects this projection; do not weaken it.

A new isolated H2 test executes the actual mapper SELECT unchanged and fails exactly `expected null but was 0`; owner projection and other-tenant/client exclusion pass. Evidence: `/var/tmp/cyf-catalog-v16-regression-20260917/red-sql-test.xml`. Candidate `4451c300` / tree `b1e5398970d31c838c0e38f8d65aa2f224942fa0` adds `WHEN i.id IS NULL THEN NULL` to that CASE. No ACL removal, no production DML, and no role/owner migration. Rerun DAO, real SQL, mapper contracts, cache tests before packaging and live verification.
