# NATIVE-READINESS-DECOUPLE-20261108

## 范围与基线（2026-11-08 +08:00）
唯一Owner：本会话sol-owner/developer。用户授权“实施”：实现、定向验证、自检与develop集成；不发布、不重启、不改生产配置/凭据/数据库，不派发子Agent。

目标：无资料读取配置也可初始化/测量/声明原生执行；详情与实际执行使用同一运行对象和能力事实；失败不伪报就绪。RB-03负责运行环境/声明，RB-02保持任务/安装授权，RB-01只展示原因。
非目标：新能力平台、协议/数据库扩建、技能专用编排、复制其他主体配置/凭据、历史任务重放、付费模型验收。

规则已读取：根AGENTS、Runtime源仓AGENTS（本CYF任务显式适用根规则及RB-1）、web/AGENTS、specs/AGENTS、ops/orchestration/README；公共接口按api/docs/interface-standard.md的线上固定888a164版本（v1.4基线及既有后续兼容条款），不修改脏API工作区。

23:16附近只读fetch/ls-remote：Runtime远端develop5dc596c9721000bcbca3c9dcb38d7b8e1c8d3a1e；Web远端develop0791132b92bd81a7c0b1ea15411949c7e05d2e91。两个主工作区均有他人脏修改且落后远端，为并发写入/源码冲突仅各建一个任务隔离工作区：
- Runtime `/home/isp/wsps/worktrees/native-readiness-runtime-20261108`，branch codex/native-readiness-decouple-20261108，base5dc596c。
- Web `/home/isp/wsps/worktrees/native-readiness-web-20261108`，branch codex/native-readiness-copy-20261108，base0791132。
- API：当前已发布888a164已有原生指令技能判断；先核对消费者，合同未变不默认改API。

前轮只读诊断证据：`/home/isp/state/cyf-local-build/tasks/lujunyi-skill-readonly-20261108/diagnosis.json`。真实ziyue GET profile三项installationVerified=true、NATIVE_EXECUTION_NOT_READY；Runtime3307914资料对象未创建，启动measure约0.077ms跳过。不要把此诊断当本候选测试或上线证据。

## 验证计划
先固定候选commit/tree；普通磁盘源码/输出/缓存/临时目录，复用Node既有测试入口，不在生产目录运行。累计测试/构建/打包600秒（含阶段内等待），真实耗时与日志留包外。覆盖原生执行、资料读取、注册刷新/关闭、技能及隔离/授权相关定向回归；Web原型先行，原因映射与组件测试。禁止自动连接付费模型/生产执行。无必要API代码变化则不启动Gradle/JAR构建。

## 设计/实施/验证/集成状态
源码改动、定向回归及Web生产构建/归档校验已完成，Web与Runtime已快进合入远端develop（2026-11-09读回）。未部署，未修改生产配置/状态。下述失败/预算申请为原始阶段证据，最终续作见文末。

### 实际改动
- Runtime：从资料类机械抽取共享进程/目录/网络隔离 `isolated-engine-profile.mjs`；独立 `NativeExecutionProfileRuntime` 持有原生探测/声明/执行。未复制第二套执行器、未增加协议/DB。
- agent-client：无资料载体也创建原生Owner；探测single-flight；注册（含重连）/执行/提交及失败清理消费同一Owner。资料构造/测量失败与原生失败隔离；关闭期间阻止晚启动/刷新，dispose等待所属探测后清理。
- 同主体Provider旧字段兼容；显式原生Provider不与不完整旧配置拼接，不自动复制凭据。新根按主体隔离，旧根保留恢复路径；manifest继续统一检查跨主体可写根。托管模板只允许新的Provider标量，不继承私有根。
- 补入Runtime制品显式清单的两个新模块，保留导入闭包/依赖校验。bridge1.1.57 / Runtime1.3.68候选。
- Web：唯一原型先增native-unready状态，再增加`NATIVE_EXECUTION_NOT_READY`→“原生执行环境未就绪”，保留已核验安装与计数、不提示重装。Web1.16.129候选；真实AgentPanel沿既有formatter消费，不额外改组件/接口。
- API：无变化（已发布888a164已能消费原生指令技能），不碰脏API、不跑无关Gradle。

### 原型
隔离工作区`prototypes/juyiting/`现有入口与文字规格，状态`?agentSkillState=native-unready#agents`。复用原详情响应式内容，没有布局重构。任务专用预览18789（18786已有他人服务，未操作），本机HTTP200已取回；尚未真实浏览器截图，不冒称PC/手机像素验收。最终停止本任务预览，不保留常驻服务。

### 验证过程与证据
普通磁盘（ext2/ext3）源码、依赖及TMPDIR；既有依赖只读符号链接复用，无npm ci/网络下载。日志包外目录：`/home/isp/state/cyf-local-build/tasks/cyf-native-readiness-20261108/evidence/`；累计耗时见`verification.json`。
- 系统Python3.6不支持`text=`的包装器前置失败：无应用测试启动，修正为universal_newlines，预留1秒计入预算；证据wrapper-preflight.txt。
- 首候选fb7a431 / tree2e61dc180fd9668e659a5e049407719f5e615505：734项，710通过、9失败、15跳过，221.132秒。9项同根因：新增模块未加入制品清单，RUNTIME_PAYLOAD_IMPORT_MISSING；保留原失败日志，绝不当通过。
- 修正候选7d620bc补齐清单，并覆盖资料构造失败不抑制原生Owner；完整同selector重测：736项，719通过、2失败、15跳过，230.010秒。仅新增host测试fixture缺release-local delivery工具链；不删除校验，修正为隔离复制库+不执行的解释器fixture。
- 真实原生隔离/付费模型E2E为opt-in，未启用；不把mock/工具测试或聊天回复当真实技能端到端成功。


### 首轮固定候选与证据复用（历史，最终Web候选见续作）
- Runtime `92df9eb8de9abf523dd7224e575c43329139a98b` / tree `31d4d7e0899f1692e924c248702fb3f19e2e48fd`：相对7d620bc仅修正 `conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs` 的fixture，生产源码、其他测试/fixture完全相同；该文件完整重跑117/117通过（56.119秒）。其余selector复用同字节输入的上轮证据；合并去重为721通过、15 opt-in跳过、无剩余失败，**不是最终tree整轮再跑一遍**。
- Web `c270a3dc0df1f742282db6c87fb83a937582aabe` / tree `aa4b0d2cd4487a6720ebf358df29c8931cf8252d`：最终65项全部通过（4.383秒），实际AgentPanel技能状态节点保留安装且无is-ready，覆盖市场生命周期与名册。此前断言误把“运行就绪不代表授权”的固定说明计入就绪，保留64通过/1失败日志，已改为真实badge断言；中间通过证据亦保留。
- Web原配置生产构建失败（12.139秒）：复用的共享node_modules缺 `pdfjs-dist@6.4.299` 与 `pako@2.1.0`，不是本任务改源码引入的依赖。未修改共享目录/lock，未externalize绕过。构建产生的任务工作区src/components.d.ts已恢复固定HEAD原字节；未覆盖主工作区。
- 在任务私有node_modules目录中按lock的resolved+sha512准备补包，但下载阶段耗时56.924秒：pdfjs-dist已下载并通过原lock SHA-512核验；随后pako下载HTTP403，未放宽完整性。共享目录依然只读；该补包过程是构建前置，同批计时未重置。
- `verification.json`命令测时累计591.928秒；加包装器前置失败保守预留1秒，预算使用约592.928/600秒，剩余约7.072秒，不足完成依赖恢复/生产构建。所有原失败日志保留。recordedAt是命令结束记录时间，未冒充开始时间。

### 历史预算例外申请（2026-11-09用户“继续”后按此前900秒申请接续）
申请本固定任务/源码同批测试、构建、打包总上限 **600→900秒**（额外300秒），仅用于从可达的既有包源/本地缓存恢复lock精确字节、再次Web原配置生产构建及必要的依赖变化回归。网络403先归因，不原样盲重试；新源必须匹配原lock完整性，不改版本、不改变业务源码。若仍失败保留证据，不发布。安装/健康不计此预算，但本任务本来也没有部署授权。

恢复时先读取本handoff、verification.json与source-inputs.json，保留同一预算/批次，两个最小隔离worktree继续复用。不要重跑整轮Runtime；当前剩余源代码未改。待构建成功和自检后再安全快进develop；当前仅本地任务分支commit，不声称已合入或发布。根规格局部修改保留在已有脏工作区，未将他人的历史/规格变更夹带提交。无最终可回收包；不虚构mark-complete登记。专用18789预览已停止，他人18786服务未动。

### 依赖来源复核（用户追问后更正）
本任务未新增依赖，仅升Web补丁版本。pdfjs-dist由b75c155于2026-10-22加入；pako由4a9f421于2026-09-08加入。复用主工作区node_modules的隐藏安装lock最后修改于2026-10-09：不含pdfjs-dist，虽记录pako2.1.0但实际包目录缺失。可确认安装目录与候选lock不一致，不能仅凭缺目录推断被谁删除或何时损坏。补包日志明确pdfjs-dist已成功校验，403发生在pako下载；此前会话及本handoff“首包403/均未取到”表述不准确，以上纠正。未继续构建或重置预算。

## 后续依赖共享工具（2026-11-09）
用户对按lock/toolchain共享安装集合授权“好，处理吧”，已在既有local_web_build.py接入，详见 `WEB-DEPENDENCY-SETS-20261109.md`。该范围17项依赖测试、7项存储测试、5项发布控制器测试通过；包含极小fixture的真实npm与Vite冒烟，不是本技能候选生产构建。本工具验证独立留证，不重置本任务约592.928秒预算。真实Web共享集合尚未准备，原候选生产构建未恢复、未合入/部署；待足够普通磁盘空间和原批次构建例外后继续，不自动替换现有工作区node_modules。


## 2026-11-09继续：真实共享依赖、构建与develop集成

用户在被告知原批次等待例外后答复“继续”，开工前已明确按此前申请同批900秒接续，不重置已用约592.928秒；记录 `evidence/build-budget-continuation.json`。未扩大为部署、生产数据或付费原生模型验收。

### 实际输入/修复
- 只读复核发现根npm缓存已包含pako与pdfjs-dist的精确tarball；两包先按原lock SHA-512确认，随后由npm ci用原lock完成安装。未新增依赖/改版本/放宽integrity，未再次盲试403地址。
- 只对本任务Web工作树稀疏排除定向selector未引用的 `tests/fixtures/juyiting/`、`tests/game/sprites/`，保留全部生产文件、测试源码、interface与技能fixture。移除本任务私有临时补包目录和已结束测试的编译缓存，未动主工作区依赖、他人缓存或生产目录。证据storage-preparation/private-dependencies-before-retirement/private-cache-retirement。
- 真实完整共享集合 `be17a0949f5e5802a8bc6d46ec3b326f0b27068e615c8a6737abd978fe108c08`，实体位于 `/home/isp/state/cyf-local-build/web-dependencies/<key>/`。依赖首次准备24.106秒，npm ci/ls、只读发布、全树摘要校验通过。
- 首次真实构建在runner加载既有Vite配置时报隐式 `__dirname`（0.895秒失败，112通过/2 pending的原报告保留）。**不回写共享依赖或加全局变量补丁**；仅将Vite目录取值改为 `path.dirname(fileURLToPath(import.meta.url))`，保持alias/LESS绝对路径语义，新增真实runner加载回归。Web最终 `038a571a0604a2ef04041e575cd37c64f8f13a33` / tree `04ce479456285e0efcdeaa76cbdbf041b0591ccd`，manifest/lock与前候选相同，仍1.16.129。
- 依赖工具极小fixture增强为ESM目录+alias导入后，17项通过（5.660秒，计入本原批次），旧7项存储/5项发布控制器输入不变，保留原有效证据；没有重复整轮Runtime。

### 最终验证与预算
第二次构建共48.074秒（含wrapper），依赖复用3.802秒，测试9.401秒（**113通过、2 pending、0失败**），原生产配置构建23.486秒，打包5.190秒，归档完整性0.994秒；差额为工具初始化/输入及共享集后验。sourceUnchanged=true。原批次全部验证命令累计680.191秒，加保守前置1秒为 **681.191/900秒**；所有早期失败、等待及重跑均保留。共享工具独立首轮17.632秒没有混入此数，也未拿来重置预算。原任务最初完整墙钟未完整埋点，不伪报为681秒；本次接续首条观测为00:14:34+08，状态文件单列接续观测墙钟与受限阶段耗时。

最终Web包107946064字节，SHA-256 `6ee8bf8cb35c6c509835f05f6ebfcfad8481249d3ed4697032efe2e9ee2eb169`。构建原输出 `web-final-retry/package/web.tgz` 已**仅同盘移动**到本任务 `package/web.tgz`，未重打包；原producer result保持历史路径，现位置由 `evidence/artifact-retention-location.json` 明确绑定。源码/工具/报告/manifest/共享集receipt均包外留存，不伪造Flow来源。

### 集成/收尾/未做事项
- 2026-11-09 00:24+08只读Flow GetPipeline确认Web4403172和Runtime5264702的triggerEvents均为空，未写配置、未启动Run。00:25–00:27，两组件仅快进push develop并ls-remote读回：Web038a571、Runtime92df9eb。主工作区分支/脏改未动；Runtime仍为精确已测试源，diff-check仅额外EOF空行的样式提示不作为无规格硬门禁，不为此改候选或重跑业务测试。
- 两个本任务worktree在确认干净且远端绑定后删除；先解开任务依赖链接，**共享目录与主安装目录未删**。磁盘从约34MiB回到约198MiB，仍紧张，不声称主机容量问题解决。
- 最终Web包在既有completed-tasks登记精确commit/tree/SHA，仅用于24小时、每组件最近两批与当前/回退保护下的后续回收；未执行clean。首次mark-complete的stdout直接打开任务证据文件，触发“task still active”保护；改为内存捕获后成功登记/读回，不关闭进程保护或绕锁。后续复用先mark-active。
- 根共享工具与先前未提交builder文件共处脏工作区，仍按文件SHA留证，**没有夹带他人内容整包提交**。此事实不影响本次实际本地构建证据，但不能声称根工具已合入。
- **未部署、未重启、未改生产配置/数据库、未运行付费原生E2E**；Runtime本次未产发布包。线上卢俊义状态尚未用新候选切换。后续安装仍需明确发布授权；Runtime打包按实际授权/精确源码安排，不把Web包或develop合入当成Runtime已交付/上线。

完整证据入口：`/home/isp/state/cyf-local-build/tasks/cyf-native-readiness-20261108/evidence/current-status.json`、原 `verification.json`、`web-final-retry/{result,manifest}.json`、develop-integration.log、worktree-cleanup.json及artifact-retention-registration-readback.json。


最终收尾读回（2026-11-09 00:32+08）：既有ledger已转accepted（仅开发/验证/组件集成，不是发布）。自有临时目录已删除，wrapper/补包/只读查询脚本先存至evidence/runner-sources；包外日志、测试报告、manifest、receipt和最终包未删除。最终主机可用空间约1.3GiB（00:29工作树收尾后曾为198MiB；未对同期全部主机空间变化归因，不宣称均由本任务释放）。接续观测墙钟1064.925秒与受限测试/构建/打包681.191秒分列于current-status.json；原任务完整墙钟未知。后续重用已完成包先mark-active，安装仍需发布授权。

### 2026-11-09 00:43+08 部署授权后准备：空间不足，未切换

用户明确回复“部署”，授权本任务固定 Runtime1.3.68/92df9eb、Web1.16.129/038a571；不包含API/数据库/付费模型。Web最终包已先通过既有工具mark-active撤销完成登记，证据`deployment-mark-active`对应实际`evidence/deploy-mark-active.json`。未重复Web构建，未启动Flow。

Runtime以Git archive提取完整固定提交中两个组件的干净源码（不使用脏主工作区，不新增worktree），调用候选已有collateExecutionPayload并复用生产已验证、去除根name/version后完全一致的lock依赖。包`runtime/package/runtime.tgz`，13,395,282字节，SHA-256 `172ebdfa3019d748cacf93b9bcb33f88b88ea14849c22250dd1088d625e31274`；`release.json/build-evidence.json/package-result.json`包外保留。归档逐文件SHA/mode和完整集合验证通过，`deployment/runtime-archive-integrity.json`。测试沿原精确输入复用，不把有2项host fixture失败的基批重标PASS；最终host117项替代对应旧suite，综合721pass/15skip，详见build-evidence。准备与打包3.978秒、完整性与本任务临时输入清理0.807秒，原批累计**685.976/900秒**，未重置；安装、备份、健康不使用剩余构建预算作为deadline。

**未部署、未停服**：已只读发现空间不足，未为单独Web先行而产生部分发布。当前普通磁盘可用1,307,320,320字节；现有程序占877,744,128字节，最近真实状态备份占589,660,160字节，两项估计合计1,467,404,288字节，短缺约160,083,968字节（约153MiB），且当前新状态备份实际大小尚未知。此为具体暂存/恢复需要，不新增任意空间门槛。既有清理器plan可合法回收0项；不删除其他任务/缓存/历史备份。只清本任务新生成payload/source/tmp，保留宿主probe源码及所有日志/manifest/最终包。空间证据`deployment/storage-readiness.json`，清理plan=`deployment/storage-plan.json`。

00:43读回生产：Runtime仍1.3.67/5dc596c、PID3307914，3主体connected/registered/ready；Web仍1.16.128/0791132、online_verified。原卢俊义技能问题尚未由新候选线上验收，不能把通道健康当技能可用。当前Runtime安装器**尚未为1.3.68适配/执行**，可复用原image-usage-20261108的LOCAL受控安装器，但须绑定新版本/源码/真实证据与前代摘要，并将旧startup探针中的TypedInspection原生Owner改为新NativeExecutionProfileRuntime（不调用其资料measure），保留原身份/锁/备份/恢复事务；候选宿主probe已保存`deployment/host-probes`。Webstandalone deploy_local入口已确认，不运行会重建并安装API的local_release.py。

下一步：落实额外普通磁盘空间/备份存储后，沿已有用户授权继续Runtime宿主prepare/受控安装→通道与卢俊义声明/技能只读验收→Web包安装及线上资源校验。无需重复申请已给的部署权限。当前为待续部署，包保持active不登记为任务已完成；未触发清理。

### 2026-11-09 01:41+08 部署完成及只读业务验收

用户“继续”后复核空间可用约1.62GiB，沿原授权部署精确Runtime1.3.68/92df9eb、Web1.16.129/038a571，不构建API、不操作DB、不启Flow或付费模型。以下替代前节storage blocked状态；原失败证据保留。

- Runtime候选在独立暂存位置验证，停写备份真实state.tar.gz约617MiB（78.764秒、tar compare23.599秒），旧程序原子归档后安装到固定app。备份`/home/isp/baks/cyf-agent-runtime-v1/20261109-native-readiness-local/`保留old-program、状态和配置，状态SHA256 `c0eb64e922e0e6216eed8d35497daf432513ff864d2d1a77ac212df001d3e180`。不恢复旧状态覆盖新事实。
- 首次prepare因177处Python缓存差异拒绝，未停服务。逐项166个pyc以相同Python3.11.13、固定源摘要及marshal/compile证明等价（另11目录）；仅允许此已证明派生缓存差异，其他程序漂移继续拒绝，原manifest未重标。新增定向策略6项、admission11项通过，实际宿主工具链3项通过无skip。安装/恢复核心身份/锁/备份行为保持。
- 首次启动发现卢俊义自身native Provider缺配置，受控补入同主体codexHome中的gpt、baseUrl和responses绑定，以及既有restricted-proxy合同所需10000ms socket connect timeout。仅连接传输超时，不是模型请求/流/安装deadline；不变更身份、模型或其他主体配置，不借凭据。配置前值在备份native-provider-config。最终PID3607269，三主体connected/registered/ready及三原生启动measure ready，current.json为verified-active。
- Web旧helper拒绝共享依赖构建器的无害可选dependencies字段，尚未发布。对源码及主机各自原版本局部适配，只保留informational metadata；source/tests/files/hash/锁/回滚不松，41项回归通过。原版本备份保留，未把有其他差异的helper整文件互相覆盖，根脏工作区改动未整包提交。
- Web第二次已安装后HTTPS验收卡住，查明调用定制Python3.11缺默认CA；用精确归属SIGINT触发原BaseException恢复，previous record摘要一致且stage释放。改用原系统/usr/bin/python3，保留TLS验证、不重建/改包；第三次事务14.585秒完成，612安装文件核验、255线上index/JS/CSS真实GET+SHA通过，record online_verified。安装无整次构建deadline，原30秒单次网络传输timeout保留。失败日志/安全中断/TLS诊断均包外保留。
- 真实ziyue认证GET与生产页面详情均确认卢俊义三技能installationVerified=true、RUNTIME_READY、reasonCode=null，页面“已核验安装、运行就绪”，截图lujunyi-ready.png。仅只读验收，未调用模型或提交任务；不称真实技能E2E通过。API实体JAR SHA与发布前一致。

原批测试/构建/打包含新增必要工具与宿主回归累计**808.894/900秒**，未重置。安装、备份、启动及业务验收不计该预算；完整原任务墙钟未知，00:14:34接续观测墙钟在current-status单列。无重复Web/Runtime全量构建。

证据根`/home/isp/state/cyf-local-build/tasks/cyf-native-readiness-20261108/`：`deployment/final-release-verification.json`、`web-install-result.json`、`web-python-tls-diagnostic.json`、`lujunyi-profile-readback.json`、`lujunyi-ui-acceptance.json`、`browser/lujunyi-ready.png`及runtime/install/installation.json、native-provider-installation.json；当前状态见evidence/current-status.json。自有浏览器和短socket临时目录收尾；不删除共享依赖、他人任务、日志、状态或备份。最终包按现有mark-complete登记，真实结果由deployment/artifact-retention-final.json记录，未执行clean。
