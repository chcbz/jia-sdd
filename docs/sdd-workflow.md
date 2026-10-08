# Multi-repository SDD workflow

## Source-of-truth rule

| Question | Authoritative location |
| --- | --- |
| What should be built and accepted? | `specs/<feature-id>/` in the root repository |
| What does the system currently do? | `docs/knowledge-base/` and the pinned submodule source |
| How does it run or get deployed? | `docs/` runbooks and deployment material |
| How is it implemented? | `api/` and `web/` submodules |
| Which backend/frontend pair is an integrated baseline? | The root commit's `api` and `web` gitlinks |

`specs/` is the intended future state. `docs/knowledge-base/` is a reverse-engineered current-state reference. Neither replaces source code for implementation details.

<a id="development-efficiency"></a>
## 开发效率与上下文管理（2026-10-08）

### 通用执行规则：所有任务适用

1. **确认范围与基线**：使用现有任务ID和handoff，固定Owner、目标/非目标、验收、源码commit/tree和worktree。分别记录本地HEAD、远端develop（实际查询时间）、受测候选与线上版本，不能相互替代。共享工作区有未提交修改时不自动pull/reset，以免覆盖其他任务。
2. **最小充分上下文**：从根AGENTS → 项目地图 → 相关模块/工具说明 → 当前handoff进入，按需搜索代码。日志、历史证据只记录路径及必要摘要；不要为“补全背景”全量读取。压缩/交接摘要包含目标、范围、源码、已确认结论、证据、阻塞、下一条可执行动作及禁止操作。
3. **连续实现与分层验证**：复用已有工具，先做能暴露本次问题的定向检查，再覆盖相关回归。Owner在授权内连续推进，不逐阶段等待批准，不新增独立Reviewer。精确输入和证据完整性匹配才复用结果；前端正式验证仍走Flow，后端在固定干净源码经编排器执行；与发布授权/部署分开。
4. **接续与收口**：Owner向子Agent/独立worktree显式传递最新项目规则路径、任务ID、源码基线、相关工具和handoff；确认接收方读过，不假设继承聊天或自动重载。在途任务自然接续时提醒，不打断其他任务。稳定知识回写已有模块/架构/运维指南，测试事实保留原证据路径。
5. **效果评估**：沿用[handoff模板](implementation/handoffs/TEMPLATE.md)记录定位、实现、验证、等待与返工原因；未知留空，按可比任务判断端到端收益。下一项真实业务任务优先使用现有流程；只有可证实的实际阻塞才驱动工具扩展，不为提效再建一套框架/台账/审批。

### 按范围裁剪文档与工具，不裁掉风险控制

- 无跨仓契约变化的局部UI/单模块修复，沿用已有任务及handoff、更新受影响说明，不仅为日常进度创建五件套SDD。
- 跨仓功能仍按下文Required feature artifact组织；身份/ACL、事务、迁移、异步契约变化保留明确设计及相关回归。任务大小不替代风险判断。
- 专项验证器只服务其声明范围：执行历史工具及 `--browser` 见[原操作说明](../specs/juyiting-execution-recovery/contract-pilot/README.md)，不是所有功能的统一门禁。不重复维护命令/参数说明。

<a id="efficiency-findings-20261008"></a>
### 效果评估：已证实与待验证（核对：2026-10-08）

- **已证实**：执行历史已有单命令入口，复用隔离后端/数据库与浏览器诊断；精确输入证据完整性核验后可免重复执行。同一固定输入，本次完整验证142.684秒、证据复用23.234秒、首次廉价反馈20.868秒。这是单次验证/缓存观测，不是业务开发前后对照，不外推整体提速比例。
- **未证实**：尚无可比真实业务任务的定位、实现、等待全程数据，不能宣称“小功能从几天降到几小时”，也未测得上下文压缩频率或token消耗下降。
- **证据和边界**：见[本次handoff](implementation/handoffs/EXECUTION-HISTORY-BROWSER-20261008.md)及其中的固定API/Web与proof引用；详细操作沿用[执行历史说明](../specs/juyiting-execution-recovery/contract-pilot/README.md)。此工具只适用于执行历史相关任务，本地浏览器诊断不是正式前端Flow、整站OAuth验收或部署证明。

## Required feature artifact

Use one directory per cross-repository feature:

```text
specs/<feature-id>/
├── spec.md             # Problem, goals, non-goals, scope
├── design.md           # UX, API/event/data/security and compatibility contract
├── tasks.md            # Explicit API/Web/integration owners and work items
├── acceptance.md       # Observable acceptance criteria and evidence
└── integration.yaml    # Candidate submodule SHAs and verification state
```

The API contract in `design.md` must state method/path, request/response/event shape, error behavior, authentication/authorization, compatibility, and version/replay semantics when it is asynchronous.

## Lifecycle

1. **Draft** — Create the feature: `./sddw new <feature-id> "title"`; define the problem, goal, non-goal and scope.
2. **Ready** — Agree the contract and split `tasks.md` into `api/`, `web/`, and integration work. Identify migrations, ACL, transactions, SSE/WebSocket replay, and rollback constraints before implementation.
3. **Implementing** — Implement in each submodule on independently reviewable commits. Do not commit one repository's source into the other or into the root.
4. **Integration-ready** — Check out the intended API/Web commits locally, run the relevant tests, then execute `./sddw pin <feature-id>` and `./sddw verify <feature-id>`.
5. **Accepted** — Record test commands/results in `acceptance.md`; set `integration.yaml` status to `accepted`; commit the spec update and both submodule gitlinks together in the root repository.
6. **Released** — Add deployment/release evidence only after the actual deployment process succeeds. The root SHA is the reproducible delivery baseline.

## Daily commands

```bash
# Inspect coordinated and implementation state
./sddw status

# Start a cross-repository feature
./sddw new agent-task-collaboration "Agent task collaboration"

# After API and Web commits are checked out locally
./sddw pin agent-task-collaboration
./sddw verify agent-task-collaboration

git add specs/agent-task-collaboration api web docs
git commit -m "feat(sdd): integrate agent-task-collaboration"
git push origin master
```

## Integration gate

A root integration commit must include all applicable items:

- `spec.md`, `design.md`, `tasks.md`, and `acceptance.md` are current.
- `integration.yaml` contains the exact API and Web commit IDs currently checked out.
- API, Web, and integration verification commands/results are recorded.
- Breaking behavior, schema migrations, access-control changes, and async replay semantics are explicitly assessed.
- The root commit updates the submodule gitlinks only after the submodule commits are pushed and reproducible.

For P0 identity/ACL/transaction/migration changes, use task/worktree/path-scoped ownership. The implementation Owner must self-check the exact scope, authorization, identity isolation, transaction/migration behavior and recovery boundary; do not create or wait for an independent Reviewer. Ordinary ready changes merge to component `develop` after the Owner’s self-check, without automatic deployment. As of 2026-10-08, frontend formal tests/builds/artifacts/deployments use Alibaba Cloud Flow; backend formal tests/builds/artifacts/deployments run locally against a fixed clean commit/tree. Versioned releases bind the same Flow Run (frontend) or local build ID/logs (backend), immutable artifact digests and online verification. Every Gradle invocation must use `python3 ops/orchestration/cyf_orchestrator.py gradle`; inspect the current relevant `build.gradle` first. Backend builds must not run in the production installation directory, and local artifact installation retains locks, backups, recovery, identity and health checks. The existing Flow downloader is not a local artifact installer; adapt and validate local inputs without fabricating a Run or restoring old source-to-production shortcuts. Production data, paid operations and actions outside the authorized release scope still need explicit authorization. See `docs/aliyun-flow-cicd-strategy.md`.

## 2026-09-14 reconciliation and archival rules

- Current feature index: `specs/INDEX.md`; full execution/planning audit: `docs/implementation/SDD_STATUS_20260914.md`.
- `delivery-status.md` is a dated read-only projection, not a second owner/gate ledger. Runtime transitions remain exclusively orchestrated in TASKS.yaml.
- A frozen SHA-bound contract must not be rewritten for routine progress. Add a dated status supplement; preserve the original bundle and evidence binding. Contract changes need their own reviewed version.
- Keep intent/design, source acceptance, integration, artifact release, activation and actual user acceptance distinct. A build or API health check does not prove functional acceptance.
- Archive completed delivery records with exact evidence and residual follow-up links. Do not remove live tasks, evidence, worktrees, services or notification jobs. Historical failures/waivers stay failures/waivers, not PASS.
- Only archive an entire feature when its own scope is accepted and released. A prior release can be archived while later defects remain active. Record archival separately; do not invent an `archived` runtime gate.
- Never run `sddw pin` against stale/dirty implementation checkouts just to make a document verifier pass. Preserve historical pins; missing release-pair evidence remains explicit. Client-only features can have Web N/A, which the current strict `sddw verify` does not support.
- Document-only reconciliation requires structure/link/schema/evidence-consistency checks, not Gradle/Vite, deployment or a separate Reviewer. Never mass-stage unrelated working-tree changes.

<a id="feature-documentation-closeout"></a>
## Feature documentation closeout（2026-10-08）

已核验特性收口时，更新现有主题说明而不是把实施记录拼入一份巨大架构文档：

| 稳定知识 | 长期归属 |
| --- | --- |
| 系统组成、模块职责和依赖 | `docs/knowledge-base/01-system-overview.md`、03/05 架构主题 |
| 功能行为、接口/事件、状态流与权限边界 | 对应模块主题（如 `06-juyiting-end-to-end.md`、07 数据安全） |
| 配置、排障、发布与恢复 | 现有 runbook / 发布策略 |
| 关键取舍及原因 | 既有 DECISIONS / 对应决策记录 |
| 原需求、冻结设计、执行计划、测试/发布回执 | 原路径保留为历史来源，日常入口链接现行主题 |

操作顺序：核对精确源码和已有验收范围 → 提炼稳定知识到相应主题 → 写明核对日期、commit、章节覆盖与未验证边界 → 特性目录增加来源导航/收口说明 → 当前入口指向主题，追溯才进入历史材料。

- 只完成一部分时按切片收口；保留其他活动任务，不将整个 feature 重标 released/archived。源码已实现未发布时明确标注，历史上线时间不代表当前线上版本。
- 冻结文件、证据和其路径不改写、不搬动；优先新增目录导航建立双向引用。需要物理归档时另核引用和证据绑定，不借整理删除历史失败或活跃待办。
- 局部复核不更新全库 `BASELINE.yaml` 的生成日期；未复核内容明确沿用旧基线。文档状态是阅读提示，不是第二份 Owner/gate 台账。
- 不新增独立审查、审批或应用构建；文档改动仅检查链接、内容/源码证据对应及原材料未变。整理完成不等于功能新增验收通过。
- 样板：[聚义厅 UI 当前规格](../specs/juyiting-ui-baseline-20261006/spec.md)。
