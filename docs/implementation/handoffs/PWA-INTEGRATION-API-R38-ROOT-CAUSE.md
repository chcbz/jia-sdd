# PWA-INTEGRATION-API-RC R38 blocked root-cause handoff — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r38-20260901` / `critical_worker` / `writer`
Authorization notification: `d0e83b257893f3139e545ecfb52b111d312182461ec3c2e27a1296c5b31df1b9`
Terminal gate: **`blocked_root_cause`; owner released; no R38 static candidate or Review request**

## Exact product and predecessor preservation

- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained read-only, clean, and exact at commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- R36 package root remained `e94730ebfc64b8e99ec140545a914ef60a776130e985afd489fcace2ee7df779`.
- R36 builder root remained `271722718143b92dfdb090e6e59dd1d6e0a3afa806233678c1389be33677143a`.
- R37 builder root remained `02902c81eecf5cdf600205a64486ca717b93a92fd9596c0d8f9ede8fe71e9604`.
- Both R38 attempts were fresh and non-overwriting. No package staging copy occurred.
- All eight intended R38 final paths remained absent: package, wrapper, sealer, unit, activation, runtime evidence, workspace, and incident roots.

## Frozen design and exact init source of truth

Each fresh builder wrote exact `pwa-api-r19-r38.init.gradle` bytes before generating constructor or contract source, then measured the bytes dynamically. Both attempts measured the same SHA-256:

`d12e76aa261d0c916cfb056951bf65a91d2cd846a685d4a8f8411897b8adec4e`

The generated Python 3.6-compatible sources use deterministic JSON and ordered step definitions. They contain no `pprint`, `sort_dicts`, or literal occurrence of the measured R38 init SHA. The frozen acceptance mapping retained:

1. one measured init SHA propagated into wrapper fixtures/bindings, coverage, argv, 17 NUL-separated keys, XML paths, toolchain catalog, and static evidence;
2. actual wrapper call and receipt-key projection against coverage;
3. all 14 non-null XML paths at `externalBuildRoot/<project-key>/test-results/<test-task>`, with orders `8`, `9`, and `17` null and no extra `build` component;
4. R36 wrapper-reference, delegated-traversal, transaction, pycache-zero, real-toolchain, Python 3.6, and forbidden-observation controls;
5. fresh `df -B1 / >= 5368709120` admission before staging/publication, static evidence seal, and builder seal.

## Consecutive R38 failure matrix

| Attempt | Category | Exact root cause | Safety result | Required successor |
| --- | --- | --- | --- | --- |
| 1 | `wrapper_receipt_template_validation_anchor_mismatch` | The validator required the literal `local selector=...`, but the preserved wrapper declares `selector` in an earlier `local` list and assigns it after constructing `classes`. The anchor was syntactically over-specific; selector/receipt behavior was not shown incorrect. | Failed before staging, publication, or any final R38 path. | The sole retry accepted the exact assignment substring while retaining all six selector/receipt anchors. |
| 2 | `wrapper_actual_projection_optional_field_mismatch` | The retry parsed the actual wrapper and passed the selector/receipt anchors, then byte-compared complete dictionaries. Its wrapper-derived rows omitted coverage-only `external_artifact_path` at order `8` and `gradle_user_home_reuse` at order `9`; selectors, dynamically derived fixtures, canonical keys, tasks/tests, and XML values were equal. The comparator conflated receipt semantics with execution-only metadata. | Failed before staging, publication, static evidence, or builder seal. | Stop R38. A separately authorized R39 must compare an explicit receipt projection and validate execution-only fields separately. |

The second failure exhausted R38's bounded retry. Orchestrator notification: `180f2c2b80042443865a804ee9a28ff933750fc14beef5cc314478cd5b799597`.

## Preserved failed builders

| Attempt | Builder | Files | Bytes | Current content-projection SHA-256 |
| --- | --- | ---: | ---: | --- |
| 1 | `/var/tmp/cyf-pwa-api-r19-static-verifier-r38-builder-lnp8c2_h` | 23 | 374975 | `cf88ca14713df0357f8603834696a885bf92e9aaff8d6ce06eeda6ac80328eaa` |
| 2 | `/var/tmp/cyf-pwa-api-r19-static-verifier-r38-builder-hegn3hfk` | 25 | 377180 | `4d7f71b5ae6075255399f9ef2b002664744a3393e7ae1719127eb9f3469d8733` |

These are preserved failed preparation roots, not accepted or sealed builders. Low-disk policy intentionally prevented a final builder seal.

Failure evidence:

- Attempt 1 attribution: `/var/tmp/cyf-pwa-api-r19-static-verifier-r38-builder-lnp8c2_h/control/first-failure-attribution.txt`, SHA-256 `1084108142a178945919cea415e9d397cbb101e7b5a18d4a156b1b8eaa7288bd`.
- Attempt 2 attribution: `/var/tmp/cyf-pwa-api-r19-static-verifier-r38-builder-hegn3hfk/control/second-failure-attribution.txt`, SHA-256 `2eddc2f8d9577a14953b6ad4f5bb029cefb95a19524bfa0343127dbf065914e8`.
- R38 matrix: `/var/tmp/cyf-pwa-api-r19-static-verifier-r38-builder-hegn3hfk/control/root-cause-matrix.tsv`, SHA-256 `d408dc7f3343ec804c3659c55f023ad31d59f002ecf5fcaf62eae5f7a75d6e59`.
- Terminal record: `/var/tmp/cyf-pwa-api-r19-static-verifier-r38-builder-hegn3hfk/control/r38-terminal.json`, SHA-256 `1e47359336bee8322c3e0082429895587683d1db33f21a02166927a6c9b35c5b`.

## Disk and prohibited-operation result

The final observation was `4,089,823,232` available bytes, below the required `5,368,709,120`. Staging admission, final publication, static evidence seal, and builder seal remained fail closed.

No Gradle, runtime/unit start/stop/restart, daemon reload, network, DB, RabbitMQ, Chromium, production access, deployment, hardlink, package staging copy, canonical evidence publication, predecessor mutation, or unknown cleanup occurred.

## Required next action

Do not retry, overwrite, or promote R38. Only a separately authorized fresh R39 may continue. It must:

1. write exact init bytes first and derive the SHA only from those bytes;
2. compare wrapper actual receipts to coverage using an explicit field allowlist: `execution_order`, `phase`, `id`, `selector`, `fixture_digest`, `evidence_key`, `task`, `tests`, `xml_dir`, and `external_xml_dir`;
3. separately require order `8`'s exact `external_artifact_path` and order `9`'s exact `gradle_user_home_reuse`;
4. parse and bind the wrapper's literal `HYDRATION_FIXTURE`, `BRIDGE_FIXTURE`, and `INIT_SHA_EXPECT` to the measured init SHA rather than inferring them only from Python projections;
5. retain argv equality, all 17 NUL keys, all XML semantic paths, Python 3.6, R36/R37 preservation, and every accepted safety gate;
6. refuse staging, publication, static evidence seal, and builder seal until a fresh `/usr/bin/df -B1 /` observation is at least `5368709120` bytes.

Runtime remains unauthorized.
