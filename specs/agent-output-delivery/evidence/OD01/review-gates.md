# OD01 implementation review gates

This is a handoff checklist, **not passing test evidence**. The sole API writer supplies a candidate commit and actual test results before independent read-only review. Canonical contracts and `ticket-contract-review.md` remain authoritative.

| Boundary | Required observable evidence |
| --- | --- |
| Persisted source owner | Real task/conversation owner accepted; wrong owner, tenant=0 fallback, case/trailing-space variants and cross-client requests denied. No historical owner backfill. |
| Trusted dispatch | Actual authorized conversation relay and explicitly targeted task command carry server-created context. Forged client context cannot establish source/run/producer. Non-relayed model chat creates no output run. |
| Redelivery | Repeated command/message origin preserves the run and command inbox hash/ACK behavior. Revoked, expired or terminal origin cannot silently start another execution; explicit dispatch uses a new origin. A WS send error with unknown delivery outcome must not revoke a run the Agent may already be executing; verify recovery using the original context. |
| Capability registration | Default-disabled code works against the old schema. Generic runtime ORM writes cannot overwrite capability snapshots. New registration clears stale capability data, including old clients without the extension; delayed old presence cannot restore it. |
| Capability dispatch | Missing, stale (>90 seconds), wrong-runtime and premature R2 capability snapshots cannot enable output dispatch. Existing map/roster abilities remain independent. |
| WS authentication | Only a bound, successfully registered current session obtains a unicast receipt. Raw bearer is absent from database, chat/event broadcasts, prompt and logs. |
| Bearer bootstrap | Only exact SHA-256 ticket hash has a global lookup exception. Request scope cannot redirect the persisted principal. Subsequent ordinary-resource access uses exact persisted scope. |
| Dynamic authorization | Expired/revoked ticket, source, binding or run fails. Immutable owner is rechecked. Same active binding can recover on a newly authenticated runtime without requiring the original runtime or dispatch freshness for every HTTP mutation. |
| Terminal replay | Successful terminal state permits only an existing authenticated receipt replay. It never authorizes a new mutation; revoked identity still rejects replay. OD01 supplies the authorization boundary; real receipt behavior is completed with OD02/OD03. |
| Concurrency | A consistent lock order covers dispatch, issuance, capability registration and revocation. Issuance count plus insert hold the same exact canonical binding lock; simultaneous requests commit at most 60 tickets per binding/minute, and rolled-back issuance consumes no quota. |
| Schema | Opt-in identity migration passes on fresh and upgraded disposable MySQL, repeats safely, and rejects incompatible columns/indexes/engine. Verify the approved non-unique binding-window index and old-schema disabled path. |
| Compatibility | Deferred WS file/result handlers and HTTP file writing remain disabled in OD01. Existing command/auth/chat regressions run where affected. |

Build evidence must identify the local dependency substitutions and lock-held Gradle command. Local MySQL tests do not establish deployed datasource routing or canonical production packaging; those remain OD06/OD11 release gates.

Run each Gradle `test` task with its own selectors in a separate lock-held invocation. A mixed Agent/Chat invocation applied `--tests` only to the last task and accidentally started unrelated Rabbit integration tests; that interrupted batch is excluded from OD01 passing evidence. The subsequent single-task authorization batch passed 12 tests; its working-tree reports and source digests are in `authorization-unit-test-results/observation.json`.
