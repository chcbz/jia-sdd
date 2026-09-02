# 聚义厅语音对话 acceptance

## Functional acceptance

- [x] Supported browser can record, stop, cancel and transcribe a short clip.
- [x] Permission denial, unsupported recorder and provider-disabled states preserve text chat.
- [x] Manual policy never sends without a separate user send action.
- [x] Auto policy is opt-in, displays a cancelable countdown and sends exactly once.
- [x] Context/draft/conversation changes cancel auto-send and produce detached manual review.
- [x] public/private/bounty voice sends preserve exact scope, explicit target IDs, task IDs and metadata.
- [x] Transcript text never selects an Agent or changes scope.
- [x] Landscape HUD and Composer share one recorder; no duplicate recording or upload is possible.
- [x] Recording/transcribing locks map input and prevents pointer/keyboard penetration.
- [x] Complete Agent text reply can be synthesized and played when voice reply is enabled.
- [x] TTS error never removes or changes the text response.

## Lifecycle and limit acceptance

- [x] 45-second client hard stop and 5 MiB client hard stop are enforced.
- [x] Backend accepts only the exact `audio/webm;codecs=opus` upload profile; actual audio bytes above 5 MiB and all other media types, including MP4/AAC, are rejected before provider dispatch.
- [x] Cancel/unmount/pagehide/hidden/track-ended paths stop every MediaStream track.
- [x] Permission, recorder, upload and TTS late callbacks are generation-fenced.
- [x] Upload and TTS AbortControllers are released and stale results ignored.
- [x] Content above Composer limit is never silently truncated.

## Security and backend acceptance

- [x] Missing/invalid `jiacn`, `client_id` or `sub` JWT claims return 401 before provider use.
- [x] CTX/ThreadLocal state cannot supply or override voice identity.
- [x] Voice endpoints are disabled by default and do not become anonymous in standalone starter mode.
- [x] Rate, concurrency and idempotency states are atomic and scoped to exact identity/content parameters.
- [x] Provider timeout does not transparently retry and is classified as unknown when billing state is uncertain.
- [x] Redis outage fails voice closed without affecting text chat.
- [x] Audio, transcript/text, raw identity, filename, credentials and provider raw body are absent from logs.
- [x] No DB migration, message creation, conversation creation, Agent call, memory write or tool/MCP call occurs in voice endpoints.

## Regression acceptance

- [x] Existing `/chat/stream` text flow passes its focused tests.
- [x] Juyi Hall continues using `/agent/map` and `/agent/roster`; `/agent/active` is absent.
- [x] Task assignment continues passing an explicit target Agent.
- [ ] Existing orientation, keyboard resize, focus trap and map interaction tests pass.
- [x] Frontend production build passes.
- [x] API focused Gradle tests pass through `cyf_orchestrator.py`.

## Verification evidence

- API revision: commit `492adc7e8ff386013264c4eef4c0bf67adf34add`; tree `ef888807fb3b190b65d813286a0733795763b411`.
- API voice-selector evidence: `7d8d5f492737cda8fe028639a66b50eb0917c8e07827938e32f49c3348509591`; fixture digest `44547c9e422ad0ca70123edffbd5261030d502644048693f1d77aae7df1384b9`; 11 classes, `48/0/0/0`; build duration `24m33s`.
- API `/chat/stream` compatibility evidence: `ChatControllerTest` evidence `4932082fcf0b765ab704e5040c4eeadff78b480b6127c689f5b66773f8669491`; `9/0/0/0`; duration `6m18s`.
- Web revision: commit `97c2f8bd439dc6f7876a4d26c91d485ea7750cda`; tree `162fc64e5d8a81a77d85bf40bd50703af38e88f7`.
- Web voice-only evidence: 23 passing; production build pass in `4m59s`.
- Independent reviews: API security/concurrency review ACCEPT `0/0/0`; frontend feature review ACCEPT `0/0/0`; supplemental selected-component run `4 pass/2 fail/incomplete`, with fresh attribution review ACCEPT `0/0/0`.
- Supplemental failures are non-blocking baseline/harness debt (stale destroy/loading assertion and incomplete `visualViewport` evidence). The complete orientation/keyboard-resize/focus-trap/map-interaction regression criterion is intentionally **not** claimed as passed.
- Integration pin: `./sddw pin juyiting-voice-conversation` completed for the revisions above; `./sddw verify juyiting-voice-conversation` PASS.
- Result: integration-ready; final accepted status remains with the independent integration review.

## Architecture-gate closure

- [x] Built-in stream completion and external final `agent_message` are distinguished; delta/delivery events are never spoken.
- [x] Exactly one finalized reply message is synthesized at most once per active voice turn.
- [x] Allowlisted WebM/Opus duration validation rejects unknown/malformed/over-45-second media before provider dispatch; retained MP4/AAC parser hardening is not an upload allowlist entry.
- [x] Redis state transitions, lease token release, TTLs and replay/conflict/unknown behavior match design section 9.3.
- [x] Every JSON error has matching HTTP/status, sanitized requestId echo and no provider detail.
- [x] JWT identity tests prove byte-exact length-prefixed HMAC scoping and no API-key/CTX fallback.
- [x] Every programmatic and user draft mutation increments draftRevision and canonical CAS is fail closed.
- [x] HallStage publishes authoritative initial and changed sceneMode for HUD visibility.
- [x] Replies over 2,000 code points are not truncated or synthesized in V1.
- [x] Auto-send is disabled while an earlier Hall reply is streaming/awaiting, and final reply correlation uses local sequence rather than server timestamps.
- [x] JWT whitespace and exact UTF-8 byte-limit cases match design section 10.2 without normalizing accepted values.
- [x] Successful idempotent replay requires the exact identity/operation/requestId/digest tuple.
- [x] A real browser WebM/Opus MediaRecorder fixture with declared `audio/webm;codecs=opus` passes; MP4/AAC (including `audio/mp4`) and fallback MIME fixtures are rejected fail-closed, while malformed/unknown/overlong WebM/Opus variants fail before provider dispatch.
- [x] Safari/MP4/AAC remains disabled in V1 and is enabled only in a later milestone after a real browser fixture plus security and compatibility validation.
- [x] STT response 256 KiB and TTS 8 MiB provider/cache/client bounds are enforced.
