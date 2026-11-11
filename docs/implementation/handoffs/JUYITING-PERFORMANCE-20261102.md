# 聚义厅性能与API堆配置维护（2026-11-02）

## 范围 / Owner / 固定基线

- Owner：当前性能诊断聊天。用户先授权资源诊断，后于同日回复“好，继续”，按已说明的受控API堆扩容对照推进。
- 目标：核对CPU/内存/磁盘及组件配额；API `Xms128m/Xmx384m` → `Xms256m/Xmx768m`，复用原JAR；定位Runtime阶段耗时和重复失败轮询。
- 非目标：不发布新应用、不重构业务、不增减业务权限、不清理/重放历史任务、不重启Runtime，不变更MySQL/Redis/ES配额。
- 根本地HEAD `3f38c028b2d0466951cfcdffb8f4122981de656b`，API本地HEAD `516267bf7b19bfc03581ae580704af9246ffb622`，Web本地HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`。工作区原有脏修改保留，未fetch，不称远端最新。
- 生产API是Flow5260799/426：commit `8100b7910df973374828c717dd885577528f929f` / tree `0dd124c6473fc4bbc01ba14de096a59bc648026d`，JAR SHA `3ef082481f1418b72eb273ae009a6fb476f7c0554d517087cbd582d53b0519d6`。版本字段`1.1.14-SNAPSHOT`按原记录保留，不自造业务版本。来源 `/home/isp/state/cyf-api-flow/versioned-release-426.json`。
- Runtime当前记录1.3.33 / commit `32416ed5bbde7ee25ba199ad586dbd0e4386e89c` / Flow5264702/116；本任务只读诊断，不修改外部Runtime源码或安装文件。

## 责任层 / 依赖 / 保护

- JVM容量属于主机生命周期入口，不改Web/API业务合同，不要求跨端构建。
- 修改主机helper必须同步恢复carrier中canonical摘要、monitor中carrier摘要；源码install.sh候选摘要对应更新。只替换本任务的堆参数及摘要引用，保留既有脏修改。
- 特别保留现安装helper独有的继承生命周期FD9验证和启动时关闭FD10修复；不把仓库较旧整文件覆盖生产。仓库与安装helper此前存在这一差异，本次没有借内存调整进行额外整文件同步。
- 变更前备份、精确原摘要与PID/JAR核对；现有monitor锁及coordinator→release→lifecycle锁全部非阻塞取得，不抢占其他任务。维护标记只由本任务创建/删除。
- 查询到两条历史QUEUED有效租约，但provider_started_at为空；未发现已开始模型调用且仍持有效租约的QUEUED任务。不据此宣称没有任何HTTP/SSE请求；重启会中断连接，由原机制恢复，不自动重放业务。

## 诊断与已准备候选

详报 `/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/REPORT.md`。

- 主机7.6GiB内存/可用3.5GiB；磁盘86%但采样I/O低；2核有突发争用，非持续满载。
- 原384MiB堆11:25—11:30自然负载窗口：72次GC暂停/累计2569.101ms/最长841.644ms/8次Evacuation Failure；与相同长度后窗比较，不能冒充同输入压测。
- Runtime `input-carriers-measure` 实际包含binary measurement、隔离进程初始化、restricted proxy/TLS探测，不只是文件大小统计；46秒为合并阶段，内部各段未分时，不能简单归因为模型推理或内存不足。
- `skill-conversation.mjs:pendingCommands()` 每次轮询遍历本地command，先按v5解析，再看receipt；吴用本地62份command中38份v4（34份已有receipt），24份v5（16份receipt、6份failure-receipt）。历史v4因此每约3秒重复解析报SKILL_COMMAND_INVALID。历史内容未删改。
- 同轮还会处理2份v5未闭环记录；非SKILL_RESULT_UNKNOWN错误目前不进入unknownRetries退避，日志重复出现绑定冲突。未据此删除授权/绑定检查、清理状态或自动重放。Runtime后续修复应在发现/恢复责任边界处理历史只读与确定失败的调度，不改API业务状态事实。

## 验证与维护状态

- 候选bash语法检查通过；既有health/carrier/installer 81项轻量单测通过，非应用构建/性能验收。
- 备份 `/home/isp/baks/cyf-api-heap-20261102-1130/`：安装前值、源码脏文件前值、manifest均保留。
- 维护执行证据 `/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/heap-maintenance/`；`manifest.json`固定前后摘要，`before-gc.json`固定原窗。
- 11:30:41启动维护；原API按现有helper发送TERM，应用自身30秒graceful shutdown期限后退出，未强杀。
- 首次候选PID1840032因维护控制面误启`CYF_API_STARTUP_DIAGNOSTICS=1`而带入额外DEBUG/TRACE；为保持纯堆对照，使用已安装helper的exact_api_process函数核对该候选PID/start_ticks/JAR/exe/UID/GID后TERM停止。没有将这次启动记为成功，也不归因为768MiB失败。该调用前一次pidfd Python能力探测失败，未发送信号。
- 原始失败/纠正记录在`attempt1-diagnostic-flag-corrected.json`/`apply.log`；第二次明确关闭诊断开关，`corrected-start.log`记录真实启动过程；尚需在本节追加最终健康、摘要及对照结果。

## 恢复

如候选不能健康，先查result与真实PID，保留维护标记，不无界重试。仅对本任务精确候选按现有锁与身份校验停止；核对文件仍为manifest.after后，原子恢复backup内canonical/carrier/monitor三个前值，保持摘要闭包；用现有helper启动同一原JAR与原堆参数。不得恢复旧数据库、会话、ACK、任务状态或其他任务配置。

源码文件未整体提交；不能把工作区既有改动归入本任务。当前维护不是新Flow构建/新应用发布。

### 维护后核对（11:46 +08:00）

- 正常参数候选PID1842665于11:42:38经现有helper完成健康稳定核验，启动等待295秒；所有额外DEBUG/TRACE/startup tracing参数均不存在。旧PID停止至恢复约11分42秒，含本任务纠正误启诊断的额外时间；不将整段维护表述成数秒无感操作。
- JAR SHA保持原值、runtime身份cyf-api及监听归属匹配。维护标记已删除，发布/生命周期锁已释放；已安装三helper的摘要闭包验证、文件与目录fsync完成。
- Runtime PID1823496未变，三Agent当前connected/registered/ready全部true；lastFailure仍保留维护期间ECONNREFUSED历史，不清除历史错误以冒充零故障。
- 8项生产canonical只读路径测试、5项启动shell测试通过；81项health回归此前通过。
- 扩展启动诊断fixture首次19项中16通过、3项在API冷启动同时运行时触发既有15秒超时，原失败日志保留；停止并发冷启动后，仅重跑这3项均通过（26.971秒总计），未放宽超时、跳过断言或反复盲试。不是应用Flow测试。
- 待补11:43—11:48自然负载GC窗与最终资源快照；不声称同输入压力对照或所有用户体验问题已解决。

### 最终观察与收口（11:51 +08:00）

新窗11:43—11:48：30次GC暂停/累计3048.518ms/最长883.800ms/0次Evacuation Failure；对照原窗72次/2569.101ms/841.644ms/8次。暂停次数和转移失败减少，但累计/长尾未改善；不宣称整体性能达标。新窗只有巡检HTTP样本，没有用户名册/概览数据。保留768MiB健康配置，不盲目追加调参。资源末值RSS约947MiB、MemAvailable约3.44GiB；CPU未证实改善。

最终证据已收口到 `/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/heap-maintenance/`，包括真实失败/纠正/成功日志、两窗GC、资源样本、测试、manifest和task-only.patch。临时root暂存目录已清理，备份保留。Runtime源码整改和完整用户链路性能验收尚未进行，不列为本次已完成。

## 在线 GC/JFR 续查（2026-11-02 12:13—12:17 +08:00；12:34整理）

### 执行边界与证据

- 用户在已说明在线GC分阶段日志、约3分钟JFR方案后授权继续。本轮仅临时诊断，无重启、强制GC、heap dump、模型付费调用、任务重放、新应用发布或额外堆/GC参数变更。
- PID1842665/start_ticks25922896及原Run426 JAR保持不变；源码分析使用 `git show 8100b7910df973374828c717dd885577528f929f:<path>`，未把脏HEAD当线上代码。12:30后只读health仍UP。
- JFR记录180秒，04:13:53UTC开始；具体控制时间、resource samples、前后logging配置见 `/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/online-profile/`。12:17:27已确认录制结束、仅本任务GC输出关闭，原stdout/stderr配置未变。原始录制与GC日志在 `/home/isp/state/cyf-api-dumps/juyiting-perf-20261102-1212/`，SHA256见online-profile/raw-sha256.json；私有目录保留，不上传。
- JFR包含5387个allocation samples、90个Java execution samples、1313个native samples，DataLoss=0。native大多epoll/net poll，不按CPU热点计数。CPU样本少，不据此推导精确业务CPU占比。
- 首次展开JSON膨胀至约1.8GiB，已完成流式归约并删除本任务中间文件；原始4.4MB JFR、compact事件和摘要保留。分析辅助进程已退出，未长期常驻。

### GC：已定位长暂停所在阶段，尚未证明底层唯一根因

- 录制窗内6个GC暂停事件，最长GC233 Remark **2865.206ms**（约12:16:23.541—12:16:26.406）；Class Unloading2852.315ms，内含G1 Complete Cleaning2840.334ms。父子阶段不能相加；不能仅凭该阶段名推断发生大量类卸载或类加载器泄漏。
- 同次CPU User0.97s/Sys0/Real2.87s，墙钟明显大于CPU时间；结合下述CPU压力，线程调度/同步等待是待验证方向，不能继续把全部长暂停解释为纯计算，也不直接归因于堆扩大。
- GC231 Mixed966.237ms，其中Merge Heap Roots837.17ms，而已记录的worker局部工作很小；同样需要区分调度/同步与真正根集合处理量。
- 多次普通Cleanup安全点主要耗在Reaching safepoint，约0.83—3.02秒；实际at-safepoint工作极短。进入安全点的等待不能等同所有应用线程全程停止。12:17后日志另有3.09秒，不能算入180秒JFR窗口。
- JFR启动附近RedefineClasses约890ms属于诊断启动污染，排除正常业务结论。本次有采样开销，没有无JFR同负载对照。

### CPU与内存：真实业务负载窗不同于此前低负载快照

- JFR150个machineTotal采样中148个>=90%；排除首个初始化0值，样本算术均值99.37%（不是精确时间加权平均）。因此**本次有真实业务的采样窗CPU持续紧张**，不能沿用早先低负载时“非持续满载”判断覆盖本窗。
- 同窗/proc资源样本MemAvailable约2.91—3.33GiB；API CPU增量15321 ticks/约181秒（CLK_TCK100，约84.7%单核），RSS约1.04—1.07GiB。说明内存尚有余量不等于CPU有余量；JFR与/proc口径不同，不混合相加估算其他进程CPU。
- 本机cgroup root/user.slice没有已观察到的quota throttling证据。没有同窗所有进程CPU归因，不能把竞争全部归咎于Runtime、MySQL或其他聊天。

### 固定线上源码确认的可优化调用点

1. **技能目录查询重复复制整包（优先）。** `PersonalWorkspaceExecutionServiceImpl.runtimeConversationCommandViews -> prepareSkillCatalog -> InstalledSkillDescriptorService.read -> SkillManagementService.descriptors:1000 -> SkillPackages.prepare:51 -> PlatformSkillPackageCatalog.PlatformSkillPackage.<init>:157 -> Arrays.copyOf`。bytesByDigest虽然缓存原包，但每次构造返回record又防御性复制整个byte[]；manifest缓存命中也未避开这次复制。
   - 保守排除每线程首个allocation sample及启动边界后，该构造点46个采样、权重约202MB；24个采样栈来自runtime命令查询，其余来自其他调用链。是采样估计权重，不是精确分配量/调用次数。全窗初次sample含很大的历史权重，不可把原始总权重约27GB报作3分钟实际分配；修正口径见allocation-conservative-summary.json。
   - 最小修复候选：在现有SkillPackages责任层为descriptor/manifest读取提供不构造整包副本的已验证元数据路径；保持当前授权、安装状态、摘要绑定与技能身份核对。不简单去掉byte[]防御性复制、暴露可变缓存，不将授权事实按digest跨租户缓存。真实取包/发布仍使用完整性保护。
2. **响应脱敏重复工作（次优先）。** `SensitiveDataSanitizer.redactSensitiveText:218`对每个字符串重复Pattern.compile，`SensitiveSanitizeConfig.normalize:130`每次replaceAll编译，fieldsOf每次反射建列表；90个Java CPU样本中5个包含脱敏调用。候选为配置级编译正则、ClassValue类元数据复用及无匹配不复制字符串，保留脱敏语义、异常/audit/failOpen行为；不能关闭脱敏。该证据不支持它是唯一或最大CPU瓶颈。
3. **成果列表触发内容校验。** `PersonalWorkspaceExecutionServiceImpl.listConversationOutputs:354 -> FileSystemPersonalWorkspaceStorage.openStream:110 -> verifyChannel:131`逐文件读取计算SHA；5个CPU样本落在该链的SHA2计算。是否在元数据展示路径重复执行及应如何复用不可变证明仍需契约核对；不直接删除文件完整性校验。

### 与真实请求的关联及局限

- 与先前只见巡检的窗口不同，这次记录了真实业务请求：名册POST /agent/roster 22.052秒（12:16:18完成）、技能能力15.004秒、workspace6.919秒、任务详情最大4.997秒；这是小样本观测值，不是稳定p95。归一化汇总见request-summary.json。
- 22秒名册请求结束在2.87秒Remark之前；此前12:15:03—12:15:16已有多条2—10秒请求。因此这次最长GC**不能解释全部慢请求**。名册覆盖了Mixed长暂停及安全点等待，但只有时间重叠、没有请求内部分段trace，不能精确分摊其22秒。
- SSE/events连接总时长不当普通接口延迟；499不能仅凭状态判为服务器故障。保留窗口内workspace503/404等真实记录，不因health UP声称业务验收通过。

### 下一步与状态

- 本轮诊断完成，性能未修复/未验收达标。保留768MiB堆，不继续盲目加内存/换GC/扩大线程池。
- 优先在SkillPackages目录投影责任层消除缓存命中后的整包复制，定向覆盖缓存命中/未命中、摘要与身份不匹配、授权撤销/安装状态变化、可变数组隔离；只有元数据路径优化，不扩大成跨端重构。真实代码修改、Flow重型回归、合入与发布须分别记录，当前均未执行。
- 后续再处理脱敏重复编译及Runtime已定位的历史记录重复轮询；不要把这些改善候选冒充2.87秒class cleaning的已证实根因。对同一业务流程复测接口、GC和CPU，才能判断用户体验收益。

### 技能包缓存职责与增长风险复核（2026-11-02，用户追问）

重新核对PID1842665/start_ticks25922896及JAR SHA未变，沿Run426源码8100b791分析：
- SkillMarketplaceConfiguration以@Bean创建单例SkillPackages；内部bytesByDigest与manifestsByDigest均为ConcurrentHashMap。全仓定向检索显示仅get/containsKey/computeIfAbsent写入读取，无remove/clear、容量/权重限制、TTL或淘汰；按不同内容SHA去重，不按当前安装技能集合收缩。GC不能释放仍被该单例Map引用的条目，进程重启才自然丢弃此缓存。
- 这是按需装载，不是启动全量装载；但SkillMarketplaceService.detail也调用prepare，list逐项调用detail，所以浏览商品也会装载整包，不限于真正下载/执行。InstalledSkillDescriptorService/SkillManagementService.descriptors及Runtime命令查询同样装载；升级后的不同SHA会新增条目，卸载/下架未见缓存驱逐路径。
- 缓存目的有三项：省重复读文件与SHA校验；省描述解析（当前冷路径把byte[]再写临时ZIP，遍历条目后读manifest）；使事务内prepare/manifest只读已准备数据，避免在持锁阶段做IO。第三项已形成“事务内未命中即SKILL_PACKAGE_PREPARE_IN_TRANSACTION”的实现耦合，不能只删除Map或加淘汰后任由事务随机报错。
- 真正需要的是不可变包存储、已验证描述及操作内稳定准备结果，不是所有曾访问包的永久堆副本。报价/购买等已有事务外prepare、事务内revalidate的模式；目录仅取描述，下载才取包。建议取消全局整包byte[]常驻缓存，目录使用有明确生命周期/可重建的描述投影；若保留描述内存缓存须可淘汰，缓存未命中不能变为业务正确性条件。操作前在锁外准备并携带本次数据/凭据进事务，保留当次授权、价格、安装状态及摘要重新核对。
- 整包改为按需读取/流式传送是设计方向，并非现有byte[] HTTP接口已支持流式；需保持完整性检查及授权时序，不把读包/哈希搬进长事务。仅去掉全局缓存而继续每次目录读包会放大IO，不能作为修复。
- 容量风险：常驻包内存随进程启动以来访问的不同内容包总字节数增长，另加描述对象、临时副本及其他业务堆。假设100种不同包平均5MiB，就是500MiB（非线上实际占用）；单包16MiB边界不构成总缓存上限。当前磁盘11包/24,368,042字节不等于当前Map占用，未做heap dump，不声称OOM已发生。
- 本轮只做分析，未改源码、未清空生产缓存、未重启。上一轮“缓存目的合理”仅说明潜在收益，不构成无界全包缓存的必要性证明；本次明确否定现实现的可扩展性。

## 技能包缓存优化实施（2026-11-02，用户明确授权）

- Owner：当前性能聊天；范围：取消API整包常驻缓存，目录/描述走元数据路径，操作内准备结果跨事务持有；不改Web/Runtime wire、不改授权/资金/安装状态机，不部署。
- 根API工作区SkillManagementService及其他真实依赖有他人脏修改，因此只建立一个必要隔离worktree `/home/isp/wsps/cyf-skill-package-memory`，分支 `codex/skill-package-memory`；不覆盖原工作区。已读取根AGENTS、API规则、RB-1既有职责及工具入口；接口规范固定于该基线 `docs/interface-standard.md`（wire不变）。
- fetch origin develop成功，固定base commit `17e8fc860f779594fcca9986e869c5353d7b2b8d`；线上仍Run426/8100b791、PID1842665。开发基线不是线上版本。
- 设计：整包只在下载/冷验证等真实需要时读入操作内存；目录描述缓存只存不可变包描述，按权重淘汰，不缓存价格/租户/权限；缓存容量影响命中率，不拒绝业务。现有16MiB单包边界用作初始描述缓存权重预算（约768MiB堆的2%，不是精确堆字节计量）；大于预算的描述直接使用但不驻留。操作内固定已准备描述，避免淘汰造成持锁阶段重新读ZIP或随机失败。
- 最早验证：SkillPackagesTest、InstalledSkillDescriptorServiceTest、SkillMarketplaceRealTransactionTest、SkillManagementTransactionTest及既有publication/position路径；重型编译/回归与validateLayering走Flow5260799固定候选，不在本机构建。暂未验证或合入。

### 候选与云端验证进行中（2026-11-02 14:04 CST）

- 实现提交 `c75fb2ff98ec1938a5fba6bef3b0074581be0701`；在同一隔离worktree合并远端develop `a4d31ddea4` 的既有fixture修复后，补充操作描述的跨线程隔离回归。当前候选 `b363c7fd3e1b14075653109611158f8ce17ebbe3` 已推送 `codex/skill-package-memory`，尚未合入develop。
- 自检：真实下载prepare保留操作内ZIP；目录、购买、安装结果等改describe；原生命令发现/创建/startEffect在事务外准备并限定同步操作描述生命周期。当前ACL/业务状态仍每次读取，不复用授权。定向扫描没有遗留Position.Prepared.bytes调用；`git diff --check`及渲染worker的bash语法检查通过，不算Java正式测试。
- 新增回归覆盖零预算/淘汰、事务中已准备描述、异常与嵌套清理、线程隔离、下载不读旧字节缓存、manifest身份和可变对象隔离、撤销后再校验。下载仍为byte[]接口，并未流式化；冷解析仍暂存整包，未宣称零分配。
- 共享Run433/434均终态后才配置本次验证。首次候选YAML被API拒绝，未创建Run；保留已知有效来源声明后更新成功，首次分支启动被明确拒绝、只读确认没有新增Run。修正来源分支过滤以包含候选后，创建Run435（API返回INIT来源尚未展开，待核验），未盲重发。
- Run435只执行worker测试/构建/上传，无部署/SSH/主机等待；job timeout10分钟，本机复用已有watch脚本仅监控本次返回Run435并在570秒发受控取消，以留出600秒总上限余量，不取消其他Run。启动配置SHA `4846a29aeca89f316d655b6c67e88b00249ff7b3a1ea57abefcdb38d1a9f266b`。
- 定向范围：agent skill/position、Runtime入口安全、skillManifestContract、skillManagementContract、positionSkillsTest，chat实际描述消费者与管理wire、validateLayering及fresh bootJar。复用现有renderer/worker/orchestrator，任务输入仅存私有证据目录，不修改共享默认runner或搬回本机重型执行。
- 证据 `/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/skill-package-change/`：policy、候选YAML/worker、固定启动上下文、真实Run状态与watch.log。生产未部署/重启；不把本节作为验证通过或性能收益证明。

### Run435归因与Run436（2026-11-02 14:10 CST）

- Run435实际checkout `b363c7fd3e1b14075653109611158f8ce17ebbe3`，终态FAIL；worker 14:04:24返回 `Gradle denied: invalid fixed Flow CI context/policy`，JUnit suites=0、compilerErrors=0（尚未启动编译，不代表编译通过）。根因是编排器对policy.branches使用旧名单的严格相等判断，单独调整policy未同步本次worker工具输入。
- 只在任务私有bundle中将既有branches列表追加 `codex/skill-package-memory`，同步policy与orchestrator的精确列表；未改共享root工具、未放开任意分支、未改变精确SHA/Flow身份/完整性/argv/fresh输出校验。Python AST与worker bash语法检查通过。Run435完整输入保存 `skill-package-change/attempt-435/`，不是相同失败的盲重试。
- 修正后的配置SHA `465e3dd98a605a479eade380aca6db77051c0893272adbc22a1a787d1f6a022d`；Run436已返回新Run ID且运行中，仍同一API候选和测试范围，待正式结果。监控只绑定436，来源展开前不重发start。

### 用户追加：删除历史分支白名单（2026-11-02 14:16 CST）

- 删除三处执行分支名单：orchestrator不再要求policy.branches精确旧列表或检查当前分支归属；worker shell不再case分支；制品封装不再限制分支名。默认policy移除branches，分支仍保留为来源记录。真实pipeline/run身份、commit/tree、干净源码、fixture/argv、锁与fresh制品保护均保留。
- 默认模板同步手动触发`triggerEvents: []`及`branchesFilter: .*`，仍无部署，job10分钟。任意分支可选不等于自动push执行，也不等于可自动发布。调用方固定候选和实际checkout核对仍负责精确源码。
- 原有root相关文件已脏；本次逐点修改、不提交他人修改、不回退文件。完整修改前值保存`skill-package-change/branch-policy-change/before/`，任务净增量`task-only.patch`，没有新worktree或本地Java构建。
- 工具回归：`ops/orchestration/tests/test_flow_ci.py` 9/9；`ops/ci/aliyun-flow/tests/test_backend_ci_default.py` 7/7。新增任意新分支/master/release分支及空分支来源不作为拒绝条件，错误Flow身份、源码、fixture/argv与陈旧输出仍拒绝；源码/模板diff检查通过。
- Run436已终态FAIL后才更新云端5260799；更新前完整YAML备份`branch-policy-change/before-cloud.yaml`；候选/回读canonical SHA `a3c41b0195a62f9d226f77e07d992baee358863afa209939d771c52c06d307ad`，状态APPLIED。没有另开规则验证Run、没有应用部署。回读与测试日志保留`branch-policy-change/`。

### 缓存候选Run436结果（保留失败，不冒充验收）

- 固定API候选仍`b363c7fd3e1b14075653109611158f8ce17ebbe3` / tree `857bb7997850782deba4f32305b4ed4cf2b92388`。Gradle真实执行约171秒，42份JUnit报告共496项，448通过、9失败、39跳过；compilerDiagnostics为空。
- 本次核心回归已通过：SkillPackagesTest12、InstalledSkillDescriptorServiceTest15、SkillExecutionServiceTest58、SkillMarketplaceRealTransactionTest29、SkillManagementTransactionTest36、publication7、Runtime入口安全23等。仍不是整轮通过或性能收益验收。
- 9失败均为PositionSkillTransactionTest setup缺少`CYF_POSITION_TEST_JDBC`，不是缓存实现断言失败；必须给其现有测试提供worker内隔离loopback MySQL。39跳过分布于SkillExecutionSchemaMySqlTest6、SkillInstallTransportMySqlTest4、SkillNativeAckMySqlTest29，需按实际受影响范围核对这些既有测试的独立数据库入口，不把跳过计入通过。
- 本次没有直接删掉position测试求绿，没有本机重型测试，未合入develop/未部署。下一步补齐云端隔离数据库夹具后对固定候选继续验证；没有运行中的本任务Flow。原始Run436日志、压缩诊断解码及watch终态保留在`skill-package-change/`。

### 接续验证Run437（2026-11-02 14:25 CST）

- 复用同一worktree，合并已推送develop `71d7548664`（既有funded-claim owner修复及测试），固定候选 `ab3da7286f140e32c45e542e9638d2bb5efff2e7` / tree `f42eda5cb1a633b0040ea97e332fb1aac4ba5df4`；未改他人工作区。
- 定位到已有岗位验证准备片段 `/home/isp/state/cyf-reusable-skills-20261102/skill-position-release/prepare.py`，提取并复用其worker临时MySQL初始化/loopback随机端口/精确PID退出清理。为现有position与skill集成用例提供相同隔离实例的不同JDBC入口和明确isolated标记；各测试仍独立随机数据库。不会使用本机或生产MySQL。任务片段见`skill-package-change/isolated-mysql-setup.sh`，云端worker运行，非本机启动。
- 本次renderer直接使用已删除分支白名单的共享orchestrator/worker/template，不再做候选分支补丁；仍精确commit断言、固定测试输入和真实Flow身份。完整上一轮输入保存`attempt-436/`，没有覆写失败证据。
- Run437已创建，配置SHA `395263b67ef3b15d28ed29cf33ce1c67d7f8071c6b98ebb49bd2cc3d5004d6f0`；同一任务时限监控绑定437。仍仅测试/构建/上传、不部署。待结果，不预先计通过。

### 验证、集成与收尾完成（2026-11-02；未发布）

- **Flow5260799/437 SUCCESS**，监控终态约244秒，总耗时在600秒内。实际固定源码为 `ab3da7286f140e32c45e542e9638d2bb5efff2e7` / tree `f42eda5cb1a633b0040ea97e332fb1aac4ba5df4`。42份XML共**496项，0失败、0错误、0跳过**；上轮缺隔离数据库的9项及跳过的39项本轮均真实执行通过。Run435/436失败记录原样保留。
- 从同一Run下载并流式核验不可变制品：归档223,851,302 bytes，SHA-256 `6e49a09aa1804c107b1c5bcd2246d91d43416b7e91ba4373fd5551f6f624db1d`；application.jar 251,350,181 bytes，SHA-256 `85ae00ca407a7f2e139dd5dde0716d56c7e777561a44c1e708d9760977a6df14`。receipt/source/run/tree、metadata摘要、依赖文件摘要与逐份XML汇总全部相符；未解压或安装到生产。
- 验证summary中8个必要任务均为本轮fresh、非skipped/failed：agent test/skillManifestContract/skillManagementContract/positionSkillsTest、chat test/skillManagementWire、validateLayering、starter bootJar。`artifact-verification.json`、`verified-test-summary.json`、原始制品及来源保存`skill-package-change/`；后续已授权安装应复用437制品，不因下载/安装另开构建。
- 精确同一受测提交已fast-forward推送组件`develop`；远端readback `ab3da7286f140e32c45e542e9638d2bb5efff2e7`。未覆盖或checkout主API脏工作区，未强推。稳定内存职责回写既有`docs/juyiting-runbook.md`，API详细说明已随受测源码提交。
- 本任务结束后在无活动Run且确认当前配置仍属本任务时，恢复**已删除旧分支白名单的新默认配置**（不是恢复旧规则）。回读canonical SHA `a3c41b0195a62f9d226f77e07d992baee358863afa209939d771c52c06d307ad`；手动触发、任意候选分支、worker-only不变。证据`restore-default.json`及修改前备份。
- 已确认隔离worktree干净并删除`/home/isp/wsps/cyf-skill-package-memory`，清理本任务3个临时编辑脚本；远端候选分支、正式源码及必要诊断/测试/制品证据保留。未清理其他任务目录、状态或生产备份。
- **完成范围：代码优化、定向正式回归、合入develop、制品核验。未执行：生产安装/重启及线上同业务流性能复测。** 不宣称当前线上已经取消全包缓存或GC/延迟已达标；后续需明确发布候选授权并按主机独立安装流程推进，再比较接口延迟、CPU、GC与内存。

### 获授权接续发布前检查：主机旧分支限制与整包兼容性（2026-11-02 14:46 CST）

- 用户在说明下一步固定Run437发布后回复“继续”，本次按固定制品安装授权推进准备；没有新开Flow、没有重建或改写437制品。
- 只读核对生产仍为Run426/8100b791、PID1842665，canonical JAR SHA `3ef082481f1418b72eb273ae009a6fb476f7c0554d517087cbd582d53b0519d6`，cwd `/home/isp/hosts/cyf/api`，health UP，Xms256m/Xmx768m保持。
- 查出遗漏的主机分支门槛：`ops/ci/aliyun-flow/host/cyf-api-flow-deploy`与`cyf-api-flow-install`仍把receipt.branch写死develop。Run437虽已FF合入develop，receipt真实来源仍为codex/skill-package-memory，不能篡改receipt冒充develop。已在源码精确移除两处名单，保留clean/source commit/tree、真实Flow身份、摘要、测试退出码、授权、锁和恢复。没有整文件覆盖其他Owner改动。
- 新增`test_api_host_branch_policy.py`直接执行两个实际receipt判定表达式，验证任意分支及脏源码/错误身份/失败构建；3项通过。既有`test_api_flow_*.py`44项通过；总47项轻量工具回归，无Java/数据库/构建。Python AST与bash -n通过。生产helpers尚未更新，不能宣称主机分支限制已经解除。
- **本轮停止在安装之前，不以专项496项替代整包发布验收。** 437相对线上还包含另Owner的全库CHECK撤除与岗位发布权限变更。其handoff `REUSABLE-SKILLS-20261102.md`记载大范围回归434失败、后续固定71d754待正式验证；437的8个定向任务并未覆盖其完整schema/资金/Chat回归。尚无完整整包发布证据。
- 当前主机发布器安装后会继续调用F06/E05 schema helper；实际已安装helper仍含旧CHECK规则/SQL摘要，另Owner的CHECK-free helper只在候选目录，尚未同步。直接调用可能先替换JAR再在schema阶段失败，故没有试错安装、重启、DDL或覆盖他人的helper候选。无需为发现此问题触发一次失败发布。
- 本次源码净增量、修改前源文件和实际安装文件快照、47项日志与readiness摘要均保存`/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/skill-package-change/host-branch-policy/`。源码修改未独立提交（root相关路径已有其他任务修改），亦未安装。下一步须收口固定整包候选的必要回归及主机helper兼容，随后复用有效制品受控安装；全库CHECK迁移仍归原Owner明确授权/真实快照流程，不纳入性能任务擅自执行。

### Run439线上核对与性能续测（2026-11-02 15:43 CST）

- 另一Owner已承接整包必要回归及安装，本任务不再安装437或接管其迁移/进程。439固定源码`8ad42be7815e499077c6a97439f0f13c96c7650e`/tree`129909ac3c71c022fffe3256bf16c0f17c9ee046`，git祖先核实包含缓存候选ab3da728；实际JAR SHA `3e1fb1d77e471915b73c1cd540bbe08ac915c2e91dd5a4f7f989586b22e26422`与installed record/versioned-release-439一致。安装器exit0；更广回归/迁移/岗位业务验收由REUSABLE-SKILLS-20261102 handoff负责，不在本任务重标。
- 15:32初查PID1940953健康；15:33观察时发生第二次进程切换，PID1946296/start_ticks27342192、同JAR；健康端口曾拒绝连接，15:38:52和15:40:00复查UP。没有自行停止/重启进程，也未推断第二次切换的原因。首次采样绑定旧PID，jstat失败、末次health失败，明确标为INVALID_FOR_API_COMPARISON；不能用shell结束0冒充采样/健康成功。原证据保留。
- 现有GC日志等长自然流量窗：旧PID15:15:00—15:18:00，10次暂停/1829.784ms/最长925.230ms；首个新PID15:29:30—15:32:30，10次/515.161ms/最长136.965ms。**负载不同**：前窗名册2次200（最长4.924s），后窗只有map401巡检，没有成功名册样本；不能给出用户延迟改善率或声称缓存优化的因果收益。
- 第二进程有效采样15:39:46—15:41:50，前后身份一致、工具exit0、末次health UP。API平均CPU65.56%（100%=一核）、RSS约857MiB；Runtime19.35%/约357MiB，MySQL11.04%。主机平均idle1.65%、iowait2.98%；15:42可用内存约3070MiB。堆末帧344MiB已用/453MiB当前容量，最大仍768MiB；FGC增量0。不据可用内存继续盲目加堆或扩大其他池。
- **长暂停仍存在**：新有效窗6次GC pause共1078.611ms，最长909.354ms。GC102主要为Evacuate Collection Set906.47ms；Humongous regions0→0，208M→138M(453M)，User0.82s/Sys0.02s/Real0.91s。与早先Remark/Class Cleaning长尾不是同一个阶段，也不是本次大对象分配触发的直接证据；没有充分依据把它归因于技能整包缓存或纯调度等待。整包缓存优化已随源码上线≠GC/体验已达标。
- 后续10秒全进程CPU只作另窗定位：API89.55%、MySQL17.95%、Runtime12.77%、短命python8.23%、headless_shell7.49%；不把另窗数值混算到前窗，不操作不明归属进程。下一步对同类成功业务请求同步取当前分配/GC分阶段证据，分清剩余对象搬迁成本与CPU竞争；当前不加拒绝阈值/强制deadline。
- 本轮仅只读诊断，未重建、安装、DDL、改堆/GC参数或追加JFR。全部观测进程已正常结束。证据`/home/isp/state/cyf-diagnostics/juyiting-performance-20261102/post-run439/`，有效窗在`second-process/`。稳定runbook已更新真实线上来源和性能未验收边界。
- 分支限制状态另行保留：源码两处移除及47项轻量测试已完成；15:33核对实际`/usr/local/sbin/cyf-api-flow-deploy`和`cyf-api-flow-install`仍有develop限定，尚未安装本任务补丁。此次439来自develop所以未被阻止，不能据本次成功宣称主机名单已经解除；不覆盖另一Owner正在维护的helpers。

### 主机分支限制收口（2026-11-02 15:53 CST）

- 继续沿用户删除旧分支名单的授权，以上一轮47项源码工具回归为基础，读取当前已安装helpers（保留另一Owner已上线的CHECK-free/schema与现行路径逻辑），只移除deploy/install两个receipt.branch==develop条件。没有把root脏文件整体复制到生产，没有更改receipt/制品/当前发布身份。
- 真实安装候选直接执行3项分支/clean/Flow/source/失败构建谓词回归通过，Python AST及bash -n通过；取得既有coordinator→release→lifecycle三锁（nonblocking，未抢锁）后校验前值、保存备份、原子替换并readback。生产API的PID/start_ticks/JAR身份未变，未重启、未运行DDL或触发新Flow。安装后canonical路径8项通过，health UP。
- deploy SHA由`67adc8632597f4c37a708146f1c1f6143a51f741f174972e5bffc37e87f97e37`改为`659ba4cd31b924d8c6d885604aeffa0eef76acad32b12c7a6d395931d0e41be7`；install SHA由`20a843ab3d0a8a22569bd441c6a755a0fc8d76f4ceb9f6a42bd3661b923cdf61`改为`750a0bf19f8dff749697ec13ee20ae4eec8d76c3ac1a53c6094fa8759f691831`。旧catalog/历史授权不改写；后续helper维护以当前摘要为前值，不能覆盖回旧候选。
- 备份`/home/isp/baks/cyf-host-branch-policy-20261102-1552/`；候选、测试、安装脚本和readback在`skill-package-change/host-branch-policy/{installed-candidate/,installed-candidate.json,installation.json,canonical-path-check.txt}`。本次仅运行规则同步，不等于额外应用部署；任意分支仍须真实Run、固定commit/tree、干净源码、制品完整性、授权与受控安装。

### Run439限时采样定位（2026-11-02 16:06 CST）

- PID1946296/start_ticks27342192/JAR身份前后未变；复用既有capture，采样名cyf-perf-20261102-1547、JFR180秒，15:47:54启动回复，15:50:59采集结束，15:51:09确认无活动录制。仅开启本任务独立GC/safepoint输出，finally关闭并核实原stdout/stderr不变。没有强制GC、heap dump、参数调优、模型调用、业务压测或重启。
- 原始JFR5,335,476 bytes；分析采用流式读取并压缩保留选中事件，没有生成上次1.8GB级JSON。分析在采样结束后进行，不混入采样CPU结论；诊断工具自身有开销，不宣称本次是无探针基准测试。证据`post-run439-profile/`，原件`/home/isp/state/cyf-api-dumps/juyiting-perf-20261102-1547/`，SHA见raw-sha256.json。
- 134个Java ExecutionSample中，49个栈包含MyBatis queryFromDatabase（约36.6%，不是数据库等待耗时占比）；64层原始栈进一步定位runtimeConversationCommandViews、InstalledSkillDescriptorService/SkillManagementService.descriptors、任务根锁/绑定与grant等读取。公共filter经常位于栈底，不因此认定filter自身就是CPU热点；SQL解析栈只占很少分配样本，也不能把MyBatis外层反射栈当SQL解析主因。
- 6842个对象分配采样；逐线程排除首次sample weight（可能包含录制前分配），剩余权重仍仅是估算，不宣称精确分配吞吐。MySQL协议相关栈权重约385MB；固定正则重复编译相关约44.7MB，主要为SensitiveSanitizeConfig.normalize（约26.4MB）和SensitiveDataSanitizer.redactSensitiveText（约13.6MB），并非全部API内存。调用链分类彼此包含，不能累加为总量。
- **未采到技能包byte[] clone。** 初次宽匹配出现1条clone，但objectClass实际为Class[]、来源Class.getInterfaces/MyBatis代理构建，不能误报为整包复制；最终分类要求byte[]+clone+SkillPackages栈。未采到不等于实际下载零复制，当前真实下载/冷解析仍允许操作内整包读取。技能包缓存优化与接口权限读取责任边界不变。
- 本轮GC8次完成暂停合计1191.842ms，最长GC135 Remark961.683ms，其中Class Unloading952.232ms、G1 Complete Cleaning901.651ms，父子不能相加；User1.01s/Sys0/Real0.96s。另见Cleanup安全点reaching等待818—889ms，但其at-safepoint仅数微秒，不能把整个reaching算作GC STW。上一轮909ms是Evacuate，本轮是Remark，不能合并为单一已证实根因。
- 进程/proc CPU增量约119.93%（100%=一个核，观测181秒），JFR machineTotal均值约98.1%，采样期间MemAvailable最低约3608MiB；现行API cgroup cpu quota=-1、throttled=0。仍有CPU竞争证据，没有新增内存门槛/扩大所有池的依据。
- 同窗慢/错误日志（不是全部请求分布）：conversation commands成功慢请求27条，最大18.901s；workspace commands30条，最大5.931s；名册成功慢请求3条，最大13.109s。ACTION_SELECTION_INVALID16条、ACTION_DELIVERY_PARENT_INVALID4条仅是错误日志次数，不当独立任务数，也不自动重放/删除任务。名册明显仍慢，不能因较早低负载GC短窗改善宣布体验达标。
- 优化优先级已进一步收窄：先沿命令发现/恢复和技能描述查询核对重复读取/反复错误来源，在原职责层减少无效工作；权限/撤销/fence/事务锁不能通过跨请求授权缓存省掉。固定默认正则可另做仅编译复用、不缓存用户内容的局部修复；本轮尚未改Java实现，不宣称这些新热点已经优化。必要源改动须固定当前候选、定向云测后独立发布，不覆盖其他Owner的最新develop。
- 本轮另一项已完成：主机deploy/install分支旧名单15:53已受控同步（见上一节），仅移除分支名单，保留来源/授权/完整性/锁/恢复；不是绕过实际失败证据。所有本任务采样/分析进程已结束，无后台监控遗留。
