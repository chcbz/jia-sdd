# RB00：Agent 成果来源与关联审计（2026-09-15）

> 范围：当前 `1.3.0` API/Web 成果目录与取件；`isp-install` 不在范围。本审计只记录当前源码可证明的事实，不能把协议常量、单元测试或计划中的客户端能力描述成线上产物来源。

## 结论

当前 API 已具备 task artifact 的版本、ACL、内容存储和用户 JWT 上传/下载基础，但在当前源码中**没有发现外部 Agent WebSocket 入站消息到 artifact 发布/工作结果提交的已接线生产调用**。

因此：

1. Day 1 可以安全交付“已有 task artifact 的用户目录和精确取件”；它只展示已经存在的可信 `agent_task_artifact` 数据。
2. 不能把 Day 1 宣称为“Agent 工作区文件自动交付”。自动导出不在当前版本范围。
3. 聊天成果入口只能在有可信 `taskId ↔ conversationId` 写入来源时启用；在此之前必须稳定空态，不能按 Agent/persona/message 文本猜测关联。
4. 若产品需要让当前外部 Agent 直接产生新的 artifact，必须另行落实一个服务端入站 bridge 或客户端协议改造；两者均不是本次“忽略 isp-install”范围可以默认假设的已完成能力。

## 已核对源码

| 事实 | 位置 | 结果 |
| --- | --- | --- |
| task artifact 服务 | `api/agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentTaskArtifactService.java` | 有 `publish/get/list/listVersions`，以 `tenantId/clientId/taskId/actorAgentId` 为精确边界 |
| artifact 事务写入 | `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskCollaborationServiceImpl.java` | `publish` 锁 task root、核验访问/版本、写 `agent_task_artifact` 和事件 |
| 工作项结果可原子包含 artifact | `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentWorkItemResultCommitServiceImpl.java` | `commitResult` 调用 `artifactService.publish`，随后 CAS 工作项为 submitted |
| 用户 HTTP 上传/下载 | `api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskArtifactController.java` | `POST /agent/tasks/{taskId}/artifacts` 要求用户 JWT + `actorAgentId`，不应被当作 Agent 自动上传入口 |
| Agent 协议常量 | `api/agent/jia-agent-core/src/main/java/cn/jia/agent/common/AgentProtocolConstants.java` | 存在 `artifact.publish` 常量，不等于 handler 已实现 |
| Agent WebSocket 入站处理 | `api/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java` | `work.result`（非 legacy）与 `artifact.publish` 都进入 `sendDeferredProtocolHandler`；未见发布/结果提交调用 |

非测试源码搜索仅发现 `AgentTaskArtifactService.publish` 的直接调用位于 `AgentWorkItemResultCommitServiceImpl`。未找到将 WebSocket `artifact.publish` 或非 legacy `work.result` 调用该服务的生产接线。

## Day 1 API 实施边界

1. 为 task/bounty 用户提供只读 artifact catalog 与精确 content read adapter；调用者身份只来自用户 JWT，不能让浏览器提交 `actorAgentId` 决定权限。
2. 复用既有 task artifact ACL、版本和存储；不能复制字节、暴露 storage URI 或新建第二个 output 表。
3. 读取错误须 fail-closed 且不泄露 artifact 是否存在；目录/下载失败不影响聊天、任务状态或既有人工上传。
4. 默认只包含已有可读可下载的 artifact；没有 artifact 时返回稳定空集合。

## Day 2 前置事实

聊天成果映射仅在下列事实具备时实施：

- 可信服务端路径在创建/提交 artifact 时同时具备准确 `conversationId`；
- 该 conversation 的参与者 ACL 可由服务端精确查询；
- 映射在同一事务内引用 `(taskId, artifactId, artifactVersion)`，不靠历史回填、标题、Agent 名称或文本内容猜测。

否则，Day 2 不启用聊天入口；Day 1 的 task/bounty 成果目录仍可独立发布。

## 下一步

API Owner 以本审计为 RB00 输入：优先实现 Day 1 task/bounty 只读 catalog。不要为补齐来源而改动 `isp-install`，不要把 deferred WebSocket 消息接线为未经完整身份/租约/幂等设计的生产入口。
