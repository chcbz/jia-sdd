# JVC-API R2 review root-cause matrix — 2026-09-02

## Scope and terminal state

- Task: `JVC-API`
- R2 rejected candidate: commit `7232308619d12c39f79653a315587ae7f645b346`, tree `af2b4472af12f0bf43403672a6ed365f6574515b`
- R2 focused evidence: selector `JVC-API-R2-service-focused`, key `146794838cb0a535366a743ec910f6b1eca711530935d6291a0ad657ea0b0c22`, fixture `59eaa48f7ee77f04e2b3e75e3fecb57884d71e3f258b39a07f0e3968eadfb418`, 34 passed
- Independent R2 review: `REJECT`, P0/P1/P2 = `0/2/0`
- Required gate: `blocked_root_cause` before any successor is authorized
- No production deployment or voice Provider activation is authorized.

## Consecutive-failure matrix

| Round | Evidence | Root cause | Required bounded remediation |
| --- | --- | --- | --- |
| R1 independent review | Pre-R2 candidate through `9762bca2`; review identified AAC timing trust, Boot 4/Jackson 3 package mismatch, missing real browser AAC evidence, and the global 50 MiB multipart exposure | The initial implementation relied on declared container timing, assumed Jackson 2 packages, treated unavailable browser MP4/AAC evidence too optimistically, and bounded audio only after broad multipart admission | R2 added encoded AAC timing lower bounds, migrated to `tools.jackson`, froze V1 to WebM/Opus, and added a voice-path request budget filter plus focused tests. |
| R2 independent review | Exact `7232308619d12c39f79653a315587ae7f645b346` / tree `af2b4472af12f0bf43403672a6ed365f6574515b`; review P1 findings in `VoiceAudioUploadFactory.java:73-95` and `VoiceTranscriptionRequestBudgetFilter.java:44-109` | (1) Parsed MIME validation checked only `audio/webm` base type and optional parameters, so bare `audio/webm` remained accepted instead of requiring the sole `codecs=opus` parameter. (2) The filter wrapped `getInputStream()` only for unknown length, while Servlet multipart parsing reaches `getParts()` on the underlying request, so chunked/unknown-length requests could still be parsed under the global 50 MiB limit before service validation. | Require exactly one parsed MIME parameter, `codecs=opus`, with no bare or extra parameter forms. Reject missing/unknown `Content-Length` at the voice filter before the chain and before `getParts()` can run; retain the known-length ~6 MiB rejection. Add unit and real HTTP chunked/unknown-length regressions proving the filter terminates before multipart parsing/provider dispatch. |

## R3 frozen implementation boundary

A single fresh `critical_worker` may modify only the existing JVC voice implementation/tests and the minimum exact configuration needed for these two findings:

1. `VoiceAudioUploadFactory` must accept only the semantic profile `audio/webm;codecs=opus`: one `codecs` parameter whose value is `opus`, no missing parameter, no extra parameter, and no alternate media type.
2. Existing successful controller/parser fixtures must declare the exact allowed profile. Add rejects for bare WebM, wrong codec, duplicate/extra parameters, MP4/AAC, and fallback types.
3. `VoiceTranscriptionRequestBudgetFilter` must reject unknown/negative content length before `chain.doFilter`; it must not claim that wrapping `getInputStream()` protects Servlet `getParts()` parsing.
4. Add an embedded HTTP regression that sends multipart without `Content-Length` (chunked/unknown-length) and proves stable fail-closed JSON before controller/provider use. Preserve known-length under-budget success and over-budget rejection.
5. Do not broaden global multipart behavior, change unrelated upload endpoints, introduce a DB migration, deploy, or enable any Provider flag.

## R3 promotion gates

- Writer commits a clean exact candidate without running unowned or parallel heavy work.
- Fresh `gpt_test_runner` runs the complete `cn.jia.chat.voice.*` focused suite through `cyf_orchestrator.py` with zero failures/skips and records exact-tree evidence.
- Fresh `sol_reviewer` independently reviews the exact R3 commit/tree and must return P0/P1/P2 = `0/0/0`.
- Only then may `JVC-API` return to `accepted` and integration pinning begin.
