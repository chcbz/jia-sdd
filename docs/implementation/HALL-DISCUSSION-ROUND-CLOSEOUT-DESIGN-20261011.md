# 厅内议事连续问答：本轮收尾详设

状态：**已发布，普通密议连续两轮线上验收通过**（2026-10-11 18:13）。Web1.14.6 `7b14dffd5d9d259df720f84e57a8453424fb0a65` / Flow4403172 Run199；API1.14.4 `fb8a43b0c1b8774582e520a809e5f52337198c25` / 原本地installer verified。前端2917通过、2既有pending，后端205通过及validateLayering/freshbootJar。实测同话头两次独立请求、第二轮继承前文、输入解锁、重取保留四条消息。public多Agent线上与独立服务端自然EOF未单独验收；真实观察及边界见 `handoffs/HALL-ROUND-IMPLEMENTATION-20261011.md`。图片能力已READY，但task440仍需任务级外部模型费用精确同意，未实际生图，见 `HALL-IMAGE-RETEST-20261011.md`。下文冻结基线/源码行号保留为原设计历史，不重标为发布版本。

## 1. 冻结范围与基线（2026-10-11）

- 用户确认：同一话头一轮结束再发下一轮；不增加插话、并发轮次、自动排队，不清会话历史。Main负责设计，实施时每个切片唯一Owner，不新增Reviewer。
- 目标：服务端本轮终态后结束本次POST响应；前端释放本轮发送锁，同时保留conversationId、历史和现有会话事件订阅。
- 非目标：点名模型/错误帧修复、图片生成、历史task424恢复、新接口/表、租户迁移、Runtime重构。其他问题见本文第8节，不能顺手扩范围。
- Web本地/远端核对基线 `13c1cb11d61f27806d0af29d3972edf50c9750e5`；线上 `21ded98d9b642eefa683403fd6068933186d7865` /1.14.5/Run197。差额13c1cb1只是密议预填文字，不覆盖/回退。
- API基线及安装manifest `33e2344a2af02bb908a20bec1125ab7c23e8d00d` /1.14.3；源码目录各自develop，tracked clean。行号按上述基线；实施前核对HEAD并保留他人更新。
- 根因及已部署源码定向复现：`HALL-DISCUSSION-ANALYSIS-20261011.md`；证据 `/var/tmp/cyf-hall-discussion-analysis-20261011-mnhtZD/online-source-diagnostic-result.json`。
- 规则：AGENTS.md、ops/orchestration/README.md。设计冻结时尚未派单；后续授权实施已由两个独立Owner/worktree完成，详见本轮handoff。本详设不构成生产发布或Runtime配置变更授权。

## 2. 状态与现有字段：无DDL

使用现有 `chat-deliberation-schema.sql:24–74`：

| 表/对象 | 本次使用字段 | 用途 |
|---|---|---|
| chat_request | tenant_id、owner_jiacn、client_id、request_id、request_revision | 既有身份范围及本轮关联 |
| chat_request | conversation_id、conversation_generation | 保持原话头，拒绝已删/换代会话 |
| chat_request | aggregate_state、state_version | 权威请求聚合状态/版本，不能单独判定PARTIAL完成 |
| chat_turn | turn_id、request_id、request_revision、target_agent_id | 本轮完整子回话集合，不以当前页面已见到的子集代替 |
| chat_turn | state、state_version、final_message_id | 子回话终态及正文引用；终态不等于正文已进入浏览器 |
| RequestView | requestId、requestRevision、conversationId、conversationGeneration、state、stateVersion、turns | 复用`ChatDeliberationService.getRequest`返回契约 |

不写入新的完成记录，不更新业务终态以消除UI等待，不删除历史请求。身份参数从已认证上下文捕获，异步读取显式复用该scope，不硬编码tenant/client，不在线程切换后重新读取ThreadLocal。

### 统一结束谓词

```text
scopeMatches(view, captured tenant/owner/client/conversation/generation/request/revision)
AND view.state in {COMPLETED, FAILED, CANCELLED, PARTIAL}
AND view.turns 非空，完整覆盖本次admission.dispatches中的turnId
AND every turn.state in {FINAL_PERSISTED, PUBLISHED, FAILED, CANCELLED}
```

- `PARTIAL`既可能是一部分仍在运行，也可能是全部结束但成功/失败混合，必须看完整turn列表。
- QUEUED、DISPATCHED、STREAMING、UNKNOWN、RECOVERY_REQUIRED不是终态；没有turn不能凭空判断成功。
- FINAL_PERSISTED已持久化，可以完成本轮；不要求额外等待PUBLISHED。但页面必须能从finalMessageId/原会话内容恢复正文。
- 不把此谓词扩到图片typed action/EXECUTE步骤：本轮范围为现有`/chat/stream`的普通public/private CHAT/INSPECT发送；现有bounty typed受理与执行链不改。

## 3. 后端设计

源码前缀：`api/chat/jia-chat-service/src/main/java/cn/jia/chat/`。

### 3.1 service/JuyitingAgentRelayService.java:84–105

新增小范围私有helper，例如 `requestScopedEvents(admission, capturedScope)`，替换当前“会话长流filter(requestId)”直接拼入POST的做法。

执行顺序：
1. 原受理事务、ACL/租约校验、idempotency不变；明确未受理仍由原错误路径处理，本轮不混入另一缺陷的协议改造。
2. 在Flux订阅时用现有 `ChatConversationEventBroker.subscribeBuffered(conversationId,generation,liveCheck)`登记本POST的独立订阅；**先登记buffer，再读RequestView**，覆盖受理到订阅之间已完成的竞态。
3. 复用 `ChatDeliberationService.getRequest(tenant,owner,client,requestId)` 读取权威快照，核对conversation/generation/revision及预期turn集合。这个读取已有readOnly事务；不要直接绕过服务查DAO。
4. 若快照已终态，本POST可正常完成；浏览器在EOF后GET原请求及正文，不能要求必须再次收到已错过的最终delta。
5. 若仍在执行，消费buffer/live事件，结构化解析JSON按requestId精确过滤，不再仅用字符串contains关联。保留原帧完整内容，不改其他业务事件。
6. 对本轮有效事件串行处理，读取权威RequestView；转发触发完成的最后事件后，再按统一谓词结束。普通delta可合并/减少状态读取，但不能跳过终态信号核对；首版优先正确串行，不新增定时扫描框架。
7. 请求读取为未知/暂时失败时，不伪装正常EOF/完成；以原错误语义让前端GET恢复。客户端断连只释放本POST订阅，不取消durable任务。
8. `Flux.using`或等价doFinally保证本订阅close一次；不能invalidate整个conversation，也不能关闭独立GET events的订阅。

阻塞式事务读取必须经现有工程允许的boundedElastic等阻塞调度方式执行，捕获身份参数，不占WebFlux事件循环；用concatMap保证当前流事件顺序，不引入无界flatMap并发。

注意：事件应在相关事务提交后才被发布；实施时检查真实调用路径并补测试证明。若发现先publish后commit，不能用sleep/固定超时凑终态，应修正该路径到提交后发布或读取已有可靠journal。此项须定向定位，不预先改所有生产者。

replayAdmission当前为有限帧返回（同文件:272起）：保持幂等、不重复admit/outbox。前端EOF读取原请求后决定继续等或完成；本次不为了让replay等待而重发模型。

### 3.2 api/ChatController.java:193–233、466–480

- 保留conversationReference、持久化鉴权、删除代次检查及传输错误处理；不把本轮完成映射成会话删除/取消。
- 外层流应随relay有限流完成正常EOF。现有handleSummary在`answer`为空时直接返回；durable回话没有填此summary，**不能误判当前一定还会因摘要调用模型而挂住**。
- 先增加集成测试验证外层正常complete；若源码无需修改，仅提交测试，不为凑文件数改Controller或普通聊天摘要。
- 不改独立`/chat/conversation/events`长订阅，也不修改ChatStreamPolicy为强制deadline。

### 3.3 后端测试

在现有 `src/test/java/cn/jia/chat/service/JuyitingAgentRelayServiceTest.java` 与 `api/ChatControllerTest.java`补：
- `completesPostAfterAllRequestTurnsTerminal`；最后业务帧仍先送达。
- `doesNotCompleteOnPartialWithPendingTurn`；两个turn一完一未完。
- `completesMixedTerminalPartial`；全部终态但成功/失败混合。
- `handlesTerminalBeforeSubscriptionSnapshot`；无最终live帧亦可有限结束。
- `buffersCompletionBetweenSubscribeAndRead`；明确控制竞态，不sleep猜测。
- `doesNotCompleteOnForeignRequestEvent`、wrong generation/identity。
- `closingPostDoesNotCloseConversationSubscriber`；两个订阅只关闭本POST。
- `disconnectDoesNotCancelDurableWork`、未知/读取失败不伪装成功、重放不生成新任务。
- Controller外层收到完整最终帧并完成；同conversation第二个request可受理；非聚义厅普通流不回归。

如确需修改broker，仅为真实测试发现的close/subscriber隔离错误；不得提前重写broker。

## 4. 前端设计

主文件 `web/src/composables/juyiting/useHallConversation.js`。

### 4.1 本轮独立资源归属

现位置：发送门禁1377–1395；POST及回调1257–1328；请求投影1399–1446；stopHallReplyStreaming243–253。

为每次发送持有局部session（或等价局部变量），至少包含：

```js
{ token, requestId, lifecycleGeneration, authEpoch, scopeSignature,
  replyGeneration, controller, streamHandle, signalCleanup,
  terminalConfirmed: false, closeReason: null, settlePromise: null }
```

token继续作为不变身份标识，不修改当前Object.freeze对象；新增可变完成标记放局部session。旧session清理仅释放自己controller/reader/signalCleanup，写共享activeSendToken前必须比较对象相同。

### 4.2 一个收尾入口

新增 `settleCurrentRequest(session, authoritativeView)`：
1. 校验身份/话头/代次/request/revision、session仍为当前；仅接受原GET完整RequestView，不以单个最终消息或稀疏event作为完整终态证明。
2. 检查第2节谓词。事件提示终态时调用已有requestReadback去重，不另建GET轮询器。
3. 先应用权威request/turns，标记session.terminalConfirmed；正常EOF/本地主动关闭均走该入口，重复调用复用settlePromise。
4. 如最终正文未显示，复用原会话内容GET恢复/去重；正文加载失败单独显示“回话已结束，正文加载待重试”，不能改成模型运行失败或重新POST。下一轮模型上下文来自服务端已持久化历史，不依赖浏览器正文是否渲染完成。
5. 仅结束本轮reader/controller；使用局部`closeReason='request-terminal'`区别于身份变更/用户取消/网络错误，不复用会Abort所有共享句柄的全局stop方法去清理旧轮。
6. 本轮锁释放后允许新request。回调current判断加入session/token归属；旧finally不能清新轮isSubmitting、reader、controller或metadata。
7. 已确认终态的主动传输收尾不进入“连接中断/结果未知”分支。`sendHallMessage()`完成结果不能因自己释放token后current检查失败而变false；先判断同session终态已确认再判断普通stale，身份真正改变时仍不得写新作用域。

### 4.3 触发点与EOF

- `applyRequestView`成功后：如果是当前本地发送session，尝试settle；不是本地session（typed receipt/history）不走本次POST资源收尾。
- `applyDeliberationEvent`：终态只触发原request GET；不能凭首次出现的一个终态turn解锁。
- `onStreamEnd`：只有传输结束，不等于业务成功。始终安排当前request权威GET；网络正常EOF但业务仍运行时保持业务busy，通过原events/poll恢复。
- API层`useHttp.js`正常reader循环不变；不提前resolve所有stream请求，不影响其他消费者。
- busy显示可包含当前未settled发送session，让按钮与真实发送门禁一致；不能仅去掉activeSendToken防双发保护。
- 不新增本地业务强制超时，不给长任务强制失败。未知请求保留requestId并GET恢复；不要自动重复POST。

### 4.4 前端测试

扩展现有 `juyiting-codex-fast-deliberation.test.js`、`juyiting-hall-conversation.test.js`；需要按钮真实状态时复用`juyiting-component-behavior.test.js`，不新建框架。

1. create Promise保持未resolve，完整GET确认COMPLETED后可发第二条；不是每个mock都onStreamEnd后立即返回。
2. 两次body conversationId相同、requestId不同，第一轮最终正文保留，POST计数精确2。
3. 部分turn已完+其他运行、RECOVERY_REQUIRED/UNKNOWN、空/不完整turns不得解锁。
4. FAILED/CANCELLED/混合终态释放锁，但不能显示为成功回答。
5. 正常EOF而请求非终态维持busy；EOF的终态GET失败不能自动重发。
6. 先GET终态后EOF、先EOF后GET、重复最终事件、重复readback都只收尾一次。
7. 旧stream late delta/error/end/finally不改新轮；话头A→B→A、登录切换同样隔离。
8. 已完成但正文GET失败，提示与业务状态分开；刷新后可恢复。
9. 断网受理未知、快速双击不重复POST；private固定对象、bounty typed路径不回归。

## 5. 最小切片（每项计划开发/定向自检窗口≤30分钟）

| 切片 | 交付 | 窗口 |
|---|---|---|
| D1 | 固定基线，新增前端开流终态/第二问失败用例与后端部分完成用例 | 20–30分钟 |
| D2 | 后端request有限流、buffer-before-read及资源close | 25–30分钟 |
| D3 | 后端Controller组合/竞态/独立订阅回归，确认无额外业务改动 | 20–30分钟 |
| D4 | 前端session归属及统一settle，终态主动收尾 | 25–30分钟 |
| D5 | EOF/未知/迟到/两问/组件状态回归，Owner自检 | 25–30分钟 |
| D6 | 组件集成、证据和发布准备，记录未覆盖项 | 15–25分钟 |

窗口是拆分目标不是已实测保证；正式构建/流水线等待、生产模型响应单独记录，不承诺包在某个30分钟切片内。可由同一Owner顺序完成；若并行，前后端独立路径各一Owner，先固定共同终态契约。

## 6. 验证/发布

- 前端先低成本定向诊断，正式测试/构建/同Run制品与部署走Flow4403172。
- 后端实施前读根/模块最新build.gradle，经`python3 ops/orchestration/cyf_orchestrator.py gradle ...`在固定干净源码上串行执行相关测试、依赖完整性、validateLayering及正式构建。
- 无DDL/DML/Runtime更新。授权发布时建议后端先部署、前端后部署，分别固定commit/tree/version/制品。顺序是现有两组件安装顺序，不增加旧协议兼容层。
- 生产验收另需在明确允许真实议事/模型调用的范围内执行：同一话头连续两问，第一问结束后第二问可发；核请求数、Agent终态、正文与上下文，不以制品上线代替业务通过。当前“写详设”不执行该操作。

## 7. 本轮不改变的语义

Agent回答完≠会话结束；请求结束≠清空历史；关闭POST reader≠取消Agent任务；会话events断开≠业务失败。用户在上一轮运行时不能并发发下一问；不加队列、不暗中取消旧任务。

## 8. 其他问题与图片状态（不并入本轮实现）

### 8.1 已确认前端问题

- 明确拒绝帧被当成conversation引用，可能丢草稿并停在SUBMITTING。
- public点名状态与对象chip/正文脱节，删除@文字仍可能路由旧对象。
- 未点名默认宋江，界面“众好汉”容易误导。以上详见首轮分析，独立修复。

### 8.2 图片：不能说从未跑通，也不能说当前版本完整验收

**历史真实PASS（2026-10-07）**：task424生成蓝鸟PNG，1370×1148，1513954 bytes，asset `ast_55c726d77f452bca372b806095f2696e`，SHA256 `faff63bfb5b87edfbc9d49a91ab114ea2fd52d6da4a7dcb9d7af962d568f1c5a`。预览、可选保存、工作空间重开、鉴权下载同摘要均有记录。

本轮实际读回的证据：
- `docs/implementation/evidence/t05-t09-business-closure-20261006/task424-media-after116-terminal-20261007.json`：原受理/typed action完成及真实页面图片入口。
- 同目录`task424-media-saved-image-download-20261007.json`：2026-10-07T05:27:40Z，HTTP200、1513954bytes、downloadSameBytes=true及上列摘要。
- 同目录`report.md:45–57`、`summary.json.completedSubsets`；特性入口`specs/juyiting-multimedia-deliberation/delivery-status.md`。本次只是核对原证据，不是新生成或新下载。

**历史未闭环**：task424图片和后来文字形成两个独立不可变根；后续“把蓝鸟改红、保留文字、一起验收”被交付范围歧义拦住。Web177复测实际0POST，不能冒充改图成功。依据同目录`task424-independent-roots-after177-root-cause-20261007.json`及`remaining-tasks-20261007.md:R01`。

**当前版本边界**：Web1.14.5、API1.14.3、统一Runtime aa6b96a与10月7日成功组合不同；本轮未查到绑定当前三端精确版本的新完整生图/改图/验收证据，未运行在线Provider。源码存在`ChatActionCapabilityService`→`ChatActionExecutionService`的generate-image/edit-image EXECUTE路径，Runtime打包清单包含controlled-image执行模块；存在代码/模块不证明现行配置/授权/Provider链有效。

普通厅内公议的`/chat/stream`和上述**任务绑定的自然议事→ACTION_REQUEST→EXECUTE→输出资产**不是同一受理链，不能用历史悬赏生图PASS推断厅内任意发一句就能生图；也不能把CHAT回答COMPLETED当图片OUTPUT_COMMITTED。

### 8.3 图片下一步最小验证（尚未执行）

用户已决定不打通历史流程，故不把task424两根恢复重列必做，也不继续在已取消的旧事项上重复生成。

1. 只读核对当前合法本人Agent的generate-image能力、绑定/租约/执行授权、provider配置存在性及实际启用状态，不输出密钥。
2. 明确授权真实生图后，用一个当前有效的新业务场景，走现有入口：需求→一次受理→action child→真实Provider→asset/output→预览/鉴权下载→单图验收；每步记录对应ID/版本/摘要。
3. 首图通过后，再单独验证改图（固定原图asset/revision/父请求）及是否保留原图/生成新版本；混合文字+图片整体交付另列用例。
4. 当前CHAT完成但EXECUTE缺失/失败：定位action capability、授权、outbox/Runtime、provider、上传/绑定中的实际失败层，不先补一套新生图API。
5. 判断口径：基础生图历史通过；当前端到端待验；历史混合改图/验收缺口保留历史事实，不升级为所有新图片流程必定失败。
