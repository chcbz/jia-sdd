# Agent Runtime v1 新客户端规范（设计稿）

> 状态：用户已确认“统一升级新客户端，不兼容旧 Agent 客户端”（2026-09-14）。本文件定义待实现的 Runtime v1；不构成生产启用或凭据发放指令。

## 1. 目标与范围

Runtime v1 让一个受控 Agent 客户端以唯一身份连接 CYF、接收定向命令，并回传不可伪造、可幂等的执行状态。

范围：客户端注册、安装绑定、在线状态、F01 Context Pack 与 E05 定向重派的 durable ACK、审计与最小页面状态展示。

不在范围：旧客户端/旧身份字符串兼容、自动重派、支付、语音 Provider、浏览器获取运行凭据、远程强制重启客户端。

## 2. 参与者与身份

- **管理员/用户**：在 Web 发起绑定或查看状态；只能看到脱敏状态。
- **Runtime v1 客户端**：安装在目标 Agent 所在主机，执行握手、收命令和回执。
- **API**：唯一裁决身份、安装状态、命令状态和审计。

每个运行时主体的唯一身份为：

```text
tenantId + clientId + canonicalAgentId
```

`personaCode` 仅可用于 Web 选择角色，不能授权、不能替代 `canonicalAgentId`，也不能作为跨 tenant/client 的查找键。旧 `jyt-*` 等协议身份不被解析或映射；旧客户端必须升级。

## 3. 安装与授权流程

### 3.1 创建安装申请

管理员在 Web 为一个已存在的规范 Agent 创建安装申请。API 创建：

```text
installationId, tenantId, clientId, canonicalAgentId,
manifestVersion, manifestSha256, enrollmentExpiresAt, status=PENDING
```

Web 仅取得安装状态、安装编号和到期时间；不得收到长期 API Key、JWT、Provider Key 或可复用运行密钥。

### 3.2 受控交付与首次激活

部署渠道将以下内容交给目标主机的 Runtime v1 安装器：

- 不含密钥的安装 manifest；
- 一次性 enrollment secret（短有效期、单次使用、不得写入日志或浏览器）；
- 安装包版本和完整性摘要。

安装器校验安装包及 manifest 摘要后，以 enrollment secret 调用 Runtime v1 激活接口。API 验证申请未过期、主体完全匹配且尚未使用，然后：

1. 使 enrollment secret 立即失效；
2. 创建可撤销的安装记录；
3. 返回安装级、受限且可轮换的运行授权；
4. 记录激活审计。

运行授权只能用于该 installationId、该 tenant/client/Agent 和 Runtime v1 协议，不能用于 Web 登录、其他 Agent 或 Provider 调用。

### 3.3 运行与失效

客户端每次启动先校验本地 manifest 版本和摘要，再建立 Runtime 会话并上报版本、installationId 与健康状态。服务端发现主体、版本、摘要或授权不一致时，返回“需要重新绑定”；客户端停止接收命令，不得降级为匿名或旧协议。

客户端不接受 API 下发的任意 shell 命令、重启命令或凭据更新；升级和重启由安装主机的受控发布流程完成。

## 4. 协议接口（v1）

接口路径为设计契约；落地时保持版本前缀，不复用含敏感输出的旧绑定接口。

| 接口 | 调用方 | 作用 | 结果 |
| --- | --- | --- | --- |
| `POST /agent/runtime/v1/installations` | Web | 创建安装申请 | installationId、脱敏状态、manifest 摘要 |
| `POST /agent/runtime/v1/enroll` | 安装器 | 消耗一次性 enrollment，激活安装 | installation 状态与受限运行授权 |
| `POST /agent/runtime/v1/session` | 客户端 | 建立/续期运行会话 | session 状态、命令通道信息 |
| `POST /agent/runtime/v1/heartbeat` | 客户端 | 上报在线/版本/健康 | online 或 rebind-required |
| `POST /agent/runtime/v1/commands/{messageId}/acks` | 客户端 | 提交命令回执 | `ADVANCED` 或幂等 `PRIOR` |
| `GET /agent/runtime/v1/installations/{id}` | Web | 查询脱敏安装状态 | PENDING/ACTIVE/REVOKED/REBINDS_REQUIRED |
| `POST /agent/runtime/v1/installations/{id}/revoke` | 有权管理员 | 撤销指定安装 | REVOKED，后续会话拒绝 |

请求主体由运行授权绑定；请求体中即使包含 tenant、client 或 agent 字段，也必须与运行授权精确一致，否则拒绝。

## 5. 命令与 ACK

每个命令至少包含：

```text
messageId, correlationId, commandId, taskId, workItemId,
target tenantId, target clientId, target canonicalAgentId,
payloadReference, expiresAt
```

`payloadReference` 指向受控上下文或成果引用，不将长期凭据嵌入命令。

状态机：

```text
PENDING -> RECEIVED -> STARTED -> SUCCEEDED
                            \-> FAILED
PENDING/RECEIVED -> REJECTED
```

约束：

- 同一 `messageId` 的同一有效状态重复 ACK 返回 `PRIOR`，不重复执行业务动作；
- 状态只能单向推进；终态不可改写；
- ACK 的 Runtime 身份必须等于命令目标；
- 命令过期、错误 scope、未知安装或已撤销安装必须拒绝；
- 只有数据库事务提交后的 ACK 才能更新任务页面状态；
- E05 只允许显式目标重派，不由 ACK 触发自动重派；F01 只确认上下文已收到/处理结果。

## 6. 客户端最小行为

1. 读取只读 manifest，并验证版本和 SHA-256；
2. 完成 enrollment 或建立运行会话；
3. 仅接收自身 scope 的命令；
4. 命令落盘或进入本地可靠队列后发送 `RECEIVED`；
5. 开始业务处理前发送 `STARTED`；
6. 最终发送 `SUCCEEDED`、`FAILED` 或 `REJECTED`；
7. 网络重连后仅重发同一 messageId 的 ACK，不重新执行已处于终态的命令；
8. 授权、manifest 或身份异常时停止消费并上报 `rebind-required`。

客户端日志必须掩码运行授权、enrollment secret、请求 Authorization 头及任何 Provider 凭据。

## 7. Web 展示

- Agent 卡片：未安装、待激活、在线、离线、需要重新绑定、已撤销；
- 任务详情：已投递、已接收、执行中、成功、失败、拒绝及相应时间；
- 安装详情：版本、配置摘要、最近心跳、状态和可执行的“撤销/重新绑定”；
- 不展示运行授权、enrollment secret、完整请求头或敏感日志。

## 8. 从 codex-ws-agent 升级

现有 `codex-ws-agent` 是旧 WebSocket 协议客户端：以 URL API key 连接、使用旧注册/任务回报消息，且其配置格式不能表达 Runtime v1 的安装级身份与 ACK 契约。因此**不能通过替换一个配置文件或 `npm update` 原地升级**；需要并行安装 Runtime v1，逐 Agent 切流后再卸载旧客户端。

### 8.1 新包组成

Runtime v1 发布包至少包含：

```text
agent-runtime-v1/                  # 新安装目录，不覆盖旧目录
  agent-runtime.mjs                # Runtime v1 主程序
  manifest.json                    # 无敏感配置、含 SHA-256
  package.json                     # 固定客户端版本
  systemd/cyf-agent-runtime-v1.service
  install.sh / validate.sh          # 安装与离线静态校验
```

旧 `codex-ws-agent` 的 `.env`、profile API key、会话目录和日志不得复制到新目录。每个新安装申请单独生成一次性 enrollment secret，通过受控部署渠道提供给目标主机；不得在浏览器、聊天或普通日志中传递。

### 8.2 单个 Agent 的切换步骤

1. 服务端先部署 Runtime v1 API，保持旧任务投递不变；
2. 为该 Agent 创建 Runtime v1 installation；
3. 在其主机安装 Runtime v1 至新目录，执行离线 `validate`；
4. 使用一次性 enrollment 激活，确认该 Agent 的 heartbeat 为 online；
5. 投递一条无副作用的 F01/E05 受控命令，取得真实 terminal ACK；
6. 仅切换该 Agent 的后续投递到 Runtime v1；
7. 观察其任务状态和审计记录；
8. 该 Agent 稳定后，撤销其旧协议授权并停止旧 profile；旧历史只保留审计。

一个 Agent 的第 3–7 步失败时，只保留其旧客户端投递，不影响其他 Agent；修复 Runtime v1 后从同一安装申请重新绑定，不能把失败客户端标记为已升级。

### 8.3 完成切换

全部目标 Agent 都完成 Runtime v1 heartbeat 与受控 ACK 后：

1. 停止旧 `codex-ws-agent` 服务和旧 profile；
2. 撤销旧 WebSocket API key/授权；
3. 清除旧客户端目录中的凭据配置与不再需要的日志，保留必要审计；
4. 后端对旧协议返回 `426 Upgrade Required`，不提供身份映射或兼容降级。

切换操作由各客户端/运行时的精确 Owner 执行；不得由协调线程停止其他线程的服务或删除其目录。

## 9. 验收

- 同名 persona 位于不同 tenant/client 时，客户端和 ACK 绝不串用；
- 未升级旧客户端被明确拒绝，不能被静默识别为新客户端；
- 激活码单次使用、过期失效；浏览器/API 页面/日志均不泄露运行密钥；
- 安装撤销后 heartbeat 与 ACK 被拒绝；
- F01 和 E05 各完成一次真实的 `RECEIVED -> STARTED -> terminal` 闭环；
- 重复 ACK 只返回幂等结果，不导致重复业务执行；
- 精确 develop 提交通过 API Flow `5260799`，以同 Run 制品部署并完成健康与受控业务 readback。
