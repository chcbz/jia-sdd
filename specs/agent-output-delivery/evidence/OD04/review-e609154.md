# OD04 independent review — REQUEST_CHANGES

Candidate `e6091542977edf7bc6860e804bede2fc4998baa2`, base `f8c731d0cef38956bb3dabaa628c6188c0040bed`. Independent read-only architect `/root/od03_independent_review`; no source edits by reviewer.

## Blocking recovery findings

**R01 — complete acknowledged remotely, local response lost.** `output-queue.mjs:500` persists VERIFYING only after PUT and complete return. If complete commits and its response is lost, persisted UPLOADING causes another PUT on restart; the API rejects PUT into VERIFYING/READY with409 and the queue marks BLOCKED. Existing response-loss test covered create only. Recover using explicit remote upload state or original completeKey replay, only restarting bytes when the actual API reports incomplete. Add a cross-instance/restart complete-ACK-loss case, proving one publication version.

**R02 — queue/inbox/ledger partial commits.** The durable queue is committed in `agent-client.mjs:4013` before runDrain transitions the inbox/ledger at2882. Three windows must recover monotonically:

1. queue committed, inbox still processing/ledger STARTED;
2. inbox delivery_pending, ledger still STARTED;
3. publication done and inbox completed, ledger still DELIVERY_PENDING.

Startup currently produces recovery_required or COMMAND_STATE_CONFLICT. A committed queue snapshot/model result must prevent model rerun, and become valid reconciliation evidence only after byte-exact commandId/runId/source/agentId/fingerprint matching. Add cross-process fault injection at each boundary; prove model-count1, unique output versions and terminal emission only after all outputs PUBLISHED. Existing restart fixture waited for pending transitions before exiting and therefore missed these windows. Keep unrelated/no-evidence recovery fail-closed.

## Reviewed boundaries and follow-up

No new blocker found in explicit API path-prefix support, WS URL derivation, reconnect ticket clearing/re-exchange, agentId profile isolation or ticket exclusion from model/command persistence. Successful npm footer283/283 was reconciled separately from the historical failed full log; this coverage does not remove the above defects.

**R03 — local snapshot retention**: archiveDir is created but unused; PUBLISHED/terminalNotified snapshots and records remain indefinitely. Root assigns this as an explicit **OD06 prerequisite before R1 acceptance/release**, not a forgotten nonblocking note. See `../OD06/client-retention-gate.md`.

Original sole client writer resumes only R01/R02 and their direct tests, then freezes a new candidate for the same independent reviewer. OD05 remains pending.
