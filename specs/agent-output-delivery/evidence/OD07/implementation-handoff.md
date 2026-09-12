# OD07 queued implementation handoff

Status: OD06 independently accepted for development; OD07 API slice is active under claim.md. Use the accepted OD06 descendant when this task is claimed; do not overwrite concurrent API integration changes. Canonical packaging and physical-device release gaps must remain explicit if development later proceeds before those external gates close.

Implement the already reviewed contracts in detailed-design.md section9, openapi.yaml lease routes, schema-contract.yaml and execution-plan.md section6. Reuse AgentWorkItemLeaseServiceImpl and its existing root transaction/CAS/event machinery. Its configured maximum lease duration is900000ms; the planned120000ms lease and40000ms heartbeat fit that bound. The old interface does not expose the specified ticket-bound recovery GET; add it without leaking another run's leaseToken. Bind the dispatched run to the work item, and validate executionRunId at claim/start/heartbeat/release/submit, including restart and old-run attempts after CHANGES_REQUESTED.

API source pointers below are relative to the API repository:

- `agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentWorkItemLeaseService.java`
- `agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentWorkItemLeaseServiceImpl.java`
- `agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentTaskCreateDTO.java`
- `agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentController.java`: create, assign, auto-assign and report routes.
- `agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentLegacyTaskCompatibilityService.java`: assignResolvedVersioned and reportResolved are shared legacy mutation entrypoints.
- `AgentWorkItemResultCommitServiceImpl`, `AgentTaskStateServiceImpl`, `AgentTaskAggregationServiceImpl` and `AgentServiceImpl` in the same service/impl directory: inspect result, direct status and aggregate completion writes.

The full policy1 gate must include newly merged funding services; see ../OD06/integration-baseline-watch.md for exact classes and service calls. Preserve policy0 funded behavior. Reject unsupported policy1+funded combinations before any financial mutation, with database evidence that task, funding and event rows remain unchanged. AgentController selects funding when any of grossBountyAmountMicro, settlementPolicy or requiredSkillRequirements is nonnull; an empty requirements array also selects that path. OD10 must preserve the intended request shape.

Do not expose policy1 creation before all legacy/direct completion and multi-member/work-item bypass guards are installed. New schema must retain strict fresh/upgrade/partial-state validation. Prove stale lease, wrong run, same-agent different run, concurrent reassignment, unsupported capability and funded-path rejection against actual MySQL. Preserve policy0 regressions. Serialize client heartbeat with submit, stop and await any in-flight heartbeat before using the last returned version; do not treat409/412 as permission to continue.

Keep API and client edits serial with a frozen handoff between repositories. Each Gradle invocation holds /tmp/cyf-gradle.lock. Run the affected checks once, archive their original reports immediately, then obtain an independent read-only review. Do not rerun unaffected passed checks merely to refresh timestamps or produce a new test count.

OD06 exposed a source-creation integration gap that seeded authorization fixtures missed: generic conversation creation wrote tenant0, while output authorization correctly required the exact owner tenant. For OD07 positive lifecycle coverage, create the source through its real authenticated service entry before claiming/dispatching/submitting; do not use a manually idealized source/run row as the only proof that the entry and authorization contracts connect. Retain explicit raw fixtures for negative/corrupt-state tests.

## Client handoff preparation

Preparation only; API freeze and independent acceptance still precede client edits. Source locations below are relative to the client repository at714b4aa:

- `conf/codex-ws-agent/agent-client.mjs`: normalizeAgentMessage already carries explicit taskId/workItemId and validates outputContext; registration/presence currently advertise only R1. The execution finish hook snapshots files, queues publication and defers command terminal notification. Connect claim/start before execution and preserve the distinction between publication and formal submission.
- `conf/codex-ws-agent/output-manifest.mjs`: outputContext has strict seven-field validation and a two-item R1 capability allowlist. Extend supported capability validation deliberately, keeping source/envelope equality and manifest path checks. Use the trusted context's task.delivery-http.v1 capability to select policy1; do not add an undocumented policyVersion field or infer it from ordinary runtime capability alone. Reject delivery capability on conversation sources or without explicit task/work-item identity.
- `conf/codex-ws-agent/output-queue.mjs`: authenticated HTTP request/retry, per-profile persistence, run locks and terminal reconciliation already exist here. Reuse their ticket boundary and secret handling; do not assume a separate output-http module exists. Lease work-item versions remain decimal strings, unlike locally bounded file byte sizes.

API wire gate: AgentCommandTransportCapture must carry the same trusted workItemId from the sole required assigned item into AgentCommandDraft and its durable wire; binding only output_run_binding is insufficient. AgentCommandCanonicalCodec must accept the canonical R2 capability list with its required identity. Verify actual capture/codec/outbox output and client normalization, preserving the existing R1 wire. Root observed both connections incomplete during implementation and notified the writer; completion evidence remains due.

Client lifecycle checks should cover claim/start before invoking the model, no execution after rejected/unknown acquisition, one serialized heartbeat in flight, shutdown before submit using the latest acknowledged version, stable key/body through uncertain responses, and same-binding new-runtime upload recovery without recovering the old runtime's active work lease. A valid no-op heartbeat is not automatically a product error; the synthetic Root probe intentionally requires expiry advancement and has a narrower acceptance boundary.

Keep task.delivery-http.v1 registration default-off until the R2 submit/recovery path is implemented and verified. An explicitly enabled isolated development fixture may exercise OD07 lease handling, but ordinary registration must not claim full delivery capability after lease-only implementation. OD08 owns durable formal-submit integration and real inline text handling; do not manufacture an attachment or report task success merely because output publication completed. The existing R1 fixture file stays byte-identical; consume lease-fixtures.json separately and retain its source hash in the client evidence.
