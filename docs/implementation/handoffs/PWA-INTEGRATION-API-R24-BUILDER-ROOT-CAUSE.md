# PWA API R24 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`  
Terminal state: **`blocked_root_cause`; owner released; no R24 static package, activation record, systemd unit, or Review candidate**

## Authority, owner replacement, and immutable product

- Product worktree: `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19`.
- Product commit/tree stayed clean and byte-exact: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- Durable predecessor authority: `PWA-INTEGRATION-API-R23-BUILDER-ROOT-CAUSE.md`, committed at `a56b4094cd9092251018815cab82a7a74dd15917`, SHA-256 `2ef05c29e9a89868cf9ca7a5b35f86d04f26fc1bbaf08721f1649fbeabc842c9`.
- The stale R24 Sol owner was atomically replaced only after its external `503 auth_unavailable` closure. This was recorded as **coordination evidence**, not a product/test failure; R20–R24 attempt history was preserved and the fresh R24 failure counter reset before construction.
- R21's live probe was never rerun. No predecessor builder or final path was modified.

## R24 failures

| Attempt | Result | Root cause | Safety result |
| --- | --- | --- | --- |
| Fresh replacement builder | Failed before controller publication | The replacement patch asserted that a required-category tuple occurred twice, but the inherited controller has a third distinct occurrence in generated-source construction. | No controller, package, activation, unit, or final path was published. Builder `/var/tmp/cyf-pwa-api-r19-static-verifier-r24-builder-853c0fd7f9d1463094eba04f92883b5a` is sealed. |
| Sole ledger-bound retry | Failed closed after manifest fixtures and before inherited-probe copying/package construction | `locate_activation_tokens` hard-codes the old R13 identity when it validates the post-rewrite token set. The four intended R24 replacements therefore produce an empty old-identity set and fail the exact-set assertion. | The normalized relative/absolute-under-root manifest checks passed, including rejection fixtures, but no package/unit/activation/final path was created. Builder `/var/tmp/cyf-pwa-api-r19-static-verifier-r24-builder-f16978f018be45918da9bc92b9c8f2e8` is sealed. |

## Evidence

- Fresh failure manifest root: `a9a3780b2b125c67b0c14724d9da0b00b1a961a64044d0149cb0877f63179688`; failure record SHA-256 `a093a726fb063ea597c92fa6d962be37821e9bfd15af6e167e45aef0e00470df`.
- Retry manifest root: `a712fefcc4e0c20aa018a381f5f0228347140fe4d6e60213b813053a285fa0f1`; retry summary SHA-256 `a0e92fe5d27911810b8404620fa68f3952532cd7a95bed610478823282838254`; Python traceback SHA-256 `634104bc9c2c518de09cb0ec26ea4d96c67365d0190454af2fd5d1385b7d8d98`.
- The retry's manifest verifier accepted both normalized relative-under-root and absolute-under-root entries, ran `sha256sum -c` from the manifest root, and preserved R13's 50 absolute-under-root rows as required.
- Every R24 final path remains absent, including `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r24.service`.

## Prohibitions observed

No Gradle, runtime start/stop/restart, daemon reload, network, DB, RabbitMQ, Chromium, production access, deployment, or product-source write occurred.

## Successor boundary

R24 is not reviewable. A separately authorized fresh non-overwriting R25 successor must:

1. retain all R20–R24 attempts and both sealed R24 builders;
2. keep Python 3.6 tokenize assignment-state extraction (no AST source positions);
3. preserve normalized relative/absolute-under-root manifest acceptance and traversal/lexical/realpath rejection;
4. pass the expected identity into the post-rewrite locator (or derive it from the semantic literals), while retaining exact four-token semantic/cardinality and unchanged-outside-span assertions;
5. never rerun the R21 probe or mutate prior/final paths; and
6. stop after its second consecutive attributed implementation failure.
