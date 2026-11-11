# 办事/议事及新用户接外单正常场景回归（2026-10-27）

- Owner：当前主会话；任务标识 BUSINESS-NORMAL-20261027。
- 用户授权：跑完正常场景首轮，统一汇总问题、修复并回归直至通过；仅相关修复发布，不自动发布无关develop内容。
- 范围：既有测试规格N01–N25、X01–X12共37条，优先无自有Agent新用户委派吴用。非目标：异常注入、断网/丢ACK、攻击/并发压测、岗位、OOM、已暂停的技能启停性能专项。
- 依据：根/web AGENTS；统一接口规范api/docs/interface-standard.md v1.4；ops/orchestration/README.md；外单D3.1及唯一原型。共享技能中自动develop部署旧口径由根规则覆盖。
- 测试账号：用户指定chcbz、ziyue，确认复用同一密码；密码仅运行时读取安全配置，不落代码/报告。真实登录生产页面，不用离线原型模拟业务结果。
- 复用既有browser.mjs/CDP，在任务私有目录分开两个登录上下文，不动用户共享原型。截图/DOM只保存在0700任务目录。既有工作区脏内容不改动或reset。
- 本地HEAD/tree/branch及远端develop查询分开保存在 /home/isp/state/cyf-business-normal-20261027/baseline.json；线上API/Runtime安装记录仅证明安装历史，当前业务另核验，Web版本待核对。
- 最早验证：chcbz真实登录成功，页面创建专属测试事项534，待点将。未写用户原事项。接着登录ziyue核对零自有Agent条件及吴用开放状态。
- 测试规格：specs/juyiting-unified-experience/business-discussion-test-cases-20261027.md；首轮结果仍待执行，不沿用历史PASS。
- 时间：定位/实施/验证/等待暂未分项采集；尚无本任务源码修改、构建或部署。

## 首轮正常页面阻断与修复候选

- 两账号真实登录成功。chcbz事项534、ziyue事项535均由页面新建；535候选可选择“吴用/其他用户”，确认走原委派按钮。ziyue实际名册含卢俊义且有历史事项，因此严格零Agent/全新用户前置不满足，不删除现有Agent，不声称该样本已覆盖。
- BUG01：确认承办后长期“正在准备议事”。534 01:22:15确认，01:27:33仍未进入；535 01:26:53确认亦PENDING。页面自然GET回执均grant ACTIVE、bootstrap PENDING/version0，conversationId/initialRequestId为空。证据任务目录browser/point-status-534.json、ziyue/point-status-535.json及截图。
- 归因证据：API原进程34366在2026-10-26 21:15–21:16遭遇数据库连接不可用（CommunicationsException、SQLTransientConnectionException），ChatBountyBootstrapRelay连续两次同类故障后永久stop；之后数据库恢复、页面创建成功，但全局首轮消费者未恢复。不是本轮制造异常，不是用户缺Agent/岗位/安装权限。日志摘要bootstrap-stop.log。
- 最小修复仅在获得outbox claim之前识别临时数据库异常，沿既有outbox 1秒→300秒恢复退避范围继续获取持久claim；不对Chat/Provider调用增加重放，不修改schema/身份/授权/租约/幂等。语义、授权、schema及未知证据错误仍保持关闭保护。该退避不是请求超时/拒绝门槛。新增精确回归覆盖恢复、退避、停止/重新启动与保护边界。
- 主api工作区HEAD516267b且有他人规则改动；唯一必要隔离工作区/home/isp/wsps/worktrees/business-normal-api-20261027，分支codex/business-normal-20261027，从线上/当时远端28700cc0固定构建。显式携带根AGENTS及接口规范v1.4，组件旧v1.2/低版本拒绝口径不覆盖最新根规则。
- 代码候选尚未验证/发布。浏览器仍只测正常场景，不做生产故障注入；为已复现问题补的代码回归不算页面业务通过。先恢复这个共同阻断再继续其依赖用例，不用反复点将制造新任务。

## 2026-10-27 07:58 接续核验

- 实时核对API332（候选6dbb9cfe）：FAIL。与API331分支限制不同，本次实际进入Gradle；同Run诊断绑定源码，`ChatBountyBootstrapRelay.java:74` 的final clock未初始化，构造器缺少测试所需的可注入时钟重载。不能将本轮误报为测试通过。
- 复用原唯一工作区，补齐四参数构造器委托系统时钟、五参数构造器初始化时钟；候选86f8ed1da1c9f4d9a6a99aedc7e330aa21034d62/tree5916e64d677aec2725559ffdbfc0c7b09224e210。diff检查通过，远端develop原为6dbb9cfe，普通快进推送；不触碰主api脏修改。
- 已启动API5260799/333固定新候选的CI-only测试/构建，无部署；设置本任务570秒受控取消监控（总Run上限600秒）。启动回执早期SOURCE尚空，保留UNKNOWN并只读确认，不重复启动。证据 /home/isp/state/cyf-business-normal-20261027/ci-clock-fix/。332诊断与日志在ci-integrated/diagnostic.json、failure-log.json；日志接口输出截断，但内嵌压缩诊断完整解码，不能声称完整日志已读取。
- 前轮浏览器端口已关闭；仅重建本任务测试上下文，原事项534/535保留，不重发点将，不动用户原型或其他浏览器。

## 2026-10-27 08:08 云端验证及真实页面续测

- API5260799/333 SUCCESS，首次终态观测248.871秒；候选86f8ed1da1/tree5916e64d。同Run包内summary绑定commit/run：3289 tests、0 failures/0 errors、164 skipped，即3125非跳过；本修复ChatBountyBootstrapRelayRecoveryTest 8/8。validateLayering与fresh bootJar均实际执行成功。无部署，默认CI配置已CAS恢复。制品/summary/XML已取回ci-clock-fix/，摘要见api-artifact.json。不把云测成功写成线上已修复。
- 本次重新登录真实应用，534/535均已收到吴用首答。只读进程核对当前API PID431517，启动时间2026-10-27 07:20:26，早于本次验证；本任务未重启，不能将恢复归因于未发布修复。测试继续沿原事项，不再点将。
- chcbz/534在同一话头补充90分钟限制、追问轮流主持及防冷场，答复针对上下文且完成后无需刷新继续；证据browser/n03-round2-complete、n03-round3-final。已实际提交文本文件生成请求，成果尚待核验，不把普通文本答复当文件交付通过。
- ziyue/535详情明确吴用为“其他用户·在线”，不依赖所有者页面代为点将；首答和后续90分钟追问正常完成。正在进行第三轮；证据ziyue/resume-task535、x04-first-reply、x04-round2。本账号已有卢俊义，严格零自有Agent前置仍未满足，不能冒充纯新用户覆盖。
- BUG02/N09：话头记录打开后，以真实鼠标点击输入框仍未收起（展开列表保持）；更多操作点击输入框能收起且保留草稿。定位现有ChatPanel.vue仅toggleHistory，无外部点击/输入/Esc收起逻辑。先登记统一修复，不扩成UI重设计。证据browser/n09-topics-open、n09-topics-click-dismiss、n09-more-open、n09-more-dismiss。DOM click/focus辅助结果不冒充真实pointer点击，最终依据click.mjs的CDP鼠标输入截图。

## 08:15 文件执行断点已定位

- BUG03：534实际提交Markdown文件生成请求（mmd-typed-request_81a4d1806a33fb153898572870ad11f10a9fc8b6）返回CLARIFY，未产生文件。UI同一时刻显示文本文件/PDF可调用。只读本任务chat_typed_outcome确认后续轮availableActions仅image-edit/image-generate，排除仅凭模型描述推断；证据task-action-facts-readonly.json。
- 同一Agent当前文本文件1.0.1历史安装3份、PDF1.0.0历史安装2份，均有唯一managed activeInstallationId；证据skill-readonly-snapshot.json（只读，无状态/订单变更）。源码ChatActionCapabilityService.available和ChatActionExecutionService新执行prepare读取全历史再按key/version要求唯一，而UI按readCurrent读取当前安装，正好将两种同版本重装技能排除。修复必须保留历史用于已有执行/恢复，不删除历史、不去掉验证；新动作使用当前有效安装指针。当前尚未提交此修复。
- 37条阶段结果已落盘specs/juyiting-unified-experience/business-discussion-test-results-20261027.md，首轮未结束，不将NOT_RUN/局部操作/缺少零Agent前置算成通过。535跨用户三轮文本已完成（首答+两轮追问），仍留原事项待文件与验收回归。
- 534已从页面另起话头（N08），原话头1760458007854保留；本轮新话头正在测试一句选书建议，下一步等待原请求完成后从话头记录回旧会话，不能重发生成文件请求。

## 08:25 接续位置与新增正常场景缺陷

- N08/BUG04：534点击另起话头，输入“一句选书建议”并真实鼠标发送后，数分钟仍无新消息且草稿保留，网络只见/agent/tasks/534 GET，没有新聊天受理。未再次发送。初步定位发送入口存在refresh/fence返回false路径，但尚未证明具体原因；不得将猜测写成已修复。
- 从话头记录选回原会话，异步加载完成后旧三轮消息、文件CLARIFY全部可读（n07-return-old-loaded）。未提交草稿在切换后清空，未证明重新进入空白话头可恢复，因此N07草稿隔离仍未通过。没有创建新事项、验收或修改原文件。
- 本轮未运行新图片生成/编辑、林冲独立主线、语音/完整手机验收，不能宣称37条首轮已完成。停止点：两个原事项保留；API已推86f8ed1并通过333但未部署；BUG02/03/04待统一修复，BUG03已精确定位当前安装与历史读取差异。下一动作优先按当前指针补齐新动作选择和接纳的回归，保留已接纳执行固定installationId历史读取，不删安装历史；然后修复话头交互并继续真实页面验证。

## 2026-10-27 08:49 接续：当前安装修复云测通过，纠正前端旧基线归因

- BUG03最小修复已提交并普通快进推送API develop：`3bca7cbd719c3a331cc36ac26020f59183a0c839` / tree `9cbaa0cf2d9d8d5f9ff516055fb79ad276604cf2`。新动作发现及新执行快照使用readCurrent；保留历史读取用于缓存预热/已固定执行，不删除历史。新增同版本重装、当前歧义、读期间变更、执行快照绑定当前安装/卸载拒绝回归；原幂等重放分支未改。
- Flow5260799/334 SUCCESS，终态首次观测243.014秒，CI-only无部署，默认配置已CAS恢复。证据`/home/isp/state/cyf-business-normal-20261027/ci-current-install/`。同Run制品首次下载遇300秒传输超时，未重跑Flow；校验Content-Range/总长度后续传完成，摘要见api-artifact.json。测试明细从同Run包提取，不沿用333计数。
- Web主工作区旧代码不能代表线上。新增且仅一处必要隔离工作区`/home/isp/wsps/worktrees/business-normal-web-20261027`，branch `codex/business-normal-web-20261027`，base `f4e7f779304ee20efa3e6f29a6830a03d20ec88a` / tree `fcd31763d8fd2484eb1ac03d4f7f5c28497ec34c`。已读根AGENTS、Web规则及接口v1.4；主仓脏内容未改。该base含其他任务未部署改动，不自动获得全部发布授权。
- **纠正08:08 BUG02源码归因**：固定1102350及当前develop其实已有outside/Esc处理；实际页面JS也含dismissTrigger。原“源码只有toggleHistory”来自旧主工作区，不是正确发布基线。本轮真实浏览器重新登录原534，点击记录按钮确认aria-expanded=true，真实鼠标点输入框后false，局部收起通过；截图n09-recheck-open/closed。不把先前截图/观察直接重标通过，更不声称本轮代码修复了outside。
- 新定位BUG02剩余点：记录打开后真实CDP Escape关闭了整个议事页（.chat-panel数量0），而非仅收起工具；证据n09-escape-closed-discussion。源码父层JuyiHall.handlePanelKeydown先捕获冒泡并stopPropagation，工具document冒泡监听来不及处理。Web候选将History/Composer工具Escape监听移至capture，实际消费后stopPropagation；无展开工具时仍由原父层返回。新增3种工具嵌套父层回归，规格补“Esc只收起当前工具”。**Web仍未提交/云测/发布**，不得宣称修复验证完成。
- BUG04进一步源码证据：newHallConversation清空conversationId，而typed路径在submit前强制bountyAssignmentContext.refresh，其要求非空conversationId；不能直接删授权核对或降级旧发送。仍需确定事项新话头创建/绑定契约，再补修复，不猜测绑定、不重放旧执行。
- 继续顺序：读取334同Run summary/XML；完成Web精确回归与BUG04契约定位；候选统一授权部署后回原534/535继续文件/PDF/图片及剩余37条。当前没有新文件执行/验收，没有宣称首轮跑完。严格零Agent样本仍缺。
- 334包内最终核对：3293总项、3129非跳过、164跳过、0失败/错误；ChatActionCapabilityServiceTest11/11、ChatActionDispatchReviewGuardTest8/8。summary及两个XML已独立保存ci-current-install/。未部署。

## 2026-10-27 09:14 发布执行进展（线上健康待最后核验）

- N09/Esc轻量真实组件定向检查36/36（mocha单文件、不生产构建），之后在唯一Web工作区将自有提交rebase到已由另一任务发布的bb997887（Web349/1.16.61）；未覆盖他人修改。候选`1fdae7355dc19dea90186251de11ad19e4402758` / tree`e2209ab2d286ecbf8066d4ddc7d5769acf733cc7`，包版本1.16.62，已快进develop。
- **Web4403172/350 SUCCESS**，终态首次观测369.028秒，包含测试/Vite/扫描及同Run部署。主机record已online_verified/run350/对应commit；公网index与JuyiHallEntry JS摘要均匹配安装清单。证据release-web/；默认CI配置已CAS恢复。浏览器功能验收尚待，不以静态摘要替代。
- **API5260799/335 CANCELED**：固定3bca7cbd71的同Run测试3293总/3129非跳过/164跳过/0失败错误，制品SHA3373a40203ec06af58ca0048e5caf90c7d42f6caa3e8730b6fc671ed1fc3f179，223909706字节；版本1.17.11。576.927秒请求受控取消，589.023秒观测CANCELED，未突破600秒；不可称Run成功。默认CI配置已恢复。
- 取消时安装器仍持有本次发布锁，durable record为activating，旧PID431517在TERM后退出耗时较长；随后受控原安装器已启动候选PID480152（09:07:21）。当前正在核对同一安装器后续完成/恢复，不重跑Flow、不绕锁、不强杀进程、不启动另一安装。启动过程持续实例化Bean，截至此记录尚未监听10018，**不宣称API上线健康**。backup及recovery保留在record.json，任务证据release-api/。
- API同Run包在主机incoming保留；直接只读核对摘要及包内summary，避免重新跨公网下载，不使用334制品替代335。Web同Run包为downloads/350/package.tgz。
- N08真正缺口：冻结generic-point-and-deliberate-contract-20261003及ChatBountyConversationService.ensure绑定每事项唯一bounty会话；测试清单要求同事项多话头，现接口未提供创建/切换绑定。不能只清空conversationId后绕过typed指派核对，也不把隐藏按钮当N08通过。保留FAIL，需明确最小多话头业务契约；本轮未更改绑定/历史数据。

## 09:22 同次安装完成及浏览器回归开始

- API335同次主机安装器在Flow取消后继续完成可恢复安装；09:14:32只读观测durable record为installed，健康10018/actuator/health为UP；实体JAR SHA与335记录匹配（release-api/online-verification.json）。Run仍CANCELED，区分安装完成和流水线超时，不改写结果。没有再次发布/重启/强杀，也未开展OOM专项。
- Web350云端日志补取：3457 passing、2 pending，Vite built；日志tail100k仍作为截断日志保存，不声称全日志。代码版本1.16.62，静态公网摘要匹配。
- 真实chcbz重新登录打开原534，加载JuyiHallEntry-BP6E1iZo.js（350），议事显示4项技能；实际鼠标打开议事记录+真实CDP Escape，面板保留1、展开true→false、草稿原文保留。证据browser/n09-escape-post-release.json，N09其它工具仍待完整补测。
- 534在旧文件CLARIFY明确终态后，页面新提交“90分钟读书会生成Markdown”指令（新用户意图，不重放旧执行），草稿已清空、吴用回复中。证据browser/n16-post-release-sent/progress。此处未验证成品，不宣称文本文件业务闭环通过。

## 09:47 接续：工具实页回归及修改子请求断点

- 已重读项目工具入口与规则，沿用Owner/工作区/接口v1.4，无另建工作区。N09实际CDP鼠标/按键验证：记录展开→点输入、更多展开→Esc、添加资料→Esc，均仅收起当前工具，议事面板保持1，草稿“工具回归草稿：不发送”逐步完全保留；证据browser/n09-tools-post-release.json。工具互斥继续补测。
- BUG03实际新请求facts含text-file、pdf-extract、image-edit、image-generate，当前安装发现修复已生效；不等于文件交付通过。
- 新BUG05/N16：修改请求mmd-typed-request_c12f0750f3dae266edf6e2e2eeb1b73f8f75d8cb受理后子请求delivery-revision_428724fbd9048469c29dee0569885661dcb4297c一直RUNNING，turn_692ec737e53dd212eb190a01f352f681a057a599/dispatch同后缀仍DISPATCHED、delta0。Runtime原持久记录已RECOVERY_REQUIRED，精确原因CHAT_FAILURE: APP_SERVER_RPC_TIMEOUT:thread/start。精简证据n16-runtime-recovery.json；DB证据n16-revision-child-state.json、n16-revision-state.json、n16-revision-outbox.json。不重放、不改恢复文件、不重新发送。
- 源码核对Runtime15483d5已发送recovery_required ACK；API3bca7c中AgentWebSocketHandler.acknowledgeChatDispatch只将明确模型合同拒绝落FAIL，其他恢复ACK只确认outbox而未更新turn；这解释服务端/页面继续处理中的状态缺口。尚未据此实现或发布修复，也没有证明thread/start为何迟于传输超时。
- 继续真实535及534资料/验收等不受该子请求影响的正常操作；没有发起新的Flow，无进程/生产数据手工干预。

## 10:23 正常外单验收、恢复状态修复候选

- ziyue/535实页已走“验收此版→预览→返回取消→重开→选择唯一文字成果→确认验收”，最终事项已完成、议事只读；浏览器重新打开后本人首页仍能进入原535，成果记录显示已验收1、历史0、固定版本1。后续在390px模拟视口确认收入案卷，详情已归档，正在核对归档后历史成果。证据ziyue/n22-*.json/png、n23-*.json/png、n25-390-result；视口模拟不是真机/软键盘验收。
- 534资料浏览预览txt/PNG、暂选2份取消重开0份、重新选择完成、本事项2份固定v1，草稿保留且无自动发消息。证据browser/n10-n12-materials.json、n12-resume-detail。仅本条移除和资料实际发送仍未整体验完；没有冒充N11/N12/N13通过。
- 状态同步最小修复：API `a681131572c82261aba00e4f18238750f1973866` / tree `29ff5a9c15e74125b4d10d25bbed7da36e66e4fd` 已普通快进develop；原主API脏工作区不动。Runtime恢复ACK使用原权限/dispatch/message/turn校验，保留已确认终态，落RECOVERY_REQUIRED并刷新请求聚合，幂等不发新请求。明确模型合同错误仍FAILED，未知不猜完成、不重放。Web `1a808f9` 原任务分支已提交（未推/未发布），只补修改卡待核对提示，既有只读刷新不变，定向5/5；日志recovery-fix/web-targeted.log。
- API5260799/336已启动CI-only，固定a681131572，原570秒受控取消监控；截至本记录RUNNING。无新部署，源码测试通过之前不称可发布。证据ci-recovery-ack/。本轮既有selector覆盖ChatCancellationVersionTest，新增Handler参数化用例尚须加入正式selector后覆盖，不将编译等同用例执行。
- 当前根backend-ci-policy.json已有非本轮脏内容，不覆盖；后续仅在任务精确工具包追加这条handler selector或在保留原修改前提下定向协调，不改在途Run。规格补充已写回business-discussion-test-cases-20261027.md末节，接口仍v1.4、无新字段。
- 开始独立林冲主线：chcbz通过正常办事输入“三人小组30分钟周会，先讨论不生成文件”，只点击创建一次；等待自然候选页，尚未确认承办。原534未知修改不重发，535已归档不再继续发消息。

## 10:40 新事项首轮回归与归档缺陷候选

- 更正10:23创建观察：当时仍在事项列表，后台保留的首页DOM被遮挡，第一次测试工具鼠标没有实际点击创建；不是产品创建失败。已给自有click.mjs加elementFromPoint命中校验，避免以遮挡坐标冒充用户点击。实际返回办事后才创建一次536，候选默认吴用，手工更换为林冲后确认，自动进入原事项并收到三点30分钟安排。N01/N02自然回归PASS，截图browser/n01-linchong-*、n02-linchong-selected、n06-linchong-first-final。实际536只有图片生成可调用；已新提交一张蓝圆白底封面请求，未确认交付。
- API336 SUCCESS，首次终态观测372.017秒；3296项/3132非跳过/164跳过/0失败错误，ChatCancellationVersionTest11/11。同Run包与独立summary/XML保存在ci-recovery-ack，默认配置已CAS恢复；CI-only无部署。新增Handler参数化用例未包含在336方法selector，仍需后续正式测试覆盖。
- BUG06/N23：535已完成验收→收入案卷后，归档详情“查看历史成果”进入BountyAcceptancePanel，仍有继续议事/验收此版；没有点这些写操作。证据ziyue/n23-archived-history。Web候选2b6fc71将归档路由复用HallCompletedRecords，只凭ACCEPTED历史批次显示已验收，保留身份/固定版本摘要；增加归档只读/不伪造验收回归，相关45项轻量组件测试通过（首轮新增测试变量作用域错误已修正）。原型规格与根正常场景规格已补充。
- Web发布协调：只读远端develop已变为00b1a6b，含其它任务8a3826b/00b1a6b的引导导航修改；主机当前记录仍Web350/1fdae73。没有擅自将这两条未核实发布的其它任务改动打包上线，没有覆盖他人develop。自有修复保存在原分支codex/business-normal-web-20261027，尚未发布；当前真实页面仍旧版，BUG06不可关闭。

## 10:59 接续：归档修复发布中，林冲执行发现相同断点

- 已核实其它任务Web353/00b1a6b/1.16.63安装online_verified后，将自有Web修复rebase到该已发布基线，保留两段原型规格。候选58210f1edbe6cc1f7ec7d9e2b401a1fda44f6aa3 / tree1363e6ba67dd939f83d2ac1f5688cba0faaecdb5 /1.16.64已快进develop。当前任务远端功能分支仍为旧rebase前历史，不force覆盖。
- Web4403172/354已启动测试/构建/同Run部署，使用release-web-recovery的CAS配置及570秒监控。启动响应初期commit为空标UNKNOWN，返回run354；正在只读跟进固定源码与终态，不重复start。此前prepare核对无活动Run且原配置为默认CI。尚未宣称354成功或页面修复通过。
- 536图片请求已终态为REVISION_REQUEST，但其子delivery-revision_cb9f6bb75d924bcce1be91438a5a3808af1a6570未交付。精确Runtime恢复文件为RECOVERY_REQUIRED / CHAT_FAILURE: APP_SERVER_RPC_TIMEOUT:thread/start，对应turn_48943a55f3f772f19add244939d24c6381915dc7；API仍DISPATCHED、delta0。与534是同一类断点，不是林冲技能开关/岗位问题；底层thread/start慢因未证明，不把状态提示修复当执行故障已解决。证据n06-task536-followup.json、n06-runtime-recovery.json；没有重放、重发或修改生产状态。
- N09补测工具互斥与选材内部预览/添加暂选/取消，议事保留且未发送，整条PASS；536的N06执行闭环记FAIL。其它37条未完成项仍保留，不宣称全部通过。

## 11:17 Web发布与归档实页回归

- Web354测试/构建与扫描成功（3465 passing /2 pending），部署FAIL，旧备份目录`/home/isp/baks/cyf-web-business-normal-20261027`已经由350创建，复制的发布脚本`test ! -e`阻止继续；installer摘要匹配，线上仍353，没有覆盖旧备份或绕保护。默认配置CAS恢复。失败Run及原制品保留release-web-recovery/和原下载位置，未重标成功。
- 修改任务发布输入：下载暂存独立为business-normal-recovery-20261027，备份按本任务加真实BUILD_NUMBER命名，保留所有摘要/身份/互斥保护。Web355在同一58210f1/tree1363e6候选重新完整测试/构建并使用**355自己的制品**部署，终态SUCCESS，首次观测251.023秒；3465 passing /2 pending，Vite9.69秒。默认配置已CAS恢复。证据release-web-recovery-retry/。
- 355主机online_verified，制品SHA`ebae1ed91885a82f0d75dcf43b2f2e68e8736e8165f53141afe5cce2dd82cbe9`与同Run包一致；公网index和JuyiHallEntry-CLCeemnR.js字节摘要匹配。没有部署APIa681131；API336仍仅CI通过。
- ziyue真实浏览器重载后从“已归档”找到原535→查看进展→查看成果与验收记录，显示已归档·只读、已验收1/历史0/版本1。真实点击预览读到原2小时安排，无继续议事/验收此版操作；390px截图无横向溢出，非真机键盘验收。BUG06/N23页面回归通过，证据ziyue/n23-archive-fixed-355、n23-archive-preview-355。
- chcbz536补充选材：添加原蓝方块为本事项资料1份，草稿“选材移除回归：保留这段草稿，不发送”；仅本条scope EXPLICIT勾选→完成→重开仍勾选→取消勾选→完成→重开unchecked，scope仍EXPLICIT、本事项1份、原资料列表仍在且草稿不变。没有发新消息；N12原文件预览与最后证据正在保存。当前chcbz页仍350脚本，ziyue页已355，按浏览器分别记录。
- 下一优先：解决Runtime新子会话thread/start超时根因；补齐API新增Handler测试selector并制定600秒内可完成的受控发布（335安装慢不能盲重试）。原534/536未知子请求不重放；多话头BUG04仍未修复，严格零Agent/真机/语音仍有前置缺口。

- N12最终原文件预览加载完成（blue-square.png/v1/320×240），scope EXPLICIT、checkbox false、任务资料1份、草稿原文均回读确认；取消退出选材没有发送消息。N12改PASS。535实际展开验收记录显示“已通过·1份固定成果”、finalization_delivery_83a865ecdf5b1659e8055dba992c004240e06e2567005b76121009fb6de9cb9b /交付版本1，写按钮0。两浏览器仍用原私有profile，无需重复登录或新建事项。

## 11:46 状态回执补测与Runtime只读诊断

- API336未运行的`AgentWebSocketHandlerTest.recoveryDispatchAckUpdatesBusinessStateBeforeConfirmingReceipt`已加入任务专用Flow工具包selector，保留原policy所有选择项，不改根仓已有脏policy。Flow5260799/337固定a681131、CI-only，136秒FAIL；三种参数均因mock零调用而失败，完整结构化失败摘要`/home/isp/state/cyf-business-normal-20261027/ci-recovery-handler/diagnostic.json`。默认CI配置已CAS恢复；不得称该候选全部回归通过或部署。
- 排查测试报文发现新测试的注册未按既有v1 fixture显式绑定runtimeInstanceId；ACK也未声明当前runtimeInstanceId。按同类已通过测试修正注册及ACK身份并断言无protocol.error；不改生产身份/ACL。提交API `129571cd61aec7b48663488f4ffc51a7bd5e111c` / tree `7185bc6600e3b97fb395b6e2a9735a02f10d4325`，快进develop；修正报文后的Flow5260799/338 CI-only运行中，已有570秒监控，不以预测结果替代终态。
- Runtime只读观察：536原请求恢复时间10:47:19.503，林冲Codex日志10:47:26.293仍记录`thread/start`的shell snapshot创建，表明当时存在同时间窗的线程启动活动；日志没有业务dispatch ID，**不能单凭时间判定就是原请求或证明它是慢的根因**。本机Runtime profile还持续记录remote-control不支持API key的等待信息，但尚无证据证明其造成此次超时。未重启、清理、重放或修改任何进程/生产数据。原处理的15秒RPC timeout和线程启动链路继续定向排查。

## 2026-10-27 11:59 接续：338 同 Run 测试明细核验

- API5260799/338 固定 commit `129571cd61aec7b48663488f4ffc51a7bd5e111c` / tree `7185bc6600e3b97fb395b6e2a9735a02f10d4325`，CI-only SUCCESS，首次终态观测 313.72 秒，**未部署**；默认 Flow 配置已 CAS 恢复。337 的身份 fixture 失败仍按原 FAIL 保留。
- 已下载并核验 338 同 Run 包 223912054 字节、SHA-256 `1f841fac954a6993580b99a69740fad56eaae15249ffaa88920a3bd448a4f644`。包内 `test-results/summary.json`：3299 总项、3135 非跳过、164 跳过、0 失败/错误；同 Run `AgentWebSocketHandlerTest.xml` 中 APP_SERVER_RPC_TIMEOUT、TURN_ACCEPTANCE_UNKNOWN、ACTION_OUTCOME_INVALID 三个参数均实际执行且无失败/错误。原包与提取的 summary/XML 在 `/home/isp/state/cyf-business-normal-20261027/ci-recovery-handler-fixed/`。
- 本修复只处理未来有效恢复回执的状态同步，不解决 Runtime thread/start 慢因；534/536 历史 ACK 已由旧 API 确认，不能假定重新收到或自动修复。不得重放未知执行。API335 部署超时原因仍待只读查证；未发起新 Run、未部署338。
- BUG04 再核源码：`ChatBountyConversationService.ensure` 在授权校验后事务内保留每事项唯一 conversation 绑定；新话头清空 conversationId 后 typed 路径无法取得绑定上下文。需要在合同、身份/事项绑定与历史行为一致前提下实现，不能直接绕过检查。
- 追加只读部署慢点证据：API335 的旧进程 09:05:48 开始优雅停机，09:06:22 日志记录 webServerGracefulShutdown 等待 30000ms 后仍有活动请求，09:06:59–09:07:00 关闭连接池；候选 PID480152 于 09:07:45 记录应用启动，09:12:58 记录 Started，应用自身报告 325.956 秒。该次启用了启动诊断 DEBUG/TRACE，影响未量化；只能确认停机与启动耗时，不能据日志断定哪个请求/Bean是根因，也不能断言下次必定同样耗时。与338 CI-only约314秒比较，直接沿用335部署路径存在超过600秒的明确风险；不绕优雅停机/锁或盲目重跑。来源 `/home/isp/hosts/cyf/api/logs/root.log.2026-10-27.7.gz`。

## 2026-10-27 12:40 资源只读采样

- 宿主机2逻辑CPU、约3.64GiB物理内存；12:40采样开始可用约688MiB，Swap已用约1057MiB。`vmstat -t 2 16`的首行是开机累计平均，应排除；后续30秒连续观察有swap in/out，区间I/O wait在2%–73%间波动，部分区间出现较大磁盘读入；另有个别区间CPU忙。说明**当前**存在换页与间歇性I/O压力，不能用短采样推断所有时段持续饱和或单独归因。
- 采样末尾API Java RSS约897MiB、Elasticsearch Java约643MiB、Runtime约313MiB；RSS随时变化，`ps %CPU`为进程生命周期平均，不代表当时瞬时占用。根分区60G标称、已用90%、可用约6.3G（不是自动清理授权）。完整数据 `/home/isp/state/cyf-business-normal-20261027/resource-observation/host-sample-1238.txt`，含结束时只读进程列表。
- 目前 `/var/log/sa` 未找到2026-10-27的sar样本；以上数据不是09:00 API启动或10:47 thread/start超时期间的历史数据，不能断定该故障由资源不足造成。两原测试私有浏览器PID/CDP均不存活。没有重启浏览器、重放未知执行、终止其他任务或清理文件；要建立因果仍需同次新业务请求、RPC耗时与资源时间线相关联。

## 2026-10-27 12:56 同次真实业务与资源采样

- 使用新建私有浏览器登录chcbz，在真实页面新建事项537：三人30分钟周会及生成Markdown；12:53:28单次点击确认吴用承办。该事项与534/536独立，没有重发其未知子请求。首轮`mmd-typed-request_cfaaff4fe419a997688aac5a0bfad172284431c4`页面显示CHAT已完成，吴用表示生成文件；随后动作请求`77cee6a8e9010fd354f82041adc3365da736de5d4af570af5070443f60c66c3e`/执行`pwe_01b51630c43a2774a7588a2a9e9e362323e2cebb06f0e3fe2718b44794a0`，12:56:01真实API响应仍RUNNING，12:56:34页面仍“正在处理”，未观察到文件。此阶段不能称失败或成功、不重发；输出端点在轮询期间有200与404，未证明404是否缺陷。截图与页面证据browser/resource-task537-*.png/json，执行响应resource-observation/task537-child-response.json。
- 12:53:28–12:56:20同机vmstat每2秒共87个采样：全部区间有swap in，49区间有swap out；I/O wait均值30.0%、最高78%，CPU user+system均值31.5%、idle均值38.6%；结束可用内存624MiB、Swap使用1077MiB。首行开机累计已剔除，数值为短时间宿主机汇总，不能归因某单一进程。原始记录resource-observation/new-task-vmstat.txt。
- 该次**文本文件技能执行**仍运行，并非已证实534/536的delivery-revision `thread/start`超时路径；没有观测到其RPC开始/结束，也无法证明资源压力造成之前超时。只能确认同次任务运行期间确有换页与I/O等待。不得根据它声称超时复现或修复，也不将537记为成果验收通过。浏览器属于本任务的新临时profile，已发正常quit，不影响服务器任务；无其他进程控制。

## 2026-10-27 14:24 事项537后续只读核验

- 重新打开真实业务站点、使用chcbz在首页找到537，点击查看进展→继续议事（未发送或重发），14:23:12页面显示“结果待核实”，同时底部仍显示“吴用 正在回复/等待回复”，事项详情资料/成果均为0。截图与页面快照 `browser/resource-task537-1419.png/json`（文件名为启动时刻，事实时间以快照为准）。从12:53:28承办到该次观察已约90分钟，说明正常文件交付仍未闭环，且提示语存在不一致。
- 真实页面轮询的子请求API响应在14:23:55仍显示请求、步骤及执行状态`RUNNING`，证据`resource-observation/task537-child-response.json`；该文件被本次采集覆盖，12:56状态以之前handoff及截图为准。API状态不代表Runtime实际在运行，不能据此推测Provider结果、重放或改DB。按执行ID只读搜索当前及12–14时API日志、吴用runtime-state未发现明确绑定记录；无记录不证明从未派发，当前无足够证据定位执行卡点。
- 14:24资源瞬时约可用524MiB、Swap已用约1.1GiB；不是对前述90分钟全程测量。未做任何服务重启、数据变更、人工恢复或新请求。下一步沿既有执行链只读查权威派发/认领/结果记录并核对实际前端提示来源，修复后发布和浏览器回归；不要猜测537与thread/start故障相同。

## 2026-10-27 15:10 最后一轮性能定位转功能修复

- 按用户要求不再继续泛化CPU/内存采样。使用现有部署指南指定MySQL socket，在READ ONLY事务内精确查询537执行与技能两张权威表。PWE旧状态QUEUED，而protocol4技能状态**RESULT_UNKNOWN**、native-model副作用UNKNOWN、版本3、updated_at=1793076870259（12:54:30.259）；因此不是持续生成90分钟。请求/步骤/链接RUNNING是未随技能状态更新的旧投影。证据`resource-observation/task537-authoritative-state.json`（不含lease token等凭据）。Runtime journal同一执行ID在12:54:30与12:54:44记录SKILL_RESULT_UNKNOWN，完成身份关联，不再靠时间猜测。
- 找到了实际技能执行目录：`/home/isp/state/cyf-agent-runtime-v1/unified/agents/wuyong/private-runs/skill-runs/4ec538586e9ee54552328573f0a8d0d0c420cc325ea92f41b3649aaefd1de19f/pwe_01b51630c43a2774a7588a2a9e9e362323e2cebb06f0e3fe2718b44794a0/`。原先只查agent inbox遗漏了native技能目录。该目录只有命令/identity/attempt/input snapshot/UNKNOWN effect，没有已保存的结果。`skill-execution-store.mjs`捕获invoke异常后持久化UNKNOWN并抛包装异常；poll只返回包装code，底层cause未持久化。故仍无法从历史记录证明CPU/内存导致原调用失败；按用户要求暂缓性能专项，不将UNKNOWN视为可重放。
- 功能缺陷确认：typed action progress正确读取技能RESULT_UNKNOWN，但通用request仍RUNNING，useHallConversation据此置等待；同一页同时显示“结果待核实”和“正在回复”。沿用既有image-turn原型unknown展示，不新增入口。原型规格在原唯一Web任务工作区补充一致性规则；根Web原型有其他任务未提交内容，不覆盖。
- Web源码base仍58210f1、接口v1.4；在原唯一Web工作区修改BountyDiscussionPanel：仅对精确匹配事项/会话代次/当前执行子请求且无实际聊天turn/streaming的UNKNOWN，去掉等待回复展示并统一“结果待核实”，保留conversationBusy、草稿及既有不重发边界；不同会话/任务/代次/请求、歧义卡片及真正生成中的回话不覆盖。新增真实组件回归，三文件定向27/27通过（轻量本机，不是正式Flow/发布证据），日志`recovery-fix/unknown-status-targeted.log`。
- 该展示修复未云测/未发布，不能宣称文件功能正常；后端请求投影、Runtime调用与正常新请求的文件交付仍待处理。下一步以功能闭环优先推进，不继续无结论的性能采样、不人工改未知事实或重发537。

- 上述Web候选已本地提交 `557eaf5`；未推送、未启动Flow或部署。

## 2026-10-27 15:38 接续：UNKNOWN提示修复已发布并完成实页定向回归

- 继续按用户要求暂停性能专项；本轮不追加CPU/内存采样、不重放534/536/537、不改生产数据库/Runtime状态。优先交付已确认的功能展示修复；文件交付与BUG04另起话头仍未解决，不宣称正常场景全通过。
- 远端Web develop查询为`69175b99f9b8a4c36194d2b4edf22a26e4e027f1`，主机现行记录同commit且online_verified，含已上线的资料交互改动。原唯一任务Web工作区干净，将自有557eaf5变基到该基线，保留他人修改；相关27项轻量测试重新通过，日志`recovery-fix/unknown-status-rebased.log`。原型规格补充随自有提交保留，未改根Web脏原型。
- 发布候选Web1.16.66，commit `b049f9348dc5966af3d1f92f5b9dbdc48f3e7b56` / tree `72252522c40e64da6558540d9571725cd3bd4e89`，普通快进远端develop。Flow4403172/359固定同一commit；完整前端测试3481 passing、2 pending，生产构建及扫描通过，同Run部署SUCCESS。570秒受控监控实际首次观测终态262.871秒（不是精确平台总时长）；原默认配置CAS恢复。证据`release-web-unknown-status/`，build-log为100k尾部截断，不称完整日志。
- 同Run制品109587125字节，SHA-256 `92ea706f471523f373b3119e4f1d939dd55dceb1a24c0bc695ff6965efe28335`，主机record为359/b049f93/1.16.66/online_verified且制品摘要一致。公网入口/业务JS对照见`release-web-unknown-status/online-hashes.json`，浏览器实际加载`JuyiHallEntry-Cb1ppgr3.js`。
- chcbz真实浏览器先记录旧版537的“结果待核实”与“正在回复/等待回话”矛盾，刷新新版本后从同一事项进入议事：标题状态、操作状态、原消息卡均显示“结果待核实”，不再显示正在回复/等待回复/等待回话；原消息保留。390×844复测，无横向溢出；输入和发送仍禁用，未知工作不被重新提交。桌面/移动视口截图与明确断言：`browser/unknown537-before359*`、`unknown537-after359*`、`unknown537-after359-assertions.json`。这不是实际手机软键盘验收。
- 只关闭本次“错误等待展示”子问题；537依然没有正式文件，后端旧request/step投影仍RUNNING，底层失败原因无新证据，N16仍FAIL。37条原状态统计不变；API129571c仍仅338 CI通过、未部署；BUG04与严格零Agent样本缺口仍存在。本任务临时浏览器已正常退出并清理其新profile，不操作用户原型/其他任务浏览器。
- 下一条动作：围绕BUG04固定同事项多话头的最小绑定/切换合同并实现；原绑定ensure只有一条会话，不能仅清空前端conversationId，也不能放松身份/任务授权。文件链路须保留真实UNKNOWN，不以放开重发或隐藏状态充当修复。

## 2026-10-27 接续：BUG04 同事项多话头候选（未上线）

- 范围仍为正常办事/议事功能；性能专项暂停，不重放534/536/537。Owner沿用本会话；仅复用原API/Web worktree，未动根组件脏源码或其他任务进程。跨端依据为根工作区`api/docs/interface-standard.md` v1.4；组件worktree携带的旧v1.2文档不作为最新规则。
- BUG04最小合同已补入原正常场景用例文档N08尾节：保留原bootstrap绑定；新增空话头须持久化同事项成员关系与幂等回执，不新建事项、不自动发送、不绕身份/当前指派授权。POST创建、GET原操作回读；只有明确404才允许同键再提交。
- API候选`0d7e474827c2dbe112aaa42f128d1b1ed997f035`，后续修复测试泛型断言为`583b347a5ac7a4df0af559ae7991f5d3bffeec21`/tree `42c104a12cf47c113bce465b54fbf52508da7689`，均推至原任务分支，未合develop/未部署。新增`chat_bounty_topic`及事务服务/HTTP边界测试；10处原绑定消费者增加同owner/task注册话头识别，原ACL/指派/代次检查保留；岗位、Runtime无改动。**新增表尚未生产迁移，安装适配器与端到端真实新话头发送/成果交付仍待验证，不可单独先发布Web。**
- Web已接入原“另起话头”：服务确认且现有认证历史含新话头才切换；复用既有选择器保存旧草稿；创建期间防重复创建、发送、删除/切换旧话头；切换身份/事项取消旧读取并隔离迟到响应。确认切换后的内容读取失败走已有读取重试，不再新建。纯本机轻量98项通过（新话头、实际页面handler、会话历史），另6项实际Hall初始化/布局定向测试通过；SFC语法/模板编译通过，非正式前端Flow。
- 前端原任务分支由于历史变基发生非快进拒绝，未强推；普通merge保留远端旧归档修复，规格重复段合并保留全部事实；随后合入查询到的develop `361ed19bf405d81813e993bac533fb2e729385cc`，保留他人文案修改。合并后重新定向验证，最终SHA及结果见后续补记。
- 原型复用`interaction-completion.js`现有historySnapshot/historyRows，不新增区域。根Web仅定向更新本任务话头helper/规格，保留其无关脏修改。桌面实际鼠标新建→旧话头恢复原消息/附件/草稿通过；390px切回新话头恢复新草稿、无旧话头附件，选中记录后收起列表且无横向溢出。浏览器缓存刷新前旧截图列表仍展开，不作收起成功证据；以`browser/topic-prototype-new-draft-mobile-reloaded.png`及`topic-prototype-assertions.json`为准。这是离线原型，不是生产N08验收。
- API Flow5260799/339 FAIL（首次终态观测58.617秒）：旧CI脚本只接受历史分支，未编译；340 FAIL（52.576秒）：第二层编排器要求旧分支数组字节值，未编译。均已CAS恢复默认配置。按具体原因仅调整**本任务打包的CI配置/工具**为精确任务分支，不改根编排器、全局规则或部署授权；轻量执行实际guard表达式确认本任务分支通过、develop拒绝，见`ci-bounty-topic/context-precheck.json`。
- Flow341 FAIL（189.603秒）：已进入真实Gradle，新增MySQL测试`assertEquals(7L, tx.execute(...))`触发JUnit泛型重载歧义；已保存日志并改为显式Long局部变量（583b347）。无测试删减，341默认配置已CAS恢复。候选342 CI-only已启动，源码583b347，570秒任务监控保留；最终结果另记，不称已通过。
- 本轮证据在`/home/isp/state/cyf-business-normal-20261027/{ci-bounty-topic,recovery-fix,browser}/`。未更新原37条正式业务用例通过数，N08仍未生产复验、N16文件交付仍FAIL；零Agent样本缺口仍在。

- Web普通merge后的固定候选为`a73a49b4ec0b8f093fb3baa6f28c1682971b58fb`/tree `2ac8505131a40e4967dc5825bbf0013b8c67526b`，原任务分支已非强制推送；合并后的98项定向回归重新通过（`recovery-fix/new-topic-merged-targeted.log`）。前端未合develop、未Flow/部署；6项初始化/布局与SFC检查为合并前候选证据，不冒充该最终tree全量测试。

### 2026-10-27 16:55 候选云测收口

- API5260799/342 **SUCCESS，CI-only，无部署阶段**。固定583b347/tree42c104a；首次终态观测270.011秒，满足600秒上限。监控没有取消该Run；原默认Flow配置已CAS恢复/readback。341期间本机watch进程异常结束143后立即用原任务Run身份恢复监控，未启动重复Run、未影响其他任务。
- 同Run制品223923326字节，SHA-256 `4d35c8d3b9320162844e73fc4ff7b5bea379957de82e4cbb169e38ca28e57e0d`，已下载验摘要。`test-results/summary.json`绑定342/583b347：3311总项，164跳过，3147非跳过，0失败/错误；不把跳过算通过。新增HTTP4项、service6项，preview7项及真实MySQL37项全部非跳过通过；定向XML已保存。MySQL新增测试证明成员关系/幂等回执唯一性与事务回滚、原anchor不变，尚不替代整个真实服务+消费者端到端事务与生产浏览器验收。
- Web最终a73a49b同tree重新跑98项及Hall6项均通过，SFC语法/模板编译复验通过；日志`new-topic-merged-targeted.log`、`new-topic-merged-page-targeted.log`。均为轻量本机证据，尚未前端正式Flow。两组件任务worktree干净，已推原任务分支，不改远端develop。
- 自有原型浏览器已关闭，PID/profile均核实不存在；仅结束仍挂起的本任务终端，不清理另一旧进程/用户浏览器/共享预览服务。未重启生产、未DDL、未改534/536/537状态。
- **下一条动作**：补齐新话头真实discussion/action/delivery消费者与完整服务事务覆盖，核对新增表的既有部署适配器；前端固定候选Flow验证。然后按明确的制品/源码与600秒部署契约安排API→Web发布，再用chcbz/ziyue真实站点跑N08及相邻发送/历史/成果验收。API冷启动耗时问题仍不授权盲重试或绕锁，不能以CI-only成功标记上线。文件交付N16、其余未执行用例和零Agent缺口保持原状态。

## 2026-10-27 多话头范围复核：暂不纳入本轮发布

用户要求：通过代码或轻量模拟明确修改点；存在风险时先不支持多会话。本轮Owner仍为本会话，目标为范围评估，不做生产修改/DDL/发布，不重放未知执行。以下结论覆盖原候选API583b347a5ac7a4df0af559ae7991f5d3bffeec21、Weba73a49b4ec0b8f093fb3baa6f28c1682971b58fb（检查时两个任务worktree均干净），及已安装`app/codex-bridge`指定文件；未查询远端或重新核验线上版本，不称最新。接口依据仍为根api/docs/interface-standard.md v1.4。

### 已确认的适配点与风险

1. **入口/恢复不一致**：`ChatBountyConversationService.ensure:59`和`ChatConversationServiceImpl.createOrReuseBounty:204`仍复用原binding会话；Web `useHallConversation.js:1052`按`update_time desc`取第一条。多话头时bootstrap与普通历史恢复可能选不同话头，旧话头晚更新可能改变下一次默认入口。需要统一默认选择规则，不是仅新增创建接口。
2. **创建/授权跨多条业务链**：候选在10个discussion/interaction/action/inspection/delivery消费者添加containsTopic；新表同时承担成员关系与幂等回执。改为复用task_id后仍需逐处统一租户/owner/client/事项/类型/存活/代次/指派检查，以及创建幂等；不能直接删除授权检查。
3. **成果聚合并未闭环**：`ChatSelectedOutputFinalizationService.resolve:156,195,221,242`限定提交会话与原成果会话一致；文字来源与正式成果修订同样有会话约束。跨会话提交需要逐项来源身份、代次、授权、摘要及修订继承契约，而非简单移除equals。当前同会话交付逻辑不能证明跨会话交付可用。
4. **请求/资料/事件是会话视图**：`ChatBountyRequestIndexService:42,182`绑定会话/代次；Web选择话头会停止旧stream/poll并载入所选会话。若提供事项级成果汇总，需要独立于当前会话的明确读取/选择语义，并验证旧话头执行完成后的展示，不能让晚到事件切换当前页。资料/草稿保留当前隔离；跨话头复用需显式引用，不自动继承全部上下文。
5. **删除明确不支持**：`ChatConversationServiceImpl.deleteConversation:119`拒绝所有juyiting bounty通用删除；Web `deleteHallConversation:1178`仍调用通用删除，成功分支清空并提示另起话头。多话头删除不能凭候选创建成功视为已支持，需要成果/执行保留及当前话头回落规则。本轮单会话方案不开放事项话头删除，不删除历史数据。
6. **重指派影响全部话头**：`ChatBountyBindingStore.replaceAuthorizedTargets:108`候选更新原anchor及注册话头。改用已有task_id关联后须同步范围，验证新旧Agent授权/历史成果来源，不可只改创建端。
7. **Runtime非所有资源按会话隔离**：实际`buildThreadKey`包含conversationId/generation/authority；受管代码工作区`WorkspaceManager.describe:348`按task+Agent映射路径与锁，不含conversationId。因此不能宣称多个话头的文件也互不影响；是否允许并行写入及锁覆盖需另做完整执行链验证。现有锁不等于已经证明无风险，也不能据此声称实际发生串写。技能输出另按executionId存储，不应改成整个事项共用结果文件。
8. **分页与正式覆盖不足**：新话头adopter依赖当前历史页包含receipt中的会话；大历史分页/旧话头恢复需补查。已有342 CI证明旧候选局部服务/HTTP/存储测试，不覆盖多话头发送→执行→跨话头交付→验收/返工→重指派/删除的整链。

### 决策与最小闭环

按用户风险优先要求，**暂不推进同事项多话头候选合入/部署，不执行chat_bounty_topic迁移**；本节取代上节“下一条动作”的多话头发布安排。保留原候选和证据，不回退或覆盖其他任务源码。事项议事维持同一身份作用域下一个绑定会话，反复进入继续原会话；普通聊天多会话不受影响。不把全局事项强制收成一个跨用户共享会话。

后续实现需同步原型/规格，收起事项议事的“另起话头”和话头删除入口（不新增开关/弹窗）；普通聊天入口保持原样；历史只读访问和执行/成果证据不得删除。这些UI调整本轮评估尚未实施，不能声称已经上线。回归重点改为：重复进入同一事项、连续讨论、补资料、执行、成果交付、验收/返工、刷新恢复及不同账号隔离。N08应明确标为范围调整/暂不支持，不伪报通过；N16仍待修复验证。

### 本轮验证边界

证据目录`/home/isp/state/cyf-business-normal-20261027/topic-risk-audit/`。实际已安装chat-runtime纯函数以合成输入验证相同输入稳定、不同会话/代次/授权生成不同thread key，4项通过，源文件SHA256见`runtime-thread-check.json`；未创建工作区或调用模型。前端首次直接Mocha缺tsx解析器，导入阶段失败，日志保留`web-targeted.log`，不是产品功能失败；使用项目现有tsx入口重新执行三个定向文件，结果另补。此次无正式云测、无真实浏览器业务回归，不更新原37条通过数。

- 前端第二次带tsx但遗漏项目tests/setup.js，结果63通过/14因window未定义失败（`web-targeted-tsx.log`）；定位为测试启动环境而非修改产品代码。按现有.mocharc.json补齐require/timeout/exit，仅运行指定三文件，最终**77/77通过**（`web-targeted-setup.log`）。命令：`node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --timeout 10000 --exit tests/juyiting-bounty-topic.test.js tests/juyiting-hall-conversation.test.js tests/juyiting-conversation-material-links.test.js --reporter dot`。仅证明已有局部前端行为，不证明上述跨会话交付/删除缺口不存在。未修改任何组件源码。

## 2026-10-27 用户确认收敛后实施：单会话闭环

- 用户确认按单会话继续跑通正常流程。Owner仍为本会话；不推进多话头候选、不改生产数据库、不重放534/536/537未知执行。
- 复用原Web工作区，新分支`codex/business-single-conversation-20261027`从本轮fetch所得origin/develop `361ed19bf405d81813e993bac533fb2e729385cc`开始；旧多话头分支/提交原样保留，未reset旧候选。主机Web record同commit且online_verified；不把该证据推广到API/Runtime。API候选工作区不动。
- 最早验证：单会话入口/保留草稿的真实组件及composable定向测试，随后Flow固定源码与生产浏览器；接受用户既有修复→发布→回归授权，仅发布本轮实际验证的局部Web候选，不自动发布其他API候选。
- 原型先行：唯一原型原位隐藏事项新对话/记录删除并加相应事件保护，公议/密议不变，原历史数据不清理。真实原型浏览器桌面历史截图single-prototype-history-desktop及390px mobile：无新对话/删除按钮、scrollWidth=390；这是原型不是生产验收。工作区原型同策略，root其他脏原型内容未覆盖。原型规格及功能用例新增用户确认覆盖条款，N08多话头改DEFERRED不伪报PASS。
- 产品候选：ChatPanel依据现有bounty类型隐藏新对话/只读历史删除；useHallConversation的新建/删除入口在bounty范围直接返回且不清草稿/消息，不调用删除接口；JuyiHall页层新建先判断bounty，避免关闭语音/清状态。无需新增表、Runtime或接口。历史选择继续保留，不删除原历史。

### 单会话首批正式发布及新发现（2026-10-27 22:20接续）

- 单会话Web1.16.68发布源码448bc5d78a32559dbffba2811dae44117becd9c8/tree b1cb914fccab7842653e64289eb89530f267ab2d，已普通快进develop。Flow4403172/365测试、扫描、同Run部署SUCCESS，监控首次终态296.666秒；主机record同commit/run/version online_verified，artifact SHA256 d16de5a6a89b41d813b187f7516893a4ad5a7b7763ca4008e38a2040f92191ea。公网产物/真实页面定向核验仍在进行，不能以主机record替代全部业务验收。默认配置已CAS恢复。
- 历史失败：363为Owner误用了仓库中名为release但实际仅CI的模板，发现后仅取消自有Run（首次终态62.068秒），未安装；恢复配置后改用原已验证同Run部署适配器，未拆分制品/绕10分钟限制。364为新单会话行为与旧terminal-layout测试仍期待新对话按钮冲突；3489 passing、2 pending、1 failing，未构建/部署。按用户确认规格更新该断言，同时保留运行中事项仍可回答CLARIFY的断言；89项定向通过后新源码448bc5d跑365，不是同输入盲重试。
- 轻量lint不是全绿：3个既有文件271项问题（163 errors/108 warnings），与361ed19相同规则/消息/数量，无新增；证据single-conversation/lint-baseline-comparison.json。不宣称lint通过，也不扩展格式重构。
- 本轮真实chcbz UI创建事项539、吴用承办、会话1760458008046；明确要求可下载Markdown文件。父typed请求mmd-typed-request_a3f4d354af2bc30acbd2a3b0e03903ed98a83c23，子请求292c32c4759a2651e6583edb42b5337fafef8b1eaab439073f41768a725be810，execution pwe_5015e487f9afa8e8913440c6c5bb7cbb877aacb8657a93428e199d508bf6。只发起这一次，不重复执行。权威typed回执是schemaVersion6/outcomeContractVersion5/RESULT_UNKNOWN，子请求仍RUNNING，无确认文件；不能记N16通过。证据single-conversation/task539-{typed,child}-response.json及browser/single-*。
- 新确认前端缺口：hallSkillResults.js只接受outcomeContractVersion4，虽然主typed投影支持4/5，导致v5技能不读取精确执行结果；此外BountyDiscussionPanel原UNKNOWN状态覆盖仅匹配当前子请求，不匹配已完成讨论父请求，页面父请求“已完成”会掩盖尚未知的子执行。本轮准备v4/v5兼容读取及精确父子UNKNOWN展示候选，不修改未知执行事实/授权、不自动重放，不把展示修复称为文件已生成。原型沿用既有未知状态，规格补充这一语义。
- ziyue已真实登录并创建外单测试事项（候选默认卢俊义，正在UI更换吴用），尚未完成确认/首轮，不能记外单通过。两账号皆有Agent，严格零Agent前置仍缺，不删除原Agent。
- 未新增API表，未发布API多话头候选，未改Runtime/生产数据库。下一步先完成单会话实页核验、兼容读取修复定向/Flow，继续两个账号正常流程；底层539 UNKNOWN保留，不重复创建同类文件任务碰运气。

### 2026-10-27 22:55 单会话第二批发布与浏览器核验

- Owner/范围不变。Web worktree `/home/isp/wsps/worktrees/business-normal-web-20261027` 当前960841394c5f671b5615b6b1bef9e802722cd1ec/tree0075126da5adae6096528f3a14397b75d567fdf4，版本1.16.69，已推develop及本任务分支。局部41项通过后Flow4403172/366正式3492通过、2pending、0失败，259.1秒首次终态SUCCESS。默认配置CAS恢复readback成功；不重发Run、不改其他任务。
- 同Run366实际归档 `/home/isp/state/cyf-web-flow/downloads/366/package.tgz` SHA256 `9d7fc4c4bddd221a8e0081cf86237039a7b75173fb22980c0ff5be22d96f4955`，与主机record匹配；公网index.html与JuyiHallEntry-Ce0RPu6y.js摘要匹配。证据single-conversation/release/verified-366.json。辅助提取曾因系统Python无hashlib.file_digest失败，改用流式hash后成功；不记应用失败。
- 真实539页面已刷新重进并恢复原内容，历史无新建/删除；390px无横向溢出，实看截图布局。v5读取及UNKNOWN父子提示实页生效，不能据此声称文件成功。Runtime精确execution的effect UNKNOWN且无result.json/输出，原始cause未保存在该effect；只读留证，不改状态、不重放、不扩大性能排查。
- ziyue新540已真实选择他人吴用并确认；会话1760458008059，父请求mmd-typed-request_cb81d4f94cfffc112c1fcc6acd92a3d68485850a，turn/dispatch后缀7af4c5f856bb1ad8f82df1edc6e11d8565641024。22:51:48回执RUNNING/DISPATCHED/seq0，尚未首答；没有重复确认/发送。新540不能当X03成功。
- 下一动作：仅观察540的原请求/精确Runtime接纳与ACK，定位首答为何未产生；不再新建同类任务碰运气。539结果UNKNOWN需权威恢复证据；不能重放或伪造交付。继续不受阻的真实交互，最后按原用例逐条收口，当前37条远未全绿。API多话头旧候选仍不发布，不DDL。

### 2026-10-27 23:00 外单540阻塞证据补充

22:57实页仍无首答。只读找到本次精确request的Runtime inbox recovery：`state=ACCEPTANCE_UNKNOWN`，`recoveryReason=TURN_ACCEPTANCE_UNKNOWN: APP_SERVER_RPC_TIMEOUT:turn/start`，receivedAt1793112320968、claimedAt1793112326374、recoveredAt1793112799790。脱敏证据`single-conversation/task540-runtime-recovery.json`。这证明请求已送达Runtime，阻塞发生在模型turn/start接纳/回读链路；不是“用户没有自己的Agent不能接外单”，也不能把RPC超时进一步推定为CPU/内存不足。当前接口仍RUNNING而恢复记录已UNKNOWN，需继续核对该精确请求的ACK同步及原turn权威回读；不得重发、改库终态或凭未知结果验收。已安装adapter在turn/start异常后会尝试thread/read reconcile，结果未形成已完成回执，不能绕现有未知执行保护。

## 2026-10-31 修复发布阻塞并继续快速回归

用户已授权修复前端Run385失败并继续发布。Owner：当前会话；仅修复必要SDK加载隔离，不扩展业务/后端/Runtime。入口规则按根AGENTS 2026-10-29 Flow只构建上传、主机独立安装。唯一任务worktree `/home/isp/wsps/worktrees/business-smoke-web-20261031`（根Web脏且历史本任务worktree已清理，不能安全切换），分支codex/business-smoke-web-20261031，base远端develop3040a404887d444f778d1bd3ef341d86fabba716/tree03a71e55b6a466149e51fb3a1484c95ae002a41c。最早验证：orientation+mini-program-file-download两个轻量测试重现→同选择器修复回归→Flow4403172完整测试构建上传→固定制品主机安装→真实页面正常用例。接口不变，不需API/Runtime联动；责任层为Web SDK适配器生命周期，非业务权限；无样式/交互改动不扩原型。线上基线bdb973a4/1.16.80/Run384；部署/用例结果后续另记，不把Run385失败改成功。

- 失败重现：同进程先跑orientation再跑file-download，26通过/1失败，和Run385同一finishSdk错误。原因是模块级单一bridgeLoadPromise复用了另一host已加载的SDK，当前fixture根本没有启动加载；不是通过删除finishSdk调用放过断言。最小修复在SDK适配器用WeakMap按host保存promise，同host去重、不同host独立；新增双host并行+同host去重实测，原取消回归仍保留。28项轻量定向全部通过，diff-check通过。版本1.16.81，提交2d95422已普通快进push到develop；Cloud386固定此候选，仍监控570秒受控取消/600秒上限，未改API/Runtime/原型。

- 2026-10-31发布收口：386 SUCCESS，3586通过/2pending/0失败，144.001秒；1.16.81/2d954229已独立受控安装，公网入口及相关JS/CSS 8项摘要匹配。备份/home/isp/baks/cyf-web-flow/20261031-business-smoke。结果已写specs/juyiting-unified-experience/business-discussion-test-results-20261031.md及/home/isp/state/cyf-business-smoke-20261031/results.json。真实浏览器6通过/2失败/24阻塞/4未执行/N08延期：PDF带入后Agent仍称无附件；文本文件卡不可在线预览；18:30起API502阻塞原看图请求、刷新恢复与验收。不重放、不改库、不重启共享服务、不扩业务修复。下一步先恢复API并核对原请求，再定向处理已记录业务问题。任务自己的干净临时worktree收口删除；提交已在develop，补丁/固定SHA留证。


## 2026-10-31 21:53 浏览器继续回归收口

- 固定Web1.16.81 / commit2d95422951289ca0b3ab74aa805f7a4b03cbecdd / tree a4e81454fe0f83bf9e167ad012d681e4163934b9 / Flow4403172/386，21:53安装记录仍online_verified，无重新构建/部署。API只读基线421/2a8a67c58c1949d671a4952bac496527ec1f3cea；本任务未重启或部署API/Runtime。
- 真实认证浏览器恢复，原看图请求已答蓝色正方形，不重放。继续事项566/567，新增569做同账号A/B。566原始文字成果仅单版验收并归档，未验收预览失败文件；记录保留已通过1份固定成果、版本1。
- 当前37条：12PASS/5FAIL/18BLOCKED/1NOT_RUN/1DEFERRED。新增通过N03/N05/N11/N20/N21/N22；失败N13范围控件遮挡、N14 PDF上下文、N16文件预览、N19停止后部分历史丢失、N23归档成果展示矛盾。归档实际成功、验收记录存在，不声称成果数据被删。
- N17尚未执行完整改图；不再借旧502作为阻塞。18阻塞及覆盖边界详见结果报告最新节。两账号都有本人Agent，12条严格新用户用例保持阻塞，不删Agent、不假通过。音频同一真实PCM WAV在独立dataURL亦解码失败，环境阻塞而非产品FAIL。
- 机器结果/截图/DOM：/home/isp/state/cyf-business-smoke-20261031/results.json及browser、ziyue目录；详单specs/juyiting-unified-experience/business-discussion-test-results-20261031.md“恢复后继续浏览器回归”。业务代码未修复；仅此前SDK修复已正式上线。
- 后续：按五项失败做修复和定向回归；补N17和真实样本/设备覆盖。性能/OOM、岗位、多会话不在此范围。工作区既有脏内容未覆盖，不新建worktree、不stage他人修改。
