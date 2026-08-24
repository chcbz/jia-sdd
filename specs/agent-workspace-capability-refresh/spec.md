# Agent workspace business capability refresh

## Problem

Agent 的 `abilities` 过去混合了 Persona/Profile 固定配置、已安装 Skill 和工作区技术标签，容易长期停留在 `codex`、`shell`、`debug`、`vue`、`java` 等通用能力。宋江据此无法判断当前接入客户端实际位于哪个项目、能处理哪些项目业务，也无法在客户端切换工作目录后及时调整分配依据。

## Goals

- 每次 `agent.register` 和 `agent.presence` 都根据该 Profile 当前 `codexWorkdir` 重新发现能力。
- 能力发现同时参考当前目录及受限的一层项目容器内容，而不是只看 Skill。
- `abilities` 只上报固定 allowlist 内的中文项目业务能力。
- 完全忽略 Profile `abilities`、Profile `skills` 和已安装 `SKILL.md`，避免固定 Persona 或通用工具能力污染调度依据。
- 支持 CYF 聚合工作区、`jia-*` 业务模块目录和天气示例目录的稳定识别。
- 不上传绝对路径、任意目录/文件名、依赖版本、文件内容或未知能力名称。
- 宽泛 home/host 目录不能证明具体项目业务时返回空能力列表。

## Non-goals

- 工作区能力不是 ACL、生产权限、代码质量或任务可执行性的证明。
- 不递归索引源代码，不构建语义代码搜索、向量库或任意项目名称推断。
- 不将 Codex、Shell、调试、编程语言、框架等通用工具/技术栈作为业务能力。
- 不修改 API/WebSocket schema、数据库字段、身份绑定或任务事务模型。
- 本次不自动迁移历史任务中 `codex`、`strategy`、`execution` 等旧能力要求。

## Scope

- Client：`codex-ws-agent` 工作目录业务能力发现、注册/心跳快照、测试和操作文档。
- API/Web：沿用现有 `abilities` 合同和宋江的能力消费逻辑，无源代码变更。
- SDD：记录识别规则、验证证据、发布快照和仍待升级的外部客户端。

## Constraints and risks

- 扫描必须有目录项、深度和 manifest 大小上限，并拒绝 symlink、TOCTOU、FIFO 和非普通文件输入。
- 只输出固定顺序的中文业务能力 allowlist，避免泄露客户名、仓库名或秘密文件名。
- CYF 聚合识别必须同时具备 Gradle settings 和完整核心模块签名，不能由通用的 `agent/chat/task` 目录误触发。
- 局部业务仓库只接受 `jia-*` 模块前缀，不能把任意同名目录当作 CYF 业务模块。
- API 当前仍按能力字符串精确匹配；升级后的 Agent 不再满足旧英文通用能力要求，相关任务应另行迁移为中文业务能力或不设置能力要求。
