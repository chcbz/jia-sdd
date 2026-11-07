# 本地前后端构建计时（2026-11-06）

- Task: LOCAL-BUILD-TIMING-20261106；Owner: local-build-timing-owner（developer）。用户要求两端重新运行并提供实测明细与优化建议。
- 范围：固定远端 develop（本次 fetch 已成功）的完整源码，复用既有 release 测试、生产构建、分层/依赖完整性与 fresh JAR，记录准备/等待/执行/打包和墙钟。非目标：无生产安装/重启/DDL/Provider请求，不触发 Flow，不把构建计时当完整发布。
- 主源码均有其他任务未提交修改，现有隔离树归其他 Owner；仅为并发写入隔离各创建一个源码树，后续不按阶段重建。
- API: f24f4c1aef16c4eb48b95329b828cc83ec2f1558 / tree 1f4be2cb808ebcfa6077e1e25383b531233e1200；`/root/.codex/worktrees/cyf-local-timing-api/api`。
- Web: c1e478f633845a448833a3973e732a12a75874aa / tree ea03d165f0dfc9fe065c06e4837f84e558b360ff；`/root/.codex/worktrees/cyf-local-timing-web/web`。
- 已读根AGENTS、组件规则及ops/orchestration/README，11-06本地规则覆盖共享技能旧Flow-only。接口规范`api/docs/interface-standard.md`现行v1.4；无产品/契约修改，责任为既有本地构建控制面，RB-1不新增业务规则。
- 证据：`docs/implementation/evidence/local-build-timing-20261106/`，固定输入request/api-inputs、runner/init/policy真实文件与摘要、阶段日志、result.json和包外测试。
- 执行：systemd transient unit `cyf-local-build-timing-20261106`，先Web再API；Web与Gradle共用既有`/tmp/cyf-gradle.lock`排队，不抢占、不并发重型构建。API仍调用原orchestrator并绑定真实任务/源码/fixture，不设600秒强杀。
- Web执行npm ci、release profile、Vite build和tar；即使测试失败也可诊断构建，失败包明确不可发布。API固定既有默认policy测试selectors，必要测试/validateLayering/bootJar保留，外部新输出；独立Gradle home仅从既有本地依赖/compile cache取种，不复制transform cache、测试结果或旧JAR。
- 完整发布600秒：NOT_MEASURED（无安装/健康/业务验收）；构建结果及各阶段实耗待实跑后补充，不预承诺达标。

## 首轮Web结果及API接续（21:47 +08）

- Web执行窗口21:18:22.518—21:31:49.560，墙钟807.042s；构建测量前的调研/源码隔离准备未计量，不当完整发布。既有构建锁排队7.054s；npm ci 49.954s；release测试565.965s；Vite进程157.888s（Vite内部报告148s、1565模块）；tgz打包24.153s；源码核验/哈希/报告收尾约2.028s。
- 测试3862通过、2 pending、1失败；TMX portable preview CLI同步集成实际30.947s超过原20s用例超时。其余断言是否可优化须保留真实CLI/文件/失败原子性覆盖，不通过调大超时或移除用例宣称提速。测试过程内500.959s，进程启动/导入/报告约65.006s；慢文件TMX snapshot 69.877s、组件行为50.857s、draft editor33.096s、HallScene E15 29.892s，见web-test-analysis.json。
- Web包`/var/tmp/cyf-local-build-timing-20261106/package/web.tgz`，SHA256 `91772bfc321bde4dcfcd893a05f9c5a6351bb2efb80f52f5ea1f9370b74b89a6`。测试失败，publishable=false，未安装。
- Web包外报告复制起初使用Python3.6不支持的copytree参数；原报告完整保留，随后复制到web-default-reports，不影响原测试/构建结果。API首次仅CLI argparse前置选项顺序错误，未启动Gradle；续跑包装器碰到Python3.6 fromisoformat缺失，改为已安装Python3.11.13并实际预检语法/CLI parser。另一预检发现metadata init basename必须是固定文件名，保留原错误，改名保持内容SHA不变。controller-preflight.json对原本地cache-defaults、私有缓存、任务guard、干净完整源码均实际PASS，再续跑。未重复Web或任何已成功重型阶段，无伪造身份/绕保护。
- API真正的Gradle进程于21:35:30开始；从21:31:49开始的原API准备/控制面失败和修复间隔保存在result.json priorAttempts和日志，不从总墙钟扣除。source/build/home均复用；source commit/tree不变。
- API冷启动诊断：Gradle插件compileJava 271.143s；约5分钟处仅对本任务Gradle daemon取线程快照，GraalVM JVMCI-native compiler已累计CPU158.033s，占该进程当时约368s CPU的43%；另有Java classpath依赖扫描。约11分钟快照可见HEAD/SSL读取，仍在配置/依赖解析，不能把尚未开始测试当通过。数据见api-thread-analysis.json及两个只读线程快照。构建机当前Java为GraalVM21.0.8，非Flow原Dragonwell；切换构建JDK/复用持久Gradle编译元数据是待对照优化，不宣称已获收益，不改生产JVM。
- 主机既有clear_disk.sh clean的du扫描同时在途；CPU采样和iostat显示明显I/O wait，10s进程IO样本du为最大读取者。只能确认资源干扰存在，不将所有耗时单因归为清理。未暂停/终止其他任务。完整发布仍NOT_MEASURED。

## API在途补充（23:18 +08；不是最终结果）

- 主Gradle图到达前：root projectsEvaluated 792.01177s，taskGraphReady 818.00541s，届时JVM uptime878.013s；嵌套插件compileJava271.14288s已包含在配置内，不重复相加。仍是首次私有cache，未带transform cache，目前无compile FROM-CACHE命中。
- `:agent:jia-agent-service:test` 658.88467s，1369记录、1失败、78 skipped。失败为`SkillExecutionMapperRealTransactionTest.unknownCannotReturnToReadyOrCancelWithoutAnActualReconciliation()`第190行assertFalse实际true，不是20秒类超时，不能按性能问题掩盖。
- `:chat:jia-chat-service:test`已出现ArchiveQuestionWorkerTest两个时序断言失败，保留完整XML后再汇总；不修改或放宽断言、不另起全量重跑。
- fresh `:starter:bootJar`已执行176.81261s并输出SHA256 `cb4ca01078165d85dfeec55956cedd21b458ac49de7df7967d9ea007ca9516ad`；其他测试/分层还在执行，非整批成功，包不可发布。
- Runtime peer入口hash与旧Flow pin相同，但相对import闭包10文件中2个已变化。实际本地Runtime HEAD`c1fc18174b256c90051874485c8c77967efad62a`/tree`9dc7ef80bbdd135cf81386a424d68f4c7ca95a0d`，不是旧pin`c3f973c2e5ca2990dd3e775b42f6bf02f7e0a060`。见`runtime-peer-closure-before.json`和`effective-fixture-binding.json`；测试硬编码runtimeCommit日志不可当真实来源。结束后复核闭包，不把入口hash不完整的证据key留作正式发布复用。
- 默认selectors中存在需显式外部fixture的MySQL/Redis用例，未配置者由现有条件skip；最终逐项列出，不当作通过。当前样本仅固定源码、本地实际工具/fixture的计时与故障诊断，不是完整发布验收。

## 用户终止慢批次并转优化（2026-11-06 23:36:50 +08）

- 用户明确要求超过10分钟停止慢批次，不再等待。已对唯一归本聊天的`cyf-local-build-timing-api-resume3-20261106.service`执行systemctl stop；unit inactive/dead，runner/orchestrator/Gradle进程均已退出，未操作其他Owner进程或生产应用。Observer同时停止。
- API组件墙钟7532.330s（含控制面修复间隔）；实际Gradle未正常结束，退出码未知，不伪造终态成功。已完成XML419 suites/3545执行记录：3407pass、3fail、135skip；另有MMD回归编译失败（billing新增构造参数后fixture未同步），且后续测试/分层未全部完成。此为取消时截面，非完整回归。
- 所有XML与proof保存包外。实际JAR SHA256`18d70608e1777ff71c36f8d2720a2efa91703d6305967ff63b9891c2fd6c164c`，251721701bytes；前文`cb4ca...`为BOOTJAR_END输出的**proof文件摘要**而非JAR摘要，按真实proof和现文件纠正。该包禁止发布。
- 新目标覆盖测试/构建/打包/受控安装/健康及必要冒烟的同批600秒，允许缓存、缩减每次发布的测试范围和并发优化；用户允许删用例不等于把已知失败写成通过，采用发布快速profile与独立回归分开记录。超过600秒停止本任务自有构建并归因优化，不停止他人或把目标做成业务请求deadline。
- 已查Flow实际与本地差异：Dragonwell固定21.0.11 vs GraalVM21.0.8；Flow parallel/workers3 vs本地workers2非parallel；Flow Test-only C1本地未带；isolatedcache零编译命中；本机I/O干扰。需对齐后实测，不能把所有问题单因归于主机。
- 当前生产API固定7bb82c5（Run591）、Web f1234a0/1.16.121（Run469）。develop含并行计费，不能未经核对直接将其作为性能优化顺带上线；生产适配器本地来源目前仍退役拒绝，必须明确适配且不恢复旧准入、不伪造Flow。

## 优化第一轮（2026-11-06 23:55 +08）

- 新增已有编排器的窄本地构建前端`ops/orchestration/local_build.py`及`local-build.init.gradle`，不改Flow、不恢复退役准入。绑定完整源码/98个构建文件/JDK/工具/selector摘要，显式参数位于原task remainder之前，失败即停；默认只执行发布安全/启动/打包基线及调用方显式回归，不伪称全套通过。控制器6项隔离测试通过。
- 原固定Flow JDK helper首次在本机bundled Python缺CA失败；明确使用系统CA后成功，未关TLS。官方归档SHA `12c642f8d6c6e0930b9b4e673d47822227ea46e7559c7b7b6b4c0331ace0580f`，实际准备204.976s（下载179.020s），工具链已在独立缓存目录解包，未修改生产JVM。该准备时间单列，不能隐藏后宣称冷启动完整发布达标。
- `cyf-local-fast-api-20261106-01` 23:44:29启动，固定原f24f4c1，Dragonwell/Test-only C1、私有持久依赖/compile缓存、必要安全/启动/边界/分层/fresh JAR基线。systemd RuntimeMaxSec=600，到点自动停止本单元全部自有进程；实际已核对MainPID0、Result=timeout，未等超10分钟继续构建。只到主服务Java编译，未取得测试/分层/JAR完整成功，**未达标、未部署**。真实单元时间和状态见`local-release-fast-20261106/api-01-result.json`。
- 下一项有证据的优化：已增加显式`--offline`选项，允许已完整解析缓存的固定输入避免metadata HEAD等待；缺依赖直接真实失败，不联网回退/不绕摘要。当前尚未实跑该选项。编译缓存由切换构建JDK后重新填充，不能把首跑/热缓存混为同一批墙钟。
- 后续仍须完成Web快速关键路径、真实LOCAL制品安装适配、同批两端安装及健康/必要业务冒烟，完整发布600秒尚未验证。源`f24f4c1`存在本次已知失败，不因快速基线未来通过自动授权安装其并行计费变更。

## 后端快速路径实测（2026-11-07 06:22 +08）

- 02与03均由600秒cgroup截止停止，MainPID=0，未等慢批次继续。02卡在全Agent compileTestJava；03改源级切片后安全测试编译39.044s/执行38.998s，23项通过，但后续production compile cache尚未齐及打包仍超时。原所有测试入口未删改。
- 04采用短生命周期Gradle JVM C1及内部parallel/workers2，图就绪约14.8s（03约131s），73+ compile cache命中；合计71.655s，但starter健康配置断言expected false实际null失败。原断言保留，定位新slice runtimeClasspath先依赖后main output，依赖同名application-prod.properties遮蔽应用资源，已按标准test顺序修正。不是应用生产配置缺值；没有把错误归为性能波动或放宽断言。05在fail归因切换gate后被原orchestrator拒绝，0.382s、Gradle未启动；恢复本Owner targeted_verification后06实际验证。
- 06固定同源f24，热缓存，**79.695s BUILT**；105项测试全过，无fail/error/skip；validateLayering及fresh bootJar/原PublicArtifactVerifier/POI全部通过，73次compile FROM-CACHE。JAR SHA54db8b51a78af7da0eee5ed87c7f22581724331edbb3ad3eca536ef33f73d759。这是性能快速基线，不消除f24全量诊断的已知失败，不授予并行计费上线；publishable=false，无安装/重启。收益同时包含缓存进一步完整、源级切片、构建JVM C1/内部并行，不能单因归因。
- 本任务自有已停批次中间class/tmp/report在保存JUnit/日志后删除；原诊断最终JAR、04/06最终JAR、Web最终包及追溯保留。仅删除已校验官方SHA的208MiB自有JDK下载归档，保留解包工具链及摘要，不删除他人缓存。逐路径见intermediate-cleanup-20261107.json。
- Web恢复原管理worktree，归档snapshot feebb82已保存引用/生成声明原件，切回原c1e478f，仅稀疏省略未选tests/fixtures且保留interface-standard；生产src/public完整。前端快速关键路径独立实跑，600秒硬上限，共用原构建锁，不与API重型构建叠加。保持同一Vite配置，仅不重复copy public到dist；打包逐文件原样加入public及dist，gzip level1并流式回收已归档的自有dist文件，再全包逐文件摘要复核。明确缩小测试范围，不声称原3865项全过。结果待补。
- 完整两端同批构建+安装+健康/业务冒烟≤600秒仍**未验证**；安装适配仍未完成，目标保持active。

## 前端快速路径实测（2026-11-07 06:27 +08）

- Web01测试47pass/2pending，Vite21.85s，但压缩期间磁盘写满、unit exit1，RUNNING结果无法flush；包未完成/未核验，绝不发布。现场确认MainPID0后删除本任务未完成88MiB流，保留测试/构建日志及manifest。API只读health HTTP200；未操作应用进程。第一次容量估计按旧242MiB node_modules，实际npm ci安装333MiB，且原排序先大public资产、后生成JS，未及早释放dist，是本次工具自身容量估算与排序问题，不能隐去。
- 修正：先归档并释放自有dist生成文件，再归档只读public；每次压缩写入检查32MiB剩余空间，低于保留线主动失败。清除自有失效中间dist、无活动使用的私有project-cache（不是modules/compile缓存），及自有解包JDK中不参与运行/编译的可重建lib/src.zip（52MiB，保留摘要）；JDK运行库、javac/java和原生产JVM未修改。稀疏worktree生产src/public完整，未选大型测试fixture不拷贝。
- **Web02 BUILT 57.225s**：npm ci16.165s、选定测试4.171s、Vite命令23.409s（内部20.98s）、打包10.923s、全包逐文件摘要核验1.592s。Mocha49项，47pass、2pending、0fail；包含interface-wire对子套件的实际Node进程执行。不是原3865项全套通过；2pending保持原状态。全新包103MiB，SHA20216940fdd891c0fe222ff8dd4d4dcf7523b0808901f07f5fd8c6716f4d4fbc；真实LOCAL manifest含完整源码tree、全部文件摘要，无Flow身份。结果publishable=false，未安装。
- 包外已保存所有测试报告、manifest、生成声明patch及阶段日志。Web自有worktree已申请归档，释放本批node_modules/source，最终包仍按保留规则保存。npm内容完整性缓存未清。
- 两端分别构建成功（API79.695s、Web57.225s）不等于同批发布≤600s；尚无本次安装/重启或新版本业务验收。当前干净源码包含未授权并行计费及已知全量失败，不把快速profile当作其上线批准。真实LOCAL安装适配/稳定候选的同批整链验证继续待办，goal未完成。

## 稳定候选正式包与真实安装契约核验（2026-11-07 06:54 +08）

- 接续时复核：07已终态BUILT，固定生产同源`7bb82c526e4ba4345ca8e88711067ed23dfcdbbc`/tree`7e6d03056902c4a36abd9ca0959d5a398e65224b`，测试/构建/打包169.544s（含打包35.288s），包224292217bytes，SHA`e667c5f309d2ea8e769390046d8d364a463248bb92e05cc694b23a5afcb675ca`。原结果、完整输入、日志和receipt复制包外`local-release-fast-20261106/api-07-*`。包仍在`/dev/shm/cyf-local-fast-api-20261107-07/package/api.tgz`，临时内存盘，不宣称已持久归档或安装。
- 实际调用source coordinator原生`native_approval/native_package/native_validate_payloads`（不调用main/安装/写生产approval），发现首次真实包因不存在`BOOT-INF/lib/opencv-4.5.5.jar`被拒。源码`common/jia-common-core/build.gradle`明确该依赖compileOnly、测试testImplementation，生产JAR无该成员是正常的；24项合成测试始终内嵌OpenCV，遗漏此正常场景。
- 修正仅在本地安装适配器：允许compileOnly OpenCV不随生产包出现；保留provenance固定coordinate/SHA/size校验；若随包出现则必须唯一、坐标与实际字节匹配原pin。未改依赖、摘要、业务源码或生产JVM。新增缺省compileOnly成功、内嵌篡改拒绝、错误版本拒绝三项回归。
- `test_native_local_api.py`实际27项通过/21.115s，包含原安装事务、锁、幂等、恢复/回退。相同真实07包经修正后的原安装payload validator通过，11.598s；无Flow身份、无生产写操作。报告`api-07-package-validation.json`和`native-local-api-tests-verified.log`。
- 生产固定helper尚未更新，线上未安装/重启；Web稳定源码正式本地安装契约和同批两端整链仍待完成。上述构建和只读校验发生在不同执行窗口，不相加冒充同批发布。目标仍未达成，不标complete。后续需先核对helper维护catalog/备份安装更新路径和生产当前状态，再执行获授权的稳定候选同批完整发布计时。

## 后端真实发布完成、前端稳定包接续（2026-11-07 07:13 +08）

- 本轮是进展：实际更新生产安装helper、真实安装/重启稳定API，并取得来源/备份/健康证据；不是仅重复状态。Goal仍active，不能宣称两端同批整链完成。
- 安装helper从已安装字节构造窄候选，保留E05 runner SHA和历史offlineMaintenance等无关线上差异，未整份覆盖源码helper。实际锁顺序auto-approval-v2→release-api，先备份精确字节，再原子替换/readback；报告`api-native-helper-installation*.json`、可重演脚本及原件在`api-native-helpers/`。当前候选保留`/var/lib/cyf-api-flow`旧状态绑定（与`/home/isp/state/cyf-api-flow`是同inode的bind mount，不是普通symlink），避免顺带迁移历史记录。首次把helper根改实体路径，导致旧record.backup父路径检查失败；在生命周期操作前拒绝。原失败保留，不改历史记录/回执。V2恢复现网绑定后通过。40项**当前有效**旧Flow门禁+native LOCAL隔离回归全部通过；包含已退役schema-3测试的首次广泛加载另有缺失历史fixture导入错误，日志保留，不声称全47项通过。
- API08固定生产同源7bb82c5/tree7e6d0305，真实新测试/分层/fresh bootJar/打包106.895s（Gradle69.244s、打包36.173s）；第一次安装预检1.961s失败；路径修复及等待115.886s；同包重试安装118.512s成功；生命周期status3.603s。后置smoke脚本误把Boot4实际`status:{code:UP,...}`写成字符串断言，真实健康无故障；修正读取实际完整fixture后仅补smoke，未重启/重编。该修复/等待77.727s、smoke2.227s都计入原批开始时间。
- **API完整批次06:59:19.467→07:06:30.208 +08，墙钟430.741s，RELEASED且under600=true**。此结论包含失败、修复和间隔，未把其剔除。JAR `21906ddb6dff0d17f28ee9f8254616da11e0cfd47ecc60ce72677a24484e9c0d`，LOCAL buildId`local-stable-20261107-08`。安装record schema4、source_kind LOCAL，前代备份摘要等于旧生产JAR`75e7886f...`；旧PID1750937退出，新PID2158354，身份/端口/JAR attestation匹配。health200且实际status.code UP；JWKS200且非空；真实受保护scene snapshot无凭据401。此是启动/安全边界smoke，不伪称有已登录用户业务写入。详见`api-08-release.json`、`api-08-install-record.json`、install/status日志；早期错误结果另存first-failure/smoke-parser-failure。
- 注意临时rough edge：本轮为收集原installer阶段时间传入`CYF_API_STARTUP_DIAGNOSTICS=1`，现有lifecycle还会向JVM加启动DEBUG/TRACE参数；当前新JVM带此诊断。**下一次正式同批重跑应移除此env，回归正常JVM参数并实际验证**，不要再次照抄08脚本中的诊断env；无需改生产Java版本或业务源码。单独的08成功不作整个goal完成证据。
- Web恢复另一个必要的干净生产同源worktree到`/dev/shm/cyf-local-stable-web`，固定f1234a0/tree0f6402f2、1.16.121，原主Web树有他人脏改动，未覆盖。完整src/public/static和根配置保留，省略原型及未选tests；interface-wire实际mjs/fixture和tests/helpers必须保留。03最初缺miniProgramRuntime helper导致导入失败，原报告保存后仅清无包的03自有临时输出；补足稀疏helper闭包后04实跑成功。没有降低断言或伪造测试。
- **Web04稳定包52.605s BUILT**，47pass/2pending/0fail，真实v2 LOCAL manifest含buildId、完整commit/tree、版本、全部612文件SHA/size和测试report/selector/counts，无Flow字段。包`/dev/shm/cyf-local-fast-web-20261107-04/package/web.tgz` SHA`1fd22f9f5f1119f03eb2f5c1ff39c09f7c58a356878f8c3de0aa5e780645cd42`。source helper的共享文件manifest校验已提取复用，stream scanner显式local开关读取root包，不发明Flow身份；新增v2 LOCAL manifest校验。12项新增隔离校验+3项既有online cache回归通过；真实04包经同一scanner/validator通过（1.703s），详`web-04-package-validation.json`。**Web本地安装事务/来源入口尚未接入，线上Web helper及站点未变**；不得把validator当安装完成。接下来在原web helper加入显式LOCAL入口，继续使用原发布锁、assets-first/index-last、摘要核验和可恢复备份，测试后受控更新helper，再做两端同批完整计时。
- 容量：API08保留真实前代备份后根盘约250MiB，下一批同盘candidate+rollback需约503MiB，不能跳过容量准入。已确认无任务JDK进程在用，将**本任务**已验证Dragonwell构建工具链逐文件SHA/mode/symlink校验后完整移到`/dev/shm/cyf-local-toolchain/dragonwell-21.0.11.0.11+10-GA`（4.844s，根盘释放342642688bytes），未删最终包/他人缓存/生产备份，也未改生产Temurin。报告`build-jdk-memory-cache-move.json`。**旧--jdk路径已不存在，后续用新物理路径，并如实绑定新工具链路径**。`/dev/shm`实际rw,nosuid,nodev，未noexec，未改mount参数；Java已验证可执行。RAM/磁盘均须继续按实际负载观察，不并发堆叠重型构建。
- 当前本任务最终包07/08、Web04及新JDK、Web源码/node_modules在内存盘；包外日志/receipt/报告已保存在根repo evidence。未冒充持久归档，未对这些仍活跃/被安装绑定的包mark-complete或删除。API/前端耗时不可跨批相加当两端完整同批达标；还要完成Web安装、移除API诊断参数、两端正常参数整链≤600s实测与相应验收，goal保持active。

## 两端同批完整发布达标（2026-11-07 07:32 +08）

- **目标已实测达成**：`cyf-full-local-20261107-01`，07:25:27.173→07:32:42.484 +08，完整墙钟 **435.314秒（7分15.3秒）**。同批固定生产同源API7bb82c526e/tree7e6d0305、Webf1234a0a/tree0f6402f2；新执行测试/构建/打包后实际安装，并完成健康和线上摘要核验。不是拿API08/Web04跨批估计相加。
- 主证据 `docs/implementation/evidence/local-release-fast-20261106/full-01/release.json`，原错误回执 `release-first-failure.json`、真实续跑 `resume-same-batch.py`、所有日志/原控制器字节/新鲜XML/测试报告及包内receipt等元数据均在同目录。修复、等待与失败不从计时扣除，原FAIL保留。

| 阶段 | 秒 |
|---|---:|
| 前置API运行状态 | 1.802 |
| Web测试/构建/打包/完整包校验 | 50.150 |
| API测试/构建/打包 | 113.161 |
| API受控备份/安装/重启/健康 | 74.750 |
| API安装后状态 | 3.596 |
| Web首次安装及失败的线上核验等待 | 120.762 |
| 故障定位/修复/续跑间隔 | 42.376 |
| Web原事务同包恢复及全部线上核验 | 15.115 |
| 最终健康/签名/安全边界/正常JVM核验 | 4.432 |
| 其余输入、哈希、包外证据保存等未分段开销 | 9.170 |
| **完整同批墙钟** | **435.314** |

- Web内部：npm ci9.491s、测试4.271s、Vite23.848s、gzip1打包8.970s、完整包内容校验1.581s，其余为初始化/源码核对/摘要。47pass、2pending、0fail；612文件完整manifest。稳定同源产物与生产内容一致，changedFiles=0；依然执行了原发布锁、前代/包完整性、备份事务及 **全部255个线上index/JS/CSS（含懒加载chunk）精确摘要核验**。合法无内容差异发布，不伪称覆盖了新功能升级。
- API内部Gradle75.905s、正式LOCAL打包34.001s；10份XML共105项、fail/error/skip均0，validateLayering和fresh bootJar通过。制品JAR SHA `b0de1e722b31041e8eac08ea35e7c40ae9e1051f559d4ef67ea43beb4439cfcc`；新PID2168125，生产Temurin参数正常，确认无startup-tracing/DEBUG/TRACE。旧PID2158354已退出。record schema4 LOCAL installed，前代真实备份摘要匹配API08 JAR。health实际status.code UP、JWKS非空、真实scene snapshot无凭据401；未做已登录用户业务写入，不能扩称完整业务验收。
- Web包SHA `704fc894ac5894e759b15e40621a946e049d3ad778451092255aaaa80295add9`，record schema2 LOCAL online_verified，source/buildId、包摘要与同批新包一致。具体安装记录另存api-install-record/web-install-record，不从文档推断当前未来状态。
- 本次真实控制面问题：新组合控制器用Python3.11运行原Web helper；该Python OpenSSL缺可用CA信任链，线上校验重试，**不是站点宕机、应用慢或TLS校验可删除**。只终止本批Web核验子进程，保留installed可恢复事务/锁/备份，使用原helper shebang的`/usr/bin/python3 -I -B`恢复**同一包/同一事务**，没有重构建或重装API。失败120.762s和修复42.376s全部计入435.314s。续跑使用剩余共同预算，未将新进程起点当新批次起点。
- 通用控制器已修正Web helper解释器，并增加安装前同解释器TLS预检；4项新增隔离回归通过。API控制器8项回归、生产固定路径8项只读回归均通过。此窄修正由同批实际恢复路径验证，**未再跑第二轮完整发布**，不承诺下一次固定耗时。原脚本完整字节保存在full-01/local_release-original.py；新脚本不能冒充原工具摘要。
- Web LOCAL事务helper已实际受控更新，保留原线上无关差异、legacy `/var/lib`绑定路径和assets-first/index-last、摘要/锁/备份/同binding中断恢复；40项精确installed-candidate隔离测试通过（`web-exact-native-helper-tests.log`）。Web04原安装14.678s成功是历史先行验证，不计入本次435.314s。
- 已落地优化：对齐Flow原Dragonwell21/C1与有限内部并行；持久依赖/JavaCompile缓存、显式offline避免反复远端解析；源码切片只编译快速基线测试，测试/分层/final JAR仍新执行；Web public流式完整打包、gzip1、避免重复dist，重型构建串行；安装复用原事务。Flow差异和早期慢/失败样本仍保留，不将某一项未经隔离对照的缩时归因成唯一原因。
- **边界**：本次是固定生产同源、热缓存、快速发布基线完整实测，不是冷构建、全量功能回归、任意新提交或所有未来发布必≤600s。已知失败f24/其他Owner改动未上线。慢构建到600s停止本批自有cgroup并优化；生产JVM不得进入该cgroup，安装仍需可恢复，不能强杀生产来凑时间。
- 存储收口：包外证据和receipt已保存；`/dev/shm`中当前/前代绑定的最终包保持，不冒充持久归档，不删除生产备份。现installed清理器仍旧CLI，不支持artifact登记；规则文档也未准许内存盘根。**未谎报mark-complete/自动回收已启用，未扩大维护工具任务或直接删除最终包**；后续按维护Owner完成工具适配后登记。根盘实际约258MiB，下一次安装前须重新处理容量，不能因本次成功忽略备份峰值。

- 完成后已核对两端源码无脏改动，为精确源码建立refs/codex/local-build-timing-20261106/{api-stable,web-stable}，删除本任务两份干净临时worktree（含自有Web node_modules）；未清其他Owner。通用入口下次须使用重新准备的干净源码路径，不照抄已删除工作区路径。已验证JDK/持久Gradle cache仍保留作为复用缓存，当前/回退绑定包与生产备份保持。

## 长期策略入口同步（2026-11-07，用户追问后）

已将已验证优化登记到现有 `docs/aliyun-flow-cicd-strategy.md`“本地快速构建发布长期策略（2026-11-07）”，同步 `docs/DEPLOYMENT.md` 与工具README的当前入口，纠正旧“未适配/未实测”顶栏。登记包含具体缓存/测试/工具链/打包/有限并发/剩余预算/原事务保护，以及内存盘非持久归档、容量不足、清理器未安装、未推送远端和共享技能未同步等边界。仅文档整理及路径/既有证据一致性检查，无新构建、安装、重启或云效运行；不将本地文件修改冒充远端已发布。

## 历史清理与持久化闭环（2026-11-07）

按用户“先清理历史临时文件和备份文件，再完成闭环”执行。精确回收1,591,824,384 allocated bytes：2个过期API备份503,287,808、3个已废弃未发布构建中间JAR755,277,824、2个旧Web载荷及1个孤儿stage333,258,752。保留当前、回退、最新两份Web备份、数据库/Runtime/未知格式及包外证据；不是清空全部历史。

JDK已完整核验迁至`/opt/cyf/toolchains/dragonwell-21.0.11.0.11+10-GA`，缓存原子迁至`/home/isp/state/cyf-local-build/gradle-home`；当前API/回退/Web包字节一致镜像持久保存于`/home/isp/wsps/private-maintenance/cyf-local-archive-20261107-*`。历史安装record原路径不改写，仍绑定的内存盘原件保留。

现有维护工具已安装并回读，支持原生API schema4/Web schema2、完成包登记及组合输出组件子根；4个完成任务已进入原registry。维护隔离回归61+67+41+84=253项。原每30分钟cron实际入口已执行，清理末尾不再递归du长持锁；最终exit3准确表示容量仍低于5GiB、没有可删候选，非未知schema失败。持久化亦占用磁盘，当前仅约1GiB余量，下一批必须复核备份峰值，不能宣称磁盘问题完全消除。

当前策略、部署说明、工具README及保留规则已同步本轮状态。具体安装/清理/登记/验证见`docs/implementation/evidence/local-release-closure-20261107/`；版本化结果以`version-control.json`实际远端回读为准。本轮无新应用构建、部署、重启或Flow，不覆盖原435.314秒成绩，也不将它泛化为未来冷构建保证。
