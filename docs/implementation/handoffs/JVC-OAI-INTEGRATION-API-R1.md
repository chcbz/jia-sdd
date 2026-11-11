# JVC-OAI API release merge — R1 source review

2026-09-05. Source integration only; runtime verification remains a separate gate in `TASKS.yaml#runtime_ledger_json`.

- Worktree: `.worktrees/juyiting-voice-release-api`; branch `codex/juyiting-voice-release-api`.
- Merge commit `34b67fed96061bf9c3132106ca219fc6f5f6ba05`; tree `fb42c46c1f63299a37b44d7e55c6a303ddf016f1`.
- Exact parents: accepted voice `92c5ec3ffb89fa58e5d44c94a2d63c794b19016c` and login fix `dc039b34d9d24a46714724d5937f2c098f6c6d87`.
- Independent source reviewer `01a0707b-36e0-7ab1-b900-d2a7bdbb4c53`: SOURCE ACCEPT P0/P1/P2=0/0/0.
- Four-path voice-to-merge delta matches the original auth patch-id `411c2b6aed49ddb0436fd79af06ce031ee28e017`; both parents remain ancestors, clean worktree, no manual conflict resolution, mode changes or extra paths.

## Changed paths relative to accepted voice

- `common/jia-common-service/src/test/java/cn/jia/core/config/CorsConfigTest.java`
- `starter/src/main/resources/application-grey.properties`
- `starter/src/main/resources/application-prod.properties`
- `starter/src/test/java/cn/jia/security/AccountSecurityProfileContractTest.java`

The only new production-profile value is the exact API-origin CORS allowance from the existing auth fix. Voice/Spring AI configuration, default-off values and multipart budgets remain preserved. Primary API develop/index/worktree and Web were not changed.

## Approved narrow verification

One orchestrated invocation, task `JVC-OAI-INTEGRATION-API`, selector `JVC-OAI-INTEGRATION-API-profile-contracts`, fixture `N/A`:

- `:common:jia-common-service:test --tests cn.jia.core.config.CorsConfigTest`
- `:starter:test --tests cn.jia.security.AccountSecurityProfileContractTest`
- `:chat:jia-chat-service:test --tests cn.jia.chat.voice.config.VoiceGlobalMultipartBudgetTest --tests cn.jia.chat.voice.config.VoiceDefaultOffApplicationContextTest`

Broad accepted voice81/chat9 evidence is reused as unchanged-source evidence, not relabelled as a new-tree full run. All four actual XML suites must be recorded before claiming the narrow runtime gate passed. No push/deployment/provider activation is implied by this source review.

## Runtime verification and source promotion completed

2026-09-05: verifier `01a0707f-d6f0-78f0-9471-bcaf2e59e00d` completed the original single Gradle invocation (no rerun). Four suites ran: CORS2, security profiles2, multipart budget1, voice default-off8; total **13 tests, 0 failures/errors/skips**.

- Cache key `4e0b5ebc1c7e90d7415c3e435626ce97cf7abd97c838a3cf3213d005108efb5e`.
- Evidence `/tmp/cyf-evidence/jvc-oai-integration-api-profile-fb42c46c1f63299a37b44d7e55c6a303ddf016f1`.
- Four XML checksums independently verified; files0444/directories0555.
- `SHA256SUMS` SHA256 `8b0bb9ea45eda37c68766ce3420527778abbb054995347e3837d156a79dc7439`.
- Exact clean candidate atomically pushed without force to `origin/develop` and `origin/codex/juyiting-voice-release-api`; former remote develop `92c5ec3f` is preserved as first parent. Primary local develop remains unchanged.

This closes API source integration, not production release. OPS containment validation and adaptation to the currently accepted host lifecycle/path contract remain required before any deployment or voice activation.
