# First independent Sol review — REJECT

Candidate1d807850, reviewed by existing `/root/od01_source_auth/od07_api_sol_review`; findings relayed by sole writer on2026-09-13. P0=0, P1=2, P2=1. Original23 scoped passing tests remain attributable to this candidate, not acceptance.

- P1: OD08 also owns listDeliveries. GET was absent, and DELIVERY_PIN only prevented GC without granting the user exact formal-delivery reads of private artifacts. Add owner-authorized batch listing and exact immutable delivery-item retrieval.
- P1: Required real MySQL reassignment-versus-submit race between two transactions was absent. Add an actual contention outcome and atomicity proof.
- P2: M003B schema validation did not reject extra foreign keys or triggers. Add deterministic drift rejection and relevant real-MySQL coverage.

Writer is repairing these in the isolated API worktree; no client slice or production feature publication has begun. Preserve this candidate evidence and associate the later repaired tree with its own original reports and repeat independent review.
