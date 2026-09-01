# PWA API R28 builder root-cause matrix — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r28-20260901` / `critical_worker` / `writer`
Terminal state: **`blocked_root_cause`; owner released; no R28 constructor, fixture, static package, unit, activation record, or Review candidate**

## Authority and immutable product

- Durable R28 authority: `docs/implementation/handoffs/PWA-INTEGRATION-API-R27-BUILDER-ROOT-CAUSE.md` at commit `04e11c0b891dda6a78f763ed16f7f33adbfcb8f4`.
- The committed authority file still measures SHA-256 `e37582e08a30fc5e083c2df1153c36a6db62e64dd8af4f7ca08b6d2999a74377`.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained clean and exact at commit/tree `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- The orchestrator atomically authorized only fresh R28, preserved all historical attempt records, and reset only the R28 consecutive-failure counter. The first failure was attributed and the live ledger was reread before the sole retry.
- R21's successful mount probe was never rerun. No Gradle, runtime start/stop/restart, daemon reload, network, DB, RabbitMQ, Chromium, production access, deployment, or product-source write occurred.

## Required strategic pivot and where R28 stopped

R28 was required to author a complete small data-driven constructor from scratch, treat each sealed predecessor package/runtime file as an individually measured donor, run a pure temporary fixture before final publication, and avoid inherited R13–R27 constructor rewriting. R28 stopped during read-only preparation, before donor-catalog freeze or constructor authoring, because the preparation command itself violated the immutable-donor boundary. The retry was limited to exact cleanup and stopped before any constructor or final-path publication.

## R28 failure matrix

| Attempt | Result | Root cause | Safety result |
| --- | --- | --- | --- |
| Fresh R28 preparation | Failed during inspection-only syntax validation | A direct `python3 -m py_compile` command targeted the sealed R18 `activation_check.py`, `mount_contract.py`, and sealer without explicit external `cfile` destinations. Running as root created package-adjacent `__pycache__` objects. R18's 367-row content manifest still passed because regular donor bytes were unchanged, but its activation checker correctly rejected the now-unlisted path set. | Failure was attributed through the orchestrator. Every R28 final path remained absent. Three writer-created pyc files and two cache directories were preserved for the bounded cleanup retry; the R18 preparation directory ctime change is irreversible. |
| Sole R28 retry | Failed closed before any unlink or rmdir | The cleanup program manually transcribed guessed SHA-256 values rather than loading the sealed first-failure JSON. Its first sorted target was `/usr/local/libexec/__pycache__/cyf-pwa-api-r19-static-verifier-r18-sealcpython-36.pyc`: configured `a3ba2f…`, sealed/measured `61d1c3…`. The assertion stopped before cleanup mutation. | This was the second consecutive R28 failure. No cleanup occurred in the retry, no fixture/constructor/package/unit/activation/final path exists, and R28 entered `blocked_root_cause`. |

## Sealed evidence

### Fresh R28 builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r28-builder-cc81626293034253`.
- Manifest: `3/3` PASS from the exact builder root.
- Builder root SHA-256: `f233047439a325f25d55d334b4c2c23a3666feec1c25f36a3dabd0fcf6156b7c`.
- Failure record SHA-256: `65d163147a86513013eaca1f328c067e3e2793823519609906260cc276aa74c6`.

### Sole retry builder

- Path: `/var/tmp/cyf-pwa-api-r19-static-verifier-r28-builder-f206a1045bb5436e`.
- Manifest: `9/9` PASS from the exact builder root.
- Builder root SHA-256: `f00cccfb0556d96de1cd2f66b845f95580d711c77107fdf16e12b2299b1e945d`.
- Failure record SHA-256: `6908e14dc73f23af93c05c2d788dd5c94e3ef7590042792104fa1a3fe9efecf2`.
- Builder root-cause matrix SHA-256: `c4b78a12f4a59ac9dc20790542acc6660bcbf514fdc37f67c3a6802b172e55ea`.
- Cleanup source SHA-256: `64f956158d2ee0a40fae8fc7f1b99a4fec354a3e6447e0d7fe241c1e773406b8`.

## Exact contamination state

The following R28-created cache files remain present and are the only recorded added regular files:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r18-preparation/__pycache__/activation_check.cpython-36.pyc` — SHA-256 `d83217d5b0a5ed6350eb5c7b285ee5ce568326ea9c7f564541a9c610055494fe`.
2. `/var/tmp/cyf-pwa-api-r19-static-verifier-r18-preparation/__pycache__/mount_contract.cpython-36.pyc` — SHA-256 `d0fa1fa82b2804a4e0a4c2e0bc2294612210c026891c4909a5bdae74c286bcb9`.
3. `/usr/local/libexec/__pycache__/cyf-pwa-api-r19-static-verifier-r18-sealcpython-36.pyc` — SHA-256 `61d1c3fa0d4f27b32793467ed2d57d049429c7389d7a04e0266441f9346290a9`.

The corresponding exact cache directories remain present. The sealed R18 package's regular files and `SHA256SUMS.package` remain byte-valid, but `activation_check.py` returns `ACTIVATION_REJECT path_set`. No claim of exact R18 package metadata preservation is made; its preparation-directory ctime cannot be restored.

## Final absence and prohibited-operation result

All R28 final paths remain absent:

1. `/var/tmp/cyf-pwa-api-r19-static-verifier-r28-preparation`
2. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r28`
3. `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r28-seal`
4. `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r28.service`
5. `/var/tmp/cyf-pwa-api-r19-static-verifier-r28-evidence`
6. `/var/tmp/cyf-pwa-api-r19-static-verifier-r28-workspace`
7. `/var/tmp/cyf-pwa-api-r19-static-verifier-r28-incidents`
8. `/var/tmp/cyf-pwa-api-r19-static-verifier-r28.activation.json`

No R28 constructor, pure fixture, donor catalog, publication staging, package/root digest, unit, activation, or static Review candidate was produced.

## Successor boundary

R28 is not reviewable. Only a separately authorized fresh non-overwriting R29 may continue. It must:

1. bind authorization to this committed matrix and preserve both sealed R28 builders plus all R13–R27 evidence;
2. load the exact candidate paths and SHA-256 values directly from sealed `failure-1.json`, never manually transcribe them;
3. prevalidate **all** candidate files, inodes, modes, owners, links, hashes, directory memberships, and exact empty-after-removal directory conditions before the first unlink;
4. after complete prevalidation, unlink only the three exact R28-created files and remove only the two exact cache directories if empty, then record the irrecoverable R18 directory ctime delta and prove the original 393-entry path inventory and R18 activation PASS;
5. never compile any donor path in place; compile only fresh staged copies with explicit external bytecode destinations;
6. only after cleanup proof, restart the requested fresh one-layer data-driven constructor, portable `statvfs`/`df -Pi` resource snapshot, pure temporary fixture, frozen inventory diff, and offline static checks; and
7. never rerun R21 or perform Gradle/runtime/network/DB/Rabbit/Chromium/production/deployment/daemon-reload actions during static construction.
