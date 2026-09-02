# 聚义厅语音对话 tasks

## API (`api/`) — owner: `critical_worker`

- [x] `JVC-A01` Add immutable voice request/result/error domain types and provider SPIs.
- [x] `JVC-A02` Add strict JWT identity resolver with no `EsContextHolder` fallback.
- [x] `JVC-A03` Add transcription multipart controller with an exact V1 `audio/webm;codecs=opus` allowlist, reject MP4/AAC and all fallbacks before provider dispatch, plus duration validation, timeout, cleanup and stable errors.
- [x] `JVC-A04` Add synthesis controller, bounded request validation and audio response.
- [x] `JVC-A05` Add Redis-backed rate/concurrency/idempotency control with fail-closed behavior.
- [x] `JVC-A06` Add disabled/default and OpenAI-compatible provider adapters behind default-off properties.
- [x] `JVC-A07` Add focused controller/service/provider/security tests using stubs only, including positive browser WebM/Opus and fail-closed MP4/AAC/fallback fixtures.
- [x] `JVC-A08` Record exact API commit/tree SHA and verification evidence.

Owned source paths are limited to `api/chat/**`, API starter voice configuration/tests and the minimum required build files. Do not modify unrelated Agent, task, conversation or memory behavior.

## Web (`web/`) — owner: `balanced_worker`

- [x] `JVC-W01` Add JuyiHall-owned voice conversation composable with state machine and lifecycle cleanup.
- [x] `JVC-W02` Add Composer microphone controls and review/countdown surfaces outside submit behavior.
- [x] `JVC-W03` Add landscape HUD, scene-mode signal and map interaction lock integration.
- [x] `JVC-W04` Add explicit-context voice send path while preserving existing text send behavior.
- [x] `JVC-W05` Add optional complete-response TTS playback, cancellation and text fallback.
- [x] `JVC-W06` Add browser mocks and tests for generation races, conflicts, auto-send and playback.
- [x] `JVC-W07` Run focused tests and production build; record exact Web commit/tree SHA.

Owned source paths are limited to `web/src/components/world/JuyiHall.vue`, `web/src/components/juyiting/**`, `web/src/composables/juyiting/**`, minimal HTTP/API integration and relevant `web/tests/**`. Do not modify unrelated visual evidence fixtures or package tooling.

## Integration and verification — owner: main orchestrator

- [x] `JVC-I01` Independent API security/concurrency review.
- [x] `JVC-I02` Independent frontend state/context/interaction review.
- [x] `JVC-I03` Verify no regression to `/chat/stream`, map/roster split and explicit target assignment.
- [x] `JVC-I04` Pin exact candidate SHAs with `./sddw pin juyiting-voice-conversation`.
- [x] `JVC-I05` Run `./sddw verify juyiting-voice-conversation` and update acceptance evidence.
- [ ] `JVC-I06` Commit/push implementation branches and root integration candidate after review acceptance.
- [x] `JVC-I07` Do not deploy production or enable provider flags without a separate production release task.
- [x] `JVC-I08` Keep Safari/MP4/AAC disabled in V1; enable it only as a later milestone after a real browser fixture and completed security/compatibility validation.
