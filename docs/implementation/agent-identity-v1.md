# Agent Identity v1

> 关联任务：A01  
> 状态：第二轮独立 Review  
> 日期：2026-07-22

## 1. 冻结结论

协作平台 v1 将 `agentId` 定义为不可变、无业务含义的稳定领域身份。新身份只允许使用：

```text
^agt_[0-9a-f]{32}$
```

示例：

```text
agt_7d9e56af84d54e45b36aab081ce93f04
```

`agentId` 不编码或暗示 `clientId`、`ownerJiacn`、`personaCode`、显示名称、机器名、进程号或权限。禁止通过 ID 字符串的前缀、分段或格式推断 owner、tenant、client、persona 或授权范围。

v1 的 canonical Agent ID 合法集合只有三类：

1. 符合 `^agt_[0-9a-f]{32}$` 的新 opaque ID；
2. 已由持久身份注册表显式登记为 `LEGACY_CANONICAL` 的历史 ID；
3. 系统保留身份 `builtin-songjiang`。

“看起来像历史前缀”不等于 canonical。除 `builtin-songjiang` 外，canonical 性质只能由格式规则或身份注册表记录决定，不能由调用方猜测。

## 2. 作用域和租户语义

### 2.1 Owner scope

Agent 的不可变所有权范围定义为：

```text
owner_scope = (client_id, owner_jiacn)
```

当前协作表字段映射冻结为：

```text
tenant_id  = 当前 jiacn 逻辑主体
client_id  = OAuth/API client
owner_jiacn = Agent 所有者 jiacn，必须与 tenant_id 一致
```

在 v1 中：

- 一个 canonical `agentId` 全生命周期只能属于一个 immutable owner scope；
- 不支持把现有 Agent 从一个 owner scope 转移给另一个 owner scope；
- 新 owner 即使使用相同 persona，也必须生成新的 canonical `agentId`；
- 所有业务访问必须显式校验 `tenant_id + client_id + owner_jiacn + agent_id`，不能因为 `agent_id` 全局唯一而省略 scope；
- 请求同时出现 `tenant_id` 和 `owner_jiacn` 时，两者不一致必须拒绝，不能静默修正。

### 2.2 Persona 唯一范围

`personaCode` 是角色/能力模板，不是执行身份。允许同一个 client 下不同 owner 分别绑定相同 persona。active persona 唯一范围必须是：

```text
(client_id, owner_jiacn, persona_code)
```

不得沿用当前较窄的 `(client_id, persona_code)` 唯一范围。

## 3. 持久身份事实源

### 3.1 Source of truth

`agent_persona_binding` 及 A02 建立的 identity registry/alias 结构共同构成持久身份事实源。其要求为：

- binding/registry 保存 canonical `agentId`、immutable owner scope、生命周期状态和历史证据；
- binding 历史记录不可物理删除，只能状态迁移；
- 已签发的 `agentId` 永不复用，即使已退役；
- legacy-canonical 必须有显式、可审计的 registry 记录；
- alias 只负责兼容解析，不改变 canonical ownership。

`agent_runtime` 只是可重建的在线运行投影：可因重启、断线或清理而重建，不能作为唯一身份事实源，也不能决定历史 ownership。

### 3.2 身份对象边界

| 字段/概念 | 含义 | 生命周期 | 能否作为任务外键/ownership 依据 |
| --- | --- | --- | --- |
| `agentId` | 稳定领域身份 | 创建后不可变，永不复用 | 可以 |
| `bindingId` | 持久身份绑定记录 | 保留历史，不物理删除 | 可作为审计引用，不替代 agentId |
| `runtimeInstanceId` | 一次客户端进程实例 | 每次客户端进程启动生成一次；同一进程 WS 重连时保持不变 | 不可以 |
| `webSocketSessionId` | 一次 WebSocket 连接 | 每次连接生成；断线立即失效 | 不可以 |
| `personaCode` | 角色/能力模板 | 可升级或显式变更 | 不可以 |
| `profileId` | codex-ws-agent 本地配置键 | 本地可修改 | 不可以 |
| `displayName` | UI 展示名称 | 可随时修改 | 不可以 |
| `clientId` | OAuth/API 客户端 | owner scope 的一部分 | 不能嵌入或从 agentId 推导 |
| `ownerJiacn` | Agent 所有者主体 | owner scope 的一部分 | 不能嵌入或从 agentId 推导 |

`runtimeInstanceId` 和 `webSocketSessionId` 均不得作为任务成员、工作项、成果、命令、ACK 的外键，也不得用于判定 ownership。

## 4. 身份生命周期状态机

持久身份状态固定为：

```text
PROVISIONED -> ACTIVE -> SUSPENDED -> ACTIVE
      |           |          |
      +-----------+----------+-> RETIRED
```

| 状态 | 含义 | 允许动作 |
| --- | --- | --- |
| `PROVISIONED` | 服务端已签发身份/绑定，但客户端尚未完成有效注册 | register、suspend、retire |
| `ACTIVE` | 身份有效，可注册 runtime 并承接任务 | reconnect、suspend、retire |
| `SUSPENDED` | 暂停使用，保留身份和历史 | 仅原 owner 显式 restore，或 retire |
| `RETIRED` | 终态 | 只读审计；禁止 restore 和复用 |

### 4.1 新建和注册

- 新绑定由服务端生成 `agt_<32 hex>`，客户端不能自行指定一个新身份。
- 创建持久 binding/registry 后进入 `PROVISIONED`；完成凭证校验和首次注册后进入 `ACTIVE`。
- 客户端保存 canonical `agentId`，每次启动生成新的 `runtimeInstanceId`；WebSocket 重连继续使用该 runtimeInstanceId，但每次连接获得新的 webSocketSessionId。

### 4.2 解绑、恢复、退役

- `unbind`：`ACTIVE/PROVISIONED -> SUSPENDED`，不是 RETIRED；历史引用保留。
- `restore`：必须显式提供原 `agentId` 或 `bindingId`；仅原 immutable owner scope、身份未 RETIRED、active persona 无冲突时允许恢复。
- `retire`：任意非终态进入 `RETIRED`；终态不可自动或人工恢复。
- 新 owner 或无法证明原 ownership 的调用必须创建新 `agentId`，不得接管旧身份。

### 4.3 Persona 变化

- persona 元数据升级不改变 `agentId`。
- personaCode 变更必须是显式、受审计的 binding 操作，并满足 active persona 唯一约束。
- 历史任务继续引用原 canonical `agentId`，事件中记录 persona/binding 变化。

## 5. 注册和授权规则

1. WebSocket 握手必须提交 canonical `agentId`、`runtimeInstanceId` 和凭证。
2. 服务端以持久 binding/registry 校验 owner scope 与生命周期状态；runtime 只用于在线投影。
3. payload 中的 `agentId` 必须与已认证 session 身份一致；payload 不能切换身份。
4. 一个 webSocketSession 只代表一个 canonical Agent；同一 Agent 的多实例策略后续由 A04 明确，但实例不改变 ownership。
5. 任务成员、工作项 assignee、命令 target、ACK actor、成果 producer 只写 canonical `agentId`。
6. `builtin-songjiang` 是系统身份，禁止外部注册、alias 接管、重新绑定或 owner 转移。

## 6. Legacy canonical 与 alias

### 6.1 在线解析边界

在线兼容解析只允许：

```text
legacy_agent_id -> canonical agentId
```

以下字段只能作为迁移审计证据或人工判定线索，禁止用于在线 alias 解析：

```text
persona_code
profile_id
display_name
```

普通请求的解析顺序：

1. 按新 opaque ID 或 `builtin-songjiang` 精确判断；
2. 查询 identity registry 判断是否为显式 `LEGACY_CANONICAL`；
3. 仅在 legacy compatibility adapter 中，以完整 owner scope 查询 `legacy_agent_id` alias；
4. scope 缺失、scope 冲突、无匹配或多候选时拒绝，不得退化为 persona/displayName 猜测；
5. 解析成功后所有新写入使用 canonical `agentId`，并记录兼容命中指标。

### 6.2 历史分类规则

| 情形 | 分类与处理 |
| --- | --- |
| runtime/binding/owner scope 唯一一致 | 可显式冻结为 `LEGACY_CANONICAL`，不得仅因字符串格式自动认定 |
| ID 前缀错误，但 runtime、binding、owner 唯一一致 | 冻结该 ID 为 legacy-canonical，并记录前缀不可信证据 |
| 短 ID 且 scope 缺失 | 阻止自动迁移，人工确认 |
| 跨 owner 冲突 | 阻止自动迁移；不同 owner 最终必须使用不同 canonical ID |
| 同 scope 多候选或 binding/runtime 不一致 | 阻止自动迁移，输出冲突报告 |
| persona/profile/displayName 唯一 | 只能生成 dry-run 候选证据，不能成为在线 alias |
| inactive 历史 binding | 保留历史，不自动恢复，不复用 ID |

### 6.3 A02 负责的 registry/alias Schema

身份 Schema 不归 B01 临时决定。A02 扩大为“身份注册/alias schema 与历史检测修复”，负责：

- identity registry/alias Schema；
- `AgentSchemaInitializer` 同步；
- Schema/约束测试；
- dry-run 检测和可审计修复清单；
- 部署迁移说明。

Schema 必须支持：canonical 类型、immutable owner scope、生命周期状态、legacy alias、审计原因和时间。active alias 唯一约束不得依赖 nullable `valid_to` 的普通唯一键；应采用 generated active column（或语义等价的非空 active key）实现：

```text
(client_id, owner_jiacn, alias_type, alias_value, active_key) UNIQUE
```

其中 v1 在线 alias 的 `alias_type` 只允许 `LEGACY_AGENT_ID`。persona/profile/displayName 可存入独立 migration evidence，但不能写成可在线解析 alias。

## 7. 当前数据审计结论

2026-07-22 只读检查确认：

- 系统 ID：`builtin-songjiang`；
- 历史短 ID：`wuyong`、`linchong`，部分 runtime 缺少 client/owner/persona；
- 拼接 ID：`jyt-{clientId}-{personaCode}`；
- 任务 373 存在 `assigned_agent_id=husanniang` 且 tenant/client 缺失；
- `jyt-jia_client-linchong` 的字面前缀与真实 client/owner 不一致；
- `jyt-jia_client-wuyong` 存在不同 scope 历史。

因此禁止按 personaCode、displayName 或 ID 前缀直接全库替换，也禁止以可删除的 runtime 记录单独证明 ownership。

## 8. A02 dry-run 输出与门禁

A02 至少输出：

```text
canonical_agent_id
canonical_type
lifecycle_status
legacy_agent_id
client_id
owner_jiacn
tenant_id
persona_code_evidence
profile_id_evidence
runtime_match
binding_match
task_reference_count
resolution_status
resolution_reason
```

自动生成修复 SQL 的前提是：owner scope 完整且一致、canonical 唯一、legacy_agent_id 在该 scope 唯一。其余记录只能进入人工清单。第一轮迁移默认不直接批量改写历史主键/外键，先落 registry/alias、验证冲突和引用，再由 B09 处理历史任务成员/工作项回填。

## 9. 后续代码影响

- `AgentServiceImpl.generateAgentId()`：改为服务端随机 opaque ID，停止拼接 client/persona。
- `bindPersona()/unbindPersona()`：按上述状态机实现 suspend/restore/retire，禁止物理删除历史 binding。
- `AgentRegisterDTO`：注册已有身份，不承担创建新身份。
- `ApiKeyHandshakeInterceptor`：校验 canonical ID、immutable owner scope、ACTIVE 状态和 runtimeInstanceId。
- `AgentWebSocketHandler`：区分 stable agentId、runtimeInstanceId、webSocketSessionId。
- `agent_persona_binding`：active persona 唯一范围调整为 `(client_id, owner_jiacn, persona_code)`。
- 协作领域表：使用 canonical agentId，并显式携带 tenant/client scope。

## 10. 验收条件

- canonical ID 合法集合已封闭定义，不依赖前缀推权。
- owner scope、tenant/client/owner 映射和 persona 唯一范围已冻结。
- 持久 binding/registry 是身份事实源，runtime 是可重建 projection。
- runtimeInstanceId 和 webSocketSessionId 生命周期明确且不作为业务外键。
- PROVISIONED/ACTIVE/SUSPENDED/RETIRED 状态机和恢复边界明确。
- 在线 alias 仅允许 legacy_agent_id；其他身份线索仅作迁移证据。
- 历史错误前缀、跨 owner 冲突、scope 缺失和多候选均有阻断规则。
- A02 明确拥有 identity registry/alias Schema、Initializer、测试和 dry-run。
