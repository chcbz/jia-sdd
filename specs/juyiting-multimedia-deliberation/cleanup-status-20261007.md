# 2026-10-07 历史开发资源清理

已删除与本功能相关的 **61个历史worktree、60个本地分支、10个远端分支**；47个远端分支查询时已经不存在，不重复计为删除。限定本任务历史范围，未清空全项目资源。

删除前核对进程cwd/Owner、fetch/readback、未合入状态；HEAD工作改动/index/untracked分别保存，未合入Git提交以bundle恢复并校验。删除本地ref采用精确SHA比较，远端采用精确lease并readback，不force删除变更远端。

保留：其他Owner活跃api-primary-v3-admission；3个远端因SHA不同于原目标，分别SDD codex/juyiting-multimedia-deliberation（b50bb7ee）、API codex/ac12-text-archive-20261003（de4dd601）、API codex/juyiting-multimedia-deliberation（d85bc64e）。最新SDD已只读导入本轮状态；不因此擅删两个API新提交。吴用、共享Client和API运行进程未操作。

**会话删除0个。** 已询问是聚义厅历史测试会话还是Codex开发会话，尚无回答；不把Git分支等同业务会话、不把归档说成永久删除，不直接清空Codex状态数据库。现有已受理成果/验收/新task426证据保留。

[机器清单](../../docs/implementation/evidence/mmd-shortest-flow-20261007/cleanup-manifest.json)含精确HEAD、删除readback及恢复bundle摘要；实际恢复内容放私有维护目录，不公开凭据/未提交补丁。此前2026-10-05 chcbz旧测试议事清理是独立历史记录，不计为本轮删除。
