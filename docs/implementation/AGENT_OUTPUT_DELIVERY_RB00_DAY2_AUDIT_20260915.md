# 1.3.0 成果交付 R1 — RB00 Day2 可信聊天关联审计

**日期：**2026-09-15
**审计基线：**API `origin/develop` `36acfb55b4bd1743b280a48864b77bd931c1dc2c`（tree `d6951e59687a8830f5a524e33824e1fdb48ccd38`）
**范围：**只读源码审计；不读生产数据、不接触用户令牌、不运行 Gradle、不部署。

## 结论

Day1 已发布的任务/悬赏成果目录继续可用；**普通聊天入口维持稳定空态**。现有源码能证明一个精确的 `tenantId + clientId + taskId ↔ conversationId` 技术绑定，但不能证明以浏览器 user-JWT 身份读取该聊天会话时，同时具备任务成果读取所需的参与者 ACL。因此本次不把绑定表直接暴露为用户聊天成果接口，也不猜测 user `sub` 与 Agent task member 的对应关系。

这不是成果数据丢失或 Day1 回退：`/agent/tasks/{taskId}/deliverables` 仍让现有服务端 ACL 决定 task artifact 的列表与精确版本内容读取。没有可信聊天映射时，聊天页显示“暂无可领取成果”是 fail-closed 的预期行为。

## 已证实的关联链

1. `chat/jia-chat-mapper/src/main/resources/db/task-thread-schema.sql` 定义 `agent_task_thread`，含 `tenant_id`、`client_id`、`task_id`、`conversation_id`，并有 scoped task/thread 唯一键和 scoped conversation 唯一键。
2. `chat/jia-chat-service/src/main/java/cn/jia/chat/service/impl/AgentTaskThreadServiceImpl.java` 在读取 team thread 时逐项校验 binding scope、活动状态、对应 `chat_conversation` 的 scope/type/key/taskId；其中 conversation 的 `taskId` 必须等于 binding taskId。
3. `chat/jia-chat-mapper/src/main/java/cn/jia/chat/mapper/AgentTaskThreadMapper.java` 的 exact 查询将 tenant/client/task 或 tenant/client/conversation 全部下推 SQL，并做 byte-exact 比较。

故而：对 **Agent task thread** 而言，`taskId ↔ conversationId` 并非文本猜测，技术绑定真实存在。

## 阻断用户聊天成果入口的 ACL 缺口

1. `AgentTaskDeliverableController` 从 `JwtAuthenticationToken` 的 `jiacn`、`client_id`、`sub` 构造 scope，并把 `sub` 作为 `actorAgentId` 传入 `AgentTaskArtifactService`。
2. `AgentTaskCollaborationServiceImpl` 的 artifact `list` 与 `readContent` 均先执行 `requireAccess(... actorAgentId ...)`；读取资格是 task member access，而不只是 tenant/client 相同。
3. `AgentTaskThreadServiceImpl` 的 task-thread 读取也要求 `AgentTaskCollaborationAccessService` 的 Agent member access，且额外使用 `AgentService.requireApiKeyOwnedAgent`。它不是 user-JWT 到 chat-conversation owner 的授权适配器。
4. `ChatConversationServiceImpl` 的普通聊天读取按 `(jiacn, clientId, conversationId)` owner scope 工作；该服务没有在同一调用中证明该 user identity 对应哪个 task member Agent，也没有提供可复用的“聊天 owner + task member”联合授权断言。

直接采用 `agent_task_thread` 查询后调用成果服务，会在没有已定义身份转换合同的情况下把 user subject 当作 Agent ID；这可能错误拒绝，也可能在未来身份命名重叠时造成越权设计。按 R1 范围修订，不能通过猜测弥补此缺口。

## 冻结的后续最小合同（仅在独立工作项中实现）

启用聊天成果入口前，API 必须提供一个单一服务端 read adapter，并在一次调用中完成：

- 从已认证 user-JWT 派生不可由浏览器提交覆盖的 `jiacn`、`clientId`、subject/identity generation；
- 精确验证该 user 是 live `chat_conversation` owner；
- 精确读取同 scope、active 的 `agent_task_thread`，并再次验证 conversation 的 `taskId`、type、scope key；
- 使用明确、已持久化的 user-to-task-participant 授权来源，而不是把 JWT `sub` 猜作 `actorAgentId`；
- 仅返回 `(taskId, artifactId, artifactVersion)` 引用，再复用既有 artifact ACL/content 边界；不复制 bytes、storage URI 或 metadata；
- 任意不存在、scope 不一致、旧 lifecycle generation、撤销 participant 或无映射一律以无泄露的空态/不可用结果结束。

该合同需要一个明确的身份/参与者来源设计和双身份负向回归后才能写入 API。它不属于本次 Day2 审计的可安全自动实现范围。

## Day2 完成状态与下一步

- **RB00：完成（证据结论）** — 可信 task-thread 绑定存在，但 user-chat-to-task-member ACL 尚不可证明。
- **RB04A：不启用聊天映射** — 保持 Day1 Web 空态，不创建 `conversation_deliverable` 或猜测式 adapter。
- **RB01/RB06A：继续** — 仅针对已有私有 storage 的准入/完整性 readback 和可用性回归形成证据；不启用新写入。
- **业务 readback：仍待授权 fixture** — Day1 要求的已有可信 artifact task、授权测试身份和应被拒绝的第二身份/client 仍是唯一可执行的生产业务验收输入。
