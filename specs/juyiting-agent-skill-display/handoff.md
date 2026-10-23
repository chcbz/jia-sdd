# 当前接续：D4 / JYT-AGENT-SKILL-DISPLAY-20261016

> 2026-10-17执行已启动，以下首段NOT_STARTED等为准备时历史记录；最新状态以文末带时间的执行记录及integration.yaml为准。

核对日期2026-10-17；Owner本聊天Owner，没有子Agent/Reviewer。本文件为当前接续；历史调查细节保留D1—D3及原证据，不再作为执行指令。

- 目标：按已认可的完整原型优化点将册移动名册/详情、常驻底部动作、桌面分栏；展示真实技能/本领与单Agent只读刷新。
- 非目标：派单、市场/购买/安装、本领编辑、Runtime扫描或重启、数据库迁移。
- 状态：D4文档交付，产品NOT_STARTED、正式验证/部署NOT_RUN；真实执行ledger未登记；无实施worktree/受测候选/制品。用户已认可原型方向，不再标待UI审核。
- 当前文档：optimization-d4.md、design-d4.md、plan-d4.md、acceptance-d4.md。预计6应用＋6测试文件一次写齐；30分钟目标不是保证。
- 规则：AGENTS 2026-10-17；已查ops/orchestration/README.md；接口标准v1.2，SHA见design及baseline。两端正式交付Flow4403172/5260799，develop不自动部署，禁止历史后端本地正式路径。
- 基线：2026-10-17 10:29 +08:00查询。根HEAD22ff039；Web本地/远端c84c5a2；API本地c1e9792、远端拟基线58b4b5f。完整commit/tree及相关文件SHA在evidence/source-baseline-d4.json。API相关远端差异为测试，保留；agent-service/build.gradle有变化，运行前重读。根目录脏及Web AGENTS.md修改不得覆盖。
- 已核实：原本领投影唯一权威；旧名册/详情会进入CAS版本维护，不适合无副作用刷新；新增owner只读GET复用安装和Runtime核验，不删除旧abilities。Runtime历史证据没有本轮复查，线上状态未查。
- UI接线重点：原selectAgent同ID会取消选择，必须局部包装；Agent子层纳入返回/深度/标题与既有守卫；父deep样式与子scoped同时修；profile请求只在详情可见时启用。
- 原型：specs/juyiting-ui-baseline-20261006/prototype/index.html#agents；布局证据为该目录上级evidence/agent-roster-layout-20261017/final。原型PASS不是产品验收；当前源指纹见ui-review.md。
- 下一动作：进入实施时登记任务、固定双端基线和非重叠工作区，按D4一次完成应用及测试代码；之后统一双Flow验证及按实际授权版本化发布。本轮不启动执行。
- 真实阻塞：没有已知待决产品方案；尚未实施不是技术阻塞。未来动态线上数据和Flow/部署耗时只能执行时核验，不写死人名技能/完成保证。
- 定位/实现/验证/等待：未做连续计时，留空；不冒称30分钟实绩或上线。

## 实施启动（2026-10-17）

用户授权“落实下去，有阻塞及时汇报”。唯一Owner agent-profile-d4-owner/current_chat_owner，已读取根/组件AGENTS、工具索引、接口规范v1.2与D4；共享技能自动部署旧文不适用。
实际工作区 `/home/isp/wsps/worktrees/cyf-agent-profile-20261017/api` 和 `/home/isp/wsps/worktrees/cyf-agent-profile-20261017/web`；各组件分支 `codex/agent-profile-d4-20261017`；基线分别58b4b5f/tree3e60bd5、c84c5a2/tree398dfd6，已再次ls-remote核对一致。ledger已登记/claim。目标、非目标、验收、最早定向反馈沿D4，不变更全局规则或其它任务；尚无受测/线上版本结论。

## 完整候选 / 统一验证（2026-10-17 11:16 +08:00）

首轮完整代码已提交：API dfdc0a22b2f65b632b21c0f7828a15ad07de320d/tree45907c2f97b131a741d52654dce0cfb8a635929f；Web a1e0480a4f713ba7361a5f47387f4855345e75be/treea5b8985b11e8ba8e52955e251c1b738d1b458f9f。CODE_WRITTEN_NOT_VERIFIED，详见evidence/coding-candidate.json；从首次源码写入到候选提交约24分11秒，后续缺陷修复另计并更新，不是上线耗时。

实际写集额外3文件：chat/build.gradle仅测试依赖oauth-resource用于真实生产JWT过滤链；Web package/lock只升级发布版本1.16.8，无新外部依赖或运行时依赖。API当前线上只读record身份为1.16.7/58b4b5f，Web线上record为1.16.4/c84c5a2（不是新版本已上线）。Web本机26条定向诊断PASS，父SFC脚本/模板编译PASS；浏览器6视口PASS（真实AgentPanel＋真实父scoped CSS，合成数据/导航壳，非完整应用或线上），见evidence/browser/result.json。修复过同ID事件误接地图和720短屏高优先级padding覆盖。

下一步：双Flow精确候选正式测试/构建；统一版本批次1.16.8，同Run不可变制品，双端验证通过后再发布，禁止本机生产构建。当前尚未发布，也未声称后端测试通过。

## 正式验证阻塞与本次修复（2026-10-17 11:37 +08:00）

首轮API Flow5260799/148精确dfdc0a2：1108 tests，71 failures，37 skipped；失败全部在未改动的Agent模块10个测试类，失败夹具与该模块生产源码从58b4b5f到本次候选均无差异。它们阻止后续chat新测试执行，不能声称新接口通过。证据evidence/flow-first-failure.json。Web Flow4403172/221：3003 passing、38 failing、2 pending，全部失败为6个整页夹具loader漏接useHallAgentProfileCapabilities，本任务引入，已修复而非删除用例。

Web修复提交da59a4b8e98920386e7ab52a77463613c2ae5a92/tree0c40c37f577836bcb77778ac8a22bdbf43769ccd，已push feature/develop；6个loader注入真实composable，受影响整页诊断248 passing。本轮实际测试文件从6增至12，无新增应用文件。最新修复提交11:33:51，距首次源码写入41分43秒（包含统一验证等待；连续纯编码时长未单独采集）；**全部最终代码30分钟内完成目标未达到**，不再用首轮24分11秒冒称达成。

补跑API149保留全部原选择器并加--continue，用于获取当前新接口的独立验证及完整基线失败清单，不跳过/降级断言；Web222验证修复候选。两端均未释放部署作业。不得为上线自动合入另一任务c1e9792的84项测试删除；未核实的失败不擅称测试过时或业务无影响。

## 全量诊断与边界（2026-10-17 11:48 +08:00）

API149使用--continue后：2436次测试执行，133次失败，85次skipped（同一类可能在多个保留sourceSet重复执行）；另26处独立编译错误源位置，集中于deadline、User分页和conversation archive测试夹具。133次中3次属于本次两个测试文件的Mockito重复stub写法（替换已有thenThrow时when先触发旧异常，应用尚未被调用）；已用doReturn/doThrow修复至API945cb9ce56f99d10854a379fc3f9fe9a56475d81/tree825897e314de5adc2394bffcdb5df86b5b4afaf8，push feature/develop。剩余既有130次失败为110个独立用例，所有失败/编译夹具均未由本次改动。完整归因与各例见evidence/flow-root-cause-matrix.json。后端全量输入已失败两次，不再盲重试；未逐例证明是“仅测试问题”，不能放行生产。

Web222：完整默认CI测试3041 passing、2 pending、0 failures，生产构建及扫描作业SUCCESS；扫描SUCCESS不等于没有存量告警。同Run下载制品SHA2569b5327ffa2d8e12b8be3f897cf22675820c179835a3be23858dc6f2fb0668927，核对manifest366文件、源码commit/tree和内置Mocha报告一致（evidence/web-flow222-artifact.json）。未发部署；为避免占用发布等待，确认本任务CI成功/部署SWITCH_MANUAL及源码后停止本任务Run222，终态CANCELED不改写为整Run发布成功；CI作业仍SUCCESS。Web流水线已准确恢复原CI-only配置并readback。

本次3个新增测试类已能运行，20/23通过，失败3项为上述fixture，不能在修复后未经云端运行声称23全通过。API150明确是**定向诊断**：更改后的候选上验证3个新类及原安装/策略/owner/AgentService回归与layering，无制品步骤、无部署阶段；不是删去全量失败后拿绿灯发布。已保留完整原全量失败证据/测试源码/发布验收要求，待基线真实修复才能重新全量交付。

浏览器新增320×568，共7视口通过；增加滚动前的实际技能/本领文字断言与detail-top截图，原detail图仅长内容滚动后按钮几何测试（大量空白为人为2000px压力fixture），不作为产品首屏视觉图。仍只是实际AgentPanel+父scoped CSS/合成数据导航壳，不是线上或完整JuyiHall浏览器验收。临时预览及自有浏览器均已停止。

最终源码提交11:44:58，距10:52:08首写自然耗时52分50秒，含云效/诊断等待。连续活跃编码时间未单独采集，30分钟全部最终代码目标未达到；evidence/coding-final.json为当前计时，不篡改首轮记录。发布版本1.16.8仍为候选，生产无变化。

## 当前结论（2026-10-17 11:52 +08:00）

- 当前功能代码已提交且远端develop已集成：API945cb9ce56/tree825897e3；Webda59a4b/tree0c40c37f。两隔离工作树干净；根/主组件工作区和其它任务修改保留，未更新根gitlink冒充已正式发布版本。
- API150明确为定向诊断SUCCESS：179 tests、0 failure/error/skipped，3个新增类23项全过，其余为原owner解析、AgentService本领投影、安装与任务策略回归；validateLayering真实执行PASS。见evidence/api-flow150-focused.json。它无最终JAR/制品上传/部署，不替代原完整发布要求。
- Web222 CI/test/build与扫描作业SUCCESS；原Run为防止未释放部署长期占用而CANCELED，非发布成功。3041 PASS/2 pending、366文件制品完整性及SHA已核验；7视口实际组件合成数据浏览器通过。
- 阻塞：API149既有110个独立失败用例（跨保留任务130次失败执行）及26处测试编译错误未修。不能证明仅测试债，不绕过、不删除、不移用另一任务删例提交、不第三次盲跑同一基线。需要先按当前统一接口契约修复基线并取得完整正式Flow验收，再恢复原版本化同Run发布批次；当届时源码变化，应重新固定真实候选/制品，不把本次诊断Run150当发布制品来源。
- 本次无生产应用发布/重启、无DDL/交易/Runtime扫描。只读确认API现行1.16.7/58b4b5f正常且healthUP，Web现行1.16.4/c84c5a2/Run220；见evidence/production-unchanged.json。无线上新GET或新UI验收，版本1.16.8仅候选。
- 编码30分钟目标未达：首次候选24分11秒，最终修复提交自然耗时52分50秒（包含验证等待）；实际文件为6应用＋12测试＋3配置。
- 稳定源码边界已回写既有docs/juyiting-runbook.md，未改写其它模块的旧基线。完整源码/失败归因/后续动作保存在本目录，无新Reviewer或新流水线。

收尾回读（2026-10-17 11:54 +08:00）：两流水线均恢复执行前原配置，完整分页查询无活动Run；控制面恢复证据evidence/flow-config-restoration.json。再次ls-remote确认develop分别为API945cb9ce56、Webda59a4b；ledger为blocked_dependency且已释放Owner，不标accepted/done。后续先处理原发布回归基线，再按重新固定的真实输入正式验证与统一部署；本轮不再继续盲跑。

## 用户续行／本地develop整合（2026-10-17 12:04 +08:00）

用户核对分支后明确“继续”。Owner仍为current_chat_owner；不改原功能范围，不再重复修复已有处理。API隔离分支codex/agent-profile-d4-20261017将本地develop@c1e97923bf与原feature@945cb9ce56无冲突合并为b76a1d0aeda572767a6d4734d050121d985bd9c9/tree82b7ff2f49d23ec99af3a190ba1433b3704c1780。此前基线未纳入本地8个提交是集成遗漏；不是本轮业务代码制造26处编译错误，也不再把已存在处理称为尚待从零修复。

已有基线包含历史用户授权删除84方法，属于继承的已知覆盖缺口，**不是本轮新修复或原未裁剪套件等价证明**；本轮新删0，不再删例换绿。源码及原基线证据见evidence/develop-integration.json、BACKEND-FLOW-5M-20261016原handoff。合并相对c1e仅增加原功能7文件；原功能生产字节未变。本轮应以合并后精确commit/tree重新跑原完整现行Flow任务+新增profile/安装/策略测试，validateLayering与fresh bootJar/同Run制品，不能复用Run147或150当新候选验收。Web源未变，可复用222的精确CI证据，但统一版本部署仍需同Run有效部署链及在线核验。主工作区无关修改保留，生产未改。下一动作为固定并push合并候选、更新既有Flow发布配置（前值备份/readback/无活动Run），执行统一验证，再在原授权内按API→Web版本化发布；不走本机构建或历史源码发布工具。


## 完整验证通过与发布控制调整（2026-10-17 12:23 +08:00）

API151在合并候选b76a1d0aed完成全部现行发布选择器及新增profile/安装/策略回归：2428次执行，2333通过、0失败/错误、95条件跳过，260 suites；validateLayering及fresh bootJar真实执行PASS，Gradle202.814秒。26处旧编译错误不再出现。Web223正式默认套件3041通过、2 pending，生产构建/扫描作业SUCCESS。两端同Run制品已独立下载校验，见evidence/api-flow151-artifact.json及web-flow223-artifact.json；历史84删例及95跳过不宣称恢复覆盖。本轮新删0。

两个Run部署作业为Owner统一验证后的SWITCH_MANUAL，不是额外人工审批。官方RetryPipelineJobRun对本任务API151待手动作业返回success，但只读复核仍未执行；没有重复调用、不假称部署完成。只停止本任务尚未部署的151/223，保留CI成功/制品证据，整Run终态CANCELED。改本次固定版本原生VMDeploy自动执行，仍禁用源码push触发且固定相同commit/tree、同Run fresh制品/完整回归/适配器。此处因控制面实际阻塞而重新生成发布批次，不把先前构建冒充新Run制品；现行默认develop仍不自动部署，最终须恢复原CI-only配置。

发布候选还核对并使用既有原生主机组绑定yjctjhskhk1ti9t4（实际主机组28833），不沿用只在待审核候选中存在的数字标识；原生下载使用本批独占固定暂存目录，在Flow作业内移动到该Run目录后交给既有五参数适配器，避免artifactDownloadPath字段的shell变量展开歧义。未修改任何主机helper或绕开发布锁。API152已启动，Web下一发布Run只在API安装/健康与只读业务核验后启动。

发布前旧local-build-v1记录的schema plan因历史摘要闭包local_published_closure_invalid拒绝，符合既有目录迁移未闭环边界；没有修改旧记录/权限绕过或假称历史绑定通过。另使用既有F06固定只读metadata函数核对两张表均existing equivalent，无DDL/DML（evidence/predeploy-schema-metadata.json）；新Flow安装有自己的来源/receipt/制品闭包，沿既有安装器新版本事务，不依赖伪造旧闭包。此时生产仍旧版本，未触发schema apply。

发现已有JYT测试账户配置，已通过正常授权码+PKCE取得本任务独立会话，只读名册13项；不伪造JWT、不借用其他聊天session。凭据/令牌只留私有临时目录，公开证据只留摘要。将用于上线后的真实GET/完整应用浏览器验收，结束清理临时会话。


## 版本化发布事实（2026-10-17 12:42 +08:00，浏览器验收尚未收口）

API5260799/152、Web4403172/224均为本次固定版本1.16.8的真实SUCCESS，原生部署单71288035/71288193各1台机器Success/healthy。API152现行完整选择器2428执行=2333通过/95跳过/0失败错误、23项新例全过，layering和fresh bootJar通过；Web224为3041通过/2 pending，扫描SUCCESS。不是把151/223的制品挪给新Run。152 archive939268c1433669f887e711f95fb9c3cb7867f08f6dd6d2ec0be3eabb884df741、JARd487704e014b1cfcb631c90a484f9f27a404cb24a9cbcc5368b50f5ef1dc3cc0；224 archive2793e16059b9d7e92207dc0d8b178e8bc6ab15a0882babf446f715452b84d23d。

API canonical安装/receipt/现行record均与152一致，healthUP。F06原schema apply在两表existing_equivalent直接通过，无DDL/DML；不因此宣称旧历史闭包被修复。重启前签发的测试JWT因key不匹配401，新正常PKCE登录后5 owned GET200、本领与原投影一致、非owner404、missing/invalid JWT401，私有no-store。Web366个安装文件与同Runmanifest逐一一致；公网入口及8个直接引用/聚义厅资源共9文件字节摘要一致，见evidence/api-release152.json、web-release224.json、online/api-result.json。

已分别在无活动Run/精确候选未被别人改动的前提下恢复r4的原CI-only配置并readback，见evidence/flow-restored-5260799.json、flow-restored-4403172.json；develop不自动部署。

完整浏览器前几次诊断先后受新手引导初次显示、身份初始化/重新挂载及脚本过早点击影响；这些尝试保留FAIL，不算产品通过、不修改业务或合成页面。真实owner名册使用POST /agent/roster，仅5 owned项，不是/agent/list的13项；线上无nonowner卡片，不能造一行测试。正常操作关闭引导并等待真实身份/名册后继续实际组件检查，尚不提前accepted。

并行任务正在迁移原型，已自然接续读取最新web/AGENTS.md；现唯一入口/home/isp/wsps/cyf/web/prototypes/juyiting/index.html。当前迁移和额外样式变化不纳入本次已批准/已部署候选，不覆盖或合入该任务AGENTS/原型脏改动。旧D4审批摘要继续是历史审批输入，不改写成当前新原型摘要。

安全事项：先前云效诊断曾误回显消费仓库凭据，已停止相关输出、原始配置/响应限私有目录、未写入公开证据；已主动告知用户建议轮换，不擅自执行凭据变更。


## 最终在线验收收口（2026-10-17T12:47:52.083902+08:00）

完整生产应用5视口1440×900、390×844、320×568、390×480、720×480通过，28个实际profile GET全200，无Runtime exception；短屏320/390/720实际内容分别滚动197/249/185px且footer不动、按钮命中可达。移动端正常“我的→好汉名册”入口，返回/关闭/同ID重入均通过。真实名册仅5本人项，无nonowner行；该UI场景NOT_APPLICABLE，真实API404另有证据。详见evidence/online/result.json及真实截图，不复用合成壳替代。

诊断失败分别归于引导/身份初始化/导航尚未换文档/移动入口/skip按钮重挂载，修正的是本任务诊断：等待新loader完成、关闭实际引导、等待身份和名册、移动从真实入口进入及原子点击。没有产品代码变更、没有新正式Run，保留每次FAIL为diagnostic，不把历史尝试篡改成功。/agent/roster的只读查询是POST标准查询信封，不误用GET /agent/list的13行作UI输入。

源码分支仍主组件develop与已push feature；b76/da59、tree82b7/0c40，最新ls-remote一致。Web现有AGENTS内容在发布期间由并行原型任务更新，未覆盖该脏改动；已读取新规则，原型新唯一入口只更新指向，不纳入本次组件commit。运行目录规范8项只读测试通过。两条配置已原值恢复，develop无自动部署。

正式交付、在线范围和剩余边界汇总release-1.16.8.md；integration标accepted/released_verified仅指本任务范围，不代表历史删例覆盖/其它模块问题解决。

测试会话清理（2026-10-17T12:48:22.522491+08:00）：已删除本任务r4/r5两个PKCE令牌文件和两次早期诊断遗留的自有Chrome profile，成功浏览器profile由harness关闭删除，无其他任务会话/进程操作。见evidence/session-cleanup.json；原始云效配置/状态/日志仍仅0700私有目录保留。

## 用户反馈视觉复核补充（2026-10-17 14:40 +08:00）

用户反馈“效果跟交互原型还是有些差异，再核对一下”。本轮Owner仅做只读视觉审计，不接管其他任务的原型／脏工作区；范围固定为点将册，接口规范v1.2不变。线上安装、本地HEAD及实际查询远端develop仍da59a4b／1.16.8／Run224。当前原型独立记录摘要，不冒充D4旧输入；主要差异在旧批准截图已存在，不能归因于原型后续更新。

已在实际完整应用与当前原型三视口1440×900／390×844／320×568核对名册／详情，记录12组计算样式及截图，另补真实图片解码后6组生产观察。确认密议未通栏朱红、移动详情仍内缩卡片、刷新及技能层级近似值、关闭图标／目标尺寸、招贤按钮排列等未落实。上次滚动／功能通过不等于视觉一致。头像初始红圆为尚未显示图片，资源HTTP200且decode成功；但大PNG与缩略图及flex收缩差异需优化，不宣称永久缺图。技能名和16项真实本领不同于原型属于数据事实，不改造数据。

详见visual-audit-20261017.md及evidence/visual-audit-20261017/。本轮未修改产品或原型、未测试构建发布，不重标原accepted功能历史为完整视觉验收。后续最小修复仅AgentPanel、JuyiHall限定选择器及现有测试，前端Flow验证／发布；API／数据库／Runtime不需变更。

14:42审计收尾：原型前后指纹一致；只写本任务审计文档和证据，生产／原型代码未改。本任务PKCE令牌文件已删除，自有浏览器及本次18786静态预览已关闭，未操作他人会话。见final-readback.json与session-cleanup.json。

## 1.16.9 小范围视觉修复启动（2026-10-17 15:35 +08:00）

用户明确授权“做一轮小范围修复，完成后发布”。沿用任务JYT-AGENT-SKILL-DISPLAY-20261016，唯一Owner本聊天，ledger从accepted重新进入本轮implementing；原1.16.8发布历史保留。工作区/home/isp/wsps/cyf/web、develop，base commit da59a4b8e98920386e7ab52a77463613c2ae5a92／tree0c40c37f577836bcb77778ac8a22bdbf43769ccd，远端develop实际查询一致；线上仍Web1.16.8／224、API1.16.8／152。API无变更，本轮仅Web版本1.16.9。

范围：AgentPanel.vue、JuyiHall.vue中Agent专属样式／关闭入口、现有对应测试及package版本；依据visual-audit-20261017.md。非目标：接口／数据库／Runtime／派单、其他页面主题、当前完整原型变更。保留web/AGENTS与原型及根仓其他任务脏修改，不stage这些文件。验收：三主视口视觉+720断点两侧／短屏、单双动作权限、长ID／本领、刷新及返回关闭；最早反馈现有挂载组件定向用例与真实组件开发预览计算样式，然后一次固定候选Flow4403172正式测试／构建／同Run部署与生产复核。接口规范api/docs/interface-standard.md v1.2未变。

## 1.16.9 固定候选与正式Flow启动（2026-10-17 15:49 +08:00）

仅6个目标文件已在Web develop提交并push：6fbdb6618b1132316a95db87cca9402de83138e8／tree212194b370ec40c2c8b1e4184ad09c5f01c1a3bb，实际ls-remote一致；未带入其他任务AGENTS／原型。133项本机定向诊断、8视口真实组件+父CSS检查通过；AgentPanel lint无问题，JuyiHall历史111 errors/82 warnings与base一致，本次新增0，不声称全量lint通过。SVG属性排版后仅补静态断言，无视觉变更；诊断与最终文件SHA绑定见evidence/visual-fix-1.16.9/local-diagnostics.json。

写配置前已分页核对无活动Run、原CI-only配置精确匹配；备份在本任务0700目录。仅4403172更新为本轮1.16.9 commit/tree固定候选，触发事件关闭；start一次得到Run225，随后详情commit确认为6fbdb66。正式测试/构建与扫描后只消费225制品在Flow原生主机部署，不本机构建/部署/升级helper。API仍1.16.8／Run152。尚需同Run制品校验、安装/公网与真实浏览器验收、恢复配置。发布输入见release-input.json，不把阶段SUCCESS当成完整发布。

## 1.16.9 发布及最终线上核验（2026-10-17T15:57:16.738908+08:00）

Flow225 SUCCESS，CI537043473／scan537043474／deploy537043475全SUCCESS，部署单71293772，1台Success/healthy。3045通过、2原有pending、0失败；同Run archive38ffacf954924f275f38e6b0deed446aed9d54e2e7c5971203ae348e3f043a87，366安装文件/9公网资源一致。真实完整应用7视口全部通过，36次profile GET200，无Runtime exception；刷新、返回同ID重入、关闭及footer命中可达通过。头像已等待decode后截图，实际缩略图68px显示正常。真实数据与原型示例的16项本领/图片编辑差异保留。

本轮配置已分页无活动Run后精确恢复并readback；develop不自动部署。只读验证，无任务/会话创建、交易、扫描、Runtime或API部署。本任务PKCE令牌已删除、线上浏览器profile已关闭清理、自有18791预览按精确cmdline归属停止。详见release-1.16.9.md及evidence/visual-fix-1.16.9/；原1.16.8历史不改写。稳定知识只局部更新既有runbook，根仓仅收本任务文档/证据和Web gitlink，不纳入其他脏改动。
