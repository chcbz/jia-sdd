# OD00 prerequisites — accepted for development; release gates pending

User authorized continuous OD00–OD11 implementation on 2026-09-09 and directed reuse of `isp-install`. P3 remains deferred. Root and isolated API/Web/client worktrees use `codex/agent-output-delivery`; original implementation checkouts are preserved.

| Item | Evidence on 2026-09-09 | Disposition / remaining gate |
| --- | --- | --- |
| API/Web/client bases | `492adc7e` / `77666e8` / `a100a50` | isolated worktrees ready |
| Workstation | Debian 13 Linux aarch64; 7.8 GiB RAM; ~2.7 GiB disk free after provisioning; `/tmp` tmpfs constrained | user-space tools only; large downloads kept off `/tmp` |
| Java / Gradle | official checksum-verified Temurin 21.0.10+7; Gradle wrapper 9.3.1 and local settings plugin compiled; legacy image dependencies require repository setup | targeted agent/chat build and MySQL test PASS with reviewed local dependency deviations; see implementation-decisions.md for substitutions and private-repository TLS gate |
| Database | isolated MySQL 8.0.45 ARM, matching isp-install version; `utf8mb4 / utf8mb4_0900_ai_ci`; InnoDB rollback and `BINARY` case-sensitive ownership predicates passed | engine PASS; real Agent/Chat production-component commit/rollback slice PASS (1 test, 0 failures/errors/skips); deployed topology remains unverified |
| Object storage | MinIO `RELEASE.2025-09-07T16-13-09Z`; private bucket put/head/get/delete passed, 34,816 bytes hash matched; anonymous GET returned 403 | local adapter dependency PASS; production backup/restore and credentials pending release gate |
| Scanner | ClamAV 1.4.3; official daily 28118/main 63/bytecode 339 databases downloaded and validated; TCP INSTREAM clean `OK`, EICAR `FOUND`, PING passed; oversized stream rejected with `INSTREAM size limit exceeded. ERROR`; 60 MiB stream limit, 2 worker threads | real local scanner PASS; application unavailable-scanner retry/fail-closed test belongs to OD02 |
| Aggregate transaction wiring | starter includes agent + chat; chat-service depends on agent-service; default Druid config supplies one datasource, dynamic config supplies one transaction manager; task mutation wrapper uses REQUIRED | production-component MyBatis/TM slice passed on one physical datasource; actual deployed starter/routing/AOP remain release gates |
| Authenticated run sources | `JuyitingAgentRelayService`, `HallActionDispatcher`, `AgentWebSocketHandler`, task command pipeline located | source-level insertion points confirmed; OD01 must prove trusted conversation/task dispatch and strict owner checks |
| Gateway | isp-install nginx template sets `client_max_body_size 100m`; sample vhosts use 60s proxy timeout | template is not effective deployment evidence; output route body overhead + 10-minute upload timeout must be verified for OD06 |
| Node / npm | Node 22.22.0, npm 11.17.0; existing web dependencies available | ready for targeted frontend/client verification |
| Remote / privilege | no established SSH key/agent/build host; noninteractive sudo unavailable | no production mutation or privileged installation performed |

## Reproduction and provenance

Tool root: `/home/chc/.local/share/cyf-output-tools` (outside Git). Services listen only on loopback: MySQL `13306`, MinIO API `19000`/console `19001`, ClamAV `13310`. Random local credentials are mode-0600 files outside Git; do not print them. These user-space development processes are not production service management.

- `python3 /home/chc/.local/share/cyf-output-tools/od00-services-probe.py`: creates/drops a uniquely named disposable database and bucket; checks rollback, exact ownership predicates, object hash and anonymous denial. It does not prove Spring transaction wiring.
- `python3 /home/chc/.local/share/cyf-output-tools/od00-clamav-probe.py`: actual clamd PING/INSTREAM normal and EICAR checks. It does not prove application scan-retry behavior.
- The verified task-owned JDK archive was removed after installation and checksum recheck to recover ~196 MiB; the installed runtime and checksum record remain.
- JDK official SHA-256: `357fee29fb0d5c079f6730db98b28942df13a6eed426f6c61cd4ad703ab27b9a`.
- MySQL official CDN ARM archive local SHA-256: `2bbbdd107bc02bd6a135d5140b6a790de5ed4d4ff5389803600c26c79e208d2a` (recorded provenance, not an independently fetched checksum). Selected server/client/share/private-library contents extracted; only the task-owned archive was then removed to recover disk.
- MySQL needs `libaio.so.1`; a task-local link targets installed ARM64 `libaio.so.1t64`. MySQL version, initialization, startup, and SQL probes passed with that local library path.
- ClamAV binaries were extracted from Debian 13 ARM packages using unprivileged `apt-get download` + `dpkg-deb -x`; no system packages were changed. Freshclam DNS TXT lookup failed but official HTTPS fallback and all three database validations succeeded.
- MinIO official binary checksum was verified before execution. Probe payload SHA-256: `6ec3f1e128eee97b9cda0b1579b03d18fc2ca777cf29e395b5215fbb554c27b9`.
- Existing `AgentTaskMutationTransactionMySqlTest` requires MySQL **8.0.21** and has not been represented as passing on 8.0.45. New OD verification must state the version it actually runs against.
- DeepSeek Flash test-runner startup failed with provider `auth_unavailable`; available Terra helper performed toolchain preparation. Independent review remains required.

No existing user cache, source modification, stash, or unrelated temporary file was removed. No business migration or production endpoint was executed. OD00 is accepted for development and unlocks OD01, with independent source review APPROVE and actual test execution. This is not an unconditional release PASS; pending production/runtime checks remain assigned in downstream-gates.md. API verification commit: `f418e3f5bf7afcdbddf9c1ecec1b293f657c977c`. The archived JUnit report is transaction-test-result.xml (SHA-256 `ba6397dd5e5bd680ae43356c420901271defd4383c39dcb2c49b10e6589cb554`).
