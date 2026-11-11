# MMD-U3-FINALIZATION-API-20260930 API Owner candidate

Date: 2026-09-30 Asia/Shanghai
Owner/profile: `01a0f0d8-8202-7040-9d9c-becce02f7a3f` / `critical_worker`
Branch/worktree: `codex/juyiting-mmd-finalization-v1` / `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-finalization-v1`
Base: `194ec91a596c28f9575a64aef47a5bf7b9fb6778` / tree `10d312e61057b1a83da1485238c2f3acf63e5361`
Candidate: `8d4ab3f82f7e924e561690e758e85a6a33d8493a` / tree `2693f3e247820042325093a4c703d1073685e1dc`

## Implemented

- Exact owner/client/tenant-scoped POST plus read-only operation/original-key GET controller under `/agent/tasks`.
- Immutable canonical request digest and ordered selected-set persistence; binary scope and safe-integer checks.
- Strict persisted request/step/execution/run/output/generation/assignment/grant/MIME/hash/length/byte verification.
- Trusted Agent promotion authority with real required-work-item lease claim/start, private token/version persistence, actual managed artifact publication, formal delivery submit, and actual owner acceptance/task completion.
- Durable phases and replay reconciliation before obsolete lease/grant/source checks; artifact, submit, and accept ACK-loss recovery.
- Current unpaid grant admission without Provider execution or client-supplied producer/run/work-item/lease/storage authority.
- Strict terminal receipt invariant: completed only with `TASK_COMPLETED`, real delivery ID, accepted delivery, completed task.
- Additive default-off Agent and Chat schemas with exact columns/indexes/checks/collations and initializer drift validation.
- Chat finalization initializer directly calls `ChatSchemaReadiness.ensureInitialized()` before source validation and DDL.

## Contract notes

- Necessary truthful domain extension: `deliveryState=changes_requested` may be projected. It becomes a nonretryable failed receipt with `FINALIZATION_DELIVERY_CHANGES_REQUESTED`; it never projects task completion. HTTP POST maps it to 409.
- `Idempotency-Key` is exact safe ASCII format and length 8..160.
- HTTP versions are restricted to 0..9007199254740991 and receipt versions remain decimal strings.
- Request reader has no arbitrary 128 KiB cap. Derived significant JSON maximum is 520,036 bytes; normalized maximum is 1,040,073 bytes. Unbounded insignificant whitespace runs are compacted while preserving one separator so invalid token joining is not accepted. A legal 99-item escaped-Unicode fixture is 371,036 bytes.

## Dependency handoff

This candidate intentionally has a source dependency on schema-readiness commit `79165b93d7dc7c8ecff30376e0ed1622c26591ac` / tree `c073c6def079214beec0d150812b49a9eb3e48c4`, which supplies `cn.jia.chat.config.ChatSchemaReadiness`. Integrate that candidate before compiling this candidate. No Turing-owned initializer path was modified here.

## Focused selectors for serialized main verification

- `:agent:jia-agent-service:mmdU3Finalization`
- `:chat:jia-chat-service:mmdU3Finalization`
- Related broader regression: `:chat:jia-chat-service:chatDeliberation`

Agent focused selector includes:
- `AgentSelectedOutputFinalizationServiceImplTest`
- `AgentTaskExecutionGrantServiceImplTest`
- `AgentSelectedOutputFinalizationSchemaInitializerTest`

Chat focused selector includes:
- `ChatSelectedOutputFinalizationServiceTest`
- `AgentTaskSelectedOutputFinalizationControllerTest`
- `ChatSelectedOutputFinalizationSchemaInitializerTest`

## Owner static self-check

- `git diff --check`: PASS before commit.
- `git show --check 8d4ab3f8`: PASS.
- Forbidden-path scan: no Web/docs/snapshot service/Turing-owned existing initializer changes.
- Standalone `javac` for the three new dependency-free agent-api contract/digest classes: PASS.
- Staged tree before commit exactly matched final tree `2693f3e247820042325093a4c703d1073685e1dc`.
- Worktree clean after commit.
- No Gradle was run, per main-thread serialization instruction.

## Covered adversarial behavior

- Actual happy chain with real mocked protocol calls and no token projection.
- Exact immutable source facts and idempotency conflict.
- Reassignment/grant revocation and current unpaid promotion admission.
- Persisted lease token/version recovery.
- Existing-artifact producer/task/work-item/type/title/visibility/metadata/storage/hash/MIME/length checks.
- Committed replay before obsolete source checks.
- READY/SUBMITTED/ACCEPTED ACK-loss recovery and acceptance-race `changes_requested` truth.
- Forged source/generation/step/output and bytes mismatch rejection.
- Same-stage task projection regression rejection.
- Deliberation/storage failure classification.
- Corrupt terminal receipt rejection without GET repair writes.
- Safe-integer, ID, key, 99-item escaped body and whitespace normalization boundaries.

## Residual verification/migration risks

- No production migration/restart/deploy was performed. Both feature properties remain default off and must be enabled coherently with existing formal-delivery and schema-readiness prerequisites.
- Additive MySQL 8 DDL and initializer metadata queries still require serialized Gradle plus isolated-MySQL verification by the main/test runner.
- Agent artifact publication is intentionally outside the authority/root transaction; recovery is idempotent, not distributed-atomic. Lease expiry during a very long multi-artifact publication can fail closed and require a new explicit operation.
