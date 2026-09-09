# OD02 internal model alignment

This records implementation decisions, not passing test evidence or OD02 acceptance. The public OpenAPI and canonical fixture remain unchanged. The source of truth for exact columns is `../../schema-contract.yaml`.

Agreed with the sole API writer:

- Keep the five upload/object/scope-quota/reference/receipt tables. Add binding quota, cumulative run upload quota and durable per-epoch cleanup rows; add upload verification and object deletion retry/lease fields.
- Each epoch has a fixed ten-minute `writer_deadline_at`; renewable five-minute `writer_until` never exceeds it. The upload session retains its independent create-time 24-hour expiry.
- Create requests are bounded even when empty or never uploaded. Successful create counts once, replay counts zero; each epoch charges attempted bytes. Default cumulative limits are ten times the run file/byte limits.
- A retry does not reserve the business file twice. It does reserve each additional physical staging copy until cleanup confirms removal. Transfer reservation ownership to the abandoned job atomically; do not release it on rejection alone.
- Commit a HELD cleanup row with the epoch before external PUT. Preserve the current successful immutable key as RETAINED. Do not configure bucket expiry on these keys. Use single PUT, with no automatic SDK multipart upload.
- Use a scoped non-null SHA-256 cleanup identity instead of a nullable or oversized composite storage-key index. Persist the complete storage identity. Lease owner columns are bounded binary identifiers.
- `completeUpload` hashes a server-owned canonical run/upload/operation envelope. Authentication and current receipt matching remain inside the mutation transaction, after OD01 source/identity locks.

Pending narrow independent architecture check: a cancelled client socket followed by a fixed grace period and DELETE/HEAD does not itself establish that the object server cannot later commit an earlier PUT. `safe_after` is a scheduling bound only. The storage fence and cleanup-release proof must be resolved in the implementation and tests before OD02 approval. The writer continues the remaining schema, service and fixture path while this check runs.

No production installation, migration or deployment is authorized by this model note. Local dependency substitutions retain the OD00 limitations.

Control-plane checks: YAML parsing, all 15 tables' primary-key/index column references and non-null primary keys, and `git diff --check` passed. The fixture digest remains `453968ce85423aaf091e81d8600f2959fc44efca66793637927a06da54e48f6f`. These checks do not execute the DDL or prove concurrency behavior.
