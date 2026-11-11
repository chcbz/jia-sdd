# W05/W06 fixture review attribution — 2026-09-06

Independent reviewer `01a07116-f22e-7351-9af4-e66dbcee21da` on `50b04489b384b40fffb034cc06c2d2a42ea8fad6` / `1b0be0504ca5da3096ce6cb6d76112b2874de666`: W05 delta REJECT 0/0/1, W06 combined REJECT 0/0/2 (shared W05 finding counted once). All four previous W05 production findings are source-closed; no new production/posting weakening found. No tests run.

| Finding | Root cause | Authorized bounded correction |
| --- | --- | --- |
| `FundedBountyQuoteClaimRealTransactionTest.java:132,145–154`; inherited by settlement fixture | Runtime DAO is a Spring bean whose inherited injected AgentRuntimeMapper is missing from Spring; MyBatis registration/reflection assignment cannot satisfy injection during bean creation. | Register the actual mapper bean from the existing SqlSessionTemplate before requesting the service. Keep production constructor selection and real transaction collaborators. |
| `AgentBountySettlementControllerTest.java:69–71` | One-argument JwtAuthenticationToken is unauthenticated; purported success/disabled cases fail at authentication. | Explicitly authenticated token for authenticated scenarios; preserve/add dedicated unauthenticated and missing-scope negatives. |

Stop repeated rejected-source verification: no Gradle on this candidate. Repair only those two test paths in a new worktree based on 50b04489, leaving all production blobs and existing candidates immutable. New owner must be explicitly admitted after old owner release; independent reviewer checks delta, then targeted transaction/controller tests and MySQL gates. W09 consumes exact correction only after source review. W05's previous failure history remains separate; no source ACCEPT is runtime PASS.

## Corrected delta closure

`01037b00b2b35896915948e5f8d8346f8f525102` / tree `be99b95f7b765870e6fc74abe247913528620e49`, parent50b04489, clean `.worktrees/eco-v0-bounty-settlement-r2`. Only two authorized test paths changed; production bytes unchanged. Original Godel independently returned **W05 SOURCE ACCEPT0/0/0 and W06 SOURCE ACCEPT0/0/0**. Mapper is a real Spring bean with identity assertion; authenticated JWT scenarios and explicit unauthenticated/missing-scope rejection tests are distinct. Prior production review is reused, not rerun.

Prepared-only `/var/tmp/cyf-eco-control-w06/run-w06-r2-nodb.sh`, SHA256 `16a8afe2e7cafba39187273e2acc77b4e3e2b232d568c50c1ef2894cd9fa7e65`, combines targeted W04/W05/W06 selectors through orchestrator. Syntax checked, not executed; runtime/MySQL/deployment remain pending. W05 root-cause authorization records the bounded shared correction and retains previous failure history.
