# Finalization/publication narrow remediation — 2026-09-05

This is a bounded correction contract, not runtime approval or second ledger. Both new review failures were attributed (count1), no selectors run.

## HOST R5, original owner Shannon3
R4 c175de689a228bcb4c98aa06748c7069ec5a7c05/treeada9241e1745c93ae1945d38f24b2bddd209d438 rejected0/1/0 by01a0721e. STOP_RECORDING handler tries ABORTED then MANUAL, suppresses both failures, calls finalize unconditionally. Finalize currently allows nonterminal PREPARED/STOP_ATTEMPTED to become0444.

Correction: finalization must centrally reject any nonterminal record before chmod/immutability and must not claim completion when terminal publication fails. Repeated receipt I/O failure leaves explicit recoverable/manual state and error, never immutable nonterminal, without invoking lifecycle before actual stop boundary. Do not promise a durable record when storage cannot write. Check all callers of the central finalizer, not just happy path; preserve terminal truthfulness elsewhere. Tests: each of three drivers initial before/afterreplace fault combined with both ABORTED and MANUAL recovery publication failures, assert zero lifecycle, unchanged selected/runtime bytes and nonterminal NOT0444, explicit failed/manual observable result. Also direct finalizer terminal allowlist rejection regression.

Owned scope: same HOST five-path R4 slice; common/canonical/isolated curl fixture unchanged. Static-only candidate then fresh narrow review. No new transaction architecture, production/build/selector.

## Web R3, original owner Shannon5
R2 9b0e1af3f39be8c74aab7a5bec9efa2ded7deb1c/treed292348558cd04fc1135245fa9b93cfa2f48cd5f rejected0/1/1 by01a07199. Helper724–769 child linked flag and special rc92 cannot attest publication/withdrawal durability; final-link-before-feedback and cleanup-unlink-before-dirsync failure can produce stale durable success after live rollback.

Correction: on ANY publication failure parent must reconcile final record/sidecar and integrity, not trust child flags/exit92 alone. Treat uncertain durable withdrawal/unknown commit as requiring preserve of matching healthy live and explicit manual recovery; do not rollback matching live behind a potentially durable successful record. Make parent commit-attempt boundary explicit before child publication and validate facts used for recovery decisions; if absence cannot be proved durable, do not infer it from pathname absence. A minimal conservative preserve-after-commit-attempt strategy is permitted if stated truthfully and parent reconciles record/sidecar facts; no fake success. Do not try to guarantee durable recovery while fsync is failing.

Tests must hit actual code: link success before child feedback, final-record cleanup unlink failure, sidecar cleanup unlink failure, cleanup directory fsync failure, for deploy AND rollback. Assert exact live/backup/rescue bytes and terminal/recovery evidence without flaky sleeps. Preserve all already-closed Python/environment/dependency-hash/recovery/proof/guard/handshake findings. Only original six Web paths, no common edit. Same static->fresh independent review->final merged-tree selector dependency. No production/proof placeholders.
