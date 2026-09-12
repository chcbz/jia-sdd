# OD06 client retention gate (R03)

Origin: independent OD04 review of e609154; design.md requires configurable cleanup after server READY and business publication. Candidate currently creates archiveDir but never archives records or releases published local snapshots. This must be implemented and verified **before R1 integration acceptance/release**. It is deferred from the bounded OD04 recovery repair, not removed from scope.

Owner: sole critical client writer, serialized under OD06 before verification; independent architect/release review. Preserve source API/Web tasks and original checkouts.

Implement bounded, configurable local snapshot and completed-record retention. Byte cleanup requires confirmed publication; receipt/fingerprint/terminal recovery evidence must survive its required replay window, and blocked/incomplete/pending-terminal records must retain what recovery needs. Coordinate with the repaired inbox/ledger reconciliation so cleanup cannot cause model re-execution, discard an unsent terminal notification or delete another run's files. Handle interrupted cleanup idempotently and restrict unlink/archive to verified private queue paths.

Verify published-byte cleanup, pending/blocked protection, replay after cleanup without model invocation, restart during cleanup, and unsafe-path rejection; document defaults and override behavior. Record actual candidate/tests. Do not claim bounded disk usage or completed cleanup until implemented.

## OD06 implementation checkpoint

Sole writer `/root/od01_source_auth` is implementing from client29aa70da. Selected defaults are snapshot24h, completed output record7d, scan1h and batch100 transitions; record retention must cover the24h protocol replay window and snapshot retention. These are implementation choices awaiting candidate verification/review, not completed behavior.

Planned durability is exact-file cleanup under the existing run lock, persisted snapshotsCleanedAt, then queue-to-archive rename; both locations participate in exact immutable command evidence recovery. Only all-PUBLISHED plus terminalNotified records qualify. Review must cover interrupted cleanup, no-follow/cross-run protection, pending and corrupt protection, empty-directory removal, and replay both after byte cleanup and final archive expiry. Durable command dedupe/ACK evidence must still prevent model invocation after the output record expires.

## Development gate closed

Accepted714b4aa after independent repair approval; see `accepted-client-retention-714b4aa.md`. Earlier implementation checkpoints above are historical. Live R1 integration remains pending.
