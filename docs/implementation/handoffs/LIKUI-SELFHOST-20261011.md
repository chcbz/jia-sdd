# 李逵自家接应 — LIKUI-SELFHOST-20261011

## 范围与Owner（2026-10-11）
- 唯一Owner：Main。本轮是用户指定李逵、提供SSH私钥并确认IP 173.230.149.118后的目标机安装接入与正常业务验收。
- 只操作李逵和该主机对应服务。不动吴用/林冲/公孙胜/卢俊义，不迁移历史事项，不增加托管租金，不复制其他角色模型密钥。
- 本轮先用既有 Runtime installation/enroll/API完成真实自家机器接入；前后端旧安装文书的产品缺口保留在 LOCAL-SELF-HOSTING-ANALYSIS-20261011.md，不能冒称页面向导也已修好。不为单角色接入新增认证表或旁路API。
- 源码不改：isp-install develop 5b902c1bcd3efced9720e015e3b8240d39ce0738 / tree7f6e8944e052071cadd0760fa38df07f2c38db58，Runtime1.0.2。原shell/制品installer在远端固定干净快照运行，记录真实Node/Python版本与制品摘要。
- API本地基线cf140272/tree136ebfbc，Web已被另轮发布到a3bceaf/1.14.9/Flow203（本机record online_verified）；本轮不发布/回退这两个组件。组件工作区干净，根仓脏改不覆盖。
- 证据目录 `/var/tmp/cyf-likui-selfhost-20261011-8qhccv`；私钥仅0600副本，不进入Git/子Agent/日志。

## 已确认事实
- 首次域名SSH因historical known_hosts与新IP/hostkey不同失败；用户确认173.230.149.118后使用任务独立known_hosts直连成功，保留全局旧记录。
- 目标hostname li159-118，isp UID1002，sudo授权可用。Rocky8.10/x86_64，Node22.22.2，Python3.6.8，Codex0.161.0。Python3.11.13-7.el8_10在现有AppStream可用（只查询）。
- 旧codex-ws-agent.service/root/PID2375295处于active；profiles对应jyt-jiafewnnv58ec2379c-likui，codexHome为旧服务目录下独立.codex-likui。尚未停止/迁移。
- 旧profile指定gpt-5.6-terra，李逵专用config.toml默认deepseek-v4-flash；不能将其继续作为本项目新Runtime默认。按项目路由使用gpt-6-luna（需真实调用核验，失败不静默回退），仅复用远端该李逵自有provider配置与凭据。

## 安装/切换边界
1. 正常用户会话核对boundToMe、scope与AgentId，复用local绑定入口，不重置所有权/历史状态。
2. 安装Python3.11独立OS包（不改系统python3默认）、原installer固定源码创建完整独立制品，不借宿主Python包、不删除其他批次。
3. 配置放/home/isp/conf/cyf-agent-runtime-v1，状态放/home/isp/state/cyf-agent-runtime-v1；李逵workspace和CodexHome独立，不使用/home/isp作为写工作区。生成密封manifest和私有enrollment secret，已有本人JWT只上传摘要创建installation，远端enroll保存独立授权。
4. 切换前备份目标旧配置/unit、记录PID/start与服务启用状态；核对仅李逵实例、在本机发布锁内温和停止旧服务，单实例启动统一Runtime，不双跑、不强杀。
5. 保留原代码与私有配置备份；如启动失败，在确认新进程停止后恢复原服务状态，不能用旧运行结果冒充新Runtime成功。
6. 正常验收：本人李逵在线/真实能力→连续两问→新普通事项执行/交付/验收。启动/心跳成功不等于业务闭环。

## 状态
- 目标机SSH成功；业务归属与安装前置继续核验。暂无开发/部署完成结论。

## 2026-10-11 22:19 +08:00：接入及文字业务验收完成（非全能力验收）
- 三仓实时远端develop已核：Web a3bceafb53b4bea2545ad3065af058c48400605e；API cf1402727466e1e51db0860200dc178eab2096c4；isp-install 5b902c1bcd3efced9720e015e3b8240d39ce0738。本轮未修改/发布这些组件源码。API实体JAR仍SHA333d525e2aa4a9cbde138ccb7507d1d55f264190d09332863a35f277624b8c57。
- 目标机通过现有AppStream安装Python3.11.13，系统python3仍3.6.8；rpm提示既有pip3不是软链，未覆盖/修理该文件。原installer使用Node22.22.2、显式/usr/bin/python3.11、隔离venv和固定PIP_INDEX_URL=https://pypi.org/simple/（实际传入URL无末尾斜杠），完整npm/Python依赖安装、stage/final closure validation均通过；没有Node版本门禁或借宿主包。远端原仓两个证书未跟踪文件未动，制品来自另外的固定Git archive快照。
- 真实用户catalog核对李逵boundToMe/canOperate、JWT scope；UI重整接应→自家接应POST200。installation以本人JWT创建PENDING，然后目标端enroll；明文一次性secret从未进入浏览器/本地日志，启用后已精确删除。
- installation `rti_dd441f1ea25d6f6c8dff50463906abf1`，host `selfhost-li159-118-935f9597`，subject `d43e3eeb4d4c8c668e29d5dadd177cb99443f417ef7b55a7ee2548e795a646ca`。最终本人GET返回ACTIVE，catalog李逵online/canOperate=true。
- 新release `/home/isp/apps/cyf-agent-runtime-v1/releases/likui-selfhost-20261011-5b902c1bcd3e`，3116常规文件，完整catalog SHA13c3885505a0aa747b90bcd7d928e251c6c6bd39af0ae967b571a29737f8f524。独立CodexHome只复制该远端李逵的auth/config，不搬其他账号HOME/会话，配置model/chatModel=gpt-6-luna，未开图片能力。
- 工作区使用李逵私有root和本机installer仓的独立bare副本（保留develop基线、删除origin），只是现有工作区管理器的受控工作基底，本轮不改源码、不fetch/push或执行开发任务；非通用任意仓开发验收。
- 在远端发布互斥下备份旧unit/env/profile；临时仅为旧目标服务设置无限温和停止等待与SendSIGKILL=no，systemctl stop确认旧PID退出，禁用旧服务，启用统一Runtime后撤掉临时停止drop-in。没有强杀、删除写锁或改他人进程。旧服务inactive/disabled/PID0；新`cyf-agent-runtime-v1@unified`以isp运行，PID3067228，active/enabled/NRestarts0。
- 配置 `/home/isp/conf/cyf-agent-runtime-v1/unified.host.json`；私有状态 `/home/isp/state/cyf-agent-runtime-v1/unified`。远端备份/安装日志/制品catalog `/home/isp/baks/likui-selfhost-20261011`。本轮不是同生产吴用合并进程：不同物理机各自一个统一Runtime。

### 真实业务证据
1. 密议conversation `1760458005674`，请求`db927721-736d-4cb3-b194-88a868c916b7`与`8a7615a6-aaa1-4903-b531-af23652db1e0`均COMPLETED，同一会话连续提问，第二轮正确回忆“青松1011”。第一轮没有遵循要求的中文固定措辞，内容偏差保留；不将它计为严格措辞通过。
2. 只新建非资金事项446，点将李逵并自动议事conversation `1760458005676`，返回三条要求的会议清单。正式成果50 UTF-8字节、SHA1987e9dc7de4021d125684372bff3c8de011c5f4f9700f0325c06b660e1aaf0c，已与实际文字重新计算匹配。
3. UI确认验收唯一POST200，operation `fin_9b06e0d4d53fcd087cef406753675477b08671b93a46ab88d8e6d911594061a7`：completed/TASK_COMPLETED，delivery accepted，task completed/version4。GET复核和刷新后列表显示已完成；重入原会话仍显示验收完成，不重复点将/创建/提交finalization。
4. 浏览器guard第一次拦截task create在本地、没有发到服务端；确认原操作后单次创建446。此为测试控制器配置遗漏，不是生产创建失败。随后两次DOM读取早于加载、一次在已进入议事时找正式成果按钮均未产生写请求，不当作业务缺陷。
5. 证据主入口 `/var/tmp/cyf-likui-selfhost-20261011-8qhccv/business-acceptance-final.json`；浏览器完整截图、请求元数据和脱敏业务回执在其`browser/`。独占浏览器已关闭，无承诺后台持续验证。

### 未完成范围与确定缺口
- **旧安装文书未修**：真实UI仍旧API-key/codex-ws-agent/失效脚本/Node>=20说明。本轮由授权操作者调用既有正式installation/enroll接口完成李逵，不是用户照页面教程即可自行接入的产品验收。
- **公网原生执行路由缺失**：生产Nginx `/home/isp/apps/nginx/conf/vhost/api.chaoyoufan.cn.conf`没有`/internal/agent/` location，实际远端173.230.149.118、UA=node对workspace-executions/commands的请求在access log为444，与远端UND_ERR_SOCKET对应。最初curl默认UA得到403属于单独的既有curl拦截，不能作为Runtime根因；换node UA后是连接断开。相同路径API loopback无凭据返回401，不能因此冒称有效Runtime原生执行已验证。
- 本轮**没有修改Nginx/防火墙、开放全部internal、透传伪身份或建立旁路SSH业务隧道**；文档/文件/技能/图片执行未通过验收。后续需冻结并补齐仅Runtime原生通道的网关路由，保留API既有installation/session/owner鉴权，再做真实文件流程；不是继续重试旧输入。
- runtime日志另有generation mismatch拒绝广播和MESSAGE_TYPE_REQUIRED；没有归因为李逵执行失败，不扩大修复到历史/无关广播。
- 总结：SSH与单主机统一Runtime接入、连续文字密议、正常非资金事项文字交付/验收完成；自助安装文书与远程原生能力仍有明确缺口。不能写成“自家接应全能力都已打通”。

## 2026-10-11 23:33 +08:00：用户授权补公网Runtime路由
- Owner Main，自然接续原任务；仅修改本机api.chaoyoufan.cn Nginx原生路由白名单，不放开整个internal、不改后端鉴权/数据库、不重装远端Runtime或改其他角色。
- API基线仍cf140272/tree136ebfbc；Web本地HEAD已到d8b703b9（其他任务），线上record仍a3bceaf/Flow203；本轮不回退/发布组件。根仓既有脏改保留。
- 候选与备份/验收证据固定在 /var/tmp/cyf-likui-gateway-20261011（生产备份另记），在原发布互斥下检查精确前值并替换配置，nginx -t后reload，失败恢复精确前值。
- 验收：白名单与后端allowed路径/方法一致；无凭据/伪凭据/普通用户/Origin/重复头不能取Runtime权限；李逵实际Node轮询200及新文件交付；446不重跑。图像未启用不计图片通过。

### 2026-10-11：公网网关补齐已部署；新事项448文件验收未通过
- 根仓develop配置源码commit `f6f34cd0673e1bafcb104ce69a512b8d182773d2`（本地提交，未push）：`ops/ci/aliyun-flow/host/nginx/` 两个配置片段及说明、定向测试。组件源码未改；实时API远端仍cf140272、Web远端仍a3bceaf，未发布其他任务本地Web d8b703b9。
- API vhost只追加一个include，精确8组原生路径/方法白名单；Authorization/X-Agent证明头/Origin不改写，不开启native CORS，不放开整个internal。既有 /agent、/ws、未知路径444及curl规则保留；不是用HTTP接口放宽backend身份。
- 生产在既有coordinator→API-release互斥下备份、固定候选、原子安装；2026-10-11 23:36:39 +08执行nginx -t PASS后reload。master PID6541未变，没有后端/Runtime重启，不强杀旧worker。Vhost SHA `006bda95d6698d0634cd278ba4f98fc7fde6f2091b4b4853046db64801835a01`；两个片段部署后逐字SHA回读匹配。
- 生产备份 `/home/isp/baks/likui-native-gateway-20261011`；完整批次 `/var/tmp/cyf-likui-gateway-20261011`，主回执 `acceptance-final.json`。
- 定向静态测试3项PASS（首次断言误匹配注释中的rewrite，修成指令行匹配后通过；非产品失败）。25个真实公网原生方法/路径携伪Runtime令牌均401。无凭据/旧API Key/普通有效用户JWT无Origin均401，带Origin的Runtime请求403，错误方法405，未知internal仍关闭连接；没有使用真实凭据执行破坏性反例。
- 实际来自173.230.149.118、UA=node的轮询在23:36:37仍444，23:36:40起200；验收时间窗保留147条实际native请求，全200。远端同一Runtime PID3067228/NRestarts0/active/enabled，旧服务inactive/PID0。API JAR仍SHA333d525e2aa4a9cbde138ccb7507d1d55f264190d09332863a35f277624b8c57。
- 只新建非资金事项448并点将李逵，conversation `1760458005697`，request `mmd-typed-request_e9719793595769df4d20a3504c80bcc109503b81`。要求真实交付三行中文UTF-8文本文件，但实际typed-outcome是CLARIFY/deliverable=false，task仍assigned、startedAt=null，未生成/下载文件、未确认验收。未触碰已完成446或其他角色/事项。
- **确认新缺口不是Nginx**：API `ChatActionCapabilityService.available/appendImageAdapter` 当前只提供资料读取和图片生成/编辑动作，没有通用文件生成动作；`ChatTypedDeliberationContextService.resolve`以该清单构造availableActions。李逵未开图片，本事项未附资料，未获得文件执行动作；普通CHAT本来就是read-only。不能将聊天文字伪装成文件，不能通过解除只读/伪造动作或旁路手造文件来冒充正常流程。
- 下一动作：若继续通用文件交付，应单独收敛议事→已有workspace文件执行→真实成果回传的最小动作接入方案；当前只完成用户授权的网关补齐，不扩大实现到文件业务或启用图片。旧自家接应文书也仍待更新。
- 测试控制器读跨域native被OPTIONS405阻止，随后用本人有效JWT在内存内执行无Origin反例401；不把CORS失败当作backend鉴权证据。recommend POST被测试guard拦截，未影响李逵唯一点将，不当产品缺陷。证据写入辅助代码曾用Python3.6不支持的text参数，改decode后保存，不涉及生产变更。

## 2026-10-12：文本文件切片开发接续（未发布）
- Main继续API worktree；Runtime独立写集交接Curie（01a12bb3-6fe7-7f73-9fdc-291e4ce188b8），原任务LIKUI-SELFHOST-20261011不重复建单。
- Runtime基线5b902c1b，API基线cf140272；详设见LIKUI-TEXT-FILE-ACTION-20261011.md。已向接收方显式提供项目/Runtime AGENTS及工具README；Curie在本次交接结束前明确确认三个文件均已实际读取。
- 原事项448不扩权；两仓完成自检并固定制品后，以新事项做真实文件下载/验收。当前只有源码候选，非上线证据。

### 2026-10-12 00:27：实现及候选制品完成；等待发布空间
- Main API4345f5e4c1/tree5bb3e2c5：242项真实定向测试全通过，分层/依赖/公开制品校验/fresh bootJar成功；已合入并push API develop，但线上仍1.14.7/cf140272、JAR SHA333d525e…b8c57。
- Runtime原Owner Curie提交dc5e335d后，Main补现有依赖诊断发现两个新增测试断言不合真实接口；已回原Owner修成按error.code/ready不为true判断，无产品放宽。最终807b86d/tree959c72f2，1.0.3；40项测试通过，Main另补2项真实payload闭包测试。临时依赖链接已清理，未正式安装/发布。无独立Reviewer。
- API制品唯一有效批 `/var/tmp/cyf-likui-textfile-api-release-20261012-stwh_2e6`，原producer成功、包持久保存、controller快照已建立；详设记录SHA。上一批控制器目录权限/不存在selector问题已留证归因并修正，旧232报告不能冒充最终242批。
- 实际阻塞：当前约195MiB空闲；按本批字节及原安装动作，发布另需约1.13GiB，缺约964MiB。未执行admission/安装，未绕空间/备份规则，未删除其他聊天/旧发布证据。需用户授权定向清理已完成的冗余制品（保留证据及当前/上一版回滚）或由用户提供空间后继续。
- 配置待做：API仅追加execution allowed MIME text/plain；李逵profile开nativeConversationTextFileEnabled且图片保持false；两者必须在原锁/备份/配置摘要/原installer链路内应用。新事项无附件请求output.txt三行内容→START/上传/commit→成果下载hash→正式验收。448仍原授权/CLARIFY，446不复测。
- 没有新的浏览器/SSH/服务进程，无生产业务写操作。开发、制品、发布、真实验收状态分开。

- Runtime807b86d已ff合入并push isp-install develop（00:26:36回读远端一致），未发布；Main接收全部写集后已关闭Curie，无遗留后台开发承诺。

### 2026-10-12 00:43：授权清理与统一发布范围
- 用户“允许”后，仅清理五个已verified旧API批次的展开application.jar冗余副本（共1269252268字节）；保留逐字核对的原始package.tgz、所有测试/安装证据以及当前1.14.7/上一版1.14.6全部回滚所需文件。旧admitted展开目录不再完整，不声称可以直接复用安装。原coordinator→release锁内检查活动FD后执行，回执在本批cleanup-completed.json。清理脚本两次前置错误均未删除文件（历史安装终态为verified、锁路径校正），保留实际脚本和前后证据。
- API4345f5e4/1.14.8原admission通过，217项SQL/initializer资源字节与当前线上一致。18项现时只读身份/inflight投影、F06/E05现时catalog equivalent；仅将text/plain加入execution MIME配置，原值保存/home/isp/baks/likui-textfile-20261012/application.properties。尚未因此重启，未新增DDL。
- 用户追加“最新不是1.14.9吗？并且最近还有页面优化，统一进行发布”：实核1.14.9是Web线上a3bceaf/Flow203，API线上仍1.14.7。统一批次不混淆组件版本：Web1.14.10/ad5a687（包含本地未发布d8b703b取消事项刷新样式和36c447c正式成果页隐藏工作区入口），API1.14.8/4345f5e4，李逵Runtime1.0.3/807b86d。不发布其他组件或扩展功能。
- Web固定候选复用Flow4403172，同Run原全量测试/构建/制品/部署，发布后恢复原CI-only配置。证据本批web-release/。API复用已有242项测试精确制品，不重复构建。
- 远端李逵原installer已在全新release完成完整npm/隔离Python依赖、stage/final闭包验证；仅制品准备成功，尚未激活。固定Node22.22.2、Python3.11.13，pip来源显式https://pypi.org/simple/（远端沿用其原固定来源，不冒称本机全局源在远端生效）。

### 2026-10-12 00:54：API/Runtime已发布，Web全量重验中
- API第一次安装因Main原子配置写入被umask077截去group read而启动失败（root:isp0600，cyf-api主组isp），不是产品源码/制品测试失败。原installer按forward-only保留本批候选，不回退旧JAR；Main在原锁内修为root:isp0640，实际runuser cyf-api test -r通过，配置字节及已准入绑定未变。随后原--local-install同binding forward repair成功，未旁路手启或伪回执。首次失败日志和修复回执保留。
- API1.14.8/4345f5e4：JAR9a76c427…c246，PID2528918/canonical cwd；loopback实际health.status.code=UP。F06两表/E05一表全existing_equivalent、exit0，未执行新增DDL。canonical目录只读回归8项通过。证据api-online-verification.json、install-forward-repair.stdout.json。
- 李逵Runtime1.0.3/807b86d已按原独立制品切换，PID3071281/active/enabled/NRestarts0；只开nativeConversationTextFileEnabled，原installation身份沿用，不重enroll；旧codex-ws-agent inactive/disabled/PID0。备份与制品完整catalog在远端/home/isp/baks/likui-textfile-20261012，业务尚未验收。
- Web Flow204/ad5a687：2924pass/2pending/1fail，旧feature-flag源码断言未同步!formalTaskRef；原新UI测试覆盖该逻辑。Main仅修正旧断言一行，定向22pass，提交235048e6820afd24f21c6ca78b4b4c30901508b7/tree1ff98d709c69b06a7f0cc18c6c6bb824f7958a96并push；不删测试/跳测。版本仍未发布的1.14.10，Flow205单次新固定候选全量重验/部署。失败Run204留证、不覆盖。

### 2026-10-12 01:06：统一发布完成，449真实验收失败（未修复）
- Web1.14.10/235048e6，Flow4403172 Run205 SUCCESS：2925pass/2pending/0fail，364安装文件及11公网资源与制品匹配；原CI-only配置恢复APPLIED。最近取消历史刷新按钮样式和正式成果隐藏工作区入口均已纳入并在390px真浏览器核验。
- API1.14.8/4345f5e4及远端李逵Runtime1.0.3/807b86d均已上线，最终记录为本批unified-release-result.json；原unified-release-intent.json保留Run204历史输入，不再当最终上线证据。
- 唯一新事项449创建201，唯一点将500/ASSIGNMENT_OPERATION_INTEGRITY_ERROR；只读证实ACTIVE grant已成功写入GENERATE_TEXT_FILE，GET449仍assigned、startedAt=null。未重复点将、未生成或验收文件。
- 根因一：AgentTaskDeliberationOperationReadServiceImpl.java:45-46白名单漏GENERATE_TEXT_FILE，339行拒绝grant回读。根因二：实际chk_pwex_output_mime缺text/plain，outbox创建执行INSERT被真实MySQL约束拒绝。两者均是本轮开发漏同步，非Nginx/网络故障；尚未修改源码或数据库修复。
- 已纠正详设“不做DDL”的错误假设；下一步仅补这两个契约、真实MySQL及grant回读测试。新约束迁移需单独核对生产授权及输入，不套用本次无新增DDL的原authority。新后端制品发布后续验449，Web/Runtime未变不重复发布；448/446不动。
- 当前没有后台修复Agent或持续验收承诺。完整失败证据task449-grant-and-mime-readback.tsv、browser/task449-final-readback.json；详设保留具体修复点。

### 2026-10-12 08:15：两处修复已构建通过；先处理主机OOM现网恢复
- 用户“好，继续”后，Main接续同任务，范围为文本生成grant回读白名单及唯一text/plain CHECK迁移、后端发布、原449验收；不发布未变Web/Runtime，不新建/点将。API工作树仍/home/isp/wsps/cyf-worktrees/likui-textfile-api-20261011，远端核对起点4345f5e4。
- 固定候选8477796f5c01650c2b3e1b6e6a7cd7744c494e6c/tree6f481923afe838b4a02aa56e481b51bb1ce5eca6，计划API1.14.9。补operation白名单、旧建表/加列SQL当前契约、新v1_17原子CHECK替换、initializer精确旧/新MIME集合与ENFORCED核验及幂等。保留未知/重复grant拒绝和所有既有MIME，不删约束绕过。
- 新增真实MySQL空库/现有CHECK升级/文本CONVERSATION插入/HTML拒绝/图片数据保留/事务回滚/重复启动测试。首批新增fixture误用隐式动作hash域，修成生产显式DELIBERATE；第二批真实MySQL暴露CHECK_CLAUSE含反斜杠转义引号，已据实际HEX回读仅规范化该表示并补单测。失败批证据保留，不放宽验证。最终原Gradle构建08:13:35成功，所有所选测试、分层、依赖与fresh bootJar通过，精确统计由producer读取。
- 批次/var/tmp/cyf-likui-textfix-api-20261012-2vrlsa7l。原表结构只读dump与MIME计数已留证，无生产DDL执行。新约束只在授权候选启动时迁移，不套用原“无DDL”authority。
- 08:07:01系统全局OOM杀生产mysqld2001（mysqld_safe已自动恢复）；08:08:30再杀API2528918。浏览器发现502后核对内核日志属实，用户已主动告知；这发生在本地回归期间、新版部署之前，不能写成新候选上线失败。完整内核日志本批host-oom-kernel.log。
- 已关闭本任务浏览器；真实MySQL测试全部成功后提前正常shutdown本任务测试DB，释放其临时数据；旧已完成本任务/dev/shm构建先保存日志/JSON/XML后释放，持久admitted JAR/原包仍在。没有停止其他聊天进程。
- 本轮原锁下仅清理本任务已verified1.14.8的两份相同传输包；随后同binding原installer恢复现网报RECOVERY_BINDING_MISMATCH，确认原installer恢复仍需要incoming副本，已在原锁内从完整admitted包精确恢复incoming并重走原installer。这一清理分类错误已留证，不再删除当前incoming。原生产JAR与配置未改、未手启旁路。恢复尚需健康核验；新版发布尚未执行。

### 2026-10-12 08:25：现网恢复，279项通过，新版已准入但首次切换前空间拦截
- 已通过原canonical lifecycle `/usr/local/sbin/cyf-api-kit start`（coordinator→release→lifecycle锁）恢复未变1.14.8，PID2673853、健康UP；原installer对“installed但离线”的同binding只查健康，不负责重启，所以改用现有标准lifecycle start，不是源码部署/手写java旁路。新代码尚未激活。
- 新候选279项测试全部通过(0失败/0错误/0跳过)，包含4项真实MySQL及27项点将回读相关测试；原producer包SHAf67206d32011d4272e2402a424e14b16261a098ce17ef8f7a20c914d9c965cf3，JAR7ef632fd922f3474e9e7097e071e3d4fcac8826d0583f4fc6906b0818f73173c。API develop已push8477796f5c。producer首次拒绝新输出目录0755，改0700后同精确构建证据打包成功，不重跑Gradle。
- 原admission通过，新授权/schema-plan显式记录唯一text/plain CHECK迁移，4个schema资源变化逐字限定，其他schema资源不变。新decision `/var/lib/cyf-api-flow/local-inputs/likui-textfix-1.14.9-20261012/install-decision.json` SHA c8151ec6cb3a10b81864f8f5abaffed30fbe3770f974d5069b1094fcb7854391；binding970f7ea89addb0563fdd45e0d7951c3ef16a2de72f723b9113b5e976587a2079。
- 首次新install在原应用停止之前因实际rollback JAR所需空间不足被拦截；record现为新版本prepared/pre_cutover，线上仍旧JAR/PID健康，不伪报新版已上线。
- 仅清理本任务已结束工作树的16MiB Gradle生成元数据(先获取原Gradle锁，全球依赖/compile缓存不动)、关闭本任务浏览器释放profile；旧本任务OOM终止进程对应7.6MiB日志无活动FD，gzip后逐字验证原SHA并保留映射。原包、安装记录及当前/上一版回滚JAR全部保留。新producer运输副本在admission精确持久复制后删除，admitted归档仍完整。当前incoming保持不动。
- 实际释放输入发生变化后已接续同decision原installer r2，不重复构建；完成后必须确认新版本/JAR/schema/实际业务。未手工修改449或schema行数据。

### 2026-10-12 08:40：API1.14.9发布成功；449文件已生成，第三处跨层遗漏修复中
- 同decision原installer r2 verified/exit0；API1.14.9/8477796/JAR7ef632fd…173c，PID2678879、canonical cwd、healthUP，目录回归8项通过。真实数据库CHECK已接受text/plain。Web/Runtime未变、不重复发布。
- 原449/原幂等key回读200：ACTIVE grant含GENERATE_TEXT_FILE，bootstrap ADMITTED/attempt1。同conversation1760458005713的唯一执行pwe_b96f4…aee已OUTPUT_COMMITTED，provider lease version1，唯一资产ast_2aa22…5937。
- 真Chromium点击“下载”得到41字节UTF-8，恰好三行“确认议题/通知参会人/检查设备”；下载SHA de2df941fcae44561d2df2d539bd94481bf241045ee57aadddcbfea9433d3b7a与数据库资产SHA/长度一致。实际文件名part_2aa22fe1b5c8753fef2074a97c885937.txt，不是请求的output.txt，未掩盖该差异。原task仍assigned；没有正式验收。
- typed-outcome GET503/TYPED_DELIBERATION_PERSISTENCE_ERROR，message=Action progress child lineage is inconsistent。已定位ChatTextFileActionExecutionService使用text-file-request域，ChatActionFinalService却统一按action-execute域推导childID；不是实际文件执行失败或网关故障。
- 最小修复抽取文本执行器requestId(event)由准入和进度读取共用；保留所有scope/父子关系/状态校验及原图片/INSPECT计算。补真实准入写入→进度reader的RUNNING/OUTPUT_COMMITTED/FAILED/CANCELLED和越权/未投影完成拒绝测试。无DDL、无新接口、无新事项/点将。
- 第一轮新增测试误引用CanonicalContextJson包路径导致编译失败，已修正到本service包、提交cd1e6d6；非生产故障。新候选API1.14.10在/var/tmp/cyf-likui-progress-api-20261012-lrxcyfv2构建中；不把源码修复当已上线。
- 本轮构建不启动MySQL fixture；schema代码不变，后续严格对照已上线1.14.9的SQL/initializer字节。自己的浏览器r3已关闭，旧成功构建/dev/shm先完整保存JSON/XML/log再释放；正式包/当前生产JAR及回滚未变。

### 2026-10-12 09:00：1.14.10发布并完成原449正式验收
- 最终API cd1e6d6ebe/tree241a547d、1.14.10，已ff合入并push develop，远端回读一致。206项实际测试0失败/0错误/0跳过，最小修复保留权限/事务/幂等/原图片与INSPECT回归、validateLayering、依赖/公开制品/POI和fresh JAR；本轮不运行独立MySQL fixture、未再次触发OOM。
- Batch `/var/tmp/cyf-likui-progress-api-20261012-lrxcyfv2`，包SHA44f45e20fb69b8e81ea99cca80ad601c899907416ac4d123cc061e4fea9ccd5c，JAR5bc239aeda3af9abfc8f4033d59d3c513219b26ec8f948aea58a48fce44b4085。包持久保留在admitted；producer运输副本准入后精确去重，原路径不再存在。
- 控制面输入纠错：尝试/dev/shm作为producer输出被PATH_UNSAFE正确拒绝，改回标准受保护批次目录，复用同一成功构建证据；prepare误传wrapper摘要而非admission.json、授权证据封装缺authorization键均在安装前拒绝，分别修正精确输入，原失败证据保留。没有重复编译、放宽原helper、伪造用户新授权或绕过拒绝。
- 再按原授权、原锁去除两个本任务完成后的冗余副本：1.14.8展开JAR、已被新版本替代的1.14.7旧回滚JAR，共507736711字节。先逐字核对完整归档内容；1.14.9完整admission/incoming/canonical及1.14.8物理回滚均保留。旧1.14.8展开admission不再完整，历史重放须从归档精确恢复，未宣称旧路径仍可用。详情completed-expanded-cleanup-result.json。
- 新decision `/var/lib/cyf-api-flow/local-inputs/likui-progress-1.14.10-20261012-r3/install-decision.json` SHA5f70b4f4bb4f1511555e7a155690a535eadbd9618f04bdd21c5e7ce43e4c67fd。binding2e010233b823574fead55312710b657f731b7e8b7bc09855f485688166c85e6f，原inspect及install均exit0，summary verified，record installed/installed。218项SQL/initializer字节未变，原F06/E05 existing_equivalent；健康UP、canonical PID2690144、目录回归8项通过。
- Web未重发；当前host record仍1.14.10/235048e6/Flow205，专属Chromium实际加载42项JS响应SHA/长度与该制品记录相符。李逵Runtime1.0.3/807b86d沿用本轮之前的真实安装回执；本切片未SSH重启或重新enroll。
- 原449进度GET已200，actionProgress=COMPLETED，childRequestId正确。正式成果页文本预览正确；真实下载output_1.txt为41字节UTF-8三行，SHA de2df941fcae44561d2df2d539bd94481bf241045ee57aadddcbfea9433d3b7a与持久资产及最终选中成果一致。下载名非原要求output.txt，已明确告知并留差异，不扩大本次到前端命名修复。
- 专属浏览器唯一获准业务写入为POST449/finalizations一次、返回200；operation fin_67e467edc68da51b0dc12226b3c70f8159b53857aababa6617537e174188abce，state completed/stage TASK_COMPLETED/delivery accepted/taskVersion4。只读DB显示唯一execution OUTPUT_COMMITTED、provider-start标记/leaseVersion1、唯一asset和唯一本次finalization；不是从聊天文字手造文件。
- 真刷新后最近事项/事项详情已完成，历史成果仍可查看，验收按钮不再允许重复提交。测试guard阻止两次recommend POST（未执行），是只读验证边界而非产品失败；未新建/重复点将、未触碰448/446或其他角色。业务完整回执business-acceptance-final.json，边界为无附件UTF8文本正常流程，并非任意文件格式/编辑/所有技能通过。
- 自己的浏览器已关闭、profile清理；成功构建/dev/shm在完整保存并核对JSON/XML/log后释放，正式admitted包/JAR、回滚和全量证据保留。没有后台子Agent或持续巡检承诺。磁盘剩余约276MiB，是后续发布需考虑的真实主机容量，不是本次业务失败。
