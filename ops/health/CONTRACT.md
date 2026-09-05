# OPS-JUYITING-HEALTHMON frozen implementation contract

Frozen on 2026-09-05 before product source edits. This file is implementation input,
not deployment authorization.

## Event and API catalog

Only these read-only observations exist:

1. `GET https://kit.chaoyoufan.cn/juyiting`: HTTP 200, `text/html`, configured
   bounded HTML marker present.
2. `GET https://api.chaoyoufan.cn/agent/map`: either the production contract's exact
   HTTP 401 with empty Content-Type and zero-byte body, or HTTP 401/403 with a JSON
   authentication-denial object. This proves only that the fixed public API/auth
   boundary responds; HTML 403/502 and HTML 200 SPA responses fail, and authenticated
   map or roster semantics are not proved.
3. `/usr/local/sbin/cyf-api-kit status`: exact canonical status authority. Exit 0 is
   trusted UP only with the required identity/artifact/listener fields; exit 3 is
   stopped only with an unowned-port-free stopped result; exit 4 can be recovery-safe
   only when runtime identity, artifact, listener ownership, PID and age are all
   explicit. Exit 1 is busy/error and exit 5 is unsafe. Unknown/truncated output is
   unsafe.
4. Read-only TCP checks: MySQL handshake on 127.0.0.1:3306; Redis unauthenticated
   `PING` on 127.0.0.1:6379 where `+PONG`, `-NOAUTH`, or `-NOPERM` proves reachability
   only.
5. `/usr/bin/systemctl is-active codex-ws-agent.service`: alert-only.

Only these mutations exist:

- Atomic monitor state/maintenance updates below `/var/lib/cyf-juyiting-health`.
- Exact API recovery command `/usr/local/sbin/cyf-api-kit start` for trusted STOPPED,
  or `restart` for the fully trusted LISTENING/NOT_READY branch after 25 minutes.
- Exact mail command `/usr/bin/python3 -I /root/.local/bin/cyf-task-email SUBJECT BODY`.
- Explicit CLI administration: `--init`, `--pause`, `--resume`, `--reset-circuit`, and
  `--notify-test`.

No URL, executable, argv, shell fragment, credential, token, PID, signal, build,
deploy, pull, DML, Gradle, business write, or Agent recovery is configurable.

## Lock order and singleton boundary

1. Validate fixed config path, ownership, mode, parent chain, bounded JSON and schema.
2. Validate fixed state directory and lock inode.
3. Acquire the monitor lock with nonblocking `flock`.
4. Validate/read state; corrupt, missing (except explicit `--init`), insecure, or
   unknown-schema state fails closed.
5. Validate maintenance marker.
6. Run bounded read-only probes.
7. Persist state atomically before any recovery command.
8. Persist the selected recovery-attempt notice, deliver that current notice ahead
   of older queued mail, then read canonical status again. Restart proceeds only when
   the same trusted PID is still MATCH/LISTENING/NOT_READY and at least 1500 seconds
   old; a healthy result, PID change, or identity change cancels the command.
9. Persist actual attempt count, timestamp and in-flight fence immediately before the
   canonical lifecycle command. Keep the same monitor flock for the complete wait;
   the monitor does not impose a timeout or signal that subprocess.
10. Run a fresh canonical status and persist the result. Every notice, including
    resource-deferred notices, is durable before it becomes delivery-eligible.

Cron overlap therefore defers immediately and cannot overlap a cold start that may
last 9-13 minutes (canonical maximum 1200 seconds).

## State transaction boundaries

State is a root-owned 0600 regular file, one link, atomically replaced from a 0600
same-directory temporary file and followed by file and directory `fsync`. Attempt and
`last_attempt_at` are durable before lifecycle execution. An interrupted `in_flight`
attempt consumes its attempt slot and is fenced by cooldown/max-attempt controls.
Recovery success requires both command exit 0 and a fresh fully trusted canonical UP
status. A healthy observation never depends on lifecycle command exit alone.

Default absence is accepted only by explicit `--init` (or an installer action that
explicitly calls it). `--status` is read-only and never creates, repairs, retries mail,
or probes services.

## Recovery state machine

- Only local canonical API STOPPED or fully trusted LISTENING/NOT_READY failures count
  toward API auto-recovery eligibility.
- Three consecutive API failures are required.
- STOPPED -> `start`.
- NOT_READY -> `restart` only with `ARTIFACT_ATTESTATION=MATCH`, exact PID,
  `RUNTIME_IDENTITY=cyf-api(987:1000)`, `PORT_10018=LISTENING_BY_PID`, and trusted
  elapsed age >=1500 seconds. The rc4 no-listener branch is intentionally alert-only.
- MySQL and Redis must be reachable; maintenance must be absent; resource preflight
  must meet at least 1 GiB MemAvailable and 5 GiB filesystem availability.
- Cooldown is >=1800 seconds. Maximum is two persisted attempts per incident, then a
  circuit latch.
- Three observed fully trusted API-UP checks reset the attempt/circuit fence. Explicit
  `--reset-circuit` also resets it without probing or recovery.
- Public web, public API/auth, dependencies, and Agent service are alert-only. An
  external-only failure can never restart a locally healthy API.
- rc1, rc5, unknown identity, malformed output, missing identity, foreign listener,
  and insecure/corrupt files are fail-closed and never recover.

## Sensitive-payload allowlist

Durable snapshots, stdout and mail may contain only: UTC timestamps, component names,
boolean health, bounded classification labels, HTTP status/content type, trusted PID,
trusted elapsed seconds, recovery action/attempt/result, incident ID, queue counts,
and fixed operational guidance. They must never contain response bodies, canonical
stdout/stderr/argv rows, process command lines, environment values, credentials,
tokens, email-env contents, passwords, cookies, authorization headers, or arbitrary
exception text. Error details are reduced to fixed exception class labels.

The durable outbox is bounded and deduplicated. Delivery failure remains pending with
bounded retry backoff. The current recovery-attempt notice is prioritized before the
long canonical wait. When full, pending events are coalesced into a bounded digest
rather than silently dropped. SMTP acceptance is reported only as helper acceptance,
never inbox delivery. `/usr/bin/python3` may be a symlink only when every lstat hop and
parent is root-trusted and the final target is a safe executable. Exceptional
`fail_closed` guards emit only a fixed sanitized message through a root-trusted
`/usr/bin/logger`; normal ticks are not sent to syslog.

## Acceptance-to-test mapping

| Acceptance | Test coverage |
| --- | --- |
| three-failure threshold and exact start | `test_stopped_threshold_starts_on_third_failure` |
| rc1 busy and rc5/foreign fail closed | `test_rc1_busy_never_recovers`, `test_rc5_foreign_identity_never_recovers` |
| external-only failure no restart | `test_external_only_failure_never_recovers_healthy_api` |
| maintenance pause | `test_maintenance_reports_but_pauses_recovery` |
| corrupt/missing/insecure state/config | `StateStoreSecurityTests`, `ConfigSecurityTests` |
| cooldown and interrupted fencing | `test_cooldown_blocks_second_attempt`, `test_interrupted_attempt_is_fenced` |
| max two/circuit and three-UP reset | `test_second_failure_latches_circuit`, `test_three_healthy_checks_reset_circuit` |
| dependency gate | `test_dependency_down_blocks_recovery` |
| startup grace/full rc4 identity | `test_not_ready_requires_grace_and_full_identity`, `test_rc4_without_runtime_identity_is_alert_only` |
| command exit is not success | `test_exit_zero_without_fresh_up_is_failure` |
| mail retry/dedup/bounds/current-attempt priority and durable defer | `MailQueueTests`, `test_current_attempt_mail_is_durable_and_prioritized`, `test_resource_deferred_notice_persisted_before_delivery` |
| web marker, empty 401, JSON denial and HTML rejection | `ProbeContractTests` |
| safe Python symlink chain | `TrustedExecutableTests` |
| post-mail same-PID restart fencing | `test_post_mail_restart_revalidation_*` |
| exceptional guard syslog only | `test_guard_logging_uses_fixed_sanitized_syslog_command`, `test_cron_syntax_contract` |
| installer staging/activation trust | `test_installer_trust_and_activation_contract` |
| maintenance directory durability | `test_pause_resume_marker_and_directory_fsync` |
| fixed config/command/security and cron syntax | `ConfigSecurityTests`, `StaticContractTests` |
| no real side effects | all monitor tests inject `FakeEffects`; static tests reject shell/configurable commands |
