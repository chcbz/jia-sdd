# JVC-OAI Spring AI audio refactor contract

Date: 2026-09-04
Base API candidate: `b3d6ba885dcdc7f1a23e308ca64f3f35cefab206` / tree `100ce0d8ff713a760a258998aa8571aee89d5b96`
User decision: unify 聚义厅 audio provider integration on Spring AI's OpenAI audio architecture.

## Target architecture

1. Replace direct OpenAI-compatible HTTP client ownership in the voice providers with the Spring AI OpenAI audio transcription/speech models available in this repository's pinned Spring AI version.
2. Resolve credentials and shared transport through Spring AI OpenAI properties. The common `spring.ai.openai.api-key`/base URL may be inherited by audio, while audio-specific overrides remain supported according to the pinned version's API.
3. Retain `jia.chat.voice.*` only for product behavior and safety policy: feature flags, identity HMAC, cache encryption, quotas, deadlines, allowed models/voices/languages/formats and explicit provider-selection contract. Do not duplicate or log secret values.
4. Delete/retire direct provider HTTP configuration only after no runtime or test path depends on it. A compatibility gateway is allowed only as an explicitly configured Spring AI endpoint and only if the same security contract/tests prove its audio endpoint behavior; no implicit fallback or undocumented endpoint change.

## Non-negotiable safety invariants

- Voice defaults stay disabled; no credential, flag, deployment or host action.
- Admission remains before spool/parse/digest; all release paths remain exact.
- Uploaded audio remains handle-based after unlink: no path reopen, no stale-path deletion and no large full-file heap copy.
- Preserve lone-surrogate rejection, identity/cache AES-GCM binding, response/error privacy, body-size/time bounds, MIME preservation and replay/cache isolation.
- A Spring AI resource adapter must not reintroduce path TOCTOU or unbounded body buffering. If the pinned Spring AI model cannot consume a one-shot channel-backed resource while preserving these limits, stop and document the precise API limitation rather than weakening the invariant.
- Speech success responses must retain bounded bytes and explicit expected content type semantics.

## Required deliverables

- Runtime dependency correctness: audio model classes are available in the production service classpath, not only test/compile-only classpaths.
- Explicit Spring AI audio configuration and tests proving common-key inheritance plus audio-specific override precedence without asserting/printing secret values.
- Provider/service adapters based on Spring AI audio APIs; remove unused direct HTTP code only when behavior is covered.
- Contract tests for official OpenAI-style audio calls plus a controlled compatibility-gateway fake, including endpoint/base-url inheritance, request headers, model/voice/language/format, malformed/multiple content-type handling and all existing security regression paths.
- Fresh serialized verification, independent security review, then a separate production-security gate.

## Scope

Writer may modify only API files directly needed for this refactor (voice Java/config/tests and required API Gradle runtime dependency declarations). No docs/ledger/Web/OPS changes, no production action.
