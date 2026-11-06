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
