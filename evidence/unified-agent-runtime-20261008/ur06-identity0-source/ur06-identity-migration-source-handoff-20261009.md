# UR-06 identity migration contract — SOURCE PHASE handoff

## Fixed input / authorization
- Original Owner critical_worker; no Reviewer/new Agent. Main owns ledger/control/formal verification.
- Rules re-read: /home/isp/wsps/cyf/AGENTS.md and /home/isp/wsps/cyf/ops/orchestration/README.md.
- Worktree: /home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008
- Branch: codex/ur06-m4-mysql-e05-20261008
- Base commit: 4a72049b66b9758ad8c19ee7fe385501f73eb314
- Base tree: f031b559a5315d56d2ea66cb36c2a7385c2e60b1
- Accepted readonly proposal: /var/tmp/ur06-identity-migration-readonly-proposal-20261009.md / SHA256 41ef332f0ec81d849894b18c88d68dbc5fcd580ac1e598c47083f38783c9c633.
- Candidate commit: c084fb8f498f335e028af534ee7a570536cbc349
- Candidate tree: a4e56538969dddab2f4543d095b9a3a7c3b0af10
- Actual push/ls-remote readback: c084fb8f498f335e028af534ee7a570536cbc349; WT clean.

## Exact three owned files / SHA256
- /home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql
  SHA256 758390679844ea293ade3ac6ba68049ab55d331279637a2e6c3d1fd070f02739
- /home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-mapper/src/test/java/cn/jia/agent/schema/AgentIdentitySchemaTest.java
  SHA256 cd8ea41b506a3ea02ae7e79df9b42f5baec618a36ef2fd14038f807f0f314eb3
- /home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentSchemaInitializerTest.java
  SHA256 82c6c8ba735ecbbfaf1d7fba42e10d9757f298fd61f410d75e7559c5c54cd55b

## Implemented scope
- Registry SYSTEM and nonSYSTEM tenant0 in both CREATE and ALTER CHECKs; registry/alias comments and alias double scope CHECKs equal latest canonical complete baseline.
- Binding active persona unique target is (tenant_id,client_id,active_persona_code), retaining create-target-before-drop order and canonical uniqueness protections.
- Three null-safe exact/BINARY/OCTET_LENGTH tenant0 preflight guards plus active persona conflict guard precede first runtime ALTER, binding MODIFY/index replacement/FK or CHECK drops. NULL/non0/active conflicts rejected; no row UPDATE/INSERT/DELETE/REPLACE/TRUNCATE conversion.
- Binding tenant metadata brought to baseline NOT NULL/default0 only after row rejection guard; immutable owner/client, identity canonical/binding keys and full five-column RESTRICT FK unchanged. Whole four immutable/terminal/no-delete trigger suffix byte-identical to base.
- Mapper original five test names preserved: current tenant0/index oracle, full CREATE parity, exact CREATE+ALTER scope/comment invariants, preflight order/unique target/FK/noDML assertions. Existing SQL scanner copied from original initializer test with parameter rename only; same eleven quoted/comment positive and four malformed negatives in original parity method.
- Service original48 names preserved: existing identity CREATE parity adds migration third edge; original weakened-scope negative retained and augmented with SYSTEMNULL, ownerTenant, dual-tenant and alias-ownerTenant catalog rejection. Only these two tests and their original catalog helper/query were changed; all other service method bodies remain byte-equal.
- Original H2 six / UR06 seven+M4six Java entire files, all19 test methods and all oracle/helper bodies byte-equal to base. EOF repair4a720 retained unchanged.

## Actual selfcheck versus formal status
SOURCE_STATIC_ONLY: exact three changed paths; git diff --check; Java tree-sitter grammar; original method/count preservation; quote scanner/corpus byteeq; complete registry/alias CREATE lexical parity; both five-column FK clauses and full trigger suffix byteeq; no old ownerTenant or dualformat introduced; guard placement and no-row-DML static proof. Synthetic tenant guard model considers only literal0 accepted and NULL/owner/non0/padding/fullwidth rejected; NOT a MySQL engine execution.

No Gradle/javac/JUnit, SQL/MySQL/DDL execution, pip/install, process control, Flow, or production operation. No live92814/PID/target interaction. Actual candidate compile/mapper5/service48+Controller8/rootlayering/MySQL19/business19 remain NOT_RUN. Source syntax/static success is not compiler/JUnit/MySQL/acceptance PASS.

## Unchanged/outside this authorization
Production AgentSchemaInitializer, canonical schema.sql, both Controller files, legacy dryrun/apply/template, UR04/UR06 fixtures/init/Node/sourceC/installer/docs/contract/ledger unchanged. Wider approved-mapping resource drift from prior report remains separately PROPOSED; do not call this candidate complete legacy/data migration. New schema rejects historical SYSTEMNULL/ownerTenant rows and does not normalize them. Runtime/ACL strict tenant0 is not a compatibility reader. Production maintenance requires separately authorized data proof, FK/immutable handling and recovery; no such authorization inferred here.

## Exact suggested original selectors for Main
1. :agent:jia-agent-mapper:test --tests cn.jia.agent.schema.AgentIdentitySchemaTest (all5)
2. :agent:jia-agent-service:test --tests cn.jia.agent.config.AgentSchemaInitializerTest --tests cn.jia.agent.api.AgentRuntimeV1ControllerTest (all48+8, original negative methods preserved)
3. compileUr04E05HttpJava / compileUr06EnrollMysqlJava with original init wiring, then ROOT validateLayering.
4. Original same fixed sourceC/accepted target awaited callback H2six + UR06 foundation7 + M4six only after Main authorized exclusive old batch cleanup and NEW inputs; Owner did not create/cancel/retry a batch or borrow any target.

Keep original failures/history and wider schema/recovery/threeAgent-release goal uncompleted. Main owns exact source formal run and ledger transition; original Owner remains available for scoped new source diagnostics, without self-expanding authorization.

Static evidence: /var/tmp/ur06-identity-migration-source-static-20261009.json
SHA256 76faed282bbba521ef568b48a75f0ac54db1821001c28264d87447460167375f
