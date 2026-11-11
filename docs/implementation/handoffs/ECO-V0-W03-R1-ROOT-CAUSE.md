# W03 R1 — root-cause matrix and bounded remediation

2026-09-05; candidate `3249b5879ca609362ecae1278987cec501702e2d`, tree `b57ec3e18b6bbd024d66733d79912d3e2a15bb55`. Not accepted or deployed.

| Evidence | Root cause | Bounded fix | Required evidence |
| --- | --- | --- | --- |
| Verifier 01a07068-b8da-7403-b6b0-330bd5ef61b6; selector eco-w03-r1-wallet-http-h2; failed key 7525a78c530d387dce9da4fba8fd4e657a322c07ed69e4c80c989b6ec0904809; no tests ran, no saved log/XML | Unversioned Spring Security resource-server dependency cannot resolve | Use repository version catalog for resource-server and JOSE dependencies; inspect both declarations before retry | One fresh serialized low-memory Gradle selector on corrected exact tree; persist output explicitly |
| Independent reviewer 01a0706a-c01f-77b2-8892-077a5ee716ca; REJECT 0/2/1 | P1: economy paths absent from dev/grey/prod JWT resource-server matcher | Add /economy/** to intended configured resource-server routes, retain JWT scope checks | Test actual matcher/security-chain behavior, not only standalone controller injection |
| Same review | P1: available/version and held balances read in separate nontransactional queries | Return all wallet fields from a single consistent SQL snapshot (preferred); no full ledger redesign | Deterministic interleaving/snapshot regression and targeted SQL verification |
| Same review | P2: empty request body reaches generic 503 handler | Map malformed/empty body to 400 BAD_REQUEST | MVC regression with zero-length application/json issuance body |

Main controller authorizes one bounded source correction after recorded second failure. Snapshot/ACL correction is routed to critical_worker per current policy; Terra resumes frozen ordinary feature integration afterwards. Only W03-owned economy files, profile matcher configuration and focused tests may change. No Gradle during source correction, no service/process control or deployment, no W04/rent implementation on this candidate. Commit clean corrected tree, then independent verification and read-only review against `specs/agent-economy-marketplace/v0-api-contract.md`.

Wallet aggregate version semantics for held-only W06 settlements remain an explicit downstream consideration, not a new R1 blocker. Rental scope remains `v0-hosting-rent.md`; no approved price/period or active charging.
