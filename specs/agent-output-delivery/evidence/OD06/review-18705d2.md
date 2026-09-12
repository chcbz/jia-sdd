# OD06 retention review — REQUEST_CHANGES

Independent read-only reviewer `/root/od05_review_fallback` found3 reproducible blockers on `18705d228b87f09e815b7a3f3aa8e758d16d6e69`. Product/root were not modified by review.

1. **R1 / P2 — busy delivery hot loop.** output-queue.mjs:959 returns on OUTPUT_RUN_BUSY without postponing an already due operation; scheduleNext at1100 repeatedly schedules1ms. Held-run-lock counterexample yields delays[1,1,1]. Add contention backoff without unlocked writes to another processor's durable run record.
2. **R2 / P2 — corrupt evidence still permits cleanup.** read at500 does not validate immutable command evidence. Removing commandEvidence from a completed command still deletes snapshots and archives successfully; resolveCommandEvidence then fails OUTPUT_QUEUE_CONFLICT. Require complete consistent evidence before destructive cleanup; retain bytes and isolate/report corrupt records.
3. **R3 / P2 — dangling directory link accepted as missing.** existsSync at676/700 returns false for a dangling run-directory symlink, producing successful cleanup/archive while the link remains. No-follow metadata checks must distinguish true ENOENT from symlinks and refuse success markers for unsafe paths.

Counterexample script/log/exit and hashes are in `review-18705d2-counterexamples/`; exit0 means the probe executed and observed defects, not product PASS. The normal terminal ledger/ACK replay path remains non-rerunning after final archive expiry. The302 passing client tests do not cover these3 cases and do not remove the findings.

Original sole writer resumed a bounded repair; API integration stays queued until same-reviewer approval. No live API or deployment acceptance.
