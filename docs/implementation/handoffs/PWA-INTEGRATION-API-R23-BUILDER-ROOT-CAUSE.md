# PWA API R23 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`  
Writer: `01a5d481-4fa1-488c-820b-284cd9db0bbc` / `critical_worker` / `writer`  
Terminal state: **`blocked_root_cause`; owner released; no R23 package, unit, activation record, or Review candidate**

## Exact authority and immutable product

- Product worktree: `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19`.
- Product commit/tree: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- Product remained clean and byte-exact; no product source was edited.
- Durable R23 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R22-BUILDER-ROOT-CAUSE.md`, commit `88913bf0dd33c19aa55540078881a2a6aca02d78`, file SHA-256 `019c6664f79f56adfce86a7173d48c60d6e849c2df7aaf1bcd5b37ae85dec44a`.
- The orchestrator authorization preserved all six R20–R22 attempt records and reset only the consecutive-failure counter before R23.

## R23 failure matrix

| Attempt | Result | Root cause | Safety result |
|---|---|---|---|
| Fresh R23 preparation | Failed at Python 3.6 activation-source token binding | On host Python `3.6.8`, the multiline raw `ast.Str` for `ACTIVATION_CHECK_TEXT` reports the closing line with `col_offset=-1`; the first extractor incorrectly required a STRING token at that AST coordinate. | Attributed through the orchestrator. The first builder created only builder-owned manifest fixtures/control evidence. No generator, package staging, final path, unit, or activation existed. |
| Sole bounded retry | Failed at retry authorization binding before construction | The retry corrected extraction to an explicit tokenize assignment-state parser, but retained the pre-attribution assertion `category=r22_sealed_r13_manifest_absolute_path_rejection,count=0`. Required first-failure attribution had correctly changed the live binding to `category=r23_python36_multiline_string_ast_location_mismatch,count=1`. | This was the second consecutive R23 failure. It stopped before manifest fixtures, predecessor reads, activation extraction, source publication, or package construction. |

Failure evidence:

- First: `/var/tmp/cyf-pwa-api-r19-static-verifier-r23-builder-05f8b70a850e460b93d0bddc2279d514/control/source-extraction-failure-1.txt`, SHA-256 `49baf2df01dfa7d6faabcf327326c873536e208c215ece28281569f3208cb933`.
- Retry: `/var/tmp/cyf-pwa-api-r19-static-verifier-r23-builder-210cf855d8994bae886bd2cfca4f7b29/control/retry-authorization-failure-2.txt`, SHA-256 `4256ba19ceb4b0f3c2f98f340f256a9bdf8d986d195d22f8d233f6127abc7efe`.
- Terminal matrix: `/var/tmp/cyf-pwa-api-r19-static-verifier-r23-builder-210cf855d8994bae886bd2cfca4f7b29/control/root-cause-matrix.json`, SHA-256 `5736ccbdb09a7b162051260b8459f32a2a2b412fdad9a564180559bcdb4bf974`.

## Sealed R23 attempts

1. First builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r23-builder-05f8b70a850e460b93d0bddc2279d514`
   - Manifest rows: `14`.
   - Builder root SHA-256: `63d8f0728a64f9f17156b4ebe325a468432ce866e23b83abb2df19687bdb1a8f`.
2. Retry builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r23-builder-210cf855d8994bae886bd2cfca4f7b29`
   - Manifest rows: `12`.
   - Builder root SHA-256: `89c3279471f4e249e5a3d94557d8e54bfc2724299f818d47a9b4bab3aa6b0c43`.
   - Terminal marker SHA-256: `13e569e5a603ca24d16a1c13ed53fc9ca61dd8dcd917756061e31f365a1e64e6`.

Terminal read-only revalidation accepted both relative-under-root and absolute-under-root sealed-manifest entries after normalization and lexical/realpath containment. R22–R13 roots verified, including all **50 valid R13 absolute-under-root rows**. This terminal verification did not resume package construction.

## Preserved safety state

- The R21 live probe was never rerun or reused.
- R18–R22 and R17–R13 sealed builders were read-only reverified; no predecessor path was edited, deleted, relinked, chmod/chown modified, or reused.
- Every R23 final path is absent, including `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r23.service`.
- No package/root/package-manifest/activation digest exists because package publication never began.
- No Gradle, runtime unit start, network, DB, RabbitMQ, Chromium, production access, deployment, or daemon reload occurred.

## Successor boundary

R23 is not reviewable and must remain sealed. Only a separately authorized fresh non-overwriting R24 successor may continue. It must:

1. bind initial authorization to this committed matrix and retain all R20–R23 attempts;
2. for any bounded retry, bind to the live first-R24 attributed category and `consecutive_failures=1`, not the pre-attribution category/count;
3. use the corrected Python-3.6-compatible tokenize assignment-state extraction: exactly one `NAME ACTIVATION_CHECK_TEXT`, followed by `OP =`, followed by exactly one `STRING`, with `ast.literal_eval` equal to the sole top-level AST assignment value;
4. retain normalized relative/absolute-under-root manifest acceptance while rejecting traversal, lexical escape, and realpath escape, preserving the 50 R13 rows;
5. perform the frozen four-role activation rewrite with pre-old `4`, post-old `0`, post-new `4`, AST/token/compile assertions, and no singleton or broad identity replacement;
6. never rerun the R21 probe or mutate/reuse either R23 builder or any R18–R22/R17–R13 path; and
7. stop again after a second consecutive R24 failure.
