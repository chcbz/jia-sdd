# PWA API R19 R18 runtime root-cause and R19 remediation matrix — 2026-08-30

Task: `PWA-INTEGRATION-API-RC`  
Successor writer: `01a0539e-38f8-71e1-9e6a-a87130ffe912` / `critical_worker` / `writer`  
Exact product: commit `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`, tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`  
Product source policy: **exact clean; no product-source edits**

## Sealed R18 terminal

- Evidence directory: `/var/tmp/cyf-pwa-api-r19-static-verifier-r18-evidence`.
- Runtime manifest root line: `598da5d77b45c38fd7162c0778687497cb07d0260783736eb3e8d6287706b1fc  SHA256SUMS.runtime`.
- Terminal marker SHA-256: `b9f92a4053f65208a892bb66813c5735e4d38172e46e8a6635f9e5b0aa67a282`.
- Exact result: `TERMINAL=FAIL`, `SERVICE_RESULT=exit-code`, `EXIT_STATUS=28`, `MAIN_DETAIL=mount_contract_failed`, cgroup quiescent, and DB/Rabbit/Chromium/production all `NOT_RUN`/`NOT_ACCESSED`.
- The empty sealed `mount-contract.runtime.txt` and the R18 helper's first assertion identify `exact_root_mount_missing`.
- R18 is permanently frozen. R19 must not restart, stop, kill, rerun, edit, relink, chmod/chown, delete, or reuse any R18 unit/package/evidence path.

## Root-cause / remediation matrix

| Finding | Exact cause | Safety result | Frozen R19 remediation |
| --- | --- | --- | --- |
| R18 failed before Gradle at mount contract exit 28 | R18 combined `ProtectHome=read-only` with `ReadOnlyPaths=/home/isp/wsps/cyf` and a nested `ReadWritePaths=/home/isp/wsps/cyf/docs/implementation`. On host systemd `239-82.0.4.3.al8.5`, the resulting namespace did not expose an exact `/home/isp/wsps/cyf` mount in `/proc/self/mountinfo`; the static fault suite simulated files but never executed this exact namespace contract in real systemd 239. | Fail closed. No Gradle/network/DB/Rabbit/Chromium/production/deploy action occurred. Sealer produced an exact failure terminal only after cgroup quiescence. | Remove `ProtectHome=read-only` from the successor topology. Before package construction, run only uniquely named mount-only systemd 239 probe units that self-clean and record real `/proc/self/mountinfo`. Select an explicit exact bind topology only from observed PASS evidence. |
| Root/doc longest-prefix contract was asserted but not namespace-proven | Static parsing proved the helper logic, not systemd 239's actual mount generation and remount ordering. | No unsafe fallback occurred; wrapper stopped at the first mount assertion. | Require real-namespace proof of exact root RO and exact docs RW mounts, with longest-prefix root for the orchestrator and product worktree and exact docs exception for docs. |
| Permission behavior was not reached in R18 | The namespace-shape assertion failed before delegated write probes. | No source write was attempted by delegated Gradle UID. | Probe and statically bind UID/GID `61019:61019` denial for source root and orchestrator writes, docs create/read/remove success, absence of any broad writable source mount, and `SOURCE_JDK=/home/isp/apps/jdk21` inaccessibility. |
| R18 static package otherwise passed inherited construction/publication gates | R18's static verifier passed fresh file-backed generation, AST/dataflow negatives, O_EXCL copies/publication, package paths, fault injection, root-owned immutable metadata, R17–R13 preservation, and fixed 5 GiB gate. | Those contracts remain useful but R18's runtime result is permanently failed and non-promotable. | Fresh non-overwriting R19 package must rerun every inherited R18 static contract and add real systemd-239 mount-probe evidence plus static topology assertions. No R18 file may be copied as a mutable/final R19 output; R19 sources are fresh file-backed complete sources. |

## Frozen catalogs and boundaries before R19 construction

- Product API/event catalog: unchanged; no endpoint, event, schema, identity, ACL, transaction, migration, or payload change.
- Verifier control events: `PROBE_CREATED`, `PROBE_PASS|PROBE_FAIL`, `PROBE_CLEANED`, `ACTIVATION_PASS|ACTIVATION_REJECT`, `NEGATIVE_HARDLINK_TEST_PASS`, `POST_RENAME_DATAFLOW_GATE_PASS`, `FAULT_INJECTION_PASS`, `CREATED_R19`.
- Lock order: `systemd preflight -> exact mount proof -> package/JDK proof -> official orchestrator -> /tmp/cyf-gradle.lock -> delegated Gradle 61019:61019 -> evidence-cache lock -> ExecStopPost after cgroup quiescence`.
- Transaction/publication boundary: all R19 content is built under fresh builder-owned staging; complete destination digests are frozen before first `RENAME_NOREPLACE`; post-rename verification reads final destinations only; activation is durable while unit is absent; the `0444 root:root` unit is the sole final non-overwriting commit point and is published last. The property is crash-safe fail-closed, not crash-atomic.
- Sensitive evidence allowlist: hashes, exact paths, modes/owners, mount IDs/options/source/root, UID/GID, test names/counts, placeholder credentials, bounded resource telemetry, PID/cgroup identity, and donor metadata. Deny environment dumps, real credentials/tokens/codes/verifiers/passwords, and production payloads.

## R19 acceptance-to-test freeze

1. Verify exact product commit/tree and clean status before probe, before publication, after publication, and before handoff.
2. Verify R18 terminal/root line and immutable before/after preservation without any R18 process or path mutation.
3. Run uniquely named mount-only systemd 239 probe(s); persist full real `/proc/self/mountinfo`, selected longest-prefix records, write-probe results, source-JDK inaccessibility, unit properties, journal, and cleanup proof.
4. Require selected topology to prove: exact root RO; exact docs RW; orchestrator and product worktree longest-match root; delegated UID/GID cannot write source/orchestrator; docs create/read/remove succeeds; no broad writable source mount; source JDK inaccessible.
5. Freshly rerun R18 A01–A20 plus the new systemd-239 namespace gates, including R17–R13 preservation, fresh complete file-backed generator/analyzer/helper sources, Python 3.6 in-memory compile before O_EXCL publication, actual-source zero violations, eight direct/alias read/open/stat/hash negatives, nested target rebind/clear, complete pre-rename digest freeze, destination-only post-rename verification, hardlink/copy negatives, independent donor copies, JDK 677/676 identities, UID/GID 61019, ONLINE=9/OFFLINE_AUTHORITATIVE=8 catalogs, exact package paths, activation fault suite, publication-last, and `5368709120` bytes minimum free-space constant.
6. Static verification only: no Gradle, network, DB, RabbitMQ, Chromium, production access, deployment, daemon reload for the successor, or R19 runtime start.
7. Seal builder evidence and publish a clean R19 handoff; transition ledger to `review` with `owner=null`. Independent Review remains mandatory; this writer cannot self-accept.

## Authorized bounded execution

The only runtime execution in this remediation is the user-authorized, mount-only, uniquely named systemd 239 compatibility probe. It must not invoke Gradle/network/DB/Rabbit/Chromium/production paths, must not operate any other unit/process, and must remove only its own transient unit state and probe-owned temporary files after evidence capture. The R19 successor unit must remain inactive and must not be started.

## R19 probe attempt and mandatory stop

The single probe unit `cyf-pwa-api-r19-r19-mount-probe-65fc0d62c33e411db1aec7cb638fbe72.service` was created with `systemd-run --wait --collect` and only the frozen mount-only properties. It exited before reading `/proc/self/mountinfo`: `ProtectSystem=strict` made `/run` read-only, while the probe attempted to unlink its own `/run/...py` executable as its first self-cleanup operation. The journal records `OSError: [Errno 30] Read-only file system`. Therefore the candidate bind topology itself is **not evaluated** and no mount-contract PASS may be claimed.

The transient unit was automatically collected (`LoadState=not-found`, `MainPID=0`, `ControlPID=0`). The exact failed-probe runtime script was then removed by the owner as bounded cleanup of that probe's own path only; no other unit or process was operated. No R19 package/final path/runtime was created or started, and no Gradle/network/DB/Rabbit/Chromium/production/deploy action occurred.

This is the second consecutive R19 successor failure after the attributed invalid control-gate transition. The task must enter `blocked_root_cause`, release the owner, and stop. A future separately authorized non-overwriting successor may use a fresh unique probe whose executable lives in a dedicated probe-owned `/run` directory granted by an exact `ReadWritePaths=` exception, allowing in-namespace self-unlink without broadening source writability. It must not reuse this failed unit/script identity and must still prove the complete exact root/docs topology before package construction.
