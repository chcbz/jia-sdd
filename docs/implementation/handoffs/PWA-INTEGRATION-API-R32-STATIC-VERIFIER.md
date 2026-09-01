# PWA API R32 static verifier handoff — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`

Writer: `sol-pwa-integration-api-r32-20260901` / `critical_worker` / `writer`

Candidate gate: **static PASS; package remains inactive; handoff is ready for independent `sol_reviewer` review**

## Authority and immutable candidate

- R32 was atomically authorized from committed R31 matrix `docs/implementation/handoffs/PWA-INTEGRATION-API-R31-VERIFIER-ROOT-CAUSE.md` at commit `f0d66e8911beaa53824faf5956ca5eedad0cbf17`.
- The verifier computed the committed R31 matrix SHA-256 in-process as `9c508d98a5eb58aeb2199c509acaa47b6ad3ab82332278e053570e3a4a07a565` and bound the same bytes to the live path; it did not use a transcribed evidence digest.
- The committed R30 matrix was loaded from `6060ca51c64eb4ea391f869a67371b6bffaeeaa9:docs/implementation/handoffs/PWA-INTEGRATION-API-R30-VERIFIER-ROOT-CAUSE.md` and measured in-process as `593c45ed2dc86d3b89c8b0570f04778b4cb20e8544961dd91c5d490aabf72b9d`.
- Product remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- R30 remained immutable: builder root `548d4a3e30fba4424219a1276d418d20ae3c0e499eb86640e07fa5428d17fe85`; package root `1cb1e29414b5d3adf90d306308d525693208bb24062bd413cab0b3a1738bb5fb`.

## R32 execution history

| Attempt | Result | Evidence | Safety |
|---|---|---|---|
| Complete pre-root preflight | Failed closed before verifier root/source creation | `/var/tmp/cyf-pwa-api-r19-static-verification-r32-preflight-failure-dhjzadvf/failure.json` SHA-256 `b9880ca41958896839f5e63834fcac952f8947811ab067b08d2388bc69049cbf`; sealed manifest root `9226953fabae023d21ae06b91821c5566ae3238d82215c7dbf6f449a96c5e506` | Parser expected nonexistent surrounding wording for the R31 retry digest. Failure was attributed through the orchestrator; no verifier root, package write, runtime, Gradle, or prohibited operation occurred. |
| Sole R32 retry | PASS | `/var/tmp/cyf-pwa-api-r19-static-verification-r32-retry-ujqf_8bw`; sealed manifest root `800014ca8c405fc62b02d8be2a16b28b65e08585d0246c4185e8fc9984aef1eb` | Complete configuration and every referenced regular file were preflighted before root allocation, then rechecked by the fresh verifier. R30/R31/R32-first evidence remained read-only. |

The first failure category was `r32_preflight_r31_retry_digest_regex_context_mismatch`. After attribution and sole-ledger reread at count `1`, the retry changed only authority parsing/retry-state binding: the digest parser anchored on the unique sealed-failure-root row, and the verifier bound the attributed first-R32 failure from its own sealed manifest rather than copied digest text.

## Frozen contract and metadata domains

- Event/API/identity/ACL/transaction/migration/sensitive-payload semantics: unchanged.
- Writes: fresh R32 retry root only through exclusive creation; R30 package and R31 evidence read-only.
- Builder-owned retained fixtures were checked as sealed root-owned mode `0400` regular files.
- Package-owned PREP/wrapper/sealer publications were checked against their classification digest and published mode/UID/GID.
- The live orchestrator path was **not** compared to fixture mode/UID/GID. Its measured live mode was `0755`, while historical compile mode was `0555` and sealed fixture mode was `0400`. Live bytes were independently Git-bound to commit/blob `de23c23550b184b6cbaaef85d184f18a313e6d33` / `38b56518e9752c7c5bc1d1e26e266ed4b6afe2e6`.
- All authoritative R30/R31 manifest/JSON bindings were measured in-process and recorded as source-path plus computed SHA-256; binding count: `55`.

## Static acceptance result

| Acceptance | Result |
|---|---|
| Committed authority, R31 count `2`, attributed R32 retry count `1` | PASS |
| Preserved R31 first/retry roots and sealed R32 first failure | PASS |
| Builder manifest/path-set/owner/mode/digest | PASS: `41` rows |
| Consumed staging absence | PASS: `6` exact PREP sources absent |
| PREP path/type/mode/UID/GID set | PASS: `393` paths |
| Package regular-file digest manifest/transcript | PASS: `367` items |
| Activation bindings and inventory root | PASS: `ACTIVATION_PASS crash_safe_fail_closed=true commit_point=activation_record paths=393 manifest_items=367` |
| Unit inactive/dead/static, MainPID=0, never-started monotonic=0 | PASS |
| Product/donor/R18/predecessors/R30 failed evidence unchanged | PASS |
| Runtime directories empty; forbidden operations absent | PASS |
| Review boundary | PASS: evidence sealed before review transition |

## Evidence

- Evidence selector: `R32_STATIC_ONLY|authority+metadata-domains+consumed-staging+package+activation+inactive-unit+preservation+forbidden-ops`
- Fixture digest: `R30_PACKAGE_ROOT:1cb1e29414b5d3adf90d306308d525693208bb24062bd413cab0b3a1738bb5fb`
- Evidence key: `2f58ae3d24a4aa5fddfc7b7ed7fac0cb38d9d499d6162e4415e541d86aa59e31`
- R32 manifest root: `800014ca8c405fc62b02d8be2a16b28b65e08585d0246c4185e8fc9984aef1eb`
- Result SHA-256: `b87f8339e81d38071c49dca4a4c6a3c62825212f1ebebc216034bb6e78b85c05`
- Detail SHA-256: `299c1da77863ab195918bfe17336d415db43909483c74c46dee27f67b0035c7e`
- Freeze SHA-256: `0f8701dccadb35f1427244cd4543e0f02d8a856f10f5a600b57b74b9c639b683`
- Verifier source SHA-256: `d8868e0805514292e3395bd675164bb677d4717df1f6c14169feaeff62b5f059`
- External cfile SHA-256: `a6da62f190d414b7a0e6fea912009d721cc8042931d875f793738c9ba62bc9a0`
- Verifier stdout SHA-256: `0912a0586353c90bb60a1ebf91f844f36235d585ca3cae934d4839c5c25c722c`
- Verifier stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)

No R21, R30 rebuild/mutation, runtime start/stop/restart, Gradle, network, DB, RabbitMQ, Chromium, production, deploy, daemon reload, donor execution, hardlink, unknown deletion, or service action occurred.

## Independent review boundary

Review the exact immutable product/package and sealed R32 root above. Confirm the separated metadata domains, in-process digest provenance, complete pre-root file preflight, consumed staging absence, package/activation/unit checks, predecessor preservation, and forbidden-operation boundary. Do not start the unit or run Gradle/runtime/production actions.
