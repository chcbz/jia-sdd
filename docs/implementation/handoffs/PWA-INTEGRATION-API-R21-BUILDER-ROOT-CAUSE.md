# PWA API R21 builder root-cause matrix — 2026-08-30

Task: `PWA-INTEGRATION-API-RC`
Writer: `01a053ca-cb13-7360-907b-9ab50855e747` / `critical_worker` / `writer`
Host ledger/journal clock preserved verbatim: `2026-08-31`
Terminal state: **`blocked_root_cause`; owner released; no R21 static package, unit, activation record, or Review candidate**

## Exact authority and product

- Product worktree: `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19`
- Product commit/tree: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`
- The worktree remained clean; no product-source byte changed.
- Durable R21 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R20-RUNTIME-ROOT-CAUSE.md`, SHA-256 `33a2eff82d3bf5a3059661736d02c4e285f3b3e8e7c0da891ed5e4622192798c`.
- Preserved R20 builder root: `087e9fad1ad58950a639c9ff9870ca0d5cec88b2cd2554841a99b722d2ddb10a`.

## Successful sole live probe

The unique R21 mount-only probe ran exactly once and passed all remaining behavior checks:

- Unit: `cyf-pwa-api-r19-r21-mount-probe-f823dc0dc0b14829ae1c1a1705ea5e69.service`
- Dedicated runtime directory: `/run/cyf-pwa-api-r19-r21-mount-probe-f823dc0dc0b14829ae1c1a1705ea5e69`
- Pure parser fixtures passed `4/4` before launch, including mount `ro` overriding superblock `rw`.
- Exact root was effectively read-only; exact `docs/implementation` was writable; longest-prefix root/docs records were correct; no broad writable source mount existed.
- Root and delegated `61019:61019` source/orchestrator writes were denied without residue; docs create/read/remove passed; source JDK was inaccessible.
- The script self-unlinked, full mountinfo/properties were captured, and `--collect` left the unit `not-found/inactive/dead` with PIDs and restarts zero. The dedicated `/run` directory is absent.
- Probe result SHA-256: `78033882439cfe30b5d28cc0412e7a6994f3cab1dbe61ee49aaf02f9147ff707`.

This probe must never be rerun or reused.

## R21 builder failures

| Attempt | Result | Root cause | Safety result |
|---|---|---|---|
| Fresh source-construction controller | Failed before publishing any package source | The controller embedded triple-single-quoted delegated shell blocks inside an outer triple-single-quoted runtime-fragment literal, causing a Python syntax error. | Attributed through the orchestrator. No package staging/final path was created. The one allowed retry changed the outer delimiter and precompiled the controller. |
| Authorized bounded retry | Failed while preparing a file-backed activation-check fragment | The activation checker legitimately contains four R13 package-identity occurrences, but the controller used a singleton `replace_once` guard. The valid multiplicity was rejected after only partial builder-owned source-staging publication. | This was the second consecutive failure. Construction stopped immediately; no bootstrap, deriver, package publication, unit, activation record, or Review transition occurred. |

Failure evidence:

- `control/source-construction-failure-1.txt`, SHA-256 `617767a46db2718761837fe23af5e00bee446d54db1d122ac2f49c9a0bfa4f97`
- `control/source-construction-failure-2.txt`, SHA-256 `2b30759cf0e72c0279b1723bcf575f74bf6f75d369651ff38bc137fa7c3c7953`
- `control/root-cause-matrix.json`, SHA-256 `8f2ec809e6e9a0c8fc8b6f37f2ed7faee970f6ee5df03a4958afc1de848ede81`

## Sealed blocked builder and preservation

Builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r21-builder-224a2d52998e47bba95baf4dda6b9b4f`

- `SHA256SUMS.builder` has 48 rows and verifies cleanly.
- Builder root SHA-256: `455a263fff1da61458659c194f17abca6b49ff6605c0107e045917b249c997da`.
- Terminal marker SHA-256: `1a8297f5cf220bf25e9cc4664ecfea7e669727b49c82f82335b93550353930cf`.
- R18–R20 and R17–R13 preservation is byte/metadata exact: 1,184 entries, root `a55b75c49add25c622379d90cbdfc72938efd64fe1cb83433c4ab977c0658293` before and after.
- Every frozen R21 final path is absent, including `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r21.service`; `publish-staging` is absent.
- The fixed free-space gate `5368709120` passed. No Gradle, package runtime, product-source write, network, DB, RabbitMQ, Chromium, production, deployment, or daemon reload occurred.

## Successor boundary

R21 is not reviewable and must remain sealed. Only a separately matrix-registered fresh successor may continue. It must:

1. use a new builder identity and never rerun or mutate the R21 probe/evidence;
2. inherit the successful R21 probe topology and parser semantics;
3. freeze an explicit inventory for the four activation identity occurrences, then use an AST literal rewrite or enumerated semantic map rather than a singleton replacement guard;
4. preserve R18–R21 and R17–R13 exactly; and
5. create a fresh non-overwriting package only after its complete file-backed source set compiles under Python 3.6 before `O_EXCL` publication.
