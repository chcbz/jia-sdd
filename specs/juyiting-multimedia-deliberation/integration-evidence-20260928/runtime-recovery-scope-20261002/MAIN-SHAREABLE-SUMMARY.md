# Main handoff — read-only capability and binding-15 recovery facts

Timestamp: 2026-10-02 (Asia/Shanghai)

## Release blocker: controlled image Provider

- Status remains **NOT_READY**. Do not install `api-full-enable-desired.NOT_READY.properties`.
- The existing installed route proves Responses/text and image-understanding access only. It is not evidence of authorization for image generation or editing.
- No authoritative generation/edit tuple was found: exact image endpoint, generation/edit model, Provider binding ID, positive epoch, operator policy/receipt, and dedicated credential custody are all missing.
- The deployed environment has no dedicated controlled-image credential, and the installed model catalog has no image-generation model entry.
- Required Main request: obtain one authoritative, non-secret Provider binding record for both generation and editing, plus separate custody of its dedicated credential. Do not reuse the existing Responses credential and do not run a paid probe before that record is frozen.

## Existing target inventory

- Exact owner scope contains 9 persona bindings, 0 `agent_hosted_profile` rows, and 0 ACTIVE hosted-profile rows.
- Four unhosted runtime rows are marked online; two Runtime-v1 installation rows exist but their last heartbeat is stale (2026-09-15).
- Local candidate remains binding 1 (`wuyong`), without changing its profile.
- No alternative existing ACTIVE hosted/server profile was found.
- Binding 15 (`gongsunsheng`) is currently SUSPENDED in both persona binding and identity registry; it has no runtime row and no `agent_hosted_profile` row.

## Binding 15: exact recovery-source finding

Binding 15 has a legitimate pre-existing **managed-hosting** lineage, verified read-only:

- exactly one current ACTIVE hosting lease for binding 15 and its exact canonical Agent;
- exactly one matching ACTIVE initial provisioning intent;
- the lease entitlement is currently valid;
- the intent references an enabled, non-expiring managed OAuth key with material present;
- key scope, managed key naming rule, description, intent reference, binding, and Agent all match;
- one root-owned mode-0600 managed claim exists and matches the exact tenant/client/owner/Agent scope;
- the managed claim contains only tenant/client/owner/Agent claims. It contains no hosted-profile generation, profile key, API-key row ID, or Provider binding;
- `codex-profiles.conf` has no section for binding 15's Agent.

No secret, credential digest, owner identifier, opaque Agent identifier, lease ID, intent ID, or key ID is included here.

## Does the minimum repair require creating `agent_hosted_profile`?

**Not for restoration through binding 15's original managed-hosting lane.** The current data proves that binding 15 originated from the paid managed-hosting state machine, whose free reprovision path uses the ACTIVE lease, ACTIVE initial intent, managed key reference, and managed runner. That path does not read or create `agent_hosted_profile`.

However, the separate endpoint `POST /agent/personas/bindings/{bindingId}/repair` is the hosted-profile publisher path. Its implementation requires an existing durable `agent_hosted_profile` row and fails closed when the row is absent. Therefore:

- calling that repair endpoint alone cannot recover binding 15;
- creating/adopting an `agent_hosted_profile` row would be an explicit migration into a different profile-publication lane, not a narrow "repair";
- authorization phrased only as "repair binding 15" is ambiguous and must not be interpreted as authorization to insert that row.

## Minimum exact authorization candidate

Prefer restoration of the original managed-hosting lane; do **not** create a hosted-profile row by default.

1. One exact-scope CAS transaction, only if all frozen source predicates still match: update only binding 15 from status `0` to `1`, and its same identity from `SUSPENDED` to `ACTIVE` with `suspended_at` cleared and `update_time` advanced; preserve binding/identity IDs, tenant/client/owner, Agent ID, persona, audit reason, provisioned/activated times, and every immutable field.
2. No new identity, no rebind, no lease/rental, no new credential, no new `agent_hosted_profile`, and no unrelated-row update.
3. Then one existing **free reprovision** request for that exact active lease/Agent, with a fresh idempotency key and expected lease version. Source code states this path performs no ledger posting and does not change price or paid period, but it does write a reprovision receipt and asks the managed runner to restore the runtime.
4. This requires separate authorization for the exact production DML/reprovision action and custody of the managed-host service. It is not covered by read-only investigation or by a generic hosted-profile repair approval.
5. Fresh CAS must re-check exact scope, ACTIVE lease/intent, valid paid-through, managed key validity, absence of a live reprovision, suspended binding/identity, unchanged managed claim, no competing ACTIVE binding for the same scoped persona, and no conflicting runtime/hosted-profile projection before mutation.

If Main instead chooses the hosted-profile publisher lane, authorization must explicitly say **migrate/adopt binding 15 into `agent_hosted_profile`**, identify the exact existing managed key to reuse, define initial lifecycle/generation/profile key, and address duplicate-lane risk. That broader migration is not the minimum supported by current evidence.

## Custody

The historical Client service Owner handle returned `agent not found`; this proves only that the Agent handle is unavailable. No service/process custody transfer was obtained. Do not stop, restart, signal, or modify any existing Client service until Main obtains explicit custody authorization.

## Actions performed

Read-only DB transactions with rollback, source/config inspection, and sanitized evidence creation only. No production DML, profile write, identity/binding mutation, Provider call, paid probe, service start/restart, or foreign-process operation was performed.
