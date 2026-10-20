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

## 项目交付规范切回双端Flow（2026-10-17）
用户明确要求后端与前端一样使用云效构建和部署。Owner/backend-flow-5m-main；根仓develop基线518c06a4，API受测基线c1e97923bf。仅修改根AGENTS、交付策略、SDD流程与编排工具索引：正式测试/构建/制品/版本部署统一前端4403172、后端5260799；本地仅开发和诊断，旧本地发布说明标为历史。develop不自动部署、版本/固定源码/同Run制品/恢复/在线核验不变。AGENTS既有路径迁移未提交修改原样保留，不夹带提交；其余脏文件不动。验收为定向规范一致性断言及diff检查，无需应用构建；不改Flow配置、不触发运行或部署，不改共享技能。Run147成功仅证明该候选CI，不宣称优化已持久化或五分钟部署。

## 2026-10-20 五分钟目标续办（Owner backend-flow-5m-main）
用户要求解释当前十分钟并优化到五分钟；范围含整条发布链路计时，但本轮只授权无部署验证，不启动/停止生产或修改其他Owner任务。API本地/14:02只读远端develop均9ca2776c27ce3270efa0ea4c366b7de0e68e8dbb/tree847927f2fc9d76ca09cee79dc7aa987a627450c5，API干净；根HEAD aae93c074960580942112707e9518d831a0ff0af且大量无关脏修改原样保留。接口规范api/docs/interface-standard.md冻结2026-10-14，本轮无业务/接口改动。
实时5260799 Run195 SUCCESS：create→terminal547秒，build375秒，deploy171秒；Run194 CI358秒，Run193完整564秒，Run192完整571秒。Run195 Gradle264.071秒、284任务（183执行/101编译缓存）、2728测试执行/0失败/122跳过；缓存归档约913MB。完整制品SHA4c08a1c70d5de09be6e676ed8ae40df84aba104489e39b5de85628f231cc258b已对主机现有incoming只读重算匹配；提取原XML计时，最慢真实MySQL套件31.910秒；大部分时间是多个串行测试JVM及Gradle/worker开销，不把其全部归因编译。VM日志明确平台省略3488行，不能声称完整部署明细；已有日志停止旧进程33秒，生产当前还可能被其他任务更新，不操作其进程。
优化首候选：仅显式CYF_FLOW_SHORT_LIVED_TEST_JVM=1时对Test进程加入TieredStopAtLevel=1；不改生产JVM/JavaCompile/测试选择器/并发/失败策略。保持Run195全部selector及顺序，保留真实MySQL、ACL/事务、layering、制品完整性及fresh bootJar。13项工具隔离回归通过；这是工具自检不是云端验收。为真实任务续办经原orchestrator claim/transition，工具快照重新绑定本任务，不冒用CHAT-STOP任务授权。
配置/原值/候选均在私有/var/tmp/cyf-backend-flow-5m-20261020（0700）；本轮候选triggerEvents=[]、无部署阶段。最早验证为同9ca2776c固定源码Flow全原范围A/B；结束前必须无活动Run/配置一致核对、恢复原值readback，不把CI五分钟等同完整发布五分钟。不因性能删除测试，不沿用历史84方法删除授权扩大覆盖缺口。正式精简证据docs/implementation/evidence/backend-flow-5m-20261020，原始日志私有目录保留。

14:13 Run196 SUCCESS，create→terminal365秒（6分05秒），job364秒；Gradle242.079秒，284任务181执行/103编译缓存，2728执行/0失败/122跳过不变。C1降低Gradle约22秒（8.3%），但worker准备/缓存/上传合计约123秒，整条CI仅缩10秒；**未达5分钟，不称优化完成**。新增task计时显示真实MySQL所在mmdU3Finalization34.705秒、chat:test15.970秒、bootJar11.237秒，各agent/chat独立项目的测试串行是下一优化点。
第二候选只增加同一Gradle进程内--parallel --max-workers=3（实测worker LARGE_3C6G），不并行启动Gradle、不绕原锁，不改每task单fork或全选择器。定向源码核对MySQL是独占临时datadir/socket/随机端口及逐用例唯一schema，Voice自有Redis独占随机端口；存在旧common RedisServerLoader固定端口且stop注释的历史风险，不扩大每task fork。第二轮必须实际同集合通过再接受并行；任何端口/事务失败须归因，不盲重试。云端配置当前仍本任务无部署实验，下一轮结束恢复原值。

14:20 第二候选Run197 SUCCESS，create→terminal283秒（4分43），CI job282秒、Gradle160.853秒（较Run195减少103.218秒）。完整2728执行/0失败/0错误/122跳过，302suite逐项name/执行计数与Run195相同，181任务执行/103 compile-cache。仅同一Gradle进程跨项目并行，没有增加单task fork，不跑并行Gradle。独立下载本Run归档229027201bytes，SHA5129d497791befb3a87e72846eb8bce1740f06cababa1f7d0a385a02f75e1f01；receipt真实197/commit9ca2776c/tree847927f2/clean及fresh JAR绑定已核验，JAR SHAa71821be与Run195相同。没有部署/重启生产，没有永久修改触发规则。
14:22:48+08 经原控制工具无活动Run、配置仍为自有r2候选核对后恢复原值并readback，原SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a完全一致。优化目前在候选实测与可复用helper，**没有永久切换默认模板**；后续Owner须显式纳入固定版本候选，不能误称默认已提速。13项工具自检通过。完整版本发布<=300秒仍未达成/未验证，不能用CI283秒加历史估值充当完整上线实测。后续动作：对授权版本按真实安装/实际ready时标继续优化，并收口默认模板；不复用本任务旧快照冒充新候选授权，不在未授权情况下重启来做压测。稳定知识已回写既有Flow策略，精简证据保留backend-flow-5m-20261020，原始配置/日志/归档私有目录不入库。

## 2026-10-20 默认配置固化（用户“好，落实下去”）
Owner仍backend-flow-5m-main；根基线df5af3cb，API本地与14:31远端develop仍9ca2776c/tree847927f2，API干净。范围：将Run197相同测试/并行/C1/compile-only策略固化为原5260799默认；保留原push和三条分支过滤、无部署，不发布新版本、不重启生产。根及host工具的其他Owner脏修改不动。接口冻结2026-10-14无变化。
现有默认是老selectors/裸Gradle；Run197又绑定旧人类任务快照，不能直接永久替换。因此仅在既有orchestrator的gradle入口补固定Flow CI上下文：只接受5260799/原三条分支/真实完整Flow commit与run、固定策略SHA和精确argv，重用干净源码核验及同一Gradle锁；无task ledger读写，不伪造Owner，不复用整轮证据，不授予部署权限。每Run动态绑定实际checkout commit/tree，测试/分层/fresh bootJar仍执行；单task fork保持原样。策略与Run197的argv机械对比一致，仅诊断init移至源码外工具目录以保持fresh build目录。
源码分拆为既有默认模板、backend-ci-run.sh、backend-ci-policy.json，prepare-backend-ci.py仅离线渲染固定工具bundle，不另建云端runner；工具bundle逐字节绑定当前orchestrator/策略/JDK/compile init，不含旧task snapshot、旧commit/tree或旧fixture。原云端source/trigger配置已保存并逐字节对比保留。隔离自检：Flow guard9、模板4、JDK13、旧orchestrator19、dependency cache13、local defaults12共70项通过；均非应用正式验收。下一动作单次update/readback后以固定API源码跑一次无部署Flow；成功保持新默认，不再恢复旧慢配置。私有证据default子目录，正式结果后续补充；完整部署五分钟仍待真实版本验收。
14:37默认候选单次update/readback成功（canonical29b84508），Run198 FAIL/79秒：worker为Python3.6，新增subprocess.check_output(text=True)不支持，发生在任何Gradle启动前；无测试运行、无制品和部署。已按原fail入口归因一次，改为universal_newlines=True并补模板回归断言；不是同输入盲重试。14:40核对无活动Run/配置归属后更新修正候选canonical cc7d7b7d429092a78193fa3a08a5846ff72fffb4bba474399c42c04a4359641b，readback成功，Run199单次启动，固定API源码仍9ca2776c。结果待正式核对，尚不称默认正式验收成功。

14:45:45 Run199 SUCCESS：14:41:01创建→终态284秒（4分44），job283秒，Gradle161.942秒。相同API9ca2776c/tree847927f2、2728项/0失败/0错误/122跳过；独立下载制品并直接解析302份XML，逐suite执行计数与Run195一致。32个指定Gradle任务全部实际执行（含layering/fresh bootJar），无整轮EVIDENCE_HIT，未改单task fork、未删测试。归档229027426bytes/SHA d194f08eb94bf9d859d7fde0586c2ff7a2040f1886b19601c39ec474316dee75，receipt Run199/完整源码/clean以及JAR SHA a71821bea7caed3ae1d37d9dadb5accde4e4f6cebc7081b0c96a32e64851c6c3均独立核验。14:46:38无活动Run且当前配置仍等于最终candidate，保持新默认（canonical cc7d7b7d...），不恢复旧慢配置；原push和三分支过滤逐字节保留，无部署阶段。14:46远端develop仍9ca2776c，原API checkout未改。
默认固化子项已完成，77项工具隔离自检通过；源码根提交5d79d99a及Python3.6修复34cf32ac，仅本地提交，Flow直接绑定该工具字节。公共证据default-candidate-proof/default-run199-summary/default-retained-config.json，原始配置、日志和归档继续私有保留。完整生产版本发布五分钟目标仍未完成：未指定新发布版本，本轮未改生产helper/未发布/未重启，不操作其他Owner host工具改动；后续由发布Owner在授权版本候选中纳入此profile，以真实同Run安装/ready/业务核验继续归因和验收，不拿CI284秒替代全链路目标。

## 2026-10-20 继续压缩（用户“继续优化，看一下还有没有压缩空间”）
Owner/backend-flow-5m-main；根基线9ad16e7b，14:50本地及远端API仍9ca2776c/tree847927f2且干净，云端无活动Run/默认仍Run199候选已实时核对。范围：继续无部署CI优化，优先重复平台JDK准备和913MB缓存开销，保留源码/工具/制品绑定、全部测试及锁/完整性/健康；不改生产、host脏文件或其他Owner路径。接口冻结2026-10-14不变。
Run199总284秒中Gradle161.942秒，其余122秒；日志可见缓存restore约16秒、archive/upload约25秒。JavaBuild使用平台jdk21，而真实构建另经固定SHA Dragonwell21 helper每次校验和fresh解包；该重复准备是候选缩时点，实际收益待测。历史schema证据明确Command不是有效组件，不复用早期失败方案；仍用JavaBuild，平台bootstrap改jdk1.8，Gradle实际运行前始终强制固定校验的Dragonwell21 JAVA_HOME/PATH，无Java降级。新增仅数值、固定标签的缓存体积观测，结果嵌入既有test-results/summary.json，不新增installer不接受的归档成员；不输出凭证或文件内容，不清缓存。
最早验证为固定同API源码一次5260799无部署完整Run；Gradle argv/selector/compile init均不改。工具26项隔离回归、内嵌Python语法和shell/diff检查通过，非应用正式验收。私有配置/备份/日志/further；后续若实测无收益不夸报提速，缓存瘦身须先取得体积分布和实际再生成代价，不能盲删依赖/编译缓存。

15:08本轮收口：工具源码39ba13ee（根仓本地提交，未push）已离线渲染并直接绑定云端工具字节。14:54:29单次update/readback到canonical `9671c967564668b0e94bdc956db2248175c78a8f65a803187e55f4d5567ae3e2`；未增加流水线。Run200 SUCCESS，14:54:34创建→14:58:10终态216秒（3分36），job215秒、Gradle114.116秒；同配置只读核对后单次复测Run201，15:02:02→15:05:50终态228秒（3分48），job227秒、Gradle123.419秒。两Run均固定API9ca2776c/tree847927f2；启动前两次远端develop核对匹配，未修改API源码。相较Run199默认284秒少56—68秒（约20%—24%），其中Gradle本身变化38.523—47.826秒，不能将全部收益归因于平台JDK准备；两次样本不是冷缓存或持续SLO保证。

两Run的同Run制品均独立下载、重算归档/JAR SHA并直接解析302份XML：2728项/0失败/0错误/122跳过逐suite与Run195一致；全部32个指定任务fresh，包含validateLayering/bootJar，无EVIDENCE_HIT，181执行/103编译缓存。实际构建仍固定校验Dragonwell21，不是Java8构建；JAR SHA仍 `a71821bea7caed3ae1d37d9dadb5accde4e4f6cebc7081b0c96a32e64851c6c3`。Run200归档229026189bytes/SHA `55430f9aaf094e4dfb2e0ef0c200509fe8f3358b40d92bf61d60472c2b535b9a`；Run201归档229026996bytes/SHA `5f3e9c0f063d5e4fc9aa1c1ffeaf19901fae6e4ffa4187ec4fcc7bf9a2c138c8`。

缓存库存两次稳定：Maven447197184bytes，Gradle约1032MB（modules-2约495MB、compile cache145MB），JDK归档约218MB、MySQL归档约48MB；目录占用不等于913MB压缩归档的贡献。JavaBuild全局缓存范围仍是下一候选，但本轮没有验证完整消费者与剔除后的再生成成本，不删除.m2、不盲删Gradle版本/变换缓存，不做无实测秒数承诺。库存漏列实际Gradle9.3.1，8.14.3=0不能当作当前版本缓存为0；后续若继续瘦身先补定向证据。工具26项隔离自检已过，收尾模板4项复核通过，均不替代上述Flow正式证据。

15:08:22最终只读readback：无活动Run、当前配置与本候选完全一致，原push/三分支过滤保留、无部署阶段；保留已验证新默认，不恢复旧慢配置。证据`docs/implementation/evidence/backend-flow-5m-20261020/further-*`；私有配置/原始日志/归档保留`/var/tmp/cyf-backend-flow-5m-20261020/further`及`repeat`。稳定知识已回写既有Flow策略。根仓及host等无关脏改动原样保留，未安装helper、未指定/发布新版本、未重启生产。

本次继续压缩与复测子项完成；完整生产版本发布五分钟目标仍未完成，任务不标done。后续由授权版本Owner在固定发布候选纳入此profile，使用同Run制品和实际安装/ready/业务核验，继续拆解历史171秒部署开销。定位/实现/验证有上述时间戳，独立耗时边界未完整采集，未知留空；不把CI节省等同整体开发周期或上线节省。

## 2026-10-20 缓存范围继续压缩（用户“继续优化”）
Owner/backend-flow-5m-main；根基线67889078，15:12 API本地/只读远端develop仍9ca2776c/tree847927f2且干净；当前云端默认9671c967、无活动Run已核对。范围仅后端无部署CI，接口规范api/docs/interface-standard.md冻结2026-10-14不变；不动其他Owner脏路径/生产helper/服务。本轮复用现有Flow和工具，不新增runner。
只读源码定向检索所有Gradle构建文件未发现mavenLocal/.m2消费者；实际cold-init显式使用Gradle仓库和源构建plugin。官方Flow YAML文档缓存配置支持cache.cacheDirs与cacheMode:remote，因此优先仅缩小远端缓存打包范围，不删除worker任何目录：保留/root/.gradle/caches及固定校验JDK/MySQL归档，移出.m2/.npm/.yarn/go和其余泛.cache。平台Maven初始化是否会重新生成仍须实测，不把447MB目录占用当压缩收益。修正库存版本标签为实际Gradle9.3.1，其余Gradle argv/测试/fork/JDK来源/SHA均不变。
最早正式验证：固定同API源码一次迁移Run，之后同配置再跑一次确认精简缓存恢复的真实耗时与测试/制品等价。旧全量缓存可能在首Run恢复，需区分迁移Run与后续热Run；不声称冷缓存保证。原配置/固定候选位于/var/tmp/cyf-backend-flow-5m-20261020/slim；失败先归因，未知写/启动只读对账，不盲重试。成功保留有证据候选，若无收益按实际结果决定，不为指标删测试或完整性校验。

首候选29191f5b已单次update/readback（canonical267acd98）并启动Run202。运行日志实证cacheDirs会**追加**JavaBuild默认路径而非覆盖，ARCHIVE_PATH仍含.m2及泛.cache且重复纳入JDK/MySQL子目录；因此该候选不接受为瘦身结果，也不按同输入重复跑。配置语法支持不代表达到覆盖默认范围的语义，前述候选假设被本次实测否定。
调整方案仅在本任务独占、一次性的Flow worker里将.m2/repository原子rename到既有私有/tmp/cyf-backend-flow-ci.*/maven-platform-repository；不删除、不改.m2/settings.xml及凭证，不动Gradle或固定运行时归档，跨设备/链接/不归本身份/目标已存在均不移动。移动放在测试之前，正式同selectors成功才证明本固定范围不依赖该仓库；结束数值库存同时保留私有stash大小和.m2剩余大小，summary记录移动状态，不输出文件内容。移除追加cacheDirs配置，避免重复归档；保留默认缓存机制。6项真实嵌入脚本隔离测试验证内容/凭证保留、双层链接、缺失目录、目的冲突及错误流水线上下文，另原27项工具测试通过。所有应用正式验证仍在Flow。Run202活动期间不改云端配置、不取消任务；终态后才核对归属并单次写入新固定候选，之后一个迁移Run和一个精简缓存恢复Run完成验收。

Run202终态SUCCESS/280秒，Gradle163.062秒，日志2728项/0失败/122跳过，缓存913466214→913469571bytes，确实未瘦身；没有独立下载其制品，不作该制品验收声明。无活动/归属核对后已替换为2cda8372候选（canonicalfae4f166），单次启动Run203。Run203初期真实日志为CROSS_DEVICE_NOT_MOVED：worker的.m2与/tmp不同文件系统，安全分支未移动任何文件，不是应用构建失败；不把“脚本成功”说成缓存已削减。
下一固定候选仅将stash放到HOME下新建0700私有兄弟目录（.cyf-backend-flow-ci.*），仍处于全局缓存路径之外，先核对repo与HOME同设备再原子rename；依然不复制或删除任何文件、不触碰settings.xml、不跟随链接/覆盖目的目录。原Flow实验目录仍存状态文件；数值库存按固定标签指向新stash。工具6项实际脚本测试和模板5项复核通过。活动Run203结束前不改云端配置；HOME是否同设备及精简缓存收益仍以之后真实Run为准，若仍不能安全移动则保留原缓存并收口，不继续同根因盲试。

Run204初期私有日志已另存run204-live.log，确认HOME仍与.m2/repository跨设备，安全分支再次不移动。终态SUCCESS/279秒、Gradle165.353秒，2728项/0失败/122跳过；缓存未精简。到此停止rename方案，不做第三次目的路径猜测或跨盘复制/删除。未独立下载此无收益候选制品。
改为GNU tar原生归档排除：仅流水线变量TAR_OPTIONS=--exclude=.m2/repository，覆盖缓存打包/恢复但不修改任何缓存源文件、不排除settings.xml/Gradle/JDK/MySQL或允许的发布成员。6项真实tar隔离测试覆盖绝对/相对/root相对路径、旧完整缓存恢复、源文件及凭证字节不变、允许发布成员全保留。移除此前无收益的移动helper和专属工具测试，恢复原Run201运行逻辑（仅库存标签修正9.3.1），不留死代码。下一验证先确认配置变量实际生效，再以同源码完整Flow核对真实归档缩减；若环境未传给缓存步骤则不声称成功，不继续无依据重试。旧默认9671c967仍有备份可恢复；本轮无任何生产动作。

归档排除首个变量映射形式候选ac1d0a55被API明确拒绝（FLOW_API_REJECTED），未启动新Run；不把配置保存请求当成功。原值仍以只读核对为准。下一固定候选改为variables的key/value序列形式并补模板断言；需实际update/readback及settings.globalParams只读确认TAR_OPTIONS绑定，之后才启动。若再次拒绝或未生效则停止同根因猜测、恢复已验收Run201默认，不继续耗费正式运行。
