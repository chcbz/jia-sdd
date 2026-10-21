# 设计接续记录（当前D2；历史澄清保留）

## 本轮范围

- 用户请求：先做聚义厅吴用接外单的最小闭环详设，并分析影响范围。
- 本轮唯一 Owner：当前聊天。Feature ID `juyiting-external-commission-mvp`；没有登记/启动新实现任务，没有抢占现有任务。
- 目标：固定范围、双主体授权、三端调用链、数据/HTTP/WS合同、取消/恢复/成本语义、影响和验收矩阵。
- 非目标：业务源码改动、原型实现、云端配置、构建、生产DDL、付费Provider调用、部署/服务重启。
- 阅读入口：根 AGENTS.md、ops/orchestration/README.md、docs/sdd-workflow.md、api/docs/interface-standard.md 1.2，以及原 juyiting-skill-execution 局部Task/Runtime分离记录。
- 共享 cyf-quick-iterate 技能中“develop自动部署”的历史描述不适用；以当前项目 AGENTS 的双端Flow、版本化部署、develop不自动部署为准，未修改共享技能。

## 固定源码

详见 baseline.json。本地：root `93f7e0afe81f3eb8d9e23e6a7555ea960c6010c2`；API `21c32034b4b60cad497db5640966fdd7635d44b8`；Web `6c350fbaa81263aff90f23027fe2250a62f1df83`；Runtime `5e8742aac6b9261a8d6cc94f77da1175e8ae74e2`。

2026-10-21 17:48:38–17:48:39 +08:00 实际 git ls-remote origin refs/heads/develop：
- root `3dff3c703bb709a64e21ce8ef0c0d73f5433f942`，与本地不同。
- API/Web 与上述本地一致；只表示该查询时点，不保证以后仍最新。
- Runtime `7ec6ffe037c6474b784bd7d151ae9e0adf469acd`，与本地不同；未fetch/merge/改写其工作区。

共享根仓已有大量无关修改/未跟踪文件，Web有 AGENTS 与原型证据修改；全部保留。API 与Runtime读取时 tracked worktree 干净。基线记录来自本地源码/工作区，不是根gitlinks或线上版本。受测候选/线上版本本轮均未核验。

## 已确认结论

1. 技能策略目录部分已分开 taskScope/runtimeScope；不等于外单全链路。
2. 原 assignment/grant target、PWE create/queue/input/result 路径尚有同Owner假设。
3. Chat outbox按任务Owner选通道，入站也有sessionOwner假设；外单必须双向路由与资料/上下文隔离一并验证。
4. 原协议4执行、effect、结果和正式验收链可复用；不另建订单/执行系统。
5. D1收敛为白名单、单吴用、固定image-edit、一张图/单PNG、一次效果、平台不收费；模型成本不等于免费。
6. 入单与首次指令分两步，避免为“一键开始”扩建跨模块事务；原任务办事页沿用。

## 最早验证与下一条动作

当前仅文档静态检查，不运行应用测试。后续实施先绑定真实ledger任务和干净三端基线，定向补“不同Owner的A委托B，缺委派拒绝”的target/queue/WS失败回归，再从EX-02双主体类型与持久授权实施。Web改动先更新现有原型。

Runtime基线差异、真实A/B/C账号、技能/模型成本来源和存量活动执行需要在相应阶段核实；它们未阻断本次设计交付，不能虚报已经具备在线验收条件。

## 文档交付

spec.md / design.md / impact.md / tasks.md / acceptance.md / integration.yaml / baseline.json。specs/INDEX.md仅加本特性Draft入口，不修改其他功能生命周期、不更新根gitlinks、不提交混合改动。

定位/实现/验证/等待耗时：未测量；业务实现未开始，正式验证与发布未开始。

## 本轮文档自检

- 必需文档、Markdown本地链接与代码围栏、示例JSON解析通过。
- baseline.json中三端/root当前HEAD与固定值相符；15个定向源码文件摘要未漂移；公共接口规范SHA核对通过。
- `git diff --check -- specs/INDEX.md`通过。未跟踪的新文档另检查尾空白/换行。
- 当前python缺少YAML解析库，未安装依赖；integration.yaml未经过YAML解析器验证，不把其他检查扩大为此项PASS。
- 未运行应用测试/正式构建/部署；所有业务验收仍NOT_RUN。未提交或推送，不混入根仓已有修改。

## 2026-10-21 用户澄清 / D1.1

用户明确吴用只是测试例子，应支持chcbz独立开启或关闭吴用、林冲接外单。当前方案已修订：任意拥有者对本人每个Agent独立控制；单Agent指每单单Agent；禁止写死用户名、角色名、personaCode或固定试点ID。政策按canonicalAgentId/binding独立，开关意愿与执行就绪分开。新增六项验收（AC33–AC38），原源码基线和NOT_RUN状态不变。上述D1“单吴用”措辞由本节替代，不表示已经实现或开通线上服务。

## 2026-10-21 用户确认 / D2（覆盖上文D1/D1.1相反默认）

1. 开启外单即同平台所有已认证用户可下单，不做用户白名单等限制。
2. 不限制任务类型；Agent能力只影响推荐承办，不作为手动选择/派单门槛。图片仅测试样例。
3. 本期不处理交付费用；未来按委派内容预估交付费用，模型调用费用只作成本展示，不是交付价格。

当前合同已同步spec/design/impact/tasks/acceptance/integration和索引。删除旧政策里的客户名单、IMAGE_EDIT服务/技能固定、成本前置与整单一次执行限制；统一候选为自己的Agent＋同平台已开放的其他Agent。离线/忙碌允许先委派，按原持久调度等待；实际工具不存在仍真实报告，不虚构执行能力。新增通用任务、多动作/返工、成本未知不阻断等用例，共AC01–AC46，均NOT_RUN。

D2仅修订设计，不追溯修改baseline.json源码证据，不声明新增代码或线上能力。旧源码和远端查询均只代表其记录时点；实际实施仍需固定新基线。没有新增Reviewer/审批/收费/性能门禁，没有触发Provider、构建、DDL或部署。

D2文档自检：本地链接/代码围栏/JSON示例/尾空白和46项用例连续编号核对通过；移除旧业务门禁的定向文本断言通过。首轮自检脚本的期望编号误用AC1而非文档AC01，修正脚本后通过，没有修改验收结果；所有业务用例仍NOT_RUN。未使用YAML解析器，未运行业务测试或部署。


## 2026-10-21 原型增补（用户新增授权）

- 用户要求“现在就更新，然后用浏览器打开让我看下”；本轮扩展范围仅离线原型，不改产品实现、不构建/部署。
- Owner：当前聊天；沿用 Feature ID `juyiting-external-commission-mvp`。
- 工作区：`/home/isp/wsps/cyf/web`；本轮本地 HEAD `19a322a4b3b51856f8c1235a73d3aac4d848b022`。与前文设计读取时间不同，不将旧基线称为当前 HEAD。未重新查询远端、候选和线上版本，无最新发布结论。
- 开工目标 tracked 原型文件无已有修改；已有未跟踪历史截图/报告保留，未覆写。根设计文档沿用本聊天 D2 工作区。
- 修改：现有 index、prototype.js、interaction-completion.js，新增同目录 external-commission.js/css 功能模块，同步 prototype-spec.md；未新增平行页面。
- 完成逐Agent开关、统一承办选择、确认委派、待指令/待运行、原议事模拟继续、精简接单概况、成本语义。
- 最早定向验证：node --check；随后复用已有 playwright-core 和 Chromium，不装依赖、不运行应用构建。浏览器验证与截图见 evidence/browser-check.json 及相邻 PNG；这是离线交互诊断，不是46项业务验收通过。
- 首轮复用已核验的既有预览（127.0.0.1:18786，serve-preview.py）。复查时原监听已消失，连接被拒绝；确认端口空闲后由本聊天启动同脚本预览，未终止/接管其他进程。再次完整浏览器检查 PASS，保留本聊天服务供预览。
- 已调用 Codex 浏览器面板打开 `http://127.0.0.1:18786/?revision=external-commission-d2#agents`，工具返回 queued；桌面实际显示和远程转发未获工具确认，不声称用户已看到。
- 未完成项：真实跨用户权限、服务端开关/委派/调度及费用成本读回均未开发。正式产品验收维持 NOT_RUN。

### 2026-10-21 原型修正：开关直接置于 Agent 详情

- 用户明确不要独立接外单卡片。移除点将册顶部管理卡片和跳转管理按钮；本人 Agent 头像/名称下方直接放接外单开关行，外部 Agent 仅只读状态。接单概况沿用详情操作区，不新增卡片。
- 复用本聊天上一轮未提交原型修改；仅修改 external-commission.js/css、index 缓存摘要及原型规格，未覆盖其他修改。开关仍按 Agent ID 和 owner 判断，与显示名无关。
- 本轮离线检查：JS语法、桌面1440×1000/移动390×844、无独立卡片、本人单开关/他人只读、两Agent四种组合、键盘切换与焦点保留、移动返回名册、刷新持久化及无横向溢出全部通过。
- 新证据：`evidence/detail-switch/check.cjs`、`result.json`、`desktop.png`、`mobile.png`；上一轮 screenshots/check 保留为历史，不再代表开关的最新布局。
- 现有预览服务18786仍可用。用户环境已报告内嵌浏览器当前URL为 `http://localhost:52787/?revision=external-commission-d2#agents`，未重启服务或变更转发。用户刷新当前页即可加载新的资源摘要；不声称已替用户操作刷新。
- 产品实现与正式业务验收仍未执行，不触发构建/部署。

### 2026-10-21 预览服务持续运行修复

- 用户两次反馈无法访问；复查确认18786已无监听，原后台进程不存在。此前启动瞬间HTTP200不能证明跨轮存活，未确认退出根因。
- 改用本聊天专用 user transient systemd unit `cyf-commission-prototype-preview.service` 运行同一只读静态预览脚本，仅绑定127.0.0.1:18786；不改业务服务、不设开机自启、不操作其他聊天进程。
- 分离命令后再次检查 unit active/running，并重跑 detail-switch 浏览器检查 PASS、HTTP200。保留供用户查看；结束预览时可仅停止此unit。
- 再次请求打开原型，UI工具返回queued；未将远程服务健康等同于桌面转发/用户浏览器已成功。

## 2026-10-21 D2.1：重新根据代码与生产界面实操复核

- 用户授权继续分析详设缺漏、重新查代码与生产UI。Owner仍为当前聊天；不新建实现任务/Reviewer。范围为设计审查、生产只读页面导航与文档修订；非目标为业务写入、模型调用、产品开发/迁移/发布。
- 先读项目规则/工具索引、现有D2及生产复核工具。共享快速迭代技能的自动部署旧描述不适用；本任务没有构建或部署。
- 新基线、远端develop查询、文件摘要、实际线上文件对照均在 `evidence/design-recheck/`。API已前进至510b293；Web核查期间由19a322a前进至68552ea，仅src/useOutputs.js变化，已重新加载生产复查当前页；Runtime本地/远端当前一致。未改其他任务代码或流程。
- 复用既有readonly-session与inspect-production工具，新建本任务独立浏览器，使用既有授权测试登录；拦截除GET和已核验列表/推荐POST以外的业务写入。实际打开PC/移动Agent详情、提出需求、原任务492待点将详情与候选、资料引用元数据。未点击确认派单/取消/发送/验收/上传，未修改Agent配置，无Provider调用。
- 16份实际加载Web资源与当前发布记录/安装文件摘要匹配；API实体JAR与当前安装回执匹配。新外单接口源码仍不存在；当前用户候选不能冒充真正跨用户验收。
- 发现10组缺漏并写入 `design-recheck-20261021.md`，详设升级D2.1 §11，影响/实施/索引同步；验收扩展到AC01–AC58，全部业务NOT_RUN。重点：多处本人名册守卫、本人离线准入、首轮bootstrap耦合、双client域、ACK/receipt/stop、真实取消边界、显式资料授权、换承办代际、公开归属、未知结果恢复。
- 开发就绪结论：业务规则无需追加产品澄清；技术平台映射/DDL与锁序/准备会话协议及迁移仍须EX-01/02冻结，不能声明全部前提已完成。本轮只修设计，原型仍缺D2.1部分异常/独立状态/文案，记录在复核报告§5，不将其标为已实现。
- 下一步：优先落实技术冻结与失败回归，再同步原型状态，之后才进入三端产品实现。生产实测仅一个真实账号，A/B/C授权隔离/执行/取消/交付仍待实施验收。
- 审查结束清理：两次独立生产审查的Chromium已退出；脚本在Browser.close回执处未退出，核对精确PID、命令、cwd且无子进程后终止本聊天两个只读脚本。未操作其他浏览器；原型预览unit仍active并保留。

## 2026-10-21 D3：按用户要求收敛为统一最小闭环

- Owner当前聊天。目标：重写详设/影响/工作项/验收，取消过度设计；非目标：产品源码、原型修改、生产操作或部署。沿原特性与证据目录，无新增任务/派工。
- 本地branch/tree及定向自检见 `evidence/d3-doc-check.json`。本地HEAD：root93f7e0a、API510b293、Web9dbd132；未查询新远端/线上、不把旧实页截图称为D3验证。重读原point-and-deliberate与assignForDeliberation，以及任务详情名册守卫；共享工作区其他改动未覆盖。
- D2.1六份合同文件原样保存在history/D2.1；当前spec/design/impact/tasks/acceptance/integration已整体换为D3，INDEX同步。复核报告保留事实但显著标记旧范围失效。
- 统一原point-and-deliberate和自动bootstrap，删除外单专属入口/启动模式/准备会话/独立delegation表状态机；扩展现有assignment/grant执行主体。资料沿当前任务整体授权和原版本快照，不另造外单选文件协议。
- 不做服务方列表/撤回/转单、新运行中取消或成本工程；保留原取消/停止含义。所有权、ACL、幂等、锁顺序和跨主体回报修正仍必需。
- 验收重新归组D3-AC01至16，全部NOT_RUN；旧58项仅历史。原型尚未同步本版，明确不声称已完成。下一步按D3同步既有原型，并在实际实施时确定现有身份来源、授权字段/锁顺序及资料版本覆盖。

## 2026-10-21 D3.1编码合同冻结
- 用户明确同平台=相同tenant_id+client_id，并要求按3小时开发目标补齐可编码详设。本轮Owner仍当前聊天，仅补文档，未新建实现任务、派发子Agent或操作生产。
- 定向读取原控制器、assignForDeliberation/assignLocked、grant/identity DDL、identity/PWE实体及测试入口；D3.1据此固定字段/政策幂等修订存储/接口分页与错误/锁顺序/修改点。原D3六份合同保存在history/D3。
- 删除平台映射未定项、资料摘要校验与重新确认要求；按提交时allTaskMaterials与原grant快照办理。无新增待指令、外单订单或第二套执行协议。
- 三小时为用户要求的开发目标，细分计划见design.md§10，不伪称正式Flow/生产验收能保证在时间内完成。本次未执行业务测试或发布；仍16组NOT_RUN。
- 后续实现直接按D3.1编码，不再询问已冻结业务规则；代码/诊断/Flow/上线分别记录。
- 文档定向自检通过：本地链接、围栏、尾空白、已撤要求及16组编号；本地branch/HEAD/tree和结果记录于evidence/d31-doc-check.json。没有运行Gradle/npm正式测试，不把文档检查当业务验收。

## 2026-10-21 编码启动（先编码、后统一部署验证）
- 用户已授权实施及随后统一部署验证。唯一集成Owner external-main；注册真实任务JYT-EXTERNAL-D31-API/WEB/CHAT-20261021。按项目MODEL_ROUTING的task/worktree并行规则，Web及Chat/Runtime为非重叠实现工作项，不设置Reviewer。
- API当前干净组件基线510b293，Web基线9dbd132；本次ls-remote确认两者develop一致。root及Web原型已有本聊天/其他任务未提交修改，保留。API主Owner仅改agent/**；Chat worker独立/var/tmp/cyf-external-chat-20261021，Web worker独立/var/tmp/cyf-external-web-20261021；各自提交后定向集成，不自动部署。
- 两个worker已显式收到项目AGENTS、工具入口、接口1.2固定SHA、D3.1及任务基线；读取回执写evidence/implementation。原型先更新后产品UI；主Owner推进authority/policy/grant/PWE。三小时为开发目标，实际结果和正式Flow证据分别报告。

## 2026-10-21 22:43 +08 编码集成与首轮Flow准备

- 主Owner `external-main`；沿用D3.1，未新增业务流程。真实任务 `JYT-EXTERNAL-D31-API-20261021`，协作Web/Chat任务见integration.yaml。
- API工作区已从原分支新建 `codex/external-commission-api`；主模块提交 `eb2b934422`，合入Chat提交后候选 `8273c0994a0b5be0262988ab8fdcfa2dc4ea7bd1` / tree `4b0f2d781b5c16da70e344aaa94df028b3da33df`。修改前API干净；未改根仓其他任务文件。AgentTaskAssigneeDTO保持原样，新增独立任务目标摘要。
- 自检补充：本人统计/旧任务列表只查询本人的任务，防止Agent接外单后读取他人任务或因混入他人任务报错；公开推荐不加载服务方任务明细。旧团队自动分派保持本人入口，外单仅走统一point-and-deliberate grant流程。
- 跨用户PWE保留A的数据域与B的Runtime认证，补充Skill start/effect/result commit及冒充/跨平台拒绝用例；尚待Flow执行，不能视为通过。
- Web候选 `e5192afd2fe799dd38f11ae07c456e72de4694e5` / tree `521493932f5d0fe930a856597f49ace3e98c8d01`；503项本地定向诊断通过，只是开发反馈。Runtime候选 `c11a078e0fc365c09706d569e0c668bcdb230d9f`，未激活。
- 22:42读取5260799无活动Run，备份配置到 `/var/tmp/cyf-external-flow-20261021/api-before.yaml`。临时CI配置只固定本次API候选、增加3个Chat回归、关闭push触发以避免重复运行；保留全部原policy argv、原分支准入及完整构建。写入readback确认，配置SHA `e629c3502c9accea9f212c51f115882fbe00eee4327eda932031a9f832880788`。**没有部署阶段、没有生产DDL/服务重启。** 结束需恢复原验证配置。
- 新增HTTP/MySQL真并发/运行时查询隔离测试及迁移preflight仍在本任务内收口；历史chat outbox缺grant引用不能从当前active授权猜回填。STOP在revoke后的原主体定位专项检查中。
- 正式结果、发布和业务验收尚无成功证据；本记录不将候选编码等同交付完成。

## 2026-10-21 23:12 +08 回归修复及迁移证据

- API Run217失败（1794 tests/3 failures/0 compiler errors），修复Chat Spring fixture、拒绝异常边界后合入；STOP只允许原grant单次terminal version增量，不放松普通callback。历史outbox增加四元授权引用，不改原context/hash。
- API Run218固定1f8a78d444c4c6e794a6ba712adcb6d43b9aed64：2807 tests/5 failures/122 skipped/0 compiler errors。真实新MySQL12项通过（含政策并发/共享锁/跨主体运行查询）；Chat authority14项通过。失败为旧PWE owner断言与fixture（两suite重复）及非法pageSize返回500。已提交cbfd347a62e6c58277ebedfca28d32f23f9d283d修复，保留全部原选择器并追加此前未执行的5个改动测试，下一轮重新验证；不能把未跑Skill测试称通过。
- 新候选临时CI仍无部署，配置/运行独立证据位于 `/var/tmp/cyf-external-flow-20261021/r2`、`r3`；结束恢复原api-before.yaml。保留原Gradle门禁，新增--continue收集全部反馈而非跳过失败。
- 生产只读迁移证据更新：14条本人grant可由不可变registry/已批准manifest/原owner-scope源码/时间序共同证明，迁移时冻结B=A；30条历史bounty dispatch可通过原bootstrap/admission证明，未猜current active授权。预检PREFLIGHT_PASS仅代表数据/catalog就绪，未执行任何DDL/重启。
- 剩余发布工作：同Run迁移包装、备份/停写/锁与前向恢复契约、最终Flow成功、Web1.16.37与Runtime1.2.3统一发布、真实双账号业务验收。前后端与Runtime尚未上线；现行版本未改。

## 2026-10-22 00:18 +08 单Owner发布与验证续接
- 2026-10-21 23:20按用户要求停止两子Agent，全部由external-main接管，不再派发。用户授权第二账号仅用于跨用户验证，不在文档、代码或日志保留密码。两个真实账号已登录，均tenant=0/client=jiafewnnv58ec2379c，owner不同。
- API 1.16.24：commit664b2576b49f277b3289c52e4eacf9d67f5d62ba/tree35c696b8706c67de47f1789002469414e7adb0f9，Flow5260799/221正式2887 tests、0 failures/errors、122 skipped，分层与fresh JAR通过；部署单71558570 SUCCESS。迁移14本人grant与30历史dispatch完成，原context保持；同Run归档SHA08fb5018809a9ed2712c008dd214bcedab70a51630bcf2a69b3d0f164d271c3f、安装JARe253757fead0c812fda20726aebd540aa82592dac7020db281bb454c6e859791，versioned-release-221 verified。默认仅CI云配置已恢复/readback。证据/var/tmp/cyf-external-flow-20261021/api-release，备份/home/isp/baks/jyt-external-d31-221-664b2576b49f277b3289c52e4eacf9d67f5d62ba。
- Runtime1.2.3：c11a078e0fc365c09706d569e0c668bcdb230d9f已推功能分支。精确unit温和停写，完整配置/HOME/SQLite及managedRoot压缩备份在/home/isp/baks/cyf-external-runtime-1.2.3-20261021；仅替换原制品路径，原配置校验通过。新PID186282真实cwd指向releases/1.2.3，三个subject当前通道注册/ready均true后更新current。业务验收尚未通过，记录active-business-acceptance-pending。备份/冷启动耗时已发生，不将active当业务成功。
- Web1.16.37 Flow4403172/282失败：3220 passed/6 failures/2 pending，未构建部署。原因是旧测试仍以名册推断task目标、无候选GET即允许canAssign及旧单参数源码断言。按D3.1契约修正四测试文件，未放宽产品授权；定向149通过。新commit44aa9c7159a7e9d0604c606776b790507e411932/treebcf1cc40be4dceac466afdcc9c445c0ed338159a已推develop，重新跑固定源码Flow；证据/var/tmp/cyf-external-flow-20261021/web-release-r2，完成后须恢复原默认配置。
- 尚不能报完成：Web正式发布、双账号真实委派/文本文件/继续交流与关闭后的新旧任务行为、生产资产摘要及最终验收记录待完成。浏览器仅记录method/path，不记录业务响应或凭据；生产测试仅操作显著标记的新测试任务。

## 2026-10-22 01:20 +08 双账号提交阻塞修复
- Web283正式3226 passing/2 pending已部署1.16.37；同Run产物及在线功能chunk核验完成，默认仅CI配置已恢复。Runtime三个subject已新PID ready。两个账号00/01/11/10候选、非owner政策拒绝、跨用户文本、带输入快照的图片编辑输出（真实红色PNG）、关闭后原任务继续、本人关闭仍可委派已实测；开关已恢复关闭。
- task499正式SUBMISSION_REQUEST停在PROMOTING，原outbox按原key重试，未新建提交或改生产数据。定位租约及聚合仍用任务A查AgentB的canonical身份。补统一TaskAssigneeAuthorityService task-scoped检查：数据始终A，live取当前active grant冻结B/binding，历史只验证冻结B canonical，不用历史授权live；无grant仅保留原本本人多Agent校验，不允许外部fallback。新查询精确平台/任务/owner/agent；不改变私域Workspace或本人团队Plan入口。
- 已增加跨owner lease CAS、聚合、grant失效/换绑/字段缺失及真实MySQL精确scope回归；尚未执行正式Flow，不标通过。API当前线上664b2576、待固定新候选；新发布不重复迁移，禁止旧JAR回退。整体仍IN_PROGRESS，3小时目标已超出，不能报完成。
- 补核对：task500实际承办为本人离线公孙胜，不是吴用；只证明离线可委派、尚未运行。已另建显著标记task501，在详情明确选择本人在线吴用并读回确认后提交；不把500当运行成功。账号/Agent名称均仅为测试输入。
- API修复候选494b3d38/Flow222：2932执行、4失败、122跳过、无编译错误。两处失败为新增撤销fixture未写DDL要求的撤销审计字段（两个source set），另两处为此次新增覆盖的旧Runtime-result HTTP断言仍读取raw响应。修正fixture及v1 envelope断言，不削弱生产约束，候选94b4c8a5重新走同选择器正式Flow。

## 2026-10-22 02:25 +08 发布核验与真实验收
- API1.16.25 / 94b4c8a5 / tree ba133c85，Flow5260799/223 SUCCESS、部署71561117 Success；2932执行、0失败/错误、122跳过。安装JAR SHA3cb830d8aa99b22aeafbe5399bf5f6da2df839b95f19c8e3e5c4b675bf1205be，versioned-release-223 verified，默认仅CI配置已恢复readback。本轮无DDL。在线记录见api-delivery-fix-r2/online-check.json。
- 498文本、499红色PNG的原提交均由原outbox自动恢复，无重生成或改队列；手机生产界面查看成果并确认验收，GET均COMPLETED/version4、delivery ACCEPTED；499刷新后摘要仍一致。正式外单闭环通过。
- 501本人测试原thread/start超时，本轮UI停止后GET原turn CANCELLED/USER_REQUESTED。新交流保留原key/body，503 TYPED_DELIBERATION_PERSISTENCE_ERROR（typed runtime unavailable），未生成新request，UNKNOWN意图未删除。不再同输入盲重试。
- 运行端当前三个通道ready但不证明typed就绪；吴用、林冲native polling报transport unknown，进程仍为186282。只读检查吴用pending/processing均0、测试原轮已取消；林冲另有DISPATCHED/recovery，故不重启共享unit。接下来仅核对吴用app-server子进程后做局部恢复，保留所有状态，不操作其他Agent。
- 主机磁盘96%，API memory索引报告flood-stage只读，此为旁路异常，未清他人数据/调低门限，不宣称为typed故障已证实根因。整体仍IN_PROGRESS，本人回归未通过。

## 2026-10-22 02:30 +08 核心闭环验收及风险保留
- 仅对精确吴用app-server PID188068做SIGTERM（确认父PID186282、CODEX_HOME/argv/cwd、服务端非终态turn=0、pending/processing=0），原supervisor启动PID244957；未重启共享unit、未清状态或重跑501已取消轮。
- 吴用skill catalog恢复CALLABLE；501新交流按原key/body得到202，新request3921225c…最终COMPLETED/PUBLISHED，typed ANSWER实际“本人任务正常”。生产UI“刷新处理状态”按原key取得原回执，UNKNOWN→ACCEPTED、显示真实答复，无重复首轮。
- 林冲现存DISPATCHED任务创建于2026-10-20 16:29:17（早于本次发布），本地recovery也是thread/start超时；当前polling异常仍在。没有动该历史任务/进程。局部恢复证明可恢复，不证明超时与重连就绪的根因已修复；不能宣称整个平台全部正常。磁盘96%与ES memory只读风险保留，不删除他人数据或降低保护门限。
- API223/Web283正式发布及498/499文本文件验收已闭合，501本人恢复实答已闭合。证据持久化到evidence/implementation/release-20261022。唯一下一步为隔离复现Runtime超时/重连声明问题并定位根因；无许可不清理林冲历史任务，不继续无变化生产重试。整体仍保留稳定性未闭环状态。
