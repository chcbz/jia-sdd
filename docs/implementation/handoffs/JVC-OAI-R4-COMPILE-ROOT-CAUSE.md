# JVC-OAI R4 compile root-cause matrix

Date: 2026-09-04
Rejected candidate commit/tree: `e180458fa0783f9e20e754f2e4230a55dbd61f70` / `087cffcd55f8c48b4eb9e91babfea8fcb470d70d`
Status at creation: `blocked_root_cause`.

## Failure history

| Terminal event | Evidence | Attribution | Consequence |
| --- | --- | --- | --- |
| R4 dispatches before Terra | Two `gpt_test_runner` dispatches ended with Codex `503 auth_unavailable` before a child command started. | External verification-provider authentication; no source test result. | No merge/test evidence was produced. |
| R4 Terra voice selector | Evidence key `d4230bad05d8e262de9e4ff4c4f43b38cf632a76dde3cd92c9e14fca89da6d35`; immutable directory `/tmp/cyf-evidence/jvc-oai-r4-voice-087cffcd55f8c48b4eb9e91babfea8fcb470d70d`; test count `0`. | `compileTestJava` stopped at `OpenAiCompatibleVoiceProviderTest.java:242`: inferred `List<? extends Object>` is incompatible with the helper's `List<String>` parameter. | This is a focused source/test compile defect. ChatController was correctly not run and no product behavior was exercised. |

## R5 bounded remediation

1. On the unchanged R4 candidate, make the smallest type-safe correction to the affected test fixture/helper so its header values are explicitly `List<String>`.
2. Do not weaken the unique JSON `Content-Type` contract or remove duplicate/conflicting-header coverage; preserve all R4 security behavior.
3. Add/retain a compiler-visible regression shape that would fail if the inferred type becomes wildcard/Object again.
4. Modify only directly related API voice test/source files; no Web/OPS/docs/ledger changes, no key/flag/deploy/host action.
5. Commit a clean exact R5 candidate.

## Required next gates

- Fresh GPT-5.6 Terra verifier: run the frozen `JVC-OAI-R5-voice` selector once. Only after PASS, run `JVC-OAI-R5-chat` once. Seal separate immutable XML evidence and SHA256SUMS.
- Fresh independent read-only reviewer: inspect R5 security closure and the evidence. Only `P0/P1/P2=0/0/0` allows fast-forward to `api/origin/develop`.
- Production remains out of scope: no OpenAI key, no flag activation, no deployment/restart.
