# PWA API R30 static verifier root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r30-20260901` / `critical_worker` / `writer`
Terminal gate: **`blocked_root_cause`; owner released; successful static package preserved but no R30 Review request or runtime authorization**

## Authority and immutable product

- R30 was atomically authorized against committed R29 matrix `docs/implementation/handoffs/PWA-INTEGRATION-API-R29-BUILDER-ROOT-CAUSE.md` at commit `ce336542c70136cadd0224a1e569f1fa8abe440f`; exact matrix SHA-256 `79d44a226987a345fc7e70c5dc80170824d94c8de8b59366bc4f703059e0fb7e`.
- Only the fresh R30 consecutive-failure counter was reset. The complete R20–R29 attempt history remained in the sole runtime ledger during execution.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- R21 was not rerun. No Gradle, network, DB, RabbitMQ, Chromium, production, deployment, daemon reload, or service start/stop/restart occurred.

## Frozen construction contracts

Both R30 constructors were authored as complete one-layer, data-driven sources; neither patched inherited constructor text. Every newly created constructor was syntax-checked before use in its own builder copy with `PYTHONDONTWRITEBYTECODE=1` and an explicit external `cfile` under that builder's R30-only `compile-output/` directory.

The successful retry froze, before donor copying:

- event/API/identity/ACL/transaction/migration/payload semantics: unchanged;
- publication lock order and crash-safe fail-closed transaction boundaries;
- sensitive-payload allowlist and explicit denial list;
- prohibited operations;
- script-role catalog; and
- acceptance-to-test coverage.

Its unambiguous builder-local regular-file results are:

| Result | Path | SHA-256 |
|---|---|---|
| Freeze | `control/freeze-result.json` | `9da38c5729421a6a0a3ccfc7ebb83a2364470f9abd74178db209f5dbf5db6b05` |
| Compile/classification | `control/compile-output-result.json` | `e5ba8923f23a9ec9d1587685add11086a0998b4bc0e505d0db80be11d1986dc9` |
| Static result | `control/static-result.json` | `cbbfef9df8d4d2455c168c1640f750f5d131b7bc731bfba573d356a6399fc308` |
| Final builder manifest | `SHA256SUMS.builder` | `548d4a3e30fba4424219a1276d418d20ae3c0e499eb86640e07fa5428d17fe85` |

## Preservation and donor result

R18 remained logically quarantined. No R18 cleanup, repair, compilation, execution, or donor use occurred. The exact three contamination hashes remained unchanged, and the recursive/exact metadata projection before/after was identical: `c5bbdd684ee8a86dc2db00c8f9ac2724afa838598395477a748df4a8a1ca4ee1`.

R29 fresh/retry builders and the sealed first R30 failure builder were reverified and preserved. Their combined exact metadata projection remained `5e0e0a192e73c81011596187ecade0553ee941e475408a99f10ad59aac0ca738`; normalized projection remained `10d6d3f0310b727d80dba6cebe403acdd684e6b7ef872a3acb1ae351c6b472a9`.

R13 was independently retained as the newest complete eligible donor:

- builder manifest `50/50` PASS, root `49b61dc187883b6eeb2065f1c7641087c63f975eab7ff96c59be634ae8d71452`;
- package path set `393` entries;
- package manifest `367` items and exact verification transcript;
- staged activation bindings PASS without compiling or executing donor files in place;
- exact metadata projection before/after `b23f359dd05a8dba07dc065707df30406262bdaa3de2002cc82ae8d77f97d2e3`; and
- normalized projection before/after `bc120b71bb4b3f67fc64fca9695ae39cb7b15cfcabfcff6ac7a57dbefa8c36b8`.

## Successful static construction

Successful builder: `/var/tmp/cyf-pwa-api-r19-static-verifier-r30-retry-builder-NSJLfc48`.

- Builder manifest: `41/41` rows, root SHA-256 `548d4a3e30fba4424219a1276d418d20ae3c0e499eb86640e07fa5428d17fe85`.
- Package root SHA-256: `1cb1e29414b5d3adf90d306308d525693208bb24062bd413cab0b3a1738bb5fb`.
- Exact package: `393` paths, `367` manifest items.
- Transform proof SHA-256: `4adac3b556885b4750cb6cc0993c9c461474630ed9dd7c96517614ae55fac299`.
- Pure fixture SHA-256: `07226a9289ed903afc530dd0f1dc2ac9ab22b8b77ec37af1616e7fd3963303ca`.
- Publication evidence SHA-256: `1f3e19748292b831b6c24bfa77e72412dbe06fbc8d44ba1bf8fbd78bce2a3bb2`.

Classification was fail-closed against frozen metadata plus suffix/shebang:

- Python only when the frozen role was `python` and Python suffix/shebang matched: seven R30 copies compiled to explicit external cfiles.
- Bash only for the frozen wrapper role with a Bash shebang: one `bash -n` PASS.
- POSIX shell only for the frozen Gradle launcher role with `/bin/sh` shebang: one `sh -n` PASS.
- Donors were never compiled or executed in place; final PREP contains no `__pycache__` or `.pyc` path.

Identity replacement used equal-length positional target unions, preserving every byte outside frozen old-token spans. Mount replacement used non-overlapping segment proof and retained per-mount `ro`/`rw` precedence over superblock flags.

Pure fixture results passed complete activation, missing-activation rejection, wrapper-tamper rejection, unlisted-PREP-path rejection, owned-fixture removal, and restored activation.

Publication used atomic `renameat2(RENAME_NOREPLACE)` for PREP, independent `O_CREAT|O_EXCL` regular-file copies, activation before unit, and root-owned mode `0444` unit publication last. Constructor activation returned:

`ACTIVATION_PASS crash_safe_fail_closed=true commit_point=activation_record paths=393 manifest_items=367`

The final R30 static paths remain present and inactive:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r30-preparation`
2. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r30`
3. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r30-seal`
4. `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r30.service`
5. `/var/tmp/cyf-pwa-api-r19-static-verifier-r30-evidence`
6. `/var/tmp/cyf-pwa-api-r19-static-verifier-r30-workspace`
7. `/var/tmp/cyf-pwa-api-r19-static-verifier-r30-incidents`
8. `/var/tmp/cyf-pwa-api-r19-static-verifier-r30.activation.json`

## R30 failure matrix

| Attempt | Result | Root cause | Safety result |
|---|---|---|---|
| Fresh R30 constructor | Failed in builder-local staging before syntax/package/final publication | The first unchanged-byte proof greedily selected non-overlapping identity spans. Lowercase `r13` occurrences nested inside complete/short identities were transformed through their enclosing replacements but counted as zero separately selected lowercase spans. | Failure attributed before the sole retry. All R30 final paths were absent. Builder `/var/tmp/cyf-pwa-api-r19-static-verifier-r30-builder-6AFqOgTo` was sealed `18/18`, root `0c56b875abae2c770d0c9008173f5660c50c7f9d1a7e4ba97b602435f37c55f8`. |
| Sole R30 retry constructor | PASS | Fresh complete constructor used equal-length positional identity proof and separate mount-segment proof. | Static package, activation record, and unit were published fail-closed; runtime remained unauthorized and inactive. |
| R30 targeted verifier | Failed after Bash/POSIX parser PASS | It incorrectly required every prepublication compile-report source path to remain under the sealed builder. Atomic PREP publication intentionally consumed five compiled Python source paths and the POSIX Gradle source path; external cfiles remained, and final package bytes were already digest-bound. | This was the second consecutive R30 failure. The verifier stopped before its activation/package-root section. Evidence directory `/var/tmp/cyf-pwa-api-r19-static-verification-YmSRO40R`, failure SHA-256 `17033164c11963680d3cc7a35f2adf5d6241972fd7d3e5f924d48c0b621f1519`, diagnostic SHA-256 `c06fab32925ed300850264bea3365efbc94bcf137c2c64de122e89e6ec524825`, manifest SHA-256 `b6ae71a226954bcd5a45805a7111d1693208fdd0dae4c8a668e1f9c7902bf3dc`. |

## Terminal state and successor boundary

The sole runtime ledger is `blocked_root_cause`, owner `null`, category `r30_targeted_verifier_postpublish_consumed_staging_source_path_assumption`, consecutive failures `2`.

R30 must not enter Review and its static unit must not be started. Preserve the successful package and all R30/R29/R18/R13 evidence exactly. Only a separately authorized fresh non-overwriting R31 may continue. It must bind each consumed prepublication syntax-proof source digest to the corresponding final package path instead of requiring moved staging paths to exist, and then independently complete static package/unit/activation verification before any Review request. No R21 rerun, Gradle, runtime, network, DB, RabbitMQ, Chromium, production, deployment, or daemon reload is authorized.
