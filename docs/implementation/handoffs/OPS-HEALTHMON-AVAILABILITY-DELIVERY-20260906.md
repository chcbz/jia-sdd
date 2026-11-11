# Health monitor availability-first delivery — 2026-09-06

## Accepted source and installed policy

- R3 `b0a34302632bc2457f1ebd9875905f1b9dc7d40f` / tree `2e47228a440555a8de30492a381c90103d0a7807`, unique Raman ACCEPT 0/0/0, actual 61/61 offline tests, evidence cache `e9bb5ed64bc21b105fe4746b225ab8479fef3a74f3cb7682be89940b87fecc37`.
- Exact Knuth installed atomically at 19:43:17; monitor SHA `657deab366401a07d50ed1acb05fa3cc274b93b1b340ffade06db83a07735d79`. Config/state/cron preserved. Installer receipt `/tmp/ops-healthmon-availability-install-r3-receipt.json` SHA `1dbadc518b8ba6c4a2dfec3582837e79e5e3a28c684d5ce36237ef7d7e8351bd`.
- Three actual attempts per incident, third failed/interrupted attempt stops further automatic attempts and queues urgent clear Chinese notice; recovery-only fixed memory/disk soft-threshold overrides 0/0; 60-second cooldown; original identity/artifact/lock guards remain.

## Recovery and monitoring boundaries

- Exact API Owner Turing performed existing-JAR start1: 18:31:21–18:42:16 native0, later recurrence at19:00 with causeUNKNOWN. Start2 via own persistent systemd service: 19:25:35–19:38:55 native0; 19:38:57 canonical RUNNING/HEALTHUP, Java1724652/ticks3026648979, PPID1/own service cgroup. No start3 or foreign unit control by monitoring.
- Old shared incident I000017 naturally closed after three healthy observations. New I000018 must not inherit those two old manual attempts. Knuth correctly made zero old-counter imports. Monitor-lock-busy is a deferred observation, not restart failure.
- Monitoring resumed; exact operator receipt pending. Public/auth and local canonical status results differ: local canonical status has recurring 15-second diagnostic timeouts. Do not equate unknown canonical state with confirmed DOWN, and do not restart from UNKNOWN. Follow-up requested from existing API owner, no additional lifecycle/probe authorized.

## R4 bounded mail-path runtime defect and repair

- Observed durable policy/resolved/new-incident messages report helper_failed, not SMTP acceptance.
- Main's pure offline subprocess reproduction (no helper invocation, credentials or network): actual /usr/bin/python3 3.6.8 under fixed LC_ALL=C/LANG=C decodes Chinese argv using ascii/surrogateescape; EmailMessage.set_content(..., charset='utf-8') raises UnicodeEncodeError. Therefore a concrete local MIME failure is demonstrated; SMTP-side cause is not asserted.
- This host has C.utf8. The same offline Chinese subject/body MIME construction with fixed C.UTF-8 succeeds and filesystem encoding is utf-8.
- Exact Knuth is authorized only a bounded mail-child locale fix under ops/health/**. Keep canonical status/recovery locale C, fixed environment and exact command guard, -I, trusted helper/config/hash, existing outbox/retry/dedup. Add an actual isolated offline subprocess/MIME regression, not only FakeEffects. New candidate + exact tests + same independent Raman review before atomic install and one due-message flush. Do not reread credentials or blindly retry SMTP before the fix.

## R4 rollout and R5 second root-cause matrix

- R4 `cce74cfea59b082beda6ecf1b12a88873707c4df` / tree `fce428b3596a22e8e6fb6ae97948bd41b869bef3`, unique Raman ACCEPT 0/0/0, 62/62 including real isolated UTF-8 MIME regression. Installed 20:45:19, SHA `2dfa473927ed4a9c3344804e96eda1b469ac08cd69488f828ab8bda2921851d4`, no state/config/cron change; ordinary origin/codex/juyiting-health-monitor push succeeded.
- Own monitor-lock holder was actually waiting on authorized automatic canonical restart1 in incident I000019 from20:28:43. Never preempted. Stored terminal20:51:57 is failed_fresh_health_not_up, attempts1/inflightnull; no native rc/current UP inferred.
- Real 120-second diagnostic email: connect930ms, EHLO38ms, login169ms succeeded; send_message began but did not return before outer120s. No SMTP acceptance confirmed. Shared receipt `/tmp/ops-healthmon-availability-r4-mail-diagnostic-20260906.json` SHA `f2535af86715dfce3750ce6cf5d0c0ac246a214e045127fb91c37c744753c554`.
- Main independently reproduced a local serialization defect without network/helper/credentials: Python3.6.8 + C.UTF-8, EmailMessage with harmless ASCII From/To and Chinese body, BytesGenerator.flatten(CRLF). Existing short17-character subject serialized in1.01s. The exact direct-notice30-character subject `【聚义厅监控】“三次恢复失败即停止重试”策略已安装；持锁待查` did not finish within8s; only this own offline child was terminated. Thus send_message timeout must not be attributed to SMTP authentication/network solely from its stage name.
- Explicit bounded R5 authorization for the second distinct mail root cause (current ledger consecutive_failures=1, not a second consecutive failure): exact Knuth may only add a proven-safe UTF-8 subject byte bound, concise new subjects retaining urgent attempt count, send-time sanitization for old queued notices, and actual isolated Python3.6 serialization regressions including the exact old long subject and current short titles. Keep detailed Chinese body, original helper/hash/config, locale isolation, state/outbox/recovery budget. No new real SMTP invocation until new exact source/tests and same independent reviewer ACCEPT. Atomic code-only upgrade does not need state lock; no API/holder/unit control.


## Final delivered — 2026-09-06 21:47 Asia/Shanghai

- Final `7c1c2d92a40bf61de6f8c6fc2514f82aa22a023e` / tree `65950037ff00fa92d9b69463d19bfdf9b2004a95` accepted by the same independent Raman (0/0/0); actual 64/64 test evidence transparently reused for byte-identical product/test/installer blobs after documentation-only clarification. Evidence cache `4573a75c6362f79e07de4fe0d7e53098463276e9ce62b5d5f510da54686170e2`; full binding in `OPS-HEALTHMON-R5-EVIDENCE-BINDING-20260906.md`.
- Exact Knuth atomically installed final monitor at21:43:42, SHA `33cd70472019aa79b6b6538f8095e92558c106cf225c9fe0937e12549fd5f634`, preserving state/config/cron and maintenance=false. Receipt `/tmp/ops-healthmon-availability-r5-install-20260906.json`, SHA `46a39d3c9bfa48c13c1a4f3250fb29b01ab94845e797e2fa2f946f13c146cafa` independently checked by main.
- Actual short Chinese notification `【监控】告警策略已更新` accepted by SMTP at21:44:54 (native0); connect115ms/EHLO32ms/login142ms/send993ms. Receipt `/tmp/ops-healthmon-availability-r5-short-mail-20260906.json`, SHA `e0c778c78e198156cdbf59ad202cf04e0764cf427742d3f788e1c9bfce9088f5` independently checked. This proves SMTP acceptance, not inbox delivery. Existing configured recipient remains chcbz@live.com. No credential/config/helper rewrite.
- Ordinary fast-forward push succeeded to origin/codex/juyiting-health-monitor at final7c1c2d92; no force or develop rewrite.
- Main final read-only stored snapshot: checks observed21:47:11–12, overall_healthy=true; canonical local API UP/PID1788116, public/auth expected empty401, web200, MySQL/Redis reachable, Agent active. Incident=null, attempts0/in_flight=null, maintenance=false, outbox_count0. These are actual monitor observations, not business/voice-release acceptance or a claim that the earlier recovery attempts all succeeded. Existing history remains in the receipts above.
- Operational next action: cron continues its minute-level checks with resource-warning-only recovery and three-attempt limit; persistent failure/unknown exhausted circuit alerts use short safe UTF-8 Chinese subjects and detailed bodies, with durable mail retry. No further source or runtime work required for this requested policy/mail change. API/voice feature-release tasks remain independent.
