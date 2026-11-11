# 聚义厅办事流程：2026-10-08 独立后台浏览器重新实测

## 结论

**FAIL_NEW_PLAINTEXT_FLOW_BOOTSTRAP_BLOCKED。当前新建纯文字事项没有跑通，不再沿用“纯文字已通、只差UI”的历史判断。**

正常登录测试账号 chcbz，真实 Chromium 133，390×844 手机视口。通过原生鼠标/键盘操作正式页面；没有 mock、没有直接 API 业务写、没有数据库修正。本轮只创建一个新事项429；旧事项426、424仅用于当前只读页面复核，绝不算新流程成功。

## 当前版本与证据

- Web 1.0.6 / Flow4403172 Run180 / `ee6ca1b6beba562e0c7fa13d422857f554644471`。当前浏览器加载的入口与聚义厅、主入口 JS/CSS 共5项公网字节均与主机安装manifest一致。
- API Flow5260799 Run117 / `49fe947d1b3b61d9419b7b599bc5c58d445c5953`。正式 JAR SHA256 与安装记录相符；当前进程PID6965，启动时间2026-10-08 00:08:09，cwd为 `/home/isp/hosts/cyf/api`。
- 这是本轮实时安装记录/指定资产核对，不冒充重跑Flow、全制品验真或新版本发布。见 [current-runtime-baseline.json](current-runtime-baseline.json)。
- 正常登录后通过个人中心页面核对账号chcbz、用户编号5。密码仅用于登录输入，不写入脚本、报告、截图或网络请求正文；认证头和Cookie不采集。

## 一、新建事项429：真实执行结果

时间均为北京时间2026-10-08。

| 环节 | 本轮实际结果 | 证据 |
|---|---|---|
| 01:13:31 创建 | 一次“开始办事”，HTTP201、COMMITTED，task429/version0，无附件、reward/funding均null | task-429-create-receipt.json、02-created.json/png |
| 01:14:52 点将 | 一次“点将并议事”，HTTP200；公孙胜，assignmentRevision1/taskVersion1；grant ACTIVE | task-429-point-receipt.json |
| 自动建立议事 | **没有完成**：bootstrap PENDING/stateVersion0，conversationId和initialRequestId均null；页面仍在点将册 | 05-pointed-chat.json/png、06-bootstrap-still-pending.json/png |
| 查看进展 | 手动关闭点将册→首页新事项“查看进展”；详情显示“正在准备会话”“准备完成后即可继续交流” | 08-open-new-progress.json/png |
| 手动进入该事项议事 | 空会话视图，“此榜文尚无议事记录”；预填默认议事草稿。未发送第二份需求，不以手动重发掩盖首轮未接续 | 09-enter-new-discussion.json/png |
| 查看成果 | 没有新正式交付；未进入验收。首次截图仍有读取中提示，不能把该瞬时提示单独判断为故障 | 10-new-results-before-bootstrap.json/png、实际deliverables/formal-deliveries网络回执 |
| 刷新与最终核对 | 刷新后仍assigned；01:28:31原点将只读查询仍PENDING、两个ID仍null | 17-new-task-final-check.json/png、18-final-bootstrap-readback.json/png、task-429-last-bootstrap.json |

点将到最终查询的观察跨度 **819.661秒（约13分40秒）**。这只是本轮观察区间，不是新设性能门槛或超时失败规则。真正的阻断依据是未生成首轮请求及下述接续组件停止日志，而不是“超过某个等待时限”。

连续浏览器网络记录确认：创建POST 1次、点将POST 1次、finalization POST 0次、chat/stream POST 0次、interactions POST 0次。共捕获207个原点将GET响应，其中主要是页面自身约1秒一次的轮询；没有脚本循环重复业务POST。list/search/recommend等查询型POST不算业务重复执行。原键由页面管理，脚本不提取认证信息，也不制造新键重试。

## 二、当前直接阻断点：后台议事接续已停

同一当前API进程PID6965日志明确记录：

- 00:09:01.551：bootstrap admission failed；异常为 `Typed deliberation schema is unavailable`。
- 00:09:02.673：再次出现同样的准入异常。
- 00:09:02.767：`Bounty bootstrap relay stopped after repeated unchanged failure`。

见 [bootstrap-log-extract.json](bootstrap-log-extract.json)，来源为当前正式 `/home/isp/hosts/cyf/api/logs/root.log`，带原始行号。**这些失败发生在新建429之前，不声称429触发了启动异常。** 当前任务PENDING与该进程接续停止日志一致。

对应已安装源码：
- `ChatBountyBootstrapRelay` 为SmartLifecycle，启动后立即轮询；同签名异常两次即stop，无此类停止后的自动恢复逻辑。
- `ChatTypedDeliberationSchemaInitializer` 通过ApplicationRunner完成初始化，ready初始为false。
- `ChatTypedDeliberationContextService.resolve` 在未启用或schema未ready时抛出上述异常。当前配置文件中的typed-deliberation与bounty-bootstrap开关均true。

**修复方向（推断，尚未实施）：先核对并修复启动就绪顺序/接续生命周期，避免暂未就绪被当成永久失败停机。** 这不等于已证明数据库缺表，也不等于当前schema始终不可用；不能靠关掉ACL/锁/幂等/真实失败保护来“跑通”。本轮未重启服务、未改配置、未修改生产数据，也没有绕过原点将链路强行发新议事。

## 三、旧问题的本轮复核，不混用历史PASS

| ID | 本轮结论 | 事实与范围 |
|---|---|---|
| SF01 返回绕行 | **原路径未能重测** | 自动点将后议事没打开，无法重做该路径返回。手动“事项详情→议事→返回”可以回详情，但不等于原自动路径已修复。 |
| SF02 首页状态陈旧 | **本轮复现点将子项** | 429服务端assigned/version1、公孙胜；首页仍“待领令/待安排”，全页刷新后变“已领令/公孙胜”。新验收后刷新子项未到达。见07与11。 |
| SF03 成功草稿未清空 | **本轮复现** | 429创建COMMITTED后首页仍保留98字原需求；全页刷新后为0。见02、07、11。 |
| SF04 完成态/动作恢复错误 | **当前旧完成记录只读复现** | 本轮GET426仍completed/version4；成果页仍显示启用的“确认验收”“继续修改”；议事输入、资料、录音入口也未禁用。未点击验收/修改/发送，不推断服务端会接受重复操作。见12、13、14及task-426-readback.json。 |
| SF05 同一需求重复显示 | **当前旧消息可见复现** | 426同一个USER气泡内两段完整重复需求，截图13可见；这不证明重复请求或重复Agent调用。 |
| R01 图文成果范围不明确 | **当前旧混合记录只读复现** | 424同会话仍可见图片与两行文字，成果页显示“本次交付范围尚不明确”，没有确认验收按钮。见15、16及task-424-readback.json。没有重新生成、修改、合并或验收该事项，不冒充新的图文业务闭环。 |

## 四、不增加功能的处理顺序

1. **先修现有点将→议事首轮的后台接续**：就绪后消费原意图，保持同scope、原键、原任务，不重复建事项或重复执行。发布后用429核对原意图恢复，再按授权补新事项端到端回归。
2. **修完成事实投影及动作约束**：各页面读同一服务端任务/验收终态，刷新只查询，已完成项不再提示重新验收或改稿；新浏览器没有本地验收intent也应呈现服务端完成事实。
3. **修首页刷新、成功草稿清理和正文拼接**：复用现有回执、查询与页面，不增新面板。
4. **修现有图文成果范围衔接**：沿既有明确来源/selectedOutputs契约处理，不自动拼接所有历史、不重写原final、不建设新的交付集合系统。
5. 修复后重做真正的“创建→点将→首轮答复→正式成果→验收→刷新”业务验收，再补自动返回路径、多媒体、异常恢复与隔离。不能用既有426已完成代替新事项429通过。

## 边界、诊断失败与现场保留

- 未验证：新Agent答复、交付、验收；新图文生成/单项修改；附件-only/自然澄清；真实麦克风；跨账号；真机键盘及断网故障注入。这些是NOT_RUN/BLOCKED，不宣称功能不存在或测试PASS。
- 首次浏览器驱动宿主会话退出，未做任何业务写；改为独立PTY宿主后重新正常登录，整个429业务段在同一稳定浏览器完成。部分原生点击因文本选择器或转场遮挡未命中，之后读取实际DOM定位；这些诊断动作不当产品失败。
- 完成只读页面取样后关闭本轮自有浏览器并清理临时profile；PID98805/98812已退出，不操作其他聊天浏览器或服务。
- 新事项429保留assigned/PENDING，不删除、归档、取消或伪造终态。后端恢复后可能继续处理原意图，避免另发一份。
- 报告文件仅为本轮测试证据；不修改现有组件代码/根gitlinks、既有运行ledger或其他Owner证据。

完整索引：[summary.json](summary.json)、[actions.jsonl](actions.jsonl)、[network.jsonl](network.jsonl)、[business-responses.jsonl](business-responses.jsonl)。时间戳原始JSON使用UTC，本文统一转换为Asia/Shanghai。
