# PWA API R25 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r25-20260901` / `critical_worker` / `writer`
Terminal state: **`blocked_root_cause`; owner released; no R25 controller, static package, unit, activation record, or Review candidate**

## Authority and immutable product

- Product worktree: `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19`.
- Product commit/tree stayed clean and exact: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- Durable R25 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R24-BUILDER-ROOT-CAUSE.md` at commit `efa119fda4fa5ef179683cd6579e804210836952`, file SHA-256 `295e428d0d9ebb91448933d9e594b71528f13d02916df8dc8b5beb2250741c5f`.
- The orchestrator atomically authorized R25, retained all R20–R24 attempt records, and reset only the fresh R25 consecutive-failure counter to zero.
- The R21 live probe was never rerun. R20–R24 and earlier sealed builders were not edited, deleted, relinked, chmod/chown modified, or reused.

## Frozen R25 contract

Before controller editing, each fresh builder froze the product API/event catalog, lock/publication order, transaction boundaries, sensitive-payload allowlist, forbidden operations, and acceptance-to-test coverage.

The intended structural fixes were frozen as:

1. derive required-category occurrences from parsed controller/template/generated structure, with named roles `controller_runtime_authorization`, `generator_template_authorization`, and `generated_builder_authorization`, rather than asserting a raw text count;
2. parameterize `locate_activation_tokens(source, semantic, expected_identity)`, using the R13 identity before rewrite and the R25 identity after rewrite;
3. retain exactly four activation token spans, unchanged-outside-span bytes, pre-old `4`, post-old `0`, post-new `4`, decoded-literal/AST/cardinality checks, and Python 3.6 compile;
4. verify each manifest with `sha256sum -c` from its own exact root while accepting normalized relative-under-root and absolute-under-root entries and rejecting traversal, lexical escape, and realpath escape; and
5. build only a fresh non-overwriting static package with no runtime start, Gradle, network, DB, RabbitMQ, Chromium, production, deployment, or daemon reload.

## R25 failure matrix

| Attempt | Result | Root cause | Safety result |
| --- | --- | --- | --- |
| Fresh R25 builder | Failed before controller publication | The constructor bound the correct immutable R24 controller path but used an incorrectly transcribed donor SHA-256 constant (`08605e…`) instead of the measured `83a7d5537338c65858d3948a5418d8556522a75b58731ee25f18008f641a7b7f`. Its fail-closed donor check stopped immediately. | No R25 controller, package, unit, activation, or final path was published. Product and predecessor bytes remained unchanged. |
| Sole ledger-bound retry | Failed before controller publication | The donor digest was corrected and the retry was bound to `r25_inherited_controller_digest_binding_mismatch`, count `1`. However, `insert_sealed_rows` still required raw `source.count("sealed_specs=(\\n")==1`. At that phase the inherited controller has two raw markers: the outer assignment and the marker inside the `verify_auth` generator-template string. | This was the second consecutive R25 failure. No generated builder, package, unit, activation, final path, runtime, or Review candidate exists. |

The second failure repeats the prohibited class of broad textual cardinality assumptions. R25 therefore stopped without using its otherwise drafted parameterized activation locator or three-role runtime inventory.

## Sealed evidence

### Fresh builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r25-builder-d74a4ce5fc5542d49799c7178c8732b4`.
- Manifest rows: `10`; `sha256sum -c` passed `10/10` from that exact root.
- Authoritative builder root SHA-256: `7896d195af380a22d07e400dcddfa76b5fd6c05e19fd5fc0e2613ea6997a25a5`.
- Failure record SHA-256: `45ac3df794609d032a36671d767e3877f51b595429ba2edfa6bb8ab2cbbf5b6a`.
- The first orchestrator attempt's free-form evidence text mistakenly states a different builder-root suffix. The immutable manifest and this terminal matrix record the authoritative root above; the sealed builder was not modified to correct prose.

### Sole retry builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r25-builder-f304a2b7760e449d9052af5433f64d1c`.
- Manifest rows: `11`; `sha256sum -c` passed `11/11` from that exact root.
- Builder root SHA-256: `55181356659279678b4244e49e270e686e5a5b850d572ef7267e052badc18c3a`.
- Failure record SHA-256: `dfced453f405606e7bb874ec8707a402853a9133604166bf6a8fea8c37b8e0ae`.
- Root-cause matrix SHA-256: `04795f06483cb4271b3b1b3036363ad80f1c3bff6b5570636b3a9c2eb4e611cd`.
- The retry independently reverified the first R25 builder root before sealing.

## Final absence and prohibited-operation result

All R25 final paths remain absent:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r25-preparation`
2. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r25`
3. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r25-seal`
4. `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r25.service`
5. `/var/tmp/cyf-pwa-api-r19-static-verifier-r25-evidence`
6. `/var/tmp/cyf-pwa-api-r19-static-verifier-r25-workspace`
7. `/var/tmp/cyf-pwa-api-r19-static-verifier-r25-incidents`
8. `/var/tmp/cyf-pwa-api-r19-static-verifier-r25.activation.json`

No product-source write, R21 probe rerun, predecessor mutation, Gradle, runtime start/stop/restart, network, DB, RabbitMQ, Chromium, production access, deployment, or daemon reload occurred.

## Successor boundary

R25 is not reviewable. Only a separately authorized fresh non-overwriting R26 may continue. It must:

1. preserve both sealed R25 builders and all R20–R24 attempts/builders;
2. bind authorization to this committed matrix and reset only the fresh R26 counter;
3. locate the outer `sealed_specs` assignment by AST/token structure while excluding the `verify_auth` string span, or patch and reinsert the decoded template before outer-structure edits;
4. freeze and assert the three actual required-category roles from controller, decoded template, and final generated builder without any raw marker-count assertion;
5. retain the parameterized old/new activation identity locator, exactly four token spans, unchanged-outside-span assertion, compile, semantic, and cardinality checks;
6. retain normalized relative/absolute-under-root manifests with `sha256sum` run from each correct root; and
7. stop again after a second consecutive R26 failure.
