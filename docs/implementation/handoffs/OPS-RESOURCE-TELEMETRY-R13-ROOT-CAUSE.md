# OPS-RESOURCE-TELEMETRY R13 Root-Cause Matrix

Date: 2026-08-29

Rejected exact candidate:

- Commit: `e55fe220ae59ca21943e4ffb04f9dfd0712bc766`
- Tree: `ca2ddc6fcd096248563472fcf61b58d818e5736a`
- Parent: `3ecc02ff2e958758b5ec8c04fa76d4c6d3a28f5d`
- Authoritative reviewer: `01a04d43-3510-7150-8c27-05288e766859`
- Verdict: `REJECT P0/P1/P2=0/3/0`

This is a repeated authoritative rejection after R12. R14 implementation is forbidden until a fresh read-only architecture pass supplies a bounded state-machine design addressing all three rows together; no local patch-by-patch retry is authorized.

## Failure matrix

| Symptom | Root cause | Required R14 design property | Required adversarial proof |
|---|---|---|---|
| The new safety anchor can itself be unlinked, moved or replaced after a pathname pre-check. If recovery is also absent, the held ordinary fd may be the only reference and reconstruction may fail after `nlink=0`. | The supposed safety primitive is still represented by a mutable pathname inside an attacker-writable namespace. Its identity is observed before use rather than protected by a trusted namespace or a primitive whose lifetime is bound to the held descriptor. | The last recoverable exact-original reference must live in a parent-fd-bound namespace that the modeled contender cannot rename/unlink/replace, or use a proven Linux primitive that can reconstruct the exact inode even after all visible links disappear. The implementation must explicitly state and enforce the trust/permission boundary; a pre-check on an ordinary pathname is insufficient. | Deterministically replace/unlink/move the anchor during every validation/use window while recovery and active are also contested. Prove exact original is never lost, all foreigns are preserved, and same nonce converges after contention releases. Include the `nlink=0` boundary or prove it is structurally impossible. |
| Active is validated exact with anchor present, then active can be replaced/unlinked before or around anchor removal. Removing the anchor can drop the original to zero links; the post-check only terminates. | Finalization is a multi-step check-then-unlink sequence with no atomic commit point and no recovery loop after the last-reference operation. | Define a finalization protocol whose commit point cannot delete the last exact link unless active remains the exact inode, or that can always roll forward from the held trusted reference. Post-finalization mismatch must re-enter convergence rather than terminate with poisoned state. | Inject active replace/unlink/move before, during and immediately after final anchor removal. Prove exact active `nlink=1`, no exact alias residue, every foreign quarantined, and immediate same-nonce reload/consume. |
| Moving an exact alias into `.quarantine`, a child directory, or another same-filesystem parent leaves `st_nlink` above the enumerated alias count. The cleanup loop sees `nlink != 2` forever even after contention stops. | Alias discovery scans only selected top-level namespaces and intentionally skips quarantine; the state machine assumes every hard link is enumerable, which is false under the modeled cross-parent move capability. The loop has no bounded terminal classification. | Eliminate correctness dependence on enumerating all hard links, constrain exact-link creation/movement by a trusted namespace, or define a bounded fail-closed terminal that preserves retryability without spinning. No unbounded `while True` may depend on unexplained `st_nlink`. | Move recovery/anchor exact aliases across parents, including quarantine and nested directories, then stop contention. Prove bounded convergence or a retryable fail-closed terminal within a fixed iteration/time bound; never infinite loop, last-reference loss, or silent residue. |

## Architecture questions that must be answered before R14

1. What exact directory/permission boundary is trusted against the modeled contender, and how is it verified by parent fd identity and ownership/mode?
2. Which Linux primitive binds the retained exact inode across namespace races (`O_TMPFILE`, `linkat(AT_EMPTY_PATH)`, trusted hard link, rename exchange, or another mechanism), and what are its kernel/filesystem/error semantics here?
3. What is the single finalization/commit protocol, including every rollback/roll-forward transition?
4. How is cross-parent hard-link movement handled without global filesystem enumeration?
5. What fixed bound terminates persistent hostile contention while preserving a subsequent same-nonce retry?

## Exact scope and gates

R14 may modify only after architecture acceptance:

- `ops/orchestration/cyf_orchestrator.py`
- `ops/orchestration/tests/test_cyf_orchestrator.py`
- `docs/implementation/README.md` for exact trust/state-machine wording.

`ops/orchestration/cyf_evidence_envelope.py`, product source, Gradle/DB/Rabbit, production, process control, runtime ledger edits by the Writer, and deletion of prior evidence remain forbidden.

Promotion requires focused adversarial coverage for all three rows, selected and full orchestration suites, checks, a clean exact commit/tree, immutable evidence, and a fresh independent Review.

## Architecture decision (2026-08-29 19:50 CST)

Fresh architect `01a04d4a-bb58-7fc1-95dd-36aa6ad617ac` proved that the former same-UID, full-capability contender model cannot simultaneously guarantee exact active `nlink=1`, deletion of the last anchor, and recovery after arbitrary post-commit unlink. The control plane therefore accepts the minimum explicit trust-boundary revision for R14:

1. recovery uses a pre-provisioned same-mount private sibling directory opened and verified by parent fd; product code never creates it lazily;
2. the modeled contender runs under a distinct credential/mount domain without `CAP_DAC_OVERRIDE`, `CAP_FOWNER`, ptrace/setns/fd access to the controller, and cannot mutate the private recovery namespace or the committed controller-owned active;
3. the only semantic commit is `renameat2(..., RENAME_EXCHANGE)` from the trusted exact anchor to an occupied active name; there is no final unlink of an exact anchor;
4. unexplained `st_nlink > 1` becomes a bounded retryable `RECOVERY_PENDING_UNKNOWN_EXACT_LINKS` terminal rather than filesystem enumeration or an infinite loop;
5. all namespace contention shares `RECOVERY_CONTENTION_BUDGET=64` with no nested unbounded retry;
6. code acceptance requires deployment evidence that the private sibling is same-mount, physical, root/controller owned `0700`, and inaccessible to the unprivileged contender. Same-UID full-root contention is now an explicit `UNRECOVERABLE_TRUST_BOUNDARY_BREACH`, not an advertised auto-recovery case.

R14 is authorized only against this revised, testable boundary. The Writer must not claim safety against another unrestricted host root process.
