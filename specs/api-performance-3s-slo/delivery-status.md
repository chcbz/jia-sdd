# API 3 秒性能治理 delivery status

更新：2026-09-11。

## 当前状态

- 生命周期：`implementing`。
- 已完成：建立跨 API/Web/Ops 的 SDD、3 秒 SLO 分层、声明/运行时双 inventory、首批聚义厅热点、受约束 route registry、operation v1 和验收门禁；独立 `sol_reviewer` R4 delta 已 ACCEPT（P0/P1/P2=0/0/0；R3 两项 P2 已收敛）。
- 实施：PERF-01 离线清单工具、PERF-A01 histogram 基础、PERF-A02 请求日志优化已进入唯一运行台账，由独立 worktree Writer 实施。API 基线为 fresh remote 确认的 `e7da0a435acdff93ae64473223631b3f7d7cbdac`，不使用旧本地 checkout。
- 已验收切片：`PERF-A02-LOG`，API `014fb7edaa53928aa5ca309ea4c8537889763563` / tree `4de32d4ccdb1efe06dd38ee2ff4009532d5300ab`；独立 source + 6 项定向单测 ACCEPT，已 byte-exact 推送 `codex/perf-api-integration-20260911`，未发布。
- 已验收切片：`PERF-A01-HIST`，API `99c8202` / tree `ac02104`，独立 source + 5 项定向测试 ACCEPT0/0/0。与日志切片合并并推送为 `5571d183fe7c612f2d5ebb272548aa5bfad77e90` / tree `b993a925464701b5a17c93461cf3f558036f5d13`；6 个改动文件均与各自 accepted candidate byte-exact，未执行新的合并树完整测试。
- 清单工具：`609cd1c` 虽独立 19 项测试通过，R2 仍被驳回 2 项 P1（非 Controller 命名的自定义注解漏检、清单输入信任边界不足），已进入 `blocked_root_cause`，不得推广或当作全量清单。修复矩阵已记录，尚未认领下一轮。原失败历史保留。
- 未完成：完整模块构建（Gradle 在配置阶段因缺少 repoUsername 失败，未执行模块测试）、全量 route/runtime 清单、隔离环境基线、查询优化、全接口达标和生产发布。
- 当前 checkout 只读静态观察为 42 个 Controller、约 401 条方法 mapping；该数字不是 accepted inventory，必须由 `PERF-01` 在 exact API tree 上确定性生成并绑定 hash。

## 下一门禁

1. 按 `../../docs/implementation/handoffs/PERF-VERIFY-R2-ROOT-CAUSE-20260911.md` 的 PERF-01 R2 矩阵授权有界修复并补充独立负例验收；已 accepted 的 API 两切片不重复审查。
2. 先完成声明/运行时 route inventory、观测和未优化基线，再允许热点源码 Writer 开工。
3. 每个实现候选继续执行 gpt_test_runner 验证、sol_reviewer 独立审查和 release_guard 门禁。

本文件是状态投影，不是第二份执行台账。
