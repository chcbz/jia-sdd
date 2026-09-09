# ClamAV scan-limit configuration review

Independent read-only reviewer: `/root/output_design_review`, architect (GPT-5.6 Sol High), 2026-09-10. This is a narrow infrastructure/configuration review, not final OD02 code acceptance.

## Finding and required repair

Installed ClamAV 1.4.3 documentation states that `AlertExceedsMax` defaults to `no`, files above `MaxFileSize` are skipped, and recursive scanning stops at `MaxScanSize`. A ZIP within the application's 200-MiB expansion bound can exceed this installation's 60-MiB member or 100-MiB aggregate scan bound. A response of OK must not imply complete scanning when a limit was reached.

Reviewer requires `AlertExceedsMax yes` as an OD02 local acceptance prerequisite. Keep the tighter limits and reject files beyond scanning capacity. The adapter treats `Heuristics.Limits.Exceeded... FOUND` as unclean, preventing READY; the UI's more specific limit wording can be refined separately.

Local official sources:

- `/home/chc/.local/share/cyf-output-tools/services/clamav/usr/share/man/man5/clamd.conf.5.gz`
- `/home/chc/.local/share/cyf-output-tools/services/clamav/usr/share/doc/clamav-daemon/examples/clamd.conf.sample` (AlertExceedsMax around line 692)

## Local action

Root held `/tmp/cyf-gradle.lock`, backed up the task-owned configuration outside Git, preserved the verified daemon executable/argv/environment/cwd, stopped it gracefully and restarted with `AlertExceedsMax yes`. Readiness at `2026-09-09T22:17:27.368531+00:00`: PING `PONG`, VERSION `ClamAV 1.4.3/28118/Wed Sep 9 14:24:03 2026`, loopback port 13310. No production service was modified.

The initial pre-change large ZIP probe exceeded its 30-second socket timeout and produced no result file. It is inconclusive, not bypass or safety evidence. The replacement probe persists each case's progress/error and allows 180 seconds per socket operation to cover the default 120-second scan limit. Protocol observations are kept in `clamav-scan-limits.json` when completed; they do not prove application state transitions.

OD06 must independently verify the actual deployed scanner configuration and scan-limit behavior. Small clean/EICAR evidence obtained before this change remains valid for those inputs only.

## Post-change protocol observation: NOT_PASSED

Command: `python3 specs/agent-output-delivery/tools/probe-clamav-scan-limits.py --output specs/agent-output-delivery/evidence/OD02/clamav-scan-limits.json` (root repository). Exit code 1.

- Clean 13-byte input: OK.
- Standard EICAR: FOUND.
- ZIP containing one 61-MiB zero-filled member: **OK**, contrary to the expected explicit limit rejection (36.848 seconds).
- ZIP containing two 55-MiB zero-filled members: `Heuristics.Limits.Exceeded.MaxScanSize FOUND` (37.919 seconds).

Daemon startup log confirms archive scanning, heuristic alerts and scan-limit alerting are enabled. Configuration presence is insufficient to close this gate. The single-member result remains under independent investigation; it is not proof that an EICAR-bearing archive would bypass scanning. No unscanned-file safety claim or OD02 acceptance is made.

A supplemental INSTREAM framing check announced one `60 * 1024 * 1024 + 1` byte chunk (command plus network-order length header, no body sent). clamd immediately returned `INSTREAM size limit exceeded. ERROR`. This proves early rejection of an oversized announced chunk only; it is not a transmitted 60-MiB payload or application failure-state test.

## Independent defensive resource review and selected repair

The expanded boundary investigation was interrupted by the review tool. The follow-up was limited to defensive bounded-resource design; the architect confirmed feasibility and provided the source references below. No code acceptance or repaired execution is claimed by that review.

Selected application policy (implementation pending):

- Each actually expanded member: at most 50 MiB.
- Shared whole-tree byte budget: at most 90 MiB, **including the root uploaded object and every member's expanded bytes at every level**. ClamAV counts an archive plus its extracted contents; do not reset this budget per nested archive.
- At most 2048 entries across the tree; root ZIP depth 1, maximum depth 3.
- Recursively inspect ZIP magic (including OOXML); reject recognized other unsupported compression/archive formats, encryption, invalid structures and unsupported methods. Declared entry sizes are not authoritative.
- Stream counters with checked arithmetic. Spool only a nested ZIP member, bounded by the shared budget, to a private 0700 directory and random 0600 file. Never extract paths from entry names. Use depth-first traversal and delete files promptly; avoid aggregating expanded contents in heap.
- Deterministic format/limit failures reject; temporary I/O failure remains VERIFYING for recovery. Both execute outside SQL transactions and before the final READY mutation.
- Keep external scanner verification mandatory and `AlertExceedsMax yes`. Configurable application byte bounds and effective daemon bounds must be checked together at OD06. The 200-MiB run business quota is unchanged.

Reviewer source references: ClamAV tag `clamav-1.4.3`, commit `d8b053865fd5995f7af98bfbcd98c9a5644bfe2b`:

- `https://github.com/Cisco-Talos/clamav/blob/clamav-1.4.3/libclamav/unzip.c#L217-L240`: the DEFLATE path maps an exceeded output bound to stream end; the temporary result is scanned later (lines 345–359).
- `https://github.com/Cisco-Talos/clamav/blob/clamav-1.4.3/libclamav/others.c#L1125-L1161`: explicit common limit checks append heuristic alerts.
- `https://github.com/Cisco-Talos/clamav/blob/clamav-1.4.3/libclamav/scanners.c#L5697-L5727`: descriptor-size limit checking operates on the supplied descriptor.

Observed config SHA-256: `dc2cce4d4e475a538f23beb4015c70a4c31dbb2bd583baf73c795d7a6045a35d`. Probe script SHA-256 at execution: `452e60ae97c991b76b03afeaf7a33bac32f1e7ccb6f104cea402e28c972b946b`. These hashes identify local evidence only; deployed configuration remains unverified.
