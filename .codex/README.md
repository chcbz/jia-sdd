# CYF multi-model agents

## 当前模型分配（2026-10-08，用户明确指定）

- **`gpt-6.1-sol` / high**：主控角色默认、架构、高风险实现，以及跨模块状态、启动恢复、身份/ACL、幂等、事务、并发和迁移任务。
- **`gpt-6-luna` / medium**：契约冻结的常规前后端实现、明确边界小修、代码探索、查询、测试执行与证据整理。涉及上述高风险语义时协调交接给 Sol，不因属于前端而保持低风险分配。
- 新任务只允许以上两个模型；不再路由旧 Terra、Mini、Spark 或其他旧型号，不自动降级。历史角色名保留，但实际模型绑定统一更新。
- 这是用户明确指定的配置策略，不是官方能力对比或项目实测结论。推理档位沿用原角色；实际调用、当前连接可用性与会话重载尚未验证。不可调用时报告准确错误，不静默换型号。
- 3 Writer + 1 只读辅助、线程容量5不变；独立 worktree、路径隔离、Owner 自检不变；Reviewer 与 DeepSeek 提供商继续禁用。
- 本轮仅改配置和文档，不改变活动任务台账，不切换当前主会话模型，不派发开发、构建或部署。唯一模型分配源为项目 `MODEL_ROUTING.yaml#model_selection_policy`。

Project-scoped Codex agent roles are defined in `.codex/agents/*.toml` and registered by `.codex/config.toml`.
Model routing and the path-scoped parallel execution policy are recorded in `docs/implementation/MODEL_ROUTING.yaml`.
The active M2 plan is `docs/implementation/M2_EXECUTION_PLAN.md`.

Current policy (updated October 8, 2026):

- up to three active source Writers on independent tasks/worktrees with non-overlapping owned paths;
- up to one read-only support Agent; thread capacity is five, with coordinator headroom;
- one source Owner per task/worktree; use slots on demand, not merely to fill capacity;
- each Owner self-checks; independent Reviewer roles remain disabled, even if historical registrations exist;
- shared paths require coordinated handoff; never overwrite another Owner's changes or preempt their processes;
- Gradle is serialized with `/tmp/cyf-gradle.lock`; shared verification resources and releases remain coordinated;
- formal frontend tests, builds and versioned releases use Alibaba Cloud Flow; backend tests, builds and versioned releases use the local path (2026-10-08); develop does not deploy automatically; immutable artifact, lock, backup/recovery and online verification remain required;
- production data changes and operations outside the authorized frontend Flow / backend local release scope retain their existing authorization and recovery requirements;
- this capacity change does not dispatch Agents, change current task ownership, restart services, or authorize a release.
