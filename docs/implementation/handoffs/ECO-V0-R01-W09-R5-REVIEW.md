# R01 / W09 cumulative review and bounded correction — 2026-09-06

Independent Sol Leibniz `01a074ac-4236-71b1-850f-75cc9a05b01f` reviewed API `ac72b17b0207177eb0118e72703d1b810f790515` / tree `c7911622f2be1a9cd3b1f1cf7570be6b487a9391`, including all previously unaccepted R01 application/ledger parents. No Gradle/MySQL/runtime executed. NoDB wrapper `/var/tmp/cyf-eco-control-w09-r1/run-nodb.sh` is prepared only and NOT GO on this rejected cumulative source.

| Scope | Verdict / root cause | Bounded remediation |
| --- | --- | --- |
| W09 production | SOURCE ACCEPT 0/0/0 | Preserve production bytes; does not accept R01 parent or W09 fixture/runtime. |
| W09 MySQL fixture | REJECT P1: registers database after CREATE, so unknown CREATE result can leak owned DB; lacks bounded JDBC connect/socket timeouts. | Register owned name before CREATE; remove only after confirmed DROP; bounded URL. Reuse W07 lifecycle principles, not its PASS or unnecessary async worker machinery. Add failure/lifecycle tests. |
| R01 application/ledger | REJECT P1: managed active OAuth key remains usable after exact intent FAILED_NO_EFFECT refund; REFUNDED work-admission and API-key handshake accept it. | In the same refund transaction, exact scope/intent-associated managed-key CAS disable; mismatch/error must roll back financial refund, never disable unrelated keys. Test post-refund key rejection, atomic rollback, retries, UNKNOWN and existing-key isolation. |
| R01 runner af40adbe | REJECT P1: managed-host module omitted from installer staging. | Already implemented by W10 integrated 4bd0c257/7600bc8a; reviewer validating final delta separately. Preserve original verdict, do not rerun passed installer92/packaging9/client-host83. |

One critical Writer will own the combined bounded R01/W09 API correction in a new `.worktrees/eco-v0-api-r5` from ac72b17b; original candidates immutable. Only hosting credential/refund collaborators and minimum exact OAuth CAS support plus relevant tests, and W09 MySQL fixture/lifecycle tests. Do not change accepted W09 commerce production, Web, runner, build scripts, schema unrelated to the finding, root ledger or release tooling. Static checks and clean candidate first; independent delta review then targeted runtime verification. No service/DB/build/deployment permission from this packet.

## Final runner closure

Same independent reviewer completed the bounded final-runner check: **4bd0c257/7600bc8a cumulative SOURCE ACCEPT 0/0/0**. `shell/codex_ws_agent_install.sh:160` stages `managed-host.mjs`; workspace-manager tests assert availability before npm and source-byte equality. `agent-client.mjs` and `managed-host.mjs` are unchanged from the fully inspected parent. Original af40adbe REJECT remains historical; final integration closes it. Existing exact-tree Node evidence is reused, no tests rerun. This does not close the separate R01 credential-refund or W09 fixture findings.
