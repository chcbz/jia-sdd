# Develop integration: preserve WIP, integrate upstream, stop for review

唯一writer：既有/root/r4_recovery_finalize，实际gpt-6.1-sol/high且主控核验/LIVE ACK后执行。串行，不派子代理。不撤销他人编辑。

所有权：以下四个worktree的Git备份/合并及真实合并冲突处理；仅为develop整合。禁止触碰原/home/chc/wsps/cyf及其他worktree的分支/文件。

- Root /home/chc/wsps/cyf-worktrees/multi-region-tenancy，feature/multi-region-tenancy。
- API Root/api，feature/multi-region-tenancy。
- Web Root/web，feature/multi-region-tenancy。
- Runtime /home/chc/wsps/cyf-worktrees/multi-region-tenancy-runtime，codex/multi-region-tenancy-agent-v2。

当前已fetch目标，必须用完整commit合并并证明ancestor：

- Root 01f7599ed28e84c1a44d2cc6c3dec13f7ddbeb67。
- API 73f19a7d599b95438f5fbb3c0bedec63f0789d97。
- Web 5eb117fa3f7a68e9af26ea62d33e5329d603634e。
- Runtime d8fae95b3206c4af4266df1209de29651f895ccb。

## 工作方式

先完整读scope-closeout-20261009.md和各适用AGENTS。重新核四仓HEAD/branch/dirtyset，没有活动writer后才变更。

1. 在/mnt/Workspace使用mktemp -d创建任务专用备份。根盘只剩约307MiB，禁止把备份/构建产物放根盘。记录原HEAD、status、tracked/untracked文件列表；保留全部dirty bytes和删除记录（tar或Git stash及patch可组合），校验备份可恢复。保留原R4产物，不运行旧collector、不清理历史证据。
2. 可以创建可追溯的本地checkpoint提交或stash来保护WIP，但先扫描拟提交路径，不能纳入凭据、host配置、生成build、native binary或私有输出；真实敏感内容不得输出到工具日志。已有删除项/未知相关改动也备份，不悄悄丢弃。
3. 逐仓合并develop。不使用reset --hard/checkout --/clean/无审查全选ours/theirs。真实冲突按语义合并，优先保留upstream新业务以及feature可信tenant范围。上游删除的RuntimeV2平台代码不自动恢复为本次必需；若feature现有依赖需要暂时保留，准确记录为待收敛，不继续新重构。
4. 根gitlinks指向实际整合后的API/Web commits，不错误采用旧Root/develop pins。所有merge至少含确切upstream祖先。保留合并前checkpoint SHA/stash，直到用户验收后再考虑清理。
5. 审查合并结果diff/check、未解决冲突标记、各祖先关系和dirty状态。可以做轻量语法检查；本任务不运行大Gradle/全量测试/服务或数据库操作，不push/publish。后续fresh构建统一flock /tmp/cyf-gradle.lock，产物置/mnt/Workspace。
6. 新增简洁develop-integration-result-20261009.md/json到feature specs，记录backup绝对路径、四仓前后SHA、checkpoint/merge/stash、冲突路径及解决理由、真实命令exit、已保存未集成项。停止写入交独立read-only review。不用大量新的控制协议/审批脚本延长任务。

本任务允许Git整合所需提交，不代表本次功能accepted。无用户阶段确认门禁。收到capacity/error时报告真实状态，不切换模型、不自动重放未知操作。
