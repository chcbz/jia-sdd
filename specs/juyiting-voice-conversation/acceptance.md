# 聚义厅语音对话 acceptance

## Functional acceptance

- [ ] Supported browser can record, stop, cancel and transcribe a short clip.
- [ ] Permission denial, unsupported recorder and provider-disabled states preserve text chat.
- [ ] Manual policy never sends without a separate user send action.
- [ ] Auto policy is opt-in, displays a cancelable countdown and sends exactly once.
- [ ] Context/draft/conversation changes cancel auto-send and produce detached manual review.
- [ ] public/private/bounty voice sends preserve exact scope, explicit target IDs, task IDs and metadata.
- [ ] Transcript text never selects an Agent or changes scope.
- [ ] Landscape HUD and Composer share one recorder; no duplicate recording or upload is possible.
- [ ] Recording/transcribing locks map input and prevents pointer/keyboard penetration.
- [ ] Complete Agent text reply can be synthesized and played when voice reply is enabled.
- [ ] TTS error never removes or changes the text response.

## Lifecycle and limit acceptance

- [ ] 45-second client hard stop and 5 MiB client hard stop are enforced.
- [ ] Backend rejects actual audio bytes above 5 MiB and unsupported media.
- [ ] Cancel/unmount/pagehide/hidden/track-ended paths stop every MediaStream track.
- [ ] Permission, recorder, upload and TTS late callbacks are generation-fenced.
- [ ] Upload and TTS AbortControllers are released and stale results ignored.
- [ ] Content above Composer limit is never silently truncated.

## Security and backend acceptance

- [ ] Missing/invalid `jiacn`, `client_id` or `sub` JWT claims return 401 before provider use.
- [ ] CTX/ThreadLocal state cannot supply or override voice identity.
- [ ] Voice endpoints are disabled by default and do not become anonymous in standalone starter mode.
- [ ] Rate, concurrency and idempotency states are atomic and scoped to exact identity/content parameters.
- [ ] Provider timeout does not transparently retry and is classified as unknown when billing state is uncertain.
- [ ] Redis outage fails voice closed without affecting text chat.
- [ ] Audio, transcript/text, raw identity, filename, credentials and provider raw body are absent from logs.
- [ ] No DB migration, message creation, conversation creation, Agent call, memory write or tool/MCP call occurs in voice endpoints.

## Regression acceptance

- [ ] Existing `/chat/stream` text flow passes its focused tests.
- [ ] Juyi Hall continues using `/agent/map` and `/agent/roster`; `/agent/active` is absent.
- [ ] Task assignment continues passing an explicit target Agent.
- [ ] Existing orientation, keyboard resize, focus trap and map interaction tests pass.
- [ ] Frontend production build passes.
- [ ] API focused Gradle tests pass through `cyf_orchestrator.py`.

## Verification evidence

- API revision: pending
- Web revision: pending
- Commands/tests: pending
- Independent reviews: pending
- Result: pending

## Architecture-gate closure

- [ ] Built-in stream completion and external final `agent_message` are distinguished; delta/delivery events are never spoken.
- [ ] Exactly one finalized reply message is synthesized at most once per active voice turn.
- [ ] WebM and MP4 duration parsers reject unknown/malformed/over-45-second media before provider dispatch.
- [ ] Redis state transitions, lease token release, TTLs and replay/conflict/unknown behavior match design section 9.3.
- [ ] Every JSON error has matching HTTP/status, sanitized requestId echo and no provider detail.
- [ ] JWT identity tests prove byte-exact length-prefixed HMAC scoping and no API-key/CTX fallback.
- [ ] Every programmatic and user draft mutation increments draftRevision and canonical CAS is fail closed.
- [ ] HallStage publishes authoritative initial and changed sceneMode for HUD visibility.
- [ ] Replies over 2,000 code points are not truncated or synthesized in V1.
- [ ] Auto-send is disabled while an earlier Hall reply is streaming/awaiting, and final reply correlation uses local sequence rather than server timestamps.
- [ ] JWT whitespace and exact UTF-8 byte-limit cases match design section 10.2 without normalizing accepted values.
- [ ] Successful idempotent replay requires the exact identity/operation/requestId/digest tuple.
- [ ] Positive WebM/Opus and MP4/AAC MediaRecorder fixtures pass, malformed/unknown/overlong variants fail closed.
- [ ] STT response 256 KiB and TTS 8 MiB provider/cache/client bounds are enforced.
