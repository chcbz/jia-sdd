# 正式悬赏全流程 bugfix 需求（2026-09-23）

状态：**draft / 1.13.19 planned / solution_defined / 尚未实施**。已按用户要求新增 bugfix 版本与修复方案；不修改应用代码、不构建、不发布。

版本方案：`docs/implementation/V1_13_19_FORMAL_FLOW_BUGFIX_PLAN_20260923.md`；结构化登记：`version-plan.yaml`。前次移动复测结果保留如下，不视为新版本验收。

## 目标与结论

在同一正式 taskId 上打通：提出需求 → 添加固定版本资料 → 点将吴用/林冲 → 榜文议事 → 实际执行 → 正式提交可验证交付件 → 用户验收/返工 → 完成/归档。

本轮正式任务 **#395「吴用竖屏闭环复测-0923-1600」**，仅指派吴用。草稿创建、资料上传、指派记录成功；派发与议事失败，未执行到正式交付/验收/闭环。不能宣称“最新版 Agent 已跑通”。

证据目录：`deliverables/verification/juyiting-formal-flow-wuyong-20260923/`，索引及摘要见 `manifest.json`。完整矩阵见 `acceptance.md`。

## BF-01 / P1：点将成功不等于命令送达，失败原因未呈现

- 复现：创建 #395 → 点“点 吴用 领令”一次。
- 实际：HTTP 200，任务 assigned；同响应 actionDispatchResults[0] 为 queued，message=`Agent offline, outside scope, or not a task member`，dispatchedAt=null。页面只显示“已点将”；后续 GET 又返回 actionDispatchResults=null，无法从详情恢复派发事实。吴用同时被名册标为 online/canOperate。
- 证据：`assign-receipt.json`、`17-assigned-wuyong-confirmed.png`、`read-only-probes.json`。
- 要求：区分指派成功、派发待处理、已接收和实际开工；合法 owner/client/tenant/member 范围的目标可收到命令；失败保留可恢复的精确分类和最近事件，刷新不丢失。自动恢复必须有持久化命令事实与幂等，不能把内存拒发伪称可靠排队。
- 验收：实际 Agent 收到同 commandId，合法领取/开工后更新业务事实；模拟断线、无成员、错作用域，分别拒绝/排队并可解释。不得移除 ACL 以“修通”。
- 根因：未完成运行时归因。源码中 task tenant=0 与会话 owner/jiacn 使用方式、成员解析/邀请状态值得优先核对；不能把混合错误文案当作已证明某一原因。

## BF-02 / P1：已点将榜文议事无法建立/发送

- 复现：#395 → 进入议事 → @吴用发送实际办理请求；再通过“另起话头”改变会话入口后发送一次。
- 实际：两次 POST `/chat/stream` 都返回 404，code=`CONVERSATION_NOT_FOUND`，message=`Conversation is not available`；页面仅提示“传令未达，请稍后再试”。未继续盲目重复。
- 证据：`discussion-error.json`、`fresh-discussion-error.json`、`20-discussion-response.png`、`25-fresh-discussion-result.png`。
- 要求：合法任务所有者与领令成员能创建/恢复任务讨论并实际送达；新话头不能继续引用失效会话。若使用受保护 task-thread 协议，接入正确受权入口，不解除通用聊天隔离。
- 验收：首次、新话头、刷新恢复均可发送且回话仍绑定 #395；跨 owner/client/非成员负例仍被拒绝；后端细分可诊断原因，前端不让用户无意义反复发送。
- 根因：404 也可能是任务作用域授权失败，不等同于单纯 conversationId 不存在。现有 ChatController 会把相关授权异常映射为此错误，需测量真实分支。

## BF-03 / P1 功能缺口：正式任务没有贯通固定版本选材与授权

- 复现：首页“提出需求”只进入私人交办；转至“起草正式任务”只接受标题/简述，不接收附件；任务详情“打开百宝箱”可上传文件，但没有完成“用于本任务”的确认动作。
- 实际：资料 `pws_56597b2fe5a84cbcace77ac4d2eafe91` v1 已上传，只在个人文件库，未与 #395 建立已验证关联。将资料正文写进榜文只是继续诊断的替代输入，不算附件步骤通过。
- 要求：需求入口明确私人/正式业务边界；正式任务提供选固定版本→预览→确认用途与权限→关联原 taskId 的路径。禁止以同名私人交办替换正式任务；单纯提文件名或上传不算授权。
- 验收：只从授权附件读取独有标记 `MATERIAL-WY-395-A`，交付文件包含该标记，任务可反查输入 fileId/version；其他未选文件不可访问；升级文件最新版本不得悄悄改变本次输入。
- 性质：现有 TASK_CREATE 刻意为仅创建任务入口，此项是用户所需全流程的集成缺口，不把未承诺的创建能力说成接口偶发故障。

## BF-04 / P2：深层百宝箱把文件“查看”全部禁用，无当前页说明

- 复现：悬赏榜 → #395 详情 → 百宝箱 → 上传测试资料完成 → 返回资料列表。
- 实际：上传已 COMMITTED，文件在列表，所有“查看”按钮仍 disabled；本次页面没有解释如何回到可查看层。不是上传失败或仍在加载。
- 证据：`14-upload-committed-view-disabled.png`；源码 PersonalWorkspace 的 detailAllowed 绑定、JuyiHall 的 panelDepth<3。
- 要求：业务需要的文件详情不被机械导航层数阻断；使用同层替换、局部子视图或可解释返回路径，保留原任务、滚动与选择。
- 验收：430×932 下按同路径上传后可预览固定版本并返回原任务；不增加无限嵌套，不为通过测试把 disabled 直接移除绕过安全边界。

## BF-05 / P1：正式任务工作空间与事件不可用

- 复现：同一登录身份、taskId=395、actorAgentId=吴用，读取工作空间和事件。
- 实际：`/agent/tasks/395/workspace` → 503 TASK_WORKSPACE_UNAVAILABLE；`/agent/tasks/395/events` → 503 TASK_EVENTS_UNAVAILABLE。
- 证据：`read-only-probes.json`。本次参数符合 Controller 契约。
- 要求：核对环境开关、依赖、作用域与真实快照错误；功能若未启用，应由能力响应显式说明和限制入口，而不是允许用户进入承诺完整办理的流程后再静默断路。
- 验收：有效身份可读取真实状态/事件并重放恢复；未授权仍不可读；不能通过吞错返回空列表伪造健康。慢请求不按任意性能阈值失败。

## BF-06 / P1：主状态显示不完整，完成依据混淆

- 证据类别：本轮实际榜单仍为 6 个筛选项；结合前序源码审计，后端 10 态，planning/reviewing/blocked/cancelled 回落“待点将”。未在生产伪造这些状态来造测试通过。
- 要求：集中完整映射与筛选，未知状态显示待核对；assigned 为待开工、running 为办理中并展示子阶段、reviewing 为待验收、completed 为已完成。“交令”保留为提交动作。
- 验收：10 态及未知态表驱动测试；正式 accepted 与 legacy completed、资金预览完成区别展示；私人“已查看/收入案卷”不改变正式验收事实。

## 下游待验收，不冒充已确认缺陷

实际开工、Provider 执行、正式提交、PDF 下载、accepted、返工新 revision、完成及归档均被上游阻塞。实施需把这些列为必须验收项，不能因源码已有端点而勾选通过，也不能凭本轮未到达就断言其全部实现缺失。

普通密议对照曾出现“已递到”后通用失败，未取得可验证的本次最终回复；仅列后续诊断项，不能用其替代正式悬赏证据，也不把等待时间作为失败判据。

## 非目标与安全边界

- 不做资金冻结/支付/结算，不动 #394，不使用扈三娘；不操作其他任务的 Agent/Gradle/systemd 进程。
- 不批量回填历史状态，不新建平行状态机，不通过手动 report/DML/伪造验收制造闭环。
- 外部 Provider 测试沿用用户已明确的费用授权，但本轮未核验是否实际调用或产生费用；不能报告零费用。
- 本轮仅需求、版本方案与既有测试记录，未实现修复、未部署；后续发布仍按用户本地构建授权、exact SHA/测试/制品摘要/健康证据执行。

## 2026-09-23 上线后新增缺陷（原 1.13.19 历史方案保持不变）

- **BF-07 / P0 交付事实失真**：#396 在点将吴用后，legacy report 将 `wi_legacy_*` 工作项和主任务直接置为 completed；该 taskId 的正式交付 `items=[]`，没有 PDF、submitted、用户 accepted。必须阻止正式 TASK_CREATE 来源在无正式提交/用户决策时被 legacy report 聚合成 completed，且不影响旧版真正 legacy 任务；测试需覆盖不同 owner/client、幂等/CAS/lease 与已存在不一致历史事实。不得直接重写 #396 生产数据来做出通过。
- **BF-08 / P1 议事结果未知**：同一 #396 的 `/chat/stream` 先 200 后出现 `net::ERR_HTTP2_PROTOCOL_ERROR`，页面报传令未达，无可验证的最终吴用答复。先以原 conversationId 和事件游标核对受理及恢复协议，避免重复投递/付费；不能仅以 HTTP 200 或 legacy completed 判议事成功。
- **BF-03 回执契约增量**：生产浏览器中精确关联 POST 201 却因跨域不可读 ETag 报失败；隔离的后续只读 GET 确认已存一条 ACTIVE INPUT。API 候选 `bc8a07974f2efdc077b865da11f9721a257c7e7d`（仅可信来源暴露 ETag，CorsConfigTest 定向通过）；Web 候选 `a689b2d300206041ab2820b985d8e1b792830da9`（不可见 ETag 时只读回查、不重发 POST/DELETE，7 个定向测试通过）。**这两个新增候选均未合入已部署 1.13.19 制品、未再次构建/部署，也不能解决 BF-07/08。**

增量事实与证据见 `acceptance.md` 21:25 CST 补充。原文顶部“计划/尚未实施”是建版当时历史状态，不能作为 21:25 现状；当前 1.13.19 已部署健康但业务验收失败。用户给出的即刻发布例外已用于原 1.13.19 上线，不自动为后续新版本免除时段、测试和健康条件。

## BF-09 / P1：权威快照已到，但等待空闲 SSE 导致正式办理不可用（1.13.21 Web patch）
- 线上1.13.20新任务#397证据：文件固定版本关联201无ETag误报；吴用指派已送达；原会话1760458004739先返回明确busy，等任务简报结束后新议事收到已递到及真实最终确认。主状态仍assigned，没有被legacy报告越过正式交付自动完成。
- 当前阻塞：GET workspace 200且唯一required ready项已验证，GET events在没有新事件时约30秒才返回200空体；前端仅onStreamOpen转live，整个等待期间误留loading，正式执行范围拒绝。证据`deliverables/verification/juyiting-formal-flow-1.13.20/mobile-portrait-20260924/07-*`与`task397-event-stream-bodies.jsonl`。
- 最小修复：validated snapshot后使用独立snapshot_ready连接状态，不谎报实时连接；仅同身份/任务/明确已指派Agent及唯一ready必需工作项才可显式发起原正式执行，服务端仍核验ACL/CAS。loading/错误/503/不匹配继续拒绝。不得通过API绕开UI替代验收。
- API不变、不再次发布后端；前端冻结新的release/1.13.21，不移动release/1.13.20。SSE服务端空闲超时/初始flush单列待优化，本次不放宽权限或编造实时成功。


## 1.13.22 增量缺陷（服务器观测 2026-09-24 01:48 +08:00）

- **BF-10 / P1 注册慢回执导致文件通道永久不就绪**：runtime `RegistrationAckObserver` 在10秒观测计时器触发后清掉当前 messageId，后续同 socket、同 agent/runtime/messageId 的合法 ACK 也永远拒绝，文件 poller 因无运行时凭据不启动。定向回归先复现4项失败；最小修复保留当前请求相关性、接受严格匹配的迟到 ACK，新注册/断线/发送失败/明确拒绝仍使旧回执失效。该缺陷已由代码与测试确认；生产注册日志不含 profile，**尚不能断言其是 #397 未拾取的唯一原因**。
- **BF-11 / P1 过期 TASK 执行缺少安全恢复**：#397 的执行仍 QUEUED，workItem leaseUntil 已过、仍 running，formal-deliveries 空。runtimeDispatchAllowed 会拒绝过期租约；owner revoke 调用仅接受活租约的 release；expireLeases 尚无生产调用入口。修复必须有精确 execution/task/workItem 的 owner 显式撤销/过期回收，保留 token/version CAS 与任务根优先锁序；不得扫描改动其他任务、延期复活旧租约、自动重跑付费任务或写库改状态。当前仅完成方案，未修改生产数据。
- **BF-12 / P1 主任务与执行阶段不一致**：#397 的主任务 assigned/startedAt=null，而创建执行已经生成 WORK_ITEM_STARTED，工作项 running。须分离服务端排队/Agent 实际接收或开工，权威事件驱动主状态和开始时间；不能为消除显示差异而把 QUEUED 描绘为 Provider 已运行。新增状态流转和延迟拾取回归后再部署。

1.13.22 尚未部署。#397 保留原执行，不新建榜文规避失败；PDF、返工、验收、归档仍未通过。

### 2026-09-24 实证新增 BF-13 / BF-14
- **BF-13 / P1 撤销后的正式办理误阻断**：撤销精确租约后required工作项ready且assignee=null是合法服务端状态；前端仅在同身份/任务/唯一点将/正式会话范围允许唯一该状态工作项，仍拒绝缺字段、外部承办人及多项歧义。Web1.13.23已发布并真实新执行成功。
- **BF-14 / P1 正式交付存储缺配置**：#397 PDF上传201后正式提交503，runtime明确FAILED、无正式交付；线上task-artifact-storage缺开关导致Disabled实现。1.13.24配置修复必须保留私有目录权限、默认MIME和尺寸、原配置可恢复、exact JAR及真实健康核验。单测通过不等于正式交付恢复；不得将本地PDF当交付件，不重试未知commit。
