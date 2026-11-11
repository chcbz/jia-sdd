# W03 configuration-binding remediation matrix

2026-09-05. No R3 runtime retry was attempted. Current R3 candidate `10219a7e7e8227540532714cc2909425c3cfc379`, tree `f6df869464b038be079810e0444afdc6b25e6518`.

| Attempt/evidence | Cause | Bounded correction |
| --- | --- | --- |
| R2 runtime log/hash and 32-test XML in W03-R2-VERIFICATION.md | Compatibility overload makes configuration record canonical constructor ambiguous to Boot | R3 production `@ConstructorBinding` is independently confirmed correct; retain it unchanged |
| R3 independent reviewer 01a070b3-0840-70c2-b3ad-53ce110fda3b REJECT 0/1/0 | New binding test enables preview using full EconomyConfiguration but supplies no JdbcTemplate, activating schema initializer unintentionally | Isolate ONLY the new binding test with a properties-only ApplicationContextRunner configuration using @EnableConfigurationProperties(EconomyPreviewProperties.class); retain existing full configuration startup/allowlist/schema tests unchanged |

Authorized next source scope: **one test file only**. Add a nested properties-only @Configuration(proxyBeanMethods=false), use its runner for both explicit binding cases, assert original bound fields. Do not mock/disable/relax production schema initialization, gates or property defaults; do not add DB or change production code. Commit clean R4, independent delta review, then one serialized focused R4 run including configuration and previously unreached OAuth security test after current R00 verifier finishes. Stop blind retries. This is test-fixture isolation, not a new feature or production fallback.

## R4 source closure

Independent reviewer `01a070b3-0840-70c2-b3ad-53ce110fda3b` returned **ACCEPT 0/0/0** on clean `97df61a1361645d23096de28d822494a24b5242d`, tree `1ec7d890b0dc4b2b44ffaeec22f51bc2197ddf2f`, parent `10219a7e`. Exactly one test file changed: binding regression uses a properties-only runner/nested configuration; existing full-context gate/schema tests remain unchanged. R3 production constructor annotation was already confirmed correct. No R3/R4 runtime test has run yet; source acceptance does not waive the serialized verifier gate.
