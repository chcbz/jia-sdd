# Concurrent integration preflight — 2026-09-13

Read-only forecast at approximately 03:21 UTC. Root fetched the exact public remote commits below using `git fetch --no-tags --no-write-fetch-head origin SHA`; no branch, index or working file changed. `git merge-tree --write-tree --name-only --no-messages` created only unreferenced analysis trees. These are not reviewed integration candidates.

| Repository | Output committed HEAD | Remote develop observed/fetched | Merge base | Textual conflicts |
| --- | --- | --- | --- | --- |
| API | `4c871209c1ea9aa49ec8b669b0d4936a0972b09b` (rejected; repairs uncommitted) | `e54f579e62d7009ab0177aa1074e095eac4ea16e` | `a9d3e7417447a9f5f59a12523e582a8e8f1818f6` | 7 |
| Web | `212bfe4f9441cc82262d98e7b0723d6c0800e3d9` | `edace747484dc01e39664485ec81b6ae2c1fd7b7` | `b31565f8741fdc6f986763dd86442a2c2a4345b0` | 3 |

API forecast tree `786ac052ef3d26f8bf6c08b4af77b9ae0df51e5d`; conflicting paths relative to API:

```text
agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentRuntimeMapper.java
agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java
agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskCollaborationServiceImpl.java
base/jia-base-service/src/main/java/cn/jia/base/filter/UriAccessLogFilter.java
base/jia-base-service/src/test/java/cn/jia/base/filter/UriAccessLogFilterTest.java
common/jia-common-core/src/main/java/cn/jia/core/common/EsRequestWrapper.java
user/jia-user-service/src/main/java/cn/jia/user/config/DefaultSecurityConfig.java
```

Web forecast tree `f8a56a91f0cb60f897d0deb4c729fd46489ffd15`; conflicting paths relative to Web:

```text
src/components/juyiting/BountyPanel.vue
src/composables/useHttp.js
tests/juyiting-component-behavior.test.js
```

## Semantic blockers that textual conflict resolution will not detect

1. API remote adds `agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskArtifactController.java`. Its `POST /agent/tasks/{taskId}/artifacts` has the same JSON consumes/produces mapping as `OutputDeliveryController.publish`. With output enabled, registering both unchanged is ambiguous. The remote adapter authenticates a user JWT and the unique `actorAgentId` query parameter and accepts managed content bytes; OD authenticates a run ticket, requires an idempotency key and publishes already verified artifacts. The agreed compatible route is documented in publication-route-amendment.md; neither credential scheme may become an alternative way to bypass the other's authority. Preserve the existing published Web `useHallArtifactTransfer.js` client behavior. Merely changing a class name or merging without text conflicts does not fix mapping ambiguity.
2. Remote adds `AgentWorkItemPlanServiceImpl`, `AgentWorkItemDependencyServiceImpl` and related controllers/DAOs, plus team recommendations and changes to collaboration state. Plan confirmation can write work-item rows. Include these new entrypoints in policy1 admission/mutation guards and exact single required work-item invariants before claiming OD07's guards cover the integrated application. This is compatibility with existing parallel features; it does not enable deferred P3 or funded R2.
3. Remote Web adds `ArtifactTransferPanel.vue`, task plan/board/team controls and changes shared `useHttp.js`. Retain their identity/transport semantics while preserving OD binary download, source reset, offline retrieval and the new review/rework flow. Full authenticated application startup and actual Hall navigation remain necessary after merging.
4. Remote adds `GET /agent/tasks/{taskId}/artifacts/{artifactId}/versions/{artifactVersion}/content` and `AgentTaskCollaborationServiceImpl.readContent`. The remote method loads `findVersion`, checks only legacy visibility/member rules and can return valid-hash inline content without consulting OD runId/ownerSharedAt/expiry. An OD private candidate defaults to task_members visibility, so applying the old read method unchanged can expose unshared inline content through this alternate endpoint. The integration writer agreed to reject OD-managed rows (`runId != null`) from legacy content reads with NOT_FOUND and test inline/object variants; OD-authorized retrieval uses its own version/download routes. Also test legacy publication against an artifact ID/version already managed by OD to prevent cross-protocol continuation or overwrite. These are identified integration findings, not independently accepted repairs yet.

The sole product writer has received these findings. Freeze/review current OD07 repairs first; integrate the selected API baseline before downstream client/submission implementation to avoid finishing against a contract that cannot be released. Web integration precedes OD10 UI implementation. Recheck remote ancestry again immediately before actual push.

## Follow-up remote API drift observed around 05:18 UTC

API develop advanced to `564e50fa6bb4889d6f0b7221de57b4c22116a810`. Root fetched only that commit object with no branch/index changes. Relative to e54f579e, four commits add command-recovery policy (00adb55d,741cc3f2) and persisted artifact outcomes/HTTP (5bfdb2a8,564e50fa):32 files,4,525 insertions,27 deletions. Web develop remains edace747; client master remains f8c731d0 (main is a separate d3aeeb53 branch).

The new JWT routes are POST `/agent/tasks/{taskId}/artifact-outcomes/accept` and GET `/agent/tasks/{taskId}/artifact-outcomes/accepted`, in `AgentTaskArtifactOutcomeController`. They do not collide textually with OD deliveries, but the service writes ACCEPTED/SUPERSEDED artifact outcomes and events through an independent locked-root path. The observed source has no OD policy/run/owner-share guard. Before integrating, verify policy1 cannot gain a parallel acceptance path and OD-managed private/run-backed rows cannot enter the legacy outcome chain. Preserve legacy policy0 behavior and its JWT actor identity; do not equate single-artifact outcomes with immutable OD08 batches or OD09 owner review.

The sole product writer has this exact baseline queued after the current OD07 client freeze, together with the Rabbit activation lifecycle repair, before OD08. The accepted9ca3eb9f candidate and its passing live retained-output checks remain valid for their recorded scope, but are not yet the final remote-integrated release candidate.
