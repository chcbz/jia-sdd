# OD02 repair candidate 010a1022 — REQUEST_CHANGES

- Frozen API commit: `010a102217d105f6e6f5dd94dc3d01a8a4e5ffcc`; worktree confirmed clean by root and writer.
- Previous candidate `0ac3921` received REQUEST_CHANGES; accepted development base remains `c5330dd5`.
- Original critical worker owns repairs R01–R08; independent read-only architect `/root/output_design_review` reviewed the immutable candidate and returned REQUEST_CHANGES; see `review-010a1022-findings.md`. Preferred adversarial provider remains unavailable as recorded in the previous review packet; this is not cross-model approval.
- The combined targeted regression on this commit passed 64/64 with no failures/errors/skips. Root rechecked all reports, command/exit and 17 changed source hashes; see `repair-010a1022-test-results/execution-notes.md` and `root-association.json`. The verdict leaves R01/R04/R06 open and closes R02/R03/R05/R07/R08. OD02 is not accepted.

## Repair and evidence index

| Findings | Candidate repair reported by writer | Passing stage evidence observed before final candidate association |
| --- | --- | --- |
| R01 | Bearer-free persisted final authorization; source/run/identity/binding locks before quota | Actual authorization MySQL suite: 9 tests, no failure/error/skip; scan barriers cover terminal/revoke/source/binding changes |
| R02–R03 | Current epoch must have RETAINED cleanup matching exact scanned object storage identity; RETAINED counts toward the two-key limit | Real MySQL/MinIO/ClamAV upload suite: 20 tests, no failure/error/skip; includes replacement/cleanup and projected third-key cases |
| R04/R07 | Central-directory-aware ZIP checks, entry accounting, strict JSON parsing | Earlier targeted unit/security batch: 26 tests total, all passed; do not add to the final combined overlapping run |
| R05 | Exact columns/indexes/CHECKs/engine/collation for eight tables | Real MySQL schema suite: 9 tests, no failure/error/skip |
| R06 | Output-specific success/error envelopes and shared filter rendering | Actual-chain/controller tests are in the preceding targeted batch; final wire/source verification pending |
| R08 | Deterministic short/long PUT size mismatch classified as permanent integrity failure | Included in the 20-case real-dependency suite; final independent review must verify state/quota semantics |

Stage originals are `/tmp/cyf-od02-evidence/repair-*-{command,exit,log,result.xml}`. Root directly read the final schema/auth/real-dependency XML counts and exits. The earlier schema failures remain historical evidence: normal index ordering and JSON-column charset/collation representation initially mismatched the expectation; both were repaired while retaining strict metadata checks. The final combined candidate run now supplies source/report association, while stage pass counts alone do not establish it.

The independent reviewer must assess closure against `review-0ac3921-findings.md`, not infer correctness from these counts. Previously documented component/mock boundaries remain applicable. No owner publication/download endpoint, client queue, Web entrypoint, integrated release or production migration is accepted by this checkpoint. OD03 remains gated on the completed review and necessary verification.
