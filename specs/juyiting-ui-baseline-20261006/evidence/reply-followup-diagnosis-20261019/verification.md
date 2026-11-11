# 发布后议事异常定向核对（2026-10-19）

## 核对范围与源码
Owner沿用当前会话；修复延续CHAT-STOP-FIX-20261019 / CHAT-STOP-UI-20261019。无新生产写入、无新部署、无服务重启。
- 线上基线：API5aa8efc246/1.16.9/Flow156，Web bca42d2ea6/1.16.10/Flow230。
- 修复候选已推develop：API `c59311a1d88b77565a7cb5d5c71618d0b47ca321` / tree `8e5d5a99644c96d5c310d89677b80cff2cbd5e91`；Web `59ba8a8ef8306eaf8a39f51a6709118b0418d783` / tree `bbed5e182603469e584d309030b5c4ad3df463f7`。推送前远端匹配原线上源码；未覆盖无关修改。
- Runtime只读源码与线上安装均6a9d8d3c1219450c19b3edfbef317e615940ab5d；未修改/安装Runtime。

## 1. 后续用户消息不显示：已确认代码原因，候选已修
`useHallChatContext.enterBountyDiscussion`会明确清空selectedAgent，而`useHallConversation.adoptTypedDiscussionReceipt`却要求selectedAgent匹配当前承办Agent，提前return false。因此线上受理之后没有GET /requests/{id}和会话content读回，仅卡片目录更新。既有测试始终填充selectedAgent而掩盖真实入口。
修复按chatContext的事项、规范scopeKey、participantAgentIds及唯一target校验；保留身份、会话代次、请求revision/stateVersion和迟到响应保护；浏览别的Agent/事项不改变议事主体，真正目标漂移必须拒绝旧读回。不合成用户消息、不二次POST。
回归先红：新增无selectedAgent用例失败，真正目标漂移用例也发现旧实现未阻止；修复后page-routing13通过，typed交互/报文/bootstrap/取消合计175通过。仅本地开发诊断，非正式Flow验收。

## 2. 空白delta造成虚假缺口：已确认代码路径缺陷，候选已修
`AgentWebSocketHandler.publishAgentMessageDelta`原来以content.isBlank拒绝空格/换行，Runtime却给所有非空片段分配deltaSeq；下一片就会触发服务层连续性检查。改用isEmpty，空串/null仍拒绝，保留真实空白原文与序号，未绕过ACL、绑定或连续性校验。
参数化原有认证身份回归覆盖普通文本、空格、换行、制表符及混合空白；通过真实WS报文规范化至服务调用断言，无跳过身份流程。该Java用例后续已在API Run161通过，详见末尾最新验证记录。
生产318片段本体没有留存，因此这是可确定的代码缺陷及缺口解释，不能宣称已逐字证实该次318片段内容；线上复验还须观察lastDeltaSeq连续、无RECOVERY_REQUIRED并完成停止/继续发送。

## 3. 不同提问都回复“收到。”：已排除输入丢失，尚未修复
只读事务核对task467/conversation1760458006508，USER消息1858627/1858638/1858649、对应context快照与dispatch outbox内容均正确；吴用实际引擎会话也收到三条不同输入并实际输出三次“收到。”。留证仅测试输入/输出，不复制凭据、个人资料或推理记录。
证据：formal-persisted-context.json、formal-dispatch.json、formal-runtime-input-output.json。
提示策略疑点：chat-runtime.mjs的buildContextEnvelope把currentUserMessage与附件/历史一起标记为不可遵循的DATA。应区分“当前人类请求是任务意图”与“文字不构成授权/系统策略”，但仅源码检查不足以证明改文案必然解决模型行为。
下一步：在固定Runtime源码的隔离候选中核对buildContextEnvelope、agent-client.mjs的FAST_CHAT_INSTRUCTIONS、juyiting-action-outcome.mjs的ACTION_OUTCOME_INSTRUCTIONS；只允许理解当前直接请求，附件/历史/日志中的指令仍为数据，禁止提升执行、文件访问、计费权限；availableActions、真实资料载体与服务端grant继续为权威。提示变动须进入instructionSourceHash/contractDigest和threadKey，不能恢复旧提示绑定。用同样三轮测试对照旧/新候选，再覆盖附件注入、缺资料澄清、纯文字成果deliverable、修改关联及验收，才可认定根因修复。不强制模型“总回复某字符串”，不把ack标为成果。

## 初次正式验证阻塞（历史）
API Flow5260799/157、Web Flow4403172/231均FAIL；云端未返回检出源码commit、作业日志为空（more=false）。因此它们不是任何SHA的测试/构建成功证据；当前仅能确认未取得有效执行证据，不能猜测是额度、网络或代码错误。未重复启动，未改用本机构建。
本轮临时配置已恢复并readback：API a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a；Web 31883fd59c9a33ef4847979fd99147375fda555d99498f17bc8cc5a6b94c389b。保存失败Run、原始受控候选、定向日志与恢复回执。控制目录/var/tmp/cyf-reply-followup-fix-20261019。

结论：两处源代码修复已集成，云端验证未完成、未发布；第三处模型回复异常仍需Runtime对照实验。整体方案不标完成。


### 2026-10-19 授权重试结果（12:28 CST核对）
- 源码未变：API c59311a1d88b77565a7cb5d5c71618d0b47ca321；Web59ba8a8ef8306eaf8a39f51a6709118b0418d783。仅CI验证，无部署、无生产重启。
- Web Flow4403172/232 SUCCESS，实际源码匹配；日志摘要3054 passing、2 pending，Vite构建及JavaScript扫描成功。日志摘录不是完整日志；尚未独立下载校验本Run制品，不作为上线证据。
- API Flow5260799/158 FAIL，实际源码匹配，日志明确验证快照owner=null导致编排器拒绝Gradle；属于本次验证准备错误，不是业务测试失败。绑定chat-stop-main/codex/writer并重建快照后运行159，没有绕过门禁或改变源码。
- API Flow5260799/159 FAIL，实际源码匹配，已实际运行219项测试，5失败、1跳过。五个失败均为AgentWebSocketHandlerTest.durableAgentCallbacksUseAuthenticatedRuntimeIdentityInsteadOfPayloadNames的参数化实例，AgentWebSocketHandlerTest.java:1175报告WantedButNotInvoked，预期acceptDelta未发生。当前仅确认失败点，未确定在哪个前置校验退出，不将其擅自归因为测试夹具或产品缺陷。分层检查/fresh最终制品不能认定通过。
- 两端终态后均确认无活动Run和候选配置无冲突，恢复原配置并readback：API a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a；Web31883fd59c9a33ef4847979fd99147375fda555d99498f17bc8cc5a6b94c389b。
- 最新阻塞已从历史无日志变为后端真实测试失败；下一步取得WS错误回执/完整测试失败详情，核对认证会话、规范化载荷、会话归属和发送者解析，再修正并验证。Runtime三轮均回复“收到。”仍独立未解决；完整议事/验收及新修复上线均不标完成。
- 证据：同目录api-run158-status.json、api-run159-status.json、web-run232-status.json、对应log-excerpt及restore-result；控制文件仍在/var/tmp/cyf-reply-followup-fix-20261019/retry-authorized和retry-owner-fixed，不复制含敏感展开参数的private-status。


## 最新核对：正式CI已通过，未发布（2026-10-19 13:01 CST）

### 已证实根因与修正
Run160（诊断源码de592f96106252dc3eba1f21c1a340874a0778ba）已从真实WS回执取得`ENVELOPE_FIELD_CONFLICT`，字段messageId：旧normalizer误将requestId与messageId当别名，注册被拒绝，后续回调收到AGENT_NOT_REGISTERED。证据为api-run160-callback-diagnosis.json，原始诊断分片合并SHA04b866e389be612bec07cca9397d82334c08671977c65c6c2732c7669807b153核验匹配。
修复遵循接口标准v1.2：两个ID各司其职，不强制相等；messageId缺失不能用requestId代替。同字段跨层冲突、身份/ACL、运行时绑定、序号连续性保持校验。参数化测试使用当前canonical消息并验证注册与最终回执关联，成果持久ID读data.persistedMessageId。

### 固定源码与正式证据
- API `cd2146f408e692fc58424390e89a40d2f10eb7d2` / tree `b757d4cf1b4d3c1b864a2be47106ba0e0b734d56`，已推develop。Flow5260799/161 SUCCESS，实际检出SHA匹配，261测试套件共2420项：2325通过、95跳过、0失败/错误；validateLayering和fresh bootJar成功。17项normalizer、1项command wire及5组普通/空白分片测试全部通过。
- API测试诊断分片SHA b9bc5a3a4e128cfb89926d368a9565b00a2bd9129b4adafc824abd4ecaa2ed7f校验匹配；详见api-run161-tests.json和api-run161-status.json。
- 同Run报告JAR SHA f36206fb630c1f93aa36f6144ebcd520a0774ce84472927b3af2bac9acadd4f7，receipt SHA7a48b260bf4de2feaafe344816df4541b248b768f93252609eb055e629a0e5a2；仅记录Flow产物元数据，未独立下载验包，不能视为部署/安装核验。
- Web `59ba8a8ef8306eaf8a39f51a6709118b0418d783` / Flow4403172/232先前已正式通过：3054 passing、2 pending及构建、扫描；本轮未改Web，不重复构建。
- 本轮没有部署、生产重启、DDL或Runtime修改；原型也没有新增交互，修复的是既有协议和产品接线，不另造原型。

### 仍未完成
正式CI阻塞已解决，但Runtime对不同输入均回复“收到。”仍未解决；本次根因仅证实WS用例注册拒绝，不据此解释模型行为。完整正式议事→继续修改→成果→人工验收的生产闭环未重新验收，全部UI优化也未发布。下一步固定Runtime源码做输入/提示策略对照，保留附件注入防护及服务端授权；新候选的版本发布须与线上核验单独进行。

Run161终态后确认无其他活动Run且临时配置一致，已恢复API原配置并readback（SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a），见api-run161-restore-result.json。Web未再改配置；先前Run232恢复记录继续有效。


## 2026-10-19 Runtime对照与生产复测（未发布）

### 固定输入与候选范围
- Owner chat-stop-main/codex/writer；Runtime基线/已安装源码 `6a9d8d3c1219450c19b3edfbef317e615940ab5d`，tree `e4d60f86995fa7070e4adfff2ef1b01c4e805031`。原仓库 `/home/isp/wsps/chcbz/isp-install` 未改动。
- 隔离worktree `/var/tmp/cyf-runtime-intent-20261019/source`，分支 `codex/chat-user-intent`，本地候选 `f94c254f956f09717711486e8941847ff2bd95c7` / tree `f664c986379d692c663598121a1eae8036424503`。未push/合入、未安装，不声称已修复线上异常。
- 四文件候选区分直接用户任务意图与附件/历史中的嵌入指令，实际developerInstructions纳入threadKey指纹，即使调用者显式提供instructionSourceHash也不能复用旧提示会话。认证/服务端授权/工具权限不扩大。
- 实际模型 `gpt-6-luna`、CLI0.161.0；生产与新隔离会话baseInstructions摘要一致。不能因HOME默认model不同而声称实际模型不一致。

### 验证矩阵
| 检查 | 实际结果 | 边界 |
|---|---|---|
| Runtime单元及typed/action/schema | 62通过 | 本地诊断，非API/Web正式Flow |
| 资料安全/普通与混合资料wire | 18通过 | 无安装/生产Runtime变更 |
| 同原第三轮envelope、fresh thread的A/B | 旧、新策略均43 | 不支持旧提示为确定根因 |
| 原三轮envelope连续重放，每组新会话 | 两组均完成60条建议并回答43 | 没有复现历史三轮“收到。” |
| 候选附件AGENTS.md注入 | 43，无action | 嵌入指令未取代任务 |
| 候选缺图输入 | CLARIFY、deliverable=false、无action | 没有臆造图片结果 |
| 增加生产同文AGENTS.md的三轮对照 | 旧策略第2轮输出空text，校验ACTION_OUTCOME_INVALID；测试中断 | 不是重复“收到。”复现，也不是整组通过；新策略本组未执行 |
| 带同文AGENTS.md的独立算术A/B | 两组均43 | 单独增加AGENTS内容不足以解释原会话异常 |
| 生产原事项467继续发送算术 | 再次收到“收到。”，deliverable=false | 原生模型最终输出与HTTP持久结果一致，问题仍在 |

资料：`runtime-live-results.json`、`runtime-multiturn-results.json`、`runtime-boundary-results.json`、`runtime-context-multiturn-finals.json`、`runtime-context-arithmetic-results.json`、`runtime-context-fingerprints.json`。只保存最终答案/测试输入/指纹，不复制凭据、模型推理、生产完整上下文或HOME。测试文本60条数量及算术结果通过，不把每条约50字视为逐条验收通过。

### 生产复测闭环证据
13:20 CST使用获授权测试账号，通过生产UI向既有正式事项467/会话1760458006508的吴用发送一次标记算术请求；未新增付费动作、未取消/验收事项。请求 `mmd-typed-request_4d91a398038f8cd545dae4d1ae3e3434160df3aa`，USER1859218，最终ASSISTANT1859219。
- HTTP请求状态COMPLETED，turn=PUBLISHED、lastDeltaSeq=2；typed-outcome=READY/ANSWER，text=“收到。”、deliverable=false。COMPLETED仅表示请求结束，不能表示需求完成或成果可验收。
- 原生rollout同一生产thread中输入为本轮算术请求，模型最终JSON也为“收到。”；已排除本次结果仅由Web渲染/服务端改写造成。
- 当前页面没有即时展示新USER消息，仍符合已定位但未上线的Web回执接线问题；旧消息重新打开可见。截图不是候选Web已修复的证明。
- 证据：`runtime-production-recheck.json`、`runtime-production-native-recheck.json`、`runtime-production-dom-summary.json`、`runtime-production-recheck.png`。

### 结论与下一动作
1. 正式API/Web CI已通过的结论保持；本轮不重跑、不发布、不重启服务。
2. 生产“收到。”已再次复现，根因仍未闭环；候选仅修正已确认的意图/授权表述歧义及会话版本绑定，不标为已证实根因修复。
3. 下一步比较原生产thread恢复历史与新隔离thread的上下文差异；使用冻结输入/隔离会话，不清生产历史、不自动重发、不隐藏无效输出。长请求空输出需记录为独立模型/合同失败，不以兜底“收到。”伪报成功。
4. Runtime候选保持隔离待进一步验证；API/Web候选部署仍需单独版本化发布与线上回归。正式议事停止、继续发送、有效成果及人工验收完整闭环仍未通过。
5. 资源诊断曾遇本任务隔离二进制快照ENOSPC；清理仅限已结束且已保留过滤结果的本任务临时HOME。它不是生产模型回复异常的根因证据。不清理其他任务、生产会话或用户原型。
