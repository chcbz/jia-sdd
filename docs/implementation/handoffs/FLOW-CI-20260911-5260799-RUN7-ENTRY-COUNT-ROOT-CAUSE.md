# Flow 5260799 Run 7 entry-count root cause

**Observed:** 2026-09-11 07:30 Asia/Shanghai  
**Run/job:** pipeline `5260799`, Run `7`, Job `513006964`  
**Scope:** no deployment; cloud-only targeted tests, layering and bootJar.

## Exact result

Flow checked out source tip and built commit `07f5140c11078942efdb7486e0db7e8c235443c2` with ticket `6d2a18c4ed3d54a0f00316085c0c9dea8f1d5f16da9b800fbd843b33e3b20ee0`. Gradle completed successfully in 4m55s. The source remained clean before/after, and four XML suites (72 tests) reported zero failure/error/skip. The mandatory bridge correctly returned rc70 and exported no application JAR.

The new numeric diagnostic removed the ambiguity:

```text
artifact archive inspection limit exceeded: entry_count configured_limit=100000 prior_total=100000 attempted_total=100001 current_declared_size=5909 depth=1 ordinal=3619
```

This is not a Gradle/test/private-repository failure. The security scanner exhausted the aggregate recursive archive entry budget while inspecting a valid nested JAR at depth 1.

## Root-cause matrix

| Symptom | Root cause | Bounded remediation | Forbidden |
| --- | --- | --- | --- |
| Gradle PASS but bridge rc70/no artifact | Aggregate recursive entry cap `100000` is below the current Spring Boot dependency closure. A read-only count of the already deployed 220,129,640-byte JAR found 127,315 entries / 760,224,425 declared bytes / depth 2. This is sizing evidence only, not Run7 artifact equivalence. | Raise only the entry-count cap to `150000` (about 18% headroom over the observed 127,315), retain 1GiB declared-size, 128MiB single nested archive and depth 3 limits, update numeric fail-closed regression, run static unit suite, commit/push exact tool delta, independently review, then issue one fresh ticket and one new run. | Do not retry Run7/ticket; do not disable recursive scanning; do not raise declared-size/depth/nested-size limits; do not treat Gradle PASS as accepted evidence; do not deploy. |

Durable sanitized summary: `docs/implementation/plans/FLOW-CI-20260911-pipeline-5260799-run7-summary.json`.
