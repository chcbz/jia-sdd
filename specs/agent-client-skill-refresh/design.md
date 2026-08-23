# Design

## Protocol

`agent.register` 和 `agent.presence` 均可携带：

```json
{"abilities":["codex","code-edit","cyf-quick-iterate"]}
```

- 字段缺失：保留已有 runtime 快照；首次注册回退 persona 默认值。
- 显式空数组：客户端声明当前无能力。
- 非空数组：trim、大小写无关去重，最多 128 项、单项最多 100 字符、拒绝控制字符。
- WebSocket API key、agentId、clientId、owner jiacn 既有身份校验保持不变。
- abilities 只接受字符串数组；对象、标量、null 元素和空白元素 fail closed。

## Client discovery

每次注册及心跳重新合并：

1. Codex 客户端基础能力；
2. profile 的 `abilities` / `skills` 配置；
3. `<CODEX_HOME>/skills/**/SKILL.md`；
4. `<CODEX_HOME>/plugins/cache/**/SKILL.md`；
5. `<workdir>/.codex/skills/**/SKILL.md` 与 `<workdir>/.agents/skills/**/SKILL.md`。

读取 YAML frontmatter 的 `name`，无 `name` 时使用技能目录名；单文件仅读前 8 KiB。四个扫描根各有独立条目预算和固定 manifest 配额，避免插件缓存耗尽预算后饿死工作区技能。

## Runtime and scheduling

`agent_runtime.abilities` 是客户端当前能力快照。`/agent/capabilities`、任务推荐、自动分配和 assignment validation 沿用该字段，因此无需新增响应结构。`agent_persona.abilities` 仅保留目录展示和兼容 fallback 语义。

presence 先按 binding/identity 全局顺序加锁，再锁 runtime；assignment 沿既有 task → identity 顺序写入 compatibility aggregate 后，再锁 runtime 快照校验，失败则整笔事务回滚。status/capability 事件捕获显式 tenant/client scope 并在 after-commit 后仅广播给同 scope 会话。
