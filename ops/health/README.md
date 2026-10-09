# CYF Juyi Hall bounded health monitor

`cyf-juyiting-health.py` is a Python 3.6 stdlib cron monitor. It checks the
public Juyi Hall HTML entry, the unauthenticated public API/auth boundary (including
the fixed endpoint's production empty-401 contract), the canonical local API status,
MySQL/Redis reachability, and the Codex Agent unit.
Only the API can be recovered, through the exact accepted canonical command.

It does **not** prove authenticated map/roster/business behavior, SMTP inbox
delivery, or whole-host availability. Whole-host failure needs an external
monitor. Redis `-NOAUTH`/`-NOPERM` proves reachability only.

## Fixed safety behavior

- `/usr/local/sbin/cyf-api-kit` must be root-owned 0755 with SHA-256
  `56537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5`.
- State is root-only, atomic 0600 under `/var/lib/cyf-juyiting-health`, protected
  by a nonblocking singleton flock held through the full synchronous canonical
  recovery (cold start is normally 9-13 minutes and can wait up to 1200s).
- Recovery needs 3 consecutive local API failures, healthy MySQL/Redis, no
  maintenance marker and a 60-second cooldown. Memory/disk observations are
  warnings rather than blockers. Recovery alone invokes the trusted canonical with
  fixed `CYF_API_MIN_MEMORY_AVAILABLE_BYTES=0` and
  `CYF_API_MIN_DISK_AVAILABLE_BYTES=0`; status and other commands do not receive
  those overrides or inherited environment values.
- At most 3 actual attempts are persisted per incident. The count/in-flight fence is
  durable immediately before invocation, including an invocation exception. The
  third failed attempt persists a circuit latch and a prioritized single Chinese
  `恢复失败，已停止自动重试（3/3）` alert; no fourth attempt occurs. A third-attempt
  success does not send that alert or latch the circuit.
- STOPPED may start. NOT_READY may restart only after 25 minutes when canonical
  output explicitly includes matching artifact, owned listener, PID/age and
  `RUNTIME_IDENTITY=cyf-api(987:1000)`. The canonical rc4 no-listener branch
  lacks a complete runtime-identity assertion and is deliberately alert-only.
- Three trusted API-UP observations reset the circuit. `--reset-circuit` is an
  explicit alternative. Public web/API, dependencies, and Agent are alert-only.
- Incident/recovery mail is queued durably. The current recovery-attempt notice is
  tried ahead of old mail, then canonical status is read again: restart requires the
  same trusted PID to remain MATCH/LISTENING/NOT_READY and at least 25 minutes old.
  Healthy/PID-changed/identity-changed results cancel recovery without consuming an
  attempt. Mail failure remains queued with bounded retry/dedup.
- New incident, recovery, resolution, reminder, digest and test mail is concise
  Chinese with the action first and bounded metadata after it. The final exhausted
  alert includes Asia/Shanghai time, impact, confirmed classifications versus unknown
  cause, attempt/action/return code/fresh health, manual next action and the resource
  override explanation. Recovery-result time is captured after the lifecycle call and
  fresh health check. Every stored probe has its own observation time; the snapshot
  timestamp is the window start. After attempt mail, maintenance, MySQL, Redis and
  canonical identity are all rechecked before the attempt is counted or invoked.
  A persisted interrupted third attempt becomes an explicit UNKNOWN terminal latch
  with one durable urgent notice and no fourth invocation. Interrupted attempts one
  or two retain their fence until three trusted UP checks, which then clear the old
  incident budget without guessing the missing native result. A later reminder or
  priority insertion cannot evict an exhausted alert from a full outbox. The fixed
  mail-helper child alone uses `LC_ALL=C.UTF-8` and `LANG=C.UTF-8` so sanitized Chinese
  argv can be encoded by Python 3.6; canonical status/recovery and other children stay
  on the fixed `C` locale. Mail contains no raw logs, secrets or inbox-delivery claim.
- `/usr/bin/python3` symlinks are accepted only through a root-owned, non-writable
  lstat chain ending at a trusted executable. Credential file content is never read.
- Cron suppresses ordinary output mail. Exceptional `fail_closed` guards alone write
  a fixed sanitized event through root-trusted `/usr/bin/logger`; no response body,
  argv, environment or credential is logged.

## CLI

```text
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --init
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --check-once
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --status
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --pause
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --resume
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --reset-circuit
/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --notify-test
```

`--status` reads the stored snapshot only: no repair, probe, mail retry, or
recovery. `--notify-test` is an explicit real mail action and must not be used by
automated tests.

Maintenance pauses only actions selected by a later tick; it never signals or
cancels an already-running canonical recovery. If `--pause` returns lock-busy
while recovery is in flight, a root operator may create the marker for the next
tick without touching the monitor/canonical processes:

```sh
/usr/bin/install -o root -g root -m 0600 /dev/null /var/lib/cyf-juyiting-health/maintenance
```

The next normal tick validates that marker and reports checks while suppressing
recovery. Remove it with `--resume` after the singleton lock is available.

Manual and automatic recovery share one three-attempt incident budget. There is no
general manual-import CLI. A separately authorized exact monitor Owner may, while
maintenance is active and under the monitor lock, reconcile a trusted manual receipt
monotonically into the existing schema-v1 recovery fields as specified in
`CONTRACT.md`. Installation, reconciliation, mail execution and resume each require
their own runtime authorization.

## Staged installation (not executed by this task)

Never execute repository scripts as root below `/home/isp`. First copy this
bundle to a root-owned staging directory, review it, then run:

```sh
/root/cyf-juyiting-health-stage/install.sh install
# Separately, only after acceptance and runtime authorization:
/root/cyf-juyiting-health-stage/install.sh install-cron
```

`install` atomically replaces the monitor from a fully written, fsynced same-directory
temporary file, so an active cron reader sees either the old or new complete bytes.
It copies config and explicitly initializes absent state. It does
not install cron, probe services, send mail, or recover API. The installer validates
the complete root-owned/non-writable staging parent chain and every payload.
`install-cron` requires the installed monitor's owner/mode/link count and SHA-256 to
match the reviewed candidate embedded in the installer, then byte-verifies the cron
copy. It does not restart `crond` or run an immediate check. Existing config/state
are never overwritten or repaired.

## Tests

```sh
/usr/bin/python3 -m unittest discover -s ops/health/tests -p 'test_*.py' -v
/usr/bin/python3 -m py_compile ops/health/cyf-juyiting-health.py
/bin/sh -n ops/health/install.sh
```

All behavior tests inject side effects; they do not access network, mail,
canonical lifecycle, systemd, or production state.
