# OD01 repair candidate verification

Frozen API candidate: `6647ed53fac06c8c7478cf58579c4eadf6f689d0`, parent `8e009b9d241979abb072d4b5b12d42b0476450dc`. Root verified the clean worktree and `git diff HEAD^ --check`. Independent re-review is pending; this is not OD01 acceptance.

| Latest batch | Tests | Failure/error/skip | Scope |
| --- | ---: | --- | --- |
| Agent final batch 02 | 147 | 0/0/0 | Authorization, codec, writer, capture, recovery/reissue, Agent service |
| Chat | 13 | 0/0/0 | Ticket exchange, raw wire, runtime selection and trusted relay scope |
| Transport | 62 | 0/0/0 | Inbox wire/hash and Rabbit decoder/consumer pass-through |
| MySQL | 7 | 0/0/0 | Production output/runtime persistence, current reads, concurrency/CAS and stale-capability renewal |
| H2 transactions/config | 42 | 0/0/0 | Assignment rollback, identity race, transport transaction, events and optional-provider configuration |

The latest groups contain 20 distinct suites and 271 tests. Earlier Agent batch 01 and initial failed batches are excluded from that total. Report bytes were scanned against configured private secret values before root archival; no values are recorded.

`execution-commands.json` preserves the writer's corrected Gradle arguments/exit codes, with selectors checked against XML. Every run was reported to hold `/tmp/cyf-gradle.lock`; MySQL credentials were supplied through the local wrapper's environment. The recorded development OpenCV/JAI substitutions apply; these are not canonical production dependency builds.

## Candidate correspondence and superseded evidence

Agent batch 01 passed, then the writer found that pre-capture run preparation could create an orphan run while the command outbox was disabled. The capture gate and its provider-resolution assertion were corrected and the same 147 tests rerun as batch 02. A duplicate import was also removed. Keep `agent/observation.json` as historical evidence; use `agent-final/observation.json` for this candidate.

After batch 02, the configuration's required output-service dependency was changed to an optional provider. The exact final configuration is covered by the newer H2/config batch, including `dbShadowRegistersWriterWithoutRabbitInfrastructure`. Its snapshot is therefore in `h2-transactional/observation.json`, explicitly excluded from the earlier Agent-final snapshot rather than represented as tested before the change.

`candidate-6647ed53-association.json` is the read-only verifier result for the five latest observations. All 35 distinct recorded source paths match Git objects in the frozen candidate, and every production Java file changed by the repair has a matching snapshot. This establishes report/source correspondence only; the reviewer must still assess test coverage.

## Evidence limits

- MySQL uses real output/runtime mappers with controlled business-source and canonical-identity boundaries; it does not prove the complete assignment transaction.
- `AgentLegacyTaskCompatibilityRealDatabaseTest.precommitFailureAfterMemberLocksRollsBackAssignmentRows` uses H2 `MODE=MYSQL` with real Spring transactions/MyBatis. The validator sees inserted task/member/work-item rows, throws, and all three are absent outside the rolled-back transaction. This is actual persistence rollback evidence, not MySQL lock-semantics evidence.
- Agent service after-commit/runtime-snapshot tests use mocks and explicit transaction synchronization controls; their limits remain distinct from the H2 and MySQL groups.
- Byte-exact evidence composes tested production writer, inbox, consumer and WebSocket boundaries. A live external Rabbit-plus-WebSocket deployment was not exercised.
- Actual HTTP filtering, private storage/scanner, deployed topology, canonical packaging, live client/Web and mobile retrieval remain later-task gates.
