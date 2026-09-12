# OD06 client retention development acceptance

Independent read-only `/root/od05_review_fallback`: **APPROVE** on `714b4aa73b474b37ec6348d045b653a3ca273cf2`, following initial candidate18705d2 and accepted OD04 base29aa70da.

All3 findings closed: active delivery lock contention uses local backoff without modifying another processor's durable record; missing/mismatched command evidence is isolated before deletion with bytes preserved; dangling run-directory symlinks produce OUTPUT_RETENTION_UNSAFE_PATH and no success/archive markers. Original independent counterexamples were rerun and behavior checked. Full client305/305 passed; queue23 and recovery7 overlap this total. Syntax/diff passed. Root verified both changed-file hashes against worktree, post-test manifest and Git blobs; exact evidence and limitations are in `client-retention-714b4aa/observation.json`.

Retention defaults are published snapshot24h, completed output evidence7d, scan1h and batch100, configurable with strict bounds. Pending/blocked/unsent-terminal and corrupt records preserve recovery material. Exact-file deletion, empty-run-directory removal, durable archive markers and interrupted cleanup are tested. The cross-process real delivery-pending test exercises publication/terminal finalization, archive and expiry with delete-policy inbox; persistent command ledger/ACK evidence prevents model re-execution after final output-record deletion. Existing command dedupe ledger lifetime is unchanged; this is not a total client-disk bound.

Client retention prerequisite is accepted for development. OD06 now continues with API reconciliation/build/text-file preview, then live integration and release assessment. R1 as a whole remains unaccepted; no live browser/Agent-offline/physical-device or deployment claim.
