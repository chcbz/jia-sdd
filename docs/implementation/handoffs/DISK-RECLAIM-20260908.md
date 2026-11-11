# Disk reclamation — 2026-09-08

User explicitly authorized log cleanup and deep compression of archived sessions. Active history, unfinished code, production data, runtime/evidence and swap remain protected. No filesystem reservation manipulation.

## Baseline and scopes

- Baseline 08:48:53 CST: root available 847,986,688 bytes (808.70 MiB), target 10 GiB.
- Installed cleaner guard confirmed in natural 08:30 cron: `PRESERVE Gradle dependency cache`; terminal 08:41:11, outcome below_target, ~819 MiB. This is not target attainment.
- `OPS-CODEX-LOG-FREEPAGE-20260908`: incremental free-page reclamation only, preserve retained rows, bounded WAL/locks.
- `OPS-CODEX-COLD-ARCHIVE-20260908`: lossless per-file cold archival, verified restore hash and private recovery index; no active-session pruning or heuristic irreversible summarization.
- `OPS-COMPLETED-WORKTREE-INVENTORY-20260908`: read-only merged/clean/inactive Web worktree shortlist; no deletion until exact candidate review.

Task owners/current gates live only in TASKS.yaml. This document records evidence, not a second execution ledger. Actual bytes recovered to be recorded after execution, not forecast as completion.

## Actual execution around 10:10 CST

- Previous delegated preparation turns were interrupted/notLoaded; main took over minimal scripts, independent Raman review, and appointed Pascal exact executor for worktree removal.
- `retire_worktrees.py` SHA5914ffc3f9a398870ec09a09f1208e86c31e02db521b5bbf2056eeac33735ccd independently ACCEPTed. First shared-lock contention caused zero mutation; cron naturally ended10:03:46 before execution.
- Actual28/28 worktrees removed via standardGit(no force/branch deletion); per-path HEAD/tree/branch receipts under `/root/cyf-disk-reclaim-20260908-main/`. User code/activeworktrees protected; final paths confirmed absent by main.
- Actualdf available1,036,320,768→9,893,982,208 bytes; net8,857,661,440bytes (~8.25GiB). This includes concurrent filesystem changes, not an isolated block-level attribution.
- SQLiteR1/R2 reclaimed8,396,800+8,400,896 allocated bytes respectively and paused on write contention. Retained rows untouched by maintenanceSQL. Neither remaining~2.56GiB freelist nor cold archive savings has been counted as reclaimed.
- ArchivalR1/R2 review preserves concerns: append race/proc fail-open fixed using readlease/SIGIO+final-state transaction; future native restore without first unpacking cold files remains an explicitly reviewed contract limitation. No actual archival unlink so far.

## Final deep-clean receipt — 2026-09-08T10:32:44+0800

- Worktrees: actual28/28 removed, allpaths independently confirmed absent; branch/commit recovery metadata retained.
- Cold archives: actual644/644; firstpass203 andsecond441, native0/0, zero skips; originaltotal 1398244402 bytes→gzip 347308147 bytes, each decompressed SHA/length verified before original unlink. Mainverified all644sidecars/compressed sizes/0600root ownership/sourceabsence; rawarchivedremaining0, no compressiontemp leftovers.
- Index and restoration instructions: `/root/.codex/cold_archives/{INDEX.json,RESTORE-ARCHIVES.md}`. Entire content retained losslessly. **Cold history must be restored before application access**; no nativegzip support claimed. ArchiveR2 future-restoreP1 explicitly corrected by sameReviewer against this contract, not discarded.
- Final filesystem available 10939473920 bytes (10.188GiB): **10GiB minimum met; 11GiB recovery margin not met**. This is a point-in-time measurement, not a perpetual free-space guarantee.
- SQLite online maintenance reclaimed16,797,696allocatedbytes; remainingfreelist deferred on writecontention. No forced retry/record deletion/serviceinterruption.
- CandidateR3page-cacheoptimization prepared after EXPLAINconfirmed fullthread scan, but **not executed**: acceptedR2alreadycompleted allarchives.
- Final private receipt `/root/cyf-disk-reclaim-20260908-main/FINAL-RECEIPT.json`; archiveindexSHA256 `b6591d5f796c6e5a756eb4b67569425840e11d8d082d3b291b6b416d54b161d3`. ProductionAPI readonlysample10:20 returnedHTTP200/2.937s; no APIlifecycleoperation bycleanup.
