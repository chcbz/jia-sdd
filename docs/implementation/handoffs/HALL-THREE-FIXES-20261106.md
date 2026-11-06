# HALL-THREE-FIXES-20261106

Owner: 当前聊天主Agent，2026-11-06。用户授权：查清根因后修复；本次不自动部署、不重放/删除用户原事项。

## 范围和基线
- 调查证据 `/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/repro/RESULT.md`。
- Web 93c2a10a0d65f680c52f7f41a8ed1c617067350c；API e2cc32306eb9d5476e26862a25f8815cf85086bc；Runtime 5d7290c92b684c3fbc03120a5ad416d79918e589。2026-11-06本轮ls-remote核对develop与线上基线一致。
- Web/API共享工作区有大量他人未提交内容且HEAD早于线上，现有其他worktree均有任务归属，无法安全复用；各新建唯一隔离worktree `/home/isp/wsps/worktrees/hall-three-fixes-{web,api}`，branch `codex/hall-three-fixes-20261106`。
- Runtime复用 `/home/isp/wsps/chcbz/isp-install`，当前branch codex/archive-position-20261105；仅写本任务明确文件，保留其他安装工具未提交改动。
- 已读根AGENTS、ops/orchestration/README、cyf-quick-iterate技能、Runtime AGENTS。所有任务沿用CYF最新Flow分工/600s、固定app实体、RB-1分层；规范 api/docs/interface-standard.md 固定API上述commit。外部Runtime改动显式遵守这些规则，不修改共享技能。

## 修正与验收
1. 能力请求只监听真实请求依赖；切任务不保留旧actor，未指派不查workspace；已完成事项阅读不走活跃办理上下文。保留身份/成员权限。
2. 推荐技能证据只对业务必要的稳定信息比较，不把瞬态健康抖动当技能变更；保留真实权限/任务变更保护。
3. 同thread增量提示明确使用原生历史，空增量不表示无历史，不全量补发。
4. 能力重注册不撤销同连接有效会话；恢复先确认状态可用再关闭健康进程；暂停恢复不显示正在回复。
最早反馈：定向轻量Node状态/消费者回归；Java正式测试及重型构建仅Flow。未运行测试不能标通过；原现场瞬态分量与恢复文件最初缺失原因保留未还原说明。

## 状态
修复、自检和三端云端测试/构建/上传已完成并合入develop；未部署。详细修改和验证见下文。不新增轮询、兜底表、通用框架，不清生产历史状态。

## 2026-11-06 实施与自检

责任层保持RB-1：Web只修读取依赖和展示；API持有推荐稳定事实/权限；bridge只修原生上下文、准入和本机恢复切换。无HTTP字段/数据库结构改变，无新轮询/缓存表/全量历史，无生产操作。

- Web：能力目录fingerprint仅身份/授权代际、enabled、taskId、targetAgentId；切事项清旧显式actor，未指派不请求workspace。已完成事项不加载活跃assignment context/delivery choices，历史消息成果仍按页读取。RECOVERY_REQUIRED仍未完成/可取消/业务busy，但不再显示生成中或流式占位。桌面/移动端原型同步恢复状态。
- API：稳定技能事实与瞬态available/runtimeState分开。模型证据按模型实际输入校验，再按当前可用性投影；已失效证据剔除、该建议UNKNOWN并解释缺口，真实安装/版本/权限/材料变化仍409。没有增加模型调用或查询。
- Runtime：同连接且健康持续的能力刷新保留已确认准入；初次连接、断线、拒绝、真实健康恢复仍要求ACK。排队CHAT执行前再尊重paused/stopped/failClosed，不抢先claim。增量提示允许使用同native thread历史；空增量不是空历史。旧材料恢复先只读确认所需状态存在，再关闭健康闲置chat；绑定/隔离验证仍在原责任层。
- 保留边界：原602出错瞬间ready分量没有日志；旧恢复文件最初缺失原因未确认。修复针对已复现机制，不宣称原现场全部时序已还原。原602/603未改、未重放、未删除。

### 固定候选
| 组件 | commit | tree |
|---|---|---|
| Web 1.16.121 | f1234a0a083b5f38c2677886e89d98fc95aed21c | 0f6402f29f9644ca8f50ceb3ca2ade846b325012 |
| API | 7261c3bedce5477364e984c71e3779b84dcaa6a0 | 10ba53dbab0c2634d1d2094235f2d84cca918675 |
| Runtime1.3.61/bridge1.1.50 | cfe99ae99effaf502a7c516f86aeb50f9808085a | 8de7020597cb25617a48477c65abf3f00a2912c5 |

### 验证证据
基础目录 `/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/`。本地轻量诊断与正式Flow分开：
- `repro/fix-web-targeted.log`119通过；`fix-web-integration.log`46通过；`fix-web-page-wiring.log`30通过（集合有交集，不累计宣传）。
- `repro/fix-runtime-context.tap`11通过、`fix-runtime-recovery.tap`15通过、`fix-runtime-channel-v3.tap`6通过。最终channel回归保留真实健康恢复的ACK边界。
- 原型1440/375宽截图`repro/fix-prototype-recovery-{desktop,mobile}.png`，恢复状态true/生成状态false。仅原型，不冒充生产组件端到端验收。
- API Flow5260799/577 SUCCESS：8套件109测试、0失败/错误/跳过，validateLayering及fresh bootJar通过，同Run制品已上传。`fix-ci/api-test-evidence.json`固定commit和JUnit明细。createTime→updateTime159秒；控制面观测包含查询延迟约173秒。
- Runtime Flow5264702/163 SUCCESS：846测试，839通过、7跳过、0失败，payload及同Run制品上传成功。createTime→updateTime83秒；控制面观测约98秒。`fix-ci/runtime-log-163.json`、`runtime-run.json`。
- Web Flow4403172/468：3902通过、2pending，Vite构建成功，但制品元数据模板只接受develop而拒绝候选分支，因此Run FAIL、不可称为制品交付完成。已修正本任务模板，并核对全部branch断言；最终469验证另记。
- 失败/取消保留：Web466模板入口旧develop断言；467两处提取真实函数的测试夹具缺少新依赖（已补，未削弱断言）；468制品元数据旧develop断言。Runtime161主动取消旧候选以补真实健康恢复ACK回归；162全部回归通过但打包版本断言仍是旧版本，已一次核对Runtime/bridge/skill固定版本并修正。无原样盲重试、无本机构建退路。各attempt原配置/候选/日志/终态保留`fix-ci/*-attempt-*/`。
- Flow均只测试/构建/上传，不调用主机。每Run独立600秒上限，本任务监视器570秒启动受控取消；未取消他人Run。API/Runtime原配置已CAS恢复；Web最终Run结束后恢复。

### 集成与发布界限
API与Runtime已在远端develop无并发新提交条件下正常快进推送（非force），原默认配置无自动触发。Web最终469 SUCCESS，已正常快进推送develop。主工作区其他dirty内容保持，不切换/重置他人分支。
尚未部署，尚未做新提示下真实模型A/B或新版本端到端复测；不能把云端通过当作线上问题已消失。现有卡住事项须发布后只读核对，再按明确操作选择处理，不自动重放。

### 最终收口（2026-11-06 14:48 CST）
- Web Flow4403172/469 SUCCESS：3902通过、2pending、0失败；Vite生产构建、JS扫描、612文件制品上传通过，固定f1234a0。createTime→updateTime227秒，控制面观测约238秒；详细`fix-ci/web-log-469.json`、`web-run.json`。
- 三端远端develop均为上表精确候选，正常快进、无force。只读回验`fix-ci/integration-readback.json`；云端结果汇总`fix-ci/verification-summary.json`。三条流水线临时配置均CAS恢复并readback成功。
- 本任务Web/API隔离worktree自检干净后删除；源码分支和固定提交已推远端，证据保留上述诊断目录。Runtime复用工作区保留其他任务dirty内容。根中已有未跟踪推荐规格仅补本次规则，不将他人原稿整体纳入本任务提交。
- 交付状态：源码修复/回归/合入/云端制品完成；主机安装/生产健康/真实模型场景复测均未执行。API/Web/Runtime本次制品下载时仍须校验来源Run、完整commit/tree和SHA-256，不能用SUCCESS替代安装完整性校验。

## 发布授权与执行（2026-11-06 用户追加“部署并回归验证”）
- 明确授权安装上表三端固定候选并做真实回归，复用Web469/API577/Runtime163，不另开Flow、不更换源码。
- 现行基线只读确认：Web463/1.16.120/93c2a10、API564/e2cc323、Runtime155/1.3.60/5d7290c。记录快照在`/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/deploy/*-previous-record.json`。
- 固定制品下载后校验：Web SHA a45a351fa1b1ce323f79f3597df24e2fa87e2ddae25cde8b3a23d37e308f4895（109813541字节，612文件）；API SHA cd024a49c0c0a6767f502784892aab041e7c82b7210fc58b66b823ddc4ef5881（224098275字节，JAR c5338cb4eaed3f9a6adf7c3d33e9dd17164a47df16b61f7f0e8eb0ad5b32ccda）；Runtime SHA 4c917db573154e7e46c5bbb29cd99db1f9df22190caee4a6c7935fb75f2628ae（28257875字节）。API首次下载传输超时后仅续传已核对Range的固定归档，未重建。
- Runtime复用既有受控host-after-flow安装器：当前Run payload与锁文件核验，Python/browser沿用已验证Run155且要求依赖输入/复制内容完全一致；原生宿主能力探针取固定cfe99ae源码。release锁、完整旧程序清单、停写后状态备份、writer锁归属及固定app原子切换保留。安装器输入/代码及阶段日志在`deploy/runtime-install/`；旧程序/状态备份目标`/home/isp/baks/cyf-agent-runtime-v1/20261106-hall-three-fixes-163`。不恢复业务旧快照、不自动重放602/603。
- API/Web继续使用现行/usr/local/sbin版本化安装入口；API无schema变更，Web保留旧hash资源并index-last。最终安装/健康/业务回归结果后续追加，不能据此段判定发布已完成。

### 实际安装与回归结论（2026-11-06 16:19 CST）

**安装完成；回归为部分通过，有未闭合发现，不能宣称全部问题已解决。** 本节更新前文“未部署”阶段状态，不修改历史CI结果。

- Web469安装exit0；612个本地文件和线上index/入口bundle字节核验通过，当前record为1.16.121/online_verified；备份`/home/isp/baks/cyf-hall-three-fixes-web-20261106-run469/`。证据`deploy/web-installed-verification.json`。
- API577安装exit0；固定JAR摘要与同Run一致，进程PID1672951、10018健康UP；canonical path 8项通过。原F06 CREATE-only检查两表existing_equivalent，未新增业务DDL/DML。证据`deploy/api-installed-verification.json`。
- Runtime163安装exit0；3项真实宿主工具探针通过（非付费模型），暂存与固定路径声明/完整性读回通过，保留停写状态备份与旧程序，固定app路径未变。初次PID1692491，后一次受控原版本重启PID1710463；最终三个Agent通道ready，两套native声明ready。没有改配置、恢复业务快照或重新构建。
- 本任务暂停的健康监控marker核对dev/ino/SHA归属后由原工具恢复；两次遇monitor锁忙未绕锁，确认锁释放后成功。仅本任务Chromium及profile已关闭清理；其他进程/工作区未操作。

#### 真实生产回归
通过正常页面操作新建606（服务器需求讨论）和607（附件诗歌讨论），使用现有测试用户；全部5轮最终为PUBLISHED，页面显示完整回复且结束生成。

1. `skill-capabilities`本轮5次均200，无cancelled；观察窗口没有404/409。590已完成事项历史可读，不请求其活跃interactions/context；599未指派阅读不请求workspace；切换606/607实际actor匹配。导航时长连接取消保留，不能混算能力查询取消。
2. 607第一轮上传并读取真实TXT《秋夜》，第二轮移除composer附件后让模型另作诗，第三轮不重复原文比较两首。模型直接引用双方诗句，未索取原文。三轮唯一native thread `01a1afe2-a068-73c0-af11-a321e86f5bea`，3条turn_context；后两轮`INCREMENTAL_SAME_THREAD`且recentMessages=0。证据`deploy/native607.json`、`native607-history-summary.json`、`browser/poem607-turn{1,2,3}.json`与截图。此为一次真实样本，不保证所有随机生成都不会澄清。
3. 606先问三个服务器需求问题，第二轮正确概括20人/内部文档/国内云/每月300元/下个月上线；未执行购买、安装或服务器命令。两轮均PUBLISHED，未进入RECOVERY_REQUIRED；**首次启动并不顺利，见下方超时发现**。
4. 原602先只读显示“需要恢复核对”、不显示“正在回复”（早期截图）；后续权威状态已变为CANCELLED/USER_REQUESTED、updated_at=2026-11-06 15:44:41.433 CST，本任务浏览器未调用取消。最终页面正确显示“本轮回复已停止”；1440和375宽截图保留，移动无横溢出。本任务未手动重放、恢复、取消或删除原602/603，不将该状态变化归因于本次修复。

#### 未闭合发现（不得掩盖）
- **启动瞬态失败不会重新完成native测量**：初次启动吴用在15:45:15的engine-open阶段`APP_SERVER_RPC_TIMEOUT`（约30s），普通通道ready不代表native执行ready。源码固定cfe99ae的`agent-client.mjs:ensureTypedInspectionProfile`只在本次启动测量一次，失败后的promise保留，无重新测量入口。因此606 bootstrap停在`BOUNTY_RUNTIME_AWAITING`重试，尚未调用模型，而非本轮原RUNTIME_SESSION_REQUIRED故障。15:59在发布锁下确认无inflight，精确核对PID/writer锁，按既有安装器函数停启同版本一次；16:03:07吴用native ready。606随后由原持久请求准入，没有另发请求或手改DB。本次只恢复运行，**未实现启动失败长期修复**。证据`deploy/runtime-install/startup-timeout-restart.*`；此前备份和固定产物不变。
- **读取503仍存在**：607的interactions/context一次返回BOUNTY_FOLLOWUP_V3_UNAVAILABLE，随后200；606 workspace在16:08:58及16:14:04两次返回TASK_WORKSPACE_UNAVAILABLE，稳定重读仍复现。不能说都是瞬态、不能宣称接口全部通过。后端日志只给snapshot_unavailable，没有细分异常；固定源码读模型校验与606/607只读表快照已保留，但**具体失败分支尚未确认**。未通过删除校验或改生产数据遮蔽。证据`deploy/browser/wire.jsonl`、`workspace606-607-readonly.json`；5轮聊天成功不等于workspace验收成功。
- 原602的旧恢复文件最初缺失原因仍未还原；没有据此清旧状态。

总报告`/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/deploy/regression-result.json`为`PARTIAL_PASS_WITH_OPEN_FINDINGS`。Runtime记录区分verified-active通道与businessAcceptance PARTIAL。本机回归是实际生产业务证据，不冒充Flow重型回归。

后端入库turn创建到最后状态更新时间：607三轮40.009/13.010/27.049s；606两轮152.972/7.224s。这不是前端首字/完整可见时间，也不含606此前因启动未就绪造成的长等待，不作为端到端性能通过结论。

下一步：先定位606 workspace的可稳定复现503与607上下文503责任分支；启动失败按现有生命周期做有因重试/显式恢复，不再靠重启、不新增轮询兜底表。后续源码修复与云端验证/部署另记，本轮不能标全部完成。

### 继续修复：读取503根因已定位（2026-11-06）
- 固定修复基线仍为已安装API7261c3b/Runtimecfe99ae，Owner沿用本任务。API主工作区有他人未提交修改，复用隔离工作区`/home/isp/wsps/worktrees/hall-three-fixes-api`；Runtime复用原工作区，不触碰其无关dirty。远端develop已前进至APIf24f4c1/Runtime dbb9e3d，包含其他计费改动，不把它们自动纳入本次部署。
- workspace503：正式提交生产TASK_REVIEWING事件的actor是agent，C04/C05共享validator却要求所有任务转换均system。606/607的event_version12均命中。只修该合法事件actor表达；保留其他事件及结构/状态校验，不改生产事件。
- context503：`followup/innodb-last-deadlock.txt`对应16:06:36实际死锁，事务9054986先持persona binding再等task root，9054988反向持task root再等binding。GET预览不产生执行授权，却进入写锁链。改为同一REPEATABLE_READ只读快照；真正提交/派发继续原有锁与权限检查，预览不调用写入准入。无新表、无通用重试。
- 回归入口：正式交付producer→共享validator、Grant只读观察/原写准入、Preview真实Spring事务/绑定冲突与ACL。Runtime启动暂态失败恢复仍待落实。以上为已确认根因及实施范围，不是新版本已发布证明。

### 修复候选与发布推进（2026-11-06 17:18 CST）
- API发布候选7bb82c526e4ba4345ca8e88711067ed23dfcdbbc/tree7e6d03056902c4a36abd9ca0959d5a398e65224b，1.1.38-SNAPSHOT，Flow591：12套件168项全部通过（含生产者三事件→读取器、只读Spring事务、并发binding快照、原写入准入、分层与fresh JAR）。589是新增测试漏导入断言，590是测试把内部IllegalArgumentException误写成外层Workspace异常；已分别修正测试，未删断言/改业务错误语义，无同输入盲重试。旧577的109项属于推荐测试选择器，不能作为本次Preview/锁回归证据；本次以591的实际套件清单为准。
- Runtime发布候选c1fc18174b256c90051874485c8c77967efad62a，1.3.65/bridge1.1.54，Flow166：848项，841通过、7云端环境跳过、0失败；主机原有3项宿主探针及实际启动声明另行通过。现已受控安装，PID1737375，三个通道ready，两套native declaration ready；本轮未再出现启动超时。能力测量完整纳入原启动gate；仅engine-open阶段APP_SERVER_RPC_TIMEOUT在清理完成后再试一次，清理失败/永久错误/执行期失败/已dispose不重试，无定时轮询、无任务重放逻辑。故障注入与真实顺利启动是不同证据，不声称生产中人为重现了超时。
- API591安装中，前置浏览器只读复测606和607 workspace均503已存证，后置及多轮回归尚未完成。证据统一`/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/followup/`；不修改原602/603。
- 避免下次develop发布丢失修复，正在单独集成并行计费源码：API Grant构造器存在真实冲突，保留billing与只读taskRoots两个不同职责依赖，并适配实际测试调用；Runtime原工作区有他人dirty且develop改变其路径，故只为该冲突新增一个`hall-followup-runtime-integration`工作区。集成候选将独立验证，**不将并行计费改造自动部署到生产**，不把591/166的证据冒充集成后tree。

### 后续修复已部署及业务回归（2026-11-06 17:46 CST）
- API591受控安装exit0，线上1.1.38-SNAPSHOT/7bb82c526e4ba4345ca8e88711067ed23dfcdbbc，制品SHA256 `065a7d166d35a85071afe7c25fed992906121002a1de2858ab7badcd203c33df`，JAR `75e7886fd502b293c5173b0f3ba6a1e21c2b6df0e51b1df408fa98598b2886ee`。10018健康UP，canonical实体目录8项检查通过。F06两表existing_equivalent，无业务迁移。安装/健康证据`followup/deploy/api-*`。
- Runtime166已安装1.3.65/bridge1.1.54，PID1737375，三个通道与两套native能力ready。宿主3项探针通过；旧程序/状态备份保留`/home/isp/baks/cyf-agent-runtime-v1/20261106-hall-followup-166`。本任务maintenance marker已按归属恢复，无状态快照回灌。API/Web/Runtime本轮部署源分别为591/469/166，不是后续集成候选。
- 安装前606/607 workspace真实浏览器均503；安装后两者workspace/context四项均200/E0，分别112.6/52.5/513/65.6ms（单次请求样本，不是性能SLA）。诗歌回复期间四个有界并发读取也均200，131–203ms；没有增加生产轮询、重试表或逐帧校验。
- 新服务器事项608/conversation1760458009364，通过正常UI明确选择在线吴用，连续两轮均PUBLISHED；第二轮准确回答20人、月预算300元、下个月上线，页面结束生成，无RECOVERY_REQUIRED。仅讨论，无购买或服务器安装动作。初始推荐包含离线扈三娘，未指派该Agent，不扩大本次修复范围。
- 本任务诗歌事项607在Runtime重启后追加第四轮：同一native thread `01a1afe2-a068-73c0-af11-a321e86f5bea`，仍INCREMENTAL_SAME_THREAD、recentMessages=0；模型正确引用原诗“独把新茶当旧游”和此前自作诗“独煮新茶待故人”，没有索取原文，终态PUBLISHED。桌面/375px截图保留，移动document scrollWidth=375，无横溢出、无“正在回复”残留。
- 本次浏览器观察的skill-capabilities四次均200、无cancelled；业务窗口没有404/409/503。另有一次SSE ERR_ABORTED和一次HTTP2_PROTOCOL_ERROR，后续流连接200、回复正常完成；传输错误单独保留，不宣传网络零异常、不将它们混算能力查询取消。原602/603未更改或重放，旧恢复文件最初丢失原因仍未还原，不宣称已恢复历史状态。
- 诗歌第四轮**浏览器实际POST发出→DOM**：首段可见14.903s、完整正文可见16.127s、生成状态结束17.877s。单样本包含服务端/模型等待；不是Runtime内部耗时或统计SLA。服务器两轮DB turn创建→最后更新15.149/9.988s，诗歌第四轮16.921s；后者不能冒充前端端到端数据。
- 本轮总报告`followup/deploy/regression-result.json`为`SCOPED_REGRESSION_PASS_WITH_TRANSPORT_OBSERVATION`；Runtime现行发布记录已在原release锁内更新businessAcceptance及证据读回，程序/身份/配置未再改变。

### develop集成与规则接续（2026-11-06）
- 已读现行根AGENTS的11-06本地构建规则；自此次接续不再启动付费Flow。此前API集成prepare因他人活动Run返回ACTIVE_RUN_NO_WRITE，无云端写入/新Run；保留原因，不抢占。已启动的Runtime167完成后仅CAS恢复原配置、保存结果。
- Runtime并行计费源码合入候选d962e92ade0cb12d291de94d6cd6d896a7b52838/tree4e9ceb8b87ce9a8a95b0f7d887826b1d3a9f0f45，1.3.66/bridge1.1.55：167 SUCCESS，866测试859通过/7环境skip，正常快进推送develop。**未安装**，线上仍166。
- API集成候选3d4bbb2e0e（完整SHA见`followup/integration-local/inputs.json`）保留f24f4c1并行计费与本轮读取修复，另验证真实billing构造调用。当前本地经既有orchestrator串行入口验证原168项及一个MySQL计费事务用例、validateLayering；在本任务独立mysqld/datadir/随机loopback端口运行，不使用生产数据库。已有Gradle锁忙时等待，不并发堆叠。仅集成验证，不打生产包、不安装计费候选；结果待补。

### 本轮交付结论与剩余集成边界（2026-11-06 18:12 CST）
- **本次部署和线上定向回归已完成**。最终只读健康再次UP，生产JAR摘要仍精确匹配591；Runtime PID仍1737375。证据`followup/deploy/final-health.json`。浏览器及本任务profile已关闭/清理，Runtime集成worktree已在推送及干净核对后删除；未修改其他工作区、进程、原602/603或生产会话状态。
- **API develop集成尚未完成，不算上线故障未修复。** 第一次本地集成验证在project configuration阶段发现共享Gradle immutable transform cache内容不匹配，尚未进入测试；错误日志及归因保留`followup/integration-local/gradle.log`。未删除/修复共享缓存；第二次改用任务独立Gradle home，仅复制依赖缓存，固定相同源码，但既有串行锁由另一任务BETA-WEN-BILLING-20261105持有。等待期间本任务没有开始Gradle测试，不能标PASS。
- 线上目标已验收，独立集成因外部构建锁暂缓。精确确认本任务PID1767341是WRITE*等待者后只停止该排队控制进程，未中断锁持有者或任何运行中的构建。第二次记录exit -15/NOT_STARTED（`attempt2/queue-deferred.json`、`result.json`），不是测试失败；两次自有MySQL都在finally停止、PID消失后删除临时datadir，日志/输入证据保留。无悬挂的本任务浏览器、MySQL或Gradle作业，无新增付费Run。
- API候选完整commit/tree保留`followup/integration-local/inputs.json`，远端任务分支已保存；保留唯一干净API工作区`/home/isp/wsps/worktrees/hall-three-fixes-api`用于后续验证，不覆盖主仓dirty、不强推develop。Runtime集成d962e92已合入但未部署。后续动作仅待锁释放后完成API集成定向验证并正常快进合入；不因此重新安装已验收的591/166/469。

### 继续收口：SSE传输异常已复现定位（2026-11-06 18:44 CST）
- 只读同一测试会话607，分别直连127.0.0.1:10018和经公开域名HTTP/2代理订阅；两端返回200及相同11446字节历史/ready内容。没有发消息、调用模型、修改事项或更改代理配置。
- 两端均没有SSE注释保活。公开代理在最后数据之后299969ms（约300秒）以NGHTTP2_INTERNAL_ERROR/rstCode2关闭；直连API在330秒观察结束时仍然打开，由探针自行关闭。与现行`location /chat`的`proxy_read_timeout 300`以及上一轮17:41:00、duration349.982s访问日志吻合。原异常是空闲SSE无保活引发的代理读超时，不是模型执行失败，也不是skill-capabilities取消。
- 证据`followup/sse-probe/idle-comparison.json`、`root-cause.json`、`nginx-chat-location.txt`；固定线上API7bb82c5。这里只读验证和根因定位，尚未改源码或生产配置。
- 最小修正应在API SSE传输层发送注释保活：不查数据库、不扫描任务、不执行模型、不推进游标、不作为业务消息；随源流结束/取消回收。现有Web解析器已忽略冒号注释，不需要增加前端轮询或改业务协议；不采用单纯增大代理超时的临时方案。
- API集成继续复用唯一工作区及原3d4bbb2候选，固定本地验证输入。先等待现有Gradle锁释放，再启动本任务MySQL/验证，避免排队阶段运行无用数据库；无付费Flow、无他人进程控制。
- 18:52 CST再次确认实际持锁者仍为另一任务PID1764749，测试进程仍存在；通过既有`conflict-alert`发送仅协调通知，没有改派/中断/操作对方产物。此次本任务只在`flock`前置等待，未启动Gradle或MySQL；结束等待前核对WRITE*与完整命令，仅停止本任务等待者PID1796054。`integration-local/recheck-lock-blocker.json`记录真实阻塞；`attempt3`未生成，不能宣称新验证已运行。原候选和干净工作区继续保留，SSE本轮仅定位、保活改动尚未实施。

### SSE保活实现与本地验证中断（2026-11-06 19:24 CST）
- 在原唯一API工作区完成最小传输层修正，commit `638896a16cbf3f6df602a65f9a6c97b4ceb4889b` / tree `50384c91391b7e5b3f71931996ec53ab7dcb8fd8`，仍为集成候选1.1.39-SNAPSHOT；包含并行计费基线，**不是可直接替换线上591的独立补丁发布候选**。修改仅ChatStreamPolicy、ChatController、既有测试及其sourceSet。未改Web、Runtime、Nginx或生产文件。
- 每30秒发无data/id/event的SSE注释；只订阅一次业务source，merge prefetch=1，不提前拉完整replay；最多一个待发送注释，多余tick丢弃。业务完成/错误/下游取消均回收定时器，不访问数据库、不扫描任务、不触发模型、不推进游标。新增5项测试覆盖注释、完成、错误、取消、同步完成和背压，连同既有4项ChatStreamPolicyTest明确加入受测sourceSet及selector；尚未取得后端执行结果。
- Web只从已上线commit f1234a0提取解析器及递归依赖到本任务证据目录，未使用当前其他任务的dirty Web代码。既有7项SSE测试及新增10000注释零消息/零游标/零错误检查，共8项通过。证据`followup/sse-probe/web-fixed-source/source.json`与`web-parser-test.log`，不是重新构建/部署Web。
- 原构建锁自然释放后启动本地attempt3，固定上述commit/tree、隔离MySQL、独立Gradle home；只复制依赖modules-2，不复用测试结果或损坏的transform cache。通过既有orchestrator取得串行锁并开始编译；命令与摘要见`followup/integration-local/attempt3/inputs.json`。
- 本次exec66106随后以143/SIGTERM结束，Gradle daemon记录client断开/Broken pipe；发起者未知，不推断其他任务违规。没有测试XML、没有PASS或生产包；`interrupted.json`保留实际退出码、源码、日志摘要。原本任务wrapper/Gradle/MySQL均已消失，未看到MySQL正常shutdown日志，datadir暂保留且无对应运行进程，见`mysql-cleanup.json`。当前另一任务1810651持锁，不抢占、不盲重试；通过原conflict-alert仅协调。
- API候选保存在原任务分支；develop仍未合入，线上仍原已验收591/166/469。当前主机安装器仍有Flow-only/LOCAL_ADMISSION_RETIRED限制，本轮未改造；不得伪造Run发布新保活。后续须先收口受测集成，再固定不夹带未授权计费变更的发布候选、明确适配本地来源，经过原锁/备份/恢复路径安装并复测超过300秒空闲连接。不能把源码完成写成上线完成。
- 已清理前次SSE探针遗留的空闲Node runner1785562，先核对完整脚本路径、无子进程及浏览器已关闭；未控制他人进程。保留本任务唯一worktree、编译/依赖缓存用于接续，避免下一次重复冷构建。

### 本地集成验证已通过，真实MVC补充验证进行中（2026-11-06 20:45 CST）
- 接续读取用户最新11-06规则：本地600秒为优化目标，不强杀；本轮没有最终包可登记清理。复用原638896a候选、原工作区和attempt3编译/依赖缓存，不复制第二套源码/缓存。上次SIGTERM发起者仍未知。本次用仅属于本任务的systemd transient unit承载既有验证脚本，仍经原Gradle串行入口；与交互工具生命周期分离，没有生产重启/定时重跑。
- `attempt3/resume1/summary.json`：121项测试全部通过，0失败/错误/跳过，9项ChatStreamPolicyTest确实执行，validateLayering通过。精确commit/tree未变。与旧591的168项差异已逐suite核对：本轮仅集成不执行bootJar，故不包含66项随打包触发的制品/POI测试；合入基线新增9项grant测试、1项MySQL计费测试、本轮9项流策略测试，168−66+9+1+9=121。前文“原168+1”是未剥离打包图的计划口径，以实际121项及selector为准；不将集成通过当作生产打包通过。
- 此次Gradle实际1927.938秒；准备/排队/验证墙钟1983.025秒，排队0.016秒。**验证已超过600秒目标；完整发布未执行、未实测**。初次未完成的编译在本轮补齐，15任务up-to-date、69执行；保留原中断耗时与后续HTTP排队/脚本失败记录，不将跨批累计省略为完整发布达标。隔离MySQL正常退出，已核对PID消失后只删除本任务两个已停止fixture的datadir，日志/源码/测试XML/缓存保留。
- 为覆盖实际改动的Controller，再运行已有ChatConversationEventsHttpTest（真实MVC编码、replay/ready、热预览背压与取消），不是新增业务代码。初次补充init误应用到included plugin build，配置阶段找不到chat项目，尚未执行测试；按原工具记录归因，改findProject限制到实际chat根。两次状态恢复命令未进入Gradle（验证gate及transition默认owner参数问题），NOT_STARTED日志分别保存，不视为测试失败或PASS。正确显式Owner/gate后，修正fixture已在`cyf-hall-sse-http-20261106-r4`执行，证据`attempt3/http2`；期间交互sleep工具再次143，但该验证unit仍运行，不能据此推断原SIGTERM发起者。
- 20:43只读线上API仍591/7bb82c5，health UP；结果`integration-local/production-readback-20261106.json`。新保活仍未部署，API develop合入等待MVC结果。主机安装器本地来源适配尚未实施，不能绕过现有锁/备份/恢复或恢复退役准入入口；后续发布候选仍须避免夹带并行计费变更。
- 后续MVC补充运行`http2`实际执行21项，其中流策略9项通过、MVC12项均在fixture初始化因`RedisScript`类缺失失败，未进入MVC业务断言。根因是该原测试在默认test中依赖common-test，而临时精简slice仅继承implementation/runtimeOnly。未修改业务代码；临时slice改继承既有testImplementation/testRuntimeOnly，保持原测试类路径而非逐个补缺失类。失败XML保存在`http2/test-results`，已通过原fail/transition显式归因与恢复验证阶段。
- 修正依赖的唯一后续验证为`cyf-hall-sse-http-20261106-r5`，runner复用`integration-local/verify-http.py`，新fixture/日志`attempt3/http3`。当前仍在串行锁等待，持锁者是另一任务1845635，本任务等待者1848560；没有运行第二套Gradle/MySQL，没有取消/抢占。unit独立于聊天保持等待及获锁后验证，**不会自动合入或部署**；`integration-local/continuation-state.json`记录实时状态。下一接续先读该unit和`http3/result.json`，不要重复启动。
- 原121项主回归XML已逐一校验摘要并保存到`resume1/test-results`，summary引用已指向不可被后续Gradle覆盖的快照；未将后续失败XML混作原成功证据。API源码仍638896a且工作区干净，develop尚未推送，线上未改动。完整收口仍需MVC通过→正常合入→隔离不含并行计费的发布候选及本地来源安装适配→打包/安装/超过300秒空闲实测；未完成部分不能宣称已交付。

### API develop集成完成（2026-11-06 21:20 CST）
- 原持锁任务自然释放后，本任务r5获锁执行；`attempt3/http3/summary.json`最终21项通过：12项真实MVC SSE回归 + 9项流策略复跑，0失败/错误/跳过。主回归121项与新增MVC12项共133个独立用例，9项策略复跑不重复算独立用例；覆盖大历史replay/ready、热预览背压、真实MVC单次编码、游标、身份错误、取消释放与保活生命周期。源码未为补充测试做新修改。
- 本次HTTP Gradle482.040秒，含排队/控制的墙钟1608.203秒；只有实际Gradle阶段低于600秒，不能宣传整轮或发布达标。日志/固定输入/不可变XML快照均在http3；早先配置/依赖失败保留原位置，不重标PASS。
- 正常快进push API develop：f24f4c1→`638896a16cbf3f6df602a65f9a6c97b4ceb4889b`，远端readback一致、工作区干净；tree`50384c91391b7e5b3f71931996ec53ab7dcb8fd8`。证据`integration-local/integration-complete.json`。前文“等待/未合入”是之前阶段状态，以此为准。
- 本任务验证units均已结束；保存失败unit状态后仅reset-failed本任务4个失败transient units，未控制他人服务或正在运行的作业。此前两个隔离MySQL均已停止并清理datadir。没有最终生产包，未登记虚假可回收产物；唯一工作区/编译缓存仍供未完成的发布步骤使用。
- **整体交付尚未结束，新SSE保活未部署。** API develop集成包含并行计费基线，不能直接安装；后续在同一工作区固定已部署7bb82c5 + 本次SSE补丁的独立候选，按真实LOCAL来源适配当前安装器，保留原互斥/完整性/备份/恢复，不能恢复已退役准入或伪造Flow。再执行生产打包必需回归、受控安装及>300秒空闲对照。当前只完成源码集成和定向验证，不将其冒充发布完成。
