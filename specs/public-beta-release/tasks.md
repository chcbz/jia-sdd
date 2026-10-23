# 公共公测发布与安全整合 — 任务

任务级实施/审核/验证由 `docs/implementation/TASKS.yaml#runtime_ledger_json` 唯一管理；不在此派发第二份 Owner。

## 剩余交付

- [ ] 关联 exact API/Web 安全修复与实际部署 artifact
- [ ] 账号/迁移及 credentialed 浏览器安全验收
- [ ] 实际用户 onboarding 可用性与隔离验证
- [ ] 记录公测 release baseline 后才关闭整体需求

完整快照映射见 [delivery-status.md](delivery-status.md)。历史定义中未进入当前运行台账的任务仍是规划，不擅自启动。

## 仓库分工（角色，不是第二份执行认领）

| 仓库/职责 | 路由 | 边界 |
| --- | --- | --- |
| API | critical_worker | 身份/ACL/事务/后端核心；exact task owner 读取运行台账 |
| Web | balanced_worker | 冻结合同下交互与前端集成；不得修改 API owned paths |
| 集成/归档 | main_orchestrator | 不重置脏主树，不覆盖其他任务认领 |
| 验证 | gpt_test_runner | exact tree/selector/fixture；重型资源串行 |
| 独立审查 | sol_reviewer | 只读，不预实现或修复 |
