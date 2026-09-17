# SDD Feature Index

更新：2026-09-14。唯一执行台账：`docs/implementation/TASKS.yaml#runtime_ledger_json`；当前全量 SDD 投影与重分配入口：`docs/implementation/SDD_STATUS_20260914.md`；逐项待办快照：`docs/implementation/archive/2026-09-14/reassignment-ledger.json`。历史归档仍保留在 `docs/implementation/archive/2026-09-06/`。

| Feature | 生命周期 | 当前结论 |
| --- | --- | --- |
| [api-performance-3s-slo](api-performance-3s-slo/delivery-status.md) | implementing | 性能 SDD 与若干观测切片已存在；按 2026-09-13 可用性优先策略，真实慢请求用于排序优化，未测算的 3 秒阈值不再阻断请求、发布或交付。完整运行采集与优化仍待推进。 |
| [account-security-foundation](account-security-foundation/delivery-status.md) | implementing | Cookie 修复包已在运行台账行政收口，但只记录 manifest 校验，缺 exact Git 绑定与 credentialed 生产验收；不能把整个账号安全需求标为完成。 |
| [agent-client-skill-refresh](agent-client-skill-refresh/delivery-status.md) | released | 已交付并归档原 2026-08-23 功能；原验收记录 API108、Client97 与运行 smoke，未在本次重复执行。 |
| [agent-workspace-capability-refresh](agent-workspace-capability-refresh/delivery-status.md) | released | 历史 acceptance 与 release 均有依据，统一原顶层 accepted 与 release.released 的陈旧状态，归档 2026-08-23 交付。 |
| [archive-pavilion-reader-mvp](archive-pavilion-reader-mvp/delivery-status.md) | implementing | 已有发布和修复记录；真实认证阅读、进度、书签、私密笔记及双身份隔离业务验收仍在 2026-09-14 重分配清单中，整体不归档。 |
| [juyiting-dual-orientation-experience](juyiting-dual-orientation-experience/delivery-status.md) | implementing | O00–O04 有 accepted 记录；真实设备和用户场景验收仍未因为源码 accepted 自动闭环。 |
| [oauth-public-client-hardening](oauth-public-client-hardening/delivery-status.md) | released | 按原 SDD 中独立审查与 2026-08-24 发布记录归档；不扩大为所有账号安全/公共公测需求已完成。 |
| [agent-economy-marketplace](agent-economy-marketplace/delivery-status.md) | implementing_preview | V0 有 accepted 切片，但真实交易、收费、退款/补偿、安装/激活与业务验收未完成；生产完整 SDD 与 V0 预览严格区分。 |
| [juyiting-voice-conversation](juyiting-voice-conversation/delivery-status.md) | implementing | API/Web/集成候选和部分制品证据已存在；真实 STT/TTS/音频 Provider、运行时启用与用户验收尚未完成。 |
| [public-beta-release](public-beta-release/delivery-status.md) | implementing | 候选及部分发布记录保留；公开可用性、真实身份隔离及端到端公测验收尚未完成。 |
| [juyiting-task-collaboration](juyiting-task-collaboration/delivery-status.md) | implementing | 已有 M3 上线和多项 accepted 记录；M4/M5、默认关闭能力、真实 Agent 安装/激活及业务验收未完成，不能整体归档。 |

## 2026-09-17 版本增量

- `juyiting-agent-model-governance`：draft；登记 Agent 模型展示/按模型费用定义智力值、揭榜模型费用、默认仅接 owner 单的外单 opt-in，以及基于悬赏任务归因的可交付技能候选总结。仅需求登记，未创建实现任务或变更冻结经济合同。
- `economy-readonly-preview-v1-7`：implementing；1.7.0新增只读预览，需求/详设/任务/验收/integration位于同名目录；尚未发布。生产经济冻结合同不修改，真实交易等不算完成。
- `juyiting-voice-conversation`：1.6代码发布有独立证据；网关TTS404、STT未执行，用户主动延期实际启用/验收，运行任务deferred；不阻塞1.7，也不归档整个语音需求。
- 上方2026-09-14表为历史快照，不覆盖其后用户已确认的阅读、双身份双客户端、移动端横竖屏验收；本次不因旧快照重复安排这些验收。

## 生命周期

draft → ready → implementing → integration-ready → accepted → released。`archived` 是另附的历史交付登记，不是运行台账 gate；功能需完整验收才能整体验收归档。已发布且有后续缺陷的记录可以归档，缺陷任务保持活动。

`agent-economy-marketplace/integration.yaml` 属 SHA 冻结生产合同，仍保留 draft；V0 实施状态由 delivery-status.md 与 2026-09-14 重分配基线补充，不修改 bundle。本文档不派发任务或开启生产。

## 2026-09-17 个人中心入口规划（最新补充）

- `economy-readonly-preview-v1-7`：已部署；授权12表修复及限定范围API40/40、Chromium15/15通过，等待用户验收。上文“尚未发布”是历史快照；最终证据见 `/home/isp/wsps/cyf/docs/implementation/V1_7_LOCAL_RELEASE_RESULT_20260917.md`，不扩大为真实交易/完整托管已交付。
- `personal-center-navigation-v1-8`：draft；用户确认将聚义厅个人中心入口纳入下一版，详设方案含双向导航/横竖屏/身份保护，仅文档。完整规格 `/home/isp/wsps/cyf/specs/personal-center-navigation-v1-8/`。旧平台增强仍保留后续待排，本轮不派发、不改运行台账。

## 1.8/1.9统一候选最新回执（覆盖早期draft排期）

- `personal-center-navigation-v1-8`：integration-ready，聚义厅个人中心及经济预览导航已完成；按用户要求不单独部署，release/1.8.0保持冻结。
- `command-observability-v1-9`：integration-ready，协作运行只读看板/安全能力发现已完成；已包含1.8并合入两个组件develop、冻结release/1.9.0，未部署。Web308+策略7、API10+制品64、生产bundle隔离浏览器99通过。
- 详设与回执：`specs/command-observability-v1-9/`、`docs/implementation/V1_9_RELEASE_READY_20260917.md`。本轮只通知候选可发布；不开启特权读取/权限，不将整体M5/G07、语音或交易标为完成。


## 1.9.2实际交付回执（覆盖上述候选未部署状态）

- `personal-center-navigation-v1-8`、`command-observability-v1-9` 已统一发布为 **1.9.2**；包含已有hotfix，修复线上回归发现的OAuth身份接口同名类遮蔽。
- 实际API `e15f7020`、Web `41ca32b`；两个组件develop/release/1.9.2已readback。真实API46/完整本轮浏览器113通过，技术发布与回归完成，**待用户本人验收**。
- 普通账号的运维看板无权说明已验证；未授予ops-read或开启read-enabled。语音、真实交易、完整server托管及整体M5/G07不在本次完成声明中。
- 最终说明：`/home/isp/wsps/cyf/docs/implementation/V1_9_2_RELEASE_RESULT_20260918.md`；SDD冻结分支 `codex/v1-9-2-sdd-release-20260918`。
