# 聚义厅多 Agent 协作平台实施主计划

> 基线日期：2026-08-03  
> 设计依据：`docs/juyiting-multi-agent-collaboration-design.md`  
> 当前里程碑：M1 代码集成完成；进入 M2 基线收敛，生产迁移/回填仍需独立发布任务审批

## 1. 当前目标

完成可恢复实时协作体验：持久 task event、workspace snapshot、SSE replay/resync、前端恢复 reducer 和 TaskWorkspace/Timeline。

完整详设和逐项执行顺序见 `docs/implementation/M2_EXECUTION_PLAN.md`。

## 2. 当前模型分工

| 角色 | 模型 | 职责 |
| --- | --- | --- |
| 主控/集成 | GPT-5.6 Sol High | 任务账本、架构冻结、集成、发布门禁 |
| M2 核心 Writer | DeepSeek V4 Pro High | C01/C01B/C01H、C02～C07A 的迁移、事务、事件、snapshot、SSE、恢复状态 |
| 边界任务 Writer | DeepSeek V4 Flash Medium | 核心任务只读 test/probe；仅 C07B/C 作为纯展示 UI Writer |
| Pro 实现 Reviewer | GPT-5.6 Sol High | 独立只读审查 DeepSeek Pro 代码 |
| Flash 实现 Reviewer | DeepSeek V4 Pro High | 独立只读审查 Flash UI/测试代码 |
| 视觉工具 | GPT Image 2 | 仅 C07 按需生成插画/空状态图，不进入关键路径 |

执行策略固定为：一次一个 active task、一次一个 Writer、一个 worktree 一个 Writer、Reviewer 只读。

## 3. 里程碑

| 里程碑 | 目标 | 主要任务 | 退出门槛 |
| --- | --- | --- | --- |
| M0 | 设计冻结与风险止血 | A01、A03、B01 | 已完成 |
| M1 | 可靠多人协作 MVP | A02、A04～A08、B02～B09 | 代码已集成；生产迁移/回填未执行 |
| M2 | 可恢复实时体验 | M2-00、C01、C01B、C01H、C02～C05、C05F、C06～C07、C07F、C08A/C08W/C08 | snapshot/SSE 可补发、gap resync、UI 恢复、集成门禁 GO |
| M3 | RabbitMQ 可靠传输 | D01～D09 | 重启、离线、重复投递可恢复 |
| M4 | 自动分派与高级协同 | E01～E08、F01、F02、F06 | 自动组队到验收全流程通过 |
| M5 | 知识检索和生产加固 | F03～F05、G01～G08 | 灰度、压测、安全、监控通过 |

## 4. M2 串行执行链

```text
M2-00
  -> C01 -> C01B -> C01H -> C02 -> C03 -> C04 -> C05 -> C05F -> C06
  -> C07A -> C07B -> C07C -> C07 -> C07F -> C08A -> C08W -> C08
```

- M2-00 先保护当前脏 `api/` 主工作树，按对象 SHA 冻结两个 stash，并锁定干净基线和资源门禁。
- C01/C01B/C01H 先完成 event version、全部业务写路径原子事件和历史 baseline；C02～C05 再完成 Broker、replay、snapshot 和 SSE，C05F 冻结后端默认关闭策略。
- C06～C07C 完成前端恢复状态和展示，C07F 冻结前端默认关闭和 M1 降级。
- C07 执行前端子阶段集成；C08A/C08W 分别验证 API/Web 累计 clean base；C08 最终 GO/NO-GO。
- RabbitMQ 属于 M3，不阻塞 M2；M2 始终从 MySQL replay。

## 5. 集成门禁

每个任务进入 `accepted` 前必须具备：

- 唯一 Owner、独立 worktree、范围内 commit。
- 任务级测试和故障注入通过。
- handoff 完整。
- 跨模型只读 Reviewer 明确 `ACCEPT`。
- 无未解释的跨路径修改。

M2 完成必须具备：

- C01、C01B、C01H、C02～C07F 全部 accepted/integrated，C08A/C08W/C08 完成双仓与最终门禁。
- API 联合测试、Web test/build 通过。
- SSE 连接窗口、重复、gap、重启和 resync 场景通过。
- 跨 tenant/client/task ACL 通过。
- Java Long 版本字符串精度测试通过。
- C08 release_guard 输出 GO；生产 DML/部署仍须显式授权。

## 6. 当前立即行动

1. 领取并执行 M2-00；只更新控制面证据，不改 API/Web 业务代码。
2. M2-00 ACCEPT 后，从锁定 SHA 创建独立累计 API/Web base；C01 从 API base 创建，不触碰脏 develop。
3. C01 使用 `deepseek_pro_worker`，由 `sol_reviewer` 独立审查。
4. 每完成一个任务主动汇报，再启动下一项；不并行启动强依赖 Writer。
