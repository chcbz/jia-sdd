# Economy API source integration packet — 2026-09-06

Prepared only; Writer requires separate ledger GO after R01/W09 correction source verdict. This integrates source for verification; it does not promote W13/release dependencies.

Inputs (remote API/Web refs rechecked at13:10):
- Preserve current accepted API `34b67fed96061bf9c3132106ca219fc6f5f6ba05` as integration baseline.
- Corrected economy candidate `d875ccfa0ba31187a29362f7ac454832af3e0e25` / tree `db94618f20e6991aef9b2170cc160d2a1a32610f`.
- Independent source-accepted three-line W06 test correction `fb2c7733c003b306e419120e7d78c23d9551183b` / tree `ab631b965d0f3fe8bfcde7828d14c6215d4b1870`.
- Web remote `d81b59e2724c45e7af47c60022296b2d20793295` must be retained later; no Web writes in this task.

A single critical Writer under W09 may create NEW `.worktrees/eco-v0-api-release-r1` from34b67fed, merge d875ccfa then fb2c7733 without rewriting original worktrees or root gitlinks. Parent/common-base/source/tree proof required. The only paths changed by both pre-correction economy and current baseline are `chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java` and `starter/src/main/resources/application-{dev,grey,prod}.properties` (common base828ef2e2). Preserve both features and default-off flags; no permissive auth fallback or new property values. Any actual conflict resolution must be explicitly listed and reviewed; report unexpected conflicts/scope changes before proceeding. All non-overlapping source bytes must be inherited exactly, including R01/OAuth correction and W06 tests.

No new product implementation, dependency changes, DB/Gradle/npm/build, service/ACL/config/secret/deployment operations or remote push. No new Agents without root-controller admission. Submit clean final commit/tree/parents and changed/resolved-path proof, then independent integration delta review. Freeze a new combined noDB selector on this final tree and run only after verification and shared-resource admission; old ac72/01037 wrappers are not GO for a different tree.

## Actual source integration proof

Clean final `1b3c7d0435d701c811716b8913bc824fb8934dec` / tree `cac8d686384b553f92a514e45bec95c71e6fe4ff`, parents1387ece25+fb2c7733. Intermediate `1387ece25c0a962a21abdc48e3e04e2acd8ab82e` / tree `451e5479f6c9ad396f7259ca79510a3bc8c0945b`, parents34b67fed+d875ccfa. No source conflicts or manual edits. Fifth shared path is `chat/jia-chat-service/build.gradle`: exact automatic merge preserves baseline voice dependencies and the accepted OAuth test-only dependency.

Coordinator independently reconstructed both merges with installed Git2.43.7 `merge-tree --write-tree`; both returned0 and their exact recorded trees. Independent blob proof: intermediate baseline-unique145/145, economy-unique302/302 exact; final differs from intermediate only in the three exact fb2c7733 test blobs, remaining3074paths exact. All three inputs are final ancestors. Hence final economy-unique299 remain source-exact plus three authorized test overrides; do not confuse this with302 unchanged final paths.

This is accepted exact source integration per the conflict-free merge policy; prior independent source reviews are reused, not a repeated full review. It is not compilation, runtime, packaging or deployment evidence. Final combined verification must use this exact clean tree after separate admission.
