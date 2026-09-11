# OD03 implementation handoff

Prepared while OD02 residual repairs are running. This is not a claim that OD03 has started. The accepted OD02 commit and independent review must be recorded before the sole API writer begins.

Worktree: `/home/chc/wsps/cyf-worktrees/output-api`. Ownership: Agent artifact publication/read services and nullable M002 extensions; Chat output persistence/services; shared authenticated download and cursor helpers; relevant HTTP security routes. Root owns coordination/evidence. Preserve other work and the Agent → Chat dependency prohibition.

Read `../OD02/next-task-handoff.md` for existing code seams, legacy event/privacy hazards and real-MySQL fixture limitations. Use the frozen `../../openapi.yaml`, `../../schema-contract.yaml` and `../../fixtures.json`; do not create another transport contract.

## Required HTTP surface

| Operations | Authentication |
| --- | --- |
| `getOutputCapabilities` | UserJwt |
| `publishTaskOutput`, `publishChatOutput` | RunTicket |
| `listTaskOutputs`, `listTaskOutputVersions`, `getTaskOutputVersion`, `downloadTaskOutputVersion` | UserJwt |
| `listChatOutputs`, `listChatOutputVersions`, `getChatOutputVersion`, `downloadChatOutputVersion` | UserJwt |

All eleven operations must be wired through the actual filter/controller chain. Keep strict request parsing, output error envelopes, request IDs, no-store, and the reviewed credential/ACL/infrastructure error distinction. Capabilities must describe actual availability and write-pause policy; R2 capability remains false.

## Implementation and verification order

1. Add exact scoped business-version persistence and schema validation, reusing OD02 object/reference/receipt primitives. Publish under source/run authorization, predecessor CAS, and atomic version/reference/receipt/event writes. New object-backed rows must not fabricate a legacy storage URI. Inline text receives the same publication ACL and expiry checks.
2. Wire task/chat publication, list, exact-version and download routes. Owner access requires explicit sharing or owned conversation, without actorAgentId, a selectable Agent, an active Agent connection, or the legacy workspace gate. Signed cursors bind scope/source/filter/snapshot; all pages recheck current ACL.
3. Acquire READ_PIN only after business authorization and current version/object validity. Stream outside SQL transactions; enforce the bounded stream deadline, renew/release with the reviewed object → reference lock protocol. Expired business versions do not become accessible through another object's surviving reference.
4. Prove the fixture upload → publication → UserJwt download for each source and compare bytes/hash, then repeat owner retrieval with Agent offline. Exercise both publication replay and response-loss recovery without version increments. The root HTTP probe is available but synthetic probe self-tests are not feature evidence.
5. Add focused real-MySQL race/rollback cases for publication versus GC, predecessor collision, and download pin versus cleanup. Cover cross-user/source/version denials, default-private title/count/event isolation including legacy workspace projections, inline outputs, expired versions, pagination beyond 100 items, legacy body/external-link representations, and write-paused reads. Reuse existing affected regression suites; do not rerun unrelated module tests just to clear old skips.

Keep this one product-code task with one writer. Prefer implementing and testing the shared publication/download path before duplicating source-specific wiring. Freeze one reviewable candidate after the related checks pass; preserve command, exit, XML and candidate correspondence once. Every Gradle invocation holds `/tmp/cyf-gradle.lock`. Independent read-only review precedes OD04.

No endpoint execution or OD03 acceptance is asserted by this handoff. OD06 retains the client/Web, canonical packaging, deployment topology, and actual mobile acceptance gates.
