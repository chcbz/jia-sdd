# 聚义厅多媒体协作：待实施任务清单

2026-10-04。对应 [待实施增量详设](implementation-design-20261004.md)；[完整产品目标](design.md)；[最新版交互原型](prototypes/adjusted/index.html)；[界面变化标注](prototypes/adjusted/annotations/index.html)。

**这是一份接手清单，不是把完整详设全部重做。2026-10-04 用户已授权恢复开发，并要求按版本节奏落实；当前源码进度见 [分版本开发回执](implementation-progress-20261004.md)。未完成的候选不提前发布。** 历史计划已移至 [历史存档](tasks-history-before-20261004.md)，不要重新执行其中已完成的 F0/B1 等工作包。

## 0. 最新优先原则

**能用、易用优先；只补缺口，不扩建系统。** 执行时合为三个工作包：①页面与输入简化（T01–T04）；②成果展示与验收接线（T05–T06）；③边做边联调、正常发布（T07–T09）。编号只用于追踪，不是九道串行门禁。

- 撤销上一版预设的新交付集合查询 API、集合版本及独立状态机。复用现有结果元数据、`selectedOutputs` 和验收引擎；仅补实际缺少的来源/替换关联和纯文字适配。
- 不新增审批、Reviewer、兼容层、独立验证项目或流水线；不要求先完整审计/全量回归再动手。
- 必需检查限于本次改动、已证实的问题和实际用户闭环；沿用已有权限、去重和正式发布要求，不新增无依据门禁。
- 不扩大页面、媒体格式、Agent 能力或部署范围。支持的格式复用预览，其余下载；功能缺陷按影响修，不拿原型代替真实功能。

## 0.1 2026-10-05 用户收口：旧议事和媒体测试数据不适配

用户明确旧议事和媒体均为测试数据，要求删除、不做适配。**取消 legacy EXECUTE 原媒体起点适配、历史关联补写和旧数据迁移；不再将这些工作列为开发或发布前置。** 历史回执保留当时的验证事实，涉及旧起点的待办由本条覆盖。

- 清理对象是用户指定环境与范围内的旧议事/关联媒体测试数据，而非代码测试fixtures、Git源码、测试回执或全站所有资料。
- 实际删除前先明确目标环境和边界、列出关联记录/媒体；不因“都是测试数据”推断数据库、账号或全部文件可清空。保留新联调数据、非目标账号/任务及非目标资料；共享媒体先核对引用，不递归清空存储目录。
- 用户随后明确 `chcbz` 账号范围；已在当前线上 `jia` 库限定清理其 109 条历史聚义厅议事、370 条消息及关联记录，删除 3 个专属媒体对象。保留空墓碑拒绝晚到写入，私有恢复备份已校验；普通聊天、原始上传及独立正式任务交付保留。搜索索引服务不可连接，残留未核验，不宣称所有存储已彻底清空。见最新开发回执及 [清理摘要](implementation-evidence-20261004/chcbz-history-cleanup-20261005/manifest.json)。
- 开发主线转入当前新流程的真实 Agent / Web / API / Client 联调及既有正常发布；新流程发现具体功能缺口才补最小修复，不继续扩建旧数据兼容。

## 1. 核对基线与状态含义

上一轮通过 Git 对象只读核对下列候选，并用 `ls-remote` 核对同名远端特性分支；不是根工作区的旧 api/web checkout，也不是线上版本证明。

| 仓库 | 候选分支 | 核对 SHA |
|---|---|---|
| Web | codex/mmd-unified-materials-web-20261003 | 12edde24a5eff19aa097e92359d787e73ec6129c |
| API | codex/mmd-unified-materials-api-20261003 | 75357f13502ed0afc641200dc8601b389d6516dd |
| Client | codex/mmd-unified-materials-client-20261003 | 777f26f39722a8f85f04b5b89f12e3c364c1a9df |
| SDD / 原型 | codex/juyiting-multimedia-deliberation | 本次修订基于 28b37fe9；原型交互来自 d8ea407a |

- **确定需调整**：候选源码与已确认原型存在可定位差异。
- **确定需补齐**：现有合同/校验不能满足该场景，不等于相关模块全无实现。
- **已有基础，待联调验证**：有源码/历史测试，不能重列为从零开发；失败后才拆最小修复项。
- **待发布验收**：缺最终集成版本与真实业务闭环证据，不等于未写代码。
- 本表是日期绑定的需求状态，不登记运行 Owner/领取状态；实际执行仍使用唯一 runtime ledger。

## 2. 不再从零开发的已有基础

| 已有基础 | 本轮定位 / 既有证据 | 接手方式 |
|---|---|---|
| 通用资料入口 | Web `HallMaterialPicker.vue` 已有“添加资料（可选）”、预览、移除、版本引用 | 复用，收简默认 UI；不要再做一个参考图选择器 |
| 点将与自动议事 | Web `useHallPointAndStart.js`；API point-and-deliberate 合同与上下文 | 补页面接线、验重复/恢复，不建第二条点将流程 |
| 密议 | `AgentPanel.vue` 明确保留“与这位好汉密议”；独立面板存在 | 保留并验证隔离，不当新模块重建 |
| CHAT / 按需动作 / 续办 | API `ChatActionFinalService`、动作/混合资料链路；Client 候选 | 真实配对验证；不照旧 tasks 的“未开始”重写 |
| 媒体与保存 | `HallMessageMedia.vue`、`HallMessageParts.vue`、`useHallConversationArchive.js`、文字选区组件 | 复用鉴权读取/幂等保存；补失败的格式与接线 |
| 正式验收引擎 | `useHallBountyFinalization.js`、API `ChatSelectedOutputFinalizationService` 与 Agent 正式交付服务 | 保留事务/幂等/恢复；改交付来源和用户入口 |
| 已有检查 | source-evidence 中跨 wire API45/Client35、隔离 MySQL19；API Flow108 历史云测及制品 | 只覆盖各自明确范围，不当全产品通过，也不无条件重复 |

历史证据见 [ordinary-request-source-evidence.json](ordinary-request-source-evidence.json)。本轮未查询流水线实时状态：其中 Web165 的 RUNNING 是历史记录，不是当前状态。API108 记录 2592 tests / 0 fail / 101 skipped，未部署；不得将 skipped 或制品成功写成完整业务验收。

## 3. 真正待实施的任务

T01–T04已形成本轮配套Web/API源码候选（Web f927f344、API 7a9418c3），定向Web311/API50项通过；尚未整体联调/上线/用户验收。T05已补精确改稿关联子增量（Web b1f807c/API 0ff0322b，Web208/API55项定向测试通过），随后已补媒体事项验收接线（Web f0f4d1fc，10组235项通过），仅支持单一明确manifest及精确改稿链；随后已补纯文字可信来源与Agent内部正式交付适配（API a847c3d4，9组112项通过）；之后已接齐文字HTTP/原items持久恢复（API 88243a31，组合源码124项及隔离MySQL24项通过）；随后补齐前端文字验收请求/原键恢复（Web 84646060，4组68项及本地构建通过）；随后接通明确文字标记与事项页展示/验收（API732f7b7f、Clientf7d6d395、Web31154e03，API87/Client34/Web123项通过）；随后补齐服务端marker校验与单根文字链APPEND/REPLACE/RESET（API6b794b0a、Client213f461、Web0a4abbbe，API109/Client37/Web130项通过）；随后接通单根文字经多轮澄清传播及即时问题CAS/原键恢复（APId0a3f80a、Client79bad1e、Web1fb1fa4c，API116/Client44/Web133项通过）；随后补齐单明确媒体清单/精确改稿链的自然议事原源（API01039abb、Cliente41246c、Web5b13014，API45/Client45/Web142项及lint/build通过，2026-10-05）；随后接通较早仍保留文字的精确改稿目标与后来追加项保留（API905adcf6、Clientb5fa735、Webf60cfbf，API120/Client47/Web148项及lint/build通过，2026-10-05）；随后接通“文字为父→明确新EXECUTE批次”的APPEND/RESET与混合验收原键恢复（APIccdf2ce8、Clientb6ca429、Webfd5f7e8，API131/Client49/Web156项及lint/build通过，2026-10-05）；随后接通已完成媒体因果父、混合保留目标与较早文字改稿及显式/仅附件议事basis（API0e70e2f0、Clientb42176c、Webc075303，API137/Client51/Web164项及lint/build通过，2026-10-05）；随后接通混合单项媒体replaces改稿、其他项保留与原键验收恢复（API329d44fd、Clientb8d74b1、Webbb64c81，API140/Client52/Web169项及lint/build通过，2026-10-05）；用户于2026-10-05取消旧议事/媒体测试数据适配，legacy起点不再开发；当前新流程进入真实联调，T05/T06尚未实际业务验收，T07–T09未完成。详见上述回执，源码/云测/上线/用户验收分别记录。Owner为职责建议；本表不登记运行领取状态。

| ID / 优先级 | 状态与工作 | 最小范围 / 建议职责 | 依赖 | 完成条件 |
|---|---|---|---|---|
| T01 / P1 | **确定需调整**：事项三入口合为“提出需求”；资料默认不要求选版本 | Web：BountyPanel、HallDraftEditor、HallOverview、HallMaterialPicker | 无 | 无资料能提交；混合资料可预览/移除；一次提交，不另加工程确认；原任务/交办权限不混用 |
| T02 / P1 | **需补页面接线并验证**：点将册承接待点将事项，只显示好汉；保留密议 | Web：AgentPanel、JuyiHall、现有 point-and-start composable | T01 接口可独立复用 | 显式 targetAgentId；点将后唯一会话/首条；密议不消费待点将事项；无事项不显示点将执行 |
| T03 / P1 | **确定需调整**：议事去顶部资料/百宝箱快捷入口；输入区仅“＋/发送” | Web：ChatPanel、HallChatComposer、HallVoiceControls 及父级接线 | 无；同文件由一个 Owner 完成 | 资料/语音/设置在＋内；返回事项详情验收；保留语音行为与正确图标；桌面/手机不遮挡 |
| T04 / P1 | **源码已补齐，待联调/上线**：同会话仅发送附件，不要求捏造正文 | Web Composer / hallTypedDeliberation；API discussion 校验/上下文；Client 按需读取 | 与 T03 共用接线；详设 D3 | 双空拒绝；正文空且有合法资料可发；有权限快照、原用户消息、去重/澄清回归 |
| T05 / P1 | **实施中，部分完成**：已补精确改稿关联、单批次媒体清单及文字HTTP/原条目/前端原键恢复；明确文字标记、事项页验收、单根文字链追加/替换/重置及多轮澄清原来源传播及单明确媒体链自然原源及较早仍保留文字改稿已接齐；已接文字为父→明确新执行批次APPEND/RESET；已接已完成媒体因果父/混合目标及较早文字改稿；已接混合单项媒体改稿；旧测试数据起点适配已取消，转新流程真实联调，不建独立集合系统 | 复用现有结果元数据、文本快照和 finalization；详设 D4 | 与 T01–T04 可并行 | 改一项保留其他项；刷新可恢复；纯文字可验收、不伪造工具 run |
| T06 / P1 | **实施中，部分完成**：事项媒体验收已去多选并返回原会话；文字事项页、单根文字链、澄清后原成果及较早文字改稿保留追加项已接齐；文字为父→新执行批次图文APPEND/RESET已接齐；已完成媒体因果父/混合目标及较早文字改稿已接齐；单项媒体改稿已接齐；旧测试数据起点适配已取消，转新流程真实验收 | Web BountyExecutionOutputs / 事项详情；复用 finalization | T05 | 只读成果清单、预览下载、确认验收/继续修改；提交用户所见精确内容，不偷换新稿；保存不是前置 |
| T07 / 随实施 | **已有基础，待联调验证**：自动回答/澄清/按需工具，多轮与真实媒体 | API / Client / Web 接口 Owner；不先重写 | T02、T04；T05 可并行验证 | 真实 Agent 处理无资料及混合资料；可读取真实图片/音频/文件；媒体晚到可恢复；故障只补实际缺口 |
| T08 / 随实施 | **已有基础，待联调验证**：文字/媒体可选保存、恢复与隔离 | API / Web；现有 archive/asset/恢复入口 | T04、T07 | 保存后空间可读同字节；刷新不重生成；跨账号/任务拒绝；密议隔离；只补失败用例 |
| T09 / P1 | **配套源码及正式CI/制品已核验，待发布与真实验收**：API109/Web167及精确候选已收敛；实际运行版本与浏览器闭环仍未完成 | 集成职责；仅改动组件走既有 Flow | 功能可用及相关检查通过，不等额外全矩阵验证 | exact commit/tree、正式云测、同 Run 制品、运行版本及线上场景一一对应；无虚报 |

T05 不能用“自动勾选全部历史成果”替代，但不必为它新建服务或版本体系。T07/T08 随实际闭环核对，沿用有效证据，不作为两个必须先做完的独立项目。

## 4. 最短执行顺序

1. Web 在原组件内完成入口、点将接线和＋输入区；API 只补附件校验与成果来源的实际缺口。相同文件一个 Owner，独立路径可并行，不增加全局串行队列。
2. 新流程成果展示/验收源码增量已形成，直接边操作真实主流程边修实际问题；不继续旧测试数据适配，不提前铺新集合框架。
3. 在同次联调中覆盖 T07/T08；正式测试/构建/发布复用改动组件的既有 Flow，发布后核对实际功能。无需先跑 CI-only 再重复生产构建。

只读核对候选和现有证据即可开始接手，不反复重查整个工程。资源互斥等待、不抢占；仅相关真实失败或授权边界阻止对应操作。纯文档无需构建。

## 5. 按改动选测试，不新增验证工程

以下是可复用的测试定位，不要求逐个改写、逐条执行；正式流水线已有测试照常运行。只为实际改动补最小用例，未变更且适用的已有证据复用。

| 任务 | 相关既有测试定位（Web tests / API 测试类） |
|---|---|
| T01/T02 | juyiting-requirement-materials-intake、juyiting-point-and-start、juyiting-hosted-point-flow |
| T03/T04 | juyiting-voice-conversation、juyiting-conversation-material-links、juyiting-typed-deliberation-wire / interaction；ChatTypedDeliberationServiceTest |
| T05/T06 | juyiting-bounty-finalization、juyiting-finalization-task-refresh；AgentTaskSelectedOutputFinalizationControllerTest、ChatSelectedOutputFinalizationService 相关测试；仅补明确替换和纯文字验收；涉及事务/权限改动才补相关回归 |
| T07/T08 | juyiting-multimedia-parts、juyiting-conversation-archive、juyiting-bounty-output-recovery；ChatActionContinuationTest / TransactionTest、ChatMixedMaterialWireTest |
| T09 | [最小验收与发布](implementation-design-20261004.md#d7-最小验收与发布)；design.md N01–N12 为覆盖参考，不要求逐项重复全量实测 |

交付时合并记录一次：提交、改动、实际测试/发布结果及未完成事项；不要求九项各出一套独立证据包。只更新已实际满足的状态；源码完成、云测通过、上线和用户验收分别记录。

**给接手 Agent：** 从本清单而不是历史 tasks 开始；从已定位候选实施最小差异，T07–T08 随真实闭环验证并修复，不先扩建系统或检查体系。遵循增量详设和现状原型，不大改、不加受控请求/参考图专用入口、不恢复验收多选；不要更改暂停状态或运行流水线，除非接手任务已取得相应执行授权。


### 2026-10-05 21:36 CST 接手状态补充

当前配套候选API329d44fd /Clientb8d74b1 /Webf6b81b4均已推develop并读回；API109 SUCCESS、Web167 SUCCESS，同Run制品及精确源SHA/tree已校验（API101 skipped；Web3146通过/2pending/0失败）。来源见 [最新回执](implementation-evidence-20261004/integration-cloud-ci-20261005/manifest.json)。T01–T06现有源码和定向测试不等于真实业务通过，T05–T09剩余仍以新流程真实运行/保存/恢复/隔离及发布验收为准。发布和真实模型/工具调用授权已向用户询问，尚未执行；不为相同候选额外重复CI-only，不恢复旧数据适配，不将CI-only制品手工部署冒充既有Flow发布。


### 2026-10-05 23:30 CST 三端发布接续

Agent已实装Client4e70c4f，两实例payload/config已核验；主机发布脚本forward-only及现有备份别名问题已修复，26回归PASS；零点调度分页18回归PASS。API5260799现有deploy已恢复，明确新版失败向前修复、不自动降级；等待2026-10-06 00:00既有调度，未创建最终Run。Web仍CI-only且仅API健康后发布。真实业务验收NOT_RUN，T05–T09不标完成。详见 [接续说明](runtime-release-20261005.md) 与 [实际回执](implementation-evidence-20261004/runtime-release-20261005/manifest.json)。用户已授权发布及既有预算内真实调用；IAB已打开chcbz登录页待用户登录，无需传递密码。


### 2026-10-05 23:47 CST 立即发布覆盖

用户明确取消零点等待。API既有Flow Run110已创建，实际检出329d44fd已只读核对并绑定发布intent，无重复Start；正在云测，尚未上线。两个timer临时暂停防重复，本次三端发布完结后恢复。API完整健康后立即发布Web。详见 [接续说明](runtime-release-20261005.md)，T05–T09及业务验收状态不变。


### 2026-10-06 00:40 CST 立即发布实际进展

Agent已完成。API110新JAR现健康运行，finalization确切一次性迁移已验证，但Flow最终FAIL：发布后schema runner仍拒绝报告目录，两表not_attempted。保留失败状态，不重放110schema。修复F06/E05 catalog及E05 hash pin，60离线回归通过并CAS安装。新API5260799/111正式测试部署正在运行，Start UNKNOWN已只读核对唯一Run/真实检出并绑定intent，未重发。Web仍API-first待111最终核验后立即发布，T05–T09 NOT_RUN。监控已恢复，两个防重timer暂未恢复。详见 [当前接续](runtime-release-20261005.md)。


### 主机北京时间2026-10-06 01:04 最新接续

API111 CI成功/JAR健康，但F06旧SQL pin不匹配新版owner-fenced资源，Flow FAIL；保留110/111报告，不重放schema。按当前JAR资源及已有mandatory-owner schema更新严格门禁，62回归通过；真实JAR/MySQL catalog只读equivalent及负控制拒绝已验证，未执行DDL，01:00 CAS安装。最新正式API112运行（CI529282011/deploy529282012），唯一Run/checkout/time/config只读reconcile已完成并绑定intent。Web仍API-first，T05–T09 NOT_RUN；监控健康，timer最后恢复。详见 [权威接续](runtime-release-20261005.md)。


### 主机北京时间2026-10-06 01:17 / UTC2026-10-05 17:17 正式API完成

API5260799/112最终SUCCESS，CI/唯一主机/同Run制品/JAR/record/approval/真实健康均核验，F06 PASS existing_equivalent，E05 not_admitted未调用。Web原deploy已一次恢复，Web4403172/168正式CI发布链运行，Start UNKNOWN只读核对唯一168/checkout marker/CI_SHA/time/config并写intent，没有重发。新同Run Web制品和线上dist字节待核验，T05–T09 NOT_RUN。Agent已完成；监控恢复，Web正式完成后恢复两个timer。见 [权威接续](runtime-release-20261005.md)。
