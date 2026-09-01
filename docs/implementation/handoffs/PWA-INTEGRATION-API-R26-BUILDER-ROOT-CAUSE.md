# PWA API R26 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`  
Writer: `sol-pwa-integration-api-r26-20260901` / `critical_worker` / `writer`  
Terminal state: **`blocked_root_cause`; owner released; no R26 controller, static package, activation record, unit, or Review candidate**

## Authority and immutable product

- Durable R26 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R25-BUILDER-ROOT-CAUSE.md` at commit `8a4d0af2153ff93c1d8376220544bf81f47f7da8`, file SHA-256 `d64e3d0c003e492416866f79b84159a9fcfe0aa95f122387cb422d44500928ec`.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- The orchestrator atomically authorized R26, preserved every R20–R25 attempt, and reset only the fresh R26 consecutive-failure counter.
- The immutable donor was measured from bytes at runtime as SHA-256 `83a7d5537338c65858d3948a5418d8556522a75b58731ee25f18008f641a7b7f`; no manually transcribed donor constant was used by the R26 constructor design.
- R21's successful live probe was never rerun. No predecessor builder, final path, product source, or production state was modified.

## Frozen R26 contract

Before controller construction, both fresh builders froze:

1. unchanged product API/event/schema and identity/ACL/transaction/migration semantics;
2. publication lock order and crash-safe fail-closed transaction boundaries;
3. sensitive-payload allowlist and forbidden operations;
4. exactly three named required-category roles: `controller_runtime_authorization`, `generator_template_authorization`, and `generated_builder_authorization`, each validated at its own representation layer without `source.count` or raw marker cardinality;
5. Python 3.6 AST/token location of the outer `sealed_specs` assignment, with STRING tokens treated atomically so decoded template contents cannot count as outer syntax;
6. separate decode/transform/compile/re-encode of the `verify_auth` STRING token;
7. parameterized old/new activation identity with exactly four semantic token spans, unchanged-outside-span bytes, pre-old `4`, post-old `0`, post-new `4`, decoded literal/AST/cardinality/compile assertions; and
8. normalized relative/absolute-under-root manifest acceptance, traversal/lexical/realpath escape rejection, and `sha256sum -c` from each exact root.

## R26 failure matrix

| Attempt | Result | Root cause | Safety result |
| --- | --- | --- | --- |
| Fresh R26 builder | Failed before controller publication | The structural locator correctly isolated the sole outer module-level `sealed_specs` assignment, but reused a tuple helper that called `ast.literal_eval`. The outer tuple contains legitimate bound `Name` nodes such as `R23_RETRY`, `R22`, `R21`, `R18`, and `R13`; literal evaluation therefore failed closed. | No controller, package, activation, unit, or final path was published. The failure was attributed through the orchestrator, then the live ledger was reread before the sole retry. |
| Sole fresh R26 retry | Failed in the mandatory pure in-memory exact-donor fixture | The retry corrected the outer tuple handling by inserting after the structurally located opening token without literal-evaluating the old tuple. The next structural helper reparsed source and searched the new AST for a node from the previous AST using Python object identity. Reparse creates distinct node objects, so `top_level_node_identity` failed before controller publication. | This was the second consecutive R26 failure. Construction stopped immediately; no controller, generated builder, package, activation, unit, final path, or Review candidate exists. |

## Sealed evidence

### First builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r26-builder-fd43508cbd834b0c9c845527334af89a`.
- Manifest: `14/14` PASS from the exact builder root.
- Builder root SHA-256: `d2fec4b81651d923e3b411aa9ac8b165c4d68681c41780a455de249cee70e117`.
- Failure record SHA-256: `ae49274894416200f4ed8a7392389473b73d50ed903fc3b238409479a0208dcb`.

### Sole retry builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r26-builder-6654390d8ba848bdae07244c460b7bb6`.
- Manifest: `15/15` PASS from the exact builder root.
- Builder root SHA-256: `229893fc385d644f7aabb1c5363413cadc20c3b97f57b734b8118e6f66e12755`.
- Failure record SHA-256: `849dfb4873a0e75eb9d941b2ba2ad59c4ea4b1e30d75d681718b8d01d7424fdb`.
- Builder root-cause matrix SHA-256: `5ba0db8d0cf5b0f8fc98990b2c1b38a4e7fe3e9605d2812008c678c993a24eef`.
- The retry independently reverified the first R26 builder before sealing.

## Final absence and prohibited-operation result

All R26 final paths remain absent:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r26-preparation`
2. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r26`
3. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r26-seal`
4. `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r26.service`
5. `/var/tmp/cyf-pwa-api-r19-static-verifier-r26-evidence`
6. `/var/tmp/cyf-pwa-api-r19-static-verifier-r26-workspace`
7. `/var/tmp/cyf-pwa-api-r19-static-verifier-r26-incidents`
8. `/var/tmp/cyf-pwa-api-r19-static-verifier-r26.activation.json`

No product-source write, R21 probe rerun, predecessor mutation, Gradle, runtime start/stop/restart, network, DB, RabbitMQ, Chromium, production access, deployment, or daemon reload occurred.

## Successor boundary

R26 is not reviewable. Only a separately authorized fresh non-overwriting R27 may continue. It must:

1. bind authorization to this committed matrix and preserve both sealed R26 builders plus all R13–R25 evidence;
2. compute top-level replacement spans from the same parsed AST/body index or stable `(node type, name, lineno, col_offset)` coordinates—never object identity across reparses;
3. retain the corrected outer `sealed_specs` opening-token insertion without literal-evaluating its Name-bearing tuple, while structurally validating the inserted AST prefix;
4. separately decode, structurally transform, compile, and re-encode the `verify_auth` STRING;
5. validate the three named authorization roles at controller/template/final-generated layers without `source.count` or raw marker cardinality;
6. retain the expected-identity activation locator, exact four spans, unchanged-outside-span proof, semantic/AST/cardinality/compile assertions, and normalized manifest verifier with correct cwd; and
7. stop again after a second consecutive R27 failure.
