# OD02 in-progress GC/recovery review

Independent read-only reviewer: `/root/output_design_review`, architect (GPT-5.6 Sol High). Review completed 2026-09-10; root reread the DAO on 2026-09-11 and confirmed the three findings remained in the current draft before handing repair to the resumed sole writer. This is not frozen-candidate approval.

## Blocking findings

| ID | Finding | Required repair and observable result |
| --- | --- | --- |
| G01 | `retryObjectDelete` sets DELETING back to READY after a storage/HEAD failure. Tombstone PUT may already have succeeded, so the object can be offered for new references with destroyed bytes. | Keep DELETING; clear/renew only the worker lease and retry schedule. A tombstone-success/HEAD-failure test must leave the object unavailable, then recovery finishes once. No transition back to READY. |
| G02 | `findDueObjects` selects only READY and `findDueCleanup` only PENDING. A process failure after DELETING/CLAIMED leaves durable work and quota stranded. | Due selection plus claim CAS must reclaim expired DELETING objects and CLAIMED jobs. Restart using a new service/worker must complete the existing jobs without a new upload/complete operation or repeated charge release. |
| G03 | `finishCleanup` marks the shared object DELETED when any epoch job completes; it does not compare that job's storage key/version with the current object byte identity. | Only completion of the exact current object's bucket/key/version fence may mark that object DELETED. Old epoch completion releases its own charge only. Test old cleanup first, current key still pending, then current-key cleanup. |

No confirmed double quota subtraction was found: finish CAS and quota delta share a transaction, so a failed later CAS rolls back the earlier delta. This does not close crash recovery or premature lifecycle transitions.

## Reference locking seam for OD03

The exact `(tenant_id, client_id, object_id)` object row is the serialization point. GC locks scope quota then object, checks effective retention references and transitions to DELETING in the same transaction, before network I/O. Every reference mutation must participate in that object lock protocol; new or extended protection requires current PASSED/READY and exact scope/byte identity. The existing reference count is retention evidence only and must never grant read ACL.

Cleanup finalization should consistently lock `scope quota -> object -> cleanup job`. The separate cleanup claim transaction may lock only the job and commit before storage operations. Existing shared quota locking avoids a certain current deadlock, but using a different suffix would be brittle for OD03's object/reference mutations.

Minimum remaining real-MySQL proofs: publication/reference-create versus GC; READ_PIN lifecycle versus GC; restart after CLAIMED/DELETING; successful tombstone with failed HEAD; old/current epoch ordering; competing recovery workers release each charge exactly once. Current sequential direct-SQL reference insertion proves static retention counting only. Production reference APIs remain OD03 work; OD02 must establish and exercise their reusable object lock protocol.

Reviewer reported snapshot hash prefixes: DAO `e14a1def`, DAO impl `5d95c409`, service `1cb29fd`, DDL `034edf2a`. Test source changed during review, so its reviewed contents were not frozen. No reviewer file edits, scans, services or Gradle commands occurred.

## Clarification: removing protection remains allowed after deletion starts

The reviewer independently confirmed on 2026-09-11 that only creation or enhancement of protection requires PASSED/READY. Release, expiry with no hold, and clearing hold still lock object then exact reference, but may run with READY/DELETING/DELETED. They must only shorten or remove protection, never extend retain time, revive a terminal reference or rebind source/object/version. This avoids stranded historical pin metadata while retaining GC's irreversible lifecycle decision. Expiry rereads exact identity/state/hold/deadline under lock; a missing object row is a consistency error, not permission to skip locking.
