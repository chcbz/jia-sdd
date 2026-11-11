# JVC-OAI Spring AI safe-audio facade decision

Date: 2026-09-04
Base candidate: `b3d6ba885dcdc7f1a23e308ca64f3f35cefab206` / `100ce0d8ff713a760a258998aa8571aee89d5b96`
Decision: native `OpenAiAudioTranscriptionModel` / blocking speech `call()` in pinned Spring AI 2.0.0 are not eligible for production audio because they fully buffer input/output and break the existing handle-only/bounded-body security contract.

## Approved direction

Unify configuration and application integration with Spring AI while retaining a product-owned safe transport adapter:

1. Bind/resolve `spring.ai.openai.*` common connection/audio properties and audio-specific override properties through Spring Boot/Spring AI-compatible configuration.
2. Supply voice-domain adapters/models as Spring beans behind the product voice interfaces. They may use Spring AI option/property types and model contracts where those contracts do not force full buffering.
3. Retain the current channel-backed, unlink-safe multipart publishing and bounded response consumer as the transport implementation until a pinned Spring AI release is proven by source and regression tests to offer streaming, bounded equivalents.
4. Remove duplicated `jia.chat.voice.*.api-key` ownership. `jia.chat.voice.*` remains only product policy: enablement, quotas, privacy/cache crypto, allowed model/voice/language/format and explicit compatibility-gateway allowlist.
5. A gateway is selectable only by explicit Spring configuration and is validated as a fixed HTTPS allowlist member; audio endpoint compatibility remains a test-gated capability, not a fallback.

## Verification contract

- Prove common Spring AI key/base URL inheritance and audio override precedence without logging secret values.
- Prove common-key credentials reach the safe adapter only through Spring configuration binding.
- Preserve exact admission-before-spool, unlinked FileChannel, no full audio heap copy, bounded TTS response, MIME/header/content-type, AES/identity/replay/cache behavior.
- Keep direct use of the pinned unsafe native audio model classes prohibited in production code; test may use fakes only.
- Fresh verifier and independent review are mandatory; production deployment is a separate gate.
