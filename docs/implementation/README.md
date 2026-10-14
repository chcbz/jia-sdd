# 多模型实施控制台

## 当前模型分配（2026-10-08，用户明确指定）

- **`gpt-6.1-sol` / high**：主控角色默认、架构、高风险实现，以及跨模块状态、启动恢复、身份/ACL、幂等、事务、并发和迁移任务。
- **`gpt-6-luna` / medium**：契约冻结的常规前后端实现、明确边界小修、代码探索、查询、测试执行与证据整理。涉及上述高风险语义时协调交接给 Sol，不因属于前端而保持低风险分配。
- 新任务只允许以上两个模型；不再路由旧 Terra、Mini、Spark 或其他旧型号，不自动降级。历史角色名保留，但实际模型绑定统一更新。
- 这是用户明确指定的配置策略，不是官方能力对比或项目实测结论。推理档位沿用原角色；实际调用、当前连接可用性与会话重载尚未验证。不可调用时报告准确错误，不静默换型号。
- 3 Writer + 1 只读辅助、线程容量5不变；独立 worktree、路径隔离、Owner 自检不变；Reviewer 与 DeepSeek 提供商继续禁用。
- 本轮仅改配置和文档，不改变活动任务台账，不切换当前主会话模型，不派发开发、构建或部署。唯一模型分配源为项目 `MODEL_ROUTING.yaml#model_selection_policy`。

<!-- SDD delivery reconciliation 2026-09-14 -->
## 历史交付索引（2026-09-14 快照，非当前执行规则）

- 当前 SDD 全量状态与重新分配边界：`SDD_STATUS_20260914.md`。
- 逐项待办静态快照：`archive/2026-09-14/reassignment-ledger.json#reassignmentInventory`；唯一动态 owner/gate 仍是 `TASKS.yaml#runtime_ledger_json`。
- 已按严格交付口径关闭 71/213 项；其余 142 项包括 accepted、default-off、业务验收、用户授权和运行时验证待办，均不可当作已交付。
- 当前执行以根 `AGENTS.md` 为准：每任务一个 Owner、自检后集成；前端正式验证走 Flow，后端本地固定输入构建，develop 不自动部署。历史交付统计不代表今天状态。
- 下文 M2/C09、独立 Reviewer 和历史资源门禁描述为历史过程；若与本段、根 `AGENTS.md` 或 Flow 策略冲突，以最新策略为准。
<!-- END SDD delivery reconciliation -->

本目录是聚义厅多 Agent 协作平台实施期间的唯一任务管理入口。

## 文件

| 文件 | 用途 |
| --- | --- |
| `MASTER_PLAN.md` | 当前里程碑、执行链、角色和门禁 |
| `M2_EXECUTION_PLAN.md` | M2 完整详设、Agent 分配、worktree、验收、风险和进度权重 |
| `M3_EXECUTION_PLAN.md` | M3 RabbitMQ 离线实施、启动门禁、依赖重排、Agent 分配和生产激活边界 |
| `TASKS.yaml` | 唯一任务入口；嵌入式 `runtime_ledger_json` 是当前执行唯一事实源，历史 `tasks` 保留任务定义与归档证据 |
| `COVERAGE.md` | 设计要求到任务、代码和测试的覆盖矩阵 |
| `DECISIONS.md` | 架构决策和接口冻结记录 |
| `MODEL_ROUTING.yaml` | Agent 角色、模型路由、Owner 自检和资源协调 |
| `JUYITING_OCCLUSION_TASKS.yaml` | 聚义厅遮挡 V2 的 23 项串行任务账本、依赖、Owner 和审核状态 |
| `handoffs/TEMPLATE.md` | 实施 Agent 的统一交接模板；不是第二任务台账 |
| `EVIDENCE_CACHE.json` | accepted 验证证据缓存；只按 tree SHA + exact selector + fixture digest 命中 |
| `../../ops/orchestration/cyf_orchestrator.py` | claim/transition/fail/evidence/Gradle/通知的单一可执行入口 |

## 当前并行容量（2026-10-08）

- 以 `MODEL_ROUTING.yaml#execution_policy` 为准：最多 3 个源码 Writer、1 个只读辅助，`.codex/config.toml` 的线程容量为 5；按需使用，不要求占满。
- 每个任务一个 Owner，独立 worktree 与不重叠的 owned paths；共享文件协调交接，Gradle 和共享重型验证仍按现行规则协调，不抢占其他聊天资源。
- 保持 Owner 自检、无独立 Reviewer；下文历史阶段/Reviewer 示例不覆盖当前 `AGENTS.md` 和模型路由规则。
- 本次仅同步容量策略，不修改运行台账中的 owner/gate，不启动开发、构建或发布。

## 强制规则

1. 没有任务 ID，不允许修改代码。
2. 一个任务同一时间只能有一个实施 Owner；不同任务在独立 worktree 且路径所有权不重叠时允许并行源码 Writer。
3. 写代码的 Agent 必须使用独立 branch/worktree。
4. Agent 只允许修改任务卡 `allowed_paths` 内的文件。
5. Owner 核对合同、diff、相关验证证据与残余风险后，经编排入口登记真实验收状态；不创建或等待独立 Reviewer。
6. 只读辅助按需提供调用链和验证准备，不构成单独审批关卡；是否使用辅助不改变任务 Owner 的交付责任。
7. `accepted` 表示单任务验收通过；只有集成验证通过后才能变为 `done`。
8. 任务完成必须记录 base commit、commit/tree SHA、changed files、evidence key、测试命令/结果和残余风险。
9. 依赖未满足的实现不得提前进入 `implementing`；不依赖该结果的已授权切片可继续。
10. 按根 AGENTS.md 和最新合同消解历史说明冲突；仍无法确定当前合同或授权时，仅暂停受影响切片并记录裁决，不因失效 Reviewer 说明停等。
11. 当前执行只读写 `TASKS.yaml` 内嵌运行台账；每个任务顶层只允许 `owner/exact_sha_tree/current_gate/blocker/next_action` 五个字段，历史明细写 handoff。
12. 失败先归因；策略为同根因、同输入连续失败两次停止盲重试。注意当前 `cmd_fail` 按累计次数阻塞，尚未区分输入/根因；记录真实 commit/tree、selector、fixture 和根因，不伪改计数绕过工具，已阻塞时按现有 `authorize-remediation` 处理。本试行不宣称工具已修复。
13. 所有 Gradle 必须经 `ops/orchestration/cyf_orchestrator.py gradle`；入口同时执行 critical-path、owner/current_gate、clean worktree exact SHA/tree、磁盘、全局锁和锁内 evidence HIT 检查。
14. 完成、异常或需要用户处理时，统一入口将结构化 `NOTIFY` 追加到 durable outbox，并可调用 `CYF_ORCHESTRATOR_NOTIFY_CMD`；主控必须主动转达其中的可执行下一步。
15. 不得 reset/clean/覆盖当前脏 `api/` 主工作树，不得 apply/pop/drop 已有 stash。

## 标准执行流程（小功能试行）

1. **固定输入**：只读根 AGENTS.md、任务直接相关合同及 handoff；在现有 handoff 记录目标/非目标、验收、仓库/branch/worktree、base commit/tree。检查本地和集成引用差异，不自动切换或清理他人工作区。
2. **开始实现**：确认唯一 Owner 和路径归属，通过现有编排入口维护状态。小功能不要求通读历史总计划，也不另建审批包；跨仓合同和高风险变更仍按 SDD 要求执行。
3. **尽早反馈**：先选能暴露接口/编译/关键行为错误的定向验证，不等全部实现结束。前端低成本诊断不替代 Flow 正式结果；后端先读相关 build.gradle，在固定干净 commit/tree 上经编排入口串行验证，保留 validateLayering 和必要回归。
4. **自检集成**：Owner 检查 diff、验收、ACL/身份/事务/恢复及任务相关风险；复用精确 tree + selector + fixture 命中的 accepted 证据。允许同一 Owner 以工具支持的 writer/verifier 模式完成验证，不强制换 Agent 或另设 Reviewer。满足证据后经编排入口登记 accepted；集成通过才登记 done，不把它解释成已发布。
5. **连续接续**：阶段结果产生后继续已授权下一步；确需交接时写接收方并确认实际接续。通知 outbox 仅是记录，不是后台唤醒或接续证明。真实阻塞时报告原因、证据和下一步，不为了连续推进扩大授权。
6. **记录效果**：使用现有 handoff 的时间线，分别记录开发与发布等待；阶段未知耗时留空，失败不删。首个真实功能只是试行样本，多个同类任务再比较耗时、返工和缺陷，不新增硬门禁、不预先宣布提速。

运行状态通过 `cyf_orchestrator.py` 写入唯一台账，常规执行使用 `claimed / implementing / targeted_verification / verifying / accepted / done`；失败和授权等待如实登记。历史 `review` 状态保留取证含义，不再作为必须经过的 Reviewer 阶段，也不批量改写旧任务。

## 统一编排命令

```bash
# 校验/查看唯一运行台账与 critical path
python3 ops/orchestration/cyf_orchestrator.py validate
python3 ops/orchestration/cyf_orchestrator.py status
python3 ops/orchestration/cyf_orchestrator.py next

# 失败先归因；现有累计计数阻塞行为见上方规则12，不绕过工具
python3 ops/orchestration/cyf_orchestrator.py fail D06 \
  --category test_failure --summary 'selector failed' \
  --evidence '/tmp/d06.log' --root-cause 'confirmed cause' \
  --remediation 'bounded remediation step'

# blocked_root_cause 后禁止普通 claim；仅主控绑定已批准矩阵开启有界整改
python3 ops/orchestration/cyf_orchestrator.py authorize-remediation D06 \
  --agent <agent-id> --profile critical_worker \
  --commit-sha <40-char-commit> --tree-sha <40-char-tree> \
  --matrix-ref 'docs/implementation/handoffs/D06.md#失败归因矩阵' \
  --next-action 'implement the frozen bounded remediation'

# Gradle 单一入口：clean exact worktree；锁内再查 accepted cache，MISS 才执行
python3 ops/orchestration/cyf_orchestrator.py gradle D06 \
  --cwd /home/isp/wsps/cyf/.worktrees/<task-worktree> \
  --tree-sha <40-char-tree> --selector '<exact selector>' \
  --fixture-digest <digest-or-N/A> -- ./gradlew <tasks/options>

# 完成、异常或需要用户动作时写 durable outbox；也可配置外部投递 hook
python3 ops/orchestration/cyf_orchestrator.py notify D06 \
  --event user_action_required --summary 'summary' --next-action 'one executable action'

# 发现跨任务资源/Writer 冲突时只发协调告警；命令不会改台账或操作进程/证据
python3 ops/orchestration/cyf_orchestrator.py conflict-alert D08 D06 \
  --summary 'D08 is waiting for the active D06 writer' \
  --next-action 'Coordinate with the exact D06 owner and wait; do not preempt.'
```

- 只读 Support 不调用 Gradle；验证由任务 Owner 使用工具支持的 writer/verifier 模式执行。历史 reviewer 模式仍不具备 Gradle 权限，不据此调度 Reviewer。
- critical path 由运行台账数组表达依赖与晋级顺序，不再构成全局 Writer 准入；无未满足依赖的任务可并行 claim。Gradle 仍由全局锁串行，重型磁盘/隔离 DB/Rabbit 资源按门禁协调。
- `/tmp/cyf-gradle.lock` 只负责串行化已获准的 verifier；锁持有者和等待者都不得被其他线程终止。冲突线程只调用 `conflict-alert`，由 exact owner 自主恢复或收敛。
- 本编排入口不提供跨线程进程控制。即使存在 exact thread ownership，任何进程控制仍须用户/主控显式授权，并只能由 exact owner 执行；协调线程不得操作其他任务的进程、Gradle daemon、systemd unit 或证据目录。
- `critical_path_preemption`、`process_preemption`、`automatic_termination` 是非法 blocker category，ledger validator 会拒绝。
- `transition` 到 `accepted/done/blocked_*/waiting_user` 会写入 `/var/tmp/cyf-orchestrator-notifications.jsonl` 并输出主动通知事件；配置 `CYF_ORCHESTRATOR_NOTIFY_CMD` 后同步调用外部投递钩子。

## Commit 格式

```text
feat(agent): [C01] persist task events with monotonic versions
fix(agent): [C03] resync on replay gaps
feat(web): [C07B] render task workspace timeline
test(agent): [C05] cover task SSE reconnect
```

## 历史执行批次（M2，保留原记录，非当前操作要求）

> 以下至文件末尾为旧批次和旧提效规则快照；模型、审查、验证地点和执行顺序均以本文当前流程及根 AGENTS.md 为准。不得用此段重新启用 Reviewer 或增加验证门禁。

```text
M2-00 -> C01 -> C01B -> C01H -> C02 -> C03 -> C04 -> C05 -> C05F -> C06
      -> C07A -> C07B -> C07C -> C07 -> C07F -> C08A -> C08W -> C08
```

- M2 C01～C08 已完成冻结候选与最终门禁；C09A/C09W successor 已 `accepted`。C09 preparation-only 已由 `release_guard` GO；当前启动 M3-00 离线 Rabbit 安全门禁。不得直接合并 dirty `develop/master`。
- C04 等 P0 一致性任务由 Sol Critical Writer；C05～C07F 冻结契约实施由 GPT-5.3 Codex Spark 加速，Sol 负责独立 Review 和最终门禁。
- 当前执行是任务级并行 Writer 流水线：独立 worktree/owned paths 可并行，最多三个只读 Agent 提前准备；ACCEPT 后自动推进，不逐项等待用户确认。
- RabbitMQ 属于 M3；M2 的 snapshot/SSE 恢复以 MySQL 为唯一事实源。M3 必须先完成 M3-00 离线隔离与 flag 零副作用门禁。

## 提效门禁

- 开发阶段只跑 targeted/touched tests；最终 candidate 由 Test Runner 跑一次模块全量。
- schema/migration/transaction 最终 tree 只跑一次隔离 MySQL。
- 证据键：`git tree SHA + test selector + DB fixture digest`；匹配时直接复用。
- no-ff merge 无冲突且 tree byte-exact 时只核对 SHA，不重复完整代码 Review。
- 自 2026-08-28 起取消固定内存/磁盘 admission gate；资源快照继续记录，Gradle、隔离 MySQL/Rabbit、npm build 和重型磁盘操作仍全局串行，真实 OOM/ENOSPC 必须归因。
