# 1.7.0 实施拆包

2026-09-17；此表是工作拆分，不是第二执行台账。exact Owner/gate只在`docs/implementation/TASKS.yaml#runtime_ledger_json`。任务均由Owner自检，不另起Reviewer。

| 任务 | 责任角色/独占范围 | 输出 | 真实依赖 |
|---|---|---|---|
| V1-7-PLAN-20260917 | 当前主控；本SDD与版本计划增量 | 需求、契约、验收、语音延期 | 无 |
| V1-7-WEB-POLICY-20260917 | balanced_worker；仅新增web/src/utils/economyReadOnlyPreviewPolicy.js及对应Node测试 | capabilities严格接纳、不可交易、scope迟到隔离；首个代码切片 | 本design合同 |
| V1-7-API-READONLY-20260917 | critical_worker；独立API worktree，新增api/agent/jia-agent-service的preview包、读mapper及测试 | 九类入口、纯试算、exact ACL、零写入 | 契约；不等待Web |
| V1-7-WEB-UI-20260917 | balanced_worker；独立Web worktree，新增preview页/composable与router/profile精确入口 | 五分区、移动端、空错状态、只读SDK | 契约即可mock并行，集成前需policy/API |
| V1-7-INTEGRATION-20260917 | 当前主控协调+验证Owner；测试/发布记录 | 双身份/无副作用/旧功能验证、develop集成、本地冻结发布 | API+Web exact candidates；Gradle/发布互斥 |

首轮只启动policy轻量代码和详设；其余包登记ready/planned，不冒充已有Agent正在处理。API/UI启动前登记具体Owner及非重叠路径，router/profile仅UI Owner写。

## 完成口径

- [x] 确认远端develop与既有1.6 release基线。
- [x] 两个语音任务deferred、保留404证据，不阻塞新版本。
- [x] 盘点已有API/Web，不重复开发交易内核。
- [x] 首个policy切片已提交、定向测试通过：`058fe4271b49e9ba4419a8fc6fd58f5dca069287` / tree `823c85842798b992864d1a534f01275ddfcf8cd6`，Owner执行Node定向7/7 PASS。尚未push/合develop/接UI/发布。
- [ ] 新API/页面完整实现并相关测试通过。
- [ ] 集成exact SHA、全部相关回归通过，前后端均合develop。
- [ ] 冻结release/1.7.0及本地制品上线健康通过。
- [ ] 通知用户可验收，按acceptance场景确认。

## 墙钟时间估计（不是传统人天、不是承诺）

以两名实现Owner并行、已有测试环境可复用为前提：契约/首切片约1–2小时；API约6–10小时、Web约4–8小时可重叠；联调/回归/修复约3–6小时；构建部署约1–2小时。合计约12–24小时净执行窗口，异常另报。磁盘增长、真实schema缺口、构建失败或资源锁排队无法在当前证据下量化，单列为等待而非假计代码工时。可将2026-09-18作为条件目标，不承诺所有外部阻塞会自动消失；首轮候选后据实际测试重估。

## 2026-09-17 16:02 执行增量

深度清理完成，原“仅数MiB可用”的构建前问题已解除（清理结果见`docs/implementation/DISK_DEEP_CLEANUP_20260917.md`）。API Owner Shannon与Web Owner Curie已分别claim并开始实现，采用独立worktree；前文“尚未分配”仅为初始快照。实际测试/候选/合入/发布仍需逐项证据，不把开工当完成。
