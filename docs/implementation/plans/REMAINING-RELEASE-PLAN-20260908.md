# 未发布 / 未启用 / 待验收执行计划

核对时点：2026-09-08 22:40 CST 附近。此文是按需更新的计划/证据投影，不是第二执行台账；未派发新实现任务、未改变生产开关。唯一认领位置仍为 `docs/implementation/TASKS.yaml#runtime_ledger_json`。

## 最新执行结果（以主机回执时间为准）

### 主机记录2026-09-10：R03剩余五项真实PASS，技术验证闭环

- warm5 session35773 完成：agent MySQL Schema 五个指定方法实际执行，1XML/5distinct/5PASS，原生0、SQL用户schema清场0、ECHILD/资源交回成立；独立终态审查接受33/33 refs，receipt `362e748d…edc539e`。
- 仅能汇总为旧Rent9+新Agent5的跨运行14方法覆盖，不能写成同次14PASS或真实业务验收；历史R7 SQL清场UNKNOWN不回填。R03技术验证已接受，W04剩余受控认证的创建/取消/退款/Web读回业务验收。

### 主机记录2026-09-10：租金9方法已分批覆盖，剩余agent5包进入短差额独审

- correctedR8原session98544已终态：租金修复方法真实1PASS，agent5未执行；wrapper124，SQLzero UNKNOWN，ECHILD/handback true。旧8加新1仅为跨运行RentSchema9方法覆盖，不是同次14PASS或真实租金业务验收。
- 两个test label修复已实际推送API origin/develop `903c24edb69ebbd2b126fa3cb620e47114bf30e9`，仅test差额，不触发重复生产发布；热验证worktree仍85b41/cb693 clean。
- 剩余5包PREP `2134a402abdde853e1e02e7c653f24ba00a7b4f58d1e02f1a5ac8b3fc6619ced` 的26refs已由Main独核；原Sol恢复审cache复制/强制实际test/5selectors/1XML差额，Knuth确认尚未RUN且可接整窗。此前停顿是交接等待，不是旧R8仍运行。
- 主机记录02:31原Sol工具差额SOURCE ACCEPT并已释放；Main fresh准入通过，已给原Owner一次完整执行窗口GO，待实际启动/原生终态，不逐阶段请示；真实native/5项计数/SQL清场/ECHILD/handback到齐才收口。保留failure1和历史UNKNOWN，不自动重试。其余真实业务、语音/身份授权、邮件及原生范围不变。

### 主机记录2026-09-10：8项实测通过，测试标签修复已提交，6项补验流程实际启动

- R7原session74221 native1，真实租金9项8PASS/1FAIL/0SKIP，agent5未执行；Main核原XML与27refs。AS1536运行已越过原bootstrap问题。失败是测试label超既有16字符限制，非业务断言失败；旧SQL零残留查询未到达，UNKNOWN保留。
- 两label已本地提交85b41cbf/treecb693cb9，独立Sol SOURCE ACCEPT；只改test值，不改生产、断言或fixture安全规则，尚未push。其余8方法/sharedfixture/生产blob不变，独审允许方法级复用。
- 新6包（原失败租金1+agent5）曾因runtime命名与原保留确认入口不一致被P2拒绝；Main按矩阵登记后授权仅plan路径/pins补正，实际29refs与精确guard已独核，原拒绝保留。新6通过后只可汇总旧8+新6，不能称同次14全套PASS。
- 磁盘一度1492381696bytes，原Owner按Main核准精确名单仅删除5个已终态可再生data，实际净回收707371008bytes，外置日志/receipt/最新R7及历史UNKNOWN data保留。未清理foreign或生产，旧SQL UNKNOWN不变。
- corrected R8整窗GO后Main精确argv核orchestrator4169785/startticks3054710375及controller4169808/startticks3054710481确实在运行；不是只派发，尚无新6结果。全局Gradle串行、AS1536及原其他资源/清理/时限不变，无生产/Provider/SMTP操作。
- 真实经济/租金/六技能业务、客户端ACK、语音音频/计费授权、邮件服务商认证、原生宿主与M4/M5范围继续保留。没有新永久邮件监听，也没有把当前测试进展标作整体交付。

### 2026-09-09 23:57 实测定位测试进程AS近限，进入单因素整改

观察型full14 R6在23:49:38 native1结束，bootstrap前初始化通过，但14方法仍未开始；原ECHILD/资源交回成立。Main核终态b81ef45a全部22refs及原样本：bootstrap VmSize1175668KiB / AS1179648KiB，只剩3980KiB，RSS126036KiB。强支持隔离进程地址空间限额压力，不证明整机物理内存不足或唯一分配失败原因。原371行观测/11bootstrap样本保留，SQL内部空档UNKNOWN。

已先登记第二失败并停止，再依据矩阵§72明确授权原Knuth单因素SOURCE/PREP：隔离AS候选1152→1536MiB，严格同步observer实际限额断言；其他资源/SQL/14测试/清理/期限均不变。未授权新运行，待独审与fresh准入；旧失败不回写。这是测试环境整改，不是新业务功能已交付；原真实业务、语音/邮件授权及原生范围继续未闭环。

### 2026-09-09 23:18 合批验证在数据库启动失败，已转最小归因

full14 原 session68344 于23:06:29 native1结束：初始化native0，private bootstrap native2，日志出现bad_alloc/signal6和线程errno11。Gradle未启动、14方法及2XML均未产生，不是14项业务断言失败。Main核终态b12751c4全部20refs，原ECHILD/资源交回成立。实际失败时AS/NPROC/cgroup用量缺失，具体资源根因仍UNKNOWN；禁止盲重跑。

原Knuth继续最小bootstrap资源归因/复用现有数字采样的SOURCE差额，未授权再启动实例或放宽限制。W04共享本次缺口，不另起重复验证。API f1426已实际发布、Web生产输入无新增差额的既有证据保留，不因隔离验证失败重复发布。真实用户ACK、钱包/租金与六技能业务验收、语音计费授权、SMTP服务商授权、原生宿主/M4/M5仍未完成。

### 2026-09-09 22:42 隔离初始化通过，合批补真实MySQL缺口

C实际session67365/init/controller均native0，22:31:43 bootstrap完成，原ECHILD及资源交回成立；Main核18refs，初始化约53秒。旧超时/UNKNOWN保持，不能归因为600秒上限调整带来成功。真正SQL测试仍未执行。

下一包复用原已审隔离认证/SQL/清理流程，仅适配已接受AS/有界时间和新namespace。主控将同夹具、源码与线上一致且缺实证的W04 FundingSchema5与R03 RentSchema9合并为14项，避免第二次建库/编译；当前SOURCE/PREP，独审及实际执行结果尚待，非14PASS。不触碰生产库，也不重新发布已上线f1426。

### 2026-09-09 21:55 新API已发布并恢复监控

- f1426/e02f（租金续租修复）21:34:59实际COMMITTED/native0，21:39:01监控交回；Main21:55核38引用及线上JAR全文ff801061、PID4020259/ticks3053278071和当前healthy21。不是仅构建或派发；R01/W14进入待真实业务验收，不重发相同版本。
- 原Owner Knuth已按条件式GO交接R03，继续已独审AS1152MiB单因素init-only诊断；尚无B通过/MySQL9通过声明。不让下一任务再空等逐阶段批示。
- 客户端新发布启动期实际5pending_ack/3ack_timeout、尚无registered；服务未重启。原Turing并行只读归因关联/重试，不能把启动期现象直接判定持续业务失败。
- Web远端仍e346，只有既已核测试差额，无新的生产输入需要重发。真实经济/技能安装/租金业务与语音、原生依赖仍未完成；SMTP AUTH526未解决，本次未发邮件。

### 2026-09-09 18:51 实际合并发布完成，邮件认证失败单独处理

- **API97ae8/9ffcf已实际部署**：18:23:21 COMMITTED/native0，JAR587a2ffd…，新PID3910271/startticks3052131872；18:28:16 monitor交回，18:31普通监控正常。Main18:47核25项终态引用、实际liveJAR全文摘要和当前PID/ticks，非仅运行记录自述。新包包含全部经济6267和SSE修复，不需再发布第二遍。
- **通知异常**：唯一97ae8完成邮件AUTH526/SMTPAuthenticationError/native1，未观测DATA接受，收件箱未知。已新增独立OPS-ALERT-MAIL-AUTH526-20260909由原Knuth只读归因，不盲重试/改密码，不把邮件失败变成部署失败。
- **租金19方法已实际启动**：18:48原Shannon执行最终R01rev2原命令，Main18:50确认orchestrator3932690/原runner3932719存活。仍待真实15租金+4catalog/XML和native终态，不是已PASS；MySQL9初始化问题仍独立保留。
- **当前客户端实际观察**：PID3657704、10:30:47启动、NRestarts0；10:31记录3条registered-stage，但无法绑定具体profile。18:23:21–18:51发布后窗口未见registration-stage事件，不能把旧3条ACK算新版本后完整业务验收，也不能凭无日志判客户端失败；不重启制造证据。
- 用户可登录聚义厅发送一条密议验证真实回复。语音真实调用及可能计费授权、受控经济/六技能/租金业务与M4/M5/原生宿主范围仍未完成；源码、实际发布、开关启用与业务验收继续分开。

### 2026-09-09 18:03 合并为一次实际发布，旧维护窗口已交回

- 6267 reserve session53518 rc1/STOP，未启停/部署API、未创建新预算；随后确有state CAS漂移，但原日志未定位具体拒绝行，不把它写成唯一确定根因。旧失败保留；17:54原Owner已实际resume，maintenance=false、incident/inflight=null、attempts0，Main独核handback634f及两个内层引用。
- SSE97ae8/9ffcf现已实际module32PASS、bootJar/verify/bridge native0。Main核26发布引用、9XML/32distinct/duplicate0及原JAR587a（220127372bytes、root0444/nlink1）/metadataa10f/inputaa0959；97ae8包含全部6267，仅新增3条OAuth路径。**决定只发布97ae8一次，不再先发6267再重启。** 尚无新runtime GO或部署完成。
- 原Reviewer已全文接受same-call协调函数及97ae8 controller六常量绑定；仅待原Owner交97ae8函数机械重绑与调用层失败退出实际差额，不重build、不改SSE原input/metadata、不绕CAS或重置三次恢复预算。
- W10四个关键已安装模块实际位于current指向的20260909102948 release，与isp-install a100a500逐字节一致，已修正“未部署”陈旧描述；不是全制品清单/运行代际/六技能真实安装验收完成。
- Web生产输入无新增差额；租金19真实Java方法仍待运行、MySQL初始化资源归因仍独立未闭环；语音/业务受控身份及可能计费授权、M4/M5和原生仓库范围不变。

### 2026-09-09 17:22 实际交付与待发布

- **API构建已通过**：6267/936d，原build native0（Gradle33分53秒、193项实际执行）及verify native0；JAR 220127346 bytes／SHA8ace2e3d。不是仍在编译。
- **发布组包已通过**：原Knuth单次assembly/现行verify均native0，Main已逐项独核原→新派生链；使用现行63a控制器、新inputa729，不改旧build证据、不重新构建。尚未切换生产；最后运行命令与fresh monitor/预算/精确JAR准入由原Owner准备，6267不等待未就绪SSE。
- **Web测试修复已交付develop e346/571b**：独立3case全部PASS、stderr0，Mainfresh远端确认。相对已部署223981仅两个测试文件差异，生产差额0，不重复发布。真实钱包/技能用户验收仍未闭环。
- **租金/种子19方法运行包已独审通过**：task重新绑定R01、内外摘要一致，Java尚未运行；R03 MySQL初始化失败仍独立保留，具体资源原因UNKNOWN。
- 16:53一次本机health读取超时，17:03追加观测HTTP200/UP；既有监控16:56五项healthy且无incident/inflight，不能把这些历史快照当后续部署准入。未做手动重启。
- 语音受控身份/真实音频与可能计费授权、真实六包安装ACK/结果及业务验收、M4/M5和原生宿主等范围仍未完成，不能整体归档。

### 2026-09-09 16:36 构建实际运行与复审收口

- API6267构建已实际启动：Main16:22/16:30核原orchestrator PID3831311存活，非仅GO。新制品/发布尚无终态；Shannon负责原运行，Knuth复用现行63a运行控制器做最小发布输入准备，不双重构建/不重启API。
- Web两处测试清理缺口已修为e3464a6/571b0a3，原独立Reviewer SOURCE ACCEPT。新三case runner已核，尚未运行，待当前heavy自然结束；仅测试差额，不需要重发已相同的Web制品。
- R03旧MySQL验证占位和Web已结束PREP占位已释放，不关闭/重启任何Agent或OS进程；资源初始化原因仍待精确归因。
- W13只读核36方法覆盖和真实V0验收缺口；W14已纠正过期“Web还未合入”描述，整体preview仍未完成。

### 2026-09-09 16:17 最新推进（覆盖下方历史快照）

- 经济36个精确Java方法实际全部PASS；5个owned源码路径已推API develop6267f3b1/tree936d6e4b，保留原租金及其他路径。Main已给一次bootJar构建GO，尚待实际运行/终态；合分支不等于已发布。
- 租金R3隔离MySQL在16:05:47初始化创建线程失败，九方法未启动；ECHILD/资源交還已证。确切资源限制原因未知，已停止重试并交原Owner只读归因。此故障不阻断已测API构建。额外H2/catalog19方法仍未证。
- Web新fixture候选c527ad6f/d47e6423已提交并交独立只读审查；原七文件110PASS和ee100test-only合develop保留，新候选尚未验证/发布。
- 语音、六技能实际安装与ACK/结果、完整受控交易验收、M4/M5和原生宿主范围仍未闭环。

### 2026-09-09 15:38 最新异常及实际执行

- 经济36个精确方法（关键7与历史失败30去重）已获一次GO并实际由orchestrator持锁执行；Main核exact holder PID3799699绑定本次包。尚无终态，不能写36PASS。
- Web独立R6诊断出现2PASS/1FAIL（第三case等待名册刷新谓词）；下一HTTP trace到60秒native124仍无阶段日志，已按第二连续失败停止，不盲重跑。原七文件110PASS及test-only ee100已合develop事实分别保留；不能据此声称Web业务无缺陷。仅准备最早期阶段标记，下一运行等经济heavy终态及明确授权。
- 租金MySQL包第二次独审仍缺未记录脱组后代终态证明；原Owner正改task-local subreaper并做有界真实轻量子进程负例，设计已独立认可。未初始化MySQL、未做生产操作，不影响经济实际验证或其他独立源码整改。

### 2026-09-09 15:17 新验证与提交交付

- Web原卡顿单case1PASS；钱包/悬赏/技能七文件110PASS、0FAIL/0PENDING，当前树0f6be357。213byte Vue warning保留并做一次定向可观测诊断，不当成无BUG。测试fixture修复已nonforce推develop ee100528，同一已测树；生产输入无差额，未因此重发Web。
- 经济上一轮真实6方法5PASS1FAIL，定位SKILL requestId错误；新61f4192/4f2193的DB+wire修复已独立源码ACCEPT，正在准备一次合并相关历史失败的H2定向验证，未运行/未合develop，完整交易闭环未完成。
- 租金已通过Web37、fixture4、reprovision5均复用。独立MySQL9运行包只读审查发现wrapper退出不等于全部Java后代终态，原Owner正有界修复清理判定；无MySQL实例初始化/运行，真实租金业务范围保留。
- 语音合法受控身份、真实音频及可能计费调用授权、六技能实际安装与ACK/结果、M4/M5和原生宿主等范围继续保留，不由上述局部PASS替代。

### 2026-09-09 14:24 主控交接恢复

- 租金reprovision5实际已10:43:02全部通过，Main此前未消费回包导致台账仍写验证中；现已独核9refs/真实XML并补记，不重跑。MySQL9及完整业务仍未完成。
- 经济51d73源码独立审查早已ACCEPT，六方法PREP也已完成但空等Main GO；14:24恢复原Owner并发单次RUN GO，禁止将这段空档算成测试耗时。通过后允许已审test-only差额直接nonforce合develop，避免重复等确认；失败按规则停止归因。
- 尚无可用automation工具/新后台定时器，不声称永续监听已修复。

### 2026-09-09 10:19 实际结果

- W09 R6真实运行24分44秒，4方法1PASS3FAIL：已越过旧阶段早停，当前修复报价H2会话/约束与技能建表适配，不是全业务通过。
- R03真实Java fixture4全部PASS；排队18分27秒，运行17分钟。02171已完成独立整合并推送develop6ad7f162，整个tree与已测候选相同；Main已fresh核远端。test-only不重启API。
- 原Shannon继续经济最小源码修复，原Knuth继续租金整合/后续5方法准备。真实租金8、MySQL9、技能安装链、语音授权及M4/M5仍保留未完成。

### 2026-09-09 09:11 接续（覆盖下列陈旧阻断描述）

- 用户授权关闭的10个旧Agent占位已实际释放；当前只恢复原Shannon/Knuth继续经济与租金，不再以线程容量等待。
- W09已正式授权运行包整改并派发：新R6把T5/T10缺阶段日志改为一次告警，保留45分钟总上限与真实四方法检查；准备差额独立审查后才能执行。本条不是测试已启动/已通过。
- R03已派发：非强制推送已审02171测试修复到自身候选分支，并并行准备新四方法验证包；不为test-only代码重启生产API。真实租金与MySQL范围未完成。
- Web已交付223981，语音仍等待受控身份/真实音频/可能计费授权；其他经济/技能及M4/M5范围不变。唯一状态以TASKS运行台账为准。

以下为早前结果与保留历史：

- **A1 Web已交付**：97cc912（与远端77666e8生产输入一致），主机00:49原子发布、00:50公网6/6严格TLS/字节核对；Mocha180PASS+原生缺仓2pending、onboarding23PASS、发布器3fixturePASS。恢复ECOUI=true，voice=false；未知来源旧live完整备份，API未重启。完成邮件SMTP接受，不能保证收件箱到达。
- **A2客户端观察部分闭环**：至少一条关联ACK已证实；全profile/真实技能安装结果未验收，不重启凑证明。
- **B2/B3经济继续推进**：R1 settings插件解析、R2 init参数类型均在业务测试前失败，均0XML；R3只修实际Gradle签名对应的String参数，主机01:16启动一次4方法诊断，约01:46以124/1806秒超时，0XML/未进入业务测试；01:50台账已blocked_root_cause并停止重试，转只读归因；修正路径R4于03:00:55实际启动，305秒根工程配置入场门限未通过（native94/0XML），--info进一步显示尚停在included插件jar开始处，没有jar完成或API主项目配置开始的证明；缓存插件整JAR等价已核实；R5已单次执行并307秒rc94终止，最终日志含96项目完成配置，但监控未看到阶段标记，仍0XML。台账已第二次blocked_root_cause并释放Owner，无R6。标记计时基点与wrapper不同，误超时/缓冲归因尚不能确认。当前还受任务派发不可用及新Agent线程上限阻断，整改未重新派发。保留原117PASS/32FAIL；不把环境失败当成业务用例再次失败。
- **B1语音只读配置核验已完成**：实际JAR已有加密共享Provider key/base，不要求重复提供密钥；网关能力、解密与精确allowlist仍未验证，独立安全key缺于已知启用输入。已接受HOST common-fallback尚未进入当前部署器；b6088349已推源码分支并于主机02:58完成install-only/monitor trust同步，仍同代API UP、无重启；新事件完成邮件03:13 DATA250/拒收0。独立安全输入只在私有stage，语音未启用；当前waiting_user，需合法受控登录身份、真实音频及可能计费调用授权，Knuth已转租金只读验收准备。M4/M5/原生仓库等未因A1发布自动完成。
- **防回退修复已完成**：WEB-PRODUCTION-FLAGS-P1（223981d）已nonforce推至develop，production默认ECO=true、voice=false；2/2回归及默认Mocha收集PASS，一次实际build native0。410/410文件与live全量相同，未重复部署；02:04已登记done并释放Owner。
- **租金前端定向验证已通过（主机03:35）**：当前Web223981/f1ab两文件实际37 PASS、0失败/跳过，单次33.968秒、源码不变。原22项静态计数遗漏循环生成15项，已据原生日志纠正，没有重跑。这里只闭环Web mock/UI覆盖，8项真实业务、MySQL9方法及退款/租约链仍待验收；原Owner已并行提交fixture修复02171a78/a5cd2ebe（仅两test路径），主控独立源码审查接受，四项离线验证待执行；尚未push，不涉及生产代码发布。
- 详细证据和各阶段历史保留于 `/home/isp/wsps/cyf/docs/implementation/handoffs/REMAINING-RELEASE-EXECUTION-20260909.md`。下面00:10及22:40内容是历史快照，不是当前Owner/gate。

## 执行补记（2026-09-09 00:10 CST）

用户已批准落实本计划；以下是本轮执行投影，覆盖下文9月8日22:40静态快照中的陈旧基线，不替代唯一运行台账。尚未完成的开发/启用不因派发变成已交付。

- **API已前进，不重建旧包**：`00681408c4592f1f76eda8eafa554a9191fb0e50` / tree `e15196b94ae289ac85b7210143c5531f5b4f10a5`，JAR `cb4284700ebcc344614696063de7ac9f5ad664b4e909ad08d7c4a94b698f3404`；9月8日23:29:26 COMMITTED，登录HTTPS 3/3 PASS，23:33监控已交还。依据 `../handoffs/JY-LOGIN-HTTPS-20260908.md`。本轮不重启API。
- **Web差额由5个增至6个提交**：新增 `97cc912 fix(ci): reduce signed dependency bootstrap downloads`；当前候选完整SHA `97cc91296ad7e4749f4aa953318af64affdb64bb` / tree `44714c632a5a67f5c16912552490f04e04a724ae`。最后证实线上仍d59b97a、index `6fd01731e31b406f3e0adddbeec3d669f71392c8312675d61f0c3788e5d88435`。不声称远端CI通过；构建前仍需fresh核验。
- **A1已认领**：复用Knuth `01a0763d-3a60-7782-9ad5-898e24525d88`，任务 `REMAINING-WEB-RELEASE-20260908`。仅独立worktree的定向测试/构建/原子发布准备，产品源码不改；主工作区脏，默认脚本硬编码该目录，因此不得在其中pull/install/build。voice=false、ECO UI=true，API不动。主控非作者审新增运行源码，CI/offline工具不作为已验证线上功能。
- **A2有一项真实进展**：9月8日23:48–23:53只读观察证实新API启动窗口23:28:59的一条关联registered ACK；Client PID2990525、NRestarts0。不是全profiles成功，也不是native终态后的新注册证明。原客户端观察Owner已释放给A1；后续技能安装需精确测试Agent ACK与结果。共享回执 `../handoffs/REMAINING-RELEASE-EXECUTION-20260909.md`。
- **B2/B3经济诊断已认领并完成初诊**：复用 `ECO-V0-W09`，新Shannon `01a081b6-4584-7201-a94d-345a29720806`，独立worktree `/home/isp/wsps/cyf/.worktrees/eco-delivery-resume-20260908`，base006814。旧32失败拆为7报价、12受报价创建阻断的结算、13技能fixture。当前源码已经包含报价cause诊断和技能SQL/审计trigger修复，先运行4个精确方法诊断，不重复实现已有修复、不重跑149 suite。当前仅授权执行包准备，尚未运行Gradle。
- **实际资源顺序**：Web重型build优先，结束即让经济4方法通过orchestrator运行，不必等公网发布收口；独立源码/轻量准备继续并行。生产迁移、真实收费、付费语音未授权。
- **语音与外部边界**：确切root voice env文件不存在；其他SpringAI/common来源未知，不能声称所有Provider配置缺失。语音本轮未启用，后续仅让精确配置Owner输出批准来源存在性/可用性的布尔证明，不输出密钥。原生仓库/真机仍是外部依赖。
- **跟进机制实况**：当前主控active goal及已派发子Agent有界等待；没有成功创建新的后台定时器，也没有发送本轮新邮件。仅在结果变化、异常或用户需动作时通知。

---

## 1. 当前基线与结论

- API：已发布 `abe17424b4ee3963bd40d94edc262c517d7ea92c`，JAR SHA256 `4195a9c1de3a2735688ce0030b53ff9d4a8e2c785e03039ef837fa8cfefe90ff`；22:03:52 COMMITTED，22:07 健康 UP、公网鉴权边界正常，监控已交还。此次独立 `ls-remote` 确认 origin/develop 仍为该提交。
- Web：最后已证实上线基线 `d59b97a5b2e75c4b700a09ecc4a310b3e69e8705`。本次直接读取部署目录 index SHA256 `6fd01731e31b406f3e0adddbeec3d669f71392c8312675d61f0c3788e5d88435`，匹配该发布回执；入口 `/static/index-Eo-IchkV.js`。
- Web origin/develop 新推进至 `4a9f421a6bc1953e8fb18ef891be040003ff23dd`。仅 fetch 对象用于审计，没有 checkout、改分支或构建。相对上述线上基线新增5个提交，尚未建立它们的部署证明。index 核对不是对全部线上文件的重验，不排除需进一步归因的局部变更。
- 本次 ancestry 检查：PWA hosted/ACL、Web preflight/onboarding、ECO W03–W09/W11/W12/R01/R02、语音 API/Web 集成提交均在各自上述已部署源码基线的祖先链中。此证明只说明代码已集成，不证明没有后续修改、生产启用或业务成功。
- 因此：不能按9月6日静态清单中的“NOT_DEPLOYED”批量重发旧包，也不能把运行台账的 accepted 当作尚未合并。其旧失败证据仍保留，使用实际版本和功能开关另行核验。

## 2. 真正的前端发布差额

| 提交 | 用户可见内容 / 工程配套 | 当前口径 |
|---|---|---|
| `10d645e` | 避让微信小程序关闭按钮 | 已提交远端，未证实上线 |
| `d82b152` | 阅读器在原生及旋转布局中预留胶囊安全区 | 已提交远端，未证实上线 |
| `fe670bf` | 按横屏/竖屏提供不同新手引导 | 已提交远端，未证实上线 |
| `fce21d2` | 公共入口表达、保留小程序访问上下文 | 已提交远端，未证实上线 |
| `4a9f421` | Flow/CI 可复现性与相关测试、证据工具调整 | 工程配套，不能仅按标题认定全部验证通过 |

最先执行：定位这批提交的现有精确 Owner、独立审查及CI结果；若台账缺项，由控制面补唯一task_id，而非另起重复Writer。核对最新远端/线上版本后，只发布确实未上线的差额。独立review仅审新增差异，复用已接受树的有效证明。Web一次构建、一次原子发布、公网index与引用资产验证；不重启API。若4a9不是单纯小修，按实际完整diff验证，不用“CI修复”标题豁免。

## 3. 用户功能剩余范围

| 功能包 | 准确状态 | 下一交付物 / 完成条件 |
|---|---|---|
| 语音输入 / 语音会话 | 代码已集成；最后已证实Web构建voice=false，生产Provider与启用未完成 | 核对实际API开关、现有安全配置和当前HOST适配；经授权进行最小真实STT/TTS验证；API先启用成功，再从当前Web源码构建启用版；录音、识别、发送、播放/取消及错误降级有真实结果 |
| 银两钱包、悬赏托管、报价/结算/退款 | API/Web代码已经合入发布源码，Web ECO UI=true；可用交易闭环未验收，不能宣布收费开放 | 先确认实际schema/后端配置；基于现有失败矩阵修复并验证充值预览、余额、明确报价/指定Agent、托管、结算/退款、幂等/隔离；只用预览测试银两，不自行开启真实收费 |
| 技能市场、购买、安装、激活与退款 | 市场及安装代码已集成，6技能种子/Java回归/安装结果业务链未闭环 | 核对6种技能包及配置、专用测试Agent；注册ACK→安装命令→包SHA验证→结果回报→激活/失败退款，一单一结果；admin-only技能不得放开普通用户 |
| 招贤令server托管租金、续租和失败补偿 | 租金代码已集成；R01/R02源码审查完成但验证记录未闭环 | 报价确认→扣费→安顿→租约→续租/补偿；local不收费、不补扣既有Agent。已有预览价每Agent 1,000 SILVER/30天，无需重新问价；真实收费不包含在本计划授权中 |
| 自动组队 / 自动拆解 / 调度 / 高级协作（M4） | 原规划E01–E08、F01/F02/F06无整体交付证据，仍属后续开发，不能靠一次构建发布完成 | 分三片：候选评分/组队/解释UI；工作项拆解/依赖/重派/自主级别/看板；Context Pack/成果存储hash/冲突与替代状态 |
| ACL知识检索与生产加固（M5） | F03–F05、G01–G08仍属规划，既有部分测试/告警不能等同整个里程碑完成 | 搜索服务与配置、任务级ACL索引、重建重试；补齐多Agent E2E、故障恢复、灰度、迁移手册、指标/安全/容量验收。复用已有运维和测试，不重新建设重复平台 |
| 原生小程序宿主方向/键盘等边界 | `JY-LAYOUT-NATIVE-20260906`等待宿主仓库；现有H5适配不能冒充原生宿主实现 | 提供原生仓库后核对真正剩余代码、实现并真机验收；新的H5胶囊避让提交优先独立发布，不一起等 |

### 不应误列为“尚未发布”的功能

1. **案卷阁列表/阅读入口、个人Agent名册、历史解绑修复、既有地图/横竖屏修复**：已发布的基线继续算已发布。后续典籍catalog/body/进度/书签/手札需真实登录验收，发现问题走BUG，不重复整个H06。
2. **客户端注册与可靠任务链**：客户端f6a2472安装和观察功能已交付；12:23–12:28历史注册ACK未成功不能当成22:30仍失败。新API部署依赖已满足，下一步一个有界只读关联ACK观察；失败才定位认证/响应/关联边界，不重启循环。任务领取/结果回报、Rabbit端到端未由健康UP证明。
3. **账号安全/全设备退出、公共公测安全与onboarding**：已发布源码中有revoke-all入口、Web退出所有设备，以及PWA隔离/ACL修复。缺的是生产迁移/会话撤销/双scope/真实onboarding验收和版本证据对齐；不是全部代码待开发或待部署。需先核验再仅补缺口，公测整体验收仍未完成。
4. **健康检查、告警邮件、已完成磁盘清理**：已有实际安装/运行/发送记录，不再列为新功能发布。SQLite剩余空闲页回收仍是运维跟进，按竞争状态有界处理，不能影响生产。
5. **性能优化/SLA**：目前完成的是诊断与目标建议，不是性能改造上线。request_id/upstream计时/RUM及按真实瓶颈修复另行实施；HTTP200不能证明典籍读取快。

## 4. 执行顺序与并行分工（计划角色，尚未新增认领）

| 顺序 | 执行线 / 建议角色 | 前置依赖 | 有界动作与验收 | 初始时间窗口 |
|---|---|---|---|---|
| A0 | 版本/控制面：主控 | 本计划 | 对齐新Web5提交Owner及源码→制品→发布关系；为旧台账仅补证据，不重启历史已完成任务 | 启动后0.5–1h |
| A1 | 快速Web发布：现有Web Owner；无Owner再由balanced_worker接手 | A0/当前差异review | 当前差额定向回归+一次build+一次发布，公共入口/胶囊/引导可用；允许真机问题独立BUG跟进 | 约2–4h；假设现有CI通过且无新阻断 |
| A2 | 已发布业务验收/客户端：现有客户端Owner+gpt_test_runner | API已满足；受控账号/真实用户触发 | 一次关联ACK观察；名册/典籍进度等受控读写；账号/公测双scope验收；每个结果记录实际版本、预期/实测，失败只开精确BUG | 先用1–2h建立结果矩阵；修复另估 |
| B1 | 语音：现有voice Owner+运行Owner | 现有HOST兼容；Provider权限/额度、真实调用授权 | API开关/Provider→真实音频→Web启用，从当前Web合入A1，不部署旧d30归档覆盖新改动 | 条件满足后4–8h；外部授权等待单列 |
| B2 | 钱包/悬赏：critical_worker，独立economy路径 | schema/配置核对；既有32失败矩阵 | 先2h归因真实SQL/fixture原因，修具体错误；资金守恒、幂等和越权验证；再预览启用 | 暂估12–24h；2h诊断后重估，非上线承诺 |
| B3 | 技能市场：客户端Owner+API/Web分路径 | A2 ACK、B2必要钱包能力 | 可并行做包/种子/API修复；安装闭环依赖ACK和结算能力，不人为等整个B2完工 | 暂估16–32h；与B2并行，不相加 |
| B4 | 托管租金：critical_worker+balanced_worker | B2账本、托管状态就绪 | 合同/界面准备并行；验证报价、租约、续租、明确失败补偿后启用预览 | 暂估8–16h自依赖就绪起；与B3可并行 |
| C1 | M4：architect冻结接口后分API/Web实施 | 当前可靠任务链实测；新任务登记 | 上述三片分别review/验证/发布；不把所有E/F串成一个大包 | 先2–4h拆包/校验复用范围，再报各片工期 |
| C2 | M5/性能：按检索与运维路径拆分 | F02/ACL合同；受控隔离环境 | 计时/可观测性可早并行；索引与ACL先实现再预发验证，生产不做未授权压测 | 首个观测切片4–8h；全部M5待拆包后估 |
| D | 原生小程序：宿主Owner | 原生仓库/真机可用 | 先判断H5修复后仍有哪些宿主缺口，再实现 | 仓库到位后1–2h诊断，完整工期再估 |

时间口径：均为大模型连续执行的**自然经过时间**，不是人天，也不是各Agent工时之和；未启动前不换算为承诺日期。首次估算使用当前主机实测参考：R6定向context约13分钟、bootJar约12分钟、一次部署至终态约16分钟；包含差异审查和可能的一轮有界修复，但未知根因可能扩大范围。上述参考不保证每轮同速。原经济计划106工程小时/45–55小时关键路径及9月8日预览日期是旧估计，不能作为已交付事实，也不适合机械扣减计算剩余时间。

## 5. 效率与发布约束

- 独立任务/worktree/路径可并行Writer，不恢复“全局唯一源码Writer”。ECO公共账本同文件由一个实现Owner维护，其他任务使用冻结接口，不并发改同一文件。
- 每项一个实现Owner，独立sol_reviewer只审新增差异；现有源码/测试证据按tree+selector+fixture复用。Gradle统一走orchestrator和 `/tmp/cyf-gradle.lock` 串行；共享DB/Rabbit/重型磁盘按真实资源隔离，不用全局源码排队代替资源治理。
- 生产API生命周期仍由精确运行Owner协调串行，Web-only发布不重启API。每个已ready包独立晋级，不等语音/资金/M4全部一起发布。
- 新部署前重新核验当前远端/线上SHA。后端今晚已同步develop，不能为“追最新”重建不变的abe174；Web确有新差额才发布。
- 首次失败先归因；第二次连续失败停止盲试，输出最小修复。原API事故三次失败预算和告警规则保持，不跨任务杀进程/重置计数。
- 不因本计划自动启用真实扣费、调用付费语音、执行生产迁移或篡改已提交数据库修复。用受控测试账号，禁止借用Token/伪造JWT。外部条件等待与Agent执行耗时分列。
- 通知只在提交/发布完成、异常、需要用户动作时发送；清楚区分“源码已合入/制品已部署/开关已启用/业务已验收”，不靠反复状态汇报冒充推进。

## 6. 范围外但必须保留的后续规划

经济V1/完整生产方案仍明确延后：Provider Egress Broker与KMS、绑定轮转/PoP、能力租约与完整隔离证明、UNKNOWN自动核账、历史资金任务迁移、第三方卖家及完整生产安全验收。不能把本轮V0预览交付等同这些完成；将来单独立项。账号注销/自助闭环属于下一阶段SDD建议，非本轮全设备退出功能的隐含上线承诺。

## 7. 依据

- `docs/implementation/TASKS.yaml#runtime_ledger_json`：本次117项快照；部分旧项文案陈旧，以上述部署证据优先。
- `docs/implementation/handoffs/JY-API-RELEASE-20260908.md`、`DELIVERY-RESUME-20260908.md`：新API实际发布/监控/邮件记录。
- `docs/implementation/handoffs/JY-ROSTER-UNBIND-ARCHIVE-20260908.md`：Web d59基线及index指纹。
- 本次API/Web `ls-remote`、新Web5提交Git log及本机已部署index摘要。
- `specs/INDEX.md`、各feature `delivery-status.md`、`docs/implementation/SDD_STATUS_20260906.md`：仅作为原始范围/历史快照，不冒充9月8日最终状态。
- `specs/agent-economy-marketplace/v0-plan.md`、`v0-hosting-rent.md`：V0/租金/后续V1边界。
- `docs/implementation/MASTER_PLAN.md`：M4/M5任务范围；历史F03–F05里程碑标签差异不改task_id/依赖。

## 8. 本次文档复核

2026-09-08，独立sol_reviewer `01a08041-ba33-7451-942b-b3dd2ea49eb1` 对本计划执行只读审查：ACCEPT（文档计划gate），无P0/P1阻断。确认版本/启用/业务边界、剩余范围、条件估时和生产/付费授权边界；建议从A0确认新增Web五提交的Owner/审查/CI开始。此结论不授予部署权限，不是实现或业务验收PASS。本Main本地引用存在性与文档diff检查通过，未运行构建/测试/生产动作。


## 2026-09-09 19:25 执行补充（不是新完成声明）

- API97ae8实际18:23发布、18:28监控交回保持；develop1911 TOKEN-TTL三路径差额尚未部署/应用生产SQL。
- R01实际19方法16PASS/3FAIL后已形成clean修复f1426d9b/e02f39ce，原独立Reviewer已恢复并接审；原包不盲重跑。
- R03诊断执行器已实际交付，仅离线9项通过，待该Reviewer顺序审查再由原运行Owner一次init-only；不是MySQL9业务通过。
- W08 catalog4已有实测，另config3+seeder2待验；W04 Spring账本4待验，均可新包定向补缺口，保留真实安装/业务/生产种子授权边界。
- 邮件AUTH526仍等待服务商/邮箱管理员查因，客户端新版本业务ACK、语音与真实收费授权及原生范围仍未完成。


### 2026-09-09 20:06 实测推进补充

R01修复f1426已独审且fresh12真实全PASS（R01三/W04四/W08五，session51648 native0/860s）；Main核25refs与4原始XML。W08缺失Java验证已补齐，转待真实seed/安装/业务验收；W04仍留真实MySQL范围。已授权原Knuthfresh FF-only推develop和一次bootJar，不重复已通过测试、不等待R03；20:04远端仍1911，尚不宣称推送/新发布完成。R03诊断native丢失实际失败保留，当前资源静默单独证实，A有界wait修复与B仅AS1152MiB候选已独审，尚未执行B。


### 2026-09-09 20:58 实际制品就绪

新f1426已真实推develop，37m47一次bootJar及独立verify-release均native0，JARff801061（220129640bytes）/metadata2dbf22c7；Main19refs和制品自带64checks核准，未重复业务12。R01转awaiting_release，原Knuth已接新W14 pin-only发布准备；仍未切换生产，旧97ae8保持最后已核上线版本。TOKEN-TTL SQL应用、真实语音/技能/钱包业务与原生依赖未因此完成。
