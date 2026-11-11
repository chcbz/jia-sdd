# UR02 original-source prerequisites handoff — 2026-10-08 21:49 Asia/Shanghai

## Exact source delivery
- Same original Turing/UR02 sole Writer; UR06 Owner previously released. No new Agent/Reviewer.
- Worktree `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008`, branch `codex/ur02-original-source-prereqs-20261008`.
- Base `db0c1628cea6f13123eca5fbcb55914b4834062b` / tree `eecf145b2d2a2a482a43594a996a7d7ad371e671` preserved.
- Candidate `e569762e62decd26b2204132595e0bb6d9c25be1` / tree `c249f6cbe0fc2f764e109e2d9d262988a0f73a12`. Task branch push successful, ls-remote exact SHA matched, WT clean. No further writes planned absent a precise diagnosis.
- Only four frozen existing paths changed. UR06/UR04/UR03 fixture, core exception, mapper schema baseline, D06 service/DAO/transactions, build.gradle/client/root docs/control untouched.

## Paths and SHA-256
- `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentRuntimeV1Controller.java` — `42264d3db8fa8c0e440e74ccc3a8320c190edb61dce50d02c44b2d0a47098de1`
- `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java` — `a1901e022e44ce1e76bfe488b57404dfa2d73e9d339a0651afa4ec2c11bfa3cd`
- `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/api/AgentRuntimeV1ControllerTest.java` — `b7bd9e8867fcbd1a8ee311f4089453d7e6733cab5fbc77bb0bd1bf47fe73481a`
- `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentSchemaInitializerTest.java` — `2c14ff3a0594fddcc0107387b1dd52c90a9837d1579338dd9e855de0f11a33d8`

## Narrow fixes
1. AgentSchemaInitializer: two added source lines only. Both hosted CREATE IF NOT EXISTS and strict expected CHECK map now include original baseline `chk_hosted_single_tenant CHECK (tenant_id = '0')` alongside state/generation/repair. Existing complete table/catalog/index/engine/collation/FK/trigger validation remains intact; exact CHECK equality remains strict. Missing/extra/wrong expressions rejected, including old3. No additive auto-migration of a3-CHECK table, no removed baseline CHECK, no permissive compatibility, no production DDL execution.
2. AgentRuntimeV1Controller: explicit AgentCommandAckRejectedException added to original rejection annotation; handler parameter widened only to common RuntimeException, annotation remains limited to AgentBizException + AgentCommandAckRejectedException (not all runtime errors). Reuses exact original `AGENT_FORBIDDEN` / `Runtime v1 request rejected` / HTTP403 / `private, no-store` response, no reasonCode/message/body/token read or logging. Existing IllegalArgumentException handler still400/no-store. No source/lease/proof/ACL checks or transaction changes.

## Original Owner regressions retained and added
All pre-existing test methods preserved, including original nested sensitive session/enroll serialization, ACK success, install-Bearer400, Origin/legacy query denial, management scope/redaction/revoke, and full initializer identity/task/audit regressions.

Exact main suite selectors (NOT_RUN):
- `cn.jia.agent.config.AgentSchemaInitializerTest`
- `cn.jia.agent.api.AgentRuntimeV1ControllerTest`

Eight added test methods (all NOT_RUN):
- AgentSchemaInitializerTest.hostedProfileInitializerAndFullBaselineDeclareSameFourChecks
- AgentSchemaInitializerTest.hostedProfileStrictCatalogAcceptsExactlyFourChecksOnRepeat
- AgentSchemaInitializerTest.hostedProfileStrictCatalogRejectsEveryMissingCheckIncludingOldThreeSet
- AgentSchemaInitializerTest.hostedProfileStrictCatalogRejectsExtraOrChangedCheckExpressions
- AgentRuntimeV1ControllerTest.d06AckRejectionsHaveOneSafeForbiddenEnvelopeWithoutPrivateReasonOrProof
- AgentRuntimeV1ControllerTest.malformedAckSessionProofStaysBadRequestAndNeverCallsD06
- AgentRuntimeV1ControllerTest.mismatchedAckBodyProofStaysForbiddenAndNeverCallsD06
- AgentRuntimeV1ControllerTest.serviceIllegalArgumentStillUsesBadRequestNotAckForbidden

Schema source-parity test compares parsed balanced real baseline/CREATE clauses; existing catalog unit helper upgraded to4 and parameterized for missing/extra/wrong-expression negative cases, no new lenient stubs. ACK test routes real Controller and original SensitiveResponseBodyAdvice through MockMvc, stubbing only original service unit seam;5 original/synthetic private-reason variants must yield identical generic403 body with no reasonCode/command/request/proof/credential fields. These mocks do NOT substitute for real MySQL/D06/HTTP acceptance. Repeated throwing stubs use doThrow to avoid invocation of a prior throwing stub. Malformed proof uses exactly one invalid generation header, not a duplicate-header accident.

## Checks actually performed / not performed
- Low-cost tree-sitter grammar and Java string escape checks PASS on all4 changed files.
- Static original agent mapper baseline versus initializer CREATE CHECK names/expressions exact4 parity PASS.
- git diff --check and staged diff --check PASS; exact four owned paths PASS; baseline/candidate/remote/clean readback PASS.
- No Gradle/javac/formal typecheck/JUnit, MySQL startup, install, Provider, Flow/service/production action. Eight new tests and related original suites remain NOT_RUN, not claimed compilable solely on grammar.
- No additional writable paths required or new blocker for these two source fixes. Original UR06 source/real7selectors/M4/full Goal validation remains separate and unclaimed.
- Main next action: freeze/cherry this exact patch, perform original Owner suites + validateLayering via orchestrator on new clean input, then actual same-target UR06 enrollment/MySQL verification. Do not change the currently running db0c input or relabel its compile results as this candidate.
