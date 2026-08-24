# Agent workspace business capability refresh design

## Runtime contract

每次构建 `agent.register` 或 `agent.presence` payload 时调用 `discoverWorkspaceAbilities(profile)`，并将返回值直接作为 runtime `abilities`：

```text
runtime abilities = discoverWorkspaceAbilities(current codexWorkdir)
```

不再合并以下输入：

- Profile `abilities`；
- Profile `skills`；
- Codex Home、插件或工作区中的 `SKILL.md`；
- `codex`、`shell`、`code-edit`、`debug`、`deploy-assist` 等基础工具能力；
- Vue、Java、Python 等技术栈标签。

因此客户端切换 Profile 或 `codexWorkdir` 后，下一次注册/心跳会自然重建快照，Persona 本身不再固定能力。

## Safe discovery boundary

1. 打开前拒绝 symlink workdir 和非目录路径；打开后使用 `fstat` 的 device/inode 与 `/proc/self/fd` canonical path 再次核对根目录身份。
2. 以目录 descriptor 为锚点扫描工作目录根，以及 `api/backend/client/frontend/packages/server/service/services/src/ui/web` 项目容器的下一层。
3. 根与容器合计最多 512 个目录项；超限、读取失败或子容器无法安全打开时整体 fail closed，返回 `[]`。
4. `package.json` 仍按最多 8 个、单文件 64 KiB、合计 128 KiB 的边界安全读取；读取结果目前不参与能力判定，保留逻辑是已接受的非阻塞清理项。
5. 文件和目录通过 no-follow/non-blocking descriptor 访问，并校验普通文件、目录内容证据，防止 symlink、FIFO 和 TOCTOU 越界。
6. 工作区必须存在项目 manifest、有效 `.git`、Docker/Compose 标记或直接源码文件，才进入业务能力推断；否则返回 `[]`。
7. 输出仅来自固定中文 allowlist，并按固定顺序返回。

## Business recognition rules

### CYF aggregate workspace

聚合工作区必须同时满足：

- 根或扫描到的容器层存在 `settings.gradle` 或 `settings.gradle.kts`；
- 同时存在且非空的精确模块目录：`agent`、`chat`、`task`、`oauth`、`user`、`kefu`、`point`。

满足聚合签名后，才允许将扫描到的精确业务模块目录映射为能力。这样普通项目即使恰好存在 `agent/chat/task`，也不会被误判为 CYF。

### Module-local workspace

局部业务仓库和容器子目录仅接受以下形式：

```text
jia-agent*
jia-chat*
jia-task*
jia-oauth*
jia-user*
jia-kefu*
jia-point*
jia-wx*
jia-sms*
jia-isp*
jia-material*
jia-workflow*
jia-dwz*
```

如果当前 `codexWorkdir` 自身 basename 符合 `jia-*`，也映射对应业务模块。无 `jia-` 前缀的局部同名目录不会单独触发能力。

### Weather workspace

根或受限容器层出现 `weather.py` 或 `weather.html` 时映射为 `天气查询`。

### Canonical business ability allowlist

- `聚义厅协作`
- `智能体管理`
- `智能体调度`
- `会话消息`
- `多智能体协作`
- `任务协作`
- `身份认证`
- `用户体系`
- `客服系统`
- `积分体系`
- `微信生态`
- `短信服务`
- `域名与主机管理`
- `内容管理`
- `工作流编排`
- `短链接服务`
- `天气查询`

其中同时具备 agent、chat、task 三类模块能力时追加 `聚义厅协作`。

## Protocol and scheduling

客户端继续通过现有 `abilities` 字段上报。API 无需变更，`agent_runtime.abilities`、能力名册、recommend、auto-assign 和 assignment validation 会读取最新心跳快照，宋江可据此区分空能力客户端、天气客户端和 CYF 业务客户端。

能力只是调度 hint，不扩大文件系统、API、身份或命令执行权限。API 当前采用字符串精确匹配，因此旧英文任务要求与新中文业务能力不会自动等价。

## Rollout and mixed-client behavior

- 新客户端部署后，等待 register 或下一次 presence 即可刷新，无需修改 runtime 数据库记录。
- 回滚客户端会恢复旧客户端自身的上报行为，但 API 协议不受影响。
- 同一服务可暂时出现新旧客户端混合：已升级客户端上报中文业务能力，尚未升级的远端客户端仍可能上报英文通用能力。
- 不应手工覆盖远端 Agent 的 runtime 行；应升级其实际连接客户端。
