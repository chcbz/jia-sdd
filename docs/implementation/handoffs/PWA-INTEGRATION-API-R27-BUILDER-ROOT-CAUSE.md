# PWA API R27 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`  
Writer: `sol-pwa-integration-api-r27-20260901` / `critical_worker` / `writer`  
Terminal state: **`blocked_root_cause`; owner released; no R27 constructor, controller, static package, unit, activation record, or Review candidate**

## Authority and immutable product

- Durable R27 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R26-BUILDER-ROOT-CAUSE.md` at commit `28616cb62cb472e0588e953303e9dba0a90bb13c`.
- The committed file bytes measured SHA-256 `ab4be3167c1daa1a02e5de4d7e25e206eed41a093837a3ebd24a5f5a5eb2eb0b`.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- The orchestrator atomically authorized the fresh R27 successor, preserved every R20–R26 attempt, and reset only the fresh consecutive-failure counter. After the first R27 failure it was attributed, the live ledger was reread, and only one fresh non-overwriting retry was attempted.
- Both R26 sealed builders were independently reverified from their exact roots. R21's successful live probe was never rerun.

## Frozen R27 contract

Before implementation, both fresh builders froze:

1. unchanged product API/event/schema and identity/ACL/transaction/migration/payload behavior;
2. publication lock order and crash-safe fail-closed transaction boundaries;
3. sensitive-payload allowlist and forbidden operations;
4. outer `sealed_specs` validation by tuple/list container, row arity, and every element's AST node type, identifier/literal position, and semantic role, with no outer `literal_eval`;
5. byte patching only at structurally located token spans and separate decode/transform/compile/re-encode of the `verify_auth` STRING token;
6. same-parse top-level body indexes or stable structural descriptors, never AST node object identity across reparses;
7. independent reparse and normalized descriptor equality in the pure in-memory exact-donor fixture;
8. exactly three required-category roles at the outer controller, decoded generator template, and generated builder representation layers;
9. parameterized old/new activation identity, exactly four STRING-token spans, unchanged-outside-span proof, pre-old `4`, post-old `0`, post-new `4`, and decoded/AST/cardinality/compile assertions; and
10. normalized relative/absolute-under-root manifests, traversal/lexical/realpath escape rejection, and `sha256sum -c` from each exact root.

## R27 failure matrix

| Attempt | Result | Root cause | Safety result |
| --- | --- | --- | --- |
| Fresh R27 builder | Failed while freezing resource telemetry | The freeze helper invoked GNU `df` with `-i` and `--output=iavail` together. Those options are mutually exclusive, so resource-snapshot publication stopped. | Contract files were written and sealed, but no constructor, controller, generated builder, package, unit, activation, or final path was published. The failure was attributed through the orchestrator and the ledger was reread before the sole retry. |
| Sole fresh R27 retry | Failed during constructor-source generation | The retry generator attempted to replace the inherited `prepend_assignment_rows` implementation by matching one exact multi-line whole-function text block. The immutable R26 constructor did not equal that brittle anchor, so generation raised `prepend_block_missing`. | This was the second consecutive R27 failure. It occurred before constructor compile or `O_EXCL` publication; no controller, generated builder, package, unit, activation, final path, or Review candidate exists. |

The retry therefore failed on its own constructor-editing mechanism before the intended AST/token structural implementation could execute. No claim is made that the frozen R26 causes were closed.

## Sealed evidence

### Fresh builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r27-builder-fb25ba11049d4d5d956d069df29678d4`.
- Manifest: `12/12` PASS from the exact builder root.
- Builder root SHA-256: `5b29d8ff0a827a3a1200819189d4a6180dc1602c91b7a842da2844d88594ab8d`.
- Failure record SHA-256: `caced478bfceae9c0050217c741c3ffe1beb74354a103f43047b4d4ace6eb63d`.

### Sole retry builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r27-builder-8afc311c21bb42a4b849771a6bfc5b9d`.
- Manifest: `16/16` PASS from the exact builder root.
- Builder root SHA-256: `f4042ef7515b36420fcb536baf554a8cb11e26de8a32123c04607511dc0628fb`.
- Failure record SHA-256: `5dc55c1d3791822c036ab2019782018b0f266b3e385827ee8a4fd0c8be39de91`.
- Builder root-cause matrix SHA-256: `d81392f107f4844cd4e6a1abe1ebcfc0a27b7bf4675a601ac9634c7771c81b9f`.
- The retry independently reverified the first R27 builder and both sealed R26 builders before terminal sealing.

## Final absence and prohibited-operation result

All R27 final paths remain absent:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r27-preparation`
2. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r27`
3. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r27-seal`
4. `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r27.service`
5. `/var/tmp/cyf-pwa-api-r19-static-verifier-r27-evidence`
6. `/var/tmp/cyf-pwa-api-r19-static-verifier-r27-workspace`
7. `/var/tmp/cyf-pwa-api-r19-static-verifier-r27-incidents`
8. `/var/tmp/cyf-pwa-api-r19-static-verifier-r27.activation.json`

No product-source write, R21 probe rerun, predecessor mutation, Gradle, runtime start/stop/restart, network, DB, RabbitMQ, Chromium, production access, deployment, or daemon reload occurred.

## Successor boundary

R27 is not reviewable. Only a separately authorized fresh non-overwriting R28 may continue. It must:

1. bind authorization to this committed matrix and preserve both sealed R27 builders plus all R13–R26 evidence;
2. construct the successor controller through parsed AST/token spans or a newly authored complete file, never a whole-function exact-text anchor;
3. retain structural outer `sealed_specs` validation for container/row arity and every field's node type, identifier/literal semantic role, and coordinates without outer `literal_eval`;
4. use same-parse body indexes or stable coordinates/descriptors and independently reparse/compare normalized descriptors in the pure in-memory fixture, never cross-parse node identity;
5. retain separate outer/template/generated representation layers and exactly three named required-category roles;
6. retain the expected-identity activation locator, exact four STRING-token spans, unchanged-outside-span proof, semantic/AST/cardinality/compile checks, and normalized manifest verifier with correct cwd;
7. never rerun R21 or mutate/reuse either R27 builder or any predecessor/final path; and
8. stop again after a second consecutive R28 failure.
