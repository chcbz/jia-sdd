# R1 release gates remaining after development acceptance

All rows below remain OPEN as of2026-09-13. OD06 development acceptance permits OD07; it does not satisfy execution-plan section9 release acceptance. OD11 owns closing applicable local integration work before declaring the complete requirement finished. Canonical build/deployment and physical-device evidence cannot be inferred from local component PASS.

| Gate | Owner / due | Minimum closure |
| --- | --- | --- |
| Canonical package and reproducible candidates | OD11 release_guard | Resolve checked-in OpenCV/JAI/catalog without development substitution, validate package and exact three-repository candidates; pins only after authorized reproducible remote source |
| Hosted mode | OD11 integration operator | Trusted hosted dispatch through artifact retrieval, record actual deployment mode |
| PUT and bounded large-file transport | OD11 integration operator | Actual interrupted upload/restart and configured size/timeout; retain original response/download bytes and Agent PID/startTicks |
| Writes paused and dependency outage | OD11 integration operator | Existing owner reads remain usable while new writes fail closed; real isolated storage/scanner outage/recovery |
| Paging and lifecycle | OD11 integration/Web operator | >100 real outputs with cursor browsing, representative disconnect/reopen; expiry/hold/GC race coverage attributable to actual runtime or specifically justified test boundary |
| Full user entry paths | OD11 Web operator | Hall, standalone chat, bounty detail, identity/history switch, no selectable Agent, workspace disabled; actual UI navigation and authorized downloads |
| WeChat | Actual-device owner + OD11 coordinator | Physical WebView download or real same-account external-browser authorization and download; resource link has no token |
| Deployment topology and operations | OD11 release_guard | Fresh/upgrade/partial schema behavior, effective same datasource/transaction manager, proxy body/timeout, private bucket and scanner/signatures/retention/backup configuration |
| Portable contract fixtures | Each contract-changing writer; OD11 cross-repository check | Applicable API/Web/client snapshots with origin/hash and standalone test consumption; root/API already identical |
| Production release | Release owner | Concrete deployment scope authorized and actual migration/deployment evidence; no incidental pipeline-triggering push |

Reuse existing successful tests and live fixtures. Only rerun affected scenarios after code/configuration changes or to close an identified gap. Do not re-probe the previously failing private Maven origins or forward credentials across hosts merely for freshness. Existing isolated persona was intentionally unbound; create a new disposable binding when a new trusted execution is required, leaving the old owner's retained artifacts intact.
