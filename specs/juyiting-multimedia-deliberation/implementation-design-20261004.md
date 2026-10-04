# 聚义厅多媒体协作：待实施增量详设

2026-10-04。与 [任务清单](tasks.md) 配套；本文件只定义**现有候选到最新需求的差异**。[design.md](design.md) 保留完整产品目标，冲突时以本次更具体的增量合同为准。

**仅交付文档。以下“拟新增/拟扩展”合同尚未实施，不得当作现有 API 调用。** 不改页面体系、不重建文件系统、不新建独立图像产品，不把历史已有能力列为从零开发。核对基线 SHA、远端及证据限制见 tasks.md 第1–2节。

## D1. 页面改动及原型对应（T01–T03）

原型继续使用 [局部调整版](prototypes/adjusted/index.html)，不重新设计外观。桌面侧栏、手机“办事/事项/资料/我的”底栏、红褐色主题、已有地图/名册数据流均保留。原型使用模拟资料、回复及标签内状态，不能直接复制成生产数据层。

| 现有差异 / 源码证据 | 要做的局部改动 | 原型定位 |
|---|---|---|
| BountyPanel 同时有起草正式任务、起草交办；HallDraftEditor 有确认视图 | 合为“提出需求”，草稿仍可恢复；需求正文必填、资料可选。提交按钮完成本次创建，不再增加重复确认 | [事项](prototypes/adjusted/index.html#tasks)、[创建标注](prototypes/adjusted/annotations/index.html#create) |
| HallMaterialPicker 已有统一入口，但默认露出版本选择 | 复用现有选择器；默认冻结选择当时的最新可用版本，摘要显示名称/类型/缩略图。版本管理留在工作空间；取消不改原草稿，移除不删原文件 | [资料标注](prototypes/adjusted/annotations/index.html#materials) |
| AgentPanel 已有密议，但无面向当前待点将事项的专用 action emit | 用父级现有待点将上下文接入“点将并议事”；不向点将册传需求/附件展示区；没有待点将事项就只保留密议 | [点将](prototypes/adjusted/index.html#agents)、[密议](prototypes/adjusted/index.html#private) |
| ChatPanel 顶部仍有事项资料/百宝箱；Composer 常驻语音和清空操作 | 顶部保留标题、对象、状态和已有返回；不加验收。底部仅输入框、＋、发送；资料/语音输入/设置移入＋ | [议事标注](prototypes/adjusted/annotations/index.html#chat-start) |
| BountyExecutionOutputs 有 checkbox、selectedKeys 及验收选中项 | 将验收操作放回事项详情；成果卡留预览/下载/保存。验收面板只读展示 T05 的正式待验收集合 | [验收标注](prototypes/adjusted/annotations/index.html#accept) |

“提出需求”作为本次新悬赏需求的唯一主入口，复用已有通用 task 创建与点将，不按文字猜测后端任务类型。既有私人交办/正式任务记录仍按各自领域服务读取，不能因合并 UI 入口绕过 ACL 或自动转类型。若既有编辑复用 HallDraftEditor，保留其领域语义而不是批量删除所有历史功能。

＋面板遵循点击外侧/ESC 关闭并恢复焦点；选择资料后保留草稿；语音录制使用已有能力，停止转写先放入可编辑草稿，不自动发送。保留 fetch receiver 修复、实际可绘制图标、录音取消、权限错误与 AI 提示，不以原型假录音替换真实语音。消息附件与引用占同一输入区域，不再增加一排固定按钮。

同一 Web Owner 负责 JuyiHall、Composer、ChatPanel 交叉接线；子任务可以拆测试，但不能并发覆盖同一组件。

## D2. 点将与密议（T02，复用而非重写）

- 创建成功后保留服务端 taskId / task revision / 资料精确引用，跳入现有点将册；不靠卡片显示文字恢复上下文。
- 在点将动作中传明确 targetAgentId，复用 `POST /agent/tasks/{taskId}/point-and-deliberate` 与原键查询。服务端负责唯一会话与首条需求，不由进入页面事件重新派发。
- “与这位好汉密议”沿用独立会话入口，不能调用 point-and-deliberate、伪造正式事项或带出尚未提交的需求资料。
- 返回点将册保留候选和待办；切换好汉密议时历史、草稿、媒体与请求状态按真实会话隔离。身份切换清理旧可见状态。
- 验证 AgentPanel 与父级的显式事件；不混淆 `/agent/map` 与 `/agent/roster`，不恢复 `/agent/active`。

## D3. 附件-only 普通请求（T04，确定合同缺口）

### 已证实差异

Web `HallChatComposer.vue` 的 canSend 要求非空 draft；`hallTypedDeliberation.js::discussionBody` 也拒绝空 content。因此“只补一张图/一个文件并发送”目前在客户端合同上被拒绝，不能只改按钮 disabled。服务端 admission/context 校验必须配套核对修改。

### 拟扩展规则（沿用现有端点/字段）

`POST /chat/conversations/{conversationId}/interactions/discussion` 沿用现有 `schemaVersion: 1`、`intent`、`taskId`、`expectedAssignmentRevision`、父结果/澄清关联及 `sourceSelectors`；不因模型结果采用 v3 改成请求 v3。

| 正文 | 精确资料引用 | 行为 |
|---|---|---|
| 非空 | 空或合法列表 | 保持原行为 |
| 空字符串/仅空白 | 至少一个合法引用 | 允许；原用户正文按实际值持久化，消息显示资料卡，不补造“请处理附件”等用户发言 |
| 空字符串/仅空白 | 空列表 | 沿用请求错误，前端不给发送 |
| 任意 | 越权、未知版本、格式错误引用 | 拒绝对应请求，不偷偷换文件或扩大权限 |

保留当前长度/资料数量合同，不趁本次新增任意门槛。幂等摘要包含真实正文、规范化精确引用及父意图，空正文与不同附件不得撞键。响应继续用现有 accepted 包装；坏参数沿用 INVALID_REQUEST 映射，资料鉴权沿用不泄露存在性的策略。网络结果未知查原请求，不自动换键再次发送。

Agent 读取附件目录后判断按需查阅、澄清还是执行；缺少明确指令可以自然问“希望如何处理这份资料？”，但不能一律要求用户补正文才能入库。用户回答继续原澄清关联。Client 的空正文处理应保持上下文不丢，不凭空赋予执行或付费权限。

新增测试：双空拒绝、单图空正文、文档/音频混合、撤权、同键重放与异体冲突、澄清续答；前后端使用同一 fixture。

## D4. 本次交付集合与纯文字（T05，最小服务端补齐）

### 已有与缺口

现有 finalization 接口接收 `selectedOutputs`，各项含 requestId / stepId / outputId / sha256 / title / purpose；`ChatSelectedOutputFinalizationService` 从真实 execution output 读取并校验字节。它不是“任意聊天文字都能验收”的接口。

最新需求移除用户多选，但**不能自动提交全部历史结果、按类型各取最新一个，或靠浏览器内存决定交付件**。需要明确且持久的本次成果集合；纯文字成果不能伪造 executionId/runId 获得现有工具产物资格。

### 最小逻辑状态（拟扩展，不要求同名新表）

| 信息 | 用途与约束 |
|---|---|
| deliverySetId / revision | 任务当前待验收清单身份和乐观锁；清单每次变更递增 |
| taskId / conversationId / assignmentRevision | 绑定当前真实任务、会话及指派；禁止密议成果偷渡到任务 |
| items[] | 每项稳定 itemId、显示名、精确来源、MIME、大小、摘要；只能引用服务端验证可读的持久内容 |
| source 类型 | VERIFIED_OUTPUT 使用原 execution/output 关联；MESSAGE_SNAPSHOT 使用完成消息/文本选区的不可变快照 |
| replacedItemIds / originatingRequest | 记录本次替换/删除哪些旧项、来自哪次真实意图；旧文件及会话历史不删 |
| status | READY / FINALIZING / ACCEPTED；生成中只呈现实际处理状态，不冒充清单已就绪 |

优先扩展既有结果/交付元数据及存储；Owner 先核对唯一键与事务边界，仅必要时增量迁移。不建独立媒体存储，不为清单复制一套工作空间。

### 清单如何产生

1. Agent 回复的结果需明确区分普通答复与“本次交付成果”。工具完成产物或明确作为交付的完成文本，通过服务端既有动作/结果投递链记录清单变更；不能仅靠前端点击/挂载触发。
2. 首次明确交付建立集合；后续改稿使用明确的旧 item 引用替换。未修改的其他项自动保留；新增/删除也须来自当前用户意图与可验证的 Agent 结果。
3. 如“改成蓝色”对应多张图，先在原会话自然澄清对象；不能把所有图一并覆盖。Agent 无法明确本次交付时继续会话，不展示假的 READY 清单。
4. 清单变更与结果持久化/可恢复事件绑定；事件重放复用 originatingRequest/结果身份，不能重复追加。乱序旧事件不能覆盖新 revision。
5. 纯文字使用完成消息的不可变 UTF-8 快照（选区绑定消息版本、区间和摘要）；禁止流式未完成正文。建立同一内容服务的授权来源，不自动保存为用户工作空间文件，不调用生成工具制造虚假 run。

### 拟新增的只读合同

为浏览器读取权威清单，建议在现有任务域增加 **`GET /agent/tasks/{taskId}/delivery-set`**（尚未实施）。响应沿用现有 JsonResult 包装，data 包含上述集合身份、revision、任务/指派版本、status 和 items；每项预览/下载走现有授权内容入口，不返回主机路径或私有外链。

无已就绪清单时返回明确无清单状态，不自动执行 Agent；不存在/无权限遵循既有 404 隔离策略。若已有等价持久查询可复用，Owner 在 T05 提交中用其实际端点替换此建议，语义保持一致，不同时保留两个产品入口。

### 拟扩展的验收写合同

复用 **`POST /agent/tasks/{taskId}/finalizations`**，新界面传：

```json
{
  "expectedTaskVersion": "<existing-task-version>",
  "expectedAssignmentRevision": "<existing-assignment-revision>",
  "conversationId": "<conversation-id>",
  "summary": "确认验收本次成果",
  "deliverySetId": "<server-issued-id>",
  "expectedDeliverySetRevision": 3
}
```

这是**拟扩展的请求形状**：当前 Controller ROOT 严格校验 selectedOutputs，不接受此 body。T05 必须配套修改 parser、DTO、摘要、持久恢复及测试；不能只让 Web 新传字段。

新请求由服务端解析清单并冻结精确内容，不再接受浏览器重新组装任意选中项。清单 revision/任务版本冲突返回 HTTP409（拟错误 `DELIVERY_SET_REVISION_CONFLICT`），前端重新展示当前清单，请用户重新确认所见成果，不能悄悄验收新稿。空/不可读/未就绪集合不可验收，区分请求错误、权限错误、临时读取错误，不伪造 completed。

沿用 Idempotency-Key、`GET .../finalizations/request` 和 `GET .../finalizations/{operationId}`。同键同清单返回原结果，同键异体冲突；写请求摘要包含集合身份/修订与完整来源摘要。GET 不推进操作、不调用工具。初始受理和冻结在同一事务/原锁边界内完成，后续沿用现有正式提交→验收→任务完成协调器。

旧操作只按原持久请求恢复；新界面统一新合同，不维护两套创建按钮/执行流程。接口兼容仅限实际在途操作与可恢复记录，不额外建设长期兼容层。

纯文字晋升需补可信 MESSAGE_SNAPSHOT 来源解析分支，复用已有正式交付服务；不能移除原输出校验来“兼容文本”。消息、选区、tenant/owner、任务/会话/指派及生产者归属均须验证。

## D5. 无多选的验收页（T06）

- 事项详情 → 原有“查看正式成果与验收” → D4 当前清单；显示成果卡及预览/下载，无 checkbox、调整交付按钮或折叠后的隐藏选择器。
- 主动作“确认验收”、次动作“继续修改”。继续修改只回原会话，保留清单；用户说明后由 Agent 更新，不直接改已生成文件。
- 没 READY 清单时显示实际处理状态/返回议事，不展示可点击的假验收。FINALIZING 显示真实进度；未知状态查原 operation；最终只有 TASK_COMPLETED 对应已完成。
- 验收不要求先保存；可选保存失败不回退验收，验收失败不重跑工具。完成后成果仍可预览、下载、保存；已验收集合不可被后续事件改写。
- 图文音频混合及跨轮修改必须保留正确集合；“自动选中当前全部卡片”不合格。

## D6. 已有能力的验证范围（T07–T08，不先重写）

| 能力 | 验证方式 | 失败后最小修复边界 |
|---|---|---|
| CHAT→INSPECT/EXECUTE | 使用真实 Agent 的现有能力，检查目录与实际读取区别、冷会话与多轮；正常请求不出现受控确认 | 现有 admission/context/continuation/Client 适配器，不另建新调度器 |
| 媒体实时展示 | 文本增量、就绪图片原位出现、音频播放/Range、文档支持格式预览，未知格式下载 | 现有 message parts/reducer/内容 API；事件去重及晚到补读 |
| 可选保存 | 文本整条/选区及媒体保存后重新打开，内容摘要一致；重试同操作 | 现有 archive 来源适配和状态恢复，不重生成 |
| 回传恢复 | 输出已完成但上传失败只补传原字节，刷新/断网不重复工具调用 | 现有 spool/outbox/status 查询；不扩展无依据超时 gate |
| 身份与密议 | 跨用户/任务访问拒绝；Agent 切换不串密议；身份切换清缓存 | 现有授权与作用域绑定，不削弱校验 |
| 双接入 | 山寨安顿/自家接应按各自真实客户端版本执行相同来源/结果合同 | 路径由适配层分配告知 Agent；不让浏览器读本机目录 |

播放能力不等于生成能力；音频场景可用合法现有素材验证传递/播放，不要求每个 Agent 凭空具备合成能力。图片验收必须由实际可用 Agent 通道产出真实图片，不拿原型 SVG 充数，不据未经核验的型号配置新付费服务。

## D7. 最终验收矩阵

| 场景 | 必须看到的结果 | 关联任务 |
|---|---|---|
| 无资料画鸟（照片风格） | 提需求→点将→真实图片→预览下载→事项验收；不强制保存或工程确认 | T01/02/05/06/07 |
| 图片+文档+音频混选 | 统一选择器、精确来源、Agent 按需真实查阅；未读不称已读 | T01/04/07 |
| 空正文只发资料 | 消息持久可恢复；可以澄清，不伪造用户文字 | T04 |
| 图A+图B+音频，只改图A | 新A替换旧A，B与音频保留；旧A仍在会话中；刷新一致 | T05/06 |
| 纯文字任务 | 完成文本有快照，可不保存而正式验收，无虚构执行记录 | T05/06 |
| 保存/下载 | 原始字节和摘要一致；保存后空间可读，失败不重跑 | T07/08 |
| 验收并发/断线 | 清单变更报冲突；同键恢复原验收，不误收新稿，不重复完成 | T05/06/08 |
| 密议/手机 | 密议不建任务、不携带待办资料；390/320px 无遮挡、＋可键盘操作、语音可取消 | T02/03/08 |
| 正式发布 | 明确 API/Web/Client 运行版本、同Run制品、实际线上闭环证据 | T09 |

正式验证由接手任务在授权执行阶段推进，复用 5260799 / 4403172；本次不读取账号密钥、不调用 Provider、不运行生产构建、不触发/取消 Flow。不因旧日志出现 RUNNING 就认定仍在运行；接手时先只读核对当前控制权与实际运行状态。
