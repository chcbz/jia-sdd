# 深度磁盘清理与1.7开发启动 — 2026-09-17

用户授权先深度清理无用worktree及云效产物，再落实开发。只执行本机文件清理；未删除云端原始制品，未重启/终止进程、未改生产数据库或线上代码。

## 执行结果

- 开始15:45根盘50GiB，available=0、100%；不是inode耗尽（inode使用17%）。
- 删除10个已被后续版本替代的本机Flow备份JAR，保留`record.json.backup`精确引用的恢复文件。
- 删除API Run77、Web Run111的旧下载包，分别保留较新的Run78/112；当前记录、当前安装、incoming与云端源未删除。
- 从51个已登记worktree中移除29个已合入或patch等价、tracked/untracked干净、无活动引用的工作树。使用非强制`git worktree remove`；Git分支与提交全部保留。
- 三棵树含Gradle/build生成内容，先保存测试/问题报告压缩包，再清可再生缓存与产物。其余脏树、未合入树、正在使用的树及共享node_modules均保留。
- worktree原分配块约3.33GiB；旧Flow文件约2.34GiB，删除项合计约**5.68GiB**。
- 刚完成删除时`df`约**5.7GiB可用**；16:02两新工作树创建后的可用字节为`5797769216`（约5.40GiB）。全盘空间随并行写入变化，删除项大小与最终净空闲不同。

初次健康检查曾HTTP503；释放磁盘后两次读取HTTP200、UP，无服务操作。这个时序与磁盘压力相关，但未据此宣称已完成该503的全面根因分析。

## 为什么之前会重新满盘

本机累积了重复源码工作树、多份不同版本发布JAR和下载包。既有定时清理仅去除字节完全相同的Flow备份，不会清不同版本或工作树，所以“定时任务执行了”不代表这些积累被处理。开发和日志仍持续写入。

另外，运行中的Codex历史SQLite、会话数据、MySQL数据以及必要开发依赖占空间，但不是可随意删除的垃圾；本轮没有压缩活跃SQLite、删数据库、清共享依赖或未合入代码来凑固定空间目标。保留范围及每次删除摘要已记录。

## 审计与恢复边界

- `docs/implementation/handoffs/DISK-WORKTREE-AUDIT-20260917.json`：51棵树的候选/保留依据。
- `docs/implementation/handoffs/DISK-DEEP-CLEANUP-RESULT-20260917.json`：最终分类计数、字节、健康及开发Owner。
- `/var/lib/cyf-flow-cleanup/deep-cleanup-20260917-bootstrap.json`：磁盘满时首个精确删除回执。
- `/var/lib/cyf-flow-cleanup/deep-20260917/`：逐项intent/result、JAR/package SHA-256、保留引用及三个压缩测试报告。

删除的是已完成checkout和废弃的本机二进制副本，旧worktree可从保留分支重新建立。未把“云效远端仍可立即下载”当已验证事实；远端制品本轮没有操作。没有将这次人工扩大范围偷偷加入定时脚本。

## 开发已分派

- `V1-7-API-READONLY-20260917`：Shannon `01a0ae61-d0b1-71e1-a5da-96f9a2fd17f8`，基于API远端develop `a8e91708`，实现只读namespace、严格scope/Owner ACL与无落库试算及测试。
- `V1-7-WEB-UI-20260917`：Curie `01a0ae62-4349-7960-9c9d-e7e54e78e34d`，基于`058fe427`只读策略切片，新增页面/API适配器和精确入口，复用现存依赖执行定向测试。
- 两Owner独立worktree、非重叠路径；没有独立Reviewer。Gradle和正式构建仍串行，不因“开工”声称已测试/合入/发布。
- 唯一状态以`docs/implementation/TASKS.yaml#runtime_ledger_json`为准。

## 集成时需保留的线上热修复

清理后从当前JAR摘要与部署记录核实：线上API为`4451c30034c1bb31b346ca6b4c0ff6bc7ebb1aca` / tree `b1e5398970d31c838c0e38f8d65aa2f224942fa0`，JAR SHA `8ee8c8cfcbd53bb50f3e8f4b60220fe6310019fa8c983498414073d162666869`。它含目录scope/null引用修复，尚不在远端develop `a8e91708`内。其工作树和恢复副本本轮均保留。已通知API Owner在1.7集成中带上该exact修复，不暂停独立开发，也不覆盖其他任务进程。
