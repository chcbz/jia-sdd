# R01 preparation — bounded implementation decisions

2026-09-05. Read-only architect `01a0707d-a85f-7d70-b282-6e62c5ee889e` inspected committed API `3249b587` and Web `42b6d804`. Recommendations are not implementation or acceptance evidence. Canonical execution status remains in TASKS.yaml.

## Main-controller decisions

- W03 acceptance is the explicit implementation dependency (now accepted). Subsequent user delegation approved preview plan v1: 1,000 SILVER per Agent per fixed 30 days; see `v0-hosting-rent.md`. Defaults remain charging-disabled and must not create new server-hosted instances for free.
- First bounded source slice: disabled-by-default configuration, protected quote admission, service-level server-mode guard **before** creating binding/runtime/profile, focused tests. Local/absent-body behavior stays compatible. This slice deliberately does not claim a paid lease/provisioning implementation.
- Reuse W03 monetary principal exactly: JWT `sub` actor, `jiacn` tenant, `client_id` client, no fallback. Architect's proposed `uid`/`token_kind` scheme is NOT adopted because it differs from the wallet contract.
- Amounts, versions, period seconds and epoch-millisecond timestamps remain canonical decimal strings, as in V0; the proposed RFC3339 change is NOT adopted.
- An idempotency replay returns the stored original mutation receipt; evolving provisioning/lease status is obtained by lookup, not changed replay responses.
- Renewal quote intent must be explicit and distinct from free active-lease reprovisioning; it cannot be inferred from `{}` plus an active lease alone. Freeze final DTOs before R02 integration.

## Concrete implementation boundaries

Existing `AgentServiceImpl#bindPersona(String,String)` creates/reuses binding before mode validation then calls `buildServerHostedBinding` (approximately 343 and 1298). Move mode admission before all binding mutation. New rent coordinator must use durable intent and after-commit filesystem preparation, then confirmed capture/refund; unknown preparation retains escrow. No generic outbox rewrite. Add separate additive hosting schema/initializer rather than altering W02 five-table catalog.

New-work admission call sites: `AgentServiceImpl#assignTaskInternal` (manual/automatic/legacy assignment), `AgentWorkItemLeaseServiceImpl` READY-to-CLAIMED, `HallActionDispatcher` TASK_INVITE/WORK_ITEM_EXECUTE, and `JuyitingAgentRelayService` direct/multi-target relay. Deny only new work for expired rent-managed leases; don't block resume/cancel/results or historical/local agents. Absence of lease is not itself proof of an authorized new free server binding: the bind gate must prevent that bypass.

Candidate API family: persona hosting-rent quotes; existing persona bind with explicit quote/price confirmation for server only; canonical Agent hosting-lease lookup; explicit renewal quote and renewal confirmation. No rental DTO is advertised frozen until documented in `v0-hosting-rent.md` and checked against existing response envelopes.

Next source Owner is critical_worker for admission/identity/transaction core; Terra owns frozen UI and ordinary integration. No deployment from this preparation handoff.

## Dependency refinement for parallel delivery

The first **non-charging admission-only** slice is tracked separately as `ECO-V0-R00`, based on accepted W02 in its own API worktree. It uses neither W03 wallet reads nor treasury issuance and does not modify W03 paths, so it may be implemented while W03 runtime verification runs. This is not acceptance of W03 or permission to implement the paid R01 flow early. R01's wallet dependency is unchanged; R00 receives its own independent verification/review. No capability is advertised as a working paid rental until full R01/R02/R03 integration.
