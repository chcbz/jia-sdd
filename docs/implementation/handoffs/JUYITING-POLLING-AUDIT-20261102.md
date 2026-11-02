# 三端轮询盘点与优化方案

核对日期：2026-11-02。Owner、完整commit/线上来源及授权边界见同目录 `JUYITING-POLLING-20261102.md`。

## 最新实施状态（2026-11-02，覆盖下文历史候选状态）

用户决定先完成前端，API/Runtime方案暂不采纳、不修改。Web1.16.95 / `362f2fc094e89eff853d81c0e3c2b9f086356b55`已合develop，Flow4403172/407测试/构建/上传成功；未部署。下表仍保留审计时的原始频率和问题，不代表修复后线上状态。

前端已落地：技能市场无待办停止timer，活跃操作按原change查询；打开/返回前台/匹配本地跨页签通知刷新权威目录。已完成技能结果退出定时扫描，但显式刷新/返回前台/作用域变化仍核验全部引用。场景/回复读取在途去重，旧生命周期延迟回调失效；成果、验收、个人执行、点将/托管等待、案卷问答在隐藏页暂停相关后台读取、回前台恢复原任务。不会因暂停观察而取消后台业务或重放写请求。

同步边界：技能市场保持前台且无本地待办时，不再周期发现其他设备的外部目录变更；需手动刷新或下次返回前台读取。storage事件只覆盖同浏览器共享存储的相关变更，不是服务端推送。保留此明确取舍，不宣称实时跨设备同步。API/Runtime的“唤醒+退避”只是讨论候选，不作为下一步默认实现。

## 结论及证据边界

不是“所有定时器都应删除”。目前混合了界面刷新、持久任务发现、失败恢复、租约/保活、动画与局部等待。没有发现可以不经替代直接删除全部Runtime命令查询的依据。现有WS在线不代表覆盖原生HTTP命令队列。

- **确认的浪费**：技能市场无待办也每2.5秒重读目录/变更列表；场景REST降级在隐藏页继续查询；议事异步interval没有在途保护。
- **隐蔽的后端轮询**：任务SSE每订阅默认5秒查询持久事件高水位；不是纯保活。把HTTP改为SSE并不会自动消除数据库扫描。
- **常驻成本**：Runtime每Agent两条3秒命令发现通道；后端250/500毫秒级任务扫描。优先减少空查询及不变数据的重复读取，而不是给所有请求增加缓存或扩大超时。
- 本报告频率是源码默认值，不是线上请求计数。按短请求计算：技能市场两个基础GET约48次/分钟/打开实例（额外逐项状态查询另计）；Runtime两通道约40次/分钟/Agent，3个Agent约120次。串行等待、在途保护、暂停和实际配置会改变真实频率。
- 生产前次慢日志/JFR只证明这些链路进入热点，不能据此推导全部请求数、空查比例或本次优化收益。没有进行新的生产压测、部署、数据库变更。

线上来源对照：29个Web快照中28个与Web401来源commit相同，JuyiHall.vue差异是另项展示改动；16个API调度文件均与API439来源commit相同。见证据 `online-source-comparison.json`。这是Git来源对照，不冒充逐字节线上安装核验。

## Web：网络轮询和恢复

路径均相对固定Web源码 `339f3be8` 的 `src/`；不是用旧脏工作区推断线上。

| 位置 | 查询/默认周期 | 启停与现状 | 处理 |
| --- | --- | --- | --- |
| composables/useSkillMarket.js（SkillManagement消费） | Agent skills目录、skill-changes列表、逐条change；2.5秒 | 面板show/embedded开启，关闭/卸载停止；递归串行，但无待办也重复全读；浏览器隐藏未单独停 | **最高优先优化**：目录打开/手动刷新/操作终态后读取；活跃操作仅查对应change。无待办停止快速查询；若要观察其他端变更，保留明确的低频补偿或事件提示，不能默默失去同步能力 |
| composables/juyiting/useHallBackendSceneState.js | scene snapshot；15秒 | SSE关闭/不支持才REST降级，不是常态两套并跑；focus可再读；interval没有在途/隐藏保护 | **本轮候选修复**：同生命周期snapshot singleflight；隐藏tick不请求，回前台补读；旧生命周期不能覆盖新状态 |
| composables/juyiting/useHallConversation.js | request权威状态 + conversation/content；2秒 | 传输结束但未完成、失败恢复、不支持事件流时开启；可能与恢复后的事件流同时存在；async interval可重叠 | **本轮候选修复**：每轮在途保护和已清除timer回调失效；看到正文但request仍busy不得提前停。后续按事件覆盖范围合并兜底与事件触发读；不能仅凭SSE连接成功就删除 |
| composables/juyiting/useHallSkillResults.js | 每个引用execution/result；2.5秒 | 只有非完成且非FAILED/CANCELLED结果续查；scope变更abort；有controller防重叠；每轮遍历全部引用，包括同批已完成结果 | 建议以未终态引用为快速刷新集合，事件提示补读；终态保留投影不等于永久缓存权限，重入/身份/授权变化仍重新读；隐藏页生命周期可补 |
| components/juyiting/BountyExecutionOutputs.vue | 成果目录/请求快照；2.5秒 | pendingAction或pending request时续查；不是永久常开 | 保留未知结果核对；与同任务验收组件是否同时挂载重复查须浏览器验证，再在已有Owner合并，不建全局缓存 |
| composables/juyiting/useHallBountyAcceptance.js | 原会话request catalog；2.5秒 | 有未完成请求且task未完成才续查；有loading/pollQueued与scope代次 | 保留；优先复用已有请求事件提示，补隐藏页暂停；不取消服务端任务 |
| composables/usePersonalWorkspaceExecution.js | execution状态；2秒 | 非终态才递归，失败显示错误，身份/销毁失效 | 保留当前执行观察；可补隐藏页暂停/返回补读；不重放执行POST |
| composables/juyiting/useHallPointAndStart.js | 原点将意图状态；1秒 | 仅PREPARING，作用域改变/显式stop/销毁/状态变化停止 | 保留原键只读恢复；不要因等待久自动换键重发；可按已有状态事件收敛 |
| components/world/JuyiHall.vue pollHostedPointRoster | loadAgents/roster；2秒 | 等待本次托管Agent上线，离开该流程或上下文变化停止 | 可用已有Agent状态事件触发核对指定目标，断线才兜底；不要用地图列表替代roster授权数据 |
| composables/juyiting/useTaskWorkspace.js | task snapshot + SSE；降级15秒 | 已有递归、poll token、隐藏关闭流/清timer、指数重连；恢复后回SSE | **保留已有优化**，不另造调度框架；只在实测发现focus等重复触发时局部修 |
| composables/juyiting/useArchiveReader.js | question snapshot恢复 + SSE重连；失败1秒 | 非正常持续拉全量；恢复失败固定1秒再查，context失效停止 | 建议失败指数退避+jitter，区分不可恢复认证/协议错误；前台补读，保留持久问题状态 |
| components/chat/Chat.vue | 会话SSE失败重连；2.5秒 | 固定延时；另有删除失败有限重试，不是状态轮询 | 建议统一采用已有终态错误不重连、隐藏暂停、指数退避的策略；删除重试不混入读轮询优化 |
| utils/pwa.js | SW registration.update；5分钟 | 全应用级更新检查，不是聚义厅业务轮询 | 低优先；可在hidden/offline跳过，HMR清理；不是本次CPU首要依据 |

**不计为持续网络轮询**：hallRequestReadbackScheduler的事件防抖/在途合并/尾随补读；议事动作后的1.5/5秒有限补读；panelChatLoad的0ms调度；自动保存防抖；气泡、录音计时、租赁tick、滚动、游戏帧与资源加载timer。miniProgram bridge的25ms是本地能力检测，非HTTP业务刷新。

## API：数据库发现、持久恢复、事件与保活

路径定位在固定API `aa6ecf93`，详细文件见证据目录 `api-schedules.txt` 与 `source/api/`。

| 类/模块 | 默认周期与工作 | 处理原则 |
| --- | --- | --- |
| ArchiveQuestionWorker | 250ms：enabled时recoverOnce + 过期/待领取扫描；执行期间另有租约续期 | 高频空查候选。事务提交后唤醒 + 持久补扫；或空闲退避。续租独立保留，不把空闲退避用于活跃lease |
| ChatDeliberationOutboxRelay | 500ms：有容量时discover/claim；dispatch/cancel/final/action；执行中另有heartbeat | 保留outbox一致性。可在提交后唤醒、失败/空闲退避；不能用内存事件替代持久outbox，不能取消FINAL/取消投递 |
| ChatBountyBootstrapRelay | 500ms：一轮一次持久claim；有polling互斥、相同失败停止机制 | 不删；复用唤醒和补扫设计。先测空查率/业务唤醒延迟再定频率 |
| AgentOutboxRelayScheduler | 默认250ms（配置）：Rabbit就绪且有容量才discover、claim、publish、settle | 不应按默认周期声称线上已启用。低频补扫/事件唤醒可优化，但保留确认与租约 |
| AgentCommandReissueCoordinator | 默认1秒：消费重连signal，再reissueDue扫描 | 已有重连信号，仍每次扫到期。可按下一到期时间安排补扫；不能丢ACK超时/进程重启恢复 |
| SkillInstallRecoveryService | 5秒：按配置租户/client发现same-wire恢复候选 | 保留已发命令恢复；不重复安装，不放宽原键/授权；按next_due索引和候选集合优化 |
| HostingRentReconciler | 5秒：配置/schema/provider有效时读取pending意图；wake标识非持久事实 | 保留补扫，不能只依赖wake；可用wake加速，空闲慢扫，不改费用/授权语义 |
| ChatBountyExecutionRelay | 5秒：pending(16)协调 | 保留执行事实协调，不自动重试付费执行 |
| ChatBountyAssetRelay | 5秒：分页64遍历pending投影 | 保留已提交成果投影及撤权保护；可由输出提交事件唤醒+持久补扫 |
| AgentStatusMonitor | 10秒：WS状态同步 + 心跳过期扫描 | 必要离线检测，不能与界面刷新一起删；可确认不变状态是否仍产生更新 |
| AgentTaskEventReplayServiceImpl | **每SSE订阅5秒**触发catchUp，读取数据库事件高水位；另接收事件hint | 是服务端真实轮询，不只是keepalive。可减少不变高水位查询/按相同授权scope合并hint；丢hint补偿仍必须存在，不能跨身份共享授权结果 |
| ArchiveQuestionSseService | 15秒：访问策略检查 + SSE heartbeat | 保活/访问收口，不是每次全量读业务表；保留 |
| ArchiveQuestionWorker / VoiceLeaseGuard / ChatDeliberationOutboxRelay的lease heartbeat | 活跃操作按lease续期，部分同时检查撤销/终态 | **保留**，不能套用隐藏页/空闲退避；需要分别证明授权撤销与lease时效才可修改 |
| MemoryJobHandler / JobExecutor / WxSchedule | 每小时同步 / 每分钟cron巡检日志 / 每日07:30 | 定时业务，不是高频聚义厅刷新；本次不改 |

额外发现AgentTaskThreadServiceImpl并发建线程后的5次10ms数据库核对、BoundedAuditDispatcher失败指数退避，均非空闲常驻全表扫描。额外扫描了Thread.sleep/递归while/响应式interval：文件读取、分页、协议流消费不是轮询；关闭时等待、审计重试等另列，不按文本命中误算为数据库常驻扫描。每个后台任务的线上enable、SQL耗时、空查率和实际索引需用运行证据确认，本轮不为未测热点擅改领取/租约/事务逻辑。

## Runtime：不能仅因WS已连接而删除HTTP发现

固定源码 `/home/isp/wsps/chcbz/isp-install` commit `32416ed5`；本任务只审查CYF相关 `conf/codex-bridge/`、`conf/cyf-agent-runtime-v1/`。

| 位置 | 工作 | 决策 |
| --- | --- | --- |
| agent-client.mjs startWorkspaceFilePoller | 即时+3秒 workspace commands；WS OPEN且未pause；独立inFlight | 不能直接删。建议将其角色明确为可靠队列补扫，若现有WS能承载完整“有工作”提示则提示即时触发、空闲补扫退避；独立lane保留 |
| agent-client.mjs startNativeConversationPoller / skill-conversation.mjs poll | 即时+3秒 conversation-executions/commands；串行、独立lane；同时扫描本地pending记录 | 保留发现/恢复；本地扫描每轮读取历史command与attempt/receipt，技能执行历史增长后也有I/O成本。可让当前进程只维护未完成索引、启动/异常时核对持久记录，但不能删除历史事实或把索引当授权 |
| skill-conversation.mjs unknownRetries | 单命令UNKNOWN已有15秒→最多5分钟退避+jitter，其他执行不被饿死 | **已有优化应保留**；外层3秒发现仍发生。非UNKNOWN的失败不能偷偷吞掉/猜成完成；分类可恢复性后再调整调度 |
| agent-runtime.mjs heartbeat → execution-adapter.mjs | 默认30秒presence；channelConfirmed后reconcilePositionSkills，再reconcileArchiveJobs | 保留心跳。技能/案卷发现不是心跳本身，未来可分离为事件驱动但不必新增独立常驻timer |
| position-skill-reconciler.mjs | position-skills GET；每轮至多两phase，先补报pending结果，inFlight合并 | 心跳周期触发，不是3秒原生命令poll的一部分。授权来源必须仍在API，不能以缓存岗位权限免除撤销检查 |
| archive-job-reconciler.mjs | archive/jobs发现及每job结果/source/提交；有inFlight | 前一步岗位对账失败会阻断本次案卷对账，属于有依赖的现状；改造先确认岗位就绪需求，不能简单Promise.all改变语义 |
| app-server-adapter/agent-client | RPC超时、启动时每10ms检查/proc进程树的可执行文件身份、进程退出/中断等待、重启退避 | 与API查询分开计；启动身份检查不能靠spawn事件直接替代（包装进程不等于测量目标）；只在证明身份不变量后优化，非本次网络轮询热点 |
| skill-conversation / agent-client | fence lease续期与到期处理 | 必要安全恢复，保留；不能等界面可见再续期 |

优先顺序：先去掉无工作仍拉全量、在途重叠、隐藏页读；再为命令发现增加**状态变化唤醒 + 有抖动的空闲/故障退避 + 重连即时补扫**。长轮询/SSE若另加新连接会增加服务器挂起请求和授权维护成本，不预设优于现有WS提示。

## 实施与验收

首批局部变更仅Web内部生命周期，无字段、UI样式、按钮或操作流程变化，因此不新增交互原型。一个规则仍由其composable负责；API/Runtime只交付审计及策略，不机械联动。

- 场景singleflight覆盖fallback tick、focus、retry/resync；隐藏tick无HTTP，回前台补读；stop/restart隔离，旧响应/错误不能污染新状态。
- 回复轮询每timer一条在途链；清除后的排队回调无效；保留请求完成与正文完成的区别。
- 定向回归：`tests/juyiting-hall-backend-scene-state.test.js`、`tests/juyiting-hall-conversation.test.js`，75项轻量Mocha通过；没有应用构建。日志 `/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/web-targeted-tests.log`。
- 自检曾发现旧测试在clearInterval后仍手动调用保存的回调，掩盖“正文出现即提前停止请求核对”。修复责任点在loadHallConversationContent的停止条件；不是删用例凑通过。
- **尚未云端正式验证、合入、发布或证明线上流量下降。** 本地定向验证不替代Flow。保留待验候选，不能把全盘点当全整改。

下一步优先处理技能市场：需同时覆盖面板打开、无待办静止、本地提交/恢复后重启观察、其他页签操作、失败与未知结果、返回前台、权限切换、卸载及最终目录刷新。对多组件同任务重复读，先以浏览器network initiator证实并发挂载，再复用已有请求Owner；不创建长期全局权威缓存。

候选源码：`5eaf8e1191abc859043953bdc4e01f53a9e2cb79`（tree `8ac2352b615d58fe1fe63ec33d7b4c9b61aae9ed`）。仅本地提交，未push/合入。定向ESLint仍有2项固定base已有错误，复跑base确认相同；未新增lint违规，但不宣称lint成功。git diff --check通过。单独worktree保留用于后续正式验证，不是已发布版本。

## 部署补充（2026-11-02 18:32 CST）

用户后续授权部署，Web1.16.95 / 362f2fc / Flow407已安装并验证612个本机文件及11项公网入口/相关资源摘要；详见JUYITING-POLLING-20261102部署节。本补充替代上文“未部署”的当前状态，不改变历史审计频率或意味着API/Runtime方案已实施；生产请求量改善尚未实测。

## 事件/阻塞等待复核（2026-11-02 19:07 CST，仅方案）

本轮fetch成功，固定API origin/develop ef702265c2aee075ab077f8e94b9963a4ef58ed9、Runtime origin/develop 9ac44c2fdeb390202497d4bff6e7de36078cc3c1；不将其当线上版本。定向快照位于证据目录event-design/；未修改API/Runtime源码、配置、服务或执行新构建。

结论：高频轮询不是业务必需；应以事件驱动与无工作阻塞等待为正常路径，而非只延长轮询间隔。阻塞队列解决等待，不自动解决事务提交与消息投递一致性、跨进程通知和恢复。

- 现有AgentTaskEventBroker已经使用ArrayBlockingQueue作为线程池任务队列，但明确是process-local/lossy hint，无订阅或队列满允许丢弃；AfterCommitPublisher投递异常只计数/日志。ReplayService订阅hint之外每订阅另设periodic catch-up。这是现有5秒数据库补读的具体原因，不能只删timer，也不应把“已有队列”当可靠事件覆盖。
- AgentOutboxRelayScheduler在Rabbit gate/readiness通过后仍定时discover/claim/publish/settle；AgentCommandRabbitConsumer已有RabbitListener/manual ACK但条件启用。仅接Rabbit consumer不能消除数据库→消息的outbox扫描；实际线上启用范围/多实例拓扑本次未核验。
- Runtime原生conversation与workspace各有独立3秒定时发现；WS OPEN并不代表这两lane有推送通知。可在既有认证通道扩展定向工作可用通知，保留原HTTP权威领取与独立lane执行，不把原生执行塞回旧WS runner。注册通知与补读要有无丢失握手/游标，重连和启动恢复未完成事实。
- 拟议正常路径：同事务写业务事实/工作项→可靠通知或after-commit加速→所属消费者按ID/分区领取→执行/原键ACK；无工作阻塞。内存只存小型ID/版本/到期索引，不缓存技能包/全部历史；队列满须合并dirty标记或可靠补读，不能静默丢失。Node侧异步事件等待，不阻塞事件循环。
- ACK超时/租约过期/重试改按最早到期项调度，到期重新核对数据库版本/锁；启动重建索引，提前插入必须唤醒，跨实例变化要有通知覆盖。时间驱动不能只依赖业务事件；活跃续租/心跳保留必要周期通信。
- 若要求连周期性补扫都没有，须可靠衔接DB提交与通知：例如持久outbox由binlog/CDC捕获并送可靠MQ，消费者确认/幂等，断线重放。只在afterCommit直接发MQ仍有提交后进程崩溃窗口；仅publisher confirm不能原子化DB+MQ双写。CDC不是本轮默认新增组件，需结合已有基础设施成本讨论。
- 暂定建议是先明确是否接受一个低频的集中异常补偿扫描：接受时复用现有持久表+提交后唤醒+有界等待+到期调度，删除每worker/每Agent/每订阅常态高频空查；不接受时再选择可重放的可靠变更传递。两者均不应把“事件+原有固定轮询全保留”当最终优化。
- 必要验收：提交后通知前崩溃、通知重复/积压/丢失、ACK丢失、重连握手竞态、队列满、租约/撤销/身份切换、多实例路由、重启恢复。空闲业务发现请求/SQL应归零（若保留集中补偿则单独计数），不以断开正常业务或取消续租达成。性能数字须实测，未实施。

## 长期架构与CAP复审（2026-11-02，讨论稿、未实施）

修正前述表述：事件驱动+持久工作项/outbox+幂等消费+恢复对账可以是长期方案；轮询publisher和事务日志订阅是outbox的两类实现，不应将CDC或绝对零轮询设为成熟度门槛。需消除的是每组件/每Agent/每订阅常态高频重复发现，不是删除所有时间驱动与恢复活动。阻塞队列仅为进程内调度，不能成为已受理任务的唯一存储。

建议职责：业务事务原子保存事实及对应工作项/outbox；提交后信号加速已归属relay，可靠投递通过既有MQ（实际启用/拓扑待核实），或同进程从持久工作表领取；Runtime复用认证WS工作通知与原权威领取合同，持久接收确认与执行结果分离；完成结果在API同事务提交事实及事件，Web按游标补读。多实例通知路由、满队列、丢ACK、重启恢复均需闭合，不能假设进程内信号可跨实例。复用现有持久表和状态机，不为模式名称另造一套账本。

CAP按操作讨论：C是线性一致性而非ACID字母C，A不是返回任意HTTP错误也算成功，网络分区时不能同时承诺两侧协调操作的强一致及全部可用。DB+MQ提交间崩溃窗口首先是双写原子性问题，outbox不消除CAP；Polling与CDC主要改变传播延迟/负载/运维成本，不自动切换CP/AP。不将整个CYF简单贴CP或AP标签。

建议业务取舍：任务归属/授权/扣费/权威完成事实优先安全，无法确认权威时不批准新的冲突写入；任务受理可在DB权威可用而MQ不可用时同事务持久保存并明确待派发，不声称已执行；展示在既有会话权限边界内允许过期状态并标明断连/版本，不用展示副本作业务授权。取消已受理不等于离线Runtime已停止，撤权生效时点与离线执行能力必须明定。活跃执行仅在既有有效授权/租约合同内继续；外部不可逆副作用无法靠消息ACK/租约自动实现exactly-once，未知结果不得盲目重放。fencing仅对验证令牌的受控资源有效。

可靠性目标：至少一次投递+业务幂等+每任务版本/顺序约束，消费者持久接手后才确认，旧执行者结果由权威存储拒绝。中断恢复依赖原任务键，不创建新业务请求。保留按到期时间调度、启动/重连恢复及按持久不一致候选的分区对账；对账不是自动重跑模型/扣费。低频补偿是可持续选择但须有明确延迟目标、索引/范围、错误归属和积压观测，不能称“低频”即认为成本小。

部署前仍须核实：MySQL复制/故障切换和读取路径、Rabbit实际开启范围/队列类型/确认模式/跨故障域布置、Runtime持久inbox与幂等覆盖、外部调用幂等能力、断连下租约/取消语义。Rabbit quorum队列需要多数派才工作，不因使用MQ或单机多进程就声称高可用/整个应用CP。CDC应由既有infra能力或relay负载/传播延迟实测驱动，不为消灭少量扫描默认新增。

一手参考（只用于模式论证，不作为项目上线证据）：Gilbert/Lynch《Perspectives on the CAP Theorem》；Microsoft Azure Architecture Center《Implement the Transactional Outbox pattern》；Chris Richardson《Transactional outbox》（Polling publisher/Transaction log tailing）；RabbitMQ《Reliability Guide》《Quorum Queues》；Kubernetes《Controllers》；Debezium《Outbox Event Router》；Martin Kleppmann《How to do distributed locking》。本轮仅更新方案讨论，不修改后端/Runtime或发布。

## 代码与实测复核后的第一批落地（2026-11-02）

以同日`JUYITING-POLLING-20261102.md`的源码/验证记录为准。现场Rabbit派发和archive.question未启用，不将它们当作此次线上热点；已启用bootstrap采用提交后提示+单次合并定时调度+5秒遗漏恢复，不引入新MQ或内存权威队列。API2723bdc375经Flow5260799/443验证后合入develop。Runtime1230924已合入develop：历史目录启动/重连完整发现，平时只复核未完成ID；58项轻量回归通过。65条本地文件夹具的20轮打开次数6380→480，仅为扫描策略证据，不代表线上CPU改善。

两者均未部署。Runtime的3秒HTTP发现、WS提示/重连补领/多实例路由、SSE和其他relay仍属后续范围；不能用第一批的局部事件化宣称全链无轮询。未知效果和绑定冲突没有被性能改造改成重放或成功。

## 原生CONVERSATION通知链第二批（2026-11-02，源码已集成、未部署）

API94ab8bf2a6经Flow5260799/444正式验证，Runtime4a89d63经66项本机定向回归，两者均快进集成develop。新旧注册协商后，新Runtime以现有WS工作提示触发权威HTTP发现；启动/重连补读与本地UNKNOWN恢复独立保留。单节点30秒补偿只查询本地订阅的配置分区，空目标不查DB、无排队工作不发提示。提示非持久命令或执行授权；跨API节点/丢提示路径可增加约30秒加处理延迟。

补偿查询的目标索引缺口已补独立显式迁移脚本，真实独占MySQL上一万条合成历史行的EXPLAIN前后回归通过；这不是生产迁移或规模性能结论。新Runtime模块缺制品清单的遗漏已由导入闭包测试发现并修复。合同/回归入口见API `docs/interface-catalog/native-work-notifications.md`，固定版本、正式测试/制品证据见主handoff第二批收口。尚未安装或修改生产数据库；workspace-file、SSE和其他relay继续保留原行为，整体优化仍有后续范围。

## 任务SSE第三批（2026-11-02，源码已集成、未部署）

API604e8d15a6 / Flow5260799/445：每连接5秒timer/高水位读取收口为每API实例单timer、单在途补偿，按完整scope去重并按tenant批量查task-meta。空闲同版本不再逐连接回放；首读、本地hint、独立游标/队列/背压、缺失/倒退/错误处理保留原路径。无订阅零timer/SQL。原5秒补偿周期不变，复用现有作用域唯一索引，无新DDL、Web/Runtime协议变化或正文/授权缓存。

正式受影响回归74项通过（Replay67、DAO6、独占MySQL1）；服务夹具6同scope订阅20轮仅20次批量调用，真实SQL验证字节隔离与现有索引访问，非生产效果数字。源码已快进合入develop，未安装。workspace-file真实生产者仍在，不能直接删掉它的发现与恢复；其3秒轮询及其他relay仍为后续范围。固定证据和兼容/关闭边界见主handoff第三批。
