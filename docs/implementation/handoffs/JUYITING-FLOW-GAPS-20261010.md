# 聚义厅流程缺口复核（2026-10-10，赠款需求暂存后接续）

## 本轮范围、状态和源码

- 用户要求：先保存新用户2000赠款详设为待完成事项，再继续查看聚义厅流程缺口。Owner：主控（只读诊断及文档）；未派发开发Agent，不新增功能范围。
- 赠款待办保存于 `/home/isp/wsps/cyf/docs/implementation/NEW-USER-2000-GRANT-DESIGN-20261010.md`，钱包隔离按client+tenant+user；钱包身份不可依赖领取表的职责修订尚待完成。本轮不实施赠款、不补款。
- 23:13 CST只读`git ls-remote origin refs/heads/develop`：三个组件本地HEAD均与查询时远端develop相同、tracked clean。API `/home/isp/wsps/cyf/api`：`33e2344a2af02bb908a20bec1125ab7c23e8d00d` / tree `0a9b387e69e3d275f6185b953b9c1851a6469118`；Web `/home/isp/wsps/cyf/web`：`17ecf1c0b581cab1456acff4db097a6a4d335e3d` / tree `101daa30ed9658949dcc9b1d4cccfb2e4d2ce539`；Runtime `/home/isp/wsps/chcbz/isp-install`：`80eadc9247132a9d6c6b3b9d7fe7b7f965e094de` / tree `ac7ffd578f1a719071be6cb0ce3d3bdc0022c841`。本轮无受测发布候选，也没有重新校验当前线上API JAR/Web制品摘要。
- 根仓已有TASKS.yaml、juyiting-runbook.md、web gitlink修改保留；不改其他会话文件或运行任务。
- 本轮检查是**源码对照 + 本地纯函数诊断 + 当前Runtime只读日志/进程观测 + 历史验收证据回读**，不是新的整站浏览器实测、正式Flow/Gradle测试或生产办理验收。
- 原始证据：`/var/tmp/cyf-flow-gap-review-20261010-s4k07zsa/`，含baseline.json、source-digests.json、local-diagnostic.mjs/json、runtime-observation.json。实际Node v20.20.2仅记录，不设版本门禁。首次基线采集误用Python3.6不支持的subprocess text参数，在任何远端查询前失败；改为universal_newlines后采集成功，不改解释器。

## 一、已成立的历史闭环，不重复列为未开发

| 流程 | 已有证据 | 不可扩大解释 |
|---|---|---|
| 吴用435、林冲436：新事项→议事执行→正式成果→验收→刷新回读 | 2026-10-09 Web1.14.1验收记录；6次回执GET、0次验收POST | 非本次新运行，不代表新托管公孙胜使用其独立Provider也已完成推理 |
| 六个普通未开工任务取消→释放占用 | 2026-10-10 GSS-CANCEL后端发布/生产结果 | 无前端取消入口；不是运行中任务强停 |
| 公孙胜旧绑定除名→新初租原单续办→统一Runtime注册 | 2026-10-10 10:59验收：原lease ACTIVE，RESERVE/CAPTURE各一笔 | 除名发生于旧绑定；不能视为新native绑定再次除名的生命周期验收 |
| 公孙胜免费重整 | 同installation、session1→2；租期/钱包/账本未变、其他三个subject未重启 | 证明接应服务就绪，不是模型推理或完整新事项交付 |

来源：`/home/isp/wsps/cyf/docs/implementation/handoffs/GSS-CANCEL-20261010.md`、`/home/isp/wsps/cyf/docs/implementation/handoffs/GSS-REJOIN-20261010.md`、`/home/isp/wsps/cyf/docs/implementation/UR06_REQUIRED_RUNTIME_CLOSEOUT_DESIGN_20261009.md`；本轮实际回读 `/var/tmp/cyf-gss-hosting-acceptance-20261010-dbXw9l/summary.json` 与 `/var/tmp/cyf-ur06-finalization-fix-20261009/browser-acceptance.json`。

## 二、已确认的实现/页面缺口

### F01 普通任务取消没有页面接线

- 后端已有 `POST /agent/tasks/{taskId}/cancel`，body仅整数expectedTaskVersion；支持普通、无资金事实、未实际开始任务。来源 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskCancellationController.java:33–67`；限制在 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskCancellationServiceImpl.java:60–66,82–113`。
- 当前Web源码搜索未见普通任务cancel API调用；`/home/isp/wsps/cyf/web/src/composables/juyiting/useHallTaskActions.js:383–409`只调用funding/cancel；`/home/isp/wsps/cyf/web/src/components/juyiting/BountyPanel.vue:280–290`只给资金榜文提供开工前撤榜退款按钮。
- 用户影响：普通事项不想继续时，无法从现页面完成“取消→解除任务占用→允许除名”，仍需人工调后端接口。这是已有能力接线缺口，不是需要再造取消API。
- 最小修复建议（未实施）：在现事项详情接普通取消动作；保持所有权与任务版本校验，提交后回读task/roster/catalog；只给支持范围提供入口。响应丢失先GET核对原task，不把409或未知结果显示成成功。funding取消保留原资金语义，不走普通接口绕退款。

### F02 已取消事项在简版详情误显示“已受理”

- `/home/isp/wsps/cyf/web/src/components/juyiting/BountyPanel.vue:617`的simpleMatterStatus遗漏cancelled，fallback只看保留的assignedAgentIds；该函数用于同文件225行“办理建议”。通用状态表 `/home/isp/wsps/cyf/web/src/constants/juyiting.js:28`已有“已取消”，因此不是后端没返回状态，而是局部展示分叉。
- **本地真实源码函数诊断已复现**：cancelled+有原指派→“已受理”；cancelled+无指派→“状态待核对”；completed对照→“已完成”。输入为合成对象，不是新浏览器实测。
- 同文件236行议事按钮只看assignedAgentForTask；591–594行仅检查指派与operableAgents，未判断任务终态。需区分“查看历史”和“继续办理”的入口；不能凭此断言后端允许取消后继续执行。
- 最小修复建议（未实施）：统一终态映射，cancelled显示“已取消”；按实际后端契约收敛终态动作，历史成果保留只读。补有/无原指派、刷新重开、取消后不再显示待办动作的用例。不删除历史指派来掩盖展示问题。

### F03 除名入口没有交代现有租约后果

- `/home/isp/wsps/cyf/web/src/components/juyiting/PersonaCatalogPanel.vue:138–145`直接emit；`/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue:2664–2679`直接unbind，未读取剩余租期或给出财务后果确认。
- 原GSS验收明确：旧租约不会自动转移到新的绑定，重新入伙重新报价；已有租约的故障接应可走免费重整。当前页面容易让用户把“除名再请回”当成免费重整。
- 最小建议：在现入口明确区分免费重整与解除绑定，并呈现现租约处理后果；**不因此增加退租退款/租期迁移功能**。这是页面告知缺口，不等于正常新任务执行阻塞。

## 三、待验证项，不提前判成已确认的办理失败

### V01 新托管公孙胜的真实新事项交付

现有GSS summary明确排除新任务及真实Provider推理。下一次必要业务验证应是一个新事项：点将公孙胜→收到实际模型答复→按需要执行→产生可读成果→确认验收→刷新回执。沿用其当前installation与现有租约，不再次除名、重新初租或补款；不验其他账号的卢俊义。

这是**验收证据缺口，不是已证实需要开发**。本轮未创建任务、发送推理或消费资金；执行前按实际业务授权核对Provider/扣费范围。

### V02 当前Runtime仍有MESSAGE_TYPE_REQUIRED

- 2026-10-10 22:55–23:14:59 CST有界读取日志162条，均为该拒绝码；服务仍active/running，PID1654189、NRestarts0。不得据此认定162次新任务失败，日志未记录被拒原始frame/type/业务关联。
- 源码可复现的一条不匹配路径：API `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java:1039–1044`发agent_status_updated；copyTrace1749起不复制messageType，sendEvent1790起只写type/channel/timestamp。
- `/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:105–111`分流connected/agent_registered/ping/command.ack，但未分流agent_status_updated；进入既有agent-client.mjs:393–396后因缺messageType拒绝。实际导入normalizeInboundMessage，以合成agent_status_updated事件复现同拒绝码；**还不能把全部线上日志逐条归因为此事件**。
- 下一动作：精确确认当前控制回执路由/事件关联，若影响新办理则修最早断点；即便只属控制回执误报，也应在原adapter明确其消费职责。不全局放宽业务消息必填校验、不恢复旧协议fallback，不新建监控系统。

### V03 新native托管绑定的除名回收边界

新入伙/重整走统一Runtime；现DELETE入口仍在 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentController.java:244–246`委托AgentPersonaProvisioningService.unbind。该类39–54行仍包含旧hosted publisher路径；AgentHostedBindingTransaction.prepareUnbind在202–205行无hosted时仅suspendDatabase并发布offline，282–310行为binding/identity/runtime投影变更。

本轮只确认了代码路径，尚未核完native身份停用如何传至installation、session和subject回收；不能据此声称越权继续执行或除名失败。此前除名发生于旧绑定，未覆盖当前新托管再次除名。此项保留生命周期验收缺口，不在本轮擅自再次除名公孙胜；若先推进正常新事项，不将它扩成运行安全专项前置。

## 四、不应混入本轮必做的事项

- 新用户2000资金：按用户要求待完成，不实施、不用手工补款假装自动化已完成。
- 运行中任务整体取消：初步接口明确不支持，ChatPanel“取消待处理回话”仅为回话层，不等于任务根取消。列为范围边界；不擅自扩成强停/退款/全流程取消系统。
- 多业务区域：三元组目标已确认，但当前取消Controller仍只接受tenant=0，其他入口也存在单区域约束；这说明全站多区域未完成，不代表当前已启用区域不能办理。不能只改赠款表后宣称全部多区域可用。
- 旧事项432、历史流程补报、旧版本兼容、跨账号卢俊义验收均不回到本轮范围。

## 五、建议接续顺序与完成口径

1. 优先补齐新托管公孙胜的一次真实新事项闭环证据；定位最早实际断点，不因注册成功宣称推理/交付已通，也不先重建检查框架。
2. 将F01普通取消页面接线与F02取消终态展示作为同一前端收口范围；保持后端现有支持边界，无需新增取消接口。
3. F03租约后果说明可作为同范围文案/交互修正；V02精确定位控制回执，V03按实际用户生命周期需要补验，不随意强杀/重启共享Runtime。
4. 当前无开发Agent在执行上述新任务；本轮只保存两份文档和诊断证据。业务代码未修改，没有Gradle/Flow、DDL/DML、服务控制、生产任务创建或新的推理消费。
