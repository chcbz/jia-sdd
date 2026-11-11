# JYT-MODEL-RECOMMEND-20261028

Owner：本聊天。2026-10-28，状态：两端已随后续版本上线；2026-10-30定位到推荐参数类型不兼容导致请求前ClassCastException；解密Key与Codex一致、原接口鉴权200，修复已合develop bb1b744956，轻量SDK HTTP smoke 2项通过；受其他任务资金事务回归失败阻塞，尚未正式Flow/安装/业务验收。

## 范围和固定源码
- 单轨升级 POST /agent/tasks/{taskId}/recommend，删除旧单人规则推荐和Web打分兜底；不新增兼容端点。
- 复用后端 ChatModel，无工具、无记忆；候选/技能权限和最终承办接纳仍由API持有。
- 非目标：Runtime/bridge、技能安装、执行协议、团队推荐、自动指派、资金/DDL、生产部署。
- 固定HEAD/tree、branch、本地origin/develop和2026-10-28实查远端见 `specs/juyiting-assignee-recommendation/evidence/baseline.json`。当前API/Web分支与develop不同，存在其他任务脏修改，禁止整仓提交/重置/合并。
- 复用当前工作区，不新建worktree。原型共享文件前值存于同目录evidence/before；只做本任务增量。
- 公共接口 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4；职责 `/home/isp/wsps/cyf/specs/juyiting-skill-execution/responsibility-boundaries.md` RB-1。
- RB-01 Web展示；RB-02 API权限/委派；RB-04 模型建议；RB-07事实来源；RB-10必要校验。D项：本次删除旧单人推荐路径，不操作原生执行设计D项或其他任务的旧runner。

## 验收/最早反馈
先原型脚本语法、纯前端合同和useHallData定向测试；Java模型/服务/Controller测试交Flow5260799，Web重型验证Flow4403172，每Run<=600s。任何真实付费推理/部署需另外核对授权。禁止本机Gradle/生产打包。
必要校验：候选越权→结果拒绝；证据引用伪造→拒绝；任务/候选变化→409；身份切换→丢弃响应；模型工具调用→拒绝、不执行；失败不自动重试。非必要新增字段允许。

## 当前事实/限制
已确认默认ChatClient有工具和记忆，摘要服务直接注入ChatModel；推荐沿后者。已有SkillManagementService.skills提供原生安装/启用/当前runtime匹配，推荐仅投影自有Agent已安装的公开描述和就绪事实，不读取外部Agent管理目录。产品描述是声明，不是工具存在证明。不得给旧runner补推荐兼容。
查询只读取当前源码与远端引用，未核验线上。开发/测试/安装状态分别记录。

## 耗时
定位、实现、验证、等待：未作可比测量，不声明缩时收益。

## 集成接续（2026-10-28 17:00后）
临时索引试合：API在远端develop `129571cd`可干净套用本任务补丁；Web在 `a6e2edc0` 有6处真实内容冲突（含外部承办候选/权限与新版事项详情）。因此仅创建一个本任务Web隔离工作区 `/home/isp/wsps/worktrees/jyt-model-recommend-web-20261028`，从精确远端develop基线解析冲突，不覆盖共享原工作区。根规则、API接口v1.4和RB-1仍适用；任务完成/终止保存证据后清理该工作区。
API/原Web的其他任务脏修改不收入候选。候选生成使用一次性临时索引（已自动清理）；补丁/源树记录见evidence/candidate.json。Skills增加仅用于推荐的只读摘要，复用管理链runtime核验，不准备/下载无关待安装包；不改管理接口已有行为。

## 本轮实现与自检快照
- 单一路由的新Controller、模型/事实投影Service已实现；旧AgentController方法、旧Service单人规则推荐及AgentTools旧推荐工具已删除。团队推荐/自动指派不在范围内。
- 已核对项目Spring AI固定依赖2.0.0及对应JAR公开方法：使用getOptions和空toolCallbacks；不使用1.x的toolNames/internalToolExecutionEnabled。签名证据见evidence/spring-ai-*-signatures.txt；仅API签名核对，不代替Java编译。
- Web集成候选保持develop的公开承办候选、外部提供方披露及离线/忙碌等待语义；非嵌入详情也有失败/重试入口。无残余合并冲突。
- 精确本地候选commit/tree/parent/ref见evidence/fixed-candidates.json。仅创建本任务本地引用，未push、未合入develop；未修改共享分支/真实索引，API和原Web其他任务修改未收入候选。
- 集成Web轻量数据/合同25项、真实事项卡UI30项通过（总55项），详见evidence/web-integrated-data.log和web-integrated-ui.log。UI桩有var-dialog解析警告；不是全站/云端测试结果。
- Java新增测试未运行，正式API/Web Flow未运行，未调用真实付费模型，未部署。根CI策略已增量加入新chat测试选择器；该文件还包含他人未提交改动，不能整文件渲染发布云端。纯任务选择器补丁另存evidence/ci-policy-task-only.patch，包含技能摘要专项测试。
- 最新原型桌面浏览器重核60秒未完成，已停止该次进程并清理专用临时profile；不得把此前截图当最新字节验收。移动端响应式仍需补验。没有重启/接管已有18786原型服务。
- 下一动作：从固定候选复核云端现行配置并仅装入本任务测试选择器，确认无他人活动Run和600秒控制后走既有API5260799/Web4403172正式验证；通过后再集成。不得把当前“本地候选已固定”重标“验证/发布完成”。
- Web隔离工作区为仍在使用的集成候选，暂保留；任务完成/终止时以fixed-candidates的提交和补丁保全后清理，不清理其他任务目录。

### 2026-10-28 17:58（Asia/Shanghai）云端只读复核
API最近342/Web最近368均为其他批次SUCCESS，本次仍无Run。当前列表未见在途运行。API云端工具bundle/policy及shell/制品检查只允许develop和两条旧分支；Web只允许develop，不能直接启动本任务候选分支冒充受测源码。未改云端配置，未推送develop触发其他任务字节。安全摘要见evidence/flow-candidate-readiness.json；原始配置临时文件已清理。正式验证接续需要在现行配置上隔离增加本任务选择器/固定候选支持（保存前值并readback），或按既定集成流程固定develop后验证，不重渲染共享脏策略、不新建流水线。

## 用户授权合入与发布（2026-10-28）
用户明确“合入develop并部署”。本Owner按固定候选执行API1.17.12/Web1.16.71；先API后Web，均使用现有Flow同Run测试/构建/制品/部署。无生产数据修复、Runtime升级或真实付费推理联调。
远端基线复查仍为API129571cd/Weba6e2edc；API相对当前运行3bca7cbd还包含已集成的恢复ACK修复a6811315及其测试129571cd。Web版本更新在本任务隔离候选中，不覆盖原工作区。
现有云端默认无部署；保存原配置后临时装配固定候选版本发布配置（停用push自动触发，手动启动单一精确Run），完成后恢复CI-only。API仅在当前云端bundle追加本任务测试选择器，不导入根仓他人脏策略。运行控制复用flow-control和既有watch逻辑，570秒受控取消预留至600秒终态；不操作其他Run。
现用API生命周期helper额外包含已安装的FD9继承锁验证与FD10关闭修复，候选固定实际SHA1ea29310…；不回退到历史模板878e2f91…，不改主机helper。
候选和准备摘要：evidence/release-candidates.json；私有控制/原配置/Run信息暂存/tmp/jyt-model-recommend-release，完成后保存非敏感证据再清理。

### API首轮失败与职责修复（2026-10-28 19:04）
- API2f0b800/Web9e35ac6均已fast-forward push到develop。API Flow5260799/343在validateLayering G1失败（chat-service直接引用agent-service实现），117秒内终态FAIL，未执行部署；不能将部分执行的测试算全量通过。
- 不新增baseline豁免。类型迁至agent-core，AgentAssigneeRecommendationModel端口位于agent-api；推荐业务、Controller及相应测试归agent-service；chat-service仅实现无工具模型端口。Controller复用HostingRentHttp JWT身份和EsContext tenant/client/owner一致性；保留400/401/404/409/502/503及模型无副作用边界。
- 修复候选5eb70edaf74ec3c9b9b5d0a3e4ce1c02e7e2c862，tree3a79d9582c81caa6415b9bf78a17e8a61a3ca88d，parent2f0b800，已push develop。只通过临时索引收入任务文件，不含共享脏修改。Flow选择器随模块移动，保留全部既有必要检查。
- API第二轮344已单次发起（初始回执UNKNOWN/INIT，无源码时不重发）；后续watch只读核对源码、终态并在570秒取消本Run。Web尚未启动，发布候选仍为9e35ac6 / 1.16.71。

### API第二轮测试夹具修复（2026-10-28 19:12）
344分层检查已通过，agent-service 1186项中3项新Controller测试失败、75项既有skip；JWT单参构造得到未认证token，预期200/404/503均实际401。修复仅测试：沿同模块已认证JWT构造方式传List.of()，另补未认证JWT必须401且不调用推荐服务的用例；不放宽生产认证。候选2bb7dac00c28b15e4b2a20852ef68558e567078e/tree6cbe166ff70b52b0a3793b539cd37aa6b3af0a56已push develop。344约174秒FAIL未部署。第三轮345已单次发起，使用原完整测试/分层/打包/同Run部署链。

## 发布阻塞与安全收口（2026-10-28 19:30）
- 两端远端develop再次核对：API2bb7dac00c28b15e4b2a20852ef68558e567078e，Web9e35ac6abcac28b3c68af9075e959c256a98a336。源码已集成，不等于发布完成。
- API Flow5260799/345构建job545155046 SUCCESS：3274次执行，0失败/0错误，164项明确skip；包含Controller5、业务8、模型3、技能摘要1（另一source set重复执行技能1），分层检查及fresh JAR成功。真实同Run归档保留在`/home/isp/state/cyf-api-flow/downloads/345/package.tgz`，测试摘要及制品摘要见evidence，不以该历史Run授权后续单独安装。
- 部署job545155047在协调锁处阻塞，Run在570秒受控取消，583.298秒观察到CANCELED；没有安装新JAR。准确阻塞是其他清理任务`/usr/local/libexec/cyf/flow_host_cleanup.py` PID829375持有`/tmp/cyf-api-flow-auto-approval-v2.lock`；健康恢复的PID819377还持有API发布/生命周期锁。不得终止其他任务、抢锁或解锁；不能仅看到无活动Flow就认为主机锁空闲。
- Flow取消没有带走本Run主机等待进程。核对PID1245098的完整run/commit身份、startTicks179794487、/proc/locks等待记录及旧安装record后，仅SIGTERM本任务仍在首个协调锁之前的等待进程；已确认退出。未触及生产安装、他人PID、锁文件或备份，避免取消后延迟安装。
- 两端云端配置已CAS/readback恢复CI-only（API保留新增测试选择器，Web原配置）。Web未发起Run，不先切新消费者。
- 旧API安装记录仍335/1.17.11，JAR摘要与旧record一致；canonical-path 8项通过。随后只读health请求超时，不能宣称线上健康；该事实与本次未安装须分开记录。未执行付费模型联调。
- 下一动作：由锁所属任务释放/安全处置协调锁及发布/生命周期锁，并确认线上健康；Owner只读核对锁空闲、远端候选和云端无活动Run后，再按已有发布授权走固定源码同Run测试/构建/部署，先API后Web。不能直接重放345安装或原样盲重试；不默认取消他人任务。当前没有实施/运行中的本任务发布作业。
- 收口：本任务Web隔离工作区逐字节比对已push的9e35ac6、无未保存untracked后删除，最终两端补丁保留evidence/api-final.patch及web-final.patch。私有原始Flow响应/配置含敏感字段，导出白名单证据后清理本任务临时控制目录；未删除同Run制品、生产状态、他人worktree或备份。根仓其他任务脏修改不提交/回退，根gitlink未冒充Web正式验证完成。

## 用户要求跑通：接续核验（2026-10-30客户端日期）
Owner本聊天；本轮先做现行版本定向验收，不回装旧包、不追逐最新develop，不操作其他任务。按2026-10-29新规Flow worker只构建上传、主机独立安装；本轮无需为验收重新构建。现场API安装381/f932d38、Web377/1fdc94a已分别包含本任务2bb7dac和9e35ac6（git ancestor核验），API推荐类相对已测候选无差额，health UP，旧协调/发布/生命周期锁未见持有者。当前develop比线上更前，不据此擅自发布无关代码。工作区仍脏，不checkout或覆盖。
验收范围：复用已配置测试登录，在本任务独立浏览器检验实际Web/API推荐；仅必要的一次模型建议请求，不确认承办、不执行Agent、不购买技能、不改钱包。身份/ACL、原事项状态和费用副作用边界保留。私有证据位于/home/isp/state/jyt-recommend-verify-20261030/；无凭据出现在证据或聊天。

### 当前线上实测：模型鉴权阻塞，不能标记跑通
- 后续其他任务发布已携带本功能：API381/f932d38、Web377/1fdc94a。API安装JAR SHA1ca567f…与发布记录一致；Web612个安装文件全部匹配记录，公网index及推荐所在JuyiHallEntry bundle摘要匹配。只读health UP。此前“未上线/锁阻塞”仅是10月28日历史，不再作为当前判断。
- 使用已配置测试账号在独立真实公网浏览器创建专用普通事项551（仅推荐通知撰写，不委派/执行）。Web实际发出一次POST /agent/tasks/551/recommend，HTTP503，code RECOMMENDATION_UNAVAILABLE，requestId9fef649e-4594-4eb4-b8ae-6b0bcf8858b2；UI正确显示不可用及手选/重试，不伪装成空推荐。网络中的200同路径含CORS请求，不能当推荐业务成功。
- 读取实际生产JAR prod配置及外部application.properties，进程无聊天模型相关环境/CLI覆盖；采用现有后端连接凭据只读GET /models返回401（当前配置模型gpt-6.1-sol）。不输出密钥、不打印鉴权header、不换用Codex/Runtime/其他用户凭据。该401证明当前连接鉴权未通过；推荐503的内部分类没有日志，不能声称已完整追踪所有异常。
- 不为鉴权错误重建、不自动重试模型；未启动Flow、未修改生产配置、未重启API。需有效的后端模型凭据/访问授权，或用户明确指定可改用的现有模型连接后继续。修复连接后仍需实际验证结构化推荐、依据与页面展示，不能仅以/models成功算跑通。
- 专用事项551已经由正常UI确认取消、权威页面显示已取消，未委派任何Agent、未执行任务、未购买技能。独立浏览器退出并清理其profile，未操作其他浏览器/服务。证据 /home/isp/state/jyt-recommend-verify-20261030/{baseline.json,web-verified.json,provider-check.json,browser/recommend-smoke.json,browser/recommend-desktop.png,browser/cleanup-ui.json}；证据无密钥/token。

### 用户确认Key后：聊天接口定向复核（2026-10-30）
源码application-prod.properties与已安装JAR同名Key按内存等值比较一致（未输出Key或摘要），不是源码新Key未打包。对当前配置gpt-6.1-sol及base-url使用Bearer发最小POST /v1/chat/completions，已捕获HTTP401，服务端error.message为Invalid API key；未修改配置或模型。首次诊断响应后证据写入脚本NameError，结果未保留；修正本地写入后第二次取得上述证据，共两次最小请求，不将其冒称一次，不继续重试。证据chat-endpoint-check.json。此结论仅证明当前网关拒绝该凭据，未判定密钥本身在其他网关无效，也不归因为模型名称；下一步需核对该Key与codex.chcbz.net网关/账号授权的对应关系。

### 对比当前Codex本地连接（2026-10-30）
按用户要求只读核对/root/.codex/config.toml与auth.json，并与已安装JAR叠加外部properties比较：base-url相同；Codex auth_mode=apikey，auth.json的OPENAI_API_KEY与后端实际配置Key内存等值比较不相同（不输出Key、长度、摘要）。Codex配置wire_api=responses、model=gpt-6.1-terra；后端chat/completions、model=gpt-6.1-sol。此处为本地配置文件事实，不冒充当前对话每次请求的实际线路追踪。不复制Codex凭据、不改生产配置、不发起新模型请求。安全摘要：/home/isp/state/jyt-recommend-verify-20261030/codex-connection-comparison.json。后续应先统一用户指定的凭据来源，再确认网关协议支持；不能仅因地址相同认定Key/协议相同，也不能把协议差异直接认作401根因。

### 重要更正：解密后Key一致（2026-10-30）
用户指出后端Key经过加密。已核实安装JAR属性为ENC(...)，使用生产PID2012424环境中的JASYPT_ENCRYPTOR_PASSWORD及已安装jasypt1.9.3、jasypt-spring-boot4.0.4实际默认算法/参数，在独立轻量Java进程中成功解密，仅在内存与/root/.codex/auth.json的OPENAI_API_KEY比较：完全一致。未输出明文、未落盘明文、未发新网络请求、未修改生产配置或重启。证据decrypted-key-comparison.json。
此前诊断脚本将ENC密文直接作为Bearer发送，导致/models及/chat/completions的401；这些结果不能用于证明实际应用凭据无效，也不能用于归因推荐503。此前“Codex与后端Key不一致”撤回。旧JSON已标记supersededForCredentialDiagnosis并链接更正，原始错误事实保留。真实浏览器推荐503仍成立，但原因待查；下一步核实实际Spring模型配置/调用协议及异常，不更换已证实一致的Key。

### 503直接故障定位与修复方向验证（2026-10-30）
- 不改Key、网关、模型或生产配置；解密凭据最小POST /v1/chat/completions，模型gpt-6.1-sol，HTTP200、有效choices。证据decrypted-chat-probe.json。因此不需要为此次问题迁移Responses协议，也不能把模型名称/Key当根因。
- 从现行API381安装JAR提取实际Spring AI2.0.0、openai-java4.39.1及推荐适配器，在独立轻量Java诊断进程装配OpenAiChatAutoConfiguration，绑定JAR+外部properties、解密Key、maxRetries=0，只用虚构候选/通知需求，不启动应用/访问数据库/执行Agent。原适配器稳定触发ClassCastException：DefaultToolCallingChatOptions不能转OpenAiChatOptions；栈OpenAiChatModel.createRequest:683→internalCall:205→call:194→AssigneeRecommendationModel.judge:41。未到HTTP拦截器，因此该次未发送模型请求。证据spring-probe.json。旧业务Service将Exception转换为RECOMMENDATION_UNAVAILABLE，符合线上503；没有将隔离复现冒称完整线上异常追踪。
- 原因是推荐适配器用ToolCallingChatOptions.builder()创建通用参数；当前实际Provider实现需要其原生参数类型。修复方向：从模型默认ToolCallingChatOptions.mutate()复制并清空toolCallbacks，保留原生类型与模型/连接参数，保留全局工具默认拒绝、响应tool-call拒绝及无记忆/无重试边界，不在业务层按Provider品牌分支。
- 仅在私有诊断源码验证上述一行替换：同一安装库/配置/合成输入，实际请求/v1/chat/completions返回200，成功得到合法JSON state=NEEDS_CLARIFICATION（合成通知缺少活动细节），证据native-options-probe.json。这证明模型适配器修复方向有效，不等于真实候选READY/UI验收通过。
- 本轮共2次真正发出的最小模型请求（原生HTTP1次、修复方向Spring调用1次）；原Spring复现0次。诊断前置经历依赖未全提取及诊断自身null计数错误，均发生在网络前，修正后才得有效复现。不以这些探针问题归因生产。不启动Flow、不修改组件代码、不重启/部署、不创建新业务事项；后续应落入正式实现、补真实Provider参数类型回归、按固定候选Flow验证并独立受控安装后验收UI。
- 提取的诊断依赖JAR已清理；库摘要diagnostic-library-shas.json、诊断源码与脱敏结果保留于/home/isp/state/jyt-recommend-verify-20261030/。明文Key仅在进程内存，不落盘。旧鉴权/Key差异结论继续保持已撤回。

### 正式修复候选（2026-10-30，继续授权）
Owner仍为本聊天；目标修复Provider参数类型，不改Key、模型、协议、权限或资金链。根/API/Web脏工作区均保留。工作区HEAD516267bf/tree32d2a425；09:11只读fetch远端develop9d2ea1ab，原功能文件与工作区逐字节相同。现行API381/f932是候选基线；当前develop397失败于其他Owner的ChatMaterialsInputService G1，不重跑已知失败/不删除分层检查。
- 正式适配器改为从model.getOptions().mutate()复制原生类型、清空回调，保留全局隐式工具拒绝/输出工具拒绝、无记忆和无重试。非工具模型也保留原生类型；无默认参数的既有通用模型沿原空工具参数。
- 原3项测试保留，新增原生类型/参数值/默认值不变回归，以及真实OpenAiChatModel→本地HTTP fixture成功/400拒绝的两条完整SDK请求测试，断言无tools、两条输入、仅一次请求。不调用真实网关，不增加依赖。
- 使用一次性临时索引形成固定候选157dc9db960385a8e663319d496822e8cf814244/tree8f1efdfe16d93c7c027cb835ca4a3c15c1b1e0c2，parent当前线上f932；仅2个推荐文件与starter版本1.1.3-SNAPSHOT，分支codex/jyt-recommend-options-fix-20261030。不checkout/覆盖共享索引/收入他人脏修改。证据options-fix-{baseline,candidate}.json与补丁；正式Flow/安装/业务验收尚未完成。
- 初始读取到Flow空闲后准备云端候选；写入前已有其他Owner Run398在途，既有控制入口拒绝ACTIVE_RUN_NO_WRITE，没有更新云端配置、没有启动本任务Run。等待对方终态并重新核对配置/实际安装版本后继续，不取消对方Run。候选准备改为复用实际381的271selectors完整worker模板；此前250selector旧模板未应用/未运行。

### 自检、合入与发布阻塞收口（2026-10-30 09:36 Asia/Shanghai）
- 已进一步核实当前安装器只接受source.branch=develop的干净制品；不修改安装器、不伪造分支/CI身份。因此前述“旧线上基线独立分支构建安装”方案未执行。候选157dc9db仅作为本任务最小代码提交并已推送；没有为不能安装的分支付费构建。
- 当前develop由其他Owner继续修复分层问题并推进至969e0f8c；其Flow398在FundedBountyServiceRealTransactionTest六项失败，日志证据/home/isp/state/jyt-recommend-fix-20261030/prior-398-log.json。不能以此判定本修复失败（398不含本修复），也不能重复构建已知失败基线或删除资金回归。
- 轻量本机自检仅编译本次1个适配器及1个SDK HTTP烟测驱动（JVM上限128MiB），使用安装包依赖；复用正式测试中的HTTP fixture逻辑，真实OpenAiChatModel成功200/拒绝400两项通过，外部模型调用0。不是全量Gradle/生产打包，也不冒充JUnit六项或云端正式验证通过。smoke-compile.log、smoke-run.log、smoke-file-shas.json与无凭据驱动保留；提取依赖JAR及诊断class已清理。
- 自检后用git merge-tree/commit-tree集成，不切换工作区、不动共享索引。已非强制push develop bb1b74495679ca57e57bc6737bfe479d11750c13/treec57b2f737423db0bd6a0a67d420f69b119582753；父969e0f8c及157dc9db。相对当时develop仅推荐适配器、测试、starter版本3文件，未覆盖他人修改。证据options-fix-integration.json。
- 本轮未修改云端配置（写入前被活动Run保护拒绝）、未启动本任务Flow、未重启/部署API、未改模型配置或Key、未创建业务事项。原先准备但未使用的云端配置/runner副本已删除，无需恢复未改动的云端配置。没有新增worktree。
- 下一动作：待资金回归Owner修复后固定包含bb1b744956的develop，复用同一轮有效Flow构建/制品完成正式六项推荐模型回归及原业务/身份回归；优先共享精确有效证据，不为本任务重复构建。主机受控安装成功后在自有测试事项核验真实推荐/UI并取消事项；在此之前不能宣称已跑通。

### 主线接续与共享构建（2026-10-30 09:54 Asia/Shanghai）
- 本Owner继续完成推荐，不扩展费用/灰度。09:42查398仍失败；随后材料主线Owner独立提交资金fixture修正8d41c4519a，并合入本推荐修复。新固定develop022cf0dbf3fb10d0963e75c5bcd2765d1433471c/tree72aa36be06b7303abff7fbc7ac959dd3dc36e41f。本线程未重复修改其fixture、启动Flow或抢占安装。
- 共享Flow5260799/399由材料Owner启动，09:52只读RUNNING，job546153030；当前来源简化API尚未显示commit，待最终receipt核实，不能以预期候选冒充已验证来源。301 selectors含本任务模型测试。沿对方570s watcher管理，不取消其他Owner Run。
- 已准备独立浏览器验收及只读共享证据核验脚本，目录/home/isp/state/jyt-recommend-fix-20261030/。浏览器仅登录并打开办事页，尚未创建新事项/调用模型；正式验收等待合格制品安装，不在旧线上重复触发已知503。验收需求含通知主题/时间/地点/受众/字数，目标READY及真实依据展示；不确认承办/执行，结束取消自有事项。
- 当前8项canonical API路径只读检查通过，仅路径/进程边界证据，不是修复已上线。优先复用399实际测试/制品/安装，不另付费构建，不复制大包占用当前主机空间。源码/Flow/安装/业务验收继续分开记录。

### 共享399正式回归结果（2026-10-30 09:56 Asia/Shanghai）
- 399真实诊断绑定022cf0dbf3，解压原始摘要SHA516cd6a9bde6a1cac49bb05a0686971be0b23329de18d9ac05a74eb058589243已与云端marker等值核验。本推荐Controller5、Service8、Model6共19项均0失败/0错误/0跳过，包含新增原生参数/实际SDK HTTP200/400测试；首次取得本修复正式云端测试通过证据。
- 整轮仍FAIL：资金测试fixture中的agent_task_funding_operation缺OWNER_JIACN列；是越过上一tenant校验后暴露的新SQL夹具问题，不再归因为推荐或Key。必要资金回归未通过，不安装399，不将19项通过写成整个发布通过。独立发布Owner继续处置，当前生产仍未由本线程变更。
- 证据/home/isp/state/jyt-recommend-fix-20261030/{shared-run399-log.json,399-diagnostics.json,399-recommendation-regression.json}。等待修正后的共享合格制品；已登录的独立浏览器尚未创建任何事项/发起推荐。

### 共享400结果（2026-10-30 10:06 Asia/Shanghai）
- 发布Owner以73ae97abe067c2fd50b489d7e39e163deeb9fd38修正三表SQL fixture与锁观察器，Run400仍FAIL；推荐Controller5/Service8/Model6再次全部通过。只读复用对方完整云端日志，验证diagnostic marker SHA后写options-fix-flow400-regression.json，不重新拉取/启动运行。
- 当前阻塞不再只是测试夹具：真实资金创建调用事件写入时缺ownerJiacn，AgentTaskEventWriterImpl拒绝，五项资金回归失败；不足余额回滚已通过。不能删除Owner验证或绕过资金测试来安装。此路径由既有发布Owner修复，本线程不并发改动其业务文件。
- 10:04现场record仍为installed/381/f932d38；未部署本推荐修复，不能宣称主线完成。独立浏览器未创建事项或触发推荐，未发生新的模型费用。

### 合格共享构建已取得，安装待完成（2026-10-30 10:19 Asia/Shanghai）
- 发布Owner修正资金事件归属，固定aa87ca4f049eaf90bff2c97934069d156adbdde1/treeebb1bfe6bb2db5910ccb8dc84038e4d039758aef，包含bb1b744956。共享Flow5260799/401 SUCCESS（Owner观察325秒）；原失败399/400状态保留，不冒称复用失败包。
- 复用401完整日志并校验原始diagnostic SHA6a6c0bc1d83d6f560e252e3e9ef886e1f7dfa698ba95657c2c7e1daa98414d0a：推荐相关19项再次0失败/0错误/0跳过，证据options-fix-flow401-regression.json。完整制品报告与安装摘要仍由共享发布Owner核验。本线程不下载第二份大包、不并发安装/重启。
- 10:18制品正在主机下载；此前只读status仍旧PID2012424/381健康，不能以401成功宣称修复已上线。主线余项仅共享安装完成后的本任务真实推荐READY/UI验收及自有事项取消。

### 线上502与受控复现（2026-10-30，401安装后）
- 10:33核实401已安装，实际JAR SHA12aeba525ed59483b8d384916d81ddc7314b01f68b6a493bfa6b0581a254485c、PID2427238、HEALTH=UP、canonical路径检查通过。本Owner未重复安装。
- 自有普通测试事项552（完整团队通知需求）真实POST一次，502/RECOMMENDATION_INVALID_RESULT，requestId e029e09d-658c-4dbc-b08a-e1eb6ce65c55，服务端duration55116ms。未指派/执行/钱包操作；原模型输出未留存，不能声称完整原响应归因。
- 两次独立只读模型诊断均使用401实际SDK、配置及内存解密后的后端Key：合成单候选返回合法READY；随后基于同一测试账号正常GET重建五个候选/当前本领及技能事实的输入，捕获READY推荐李逵且evidenceIds=[]。李逵无登记本领/已安装技能；当前decode拒绝正确。此为同类明确复现，不冒称历史原响应。浏览器1次+独立诊断2次共3次模型请求，无自动重试。
- 另发现推荐投影把原生INSTRUCTION经验包要求为admissionEnabled+READY；实际已启用/目录匹配的image技能按原管理合同为NOT_EXECUTABLE、admission=false，不能当成可执行工具，但也不应丢失其可引用的已安装经验事实。不会改管理准入或启用执行。
- 后续固定401源码aa87ca4f04最小修复：只将具有可引用证据的候选送入模型；无证据仍在手动候选，不能满足当前READY合同，不以规则评分取代模型适配判断。按技能kind匹配原管理事实投影，保留身份/目录/版本/启用校验，增加无内容的拒绝原因日志以免再次丢失诊断。公共接口不变、无工具/记忆/自动重试。共享脏SkillManagementService不覆盖，使用固定源码文件和临时index集成。

### 第二轮证据修复合入（2026-10-30）
- Owner本聊天，固定base=401线上aa87ca4f04；通过私有文件+临时index生成16a769bd727cebaa636cb18d55f238e80aa44d8f/tree4f5f8395e3e8b97dee96d08fc181511fd819034b，已非强制push develop。共享工作区HEAD/index及他人脏文件未覆盖，无新worktree。API版本1.1.4-SNAPSHOT；公共规范仍api/docs/interface-standard.md v1.4。
- 仅六文件：推荐模型输入排除无可引用证据者（不改手选池），INSTRUCTION按原管理合同作为已启用且目录匹配的经验引用（不开放执行admission）；提示词明确非空证据；502新增常量结构原因日志。无工具/记忆/自动重试/权限或资金改动。RB-1职责维持；不涉及执行runner/协议删除D项。
- Service预计13项、Model6、Controller5、SkillManagementRecommendation4（普通及contract），正式数量/结果待Flow。本机仅使用401安装依赖对3个生产类进行定向javac -proc:none诊断，日志仅deprecated提示；不冒充正式JUnit/Gradle/发布。早先两条工具会话143中断已重启本任务轻量操作，没有运行本机构建。
- 事项552已通过UI取消，cleanup-ui.json证明“事项已取消”，无承办/执行/钱包变化。第二轮只准备新验收，不重复请求旧事项。
- 复用401实际worker-only模板与301selectors，保存本任务独立快照，准备一次必要Flow，不减回归、不为主机安装另开Run。候选、补丁、日志：/home/isp/state/jyt-recommend-fix-20261030/evidence-candidate/；构建控制证据：同级evidence-release/。本节不宣称正式测试、安装或业务已通过。

### 第二轮云效终态（2026-10-30 11:51 Asia/Shanghai）
- 本任务一次启动API5260799/402，固定develop16a769bd72；启动返回ID时来源字段暂空、状态UNKNOWN，未重复启动，随后只读核实402 SUCCESS。watcher观察总330.849秒（含终态轮询间隔），未触发570秒受控取消。云端仅worker测试/构建/上传，未连接或等待主机。
- 原默认配置已按CAS备份恢复并readback（configSHA83846448b8e635b03d771ec1b6546d0d83ec7240e5f98cfcb2151b6ae57b645a）；不覆盖其他活动Run。正在下载402真实不可变制品，完整测试报告、摘要闭包、安装及真实事项验收仍待核验。
- 文档检查`./sddw check-docs juyiting-assignee-recommendation`报告该特性原缺acceptance.md/design.md/integration.yaml/tasks.md；没有将此检查写成PASS或为局部修复新增四套重复文档。现行合同、handoff及发布证据路径保留。

### 第二轮完整制品核验与安装启动（2026-10-30 11:58 Asia/Shanghai）
- 402同Run receipt commit/tree/branch=develop、干净源码、Gradle/bridge退出0与application.jar摘要闭包均核验通过。制品SHA1c1144e373fe15091939443eef146293955263ce555861c6e5c34c84ec5b82d0；JAR SHA498b0a1f8b2e42000efbddd0801557b1f97fce790cff9418462c601876fa09b3。
- 正式推荐Model6/Service13/Controller5，SkillManagementRecommendation普通4+contract4，总32次测试执行全部0失败/0错误/0跳过；整包3766次执行，0失败/0错误/159既有跳过。保留身份/资金/材料/原生结果/MySQL与分层、fresh JAR回归，未缩减选择器。证据evidence-fix-flow402-regression.json及私有api-test-results-summary.json。
- 安装前重新核实线上仍401/aa87ca4f/JAR12aeba52，当前PID4647（不沿用先前PID2427238）、health UP/attestation MATCH，canonical8项通过。安装脚本绑定此前制品和当前版本，移动下载包避免复制，调用既有cyf-api-flow-deploy受控锁/备份/恢复；不修改生产Key/模型/配置、不重建Web、不重启Runtime、不手工DDL。安装终态及真实业务验收尚待完成。

### 第二轮安装完成（2026-10-30 12:12 Asia/Shanghai核验）
- 主机独立安装402退出0，CYF_API_FLOW_INSTALL=PASS；当前PID16865，JAR SHA498b0a1f8b2e42000efbddd0801557b1f97fce790cff9418462c601876fa09b3，HEALTH=UP/ARTIFACT_ATTESTATION=MATCH，canonical8项通过。Spring实际启动295.942秒；主机安装/冷启动独立于Flow330.849秒观察，不重复构建、不下传Flow截止时间。
- 重启前测试浏览器旧用户token在普通只读GET被401拒绝（空body）；不是模型401、未调用模型。仅清理本任务浏览器api_token并通过正常UI重新登录，技能GET200/E0确认吴用图片说明技能启用、NOT_EXECUTABLE、admission=false。没换后端Key或生产配置。
- 新普通事项554为明确匹配当前图片生成经验的需求，只查推荐、不确认/执行。真实推荐调用已发出一次，结果待记录；没有重试552或修改登记能力来凑成功。

### 主线真实验收完成（2026-10-30 12:20后 Asia/Shanghai）
- 新事项554一次真实`POST /agent/tasks/554/recommend`返回HTTP200/E0、state=READY，requestId=5a661d37-2b70-400d-ae45-fefe48ed3244；模型推荐吴用，引用服务端可用INSTALLED_SKILL“图片生成”证据，UI显示需求理解、推荐理由、原生INSTRUCTION经验说明及未核实工具/PNG输出等缺口。没有将技能经验冒称可执行工具，没有更改Agent本领以凑成功。
- 本轮验收只1次模型请求，无自动或人工重试、无指派/执行/钱包操作；推荐接口、实际后端SDK/连接、服务端事实投影、Web消费展示闭环通过。不是图片生成执行验收，也不宣称所有需求必有推荐（无匹配仍NO_MATCH）。未扩展费用功能。
- 已正常UI确认取消自有事项554；随后正常GET200/E0确认status=cancelled、assignedAgentId=null、taskVersion=1，UI显示事项已取消。原事项552也已取消，未修改其他任务（如553）。独立浏览器退出并清理自有profile；诊断提取库/classes和临时index已清理，补丁/必要证据保留，无新worktree。
- 版本/证据：API develop16a769bd727cebaa636cb18d55f238e80aa44d8f/tree4f5f8395e3e8b97dee96d08fc181511fd819034b，1.1.4-SNAPSHOT，Flow5260799/402；Web沿既有377未重建，Runtime/模型Key配置未改。正式32次推荐测试全部通过；整包3766/0失败/0错误/159既有跳过。安装、健康、真实业务均已核验；云端原配置已恢复。
- 最终摘要：specs/juyiting-assignee-recommendation/evidence/evidence-fix-release402.json；详细私有证据/home/isp/state/jyt-recommend-fix-20261030/{evidence-release/final-verification.json,browser-final/recommend-smoke.json,browser-final/recommend-ui.txt,browser-final/recommend-desktop.png,browser-final/cleanup.json}。稳定排障与证据边界回写docs/juyiting-runbook.md；原401误诊已撤回、旧失败验收/Run不改写。本主线完成；文档工具的既有四个缺失模板仍如前记录，不冒充全仓文档校验通过。

### 资料元信息增补开工（2026-10-31）
- Owner本聊天；用户要求将资料名称、类型、摘要纳入推荐。固定API base/develop=8ab1a42ac2e3f19558b97631ee58932d0006ff62（本轮fetch核实），线上记录419同源码；共享工作区HEAD516267bf含其他任务脏改，继续使用任务私有候选+临时index，不覆盖共享文件。
- 范围：API推荐服务复用PersonalWorkspaceTaskLinkService/PersonalWorkspaceService授权只读元数据，准确绑定关联版本，模型提示结合元信息判断需求，推理后复核资料变化。公共HTTP合同不变（interface-standard.md v1.4），不联动Web/Runtime、不读取正文、不新增摘要模型调用、不改费用/模型连接；RB-1业务事实API负责，模型负责适配判断。
- 权威个人工作空间文件/版本当前没有摘要字段；本轮summary缺失明确null，不以名称或MIME冒充内容摘要。尚未实现摘要采集/存储。只读取ACTIVE INPUT/REFERENCE，不将OUTPUT当输入。
- 最早验证：本机补丁/调用链静态自检，正式Service/Model/资料读取相关回归与validateLayering随Flow，不运行本机重型构建。候选与后续证据目录/home/isp/state/jyt-recommend-materials-20261031/。此记录不代表实现/验证/上线完成。
- 用户审核完整Prompt后确认实施，并明确不限定附件类型。候选使用用户批准全文，不保留image/*专用提示或后缀→技能规则；资料名/原文件名透传，MIME辅助。新增未知MIME、陌生后缀、无后缀资料回归；摘要缺失边界已向用户说明并获确认。Prompt原文暂存任务目录approved-prompt.txt，正式源码为chat推荐模型类。

### 资料推荐候选与首轮验证（2026-10-31 18:10 Asia/Shanghai）
- 功能提交db4b916582ed0ee53ecf9662c6d14df9cc936ac4已非强制合入develop；1.1.9-SNAPSHOT，7文件，公共HTTP/数据库/Web/Runtime均不变。完整批准Prompt已写入，资料支持所有类型（无白名单/后缀映射）。共享工作区/index未修改。
- Flow5260799/420失败，观察134.687秒；业务源码编译通过，新增RecommendationMaterialsTest通配导入使两个Failure类型歧义，4个位置编译失败，非模型/网络故障。未产可发布制品、未安装、线上仍419。失败诊断保留release/run420/，不把已跑部分测试当完整PASS。
- 已仅修测试显式导入，提交2a8a67c58c1949d671a4952bac496527ec1f3cea；保留同一回归策略（550 argv，recommendation.*含新增7项）。云端临时配置已CAS恢复并readback。下一次为修复输入后的必要验证，不原样重试，不删测试。

### 资料推荐云端验证成功（2026-10-31）
- 修复候选2a8a67c58c1949d671a4952bac496527ec1f3cea/tree6ed7f2ae3fbaf24ea0edca24e05ce2bb02d6e2ec，Flow5260799/421 SUCCESS；观察443.043秒，worker只测试/构建/上传，无主机等待。420保留原FAIL，不重标；必要回归与fresh JAR均未删减。
- 批准Prompt与固定源码逐字一致，SHA256=0fe2a5537d5529acd57b1b20f8b44ab64e9a58c2cf694a93e8ead211485a4731。云端临时配置CAS恢复并readback至原canonicalSHA d87b3ad62339dacd03d90117b848517dce3e8f03856768b2da6e29e83ac7a4b7。正在下载421同Run制品，完整报告/摘要、独立安装与业务验收尚待核验；线上此时仍419/HEALTH UP/attestation MATCH，canonical8项通过。

### 421制品核验与独立安装（2026-10-31 18:26 Asia/Shanghai）
- 同Run制品SHA256=67d72fa732e9b8ced033d0e425a91871f36f68804536a7af0d14cfb929b13371，JAR SHA256=437ee83a4ccc2b73a1ede0f8ccdfe3a5416e90f48efcc8112b2bd8d514950076；receipt固定源码/tree、develop、干净输入、Gradle/bridge退出0及JAR闭包均核实。
- 推荐资料7/Service14/Model6/Controller5，共32项全部通过；连同工作空间/精确版本读取/MySQL资料回归，共63项全部0失败/0错误/0跳过。整包3401次测试、0失败/0错误/160跳过（不将跳过项称为已通过）。本机仅补丁/Prompt一致性/控制脚本语法检查，没有本机构建。
- 复用421制品独立主机安装，严格核对旧状态仍419/8ab1a42及实际JAR31e8f730；调用既有cyf-api-flow-deploy锁/备份/恢复入口，不创建新Flow、不改生产配置/模型Key、不重启Web或Runtime。安装终态、健康和真实资料推荐待验。

### 421安装与健康通过（2026-10-31 18:38 Asia/Shanghai）
- 既有安装器退出0；当前记录installed/421/2a8a67c5，实际JAR SHA437ee83a一致，HEALTH UP、ARTIFACT_ATTESTATION MATCH，canonical8项通过。安装/启动在主机独立完成，未延长Flow、未下传600秒截止时间。
- 自有浏览器正常登录测试账号；新普通事项568只写“分析结果”，上传/关联本任务合成1像素PNG“现场检测结果.png”，create200、upload/link201，均E0。只触发1次真实推荐，不指派/执行/资金操作；返回结果及取消/解绑/回收资料待完成。不操作其他已有事项。

### 资料推荐真实验收与收口（2026-10-31）
- 自有事项568一次POST推荐200/E0/NO_MATCH，需求理解明确：“需求是分析关联资料‘现场检测结果.png’中的检测结果，需具备读取图中检测信息并结合相应领域进行解读的能力。”模型明确仅有元信息/无摘要，不声称已看图；这证明短需求结合资料名/类型进入能力判断。候选证据不匹配时没有强行推荐，不把NO_MATCH包装成READY，也不是正文分析或技能执行验收。
- 真实模型仅1次、无自动重试、无指派/执行/钱包操作。事项568正常取消后GET确认cancelled且未指派；自己的资料关联已DETACHED，合成68字节PNG已TRASHED且无引用。首次清理脚本未按前端合同给强ETag/acknowledgement，trash412无副作用；核实既有workspaceRevisionTag和acknowledgeExistingReferences=true合同、重新读取0引用后，仅重试清理该文件成功。未改产品代码/权限、未重复推荐或取消，不影响其他用户事项。
- 浏览器正常退出，自有profile已删除；本任务无worktree。私有最终patch、批准Prompt、固定源码、420失败与421完整制品/安装/验收证据保留/home/isp/state/jyt-recommend-materials-20261031/；临时index及候选副本收口，不碰共享工作区或其他任务状态。
- 当前已核验上线：API1.1.9-SNAPSHOT/2a8a67c58c1949d671a4952bac496527ec1f3cea，Flow421；Web/Runtime/模型连接配置未改。稳定资料推荐知识已回写docs/juyiting-runbook.md；汇总specs/juyiting-assignee-recommendation/evidence/evidence-materials-release421.json。摘要存储/生成和前端推荐动态效果不在本次实现中，不宣称已完成。

### 2026-10-31 待确认承办详情三项修复（进行中）
- Owner：当前会话；范围：推荐重试读取权威事项、承办选择对齐唯一原型、候选空态。不改模型连接/Prompt、API权限、费用或Runtime，不操作用户事项的指派/取消/资料。
- 固定源码：Web origin/develop 2d95422951289ca0b3ab74aa805f7a4b03cbecdd；API 2a8a67c58c1949d671a4952bac496527ec1f3cea。生产记录分别匹配上述commit（2026-10-31查询）。共享工作区大量无关修改；少量候选文件在 /home/isp/state/jyt-assignee-detail-fix-20261031/candidate 保存，临时index集成，不覆盖共享工作区。
- 真实诊断：正常登录只读打开事项565并推荐，捕获409 RECOMMENDATION_STALE，后续200 NEEDS_CLARIFICATION。不能将瞬时过期归咎于key或宣称已确定具体候选漂移字段；不移除服务端并发保护。前端重试目前不重读事项详情；无推荐被误作无候选已定位。
- 分层：Web负责请求生命周期与展示；API继续拥有候选准入及推荐快照校验。接口规范api/docs/interface-standard.md v1.4不变；只改Web，不默认联动后端/Runtime。正式验证走Flow4403172，当前未启动/未发布。
- 2026-10-31实施：唯一原型assignee-recommendation.js/css、prototype-spec先更新；候选按外单原型增加内联卡、所属筛选、选中态、PC双列/手机单列。Web刷新先GET详情再单次POST推荐，preparation与模型epoch分别管理；普通候选成功读取的taskId传至BountyPanel决定真实空态。原型手机390px已确认单列且无横向溢出（browser/prototype-mobile.png），桌面继续核验。
- 最小轻量检查10项通过（6秒；含SFC行为+推荐状态），不冒充正式CI。诊断首次缺public fixture、随后未启用tsx的加载问题已修正诊断入口，非产品失败。候选读取失败/身份或事项切换不调用模型，版本更新与重复点击合并有定向回归。
- 远端已前进到9a8df904（小程序下载任务），不覆盖该任务；候选基于其集成，原型规格保留其新增节。合入develop commit 4b62b77ddcba06307e04b89a45c43a399cc27c3d，Web1.16.82，精确tree见/home/isp/state/jyt-assignee-detail-fix-20261031/source.json。共享主工作区与index未改（仅唯一原型本次增量及根文档更新）。
- Flow4403172/387已启动；启动初始UNKNOWN因source未到，实际Run387 RUNNING，固定输入及控制面证据release/。监控总600秒上限，只结束本任务Run，不运行本机生产构建。当前未安装。
- Flow387真实FAIL（约113秒观察），3625项通过/4项失败：旧UI测试仍点击“更换承办好汉”来展开默认已展开列表，或断言“无推荐即无人”的旧源码条件。已按新交互更新原有4项回归，未删回归/未放宽准入；定向行为3项及空态契约1项通过。测试修复commit709d30ddb77f4e8b33d405093b6b4a75585a2e64，Flow388已固定该候选执行；387失败证据保留release/run387，不使用失败Run制品。
- 原型PC1440宽双列542.5px/542.5px、手机390宽单列332px，无横向溢出；截图browser/prototype-desktop.png、prototype-mobile.png。生产安装前已在现有锁下备份Web386（/home/isp/baks/cyf-web-flow/20261031-assignee-detail-fix），不回滚API或业务状态。
- 2026-11-01已安装并核验：Web1.16.82 / 709d30ddb77f4e8b33d405093b6b4a75585a2e64 / tree bc473ff477299d55dd123ee665637e32673400fc；Flow4403172/388 SUCCESS，平台create→update128秒，3629 pass / 0 fail / 2 pending。制品SHA256 f7f222600209543dc4991f022b31e08ffc1203c3e34c53407345409af2024881，612个制品文件核对通过。主机独立安装exit0，线上入口及聚义厅懒加载资源与制品摘要匹配。云端配置已按readback恢复原值，不触发API/Runtime构建或安装。
- 线上业务：同一用户事项565只读打开；真实存在5个可选候选时不再显示招贤空态。手选与所属筛选不触发指派，切换筛选保留选择；PC1440双列、手机390单列且无横向溢出，browser/online-verification.json及online-1440/390.png。显式重新推荐观察到先GET最新事项再POST 200 NEEDS_CLARIFICATION，读取/推荐阶段spinner、推荐按钮、候选选择与确认按钮均为正确忙碌/禁用状态。没有确认承办、取消事项或修改用户资料。
- **第一问题结论边界**：上线后首次自动推荐仍出现一次服务端409 RECOMMENDATION_STALE；显式刷新后成功。已修复旧版本直接重试的前端缺口，但现有证据未定位服务端前后快照具体哪个候选/资料字段变化，不能宣称所有409都消失或该409一定是误判；保护仍保留。若持续发生，需要对该服务端快照变化继续做定向归因，不盲目重试模型。
- 汇总：specs/juyiting-assignee-recommendation/evidence/evidence-detail-release388.json；证据/home/isp/state/jyt-assignee-detail-fix-20261031/。根文档与共享原型的其他任务修改保持，不宣称根仓已整体提交。
- 收口：本任务候选副本及临时index已删除，commit/最终patch/云效失败与成功证据/制品/截图保留；自有浏览器profile关闭清理，自有18786原型预览停止，不操作其他会话服务。2026-11-01最后查询远端develop已由其他任务推进至e6a95da，当前部署仍固定709d30d/388；本任务不自动部署后来源码。

### 2026-11-01 向量推荐概设（仅分析，待确认）
- Owner：当前会话；用户要求重新核对代码和规格，输出符合当前架构/职责边界的最小概设。非目标：实施、模型计费探测、合入、部署、改用户事项。
- 固定读取：API origin/develop `2a8a67c58c1949d671a4952bac496527ec1f3cea` / tree `6ed7f2ae3fbaf24ea0edca24e05ce2bb02d6e2ec`；Web `e6a95da175384ab8ed7d34337fc7a45f2d92ef60` / tree `4b792f1eff9a9f801af8b0029c0cbcec653b51b0`。本轮fetch成功；共享脏工作区不作产品基线、不覆盖其他任务。
- 概设：`specs/juyiting-assignee-recommendation/vector-concept-20261101.md`。现有Embedding/ES记忆基础已发现，不混用记忆库；推荐拟用批量Embedding＋Redis向量缓存＋候选内精确匹配，不新增索引平台。外部无正面能力证据、资料summary=null、既有409未完全定位均明确保留事实边界。
- RB-01/02：Web仅文案/状态消费，API拥有推荐与权威事实，技能/资料批量读取归原服务；chat适配只负责模型/缓存。RB-03无Runtime变更。现行接口规范工作区v1.4与固定API提交v1.2的差异已记录，实施遵循用户最新规则，不扩为全项目迁移。
- 待确认：纯向量不再生成具体澄清/复杂推理是否可接受；是否先验证当前连接声明的Embedding模型。未做模型调用、测试/构建/生产修改；概设不替换现行已上线R1规格。最早验证为获准后的合成语料连接验证与效果样本，不把stub单测当模型效果证明。

### 2026-11-01 用户改选Elasticsearch，概设v2（未实施）
- 用户明确改用Elasticsearch路线；原概设原路径更新为v2，Redis缓存＋API计算退出目标方案，不并存两套。沿前轮固定API/Web基线，本次未重新fetch或宣称最新线上。
- 最小设计：现有ES连接＋独立能力投影索引；当前授权/可引用证据精确版本过滤；请求内批量补齐缺失索引、确认搜索可见；批量多查询精确匹配，按Agent取最佳证据后汇总。能力更新不先新造MQ/异步平台，删除与索引清理纳入交付边界。
- 分层：推荐编排在agent-service，ES分区/持久化在agent存储适配，Embedding端口agent-api/实现chat-service；原技能/资料服务持有权威。无Runtime/业务SQL迁移/聊天记忆索引变化；具体模块依赖及ES DSL需实施时固定版本验证。
- 保留待确认：纯向量是否允许撤下具体澄清/复杂推理；现有Embedding连接验证授权。本次ES选型不视为这两项已确认。文档明确冷索引、搜索可见、分片/bulk部分失败、候选覆盖与性能/费用边界。没有产品改动、外部计费调用或部署。

### 2026-11-01 索引写入时机纠偏（概设v3，未实施）
- 用户指出检索时才写索引的性能问题。撤回v2请求内补索引：能力变更后登记可恢复的更新意图、后台批量Embedding/ES写入，初次启用前初始化；推荐只生成查询向量并读ES，不同步补写/等refresh。
- 已定向查到现有Agent命令outbox，但未证明可承载能力索引，不挪用Runtime命令合同。持久任务/调度复用需核实；没有合适入口才加本用例最小更新记录，不承诺完全零SQL变化，不造通用平台。
- 首版缺少当前版本索引时明确503 RECOMMENDATION_INDEX_NOT_READY并保留手选，不伪报NO_MATCH、不隐式回退旧向量。后台旧版本完成不得覆盖新版本，崩溃恢复/部分失败/数据删除进入必要回归。
- 仅更新概设与handoff，未调用Embedding、操作ES或改生产；纯向量产品取舍仍待确认。

### 2026-11-01 现有推荐优化：直接判断、取消需求补充（进行中）
- Owner：当前会话。用户暂缓向量新方案，仅记录；本次改现有单次ChatModel推荐Prompt，强化原文件名/后缀→格式线索→任务操作→技能用途推断，移除NEEDS_CLARIFICATION及推荐问题展示；不新增后缀映射/正文解析/Embedding/ES/Runtime变更，不部署。READY/NO_MATCH/NO_CANDIDATES及ACL、证据归属、409保护保留。
- 2026-11-01重新fetch：API 2a8a67c58c1949d671a4952bac496527ec1f3cea；Web b022d4ca05ff5d81cc6d84d863d8ec7f49563445。共享工作区相关路径脏/未跟踪且HEAD落后，不能安全复用其字节；使用本任务最少文件候选副本与临时index，不新建worktree、不覆盖共享源码/index。候选与证据：/home/isp/state/jyt-recommend-direct-20261101。
- 原型先行：唯一原型assignee-recommendation及prototype-spec移除补充需求状态；随后同步产品UI/解析与后端Prompt/解码。保留questions字段为空以限制DTO改动，不保留旧状态分支；非空问题视为不支持的模型结果。接口规范工作区v1.4及RB-01/02适用，后台/Runtime不联动。
- 最早验证：本机轻量解析/原型检查，正式API/Web回归走既有Flow。真实模型效果与结构契约测试分开报告，未获准不调用真实付费模型。
- 候选已自检合入develop：API ae4093b919a985a906107bcfc0d0457eaea943e7 / tree cb3a6d9ea5e6c714c178588ea5b839b5333115ff / 1.1.10-SNAPSHOT；Web 04c5240018eb4402194c84eb64f03e2f02192cbc / tree c7776c9de4e3ae6e9bdfca0b4931eae2d0f262e8 / 1.16.83。前端定向8项通过（62ms），SFC解析与模板编译通过；离线原型1440/390去问题状态、无匹配手选、加载禁用和无横向溢出检查通过，非生产验收。原型首次采集未找到详情卡，修正hash并补诊断后通过，未修改无关页面。
- 正式Flow准备使用当前云端配置，只固定本次SHA并关闭当次触发，不改测试策略/不加安装。后端嵌入策略550 argv包含recommendation.*、Controller和Model回归；每Run600秒限制，单独监控。当前尚无正式测试结果，不部署。
- 云端正式验证完成：API5260799/422 SUCCESS，平台create→update331秒，3401 tests / 0 failures / 0 errors / 160 skipped；Controller5、Service14、Model6共25项均执行通过。Web4403172/389 SUCCESS，平台113秒，3649 pass / 0 fail / 2 pending。初始start因source未齐为UNKNOWN，始终只读追踪同Run，无重复启动；两端均在600秒内终态。
- 已下载同Run制品，API包SHA e2f5a74c64e51f03f4bb15744fb1ed45cc6fae0a8f7d3d37fd2a952bea296c67，JAR receipt SHA08769a99d13b21ef21cfae476653ff34b8d90829d1faf5af77c3b11698d8161f；Web包SHA6d6a9ab241706c18ad9de67b726a338bf13c8f0e07a656d46ee7cf6b15eb83d4。固定commit/tree、报告/receipt来源核对，CI-only未调用主机安装。两端云端临时配置均CAS恢复并readback匹配前值。
- 汇总证据 /home/isp/wsps/cyf/specs/juyiting-assignee-recommendation/evidence/evidence-direct-recommend-20261101.json；完整证据 /home/isp/state/jyt-recommend-direct-20261101/final-verification.json。Prompt单独保留prompt.txt，SHA96353393a07f663c0e0bb333d14a7f26b86079c5d3e211ee07c1908140a2842b。真实Provider调用0，结构测试不等于后缀语义效果证明。
- 未部署、不改模型连接/凭据、ES/Runtime或用户事项；将来获准安装顺序API→Web，旧Web可读取新API状态子集，切换后不保留澄清分支。本次自己的预览进程已精确停止、浏览器profile已清理；候选副本/临时index收口，提交/patch/必要证据保留，不操作其他任务工作区。

### 2026-11-01 用户授权部署最新develop（本轮安装）
- 用户明确要求“部署develop最新代码”。19:00前后实时ls-remote核对API ae4093b919a985a906107bcfc0d0457eaea943e7、Web04c5240018eb4402194c84eb64f03e2f02192cbc，与已验证Run422/389完全匹配，复用制品，不新开Flow、不本机构建、不覆盖共享工作区。
- 安装顺序API→Web，既有锁/备份/恢复入口；旧API421、Web388。Web原版本612文件已锁内备份并tar compare通过，路径/home/isp/baks/cyf-web-flow/20261101-recommend-direct。API由既有受控安装器备份恢复。
- 初次主机协调脚本在任何安装操作之前因summary没有tree字段退出；改为从同Run receipt读取tree/JAR并交叉核对，原报告不修改，无重复构建或弱化校验。当前安装/在线结果待下文补记，模型调用0，不改模型配置或业务事项。
- 19:14完成安装/在线技术核验：API422安装exit0，版本1.1.10-SNAPSHOT/ae4093b，实际JAR08769a99与receipt一致、HEALTH UP/ATTESTATION MATCH，canonical8项通过；既有F06 schema校验两表均existing_equivalent，无新增手工迁移。Web389安装exit0，1.16.83/04c5240，612文件摘要核对，公网入口及聚义厅JS/CSS等8项资源与制品一致，入口引用关系通过。再次ls-remote两端develop未变。
- 未新增Flow运行、未本机源码构建、未真实模型调用、未操作用户事项/模型配置/Runtime。真实推荐语义验收未执行，不将健康或静态资源核验等同业务效果验收。汇总release/deployment-verification.json与规格evidence-direct-recommend-20261101.json；此前final-verification.json保留当时CI未部署事实，后续安装以本条和部署证据为准。

### 2026-11-01 推荐体验与宽松用途判断（进行中）
- Owner当前会话；用户四点：等待态去技术文案、避免技能判断过严、需求理解默认折叠、移除底部候选刷新图标。基线远端API ae4093b / Web04c5240，线上同提交。共享主工作区脏，最少候选文件在/home/isp/state/jyt-recommend-ux-20261101，不覆盖其他任务文件/index、不新建worktree。
- 原型先更新唯一prototypes/juyiting/assignee-recommendation.{js,css}及prototype-spec；随后Web仅展示改动，API仅Prompt和对应回归，无wire/数据库/Runtime/ES/连接配置变更。接口规范api/docs/interface-standard.md v1.4、RB-01/02。通用分析统计不要求独立专用技能，图片任务有可引用识图用途证据应推荐；仅生图或编辑用途不捏造识图能力，未知内容不等于无能力。保持权限、证据归属、409、单次无工具推理。
- 最早验证：原型390/1440、Web定向行为；重型回归仍Flow；本轮没有自动部署授权，不额外调用真实模型，不更改用户事项。
- 用户续需求：全部可选Agent交给模型逐一返回推荐度/理由。本轮单轨升级现有recommend接口，recommendations覆盖整个授权候选集（包括无公开能力证据者），新增recommendationLevel HIGH/MEDIUM/LOW/UNKNOWN；未知不冒充低能力，有无推荐由服务端据评级汇总READY/NO_MATCH，NO_MATCH仍返回全部评级。无候选才不调用模型。模型单次批量、无逐候选调用；无额外私有能力读取。
- 必要校验依据：防跨候选/伪造依据维持ID及available验证；完整评估语义要求每个输入候选恰好一行（重复/遗漏会误标已完成）；未知枚举不可推断显示；非UNKNOWN必须有可引用依据，UNKNOWN可空依据、不伪装支持。失败整次502，保持手选与显式重试，不后台补推理。已知权限/409仍由原服务负责。消费者同步useHallData、BountyPanel、地图推荐标记（仅HIGH/MEDIUM高亮）；低/未知不默认选中但允许用户手选。
- 本机定向19项通过（7秒）；自有浏览器核验原型1440/390，等级理由、默认折叠、NO_MATCH手选和等待禁用、无横向溢出。测试适配器补新模块导入；原型诊断导航/响应式重绘时序已改为目标状态等待，不改产品延时。已有18786预览属于其他任务，仅复用、不停止；自有浏览器/profile已清理。
- 自检非强制合develop：API0eb9fa93dc8eb5c75d1cf8612af059e6425a82ed/treead265c1732570ac4ec29a8a7b562f56a27f030f7/1.1.11-SNAPSHOT；Web5d2f713c6878bfda423f825a2475c9172d600090/tree880bd61552acdaf664b011c034f56f613a156e81/1.16.85。Web基于刚推进de927e1（其他任务点击修复）集成，保留其改动，不覆盖共享index/源码。
- FlowAPI423/Web391已固定候选运行，CI-only，保留必要回归及每Run600秒总上限。启动初始UNKNOWN只读追踪同run，无重复启动或主机安装。原配置快照与CAS恢复输入在/home/isp/state/jyt-recommend-ux-20261101/release；终态待补记。
- API423 SUCCESS（平台create→update343秒）。Web391 FAIL：3647通过、2pending、3处测试加载器未提供新增helper模块；保留run391/原始失败与恢复记录，不使用其制品。补齐三个现有SFC适配器及新等级/提醒文案fixture后，相关35项本机定向通过（5秒）；仅测试修复commitbea12d720b217183331e9e1e6294a47c1028b484/tree0c511603a55f7d479aaf638ab3be66f24908174a，产品版本仍1.16.85。
- 修正输入的Web392 SUCCESS（平台create→update105秒），两端均600秒内终态，无取消他人任务。API/Web云端配置均CAS恢复并readback匹配原值；无新主机安装，真实模型调用0。同Run制品下载/报告汇总中，不能据单测结构检查宣称模型推荐效果已验证。
- 最终制品核验：API423包SHA c3aa8bb5e480b86d31b4571968c06077871d967c0764c890b31f1d90821d6753/JAR51dc01dbdbedaf4857c4c0ca2fd147a228fbd0f800712366e6047d61c154c514，3402 tests/0 failures/0 errors/160 skipped，推荐及资料33项全通过；Web392包SHA469fbc59e5a8e0ac1897ed1881a796ac7badc94e350268f85a970096b5471173，3653通过/2pending/0失败，612个dist文件全量摘要一致。API下载触发传输超时后从同Run字节221461900以206续传，并校验完整包/JAR，不额外构建。
- 最终状态implemented_integrated_ci_verified_not_deployed。根证据specs/juyiting-assignee-recommendation/evidence/evidence-rated-recommend-20261101.json；完整final-verification.json、patch、Prompt、测试/制品保留本任务state目录。候选副本及临时index已精确收口，无worktree；共享生产源码/index及他人预览进程不动。真实Provider调用0，生产记录只读仍API422/Web389；本轮未安装、不改模型Key或用户事项。

### 2026-11-01 用户授权部署逐人推荐度与推荐体验优化（完成）
- Owner当前会话；授权“部署”。实时确认既有API5260799/423、Web4403172/392均SUCCESS，复用已核验不可变制品，未新开Flow或本机构建。固定API0eb9fa93dc8eb5c75d1cf8612af059e6425a82ed（1.1.11-SNAPSHOT）、Webbea12d720b217183331e9e1e6294a47c1028b484（1.16.85）；未追踪其他提交或覆盖共享工作区。
- 旧站点389在既有deploy.lock内备份至/home/isp/baks/cyf-web-flow/20261101-recommend-ux，612文件tar compare通过；API备份和恢复由现行受控安装器负责。首次安装会话exit143（SIGTERM来源未确认），在切换前中断，旧422记录及进程未变；保留interrupted-attempt.json，重新核验incoming摘要后恢复同Run下载，由独立持久主机会话继续原安装器，没有重复构建/绕锁。第二次安装exit0，不将第一次中断记为成功。
- API安装22:03终态exit0，22:04健康UP/ATTESTATION MATCH，实体JAR SHA51dc01dbdbedaf4857c4c0ca2fd147a228fbd0f800712366e6047d61c154c514，record Run/commit/tree匹配，canonical8项通过。既有F06 schema检查两表existing_equivalent；E05无精确授权未运行，无手工迁移。
- Web392安装exit0；公网入口开始返回已知旧缓存，第13次在既有安装器窗口内匹配本次index；未改缓存配置/放宽校验。22:07独立核验全部612个安装文件，以及公网index、入口/依赖、聚义厅JS/CSS共8项资源摘要和入口引用关系通过。
- 证据/home/isp/state/jyt-recommend-ux-20261101/release/deployment-verification.json，规格汇总evidence-rated-recommend-20261101.json同步；原final-verification.json及*-verified.json保留构建完成时未部署事实。未新增真实模型调用、修改用户事项/模型连接/凭据/Runtime；实际推荐语义效果仍未验收。

### 2026-11-01 截图去冗余与自有Agent优先（进行中）
- Owner当前会话；目标删除截图红框的推荐摘要/依据/重推区、通用告知及候选归属筛选，正常态以候选卡片和确认操作为主；加载/失败必要状态保留。模型判定双方满足需求时优先boundToMe=true，不提升不匹配/UNKNOWN候选；Web保留模型顺序。不改接口、ACL/快照/证据、模型配置、数据库或Runtime；本轮未授权部署。
- 远端2026-11-01重新fetch API0eb9fa93/Webbea12d7，线上同版本。共享主工作区脏且HEAD旧，复用上轮最小候选文件+临时index方式，不覆盖共享产品源码/index；证据目录/home/isp/state/jyt-recommend-clean-20261101，完整base commit/tree见source.json。接口规范api/docs/interface-standard.md v1.4；RB-01/02，仅Web展示和模型Prompt责任层。
- 原型先更新唯一web/prototypes/juyiting/assignee-recommendation，再实现产品；轻量定向行为与390/1440原型，正式回归用Flow，单Run600秒；不额外真实模型计费。

- 实现自检并合入develop：API efcb87549d332c5bfd5b18507b2524360d241263 / tree 0df2cea2d8bf2fd8fbfcf5a1e14cfec5b2e91f42 / 1.1.12-SNAPSHOT；Web 435c14c6158d585a4eef48722362dc57a2d73586 / tree 502af9c517355c88134472a609159a44f11654d6 / 1.16.86。Web定向13项通过（6秒）；原型390/1440无横向溢出，正常态删除摘要及筛选、NO_MATCH保留手选、错误重试及加载禁用通过。最初本机夹具缺hall.tmx/遗漏tsx加载器已按固定源码与既有入口修正，不是产品回归失败。
- 前后端CI-only正式Run API424/Web393；均固定上述完整源码，start响应UNKNOWN时只读跟踪已返回Run，无重复启动；监控仅本任务Run、达限受控取消。共享原型18786预览复用，测试浏览器已关闭，不操作别的进程。

- Web393 FAIL：3650通过、2pending、4失败，均为旧测试仍要求本轮用户删除的交办说明/能力依据/正常态重推面板。同步4个真实消费者测试到新交互合同，保留确认派单/归属/分页/失败重试断言；相关61项本机定向通过（12秒），未删测试或恢复冗余界面。测试修复提交Web 7b44dec7665d1e32bf02de119043e20fd55cbf58 / tree f6b1824d65656285e5ee595329c0c7aef91db207（产品版本仍1.16.86）已合develop；393失败与输入/配置/日志保存在release/run393，成功候选不得复用失败包。API源码未变，不重复API构建。

- 正式回归完成API5260799/424 SUCCESS（平台create→update418秒）、Web4403172/394 SUCCESS（127秒），均600秒以内。API {'tests': 3402, 'failures': 0, 'errors': 0, 'skipped': 160}，推荐相关33项全通过；Web 3654通过/2pending/0失败。两端固定commit/tree、同Run制品SHA与报告绑定核对通过，Web 612个dist文件摘要通过。
- 两端临时Flow配置均CAS恢复readback前值。已核验候选字节等于已推送commit后清理本任务candidate/base/index；必要patch、Prompt、截图、CI/制品证据保留。正式汇总specs/juyiting-assignee-recommendation/evidence/evidence-clean-recommend-20261101.json；API/Web均未安装，现行仍423/392；无真实模型效果抽测、用户业务写入、模型配置/Runtime变更。

### 2026-11-01 用户授权部署精简界面与自有优先
- 用户明确“部署”，Owner当前会话。只读复核固定API424/Web394均SUCCESS；复用既有已核验制品，来源完整commit/tree及摘要见/home/isp/state/jyt-recommend-clean-20261101/release/*-verified.json。旧线上API423/Web392记录保存至本轮release目录；通过既有锁/备份/恢复入口按API→Web部署，不新开Flow、不本机源码构建。
- 使用本任务持久主机会话，避免上轮终端会话SIGTERM打断安装；安装仍使用原受控安装器，不绕锁/ACL/摘要保护。主机启动不套用Flow600秒上限。当前执行中，后续终态/线上核验单独补记；不调用付费模型，不改用户事项、模型连接配置或Runtime。

- 23:12:49完成主机安装及技术核验：API424安装exit0，1.1.12-SNAPSHOT/efcb87549d，实体JAR SHA1f4dd69b7f04783f90b2a1e2cbac84ffd5aa1b4942c0a3d50c29ab3101ae59cd，与来源receipt/record一致；HEALTH UP、ARTIFACT_ATTESTATION MATCH，canonical8项通过。Web394安装exit0，1.16.86/7b44dec7665，612文件摘要及公网入口/聚义厅等8项资源摘要、当前入口引用关系通过；旧入口缓存第5次核验匹配新版本，没有改缓存配置或降低校验。
- 旧Web392备份/home/isp/baks/cyf-web-flow/20261101-recommend-clean，tar compare通过；API备份与恢复由原安装器留存。执行全程原锁/权限/完整性保护，未重开Flow、未本机源码构建、未改用户事项/模型配置/Runtime、真实模型调用0。此前CI未部署报告保留历史事实，部署证据release/deployment-verification.json及规格evidence-clean-recommend-20261101.json已同步；真实推荐语义效果仍未抽测。

### 2026-11-01 推荐候选默认折叠（进行中）
- Owner当前会话；用户授权更新原型/规格并开发，不部署。目标默认展示推荐人及理由、收起候选；更换后自动收起，动态点名确认；无合适推荐时展开且不默认选人。只改Web交互/文案，不改变模型排序、后端/Runtime/接口/权限和指派恢复机制。接口规范api/docs/interface-standard.md v1.4，RB-01/02。
- 远端fetch确认Web develop 7b44dec7665d1e32bf02de119043e20fd55cbf58/tree f6b1824d65656285e5ee595329c0c7aef91db207，线上Web394同版本。共享产品源码/index脏且旧，使用最少候选文件+独立index，不覆盖共享改动。证据/home/isp/state/jyt-recommend-collapse-20261101/source.json。
- 原型唯一入口web/prototypes/juyiting，先更新并验证390/1440后实现；最早轻量组件行为回归，正式Web Flow4403172测试构建上传，单Run600秒。无API Run、不调用真实模型、不部署。
- 2026-11-02 00:07实现自检合develop：Web69c2ccb0d7181ef614a1aa47df8f04f7972633c4/tree698121b2160a9cbb0cb0f2dd9d390bbdd3542ea5，1.16.87。产品只改BountyPanel与等级展示helper；默认折叠/手选自动折叠和焦点恢复/点名确认，未改API和排序。原型390/1440及长文案不溢出、错误重试/手选/加载禁用通过。共享原型规格另有原有修改，采用仅追加本轮段落，不覆盖其前值。
- 本机定向27项通过（20秒）。首次定位并修复watch注册早于computed初始化的问题；新测试夹具另按既有身份切换关闭详情行为重新打开，不改变产品身份隔离；此前失败日志保留。正式Web4403172/395已启动，UNKNOWN响应有明确Run395，只跟踪同Run不重复启动；本任务持久监控570秒受控结束以守600秒上限。未部署、真实模型调用0。
- Web395 FAIL（3654通过、2pending、1失败）：托管点将静态测试仍断言旧内联@click赋值，与新增选人自动收起/焦点恢复方法不符。更新该真实依赖测试为selectMatterCandidate，验证赋值/收起/焦点及不emit派单，原确认与候选权限断言保留；4项本机定向通过（23ms）。没有降低业务断言、跳过测试或使用失败制品。395配置已CAS恢复readback，状态及日志保留release/run395与web395-log.json。产品源码未追加改变，测试修复提交后重新固定CI输入。

- 2026-11-02最终完成：Web9a4e8b195b551af2b7e44797b29c8e7379c6f2e2/tree5898d46fafd2dfc756b76535d8fa82b3a610f37e（1.16.87）合develop，Flow4403172/396 SUCCESS（平台create→update224秒，600秒以内）；3655通过、2pending、0失败，同Run制品SHA 65a9fadeb987b70ee2e8e0b8a36ccb68cc8f21a565f93b4a47791d262e944ac5，612个dist文件完整摘要/固定commit/tree/版本/报告已核验。临时云配置CAS恢复readback匹配，不将395失败改标成功。
- 证据specs/juyiting-assignee-recommendation/evidence/evidence-collapse-recommend-20261102.json；原型390/1440、长文案、折叠/手选焦点通过。已核对候选字节等于固定Git提交后收口本任务candidate/base/index；保留patch、前值、日志、浏览器截图与不可变制品。不覆盖共享产品源码/index，不停他人原型服务。根文档增量更新，未声称根共享脏区整体提交。未部署、未调用真实模型、未改API/Runtime或用户业务数据。

### 2026-11-02 用户授权部署承办候选渐进展开（执行中）
- Owner当前会话，用户明确“部署”；仅Web1.16.87/9a4e8b195b551af2b7e44797b29c8e7379c6f2e2，复用Flow4403172/396测试构建成功的不可变制品，不新开Flow、不本机源码构建。原线上Web394/1.16.86；API/Runtime不变。
- 固定源码/制品、安装前记录及计划见/home/isp/state/jyt-recommend-collapse-20261101/release。沿既有deploy.lock备份旧站点及record，归档/home/isp/baks/cyf-web-flow/20261102-recommend-collapse；使用现行主机安装器，安装和公网资源核验分别记录。不改模型配置、不写用户业务数据或触发真实模型。

- 2026-11-02T00:30:49.560198+08:00完成：Web396安装exit0，1.16.87/9a4e8b195b551af2b7e44797b29c8e7379c6f2e2，来源SHA65a9fadeb987b70ee2e8e0b8a36ccb68cc8f21a565f93b4a47791d262e944ac5与现行record一致，612安装文件及公网8项入口/聚义厅资源摘要和入口引用关系通过。旧394备份/home/isp/baks/cyf-web-flow/20261102-recommend-collapse，tar compare通过。证据release/deployment-verification.json及规格evidence-collapse-recommend-20261102.json同步；CI未部署报告保留历史事实。未新开Flow、未本机源码构建、未修改API/Runtime/模型凭据或业务数据，未调用真实模型。

### 2026-11-03 推荐模型外延迟与专用模型配置（进行中）
- Owner当前会话；目标模型外总耗时<3秒，新增推荐专用模型/推理参数且默认继承全局；不自动部署、不切线上模型、不调用付费模型、不改Web/Runtime/HTTP契约，不上向量检索。接口规范api/docs/interface-standard.md v1.4、RB-1沿用。
- 固定API origin/develop 9aa75fcf0ab0f19935c766374b12d809effffc53/tree14d84adaad4faf93cb1d13d07b09274739db9580；线上452/1.1.16-SNAPSHOT；本次fetch远端一致。共享工作区HEAD旧且目标文件有他人修改，无法安全复用，使用唯一隔离工作区/home/isp/state/jyt-recommend-latency-20261103/api，branch codex/recommend-latency-20261103；不改共享index/源码。
- 已读日志样本55,989ms，其中模型32,037ms、模型外23,952ms；不是分位数。证据/home/isp/state/jyt-recommend-latency-20261103/{analysis.json,timing-evidence.log}。发现候选及技能版本查询间接构建完整Agent统计，推荐并不消费该统计；先收口轻量投影和重复读取并补阶段计时，不将猜测当实测。
- 最早反馈静态diff/调用点检查；正式必要Java回归/validateLayering走Flow5260799，600秒上限；真实模型外链路未测前不得标记3秒达成，不引入应用3秒强制超时。
- 源码候选33da2486eb2587a68ae1de2225bf76f1907e1d3d/tree e33aa0689ee6f2c3435480b1c131a2b7929dc991，API1.1.17-SNAPSHOT，已推任务分支；轻量diff及实际Spring AI2.0选项签名核对通过，不是Java测试证明。复用当前云端配置只固定本候选分支/commit，无主机步骤，已核对有效policy包含推荐/Skill全套、AgentServiceImpl、skillManagementContract、validateLayering与fresh bootJar。Flow5260799/453已创建，start返回UNKNOWN含真实Run453，仅只读追踪不重复启动；本任务持久watch按570秒受控结束保障600秒上限。不部署/不切全局或线上推荐模型。
- 静态调用链优化范围：旧推荐成功路径4次完整事项投影（主流程2次+候选枚举2次）改为2次必要事项投影+候选入口owner根读取；在原tenant=0历史统计路径，每个自有Agent两轮共6次无用统计装配（候选1+版本事务外1+内1，乘2）现为0次。仅为调用数分析，不是延迟实测。SkillAgentVersions的所有真实读取消费者复用同一无统计能力投影，身份/系统Agent/版本计算不变；相关技能事务夹具同步。未改认证基础层、资料读取、写入锁、HTTP字段或模型Prompt。
- 2026-11-03 14:42完成本轮实现/CI/集成：33da2486eb2587a68ae1de2225bf76f1907e1d3d已普通快进推送develop并远端回读一致；Flow5260799/453 SUCCESS，平台create→update405秒（600秒内）。3499次测试执行中3349通过、150既有条件跳过、0失败/错误；本轮必需的推荐36次及能力投影/技能版本/真实技能事务相关套件均0跳过，validateLayering与fresh bootJar通过。源码commit/tree、同Run报告、制品SHA ecf303ea29e6e1a4b21064f33a4d454395179b2ad69714930ff65e82649501b3及JAR SHA ed2873adc3f379c3017c58f493ef7002fa4f3a19595d7b7bd2de4e5b125a4893核验通过；云配置CAS恢复前值/readback一致，无第二次付费构建。
- 证据specs/juyiting-assignee-recommendation/evidence/evidence-latency-model-config-20261103.json，固定包/测试报告/配置恢复/集成回读保留/home/isp/state/jyt-recommend-latency-20261103/release。仅测试本地模拟Provider HTTP，无付费模型请求；未部署、未改线上模型/key、Web/Runtime/业务数据。**模型外<3秒尚未实测验收**；下一步须授权部署固定453制品后按真实请求的HTTP耗时扣除同请求模型耗时核验，记录候选/技能/附件规模，再针对剩余慢阶段继续优化。不能将静态减少调用数或本次云端测试成功当成3秒达标。
- 轻量`sddw check-docs juyiting-assignee-recommendation`未通过：该特性目录缺acceptance.md/design.md/integration.yaml/tasks.md四项旧入口产物，本轮未删除这些文件；保留真实失败于/home/isp/state/jyt-recommend-latency-20261103/docs-check-result.json，不为本次局部优化扩建规格文件或伪报文档检查通过。此结果与Flow正式Java/分层/制品核验分别记录。
- 已保存固定源码patch/commit/tree与有效证据，移除本任务唯一干净worktree和临时SDK只读解包；未改共享API工作区/index、未清他人工作区/生产备份。任务分支与develop中的固定提交保留。开发验证/合入完成，性能目标验收仍待部署与实测。

### 2026-11-03 推荐模型小样本选型（进行中）
- 用户在“确认网关支持后小样本比较，不直接切线上”建议后授权“好，继续”。Owner当前会话；仅同网关的合成数据模型比较，不部署、不修改配置、不写业务数据、不执行任务。复用既有state/model-comparison，无新worktree/Flow/构建。
- 固定Prompt及输入结构来自API33da2486eb2587a68ae1de2225bf76f1907e1d3d；共享工作区脏且HEAD不同，使用git show，不覆盖源码/index。模型连接复用Codex已配置同一网关与其现有凭据；本轮没有重新核对后端解密key相等，结果不冒充后端完整链路验收。
- 纠正上一条回复：官方网页工具返回空内容，不能称已核实Luna/Terra的官方定位或参数。GET /v1/models实际200，列出gpt-6-luna/gpt-6.1-terra，未列gpt-5.5；列表不等于生成可用。最初Python默认CA路径缺失导致TLS失败，显式使用系统现有CA bundle后成功，未关闭证书校验。
- 计划图片/PDF/混合附件各1例，复用生产Prompt，三模型默认参数对比，共最多9次真实调用；仅虚构候选、技能和附件名，无真实用户数据。不传未经验证的推理参数；记录返回model/usage/完整时延/JSON与有限语义断言。样本太少不计算P95或宣称稳定SLO；失败不自动重试，同模型连续失败两次停止剩余样本。证据/home/isp/state/jyt-recommend-latency-20261103/model-comparison。
- 小样本完成：真实8次调用，Luna/Terra各3次成功，gpt-5.5两次400 model_not_found后停止。Luna图片/PDF/混合8.951/13.580/11.548秒，Terra8.185/10.580/9.503秒；6个成功输出JSON、全候选/归属优先/证据归属/生成不冒充识图/UNKNOWN等有限断言均通过，人工核对理由未发现上述样本错误。这不是P95/线上全链路或更大候选集证明，不能与旧32秒日志直接做等量提速结论。未改模型配置。

### 2026-11-03 模型配置收回JAR（进行中）
- 用户明确要求核对/home/isp/hosts/cyf/api/application.properties并将配置合回JAR。范围仅本线程聊天/推荐模型配置，不迁移该文件内其他业务开关、身份/租户/授权或embedding凭据，不删除整个外置文件，不自动部署/重启。
- 实时只读发现外置spring.ai.openai.chat.model=gpt-6.1-sol（与早前记录不同），JAR内仍gpt-5.5；外置无jia.chat.recommendation.*。此次保持现有全局模型gpt-6.1-sol并收回prod源码，不借配置归并擅改为小样本胜出Terra。推荐专用配置保留可单独设定能力，默认继承。
- 远端develop核对06dc2a725249746eb0a0cc515c2d3601de0817b9，包含33da2486及其他已集成任务。共享api脏，采用隔离Git index精确修改配置/说明/版本，不覆盖工作区和共享index。固定候选后Flow测试构建JAR；部署授权前保留外置当前值，新包上线时仅移除重复模型键，保留其他配置和完整可恢复备份。
- 源码8c79a3752f232d78a51ceeab0459afa86a815831/tree040be4cbd6753e4e5da0c4a88d6eca5d0f022d96（1.1.18-SNAPSHOT）已普通快进合入远端develop并回读一致；只改prod配置、版本及既有推荐配置说明。静态校验三个模型配置键唯一，全局sol、推荐两项为空；未复制/打印密钥，未修改主机配置。Flow5260799/456已启动并回读RUNNING，CI-only固定候选，原云配置已快照，task-owned监控600秒以内受控终止。构建/制品核验待完成，不将合入当作JAR构建或部署成功。
- 纠正范围：用户随后明确要求“整个application.properties合回JAR、删除整个外置文件、推荐专用模型gpt-6-luna”。上段仅模型键方案被本次明确要求取代。旧候选8c79a/Flow456测试构建通过但未部署，保留release-model-only456及原source，不使用其包执行全量配置切换。
- 全量配置快照已受限备份到/home/isp/baks/cyf-api-config-merge-20261103/application.properties，SHA4d5bd77d5176a170f901f61ecab6a5a0a211c087179364d206a8c2bd8f966854，共122个唯一键，无续行；embedding key为原ENC密文，未解密或输出，不引入明文凭据。合入prod时同名20键使用原外置值，其他原prod值保留，新增推荐模型Luna；全量有效值等价检查通过。
- 新候选b5595c99cd07466489f24c1a51e1bcff50d88e35/tree3d711741212a94715f5a707ab79168104c06b6f7，1.1.19-SNAPSHOT。复用原任务目录/分支，无新worktree。生产已由其他任务更新到455/06dc2a，当前候选包含该基线，不回退其源码。按用户明确归并并删除外置文件要求，固定制品构建后用既有安装器安装；先保留旧外置配置确认新包健康，再在原发布锁/生命周期锁下备份删除整个外置文件并重启，失败恢复原配置后重启。当前尚未安装/删除；不改其他配置文件、数据库、Runtime/Web。
- b5595c99已普通快进合入develop；Flow5260799/457固定该源码执行。核对迁移涉及的索引列表：不存在旧prod独有列表项或标量/索引冲突，避免跨PropertySource列表覆盖合并后改变授权范围。实际进程prod profile、主机无其他application配置文件，现有音频Provider环境变量保留不动。上述检查只记录键/摘要，不输出值。
- 生产切换复用既有api-install-verified.py→cyf-api-flow-deploy安装器；另以一次性受限脚本调用既有cyf-api-kit锁继承合同，负责全量配置文件删除/失败恢复。不修改全局安装器或新增框架；锁冲突只停止协调，保持同Run制品、备份和JAR来源证明。Flow监控一次网络连接超时退出，重新只读跟踪同457，未重启流水线。
- Flow457 SUCCESS，平台create→update361秒；3507次测试执行、3357通过、150既有条件跳过、0失败/错误，推荐相关36次全通过，validateLayering/fresh bootJar与源码/制品摘要核验通过。制品SHA44c829bc4d6713acf35cb72baaecf3caf14667b2ca1501ad674bf081ba356f8c；JAR SHAca82129823f432b8cfaf597180bcedbab1ea801d1ade66d76ca3e95d67faf5c2。云配置CAS恢复/readback一致。解包原包后逐字节核对prod资源等于固定Git源码，全部122项等于原外置值，推荐Luna/全局Sol正确；一次性核验脚本最初未接受tar的./路径前缀已修正为唯一规范化成员，并重验通过，没有重建或更换制品。
- 主机安装前确认现行455源码为本候选祖先、外置摘要未变，保存previous-record后启动既有受控安装器安装457。外置配置尚保留，待新包安装/健康完成后执行删除与重启核验。不本机源码构建、不新增Flow、不迁移数据库、不修改Runtime/Web。
- **2026-11-03 16:11完成全量配置归并与上线**：457受控安装exit0，首次健康UP/摘要MATCH、canonical路径回归通过；随后在原发布锁/生命周期锁内确认快照未变，16:04:47删除整个/home/isp/hosts/cyf/api/application.properties并通过既有生命周期工具重启。16:10:46重启exit0、健康UP/MATCH，未触发恢复。
- 16:11独立核验PID2687906、cwd和-jar均canonical实体目录，prod profile、安装记录457/b5595c99及运行JAR SHAca821298...一致；外置路径不存在（包括无残留链接），无聊天/推荐模型或配置来源的CLI/env覆盖。全部122项已在JAR内保持原值，推荐gpt-6-luna、全局gpt-6.1-sol。密钥保持原ENC密文，不输出/改换/复制新凭据；其他外置配置、Web/Runtime/数据库未操作。
- 恢复资料：原外置完整字节/权限快照/home/isp/baks/cyf-api-config-merge-20261103，旧455 JAR备份沿安装record的backup/previous_sha256追溯；回退旧JAR时须同步恢复原外置配置，不能只回JAR导致缺失生产配置。源快照/提交流水/Cloud恢复/两个启动阶段分别保留，release-model-only456是被用户新范围取代的未部署历史包，不冒充本次成果。
- 根证据specs/juyiting-assignee-recommendation/evidence/evidence-config-in-jar-20261103.json；完整主机/制品/配置核验在state/config-in-jar/release/deployment-verification.json、packaged-config-verification.json、config-cutover.json、installed-verification.json。临时index/解包JAR已清理，无新增worktree、无遗留监控/构建任务；共享源码/index及他人修改未覆盖。**当前完成的是全量配置收口、模型设置及健康验收；未调用线上推荐接口，模型外<3秒仍未实测达标。**

### 2026-11-03 16:22 线上小样本性能实测（本轮只测量，不发布）
- Owner：当前任务Agent；范围为既有推荐HTTP性能/正确性，非目标为派单、任务执行、资金操作、配置修改或再次部署。核对现行API457/b5595c99cd07466489f24c1a51e1bcff50d88e35、PID2687906及JAR SHA ca82129823f432b8cfaf597180bcedbab1ea801d1ade66d76ca3e95d67faf5c2；共享源码脏区未改，源码分析使用git show固定版本。
- 复用测试账号PKCE及统一信封，经公网接口串行推荐既有open事项573（版本0，4候选），3次完整保留：HTTP15597/11756/10143ms；模型14906/11541/9896ms；HTTP减模型691/215/247ms。前两次200 READY，第三次502 RECOMMENDATION_INVALID_RESULT（CANDIDATE）。只读取/推荐，不确认承办。
- 两个成功样本平均13676.5ms，模型平均13223.5ms，占约96.7%；与历史单样本55989ms相比观测耗时少约75.6%，不是同输入受控A/B，不能单独归因换模型或宣称P95。
- 两次成功均优先推荐具备识图技能的吴用(HIGH)，没有要求额外成绩统计技能。第三次失败不能剔除；固定源码CANDIDATE表示未知/重复/不可操作候选，该链路构造canOperate=true，因此范围已缩小为未知或重复ID，但未保留原始模型输出，不能断言具体错字或重复对象。
- 同PID更早自然请求：16:12 HTTP38101ms/model31022ms，模型外7079ms；16:18 HTTP17107ms/model12977ms，模型外4130ms且502。模型外稳定<3秒仍未证明，不能仅凭本轮三个热态样本验收。候选/技能读取该时段各约1秒，本轮各约16–70ms；尚无逐SQL/调度证据确认根因。
- 优化建议优先级：先解决候选标识输出稳定性（请求内短引用映射、保留唯一性/覆盖/证据校验，结构化输出需验证当前网关支持，不自动重试掩盖失败）；再压缩重复技能免责声明和本领重复表示、精简输出，保留能力与隔离边界；最后对偶发非模型慢请求关联SQL/线程/GC证据，必要时在现有存储责任层做批量读取，不能删除前后快照保护。Luna保持用户指定，不擅自换模型/推理参数。
- 证据：/home/isp/state/jyt-recommend-latency-20261103/live-measurement/summary.json、timing-evidence.log、background-timing.log；受限权限results-private.json保留真实响应，无token/密钥落盘。此次没有构建、部署或源码修复。

### 2026-11-03 推荐输入精简实施启动
- Owner当前Agent；范围：请求内短编号、精简模型投影/Prompt、错误原因细分及定向回归；不换Luna、不改外部HTTP合同、不部署、不新增缓存/向量检索。权限/前后完整观察快照保留。固定基线远端develop=b5595c99cd07466489f24c1a51e1bcff50d88e35/tree3d711741212a94715f5a707ab79168104c06b6f7。
- 主工作区HEAD516267bf与远端不同且有并发大范围脏修改，安全隔离仅创建一个worktree：/home/isp/wsps/cyf-api-recommend-compact，branch codex/recommend-compact-20261103。Owner显式沿用根AGENTS、api/AGENTS及api/docs/interface-standard.md（基线b5595c99）；只修改推荐service/model/对应测试及说明。正式Gradle回归走既有Flow5260799，先本地diff/静态核对，不本机构建。
- 候选1cfbf7417659108b7fde72ca924d198c2d8335ab/treefaad154cc54d7861afbaf3ac7a47fcda60cdae4c，版本1.1.20-SNAPSHOT。实现保持完整Observation前后比较/HTTP投影，另装配短编号模型投影；候选编号A1，证据A1E1，精确反查服务器事实；未知/重复/不可操作分开固定原因日志。Prompt减少重复规则及免责声明，不改Luna/参数/重试，未知技能不猜测。
- 云效准备时其他任务458已结束但正在恢复配置，首次CAS检测CONFIG_CHANGED_NO_WRITE即停止写入；只读确认458 SUCCESS和当前配置后重新快照准备，不取消/覆盖他人Run。只修改当前云端bundle中本任务定向selector并固定源码、保留原云端工具与重型验证入口；原配置/候选/策略在state/jyt-recommend-compact-20261103/release。459 SUCCESS、日志103 tests/0失败/错误/跳过，validateLayering和fresh bootJar完成，主机未安装。原云配置CAS恢复/readback一致。制品正在独立下载核验，Run没有等待本机。
- 同Luna/默认推理、同网关的真实模型小样本对照：图片9.631→7.001秒，PDF9.266→6.829秒，混合12.899→8.008秒；前后各3次，合成4候选/同需求，PDF逆序交替调用；6次全部HTTP200并通过候选覆盖/证据归属/自有优先/生成非识图/UNKNOWN检查。平均10.599→7.279秒（减少31.3%），输入字符平均3664→2041（减少44.3%），prompt tokens平均2010→1266（减少37.0%）。这是模型直连小样本，不是线上HTTP端到端/P95，也不是失败率保证。使用现有Codex网关凭据，没有重做后端ENC密钥等价性比较，没有记录凭据或改配置。
- 17:19集成：期间远端develop增加c58a41a450（技能元数据发布管理）；无冲突合入后普通push develop=4ff35d7b87b344b3721f1d35575e7f18d5b08ee2/treec304d6bbbd176fa1ebd46422bfeee770c76dbdc9。自检相对远端仅本任务6文件，推荐生产/测试源码与459完全一致，保留并发7文件。**459绑定1cfbf741，不冒充4ff35d7b集成包；本轮不为合并重建，下一次授权发布须按实际最终commit构建/验证，不能把459包作为最新develop包安装。** source.json与integration.json分别保留两者，未修改共享主工作区/index。
- **17:24制品核验完成**：459候选103项全部通过，其中推荐Controller5/Service16/Materials7/Model9共37项；source/tree/同Run/JAR及制品摘要闭包通过。制品SHA1ff68c6ee50f7c7063bead56d6752a8b3363065c2293cb1be4285fa8c6532be4，JAR SHA165fdf15d681a92b81c294036bee78a60a96603c2db7cc815b3071563756dce2。精确记录release/api-verified.json；根汇总specs/juyiting-assignee-recommendation/evidence/evidence-compact-model-input-20261103.json。已保存补丁、原提交和并发集成记录，移除本任务唯一干净worktree；未清理他人目录、未改主工作区/index、无遗留watch。当前完成开发/候选验证/合入/合成模型对照；尚未发布，线上模型外偶发慢请求与部署后的端到端效果仍需单独核验。

### 2026-11-03 17:47 合入后候选验证接续（不部署）
- 用户“继续”按上一轮待完成的集成候选构建/验证推进；Owner不变，不推断生产安装授权。本次固定远端develop=4ff35d7b87b344b3721f1d35575e7f18d5b08ee2/treec304d6bbbd176fa1ebd46422bfeee770c76dbdc9、版本1.1.20-SNAPSHOT。459是1cfbf741源码制品，不能冒充本次集成树；实时查询最近为459/458 SUCCESS，无现成相同集成源码Run。
- 不再创建worktree、不改应用源码或共享脏index；从api Git对象读取固定build.gradle及变更。复用既有Flow控制/校验入口，单次5260799覆盖推荐Service/Materials/Controller/Model与并发合入的技能发布/元数据Mapper/推荐技能/Position事务回归、validateLayering和fresh bootJar；仅云端测试构建上传、600秒上限。不重复付费模型调用，先前Prompt对照仍适用于字节一致的推荐代码。
- 本轮源码/云配置/测试/制品证据固定在/home/isp/state/jyt-recommend-compact-20261103/integrated/，原459证据保留不覆盖；线上安装与端到端验收仍未执行。
- 460终态FAIL（未发布）：推荐37项及并发技能发布/Mapper等通过，PositionSkillTransactionTest9项均在setup失败：缺少CYF_POSITION_TEST_JDBC。归因为Owner装配集成定向策略时遗漏该专用云端MySQL夹具，非推荐代码错误；失败日志/诊断完整留在integrated/release，failure-460.json固定根因。不能使用该Run产物，不删除/跳过9项测试。
- 修复仅CI输入：从已成功458候选复用岗位事务的worker隔离MySQL准备（独立临时datadir、随机loopback端口、核验已有MySQL归档、准确子PID退出清理）；只导出本测试所需CYF_POSITION_TEST_*，不访问生产库。460原云配置已CAS恢复；修正候选在integrated/release-fixture，应用commit/tree和全部测试选择器不变。先bash -n与来源核对，变更夹具后再启单一Run，不是原输入盲重试。
- 461 SUCCESS：固定4ff35d7b集成源码，132 tests / 0 failures / 0 errors / 0 skipped；推荐37项、并发技能/岗位/Mapper29项，构建依赖验证66项。PositionSkillTransactionTest9项全部实际通过；不重标460失败，不改变业务源码或删测试。第一次监控460遇到一次ServiceUnavailable后仅恢复同Run只读查询，没有重启或误取消流水线。461观察至终态约161秒，小于600秒；云配置已CAS恢复并readback一致。
- 合入后制品正在由本机下载/核验（integrated/release-fixture）；Flow已结束，不承担本机等待。此次没有新增worktree、没有Gradle本机执行，没有部署、重启、配置切换或生产数据库操作。原459候选及460失败证据继续保留，不能互相替代。
- 轻量文档入口检查sddw check-docs juyiting-assignee-recommendation返回FAIL：该特性目录缺acceptance.md/design.md/integration.yaml/tasks.md，结果已存integrated/docs-check.txt。这是既有文档入口完整性缺口，不是源码/CI回归失败；本次没有为局部验证补造设计/验收事实或扩大成文档框架整理，不声称文档检查通过。
- **18:04集成制品核验完成**：Flow5260799/461绑定4ff35d7b/treec304d6bb/1.1.20-SNAPSHOT；同Run源码/干净树/测试/制品/JAR闭包全部通过，132项无失败/错误/跳过，包含推荐37与并发集成29。制品SHA784c9a1e1f58572aad24075daed8f4429a0e8085e1c961b8925cb1ab3c75b20c；JAR SHA3ed26b857762deff2d0e76932753a5f2230c45f2fa5a2e8773c45ee71c6afe3b。
- 本机下载首次会话exit143中断，保留221232525字节partial；未再启动Flow，沿同461不可变制品以Range续传并验证206/offset，最终223873926字节，完整SHA核验通过。没有冒充旧459候选制品、没有修改460 FAIL状态。
- 最新汇总integrated/completion.json，固定发布材料integrated/release-fixture/api-verified.json、api-artifact.tgz、api-receipt.json、api-summary.json；根特性证据已增补集成成功记录，保留原候选历史。**当前已具备精确集成源码的受测制品，未安装、未改生产配置。后续获授权发布同一4ff35d7b候选时复用461包，不重复付费构建；安装前核对线上状态/来源/备份锁，再做真实HTTP耗时与推荐正确性验收。**

### 2026-11-03 18:46 固定461部署与实测（已安装，业务验收未通过）
- 用户“继续”承接上一轮“是否现在部署并线上复测”，授权固定461安装和仅推荐复测。安装前实时线上458/c58a41a，核验为4ff35d7b祖先，保留并发技能发布；使用现成461不可变包，没有新增Flow、本机构建、外置配置或Web/Runtime重启。
- 复用受控cyf-api-flow-deploy，保留原发布锁/备份/恢复，installer exit0。API1.1.20-SNAPSHOT/4ff35d7b/treec304d6bb，JAR SHA3ed26b857762deff2d0e76932753a5f2230c45f2fa5a2e8773c45ee71c6afe3b，PID2780007；HEALTH=UP/ATTESTATION=MATCH，canonical回归通过，cwd/-jar实体路径正确、prod生效；全局Sol/推荐Luna仍在包内，无外置application.properties或模型参数/环境覆盖。备份及安装详情见integrated/release-fixture/deployment-verification.json、install.log和previous-record.json。原下载包被安装器校验转入incoming并回收冗余下载，原artifact.tgz路径不再存在，不以路径缺失要求重建。
- 真实同一自有事项573/version0，JPG成绩图片，4候选；3次依次HTTP200/409/502。总耗时20.819/10.211/6.069秒，模型15.672/5.982/5.097秒，客户端总耗时减模型耗时=5.147/4.229/0.972秒。首轮启动后请求保留；第2轮stale后先只读查技能，再执行原计划剩余第3轮，无自动重试、确认承办、派单、执行或扣费操作。
- **验收未通过，不能宣布提速或模型外<3秒达成。** 第1轮识别图片统计需求，但吴用识图证据不可用、被评UNKNOWN，林冲MEDIUM居首；后续两次技能查询均显示识图enabled/NOT_EXECUTABLE。这是动态技能证据问题，不等于模型未识别后缀，也不能据后续状态倒推首次具体失败原因。
- 第2轮日志已进入后置observe后才stale，可确定任务版本/标题/描述/状态比较已通过、候选/证据快照变化；具体字段无日志，不能断言一定是心跳。第3轮快照通过后模型结果CANDIDATE_COVERAGE，确定漏评候选，原始模型输出未记录，未知漏了谁。保留完整校验，不伪造缺失推荐、不移除权限/证据归属。
- 模型外瓶颈集中候选证据装配：首轮两遍1.922+1.701=3.623秒，第2轮后置证据2.318秒/候选0.921秒；第3轮模型外0.972秒，表明有波动，不能把一次热态当稳定达标。候选逐Agent读取技能，在线身份/目录重复查询及全量产品读取是下一步定向分析点，尚未证明各SQL或CPU占比，不擅改公共层或Runtime。实时主机有并发工作，未操作其他任务进程。
- 证据：/home/isp/state/jyt-recommend-compact-20261103/live-measurement/summary.json、timing-evidence.log；受限results-private/skills-before-private/skills-after-private保留原样，token未落盘。旧457两成功平均13.6765秒与本轮成功20.819秒不构成提速证据；能力状态/负载/时点不同，合成31.3%不能替代本次线上结论。
- 下一步应聚焦证据读取与快照变化定位、模型完整覆盖约束；本轮不擅换Luna、不进行额外付费模型样本或重建。部署成功与业务/性能验收失败分开记录。

### 2026-11-03 19:17 稳定性与证据读取优化启动
- Owner当前Agent；用户授权继续优化，范围为推荐证据读取、推荐快照语义和模型覆盖，不改Web/Runtime/执行准入、不更换Luna、不部署。线上461/4ff35d7b；实时远端develop同4ff35d7b/treec304d6bb。共享api HEAD516267bf且目标SkillManagementService有并发脏改，不能覆盖；唯一任务隔离worktree /home/isp/wsps/cyf-api-recommend-stability，branch codex/recommend-stability-20261103，基线固定4ff35d7b。显式沿用根AGENTS、api/AGENTS、接口规范api/docs/interface-standard.md@4ff35d7b及RB-1，非全链重构。
- 最早验证：静态调用扫描+现有网关gpt-6-luna严格JSON Schema必要字段探针（1次），输入故意要求只给A1，实际四个required键全部返回，HTTP200/3.561秒；证明当前路由支持此样例，不宣称所有业务正确。凭据在内存，输出只合成数据。证据/home/isp/state/jyt-recommend-stability-20261103/schema-probe.json。官方文档/源码网络读取未取得正文，实际SDK2.0.0将通过生产包类签名和云端HTTP请求测试核验，不据记忆写SDK参数。
- 拟实现：单观察批量入口共享产品/已批准版本、按Agent批量已有授权读取，空技能跳过运行目录；一份已认证运行目录对应一轮观察，删除内层重复整目录比较造成的CHANGED（外层模型前后事实复核保留）。模型输出按固定候选键必填+模型rank排序，API还原原HTTP数组，明确漏项/未知项/证据错误仍失败；未知Provider不静默降级。增加快照原因分类日志，不记身份/Prompt/原始输出。性能无硬deadline。
- 回归：推荐Service/Materials/Controller/Model、技能推荐、必要SDK实际HTTP参数与定向管理事务回归；重型测试、分层、fresh JAR在Flow5260799固定候选执行，遵守600秒。先修复并合入受测候选，生产验收和发布单独记录，不承诺<3秒已达成。
- 源码24a472bf806ea2b164e14df133d19a6ba6158a31/tree2341a6e001b32cd7247455fd395594c58a2e96fb（1.1.21-SNAPSHOT）已push任务分支；静态检查通过。注意既有authorizationsForAgent关联市场installation，不保证原生岗位安装存在；因此本次仅新增activeAuthorizationsForAgent，在存储责任层按managed_state.active_installation_id联接授权，tenant/client/agent作用域保留，配真实H2/MyBatis原生/市场/跨scope回归，未复用不适用查询或补造购买事实。
- 请求级结构化样例3次HTTP200：图片6.956秒/PDF6.464秒/混合6.893秒，完整候选/证据归属/自有优先/仅生图不等于识图/UNKNOWN断言全通过；不是线上性能/P95或失败率保证。Spring AI生产包2.0.0已核验outputSchema进入JSON_SCHEMA且SDK写strict=true；云端回归包含实际HTTP请求断言。没有更换Luna或改变推理设置。
- Flow协调：首次检测他人462 RUNNING不写入；空闲准备后发生其配置恢复，CAS报CONFIG_CHANGED_NO_WRITE，保存旧准备快照后重读。20:03本任务candidate更新成功，随后start返回FLOW_API_REJECTED（无本任务Run ID）；只读查询新463来源是codex/skill-catalog-consolidation-20261103，明确不是本任务24a，不使用/取消它、不伪称启动成功。当前不覆盖在途配置，等待对方终态及恢复后再核对源码/固定配置。错误与请求上下文在release，未盲重发start。
- 自检进一步去重：严格JSON解析已拒绝重复键，解码不再二次检查同一候选重复/未知；rank只要求可排序整数，不为名次跳号增设失败门槛。同rank稳定排序。候选00b61e3424未单独构建。
- 并发463成功并将767d631e1edfd4e0c59acabdff68cc523fceeef5合develop，涉及技能退市；本任务在正式构建前合入，冲突仅推荐技能方法，保留“已退市不作为推荐发现、已安装仍可管理/执行”的并发语义，旧事务测试适配新的批量Java端口、断言不变，并新增批量退市回归。固定集成62ba7b942e06d73b5253d9b9debb3a35d8f7e82d/treeeeb5ee485938bb29c3351a8cf57388f44dec89bd，1.1.21-SNAPSHOT；未碰他人worktree/主工作区。
- 他人463结束恢复到本任务先前candidate后，本任务CAS恢复原develop配置，readback一致；旧协调记录单独保留coordination-before-integration。重新基于当前原配置装配固定62ba7b，Flow5260799/464返回真实Run ID，初态INIT sources空记UNKNOWN后仅查同464，已RUNNING；不盲重启。测试加入原生/市场批量Mapper和技能退市真实事务用例，worker私有MySQL夹具显式存在，不重犯460缺fixture；600秒task-owned watch在运行。当前未部署。
- **20:20正式完成候选验证/合入**：Flow5260799/464 SUCCESS，create→update192秒（观察终态212秒），145 tests/0 failures/0 errors/0 skipped，含推荐Controller5/Service19/Materials7/Model9共40、技能批量8、原生/市场批量Mapper1、技能退市真实事务1及并发集成回归；分层、fresh JAR、源码干净及制品闭包通过。严格Schema实际SDK HTTP字段及默认options不被修改均通过。一次监控会话exit143后仅恢复同464只读监控，未重复构建。
- 同62ba7b942e/treeeeb5ee48/1.1.21-SNAPSHOT普通快进push develop且readback一致，保留767d631e并发技能退市语义；无二次集成树变化，不为合入另开付费Run。云配置CAS恢复原develop/readback一致。最终制品SHAac776c419882e04d555ddd679e646a0b1cbd1a33e67ea3add9e8562da13b1670，JAR SHA82bae8a393036173d359713108b45383b7efd5d1666142b72aa947595165850f；本机完整下载并核验，没有安装。
- 模型三样例平均6.771秒，严格Schema增加输入token（平均1657），不宣称token/费用下降，也不将合成样例当线上HTTP/P95；本候选模型外3秒尚未测量，上一已发布461结果失败保持。证据为/home/isp/state/jyt-recommend-stability-20261103/{completion.json,model-summary.json,release/api-verified.json}及特性evidence/evidence-stability-20261103.json。没有自动重试、放宽缺项/跨证据校验或切换模型。
- 唯一worktree源码已提交/push，必要补丁存state/api.patch；按任务收口移除干净隔离工作区，不改共享api/index或其他worktree。后续若授权发布本62ba7b，直接复用464固定制品并做真实推荐复测，不重新构建；此轮“继续优化”未扩成生产发布授权。

### 2026-11-03 20:47 固定464部署与真实推荐复测
- 用户“继续”承接部署固定464并线上复测的确认；仅发布本已验证候选，不重新构建。安装前实际线上463/767d631e，已确认其为62ba7b942e祖先，保留并发技能退市内容。既有受控安装器exit0，备份/锁/恢复不变，未修改Web/Runtime或外置配置。
- 当前API1.1.21-SNAPSHOT，Flow5260799/464，commit62ba7b942e06d73b5253d9b9debb3a35d8f7e82d/treeeeb5ee485938bb29c3351a8cf57388f44dec89bd，JAR SHA82bae8a393036173d359713108b45383b7efd5d1666142b72aa947595165850f；PID2855106、HEALTH=UP/ATTESTATION=MATCH，canonical回归通过。prod、实体cwd/-jar正确；包内全局gpt-6.1-sol/推荐gpt-6-luna，无外置application.properties及模型环境/参数覆盖。安装证据/home/isp/state/jyt-recommend-stability-20261103/release/{previous-record.json,install.log,installed-verification.json,deployment-verification.json}。原下载包经安装器处理，不因旧下载路径消失重建。
- 同自有open事项573/version0，保留启动后首次推荐，3次串行均HTTP200 READY且4候选完整；总耗时17.361/7.375/7.211秒，模型15.070/7.047/6.894秒，客户端总耗时减模型为2.291/0.328/0.317秒。模型外三样本均<3秒，后两次均值0.3225秒；不宣称稳定SLO/P95或受控A/B提速比例。未自动重试、确认承办、执行或扣费。
- **语义验收仍未全通过**：三次均识别图片成绩需求、吴用识图证据available=true；前两次仍把仅资料分析/文档处理的林冲排在吴用之前，第二次还给林冲HIGH且未指出读图缺口；第三次识图优先正确。所有候选均自有，本轮不能验证自有vs外部偏好。接口稳定性/候选覆盖样本通过，不掩盖排序问题。
- 下一步应让Prompt更明确“读取资料是后续分析的前置能力”，通用统计/文档技能不自动证明可读取图片；依旧由模型判断，不在代码硬编码后缀或改写评分。本轮仅部署/复测，未偷偷修改线上Prompt或另启构建。详情/home/isp/state/jyt-recommend-stability-20261103/live-measurement/{summary.json,timing-evidence.log}，受限原响应results-private.json；旧461失败事实保留。

### 2026-11-03 推荐读取前提Prompt优化启动
- 用户授权优化，不含本轮新候选部署。Owner当前Agent；只修改推荐模型Prompt/定向测试及业务规格，不改HTTP、评分代码、Web/Runtime、模型或配置。根/api共享工作区有他人脏改，复用无安全空间，创建唯一隔离worktree /home/isp/wsps/cyf-api-recommend-reading，分支codex/recommend-reading-20261103；远端develop读取基线cd548fa6fa71679dea294193b4c52ee04ba339e2，包含前轮62ba7b及并发回复修复。
- 契约沿用api/docs/interface-standard.md（固定基线cd548fa6fa）；RB-1模型判断能力/排序，API只供本次证据及验证引用，不写文件类型映射。读取是必要附件处理的前提；简单统计不设专用技能门槛；自有优先只适用于满足核心需求者。已给足文本/只需摘要/文件名任务不额外要求正文读取。已删除技能不作为当前证据，合成通用分析反例不冒充用户当前真实配置。
- 最早验证：Prompt传递及隔离选项的定向ModelTest；独立小样本真实Luna语义检查覆盖读取前提、自有优先、复合技能、混合附件和无需读取例外；重型回归/分层/fresh JAR走固定Flow，不本机构建。官方Prompt文档工具本轮未返回正文，不依赖未读取文档改变SDK参数。
- 候选e2e33bc67ccfd25033748726a997aed81e873cce/tree321fd3418539f168a33e685436fa20712111d822，1.1.23-SNAPSHOT，已push任务分支。8组真实Luna模型语义样例全部通过，平均10.612秒；仅合成样例，不是新线上快照、P95或提速证据。案例存API测试资源recommendation-reading-cases.json，原输出/断言在/home/isp/state/jyt-recommend-reading-20261103/model-samples.json，不存凭据。
- 本任务初次本地配置准备脚本未匹配已有bundle的validate=True，外层shell未启用失败即停，导致准备失败后仍应用旧候选并启动468。该Run不作为验收，已核对本任务返回ID/分支后受控停止，终态CANCELED，观测234.552秒；未取消他人Run、未部署。证据release/canceled-468保留。修正解析并让本地及worker固定提交校验都在set -e后执行；精准范围只含推荐Service/Materials/Controller/Model、分层及fresh JAR，移除该范围不消费的worker MySQL/Runtime准备。归因是任务协调脚本错误，不是应用回归失败；不隐藏无效Run开销。
- **22:19正式验证/集成完成**：Flow5260799/469 SUCCESS，create→update103秒，观察终态121秒，106测试全部通过（推荐Service19/Materials7/Controller5/Model9共40，其余构建依赖回归），分层与fresh bootJar实跑；测试任务/validateLayering/bootJar均无skip/failure。精确e2e33bc67c/tree321fd341/1.1.23-SNAPSHOT已普通快进push develop且远端readback一致，无需再次构建。云配置CAS恢复原develop/readback一致，原468 CANCELED不改写。
- 制品SHA7defe03481ebce27d21b621e9340eb11e2a7ec311127676526e0071a03b48261，JAR SHA6894b690882b87e303192d4d69723be2882a685ff26d0df5a312ccf6597c7ae8，同Run来源/干净源码/测试/摘要闭包通过。首次下载传输超时停在218033547字节，沿同469固定制品Range206续传至223888850字节并验证完整摘要，没有重开构建。
- 未部署，未访问真实推荐或更改线上技能。8组模型样例仅作Prompt语义证据，不能宣称线上3秒或稳定准确率；开发与合入完成，生产验收待授权。后续固定469包在/home/isp/state/jyt-recommend-reading-20261103/release/api-artifact.tgz可复用；主机安装仍需核对当前版本不回退他人更新，沿正常锁/备份/恢复流程。完整汇总completion.json及特性evidence-reading-20261103.json。
- 任务隔离worktree已在确认干净且源码push后删除，差异保留state/api.patch；模型样例runner已改为从固定source.json commit读取源码/测试资源便于追溯，不依赖已删除worktree。共享api工作区及其他任务修改未动；根文档仅定向更新，未整仓提交。

### 2026-11-03 22:42 固定469授权部署
- 用户明确“部署”，复用469/e2e33bc67c/1.1.23-SNAPSHOT已验证不可变包，不开Flow、不本机构建。实时线上467/cd548fa6fa为候选祖先，核对保留其临时回复语义/计时改动；不退回前轮464。安装前保存release/previous-record.json，逐项验证本轮四组推荐回归、分层/fresh JAR及制品来源摘要。
- 沿既有cyf-api-flow-deploy主机受控安装、锁/备份/恢复；不改外置配置、不重启Web/Runtime、不执行数据库手工迁移。安装与线上健康/配置核验分开记录；本次部署不复用旧模型样例冒充实际业务/性能复测。
- **22:51安装/线上技术核验通过**：受控installer exit0，API1.1.23-SNAPSHOT/e2e33bc67c/Flow469，JAR SHA6894b690882b87e303192d4d69723be2882a685ff26d0df5a312ccf6597c7ae8，PID2932716；HEALTH=UP/ATTESTATION=MATCH、canonical回归通过，prod及实体cwd/-jar正确。包内全局Sol/推荐Luna，无外置application.properties或模型环境/参数覆盖。服务正常冷启动后才记成功，未追加应用启动硬截止或中断。
- 既有安装器F06 hook报告existing_equivalent，E05未授权未调用；无新增手工迁移/功能激活。备份路径和恢复来源见release/deployment-verification.json、previous-record.json、install.log。原下载包按安装器校验入库/回收，不因下载路径消失重建。
- 本轮只部署并完成技术核验，没有实际调用推荐、确认承办/执行或新增模型样本；业务排序及耗时仍需当前任务与当前技能事实实测，先前8组合成通过不冒充本次线上业务验收。completion及evidence-reading更新安装层状态，保留468取消与469正式测试来源。

### 2026-11-04 外部接单技能推荐摘要
- 用户“好，执行下去吧”授权补齐外部接单候选技能摘要；Owner当前Agent。只改API推荐输入与现有接单权限发现链路、测试和规格；不改Web/Runtime、HTTP字段、模型、评分规则、安装/接单开关或发布生产。唯一隔离worktree /home/isp/wsps/cyf-api-recommend-external（共享api有他人脏改），分支codex/recommend-external-20261104，基线origin/develop509325a971ed7478fcd60d3370bebae26185349a。统一接口规范固定该commit的api/docs/interface-standard.md，沿根AGENTS最新兼容/职责规则，不沿旧组件文档扩大校验。
- 授权由既有ExternalServicePolicy候选SQL负责：同tenant/client、有效绑定、非SYSTEM、本人或最新接单开关开启。新增仅内部recommendationCandidates投影复用该SQL分页，并携带可信provider owner供能力目录隔离；不另开HTTP查询外部技能，不伪造provider Actor，不给管理接口放宽readOwned。原公开候选字段不变，内部owner字段JsonIgnore且不写模型输入/HTTP结果。
- SkillManagement批量推荐读取消费上述可信候选，自有/外部共享一次产品/版本读取；外部仅已启用安装且产品仍公开的用途摘要，使用提供方真实owner的当前会话fence核对可引用状态，不读取技能正文、文件、凭据、私有本领或历史成果。provider证明不一致不输出旧安装摘要。HTTP外部依据只给序号引用/名称/公开用途/运行状态/可引用性，隐藏installationId/skillKey/version；model仍用请求内短编号。
- 模型前后重新发现候选及读取技能，关闭接单、身份提供方变化、技能改变按原409失效；不靠新超时/缓存掩盖。最早定向验证覆盖推荐输入/返回脱敏、外部provider目录隔离/禁用/退市、真实MySQL接单绑定/跨scope/关闭开关与分页；保持现有管理权限。源码边界RB-1业务权限API、目录隔离适配器、模型判断，不扩大到Web或Runtime改造。
- 固定候选1d8b15c1e987286c5a09f4ef1a8aae104ad23f0e/treea94c175a3b7ec186450e42c07a3bcb2533960330，API1.1.24-SNAPSHOT；已push任务分支，静态diff检查通过。Flow5260799/476已取得真实ID，初态sources未齐记UNKNOWN后同Run观察RUNNING，600秒受控watch。范围：推荐Service/Materials/Controller/Model、技能摘要、AgentService候选调用、接单策略unit及真实MySQL绑定/跨scope/开关、退市后保留管理的事务回归、validateLayering/fresh JAR；使用现成worker MySQL/岗位夹具，不本机Gradle。
- 内部候选DTO新增JsonIgnore提供方字段，仅AgentService→推荐服务→技能摘要读取使用，未被Controller直接返回；公开TargetSummary/HTTP推荐Result仍由原结构装配。模型前后比较内部技能事实与provider owner，删除同责任层再次比较派生evidence的重复检查；不能用公开脱敏序号替代真实变化检测。新增外部甜点技能案例验证模型得到名称/用途且前端依据不带private owner/install/key/version；未知信息不猜测。
- 首次正式Flow5260799/476 FAIL：编译通过，142测试中仅AgentServiceImplTest旧断言失败（内部record仍断言2字段，新增提供方后为3）；同时修正同用例仍验证旧public candidates调用的问题。不是权限用例失败，未放宽权限/业务断言：改为验证真实提供方字段及recommendationCandidates调用。MySQL16项、安装事务1项、推荐Service21项、技能摘要10项均已通过；失败Run不作为交付证据。原云配置CAS恢复。
- 修正候选b71b559fe8527daac7b44e66856c095b70d46e01/tree0a898e68fbe19b9c6d9f4d475a45d47bdd8daeb5，Flow5260799/477重跑原完整定向范围。启动响应INIT身份尚未就绪，按返回477只读跟踪，不重复start；每Run按600秒上限监控。不部署。

- **08:52验证/集成完成**：Flow5260799/477 SUCCESS，create→update163秒（观察终态177.612秒），142测试全部通过、0失败/错误/跳过；其中本轮9组业务范围76项，其他构建依赖66项。validateLayering及fresh bootJar实际执行，构建84.073秒。完整commit/tree、干净源码、同Run receipt与制品摘要已核验；原476失败保留。
- 已将b71b559fe8527daac7b44e66856c095b70d46e01普通快进push API develop，远端readback一致；无覆盖共享api的并发修改。云配置CAS恢复原值并readback；477初始UNKNOWN响应另以精确source只读核实成功，没有重复start。
- 固定制品`/home/isp/state/jyt-recommend-external-20261104/release/api-artifact.tgz`，SHA946302df0f6420207c53e572934ceec712859322c496828505b578e98585b256，JAR SHA3f9e8679ac5c2339c710bfc20e93e36246ca1310b8624b1236c1b5f6b471ef9b，版本1.1.24-SNAPSHOT。未部署、未访问真实推荐/扣费或修改线上技能；外部真实Agent效果与新增读取耗时待获授权发布后核验，不宣称线上已修复或模型外稳定3秒。
- 稳定知识已回写既有runbook、规格及evidence-external-skills-20261104.json；源补丁state/api.patch、失败/成功证据和completion.json保留。根文档已有并发/未提交内容，仅定向更新，不整仓提交、不改共享gitlink。完成保存后删除本任务干净worktree，后续部署复用固定477制品且先核对并发上线版本，不重新付费构建或回退他人变更。

### 2026-11-04 08:57 固定477授权部署
- 用户明确“部署”，复用已验证477/b71b559fe8/1.1.24-SNAPSHOT，不再开Flow或本机构建。安装前实时线上475/509325a971、HEALTH=UP/ATTESTATION=MATCH，为候选祖先；保存previous-record.json，无并发更新回退。
- 主机既有受控安装器exit0，备份/锁/恢复机制保留。实体JAR SHA3f9e8679ac5c2339c710bfc20e93e36246ca1310b8624b1236c1b5f6b471ef9b，来源477及commit/tree一致；新PID3238459，健康UP、产物MATCH，canonical只读回归通过。包内推荐gpt-6-luna保持，无外置application.properties；未改Web/Runtime或模型连接。
- 复用旧安装核验脚本时最初因477未启用taskTimings采集而在任何生产变更前停止；改用同477完整成功作业日志核验6个必要任务均实际执行、无skip/cache/failure，并结合142项JUnit和receipt验证；未伪造计时或跳过必要测试。证据release/fresh-task-evidence.json。该本地核验停止不属于应用安装失败。
- 专用账号登录及事项列表HTTP200；当前无open测试事项，候选/真实推荐业务验收未运行。不创建事项、不改用户技能/接单状态、不触发模型计费，不宣称外部Agent真实推荐效果或性能已验收。用户可在自己的待确认承办事项重新推荐。
- 证据：/home/isp/state/jyt-recommend-external-20261104/release/{installation-plan.json,install.log,installer-result.json,installed-verification.json,deployment-verification.json,readonly-smoke.json}。固定下载包已由既有安装器移入并回收，receipt及来源云端477仍保留，不因本地旧下载路径不存在重建。
