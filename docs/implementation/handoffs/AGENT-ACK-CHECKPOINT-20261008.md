# Agent ACK 高水位检查点优化（2026-10-08）

## 范围与状态

Owner：`ack-checkpoint-owner-20261008` / `critical_worker`。任务：`AGENT-ACK-CHECKPOINT-20261008`。
源码仓库：`/home/isp/wsps/chcbz/isp-install`；独立工作区：`/home/isp/wsps/worktrees/ack-high-water-checkpoint-20261008`。
候选分支：`codex/ack-high-water-checkpoint-20261008`。已自检并快进合入远端组件 `develop`，readback 固定为 `5b71067f7bcbc7ca7f1076f5a9e10321b400785a`；tree 为 `671ebbfc2f211f1113c29a61cd6d25da65990ac5`。最终源码/测试/集成信息见同名 evidence 目录的 `result.json`。

仅改 Agent 客户端高水位持久化、离线迁移工具、安装制品列表及相关测试/文档；未改 ACK wire、服务端或前端。
截至 2026-10-08 实现交付时，运行目录、服务、进程、线上 ACK 队列与旧高水位文件均未修改；没有部署、重启或生产迁移。**实现交付不等于上线或自动释放空间**。2026-10-09 后续授权回收见下节。

## 设计与自检结论

- 新格式 2 不再逐序号留文件。常态保存 `initialized.json` 与 `checkpoint.json`，独立 `ack-sequence.json` 保存匹配的提交栅栏。
- 单个 `intent.json` 保存精确 ACK、前后检查点及完整性摘要，串行入队时持久化后才推进证据。
- 写序：intent → checkpoint → ACK → counter/commit fence → 删除 intent；每次发布同步文件及目录。
- 只允许恢复可证明的写入前缀，不取最大值、不回退旧检查点、不覆盖不同 pending payload。
- counter 已提交的残留/恢复日志不能重建已 dequeue 的 ACK；更旧 intent 与当前高水位冲突必须停止。
- 健康检查、事务恢复、序号分配、FIFO 视图与发送仍位于现有跨进程锁边界。保留持锁后 quarantine 复查。
- 身份、storageId、序号、文件名与 pending duplicate/future 检查保留；异常 quarantine/fail closed。
- 不抢占或自动偷取陈旧锁。真实子进程中断测试确认留锁，只有测试自行确认已退出的自有进程后才在一次性 fixture 中移除锁。
- 哈希用于数据完整性，不是签名/抗恶意重写。重启后的整套一致旧快照仍需独立可信见证才能发现；本任务没有声称提供该能力。
- 未改待发送 ACK、superseded/quarantine 的生命周期；pending 扫描复杂度仍与真实队列长度相关，不声称其也已变为常数。

## 离线迁移与恢复边界

`conf/codex-ws-agent/migrate-ack-high-water.mjs` 随安装制品交付，不会在运行时/安装时自动执行。

1. 发布 Owner 必须先固定版本/源码与目标 profile/Agent 身份，并停止其全部 Writer；不能用热重载代替维护或处理其他聊天的服务。
2. 显式提供 profile 存储 root、Agent ID 与 root 外的唯一 `.jsonl.gz` 备份路径。拒绝 symlink 伪装的内部备份路径/legacy source。
3. 流式压缩完整旧高水位证据，验证 count、maximum、snapshot digest、身份、原计数器与 pending 后才发布迁移日志。
4. 更新检查点、独立计数器及新身份标记后，只回收经完整备份覆盖的旧高水位文件；批量删除结束后统一同步目录，再清除迁移日志，避免按 29.3 万文件逐次 fsync。不清理 pending/quarantine，不激活代码或重启服务。
5. 中断保持 stopped 状态，以相同工具、参数和备份路径恢复。新 runtime 对未完成迁移/旧格式报告 `ACK_OUTBOX_MIGRATION_REQUIRED`。
6. 备份不覆盖；源/备份冲突停止。代码及完整运行状态的回滚需独立恢复安排，不能只还原计数器或将旧 binary 对新格式启动。

## 验证口径

仅运行 Agent Node 单元/集成测试、Bash/JS 语法检查与 diff check；没有本机前后端生产构建，也没有将本地证据称作 Flow 发布证据。
精确 commit/tree、Node 版本、selectors、fixture 摘要及日志路径见 `result.json`；任务证据同步通过 `cyf_orchestrator.py` 注册。

已在干净 `origin/develop` 基线 `4e70c4f` 复现无关失败：
`profile validation rejects equal, nested, and symlink-aliased CODEX_HOME paths` 的 fixture 未配置 typed inspection 网络策略，先触发 `typedInspectionProviderNetwork must be isolated or restricted-proxy`，而非它断言的 HOME 重叠错误。
不改无关功能/fixture。广泛回归显式排除此已归因测试，报告该额外 skip；不得写成“全部客户端测试通过”。
基线中的旧 payload 固定数量断言因本任务安装制品变更一并改为 exact manifest/payload 对比，保留完整性约束而非包大小/数量硬门槛。

### 最终验证摘要

- 新增检查点/故障注入/跨进程并发/离线迁移回归：57/57 PASS。
- 其余 36 个测试文件：638 PASS，10 个既有 skip。
- skills 显式正向名称 allowlist：91 PASS，1 个已归因的基线失败排除。
- 合计 797 个测试：786 PASS、0 FAIL、11 SKIP；不是“无排除全量通过”。
- JS/Bash syntax 与 `git diff --check` PASS。仅使用已声明的 ws 8.21.1 / yauzl 3.4.0 与 Node 20.20.2，未新增依赖。
- 一次性 fixture 分配并出队 128 次 ACK 后：高水位 2 文件，逻辑 482 bytes，分配块 8,192 bytes；独立计数器另分配 4,096 bytes。不是线上实测，也不代表生产已释放空间。
- 未执行前后端构建/Flow 发布、安装、生产数据迁移或服务重启；下一步须固定明确发布版本并安排授权的停 Writer 迁移。

## 2026-10-09 授权存量回收（16:00 CST 核验）

用户明确要求“不等了，直接释放”。Owner 延续本任务；仅处理共享应用数据目录下已退役的吴用 profile 高水位，不发布共享主 Agent、不操作其他任务进程或独立实例。

- 新核验：共享主 Agent 虽仍运行旧代码，但其 `codex-profiles.conf` 自 2026-10-02 起仅配置陆俊义、林冲，未配置吴用；运行中的吴用使用独立 `wuyong-local` 安装及数据 root。不能再以“共享服务运行旧代码”推断退役吴用数据仍有 Writer。
- 目标 root：`/home/isp/apps/codex-ws-agent/data/inbox/6a79742d6a69616665776e6e763538656332333739632d7775796f6e67`。已确认该目标无运行实例写入；迁移工具持有此 root 现行跨进程序号锁，不偷锁。
- 精确校验：292,658 个已提交序号 marker，maximum 与 counter 均为 292,658；另有一个 0-byte legacy 原子写临时文件。最初轻量统计将临时文件计入 legacy 数量，误判冲突；正式逐项核验后纠正，未强行推进冲突状态。第一次回收诊断在遇到未知临时文件时停止，未备份、删文件或改计数器，随后改用现有已验证迁移工具。
- 工具固定源码 `5b71067f7bcbc7ca7f1076f5a9e10321b400785a`（任务独立 worktree，tracked clean）。工具完整压缩备份、校验内容/身份/最高序号后，转换该退役 root 至 format 2，并回收覆盖的旧 marker 与遗留空临时文件；没有迁移或合并独立实例的数据。
- 备份：`/home/isp/baks/ack-high-water/wuyong-legacy-migration-20261009T155127.jsonl.gz`，3,079,530 bytes，SHA-256 `e1dc8e1422afb7a1ddd5285c5bc0d242c982f761c8c14d34383e12a2ec9f54a2`。完整性/恢复摘要见同目录本次 evidence。
- readback：高水位仅 `initialized.json`、`checkpoint.json`；checkpoint 与独立 counter 完全匹配，序号仍为 292,658；无未完成 intent/lock。50 个非高水位/非 counter 文件逐字节摘要不变，包含待发送及其他持久化数据。
- 分配块：操作前 1,214,255,104 bytes，操作后 15,532,032 bytes（主要为原目录保留的目录块）；扣除备份分配块，净释放 1,195,638,784 bytes（约 1.11 GiB）。未额外重建目录来压缩目录元数据。磁盘可用空间约由 745 MiB 升至 1.9 GiB。
- 两个服务 active，PID 保持 2237、324415；无服务停止/重启、运行代码部署或 ACK 发送。共享主 Agent 的运行版本仍为旧版，不能将这次退役目录迁移称为共享代码已上线。旧代码也不能直接重新启用已迁移 root；如重新启用须使用新 runtime，或按完整备份恢复方案处理，不单独恢复 counter。
- 证据：`/home/isp/wsps/cyf/docs/implementation/evidence/AGENT-ACK-CHECKPOINT-20261008/reclaim-20261009/`；`migration.log` 为现有工具成功回执，`before.json` 为非目标文件摘要，`result.json` 为最终 readback、备份摘要和净回收量。
