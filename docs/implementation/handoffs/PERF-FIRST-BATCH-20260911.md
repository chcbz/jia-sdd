# PERF first implementation batch — 2026-09-11

Task contracts only; current owner/gate stays in TASKS.yaml runtime_ledger_json.

- User authorized implementation of API <=3s initiative; not production load tests or cross-task process control.
- Root base c953802b4e7b719900ef531ebed37c309a882805; API base e7da0a435acdff93ae64473223631b3f7d7cbdac (fresh origin develop ls-remote confirmed). Dirty root/API/Web checkouts remain untouched. Historical 42/401 count is not this candidate inventory.
- PERF-00: control-plane SDD/ledger/handoffs; contract independent reviewer R4 ACCEPT from prior turn, not source acceptance.
- PERF-01: independent root worktree `.worktrees/perf-inventory-20260911`, branch `codex/perf-inventory-20260911`; allowed paths `ops/performance/**` only. Deliver dependency-light deterministic offline scanner/reconciler, profile/source binding and negative tests. Never infer runtime equality from static scan or skip unsupported expressions. Runtime capture and full PERF-01 acceptance remain pending without legitimate isolated profile evidence.
- PERF-A02: independent API worktree `.worktrees/perf-api-logging-20260911`, branch `codex/perf-api-logging-20260911`; allowed paths `common/jia-common-service/src/main/java/cn/jia/core/interceptor/HttpRequestLogInterceptor.java`, `common/jia-common-service/src/main/java/cn/jia/core/config/HttpRequestLogConfig.java`, and their corresponding tests only. Remove eager parameter/header/body logging and per-request JVM-memory sampling, monotonic request-scoped async-dispatch-safe timing, bounded safe route/request ID, slow/error structured logs. No business/audit filter, ACL, transaction, timeout or response changes. This slice is not whole-request filter/TTFB/SLO evidence.
- PERF-A01: independent follow-up API worktree; allowed paths will be frozen before claim. Add route-histogram configuration and tests without weakening actuator security or public exposure. May proceed independently of inventory runtime capture; runtime baseline requires metrics.
- Verify with dedicated verification owner then independent read-only sol_reviewer; no Gradle except orchestrator and explicit bounded resource admission. No provider retry on known gpt-5.4-mini unavailable; known-working Sol verification-only fallback allowed.
- First batch does not authorize Agent query changes until credible isolated baseline. WX daily-vote Writer owns unrelated wx/material/point/user paths; no overlap or process intervention.

## PERF-A01 owned-path freeze

- Worktree `.worktrees/perf-api-metrics-20260911`, branch `codex/perf-api-metrics-20260911`, same API e7da0a43 base.
- Allowed paths only `starter/src/main/java/cn/jia/config/ApiPerformanceMetricsConfig.java`, `starter/src/test/java/cn/jia/config/ApiPerformanceMetricsConfigTest.java`, and `starter/src/main/resources/application.properties` (new bounded metrics property lines only). No dependency/security/other profile changes.
- Slice: existing Boot/Micrometer HTTP server request histogram with 1s/2.5s/3s buckets, bounded route tag cardinality and neutral unknown-route handling, tests for configuration and bounds. Reuse Boot Hikari/JVM metrics; no duplicate servlet timing filter, no public actuator exposure. Inflight/deadline enforcement and dedicated exporter/dashboard stay follow-ups, never claim complete PERF-A01.

## A02 submitted candidate and verification admission

- Writer candidate `014fb7edaa53928aa5ca309ea4c8537889763563`, tree `4de32d4ccdb1efe06dd38ee2ff4009532d5300ab`, three owned files only, base `e7da0a435acdff93ae64473223631b3f7d7cbdac`.
- Independent known-working Sol verification fallback admitted for ONE offline `:common:jia-common-service:test --tests cn.jia.core.interceptor.HttpRequestLogInterceptorTest` through orchestrator; max workers1, JVM384m/metaspace256m, JDK21. No DB, full build, production or foreign process control. Missing dependencies require attribution, not repeated Gradle.

## Inventory submitted candidate

- Root tooling commit `276518afe32edc3480e8948f003de100d8dc822c`, tree `0b20a13cbaf211e59766598b3161e5eeae3136e7`, base `c953802b4e7b719900ef531ebed37c309a882805`; four `ops/performance/` files only.
- Writer reports 7 standard-library unit tests and py_compile PASS, not independent verifier evidence. Independent review requested. Explicit supported-parser subset, no live capture/YAML validity/full inventory acceptance claim.

## A02 verification attempt1 root cause / bounded remediation

- Native rc2 occurred before any Gradle/lock/test: supplied documented task-first CLI order conflicts with current argparse REMAINDER. Correct form is `gradle [all orchestrator options] PERF-A02 -- ./gradlew ...`.
- Main parse-only validation of corrected argv passed; no Gradle launched by validation. Authorize exactly one actual offline selector using corrected argv, preserving tree/selector/limits.
- Actual log `/var/tmp/cyf-perf-verify-20260911-T7Yu/owned-log` SHA256 `6226ef241a74805c19af12fb80259a31a0edcac0c1c415ed0b2bd72c71a3e64b`. Initial blocker attempt string supplied an incorrect hash; it remains historical and is superseded by this exact-file correction (evidence cache has corrected hash).

## Independent R1 source review

Reviewer `01a08df1-c152-7c32-8fc8-b06c9495fa78`: A02 `014fb7e/4de32d4` SOURCE ACCEPT 0/0/0, conditional on actual scoped tests (not full module acceptance). Inventory `276518a/0b20a13` SOURCE REJECT 0/3/0:

1. Unknown/composed/aliased annotations silently omit routes (e.g. @MyGetMapping and @GM yield no route or diagnostic).
2. Scan accepts unbound/empty framework manifest and reports ok: missing exact commit/tree, malformed route surface, empty framework data are not rejected.
3. Runtime parser drops malformed records, does not expand Boot4 structured plural methods/patterns or multi-method/path arrays; claimed capture_content_sha256 is not verified, forged hash/empty malformed matching captures can PASS.

Bounded remediation owned `ops/performance/**`: conservative unknown-annotation diagnostics with explicit known non-mapping allowlist; fail-closed unsupported grammar, strict non-empty bound declared framework surface, Boot4 structured mapping condition expansion, strict input record shapes, mandatory canonical payload hash verification and missing envelope rejection. Add negative regression tests for every finding; no live runtime claim. Reviewer-created Python bytecode cache is generated task-local dirtiness only, not source change.

## A02 actual independent unit evidence

Exact candidate `014fb7e/4de32d4`: JDK21 cached-jar javac native0; JUnit Launcher native0,6found/6executed/6PASS,0skip/fail/abort. Evidence `/var/tmp/cyf-perf-verify-20260911-T7Yu/a02-exact-source-junit-r3`; source manifest `4b6afc693fe0fc706ebfdec30a41d9f6fe70a62b09bed1899178f7152cc50218`,26jar manifest `020fcf14bc905715841580c755f6b8ce344156142f79c09b4f679a35d02e5cec`; cache key `13c9ddf4824b54e4260663f540085dde1ed0992e16a8bec73b1ae96563ca3c6c`. Main verified all13 evidence-sha256 entries and clean exact tree. This covers changed source/unit behavior only: attempted full-module Gradle failed configuration before tests, Boot wiring/runtime/performance not verified.
