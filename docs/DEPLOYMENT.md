> **2026-10-07 部署路径调整：** 当前 API 实体目录已迁回 `/home/isp/hosts/cyf/api`，旧 `/opt/cyf/service/api` 仅为兼容软链接。同一 JAR、独立 `cyf-api` 身份、Java 21、统一锁、Flow 状态与备份保持不变。部署目录及 `/home/isp`、`/home/isp/hosts`、`/home/isp/hosts/cyf` 均为 root:root 0755，不可恢复为非特权可写。历史 M1/M2 发布说明不因此重新获得执行授权。

# CYF 项目部署说明

> **2026-09-30 健康监控修复：** cron 探测、独立 system.slice 自动恢复及 SMTP 认证错误定位见 `docs/implementation/API_502_HEALTH_RECOVERY_20260930.md`；监控源文件维护入口为 `ops/maintenance/health_monitor/`。13:49 凭据更新后单次邮件已获 SMTP 接受；不应把 SMTP 接受等同收件箱送达。

> **当前默认（2026-10-08）：前端 Flow、后端本地测试/构建/制品部署；develop 不自动部署。发布绑定明确版本、固定 commit/tree、同批制品与在线核验。保留锁、备份、恢复和身份/权限；不另设 Reviewer 或逐次人工门禁。以 `docs/aliyun-flow-cicd-strategy.md` 为准。此次规则调整未构建、部署或重启服务。**


> **执行边界：** 前端复用 Flow `4403172`，禁止本机生产打包或 Flow 失败后的本地回退。后端使用固定源码/独立 worktree 本地构建，不在生产安装目录编译；所有 Gradle 经 orchestrator。现行 API Flow 下载适配器不是本地输入入口，须适配和验证本地制品安装契约后发布，不伪造 Run 或恢复旧源码到生产脚本。完整策略见 [`docs/aliyun-flow-cicd-strategy.md`](aliyun-flow-cicd-strategy.md)。

> ## M1 历史发布约束与当前限制（更新：2026-09-05）
>
> M1 发布流程的固定资源阈值已于 2026-08-28 取消；资源快照仅用于观测，不把旧 5 GiB 阈值作为当前发布阻断条件。
> 后续源码发布前必须先完成 release pipeline 的新安全路径适配与独立验收；资源与数据库快照可参考历史 runbook 第 1 节，但不得直接执行其中旧部署命令。M1 API 禁止从脏 `/home/isp/wsps/cyf/api` 构建。
> `/home/isp/bin/cyf_api_kit.sh` 统一提供已部署 JAR 的生命周期入口；旧 `*_start.sh`/`*_deploy.sh`
> 仅作兼容转发，不再 pull/build。直接 source-to-production 快捷部署已禁用。M1 发布仍只能使用
> `ops/release/` 的 SHA-pinned pipeline，并将唯一允许 source 设为
> `/home/isp/wsps/cyf/.worktrees/m1-integration-api`，expected HEAD
> `c024126ae297f2a8b31c674d8b6530a8f96db556`；发布前必须断言 clean/HEAD，构建并记录 JAR SHA-256。
> codex-ws-agent source 锁定 `/home/isp/wsps/cyf/.worktrees/m1-integration-isp-install`，expected HEAD
> `d1a71ccd46809fdc70716fab1f847ca8a24222ad`。
> 资源观测应覆盖 source、release、backup、deploy、agent backup 所在文件系统；维护窗口、SHA、备份和审批约束不变。
> 完整停写、备份、restore drill、迁移顺序、forward-only scoped UNIQUE、获批 DROP+CREATE 全量恢复和 fail-closed smoke 见
> [`docs/implementation/M1_RELEASE_RUNBOOK.md`](implementation/M1_RELEASE_RUNBOOK.md)。第二轮 release guard 只要求修订该 runbook，API/isp-install HEAD 不变。


## 一、项目拓扑

```
                     ┌────────────────────┐
   用户浏览器 ────> │ kit.chaoyoufan.cn   │  (443)  nginx
                     │ root: /cyf/web/kit  │
                     └────────┬───────────┘
                              │ /api 代理
                              ▼
                     ┌────────────────────┐
                     │ 127.0.0.1:10018    │  Java Spring Boot
                     │ (cyf-api-kit.jar)  │
                     │ profiles: prod     │
                     └────────┬───────────┘
                              │ ws://10018/ws/agent/channel
                              ▼
                     ┌────────────────────┐
                     │ codex-ws-agent     │  Node.js
                     │ agent-client.mjs   │  → codex CLI
                     └────────────────────┘
```

**项目仓库：**

| 项目 | Git 仓库 | 本地路径 |
|------|---------|---------|
| 后端 API | `https://gitee.com/chcbz/jia.git` (develop) | `/home/isp/hosts/cyf/workspace/cyf/api` |
| 前端 Web | `https://gitee.com/chcbz/cyf-web-kit.git` (develop) | `/home/isp/hosts/cyf/workspace/cyf/web` |

---

## 二、服务器环境

| 组件 | 路径/配置 |
|------|----------|
| 后端运行时 | `/opt/cyf/runtime/temurin-21-jre` (Java 21, root-owned) |
| Node.js | `/home/isp/apps/node/bin/node` (v20) |
| Gradle | `/root/.codex/memories/gradle-9.3.1/bin/gradle` |
| MySQL | socket: `/home/isp/apps/mysql/mysql.sock`, port 3306 |
| Redis | 127.0.0.1:6379 |
| Nginx | `/home/isp/apps/nginx` |
| 部署目录 | `/home/isp/hosts/cyf/api` (后端), `/home/isp/hosts/cyf/web/kit` (前端) |

---

## 三、前端 Flow / 后端本地发布与生命周期操作（2026-10-08）

### 后端

正式测试、`validateLayering`、`bootJar` 和唯一制品生成使用本地固定 commit/tree 的干净源码目录或独立 worktree。先读最新相关 `build.gradle`，所有 Gradle 经 `python3 ops/orchestration/cyf_orchestrator.py gradle ...` 串行执行；记录本地 build ID、版本、源码、测试日志及制品 SHA-256。安装仅消费同批已验证制品，保留统一发布锁、备份、原子替换、恢复、`cyf-api` 身份和健康/业务核验。生产 `/home/isp/hosts/cyf/api` 只安装制品，不构建。旧后端 Flow 不再是默认发布入口。现行 `cyf-api-flow-deploy` 依赖真实 Run 下载，本地制品输入需适配与验证；不得伪造 Run 或直接启用旧 pull/build/restart 脚本。

历史云端基线记录：Run `13` / commit `4b94cc252cfaac239c734d96ddcb1370290588e4` / 部署单 `69480251`。这是旧记录，不是当前最新上线证明、后续发布授权或本地 build 证据，不能重复执行旧配置。

生命周期操作与源码发布已拆分。`isp` 用户统一使用 `/home/isp/bin/cyf_api_kit.sh`；该脚本通过
受限 NOPASSWD sudo 调用 root-owned canonical 命令。`/home/isp/bin` 位于 `isp` 可写父路径，只是非特权
便捷入口，不属于 root 信任边界；脚本内的 root 拒绝仅防误用。root/自动化必须只解析并执行
`/usr/local/sbin/cyf-api-kit`，不得执行 `/home/isp/bin` 下的脚本：

```bash
# isp 用户统一入口；无参数默认 restart
/home/isp/bin/cyf_api_kit.sh status
/home/isp/bin/cyf_api_kit.sh start
/home/isp/bin/cyf_api_kit.sh restart
/home/isp/bin/cyf_api_kit.sh stop
/home/isp/bin/cyf_api_kit.sh --help

# deploy 子命令当前 fail-closed，仅输出迁移提示，不执行发布
/home/isp/bin/cyf_api_kit.sh deploy

# root/自动化入口；默认动作是 restart，不拉代码、不执行 Gradle
/usr/local/sbin/cyf-api-kit status
/usr/local/sbin/cyf-api-kit start
/usr/local/sbin/cyf-api-kit restart
/usr/local/sbin/cyf-api-kit stop

# 以下仅为历史/隔离诊断入口，不是当前默认生产发布路径；不要在本机执行真实构建
ops/release/verify-release.sh --input <release-input.json>
ops/release/deploy-api.sh --input <release-input.json> --dry-run
```

`/usr/local/sbin/cyf-api-kit` 使用精确 Java/JAR 进程识别、PID/制品 SHA 运行记录、统一发布锁、
内存/磁盘门禁和 `/actuator/health` 健康门禁；冷启动最长等待 1200 秒。注意当前已安装生命周期核心仍有资源拒绝逻辑，
这与 M1 runbook 的非阻断资源观测不是同一实现；本次仅统一入口，不调整该核心的资源策略。Java 使用 root-owned
Temurin 21 JRE，并降权为独立的 `cyf-api` 账号运行；可信 JAR 与密钥位于 root-owned
`/home/isp/hosts/cyf/api/`，运行记录位于 `/run/cyf-api/`，不会从 `isp` 可写目录执行或写入 root 临时文件。
Jasypt 密钥不暴露给交互账号 `isp`，生命周期日志写入 `/var/log/cyf-api/`。`/tmp` 下的 API 锁和
`/run/cyf-api/` 由 `/etc/tmpfiles.d/cyf-api-locks.conf` 以 root 身份预创建。
旧 `/home/isp/bin/cyf_api_kit_start.sh` 与 `/home/isp/bin/cyf_api_kit_deploy.sh` 仅兼容转发到统一入口；
`deploy` 子命令保持 fail-closed，禁止绕过不可变制品、独立验证、自动回滚和生产审批门禁。
历史 `ops/release/m2-c08*.json` 仍指向旧的 `/home/isp/hosts/cyf/api`
运行路径，不得用于新的 `--execute`；下一次源码发布前必须先将 release pipeline 适配 root-owned JAR、
`cyf-api` 运行身份和 `/run/cyf-api/` 记录路径，并重新独立验收。
`implementation/M1_RELEASE_RUNBOOK.md` 当前仅保留历史门禁与迁移约束，路径适配完成前不可按其中旧部署命令执行。

**JVM 参数：**
```
-Xms128m -Xmx384m -Xss256k -XX:MaxMetaspaceSize=192m -XX:MaxDirectMemorySize=64m -XX:+UseG1GC
```

**启动参数：**
```
--server.port=10018 --server.address=0.0.0.0 --spring.profiles.active=prod
```

### 前端

正式发布使用阿里云 Flow `4403172`：固定发布版本和完整源码 commit，由同 Run 执行 JavaScript 扫描、相关测试、Vite 生产构建、制品上传和主机部署，再在线核验。`develop` 合入/push 不自动部署，不要求转 `master`；按具体版本安排触发，验证成功不等于上线。不在本机打包，不因 Flow 失败转本地构建。

历史云端基线记录：Run `86` / commit `e88425bd5416388e86ff1c1420502c3b571c861f` / 部署单 `69337967`。这是旧记录，不证明当前最新配置或上线状态；当前配置/Run 须实际查询，不能据此新建流水线或恢复旧 webhook。

`/home/isp/bin/cyf_web_kit_start.sh` 不作为源码到生产发布入口；Flow 失败不授权该脚本本地生产构建或部署，本地结果不代替正式 Flow 证据。

### codex-ws-agent

```bash
# 重启 agent（通常随 API 重启后自动重连，手动操作少）
bash /home/isp/bin/codex_ws_agent_start.sh restart

# 查看状态
bash /home/isp/bin/codex_ws_agent_start.sh status
```

---

## 四、常用运维操作

### 查看进程

```bash
# 后端
ps -ef | grep cyf-api-kit | grep -v grep

# 前端（纯静态，无进程）

# agent
ps -ef | grep agent-client | grep -v grep
```

### 查看日志

```bash
# 后端启动日志（仅 root 读取；isp 使用统一入口 status）
ls -t /var/log/cyf-api/startlog_*.log | head -1 | xargs tail -50

# agent 日志
tail -f /home/isp/apps/codex-ws-agent/logs/startlog_*.log

# nginx 访问日志
tail -f /home/isp/logs/access/kit.chaoyoufan.cn.log
```

### 数据库维护

```bash
# 连接 MySQL
/home/isp/apps/mysql/bin/mysql -S /home/isp/apps/mysql/mysql.sock jia

# 查看表结构
SHOW CREATE TABLE chat_conversation;
SHOW CREATE TABLE chat_message;

# 执行迁移 SQL
source /home/isp/hosts/cyf/workspace/cyf/api/chat/jia-chat-mapper/src/main/resources/db/openclaw-channel-migration.sql
```

### 重启 nginx

```bash
/home/isp/apps/nginx/sbin/nginx -s reload
```

---

## 五、数据库变更注意事项

代码中如有新增字段的 Entity，需要同步执行 `ALTER TABLE`。迁移 SQL 文件在：
- `api/chat/jia-chat-mapper/src/main/resources/db/openclaw-channel-migration.sql`
- `api/agent/jia-agent-mapper/src/main/resources/db/ability-evaluation-schema.sql`
- `api/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-schema.sql`（B01 多 Agent 协作表）

### B01 多 Agent 协作 Schema 迁移

该迁移扩展 `agent_task_meta`，并创建 `agent_task_member`、`agent_task_work_item`、
`agent_task_request`、`agent_task_artifact`。首次上线必须先备份数据库、执行迁移，再部署写入协作数据的应用版本：

```bash
/home/isp/apps/mysql/bin/mysql \
  -S /home/isp/apps/mysql/mysql.sock \
  jia < /home/isp/hosts/cyf/workspace/cyf/api/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-schema.sql
```

迁移后验证：

```sql
SHOW CREATE TABLE agent_task_member;
SHOW CREATE TABLE agent_task_work_item;
SHOW CREATE TABLE agent_task_request;
SHOW CREATE TABLE agent_task_artifact;
SHOW COLUMNS FROM agent_task_meta;
SHOW INDEX FROM agent_task_artifact;
```

迁移边界与回滚注意：

- 四张新表的 `tenant_id`、`client_id` 均为非空；`tenant_id` 对应当前 jiacn 逻辑主体，`client_id` 对应 OAuth/API client。
- 历史 `agent_task_meta.tenant_id/client_id` 暂不收紧为非空，也不在 B01 自动回填成员或工作项；历史回填由 B09 单独执行。
- 迁移文件可重复执行缺失字段/索引和 `CREATE TABLE IF NOT EXISTS`，但同名错误索引不会被迁移脚本自动替换；应用启动时 `AgentSchemaInitializer` 会校验关键索引唯一性、列顺序和前缀索引并快速失败。
- 已产生协作业务数据后禁止直接 `DROP TABLE` 回滚。应先停止新写入、导出四张表数据，再回退应用；新增列可保留，不影响旧版本读取。

**历史教训：** `chat_conversation` 和 `chat_message` 表加了 `conversation_type` 等字段但 SQL 未执行，导致 `AgentStatusMonitor` 定时任务抛异常，agent 连接状态无法维护。

---

## 六、部署清单

| 检查项 | 命令/位置 |
|--------|----------|
| 后端进程 | `ps -ef \| grep cyf-api-kit` |
| 后端健康 | `curl -fsS http://127.0.0.1:10018/actuator/health` |
| agent 连接 | `tail -2 /home/isp/apps/codex-ws-agent/logs/startlog_*.log` 含 `connected` |
| 前端页面 | `curl -k -s -o /dev/null -w "%{http_code}" https://kit.chaoyoufan.cn/` |
| nginx | `/home/isp/apps/nginx/sbin/nginx -t` |
| 数据库 | `/home/isp/apps/mysql/bin/mysql -S /home/isp/apps/mysql/mysql.sock jia -e "SELECT 1"` |
| Redis | `redis-cli -s /home/isp/apps/redis/redis.sock ping` |

## 七、常见问题速查

| 现象 | 排查 |
|------|------|
| 前端 500 | nginx 日志 `access.log`；文件权限 `chmod -R a+rX /home/isp/hosts/cyf/web/kit/` |
| agent 连不上 | 检查 `tail -20 /home/isp/apps/codex-ws-agent/logs/*.log`；确认 `curl -I http://127.0.0.1:10018/ws/agent/channel?api_key=...` |
| API 500/502 | root 查看 `/var/log/cyf-api/startlog_*.log`；isp 执行 `/home/isp/bin/cyf_api_kit.sh status`，root 执行 `/usr/local/sbin/cyf-api-kit status` |
| 数据库报错 | 检查断新字段是否已执行迁移 SQL |
| JVM OOM | `dmesg -T \| grep -i oom`；当前上限 `-Xmx384m`，调整前先复核主机资源 |

### A02 持久 Agent 身份 Schema 迁移

> 状态（2026-07-23）：第三轮修复待独立 Review，尚未 accepted/done；本轮未执行生产迁移。
> 以下仅是获批维护窗口的操作手册，不代表当前已获生产执行授权。

A02 新增 `agent_identity_registry`、`agent_identity_alias`，并把现有
`agent_persona_binding` 的 active persona 唯一范围调整为
`(client_id, owner_jiacn, persona_code)`。`owner_jiacn`、binding 生命周期和 alias active key
均使用 generated column；在线 alias 类型仅允许 `LEGACY_AGENT_ID`。

**必须先迁移、后部署应用。** 新版 `AgentSchemaInitializer` 会校验索引列顺序和唯一性；若仍是旧的
`(client_id, active_persona_code)` 索引，应用会快速失败，避免在错误身份约束下启动。

1. 备份数据库，并确认 B01 四张协作表已存在。
2. 检查 `agent_runtime` 是否已有 `owner_jiacn/persona_code/binding_id`。全新当前 Schema
   可直接运行 dry-run；b0 Schema 缺少三列，不能先运行当前 dry-run。b0 必须先在获批维护窗口
   应用第 3 步 fail-closed DDL，再运行第 4 步只读报告；迁移与报告复核完成前禁止写 registry/alias 映射。
3. 执行迁移。迁移只做 DDL，不插入、更新、删除任何历史身份或任务记录，可重复执行：

```bash
/home/isp/apps/mysql/bin/mysql --no-defaults \
  -S /home/isp/apps/mysql/mysql.sock \
  jia < /home/isp/hosts/cyf/workspace/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql
```

4. 运行只读报告并保存完整输出：

```bash
/home/isp/apps/mysql/bin/mysql \
  -S /home/isp/apps/mysql/mysql.sock \
  --batch --raw jia \
  < /home/isp/hosts/cyf/workspace/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-identity-dry-run.sql \
  > /tmp/agent-identity-dry-run.tsv
```

报告门禁：

- 只有 `resolution_status=AUTO_ELIGIBLE` 可进入后续人工复核的 registry/alias 修复清单；本脚本不生成或执行 DML。
- `BLOCKED_MISSING_SCOPE`、`BLOCKED_CROSS_OWNER`、`BLOCKED_MULTIPLE_*`、
  `BLOCKED_RUNTIME_CONFLICT`、`BLOCKED_LINKED_EXACT_CONFLICT`、
  `BLOCKED_TASK_SCOPE_MISSING`、`BLOCKED_TASK_SCOPE_CONFLICT`、`BLOCKED_NO_BINDING` 一律只报告，不得按 persona、displayName、profile 或 ID 前缀猜测。
- task-only/runtime-only 记录不是持久 ownership 证据；历史任务外键回填仍由 B09 执行。
- 历史 binding 的空 `tenant_id` 不等于 owner scope 缺失；owner scope 由非空
  `(client_id, jiacn/owner_jiacn)` 决定，后续 registry 写入必须令 `tenant_id=owner_jiacn`。

5. 迁移后验证：

```sql
SHOW CREATE TABLE agent_identity_registry;
SHOW CREATE TABLE agent_identity_alias;
SHOW CREATE TABLE agent_persona_binding;
SHOW INDEX FROM agent_identity_registry;
SHOW INDEX FROM agent_identity_alias;
SHOW INDEX FROM agent_persona_binding;

SELECT status, lifecycle_status, COUNT(*)
FROM agent_persona_binding
GROUP BY status, lifecycle_status;
```

预期关键约束：

- registry 的 `canonical_type` 仅为 `OPAQUE/LEGACY_CANONICAL/SYSTEM`，生命周期仅为
  `PROVISIONED/ACTIVE/SUSPENDED/RETIRED`，`canonical_agent_id` 全局唯一且保留 RETIRED 记录。
- 非系统 registry 与所有 alias 均要求 `tenant_id=owner_jiacn`；alias 通过复合外键绑定同一
  registry/canonical/scope，不能改变 canonical ownership。
- active alias 唯一键为
  `(client_id, owner_jiacn, alias_type, alias_value, active_key)`，不依赖 nullable `valid_to`。
- active persona 唯一键为 `(client_id, owner_jiacn, active_persona_code)`；active Agent ID 全局唯一。

迁移风险与回滚边界：

- 最大风险是历史中同一 `agent_id` 在多个 client/owner 同时 active。迁移会先创建临时全局唯一索引；
  若冲突则失败且保留旧索引，不会先拆除现有保护。必须依据 dry-run 人工处置，禁止自动改 ID。
- generated column、索引和 CHECK/FK 的 `ALTER TABLE` 可能持有 metadata lock，应在低峰执行并避开长事务。
- registry/alias 开始写入后禁止删除表、物理删除 binding/registry 历史或复用 RETIRED agentId。
  应回退应用但保留身份表与新列；alias 撤销使用 `REVOKED + valid_to`，不能 DELETE。
- A02 不写生产映射数据，不改变 B01 四表，不回填历史任务；后续 B02/B09 只能消费经复核的映射。


## A02 加固触发器部署

迁移脚本 `agent-identity-schema.sql` 末尾新增 4 个触发器（`DELIMITER $$ ... DELIMITER ;`）。
MySQL 客户端执行时如果遇到 `DELIMITER` 语法错误，改用以下方式：

```bash
/home/isp/apps/mysql/bin/mysql -S /home/isp/apps/mysql/mysql.sock jia << 'EOSQL'
source /home/isp/hosts/cyf/workspace/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql
EOSQL
```

触发器功能：
- 阻止 UPDATE 不可变 identity 列（canonical_agent_id, client_id, owner_jiacn 等）
- 阻止 DELETE registry/alias 行（必须用 RETIRED/REVOKED 代替物理删除）
- 阻止 RETIRED → 其他 lifecycle_status（不可复活）
- 阻止 REVOKED → ACTIVE alias（不可重新激活）

MySQL 8.0.21 不支持 `CREATE TRIGGER IF NOT EXISTS`。脚本使用
`DROP TRIGGER IF EXISTS` + `CREATE TRIGGER` 重建四个精确定义，可连续执行；上线前必须在隔离
MySQL 8.0.21 执行两遍并验证 trigger 数量和定义。
## B09 历史任务成员/工作项回填

> 状态（2026-07-29）：B09 已由 `adversarial_reviewer / DeepSeek V4 Pro High` 独立 **ACCEPT**；
> M1 integration release guard 的 trigger-count 缺陷已由
> `c49d148da40bc1f2998954cef27feee7c6b77b57` 修复并在隔离 MySQL 8.0.21 验证；
> 当前 expected API HEAD `c024126ae297f2a8b31c674d8b6530a8f96db556` 追加了聚义厅 @ Agent 归属校验。
> **仍未执行生产回填、未部署；磁盘门禁已临时清理通过，但生产执行仍必须按 M1 runbook 重新过门禁。**

B09 只消费已确认的 A02 registry/alias，不创建身份、不修改 `agent_task_meta`。审批值是数据库按
`BINARY manifest_row_key` 顺序、以固定宽度 SHA-256 链计算的 canonical manifest digest；不是 TSV
文件的 `sha256sum`。approval 会从 LONGTEXT staging 重新校验、解码并计算每行 key/digest 和整批
digest，apply 会再次从 sealed 持久化行计算 digest/行数并与 batch 精确比对。

### 1. 预检资源路径

```bash
CYF_API_ROOT=${CYF_API_ROOT:-/home/isp/wsps/cyf/.worktrees/m1-integration-api}
EXPECTED_API_HEAD=c024126ae297f2a8b31c674d8b6530a8f96db556
test -z "$(git -C "$CYF_API_ROOT" status --porcelain)"
test "$(git -C "$CYF_API_ROOT" rev-parse HEAD)" = "$EXPECTED_API_HEAD"
AUDIT_SCHEMA_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill-audit-schema.sql"
DRY_RUN_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill-dry-run.sql"
MANIFEST_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill-manifest.sql"
STAGING_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill-staging.sql"
APPROVE_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill-approve.sql"
APPLY_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill.sql"
ROUTINES_SQL="$CYF_API_ROOT/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-backfill-routines.sql"

for sql in "$AUDIT_SCHEMA_SQL" "$ROUTINES_SQL" "$DRY_RUN_SQL" "$MANIFEST_SQL" \
           "$STAGING_SQL" "$APPROVE_SQL" "$APPLY_SQL"; do
  test -r "$sql" || { echo "missing/unreadable: $sql" >&2; exit 1; }
done
```

### 2. 从旧三表升级并安装最小权限写入边界

**顺序固定：停写/备份 → 审计 DDL → definer routines → 授权/revoke → 重新导出审批。**
旧三表版本直接执行当前 `AUDIT_SCHEMA_SQL` 即可幂等新增第四张 batch 表；脚本把旧 manifest
对应 batch 标为终态 `LEGACY_UNSEALED`，保留旧 issue/manifest/run 历史但新 apply 永不消费。
脚本可连续执行两遍；旧 approval、旧 run 不能升级为新 sealed 证据，必须在 DDL/routines 完成后重新
导出 manifest、人工审核并调用 v4 approval。

以下示例中的账户名/host 应由 DBA 按环境替换；`cyf_b09_definer` 必须是锁定、不可登录的专用账户，
不能复用 root、应用 runtime 或日常 migration 账户：

```sql
CREATE USER IF NOT EXISTS 'cyf_b09_definer'@'localhost'
  IDENTIFIED BY '<DBA-random-secret>' ACCOUNT LOCK;
ALTER USER 'cyf_b09_definer'@'localhost' ACCOUNT LOCK;
```

```bash
# 1) DBA/root：四表创建/旧三表幂等升级、LEGACY_UNSEALED 隔离、12 个 trigger 精确替换
/home/isp/apps/mysql/bin/mysql --no-defaults \
  -S /home/isp/apps/mysql/mysql.sock jia < "$AUDIT_SCHEMA_SQL"

# 2) DBA/root：以固定 locked definer 安装永久 SQL SECURITY DEFINER routines
/home/isp/apps/mysql/bin/mysql --no-defaults \
  -S /home/isp/apps/mysql/mysql.sock jia < "$ROUTINES_SQL"
```

DBA 对 definer 授予：源表/audit 表 `SELECT`、库级 `CREATE TEMPORARY TABLES`、issue/batch 的
`INSERT,UPDATE`、manifest/run/member/work-item 的 `INSERT`，以及四个 v4 routines 的 `EXECUTE`：

```sql
GRANT SELECT, CREATE TEMPORARY TABLES ON jia.* TO 'cyf_b09_definer'@'localhost';
GRANT INSERT, UPDATE ON jia.agent_task_backfill_issue TO 'cyf_b09_definer'@'localhost';
GRANT INSERT, UPDATE ON jia.agent_task_backfill_manifest_batch TO 'cyf_b09_definer'@'localhost';
GRANT INSERT ON jia.agent_task_backfill_manifest TO 'cyf_b09_definer'@'localhost';
GRANT INSERT ON jia.agent_task_backfill_run TO 'cyf_b09_definer'@'localhost';
GRANT INSERT ON jia.agent_task_member TO 'cyf_b09_definer'@'localhost';
GRANT INSERT ON jia.agent_task_work_item TO 'cyf_b09_definer'@'localhost';
GRANT EXECUTE ON PROCEDURE jia.b09_compute_staging_manifest_digest_v4 TO 'cyf_b09_definer'@'localhost';
GRANT EXECUTE ON PROCEDURE jia.b09_approve_manifest_atomic_v4 TO 'cyf_b09_definer'@'localhost';
GRANT EXECUTE ON PROCEDURE jia.b09_compute_approved_manifest_digest_v4 TO 'cyf_b09_definer'@'localhost';
GRANT EXECUTE ON PROCEDURE jia.b09_apply_manifest_atomic_v4 TO 'cyf_b09_definer'@'localhost';
```

普通 B09 operator/apply 账户仅授予源/audit 的 `SELECT`、`CREATE TEMPORARY TABLES`，以及两个入口
`b09_approve_manifest_atomic_v4`、`b09_apply_manifest_atomic_v4` 的 `EXECUTE`；显式回收：

```sql
REVOKE INSERT, UPDATE, DELETE ON jia.agent_task_backfill_issue FROM '<b09_operator>'@'<host>';
REVOKE INSERT, UPDATE, DELETE ON jia.agent_task_backfill_manifest_batch FROM '<b09_operator>'@'<host>';
REVOKE INSERT, UPDATE, DELETE ON jia.agent_task_backfill_manifest FROM '<b09_operator>'@'<host>';
REVOKE INSERT, UPDATE, DELETE ON jia.agent_task_backfill_run FROM '<b09_operator>'@'<host>';
REVOKE INSERT, UPDATE, DELETE ON jia.agent_task_member FROM '<b09_operator>'@'<host>';
REVOKE INSERT, UPDATE, DELETE ON jia.agent_task_work_item FROM '<b09_operator>'@'<host>';
REVOKE CREATE ROUTINE, ALTER ROUTINE ON jia.* FROM '<b09_operator>'@'<host>';
GRANT EXECUTE ON PROCEDURE jia.b09_approve_manifest_atomic_v4 TO '<b09_operator>'@'<host>';
GRANT EXECUTE ON PROCEDURE jia.b09_apply_manifest_atomic_v4 TO '<b09_operator>'@'<host>';
```

部署后用 `SHOW GRANTS` 复核 operator 没有上述六表 DML、没有 routine/trigger/DDL 管理权限；再由该
受限账户实测 direct INSERT batch/manifest/issue/run 均返回 command denied，而两个入口 `CALL` 成功。
`AgentSchemaInitializer` 会 fail-closed 校验四表关键列、binary collation、索引、PK/auto_increment 和
12 个 trigger 的 table/timing/event/body；括号结构参与匹配，不再被归一化删除。

### 3. 生成并审核报告

```bash
MANIFEST_FILE=/tmp/task-collaboration-backfill-manifest.tsv

/home/isp/apps/mysql/bin/mysql --no-defaults \
  -S /home/isp/apps/mysql/mysql.sock --batch --raw jia \
  < "$DRY_RUN_SQL" > /tmp/task-collaboration-backfill-dry-run.tsv

/home/isp/apps/mysql/bin/mysql --no-defaults \
  -S /home/isp/apps/mysql/mysql.sock --batch --raw jia \
  < "$MANIFEST_SQL" > "$MANIFEST_FILE"

APPROVED_DIGEST=$(awk -F '\t' 'NR==2 {print $1}' "$MANIFEST_FILE")
[[ "$APPROVED_DIGEST" =~ ^[0-9a-f]{64}$ ]]
awk -F '\t' -v d="$APPROVED_DIGEST" 'NR>1 && $1 != d {exit 1}' "$MANIFEST_FILE"
```

归档两份完整 TSV、canonical digest、审核人/变更单和阻断项结论。manifest 每行包含数据库生成的
同一 digest 以及全部 row-digest 输入；不得编辑、重排、追加或删行后继续使用原 digest。

### 4. 原子审批并 seal manifest

staging 所有导入列均为 LONGTEXT；approval 在持久化前显式拒绝超限 utf8mb4、奇数/非法 HEX、
非 canonical 数字/枚举、重复 key、伪 row digest 或伪 batch digest。以下操作必须在同一 session：

```bash
APPROVED_OPERATOR='<审核操作人或变更单号>'
test -r "$MANIFEST_FILE"

/home/isp/apps/mysql/bin/mysql --no-defaults --local-infile=1 \
  -S /home/isp/apps/mysql/mysql.sock jia <<EOSQL
source $STAGING_SQL
LOAD DATA LOCAL INFILE '$MANIFEST_FILE'
INTO TABLE tmp_b09_approved_manifest_staging
FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
IGNORE 1 LINES;
SET @b09_approved_manifest_digest = '$APPROVED_DIGEST';
SET @b09_operator = '$APPROVED_OPERATOR';
source $APPROVE_SQL
EOSQL
```

approval 的 durable DML 位于 DBA 预装的 `SQL SECURITY DEFINER` v4 routine 内，并带 `EXIT HANDLER/ROLLBACK/RESIGNAL`；成功后 batch 从
`LOADING` 单向变为 `SEALED`。sealed batch/manifest 禁止 UPDATE、DELETE，也禁止继续 INSERT append。
即使客户端使用 `mysql --force`，失败后继续解析也不会留下部分 approval。

### 5. 原子 Apply

```bash
/home/isp/apps/mysql/bin/mysql --no-defaults \
  -S /home/isp/apps/mysql/mysql.sock jia <<EOSQL
SET @b09_approved_manifest_digest = '$APPROVED_DIGEST';
SET @b09_operator = '$APPROVED_OPERATOR';
source $APPLY_SQL
EOSQL
```

apply 账户不持有 audit/member/work-item 直接 DML，只能 `EXECUTE` v4 routine。apply 只消费 operator byte-exact 匹配的完整 `SEALED` batch，并在事务快照内验证 sealed 行数、
canonical digest 及当前 source/scope/resolution 双向一致性。issue/member/work item/run 的全部 DML
位于同一带异常处理的数据库原子单元；任一点失败（包括最终 run audit）都整体回滚，`mysql --force`
也不能产生部分业务行或伪 `SUCCEEDED` run。重复成功 apply 不重复业务行，但会新增成功 run 并累计 issue。

### 6. 验证

```sql
SELECT report_sha256 AS manifest_digest, manifest_row_count, seal_status,
       approved_operator, approved_at, sealed_at
FROM agent_task_backfill_manifest_batch
ORDER BY id DESC;

SELECT report_sha256 AS manifest_digest, COUNT(*) AS persisted_rows
FROM agent_task_backfill_manifest
GROUP BY report_sha256;

SELECT run_id, report_sha256 AS manifest_digest, operator, manifest_row_count,
       issue_row_count, member_insert_count, work_item_insert_count,
       run_status, completed_at
FROM agent_task_backfill_run
ORDER BY id DESC;

SELECT issue_code, COUNT(*) AS issue_count, MAX(occurrence_count)
FROM agent_task_backfill_issue
GROUP BY issue_code
ORDER BY issue_code;
```

### 7. 风险与回滚边界

- 安全边界是 locked SQL SECURITY DEFINER + 最小授权/revoke + trigger 关联校验；任何 caller 可设置的 `@b09_*` 变量都不是授权凭据。
- DBA/root、可改 routine/trigger/GRANT 的账号仍可伪造或移除审计保护，明确位于本方案威胁边界之外；不能宣称 trigger 能防住数据库管理员。
- 命名锁只串行化 B09；必须停止普通任务写入后再导出、审批和 apply。任何漂移都应重新导出并审核。
- 多 Agent 历史任务只安全回填 member，不猜测 work-item 拆分；活动任务不伪造 B04 lease。
- 不删除或覆盖 sealed manifest batch/rows、run 或 issue 审计；业务回退仅处理经变更单确认且未被后续业务修改的 `assignment_source='migration'` 行。
- B09 不写 task event；待 C01 后由独立任务补充。

### HTTPS 登录反向代理约束（2026-09-08）

- 应用主配置 `api/starter/src/main/resources/application.properties` 显式保留 `server.forward-headers-strategy=framework`；不能只依赖公共模块的同名资源，应用根资源会遮蔽它。不要为修复登录而删除语音禁用配置。
- API Nginx 各代理 location 清除客户端 `Forwarded`、`X-Forwarded-Prefix`，固定 `Host`/`X-Forwarded-Host` 为 `api.chaoyoufan.cn`，并由边缘覆盖 Proto/Port/For；不能仅在 server 层添加会被 location 指令覆盖的设置。
- 回归：`:starter:test --tests cn.jia.security.LoginForwardedHeadersConfigurationTest`，所有 Gradle 仍须经 orchestrator。
- 上线实测 HTTPS 授权入口正常请求及伪造代理头请求均302至 HTTPS 登录页，登录页200；不跟随未知跳转、不打印或保存 Cookie/token。健康检查200或匿名401不能替代该验证。
