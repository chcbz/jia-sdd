# R01 foundation R2 candidate (not full R01 acceptance)

Original critical writer handed over clean `ae311a1deb74ad4aae3a78e45303766af4124c8f`, tree `2cd1bc06ad783565466d0d8ee4493e20f5e95f9f`, parent rejected `a7f7ac17d1133f9f97f0f874c4b826f1e1ef2d98`. Ten changed hosting-specific paths; no shared posting delta. Main confirmed clean exact SHA/tree/parent. No Gradle/DB/runtime performed by writer.

Reported corrections (pending independent review/runtime):
- Exact columns/index/CHECK/immutable-trigger validation; explicit RowCallbackHandler fixes r1b compile ambiguity. Test source includes17 malformed catalog variants.
- Trusted internal FUNDS_RESERVED/PROVISIONING_UNKNOWN→SERVICE_READY CAS, persisted readiness time, then capture. Unknown still held without proof; duplicate/stale/foreign callbacks covered in source.
- Refund frees nullable live-Agent uniqueness slot while retaining historical lease/intent/escrow, enabling fresh retry with old-callback fencing.

Targeted schema text/H2 service/noDB regressions plus isolated MySQL catalog/shared-posting verification still required. R01 root-cause matrix remains `ECO-V0-R01-R1-ROOT-CAUSE.md`; source fixes alone do not close it. Default charging remains disabled, no seed/deployment. HTTP, canonical Agent/binding authorization and allocation, after-commit managed provisioning proof, manual renewal, expiry/new-work admission and wallet held-version integration remain downstream.

Writer proposed HTTP DTOs for later freeze: existing persona hosting-rent quote with explicit INITIAL purpose/optional existing Agent, server bind with INITIAL/REPROVISION action and quote/plan/amount/period confirmation, canonical Agent lease lookup, lease renewal quote and renewal confirmation. All use JsonResult/exact JWT principal, canonical decimal strings and immutable admission receipts. No public readiness/refund callback. Main must resolve identity allocation/authorization/readiness semantics before advertising R02 DTO freeze.

## Independent R2 source result

Original independent reviewer `01a07116-f22e-7351-9af4-e66dbcee21da`: **ACCEPT P0/P1/P2=0/0/0**, exact ten-path delta. Catalog/trigger/callback typing, owned/versioned SERVICE_READY reconciliation, and history-preserving retry close the three prior P1s in source. No new conservation or lock defect found; regression sources consistent. No runtime artifacts inspected, tests not run. Source acceptance does not replace exact noDB/H2/MySQL execution or imply full R01 completion.

Verification dispatch held before launch: orchestrator rejected R01 verifier assignment because three existing read-only slots are occupied (unrelated API artifact verifier plus host-adapt/landscape reviewers). No R2 Gradle run or ledger mutation occurred; R01 remains awaiting_verifier. Conflict alert emitted; no preemption or guard bypass. Main script remains ready for the next naturally available admitted verifier.
