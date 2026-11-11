# Codex 原生执行技术详设 v2：核心底座与依赖总览

创建日期：2026-10-27；设计修订：2026-10-28（Asia/Shanghai），v2.1（规格/源码/模拟复核）。Owner：本聊天主 Agent。
状态：设计，未实施/部署。配套范围方案：`/home/isp/wsps/cyf/specs/juyiting-skill-execution/native-execution-plan-20261027.md`。
固定源码：见 `/home/isp/wsps/cyf/docs/implementation/handoffs/CODEX-NATIVE-SKILLS-20261027.md` 四仓HEAD/tree；此次定向核对这些工作区的实际源码，不视为远端最新或生产状态。工作区其他任务脏改动不纳入本次交付。
公共接口：`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4。文中“拟新增”接口/状态是待实现的内部设计，不冒充现有 wire；落地时同步现有 management-contract、DTO/schema与消费者测试。官方检索本次未取得有效正文，app-server新接线以固定实际二进制schema验证，不凭通用文档推断生产支持。

## 0. v2分层、依赖和阅读顺序

本次从“已有技能原生执行”扩展为“无技能探索→真实成果→提取技能→新任务复用”。原有回传/恢复细节保留；图片、Office、浏览器和新增视频/技能提取移入独立扩展详设：`/home/isp/wsps/cyf/specs/juyiting-skill-execution/native-execution-extensions-20261028.md`。

**核心不依赖任何具体业务技能或服务商；技能是经验包，不是执行通行证。** 工具决定可执行能力，授权决定允许范围，模型决定业务步骤，技能提供复用指导。核心可以在skills集合为空时执行。没有工具/权限不能靠技能说明补足。

### 0.1 核心模块与直接依赖

| 模块 | 边界/输出 | 直接依赖 | 本文细节 |
| --- | --- | --- | --- |
| C0 执行合同与授权 | 无技能/有技能统一接纳、输入/输出/工具范围、身份和lease | 既有API身份/任务体系 | §4、§9–10 |
| C1 原生执行与隔离 | 固定app-server、thread/turn、命令/工具、沙箱生命周期 | C0 | §5–6 |
| C2 基础材料与工作区 | 原文件/图片载体、基础文本读写、任务路径和草稿 | C0、C1 | §5、§7–8 |
| C3 受控工具机制 | 工具能力注册、凭据引用、外部操作/effect、取消/恢复 | C0、C1 | §6、§11 |
| C4 成果交付 | 快照、选择、stage/commit/receipt、投影/下载 | C0、C2 | §7–10 |
| C5 执行证据与提取素材 | 工具/脚本/成果版本关联，授权留存和回收 | C0、C1、C2、C3、C4 | §13 |
| C6 技能包生命周期 | 既有安装/版本/发现、授权集合只读挂载 | C0、C1、C2；既有技能管理 | §4–5 |

依赖是实现/能力依赖，不表示每个请求都调用所有模块。C5从执行开始增量记录，不能等C4提交结束才追溯脚本；C6先负责包管理基础，不依赖技能提取E6。这里模块是代码职责，不要求拆七个服务或新建插件市场。

### 0.2 依赖图

```text
既有身份/任务/API合同
          ↓
         C0 → C1 → C2 → C4
          └──────→ C3
C0/C1/C2/C3/C4 ──→ C5（从开始记录，到成果关联）
C0/C1/C2 + 既有技能管理 ──→ C6

C1/C2/C3/C4 → E1 图片、E3 浏览器、E4 通用HTTP
C1/C2/C4    → E2 Office、E5 本地媒体
C1/C2/C4/C5/C6 → E6 技能提取

E5 的素材可选来自 E1/E4/E3，不是硬依赖
E6 验证视频技能可选使用 E5；提取文本技能不需要 E5
```

精确直接依赖以上表及扩展表为准；图中省略传递箭头。核心只认工具能力和通用结果，不按图片/视频/Excel技能名称分支；扩展通过工具接口使用核心。新增普通技能仅增加包，新增依赖更新固定工具制品，新服务优先E4脚本/配置；只有新安全/恢复语义才修改核心合同。

### 0.3 分阶段交付（不是只改Runtime）

| 阶段 | 必要内容 | 验收边界 |
| --- | --- | --- |
| K1 核心最小闭环 | C0/C1/C2/C4 + C3本地工具接口 + C5最小脚本/事件留存 | skills为空，读TXT/写文件/真实下载；恢复不重做 |
| K2 通用机制完整 | C3、C5完整、C6；保留既有图片服务不中断 | 通用effect、多技能/空集合、旧版本恢复、来源可追溯 |
| X1 原需求能力 | E1/E2/E3（其依赖满足后可并行） | 生改读图、常规文件、网页操作全部回归 |
| X2 探索与沉淀 | E4/E5；E6文本切片可先独立做 | 无技能完成视频→提取→安装→新参数复用 |

API负责接纳合同、资料/结果、来源/候选和管理衔接；Runtime负责真实执行/工具/快照；Web复用任务/技能界面补足状态、提取与成果交互。核心是架构层，不等于Runtime单仓。阶段无新增人工审批；发布和外部付费仍按实际授权。

### 0.4 本轮复核约束（2026-10-28）

复核记录：`/home/isp/wsps/cyf/specs/juyiting-skill-execution/native-execution-review-20261028.md`。发现8项设计缺口/需细化边界，已在本详设和扩展文档修订；这些修订不是产品修复。2026-10-28用户已确认复核记录§4的两项默认规则：技能归当前用户私有，仅向有管理权的Agent安装，不自动公开；已保存脱敏包独立保留至用户删除，源资料按既有规则删除，并尊重明确隐私/权利撤销要求。

本设计沿用management-contract.md末节2026-10-26口径：安装/升级动作批准固定候选requiredPermissions，不增加逐权限勾选或逐Agent确认；平台不新增运行费用预算/预扣/价格未知拒绝门禁。对具体任务的数据外发、账户操作和发布范围核对，不等于每次Provider调用都弹费用审批。真实技能购买报价规则不变。提取候选验证和安装依赖就绪分开；缺实际依赖不能标可运行或借提取绕过安装准备语义。

### 0.5 本任务实施约束（2026-10-28用户确认）

- 遵循已有架构，先实现K1最小闭环；不增加未要求的功能，不另建通用框架。
- 禁止为不可能的场景写防御性代码；错误处理仅覆盖实际可发生且需要恢复的失败路径。实现时对应具体风险、触发条件和回归入口，不因设计列出机制就无条件扩建；既有身份/ACL、幂等和数据完整性保护继续保留。
- 简单、明确、低风险的请求直接完成，不重复规划或展开长篇方案。这些约束仅适用于本任务，不修改全局或共享技能规则。

## 1. 首先厘清三个不同的“返回”

1. **模型消息**：流式文字、工具进度、最终说明；用于展示，不授予操作权限，不证明文件存在。
2. **执行成果**：真实文件快照、结构化数据、输入交付证据、固定结果清单；由bridge控制收集和提交。
3. **后端提交/归档事实**：后端认可清单并完成业务投影；这是页面可用成果及任务完成的依据。

`turn/completed`只说明模型回合结束；HTTP 200、WebSocket发送成功、模型写“已生成”也不能单独代表任务完成。bridge不修改模型的业务结论来控制回传，而是控制哪些真实文件可以被提交、提交给哪个执行、何时可声明交付成功。

## 2. 已核实的现有基础与缺口

Runtime源码前缀：`/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/`。

| 源码 | 已存在 | 原生执行所需改造 |
| --- | --- | --- |
| `skill-executor.mjs` / `executeSkill` | 精确包、TaskSkillBinding、claim/resume、runner、结果持久化、stage/commit/receipt | 加入真实原生执行runner，不绕过外层执行生命周期 |
| `agent-client.mjs` / `runSkillNativeModel` | 只读模型返回JSON，宿主后写成果 | 不能把现有native-model名称当原生文件操作；新增隔离工具执行模式 |
| `app-server-adapter.mjs` | thread/turn，文字/终态，read-only与拒绝server request | 明确执行模式策略，工具事件、授权回调、取消/恢复，不能全局取消限制 |
| `skill-conversation.mjs` | lease/fence、inputs、上传、result-commits、resume读回 | 接新runner和成果快照，扩展格式/元信息；保留摘要和持久回执 |
| `skill-execution-store.mjs` | 原子JSON/checkpoint、blob、结果绑定、SkillEffects | 模型草稿与可信blob分离、流式文件快照、多步tool/effect映射 |
| `conversation-native.mjs` | 输出MIME/内容校验 | 当前有固定16MiB和非空限制；不能直接作为新通用文件规格 |
| `skill-install-manager.mjs` | 受管安装、当前视图/保留版本 | 当前完整包实体收口及固定版本只读挂载 |

API入口已核对：
- `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/PersonalWorkspaceConversationRuntimeController.java`：stage、resume、result-commits。
- `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/api/ChatSkillResultController.java`：用户结果查询；COMPLETE时核对关联状态后给出成果。

`report-outbox.mjs`的`work.result`执行报告及管理回执不是文件成果commit；不能把它的ACCEPTED当成文件已交付。原生文件继续复用conversation结果链，不额外并行提交第二个权威结果。

## 3. 从接纳到交付的完整时序

```text
用户 → Web/API：任务意图 + 附件引用
API：身份/任务权限 → 固定输入快照、执行、工具授权、可空技能集合和输出范围
bridge：claim/resume + lease/fence → 查询是否已有结果/未知effect
bridge：准备输入、固定技能视图、执行Home和工具能力
bridge → app-server：绑定thread/turn，提交指令和材料索引/原生图片
Codex → 本地工具：读文件、写草稿、调用技能脚本
Codex → 图片/浏览器MCP：受控操作，bridge记录工具/effect事实
Codex → artifact.stage：申请将实际草稿冻结为候选成果
bridge：安全打开/快照/校验/算摘要/持久化 → 返回artifact引用
Codex → result.propose：选择最终候选成果及说明（不提交后端）
app-server → bridge：回合completed
bridge：确认提案、工具状态、授权和输出合同，冻结唯一result
bridge → API：逐文件stage → 核对stage回执
bridge → API：提交result manifest → 核对commit回执
响应丢失：bridge → API resume读回持久事实；不重新执行模型/Provider
API：归档/投影 → 用户结果查询可返回可下载成果
bridge：持久receipt → 释放本执行资源；按可恢复性清理
```

MCP工具名 `artifact.stage`、`result.propose` 是本项目拟新增逻辑名称，最终transport合法工具名在固定MCP协议适配时映射；不是宣称Codex内置这些方法。

## 4. 执行身份、授权和单/多技能问题

### 4.1 服务端绑定的执行上下文

bridge在内存和私有checkpoint中绑定：tenant/client/owner、Agent、task/run/conversation及generation、executionId、commandId、输入snapshot摘要、可空的固定技能安装/摘要集合、工具能力、threadId/turnId、lease/fence、取消/撤销状态。

这些字段来自已认证API/受管本地状态。模型工具参数不得选择另一executionId、Owner、Provider凭据、安装版本或API地址。每个MCP连接/服务实例由bridge预绑定执行，不能仅信任模型传入taskId。

### 4.2 基础能力与技能执行授权（v2替代必须先有技能的假设）

- 新原生接纳合同绑定执行身份、输入快照、工具能力、输出范围和**可为空**的精确技能集合；无技能不伪造TaskSkillBinding、不自动安装“万能技能”。
- 普通任务使用C1/C2基础工具即可探索、编写临时脚本并交付；临时脚本只能在当前沙箱权限内运行，不被当成已安装受信技能或新的网络授权。
- 现有v4 parseSkillCommand要求单skill/TaskSkillBinding，不能直接删校验或把null塞进去。新增原生执行合同显式协商，将公共claim/resume、材料、effects、结果提交生命周期复用/提炼给无技能和有技能入口；旧命令继续按原精确包解释。
- 非空技能集合复用现有安装/TaskSkillBinding权威，接纳时固定每包安装ID/摘要及授权，不挂全部主Home。新集合字段/执行语义同步API、Runtime和Web消费者，不依靠旧消费者忽略未知字段执行。
- 基础TXT/Markdown读取不新增购买项；任务使用付费/外部工具须有相应授权，技能为空不是任意外网/任意凭据权限。
- 输出合同来自用户任务和工具能力，不要求从某个技能manifest推导。要求MP4的任务明确允许该类型，纯读图解释可无文件；现有只允许单TXT的合同不能冒充支持视频。
- 需要未获准工具/技能时返回具体缺口，用户授权后按明确的新执行/授权修订绑定继续，保留旧执行未知effects，不偷偷重放。

### 4.3 新旧合同落点：复用生命周期，不冒充旧接口已支持空技能

| 现行约束 | v2目标 | 兼容边界 |
| --- | --- | --- |
| parseSkillCommand及executor强制skill/descriptor | 通用执行入口先验证执行合同；非空技能逐包核验 | 不移除旧命令所需绑定；新入口明确协商 |
| 输出合同取descriptor.manifest.outputs | 无技能取服务端冻结的执行输出合同，有技能还满足其声明 | 不创建假manifest/虚拟已安装技能绕校验 |
| result/inputReceipts校验依赖runner | 原生载体按实际文件交付方式核验 | 不冒称local-script或已阅读全文 |
| claim/resume/result-commit及结果查询基于旧技能/协议 | 复用状态存储、锁和相同提交语义，扩展明确的原生接纳/读取分支 | 必须改API服务和消费者；不声称仅Runtime改造 |
| 用户结果查询含旧协议条件 | 能读取明确的新执行类型及其投影 | 旧历史按原摘要/绑定读取，未知执行语义不猜测 |

本文§9记录已核实的现有路由/preimage，作为复用基线，不保证无技能新合同能原样通过现有校验。实施时在现有管理合同列出实际字段/协议版本、生产者/消费者和混合回归；路径能复用则复用，不为命名统一另建结果系统。新结果绑定仍包括执行身份、输入快照、输出范围及有技能时的精确包，不因skills为空丢失授权来源。

### 4.4 材料清单、失败材料与执行中新增材料

接纳时完整来源清单包含全部用户引用及其交付状态，冻结输入快照不静默移除失败项。当前v4要求每个冻结input都有DELIVERED回执，且不接受额外input；因此原生合同必须明确区分“所有来源的处理记录”“已交付输入集合”和“本次输出必需输入”，不能把失败附件伪报DELIVERED。

新原生合同在固定来源清单中绑定逐项成功/失败/未支持事实及范围；仅当任务可独立完成且用户要求允许时交付部分结果，并说明缺失项。影响必须输出的材料失败则该目标不可成功。旧v4仍按原全量回执规则读取/恢复，不修改其摘要。

浏览器下载、图片/视频工具输出属于执行中派生材料，不追加进原用户输入回执，也不覆盖原snapshotHash。bridge追加不可变派生记录：当前执行、产生的工具/operationRef、字节hash、来源地址或原材料引用（秘密脱敏）、当前ACL、可用于哪些后续工具。必要时以新原生合同的派生清单摘要绑定最终结果。下载到文件不等于得到上传到另一站点的授权；后续外发仍核对范围。

### 4.5 有效能力计算

有效能力 = 固定引擎可用工具 ∩ Runtime实装依赖 ∩ Agent配置 ∩ 本执行授权。
公共supportedInputs由公共配置/载体探测产生，Agent仅覆盖差异。技能依赖探测和实际安装状态仍按现有registry；不把安装SKILL.md等同于依赖可用。
声明输入可交付与“保证语义解析成功”分开：能传原文件不代表能解密/读取任意Office；逐文件保留交付与处理状态。

## 5. 文件系统、技能包与进程边界

### 5.1 不可信可写区与可信结果库必须分开

以现有 `SkillExecutionStore.directory = <workspaceFileRootDir>/skill-runs/<scopeDigest>/<executionId>` 为可信执行状态根；该根不挂给模型。

```text
<execution-root>/
  identity.json / command.json / result.json / receipt.json  # bridge私有
  effect-*.json / tool-*.json / selection.json               # bridge私有事实
  outputs/<outputId>              # 已冻结可信blob，模型不可写
  inputs/                         # 校验后只读挂入 /inputs
  scratch/                        # 模型工作区 → /workspace
  drafts/                         # 拟新增，模型产物区 → /outputs
```

注意：**沙箱的 `/outputs` 是宿主 `drafts/`，不是现有store的 `outputs/`**。否则模型可以在hash后改写可信blob，破坏恢复和commit。

请求/执行Home沿既有inspection-state绑定路径保留配置/会话，不再次复制execution-root；通过一份私有映射绑定Home、execution、thread和挂载。路径示例不再扩建第二套结果存储。

### 5.2 挂载与隔离

- `/runtime`、`/inputs`、获准`skills/<key>`只读；`/workspace`和草稿`/outputs`可写。
- 主Home下配置、auth、其他技能、浏览器秘密、其他任务都不挂载。
- 进程状态目录按引擎实际需要最小放行；有效配置和能力由bridge固定，引擎不能通过模型写配置获得更多MCP/网络。需要可写Home状态时，不把“文件只读”作为唯一权限依据。
- 复用bwrap namespace及固定工具链；本地命令无直接外网。模型服务、图片、浏览器访问走各自受控通道；不允许可执行包自行调用任意Provider绕过effect。
- 执行拥有明确进程组/生命周期记录；取消只处理本执行进程，不按进程名全局kill。重启核对PID/start身份，避免误杀PID复用后的进程。

### 5.3 引擎自动发现范围必须封闭

真实只读探测发现：系统Codex 0.164.0不仅发现CODEX_HOME中的技能，还发现cwd下`.agents/skills`，并自动具有system scope技能。此探测未运行模型，证明发现范围，未证明恶意技能已经执行。因而“只挂获准主Home包”不足以保证实际发现集合。

原生执行的thread cwd设为bridge控制的只读中性根（逻辑路径`/execution`），不设为用户附件目录或模型可写workspace；其祖先、引擎配置/插件及所有候选发现根按固定引擎实际机制治理。工作文件仍在`/workspace`，工具明确指定路径，不把可写目录当隐式受信项目根。若引擎仍扫描其他路径，使用实测支持的禁用/根配置或只读遮蔽；不能凭空假定有allowlist配置项。

初始化、技能刷新及恢复时核对实际发现清单：业务技能必须匹配授权路径/包hash；系统技能单独归入固定引擎受管清单，不能把其出现解释为安装/网络/付费授权。文件名为SKILL.md/AGENTS.md的附件和工作区生成文本只是资料，不能自动进入受信技能/开发者指令。发现越界项时阻止受影响执行并报告原因，不静默替换或自动授权。新原生路径统一使用隔离环境，包括无附件/纯TXT任务，不能沿旧hasNativeMedia分支落到主Home执行shell。

### 5.4 技能升级/停用

当前完整包在主Home `skills/<key>`；历史仅保留在途/可恢复安装引用。安装锁内暂存校验、写迁移意图、归档旧包、发布新包、更新索引、完成记录；启动恢复处理半完成切换，不读混合包。
逐包只读bind固定到执行Home，不随主Home升级重挂。跨文件系统迁移不假设rename原子，先按摘要验证复制候选、切换索引，最后在无引用时清理旧实体。
停用禁止新接纳；既有明确撤销通过broker/API检查阻止后续受保护调用。目录移除不是授权撤销机制。原生并发执行不能修改共享技能脚本。

## 6. app-server与工具接线

### 6.1 适配器模式

保留现有只读CHAT模式；新增“已授权原生执行”策略对象，包含固定可读/可写挂载、网络通道、工具集合、执行绑定与输出范围。不是全局替换approval或sandbox常量。

实施第一步锁定实际交付的Codex二进制及生成schema，验证initialize、thread/start/resume、turn/start、事件、interrupt、skills/list、MCP状态和工具调用。系统0.164.0的发现探测不能代替生产候选验证。使用真实支持字段，不以未知字段被忽略当成安全策略生效。

### 6.2 工具如何执行

- 沙箱文件/命令工具由app-server实际执行；bridge靠外层隔离、只读挂载和出口限制控制边界。**不是每次shell调用都会回调bridge审批**。
- 图片/网页/成果工具经已配置的受控MCP服务。服务入口预绑定执行，内部检查有效授权/lease，并持久化操作事实。
- MCP工具调用与app-server向客户端发出的approval/user-input请求不是同一种消息，不能把处理某个server request当成所有工具均可用。
- bridge只处理固定schema中需要客户端回答的请求；未获准动作拒绝对应请求，用户澄清不直接增加权限；不要在原生模式继续无差别拒绝所有server request。

### 6.3 事件规范化与展示

adapter把真实事件映射为内部类别：模型文字、工具开始/进度/完成、候选成果、提案、回合终态、需要用户输入、异常。内部类别不是新的app-server方法名。

按execution/thread/turn/item关联；文本用于展示，工具stdout是非可信内容，不能解析某个“SUCCESS”字符串自动提交成果。工具参数/日志中的凭据和页面秘密脱敏，不保存或展示模型隐含推理。

已有事件消费者新增无害进度字段可忽略，但不能忽略新的执行/完成语义。事件重放按持久工具调用ID去重；若引擎未提供可靠序号，不伪造严格的引擎事件序号，bridge自己的发送序号仅用于自身下游游标。

## 7. bridge如何收集结果：具体工具合同

### 7.1 `artifact.stage`：收集一次真实文件快照

拟新增工具输入（仅业务参数）：

```json
{
  "path": "/outputs/analysis.xlsx",
  "displayName": "分析结果.xlsx",
  "mediaTypeHint": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}
```

工具连接已绑定执行；path只允许草稿区文件，不接受任意host路径/URL。名称是显示建议，不参与宿主路径拼接；MIME hint不作为实际内容真实性依据。

执行算法：
1. 检查连接执行、授权、取消状态；禁止在最终清单冻结后新增/替换成果。
2. 以固定草稿根dirfd安全打开目标，拒绝绝对路径逃逸、`..`、软链接/magiclink、设备/FIFO/socket和目录；使用支持`openat2(RESOLVE_BENEATH/NO_SYMLINKS)`的固定小helper或等价逐层dirfd方案，不能用字符串startsWith或“realpath后再普通open”代替。
3. 从已打开FD流式复制到**bridge私有临时blob**并计算SHA-256/字节数，核对前后元信息；源在复制中变化则报告文件尚未稳定，允许模型关闭写入后重试。文件事件/inotify只作提示，不作为文件完成证明。
4. 对复制后的同一字节快照验证格式，fsync文件；分配稳定outputId并登记调用→output映射，将私有临时blob发布到可信outputs后fsync目录。失败临时文件仅清理本次拥有的对象。
5. 返回artifactRef/outputId、实际MIME、字节数、摘要、已快照状态。模型看到的是候选引用，不是后端已交付回执。

复制后模型再改草稿不会改变已冻结结果；要提交修改版必须stage一个新候选。重复同一调用使用已有映射，不能重读已经变动的源；模型主动再次stage视为新候选，可在本执行内对相同内容节约blob，但不同显示名称/选择意图仍独立记录。暂不跨Owner全局去重。

### 7.2 `result.propose`：指定最终成果集合

拟新增工具输入：

```json
{
  "summary": "已分析数据并生成结果。",
  "artifactRefs": ["artifact_generated_by_bridge"],
  "data": null
}
```

返回 `proposalId`、提案摘要、`pending-finalization`。只允许选择本执行已stage的引用，验证输出合同、多文件要求及dataSchema。模型不提供artifact hash、bytes、inputReceipts、manifestId或最终完成状态。

回合完成前可显式修订提案，旧提案留审计，不上传成正式结果。回合正常completed后，bridge核对无未决受保护工具、提案有效、授权/lease有效，冻结最后已接受提案。最终文字作为展示说明；不能从Markdown链接正则扫描宿主文件自动交付。

提案和回合终态也要可恢复：bridge持久绑定proposalRevision、所选artifact摘要集合、thread/turn及工具调用关闭事实，再核对引擎终态并冻结result。仅持久提案但终态事件丢失时须查询原回合；不能从模型最终一句话或候选文件存在推断completed。最终清单冻结与新候选接纳在同执行锁下互斥，收到晚到工具事件先核对既有调用，不覆盖已冻结清单。没有足够引擎终态证据时保留待核对，不新开回合重做付费步骤。

没有提案：纯文本任务若合同允许，bridge可将该回合最终文本作为文字结果；要求文件的任务不能静默空成果成功。可在同一执行继续明确的补交回合，但先查工具/effect状态，只收集已生成文件，不自动重跑外部操作。

### 7.3 部分成功、取消、失败

默认最终清单是原子交付集合，不能只上传其中成功文件就宣布全任务完成。允许部分交付时由用户意图/合同明确，记录缺失项；不能把失败操作从历史删除。
取消/失败回合的候选保留私有恢复证据，不自动发布为最终成果。用户后续明确要求取回部分结果时，通过获准恢复/交付路径使用已有快照，不重做Provider。

## 8. MIME、内容检查和输出元信息

校验目标是正确交付、防越界、防主动内容跨域，不是bridge理解每份表格业务。

| 类型 | 传输/成果检查 | 业务正确性验收 |
| --- | --- | --- |
| TXT/MD | 合法编码；允许合法零字节文件，不能以全格式非空统一拒绝 | 中文/范围读取/所需内容 |
| HTML | 合法文本，类型明确；预览隔离而非全盘删除用户代码 | 实际隔离浏览器加载 |
| CSV/JSON | 文本及对应结构；CSV公式按明确语义区分 | 重新读取核对字段/记录 |
| PNG/JPEG等 | 格式签名与必要解码，沿用图片行为 | 内容/尺寸/透明补边 |
| XLSX/DOCX | 验证OOXML必要结构，ZIP条目不越界；不执行宏/外部关系 | 相应库重开核对表格/段落 |
| PDF | 格式/必要解析，不执行主动内容 | 中文/页/提取/生成核对 |

对不可信压缩文档避免全量解压到任意目录；资源使用要实测并给具体错误，不无依据复制一套硬编码大小门槛。需要保护解压资源时按实测风险另写阈值依据，不承诺无限资源。

现有16MiB/非空规则、客户端字节长度校验、API multipart、网关、数据库/对象存储、下载端都要定向核对并协同修改；不能只删bridge一行。空TXT有效，空XLSX无效。当前store/上传Blob及API `file.getBytes()`有整文件内存化，通用大文件路径改为流式校验/存储与上传；仍复用既有multipart路由，不默认新建分片协议。精确实现限制如仍存在必须对用户明示，不静默截断。

现有结果摘要preimage只覆盖data、artifact outputId/hash/length、inputReceipts。显示文件名等新增元信息如参与安全/语义必须定义新的明确摘要版本或已绑定的元信息记录；不可偷偷加字段重算历史摘要。旧清单继续按原preimage校验。新旧摘要golden fixture在JS/Java双侧验证，不因JSON字段顺序或数字/字符串转换漂移。

## 9. bridge结果回传：复用现有精确HTTP链路

以下是已存在路由，公共信封/鉴权由现有transport适配；示例为业务层payload，不是可直接绕过鉴权调用的curl。

### 9.1 本地持久结果

bridge把已选择快照投影为现有result结构：executionId、snapshotDigest、data、artifacts及inputReceipts，先保存blob，再写result checkpoint（临时文件→fsync→rename→目录fsync）。输入交付回执由文件交付/载体层生成，不能让模型自证“已阅读”。“已交付”不等于“模型完整阅读全部内容”。

新原生runner必须扩展当前 `local-file`只允许`local-script`的回执规则，并在合同说明原生文件载体语义；不能假填`local-script`绕过校验。

同执行已经冻结结果时，不接受另一摘要覆盖。需要修改正式结果则走明确的新执行/修订，而不是修改旧manifest。

### 9.2 上传每个输出

```text
POST /internal/agent/tasks/{taskId}/runs/{runId}/conversation/outputs/{outputId}/content
multipart:
  file=<可信快照流>
  version=<lease version>
  token=<lease token>
  sha256=<快照SHA-256>
  byteLength=<十进制字符串>
```

bridge以受管Runtime身份调用，模型不能看到鉴权头/fence。后端再次校验身份、任务、lease/fence、长度、摘要；文件存储操作受现有执行锁协调。

现有stage回执含outputId、sha256、byteLength和STAGED/COMMITTED。bridge逐项匹配后才推进；一个文件失败则该文件待恢复，不能靠HTTP成功码认为全清单上传成功。同outputId同内容可重传/读回，异内容为冲突；不能换新ID制造重复成果。

已stage但未commit的是暂存，不向用户冒充正式可下载成果。

### 9.3 提交唯一结果清单

现有计算：

```text
preimage = { schemaVersion: 1, data,
             artifacts: [{ outputId, sha256, byteLength: number }], inputReceipts }
digest = SHA256(existingCanonicalJson(preimage))
manifestId = "manifest_" + digest
POST .../conversation/result-commits/{manifestId}
payload = { fence, snapshotSha256, data,
            artifacts: [{ outputId, sha256, byteLength: string }], inputReceipts }
```

数字/字符串转换沿现有明确投影，不能直接对wire字节hash替代preimage。artifact顺序冻结；语义变化必须升合同，不重排历史结果。

bridge核对回执：manifestId相等、state=RESULT_COMMITTED、resultSha256等于本地摘要、phase为ARCHIVING/COMPLETE；内部适配使用resultDigest，公共字段resultSha256，不能混用。

后端在事务/执行锁下确认全部输出存在且摘要一致、绑定有效、没有冲突结果，再持久结果并推进归档投影。网络响应不构成跨文件存储/数据库的天然分布式事务：先stage后commit、恢复读取和孤儿暂存清理解决中间状态，不宣称上传事务可自动回滚外部存储。

### 9.4 回执持久化与完成语义

bridge保存receipt（execution/snapshot/localResultDigest/manifestId/resultDigest/state/phase）后可释放模型进程与挂载；删除唯一成果blob前要核对后端持久状态/完整性及恢复需要。

RESULT_COMMITTED + ARCHIVING：结果已提交，业务投影仍在完成，页面不能声称所有成果可用。
COMPLETE及关联链状态完整：用户结果接口给出正式outputs，下载经用户ACL。bridge不能直接把宿主路径或Provider临时URL当下载地址。

现有 `ChatSkillResultController`在COMPLETE时检查step/link/request等事实；沿用该路径。浏览器/Web刷新只是读投影，断线重连读回事实，不依靠一条易丢的“完成”推送。

### 9.5 前端成果发现也必须改，不能只复用展示卡片

现有`hallSkillResults.js/skillResultReferences`仅从schemaVersion6、outcomeContractVersion4的ACTION_REQUEST及其child EXECUTE关系取executionId；新原生直接执行即使后端提交完成，也不会自动进入这条发现链。新接纳时由后端在现有request/step/execution关系中持久化原生执行引用，Web通过明确版本化的请求/步骤投影发现并查询结果；不得伪造模型ACTION_REQUEST或扫描“最新成果”猜归属。

复用原成果卡片/下载，不等于数据源和合同无需改动。同步修改现有结果查询对协议4的条件、Web精确字段解析与允许的增量字段、刷新/恢复路径；旧结果引用与摘要继续可读。当前Web允许MP4作为下载项，但不在inline MIME集合，带预览URL会被拒绝；增加视频播放必须同时修改服务端预览策略、Web校验/播放器与回归，不能仅输出previewUrl。

## 10. 结果状态与失败恢复表

下列本地阶段是说明/checkpoint设计，非要求新增一整套API状态枚举：

```text
ADMITTED → RUNNING → CANDIDATES → RESULT_FROZEN
         → OUTPUTS_STAGED → RESULT_COMMITTED → PROJECTED → RETIRABLE
```

持久事实优先于内存阶段；恢复必须核对snapshot、版本、工具状态和后端allowedWork。只能在明确允许时继续执行。

| 故障点 | 持久证据 | 恢复动作 | 禁止 |
| --- | --- | --- | --- |
| turn/start响应丢失 | 执行→thread/clientMessage绑定 | 查询原回合；未知则保留未知 | 新建回合重做任务 |
| 草稿写完未stage | 工作区及工具记录 | 核对后可补收集 | 当文件存在就已交付 |
| stage复制中崩溃 | 私有temp、未完成收集记录 | 清本次temp/重收稳定草稿 | 使用半文件 |
| blob完成但结果未冻结 | 候选及选择提案 | 恢复选择/核对终态 | 扫目录全部上传 |
| 一个输出上传响应丢失 | outputId/hash/本地blob | 同ID确认/重传同字节 | 新生成文件或新outputId绕过去 |
| commit响应丢失 | result.json/manifestId | POST原resume，核对服务端清单；必要时同manifest重交 | 调模型/Provider再生成 |
| commit完成、receipt未落盘 | 后端resultManifest | 验证清单后补本地receipt | 缺本地blob就误判任务未做 |
| ARCHIVING/投影失败 | 后端持久结果 | 修复/重试同一投影 | 重新stage并创建第二个执行 |
| Provider调用后断线 | effect START_RECORDED/UNKNOWN | 查询真实Provider事实；无法确认则待处理 | 盲重试付费操作 |
| lease过期/身份改变 | 原fence/身份 | 停止受保护新调用，resume重新确认权限 | 旧lease继续提交 |
| 取消与commit并发 | 后端执行锁下结果 | 按已持久先后读回真实状态 | 宣称已提交结果被撤回/外部操作被回滚 |

文件上传/查询等幂等恢复可以退避重试；“同根因同输入连续失败两次停止盲重试”不等于禁止已明确幂等的受控恢复，但不得对不确定副作用重复invoke。网络错误需分类；不因任意SLO中止模型流。

## 11. 通用工具调用与副作用机制（C3）

### 11.1 统一受控调用入口与多步effect

每个工具调用记录执行、工具名/版本、引擎item/tool call关联、授权摘要、输入摘要、开始/结果及产物引用；秘密字段不入日志。bridge分配持久操作ID，不把用户提示hash当操作身份。

多步执行允许多次生图：每次明确新调用获得新操作ID；同一传输重送映射原ID。当前image runner中固定`generate` effectId不能直接用于整个原生多步任务，须按持久工具步骤命名。参数发生变化而仍使用原ID必须冲突，不能覆盖旧收费事实。

现有SkillEffects保留“服务端start→本地start落盘→外部调用→结果blob落盘→report确认”顺序。恢复成功effect只读回/补报；未知effect停止依赖该结果的步骤。模型声称“再试一次”不能自动把未知付费调用包装为新ID。

### 11.2 原生多步恢复不能沿用旧runner的整体EXECUTE判定

已核对API现行resume：有任何effect且无最终manifest时，只给QUERY_EFFECT/RECOVER_LOCAL_RESULT，即使该effect已SUCCEEDED也不再给EXECUTE。现有SkillEffects.mayStart据此禁止新effect。这适合原单runner恢复，却会阻塞原生任务“完成图片后断线，再继续配音/合成”。

原生合同新增明确的续执行授权语义（具体wire枚举随合同固定）：在同execution/fence下恢复已确认步骤，允许尚未开始且仍获准的新步骤，禁止重放已有/未知操作。持久操作ID独立于模型turn/itemId，多个引擎重连ID可关联同一逻辑操作；不能仅以新callId认定用户要再付费一次。接纳新调用前向恢复上下文提供已有operationRef及其状态；UNKNOWN的替代调用不能用换ID绕过，确需重新操作须有明确处理决定。

错误分类区分未发送前校验失败、远端明确拒绝、调用后结果未知；当前invoke将异常统一UNKNOWN，不能直接当通用语义复用。任务必需外部操作UNKNOWN或仍在执行时不能报告完整成功。已确定失败的非必需探索步骤可继续替代方案，保留失败记录，并在最终清单记录相关操作依赖/未交付项；当前后端“所有effects必须SUCCEEDED”的commit校验须按新原生语义扩展，不删除旧v4校验或把FAILED/UNKNOWN改写为成功。

### 11.3 通用工具与服务机制（C3）

C3仅实现执行绑定、工具声明/版本、凭据引用、授权检查和持久操作恢复；图片HTTP编码、视频参数、Office算法不进入核心。工具是固定实现或已授权执行脚本的受控入口，不是模型自注册一个工具就获得权限。
通用外部HTTP调用属于E4，通过C3持有凭据/记录effect；模型可以编写服务请求组织脚本，但不能读取秘密或绕过出口。新增服务不一律新增bridge分支。依赖声明只描述需要，不自动授权网络、收费或安装程序。

## 12. 扩展实现入口

图片、文档和浏览器的原详细约束已迁入扩展详设，并新增通用HTTP、本地视频及技能提取：`/home/isp/wsps/cyf/specs/juyiting-skill-execution/native-execution-extensions-20261028.md`。
本文§8保留通用成果安全/格式规则；具体库、Provider、浏览器步骤归扩展。扩展可以和核心同仓发布，逻辑依赖不得反向变成“核心要有视频技能才能运行”。

## 13. 持久化、并发、清理与观测

单execution只有一个有效提交者，由现有lease/fence及执行锁控制；不能仅靠进程内Map防并发。多个Agent/执行可以并行，不共享可写工作区和tool session。文件stage/最终提案通过本执行串行化点协调；final freeze后拒绝新候选，不截断仍在进行的工具操作假装完成。

保留已有store，拟新增工具调用映射、候选索引和提案checkpoint；不另建权威业务账本。后端仅在现有执行/绑定合同中增加必要集合/元信息；是否需DDL在定位现有存储后固定迁移，不凭方案臆造已存在表。新字段不修改历史hash原文。

清理分三类：
1. 模型进程/挂载：终态或有效取消后只释放本执行。
2. scratch/drafts/输入副本：结果/恢复证据足够且无活动引用后清理；保留未知effect必需资料。
3. 可信blob/旧技能：后端持久成果已核对、无恢复引用再回收；旧版本有引用不能删除。删除意图/结果可恢复，孤儿先核对事实，不按年龄全删。

记录：执行/工具ID、模型与引擎版本、包摘要、输入交付状态、产物hash、upload/commit/投影状态、实际耗时和错误。绝不记录Key/完整Cookie/密码，不把敏感原文全量复制日志。性能观测不添加任意拒绝请求阈值。

### 13.1 从首次执行就保留最小可提取证据（C5）

记录应在执行开始建立，不等点击“提取技能”才找已删除文件。每次可观测的脚本运行关联：工具调用/命令身份、脚本内容摘要和私有版本快照、工具链版本、获准输入引用、退出/失败事实和所产成果。会话可跨多个执行，来源通过精确执行/修订引用串联，不共享未绑定可写工作区。

shell inline命令与生成脚本也纳入可观测快照；脚本/子进程在运行时动态修改、代码来源无法确定或引擎未暴露足够事件时，明确标记证据不完整，不能声称捕获了实际执行的全部代码。必要时在受控命令入口捕获执行前版本并与运行后变化关联，不靠事后只扫最终文件。C5不要求无限制录制终端、浏览器密码或模型隐含推理。

提取所需源码包与临时scratch分开：在已授权任务留存范围内，将最小脚本版本/依赖/成功成果关联保存为私有资料，绑定Owner和ACL；不得把全部工作区当审计包长期保存。凭据注入在C3，不进入脚本；发现硬编码秘密时阻止其进入可复用/分享包，并将相关源证据按敏感资料规则处理。脱敏派生件有自己的hash，不能冒充原脚本hash。

后端提供来源可用性和保留策略，保留期限沿既有资料规则/明确设置，不在此臆定永久或固定天数。未实现持久来源归档前，不能在UI承诺任意历史会话都可提取；只显示仍可访问的来源。历史记录缺源时允许生成标注为重建/待验证的候选，但不能冒充从成功脚本直接提取。

### 13.2 回收条件补充

删除scratch前，若该执行在获准可提取留存范围内，先确认最小来源包已持久化或明确标记留存失败并交由既有保留策略处理；不能一边宣称可提取一边清掉唯一脚本。来源包删除与用户数据删除/权限撤销一致；提取中的来源引用在本任务内保护，完成后释放，不长期阻止全部目录清理。

## 14. 实现清单与测试入口

| 工作项 | 入口/交付 | 最早定向验证 |
| --- | --- | --- |
| 原生模式/真实工具 | app-server-adapter、agent-client、通用执行生命周期 | skills为空的真实回合写TXT；工具事件、取消/unknown |
| 技能视图/授权 | installer、registry、profile、现有TaskSkillBinding | 单技能→集合协商、未授权包不可见/不可调用、升级恢复 |
| artifact与提案 | execution-store、新受控成果工具 | 路径/符号链接/并发写、snapshot不被模型修改、空TXT、多文件 |
| stage/commit | skill-conversation、executor、API既有controller/service | 丢回执/重复上传/冲突摘要/lease过期/ARCHIVING |
| 通用文件载体 | ChatMaterialsInputContract、typed-inspection载体、输入回执 | TXT不丢、图片原生保留、Office路径可读、失败材料明确 |
| MIME/内存路径 | conversation-native、API文件存储/下载、Web | HTML/XLSX/DOCX/PDF、流式文件、预览隔离和名称 |
| 图片 | image-provider复用、原生技能/MCP、effects | 生改读、透明尺寸、两次有意生成、重送不重复收费 |
| 浏览器 | 固定工具链、MCP/browser服务、出口、状态存储 | 自有站点登录/上传/下载/授权提交、隔离/未知恢复 |
| 前端 | 既有执行详情、成果卡片/下载、结果查询 | 模型结束但上传失败不显示完成；刷新后结果一致 |
| 来源/提取 | C5留存、E6来源快照/候选、既有技能管理 | 无技能任务→脚本证据→候选→验证→安装→换参数复用；缺证据不伪补 |

复用现有API `SkillExecutionServiceTest`、`SkillExecutionMapperRealTransactionTest`、`ConversationLeaseWireHttpTest`、`SkillNativeResultMySqlTest`等对应入口；新增fixture前核对实际selector，不复制无关旧任务ID。Runtime在现有node测试体系加定向测试，不另建大runner。

必测故障注入：每个持久步骤前后crash、上传回执丢失、commit已成功响应丢失、effect已调用响应丢失、模型工具重复事件、取消与提交竞态、身份变更、目录替换、磁盘写失败、投影失败、重启恢复。

正式重型测试/构建/打包走既有Flow，各Run总计<=600秒，不能拆Run规避；真实模型/Provider用获授权独立测试输入，不重放事项538。完成证据分别包含工具trace、真实文件重开/下载、后端commit与投影事实，不只截图“成功”。

## 15. 实施前必须固定但不得假装已验证的参数

设计已选定：只读技能挂载、隔离草稿/可信blob、显式stage/propose、既有HTTP结果提交、受控图片/浏览器MCP、现有管理系统复用。

以下在切片A/各组件实施时取得真实值，记录到同一handoff，不要求再开一轮泛化架构讨论：
- 交付Codex版本、实际schema、MCP传输/配置字段和工具事件形态；不沿用未经验证的系统版本。
- 现有工具链中Python/Office/Chromium/Playwright精确版本、依赖锁/镜像摘要、sandbox内可达路径。
- 当前API/Web/网关格式/大小/空文件限制与所需协同修改、流式存储适配能力。
- 新原生执行合同（含空技能集合）、授权技能集合、输出元信息与提取来源/候选的实际协议版本/DTO；旧版本拒绝未知执行语义而兼容无害字段。
- 安全文件打开helper与最终进程权限实测；跨重启包索引/挂载/回收验证。

这些是具体实现验证项，不是已上线能力。仅文档检查通过不得把本详设标成原生执行验收通过。
