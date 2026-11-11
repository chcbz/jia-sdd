# 图片与文件对话交付 MVP：C0 只读能力盘点

日期：2026-09-18。状态：**源码/本机部署目录盘点已完成；真实工具执行、线上配置与运行时合同仍待核实，不能转 ready 或声称 MVP 可用。**

范围：生图、原图修改、资料生成 PPT，以及用户上传 PPT/Word/PDF/Excel 后让 Agent 读取、对话修改、预览和下载。不建设在线内容编辑器。本轮无应用代码修改、无用户任务提交、无 Provider 调用、无安装/重启/发布、无运行台账变更。

## 1. 结论

现有系统不是从零开始：已有 Agent 会话、任务、成果存储/版本服务、owner 成果读取、图片/文本预览和正式交付/要求修改基础。但**用户输入文件 → Agent 真正读取/修改 → 自动回传文件 → 对话领取新版本**尚没有足够证据证明已打通。

优先补的是以下四段，而不是再造一套成果系统：

1. 用户私有输入文件及对话引用；不能把用户上传伪装成 Agent 生产的成果。
2. 运行时在任务隔离空间获取输入，执行实际图片/文档工具。
3. 运行时以真实 Agent 身份自动提交指定输出文件，可靠保存后才报告可领取。
4. 文件名/类型、Office/PDF 只读预览、源版本绑定和“继续修改”的对话接线。

**只在网页加上传按钮，或只安装几个技能，均不足以完成 MVP。**

## 2. 证据边界与精确基线

- API：`e15f7020bf77153912aafce15fc11c67b2f06e11`，tree `551c452f1a81bbc6f6b198452891d2189b967fd8`。
- Web：`737506e7af06bb4ea4ec2386dc507ec745297481`，tree `05f1c965cd07bb02ef5caaf551f5ab4c87fbfc21`。
- 上述来自已核对的 1.9.6 发布记录，本轮以 `git show <SHA>:<path>` 读取；不是用陈旧/有改动的 checkout 推导线上，也不是重新完成全量发布审计。
- 本机运行时 `current` 指向 `/home/isp/apps/codex-ws-agent/releases/1.1.0-m4.20260913-677c29d8c10e-single-registration-hotfix-20260917`。
- 该目录 `agent-client.mjs` SHA-256：`1d3a41539478c9907e96c5d3e35192282b2b33433db27d2d328cb755ca11de95`；版本源码 checkout 同名文件：`e0c126ae7141cfccac1a47deec01c217a3d12f023fd275871864ee4a118c46cc`，**两者不相同**。不可直接在旧 checkout 上实现后覆盖部署副本；需先找到/归拢准确源码基线。
- 只读观察到一个对应 Node 入口进程、配置文件中三个 profile。不是全站 Agent 数、账号名册数或在线能力证明；未证明进程内已加载字节与此刻磁盘文件完全一致。
- 原浏览器只读审计继续引用 `docs/implementation/evidence/mvp-audit-20260918/`；本轮未重做浏览器操作，更未把旧读取证据写成生成验收。

可重现证据：`docs/implementation/evidence/creative-delivery-c0-20260918/inventory.json`，包含 exact 源文件哈希、运行时磁盘哈希和脱敏的环境观察，不含凭据/会话正文/用户附件。

## 3. 逐段盘点：可复用 / 缺接线 / 需新增 / 未验证

| 环节 | 已看到的证据 | 判定与补齐项 |
| --- | --- | --- |
| 对话、目标 Agent、任务 | `useHallConversation.js` 发送显式 target/task 和 metadata；`ChatMessageDTO` 有会话、内容、任务、目标和 metadata | **复用 + 缺接线**：有通用 metadata 不等于已存在安全文件引用；需输入引用、源成果版本和对话修改合同 |
| 上传文件 | `ArtifactTransferPanel.vue:14–43` 是手填成果 ID、版本、可见范围的上传表单 | **新增输入语义**：不能把它当用户材料上传入口。其文件选择与 composable 白名单未列 Office MIME |
| 成果持久化/版本 | `AgentTaskCollaborationServiceImpl.java:304–380` 有 task-root 锁、ACL、producer、版本 CAS、存储和事件 | **复用**：扩展文件/预览元数据，原图和资料标记 input，不另建成果成功台账 |
| 用户取件 | `AgentTaskDeliverableController.java:63–101` 有 owner 列表及精确版本下载，无需 owner 假冒 actorAgentId | **复用**：优先 owner 路径，保持同一 task/owner 隔离；真实存储启用/类型配置未在本轮验证 |
| 图片/文本预览 | `OutputPreview.vue`、`useOutputs.js:241–245` 已有文本/PNG/JPEG 预览逻辑 | **复用 + 扩展**：不是没有预览；PDF/Office 逐页/工作表预览仍需实现或接线 |
| 文件类型与名称 | 前端上传允许 PDF/图片等，未列 Office；API 存储默认白名单也未列 Office；HTTP 下载为 `.bin`，成果列表下载使用 title | **需修整**：精确 MIME 与安全文件名/扩展名、格式验证必须贯通。不能断言所有下载都为 `.bin`，也不能靠改后缀或伪装 ZIP 绕过类型支持 |
| Agent 收到输入文件 | 部署 `task-context-pack.mjs:199–222` 校验的成果为 ID/版本/哈希等元数据，非文件字节；`resolvePrompt` 主要取文字字段 | **缺接线**：尚未证实有任务授权的输入下载/落盘和文件引用交给工具的链路；metadata 不能替代真实文件 |
| Agent 回传输出文件 | 部署 `agent-client.mjs:3833–3880` 主执行结束回传文字 `output` 和状态；`artifact.publish` 出现在协议枚举不代表自动发布已实现 | **缺接线**：未发现该主路径自动收集指定输出、上传并等待持久回执；不能据此排除所有远端/外挂扩展 |
| 可信自动生产者 | API `AgentWebSocketHandler.java:255–266` 的普通 `work.result`、`artifact.publish` 等仍 deferred；HTTP artifact publish 需用户 JWT + actor | **需新增/扩展可信适配器**：复用已有 native runtime 身份能力，不把用户 JWT 塞进 Agent 冒充 producer。legacy task.report 与专用 skill result 另有处理，不等于所有 WS 消息失效 |
| 正式验收与返工 | 现有 formal-deliveries GET/POST/decision、lease/CAS、成果 manifest 与前端控件 | **复用 + 接线**：对话“修改第三页”需绑定确切源版本，进入已有返工域；正式提交当前 HTTP 也需 JWT，自动提交须设计真实身份适配，不能绕过 lease |

已有源码中的 16/64 MiB、预览字节/像素限制是**当前实现事实，不是本方案推荐门槛**；按用户 Gate Evidence Policy 核对依据和最小范围，不盲目继承或换成更大的任意值。

## 4. 工具能力，不以名称代替执行证明

### 4.1 本机部署 Agent

- 三个本机 profile 配置使用 `gpt-5.6-luna`、隔离的 Codex Home；模型配置值不是文件生成/图片工具能力证明。
- 各 Home 的技能目录均能找到 `imagegen/SKILL.md`，其内容区分内置工具与需明确授权的 CLI 路径；本轮未调用任一路径，实际运行时工具暴露、Provider/额度仍未知。
- 在所检查 profile 的 skills/plugin-cache/workspace skill roots 中未找到专门的 PPT/Word/PDF/Excel 技能。**这是定向目录观察，不等于模型不能写代码或其他服务不存在。**
- 部署源码 `resolveProfileAbilities`（约第 3422 行）实际调用 `discoverWorkspaceAbilities`；`discoverCodexSkills` 虽然存在，不是此处实际注册入口。故技能文件存在、名册能力和实际可执行能力必须分开。当前接口文档“合并所有 skill 名”的旧描述不能直接当运行事实。
- 缺少 workspace policy 的 profile 普通 command 路径会受限制，而 chat 是另一条路径；不能为获得文件权限把 chat 或工作目录放开。文件任务应使用明确隔离、明确工具权限的任务执行路径。

### 4.2 可复用代码与宿主机依赖

| 类型 | 只读观察 | 能说明什么 / 不能说明什么 |
| --- | --- | --- |
| Word | exact API 的 `WordUtil` 有 doc/docx → HTML 辅助代码 | 可评估预览复用；不是已接入 Agent 的文档修改器，转换输出必须按不可信内容处理 |
| PDF | exact API 的 `PdfUtil` 有 PDF → HTML 辅助代码 | 可评估基础读取/预览；不证明 PDF 内容修改、版式保留和逐页预览已可用 |
| Excel | `ExcelUtil` 有 POJO 导入/导出；业务调用见用户导入 | 可复用基础处理经验；不等于任意用户工作簿/公式的无损修改 |
| Java 依赖 | `jia-common-core/build.gradle` 的相关库主要为 compileOnly，测试另有依赖 | 不能仅凭源码导入就断言生产 classpath 已含相应工具 |
| 本次 shell 的 Python | 3.6.8；`openpyxl` 可发现，`pptx/docx/pypdf/fitz/PIL/reportlab` 在该解释器未发现 | 只证明本次解释器模块发现结果；不代表各 Agent sandbox、虚拟环境或远程服务 |
| 本次 shell 的 PATH | 能定位 tesseract；未定位 libreoffice/soffice/pdftotext/pdftoppm/mutool/pandoc | OCR 命令存在不等于 OCR 数据/流程可用；未在 PATH 发现也不是全机不存在 |

本轮不安装工具、不选择付费 Provider、不估计未经测算的生成成本。工具选型应在实际执行隔离环境及文件样例上验证，不能把开发助手内置工具视为产品能力。

### 4.3 分格式当前状态

| 用户能力 | 现状结论 |
| --- | --- |
| 生图 / 按原图改图 | 有技能说明线索；实际工具可用性、原图传递、输出回传均待验证 |
| 新建 PPT / 修改外部 PPT | 未取得运行时生成/修改/渲染链路证据，需接入明确工具 |
| 修改 Word | 有服务端转换工具代码可评估复用；读取/编辑/导出闭环未验证 |
| 修改 Excel | 有导入导出工具代码及宿主 Python 模块线索；复杂工作簿/公式保持未验证 |
| 修改 PDF | 有转换工具代码线索；真实内容修改与预览闭环未验证，扫描件另列 |

## 5. 最小接线方案（候选，不是冻结 API 合同）

### A. 用户侧输入与对话

- 为既有 task 增加私有 input 语义和输入文件引用；身份从当前认证推导，不接受任意 owner/服务器路径/远程 URL。
- 上传后返回文件引用、实际类型、名称、哈希、版本、读取能力状态；绑定前验证与 task/conversation/Agent scope 一致。可以先建轻量草稿任务，不要求用户手填工作项或技术 ID。
- 同一会话发送文字 + 输入引用 + 明确目标；修改消息另绑定 source artifact/version，歧义先澄清。
- 输入/输出继续使用既有存储与权限机制的可复用部分，但用户输入不能借用 `producerAgentId` 假装 Agent 成果。

### B. 运行时文件桥接

- 推荐补一个有明确版本和权限的文件桥接能力：领取被授权输入到本任务空间 → 把文件交给实际工具 → 校验明确声明的输出 → 以 runtime 身份上传 → 获得持久回执。
- 凭据留在可信客户端/适配器，不交给生成模型或写进对话；不得通过公开 URL、共享全机目录或扫描其他任务成果实现“自动交付”。
- 输出以显式 manifest 指定相对路径、文件类型、哈希、源版本、预览关系和改动摘要。校验路径归属及符号链接边界，不自动搜集目录中全部文件。
- 上传失败恢复同一文件；执行结果未知先查 receipt，不重复生成/收费。普通聊天结束不等于文件交付完成。
- 优先评估已有 runtime 身份下的 HTTP 文件传输适配，复用 artifact service；不要把大量二进制直接塞进现有 WS 文字回报。最终路径、schema、鉴权和提交事务仍需冻结。

### C. 用户领取与继续修改

- 复用 owner deliverables 和正式交付列表；统一安全下载名称/扩展名，保留原文件、派生版本、历史和任务关系。
- 图片复用现有预览；文档建立与原文件版本/哈希绑定的预览附件或投影，所有页面/工作表同样鉴权。
- 预览失败单列错误，不抹掉已保存的可下载文件；但不得宣称完整预览验收通过。
- “继续修改”仅带着明确版本回到 Agent 对话，映射既有 rework；无需页面内画布或 Office 编辑器。

## 6. 实施顺序与范围决策

排期补充：下列为原运行时接线顺序；最新 `docs/implementation/VERSION_PLAN_20260918.md` 已将不依赖客户端的个人文件库先排为 1.10.0，Word 闭环排 1.11.0，图片/PPT 排 1.12.0，完整 MVP 排 1.13.0。客户端待确认不阻塞基础文件库。盘点事实与证据未改写。

1. **C0 后半段**：确认版本化客户端是否纳入本需求范围，找回与部署副本一致的源码基线；核实工具暴露、真实存储配置、授权和逐格式执行环境。保留现有运行，不触碰其他任务进程。
2. **C1 合同**：冻结 input/output/preview/source-version schema、用户与 runtime 双身份、上传/领取/回执、幂等、lease/事务、错误和恢复语义；补足方法/路径后才可转 ready。
3. **最小纵向切片**：选择一份无敏感数据的普通 `.docx`，先做“上传 → Agent 读取并改一段 → 自动交付新版 → 预览/下载 → 再次对话修改”。这是建议顺序，不代表 Word 已有运行时能力；若 C0 实测表明另一格式更容易，按证据调整。
4. **并行扩展**：合同稳定后图片工具、PPT、Excel、PDF 按非重叠路径扩展；每格式分别记录通过/不支持/未测。只完成切片不能宣布全部文件 MVP 完成。
5. **集成验收**：保留原件、非目标内容、双身份隔离、刷新/离线取件、上传中断/重复回执、预览失败、文件打开与实际内容修改，绑定 exact source/制品/配置。

### 必须明确的范围边界

此前未包含 `isp-install` 客户端改造。当前发现的输入落盘、可信输出提交和完成回执属于运行时边界；**推荐允许在版本化 `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/` 做最小文件桥接改造**，不直接改 `/home/isp/apps/...` 部署副本，不顺带重构客户端。

在该范围确认前，仍可继续完善 C1 文档；不应把“网页/API 可以改”误当成客户端也已获授权。若坚持不改客户端，需要另行证明现有可用的受信工具/适配器足以完成输入输出，否则不能承诺自动交付。付费额度、资料外发和生产改动另遵现有授权，客户端授权不替代这些授权。

## 7. 可复用的测试入口与本轮检查

后续按变更选择已有测试：
- Web：`tests/juyiting-artifact-transfer.test.js`、`tests/output-delivery-rb05.test.js`、`tests/formal-delivery-od10.test.js`、`tests/juyiting-hall-conversation.test.js`。
- API：`AgentTaskArtifactControllerTest`、`AgentTaskDeliverableControllerTest`、`AgentTaskArtifactStorageF02Test`、`AgentTaskFormalDeliveryServiceImplTest`、`AgentTaskFormalDeliveryDecisionServiceImplTest`、`AgentTaskContextPackControllerTest`、`AgentWebSocketRuntimeAuthenticationTest`。
- 新增定向验收应覆盖输入不冒充成果、真实 runtime producer、失效授权/任务隔离、源版本冲突、上传恢复、每格式文件打开/内容保留。旧测试存在不等于本次已经执行。

本轮：exact 源码和部署目录只读；JSON 证据与本地文档结构检查、`git diff --check`。未运行应用测试/构建/部署或生成任务。Python 环境缺少 `tomllib` 与 `importlib.metadata`，已归因为 3.6.8 标准库差异，改用显式白名单扫描与模块存在性检查；未安装依赖、未盲目重试，未声称完成 TOML 全量解析或依赖版本核验。

## 8. 后续业务范围补充：个人工作空间

用户在盘点后明确要求个人工作空间。上文为当时源码/部署目录事实及候选接线，不改写其证据；候选“先建任务上传”调整为 owner 文件库允许无悬赏上传、任务关系可选，在执行时绑定明确 task/run 授权。最新设计以 `specs/juyiting-creative-delivery-mvp/workspace-design.md` 为准，空间对已有成果采用投影复用而非另造 artifact。该新增业务范围尚未实现，也没有新增运行时测试结论。
