# OD01 identity lock order — independent architecture clarification

Independent read-only architect decision, 2026-09-09. This checks compatibility with existing identity code; it does **not** accept the unfinished OD01 implementation.

Canonical order:

`business source root -> output_source_binding -> output_run_binding -> agent_persona_binding -> agent_identity_registry -> agent_runtime`

For TASK, lock `agent_task_meta` and then the exact authorized member row. For CONVERSATION, lock the exact persisted conversation owner row. A nonlocking run/runtime projection may discover keys; authorization rows must then be re-read and validated under the canonical lock order.

Existing API source establishes the required prefixes:

- `AgentStatusTransitionWorker` documents and implements binding, identity, then runtime.
- `AgentIdentityServiceImpl.activateForFirstRegistration` locks binding and identity before `AgentServiceImpl.register` locks runtime.
- `AgentLegacyTaskCompatibilityService` task assignment/report holds the task root before binding/identity authorization.

Two concrete draft hazards must be removed: issuance must not lock output source/run before acquiring the business task/conversation root, and capability/runtime authorization must not lock runtime before binding/identity. Both reverse existing mutation chains.

Registration, unbind and status transactions that already hold identity/runtime locks must not subsequently call source/run locking. Dynamic ticket rejection on inactive binding is sufficient for revocation. Any proactive run revocation needs a separate transaction beginning in canonical source/run order.

Required implementation evidence: barrier-driven concurrent dispatch/run creation versus ticket issuance, and registration/unbind/status versus ticket issuance/capability refresh. Assert bounded completion without deadlock and rejection of stale binding/runtime. The final read-only code review must verify actual callers as well as helper lock order.
