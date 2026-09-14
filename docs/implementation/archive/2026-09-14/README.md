# 2026-09-14 清理与重新分配基线

- 运行台账快照：`reassignment-ledger.json`。它记录了全部 213 项任务的 gate、Owner、精确源码、阻塞原因和下一动作。
- 仅 `done`、`deployed_online_verified`、`deployed_verified` 被归类为“功能闭环”。其余均保留为重新分配或业务验收事项；这特意避免把 `accepted`、`default-off`、`awaiting_business_acceptance` 当作已交付。
- 清理 Git worktree 不删除分支或提交；所有移除均使用非强制 `git worktree remove`，脏 worktree 或运行中的目录会保留。
- 原生客户端兼容候选与 API 当前兼容性验收、以及仍由活动任务使用的启动优化 worktree 不清理。
