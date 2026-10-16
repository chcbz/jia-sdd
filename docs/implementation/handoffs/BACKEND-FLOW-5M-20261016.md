# BACKEND-FLOW-5M-20261016

Owner backend-flow-5m-main / codex。用户授权尝试优化与实测；先无部署，未授权任意版本生产重启/资源采购。状态以TASKS.yaml为准。

- 范围：现有5260799，固定源码、原默认测试集合、JDK准备计时、compile-only缓存对照；不创建流水线、不减少测试、不覆写其他Owner修改。
- 根基线e05498ed8f8d67d791ad8d269ae5bbc00b3592e6/tree3e7418605fef2d518aa9b04643c9936dd9a06abc，develop，工作区已有脏修改；本任务只新增独立helper/测试及记录。
- API基线58b4b5f408257c6d5103d915e13c7927c1571e20/tree3e60bd5858735790b7886ef00a9a94614816fb75，2026-10-16只读ls-remote一致。不把当前源码当线上或Run139受测源码。
- 工具/规则：/home/isp/wsps/cyf/AGENTS.md、ops/orchestration/README.md、ops/ci/aliyun-flow/flow-control.cjs；api/docs/interface-standard.md 2026-10-14冻结版，无接口改动/子Agent交接。
- 证据目录 docs/implementation/evidence/backend-flow-5m-20261016；私有配置备份/候选 /var/tmp/cyf-backend-flow-5m-20261016（0700，原值0600）。配置中原triggerEvents为push，只验证无部署；实验临时置空，结束恢复匹配原值，不静默永久修改触发策略。
- 原因新证据：/var/tmp/cyf-ur-flow-r16-20261008/run139-log-read5.json保留实时中间片段；19:28:46准备→19:48:58 RPM完成，共1212秒；41MB headless包6分53秒。常用curl/tar/git/python已存在但dnf还升级，不能把这段耗时归给Gradle缓存。
- 最早验证：bootstrap合成归档安全/缓存回归；Flow固定源码无部署运行，真实worker验证JDK ABI、原selectors、layering/fresh bootJar。随后同SHA新Run测热缓存，不伪造新Run、生产回执或完整发布达标。
- 设计：只缓存固定SHA压缩包、逐次验证并新目录解包；不执行缓存解压目录。JDK选官方Dragonwell Extended21.0.11.0.11+10（与Run139 RPM+21补丁构建不同，显式记录，不能作为单变量纯缓存对照）。首次运行与第二次保持同JDK。
- 云端Gradle通过原orchestrator串行入口；固定控制工具与本任务授权快照传入独立临时目录，快照只作本Run输入，不是可写权威台账。锁与源码清洁检查保留；不复用整轮成功证据。
- 完成口径：构建测试通过不等于部署。端到端300秒要另绑定实际版本、同Run制品和线上核验；排队、冷/热缓存分报，无性能强制deadline。

## 实验进展（2026-10-16）

- Run140：GitHub下载socket timeout，Gradle未开始。改官方Dragonwell OSS镜像（同官方SHA），不重复相同输入。
- Run141：官方OSS冷下载/校验/解包/Java和javac版本检查6.138s；编排器调用参数误放task_id后被REMAINDER吞掉，Gradle未开始。修正为选项→task_id→命令，并调用原parser做无副作用自检。
- Run142：JDK冷准备6.470s，原编排器真实Gradle18.370s，失败于旧Flow引用已删除的chatDeliberation task。源码5d54634a3d在10月15日删除过时suite并迁移保留输入，不重新引入兼容任务。
- 修正映射：现src/mmdRegressionTest/java全部50源文件由7个现行task覆盖，49测试类按类去重，每类仅一个task运行；保留原所有其他selectors，补src/test内迁移的ChatConversationEventsHttpTest、SkillExecutionDeclarationTest。完整映射见私有chat-suite-map.json和chat-suite-dedup-selectors.json。新实验不是Run139原套件的同输入对比。
- 未运行历史Run139专属UR03跨客户端fixture；不据当前默认套件宣称旧UR03失败已修复。
- 只读观察现行本地发布1.16.7、同58b4b5f源码的已有日志：Spring Started56.107s、process-at-Started58.109s。不是本任务安装，Started不是完整installer/业务ready。
- helper合成安全测试12项PASS；真实Gradle/cache/端到端仍待终态。没有生产启动/停止、DDL或本机Gradle执行。

## 本轮收口（不是五分钟目标完成）

- Run143 FAIL：从创建到作业结束134秒；JDK6.697s，Gradle105.118s。JUnit部分任务图实际1086项=978pass/71fail/37skip（86 suites，失败集中10个suite）。agent service子集1000项=71fail/37skip。测试失败后后续测试/layering/bootJar/制品/部署未获验收；不把2分14秒失败当成功发布提速。
- 失败清单`docs/implementation/evidence/backend-flow-5m-20261016/run143-tests.json`来自日志诊断gzip分块，解码后SHA匹配。已见旧JSON path、HTTP状态、反射签名等与现实现不符；SkillMarketplaceRealTransaction等也失败，不把全部71项武断归为只改断言即可，须按2026-10-14冻结规范逐项判断实现或fixture问题，保留ACL/事务。
- 本轮不扩展到10个业务suite的协议迁移/事务修复，不删除测试、不重跑同失败源码，也不伪报热缓存效果。状态`blocked_dependency`，不是accepted/done；下一动作是修复该固定基线失败后，在新精确源码重新进行冷/热对照，再绑定明确版本实测部署。
- 独立工具自检12项、原控制面Python静态7项/Node13项PASS，总32项工具检查；不替代业务测试。初次控制测试文件名未命中、实际0项，没有作为测试证据；后来运行正确文件得到7+13项。
- 21:19:33+08:00恢复前确认无活动Run、当前配置仍为本任务candidate；经原flow-control单次写回原值并readback，原SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a完全一致，见restore-result.json。不保留临时branch默认值或关闭push触发状态，不启动恢复后的Run。
- 私有完整候选/配置/实际调用/日志分别位于/var/tmp/cyf-backend-flow-5m-20261016/{r2,r3,r4,restore}。固定实验远端分支codex/backend-flow-5m-20261016仍指58b4b5f，无API源码改动，不删除证据ref。
- 生产仅执行一次原helper status，只读PID/监听归属/健康和制品证明；本任务没有安装、重启、SQL或修改其他聊天进程。
- 定位/实现/验证/等待未独立计时，不编造开发效率收益。已证明的是JDK准备路径可压到约7秒，不是整条流水线成功或端到端五分钟。

## 十分钟定向修复（2026-10-16 21:50，用户授权）
Owner backend-flow-5m-main；API clean base58b4b5f，隔离worktree `/var/tmp/cyf-flow-testfix-20261016/source`，分支codex/flow-testfix-20261016。仅修测试fixture、保留ACL/真实事务；不修改生产、不部署。最早验证为5个已明确根因的suite及validateLayering；其余不以删除掩盖失败。

21:59十分钟窗口收口：修正候选51a6410ec02e0fcbb82c8516f0b160eaeea1587d覆盖原32项失败（5类），没有改业务源码。真实本地验证经orchestrator串行、既有受限构建cgroup执行，第一次新输出0755被原metadata拒绝，归因后仅修自有目录0700；第二次尚在test阶段，不能声称32项已经PASS。日志与输入 `/var/tmp/cyf-flow-testfix-20261016/{test.log,input.json,result.json}`（result须确认commit和日志对应；首轮失败记录不代表第二轮终态）。
用户最新明确“10分钟修不了就删掉”作为本次删除授权，覆盖之前本任务默认不删测试的范围：第二个隔离候选d70a0f41e6在51a6410之上仅删除其余39个失败测试方法，保留类/辅助方法/其他用例；其中含10个Runtime安全回归，明确存在覆盖缺口，绝不记作修复或验证通过。完整逐例清单`docs/implementation/evidence/backend-flow-5m-20261016/testfix/removed-tests.json`。路径 `/var/tmp/cyf-flow-testfix-20261016/trim-source`，分支codex/flow-testfix-trim-20261016。未合入develop、未push、未部署；删除候选尚未编译/验证，不复用51a6410的测试结果冒充其验收。下一步读取本次既有验证终态，再对最终候选做一次原流程验证；不继续盲目删减或重跑。

## Flow144真实复测（2026-10-16）
用户明确授权删除剩余失败并重跑Flow计时。局部本地51a6410最终72项/71通过/1失败（事件occurredAt字符串断言），并非全绿。新候选aca649bac2383a9054b2891ba930c7fc203d1f61/tree7f36c14ba95bf54b1d20c71583c83d298ec386fd删除该最后方法，累计40项删除，清单testfix/removed-tests-flow144.json。独立分支codex/flow-testfix-trim-20261016已push，未合入develop。复用原工具及JDK方案，无部署；临时配置已备份并readback，Run144已启动，实际source仍需实时核对。私有过程证据`/var/tmp/cyf-backend-flow-5m-20261016/r5`，结束后恢复配置，不将40项删除当修复或原套件等价性能。

Run144终态FAIL：22:07:42创建→22:10:28作业结束，总166秒（2分46）；JDK冷准备6.265秒，Gradle136.439秒。云端压缩诊断SHA fcecc35c156f6d3b6c50ff7d4fa39904551305d788c659b6be37fd07afdb7b30已重算匹配，实际commit aca649bac2383a9054b2891ba930c7fc203d1f61/run144匹配。部分任务图1278项=1224pass/16fail/38skip；agent mapper86全PASS，agent service960项/0fail/37skip，base32全PASS，chat200项/16fail/1skip。新失败位于7个Chat/WebSocket/Voice套件，不是原40项复发。保留授权删除40项的覆盖缺口；不将166秒失败当完整构建/部署达标，未产生成功制品。只启动用户要求的这一次Flow，未再删新失败或重跑。
22:12:21+08:00无活动Run/配置仍为本candidate核对后，原flow-control已恢复原配置并readback，SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a完全一致；未部署、未改生产。正式摘要与16项失败见testfix/flow144-{timing,tests,restore-result,candidate-proof}.json及flow144-phase-timing.log。独立源码分支已push，不合入develop，任务仍被新测试失败阻塞。下一步需对这16项做明确处置后才有成功完整计时。

## 16项Chat失败十分钟续修（2026-10-16 22:31:54+08）
用户授权先修复、到时未修复逐项删除。唯一Owner/backend-flow-5m-main，沿用隔离trim-source和codex/flow-testfix-trim-20261016，base aca649bac2/tree7f36c14b；仅7个测试类，不改业务/生产。按2026-10-14 interface-standard固定规范修Q/R、WS messageType/data/correlationId、金额/分页/时间与真实错误HTTP；取消测试允许现行startup帧并继续核验取消传递，不延长超时。最早验证复用原Flow完整候选，结束恢复共享配置。

续修首轮源码eb4da1fad322f9e3d997f7e6bdc2f259648bdfd4，Run145 FAIL总170秒；原16项Chat失败全部通过，未新增删除。部分任务图1347项=1308pass/1fail/38skip，新失败是common RequestIdFilterTest.generatesNewIdForInvalidClientValues：现行非空无控制字符契约允许旧测试列入invalid的short/space/slash/129长度值。新固定提交bca14e2fe73dd00402ed3fdfc51adc50d34a120e/tree2d445cb5e4f5d3c0cf75744586377aeda892b850将这些值列入正向回归，负向输入改null/空/空白/换行/回车/Tab；保留requestId替换/响应关联和MDC断言。22:41:43完成代码提交（从22:31:54起9分49秒），本轮0项删除。
Run145已终态后无活动Run核对、restore/readback恢复原配置；Run146对bca14e2fe7已真实启动。十分钟限制用于修改窗口，后续只等待该固定候选云端验证和恢复；不是声称十分钟已全绿。源码仍只在独立候选分支，无develop合入、无应用部署。证据r6/r7，Run145正式摘要testfix/flow145-*.json。

Run146终态FAIL总164秒（2分44），JDK6.445秒，Gradle135.493秒；诊断确认bca14e2fe73dd00402ed3fdfc51adc50d34a120e/run146。已执行1347项=1309pass/0fail/38skip，原16项及新RequestId用例均通过，本轮新增删除0（此前40项删除仍保留覆盖缺口）。随后common:jia-common-starter:compileTestJava失败，RequestDeadlineExceptionHandlerTest.java34/53两处仍调用已删除JsonResult.getStatus()，日志重复6条但只有2处源码错误。该新阻塞不算原16项复发，不继续扩大修复窗口或删新用例；完整编译/后续测试/layering/bootJar/制品未获验收。没有应用部署；源码仅候选分支，未合入develop。下次应修该公共测试的HTTP状态断言后再做完整流水线，不能拿本次0fail部分任务图当全绿。Run146共享配置已无活动Run/候选一致核对后原flow-control恢复并readback，原SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a；证据testfix/flow146-*.json。

## 本地完整Flow范围批量验证（2026-10-16 23:20—23:30+08）
用户授权十分钟修复、到时只删除已确认失败且未修复用例；不删除未运行用例。本轮不触发Flow/不部署。Owner不变；本机隔离trim-source base bca14e2fe7，远端develop于23:20只读核对仍58b4b5f。新候选371418514e修正deadline的两处已移除status断言，保留真实503/504并补protocolVersion/requestId；恶意关联ID fixture改CRLF，保留真实控制字符拒绝检查。规范v1.2不变。
复用既有本地runner及消费者init/metadata，原orchestrator串行锁，1.5GiB自有cgroup、单worker/384MiB测试堆；从Run146脚本机械提取全部任务及--tests，无漏选/新增忽略，增加--continue批量收集独立模块失败。输入、运行日志和结果在`/var/tmp/cyf-flow-testfix-20261016/local-full/`。本机JDK/资源与Flow不同，测试范围对齐不等于云端环境字节等价；无外部数据库凭据时条件skip须如实报告。正在执行，不称全绿。

23:30十分钟修改窗口到期：当前报告1514项/0fail/38skip，已知编译错误已修，本轮删除0。全流程仍执行（starter及后续自定义sourceSets），仅继续等待/收集；不把耗时或部分报告当全绿。到时后新增确认失败按用户授权删除，不继续无限修复；受测源码在运行期间不修改。

23:40首轮完整批量终态FAIL，Gradle1126.409秒（18分46秒）；2351项=2232pass/34fail/85skip，user-service和chat归档测试源编译失败，其他独立任务继续完成。不是十分钟内全绿，未运行的编译阻塞套件不算通过。23:42按最新明确授权删除43个方法（34运行失败+9编译受阻），另删一个只被删除方法调用且自身编译失败的helper；删除包含12个Redis端口冲突的本机fixture失败、ACL/事务/WS回归覆盖缺口，不能说业务已修复。累计历史40+本轮43=83方法删除。清单testfix/local-full-removed-tests.json。
删除候选bb56574908d45e71580c5638b83ac65ac807b7b4/treeaab8ffc3e04c4de3e14040608b0770b278e92fa9；仍隔离分支未push/未合入develop。使用同31任务/192selectors、fresh输出在local-full-final进行完整本地复验，不变业务、不新启Flow、不部署。

额外静态边界：RequestIdFilter已接受非空无控制字符的不透明ID，但TimeoutErrorContract仍使用8—128位字符白名单；本轮将“恶意ID”fixture改为确实无效的CRLF，未修生产端两种校验的潜在不一致，不能以该fixture通过声称任意合法opaque ID的超时处理均正确。此项不在本轮业务源码修改范围。

23:53第二轮完整本地复验耗时625.945秒，全部测试源编译通过；2384项=2288pass/1fail/95skip，仅剩此前编译阻塞而未执行的ChatConversationArchiveControllerTest.statusMapsOnlyTheScopedReadAndNeverInventsRecoverySideEffects：旧domain Receipt与现wire ArchiveReceipt直接比较。23:54按既有超时删除授权删除此1方法，保留该类HTTP错误状态回归及其他未失败用例。累计本轮44（此前40，合计84）删除，不记作功能修复。候选c1e97923bf2325e3ada33b7e2816f203630f020d/treef192948af6ff27b4e78f6f1585aca9bd8a6b4968，最后一次完整本地确认目录`/var/tmp/cyf-flow-testfix-20261016/local-full-confirmation`；尚未终态，不声明成功。

## 本轮本地收口（2026-10-17 00:04+08）
最终c1e97923bf2325e3ada33b7e2816f203630f020d/treef192948af6ff27b4e78f6f1585aca9bd8a6b4968完整本地SUCCESS：2383项=2288pass/0fail/95skip；全部31个指定任务EXECUTED（含validateLayering/fresh bootJar），公共制品安全及POI运行时测试也执行。Gradle子进程512.617秒（8分33），自身报告8分27；不是Flow耗时。合计三轮本地验证，整体处理超过十分钟，不能声称一次或十分钟完成全量修复验收。
本轮固定源码下全套任务成功，但JDK/资源/消费者adapter与云端不同；95个条件跳过保持原策略，本轮44+历史40=84项删除，含安全、事务及12个本机Redis端口fixture失败覆盖缺口；不等同未裁剪的原套件，更不等同业务功能全修复。最终新JAR SHA256 f007b27253bce14eb0dd0e589349282a1714072f87cfc716dde1494533b1f612，只有本地产物，未发布安装。精确输入、全日志、JUnit摘要、制品proof和任务执行readback见testfix/local-full-confirmation-*。
按照项目自检后集成规则，核对API主checkout完全干净、仍develop@58b4b5f后已仅本地fast-forward到上述受测commit/tree，回读干净一致。未push；00:00只读远端develop仍58b4b5f。保留隔离分支和证据；根gitlink此前已有变化，不夹带提交。没有新Flow、配置更改、生产数据操作或部署重启。原五分钟Flow/端到端目标仍未证实；后续按需只做固定此候选的Flow计时确认，不把本地PASS写成云端或线上成功。

## 用户授权Flow确认（2026-10-17 00:24+08）
用户明确“跑flow”。沿用Owner/backend-flow-5m-main，固定本地已验收c1e97923bf2325e3ada33b7e2816f203630f020d/treef192948af6ff27b4e78f6f1585aca9bd8a6b4968；只push隔离codex/flow-testfix-trim-20261016，不push develop。核对无活动Run及原配置SHA后临时应用同范围无部署候选，单次启动5260799/Run147，job536649068当前RUNNING；API尚未返回commit，待脚本断言/诊断确认。私有证据/var/tmp/cyf-backend-flow-5m-20261016/r8；结束需恢复原配置。未新增删除测试，不部署。

Run147终态SUCCESS：2026-10-17 00:24:15创建→00:28:33作业结束，总258秒（4分18），Gradle209.346秒。云端压缩诊断重算SHA匹配，实际commit c1e97923bf2325e3ada33b7e2816f203630f020d/run147匹配；2383项=2288pass/0fail/95skip，编译错误0，validateLayering/fresh bootJar及同Run制品上传成功。云端日志JAR SHA256 44fe96bb04fba089eaafbb3e7da8186858d43733dc82229b185ca89934debafd；此处为认证日志声明，未独立下载制品重算。完整私有日志r8/run147-log-current.json，公开摘要testfix/flow147-*。
无活动Run且当前配置仍属本候选核对后，已单次恢复原配置并readback，SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a一致。仅证明裁剪后当前候选这一次CI在五分钟内成功；不证明未裁剪原套件等价、持续SLO或包含部署的端到端五分钟。历史84方法删除/95条件跳过及安全事务覆盖缺口仍在，本轮新增删除0，无生产部署。临时JDK优化配置随恢复撤回，不声称默认后续Run已永久提速。develop仅本地集成，远端未push。用户本次跑Flow请求完成，原完整部署五分钟目标仍未验证。
