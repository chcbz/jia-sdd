# W07 R1 independent source rejection

Exact `138d636d98f021d8b9da84e9dac3d749ead73eea`/tree `cd862676a60b4b7ed46c598c15646366d7f915a3`. Reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **REJECT 0/2/2**. Source only, no runtime evidence inspected.

| Severity | Root cause / path | Bounded correction |
| --- | --- | --- |
| P1 | EconomySkillSchemaInitializer.java270-277 examines only immutable-table triggers or named prefix. Arbitrarily named BEFORE INSERT hook on economy_skill_order can rewrite buyer_id and evade exact-catalog validation | Inspect all triggers on all seven owned tables and compare exact expected set; reject unexpected business-row hooks. Add malformed full-catalog regression. |
| P1 | Initializer177-217/ForeignKeySpec omits referenced database; same-named FK can target foreign database same table/column | Validate referenced schema equals current database, not just table/columns/rules. Test cross-schema FK using only verifier-owned temporary DBs. |
| P2 | EconomySkillSchemaContractTest75-77,94-95 contradicts mapper: publishProductVersion allowed but also matches forbidden productversion substring; qualified v. scope not accepted by assertions | Correct only assertions to actual permitted updates and qualified exact scope. Retain immutable version-write prohibition and strict scope requirement. |
| P2 | EconomySkillSchemaInitializerMySqlTest219-230 splits first semicolon in DDL comment, so partial fixture executes comments instead of table | Parse/slice first CREATE TABLE statement safely or use established Spring ScriptUtils; assert fixture actually contains exactly one owned table before partial-catalog validation. |

W07 original writer must preserve the exact 24-file scope, no W08/W09/shared-code expansion. Source gate rejection does not imply runtime tests ran. Verifier session92834 reported zero-byte own log `/var/tmp/eco-w07-r1-nodb-iNai32/gradle.log`, no gradlew child and an open global-lock descriptor; that alone does not prove lock ownership. Exact verifier may cancel only its own **confirmed not-yet-running** invocation under main authorization, without signaling foreign lock holder or daemon. If Gradle already started, let it finish naturally and report partial XML. After explicit immutability release, bounded remediation then new clean candidate review/tests.

## Waiting invocation cancelled by exact owner (not a test result)

Verifier `01a07146-2fd0-7253-aa5f-8c2594c9231b` reports own process chain bash812846/python812852/tee812853, no gradlew child, own session92834 cancelled by Ctrl-C under main authorization, shell120. Empty log SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, no XML. Clean W07 tree explicitly released. No foreign process/daemon action and no test retry. This is cancelled-before-Gradle evidence, not a failing/passing suite or a second source failure.

## Correction candidate

Original writer clean `b4614bd57aa9707412d3855548b2f3e17a325f16`, tree `bd391fe13f530bdbb7d43698f98d54075b45d3cb`, parent138d636d. Exactly initializer/schema assertion/MySQL regression three files. Reports all four findings addressed with arbitrary-hook and foreign-schema regressions. DDL/entities/mapper APIs unchanged. Main checked exact clean HEAD/tree. No runtime/test evidence; independent delta review pending.

Independent delta reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **ACCEPT0/0/0** on exact b4614bd/treebd391fe1, three files, all four findings closed in source; no runtime evidence. Global read-only slots naturally released; original verifier resumed for new `/var/tmp/cyf-eco-control-w07/run-w07-r2-nodb.sh` exact candidate/selector, no blind reuse of cancelled R1 run. MySQL needs separate GO.
