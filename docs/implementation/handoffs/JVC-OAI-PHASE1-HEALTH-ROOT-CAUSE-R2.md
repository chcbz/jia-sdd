# Phase1 stopped root-cause matrix R2 — 2026-09-06

Controller task JVC-OAI-RUNTIME-PHASE1 stopped at blocked_root_cause, consecutive_failures=2. Actual evidence shared by sole runtime owner `/tmp/jvc-oai-runtime-phase1-diagnostic-r1-20260906.t8kPbu` (all eight named files allowed, no sibling/private evidence). result.txt SHAb854102ae2e50ee918ceaac21fcafb549e19f2bc641b8b97396301a6bf8e246e; root-cause-matrix.txt SHAe8cca88a79c08ec79621236bff8490e4b12b3e470bae3d49abbba37a0740004c.

| Observation | Actual meaning | Missing | Proposed bounded remediation (NOT GO) |
|---|---|---|---|
| Explicit status native1, zero allowlisted keys, raw discarded | Invocation failed; historic root cause UNKNOWN_NO_RAW | Locks or downstream branch, not process failure proof | Preserve result; do not retry or demand old raw recovery |
| 12:22:40 direct curl native28 after5s, HTTP000 | Health not proven; exactAPI PID1222845/startticks3021456883 stable, owns0.0.0.0:10018 | Host pressure vs application stall/dependency health latency | One passive resource/API observation, no health/status retries |
| flags OFF, exactAPI exe/JAR/account/runtime match | Current voice disabled | No audio activation claim | Reuse valid current evidence, recheck only at eventual change boundary |
| rescue SHA246520/Boot/chain/runtime PASS | Artifact/record structural checks passed | Healthy operational rescue not yet accepted | Do not label operational-rescue trust complete without health |
| 19Nginx tuples loopback, WS Upgrade valid | Static consumer semantics compatible | Config0775 isp:isp mutable trust; no live WS probe by scope | Separate content/permissions/custody decision; no foreign WS /proc |

## Independent review scope

Godel read-only small shared evidence + acceptedsource only; no live/lock/log/proc/test/build/config reads, no source repairs. Assess and freeze minimum soleOwner diagnostic allowance:
- One host aggregate `/proc/{loadavg,meminfo,pressure/{cpu,memory,io}}` read, no per-foreign-process data. One exactAPI process stat/status/wchan/io/task-state summary with PID/ticks stability; two bounded samples only if needed for rates, fixed short interval. No stack dumps/attach/jcmd/jstack/signals or foreign processes.
- Exact API own stdout/stderr log FILE DISCOVERY via only its `/proc/<pid>/fd/{1,2}` readlink if necessary, no other FDs; only known trusted canonical `/var/log/cyf-api/` regular log path. Read bounded tail in memory and emit strict category/count/timestamp only (OOM/GC/DB/Rabbit/HTTP pool/timeouts/shutdown), no raw lines, prompts, credentials, request bodies, identity data or opaque exception strings. No journal scan/other logs. If destination not canonical/no-follow-safe, stop log inspection and report NOT_PROVEN.
- Source review health contributors from accepted/source-version caveat; current live source UNKNOWN so no automatic source attribution. Passive observations cannot on their own prove responseUP.
- No API/Nginx mutations, status/health retry, locks/control, DB/network or heavy build.
- Determine whether Nginx mutable metadata is an install blocker vs external trusted snapshot custody condition, and whether WS static tuple is sufficient for phase1 loopback compatibility. Do not manufacture new requirements to inspect foreign agents.
- Propose executable next step only after evidence; no blanket restart GO. Healthy new flagsOFF release remains goal, current operational recovery is not permission to change dependencies/other tasks.

This matrix is a stopped-loop remediation proposal, not runtime authorization. Main remains coordination-only; sole runtime Owner unchanged. Independent acceptance then controller authorize-remediation is required. Do not repeat prior static/flags/JAR/consumer scans unnecessarily.

## Independent acceptance and bounded authorization

Godel5 actual independent review: partial evidence ACCEPT; stopped-loop matrix CONFIRMED; PASSIVE_HEALTH_DIAGNOSTIC_ALLOWANCE APPROVE; source/operational findings P0/P1/P2=0/1/0 (P1=Nginx mutable configuration). Main accepts and, ONLY after successful controller authorize-remediation, grants soleTuring PASSIVE_HEALTH_DIAGNOSTIC_R2 under the proposed no-network/no-control scope above, narrowed as follows:
- Aggregate host values once. ExactAPI max two process samples at fixed short interval, state/wchan category counts only.
- At most two own canonical log files, combined maximum256KiB OR each last200 lines, whichever reached first. FD1/2 readlink only, trusted canonical path/no-follow checks mandatory. Logs classify categories/time ranges/counts in memory only. Missing PSI files are platformUNAVAILABLE, not a command retry condition.
- No status/health retry, new requests, locks, signals/attach/service control, foreign processes, configuration or permissions edits. Output passive candidates, not healthUP or proven root cause.
- Completed rescue check is RESCUE_ARTIFACT_TRUST=PASS only; OPERATIONAL_HEALTHY_RESCUE remains NOT_PROVEN. Correct the collector's over-broad rescue trust phrase in any report, do not rewrite original evidence.
- Static Nginx WS tuple IS sufficient for stage1 WS/loopback compatibility; no foreign runtime check is required. Real blocker is0775 isp config, writable by API GID1000. Immutable external snapshot alone does not remove this capability; separate exact-path/custody/permission remediation preservingSHA3a0e51c798c579e017e548322eb4c8f7f5b5dbc040436f90d74814f0d42e36c4 and newest CORS is required before consumer proof. Not authorized in this step.

Web own512M collector is concurrently authorized after ECO heavywindow release at12:30; note its timing when interpreting host aggregates, never attribute earlier12:22 timeout to later build. This passive diagnostic does not consume heavy resources. Independent review follows actual summary before any active remediation.

## Passive R2 actual result and proposed narrowing

SoleOwner shared `/tmp/jvc-oai-runtime-phase1-passive-r2-20260906.SUgAiP/{01-host-api-samples.txt,02-own-log-categories.txt,result.txt,root-cause-candidates.txt,SHA256SUMS}`. resultSHA9932bc3f57c2ad01c1e155e20b9cc5fc18d5cd8e1baf3bcacc7f10c82a22d0fb; candidatesSHA5b26f7f54590a83667abca8d548d99b08bbd469ffdaf2f6bcdb8659e81b0d4da. ExactAPI stable;111threads, RSS343240kB/swap477320kB, lowCPU over2s. Trusted own log bounded200lines at12:38–12:41 has OOM12/GC166, other allowed categories0. This supports JVM memory/GC as candidate, not proven12:22cause orhealthUP. New Web collector eventually failed before Vite due npm identicalconfigpath, not a product memory failure; do not conflate these events.

Main proposes independent acceptance and a final bounded discrimination allowance, NOT execution yet:
- Owner discloses prior OOM/GC classifier patterns from own command (no live read). Distinguish real `OutOfMemoryError` subtype (Java heap space, GC overhead, Metaspace, direct buffer, native thread/OS allocation, UNKNOWN) using at most one new trusted same-log256KiB/200line in-memory scan; emit fixed categories/counts only, no raw exception/line.
- Read only exactAPI cmdline whitelist numeric -Xms/-Xmx/-Xss/-XX:MaxMetaspaceSize/-XX:MaxDirectMemorySize/MaxRAMPercentage and GC choice; no other argv/config values. CheckPID/ticks before/after. No jcmd/attach/signals/requests or runtime property writes.
- Inspect metadata and ACLs only for relevant Nginx config/ancestor chain (existing exact source and effective included paths already shared), no config changes/full raw contents. Determine minimal API-group-write removal preserving administrative isp owner capability and exact content/latestCORS; no permission mutation yet. Check scope/custody against done JY-FOLLOWUP-RELEASE-20260906; no active other Nginx owner in shared ledger observed12:39. If path ownership conflicts, alert-only.
- Return concrete bounded remediation plan for owner (e.g. genuinely evidenced heap constraint vs other subtype; content-preserving mode/ACL changes), do not blindly increase all memory limits or restart without a source/runtime release gate.

This prepares a corrective action, not another general health polling loop. No repeated status/curl, no foreign state, no heavy build. Independent reviewer must decide if this observation is needed/sufficient to proceed toward actual recovery and scoped permissions correction.

## FINAL_MEMORY_NGINX_DISCRIMINATOR_R3 authorization

Godel independent actual passiveR2 ACCEPT, rootcause NOT_PROVEN, final discriminator APPROVE; no new sourcefinding, existing NginxP1 retained. After successful controller admission, main authorizes soleTuring one discriminator now, no further planning round:
A. Disclose prior OOM/GC regex/match semantics from OWN already-executed commands offline (no samples/live reads); clarify line/token/event count.
B. Once same trusted own canonical log, max256KiB/200lines with stable/no-follow and exactPID/ticks, output only fixed OOM subtypes: JAVA_HEAP_SPACE, GC_OVERHEAD_LIMIT, METASPACE, DIRECT_BUFFER_MEMORY, NATIVE_THREAD, NATIVE_OR_OS_ALLOCATION, OTHER_OUT_OF_MEMORY_ERROR, UNKNOWN_OOM_TOKEN; window timestamps/actualOOM line count/GC count. No raw logs, stacks or arbitrary exception strings. This is new observation, not reproduction of old window.
C. Once exactAPI numeric JVM argument whitelist Xms/Xmx/Xss/MaxMetaspaceSize/MaxDirectMemorySize/MaxRAMPercentage plus GC enum. Duplicates/conflicts/missing/invalid explicit. No other argv/secret values.
D. Metadata/ACL only for current relevant Nginx config and its ancestor chain: modeUID/GID/symlinks/mask/defaultACL; compute effective UID987/GID1000 write/rename/replace ability. No config content reads. Produce exact minimal permission/ACL delta preventing API modification both directly and through parent replacement, preserving current configSHA3a0e51… and CORS/administrativeisp ability. Do not implement changes. Active scope conflict => alert-only.
Output concrete task mapping: genuine heap/overhead=>heap-only corrective proposal, metaspace/direct/native subtype=>corresponding single constraint; unknown/no genuineOOM=>NO memory parameter change. Permissions exactpaths+delta. No general health polling loop; no curl/status, locks, signals/attach, foreignproc, production edits, deployment or heavy operations. Main will separately authorize concrete remedy based on actual results, not speculative global memory increases.
