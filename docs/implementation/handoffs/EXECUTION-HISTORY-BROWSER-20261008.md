# Execution history browser slice — 2026-10-08

Owner: history-browser-owner (single owner). Task: EXECUTION-HISTORY-BROWSER-20261008.

Scope: real Chromium renders production PersonalWorkspace.vue + real history composable/useHttp → loopback proxy → existing Java JWT/Controller/service/MyBatis → isolated MySQL. Verify 20+1 paging, refresh, empty vs503, identity cleanup, controls at1440×900/390×844/844×390. No Provider/production/deployment.

Fixed API: /home/isp/wsps/worktrees/cyf-execution-history-http-integrate-20261008 @033f200e4a732d4f44b62af1cad794bd9f029ac7, tree661f6ab0599427889b3bd6fde66aa172c791057c.
Fixed Web: /home/isp/wsps/worktrees/cyf-contract-consumer-20261008 @75766a3b78c2e552ef448e924a813ed2dfc7ecd4, treef6f2f4bf35055b1bc88eb2d09b2d11274dd03cdf. Not main checkout or deployed version.
Root changes: existing runner optional --browser; two scoped browser assets; no product source edits. Commit in owned codex/dev-feedback-pilot-20261008 worktree, selectively sync main root.

Boundary: standalone production component; synthetic store/auth and explicit ancillary files/roster/capabilities. Mount recovery invokes production loadHistory(adopt:false), excluding exact execution restoration/selection. History HTTP responses are not mocked. Mouse coordinate dispatch + hit testing, not HTMLElement.click(). Mobile viewport coverage is Chromium emulation, not physical device/full Hall acceptance. Frontend local diagnostic is not formal Flow4403172 evidence.

Status: DONE for scoped browser diagnostic. No product bug discovered or source change required; no component integration needed. No original deferred task reopened.


## Final result / evidence

- Harness commit fd6c8a22; full SHA in proof.json. Owned root branch codex/dev-feedback-pilot-20261008; selectively synced to dirty main root, no blanket merge/reset. Not pushed or deployed.
- 33 runner +15 preflight +19 orchestrator =67 tool tests PASS. Browser fail-closed tests cover Node-only receipt, missing viewport and screenshot tampering.
- /var/tmp/cyf-execution-history-check/run-ss80ge4g/summary.json: PASS,142.684s; first cheap consumer feedback20.868s. Java contract test +validateLayering PASS.
- Chromium29 checks /15 real historyHTTP; original Node17 assertions /8 HTTP;26 real mapper queries;0 forbidden calls;database snapshot unchanged.
- Exact-input REUSED in23.234s without credentials or Gradle/MySQL/browser rerun. All3 screenshot hashes checked; mobile/landscape screenshots also visually inspected. This is not historical fullHall clipping acceptance.
- Durable archive: specs/juyiting-execution-recovery/contract-pilot/evidence/browser-20261008/proof.json + full bundle/screenshots. All archived SHA256 checked; original run paths retained for traceability.
- Precheck found obsolete Chromium wrapper target missing; reused installed /usr/lib64/chromium-browser/chromium-browser133.0.6943.141. No install, shared launcher edits or real-test retry. Owned browser/dev-server/MySQL/Tomcat lifecycle closed normally.
- Next scoped history change can reuse --browser with its own task/source. Frontend formal validation remains Flow4403172, no release authorized. User has no required action.
- 人工定位/实现/等待耗时未独立计时，不补造；以上只报告机器验证/复用耗时。
