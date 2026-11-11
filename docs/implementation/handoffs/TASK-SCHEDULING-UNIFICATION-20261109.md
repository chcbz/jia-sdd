# TASK-SCHEDULING-UNIFICATION-20261109

## 当前任务临时时限例外（用户再次确认）

用户明确“临时取消时间限制”：本任务测试、构建、打包、发布与回归暂不执行原600秒上限，仍记录实际耗时和真实失败，不以超时重启或拆批。仅限本任务，不永久修改项目/共享规则；不改变发布与生产操作授权、身份/ACL、资金幂等、事务、锁、制品完整性、备份及恢复边界。下文历史时限和阶段状态保留作追溯，不作为当前时限指令。

## 范围与固定输入
Owner：本会话。2026-11-09用户要求现有task升级为统一调度入口，费用任务首批接入。
API只读基线49f6b4d20abecd87dfceb8db3c7bbf7600e1eb6b（本地origin/develop，与此前安装记录一致；未查询远端最新）。主区脏修改不动。
当前仅调查与设计准备，未改应用、迁移、构建、发布或启用扣费。遵循根AGENTS/API接口规范/RB-1；正式本地构建普通磁盘、累计600秒。外部Runtime和主机任务尚未盘点，不宣称全系统完成。

## 已核实
- JobHandler/JobRegistry/JobExecutor及带job-*权限的手动HTTP入口可复用。cron扫描只打日志；互斥containsKey/put非原子且仅本机；同名注册覆盖；运行状态未持久化；固定线程池缺少业务隔离。
- TaskService/TaskPlan/TaskItem仍服务计划事项业务和周期项预生成，不能重释其字段为集群任务状态或删除既有消费者。
- MemoryJobHandler同时实现处理器和自带@Scheduled，启用统一cron必须同步撤销旧触发以免双跑。
- 已有RedissonDistributedLock及starter依赖，可评估复用；未验证生产Redis拓扑和故障行为，不把源码依赖当已具备可靠集群协调。
- 命中包括业务恢复扫描、消息派发、本地文件回执、连接心跳和执行租约维护；不能都改成集群唯一任务。本地资源处理必须具有节点归属。
- BackgroundSchedulingConfiguration禁止fixed-tenant灰度调度，新入口必须保留。手动触发继续要求身份、权限、可信租户及业务授权，不因注册收费任务扩大权限。

## 设计方向（未实现）
- task负责注册、触发、执行状态、恢复及集群协调；业务保留队列/事务/资金幂等，避免复制业务状态机。
- 支持cron、一次性到期和事件唤醒，区分集群业务任务与节点本地维护；执行中协议心跳不机械迁为集群任务。
- 数据库保存不可丢待办与执行版本；Redis若用于锁/通知仅作协调优化。丢通知/Redis重建须靠启动恢复和低频索引补查兜底，不承诺零空查询。
- 余额事件可靠关联资金提交，合并用户唤醒；处理中新事件不能被旧完成动作覆盖。
- 接管使用领取令牌/版本阻止过期执行者覆盖状态；扣款仍按租期业务幂等。外部副作用逐消费者分析，不承诺调度exactly-once。
- 定时线程不承担长业务；慢任务不阻断租期唤醒。重试不创建新的收费调用身份，不自动重发Provider付费请求。

## 下一步
1. 核对现有事件/消息可靠投递、Redis实际部署（不输出凭据）、task模块依赖和计划业务消费者。
2. 将初步命中按任务标识、租户/节点作用域、恢复事实、旧入口停用点及定向回归分类，补完整调用链。
3. 固定最小schema/API、执行与失败规则；先验证集群领取/重启恢复/通知丢失/执行中唤醒/权限隔离，再逐批迁移，每项只留一个有效触发入口。
4. 费用注册30天续费、余额增加恢复、锁定超过15天移除。金额、资格及旧事项保留规则由费用/Agent模块实现。

## 初步源码关键词命中（不是完整迁移清单）

```text
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentReconciler.java:58:    @Scheduled(fixedDelayString = "${agent.hosting-rent.reconcile-delay-ms:5000}")
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentStatusMonitor.java:31:    @Scheduled(fixedDelayString = "${jia.agent.status.offline-scan-interval-seconds:10}000")
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandReissueCoordinator.java:48:        this.worker = Executors.newSingleThreadScheduledExecutor(runnable -> {
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandReissueCoordinator.java:54:            worker.scheduleWithFixedDelay(
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentOutboxRelayScheduler.java:55:        poller = Executors.newSingleThreadScheduledExecutor(runnable -> {
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentOutboxRelayScheduler.java:65:        poller.scheduleWithFixedDelay(
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskEventReplayServiceImpl.java:219:                recoveryTimer = timerExecutor.scheduleAtFixedRate(() -> scheduleRecovery(epoch),
origin/develop:agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillInstallRecoveryService.java:31:    @Scheduled(fixedDelayString="${economy.skill.marketplace.recovery-delay-ms:5000}")
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveQuestionSseService.java:80:                java.util.concurrent.Executors.newSingleThreadScheduledExecutor(
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveQuestionSseService.java:282:                    heartbeat = heartbeatExecutor.scheduleWithFixedDelay(
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveQuestionWorker.java:96:            executor.scheduleWithFixedDelay(this::safeRun, 0, 250, TimeUnit.MILLISECONDS);
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveQuestionWorker.java:520:        return Executors.newSingleThreadScheduledExecutor(runnable -> {
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveQuestionWorker.java:623:            future = scheduler.scheduleWithFixedDelay(this::renew, renewInterval.toMillis(),
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/job/MemoryJobHandler.java:57:    @Scheduled(cron = "${chat.memory.job.sync-cron:0 0 * * * ?}")
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyAssetRelay.java:38:        this(projector, () -> Executors.newSingleThreadScheduledExecutor(r -> {
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyAssetRelay.java:57:        scheduler.scheduleWithFixedDelay(() -> { if (current(epoch)) safePoll(); }, 0, 30, TimeUnit.SECONDS);
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyExecutionRelay.java:28:        scheduler=Executors.newSingleThreadScheduledExecutor(r->{
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyExecutionRelay.java:31:        scheduler.scheduleWithFixedDelay(this::safePoll,0,5,TimeUnit.SECONDS);
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java:282:                ScheduledFuture<?> heartbeat=ensureScheduler().scheduleAtFixedRate(()->{
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java:292:                ScheduledFuture<?> heartbeat=ensureScheduler().scheduleAtFixedRate(()->{
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java:423:        ScheduledFuture<?> heartbeat = heartbeatScheduler.scheduleAtFixedRate(() -> {
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxRelay.java:489:        return Executors.newScheduledThreadPool(maxConcurrentDeliveries + 1, r -> {
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/NativeConversationWorkNotifier.java:30:        this(sockets,discovery,()->Executors.newSingleThreadScheduledExecutor(r->{
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/NativeConversationWorkNotifier.java:41:        owner.scheduleWithFixedDelay(()->{
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/service/recommendation/RecommendationUsageJournal.java:83:    @Scheduled(fixedDelayString = "${jia.chat.recommendation.usage-recovery-delay-ms:60000}")
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/voice/service/VoiceLeaseGuard.java:18:    private static final ScheduledExecutorService EXECUTOR = Executors.newScheduledThreadPool(
origin/develop:chat/jia-chat-service/src/main/java/cn/jia/chat/voice/service/VoiceLeaseGuard.java:42:        this.future = executor.scheduleAtFixedRate(() -> {
origin/develop:task/jia-task-service/src/main/java/cn/jia/task/executor/JobExecutor.java:127:    @Scheduled(cron = "0 * * * * ?")
origin/develop:wx/jia-wx-service/src/main/java/cn/jia/wx/schedule/WxSchedule.java:59:	@Scheduled(cron = "0 30 7 * * ?", zone = "Asia/Shanghai")
```

## 接续2：依赖、通知与最小合同（2026-11-09）

### 新核实的依赖
- AgentTaskEventBroker类声明及实现为process-local/lossy唤醒；AgentTaskEventAfterCommitPublisher在事务提交后通知，但不构成跨容器可靠队列。不能把这两者直接作为余额续费消息总线。
- Agent已有带确认的Rabbit发布器，但属于Agent命令合同，不让task反向依赖agent/service，不借Agent命令exchange承载调度业务。是否引入消息中间件不是本轮默认前提。
- TaskService真实消费者包含HallTaskCreationServiceImpl、AgentServiceImpl、AgentTaskRequirementEditServiceImpl、Chat TaskTools、TaskAlertJobHandler。TaskPlan/Item/Detail及CRUD必须保持业务含义。
- TaskTenantConfiguration只覆盖task_plan/task_item/v_task_item，新增调度表不会自动因包名而取得隔离；发现、排序、LIMIT和领取必须按进程可信tenant以及适用client/node作用域执行，不能领取后过滤。
- task-service依赖task-api、base-api、common-service、task-mapper；调度契约应放task-api/core，业务实现依赖该契约，task不得依赖agent/economy/chat实现。
- 手动JobController有权限注解，但目前接受通用params，失败字符串也包装success；新增资金处理器不得因持有通用job-execute就获得任意用户扣款能力。内部业务任务明确不暴露通用手动入口，手动补跑只能引用已持久受权任务。

### 建议固定的最小实现合同
1. 注册定义继续使用JobHandler/JobRegistry思路，增加作用域/触发元数据，重复名称作为配置错误，不能静默覆盖。cron真正启用需逐处理器迁移标识，不能顺带启用从未自动执行的提醒或重跑Memory的旧@Scheduled。
2. 调度持久记录与旧task_plan/item分开，归task模块；最少含scope、handler、businessKey、dueAt、状态、requestedRevision、completedRevision、领取token及租约到期、attempt和错误摘要。准确DDL/索引须实现前固定；不保存用户正文/凭据，不建通用流程编排引擎。
3. 业务事务内登记/更新待办，提交后唤醒只作优化。余额增加处理与待办登记同库同事务，不能afterCommit才首次落库。若可靠登记失败，不能声称事件已保存；后续核查钱包真实posting层，避免在每个退款/赠送Controller重复实现。
4. 按scope+handler+businessKey合并唤醒。执行领取时固定revision，执行中又收到事件则requestedRevision前进；完成只能确认已处理revision，不能把新唤醒一起标完成。定时改期/取消也需版本匹配，旧闹钟不能复活已移除关系。
5. Redis拟用于统一调度所有者的协调和跨节点唤醒，不存唯一收费事实。单个调度所有者按最近dueAt设置闹钟，处理后重排；待办落库成功但通知失败，由低频索引补查/接管恢复发现。Redis不可用不无锁退化为各容器自由执行；任务保留，业务既有执行不被调度故障强停。
6. 多容器任务领取与完成仍有数据库CAS/token；锁切换不代表旧业务调用物理停止。扣款使用账务唯一事实和业务事务；消息/外部操作不得在未知结果下无条件重试。
7. 仅短事务处理发现/领取/结果，不持数据库事务等待Provider/长操作。定时线程只安排唤醒，业务线程执行；费用与慢任务不能共用会被长期占满的无界队列。具体并发度按既有配置/负载确定，不新设无依据门槛。
8. 每项迁移保持原fixedDelay/cron/事件语义和停用开关，未知handler保持待处理并告警，不当成功删除。灰度/非执行节点不自动接管；停机停止新领取，已完成事实不重放。

### 首批分类
| 类型 | 已定位入口 | 处理方向 |
| --- | --- | --- |
| 集群业务周期 | MemoryJobHandler、WxSchedule、TaskAlertJobHandler | 统一注册；先核对业务权限和错过时间处理，不同时保留原触发 |
| 业务恢复/到期 | HostingRentReconciler、SkillInstallRecoveryService、AgentStatusMonitor | 保留原业务状态机，由统一调度驱动；分别验证真实scope |
| 队列/派发唤醒 | AgentOutboxRelayScheduler、ChatBountyExecutionRelay、ChatBountyAssetRelay、NativeConversationWorkNotifier | 保留现有领取与ACK；调度只替换扫描/唤醒，不再复制队列 |
| 节点数据恢复 | RecommendationUsageJournal | 回执目录所属节点执行，不能全局只选一个任意节点 |
| 连接/执行维护 | SSE心跳、VoiceLeaseGuard、ArchiveQuestionWorker续租、ChatDeliberationOutboxRelay心跳 | 保留执行者/连接本地语义；不强塞成集群唯一业务任务 |

### 已确认费用规则（供首批消费者，不由调度层解释金额）
- 技能新安装50文、升级20文；确认预占，成功扣款，明确失败/取消释放，重复请求不重复收费。
- 平台托管500文/30天，自行部署50文/30天；首次确认预占，部署成功且服务可用后扣款起租。
- 到期可用余额足够自动续期；不足锁定。可用余额增加后检查恢复，恢复租期从成功扣款解锁起算30天，锁定期间不收费。
- 锁定只限制新增承办、密议新请求、新技能安装/升级；已有事项及已受理技能操作继续完成结算，不在执行派发入口加拦截。已有租金派发拦截需相应收窄。
- 连续锁定超过15天解除使用关系并停止自动续费；不删除实例、不撤销旧事项执行身份和授权。
- 存量两种部署均给予上线时起30天过渡期，不追扣历史。
- 主动移除不退当期款；重新请回由原用户复用原实例/技能/历史，收取完整一期，旧剩余租期不结转；其他用户不得接管旧实例。
- 多Agent按到期时间、固定同时间顺序处理；余额不足不阻塞后续Agent。
- 不恢复固定5分钟全业务空扫描；采用到期/余额事件，保留必要可靠性兜底。

### 尚需闭合的技术证据（不是已完成项）
- 生产Redis部署/故障恢复与公共锁线程归属、可靠唤醒实现，以及钱包统一入账扩展点尚需定向核对。
- 最小迁移SQL及索引、正式源码隔离位置/候选、定向回归与发布批次尚未固定。
- 尚未写应用源码、构建或安装；文档不代表统一调度和新增收费已启用。

## 接续3：统一入账责任与规格落盘
- 固定源码全生产调用搜索：EconomyLedgerMapper.updateAccountBalance唯一调用在EconomyPostingServiceImpl.postInTransaction。余额变化应在USER/AVAILABLE账号净增加时同事务登记可靠唤醒，不在钱包展示Controller或每个退款入口重复实现；posting重放直接返回旧事实。
- 新发现资金/调度锁反转风险：posting持账户锁再登记待办，调度必须短事务领取后释放调度行锁再执行业务，结果另事务CAS写回，不能持调度锁调用钱包。
- 本机6379存在监听，但redis/redis-server两个systemd名均inactive；仅此不足以判断生产Redis部署方式/可用性。本轮无密码查询、Redis写入、重启或配置变更。
- 当前设计、任务、验收及未pin的integration已落specs/task-scheduling/，纳入specs/INDEX.md。首次导航因缺integration.yaml失败，补充真实draft/pending元数据后check-docs task-scheduling PASS（不代表应用测试/发布）。
- 应用代码、DDL、构建、收费启用均未执行。下一步是协调机制和候选源码实现，不重复从头扫描已核实入口。

## 用户交接方案定案：先收尾再邀请（2026-11-09）
用户明确接受在再次邀请前闭环：移除后收尾，原事项完成/取消且旧执行安全收束、私有运行上下文隔离完成，才允许任何用户再次邀请。不实现交接后替旧用户继续工作的多身份/多技能版本兼容；原用户未验收不取消时可长期收尾。
正式费用/交接合同回写specs/agent-economy-marketplace/beta-wen-billing.md新增节，涵盖后来确认的已有技能首期计费、自行部署周期费、超15天移除优先、存量过渡和共享知识边界。此前handoff中笼统“原用户复用、其他用户不得接管”由该现行合同替代：其他用户可在收尾交接后复用公共实例，但不得继承旧私有数据和凭证。
本次仅文档更新；task-scheduling导航PASS，未运行应用测试/发布。

### 首期技能数量口径确认
用户确认报价时已安装技能按种类计一次；停用未卸载计入，已卸载/历史版本/系统基础工具不计入；清单变化重新报价确认，不事后加钱。已回写费用责任规格；当前已知金额与交接业务问题已确认，剩余技术核实不冒充实现完成。

## 实现切片1开工（2026-11-09）
- 已只读查询远端develop，现为c661e6421346d610ee063b0fb9b614e282e7bcca，随后fetch核对。相较旧调查49f6b4d20，task/economy/common无差异；不回退期间他方修复。
- API主工作区94项脏改，不覆盖。唯一隔离工作区/home/isp/wsps/worktrees/task-scheduling-api，分支codex/task-scheduling-20261109；base tree ec09a5c1dadb8162ce7973711ea7d40cb0116c06。本worktree遵循根/组件AGENTS、RB-1和接口规范。
- 首候选326cd6fe2b207fc8ef54663cb27e57533444813c，tree ce886fb4fbf5ab1a18b7a164ad6c6c9a56d2cffe：新增无I/O的ScheduledWork合并事件/改期/取消/领取/续租/完成/重试状态转换；JobRegistry同名不同处理器拒绝替换，同实例重入允许。没有启用任何调度器或费用消费者，没有数据库DDL。
- task-core新增22项定向测试，覆盖执行中事件不丢、改期/取消优先、过期接管token、重试保持逻辑revision、租约更新及并发重复注册。测试中的期限为合成输入，不下传业务deadline。
- 编排器既有台账登记本任务Owner；测试/构建600秒仅计本批阶段。普通磁盘输出/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/，Gradle串行、512m/SerialGC、原依赖完整性入口。未创建生产包，不部署。
- 首次验证在Gradle启动前因argparse REMAINDER参数顺序错误失败；保存core/result.json和gradle.log。修正为选项在task_id前后再接命令，保持源码不变，core-2重新验证；原失败不重标，累计预算不重置。

## 实现切片1验证完成（2026-11-09）
- 首轮真实测试发现ScheduledWork.nextWakeAt/retry将nullable Long与primitive long混用三元表达式，导致空闲/取消路径自动拆箱NPE。已通过既有fail入口归因；用显式分支修正，没有删除或弱化测试。
- 修复候选d1f418042099a09fc8bcabb7f4141f90f416f5ff，tree ac47aa0e9762384975abb8632e1e5b916c67ab0c。core-3真实重跑22项全部通过（19状态模型+3注册），validateLayering通过。源码分支干净，未push/合入/发布。
- 证据：/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/core-3/result.json、gradle.log、build/jia/task__jia-task-core/test-results/test/。前两次失败证据保留；三个driver记录的测试/构建阶段累计72.703秒。另一次systemd命令因/usr/bin/python3.11不存在在启动前直接失败，随后使用实际/root/.local/bin/python3.11；未启动额外Gradle，也未重置预算。
- 当前只完成无I/O模型与注册冲突处理。数据库持久化/CAS、Redis协调、余额事务唤醒、收费接入、旧调度迁移、生产迁移/部署均未完成；测试通过不表示整项完成。
- 已核对公共锁：RedissonDistributedLock支持watchdog/固定租期，但ILock无失锁通知，unLock只先查isLocked，不能作为调度所有权凭据。task协调适配须保持锁线程归属与领取前持有确认；不顺手改全项目公共锁。数据库领取短事务提交后才调业务，资金期次幂等仍不可省。
- 下一步在同一worktree固定调度持久化表与CAS存储，并补真实事务/并发验证；不可先启用cron或费用。现行设计/tasks已同步实际状态。

## 实现切片2：持久化/并发领取（2026-11-09）
- 候选7e4e31d3c97872dc4387ef4f010d576577548647，tree 6e15d1b77cb8525a2884a6276f08190705005bae；仍为同一隔离工作区/分支，未push/合入/发布。新增ScheduleKey、ScheduledWorkRow/Mapper/XML、DDL及ScheduledWorkStore；没有新框架、没有业务费用依赖、没有自动执行DDL或启动调度。
- 存储采用tenant/client/handler/business/node键；进程scope在存储边界落实，节点/租户在排序LIMIT前过滤；索引next_wake_at。业务登记加入原事务；worker不允许嵌入业务事务，以短事务领取/完成/续租，不在行锁内执行业务或网络调用。数据库时间用于claim，版本与token控制迟到结果；过期claim可恢复，运行中新事件保留。
- 首候选6a604cc13954ee5b276f55f96ac21695efc5d62f真实MySQL测试14项中11项失败：现行TaskTenantConfiguration虽忽略新表，仍由JSqlParser重写SQL，把FOR UPDATE SKIP LOCKED移到ORDER/LIMIT前。已沿fail归因并保留storage-1证据。修正仅给显式分区的新Mapper添加InterceptorIgnore(tenantLine=true)；未改旧表隔离或删回归。
- storage-2结果PASS：14项真实MySQL测试（独占8.0.21进程+生产DDL/SQL/现行租户插件/Spring事务）、22项core测试、validateLayering。额外legacy-1在相同候选执行原TaskServiceImplTest、TaskPlanTenantPersistenceTest、TaskControllerTenantTest，共14项全通过。合计50项，无跳过。
- 证据根 /home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/：storage-1失败、storage-2成功、legacy-1成功各有result.json/gradle.log/XML；入口verify-storage.py/verify-legacy.py，前次driver保留storage-1/driver.py。与前切片合计记录测试/构建阶段238.273秒，未重置600秒预算；无生产打包/安装。
- 纠正一次测试工具的内存开销：首storage driver对1.1GB mysqld一次read_bytes做摘要；后续改为hashlib.file_digest流式读取，同一文件摘要绑定不变。只修改任务自己的验证脚本。
- 已确认两个自建mysqld停止后，仅删除其mysql/data临时库，保留mysql.log及XML/日志/receipt；精确路径见fixture-cleanup.json，未清其他任务/生产库或共享缓存。首次清理命令因默认Python3.6不支持subprocess text参数在任何删除前失败，使用Python3.11完成。本任务仍活动，无最终发布包登记可回收。
- 恢复测试为重建store和接管过期claim，并非实际容器/Redis宕机。最小业务事实表回滚不是实际钱包消费验证，未宣称多容器调度或自动扣费已完成。
- 下一步：同一worktree实现调度运行与Redis唤醒/所有权适配，固定灰度禁用与节点归属，再接余额可靠登记和费用消费者；旧调度逐项切换。当前无需用户业务确认。

## 连续实现切片3～5（2026-11-09，未上线）
- 用户明确无需确认时直接继续；本轮连续完成协调运行、条件装配、统一余额事实扩展和Agent订阅适配，未逐阶段要求确认。
- task候选176f71d0d6：新增ScheduleService、ScheduledJobHandler、typed invocation、RedisScheduleWakeup/Coordinator、有界ScheduledJobRunner、生命周期与配置。使用现有JobRegistry，旧handler不自动迁移；ApplicationReady后运行，fixed-tenant灰度不创建runtime。集群/本机节点协调器共享worker容量，本机claim续租不依赖集群owner。
- coordination-1编译失败：修改execute失败信封时误改status Map返回；已fail归因并恢复status，未删测试。审查同时补SKIP LOCKED空领取退避，避免到期索引热点空转。修复后coordination-2 67项PASS；加装配/灰度验证后coordination-3 70项PASS（含MySQL20、Redis双客户端6、core22、旧业务14、runner3、controller2、配置3），分层均PASS。
- 余额事实候选791b3a536d：EconomyAvailableBalanceListener为同步同库事务扩展，posting完成写入后仅USER/AVAILABLE净正增加通知；replay无新通知，监听器失败回滚钱包和已登记事实。没有额外Agent查询或执行扣费；现有构造接口不变，无观察者不新增I/O。复用economyHostingRegression入口，balance-1 43项H2事务回归PASS（26posting+17hosting），分层PASS。
- 当前候选049c069cd2dca32988ecb35bcdad8dcfab6ea79d，tree ab1b8b573faf1c4bec8a62148bd2f8915a782170：HostingRentBalanceWakeup在auto-renew-enabled时订阅余额事实，同事务登记用户键，立即到期0避免主机时钟差；与进程scope不一致拒绝，不将其他tenant重标为当前tenant。balance-adapter-1复用managedHostingRegression，4项PASS，分层PASS。
- 手动JobController执行失败不再被包装成功，通用权限无法调用ScheduledJobHandler；status响应恢复原样，空请求正确拒绝。定向搜索当前Web/src未发现/job/execute消费者，未扩改Web。
- 仅只读核实本机Redis PID4136实体/home/isp/apps/redis/bin/redis-server、root会话cgroup；未读凭据、未连生产Redis做测试、未改生产进程。真实协调测试用自建Redis及独立客户端；无锁降级测试是异常注入，不宣称生产网络故障验收。
- 同一证据根/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/；coordination-1失败、coordination-2/-3、balance-1、balance-adapter-1分别保存完整commit/tree、argv/fixture哈希、日志/XML/result。源码、测试通过与安装分开；未push/合入/生成最终生产包/迁移/收费启用。
- 自建MySQL/Redis进程均已正常结束；仅清理coordination-2/-3中本任务已停止mysql/data，保留mysql.log/redis.log/XML等，见coordination-fixture-cleanup.json。不清理生产或他方缓存。

## 测试/构建预算例外待确认（非业务规则待澄清）
- 已记录同批累计591.831秒（含失败和等待）：core0.092、core-2 37.060、core-3 35.551、storage-1 73.248、storage-2 65.749、legacy-1 26.573、coordination-1 45.832、coordination-2 71.864、coordination-3 81.164、balance-1 51.186、balance-adapter-1 103.512。600秒剩8.169秒，不按阶段/重试重置。
- 当前固定源码049c069cd2dca32988ecb35bcdad8dcfab6ea79d；最后测试已成功，无在途构建。下阶段还需实际钱包/租约/调度全链MySQL及自动续费/锁定/收尾回归，按现有一次模块回归51～104秒实测，不可能在8秒内完成。申请总测试/构建/打包预算延长至1200秒（额外600秒）；不包含安装/健康等待，不下传为业务deadline。
- 未获例外前不启动下一次Gradle/测试/打包，不拆批规避；保留已通过精确输入证据并继续使用串行、普通磁盘、compile-only缓存，必要失败不发布。预算批准后按后续真实候选固定SHA再运行，不复用旧候选冒充新测试。
- 未完成：真正的自动续费/到期/超过15天移除处理器、已有技能首期/周期收费、资格入口收窄、收尾交接私有数据隔离、cron/旧调度迁移、全链故障验收及受控发布。当前开关禁止提前启用，余额订阅成功不等于租约扣款已实现。

## 预算例外已批准（2026-11-09）
- 用户明确回复“允许”：仅本批测试/构建/打包累计上限延长至1200秒，既有591.831秒计入，余608.169秒；不重置默认600秒规则、不改变发布/生产扣费授权。
- 原Owner在同一worktree继续，保持串行磁盘构建、真实失败留证、必要回归与资金事务边界。

## 租费消费者切片（2026-11-09，未上线）
- 固定候选f588988e4a55cf67f077374ec06b9cb8cbe3886f，tree 4e79db135642c6a4c4e366e6542cf0e60ac0a8c8。新增固定30天自动续费、余额不足LOCKED、严格超过15天转FINISHING（保留实例slot/身份，关系收尾处理器尚未实现）。租期从成功付款后的数据库时间开始；锁定重查不重置锁定时间，无锁定期补收。
- 到期/余额事实统一合并为用户键hosting-rent.reconcile-user；按paid_through/lease_id排序、100行keyset分页，付不起不阻塞可支付项。业务根锁→SYSTEM/USER排序账户→调度登记；整页资金处理后才登记，避免首行FINISHING先锁调度、后行付费再锁钱包的真实反转风险。
- 新期内部直接RENEW_HOSTING_RENT从本USER/AVAILABLE到系统租金收入，无外部调用/无必要预占中间态；保留通用posting事务/余额/幂等/借贷平衡。幂等取scope+lease+旧paidThrough，不用调度revision。初始/手动续期成功也同事务通知租约变化，economy不依赖task。
- 独占MySQL8.0.21实际DDL/Mapper/钱包posting/调度store/回调集成15项、余额适配4项、原资金H2事务43项，renewal-1共62项PASS、零跳过，validateLayering PASS。覆盖真实发放→余额事实→领取→续费、并发重入、跨分区、101个付不起之后仍续费尾项、定界15天、钱款/租约/调度同回滚、并发入账与先收尾后扣费锁序。
- 证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/renewal-1/{result.json,gradle.log,build/}；本轮346.382秒，累计938.213秒，批准上限1200秒，剩261.787秒。耗时包括配置/编译（agent-service约40秒）、独占MySQL初始化/15项集成（managedHostingRegression约81秒）、原回归约8.5秒及等待；不是20分钟统一业务deadline。
- 当前开关仍禁用，结构SQL只落源码，未迁移/安装/启用收费。FINISHING只登记可靠收尾待办，不能冒充已移除关系/已隔离私有Runtime。首期技能清单/金额、自行部署默认价与存量30天过渡、真正收尾/私有交接、调度迁移仍未完成。

## 资格入口收口与恢复审查（2026-11-09）
- 候选c800400c3d：租期准入移到AgentTaskExecutionGrantServiceImpl的首次承办事务（原幂等重放不重验）、ChatDeliberationService新密议请求接受事务（请求重放不重验）；HostingRentWorkAdmission使用租约锁定读使准入与状态变更一致。移除WorkItem claim和HallActionDispatcher的重复费用门禁，旧事项继续执行；保留原身份/成员/授权/版本检查。既有技能安装/升级准入保留，新承办目标重派仍有资格检查。
- admission-1的Agent门禁3项、授权54项、已有事项领取34项通过，零跳过。随后Chat bf08FormalFlow编译失败，原因是原sourceSet包含AgentWebSocketHandlerTest却漏含已存在的UnifiedRuntimeTestSupport；没有执行Chat测试，不称整轮成功。已通过fail归因，保留原log/XML/result，源码补入同一个既有辅助类，不删原回归。
- 审查发现恢复缺口：只在回调最后登记用户下一期限，可能在A续费已提交/worker退出后把B更早到期漏到A新期末。修正把每页最近期限读取与可靠登记放入原资金事务；不新增每Agent定时扫描、补偿后台或外部网络调用。增加“业务提交后没有任何handler后处理仍保留B期限”和“最终期限登记失败整体回滚”两个真实MySQL用例。
- 当前固定候选d06503d0c3fe3c92a87084cf7f3f0dd854623443，tree 5dcec3483837817b52d9f4716c2aca0cbfc10f1d，工作区干净；修正源码尚未运行。原续费15项/余额4项/旧资金43项的PASS只绑定f588988e4a，不能重标为此候选通过。
- 独占测试MySQL已正常结束，只清除本任务renewal-1/mysql/data，mysql.log/XML/receipt/driver/build保留，精确记录renewal-fixture-cleanup.json；没有清理他方缓存/生产数据。两个本任务构建单元均停止，无在途Gradle或测试MySQL。
- 未push/合入/生产打包/安装/DDL/开关启用，关系收尾处理器、私有隔离、首期技能清单费用/自行部署/存量过渡、cron和旧调度迁移、最终全链回归与发布仍未完成。

## 再次预算例外待确认（仅构建验证时限）
- 本次续费回归346.382秒，准入回归114.118秒（失败照计）；加前591.831秒，累计1052.331秒，1200秒上限剩147.669秒。
- 当前d06503d0c3修正影响economy-api/service与Agent消费者，还需完整重跑真实MySQL新增恢复用例及原资金回归、Chat派发/密议与准入回归、validateLayering；不能只凭前一候选测试完成。近期费用链实跑346秒、准入113秒，无法可靠安排在剩147秒内完成。
- 拟申请累计上限延长至1800秒（额外600秒），仅本批，不修改默认600秒或生产服务deadline。沿同一worktree/串行compile-only缓存和磁盘输出，保留失败证据，不删回归、不拆批重置。获批前不再启动测试/构建/打包；待统一固定此候选所需selector后执行，不创建新框架。

## 时限范围更正（2026-11-09用户最新澄清）
- 用户明确：10分钟只限定单元测试、构建和发布，不限定回归验证。根AGENTS已载明，工具入口说明同步；规则写入不代表混合Gradle driver计时已经适配。
- 上述1052.331秒为包含集成／回归的历史合计墙钟，不是新范围下受限阶段累计，原receipt不改写。此前仅据该合计提出的1800秒例外请求不再作为继续回归的依据；需从原任务计时与XML核实单元测试、编译等实际耗时，不能把混合任务整体豁免。既有本批1200秒批准保留记录，不推定新增发布授权。
- 下一步先调整本任务验证入口的分阶段计时，避免整体RuntimeMaxSec误杀不限时回归，再验证d06503d0c3候选。此次仅同步规则，未执行新测试、构建、安装或生产操作；未将待验证修复宣称通过。

## 恢复与准入联合验证完成（2026-11-09，仍未上线）
- 固定受测候选2dd788cb0bda04a5d5f24f78ecc3a95da6c74bba，tree 28be6399b0d268b856ba35a5b15db975fc8c9926。combined-3全部196项PASS、无失败/跳过，validateLayering PASS：真实MySQL续费17、余额适配4、准入3、授权54、旧事项领取34、派发21、密议真实事务20、原钱包/租金真实事务43。覆盖最近期限原子登记与失败回滚、锁定后新请求拒绝且原幂等重放不重验、派发不重复租期门禁。
- 原combined-1在Gradle前因Owner处于implementing而被工具拒绝，已归因并切targeted_verification；combined-2续费与Agent用例通过，但Chat编译暴露FinalReplyTimingTest这一既有辅助依赖未包含。补齐同源集且检查辅助类依赖后，combined-3通过，不删任何既有测试、不伪报原失败成功。
- 证据根仍/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109；combined-1/-2/-3各保留driver/log/receipt，combined-3/test-summary.json绑定9份XML摘要。确认无进程引用后只删除combined-2/-3的自建MySQL data目录，见combined-fixture-cleanup.json；mysql.log、构建输出与全部证据保留，没有清理他方/生产数据。
- 本任务验证driver已用Gradle suite事件分别记录真实MySQL/H2回归区间；任务名含Regression的Mockito单测仍计受限时间。旧证据只按明确真实集成类XML时长排除，其余未知开销保守计入，不改旧receipt。没有对整个包含不限时回归的systemd单元设置墙钟RuntimeMaxSec；仅监督本任务子进程的受限计时，不影响应用服务。
- combined-3交付验证墙钟156.227秒，其中回归48.786秒、受限阶段107.433秒。timing-reclassification-20261109.json汇总保守受限累计上界1148.902秒，原批准1200秒剩至少51.098秒；不是包含回归的总墙钟。源集辅助类修正已提交，未push/合入/打生产包/安装/迁移/开启费用。

## 主动移除的资金边界候选（2026-11-09，尚未验证）
- 当前HEAD bd7d8d34c85838d4e5bd2ea0a9836d547c161715，tree 6c2f97b1e1462dbe261b255a5265fcda1055ffc5，原worktree干净。HostingRentRenewalService.stopRenewal在调用方同库事务内锁租约、核对付款人，将ACTIVE/LOCKED转FINISHING并可靠登记收尾；保留paidFrom/paidThrough/实例/绑定/live_slot，不退款、不重扣。重复停止无新事件，和续费以同一租约根锁排序。
- 新增5个真实MySQL用例：保留租期/身份/slot与幂等、停费后入账不复活、错付款人/禁用分区/未付部署拒绝、外层移除失败全回滚、移除与续费竞争。只做了diff检查，未运行；前196项PASS不绑定此候选。prepare的verify-combined.py指向combined-4、至少201项，尚未启动。
- 这是资金责任层接口，不是完整“移除好汉”已完成：HTTP/Agent关系收尾与Runtime私有清理尚未接入，现行旧unbind不能原样复用；没有修改现有业务入口或启用开关。后续须在实际关系移除事务调用，保留旧执行身份，待旧事项/执行/技能操作结束与私有交接确认后释放邀请资格。
- 尚需首期技能固定清单与两种部署/过渡收费、技能安装升级费用接入、cron及旧调度迁移、最终受控发布和真实业务验收。

## 受限编译时限待确认（回归已排除）
- 原批准本批1200秒按新范围重算后仅余保守51.098秒。新候选改变economy-api/service及Agent测试编译，近期联合验证受限阶段107.433/117.596秒；不能可靠在51秒内完成必要编译与单元测试，不先盲跑到强制中断。
- 请求本批受限阶段累计额度延长到1800秒（额外600秒），回归仍单独计时、不受上限；未重置默认600秒规则、未新增生产发布授权。保留原源码/单工作区、串行、普通磁盘、编译缓存与真实证据。批准后先验证bd7d8d34c8，再继续关系/私有交接闭环；没有在途构建或测试库进程。

## 单次执行规则替换累计预算（2026-11-09用户明确更新）
- 用户明确“10分钟只限定单次构建发布，异常重试重新计算”。每次执行600秒、异常重试从零计时；回归继续单独记录且不限时，不跨候选/开发过程/尝试累计。根AGENTS、工具入口说明和专题任务口径已同步。
- 前述1148.902秒累计上界、剩51.098秒和1800秒申请保留为历史，已不构成当前阻塞；无需用户批准该累计扩时请求。此前失败与PASS证据均不改写。
- 当前源码仍bd7d8d34c85838d4e5bd2ea0a9836d547c161715。继续时须先将本任务verify-combined.py从读取历史remainingSecondsLowerBound改为单次600秒计时，历史reclassification文件只读保留，并沿既有编排入口清除过期waiting_user状态；共享工具的适配范围另核实，不能把文档更新当成脚本已经改造。
- 此次仅更新规则及交接，不运行测试/构建/发布、不改生产开关或数据。

## 单次预算工具接续与主动停费验证（2026-11-09）
- 本任务verify-combined.py已移除读取历史累计remainingSecondsLowerBound，单次boundedLimitSeconds=600；真实回归suite事件继续单独计时，失败重试需新输出并保存前次driver/receipt，不对整个含回归的unit设墙钟截止。共享Web/API发布入口未据此宣称已全部适配。
- combined-4固定bd7d8d34c85838d4e5bd2ea0a9836d547c161715/tree6c2f97b1e1462dbe261b255a5265fcda1055ffc5，72项PASS、零跳过、validateLayering PASS；续费/主动停止真实MySQL22项、门禁3、余额适配4、原资金H2事务43。没有重复原授权/派发/密议整套196项。
- 当次总墙钟172.013秒，回归42.035秒，受限129.972秒；满足单次600秒。主动停止接口验证完成，不等于Agent移除HTTP/关系解除/Runtime私有访问隔离已接通。
- 费用链调查确认SkillManagementService已有原子reserve/capture/refund及结果未知保留/重试幂等，不另建收费框架。现行旧实现按商品登记价、COVERED升级及保留权益重装免单，与用户50/20文规则冲突。
- 候选eee12fd81e4aa9fca50f026e60dfd4e34823aee7/tree4ee2c26e6ab3881186a4b591c4ce245418343ab3：economy-core固定操作费50/20；新quote/create使用原订单资金闭环，COVERED/PAID资格政策仍保留但不免操作费，未接纳旧免费quote需重报；已接纳操作仍原事实重放。目录安装价显示50文，旧已退役购买HTTP不恢复。删除只为免费重装查历史权益的分支，旧历史执行授权/摘要核验保持。
- 当前skill-fees-1仅运行现有SkillManagementTransactionTest真实MySQL全类及分层；覆盖范围包括安装、升级、重装、失败/未知结果、并发、权限/身份和旧执行快照；新增固定价/报价不冻结/49文不足/客户端零价拒绝用例。结果待收取，未上线、未启用收费开关。

## 技能固定操作费与租期准入补漏（2026-11-09，未上线）
- skill-fees-1启动失败并已归因：独占MySQL socket路径超过107字节，未运行业务用例。6599660ef49cd3290411b6f991b37f10361bcf83修正夹具支持短的普通磁盘socket根，数据/日志仍放批次目录，退出只清理自有socket，不改生产数据库/共享临时目录。
- skill-fees-2绑定6599660ef4，真实MySQL47项中45通过、2失败；墙钟285.620秒，真实回归209.669秒，受限75.951秒。失败为旧测试错误预期：COVERED升级仍应收20文并新增订单；历史adoption凭据被篡改仍须拒绝，即使重装收费也不能跳过原卸载/历史完整性证据。保留失败日志/XML，不放宽生产授权校验。
- 审查纠正此前“技能准入已保留”的不准确结论：旧SkillAgentVersions仅在ready=true时调用租期门禁，而当前SkillManagementService统一传false，因此新安装/升级实际未受该门禁保护。ee943d7184将新quote/create（先处理幂等重放）接到HostingRentWorkAdmission集中政策：INSTALL/UPGRADE要求有效租期，FINISHING拒绝所有新技能变更；LOCKED仍允许ENABLE/DISABLE/UNINSTALL。旧回执/结果/retry/reconcile/已接受重放不加租期门禁；不在执行派发层重复拦截。
- 责任与锁：Agent既有身份/Runtime/CAS锁后、技能状态与钱包写入前锁租约；续费只有租约→钱包→调度，不获取技能actor/identity。后续关系收尾不得引入租约→身份而与新技能入口形成反转；身份交接与租约操作必须按实际共用根锁序完成。
- 新增3项消费者真实MySQL事务回归（租期状态mapper为明确模拟边界，不宣称真实租约并发）：欠费后新报价/已报价确认拒绝且无部分资金/命令写入、已接受安装在FINISHING后仍重放并完成扣款、收尾拒绝卸载但锁定仍允许停用；集中政策另加2项单测，覆盖全部操作及无schema零查询。
- skill-fees-3正在验证ee943d7184：50项真实技能事务、10项推荐单测、5项租期政策单测及validateLayering。上一driver写死至少60项，但原类实际47项；本次按固定selector核对65项/3份报告，不能通过删用例凑门槛。结果待收取，尚未合入/生产打包/迁移/启用。
- 移除/交接仍未接通：现行AgentPersonaProvisioningService.unbind→AgentHostedBindingTransaction会拒绝忙碌Agent，停用身份/API key并清空Runtime绑定；不能把stopRenewal接在此旧流程上就称“只解除关系”。FINISHING处理器、实例再次邀请、私有Runtime撤权仍需完成。

## 技能固定费用验证通过（2026-11-09）
- skill-fees-3绑定完整commit ee943d71845496e31bf55a95936ce54dc9f75d46、tree 5186f7dd19d28c4c63a728ba22ed57edb2e50239；65项PASS、无失败/错误/跳过，validateLayering PASS。50项真实MySQL技能事务、10项推荐单测、5项集中租期准入单测；租期状态在技能事务类中为明确模拟边界，真实租约并发仍沿独立续费切片覆盖，不声称此次跨租约/身份并发已验收。
- 墙钟324.510秒，其中真实回归175.616秒、受限阶段148.889秒；单次600秒内。未打生产包/合入/部署/迁移/启用开关。原skill-fees-1/-2失败保留，不重标成功。
- 证据目录/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/skill-fees-3/：result.json、gradle.log、test-summary.json（逐XML摘要）、driver.py、regression-timing.init.gradle及原XML。编排证据key fd424ffd6264984ef47ae44cad8c4f4f933e88b8a74e19cece7d9a0801a5fa28。源码工作区干净；运行结束。
- 已核对SkillApiExceptionAdvice处理HostingRentApplicationException，经原技能错误合同返回AGENT_FORBIDDEN，无新wire枚举/猜测兼容。报价与确认各自检查是状态可能在两请求之间改变，不在回执/旧执行反复检查。
- 仅在确认无进程/cwd/fd引用后清理本任务combined-4/mysql/data（约167MB），日志/回执保留，记录combined-4-fixture-cleanup.json；未清理生产、其他任务或未知缓存。技能夹具tmp结束后已无data目录，没有声称保留不存在的MySQL数据。
- 下一动作：关系移除/收尾闭环。先固定当前binding.status同时承担邀请关系与身份认证的实际调用方；新移除不得直接复用旧unbind（其会停用身份/清绑定）。统一责任层保持旧事项及已接受技能操作，收妥进程/私有访问撤回证据才释放重新邀请。之后首期技能清单/自行部署/存量30天、取消路径、cron和旧调度迁移及完整受控发布。不存在待用户确认的业务问题；尚未完成项目，不标完成。

## 精确租约移除接口（2026-11-10，未上线）
- ee72d6c3b787269dd8cd04c3dc50e38a21f5d596新增主动移除应用服务及HTTP候选：DELETE persona bind必须携带确认时固定的agentId/leaseId；认证付款人、owner、persona、当前绑定一致后，按身份/绑定→租约→调度顺序停止续费进入FINISHING。不会停用执行身份/API key、清Runtime绑定或检查忙碌后拒绝；不依赖当前套餐价格和Provider可用性。
- 此候选尚非完整移除：目录投影、Web快照确认、真正FINISHING处理器及Runtime私有交接未接通；旧unbind实现仍待清除，不提前启用/发布。首次邀请报价尚需阻止未交接的live lease（reserve已有阻止），已接受重放继续保留。
- removal-1固定上述候选，47项执行46通过/1失败：HTTP body辅助器只校验允许字段，不保证必填；空body对象会把null传入服务。真实租约MySQL25项通过，不能以此把整轮重标成功。已通过fail记录根因，6b6db73257c6b73d54194b0e107c4f584c4ff22a使用原required字段解析修正，不添加框架或兼容退路。
- removal-2正在固定6b6db73257/tree5763a1206005993a31cc96337f0b4ed5df192960验证原47项（续费MySQL25、application8、reprovision5、controller9）和validateLayering；受限单次600秒、真实MySQL回归单独计时。证据在/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/removal-{1,2}/，首轮driver已保存。无生产数据/安装/开关操作。
- 契约已写入beta-wen-billing.md主动移除接口节，明确前端确认前固定租约，确认后不改用新的租约；未宣称Web已经实现。
- 后续清理调查：不仅有现已未调用的AgentPersonaProvisioningService.unbind→prepareUnbind，repair的SUSPENDING分支仍调用completeUnbind。故不能仅删除unbind方法就宣称旧破坏性恢复入口退役；关系切换时须一并处理repair可达路径，保留新方案自身恢复，不自动重放旧停用意图。

## 移除入口定向验证通过（2026-11-10，未上线）
- removal-2固定6b6db73257c6b73d54194b0e107c4f584c4ff22a/tree5763a1206005993a31cc96337f0b4ed5df192960，47项PASS、零失败/错误/跳过，validateLayering PASS。真实租约/钱包/调度MySQL25项、application8、reprovision5、controller9；身份边界在移除应用集成中模拟，不能当作Runtime或完整跨用户验证。
- 墙钟132.308秒，真实MySQL回归39.457秒，受限92.847秒。result/gradle.log/test-summary（XML摘要）/driver/timing init及XML保留同批目录。首轮失败原样保留，未发布失败包；本轮未打生产包/合入/部署/迁移/启用开关。
- 编排已回implementing继续完整关系收尾、同实例私有交接、首次费用和调度迁移；目标未完成。当前无需业务确认，Web未更新，不能单独上线API候选。

## 邀请资格与锁序接续（2026-11-10）
- a85be4271258b92b456c135fc4899412a6c86dc1/tree0830f40c8c2274f80dfe825da6d75063e81cfa2c：INITIAL新报价在当前身份/绑定后检查live lease，ACTIVE/LOCKED/FINISHING等未释放slot都拒绝；原quote事实重放在新准入之前保留。原reserve的数据库live-slot唯一性/事务检查保留；不依赖前端禁止按钮保证安全。
- 删除bind确认在persona/binding之前的无结果lease FOR UPDATE，实际live-slot检查由ledger.reserve在已有绑定锁之后负责；新增3项测试覆盖未释放报价拒绝、原报价重放、确认绑定→资金顺序。invitation-1正在验证上述固定候选50项及分层，不能预标通过。
- **尚有真实锁序依赖需统一整改**：renewalQuote/renew非重放、reprovision及HostingRentReconciler.freeSnapshot/snapshot、ManagedHostingCredentials.authorize存在lease→binding；新移除和技能入口为binding/identity→lease。不是修了bind就全链解决。须在这几个真实依赖处统一绑定根先于租约，并覆盖原托管/reprovision/凭证回归；不能简单撤销绑定锁或授权，不能在调度handler持有lease再调用身份交接。
- Web当前主工作区在JuyiHall/useHallData及原型有他方脏修改，未覆盖；尚未创建Web worktree。后续确需一份隔离Web工作区，不能从主工作区直接批量stage或reset。
- invitation-1在测试编译失败（继承的setClientId返回BaseEntity，链式setStatus不可见），未运行业务回归；已fail归因，a99be009f95765d930448b6c804289d2f43bc6ce只拆开fixture的继承setter。invitation-2正在重验50项，旧失败保留，不削减用例。

## 邀请报价准入验证完成（2026-11-10，未上线）
- invitation-2固定a99be009f95765d930448b6c804289d2f43bc6ce/tree31f4a158fc706052ab65ff776d6a6af97e36d081：50项PASS、零失败/错误/跳过，validateLayering PASS。新增报价/重放/锁序3项仅验证当前应用边界，不宣称全链并发无死锁。
- 墙钟139.800秒，真实MySQL回归55.133秒，受限84.652秒；证据/result/driver/timing/XML摘要在invitation-2目录。invitation-1编译失败保留；没有在途验证进程，编排回implementing，API工作区干净。
- 下一动作明确：同一hosting责任层统一renewalQuote/renew/reprovision/Reconciler/ManagedHostingCredentials的binding→lease锁序（已有credentials测试断言旧顺序，需要按真实风险更新并补并发），再完成FINISHING和私有交接。未做Web、未合入/发布，原目标保持完整。

## 托管恢复锁序统一候选（2026-11-10）
- b77e8d20c8f4e2de88340f1b369e591c7d1114ca/tree757e07787ccc644539dae194cae97cb938aef59a：renewalQuote/renew/reprovision先锁现有绑定再租约；Reconciler付费/免费快照复用现有精确tenant/client/persona锁查询，绑定→intent→lease，再核对原lease绑定ID，旧发现行不能指向新关系。没有新DAO/锁框架/周期扫描。
- 安装授权保留Runtime现有installation-first fence，随后绑定→intent→lease；不能把安装锁移到绑定之后而与注册/会话链反转。原身份、安装摘要、原付款人、CAS和事务校验不删除。
- settle保留上一快照的intent仅作发现键，进入新事务后重新按绑定→intent→lease读取权威事实；直接使用重新锁定的intent，删除原先提前取intent锁及重复查询。未把I/O前的旧状态当作最新授权。
- 两个新增真实H2争用测试：一个事务先持绑定根等待恢复开始，随后取租约/intent根；恢复必须先等待绑定，不能持有金融根造成反转。该测试覆盖锁序行为，不等于实际MySQL跨租约身份或Runtime进程验收。原托管/免费恢复/安装关联、续费与精确移除共73项及分层正在hosting-locks-1验证。

## 托管锁序验证通过（2026-11-10，未上线）
- hosting-locks-1固定b77e8d20c8f4e2de88340f1b369e591c7d1114ca/tree757e07787ccc644539dae194cae97cb938aef59a，73项PASS、无失败/错误/跳过，validateLayering PASS：真实MySQL续费25、application12、reprovision5、controller9、reconciler11、credentials11。原手工续租、免费恢复及付费恢复结算的锁序断言同步；H2并发根锁用例通过，不能称真实多容器验收。
- 墙钟165.947秒，真实MySQL回归41.087秒，受限124.844秒；混合H2/mock类本次仍保守计入受限时间，没有为豁免改名。证据/test-summary逐XML摘要/driver/timing init在hosting-locks-1目录，未发布生产包或改数据/开关。
- 编排回implementing，当前API工作区干净，无在途验证。下一步实际FINISHING关系与Runtime交接；不要再次把本轮锁序整改列为未实施，但仍需最终全链回归。完整目标其余首次费用、存量过渡、前端、cron/旧调度迁移和上线仍未完成。
- Runtime源码入口已只读确认/home/isp/wsps/chcbz/isp-install/conf/codex-bridge，不能编辑app安装目录；工作区规则/固定源码/是否有他方修改需动手前重新核对并显式携带根AGENTS与接口规范/RB-1。未对Runtime做任何写入。

## 2026-11-10 接续：欠费即收尾与满15天自动终结
- 用户明确继续实施。Owner仍task-scheduling-owner；API复用干净worktree `/home/isp/wsps/worktrees/task-scheduling-api`，base b77e8d20c8f4e2de88340f1b369e591c7d1114ca/tree757e07787ccc644539dae194cae97cb938aef59a；Web e76d0c1候选保留，178通过/1失败尚未归因，未上线。根仓库他方修改不覆盖。
- 最新规则：失败即可恢复收尾，满15天（>=）自动验收已交付事项、取消未完成/失败事项并分别扣除/释放预占，进程退出后清理再解除。保留公共资源、实例与原用户后端历史。内部LOCKED=可恢复收尾，FINISHING=最终解除，避免新增兼容状态；不再允许LOCKED期间新增技能启停/卸载。
- 第一切片收口租期截止/调度与集中准入：15天从到期时间起算，延迟唤醒不得延长宽限；精确deadline先于余额；全新技能变更复用单一准入，旧受理/执行不改。回归覆盖deadline前1ms/恰好deadline、错过到期唤醒、无部分资金/命令写入与旧操作完成。完整事项终结和Runtime交接仍未实现，开关保持关闭。
- 当前遵守根AGENTS最新计时：固定源码批次受限阶段累计600秒，真实集成回归单列，不采用旧driver无条件重试重置口径。本次不操作生产数据库、不清理生产HOME、不发布。

### 自动验收实际依赖核对（2026-11-10，只读定位，不代表实现）
- 现有正式验收`AgentTaskFormalDeliveryDecisionServiceImpl.decide`在事项根锁事务内调用TaskBillingService.capture，取消`AgentTaskCancellationServiceImpl.cancel`在同一根锁事务内撤销执行/讨论/授权并release；自动处理应复用这两条资金路径，不另写扣款。取消已支持failed，不把失败当自然完结遗漏预占。
- 自动验收不能直接假扮用户调用：当前正式交付事件只允许role/task_owner，`AgentTaskWorkspaceEventValidator`也强制该身份及严格payload。需要在责任层增加明确系统自动验收来源，并同步事件合同、持久化review归属和相关消费者/定向回归，不能仅绕过事件校验或伪造用户验收事实。
- 调度处理不可持租约锁后再取事项根锁：现有承办链事项根→身份/绑定→租约，自动收尾应按该真实锁序或分阶段不可逆状态处理。任务发现须在SQL排序/LIMIT前限定原关系的tenant/client/owner/Agent，不能扫描跨用户事项后过滤。
- Web旧失败已定位：基线8b1b77c和候选均在panel-overlay的v-if与key之间含help-replay的v-show，测试硬编码属性相邻而失败。5d1124c仅修测试为同一overlay内分别验证v-if/key，未改变产品遮罩/代际逻辑；原178/1失败保留，待重新运行。

## 欠费收尾准入/截止切片验证通过（2026-11-10，未上线）
- API 01d9560e1c37bb6120549091ff8d75daff80d13a/tree5440f0454c53c0018e5943ab29845a768ea041fb：到期失败即停止全部新技能变更，LOCKED表示可恢复收尾；>=15天优先FINAL FINISHING，不再扣费；锁定时间按实际到期而非唤醒时间，延迟调度不延长宽限。旧执行/已受理回执入口未增加租期拦截。
- arrears-finishing-1因系统Python3.6不支持driver参数而在Gradle前失败；-2租期28+准入5通过，技能夹具因socket路径过长未执行业务用例，保留真实失败。已归因复用既有短普通磁盘socket配置；未修改源码重试预算不重置。
- arrears-finishing-3固定同源码83项PASS（租期真实MySQL28、集中准入5、技能真实MySQL50），零失败/跳过，validateLayering PASS。墙钟262.418秒，真实回归204.726秒，受限57.689秒；与-2累计受限154.805秒（另有Gradle前不足1秒启动失败），未运行正式生产打包/部署。测试结果含逐XML摘要、精确driver/timing存档，证据位于既有任务目录。
- Web 5d1124cc2bc12e1d00cf9739eaebcc519a74a676/treef18997409a6e4f6301dc6a649cc79ff6312bf708：web-removal-2重新运行3个定向文件，179项PASS、零失败；墙钟41.947秒。修正同一遮罩内属性非相邻导致的旧测试失败，未放松身份/会话代际保护；不宣称真实浏览器PC/mobile验收或完整租期页面完成。
- 当前没有在途验证，API/Web工作区干净，未合入/发布/迁移/启用收费。剩余下一动作：先增加系统自动验收的真实审计来源/事件合同与集中责任层，再接统一调度最终处理器；自动取消复用已有资金事务；Runtime真实退出/私有清理及关系释放仍待实现。不能将此次截止事件注册当作15天业务终结已跑通。

## 2026-11-10 自动事项结算接续（候选，未验证）
- Owner复用API worktree，base01d9560e1c/tree5440f045；本次不改生产/不启用开关。系统自动验收使用既有决定与capture事务，reviewed_by_jiacn=null、review_reason=hosting_rent_expired；事件actor=system/null及固定reasonCode，外部用户decide不接受该来源。Mapper/事件读校验一起按明确系统来源收口，历史用户验收不改。
- 新HostingRentTaskSettlement只承担事项阶段：按原租约绑定发现owner/Agent，在SQL分区后按id分页发现未完成事项；每事项按root→binding→lease重查已满15天FINISHING及关联，reviewing必须存在submitted正式交付才自动验收，其他未完成/failed复用取消退款。主动移除未达期限、已完成、旧绑定/旧调度不强制处理。不会释放live slot或宣称进程退出/私有清理已完成。
- 最早验证：系统来源/重放/禁止伪装/事件读合同、收尾责任层mock分支、真实MySQL钱包+事项+收尾发现/绑定锁+自动验收与取消事务。统一调度最终handler与Runtime交接须在该资金责任边界通过后接通，未把无消费者队列当已完成。

### 自动结算首轮失败归因（2026-11-10）
- auto-settlement-1固定b54c372611799e43e8e35373bbbaee9627aa4138/treea659d15582d4e63e0933281179704bea11a01269，29项中27通过、2失败；未到分层检查，不上线。实际耗时/result与driver存档保留原目录。
- 根因矩阵：本轮mock重设when提前执行已有锁断言，与生产调用无关，改doReturn保留运行时锁断言；新增取消用例遗漏prepareCancellation的正式DDL，复用既有完整夹具，不模拟存在性或删除资金断言。上一失败为技能MySQL socket路径，已在arrears-finishing-3通过；不是同根因重试。
- 修复限定两个测试，重新固定commit/tree后重验原29项及分层。无生产库、进程或开关写入。

### Runtime真实退出前置修复范围（2026-11-10）
- Owner沿用task-scheduling-owner；外部源码/home/isp/wsps/chcbz/isp-install基线c1fc18174b256c90051874485c8c77967efad62a/tree9dc7ef80bbdd135cf81386a424d68f4c7ca95a0d。已读取该仓AGENTS及CYF根规则、API接口v1.2和RB-1；CYF本地构建/固定app覆盖该仓历史版本目录口径。该仓其他Python/安装器等脏修改保持不动。
- 实际缺口：app-server-adapter.shutdown强杀后100ms无条件resolve；child.killed仅表示发出信号，不是退出。RB-1 bridge负责本机进程退出，修复限adapter的关闭事实、已有版本元数据及定向测试，不改API权限/协议、不操作实际Runtime。
- 采用已有executor的事实策略：等待owned child close，旧超时只用于SIGKILL升级，不作为成功依据；错误/未退出保留等待与上层所有权。测试覆盖延迟close、并发shutdown、已关闭、真实SIGTERM忽略后SIGKILL。此修复不等于私有数据清理或关系释放已完成。
- auto-settlement-2固定ab05c744809c26c8cc0ef09d036a7628987b2a99/treebecab08b312ce141e63cd81aca018eefb6b5745d：29测试全过，但validateLayering发现新服务直接依赖economy mapper，整轮FAIL保留。墙钟115.256s、回归54.160s、受限61.096s。不是已完成交付。
- 分层修复不增baseline例外：租约加锁、FINISHING状态与满15天判定移入既有HostingRentRenewalService，调用者必须在事项根事务中；Agent只消费结果并管理事项事务/绑定。真实MySQL仍使用正式economy实现，新增同用例近期lockedAt不终结断言；无新框架或跨层重复规则。

### Runtime关闭事实验证通过（2026-11-10，未上线）
- 外部Runtime候选50cf10ce274c3a24d7a00a45ac5f85627e56849f/tree809124cfe4f48707a1cf1c90f94fcd14594fe15b；bridge1.1.55、Runtime1.3.66。仅提交adapter/5项专属测试/版本及lock元数据，他方脏修改未纳入。
- 在普通磁盘git archive干净源码验证app-server-shutdown+现有chat-runtime，共59 PASS、0跳过/失败，墙钟20.865s。含真实owned child忽略SIGTERM后SIGKILL及close核验；unit含超过旧100ms仍不确认、并发关闭、已关闭、信号失败不假成功。无生产模型调用/服务启停/本地HOME清理。证据runtime-shutdown-1/{result.json,test.log,driver.py}绑定源码、Node及依赖树摘要。
- 仍仅完成实际进程关闭前置；最终finishing调度、Runtime交接wire及持久回执、私有清理、关系释放没有完成。规格清除“全部不自动验收/本次不提取知识”与最新欠费15天要求相冲突的旧描述，主动移除与欠费分别明确，未宣称实现。

### 自动事项结算切片验证通过（2026-11-10，未上线）
- API 4224bf0d4bf261630aa77d6e094b2d074e60c9bb/treee6a37add37533fe53a174131980db0396de27b7c：auto-settlement-3共29 PASS、0失败/错误/跳过，validateLayering PASS。9事项阶段、8系统验收单测、12真实MySQL资金/自动结算回归。系统验收来源、事务失败回滚、验收取消竞争、旧owner隔离、未满期限/主动移除不强制均已覆盖；不代表Runtime全链交接通过。
- 墙钟151.854秒，真实回归51.007秒，受限100.841秒；原失败保留，driver/timing/逐XML摘要同批存档。已停止本批owned MySQL，无生产库写入/打包/合入/发布/开关变更。
- 当前API干净候选4224bf0d4b、Runtime已提交50cf10c（外部仓库其他脏改保留）、Web既有5d1124c不变。根文档/ledger仍有他方改动，不整仓stage。下一动作：完整finishing处理器与Runtime交接合同、持久退出清理回执及关系解除；不能只注册任务阶段就把整个schedule标成功。公共资源保留/私有数据清理及旧凭证和迟到费用归属仍须完整验收。

## 2026-11-10 接续：Runtime持久停止栅栏（实施中）
- Owner task-scheduling-owner，Runtime基线50cf10ce274c3a24d7a00a45ac5f85627e56849f/tree809124cfe4f48707a1cf1c90f94fcd14594fe15b；复用原外部源码，不覆盖他方Python/安装器等脏改。API4224bf0d4b和Web5d1124c本轮暂不改。已重读CYF规则、工具入口与Runtime相关源码。
- RB-1职责：RuntimeHost只负责按完整subject/installation停住原执行并保留本地所有权，不判断余额/租期。原生命周期gate和private-json原子持久化复用；每Agent只保留一个当前交接操作标识与REQUESTED/QUIESCED事实。新启动/ensure/reprovision/activate不能越过该事实；不新增轮询或全局调度。
- 必要校验依据：旧installation/不同operation不能停止或接管当前交接；损坏/不匹配的本地事实不能被重建覆盖；未确认close不得报告QUIESCED或释放writer锁。只返回进程停止事实，不冒充私有清理完成。持久栅栏仍需接入已授权hosting wire和最终调度，不单独启用生产。
- 最早验证：真实普通磁盘状态重启保留，关闭失败保留REQUESTED与锁，同操作幂等/异操作冲突，排队activate/reprovision拒绝；既有RuntimeHost/hosting-control回归保证正常初始化和其他Agent不受影响。完整私有清理/最终关系释放仍待后续。
- runtime-handover-1固定fb9116eb5410144f44ea4d177f57af36da9ddb5d/treec9976cfd15d1e2b418c8aa54d11e50d757da958d，共146项137通过/9夹具失败，新增7项持久停止测试全过。35.635s全额保守计受限；失败原样保留，不宣称完整验证通过。
- 归因：复用上轮两个目录archive，遗漏既有systemd/shell静态测试输入和6个历史固定git archive夹具；2个真实UDS用例受批次长TMPDIR超过socket限制。修复driver不改产品代码：复用同一任务已创建的干净source补齐完整固定archive，独立git元数据仅借原仓对象只读alternates，短普通磁盘TMPDIR；同源剩余564.365s，不删146项选择或修改历史固定源码。
- runtime-handover-2在同fb9116e源码完整146 PASS/0跳过失败，50.666s，本候选累计受限86.301s（真实UDS/进程测试本次亦保守全计入）。已归因修复driver，首轮失败保持；非应用代码问题，不扩时/删测试。
- 实际动态托管接续发现：resumeAdmitted在重启读到有效handover时会把“故意停止”误记为recoveryRequired。继续在现有host/hosting-control边界修复：统一返回HANDOVER_PENDING，controller不改写原enrollment事实；新增动态托管重启集成覆盖无新executor/enrollment/session、其他Agent继续ready。无新增wire兼容或业务租费判断。
- cd82264动态托管修复在runtime-handover-3完整147项PASS（待result收录），真实停止仍不能仅凭上层回执推断：向下追查发现TypedInspectionProfileRuntime.dispose吞掉shutdown/egress失败且提前清空activeAdapters。此为最终清理的真实依赖，本轮继续修复，不按无关优化扩大范围。
- 修复限制profile.dispose：并行等待全部关闭结果，失败对象/会话所有权/CA保留并向上报SHUTDOWN_UNCONFIRMED；仅成功对象移除，不提前删私有资源。保持pending startup的既有拒绝语义，不把已取消启动误作运行故障。新增失败重试、其他对象仍关闭、warm代理失败、在途close失败用例；既有profile及host/control一并回归。
- runtime-handover-3精确cd822644bc5f8c77442ee709b6837fcf057d2b5b/tree151367ac8056dc2a447c7b7094feaff8dbdea309，147 PASS/0跳过失败，56.252s。没有已启用生产终结入口。
- runtime-handover-4精确e8ea66f7810bef99fced1538ffa5f9d28c2eaaae/tree9685ed0d1c7a7663721d82de1a60ef2356986bc8，178项：176通过/1失败/1既有native probe条件跳过，52.876s。失败为新增全profile回归读取固定历史carrier evidence时，root tar默认保留git archive的0664，实际源码0644；不得放松生产loader的不可group-writable规则。
- 根因矩阵：前次全archive/Git对象/UDS夹具已由同源146通过验证解决；本次是新增profile用例发现的文件模式差异，不是同根因盲重试。driver外层archive显式git -c tar.umask=0022，保留原证据内容摘要与历史consumer archive行为；同源剩余547.124s。native probe仍明确未运行，不把跳过记通过或宣称真实Provider验收。

## Runtime持久停止保护验证完成（2026-11-10，源码未上线）
- Runtime候选e8ea66f7810bef99fced1538ffa5f9d28c2eaaae/tree9685ed0d1c7a7663721d82de1a60ef2356986bc8，版本Runtime1.3.67/bridge1.1.56。runtime-handover-5：178项，177 PASS、0失败、1既有真实native bwrap handshake条件跳过（未开启CYF_TYPED_INSPECTION_NATIVE_PROBE），不能宣称真实Provider/生产交接验收。新增停止/错误保留用例全部通过；普通运行、真实UDS、同实例托管恢复及其他Agent回归通过。
- 本轮52.272s，同源含原失败累计105.148s受限；日志/driver/result/test-summary记录来源与摘要。source是复用任务archive+独立Git索引，测试后干净；原源码其他Python/安装器脏改保持不变。未打生产制品、未合入develop/部署/迁移/启用收费。
- 已实现：内部RuntimeHost.quiesceAgent在原subject gate和writer所有权下先持久REQUESTED，实际executor.close完成才QUIESCED；重启/ensure/reprovision/activate不能恢复旧执行。托管resume保留原部署事实，不把有意停止标成恢复故障。TypedInspectionProfileRuntime.dispose不再吞关闭/egress失败，未确认对象、会话所有权和CA保留，不允许上层提前宣布停止。
- 该方法目前是内部生命周期接口，**尚未接入最终hosting wire、任务收尾handler或公开停止命令**；QUIESCED不等于私有清理完成。仍待：公共资源确定清单下的私有清理及持久回执、关系/身份投影解除、同实例重新邀请、原费用迟到归属和旧破坏性repair退役；全链及最终上线未完成。
- 下一动作定向提示：已只读查看静态HOME目录名，除sessions外还有thread_history/state/goals/memories/queue/logs SQLite及WAL/SHM、shell_snapshots、tmp/.tmp、thread-writer-locks和.cyf-skill-view-staging。不能只删sessions就宣称清理；不能凭auth.json文件名猜公共/私有，应从配置的凭证归属和受信公共模板确定保留清单。公共skills/config/凭证与独立费用/ACK归属证据不得无差别删除；后端私有历史不迁给新用户。
- 磁盘仅移除已退出0且无pid/cmdline/fd引用的本任务auto-settlement-3/mysql-owned/data；保留全部测试/fixture日志及receipt，未清理生产HOME或他方状态。当前没有在途测试。

## 2026-11-10 接续：关闭失败的可恢复性（未上线）
- 定向追踪发现真实依赖缺口：disposeAppServerState原先先清空adapter引用并设disposed，shutdown失败后的重入直接返回；disposeProfileState同时缓存失败promise。不能据此进行私有清理。另idle warm关闭在finally提前删除inputs，失败promise也阻止后续重试。
- Runtime候选8049beaca3abe7d85c267b5455ed93ff2de4f4e5/tree42e94ff35eee6740899e384f0e439004bf9efaa4，Runtime1.3.68/bridge1.1.57。在既有dispose责任层保留未确认退出的adapter集合、并发调用共享关闭promise、成功对象不重复关闭；失败清空promise供显式重试，但disposed保持true、不恢复执行准入。idle warm仅实际关闭及egress退出后删除inputs，失败保留资源及所有权。没有新增调度/自动无限重试/租费规则。
- runtime-handover-6固定干净archive：181项，180 PASS、0失败、1既有native bwrap握手条件跳过；56.908秒保守全计受限。新增3项覆盖关闭失败重试、并发join、成功幂等、失败保留私有输入；沿用host/control/profile/child定向回归。实际Provider握手仍未运行。agent-client整体影响回归继续在同源码runtime-handover-7，不重置600秒预算。
- 外部Runtime他方安装器/Python等脏修改保留；不触碰生产HOME/状态，不打包安装、不合入develop，不启用收费。剩余仍为私有清理与共享资源保留、可信hosting交接及持久回执、最终handler与关系释放/重新邀请、全链验证发布。
- runtime-handover-7同8049bea源码agent-client整体223 PASS、0失败/跳过，42.039秒；与-6合计403 PASS、1明确跳过，累计受限98.947秒。两批test-summary.json记录日志摘要、固定源码与真实计时，archive测试后git status干净；无在途测试。完整交接/清理和上线仍未完成。

## 2026-11-10 交接通信与费用证据集成（仍未完成/未上线）
- 上一目标轮属于实质进展：关闭失败重试修复已落地并验证；本轮继续新增API→Runtime正式停止合同而非停留内部方法。沿用同Owner、原worktree，根工作区和外部Runtime他方脏修改未纳入。
- Runtime2de63186909c292218758eb1f21115d9760f4821/treedd8ea8d35495cb633564b04dc05629221e68340e：`hosting.quiesce`使用现有UDS/公共信封，原关系和当前已受理代次+独立handoverId。旧owner/binding/lease/install/manifest/generation拒绝，旧代次不能停止新reprovision；挂起注册仅取消并join本subject，重启回读持久QUIESCED，不创建执行。新reprovision不能越过持久停止。真正execution-adapter.close失败也不永久缓存拒绝promise，显式重试仍保留原attachment和准入停止。
- API当前a197a10a2a499c744db87541a11f71186c43f3f9/tree8b3dda93d492aa7cbcc3c9dcf63f31a2382329cc：ManagedHostingProvisioner/Unix适配增加quiesce。事务外、精确scope+原candidate，不prepare/enroll，不新增HTTP入口；原回执精确echo+host+QUIESCED才为true。丢响应/未知/错关系false，不授权清理/退款/重邀。两端共享报文与规范依据见beta-wen-billing.md末节。
- runtime-handover-8：186项185 PASS/1原native probe条件跳过，56.932s。新增真实adapter失败重试、共享codec、旧代次、重启与挂起注册；未使用真实Provider。
- API hosting-quiesce-1：固定ba0493185a/tree933ac9362522ba2a3b158dc9419384b04f6a1bdd，38项35通过/2失败/1旧初始托管真实UDS条件跳过；92.928s。新增Java→Runtime实际socket停止测试通过，但两项旧UDS测试因JUnit继承长java.io.tmpdir超Unix路径限制失败，validateLayering未执行。保留原失败。后续复用已有hosting-java-bridge-fixture与真实initial/reprovision测试，将quiesce追加到原生命周期；删除本轮新建的重复runner，未保留两套夹具。
- 修复driver使用短普通磁盘`/home/isp/state/cyf-test-tmp/hqN`，JAVA_TOOL_OPTIONS/TMPDIR等仅影响本批测试。启用既有`CYF_GSS_RUNTIME_TEST_SOURCE`/`CYF_GSS_NODE_BIN`，不放松生产socket ACL。hosting-quiesce-2在Gradle前被编排gate拒绝（7.952s，未跑测试），原因是误用了只适用于blocked_root_cause的authorize-remediation；恢复正确Owner targeted_verification后才继续，未绕锁/伪造证据。
- hosting-quiesce-3：上述APIa197a10 + Runtime32e33df（2de6318仅额外测试历史、已删重复runner），37 PASS、0失败/跳过，validateLayering PASS；61.736s，累计保守受限162.613s。实际Java生产适配器→Runtime生产UDS/control/host覆盖initial/replay/reprovision及当前/旧代次quiesce；native API/enrollment/executor是合成夹具，不是线上或真实模型验收。

### 停止与费用记账候选合流
- 私有清理依赖审计确认：原Runtime候选分支尚未包含独立CHAT/原生/图片usage回执，而已有费用分支固定`5dc596c9721000bcbca3c9dcb38d7b8e1c8d3a1e`含这些实现。不能按旧树做清理后再覆盖费用实现。只读merge-tree确认仅3个版本文件冲突，随后在本任务现有Runtime分支合并固定提交；未修改费用分支工作区/他方脏文件。
- 当前Runtime `d471d49e5f13cb9b027721b43e131ae661677979`/tree`885db70a4ecc370dbaf83b22f07e4793f7524c6d`，Runtime1.3.70/bridge1.1.58。冲突各版本文件去除版本后两侧对象完全相等，再统一升版；无依赖变动，非整文件回退。普通CHAT、native execution、provider图片独立回执与真实关闭/停止合同均在同树。
- runtime-handover-9：19个定向suite共725项，723 PASS、0失败、2明确条件跳过，137.865s；两跳过为现有真实openpyxl材料工具链与bwrap原生握手，不能宣称其通过。覆盖费用先于成果失败持久化、ACK丢失/重启仅重投费用、旧任务/停止和技能管理/公共包；并发度2匹配主机2CPU，未运行Gradle并发重构建。固定完整archive、Node/依赖树与日志SHA保存在result/test-summary。
- hosting-quiesce-4重新实际执行（不是EVIDENCE_HIT）同APIa197a10对合并Runtime d471d49：37 PASS、0失败/跳过，validateLayering PASS；50.258s。本次保守携带此前API162.613+合并Runtime137.865=300.478s，合计约350.736s；未豁免集成耗时，也未给应用下传deadline。原失败/拒绝均保留。下一批driver复用键显式加入runtimeGitTree；本批result已有完整Runtime固定SHA/tree且确实实跑，原driver不改写。

### 下一实施点（勿重复已完成停止修复）
1. 私有清理仍未实现：不能只删sessions，也不能删HOME全体。保留公共技能/配置/凭证需来自可信模板/安装事实，不能按auth.json文件名猜归属。managed.template已持久保留providerEnvironment和精确codexConfig；静态HOME公共凭证来源仍须核对。state/inbox还混有公开skill-install packages/journal与用户私有会话，需要在资源责任层收口。
2. 已核实skill-install-manager绑定identity包含owner且拒绝改绑；listInstalledSkills依赖journal.installations中的原command与immutable package、技能当前视图摘要。下一关系不能简单把skills目录复制走或删除journal。需显式退休旧关系的命令/私有身份，保留可验证公共安装事实，清理后才允许新身份绑定；同实例/公共包不新建另一套运行时。
3. merged源码费用位于CHAT usage-pending/acknowledged及native SkillExecutionStore中的native/provider usage源与独立receipt。删除执行目录之前必须保存/交付原费用事实，不能把business receipt当费用ACK。API withNativeFence(...false)不要求online/registered，但仍要求原有效binding/install/session；因此可在原关系未解除、引擎已停止时用成本专用会话送达持久回执，不恢复执行/启动模型。具体flush集成和失败恢复尚未实现，不能宣称完整费用结清。不得用新owner身份发送旧owner证据，也不得静默丢unknown start/terminal。
4. 最终收尾handler、私有清理持久回执、knowledge安全提取、关系/身份解除及同实例重新邀请（含自部署通道）仍未完成；统一调度其余迁移/多容器与Web完整状态验收和部署仍按原剩余范围，不缩成quiesce即完成。feature switches仍未启用。
- 当前无在途应用测试/服务。没有生产HOME/数据删除、生产模型调用、安装/启停、迁移或新用户收费；未合入develop/发布。

## 2026-11-10 接续：停止后的原归属费用回执（实施中，未上线）
- Runtime候选cef79bd将原SkillConversationLane已有source扫描/HTTP/费用ACK及重投提取为SkillUsageDelivery，live lane复用同实现；独立实例无需伪造registry/runner，不能poll/process/取lease。CHAT同样新增flush，两轮仅按STARTED→TERMINAL送达原事实。PENDING_USAGE/PENDING_PRICE确认的是后端接收，不宣称零费用；原业务receipt不代替费用ACK。未知旧command或证据冲突不许可后续删除。
- runtime-handover-10固定cef79bd/tree4bb9e4fb2ac2bf151c6d896280ce005cc2b961a9，PASS，58.669s；之后将新模块补入原immutable payload显式清单（0e0981c/tree758d3051cbed6bf00059102b264fce1f79699c67），runtime-handover-11全量实际重跑相关9套PASS，77.593s。原日志及固定输入保留；未复用证据宣称其他源码通过。
- 5a3b182/tree82636ac068c765f25074fbc6f52fe15d4a2a220d新增RuntimeHost.flushAgentUsage：沿原subject gate/writer所有权，持久QUIESCED且无executor才可送达；请求绑定原installation/operation/owner，先记录owner再外部IO，成功标记usageAccepted。失败可原归属重试，换owner拒绝；重启/同操作成功幂等。此标记仍不是私有清理或关系解除许可。
- 实际usage-handover使用RuntimeV1Client原authorization申请短暂native session，不enroll/register、不启socket/engine，finally撤掉本机session。CHAT不调用live initialize（会恢复业务队列/GC）；缺费用目录是没有source，不创建业务状态。native使用原owner的scope/hash目录，只发送usage/provider-usage，不恢复执行。不改变收费/定价责任，不调用Provider。
- runtime-handover-12同5a3b182实际失败，70.819s：本批560项557通过/2失败/1原跨端M3明确NOT_RUN，不能算作全部通过。第一处为全artifact验证负例：根因是execution-adapter静态import新usage模块提前拉入skill-manifest的AJV，在未准备依赖的诊断阶段提前报MODULE_NOT_FOUND，破坏既有validator错误分类。不是fixture/磁盘/权限原因，不删除负例。修复为flushUsage被调用时再动态import，保留原预检顺序且不增加常驻依赖。4f30aa5候选Runtime1.3.73/bridge1.1.60，待runtime-handover-13原11套重跑。保守携带前三批累计207.081s，不给应用下传deadline。
- 尚未接入hosting wire/API终结handler；当前公开quiesce仍只代表停止。未做私有数据删除、公共技能退休/重绑、知识提取、关系释放或线上收费。其余全范围不缩减。
- 补全runtime-handover-12的第二失败归因：新host restart夹具错用不存在的`host.close()`而非既有`host.stop()`，发生于同owner送达/并发幂等/持久标记断言已通过之后，restart部分未执行，不能宣称restart已验收。runtime-handover-13已启动后才在完整summary核实该失败，保留实跑，不中止/重标；d5622a9仅修夹具三处stop调用，不削弱生产检查。原故障候选不再原样重试，下一候选需重新完整验证。该遗漏为本轮检查疏漏，不归因性能或环境。
- runtime-handover-13：4f30aa5/tree9966a05b0e7a9c62633594c5d715128326d5f3cd，560项558 PASS/1FAIL/1原M3跨端NOT_RUN，74.563s；原artifact负例已恢复通过，唯一失败为上述未修夹具close调用。未将失败报成功。
- runtime-handover-14最终固定d5622a935aa23a28cf675163f9a297ad1f1b1526/tree40bd4ed41def6805e1a9e6cbbafa3f898e028b06：560项559 PASS/0FAIL/1原M3跨端明确NOT_RUN，77.461s，11套实际运行；最终本地源码archive干净，Node24.22.1/依赖摘要/日志及selector全记录。含失败保守累计受限359.105s，未超600s；无在途测试。
- 本次已验证新增source-only CHAT/native/provider补报不执行新工作、同source重启重投/丢ACK/未知价不补零、不同owner目录不混用、原subject停止/owner锁定/并发join/成功持久幂等与重启读回。真正RuntimeClient网络身份约束复用原客户端；新增cost-only调用测试使用合成HTTP/client回执，不能宣称API+DB/真实Provider/生产交接通过。
- 下一动作：把usage前置条件接入完整收尾合同，但不能先暴露“完成”入口。公共skill journal目前identity含owner，installations.command包含原管理命令，技能查找仍依赖其target/skillKey/权限/版本；需在既有SkillInstallManager责任层明确退休旧关系、保留可核验公共安装事实，不能直接删journal或清identity让旧命令在新用户下重投。静态公共凭证来源、全私有根清理、知识安全提取、最终API handler及自部署仍未完成。不得因本轮费用证据模块完成缩减原目标。

## 2026-11-10 公共技能事实与旧关系退休（源码候选，未清理生产）
- 前一目标轮有实质进展：费用source-only发送/停止gate及持久回执已实现并验证。本轮续做公共技能与旧关系管理命令分离，不将费用模块当完整上线。
- Runtime0e2716788aa538d39cca99036c23d9e727d595c7/treea3ad6c92cf954a42d2523d8adc6a13aad776fe4f，Runtime1.3.74/bridge1.1.61：SkillInstallManager journal改为format3，installation只保留target/skillKey/权限摘要/版本与原不可变包marker/manifest/hash，不再依赖包含owner/downloadPath的私有command。已有format2只在initialize既有writer锁下验证原完整摘要/命令/receipt后原子升级，不保留运行时双轨读写、不下载/重装/改包marker；普通读仅接受format3，旧完整管理命令在显式退休之前仍按原语义保留。
- `retireRelationship`沿原manager tail+跨进程锁，必须无live session且精确原identity/operation；未获后端receipt的已开始管理结果阻止退休，RECEIVED仍可证明未执行。退休前验证当前技能视图和全部保留公共包；原子清除identity/commands/messages/fences，只留退休operation及identity摘要。保留公开技能包/视图/安装事实，不主动删文件、执行或重投旧命令。退休后bindSession明确阻止原/新用户自动接管；后续成功私有清理及授权新关系的显式准入尚待接入，不能据此重新邀请。
- runtime-handover-15固定上述0e27167，551项550 PASS/1 FAIL/0跳过，125.741s。新增公共包保留/退休幂等重启/未收据与包篡改/原format2升级均通过；失败是既有journal负例仍replace字符串`formatVersion:2`，换成format3后没有修改实际fixture，误把完好字节用于assert.throws。生产代码无错误通过/放松，修复仅将该负例替换当前3版本字段（5cccab1）。保留失败，不宣称完整候选全绿。
- 下一批runtime-handover-16只重跑本次确实改动的journal负例suite，并补此前未跑的真实SkillRegistry消费者；其他550 PASS绑定原0e27167，不能冒称新tree整体实跑。精确新版全量验证留在后续最终候选，不为测试夹具一行重复执行无关场景。保守携带之前累计484.846s，不借改selector声明未执行用例通过。
- 只读核对静态wuyong/linchong/lujunyi的auth.json均为auth_mode+OPENAI_API_KEY，API key在内存比较均与operator providers.json的shared scopes存在相等值；未打印/记录密钥或其摘要，未修改文件。此仅定位可信公共凭证来源，尚未核验具体subject→scope选择及恢复模板，也不代表可直接保留整个auth.json。managed仍有持久精确codexConfig/providerEnvironment；静态公共配置基线及清理实现未完成。
- runtime-handover-16最终测试修正候选5cccab177bbf93963df6f726eed8168070667cbf/treed13ff1a5da25222948c4a74efb353e2b1373fa0f，journal-validation+SkillRegistry两套全部通过（详见test-summary），1.284s；与之前保守累计486.130s。最终archive干净。没有新生产制品/安装/数据迁移；其余550通过仍只标原0e27167，不将整个新tree宣称全套实跑。无在途测试。
- 后续实现仍需完整收尾入口调用成本flush→管理结果结清/公共skill retirement→知识安全提取及全部私有根清理→成功持久回执→后端关系释放→同实例新邀请显式准入；当前retirement会刻意阻止所有新bind，不能单独启用。现阶段需要查清结果结清通道：费用有原native HTTP，技能管理receipt仍走现有WS，不能为了退休假造receipt或直接扔掉已开始安装结果。
- 接续定向源码事实（API仍a197a10，未改）：`SkillManagementService.result(Proof, envelope)`约755行本身已用`authentication.withFence(proof,false)`，原owner/install/host/change/command绑定、摘要、事务和结果幂等receipt均在服务层，不要求在线注册。因而下一步优先给该既有服务补原native认证HTTP结果投递适配，并在停止补报中复用SkillInstallManager原pendingResults/acknowledgeResultReceipt；不另建业务结算器、不要让已停止Agent重新注册执行。应同步明确native route白名单/Controller公共信封及定向API+Runtime合同验证。

## 2026-11-10 停机证据HTTP与托管控制链路（已定向验证，未上线）
- 承接原全范围，不缩减目标、不创建新实例/新调度器。当前发现并修复的真实缺口：原费用补报helper虽然不注册WS，但API native filter仍强制在线channel，停止后真实HTTP会被拒绝。只对原CHAT/conversation/provider费用POST及新增技能结果POST允许无channel，持久会话/主体/安装/owner/代次校验不变；命令发现、package、lease和业务成果提交不放宽。
- API e4afc2c54351e67b216c33614b00a327576c59bf/tree2d7c04ab3db926d71110e260722e32189b80f025：新增SkillManagementResultController，复用原SkillManagementService.result事务/摘要/幂等，不新建结算器。外层标准HTTP data承载原不可变work.result，响应承载原work.result.receipt，HTTP与原消息关联各自保留。独占native namespace/no-store/严格requestId/query；现有入口责任层实现，不在业务层复制认证。
- Runtime6aaef37a81563d481c080e754ff2f19b206900f4/treeecda90ed064cfa5abd975a8582d8439b5f8adc2f：SkillInstallManager.flushResults使用原pendingResults/acknowledgeResultReceipt，原owner未确认/错误receipt/丢ACK均不消费结果；停止helper使用真实defaultSkillInstallStateRoot查找journal，在原writer锁内marker-only恢复并补报。不下载、不执行、不开启引擎。候选usage-handover→evidence-handover、flushAgentUsage→flushAgentEvidence、usageAccepted→evidenceAccepted为未上线单轨替换，无历史兼容支路。
- 测试准备故障handover-evidence-runtime-1：复用归档快照时git rename未列入D，旧usage-handover.mjs残留触发clean断言，0.4209s，Node未运行。保留driver/result；核对旧文件与5cccab1原字节相等后仅删除本任务snapshot中该文件；driver删除列表加--no-renames。不涉及生产/其他工作区。
- handover-evidence-runtime-2固定6aaef37：5套291/291 PASS，无skip，115.254s，依赖树摘要1849a093b5485fc458dd4ad960a01d35539adc7a38ac7affc9111c65ecf77554、Node24.22.1。handover-evidence-api-1固定e4afc2c：64/64 PASS，validateLayering通过，128.951s墙钟/109.676s受限/19.272s真实MySQL回归。含持久认证filter、真实MVC codec/controller、两项MySQL原结果幂等/迟到事实；并非生产Provider测试。
- 进一步接通hosting.evidence/evidence.result：复用quiesce全关系/current admitted generation/handoverId/受限UDS，先验主体/操作一致，再调用host.flushAgentEvidence；未停机拒绝，未送达返回EVIDENCE_PENDING，全部原证据确认后EVIDENCE_ACCEPTED。成功仍保留QUIESCED及subject锁，不清理HOME、不释放关系、不允许重邀请。API事务外调用，丢回复返回未确认，不重新prepare/enroll/session。
- 生产候选提交API5a162ba86c，最终含Java真实UDS测试611e4e4e70625a4a7f1014d00a08c1d8cf7cd6b2/treea5029aaad37f6c36a5f07e7422988041af63c5e1；Runtime5fd95608e474215e15f87b3fe59a58bde8c599c0/tree4094a50bcef40241cc8e13b90b421078ae157c06，Runtime1.3.76/bridge1.1.62，最终测试修正290012d48874f2f4249a1c20104815cef42244d3/tree5016c12500ff82b7bde3732c230b4b586f05dcbe。c67203c新增真实原journal定位/不同boot/丢ACK/错误owner/安装保留测试；7b73f2d为Java fixture配置合成证据接收器（真实stop、UDS、gate、journal，不冒称真实Provider接收）。
- handover-evidence-runtime-3固定5fd9560：181项180PASS/1FAIL/0skip，54.554s。唯一失败为新共享fixture测试遗漏hostingReply import，生产逻辑及新真实journal定位、受控evidence/重启均通过；保留失败。290012d仅补测试import，handover-evidence-runtime-4完整hosting-control28/28 PASS，2.618s；不将181项宣称在最终tree全量重跑。
- handover-evidence-api-2最终611e4e4e：UnixManagedHostingProvisioner16/16 PASS、0skip、validateLayering通过，96.554s。包含真实Java socket→Node HostingControl→RuntimeHost：未停机拒绝、旧代次/异handover拒绝、原代次停机、第一次pending、后续成功、重复持久回执；使用最终Runtime290012d干净快照。原生登录/执行器/外部接收为合成，不等于完整API+生产Runtime验收。
- 当前证据根/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/；各handover-evidence-{runtime,api}-*/result.json、driver.py、test.log/gradle.log、test-summary.json或XML保留真实源码和失败记录。包含全部失败的本轮保守受限累计379.077s（真实MySQL19.272s单列），未超600s。此前旧候选486.130s为历史，未合并冒称本轮已重跑。API工作区及Runtime受测snapshot干净，无在途测试。
- 两端相同fixture SHA256：hosting-evidence-v1.json=498f6c5596f3a15076e572da3e1c0e53e7dc3edcbbafe51988a861ef35d9dc04；skill-management-result-http-v1.json=4336102e99b142fa110ba1bea4bae85739dfcbcafe0903a35984f94d1d766b3f。规范beta-wen-billing.md补充该阶段合同，统一接口1.2/RB-1不变。
- 尚未发布/合入develop/push/安装/迁移/调用模型/激活月费；未写生产HOME及身份。root与Runtime其他任务脏文件未暂存。Web仍5d1124c，未重跑或冒称完成。
- 下一明确依赖：最终收尾handler不能仅把EVIDENCE_ACCEPTED当结清。SkillManagementService.applyEvidence(PREPARED)会创建新ACTIVATE；停机后不能再执行它。需在原管理责任层依原结果/停机事实结束未执行操作，UNKNOWN保留原owner的审计/待结事实，不能伪造NOT_STARTED/退款/receipt。Runtime initialize已对已开始无结果命令做marker-only恢复，RECEIVED证明未开始但当前不会生成结果；全成本/管理结果送达与最终财务处理须区分。
- 后续仍需：公共skill retirement接入、可信公共配置/凭据重建、全部私有根清理与安全知识提取、持久cleanup receipt、原关系授权注销/新邀请显式准入、自部署通道、首次现有技能计费、统一调度剩余迁移、Web月费/收尾状态与PC移动回归、最终发布。旧AgentPersonaProvisioningService.unbind/repair(SUSPENDING)仍调用publisher.publish→transactions.completeUnbind，完整切换时须收口，不能作为新清理成功捷径。FINISHING schedule目前仍无完整handler，不能宣称主线完成。

## 2026-11-10 停机未开始安装结清与管理残留清理（接续，未上线）
- 上一轮有实质进展：native证据HTTP及hosting.evidence已实现并验证。本轮不重复前轮全套；继续补真正阻挡清理的已接收未执行技能命令，以及管理目录私有残留。
- Runtime b2a0fcfbb3d8b767631996d8688b004085d4c6af/treeea9fc911f26a86f1bcfacc6e1d70dee892d01b5d（1.3.77/bridge1.1.63）：finalizeStoppedResults只在永久停止原owner下调用，沿manager原tail/writer锁把确实RECEIVED未开始命令记录成NOT_STARTED/ENTITLEMENT_TERMINATED；原执行instance/命令和消息关联保持，不下载/执行。READ抽出同一只读_finishRead供正常执行与停止收尾复用，未见原命令仍UNKNOWN，已存在结果（包括UNKNOWN）从不改写。helper在原journal恢复后先生成缺失的可证明结果，再按已有HTTP回执补报；失败仍阻止evidenceAccepted。
- Runtime handover-evidence-runtime-5：固定b2a0fcf，skill-install-manager+runtime-host两套232/232 PASS/0skip，121.340s。覆盖已有READ/正常安装/真实ZIP/事故marker恢复及新PREPARE/ACTIVATE未开始、缺失READ UNKNOWN、原结果不可改、错误owner/仍在线拒绝、重启幂等。完整执行，不将仅几项新用例称为全链。
- Runtime71ab0c600ee954bacce2e8d0ab7847afdc6b3fd8/tree81116148b38389406764d4d7a700efe0a3e21773（1.3.78/bridge1.1.64）：retireRelationship在退休事实提交后清理管理staging/stale-locks、未知临时journal写、未登记包及HOME/.cyf-skill-view-staging。保留核验过的immutable packages、公开journal和当前writer锁；包目录复用既有canonical/owner校验，删除子链接只删链接、不触及外部目标。提交后清理故障可同operation重试，不能重新bind；不新增cleanupComplete或成功邀请承诺。
- handover-evidence-runtime-6：固定71ab0c6，test-name-pattern明确只跑8项退休/停止相关测试，全部PASS/0skip，10.892s。验证包与发现视图字节保留、私有请求/临时journal/旧锁删除、外部symlink sentinel不变、退休commit后故障恢复；上一个232PASS仍绑定b2a0fcf，不冒称最终tree全量实跑。
- API71347f85dbad059b9b9ff395d357876aa5be7d1d/treebbcea5b0f468db966162e1d6b9045f15705b8a86，仅新增真实MySQL回归，不改原财务生产实现：RECEIVED PREPARE/ACTIVATE的NOT_STARTED终止安装、释放原50文一次；UNKNOWN准备/无法证明未切换的激活保留HELD和RECOVERY_REQUIRED，不因terminal reason退款。handover-evidence-api-3四项全部PASS/0skip，validateLayering通过；墙钟76.342s、受限48.733s、真实MySQL27.605s单列。
- 本轮连同前轮原失败的保守受限累计560.042s，未超600s；证据均在既有task根handover-evidence-{runtime-5,runtime-6,api-3}目录，source/driver/log/test-summary/XML均固定。无在途测试；无生产安装/迁移/清理/扣费/模型调用。API工作区及Runtime本任务路径已提交，其他任务的脏文件未动。
- 注意仍未覆盖API创建但从未送达Runtime的新ACTIVATE（例如停机补报PREPARED后创建），不能把不存在journal命令推断为NOT_STARTED并伪造退款。最终handler应在原管理责任层根据送达/停机事实收口；未知已开始结果在后台长期归原owner保留，不计给新用户。
- 下一步全私有根清理不能只删HOME：createProfileState还将chat-workdirs、threadBindingStore、各种inbox/ack/usage置于agent.stateRoot/inbox；workspaceFileRootDir、typedInspectionRootDir+profile、typedInspectionStateRoot+profile及controlledImageHttpLedgerRoot是显式额外根。createRuntimeExecutionHost以normalizeProfile(agent.profile,{},isolated:true)为实际profile，未继承全局隐式root。profile.workspacePolicyId还会建立GitWorkspaceManager：policy.root/taskId/agent-<encodedAgent>与.metadata/.locks/.archive-quarantine，不属于HOME/work/state，不能递归删除shared policy.root或repository，需复用manager的精确subject/task归属及已有archive/remove能力。源码入口conf/codex-bridge/agent-client.mjs约5900/6515、workspace-manager.mjs约287/346。这项范围审计是下一清理实现的必要输入，不作为无关重构。
- 全目标不变：管理退休尚未接入最终host cleanup；全HOME/工作目录/外部私有根、公共配置凭据可信恢复、安全知识提取、cleanup持久回执/新关系显式准入、自部署、首次技能清单计费、统一调度剩余迁移、UI/真实浏览器/最终发布均未完成，目标继续active。

## 2026-11-10 完整清理边界需用户澄清（只读发现，未删除）
- 上一目标轮为真实进展：b2a0fcf/71ab0c6及API71347f8代码/测试已完成；当前HEAD读回仍一致，无在途构建。
- 只读读取现行operator unified-profiles三个JSON，仅输出profileId/工作路径/policy字段，不输出凭据/会话正文：吴用codexWorkdir实际为/home/isp/wsps/cyf（本项目共享工作区）；林冲/卢俊义分别为/home/isp/hosts/cyf/agent-clients/jyt-jiafewnnv58ec2379c-{linchong,lujunyi}；三者workspacePolicyId=cyf，HOME和private-runs各自位于/home/isp/state/cyf-agent-runtime-v1/unified/agents/<profile>/。
- 因此不能把profile.codexWorkdir统称为可删除的Agent私有根，否则会删除本项目与无关脏修改。GitWorkspaceManager的真实工作区在policy.root/task/agent-<agentId>，Git对象由共享repository持有；现行archiveWorkspace只允许无可见修改且非base HEAD已发布到可信remote的任务归档，不能直接拿它处理取消/未提交事项，更不能全仓GC或删除shared root。
- 尚无证据/用户决定证明“共享代码仓库及其Git历史”属于公共可保留数据；保留它们可能保留事项提交，删除它们又影响共享项目。下一步先向用户确认这一条数据分类：共享项目仓库（含Git历史）是否按公共数据保留，解除时仅清原Agent会话、专属执行/临时目录及可证明归属的任务工作区。若不作为公共，则需明确其私有数据去向/权限边界后实现，不自行把全私有清理缩为仅sessions。
- 未执行生产删除/迁移/配置修改/模型调用；目标仍active。这是首轮具体数据分类澄清，不满足blocked阈值，不标blocked/complete。

## 2026-11-10 用户确认共享仓库保留，解除分类阻塞
- 用户明确“这些是公共数据，需要保留”：共享项目仓库及Git历史按公共数据保留。已写入beta-wen-billing.md现行收尾合同；不扩展为所有工作文件/附件/凭证均公开，不新增跨用户访问授权。
- 目标已由用户恢复active。原数据分类阻塞解除，继续原完整目标；无需重复询问该边界。
- 只读核对Runtime HEAD仍71ab0c600ee954bacce2e8d0ab7847afdc6b3fd8，API仍71347f85dbad059b9b9ff395d357876aa5be7d1d。本次仅落定合同，未执行生产清理/安装/收费，不宣称清理代码已完成。
- 下一动作：在既有Runtime收尾边界落实受控私有根清理与公共仓库排除，串联原证据确认、技能退休及持久清理回执；保留任务worktree的真实归属与共享对象边界，不直接删除codexWorkdir或policy.root。

## 2026-11-10 清理生命周期与持久回执入口（候选，非完整清理实现）
- 上轮归类为progress：用户明确数据分类并写入现行合同，真实阻塞解除。本轮沿原目标落实Runtime责任层，未缩小完整上线目标。
- Runtime提交a16fca8c84f20a58aa5bdfe2165a4a7fbbd725fb/tree3c991484ad10ce617305427506b459e8de8071e1，Runtime1.3.79（bridge未改）：RuntimeHost.cleanAgentPrivateData复用subject gate/ownership/original handover，要求同installation/operation/owner、QUIESCED且executor为空、evidenceAccepted。缺存储adapter明确拒绝，pending/异常不记录成功；确认后持久cleanupComplete，并发/重启读取同回执，不重复清理，不解除原writer锁、不允许ensure/reprovision/旧执行重启。
- handover-evidence-runtime-7固定上述commit/tree，4/4定向测试通过（private cleanup gate两项、cost handover、handover quiesces）；2.544s，携带先前560.042s后保守累计562.586s。源码为既有干净snapshot，依赖摘要不变；日志/driver/result在既有任务证据根。测试storage adapter为合成，不冒称真实私有文件清理已覆盖。
- 仅明确三个本任务文件提交；Runtime已有Python打包/安装等无关脏修改未暂存。未发布、未生产清理、未新扣费、未迁移。
- 下一实际实现：生产storage adapter和hosting.cleanup控制消费者尚未接线。须先退休SkillInstallManager原journal，再保留公共安装事实/包、重建可信配置凭据、清理所有私有根（不能删公共codexWorkdir/Git）；保留handover.json及.runtime-writer.lock以便失败恢复。managed subjectAgent由持久template生成profile/providerEnvironment，codexConfig在subject.template；静态配置来源仍需对应operator scope精确解析。stateRoot/inbox中有按hex(agentId)分区的skill-install/<scope>公共journal/packages，不能将整个inbox直接删除。
- API FINISHING handler、自部署、显式新关系准入、首次技能计费、调度迁移及Web/最终发布仍未完成，目标active；无在途测试。

## 2026-11-10 实际CODEX_HOME清理存储步骤（候选，未接生产入口）
- 上轮为progress：a16fca8实现并验证原owner清理gate/回执。本轮继续真实存储删除，不把合成callback测试当清理完成。
- Runtime408116c4fb963cf981e06d73dffb3abd25d125b5/treef0623b0b7bd5471d16c9d54daecb87181e28115f，候选版本仍1.3.79未发布：新增lib/private-home-cleanup.mjs的cleanStoppedCodexHome。调用合同限定停止/证据/技能退休/知识尝试后；从可信publicFiles恢复config.toml、可选auth.json，保留公共skills，删除其余所有HOME项（包含未知文件与SQLite sidecars），不使用易遗漏的私有文件名枚举。无公共配置/与公共仓库重叠/非受控HOME或skills链接在删除之前拒绝；删除子链接不跟随目标。公共文件原子写及目录fsync，部分失败可用同可信基线重试。返回homeCleaned而非完整confirmed，不开放重新邀请。
- handover-evidence-runtime-8：上述固定commit/tree，4/4实际临时磁盘文件测试通过；覆盖会话/数据库/sidecar/快照/旧凭证删除、公共技能及配置恢复、共享仓库代码和.git/history原字节保留、symlink外部目标不变、拒绝条件不先删数据、残余临时写恢复及幂等。0.687s，保守累计563.273s；证据在原任务根。仅合成凭据，不读取/泄露生产密钥，不调用模型。
- 当前helper尚未接到完整cleanPrivateData adapter，**不是完整cleanup**；知识安全提取、可信静态配置映射、state/inbox/native等其余私有根、hosting.cleanup及API最终收尾仍需实现。此为待接线存储步骤，不部署半成品、不宣称上线。原其他任务脏修改未动，无在途测试。

## 2026-11-10 原关系技能退休接入Runtime state清理（候选）
- 上轮为progress：HOME实际删除及4项测试。本轮实现stateRoot实际清理，不把公共包所在整个inbox误保留或误删除。
- Runtime b616c750830ab8f121ac7acde01d99965a5cae5e/treef8b80b94294ced5a57f0ed65260b96cfbb9dee2f：evidence-handover导出stoppedSkillManager唯一定位器，证据补报与清理使用同一真实scope/journal路径。private-state-cleanup先requireOwnedPrivateRoot及公共仓库重叠检查，再initialize/retireRelationship同原owner/install/operation；结果未收据或身份不符拒绝清理。递归仅沿保留技能管理根祖先，其他state/inbox/session/私有链接删除；保留handover.json及.runtime-writer.lock、已退休manager根（public packages/journal），逐目录fsync。
- handover-evidence-runtime-9固定上述source：4/4磁盘测试通过，4.310s；真实SkillInstallManager ZIP准备/激活/receipt/退休，公共包与HOME技能原字节保留、邻接chat-workdirs删除、未收据/异owner不删状态、共享仓库/链接边界及重复清理。测试控制文件为合成，未冒称托管端到端。
- handover-evidence-runtime-10同tree：3/3原证据补报定向回归通过，3.608s，覆盖真实journal定位/未确认重试/原owner及成本无引擎补报；定位器抽取未改变receipt行为。最近证据保守累计571.191s，无在途测试；目录仍原task根，Node24.22.1/依赖摘要不变。
- 未安装/清理生产/迁移/收费；仅上述3个任务文件提交，其他dirty路径未动。两个存储步骤返回homeCleaned/stateCleaned，不冒充全根confirmed；尚需聚合adapter按统一gate和可信配置预检接线，知识提取尝试须在删除前，state清理须在HOME删旧凭据前后按重试与公共skill定位正确编排；外部native/typed/image/work根、hosting.cleanup、API最终关系释放/同实例再邀请与剩余原范围未完成。

## 2026-11-10 私有材料根与聚合清理接通Host实存储验证（未部署）
- 上轮progress：原管理退休及state清理已实现验证。本轮将HOME/state步骤真正聚合，并补workspaceFileRootDir、image ledger、typed input/state按hex(agentId)子目录、非公共work roots。公共仓库内的工作目录保留；专用私有根与公共根重叠或根覆盖控制目录拒绝；HOME/state内嵌私有根交由其责任步骤，外部根去重/包含消除后逐项删内容、保留目录并fsync。不扫其他Agent typed目录、公共policy根或Git历史。
- 生产源码候选3de0984a5bfed44b09a1da52bf6510c48d0ba84a/treedded6bdafaf1953c2d33157456cdef28bee577f6：private-data-cleanup在任何删除前预检全部根与公共配置，要求提供知识adapter；先按operation提取（失败不挡清理、不泄漏原始错误），再retire/state→materials→HOME，全部成功才返回confirmed+EXTRACTED/FAILED；RuntimeHost将安全knowledgeStatus随cleanupComplete持久保存。
- handover-evidence-runtime-11：上述tree实际磁盘三套12/12通过，5.759s；包括原HOME/state全部测试、新外部材料根/其他Agent保留/共享仓库保留/缺基线或坏根不先删前序数据/知识失败仍清理和安全receipt。知识adapter为合成，不是实际模型知识抽取验收。
- 最终测试提交64a62264c190c66ad757da8264b87257c0eaf8e9/tree92ec4c2027ae5e8b05013d96e1040dfddd14e9a8；handover-evidence-runtime-12三项Host cleanup gate测试全部通过，1.278s。新增真实RuntimeHost gate→cleanStoppedPrivateData→临时磁盘删除→原handover持久FAILED/cleanupComplete→Host重启同回执，原执行不重启，writer锁保持；非只测合成cleanup callback。
- 本组受限保守累计578.228s（原失败仍计入），无在途测试；前12项仍绑定3de0984，最终3项绑定64a6226，不冒称最终全部重跑。Runtime版本1.3.79/bridge1.1.64未发布。无生产数据变动、安装、迁移或扣费。
- 聚合器已经实现，但运行时工厂/托管控制尚未配置公共基线与真实安全知识adapter，因此未接通生产调用；不能以已实现默认假知识提取替代。下一步需要从managed subject.template和静态operator config提供可信公共文件/仓库集合，接hosting.cleanup及API调用；静态运行配置来源仍需核定而非复制旧HOME。知识provider调用不能擅自计给原用户，失败记录不能伪称提取。自部署、API FINISHING完整handler/未知技能事实结算、再邀请准入、首次技能费、其余统一调度、Web及上线验收仍在原完整范围。

## 2026-11-10 托管清理控制与可信模板配置接线（Runtime候选，API待接）
- 上轮progress：完整存储聚合及Host真实文件验证。本轮Runtime9123d057173d3d6297ce9a91fd84c2ae1661c50c/tree2018fc3624864c7fe98fee24c7e4424cc9254b41，版本1.3.80/bridge1.1.64：hosting wire增加cleanup；control沿当前admitted完整关系/generation/handover调用Host.cleanAgentPrivateData，CLEANED/CLEANUP_PENDING不释放/重邀。subjectAgent从持久template生成冻结publicFiles(config.toml)，公共Provider环境不变，旧用户config/auth不保留。
- execution-adapter提供真实cleanPrivateData聚合器，选原workspacePolicy的repository/root为公共保留集合，声明policy却无法解析时拒绝清理；runUnifiedRuntime将adapter接Host，extractKnowledge是显式注入依赖，生产CLI当前未提供该实现，故尚不能完整清理，缺能力明确报错而非伪造已提取/成功。静态Agent的公共配置来源还未接线。
- handover-evidence-runtime-13固定该tree：hosting-control全30/30通过，3.341s；新测试覆盖closed wire拒绝路径/publicFiles、真实control→Host→存储删除、原证据未确认不清理、异owner/binding/handover/generation拒绝、旧私有config/auth替换为保存模板、重启返回同一持久清理事实且不重新登录/不开放reprovision。执行器/原native接收/知识提取为合成，文件清理及持久gate为真实。
- 累计受限保守581.569s，原失败不改标，无在途作业。API工作区只读核对仍71347f8且干净；ManagedHostingProvisioner/UnixManagedHostingProvisioner目前仅quiesce/flushEvidence，handoverRequest仅允许quiesce/evidence，下一步增加cleanup消费/共享fixture及真实Java/Node UDS用例，不可声称API已接通。现未生产安装/清理/迁移/扣费。
- 剩余完整范围不变：真实安全知识提取与公共知识保存、静态公共基线/自部署、API FINISHING及未送达技能phase处理、关系释放与同实例新邀请、首次技能费、调度剩余迁移、Web完整回归和受控上线。仅Runtime30项通过不满足完整验收。

## 2026-11-10 API消费清理回执与真实Java/Node闭环（候选，未发布）
- 上轮progress：Runtime控制+可信托管模板。当前新增API.cleanup消费生产合同，并扩展真实Java socket→Node HostingControl→RuntimeHost→实际临时磁盘清理链路，不把Runtime已有30项当跨端验收。
- API初候选f712d4879f06fad6fd8144ed7b15c5cc8f2d9995/tree6d26fa2b0a1d6d438f04ca8ca3436ac3f435ed74：ManagedHostingProvisioner新增cleanup，Unix适配器复用handover事务外调用/精确绑定解码，仅CLEANED成功；不enroll/不收费/不释放关系。Runtime ef73bac6cbf60dff4161661edf765415d3017276/treec03ee8d1e9b91e5b8ee9e8ca9c7350d5838ac27c：新增共享hosting-cleanup-v1.json，两端SHA256=3662d30696727ec9d95da4227e9de481e86404eef696e1d16f07aa4a3e6cf88a；Java bridge fixture使用真实存储aggregate，外部knowledge/native/executor仍为合成。
- 新跨端cleanup候选构建批次cleanup-control-api-1，固定上述两端源码，600s用于该候选/重试累计；之前581.569s属于已记录证据补报/Runtime本地候选族，不覆盖本次新增API消费源码，也不重标其测试。首次17项15PASS/2FAIL，89.505s：公共request编码器遗漏cleanup方法白名单，fixture构造抛异常、真实调用在发包前被捕获为false。同一根因已用orchestrator fail记录，未盲重试。
- 修正API bb5d0efbf88e7e4302fca080eb7b29fb1b594a17/treee9d7ce5434588b156cabdcfccc3dce3ebedcfa1b，仅补原共享编码器方法白名单。cleanup-control-api-2重跑完整UnixManagedHostingProvisioner17/17 PASS、validateLayering通过，77.967s，继承首次受限耗时不重置。含真实UDS拒绝未停机/旧代次/异handover、原证据确认后实际清理、重复持久回执，以及契约丢回复/pending/错误回执和事务内I/O拒绝。
- cleanup-control-runtime-1固定ef73bac，对hosting-control的cleanup名称定向回归通过（具体总数见test.log），1.303s。跨端本批保守受限总计168.772s（原失败包含），无在途测试；Node/Gradle/JDK/fixture与原driver/log/result绑定，未打生产包。
- API、Runtime本任务路径已提交，API工作区干净；根文档及Runtime其他dirty内容未广泛提交。无deploy/develop merge/push、生产HOME删除、数据库迁移或新扣费。此回执能力不等于FINISHING调度handler完成；下一需接真实知识安全提取/静态公共配置，处理原技能API未送达phase及最终事务释放/新关系准入；自部署、首次技能费、统一调度余项、Web与完整上线仍在原范围。

## 2026-11-10 静态Agent公共配置基线（候选，未配置生产）
- 上轮progress：API.cleanup合同及真实Java/Node验证。本轮补静态Agent的可信publicFiles来源，避免只能托管清理或从旧HOME继承私有凭据。
- Runtime3875343b17d186f25a59a98f550fd0f1e28b0e06/tree55f2d8a269228b5a0f8e47f14f0b632e8ef937b1，版本1.3.81/bridge1.1.64：manifest Agent条目可声明publicFilesPath；security读取运维0600 canonical JSON、核对完整tenant/client/Agent及config.toml/可选auth.json白名单；收集所有主体根后拒绝基线位于任一Agent可变根或host state。启动读取冻结，公共文件不出控制wire；未声明仅在清理时报缺公共基线，不增加普通执行热路径查询。
- cleanup-public-baseline-runtime-1固定上述tree，5/5通过，1.176s；含正确原主体/不可变快照、错租户/client/Agent、未知文件/空配置、自己及其他Agent私有根/host-root拒绝、文件权限/符号链接拒绝、旧HOME未被读取复制、既有配置/真实Host清理回归。携带跨端前168.772s后保守累计169.948s，无在途测试。
- 后续单独README提交仅解释该现行配置与未接线边界；不将文档提交冒称新tree测试。只读运维目录发现现有三个静态profile均为gpt-6-luna、workspacePolicyId=cyf，skill-bindings.json只列图像provider的adapter/credentialEnv/endpoint/model/revision；不存在由此证明静态聊天公共配置已冻结的事实。未输出密钥/其摘要、未改production配置或HOME。
- 当前实际公共基线文件尚未生成/写入production。真实知识adapter/公共知识存储、CLI入口、自部署控制及API最终FINISHING/关系释放/新关系准入仍待接通；完整原需求不缩小，未部署/迁移/扣费。根及Runtime其他任务脏文件未触碰。

## 2026-11-10 知识提取持久去重与清理故障恢复（候选，未调用实际模型）
- 上轮progress：静态公共基线实现及测试。继续核对真实知识adapter前发现聚合器原先在每次清理重试都调用extractKnowledge；若Provider已执行而后续磁盘删除/最终回执失败，会重复消耗。该实际成本/恢复缺口由现有RuntimeHost handover记录收口，不新建调度或审计框架。
- Runtime26a951c8852934ce87df5d3e9867fea40e949ac1/treee5a1422a0f52c7a665f80b4726e95c0e9cb7a1fd，版本1.3.82/bridge1.1.64：Host向存储adapter提供原记录knowledgeStatus和持久状态回调；只允许REQUESTED/EXTRACTED/FAILED，读取时要求原evidenceAccepted。aggregate先持久REQUESTED再调用；Provider结果/失败状态先落盘再清理。EXTRACTED/FAILED重试不再次调用；REQUESTED重启视为未知并记FAILED，不盲重发收费请求，不假报成功。状态落盘失败不开始Provider或删除。
- cleanup-knowledge-journal-runtime-1固定上述tree，18/18定向通过，10.376s，前169.948s累计180.324s；覆盖新请求journal失败不调用不删、未知前次调用不重发且清理继续、真实Host→实际存储清理完成但最终回复丢失→重启只读EXTRACTED且提取计数保持1，以及聚合/托管控制相关回归。知识Provider为合成，实际模型、价格和生成知识质量均未验证；无线上数据变动。
- 未触碰其他Runtime dirty路径；无在途测试。真实知识提取实现/公共知识保留及运维配置仍缺，不能拿去重状态机冒充知识功能完成。尝试官方structured-output资料检索未取得可用正文，尚未据此添加Provider SDK/假定模型能力；后续优先核对现有Provider HTTP适配责任层，保留未获授权不向用户加扣费的约束。完整最终收尾/再邀请/自部署/月费与调度/Web/部署范围仍未完成。

## 2026-11-10 启用真实知识提取前的成本归属确认
- 前轮为progress：知识提取去重/故障恢复源码26a951c及18项测试。当前只读HEAD仍26a951c，无在途任务；未新增Provider调用、生产写入或扣费。
- 现行beta-wen-billing.md明确“公共知识提取费用归属尚未冻结，未获明确授权前不新增用户扣费”。这一问题影响真实模型调用的成本主体、后端记账归属及清理后迟到usage，不应在接实际Provider时偷偷当原事项/原用户费用，也不能因为提取在停止后执行就漏记平台成本。
- 向用户逐项确认建议规则：到期解除时公共知识提取由平台承担，只记平台成本，不扣原用户文。尚未得到该决定，不写为已冻结合同；无需用户再次确认公共仓库保留或既有退款/清理边界。目标维持active，不标blocked或complete；其他实施与完整上线尚未完成。
- 文档检索工具未返回可用正文，官方页面直连返回403；没有据此假定新模型/SDK能力或改用未知Provider，没有公开内部配置/密钥。真实知识提取尚未实现/验收，既有18项不能充当真实Provider证据。

## 2026-11-10 用户冻结公共知识提取成本归属（规格更新，未冒称实现）
- 用户明确：提取公共知识产生的模型费用由平台承担。已同步既有计费合同：记录平台实际模型成本，不扣原用户的文、不预占余额、不进入原事项验收结算；保留Agent/提取批次追溯，usage/价格缺失记待核算，原执行迟到成本仍按原绑定处理。
- 本次只读检查UsageCostServiceImpl：现有成本日志与钱包独立，taskId为空时不聚合事项费用，但Binding仍要求ownerJiacn；仅将taskId置空不能证明已实现平台成本归属。后续须在实际提取上报责任边界明确平台归属，不能假冒原用户或未经核实创造平台用户来套用。
- 本次仅更新合同/交接，未修改运行代码、调用付费模型、扣费或发布。真实知识提取、平台成本上报及最终收尾链路仍待实现验证，既有未完成范围不变。

## 2026-11-10 平台知识提取成本账本支持（已定向验证，未发布）
- 上轮为用户费用归属确认/规格更新，属于有效进展；本轮沿真实API源码实现，不将确认本身当运行能力。API候选ae1fba239a1e0b79946775fb7fff8c40a8894f17/tree10456b9f7991b2700a69dc110d2e2353576860ed，工作区干净。
- UsageCostService提供显式platformBinding，空owner/空task表示平台成本，不创建假平台用户/事项；用户成本保持原序列化与receipt hash，原owner/task不能改绑。record/observation使用原绑定的null-safe比较，平台费用不产生事项summary、钱包扣款或预占；实际usage/价格缺失仍待核算。调用方仍须来自可信内部来源，不接受请求自行选择平台归属。Agent/提取批次由来源sourceAttemptId绑定，真实提取生产者尚待接通。
- 初建成本表允许usage owner为空，task summary owner仍非空；新增显式维护迁移migration-platform-usage-cost-20261110.sql，只改该列可空性，不改已有owner/金额/回执、不增CHECK、不在应用启动自动迁移。生产尚未执行迁移。
- 复用本任务既有本地/真实MySQL驱动，platform-usage-api-1固定上述源码，Gradle退出0、validateLayering通过；UsageCostServiceMySqlTest16项+EconomyUsageCostSchemaTest2项全部通过，无skip。新增真实数据库用例覆盖平台实际成本/缺usage/缺价格/重复回执、平台与用户双向改绑拒绝、事项汇总隔离、显式迁移重复执行及旧用户回执保留。没有用户钱包表参与该账本测试，不将其宣称完整扣款链路验收。
- 外层driver误设至少20项，返回FAIL/2；保留原result.json不重标、不重跑应用构建。后续evidence-reconciliation.json逐项核对固定源码@Test方法名与两份XML恰好18项，确认实际测试PASS，记录后处理计数错误；第一次核验误用系统Python3.6未执行成功，改用既定Python3.11完成只读核验。证据目录/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/platform-usage-api-1/。
- 本轮墙钟88.906s，真实MySQL集成/fixture17.981s，受限阶段70.921s；沿已有候选族保守累计251.245s。只有本任务独立临时MySQL被启动/停止，fixture退出事实在mysql-owned/fixture.json；无在途构建，不启动生产服务、不调用付费模型、不扣款/迁移/发布。
- 下一步仍须实现真实安全知识提取及公共知识保存、平台实际usage上报并接CLI，API FINISHING完整handler/未送达技能phase及最终释放、同实例再邀请、自部署、首次技能计费、余下调度迁移/Web和受控上线。账本18项通过不是完整需求完成，原完整目标保持。

## 2026-11-10 公共知识模型调用、隐私复核与持久存储（候选，CLI尚未接线）
- 上轮平台成本账本18项验证为有效进展。本轮Runtime374c36c→5ea5860→340ea06d237ad976c5e6deabf5a6d544b5c4b9d4/tree192b3240c3790dd9c24638a25a80e0845e7a5e03，候选版本1.3.83/bridge1.1.64；仅提交本任务新增模块/测试及Runtime版本，其他dirty路径未动。
- knowledge-responses提供真实fetch Responses传输实现：可信HTTPS精确endpoint/模型/凭据；无工具、无原thread续接、store=false，禁止重定向携带凭据，不自动重试。平台STARTED必须先由持久sink确认才调用；收到响应先保留actual model/service tier/raw usage再检查完成状态/JSON。拒绝/无效输出/HTTP错误仍有成本证据；网络或解析结果不明仅保留STARTED待核算，未借requested model填实际模型或补零。成本记录不含输入/提示/输出/凭据。价格快照取得及API核算仍待真实接线，不能声称该模块已准确算出人民币金额。
- knowledge-extraction按原subject+handover+stage确定费用attempt，先抽象通用知识，再以仅含draft的独立调用做公开隐私复核；失败/结构异常不publish，只写复核后的entries。双调用仅在解除收尾、有源文本且有候选知识时发生，不进入正常事项热路径。空HOME不调用、空候选不复核；输出不能控制路径/命令/授权。隐私复核是模型判断，不是数学匿名性证明，尚需真实材料隐私/质量验收；mock safe=true不能冒充语义已验收。
- public-knowledge-store使用独立host state下public-knowledge与platform-usage，subject/operation以摘要作文件名，原子0600/fsync/独占写入，重复同事实可复用、改写拒绝；与传入任何私有根重叠拒绝、不跟随链接。公共内容不含原owner/会话/draft；平台receipts不混用户钱包，私有Agent根删除后仍保留。这不是允许将原会话迁成公共文件。
- knowledge-extraction-runtime-1固定374c36c，12/12通过、2.516s。knowledge-publication-runtime-1固定最终340ea06，17/17通过、1.197s：包括真实临时磁盘幂等/权限/链接/多Agent隔离，以及本机真实HTTP两次请求→先持久STARTED→保留usage→复核→公开artifact→删除私有根后公共内容/平台receipt仍在。HTTP服务器是合成Provider，没有调用外部模型，不是实际模型质量/价格验收。Node24.22.1/依赖摘要1849a093b5485fc458dd4ad960a01d35539adc7a38ac7affc9111c65ecf77554；沿前251.245s保守累计254.958s，回环用例极短仍全部计受限时长。
- 官方Responses文档web检索/两个官方页面open均未返回正文；未宣称已从官方验证具体模型能力/价格。以上请求合同仍须与实际部署Provider完成后续契约验收，模型名保持用户指定gpt-6-luna，没有替换模型或从未经验证资料补单价。
- 下一步：实际本地会话读取/分批输入，接可信Provider配置/平台价格快照及CLI，再将host持久platform usage传至API账本；当前新模块已有真实HTTP/磁盘组合验证，但未由生产cleanPrivateData调用。最终FINISHING handler/技能结算/关系释放/同实例再邀、自部署/首次技能费/剩余调度/Web/上线仍未完成。未启用生产清理、迁移、收费或部署，原完整目标不缩小。

## 2026-11-10 真实会话读取与CLI知识提取接通（候选，未配置/发布生产）
- 上轮传输/隐私复核/持久存储实现与17项组合验证为有效进展。本轮最终Runtime a29a3723d32d6fcd63c93f85873c88ce80a8af27/tree874e64d36b4606cb67f4c8a1293d3cf1df80b8c5，版本1.3.84/bridge1.1.64；API仍ae1fba239a1e0b79946775fb7fff8c40a8894f17且工作区干净。
- knowledge-sessions从实际停止后的CODEX_HOME按确定顺序流式读取sessions/archived_sessions，仅response_item里的user/assistant文本；不送session_meta/路径、工具结果、图片或重复event_msg，链接不跨HOME读取。按operator指定输入字节容量切批，UTF-8不截断/不丢字符、不一次加载全历史；内存仍会包含当前JSONL记录，不宣称对任意超大单条记录完全常量内存。容量是实际模型上下文留足提示/输出后的配置，不猜模型限制、不加运行deadline。
- extraction改为逐批顺序调用，稳定attempt绑定subject/handover/batch/stage；逐批公开复核后的entries，旧handover恢复仍不会重复付费。源文本首尾空白必须保留，发现原传输exact校验误把输入当标识后已修复并新增回归；没有修改模型身份校验或删除输入字符来绕过。
- knowledge-maintenance与真实CLI已接通：可配置CYF_RUNTIME_KNOWLEDGE_CONFIG_FILE（精确字段configVersion/endpoint/model/channel/credential/maxInputBytes），仅operator0600、所有Agent/managed/host可变根之外；不继承原用户HOME凭据。模型路由在启动读取冻结、仅停止收尾时调用；未配置仍不启用假提取，正常事项执行不受影响。日志脱敏加入平台凭据。可变profile根集合直接复用manifest导出，避免新列表遗漏typedInspectionStateRoot。
- private cleanup真实组合回归：从实际临时HOME读取文本→持久平台STARTED/RESPONDED→提取/复核→公共知识保存→删除私有HOME/state/materials，公共技能/共享仓库Git仍保留；重复清理无第二次调用。Provider返回仍为合成，不代表实际模型隐私/质量/路由验收。未创建生产知识配置、未调用付费模型、未删除生产数据。
- 部署依赖扫描发现旧install.sh显式拷贝表遗漏前序新增evidence/private-cleanup模块；与本轮knowledge模块一并补齐install/validate清单，并补齐validate的api/message envelope。新增入口完整相对import图→两个清单的静态闭包测试，避免源码测试通过而包缺文件。bash -n通过；未执行生产打包/安装，不将静态闭包冒充产物验收。
- 本轮证据：knowledge-sessions-runtime-1固定529b6b0，22/22、1.257s；knowledge-maintenance-runtime-1固定44c20c6，161/161（含runtime-host全文件与CLI源入口）、56.448s；knowledge-cleanup-runtime-1固定230c5cf，33/33、1.907s；knowledge-cleanup-runtime-2固定最终a29a372，34/34、1.931s。均无skip/失败，依赖摘要沿用1849a093b5485fc458dd4ad960a01d35539adc7a38ac7affc9111c65ecf77554，Node24.22.1；既有族保守受限累计316.501s，未重标历史源码测试，无在途进程。
- 下一步明确：平台价格快照在付费前取得/留存、host平台回执与API成本账本的真实受信传输和恢复（当前仅本地持久未入API账），实际Provider合同/隐私质量验收及生产operator基线配置。API FINISHING handler、未送达技能phase结算、关系释放/同实例新邀、自部署、首次技能费、统一调度余项、Web与受控上线仍是原完整范围。源码CLI接通不等于资金闭环/全部上线。

## 2026-11-10 平台知识费用上报API与定向验证修复
- API e3e160bbc0增加原生认证knowledge-usage接口、FINISHING原关系校验、付费前价格快照与Responses实际usage归一化；绑定平台null-owner/null-task，无用户钱包/事项结算写入。尚未接通Runtime上报，未发布。
- platform-knowledge-api-1实际11项中9通过、2失败，受限104.054s：Controller fixture缺原生Proof；金额断言误以原始七位乘积比较六位记账值。7290de8b3e108c9ff3c2160d757d4923e45689e3/tree b652dbd8df0d9048e848e7a82b68bc4f7cb2e08a只修复这两项fixture/断言，未放松生产认证或金额规则。
- 根因矩阵：上述两项是测试输入/断言问题；platform-knowledge-api-2是编排状态blocked_root_cause拒绝，未编译/执行测试，受限7.528s，与此前业务失败不同。现按既有authorize-remediation绑定修复源码恢复验证，不绕过Gradle gate。
- 既有受限316.501s+104.054s+7.528s=428.083s；后续保守剩余171.917s。首轮driver的remaining常量未同步但实际104.054s未超当时283.499s剩余，原证据保留；后续计算已修正。下一轮新目录platform-knowledge-api-3，不覆盖原失败。

- 修复后platform-knowledge-api-3通过：固定7290de8b3e/tree b652dbd8df，11项全通过（无skip），validateLayering通过；受限54.554s、独立集成0s、墙钟54.559s。保守族累计482.637s，剩余117.363s。原两次失败证据保持原状，无在途构建。只完成API生产者入口及核算单元验证，不代表Runtime上报/重启恢复/线上验收完成。
- 下一步Runtime保留本地平台receipt后以原生身份上报；STARTED取得API快照确认再调用模型，RESPONDED传实际usage；清理前flush未ACK费用证据，失败保留原凭据等待恢复，不重放模型调用。共享仓库与Git继续保留。

## 2026-11-10 Runtime平台费用真实原生传输与清理恢复接通（候选，未发布）
- 上轮完成API11项验证属于有效进展；本轮Runtime最终d6954f182c9e702425ae94c8857fa50f8c22e006/treedc58e4f12df474e68621752a46f12788b490ace4，版本1.3.85/bridge1.1.64。只提交18个本任务文件，既有Python/install/new-api等他人修改未动。API仍7290de8b3e，未合入/push/部署/迁移/收费。
- knowledge-maintenance现将本地持久STARTED→原生API快照ACK→外部模型→持久RESPONDED→原生API实际usage ACK串接；复用RuntimeV1Client.session/nativeFetch与readNativeJson，按同CLI启动instanceId、原installation授权，无enroll/register/引擎重启。ACK绑定handover/attempt摘要/原revision，PENDING_USAGE/PENDING_PRICE可保留，不猜零金额/请求模型为实际模型。平台提供者和用户HOME凭据仍分开。
- host journal按subject+lease/handover分区保留原事实和其摘要绑定的API ACK；恢复只扫描本次操作，顺序补送started/responded，不扫全部历史。无会话文本/draft/平台密钥写入成本journal。共享仓库/Git与公共知识保持原保留规则。
- HostingControl传可信leaseId，RuntimeHost首次清理持久cleanupLeaseId并拒绝后续换租约。private-data-cleanup在任何模型调用前要求费用flush适配器，持久EXTRACTED/FAILED后补送费用，未确认前不删私有凭据/数据；重启或失败只补回执，不重新花模型费。提取失败允许清理的前提是成本证据已入账，缺usage保留待核算，不能伪装为已知零费用。
- 新增原生hosting-leases精确POST路由限制；候选CLI/执行工厂、操作journal及受影响fixtures同步。现有接口v1.4/RB-1责任不扩展到Web；业务FINISHING授权仍由API持有。合同已回写beta-wen-billing.md“平台知识成本上报与清理顺序”，Runtime README如实标记未发布/未完成的业务链路。
- 第一次knowledge-delivery-runtime-1在fixture准备mkdir失败：driver误保留旧短临时根kcr2，不是测试失败、未执行应用测试。原错误保留，result.json记录从空输出目录创建到失败后观测的44.333s保守上界（含观测间隔，非精确执行耗时）；没有删除/接管旧目录。修正新driver使用kdr2、新输出knowledge-delivery-runtime-2，没有重放同错误。
- knowledge-delivery-runtime-2固定d6954f1，206/206通过，0 fail/skip/cancel；墙钟60.186s，全部保守计受限阶段。包括原RuntimeHost全文件/CLI source slicing、HostingControl、知识各模块、存储与native HTTP合同。Node24.22.1，固定依赖摘要1849a093b5485fc458dd4ad960a01d35539adc7a38ac7affc9111c65ecf77554。沿历史候选族人为保守累计586.156s；其中本次固定Runtime候选准备上界44.333s+实测60.186s=104.519s，不将历史不同源码候选族累计解释为用户整个开发过程600秒限额。下一实际固定源码/批次仍按根AGENTS执行同批累计，不能重试重置。
- 新增真实回环HTTP：真实RuntimeV1Client从磁盘原授权换原生会话、验证Q/R关联与native headers、先STARTED确认再模型调用、传实际usage、无pending时不再换session。API响应与模型输出仍合成；不冒称真实Java Controller/数据库/模型价格或隐私语义已验收。另以真实磁盘验证RESPONDED在模拟数据库commit后丢ACK，旧私有数据完整保留，重建maintenance后同事实重送、Provider仅调用一次，费用ACK后才删除。
- 没有在途测试/构建，未启动生产服务或外部付费模型。接下来必须做真实Java+Node+账本集成（价格快照/ACK丢失/实际认证）以及完整FINISHING handler：事项终结→真实停机→旧执行证据→技能财务结算→知识/平台成本→私有清理→关系释放/授权撤销；旧unbind/repair旁路、同实例再邀请、self-host、首次技能费、剩余统一调度/Web/生产配置/完整上线仍未完成，不缩小原目标。

## 2026-11-10 平台知识成本Java/Node/MySQL联测推进与fixture归因
- 原Runtime206项通过为有效进展；本轮新真实联测批次固定API31b6a10b32→079e32f09b、Runtime3ec4888→0ff1d49（后两次仅诊断fixture），使用实际RuntimeV1Client/maintenance→回环HTTP→Java生产Q/R advice、原生认证服务/filter/controller/normalizer→Spring独立事务与MySQL成本表。身份DAO/FINISHING discovery是明确合成，未声称全套生产身份SQL或模型语义验收。
- knowledge-http-api-1失败：成本流程在provider前停止，node fixture宽泛assert.rejects误当预计的RESPONDED丢ACK，后续spent=0暴露；受限48.833s/集成13.132s/墙钟61.965s。保留原结果，第二候选收紧assert要求确已调用Provider并保留HTTP阶段/服务端异常。
- knowledge-http-api-2仍失败但证据明确为session403：测试将AgentRuntimeAuthenticationFilter无条件挂全部路径，遗漏生产AgentRuntimeSecurityConfiguration.securityMatcher(selectsRuntimeCredentialLane)，导致installation-Bearer的session被错误送入封闭native操作列表。非生产功能缺陷，未发生模型消耗/记账；必须在fixture按同生产matcher分流，不修改放宽生产allowed路径。
- 修复矩阵：第一次是错误被断言遮蔽（已收紧）；两次实际根因是测试credential lane组装错误（本轮按生产matcher修复）；不是API成本账本或协议金额问题。不原样重试，不重标前两次PASS。继续通过既有remediation绑定修复源码恢复验证，无新审批或生产操作。

- 第三轮联测在途时磁盘剩561MB，已只回收knowledge-http-api-1和-2/mysql-owned/data这两份本任务已停止的合成MySQL数据：逐一核对fixture.json owned/exitCode/endedAt、失败结果和原PID不存在。保留mysql.log、fixture.json、Gradle/XML/result/Node日志、源码与所有生产数据/备份；未清理在途第三轮。

## 2026-11-10 平台知识费用真实联测通过（候选，未发布）
- 最新用户决定：公共知识提取产生的模型费用由平台承担。提取与隐私复核均不扣用户文、不预占、不并入原事项结算；保留实际usage及价格快照，缺usage/价格标记待核算，不当作零成本。共享项目仓库及Git历史仍作为公共数据保留。
- 第三轮knowledge-http-api-3定位实际生产协议缺陷：伪造原生token正确返回401，但AgentRuntimeAuthenticationFilter.reject旧code-only JSON不能被Runtime v1.4解码。API82c92090c8改用既有JsonResult.failure及RequestIdFilter关联，保留认证/ACL与原状态码；761d046cfd修正断言为标准五字段，不放宽Runtime解码。
- 第四轮knowledge-http-api-4已终态PASS：API761d046cfd10489c7cb0a01f8d73a9b0e49d9dd5/tree ebf75db570f0a3606fcb4f859e3a514609d3c4e2，Runtime0ff1d4998d45b9c17422cdb9275e195234ecb39e/tree56fb81a1d97181d48c1fe0c485752f4976b2f0bc。30 tests，0 failures/errors/skipped，validateLayering通过。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/knowledge-http-api-4/result.json；日志及XML保留同批目录。
- 真实Node→Java原生认证/Controller→MySQL事务验证价格快照0.000132元、提交后丢ACK重送不重复记账、不再次调用模型、缺价格/usage待核算及伪造token拒绝。身份DAO和FINISHING发现为合成fixture，外部Provider为合成；不冒称真实供应商计价、隐私语义或完整生命周期验收。
- 本轮墙钟92.412s，其中真实集成11.606s、受限80.802s；同批前序受限145.348s，累计226.150s（600s以内）。保留前三轮失败，不重标通过。无在途验证，未发布、迁移、扣费或调用外部付费模型。
- 第四轮前仅回收第三轮已终态且PID不存在的任务自有合成mysql-owned/data；保留fixture.json、日志、XML、result、源码与生产数据/备份。第四轮数据未删除。
- 完整FINISHING编排、旧unbind/repair旁路收口、同实例再邀请及self-host、技能费用与统一调度余项、Web/线上验收仍未完成；此次通过仅覆盖平台知识费用链路，不代表全任务完成。

## 2026-11-10 最终收尾依赖检查：托管恢复发现按进程环境分区
- 前一轮已取得真实平台费用联测PASS并保存证据，为有效进展。本轮继续完整目标，不将费用链路通过当作生命周期上线。
- 发现HostingRentReconciler两个后台队列原先跨环境ORDER BY/LIMIT后再preview过滤，违反后台发现先分区规则，并让其他环境数据占据本环境分页。已在EconomyHostingRentMapper的selectPendingIntents/selectPendingReprovisions下推可信FixedTenantAdmissionPolicy的tenant/client；client未固定时只放开同tenant的client，大小写精确匹配。原preview活动准入、binding/intent/lease事务与外部I/O边界保持；不扩大Web或执行入口修改。
- 固定API 2fc7ca09491ed8efaf068cd9a59abf52c7106d18/tree 2230a409c2e4884b2de590ca401b0af805b14ee4。生产调用方仅HostingRentReconciler；构造测试、分页测试及动态MyBatis SQL绑定测试已同步。定向managedHostingRegression HostingRentReconcilerTest与validateLayering通过：13 tests，0失败/错误/跳过；受限95.936s，集成计时0s，墙钟95.94s。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-discovery-scope-1/result.json。本轮SQL为真实动态解析/绑定验证，未冒称已覆盖真实MySQL跨环境100条分页；该数据集成仍应补充。未合入/push/发布/迁移/扣费。
- 再次核对最终停止的实阻点：UnixManagedHostingProvisioner.prepareAndObserve会ensure激活，不可用于FINISHING发现；Runtime hosting-control.mjs只允许activeOperationKey且admittedAt非空的代次quiesce。较高已prepare但未admit代次不能冒充当前运行代次，API当前也没有只读解析当前admitted关系的端口。后续须补这一个明确的Runtime边界，再接最终handler，不放宽停止合同或使用最新候选猜测。

## 2026-11-10 当前已受理代次查询与停机竞争修复（验证中）
- 新增hosting.current只读原INITIAL关系查询，返回持久activeOperationKey而非latestGeneration；API/Runtime同一合成fixture及合同已同步，不prepare/ensure/enroll。Runtime版本候选1.3.86，API候选4aa1df6187；尚未发布。
- Runtime第一次hosting-current-runtime-1：31/32通过；新增foreign initialIntent测试未同步INITIAL operationId，被正确wire拒绝而非预期association拒绝。修正合成fixture，不放宽身份校验，失败证据保留。
- 检查同时发现实际竞争：已prepare未admit的ensure可在永久quiesce后改变activeOperationKey。新增精确检查，仅拒绝停止后未admit操作，不改变普通执行。第二次hosting-current-runtime-2：32/33通过，新竞争测试通过；但过宽ensure拒绝破坏原admitted只读重放（旧合同UNKNOWN）。已收口为operation.admittedAt===null才拒绝，不激活旧操作、不放宽新admission。
- 根因矩阵：第一轮为fixture内部INITIAL不一致；第二轮为新增guard范围过宽；与已通过费用HTTP链路的401信封修复不是同根因。两个失败均保留，无原样重试。下一轮固定修复源码重跑完整hosting-control并验证API codec/事务外边界；已受理停机重放和新候选拒绝须同时通过。
- Runtime第三轮hosting-current-runtime-3固定6f6043a：33/33通过，0 skip/fail，4.240s，同批前三次累计12.494s。API第一轮hosting-current-api-1误复用不含UDS配置的driver：两个既有Unix socket测试因批次tmp路径过长失败、真实Node联测因缺CYF_GSS_RUNTIME_TEST_SOURCE跳过，新增current单元断言通过；原81.837s失败保留。改回既有cleanup-control driver的短普通磁盘tmp/明确Node与干净Runtime源码环境，不改生产传输/测试断言绕过；再增加真实Java→Node current选择与停机后第三代ensure拒绝验证。

- API第二轮hosting-current-api-2已PASS：固定37eac21b8c12816670f3f6daff1a33e155311500/treeccb95a9113e6e5b482077b67962f39f726f3cad2，Runtime6f6043a667c47448ca819e3c4efea435032d318b（1.3.86），19 tests，0 fail/error/skip，validateLayering通过。真实Java adapter→Node Runtime UDS验证已prepare第三代但当前仍第二代、实际quiesce之后第三代ensure被拒绝、current不变，以及原费用证据/私有清理幂等链。身份/API executor为合成fixture，非生产业务最终解除验收。真实联测方法XML耗时['0.76']秒；driver保守将整轮55.55s计受限（其中含该真实集成，不把它冒充单元测试），前次81.837s累计137.387s，小于600s。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-current-api-2/result.json，原失败保持。
- current查询只返回operation+候选公共标识，不返回enrollment secret/hash；Candidate未用于重新授权，调用路径无ensureInstallation。停止竞争修复保留已admit ensure只读UNKNOWN重放，仅拒绝quiesce之后未admit的新代次。无在途验证，未合入/push/上线/迁移/真实费用。
- 下一主线：以原FINISHING lease/binding建立事务快照，事务外current→quiesce→flushEvidence；补技能财务终结（不得凭PENDING判定未发送）、cleanup成功后原关系最终释放/授权撤销。不得调用prepareAndObserve发现目标；原unbind/repair旁路、再邀请/self-host/技能首次费/调度余项/Web及完整上线仍未完成。

- hosting-completion-api-1真实MySQL回归在途时磁盘剩419MB；仅回收已PASS的knowledge-http-api-4/mysql-owned/data（163MB合成测试库），核对fixture owned/exitCode=0/endedAt、终态result及PID695445不存在。保留原fixture.json、日志、XML/result/源码/全部生产数据备份；未碰在途hcomp1测试库。

## 2026-11-10 最终解除财务事务原语完成验证（未接最终handler/未发布）
- API 19132aca8d56a9231dd6e0ff3f5b6e9fe7b74b87/tree461b72d00afbb41d1da542d6cc3b588716bdb1c2。内部HostingRentRenewalService.completeHandover要求调用者已有关系释放事务，锁原lease并核对USER付款主体/binding/Agent。仅FINISHING→CLOSED/live_slot=NULL，保留原paidFrom/paidThrough/latestIntent及账本；同关系CLOSED重放不加版本、不碰后续邀请的租约；ACTIVE/错主体/换绑拒绝。无退款/扣费/额外schedule查询，无Runtime调用，无数据库CHECK或新表。
- 执行固定源码HostingRentRenewalMySqlTest全套与validateLayering：31 tests，0 fail/error/skip；真实MySQL验证关闭重复、原关系保留、同实例新租约占位可用但旧重放不改新租约、caller回滚保留live slot、拒绝不完整事务及错owner/binding/Agent，连同既有续费/15天/资金并发回归通过。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-completion-api-1/result.json，短测试库根/home/isp/state/cyf-test-tmp/hcomp1/mysql；未使用生产库。受限95.373s，独立真实集成47.547s，墙钟142.922s。
- 此原语不能单独挂到移除入口：最终Agent handler仍须先实际停机、原证据与技能费用结清、平台知识成本与私有清理成功，才与binding/授权撤销同事务调用；源码方法通过不代表整个解除流程完成。
- 下一收口的锁序已核对：Runtime ensureInstallation先锁installation再binding→intent→lease；最终释放也须先取原installation锁，不能binding→runtime.revoke造成反序。AgentHostedBindingTransaction旧suspendDatabase保存历史binding并清runtime归属可供按职责复用，但prepareUnbind(hosted=null)及completeUnbind仍有未接清理旁路，不能沿旧调用直接宣布收尾成功。HostingRentOwnerResolver.requireOwner依赖用户可登录，只适合新请求；后台最终收尾须用可信原租约/绑定事实，不因原用户被禁用永久卡住清理。
- 当前无在途验证，未合入/push/部署/迁移/真实扣费。任务保持完整范围，下一步仍为最终生命周期编排及技能财务收口，不将财务单项验收当作完整上线。

## 2026-11-10 原关系最终提交推进（验证中）
- 新增HostingRentHandoverCompletion，供未来生命周期Owner收到CLEANED后调用；同事务installation先锁，再原binding→初始intent→lease，校验原关系/当前host及无未完成事项，撤销Runtime授权及存在的原专用key、关闭财务占位、挂起binding/identity、清原runtime归属，不删除实例/公共数据。CLOSED重放不触碰后续邀请者。没有把它挂入旧unbind或生产入口。
- 首次hosting-release-transaction-1固定27bac029cf：6项真实Spring事务代理/H2 effect测试通过，但validateLayering失败（新Agent service直接依赖EconomyHostingRentMapper，G1无例外），整轮FAIL保持，受限99.834s。修复不添加baseline豁免：原intent/lease锁和读取移至既有HostingRentRenewalService.lockHandover，Agent只消费财务API快照；新增真实MySQL快照事务边界验证。
- 根因矩阵：当前为新服务跨模块mapper越界；之前hosting-current-api-1为UDS driver临时目录/环境错误且随后19项真实跨端已通过，非同根因重试。当前修复改变依赖责任边界及相关fixtures，不删除分层门禁；下一固定源码跑completion+renewal MySQL和layering。任务仍未达到完整验收条件。

- 第二轮关系事务验证在途时磁盘剩299MB，已仅回收旧hcomp1/mysql/data的167MB合成测试数据：原hosting-completion-api-1为PASS、MySQL日志明确Shutdown complete、socket已不存在且/proc无该datadir的mysqld；保留mysql.log、源码/driver、XML/result和其他证据。未删除在途hrel2或生产数据/备份。

- hosting-release-transaction-2已终态PASS：固定API75dd35ab0be7dfb83163f829e83fe5ee14bee7db/tree e7d6513ac4511681d7bad30ade705edf4e52c8fa，38项、0失败/错误/跳过，validateLayering通过。墙钟135.839s，真实集成42.281s，受限93.553s，与前轮99.834s累计193.387s。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-release-transaction-2/result.json。原G1失败保持，不添加分层豁免；本次为财务API快照及最终关系事务验证，不代表完整FINISHING handler或生产发布完成，publishable=false。公共知识提取和隐私复核继续归平台成本，不扣用户；该费用链路既有30项真实联测已通过，仍未上线。

## 2026-11-10 真实停机事实与迟到技能回执闭环（实施中）
- 上轮38项通过及真实结果落盘为有效进展。本轮仍推进完整目标，重点解决PREPARED迟到后创建ACTIVATE的真实缺口。FINISHING本身不是停机证据，已受理安装在尚未实际退出时仍可完成，不能用欠费/FINISHING状态直接退款或禁止旧执行。
- 沿原lease增加handover_id/executor_stopped_at这一生命周期事实（无新表、无新调度框架、无CHECK）。只有最终Owner收到原Runtime QUIESCED后在原绑定事务记录；租约锁下验证原付款人/Agent/binding和FINISHING，原handover重放幂等、其他handover拒绝。schema/fresh DDL/显式结构升级同步，历史行不回填“已停止”。当前尚未接最终Owner调用，不冒称生产事实已存在。
- SkillManagement结果责任层在真正已停止时收到PREPARED：保留原回执，不创建ACTIVATE，按原订单释放安装费用（因本事务尚未生成激活意图，非凭PENDING猜未发送）；真实APPLIED仍结算、UNKNOWN仍待查且不退款。已有DISABLE的NOT_STARTED终结不再无限生成修复发送；已停止后的变更派发拒绝，普通事项执行入口不动。该停止标识不替代原identity/installation/host绑定。
- 现有actor→installation→binding/runtime→skill与原租约锁序已检查；最终释放也先锁installation，租约续费不反向取installation。增加查询仅在技能结果/派发冷路径，不逐消息/逐token查询，不添加主业务成本门禁。缺失的已发命令仍须由停止后的原命令查询证据结算，不能据此宣称全部技能财务已终结。
- 接下来固定候选跑原真实MySQL租约全套、新结构迁移及技能全套事务回归、validateLayering；完整FINISHING handler/旧旁路/再邀请/self-host/调度/Web/上线范围不变。
- 固定候选API75f748c8f6，hosting-skill-stop-1在途，真实租约/技能MySQL共预计93项及validateLayering；新增结构迁移保留历史/原关系停机幂等/回滚/错付款人、迟到PREPARED无ACTIVATE退款、UNKNOWN不退款、APPLIED仍结算、派发停止和DISABLE终结回归。driver路径/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-skill-stop-driver.py；本批独立源码/受限预算600s，真实MySQL回归单独计时，未发布。
- 启动前仅删除已PASS且明确Shutdown complete、socket不存在、/proc未运行该datadir的旧hrel2/mysql/data；保留该批mysql.log、测试报告、源码及所有生产状态/备份，未动新hstop1。
- hosting-skill-stop-1已PASS：API75f748c8f6b601c569437fa9a6b9b0dece552d5a/tree29e1fd39cb145b8f042117e98ad0315e403a8cfa，93/93、0失败/错误/跳过，validateLayering通过。墙钟346.080s；真实MySQL233.041s、受限113.035s。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-skill-stop-1/result.json。租约/资金SQL真实，技能测试中的租约发现及身份/session仍为合成，外部模型无调用；不是完整收尾验收或上线。
- 继续接实际停机生产者：HostingRentManagedStop只读current→原关系/未完事项事务校验→事务外原代次quiesce→原关系事务记录executorStoppedAt。handoverId固定原leaseId；不prepare/ensure/enroll、不清理/释放。原关系锁/校验从最终释放方法抽为同一私有责任实现，避免多处复制。当前尚未注册最终FINISHING handler，接线及全链验收仍待完成。
- hosting-stop-owner-1已PASS：APIba9cc8f775db0936ac369303e36aaa5a804b0870/tree791c58dc9a33da4d08dccbed96ce334efdbce0b4，14/14、0失败/错误/跳过，validateLayering通过；受限119.405s、墙钟119.407s，无真实MySQL回归计时。证据/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/hosting-stop-owner-1/result.json。覆盖实际Spring代理事务/H2 effects及Mock Runtime编排（不得冒充本轮真实UDS联测）：没有QUIESCED不记停机、未完旧事项不停止、原代次/leaseId稳定、DB确认失败同handover恢复、停机事实不撤身份/释放关系。前轮93项真实MySQL事实保持原候选证据，两个候选均未发布。
- 当前无在途测试，API工作区干净。新增ManagedStop已是实际current/quiesce适配器消费者，但最终FINISHING schedule handler仍未注册，不能宣布最终业务接线完成。
- 下一实阻点仍是已存在ACTIVATE/POLICY但Runtime无原journal的操作。源码核实SkillManagementService.dispatch目前事务后调用sessions.dispatch；仅PENDING无法证明未发。Runtime._finishRead对missing observedCommand正确返回UNKNOWN/INTEGRITY_UNPROVEN，不能改成退款事实。须查原transport/outbox领取事实能否证明未交付；否则补最小持久发送事实及停机后的原命令观察，保持无法确认的历史事实UNKNOWN。不要为补齐链路将缺记录当NOT_STARTED。
- 额外已核实但未修改：native证据链SkillAgentVersions.requireOwned依赖HostingRentOwnerResolver.isAuthenticatable；AgentRuntimeAuthenticationService.validateRow也校验原account/authEpoch。禁用原用户会拒绝其原native证据身份；不能只删业务登录检查或放宽native认证当修复。后台最终关系事务本身未依赖原用户可登录，原证据维护授权仍须在明确的可信维护边界处理。
- 停机后资金收口的下一步发现（源码依据，尚未修改/验证）：AgentSkillInstallRecoveryMapper.claimOutbox在调用SkillInstallDispatchService之前，同原delivery/outbox事务持久attempt_count+1、CLAIMED、租约；finish不清attempt_count。有可能直接复用该事实识别**从未领取的原native marketplace outbox**，避免新增发送字段。须在同原skill/installation事务锁原delivery→outbox、验证完整source/wire/hash/attempt及attempt_count=0/no lease，再关闭原命令；并覆盖已发现candidate并发迟到claim/dispatch。不能仅看command.PENDING、只看当前attempt或只看outbox.status。
- 仍需先核完旁路：AgentCommandRabbitConsumer.dispatchAcquired也会调用skillDispatch，但前置inboxService.claim依赖source settlement；原native destination从不设publisher确认，不能未经验证推断该路径不可能。PositionSkillService的native命令由positionCommand直接返回，不经过相同outbox；不得将普通市场“未领取”证明套到position变更。已领取/发送不明或历史证据缺失保持UNKNOWN。下一动作先封闭这些真实路径，再实现已证明未派发的费用释放，而不是另造通用消息框架。

## 2026-11-10 复用原outbox证明未派发并释放技能费用（实施中）
- 上轮93项真实MySQL和14项停机编排/事务均已PASS，为有效进展。本轮工作区基线ba9cc8f775干净，继续完整目标。
- 旁路已核实：Rabbit Inbox实际decodeFrozenWire要求旧task根schemaVersion/字段，SM-C1为protocolVersion+data；且validateOutbox要求aggregate_type=task和PUBLISHED。市场原native outbox为skill-change、NONE发布确认，既有Rabbit源准入拒绝，不靠删除身份/ACK校验。Position命令则由native reconcile直接返回，不使用市场outbox，本次明确不套其未领取证明。
- 未派发证明复用SkillInstallCommandWriter及原transport DAO查询：同事务锁delivery→active outbox，仅原生市场生产的初始版本0、delivery attempt_count=1/outbox attempt_count=0、PENDING且无lease，且原关系/command/message/attempt/wire及payload摘要完整时成立；claim发生在真实send之前且增长版本/次数，完成/过期不重置。仅PENDING、当前缺Runtime journal或空查询均不能退款。原DAO的activeOutboxes查询从Hall子接口提升到共同transport接口，复用既有Mapper/实现，不加新表/SQL路径。
- 内部cancelUndispatchedForHandover只针对原实际停止租约/绑定/installation/host，复用原runtime锁序，不要求原用户仍可登录（不放宽外部native身份校验）。资金释放/原安装终结/命令CANCELLED同事务；CANCELLED是API未派发取消事实，不伪造Runtime NOT_STARTED或result receipt，真实原PREPARED记录保留。已领取、UNKNOWN、READ、position或缺证据返回未终结，不能清理。迟到旧candidate即使claim，也须在派发责任层遇到CANCELLED拒绝网络发送。
- 必要验证：真实MySQL首次/ACTIVATE未派发退款幂等、原回执保留、领取过不退款、stale candidate拒发、事务回滚、原用户登录失效仍可内部结算而新请求拒绝、错绑定/未实际停机拒绝、DISABLE无退款保留公开安装、摘要不符不退款；并以生产Inbox decoder验证真实native wire不可绕Rabbit派发。运行原技能全套及原关系/停机/transport事务用例和layering，不改变整体上线范围。

### 2026-11-10 未派发回归首轮失败归因及修正
- 固定API092799a6074425bfd5aab674e951d25361ff8e93/tree7f0f74d4571e79a1d86722e5ae5e0d7a3170d344，hosting-undispatched-1真实结果FAIL：84项中82通过、2失败，layering未执行，不发布。墙钟309.887s，真实MySQL回归209.296s，受限阶段100.591s。
- 两处为测试夹具错误：Mockito `when`重设原requireOwner时先以null触发既有拒绝逻辑；真实Inbox将非原task wire的解析失败包装为AgentInboxIdentityConflictException/WIRE_CANONICAL_PROVENANCE_INVALID，而非裸IllegalArgumentException。仅改成doThrow及精确异常断言，未改业务/认证准入、未删测试。
- 修正候选e9568b8501，hosting-undispatched-2继续原84项+layering；保守携带前轮100.591s受限时间，不重置预算。当前验证在途，结果未宣称通过。完整来源与日志在既有任务证据目录。
- 前轮hstop1测试MySQL数据是在PASS/Shutdown complete、socket不存在及无使用该datadir进程后定向删除，日志/XML/源码及结果保留；未触及生产、共享仓库/Git、备份或他人数据。本轮临时数据库由测试正常退出清理，无手动清理在途数据。
- 平台公共知识提取/隐私审核费用规则已在合同和记账实现收口；实际usage缺失或缺价仍待核算，不扣用户钱包，不并入事项结算。此状态不代表完整FINISHING业务链或生产发布完成。

- 修正回归已完成：API e9568b85011a734a76617d3c7c145d3779f69633/tree 1b3cc5c41558ec652c0acaeec3f2a09c9333bff1，hosting-undispatched-2 **84/84、0失败/错误/跳过，validateLayering通过**。墙钟275.796s，真实MySQL回归210.221s，受限65.57s，加前轮累计166.161s，未超600s。未发布；前轮失败仍保留。
- 下一动作：收口已原回执确认FAILED_RETRYABLE但仍HELD的技能资金；复用原订单退款，不再次将已FAILED安装/entitlement执行失败CAS，保留真实回执。之后才接最终FINISHING handler，不能把84项通过当作完整上线。

## 2026-11-10 已确认失败技能的最终资金收口（实施中）
- 上轮为有效进展：e9568b8501的84项+layering通过，当前无在途测试，API干净后开始本轮；不是阻塞或重复等待。
- 责任层仍在技能业务服务：将内部入口更名settleStoppedChangeForHandover（无外部接口/兼容分支），原真实停机/原关系锁保持不变。已有FAILED_RETRYABLE且原RESULT回执持久时，复用原订单退款，终结为FAILED_FINAL/ENTITLEMENT_TERMINATED；不重做已经FAILED的安装/entitlement CAS，不改原回执或公开包。
- 复用既有terminateSupersededFailures退款代码为私有terminateFailedChange；正常重试和被后续变更替代的规则不变。UNKNOWN、已领取无结果不退款，APPLIED已捕获费用不回退。position仍不套市场outbox证明。
- 定向验证增加真实MySQL失败退款幂等/原安装与回执不变、父事务回滚、UNKNOWN不退、已APPLIED不退；原全套保留。未接最终handler，未发布/迁移/真实扣费。

- 本轮已完成：API a8050104eef501695ec46e4ce31ede354f1124b8/tree 83805097dcf2833e9728cb9f8dffd0eaef8fb342，hosting-failed-settlement-1 **88/88、0失败/错误/跳过，layering通过**；墙钟317.664s，真实MySQL回归213.271s，受限104.389s。API干净，未发布。

### FINISHING统一调度实际接线候选
- 新增HostingRentFinishingHandler注册原hosting-rent.finish，不另建定时器/队列。以原租约key发现原绑定、从经济API读取INITIAL意图（不新增Agent直连经济Mapper/G1豁免），调用既有事项收口→ManagedStop→原证据flush→技能资金收口→Runtime.cleanup→最终关系事务。外部调用不包数据库事务；未知/失败抛出使既有调度器保留原key重试，不另造重试状态。
- 技能发现限定tenant/client/Agent/原owner/installation/host，沿既有created_at/change_id索引游标分页，每页100；仅HELD、FAILED_RETRYABLE或原未终结变更进入收口，终结历史不反复结算。LEFT JOIN保留缺命令但资金仍HELD的异常，不能因关联记录缺失误报无待结费用。每项仍复用原锁/事务；分页本身不证明停机/清理。
- 生产接线候选待本轮验证；九项handler顺序/未知/最后事务恢复/陈旧key/错误分区/调用事务/缺INITIAL测试使用mock，只证明编排，不冒充完整真实Runtime联调。原真实MySQL技能增加2项发现/余额与UNKNOWN保留；保留之前88项。
- 待继续：原unsafe unbind/repair旁路、同实例重邀、自托管/剩余统一调度迁移及全量交付审计，实际生产迁移/发布、跨端验收尚未完成。此次注册不能代表上述均解决。
- 接线验证期间只读确认旧旁路范围：AgentController.DELETE bind已经调用HostingRentApplicationService.remove→stopRenewal，不再调用旧unbind；AgentPersonaProvisioningService.unbind当前生产源码无调用方，只有测试。仍实际暴露的是POST /personas/bindings/{bindingId}/repair→repair→resumeRepair，SUSPENDING分支会调用completeUnbind并直接停用关系，未经过新cleanup。下一轮针对这条真实公开旁路及已无生产调用的旧unbind路径单轨收口，不误称DELETE新路径仍有同一问题。旧server bind已在Controller拒绝，local bind仍走旧本地准备流程，须同自托管月费准入一并核对，不能仅删除旧server代码就宣布全模式闭环。
- 本轮源码静态追查的待修点：handoverPendingPage现在包含FAILED_RETRYABLE，但settleStoppedChangeForHandover对positionChange在读取原RESULT前直接返回false；因此无费用的岗位技能已有确定失败回执时也可能永久阻塞最终cleanup。不要放宽岗位命令的未派发证明；应仅允许原已验证FAILED_RETRYABLE的终结复用同一失败事实、保留岗位证据/公共包，无订单则无退款，再将position排除限制收窄至pristine-outbox分支。该问题是新最终handler调用范围发现，待当前固定源码验证终态后再改，不能因99项结果为绿而忽略。

- FINISHING接线首轮验证终态PASS：API 557401aad141cb012098b3b5c7812218571a7187/tree 0cacc601f11288751d59574a711aefe806fd240e；hosting-finishing-handler-1 **99/99、0失败/错误/跳过，validateLayering通过**。墙钟341.851s，真实MySQL回归226.983s，受限114.861s。当前无在途验证，API工作区干净；源码已注册handler，但九项编排测试不是全链路实测，上一条岗位技能确定失败的收口缺口仍待修，不能把PASS扩大成完整可上线。未迁移/发布/真实扣费。
- 下一条动作先修positionChange过早排除：只在pristine市场outbox分支排除岗位命令，原确定失败RESULT可以无订单终结；补岗位原结果/无订单资金不变及缺证据不终结回归，然后核准分页跨100条及真实调度注册/Runtime联调。其余完整目标保持，不缩成这轮99项。

## 2026-11-10 岗位技能确定失败与最终收尾发现边界
- 上轮实际接线并取得99项PASS，属于有效进展；本轮起点557401aad1，API干净且无在途验证。
- 将position排除仅保留在市场pristine-outbox证明分支；原持久RESULT/FAILED_RETRYABLE可使用既有终结逻辑，无订单则不触钱包。新增测试走真实reconcilePosition创建command/candidate、原result处理，再进入停机收口；岗位policy存储/native身份是夹具，SQL安装、回执与资金表真实，不伪造原市场收费单为岗位单。
- 实测覆盖候选：岗位确定失败保留安装/entitlement/回执、余额无变化；岗位PENDING不能套市场未派发证明、岗位UNKNOWN不终结；LEFT JOIN查到持款但命令缺失时保持未结清而不误报ready；相同created_at的101项跨页与其他owner过滤。新增真实Spring条件注册+JobAutoConfiguration初始化，确认只在租赁调度开启时注册原FINISH handler，不以直接new对象代替注册验证。
- 当前为新候选待验证；生产、发布、全链路及旧repair旁路仍未完成。
- 首轮hosting-position-final-1在27项managed回归中26通过、1失败，技能SQL与layering未执行。原因是实际Spring会对mock SkillManagementService调用@Autowired setter，测试把依赖注入误判为业务执行；已只修正为禁止settleHandoverChanges调用，仍验证其余依赖无业务调用。未改生产行为/条件注册，保留FAIL。受限77.061s累计带入重跑，根因与此前Mockito restub不同，不盲重试。修正候选4dfa23b054继续105项。

### 岗位收尾本轮重试根因矩阵
| 证据批次 | 根因 | 修正/影响 |
| --- | --- | --- |
| hosting-undispatched-1 | 旧Mockito restub执行原answer、Inbox异常包装断言错 | e9568b8501修正后84项通过；后续88/99亦通过；非当前输入根因 |
| hosting-position-final-1 | 实际Spring依赖setter注入被verifyNoInteractions误判 | 4dfa23b054区分setter注入和settleHandoverChanges业务执行；不改生产 |
| hosting-position-final-2 | ledger累计失败进入blocked_root_cause，transition被拒；shell未以set -e停止，driver被原Gradle准入再次拒绝 | 无Gradle/测试启动，保留4.421s真实开销；现走原authorize-remediation入口，后续命令使用set -e，累计受限81.482s，不绕锁/准入 |
- 磁盘接近满时，仅清理本任务四个已PASS旧验证批次的派生.class输出（不是最终安装包，不触保留策略内的制品）：hosting-undispatched-2、hosting-skill-stop-1、hosting-stop-owner-1、hosting-release-transaction-2。逐文件确认非链接、结果PASS且publishable=false、无/proc进程cmdline/cwd/fd引用，再留完整源commit/tree、原result摘要、14031个文件SHA/身份清单后删除，78,654,229字节；释放后可用约143MiB。源码、JAR、XML/HTML、日志/result、当前批次和生产/备份未动；证据completed-verification-classes-cleanup-20261110.json，未伪登记整个仍在进行的任务完成。
- 原生岗位真实路径测试暴露实际多余写入：settleStoppedChangeForHandover在UNKNOWN岗位变更上仍调用市场actorLock，插入不需要的agent_skill_actor_root(owner)，而原岗位协议没有payer/market actor。应保留市场分支原actor锁，岗位分支只复用原installation/binding/技能根，不新增市场根；UNKNOWN/PENDING没有业务写入。本轮固定源码仍运行，待终态后修正，不通过放松资金/快照断言绕过。
- hosting-position-final-3终态FAIL：105项103通过，岗位UNKNOWN/PENDING两项精确快照发现多余market actor root，其余原生岗位失败收口、分页及Spring注册均通过，layering未执行。墙钟380.135s（含真实回归320.542s），受限59.593s，连同前两次累计141.075s。修正仅让市场变更保留actorLock、岗位仍锁原installation/binding/lease/skill；不放松断言，确定失败测试也新增actor-root不变断言。
- 剩余统一调度迁移的当前源码定位（只读，不声称已改）：HostingRentReconciler仍@Scheduled 5s且wake仅AtomicBoolean，ApplicationService在174/328行afterCommit唤醒，尚非同事务持久调度；SkillInstallRecoveryService仍@Scheduled 5s扫描原outbox并独立领取；AgentStatusMonitor仍@Scheduled离线扫描。现有ScheduleService.signal/reschedule/cancel可直接复用，JobAutoConfiguration真实注册已进入测试。本轮不临时为这些入口另建新调度器；后续按事件/必要周期分开收口，不能因FINISH handler完成就称统一调度全面完成。

- 本轮修正验证完成：API 1ef7fffc36424584cc697750202fe76bb7474e2f/tree c48c1576e16ddd635a9bff1e3bcf1c2c824e17e2，hosting-position-final-4 **105/105，0失败/错误/跳过，validateLayering通过**。墙钟374.074s，真实MySQL回归254.222s，受限119.835s，含前轮累计260.91s，未超600s；此前FAIL保留。当前API干净，无在途测试或清理进程，未合入/发布/迁移。
- 已验证原生岗位真实command/candidate/result SQL→停机后无订单终结；岗位UNKNOWN/PENDING无市场actor根/钱包写入；持款但命令缺失不误报ready；101条同时间戳分页不漏项/过滤其他owner；真实Spring条件注册原FINISH handler。岗位policy持久和native身份仍夹具，不能称完整真实Provider/Runtime/用户验收已完成。
- 下一动作：单轨撤除旧POST /personas/bindings/{bindingId}/repair及SUSPENDING→completeUnbind绕过最终cleanup的链，处理无生产调用的旧unbind方法，保留真正仍被使用的公共身份/目录工具；沿当前Web源码无该repair消费者的结果，不默认修改Web。随后继续同实例重邀、自托管收费/控制、已有技能首费/月费核验、其余调度迁移和完整上线验收。不可将105项或平台知识计费已完成缩成整个目标完成。

## 2026-11-10 旧直接解绑旁路单轨撤除（实施中）
- 上轮105项及layering已PASS，本轮基线1ef7fffc36424584cc697750202fe76bb7474e2f，API工作区干净，无在途进程；属于实际进展后的接续。
- 删除旧repair HTTP映射、旧PersonaProvisioningService.repair/unbind及HostedBindingTransaction.resumeRepair/prepareUnbind/completeUnbind和仅为旧解绑服务的私有清空/发布helper；同步移除其不再使用的task/event依赖，不保留兼容转发或隐藏执行入口。
- 调用链核对：新DELETE bind已走租费remove/stopRenewal；此改后当前Agent service源码调用clearBindingAfterUnbind/suspendForBinding的唯一最终释放链为HostingRentHandoverCompletion。共享AgentHostedRuntimePublicationWorker仍被AgentServiceImpl用于正常发布，保留它及原事务/隔离回归，不顺手删除公共工具。
- 删除10个旧直接解绑/恢复执行测试及1个旧repair服务用例（被测方法本身退役），保留其余有效身份、分区、代次与公共发布测试；增加真实MockMvc验证旧HTTP路由404且无业务调用、内部旧执行方法不存在。新移除租约要求与scope校验原测试保留。加入HostedBindingTransactionTest到既有定向source set，覆盖仍使用的公共规则。
- 历史接口库存保留原基线条目，只增当前退役说明；当前Web源码无该repair消费者，不改Web。源码、验证与上线分开，未发布/迁移。

- 旧直接解绑旁路验证终态已核验：`hosting-legacy-unbind-removal-1/result.json`，API `3a45b4fcdca74904191a94970ad6d8e7fd6c8e69` / tree `93282ae9388f71e33262b1801cb5a678b06e734a`，72项全部通过，0失败/错误/跳过，包含validateLayering，受限158.155s；publishable=false，未发布。完整目标仍未完成，同实例重邀等剩余项保持原记录，不将本轮验证扩大为完整上线验收。
- 用户再次明确公共知识提取模型费用由平台承担；既有beta-wen-billing.md第453条已覆盖：独立平台成本记账、实际usage/模型单价、Agent/批次关联、缺证据待核算，不扣用户余额/预占、不计原事项结算。本次确认不改变原事项费用归属，不重复新增计费路径。

## 2026-11-10 同实例再次邀请：公共投影保留与真实身份约束
- 上轮已完成72项验证终态核验（有效进展）。本轮API基线3a45b4fcdca74904191a94970ad6d8e7fd6c8e69，工作区原干净；只改本任务路径，不发布。
- 实际发现最终释放仍复用旧clearBindingAfterUnbind SQL，将client_id/persona_code/persona_name一并置空，丢掉公共实例所属客户端及人设关联。修正为仅清空私有owner/binding、endpoint/token和当前事项/错误投影，保留公共实例关联；原精确关系CAS不变。新增真实MySQL/生产Mapper验证保留、私有清空、重复及旧关系迟到不能清新关系，尚待验证。
- 不直接改写identity owner来冒充同实例再邀请：当前agent_identity_registry的canonical全局唯一，owner/client/binding写明immutable，alias复合外键引用原scope；旧任务读取允许已激活的SUSPENDED/RETIRED身份。需要把长期公共实例身份与历次私有关系身份职责在原身份边界收口，保留原任务/会话授权事实，不能粗暴UPDATE旧owner或取消唯一约束。此为已读源码的真实依赖，不是新业务澄清。
- 同实例链仍有明确未完成项：quote无active binding生成新agt_、bind始终插入runtime；Runtime INITIAL拒绝已存在subject、prepare重放从当前subject取manifest，不能简单覆盖subject；退休skill journal不能直接bindSession。后续要保持原操作历史结果、清理完成事实及新私有凭据准入，不能仅解除retirement检查。当前小修仅避免销毁公共投影，不宣称这些问题已修完。
- 公共投影保留验证已完成：API `94038eab52c6eb1fb89733f839dff47544254001` / tree `cc20d7a6eaa10d9c8509bcb42e8a1e61558ea869`，`hosting-public-projection-1` 11项全部通过（2项真实MySQL生产Mapper + 9项既有释放事务），validateLayering通过，墙钟119.624s。逐份XML及result已核对，无失败/跳过，未发布。本轮没有修改既有身份唯一约束或绕过Runtime退休保护。
- 下一实现依赖进一步核实：agent-identity-schema.sql不仅注释，还包含owner/client/binding不可改的真实TRIGGER；AgentSchemaInitializer同时维护canonical唯一索引；alias仅以含registry ID的复合外键引用registry。不得只改Service或在测试里省略这些约束后宣称重邀可用。13处当前Agent service的findExactByCanonicalInScope调用及历史requirePersistedCanonicalAgentIdInScope需要区分当前邀请与历史读权限；原生安装/会话/技能仍必须绑定新的私有关系，旧历史不可改归属。

## 2026-11-10 同实例历次关系身份基础（实施中）
- 上轮公共投影保留11项通过，API基线94038eab52；本轮实现registry保留历次不可变关系，canonical仍为公共Agent，不更新旧owner/binding。生成live_agent_id只对PROVISIONED/ACTIVE占位；当前关系DAO与已激活历史读DAO分开，历史读保留原scope且不能注册执行。
- 同步fresh schema、AgentSchemaInitializer、既有identity升级SQL和独立受控agent-identity-reinvitation-v1.sql。迁移为同一ALTER加新保护/去掉旧全历史唯一，不删除旧行/别名/触发器；生产未操作。独立脚本无旧索引时不重复ALTER，最终结构仍由现有initializer核验。
- 新增真实MySQL生产Mapper/Service测试：不同owner与同owner再次邀请，旧历史可读但不能注册、未激活新邀请不遮蔽历史、live唯一拒绝第二条、原不可变触发器拒绝owner改写；真实聚焦迁移重入保持原行与alias。测试直接配置授权关系是身份层夹具，不宣称前端报价/收尾/Runtime全链打通。
- 必须补齐实际报价/确认对清理完成资格的准入、公共runtime复用、Runtime原operation结果不可改写和fresh私有凭据；当前candidate只改身份基础，不能发布。
- 身份基础首轮`hosting-identity-history-1` 80项77通过/3失败；三个真实DB用例均在建表夹具阶段失败，原因是手写substring误把SQL COMMENT字符串内部的分号当语句末尾（tenant注释），尚未执行新业务断言；其余18身份、50schema、9收尾事务通过，layering因测试失败未执行。修正只截取已知生产CREATE TABLE的行末`;\n`，保留完整DDL和真实触发器，不放松断言。
- 固定源码运行期间完成只读消费者核对：roster/scene/binding投影都通过binding_id关联历史身份，不会因新关系重复；发现外部服务授权的AgentExternalServicePolicyMapper.identity仅按canonical查询，会在多次邀请后返回多行。修正为查询PROVISIONED/ACTIVE当前关系，加入同一真实DB跨owner测试验证返回新关系，保留服务业务权限判断；不修改无影响消费者。
- 本轮身份基础修正验证PASS：API `fb011f3c31ba6190380f343bdc157ba69ed844d3` / tree `ff8fe8a7f3a4e2d8a07ae9bd192c701e9cd390cf`，`hosting-identity-history-2` **80/80，0失败/错误/跳过，validateLayering通过**；墙钟103.788s。逐份XML/result已核验。首轮FAIL保留，当前API干净，无在途验证；未发布/生产迁移。
- 已验证真实MySQL历次关系不可变、当前/历史查询分离、live唯一、原owner读资格、新owner未激活无历史读资格、外部服务当前身份不会多行、真实迁移重入/原alias及触发器保留。该fixture直接创建授权binding，不证明报价→确认→清理→Runtime重邀全链完成。
- 下一条动作：基于已保留的runtime客户端/人设关联，实现报价与确认复用同一公共Agent、通过economy既有API核对最后完成的handover，旧清理未完成不报价预占；新binding/registry对应新私有关系，不再INSERT重复公共runtime。随后Runtime保留旧operation结果，允许仅CLEANED后的新INITIAL，原subject根与公共包保留、换新私有身份；不能覆盖旧manifest导致历史回放指向新身份。native安装表仅installation_id唯一，canonical有普通状态索引，不需为重复canonical改安装表。
- 源码消费者核对：AgentRuntime/Scene/PersonaBinding以binding_id关联身份；EconomyReadOnlyPreview当前ownership也显式过滤可用lifecycle及active binding，未发现需本轮改动。TaskAssigneeAuthority历史分支使用已激活历史读、当前执行仍核对grant绑定ID及owner；外部assignedTarget仍比对原grant binding，不将旧授权转给新邀请。

## 2026-11-10 同实例报价与确认接线（实施中）
- 本轮从fb011f3c31干净工作区接续，上一轮80项和layering已通过。以persona原锁为入口；仅无当前binding时锁定当前scope/persona公共runtime（最多两行发现歧义，不猜历史实例）。公共投影仍有owner/binding则拒绝，不调用费用域。
- 费用域新增内部completedHandover查询：必须是该Agent最新CLOSED租约、已持久停止事实、原INITIAL已成功且未退款、原installation与保留runtime一致；只读、不扣费、不触发Provider。API不新增economy mapper依赖或跨层G1例外。
- 报价复用该公共Agent ID；确认重新核对同一个公开实例与完成事实，旧报价试图新建另一个ID则拒绝。预占、新binding、新registry及原runtime的空关系CAS在原事务中完成；旧关系记录及公共实例不覆盖，不再INSERT第二个runtime。CAS失败全部回滚；恢复信号仍沿原afterCommit，尚未迁移统一持久调度。
- 新增6项应用事务用例及2项真实MySQL生产Mapper/经济域用例，覆盖重邀报价不动钱、确认复用、收尾未成拒绝、旧报价不换实例、CAS失败回滚、公共数据保留/旧释放不清新关系及最新租约/原installation闭环。验证尚未执行；这些不是实际Runtime重邀验收，Runtime当前仍拒绝已有subject的新INITIAL。
- 重邀准入首轮hosting-reinvite-admission-1：50项48通过/2失败，5项真实MySQL、18项身份、9项收尾事务均通过。失败为两项新quote用例的plan夹具漏amountWen/periodSeconds/status，在原plan一致性检查拆箱时NPE；补齐与原配置一致的套餐字段，不改生产校验/金额、不放松断言。首轮真实失败保留，layering未执行，修正后继续同矩阵。
- 重邀准入修正验证已PASS：API `a41e909a877936ad866a2bd2966f7b9ed6f7866f` / tree `b01bffa774c1ed124c0eec61dd3073f0b5c03875`，`hosting-reinvite-admission-2` **50/50，0失败/错误/跳过，validateLayering通过**，墙钟72.586s。逐份XML/result核验：18应用事务、18身份、9收尾、5真实MySQL。首轮失败保留；未合入/发布/生产迁移。
- 下一动作转到Runtime同根新关系准入，当前源码未动。已核实subjectKey仅由tenant/client/canonical组成，故保留Agent ID即可保留同一home/work/state根；不能新建owner目录冒充复用。HostingControl现在operations共用subject.manifest/initialAssociation，重邀不能直接覆盖它导致旧prepare/ensure回放换成新身份；需要保存每次原操作的确定manifest/关系事实。RuntimeHost.ensureAgent现在拒绝manifest变化且handover阻止initialize，必须通过已确认CLEANED且无旧executor的显式新关系准入，不能直接删handover或绕过quiesce。SkillInstallManager仍需只在该准入后解除退休标记，公共包不重新安装。
- 主机API/Runtime均有显式tenant/client/owner准入配置；多用户实际验收须使用获授权且两端都配置的用户，不擅自删除allowlist或扩大生产授权。该配置事实不是当前API报价功能通过即代表可跨任意用户运行。

## 2026-11-10 Runtime公共技能的新关系准入基础
- 上个仅确认平台费用归属的回合未产生实现进展；本轮重新核对Runtime真实HEAD/脏路径，继续同实例新关系准入。遵循CYF现行本地构建、普通磁盘、RB-1与interface-standard v1.4，不操作外部仓库无关脏文件。
- Runtime提交 `d5c95279c39937a3bc3ff7ed2c4b9f7cea3274e4` / tree `2af0808c5c12eeba7923493597a07b4af69bd05b`，bridge1.1.65 / runtime1.3.87（仅源码版本，未发布）。SkillInstallManager新增仅供可信Host调用的admitRetiredRelationship：原退休operation/身份摘要精确匹配、同公共tenant/client/Agent、新installation、无活动session；原writer lock与串行队列内完成残留清理并原子保存新身份/摘要回执，公共包不重装。普通bindSession仍拒绝退休状态，未新增wire开关或绕过鉴权。
- 新身份成功落盘后精确重试只读回执，不再清理新commands/fences；旧retire迟到不能清新身份，后一轮retirement不能被上一轮admission复活。测试包括实际公共包/技能bytes不变、无额外下载、跨owner与同owner再邀请、重启及提交后中断、旧session拒绝、新session绑定、跨公共scope拒绝、新命令留存与后继退休。
- 验证 `skill-readmission-1/result.json` 与test.log：固定上述源码，Node24.22.1，skill-install-manager完整文件 **112/112，0失败/取消/跳过**，受限116.583秒，普通磁盘TMPDIR；未运行应用/Provider调用或扣费。最初driver用系统Python3.6不支持text参数，在Node启动前失败，已记录并改明确Python3.11，不伪作测试失败或重置已运行阶段。
- **仍未接入Host/HostingControl，不能据此宣称同实例重邀完成。** 下一步需在原subject生命周期锁下核验完整cleanupComplete，持久化新关系切换并调用此准入，再更新执行引擎注册。已读源码确认engine.addAgent也仅允许closed且相同installation；execution-adapter的known Set会跳过已知subject注册。两处须通过明确新关系准入同步收口，不能移除普通addAgent身份限制或建第二个engine。
- HostingControl当前format1 operations引用当前subject；必须先保留每段关系原manifest/initialAssociation再允许切换，旧prepare/observe回放不能引用新身份，旧ensure/cleanup不能操作新关系。materialize的subject/manifest/profile文件同样要在既有锁与确定过渡记录下恢复，不能简单删除handover。无生产部署/迁移/服务改动，完整目标继续进行。

## 2026-11-10 Runtime历次关系候选回放闭环
- 上轮技能准入已形成源码及112项通过的证据，本轮从真实Runtime HEAD d5c9527接续；无在途测试/生产动作，旧摘要不是当前部署证明。
- Runtime提交 `0df457d62a51eba7e55ff0956235e46563a068a3` / tree `9d9289a8d41a351f234469e211fc0f4a5c4d731f`，Runtime源码1.3.88。HostingControl私有journal升为format2：每个operation持有原manifest、原INITIAL关系、enrollment摘要/到期的确定快照；不额外复制旧secret/template。prepare与observe回放取原candidate，不能随当前公共subject换关系而改写原身份。旧installation的ensure/quiesce/evidence/cleanup拒绝为SUPERSEDED，observe仍返回原候选UNKNOWN，不访问新executor。
- format1只在既有control writer lock内单次迁移，严格检查旧operation字段、引用及新结构的原有一致性约束，验证成功后原子落盘；无效旧journal保持原bytes，不补猜未知事实或调用enroll。不新增第二种wire合同，外部hosting-v1不变。关系按installation分组验证连续generation、原INITIAL、同候选；当前subject仍只能指向当前关系操作，按分组查找避免为每个subject重新扫全部操作。
- 新增持久迁移/重启不重复改写、非法旧journal不写入、公共subject换关系后原prepare/observe不变及旧4个修改入口被拒绝用例。最后一项直接设置存储夹具，只证明回放边界，不代表真实CLEANED→新关系已完成。
- `hosting-candidate-history-1`首轮43项41通过/2失败；两项真实UDS夹具的临时路径超过Unix socket地址限制（批次路径过长），不是业务失败。保留日志；仅将该任务TMPDIR改为普通磁盘 `/home/isp/state/cyf-local-build/hch-*` 的短根，stat确认非tmpfs/ramfs，结束后只删本轮精确temp根，不改源码、不删测试。
- 同一固定源码 `hosting-candidate-history-2`：**43/43通过，0失败/取消/跳过**，两轮受限共13.703秒（首轮6.964秒+本轮6.739秒），含hosting-control与hosting-lifecycle整文件、实际UDS互通/权限 fixture和成熟engine生命周期 fixture；尚非生产/全链重邀验收，无发布。
- 下一条实际动作：RuntimeHost增加在原writer/lifecycle锁下的CLEANED后新关系切换；对subject.json/manifest/skill身份/引擎闭合注册/handover采用一个可恢复的确定过渡，原manifest→新manifest不能靠删handover强行启动。随后HostingControl新INITIAL接入。仍未接入前轮admitRetiredRelationship，不能把这两项基础宣称完整功能；其他原列出的统一调度、自托管/月费审计、验收/发布剩余项不变。

## 2026-11-10 技能身份与成熟执行引擎新关系准入接线
- 上轮43项通过及immutable candidate是真实进展。本轮重新读取HEAD 0df457d和真实adapter/engine，纠正先前静态调查中的不完整结论：adapter.close第325行已清除known，所以不是“永远跳过注册”；不为此重复修改缓存逻辑。真实阻断是engine.addAgent只允许旧installation、skill retirement不能普通绑定新关系。
- Runtime `d940b111fd9828befd7e7d81ece4e4a96afb697d` / tree `62b01dc00a55e8b6daddd8881086ce327c267963`，Runtime1.3.89 / bridge1.1.66，未发布。成熟engine复用同一注册实现，新增仅trusted host可调用admitAgent：原entry必须已closed/无state、原manifest精确匹配、同state/HOME/work/profile；普通addAgent仍不得换installation。重启无旧entry时仍核对公共tenant/client/Agent及新installation；不会创建第二个engine或先启动进程。相同新candidate尚未创建executor的重复准入无副作用，活动执行器不能再次准入。
- execution-adapter新增admitRelationship接线，调用真实SkillInstallManager的原retirement摘要准入，再向同一engine注册新manifest，标记known以让后续createExecutor使用新entry。不触发enroll/session/socket/model；attached的旧/新执行器存在即拒绝。该方法只供后续RuntimeHost持久CLEANED→新关系过渡调用，不作为wire/工具开关，当前尚未由Host调用。
- 新增三项真实模块测试：成熟engine同根旧关闭→新身份/活动与普通add拒绝/旧state处置/peer不受影响；重启无旧engineentry；真实adapter+真实skilljournal retirement→新identity→真实engine注册精确重试，证明后续createExecutor不会退回普通add；socket/session调用均显式禁止。旧测试仍完整运行。
- `engine-readmission-1/result.json` / test.log：**46/46通过，0失败/取消/跳过**，受限8.443秒，普通磁盘短TMPDIR已按精确路径回收，无生产安装/重启/迁移/实际扣费或模型调用。当前两份hosting完整文件通过不扩大为全部bridge测试/完整上线验收。
- 下一步剩余且必须做：RuntimeHost在既有subject writer/lifecycle锁内持久化CLEANED→新manifest切换，恢复中不能重启旧执行器；同一过渡调用adapters.admitRelationship并更新subject.json/manifest/profile，最后安全终结旧handover，随后HostingControl新INITIAL才可放开。前两轮与本轮没有提前放开新INITIAL，因而未产生“缺清理即可换用户”的半启用链路。其他统一调度、自托管、计费审计、端到端验收和发布剩余保持原范围。

## 2026-11-10 RuntimeHost同根关系切换与中断恢复
- 上轮真实engine/skill接线46项已通过。本轮从d940b11核对后继续，不修改无关脏路径、不部署；增加Host边界并将adapters.admitRelationship传入真实runUnifiedRuntime，未提前放开HostingControl新INITIAL。
- Runtime候选 `ecb2d9c75417a0ab210126e31708613549f44d83` 验证49项通过；随后自检补强实际stateRoot/profile对照与已关闭新engineentry的精确恢复，当前 `fcd1a88d96ee44c346c2e16225162fb933b9c629` / tree `16f6307d460aac61a08de82e3213478bad748d8a`，Runtime1.3.90 / bridge1.1.67。没有把前一批验证冒充后一源码。
- RuntimeHost.readmitAgent只接受可信control生成的同公共subject、同profile/roots、新installation和原CLEANED事实；原handover/lease/owner与cleanupComplete必须精确匹配。原subject lifecycle gate及writer lock内持久化relationship-admission.json PREPARED→materialize→真实adapter技能/引擎准入→COMMITTED→只删除已核对的旧handover→初始化新执行器；不enroll/打开会话/调用模型。旧锁inode与公共项目文件保留，原关系迟到不能清新关系。
- initializeAgent读取过渡记录：PREPARED、仍有旧handover或旧manifest均只保持QUIESCED，重启不能偷偷恢复原执行。COMMITTED回执保留原清理事实，允许完成删除旧标记前后的精确恢复；其他operation/关系不能认领这个过渡。下一次真实private-state cleanup会按原边界删除该旧过渡回执，不能在新关系尚活动时复用旧邀请。
- 自检发现仅比较调用方previous/new roots仍不足：现有state的实际root/profile也必须精确相同，已补并测试避免沿旧writer锁操作另一个root。发现新engine初始化失败会关闭新entry，Host重试需允许“同admittedFrom+同新agent且已closed无state”再次注册；保留活动执行器拒绝与普通add不能换installation。
- `host-readmission-2/result.json` / test.log：**50/50通过，0失败/取消/跳过**，受限9.028秒；前一源码49项8.980秒记录独立保留。普通磁盘短temp已精确回收。新用例覆盖原关系/实际root错配拒绝、同writer inode/public文件保留、原executor确实关闭、新identity初始化、原请求迟到、PREPARED重启、COMMITTED旧marker还在与已删除两种恢复、旧manifest启动阻断。Host层materialize/cleanup/adapter使用职责夹具；真实adapter+manager+engine用例单独存在，尚非全链同实例重邀。
- 下一动作已收敛为HostingControl：新INITIAL在原CLEANED证明后才生成新候选，保留旧candidate回放并保存原候选引用/清理关系；runOperation用host.readmitAgent与同根manifest/subject/profile精确可重入materialize，保持原公开template/config而换新私有授权。旧subject之前的运行job须先确认退出，不能让其覆盖新relation。随后执行实际控制prepare→ensure→新session与再次重启/连续第三次邀请回归；API/Runtime跨组件及调度/月费审计/上线剩余保持原范围。

## 2026-11-10 同实例真实控制入口接线与连续邀请回归
- 上轮Host切换/恢复50项通过是真实进展。本轮实际HEAD fcd1a88接续，将HostingControl INITIAL→readmitAgent→materialize接通，不再停留于未调用helper。
- Runtime先提交908f7c0（51项通过），再补部分materialize中断恢复，当前 `298642f5b194080d294b2aadb25e2c41f4014614` / tree `33142726317a350770bf036ca2d99e8b0c57717f`，Runtime1.3.91 / bridge1.1.67，未部署。新INITIAL遇到已有公共subject时读取原完整CLEANED/lease/owner证明，必要时仅恢复已清理subject的writer锁，不启动旧执行器；原host gate复核无executor并等待旧job退出后才生成新候选。
- 新subject保留同公开template/config/roots，生成新installation/enrollmentSecret；仅存previousOperationKey/handoverId用于过渡，原candidate完整回放不改。ensure在原Host持久过渡内按精确旧或新manifest恢复subject.json/manifest，profile/config仍必须相同；调用真实admitRelationship接口后去掉过渡引用，再走原native授权加载/一次enroll/activate，不复用旧私人凭据。普通REPROVISION与原scope allowlist保持不变。
- 新增连续第一→第二（不同owner）→第三（原owner再次邀请）的控制链测试：真实HostingControl+RuntimeHost+cleanStoppedPrivateData，包括CLEANED之前拒绝、实际删除原auth.json/native authorization、公共.git历史bytes不变、同state/HOME/work/profile、旧prepare回放及旧cleanup迟到、cleanup后重启、prepare后重启、正常重启不再enroll、每次新私有installation且只调用一次enroll。业务scope仅在合成fixture显式授权第二owner，未改生产allowlist。
- 新增实际manifest已写新而admitRelationship中断的回归：PREPARED留下、旧executor未重建、未新增enroll；重启从同一过渡恢复，最终新identity READY且仅补一次enroll，旧candidate不变。
- `control-readmission-2/result.json` / test.log **52/52通过，0失败/取消/跳过**，9.935秒受限；前一源码51项10.213秒独立保留。磁盘短temp已精准回收。上述控制链的native API/执行器和模型响应为合成fixture，admitRelationship在该控制链中使用stub；前轮真实adapter+技能journal+engine单独有测试，不能据此宣称API→Runtime→真实管理技能全链或生产验收完成。
- 下一验收缺口：以真实adapter/engine/skill journal结合控制链，验证保留公共技能在新owner首次账单与后续管理消息正常使用；再补API/MySQL原租约关闭→新报价预占→同实例原生注册/身份授权的跨边界回归。仍需审计自托管50文、已有技能首次及月费、剩余独立@Scheduled迁入统一task、disabled-owner原证据边界、Web真实验收、打包/受控发布/生产迁移。完整目标继续，不将本轮52项替代完整上线验收。

## 2026-11-10 真实控制/执行器/技能闭环揭示并修复公共仓库遗漏
- 上轮控制fixture52项为真实进展，但admitRelationship stub仍是覆盖缺口。本轮新增hosting-readmission-integration.test.mjs，组合真实HostingControl、RuntimeHost、execution-adapter、成熟engine、技能journal和真实清理器；仅HTTP/WS服务端回执/模型响应使用合成数据，未调用线上API/Provider。loadEngine仅捕获真实executor供断言，不替换内部实现。
- 第一轮 `07749a64e8dede362cd838674ba3e56d9616c7fd` / `real-engine-readmission-1` 真实失败，4.223秒：新关系已READY且保留技能身份/bytes通过，但公共work/.git/history丢失。原因是adapter只把workspace policy的repository/root作为公共根；未配置policy的托管codexWorkdir被材料清理器当私有根。前轮控制fixture显式传入公共work根，未覆盖此实际接线，不能将之前PASS当作公共仓库完整验收。
- 修复责任层为真实execution-adapter公共/私有根分类：codexWorkdir作为公共项目根明确传给现有清理器，再并入已配置policy根去重；不扫描Git、不改写历史、不把独立chat/attachments/image/typed私有根转为公共，不新增框架或另一份删除实现。已有HOME/state/公共根重叠保护保留。
- 当前Runtime `b970258db0e641318bc201f068c66ac5efb002a0` / tree `edb825ff833b5d067b10f4d68970e3515f61b185`，Runtime1.3.92 / bridge1.1.67，未发布。`real-engine-readmission-2` PASS，真实回归4.531秒：原会话安装/activate实际instruction包、ACK原结果、原证据drain、技能退休及私有清理、新owner鲜活enroll/session/registration、真实新engine绑定原包、通过WS新关系READ管理指令返回原target；公共.git/技能bytes不变，一次下载、两次enroll、原state disposed且旧session为null。
- 同一当前源码补跑受影响5份hosting/cleanup单元fixture文件 `public-work-cleanup-unit-1` 全部通过，受限14.452秒；真实跨模块回归另记，不伪作单测或线上验收。原失败日志保留，不删除测试或放松公共仓库断言。磁盘短TMPDIR精确回收，无服务/生产目录变化。
- 下一项API/MySQL联动仍未验收：当前API工作区干净且HEAD仍a41e909a877936ad866a2bd2966f7b9ed6f7866f，未把Runtime通过冒充新租约账单/注册权限通过。已再次定位剩余独立调度：HostingRentReconciler5s、SkillInstallRecoveryService5s、AgentStatusMonitor10s、旧JobExecutor分钟扫描；应用afterCommit仍只是wake而非同事务持久schedule。应按统一task要求接入并保留原幂等/租约，不能宣称统一调度已全部完成。其余自托管、首次保留技能/月费、disabled-owner原证据、前端/上线验收保持原范围。

## 2026-11-10 托管开通/重建迁入持久调度及资金原子性验证
- API `f07a086349106eddb6b6892c292a96a030dcbca3` / tree `54877d754f3c9c87fdba41d9dbcfcbc5a9436e2e`：HostingRentReconciler实现ScheduledJobHandler，撤除5秒@Scheduled与内存wake；INITIAL/REPROVISION在原业务事务内按intent/request键登记。启动只做一次按分区/主键分页补登记，回调精确取单条业务，UNKNOWN交给统一调度重试；provider I/O保持事务外，既有资金/身份/结果逻辑不变。统一调度开关与迁移必须随候选启用，不能新旧writer混跑。
- `hosting-provision-scheduling-1`原result为FAIL但Gradle实际exit0：40项全部通过、validateLayering通过，受限105.639s。真实原因是task-local driver照搬上一批4报告/50项断言，实际selector为3报告/40项。保留原FAIL/result/log，不为计数重建；逐份XML名称/数量/失败/跳过及layering事件另行核验并绑定摘要，见同目录verification-audit.json。此次核验只证明40项定向范围，不改写原批次结果或宣称可发布。
- 当前新增真实MySQL三项：500文预占+原reconciler.signal+实际ScheduledWorkStore/Mapper提交及重复；signal后caller失败全回滚；缺调度表时不留下已预占资金。复用原HostingRentRenewalMySqlTest临时数据库，不碰生产、不实际调用Provider；它证明资金/调度共同事务，不替代API HTTP→Runtime注册全链。
- API `a86109d405`固定源码验证启动：hosting-provision-scheduling-mysql-1，selector为原40项加initialProvision*三项；日志/结果位于既有任务证据根，尚待终态。单元/编译等受限、真实MySQL时间单记，未发布。
- 接续只读核实：剩余调度不止Agent的SkillInstallRecoveryService/AgentStatusMonitor和旧JobExecutor。MemoryJobHandler亦有实际@Scheduled入口；旧JobExecutor扫描仅日志，不能删除扫描后就宣称cron执行已实现，也不能将旧getCron全部自动启用。完整cron发生点/错过策略、节点本地连接归属仍按task规格处理，旧清单不是完成证明。
- 上述MySQL批次终态已核验：API `a86109d4050da9b916a18b992c8935e3b6b2035d` / tree `aee7fb45899597da065d8fe544a9f893b943ccb0`，43/43、0失败/错误/跳过、validateLayering通过。墙钟91.153s，真实MySQL16.249s，受限74.901s。每份XML及三个initialProvision用例名称已回读；当前无在途构建。原stale-count FAIL保留，没有重复同源码构建。
- 费用源码审计明确缺口：HostingRentApplicationService当前仍只允许mode=server；HostingRentLedgerServiceImpl.quote金额只取plan.amountWen，reserve将同一金额写入lease。未读取首期保留技能清单，也未区分首期总价与后续租费；因此不能通过临时把plan设成“500+技能数×50”补齐，否则后续每30天会重复收已有技能首费。下一费用改动必须在原quote/lease责任层分别固定首期清单/总价和周期基础租费，同步SQL/实体/接口及真实MySQL；不能由Web补算或写临时兼容。
- 已确认现行合同的技能费为新安装50/升级20一次操作费，首次/重邀已安装清单×50为首期附加，后续正常租费；不是每月重复收技能安装费。自托管50文/30天及存量30天过渡仍需真正接通，不能用renewal fixture的50文金额冒充自行部署入口已实现。
- 技能恢复迁移调用链已核实：SkillInstallCommandWriter的write/writeManagement是事务内原delivery/outbox生产边界，宜在此原子登记；SkillInstallRecoveryService当前仍5秒扫描。新调度需按delivery精确读、依据原next_retry_at/lease_until/更新间隔重排，保留原wire/claim CAS，终态无需持续扫；启动补登记需要覆盖将来到期/被租用行并用主键分页，不能复用旧只取due前25条的SQL造成漏单/空转。受影响构造与回归包括SkillManagementTransactionTest、SkillInstallTransportMySqlTest、SkillMarketplaceRealTransactionTest及SkillInstallRecoveryServiceTest。当前本节仅分析，尚未修改技能调度代码。

## 2026-11-10 技能原命令逐条调度迁移（在途验证，未发布）
- 上轮43项真实资金/调度联合验证为实际进展；本轮从干净API a86109d405接续，实现SkillInstallCommandWriter.writeManagement原delivery/outbox事务内登记，Recovery改ScheduledJobHandler，撤除5秒扫描。查询按单delivery定位原未完成command/当前skillRevision，保持原wire、权限、租约及CAS；启动补登记采用包含将来重试/活跃租约的主键分页，不拿旧due LIMIT25当全量恢复。
- nextAttempt复用原next_retry_at、lease_until和60秒更新间隔。真实独立outbox租约也必须返回其到期时间，否则单delivery新调度会在delivery已到期/outbox未到期时立即循环；已加入该延期路径及用例，不新设任意时限。
- 真实SkillManagementTransactionTest已接实际task schema/mapper/store，并补订单资金+调度提交、外层回滚、调度SQL失败全回滚；旧市场夹具只调整构造/调用保持原语义，不能当统一调度集成证据。shared fixture被chat测试编译，因此仅补其实际测试依赖，不修改Web。
- 固定API 61033d3632（完整SHA以skill-delivery-scheduling-1/result.json为准），正运行13项恢复单测+81项实际MySQL技能事务/资金/原wire回归及layering，当前session93192，终态前不改受测源码。未安装/迁移生产。
- 核对实际消费者发现必补的多容器问题：AgentManagedSessionLookup/SkillManagedSessionAdapter只访问本节点WebSocket；不能把此handler留作target_node为空的集群owner任务，否则owner不持有连接时会反复离线。当前候选尚未解决，禁止发布。后续在已存在的“注册成功且会话ready”边界按Agent补登记到本节点，writer登记本node，回调不持有本机ready会话时结束当前节点待办；重连到新节点沿真实注册边界重新登记。保留原delivery租约确保跨节点移交不抢发送，不引入跨容器转发框架或所有节点周期扫描。既有AgentCommandReconnectSignal为有损内存队列且专属旧命令，不能拿它冒充本次可靠登记。
- skill-delivery-scheduling-1终态FAIL：94项中93通过，唯一失败为新增回滚fixture将install()（包含package.describe文件准备）整个包在外层事务，命中既有SKILL_PACKAGE_PREPARE_IN_TRANSACTION；并非实际调度/账务失败。受限96.112s、真实MySQL277.293s，墙钟373.405s，layering未执行。修正为在原writer真实writeManagement/调度写入之后注入失败，install准备仍在事务外，严格核对回滚及故障原因，不删除该用例。
- 本轮顺带收口已发现的节点职责：新增仅内部调用的AgentSessionReadyListener，在真实WS已认证/回执交付/本机目录ready后同步登记；失败撤销注册并关闭连接，强制重连重试，不吞可靠登记失败。技能writer及恢复键指定配置node-id，无本机会话的旧节点待办结束；新节点真实注册按该Agent分页登记原pending命令。原delivery/outbox租约不改变，跨节点不会抢原claim；不新增跨容器转发器。删除全Agent启动扫描，启动后持久任务或实际重连边界恢复；全局集群任务不能代替本地WS归属。
- 失败矩阵：前一批93项成功；唯一failed-input为测试中事务边界错误，修复后输入有实质变化；节点归属修复另有真实MySQL移交、无本地socket终止、错node拒绝、WS回执失败/登记失败关闭回归。既有ledger把历史失败累计到blocked_root_cause，沿authorize-remediation提交本矩阵，不绕过锁、不原样盲重试。
- 节点修正候选已提交：API `ffb8caaa5505d7e718102ff115e3f088993373c8` / tree `c9e8c386511d1030dd388a03cde0a17578c5e4ea`。`skill-delivery-scheduling-2`正在跑97项技能恢复/实际MySQL及16项真实WS handler夹具，session54111；它不是外部真实Runtime线上注册验收。固定源码运行期间未改API。
- 当前节点合同：key.targetNode来自`cyf.task.scheduling.node-id`，不来自HTTP/模型；writer与统一runner使用同一配置。注册完成后的内部listener按可信tenant/client/Agent分页查询旧pending并持久signal，无网络/模型调用；注册未成功不登记。listener写库失败时撤销会话并关闭当前socket，避免“已收到注册回执但永远没有恢复信号”。回调缺本机ready socket直接结束该节点待办，新节点连接重新登记；原command/outbox内容、资金、private identity和claim/CAS保持原样。
- 剩余系统任务清单不能缩成三个类：只读源码还发现RecommendationUsageJournal、ChatBountyAssetRelay、ChatBountyExecutionRelay、NativeConversationWorkNotifier、ArchiveQuestionWorker的业务轮询，以及AgentOutboxRelayScheduler、AgentCommandReissueCoordinator、AgentTaskEventReplayServiceImpl。需按当前启用状态和职责逐项接入/退役；执行租约、SSE/语音/连接心跳属于本机执行归属，不能直接改成集群唯一业务任务。MemoryJobHandler、AgentStatusMonitor、JobExecutor旧cron也仍待处理。此为实际范围审计，不宣称已改这些类。
- 接续核验session54111已终止，skill-delivery-scheduling-2实际FAIL，不可发布：chat定向测试编译无法解析SkillExecutionFixtures（详见原gradle.log）；未取得完整113项及layering通过证据。墙钟806.209s，真实MySQL回归568.003s，受限238.206s，未触及600s受限预算。保留原result.json/日志；下一步定位chat测试source set/fixture编译依赖后再验证，不原样重试、不因墙钟超过10分钟归因为预算超限。
- 用户再次明确公共知识提取模型费由平台承担；现行beta-wen-billing.md第453行已有该合同，无需重复建立收费规则。执行边界仍为平台实际成本记账（Agent/提取批次关联），不扣用户余额、不占事项预占、不纳入用户验收扣费；生产启用与完整交付状态仍需独立核验。

## 2026-11-10 测试共享夹具修复与剩余调度责任再核对
- 上轮97项技能测试的XML已实际回读：SkillInstallRecoveryServiceTest 15/15、SkillManagementTransactionTest 82/82，均无失败/错误/跳过。但后续chat编译失败，整批保持FAIL，layering未完成。根因为SkillExecutionFixtures实际在src/sharedTest/java，新增source set只包含src/test/java；修复仅补该源码目录，不复制夹具或改变业务断言。
- API候选67c24a3627（完整SHA/tree由skill-delivery-scheduling-3/result.json记录）已提交，重排验证先跑chat注册/auth边界、再97项技能测试与layering；session18036正在执行。源码固定期间只读审计，未改受测API文件。前一失败记录及归因保留，无生产操作。
- 全仓main源码核对补足范围：ChatDeliberationOutboxRelay不仅有本地执行heartbeat，还有业务nextDueAt/恢复scan；只能保留前者，不能把整个类视为连接维护而跳过迁移。ChatBountyBootstrapRelay亦有一次性业务闹钟，仍须接统一调度。WxSchedule每日07:30投票及随机延迟每日一句是实际@Component/@Scheduled，原始清单已列出，后续摘要遗漏不能缩小范围；旧TaskAlert仅元数据，仍不自动启用。
- AgentSceneServiceImpl的worker.schedule(action)为Reactor流处理串行派发，不是到期业务定时器，本轮不机械迁移。ArchiveQuestionWorker须拆分业务250ms候选轮询与在途claim续租，保留后者的执行者归属。AgentStatusMonitor同时处理本机connected集合与数据库超时，不可直接用任意集群owner的本机连接集合判断全局在线状态。
- RecommendationUsageJournal的本地回执故障恢复不能简单替换成“写文件后数据库signal”：其存在目的正是DB故障后保住成本证据。需在节点归属的统一恢复入口保证文件存在但调度SQL未提交/进程重启也能发现，不重发模型、不读取其他节点目录；保留现有原价表/usage/绑定，不能把数据库失败转成再次付费调用。此处为已核实实施约束，尚未接线。
- skill-delivery-scheduling-3中chat两份XML已回读：AgentWebSocketRuntimeAuthenticationTest 7/7、AgentWebSocketSkillExecutionRegistrationTest 9/9均通过，无失败/错误/跳过，确认共享夹具编译修复有效。随后进入真实MySQL技能事务回归，regression-events.jsonl记录start=1794303425.515；整批仍在途、未取得layering/终态，不标113项全通过。当前可继续跟踪同session18036，禁止因观察等待超时重启。
- session18036终态FAIL已回读：skill-delivery-scheduling-3的四份XML合计113/113、0失败/错误/跳过，但validateLayering拒绝SkillInstallRecoveryService的cn.jia.task.scheduling.*通配符跨域引用（G1），不能把测试通过当整批通过。墙钟1735.378s、真实MySQL1251.050s、受限484.328s；真实回归不受600秒限，受限阶段未超限。
- 本轮失败矩阵：上一批为chat未包含共享fixture源码目录，本批该问题已被实际16项通过证实修复；新失败是分层解析不能证明通配符仅引用core/API。候选a81b043df1改成ScheduleKey、ScheduleService、ScheduledInvocation、ScheduledJobHandler四个明确导入，未加例外、未改变测试或业务逻辑。下一定向验证先layering，再15项恢复单测；原113项仍归原67c24a3源码，不将历史报告改标新候选。编排器历史累计失败触发矩阵，按既有authorize-remediation处理，不绕过门禁。
- skill-delivery-scheduling-4终态为预算中断（exit -15 / budgetExceeded=true）：API a81b043df176b3a3ca89c1ed6edbe6b5b49b52e9 / tree e6408cf0e48681dc7f46be37896c18f074e84824，受限601.078s、真实回归0s。监督器在600s触发，仅本次进程组退出，随后核实本次Gradle launcher/daemon PID862915/863136及入口862883均不存在。未做生产操作、未终止其他任务。
- 分层检查已实际通过（97.946s）；剩余编译/15项单测未完成，不能把超时标通过。Gradle根项目配置到projectsEvaluated为307.089s，taskGraphReady318.933s，JVM启动亦有等待。同期只读主机负载40.53/27.50/13.91，另有非本任务dnf进程消耗CPU；可用内存约2965MiB，非内存盘/OOM证据，不干预他人任务。负载竞争为观测到的耗时因素，不能据此声称唯一根因。
- 固定源码受限600秒预算已用完，遵循本会话用户提供AGENTS的同源码累计规则，不通过新批次名重置、变更无关源码或将单测改名回归规避。下一需要用户批准本候选累计上限延至1200秒（额外约600秒），待负载下降复用已验证编译缓存，补15项恢复单测，不重跑113项真实回归；保留分层成功和本轮timeout原证据。整体目标未完成，未标blocked/paused/complete。
- 用户随后明确“允许”额外10分钟验证；仅本候选a81b043df176b3a3ca89c1ed6edbe6b5b49b52e9累计1200秒，已有601.078s，剩余598.922s。skill-delivery-scheduling-5只补15项SkillInstallRecoveryServiceTest；分层复用同源码上一批实际PASS，不重跑113项数据库回归。相关build.gradle摘要与上一批已读取输入逐一比对一致。原超时保留，不扩大为发布授权或其他候选不限时。
- skill-delivery-scheduling-5已终态PASS：15/15恢复单测、0失败/错误/跳过，固定a81b043df176b3a3ca89c1ed6edbe6b5b49b52e9/tree e6408cf0e48681dc7f46be37896c18f074e84824。受限473.315s，和上批累计1074.393s，在用户批准1200s内；墙钟473.319s，真实回归0。已回读唯一XML（SHA256 fcb71d6a95b315ae500e1d47ac805c6300c807c8fc71b0207af2a82d415ad565）及同源码第4批layering事件failed=false/skipped=false；编排器保存可复用证据key=5a6a6968383ccf74e9b8b1aced2c21d387a2e1431c9cf721c52e0339bece2a05。
- 本候选仅将跨域通配符改为明确core/API导入，上一实质逻辑候选67c24a3的113项真实测试通过事实保持原SHA归属。先前两个整批FAIL和timeout不重标；当前无在途验证、API工作区干净。未打包、发布或操作生产数据；全目标仍包括剩余调度/cron、首期技能清单与基础租费分开、自行部署/存量过渡、真实同实例重邀链路、Web及线上验收，不能因本片段验证通过宣布全部完成。
- 下一实现应先闭合剩余统一调度的明确周期/发生点语义：当前ScheduledWork领取会清空dueAt且Claim仅存revision，不能用revision冒充cron时间，也不能启动时signal(now)导致每次重启多执行。需在task责任层持久化发生点/下一期限并同库原子登记；显式注册目标，不自动启用旧TaskAlert。Memory业务同步和ChatDeliberationOutbox业务scan与其本地执行租约分开处理。该段为下一实现约束，尚无新cron源码或迁移。

## 2026-11-10 cron持久发生点基础候选
- 从干净API a81b043df1继续，当前修改限task模块，目标为补缺的cron发生点/错过策略；不把新基础替代全部系统任务迁移。新增内部CronScheduleService、显式定义、同库cron游标DDL/Mapper、CronScheduleDispatcher及条件装配。无额外轮询、无应用自动迁移、无自动启用旧getCron；派发/续费现有行为不变。
- 同一事务创建原发生点的task待办并推进下一闹钟，重启相同定义保留旧游标；显式COALESCE/SKIP分别处理停机错过，原已接受发生点不随取消/改表达式丢弃。节点仍沿既有targetNode；SQL确切tenant/client/handler/node后加锁。
- 增加12项纯单测（包含时区/DST、正常迟到与真错过、原发生点、重复注册、取消、配置/旧handler拒绝），并在原ScheduledWorkStoreMySqlTest复用同一私有MySQL加4项真实原子回滚/并发/重启/取消隔离验证；条件装配测试补CronMapper及无SQL自动执行断言。尚未测试、未提交/发布时不宣称完成；Memory等消费者与慢业务容量未改。
- cron候选已固定并验证：API 6cd01771f1c3aea76ba75a052cb834a091904b2b / tree 75de1f7bfbfe18b61bce95b46e5f29a422ed7d40。cron-scheduling-1终态PASS，三份XML已回读：CronScheduleDispatcherTest12、TaskSchedulingConfigurationTest3、ScheduledWorkStoreMySqlTest24，共39/39、0失败/错误/跳过，validateLayering通过。墙钟371.917s、真实SQL56.047s、受限315.867s。测试涵盖新增4项真实事务/并发发生点；没有实际模型调用，也不是Memory/Wx消费者验收。
- 本轮仅增加cron基础及条件Bean，尚无业务调用register；现行Memory/Wx等旧入口未切换。下一步需实际消费者按进程可信client/节点注册，不得给可跨client的旧全局任务虚构client、仅删除旧扫描就宣称迁移完成。租费首期技能清单/续期基础价、自行部署/存量过渡、disabled-owner原始证据及完整重邀/前端/生产验收仍保持完整范围。
- 本任务两个已终止私有MySQL临时目录cron1和hprovm1已精确回收（合计343601557文件字节）：核对各自driver绑定、PASS、无mysqld进程引用、日志Shutdown complete后保留owned-mysql-retained.log及摘要/cleanup.json到原批次证据根，再删除对应临时目录。未删除生产状态/备份、源码、包或其他任务缓存。磁盘可用约728MiB；非内存盘清理。本次验证session25378已结束，当前API工作区干净，无在途构建。
- 接续核对Memory发现其现行记忆同步/汇总持久化固定tenant=0且遍历多个client，不能为迁移虚构客户client，也不能直接改成任意租户跨库同步。先在task责任层补内部租户维护范围：显式空client仅允许未限制client的进程；外部FixedTenantAdmissionPolicy不变，现有SQL分区在LIMIT/锁之前排除固定client不可见维护行。增补cron准入单测和真实MySQL领取/结算/租户/节点隔离测试。此改动尚待验证，Memory业务消费者仍未迁移；不改变资金/主流程或生产配置。
- 维护范围候选79f545c4e1已固定，cron-maintenance-1/session27509正在验证（layering、cron单测、条件装配、真实MySQL共预期43项），不可提前宣称通过或启动同候选重复验证。未修改生产数据/配置。
- 下一消费者优先RecommendationUsageJournal：其磁盘回执是SQL故障期间的成本证据，不能只靠“写文件后signal”恢复；计划将既有recover的定时触发从@Scheduled移到显式节点绑定cron（本机可信node-id、进程tenant/可选client），复用统一调度重启/DB恢复能力，不再调用模型。存储/原价/usage/ACK删除逻辑保留；调度适配与磁盘记账分开，不能把adapter上线与全任务迁移混称完成。该项仅完成源码审计，尚未实施。
- cron-maintenance-1/session27509已终态PASS：API79f545c4e14dd63d4e78bff413f8bb9899ad6c24/tree ab1d238cdf58ac62cf8c39fb64650d04b7c06c67，43/43及validateLayering通过，真实XML另行回读。墙钟303.386s，受限阶段未超600s；结果及详细时限在原result.json。固定client不能登记/领取/结算租户维护任务，租户/节点隔离真实MySQL通过。无部署，Memory/推荐回执等业务尚未接线。
- 已实现推荐费用回执恢复适配：删除Journal原@Scheduled，新增统一调度enabled条件下的RecommendationUsageRecovery（本机稳定node-id、进程client或显式租户维护、UTC默认每分钟、COALESCE）。ApplicationReady后注册并保留cursor，SQL注册错误传播；前台写回执不依赖新signal，不重发模型。新增注册/客户端/节点/失败单测及实际磁盘失败后经适配恢复原回执测试。沿现有runtimeCapabilityRegression源集增选这两份测试，不新建runner；尚未验证或部署。
- 推荐回执候选已提交API ade61e8324（完整SHA/tree在recommendation-recovery-1/result.json），启动recommendation-recovery-driver-1.py，当前session41393在途；预期13项（Journal9+Recovery4）及layering。这是普通磁盘单测，不将其标作真实DB回归，沿600秒受限预算。下一动作只跟踪本session/result，禁止同候选重复启动或在固定源上改代码。未部署。
- cron-maintenance-1实际时限：受限246.453s、真实SQL56.930s、墙钟303.386s。XML回读43/43（Cron14、Config3、SQL26）；其私有cmaint1/MySQL在确认PASS、Shutdown complete、无进程引用后清除171800787字节，原批次保存owned-mysql-retained.log及owned-mysql-cleanup.json，未碰生产/备份/其他任务目录。
- recommendation-recovery-1/session41393终态FAIL（预算中断）：固定API ade61e83240320eaa4d93e905d135fc8f33788bb/tree b6095ca4216cf7dc0e6999f13e0081eed04f7164，墙钟600.961s，预算600s触发SIGTERM，原状态保持FAIL。layering实际通过58.910s；根项目配置96.784s、taskGraphReady101.948s（相对init），agent-service编译215.029s成功，chat-service编译尚未结束，13项单测无XML，不能宣称通过。没有真实SQL回归，不豁免本批时间。
- 已轮询确认原session终止，核对本批Gradle893697/893607及driver893490无存活；未重启验证、不终止他人任务，无生产操作。诊断线程快照保留gradle-thread-diagnostic.txt；主要已测耗时为依赖编译/配置，并非用量恢复逻辑实际运行。现有task基础43项PASS仍归79f545c4，不冒充当前chat迁移验证。
- 下一动作需本候选额外600秒验证授权（累计1200秒，已用约601秒），复用已完成的同源依赖编译和layering，补chat编译与13项定向单测，保留超时证据。不以改名/无关源码提交重置预算。当前申请是按用户本会话提供AGENTS的固定源码累计条款，不援引旧候选a81的批准。首次遇到此具体候选预算阻碍，不标blocked或完成。
- 后续只读调查：NativeConversationWorkNotifier的30秒业务恢复可归入本节点cron，但事件合并仍用本地执行器，旧ChatBountyBootstrapRelayRecoveryTest嵌套5项须同步真实调用入口和停止语义；未改源码。AgentStatusMonitor同时有本地连接刷新与全库超时，需要拆清节点心跳/集群超时责任后再迁，不能任意容器本地集合代表全局。首次技能报价仍不能直接复用InstalledSkillDescriptorLookup.read（明示含历史、要求当前owner）或activeAuthorizationsForAgent（仅managed安装），公共/模板/手工安装库存覆盖待闭合，未假报完成。
- 用户随后明确“允许”当前ade61e候选额外600秒；累计上限1200秒，已用600.959秒，余599.041秒。本次recommendation-recovery-2只补chat编译与13项单测，复用同源layering成功（58.910s）；全部相关build.gradle摘要与前批比对一致，工作区干净。授权不扩成其他候选/生产发布或无限重试。
- 首期技能费/重邀只读影响追踪新增实证：Runtime SkillInstallManager.listInstalledSkills默认只读state.skills未removed的当前安装（停用仍保留，includeRetained才读历史），但其来源仍仅受管state，不是任意CODEX_HOME技能扫描；SkillRegistry.declaration也只消费该来源。API SkillManagementService.descriptors/validInstallation会依据原change/adoption的owner及原runtimeInstallationId授权，因此“保留公共包+创建新运行身份”不自动等于新关系可用这些技能。首期付款必须建立新关系针对原不可变公共包的使用资格，不能仅计算个数、改旧owner/安装凭据或删旧ACL；旧任务的原授权保持只读可追溯。此为完整重邀验收的真实依赖，未实施也不添加临时兼容绕过。范围仍包含完整已安装清单（系统基础工具排除）、固定报价/清单变化重报、基础租费独立以及新关系授权三项闭环。
- recommendation-recovery-2/session4780终态PASS，实际回读Journal9+Recovery4共13/13、0失败/错误/跳过，固定ade61e83240320eaa4d93e905d135fc8f33788bb/tree b6095ca4216cf7dc0e6999f13e0081eed04f7164。本批墙钟539.426s，和前批受限累计小于1200s（精确数在result.json）；同源layering复用第1批58.910s的真实PASS，原timeout保持FAIL。Agent依赖编译本批FROM-CACHE5.028s，chat编译206.898s、定向测试源码编译24.028s，已完成13项不是只通过编译。未发布；下一继续本节点native待办恢复调度迁移，事件即时提示/现有主流程保留。
- NativeConversationWorkNotifier已将30秒恢复timer迁至节点绑定NativeConversationWorkRecovery，事件提示合并仍使用单线程本地Executor（非ScheduledExecutor）。恢复只读当前本机订阅，无订阅不查业务库；停止后不补查，发现失败传播给task重试，不重发业务执行。原bounty测试中5项native场景移入独立NativeConversationWorkNotifierTest并全部保留/更新调用入口，增加节点/client注册与条件装配共8项；新文件同时纳入原mmdControlledImageBridge和现有runtimeCapabilityRegression入口，不把移动测试变成删除覆盖。此片段未验证/发布。
- 推荐回执受限精确累计1140.381s（600.959+539.422），在用户批准1200s内，session4780已结束。API后续实际业务迁移候选e19d6f0fa6已提交（完整SHA/tree在native-notification-recovery-1/result.json），session70915正在执行8项NativeConversationWorkNotifierTest及layering；新候选默认600秒，没有沿用上一候选额外批准。下一只跟踪本session/结果，不重复启动/不在固定源上改代码。当前没有生产发布、迁移或实际扣款。
- Bootstrap迁移预检补充责任边界：现行AgentTaskBountyBootstrapWakeupPublisher的事件在Spring afterCommit内发布，而ScheduledWorkStore使用REQUIRED同库事务；不能把事件listener简单改为schedule.signal，避免复用已提交仍绑定的事务资源导致新待办未真正提交。迁移须在原业务事务里登记，或在明确afterCommit边界独立新事务，并保留原outbox恢复事实（不得双轨伪造可靠性）。此外Chat admission依赖本机Runtime readiness，不能把每节点现有恢复直接收成任意单一cluster owner，避免owner始终不在Agent所在节点；原队列lease/CAS、readiness及Runtime-awaiting重试保留。当前仅审计，无Bootstrap源代码修改，未缩减全量迁移范围。
- native-notification-recovery-1/session70915已终态PASS：API e19d6f0fa628f728a7dc9e673130aa2814f0870a/tree d1876b2015540ff8451c0c802070699d3ae40bff，8/8通知合并/两lane恢复/无订阅/停止/条件装配单测及layering通过。墙钟539.329s，未超600s；真实XML已回读，原5项没有删掉覆盖，另3项新增边界。仅证明本消费者迁移，未部署/全局迁移未完成。
- Bootstrap源码迁移已实现：去除独立ScheduledExecutor/ScheduledFuture，接ScheduledJobHandler和本节点固定recovery键；启动登记移到ApplicationReady，原readiness/claim/CAS/退避/重复故障停止语义不变，停止不删除持久业务工作。afterCommit通知仅在需要提前期限时使用REQUIRES_NEW短事务；in-flight hint仍内存合并并由当前回调提交后续闹钟，不向业务派发添加租费门禁。未改Agent producer/业务队列状态机。
- 保留原12项Bootstrap定向行为测试（本地取消timer断言转为task持有该职责；停止/重启、无早取/退避、通知合并及未来hint均保留），新增就绪/通知事务传播2项和真实H2+Spring afterCommit独立连接可见性1项。后者检查在原事务资源尚绑定时新调度写入已对另一连接可见，不以Mock传播枚举代替提交事实；调度MySQL SQL仍由task真实MySQL证据负责。待验证，未发布。
- 接续实查：bootstrap-scheduling-1/session62308仍运行，固定API 9e32efa84957a8fcf5a0c26b6ae7d37c11c05141/tree ff187eb119c265abdb1f6d517e72a7f279ee2123；沿原批观察，没有重启或修改受测源码。layering实际PASS（61.913s），15项测试终态尚待回读。使用用户本轮附带规则：同源码受限阶段累计600秒，旧README的重试重置口径不适用本轮。
- 下一批只读核对纠正：ChatBountyExecutionRelay确有旧timer代码，但已无@Component；其Coordinator.pending固定返回空、coordinate固定RETIRED，属于已退役v1-v3，不应为了统一调度重新启用。仍被两项旧capability ObjectProvider及历史测试引用，清理时须一起核对，不可据grep结果登记新cron或复活旧执行。
- ChatBountyAssetRelay仍@Component/条件启用，projector.pendingQuery目前明确排除execution_protocol_version=4，且JdbcTemplate扫描缺少固定环境/客户端分区；迁移前须确认其历史成果投影职责与现行启用范围，在发现责任层解决分区而非在取LIMIT后过滤，不可直接作为任意集群全表任务。
- MemoryJobHandler日/周/月汇总虽使用确定性文档ID，但每次先调用summaryGenerator再save；文档ID幂等不等于模型费用幂等。替换为可重试调度前须处理未知付费调用结果，不可直接让task重试整批并重复生成成功用户摘要。WxSchedule除每日cron还有DelayQueue+ThreadRequest的随机每日一句，现有15分钟Redis日锁不能代表发送幂等；迁移应连持久随机期限及原发送职责一并闭合，不能仅替换注解。
- bootstrap-scheduling-1/session62308终态PASS：固定9e32efa84957a8fcf5a0c26b6ae7d37c11c05141/tree ff187eb119c265abdb1f6d517e72a7f279ee2123，15项测试及layering通过，受限517.794s、墙钟517.805s，无失败/错误/跳过；未部署。原afterCommit独立连接测试实际运行成功。
- 成果投影后续核对：不能把projector的`<>4`误读成“仅旧v1-v3”，现行原生协议为5（PersonalWorkspaceExecutionServiceImpl核对executionProtocolVersion=5）；因此AssetRelay仍需迁移并保留原生成果投影，不随已退役ExecutionRelay一起删除。下一候选复用30秒统一恢复入口、保留即时事件合并和原任务根锁/发布事务，并在查询适配层按固定tenant/client前置分区；现有WorkspaceProjectionQueryMySqlTest可用于真实SQL回归，不新造runner。
- 成果投影候选已提交API43ab7beeca（完整SHA/tree见asset-scheduling-1/result.json）；session29238正在运行15项定向验证及layering。原7项事件行为仍保留，新增持久节点注册/停止回调2项，历史文件名/空页3项，真实MySQL3项（新增固定tenant/client在排序LIMIT前分区，外部hint不得覆盖环境）。复用runtimeCapabilityRegression/source fixture，实际MySQL区间单独计时，其余受限600秒；不复用上一候选额外授权、不在受测源上继续修改。
- 实现：AssetRelay移除ScheduledExecutor定时器，统一cron30秒恢复；即时事件仍普通单线程执行器合并，独立消费者同步边界保留原事件与扫描串行性，不在请求线程等待投影。原task-root事务/ACL/费用/成果发布不改。Projector查询适配器构造时取得固定环境，所有pending查询前置分区；不向Controller/Web机械透传tenant，不新增另一套循环或恢复队列。已退役ExecutionRelay未重新启用。当前未发布、未迁移或扣款。
- asset-scheduling-1/session29238终态PASS：API43ab7beeca252c839787b89c8bbbdd8fe874e217/tree79c3cc7ff73b3fcaaff18e775ee3cb38fd82f0ff，真实XML9项relay+3项历史读取+3项MySQL（含分区在LIMIT前）全部通过，layering通过；墙钟533.309s，真实MySQL47.088s、受限486.219s。未部署。
- 下一消费者AgentStatusMonitor审计：旧方法同时刷新本机socket并扫描全库超时，每节点均查findByStatusAndAbility(null,null)；迁移拟拆为节点连接刷新及集群超时任务，保留已提交lastSeen与原锁内再读，不能把某节点没有socket认作全局掉线。连接刷新只查实际connected IDs，无连接不查业务库。原Worker绑定/身份SQL及校验硬编码tenant0，应在此业务边界使用进程FixedTenantAdmissionPolicy，保留binding→identity→runtime锁序和原发布再核验；不机械重写其他主键DAO。
- Agent presence候选bdb9215845已提交，session41583运行presence-scheduling-1（完整commit/tree在result.json）。验证15项：Monitor10、调度装配3、真实MySQL发现1、原真实锁序1及layering；真实MySQL区间单独计时，其余累计600秒。尚未验证/部署，受测源码保持不变。
- 实际责任层复核发现：BaseDaoImpl仅其通用QueryWrapper路径追加tenant，AgentRuntimeDaoImpl直接baseMapper+LambdaWrapper并不自动分区；因此只给此次两处presence发现查询增加进程固定tenant/可选client（索引等值+binary精确语义），没有机械改所有主键方法。原公共DAO其他使用方式不改。节点刷新无连接不查库，有连接只查其ID集合；集群超时任务使用持久lastSeen并保留锁内再读，本机socket缺席不直接定义远程离线。Worker身份绑定的tenant0常量改为进程配置，真实MySQL锁序测试仍保留。
- 单个原十秒定时入口已去除，新增显式注册agent.status-connections（node-bound）及agent.status-timeouts（cluster）；默认cron仍十秒，配置键jia.agent.status.scan-cron。没有自动激活旧JobHandler cron，没有本机第二poller。原事件发布再校验、用户/关系ACL、SkillAgentVersions观测及任务字段变更语义保持。
- presence-scheduling-1/session41583终态FAIL，受限533.432s，没有启动测试；不是OOM或超时。layering及主代码编译已通过，唯一根因为新配置测试调用ScheduledJobHandler接口的executeScheduled（声明throws Exception），测试方法漏声明/处理受检异常。修复仅补测试方法throws Exception，保留3项装配断言和全部业务测试，不改接口/不删测试。原失败日志和源码保留；更正后为真实变化的测试输入，不原样重试。
- 当前失败矩阵：历史skill-recovery-wildcard-layering已由a81及后续真实layering通过证明修复；历史预算异常有明确单候选批准且未沿用；本次presence-scheduling-test-checked-exception首次出现且已定位编译器两处行号，新增fixture声明后才能验证。ledger累计失败触发root_cause_matrix_required，按原authorize-remediation记录当前更正源和此矩阵，不绕过准入。后续新固定候选仍默认600秒，受限/回归分开。
- 更正候选97fe0bf717已提交，presence-scheduling-2/session92096正在原入口执行相同15项+layering；本次无需重新编译未变主代码时仅复用有效compile缓存，不复用历史测试结果。未发布，不改正在受测源码。
- presence-scheduling-2/session92096终态FAIL：实际XML显示调度装配3、Monitor10、真实锁序1均通过；唯一失败为新增真实发现fixture仅加载基础agent_runtime DDL，遗漏既有agent-runtime-session-fence-v1.sql，MyBatis查询提示runtime_installation_id缺失。不是过滤SQL/资金或生产故障。已用原正式migration补齐本测试私有库，不为过测试改SELECT列/删除断言。原失败保留。
- 修正候选f8aae90f1e已提交，presence-scheduling-3/session78282在途，同15项与layering，复用有效主代码compile缓存但不复用测试结果；真实MySQL单独计时。未生产迁移/发布，不改当前受测API。
- ChatDeliberationOutboxRelay下一步调用链已核对：本类业务scan/nextDueAt一次性闹钟必须迁移，deliveryScheduler及三个在途claim heartbeat仍本机执行者责任。原wake事件来自afterCommit，沿Bootstrap已验证的REQUIRES_NEW通知边界解决，不将长Provider调用搬到统一调度线程。原独立deliveryExecutor/容量、claim/settle、nextDueAt、500ms故障退避及5秒漏提示恢复保持。R8真实集成有3处依赖旧start自动本地timer，需改为显式驱动统一回调而非删除测试；commit单测嵌套Scheduling的8项覆盖也保留。

- presence-scheduling-3/session78282终态PASS：APIf8aae90f1ecdf13a21b01189583f4a9b33451b80/tree107b2b9455ee490cd4b075895fc6bf11300ac88f，15/15及layering通过，真实XML回读无失败/错误/跳过；受限420.999s、真实MySQL87.895s、墙钟508.902s。前两批失败保持原状态，分别修复fixture受检异常声明和漏加载既有session-fence migration；没有改生产查询以迎合测试。未发布。
- ChatDeliberationOutboxRelay候选25c5444ecc已提交，deliberation-scheduling-1/session67531正在运行34项（原commit/调度13、新独立JDBC afterCommit1、真实H2 R8业务20）及layering。任务源码固定；此轮受限600秒，真实R8单独计时，新增小型JDBC fixture保守计入受限阶段。未发布/生产操作。
- 实现保留deliveryExecutor/容量与本机执行心跳，只删除业务pendingWake/ScheduledFuture；节点固定key接管最早deadline，ApplicationReady登记，提示只在提前期限时REQUIRES_NEW提交。短调度回调只发现/领取并派发原执行器，模型/网络调用不占统一调度worker。原nextDueAt/5秒补查/500ms异常退避及生命周期归属保持，停止不删除持久工作。
- 旧13项测试均保留，旧timer被取消后的断言改由统一回调启动/停止/就绪及真实key验证；在途心跳未改。R8原3处start自动定时触发改为显式统一callback入口，其真实claim/settle/隔离/异步delivery及20项业务断言保留，并非删测试或用Mock代替业务SQL。新JDBC测试在旧事务afterCommit尚未清理时，用独立连接读到新wake，防止REQUIRED写入丢失。

## 2026-11-10 deliberation-scheduling-1受限阶段终止
- 接续轮询原session67531，终态FAIL：固定API25c5444ecc6f0cde1460abbe55cd7489b07b9fae/tree0185b912aeb46820d9e2792b9ea960ab58ab4154；受限/墙钟600.935秒，真实回归0秒，driver以SIGTERM结束本批进程组。result.json与gradle.log保留在`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/deliberation-scheduling-1/`。未启动重复验证，未更改固定源码，无生产操作。
- 已实测validateLayering通过69.108秒，chat主源码compileJava通过189.915秒，根配置/任务图136.950秒（相对init）；其余时间包含JVM启动、依赖构建/缓存恢复。没有生成测试XML，34项预期用例不能宣称通过。终止后精确检查本driver、原编排器943517与GradleDaemon无存活；不清理其他进程或缓存。磁盘可用约481MiB。
- 本次遵循会话提供AGENTS的固定源码累计600秒，不用磁盘旧文档重试重置口径。需用户批准本候选额外600秒（累计1200秒）才能继续同源验证；现有批准只覆盖旧a81/ade候选，不能挪用。后续可复用同源layering和主源码编译缓存，补14项定向单测与20项真实R8回归，真实回归单独计时。原FAIL不重标、不删测试、不以无关提交重置预算。
- 等待期间只读审计下个AgentTaskEventReplay迁移：timerExecutor仅为补偿扫描，不是传输心跳；应移除共享业务timer、保持catchUpExecutor单航班/最后订阅取消中断/原ACL及背压，用节点统一恢复触发。原测试中主动计时触发掉失通知和slow compensation须改成实际统一回调，不可仅改计数断言；尚未改该源码。ArchiveQuestionWorker还含旧250ms业务扫描及独立租约心跳，后者不能删除；完整范围未缩减。
- 用户明确“允许”25c5444候选追加600秒；累计1200秒、已用600.935秒，余599.065秒。第2批保持精确源码及所有构建输入不变，摘要已复核；复用同源layering与编译缓存，仍执行全部14项单测及20项R8真实回归。原FAIL保留，授权不扩成其他候选无限重试。工作区干净、普通磁盘可用429MiB，未发布。

- deliberation-scheduling-2/session10342终态PASS，已回读4份XML共34/34（14单测+20真实R8）、0失败/错误/跳过。固定25c5444ecc6f0cde1460abbe55cd7489b07b9fae/tree0185b912aeb46820d9e2792b9ea960ab58ab4154，受限199.288s，真实回归24.119s，墙钟223.414s；累计受限800.223/1200s，复用同源第1批layering69.108秒PASS。原FAIL保留。统一调度后原容量/afterCommit独立JDBC提交/租期禁止新密议而既有继续/真实发布重试均通过，未部署。下一消费者AgentTaskEventReplay，仅移除业务恢复timer、保留订阅执行和原授权/背压。
- 事项事件补查源码已迁移：AgentTaskEventReplayRecovery显式节点cron默认5秒，ApplicationReady注册；原服务删除业务ScheduledExecutor及periodicCheck字段，不保留旧timer兼容轨。统一回调只提交原catchUpExecutor的single-flight恢复，保持订阅scope/分页/背压/容量与最后取消中断；无订阅不提交执行/不查业务库。没有移动SSE心跳。既有47项测试保留，周期掉失/饱和/慢查询用真实新适配回调触发；计时器队列断言替换为实际订阅清理，新增4项登记/节点/失败/启用测试。沿既有mmdU1BootstrapOutbox源集定向执行，不新增runner框架。源码未验证/未发布。
- 新候选固定APIe507d428f8ae4cefa965d8c383bcf1fae205364a/treee4bee346694e699ceb66d4067232f519a2bae17f，event-replay-scheduling-1/session91140在途，driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/event-replay-scheduling-driver-1.py`；预期51项（原47+新增4）及layering，默认600秒，未复用旧候选扩时。当前已完成根配置/任务图，尚无测试结果；接续先轮询该session，不在同源验证中改代码/重启。工作区干净。下一消费者Rabbit发布与命令重发只读审计：原配置分别AgentRabbitPublishEnabledCondition/agent.rabbit-dispatch.enabled，均须保留，不自动打开；业务发现目前仅传processTenantId（selectDue/Stale/Corrupt、findDueCandidates），固定client分区需在真实SQL LIMIT前补到发现责任层，而非领取后过滤。尚未修改Rabbit源码。
- event-replay-scheduling-1/session91140终态FAIL（600.974秒受限、真实回归0秒、SIGTERM），精确e507d428f8ae4cefa965d8c383bcf1fae205364a/treee4bee346694e699ceb66d4067232f519a2bae17f。XML0份，不能声称51项已通过；layering通过42.934秒、Agent主代码编译222.816秒、根任务图105.851秒（相对init）。原源集继承agent testImplementation对chat-service的依赖，Agent ABI变化又触发chat-service编译，截止时只输出编译警告未完成事件，这是本次剩余耗时的实质来源；不是事件补查业务调用慢。终止后driver/GradleDaemon均无存活，未重启/改源码/操作生产。
- 需要单独批准本e507候选额外600秒（累计1200）补51项验证，不能挪用仅对25c5444生效的上次批准。保留FAIL、同源layering成功及主代码编译缓存。后续可按真实依赖优化定向测试源集，避免每次Agent纯单元验证强制重编译chat；当前不得以改源集/无关提交重置已有预算，也不删必要用例。

## 2026-11-10用户临时取消时限
- 用户明确“临时取消时间限制”，本任务后续本地验证/构建/发布暂不以600秒中断，继续记录实际阶段/墙钟耗时；不修改根AGENTS或共享长期规则，不追溯重标既往FAIL，不放宽身份/ACL、串行锁、资金事务、必要回归、普通磁盘和受控发布边界。恢复时限由用户后续决定。
- 恢复精确e507d428f8ae4cefa965d8c383bcf1fae205364a事件补查验证：工作区干净，前批全部输入摘要一致；第2批复用第1批同源layering42.934秒成功及编译缓存，继续原51项测试。新driver显式记录本次临时豁免和原600.974秒，不覆盖历史记录。生产状态未变。
- event-replay-scheduling-2/session74945已结束：Gradle实际成功、两份XML全部71项通过，但外层driver误将预期数量写成51，故原result保持FAIL(exit2)。已定位数量来源为原服务37项@Test+10参数用例+完全限定@RepeatedTest(20)=67，新适配4项，总71；并非多跑未知用例或缺测。第2批墙钟306.942秒，全部为单元验证，受用户临时豁免。接下来用精确源码方法名/参数名/重复次数与原XML逐项核对，形成独立纠正验收凭据，不重标原FAIL、不重复构建或删除重复竞态用例。
- 独立`event-replay-scheduling-2/verification-audit.json`已PASS：逐一匹配37方法名+10参数名+20重复用例与XML，以及新增4方法，共71/71；绑定源码、报告、原result、审核脚本、同源layering日志摘要。原第1批超时、第2批driver数量FAIL保留，实际用例未重跑，编排归因已解除。该消费者源码可用于下一集成候选，未发布。
- 下一片段先迁Rabbit Outbox：仅原publish启用且统一调度启用才装配新handler；原Rabbit Shadow/dispatch gate、topology readiness、独立publish worker和确认/settle事务保留。业务扫描用持久节点deadline，未开启Rabbit；原25–60000ms设置语义保留。补固定client发现分区在SQL LIMIT前，服务/DAO既有锁和主键方法不全面改造。Command reissue、Memory/Wx、Archive以及资金全链仍未完成。
- Rabbit Outbox候选已提交1b2fccf25e（完整commit/tree见`rabbit-outbox-scheduling-1/result.json`），当前session81582在途，driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/rabbit-outbox-scheduling-driver-1.py`。预期38项：scheduler6、config3、mapper合同7、真实隔离H2事务22，加layering；未验证完成不可称PASS。显式清掉D03_MYSQL环境参数，只使用该测试自身私有H2，不连接生产数据库/Rabbit。计时沿用户本任务临时取消上限，仍分别记录H2回归与其他阶段。接续先轮询本session；不可因观察超时重启或改固定源码。
- 当前实现只迁Outbox，不冒充CommandReissue完成：删除本机250ms业务poller，保留原publish worker/容量/drain；ApplicationReady持久首唤醒、回调持久下一期限，stop后回调不查库；失败传播给task恢复。config在原publish条件外叠加明确统一调度开关。固定client只在DAO发现适配器传给三条SQL，LIMIT前精确分区；不新增逐主键过滤。新增H2用低id外部client、大小写及尾空格覆盖due/stale/corrupt三路，原事务/锁序用例未删。原配置下Rabbit仍关闭，未发布。

- rabbit-outbox-scheduling-1终态FAIL，墙钟613.757秒，非超时；主代码及layering通过，两个新增测试漏声明ready()受检异常导致测试编译失败，无测试通过结论。仅补throws Exception，不改业务/断言。修正候选d4a1afc7a3ba8360d11fe71fcbca85bf67bace6e/treec5b85608eb42a9585b5fe5eb6261b4a614ac71b9；第二批沿用户本任务临时取消时限继续，无生产操作。

- rabbit-outbox-scheduling-2/session1565终态PASS：API d4a1afc7a3ba8360d11fe71fcbca85bf67bace6e/tree c5b85608eb42a9585b5fe5eb6261b4a614ac71b9；真实XML回读38/38、零失败/错误/跳过，layering通过。墙钟415.343秒，H2真实回归10.072秒，其余405.267秒；仍适用临时无时限。未发布，未连接生产Rabbit/数据库。
- 普通磁盘低至约200MiB：仅清理本任务三个已终止FAIL批次event-replay-scheduling-1、deliberation-scheduling-1、rabbit-outbox-scheduling-1的classes/generated/tmp编译中间目录，删除文件字节66940885；各原批次compiler-intermediate-cleanup.json记录精确路径及源码，保留libs、日志、XML、reports、result及全部源码，不触及生产/备份/共享缓存/活动批次。回读可用251MiB。
- 下一实际迁移为AgentCommandReissueCoordinator：删除本机业务timer，保留单线程普通worker、非阻塞有界重连队列、cursor、事务及自动重放来源保护；统一node-bound到期回调先持久下一次期限，再single-flight提交扫描，慢扫描不占金融调度worker。config保持原Rabbit启用门并明确统一调度开关，bean暴露具体ScheduledJobHandler类型。只给due发现DAO补固定client的LIMIT前分区，reconnect及主键授权保持。定向补Ready/单飞/失败/停止/注册与真实H2隔离测试，不激活生产禁用Rabbit。

- Command recovery固定候选b6c29aaaad817abce9ff0497721672e897cf12af/tree24f38f0da638140a38490f087348e5235b423c33开始command-recovery-scheduling-1：预期coordinator7、config3、mapper合同5、真实H2事务20，共35及layering。DAO新增固定scope构造依赖的全部9处显式fixture调用已同步；业务service未改，当前定向未声称其余fixture全部实跑。未发布，沿本任务临时无时限。

- 后续Archive只读调用链核对：业务250ms发现位于ArchiveQuestionWorker.start；独立leaseExecutor是运行中30秒租约的10秒续租，必须保留。Bootstrap目前ApplicationRunner触发start，应收口为显式统一Ready注册/回调，普通worker执行Provider，避免阻塞调度。JdbcArchiveQuestionStore的claim/exhausted/publish三路发现硬编码tenant0，且ArchiveOwnerScope紧凑构造器无条件改tenant为0；仅更改SQL不能解决隔离，应先按该个人数据scope真实生产者/消费者定向修正责任边界，不把记录构造默默改tenant的行为当可靠分区。当前仅分析，未改Archive源码。
- 资金后续只读核对确认：初次quote和lease均直接复制plan.amountWen，尚无保留技能库存收费字段；未来加入首费时必须同时拆分quote总额与lease基本月租。现状不能声称已覆盖保留技能首次收费，亦不能将未上线的潜在总额重复续扣说成已发生生产错扣。

- command-recovery-scheduling-1/session89949终态PASS：API b6c29aaaad817abce9ff0497721672e897cf12af/tree24f38f0da638140a38490f087348e5235b423c33。XML独立回读35/35（coordinator7/config3/mapper5/H2事务20），零失败/错误/跳过，layering通过。墙钟803.516秒，H2集成21.971秒、其他781.543秒，用户临时取消时限生效，未中断/重标。主要任务耗时mapper compile58.87、Agent compile165.15、Chat compile161.86、定向test compile50.12、layering50.94秒；本轮没有实际生产/付费调用。源码干净，已无在途Gradle。
- Archive后续边界精确入口：ArchiveOwnerScope将任意tenant改0；生产者ArchiveQuestionController.authorize/ArchivePersonalDataController.authorize显式使用SINGLE_TENANT，ArchiveConversationTools和ArchiveMaintenanceService传现有可信subject/scope。JdbcArchiveQuestionStore三路扫描WHERE硬编码0，Worker.allowed又只认0。迁移时不能只给扫描SQL注入tenant而忽略scope构造/生产者，应先定向检查其余个人数据存储，保持公共档案定义与私有用户数据区别。已定位ArchiveQuestionBootstrapTest/FeatureFlagTest、WorkerTest、JdbcArchiveQuestionStoreTest及真实ArchiveQuestionMySqlIntegrationTest；现有测试强断言旧强制0行为，不可把测试存在当保留理由。
- 接续仍为完整TASK-SCHEDULING目标，不因两处Rabbit通过缩小范围：剩余Memory/Wx/Archive业务定时、真实多容器Redis/混合容量、保留技能全量库存/报价冻结/新关系资格、首费与基本租金分离、自部署50/既有30日过渡、完整同实例重邀、Web桌面移动和受控发布/线上验收。当前所有进展为源码/局部验证，尚不可宣称完整可验收或上线。

- Archive候选2ef3fc916fa780c85c90e189ed5a82acfcece82d/tree5d5637d6bc74eb9a4d042287573ba63ac06287f6：Bootstrap改为Ready显式node-bound注册及持久下一期限；Worker只普通single-flight执行器，10秒在途lease续租保留；未改原outbox执行/重试/队列公平规则，不在统一调度线程调用Provider。原250ms恢复周期/独立功能关闭开关保持。真正影响的私有scope构造不再强制tenant0，两HTTP生产者从固定配置取tenant，原可信tools/maintenance scope继续沿用；三个发现SQL在ORDER/LIMIT前配置tenant/client，public内容/索引不改，不增加逐主键tenant过滤。
- Archive定向计划75项（73单测、2真实MySQL），复用archiveReaderRegression入口及既有自有MySQL fixture；原H05A用例改用进程自行启动的私有MySQL，不读取用户数据库环境。包含HTTP可信非零tenant、私有数据service、35项worker含租约、Bootstrap/feature/store、真实原四域并发/重放/CAS及新增tenant/client大小写/尾空格前置LIMIT。当前待验证，不能称PASS。
- 为真实私有MySQL腾普通磁盘，只清理本任务已终止presence3/deliberation2/event-replay2及bootstrap1/asset1/cron-scheduling1/cron-maintenance1的编译classes/generated/tmp；累计110665438文件字节，精确路径与commit在原批次compiler-intermediate-cleanup.json；日志/XML/reports/libs/源码及最近Rabbit/Command批次均保留。回读344MiB，不碰生产/备份/共享缓存/他人数据。

- Archive正式验证session63110在途，driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/archive-question-scheduling-driver-1.py`，结果目录`archive-question-scheduling-1/`；接续优先轮询同session，不因观察等待超过600秒重启。当前已进入Agent生产编译（Archive core变化引发真实依赖重编译），无测试通过结论。源码固定，等待期间只读调查。
- Memory下一步只读确认：MemoryJobHandler必须继续作为普通JobHandler供手动调用，不能直接变ScheduledJobHandler；旧JobExecutor会拒绝后者手动执行。统一调度可用单独显式cron适配器，但不得靠异步提交成功/固定ES文档ID宣称付费执行幂等。LongTermMemoryServiceImpl在写ES/标记SYNCED之前调用摘要和embedding，失败后pending会保留；daily/weekly/monthly也先付费再写固定ID。现有task JobExecutor只有进程内runningJobs和日志，无持久完成事实，不能复用作未知结果去重。Memory迁移需明确业务接收/未知结果边界，不盲用调度恢复重放同cron付费批次；尚未改源码。原手动/历史周期业务能力不能删失。

- archive-question-scheduling-1/session63110终态FAIL，402.397秒；layering30.909s与全部main编译通过，未运行测试。唯一编译失败为ArchivePersonalDataServiceTest使用全限定类名构造HTTP controller，之前短名依赖扫描漏掉其新增FixedTenantAdmissionPolicy参数。已复核全限定/短名全部引用，只修此fixture，保留断言；同批增加真实MySQL测试AfterEach停止其自有Worker，避免测试租约线程残留，不改业务源码。
- 本次失败矩阵：Rabbit受检异常已由d4a1afc/38项+layering通过证明修复；Command恢复b6c29aaaad/35项通过；EventReplay原计数FAIL由原XML逐名称71项独立audit确认（不重标原FAIL）；旧预算事件用户临时取消上限后不再适用，但历史FAIL保留。当前首次archive-private-data-fixture-constructor有编译器精确行号和真实修正，非同输入盲重试；ledger累计root_cause_matrix_required按此记录authorize-remediation后验证，不绕过。

- Archive批次2/session96485中断FAIL，603.301秒（非预算到期）。真实私有MySQL2/2已完成、73项单测未全跑；不能把部分XML说成75项通过。线程dump证实新测试在worker同步runOnce持锁且等finally释放latch时，主线程Mockito.verify同方法反向等待；只SIGTERM本任务Gradle test worker PID1020512，driver自然收尾，证据在archive-question-scheduling-2/test-thread-observation.txt与test-interruption.json。另两失败为common-test的application.properties抢先命中、150ms测试租约在实际负载下失效。新候选仅修测试：原子计数不再争同步方法锁；枚举实际packaged资源准确核对默认关闭；publisher隔离用固定clock加真实renew方法的latch，独立墙钟跨租约用例保留。原失败/跳过与耗时不重标。批次1已终止编译中间产物清理22151539文件字节，路径/commit回执在其compiler-intermediate-cleanup.json，未动libs/日志/源码/生产。
- 修正候选5ef7f8d870da754df25460f3124ffa9008f75fff/treef846b3c48441e6d143ad075fc32e9a246d978632，archive-question-scheduling-3/session1028正式在途；仍是75项+layering，未删断言/重标上一批。下一自然接续先轮询session1028并查原gradle.log，不并发启动另一Gradle、不修改固定API源码。
- 后续旧计时入口定向核实：task/.../executor/JobExecutor.scheduledExecute仅每分钟打印getCron元数据，不执行业务；可直接移除无用定时方法，不需迁入另一个空扫描。TaskAlertJobHandler仍是可手动调用的普通JobHandler、cron仅元数据，设计§55/88明确不能自动启用。Memory需独立cron适配以保留普通手动入口，未知付费结果不能仅靠ES固定ID宣称幂等；Wx须保留发送/随机期限能力，不能删除业务来凑统一调度完成。未在本候选扩改这些业务。

- archive-question-scheduling-3/session1028终态FAIL，611.955秒，75项74通过；真实MySQL2/2、Bootstrap/HTTP/store/service及修正spy/资源测试均通过，layering通过，零跳过。唯一失败旧healthyProviderCrossingInitialLease...在300ms墙钟租约下RUNNING而非SUCCEEDED；不能调大生产租约或把失败叫成功。候选ce9e25b24b保留真实异步heartbeat及真实renew CAS，受控业务clock逐次+100ms、8次renew后provider返回，显式证明跨原300ms初始期限；另增无续租推进60秒必须丢弃结果的反例。上一批publisher隔离已通过，说明该剩余是独立墙钟用例；本次有实质修正，不原样重试。原历史失败矩阵不变，按既有authorize-remediation恢复验证。
- 同一目标下一处无用计时器已删除：候选8e015b3b3a43d04a7a25929a69af1c2dfd77284a/treee8231bbe0f02cc6250bbba3264ca068ddc2a3f1d移除JobExecutor每分钟只打印cron元数据的Scheduled方法，普通手动调用和JobHandler cron元数据保留，不注册TaskAlert、不新增空查询。补2项executor回归，与原Controller2、CronDispatcher14一起验证，联合Archive76共94项及layering。尚待本批结果，未发布。
- 磁盘只回收已终止Archive2的classes/generated/tmp，共22598138文件字节，原路径/commit见archive-question-scheduling-2/compiler-intermediate-cleanup.json；测试XML、日志、线程dump、libs全部保留，未清理共享缓存或生产数据。
- 接续入口：archive-question-scheduling-4/session21254确认存活，driver为同名driver-4.py；本批源码8e015b3b3a，94项+layering。下一轮先poll同session，不重复启动/不改固定源码。上一轮已实质修改并提交归档测试、移除旧元数据计时器，属进展；目标仍完整资金/租费/技能/收尾/统一调度及上线验收，未缩为Archive通过。
- 本轮等待同一session21254期间只清理精确6个已终止自有批次的编译中间产物：combined-3、hosting-position-final-3/4、skill-delivery-scheduling-5、hosting-provision-scheduling-1、hosting-legacy-unbind-removal-1。逐批核对result为PASS/FAIL、无进程引用、无既有cleanup记录，保留commit/精确路径/fileBytes到原批次compiler-intermediate-cleanup.json；仅classes/generated/tmp，未删libs、日志、XML、源码、共享依赖、备份或生产状态。共132108482文件字节（实际文件系统释放另观测），避免后续私有MySQL反复逼近磁盘耗尽。当前正式验证不重启。
- archive-question-scheduling-4/session21254终态PASS，API8e015b3b3a43d04a7a25929a69af1c2dfd77284a/treee8231bbe0f02cc6250bbba3264ca068ddc2a3f1d；逐XML独立回读94/94，0fail/error/skip，layering通过。Archive76（Bootstrap4/feature2/worker36/两HTTP各6/service13/store7/真实MySQL2），task18（Controller2/manual executor2/CronDispatcher14）。墙钟748.962秒，真实MySQL176.940秒，其他572.013秒，用户临时取消限制，原失败保留。源码干净，本批Gradle终止，生产未变；归档问答业务发现迁移及旧metadata空timer退役已验证，不能作为Memory/Wx或完整上线证明。
- 下一实际工作仍为剩余Memory/Wx与费用闭环。新增只读核对：Memory的findPendingMemoryConversations原生SQL固定tenant0，LongTermMemoryServiceImpl也硬编码0；MemoryRepositoryImpl仅按jiacn查询ES，不能只把SQLtenant改掉便在新分区启用索引读写。迁移须在实际存储责任边界处理分区，不逐层复制认证。任务基础没有持久外部调用receipt，新的重复cron必须避免同一次未知付费执行被通用重试放大；保留原手动与周期能力，不顺手关闭。尚无该部分代码修改。
- Memory开始实作：普通MemoryJobHandler保留手动执行/业务锁，独立定时入口删除；新增MemoryScheduledJob显式cron及MemoryJobRunStore/JDBC同库发生点回执，STARTED在模型前提交，结束状态独立提交；同一发生点的STARTED/终态均不重复模型，新周期保留pending重试。DDL仅候选，无自动迁移/付费调用。复用runtimeCapabilityRegression入口，计划32项（adapter18+原memory10+真实MySQL4）与layering；真实MySQL验证并发单次、独立连接可见已提交STARTED、结束回滚保留未知、下一周期和精确scope/token。原service/ES的tenant0/owner-only问题与混合容量还未修改，不能称Memory迁移完全完成或提前上线。
- Memory候选6da33367f228e49885bd8e83521d324a7ab2cfa6/tree3118ebc5e2edc7a23c024180e42b4012bb87f72d已提交；memory-scheduling-1/session28708在途，driver memory-scheduling-driver-1.py，32项+layering，无600s终止，真实MySQL单列。下轮先poll28708，不并发Gradle或修改固定API源码。
- Memory后续真实调用链已定位（只读，尚未改）：MemoryRepository仅LongTermMemoryServiceImpl、ChatController.library读写、LongTermMemoryAdvisor三个生产消费者；advisor上下文已有clientId（相邻DatabaseChatMemoryAdvisor已用），Controller用现有EsContext。可在这些实际边界传client/owner、存储适配从配置取tenant，不层层解析JWT。日报/周报/月报原findActiveJiacns丢失client，必须保留client/owner组合；原conversation DAO/service有显式tenant重载可直接复用，不加历史0兼容。ES原query只有jiacn，需责任层索引过滤+新字段映射及带scope的确定ID；未知旧doc不能猜client归属。cleanupExpiredMemories有旧删DB消息能力，但MemoryJobHandler未调用，本迁移不能自动启用该清理（用户要求数据库会话长期保留）。上述是下一源码工作，不属于本32项结果。
- memory-scheduling-1/session28708终态PASS：固定6da33367f228e49885bd8e83521d324a7ab2cfa6/tree3118ebc5e2edc7a23c024180e42b4012bb87f72d；独立回读XML32/32（adapter18、真实MySQL4、原memory10），0fail/error/skip，layering通过。墙钟881.995秒，真实MySQL93.000秒，其他788.947秒，临时时限豁免仍有效，未发布。下一实际工作为SQL/ES分区，不把本批当作完整Memory或完整上线验收。
- 只读GET现行chat_memory/_mapping，实际alias目标chat_memory_v2：jiacn、conversation_id、summary_type均keyword，embedding1024/cosine/bbq_hnsw；没有tenant_id/client_id。证据memory-index-mapping-observation.json（本任务既有证据目录）。必须受控添加精确keyword映射并同步真实三个消费者，不能假设动态text字段或.keyword已有，也不能猜测旧doc的client归属。未改生产mapping/文档，未调用模型。
- 本轮仅回收已终止自有archive-question-scheduling-3/4编译classes/generated/tmp，文件字节22598872+22848789；原批次compiler-intermediate-cleanup.json保留commit/路径/结果，保留libs/XML/logs/reports/源码，未清理生产、备份或共享缓存。
- Memory分区候选已实作（待验证）：raw SQL发现从进程tenant/可选client精确过滤后cursor/LIMIT，活跃摘要按MemoryOwner(client/account)发现；服务复用显式tenant DAO与原锁/事务；三个真实ES消费者携带trusted client，ES统一keyword预过滤，确定ID纳入tenant/client，未知历史文档无owner-only兜底。新增mapping JSON只为受控候选，生产未变。定向增加真实MySQL大小写/尾空格/分页/配对/污染排除、ES query/mapping、advisor/context和Controller案卷边界；原memory与发生点回归仍保留。详细职责/迁移前置写入原design，非新框架。
- Memory源/索引分区候选固定API761027c99d4ef4f885e842a4a887a2497d26058d/tree1735c56fa6506092d3354d04aa2a2a3fcd27d521，memory-scope-1/session74458已启动；driver为本任务证据目录memory-scope-driver-1.py，52项（原adapter18/receipt MySQL4、memory服务12、ES9、真实scope MySQL4、advisor2、Controller案卷3）及layering。临时无时限，生产和mapping均未改。下轮先轮询74458，不修改固定API源码、不并发/重启Gradle。UR04/UR06自建Spring fixture补明确0租户policy bean，旧工作流SQLfixture调用同步新mapper签名；这三份fixture尚非本52项实跑范围。
- 等待期间Wx只读核对：旧每天7:30投票含15分钟Redis NX租约，然后创建随机当日DelayQueue及ThreadRequest长等待每日一句；不能只搬7:30cron而保留内存队列。订阅实体有tenant/client，公共MyBatis责任层需核对后台上下文；Kefu发送/MatVote出题仍按jiacn接口，须沿实际调用链验证可信client的来源与执行隔离，不能由调度任意改scope。下一迁移要保留持久随机到期、重复同日发生点/未知外部发送结果语义，不扩改共享ThreadRequest、不自动触发真实微信发送。本轮未改Wx源码。
- 2026-11-11接续74458仍存活（已poll），未重启/改候选。Wx边界进一步核实：TaskTenantConfiguration拦截器只覆盖cn.jia.task.mapper的task_plan/task_item/v_task_item，不能作为Kefu/Mat/Wx自动隔离证据；BaseDao.selectByEntity只在实体显式tenant时过滤，后台不会自动填可信client。MpUserService.findByJiacn当前仅按jiacn取首条，MatVoteQuestionMapper.selectNoTick原SQL也仅jiacn。后续迁移需在订阅发现/具体发信用户查找/出题查询三个实际边界补scope，不向通用ScheduledJobRunner塞HTTP上下文或全局扩大拦截器。本轮仅只读确认，未变更微信业务、未发送真实通知。
- 2026-11-11等待memory-scope固定候选期间只读核验Runtime：HEAD仍b970258db0e641318bc201f068c66ac5efb002a0/treeedb825ff833b5d067b10f4d68970e3515f61b185；外部仓README/install/python-artifact/freeze/new-api-deps等为无关脏修改，未覆盖/暂存。实际CODEX_HOME/skills顶层：linchong4、wuyong5、lujunyi3个带安装marker的普通技能目录；managed现有一处HOME仅.system。未读取会话内容、未据此计算扣费或把顶层枚举冒充完整含停用库存。listInstalledSkills默认仅journal current/nonremoved且校验可见view，includeRetained则含历史activated版本，不可拿后者计费。Runtime未编辑/构建/发布，首费完整库存和新关系权益仍未完成。
- memory-scope-1/session74458终态FAIL，761027c99d/tree1735c56fa6，墙钟1677.907秒，真实MySQL313.921秒，其余1363.986秒；全部52实跑，48通过，4个新MySQL用例因同一SQL1267失败。layering与编译通过，原receipt MySQL4/adapter18/service12/ES9/advisor2/Controller3均通过；不能重标整批成功。根因为`m.conversation_id = CAST(c.id AS CHAR)`在源列general_ci、连接0900_ai_ci时双方IMPLICIT collation冲突，后续binary谓词不能消除前面表达式错误；测试保留不改collation。修正仅把JOIN右边变为canonical id的BINARY表达式，保留左边列可用索引及尾空格精确语义，移除重复binary谓词，不放宽scope或重放保护。按编排器登记真实失败后重新固定候选验证。
- 新候选0b99bdd02e已提交，memory-scope-2/session80398正式在途（driver memory-scope-driver-2.py；完整commit/tree由该批result.json绑定）。仍跑原52项与layering，未删除失败断言或改变fixture排序规则；临时无时限，生产未变。下一接续首先poll80398，不再poll已终止74458，不改API固定源码/不并发Gradle。上一目标轮有实质SQL修复、提交和新批验证进展；完整资金与调度上线目标未缩小。
- 2026-11-11因当前正式验证直接读取task-scheduling-api固定源码、前批墙钟1677.907秒，确实不能在原目录并发写下一消费者；既有其他worktree属其他任务不可复用。仅新增一个本Owner持续复用的写入工作区`/home/isp/wsps/worktrees/task-scheduling-api-next`，分支`codex/task-scheduling-next-20261111`，base0b99bdd02ef4e6ac034aeb1f7d834acbeece1911/treed0643794f372dc869748fe2e6f5cfd11b3735cd2。不按阶段/重试再建worktree，不启动第二批Gradle；当前80398继续读原目录，后续代码在新目录推进，最终合入后按本任务范围回收。Owner仍task-scheduling-owner，不新增子Agent/Reviewer，适用根AGENTS、API接口规范v1.4和RB-1。
- 2026-11-11 memory-scope-2/session80398终态PASS：API0b99bdd02ef4e6ac034aeb1f7d834acbeece1911/treed0643794f372dc869748fe2e6f5cfd11b3735cd2；独立回读7份XML52/52，0fail/error/skip（adapter18、receipt MySQL4、service12、ES9、scope MySQL4、advisor2、Controller3），layering通过。墙钟1169.957秒、真实MySQL78.142秒、其他1091.811秒；用户临时取消时限，旧失败不重标。实际ES mapping/query与混合worker容量仍待验证，不冒充上线。
- Wx第一片段已固定于writer候选b6e4e4200edb7915ab82a350213d40555001ae8b/treee6f8f5d4952aae304c30e5bda51fd98da6a4770d：新增notice receipt（冻结日/订阅/接收人/随机截止时间；STARTED原token结果，未决不得重发）、受控DDL候选无CHECK无启动建表；Kefu订阅发现DAO按配置tenant/optional client在cursor/LIMIT前精确分区，派送前按冻结owner/type/subscription重新确认有效，旧普通业务查询未扩改。服务透传，不注入HTTP上下文、不新增全局拦截器。新增10项（Key2、receipt真实MySQL5、订阅真实MySQL3），复用纯JDBC fixture而非Agent业务service依赖。
- wx-notice-scope-1/session83256在途；driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/wx-notice-scope-driver-1.py`，在task-scheduling-api-next固定源码执行10项、Kefu服务编译及layering。不可在本固定writer改源码/并发Gradle。当前仅receipt和订阅查询实现，旧WxSchedule cron/DelayQueue尚未替换，收件人/素材/模板scope及真实发送结果歧义仍待补齐；没有发真实微信、没有应用DDL或发布生产。
- wx-notice-scope-1/session83256已PASS：b6e4e4200e/treee6f8f5d495，独立回读3份XML10/10，0失败/错误/跳过；Kefu服务编译及layering通过。墙钟356.902秒、真实MySQL100.999秒、其余255.902秒。receipt/订阅边界已验证，不代表Wx整体迁移完成。原验证工作区结束后ff至该候选，在原task-scheduling-api继续写入；只复用现有两处本Owner工作区，不再新建。
- 下一候选0715d0cd6e7f886452fdd44b4552469f57f83fd1/tree2dad208ae70fc18f68aec0d4524567c84a321b39已提交：MpUser计划发送查找按配置tenant+admitted client+exact jiacn在LIMIT2前限定，重复身份报歧义而非任取第一；Kefu模板定义同scope且有效；新增scoped发送入口只查一次确切用户/活跃事实并返回sent+active，发送日志带scope。实际模板主键读取后核对其tenant/client/appid再发，不扩改全部DAO；共有文本发送抛出异常时不发第二条模板（未知外部结果），明确false仍保留模板fallback。旧普通调用共用协议发送实现，原测试同步真实一致appid，新增5项mock外部调用及3项真实DB验证（recipient2+type1）。无真实微信、付费模型或生产修改。
- wx-recipient-send-1/session60067在途，固定原task-scheduling-api0715d0cd6e；driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/wx-recipient-send-driver-1.py`，目标22项（wx13+原Kefu4+新Kefu5）和layering。后续先poll60067，不在原固定源码编辑/并发Gradle。task-scheduling-api-next在83256终态后ff到0715用于下一阶段源码，保持同一Owner。WxSchedule旧cron/DelayQueue尚待真正替换，素材scope、答题Redis关联所有消费者、deadline/receipt发送事务仍待完成；完整资金上线目标不缩小。
- wx-recipient-send-1/session60067终态PASS：0715d0cd6e7f886452fdd44b4552469f57f83fd1/tree2dad208ae70fc18f68aec0d4524567c84a321b39；独立XML回读22/22（Kefu旧4+新5、Key2、receipt MySQL5、subscription/type MySQL4、recipient MySQL2），0失败/错误/跳过、layering通过。墙钟661.904秒，真实MySQL148.066秒，其余513.833秒；临时取消时限有效，没有因超过10分钟重启。无生产变更。
- 完整Wx候选1807de23d4f514be88457c5a9f71113f71b8d331/treef0e6d776161d3d2161c9592f0f952ceb4ee79455已固定在task-scheduling-api-next：旧WxSchedule @Scheduled/Redis15min锁/DelayQueue/ThreadRequest全部移除；显式wx.daily-plan SKIP cron，按scope分页订阅，每订阅短事务冻结notice+登记task，重复计划不重抽随机截止时间，错过前日不补发。新增wx.daily-delivery从receipt原due恢复，发送前独立提交STARTED，结束另事务；过期/退订/无素材跳过，未知发送不重发，Redis答题指针失败不能改写已被微信接受的送达事实。尚未验证，不当成完成或发布。
- 实际素材依赖补齐：新MatPhrase/MatVote入口在DAO从进程配置取得tenant/admitted client，SQL先分区再RAND/LIMIT；已答题排除用精确scope/account NOT EXISTS，保留已授权questionId取选项，不全面改DAO。Webhook主动取题也调用同一已分区入口。答题指针所有读/写/条件删除及退订统一到WxDailyVoteKeys.answerPointer(appid,jiacn)，复用已有公众号身份+账号长度编码哈希，保留2h语义，不读旧owner-only key作兼容；旧key自然到期不批量删生产Redis。Kefu回执返回实际recipient appid供定时发送写同key。原13个Callback用例同步消费契约、新增key分区断言；旧starter真实发消息fixture改成仅注册cron（不在本次59项内，不冒充starter通过）。
- wx-daily-scheduling-1/session35768当前在途；driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/wx-daily-scheduling-driver-1.py`。固定读取task-scheduling-api-next1807de23d4，目标59项（前22+materialMySQL2+planner5+dispatcher14[8普通+6状态]+keys3+callback13）及layering/material服务编译。接续先poll35768，不编辑此固定源码、不并发Gradle。原task-scheduling-api仍0715、无在途验证，可在需要继续实现时安全ff后复用，不新增第三worktree。
- 本轮真实进展：Memory52通过、Wx基础10和scoped-send22通过，以及完整旧timer迁移/素材/答题关联候选提交并启动验证。后续仍需Wx真实同库计划+task原子性/重启集成、实际Redis与混合慢任务容量、Memory实际ES mapping/query；费用全目标的保留技能完整库存/首次费用与基础续租拆分/selfhost/30day过渡/释放再请入/原账号维护授权/桌面移动端/受控迁移与最终部署验收仍未完成，不能缩小为本轮59项通过即全目标完成。
- wx-daily-scheduling-1/session35768终态FAIL，墙钟309.987秒，尚无应用编译/测试通过；G1 layering拒绝两个新增生产文件的`cn.jia.task.scheduling.*`通配导入，而不是业务模块依赖方向错误。修正候选b7ca82a3239c0202693c7f2fb3dbc3dc6618a2c2/tree67b232464b410dd2b4b35b9da3e4d78825539970只把两处换成实际使用的9个明确类导入，不增加baseline豁免、不删layering、不删59项。原task-scheduling-api在验证35768读取另一工作区期间ff1807，35768结束后修复在此提交；没有覆盖在途源码。
- 当前失败矩阵：先前Memory collation失败已经由memory-scope-2的52项通过确认修复，Wx基础10及scoped-send22也独立通过；本次新增G1通配导入首次失败有精确路径、规则和源码修正，不是同输入盲重试。历史archive/Rabbit/Command/资金fixture失败的修正证据保留上文，不重标旧FAIL。编排累计失败将gate设为blocked_root_cause，沿已有authorize-remediation以本handoff解锁具体修正候选后再验证，不绕开门禁。
- wx-daily-scheduling-2/session15903当前在途，driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/wx-daily-scheduling-driver-2.py`，固定原task-scheduling-api b7ca82a3239c0202693c7f2fb3dbc3dc6618a2c2/tree67b232464b410dd2b4b35b9da3e4d78825539970，仍59项+layering/material编译；本次没有时限中断。另一本Owner工作区task-scheduling-api-next在35768结束后ff到b7ca82a323，用于真实同库接线验证，不能改在途原工作区。
- 新增待验证`WxSchedulingTransactionMySqlTest`（next工作区未提交）：生产task/notice DDL、实际ScheduledWorkStore/MyBatis/TaskTenantConfiguration/Spring事务与独立MySQL，4项覆盖同库计划+task提交/失败回滚及afterCommit唤醒、进程重建保留due、两个REPEATABLE_READ空快照并发冻结唯一原随机期限、provider看到已提交STARTED以及结果回滚后任务重领不重发。外部微信仍mock，未发真实通知。
- 接线推导发现实际快照问题：planner先find缺行，在同一REPEATABLE_READ事务内并发INSERT输家遇到duplicate后，原Jdbc receipt再普通find仍可能读到旧空快照。已仅把plan末尾返回获胜行改为current read `FOR UPDATE`，普通find不加锁；原唯一键/外部开始token/结果状态不变，不加轮询或补发。新增并发barrier测试强制两个初始空快照交错，待正式验证，不以推导当PASS。
- 对余下首费只读复核：HostingRentLedgerServiceImpl.quote仍直接用plan.amountWen，reserve同时把quote.amountWen复制给lease和initial intent，若只加技能费会让后续续租重复收费；必须在正式技能库存接入时一并冻结首期合计与基础月租并分离写入，不可只改前端展示。ManagedHostingProvisioner现有capabilities只有可用性/host，无完整公共技能库存协议；新增库存需事务外读取、冻结及Runtime按同快照确认，不可用journal历史版本数冒充已安装技能种类。当前未修改资金/Runtime代码，未扣费、未部署。
- wx-daily-scheduling-2/session15903终态FAIL，墙钟847.862秒，真实MySQL307.058秒、其余540.804秒；layering与应用/测试编译通过，实际执行50项中39通过、11失败（其后Kefu9因Gradle前置失败未执行）。独立XML确认11项全为旧Callback helper第91行同时stub缓存与fallback，缓存命中后fallback未用的UnnecessaryStubbingException；业务断言未失败。只移除这条无用stub，保留Mockito strict及显式fallback不匹配测试，不给所有测试lenient、不删13项。
- 新候选ea9784f708b981b2a038b507c9ee2856be906d45/treea12a5ade84b2b83f64c70edc792873dacd157262在next工作区已提交，除stub清理外包含真实同库4项和plan current-read修复；答题Redis指针补上可信进程tenant，避免不同环境复用同公众号/账号时碰撞。Webhook从配置策略取tenant、调度从可信invocation取tenant，适配器一次编码tenant/appid/account，所有生产者/读者/条件删除一起切换，不从外部body取tenant，不做旧key双读。现有Callback私有MySQL fixture补注入配置，但本批不启动其另需环境的测试，不冒充已跑该fixture。
- wx-daily-scheduling-3/session42735在途；driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/wx-daily-scheduling-driver-3.py`。固定next工作区ea9784f708，原59项全保留加真实同库4项共63、layering/material编译；临时无时限，继续串行普通磁盘。接续先poll42735，不在next编辑/不重复启动。原task-scheduling-api仍b7ca82a323且干净，可按需ff复用做下一工作；全部旧失败记录保留，未执行生产迁移、真实发送、扣费或部署。
- wx-daily-scheduling-3/session42735终态FAIL，676.795秒；54项52通过、2失败，Kefu9项未执行，layering通过。失败分别为异步派发拒绝时身份查询本就不应执行而fixture多stub（line92），以及真实MySQL调度重试使用旧规划clock而早于实际settlement。候选c1578b9c94仅修fixture：拆出account-only准备并新增无身份查询断言；用生产retryAfter按数据库结算clock重试，短暂等待真实due领取。保留严格Mockito、未知结果不重发和全部事务断言，不调整生产语义/时限。batch2原11项中10已通过，本批余1为另一未使用身份stub；前一findByKey修正不回退。历史失败与真实耗时保留，按既有矩阵恢复验证，不原样盲重试。
- 修正后的wx-daily-scheduling-4已启动session68404，driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/wx-daily-scheduling-driver-4.py`；固定源码见该批result.json（c1578b9c94），仍63项+layering。下次先poll同session，不改受测task-scheduling-api-next、不并发Gradle。原task-scheduling-api同commit可作后续writer。临时取消时限仅本任务，driver boundedLimitSeconds=null，真实失败不重标；生产未变。完整费用/调度/Runtime交接与上线范围不因本轮fixture修正缩小。
- wx-daily-scheduling-4/session68404终态PASS：APIc1578b9c947316f07f05615dd88dc2fdd772a7f0/tree0809776736200e8d3b4b0828c68840258a06bb7a。独立回读12份XML共63/63，0失败/错误/跳过；layering及Material编译通过。墙钟615.801秒、真实MySQL215.966秒、其他399.827秒；无600秒中断。新增真实事务4项均通过，证明同库原子计划/调度、双REPEATABLE_READ快照竞争当前读、STARTED已提交及结束回滚后不重发；生产无微信发送/迁移/发布。前3批失败原状保留，完整剩余范围不变。
- Memory真实ES验证下一候选：生产ES只读确认9.3.0；现行health credential没有临时index的完整写/管理权限，不扩权、不尝试修改生产。改用同已安装9.3.0二进制启动本任务独立loopback端口/config/data/log的临时ES节点，测试前严格核对专用clusterName/非9200，之后仅删除自建index并停自有进程。新增真实MemoryRepository/Java client测试覆盖实际1024维bbq_hnsw映射增量、128条异域/大小写/尾空格/无scope干扰记录先过滤后topK与100条摘要limit、精确count及按进程分区维护；Embedding仅本地固定向量，无模型费用。此项源码准备中/未验证，生产mapping不变，未把读取health视为迁移授权。
- 首次临时ES启动session13086在Gradle之前退出78：既有cyf-local-build父目录不可被isp遍历，应用本身未启动；日志和lifecycle保留memory-es-fixture-1。不放宽已有目录权限，fixture2改用本任务既有普通磁盘`/home/isp/state/cyf-test-tmp/memory-es-fixture-2`，仍独占config/data/log、isp用户，包外证据保留原任务目录。无需生产账号权限/生产配置变更；源码551f06fa0292facef7c5b129f7da6620cb052d02/tree1df8e30b6685c3883697dfc19e7af264927750af待验证。
- 下一接续先poll session87943：`memory-es-fixture-runner-2.py`监督本任务独立ES及随后`memory-es-driver-2.py`的10项真实ES/原scope单测+layering。当前已确认独立ES9.3.0进程1122236启动中，256MiB heap、ext4 data/log，只用既有二进制，未改变生产config/凭据/索引；runner终态finally仅停止自己新建进程组并保留lifecycle/server日志。受测工作区改为原`/home/isp/wsps/worktrees/task-scheduling-api`，HEAD551f06fa02（精确SHA上条），在途勿编辑；`task-scheduling-api-next`仍c1578b9c94，若下一阶段写入先核对干净再FF551f06fa02，不能反向覆盖。无第二个Gradle运行，Runtime源码仍未在本轮改动。task checklist已同步Memory52/Wx63真实结果但保留完整未交付范围。
- memory-es-fixture2/session87943终态FAIL：独立9.3.0节点正常启动并已finally停止（lifecycle确认），应用/分层通过；编译新增测试时发现锁定的Java client9.2.2 GetMappingResponse使用get(index)，无result()。javap已核实，只修该一处API调用，全部断言保留；该批无10项通过结论。Gradle批528.953秒，fixture独立启动约151.6秒，原失败保留。继续用同独立节点配置新批次验证，不接生产账号、不放宽映射/身份验证。
- 并行于Memory验证，在另一自有writer `task-scheduling-api-next`推进资金主线：增加冻结报价recurring_amount_wen并与first invoice总额分离；lease只承接周期额、intent/预占/实扣/退款保持全额，手动续租也仅写周期额，自动续费原消费者无需新增查询。6文件候选含fresh DDL、schema catalog、mapper、实体、业务及两项真实H2回归，尚未验证；完整Runtime库存/首费生成仍未接入，测试明确只验证资金边界，不把手工冻结fixture视作完整首费方案。原租约金额查读及锁序不变，无前端契约变化，无历史字段fallback/新增CHECK/生产DDL。
- Memory修正批session39164正在运行，driver memory-es-fixture-runner-3.py→memory-es-driver-3.py；复用确认已停止的独立ES2配置/data普通磁盘，批次2失败日志已包外留存。固定原API工作区6e5bb6df71，不编辑该受测工作区、不并发Gradle。
- 首单/周期租金分离已提交writer `task-scheduling-api-next`：c4ce0e9952实现、e5b09fdf3c补真实MySQL自动续费+fresh catalog、fcca6128c5在运行前审查修正充值fixture规范UUID。三新增用例明确不冒充库存定价：H2首单全额结算→手动续费只周期额，余额不足/失败全退，MySQL真实首单650/周期500→正常自动续费仅500且重复callback不再扣费。待执行driver `rent-recurring-split-driver-1.py`，92项（posting26+rent19+renewal47）及layering；当前Memory session39164占用Gradle，尚未启动该批，不并发。下一步先确认Memory终态，然后切ledger到fcca完整commit/tree再跑此候选；不要把92计划数写成已通过。
- memory-es3/session39164终态FAIL：全部编译/layering与原scope9项通过，真实ES1项失败。实际allocation explain（memory-es-fixture-3/allocation-observation.json）证实唯一NO为disk_threshold：普通磁盘4.7GiB可用但节点默认90%要求5.8GiB，首个新index primary未分配，保存返回真实503/unavailable_shards。不是身份query失败，也不重标成功。10项中9通过/1失败，Gradle批482.953秒；finally已删自建index并停独立进程。
- 下一fixture4仅在任务专用ES节点配置关闭disk-threshold allocation decider：本fixture为固定131条合成1024维文档，容量远低于现有4.7GiB；不改生产ES任何watermark，不清他人磁盘，不改变检索/隔离断言，configSHA进入原证据。复用已停ES2目录；业务源码仍6e5bb6df71，非同输入盲重试。首个fixture父目录ACL问题已解决，第二个client-getter已编译通过，当前根因独立为合成测试节点分配设置。优先完成实际ES再串行验证首单/周期租金92项。
- 2026-11-11接续：用户再次明确“临时取消时间限制”，仅本任务验证/构建/发布不执行600秒中断，继续保留实际阶段/墙钟耗时、失败、锁与恢复保护；不改项目长期规则/共享技能。已核对原API固定6e5bb6df71/tree f58c46ef07c8da946a2bf229b1d5156452dce496，恢复targeted_verification并启动memory-es-fixture-runner-4.py，session65997；仅专用测试ES关闭分配磁盘水位判断，生产未变。租金92项仍未启动；待ES终态及XML独立核对后串行执行a009217423候选，不编辑在途受测源码。
- memory-es4/session65997终态PASS：API6e5bb6df71a918d355719db418615d1e5b5940be/tree f58c46ef07c8da946a2bf229b1d5156452dce496，独立回读XML确认scope9+真实ES1共10/10，零失败/错误/跳过，layering通过。Gradle批411.461秒，含独立节点启动/退出墙钟572.744秒。lifecycle证实仅自有进程已退出；生产mapping未迁移。旧allocation FAIL保留。本结果验证真实先分区再KNN/topK/摘要limit与维护范围，不代表生产迁移完成。
- rent-recurring-split-1已启动session7663；固定next工作区a009217423339f6f8cec26db4378b6738c4176ed/tree99636872364e2e53f250348764240ce9fc2a144e且启动前干净，预期posting26+rent19+renewal47共92及layering。下一接续先poll7663，不修改受测next工作区、不重复运行或并发Gradle。完整首费库存/生命周期/迁移/发布目标尚未完成。
- rent-recurring-split-1/session7663终态FAIL，351.028秒；layering/编译通过，实际45项28通过17失败，后续MySQL47未执行。独立XML证实posting26通过、rent19中17因H2简化建表缺少既有生产handover_id/executor_stopped_at列而查询失败。修正2687dc4e9b仅同步这两个nullable列和生产类型，保留原资金/并发/幂等断言，不修改生产业务。前Memory磁盘水位失败已有ES4真实10项PASS修复证据，不与此新fixture根因混为重试；原全部FAIL保留。沿既有矩阵恢复此次固定修正候选验证。
- rent-recurring-split-2/session79771终态FAIL，1087.365秒；独立XML确认92执行91通过：posting26/rent19全通过，MySQL47中46通过。上一H2缺列问题已修复。唯一失败为新用例把真实leaseId传给旧seed专用helper（内部拼接agent-前缀），实际canonical Agent因此查询null；资金断言尚未执行到后半段。8803d6a393仅改为冻结报价真实agentId查询（两处），保留全额首扣/续租500/幂等/余额/借贷平衡断言及92项，不修改生产行为。原FAIL保留，不重标通过；继续第三批验证。
- rent-recurring-split-3/session33881终态PASS：API8803d6a39399b4dd356d28f82c09d0a7cf8e10d8/treeb5867002a481126760a51197fd333dbba86bc56a。独立回读3份XML：posting26+H2 rent19+真实MySQL renewal47=92/92，零失败/错误/跳过，layering通过。墙钟661.588秒，其中真实MySQL285.169秒、其他376.416秒；临时取消时限已生效，未因600秒中断。首单650/周期500真实预占/扣款/后续自动续租/重复callback/余额50/分录平衡测试通过；该用例仍只证明资金消费边界，不冒充完整公共技能库存生成报价。前两批失败和修正分别保留。
- 当前没有在途验证进程；下一步继续完整首费库存与确认快照、selfhost50/已有部署过渡、释放再准入/原账号维护、统一调度慢任务与资金容量、生产ES迁移、桌面移动端及最终集成/受控发布。API原worktree仍6e5bb6df71，next固定8803d6a393且干净；两者都未部署，未操作生产迁移/真实扣费/模型调用/微信发送。可按干净检查将原worktreeFF到8803复用，不创建第三份。Runtime仍b970258db0e641318bc201f068c66ac5efb002a0，历史独立工作区脏修改继续保留。

### 2026-11-11 首费库存接线推进（未上线）
- 上轮分类为progress：ES10、资金92获得真实通过证据。当前完整目标不变，继续库存→冻结报价→确认/结算，不缩小为单独库存接口。
- Runtime新增原生公共库存读取：`conf/codex-bridge/skill-inventory.mjs`使用现有完整性核验AppServerAdapter的catalogOnly初始化，仅skills/list(forceReload)，不读取account/model/MCP、不建thread/turn/不调用Provider。复用当前安装journal补齐禁用管理技能，不含已删除/历史版本和system工具；原生引擎解析手工/项目/插件元数据，不写另一个受限YAML解析器。只回传skillKey/source/revision及排序摘要/字符串计数，不泄露本机路径、正文或凭证；未知/发现错误/同名冲突/安装中变化不当零。原生revision为SKILL.md定义摘要，管理revision包含安装ID/包树/版本/启用状态。HOME为Agent的HOME父目录，不继承服务账号的私人HOME。
- `hosting.inventory`加入原受控UDS契约，按可信scope+canonical Agent解析同host的既有静态/托管profile；新受限model-only模板尚无HOME/work/技能时仅返回空库存，不提前创建实例。原subject门、权限与进程退出证据保留；不恢复旧技能执行协议。API2339eb48e6已新增对应provider读取及摘要/计数/作用域验证，null表示未知，不默认为0；API报价业务尚未调用，未收技能首次费用。
- 轻量诊断`skill-inventory-1/node.log`实际原生5项等42项通过、2项旧UDS用例因过长TMPDIR导致Unix listen EINVAL失败，保留原FAIL。不是业务协议错误；随后正式源快照复用既有`runtime-handover-1/source`，短普通磁盘TMPDIR sinv2，不改socket权限/保护，不用tmpfs。
- Runtime faa0b322da053800034371a8d1c6f763f9f76092/treee136f63cbe8f2234c0c82e96f843806d44e6434f（1.3.93/bridge1.1.68）`skill-inventory-2`167/167 PASS，零失败/错误/跳过，墙钟484.393秒。含原生实际初始化、实际普通/项目/合法folded YAML/禁用native发现、管理journal完整历史/退款/退休/不可变包、原有AppServer流/关闭及hosting控制。实际冷启动35.013秒，无模型调用；不把mock discovery当真实引擎。证据固定完整commit/tree、依赖树摘要及Node24.22.1。
- 后续Runtime7204b704a487dd0856d15e4391552680faafcef8/treeb86adb3d11de8f5b45e7632c332c617da5ed776a只增加跨语言fixture与测试（生产源码同faa0），`skill-inventory-3`40/40 hosting控制 PASS，墙钟18.074秒，包含真实UDS库存与共享Unicode摘要fixture。已有API/Runtime fixture逐字同源。原Python freeze等他人dirty文件未提交/未纳入干净测试快照，未覆盖。
- 接线前定位到真实延迟问题：原控制探测默认2秒/配置上限20秒不能承载实际库存冷启动35秒；API1eeef3b63c新增operator-only inventoryTimeoutMs默认60000（按上述实测），仅库存RPC采用，快速控制不变，不把构建时限传给业务。API7c2ae8aa35追加真实Java→UDS→原生引擎库存断言，既有fixture显式测试二进制/合成HOME且无Provider，确保不是仅两边codec各自PASS。
- 当前session65785在途：`skill-inventory-api-driver-1.py`固定next工作区7c2ae8aa35（完整SHA/tree在该批result.json）、Runtime干净快照7204b704，20项及layering，显式启用已有真实Java/Runtime fixture和实际原生库存；Java和Node临时目录统一短普通磁盘sinva1。下一接续先poll65785，不改next/Runtime快照、不并发Gradle，不重复启动。API完整首费生成/冻结/确认、权益/自部署/过渡、混合容量/最终迁移发布仍未完成；生产没有变更/真实扣费/微信或模型调用。
- skill-inventory-api-1/session65785终态PASS：API7c2ae8aa35e634b76a6ec40955babb0acb58a198/tree077f7d4a5e1a58e82989dabbffd613d6bf6e2c1d，Runtime7204b704干净源快照。独立XML确认20/20零失败/错误/跳过，layering通过；真实Java→UDS→HostingControl→原生AppServer skills/list验证普通及禁用技能2种、新实例库存0、原生命周期回放/停止/清理均通过。全批560.982秒，真实跨边界该用例36.197秒（XML）；复制的driver只识别MySQL timing事件，result.regressionSeconds=0并不表示没有集成回归，不将真实36.197秒重标单元测试。共享fixture两端SHA256=33a9e543808df8765b6e2e298bb4e3f86c0d210f468223832b9e34d57b1ec01a。没有在途进程，仍未上线/调用模型/真实扣费。
- 接续风险调查（不得误称已实现）：`SkillManagementService.origin/validInstallation/qualifies`仍将安装授权绑定原change.owner与原Runtime installation；`agent_skill_installation_authorization`主键仍tenant/client/installation_id。Runtime的admitRetiredRelationship已保留public installation ID并换私有身份，但API不能仅收首费就自动复用旧owner授权；也不能伪造INSTALL/APPLIED或复用历史adoption迁移来授新权。本次inventory目前仅skillKey/source/revision，足够计数/报价变化判断，但新关系资格还需要保留管理安装身份/公共版本证明，并在唯一技能授权责任层落实新租约/付款关联，旧授权/历史事实不可被覆盖。此为总目标已有“新关系资格”实际代码缺口，非新需求/新增审批。
- 下一具体动作：先扩充管理库存行的公共安装/版本引用及跨语言fixture（原生非管理技能不虚构市场安装），沿真实授权调用链确定公共安装与关系权益分离；然后冻结首期库存/总价与基础周期价到原quote，外部库存读取放在短事务之外、确认重放优先，确认库存变动拒绝新预占；资金92原通过证据保留且补实际生成首费回归。再完成selfhost50/旧部署过渡、释放再准入/原账号维护、混合容量、生产ES/数据迁移及Web/完整发布验收。可继续复用原API worktree（当前6e5bb6df71，先clean再FF）作为writer；next为上述7c2ae8aa35。Runtime源7204b704，已有他人Python/install等dirty不动，正式snapshot在runtime-handover-1/source且无在途读取。

## 接续：首次技能报价回归收口（未编译候选）
- 上轮为任务临时时限例外的持久化；本轮实际推进测试与契约，未开始构建、生产迁移/部署/扣费。当前API仍HEAD7c2ae8aa35，Runtime仍HEAD7204b704，新增修改未提交，不能复用这些HEAD的旧PASS为当前证明。
- 两端hosting-inventory-v1 fixture同步enabled及managed installation公开引用，重新计算Unicode规范JSON摘要；逐字节/摘要检查通过。Runtime skill-inventory.mjs仅node --check通过，非运行测试。
- 修复UnixManagedHostingProvisioner.decodeInventory新增snapshot JSON序列化未在受检异常捕获内的问题。
- H2首次费用测试由手工插入加价报价改为真正ledger.quote(count=3)，断言首费、基本月租、清单持久化与幂等；MySQL自动续租测试同样用真实首次报价产生650文，保留续租500/余额50断言。其他初次/续租构造参数及H2四个清单列已更新。
- Application测试补无事务inventory替身、冻结空清单、receipt新字段及原控制不可用场景；新增清单摘要/主机变化拒绝确认且不预占用例。尚未编译/执行，不声称PASS；仍需非空报价breakdown、观察期间关系变化/并发成功重放覆盖与完整diff审查。
- 下一步：核查API所有新构造调用与schema手工fixture、Runtime managed metadata实际来源及template/orphan可用性，补测试后固定候选；读build.gradle并复用现有串行driver验证。无在途构建/测试句柄。其余技能新关系授权、selfhost/过渡、混合调度容量、生产迁移及全链验收等仍未完成。

### 固定首费候选与在途验证
- API候选d3c8648aeae06ea9380973d1d7a8a6e8cd9f30b4/tree dd5aca5cde7d8ca552ee14a572f157a639b7542c，工作区干净。补非空/禁用技能清单传递与费用分项、观察期间owner变化拒绝、控制不可用时并发成功确认重放测试。`first-skill-fee-driver-1.py`已启动，session **37227**；预计114项（原92资金/真实MySQL+Application22），另layering。本批未结束，不能视为通过；接续先轮询此句柄，不重启。
- Runtime候选b18f8b68e5912e20e2917dbfbc4c3c231243080c/tree415899348b4119330183a95b267e453c98797ddd，只提交本任务5文件，保留其他脏改。补inventory模板workspace policy有效性；未知subject但已存在root拒绝零报价，避免把孤儿数据当空清单；managed字段直接来自原SkillInstallManager._descriptor，不造安装事实；要求enabled明确布尔值，补metadata与orphan/policy回归。
- Runtime尚未运行新测试；已准备`skill-inventory-runtime-driver-4.py`（输出skill-inventory-4、短磁盘tmp sinv4），须待当前Gradle结束后串行启动，复用干净snapshot，不并发重载它。该批应167旧项+2新增=169项；真实native发现无provider/turn调用。
- 新查Web的HostingRentPanel仍含“仅手动续租”“自家接应不收托管租金”旧口径，未修改产品/原型；必须在报价分项及自托管接入时一并按固定30天/自动续费规则收口，不能宣称当前Web已符合。保持原型先行与既有单一原型目录。
- 在途分项回读：first-skill-fee-1资金H2的两份XML已生成（以XML结果为准），API/Agent后续仍在编译/运行；不可提前宣称整批114项或layering通过。费用合同已补公开清单字段、事务外观察、报价分项、确认前摘要检查及新关系权益未完成边界；不冒充已上线。下一接续保持session37227，不启动第二个重型验证。

### 首费第一批终态与修正候选
- session37227已终止FAIL；first-skill-fee-1固定d3c8648a，墙钟874.162秒，实际114项/6失败（Application22中4、MySQL47中2、H2账务26+租金19全过），原日志/XML保留。不是超时/OOM。归因已通过orchestrator fail登记`first-fee-fixture-and-catalog`。
- 具体根因：测试inventory默认answer调用另一个mock.available，随后when重设触发Mockito嵌套桩；新测试给500计划与本类配置1e9冲突；schema catalog的column helper只给varchar带collation，新char/longtext实际也有utf8mb4_0900_bin。修复不削弱身份/金额/目录断言。
- 沿调用链发现另一个真实遗漏：EconomyOperationWire对外QuoteView没有新增首费明细。已同步投影，并扩展原真实MVC边界测试断言3字段及原时间/身份规则，加入既有managedHostingRegression source set；另同步HostingRentHttpTest构造调用。
- 修正API候选e309bc6abe05e1b44bb1dd81ad97bb623f459df9/tree0fcef1028c6dc65db3f65171cc7a0011ec0f1655，尚未测。已准备first-skill-fee-driver-2.py，预期117项；必须等Runtime当前测试终态后启动。orchestrator累计旧失败触发root_cause_matrix_required，重试前依据本归因/实际修正执行authorize-remediation；不是同输入盲重试。
- Runtime `skill-inventory-runtime-driver-4.py` 已启动，session **11121**，固定b18f8b6；当前唯一在途重型验证，接续先轮询。未启动第二批Gradle。
- 单一原型目录的baseline-ui.js“ui-hosting”弹窗已加650=500+3×50文分项、30天自动续费和欠费收尾说明；prototype-spec同步，node语法检查及既有18786服务HTTP内容读回通过。只改命中行/追加规格，保留原脏修改；尚未浏览器PC/手机验证，Web产品未改。
- 已authorize-remediation固定e309bc6；第二批driver进一步合并UnixManagedHostingProvisionerTest20项，最终预期**137项**（117+20）+layering；显式绑定Runtime b18f8b6 clean snapshot、跨端fixture与短磁盘UDS路径，实跑Java→UDS→原生inventory，不另开重复编译批次。待session11121终态后执行；尚未启动。前述117是扩展前计划，不是执行结果。

### Runtime终态与API第二批在途；真实原型入口核查
- Runtime session11121已终止PASS：skill-inventory-4固定b18f8b6/tree415899348b4119330183a95b267e453c98797ddd，679.613秒，TAP实际170/170、0fail/cancel/skip（前述169为计划估计，以真实TAP为准），覆盖实际native inventory、安装/交接、hosting控制。未部署。
- API second batch `first-skill-fee-driver-2.py`已启动session **41430**，e309bc6/tree0fcef1028c6dc65db3f65171cc7a0011ec0f1655，预期137+layering，实Java→UDS→native fixture，暂无终态。接续先轮询；不可重复启动或改源码。
- 原型真实浏览器：复用已有CDP harness和普通磁盘profile，不装依赖。系统完整Chromium启动不提供CDP（first-fee-prototype-1 FAIL保留），旧/usr/local/bin/chromium-headless-smoke指向已不存在缓存；实际可用为/usr/lib64/chromium-browser/headless_shell133.0.6943.141。第二批浏览器可用，但旧ui-hosting入口已被现行renderRuntimeCatalog覆盖；诊断证明不是API/付费问题。
- 已将现行complete-runtime-hosted入口与旧ui-hosting统一调用showHostingQuotePreview，更新唯一原型同目录及规格，不另做平行页面。first-fee-prototype-3 PC/390手机两端PASS有截图，17.069秒；看图发现语义按钮转换造成重复关闭图标，已去除多余footer，保留原header关闭。
- 去除footer后的prototype4等待dialog失败，未伪报通过；prototype5增加document.readyState完成后再点击，并收集Runtime异常用于归因，session **67371** 在途。若再次失败须检查result.exceptions/diagnostic，不盲重试。当前Web产品仍未改。
- 前端真实调用链发现另一个关联遗漏：HostingRentPanel.timestamp仍仅接收decimal字符串，而EconomyOperationWire明确输出数值epoch；需改成规范数值时间展示并补测试。首费分项将直接展示API结果，不在Web重算50文定价；HOSTING_RENT_QUOTE_STALE需作为明确无新预占拒绝清除原报价并引导重查，不能当未知结果无限重放。历史已提交确认的原key/金额恢复不能因新增展示字段被抛弃。
- prototype5最终当前源码PC/手机PASS，23.073秒；有desktop/mobile截图与源文件/浏览器摘要。prototype4的点击早于document ready，补页面就绪条件后同实现验证成功；旧FAIL保留。当前无在途浏览器。
- Web工作区task-scheduling-web新增未提交候选：费用总额/正常租费/已有技能数/首费分项、自动续费说明；去旧自托管免费说明；数值epoch日期展示；QUOTE_STALE明确无新预占处理，保留旧已提交operation恢复规则，不为新增展示字段否定旧key。新增UI分项/有效期/取消不收费测试及清单过期后允许用户重新预览、不自动重扣测试。尚未执行Web测试，不称通过；待API session41430终态后串行跑，当前只有API在途。
- **接续重要：session41430的driver父进程返回143，但Gradle实际仍在运行，不能重启。** 已核验orchestrator PID1197950（PPID1）、Gradle daemon1198037仍活，日志推进至point API编译（约468秒）。first-skill-fee-2/result.json仍RUNNING是父driver未收尾，不是子任务终止证据。后续按PID归属/日志持续核验，等待orchestrator的真实GRADLE_EXECUTION_TIMING和XML，再单独写supervisor-interrupted审计；不要伪造driver正常退出/重跑。原因待查，尚无OOM或预算超限证据。当前API固定源码仍不能修改，也不要启动另一重型验证。

### 2026-11-11 接续：首费API终态与真实产品浏览器
- 已重新按PID/日志确认原first-skill-fee-2子进程结束，未重复启动。Gradle真实exit0、986.901秒，137/137且0fail/error/skip、validateLayering通过；独立核对6份XML（账务26、租金19、真实MySQL47、应用22、HTTP3、真实UDS/native20），API仍e309bc6/tree0fcef102且干净。父driver143原因未知，原result.json RUNNING/日志保持不改；另存`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/first-skill-fee-2/supervisor-interrupted-audit.json`，不冒充driver正常结束。
- Web `web-first-fee-1/driver.py`复用原依赖/测试工具，7ec2dbe固定输入55/55通过，69.764秒；覆盖报价controller、实际Vue组件、文案及自部署接入现有测试，未做生产构建。临时取消时限仅当前任务，实际耗时保留。
- 新增可重复运行的`web/tests/hosting-rent-browser.mjs`：复用现有Vite+Vue+CDP工具，实际HostingRentPanel/useHostingRent/capability decoder，仅HTTP及认证store使用合成fixture。桌面1440、手机390及窄屏320验证650=500+150、数值时间、无横向溢出、预览/取消不确认、库存过期拒绝不盲重试、显式重查再预占（新幂等key及650文/30天原字段）。不声称是真API/生产扣费验收。
- 浏览器首批FAIL是测试fixture给只读Window.closed赋值，原证据保留；只修fixture为panelClosed，非生产代码问题。当前Web5f63606fec8375e3d104a122f49916abc5a6bf64（后两个commit仅新增/修正浏览器测试，产品源与55项输入一致），`web-first-fee-browser-2/result.json`16.894秒PASS，3尺寸截图和源摘要齐全、0Runtime异常；人工看过mobile.png，按钮/金额可见。浏览器/Vite已结束，没有遗留进程。原型PC/mobile通过仍只证明原型，未混入产品证据。
- 未做生产安装、迁移、实际付款或Provider调用。剩余新关系技能授权、自部署/存量过渡、完整同实例再入会、认证/调度容量/Redis恢复、生产映射及打包上线范围不缩小。
- 继续核查发现后续落点：现有SkillManagementService的origin/validInstallation及多个消费者绑定旧change owner、旧runtime installation，不能只改首费数字就授权新关系。HostingRentReconciler.settle中已有binding→intent→lease→账务同事务入口，可接新关系授权；不能覆盖原安装授权/伪造APPLIED/adoption证据。HostingLeaseChangeListener合同只允许登记调度，不把复杂技能授权塞入其回调。Runtime prepare目前未携带报价库存摘要，确认后到异步prepare之间的最终库存闭合仍待完成；不得据此次137项称该竞态已覆盖。
- 已核对7ec2dbe→当前5f63606全部diff仅新增browser脚本，原明确Mocha selector及其源/fixture/依赖输入未变；55项精确复用说明保存`web-first-fee-browser-2/unit-evidence-reuse.json`，原测试结果不改写。当前tree099ef69ad0e9580b85ecb029450503ab18aa4294。当前没有在途测试/构建，可继续修改API，无需等待旧143 wrapper。

### 2026-11-11 新关系保留技能授权候选（验证在途）
- API598408aa43候选：不加派生授权表/伪造安装订单。SkillRelationshipAuthorizations从当前绑定的已扣款INITIAL及其原冻结库存解析当前关系权益；原安装授权/command/receipt仍只作不可变公共安装来源，关系主体及Runtime fence来自当前绑定。普通续租不替换原首期来源，单纯预占不可授权，关系解除即不可读取该来源；native技能不发明marketplace ID。
- 当前接线到管理source、目录/描述符、推荐、W05资格及native/executable admission。目录/推荐每Agent加载一次；无技能/租金schema关闭跳过空查询。新会话不驱动旧关系command的capabilitiesChanged；技能总览latestChange按owner过滤，不泄露前任私有变更。
- 测试补付费库存解析、禁用技能/原生技能、精确引用及缺付款拒绝；真实MySQL以原生产DDL和真实原安装过程验证新owner描述符、新Runtime准入/停用和历史授权不变。租金capture在本测试为明确fixture，真实资金事务另有首费137/租金92证据；没有伪称此批完成同Runtime交接全链路。
- `retained-skill-driver-1.py`已启动session **30660**，独占当前Gradle，接续先轮询，不修改受测API。包含validateLayering、SkillManagementTransactionTest全类82、Recommendation10、新单测4、新MySQL retained*3（预期99项；driver当前粗略数量阈值误写100，若仅此审计失败需依XML单独更正审计，不为计数重跑）。临时取消时限仍有效，磁盘tmp固定`/home/isp/state/cyf-test-tmp/retainskill1`；不生产部署。

### 2026-11-11 接续：临时取消时限与首轮失败归因
- 用户再次明确“临时取消时间限制”，仅本任务生效，继续记录实际耗时与失败，不改变资金、授权、锁及可恢复安装要求。
- retained-skill-1 已终止FAIL，457.897秒；不是计数阈值问题。编译发现SkillManagementTransactionTest的三个outbox mapper调用缺少调度改造后的processClientId参数，测试尚未执行。原日志/result保留；修正fixture传入ACTOR.clientId，不放宽生产隔离。新批次同时修正预期99项审计阈值。
- 修正已提交API `a743c77618`；第二批 `retained-skill-driver-2.py` 正在运行，session **78854**，输出 `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/retained-skill-2/`。没有600秒终止条件；先轮询终态，不修改受测API、不启动并行重型任务。当前不代表验证通过或上线完成。
- 第二批已终止：1606.630秒，99项中96 PASS/3 FAIL；失败均为新MySQL fixture按首个分号截取DDL，撞上真实persona_binding列注释中的分号。原结果未重标。API `abb9fd9722`改用既有集成fixture的`;\n`语句边界，另外补不同buyer/owner的新关系准入及停用、旧owner拒绝回归；生产源码没有变化。
- 精确diff只有RetainedInventoryMySqlTest；第二批82事务+10推荐+4权益单测的XML、摘要和新候选绑定保存在`retained-skill-2/unchanged-suite-reuse.json`，不复用失败的3项、不重复整个82事务套件。第三批`retained-skill-driver-3.py`运行session **18616**，只跑4项retained*及validateLayering；输出`retained-skill-3/`。先确认终态再修改API。
- 只读核查确认最终prepare库存闭合仍缺：Runtime prepare只持久化原association，API Preparation不带冻结库存；不能把确认前inventory查询当成异步prepare最终校验。后续应在同subject串行边界核对冻结摘要并持久化精确操作结果，处理丢响应重试，保留UNKNOWN与确证无副作用的区分；尚未实现或验收。
- 第三批571.912秒：原3个SQL场景PASS，新增different-buyer场景FAIL；原因是测试切换owner后仍通过旧ACTOR调用私有change读取，服务正确拒绝RESOURCE_NOT_FOUND。第四批460.543秒：修正为转移前冻结DTO后，继续暴露继承proof()仍使用旧owner，服务正确拒绝SKILL_AGENT_OFFLINE。两批真实失败保留，均未放宽生产权限。
- 当前API `39012a9d13`仅补fixture当前owner的注册session证明（初始安装时仍为原owner），新增测试也显式验证前任不能再读取变更。第五批4项SQL+layering已启动session **70714**，输出`retained-skill-5/`；先轮询，不能在活跃验证时改API。本轮仍没有生产操作。
- 第五批终态PASS，443.254秒，4/4 SQL回归、validateLayering通过。当前API `39012a9d13ddfb9cdcf495992686288e195b3561` / tree `31615f12394ae1e21b1286b33bb8b8318b447b05`，工作区干净；无在途Gradle。不同buyer/owner准入与停用、前任读取/准入拒绝、原授权不变已实际通过；原生技能及管理会话仍用可信fixture，不能宣称真实生产认证/全Runtime重邀已验收。
- 经完整diff和XML摘要重新核实，第二批三套96项受测产品源码/fixture未变（仅第四套SQL测试文件修改），精确复用审计更新到`retained-skill-5/unchanged-suite-reuse.json`；合并100项范围及边界在`combined-verification.json`。所有原失败批次保留原状态，没有重新标成PASS。
- 下一动作：完成Runtime prepare与冻结库存的最终闭合（API/Runtime共同合同、同subject串行核对、持久回执与丢响应恢复），再补升级/全同实例关闭重邀、自部署和存量过渡、调度容量及生产发布范围。当前只有定向功能验证，不满足完整上线验收。

### 2026-11-11 冻结库存与Runtime prepare闭合（实现完成，API验证在途）
- Runtime候选`456fe04856cf9d1140de25558f7d736129213054` / tree `4ca3fd6af424ab8c26088b5e52193ade1540cc83`，版本1.3.94：INITIAL prepare携带`quotedInventory`，复用subject门和库存观察；成功/库存不符均在原operation journal记录，不新增账本或调度器。库存不符为candidate=null的持久拒绝，重启、重试和库存恢复都不能把原intent改成可执行候选；缺失观察/写盘失败仍未知。原已准备关联不补造新库存事实，生命周期请求不传播报价字段。
- Runtime `prepare-inventory-runtime-1` 67/67 PASS，90.051秒（测试本身87.850秒）；包含库存、控制、真实UDS、真实执行适配器同根重邀、生命周期，以及持久拒绝/重启/成功重放不重观察/缺失quote/写盘失败等。原生发现部分真实、重邀test的native catalog显式fixture，原skill manager及磁盘仍真实；不声称生产API重邀验收。复用已有干净snapshot，无新worktree、无付费调用或生产变更。
- API候选`9650453056`：从原quote只读投影拿host/digest（不在intent/lease锁后新增quote锁），传入prepare；严格接收绑定原报价/关联/host的FAILED_NO_EFFECT，既有ledger负责释放全部首次预占，UNKNOWN不退款。原库存传输timeout同时用于带quote的INITIAL prepare（含真实库存读取），ensure/observe/正常reprovision不延长、不下传构建deadline。
- 两端共享`hosting-inventory-rejection-v1.json`，历史frozen fixture字节未改；新测试显式扩展prepare。新增真实Java→UDS拒绝重放与无credential产生、真实MySQL650文整单退款幂等及scope投影验证。
- API `prepare-inventory-api-driver-1.py`已启动session **68822**，固定Runtime snapshot上述456fe04，目标88项（Reconciler18、Unix22、RenewalMySQL48）及validateLayering。输出`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/prepare-inventory-api-1/`。接续先轮询，不改API或被Java fixture引用的Runtime snapshot，不启动并行重型验证。
- 上次retained-skill 100项是原39012a9候选证据，本轮API/Runtime改变后不冒充完整新候选验收。完整待办仍含同实例真实API交接、升级/自部署/存量过渡、认证/调度容量/Redis接管、生产映射和最终上线。
- 在本批验证期间只读追踪真实退款调用链发现额外必修缺口：`HostingRentReconciler.settle(false)`调用`ManagedHostingCredentials.disableForRefund`，后者仍强制要求legacy managedApiKeyId；新的库存拒绝发生在创建Runtime candidate/credential之前，Runtime installation/manifest及managed key应为空，runtime_provision_generation应为DDL默认0（不是null），此路径当前会回滚退款。不能把新ledger独立退款测试或mock credentials的Reconciler测试当完整退款闭环。待68822终态后，在既有凭据责任层区分“确无签发关联”与“已有legacy key需精确撤销”，任何已签发Runtime仍不得猜无副作用；补真实协作者串联和无签发/错误关联反例。当前API批次继续保留原候选，不中途修改。

- 2026-11-11接续收到用户“临时取消时间限制”：仅当前任务继续取消时限，真实计时/失败证据照常保留，不扩大生产授权或取消资金、身份、锁与恢复保护。已轮询68822确认仍在运行，driver boundedLimitSeconds=null，不重启、不修改受测源码。

### 2026-11-11 接续：库存闭合验证终态与真实退款链修复
- 上一goal轮为verified wait：多次轮询68822及原PID1255515存活，未重启或中途修改。现68822真实exit0，`prepare-inventory-api-1/result.json`为88/88 PASS、0fail/error/skip，905.413秒，validateLayering通过；绑定API9650453056b620cf4f648a8f2b3e10aa5260fc02/tree6c181706af4800a4c7136e19899fec51e31c421a及Runtime456fe04。没有把该结果当尚未修复的完整退款链证明。
- API新候选2751453c8e：在ManagedHostingCredentials原责任层接受`FAILED_NO_EFFECT`且未签发（installation/manifest/key为null、generation=0）；不再索取不存在的旧key。实际存在的旧key仍精确撤销；已签发/残缺Runtime关联、未知结果、无事务、错误scope不走无凭据退款。没有新增兼容层/查询/表。
- 将原ledger独立库存退款测试升级为真实Reconciler→ledger/posting→credentials及MySQL事务串联，真实identity/binding读取；外部Runtime响应和登录身份解析为显式fixture，实际UDS证据另有Unix测试。验证650文整单退回/重复派发不重退/无租期；新增已签发关联回滚真实账本、UNKNOWN保留预占。凭据单测覆盖默认generation=0与异常关联，不把null当未签发。
- `unissued-refund-api-driver-1.py`已启动session **73530**，输出`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/unissued-refund-api-1/`；56项（Reconciler18、Unix22、Credentials13、定向MySQL3）+validateLayering，无时间截止，普通磁盘tmp`/home/isp/state/cyf-test-tmp/urefund1`。接续先轮询，不改API或共享Runtime snapshot，不并行重型测试。尚未通过、尚未发布。
- 完整余项仍保留：实际同实例关闭→报价预占扣款→新关系重邀/升级、自部署50文及存量30天过渡、原账户停用收尾认证、统一调度混合容量/Redis恢复、生产映射迁移和最终打包上线。只读确认AgentController local/default仍绕租费；ScheduledJobRunner所有handler共用一个Semaphore，慢Memory/Wx占满时会延迟租费，不因本轮退款修复视为已闭合。

### 2026-11-11 退款链通过，继续交接后费用验证
- 上一goal轮为progress：API2751453c8e实现无签发退款并启动56项串联验证。本轮已确认73530真实exit0；`unissued-refund-api-1/result.json`为56/56 PASS、0fail/error/skip、validateLayering通过，751.342秒（真实SQL90.016秒；其余661.321秒），绑定tree ae9da38ef0cee6431fab7eb808824e089bbeb6ab。临时取消时限继续生效。真实Reconciler/资金/凭据协作者650文退款、已签发回滚、UNKNOWN保留均已通过，仍不是完整生产重邀证明。
- 新候选API41b8b2faef仅扩展测试：MySQL实际拒绝退款后显式新报价700文、报价本身不预占、新确认幂等且原失败intent不可复活；保留技能不同buyer/owner的20文升级，重放确认/APPLIED只扣一次，原钱包/原授权不变，新安装只向新owner准入。原租金首期capture为该技能fixture的明确合成事实，升级订单和扣费是真实服务/SQL；不冒充全流程跨Runtime证明。
- 复用已有driver启动`handover-fee-api-driver-1.py`，session **65177**，orchestrator PID **1272346**。普通磁盘输出`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/handover-fee-api-1/`，tmp`/home/isp/state/cyf-test-tmp/handoverfee1`；固定API候选，目标1项退款后重报价SQL+5项retained* SQL、validateLayering。无并行Gradle、无强制截止。先轮询终态，不能修改受测API。
- 下一实现范围保持原完整待办，不因新增测试缩小上线目标；需要继续处理同实例实际API/Runtime交接、自部署与存量过渡、原账户停用时的受控维护认证、统一调度混合容量、Redis接管/生产迁移/发布。当前只读确认HostingRentOwnerResolver.requireOwner与AgentRuntimeAuthenticationService.account仍依赖isAuthenticatable；维护链不能通过放宽所有用户/执行认证解决，须在原维护边界闭合并保留authEpoch/精确原关联。
- 同期只读联动核查发现Web真实缺口：当前hostingRentContract.validLease只识别PROVISIONING/ACTIVE/REFUNDED；lookupNotOlder禁止ACTIVE→LOCKED/FINISHING与LOCKED→ACTIVE；API lookup也将LOCKED/FINISHING统称PENDING。这会使真实到期状态被前端当异常，不是仅文案问题。必须在租约查询合同与对应Web消费处闭合，不改事项执行入口。
- 已先在唯一原型`/home/isp/wsps/cyf/web/prototypes/juyiting/baseline-ui.js`与其spec补rent-locked/rent-finishing/rent-active三个离线状态，原样式/弹窗，无新付款入口；node --check通过。浏览器driver已复用准备于`rent-lifecycle-prototype-1/check.mjs`，尚未执行。等待65177终态再串行验证原型，之后才能修改产品界面；当前没有把原型当产品完成。

### 2026-11-11 接续租约生命周期显示
- 上一goal轮仅确认取消时限并读取状态，属于no progress；本轮已重新核对API三项未提交改动、Web基线及原型真实结果，继续实现而非等待审批。
- 原型`rent-lifecycle-prototype-1/result.json`确认PASS，39.190秒，1440/390三状态六截图；补正前条“尚未执行”的历史状态，不把原型等同产品。
- Web候选f2f2596补LOCKED/FINISHING解析、权威高版本状态切换和实际页面文案/无付款动作；金额改“租约金额”避免首次含技能费用被误认为正常月租或已付。保留旧版本/同版本冲突/终态复活拦截。新增4项合同与真实Vue组件测试；当前`web-rent-lifecycle-1`运行session39926，尚待终态。API改动尚未验证，不宣称上线。
- Web f2f2596实际定向测试59/59 PASS，161.806秒；依赖完整性核对通过。6901383仅增加浏览器生命周期矩阵，产品源码/上述测试未变；尚未执行该浏览器候选。
- API当前c69dbb5b69 / tree d330f828d7c26d7b1b8e5995556b99397afe4fde：修正升级测试在catalog后读取持久事实，以及lookup收尾状态；计划23应用测试+5技能SQL。`rent-lifecycle-api-1`在Gradle启动前被门禁拒绝（31.499秒），原因Owner gate误设implementing。随后fail把前次fixture失败与本次控制面失败累计为blocked_root_cause；transition被正确拒绝，但shell未用&&而继续调用driver，`rent-lifecycle-api-2`同样门禁拒绝（17.384秒）。两批均未运行Gradle，不当作测试失败/通过，不覆盖原记录。
- 修复矩阵：①原handover-fee-api-1：stale DTO fixture，c69dbb5中已在catalog完成后按当前owner重读，不降低断言/ACL；②rent-lifecycle-api-1/2：控制面顺序错误，使用现有authorize-remediation绑定本段矩阵，再转targeted_verification，命令用&&串行；guard本身不修改、不绕过、不启动旧批次。仅在授权修复和transition成功后开fresh第三批。完整上线待办保持不变。
- 已通过authorize-remediation与targeted_verification，API第三批`rent-lifecycle-api-3`session84744，编排器PID1285891已真实取得Gradle锁并编译；固定c69dbb5候选，不中途修改。当前仍在途，未视为PASS。后续先轮询该session，不重启。
- Web浏览器第一批21.001秒失败于默认Chrome包装器引用已不存在的缓存二进制；按已有成功批次显式使用系统headless_shell、普通磁盘tmp及disable-dev-shm-usage，未改全局工具。第二批48.996秒：原首次报价/取消/库存拒绝/重新确认三尺寸均通过，新增生命周期fixture动态JS少一个闭合花括号而失败；产品无异常。已修正fixture并保留两批FAIL，第三批session56280在途，不能把部分通过重标整批成功。
- 下一完整范围未缩小：实际API/MySQL→原Runtime关闭/清理→新报价/预占/扣款/重邀、selfhost50文及存量30天过渡、原账户停用时维护认证、调度混合容量、Redis/ES生产验收、最终构建迁移安装。只读进一步确认调度claimDue/nextDelay当前只按tenant/client/node过滤，任何容量分工必须在SQL排序/LIMIT前限定可用handler，不能claim后过滤或仅加心跳；Cron dispatcher只产生真实handler occurrence，不直接运行慢业务，容量划分不需改cron语义。暂未改这部分源码。
- Web第三批终态PASS（session56280 exit0），48.126秒，候选8e7019ea882db363fe3b19b2855816e388f90b0c。1440/390/320首次报价全交互+ACTIVE→LOCKED→ACTIVE→FINISHING实时刷新共12检查、12截图，无浏览器异常；锁定/收尾无付款/重邀动作、重查不写入、原capture保留、窄屏不溢出，已人工查看mobile-finishing截图。HTTP和登录store为显式fixture，不是生产/真实支付验证。`web-rent-lifecycle-browser-3/unit-evidence-reuse.json`核对f2f2596→8e7019e仅浏览器脚本变化，产品/59项测试/依赖输入未变，保留有效单测证据而不重复跑。
- API第三批session84744真实exit0，`rent-lifecycle-api-3/result.json` 28/28 PASS、0fail/error/skip，validateLayering通过，885.848秒（SQL169.945秒，其余715.896秒；临时取消时限）。不同buyer升级20文只从新钱包扣一次、原授权/钱包不变现已通过真实MySQL；前次失败仍保留。23应用层测试含LOCKED/ACTIVE/FINISHING只读映射通过。当前API c69dbb5工作区干净，无在途Gradle；Web8e7019e干净，浏览器已结束。尚未发布，无生产扣费。

### 2026-11-11 统一调度混合容量实施
- 上一goal轮为progress：API生命周期/新owner升级28项、Web59项及三尺寸实际组件回归已通过，未上线。本轮基于干净c69dbb5继续完整范围中的慢任务饥饿缺口，不将已通过局部切片当完整上线。
- API候选858dfcc1cf：注册处理器声明CONTROL或默认GENERAL；只有租费对账与cron数据库游标声明CONTROL，Memory/Wx/Runtime等保持GENERAL。同一runner/待办表/Redis owner/心跳中独立有界容量，新增明确部署参数`cyf.task.scheduling.control-workers`，原workers负责GENERAL。没有新增业务调度器/轮询/付款入口，未给业务下传deadline。
- claim/最近期限共用SQL包含/排除handler集合，排序/LIMIT/锁定前分组；无CONTROL注册时不发该组空查询，组容量满时不查该组。旧无子集的store调用使用同一SQL实现，不保留第二执行协议或历史适配。未知handler仍按原GENERAL失败重试，不自动执行普通JobHandler。
- 新建表及受控追加迁移候选`task-scheduled-handler-index-v1.sql`补handler期限索引，不新增CHECK；未在生产执行。新测试含跨tenant/client/node且40个更早慢待办下CONTROL先领取、迁移重复不改待办事实、失败归还容量、各组最近期限、实际MySQL续费在另一慢回调未释放时扣500文成功。慢外部操作为显式阻塞fixture，续费服务/钱包/事务/SQL及runner为真实实现，不称实际Memory/Wx provider验收。
- `scheduler-capacity-api-driver-1.py`session95166串行运行，目标51项（task runner5、store MySQL28、cron14、config3、实际续费混合容量1）及validateLayering；不同Gradle test任务各用独立MySQL磁盘临时目录。临时时限豁免生效；先取得终态，不改受测API、不并行Gradle。完整Runtime交接/自部署/存量过渡/维护认证/Redis与ES生产验证/最终上线仍待完成。
- 本批在途只读追踪同实例重邀的真实注册链，发现具体必修：`AgentRuntimeAuthenticationService.issue()`仍按tenant/client/canonical查询全部registry并要求size=1；保留旧SUSPENDED历史后，新关系必然与旧记录并存，正常新session会被拒绝。应在原注册身份查询责任层使用已有`live_agent_id`唯一投影选当前关系，不删历史、不放宽到任取第一条，补真实SQL历史+新关系及session发行回归；等待当前验证终态后修改。
- 维护认证边界进一步定位：FINISHING handler本身从原binding/intent构造UDS控制请求，不调用OwnerResolver；实际旧账户停用阻塞点包括`PlatformKnowledgeUsageController`的withNativeFence→validateRow→account(isAuthenticatable/authEpoch)。不能笼统放宽所有Runtime/用户认证，也不能把普通重邀session查询修复误称维护认证已解决。后续仍需精确原installation/lease的维护入口及凭据策略闭合。
- 接续goal轮先轮询95166并核对PID1296664存活，未重启/未改受测源；上轮属于progress。本轮已读取四份真实XML：task runner5、cron14、config3、store MySQL28共50项全部PASS（无fail/error/skip），含handler筛选及迁移；同批实际续费混合1项仍在编译/执行前，整批尚未终态，不把部分结果记作51通过。下一源码修改仍等95166终态；随后优先修复重邀session的live_agent_id查询缺口并补真实身份SQL/发行回归。无新增生产操作。

### 2026-11-11 调度容量通过，修复重邀会话发行
- 上一goal轮为verified wait：轮询95166确认仍存活；本轮已取得真实exit0。`scheduler-capacity-api-1/result.json`绑定API858dfcc1cf/tree cd4919d72325d1ead5d4ced8411b08f572721203，51/51 PASS、无fail/error/skip、validateLayering通过；总1035.957秒，其中真实SQL163.968秒，临时时限豁免继续有效。实际租费续扣不再被阻塞GENERAL回调占满容量拖住；非实际Memory/Wx provider验收。
- API新候选511fa4ad7d仅修改session发行的当前身份选择：使用已有live_agent_id投影，保留tenant/client与后续owner/binding/installation/account/epoch fences及歧义拒绝，不删除旧身份历史、不新增兼容层。
- 新回归使用真实MySQL身份/绑定DAO、immutable trigger与身份服务：旧关系激活→停用保留→新owner同agent重邀→实际issue/verify选新绑定；历史未改、新关系停用后原token及重新发行均拒绝。Runtime行持久化、installation、account为明确mock，不冒充实际同实例端到端关闭/重邀验收。另补查询谓词单测，原歧义/权限围栏保持。
- 已经既有编排器进入targeted_verification，启动`reinvite-session-api-driver-1.py`，session **83119**；普通磁盘输出`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/reinvite-session-api-1/`，tmp`/home/isp/state/cyf-test-tmp/reinvsession1`。目标persistent session26项+身份SQL4项=30、validateLayering。无时间截止；接续先轮询，不改固定受测API、不并行重型Gradle。尚未宣称通过、未部署、无生产扣费/迁移。
- 完整目标保持：实际API/MySQL→同Runtime收尾重邀，自部署50文及存量过渡，旧账户停用维护认证，Redis/ES实际部署验证，最终固定制品上线与业务验收尚待完成；不能以局部绿灯替代完整上线。
- 在途只读补全维护认证调用链：Runtime `lib/knowledge-maintenance.mjs` 的withDelivery先`client.session()`再`nativeFetch`知识费用；因此旧账户停用不仅会挡HTTP过滤器/withNativeFence，还会在发行新的普通session时先失败。不能只改controller或豁免channel。已有lease FINISHING、initial intent的runtimeInstallationId/manifest、recordExecutorStopped事实及installation bearer可用于收口专用维护授权；需与实际请求入口、Runtime client、controller事务围栏一起验证，不能让维护授权用于WS/执行。此为下一设计定位，不是已实现或通过。当前API仍固定511fa4ad7d验证中。

### 2026-11-11 原账户停用维护入口实施边界
- 前轮为progress（51项通过、511fa4ad7d修复及30项启动）。本轮先轮询83119确认仍在运行；不改固定受测API。Runtime已读取外部仓库AGENTS，本任务显式继续遵循CYF根AGENTS、RB-1及interface-standard v1.2；普通磁盘、本地来源、固定app目录规则覆盖其旧Flow/releases口径，不修改其他项目/共享技能。
- 维护认证收口选择：保留知识费用原HTTP路径与Q/R，不继续使用用户native session；Runtime用原installation bearer经专用recordKnowledgeUsage调用，不申请session、不启动/注册Agent。API复用Runtime-v1安装认证责任层，在同一事务持有installation锁；知识账本服务按原binding→initial intent→lease顺序核对原安装/manifest、FINISHING、executorStoppedAt及handoverId，再允许平台成本记账。旧用户登录状态/authEpoch不成为该安装维护授权的条件，普通session/WS/执行授权不变。
- 原native知识入口随切换移除，不提供双轨或降级；维护请求不能选择URL/凭证/费用归属、不能转成执行或新承办。原账户停用、错误安装/租约、未停机、收尾结束/凭据撤销、普通session冒充、重复/丢回执账本需定向覆盖。尚未实现API部分、未发布；当前并行仅推进Runtime非重叠源码，不修改API受测源或旧Runtime冻结快照。
- Runtime非重叠实现已落到原lib：`RuntimeV1Client.recordKnowledgeUsage`只构造固定费用URL、复用已保存installation bearer与原Q/R编解码；知识提取不再调用session/nativeFetch，不启动执行器。普通nativeFetch拒绝知识namespace，未保留旧认证路径。更新合成transport fixture和真实loopback HTTP检查：未调用session，STARTED先回执后provider、实际usage回报、私有清理仍通过；新用例拒绝lease路径注入且不读取凭据。
- 轻量诊断session88140真实exit0，23/23 PASS、0skip/fail，14.854秒。证据`maintenance-runtime-diagnostic-1/{node.log,inputs.json}`绑定编辑文件摘要，明确不是冻结制品或API集成验收。Runtime改动尚未提交/升版，Java跨进程fixture需随API认证切换更新；主仓原有README/Python制品等无关脏修改未动。API83119仍在managedHostingRegression，继续先等该固定候选终态。
- 已确认83119真实exit0：`reinvite-session-api-1/result.json`为API511fa4ad7d/tree dc0893d60c951190242560ad8b0c715375697adb，30/30 PASS、0fail/error/skip、validateLayering通过，总782.988秒（SQL169.839秒，其余613.147秒）。真实身份SQL保留旧关系且新session发行/验证通过；不是完整Runtime关闭重邀证明。
- 维护新候选API72d98fbe34：Runtime-v1复用authenticate+installation lock的内部回调边界；普通session复用相同锁校验但原用户/身份围栏不变。知识controller只接原installation Bearer，原native route不再允许；费用服务锁原binding→intent→lease并核对已停机/FINISHING/原安装manifest/handover，不读取用户登录状态。原普通业务认证不放宽。
- Runtime候选7a7089de46b0e970ffa83c52dc5a58aff9725c72/tree a4a4fd4226f9fd0a7dc4f5b44c1a5b0ec3884fd1，版本1.3.95，bridge1.1.68未变。只提交7个本任务文件，无关脏修改保留。不可变源码快照`maintenance-runtime-1/source`来自git archive，只包含runtime/bridge受影响路径；没有改变旧runtime-handover-1快照。
- API验证已启动`maintenance-auth-api-driver-1.py`session **56834**，orchestrator PID1318506；目标61项（普通session26、Runtime-v1 22、知识controller4、成本record8、真实Node HTTP/MySQL账本1）+validateLayering。普通磁盘输出`maintenance-auth-api-1/`，独占新MySQL由driver托管；当前API干净受测，不修改API或maintenance-runtime-1/source。临时时限豁免，不并行重型Gradle。
- Node→实际安装认证服务/事务→controller/normalizer→MySQL账本用例改为原账户DISABLED且authEpoch变化；普通session请求仍拒绝，知识STARTED/RESPONDED及丢ACK重投仍需通过。安装/绑定/租约repository为明确fixture，并非真实身份SQL/完整最终收尾证明；1次实际提取路径的合成provider调用，另外2个同handover不同batch的合成HTTP观测保留待价格/待usage账本覆盖，不声称3次真实提取。
- Runtime冻结验证`maintenance-runtime-1/result.json`为真实FAIL（17.018秒）：14项通过，private-data-cleanup文件装载失败，缺yauzl；git archive没有带node_modules。不是业务断言失败，不重标通过。已确认原冻结snapshot与主仓各有既有bridge node_modules，下一步在API56834终态后核对package-lock/依赖摘要并给本冻结源码补齐同锁依赖，再用新结果路径重跑23项；等待时不修改API固定输入。原`maintenance-runtime-diagnostic-1`23项通过保持诊断性质。
- 下一动作：先轮询56834（仍live），处理真实失败后再推进维护权限实际SQL/最终同实例交接。完整剩余目标不变：自部署50文/存量过渡、Redis/ES生产验证、最终固定制品/迁移/部署/真实业务验收。未新增生产操作、无真实扣费或provider请求。

### 2026-11-11 维护验证归因与定向修正
- 上一goal轮为progress（API/Runtime维护源码和跨端fixture完成并启动验证）。本轮轮询56834取得真实exit1：`maintenance-auth-api-1`总991.808秒，实际XML61项60PASS/1FAIL，layering已通过。真实Node→安装认证事务→知识controller→MySQL账本用例通过：旧账户DISABLED/authEpoch已变化，普通session拒绝而平台知识原价/丢ACK回放成功；普通session26项、controller4项、cost8项全部通过。
- 唯一失败为新`installationMaintenanceDoesNotIssueSessionAndRechecksRevocationUnderLock`测试直接复用tenant-a helper，却使用setUp默认tenant0策略。产品正确拒绝scope，未进入目标断言；经现有fail入口归因，再转implementing。候选0d5a98e419仅给该测试active/revoked两fixture显式tenant0，两行改动；保留foreign scope拒绝，不改任何生产认证。
- 下一API定向只需重跑Runtime-v1整类22项及layering；其他39项输入/生产源码/跨端fixture未变，可沿输入摘要+原XML复用，不为两行fixture重新启动MySQL。`maintenance-auth-api-driver-2.py`已准备，尚未启动，待Runtime72974结束后串行。
- Runtime缺依赖FAIL原样保留。只读核对新旧bridge package.json/package-lock字节相同，旧已验证dependencies完整tree SHA `1849a093b5485fc458dd4ad960a01d35539adc7a38ac7affc9111c65ecf77554`匹配；证据`maintenance-runtime-1/dependency-precheck.json`。API结束后才向同一冻结源码补齐该集合，不改任何source bytes、不安装/覆盖共享依赖。`maintenance-runtime-driver-2.py`session **72974**运行10个相关文件（Runtime-v1/HTTP/知识/私有清理），输出`maintenance-runtime-2/`；保留原FAIL，不新建worktree，不需用户确认。
- 本轮已核验源证据并更新specs/task-scheduling/tasks.md，生产迁移/上线项保持未完成。另清理3个已经PASS、MySQL明确Shutdown complete且无存活进程的本任务一次性datadir约493MB，保留mysql.log/所有XML/receipt/源码；精确记录`completed-owned-mysql-cleanup-20261111.json`。未清理生产/备份/他人缓存，磁盘回到约2.4GB可用。
- 只读观察本机Redis PID4136仍运行，redis.service inactive且当前prod properties无直接redis拓扑键，因此不能据此宣称线上Redis拓扑核验完成，未做任何Redis写/重启/接管操作。完整目标其余项保持不变。
- Runtime72974真实exit1，`maintenance-runtime-2`84项83PASS/1FAIL、95.052秒；dependencies摘要前后不变。唯一失败为runtime-v1.test的source systemd模板测试，原精简git archive只打包conf，缺`systemd/cyf-agent-runtime-v1@.service`，不是业务断言失败。两次冻结失败的共同准备问题为输入不完整：第一次缺忽略的node_modules，第二次扩大测试后缺仓库模板；因此不再逐文件猜补，已按**同一固定7a7089d完整git archive**补全源码快照，保留已核验依赖，不改产品源码、不删断言。
- 修复矩阵（当前重试依据）：API1唯一FAIL→测试tenant-a/默认tenant0不一致→0d5a98e419仅两行fixture修正，产品/39项独立suite输入不变；Runtime1缺依赖→同锁完整已验证dependency tree补齐；Runtime2缺模板→完整固定commit archive补齐非conf源码，不再使用精简snapshot。原FAIL保留，不能直接当完成。Runtime第三批`maintenance-runtime-driver-3.py`session **50913**，同84项，输出`maintenance-runtime-3/`，记录完整源码+依赖摘要，正在运行；API2尚未启动，串行等待Runtime终态。
- 编排器fail归因后累计为2并要求root_cause_matrix；既有历史stale DTO项已由c69dbb5重新读取当前owner结果修正并在rent-lifecycle-api-3的28/28验证关闭，未复活旧候选。当前矩阵仍以上述API两行fixture和Runtime完整snapshot准备为唯一新修复，不改guard、不自动重跑旧失败。下一API启动前必须authorize-remediation绑定当前候选及本段，再用&&进入targeted_verification。
- Runtime第三批50913已真实exit0：`maintenance-runtime-3/result.json`同7a7089d完整源码、同dependencyTree，84/84 PASS、0fail/error/skip/cancel/todo，36.140秒，依赖前后不变。原两次输入准备FAIL保留；未安装/上线。
- 已完成既有authorize-remediation并用&&进入targeted_verification；API第二批`maintenance-auth-api-driver-2.py`session **66451**在运行，目标22项Runtime-v1整类+validateLayering。API0d5a98e419干净，冻结原源码不改，输出`maintenance-auth-api-2/`；不启动SQL fixture，不做全61重复验证。
- 复用证据已实际生成`maintenance-auth-unchanged-suite-reuse.json`：逐项比对原输入SHA均相同，git diff严格只有新增active/revoked两行tenant0 fixture；4个独立原XML（普通session26、知识controller4、知识cost8、Node→HTTP/MySQL1）39项无fail/error/skip且报告SHA固定。当前状态ELIGIBLE_FOR_REUSE_NOT_FINAL_BATCH_PASS；必须等新22项及layering通过才能形成61项组合验收，原61项失败批不重标。
- 下一动作先轮询66451。之后继续实际关系SQL/完整同Runtime关闭与重邀，而非把维护HTTP fixture通过当全链上线。完整自部署/过渡/生产Redis/ES/部署等余项保持原范围，尚无需用户澄清。

### 2026-11-11 实际重邀投影链继续核查
- 本轮先轮询66451确认仍live，上轮为progress（Runtime84 PASS、API2启动及39项复用核验）。固定API仍未修改。
- 读完整重邀调用链发现另一个真实缺口：`AgentRuntimeMapper.clearBindingAfterUnbind`保留旧runtime_installation_id/host/instance/generation用于`HostingRentApplicationService.releasedInstance`→`renewal.completedHandover`确认旧交接，这本身需要保留；但`attachReleasedBinding`只写新owner/binding，没有重置这4项。`ManagedHostingCredentials.ensureInstallation`只绑定新intent/install，不更新Runtime投影。随后`AgentRuntimeAuthenticationService.issue`会因新installation与旧投影不一致拒绝会话。先前live identity修复不能解决该投影问题，不能放宽session校验来绕过。
- 下一修复归属明确：在现有原子`attachReleasedBinding`完成新关系时重置4项会话关联；释放前/释放后待邀请时保留旧install闭环，原历史归属仍在旧lease/intent/registry中。只影响该mapper和实际调用方测试，不改变执行入口或认证规则。
- 原`HostingRentRenewalMySqlTest.seedRuntimeProjection`极简表缺少这4列，现有重新绑定测试没有覆盖它们；下一步补齐真实字段、保留旧install直至新attach并断言新attach清空，再将`reinvitedRuntimeSessionUsesCurrentSqlIdentityWithoutDeletingHistory`的Runtime持久化mock替换为实际mapper/DAO，串起真实clear→attach→issue/verify（identity与Runtime均SQL），保留account/installation显式fixture。必须等待66451终态才改受测源；这仍不代替最终API/UDS/Runtime全交接验收。

### 2026-11-11 维护组合验收与重邀投影修复
- 接续确认维护API第二批66451真实PASS，22项及layering通过，631.471秒；结合逐项输入/报告摘要核对的39项复用，`maintenance-auth-combined-acceptance.json`固定0d5a98e419/tree97953855形成61项组合PASS。原maintenance-auth-api-1 FAIL不重标；安装/关系协作者仍有明确fixture，不代表完整交接或上线。
- 用户再次临时取消本任务时间限制，沿用已有豁免，不修改全局/其他项目时限，不削弱生产授权、锁、资金与恢复保护。
- API新候选2126fe84eb：仅在原子attachReleasedBinding建立新关系时清空旧installation/host/instance/generation；clearBinding仍保留旧安装用于completedHandover核对。没有新增兼容层、额外查询或放宽session校验。
- 真实MySQL用例补四列并断言释放后保留安装、新绑定清空、迟到旧解绑不能破坏新关系；重邀session用例移除Runtime DAO mock，改真实mapper/DAO串起clear→attach→issue/verify，保留安装/account明确fixture与旧身份历史。
- `reinvite-projection-api-driver-1.py`经编排器进入targeted_verification，session95921，目标34项+layering，输出`reinvite-projection-api-1/`。固定源码受测期间不编辑API。完整范围仍包含自部署/存量过渡、完整交接、生产Redis/ES/容量及最终受控发布，尚未上线。
- 重邀投影批95921真实exit0：`reinvite-projection-api-1/result.json`固定2126fe84ebd793034054e1ca7783fb862ea97e93/tree3052a73416aaf8c6074e741524ed6b17a5023f36，34/34 PASS、0fail/error/skip，layering通过，1081.352秒。实际SQL已覆盖旧安装保留至新attach、新会话generation从1开始、旧身份历史保留和旧解绑无效；仍非完整Runtime交接。
- 下一候选0949b3b4ed只升级原`PlatformKnowledgeUsageHttpMySqlTest`，不另建测试框架：去掉installation与FINISHING关系mock，实际MySQL生产installation/rent/usage DDL +真实installation DAO、binding锁、intent/lease锁、renewal服务；binding测试表只包含实际消费字段。普通session拒绝仍用明确account/identity替身，provider仍合成；保留真实Node HTTP、丢ACK重投、原价冻结、平台独立账本。新增SQL关闭租约/撤销installation后不得继续写cost断言；不把该组合称为完整业务收尾。
- `maintenance-sql-api-driver-1.py`经&&进入targeted_verification，session67446，固定新候选、独占普通磁盘MySQL，1个跨端测试+layering，输出`maintenance-sql-api-1/`。临时时限豁免继续有效。API受测期间不改固定输入，未部署或使用付费provider。
- 维护真实关系SQL批67446已真实exit0：`maintenance-sql-api-1/result.json`固定0949b3b4ed88304eee6b7e4543838180f7870ea7/tree49b347d3daa6edfd1d75e27c66f470538b4478d3，1/1跨端用例PASS、layering通过，590.871秒。实际Node→安装Bearer查库与锁→binding/intent/lease原关系锁→usage账本通过；旧账户停用/epoch变化不影响平台维护，普通session仍拒绝；原价与丢ACK幂等、未扣用户款、SQL CLOSED/REVOKED拒绝均通过。安装/关系mock已移除，只有普通session身份/account及provider是明确fixture；仍不能称完整API/UDS/Runtime交接。
- 本轮未做生产部署/迁移/真实扣费/付费provider。两批测试均终态，无受测输入仍在运行；API干净0949b3b4ed。下一动作在现有测试路径组合真实API/MySQL→同Runtime UDS stop/cleanup→新报价预占捕获→重新准入（原UnixManagedHostingProvisionerTest已具真实UDS，credentials/session为mock；本轮两SQL链分别通过但尚未合成全链）。自部署50文及存量两种模式30天过渡仍是产品缺口，不因这些PASS删除；Redis/ES/消费者容量/最终发布待办不变。当前无需用户澄清。

### 2026-11-11 10:22 恢复实施 / 12:00验收目标
- 用户要求继续并在北京时间12:00前完成闭环提交验收，撤销此前暂停；Owner仍task-scheduling-owner。先处理复审确认的旧托管执行分支与同事务重复查询，再补产品收费缺口及关键闭环验证；不新增框架，不以缩减回归伪报交付。
- 固定基线API0949b3b4ed88304eee6b7e4543838180f7870ea7（tree49b347d3daa6edfd1d75e27c66f470538b4478d3），Runtime7a7089de46b0e970ffa83c52dc5a58aff9725c72；保留既有未提交组合测试及无关修改。现有worktree复用，无新worktree。当前查阅根AGENTS、组件AGENTS、工具索引及cyf-quick-iterate；冲突的Flow-only按本地规则覆盖。
- 旧发布worker仍负责当前Runtime投影通知，不能连同旧文件publisher一并删除。范围为移除旧文件开通状态机、独立保留仍被引用的scope及投影worker；身份/锁/资金/跨I/O重新核验不削弱。
- 10:52 复审整改候选API ed5010e882：连同确认无生产调用的旧HostedProfile写DAO/Mapper及旧解绑投影方法移除，保留历史表/实体/只读预览与当前绑定投影通知；给现有资金/协调测试增加不重复读取绑定的断言，不新建框架。
- 第一批closure-api-1真实FAIL：128项127PASS/1FAIL，1459.833秒，失败为组合测试UDS路径125字节超过系统限制；原53个租费SQL用例通过，未冒充完整批次通过。Runtime closure-runtime-1真实FAIL：61项58PASS/2FAIL/1cancelled，627.048秒；两项相同长路径EINVAL，一项并行负载下fixture超时。保留日志/报告，不改应用超时/身份规则。
- 明确修正：沿用既有普通磁盘短tmp路径策略c2/cr2，串行运行API与Runtime；删除runner重复启动的无用MySQL（测试类本来已自己拥有MySQL）。后续只重跑组合SQL及受影响单测/新增作用域回归，不重复全53个未改SQL用例。该修正是测试环境，不是产品兼容补丁。
- 11:22 closure-api-2真实FAIL：122项121PASS/1FAIL，1266.422秒；layering通过，bootJar未到达。组合用例已通过首费/停机/私有清理/SQL关租约与撤销安装，失败于下一用户报价，不标完整通过。
- 归因矩阵更新：本轮不是配置对象复制（validateHostingConfig返回原对象，已实测sameConfig=true）。原生skills/list诊断明确返回“provider name must not be empty”，共享测试fixture缺少provider name；生产example已有name。修正只给fixture补合法名称（Runtime e543c40），不改产品失败判定/库存语义/传输超时。原始诊断保存在closure-inventory-diagnostic.log；未知库存仍拒绝收费。
- 下一验证：API源码保持ed5010e882不变，复用已固定输入的121个通过用例，重跑失败组合链+layering+fresh bootJar；Runtime短普通磁盘tmp串行61项。原两批FAIL保留，禁止重标。自部署/存量迁移/生产验收不因本次清理自动完成。
- 11:43 closure-api-3再次真实FAIL：仅组合链在下一报价NOT_READY，770.688秒，bootJar未执行。没有把修正provider name等同于全问题已解决。新独立诊断确认原生库存47.074秒（measure41.090秒），停止/清理后的真实HostingControl库存也返回1项；因此传输时限/组合负载是当前待验证假设，不宣称已证实。
- 后续候选仅调整组合测试专用inventory传输窗口为120秒，并在Node测试fixture记录安全method/elapsed/errorCode，保留真实observer、资金/隔离断言和全部产品配置；不提高生产时限。新API71b8033dea、Runtime20e2b7c。此次属于有新观测/隔离条件的诊断回归，不把原失败重标。若再次失败，在12:00前按未通过提交，不以取消断言或合成库存冒充闭环。

### 2026-11-11 11:58 验收提交（未通过，未上线）
- 最终诊断closure-api-4仍FAIL（1个组合用例），API71b8033dea/treebbe36b797a9c222fdba35e7afd1ece038b0ae51d，Runtime20e2b7c/tree6ae6292b619fdf45000f36caea048b38f19af75e。首次库存60074.081ms，第二次965.988ms，确认默认60秒冷启动边界确实被超过；仅测试120秒窗口使其走过550文新报价及确认，未改生产设置。
- 新失败在HostingRentRenewalMySqlTest:307等待新关系ACTIVE，而不是报价；只读运行诊断确认hostingFixture创建的RuntimeHost.admitRelationship为undefined，RuntimeHost.readmitAgent:205要求真实适配器。生产createExecutionAdapterFactory已有该适配器，先补测试接线而非放宽生产围栏；不能加无条件成功stub。
- Runtime61项在e543c40通过（87.993秒）；API121独立单测/Mapper输入未变可复用，原失败批不改成PASS。最后bootJar未执行，无新生产包/安装/迁移/真实扣费/付费模型调用。API/Runtime源码提交保留，原脏工作区未覆盖；仅移除已停的本任务MySQL临时data，日志与报告保留。
- 用户12:00完成闭环目标未达成，按未通过提交验收材料，不宣称完整上线。当前剩余：真实重新准入组合接线与回归、默认库存窗口冷启动、fresh包；自部署50文/存量切换及生产Redis/ES/混合容量/线上验收仍是独立未完成项。下一动作先按现有失败归因处理，不盲重跑或新建框架。

### 2026-11-11 12:55 两小时交付目标恢复
- 用户要求两小时内完成，目标14:55；范围不缩水，不以降低资金/身份/私有清理断言赶工，不再进行额外重构。
- 当前归因矩阵：closure-api-4新关系未ACTIVE源于Java组合fixture缺少admitRelationship；Runtime a370d98将生产createExecutionAdapterFactory.admitRelationship接入，该真实manager/engine处理无attached executor的进程恢复形态；executor注册仍明确合成，带attached executor关闭的真实路径已有独立readmission集成测试。不是无条件成功stub，不修改生产围栏。
- API71b8033保持固定；closure-api-5只跑失败组合链及layering，不提前生成仍缺产品功能的最终包；原FAIL保留。当前仍待默认60秒冷启动、自部署/存量切换及真实交付。
- 13:21取得closure-api-5真实PASS：API71b8033、Runtime a370d98固定输入，1199.867秒；完整单用例包含首费500文、旧关系关闭/安装撤销、私有文件删除、技能保留、新报价550文/新关系首费捕获、旧完成重放不能影响新关系、账目借贷平衡。executor注册/Provider仍合成；不宣称真实WS上线。Layering通过，未构建JAR。
- 冷库存实测：旧源a370d98组合中114958.781ms；5036228去重复policy哈希后，在同一主机重载/并行原生测量时88891.855ms，仍超默认60000ms，不判性能通过。第二轮bba4f8b把同一次冷测量的重复全量哈希收口为一次内容测量+前后ctime/inode/权限/祖先状态一致性核验；显式recheck和实际进程身份核验保留，新增测量中二进制/资源同size/mtime篡改拒绝测试。版本Runtime1.3.96/bridge1.1.69，尚未发布。
- API f9a7365仅测试：恢复组合测试默认库存窗口；新增真实Redisson客户端断开后watchdog过期接管测试，不forceUnlock、不操作生产Redis、不将其冒充容器网络分区全验收。下一批closure-api-6为这8项+layering；先等待Runtime固定bba4f8b定向测试终态，串行重型验证。
- 当前额外观察：自行部署仍由AgentController→AgentPersonaProvisioningService免费绑定；ManagedHostingProvisioner仅UDS托管适配，HostingControl current/prepare对非托管静态主体无租约关联路径。因此自部署不是只登记50文套餐，需要真实生命周期接线；不能新增假库存/假READY或直接预扣替代。既有主体切换同样依赖精确原安装/绑定接入收尾，不能仅插租约后标迁移完成。当前不实施未经验证的资金或身份临时补丁。
- 13:34正式固定Runtime bba4f8b的组合证据：closure-runtime-7 135项134PASS/1SKIP、282.966秒（遗漏原生库存测试开关，原批记FAIL不改）；同一冻结source7/同dependency tree的closure-inventory-8显式CYF_INVENTORY_CODEX_BIN补跑库存全6项，6PASS/0SKIP、33.127秒。合并唯一135项PASS见closure-runtime-combined-acceptance-8.json；原生库存用例实际约28.95秒，默认API窗口仍待完整组合再验证。
- 发布前核对当前线上record：API cbeab0d8c5/1.1.47-SNAPSHOT包含3个未合入本任务的已部署会话刷新修复；远端develop已于13:29成功fetch，固定c661e64213已在本任务祖先中，但不包含该已部署分支。已合并cbeab为f3a97a5224，保留本任务平台维护/证据投递认证lane及线上401/503权威信封；两组WS回归一并保留。不覆盖脏修改，不假称原121项全部可复用。
- 因真实线上基线合并，closure-api-6扩为受影响会话/注册/维护权限、真实Redis失去客户端接管及默认窗口组合生命周期，所有源码受测期间固定；不增加无关全量业务测试。当前版本未上线，后续新制品须高于已部署1.1.47。

- 13:53线上Redis只读盘点完成：受限配置文件提供现有认证，经标准RESP读取INFO（无锁写入/重启）确认4.0.6 standalone master、0副本、AOF关闭/RDB末次ok；生产JAR prod默认127.0.0.1:6379/db0。PID4136属于既有session scope，不宣称systemd守护或高可用。证据production-redis-observation-20261111.json。首轮CLI4.0.6不兼容新flag的失败记录保留，不能误归因为凭据错误。生产拓扑项已核实，故障接管仍待当前隔离双客户端结果/线上验收；不为此擅自升级Redis或更改配置。

- 14:08 closure-api-6真实PASS：固定API f3a97a5224bf29f3f7a2761b2385e8690b888d45/tree f06853285388dc837abe29b460dd129e24ada96c，Runtime bba4f8b/source7；101/101、0fail/error/skip、分层通过。总1866.891秒，记录的集成区间214.919秒，余1651.938秒；临时取消时限仍按实际记录，不将单测改名规避。Gradle实际1784.973秒，未执行bootJar。认证54、WS17、Redis7、Runtime-v1 22、完整托管生命周期1。
- 默认60000ms库存窗口下组合全链通过，清理后冷库存30019.752ms、后续2893.541ms。未延长生产窗口；先前120秒诊断批仍单独保留。固定fixture使用实际admitRelationship/manager/engine，账户目录/executor注册/知识Provider仍明确合成，不声明真实线上WS或付费模型验收。
- 只回收已明确Shutdown complete且无精确datadir存活进程的c6/mysql/data 172847453bytes，三份fixture日志复制到closure-api-6并保存SHA；记录owned-fixture-cleanup.json。未删源码/制品/备份/他人缓存，没有在途本任务测试进程。
- 当前完整目标仍未达成：自部署须经可信远程安装/库存/准备/就绪/收尾关联接入现有租约闭环（当前只有托管UDS，local bind仍免费）；存量切换必须建立真实原安装/关系关联；不能靠50文配置、假READY、插租约或临时放宽授权交付。其后才是fresh固定包、生产mapping/DDL、受控安装和真实业务验收。两小时目标14:55未被改成缩减范围的交付承诺，已向用户明确剩余时间无法承诺完整上线；不提前发布不完整收费候选。

### 2026-11-11 自行部署验证目标（用户指定）
- 用户指定使用 `isp@chcbz.net` 中的李逵做自行部署开发验证；共用租费/续费/调度/收尾业务逻辑，仅适配安装及控制通道，不另造收费流程。
- 14:34首次只读SSH核对在主机认证阶段失败：本机known_hosts中chcbz.net的ECDSA记录与远端不一致；当前解析173.230.149.118，远端报告指纹 `SHA256:MlERdPRQc4D4HOPjZ731qmk118bLWCI2353BMAQvDJI`。远程命令未执行，李逵实例/绑定/版本/在线状态尚未核实。
- 未删除known_hosts或关闭StrictHostKeyChecking，未改余额/关系/会话或远端配置。需用户通过可信控制台确认该主机指纹，或提供正确目标；不将本次失败当业务回归失败，不盲重试。
- 用户随后明确授权忽略该主机警告。采用临时、目标专用known_hosts接受此前观察的同一ECDSA指纹，登录仍StrictHostKeyChecking=yes，若指纹再次变化则停止；没有删除/改写全局信任记录。附件私钥仅复制到0700临时目录的0600文件，连接结束随目录删除，不写入源码/证据。
- SSH已实际成功：主机li159-118、用户isp(uid1002)，Runtime进程PID4185。只读配置定位李逵profile `likui`，canonicalAgentId `jyt-jiafewnnv58ec2379c-likui`，installationId `rti_dd441f1ea25d6f6c8dff50463906abf1`，manifest tenant0/client jiafewnnv58ec2379c；hostId selfhost-li159-118-935f9597。manifest/profile位于 `/home/isp/conf/cyf-agent-runtime-v1/likui/`，私有HOME为 `/home/isp/state/cyf-agent-runtime-v1/unified/agents/likui/codex-home`。只读取明确允许的配置元数据，未读取会话/凭证正文。
- 该主机标准app/runtime与app/codex-bridge的package.json不存在，实际进程源码路径/版本和API侧绑定/会话状态仍需核实，不能直接套用本机安装路径或声称业务在线；原指纹故障已由用户授权接受解决。证据self-host-likui-observation-20261111.jsonl。未远程写配置、部署、扣款、停止进程、解除关系或清理数据。

### 2026-11-11 李逵 Runtime 已按用户单独授权升级
- 用户明确要求“直接升级李逵服务器上的runtime版本”。本轮选择当前已生产验证的Runtime **1.3.71 / bridge1.1.59**（源码01914a4f8b1777e0e7496548d240cb46d138efde/tree712d8615d91f4e9baa885aa17a701112c3ded9d1），**没有部署尚未发布验收的租费候选1.3.96**，也没有部署API/Web、扣费或解除关系。
- 目标isp@chcbz.net / li159-118，李逵既有installation rti_dd441f1ea25d6f6c8dff50463906abf1及配置不变。旧Runtime1.2.1/bridge1.0.1从releases/1.2.1切到固定app，PID4185→306359；旧程序归档至/home/isp/baks/cyf-agent-runtime-v1/20261111-likui-runtime1371/program，停写完整配置/状态快照private-state.tgz同目录。现有会话、技能、凭证和公共仓库未清理；旧current链接在验证后移除。
- 复用本机已验证程序制品，按原7501项manifest逐项核对文件摘要、模式、内部链接与完整文件集后重新封装（不在生产目录编译）。归档SHA256 2b8e52a14b258fd004481d86eb7e908cead66f8bf1975483d27d9db5f7ccae8a。远端现有配置预检通过；补齐系统依赖bubblewrap，未更改内核参数/应用配置。
- 本次核验：systemd active、真实app/node执行路径、旧进程退出，当前health同PID且connected/registered/ready均true、channelState=ready、lastFailure=null；没有调用付费模型，不能将在线验收等同真实事项或租费全链验收。
- 原封装脚本未处理已登记的内部依赖symlink而失败，归因后按原manifest核对链接及其边界重试；首次远端展开被umask缩小目录权限而预检失败（旧服务未停），归因后显式保留源权限展开到新candidate-2并通过。失败证据保留，未盲重试/放宽摘要；未启用的失败暂存已删除，备份保留。
- 证据：/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/likui-runtime-upgrade-2/remote-acceptance.json；远端/home/isp/state/cyf-runtime-upgrades/likui-20261111-runtime1371/acceptance.json。远端安装切换11.165秒，构建/展开各尝试失败分别保留，不冒充首次成功。
- 升级前另完成资金责任层续费planId绑定（API0c583d6c77298e866d67d0157cc1d7c3aa470259）：防止跨部署套餐续费，不增加SQL或层层校验；同套餐版本变价继续允许。首批测试误用钱包字段导致编译失败，修正后20项真实H2事务回归及validateLayering通过。原runner误沿用“至少30项”汇总门槛使外层FAIL保留，逐项报告摘要及目标用例核对见renewal-plan-api-2/report-audit.json，无重复构建。本API改动未发布。
- 本轮升级不解决自部署收费/远程生命周期控制、存量30天过渡、数据库与ES生产迁移等主任务缺口；不能将本次升级标为整套租费功能上线。

### 2026-11-11 15:26 继续自部署接线：现有租约身份入口
- Owner仍task-scheduling-owner，复用API worktree task-scheduling-api-next；起点0c583d6c77298e866d67d0157cc1d7c3aa470259，候选cac049e991。当前仅补现有租约查询/续费/解除/重整的身份入口，不部署、不扣费、不改李逵identity，不把该切片称为自部署收费完成。
- 调用链确认：身份责任层原本支持登记的LEGACY_CANONICAL，且按tenant/client/owner精确查registry；租费入口额外硬编码agt_正则导致合法存量ID在到达身份责任层前被拒绝。现有租约入口改为协议文本校验，仍要求返回canonical与请求字节一致，别名不自动转换、外部owner无权读取。初次新建/重新邀请仍走既有opaque路径，尚不支持存量静态主体首次接入/重邀，不能据此迁移真实李逵。
- 无新SQL、无兼容映射表、无Web/Runtime协议变化；新增5项定向测试，覆盖存量canonical查询/续费、别名拒绝、scope拒绝和非法文本。原应用整类共28项，加validateLayering，经既有编排器执行existing-identity-api-1；结果尚待终态，不先报PASS。
- 远程控制真正缺口已确认：现有execution-adapter的WS属于executor，RuntimeHost.quiesceAgent会close executor，不能直接拿该WS承载后续evidence/cleanup而声称闭环。需宿主控制通道独立于执行器存活、复用同一hosting业务处理器与原installation认证，并完成静态主体精确接管；不以SSH执行业务命令、不加假READY或空轮询替代。当前只是调用链结论，尚未实现。

- 15:29 existing-identity-api-1真实PASS：API cac049e991e8d46a80aa2955de1a6d73283f6009/tree1cbb207cf94e5de4b45b080f646aeba825a2c94e，28/28、0fail/error/skip，validateLayering通过；155.822秒（受限155.816秒），未生成/发布JAR。证据目录 /home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/existing-identity-api-1/；无本任务在途测试进程。
- 下一实现仍为自部署宿主控制与静态主体接管；随后两种模式共用租约套餐/30天过渡迁移及生产交付。不要把本次身份入口修正或已完成李逵1.3.71升级当作自部署收费闭环。API工作区干净；Runtime仍bba4f8b且原无关脏改未触碰。本机普通磁盘余约881MB，继续构建前按实际产物检查，仅清理本任务可回收内容，不全盘清缓存。

### 2026-11-11 15:45 存量静态实例共享生命周期接入
- 上一goal turn为progress：APIcac049e身份入口修正、28项及layering通过，非整体交付。本轮继续真正缺失的静态主体接管，而非重复已绿托管链。Runtime工作区仍复用isp-install，原README/install/Python等无关脏改未触碰；根AGENTS本地普通磁盘/600秒、RB-1和统一接口v1.2显式适用外部Runtime。
- Runtime候选1.3.97：bdaab8c新增hosting.adopt、静态profile关联、无模板静态宿主、同一状态机current/停机/证据/清理/重邀；2488e71补完整测试；e54aa6c仅增加Java跨端fixture的静态模式。没有新建业务实例、SSH控制特例或钱款处理；只是协议及本机生命周期能力，远程控制与真实cutover未接线。
- 第一批adoption-runtime-1真实FAIL：232项225PASS/7FAIL、73.188秒。一项新增测试在尚未绑定evidenceOwner前错误期待EVIDENCE_REQUIRED，实际IDENTITY_CONFLICT是正确保护；补明确pending evidence步骤后同时验证两阶段。另6项原consumer测试读取固定历史git archive，完整源码snapshot无.git，补runner显式只读GIT_DIR及固定历史commit，不修改被冻结历史fixture或生产逻辑。原FAIL保留。
- 第二批adoption-runtime-2真实PASS：Runtime2488e71dfb869572937eb0fc97fe364d563aea91/tree8de91ed2d655a87d3a3dc51d24d9b0fed73257d4，232/232、0fail/cancel/skip/todo，124.130秒，依赖tree前后相同。实际私有目录清理/同一HOME新关系准入已运行；原生注册/公共知识provider仍fixture，不声称生产WS/付费模型验收。证据 /home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/adoption-runtime-2/。
- API候选b49120979d：新增同一adapter的adoptExisting，完整回显与host绑定，不签发凭证；免费重整统一使用安装责任层带锁读取而不是再次ensure待注册安装。初次新安装仍需enrollment；既有安装REPROVISION允许明确null，后续关系/安装/manifest/代际检查不变，无新SQL轮次。
- adoption-api-1固定API候选、Runtimee54aa6c/source3，正在执行62项与layering（真实Java UDS静态adopt→current→quiesce→evidence→cleanup，以及原托管UDS链/身份/安装事务）。独立600秒计时，短普通磁盘tmp a3；没有并发重型任务，没有MySQL/Redis/生产数据变更。待轮询exec session8980，日志路径同证据根adoption-api-1。

- 15:53 adoption-api-1真实PASS：APIb49120979dc04eec629a443fa20492932dea2358/treead0595efb45132b58887e5a3af5b29ee557db012，62/62、0fail/error/skip、layering通过，356.945秒，未执行bootJar。已逐项读取XML确认实际Java静态adopt清理用例（1.763秒）、安装fence/无注册元数据重整用例确实执行，没有只看汇总。runtime-input-audit.json核对source3完整581个Git blob、e54aa6c完整commit/tree、Node和依赖摘要；未将mock/fixture当实际生产资金验收。
- 原Runtime第二批session75382和API8980均已终态；本轮没有在途构建/测试。真实李逵只读查询另确认存在nginx1.12.2/1.14.1及443监听，没有修改nginx/端口/证书/运行配置，也未决定或实现新的远程控制传输。不要因存在443就假设可用mTLS或宿主控制端点。
- 下一动作继续远程宿主控制（必须独立于被停止的executor存活）、静态实例绑定后的50文套餐/30天过渡及首次调度接线。API工作区干净；Runtime仅保留原无关脏改；Runtime1.3.97候选与此前实际李逵1.3.71部署分开记录，均未新增扣费/清理生产数据。完整目标保持active。


### 2026-11-11 16:08 Runtime远程控制子链完成，主目标仍active

- 本轮未改API（仍b49120979d）、未操作生产端口/证书/服务/资金或私有清理。Runtime任务提交121efd99924846b7cc8d4116f731e5a5d58d2548及6ccbfcbb41cc26ecbd635cd66d56c5cbda4e796b，候选1.3.98；保留README/install/python-freeze等所有原无关脏改。
- 原HostingControl增加可选运维remote配置和mTLS listener，复用原UDS handler/帧/关系/journal；TLS不依赖被停止的executor。私钥/CA必须在Agent可写根之外且权限正确。无未认证入口、SSH业务命令、重复收费引擎或证书轮询。
- tls-runtime-1：固定121efd9/tree c29cd9bae595acbd519895ef717df095cb42dd87，235/235，0fail/cancel/skip/todo，150.318秒。tls-runtime-2：固定6ccbfcb/tree b6d47b9fad36c33ff2eaedde6a31252ec2f11bde，12/12，9.426秒；后一提交仅追加配置隔离测试/指南。两批source-audit.json逐个核对582个Git blob，Node与依赖tree绑定。driver沿既有adoption模板，普通磁盘tmp t1/t2，各600秒独立计时。sessions32292/96204均终态，无在途测试。
- 实测包含Agent停止后证据控制、TLS/UDS同journal重放、错误scope、缺失/伪造客户端证书、服务端身份不符、超大帧、密钥权限、Agent根内凭证、符号链接和CA可写拒绝。测试使用临时证书与既有模拟原生执行/provider，不是生产收费或真实李逵远程验收。没有最终制品/部署。
- 下一动作：API共享adapter的可信host路由和TLS客户端。现UnixManagedHostingProvisioner.exchange约355行只走UDS；可沿Spring已有SSL配置或JDK上下文接入，禁止请求传endpoint。必须解决attachReleasedBinding会清空runtimeHostId的路由点：初次重邀prepare使用持久化quote.inventoryHostId，后续candidate.hostId，不能退回本机。probeCapabilities目前无Agent参数且static template=null会返回不可新建，不能以此拒绝已有静态实例的正常重整。原账本/调度共用，接着自部署50文、存量两种模式30天过渡/首次调度、legacy规范ID重邀身份责任层，再生产迁移/制品/实际验收。
- 当前磁盘约650MB可用，继续使用普通磁盘，不能为腾空间删未知包/日志/备份或用tmpfs。Runtime安装仍是李逵1.3.71，不把候选1.3.98当已部署。
- 文档检查`./sddw check-docs task-scheduling`本轮FAIL，原因是三个无关已退役路径重新出现：agent-client-skill-refresh/delivery-status.md、agent-workspace-capability-refresh/delivery-status.md、oauth-public-client-hardening/delivery-status.md；原始输出保留tls-doc-check.log。不删除他人文件、不把文档检查说成通过；本任务git diff --check通过。


### 2026-11-11 16:39 API可信路由/mTLS已实现，tls-api-4仍在途

- 前轮是明确progress：Runtime双端传输候选通过。本轮API提交d5a445b4→c2f717dac4→897e5095800f7fc294b0858f04b2767a4954d654（tree0f6e6875110780d84ba03e3eff39f9a29d0dc7ea）；Runtime仅fixture提交8e556e9→bd73fe4。未生产配置/部署/扣费/清理。API工作区干净，Runtime原无关dirty保留。
- `HostingControlRemoteProperties`注册operator localHostId及hostId→endpoint(address/port/SSL bundle/scope)；`HostingControlChannel`只承担可信路由与mTLS，SSLContext按Spring当前bundle实例复用。候选host优先，首次prepare用quote.host，其他从已登记runtime单次按scope查询；缺host拒绝，不对已存在投影回落本机，避免新关系清空投影字段后错路由。只有无投影的新托管主体可走明确本地host。candidate/quote已带host不多查库，未增加扫描/Redis或第二计费引擎。
- 现existing probe(四参数)沿真实Agent主机发原capabilities，允许static template=null返回available=false（仍可管理既有实例）；新建三参数探测仍要求true。应用免费重整使用四参数；消息合同未变，API业务授权和账本原样。UDS和mTLS回复均核对选中host，端点不从HTTP请求接收。
- tls-api-1在Gradle前因ledger仍b491209而拒绝，FAIL保留；同Owner正常transition固定新候选。tls-api-2生产源码编译通过、测试fixture未导入Map导致编译失败（280.546秒）；修复java.util.Map，同原工具记录归因并authorize-remediation（工具累计旧wallet失败导致计数2，非同根因盲重试）。tls-api-3：99项/97通过/2失败，486.248秒、layering通过；实际Java TLS静态探测/adopt/current/停止/证据/私有清理和负向身份均通过，H2重整5/应用28/凭证14/Runtime服务23通过。report-audit.json另存真实失败明细，不改原FAIL。
- 两个失败：旧UDS fixture精确字段集合不接受remoteAddress:null（已改为只在TLS返回）；静态清理第1次调用false，原因尚不能证明。现在实际exchange直接抛异常/输出非CLEANED结果，Runtime fixture只记method/outcome/errorCode/elapsedMs，无正文/凭证；保留原1000ms测试值，没有猜测提高生产超时或改为跳过。后续根据实测处理。
- **当前正在跑tls-api-4，exec session94645**，driver `/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/tls-api-driver-4.py`，日志tls-api-4/gradle.log；固定API897e509580、Runtime bd73fe4的tls-runtime-source-4；29项adapter/channel及layering。16:38实际PID1648007存活、处于agent compileJava，独立600秒内。先poll同一session，不因观察过期另启或重标结果。源码不得在此批仍编译时修改；runtime-input-audit.json已核对582Git blobs、Node与依赖tree。上批43894/81555均已终态，审计session62501已结束。
- 控制配置只读核对记录在tls-api-3/local-host-route-observation.json与likui-host-route-observation.json：本地host=cyf-unified-065bb566a2d82210、UDS control.sock/gid1000；李逵host=selfhost-li159-118-935f9597、active/running/PID306359、未配置hostingControlPath。无证书/端口写入。最终部署必须设置新的local-host-id，不能把旧配置原样部署后宣称收费可用。
- 后续真实缺口：自部署50文套餐和Web确认（现AgentController local仍走免费AgentPersonaProvisioningService，Web hostingRentContract硬编码mode=server）；费用模式必须由可信部署事实决定，不能仅凭用户mode给托管主机50文价。AgentRuntimeEntity没有部署模式字段，不能从远程/本地传输自动推断托管类型；应在既有运维主机配置/原租约责任层明确，并复用同一账本/调度。还需存量双模式30天过渡和首次调度、legacy规范ID重邀（provisionOpaqueIdentity目前拒绝非agt_，原live_agent_id唯一键迁移已允许历史身份保留）、生产DDL/ES/最终fresh制品与完整真实验收。
- 当前普通磁盘约470MB余量。构建并未使用tmpfs；不清其他任务或未知包/备份。最后文档检查仍为已知3条无关退役路径复现，详见tls-doc-check.log，不将其说成通过。

- 16:42 tls-api-4已真实PASS：API897e5095800f7fc294b0858f04b2767a4954d654/tree0f6e6875110780d84ba03e3eff39f9a29d0dc7ea，Runtime bd73fe4固定source4，两类29/29、0失败/错误/跳过、layering通过，489.176秒全部计入本批600秒。XML逐条核对Java mTLS链8.793秒、原托管UDS链30.095秒、静态UDS链1.979秒；静态首次cleanup CLEANED耗时32.997ms、重放0.897ms。原false本批未复现，原轮没有原因信息，不反推成已证明的超时；未修改原1000ms测试值及生产默认值。
- session94645已终态exit0，当前本任务没有在途测试/构建；Runtime/API候选均未发布。前批99项中与本次transport两类之外70项通过证据仍绑定原c2f717，而不宣称“本候选99/99”；最终发布仍需受影响整合覆盖。当前普通磁盘约437MB余量。下一动作是实际主线的50文套餐/可信部署类型与Web本地确认，再存量过渡/legacy重邀，不能停在本轮控制子链通过。

### 2026-11-11 自部署套餐定向候选
- 接续未提交草稿并完成报价/确认/续租责任层及fixture收口，API提交 `cc72fe836215f59e4a36019663746299d9a8df13` / tree `2f513c47faae8fb9e96a128a207979cb96296ed5`。保持显式主机计价配置，远程不等于自行部署，前端不能降价；续租按原planId共用账本，未新增表或兼容构造器。
- 新增自部署50文报价、客户端降价拒绝、主机类型变化拒绝、原套餐续租不探测主机及本地/远程计价分类测试；原有测试修正真实套餐与租约fixture。当前 `pricing-api-driver-1.py` / `pricing-api-1` 正经原编排器运行三个suite及layering，exec session9594，未出结果。普通磁盘初始434MB，不使用内存盘。
- 尚未改HTTP local免费绑定入口和Web；原型已有两种价格说明，但产品local仍绕开租约面板，需与HTTP一次收口后发布。未变更生产配置、扣款、迁移或Runtime运行版本。
- `pricing-api-1`实际FAIL/timeout，600.889秒，session9594已结束；没有完整测试报告，不能记为42项通过。日志显示变更配置/mapper ABI后agent/chat依赖重新编译，其中chat compileJava124.037秒，约末段才进入managedHostingRegression。精确归因已由原fail入口登记（本轮连续失败1），保留原结果；所有本任务该批子进程已退出。
- 复用原JavaCompile缓存、测试与layering不缓存，启动同源`pricing-api-2`，session18220，新输出、新600秒；不修改源码。`authorize-remediation`因尚未达到blocked_root_cause而拒绝（仅一次失败，不需要该操作）；随后原正常transition到targeted_verification，不改写或绕过blocked状态。原失败不重标。最终结果待回收。

- `pricing-api-2`已PASS，42/42、0失败/错误/跳过、layering通过，485.806秒，固定cc72fe8362；session18220已终态。首轮超时与本次通过分别保留，不合并耗时。重跑没有免除测试预算。
- 后继API4773d49c83删除HTTP默认/local免费绑定，统一付费确认，移除Controller直接方法和旧service构造依赖；租约投影加入planId；补空mode拒绝、两模式真实HTTP信封测试。`pricing-http-1`编译FAIL/118.921秒：误删了仍被Controller异常处理器使用的HostingRentAdmissionException import，修复为f38eb78e29c19fa0868e07a19e38a3a478ee0116/treeec7aa289dd61c8732153f633afb76d2a1b559b85。原fail归因后同Owner新批`pricing-http-2`，session28027，54项四suite及layering在途。沿现有本地构建策略使用C1，实际命令/工具链固定于driver及result，不改生产JVM。
- Web bf6d870ba85368b0e0c5ade3c44f83f0f2d9e7d8/treebb9f79127e827ab66213856f070c1b81114a54bf：两入口共用面板，按冻结套餐发mode，显示权威类型，所选类型不匹配禁止确认；useHallData旧免费调用不再发请求。未知历史重整没有planId时仍恢复原server操作，不清空/重换资金操作。脏源码诊断51项通过；同源正式定向`pricing-web-1`正在收集，不能当最终生产构建。
- 原型先行：仅定向改现有脏原型baseline-ui.js的报价函数和spec新增段，其他修改保留、未整体提交。新增`scenario=rent-selfhost`展示200文首费/50文续期与类型不匹配文案；node --check通过，127.0.0.1:18786的index及新JS实际HTTP200、回读命中该场景。产品浏览器脚本已扩展三视口两种选择，本轮尚未跑。原型是离线示例，不代表生产扣费。

- `pricing-http-2`生产编译通过但测试编译FAIL/284.488秒：新AgentControllerTest三处直接调用及反射签名把HttpServletRequest/byte[]顺序写反，按真实签名统一修正，API最终候选 **3fdfb9d72480105e9a6e4e9c04b90b41d7503b3c/tree96c480f163064d143e26ac8af78c4ac4d0206120**。原fail归因计数为1，authorize-remediation因无blocked状态拒绝；正常同Owner transition后再运行，未跳过根因修复。
- **pricing-http-3：54/54测试通过、layering通过、Gradle exit0/257.117秒，外层driver异常结束exit143，原因未证明。** session89249已终态、无遗留子进程；原result.json停在RUNNING，保持原始文件不伪写PASS。另存`completion-audit.json`逐个XML/摘要/固定source/log核验，标TESTS_PASS_WRAPPER_INTERRUPTED及publishable=false。不能说本批外层driver正常PASS，也不用为已有完整同源测试结果盲重跑；最终发布仍须正规fresh制品回执。
- Web **bf6d870**同源正式定向`pricing-web-1` **51/51通过、13.064秒**。实际Vue/控制器浏览器回归在同目录`browser/result.json` **18检查/18截图/0异常，60.982秒**，1440/390/320三视口均覆盖原租约状态、首费清单、取消、过期重新报价、自部署200文首费/50文周期、方式不匹配禁确认与local确认请求；HTTP/身份是明确合成fixture，不是生产或真实资金验收。已查看320px不匹配截图，文字正常折行、无横溢，底部操作在既有面板滚动区；Chrome/Vite已退出。
- 当前API/Web工作区均干净，Runtime源码未动，生产API/Runtime/李逵版本未变。磁盘剩余约179MB（普通盘），未清理未知包/备份，不转内存盘；最终打包前须按已有策略处理本任务可重建输出并保留包外证据。
- 下一条主线动作：两种部署存量30天过渡的真实登记/首个调度、legacy规范ID保留实例重邀、真实自部署首次/重邀链路（不能把static已有实例当新建prepare）、生产DDL/ES/主机证书端点配置、最终固定制品/受控安装与真实Web/WS/扣费故障验收。**报价入口闭环不等于本轮总需求完成。** 当前没有在途构建或浏览器，用户无新增确认事项。
