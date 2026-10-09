# SDD Feature Index

## 阅读入口（2026-10-08 文档收敛，不修改特性生命周期）

本页原表格与日期补充是**历史状态投影**，并非所有特性的最新状态清单；不要仅因某段写 draft/released 就推断今日状态。当前 Owner/阻塞查 `docs/implementation/TASKS.yaml#runtime_ledger_json`，发布结论查对应精确版本证据；未核实项不在此批量改状态。

- 当前架构/模块知识：[知识库入口](../docs/knowledge-base/README.md)（留意局部核对与旧基线边界）。
- 已完成范围收口样板：[聚义厅议事 UI](juyiting-ui-baseline-20261006/README.md) → [组件职责](../docs/knowledge-base/05-frontend-architecture.md#hall-discussion-composition) / [行为与回归](../docs/knowledge-base/06-juyiting-end-to-end.md#hall-discussion-ui)。仅 UI 切片，非整个特性或业务完成。
- 其他特性尚未逐项完成知识收口；下方历史合同、状态和证据继续保留，不以本次文档整理替代核验。

## 历史索引及增量记录


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

- `juyiting-agent-model-governance`：ready（2026-09-18）；已冻结 Agent 模型/计费智力值、无副作用揭榜模型费用预估、默认 owner-only 的同 scope 外部精准邀请，以及基于已接受任务结果的可交付技能候选/确认合同。未创建实现任务，未变更冻结经济合同。
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

## 2026-09-18 MVP 价值闭环重评估

- 认证只读体验与 exact release 源码核对见 `docs/implementation/MVP_VALUE_GAP_ASSESSMENT_20260918.md`；不把空成果列表、历史聊天或接口 200 当成新任务执行验收。
- `juyiting-agent-model-governance` 保留 ready 设计，**不等于完整治理优先于 MVP**；最新安排为 1.10 文件库、1.11 Word 闭环、1.12 图片/PPT、1.13 完整文件 MVP、1.14 治理。版本安排见 `docs/implementation/VERSION_PLAN_20260918.md` 第 1 节；未派发、未改运行台账、未自动扩大客户端/付费授权。
- 正式交付已有发布代码与线上读取入口；缺口按真实任务→执行→成果→验收链路逐段核实，不能把整套 R2 重标为尚未开发。

## 2026-09-18 用户明确 MVP 最低成果范围（覆盖仅文本建议）

- `juyiting-creative-delivery-mvp`：draft（业务目标已明确，技术合同待核）；完整范围分 1.10.0–1.13.0 交付，目标为真实生图、按原图改图、根据用户材料生成可下载可编辑 `.pptx`，并支持上传用户已有 PPT/Word/PDF/Excel 由 Agent 读取和对话修改；逐格式验证预览及新文件下载，不建设在线内容编辑器。必须贯通原图/资料输入、实际执行、文件持久化、预览/下载和修改版本，不以提示词/大纲/演示代替。
- `juyiting-agent-model-governance`：保留 ready 设计、后移 1.14.0；默认 owner-only/权限隔离/费用诚实前置，完整计费智力值、外单和技能自动总结不阻塞上述 MVP。
- 最新统一排期：`docs/implementation/VERSION_PLAN_20260918.md`；原只读体验证据保留，未转写为生图/改图/PPT 执行通过；本轮无实现、无用量、无运行台账变更。

## 2026-09-18 个人工作空间补充

- `juyiting-creative-delivery-mvp` 继续 draft、首版 1.10.0 / 完整 MVP 1.13.0：业务中心改为个人工作空间，统一管理上传资料和 Agent 交付，悬赏关联可选、固定文件版本，Agent 仅访问本次授权输入；具体见同目录 `workspace-design.md`。无实现、无运行台账变化；原 C0 证据不等于工作空间已上线。

- C1 接口/数据候选已补入 `juyiting-creative-delivery-mvp/workspace-contract-v1.md`，分 A/B 个人文件库和 C/D Agent 执行桥接；28 项设计案例未执行，feature 保持 draft，无应用/台账变更。

## 2026-09-18 个人工作空间 1.10 实施准备与估算

- 任务和范围：`juyiting-creative-delivery-mvp/v1-10-implementation-plan.md`，10 项未派发任务，工程预算 72–118 人时；API/Web 两线按各每天 6 小时有效投入假设为 10–16 个工作日，非 Agent 连续耗时或上线承诺。
- 验收：同目录 `v1-10-acceptance.md` / `v1-10-acceptance-cases.json`，30 项全部未执行。已记录 18 个 exact 源码 blob 的估算依据，不是应用测试证据。
- feature 继续 draft、完整 MVP 仍为 1.13；本轮仅实施准备，无代码/台账/生产/付费变更。

## 2026-09-21 聚义厅整套体验设计

- `juyiting-unified-experience`：draft，基于用户认可的完整离线Demo完成整体方案、UI/工程详设、14包WBS与工作量估算。首次默认地图，明确保留手动横竖屏切换，统一办理链路而不合并私人/正式任务权限。基础45–71人日，含具体风险51–82人日；两名核心研发+兼职测试参考7–10工作周。仅设计交付，未派发、未改应用/运行台账、未构建/部署；接口待M0冻结。规格入口 `/home/isp/wsps/cyf/specs/juyiting-unified-experience/spec.md`。

### 2026-09-21 Agent并行实施补充

`juyiting-unified-experience`已由用户授权开始Agent并行开发，状态implementing；旧7–10周人力排期不用于本次执行。先完成10个已完成worktree清理和历史交接压缩，再从Web1.13.9/API1.13.8建立独立工作树，派发W01与B01A两名Writer。完整14包已登记唯一运行台账；无Reviewer、无Flow、无本机生产构建、无新发布。第一波合同与接续计划见 `/home/isp/wsps/cyf/specs/juyiting-unified-experience/agent-execution-plan.md`。

## 2026-09-22 Agent 通讯与协作执行详设

- `juyiting-task-collaboration` 增量详设：[功能缺口与详细设计](/home/isp/wsps/cyf/specs/juyiting-task-collaboration/connectivity-detailed-design-20260922.md)，draft。覆盖显式 @直达、密议、宋江受限协调、Agent 问答/委托、Eva 真实测试构建和开发控制面；14 项功能、32 项待执行验收。仅文档，不修改既有 feature 生命周期/冻结合同，不派发实现、不激活、不改唯一运行台账。


## 2026-09-23 正式悬赏移动竖屏复测 bugfix

- `juyiting-formal-flow-bugfix-20260923`：draft，吴用正式悬赏 #395 真实 UI 复测未闭环。已整理点将未送达、榜文议事 404、正式资料关联缺口、深层文件查看禁用、workspace/events 503、主状态映射不完整六项需求；交付/验收为被阻塞未到达。未实现、未构建/发布；证据及验收见该目录。

- 版本增补：**1.13.19 planned / solution_defined**，上述六项修复纳入同一 bugfix，实施未开始。方案：`docs/implementation/V1_13_19_FORMAL_FLOW_BUGFIX_PLAN_20260923.md`；登记：`specs/juyiting-formal-flow-bugfix-20260923/version-plan.yaml`。


## 典籍阁 Agent 任职与内容维护方案

- `archive-agent-maintenance`：ready / D2，可交接其他 Agent 从 M0 实施。宋江协调或直达任职 Agent，经技能与受控 API 完成多书/不可变版本、草稿校验及授权发布；保留旧阅读、身份隔离和共享执行/存储合同，不扩旧 ItemRef。入口：[实施交接](/home/isp/wsps/cyf/specs/archive-agent-maintenance/handoff.md)、[详设](/home/isp/wsps/cyf/specs/archive-agent-maintenance/design.md)、[开发计划](/home/isp/wsps/cyf/specs/archive-agent-maintenance/tasks.md)。84 项业务验收均未执行；仅文档提交，无派发、组件 gitlink/运行台账修改、构建部署或生产激活。

- 2026-09-30 语音补充：升级后 CLIProxyAPI 的 Realtime 单次真实音频交互已验证，旧独立 STT/TTS 路由404记录仍保留；新适配单列 `juyiting-voice-realtime`，源码/发布/生产启用/设备验收分别追踪，不把网关证明写成页面已上线。

## 2026-10-07 多媒体议事实际状态补录

- [juyiting-multimedia-deliberation](juyiting-multimedia-deliberation/delivery-status.md)：implementing / NOT_COMPLETE。API117、Web177已版本化发布；纯文字、图文理解、原图片生成、可选保存有真实子集证据。新task426最短纯文字完整闭环通过，存在四项确定UI缺口；混合关联/验收、附件-only/澄清、音频、第二账号及Client集成仍见[剩余任务](juyiting-multimedia-deliberation/remaining-tasks-20261007.md)。历史worktree/分支已按范围清理；Codex历史子会话34个已原生删除，当前及Owner主会话保留。本轮未新增构建或部署。
