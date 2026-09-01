# PWA-INTEGRATION-API-RC R37 blocked root-cause handoff — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r37-20260901` / `critical_worker` / `writer`
Terminal gate: **`blocked_root_cause`; owner released; no R37 package, wrapper, sealer, unit, activation, runtime evidence root, workspace, or incident root was published**

## Authority and frozen scope

- Authorized claim notification: `15cfe28974c8427662155246e32392bd8d67e88376177bc664cf030ba98c21dd`.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained read-only, clean, and exact at commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- The writer read the sole runtime ledger, R36 handoff, and the independent R36 Review `REJECT 0/1/1` before writing.
- Frozen controls cover event/API catalogs, lock order, evidence publication boundaries, sensitive-payload allow/deny lists, and acceptance-to-test mappings for wrapper fixture/key equality and all XML semantic paths.
- No Gradle, runtime/unit start/stop/restart, daemon reload, network, DB, RabbitMQ, Chromium, production access, deployment, package copy, final publication, or unknown cleanup occurred.

## R36 preservation

R36 remained inactive and byte-exact:

| Artifact | SHA-256 |
| --- | --- |
| Package manifest root | `e94730ebfc64b8e99ec140545a914ef60a776130e985afd489fcace2ee7df779` |
| Builder manifest root | `271722718143b92dfdb090e6e59dd1d6e0a3afa806233678c1389be33677143a` |
| Accepted static manifest root | `0c8b6291912bd494928a8316af8605352acfec366f054b74063a8e484f7d3827` |
| Wrapper | `01780d5e4b00b650e289788f5a90bf578358bfef2cfb4fabba5b39158bdd05f7` |
| Sealer | `6a9b889e30c56521a03b5e88acad3ae20876a3b5e88fb5ea84835713fcee0605` |
| Unit | `51fa1e7e6b38b04137a939deba880950bfe21cb0bc14ec33f5ed983f31222c16` |
| Activation | `91fc1e2f1203e5910826f31db11d48b398837917444a0f1f0f16e0795b6cf60d` |

All eight intended R37 final paths remained absent.

## Frozen R37 acceptance design

The preserved builder froze these exact successor requirements before source generation:

1. write exact R37 init bytes once and measure their SHA once;
2. derive wrapper hydration/bridge fixtures, coverage, argv catalog, 17 canonical NUL-separated keys, and XML paths from that measured init/build-root source of truth;
3. reconstruct the wrapper's actual nine online argv arrays and receipt keys and require byte-equality with coverage/catalog projections;
4. require all 14 non-null XML paths to equal `externalBuildRoot/<project-key>/test-results/<test-task>` with no extra `/build` segment, while orders `8`, `9`, and `17` remain null;
5. reject any R30/R36 digest or path in the final wrapper;
6. retain 18 wrapper references, five delegated traversal probes, three workspace adversarial rejects, pycache-zero, fixture before/after package metadata equality, two-phase evidence, real tool manifests/forbidden observations, Python 3.6, and fresh disk gates.

Freeze files and their digests are sealed inside the builder.

## Consecutive failure matrix

| Attempt | Category | Symptom | Root cause | Safety result | Bounded successor |
| --- | --- | --- | --- | --- | --- |
| 1 | `python36_pprint_sort_dicts_unsupported` | Source-of-truth module generation raised `TypeError` before writing the module. | Host Python `3.6` does not support `pprint.pformat(sort_dicts=...)`. | No package copy, final path, product/R36 mutation, or prohibited operation. | The sole retry switched to deterministic JSON-serialized step definitions compatible with Python 3.6. |
| 2 | `hardcoded_init_sha_expectation_mismatch` | The retry generated `r37_contract.py` and an explicit external cfile, then failed an init-SHA assertion. | The retry self-check independently hardcoded a guessed digest `7ea7ece1...` instead of deriving the expected value from generated init bytes. The generated source-of-truth measured `2a7d86da852a7813707bb733598a432cdf544f72174432fda82efc85e1a166fe`. This contradicted the single-source-of-truth objective inside the construction check itself. | No package staging copy or final R37 path. Product and R36 remained exact. | Stop R37. A fresh R38 must write init bytes first, measure once, and thread only that measured value through every derived artifact and assertion. |

The second failure was attributed through the orchestrator under notification `0b48ff9fa582c2c891169e9e5d64ca1304bb03d17224d65e3ef015333b98b719`; blind continuation is forbidden.

## Preserved failed builder

- Builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r37-builder-P36LGdiQ`
- Builder manifest root: `02902c81eecf5cdf600205a64486ca717b93a92fd9596c0d8f9ede8fe71e9604`
- Builder root-file SHA-256: `9db93c6e442d9c7a104044609dbdbd62c99c6f564e4b3cfa6f363782e84c8331`
- Files: `11`
- Preserved partial source SHA-256: `4e631d68f6fd4c91ce04c6ee8a23e6c7e163814747bba702ea1f2fb53da9cda0`
- Failure attribution SHA-256 values:
  - attempt 1: `0db787d850a33b354128bce0deb176e4de54064f0ca4bb369bd7148772a60285`
  - attempt 2: `1ea51c44d3531aec1dcd9ba7668388132a455fe8cfee5c1637ea812df3458aa2`
  - matrix: `25f60b2364d2dbefcea947adbdc32c715e1dedf2667e5c3181c8ed60010defce`

The partial source is evidence only and is not an accepted generator/package.

## Disk gate observation

The initial frozen observation was `4684582912` available bytes and the terminal observation was `4683124736`, both below the retained `5368709120` minimum. No final-publication gate was attempted and no unrelated path was cleaned. A successor must admit staging only when a fresh observation also includes sufficient staging headroom, so it cannot turn a known low-disk condition into another counted construction failure.

## Required next action

Do not retry or overwrite R37. Only a separately authorized fresh, non-overwriting R38 may continue. It must preserve R36 and R37, avoid any hardcoded init digest, measure exact init bytes once, generate wrapper fixtures/coverage/argv/17 keys/XML paths from that value, and execute the new wrapper-actual argv/receipt and all-XML static gates before independent Review. Runtime remains unauthorized.
