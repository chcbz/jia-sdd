# GSS Runtime hosting control v1 — implementation contract

Frozen 2026-10-10 09:07 CST by Main for GSS-HOSTING-API-20261010 and GSS-HOSTING-RUNTIME-20261010. Changes require notifying both Owners; no fallback to the retired broker. This document is a development contract, not production evidence.

## Wire

Private AF_UNIX stream, UTF-8 one JSON request and one JSON response per connection, newline terminated. Protocol literal `runtime-hosting-v1`. `method` is `capabilities`, `prepare`, `ensure`, or `observe`. No credentials, paths, commands, provider data, or arbitrary URL accepted from API. JSON numbers use safe integer milliseconds/generations; all IDs are strings. Strict duplicate/unknown-field rejection; fixed validated configuration governs trusted socket permission and scope. Socket default `/run/cyf-agent-runtime-v1/unified/control.sock`.

`capabilities` request: protocol,method,tenantId,clientId,ownerJiacn. Response: protocol,method,tenantId,clientId,ownerJiacn,available(boolean),hostId. available means configured template/provider and control host ready for this exact scope, not merely socket exists. Probe occurs OUTSIDE DB transaction; prior successful idempotent submission may replay without it.

Every other request has protocol,method and the following FLAT association (responses echo all fields exactly):
- tenantId,clientId,ownerJiacn,canonicalAgentId,bindingId,leaseId,initialIntentId,operationId: exact strings.
- operationKind: `INITIAL` or `REPROVISION`; initial operationId equals initialIntentId.
- reservedAt,requestedAt: positive integer epoch milliseconds; validUntil: null for initial, integer lease expiry for reprovision.

`prepare` has only these fields. Runtime persists candidate/journal before responding. Repeated operation + identical association returns same candidate; mismatched reuse is rejected. Full subject serialization handles concurrent operation allocation.

Prepared response additionally has outcome=`PREPARED`, installationId (`rti_` +32 lowercase hex), manifest (existing RuntimeV1 format; includes sha256:-prefixed digest), manifestSha256 (BARE 64 hex), enrollmentSecretSha256 (BARE 64 hex), enrollmentExpiresAt (integer epoch ms), provisionGeneration (positive integer), hostId. Secret is only in Runtime private state, NEVER in response. API stores manifest digest BARE hex. INITIAL starts generation 1. REPROVISION uses same installation/manifest/auth and allocates one monotonically greater generation for the same subject; repeated prepare reuses its allocation. enrollment candidate metadata is retained for exact idempotent linkage, but REPROVISION does not reenroll or extend its expiry. Manifest version `1`, runtimeProtocolVersion `v1`; manifest only needs existing required identity fields plus computed digest.

`ensure` and `observe` additionally carry installationId,manifestSha256,provisionGeneration, matching prepared candidate. API sends ensure ONLY after transactionally authorizing/ensuring installation and binding it to the exact persisted initial intent; reprovision target generation also fixed transactionally. Observe does not activate anything. Initial prepare alone never enrolls or activates. Lost prepare/ensure response is recovered by identical calls, never by creating new order/payment/installation blindly.

Operation response has the association, installationId,manifestSha256,provisionGeneration,hostId,outcome. outcome is `UNKNOWN`, `RECOVERY_REQUIRED`, or `SERVICE_READY` (errors may return protocol,method,outcome=`REJECTED`,reasonCode only; never count rejected/error as no-effect/refund proof). UNKNOWN may include reasonCode. SERVICE_READY additionally requires runtimeInstanceId,sessionGeneration (positive integer), serviceReadyAt(epoch ms), registeredAt(epoch ms), executorReady=true,durableReady=true,evidenceRef(non-secret operation identifier). Both timestamps must belong to this operation and registration. API independently verifies current scoped installation/session/runtime identity with the same host/instance/generation; generic online row is insufficient.

## State / configuration

Only one existing RuntimeHost / service. Dynamic managed subjects must survive process restart; admitted dynamic entries reloaded from private journal, not arbitrary request-supplied config. Independent provider template explicitly configured with no inheritance of another user's HOME/private credentials. Template is configured locally by operator, never sent over socket. Runtime Owner documents exact config fields and writes source template/installer support; does not edit production config.

Per subject add/recreate must update RuntimeHost, execution adapter attached map, and engine entries/profiles; closed objects cannot be reused. Enrollment uncertainty stays RECOVERY_REQUIRED; never repeat a consumed secret. Free reprovision reuses valid installed authorization and requests a new session; no new enroll/charge. A failed new subject must not block heartbeat/registration for existing agents. Operation generation persists independently from runtime process/session generation. Server observes current host/executor/session rather than trusting old persisted READY after restart.

API migration: initial intent runtime_installation_id VARCHAR(100) NULL, runtime_manifest_sha256 VARCHAR(64) NULL, runtime_provision_generation BIGINT NOT NULL DEFAULT 0; reprovision runtime_target_generation BIGINT NULL. Scope/install unique where nonnull; schema/entity/mapper/migration consistent. CAS, exact owner/binding/lease checks and existing settlement maintained. Old managed_api_key_id audit retained but no legacy-key runtime fallback. Precise old key revocation is a separately explicit release step, not a blanket development DB change.

No new public API/UI; current GSS pending lease/intent/reserve continued. No production mutation/restart/payment as part of development. Root plan /home/isp/wsps/cyf/docs/implementation/GSS-UNIFIED-HOSTING-REPAIR-PLAN-20261010.md and handoff /home/isp/wsps/cyf/docs/implementation/handoffs/GSS-REJOIN-20261010.md define target and exclusions.

## Operator permission binding (09:12 clarification)

Read-only target identities: Runtime UID0/root, API user cyf-api primary group isp/GID1000. Control socket must grant the explicit trusted API group access (0660) and its operator-owned parent traversal (0750), no world bits. Runtime control config explicitly carries trusted numeric socketGid; API existing runnerUid0 remains meaningful. Do not silently chmod or adopt unrelated paths; installer/operator creates dedicated path. Existing service has no RuntimeDirectory, so source unit/config documentation must cover creation/recreation after reboot. Main will verify candidate config interoperability before release; no live changes here.
