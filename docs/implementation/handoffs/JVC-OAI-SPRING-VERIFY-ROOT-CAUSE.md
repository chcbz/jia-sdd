# JVC-OAI Spring AI facade verification root-cause matrix

Date: 2026-09-04
Exact candidate: `6bc95a30cddd610a0c25a4010ca800c828b37ba0` / tree `1493d191e9f82178b06fd44bbbcc9affdda0548d`
Status at creation: verification dispatch stopped before Gradle; no product selector, XML result, evidence cache record, credential, feature flag, host, or production operation occurred.

## Consecutive-stop matrix

| Attempt | Boundary | Root cause | Product implication | Bounded remediation |
| --- | --- | --- | --- | --- |
| Spring AI native-model review | Static source inspection before the safe-facade source change | The pinned Spring AI 2.0.0 OpenAI audio models buffer uploaded resources/responses in full, violating the established handle-only upload and bounded TTS response contract. | Native models are prohibited from the production voice path. | The candidate replaces the intended native-model usage with a Spring AI configuration/common-property facade over the existing channel-backed bounded transport. |
| Spring facade verification dispatch | Orchestrator task lookup before Gradle | The verifier incorrectly supplied selector labels `JVC-OAI-SPRING-voice` / `JVC-OAI-SPRING-chat` as task IDs. The ledger task ID is `JVC-OAI`; selector labels belong only in `--selector`. Orchestrator rejected `unknown task` before worktree validation or Gradle. | No product assertion was executed and no runtime evidence exists for the candidate. | Bind one fresh Terra verifier to task `JVC-OAI`; all orchestrator options precede the task ID; run voice exactly once, then ChatController exactly once only if voice passes. |

## Frozen verification contract

- Worktree: `/home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-api`, clean at the exact commit/tree above.
- Use only `JVC-OAI` as the orchestrator task ID. The selector names are `JVC-OAI-SPRING-voice` and `JVC-OAI-SPRING-chat`.
- Every Gradle child command uses the orchestrator, one worker, no daemon/watch-fs, bounded JVM and `-PrepoUsername=unused -PrepoPassword=unused`.
- The voice command runs once. Only a zero exit permits the ChatController command. Any non-zero result ends the attempt and must be attributed before another retry.
- Copy each produced XML directory to a new immutable `/tmp/cyf-evidence/jvc-oai-spring-{voice|chat}-1493d191e9f82178b06fd44bbbcc9affdda0548d/` directory and create `SHA256SUMS`; do not overwrite existing evidence.
- No source edit, native Spring AI audio-model use, credential read/install, feature-flag change, host action, deployment, reload, or restart is authorized.

## Required review after passing runtime evidence

A fresh independent reviewer must confirm common/audio property inheritance and override precedence, explicit HTTPS compatibility-gateway allowlisting, no production use of unsafe native audio models, and preservation of admission-before-spool, unlink-safe FileChannel-only upload, bounded TTS response, MIME/content-type ambiguity rejection, AES identity/cache binding, and replay isolation. Only `P0/P1/P2 = 0/0/0` may permit API merge consideration; deployment remains a separate gate.
