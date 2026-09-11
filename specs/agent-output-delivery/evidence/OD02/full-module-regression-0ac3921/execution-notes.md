# OD02 candidate 0ac3921 execution notes

Candidate: `0ac392156627d231ceb2fcb408e938bd877271b4`  
Base: `c5330dd50da6c03e55edca0744485a1b95385552`  
Worktree: `/home/chc/wsps/cyf-worktrees/output-api`  
Evidence root: `/tmp/cyf-od02-evidence/full-module-regression-0ac3921`

The worktree was clean at the candidate when these reports were archived. The full-run shell command and process exit code were not retained in the inherited runner session or JUnit artifacts. They are recorded as unavailable rather than reconstructed from environment variables. No test was rerun only to improve bookkeeping. The known run constraints were the global `/tmp/cyf-gradle.lock`, `--no-daemon`, `--max-workers=1`, the 512 MiB/256 MiB JVM limits, Java from `/home/chc/.local/share/cyf-output-tools/java`, and the development-only init `/home/chc/.local/share/cyf-output-tools/od00-development-opencv-substitution.init.gradle`.

## Full module reports

- `:agent:jia-agent-core:test`: no test sources/reports.
- `:agent:jia-agent-mapper:test`: 153 tests, 0 failures/errors/skips.
- `:agent:jia-agent-service:test`: 1236 tests, 1 failure, 0 errors, 103 skipped.
- All 22 mapper and 112 service XML reports are preserved under `raw/`.
- This is not recorded as a green full-module run.

## Candidate output subset

The 16 output-related suites that actually ran non-skipped contain 69 tests, all passing. Their reports are under `candidate-output-nonskipped/`. `association.json` verifies all report bytes and 66 source snapshots against candidate `0ac3921`; this proves correspondence only, not coverage or release readiness.

| Suite | Tests | F/E/S | Timestamp UTC | XML SHA-256 |
| --- | ---: | --- | --- | --- |
| `cn.jia.agent.output.service.OutputUploadRealDependenciesTest` | 15 | 0/0/0 | `2026-09-11T05:52:46.278Z` | `2a3c9a18a8c8102bdeb6001822e095f1c55525837d05a51f20c867cc428806d8` |
| `cn.jia.agent.output.service.OutputAuthorizationMySqlConcurrencyTest` | 8 | 0/0/0 | `2026-09-11T05:51:50.334Z` | `10d22b5023a64c1a156cd4f99a1fff55a8d5e9ffc6e7bd3f62c20bd4be54bdfb` |
| `cn.jia.agent.config.OutputUploadSecurityCoexistenceTest` | 4 | 0/0/0 | `2026-09-11T05:51:31.933Z` | `e17366309ac07debd2f2205ff8a4a73806d6d6f5a04381984c95d4a622d60e94` |
| `cn.jia.agent.output.service.OutputContentInspectorTest` | 6 | 0/0/0 | `2026-09-11T05:52:37.505Z` | `c0ab572d0149f696662d00be40ad23ca5c334708bacb5903b4390b22675b4642` |
| `cn.jia.agent.output.service.ClamAvOutputMalwareScannerTest` | 1 | 0/0/0 | `2026-09-11T05:51:50.255Z` | `e3af6f3fb5f06b98ab0ceeb63088fa7765b316c1b06196b0776ab83f680f511c` |
| `cn.jia.agent.config.OutputObjectSchemaInitializerMySqlTest` | 2 | 0/0/0 | `2026-09-11T05:51:27.910Z` | `9e53c6508611eb2165c6267371c786336df93d1d30729aadab0390d7ba7a7208` |


The full-run `OutputUploadRealDependenciesTest` is the candidate-corresponding rerun after the unused DAO `markObjectDeleting` declaration/implementation was removed. It supersedes the prior GC15 report only for strict source/report association. The earlier report remains valid historical execution evidence with its recorded source mismatch; it is not silently relabeled.

## Preserved environment failure

`cn.jia.agent.service.impl.AgentCommandDlqRedriverRabbitIntegrationTest` has 1 test and 1 failure at `2026-09-11T05:53:48.636Z`; XML SHA-256 `b2ada5dcb194a30f2003d468443349f02b27324c2f68eea3a54d4e9773581b66`. The assertion requires the exact executable `/home/isp/apps/rabbitmq/sbin/rabbitmq-server` and RabbitMQ 3.6.11 fixture. This test source is byte-unchanged from base `c5330dd5` to candidate `0ac3921`.

The suppressed `/proc/8150/stat` absence is retained in the raw XML and is not treated as proof that this OD02 run changed host Rabbit state. OD02 archival did not install RabbitMQ, restart a broker, mutate production topology, or execute production DML.

## Credential and scope limits

`credential-scan.txt` records no configured high-risk Maven/MySQL/MinIO password/access-key/secret-key value and no signed-URL credential marker in the copied XML. Secret values were read only in-process for comparison and were not printed or stored.

Canonical dependency packaging remains pending because the private repository TLS issue is unresolved. Production migration, deployment, owner publication/download, browser UI and live end-to-end retrieval are outside OD02 and remain later serial tasks.
