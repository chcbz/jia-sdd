# PWA-INTEGRATION-API-RC R36 fresh static package handoff — 2026-09-01

Task: `PWA-INTEGRATION-API-RC`
Writer: `sol-pwa-integration-api-r36-20260901` / `critical_worker` / `writer`
Candidate gate: **static PASS; package inactive; ready for independent `sol_reviewer`; runtime remains unauthorized**

## Authority and exact product

- Authorized remediation notification: `cb1da87c7d46123c3c63b392f36435757c48b3041f8896c1ddf0a77035201acf`.
- Durable predecessors read before implementation: R34 static handoff, R34 Review `REJECT 0/4/0`, and `PWA-INTEGRATION-API-R35-ROOT-CAUSE.md`.
- Product worktree `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19` remained read-only, clean, and exact at commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`.
- R36 began as an ordinary independent byte copy of immutable R34 package `/var/tmp/cyf-pwa-api-r19-static-verifier-r34-preparation`. R34 remained exact at package root `35eeca708341340825e77fa8c961d14f94159f72bbc07708711179bc9ed8b7e9` and builder root `d63f7a4dc168108216a02da8c996b0d6bac00151b62605d99b1a524db8462f97`.
- All R35 `/run/...r35...` roots and failed evidence were preserved. The observed R35 package manifest remained `189cb4bf48f457625709f2e2a2e18f8509cf6fb4bf5db2a76fb75e2ef0396813`.

## Exact fresh roots and bindings

| Role | Exact path | Binding |
| --- | --- | --- |
| Sealed builder | `/var/tmp/cyf-pwa-api-r19-static-verifier-r36-builder-ZwabUscc` | builder manifest root `271722718143b92dfdb090e6e59dd1d6e0a3afa806233678c1389be33677143a`; root-file SHA-256 `96a6bab931501b322a862c3278d08b86be527a1ab9bc5e9258d10af65f8611f0`; 60 files |
| Package PREP | `/var/tmp/cyf-pwa-api-r19-static-verifier-r36-preparation` | 401 exact paths; 374 manifest items; package root `e94730ebfc64b8e99ec140545a914ef60a776130e985afd489fcace2ee7df779` |
| Wrapper | `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r36` | SHA-256 `01780d5e4b00b650e289788f5a90bf578358bfef2cfb4fabba5b39158bdd05f7` |
| ExecStopPost sealer | `/usr/local/libexec/cyf-pwa-api-r19-static-verifier-r36-seal` | SHA-256 `6a9b889e30c56521a03b5e88acad3ae20876a3b5e88fb5ea84835713fcee0605` |
| Static unit | `/etc/systemd/system/cyf-pwa-api-r19-static-verifier-r36.service` | SHA-256 `51fa1e7e6b38b04137a939deba880950bfe21cb0bc14ec33f5ed983f31222c16` |
| Activation | `/var/tmp/cyf-pwa-api-r19-static-verifier-r36.activation.json` | SHA-256 `91fc1e2f1203e5910826f31db11d48b398837917444a0f1f0f16e0795b6cf60d`; `runtime_authorized=false` |
| Runtime evidence | `/var/tmp/cyf-pwa-api-r19-static-verifier-r36-evidence` | root-owned mode `0700`, empty |
| Runtime workspace | `/var/tmp/cyf-pwa-api-r19-static-verifier-r36-workspace` | parent `root:61019` mode `0710`; exact five empty children `61019:61019` mode `0700` |
| Incident root | `/var/tmp/cyf-pwa-api-r19-static-verifier-r36-incidents` | root-owned mode `0700`, empty |

Publication remained inactive and non-overwriting. No daemon reload or service action followed publication.

## R34 Review 0/4/0 closure

1. **PREP declaration and init binding:** wrapper line 2 declares exact R36 `PREP`, before `set -Eeuo pipefail` on line 3. The only accepted init is `pwa-api-r19-r36.init.gradle`.
2. **Workspace traversal:** the final parent is `0:61019:0710`; only `home`, `gradle-user-home`, `external-build`, `project-cache`, and `tmp` exist beneath it. Each child is empty `61019:61019:0700`. Exact `setpriv` probes created/read/removed a file as `61019:61019` in all five children and denied unrelated `61020:61020`.
3. **Accepted evidence semantics:** the verifier executed exact packaged fixture `/var/tmp/cyf-pwa-api-r19-static-verifier-r36-preparation/static_contract_tests.py`, not a builder-local substitute. It semantically validated all 18 wrapper package references, the exact wrapper reference set, five delegated traversals, three adversarial workspace rejections, complete two-stage evidence preparation, and final sealer ordering.
4. **R36-only catalogs:** `acceptance-coverage.json`, `argv-catalog.posix-quoted.txt`, `h06-donor-catalog.json`, and `toolchain-catalog.json` contain zero `R30/r30/R34/r34` tokens. All 17 argv rows bind the exact R36 adapter and init.

## R35 root-cause closure

- The packaged fixture sets `sys.dont_write_bytecode=True`; the accepted verifier invokes it with `PYTHONDONTWRITEBYTECODE=1`.
- All temporary and final traversal ancestors were checked. The fixture reported 39 temporary-ancestor and 29 final-ancestor traversal checks.
- Exact package `SHA256SUMS.package`, `PACKAGE_PATHS.json`, and full metadata projections were byte-equal before and after the fixture.
- No package `__pycache__` directory or `.pyc` file existed before or after the accepted fixture.

## Retained safety contracts

- Two-stage evidence remains provisional cache → 17 validated receipts → `PREPARED_NOT_PUBLISHED` candidate → quiescent `ExecStopPost` final atomic canonical replace.
- All 17 canonical keys equal `sha256(tree_utf8 + NUL + selector_utf8 + NUL + fixture_utf8)`, are unique, and preserve exactly nine ordered online keys.
- `external_xml_dir=null` remains exact at execution orders `8`, `9`, and `17`.
- Host Python `3.6.8` compiled all nine verifier-selected sources to explicit external cfiles; AST checks found no `subprocess.run(text=...)` or `capture_output=...`.
- Actual final toolchain manifests are Gradle `5a8e6c65ec11aa964126c38d4578c9c9e0cb085016e9afea7b504a3e7345bed5` and Maven local `ca62af45b9324ad0f7da1591af3f72b0777b16e386069d7398fb5f4a5f197603`. The hardlink-negative check covered 368 corresponding files.

## Attributed first attempt and sole repair

The first accepted static verifier root `/var/tmp/cyf-pwa-api-r19-static-verification-r36-20260901T191556-2670106` failed after the exact packaged fixture had passed, because the generated Gradle/Maven tree manifests recorded staging-root mode `0700` while the final roots were mode `0555`. Only the toolchain root rows differed. The failure was attributed through the orchestrator as `toolchain_manifest_root_mode_finalization_order`, notification `eaa01a86545502f557d9b3c7cb6408edabfb267f599efc3ca4082882e9eb56ea`.

- Failure SHA-256: `70108f0e7e3e73f123f1a521654c3c93277adabdb47367293b9cc173bf0220e5`.
- Sealed failure manifest root: `4f45b0e075aa7c520630648744556a8596eb09626297aecbeed608bf7b9b46fe`.
- Failure root-file SHA-256: `a7e35660a3f1236035401111652713540b44d72e605e8e9b0c6f92ad99aa34b3`.

The sole bounded repair normalized toolchain roots before manifest measurement in the generator, regenerated exact final toolchain manifests and all dependent coverage/catalog/wrapper/package/activation bindings, retained byte-exact `PACKAGE_PATHS.json`, and left the runtime inactive. Repair terminal SHA-256 is included in the sealed builder; the repaired package root is the final root above.

## Disk gates

Each gate independently executed `/usr/bin/df -B1 /` and required at least `5368709120` bytes:

- Initial final publication: `5384540160` bytes — PASS.
- Retry package finalization: `5672476672` bytes — PASS.
- Accepted verifier entry: `5671747584` bytes — PASS.
- Static evidence seal: `5672120320` bytes — PASS.
- Final builder seal: `5670780928` bytes — PASS.

## Accepted static evidence

- Evidence root: `/var/tmp/cyf-pwa-api-r19-static-verification-r36-retry-20260901T192716-2687397`.
- Selector: `R36_STATIC_ONLY|exact-package-semantic+prep-order+references+delegated-traversal+r36-catalogs+transaction+canonical-keys+real-toolchain+python36+forbidden-observation+r34-preservation`.
- Fixture digest: `R36_PACKAGE_ROOT:e94730ebfc64b8e99ec140545a914ef60a776130e985afd489fcace2ee7df779`.
- Evidence key: `23da733bfd918945d2b979457aa4e29e9f94a64117a4145dc97dbd8c05f4fe9c`.
- Static manifest root: `0c8b6291912bd494928a8316af8605352acfec366f054b74063a8e484f7d3827`.
- Static root-file SHA-256: `55d16c45dfe6a604823a70a33c1a8bc1bb4b9c10b540732769e856099829e92e`.
- Result SHA-256: `804976c49b0d9082a573e5750322fbc14e0ab2fb795cdcba4bf18b66b98c88da`.
- Details SHA-256: `8cd1d4468307f728a282d01cb9bbe987995b0765d4b2116553a901b65665f4a4`.
- Forbidden-observation SHA-256: `99783e0870acc99fa1b988e5b311343ccbd1876f868118d4439d800914613cb4`.

Real forbidden observations show the exact R36 unit loaded but inactive/dead, zero PID/restart/start timestamps, no exact R36 runtime process, empty runtime evidence/incidents, clean product, and preserved R34 predecessors. This scope makes no global claim about unrelated host processes.

## Prohibited-operation result and review boundary

No Gradle, runtime/unit start, stop, or restart, daemon reload, network, DB, RabbitMQ, Chromium, production access, deployment, canonical accepted-cache publication, hardlink, R35 mutation/cleanup, or unknown cleanup occurred.

Independent `sol_reviewer` must inspect the exact sealed builder, final package/bindings, preserved first-attempt root, and accepted sealed evidence root. Runtime remains separately gated and must not be started by the Reviewer.
