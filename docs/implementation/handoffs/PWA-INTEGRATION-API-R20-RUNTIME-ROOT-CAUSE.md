# PWA API R20 mount-probe root-cause matrix

Task: `PWA-INTEGRATION-API-RC`  
Instruction current date: `2026-08-30`  
Host journal/ledger clock preserved verbatim: `2026-08-31` (future-dated relative to the instruction date)  
Terminal gate: **`blocked_root_cause`; owner released; no R20 package and no Review request**

## Exact product and authority

- Product worktree: `/home/isp/wsps/cyf/.worktrees/pwa-integration-api-rc-r19`
- Product commit/tree: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / `bad28da5c05d6448d805f88c4e88457f0f657a5e`
- Product remained clean; no product-source byte changed.
- Durable authorization matrix: `docs/implementation/handoffs/PWA-INTEGRATION-API-R19-R19-RUNTIME-ROOT-CAUSE.md`
- Matrix SHA-256: `5e94024d5ab5fe448a4f088b7d88ebed921f7fb6683fe309e5722945588d2de7`

## Sealed R20 evidence

- Builder/evidence root: `/var/tmp/cyf-pwa-api-r19-static-verifier-r20-builder-5c75a1c98662458b`
- `SHA256SUMS.builder`: 32 payload rows
- Builder root SHA-256: `087e9fad1ad58950a639c9ff9870ca0d5cec88b2cd2554841a99b722d2ddb10a`
- Single probe identity: `cyf-pwa-api-r19-r20-mount-probe-cec391e3703e43cea40d4025eb7068c2.service`
- Dedicated runtime directory: `/run/cyf-pwa-api-r19-r20-mount-probe-cec391e3703e43cea40d4025eb7068c2`

## Root-cause matrix

| Attempt | Result | Root cause | Safety result |
|---|---|---|---|
| Probe-launch wrapper preparation | Rejected before `CreateProcess`; probe executions remained zero | The controller wrapper contained recursive directory removal. Command safety rejected the complete shell before `systemd-run`. | Attributed through the orchestrator. The same frozen probe identity remained unused and was retried once with allowlisted regular-file unlink plus exact `os.rmdir`; no topology or identity change. |
| The single actual R20 probe | `systemd-run` exit `1`; assertion `broad_writable_source_mounts:/home/isp/wsps/cyf` | The parser defined writable as `rw` in per-mount options **or** `rw` in superblock options. Mountinfo reported the exact root bind as per-mount `ro` over an underlying ext4 superblock `rw`, so the predicate falsely classified the exact read-only root as broadly writable. | This was the second consecutive post-reset failure. The probe was not repeated. No package/unit/review candidate was created. |

## Observed mount evidence and incomplete acceptance

The single real systemd 239 namespace produced:

```text
869 867 253:1 /home/isp/wsps/cyf /home/isp/wsps/cyf ro,relatime shared:466 master:1 - ext4 /dev/vda1 rw
870 869 253:1 /home/isp/wsps/cyf/docs/implementation /home/isp/wsps/cyf/docs/implementation rw,relatime shared:467 master:1 - ext4 /dev/vda1 rw
```

This proves that exact root and docs mount records existed and that their per-mount flags were respectively `ro` and `rw`. It does **not** establish the complete acceptance contract: the false-positive broad-writable assertion stopped execution before root/delegated source-write denial, delegated orchestrator denial, docs create/read/remove, and source-JDK inaccessibility probes. Therefore no probe PASS or topology promotion is claimed.

## Cleanup and preservation

- The probe self-unlinked its script before the failing assertion.
- `systemd-run --collect` auto-collected the transient unit.
- Final probe state: `LoadState=not-found`, `ActiveState=inactive`, `SubState=dead`, `MainPID=0`, `ControlPID=0`, `NRestarts=0`.
- The exact dedicated `/run` directory is absent; no probe unit or script remains.
- R18 builder root remains `5ab7f8c26679521c86d3211fcfa79eb327b75f047c87924c4638da1294649a17`; R18 runtime manifest remains `598da5d77b45c38fd7162c0778687497cb07d0260783736eb3e8d6287706b1fc`; R18 terminal remains `b9f92a4053f65208a892bb66813c5735e4d38172e46e8a6635f9e5b0aa67a282`.
- R19 builder root remains `f0dc56c072126202560cbfa94b20e2c06695140b7810bf22fb9bfb6624e0bfcf`.
- R17–R13 sealed roots and the 367-row R18 package manifest were reverified without mutation.
- Fixed free-space preflight `5368709120` passed before the probe.
- Gradle, successor runtime, product source writes, network, DB, RabbitMQ, Chromium, production, deployment, and daemon reload were not run.

## Terminal state and successor boundary

The runtime ledger is `blocked_root_cause`, `owner=null`, blocker `r20_probe_mount_writability_superblock_false_positive`, consecutive failures `2`. R20 must not enter Review.

Only a separately authorized fresh successor may continue. It must use a new unique probe identity and define effective writability with explicit per-mount `ro`/`rw` precedence; superblock flags may be consulted only when per-mount options contain neither. It must then execute the complete root/docs/longest-prefix/write-denial/docs-lifecycle/JDK-inaccessible contract once before any fresh non-overwriting package construction.
