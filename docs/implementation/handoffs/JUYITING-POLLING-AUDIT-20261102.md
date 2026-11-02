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
