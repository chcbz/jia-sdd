# 1.13.1 闭环详细设计（候选合同）

日期：2026-09-19。本文是待实现合同，不是线上接口文档。实现前 W00 固定现有任务初始 lease、会话授权、artifact 存储适配的 exact 合同；不允许以这些核对为由删掉业务目标。

## 1. 页面和交互

### 1.1 工作空间

保留文件库管理。补来源/关联悬赏筛选、文件详情“关联悬赏”“交给 Agent”“查看来源议事”“继续修改”，以及“执行记录”页签。选材弹层先选文件再选版本；回收站内容不能加入新执行。

“关联悬赏”选择本人可操作任务、INPUT/REFERENCE、精确版本；这是资料整理，不立即调用模型。选择已有成果作为新任务资料时保留真实 AGENT_DELIVERY 来源，不把旧成果冒充新任务已交付。

“交给 Agent”携带不透明选择引用进入授权私人会话，页面恢复后由 API 再鉴权；URL 不含文件内容、凭据、永久下载地址，前端路由参数不能作为授权依据。既有私人执行表单改为同一会话流程快捷入口，不能另留一套独立状态。

### 1.2 悬赏榜/任务详情

增加“资料与成果”区域：输入资料、参考资料、执行记录、待验收交付、历史成果；每项有版本/来源/预览/下载。“添加资料”共用空间选择器，“上传”也归入空间。任务 owner 不必先扮演某个好汉才能管理本人资料。

“进入议事”打开服务端绑定的任务会话并显示当前任务条；不以地图当前选中角色隐式决定接单 Agent。揭榜/指派继续复用显式 agentId 和原任务规则。**挂资料不触发任务执行；从议事确认的一次执行必须复用任务运行，不得再触发另一条 assign/chat 运行。**

### 1.3 厅内议事

- 输入框提供“添加资料 → 从工作空间 / 上传”；展示所选版本标签，选中未发送只是草稿。
- 顶部展示“私人议事/任务名称”、目标 Agent、已加入资料；多 Agent 讨论中本版文件处理选择一个明确执行者，其他参与者不自动获得文件和内容。
- 已发送资料卡持久化：名称、版本、用途、被授权执行者、授权状态；只读讨论文件也走明确的资料读取授权，不给普通聊天进程整个网盘权限。
- 文件操作采用显式“基于所选资料执行/生成交付件”模式；纯文字闲聊保持原通道。正文含“做 PPT”等可提示进入该模式，但不得暗中触发额外付费。
- 本轮需求作为用户消息保存，服务端建立一条执行并回显执行卡；确认按钮就是该次明确授权，不再重复点击两套发送按钮。
- 支持“只读资料讨论”：例如“解释这张表的数据”，使用同样的固定版本授权和受控读取，返回实际基于资料的讨论回复，不强迫生成文件或创建悬赏；仅讨论不自动改变任务状态。未选资料不能靠同名文件猜测读取。
- 成果卡提供预览、下载、版本历史、继续修改、去任务；任务 owner 看到正式交付的“验收通过/要求修改”。私人会话成果有“确认采用”，不伪造 formal-delivery。

### 1.4 三条主要旅程

**悬赏起步**：创建/选择悬赏 → 从空间加入材料 → 进入任务议事 → 确认执行 Agent/本轮版本/需求 → runtime 实际处理 → 成果三处可见 → 预览下载 → 要求修改 → 新交付批次 → owner 验收。

**私人议事起步**：新建私人议事 → 上传或选空间文件 → 说需求 → 确认执行 → 会话成果自动入空间 → 继续修改。之后需要悬赏时，明确创建/选择本人任务、选择带入哪些资料/成果作为参考，创建任务会话关联；原私人对话和旧执行归属不改写、不公开。

**空间起步**：选多个文件及版本 → “用于悬赏”或“交给 Agent” → 到达前两条旅程。任何入口都无需下载重传。

## 2. 核心关系与唯一事实源

```text
认证 owner / client / tenant
 ├─ 文件条目 → 不可变版本 → 私有内容对象
 ├─ 悬赏 → INPUT/REFERENCE 关联（固定文件版本，仅关联）
 ├─ 议事 → 资料卡/执行卡/成果卡（持久引用，不是内容副本）
 └─ 执行 executionId
     ├─ 可选 businessTaskId + 必需的已授权 conversationId（新会话入口）
     ├─ runtimeTaskId / runId / targetAgentId / task workItem & lease（任务模式）
     ├─ 本轮输入授权快照 / 费用外发确认
     └─ outputId → 内容 + 文件版本 + 可选 task artifact 版本
                                  └─ formal delivery 批次 → owner 决定
```

- **关联 ≠ 授权**：INPUT/REFERENCE 只是任务材料目录。执行创建事务才复制用户本轮选择为授权快照；后续新增材料不自动进入进行中的任务。
- **会话 ID ≠ 权限**：当前私人执行仅收存 conversationId，不足以证明会话归属；新服务必须调用 chat 的真实 scope 授权并核对 task/conversation/target，不能从 metadata 取 owner。
- **内部运行 ID ≠ 悬赏**：旧 pwe_task_* 是私有队列命名空间，不是业务任务根。本版归一化视图区分 businessTaskId（可空）和 runtimeTaskId，不用前缀猜授权，不把私有执行加入公开悬赏列表。
- **内容只存一次，投影可多处**：个人文件版本绑定内容对象；任务模式生成精确 artifact 版本和映射，正式验收以原 artifact/formal-delivery 为准。空间与议事只作目录投影，不另建第二套任务验收状态。
- 现有 artifact 存储按 task 隔离，不能直接塞入 owner 存储 URI；增加受限内容解析适配，服务端从已验证 output 映射解析同一对象，下载入口仍核对各自 ACL。禁止接受浏览器指定任意 storageUri。
- **原件与派生**：首次修改上传原件，创建派生交付条目 v1，记录 parentFileId/version；后续“继续修改”在该交付条目追加不可变版本，并记录准确父版本。跨格式转换新建派生条目。任务 artifact 版本与空间版本用映射关联，不假定两个编号相等。
- 并发修改同一 v1：按提交顺序保存 v2/v3，二者 parent 均为 v1；UI 表示分支来源，不能声称 v3 基于 v2。latest 指最后保存，不代表最后验收；采纳/正式批次都固定版本。
- 同文件多任务：复用内容和版本，但每个任务有独立关联、授权及交付状态；解除 A 的关联不影响 B。

## 3. 数据增量与迁移

以下为逻辑增量；物理表/列名和现有表复用在 W00 冻结，不能直接把草案当生产 DDL。

| 记录 | 必要字段/约束 |
| --- | --- |
| 会话文件关联 | tenant/client/owner/conversationId、relationId、fileId/version、用途、relationRevision、ACTIVE/DETACHED；唯一作用域+会话+文件版本+用途 |
| 执行上下文扩展 | businessTaskId、conversationId、messageId、originExecutionId、sourceOutputRef、contextRevision、阶段/状态版本、最后错误、外发/费用确认引用 |
| 执行输入快照 | 复用当前 fileId/version/hash；补角色、授权 revision、明确 target/runtime 归属；运行后不可偷偷替换输入 |
| 输出映射/派生 | executionId/outputId 唯一；workspace file/version、parent refs、artifactId/version、businessTaskId、真实 producer/run、publication 状态 |
| 私人成果采用 | owner+execution/output+版本、decision revision；与任务 formal-delivery 严格分域，不影响悬赏状态 |
| 可靠投影事件 | outbox/eventId、源 aggregate/revision、目标会话/任务、delivery 状态、尝试记录；消费者 inbox/dedupe 唯一键 |

新增可空列和新关系表，保持 1.13.0 API 可用。历史数据仅从可证明的 output/execution/artifact 关系生成映射；不得按名称、目录、聊天文字猜来源。无证据记录显示“历史关联待确认”。历史导入幂等保留显示名、回收站状态，不复制字节；先只读统计再提供 dry-run 和单独授权的数据计划。新关系可停用恢复旧读路径，不能为降级删除新文件或回退用户数据。

## 4. 候选 HTTP 合同

表中“新增/扩展”均待实现。Browser 请求由 JWT 推导作用域；路径和 JSON 中的 ID 均二次校验，不接收任意 owner。所有写操作带 Idempotency-Key；预期 revision/ETag 的更改带版本前提；读内容使用 private,no-store。输入中未知权限字段拒绝而不是忽略后信任。

| 方法/路径 | 状态 | 请求/响应要点 |
| --- | --- | --- |
| GET/POST `/agent/tasks/{taskId}/file-links` | 已有，复用 | POST `{fileId,version,role:INPUT\|REFERENCE}`；返回 relationId/revision/ETag；用户不能写 OUTPUT |
| DELETE `/agent/tasks/{taskId}/file-links/{relationId}` | 已有，复用 | If-Match + key；只解除关联，单独说明进行中授权不自动撤回 |
| GET `/agent/personal-workspace/files/{fileId}/contexts` | 新增 | 分页返回本人可见任务/会话/源与派生/执行关系；不可见关系不泄漏名称、内容或 ID |
| GET/POST `/agent/conversations/{conversationId}/file-links` | 新增 | 同精确文件选择；经 chat scope 校验；返回 relation/revision；仅个人作用域资料，不广播 |
| DELETE `/agent/conversations/{conversationId}/file-links/{relationId}` | 新增 | 同任务解除语义；历史消息卡保留引用但按现权限显示 |
| GET `/agent/personal-workspace/executions/capabilities` | 已有，兼容扩展 | 可选targetAgentId；返回逐场景READ/GENERATE/MODIFY能力、工具实测状态/证据、输入/输出类型和费用告知；全局MIME配置不等于该Agent可执行 |
| GET `/agent/personal-workspace/executions` | 新增 | taskId/conversationId/state/cursor 过滤；返回 `{items,nextCursor}`，稳定 createdAt+executionId 游标并绑定作用域 |
| POST `/agent/personal-workspace/executions` | 兼容扩展 | 现有 instruction/targetAgentId/taskId/conversationId/outputContentMimeType/inputs；新增 operation（READ/GENERATE/MODIFY）、sourceOutputRef、messageId、contextRevision、grantConfirmation；READ无输出类型，不能进入文件提交/正式交付；旧客户端缺operation沿用原文件执行语义，但不得绕过原有 ACL |
| GET `/agent/personal-workspace/executions/{executionId}` | 兼容扩展 | 保留旧 state；新增 businessTaskId、phase、stateRevision、outputs、publicationState、deliveryRef、source refs 和可恢复动作 |
| POST `/agent/personal-workspace/executions/{executionId}/revoke-inputs` | 复用/补语义 | 预期 grantRevision；撤销未读取授权与实际取消不同；进行中请求给实际可撤销状态，不声称已回收已读字节 |
| POST `/agent/personal-workspace/executions/{executionId}/recover-publication` | 新增 | 仅恢复已保存 output 的索引/消息/正式提交；key + 预期 publicationRevision；绝不再次触发 Provider |
| GET `/agent/conversations/{conversationId}/deliverables` | 新增 | `{items,nextCursor}`；item 包含 exact output/file/可选 artifact 与 formal refs、预览状态；替代 conversation 的固定空列表 |
| GET `/agent/tasks/{taskId}/deliverables` | 已有，兼容接入 | 接收新 output→artifact 映射；保留旧响应合同，新增字段需同步严格前端校验器，不覆盖旧手工成果 |
| GET `/agent/tasks/{taskId}/formal-deliveries`；POST `.../{deliveryId}/decision` | 已有，复用 | decision 为 accepted/changes_requested，expectedTaskVersion/expectedDeliveryVersion；修改原因必填；不新建竞争验收接口 |
| POST `/agent/personal-workspace/executions/{executionId}/adoptions` | 新增 | 私人采用 `{outputId,fileVersion,expectedRevision}`；返回个人 decision，不能触发正式任务完成 |
| POST `/agent/conversations/{conversationId}/task-contexts` | 新增 | `{taskId,selectedFileRefs,expectedContextRevision}`；核对本人任务，幂等创建/解析任务会话，返回目标会话及关联结果；不搬旧私聊记录 |

任务新建复用现有创建接口，再调用 task-contexts；第二步失败可凭 key 恢复绑定，不重复创建悬赏。任务议事优先复用已有 `AgentTaskThreadController`/scope 服务解析会话，W00 固定 exact 方法与响应；上述 facade 若能直接复用则不增加重复持久模型。

READ运行成功的归一化phase为READ_COMPLETED、outputs为空，并持久化源版本引用与回复；不能将无文件回复投射为OUTPUT_COMMITTED。旧客户端不创建READ请求；新客户端使用operation/phase识别它。新的READ协议按能力握手接入runtime。

返回对象中的 `outputs[]` 至少含 outputId/fileId/fileVersion/hash/contentMimeType/byteLength/parentRefs 和服务端计算 actions。预览/下载复用授权的精确文件版本或 task deliverable 内容接口；不把下载 URL 存成永久卡片状态。query 的 fileId/taskId 不可绕过 owner 范围。计费未知时 `costStatus=UNKNOWN`，不显示零。

错误：401 未认证；缺必要 scope 403；越权/不存在资源统一 404；400 格式/角色/上下文组合错误；409 幂等冲突/任务状态变更/不同源版本；412 revision 不一致；428 缺必需版本前提；422 能力或执行条件不满足；503 真实服务不可用。发布结果未知返回可查询 operation/execution 引用，而非自动重试生成。

## 5. 调度、正式交付、修改和验收

### 5.1 两种模式，同一个用户执行入口

- 私人模式：延续 owner 私有 queue/run，不创建公开悬赏。conversationId 必须真实属于当前作用域，未有会话先通过 chat 服务创建纯会话元数据，不为创建会话调用模型。
- 任务模式：服务端固定业务 task + 既有 workItem + run + producer + 有效 lease。现有 R2 正式交付限制单 required workItem，本版单 Agent 路径遵守该合同，不偷偷扩成多 workItem 自动协同。
- W02 必须接入正确的初始领取/租约流程；现有私人 pwe_run 不能当作已有任务有效 lease。若任务已有运行，复用其执行记录/输入授权绑定，或明确冲突；不能并行私有跑一份再伪造正式提交。
- 所有 runtime 输入下载/输出提交继续使用精确 runtime credential lane，不让用户 JWT 假扮 producer，不把 lease/token 展示给浏览器。

### 5.2 一次需求一次执行

服务端在事务中持久化用户意图/执行记录/授权/outbox。chat 消息投影与派发由已持久化记录恢复；即使聊天消息落库是异步，重试不得产生第二次任务。文件模式不再同时发送普通 `/chat/stream` 模型请求；普通讨论与文件执行消息用结构化 kind 区分。

重放同 key + 同归一化请求返回同 execution；同 key 不同资料/源版本/Agent 报冲突。用户显式发起新一轮才创建新 key；网络重试保留旧 key。界面 loading 禁连击只是辅助，不能代替服务端幂等。

### 5.3 输出保存到三处

真实输出校验类型/签名/长度/hash/生产者 → staging 私有不可变内容 → 输出提交事务写版本/映射/任务 artifact 与 outbox → 正式交付服务按现有 lease/CAS 提交 → 私人/任务会话投影成果卡。

文件系统和数据库不做虚假的跨系统原子承诺：字节先 staging，数据库提交决定可见性；孤儿对象按明确授权维护，不碰现有用户文件。任务 artifact/正式服务边界若不能同事务完成，以可靠 outbox 分步恢复，展示“文件已保存，任务交付同步中”，不能报待验收或成功完成。

旧输出提交路径需要新增映射适配，而不是浏览器手工上传成任务成果。下载/预览三处校验同一个 hash；任务成员下载与 owner 个人空间权限分开，不能借公开成果读未选输入。

### 5.4 修改与决定

“继续修改”带 exact sourceOutputRef 和所处 task/conversation，预填材料但必须确认新一轮授权。任务 changes_requested 先完成正式决定并返回其版本，再以该决定作为幂等来源派生返工；聊天不能自行把 task 改为完成。

“要求修改并执行”一次确认可授权上述两阶段：决定成功执行创建失败时显示“已要求修改，尚未开始返工”，提供恢复同一创建操作；不回滚/重复决定、不重收费。纯“要求修改”可只保存意见而不立即派发。

多处验收都调用同一正式 decision：其他页面刷新同一状态；并发通过与要求修改用 CAS 决胜，冲突者重新读取。工作空间的“已验收”按任务/批次/版本展示，不能给跨多任务文件一个无上下文总状态。

## 6. 状态与可靠事件

不破坏旧 `QUEUED/INPUTS_REVOKED/OUTPUT_COMMITTED/FAILED` 的消费者；新增 phase/publicationState/revision 描述更细状态。明确兼容测试，不直接替换旧 enum。

| 用户文案 | 权威依据 |
| --- | --- |
| 待执行 | 已保存请求/授权，尚未领取 |
| 处理中 | runtime 明确领取/开始处理的持久记录 |
| 保存中 | 输出已产生，尚未提交 |
| 已保存/可领取 | 精确内容提交及授权读取通过 |
| 同步中 | 文件已提交，会话/任务投影或正式提交未完成 |
| 待验收/已验收/要求修改 | 对应 formal-delivery 记录，不从文件推断 |
| 结果待确认 | 请求/Provider 响应丢失，尚无可信终态；查原 execution |
| 失败/撤销 | 真实失败或确认撤销范围，附下一步，不伪称瞬时停止 |

复用会话事件通道，新增事件候选 envelope：`{eventId,eventType,conversationId,executionId,aggregateRevision,occurredAt,payload:{outputRefs,phase}}`。事件类型为 file_link.changed、file_execution.changed、file_delivery.available、formal_delivery.changed；只发引用，不广播敏感文件名/正文/凭据。按成员授权分别投影，默认个人 owner 可见。

事件消费者按 eventId 去重、aggregateRevision 拒旧事件；重连传游标，缺口/过期先拉权威快照。事件或 outbox失败时靠执行/成果查询恢复，不能以一条 SSE 为唯一领取依据。不会因超性能 SLO 取消请求；保留真实传输超时、用户取消、身份切换和租约约束。

## 7. 权限与恢复边界

1. 文件上传默认只有本人；关联任务仍不授予全部任务成员读取原件。每轮明确授权给选定执行 Agent；引用资料也属于读取授权范围。
2. 群议事附件/执行卡采用 owner 私有可见性；输出是否发布给任务可见范围随正式提交明确告知。不得通过群消息正文自动扩散输入内容。
3. 删除关联不自动撤销正在处理的快照；单独“撤销未开始授权”核对 revision/领取状态。回收站操作先呈现引用影响，不删除正式交付字节；恢复文件不自动恢复已撤销授权。
4. 退出、切身份、切 task/conversation、切目标 Agent清理草稿/URL/缓存和过期请求；主动转移上下文必须用户确认，不能自动把 A 资料带给 B。
5. 附件正文为不可信输入，不执行其中宏/脚本或越权要求；工具在隔离工作目录按 manifest 读写，不开放任意服务器路径。
6. Provider 真调用需既有授权范围及实际账户/预算/资料外发确认；保存确认可审计引用，不存凭据；不得先调用再补确认。

## 8. 工程接入与待冻结点

Web 复用 PersonalWorkspace.vue/usePersonalWorkspace.js、JuyiHall.vue、BountyPanel.vue、ChatPanel.vue、useHallConversation.js、useOutputs.js、useFormalDeliveries.js。新增共享 WorkspaceFilePicker、FileReferenceCard、ExecutionCard、DeliveryCard 及独立关系/执行 composable，避免向 JuyiHall.vue 堆入所有业务状态。

API 复用 PersonalWorkspace*Controller/Service、chat scope/task thread 服务、AgentTaskDeliverableController、AgentTaskFormalDelivery* 与原运行租约服务。新增统一执行编排和内容/成果映射适配，不泛化重构现有经济/协同域。必要 runtime 改动只在版本化源码目录，禁止直接编辑部署副本。

W00 必须产出：task/thread/lease exact 调用图、任务与私人运行单一派发方案、对象存储适配合同、消息/outbox复用清单、runtime commit/tree及实际能力、迁移字段/索引/锁序、Provider 测试授权清单。锁顺序以现有任务 root 先锁约束为起点统一 task→execution→按ID排序文件→output；逆序存量调用必须修复并并发验证，不能仅在文档声明。

这些是当前可见的真实风险，不是假定已实现；W00 冻结后方进入对应高风险写路径实施。

## 2026-09-19 多part预览兼容补充（W12/W13）

本节是增量实现合同，不改写上文冻结业务语义；测试和发布结论独立记录。

- 个人空间和任务成果的既有`GET .../preview`缺省保持旧single-`content` catalog；任务Office/PDF仍返回`EXTRACTED_TEXT`，不迫使1.13.0客户端理解新parts。
- 新客户端仅在metadata请求显式加入`?view=parts`。非法/重复view或混入身份参数返回400；query永不替代JWT owner/client、任务或文件ACL。`.../preview/parts/{partId}`仍按精确版本和owner先鉴权。
- PPT：`slide-N` PNG，任务representation=`PAGED_IMAGE`；Excel：`sheet-N`纯文本，`SHEET_TEXT`，显示单元格坐标和原公式、绝不执行公式；PDF：`page-N`逐页提取文本，`PAGED_TEXT`，不是PDF页面图像/版式保真；DOCX仍`content`提取文本。
- 新catalog末尾保留`content`兼容提取文本；新UI可从分页导航排除这项，旧URL仍可读。支持格式不是实际Provider能力或收费授权。
- PPT派生预览的输出格式采用1600×1200边界框，保持比例；这是预览分辨率设计，不按源尺寸拒绝文件或中断后续页面。metadata不生成PNG，只按请求页渲染；巨大源pageSize不得直接分配原尺寸画布。嵌入图解码和外部资源读取另做Owner安全核对。
