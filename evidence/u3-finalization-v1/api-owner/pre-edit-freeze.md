# MMD-U3-FINALIZATION-API-20260930 pre-edit freeze

Date: 2026-09-30
Owner/profile: `01a0f0d8-8202-7040-9d9c-becce02f7a3f` / `critical_worker`
Base commit/tree: `194ec91a596c28f9575a64aef47a5bf7b9fb6778` / `10d312e61057b1a83da1485238c2f3acf63e5361`
Frozen wire source: `/home/isp/wsps/cyf/evidence/u3-finalization-v1/frozen-contract.md`

## Event/API catalog

Public HTTP (exact):
- `POST /agent/tasks/{taskId}/finalizations`, mandatory `Idempotency-Key`, exact frozen request body, synchronous completed `200` or genuine pending `202`.
- `GET /agent/tasks/{taskId}/finalizations/{operationId}`, read-only.
- `GET /agent/tasks/{taskId}/finalizations/request`, mandatory original `Idempotency-Key`, read-only; route precedes `{operationId}`.

Internal Agent API:
- Trusted selected-output promotion accepts only server-validated owner/task/assignment/conversation source facts and bytes; it returns public recovery facts only.
- No producer/lease token, storage URI/path, Provider request, or caller-supplied run/work-item identity crosses the public HTTP boundary.
- Existing lease claim/start, artifact publish, formal submit, and owner decision services remain authoritative.

No new domain event is treated as proof of completion. `TASK_COMPLETED` requires persisted accepted formal delivery plus persisted completed task.

## Lock order

1. Chat finalization operation row (short local transaction only) for immutable create/CAS phase updates.
2. Release all Chat locks.
3. Read and validate conversation/request/step/execution/output and bytes without holding operation locks.
4. Invoke Agent trusted promotion/reconciliation; Agent acquires task/grant/work-item/lease/artifact/formal-delivery locks according to their existing service order.
5. Return to a new short Chat operation CAS transaction to record the acknowledged phase.
6. Invoke formal acceptance without any Chat lock, then persist the terminal Chat phase in a new transaction.

Never hold Chat/conversation locks across Agent root, private storage, artifact, submission, or decision calls. Never acquire Agent locks from an Agent transaction by calling Chat.

## Transaction boundaries

- Idempotency insert/fingerprint conflict and immutable selected-output rows: one Chat transaction.
- Each stage/state/error/version update: independent Chat transaction with expected state version.
- Source resolution and byte reads: read-only/non-transactional snapshot followed by exact hash/length/MIME validation.
- Agent promotion authority create/reconcile, lease authority persistence, and each phase fact: short Agent transactions; filesystem copy is outside DB locks and is reconciled by deterministic IDs/digests.
- Existing artifact publication, formal submission, and formal decision retain their own transactions. No distributed transaction is claimed.
- Replay lookup and committed-delivery reconciliation occur before stale task/assignment/lease rejection.

## Sensitive-payload allowlist

Persist/return only:
- owner scope IDs (`userId`, `clientId`, `tenantId`) internally; none added to receipt;
- operation/task/conversation IDs;
- expected task and assignment versions;
- immutable six-field selected outputs;
- source execution/run/output identity internally;
- SHA-256, validated MIME, byte length, owner-provided title/purpose/summary;
- deterministic artifact/manifest/delivery IDs and public delivery/task states;
- owner-safe error code and retryable flag.

Never return or log/persist in Chat operation payloads:
- lease token, provider credentials/request/response, authorization headers;
- private storage root/path/URI;
- arbitrary producer identity supplied by browser;
- raw selected bytes or unrestricted exception messages.
Lease token may exist only in the Agent-private promotion authority row for recovery and must be cleared after durable formal submission.

## Acceptance-to-test coverage freeze

- Happy path uses committed conversation bytes, actual lease claim/start, private artifact publication, formal submit, owner accept, and real task completion.
- Same key/same body replays immutable operation; same key/different body is `409`.
- Owner/client/tenant mismatch and forged task/conversation/request/step/output are denied/not found fail-closed.
- Stale conversation generation, task version, assignment revision, reassignment, and grant revoke fail before new side effects.
- Exact ordered selection, uniqueness, SHA-256, MIME, length, and byte content are validated.
- Recovery tests cover lost ACK after promotion, ready-to-submit, submission, acceptance, and terminal persistence.
- Known committed replay precedes obsolete version/lease validation.
- Both GET variants perform no writes or orchestration.
- Authenticated user authority is distinct from producer authority; token/storage secrets never appear in receipts.
- Schema tests require binary scope/idempotency constraints, additive DDL, FK/index/check validation, and initializer ordering before repository use.

Verification ownership: writer adds focused selectors and static checks only; main/gpt_test_runner runs Gradle after candidate commit.
