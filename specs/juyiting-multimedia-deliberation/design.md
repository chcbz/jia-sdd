# 多媒体悬赏议事：详细设计（候选合同 v1）

> **2026-10-03 通用点将源码进展**：[新主路径合同](generic-point-and-deliberate-contract-20261003.md)。API712dafc、Client42e554d已推特性分支；点将59PASS、Chat51PASS/3条件MySQL未跑、Client18PASS。Web新点将接线与自动资料查阅/执行仍待完成，未发布。

> **2026-10-03 最新实施指令**：用户明确“无需做太多兼容补丁，一切都按新方案实施”。新入口、新请求统一走通用资料与按需议事；不新增旧生图入口、双轨产品流程或回退适配工程。只保留身份隔离、幂等、未完成请求及既有内容保护，不以历史兼容覆盖率阻塞新方案。

> **2026-10-03 用户纠偏（当前优先）**：[通用资料详设增量v3](unified-materials-correction-20261003.md)取代独立参考图入口及图片限定业务流程。唯一“添加资料（可选）”须支持图片/文档/音频等；Agent判断用途，通用会话、输出、保存与交付保持完整范围。不是文案改名；绘图专用wire仅作为执行适配，不扩展旧产品入口，原34项需补UM01–UM10。当前已完成创建/资料基础源码自检，通用点将会话链路与整体验收仍待完成。

> **2026-09-28 优先补充**：[融合详设v2](fusion-detailed-design-v2.md) 明确统一admission、按需读取、任务办理授权、明确需求直接execution及取消/续办边界；不再把“先CHAT后执行”视为必经步骤。本文其余UI/媒体/归档合同继续有效，新增接口仍为拟议。

日期：2026-09-27；状态：draft，未实现/未迁移。下文新增字段、表逻辑名、接口、事件均为**拟议合同**，不得作为现有线上 API 调用说明。M0 核对最新组件 schema/DTO 后冻结映射；不改历史冻结合同或原验收结论。

## 1. 核心边界与数据流

```text
需求 + 可选空间版本 → 点将事务/投递 outbox → 唯一悬赏议事
                                               ↓
                           授权上下文 → CHAT 答复/澄清/结构化执行意图
                                               ↓ 服务端权限/能力/费用校验
                           文件 execution → Agent inputs/outputs/scratch
                                               ↓ 校验上传/manifest
                           持久内容 + 会话 asset/part → 事件/历史媒体展示
                                  ↙ 用户选择             ↘ 用户选定最终集合
                           个人文件/版本               正式交付 → 验收/完成
```

- durable request/turn/outbox/snapshot/event 复用 fast-deliberation 修正后的实现；不增加另一套聊天队列/事件日志。
- bootstrap outbox 是点将业务与聊天受理间的可靠协调意图，优先复用已有 outbox 机制，不能混淆为新的模型执行队列。
- CHAT 产生执行意图，不自带目录、工具或计费权限。服务端执行协调器检查本轮授权后调度现有文件 execution。未获授权时在会话说明，不绕过执行协议。
- 会话按 scope/task 唯一；assignmentRevision 只识别投递/交接版本，不作为每轮新建会话的依据。

## 2. 交互详设

### 2.1 需求与点将

需求表单提供可选资料选择器，显示缩略图/文件名/版本；选择不意味着开放整个空间。点将必须显式携带目标 agentId。完成点将后自动进入“悬赏议事 · 需求标题”；需求首条消息包括原文、资料卡和接收 Agent。

状态分别显示“点将已完成 / 需求投递中 / 已受理 / Agent 回复中 / 需要补充 / 生成中 / 产物就绪 / 失败可恢复”。没有 runtime ACK 不标“Agent 已收到”；点将成功不标“已生成”。局部失败保留任务和会话，重试仅补投递。

### 2.2 会话工作台

文字、图片、音频、普通文件可以在一条回复混排。图片有占位、缩略图和放大；音频有播放器，默认不自动播放；其他文件按真实支持格式预览，未支持格式明确“可下载，暂不支持预览”。资料、已保存、最终成果放侧栏/移动端页签，不要求退回百宝箱，切换时保留草稿。

输入支持文字、空间引用、会话结果引用。引用图片后可说“改成蓝色”；新稿保留来源，不覆盖旧稿/原参考图。不明确引用时按上下文合理判断，不能唯一确定再澄清。

实时定义：文字增量和执行状态即时展示；完整媒体经服务端验证就绪后原位出现。不承诺逐像素生图或未完成音频边生成边播放。

### 2.3 保存与验收

保存可选单个/多项内容或文本选区；默认创建文件，重复保存同一快照返回已有结果。“另存副本”是独立意图；“更新已有文件”须显式选择并带 expectedVersion。多项保存显示逐项结果，不能一项失败把所有项标成功。

验收面板列出精确最终成果，可排除旧稿。可选“同时保存到空间”，但不是完成前置。正式提交及验收由服务端协调，失败显示实际阶段；只有任务领域确认完成才显示完成。验收成功、可选归档失败时仅重试归档。

## 3. 内容模型与存储

### 3.1 一份内容，三种引用

```text
不可变内容 ContentRef（私有存储字节、sha256、MIME、长度）
 ├─ ConversationAsset → MessagePart（会话 ACL）
 ├─ WorkspaceFileVersion（主动保存后，个人 ACL）
 └─ FormalArtifactVersion（最终提交，正式任务 ACL）
```

`ContentRef` 是逻辑合同，不要求新建 content 表。优先复用已存在输出元数据/storageRef，以资产、用途和来源关系补充。不同用途不互相授予权限；浏览器不能用裸 content hash 任意认领内容。

会话产物复用 `/opt/cyf/service/workspace-private`；正式交付沿用 `/opt/cyf/service/task-artifacts-private`，必要时复制但核对同一摘要。两个根均保留，无第三存储根/历史迁移/跨 owner 物理去重。后端实际路径从配置读取，不在代码中硬编码。

### 3.2 建议新增或扩展的逻辑记录

| 记录 | 核心字段 | 唯一性/约束 |
| --- | --- | --- |
| DiscussionBootstrap | scope、taskId、assignmentRevision、requirementRevision、conversationId、initialRequestId、stage、revision | scope/task/assignmentRevision 唯一；需求原文和资料快照不可被重试替换 |
| MessagePart | messageId、partId、kind、state、text/assetRef、revision、sourceExecutionId | messageId/partId 唯一；只接受更高 revision，ready 不能被旧事件回退 |
| ConversationAsset | assetId、scope、taskId、conversationId、messageId、partId、outputId、runId、storageRef、hash、mime、bytes、state | run/output 唯一提交；ready 必須具有已验证字节，scope 不从请求信任 |
| ExecutionLink | turnId、intentId、executionId、runId、partId、assignmentRevision、inputSnapshotId | scope/turn/intentId 唯一；一轮可多执行，但重放同意图不重复计费 |
| ArchiveLink | actorScope、sourceSnapshotKey、targetFileId、version、operationId | 普通保存 sourceSnapshotKey 去重；另存需新显式意图 |
| Finalization | operationId、taskId、selectedSetHash、expectedTaskVersion、deliveryId、decisionId、stage | 操作幂等；集合/版本锁定，验收前不得暗换最新稿 |

`sourceSnapshotKey` 包含资产不可变版本，或 messageRevision/partId/文本选区边界及内容摘要；文本选区按 Unicode code point 定义，服务端从持久消息截取并验证摘要，不信任前端任意正文伪装选区。流式未完成文本先冻结快照才能归档。

所有引用关联都需强制 scope 一致；实际 DB 表名、索引迁移及历史映射由 M0 输出，不预设每个逻辑记录都需独立新表。

### 3.3 生命周期

未归档会话资产不是临时浏览器文件：刷新或 Agent 离线仍可读取。空间归档和正式成果各自持有保留引用；删除会话不级联删除它们。GC 只处理已无任何有效引用且符合明确保留策略的对象；本期不新增自动清理任务/任意 TTL。权限撤回立即阻止后续领取，但不能承诺追回已下载字节。

## 4. 自动投递、执行及上下文

### 4.1 点将协调

1. 在任务权限及 expectedTaskVersion 校验后，以点将业务事务保存 assignmentRevision/资料快照和 outbox。
2. 幂等消费者确保既有 task-thread，会话唯一约束保证跨端重试仍只有一个。
3. 以稳定 requestKey 调用 durable admission，写入可見需求/资料首条消息。原文、文件版本来自业务 DB，而非前端回调临时变量。
4. 分发前读取目标能力；按明确的匹配协议受理，不向缺能力客户端发送现代 wire。现代请求受理后不偷偷 fallback 重跑。
5. 各阶段失败保存真实状态；只有用户新修订/重新点将才产生新意图。

不跨模块假装一个大事务：任务 outbox、会话 admission、execution 与结果发布采用幂等桥接和可查询状态。数据库消息/event 写入同事务或同 outbox，避免字节已提交但消息永久缺失。

### 4.2 上下文与生成桥接

快照必须可独立重建：需求修订、已授权资料精确引用、相关历史正文/有来源向量的摘要、当前输入、目标/参与者权限。threadId 是缓存，不是真相；冷线程、配置更换和内置宋江均消费同一业务快照。上下文过长时生成可追溯摘要，不仅保留无法读取的消息 ID。

拟议模型结果 `replyAction = answer | clarify | propose_execution`。执行意图含 `intentId, operation, inputRefs, outputSpec, instruction`；不接受任意 shell、文件绝对路径或未授权 URL。服务端根据用户需求/上下文、目标能力与既有授权做决定，不以模型自述“用户已批准”作为授权。附件内的指令也是不可信数据。

新增执行用途候选 `CONVERSATION`，沿用现有 PRIVATE/TASK 而不改变其语义。conversation scope 和真实 task/work-item 归属须明确映射；复用 run/lease 和 producer 绑定。澄清不占生成 lease。每次真实生成/修改建立新 execution，并以 ExecutionLink 关联 turn 和媒体 part。

### 4.3 Runtime 输入输出

InputRef 联合类型：

```json
[
  {"kind":"workspace_version","fileId":"f1","version":2},
  {"kind":"conversation_asset","assetId":"a1","revision":1},
  {"kind":"message_snapshot","messageId":"m1","partId":"p1","revision":3}
]
```

引用仅是请求，服务端验证 ACL/版本后形成受控输入清单、摘要、MIME/长度；需要物化的文本快照作为文件输入，不给 runtime 任意查库权限。runtime 用绑定 run/producer 的已有 native 接口领取，校验后写入本次 inputs。输出写入 outputs，scratch 不会自动发布；检查路径穿越/符号链接逃逸，不全盘扫描。

保留 native `/start` 成功回执先于 Provider 调用；按能力明确是否可读取图片/音频以及输出格式。server/local 均使用相同 wire 合同，只有本地根配置不同。模型提示词说明真实输入/输出相对路径，但 prompt 不承担 ACL 或上传职责。

输出上传沿用已有 `/internal/agent/tasks/{taskId}/runs/{runId}/outputs/{outputId}/content` 与 `/output-commits/{manifestId}`；CONVERSATION 提交只创建持久资产/part，不自动个人归档/正式交付。重复 manifest 返回已提交结果；摘要或清单变化报冲突。

## 5. 接口候选合同

### 5.1 共通规则

新增写请求必须有 `Idempotency-Key`。作用域为已认证 tenant/client/owner + 业务操作；同键同 payload 返回原结果，同键异 payload 返回 409。tenant/owner/senderType/name 均由服务端推导。认证遵循现有 JWT/会话约定，cookie 写入沿用 CSRF 防护，不引入新的全局认证机制。

异步请求返回 202 与 `operationId/state/revision/statusUrl`；重复已完成请求返回当前终态，不重执行。状态请求只读。400 无效引用/格式，401 未登录，404 无权或不存在（不泄露他人资产），409 幂等/版本/状态冲突，422 格式/能力不支持。能力暂不可用、Agent 离线可记录等待或明确业务失败；禁止伪报已经送达。错误体候选 `code,message,retryable,operationId,stage`，禁止包含绝对私有路径/令牌。

下表“扩展/新增”均待实现；“已有”表示复用入口，不表示支持新字段。

| 方法/路径 | 性质 | 请求/返回增量与权限 |
| --- | --- | --- |
| `POST /agent/tasks/{taskId}/assign` | 已有入口扩展 | 显式 agentId、expectedTaskVersion、requirementRevision、inputRefs；已授权任务 owner；返回 assignmentRevision、discussion bootstrap 状态，任务提交与 outbox 一致 |
| `GET /chat/task-threads/{taskId}/discussion-bootstrap` | 新增 | 按 assignmentRevision 查 conversationId/initialRequestId/stage/revision/error；当前任务 owner |
| `POST /chat/task-threads/{taskId}/discussion-bootstrap/retry` | 新增恢复 | assignmentRevision；仅恢复现存意图，不重新点将/改资料，返回 bootstrap 状态 |
| `POST /chat/task-threads/{taskId}/team` | 已有复用 | 服务内确保稳定 thread；保持旧 actorAgentId 参数与权限校验，不将其当身份凭证 |
| `POST /chat/stream` | 已有 + durable 候选扩展 | 保留旧 content，新增 protocolVersion、inputRefs、replyToMessageId/part 引用；返回既有流及稳定 requestId/turnId |
| `GET /chat/conversation/content` | 已有扩展 | 历史消息增加 parts、revision、execution 状态；旧 content 字段保留；会话 ACL |
| `GET /chat/conversation/events` | 已有扩展 | 沿用候选 cursor/replay，新增媒体事件；不另起并行 SSE 通道 |
| `GET /chat/conversations/{conversationId}/assets/{assetId}` | 新增 | 返回 owner-safe 媒体元数据、state/revision、预览和内容入口；会话与资产双重 ACL |
| `GET /chat/conversations/{conversationId}/assets/{assetId}/content` | 新增 | 就绪字节，支持 inline/attachment 与音频 Range；404 隔离，未就绪 409 |
| `POST /chat/conversations/{conversationId}/archive-operations` | 新增 | items 含 assetRef 或 textSelection，mode=create/reuse/copy/new_version；可选 targetFileId/expectedVersion；返回逐项结果/operationId；源读取权 + 目标个人空间写权限 |
| `GET /chat/conversations/{conversationId}/archive-operations/{operationId}` | 新增 | 归档状态及成功 fileId/version，不重调用 Agent |
| `POST /agent/tasks/{taskId}/finalizations` | 新增协调 | selections、expectedTaskVersion、summary、saveToWorkspace；固定成果集合；仅有验收权限的用户，返回 operationId/stage/deliveryId |
| `GET /agent/tasks/{taskId}/finalizations/{operationId}` | 新增 | 返回提交/验收/完成/可选归档各阶段真实状态 |
| `GET /agent/tasks/{taskId}/finalizations/request` | 新增核对 | 用原 Idempotency-Key 查意图，响应未知不产生新生成/新验收 |

归档响应未知时，原键重发同 payload 或按已知 operationId 查询；finalization 同理。404 不是在途请求未受理的证明。bootstrap 以固定 assignmentRevision 查状态。M0 须使新路径与现有统一响应包装兼容，不能对旧客户端全局换格式。

### 5.2 消息与事件

拟议消息片段示例（占位 ID，不是可调用数据）：

```json
{
  "messageId":"m1","conversationId":"c1","taskId":"t1","turnId":"turn1",
  "content":"已开始绘制。","textState":"final","revision":4,
  "parts":[
    {"partId":"p1","kind":"text","state":"ready","text":"已开始绘制。","revision":1},
    {"partId":"p2","kind":"image","state":"processing","sourceExecutionId":"e1","revision":1}
  ]
}
```

媒体 ready part 补 `assetRef,mimeType,name,byteLength,contentHash`；width/height/duration 来自实际检测而非模型猜测。模型返回的 Markdown 本机路径或外链不自动升级为 asset。

新增事件类型候选 `part.processing/part.ready/part.failed/execution.changed/archive.changed`。统一 envelope 为 `eventId,conversationId,seq,requestId,turnId,messageId,partId,executionId,revision,type,payload`；按实际类型允许关联字段为空。事件授权与历史读取一致，永不广播私有 asset 到不相关会话。

同一会话 seq 单调；eventId 去重、part revision 防回退。重连沿用 durable cursor；游标不可回放时返回 resync_required，客户端拉授权快照及快照 watermark 后继续，防快照/订阅竞态。旧消息没有 parts 时从 content 渲染，不编造媒体已就绪。

## 6. 状态与恢复

| 对象 | 正常路径 | 失败/恢复原则 |
| --- | --- | --- |
| Bootstrap | assignment_committed → thread_ready → admitted → dispatched | outbox 幂等补齐；Agent receipt 与平台分发区分 |
| CHAT turn | admitted → responding → text_final | 沿用 durable 失败/取消状态，text_final 不终止挂接媒体 execution |
| Media part | pending → processing → ready | failed/cancelled 独立呈现；ready 必須持久字节通过校验 |
| Execution | admitted → start_ack → running → output_committed | 上传失败恢复上传，不能自动重跑收费工具；未知结果先查执行 |
| Archive | pending → saving → saved/partial_failed | 仅重试失败归档项，不影响会话/验收 |
| Finalization | selected → submitting → submitted → accepting → accepted → completed | 任一阶段失败保存阶段及标识；accepted 不等于领域已完成 |

刷新、SSE 重放、连接恢复不自动再生图。用户主动“再生成”才新建 intent；用户取消应对实际执行发明确取消而非仅关闭文字流，最终状态按服务端确认。取消与提交竞态用 run/version/lease 校验：已完成结果保持事实，不伪装被撤销；晚到事件不污染其他身份/任务。

重新点将提高 assignmentRevision，复用会话但重新检查交接权限。新 Agent 仅获明确授权上下文；旧 Agent 未获续权不得领取/提交新输出，在途执行按所有权/版本规则处理，不允许旧结果完成新分配。

## 7. 正式交付与验收权限

Finalization 是编排，不是让浏览器成为 producer。服务端先验证用户可验收任务及选中内容来源/用途，固定 selectedSetHash 和 expectedTaskVersion；通过明确受信生产者适配器复用正式提交服务，保存正式 artifact 版本/摘要映射。

现有正式提交要求的 run/work-item/lease/producer 不能简单删掉或伪造。M0 必须设计具备任务边界的内部晋升操作/授权能力，仅允许提升本任务已验证资产，不向浏览器暴露 lease token，也不接受用户自填 storageRef/hash 认领文件。该适配器是关键 API 改造，不是 Controller 里冒充 Agent。

字节转存成功后才登记正式成果；正式交付的事务及锁维持原有语义。再以真实用户身份记录验收，使用 delivery/task version CAS 防多端并发。选择纯文本时冻结文本快照；“画鸟”需求必须有真实可领取图片。是否满足需求由用户验收，领域状态完成仍由服务端判断。

## 8. 安全与兼容

- 每次媒体 GET/HEAD/Range、保存、引用、最终提交校验当前身份及对应 ACL；短期地址不是永久公开令牌。鉴权过期返回可理解错误，不对 XHR/media 循环重定向登录。
- 当前存储仅支持 tenant=0 的限制如实保留，不借本需求扩租户；scope 与目标 Agent 归属均来自服务端。
- 校验 MIME/魔数、摘要、实际大小、文件名和路径；HTML/SVG/Markdown 主动内容安全处理，默认不执行脚本。文档预览沿用安全转换；不通过 iframe 任意远程地址冒充预览。
- 现有私有读取使用 Authorization 时，浏览器图片/音频采用认证 fetch/blob 或等效安全同源方案；撤销 URL/身份切换清理缓存。音频 Range 返回 206/Content-Range，非法区间 416，HEAD 无正文；未支持拖动不展示虚假的可拖动承诺。
- 逐目标协商协议版本、读取格式、生成/修改与输出用途；前端功能展示不等于 Agent 能理解/生成音频。老客户端继续原合同，不将已受理新执行降级再跑。
- 文本 MIME、音频 MIME、TASK 分类与存储白名单须显式补齐测试；不能把音频伪装成 PDF/document 来绕过校验。
- 保留真传输超时、用户取消、锁/lease/幂等、身份切换保护；慢请求仅观测，不把任意性能 deadline 下传执行为取消。

## 9. 迁移、启用与观测

增量建列/索引/关系，优先复用现有表。旧 content/PRIVATE/TASK 行无需强制回填；历史只有本机路径的消息仍标不可领取，不能生成假资产。DB fixture 覆盖空库、存量升级、重复执行、失败恢复及读写兼容；实际 DDL、唯一索引和事务映射在 M0 固定。

实施顺序：基础分支修复 → additive schema/API 可兼容旧行为 → 客户端能力 → 新前端/按目标启用 → 图片链路 → 完整多媒体。发布失误优先修正，新入口可暂停接收但不得丢弃在途操作/既有资产，恢复查询持续可用；不做保守回退默认策略，不对已写数据破坏性删表。

观测使用关联 ID、阶段、错误码、耗时、实际用量（有可信来源时）；日志不含输入正文/私有 URL/token。统计重复受理、缺媒体、上传/保存/交付失败帮助优化，不把未测算数值变为发布硬门槛。

## 10. M0 必须关闭的合同问题

1. fast-deliberation 最终 merged SHA/event cursor/身份接口及快照结构。
2. 现有 task-thread 与悬赏唯一会话映射，重新点将和现有 delivery/task 状态对应。
3. CONVERSATION 用途、logical asset 与现有输出表的最小 DDL；全链路事务/幂等索引。
4. 用户选定成果晋升的受信适配器、生产者授权与可恢复状态。
5. 各格式真实能力/MIME 支持、媒体鉴权与 Range；费用授权如何映射到既有授权范围。

这些是已标明的实现前设计决策，不表示要再让用户重复确认已明确的产品流程。
