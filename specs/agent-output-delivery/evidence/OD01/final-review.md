# OD01 independent final review — CHANGES_REQUIRED

Reviewed candidate: `8e009b9d241979abb072d4b5b12d42b0476450dc`, against `f418e3f5bf7afcdbddf9c1ecec1b293f657c977c`.

Independent read-only reviewer: `/root/output_design_review`. The reviewer changed no files and ran no Gradle command. The original writer is now responsible for a bounded repair and a new candidate; OD02 remains unopened.

## B1 — command bytes rewritten after durable capture

`chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java:1093` enriches and reserializes the supplied raw command bytes during WebSocket delivery. This violates the explicit byte-exact contract in `agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentRawCommandDispatcher.java:6` and separates delivered bytes from durable outbox/inbox `wire_payload` and hash.

Establish trusted context before canonical wire capture/hash; send supplied bytes unchanged. Preserve task root/member → output source/run → identity/runtime → delivery/outbox lock order. The current assignment path already holds runtime locks before its late `captureTaskInvites` call, so mechanically moving enrichment to that call is insufficient.

New policy-0 commands without fresh output capability must preserve legacy execution. A terminal, revoked or expired same-origin run must not be downgraded into another no-context execution. Already persisted output-aware commands must never have their context stripped during transmission.

Required verification: persisted wire/hash equals exact WebSocket bytes with output enabled; repeated delivery preserves run/context; relevant canonical codec/capture/raw-dispatch behavior remains valid.

## B2 — receiving runtime is not selected by dispatch authorization

Run creation validates the current database capability snapshot, but task/direct/conversation delivery can send its output context to another still-open registered session. That stale runtime can receive output-aware work it cannot authorize.

Select only the exact current registered runtime whose fresh capability snapshot authorized the output-aware dispatch. Keep runtime selection internal where possible; original runtime remains audit metadata, and same-binding recovery on a newly authenticated runtime remains supported.

Required verification: multiple registered sessions cannot deliver output-aware work to stale/wrong runtime generations; current runtime receives it; task and conversation paths are both covered; policy-0 legacy delivery is retained.

## B3 — ticket reissuance incorrectly uses dispatch freshness

`agent/jia-agent-service/src/main/java/cn/jia/agent/output/service/OutputRunAuthorizationServiceImpl.java:118` uses `requireFreshRuntime` and rechecks the 90-second capability lifetime during ticket issuance. The contract applies that lifetime to creation/dispatch, not bearer recovery.

Split current authenticated runtime generation/binding checks from dispatch-freshness checks. Same active binding/current registered generation can reissue after capability age exceeds 90 seconds. Changed generation, changed binding and revoked authorization still reject; terminal reissuance remains status-only.

Required verification: stale-capability same-generation reissuance succeeds; dispatch freshness remains enforced; terminal and revocation boundaries remain intact.

## Evidence and next gate

Candidate/source association is closed separately: the frozen candidate passed seven authorization unit tests and six real MySQL tests with no failures/errors/skips; see `candidate-8e009b9d-test-results/observation.json`. Those results do not override the three findings.

The original writer owns all three repairs and the affected targeted tests. Each Gradle test task holds `/tmp/cyf-gradle.lock` and archives its XML before the next task. A new committed candidate must receive independent read-only re-review before OD01 is accepted for development or OD02 starts. Canonical packaging and actual production topology remain OD06/OD11 gates.
