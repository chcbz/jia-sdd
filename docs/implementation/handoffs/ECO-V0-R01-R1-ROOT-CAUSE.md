# R01 foundation R1 — review rejection and bounded remediation

Candidate `a7f7ac17d1133f9f97f0f874c4b826f1e1ef2d98`, tree `1c8f7acb16469be6c851437d9da082b6dad285df`; independent reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **REJECT P0/P1/P2=0/3/0**. W03/R00 parent acceptance is unchanged. This is foundation-only, not full R01 acceptance.

| Failure | Evidence / root cause | Bounded correction and verification |
| --- | --- | --- |
| Wrapper argument order | `/var/tmp/eco-r01-foundation-r1-JfDId3/gradle.log`, SHA256 `6226ef241a74805c19af12fb80259a31a0edcac0c1c415ed0b2bd72c71a3e64b`; task positional preceded wrapper options, so argparse REMAINDER consumed required metadata; no tests ran | Main supplied `/var/tmp/cyf-eco-control-r01/run-foundation-r1b-nodb.sh`; finish the already-authorized invocation, do not reconstruct flags or retry blindly |
| P1 incompatible full catalog accepted | `EconomyHostingRentSchemaInitializer.java:75-96,220-264` only compares names; matching non-unique index and `CHECK(1=1)` can be accepted | Validate actual column definitions, index uniqueness/type/visibility, CHECK expression/enforcement and immutable triggers using accepted W02 approach; add complete-but-incompatible MySQL cases |
| P1 unknown provisioning cannot reconcile success | `HostingRentLedgerServiceImpl.java:335-341`, mapper `:237-246`, service interface `:8-14`; UNKNOWN cannot reach capture | Add trusted internal successful reconciliation with intent/version CAS. Unknown remains escrow-held absent proof; test unknown->success, stale/duplicate callback and conservation |
| P1 refunded Agent cannot retry | Mapper `:146-161`, schema `:85-87`, service `:199-202`; REFUNDED lease plus unique Agent key permanently blocks INITIAL | Reuse only refunded/no-effect lifecycle under CAS with a fresh intent (or equivalent safe history-preserving transition); test reserve/fail/refund/new-quote/reserve, old intent fencing and no duplicate charge |

## Execution boundaries

Stop the rejected candidate's retry loop. Wait for current noDB verifier to finish and explicitly release immutable tree before any source write. No MySQL authorization on rejected source. Resume original critical writer in its original rent worktree; preserve other writers' isolated worktrees and accepted parents. Run targeted verification and independent delta review only on a new clean committed tree.

Full R01 still requires canonical binding authorization, after-commit managed provisioning/readiness proof, quote/bind/lease HTTP, renewal CAS, expiry/new-work admission and retry wiring. Held-only wallet version integration remains required downstream. Nothing deployed or charged.

## Authorized r1b compile result

Verifier `01a07115-7ec0-7242-b839-5f95055a5bbf` completed its single r1b invocation, exit1, session8080, no source edits. Verifier initially reported no test XML; main checked the handed-over artifacts and corrected this below. `/var/tmp/eco-r01-foundation-r1b-FwHyIf/gradle.log` SHA256 `1b32fdbc51eccaedb074284eaf933ce8c981ea207375884d0db3f8292d62d5b5` reports `EconomyHostingRentSchemaInitializer.java:83` ambiguous `JdbcTemplate.query` overload (`ResultSetExtractor` versus `RowCallbackHandler`). Add an explicit callback type or unambiguous block return as a fourth bounded correction. No service/Agent test success evidence. Existing rejected candidate is now released for source remediation; no running verifier needs its tree.

Provider note: original writer's first resume returned model-capacity error; one bounded existing-agent retry succeeded and acknowledged read-only standby. No provider switch or DeepSeek route was made.

Main artifact correction: log SHA256 matches. Gradle did run `:economy:jia-economy-mapper:test` before the service compilation failure. Fresh `TEST-cn.jia.economy.schema.EconomyHostingRentSchemaContractTest.xml` has **1/0/0/0**, timestamp `2026-09-05T10:52:13.282Z`. This single schema-text check is partial evidence only, not a passed r1b selector or foundation acceptance. Whole invocation remains failed.
