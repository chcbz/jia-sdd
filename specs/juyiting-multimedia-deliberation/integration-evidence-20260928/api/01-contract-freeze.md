# MMD API pre-edit contract freeze — 2026-09-28

Bound to develop `e15e1a9d947e86e5f81a3288948087466a8a879c` / tree `d72e0473ede839f9809b73705ccbc8a1af4fb500`, fast `caee54fc27a08146f9cc57219cf86c763e41c531`, merge base `9a60cac066294d348066acb99ffc628611b85051`.

## API catalog frozen for this merge

Additive durable API from fast branch, while retaining existing `/chat` APIs:

- `POST /chat/stream`, optional `Idempotency-Key`; route is only `CHAT` or authorized `INSPECT`; `EXECUTE`/unknown/conflicting hints fail before conversation mutation.
- `GET /chat/capabilities`.
- `GET /chat/requests/{requestId}`.
- `GET /chat/turns/{turnId}`.
- `POST /chat/turns/{turnId}/cancel`.
- `POST /chat/requests/{requestId}/cancel`.
- `GET /chat/conversation/events?id=...`, additive `cursor` and `Last-Event-ID` replay.
- Existing stop/delete/content/list/update/library endpoints remain source compatible.

Wire additions: `requestId`, `requestRevision`, `interactionHint`/legacy route aliases, `clientSeenVector`, `inputRefs`; deprecated request `senderType`/`senderName` remain accepted but ignored.

## Event/protocol catalog frozen for this merge

- Durable outbox event types: `DISPATCH`, `CANCEL_REQUESTED`, `FINAL_PERSISTED`.
- Persisted conversation event types: `agent_message_delta`, `agent_message`, `resync_required`, `turn_cancelled` (plus migration `recovery_required` compatibility records).
- Agent protocol: `chat.message`, `chat.message.delta`, `chat.dispatch.ack`, `chat.stop`; stable transport `messageId`, business `requestId`, `turnId`, `dispatchId`, exact target/scope, context snapshot ID/hash.
- Existing command/task protocol and native START/ACK semantics are not redefined by this merge.

## Identity/ACL freeze

- Human identity comes only from `HumanSenderIdentityResolver.resolve(EsContext)` and is passed as `ServerResolvedSender`; request body/metadata sender aliases never become persisted or relayed identity.
- Agent identity comes only from authenticated WebSocket session agent ID plus `AgentSenderIdentityResolver` (`runtime.name -> personaName -> authenticatedAgentId`); payload `senderName`/`agentName` never become final/delta identity.
- All durable rows and reads are exact tenant/owner/client scoped, with conversation generation fencing and exact callback binding to conversation/request/turn/dispatch/agent/snapshot/hash.
- Cross-scope failures remain indistinguishable `NOT_FOUND_OR_FORBIDDEN` where applicable.
- `taskMaterials` remain server-resolved, owner/client/task scoped, active-link filtered, opaque references only; they grant no file-read permission.

## Lock order freeze

1. Admission: lock exact live conversation, then lock/find request idempotency row; insert user message/request/snapshot/turn/outbox in that transaction.
2. Turn mutations/final/cancel/publish: visibility read, then lock exact conversation, then lock exact turn; group cancellation locks turns in deterministic query order (`created_at,target_agent_id`).
3. Outbox claim/renew/settle/ACK: lock exact outbox row only, then CAS by version + lease owner + fencing token.
4. External WebSocket/model/SSE delivery must execute outside a database transaction; no lock is held across provider/model/network work.
5. No new cross-domain Agent task/workspace lock is introduced in this integration.

## Transaction boundary freeze

- `admit`: user message + request + all child snapshots/turns/DISPATCH outbox rows are one rollback-on-exception transaction.
- `persistFinal`: authoritative final message + turn CAS + persisted event + FINAL_PERSISTED outbox + aggregate update are one transaction.
- `acceptDelta`, cancel, publish, recovery state, outbox claim/renew/settle/ACK are short independent rollback-on-exception transactions.
- Replay/query methods are read-only transactions.
- Existing native START transaction and task material link transactions remain untouched.

## Sensitive payload allowlists

- Client metadata copies only bounded scalar/list keys from `ConversationMetadataPolicy`; `senderType` and `senderName` stay excluded.
- Server may append authoritative scope/request/route/target/sender fields after copying allowed client metadata.
- Durable dispatch payload contains only exact IDs/scope, current content, bounded allowed metadata, authorized `inputRefs`, source vector and facts manifest. It must not include tokens, cookies, API keys, authorization headers, provider bodies, reasoning, tool stdout/stderr, private absolute paths, or file bytes.
- `taskMaterials` are server-created opaque `{available, taskId, fileIds, unavailableReason}`-style facts, not caller-provided payload.
- User-visible delta/final contains model answer content only; internal trace/tool output is not published.

## Scope decision

This merge fixes only F1 required to preserve current security semantics in the new durable path. F2/F3/F4 remain explicit residual risks and are not represented as complete or release-ready.
