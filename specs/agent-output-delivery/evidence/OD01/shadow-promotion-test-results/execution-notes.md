# OD01 shadow promotion repair evidence

Frozen API candidate: `c5330dd50da6c03e55edca0744485a1b95385552`, parent `6647ed53fac06c8c7478cf58579c4eadf6f689d0`. Only the transport writer and its test changed. Root verified clean status and the two-file diff; independent re-review is pending.

The promotion validator reads and strictly validates the optional persisted context, reconstructs canonical bytes using it, and preserves the original stored outbox entity. New cases exercise enriched and legacy context-free promotion plus rejection of rehashed source-context tampering.

| Latest batch | Result | Boundary |
| --- | --- | --- |
| Service | 32 tests, 0 failures/errors/skips | Writer19, codec8, H2 real transport transaction3, configuration2 |
| Mapper | 6 tests, 0 failures/errors/skips | Existing SQL-annotation mailbox/promotion/CAS contracts |

The separate first writer-only 19-test run is not added again. Per-batch observations preserve XML hashes, source hashes, reported command module/flags/selectors and exit 0. All Gradle invocations were reported to hold `/tmp/cyf-gradle.lock` and use the recorded development dependency init; no credentials are saved. Mapper tests check SQL clauses, while inspection of the actual promotion SQL confirms it changes status/marker/version/update_time only. This is not a live external Rabbit or MySQL promotion test.

`../candidate-c5330dd5-observation.json` combines the newest report for each suite with candidate-matching source snapshots. It explicitly retains the provenance of four superseded suite reports and three older writer-source snapshot entries. The resulting 21 distinct suites contain 280 passing tests; the read-only verifier confirms all 37 source paths match the candidate in `../candidate-c5330dd5-association.json`.

The earlier MySQL controlled-source/identity boundary, H2-versus-MySQL distinction, mocked Agent service synchronization, composed byte-chain evidence and canonical dependency/deployment limitations remain unchanged. No acceptance decision is inferred from passing counters.
