# HOST R3 bounded remediation — 2026-09-05

R2 independent reviewer 01a07199-aea5-7242-ab75-9d5e383d0e9b rejected dac3d443eb5366cf7f16c4c76f41067cb524af50 / tree a0e30e42c4c62ba493d58f380c74af9de95c8cac with P0/P1/P2=0/3/0. Second consecutive source failure has been recorded with blocked_root_cause; no offline selector or deployment has run.

| Finding/root cause | Bounded correction | Required proof |
| --- | --- | --- |
| Python startup remains ambient despite privileged shell: entrypoints/helper/common.sh call python3 without isolated mode | Absolute /usr/bin/python3 -I -B consistently across relevant release entrypoints, helper, direct common dependency and canonical Python paths; preserve Python 3.6 compatibility | Hostile PYTHONPATH/PYTHONHOME and CWD module fixtures exercise actual validation paths, not --help only; payload never executes |
| curl config and proxy can redirect authenticated audio/health calls | curl -q as first argument, explicit --noproxy '*' for loopback; fixed trusted tool resolution/environment in activation and canonical health | Real curl in owned bounded loopback fixture proves proxy/config remap is ignored, not fake curl alone; no production/external targets, credentials or audio |
| Three independent transaction handlers lack symmetric fault matrix | Complete rollback and activation partial-stop, COMMITTED and terminal receipt faults, after-replace, before-chmod and file-fsync coverage | Every applicable handler/fault pair checks truthful terminal record and actual selected/runtime state; explain genuinely inapplicable cells rather than silently omit |

## Ownership and execution contract
Original critical_writer Shannon3 (01a07121-a86e-7e13-bd4e-611c33076550) owns only existing HOST-adapt paths in .worktrees/jvc-oai-host-adapt-r1 plus bounded common.sh isolation. Web's six owned paths remain untouched. Direct apply_patch; no nested heredoc replacement generators. Static Bash/explicit Python AST/pin/scope checks only until clean commit and fresh independent source/safety admission.

If a real curl regression fixture is required, author test source using exclusive private root0700 directory and owned unprivileged server bound only to 127.0.0.1 ephemeral port. No external requests, no installed runtime execution, no service/lock/DB/namespace actions; fixture lifetime/cleanup exact-owned only. This document authorizes source design, NOT execution: reviewer must explicitly admit the actual selector and fixture safety first.

Preserve already-closed real STT/TTS contract, canonical FD proof, exclusive shm fixture, Nginx route closure, and post-health receipt truthfulness. Reuse accepted API/Web source, tests and artifacts. Old131 remains not passed. No production enablement, key access, builds or repeated accepted tests.

## Shared dependency addendum from independent Web review (21:47 CST)
Web reviewer identified common.sh health curl777–805 inherits proxy and CA overrides; HOST is sole common.sh owner. Extend bounded common hardening to curl -q first argument, direct --noproxy '*', and trusted system CA defaults rather than inherited CURL_CA_BUNDLE/SSL_CERT_FILE/SSL_CERT_DIR or proxy variables. Web entrypoint will separately sanitize environment and pin common.sh bytes in guard digest. No Web six-path edits by HOST. Explicit tests/static contract and fresh review must include this dependency; no production/network execution in source phase.
