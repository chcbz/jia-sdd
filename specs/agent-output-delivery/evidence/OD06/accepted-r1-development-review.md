# OD06 independent R1 development gate

Verdict (2026-09-13): ACCEPT / accepted_for_development; OD07 unlocked. Reviewer `/root/od06_tenant_review` is independent and read-only. No P0/P1 product defect requires reopening the frozen candidate. This is not R1 release acceptance; overall acceptance remains pending.

Frozen API `f1978b09ac7d567a53923f7c7e5c1bc3667e6a13`, Web `212bfe4f9441cc82262d98e7b0723d6c0800e3d9`, client `714b4aa73b474b37ec6348d045b653a3ca273cf2`. Reviewer independently read source status/SHAs, archived JSON/XML and hashes, and compared the root/API fixture. All product trees were clean. No Gradle, browser or live requests were rerun during review. Root records the returned verdict here; see r1-candidate-association.json for Root checks.

| Acceptance | Evidence level and result | Remaining verification |
| --- | --- | --- |
| O01–O03 | OD04/05 reviewed components; real conversation Markdown and TASK Markdown/PNG/ZIP; offline byte equality; actual resource-route browser reads | Hosted deployment mode; PDF has not been exercised |
| O04/O27/O30 | Reviewed queue/idempotency/corruption checks; real committed complete response dropped, restarted Agent recovered PUBLISHED, generator count1, only v1 | PUT interruption, large-file/timeout, recovery UI |
| O05/O06 | API snapshot pagination and Web event dedup/order/refresh/truncation component tests | Live >100-item pagination and disconnect/reopen slice |
| O07/O09/O23/O26 | Reviewed identity/ACL/run/ticket/cross-binding negatives; actual WS dispatch/ticket/publication, foreign list/detail/download404, JWT reads | Deployment authentication/topology validation |
| O08/O19 | Reviewed three Web entries, no-Agent resource route and legacy states; actual TASK owner share and resource-page retrieval | Hall/bounty/history/identity navigation and workspace-disabled browser paths |
| O10–O12/O28/O29 | Reviewed path/symlink/FIFO, hash/MIME/ZIP, quota, rollback, GC/read-pin/owner-share components and real dependencies; three formats passed actual storage/scanning | Runtime outage and production sizing configuration |
| O20 | Client retention305/305 and reference/GC tests; actual unbind retained all three files; Root read saved bytes | Real expiry/hold/GC concurrency and unbind UI |
| O21 | Four resources/eight desktop and simulated-mobile viewports with screenshots and download byte checks | Physical WeChat or demonstrated real authorized alternative |
| O22 | Writes-paused capability/write503/retained-read component coverage | Live paused/storage/scanner outage; unsupported policy1 clients belong to OD07 |
| O02/O30 | Reviewed manifest bounds/duplicates/special-files/queue corruption/restart; actual ZIP contains change.patch and README.md | Hosted deployment evidence |

Review evidence: live-conversation-text-43e6bb94, live-bounty-task3-f1978b09, browser-resource-pass-f1978b09, live-recovery-unbind-f1978b09 and their Root observations; earlier accepted OD01–OD05 and OD06 repair/retention reviews remain separately attributable, not relabeled as live/full-suite results.

P2 evidence gaps accepted for continued development:

- Root/API fixture3150B is byte-identical, SHA256453968ce85423aaf091e81d8600f2959fc44efca66793637927a06da54e48f6f. Web/client directly test their consumed protocols but have no matching shared fixture snapshot. Contract-changing writers must add applicable snapshots; OD11 checks their hashes.
- TASK4 helper compared HTTP downloads with snapshots in memory. Root independently read snapshots, not preserved TASK4 HTTP bodies; TASK3 download bytes were independently checked through online/offline/unbound phases. Publish-stage recovery probes should retain downloaded bytes.
- Agent exec-session/registration/stop boundaries exist, but Agent OS PID/startTicks were not persisted. Keep complete process identity in subsequent recovery evidence.

The reviewer explicitly allowed OD07 critical-worker lease/policy implementation, including all funded/legacy/direct completion guards and unsupported client rejection. Remaining R1 release gates are tracked in r1-release-gates.md; none become passed merely because OD07 starts.
