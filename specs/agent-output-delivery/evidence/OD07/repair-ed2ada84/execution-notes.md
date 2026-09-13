# OD07 repair execution and evidence association

Candidate `ed2ada849cd7f06eac4e217641c70dafffaca54e`; independent review pending. Original report/log bytes are retained. Counts are per invocation; do not add prior or UP-TO-DATE results as new tests.

Both invocations used `/home/chc/wsps/cyf-worktrees/output-api` and the existing `/tmp/cyf-od02-evidence/run-gradle-with-od-env.py` wrapper. The operator reports unchanged local JDK, OD01/OD02 MySQL and OD02 MinIO/Clam environment. Actual MySQL suite uses `OD01_MYSQL_*`. The 29-suite invocation inherits these variables but contains no actual conditional MySQL suite; its RealDatabase/RealTransaction helpers remain component/H2 evidence.

The wrapper holds `/tmp/cyf-gradle.lock`, invokes `./gradlew --include-build plugin --init-script /home/chc/.local/share/cyf-output-tools/od00-development-opencv-substitution.init.gradle --no-daemon --max-workers=1`, with `-Dorg.gradle.jvmargs=-Xmx512m -XX:MaxMetaspaceSize=256m` as one argument. This is a development dependency path, not a canonical package build.

Actual MySQL invocation (4/4, no skips):

```text
python3 /tmp/cyf-od02-evidence/run-gradle-with-od-env.py :agent:jia-agent-service:test --tests cn.jia.agent.service.impl.OutputDeliveryPolicy1MySqlIntegrationTest
```

Affected invocation (442/442, 29 suites, no skips), reconstructed from the operator-confirmed full selector list in the original `affected/writer-observation.json`:

```text
python3 \
  /tmp/cyf-od02-evidence/run-gradle-with-od-env.py \
  :agent:jia-agent-service:test \
  --tests cn.jia.agent.api.OutputLeaseControllerTest \
  --tests cn.jia.agent.config.OutputUploadSecurityCoexistenceTest \
  --tests cn.jia.agent.config.OutputUploadSecurityConfigurationTest \
  --tests cn.jia.agent.output.service.OutputLeaseFixtureContractTest \
  --tests cn.jia.agent.output.service.OutputLeaseServiceImplTest \
  --tests cn.jia.agent.output.service.OutputRunAuthorizationServiceImplTest \
  --tests cn.jia.agent.service.funding.FundedBountyQuoteClaimRealTransactionTest \
  --tests cn.jia.agent.service.funding.FundedBountyQuoteClaimServiceTest \
  --tests cn.jia.agent.service.funding.FundedBountyServiceRealTransactionTest \
  --tests cn.jia.agent.service.funding.FundedBountyServiceReplayTest \
  --tests cn.jia.agent.service.funding.FundedBountySettlementDeliveryPolicyGuardTest \
  --tests cn.jia.agent.service.funding.FundedBountySettlementRealTransactionTest \
  --tests cn.jia.agent.service.impl.AgentCommandCanonicalCodecTest \
  --tests cn.jia.agent.service.impl.AgentCommandTransportCaptureConstructorContextTest \
  --tests cn.jia.agent.service.impl.AgentCommandTransportCaptureTest \
  --tests cn.jia.agent.service.impl.AgentCommandTransportRealTransactionTest \
  --tests cn.jia.agent.service.impl.AgentCommandTransportWriterImplTest \
  --tests cn.jia.agent.service.impl.AgentLegacyTaskCompatibilityEventTest \
  --tests cn.jia.agent.service.impl.AgentLegacyTaskCompatibilityRealDatabaseTest \
  --tests cn.jia.agent.service.impl.AgentServiceImplTest \
  --tests cn.jia.agent.service.impl.AgentTaskAggregationDeliveryPolicyGuardTest \
  --tests cn.jia.agent.service.impl.AgentTaskAggregationRealDatabaseTest \
  --tests cn.jia.agent.service.impl.AgentTaskCollaborationServiceImplTest \
  --tests cn.jia.agent.service.impl.AgentTaskCollaborationServiceRealTransactionTest \
  --tests cn.jia.agent.service.impl.AgentTaskStateServiceImplTest \
  --tests cn.jia.agent.service.impl.AgentTaskStateServiceRealTransactionTest \
  --tests cn.jia.agent.service.impl.AgentWorkItemLeaseRealDatabaseTest \
  --tests cn.jia.agent.service.impl.AgentWorkItemLeaseServiceImplTest \
  --tests cn.jia.agent.service.impl.AgentWorkItemResultCommitServiceImplTest
```

Root independently parsed all XML and verified the candidate Git diff SHA256 matches the operator's MySQL execution-time observation `37ef8b6985e5f64636e46dc9a41cd16d8398735a83392cc89d96aff83602e54c`. For 442, only the original observation's patch hash `5ad51a2e3afbf07a4eb5fb6241fbc436afc70159b93c841234bccbf127298d8c` was retained; no old patch or per-file runtime source snapshot exists. The sole writer attests that only the MySQL test was subsequently strengthened and no production source changed. Root does not claim independently reconstructing that intermediate patch. The final strengthened MySQL test passed 4/4, including transactional outbox/receipt rollback and attempt-limit recovery checks; independent review assesses coverage.

`mysql-final-ed2ada84.log` is only an UP-TO-DATE confirmation and is not counted as another execution. Earlier failed fixture-hardening attempts remain with the operator; they are not relabeled as passing. Live HTTP, the new remote integration paths, client behavior and release remain separate gates.
