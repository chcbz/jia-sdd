# Frozen candidate regression

Candidate `7701a5564fd1ab8ec1a3b84568e383d8b7aaf587`: 83 tests across eight suites, zero failures/errors/skips; actual command exit 0. The writer supplied the actual invocation from its tool call in `command.json`; root copied the retained log, exit and XML and independently checked their counts and hashes. The included wrapper holds `/tmp/cyf-gradle.lock` and uses the previously reviewed development dependencies, not a canonical release build.

Root verified the clean frozen candidate before this run. The writer preserved reports before beginning the next repair. No pre-run source hash manifest was generated for this candidate; root extracted the fourteen relevant Git source/test blobs after the run, recording that limitation in `results/observation.json`. `root-association.json` verifies those blobs and archived XML; it is source/report correspondence, not complete compiled-dependency provenance or coverage.

| Suite | Tests |
| --- | ---: |
| OutputObjectSchemaInitializerMySqlTest | 9 |
| OutputUploadSecurityCoexistenceTest | 4 |
| OutputUploadSecurityConfigurationTest | 4 |
| OutputAuthorizationMySqlConcurrencyTest | 10 |
| OutputContentInspectorTest | 9 |
| OutputRunAuthorizationServiceImplTest | 11 |
| OutputUploadRealDependenciesTest | 20 |
| AgentIdentityServiceImplTest | 16 |

Independent review still requires the R01 post-identity-lock recovery clock check and its MySQL barrier test. This batch does not contain that new test and does not establish OD02 acceptance. Earlier overlapping stages and the known full-module Rabbit prerequisite failure are retained separately, not added to these totals. No product test was rerun by root during archival.
