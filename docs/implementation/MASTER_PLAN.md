# 聚义厅多 Agent 协作平台实施主计划

> 基线日期：2026-08-03；模型路由更新：2026-08-17
> 设计依据：`docs/juyiting-multi-agent-collaboration-design.md`
> 当前状态更新：2026-09-06；以下 M2/M3 原始排程与模型名称仅为历史，实时 owner/gate/路由以 TASKS/MODEL_ROUTING 为准。

## 1. 当前目标（2026-09-06）

1. 已交付记录按 `archive/2026-09-06/README.md` 归档，保留所有后续缺陷与生产激活缺口。
2. 案卷阁 CORS 已修复上线，既有 follow-up Owner 完成 authenticated adapter/阅读闭环及屏幕循环，不重复派发 CORS 修复。
3. 语音完成当前 host/API/Web 发布分阶段验收；SILVER/技能/租金 V0 完成 W/R 剩余实现与集成后发布开发预览。
4. M4/M5 仍是未完成规划；完整清单见 `SDD_STATUS_20260906.md`，不能用旧 M2 计划代表当前全部进度。

## 2. 当前模型分工

| 角色 | 模型 | 职责 |
| --- | --- | --- |
| 主控/架构/P0 Writer | GPT-5.6 Sol High | 控制面；身份/ACL/事务/迁移/snapshot 一致性升级和最终门禁 |
| 快速契约 Writer | GPT-5.3 Codex Spark Medium | C05～C07F 冻结契约的 packetized Java/Vue 实施与 focused tests |
| 独立 Test Runner | GPT-5.4 Mini Medium | 串行 targeted/full tests、隔离 MySQL 和证据索引 |
| 只读准备 | GPT-5.6 Terra / GPT-5.4 Mini | 调用链、验收矩阵、冲突和证据准备 |
| 独立 Reviewer/最终门禁 | GPT-5.6 Sol High | 写审分离、P0/P1 Review、C08 GO/NO-GO |

执行策略是**任务/worktree/路径级并行 Writer 流水线**：独立任务可在独立 worktree 按不重叠 owned paths 并行实施；每个任务仍只有一个源码 Owner。Reviewer/Verifier 保持只读，Gradle 与隔离 DB/Rabbit/browser/build 等共享重型资源继续串行或错峰。任务 ACCEPT 后自动推进并主动汇报。

## 3. 里程碑

| 里程碑 | 目标 | 主要任务 | 退出门槛 |
| --- | --- | --- | --- |
| M0 | 设计冻结与风险止血 | A01、A03、B01 | 已完成 |
| M1 | 可靠多人协作 MVP | A02、A04～A08、B02～B09 | 代码已集成；生产迁移/回填未执行 |
| M2 | 可恢复实时体验 | M2-00、C01～C08、C09A/C09W/C09 | 冻结候选 GO，并安全收敛到当前 develop/root pin 候选 |
| M3 | RabbitMQ 可靠传输 | M3-00、D01～D09、M3-RG | 重启、离线、重复投递可恢复；生产激活另行授权 |
| M4 | 自动分派与高级协同 | E01～E08、F01、F02、F06 | 自动组队到验收全流程通过 |
| M5 | 知识检索和生产加固 | F03～F05、G01～G08 | 灰度、压测、安全、监控通过 |

## 4. 历史 M2 依赖链与只读准备流水线

```text
M2-00
  -> C01 -> C01B -> C01H -> C02 -> C03 -> C04 -> C05 -> C05F -> C06
  -> C07A -> C07B -> C07C -> C07 -> C07F -> C08A -> C08W -> C08
```

- 显式依赖链保持不变；依赖已满足且 owned paths 不重叠的任务可并行使用独立 Writer，Explorer/Mini 可继续只读准备。
- 此处记录原 M2 排程；C01B 等后续节点已推进，不再把 C01B 当作当前下一项。
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

## 6. 历史 M3 启动行动（已被后续执行取代）

1. 从 API `cbd4716` / tree `6863d7a` 创建 M3-00 独立 clean worktree并绑定基线。
2. 先验证所有 M3 flags 显式默认关闭、flag-off 零副作用和非法组合 fail-fast。
3. Rabbit 测试只允许 Testcontainers、随机端口/账号/唯一 vhost，禁止连接本机 5672 或远程/生产 Rabbit。
4. M3-00 ACCEPT 前不得启动 D01；仍不部署、不迁移、不操作生产 Rabbit。

## 7. 归档与当前里程碑边界

M1/M2 历史 accepted/integrated 见全量矩阵；D06/D08/D09/M3-IR accepted，M3-RG 有上线记录，但生产 Rabbit 激活/端到端不能由 health 代替。M4/M5 E/F/G 仍待交付。当前源码/验证继续任务级并行，资源冲突仅告警；本次文档归档无任何调度转移。

## 里程碑口径差异（本次显式披露）

历史 `TASKS.yaml.tasks` 将 F03/F04/F05 标为 M4，而 `MASTER_PLAN.md` 里程碑表将知识检索 F03–F05 归 M5。不可修改只读快照来掩盖这个差异。本轮 SDD 展示采用主计划的产品阶段口径：M4=E01–E08、F01/F02/F06；M5=F03–F05、G01–G08；执行依赖和任务身份始终以 exact task_id 为准。该展示裁决不变更台账归属、依赖、Owner 或完成状态，F03–F05 仍未完成；历史元数据统一留给后续独立控制面维护。
