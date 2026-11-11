# 剩余缺陷修复与真实验收记录

核对时间：2026-10-20 10:29 CST。Owner chat-stop-main，CHAT-STOP-FIX-20261019，单Agent。

**结论：已修复并上线本页列明的异常，文字主流程和真实停止已通过；不是整个优化方案全量验收完成。** 不将正式Flow通过、文字流程通过或新版本安装等同于全页面/媒体/历史执行闭环。此前截止未达成事实不改写。

## 固定源码与正式发布

| 组件 | 最终部署 | 源码 | 正式验证/发布 |
|---|---|---|---|
| API | 1.16.17 | `0620837a97f48e01a613a436f33b06ea862f043e`；tree `b63aa2910dfaf925b4bace23b893422f8d4223a8` | Flow5260799/193 SUCCESS，2594通过/122跳过；同Run制品安装已核验 |
| Web | 1.16.20 | `f184d9d371d676af250fbdfbc21e773d774c480b`；tree `e9292b7d666ff1c0cf068af3c55599d57ecab69c` | Flow4403172/252 SUCCESS，3100通过/2pending，366安装文件全匹配，公网入口与议事JS/CSS匹配 |
| Runtime | runtime-ui-workflow-1.16.17 | `2f0518de38eef3b33dc6498865c35f266133a7e6` | 既有安装/激活路径；66payload匹配；该批13队列定向通过/192跳过；先前提示合同21通过 |

- API193归档SHA256：`5f7b5053c9ff782ab33e15c6fe47b4481abb323f0cf4a8730511b056e338c84c`；JAR `2991a56bc29db147e865c74fd50c8ef143051eee0aea4db4c125dac986ff6cea`。实际/proc PID3427255使用canonical实体路径，旧pidfile不作证据。
- **API补充正式CI194**：同0620837源码，2602通过/122跳过，SensitiveResponseBodyAdviceTest全部8通过（含新增2）。194无部署阶段，不把补充测试冒充193原本覆盖；实际线上JAR仍来自193。
- Web252归档SHA256：`75dc2758a6da089f3fc1d799dcf6383bcad1366a91423aba9f4129f04936b4cd`。
- API/Web临时Flow配置均已冲突检查并恢复，readback成功。没有本机构建生产制品、DDL、手改DB或取消别人的Run。
- 详细结构化回执见本目录`api193-*`、`api194-*`、`web250-*`、`web251-*`、`web252-*`。定向本机测试不算正式验收。

## 修复原因与边界

1. **流式停止409**：持续delta同时推进stateVersion；前端曾只推进version、不推进lastDeltaSeq，导致587/0错误配对。前端同步投影两个字段；后端仅对“版本差=delta差”的纯输出推进允许停止，保留原身份/锁/CAS/终态幂等。
2. **停止后半截气泡仍在生成**：清理同turn CANCELLED/FAILED的streaming并保留当次半截文字，标为未完成，不波及其他Agent。
3. **刷新历史取消会话重新出现生成气泡**：activeRequest已取消，但另一个旧request的delta仍能进入消息reducer。非当前request的历史delta不再生成实时气泡；已保存历史最终消息继续展示。没有新增监听/轮询。
4. **验收已成功但输入框仍显示**：事项列表副本滞后。当前taskId精确匹配的权威reviewContext COMPLETED即刻关闭composer，不等待列表刷新，不锁其他事项。
5. **确定模型契约错误未收口**：白名单确定拒绝在同会话/轮次fence内落FAILED，事务后发布原事件；网络未知不伪造FAILED。
6. **workspace协议拒绝**：实际HTTP响应脱敏反射补了三个null reply字段，事件8字段违反5字段严格合同。仅ProtocolMessage省略correlationId/code/msg空值，保留data:null与嵌套脱敏。Runtime不放宽解析；修复后确已通过该层，但下层D06上下文问题仍未解决。
7. **超长URI审计失败**：100字符字段改写入28码点前缀+SHA256摘要；无DDL。真实115字符typed-outcome路径在按主键倒序5000条的只读检查中命中3条摘要。
8. **模型误称无法提交**：明确平台会根据有效typed outcome提交成果，不让模型捏造提交工具或先于回执宣布成功。本轮实际两组文字提交/修改未再出现该误述；不能保证所有模型输出永不出错。

## 真实浏览器验收

均为生产https://kit.chaoyoufan.cn，本任务自有CDP浏览器，吴用，真实页面操作；仅对准确路径的一次性测试写入放行。不是直接API写入替代UI。截图包含自有测试内容。

### 475：停止、继续、自然修改、验收

- Web250，PC1440×1000：生成中第一次点停止，POST438/437；返回200、CANCELLED441/439。网络期间仍有delta推进，未要求用户连点。
- 同事项移动390×844：再次生成中第一次点停止，POST439/438；返回200、CANCELLED442/440。
- 两端均保留半截内容/已停止（未完成），停止控件消失，仍可继续发消息。
- 随后发送短通知→成果自动提交→自然修改19点为20点→预览确为20点→真实确认验收200 COMMITTED、task COMPLETED(v6)、delivery ACCEPTED(v1)。详见`live-receipts.json`。
- Web251补上验收后composer隐藏；刷新时发现历史delta重放问题，未掩盖该失败。
- **Web252最终回归**：重新加载公网`JuyiHallEntry-DqChFqJT.js`，重进475；PC/移动均0个streaming气泡、0个议事composer，持久最终文字仍可见。截图`mobile475-restored-no-ghost-stream.png`、`pc475-restored-readonly.png`。

### 476：全新移动文字流程

- Web251，390×844，开始办事保存正式事项476（待点将），推荐吴用→用户点击交给吴用→建立会话1760458006515→30字通知直接提交。
- 议事自然修改日期10月21日→10月22日；后续真实文字成果及预览都为22日20点，不需要“引用修改”按钮。
- 点击工具栏验收图标→预览→确认验收，200 COMMITTED/COMPLETED/ACCEPTED；**无需刷新议事composer即刻消失**。
- 此测试在251完成，252只增加非当前历史delta隔离；不把476过程虚报为从252开始。相关回执`mobile476-receipts.json`，截图`mobile476-result-text.png`、`mobile476-accepted-readonly.png`。

## 尚未闭环/不能标通过

| 项目 | 当前证据/下一步 |
|---|---|
| 历史PRIVATE workspace执行 | 两条真实pwe命令越过事件格式校验后报RUNTIME_COMMAND_CONTEXT_REQUIRED，缺原始D06工作上下文。需在命令生产端按当前合同核对/生成原始绑定，不可Runtime捏造上下文或直接改历史DB；未验收文件执行成功。 |
| 材料恢复 | 仍观察MATERIALS_RECOVERY_BINDING_INVALID；必须取得对应record及原始materials/admission绑定逐字段核对。源码有materialsInput条件，不能无证据断言普通CHAT全被误路由。 |
| 正式议事新增资料 | 实页“添加资料”只展开已关联资料/范围，没有空列表下的新选择入口；与F6共用选材目标仍有差距，未以已有资料展示冒充新增资料全流程。 |
| 完成后的恢复呈现 | 475刷新仍可能显示初始已取消request的状态，历史“回答此问”按钮及原验收恢复操作仍显示。composer已隐藏不等于所有历史写操作入口完成只读收口；未点击这些写入口，不能声称完整readonly。需统一当前请求选择及终态控件可用性。 |
| 完整页面、媒体、多Agent、付费 | 尚未全部走查。议事重复标题/目标提示等与最新原型仍需对照；文字主流程成功不覆盖这些项目。 |
| 自有旧测试474 | 此前b73042f生成后backend STREAMING异常仍需定向读回/真实停止收尾；没有把它伪造为已完成或直接改DB。 |

本记录不将以上OPEN改成PASS，不以总测试数替代需求验收。不安排多Agent，不扩建框架。

## 2026-10-20 11:20 CST 续接实施检查点（未整体验收）

- Web **1.16.21 / ab484ee60505295877096d6db4bab468cec120ad / Flow253 SUCCESS**；3105通过、2pending。tree `1deb3b0e4557ec108268b4298d763f9ebe5fc464`，归档SHA256 `227bfb2a522a3be1d31b4e9f35556cc53597e26cd6372ecbe06f648930d8791f`；366安装文件、同Run制品与公网入口/议事JS/CSS逐项匹配。临时配置已恢复并readback。API/Runtime本轮未改动/发布。
- 本批实现完成态控件和旧状态收口、验收权威闭合隐藏恢复按钮、正式议事共用固定版本资料选择。原型与规格同步；文档检查97项通过。组件集成146项本机诊断通过，不用它替代Flow。
- **真实浏览器未通过的两项**：
  1. 已完成475的成果页“查看议事记录”不跳转。源码`continueBountyModification`把所有终态都拒绝，导致只读导航也被禁止。已补本地修复（仅允许completed只读回原会话，cancelled仍不恢复）；18项定向通过，但在253发布之后修改，**不在253制品中**，尚未正式验证/发布。
  2. 自有474的catalog184首轮CANCELLED、185后续轮STREAMING(2776/2775)，页面恢复却采用首轮。实际UI点击向旧turn_45ece发送取消；本次测试只放行真实待停止turn_007088的精确路径，因此请求被保护拦截，**没有取消成功，也没有写入生产**。随后首轮权威读回显示已取消，不能误算后续轮已停止。证据`owned474-restoration-gap.json`。候选定位是活动请求恢复/历史事件归属，不是后端取消CAS再次失败。必须与首轮adoption的冻结合同分开修复，不以取任意最新会话替代原会话恢复。
- 475截图`/var/tmp/cyf-remaining-implementation-20261020/browser/pc475-terminal-web253.png`实际停在成果页且有新手指引；不是终态议事截图，不能用0个chat控件证明只读通过。浏览器已登录但未完成本批PC/移动端闭环，不标PASS。
- 历史材料v4/current-v5恢复、PRIVATE缺D06 delivery仍OPEN，详见code-backend-design的11:06事实；未篡改冻结记录或直接修库。
- 下一步严格顺序：只读导航与原会话活动请求恢复一并补齐回归→集中Flow→PC/移动重进/停止/选材/交付/验收；PRIVATE admission独立按原合同修复，历史记录只能有授权地取消/撤销。媒体、多Agent、付费、全页面尚未全验收，不以文字链路或测试总数替代。

## 2026-10-20 11:48 CST：254发布与生产定向验收

- Web **1.16.22 / d349f0b3e77078def8e0f344d74d4ae8fff261ad / Flow254 SUCCESS**，tree `55bd57c12fa292a2e4598a9913076cc4bd7546f9`。3113通过/2pending，366安装文件和公网入口/议事JS/CSS一致；归档 `48617a7c9a01e8ef9dd6761c8eb89e6642fb4a7b7af46a5ee8b91689ef9708a7`。配置恢复/readback完成；API和Runtime未重复构建/发布。结构化证据 `web254-*`。
- 474真实点击停止的是后续request `b73042f...` / turn `00708861...`：2776/2775发起，HTTP200返回CANCELLED、2777/2775、USER_REQUESTED。不是旧首轮取消；回执 `web254-live-receipts.json`。刷新重新进入仍可继续讨论，停止控件不再显示。
- 475通过“查看进展→查看历史成果→查看议事记录”真实进入原议事；PC显示“事项已完成”，只有刷新与话头记录，0个可见输入框，无回答/新建/删除/验收恢复按钮。移动390×844也真实存在议事面板并保持只读、无横向溢出。移动布局隐藏桌面状态文案，不能把该项写成移动显示完成标签。截图 `pc475-completed-history-web254.png`、`mobile475-completed-history-web254.png`。
- 474空资料目录可打开共用资料选择器；选既有自有验收文件 `CYF-ACCEPTANCE-20261016-concurrent.txt`，预览实际内容明确“测试资料，不含业务数据”。移动端“预览/收起预览”切换正常；PC选择后添加、完成，唯一POST `/agent/tasks/474/file-links`返回201，固定version=3、role=REFERENCE、state=ACTIVE，relationId `pwtl_f9ceabc25d6c48e98289f008963fa0f7`。选择本身没有发送议事；刷新关联仍在。此项仅证明资料选择/预览/绑定，不等于Agent材料执行通过。
- 开启临时fetch克隆观测期间看到network error/重连；移除观测（完整刷新）后以原生fetch重新进入474，20秒只读CDP记录无错误，控件正常。本次不据受干扰观测新增产品缺陷或宣称网络绝不会中断，后续材料真实发送单独核验。
- 历史v4材料记录、PRIVATE D06生产端和未覆盖媒体/多Agent/付费/全页面仍OPEN；不标整体完成。

### 11:56续核：新材料合同与SSE故障反证（不关闭OPEN）

- 真实UI继续向474发送固定v3读取需求；唯一discussion POST202生成 `mmd-typed-request_de8c3d2cf2ecc9e9d28a6cec4069c1382fca295a` / `turn_e00435aebd020af5c8cbf450efc8c0c88889b1d8`。Runtime归档COMPLETED；冻结typedDeliberation为**v5**，非历史v4恢复问题。
- 当前吴用原生材料profile只有`image/png / LOCAL_IMAGE`，无DIRECT_TEXT；因此text/plain固定v3虽然正确进入sourceSelectors，但nativeSources为空。实际模型返回缺少可读文本、请求补充；最终typed-outcome **READY/澄清**，不是交付成果。不能将文本读取不支持解释成“关联丢失”，也不擅自扩展原生输入能力。精确证据`web254-material-current-contract.json`。
- **新确认的同步断点**：原生fetch（没有临时克隆观测）也捕获SSE `net::ERR_HTTP2_PROTOCOL_ERROR`，页面停在“CHAT · 已受理/正在回话”，尽管权威request GET已COMPLETED/FINAL_PERSISTED72/70、finalMessageId1867271。刷新重进后显示已保存答复及澄清卡、输入区恢复。故前述20秒无错误只是观察窗口，不能排除真实传输故障。`web254-native-sse-diagnostic.json`保留CDP错误；`pc474-material-final-stale-ui-web254.png`为刷新前反证。
- 已确认传输错误与状态滞留同时存在，**尚未确认HTTP2中断服务端根因**；现阶段不能声称只有模型问题或随意加轮询解决。下一步定向核对现有恢复readback是否推进当前request/turn及最终消息，并定位实际SSE协议错误；只复用原权威读取、生命周期/身份guard和原事件流，不增加并行监听/自动重发/伪造完成。相关修复与回归集中后再Flow，不为记录文档重复构建。
- 本次自有浏览器关闭，环境原型标签未动；未取消他人进程，未直接改数据库/冻结历史记录。

### 2026-10-20 12:20 CST：Web255与SSE根因修正候选
- Web1.16.23/f08e427f56f9172068b697eae13dcdbfd0076f9c，tree9ba5c9cc7e45828f3e251699c5d16b3acebd4d97；Flow255正式3125通过/2pending，同Run归档29e06f8e5fd5798baa9b987532b142cff08d78fa504bc78aa4978b115d9aa672，366安装文件及公网入口/议事JS/CSS一致。已恢复云端配置并readback APPLIED（第一次缺name参数被本地校验拒绝、未写云端；补全参数后成功，不是重复部署）。
- 认证后的新自有浏览器继续474吴用原会话，资料范围明确NONE；新文字discussion唯一POST202→f9ecc2b907e2f3987e84cc292af8e82e98190271/turn0e93888268a26fa23581dd1a7bb900f80dd29ec3。没有刷新，界面出现持久最终通知；request权威COMPLETED、FINAL_PERSISTED23/21、finalMessageId1867453。此时后端仍193，仍有真实HTTP2断流，证明前端恢复不再无限等待；不代表服务端断流已修复，也不等于文本交付验收（此轮typed outcome是议事答复）。证据web255-pc-natural-recovery.json/png。
- 首次人工断网发生在该轮最终答复显示之后，明确**不算生成中断网测试**；暂时将自有浏览器离线，避免旧服务端回放反复溢出，部署后再继续真实在途断网。
- 生产root.log 11:54:11/11:54:41可证实64条缓冲溢出及SSE响应无法JSON编码，脱敏摘录sse-replay-overflow.log。后端最小补丁9ca2776c27ce3270efa0ea4c366b7de0e68e8dbb（tree847927f2fc9d76ca09cee79dc7aa987a627450c5），仅认证durable流去除急切buffer、4项新增回归；API1.16.18/Flow195运行中。正式结果与生产复测未出，不标已修复。

### 2026-10-20 12:40 CST：本批上线闭环、真实恢复验证及仍OPEN的投影问题
- **正式发布已核验**：API195/1.16.18/9ca2776c27，2606通过/122skip，新增4项全部包含在ChatConversationEventsHttpTest 9项内；SensitiveResponseBodyAdviceTest 8项本批正式执行。Flow SUCCESS、同Run归档4c08a1c70d5de09be6e676ed8ae40df84aba104489e39b5de85628f231cc258b、JAR a71821bea7caed3ae1d37d9dadb5accde4e4f6cebc7081b0c96a32e64851c6c3、canonical运行PID3525824/cwd与健康核验一致，版本记录verified。API与Web临时Flow配置均已恢复/readback。API193/194不冒充本次测试。
- Web255+API195：原474继续PC300字修改a04fbd98...→child delivery-revision_1478eb...（finalMessage1867506，337个delta）；移动改22日200字ecd44e24...→child delivery-revision_45c27d...，页面显示22日完整方案，无横向溢出。**总计3次discussion POST**（含前批f9ecc），各一次，无自动重发；后来尝试23日草稿被前端核对挡住，未POST。未改DB/Runtime/资金。
- **修正验证边界**：CDP offline并未可靠中断既存SSE——离线期间仍收到实时提示、同时只读GET失败。因此上述截图只证明PC/移动正文可见，不能称完整“在途SSE断开→全部状态自动恢复”通过。12:33的AbortController试验没有新请求且被识别为取消，不计在途恢复。12:37:02另对自有流reader显式注入TypeError（不clone、不改帧、立即恢复原fetch），12:37:05观察现有重连先GET原request终态再重开SSE，无新POST，确认Web255实际重连路径生效；它是受控故障，不是自然HTTP2故障。稳定重登后的本次观察窗口没有新的HTTP2错误，API新PID没有缓冲溢出/转换异常。
- **新确认OPEN（不得以正文恢复替代验收）**：
  1. SSE仍可传递而typed-outcome/catalog GET失败时，网络恢复后无后续事件便不再补齐成果状态，工具栏验收入口可能缺失。手动重取能暴露下一项，但不是自动恢复PASS。
  2. `retryHallConversation`只重取会话；原任务投影还在taskVersion3，权威interactions/context已经7。`bountyAssignmentContextProjection`按合同严格拒绝不一致，之后发送未发出POST。下一步需先在同身份/任务/会话fence内读取并收纳canonical TaskDTO，再刷新assignment/catalog/outcomes；不得删掉taskVersion或授权检查。
  3. 打开验收弹层会读取最新delivery-review-context，但`previewReviewOutput`仅在输出数组为空时刷新；已有旧批次非空缓存找不到最新artifact时，直接显示“此固定成果暂不可预览”。下一步核对精确artifact/version/hash不匹配时一次性刷新原outputs，重做fence与精确匹配；不得猜选最新文件/放宽摘要。此次未确认验收，474保留待验收用于后续修复。
- 上述3项属于同一“旧投影恢复”缺口，已主动告知用户，不在本次已发布补丁中暗称修好。历史PRIVATE缺D06、冻结v4材料以及全媒体/多Agent/付费/全页面仍保留原OPEN。结构化证据web255-api195-browser-verification.json及同名截图。

## 2026-10-20 13:30 CST：三项当前DFX闭环（非历史兼容）
- Web1.16.24 / 50107f38a757a5ce58d298965a953a353d7b48b1 / tree2adbc30cdc5cdbd7db3f41375751113e22e448b8，Flow4403172/257 SUCCESS，3142pass/2pending。归档SHA256 `90ba66fb29cecd724c10e8bb91d27a4c5c1ec7e2ba4036c6bf2c48b519790716`；366安装文件及公网入口/JuyiHall JS/CSS匹配。原配置已恢复/readback APPLIED。API195/1.16.18和Runtime未变。
- Flow256测试失败：页面测试替身未提供新增恢复方法/上下文依赖，3137pass/5fail/2pending，无部署；补齐后257正式全量通过，不跳过测试。本机定向149项、页面组件/路由122项只作开发反馈。
- **事项快照**：自有474新发23日通知、再在移动视口自然改24日，均真实受理，无页面刷新；当前taskVersion7→9→11，最终验收12。不放宽版本/指派/身份门禁。
- **失败读恢复**：13:18–13:19仅本测试浏览器按精确conversation阻断目录/typed-outcome GET，SSE未改；原生消息继续到达。13:19:14.165恢复fetch，13:19:15现有调度自动GET目录/typed-outcome，卡片恢复；无刷新、自动POST、第二条事件流或新监听。此为显式GET-only传输故障注入，不冒充自然断网。
- **精确预览**：先预览22日成果建立缓存，再生成23日成果；13:19:49打开验收上下文、13:20:01点击预览才一次刷新原deliverables，随后读取新artifact/version1内容，正文确为23日。移动继续修改24日后也精确预览24日成果。无换旧版本、无摘要绕过。
- **完整文字主流程**：PC1440×1000新477、移动390×844新478，经实际界面创建待点将→确认吴用→自动原议事→文字正式交付→预览→显式验收，均COMMITTED/COMPLETED/ACCEPTED、taskVersion4；474亦ACCEPT/COMPLETED/taskVersion12。三次终态composer隐藏，390视口无横向溢出。截图及精确回执见web257-projection-dfx-verification.json及pc257/mobile257系列。
- 测试限定：runner最初错误许可路径分别本地拦截一次474讨论及477创建；没有到达服务器写入。前者明确再次点击发送，仅两个修订真实admission；后者通过“确认继续原张榜”原键恢复。移动478创建无拦截。记录反证，不把受控/误配故障算原生线上问题。新会话全流程只用吴用，无李逵、扣费、直接DB修改或历史修补。
- **仍OPEN（独立范围）**：PRIVATE原D06缺失、历史v4材料；媒体/多Agent/付费/全页面完整覆盖。未增加兼容层或伪造绑定。当前三项已闭环，不等于整体历史需求所有分支通过。
