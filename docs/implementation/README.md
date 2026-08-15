# 多模型实施控制台

本目录是聚义厅多 Agent 协作平台实施期间的唯一任务管理入口。

## 文件

| 文件 | 用途 |
| --- | --- |
| `MASTER_PLAN.md` | 当前里程碑、执行链、角色和门禁 |
| `M2_EXECUTION_PLAN.md` | M2 完整详设、Agent 分配、worktree、验收、风险和进度权重 |
| `TASKS.yaml` | 唯一任务账本；状态、Owner、依赖和交付证据以此为准 |
| `COVERAGE.md` | 设计要求到任务、代码和测试的覆盖矩阵 |
| `DECISIONS.md` | 架构决策和接口冻结记录 |
| `MODEL_ROUTING.yaml` | 多模型 Agent 角色、模型路由、写审分离和资源约束 |
| `JUYITING_OCCLUSION_TASKS.yaml` | 聚义厅遮挡 V2 的 23 项串行任务账本、依赖、Owner 和审核状态 |
| `handoffs/TEMPLATE.md` | 实施 Agent 的统一交接模板 |

## 强制规则

1. 没有任务 ID，不允许修改代码。
2. 一个任务同一时间只能有一个实施 Owner；当前全局最多一个 active Writer。
3. 写代码的 Agent 必须使用独立 branch/worktree。
4. Agent 只允许修改任务卡 `allowed_paths` 内的文件。
5. 实施 Agent 只能把任务提交到 `review`，不能自行标记 `accepted/done`。
6. Reviewer 只读；发现问题时驳回，不直接修复其审查的代码。
7. `accepted` 表示单任务验收通过；只有集成验证通过后才能变为 `done`。
8. 任务完成必须记录 base commit、commit、changed files、测试命令、测试结果和残余风险。
9. 依赖未完成的任务不得提前进入 `in_progress`。
10. 设计文档与任务账本冲突时，暂停实施并在 `DECISIONS.md` 记录裁决。
11. 所有 Gradle 命令必须持有 `/tmp/cyf-gradle.lock`。
12. 不得 reset/clean/覆盖当前脏 `api/` 主工作树，不得 apply/pop/drop 已有 stash。

## 状态机

```text
draft -> ready -> claimed -> in_progress -> review -> accepted -> integrated -> done
                   |             |             |
                   v             v             v
                blocked       rejected      blocked
```

补充状态：

- `cancelled`：任务被正式取消。
- `lease_expired`：Owner 超时失联，等待主控检查已有成果后重派。

## 标准执行流程

### 主控 Agent

1. 读取根 `AGENTS.md`、设计文档、`MASTER_PLAN.md`、当前里程碑详设和任务账本。
2. 检查依赖，只把满足条件的任务标记为 `ready`。
3. 原子填写 `owner`、`reviewer`、`lease_until`、`branch`、`worktree`，再允许实施。
4. 保持一次一个 active Writer；可并行的只读审计不得阻塞关键路径。
5. 收集 handoff 和 commit，分派不同模型的独立 Reviewer。
6. 按依赖顺序集成，并执行跨模块验证。
7. 更新 `COVERAGE.md`，确认没有漏项，并主动向用户汇报。

### 实施 Agent

1. 确认任务是 `claimed` 且 Owner 是自己。
2. 阅读任务输入和直接依赖 handoff。
3. 只在独立 worktree 和允许路径中修改，不回滚他人变化。
4. 每完成一个可验证节点更新 progress。
5. 运行任务卡要求的测试。
6. 提交带任务 ID 的 commit。
7. 按模板写 handoff，把状态改为 `review`。

### Reviewer

1. 不使用 Writer 的结论作为事实，只读取任务卡、完整 diff、代码和测试证据。
2. 逐项验证 acceptance、依赖 contract、越界修改、兼容性、并发、安全和迁移风险。
3. 通过则标记 `accepted`；不通过则 `rejected` 并给出可复现问题清单。
4. Reviewer 不直接修复代码。

## Commit 格式

```text
feat(agent): [C01] persist task events with monotonic versions
fix(agent): [C03] resync on replay gaps
feat(web): [C07B] render task workspace timeline
test(agent): [C05] cover task SSE reconnect
```

## 当前执行批次（M2）

```text
M2-00 -> C01 -> C01B -> C01H -> C02 -> C03 -> C04 -> C05 -> C05F -> C06
      -> C07A -> C07B -> C07C -> C07 -> C07F -> C08A -> C08W -> C08
```

- 当前第一项是 M2-00，只收敛控制面、dirty tree、stash、累计 clean base、协议/B09 双状态和资源证据。
- M2-00 ACCEPT 前不得开始 C01 业务代码；M2 全程不直接集成到当前脏 develop。
- M2 的核心 Writer 为 DeepSeek V4 Pro High；Flash 在核心任务只做只读 Test Runner，仅在 C07B/C 作为纯展示 UI Writer。
- RabbitMQ 属于 M3；M2 的 snapshot/SSE 恢复以 MySQL 为唯一事实源。
