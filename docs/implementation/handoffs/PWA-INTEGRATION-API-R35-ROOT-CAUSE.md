# PWA-INTEGRATION-API-RC R35 blocked root cause

Date: 2026-09-01

## Terminal state

- Ledger gate: `blocked_root_cause`
- Consecutive accepted-static-verifier failures: `2`
- Product source: unchanged, clean, exact commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`
- Runtime/Gradle/network/DB/RabbitMQ/Chromium/deploy/daemon-reload/start: not run
- R35 unit observation: loaded, inactive/dead, `MainPID=0`, `ControlPID=0`, `NRestarts=0`, all start/active/inactive monotonic timestamps `0`
- R35 is **not review-ready** and has no accepted static evidence root.

## Exact preserved roots

- Builder: `/run/cyf-pwa-api-r19-static-verifier-r35-builder-vn4qisr1`
- Package: `/run/cyf-pwa-api-r19-static-verifier-r35-preparation`
- Wrapper: `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r35`
- Sealer: `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r35-seal`
- Unit: `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r35.service`
- Activation: `/var/tmp/cyf-pwa-api-r19-static-verifier-r35.activation.json`
- Workspace: `/var/tmp/cyf-pwa-api-r19-static-verifier-r35-workspace`
- Failed evidence 1: `/run/cyf-pwa-api-r19-static-verification-r35-20260901T184205-2640563`
- Failed evidence 2: `/run/cyf-pwa-api-r19-static-verification-r35-retry-20260901T184431-2642261`

Do not mutate, remove, start, or reuse these R35 paths.

## Exact digests

- Current unaccepted package manifest SHA-256: `189cb4bf48f457625709f2e2a2e18f8509cf6fb4bf5db2a76fb75e2ef0396813`
- Generator SHA-256: `bb0a10f9617e5c0b4b90688184c87922485f7ca8d47047aff13c4d33f04c91c7`
- Accepted-verifier source SHA-256: `bfeaadaef924534a99846ca8a91a34f4ddd026db453ec5a7c8d5d77311f5b6b9`
- Freeze SHA-256: `1da4d94361de0e95cfb6d18d262f76136025710b47df85e989d3c67080a533b5`
- Acceptance-to-test SHA-256: `33fb48108bd20d2b10d20ac702a494c653a11fcdff7cf733d7dccc88115832f2`
- Failure 1 SHA-256: `1e1cca60fa2be31698880e4cb1e3671c07469866c52b94ca1858525103b05cf1`
- Failure 2 SHA-256: `aacc0291d01a2ec6d0ceb48b556706cf3c80922148a81b3e0d096fe81ac69683`

The package manifest is not an acceptance root: the first fixture invocation added unmanifested `__pycache__/runtime_prepare.cpython-36.pyc` bytes.

## Root-cause matrix

| Attempt | Category | Exact cause | Evidence |
|---|---|---|---|
| 1 | `static_fixture_simulation_ancestor_traversal_contract` | The fixture correctly made the simulated workspace `root:61019 0710`, but its outer `tempfile.mkdtemp` ancestor remained `root:root 0700`; delegated `61019:61019` could not traverse it. | Failed evidence 1 `failure.json`; builder `control/static-verifier.stderr` |
| 2 | `accepted_fixture_package_bytecode_mutation_between_attempts` | The exact packaged fixture imported package modules without disabling bytecode writes. The first run, as root, created package-local `__pycache__` after the pre-fixture path check. The retry then correctly rejected the two unmanifested paths at `PACKAGE_PATHS` equality. | Failed evidence 2 `failure.json`; builder `control/static-verifier-retry.stderr` |

These are independent fixture/verifier defects. The second failure exhausted R35's retry budget.

## Preserved successful construction observations

- Wrapper declares exact R35 `PREP` on line 2, before `set -Eeuo pipefail` on line 3.
- Wrapper init is exactly `pwa-api-r19-r35.init.gradle`; no alternate init filename exists.
- Workspace parent is `root:61019 0710`; its exact five children are `61019:61019 0700` and empty.
- R35 acceptance/argv/H06/toolchain catalogs were regenerated with no `R30/r30/R34/r34` tokens.
- Publication df gates passed with `5,808,701,440`, `5,809,430,528`, and retry-finalization `5,805,084,672` available bytes, each above `5,368,709,120`.
- R34 remains immutable: package root `35eeca708341340825e77fa8c961d14f94159f72bbc07708711179bc9ed8b7e9`; builder root `d63f7a4dc168108216a02da8c996b0d6bac00151b62605d99b1a524db8462f97`.

## Required R36 remediation

A separately authorized fresh R36 must:

1. Ordinary-copy immutable R34 into completely fresh, non-overwriting roots; do not copy or clean R35.
2. Before publication, set the semantic fixture's outer temporary ancestor to `root:61019 0710`.
3. Set `sys.dont_write_bytecode = True` in the packaged fixture and invoke it with `PYTHONDONTWRITEBYTECODE=1`.
4. Snapshot exact package path metadata before and after fixture execution and fail unless byte-equal.
5. Retain R35's PREP-before-`set -u`, exact reference/init, delegated traversal, R35-only catalog, two-phase evidence, 17 NUL-key, toolchain, forbidden-observation, Python 3.6, and nullable XML contracts.
6. Re-run only from a fresh evidence root with fresh root `df -B1` gates immediately before final publication and static sealing.

No R35 retry or repair is authorized.
