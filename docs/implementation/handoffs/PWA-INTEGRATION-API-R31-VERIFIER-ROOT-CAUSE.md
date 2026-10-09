# PWA API R31 static verifier root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r31-20260901` / `critical_worker` / `writer`
Terminal gate: **`blocked_root_cause`; owner released; no R31 Review request or runtime authorization**

## Authority and atomic R31 claim

- R31 was atomically authorized with `cyf_orchestrator.py authorize-remediation` against committed R30 matrix `docs/implementation/handoffs/PWA-INTEGRATION-API-R30-VERIFIER-ROOT-CAUSE.md` at commit `6060ca51c64eb4ea391f869a67371b6bffaeeaa9`.
- Exact R30 matrix/handoff SHA-256: `593c45ed2dc86d3b89c8b0570f04778b4cb20e8544961dd91c5d490aabf72b9d`.
- Only the fresh R31 consecutive-failure counter was reset to zero. All R20–R30 attempts remained in the sole runtime ledger.
- Immutable product remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.

## Frozen R31 verifier contract

Fresh non-overwriting root: `/var/tmp/cyf-pwa-api-r19-static-verification-r31-qjygjoho`.

Before verifier execution, R31 froze:

- unchanged event/API/identity/ACL/transaction/migration/sensitive-payload semantics;
- lock order and read-only transaction boundaries;
- sensitive-payload allowlist and denial list;
- exact subprocess allowlist limited to read-only Git and systemd state queries;
- forbidden operations; and
- acceptance-to-test coverage for authority, builder provenance, consumed staging absence, published final digest binding, package path/mode/owner/digest inventory, immutable manifest, activation/package root, unit inactivity, preservation, and Review boundary.

Evidence:

| Artifact | SHA-256 |
|---|---|
| `control/freeze.json` | `066f442738048ccca4cd223930173d8433e0a1af86868b68d84569ae3678e832` |
| `source/verify-r31.py` | `2354f1ce7517b707b25b0c6fd1496ff862c35903310488ea14bf5150d8012e12` |
| external `compile-output/verify-r31.pyc` | `91cdf13e5158b7ab93f16be0668b6a5c744afe74731155ef32b724bdecd41258` |

The verifier did not compile or execute R30 package/donor files in place.

## R31 failure matrix

| Attempt | Result | Root cause | Safety result |
|---|---|---|---|
| Fresh R31 targeted static verifier | Failed closed after authority, sealed R30 builder manifest, builder path-set, and provenance-record digest checks | The verifier applied the compile classification mode/UID/GID tuple for the builder-local `orchestrator-fixture` copy to the live coordination-control source `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py`. Those paths are digest-bound but have different ownership domains. The compile record describes pre-seal staging mode `0555`; the current sealed staging copy is mode `0400`; the live control source is mode `0755`. Only package-owned PREP/wrapper/sealer publications should inherit classification metadata. | Failure JSON SHA-256 `0007039feeaf721cef24e536c13f679ee6daf5d0278b385ae0ca5f86e3fb3713`; stderr SHA-256 `975602e7db2d02ae74e1418a1fa77db4b0e804ac83eca892e288117d7dba6a0a`; stdout empty. No R30 path was written, no runtime started, and no prohibited operation occurred. |
| Sole R31 retry construction | Failed closed before `tempfile.mkdtemp`, source creation, compile, or verifier execution | Retry preparation transcribed an expected first-failure SHA-256 `d63e643a...` instead of measuring the preserved file directly. The actual immutable first-failure SHA-256 is `0007039f...`; the binding assertion correctly stopped before a retry root existed. | Sealed failure root `/var/tmp/cyf-pwa-api-r19-static-verification-r31-retry-construction-failure-vjuqic8m`; failure SHA-256 `e594ec80542fcc7604fd3ddebbf7aa0c9a412a8d6214d9b2ae07e3aa4b0faedc`; manifest root `941ca29a426808cb3899a4181a96ec8a16cac4dfc7efd6df5c699a190f6fa954`. No retry verifier ran. |

The first failure was attributed through the orchestrator, and the sole ledger was reread at category/count `r31_orchestrator_fixture_staging_mode_applied_to_external_control_path` / `1` before retry preparation. The second failure was then attributed through the same entrypoint, triggering the mandatory stop.

## Preserved R30 package state

R31 did not rebuild, alter, activate, or start the successful inactive R30 package. Post-failure read-only checks remained exact:

- builder manifest root: `548d4a3e30fba4424219a1276d418d20ae3c0e499eb86640e07fa5428d17fe85`;
- compile evidence: `e5ba8923f23a9ec9d1587685add11086a0998b4bc0e505d0db80be11d1986dc9`;
- package root/final inventory: `1cb1e29414b5d3adf90d306308d525693208bb24062bd413cab0b3a1738bb5fb`;
- activation record SHA-256: `d006d1164570c2b616d0ceefe0e4ab92ecdf7ed99c49c6922daa62d45cd6002a`;
- product commit/tree remained exact and clean;
- unit remained `inactive` / `dead`, `MainPID=0`, `ExecMainStartTimestampMonotonic=0`.

R21 was not rerun. No Gradle, network, DB, RabbitMQ, Chromium, production, deploy, daemon reload, service start/stop/restart, package mutation, donor execution, unknown deletion, or runtime action occurred.

## Terminal state and successor boundary

The sole runtime ledger is now:

- gate: `blocked_root_cause`;
- owner: `null`;
- category: `r31_retry_first_failure_digest_transcription_mismatch`;
- fresh R31 consecutive failures: `2`.

R31 produced no static PASS and must not enter independent Review. Preserve both R31 evidence roots, the successful inactive R30 package, R30 evidence, and every predecessor exactly.

Only a separately authorized fresh non-overwriting R32 may continue. It must bind this committed matrix and the live count `2`, measure the preserved first-failure digest directly rather than transcribing it, and correct only the verifier distinction between the digest-bound live orchestrator control source and package-owned published metadata. It must retain the required consumed staging absence PASS assertion and all remaining immutable package/unit/activation/product/donor/forbidden-operation checks. No R21, R30 mutation/rebuild, runtime, Gradle, network, DB, RabbitMQ, Chromium, production, deploy, or daemon reload is authorized.
