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
  maintenance marker, canonical-minimum resources, a 30-minute cooldown, and
  has at most 2 attempts before circuit latch.
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

## Staged installation (not executed by this task)

Never execute repository scripts as root below `/home/isp`. First copy this
bundle to a root-owned staging directory, review it, then run:

```sh
/root/cyf-juyiting-health-stage/install.sh install
# Separately, only after acceptance and runtime authorization:
/root/cyf-juyiting-health-stage/install.sh install-cron
```

`install` copies code/config and explicitly initializes absent state. It does
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
