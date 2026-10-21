# D31 migration preparation — 2026-10-21

Task JYT-EXTERNAL-D31-CHAT-20261021. **Preparation and production SELECT only; no DDL/DML, stop, restart, build or deployment executed.** Parent owns final same-Run Flow 5260799 release wrapper. The user has authorized unified deployment including a bounded API maintenance stop; this document does not invent a further blanket approval requirement.

All filenames below are relative to `/home/isp/wsps/cyf/specs/juyiting-external-commission-mvp/evidence/implementation/migration/`. Exact SHA-256 values, target server UUID digest, MySQL version, helper hashes and source origins are in `candidate-pins.json`. That manifest pins content, not a final Flow artifact: parent must bind its digest and integrated API commit/tree to the actual release Run. No F06/E05 helper was modified.

## Corrected binding conclusion

The earlier `production-readonly.json` remains a historical observation: strict old-manifest tenant equality is 0/14. **It is not a requirement that the old grant contain a binding field that never existed.** `flow-preflight-report.json` supersedes its blocking interpretation:

- 14 grants, all ACTIVE; **14/14 eligible for migration-time same-owner binding freeze**, unresolved 0.
- 31 DISPATCH rows, all SENT: 30 bounty + 1 private. **30/30 bounty references uniquely proven**, ambiguous/unresolved 0. No reference comes from latest ACTIVE grant.
- One in-flight CHAT turn, state DISPATCHED, masked ID `defe328366e432f1`, exact source reference proven. Do not cancel it or change payload/context to make migration pass. Stop/reconnect may interrupt transport; callback/recovery must be checked after startup.
- Registry canonical/owner/client/tenant/binding immutable-update trigger currently exists, created 2026-09-16; no-delete trigger created 2026-08-01. Both precede all these grants (2026-10-20 through 2026-10-21). Body digests and timestamps are captured by audit; exact bodies are checked by `grant-freeze.cte.sql`.
- Registry `create_time`, `provisioned_at`, binding `create_time`, `bound_at`, and both last-update times precede every matching grant. Every owner/client/tenant/canonical projection matches byte-exactly; lifecycle and binding active. No other binding row with the same canonical ID exists.
- Approved immutable manifest corroborates **same owner + client + canonical + binding, approved before grant**, for all 14. Its old tenant is not used as today's routing scope or silently rewritten. Today's exact tenant comes from grant + immutable registry + binding. This avoids assuming a historical tenant-normalization receipt.
- At pre-D31 API base `510b2937696495b54a9203729784660e62c65082`, `AgentTaskExecutionGrantServiceImpl` resolves assignment through `legacyAssignments.resolveAgentId(tenant,client,taskOwner,requestedAgent)`, then persists canonical target and owner. `AgentLegacyTaskCompatibilityService` uses the same owner-scoped identity resolver. The original bootstrap matches exact grant, source action, target, requirement and assignment. No old cross-owner authority is invented. Platform isolation here is persisted **client_id** (plus tenant); there is no separate `platform` column in these identity/grant tables.

This is a **cutover freeze of the verified current binding for the original same-owner canonical subject**, not a statement that old grants stored historical binding IDs. `executor_owner_jiacn = grant.owner_jiacn`, binding is the corroborated immutable registry binding, `external_policy_revision = NULL` (self assignment, not an external-policy decision). `grant-freeze.cte.sql` intentionally covers this observed legacy cohort only; a new opaque identity, changed binding, changed owner/client/tenant, post-grant update, ambiguous source, missing guard or unclear subject fails closed rather than widening evidence rules.

Replacement audit limits: no dedicated complete identity replacement log was found in the inspected schema. Binding rows themselves are mutable; their timestamps alone are NOT proof. The no-rebind/no-delete registry constraints, independently approved manifest, exact current binding projection and original owner-scoped source are the combined evidence. Current metadata cannot prove no privileged DBA ever disabled guards; do not claim such a forensic guarantee. There is no observed replacement in this cohort, so absence of a nonexistent historical grant-binding column is not a release blocker.

## Read-only executable gate

```
python3 -B /home/isp/wsps/cyf/specs/juyiting-external-commission-mvp/evidence/implementation/migration/flow-preflight.py
```

Observed result: `PREFLIGHT_PASS`, exit 0. Checks pinned inputs/helpers/target, exact guard-based grant candidates, immutable dispatch proof, invalid JSON and clean pre-expansion catalog. Uses one consistent READ ONLY MySQL transaction; only counts and hashed IDs are emitted. Exit 2 on real mismatch/unresolved rows. After any expansion it deliberately requires phase-resume catalog checks rather than replaying once-only ALTERs. PASS is **not** a stop/backup/postcheck/deployment receipt.

`test_preflight.py`: 7 local gate decision tests PASS (no DB writes). Actual CTE SELECTs executed successfully on production MySQL 8.0.21. UPDATE/ALTER execution and rollback behavior have **not** been tested on a disposable DB; parent must include the pinned migration inputs in isolated Flow migration validation. No local Gradle.

## Minimal execution order for parent Flow wrapper

1. Fix integrated API commit/tree, version, **same Run immutable artifact SHA**, migration manifest SHA, helpers and target. Validate artifact before downtime. Do not use LOCAL/source-to-production admission to replace Flow provenance.
2. Acquire existing coordinator `/tmp/cyf-api-flow-auto-approval-v2.lock` → global release `/tmp/cyf-release-api.lock` → lifecycle `/tmp/cyf-api-lifecycle.lock`; inherit their existing descriptors/contracts, never reacquire in child or delete/steal a lock. A feature MySQL advisory lock `cyf:external-commission:v1` may follow those locks, held by the live migration connection until completion. It is not a substitute for stopping writers. Contention waits; no cancellation of other runs.
3. Use existing lifecycle controls to stop the precisely identified canonical API process; verify PID/start-generation, `/home/isp/hosts/cyf/api/cyf-api-kit.jar`, inactive runtime record and no surviving canonical writer. Check other authorized DB writers/jobs are quiescent; release lock alone does not prove this. Parent wrapper retains maintenance ownership through schema and installer phases.
4. Backup **after stop and before DDL** into `/home/isp/baks/jyt-external-d31-<Run>-<commit>/`, directory0700/files0600. Save exact catalog/triggers, consistent data, installed JAR/receipt/config metadata, source/SQL/backup SHA256. Include `agent_task_execution_grant`, `chat_dispatch_outbox`, and proof dependencies: bootstrap outbox, typed admission, turn, context snapshot, identity registry, persona binding, legacy manifest. Capture policy table existence (currently absent). Use installed mysqldump with `--single-transaction --skip-lock-tables --no-tablespaces --set-gtid-purged=OFF` and explicit socket/schema/table list; validate exit, nonempty backup and recovery availability. Do not expose dump/raw IDs or credentials to Flow logs/git. Backup/restore not performed by this task.
5. Re-run gate under maintenance. Validate all required columns/indexes/constraints from catalog, including policy absence. Fail closed on drift. Run SQL phases **in this order, not lexical filename order**:
   - `00-agent-expand.sql`: three nullable grant columns.
   - `01-chat-expand.sql`: four nullable grant reference columns + exact dispatch index. Its diagnostic SELECT contains raw IDs: redirect full output to root-only backup evidence, emit counts only to shared logs.
   - `candidate-agent-policy.sql`: exact parent policy schema. Inspect absence/exact equivalence first, not just CREATE IF NOT EXISTS success.
   - `02-agent-freeze.sql`: begin transaction and fill only all-null executor pairs with strict proven candidates. **Leaves transaction open**. In the SAME mysql connection execute `04-agent-postcheck.sql`; require total equals stopped inventory and `unproven=missing=conflicting=0`, then COMMIT; otherwise ROLLBACK and stop. Piping the file alone exits/rolls back; the wrapper must retain the connection and inspect results.
   - `02-chat-proven-backfill.sql`: transactional four-column-only backfill, repeat-safe for all-null tuples. It commits; never modifies payload/snapshot/contextHash/status. Then `03-chat-postcheck.sql`: proven count must equal inventory bounty dispatch count, missing/conflicting both zero. Re-run read-only proof audit to confirm no unresolved source rows (postcheck only joins proven rows).
   - `05-agent-finalize.sql`: make executor owner/binding NOT NULL, add executor index. Exact catalog postcheck types/collations/nullability/ordered indexes and policy schema; capture counts/checksums. Original `candidate-agent-grant.sql` is **reference only**, not a runnable phase: its broad current-registry UPDATE is replaced by the bounded freeze.
6. Only after all schema/data postchecks, continue **the original same-Run installer** with its receipt/artifact validation and correctly inherited lock contract. The installed helper has a stopped-maintenance path (`--local-offline-maintenance`, inherited FD10/8/9, kernel ownership checks), but that path is LOCAL-admission-specific, not permission to convert this Flow release into LOCAL. Parent must attach the Flow wrapper to the verified lock/lifecycle contract, not just export fabricated receipt variables or invoke a second locking coordinator beneath held locks. Do not modify F06/E05 schema handlers.
7. Installer backs up/activates the verified JAR, starts once, performs health and business checks. Verify persisted owner A/executor B boundary, callback on the proven in-flight turn, ACK/reconnect, no duplicate dispatch/final, no new schema exceptions. Keep service stopped on migration failure; do not quietly start old code against tightened schema.

## Partial execution and recovery (actual integration requirement)

MySQL DDL auto-commits. After interruption inspect each column/index separately; skip only byte-equivalent definitions (type, collation, nullability, ordered keys/uniqueness), apply only missing statements under the same maintenance contract. Wrong/partial definitions block, not silent IF NOT EXISTS success. Preserve phase receipts with SQL hashes. Backfill rerun: exact tuples are no-op; partial pairs/tuples or mismatches block; never replace them with a newly active grant. Re-check source proof on every resume. DML rollback cannot undo earlier DDL.

**Old binary grant INSERTs omit new executor columns; after NOT NULL tightening an app-only rollback is unsafe.** Existing installer has ordinary automatic `restore_and_start`; its `forward-only` decision is currently bound to LOCAL admission (`RUN_ID` empty), not proven available for normal Flow. Do not assume an environment switch is a validated Flow recovery contract.

Parent Flow wrapper must choose/validate one concrete failure path before starting candidate:

- Flow-bound forward recovery: suppress old incompatible restart with a durable verified recovery decision; retain maintenance on failure and repair using the same/new explicitly pinned Flow artifact. Reuse installer contracts, not F06/E05 edits; or
- schema-aware rollback while all writers stopped: verify candidate stop, loosen only the two new grant columns back to nullable (retain data/indexes), verify exact restored catalog compatibility, then let original installer restore its backed-up old JAR and start/health. This loosening must occur **before** any automatic old start, not after wrapper regains control. Do not blanket-drop or restore full tables while live. After candidate traffic, assess new external assignments before old-binary rollback; no automatic semantic downgrade.

This recovery hook/order and final Flow wrapper are real remaining implementation/validation items owned by parent, **not unresolved historical binding or a new request for human deployment authorization**. Backups are recovery inputs, not proof a full restore is safe; fresh writes require a separately bounded data recovery decision.

## Chat patches ready for integration

Cherry-pick in order from `/var/tmp/cyf-external-chat-20261021`:

1. `f3f790880778970a56184f7bdc78c100e1cd8bef`: STOP after REVOKED/SUPERSEDED version+1 follows exact original persisted grant/B; ordinary incoming remains strict, no active replacement.
2. `8cc5c1467591945b16ec708ff2e70df71727a785`: all four outbox reference columns; historical contexts retained, authority frozen by persisted tuple.
3. `a5c018578c1f49df915b1193b1c1f87fbb9c7088`: Flow217 missing Spring authority bean and cancellation fixture; real AgentBizException(AGENT_FORBIDDEN) translation; DB errors propagate; Mockito restub corrected.

Formal Java validation remains parent Flow on integrated commit (Run217 was old candidate: 1794 tests / 3 failures / 38 skips). No new Java pass claimed here. Runtime delivery remains `c11a078e0fc365c09706d569e0c668bcdb230d9f`; no additional Runtime changes/deployment for migration.

## 2026-10-21 23:32 single-Owner release wrapper

Supersedes the earlier uncertainty about Flow forward-only propagation: the installed adapter preserves the environment and numeric Flow installer does not overwrite CYF_API_FLOW_FORWARD_ONLY. Six existing numeric-Flow offline installer fixtures PASS (including exact retry, failure preservation and wrong-source/artifact rejection); this is not production approval.

`flow-migrate.py` loads the SHA-pinned existing adapter and wraps only its existing invoke_installer hook. Original five-argument Flow/receipt/artifact admission and coordinator lock run first; coordinator stays held throughout migration and installer. Under original release→lifecycle locks, stop only canonical API, verify no surviving canonical JVM, backup affected tables/catalog + old JAR/record, obtain a single-session named DB lock, prove immutable same-owner and original dispatch tuples, expand only exact missing columns/indexes, backfill transactionally with zero-unresolved/conflict checks, tighten grant columns, and verify original catalog preserved. SQL hash is rechecked at use; phase receipts remain private and immutable input binding is required.

Release/lifecycle locks are then released while original coordinator remains held; original installer reacquires its normal locks. Forward-only=1 prevents incompatible old restart on candidate failure; wrapper verifies stopped state on nonzero/exception. No LOCAL bridge/admission, no F06/E05 edits or replacement installer. Root-only binding records actual pipeline/run/source/tree/version/archive/pins/wrapper and before-state digests. Ten offline wrapper tests PASS; no real DDL/start has executed at this revision. Host-stage same-Run verification and live postchecks remain required.
