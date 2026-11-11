# H06 R47 runtime failure root-cause matrix

Date: 2026-08-29 CST

Exact H06 candidate: `5643e7d1f05bc645b66eb9eb6e459890da39fb79` / tree `e4d6db9273db6c73ec7c13242fd61e7b59f9fe28`.
Attached H05A API: `97d046cea9e65e22db1f3faee1809251a144ec6b` / tree `0a6292aafef71e34959d173f3eafe03b1e3a7c77`.
Persistent unit: `cyf-h06-r47-exact-verifier.service`; terminal FAIL at 2026-08-29 13:04:50 CST.

| Item | Evidence | Attribution | Bounded remediation |
|---|---|---|---|
| First failing gate | `:chat:jia-chat-service:test --tests cn.jia.chat.archive.service.ArchiveMySqlIntegrationTest`; method `realMysqlSchemaImportRestartConcurrencyMismatchAndDriftFailClosed`; assertion `ArchiveMySqlIntegrationTest.java:88` | Product/API concurrency behavior; not invocation or environment | Analyze blocked worker/thread/DB lock path and make the concurrent import state machine terminate deterministically without weakening mismatch/drift fail-closed semantics |
| Symptom | `pool.awaitTermination(60, TimeUnit.SECONDS)` returned false; log SHA-256 `eb66b6235db72d41552a444f5b3dbe7b0775d9d2ec0738cfc779e50667e8b7c1` | At least one concurrent import worker did not finish in 60 seconds | Add bounded diagnostic regression that proves all futures terminate, rollback/locks/connections release, and mismatch/drift remains denied |
| Infrastructure | MySQL ready, global Gradle lock acquired normally, prepare gate PASS, static PPID=1 unit remained alive to terminal | Infrastructure did not cause the observed assertion | Do not rerun unchanged code or alter systemd/lock policy |
| Cleanup/resources | Secret cleanup PASS; MySQL cleanup PASS; evidence preserved; start free `5412802560` bytes, post-run free `2932166656` bytes | Cleanup contract passed; evidence is authoritative | Preserve R47 evidence. Before any later full rerun restore >=5 GiB without deleting active evidence |

No blind retry is authorized. R48 must first produce a new exact API candidate and update the H06 exact attachment/provenance pin, then run a focused offline concurrency selector through the orchestrator. Only after focused PASS and a fresh review may one new full persistent H06 runtime be authorized.
