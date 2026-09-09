# OD02 storage fence — narrow independent review

Reviewer: existing independent read-only architect `/root/output_design_review`. Reviewed the abandoned-key protocol against the OD02 model at root `0d91958`; no product edits or Gradle commands. This is a design review, not storage test evidence or full OD02 acceptance.

**Blocking finding:** `writer_deadline_at + grace`, client socket cancellation, DELETE and HEAD-absent cannot prove that a previously accepted PUT will not commit later. Marking the job DONE and releasing physical quota based on those observations permits an unaccounted object to reappear.

The reviewer recommends the following minimal single-PUT repair:

1. Permanently unique epoch keys; every data PUT is atomic create-only (`If-None-Match: *`). The service controls the header; if a presigned URL leaves the process, its signature must also bind that header.
2. Abandonment cleanup overwrites the exact key with a zero-byte service tombstone whose metadata binds the stable cleanup identity. It does not leave a deleted, writable key.
3. Strong-consistent HEAD must confirm the exact key, zero size and matching cleanup token. Only then can a scoped SQL CAS mark DONE and release that job's charge once. Failure or uncertain response retains durable retry state and charge.
4. Keep tombstones and never reuse their keys. Bucket lifecycle must not delete these fences or retained files. Versioning must be disabled; overwriting a versioned object would retain charged historical bytes.
5. Storage calls stay outside SQL transactions. Finalization rechecks job/epoch/key/charge in the consistent quota/upload/job lock order.

Required real-MinIO and production-adapter checks: slow/paused old PUT against tombstone; old PUT first then tombstone; replay of the old PUT after DONE; lost tombstone acknowledgement and retry; nonzero or wrong-token HEAD; PUT/HEAD failure; exact transfer and once-only release of the old epoch's physical reservation; rejection of incompatible bucket versioning.

MinIO's atomic conditional-write behavior must be demonstrated for the installed version. If that check fails, the single-PUT implementation cannot claim this fence; the reviewer identified server-owned multipart completion plus durable abort as a fallback requiring separate implementation and verification. The current writer is testing the single-PUT path first.

The finding remains open until implementation and real storage/quota evidence close it. Unrelated OD02 schema, authorization, scanner and fixture work continues under the existing sole writer.

Reviewer clarification: the current epoch may become READY and transfer its own base reservation to stored bytes while old jobs independently retain their charges. There is no added requirement to wait for every old job before READY. Final READY-object GC uses the same tombstone fence. R1 rejects Suspended buckets as well as enabled versioning; use a private bucket that has never enabled versioning. Permanent tombstones retain object metadata cost even with zero content bytes; normal GC does not reclaim them. A future reclamation design would need a stopped-writer maintenance boundary that proves every old writer is invalid.

Subsequent protocol evidence: `minio-protocol-execution.md` and `minio-protocol-probe.json` record a real-MinIO probe. The same independent architect found it sufficient to remove the single-PUT feasibility uncertainty for the tested version. This narrows the open finding to production adapter behavior and application cleanup/quota correctness; it does not close the full OD02 gate.
