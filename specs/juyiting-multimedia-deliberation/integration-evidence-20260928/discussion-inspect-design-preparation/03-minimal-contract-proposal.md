# MMD discussion/clarification/inspect — minimal next contract proposal

Date: 2026-10-01. **Proposal for Main/API Owner freeze; not an implemented or authorized interface.** It preserves the already frozen schema-3 EXECUTE body/preview/consent/admit contract and adds only DISCUSSION, CLARIFICATION_REPLY, typed outcomes and truthful INSPECT closure.

## 1. One POST, strict schema branches

Keep the single mapping:

```text
POST /chat/conversations/{conversationId}/interactions
Idempotency-Key: <required exact key>
Cache-Control: no-store
```

`ChatBountyInteractionController` remains the sole POST mapping. Schema 2 stays byte/semantic compatible. Schema 3 uses strict per-kind DTOs; unknown or extra fields are rejected rather than ignored. Identity comes only from authenticated JWT tenant plus `EsContext` owner/client and the path conversation. No body field may override tenant/client/owner.

All schema-3 long/revision fields are canonical decimal strings with the field’s real lower bound; do not convert to JavaScript numbers or impose one universal positive rule. `schemaVersion` itself remains numeric `3`. Content is exact Unicode: no trim or normalization before hashing/persistence. Same scoped key plus a different exact normalized kind/content/mode/ref/parent/version body is `409`.

### 1.1 DISCUSSION exact candidate body

```json
{
  "schemaVersion": 3,
  "interactionKind": "DISCUSSION",
  "taskId": "task_1",
  "expectedConversationGeneration": "7",
  "expectedTaskVersion": "0",
  "expectedAssignmentRevision": "0",
  "targetAgentId": "agent_1",
  "content": "再鲜艳一点",
  "referenceMode": "NONE",
  "inputRefs": [],
  "replyTo": null,
  "continuationOf": null
}
```

Exact invariants:

- `replyTo` and `continuationOf` are exactly null.
- `referenceMode=NONE` requires exact empty `inputRefs`.
- `AVAILABLE|INSPECT` requires non-empty strict refs after Main freezes per-capability type/count/media bounds; no silent truncation/deduplication/latest selection.
- The source union reuses exact task-linked workspace versions and current-conversation asset refs. Browser URLs, local paths, hashes, MIME, byte length and producer tuple are not authority.
- DISCUSSION carries no `actionProposal`, `authority`, consent ID or operation-grant ID. A server-created typed proposal is an outcome, not a field the browser can use to self-authorize.

### 1.2 CLARIFICATION_REPLY exact candidate body

```json
{
  "schemaVersion": 3,
  "interactionKind": "CLARIFICATION_REPLY",
  "taskId": "task_1",
  "expectedConversationGeneration": "7",
  "expectedTaskVersion": "0",
  "expectedAssignmentRevision": "0",
  "targetAgentId": "agent_1",
  "content": "用上一稿，颜色更鲜艳",
  "referenceMode": "AVAILABLE",
  "inputRefs": [
    {"kind":"CURRENT_CONVERSATION_ASSET","assetRef":{"assetId":"ast_1","revision":"1"}}
  ],
  "replyTo": {
    "requestId": "request_waiting",
    "stepId": "step_waiting",
    "clarificationRevision": "1"
  },
  "continuationOf": null
}
```

Exact invariants:

- `replyTo` is required and has exactly three fields. It must resolve to one open `WAITING_USER` pending question in the same authenticated scope, conversation generation, task, target and assignment.
- `clarificationRevision` is an exact CAS. Closed, superseded, already-answered, wrong-parent or changed-revision replies are conflict/not-found-safe and create no resume.
- `continuationOf` is exactly null; clarification reply and execution lineage are not interchangeable.
- The reply transaction persists the user message, closes the exact pending question once, and persists a resume fact. It does not itself create a consent, operation grant, execution, command or START.
- If the pending step belongs to an **initial explicit point-and-start intent that has never reached RESERVED/CONSUMED**, resume may continue that same intent only after all original authority/currentness facts are revalidated. This is not permission to reuse a consumed initial consent and not permission for a later new edit/regeneration.
- A later follow-up proposal always requires its own EXECUTE keys and the frozen preview/issue/admit flow.

### 1.3 EXECUTE remains frozen

Do not redefine it here. The exact `interactionKind=EXECUTE` body, source union, preview, provider-consent issue/recovery/revoke, final admit response and `GET .../interactions/request` semantics remain those in `controlled-image-followup-owner-contract-v1.md` and its prioritized base/owner decisions. In particular, EDIT requires exactly one current-conversation asset, exact continuation parent, a fresh per-intent operation grant/consent, and one START.

## 2. Admission response and original-key recovery

Candidate DISCUSSION/CLARIFICATION_REPLY accepted projection has exactly these fields:

```json
{
  "schemaVersion": 3,
  "interactionKind": "DISCUSSION",
  "requestId": "request_...",
  "userMessageId": "message_...",
  "stepId": "step_...",
  "state": "RECEIVED",
  "stateVersion": "0",
  "eventCursor": "...",
  "statusUrl": "/chat/requests/request_...",
  "replay": false
}
```

For a clarification reply, `interactionKind` is `CLARIFICATION_REPLY`; all other field names remain exact. POST returns `202`; exact replay may return `200` or the frozen convention Main chooses, but the projection bytes/semantics must be the persisted original fact and `replay=true`. EXECUTE keeps its already frozen exact projection.

Keep the frozen read-only recovery path for every schema-3 kind:

```text
GET /chat/conversations/{conversationId}/interactions/request
Idempotency-Key: <the original interaction key>
```

No query and no body. Response uses `Cache-Control: private, no-store`. It returns only the persisted admission projection for that scoped key. It performs zero task/link/message/request/step/event/outbox/consent/grant/execution/run/lease/START writes and does not re-resolve refs or dispatch a model. Owner-safe `404` means “not observable now”, **not proof the POST was never accepted**. Unknown transport outcome therefore stays on the same key/body and first performs this GET; it never changes key, removes refs, downgrades to schema 2/legacy, or creates fresh authority.

Current state, pending question and typed outcome remain on the authenticated status projection at `statusUrl`; original-key GET is recovery, not a mutating status poll.

## 3. Strict reference modes

### NONE

- `inputRefs=[]` exactly.
- No source catalog or content read.
- Suitable for ordinary discussion and text-only clarification.

### AVAILABLE

- Resolve each exact ref under current authenticated scope/task/conversation/assignment ACL.
- Freeze a metadata snapshot and expose only bounded `availableRefs`: source identity/revision, media classification and server facts required by the eventual capability contract.
- Do not open, download, materialize, hash anew, stage or send referenced bytes to Client/model.
- AVAILABLE can help identify “the previous output” for a proposal, but it does not prove the model saw the image.

### INSPECT

- Requires an explicit `referenceMode=INSPECT`, exact refs, current ACL, an immutable server manifest, and a target runtime whose exact registered INSPECT capability covers every source/media kind.
- API materializes only the fixed authorized manifest; Client may read only that manifest through the dedicated inspection adapter. Generic workspace/Codex execution, routing tags and browser preview are not substitutes.
- The inspection result is a discussion answer or typed clarification/proposal. INSPECT creates no controlled-image claim, Provider consent, operation grant, execution, command or START and cannot consume image-generation permission.
- If capability is absent, source is unreadable, or any ref is stale, reject/clarify; do not silently fall back to AVAILABLE while claiming inspection.

## 4. Durable typed outcomes

Extend the authenticated request/status projection with exactly one nullable `outcome` and one nullable `pendingQuestion`. Candidate strict union:

```json
{"kind":"ANSWER","messageId":"message_answer"}
```

```json
{
  "kind":"CLARIFY",
  "pendingQuestion": {
    "requestId":"request_...",
    "stepId":"step_...",
    "clarificationRevision":"1",
    "question":"你想修改哪一张当前会话图片？",
    "required":["EXACT_CURRENT_CONVERSATION_ASSET"]
  }
}
```

```json
{
  "kind":"EXECUTION_PROPOSAL",
  "proposalId":"proposal_...",
  "proposalRevision":"1",
  "operation":"EDIT_IMAGE",
  "instruction":"再鲜艳一点",
  "sourceRefs":[
    {"kind":"CURRENT_CONVERSATION_ASSET","assetRef":{"assetId":"ast_1","revision":"1"}}
  ],
  "sourceDigest":"...",
  "continuationOf":{"requestId":"request_previous","stepId":"step_previous"},
  "authorizationState":"REQUIRED"
}
```

`EXECUTION_PROPOSAL` is immutable planning data and explicitly **not authority**. Web may display it and seed the frozen EXECUTE preview body, but actual external/paid work starts only after the current user confirms this exact proposal/source/strategy and the server issues a fresh consent/operation grant. Proposal IDs/revisions are server facts; models and browsers cannot sign authority.

A pending-question record minimally binds scope, conversation/generation, task/assignment/target, request/step, clarification revision, question/required facts, resume-context digest, state (`OPEN|ANSWERED|SUPERSEDED|CANCELLED`) and state version. A proposal record minimally binds the same causal scope plus operation, exact source snapshot/digest, instruction and parent lineage. Use strict unique/CHECK/FK constraints; do not store these only in JSON event text.

### Typed Client result, not prose parsing

Current Client has no typed result channel. Candidate additive sibling runtime event:

```json
{
  "messageType":"chat.interaction.outcome",
  "schemaVersion":1,
  "tenantId":"...",
  "clientId":"...",
  "targetAgentId":"...",
  "conversationId":"...",
  "requestId":"...",
  "turnId":"...",
  "dispatchId":"...",
  "outcome":{"kind":"CLARIFY","question":"...","required":["EXACT_CURRENT_CONVERSATION_ASSET"]}
}
```

The API accepts it only from the authenticated currently bound target/dispatch and validates the strict outcome union against the server snapshot. It derives IDs, scope, source descriptors and digests itself. An `EXECUTION_PROPOSAL` from Client may propose operation/instruction and choose only refs already present in the authorized context; it cannot provide grant/consent/model/account facts. Plain `chat.message` text remains an ANSWER body and is never reparsed as a proposal.

Main may choose a different exact event name during freeze, but a structured authenticated channel is mandatory if planning occurs in Client. Deterministic API routing may persist the same typed union without invoking Client at all.

## 5. Natural multi-round closure

### “再鲜艳一点”

1. Admission fixes current conversation/task/assignment/target and the user message.
2. Server causality/metadata finds the directly focused prior output and exact current-conversation asset.
3. If exactly one editable image is in focus, create an `EDIT_IMAGE` proposal with that asset and prior producer request/step. No model is required merely to discover the source.
4. If semantic interpretation is needed, an optional constrained planner returns a typed proposal; it cannot authorize it.
5. If source focus is absent/ambiguous, persist `CLARIFY` before execution reservation.
6. User accepts the exact current proposal; Web starts a **new** frozen EXECUTE preview/consent/admit flow with new keys and authority.

### “换成黄鹂”

Use the same source/causality rules. When one exact current image is focused and the text clearly changes its subject, propose `EDIT_IMAGE`; otherwise clarify which image or whether the user means a new generation. Do not guess between GENERATE and EDIT from a routing label alone.

### First point-and-start

If the user’s original point-and-start action already binds an exact explicit generation intent and all required facts/authority/capability are present, execute directly; do not force a CHAT/planner turn. If essential information is missing, persist a question before RESERVED/START. A reply can resume that same still-live initial intent; after it is consumed/completed, “again/change/edit” is a new intent with new consent/operation grant/command/START.

## 6. State, events and recovery

Candidate additive event facts (names to freeze, semantics required):

- `interaction.accepted` — immutable kind/mode/body digest and causal IDs.
- `reference.catalogued` — AVAILABLE metadata snapshot only; explicitly `bytesRead=false`.
- `reference.materialized` — INSPECT fixed manifest, exact snapshot digest and capability; never emitted for AVAILABLE.
- `clarification.requested` — question ID/revision and request/step enters `WAITING_USER`; execution lease/reservation absent.
- `clarification.answered` — exact reply request and pending CAS closes once.
- `interaction.resumed` — resume parent/child and new state version; not authority.
- `interaction.outcome` — strict ANSWER/CLARIFY/EXECUTION_PROPOSAL projection.
- Existing execution/asset events remain authoritative for START/output; a proposal event is never an execution event.

`WAITING_USER` is non-terminal but replyable. Web busy state must separate “execution genuinely occupies a lease” from “question awaits user”. Refresh reconstructs pending question/proposal from API rows/events, not session memory. Late events and reads are fenced by identity/auth generation, conversation generation, request/step and state version.

## 7. Required rejection branches

- Unknown/extra field, wrong schema/kind/mode combination, noncanonical revision, empty/invalid exact content per frozen text rule.
- JWT/EsContext/path/task/target/conversation/generation/assignment mismatch: owner-safe not-found or typed conflict without leakage.
- Same key with changed content, mode, ref order/set, ref revision, reply parent, continuation parent, or version.
- `NONE` with refs; AVAILABLE/INSPECT with invalid or stale ref; browser path/URL/hash/producer metadata supplied as authority.
- AVAILABLE causing any byte/materialization call.
- INSPECT routed to a target without exact current capability, or any manifest/source mismatch.
- DISCUSSION carrying execution authority/action fields; CLARIFICATION_REPLY without one exact open question; reply to answered/superseded/wrong revision question.
- Plain final text treated as typed proposal; proposal treated as consent; old/consumed consent reused; initial GENERATE grant used for EDIT.
- Ambiguous “再鲜艳一点/换成黄鹂” silently selecting a source/operation.
- Network/ACK unknown causing a new key, second dispatch, second consent, second START, or Provider retry.
- Reassignment, revoke, current requirement drift, target capability drift or stale source after proposal/clarification.

## 8. Minimum regression set

### API transaction/auth/schema

1. DISCUSSION/NONE happy path and exact replay; same key changed Unicode/null-vs-empty/mode/ref/parent gives 409.
2. Cross tenant/client/owner/path/task/target is indistinguishable owner-safe 404; no leaked IDs.
3. AVAILABLE with image/audio/text/file exact refs produces metadata only; instrumented byte reader count remains zero.
4. INSPECT rejects disabled/unsupported target and never creates execution/consent/START rows.
5. Real INSPECT fixture, once implemented, proves exact manifest bytes, ACL, MIME and no execution side effects.
6. Pending question creation transaction; failure after question/message/event insertion rolls all back.
7. One exact clarification reply closes once and resumes; duplicate exact replay is stable; competing replies have one winner.
8. WAITING_USER has no execution reservation; reassignment/revoke between question and reply prevents unsafe resume.
9. Typed Client outcome accepts only exact authenticated dispatch and strict union; prose cannot create proposal.
10. Original-key GET has zero writes/timestamp changes; 404 does not trigger replacement POST.
11. Existing schema-2 and frozen schema-3 EXECUTE MVC/body/hash fixtures remain byte/semantic compatible.

### Client

1. Existing CHAT text/delta/final remains unchanged when no typed outcome is requested.
2. Strict typed outcome parser rejects unknown fields/kinds, unauthorized refs and scope/dispatch mismatch.
3. AVAILABLE context never invokes a byte reader.
4. INSPECT stays unadvertised until an actual adapter plus manifest tests pass; labels/generic executor cannot enable it.
5. Dual profiles cannot reuse each other’s home, manifest, source files, thread binding or result.

### Web

1. `WAITING_USER` enables only exact reply/discussion actions while execution-busy remains blocked.
2. Reply UI visibly binds request/step/revision; cancel/scope change clears it without sending.
3. Composer and output card both use one follow-up lane; output card no longer performs independent POST/recovery.
4. AVAILABLE sends strict refs but does not claim “已查阅”; INSPECT requires explicit user action/capability.
5. Proposal card shows exact operation/source/parent and requires current explicit acceptance before frozen EXECUTE flow.
6. “再鲜艳一点/换成黄鹂” one-source case renders proposal; zero/multiple-source case renders clarification.
7. Unknown POST uses same-key GET and never automatically resends/changes body; stale responses are fenced.
8. Initial explicit authorized generation can proceed without mandatory planner; missing facts display pending clarification.

## 9. Suggested exact later Owner path sets

These are proposed allowlists to freeze separately; they are not permission in this prep task.

### API owner candidate

Existing paths:

- `chat/jia-chat-service/src/main/java/cn/jia/chat/api/ChatBountyInteractionController.java`
- `chat/jia-chat-service/src/main/java/cn/jia/chat/api/ChatController.java`
- `chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyDiscussionAdmissionService.java`
- `chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationService.java`
- `chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java`
- `chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentRuntimeCapabilities.java`
- `chat/jia-chat-mapper/src/main/java/cn/jia/chat/deliberation/ChatDeliberationDao.java`
- `chat/jia-chat-mapper/src/main/java/cn/jia/chat/deliberation/ChatDeliberationDaoImpl.java`
- `chat/jia-chat-mapper/src/main/java/cn/jia/chat/deliberation/ChatDeliberationMapper.java`
- `chat/jia-chat-mapper/src/main/resources/db/chat-deliberation-schema.sql`
- `chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatDeliberationSchemaInitializer.java`

Additive candidates under the same packages: strict schema-3 discussion/reply DTO, `ChatBountyFollowupAdmissionService`, reference snapshot/resolver, pending-clarification/proposal entities/DAO mapping, and focused controller/service/transaction/schema tests under `src/chatDeliberationTest`. Do not modify initial point-and-start, frozen EXECUTE authority, Agent grant/native Provider code, voice, formal delivery or production migration in this package unless Main separately expands the matrix with evidence.

### Client owner candidate

- `conf/codex-ws-agent/agent-client.mjs`
- `conf/codex-ws-agent/chat-runtime.mjs`
- `conf/codex-ws-agent/app-server-adapter.mjs`
- additive typed-outcome and fixed-manifest-inspect modules under `conf/codex-ws-agent/`
- focused `conf/codex-ws-agent/test/agent-client.test.mjs`, `chat-runtime.test.mjs`, and new typed-outcome/inspect tests

Do not modify or enable `controlled-image-bounty-v3-capability.mjs` merely to claim INSPECT. Controlled execution remains a separate sibling capability.

### Web owner candidate

- new `src/composables/juyiting/useHallBountyFollowup.js` plus a pure strict wire/recovery helper
- `src/composables/juyiting/useHallConversation.js`
- `src/composables/juyiting/hallDeliberationState.js`
- `src/composables/juyiting/hallMultimediaDeliberationUi.js`
- `src/components/juyiting/HallChatComposer.vue`
- `src/components/juyiting/BountyDiscussionPanel.vue`
- `src/components/juyiting/BountyExecutionOutputs.vue`
- minimal `src/components/world/JuyiHall.vue` wiring
- focused `tests/juyiting-hall-conversation.test.js`, `tests/juyiting-multimedia-deliberation-ui.test.js`, and new follow-up wire/recovery tests

Keep one orchestrator: composer and output card submit structured intents through the same composable. Do not treat local selected agent/task, a routing label, or browser media as server authority.

## 10. Main/API Owner decisions still required

1. Freeze the exact DISCUSSION/CLARIFICATION body fields, response status convention, strict JSON unknown-field policy and per-field text/null rules.
2. Freeze non-execution ref unions, ordering, actual media/count/byte bounds from real INSPECT capability rather than borrowing the image execution limit.
3. Choose and freeze the typed Client outcome event name/schema and whether deterministic API planning is sufficient for the first package.
4. Freeze pending-question/proposal tables, state transitions, lock order and request/status projection shape.
5. Define the actual INSPECT adapter, manifest transport, sandbox/tool policy and evidence required before capability advertisement.
6. Define how an unconsumed initial point-and-start intent enters WAITING_USER and resumes without turning old/consumed authority into a new intent grant.
7. Freeze exact Owner path matrices and real MySQL/transaction/browser/Client integration fixtures.

No decision above may authorize paid/external execution by natural language, a proposal, a routing tag, or this document.
