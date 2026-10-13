# Codex Project Map

## 日常阅读入口（2026-10-08 收敛）

- **如何执行本项目任务**：根 `AGENTS.md`；构建/部署以 `docs/aliyun-flow-cicd-strategy.md` 为准。
- **系统如何工作、改动落在哪里**：[架构与模块知识入口](knowledge-base/README.md)。按任务只读一至两个主题；注意各节实际源码核对范围，未重建的旧基线不当作当前事实。
- **准备做什么**：[特性索引](../specs/INDEX.md)与对应 SDD；当前 Owner/阻塞仍只查 `docs/implementation/TASKS.yaml#runtime_ledger_json`。
- **过去为何这样做、如何验收**：按主题文档的来源链接查原设计/交接/发布证据，不默认串读历史计划。文档收口见 [SDD 工作流](sdd-workflow.md#feature-documentation-closeout)。


<!-- SDD delivery reconciliation 2026-09-06 -->
## 历史交付索引（2026-09-06 快照，不代表当前版本）

- `specs/INDEX.md`：全部跨仓需求及 delivery-status（包括补录的语音、公共公测和协作 SDD）。
- `docs/implementation/SDD_STATUS_20260906.md`：全部运行任务和原始规划的完成/未完成映射。
- `docs/implementation/archive/2026-09-06/README.md`：已执行的历史交付归档及保留的后续问题。
- 本地 api/web checkout、远端 accepted commit、实际部署与 root gitlinks 不可混用；静态知识库生成基线未在本次重建。
<!-- END SDD delivery reconciliation -->

This file is a compact orientation map for future Codex sessions. It should stay short and stable; detailed feature notes belong in focused runbooks.

## Top-Level Layout

| Path | Purpose |
| --- | --- |
| `web/` | Vue frontend app, Vite build, UI components, frontend assets, frontend tests |
| `api/` | Java backend workspace with Gradle modules for common, agent, chat, task, and ISP domains |
| `docs/` | Project guides, implementation plans, operational notes, and the reverse-engineered knowledge base |
| `deliverables/` | Packaged deployment artifacts and generated packages |

## Git Layout

- The workspace root is the `jia-sdd` coordinating Git repository.
- `api/` and `web/` are independent Git repositories registered as submodules and pinned by the root commit.
- Agent client development continues to follow ADR-004: versioned source lives under `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/`, while `/home/isp/apps/codex-ws-agent/` is the deployment copy; no additional repository is required for economy/skill delivery.
- Use `git status` for the coordinated delivery baseline, and `git -C api ...` or `git -C web ...` for implementation history.

## Frontend Layout

| Path | Purpose |
| --- | --- |
| `web/src/main.js` | Frontend bootstrap |
| `web/src/router/index.js` | Route registration |
| `web/src/components/` | Vue components grouped by feature |
| `web/src/components/world/JuyiHall.vue` | Current Juyi Hall page composition |
| `web/src/components/juyiting/` | Juyi Hall panels, map stage, tokens, command/chat surfaces |
| `web/src/composables/` | Shared and feature-specific frontend logic |
| `web/src/composables/juyiting/` | Juyi Hall data, conversation, physics, sound, and portrait logic |
| `web/src/constants/juyiting.js` | Juyi Hall filters, role metadata, map anchors, obstacles, walk bounds |
| `web/src/stores/` | Pinia stores and demo data |
| `web/src/assets/` | Frontend static assets imported by source code |
| `web/tests/` | Frontend contract and smoke tests when available |

## Backend Layout

| Path | Purpose |
| --- | --- |
| `api/agent/` | Agent runtime, persona, task metadata, roster/map/task APIs |
| `api/chat/` | Chat conversations, messages, Juyi Hall conversation type support |
| `api/task/` | General task planning and execution modules |
| `api/common/` | Shared backend infrastructure, utilities, base entities, test support |
| `api/isp/` | ISP/domain/CMS related modules |

Backend modules are split into `*-core`, `*-api`, `*-mapper`, `*-service`, and `*-starter` style Gradle projects. Inspect the nearest `build.gradle` before choosing a build or test command.

## Build and Test Entry Points

### 先找已有入口（2026-10-08）

| 任务场景 | 定向入口 |
| --- | --- |
| 本次提效已证实什么、下一项任务如何执行 | [开发效率与上下文管理](sdd-workflow.md#development-efficiency)：验证复用已测；整体开发周期/上下文收益待真实业务任务检验 |
| 核对任务基线、脏工作区、fixture位置 | [编排工具索引](../ops/orchestration/README.md)：`cyf_orchestrator.py preflight`，只读诊断，不等于验证通过 |
| 执行历史接口/前端消费的定向回归 | [执行历史单命令说明](../specs/juyiting-execution-recovery/contract-pilot/README.md)：`execution_history_check.py`，精确输入命中才复用，否则走既有编排锁验证 |
| 子 Agent/独立 worktree接续 | 交接项目 `AGENTS.md`、命中的说明、当前任务ID和固定源码；不依赖聊天记忆或旧worktree自带说明 |

按场景只读对应说明；执行历史试点不覆盖所有功能，`--browser` 仅补充独立组件浏览器诊断，不替代前端正式Flow、整站/OAuth验收或发布授权。


Develop is for integration and verification, with no automatic deployment. As of 2026-10-08, frontend formal tests, production builds, artifacts and deployments use Alibaba Cloud Flow; backend formal tests, builds, artifacts and deployments run locally from a fixed clean commit/tree. Versioned releases bind the same Flow Run (frontend) or local build ID/logs (backend), artifact digest and online verification; see `docs/aliyun-flow-cicd-strategy.md`. Frontend local work remains limited to development previews and low-cost diagnostics:

```bash
cd web && npm run dev -- --host 0.0.0.0
```

Local Vite production builds are prohibited; backend local Gradle results are formal evidence when bound to the exact commit/tree, selectors, fixture and build artifact. All Gradle work must go through `python3 ops/orchestration/cyf_orchestrator.py gradle`, after inspecting the current relevant `build.gradle`. Build backend artifacts outside the production installation directory; deploy verified bytes under the existing lock, backup, identity and health/recovery protections. Local installer input adaptation still requires verification; do not fabricate Flow Runs or restore old pull/build/restart shortcuts.

## Common Search Targets

- Juyi Hall UI: `rg -n "JuyiHall|聚义厅|juyiting" web/src`
- Agent APIs: `rg -n "/agent|Agent" api/agent web/src`
- Chat stream/events: `rg -n "chat/stream|conversation/events|juyiting" api/chat web/src`
- Task assignment: `rg -n "assign|悬赏|tasks/search|tasks/.*/assign" api/agent web/src`

## Documentation Entry Points

- `docs/aliyun-flow-cicd-strategy.md`: authoritative frontend Flow / backend local build, test, artifact, and deployment policy.
- `docs/aliyun-flow-host-cleanup.md`: Flow host cleanup scope, installed script, dry-run commands, and resource measurements; no broad workspace or age-based pruning.
- `docs/juyiting-runbook.md`: compact guide for ongoing Juyi Hall changes.
- `docs/juyiting-occlusion-system-design.md`: extensible full-map occlusion, world sorting, TMX schema, migration, validation, and Agent execution plan.
- `docs/juyiting-occlusion-system-execution-plan.md`: serial implementation backlog, DeepSeek/GPT allocation, handoff gates, verification, and release sequence for occlusion v2.
- `docs/juyiting-feature-guide.md`: deeper Juyi Hall behavior and data-flow documentation.
- `docs/juyiting-collaboration-implementation-plan.md`: historical implementation plan for collaboration flow work.
- `docs/juyiting-multi-agent-collaboration-design.md`: target architecture, detailed design, backlog, migration, and phased rollout plan for reliable multi-Agent bounty collaboration.
- `specs/agent-economy-marketplace/`: draft SDD for SILVER wallets, token-priced bounty settlement, and Agent skill commerce/delivery.
- `docs/implementation/README.md`: execution control center for multi-model implementation, including the task ledger, coverage matrix, decisions, and handoff rules.
- `docs/codex-ws-agent.md`: Codex websocket agent operational notes.
- `docs/project-feature-implementation-checklist.md`: cross-project feature completeness and optimization checklist.
- `docs/project-markdown-coverage-matrix.md`: one-to-one coverage record for every audited source Markdown file.
- `docs/project-api-endpoint-audit.md`: endpoint-level mapping from interface documentation to Controllers.
- `docs/project-plan-task-audit.md`: Task/Phase-level implementation audit for project plans.

## Maintenance Rule

When a future task uncovers stable project knowledge that would save repeated exploration, update this file or the relevant runbook in the same change.

- `docs/knowledge-base/README.md`: task-routed entry point for current-state code, API, data, and integration reference.
- `docs/knowledge-base/04-backend-api-index.md`: compact Controller/base-path index; use the full API inventory only for method-level details.
- `docs/sdd-workflow.md`: multi-repository SDD lifecycle and integration gate.
