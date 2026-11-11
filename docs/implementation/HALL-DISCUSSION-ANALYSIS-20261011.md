# 厅内议事：首轮问题分析（2026-10-11）

## 范围、Owner、基线

- 用户要求：先分析厅内议事；Main唯一Owner。仅只读源码/版本核对、临时合成接口诊断及本文档，不实施修复、不发布、不创建生产会话/事项、不调用模型或业务写接口。
- 核对时间：2026-10-11 11:52–11:58 CST。Web/API develop tracked clean。Web本地及实时远端 `13c1cb11d61f27806d0af29d3972edf50c9750e5`；生产Web **1.14.5 / Run197 / `21ded98d9b642eefa683403fd6068933186d7865`**。
- 本地比生产多出的13c1cb1只去除密议预填文本的@前缀（两业务行及测试），不是本轮修复，也不能当作已上线。没有改动或回退此提交。
- API本地/实时远端 `33e2344a2af02bb908a20bec1125ab7c23e8d00d`；安装record及实际JAR manifest同commit，版本1.14.3，tree `0a9b387e69e3d275f6185b953b9c1851a6469118`。本轮未重新运行后端测试或生产Provider。
- 入口：AGENTS.md、ops/orchestration/README.md、知识库06会话契约、HALL-PROTOCOL-CONVERGENCE-20261009.md；复用现有Vue composables、tests/setup.js与capabilities fixture，不新增测试框架/Reviewer。

## 证据强度

证据目录：`/var/tmp/cyf-hall-discussion-analysis-20261011-mnhtZD`。

1. `source-proof.json`：本地、线上源码及差异。
2. `diagnostic-result.json`：本地13c1cb1实际Vue会话/context函数，合成API，五个观察场景。
3. `online-source-diagnostic-result.json`：取**已部署21ded98**的useHallConversation源码重复定向复现；只改模块import为绝对路径，不改业务逻辑。其他依赖与已部署commit字节相同，差异清单已检查。
4. 两轮诊断均exit0、观察一致；这是实际前端函数+合成接口诊断，**不是线上真人发送/模型推理/完整HTTP跨端实测**。没有访问生产账号数据。

## 当前链路与语义

`PublicDiscussionPanel → ChatPanel/HallChatComposer → useHallChatContext + useHallConversation → POST /chat/stream → scope/roster校验 → durable admission → outbox → 内置宋江或目标Runtime → durable事件/请求GET → 页面`。

- 公议不点名时前端targets为空；后端`JuyitingConversationScopeService.java:76–78`补默认Agent，`BuiltinHallAgentSupport.defaultAgentId()`返回宋江。这不是广播给全体好汉。
- 前端`useHallChatContext.js:159–162`每次点名覆盖为一个ID。接口层可以存在多目标，但当前输入区并没有可靠的多选点名模型；不能把“众好汉”文案当作多Agent调度完成。
- 本轮不将公议聊天、悬赏事项议事、真实创建/指派任务合并为同一功能；也未证明“讨论结论→真实办理”已闭环。

## P1-A：回话已完成，但下一条发送被未释放的隐藏锁挡住

**定向复现已成立**：请求/turn回读分别COMPLETED/PUBLISHED，`isConversationBusy=false`、`isSubmitting=false`、`isAwaitingReply=false`，保持POST流未结束；发送第二条返回false，POST总数仍1，第二条草稿保留。

根因链：
- `JuyitingAgentRelayService.java:99–105`将当前request过滤后的**会话长事件流**拼入POST响应，没有该request全体turn终态的结束条件。
- `ChatConversationEventBroker.java:35–43`提供长订阅，不因普通最终回话自动结束。
- `useHttp.js:231–289`在reader结束前不返回。
- `useHallConversation.js:333–339`业务终态只更新可见busy/streaming/awaiting。
- 同文件`:1381–1390`的activeSendToken只在await performHallMessageSend结束的finally释放；下一条却先被此token拒绝，且该token不在可见busy中。

建议修复（不新增功能）：把**单次提交锁/单个request传输生命周期**与会话长SSE订阅分开。仅在权威request及全部相关turn已终态后收尾该request的POST reader和token；不能见到任一子Agent最终消息就提前结束。后端POST应按该request聚合终态收尾，长事件订阅另走现有会话events。旧回调/旧finally必须核对request token和身份代次，不能清掉下一条发送状态。不要仅删除并发保护，也不要用固定时间强制解锁。

验收：终态但连接仍开时可发第二条；多子回话部分完成不能解锁；失败/取消正确收尾；断网未知仍禁止盲重发；旧流迟到不污染新请求；身份/话头切换隔离。

## P1-B：服务端明确拒绝被当成普通会话帧，页面继续等待

**定向复现已成立**：输入与后端一致的`{error:"target outside owned roster",conversationId:"1001",...}`后正常结束传输；send返回true，activeRequest仍SUBMITTING，busy=true，草稿已清空，页面“等待回话”，没有错误消息。

根因链：
- `JuyitingAgentRelayService.java:71–81`在admit前以SSE error对象返回明确拒绝，而非accepted请求；对象含conversationId、不含request终态。
- `useHttp.js`对HTTP错误有判断，但HTTP200的SSE帧直接转onStream，不解析业务error。
- `hallConversationMessages.js:326–334`优先将任何含conversationId的对象认作会话引用，未识别error；`useHallConversation.processStream`同样无此拒绝分支。
- `useHallConversation.js:1230–1248`此前已清草稿并置SUBMITTING；正常onStreamEnd不把明确未受理转成失败。随后GET不存在的request也不能证明已受理。

建议修复：使用明确、关联当前request的拒绝契约（拒绝发生于admission前时优先标准非2xx，或定义本次请求的结构化拒绝事件）；前端先判断错误再处理conversation引用。明确未受理时展示原因、解除本请求busy，恢复原草稿但不覆盖用户的新编辑，不自动重发。网络中断/是否受理未知仍只GET原request，不能当明确拒绝直接解锁。不要把所有错误一律归为“连接中断”。

验收：非法目标/租约不可接新工作/scope拒绝有明确反馈；无幽灵SUBMITTING；草稿不丢；未知请求和已受理失败分开；身份/话头切换后的旧错误不污染当前会话。

## P1-C：点名对象、可见对象与草稿文本脱节

**三个定向场景成立**：
1. 公议点名甲后，wireTargets=[甲]，但传给面板的conversationAgent=null、目标文案“众好汉”。
2. 删除草稿里的@甲、输入普通新问题，wireTargets仍=[甲]。
3. 草稿能同时出现“@甲 … @乙”，wireTargets却仅=[乙]。

根因：
- `useHallChatContext.js:31–34`conversationAgent只由conversationSubject取得；public的setMentionAgent只改chatMentionAgentIds，不改该subject。
- `JuyiHall.vue:583`传入selected-agent=conversationAgent；`HallChatComposer.vue:211–216`public目标chip依赖该selectedAgent，因此实际点名的chip缺失，清除对象入口也不可见。
- `useHallChatContext.js:159–162`点名ID是独立单值数组；`useHallConversation.js:1782–1803`只向草稿添加@文本；编辑草稿不变更点名ID，追加第二个人时旧文本仍可保留。

建议修复：沿用**单目标**能力，不扩多人调度；明确唯一权威点名状态，public的目标chip/文案/请求体统一读取该状态。更换或清除对象同步展示，避免“正文看似多点名、实际上只投递最后一人”。普通正文中的人名不能自动授予调用权限。删除文本是否清目标须选择明确一致的交互：推荐可见chip为权威，正文不再重复承担隐藏选中态；清除chip后恢复默认宋江并明示。名单变化导致原目标不可用时明确提示，不悄悄转给默认Agent。

验收：点名→chip可见→实际投递一致；切人/清人/删正文/另起话头均无隐藏残留；私聊固定对象、悬赏成员约束及只点自家好汉保持。

## P2：默认对象文案不准确

`PublicDiscussionPanel.vue:6–9`显示“向众好汉传话”，`useHallChatContext.js:60`显示“众好汉”，但不点名实际为宋江。建议显示“宋江主持；可点名自家好汉”等准确提示，而不是为文案新增广播/多人执行功能。

## 最小后续范围

1. 先修P1-A（连续对话）和P1-B（明确失败收尾）。
2. 修P1-C，并顺带统一P2默认对象文案。
3. 复用原测试入口补真实挂载/HTTP事件合同：重点保留“终态但连接未断”及“HTTP200错误帧”，不能mock每次都onStreamEnd后立即resolve从而掩盖问题。
4. 源码修复后另行按前端Flow/后端本地验证与授权发布；本轮没有启动构建/发布。旧基线测试通过不撤销，但不能替代新增失败形态覆盖。

未验证：真实在线第一问/第二问、宋江Provider/工具调用、托管Agent当前接收与执行、完整多目标聚合、议事形成事项及资金效果、移动端此次真实截图。上述缺少证据不自动认定为故障，也不宣称流程全部跑通。

## 2026-10-11 详设接续

用户确认一轮结束后再发下一轮，具体待实施详设见 `HALL-DISCUSSION-ROUND-CLOSEOUT-DESIGN-20261011.md`。其他点名/拒绝问题独立保留；图片不是从未生成成功，但当前组合的新完整流程尚未验收，证据与边界见详设第8节。没有实施或发布。
