# 聚义厅语音对话 tasks

## API (`api/`) — owner: `critical_worker`

- [ ] `JVC-A01` Add immutable voice request/result/error domain types and provider SPIs.
- [ ] `JVC-A02` Add strict JWT identity resolver with no `EsContextHolder` fallback.
- [ ] `JVC-A03` Add transcription multipart controller with an exact V1 `audio/webm;codecs=opus` allowlist, reject MP4/AAC and all fallbacks before provider dispatch, plus duration validation, timeout, cleanup and stable errors.
- [ ] `JVC-A04` Add synthesis controller, bounded request validation and audio response.
- [ ] `JVC-A05` Add Redis-backed rate/concurrency/idempotency control with fail-closed behavior.
- [ ] `JVC-A06` Add disabled/default and OpenAI-compatible provider adapters behind default-off properties.
- [ ] `JVC-A07` Add focused controller/service/provider/security tests using stubs only, including positive browser WebM/Opus and fail-closed MP4/AAC/fallback fixtures.
- [ ] `JVC-A08` Record exact API commit/tree SHA and verification evidence.

Owned source paths are limited to `api/chat/**`, API starter voice configuration/tests and the minimum required build files. Do not modify unrelated Agent, task, conversation or memory behavior.

## Web (`web/`) — owner: `balanced_worker`

- [ ] `JVC-W01` Add JuyiHall-owned voice conversation composable with state machine and lifecycle cleanup.
- [ ] `JVC-W02` Add Composer microphone controls and review/countdown surfaces outside submit behavior.
- [ ] `JVC-W03` Add landscape HUD, scene-mode signal and map interaction lock integration.
- [ ] `JVC-W04` Add explicit-context voice send path while preserving existing text send behavior.
- [ ] `JVC-W05` Add optional complete-response TTS playback, cancellation and text fallback.
- [ ] `JVC-W06` Add browser mocks and tests for generation races, conflicts, auto-send and playback.
- [ ] `JVC-W07` Run focused tests and production build; record exact Web commit/tree SHA.

Owned source paths are limited to `web/src/components/world/JuyiHall.vue`, `web/src/components/juyiting/**`, `web/src/composables/juyiting/**`, minimal HTTP/API integration and relevant `web/tests/**`. Do not modify unrelated visual evidence fixtures or package tooling.

## Integration and verification — owner: main orchestrator

- [ ] `JVC-I01` Independent API security/concurrency review.
- [ ] `JVC-I02` Independent frontend state/context/interaction review.
- [ ] `JVC-I03` Verify no regression to `/chat/stream`, map/roster split and explicit target assignment.
- [ ] `JVC-I04` Pin exact candidate SHAs with `./sddw pin juyiting-voice-conversation`.
- [ ] `JVC-I05` Run `./sddw verify juyiting-voice-conversation` and update acceptance evidence.
- [ ] `JVC-I06` Commit/push implementation branches and root integration candidate after review acceptance.
- [ ] `JVC-I07` Do not deploy production or enable provider flags without a separate production release task.
- [ ] `JVC-I08` Keep Safari/MP4/AAC disabled in V1; enable it only as a later milestone after a real browser fixture and completed security/compatibility validation.
