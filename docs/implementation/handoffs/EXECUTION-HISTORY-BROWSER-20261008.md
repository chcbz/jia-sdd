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

## 提效结论收口（2026-10-08）

测试事实仍以上述固定源码和proof为准。已证实单命令验证与精确输入复用；未测量业务端到端周期/上下文压缩收益，不外推整体提速。下一步使用已有流程完成真实业务任务，而非默认继续扩建工具。

稳定执行规则已回写 `docs/sdd-workflow.md#efficiency-findings-20261008`，并由根 `AGENTS.md` 与 `docs/codex-project-map.md` 建立入口；不要求后续Agent读取本聊天。后续结论维护该工作流章节，本handoff保留本次证据。此次为当前工作区文档更新，未向全部在途Agent广播或取得阅读回执，也未发布到远端；独立worktree接续需Owner显式传递最新入口。

## 远端develop核对与通用规则收口（2026-10-08 23:39 +08:00）

本次通过git ls-remote实际查询origin的refs/heads/develop，不把本地跟踪引用当远端最新。三个主工作区分支名均为develop，但均已分叉（下列数值为提交图各自独有的commit数，不等同缺少的功能数）。查询结果是该时刻快照，不是永久“最新”。

| 仓库 | 主工作区HEAD | 远端develop | 本地独有 / 远端独有 |
| --- | --- | --- | --- |
| . | `cd2c6ef361f6cccee9a83b2a678dac7d19f9320a` | `7997310541164ff0b4586a17cd55c59a79c4d34e` | 4 / 11 |
| api | `033f200e4a732d4f44b62af1cad794bd9f029ac7` | `ce047c43e0f275d1ad427c484b8919213be36fa4` | 1 / 328 |
| web | `c567e0593bd0334a4f6d47536e235fc1c3af7bb5` | `75766a3b78c2e552ef448e924a813ed2dfc7ecd4` | 1 / 520 |

- 先前受测Web75766a3b与此刻远端develop一致；受测API033f200e与此刻远端develop ce047c43不同。原PASS不作废，但仅覆盖固定组合，不能宣称最新develop前后端组合通过。当前线上版本未查询，不推断。
- 根仓库和Web存在大量未提交修改；本轮不pull/reset、不改分支、不覆盖修改，不触发构建或部署。后续业务开发应从重新核实的远端develop固定干净worktree，并逐项处理本地独有改动，不能把旧候选证据平移给新tree。
- 项目入口已统一为“开发效率与上下文管理”：根AGENTS只保留通用原则与索引；工作流集中维护通用执行、按风险裁剪、专项工具及效果评估；项目地图、handoff模板同步，原效果评估锚点和历史证据保留。
- 本轮为当前主工作区文档修改，未提交/推送到远端，未宣称其他worktree已同步。入口与链接检查通过，无需应用构建。
