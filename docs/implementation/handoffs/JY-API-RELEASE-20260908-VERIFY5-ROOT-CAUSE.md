# VERIFY5 native failure / changed remediation — 2026-09-08

Exact f2fb244e56439b79515add48fe3a987ccda9b462/tree91be8e6cdd1042bfaddf36a90f83c17eed4ef42b unchanged. Single session20160 started17:16:52; native Gradle rc1 at17:26:41, BUILD FAILED9m39s/11executedtasks, not a deadline/OOM/assertion failure. Five selectedXMLs absent, tests0. Receipt `/var/tmp/cyf-jy-api-release-20260908/verify-5selectors-receipt.json` SHA12bab18f928b4f745c44458bec35bf466c1c97a1e26b0a4c96b68091ef5f1b35; log SHAa90fcece6348a5bb4ad2c8d81db416f30c79fc8923fea8988911482d7d592bc5.

## Matrix

| Fact | Root attribution | Changed action |
| --- | --- | --- |
| common:jia-common-test:compileJava cannot resolve org.apiguardian:apiguardian-api:1.1.2, no cached version for offline mode | Proven missing offline test dependency; not a product-code failure | Allow ordinary configured repository resolution by removing --offline; no dependency refresh, URL change, publish task or credential lookup |
| R3 partial339class files existed, but current Gradle itself logged deleting stale task outputs and recompiling common-core | Presence of prior class files was not proof of reusable Gradle execution state. Underlying ownership/history invalidation not fully established; no evidence JY output was deleted by cron | Retain current naturally terminated build outputs/history; do not clean or assert guaranteed up-to-date |
| Current hook: taskgraph125; configuration/taskgraph~212s after hook; common-core90.9s; only11tasks finished in9m39 | Ten-minute whole-invocation cutoff is poorly matched to complete dependency compilation plus five test selectors | New bounded45-minute complete-verification envelope with same phase timing, log/native receipt, exacttree/5selectors/JVM384M/worker1/global lock; not another unchanged10min attempt |
| Actual own daemon sampled CPU82.8%, VmSwap0/nice0/unlimitedCPUquota | No proof of OOM or swap as this attempt's cause | No heap increase, process preemption, cache cleanup or resource-wait admission |

This is the second actual failure after earlier R3; STOP/blocked_root_cause before any new execution. Main explicitly permits preparation only of the small changed wrapper/plan for independent review. After actual acceptance, authorize-remediation through the orchestrator starts ONE new changed execution cycle. Original R1/R2/R3 and VERIFY5 history remains intact. User requests complete backend publication; no source acceptance or failed test command is a deploy PASS.

17:33 independent Raman actual ACCEPT0/0/0 exact new VERIFY5_COMPLETE script37543c087dc1b0373a483fe5e1a7dd4bc1cc34d98f13fbfdacfd2dfaae6e94b4/hookunchanged9da85. Permits ONE fresh execution under main authorization, not further automatic retries. Per-class positive tests and zero skipped/errors/failures manual gate remains mandatory. Main user-authorized forward remediation invokes authorize-remediation after recorded STOP2; all original failures retained.
