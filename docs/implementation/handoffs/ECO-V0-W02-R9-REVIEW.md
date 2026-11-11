# ECO-V0-W02 R9 independent review

Date: 2026-09-05
Candidate: `60ccada8790463f63789dc0fafc66758a9bd4679`
Tree: `3091f3a94020013754db39eab711af816df28665`
Reviewer: `01a06f6b-af66-7101-a55c-a4551517d089` (`sol_reviewer`)
Verdict: **REJECT** — P0=0, P1=4, P2=2

| Severity | Finding | Evidence | Bounded remediation |
|---|---|---|---|
| P1 | Generic `ISSUE_SILVER` accepts an ordinary USER principal; preview allowlisting is not treasury authority. | `EconomyPostingServiceImpl.java:423-431`; `EconomyPostingServiceRealTransactionTest.java:391-395,412-414` | Fail closed in the generic posting path unless an unforgeable issuance authority is supplied; W03 may later expose only the frozen non-production preview issuance path. Add ordinary-user rejection. |
| P1 | `allow_negative=1` is accepted beyond explicitly approved system contra/variance accounts. | `economy-v0-foundation.sql:24-28`; `EconomyPostingServiceImpl.java:204-209,491-500` | Whitelist exact negative-capable SYSTEM owner/purpose combinations in DDL and Java; reject TASK/ORDER/AGENT and unrelated SYSTEM accounts. Add real-MySQL coverage. |
| P1 | Existing funding state is resolved after account locks, conflicting with frozen funding/allocation → accounts → escrow order. | `EconomyPostingServiceImpl.java:143-144,226-228,260-265` | Resolve/lock funding state before sorted account locks, then escrow, with one documented order shared by later capture/refund paths. |
| P1 | Re-runnable SQL drops immutable-row triggers before recreating them, exposing an interruption/failure window. | `economy-v0-foundation.sql:146-201` | Remove destructive trigger replacement from bootstrap SQL; use fail-closed exact-definition validation and a serialized initializer/migration path. |
| P2 | Concurrent application nodes can race missing-trigger creation and fail the loser. | `EconomySchemaInitializer.java:201-220` | Serialize initialization with a DB advisory lock or re-read and exact-validate after duplicate creation. |
| P2 | No 100-request high-contention debit conservation test. | `EconomyPostingServiceMySqlConcurrencyTest.java:96-150` | Add isolated-MySQL 100-request contention assertions for success/rejection counts, non-overdraft, versions, journal sum, and escrow totals. |

Reused exact-tree verification evidence:
- no-DB: `81d6533d3716bfcab3e459fd98116f792680b952ed3bc79a44cbfa1b73a90342`
- isolated MySQL: `685f045e7b2b40b02eb124d38e5cb33f9f820e1001f2ab08f680f3f44198ed20` (28/0/0/0; fixture cleanup user/db 0/0)

No Gradle was run by the reviewer. W03 remains dependency-blocked until a remediated exact W02 tree passes fresh verification and independent review.
