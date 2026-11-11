# R01 R4 source candidate — 2026-09-06

Not compiled, runtime-accepted or deployed. Independent review must include the full unaccepted R3 application delta plus R4, not only the final commit.

| Repository | Commit | Tree | Parent |
| --- | --- | --- | --- |
| API, `eco-v0-rent-application` | `aa81221be06e141512f110d80a514f8a157aacb7` | `5d4d87fe8864ffe6325708a1e8504a1c8e47b5b1` | `3bb9b762fa3a3e266da0bb61850ac5dc593e7450` |
| Existing runner source, `eco-v0-rent-agent` | `af40adbe7d1541b51755107b2c4ba55cfa151bfe` | `21aaef688052057ea4ca38b194cce01c4796d5a1` | `3b337d22ee4ec543b7223d45131bcbf8ee38d41d` |

Original owner reports concrete permission-restricted private Unix-socket ensure/observe adapter inside existing runner, engine-initialized plus exact canonical registration readiness, durable zero-money free reprovision with once-only lease CAS and unchanged paid periods, original intent scoped OAuth reference, and trusted readiness time surviving delayed capture. Unknown/mismatch/timeout retains escrow. HTTP contract unchanged; feature default-off.

Main verified clean SHA/tree/parents and 22 API / 4 runner changed paths. Only static/syntax/whitespace/catalog-shape checks were run by writer. Candidate assertions are not test evidence.

Proposed verification: `cn.jia.agent.hosting.*Test`, `HostingRentLedgerServiceRealTransactionTest`, `EconomyHostingRentSchemaInitializerMySqlTest`; runner `test/managed-host.test.mjs`, `test/agent-client.test.mjs`. Admit verifier and freeze exact source/fixture before running; all Gradle through orchestrator.

Release integration must add `managed-host.mjs` to the existing install script's explicit staged-module list; writer intentionally did not touch W10 installer ownership. Configure matching API/runner scope, owner, restricted socket/directories, runner UID, trusted seed home and executable/workspace policy. No new daemon/repository. Older four-table hosting catalog fails closed: actual preview schema installation must match the final candidate, no implied automatic upgrade.

R01 source owner handed off and now owns W09 in a separate tree; preserve these two candidate trees immutable.
