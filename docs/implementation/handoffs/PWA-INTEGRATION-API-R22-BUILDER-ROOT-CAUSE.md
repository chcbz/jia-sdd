# PWA API R22 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `01a05aa2-f1a3-7603-a7b9-97067a321970` / `critical_worker` / `writer`
Terminal state: **`blocked_root_cause`; owner released; no R22 static package, unit, activation record, or Review candidate**

## Exact authority and product

- Product worktree: `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19`
- Product commit/tree: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`
- Product remained clean; no product-source byte changed.
- Durable R22 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R21-BUILDER-ROOT-CAUSE.md`, commit `5145bfd5100b7a6bf0577be683f0f7ac34a3db13`, file SHA-256 `5d32ea4ea00c66e63db49778eb13421f92ad540b94952fc689f1c0ab87671c5f`.
- R21 remained immutable. Its sole successful live probe was not rerun.

## R22 failures

| Attempt | Result | Root cause | Safety result |
|---|---|---|---|
| Fresh activation-inventory inspection | Failed before freeze/source publication | The read-only helper used `ast.get_source_segment`, which is unavailable in the required host Python `3.6.8`. | Attributed through the orchestrator. The fresh R22 builder contained only control evidence; no source/package/final path was published. The sole bounded retry switched to Python-3.6-compatible AST/token inventory logic. |
| Authorized bounded freeze retry | Failed while verifying the immutable R13 sealed manifest | The new verifier incorrectly required relative manifest names. R13's valid 50-row `SHA256SUMS.builder` uses absolute paths, all contained under the exact sealed R13 builder root. | This was the second consecutive R22 failure. Execution stopped before activation inventory publication, inherited-probe copying, preservation snapshot, package source construction, package publication, unit, activation, or Review transition. |

The exact second failure was `r22_sealed_r13_manifest_absolute_path_rejection`. A correct successor verifier must accept both relative-under-root and absolute-under-root entries after normalization and exact-root containment checks.

## Sealed R22 builder

Builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r22-builder-584839eb2ff24243a97a4479fb9617df`

- `SHA256SUMS.builder`: 12 payload rows, verified at sealing.
- Builder root SHA-256: `8d0494d498404212c4ddc61fc4412c7b18e83587596ff183862ed78c6d0f8c7f`.
- Root-cause matrix SHA-256: `00e30062a2c3492ed41b7dfb3a80906eeecb15357fb2bb5547013581bf2bbffe`.
- Terminal marker SHA-256: `89d814da7ca1ab63703e87988465fd07a189b588bc158a78f0cd93b170931202`.
- R21 probe result remained SHA-256 `78033882439cfe30b5d28cc0412e7a6994f3cab1dbe61ee49aaf02f9147ff707`, `PASS`, and was not rerun.
- R21–R13 sealed builder manifests were read-only reverified using the predecessor-compatible containment rule during terminal sealing. R13 has 50 absolute-under-root entries; no predecessor mutation occurred.
- Every frozen R22 final path is absent, including `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r22.service`.

## Frozen activation rewrite requirement

R22 did not reach activation-inventory publication. The successor requirement remains unchanged and is now coupled to the manifest fix:

1. Parse the immutable R13 `ACTIVATION_CHECK_TEXT` assignment with Python-3.6-compatible AST APIs.
2. Freeze exactly four semantic full-literal identities before publication: preparation root, wrapper path, sealer path, and unit path.
3. Rewrite those four enumerated literals with AST/token-semantic assertions, exactly once each.
4. Assert total old activation identity cardinality is four before and zero after.
5. Do not use singleton replacement or a broad package-identity replacement.

## Prohibited operations and successor boundary

- No Gradle, runtime unit start, network, DB, RabbitMQ, Chromium, production access, deployment, daemon reload, or product-source write occurred.
- No R22 package/root/package-manifest/activation digest exists because publication never began.
- R22 is not reviewable and must remain sealed.
- Only a separately authorized fresh non-overwriting successor may continue. It must use a new builder identity, preserve R18–R22 and R17–R13, never rerun the R21 probe, fix sealed-manifest absolute/relative containment, and then perform the explicit four-occurrence AST/token activation-identity rewrite.
