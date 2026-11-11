# JVC-OAI Spring AI R6 accepted source

2026-09-05. Source accepted and pushed, **not deployed**.

- Commit: `92c5ec3ffb89fa58e5d44c94a2d63c794b19016c`
- Tree: `fa067814f1236f85de687e0b6b7e3f1976875214`
- Independent reviewer: `01a07050-2b21-71c0-8df6-a9993df8c25c`, ACCEPT P0/P1/P2=0/0/0.
- Voice: 81 tests, 0 failure/error/skip; evidence key `0928aee5d4c5974a8c0cdf7a061930a360ae36f302e9d2b82b03d0e2ef0b6945`.
- Chat: 9 tests, 0 failure/error/skip; evidence key `17cb84fc8857657bfd878b8ee51da483a2cb340b96fe2fc32786b9cb62a302d7`.
- Evidence directories: `/tmp/cyf-evidence/jvc-oai-spring-{voice,chat}-fa067814f1236f85de687e0b6b7e3f1976875214`, verified SHA256SUMS, read-only 0555/0444.
- Voice manifest SHA256: `9ba98bee26d2940d56be25277aba654fc5c2acba74a858fd0c82416ea78e420d`.
- Chat manifest SHA256: `17b14c1572d02e6e2531bdfc628931588fcd4d28c86f95bdacbcc9ed168f4638`.

Four P1 closures accepted: disable unsafe native audio autoconfiguration; remove duplicate voice credential/URL properties; allow exact validated HTTPS gateway dispatch; strictly reject ambiguous TTS response MIME. Existing bounded/unlinked upload and identity/replay/cache contracts remain preserved.

Exact source was atomically pushed without force to `origin/develop` (fast-forward from `492adc7e`) and `origin/feat/juyiting-openai-voice-provider`. Local `api` develop commit `dc039b34` was not changed. It contains a newer login-origin fix outside the voice branch; release integration must retain it rather than replace/reset the workspace.

Production deployment/feature activation still require the OPS and release integration gates. `docs/DEPLOYMENT.md` now documents `/opt/cyf/service/api` and canonical lifecycle entry `/usr/local/sbin/cyf-api-kit`; the older voice packet targets `/opt/cyf/api`. Do not apply that historical host layout blindly or use obsolete source-to-production start scripts.
