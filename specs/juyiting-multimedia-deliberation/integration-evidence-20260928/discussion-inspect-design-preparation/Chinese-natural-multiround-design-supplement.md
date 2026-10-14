# 聚义厅自然多轮与全媒体闭包补充说明（临时冻结输入）

日期：2026-10-01。

状态：**L0 只读设计补充，不是已冻结 HTTP/wire、实现许可、上线合同或产品验收结论。** 本文基于 Client `71b26ce69d25a59f223499854b692e597b57d911` / tree `9675a2d85bf08a8e1af45d7c8e76106352db55a3`、API `8121e8d89ad0be13ddb79012b61955bac5ae8caa` / tree `e106bfa99b78c97ac2e6a765a7032a1db20dc9bf`、Web `8b8c951d4902a5927c85a43a3fcede525154509b` / tree `386d1e002c7fe53c6c9b992d3d669b50e8ea70fe` 的干净基线。它补充自然中文多轮、澄清、全媒体与双接应的产品闭包，不覆盖同目录既有四份准备材料，也不把其中任意 draft 自动提升为可上线合同。

## 1. 用户看到的是一个持续会话，不是手工协议控制台

用户第一次明确描述“画一只鸟”、完成点将且该次业务动作已经形成所需授权时，应在同一个悬赏会话内直接办理；不强制先调用另一个聊天模型，也不要求用户额外选择 `GENERATE_IMAGE`。

如果缺少真正必要的信息，应在创建执行占用、消费许可或 START 之前提出清晰问题，例如“你希望使用哪张参考图？”用户随后可自然回复，也可补充可用资料。回复必须关联服务器持久的确切问题，但界面不应要求用户理解 request/step/revision 等内部字段。

首稿产生后，用户可以直接说：

- “再鲜艳一点”；
- “把背景换成黄昏”；
- “换成黄鹂”；
- “先看看第二张参考图里是什么”；
- “这个音频里说了什么”；
- “把刚才那份文件作为资料，但先不要执行”。

系统应结合当前会话的因果链、当前聚焦成果、资料元数据和服务器权威 lineage，得到以下之一：

1. 直接普通回答；
2. 缺少必要事实时提出持久澄清；
3. 形成结构化执行 proposal，展示拟进行的操作、来源和影响，等待本轮必要授权；
4. 已存在本轮完整执行授权时进入对应执行。

只有歧义才澄清。不能为了系统实现方便，强制用户每轮手工选择 operation、重新点将，或先经过固定 LLM。规则、UI 明确动作、服务器元数据和受限 planner 都可以产生 proposal；它们都不能签发权限。

## 2. NONE、AVAILABLE、INSPECT 是资料使用方式，不是三个聊天系统

### NONE

本轮不携带资料引用。普通讨论、状态询问、文字补充和不依赖附件内容的澄清都可走 NONE。它可复用现有 durable CHAT 基础，但仍需下一合同补齐 schema-3 受理、因果状态与恢复。

### AVAILABLE

用户把精确资料声明为“本轮可用”，服务器验证身份、范围、版本与可见性，仅向 Agent 提供目录和必要元数据。AVAILABLE：

- 不读取、下载、打开、物化或转发资料字节；
- 不声称 Agent 已经看过图片、听过音频或读过文件；
- 不自动升级为 INSPECT；
- 不创建生成/编辑执行权限；
- 可用于识别“上一稿”“第二张资料”等候选来源，但语义仍有歧义时应澄清。

非执行讨论的资料类型与数量应由真实查阅能力合同冻结，不套用图像执行的来源上限，也不凭空新增固定数值。

### INSPECT

用户明确要求当轮查阅内容时，才进入 INSPECT。它必须同时具备：

- 当前认证 scope 和来源 ACL；
- 精确版本或当前会话资产引用；
- 服务器冻结的只读 manifest；
- 目标接应实际注册且已验证的对应媒体查阅能力；
- 真实读取路径、沙箱/工具策略和结果恢复证据。

浏览器能够预览、播放或下载，不代表 Agent 能理解该内容。`inspect` routing 标签、“只读”文字、approval 配置、通用 Codex 执行器或接应名称也不是能力证明。

当前 Client 基线明确不提供真实 INSPECT：能力声明为 unsupported/disabled，`runReadOnlyInspection` 会拒绝。因此完整产品中的图片、音频、文本和文件查阅仍是待实现能力，不能用 AVAILABLE 元数据或模型猜测冒充。

## 3. 真实 CHAT 声明与双接应

现有 Client 只有在 profile 明确满足 Fast CHAT、app-server、read-only sandbox 与 read-only-constrained tool policy 时才声明 CHAT enabled；同时 `strictNoToolsVerified=false`。这意味着当前可复用的是受约束 CHAT，不是已证明“绝对无工具”，更不是 INSPECT 或 controlled execution。

“自家接应”和“山寨安顿”是不同运行实例与归属方式：

- 自家接应使用自身 profile、Home、workdir、连接和能力声明；
- 山寨安顿使用 managed owner/generation fence 与独立 Home/workdir/readiness；
- 两者都必须分别注册真实 CHAT、INSPECT、媒体类型和 controlled execution 能力；
- 不能因名称、persona、部署位置或另一个实例已可用而继承能力；
- 不能跨 profile 混用 thread、manifest、资料路径、credential binding、持久 claim 或结果。

最终组合测试必须分别覆盖两种接应，而不是只在一个 mock adapter 通过后宣称“双接应完成”。

## 4. typed proposal、澄清结果与权限边界

当前 Client/API 链只传文本、delta 和 final，没有可持久化的 typed planning/clarification outcome。模型文字“我准备修改图片”只是回答文本，不能被 Web 或 API 重新解析为执行命令。

下一合同需要真实结构化结果通道，使服务器能持久表达：

- `ANSWER`：普通回答；
- `CLARIFY`：确切 pending question、所缺事实与 clarification revision；
- `EXECUTION_PROPOSAL`：候选 operation、精确来源、instruction、父链和当前授权状态。

proposal 是可展示、可确认的计划事实，不是 authority。模型、Client、Web 和 metadata resolver 均无权凭 proposal 创建外发、费用、operation grant、consent、execution 或 START。服务器仍须在用户明确接受当前新意图后，依据当前身份、assignment、来源、目标能力和 Provider/费用策略形成独立授权。

自然输入的最小路径建议：

- “再鲜艳一点”：若当前因果焦点只有一张可编辑的会话图片，可形成以该精确资产为来源的 EDIT proposal；有多张或没有明确焦点则澄清。
- “换成黄鹂”：如果上下文唯一指向当前图片，可提出 EDIT proposal；如果也可能表示重新生成，或来源不唯一，则询问而不是猜测。
- 用户在成果卡明确点击某一稿的“修改”：UI 已提供精确来源，可以直接形成 source-exact proposal，但仍不能跳过本轮授权。

不要求每次都调用 planner：服务器规则和显式 UI 已足够时直接产生 typed outcome；只有需要理解自然语言且规则无法确定时，才可选用受限 planner。

## 5. 初始澄清 resume 与后续新意图严格分开

### 初始意图尚未消费

首次点将已经授权了一个精确生成意图，但在 RESERVED/START 前发现缺少必要信息时，可以进入 `WAITING_USER`。服务器应持久保存问题和 resume context，并释放不应长期占用的执行资源。

用户回答后，可以继续**同一个尚未消费的初始意图**，前提是重新验证当前 task、assignment、requirement、target、grant、consent、资料和 capability 全部仍匹配。澄清回复本身不消费许可，也不创建第二次执行。

### 后续新意图

首轮已消费、完成或外部接受状态未知后，“再来一张”“再鲜艳一点”“换成黄鹂”均是新的业务意图。它们必须拥有新的：

- interaction key 和精确正文；
- request/step/intent；
- 本轮 operation/source 授权；
- 必要的 consent；
- execution/run/command；
- 持久 pre-call claim 和一次 START。

不能静默复用初始 grant、旧 consent、旧 command、旧 START 或 `CONSUMED` 权限；更不能把 UNKNOWN 当失败后换 key 再外发。

## 6. 同一会话、多 request、多媒体与因果链

一个悬赏 conversation 可以包含多个独立 request：普通讨论、资料可用声明、查阅、澄清回复、首次生成、后续编辑、再次生成或其它媒体办理。它们共享会话上下文，但不共享幂等键、执行权限或外发许可。

每个 request 应持久关联：

- 用户消息和目标 Agent；
- interaction kind 与 reference mode；
- 当前 task/assignment/conversation generation；
- 精确 input snapshot；
- `replyTo` 或 `continuationOf` 的真实因果关系；
- pending question、typed outcome、step 与必要的 execution/run 链；
- 独立 state version、事件 cursor 和恢复入口。

`replyTo` 只用于回答仍开放的确切问题；`continuationOf` 只表达上一稿/规划/执行父链。二者不可互换，也不能只保存在浏览器内存。

全媒体闭包必须分别处理：

- 图片：显示、查阅、生成、编辑、多个旧稿/新稿并存；
- 音频：播放不等于理解，理解和生成分别要求真实能力；
- 文本/文档：AVAILABLE 目录与 INSPECT 内容读取分开；
- 其它文件：只有实际 parser/adapter 能力和 MIME/ACL 合同覆盖时才可查阅。

不能为了支持全媒体而放宽冻结的 controlled-image v3 来源联合类型，也不能把会话资产伪装成 workspace 归档文件。

## 7. WAITING_USER、事件与恢复

`WAITING_USER` 是可交互的非终态，不应继续让整个 composer 禁用。Web 需要明确显示“正在回答哪条问题”，只允许绑定该 pending question 的回复或独立普通讨论；真正有执行租约占用时才按执行事实限制冲突操作。

事件与读回至少要让刷新/重连重新得到：

- 当前 request/step 和状态版本；
- 开放的 pending question；
- 已回答/已 supersede 的澄清事实；
- typed proposal 及其精确来源/父链；
- 已创建 execution/run/asset 的权威关联；
- 多个旧稿和新稿的持久媒体事件。

网络结果未知时，先用原 Idempotency-Key 做只读恢复；404 不证明原 POST 未受理。不能自动换 key、删 refs、退回 legacy、重放 Provider 或创建第二份 consent。迟到事件必须受身份、会话 generation、request/step 和 state version fence，不能污染用户当前选择。

## 8. 保存、正式提交、验收与任务完成相互分离

会话中的已验证媒体资产即使尚未保存到个人工作空间，也应可在权限有效时继续预览、下载和作为精确上一稿来源。

- “保存到空间”创建工作空间引用或版本；不改变原会话资产 producer lineage。
- “正式提交”选择成果形成正式 delivery manifest；不是简单把所有会话产物都提交。
- “验收”针对正式提交的成果及需求标准；不因模型回答或 asset ready 自动完成。
- “任务完成”是更后的业务状态，不能由生成成功、保存成功或一次聊天自动推导。

operation grant 或 consent 被消费/撤销，不应删除已经合法提交并仍可读的资产；资产读取、归档和正式交付继续使用各自 ACL 与状态事实。

## 9. 当前可复用与明确待实现

### 可直接复用的实际基础

- 同一 bounty conversation 与 durable request/turn/event 基础；
- DISCUSSION/NONE 的现有持久 CHAT admission；
- bounded history、task facts 与 metadata-only availableRefs 投影基础；
- 严格 target runtime capability negotiation；
- 会话资产 producer lineage、预览/下载及旧稿持久事实；
- 已冻结的 controlled-image EXECUTE owner authority 与 disabled Client v3 source wire；
- Web 现有会话、事件、成果展示和身份/选择 fence 的部分基础。

### 尚未实现，不能宣称 READY

- schema-3 DISCUSSION/CLARIFICATION_REPLY 的冻结 HTTP/DTO/digest；
- 持久 pending question、clarification reply CAS、resume 与因果链；
- typed ANSWER/CLARIFY/EXECUTION_PROPOSAL runtime/API/event wire；
- 严格 AVAILABLE source resolver 与零字节证明；
- 真实图片/音频/文本/文件 INSPECT adapter、manifest、ACL 和能力声明；
- WAITING_USER 可回复 Web 状态与唯一 follow-up composer/成果卡编排；
- 双接应真实组合；
- 多 request、多稿、多媒体事件恢复；
- 保存、正式提交、验收及需求完成的最终跨仓闭包；
- 真实 Provider 账户/费用/外发授权与产品验收证据。

## 10. 需要 API Owner/Main 冻结的决策

1. DISCUSSION 与 CLARIFICATION_REPLY 的严格 schema-3 字段、null/empty/Unicode、版本域、canonical digest 和错误响应。
2. pending question、reply CAS、resume、proposal 和 causality 的表约束、锁顺序、状态机、事件及 GET 投影。
3. NONE/AVAILABLE/INSPECT 的严格 source union、排序、媒体能力和实际边界；不得借用无关固定数值。
4. typed Client outcome 的确切 event/DTO 以及服务器如何验证当前 dispatch、scope 和 refs。
5. 真实 INSPECT 的 manifest 传输、字节物化、工具/沙箱策略、双接应能力声明及验证证据。
6. 初始未消费 intent 进入 WAITING_USER 后如何安全 resume，以及何时必须成为后续新 intent。
7. Web 原键恢复、WAITING_USER 回复和 proposal 接受后进入既有 EXECUTE preview/consent/admit 的确切状态机。
8. 全媒体资产事件、保存、正式 delivery、验收和任务完成之间的权威边界。

## 11. 既有 draft 的语法与冻结纪律

同目录 `03-minimal-contract-proposal.md` 保持 immutable，不在本补充中修订。Main 指出的“1.2 accepted JSON 看起来多一个 `}`”应作为冻结前检查项保留：当前文件第 48–69 行展示的是候选 `CLARIFICATION_REPLY` body，第 88–101 行展示候选 accepted projection；无论目视是否配平，二者都只是 draft。

正式冻结前必须把最终候选分别保存为独立机器可解析 fixture，执行严格 JSON 解析、字段集合、unknown-field、kind-specific nullability 和响应 shape 校验。不能通过修改说明文字来推定 wire 已正确，也不能因某段 JSON 能解析就认定字段、HTTP 状态或语义已经获准上线。

## 12. 非授权声明

本文没有修改仓库、ledger 或 SDD，没有运行测试、Gradle、构建、数据库、网络或 Provider，没有选择账户/模型、产生费用或部署。本文不能授权真实外发，也不能把 API/Web Owner 正在实现的半成品、旧 proposal 或任意设计文档当成完整产品已完成。
