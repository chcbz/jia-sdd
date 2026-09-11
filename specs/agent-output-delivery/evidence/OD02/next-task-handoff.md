# OD03 preparation — publication and authorized retrieval

Preparation only; OD03 remains not started and depends on an independently accepted OD02 candidate. Keep the single API writer policy. This map was checked against the unchanged publication/workspace code at API `c5330dd5`, while OD02 storage files were in progress; recheck the accepted OD02 interfaces before implementation.

## Reuse and boundaries

Paths below are relative to the API repository.

| Existing seam | Implementation consequence |
| --- | --- |
| `agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentTaskArtifactService.java` | Existing artifact publication/reads use an Agent actor. The new UserJwt read contract must not accept actorAgentId as a way to acquire producer/coordinator privileges. |
| `agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskCollaborationServiceImpl.java` | `publish` enters the task-root transaction; private `publishLocked` validates versions, writes the artifact and appends its event. Its payload validator currently requires exactly content or storageUri. Add the reviewed object-backed path without inventing a storage URI to satisfy the legacy validator. Preserve legacy rows and exact integer-version bounds. |
| `agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentTaskArtifactEntity.java` and `agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentTaskArtifactMapper.java` | Apply the nullable artifact extensions in the root schema contract; preserve the logical version key and exact scoped predecessor locking. New rows choose exactly one of content/storageUri/objectId. |
| `agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskWorkspaceEventValidator.java` | Existing ARTIFACT_PUBLISHED replay validates artifact identity/type/version, legacy visibility, optional workItemId and digest. Reuse that event contract; do not add object keys, tokens or an unrecognized visibility/event type to the replay stream. |
| `agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskWorkspaceController.java` | The legacy browser snapshot requires actorAgentId and the task-events gate. It cannot be the only route for an owner to retrieve explicitly shared files. New owner routes must work with no selectable Agent and with that gate disabled. |
| `agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskWorkspaceServiceImpl.java` and `agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentTaskWorkspaceMapper.java` | Legacy snapshots expose artifact titles and timeline metadata under role-based access. Audit these projections for new output-backed rows so an unshared/private title or event does not leak through this older browser route; checking only the new download controller is insufficient. Preserve legacy behavior where it does not conflict with new output ACL. |
| `chat/jia-chat-service/src/main/java/cn/jia/chat/output/ConversationOutputSourceAuthorizer.java` | Reuse the exact owned-conversation DAO and OD01 source authorization for Agent publication. Keep user read authorization distinct from producer/run write authorization; the Agent module must not import Chat implementation classes. |

## First observable slice

Using the accepted OD02 real-byte fixture, publish one exact task artifact version with explicit OWNER_SHARE and one conversation output. Obtain each through the frozen UserJwt list/detail/download route, close the Agent connection and download again; hash must match the stored fixture. Then prove that changing user/scope/version or omitting OWNER_SHARE rejects access without exposing title/count. These are OD03 checks within the existing O03/O06/O07/O08/O09/O19/O29 scope, not a claim of end-to-end client/Web acceptance.

Implement durable publication receipt, exact source/run/producer/object binding, predecessor CAS and reference creation in one transaction. Wire READ_PIN creation/renewal/release to the accepted OD02 object locking and tombstone GC; no network stream while SQL locks are held. Reuse the canonical signed cursor, expiry and error-envelope rules; never export bucket/key, absolute workspace path or credentials.

Extend the actual HTTP filter-chain tests with exact publication POST ticket routes while list/version/download GET stays UserJwt. Reuse focused regression suites such as `AgentTaskCollaborationServiceRealTransactionTest`, `AgentTaskCollaborationServiceImplTest`, `AgentTaskWorkspaceServiceImplTest`, `AgentTaskWorkspaceMySqlTest` and `AgentTaskWorkspaceControllerTest` where affected. All Gradle invocations hold `/tmp/cyf-gradle.lock`; no test run or passing result is asserted by this preparation note.

OD02's subsequent GC review (`gc-recovery-review.md`) adds a required reference seam: all mutations lock exact object then reference; creation/renewal/adding hold revalidates PASSED/READY, whereas release/expiry/removing hold may perform only monotonic reduction even after DELETING/DELETED. Terminal references never reactivate. Use the shared object lock for publication and READ_PIN race tests; raw SQL inserted before a sequential GC call does not prove this protocol. G01–G03 must be repaired and reviewed in OD02 before relying on that handoff.
