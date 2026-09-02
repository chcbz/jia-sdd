# 聚义厅语音对话 design

## 1. Architecture

```text
HallChatComposer ─┐
                  ├─> one JuyiHall-owned voice state machine
HallVoiceHud ─────┘      │
                         ├─ getUserMedia + MediaRecorder
                         ├─ POST /chat/speech/transcriptions
                         ├─ transcript review / countdown auto-send
                         └─ existing explicit /chat/stream send path
                                      │
                                      └─ final assistant text
                                            └─ POST /chat/speech/synthesis
                                                   └─ audio playback
```

Text remains canonical. Speech input and output are presentation/transport layers around the existing Juyi Hall chat contract.

## 2. User flow

### 2.1 Recording

1. User clicks microphone in Composer or landscape HUD.
2. Client freezes draft and full send context, allocates `turnId` and increments generation.
3. Permission is requested from a direct user gesture.
4. While recording, map interaction, draft edits, target changes, new-conversation actions and send actions are disabled.
5. User stops/cancels, or client stops at 45 seconds/5 MiB.
6. Client stops all tracks, constructs Blob, uploads multipart with AbortController.

### 2.2 Manual send policy

- Transcript is shown in a review surface outside the Composer submit form.
- Empty draft: `写入草稿`.
- Existing draft: `追加` or `替换`, each explicit.
- Combined content above 1200 characters is not silently truncated.
- User edits and sends through the existing text path.

### 2.3 Countdown auto-send policy

- Auto-send is opt-in and disabled by default.
- On successful transcription, perform CAS against the frozen draft/context.
- If valid, show transcript with a 1500 ms countdown and `取消`/`立即发送`.
- At expiry, call the existing send path with explicit `{content, contextSnapshot, source:'voice', turnId}`.
- Any mismatch, visibility loss, route change, provider unknown state, length violation or active send cancels auto-send and opens manual review.
- Auto-send sends a chat message only. Existing server-side confirmation remains mandatory for task assignment or other high-impact actions.

### 2.4 Voice reply

- `replyVoiceEnabled` is opt-in and independent of hall sound preference.
- After `/chat/stream` finishes, select the final non-user text message belonging to the current turn.
- Call synthesis with bounded text and configured voice.
- Play returned audio; failure only reports a non-blocking voice error.
- Starting a new recording stops current playback.
- V1 does not perform sentence-level streaming TTS or full-duplex interruption.

## 3. Frontend state contract

```text
unsupported
idle
requesting_permission
recording
stopping
transcribing
pending_send
review
conflict
sending
waiting_reply
synthesizing
speaking
error
```

A generation token fences all async callbacks. `cancel()` increments generation, aborts upload/TTS, clears timers, stops recorder when active, stops every MediaStream track, stops audio playback and ignores stale callbacks.

### 3.1 Frozen context

```json
{
  "draft": "",
  "draftRevision": 12,
  "conversationId": "123",
  "conversationScopeType": "private",
  "conversationScopeKey": "agent:a1",
  "mode": "private",
  "targetAgentIds": ["a1"],
  "targetAgentId": "a1",
  "participantAgentIds": ["a1"],
  "mentionAgentIds": [],
  "selectedAgentId": "a1",
  "selectedTaskId": null,
  "taskId": null,
  "outgoingMetadata": {}
}
```

String arrays are normalized and sorted. Metadata is deep-copied and compared using stable key order. `conversationId`, draft text and draft revision are part of CAS.

### 3.2 Locks

`voiceInteractionLocked` is true from permission request through transcription/countdown/review until apply/discard/error cleanup. `JuyiHall` passes:

```text
Boolean(activePanel) || voiceInteractionLocked
```

to stage interaction lock. HUD prevents pointer/keyboard propagation. Hall sound effects are transiently suppressed without changing the persisted sound setting.

### 3.3 Landscape HUD

- Visible only in landscape scene mode with chat panel closed and voice enabled.
- Displays explicit target label, recording timer, stop/cancel and countdown state.
- Hides when a chat panel opens; Composer then controls the same state.
- Review/conflict opens the chat panel without resetting the frozen discussion context.

## 4. API contract

### 4.1 Transcription

```http
POST /chat/speech/transcriptions
Authorization: Bearer <JWT>
Content-Type: multipart/form-data
```

Parts:

| Field | Required | Contract |
| --- | --- | --- |
| `audio` | yes | one file, max 5 MiB |
| `requestId` | yes | 16-128 safe ASCII characters |
| `language` | no | allowlisted, default `zh-CN` |
| `durationMs` | no | client observation only; never authoritative |

Success:

```json
{
  "code": "E0",
  "msg": "ok",
  "status": 200,
  "data": {
    "requestId": "01...",
    "text": "请林教头查看榜文",
    "detectedLanguage": "zh",
    "durationMs": 8120
  }
}
```

The endpoint rejects conversation, target, task, provider, model, URL and prompt fields.

### 4.2 Synthesis

```http
POST /chat/speech/synthesis
Authorization: Bearer <JWT>
Content-Type: application/json
```

V1 request:

```json
{
  "requestId": "01...",
  "text": "林冲领命。",
  "voice": "juyiting-default",
  "format": "mp3"
}
```

- Text maximum: 2000 Unicode code points.
- Voice and format are allowlisted server-side.
- Response is audio bytes with an appropriate media type.
- Endpoint is presentation-only and does not create messages.

### 4.3 Authentication

Both endpoints read immutable identity from `JwtAuthenticationToken` claims:

- `jiacn`
- `client_id`
- `sub`

Missing, blank or non-string claims return 401. No default/anonymous identity and no `EsContextHolder` fallback.

### 4.4 Errors

| HTTP | Code |
| ---: | --- |
| 400 | `VOICE_INVALID_REQUEST` |
| 401 | `VOICE_UNAUTHORIZED` |
| 409 | `VOICE_IN_PROGRESS` / `VOICE_IDEMPOTENCY_CONFLICT` / `VOICE_RESULT_UNKNOWN` |
| 413 | `VOICE_TOO_LARGE` |
| 415 | `VOICE_UNSUPPORTED_MEDIA` |
| 422 | `VOICE_INVALID_AUDIO` / `VOICE_NO_SPEECH` / `VOICE_TOO_LONG` |
| 429 | `VOICE_RATE_LIMITED` |
| 502 | `VOICE_PROVIDER_ERROR` |
| 503 | `VOICE_DISABLED` / `VOICE_UNAVAILABLE` |
| 504 | `VOICE_PROVIDER_TIMEOUT` |

A dedicated exception handler returns real HTTP status and never exposes provider bodies, credentials, audio or transcript in logs.

## 5. Backend design

- Separate `SpeechTranscriptionController`/`SpeechSynthesisController`; do not add responsibilities to `ChatController`.
- Provider-neutral `SpeechTranscriptionProvider` and `SpeechSynthesisProvider`.
- Default disabled providers and `enabled=false` configuration.
- Dedicated HTTP client with connect timeout <= 3s and total deadline <= 25s; no transparent retry or cross-provider fallback.
- Streaming/spooled multipart handling; no repeated full-file byte-array copies.
- Byte size, exact allowlisted declared MIME/codec and container signature validation. V1 upload allowlist contains only `audio/webm;codecs=opus`; unsupported input fails closed before provider dispatch.
- Per-identity concurrency 1, per-minute 6, per-hour 60, bounded global provider concurrency. Redis unavailability fails closed for voice only.
- Idempotency key scope binds HMAC(identity), requestId, language/voice parameters and content hash. State: `IN_PROGRESS`, `SUCCEEDED`, `FAILED_KNOWN`, `FAILED_UNKNOWN`.
- A successful result may be encrypted in Redis for <= 10 minutes solely for idempotent replay. No DB/object-storage/business-log persistence.
- Provider timeout after request dispatch becomes `FAILED_UNKNOWN` and is not automatically retried.

## 6. Compatibility and configuration

Frontend feature flag and backend flag default to off. Browser support is detected at runtime. V1 selects `audio/webm;codecs=opus` only: the client must use that exact MediaRecorder MIME/codec profile, and the server allowlist must reject MP4/AAC, Ogg, WAV, MP3 and other fallbacks with `VOICE_UNSUPPORTED_MEDIA` before provider dispatch. If a browser does not support `audio/webm;codecs=opus` (including Safari deployments that expose only MP4/AAC), voice recording remains unavailable and the existing text chat stays usable.

Safari/MP4/AAC support is a later milestone, not a V1 fallback. It may be enabled only after a real browser-produced MP4/AAC fixture and separate security and compatibility validation are recorded. No V1 client capability probe or server configuration may enable it implicitly.

Spring multipart request limit must exceed 5 MiB for envelope overhead, while service byte validation remains 5 MiB. Production enablement requires an exact Nginx location for `/chat/speech/transcriptions` with approximately 6 MiB body limit and a shorter timeout, without changing `/chat/stream` behavior.

## 7. Observability and privacy

Allowed telemetry: stable error code, latency, byte/duration buckets, provider alias, MIME, rate-limit/idempotency outcome. Forbidden: audio, transcript/text, filename, raw identity, authorization, provider raw body and request payload logging.

## 8. Decisions

1. V1 uses server batch STT, not Web Speech or Realtime STT.
2. V1 uses countdown auto-send, not default immediate send.
3. V1 speaks only after a complete text response; streaming TTS/VAD/WebRTC are later milestones.
4. Text remains the authoritative conversation record.
5. Voice endpoints do not bind to or mutate conversations.
6. No DB migration.
7. Production deployment and provider activation require a separate release task.
8. V1 browser uploads are limited to `audio/webm;codecs=opus`; Safari/MP4/AAC is a later milestone gated by real-browser fixture, security and compatibility validation.

## 9. Frozen clarifications from architecture gate

### 9.1 Voice turn to reply correlation

V1 permits only one active auto-sent voice turn per Juyi Hall page. A second recording may stop playback but cannot auto-send until the first turn is terminal.

The frontend records for the active turn:

- `turnId` generated locally;
- send timestamp;
- baseline set of message local IDs;
- conversation ID before send and the conversation ID returned by `/chat/stream`;
- set of reply message IDs already synthesized.

`useHallConversation` exposes an explicit finalized-reply callback with `{conversationId, message, source}`:

1. For a synchronous built-in assistant response, the first non-empty assistant message added/changed after the baseline is finalized on `/chat/stream` end.
2. If the stream only reports Agent delivery and remains awaiting an external Agent, stream end is not final. The first `agent_message` final event associated with the same active conversation and newer than the voice send is finalized.
3. Delta events are never synthesized. A final message ID is synthesized at most once.
4. V1 speaks the first complete finalized reply for the active turn and then closes voice-reply correlation. Later independent Agent messages remain text-only.
5. Conversation mismatch, route/unmount, new conversation, manual text send or a 120-second reply timeout closes the correlation without TTS.

This frontend serialization is required because the existing Agent event contract does not carry a client `turnId`; adding cross-service turn propagation is deferred.

### 9.2 Trusted server duration validation

V1 accepts only browser-recorded WebM containing Opus audio and declared exactly as `audio/webm;codecs=opus` for transcription. The upload entry point rejects MP4/AAC (including `audio/mp4`), `audio/ogg` and arbitrary WAV/MP3 with `VOICE_UNSUPPORTED_MEDIA` before provider dispatch. A browser that supports only MP4/AAC therefore fails closed while text chat remains available.

Before provider dispatch, an `AudioDurationInspector` parses the allowlisted WebM container metadata with bounded reads:

- WebM/Opus: EBML `Info` duration and timecode scale.

The backend may retain hardened MP4/M4A duration-parser code and isolated parser tests for a future milestone, but that parser is not an upload allowlist entry in V1 and must not make MP4/AAC uploads succeed by itself. Safari/MP4/AAC enablement requires a real browser-produced fixture plus separate security and compatibility validation.

Unknown duration, malformed metadata, integer overflow, non-finite values or duration greater than 45,000 ms fail closed with `VOICE_INVALID_AUDIO` or `VOICE_TOO_LONG`. The parser has a fixed metadata read/box/depth budget and never decodes or transcodes the full media. `durationMs` from the client is diagnostic only.

### 9.3 Atomic Redis state

STT and TTS use separate namespaces. Identity scope is HMAC over length-prefixed UTF-8 claim bytes. Content digest binds contract version, operation, parameters and audio/text bytes.

Atomic begin operation:

- absent + quota available + concurrency available -> create `IN_PROGRESS`, reserve one concurrency lease;
- same request ID and same digest `IN_PROGRESS` -> 409 `VOICE_IN_PROGRESS`;
- same request ID and different digest in any state -> 409 `VOICE_IDEMPOTENCY_CONFLICT`;
- same digest `SUCCEEDED` -> replay encrypted cached result/audio if present, without provider call;
- `FAILED_UNKNOWN` -> 409 `VOICE_RESULT_UNKNOWN`;
- `FAILED_KNOWN` -> a new request ID is required.

Terminal transitions are compare-and-set from `IN_PROGRESS` only:

- success -> `SUCCEEDED`, encrypted result TTL 10 minutes;
- provider/request failure proven before ambiguous dispatch -> `FAILED_KNOWN`, TTL 2 minutes;
- timeout/disconnect after possible dispatch -> `FAILED_UNKNOWN`, TTL 10 minutes.

The concurrency lease TTL is provider deadline + 30 seconds and is explicitly released in `finally` only by the matching lease token. Rate counters are not rolled back. Redis failure before reservation returns 503; failure after dispatch becomes unknown. No transition causes an automatic provider retry.

### 9.4 Uniform response contract

All non-audio errors return:

```json
{
  "code": "VOICE_TOO_LONG",
  "msg": "录音超过允许时长",
  "status": 422,
  "data": {
    "requestId": "01..."
  }
}
```

`requestId` is echoed only after it passed safe syntax validation; otherwise it is null. HTTP status equals the `status` field.

Successful TTS returns a non-empty bounded body with:

- `Content-Type` matching the selected server format (`audio/mpeg` in V1);
- `Cache-Control: no-store`;
- `X-Voice-Request-Id`;
- a valid positive `Content-Length` when the body is materialized.

An empty provider body is `VOICE_PROVIDER_ERROR`, never HTTP 200.

### 9.5 Byte-exact JWT identity

Only an authenticated `JwtAuthenticationToken` is accepted. API-key authentication, CTX cookie and `EsContextHolder` are not fallback identities. Claims `jiacn`, `client_id` and `sub` must each be a non-empty String within configured UTF-8 byte limits. Accepted claim values are not trimmed, case-folded or Unicode-normalized.

For HMAC input each component is encoded as unsigned 32-bit big-endian byte length followed by exact UTF-8 bytes, in fixed `jiacn`, `client_id`, `sub` order.

### 9.6 Canonical CAS

`draftRevision` increments for every user or programmatic draft mutation, including clear, mention insertion, library citation and voice apply. Canonical context comparison uses:

- null distinct from empty string;
- IDs compared as exact JavaScript strings without trim/case/Unicode normalization;
- arrays de-duplicated then sorted by UTF-16 code-unit order;
- metadata limited to JSON-compatible values and canonicalized by recursively sorting object keys while preserving array order.

Any incomplete or unequal comparison produces detached manual review. Detached review cannot replace, append to or send the current draft until the user explicitly chooses to adopt it under the current context.

### 9.7 Authoritative scene mode

`HallStage` emits `scene-mode-change` with the computed effective `sceneMode` immediately after initialization and on every effective mode change. `JuyiHall` stores that value and uses it as the only authority for landscape HUD visibility; physical orientation alone is not authoritative.

### 9.8 Long TTS reply behavior

V1 does not silently truncate or partially describe a reply as complete. If the finalized reply exceeds 2,000 Unicode code points, automatic TTS is skipped, the complete text remains visible, and the UI reports `回话较长，已保留文字，未自动朗读`. Sentence-level segmented TTS is a later milestone.

## 10. Final contract closure

### 10.1 Local reply event sequence

Auto-send is ineligible while `isStreaming` or `isAwaitingReply` is already true. `useHallConversation` owns a monotonic local `replyEventSequence`, incremented whenever a final assistant/Agent reply candidate is observed. A voice turn captures the sequence immediately before send and accepts only a final callback whose local sequence is greater than the captured value, whose conversation ID matches the send result, and whose message ID was not in the baseline/spoken sets. Server timestamps are not used for correlation.

### 10.2 JWT claim limits and blank handling

- `jiacn`: maximum 256 UTF-8 bytes;
- `client_id`: maximum 256 UTF-8 bytes;
- `sub`: maximum 512 UTF-8 bytes.

A zero-length or Unicode-whitespace-only String is rejected with 401. A non-blank accepted value that contains leading or trailing whitespace is preserved byte-for-byte; validation must not replace the value with a trimmed representation.

### 10.3 Exact idempotent replay scope

A `SUCCEEDED` replay is allowed only for the exact tuple:

```text
(identity scope, operation, requestId, content digest)
```

A different requestId always creates a distinct operation subject to rate/concurrency controls and cannot discover or replay an older result by digest alone.

### 10.4 Concrete media fixtures and output bounds

Tests include a positive fixture produced by a browser MediaRecorder using the V1 profile:

- valid WebM/Opus declared as `audio/webm;codecs=opus`, with known duration below 45 seconds, accepted by the upload allowlist and duration validation.

Upload-contract fixtures also prove that MP4/AAC (including `audio/mp4`), Ogg, WAV, MP3 and other fallback types are rejected with `VOICE_UNSUPPORTED_MEDIA` before provider dispatch. Malformed, missing-duration and over-45-second WebM/Opus variants fail closed. Positive MP4/AAC fixtures, if retained for hardened parser unit coverage, are parser-only evidence and do not authorize the V1 upload path; they become an enablement prerequisite only for the later Safari/MP4/AAC milestone.

TTS limits are fixed as follows:

- provider response body maximum: 8 MiB;
- encrypted Redis cached TTS result maximum before encryption: 8 MiB;
- HTTP TTS success body maximum: 8 MiB;
- frontend synthesis download/playback maximum: 8 MiB.

Any declared or accumulated response larger than 8 MiB is aborted and mapped to `VOICE_PROVIDER_ERROR`; it is never cached or played. STT transcript JSON/provider response maximum is 256 KiB.
