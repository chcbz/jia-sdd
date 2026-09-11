# 产物交付详细设计 v1.1

设计状态：已细化并通过独立只读复核，无设计级阻塞；实现状态：OD00、OD01 开发门槛已通过，OD02 评审修复中，详见 [task-ledger.yaml](task-ledger.yaml)。本文是 [design.md](design.md) 的实施细化；v1.1 的交付范围与传输取舍以本文为准。机器可读契约见 [openapi.yaml](openapi.yaml)、[schema-contract.yaml](schema-contract.yaml)、[fixtures.json](fixtures.json)。

## 1. 两个可独立验收的版本

| 项目 | R1：用户先拿到文件 | R2：正式悬赏交付与验收 |
| --- | --- | --- |
| 对话 | 自动采集 manifest 指定文件，列表/下载，文本/图片预览 | 复用 R1 |
| 悬赏 | Agent 显式分享文件给发布人，显示「已分享，未正式验收」 | 新建单 Agent 任务要求正式提交、人工验收、返工 |
| 状态 | 保留旧任务执行状态，另显文件同步状态 | 持久 deliveryPolicyVersion=1，禁止 legacy 完成绕过 |
| 范围 | 受控输出目录、整文件重传、API 代理下载、列表轮询 | 同一字节服务、租约 HTTP 适配、冻结批次和审计 |
| 暂缓 | Agent 跨会话聚合页、目录浏览、分片/ZIP、Office/PDF 内嵌预览 | 多工作项联合验收、跨用户委托、资金结算、WS 成果写入适配 |

R1 的悬赏分享不是缩小权限检查：只有生产者对自己的指定成果明确 `publishToOwner=true` 才建立 OWNER_SHARE 授权；默认 false。私有/审核资料不因同 scope 或拥有 Agent 自动开放。R1 不标记已验收，不宣称文件存在使任务完成。

R2 先限制新策略任务 `maxAgents=1` 且只有一个 required work item；服务端在创建、组队、增工作项、自动点将等入口硬校验。既有多人任务保持 policy=0，仍可显式分享文件，不改变旧聚合规则。多人正式交付另扩展，避免本轮引入联合批次/部分验收状态机。

## 2. 缩短周期的固定技术决策

| 决策 | v1.1 选择 | 减少的工作 |
| --- | --- | --- |
| 传输 | HTTP 是上传、发布、租约、提交的唯一首发写入口 | 不同时实现和联调 HTTP/WS 两套 DTO/回执 |
| WS | 只增加受绑定会话保护的 `output.auth.request/receipt`，并在派发中添加 outputContext | 不开放目前 deferred 的 work.result/artifact.publish，且不谎报支持 |
| 存储 | 一个私有 S3 兼容适配器，流式经过 API；OSS 使用其兼容端点须先探测 | 不同时开发多个云 SDK、签名直传、分片和浏览器 CORS |
| 数据归属 | 字节基础设施进入 agent 模块，chat 通过 agent-api 的来源授权 SPI 对接 | 不新增 Gradle 模块，不建立 agent → chat 反向依赖 |
| 刷新 | 打开/操作后刷新，前台有待同步任务时 5 秒轮询，后台暂停 | 不让新增持久 SSE/复杂 reducer 成为首发前置 |
| 采集 | manifest + 指定输出目录，辅助脚本写 manifest | 不依赖新增 MCP 服务、自然语言路径解析或全盘监视 |
| 验收 | 单 Agent、单 required work item、人工整批验收 | 推迟多人部分验收与自动审核引擎 |

已有 `chat-service → agent-service` 依赖可直接复用。`OutputStorage` 接口与 DTO 放 agent-api/core；存储实现、通用元数据和引用 DAO 放 agent-service/mapper 的 `output` 包；chat_output 仍放 chat 模块。由 chat-service 实现 `OutputSourceAuthorizer` 的 CONVERSATION 分支，通过注入的 handler registry 被 agent-service 调用；agent-service 不引用 chat 类。TASK 分支由 agent-service 实现。扫描到两个相同 sourceType handler 时启动失败。

成立前提：当前聚合应用在同一数据源和 Spring transaction manager 下加载 agent/chat（OD00 验证）。跨独立数据库部署不在 12～18 人日估计内；若探测不成立，先修正部署契约并重估，不把跨库写入当成本地事务。

## 3. 模块、类和文件责任

| 仓库/模块 | 拟增或修改落点 | 职责 |
| --- | --- | --- |
| agent-core | `cn/jia/agent/output/dto`、entity | 线协议 DTO、实体、错误码、状态常量 |
| agent-api | `cn/jia/agent/output/OutputStorage`、`OutputSourceAuthorizer`、`OutputApplicationService` | 接口；不依赖 chat/web 层 |
| agent-mapper | `cn/jia/agent/output/dao` 与 `resources/db/output-delivery-*` | scope 精确 SQL、schema 与增量迁移 |
| agent-service | `cn/jia/agent/output/api`、`service`、`storage`、`jobs` | 用户读、Agent 写、对象校验、GC、引用、auth ticket |
| agent-service | `AgentWorkItemLeaseServiceImpl`、`AgentWorkItemResultCommitServiceImpl`、兼容/聚合服务 | R2 租约复用、唯一正式提交、policy 禁入 |
| chat-service | `JuyitingAgentRelayService`、`HallActionDispatcher`、`AgentWebSocketHandler`、新增 output 包 | 可信 run 派发、身份交换、会话成果服务与精确授权 |
| chat-mapper | ChatOutput DAO、严格 conversation owner 查询 | 拒绝 tenant=0 回退、核对持久 jiacn |
| client | `output-manifest.mjs`、`output-exporter.mjs`、`output-queue.mjs`、`output-http.mjs`（拟增） | schema 校验、安全快照、持久队列、HTTP 重试 |
| client | `agent-client.mjs`、`workspace-manager.mjs` | run 上下文、finish 顺序、聊天/命令统一采集 |
| Web | `components/outputs/OutputCard.vue`、`OutputList.vue`、`OutputPreview.vue` | 共用成果展示；不推断业务权限 |
| Web | `composables/useOutputs.js`、`utils/outputDownload.js` | 请求取消/分页/轮询/鉴权 Blob 下载 |
| Web | `ChatPanel.vue`、普通聊天消息与会话层、`BountyPanel.vue`、`TaskWorkspacePanel.vue` | 两个用户入口，复用原 map/roster/点将不变量 |

R1 不开放通用远程 Agent 工作空间读 API。普通未转发到外接 Agent 的模型会话不宣告文件能力；需要覆盖新增来源时必须建立相同 trusted run 绑定。

## 4. 标识、身份与凭据

所有 scope/owner/id 为原值精确匹配，SQL 使用 VARBINARY 或二进制比较；不得 trim、Unicode 归一化或大小写折叠。旧 BIGINT 会话 ID 在线协议中用规范十进制字符串，不经过 JS Number。新资源 ID 使用服务端或客户端生成的 32 位小写 UUID hex（外部 ID 总长不超过 100）；不得使用文件名作为主键。

用户主体仅来自 JWT 的 `(jiacn,client_id)`；二者映射到现有单用户 scope，不猜测额外组织租户。用户下载不能携带 actorAgentId 切换身份。source binding 在创建时记录不可变 owner；历史来源只有经严格 scoped 查询并核对持久 owner 才回填，tenant=0/归属冲突失败关闭。

服务端在现有已授权派发路径创建 `output_run_binding`，关联真实 task/conversation、producer、bindingId、原 runtimeInstanceId、commandId/messageId、交付策略与 24 小时恢复截止。向目标 Agent 单播 outputContext：`schemaVersion,runId,source,maxFileBytes,maxBatchBytes,manifestRelativePath,capabilities`。不得把 commandId/messageId 的本地 fallback 当 taskId，也不把 runId 直接当授权。

客户端在已绑定 WS 请求 `output.auth.request {schemaVersion:1,messageId,runId}`；处理器核对 session scope、producer、当前 bindingId/吊销状态和源业务授权，单播 `output.auth.receipt {causationId,runId,token,expiresAt,operations}`。token 为随机 256-bit opaque bearer，服务端仅存 SHA-256；15 分钟有效，audience 固定 output-api，权限为 run/source 绑定的 upload/publish/status，R2 有效任务另给 lease/submit。请求和回执禁止广播、落聊天或日志。

Agent HTTP Authorization 使用该 ticket；用户 JWT 不能调用 Agent 写接口。token 不进入 prompt/manifest/子进程环境，在桥接进程内存保存，断线重启重新通过绑定 WS 取得；source/producer/binding 的动态有效性每次 mutation 再查。原 runtime 记录用于溯源，上传恢复可由相同未吊销 binding 的新已认证 runtime 执行；这不授予旧 work lease，新策略提交仍必须匹配服务端当前 lease/CAS。重新派发、换 Agent、撤权或恢复截止后拒绝新的发布/提交，已发布用户副本继续保留。

对象 ticket 不授予 arbitrary URI、文件路径或管理员权限。限频默认每 binding 60 次 auth/min；超限 429。token 元数据在 `output_access_ticket` 独立表持久化，过期批量清理。

鉴权引导例外：尚无主体时，只允许用服务端计算的 bearer SHA-256 精确查询 `BINARY(32) ticket_hash`，由持久行建立 scope；请求传入的 tenant/client/run/binding 不得决定主体。此后资源和业务查询必须使用行派生的精确 scope 并动态校验授权，仍遵守同一未撤销 binding 的新 runtime 恢复规则。普通资源 ID 不享有无 scope 查询例外。签发限频在同一精确 binding 行锁下完成窗口计数与 ticket 插入，可添加非唯一索引 `(tenant_id,client_id,binding_id,created_at)`。

身份事务锁顺序：业务 source root → output_source_binding → output_run_binding → agent_persona_binding → agent_identity_registry → agent_runtime → output_access_ticket 精确行/窗口范围。TASK 先锁 task root 与精确 member；任务关联会话先锁 task/member，再锁会话持久 owner 行。非锁投影仅用于发现键，持锁后重读授权信息。该顺序保留既有注册/解绑/status 的 binding → identity → runtime 前缀；已持身份锁的路径不得反向获取 source/run 锁。具体依据见 [identity-lock-order-review.md](evidence/OD01/identity-lock-order-review.md) 与 [repeatable-read-review.md](evidence/OD01/repeatable-read-review.md)。

MySQL RR 下，签发限频不能在早期投影已建立快照后使用普通 COUNT；持同一 canonical binding 锁后，按 binding-window 索引执行有界 `LIMIT 60 FOR UPDATE` 当前读并计行数。HTTP 鉴权完成 source/run/identity/runtime 锁后，再以同一 hash 当前锁读 ticket；核对两次读取的不可变 scope/run/source/producer/binding/operations，依据 locked run/ticket 重验状态、撤销与权限，并在锁等待后重新取时钟检查 expiresAt/recoveryUntil。纯 ticket 撤销/清理可以独立执行，但不得持 ticket 锁后回取前序锁。

终态恢复：RESULT_SUBMITTED/CLOSED 在恢复期内允许同一未撤销 binding 的已认证新 runtime 换取仅含 `status` 的 ticket。来源 SPI 使用显式只读回执模式，允许具有精确 READ_ONLY 历史成员权限的来源，仍拒绝 LEFT/REJECTED/越界或已撤销身份。终态服务鉴权仅接受内部 `requiredOperation=status, receiptReplay=true`；旧 ACTIVE 时签发的全权限 ticket 也不能再授权 upload/publish/submit。

## 5. 数据模型与唯一约束

[schema-contract.yaml](schema-contract.yaml) 定义每表字段类型、可空性、索引、阶段和不可变字段，是生成 mapper/迁移审查清单的输入，**不是可执行迁移**。所有表 InnoDB，同数据源；时间为 epoch ms BIGINT，所有 bigint/version 在线协议为十进制字符串。业务审计、错误码限制长度；正文 TEXT/MEDIUMTEXT 仅用于受大小限制的文本，不保存二进制。

| 核心约束 | 实施要求 |
| --- | --- |
| 版本唯一 | task 沿用 `(tenant,client,artifactId,artifactVersion)`；chat 同等 outputId/version |
| 来源唯一 | `(tenant,client,sourceType,sourceId)`；owner 创建后不可更改 |
| 幂等唯一 | `(tenant,client,actorKind,actorId,operation,idempotencyKey)`；source/version 纳入 request digest |
| 上传写入 | 每 uploadId 同时仅一个未过期 writerEpoch；数据写不同 immutable staging key，过期旧 writer 不可 finalize |
| 对象引用 | 所有 objectId 关联同 scope；禁止仅按 ID 或 hash 查找后授权 |
| 当前批次 | R2 task meta current_delivery_id + version CAS；同 task 的 revision 唯一 |
| 审核唯一 | 一个 delivery 只允许一个最终决定；重试返回相同 receipt，不允许修改结论 |
| 内容互斥 | 正文/受管 objectId/历史 external URI 三选一；新写默认拒绝任意外链 |

`output_object_reference` 同时承担字节保留与部分发布授权的事实，但二者不可混淆：ROLE_CANDIDATE 只沿用 Agent 协作 ACL；OWNER_SHARE 明确给 source owner；DELIVERY_PIN 只经正式提交事务创建；READ_PIN 仅延长传输保留、不赋予新的读取主体。每条引用都带来源版本和 optional deliveryId；不能发现任意 ACTIVE 引用就让调用者读对象。

内联成果无 objectId，不能因此跳过 owner/share/delivery ACL；版本过期与发布授权放业务版本字段及交付清单，文件对象引用仅用于字节存活。R1 正文长度沿用 256 KiB UTF-8 限制。

## 6. 上传与登记：可恢复步骤

1. `POST output-uploads`：校验 ticket/source/run、name（仅 basename）、size/hash、配额。在短事务内锁 source → run → 幂等行 → scope 配额行，预留 expectedBytes，创建上传/对象槽位；返回 uploadId 和相对同源 uploadUrl。拒绝客户端传 bucket/key/URI。
2. `PUT .../content`：短事务 CAS 领取上传 writerEpoch，并预登记该 epoch 的持久清理行后才允许外部写入。`writer_until` 为 5 分钟可续租约，`writer_deadline_at` 固定为该 epoch 首次领取后 10 分钟、续租不得越过；upload 的 24h 会话期限固定于 create。提交后流式读取，边读边哈希/限额/类型探测，将 bytes 写到包含 uploadId/epoch 的唯一 key；写入不覆盖其他 epoch。读不持 SQL 锁。
3. 完成后以 writerEpoch、sessionVersion CAS 写 size/hash/object key；当前 binding/run 已失效或 epoch 丢失则只留下可清理 staging，不得 READY。校验失败 REJECTED；未写入的预留可释放，已写入或仍可能被迟到 writer 写入的存储占用须待物理清理确认后释放。中断可由新 epoch 全文件重试，原文件快照不重新生成。
4. `POST complete` 触发持久验证 job，并固化该请求的 HTTP 状态与响应正文；相同幂等键始终返回原回执（如首次 202/VERIFYING），即使对象后来已 READY。客户端通过 `GET upload` 查询后续状态。摘要不符返回 422，格式拒绝按 OpenAPI 返回 415/422；扫描服务不可用保持 VERIFYING 并重试，不能旁路通过。超过 24h 会话过期，客户端可在有效 run 下创建新 uploadId 重传同一快照。
5. READY 后 `POST artifacts` 或 `POST outputs` 登记：统一锁序，校验对象 PASSED/READY、同 run/source/producer、版本 predecessor、publishToOwner；原子写业务版本、引用和 receipt。task 复用已有 ARTIFACT_PUBLISHED 事件类型及严格 payload 格式；不创建任意新类型使旧回放失败。
6. chat 首发不依赖持久事件推送，消息卡片通过 runId/conversationId 的列表请求发现。HTTP 成功丢包由相同幂等键重放返回确切版本；客户端不得擅自 version++。

默认限制：50 MiB/文件、200 MiB/run、100 文件/run；scope 暂存+正式对象总额 1 GiB，2 个并发上传/binding、8 个/scope，均配置化；scope 聚合配额需要数据库行锁/CAS，不能先 count 后无锁插入。预留 → 实际占用 → 物理删除后释放；重复重试不重复计费/占额度。30 天对话/OWNER_SHARE 引用，SUBMITTED 无自动到期，ACCEPTED 至少 90 天，hold 优先。

OD02 内部持久模型补充：binding 配额行保证空集合下的并发名额原子性；run 配额行分别累计 create 成功数与领取 epoch 的 expected_size，默认上限为 `run.max_files*10` 和 `run.max_bytes*10`，失败不退、receipt 重放不增加，零字节及未开始 PUT 的请求同样受请求数限制。文件业务额度只预留一次，但每个尚未物理清理的旧 epoch 都保留独立 scope 预留；转移给 cleanup job 时不释放，删除失败继续占用。验证和删除的 attempts/next/lease 字段存库，重启可重新领取。字段与索引见 `schema-contract.yaml`。

R1 使用受限 MIME allowlist：纯文本/Markdown/CSV/JSON、PNG/JPEG/WebP、PDF、ZIP、DOCX/XLSX/PPTX。内容探测与扩展名不符拒绝；Office ZIP 结构识别需有界读取，禁止宏类型；杀毒扫描接入一个部署就绪的隔离扫描器（建议 ClamAV sidecar），流式接口/资源限制在 OD00 锁定。未部署扫描器时功能不宣告 READY，不能用“只下载”替代扫描。HTML/SVG/可执行文件本轮不接收；PDF/Office/ZIP 只下载，不在主站预览。所有格式仍可能包含业务敏感信息，manifest 显式发布是必需边界。

OD02 扫描资源边界：ZIP/OOXML 每成员实际展开不超过 50 MiB；全树总扫描预算默认 90 MiB，按“上传对象本身字节 + 每一层各成员实际解出字节”累计，不能只加叶子或每层重置。全树最多 2048 条目，根 ZIP 为第 1 层、最大 3 层；应用配置与部署扫描器能力配套，不能单独放大。ZIP 嵌套按 magic 识别并递归共享预算；其他已识别且不支持的压缩/归档格式、加密、损坏与不支持方法拒绝。成员声明大小只能辅助，实际读取计数才是门槛。200 MiB/run 的业务字节配额不变。

展开采用顺序有界流；需递归的单个 ZIP 成员才暂存到私有目录/随机临时文件（目录 0700、文件 0600），绝不按 entry path 落盘，深度优先完成后立即删除。总展开内容不累积到 heap。确定性格式/资源错误进入 REJECTED；临时 I/O 故障保留 VERIFYING 供持久重试。工作在验证 lease 领取后的外部处理阶段，不持 SQL 锁，最终 READY 仍需确认 scanner clean 及当前业务授权。部署至少核验 ClamAV `MaxFileSize 60M`、`MaxScanSize 100M`、`StreamMaxLength 60M`、`AlertExceedsMax yes` 与实际行为；扫描器更紧时须同步收紧应用，未核对前不得启用 READY。依据与限制见 `evidence/OD02/clamav-limit-review.md`。

## 7. 幂等、锁序与 GC

POST 操作统一 Idempotency-Key（16～100 ASCII）；request hash 对严格解析后的已知字段用 RFC 8785 canonical JSON 再 SHA-256，拒绝重复 JSON key、未知字段、重复 items 和非法数字。lease回执含业务leaseToken，允许在受保护receipt中保留，只对同一合法run-ticket重放，不进入用户接口/日志；output auth bearer不落receipt。文件字节另用流 hash；PUT 由 uploadId+expectedHash+writerEpoch 管理，不另造业务幂等键。

终态的原 POST 重放不新增 HTTP 端点：服务端由路由固定 originalOperation，并由持久 ticket/run 推导只读回执候选分支，以 `status + receiptReplay` 鉴权，锁后再次确认终态。随后在 run 锁之后用当前/锁读查既有 receipt，精确匹配 scope/run/originalOperation/idempotencyKey/canonical body hash 及资源/actor 绑定后原样返回。缺失或不符即拒绝，不创建 receipt、不转入 mutation，也不在同事务升级为 WRITE 模式。客户端不能提交 readMode/receiptReplay/originalOperation 来选择该分支。ACTIVE 新请求仍使用原操作权限与 WRITE 来源授权；成功状态变化与 receipt 同事务提交。具体实现归 OD02/OD08。

先鉴权再查 receipt；同参数成功重放返回原 HTTP status/body（不得含 output bearer/存储签名 URL），同键异参 409 IDEMPOTENCY_CONFLICT。成功/终结性业务拒绝写 receipt，409 VERSION_CONFLICT 含调用者已获授权的 currentVersion，修正业务意图需新 key；503 与传输失败不记终结性 receipt。lease/upload receipt 保留到 run 恢复截止后7天，成果登记/提交/审核 receipt 至少保留到资源保留期结束后7天，R2 提交/验收审计不得因去重缓存过期重做。

统一事务锁序：source 根 → run（需要时）→ 幂等 receipt → workItem（需要时）→ delivery（需要时）→ quota（需要时）→ upload（需要时）→ 排序后的 object → reference。同一 task 的 source 根就是现有 task root；CONVERSATION 则是 source_binding。引入任何复用 service 前检查它是否反向锁以上行；不能只依赖文档声称不死锁。外部网络调用一律放事务外。GC 只按 quota → object → reference 的后缀顺序锁行，决不反查并锁 source/workItem。

OD01 身份锁在 run 后、receipt 前完成，HTTP filter 不替代 mutation 事务内的动态授权。OD02 quota 子序为 scope → binding → run-upload-quota；只触及所需行。cleanup 与 upload/object 的锁顺序须统一，不能由清理 worker 先锁 job 再反向进入业务事务。无正文的 `completeUpload` receipt 使用服务端构造的 `{"runId":"…","uploadId":"…","operation":"completeUpload"}` 做 canonical JSON hash，避免同 key 被移到另一条 upload 路由；public POST 不新增正文或分支选择参数。

所有引用更改与 object DELETING CAS 在同一对象锁下串行；GC 检查无 ACTIVE 有效引用/pin/hold 和无活跃上传，标 DELETING 提交后清除存储字节，完成后 DELETED 并释放实际配额。OD02 单 PUT 存储协议通过同 key 的零字节 tombstone 替换并核验来清除字节，防止迟到写入重建；它与 SQL 的 DELETED 状态是两个不同层次的记录。失败重试不复活对象；生成新引用只允许 PASSED/READY。到期引用转 EXPIRED 后不能借其他来源仍保存对象而恢复访问。

引用锁协议补充：新建引用/READ_PIN、续期或加 hold 都属于增加保护，须在精确 object 锁下重验 PASSED/READY，再锁写 reference。释放、无 hold 到期转 EXPIRED、清除 hold 只允许单调减少保护，可在 READY/DELETING/DELETED 下于 object → reference 锁序幂等执行；不得顺带延长期限、复活终态引用或改绑对象。expiry worker 无锁枚举后必须锁下重读 scope/object/key、ACTIVE、hold=false 和到期时间。DELETED 对象行保留供这些操作串行化；异常缺失作为一致性错误，不能绕过锁。cleanup finalize 使用 scope quota → object → cleanup job，过期 CLAIMED/DELETING lease 可由新 worker CAS 重领，旧 epoch 清理仅释放其自身占用，只有确切当前 bucket/key/version 的 fence 才能推进对象 DELETED。

下载先校验业务权限/版本有效期/对象状态，建立 READ_PIN。流下载硬上限 10 分钟，pin 默认 11 分钟、每 30 秒续至传输期限；完成即释放，进程崩溃自动到期，过期不会无限占用。业务撤权后新请求拒绝；已开始的流最多持续当前传输期限，在产品契约说明。首次版本不生成签名 URL，减少泄漏及撤销窗口。

## 8. 文件清单与客户端行为

manifest 路径来自 trusted outputContext，限定本次 `outputs/<runId>/manifest.json`；内容样例见 fixtures。schemaVersion=1，最多 100 items，总 manifest 128 KiB。只允许 `outputId,title,relativePath,artifactType,publishToOwner`；没有 tenant/source/Agent/token 权威字段。首次 ID 生成后写盘稳定保存，重传不能重分配。manifest 指定的文件必须位于本次导出根中；跨目录已有文件需要显式用户导出命令复制到该根，R1 不开放任意根。

CLI 辅助脚本只更新 manifest，不持网络凭据；网络操作由桥接进程完成。finish 顺序：等待模型执行结束 → 验证/读取 manifest → 在本地 workspace 锁内完成安全快照（copy+fsync、校验普通文件、逐级 no-follow）→ 持久 queue 事务性落盘 → 释放锁 → HTTP 上传/登记。聊天也申请每 run 输出根的本地锁，不复用未隔离的共享目录。

队列放桥接进程私有 state root（0700，文件0600），不在模型可写工作目录。每条记录保存 run/source、outputId/version、snapshot hash/path、uploadId、状态、幂等键、重试次数，不存 bearer 明文。原子 tmp→fsync→rename→fsync(dir)；每 binding 单消费者/文件锁；队列损坏隔离并告警，不猜测记录已成功。

状态：SNAPSHOTTED → UPLOADING → VERIFYING → REGISTERING → PUBLISHED；可重试网络错误加指数退避（1/2/4…60 秒，上限 24h，带抖动），认证错误重新交换一次 ticket；权限撤销/源不存在进入 BLOCKED，不无限重试。手工“重试同步”只能继续已有快照。R2 正式提交独立 DELIVERY_PENDING 队列，必须在所有必需成果 PUBLISHED 后调用 submit；失效 lease 明确提示需重新授权/重新领取，不能重用旧完成命令。

文件内含模型自己声称成功不是采集条件；有 manifest 才发布。无 manifest：普通问答正常返回文本；有明确 files 交付要求则提示缺产物且不能正式提交。R1 先支持由 Agent 生成的文件，不承诺从全部历史工作目录自动找回产物。

## 9. R2 租约、提交、返工的唯一闭环

HTTP `POST work-items/{id}/lease/{action}` 支持 claim/start/heartbeat/release，复用现有 AgentWorkItemLeaseService。agentId 从 ticket 注入，不接受正文覆盖；expectedVersion 为十进制字符串，start/heartbeat/release 必须带 leaseToken。默认 TTL 120 秒、40 秒心跳，现有默认最大900000ms，120000ms符合该边界；OD07再核对实际配置。单客户端串行化心跳和 submit，提交前停止并等待 in-flight 心跳回执，使用最新版本。412/409 不能当作继续执行的许可。

新策略任务从创建即 policy=1。lease claim 之后 start，上传等待期间有界续租（单次 run 硬上限 24h）；`submit` 取 task/source 根锁，校验当前单 workItem、producer、运行绑定、leaseToken/until/version、expectedTaskVersion，所有项同 source、已发布确切版本且可对 owner 分享。

同事务：创建 revision/delivery/items → 写冻结清单成果（已有 artifactType=summary）→ 建立 DELIVERY_PIN（包括仅正文的 owner 交付授权）→ 工作项 CAS 为 submitted、保存 resultArtifactId/resultDeliveryId 并释放 lease → task currentDeliveryId/version → 写既有 work-item/任务事件和 receipt。`TaskDeliverySubmissionService` 是唯一事务入口；旧 result commit 对 policy=1 拒绝或委托，legacy report/直接状态更新/新增协作者均硬拒绝绕过。

验收 ACCEPT：source/task → receipt → workItem → delivery → object/ref 顺序锁；确认 currentDeliveryId、deliveryVersion、taskVersion、submitted workItem 绑定的 resultDeliveryId 相同；校验交付引用/对象可用，写不可修改 review，delivery ACCEPTED，workItem completed，聚合 task completed，延长 pin，写既有事件/receipt。重复相同 key 回原值；不同 key 对终态拒绝 409。

要求修改 CHANGES_REQUESTED：相同锁序写 review、delivery 终态及原因，保留上一批次/pin；workItem 转回现有 `ready` 可领取状态（源码 SUBMITTED→READY 允许），清除当前 resultArtifactId/resultDeliveryId、submittedAt/completedAt/lease，version++；task.currentDeliveryId 清空并重算为可工作非终态。新执行必须经已有 command 派发并领取新 lease，run 新建。首次 R2 不自动派发返工命令，UI 提供“重新执行”明确操作，避免用户刚提交意见就重复扣算力或启动多次执行。下一批 revision+1、supersedesDeliveryId 指向旧批次。

已 CHANGES_REQUESTED 的旧批次可读作历史，不能被再次验收；撤回已验收结论/部分验收/取消进行中的正式任务不在本轮开放范围。SUBMITTED pin 若长时间未处理留待人工管理并告警，不能静默自动接受或删除。

提交授权精度：这里“可对owner分享”指生产者有权在本次submit事务创建DELIVERY授权，**不要求预先存在OWNER_SHARE**。ROLE_CANDIDATE可以一直保持发布人不可读，直到提交事务一起创建批次和DELIVERY_PIN（内联正文则由交付条目授予同样权限）。R1的publishToOwner是独立的主动分享选择，不是R2正式提交的前置步骤。

## 10. API、列表与 UI 细节

OpenAPI 文件冻结 R1/R2 路径、认证、请求/响应 schema、幂等 header、错误；对比旧草案增加 exact version 列表和 lease 操作，**不开放 WS 的同义写入处理**。错误结构在这些新增端点统一为 `{code,message,retryable,requestId,details?}`，成功采用 `{code:"E0",data:...}`；下载成功为二进制。别直接把普通 Result 业务错误套成 HTTP 200；frontend useHttp 需同时判断 HTTP 与 envelope。

列表返回 `{items,nextCursor,snapshotAt}`，limit 默认20最大100；游标为签名 opaque token，绑定 scope/source/filter 和 snapshotAt，过期15分钟。按 createdAt DESC/outputId DESC/version DESC 排序，后续查询限制 createdAt<=snapshotAt；新写入通过刷新第一页看到。每页实时过滤当前 ACL，不能泄漏被撤权项的标题/计数。不要把 cursor 解码后信任客户端重写 source。

共用 OutputSummary：source、outputId/version、title、name、mime、size/hash、producer展示、createdAt、state、publicationKind、previewKind、canDownload；绝不返回 bucket/key、绝对路径或 API token。R1 publicationKind 为 CONVERSATION_OUTPUT/OWNER_SHARE/INTERNAL，R2 增 DELIVERY。UI 不从 canDownload 推导验收权，reviewActions 来自 delivery 详情的服务端授权结果。

useOutputs 按登录身份 fingerprint+source 建 cache key；切换会话、登出、组件卸载取消 AbortController、清除列表及 Blob URL，过时响应不可回填新会话。同步中前台轮询每5秒，完成即停止，失败退避至30秒；打开面板/窗口恢复可见/发布或验收成功后刷新。

下载用带 JWT 的 fetch 获取 Blob，再触发浏览器保存，文件名读取安全 Content-Disposition；不把 JWT 拼入 URL。只内嵌 <=1 MiB 文本/Markdown（转义/DOMPurify）和受限尺寸位图预览，图片尺寸解码过大拒绝预览但可下载。其他类型显示“可下载，暂不支持预览”。客户端 Blob 在操作后释放，单文件50MiB上限与移动内存联测。

微信壳 R1 使用同账号网页成果页作为取件位置：页面只含 resource route，不含 token；若 WebView 无法保存则展示“在浏览器登录后下载”指引。正式宣告微信可取件前必须验证该外部浏览器路径可到达且可完成同账号登录；原生 bridge 不是 R1 前置，但若真机无可行路径则微信场景不通过发布门槛。

## 11. 迁移与可操作发布步骤

1. OD00 检查依赖/作用域/事务管理器、存储和扫描器；record evidence，不执行业务迁移。
2. M001 新建 output 元数据/引用/receipt/quota/ticket 表与 chat_output；M002 给现有 task artifact 加 object/run/display/publish 字段，所有增量可空且旧读兼容。schema initializer 与 SQL 使用同一结构清单；历史 tenant=0 不自动改 owner。
3. 部署 R1 API 开关关闭，strict schema validation 和存储上传/读/删探针通过后只开放测试 scope；升级一个 client，再发 Web。做聊天文件、悬赏显式分享、离线下载、跨用户拒绝验证后扩大用户范围。
4. M003 新增 delivery 表和 task meta policy/currentDelivery/revision，workItem resultDeliveryId；存量 policy=0，新任务默认先0，所有 R2完成禁入检查上线后才按 allowlist 新建1。
5. R2测试 scope 核验 claim/start/heartbeat/submit/review/change-request 全链路，且 legacy bypass 被拒绝，再开放新建单 Agent 正式交付任务。
6. 切换出故障时暂停新上传/新建policy1/新提交，保留已经有权限的读路径，修复并向前迁移。不要回退 schema 或将 policy1 批量降为0。

发布前记录 root/api/web/client SHAs、schema版本、image/package digest、feature flags、存储和扫描器版本。client 为外部仓，用 integration.yaml 的 external_candidate 字段单独记录；R1/R2分别有验收记录，不以代码提交代表上线。

## 12. 不可省略的验证

数据与负向矩阵沿用 acceptance O01～O25；新增协议/配额/上传 epoch/队列/单工作项/返工见 O26～O33。contract fixtures 可同时被 Java/Node/Web 测试读取，避免各层手写不一致的 mock；OpenAPI 只能生成类型和客户端骨架，不能生成或替代 ACL/状态机。

每个任务一轮针对性测试与独立评审，修改涉及哪组不变量就补测哪组；R1/R2整体验收各执行一次相关后端/前端/client测试与正式前端构建。所有 Gradle 命令持 `/tmp/cyf-gradle.lock`，不以并行构建缩工期。存储与引用/验收并发必须有真实 MySQL 测试；纯 mock 不足以证明事务约束。

R2 显式返工接口为 `POST /agent/tasks/{taskId}/deliveries/{deliveryId}/rework`，仅source owner可调用。按源根/幂等顺序核对旧批CHANGES_REQUESTED、工作项READY、无已排队/执行新run、expectedTaskVersion、revision与执行attempt上限，原子写既有command outbox和receipt并返回QUEUED。重复调用不重复派发；最多3个审核revision，执行失败仍遵守原maxAttempts，耗尽返回409并说明需人工处理，不暗中重置计数。

R1客户端采集先覆盖当前Linux实现的本地/托管两种模式；其他OS只有通过等效no-follow/隔离快照测试后才公布output能力，不在缺少安全文件API时静默降级。现有task artifact版本仍受INT约束（1～2147483646），虽在线用字符串，也必须拒绝超出数据库范围的版本。

R2恢复接口补充：`GET /agent/tasks/{taskId}/work-items/{workItemId}/lease` 使用run ticket返回当前workItem版本/状态；只有ticket.runId等于workItem.executionRunId才返回活动leaseToken。run_binding另存服务端workItemId；claim在现有CAS事务写execution_run_id，start/heartbeat/submit要求相同run，不能用同一Agent的另一run冒领。初次READY且executionRunId为空时只允许当前已派发run领取。提交将run标RESULT_SUBMITTED；要求修改结束原run，返工命令创建新run并成为当前获准派发run。旧run不能趁READY状态重新claim。

run状态的业务终态与身份撤销分开：RESULT_SUBMITTED允许在恢复期内、身份仍有效时读取原submit receipt/status，禁止新增发布/claim/submit；CLOSED同样允许读取已完成回执但不重新执行。先做身份/来源/操作授权，再在允许回执读取的状态下重放，未命中receipt才校验新mutation所需ACTIVE状态。REVOKED、binding撤销或scope不符始终拒绝。不得因“先把run结束”造成成功提交的丢ACK重试永久失败。

上传临时对象资源边界：每upload最多10个writer epoch、最多2个尚未清理的staging key并存；新epoch须先回收更旧staging或等待。OD02 采用 READY 保留原 immutable key 的方案，该 bucket/key 前缀不配置自动删除生命周期，统一由持久 cleanup/GC 管理；不能把 24h 临时文件规则施加到已发布文件。单个run累计上传请求/重试字节设置配置上限；超限429而非无限重新创建upload session。cleanup 的 `safe_after` 只是调度下界，不能单凭客户端超时或固定宽限时间认定存储端已不可能迟到提交；释放配额前须有写入隔离与清理确认，具体实现需通过 OD02 独立评审。

OD02 单 PUT 写入隔离：所有数据 PUT 由服务端强制原子 `If-None-Match: *`，不使用 SDK 自动 multipart。废弃 epoch 及 READY 对象最终 GC 均向同一唯一 key 写入零字节服务端 tombstone，metadata 绑定 cleanup identity；强一致 HEAD 确认 key、零长度、identity 后才 CAS 释放该条预留或实际占用。普通 GC 永不删除或复用 tombstone，首发只接受从未启用 versioning 的私有 bucket，不能接受可能保留旧版本的 Suspended 状态。需记录长期对象元数据成本；未来回收须另有能证明所有旧 writer 已失效的停写维护设计。当前 epoch 验证成功可独立 READY 并将基础 reserved 转 stored，旧 epoch 各自的预留继续计入额度，无需等待它们全部清理后才能 READY。真实 MinIO 与生产 adapter 的条件写并发验证通过前，该协议不视为已实现或通过验收，评审要求见 `evidence/OD02/storage-fence-review.md`。

能力协商落点：新增注册/心跳字段 `outputCapabilities`，仅允许 `output.http.v1`、`task.owner-share.v1`、`task.delivery-http.v1`。写入runtime的独立 `output_capabilities_json`、`output_capabilities_runtime_id`、`output_capabilities_updated_at` 可空列，由已认证当前runtime/binding的CAS更新；不复用业务 `abilities`，不影响map/roster现有来源。旧客户端缺失视为不支持；当前在线runtime匹配且能力快照90秒内有效才允许新建run/派发policy1任务。能力是调度门槛，不代替API授权；来源/租约/撤销校验仍必需。R1注册仅公布前两项，R2处理器/依赖/客户端完整就绪才公布第三项。
