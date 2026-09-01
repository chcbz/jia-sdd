# PWA API R34 fresh static package handoff — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`  
Writer: `sol-pwa-integration-api-r34-20260901` / `critical_worker` / `writer`  
Candidate gate: **static PASS; package is inactive; ready for independent `sol_reviewer`; runtime remains unauthorized**

## Authority and exact product

- The earlier R34 mandatory stop is preserved in `PWA-INTEGRATION-API-R34-BUILDER-ROOT-CAUSE.md` and commit `58ec11fa23ed54c109a0bd508847948a8dd39155`.
- On September 1, 2026, the user explicitly reauthorized bounded R34 continuation after a separate cleanup Owner reported releasing `641101824` bytes. The orchestrator reopened remediation against the committed R34 matrix; no failure history was removed.
- The generator independently measured `5442899968` free bytes immediately before its first final-path operation, passing the exact `>= 5368709120` gate.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- R33 attribution remained byte-exact at SHA-256 `85d00236b563b5f597459daf0ca48ce5e088ede47f027d02e80210144b31d56d`. R30/R33 complete metadata/content projections matched the builder-frozen before images at final seal.

## Fresh exact package roots

| Role | Exact path | Binding |
| --- | --- | --- |
| Sealed builder | `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-builder-oq1inx6b` | builder manifest root `d63f7a4dc168108216a02da8c996b0d6bac00151b62605d99b1a524db8462f97`; root-file SHA-256 `6b1321c2cda02f987fb137fb7f2204961da7d74a7c79d5174ed74fa62d157b5e` |
| Package PREP | `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-preparation` | `398` exact paths; `371` manifest items; package root `35eeca708341340825e77fa8c961d14f94159f72bbc07708711179bc9ed8b7e9` |
| Wrapper | `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r34` | SHA-256 `e36b87833490a3b61b2bf603756ee6e44ce2dac077291974b3158d88435f5151` |
| ExecStopPost sealer | `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r34-seal` | SHA-256 `c0915a59973e360b44eb5235ac9998643376a8746a9080b8b2ff4b0932b8594c` |
| Static unit | `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r34.service` | SHA-256 `d6f21dcfeda7ebadacf981f21fce1a9a98c30c394bd81214962a621b7ae218a2` |
| Activation | `/var/tmp/cyf-pwa-api-r19-static-verifier-r34.activation.json` | SHA-256 `737983c97cc1497460abf1a727d4e5b264093ae5d367fc02fccea7a9be896e36`; `runtime_authorized=false` |
| Runtime evidence root | `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-evidence` | root-owned mode `0700`, empty |
| Runtime workspace | `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-workspace` | exact five mutable children, each `61019:61019`, mode `0700`, empty |
| Incident root | `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-incidents` | root-owned mode `0700`, empty |

Publication was fresh/non-overwriting with PREP first, activation before unit, and unit last. No daemon reload or service action followed publication.

## R30 Review closure

### P1 — exact mutable children

The final workspace contains only:

`home`, `gradle-user-home`, `external-build`, `project-cache`, `tmp`.

Each was observed as a plain empty directory owned by `61019:61019` with mode `0700`. The corrected adversarial fixture passed normal creation and rejected an unlisted child, a symlink child, and a nonempty child. The unit binds `runtime_prepare.py` in `ExecStartPre` before activation checking.

### P1 — provisional to accepted evidence transaction

- The package-local adapter points the exact orchestrator only at `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-evidence/provisional-cache/EVIDENCE_CACHE.json`.
- A Gradle exit cannot directly update the canonical cache.
- Seventeen immutable postcondition receipts are required before a `PREPARED_NOT_PUBLISHED` candidate can be built.
- The adversarial pure fixture proved successful candidate preparation leaves canonical bytes unchanged and an incomplete receipt set rejects before acceptance.
- `ExecStopPost` revalidates service result, main-process terminal identity, cgroup quiescence, candidate state, baseline digest, and collision absence. Its canonical `os.replace` is immediately followed by `os._exit(0)` and is the final publication operation.

### P1 — canonical NUL-separated keys

The static verifier imported the exact packaged orchestrator and independently recomputed:

`sha256(tree_utf8 + NUL + selector_utf8 + NUL + fixture_utf8)`.

All `17` stored keys equal the exact orchestrator result, all are unique, and the ordered online catalog contains exactly `9` keys. The non-XML `bootJar`/bridge rows preserve `external_xml_dir=null` at execution orders `8`, `9`, and `17`; any non-null non-string value is rejected before transformation.

### P1 — real Gradle/Maven digests

The package regenerated manifests from its actual independent copies, and the fresh verifier regenerated them again:

- Gradle actual tree-manifest SHA-256: `5a8e6c65ec11aa964126c38d4578c9c9e0cb085016e9afea7b504a3e7345bed5`.
- Maven actual tree-manifest SHA-256: `ca62af45b9324ad0f7da1591af3f72b0777b16e386069d7398fb5f4a5f197603`.

Both byte-equal the package manifests and their stored coverage bindings. The hardlink-negative check covered `365` corresponding package/donor regular files; every package regular file had `nlink=1` and no corresponding donor inode was reused.

### P2 — real forbidden-operation observation

The sealed verifier evidence contains actual command output, not hardcoded false flags:

- `systemctl show`: `LoadState=loaded`, `ActiveState=inactive`, `SubState=dead`, `MainPID=0`, `ControlPID=0`, `NRestarts=0`, and all three start/enter monotonic timestamps `0`.
- bounded `journalctl -u cyf-pwa-api-r19-static-verifier-r34.service -n 20`: no entries;
- exact `/proc` cgroup/cmdline scan: zero R34 runtime process matches;
- runtime evidence and incident roots: empty;
- product exact-clean and R30/R33 preservation: PASS.

The observation scope is explicitly the exact R34 unit/package/process and product/predecessor metadata; it makes no global claim about unrelated host processes.

## Python 3.6 and R33 root-cause closure

- Host Python was `3.6.8`.
- Generator, setup/patch controls, exact orchestrator, adapter, runtime preparation, transaction, activation, sealer, corrected adversarial fixture, and static verifier all parsed and compiled with explicit external cfiles.
- AST checks rejected `subprocess.run(text=...)` and `capture_output=...`; package code uses `universal_newlines=True` where decoded subprocess output is required.
- Coverage transformation uses an explicit `None` branch and calls `.replace()` only after `isinstance(value, str)`.

## Static verification history and evidence

The first fresh static verifier root is preserved at `/var/tmp/cyf-pwa-api-r19-static-verification-r34-01cde25351e9`. It failed only because its owned transaction-case parent was not created before `prep.mkdir()`; it did not run Gradle/runtime or alter the package/canonical cache. The sealed failure manifest root is `7c645c8df94748732f61b01ed8cd228e1ee45b2eff4fe24303d7ef52196f0413`.

The sole fresh retry corrected only that builder-local fixture parent creation and passed:

- Evidence root: `/var/tmp/cyf-pwa-api-r19-static-verification-r34-retry-420552ed3332`.
- Selector: `R34_STATIC_ONLY|fresh-package+mutable-children+transaction+canonical-keys+real-toolchain-digests+python36+forbidden-observation+preservation`.
- Fixture digest: `R34_PACKAGE_ROOT:35eeca708341340825e77fa8c961d14f94159f72bbc07708711179bc9ed8b7e9`.
- Evidence key: `ede93727e20e2a124d43ebdd52f93759ee2ed497835bffa7777ed27a2674408a`.
- Static manifest root: `829a26324b0a4fc448a48e17e9e10706991d03fd2f269cf2d413b21e56bae670`.
- Static manifest-root file SHA-256: `fe16edde2cedff71221c087a15bf5d4abe46b98cd5bad609a7a357f4835a4aff`.
- Result SHA-256: `ecb7a29be1b3bc17981d99574572ebe58435efe4ce4fa5a89a1cd3251414a8d7`.
- Details SHA-256: `73298c48ebeda7f8f512e7739e7fb69a76afbab98ce76ca9f1ad5c424d1e4c26`.
- Forbidden-observation SHA-256: `1b8d4cebda17fa3925a4ced1276ad8251cb6c847b2c2b26f207623a9766207f8`.
- Static-seal disk observation: `5438767104` free bytes, passing `>= 5368709120` immediately before manifest sealing.

## Prohibited-operation result and review boundary

No runtime/unit start, stop, or restart; Gradle; canonical accepted-cache publication; daemon reload; network hydration; DB; RabbitMQ; Chromium; production access; deployment; R21 rerun; hardlink; unknown cleanup; or R30/R31/R32/R33 mutation occurred.

Independent Review must inspect the exact package, builder, failed verifier root, and successful sealed verifier root above. Runtime remains separately gated and must not be started by the Reviewer.
