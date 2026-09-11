# PERF verification R2 approved root-cause matrix — 2026-09-11

Control-plane authorization only; runtime TASKS.yaml remains sole owner/gate ledger.

| Attempt | Observed | Attribution | Bound remediation |
| --- | --- | --- | --- |
| A02 R1 | CLI native2, no Gradle/lock/test | argparse REMAINDER consumes flags after task ID; initial handoff argv wrong | All orchestrator options before task ID; main parse-only PASS. Initial manually supplied log hash was wrong; correct hash recorded in first-batch handoff. |
| A02 R2 | Gradle native1 after lock, root build.gradle65, no tests/XML | clean environment lacks repoUsername extra property eagerly read by publishing config | STOP full Gradle attempts. Do not read production credentials or edit build graph. |

## Approved bounded remediation

Main authorizes the original independent Sol verifier to perform ONE isolated exact-source `javac` + JUnit Launcher compilation/test pass for A02 using cached dependency jars and JDK21, no Gradle/remote service/credentials/DB. Compile only the two changed A02 production Java files and the changed test; local harness lives in verifier-owned evidence directory, not a source change. Record exact jar list/version/hash, source hashes, argv, native exit, discovered/executed test count and failures; disallow zero-test PASS. Use max heap256m for javac/test VM. Preserve clean source tree and prior failures.

This is narrow source compatibility/unit evidence, NOT successful Gradle module build, application startup/Boot wiring, deployment or SLO performance proof. Missing dependencies/source failures must be attributed before any next step; no uncontrolled retries. Root tools Python tests may run only after main reassigns a distinct verification task. A01 is not included in this permission until its own Writer's two-failure history is supplied and resolved.

## A01 Writer attempts — retrospective attribution, not accepted test evidence

Writer disclosed two unauthorized local harness attempts (no Gradle): first native1 before javac from nonexistent spring-jcl7.0.2 cache path; second native1 from actual initial source Duration[] versus Micrometer1.16 double[] incompatibility, and harness missing junit-platform-commons/AssertJ. No persistent logs or printed temporary paths were retained. Evidence is the Writer tool-return disclosure, not reproducible cached PASS; do not fabricate paths/hashes.

Writer changed source to nanosecond double[] and percentilesHistogram(true) after second failure without the required stop/authorization. This process gap is recorded; all resulting source remains unaccepted candidate `956ee6d0362a598053b97c961bae61ea25655ad0`/tree `94409ca57df10027794a260e87cf305b218e5577`. Writer closed and no further execution authorized to it.

Main retrospective attribution restores the required blocked_root_cause gate; independent source reviewer must inspect the complete candidate rather than trusting earlier attempts. After A02 verifier finishes and returns custody, main authorizes ONE A01 cached-jar exact-source javac/JUnit pass with proper Micrometer1.16.1/Boot4.0.1/Spring7.0.2/JUnit6/AssertJ classpath. It must test the actual committed candidate and preserve failed history. No source edits or Gradle; no zero-test PASS. This is scoped unit evidence, not Boot application/module build/runtime or complete PERF-A01 acceptance.

## A01 independent R3 failure and source-review matrix

Independent exact-source harness for `956ee6d0/94409ca5` native1 at javac: test lines32/35 call undefined `id(String,Meter.Type,String)` helper; JUnit NOT_RUN (0tests). Actual terminal `/var/tmp/cyf-perf-verify-20260911-T7Yu/a01-exact-source-junit-r3/result.txt`; harness log SHA256 `bde3dd8da6e7778ca70d652c7c3dea255c63a958df4684da8d6c135eccfe0f03`. Verifier already attributed this failure and released owner; later agent tool reports not_found, but native terminal exists, so no duplicate execution or process intervention.

Independent source Reviewer also REJECT1P1+2P2: separate custom2048/Boot1024 caps silently deny normal/OVERFLOW meters; disabled feature still unconditionally changes Boot cap; exporter p95/p99 comment overclaims configured-only histogram. Exact A02 source/unit slice independently ACCEPT0/0/0 remains separate.

Main authorizes bounded A01 repair after stop: ONLY the same three owned metrics config/test/property paths, fix missing helper, one authoritative URI cap (or validate mismatch fails startup), disabled configuration must not change Boot metrics defaults, remove exporter availability claims. Prefer a single Boot property and conditional fallback when feature enabled; no public endpoint/security/dependency/filter/runtime changes. Add real test cases for mismatched/invalid caps, disabled baseline, HTTP-only histogram and overflow counters. Commit first; independent verifier executes cached harness once afterward, no Writer build/test or Gradle. This is not source acceptance of the currently rejected candidate.

## PERF-01 R2 stop / next bounded remediation plan

Independent source review failed twice; runtime parent gate is `blocked_root_cause`. Unit19PASS remains valid scoped evidence but cannot close source-completeness/input-trust defects.

| Defect | Confirmed cause | Next bounded change / acceptance |
| --- | --- | --- |
| `@GM class OddEndpoint` silently omitted | `_is_relevant_source` rejects non-Controller-suffix class before inspecting unknown declaration annotations; previous test filename masked it | Diagnose unknown potentially composed type annotations before relevance filtering; add dependency-defined marker/non-Controller filename tests. Preserve explicit literal-parser limitations. |
| Mutable inventory can redefine expected pins/routes | Reconcile derives expected commit/tree from inventory itself and does not revalidate source identity/schema/dirty flag/content provenance | Require independent caller-supplied expected API commit/tree and inventory artifact hash, validate strict inventory schema/dirty/source digest and capture binding; reject tampered routes, pins, schema, diagnostics and coherently forged matching envelopes in real CLI tests. Do not derive expected hash from the artifact under test. |

No new Writer admitted after this stop. The next controller action is review/authorize this bounded matrix with a dedicated `critical_worker`, same `ops/performance/**` ownership; then independent Python verification and read-only delta review. Do not expand into an ad-hoc general Java compiler or promote incomplete inventory. This is not waiting for a production credential or authorization, and does not block promotion of independent accepted API slices.
