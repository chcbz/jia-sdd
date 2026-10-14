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
