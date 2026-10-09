# PWA API R29 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r29-20260901` / `critical_worker` / `writer`
Terminal state: **`blocked_root_cause`; owner released; no R29 static package, unit, activation record, runtime evidence, or Review candidate**

## Authority and immutable product

- R29 authorization was bound atomically to committed R28 matrix `docs/implementation/handoffs/PWA-INTEGRATION-API-R28-BUILDER-ROOT-CAUSE.md` at commit `281c989fdd9275e042121a1f250c2341e6982c03`; exact matrix SHA-256 `b0cc8c8a2b3be86d452f988a555dcb8db4d175bc79641532070002be6a0ee2a6`.
- Only the fresh R29 consecutive-failure counter was reset. All R20–R28 attempts remain in the sole runtime ledger.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- R21 was not rerun. No final R29 path was created. No Gradle, runtime start/stop/restart, network, DB, RabbitMQ, Chromium, production, deployment, or daemon reload occurred.

## R18 logical quarantine

R29 followed the user safety correction and did **not** clean, repair, compile, execute, or use R18 as a donor. It loaded R28 `failure-1.json` directly, SHA-256 `65d163147a86513013eaca1f328c067e3e2793823519609906260cc276aa74c6`, and preserved the exact contamination:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r18-preparation/__pycache__/activation_check.cpython-36.pyc` — `d83217d5b0a5ed6350eb5c7b285ee5ce568326ea9c7f564541a9c610055494fe`.
2. `/var/tmp/cyf-pwa-api-r19-static-verifier-r18-preparation/__pycache__/mount_contract.cpython-36.pyc` — `d0fa1fa82b2804a4e0a4c2e0bc2294612210c026891c4909a5bdae74c286bcb9`.
3. `/usr/local/libexec/__pycache__/cyf-pwa-api-r19-static-verifier-r18-sealcpython-36.pyc` — `61d1c3fa0d4f27b32793467ed2d57d049429c7389d7a04e0266441f9346290a9`.

The two cache-directory records and all three child/file modes, owners, links, sizes, mtimes, ctimes, and hashes remain exact against the R28 failure record. R18 remains non-authoritative because its path set is contaminated and its preparation-directory ctime is irrecoverable. Quarantine evidence SHA-256: `a56bea36f094004608feb64ed3fd5b64f3c9b8956036bd9ced4968f2127d5ee3`.

## Donor selection and frozen contracts

Before donor copying, the retry wrote the event/API catalog, lock order, publication transaction boundaries, sensitive-payload allowlist, prohibited-operation list, and acceptance-to-test map. Freeze SHA-256: `8a282b7858d0ddc8a7cd8bf3edd4e150efa8b216f6050f2fa99bba178348f443`.

Read-only independent selection result:

- R17 sealed builder manifest: `37/37` PASS, root `18b528b0284ba9a7da7a4c2560fd7123e422323647765eaf89a4621a35d47f39`; ineligible because R17 never produced a package path set or activation record.
- R13 sealed builder manifest: `50/50` PASS, root `49b61dc187883b6eeb2065f1c7641087c63f975eab7ff96c59be634ae8d71452`.
- R13 package: exact `393` path entries, `367` manifest items, verification transcript exact, and staged activation bindings independently PASS without executing or compiling donor files in place.
- Therefore R13 was selected as the newest complete eligible donor. Donor-selection evidence SHA-256: `9f4cf29fe4ac49100047af8cb20ccbead790023f0b8c14698682e86a4711869d`.
- Donor before/after full metadata and regular-file digest projections are exact: both `b23f359dd05a8dba07dc065707df30406262bdaa3de2002cc82ae8d77f97d2e3`. Preservation evidence SHA-256: `cd1204e41028711b025bcd8cc6df466a6af3dd8064efdc31c7e3c84dea82676b`.

## One-layer constructor status

R29 authored a complete one-layer data-driven constructor from scratch at retry-builder `source/build-r29.py`, SHA-256 `6639e6b17d20dbd0ab9fda18735e8e5dfd09cfa732c9a1fa68fbc4804ca355b0`. It does not patch inherited constructor text and contains no nested generator source strings.

The complete constructor compiled under Python 3.6 with `PYTHONDONTWRITEBYTECODE=1` and explicit external cfile `pycompile-control/build-r29.preflight.pyc`, SHA-256 `a1054739ce909994ca0d7a868541a62d20214c58332440b12d3f2a0a2f5aa7ef`. During execution it:

- wrote frozen catalogs before donor copying;
- used portable `os.statvfs`, `df -Pk`, and separate `df -Pi` parsing from the final POSIX columns;
- independently verified R17/R13 and selected R13;
- created only R29-owned staging;
- copied only regular files with independent `O_CREAT|O_EXCL` inodes;
- applied explicit file-specific identity and mount-topology transforms in staging; and
- never compiled beside donor/source paths.

It stopped before transform-proof completion, pure fixture, package manifest publication, activation, final publication, or unit creation.

## R29 failure matrix

| Attempt | Result | Root cause | Safety result |
| --- | --- | --- | --- |
| Fresh R29 | Failed before freeze execution | The inline freeze helper had an accidental trailing quote after the `sensitive_payload_allowlist` list literal, producing `SyntaxError`. | Only a unique empty R29 builder and failure record were created. Failure was attributed, the live ledger was reread, and one fresh retry was used. |
| Sole R29 retry | Failed during staged-copy syntax checking | The constructor correctly discovered Python files by suffix/shebang, but then unconditionally appended both wrapper and sealer to the Python compile list. The wrapper is Bash; Python rejected line 2, `set -Eeuo pipefail`. The outer shell also used ambiguous nounset expansion for the tee target, but the owned process traceback was recovered and the substantive constructor failure was the script-type classification bug. | No final path was published. Only R29-owned staging copies and control evidence exist. This was the second consecutive R29 failure, so execution stopped. |

Failure evidence:

- Fresh failure: `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-builder-EaZLdnm4/control/failure-1.txt`, SHA-256 `0c7c4eda4b5ee736e3adf36bcdc1390534de730c86fd389de18ee5823d5fa691`.
- Retry failure: `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-retry-builder-z6o0zlTV/control/failure-2.txt`, SHA-256 `475186714b3bf6c77c48a0e4b8be79879a7c18559db4a4618b085dffd2928d98`.
- Common sealed root-cause matrix SHA-256: `efe44d7cc1865dfbae85e4aecdbe222c26c474116dc6addacce356717239605e`.

## Sealed builders and final absence

- Fresh builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-builder-EaZLdnm4`; `4/4` manifest PASS; root SHA-256 `c501a1b9eb3f666c03c766be98abeaa9f2ad0a9e3419d069bb8359a7b62830c0`.
- Sole retry builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-retry-builder-z6o0zlTV`; `386/386` manifest PASS; root SHA-256 `dcd1dcaa8885521f7c1db3a850d131a561dfb966b41523145f564bda6d1dd5ad`.

All R29 final paths are absent:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-preparation`
2. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r29`
3. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r29-seal`
4. `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r29.service`
5. `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-evidence`
6. `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-workspace`
7. `/var/tmp/cyf-pwa-api-r19-static-verifier-r29-incidents`
8. `/var/tmp/cyf-pwa-api-r19-static-verifier-r29.activation.json`

No R29 package, pure activation fixture verdict, static unit, activation record, package/root digest, or Review candidate exists.

## Successor boundary

R29 is not reviewable. Only a separately authorized fresh non-overwriting R30 may continue. It must:

1. bind to this committed matrix and preserve both sealed R29 builders plus all predecessor evidence;
2. retain R18 logical quarantine exactly and continue using the independently verified R13 donor;
3. classify every R30 staged script by suffix and shebang before syntax validation;
4. compile only Python copies with `PYTHONDONTWRITEBYTECODE=1` and explicit external `cfile`; validate the Bash wrapper with a non-executing shell parser on the R30 copy;
5. use an unambiguous builder-local result path such as `${R30B}/control/result.json`, never `$R30B_RESULT`;
6. resume from a fresh R30 builder, not from R29 staging, and retain explicit file-specific cardinality, unchanged-byte, mode/owner, manifest, pure-fixture, fail-closed publication, and unit-last checks; and
7. never rerun R21 or perform Gradle/runtime/network/DB/Rabbit/Chromium/production/deploy/daemon-reload actions during static construction.
