# OD07 queued implementation handoff

Status: preparation only; OD07 has not started. The sole writer is still executing OD06 live R1 integration. Use the accepted OD06 descendant when this task is claimed; do not overwrite concurrent API integration changes. Canonical packaging and physical-device release gaps must remain explicit if development later proceeds before those external gates close.

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
