# M1 API + isp-install 串行集成交接

## 1. 最终状态

- Writer：GPT-5.6 Sol High，当前唯一写入者。
- Reviewer gate：`release_guard` / GPT-5.6 Sol High，只读且与 Writer 工作阶段分离。
- API branch/worktree：`feat/m1-integration-20260728` / `/home/isp/wsps/cyf/.worktrees/m1-integration-api`。
- API initial integration gate commit：`0907762eb6578987d1765c3f16dddeed0e545a45`。
- API release-guard fix / final HEAD：`c49d148da40bc1f2998954cef27feee7c6b77b57`。
- isp-install integration final HEAD：`d1a71ccd46809fdc70716fab1f847ca8a24222ad`。
- 两个工作树最终 clean；B08 `stash@{0}` 未 apply/pop/drop。
- 未部署、未重启生产服务、未连接生产 MySQL、未执行生产 DML。

## 2. 集成内容与冲突处理

- API 串行集成 B08 initial、A08、B08 hardening、B07、B09，并手工合并：
  - `AgentSchemaInitializer` 同时保留 A08 identity 与 B09 audit validation；
  - `AgentServiceImpl`、identity DAO/service 同时保留 A08 runtime、B08 compatibility/historical persisted-reference、identity locks；
  - `schema.sql` 与 initializer 安全迁移 source schema 可能存在的 global `UNIQUE(task_id)`，目标为 `UNIQUE(tenant_id, client_id, task_id)`；
  - B07 task-thread ownership、ACL 与 byte-exact message scope 全部保留；
  - B09 sealed audit schema、definer routines 与 12 个 exact trigger 全部保留。
- isp-install 串行集成 A07 七个提交；冲突保留 base `168ad60` 每个 Agent profile 的 `codexModel`。
- archive/quarantine worktree 保留；未引入 `git worktree remove/prune`。

## 3. 第一次 release_guard：REJECT

第一次独立 release guard 在 2026-07-29 判定 **REJECT**，发现：

1. **P2 code**：`backfillAuditTriggerCount()` 使用不存在的 `trg_task_backfill_manifest_update_guard`、`trg_task_backfill_run_update_guard`，可能在四张空 audit 表仅保留两个合法 `no_update` trigger 时误判为零并重复 bootstrap。
2. **P0 ledger**：A07/A08/B09 已独立 ACCEPT，但 `TASKS.yaml` 与 handoff 未闭环。
3. **P1 release gate**：缺少锁定 clean integration worktree 的构建路径、完整备份/restore drill、forward-only scoped UNIQUE 回滚边界和 M1 smoke 手册。

## 4. 本轮关闭

- `c49d148da40bc1f2998954cef27feee7c6b77b57` 修正两个 trigger 名称。
- 新增隔离 MySQL 8.0.21 回归：初始化完整 schema 后只保留两个合法 `no_update` trigger，第二次 initializer 必须 exact validation 失败并保持仅两个 trigger，证明未重复 CREATE。
- 更新 `TASKS.yaml`，将 A07/A08/B09 置为 accepted，恢复 owner/writer model、独立 reviewer、commit、tests、files、handoff 与 progress 证据。
- 新增 A07/A08/M1 handoff，最终化 B09 handoff。
- 更新 `docs/DEPLOYMENT.md` 并新增 `docs/implementation/M1_RELEASE_RUNBOOK.md`，锁定构建来源、磁盘/备份/restore/迁移/回滚/smoke 门。

## 5. 本轮验证

所有 Gradle 命令均使用 `/tmp/cyf-gradle.lock`、`--no-daemon`、单 worker、`-Xmx384m`。

- `AgentSchemaInitializerTest` 定向：PASS。
- `AgentSchemaInitializerMySqlTest`，隔离 MySQL 8.0.21：4/4 PASS。
- 完整 `:agent:jia-agent-mapper:test`：66 PASS。
- 完整 `:agent:jia-agent-service:test`：333 tests，15 个环境条件测试跳过，0 failures/errors；MySQL 条件 initializer 测试已另行实库执行。
- `git diff --check`：PASS。

## 6. 发布状态与残余风险

- 当前 `/dev/vda1` 可用空间约 `2.2 GB`，低于 M1 runbook 的门槛；**生产备份、迁移和部署仍为 BLOCKED**。
- 发布必须由新的独立 release guard 再审本轮 commit 和 runbook；本 handoff 不等于生产授权。
- scoped UNIQUE 是 forward-only schema boundary；一旦跨 scope 复用同一 task ID，不得仅回滚旧应用并重建 global unique。
- B09 definer/GRANT/REVOKE 与 A08 legacy identity apply 仍需 DBA/人工审批，不可由应用启动隐式代替。

## 7. 第二次 release_guard：仅 Runbook REJECT，代码与验收记录 CLOSED

2026-07-29 第二次独立 `release_guard` 明确确认 API 代码修复及 A07/A08/B09 验收台账已经关闭，只拒绝 `docs/implementation/M1_RELEASE_RUNBOOK.md`。本轮 Writer 未修改 API/isp-install HEAD，仅修订获准发布文档，关闭：

1. task-thread smoke 不再固定 `senderName`：普通非 system persona 注册后 fail-closed 解析服务端 canonical Agent ID，再查询并解析实际 `name/personaName`，append/list 强制使用并验证同一实际 sender；正负响应均严格解析 JSON envelope。
2. 停写真正可执行：以精确 JAR argv 匹配并 `TERM` 停止 API、使用实际 agent service stop 脚本，断言进程与端口消失；SQL 排除当前只读检查 session 后计算 active modifying transaction count 与 modified rows，shell 强断言两者为零。
3. 增加获批完整灾难恢复：所有危险块要求 `M1_APPROVE_FULL_RESTORE=YES_I_UNDERSTAND_DATA_REPLACEMENT`，先停服务并保存失败现场，再校验完整 dump，按原 charset/collation `DROP + CREATE` 精确生产 schema 后恢复；核验 schema、row counts、checksum、关键表，恢复旧 JAR 与 agent tar/config，并恢复或撤销 B09 definer/operator 的 mysql 系统账户与 grants 后启动旧栈 smoke。
4. 磁盘门禁移为第一项：任何 Gradle/npm/dump/tar/备份前，对 API source、release、backup、API deploy、agent backup 的每个不同文件系统检查 `max(5 GiB, 2*estimated DB + reserve)`；不存在路径使用最近存在父目录。当前约 2.2 GiB 仍明确 BLOCKED。
5. dump 内容 fallback 改为 `gzip -t` 后由 `awk` 完整消费 gzip 流，不再使用可能在 `pipefail` 下触发 SIGPIPE 假失败的 提前退出的单命中搜索 pipeline。
6. 对 Markdown shell blocks 执行逐块 `bash -n`，并静态检查 fence、危险 restore gate/变量、固定 senderName、尾随空白和两个集成工作树 HEAD/clean。

本轮没有连接生产 MySQL、没有执行维护窗口命令、没有部署或重启生产服务。API 仍为 `c49d148da40bc1f2998954cef27feee7c6b77b57`，isp-install 仍为 `d1a71ccd46809fdc70716fab1f847ca8a24222ad`。

## 8. 第三次 release_guard：仅 Runbook REJECT，代码 HEAD 继续冻结

2026-07-29 第三次独立 `release_guard` 继续只拒绝 `docs/implementation/M1_RELEASE_RUNBOOK.md`；API 代码、isp-install 和 A07/A08/B09 验收记录仍为 **CLOSED**。Writer 仅修订发布文档，关闭：

1. 所有完整恢复 prerequisite 均在首个 schema migration 前创建并校验：旧 JAR、完整 agent app/config tar、checksum 锁定的旧 API JVM/app argv、`BASE_URL`/Auth curl 数组、旧版本只读 smoke Agent、精确启停/停写/恢复审批函数及数据库证据；恢复旧栈时从锁定文件重新加载 argv 并重建 curl 数组。
2. agent writer 门禁遍历 `/proc`，对 node argv 中 `agent-client.mjs` 的绝对路径直接 `realpath`，相对路径按 `/proc/$pid/cwd` 解析，并在 cwd 消失竞态时 fail-closed；任意重复 writer 阻断，wrapper 不能替代该断言。
3. 第一磁盘门禁同时覆盖 `AGENT_SRC` 与 `AGENT_APP_DIR`，连同 API source、release、backup、API deploy、agent backup，对每个不同 filesystem 去重检查并保留全部路径映射证据，覆盖后续 Gradle/npm/dump/tar 写目标。
4. restore drill 使用显式 14 表 `PRESENT|ABSENT` manifest，对生产 PRE 与隔离 restore 生成同格式 exact row-count TSV 并 `cmp`；完整灾难恢复复用同一基线和动态 `CHECK TABLE` 集合，不再硬编码可能被标记 `ABSENT` 的表。
5. 增强迁移前静态时序门：恢复依赖变量、函数、checksum 和路径必须早于首个 migration 定义/校验，迁移后不得重新定义关键 rollback artifact；Markdown bash/Python/fence/危险变量引用均执行静态检查。

本轮未修改 API/isp-install HEAD，未连接生产 MySQL，未执行 runbook 命令，未部署或重启生产服务。API 保持 `c49d148da40bc1f2998954cef27feee7c6b77b57`，isp-install 保持 `d1a71ccd46809fdc70716fab1f847ca8a24222ad`。
