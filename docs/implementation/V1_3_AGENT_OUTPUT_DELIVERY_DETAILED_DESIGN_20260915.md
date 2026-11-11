# V1.3.0 Agent 产物交付 R1 详细设计

> **状态：实现基线（2026-09-15）。** 本文把“Agent 已生成文件但用户不能可靠领取”的需求落实为 `1.3.0`。它是开发和验收的合同，不表示功能已经合入、启用或发布。
>
> 运行 Owner、精确 SHA、阻塞项和 Flow Run 以 `docs/implementation/TASKS.yaml#runtime_ledger_json` 为准；版本排序见 `docs/implementation/VERSION_PLAN_20260915.md`。

## 1. 结论、范围与决策

### 1.1 产品结果

当受控 Agent 完成一次聊天或悬赏运行时，它可以**显式**交付 manifest 中列出的文件。授权用户可在：

1. 普通聊天的“本次成果”；
2. 悬赏详情的“已分享成果”；

查看元数据、预览受支持的小文件或下载精确版本。分享只代表文件可取，**不代表悬赏已提交、已验收、已结算或任务完成**。

### 1.2 R1 范围

| 包含 | 不包含 |
| --- | --- |
| run-bound Agent 自动发布、离线后取件、幂等恢复 | 正式提交、人工验收、要求修改、返工（`1.4.0`） |
| 私有本地文件系统成果库、受控 manifest、客户端安全快照/队列 | MinIO/S3、ClamAV、浏览器直传、分片上传、大文件 |
| 对话与悬赏的用户只读列表、精确下载、有限预览 | 多 Agent 联合交付、自动审核、资金和结算 |
| 两身份/两客户端隔离、撤销/过期拒绝 | 任意工作区浏览、历史目录回填、旧客户端兼容 |

### 1.3 架构决策

1. **新重基线优先。** `specs/agent-output-delivery/latest-baseline-replan.md` 覆盖旧 `detailed-design.md` 的 MinIO/ClamAV/独立 output 域方案。旧候选只作为负向测试与风险案例参考，禁止整体 merge 或 cherry-pick。
2. **一个文件事实源。** 继续使用 API `AgentTaskArtifactStorage` 和 `agent_task_artifact` 保存字节、hash、精确版本与任务成果；`artifact-outcomes` 保持正式裁决唯一事实源。对话表只能保存“会话 → 已有精确 artifact 版本”的映射，不保存第二份文件、storage URI 或可改写版本。
3. **一个 Agent 写协议。** 文件字节仅走受控 HTTPS multipart 发布接口；WebSocket 只用于已认证 runtime 换取短期 ticket 和接收回执，不能承载文件字节。
4. **身份由服务端推导。** Agent 请求不能指定/覆盖 tenant、client、task、conversation、producer agent、文件路径或存储位置。它们全部来自持久化的 run binding 和 opaque ticket。
5. **先快照、后联网。** Agent 只向私有队列中的不可变本地快照上传，绝不从模型可写工作区直接读取上传。
6. **默认关闭、故障隔离。** `agent.task-artifact-storage.enabled` 保持 false，存储准入和小范围验证完成前不接受 Agent 自动写入。成果同步是异步附加能力：它不能阻塞聊天回复、任务终态、Agent 断开、用户退出或既有人工成果读取。

## 2. 基线、影响和已知缺口

### 2.1 当前代码基线

| 组件 | 事实 | 对 R1 的影响 |
| --- | --- | --- |
| API `origin/develop` | `bff69fb869867f0d2d453a3f9fa22c9332aa23c5` | 已有私有 content-addressed 文件系统存储、task artifact 与 artifact outcome；R1 不重造它们 |
| Web `origin/develop` | `a9c5224a00c5f1491e6f36c7b9e396244b2985a4` | 已有聚义厅工作台 `ArtifactTransferPanel`/`ArtifactOutcomePanel`；R1 新增聊天/悬赏用户入口，保留工作台用途 |
| 根仓候选 | `origin/codex/agent-output-delivery` = `e2ea0c221eb104b92fd5c9e20c8cb48d946c4889` | 设计来源而不是可直接发布分支 |
| 客户端候选 | `29aa70da8bb9f0476379dd6bd9e41731c5219457` 当前在 `isp-install` 不可达 | 客户端提交未推送前，禁止宣布完整 R1 发布 |

### 2.2 已有能力

- `AgentTaskArtifactStorage` 的实现将对象定位从精确 `tenant/client/task` 和内容 hash 推导，拒绝外部传入路径或 URL；文件系统实现检查私有目录、符号链接、哈希与长度。
- `AgentTaskArtifactController` 已提供用户 JWT 的 `/agent/tasks/{taskId}/artifacts` 上传和精确版本下载；它要求用户 JWT 及 `actorAgentId` query，**不可以**作为 Agent 自动上传接口。
- `AgentTaskArtifactOutcomeController` 和 `artifact-outcomes` 已表达“权威接受/取代”；R1 不调用它来把分享升级为验收。
- 现有存储默认单文件上限为 **16 MiB**，默认 MIME allowlist 包含文本、JSON、PDF、PNG/JPEG、ZIP 等。

### 2.3 本版的用户和系统影响

| 影响面 | 变化 | 兼容性 |
| --- | --- | --- |
| Agent 客户端 | 增加 manifest、快照、私有队列、ticket 和发布回执 | 只支持升级后的 Runtime v1；旧客户端不静默降级 |
| API | 增加 output run binding、ticket、幂等回执、conversation 映射和只读入口 | 现有用户上传/下载/裁决接口保持原语义 |
| 数据库 | 只新增绑定/回执/映射表和索引 | 不回填来源不明的历史记录；不重建旧 artifact 表 |
| Web | 聊天与悬赏新增只读成果入口 | 聚义厅工作台的人工上传/裁决面板不改为自动发布入口 |
| 运维 | 需准备私有 root、备份恢复与 feature flag | 未准入时 fail-closed；既有业务不因 R1 写入失败而受影响 |

## 3. 用户流程

### 3.1 聊天成果

1. 用户在其身份下向已升级 Agent 发起可产出文件的运行。
2. API 创建 `runId`，将本次 task、可选 conversation、目标 Agent 和 scope 固化为 output run binding。
3. Agent 在本次输出根写入 `outputs/<runId>/manifest.json` 和文件。
4. Agent 先完成原有聊天/任务终态，再在 finish 后钩子校验 manifest 并安全快照到私有队列；上传、ticket 交换和发布全部异步进行。
5. 用户打开聊天成果列表：已发布时看到标题、类型、大小、hash 前缀、产生时间和“已分享，非正式验收”；仍在队列中时只显示“成果同步中”，不伪报已可下载。
6. 用户仅可预览受支持内容或下载精确 artifact version；Agent 离线后仍可领取保留期内已发布文件。

没有 manifest、manifest 无有效条目、存储不可用或发布被拒绝时，聊天文本和原任务状态仍按原业务返回。页面只报告成果不可用/同步失败及可执行的刷新或重试同步动作；不得把模型文字中的“已生成文件”当作交付成功，也不得把成果故障升级为整段聊天失败。

### 3.2 悬赏成果

1. Agent 运行绑定到悬赏 task；可选 `publishToOwner=true` 的 manifest 项才会显示给发布人。
2. 发布人从悬赏详情读取只读列表、下载精确版本。
3. 页面只能标记“已分享”。正式接受、取代、退回和返工保持关闭，留给 `1.4.0`。

### 3.3 中断和恢复

- 上传网络中断或响应丢失：客户端重启后从队列复用**同一快照 hash 和同一 idempotency key**；服务端返回原 receipt 或继续未完成操作。
- ticket 过期：客户端只重新请求 ticket；不重新执行 Agent，也不扫描/重读模型工作目录。
- binding 被撤销、Agent 更换、scope 不符或运行过期：停止发布并将队列项置为 `BLOCKED`，不无限重试。已成功发布的用户读路径不因 Agent 离线而消失。

## 4. 总体架构

```text
Agent workspace (model-writable)
  └─ outputs/<runId>/manifest.json + declared files
         │ validate + no-follow snapshot
         ▼
Runtime v1 private queue (0700/0600; immutable snapshot)
         │ authenticated WS: request short ticket
         ▼
API output publication bridge
  ├─ validate opaque ticket → derive scope/run/task/conversation/agent
  ├─ bound multipart → SHA-256 + MIME/size checks
  ├─ existing AgentTaskArtifactService + AgentTaskArtifactStorage
  └─ atomically persist receipt + optional conversation mapping
         ▼
agent_task_artifact (exact artifact version) ──► existing private storage
         │
         ├─ task/bounty read adapter
         └─ conversation_deliverable mapping ──► conversation read adapter
                                             ▼
                                Web OutputList / OutputPreview / download
```

### 4.1 服务责任

| 责任 | 组件 |
| --- | --- |
| 生成与校验 manifest、执行 no-follow 快照、持久重试 | `isp-install` Runtime v1 |
| run 与目标主体/业务来源的不可变绑定、ticket 签发/撤销 | API runtime/dispatch 服务 |
| 受控上传、幂等、调用既有 artifact 服务 | API `AgentOutputPublicationService`（新增桥接，不复制 artifact ACL/版本逻辑） |
| 字节存储、内容寻址、hash 和精确 artifact 版本 | 既有 `AgentTaskArtifactStorage`、`AgentTaskArtifactService` |
| 会话归属 | 新增 `conversation_deliverable` 只保存 artifact 精确版本引用 |
| 展示、预览、带 JWT 的 Blob 下载、取消过期请求 | Web 共用 outputs 组件 |

### 4.2 直接聊天的 task 绑定

R1 的一个 artifact 必须有 task artifact 版本。因此，启用文件交付的直接聊天派发需要一个内部 **delivery-only task binding**；它只用于版本、存储和 ACL 归属，不在悬赏工作台伪造待办任务，也不改变没有文件需求的聊天流程。

该绑定**不在用户回复的关键路径上制造失败**：调度服务在向已具备输出能力的 Runtime 派发前尝试建立 binding；建立失败时，该 run 以“无成果导出能力”继续执行正常聊天，不签发上传 ticket，不取消用户请求，也不创建无归属的文件。

RB00 必须先盘点现有聊天派发是否已拥有可靠 `taskId`：

- 已有 `taskId`：直接写入 output run binding；
- 没有 `taskId`：创建不可协作、同 scope 的 delivery-only task 后再创建 binding；
- task/binding 任一项无法精确建立：正常聊天继续，但本 run 不获得 output capability。

这避免为了聊天另建一套“output 文件/版本”事实源，也避免低优先级成果同步拖垮聊天可用性。

## 5. 客户端详细设计

### 5.1 `outputContext`

派发给 Runtime v1 的受信任上下文至少包括：

```json
{
  "schemaVersion": 1,
  "runId": "uuid-hex",
  "outputRoot": "outputs/<runId>",
  "manifestRelativePath": "outputs/<runId>/manifest.json",
  "maxFileBytes": 16777216,
  "maxFiles": 100,
  "allowedMimeTypes": ["..."],
  "canShareToOwner": true,
  "expiresAt": "epoch-ms"
}
```

它不包含 upload ticket、tenant/client、任意可写服务器路径、对象 URI、长期 API key 或 Provider 凭据。服务器保留这些权威字段，客户端不得用 context 构造身份。

### 5.2 manifest v1

固定位置为 `outputs/<runId>/manifest.json`，UTF-8 严格 JSON，最大 128 KiB、最多 100 项。建议的封闭 schema：

```json
{
  "schemaVersion": 1,
  "items": [
    {
      "outputId": "report",
      "title": "调研报告",
      "relativePath": "report.md",
      "artifactType": "document",
      "publishToOwner": true
    }
  ]
}
```

规则：

- `relativePath` 必须是导出根内的相对路径；拒绝绝对路径、空段、`.`、`..`、反斜杠规避、NUL、目录、符号链接、设备、FIFO 和未声明文件。
- 只接受普通文件，逐级 `NOFOLLOW_LINKS` 打开和复核；snapshot 前后核对 inode/大小/hash，变化即拒绝该项。
- `outputId` 为固定小写标识（1–100 字节），同一 manifest 不重复；重试沿用同一 ID 与快照 hash。
- `title`、类型和扩展名不构成授权；MIME 由客户端初判、服务端再判。HTML、SVG、可执行文件和脚本一律拒绝。文本、PNG/JPEG 可预览；PDF/ZIP 仅下载。

### 5.3 安全快照和队列

新增文件建议位于版本化客户端源：

| 文件 | 责任 |
| --- | --- |
| `output-manifest.mjs` | 严格解析、路径和 schema 校验 |
| `output-exporter.mjs` | no-follow 安全读取、copy+fsync、hash 与 snapshot 清单 |
| `output-queue.mjs` | 私有队列状态机、原子持久化、恢复和隔离损坏项 |
| `output-http.mjs` | ticket、multipart 发布、receipt 查询与有界重试 |

队列根由桥接进程拥有，目录权限 0700、文件 0600；不可位于模型可写 workspace。写入使用 `tmp → fsync(file) → rename → fsync(directory)`。记录保存 runId、outputId、snapshot path/hash、状态、idempotency key、receipt reference 和重试信息；**不得**落 ticket 明文。

状态机：

```text
SNAPSHOTTED → PUBLISH_PENDING → TICKET_PENDING → UPLOADING → PUBLISHED
                                        │              │
                                        └────→ BLOCKED ←┴── retryable transport error → PUBLISH_PENDING
```

`SNAPSHOTTED` 即表示 Agent 的业务执行已经结束；其后的状态推进不反写聊天/任务终态。

- 网络错误：受控退避和单消费者恢复，最长不超过 binding 的业务恢复期限；不发起并行重复上传，也不向下游施加人为性能 deadline。
- 401/expired：重新交换 ticket 后继续同一快照；认证/授权未恢复则明确进入 `BLOCKED`。
- 403、来源撤销、manifest 不合法、hash/MIME 不符：`BLOCKED`，保留脱敏诊断，不盲目重试。
- 队列损坏：隔离该记录并告警；不能推断“可能已上传成功”。
- 磁盘写满、存储只读或 API 暂不可用：保留正常聊天/任务结果，暂停新的 snapshot；已发布文件继续读。恢复后只由用户或运行 Owner 显式触发“重试同步”。

## 6. 身份、run binding 与 ticket

### 6.1 持久 run binding

服务端派发时创建 `agent_output_run_binding`。一行至少固化：

```text
tenant_id, client_id, run_id (unique), task_id, conversation_id nullable,
producer_agent_id, runtime_installation_id, output_capability_version,
state, recovery_until, revoked_at, created_at
```

`runId`、scope、producer、task、conversation 和 installation 创建后不可改写。所有变更先根据精确 scope 找 binding 并加锁；不得根据 persona、用户传入的 taskId 或聊天 messageId 推断。

### 6.2 opaque ticket

1. 已认证 Runtime v1 在其单播 WS 会话发送 `output.auth.request {runId, requestId}`。
2. API 检查运行时安装、scope、producer、binding 状态、能力版本和 `recovery_until`；生成随机 256-bit ticket，只持久化 SHA-256、过期时间、binding ID、允许操作和签发审计。
3. API 单播返回 `output.auth.receipt {requestId, ticket, expiresAt}`。ticket 不入 prompt、manifest、子进程环境、浏览器、普通日志或持久队列。
4. HTTP 发布只接受 `Authorization: Bearer <ticket>`；用 hash 找 ticket 后，从行和 binding 推导全部权威身份。请求体中的 scope/task/agent 字段不存在；即使客户端添加未知字段也按封闭 schema 拒绝。

ticket 有效期短、只用于当前 run 的 `publish/status`，被撤销的安装或 binding 立即失效。`artifact.publish` 协议常量只能表示受控发布能力，不能成为未绑定的任意文件上传授权。

## 7. API 契约与数据模型

### 7.1 Agent 发布接口

新增专用路径，不能复用要求用户 JWT 的 `POST /agent/tasks/{taskId}/artifacts`：

```text
POST /agent/runtime/v1/output-publications
Authorization: Bearer <opaque-run-ticket>
Idempotency-Key: <16..100 ASCII chars>
Content-Type: multipart/form-data
```

multipart 固定且仅有两部分：

- `metadata`：`application/json`，最大 64 KiB；封闭字段 `outputId`、`title`、`artifactType`、`publishToOwner`、`declaredSha256`、`declaredMimeType`；
- `content`：一个普通文件，最大 **16 MiB**。

服务端限界读取、独立计算 SHA-256、检测/校验 MIME，并把 ticket 推导的 `taskId`、`producerAgentId` 注入既有 `AgentTaskArtifactService.publish`。处理器采用路由级背压和有界资源释放；资源不足只返回可恢复失败给队列，**不能占用或取消聊天、任务调度和既有下载请求**。无论请求怎样命名，不能覆盖 task、scope、agent、artifact 存储 URI 或 artifact version；版本由服务端对 `outputId` 的既有精确版本 CAS 决定。

成功响应仅含：

```json
{
  "outputId": "report",
  "artifactId": "...",
  "artifactVersion": 1,
  "sha256": "...",
  "byteLength": 1234,
  "publishedAt": 0,
  "publicationKind": "CONVERSATION_OUTPUT"
}
```

同一个 idempotency key 且相同 `runId/outputId/sha256/metadata` 返回原 receipt；同 key 不同请求摘要返回 `409 IDEMPOTENCY_CONFLICT`。响应绝不含 storage URI、文件系统路径或 ticket。

### 7.2 用户只读接口

新增读适配器，以用户 JWT 的 `(jiacn, client_id, sub)` 进行来源 ACL，不再要求浏览器传 `actorAgentId`：

```text
GET /agent/conversations/{conversationId}/deliverables?cursor=&limit=
GET /agent/conversations/{conversationId}/deliverables/{deliverableId}/content
GET /agent/tasks/{taskId}/deliverables?cursor=&limit=
GET /agent/tasks/{taskId}/deliverables/{artifactId}/versions/{version}/content
```

列表返回 `items,nextCursor,snapshotAt`。游标为签名 opaque token，绑定 exact scope、source、筛选条件和快照时间；默认 20、最大 100。每页重查 ACL，撤权数据不得泄露标题、数量、hash 或存在性。下载使用 `Cache-Control: private, no-store`、`X-Content-Type-Options: nosniff` 和安全的 `Content-Disposition`；禁止签名对象 URL。

### 7.3 最小迁移

| 表 | 用途 | 关键约束 |
| --- | --- | --- |
| `agent_output_run_binding` | run 与精确 scope/task/conversation/producer/runtime 的权威绑定 | `(tenant_id,client_id,run_id)` 唯一；不可变归属字段 |
| `agent_output_access_ticket` | ticket hash、过期、撤销、操作范围、签发审计 | `ticket_hash` 唯一；只保存 hash，不保存 bearer 明文 |
| `agent_output_publication_receipt` | Agent 发布幂等回执 | `(binding_id,idempotency_key)` 唯一；请求摘要固定 |
| `conversation_deliverable` | conversation 指向既有 task artifact 精确版本 | `(tenant_id,client_id,conversation_id,task_id,artifact_id,artifact_version)` 唯一；不保存第二份 bytes/URI |

迁移只新增表、索引和外键/逻辑完整性检查；不自动把 `tenant_id='0'` 或归属不明确的历史数据映射给用户。R1 读写路径必须始终把 tenant/client 作为查询前缀。

### 7.4 事务、外部 I/O 与失败语义

- 先验证 ticket/binding，再取得 task/source 和 receipt 的确定锁；调用现有 artifact service 时复用其 ACL、版本和事务边界。
- 文件系统 `store` 在数据库事务外完成；数据库回滚可能留下无引用的内容寻址孤儿对象。R1 增加只删除“无 artifact 行引用、超过恢复窗口、且存储身份/hash 精确匹配”的保守 reconciliation；不做基于路径猜测的删除。
- artifact 发布、receipt 和 conversation 映射在同一业务事务完成。任一失败时不返回成功；已存文件按上述安全回收。
- 不在数据库事务中执行 WebSocket、下载流或其他网络 I/O。

## 8. Web 详细设计

### 8.1 组件与状态

新增通用只读组件：

| 文件 | 责任 |
| --- | --- |
| `web/src/components/outputs/OutputList.vue` | 列表、状态标签、空/无权限/未知状态 |
| `web/src/components/outputs/OutputPreview.vue` | 严格转义文本和受限位图预览 |
| `web/src/composables/useOutputs.js` | 请求、分页、取消、刷新和 cache key |
| `web/src/utils/outputDownload.js` | JWT fetch → Blob → 安全下载 → 释放 Blob URL |

`OutputList` 被普通聊天和悬赏详情复用。既有 `ArtifactTransferPanel` 和 `ArtifactOutcomePanel` 保持在聚义厅工作台，不作为 R1 的用户上传或验收入口。

### 8.2 呈现和缓存规则

- 每项显示标题、类型、精确版本、大小、hash 前缀、产生时间和“已分享，非正式验收”。不显示本地路径、storage URI、producer credential、ticket。
- 页面状态必须区分 `无已分享成果`、`成果同步中`、`暂不可读取`、`无访问权限` 和 `已分享`；失败状态附带“刷新”或“重试同步（仅原快照）”动作，绝不能替换或阻塞聊天正文。
- 仅预览不超过 1 MiB 的 UTF-8 文本/Markdown（HTML 一律转义）及受限尺寸 PNG/JPEG；PDF、ZIP 和未知类型仅下载。
- cache key 固定为 `identityFingerprint + sourceType + sourceId`。登录身份、client、会话或悬赏切换，登出和组件卸载时取消 `AbortController`、清空列表并释放 Blob URL；旧响应不能回填新上下文。
- 网络结果未知显示“请刷新确认”，不把失败、403 或空数组显示为“没有成果”；403 只显示无访问权限，不能泄露成果存在性。

## 9. feature flag、发布与回退

### 9.1 开关

建议独立 feature flag：

```text
agent.output-delivery.r1.enabled=false
agent.task-artifact-storage.enabled=false
```

两者都开启且 storage 准入通过，才对允许 scope 签发 output ticket。关闭任一开关时：

- 不再签发新 ticket 或接受新自动发布；
- 已发布的、已有授权的读路径保持可用；
- 不删除数据、不回退 schema、不把分享状态伪装为验收。

### 9.2 存储准入

启用前必须记录实际证据：私有绝对 root、API 运行账户的最小权限、非符号链接、真实读写/hash readback、失败恢复、备份恢复演练及实际制品/备份所需空间。容量仅按本次制品和可恢复副本计算，不采用任意“预留 N GiB”门槛。

### 9.3 合入和发布

- 每个路径独立的 Owner 在最新 `develop` worktree 自检后合入；不创建独立 Reviewer 队列。
- 先发布 schema/读取兼容与 API/Web 代码，并保持两个 R1 写开关关闭；这一步不能改变既有聊天、悬赏、人工 artifact 或下载行为。通过 storage 准入、客户端可达和端到端证据后，再对一个明确测试 scope 开启新写入；扩大范围只在真实可用性读回后进行。
- API 用 Flow `5260799`，Web 用 Flow `4403172`；正式证据绑定精确提交、测试摘要、同 Run 制品摘要、部署顺序和线上 readback。
- 后端发布遵循当前北京时间每日 00:00 汇总发布规则；前端按既定 minor/major 时段规则。不得为了 R1 新增重复流水线或用本机生产构建替代 Flow。
- 客户端必须从 `isp-install` 的可达版本化提交发布。当前 `29aa70da…` 不可达是硬事实，不得用聊天记录或本机运行目录替代 release evidence。

## 10. 风险矩阵与处置

| 级别 | 风险/影响 | 处置 |
| --- | --- | --- |
| P0 | 旧 output-delivery 方案和最新重基线冲突，整体合入会产生第二套表、对象和 ACL | 以本详设和 `latest-baseline-replan.md` 为准；旧候选仅作案例参考 |
| P0 | Agent 自动上传误用用户 JWT + `actorAgentId`，可产生身份混淆 | 专用 opaque run ticket；服务端从 binding 推导 scope/task/agent |
| P0 | API/Web 旧候选与 develop 分叉大，直接 merge 会覆盖后续修复 | 均从最新 develop 新建 worktree，按 R1 包重新实现/选择性整合 |
| P0 | 客户端提交 `29aa70da…` 不可达 | 先推送该提交或等价完整分支；未完成前禁止把 R1 标为完整上线 |
| P1 | 私有文件系统配置不当、备份不可恢复或默认关闭误被绕过 | feature flag fail-closed；启用前做权限、读写、hash、备份恢复准入 |
| P1 | ZIP/PDF 等可能含恶意或敏感内容 | 16 MiB、严格 MIME、禁 HTML/SVG/可执行文件、不内嵌 PDF/ZIP；R1 不声称已病毒扫描 |
| P0 | 成果同步故障反向阻塞聊天回复、任务终态或既有下载 | finish 后异步快照/上传；失败只影响本 run 的交付件，并保留正常业务结果和已发布读路径 |
| P1 | multipart 与 16 MiB 文件造成 API 内存/代理限制压力 | 路由级背压、单请求上限和真实观测；资源不足只进入队列恢复，不把任意超时当可用性门槛 |
| P1 | publish 成功但响应丢失导致客户端重复上传 | 绑定级 idempotency receipt、同快照 hash、队列恢复；不重跑 Agent |
| P1 | 会话/身份切换后 Web 串缓存或泄露标题 | identity+source cache key、取消请求、每页重查 ACL、负向双身份测试 |
| P2 | 16 MiB 不适合大代码包/媒体 | 明确拒绝并提示；对象存储/扫描/大对象作为独立后续版本，不临时放宽 |
| P2 | 孤儿内容文件占用存储 | 只按无引用+恢复期后的精确 hash reconciliation 回收；失败保留并告警 |

## 11. 验收矩阵

| 类别 | 必须证明 |
| --- | --- |
| manifest | 路径穿越、绝对路径、符号链接、目录、FIFO、未声明文件、重复 ID、超限数量/大小均拒绝 |
| 可用性隔离 | 存储关闭、ticket 失败、磁盘满、上传 5xx、队列异常时，聊天正文、任务终态、用户退出、既有人工 artifact 和已发布下载仍可用 |
| 客户端恢复 | snapshot 后改写 workspace 不影响上传；断网/ACK 丢失重启不重跑 Agent、不重复版本；队列损坏隔离 |
| ticket | 伪造 run、过期 ticket、撤销安装、不同 tenant/client/agent、ticket 重放到另一 run 全拒绝 |
| 存储 | 精确 scope/hash/mime/长度读回；根目录或对象符号链接/篡改拒绝；无凭据/路径泄露 |
| 会话/悬赏 ACL | 两身份两客户端交叉读取、跨会话/跨 task 猜 ID 均拒绝；授权用户可下载 exact version |
| UI | 聊天和悬赏都有成果入口；切换身份/来源不串缓存；HTML 不执行；PDF/ZIP 不内嵌；状态不误称验收 |
| 回归 | 现有 JWT artifact 上传/下载、聚义厅工作台人工传输、artifact outcomes 继续按原合同工作 |
| 发布 | 精确 API/Web/client SHA、Flow Run、同 Run 制品、feature flag、真实线上上传/下载/跨身份拒绝 readback 完整记录 |

## 12. 实施拆包、依赖与完成定义

| 包 | 产物 | 可并行关系 | 完成定义 |
| --- | --- | --- | --- |
| RB00 | 三仓 latest-develop 差异、direct-chat task binding 盘点、接口冻结 | 先行 | 无旧大分支整体合入；路径/所有权明确 |
| RB01 | storage admission、配置和 recovery evidence | 可与 RB02 并行 | 开关仍默认关闭；真实私有读写/恢复通过 |
| RB02 | 客户端 manifest/snapshot/queue/ticket client | 可与 RB01/RB05 并行 | 静态/定向测试证明 no-follow 与恢复语义；版本化提交可达 |
| RB03 | run binding、ticket、publication bridge、receipt、reconciliation | API 核心串行 | Agent 不能伪造 scope/run/agent；幂等和 rollback 通过 |
| RB04 | conversation mapping、task/conversation read adapters | 依赖 RB03 | 映射无第二份 bytes；ACL 负向用例通过 |
| RB05 | 聊天/悬赏只读 UI 和下载/预览 | 可先做 UI 契约，联调依赖 RB04 | 切换隔离、预览限制和无验收误导通过 |
| RB06 | 端到端集成 candidate | 依赖 RB01–RB05 | 实际 Agent 产出文本/图片/ZIP，两个入口 readback |
| RB07 | develop 合入与 Flow | 依赖 RB06 | 同 Run API/Web 测试、构建、制品、部署成功 |
| RB08 | 线上小范围启用、release manifest、归档 | 依赖 RB07 与客户端可达 | 真实发布/下载/拒绝 readback；开关与恢复材料齐全 |

## 13. 可用性合同与运行处置

### 13.1 不可破坏的运行合同

1. 成果发布是异步附加链路，不参与聊天响应、模型运行结束、任务租约终态或用户退出的成功判定。
2. 新写入不可用时，关闭/暂停的仅是新 output ticket 与 publication；已分享文件的授权读取、现有 JWT artifact 接口和 `artifact-outcomes` 继续独立服务。
3. 调用者永远可以安全刷新、重新登录或重新打开页面；未知网络结果只能恢复查询 receipt/列表，不能重复执行 Agent 或隐式新增 artifact version。
4. 对用户可见的失败文案必须明确范围，例如“本次成果暂未同步，聊天回答不受影响”；不得笼统显示“典籍/服务暂无法读取”或把无权限伪装为数据缺失。

### 13.2 运行处置顺序

| 观察到的实际问题 | 处置 | 不应做的事 |
| --- | --- | --- |
| 存储初始化/写入失败 | 停止新 ticket，保留队列与现有读；记录精确 I/O 错误，修复后重试原快照 | 重启 Agent、删除队列、删除已发布文件或中断聊天 |
| API publication route 异常 | 保留正常任务/聊天结果，返回可恢复状态；按 receipt/runId 追踪 | 复用用户 JWT 上传接口或让浏览器代传 Agent 文件 |
| Web 列表/下载异常 | 仅该成果面板显示可刷新状态，聊天/悬赏主体继续使用 | 清空用户会话、把 403 显示为无成果 |
| 跨身份/来源 ACL 拒绝 | 记录脱敏审计并拒绝，不泄露存在性 | 自动放宽 allowlist、使用 persona 代替 scope |

## 14. 明确的停止条件

以下任一情况不应靠绕过检查开启或扩大 R1 **新写入**：

- 不能证明 run 到 task/conversation/Agent 的精确绑定；
- 客户端版本化提交仍不可达；
- 私有 storage 的权限、hash readback 或恢复验证失败；
- 云端 Flow 对精确 develop 提交失败；
- 双身份/跨来源读取测试出现数据泄露。

停止仅限制相应 R1 写入或扩大范围；既有聊天、悬赏、人工 artifact、阅读和聚义厅功能保持独立运行。修复后以新的精确提交和 Flow Run 继续，不以旧日志、默认关闭代码或本机结果宣告交付。

## 15. 工作量、并行方式与实施计划

> 以下是 **24 小时运行的 Agent 执行周期与日历耗时估算**，不是“人工人天”。估算包含实现、自检、合入、云端 Flow、修复一次真实失败和发布 readback；不把等待下一次后端发布窗口伪装成开发工时。

### 15.1 工作量拆解

| 包 | 路径/范围 | 主要内容 | Agent 执行量估计 | 依赖 |
| --- | --- | --- | --- | --- |
| RB00 | 根仓/API/Web/client | 最新 develop 差异盘点、direct-chat task binding 取证、契约冻结 | 4–8 小时 | 无 |
| RB01 | API 配置/运维 | 私有 storage 准入、配置、恢复证据、开关接线 | 4–12 小时 | RB00 |
| RB02 | `isp-install` Runtime v1 | manifest、no-follow snapshot、私有队列、ticket/receipt 恢复 | 12–24 小时 | **客户端候选可达** |
| RB03 | API runtime/agent | binding、opaque ticket、专用 publication bridge、幂等 receipt、保守孤儿回收 | 20–36 小时 | RB00；同一 schema/ACL 路径单 Owner |
| RB04 | API chat/task read | conversation 映射、只读列表/下载适配器、ACL 负向测试 | 12–20 小时 | RB03 |
| RB05 | Web 聊天/悬赏 | 共用成果列表、预览、下载、身份切换隔离 | 12–20 小时 | 可先按冻结契约并行；联调依赖 RB04 |
| RB06 | 三端集成 | 真实 Agent 文本/图片/ZIP、故障隔离、双身份负向、问题修复 | 16–32 小时 | RB01–RB05 |
| RB07/RB08 | Flow/发布 | develop 合入、云端测试/构建、同 Run 制品、分阶段开关、线上 readback | 8–20 小时 + 发布窗口 | RB06、客户端可达 |

**总实现量**约为 88–172 个 Agent 执行小时；由于 API、Web、客户端和存储准入可并行，关键不是相加，而是 API 核心链路、客户端可达性、集成和 Flow 发布窗口。

### 15.2 关键路径与实际日历估算

```text
客户端候选可达 ─┐
RB00 ─→ RB03 ─→ RB04 ─┬→ RB06 ─→ Flow / 后端下一个 00:00 发布窗口 ─→ RB08
RB00 ─→ RB01 ─────────┤
RB02 ──────────────────┤
RB05（契约可并行）──────┘
```

| 情形 | 到“功能候选完成”的预计日历耗时 | 到“完整发布并线上 readback”的预计日历耗时 |
| --- | --- | --- |
| 客户端等价提交已在今天可达、无新增架构阻塞 | 3–5 个自然日 | 5–8 个自然日，外加后端下一次符合规则的 00:00 发布窗口 |
| 客户端提交仍不可达 | API/Web 可在 3–5 个自然日形成关闭开关的候选 | **无法对完整 R1 给出可信日期**；客户端可达是硬依赖 |
| Flow/迁移/ACL 出现一次真实失败 | 在相应阶段增加 1–2 个自然日用于定位、修复和重跑 | 以修复后的 Flow 成功和下一次发布窗口为准 |

如果客户端等价分支在 **2026 年 9 月 15 日** 可达，且没有发现新的 ACL/迁移根因，目标是：在 **2026 年 9 月 18–20 日** 形成完整 R1 线上 readback。后端实际部署仍固定为成功构建后的下一次北京时间 00:00 汇总窗口；这个日期范围会随当前时刻、Flow 排队和客户端推送时点变化。

### 15.3 具体执行顺序

#### 阶段 A：冻结边界与解除外部阻塞（第 0 天）

1. 从 API/Web 最新 `develop` 创建独立 worktree；不触碰当前脏工作区，不合入旧 `output-delivery` 大分支。
2. 对比旧候选与重基线，冻结：manifest schema、run binding 字段、ticket claims、multipart contract、conversation mapping 和 Web DTO。
3. 在 `isp-install` 远端恢复/推送 `29aa70da…` 或等价完整分支；核对该提交含 Runtime v1 的 manifest、snapshot、queue 和发布接线。
4. 建立 RB00 证据：普通聊天是否已有可靠 taskId；无 taskId 时 delivery-only task 的精确创建入口和失败降级路径。

**退出条件：** 客户端基线可达，或明确登记为唯一外部 blocker；API/Web 工作项路径无重叠。

#### 阶段 B：三个实现 lane 并行（第 1–3 天）

| Lane | Owner 范围 | 交付物 |
| --- | --- | --- |
| API core | binding、ticket、publication、receipt、迁移 | RB03；只允许一个 Owner 修改同一 transaction/schema/ACL 路径 |
| Runtime client | manifest、snapshot、queue、ticket、finish 异步接线 | RB02；不修改 `/home/isp/apps/codex-ws-agent` 运行目录 |
| Web | outputs 组件、chat/bounty 入口、缓存隔离和下载 | RB05；先以冻结 DTO mock 自检，API ready 后再联调 |
| Storage admission | 私有 root、feature flag、恢复证据 | RB01；不能启用写入，不操作生产数据 |

每个 Owner 做最小定向自检后直接合入所属 `develop`；没有独立 Reviewer 队列。API 核心更新与读映射（RB03→RB04）依赖明确，不能由多 Owner 同时写同一事务链路。

#### 阶段 C：API 读路径、三端集成与故障闭环（第 3–5 天）

1. API Owner 完成 RB04：会话映射、任务/会话只读适配器、opaque cursor 与 user-JWT ACL。
2. Web 对接真实 API：聊天、悬赏、预览、下载、身份切换/AbortController。
3. Runtime 用三个真实产物进行发布：文本、PNG/JPEG、ZIP；验证 storage 关闭、网络中断、ACK 丢失、ticket 过期、磁盘/存储失败、跨身份读取等情形。
4. 任何成果链路异常只修成果链路；聊天/任务终态、已发布读取与原人工 artifact 不回退、不重启、不被阻塞。

**退出条件：** RB06 验收矩阵全绿，且故障隔离用例证明核心业务仍可用。

#### 阶段 D：合入、Flow、分阶段启用与发布（第 5–8 天）

1. API/Web/客户端精确提交合入 `develop`；先部署 schema/兼容代码，两个 R1 新写开关维持关闭。
2. 使用 API Flow `5260799`、Web Flow `4403172` 对 exact develop commit 运行正式测试、构建、同 Run 制品与部署；不使用本机 Gradle/Vite 生产构建替代。
3. 在明确测试 scope 开启 storage 与 R1 output 写入，完成线上真实上传、聊天取件、悬赏取件、跨身份拒绝、退出/重登后的 readback。
4. 成功后扩大范围；失败立即关闭**新写入开关**，保留核心功能和已有读路径，修复后按新 SHA 重新走 Flow。
5. 将 root/API/Web/client SHA、Flow Run、制品摘要、开关、storage 恢复证据与线上 readback 写入 release manifest，达到完成定义后再归档。

### 15.4 资源与职责约束

- 推荐同时运行 4 个 lane：API core、Runtime client、Web、storage admission；RB06/Flow 期间收敛为集成 Owner + 各路径 Owner 协同。
- 不设置“全局唯一源码 Writer”，但同一 API schema/ACL/事务路径仍只能有一个实现 Owner；worktree 和路径边界必须明确。
- API/Web 正式测试、构建、制品和发布只走 Flow；重型资源按实际互斥等待。
- 不创建独立 Reviewer。责任 Owner 自检、合入 develop，再由云端 Flow 和线上 readback 作为发布证据。

## 16. 范围修订：`isp-install` 不属于当前版本（2026-09-15，优先级最高）

用户已明确：`/home/isp/wsps/chcbz/isp-install` 及其客户端发布不在当前需求范围。本节覆盖本文此前任何将 Runtime v1 客户端、`29aa70da…`、manifest、安全快照、私有队列、客户端 ticket 交换或客户端发布接线列为本版本前置、工作包或发布条件的表述。

### 16.1 当前版本重新定义

当前 `1.3.0` 交付的是 **服务端成果目录与用户取件 R1**：

- 复用已经存在的 `agent_task_artifact`、私有 `AgentTaskArtifactStorage` 和 `artifact-outcomes`；
- 将现有、已被服务端正确发布的 task artifact 安全映射到聊天和悬赏详情，提供列表、有限预览和精确下载；
- 修复/补齐 user-JWT 的读取 ACL、会话映射、缓存隔离、可用性降级和 Web 用户入口；
- 不开发、不发布、不要求修改任何 `isp-install` 客户端代码。

**本版本不宣称实现“Agent 工作区自动导出文件”。** 当前 API 虽有 `artifact.publish` 协议常量，但 `AgentWebSocketHandler` 对该入站消息仍是 deferred handler；它不是已可用于生产的客户端上传能力。manifest、run-bound ticket、multipart publication bridge 和客户端恢复队列转入后续单独的 **Agent Runtime 输出协议版本**，届时再从端到端客户端需求立项。

### 16.2 当前唯一成果来源

R1 只展示服务端已有的、满足以下条件的 artifact：

1. 已通过既有 `AgentTaskArtifactService.publish` 进入 `agent_task_artifact`；
2. 已有精确 tenant/client/task、版本、hash 和可读 visibility；
3. 若要在聊天中显示，服务端能用可信 task/conversation 关联写入 `conversation_deliverable` 映射。

R1 不接受浏览器上传、不接受未经实现的 WebSocket `artifact.publish`、不从 Agent 工作目录扫描文件，也不因聊天文本里提到“已生成文件”而创建记录。若当前线上尚无满足上述条件的 artifact 生产方，R1 页面应稳定显示“暂无可领取成果”，不能冒充已支持自动导出。

### 16.3 仍需实施的 API/Web 设计

| 工作项 | 当前版本保留 | 说明 |
| --- | --- | --- |
| RB00 | 成果来源盘点和 task↔conversation 的可信关联 | 确认现有 `AgentTaskArtifactService.publish` 调用路径；没有可信关联则不映射聊天 |
| RB01 | storage 准入与内容完整性 readback | 仅启用既有私有文件系统 storage；不引入对象存储/扫描器 |
| RB03A | 用户只读成果目录 | task/conversation 列表、精确下载、user-JWT ACL、opaque cursor、无泄露错误语义 |
| RB04A | conversation deliverable 映射 | 只引用既有精确 task artifact version；不复制字节或 storage URI |
| RB05 | Web 聊天/悬赏入口 | 共用只读组件、下载、有限预览、身份/会话缓存隔离 |
| RB06A | 集成与可用性回归 | 使用既有服务端 artifact 生产路径验证；不依赖客户端改造 |
| RB07/RB08 | Flow、分阶段开关、线上 readback | API/Web 发布；没有客户端 release 前置 |

移出本版本：原 RB02、run binding、opaque ticket、Agent publication multipart endpoint、publication receipt、客户端 snapshot/queue，以及相应的客户端候选可达性检查。

### 16.4 修订后的工作量与日历计划

| Lane | 估计 Agent 执行量 | 可并行性 |
| --- | --- | --- |
| API 来源盘点、read ACL、conversation 映射与迁移 | 20–36 小时 | API transaction/schema 路径单 Owner |
| Web 聊天/悬赏成果入口 | 12–20 小时 | 可按冻结 DTO 与 API 并行 |
| storage 准入、可用性/回归用例 | 8–16 小时 | 与 API/Web 并行；不启用新写入 |
| 集成、Flow、线上 readback | 12–24 小时 | 依赖前三项 |

总量调整为 **52–96 个 Agent 执行小时**。若没有发现来源归属或 ACL 的新根因，预计 **2–3 个自然日形成 API/Web 候选、3–5 个自然日完成 Flow 与线上 readback**，再受后端成功构建后的下一个北京时间 00:00 发布窗口约束。

当前关键风险不再是客户端提交不可达，而是：**现有 artifact 是否确实由可信生产路径写入，以及聊天与 task 的关联是否可精确证明。** 这两个问题由 RB00 在实现前给出事实结论；不能证明时，保留 task/悬赏入口，聊天入口只显示空态，不凭猜测映射数据。
