# Lease helper repair review

Independent reviewer `/root/od06_tenant_review` rejected93759b5 for one remaining P1: version+1 and a canonical expiry alone do not prove renewal. Its fake returned the same leaseUntil through claim/start/heartbeat and the probe still succeeded. Require heartbeat expiry to increase; also reject internal whitespace under OpenAPI's non-whitespace identifier contract (P2).

The original three P1s were independently confirmed closed. Seven synthetic controls passed, hashes matched, root was clean and no pycache remained. No live/API review occurred. Root adds the two bounded checks and counterexamples before re-review; prior evidence is preserved without reclassifying it as passing this repair.
