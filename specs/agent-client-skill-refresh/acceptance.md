# Acceptance

## Criteria

1. Persona 默认 `planning`、客户端上报 `code-edit` 时，runtime 保存 `code-edit` 而非 `planning`。
2. 旧客户端省略 abilities 时不清空已有 runtime；首次接入可回退 persona。
3. 新增或移除 `SKILL.md` 后，无需修改 persona，下一次 presence 刷新能力快照。
4. `/agent/capabilities` 与宋江 recommend/auto-assign 使用刷新后的 runtime abilities；能力覆盖不完整时不自动分配。
5. 能力声明不绕过既有 API key、绑定和 canonical Agent 身份校验。
6. status/capability 事件按 tenant/client 隔离，并且只在事务提交后发布。
7. presence、unbind 与 assignment 对身份/runtime 使用一致锁顺序，避免撤销后写回或陈旧能力分配。

## Evidence

- codex-ws-agent `npm test`: PASS (97/97)
- codex-ws-agent `OPENCLAW_API_KEY=test node agent-client.mjs --validate`: PASS
- targeted API/Chat Gradle tests: PASS (108/108; `AgentScopePublicationCoordinatorTest`, `AgentStatusMonitorTest`, `AgentServiceImplTest`, `AgentWebSocketHandlerTest`; tree `36848d39845d3b5837d9c967f58551ef7fefabbc`; `/tmp/cyf-gradle.lock` held; `--rerun-tasks`)
- API/client `git diff --check`: PASS
- independent review: ACCEPT (no P0/P1; API commit `4c0f4500eef70f410ffd5e9e477d97943c3dce9b`)
- production deployment: PASS (2026-08-23 CST)
  - API commit `4c0f4500eef70f410ffd5e9e477d97943c3dce9b`; deployed JAR SHA-256 `73d9670b8790d4bdf3998788a80cb4ddad0d6c556de2fe8d318c33ca30176323`
  - client commit `f447069608e0765acfad37ee122551187bdaedfb`; installed client SHA-256 `b36dab72702b4639eadc25d6093fa848e1be0d42045721b6a43543968f56a218`
  - `codex-ws-agent.service`: active after two heartbeat periods; three established WebSocket connections; no continuing reconnect/authentication failures
  - API `/actuator/health`: HTTP 200, `UP`; public site: HTTP 200
  - production `agent_runtime`: 吴用、林冲、卢俊义均 `online` and heartbeat refreshed; all contain `codex/shell/code-edit/debug/deploy-assist`
  - production dynamic discovery: 吴用 runtime has 11 abilities including discovered `imagegen`, `openai-docs`, `plugin-creator`, `review-agent`, `skill-creator`, and `skill-installer`
  - capability/recommendation runtime-source behavior is covered by the targeted API suite above; production smoke confirms the refreshed runtime snapshot consumed by those paths
