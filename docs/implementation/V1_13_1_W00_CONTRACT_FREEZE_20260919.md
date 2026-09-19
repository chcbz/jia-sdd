# 1.13.1 W00 合同冻结：真实调用链与实施边界

日期：2026-09-19。基线：API `0562bdeac74d0d103e001e603f3ebc7ea0e3f798`（tree `e183de7fd710c660022fe5e95755bb71c13c06f7`），Web `fa1b6e20e4ef99ff9fb31e9fa2f6802f5176035d`。本文件冻结 W01–W04 的接入边界；它不表示功能已实现，也未执行 Provider 或外发用户资料。

## 1. 已验证的当前事实

### 1.1 私人工作空间执行并不是悬赏执行

`PersonalWorkspaceExecutionController` 接受 `taskId`、`conversationId`，但 `PersonalWorkspaceExecutionServiceImpl#create` 仅：

1. 以 tenant/client/owner 检查目标 Agent 与可选 task file-link 所属；
2. 创建 `pwe_*` task/run 命名空间和版本固定的输入快照；
3. 由 runtime-only `GET /internal/agent/tasks/workspace-executions/commands` 派发 `WORKSPACE_FILE_EXECUTE`；
4. runtime 通过受控 internal 路径下载输入、stage 输出、commit manifest；
5. `commitOutputs` 仅把输出归档成 owner 的 `AGENT_DELIVERY` 工作空间文件版本。

它不创建/领取 task work item、没有实际 work-item lease、没有 task artifact、没有 formal delivery，也没有会话成果投影。因此 `pwe_task_*` 绝不能被当作业务 taskId 或正式交付来源。

### 1.2 当前任务进入正式交付的有效链

任务的真实链为：

```text
POST /agent/tasks/{taskId}/assign
  -> AgentLegacyTaskCompatibilityService.assignResolved...
  -> task member + default required work item(READY)

AgentWorkItemLeaseService.claim -> CLAIMED
AgentWorkItemLeaseService.start -> RUNNING
  -> 必须为任务成员、规范 Agent 身份、未过期 lease、精确 work item version

AgentTaskArtifactService.publish / AgentWorkItemResultCommitService
  -> task-scoped artifact + work item 提交 CAS

[feature flag jia.agent.formal-delivery.enabled=true]
AgentTaskFormalDeliveryService.submit
  -> 仅一个 required work item、RUNNING lease、producer/run、artifact hash/version
  -> task REVIEWING / formal delivery SUBMITTED

AgentTaskFormalDeliveryDecisionService
  -> accepted / changes_requested 的唯一正式决定
```

浏览器不得取得或提交 lease token；不能用私人 runtime 成功回执伪造上述任一步。W02 的任务模式必须在服务端创建/持久化一次执行记录后，复用这个链；runtime 的 `AgentRuntime` 凭据只用于领取其已授权输入及提交该执行的字节结果。

### 1.3 会话范围及模块方向

- `ChatConversationService#getOwned`/`findOwnedMessages` 只允许**非 task-thread**的 owner 私人会话；不能用于 team task thread。
- `AgentTaskThreadService` 能验证 task member 与 team-thread 的绑定，但调用者需要 `actorAgentId`，且它是 chat-service 内服务。
- `JuyitingConversationScopeService` 可根据 task 的可写成员冻结聊天发送范围，但它是 UI/chat-send 授权逻辑，不是可供 agent 执行服务调用的持久化 scope port。
- Gradle 方向为 `chat-service -> agent-service`，而 `agent-service` 当前不依赖 chat API；直接注入 chat-service 会形成不正确的反向模块关系。

**冻结决定：**在 `chat:jia-chat-api` 新增窄的 `WorkspaceConversationAccessService`（或语义等价名称）端口；`chat-service` 实现它，`agent-service` 只依赖 `chat-api`。该端口只能返回经过 tenant/client/owner 校验的会话事实：`conversationId`、scope type/key、可选 business taskId、固定 target agent 集、lifecycle/revision；不得返回消息正文，不能以前端 metadata 或 conversationId 自行推导 owner。task-thread 情况复用其已存在的强绑定；私人 Juyiting conversation 情况复用严格 owner scope；泛化普通会话不能绕开已存在 task-thread 拒绝规则。

### 1.4 runtime 与客户端边界

`AgentRuntimeAuthenticationFilter` 只允许明确的 native credential lane 路径；当前文件桥客户端只接受严格的 `WORKSPACE_FILE_EXECUTE` input/output manifest，并把 `AgentRuntime` token 保留在进程内。浏览器 JWT、URL 参数、Chat metadata、文件 storage URI 都不能变成 runtime/producer/lease 授权。

**冻结决定：**W02/W04 如复用文件桥，扩展的 command/commit 语义仍须：

- 以 runtime 认证的 `tenant/client/owner/agent/runtimeInstance` 查找精确 execution；
- 不把 lease token、storageUri、Provider 凭据下发到浏览器或 durable prompt/inbox；
- 由服务端的任务执行编排保存 lease/producer/run 对应关系，并在 runtime commit 时复核 target Agent、输入快照、输出 hash 和状态；
- 若 runtime 客户端协议增加业务 task/work item 字段，字段只作关联/去重；是否可以正式提交仍由服务端查 execution + current lease 决定。

### 1.5 存储与成果投影

workspace version 由 owner scoped file/version 表与 `PersonalWorkspaceStorage` 管理；task artifact 由 task scoped artifact storage 管理。两套编号、ACL 与存储 URI 不能相互假设相同。当前 workspace runtime output 已经是实际文件版本；task artifact 需要其自己的 producer/work item/run 实证。

**冻结决定：**W04 新增 output mapping/adaptor，不接受浏览器指定 storage URI。输出先由 runtime 写入已受控的 private staging；提交事务将精确 hash/version 映射为工作空间投影及（任务模式）artifact/formal delivery 所需产物。若跨存储无法单事务，采用持久 publication state + 可重放恢复；恢复只能补目录/事件/正式提交，绝不能重新调用 Provider。三处展示都使用同一个 output/mapping，不能复制字节或另造验收状态。

## 2. W01 合同

W01 提供资料目录及 ACL，不触发模型：

1. task file links 保持 `INPUT|REFERENCE`；不允许用户 POST `OUTPUT`。
2. 新增 conversation file links，唯一键至少为 `(tenant, client, owner, conversation, file, version, role)`；文件版本不可变，ACTIVE/DETACHED 与 revision/ETag 明确。
3. 每次创建/删除关系经 `WorkspaceConversationAccessService` 和 workspace owner/version 双重检查；task relationship 继续经 task owner scope 检查。
4. 提供 file contexts 只显示当前 caller 已获授权的 task/conversation/execution/source 映射；不可见关系不能泄漏 ID、名称、文件内容。
5. 浏览器关系写入需要 `Idempotency-Key`，删除有 `If-Match`；身份切换不能复用旧请求。

W01 不把 link 当运行授权。W02 创建执行时，才将本次已选 file/version 复制为不可变的 execution grant snapshot。

## 3. W02 合同

W02 建立统一 execution aggregate，但保留两种业务模式：

| 模式 | `businessTaskId` | work item / lease | 最终状态 |
| --- | --- | --- | --- |
| PRIVATE | null | 不创建 task lease | workspace output + optional personal adoption |
| TASK | 必填，且与 authoritative conversation task 一致 | 任务的已指派 Agent、单 required work item、claim/start 后的真实 lease | task artifact + formal delivery（仅 feature enabled 时） |

- 一次确认、一个 idempotency key、一个 execution；同 key 不同 Agent/文件版本/源输出/operation 必须冲突。
- TASK 模式先锁/验证 business task 与会话范围，再固定文件 relation/input snapshot；禁止拿 `pwe_task_*` 或任意 `taskId` 冒充业务 task。
- W02 必须明确处理「该 task 已有运行中 work item」：复用同一 execution 或 409，不允许静默并发第二个私有 run。
- 用户取消/撤销只对尚未读取的 grant 或未开始 lease 生效；不能声称已收回 Agent 已读取字节。

## 4. W03 / W04 合同

- W03 的执行卡、资料卡、成果卡不是 chat 文本猜测；按 executionId/output reference 存储/投影，SSE 只传引用，断线通过 authoritative query 恢复。
- READ 与文件生成/修改区分 `operation`；READ 不产生 output/file/formal delivery。
- W04 在任务模式先提交 task artifact，再按现有 formal delivery 服务提交；只有正式服务成功才显示「待验收」。workspace 或 conversation 的「已保存」不等于交付已提交。
- private adoption 与 formal-delivery decision 严格分域。

## 5. 迁移、锁与测试约束

- 采用新表及 nullable 扩展，历史数据仅从已有 execution/output/artifact 的可证明关系回填；不按文件名/聊天文字猜测。
- 锁顺序固定：**task root → execution → file（按 fileId）→ output**。conversation 只在其 scope service 内验证/锁定；不得在持有 execution/file 锁时反向获取 task root。
- W01/W02/W04 要覆盖：双身份、双任务、同一文件两任务、版本分支、重复 key、If-Match 冲突、runtime agent 不匹配、失效 lease、commit 后投影恢复和 feature flag 关闭。
- Provider、真实用户文件外发、扣费不属于 W00；后续真实业务 E2E 需要独立授权。

## 6. 立即实施分工

- **W01**：关系表、conversation scope port、task/conversation links 与 ACL；不改私人执行主流程。
- **W02**：统一执行 aggregate 与 TASK lease/run 编排；不改 Web 页面。
- **W03/W04**：待 W01/W02 合同实现后接会话投影、artifact/formal mapping。
- **Web**：已并行的 task-links composable 只能调用已有接口，不承担 server authorization。
