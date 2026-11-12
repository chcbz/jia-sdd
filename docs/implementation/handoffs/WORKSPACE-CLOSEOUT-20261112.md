# 分支、worktree、会话及磁盘清理 · 2026-11-12

## 授权与范围

用户要求完整盘点并清理代码分支/worktree、总结与清理Codex历史会话、临时文件及历史备份。范围为当前主机CYF根/API/Web与共享isp-install中的Codex任务分支；不扩展为其他项目、其他主机、生产业务数据/身份、当前会话或活动进程删除。不构建、不部署、不重启服务。

固定起点：根ee2bc63e、API e2e2cbe230、Web60ddd8a、isp-install3897676。四仓先fetch/prune核对。应用列表只有当前CYF主会话活动；两条旧CYF会话闲置。每个待删worktree检查Git状态、独有提交、忽略文件及进程cwd/FD/exe/mmap占用，不以年龄判定可删。

## 已执行

| 项目 | 结果 |
| --- | --- |
| worktree | 删除15个历史工作树，各仓只留主develop工作区 |
| 本地任务分支 | 删除117个codex分支 |
| 远端任务分支 | 删除126个已合入及12个独有候选codex分支；使用固定SHA lease避免误删并发更新 |
| 独有内容 | 删除前生成并验证差量Git bundle，保存两处脏树patch/原文件及独有日志；不代表候选已合入 |
| 会话 | “优化聚义厅资料选择”和“清理磁盘空间”两条旧会话通过应用接口归档；当前会话、其他项目及原始会话库保留 |
| 构建中间产物 | 删除明确build/classes、build/generated、build/tmp等10922个目录，约809.53MiB；不删test-results/reports/最终包/源码 |
| 旧状态备份 | 删除20261111-task-scheduling-runtime1399-retry3/state.tar.gz，726122215字节；保持当前pin及最新两份状态备份 |
| 审计暂存 | 删除上一轮已完成Git审计的3个可重建candidate/resolved目录，原patch和脏文件快照保留 |

旧状态备份是单文件受控删除：持有现有host-cleanup与Runtime发布锁，核对current为verified-active、非当前/最近两份、根拥有且不可被其他用户写、无进程使用、单硬链接，记录SHA及前后身份后unlink。此路径与原清理器拒绝的旧程序目录分开；未修改清理器保护规则。批次写入STATE_ARCHIVE_RETIRED_20261112.json，明确完整状态恢复已不可用，不伪造原receipt。

空间：起始约82MiB可用；收尾df可用3211837440字节（约2.99GiB）、使用95%。净释放约2.9GiB，受服务持续写入影响，不等于逐文件逻辑长度总和。

## 保留与未完成范围（不声称全部清空）

1. Codex工具提供归档，本轮没有物理删除JSONL或直接改在线SQLite；本机会话13份CYF记录含接续副本，未把文件数当作独立会话数。总结见[会话接续](../../../specs/codex-history-closeout-20261023/summary-20261112.md)。
2. 当前/最新两份Runtime状态备份保留。旧程序树现有清理器报告unsafe directory（所有权/布局不符）；未用递归删除绕过。不改权限以迎合清理器。
3. 6份调度Runtime历史包位于嵌套任务目录，既有mark-complete首次返回`task outside explicit bases`，未反复重试、伪造登记或直接删包。仍需按既有归档布局正式迁移/登记后处理，当前/回退绑定仍保护。
4. `/var/tmp`、`baks`并非纯垃圾目录：其中有唯一源码、恢复材料、用户资料、历史测试证据及未明确归属文件，本轮不整目录删除。审计记录、原失败日志、未合入源码差量包不是可丢弃备份。
5. 非codex远端基线/功能分支、其他项目会话不处理；不存在“所有仓库所有分支只剩develop”的声明。

## 证据与恢复

证据根`/home/isp/state/cyf-local-build/tasks/workspace-closeout-20261112/`：

- `worktrees-before.json`、`worktrees-removed.json`、`branches-*-before.json`、`branches-result.json`：固定SHA及逐项操作。
- `branches-*-unique.bundle`、`worktree-*-unique.bundle`：未合入提交的差量恢复材料，均通过git bundle verify；依赖所属仓库已有develop祖先，不是完整仓库备份。用`git bundle list-heads`查原分支，再在对应仓库fetch需要的head。
- `worktree-*-dirty.tar.gz`、patch、ignored-evidence：恢复原脏修改；不把这些覆盖到当前develop。
- `sessions-inventory.json`、权限600的`history-extract-private.json`：本地历史导航/摘录，不提交正文或凭据。
- `intermediates-result.json`、`old-state-delete-{intent,result}.json`、`scratch-result.json`及`result.json`：清理对象、摘要、空间和保留范围。
- `runtime-backups-plan.json`、`cache-plan.json`、`package-registration.json`：旧工具真实跳过/拒绝原因，不将无可删候选重标成功删除。

本轮只维护文档与运维证据；API新修复未部署、扈三娘延后、task648费用待核对等业务状态不因清理而改变。
