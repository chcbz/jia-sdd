# R4: artifact scan-limit diagnostic remediation plan

## Status and purpose

Run3 on September 10, 2026 (Asia/Shanghai) achieved native Gradle exit0, `bootJar`, and four XML suites/72 test cases without failures, errors, or skips. It nevertheless failed as a pipeline because the post-build bridge returned70 before exporting an application JAR. The bridge’s recursive JAR scan reported only `artifact archive inspection limit exceeded`; its fixed limits and a common error message cannot distinguish the actual trigger. This plan is diagnosis-only instrumentation, not a threshold increase or a rerun approval.

The private Maven/OpenCV and variable-group mapping are verified successful in Run3. Old pipelines1466118/4403172 remain unchanged;5256653 remains manual/no-deploy.

## Established facts

| Fact | Evidence |
|---|---|
| Gradle execution finished successfully | Run3 receipt, stdout: 201 executable tasks, BUILD SUCCESSFUL in4m13s, native exit0 |
| Targeted quality evidence | exported sanitized XML: 4 suites/72 cases, failures/errors/skips0 |
| Private OpenCV supply | same-run dependency provenance: org.opencv:opencv:4.5.5,722802bytes,SHA323d…95f4 |
| Export failed before delivery | receipt bridge_exit70, statusbridge_failed, no `application_jar` record |
| Scan ambiguity | `verify_export_jar` subtracts nested and outer `ZipInfo.file_size` from shared1GiB and shared100000-entry budgets, then raises one shared message |

No Run3 cloud JAR remains recoverable in the exported evidence. The 9302-byte artifact download is evidence-only, not a deliverable.

## Root-cause matrix

| Candidate | What can be concluded | What cannot |
|---|---|---|
| shared declared-size sum >1GiB | possible; nested ZIP container sizes plus their members are cumulatively charged | actual count, current member declaration, and whether this condition fired |
| shared entry count >100000 | possible; entries at all recursive levels are cumulatively charged | actual count and whether this condition fired |
| ZIP bomb/unsafe content | not established | must not call it a bomb or relax controls |
| existing PublicArtifactVerifier PASS | its own constraints passed | that bridge’s recursive metrics should pass; scopes/limits differ |

Fixed API6267 verifier uses config1MiB, per nested JAR256MiB, cumulative nested extraction2GiB and a per-archive100000-entry check. It is not the same recursive bridge budget.

## Allowed source-owner scope

Original `critical_worker` only, original Flow worktree, only:

- `ops/orchestration/flow_remote.py`
- `ops/ci/aliyun-flow/tests/test_flow_remote.py`
- `ops/ci/aliyun-flow/README.md`

No API changes, YAML/control scripts, ticket/receipt schema expansion, root orchestrator changes, cache/import changes, threshold changes, publish/deploy behavior, or source task changes.

## Required implementation contract

1. Preserve exact current limits: recursive declared-size1GiB, recursive entries100000, nested file128MiB, max depth3. Do not change scanning traversal or accept an unchecked archive.
2. Replace the common budget failure only with a bounded, nonsecret diagnostic string that identifies **one** dimension: `declared_size` or `entry_count`.
3. Include only fixed numeric telemetry: configured limit, prior total, attempted total, current declared size, current depth, and member ordinal within its current archive. Do not include archive/member filenames, ZIP comments/extras, file content, raw password patterns, paths, credentials, source URLs, or exception stack traces.
4. Maintain existing fail-closed behavior for malformed ZIP, nested archive, secret detection, scan bounds and all native Gradle/receipt/export gates.
5. Add fake-ZIP unit tests that independently exceed each fixed budget, assert the correct dimension and only allowed numeric fields, and assert no secret/string member names leak. Keep existing nested-secret rejection test.
6. No real Gradle/npm/cloud/database build. One bounded standard-library suite only; reviewer reuses unchanged Run3 evidence and does not rerun cloud work.

## Acceptance / next gates

- Source owner self-tests fake archives only.
- Independent reviewer must inspect exact diff and redaction contract.
- Main must byte-exact integrate accepted files, issue a new ticket and obtain a separate exact payload review.
- A future cloud run must be separately authorized. If it again fails at scan, report the dimension/counters and stop; this plan does **not** authorize any threshold modification.
