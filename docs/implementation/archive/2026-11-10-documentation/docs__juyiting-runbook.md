# Juyi Hall Runbook

## 全局回归入口（2026-11-10）

聚义厅业务回归统一使用[全局分类操作手册](../specs/juyiting-unified-experience/global-regression.md)与[权威用例数据](../specs/juyiting-unified-experience/global-regression-cases.json)：14类119项，覆盖原核心17项及新增102项。本次只完善定义，119项均未执行；拍照、相册实际调用明确排除。原核心历史通过仅限固定候选及原范围，不替代全局验收；真实UI、隔离故障、双账号、管理写及语音前提见手册。

This is the short working guide for future 聚义厅/Juyi Hall iterations. Use `docs/juyiting-feature-guide.md` for deeper flow details.
For map masking, prop depth, occluder assets, and future map expansion, use `docs/juyiting-occlusion-system-design.md`.
Historical occlusion implementation sequencing is recorded in `docs/juyiting-occlusion-system-execution-plan.md`; current execution and model routing follow `AGENTS.md` and `docs/implementation/MODEL_ROUTING.yaml`.
Historical occlusion visual findings are recorded in `docs/juyiting-occlusion-visual-review-v0.md`; they do not add a separate Reviewer or release approval gate.

## 工作发现与补偿（2026-11-03上线核对）

2026-11-03 08:44核对：API `eb8df08946cf7f150c9c86d20b8eb97fbea50fcd` / Flow450、Runtime `a3238b1b0192339c031197c50e3e99a9a8e6641d` / Flow122（1.3.37、bridge1.1.27）已安装，实际字节/健康及三个Agent连续新鲜通道ready已核验；这不是全量业务验收。详细证据和恢复见 `docs/implementation/handoffs/JUYITING-POLLING-20261102.md`。

- native conversation和workspace-file分别协商通知能力，提交后WS只作提示，HTTP/DB仍为权威；启动/重连补读，漏提示/跨节点通过每节点共享30秒候选补偿恢复。已协商时不再常态3秒发现；历史QUEUED不合法候选仍可引发低频读，不自动重放UNKNOWN。
- Bootstrap提交后合并唤醒+5秒补偿；任务SSE每实例5秒single-flight，完整scope去重批量读metadata，无订阅无扫描。保留独立授权/游标和失败恢复，不缓存事件正文充当权威。
- 议事outbox由全部实际生产者提交后提示、持久重试/ACK/lease到期及槽位释放驱动一个合并timer，5秒集中补偿；保留4槽位、数据库fencing、ACK和续租。未来deadline以扫描起始时刻查询，停机/旧生命周期不能复活调度器。
- API认证注册回执`archiveJobDiscovery:0|1`来自归档Controller同一启用配置；Runtime只停止禁用归档发现，岗位接口不误关。缺字段兼容旧API，旧注册异步尾续不得沿用新会话。UNKNOWN/传输/未确认HTTP/恢复环境错误复用command-local退避，不迁移旧binding、不设业务deadline或自动重放。
- 自然约一分钟窗议事发现从91降至14/13，另新增到期MIN14/13；岗位继续读取，08:26启新Runtime至08:40当前日志未见归档404。CPU未证明稳定改善，不称全部轮询清零。09:11按用户授权备份并删除旧任务544/547及其专属执行状态，不再为两者做恢复兼容。09:40新事项582首轮执行、下载校验及用户验收completed通过；581在原生工具就绪后补充回复并完成。通道ready不代表异步原生工具已就绪，冷启动窗口及单条启动协议帧拒收仍未修复，不能据新执行成功声称所有异常消失。全范围审视及限制见`docs/implementation/handoffs/JUYITING-POLLING-AUDIT-20261102.md`。
- 固定候选分支是来源信息，不使用旧develop名单拒绝真实Run制品；schema工具仍核对commit/tree/identity/receipt/JAR与安装状态。临时systemd安装承载不得在后置失败时清理其启动的生产JVM；后置恢复使用原锁核对已装字节，不重建或重复安装。

## 技能包内存边界（2026-11-02源码及线上来源核对）

实现基线 `ab3da7286f140e32c45e542e9638d2bb5efff2e7`，Flow5260799/437定向496项全部通过。2026-11-02 15:40核对：已由整包发布任务随Run439/`8ad42be7815e499077c6a97439f0f13c96c7650e`安装，来源包含该优化；实际JAR SHA `3e1fb1d77e471915b73c1cd540bbe08ac915c2e91dd5a4f7f989586b22e26422`与记录一致，当前PID1946296、health UP。439整体发布/迁移由REUSABLE-SKILLS-20261102 handoff负责，本节不替代其业务验收。等长自然流量GC短窗有改善迹象，但负载不匹配；后续窗仍出现909ms暂停及明显CPU压力，尚未证明用户体验或整链性能达标。

- 不保留全局ZIP字节缓存。目录、报价/购买准备、安装结果和岗位准备使用不可变包描述；真实下载才读取包字节，冷描述解析也可能暂存整包。下载仍为byte[]接口，不是流式或零复制实现。
- 描述LRU使用16MiB**估算权重预算**，不是精确JVM占用上限、包大小新门槛或拒绝业务条件；超预算描述只用于当次操作、不常驻。授权、价格、安装状态仍读当前业务事实。
- 原生任务在持锁前准备描述，一次同步操作内固定引用，finally释放；缓存淘汰不迫使已准备事务重读ZIP。不要再让事务是否成功依赖某个全局包缓存命中，也不要为性能移除授权/摘要/fence校验。
- 责任与回归见API `agent/docs/skill-package-memory.md`；固定源码、测试、制品和发布状态见 `docs/implementation/handoffs/JUYITING-PERFORMANCE-20261102.md`。发布后须用同类业务流对照接口延迟、CPU和GC；本轮云测不代表线上性能已达标。

## 新版工作台使用指导（2026-10-27源码核对）

覆盖Web `bb9978876a6fe1d8e5bc284e4b4737f654b9caa0`（候选1.16.61），仅HallOnboarding/HallOverview与引导状态；不重标其他模块或当前线上版本。

- 工作台按`home-overview`及760px CSS断点识别手机/PC：手机定位底部导航，PC定位左侧导航；横屏模式不等于PC。入口未显示时保留说明，不自动切页。
- 四步覆盖办事需求保存、事项确认承办与原议事协作/明确验收、资料固定版本复用、我的与重看帮助。引导本身不提交/委派/发送/验收。
- `useHallOnboarding`版本v3；历史v2记录保留，按精确身份隔离。稍后仅本次浏览器会话收起；跳过本版本/完成按原存储策略保留，仍可从“使用帮助”重开。
- 目标取可见节点；贴底固定导航允许高亮，不为8px留白反复滚动。保留背景inert、焦点圈闭/归还与Esc稍后；地图纯说明和虚拟横屏仍兼容。
- 唯一原型仍为`web/prototypes/juyiting/`的help状态。2026-10-27按用户后续授权已发布Web1.16.61 / bb99788 / Flow4403172/349，3454通过、0失败、2既有pending，总224秒；同Run制品、612项安装文件与9项公网入口/资源摘要匹配，部署单71853086为Success/healthy，默认CI-only已恢复。开发CI348不冒充部署Run；随后09:08—09:09只读观察当前线上已为其他发布1.16.62/Run350/1fdae735，其继承bb99788且引导三源码未变，当前入口/引导资源摘要匹配，未由本任务发布或回退。未执行授权账号内交互/真实办事验收。证据见`docs/implementation/handoffs/JUYITING-ONBOARDING-20261027.md`及`docs/implementation/evidence/juyiting-onboarding-release-20261027.json`。

### 引导与导航联动修复（2026-10-27源码核对）

覆盖Web `00b1a6b367ded7764a416a065e49c409360fbfba`（1.16.63），只涉及JuyiHall导航链路；源码实现不等于已上线。引导不再映射成`externalRootModalOpen`，手机底栏继续显示并预留空间，PC侧栏保持可见，两端导航显式inert；引导关闭恢复。普通业务模态、详情与键盘隐藏规则保留，HallOnboarding的背景隔离/焦点圈闭不变。回归需同时覆盖真实JuyiHall显示决策和引导定位，不能只造始终可见导航的shell。正式CI为Flow4403172/352 SUCCESS，3463通过/0失败/2既有pending，121秒；同Run制品与612项文件摘要核验。后续已获授权通过Flow4403172/353于2026-10-27 10:45:01 +08部署1.16.63，总318秒；同Run测试3463通过/0失败，612项安装文件与9项公网入口/资源摘要匹配，原CI-only配置已恢复。线上认证交互未执行。发布证据见`docs/implementation/evidence/juyiting-guide-nav-release-20261027.json`。边界和证据见`docs/implementation/handoffs/JUYITING-GUIDE-NAV-20261027.md`。

## 同平台Agent接外单（2026-10-22核对）

本节覆盖API `94b4c8a5`（1.16.25/Flow223）、Web `44aa9c71`（1.16.37/Flow283）、Runtime `c11a078e`（1.2.3）的D3.1实现和本轮生产验证；下方其他模块保持各自原核对基线。合同与分层证据见 `specs/juyiting-external-commission-mvp/`。

- 同平台由认证的tenant_id和client_id同时精确相同决定，不由显示名/账号名推断。开关属于单个Agent的当前绑定，默认关闭；只能本人在Agent详情内管理。候选为本人Agent及同平台开启接外单的其他Agent，能力仅用于推荐，不引入收费或任务类型准入。
- 两类承办共用point-and-deliberate：选择不执行，确认委派沿原grant快照和自动首轮执行，不增加订单、待指令或二次开始。关闭只拒绝新外单，本人和存量授权不受该开关影响。
- 数据域A（任务/资料/会话）与执行域B（Agent/绑定/Runtime）分别固定；本人A=B。实时执行、租约、聚合及回报共用task/grant-scoped authority，要求当前ACTIVE grant及完整冻结B/binding。历史冻结身份只用于历史读取，不授权实时执行；缺字段不通过本人fallback掩盖。私域Workspace和原本人团队Plan权限未扩大。
- 正式Flow、安装制品摘要、双账号文本/PNG提交验收和本人恢复后实答已核验；这些是本功能范围证据，不等于平台零故障。运行端通道ready不证明typed/model就绪；本轮本人thread/start超时在精确空闲子进程恢复后复测通过，但超时/重连就绪根因仍未闭环。共享运行端已有其他历史未完成任务时，不重启整个unit、清队列或冒充成功；先定位原记录并按实际授权恢复。细节保留于特性handoff及release-20261022证据，不作为自动恢复策略。

## 开发规范入口

遵循 `AGENTS.md`：聚义厅低于 `2.0.0` 均为内测版本，不考虑旧版本兼容，以最新契约为准；Owner 自检，无独立 Reviewer。下列数据边界是当前实现契约，变更时同步更新实现、测试与文档；安全、数据操作授权和 Flow 验证不因内测而取消。

## 典籍阁检索依赖与巡检（2026-10-20核对）

- 典籍阅读与案卷检索分开。案卷检索 `/library/search` 经 `MemoryRepositoryImpl` 使用Embedding和Elasticsearch；本次恢复原ES服务并确认 `chat_memory` 指向 `chat_memory_v2`，认证只读搜索成功，不删除知识库索引。
- 现有每分钟健康巡检新增ES集群和生产索引搜索检查，连续3次失败沿用告警，恢复后解除；不会因ES单独失败重启API/ES。green/yellow且目标分片检索完整才算依赖健康，yellow分类保留。规则、固定凭据文件和安全部署见 `ops/health/README.md` / `CONTRACT.md`。
- API health UP不等于知识库检索可用。2026-10-20早先核验发现OpenAI兼容代理Embedding404后hash伪向量降级；17:35按用户授权改为智谱官方兼容接口 `embedding-3` / 1024维，外置配置仅覆盖 `spring.ai.openai.embedding.*`。`spring.ai.model.embedding=openai` 表示现安装包的协议适配器，并不表示实际供应商为OpenAI；公共聊天连接不变。21条存量案卷已备份并重算向量，保留正文/归属/ID。真实认证写入成功、自然语言查询命中核验案卷第1位，应用落库向量与智谱直接返回向量cosine约1；本次合成案卷已精确删除。
- 17:35的供应商切换仅为原1.16.18 JAR配置维护；随后代码修复通过Flow5260799 Run210/211版本化发布。当前核对的API为 **1.16.20 / Run211 / c09fd09e86ef775c91b21acf63847079c9186c79**，安装JAR SHA `7d711fbe15207a3abbd33a732afdcc39138a80a05161e0df29018890a65f4e60`；Web仍为1.16.24/50107f38，不因后端发布重标前端。当前配置、同Run制品/安装/health证据见 `specs/juyiting-ui-baseline-20261006/evidence/implementation-20261019/remaining-20261020/library-repair-*.json`。
- 向量查询的账号过滤必须在`knn.filter`内部，使用实际keyword字段`jiacn`，不能恢复顶层query与未过滤KNN的OR组合或不存在的`jiacn.keyword`；命中结果再核对source归属。写入使用明确文档ID，读取使用ES hit ID。Embedding必须为1024维有限非零真实向量，供应商失败不得生成hash/随机向量；案卷检索失败返回`LIBRARY_SEARCH_UNAVAILABLE`，不伪装成E0空列表。
- 现有`memory_sync`独立绑定`chat.memory.job.sync-cron`（默认每小时整点），通过既有`taskExecutor`执行；不启用全局JobExecutor的其他cron。手动/定时handler共享Redis watchdog锁，每会话另有共享锁。自动读源仅限活父会话、精确账号/client/tenant归属的USER/ASSISTANT消息；任务线程仍排除，不把SYSTEM运行通知写入个人知识库。
- 同步先捕获消息快照，摘要与Embedding调用在DB事务外；提交时锁父会话并复核生命周期，ES写入成功后仅将快照内PENDING IDs改为SYNCED。ES与DB不是分布式事务：中途失败保持PENDING，以账号/client/会话/快照确定ID覆盖重试，不能宣称跨存储原子性。分页游标在失败后仍前进，避免失败记录独占扫描。四类摘要供应商失败/空内容/无有效summary均报错，不以兜底统计或空JSON标记成功；日/周/月摘要按账号与周期固定ID。没有激活过期删除任务。
- 当前正式回归2746次执行、0失败/0错误、122跳过；本批5个聚焦suite全部执行通过（含真实隔离MySQL）。认证单账号写入/语义搜索、PC与390×844移动端展示/引入草稿，以及浏览器离线错误提示已复核；引用未发送给Agent。**第二账号登录互查尚缺第二个授权凭据。20:00生产自动同步实际触发，但摘要ChatModel失败：当前代理对配置模型gpt-5.5返回HTTP400/model_not_found（unknown provider）；该模型也未出现在当次代理模型目录。合成会话保持PENDING、未生成ES记录，证明失败未伪报成功，但自动入库验收未通过。** 摘要调用的是独立于智谱Embedding的现有公共聊天连接，不能据此判定智谱Embedding异常；未擅自切换公共聊天模型。20:04仅精确清理本次合成会话/消息，21条原ES案卷保留。详见本批`library-repair-sync-*`与`library-repair-summary-provider-diagnostic.json`。
- 20:23按用户指定，仅生产外置`spring.ai.openai.chat.model`覆盖为`gpt-6.1-sol`；代理base-url/密钥和智谱Embedding专用连接不变。切换前真实chat/completions返回HTTP200及可解析的非空summary JSON；原1.16.20 JAR经现行生命周期helper重启，health UP、JAR摘要不变、维护标记移除。配置备份`/home/isp/baks/cyf-summary-model-20261020-201639`。这是公共聊天/摘要模型配置维护，不是新源码/Flow发布；源码内默认值未改，由外置配置覆盖。模型调用验证不等于自动入库验收，新配置下21:00整点同步已实跑成功，详见下条；20:00失败证据保留。
- **21:00真实自动写入与检索闭环通过**（同一API/Web源码基线，生产模型覆盖为gpt-6.1-sol）：既有小时任务21:00:00触发、21:00:43完成；合成普通会话消息变为SYNCED，摘要保留门卡存放事实，ES仅一条确定ID文档、向量1024维；重新登录的测试账号自然语言查询200/E0、目标rank1，PC1440×1000/移动390×844展示通过。未更改cron、未手工触发Job。测试会话/消息/该ES文档按归属和版本精确清理；原21文档及非向量字段复核保留，另有正常同步新增1条，清理后22条，不删除其他会话产物。证据`summary-sol-acceptance.json`及同目录`summary-sol-*`。
- 验收边界：第二账号真实登录互查仍缺授权凭据；日/周/月定时窗口未在本次生产实跑，沿用正式定向测试。当前“引入传令”按Web既有逻辑生成120字摘录并附引用ID，长JSON可能截断关键事实；本次确认草稿被填入，未发送给Agent，也未证明Agent会按ID读取完整原文，不将它写成“全文引用端到端通过”。这是既有引用行为，未在本次读写修复中扩展UI/全文注入。
- 后续聊天连接调整不得覆盖Embedding专用连接；换向量模型须同步核对维度与已有向量重算，不能只改模型名称。本次保留21条已重嵌入的存量案卷，没有再次重算或清理它们。巡检工具原核验范围仍以`elasticsearch-health-restoration.json`为准；原缺陷和切换失败批次保留历史证据，不改写为成功。其他章节仍沿用原基线。

## Primary Files

| Area | Files |
| --- | --- |
| Page composition | `web/src/components/world/JuyiHall.vue` |
| Map stage | `web/src/components/juyiting/HallStage.vue` |
| Map character token | `web/src/components/juyiting/AgentToken.vue` |
| Roster panel | `web/src/components/juyiting/AgentPanel.vue` |
| Bounty/task panel | `web/src/components/juyiting/BountyPanel.vue` |
| Chat/command panels | `web/src/components/juyiting/ChatPanel.vue`, `web/src/components/juyiting/CommandPanel.vue` |
| Selected agent summary | `web/src/components/juyiting/SelectedAgentCard.vue` |
| Data loading | `web/src/composables/juyiting/useHallData.js` |
| Conversation/events | `web/src/composables/juyiting/useHallConversation.js` |
| Movement/positioning | `web/src/composables/juyiting/useHallScene.js`, `web/src/game/scenes/HallScene.js`, `web/src/game/entities/HallAgent.js` |
| Role portraits | `web/src/composables/juyiting/useWaterMarginRoles.js` |
| Constants and role metadata | `web/src/constants/juyiting.js` |
| Visual assets | `web/src/assets/juyiting/` |

## Current Data Boundaries

- `mapAgents` is for the map stage and comes from `GET /agent/map`.
- `agents` is for roster, recommendations, ability options, and selected-agent detail surfaces.
- Roster filtering calls `POST /agent/roster`.
- Task search calls `POST /agent/tasks/search`.
- Task assignment calls `POST /agent/tasks/{taskId}/assign` with an explicit `agentId`.
- 普通事项推荐使用 `POST /agent/tasks/{taskId}/recommend` 的结构化对象合同（`expectedTaskVersion`请求，`state/recommendations/evidence`响应）；与团队推荐/自动指派区分，不保留旧评分数组兼容。手选不依赖推荐成功，确认承办仍走原授权链。当前合同见 `specs/juyiting-assignee-recommendation/spec.md`。
- Runtime abilities are client-owned snapshots: `agent.register` and `agent.presence` may refresh `agent_runtime.abilities`; persona abilities are fallback defaults only.
- Juyi Hall chat sends through `POST /chat/stream` and receives events from `GET /chat/conversation/events`.
- 招贤令 binding calls `POST /agent/personas/{personaCode}/bind`。`mode=server` 沿用租约/预留/intent，最新开发源码接入同一个统一 Runtime，不再通过旧 codex-ws-agent broker 安装；源码与上线边界见下节。`mode=local` 本轮未改，不据此推断其新验收状态。
- Do not use `/agent/active` for Juyi Hall.

### 待承办需求：当前态与执行快照（2026-11-04局部核对）

覆盖API `1899d2fd164e097d9b11b86f535f36b29da0f1a1`、Web `6f0030ddfb45f411b9174ff1e3d06af8d15e91bd`。只更新普通待承办事项编辑边界，其他模块沿用原基线。

- 每事项一条当前需求，标题/描述覆盖更新，资料使用既有固定版本链接。详情与推荐读当前态，不扫描审计历史。真实变化递增并发字段；无变化保存保持版本及承办选择，不重复推荐。
- 保存与推荐分开：API原子更新当前态、资料和摘要；Web收到成功回执后，真实变化才以新taskVersion重新推荐。推荐失败保留已保存内容，可重试/手选，不自动承办。
- 创建回执仍保留CREATE快照；承办授权事务冻结当前需求revision作为执行输入。普通编辑不逐次追加全文历史，既有快照/摘要只读保留。最小操作记录用于幂等及丢失响应核对，不是审计历史副本。
- 编辑器视觉核对（2026-11-04，Web `a99d6facf1522f54a5423beb0dbc7aea2ab071b9`）：三入口透明图标；标题/描述弹窗Teleport到body，在组件边界提供原型主题及按钮/输入样式，不依赖厅内父节点继承。保存/并发/推荐契约不变。
- 原GET/PUT `/agent/tasks/{id}/requirements/edit`继续使用；带原Idempotency-Key的GET只核对该提交结果，不写入、不重放。并发字段不能替代owner/状态/资料权限；责任集中在既有API服务与文件适配层。
- 新库结构不含CHECK，普通启动不回填。老数据从可信完整快照受控迁入，不从截断摘要推导。新版本接收编辑后回退旧API必须停写并补齐旧读取所需的精确业务快照，不能直接恢复旧库覆盖新事实。

合同见API `docs/interface-catalog/task-requirement-edit.md`；安装及线上验收证据分别见 `docs/implementation/handoffs/MATTER-EDIT-20261104.md`。本轮未建设通用审计系统。

### 初步任务取消（2026-10-10源码核对）

覆盖 API `36d9e5452ab8beb64b97e5570da6ede10ec38797`：所属用户调用 `POST /agent/tasks/{taskId}/cancel`，JSON 仅含整数 `expectedTaskVersion`；成功返回 `{taskId,status:"cancelled",taskVersion}`。这是后端接口，未新增前端取消按钮。

- 初步仅支持无悬赏资金事实、未实际开始的普通任务。已点将但成员尚未开始也可取消；当前执行、租约、指令或不支持的资金事实返回409，不部分写入。原 `/funding/cancel` 暂不删除，不通过普通取消绕资金结算。
- 同一事务退出邀请/已接受成员、取消待执行工作项、撤销ACTIVE执行授权、关闭无租约RETRY bootstrap，释放本任务占用；不启停共享Runtime，不清其他任务占用。保留原点将与历史事件/成果，规范终态Provider消费授权不等于悬赏托管资金，不能因此退款或重新付费。
- 已取消的完整终态任务可用原taskVersion重复请求，回读现有结果，不新增事件/版本/退出时间。LEFT/REJECTED的completedAt是原状态服务写入的退出时钟，不应误判为实际开工证据。
- 实现入口为 `api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskCancellationController.java` 与同组件 `service/impl/AgentTaskCancellationServiceImpl.java`；定向回归入口 `:agent:jia-agent-service:initialCancellation`。发布/具体生产操作证据单独见 `docs/implementation/handoffs/GSS-CANCEL-20261010.md`，不以源码核对代替线上成功。

### 统一 Runtime 托管接线（2026-10-10源码与本次生产核对）

覆盖 API `33e2344a2af02bb908a20bec1125ab7c23e8d00d`（1.14.3）、Runtime `80eadc9247132a9d6c6b3b9d7fe7b7f965e094de`；仅此范围更新，不重标其余文档基线。源码实现、安装回执和业务验收分别见下述handoff。

- 原 bind/初租/免费重整接口不变。Reconciler → `UnixManagedHostingProvisioner` 的 `runtime-hosting-v1` 私有 UDS → 同进程 `HostingControl` → 同一个 `RuntimeHost` 的单subject add/recreate；没有第二服务、旧API-key fallback或新付款通道。
- `prepare` 持久化候选而不激活；API短事务精确ensure installation并绑定原initial intent后才`ensure`。新订单通道能力检查位于资金事务外，已提交幂等回执优先回读；保留身份/租约/账本/CAS。
- 初租就绪必须完整operation/installation/host/instance/session证据及API独立`currentRegisteredProof`。进程存在、旧online或持久READY不能单独结算。免费重整沿用installation/授权，产生新session/目标代次，不重新enroll、不改租期/资金、不重启其他角色。
- 新字段：initial intent的`runtime_installation_id`、`runtime_manifest_sha256`、`runtime_provision_generation`；reprovision的`runtime_target_generation`。显式迁移资源`economy/jia-economy-mapper/src/main/resources/db/migration-gss-hosting-runtime-v1-20261010.sql`，本次已执行两ALTER并通过真实MySQL8.0.21精确catalog/触发器验证。应用不自动修补旧/不匹配catalog；新增字段后旧1.14.2 initializer不接受该catalog，本次forward-only，不盲重启旧JAR。
- Runtime配置及唯一installer说明见组件`conf/cyf-agent-runtime-v1/HOSTING-CONTROL.md`：外部私有`hostingControlPath`、独立托管provider模板、`socketGid`与API`socket-group-gid`一致；受限0660 socket与开机tmpfiles父目录。本次路径`/run/cyf-agent-runtime-v1/unified/control.sock`，runnerUid0、socketGroupGid1000。不得复制其他账号HOME/凭据；授权不确定返回RECOVERY_REQUIRED，无自动换钥/遗留锁强占功能。
- 正式后端390通过/分层与fresh bootJar；Runtime157通过/1既有跳过，另桥接2通过。API1.14.3原本地安装器verified/healthUP、Runtime固定release已安装；本次公孙胜原单ACTIVE与一次UI免费重整SERVICE_READY已真生产验收：同installation/session1→2，原租期/钱包/账本不变，三个既有subject/PID/session未重启。旧broker key按原intent精确退役，不批量吊销。
- 完整源码、发布批次、原lease/request、恢复边界与证据见`docs/implementation/handoffs/GSS-REJOIN-20261010.md`。这不是全产品或模型推理验收；未新增订单/任务/赠款，也没有卢俊义账号业务验收。

### 厅内连续问答：本轮收尾（2026-10-11 18:13，已发布/普通密议两轮实测）

覆盖线上Web1.14.6 `7b14dffd5d9d259df720f84e57a8453424fb0a65`（Flow199）、API1.14.4 `fb8a43b0c1b8774582e520a809e5f52337198c25`（本地同批制品原installer verified）。普通密议已实测同话头连续两问、下一轮解锁和重取历史；不是全场景/图片端到端验收。详设及验收边界见 `docs/implementation/HALL-DISCUSSION-ROUND-CLOSEOUT-DESIGN-20261011.md`、`docs/implementation/handoffs/HALL-ROUND-IMPLEMENTATION-20261011.md`。

- 同一话头一轮结束后再发下一轮：结束request，不关闭conversation，不清历史；没有新增并行提问/自动排队/自动取消。
- 普通CHAT/INSPECT POST在完整权威RequestView覆盖本次全部turn且全部终态后EOF；PARTIAL必须检查子turn。buffer先注册再读快照，单POST订阅关闭不影响会话GET events。typed `/interactions`不走该relay，含EXECUTE/未知step不套CHAT终态谓词。
- public/private前端每次发送持有独立session；终态GET释放本轮reader/发送锁，EOF自身不是业务完成。旧回调、poll、finally和正文恢复不能覆盖新轮/换身份；最终正文加载失败与业务终态分开，不重复POST。
- 本次连续问答无新增表/接口/Runtime改动。正式发布后端205项及分层/freshbootJar通过；前端Flow4403172/Run199 SUCCESS（2917通过、2既有pending、0失败）。线上同一吴用密议两request均COMPLETED，第二轮保留上下文，重取保留4条消息；public多Agent线上未测、浏览器主动收尾不等于独立观测服务器自然EOF，具体边界见handoff。
- 图片链路当前核对（2026-10-11）：Runtime配置根为`/home/isp/conf/cyf-agent-runtime-v1`，Runtime1.0.2/`5b902c1`；仅吴用图片配置已启用，不推断其他Agent。新普通事项445已真实生成蓝鸟→基于首图改红鸟→鉴权预览/下载→正式验收→刷新恢复完成；原图可读、当前交付只取改图。最终验收线上为API1.14.7 `cf1402727466e1e51db0860200dc178eab2096c4` / Web1.14.8 `621b87a1b977e5c8fd0ef9cd22b068d7d0622b42`（Flow201）。生成/编辑发生于前一发布1.14.6/1.14.7，升级后未重复Provider调用。内容保留偏差：红图透明背景而非要求白底，不称视觉内容完全通过。证据与分批边界见 `docs/implementation/HALL-IMAGE-RETEST-20261011.md`。
- 图片识别配置核对（2026-10-12；覆盖吴用、Runtime 源码 `5b902c1bcd3efced9720e015e3b8240d39ce0738`）：图片生成/编辑与 `INSPECT` 分开启用。现用 `/home/isp/conf/cyf-agent-runtime-v1/unified-profiles/wuyong.json` 已补齐 `typedInspection*`；真实模型/载体证据在 `/home/isp/conf/cyf-agent-runtime-v1/inspection-evidence/wuyong-20261012.json`。任务450的正常业务接口已走通 `CHAT → INSPECT`，原PNG的 `LOCAL_IMAGE` 摘要回执与蓝鱼/白底识别答案一致；当日接口验证与页面回读通过；独立的页面发送问题已在下述2026-10-13版本修复并单独复验，不能用此前接口验证替代页面证据。`codexHome` 绝对路径不直接进入识别稳定摘要，二进制身份、模型、Provider与隔离策略仍绑定；迁移后须按最新配置重新测量，不复用旧路径候选或伪造能力证据。完整边界/迁移交接：`/home/isp/state/cyf-diagnostics/hall-image-inspect-20261012/HANDOFF.md`。
- 议事发送前检查核对（2026-10-13；Web修复 `92320bc6c15cd6f0328ee99bbf191da2bc9c32a6`，发布1.14.12 `cb730681570688e0051b5cd79737a3c004817881`）：已有榜文会话不能依赖本浏览器的原点将恢复记录来取得 `assignmentRevision`；缺失时读取 owner 鉴权的 `GET /chat/conversations/{conversationId}/interactions/context`，严格匹配事项、任务版本、目标好汉和会话代际，不从历史成果或 `taskVersion` 猜测指派版本。身份/上下文变化丢弃迟到响应，失败不提交、不清空草稿。指派检查先于成果索引检查；同一上下文并发索引刷新等待同一读取，保留后续刷新与旧读取隔离。任务450只读复现为索引准备成功、指派版本为空而答复刷新失败，并非接口读取慢；原统一提示掩盖了真正原因。本机受影响回归386项通过；补充不部署CI `5263692/Run11` 对精确源码2952项通过、2项pending，构建成功。验收页同步透传索引读取错误，不降级绕过核对；前述为源码验证；正式Flow4403172/Run207对1.14.12完成同批测试、构建与部署，364份安装文件及11份公网资源与制品匹配。全新浏览器任务450真实发送一次HTTP202，自动恢复指派并走通CHAT→INSPECT，原PNG的LOCAL_IMAGE摘要一致，新识别答案在页面自动显示；未重复生图或重置START。发布后已恢复原仅验证配置。证据：`/home/isp/state/cyf-diagnostics/hall-image-inspect-20261012/catalog-send/`与`catalog-release/RESULT.json`（同诊断根目录）。
- 新建事项图片资料场景复核（2026-10-13；线上Web1.14.12 `cb730681570688e0051b5cd79737a3c004817881`；仅诊断、未修复）：办事页选择工作空间PNG可成功提交并绑定固定版本，但新点将回执含 `GENERATE_TEXT_FILE`，现有前端 `hallPointAndStartIntent.js` 的操作集合/普通议事权限精确比对未同步，导致服务端已受理而页面报回执不匹配。任务455按界面提供的林冲实测，识别和显式附图后的改图均返回澄清，无INSPECT/EXECUTE子请求、无图片交付；林冲现用profile未见吴用的识别认证配置，受控图像能力只读返回UNAVAILABLE且无providerBinding。后续消息需要另勾选“随本条消息发送”，任务原图未默认随消息附带。此前任务450吴用的已生成成果识别成功不能推广为全部Agent或新建事项资料流程通过。证据 `/home/isp/state/cyf-diagnostics/hall-upload-inspect-edit-20261013/RESULT.json`；先同步最新点将契约并核验所选Agent真实能力，再回归完整入口，不重复点将或重置原事项。
- 图片现行契约（2026-10-11，覆盖上述API/Web）：已提交输出来源按link/request/step的`OUTPUT_COMMITTED`核验，改图源及验收不能仍要求旧`RUNNING`，不加双状态兼容；保持owner/client/tenant、grant、lineage及bytes/hash核对。媒体回执可含序列化的`messageSource:null`，不能误拒；非null混合来源/未知字段仍拒绝，提交请求契约未放宽。验收成功必须同时核operation completed/TASK_COMPLETED、delivery accepted和task completed；页面刷新只读恢复同operation，不自动重POST。

## Role Portrait Rules

- Role matching is done by `portraitRole(agent)` in `useWaterMarginRoles.js`.
- Role metadata is in `portraitRoles` inside `web/src/constants/juyiting.js`, covering all 108 Water Margin prototypes with rank, star name, name, nickname, palette, and motif.
- If an agent has `agent.avatar`, that wins.
- Per-role assets live under `web/public/juyiting-portraits/`: all 108 prototypes have static SVG fallback portraits, plus realistic PNG portraits as 4 single images and 26 `water-margin-atlas-*.png` 2x2 sheets. Do not place static files under `web/public/juyiting/`, which collides with the `/juyiting` route.
- `useWaterMarginRoles.js` prefers explicit agent avatars, then custom generated SVG for `visualConfig`, then realistic PNG/atlas portraits for matched roles, and finally the static SVG fallback. Do not reintroduce the old 3x2 sprite-grid fallback.

## UI Invariants

### 需求入口与事项列表（2026-10-11 源码局部核对）

覆盖Web1.14.9 `a3bceafb53b4bea2545ad3065af058c48400605e`（Flow4403172/203，2026-10-11 21:48 +08:00部署及线上资源核验通过），仅入口/事项列表与取消布局范围，不重标其他基线：默认“提出需求”统一经 `openDefaultRequirementCreate` → `openPrivateDraft` 打开独立 `HallDraftEditor`（draft浮层），宽窄屏及多媒体开关均不再跳到事项内填表。保留现有草稿保存离开保护、返回栈与来源筛选；BountyPanel仅管理既有事项，不再暴露 `openCreateRequirement` 或创建表单/提交事件。已有普通/资金请求结果未知时的核对与原请求恢复入口保留，不代表允许新建。取消区按钮等宽、保留描边次级样式，内部12px间距/上下16px留白；资金展示与撤榜使用原金额校验/事件，普通取消条件和确认逻辑不变。源码与定向证据见 `docs/implementation/handoffs/BOUNTY-TOOLBAR-20261009.md` 的2026-10-11跟进。


- Map filtering and roster filtering are separate. Changing roster status should not remove map agents.
- 厅中实景浮动点将列表用未筛选 `/agent/roster` 的当前用户可操作投影，不用 `mapAgents`；角色型 Agent 还需persona catalog 正向绑定确认，缺失/失败不能把残留 runtime 当作有效绑定。刷新后选中对象按 ID 替换为新 roster/map 对象，不保留旧权限或状态字段。
- `visibleAgents` should derive from `mapAgents`, not from roster state.
- Bounty assignment should receive the target agent from the clicked row or explicit action payload.
- Chat context should preserve selected agent, mentioned agents, selected task, and `scene: 'juyiting'` metadata.
- Keep map controls and fixed-format UI elements dimensionally stable to avoid layout jumps.
- 横屏白屏排查先检查 `JuyiHallEntry` 的 entry/background 明确高度链；反复进入地图时，melonJS 缓存 `loader.load() === 0` 不触发回调，必须处理缓存资源状态并清理等待监听，不能只验证首次横屏。
- melonJS 15 的 `video` 无 `destroy()`：重复挂载还需核对全局 renderer/run loop、当前容器 resize 与输入坐标，不能只测 loader 缓存命中。
- 弹框尺寸由常驻 `useHallExperienceMode.js` 更新，`--hall-visual-height` 仅绑定在 `JuyiHall.vue` 根节点；不要恢复 `HallStage.vue` 的 document 全局高度写入，否则退地图后会残留横屏高度。
- 厅前议事需同时验证 visualViewport-only 键盘缩高与恢复（不改变物理方向）；高度 ≤320px 使用紧凑头部，不能只缩 overlay 而让固定内容遮住输入框。典籍正文、手札各自有界滚动。
- 微信 CSS 全景旋转不是宿主原生横屏；系统键盘方向需在小程序宿主工程处理，不能以 UA 仿真结果宣称真机已修复。
- 典籍从书架进入阅读可复用同实例、身份隔离的目录；必须先读取服务端进度再选取续读章节，不能并发打开卷首并让自动保存覆盖旧断点。
- 典籍进度写入 `PUT /archive/v1/me/progress/{editionId}` 携带 `Idempotency-Key`；跨域排查先验证生产 OPTIONS 的 Allow-Headers。reader 单测必须覆盖真实 `createApi → useHttp → fetch` 边界，不能仅 mock `api.put`。

- 百宝箱执行回执与历史恢复：GET `/agent/personal-workspace/executions` 为 owner/client/tenant 隔离的只读分页，GET `/executions/request` 用原 `Idempotency-Key` 核对；404 不证明在途 POST 未受理。未知意图不能因查看另一条终态记录而被清除，刷新不能自动重复生成。
- Runtime 的精确 `/internal/agent/tasks/{taskId}/runs/{runId}/failure` POST 必须同时具备 Controller 与 native filter 允许路径；客户端 inbox `completed` 不等于交付成功，须看 outcome/服务端终态/可验证产物。见 `specs/juyiting-execution-recovery/`。
- PRIVATE `WORKSPACE_FILE_EXECUTE` 的成功事实是 `OUTPUT_COMMITTED`、owner results manifest 与 owner-safe 文件版本/摘要验证；D03 不发送 legacy `work.result` / `work.result.receipt`，验收不得伪造或要求该回执。

### 验收状态刷新恢复（2026-10-09核对）

覆盖Web `17ecf1c0b581cab1456acff4db097a6a4d335e3d`（1.14.1）的 `useHallBountyFinalization.js` 与 `BountyExecutionOutputs.vue`：恢复合法本地intent后，按operationId或原幂等键自动一次GET回执，不自动resume/POST。核对中与未知/查询失败不能表述成“验收尚未完成”；服务端任务完成与已校验回执完成分开呈现。身份/会话/任务切换及卸载取消旧请求并忽略迟到响应，完成任务不能再次提交验收。刷新复验应同时核对正式成果正文、回执终态与网络中无重复验收POST。

线上交付证据与范围见 `docs/implementation/UR06_REQUIRED_RUNTIME_CLOSEOUT_DESIGN_20261009.md` 当前交付摘要；此条不代表其他账号或历史任务已验收。

## Backend Areas

| Concern | Backend path |
| --- | --- |
| Agent runtime/persona/task meta | `api/agent/` |
| Juyi Hall conversation type and messages | `api/chat/` |
| General task domain | `api/task/` |

Start backend searches with:

```bash
rg -n "map|roster|tasks/search|assign|AgentRuntime|AgentPersona" api/agent
rg -n "juyiting|conversation_type|chat/stream|conversation/events" api/chat
```

## Verification Checklist

As of 2026-10-22, select the relevant web/tests and offload memory-intensive testing/builds to Flow4403172 for the exact remote commit. Lightweight diagnostics, queries, coordination and online verification may run locally; choose by workload, not Node.js/Gradle tool name. Local production packaging is prohibited. Develop does not auto-deploy. Explicit releases bind version, commit and same-Run artifact. End the Run when execution completes; do not wait inside it for other pipelines, ready files or acceptance. Keep deployment integrity, locks and recovery; online acceptance is recorded separately. See AGENTS.md and docs/aliyun-flow-cicd-strategy.md; this policy update does not itself change cloud configuration.

Useful search:

```bash
rg -n "juyiting|JuyiHall|agent/map|agent/roster|agent/active|assign-task" web/tests web/src
```

For visual changes, start the dev server when useful:

```bash
cd web && npm run dev -- --host 0.0.0.0
```

## Documentation Hygiene

- Keep this runbook short and operational.
- Put detailed flow diagrams or long explanations in `docs/juyiting-feature-guide.md`.
- When fixing a repeated issue, add one sentence here under the relevant section so future sessions do not rediscover it.

## 交付与语音诊断

### 已有媒体成果提交（2026-10-21局部核验）

源码基线API `510b2937`、Web `68552ea7`、Runtime `5e8742aa`（2026-10-21续核）；覆盖已有成果引用、提交、单项图片修改/保留文字和验收，不代表新增文件生成能力或其他模块已复核。
- 生成完成不是待验收：完成EXECUTE后，用户在原议事明确提交；多个独立成果先选“本轮成果”，不默认最新、不合并所有临时成果。SUBMISSION_REQUEST仅引用精确父摘要/保留targets，说明不是新的文字RESULT。
- 原DELIVERY_REQUESTED outbox复用finalization；确认真实delivery及submissionProgress后才是正式提交，验收仍由用户确认。新格式扩展生成/预览适配，不在主提交流程加格式分支。
- final读取会校验媒体父链并进入现有任务/输出FOR UPDATE：直接outbox读取、动作读取、混合文字外层必须使用REQUIRED读写事务，不因方法名是read而标readOnly。MySQL1792/25006应查实际Spring外层事务，禁止删锁、改新事务或直接改业务状态来绕过。
- 提交暂态失败保留原event/key及生成结果，修复后由原outbox恢复；不要重生成、重提、清队列。恢复后核对原输出hash、正式RESULT数量和人工验收回执，服务UP不代替流程成功。
- REVISION_REQUEST持久化回放必须传入原始`inspectionInputReceipt`并校验v5封包；不能以null代替原生资料证据，否则读路径报`TYPED_FINAL_INVALID_JSON`，不应误判模型JSON错误。正式修改以固定FORMAL_ARTIFACT输入证明替换目标，未修改项经原版本/摘要/权限核验由后端保留，不靠模型重写文字。
- PNG/JPEG正式图片预览沿用64MiB成果读取契约及既有解码尺寸保护，不复用1MiB小文本阈值；未知格式不因此开放，文本/PDF/Office策略不改。
- API1.16.23/Flow216、Web1.16.35/Flow279下，独立496已实跑混合文媒→只修改图片→保留原文字重交→人工验收，刷新后COMPLETED；移动为模拟视口，非真机。已完成495单图片证据保持原基线。该次验证发现的重入EXECUTE终态忙态残留已于Web1.16.36修复（源码9dbd132e8bc25119c0532cbed672ab7fa4a214b3，Flow281）；原bootstrap与恢复请求共用媒体提示后的single-flight权威GET，按当前request/conversation/EXECUTE绑定，不以媒体消息判完成。“重取回话”先读当前请求再读历史，并保留guard/代际/版本约束；没有新增轮询或业务写。正式回归覆盖该转换，线上仅做496已完成历史的PC/移动只读复查，未重做付费执行，不将此主链路通过当作所有恢复路径通过。完整失败/补漏/发布证据保留既有`specs/juyiting-ui-baseline-20261006/optimization/production-parity-release-20261021.md`。


- TASK 正式 PDF 交付依赖显式启用 `agent.personal-workspace-storage`、`agent.task-artifact-storage` 与独立私有根目录；验收看正式交付列表/manifest及内容下载，不以本地 PDF 或上传 201 替代。
- 语音最新契约见 `specs/juyiting-voice-realtime/design.md`；录音实现路径以对应交付 commit 为准，不将历史候选路径当作当前 checkout 的入口。保留明确 Agent/会话、发送与回复关联，网关凭据不进入浏览器；能力证明、发布、生产启用和设备验收分开报告。
- 转写立即返回 `VOICE_UNAVAILABLE/503` 时检查 Redis 准入；已复现的 Redis4 Lua 限制及隔离回归方法见 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`，不操作生产 Redis 数据。STT/TTS 的原生事件、音频终态与 fidelity 要求按最新语音契约验证。
- 历史启用/测试/发布回执见 `docs/implementation/VOICE_REALTIME_ACTIVATION_20260930.md` 和 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`；这些是历史证据，不代表当前线上 commit 或真实设备已验收。当前状态须核对精确 commit、实际 Flow Run 和在线证据。

### 远端自家接应历史实测边界（2026-10-11，李逵；当前文本能力见下文）
- 核对源码：isp-install Runtime1.0.2/`5b902c1bcd3efced9720e015e3b8240d39ce0738`；受测Web1.14.9/`a3bceaf`、API1.14.7/`cf140272`。仅覆盖李逵在173.230.149.118的独立主机统一Runtime（非与本生产机合并进程），既有installation/enroll、两轮文字密议与事项446文字正式验收；未发布Web/API。
- 主机配置在`/home/isp/conf/cyf-agent-runtime-v1`，状态在`/home/isp/state/cyf-agent-runtime-v1/unified`；新服务`cyf-agent-runtime-v1@unified`，该主机旧`codex-ws-agent`已停用。不要重启旧服务形成双实例。
- 远程接入不止需要`/agent/runtime/v1`与WS：原生文件/技能等还有`/internal/agent/`路径。当前公网网关无对应location，李逵Node请求实际444，文件通道尚未通过；不通过开放全部internal或绕过Runtime鉴权处理。页面旧安装文书也尚未更新。文字验收不代表这些能力可用。
- 来源：`/home/isp/wsps/cyf/docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`、`/var/tmp/cyf-likui-selfhost-20261011-8qhccv/business-acceptance-final.json`。历史服务PID和当次过程留handoff，不作为今后在线状态依据。

### 已取消事项成果操作区（2026-10-11 局部源码核对）
- Web `d8b703b9fae877daf224e159850f0f7c97ccf174`：正式成果与验收页的两个“重新读取”入口使用独立描边按钮组，12px间距、44px最小高度，≤600px纵向等宽；仅布局变化，仍走原历史成果/议事文字读取，不恢复办理或验收。当前只完成本机定向诊断，非上线声明；证据见 `docs/implementation/evidence/terminal-history-layout-20261011/`。
- 2026-10-11 补充局部源码核对 `36c447ceb3f067618df37b934cb813e819aa88b3`：正式成果与验收页（formalTaskRef存在，不限状态）不展示标题栏协作工作台按钮；返回普通事项后沿用原开关与subject条件恢复入口，TaskWorkspacePanel未下线。仅本地定向诊断通过，未发布。

### 2026-10-11 公网自家接应：Runtime原生网关

核对API `cf140272`、Runtime1.0.2与根仓网关配置 `f6f34cd0`。本机Runtime直连127.0.0.1:10018不代表远端链路可用；远端需经api.chaoyoufan.cn的原生路径白名单。配置源码位于 `ops/ci/aliyun-flow/host/nginx/`，安装到 `/home/isp/apps/nginx/conf/snippets/` 并由该域名vhost include；后端installation/session/channel/owner/task鉴权仍是唯一授权依据，不代理整个internal，不注入身份头。

李逵173.230.149.118在实际公网轮询已从444恢复200，原Runtime未重启。此结论只覆盖网关：新事项448的通用文本文件请求停在CLARIFY，当前议事动作清单没有通用文件生成适配；不等同全文件/技能/图片流程通过。详细验收边界见 `docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`，该处历史22:19“未改Nginx”已由后续授权部署记录更新。

### 李逵公网自家接应：文本文件正常流程（2026-10-12局部核验）
- 当前核验组合：API1.14.10/`cd1e6d6ebe`、Web1.14.10/`235048e6`（Flow205）、isp-install Runtime1.0.3/`807b86d`；仅覆盖173.230.149.118李逵的无附件UTF-8纯文本生成、上传提交、预览/下载与正式验收。原448的历史CLARIFY结论不代表新版能力；不回填旧grant。
- `GENERATE_TEXT_FILE`为独立EXECUTE操作，必须同时有当前task grant、`nativeConversationTextFileEnabled`配置及实际ready的文本执行器声明；不是普通聊天任意写盘，也不要求开启图片付费能力。输出text/plain必须同时通过配置和数据库`chk_pwex_output_mime`，不可只更新其中之一。
- 文本动作稳定子请求ID与图片动作的域不同；准入与进度投影共用文本requestId计算，不能把“执行关联不一致”当作文件生成失败而重复点将。完成后按既有正式成果finalization验收，保存到工作空间不是前置条件。
- 原事项449真实文件/下载字节SHA与验收选中成果一致，finalization完成且刷新后事项completed；不代表其他格式转换、文件编辑、图片或全体角色验收。当前下载名为系统output_1.txt（议事卡片part_ID.txt），尚不保留用户指定文件名。
- 稳定源码及边界详见`/home/isp/wsps/cyf/docs/implementation/LIKUI-TEXT-FILE-ACTION-20261011.md`；当次验收、失败与发布证据留`/home/isp/wsps/cyf/docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`。历史PID/批次不作为今后在线状态依据。
- 本文上方两项页面局部优化已纳入Web1.14.10/Flow205并发布；其“仅本机诊断/未发布”描述属于2026-10-11历史阶段，而非当前发布状态。

### 自家接应安装交接（2026-10-12 23:38发布核对）
核对已上线API `0fe830d1ea` / Web `aad2ae9`（均1.14.11）、isp-install develop `a39c085`：local文书提供可信Scope的runtimeSetup，不再提供旧API Key/profile或虚构目标机路径。首次接入由目标机prepare工具生成manifest/一次性secret和非秘密handoff；本人页面显式登记六字段摘要，目标机enroll后单实例切换。查询/登记状态不等于在线，不轮询，不在响应未知时重建安装。

程序、配置、状态分别归入apps/cyf-agent-runtime-v1、conf/cyf-agent-runtime-v1、state/cyf-agent-runtime-v1/INSTANCE/agents/SUBJECT/codex-home；使用目标机获授权基目录。已有Runtime升级/目录收口保留身份、授权、完整HOME和SQLite路径索引，不重新登记/enroll。唯一操作入口：`/home/isp/wsps/chcbz/isp-install/docs/cyf-agent-runtime-v1-self-host.md`，迁移见第9节；仓内codex-ws-agent仅为内嵌执行库，不是第二套服务。

正式证据：安装器19项；API175项全过及同本地R2批次安装；前端Flow4403172 Run206成功（2932通过/2 pending），364安装文件及11公网资源匹配，现行API健康UP。tenant0原有限制未放宽；不创建生产installation、不付费，完整新用户登记E2E未执行。现行主机Runtime二进制仍1.0.2，页面不会自动升级远端机器。范围、OOM异常恢复及版本/摘要闭环见`docs/implementation/handoffs/SELFHOST-ONBOARDING-20261012.md`和`specs/runtime-self-host-onboarding/`。

### 本机旧 Agent 目录已退役（2026-10-12 局部运维核验）
- Runtime仍为1.0.2/`5b902c1bcd3efced9720e015e3b8240d39ce0738`原制品；本次只迁路径、没有API/Web/Runtime版本发布。旧`apps/codex-ws-agent`和`apps/codex-ws-agent-instances`完整归档至`/home/isp/baks/runtime-path-unify-20261012/retired`，旧服务masked、旧bin启动脚本已归档，无兼容链接。
- 三静态Agent的codexHome统一为`/home/isp/state/cyf-agent-runtime-v1/unified/agents/{角色}/codex-home`；策略和模型目录文件在`/home/isp/conf/cyf-agent-runtime-v1/`。旧历史数据保留state下history，59个会话索引路径同步；不得再照抄旧HOME或旧policy路径。
- 三静态Agent在线，旧根无活动进程引用；吴用既有图片识别证据不变、无模型调用重测READY。此核验不包括恢复原已离线的托管Agent。内嵌`codex-ws-agent/`执行库仍保留；详见`docs/implementation/handoffs/RUNTIME-PATH-UNIFY-20261012.md`。

### 技能包存储与安装摘要（2026-10-13局部源码核对）

覆盖API develop `b62d6e961facae02f0645b91b1072bd688d941b5` 的I04/I05，非完整技能执行/当前线上证明。现网基础切片仍API1.14.12/0833bfe、Runtime1.0.3/6325af1；发布证据见 `specs/juyiting-skill-execution/evidence/release-20261013/summary.json`。

- 唯一新增存储配置 `economy.skill.marketplace.package-store-root`，默认 `/home/isp/state/cyf-skill-packages`；对象按hash不可变寻址。quote/购买/下载在事务外prepare字节，在短事务内复验批准版本/价格/身份；旧版安装不依赖current指针。
- 普通说明包可以无manifest；可执行包安装成功回执的manifestSha256必须绑定批准ZIP内原始字节，缺失或篡改不激活、不结算。已确认不可变回执可在对象退役后重放，仍核验主体/fence/安装身份。
- 运行费用只登记说明，未知费用不影响描述校验；原技能包购买/退款事务不变。维护HTTP发布、目录READY、统一执行、资料识别/修改与结果提交链尚待后续实现，不把对象store.publish或单测通过当成可用技能。
- 定向证据分别在特性目录的i04-proof.json、i05-proof.json；生产目录/配置未在本切片创建或改写。

本小节新增覆盖（2026-10-13，API源码 `16fe9f92e2b7ea64cdf7a710fd284ee528cba155`）：I06的 `agent_skill_execution` 为PWE一对一附属快照/effect记录，不是新任务表；DDL是显式迁移资源，当前未在生产执行，也未接入protocol4写流。CAS只写mutable投影、递增version，终态不重开；RESULT_UNKNOWN不回READY；结果阶段对象manifest支持零文件。I08由agent定义 `SkillCapabilityLookup`、chat提供可信live-session目录索引，代际/断线/主体歧义fail closed；目录事实不授予安装entitlement或任务调用权限，该基线尚未接注册消息或权威可调用join（后续I10源码接线见下节，I11仍待实施）。I06定向130项、I08定向11项与layering均PASS；这两批源码未再次上线，不将单测或空registry当在线技能可用证明。

### 技能目录与认证注册（2026-10-13局部源码核对）

覆盖API源码 `02faad300b8ee27ce706e5720b31b3c221fb8bb8`、Runtime源码 `b79558e4f18b431c1ff698432b3d6a7c07aac8d5` 的I09/I10；双端已合入并push develop，尚未发布这批源码。首批在线版本沿上节发布证据，不把源码接线等同线上技能可用。

- Runtime只从既有持久安装registry/marker核验的可执行manifest测量目录，不扫描任意HOME，不要求普通说明包有manifest。按runner注册表/工具摘要/完整主体provider绑定探测；费用不参与READY。具体runner与binding文件加载尚未接入，无真实适配器不得READY。
- 完整owner scope来自已相关性校验的认证注册回执runtimeAuth，并核对安装session fence；profile、模型消息和presence均不能授予主体或能力。初次测量后额外注册一次，activation等待目录ACK；重复ACK与heartbeat只用缓存。安装变更、断线、暂停或健康撤销失效，旧异步测量不能恢复旧目录。
- API严格解析skillExecution schemaVersion1目录，仅实际认证绑定及回执送达后激活；未知字段、非法摘要/状态、重复版本与重复JSON key不可保留旧目录，缺报告替换旧数据。目录只反映运行事实，I11仍须权威安装entitlement/descriptor及任务权限join，不直接授予调用权。
- I09定向262项；I10 Runtime416项、Java46项及layering PASS。证据 `specs/juyiting-skill-execution/evidence/implementation-20261013/i09-proof.json` 与 `i10-proof.json`。未真实Provider调用/生产DDL/Web发布；上传图片→识别→修改完整业务验收仍NOT_RUN。


### 技能安装与运行能力核对（2026-10-13 局部源码核验）

覆盖API源码 `2fb221ae15797c819b0fcb674880730bca1cf166` 的I11a，已合入/push develop、**未发布**；当前旧action-v3实现不是最终技能执行协议。

- `InstalledSkillDescriptorLookup`/`InstalledSkillDescriptorService`只读真实安装证据：精确Owner/canonical Agent、ACTIVE entitlement/order、SUCCEEDED installation及相同activation epoch、批准权限和包摘要、成功result receipt与安装/host binding。普通说明包明确NOT_EXECUTABLE；结果消息ID不等于安装command ID。包准备仍在事务外；缓存仅不可变内容，权限每目录统一末尾复读，不按技能重复读取全量entitlement。
- **2026-11-02原生安装核验更新（API ef702265/Web98f7682）**：INSTRUCTION包没有可执行manifest是正常合同，用`verifiedNative()`核对安装事实；受管安装允许没有传统order，不补造订单。`NOT_EXECUTABLE`表示不提供独立runner，管理页显示“已启用（原生技能）”。需再核对宿主原生执行配置/实测注册及任务availableActions，不能只看安装或heartbeat就断言能生成文件。林冲原缺inputCarriers；补齐独立目录及匹配载体配置后仍等待异步工具测量，使用新请求验证，不重放冻结旧请求。Provider私有配置按scope和真实安装ID管理，安装/卸载不自动复制他人密钥。正式包text-file/analysis1.1.0来源Flow118/119，目录已发布；详情和实际验收见REUSABLE-SKILLS-20261102 handoff。
- `ChatActionCapabilityService.inspectInstalledSkills`只投影安装/Runtime观察：匹配当前scope/fence与manifest/runner/摘要、工具和Provider绑定要求，join后复核live目录；断线、主体歧义、缺依赖、目录切换不能保持旧运行就绪。metadata仅白名单描述/schema/输入/输出/costInfo，没有执行路径或内部主体配置。
- `RUNTIME_READY` **不是任务可调用/执行授权**，也不会因此新增availableActions。任务ACL、目录HTTP和EXECUTE_SKILL baseline/接纳仍待I11b/I16/I18；费用信息不参与本核对，购买/退款链保持。当前receipt按installation读取尚待受控索引/schema接线；未证明生产目录读取性能，不开放未完成的HTTP路由。
- 定向171 tests与layering PASS，包含真实H2安装/回执SQL；不是MySQL catalog/在线识图证据。历史失败、固定输入与最终证明见 `/home/isp/wsps/cyf/specs/juyiting-skill-execution/evidence/implementation-20261013/i11a-proof.json`。完整上传→识别→修改→下载仍NOT_RUN，无新配置、生产DDL、Web或本批API/Runtime发布。

### 图片技能当前运行基线（2026-10-15 局部在线核验）

本节仅更新吴用图片技能与相关协议边界；以上2026-10-13切片说明保留为历史基线，不代表当前线上仍未接线，也不据此宣称全部接口/全部技能完成验收。

- 已上线：Web1.16.1（Flow4403172/Run213，commit `421f628c245b83466cafb70510ff69188180bdee`）；API1.16.5（本地build `cyf-interface-api-release-20261015-r12`，commit `6116a10403e0df250850e6ebb73f8123f5ac9ded`）；Runtime1.2.7（commit `6a9d8d3c1219450c19b3edfbef317e615940ab5d`）。本节不重标历史制品或历史验收。
- 技能目录可调用必须同时满足真实安装权益、当前认证session与测量能力、任务及资料授权。认证回执先在API边界将Receipt显式投影，统一wire使用 `runtimeInstallationId` 和十进制字符串 `sessionGeneration`；Runtime不可按JS Number接收。不能因安装成功或目录不可用而重复购买或直接补数据库记录。
- 技能包 `skillVersion`（如`1.0.0`）是语义版本，不是Long；`factsManifest`及`contextSnapshot.facts`内的action descriptor按其技能契约校验，不能误用通用`*Version`整数校验。其他状态版本/代际及CAS检查保持；取消请求的公开 `expectedStateVersion` 是可选十进制字符串，在API边界严格转Long，不放宽全局JSON类型转换。
- 原生模型output schema按本次冻结的availableActions生成并绑定digest；无可用action时只允许ANSWER/CLARIFY。当前参数投影支持封闭对象、全部属性required的保守子集；可选属性/开放对象/`$ref`等不支持的schema明确报`ACTION_MODEL_SCHEMA_UNSUPPORTED`，不能宣称通用JSON Schema支持或静默删参数。当前image-edit参数为空封闭对象，已真实运行。
- 任务459实际已执行image-edit，Provider结果归档为`RESULT_COMMITTED`，页面预览/下载成功，下载摘要与成果manifest匹配。三角形由蓝变黄，其余形状、文字及相对布局保留；生成图由800×600放大为1448×1086并带轻微纹理，不承诺像素级无损编辑。首次识别形状/颜色/位置正确，但Q7Z5被误读成0725，识别质量不能按“请求完成”判定全通过。
- 费用只登记：本次目录costInfo为UNKNOWN，商品零价不等于Provider运行免费；未新增费用审批或外单功能，认证、资料隔离与第三方回调未放宽。
- 发布/测试证据：`/var/tmp/cyf-interface-api-release-20261015-r12/`、`/var/tmp/cyf-interface-runtime-release-20261015-r8/`。在线成果与下载校验：`/var/tmp/cyf-interface-ui-acceptance-20261015-r2/task459-image-result-manifest.json`、`download-image-verification.json`；完整任务接续仍在`specs/juyiting-skill-execution/handoff.md`。

### 议事输入框不自动填充（2026-10-16源码核对）

覆盖 Web commit `2c8d6703eead623f555029341101cb688b9d448a` 的密议入口、榜文议事及 briefSelectedTask：进入会话不再写入默认开场白，保留已有用户草稿和显式 @ 行为；原权限与上下文绑定不变。仅为源码行为，不代表线上已切换。定向诊断及发布边界见 `docs/implementation/handoffs/DISCUSSION-NO-PREFILL-20261016.md`。

### 资料管理诊断基线（2026-10-16）

本轮只读审计固定Web `2c8d6703eead623f555029341101cb688b9d448a`、API `fc399976710f5b724916013926be2cbff899af8c`。资料版本/元数据revision/byteLength在当前HTTP wire为十进制字符串；组件版本选择不能转为number。资料写操作须保留精确版本前置条件、目标fileId/身份隔离和原意图幂等；不能把gzip表示ETag原样当业务版本、不应在未知结果时换key重传。目录/详情/写回执须分别绑定查询或文件代次。当前实现存在已复现缺陷，不代表这些要求已修复。

本轮覆盖文件生命周期、资料引用、预览/下载和身份/并发边界：前端70项既有回归通过，后端104项中11项HTTP测试失败；源码和隔离复现/生产日志的边界、逐功能矩阵及修复顺序见 `docs/implementation/WORKSPACE-MANAGEMENT-AUDIT-AND-REPAIR-20261016.md`，原始证据保留 `docs/implementation/evidence/workspace-management-audit-20261016/`。无新发布，不以此更新线上版本结论。

### 技能终态与异常停机发布（2026-10-16局部核对）

- 源码覆盖：API `ab379ba8f27a3b1481fc426d6d007ae76b096b2e` 的 PWE 启动校验。`RESULT_COMMITTED` 是协议4技能结果的合法终态；技能终态校验和任务执行校验均须接受它，并继续拒绝缺失/错误协议版本和无效任务、会话授权栅栏。不要把合法结果回写旧状态来让启动通过。
- 现行发布控制器的显式 `stoppedRecovery` 输入用于已经异常停机的 API：`runtimeGeneration=null`，绑定当前 JAR/安装记录、同一 boot、固定候选和真实恢复授权，并重新确认无 canonical Java writer、无10018监听、无运行记录；不从失败的live校验自动回退、不伪造历史PID或正常停机回执。原制品准入、coordinator→release→lifecycle锁、备份、安装、健康和schema检查继续保留。控制源码固定版本 `8dd17271f2206d39a2ebfb0f4fd4e641e7a3ae23`，只覆盖这条新增恢复输入，其余路径沿用既有基线。
- 实际测试/制品/安装与线上核验分别见 `docs/implementation/handoffs/API-STARTUP-RECOVERY-20261016.md`。本节不把健康检查当完整业务验收，也不表示健康监控的自动恢复摘要绑定已修复。
- 发布核验补充（2026-10-16T16:25:40.933551+08:00）：API1.16.6同批本地制品已由原发布器verified，canonical进程/摘要/healthUP及公网未认证鉴权边界已核验；无生产数据重写。完整业务与自动恢复机制不在该上线结论内。

### 点将册技能／本领与响应式详情（2026-10-17局部源码及Web1.16.9线上核验）

覆盖API `b76a1d0aeda572767a6d4734d050121d985bd9c9`、Web `6fbdb6618b1132316a95db87cca9402de83138e8`；仅点将册展示与只读资料接口。API保持1.16.8／Flow152；Web1.16.9经Flow225同Run制品部署，完整应用7视口/36次实际profile GET通过，不外推其它模块或历史删例覆盖。

- **本领（2026-10-29更新）**来自原Agent资料权威投影：请上梁山初始化，之后由本人维护；注册/presence不再覆盖资料或本领。只有空白存储回退persona，字面量`[]`是真正空值；非宋江内置角色默认空。名册、地图、匹配消费者继续使用原abilities字段，不增加第二套本领存储；本领不是技能就绪或授权证据。
- **技能**来自现有安装权益／回执／包摘要核验与当前认证Runtime目录，详情分开展示安装核验和运行状态。已核验安装数不等于目录条数或READY数；`RUNTIME_READY`不授予任务调用权限。任务目录仍需原任务授权，市场权益接口仍负责交易/安装关系，不混入本领。
- 新`GET /agent/{agentId}/profile-capabilities`仅当前拥有者可读非系统Agent，无query/body；单次只读聚合原本领与白名单技能状态，不推进Agent技能版本、不扫描、不重注册、不派单。技能描述源失败时可保留本领并明确技能不可用，不伪造空目录成功。
- Web只在当前可见、owned、非system详情发该GET；手动刷新同一GET，读取最新已入库记录，不能宣称刷新了Runtime工作区。关闭、选人、身份代际变化会取消自身请求并隔离迟到响应；不取消Runtime业务。合法空本领覆盖旧摘要，但不写改派单名册对象。
- ≤720px采用名册→详情层级，返回保留筛选/滚动；同ID重新点选不取消选择。手机详情全宽无内缩卡片，正文16px、头像68px固定且复用缩略图；刷新显示真实读取HH:mm及只读说明。>720px独立分栏滚动；详情内容滚动与底部动作是同级区域，单密议朱红通栏，双动作点将主操作／密议中性次操作，保留原资格及busy控制。关闭为44px点击区的SVG叉号，选择器限定Agent浮层，不影响其他面板。没有全局换肤或派单算法改动。

完整合同见 `specs/juyiting-agent-skill-display/design.md`；当前发布、真实验证及边界见同目录`release-1.16.9.md`、`handoff.md`、`evidence/visual-fix-1.16.9/online/`；1.16.8记录保留原事实。组件早期合成数据截图不是线上证据；95跳过/2 pending与继承84删例按发布记录保留。两条Flow原CI-only配置均已恢复，develop不自动部署。其余模块仍沿原基线。

### 本领就地维护与注册职责（2026-10-29局部上线核验）

覆盖：API `648d644bc2fcc27c3ea7d67d49d6f541370c55eb`（1.17.15 / Flow5260799/372），Web `1fdc94ac152e07091016fb9d3d898acf37551a6c`（1.16.76 / Flow4403172/377；本领及技能标题栏视觉对齐），Runtime `b74612c610457651b5fa2a4abb59e01de3f73529`（1.3.24 / Flow5264702/97）。仅本领维护和最小注册/presence职责；其余模块沿旧核验范围。

- 好汉详情本领区本人可编辑，每行一项，可清空、取消；其他人/系统只读。红色保存按钮保留清晰键盘轮廓。保存后读取profile-capabilities权威结果，不仅修改本地标签。
- 2026-10-29 Web1.16.75局部对照：编辑入口/取消依完整原型主题使用44px浅灰绿控件；输入框暖白底、8px圆角及每行一项/留空提示；取消在前、朱红保存在后并靠右。保存键盘焦点保留朱红底白字，外置2px轮廓，不能反色成白底。以完整页面计算样式而非孤立CSS声明验收，PC/手机与720px断点两侧已核验；不外推全站或实体软键盘覆盖。
- Web1.16.76补修技能标题栏：标题/已核验安装数量在左，管理技能为最后一个控件并用margin-left:auto靠右；加载/失败不伪造数量，原本人/可操作/非系统权限条件不变。按钮按完整原型浅灰绿底/深色字；PC、手机及720px断点两侧位置/计算样式对照与只读管理打开/关闭/焦点恢复通过，不涉及安装/购买操作。
- `PUT /agent/{agentId}/abilities`依接口标准v1.4使用JsonRequest/JsonResult；请求含expectedAbilities和abilities，服务端事务内校验本人身份/绑定/行锁及当前完整列表CAS，只写abilities。冲突409保留草稿并要求显式核对；网络未知不自动重发。值CAS不追踪ABA或编辑历史。
- 每次最多128项、每项最多100个UTF-16单位，去首尾空白、忽略空行及大小写重复首项、拒绝控制字符。本领变化仍会影响既有匹配评分；不会安装技能、改变就绪或获得执行授权。
- 注册仅保留认证Agent身份、endpoint和实际被消费的运行声明；presence仅保留动态状态/任务/错误，原认证和会话防护保持。名称/头像/人设/本领由请上梁山初始化或本人资料维护，Runtime不再反复发送/回写。此次按用户决定同步升级，不保留旧客户端字段双轨。
- 三端云端正式回归、主机独立可恢复安装、公网入口与功能资源字节、PC/手机编辑/清空/冲突/恢复及真实presence ACK后值不变已核验。未主动执行付费模型/任务，也未为注册E2E再重启Runtime。源码、备份、失败Run与最终证据详见 `docs/implementation/handoffs/JUYITING-PERSONA-ABILITIES-20261029.md`。
- 当次上线沿用安装前其他任务的maintenance标记且未改归属；手动健康通过不代表自动巡检已恢复，恢复由该标记原持有人收口，后续维护先核对实际状态。

## Agent断连与健康观察（2026-10-21局部核验）

核验范围：本机unified Runtime源码`134773544c44284064cd8668f501e6de263a7f4f`、制品`runtime-health-1.2.1`及主机`ops/health`巡检。其余功能沿用各自旧基线；远端Runtime未因此升级。

- systemd active不等于可用：必须核对当前MainPID、连接、注册、执行就绪和有效presence回执。本机Runtime每个心跳周期原子写`/home/isp/state/cyf-agent-runtime-v1/unified/host/runtime-health.json`（0600）；监控核验快照和回执均不超过3个配置周期。当前30秒心跳，监控每分钟运行，连续3次失败按既有策略告警。时效用于观察，不中断业务流、不授予身份或重放任务。
- 暂态网络故障（含Undici连接/请求头/响应体超时）和既有可重试HTTP错误沿用指数退避，间隔上限60秒；鉴权撤销、TLS、协议或未知永久错误保留隔离并记录脱敏分类/错误码。隔离必须先修复原因再受控恢复，不靠修改心跳时间或重新登记掩盖问题。
- 主机巡检只覆盖本机已挂载Agent，不代表远端候选全部在线。Agent异常只告警，不自动重启共享Runtime；API沿用可信恢复carrier/生命周期锁/次数预算。carrier的`--check`须在预留次数前校验canonical精确摘要，升级canonical后需审阅并同步固定摘要，禁止自动信任新字节。
- API除安装身份/端口/health外观察当前PID日志末1MiB的OOM/Metaspace错误；历史PID不影响新进程。此检查只告警，不替代类加载/内存根因诊断，也不因这一信号强制重启。
- 本轮在线验证：三个本机静态通道注册和回执健康；实际任务493吴用、林冲可选，未点击承办、未调用模型。远端和历史离线主体不计入本机成功。证据及未闭环项见`docs/implementation/handoffs/REQUIREMENT-EXECUTION-20261016.md`的本轮收口，不以此重标其他任务完成。

### Runtime固定目录与版本查询（2026-10-23本机迁移核验）

- 现用实体程序为 `/home/isp/apps/cyf-agent-runtime-v1/app/`，仅保留一套程序；旧版本目录和`current`链接已退役。历史程序在 `/home/isp/baks/cyf-agent-runtime-v1/20261023-fixed-dir/`，压缩归档均经完整性测试与全量compare。版本号、commit/tree、依赖锁和制品摘要仍保留，不因目录固定取消版本追溯。统一规则见根`AGENTS.md`对应节。
- 本机实际仍运行Runtime **1.2.6**，源码 `7dd120f5d3a61559ebf4347aa63b638f7e6a4153` / tree `a1ad4c9980b962865f2fe50f70e48171549d30df`，仅4个Python venv生成文件的安装路径重定位；应用代码、Node及依赖未更换。新制品清单与来源/转换记录以主机 `release-records/current.json`、`current.manifest.json` 和实际systemd/PID为准；历史 `1.2.6.json` 保留原发布事实，不当作现用路径。
- 安装入口、模板与重定位工具已合入isp-install develop `297272f5e7af49c6bda703b37f0fc8a6a830a4a7`；源码候选1.2.7未部署。原共享源码checkout未切换；适配源码在独立worktree `/home/isp/wsps/chcbz/isp-install-worktrees/runtime-fixed-dir-20261023`，操作以固定源码的self-host指南§2.1/§7.1为准。
- 迁移前完整停写备份含配置、身份、完整HOME/SQLite、static/managed及inbox/outbox；现行配置、manifest、安装授权摘要及原4份RECOVERY_REQUIRED记录核对未变，未重新enroll、清队列或调用付费模型。静态Agent的apps内manifest/runtime-state未迁移，仅旧程序归档；历史吴用嵌套安装内未启用的manifest和空状态目录完整归档，非现行身份。
- 本次停止主进程09:10:26，完整备份/全量比对完成09:57:49，新主进程09:58:15启动；压缩与校验耗时较长，是本次实际成本，不作为常规维护耗时承诺。随后遇并行API启动修复导致10018拒连，未接管或重启API；后端恢复后Runtime原生自动重连，10:31:19确认三个静态通道的新PID注册、ready及新鲜回执。此为当次核验，不是持续健康或全部技能/业务验收承诺；未重跑业务模型。
- 恢复不得直接从备份目录启动、改链接假装回退或用旧状态覆盖新业务事实。完整映射/摘要/恢复和未优化的备份耗时边界见 `docs/implementation/handoffs/RUNTIME-FIXED-DIR-20261023.md` 及私有归档 `RECOVERY.md`。

## 议事临时工具收起（2026-10-26源码核对）

覆盖Web commit `7806f7656cc27c72906d5d36b30ac2fdab069341` 的 `ChatPanel`、`HallConversationHistory`、`HallChatComposer`，非线上版本声明：话头记录、＋设置、引用资料支持面板外点（含输入框）及Esc收起，工具切换互斥。外点不抢焦点；Esc恢复入口，不退出议事。删除确认/删除中及子级预览/选择弹窗优先，隐藏弹窗不阻塞工具。关闭只改变展示状态，不发送/删除、不清草稿/引用、不取消录音，语音处理必要控件保留。正式/私人/公共共享基础行为但数据/身份隔离不变。12项真实组件组合交互测试及相关轻量回归通过，尚无本轮Flow/部署/真实浏览器视觉验收；证据及边界见 `docs/implementation/handoffs/DISCUSSION-DISMISS-20261026.md`。其他模块仍按各自原基线。

### 上述三项UI修复的发布补充（2026-10-26 13:55 +08:00）
Web1.16.52 / `8f77f4962b5cb80862115bbfd8b2a431fd0554f5` / Flow4403172/328已安装；功能源码与7806f76一致，后续仅升版及共享绑定测试替身修正。正式发布profile3365通过、0失败、2 pending；部署单71798391 Success/healthy，同Run制品摘要与612安装文件及9项公开资源匹配。原CI-only配置已恢复；未重新验API/Runtime或登录逐一实操三项UI，不能把资源核验写成PC/移动体验验收。详细版本、前次327测试失败及恢复证据见上述handoff和其release/verification.json。

### 输入切换、选材入口与议事预览补充（2026-10-26源码核对，未部署）

范围固定Web `1eceae1dce92159f8ca81a1226d060823b10e3fd`（tree `43fa061941ca521d183235fb90ecec61a36fbbfa`）：文本框focus（含Tab）及语音开始/停止按钮的组件事件也触发工具收起；不清草稿、不取消录音，删除/子级modal优先。榜文议事回形针直接打开既有 `HallMaterialPicker` 的dialog-only入口，不再展开输入区下方的旧任务目录；可选使用范围及已有任务关联位于弹层折叠设置，范围与显式版本勾选在“完成”才采用，取消保留原范围和关联。完成才关联本次暂存固定版本，失败/未尝试选择保留并显示继续入口；不发送消息，也不因移除暂存删除已有任务关联。私议/公议引用目录协议沿用旧基线。

议事 `HallMessageMedia` 预览无下载按钮及空下载栏，音频设置 `controlslist="nodownload"`，不支持格式如实说明；错误重试/关闭焦点恢复/身份切换清理保留。百宝箱和非议事资料管理下载不变。原型同步议事例外，不能再按旧C09为议事预览加回下载按钮。以上仅源码与定向本机回归，不表示Flow/生产构建/部署或真实PC移动体验验收完成。证据分别见 `docs/implementation/handoffs/INPUT-SWITCH-20261026.md`、`MATERIAL-PICKER-PARITY-20261026.md`、`DISCUSSION-PREVIEW-20261026.md`；其他模块仍按各自原基线。

### 厅内议事与密议统一资料交互（2026-10-27源码核对，未部署）

覆盖Web `69175b99f9b8a4c36194d2b4edf22a26e4e027f1` / 1.16.65，替代上述“私议/公议引用目录沿用旧基线”的前端展示说明，其他模块与既有发布记录不变。`ChatPanel`、`HallChatComposer`、`HallMaterialPicker`共用工具位置、选择/导入、卡片预览与收起逻辑；会话/事项仍分别绑定原目录适配器，历史、ACL及发送协议不合并。

- 左侧＋/回形针，右侧麦克风/发送；PC回形针打开共用选择窗，移动展开拍照/相册/资料。图片复用个人空间上传，只有COMMITTED的固定版本才能成为引用，未知结果核对原操作，不重复上传。
- 选中卡片在输入框内，隐藏横向滚动条但保留触摸/键盘滚动；完成才应用选择和范围，取消保留。移除只解除已有链接，不删除个人空间文件，不改执行快照。
- 移动三入口与更多/历史互斥，外点、输入聚焦、Escape收起；子窗优先，关闭不清草稿/引用、不发送、不取消录音。输入锁定只收起资料入口，不误关语音必要设置。
- 未建立会话的新密议仍需先取得服务端会话ID；不自动发送或伪造ID。Flow4403172/357全套测试3480通过、2 pending，构建/扫描成功；133项真实组件浏览器夹具通过（合成workspace/links），不替代手机相机权限或真实API上传验收，未部署。追溯见 `docs/implementation/handoffs/DISCUSSION-MATERIAL-PROTOTYPE-20261027.md`。

### 统一资料交互发布补充（2026-10-27 14:14 +08:00）

上述统一交互已发布Web1.16.65 / `69175b99f9b8a4c36194d2b4edf22a26e4e027f1`，Flow4403172/358在153秒内完成测试3480通过、2 pending及构建/扫描/部署；部署单71879400单机Success/healthy。612份制品/安装文件及公网入口、聚义厅关键资源摘要一致，默认CI-only配置已恢复。仅部署与资源核验，不重标真机相机/相册权限、真实图片上传或登录后完整业务验收。API/Runtime未部署；完整摘要、恢复目录及证据见上述DISCUSSION-MATERIAL-PROTOTYPE handoff的授权发布结果。

### 上述输入/选材/预览修复发布状态（2026-10-26 15:22 +08:00）

Web1.16.54 / commit `cbd8f2d43b42a38b5314c4749ad9b05564031176` / tree `c6064d039857e8f43329c6909bd5eb74373322f1` 已经Flow4403172/330安装，功能源码仍为上述1eceae1，发布提交仅升版。正式release profile3390通过、0失败、2 pending；Flow创建至终态192秒，部署单71807860 Success/healthy，同Run制品SHA-256 `0d7a42ebd21c9c2aa14ef99aa29d4d8abfb08280d5f9a561b30df1147b8b13b1`。612份安装文件及9项线上入口/聚义厅公开资源匹配，原CI-only配置已恢复。API/Runtime不在本次部署范围；未登录逐项PC/移动体验验收，重复“议事答复”去重未实现。证据见 `docs/implementation/handoffs/material-picker-parity-20261026/release/verification.json` 及上述三份handoff；不重标实现阶段历史验收。

### API OOM留证（2026-10-26局部核验）
- 当前API源码28700cc0ee7012ecab5c7b84fc54a9e676f4c137；本节仅核验主机诊断配置，不代表技能管理业务验收通过。Flow5264702/74把`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/isp/state/cyf-api-dumps/`写入现行启动器，并在当前JVM读回生效；保留192MiB Metaspace上限，不以增加内存冒充根因修复。
- `/home/isp/state/cyf-api-dumps/`须是实体目录、服务账号cyf-api所有、0700；新主机需先创建并核验可写，再启用同样参数。hprof可能含业务数据和凭据，只在受限目录分析，不直接上传/公开、不自动删除已有证据。启用参数不等于已验证实际OOM产出；本次没有人为触发OOM或heap dump。
- 故障留证结合OOM/GC日志与同PID类加载/loader快照；当前快照不能代替已退出故障PID，也不能仅凭依赖包存在推断类已加载。当前配置证据见`/home/isp/state/cyf-skill-management-recovery-20261026/uninstall/release/oom-dump/`，历史故障与未闭环事项见技能管理handoff。

### 议事单轮展示投影（2026-10-26源码核对；Web1.16.56已部署）

功能源码覆盖Web develop `d050cc04e0e15c71106a40b968abbc2bfef68326`；2026-10-26 17:53 +08:00核验发布版本1.16.56、commit `fe53b812f75a940eebc743918d3c91b120bbd603`（仅升版）、tree `ff7445f0a5e5fe43633c1b5d047f977e8c5872ad`。Flow4403172/336成功，3403测试通过、0失败、2 pending；部署单71826936成功。612安装文件与9项公开资源匹配同Run制品，默认CI-only配置已恢复。此处不代表真实登录会话/Provider端到端验收；原本地Web checkout旧HEAD不等于线上版本。

- `hallDiscussionTurns.js`在显示层按同会话/同事项的`outcome.assistantMessageId → actionProgress.childRequestId → message.requestId`关联原答复与成果。历史metadata及SSE/request-stream的requestId由`hallConversationMessages.js`保留。没有完整或唯一关联时保留原记录，不按时间、文本相似度或最新成果猜配。
- 状态取子执行actionProgress而非父CHAT终态。原始消息/原始存档来源不改写；通用交付模板只在已确认关联的成果中隐藏，其他正文和资产仍保留。预览/验收继续复用原asset revision及request/step/output身份，不创建新成果或自动验收。
- `BountyDiscussionPanel`持有会话级单一放弃恢复控制器，回复内`BountyExecutionTermination`只显示对应请求的折叠入口/恢复状态；历史无关联的执行保留底部折叠入口。确认前不发请求，确认时重新检查候选；身份/会话切换清理确认，既有幂等键、费用事实、权限、冲突和未知结果恢复语义不变。放弃不等于服务商停机或退款。
- 本轮无API/Runtime变更。源码、原型、测试及上线验收边界见 `docs/implementation/handoffs/DISCUSSION-TURN-PROTOTYPE-20261026.md`，不将云端CI成功当成线上业务验收。

#### 2026-11-04 展示投影补充（Web1.16.109已部署，定向浏览器验证）

Web `b60b5d900923f25f519b651898ac52c10bcbf423` / 1.16.109：同一展示投影也使用`reviewProgress.childRequestId`，沿明确关联收拢REVISION_REQUEST→后续CHAT→ACTION_REQUEST→成果。不改后台记录/任务状态，不按任务类型、文案或时间猜关联；冲突/缺关联保持分开。处理中显示通用“正在处理…”，有实际答复或成果后移除正常状态提示，仅保留最终内容；失败、取消、待核实反馈保留，CHAT完成但结果未到不能显示任务完成。归档使用原消息身份，合并的文字成果仍按原messageId提供预览/验收，澄清按钮使用原投影。普通ANSWER/CLARIFY流式协议不变。2026-11-04复用Flow445制品安装成功，612安装文件及8公共资源摘要匹配；正式站点重新打开专用588，PC1440/移动390均确认一条用户请求对应一条答复，单独完成提示消失、正常正文和HTML成果各一份。未新发模型请求或执行验收；本轮处理过程由正式回归覆盖，不能扩称全流程线上验收。详细证据见DISCUSSION-RETEST-20261102 handoff。

### 技能管理在线核验（2026-10-26）

本节核对Web1.16.57/8cdf33af、API1.17.10/28700cc0、Runtime1.3.16/19eac2f；范围是技能管理，不含岗位或模型执行。正式发布与验收证据见技能管理handoff及`specs/juyiting-skill-execution/evidence/management-online-acceptance-20261026.json`。

- 单列表显示每项技能当前版本；安装/升级/启停/卸载均在原行展开，不通过额外安装开关或岗位同步授权。历史版本是追溯/旧任务引用，不是同时启用多个版本。
- 卸载移除新调用发现入口，保留订单、权益、成果和历史包；重新安装先按现有权益报价，不删除旧安装记录来冒充升级。取消确认不应产生业务变化。
- 验收要同时看操作回执、Runtime实际目录和真实页面“运行就绪”。数据库online或Runtime本地ready、单独SUCCEEDED不能证明端到端可用；DISABLE已停止新调用时仍可能显示Runtime策略待同步，需核对原操作，不重复提交。
- 技能目录重注册等待ACK期间不应发出假offline撤销绑定；后台列表轮询也不得吞掉用户已确认的操作。健康异常、身份/会话代次、事务/幂等和锁保护保持。
- 无新升级候选时记录自动化覆盖与已有升级事实，不人为降级造验收。未知结果只核对原操作，不新购或重放旧UNKNOWN。Flow取消与安装结果分别记录，不能将随后安装成功改写成Run成功。

### 技能管理耗时排查（2026-10-26核对）

Runtime1.3.17/bridge1.1.9，源码`d9061dbaa2e45994f965d90b39ff8120aa336b11`已安装并完成真实页面PDF启停核验；这是观测更新，不是性能优化完成。Web/API仍沿用上节基线，旧完整验收证据不重写。发布Run79为CANCELED，主机随后安装完成，必须分别记录。

- 只从当前systemd PID的日志关联`runtime-phase-timing`及`runtime-management-timing`，按subjectKey/commandId区分操作；先看queueWaitMs与handlerMs，再看skill-command-handle、skill-catalog-refresh，不能将同命令重送当成新安装。
- 冷启动区分profile-state-initialize、input-carriers-measure与app-server-initialize；健康文件PID须匹配当前进程、时间新鲜且已registered/ready，不能复用重启前健康事实。
- 计时使用单调时间，不含任意业务正文或凭据；观测异常不影响执行结果，不设置性能拒绝/deadline，不删摘要、隔离或刷盘保护。Runtime分段时间不等于浏览器端到端时间，不同负载样本不能直接宣称优化收益。
- 本次明细及尚待定位项见`docs/implementation/handoffs/SKILL-MANAGEMENT-20261023.md`的20:17接续；机器证据在任务`performance/acceptance.json`。尚未定位内部唯一根因，也未上线性能修复。

#### 1.3.18测量实现与线上边界（2026-10-26 21:08核对）

Runtime/bridge `1.3.18/1.1.10`，源码`45a2c78e653e4d73a1f70dacc7e09653aa8f6763`，Flow5264702/80 SUCCESS、575项通过；真实生产页面PDF启停与最终吴用/林冲技能就绪核验通过。local-script解释器每次完整SHA不变，改为异步1MiB分块，执行前仍复测；同FD/路径/属主/权限及元数据前后核对覆盖异步替换风险，不新增跨请求信任缓存。

本轮尚未证实端到端提速：UI停用约58秒、启用42秒，Runtime分段约24秒/31秒；不能与旧轮仅Runtime10秒/18秒混算。后续需继续定位策略切换/目录测量及传输等待；冷启动载体测量仍偏慢，未在本改动中解决。详见`specs/juyiting-skill-execution/evidence/management-performance-20261026.json`；历史Run79的取消事实保留。

### 事项详情发送状态（2026-10-26源码核对，未部署）

覆盖Web `2f90a708c3fece1d6e7872e9a5589a4cb6193a07`，tree `99fed1d93158dca2f2291780dcddbda9393bf4d6`；这是源码实现，不重标线上版本。`BountyPanel`不再把所有点将状态放在独立黄色区域：ADMITTED/ATTACHED仅折叠技术详情，继续议事沿用原入口；SENDING/PREPARING/CONFIRMED中性展示，其中SENDING不提供重复查询/恢复操作。UNKNOWN或未识别状态显示待核对提醒，FAILED显示真实错误；COST_CONSENT_PENDING明确旧费用确认边界，不启用旧提交。HISTORICAL仅折叠历史指派；终态仍不显示恢复操作。

查询发送结果沿用`check-point-and-start`，只有UNKNOWN保留显式`resume-point-and-start`，参数仍为当前事项，不新增请求/自动重放/执行权限。身份切换继续关闭详情；技术详情在任务/身份/状态变化后重新折叠。目标名称只匹配已有同ID好汉，不借用当前候选；原投影无资料展示名，显示数量，固定ID/版本在技术详情保留。没有资料事实不推断0份。原型`prototypes/juyiting/index.html?scenario=matter-status#detail`仅离线状态演示；实现、验证和未部署边界见`docs/implementation/handoffs/MATTER-STATUS-20261026.md`。

### 选择成果验收的条目内预览（2026-10-26源码核对，未部署）

覆盖Web `c660e9b4f94ef37154965a6b9c88fe36c409ef2f`，tree `433de4636b15c945dda88d1829f1eb045776fc06`；只更新选择成果模式，不改变旧整批验收分支。`HallDeliveryReviewDialog`用原choices.key定位展开行，scoped slot绑定原item；序号只用于“成果N”展示，不参与验收身份。一次展开一个预览，按钮标记展开状态，切换/关闭/上下文改变清空。预览与复选框完全分离，不自动选中或验收。

`JuyiHall`保留原selectionKey+sha256匹配；加载/失败反馈显示在所属条目。`BountyExecutionOutputs`按最新预览序号与原任务epoch阻止迟到结果覆盖，新身份/关闭仍拒绝旧回调。原固定成果来源、缓存/对象URL清理、提交与幂等协议不变，不新增下载能力。缺失预览器或原成果不可用如实说明，不借用其他版本。原型复用delivery-entry/image-turn弹窗，额外两稿演示scenario=review-preview；源码、验证和未部署边界见`docs/implementation/handoffs/REVIEW-PREVIEW-20261026.md`。

### 上述事项状态与条目预览的发布状态（2026-10-26核对）

上两节描述的源码行为已由Web **1.16.58**，commit `3c95bfeef3826cb439c3da92ddfd82e642a507fe`（tree `93d9c9c7338ef34440a040d4d0713f3a18ba6a5f`），Flow4403172/341发布。前述“未部署”仅为实施时基线；本次同Run测试/扫描/构建/安装成功，612个安装文件及9项公网资源摘要核验通过。没有新增API/Runtime接口或发布；真实登录业务端到端尚未核验。发布证据和恢复边界见 `docs/implementation/handoffs/REVIEW-PREVIEW-20261026.md` 发布完成节及其release证据文件，不以历史发布记录推断未来线上版本。

### 技能管理 journal 验证复用（核对：2026-10-26，Runtime1.3.19）

源码 `isp-install@04b1129455c3c472a3db3b5ed6a1f1ca7547704e` 的 `SkillInstallManager._load` 每次仍安全打开并完整读取journal；仅同manager、同路径/scope、完整字节相同时复用上一份已通过的解析/摘要/历史关联校验，返回独立深拷贝。改变内容重新全验；权限、硬链接和路径保护先于复用；不使用mtime/TTL信任缓存、不改变刷盘/ACK/恢复。重启后首次读取必须全验。回归入口 `conf/codex-bridge/test/skill-journal-validation.test.mjs` 与原manager恢复测试。

Flow5264702/81已安装此版本并完成真实页面PDF启停/最终就绪核验。单组UI耗时19.1/33.9秒仅说明该样本较前轮下降，稳定延迟与冷启动性能未验收；诊断要同时取浏览器单调耗时和Runtime command/catalog/receipt分段，不能把局部读取加速说成整体性能闭环。完整来源仍见[技能管理handoff](implementation/handoffs/SKILL-MANAGEMENT-20261023.md)及[性能证据](../specs/juyiting-skill-execution/evidence/management-performance-20261026.json)。

### 已完成事项与只读验收记录（2026-10-26源码核对，未部署）

覆盖Web `3eb09e493fb6a68c67e42b9aba4a3f1dbc7d2de4`（tree `b5a970e53bf8925ccb8141ce5c00e9b4a3357fd3`），Flow4403172/343测试/构建成功。事项详情完成态不再提示补充修改；历史议事入口走原只读continueBountyModification，不走写意图discussTask。成果主入口为“查看成果与验收记录”，HallCompletedRecords替代完成态旧验收Panel；其他状态旧分支保持。正常成果页无“查看议事记录/重新读取”常驻按钮，仅失败重试、缺失重新核对。

已验收集合只消费原delivery-review-context中ACCEPTED批次RESULT项，其他历史只列既有正式交付history；不会把任务completed或生成完成当作验收事实。相同artifactId/version/hash不重复列在两个区域；名称/预览仍用同编号、版本、摘要匹配现有useOutputs目录。元数据缺失显示序号/编号，不猜文件名；没有验收时间/操作者字段，不补造。单项行内预览与上下文取消复用OutputPreview；已有游标按需补读，失败显式重试可重走分页，不自动重放任何命令。

收入案卷仍用原API，仅加确认及确认期间身份/任务/版本变化保护。无新API/Runtime契约，本轮未部署；原型/规格、测试与制品边界见 `docs/implementation/handoffs/COMPLETED-REVIEW-PROTOTYPE-20261026.md`。历史发布1.16.58不能当作此优化已上线。

### 已完成事项只读页面发布核对（2026-10-26）

上述完成态详情与验收记录投影已在用户授权后随Web **1.16.59**发布：源码 `1102350543846e59f2c31dfc36145155da4f7773`（相对功能基线3eb09e4仅升版），Flow4403172/344成功，3440测试通过/2既有pending。部署单71844377成功；612安装文件及9项公网入口/相关资源匹配同Run制品。API/Runtime未改，真实登录/Provider端到端未复测；不以资源一致性代替业务验收。云端已恢复CI-only。发布/恢复与完整摘要见 `docs/implementation/handoffs/COMPLETED-REVIEW-PROTOTYPE-20261026.md` 及其 `completed-records-20261026/release/`，上方“未部署”仅为前阶段历史状态。


### 技能结果回执调度（核对：2026-10-27，Runtime1.3.20）

覆盖 `isp-install@15483d554a0fd6b01c3413d68c80e5367654a942`，Flow5264702/84成功、597项测试通过，主机同Run制品与675项payload一致。仅精确关联的技能结果回执不等外层ingress中的catalog刷新；仍进入原manager.tail/锁，普通命令/聊天回执保持顺序，断线及close drain保护不变。定向回归见Runtime `test/runtime-host.test.mjs`；不改变READY/注册ACK判定。

真实生产页面两轮PDF停用/启用完成，最终吴用4技能、林冲原图片技能就绪，订单/权益/安装不变。四个命令首次回执都在catalog结束前处理，队列等待约0.027–0.042ms；这是排队消除证据，不是回执处理或端到端耗时。页面可比停用17.007秒、启用30.005/27.616秒，仍非稳定性能通过。若页面“完成”同时仍写Runtime策略待同步，不计作完整完成；保留原始样本并等明确同步完成提示，READY另验。证据见[技能管理handoff](implementation/handoffs/SKILL-MANAGEMENT-20261023.md)和[性能证据](../specs/juyiting-skill-execution/evidence/management-performance-20261026.json)。

本轮安装经验仅限任务适配器：ENOSPC时记录写失败不能阻止旧服务恢复；独立备份比对未完成不能视为可恢复备份。Run83压缩备份在时限内未完成比对并自动恢复旧服务，Run84在可用空间实际恢复后沿用非压缩完整备份成功；不把压缩方案宣称为现行发布流程，不删除旧备份、不跳过完整性/发布锁。修复的任务脚本及阶段记录保留 `performance/receipt-capacity/`，不代表所有安装入口已统一修改。

### 轻量工作台文案约定（2026-10-27源码核对，未部署）

覆盖Web候选 `f4e7f779304ee20efa3e6f29a6830a03d20ec88a`（1.16.60；基线1102350；Flow4403172/347测试3447通过、2既有pending，构建/扫描成功，未部署），不改变协议/状态/权限。轻量主线采用“事项、资料、好汉名册、待确认承办、待我处理、已归档、议事记录、新对话”；地图文化名及正式资金悬赏专用词不机械替换。开始办事只保存需求，确认承办才交给好汉，提交成功不等于开工；资料管理不等于授权后仅本人可接触，承办处保留所属用户及外部运行环境/模型处理边界。

查询结果与继续原操作分别对应既有读回和写恢复；停止等待不撤回消息，放弃本轮未交付结果不退款、不保证服务商停机，也不删除已上传成果。多选验收说明所选数量及事项完成后果，历史整批验收分支仍说明整个批次。议事无下载入口不提示“请下载查看”，独立资料页下载保留。

草稿保存冲突时当前输入仍在页面中，但打开服务端版本会替换它；提示先复制需要保留的内容再重新载入，不承诺未实现的未保存副本。实际SFC+adapter隔离回归已核实，生产并发写入未试验。

本次是源码/离线原型核对，不是完整ACL、费用、内测资格或线上业务验收。97条处置与剩余事实核实见 `specs/juyiting-ui-baseline-20261006/optimization/copy-audit/implementation-20261027.md`，执行证据见 `docs/implementation/handoffs/JUYITING-COPY-20261027.md`；未改变其他段落的线上基线标识。

### 用户可见提醒精简（2026-10-27增量核对，1.16.67已部署）

覆盖Web `361ed19bf405d81813e993bac533fb2e729385cc` / 1.16.67（并行集成基线b049f934；仅本节描述此源码，不重标上文线上基线）。资料保存/关联正常成功以列表和输入框反馈，不追加“原关联操作已提交”等提醒；同键恢复成功清除旧错误。结果未知、详情加载失败、状态被其他操作改变、离页无法恢复仍提供简短提示与原有恢复入口。

普通议事、协作和成果界面不展示路由/引擎、执行/请求编号、哈希、内部事件版本等诊断内容。状态采用中文，正常连接不重复常驻解释。专业接入/运维配置、业务文件版本、付款和退款交易号、费用/权限/删除/撤销风险仍保留；精简展示不改变原请求、鉴权、幂等、验收与安装结果判定，不修改用户或AI正文。

CI Flow4403172/361完整测试3486通过、2既有pending，构建/扫描成功，Run135秒。用户后续授权部署后，Flow4403172/362重新完整测试/构建并安装同Run制品，3486通过、2既有pending，总耗时236秒；部署单71895736一台Success/healthy。2026-10-27 16:25核对612安装文件及16项线上入口/资源摘要一致，Web1.16.67已上线；发布证据在同目录release/，不代表全账号业务实测。静态清单、浏览器夹具范围、动态返回文本及线上账号未验边界见 `specs/juyiting-ui-baseline-20261006/optimization/evidence/user-facing-copy-cleanup-20261027/audit.md`，交付记录见 `docs/implementation/handoffs/USER-FACING-COPY-CLEANUP-20261027.md`。

## 推荐承办排障与证据边界（2026-10-31局部核对）

本节资料推荐覆盖API `2a8a67c58c1949d671a4952bac496527ec1f3cea`（Flow421、1.1.9-SNAPSHOT已安装并核验）；连接排障历史仍为2026-10-30基线。安装与真实验收另见 `docs/implementation/handoffs/JYT-MODEL-RECOMMEND-20261028.md`，不代表本指南其他模块已重验。

- 连接复用后端ChatModel的底层连接/凭据/传输；独立无工具、无记忆、无自动重试调用。复制模型原生options，不用通用ToolCallingChatOptions替换Provider原生类型；默认工具拒绝、输出工具调用拒绝仍保留。
- 推荐只接受模型引用当前候选的可用证据。登记本领是声明，不是完成保证。INSTRUCTION已启用且实时安装目录匹配、NOT_EXECUTABLE时可作为经验引用，不是执行工具/admission；EXECUTABLE仍需启用、admission及READY。
- API观察完整授权全集，但无可引用证据者不送模型，手选不删人；全体无证据为NO_MATCH且不调用模型。推理后复核事项、完整候选及关联资料观察，变化409。空/伪造/不可用依据仍502，不补造或自动重试。
- 推荐读取当前事项ACTIVE INPUT/REFERENCE资料的名称、原文件名（含后缀）、关联版本MIME、版本/用途/状态；复用工作空间只读授权入口，关系和历史版本完整分页。不按资料类型筛选、不预设后缀→技能映射，MIME仅辅助；批准Prompt让模型结合任务目标自行判断。不是附件正文读取或视觉分析调用，不发送路径/下载URL/身份/哈希，不新增模型调用。
- 当前权威工作空间没有摘要字段，summary为null，不编造或宣称已生成摘要；不以最新版本类型替代关联旧版本。推理期间资料变更返回过期；读取失败不能伪装无附件。正式推荐32项回归通过；真实“分析结果”+PNG元信息已推断出读取图中检测信息与领域解读需求，模型判定候选证据不匹配返回NO_MATCH，不强行推荐。此验收不是图像正文分析/执行验收。证据见`specs/juyiting-assignee-recommendation/evidence/evidence-materials-release421.json`。
- 503先区分装配/SDK/传输；502查看`assignee_recommendation_invalid reason=...`常量结构原因，不开启模型全文或凭据日志。诊断ENC(...)须使用实际Jasypt参数在内存解密，禁止把密文当Bearer、禁止输出或落盘明文。
- 核对JAR prod与外置配置及真实进程覆盖，不能仅从源码模型名推断线上。2026-10-30首轮核实线上公共聊天采用历史外置gpt-6.1-sol覆盖；本次未换Key、模型或协议。

## 原生 Word/Excel 文件链路（2026-10-30 局部核验）

适用源码：Runtime `d0c35270cf9164a1aa7e1247365e716d6e0be43f`（1.3.27/bridge1.1.18）、API `dec6e2858239e3a5a8efb22c87dcb45321faff0c`。仅本节覆盖的新链路已核验，不更新全文旧功能基线。

- 用户上传固定版本的DOCX/XLSX材料后，模型通过app-server原生命令调用Python文档库，读取、修改、保存并提交真实成果；API保留资料/任务权限、成果提交和鉴权下载，bridge不编排文档内容或计算公式。
- Python解释器、标准库、python-docx/openpyxl随工具制品交付；生产 `.toolchain` 实测约342MiB，共享一份、只读映射进入请求沙箱，不逐请求复制。请求输入、工作文件、输出以及发布制品/备份另占空间；“工具共享”不代表这些内容零增长。不本机pip/源码构建，不自动清理历史备份。
- 能力开启必须配套三处：Runtime真实文档沙箱探针成功；API的typed声明解析和native输出交集支持对应MIME；成果存储配置允许对应MIME。仅补成果MIME配置不够，旧API可能拒绝整个混合能力声明。
- Flow worker完成重型测试和工具打包；worker用户命名空间不能执行目标bwrap隔离用例时，制品绑定精确测试源码及摘要，由目标机在停旧服务前完成必需轻量探针。两份证据缺一不可，不能把Flow跳过项宣称通过。
- 生产task559在Runtime109/API403上完成普通议事→原生执行→正式成果→鉴权下载→DOCX/XLSX重开及内容核对。旧PNG/TXT/Markdown/HTML成果下载也已重新核验；这不是新一轮生图/改图模型执行。该Office批次未覆盖浏览器/PDF及原默认改图单请求E2E；浏览器后续状态见下文2026-10-31条目。
- 详细发布、实际停服窗口及验收证据见 `docs/implementation/handoffs/CODEX-NATIVE-SKILLS-20261027.md` 2026-10-30 Office收口节；用户成果验收/接受按钮未代点。

### 语义控件维护入口（2026-10-30局部核对，Web1.16.78已部署）

覆盖Web1.16.78 `52683f07806bab9e6275513c88d14a496e01832d`，仅本轮控件外观/交互，不重标其他线上基线：共用显式样式入口`web/src/styles/hall-controls.css`（由main.js导入）。熟悉工具用hall-tool、上下文列表跳转用hall-row-link，44px/aria-label/title及焦点保留；明确业务用纯文字和原主次/危险样式，独立动作区可用hall-action-surface；不可按按钮文字在运行时猜业务。委派按钮role=switch复用原更新状态，语音保留原生checkbox/change并绘制滑轨，UNKNOWN不重发。资料版本与下载同排且继续绑定selectedVersion；OAuthCallback模板/样式和回调路由既有`meta.publicEntry`展示标记配套更新，复用App全宽可滚动独立入口，隐藏应用栏、SideMenu和PWA浮条；不修改state验证、交换、URL清理或安全返回。

新改动先在唯一原型`web/prototypes/juyiting/`及其specs/prototype-spec.md更新，再按既有组件显式接入；不要全局改写所有button。集中合同回归`web/tests/juyiting-semantic-controls.test.js`，业务消费者按实际事件/固定版本验证。Flow4403172/381正式3537项通过、0失败、2既有pending，612项制品摘要核实；主机独立备份/安装exit0、record online_verified，公网8项资源一致。真实公网上下文回调失败态1440/390/320与低高度共5尺寸核验无全局栏/菜单/PWA、无横溢出且操作/页脚可达；不是授权账号登录成功或全站真实API验收。此前68项产品浏览器为隔离SFC检查，不作全站E2E。精确来源、两次实际发布及备份恢复见`docs/implementation/handoffs/SEMANTIC-CONTROLS-20261030.md`。

#### 选材同行按钮与委派右对齐（2026-10-30源码核对，1.16.79未部署）

覆盖Web `0db1b48c1948d12595041eadb9eb0bc1af3b990a`：AgentPanel的委派开关/状态组显式靠右、状态不拆行，复用原role=switch及异步结果。HallMaterialPicker中“预览/收起预览”与“添加/已添加”同一行业务动作统一文字；独立“上传资料”入口使用hall-tool上传图标，保留原生multiple文件输入、aria-label、焦点与原change/未知核对语义；需求区“添加资料”仍是纸夹工具图标。既有“已选N份”为展开状态入口，不改为添加操作。

原型规格已先同步。集中样式/选材与首页消费者定向回归50项通过；原型/真实组件隔离浏览器60项覆盖1440/721/720/390/320，非生产API E2E。Flow4403172/383正式3539通过、0失败、2既有pending及构建/扫描/上传成功，612项制品摘要已核实；本轮未安装，不能把此前1.16.78上线事实延用为1.16.79已上线。失败382、固定制品与恢复交付入口见同一handoff。

#### 委派控件内部顺序（2026-10-30源码核对，Web1.16.80未部署）

覆盖 `bdb973a45c39959b483f1707b9a01875904b90ec`：AgentPanel右侧组合从左至右为“已开启/已关闭/核对中 → 开关”，滑轨位于最右，与唯一原型已有顺序一致。只交换原button内的状态/轨道DOM节点，不以全局row-reverse影响其他开关；组靠右、aria、原更新/禁用与未知核对不变。原型规格已明确该顺序。

受影响回归25项通过，原型20项与实际组件隔离浏览器24项覆盖五尺寸/四状态及Space/Enter、禁用不重发；非生产API E2E。Flow4403172/384完整3539通过、0失败、2既有pending及测试/构建/扫描/上传成功，612项制品摘要核实。本轮未部署；后续部署复用384不可变制品，来源与SHA见SEMANTIC-CONTROLS-20261030 handoff，不把此前1.16.78上线记录重标为本版已上线。

#### 委派与选材修正发布核对（2026-10-30 22:55，Web1.16.80已部署）

本节更新前两节局部修正的发布状态，不重标其他模块：Web1.16.80 / commit `bdb973a45c39959b483f1707b9a01875904b90ec` / tree `c6d59eb8b23c399b23c16fccc6d0c844c468f73b` 已实际安装，复用Flow4403172/384（3539通过、0失败、2既有pending，612项制品摘要核实），未重复构建。归档SHA-256 `1ad66609c1f20084dca90975bf9d6b9e36c4491e615c5469b8fb1afbccb594e4`；既有锁下备份381后独立安装exit0，真实record为384/1.16.80/online_verified。恢复资料保留 `/home/isp/baks/cyf-web-flow/20261030-semantic-controls-switch-order/`，归档SHA `d2c7586e01f5784bf2ceaab8cef314e3bbd90e48fa5b73b4474b3b78898c2e8f`。

公网入口旧缓存在安装器第10次核对匹配后通过，独立8项入口/实际引用JS/CSS大小及SHA全部一致。当前发布包含委派行靠右且“状态 → 最右开关”、选材同行预览/添加统一文字及独立上传图标；未改API/Runtime或业务状态。没有追加生产账号E2E，既有原型/隔离组件检查不冒充线上账号验收。安装、备份、当前记录和资源明细见同一handoff及 `/home/isp/state/cyf-semantic-controls-20261030/deployment/switch-order/`。

### 原生浏览器脚本（2026-10-31核对；Runtime c12f7ed / Flow111）

- Runtime1.3.29/bridge1.1.20在固定app安装。Playwright/Chromium/中文字体为程序级只读共享制品，模型通过普通exec读取`/usr/lib/cyf-browser/README.md`并调用`browser-session.mjs`；不是bridge的browser专用动态工具。bridge成果工具仍只有artifact_stage/result_propose。
- 执行使用命名权限配置，workspace/outputs及隔离procfs可写，输入/引擎Home/共享工具只读。内层允许浏览器本地socket IPC；外网目的地仍由外层namespace/nft与精确origin代理控制，空origin没有新增出网授权。Chromium sandbox/TLS未关闭，匿名context不复用宿主登录态。
- 生产task561真实模型从现有HTML材料完成中文填表/点击、浏览器下载TXT及PNG截图，再正式提交、鉴权下载、核对SHA与内容。无扩展名输入第一次导航未找到表单，模型自行改为读取原HTML后setContent，不依赖人工脚本代执行。该证据覆盖本地页面，不是公网登录/MFA/交易验收；授权HTTPS/拒绝出网/TLS/取消由同制品真实主机探针独立验证。
- 无proposal且已确认模型结束的执行，按已有执行失败回执收口，不再启动模型；task560已由旧失败事实转FAILED，不重放。PDF及默认改图单请求端到端仍未闭环。证据：`/home/isp/state/cyf-native-skills-20261028/browser-development-20261030/acceptance/browser-task561-verification.json`。

### 通用文件流式处理与原生能力注册（2026-10-31局部核对）

覆盖API `616324d3942543d2508811c867febee92d9e6056` / Flow416，以及Runtime `dedf9c75734b719bd262d7e84b88f49bcc11b141` / Flow114（1.3.31/bridge1.1.22）；仅更新下述行为，不重标前文历史验收。

- 新链路不再要求API维护原生格式白名单或另配成果MIME列表：API从授权材料目录和同一已认证Runtime会话冻结合同，保留身份/任务/租约/摘要与成果绑定。此前Office“三处配套”是旧版本部署要求，不再适用于本基线。文件可传输不等于可解析/预览；浏览器主动内容仍按附件下载安全策略处理。
- 上传、材料读取、成果暂存/转存/下载采用有界流；文件仍完整落盘，摘要增量计算，非分片协议。Range/HEAD/完整摘要及权限复核保留。大文本只截取预览内容（当前200000码点），不截断原文件；33MiB+1上传/鉴权完整下载SHA及partial预览已实测。WebSocket保留64KiB控制消息限制，不承载文件体。
- Runtime本机能力探针使用无命令deadline的自有command/exec，进程退出/关闭仍终止等待；普通RPC不随之取消超时。generic ready只说明通道，必须确认测量完成后重新注册的原生能力。真实启动测量与临时浏览器测试的参数必须一致，不能凭一个较长timeout测试通过就认定启动声明可用。
- 旧任务不自动重放；当前事项的CLARIFY应正常回复原问题。模型执行、result commit、鉴权下载/内容核验和业务验收分别记录。完整证据与当前未完事项沿用`docs/implementation/handoffs/CODEX-NATIVE-SKILLS-20261027.md`，不新增发布门禁或重复构建。

#### 原生议事资料生命周期（2026-10-31核对，API8ab1a42 / Flow419）

议事路由基线与本轮材料授权分离：包准备、context、派发/回执核对原grant/指派/身份，不把最初输入快照当永久必选资料；本轮资料由现有材料适配器按活动关联、版本和摘要授权。原生EXECUTE_SKILL使用本轮冻结snapshot，选中成果promotion核对成果自身归属与保留事实，均不从已移除的最初输入推断文件权限。普通/付费冻结输入路径仍保留原检查，不能用discussion基线代替执行授权。

本基线已实际安装。task563换资料后正常议事、模型自主离线尺寸修正、正式回传与鉴权下载通过；未直接写业务DB或自动重放旧任务。Runtime114真实TXT/MD/HTML/XLSX/中文PDF/浏览器页面交互及生图通过；改图内容通过后，1254×1254初始尺寸偏差经普通离线请求修正为256×256。Word由同制品真实隔离探针验证，本轮未追加Word模型E2E；未替用户点击业务验收、未做资金或任意网站登录/MFA/交易验收。最终证据沿用handoff及`/home/isp/state/cyf-native-skills-20261028/pdf-development-20261031/mainline-final-verification.json`。

#### 待确认承办详情（2026-11-01局部核验）
源码Web709d30ddb77f4e8b33d405093b6b4a75585a2e64，1.16.82，Flow4403172/388已安装核验；只覆盖承办推荐/手选区域，不重标其他功能。
- 显式重新推荐先GET权威事项再POST推荐；加载阶段显示动态状态并锁定选择/确认。保留服务端真实并发过期响应，不自动循环调用模型。此次真实重试200 NEEDS_CLARIFICATION；首次自动推荐仍观察到一次409，具体快照变化原因未归因，不宣称完全消除所有过期响应。
- 手选按卡片展示，全部/我的/外部筛选；有可选候选时，即使模型无推荐、需澄清、失败或过期也不显示“无人可承办”。只有当前事项候选读取成功、全集为空且无下一页才显示招贤提醒；加载/错误/筛选为空不冒充全集无人。
- PC双列/手机单列已核验；不改API模型连接、Prompt、费用或Runtime。详细回归及安装证据见specs/juyiting-assignee-recommendation/evidence/evidence-detail-release388.json。

### 2026-11-01 直接推荐上线补充
- 核对范围：API ae4093b919a985a906107bcfc0d0457eaea943e7（Flow422）、Web04c5240018eb4402194c84eb64f03e2f02192cbc（Flow389），用户授权安装后健康及线上资源摘要通过；不代表其他能力重新验收。
- 推荐阶段仅READY/NO_MATCH/NO_CANDIDATES，questions为空；已删除需求补充展示，正常执行议事澄清不受影响。现有单次ChatModel结合原文件名后缀/组合后缀、名称、辅助MIME及任务目标推断操作、匹配技能用途，本领作为参考，无代码后缀映射、不读取正文。未知格式不伪装确定，证据不足不强行推荐。
- ES/向量新推荐方案仅记录暂缓；本次无真实模型效果抽测，既有409快照保护保留，不宣称全部过期问题已解决。证据：specs/juyiting-assignee-recommendation/evidence/evidence-direct-recommend-20261101.json。

### 2026-11-01 逐人推荐度上线（22:07技术核验）
- 固定源码API0eb9fa93dc8eb5c75d1cf8612af059e6425a82ed/Webbea12d720b217183331e9e1e6294a47c1028b484，Flow423/392通过，已获授权按API→Web安装；API健康UP/摘要MATCH、canonical8项通过，Web612文件及公网8项入口/聚义厅资源摘要通过。部署证据位于/home/isp/state/jyt-recommend-ux-20261101/release/deployment-verification.json。
- 新候选将所有授权可选Agent一次性交给模型，逐人返回HIGH/MEDIUM/LOW/UNKNOWN与理由；不再过滤无公开证据者，而以UNKNOWN说明资料不足。NO_MATCH仍含全体评级；无候选才跳过模型。API负责权限、快照与引用归属/完整覆盖，模型负责适配判断，无服务器规则打分和额外模型调用。
- Web各卡展示推荐度/理由；高/中优先展示并用于地图推荐标记，低/未知仍可手选且不默认选择。等待文案非技术化，需求理解默认折叠，移除底部候选刷新图标，保留显式重新推荐与防误操作。
- 结构/回归已验证，但真实模型对图片识别等需求的推荐效果未在本轮验收。最新合同与证据见specs/juyiting-assignee-recommendation/spec.md及evidence/evidence-rated-recommend-20261101.json。

### 2026-11-01 待确认承办精简与自有优先（23:12已部署，Flow424/394）
- 核对源码API efcb87549d332c5bfd5b18507b2524360d241263（1.1.12-SNAPSHOT）、Web 7b44dec7665d1e32bf02de119043e20fd55cbf58（1.16.86）；用户授权后已替换以上API423/Web392上线基线；API健康UP/制品MATCH、canonical8项通过，Web612个文件及公网入口/聚义厅等8项资源摘要通过，实际模型语义效果未抽测。部署证据：/home/isp/state/jyt-recommend-clean-20261101/release/deployment-verification.json。
- 正常推荐完成直接展示候选卡片（归属/运行状态/推荐度/理由）与确认入口，删除需求理解/能力依据/通用说明面板及归属筛选；只有LOADING/ERROR/STALE显示必要反馈，错误/过期提供显式重试。
- 由模型先判断关键能力；双方满足时自有优先，评级不因归属抬高。不匹配或未知的自有Agent不压过合适外部Agent。前端保留服务端模型数组顺序，不按等级重新排序，不自动提交指派。单次模型调用、ACL/证据/409不变；真实语义效果尚未验收。


### 2026-11-02 承办候选渐进展开（开发已验证，未部署）
- 核对范围Web 9a4e8b195b551af2b7e44797b29c8e7379c6f2e2 / 1.16.87，Flow4403172/396成功；只涉及待确认承办交互及等级展示。原型与原型规格已同步，无后端/模型排序/接口改动；上节1.16.86仍为最近已核验的上线版本，本次不安装。
- 有HIGH/MEDIUM推荐时仅展示推荐人/理由，默认收起其他候选；点击「更换承办人」展开，「收起候选列表」折叠。手选后收起并恢复入口焦点，标题「已选承办」、按钮「确认由{姓名}承办」，选人本身不派单。无合适推荐默认展开、不预选；加载/发送禁用、权威空态、失败/过期重试及身份/事项版本重置保持。
- 展示等级为优先推荐/可以考虑/匹配较低/资料不足，枚举与模型返回顺序不变。390/1440原型及长文案检查、组件定向27项+托管静态4项、正式全量回归通过。证据specs/juyiting-assignee-recommendation/evidence/evidence-collapse-recommend-20261102.json。

### 2026-11-02 承办候选渐进展开已部署
- 后续用户授权“部署”，复用Flow4403172/396不可变制品安装Web1.16.87/9a4e8b195b551af2b7e44797b29c8e7379c6f2e2，未重建。安装exit0，612个文件及公网入口/聚义厅共8项资源摘要与当前入口引用关系通过。该记录替代上一节本功能“未部署”的历史状态；API/Runtime不变，真实模型语义不在本次发布验收范围。
- 旧Web394备份/home/isp/baks/cyf-web-flow/20261102-recommend-collapse，tar compare通过。部署证据/home/isp/state/jyt-recommend-collapse-20261101/release/deployment-verification.json；保留原CI未部署报告，不重标历史执行事实。


### 技能管理岗位与可复用技能包（核对：2026-11-02，API8ad42be781）

- 技能商品审核/发布使用既有岗位权限，`skills:platform`配合SKILL_REVIEW/SKILL_PUBLISH及有效任职/绑定；不再由该发布入口的ROLE_ADMIN放行，不授予全站权限。运行与业务授权仍遵循RB-1，技能包不承担API权限或Runtime隔离。
- 本次已建立“技能管理”岗位并由chcbz所属吴用任职。真实Owner可携带任职authority代办发布；不能据此声称Agent模型已获得独立自主发布通道。HTTP入口、固定幂等键和恢复查询沿用岗位合同。
- 新增正式目录包：识图、文档工作台、网页操作与验收、信息检索，均1.0.0免费指令技能，可在既有技能管理中为不同Agent安装；发布不是自动安装，实际安装继续经原受管安装流程。原生能力前置由Runtime116提供，不为技能名增加bridge编排分支。
- `/home/isp/state/cyf-skill-packages`目录由实际API身份持有写权限，现为cyf-api:root/0750，包文件0444；组/公共不可写、摘要寻址、原子不覆盖及授权检查保留。不要恢复旧root只读目录使合法发布再次503，也不递归放开已发布对象权限。
- CYF业务表不依赖CHECK；生产44表82条已删除且正常启动后仍0条。具体规则见API `docs/interface-catalog/database-check-rules-20261102.md`；PK/UK/FK/NOT NULL/类型/事务/锁/幂等保留。不能启动时自动清库或补回CHECK。
- API Flow439与主机安装/SQL/任职/四包发布证据见REUSABLE-SKILLS-20261102 handoff及`/home/isp/state/cyf-reusable-skills-20261102/skill-position-release/production-final-verification.json`。当前核验覆盖此链路，不包含历史告警修复、全业务性能结论或吴用自主模型发布测试。


### 前端后台观察生命周期（2026-11-02，开发已验证、未部署）

- 核对源码Web1.16.95 / `362f2fc094e89eff853d81c0e3c2b9f086356b55`，Flow4403172/407；只覆盖前端，不表示API/Runtime方案已修改或线上已切换。
- 技能市场目录在打开、手动刷新、返回前台和相关跨页签本地存储通知时读取；无待办不启动周期全量查询，有待办只核对原change，终态后合并目录刷新。持续前台空闲时不实时发现其他设备变更，可手动刷新；本地storage通知不是服务端推送。
- 相关场景/议事/成果/验收/个人执行/点将等待/案卷问答观察在隐藏时暂停后台读取，回前台按原任务恢复。隐藏不取消后台业务，不重发未知写入。已完成技能结果不参与定时扫描，显式刷新、前台恢复与作用域切换仍重新授权读取。
- 场景与回复读请求在同一生命周期内合并或串行，卸载/停止/切换身份后旧回调不得重启观察或覆盖新状态。回复正文已经出现不代表持久请求已终态，仍保留必要核对。实现与回归证据见JUYITING-POLLING-20261102 handoff；未测量生产请求量及CPU改善比例。

### 前端后台观察优化已上线（2026-11-02 18:32 CST）

用户授权后，复用Flow407制品安装Web1.16.95 / 362f2fc094e89eff853d81c0e3c2b9f086356b55；612文件及公网11项入口/聚义厅/技能管理资源摘要和JS引用关系通过。此记录替代上节未部署状态。备份/home/isp/baks/cyf-web-flow/20261102-polling-web407；证据见JUYITING-POLLING-20261102 handoff。API/Runtime不变，无生产性能收益实测；已打开旧页面刷新后加载新版本。

### HTML / Markdown 文件静态预览（2026-11-03源码局部核对）

- Web候选 `b0404c4042c90d6bf862b54db2b2ff9ee3405bf3`（1.16.98）在资料详情、成果目录/正式交付及议事成果复用 `RichDocumentPreview.vue`。HTML/HTM展示静态排版，MD/Markdown经marked展示标题、列表、表格及代码；保留下载，空文件显示提示。
- 读取沿用原身份授权与固定文件版本，不改变API契约。议事HTML/MD仍通过原downloadUrl读取，不增加服务端inline许可。切换身份/文件后不显示旧请求结果。
- 不可信内容经DOMPurify清洗后放入无脚本/无同源权限iframe；CSP禁外部资源与网络，移除链接、表单及主动内容。保留内联样式和安全data位图；依赖外部脚本/CSS的HTML不保证完整还原，需下载原文件查看。
- 此为源码与定向浏览器核对，**本次未部署**。正式Flow与证据入口：`docs/implementation/handoffs/HTML-MD-PREVIEW-20261103.md`，不据此推断当前线上已支持。

### 启动工具链与消息准入（2026-11-03部署核验）

覆盖源码：Runtime `73204aefb1e823aa6f80ba850be42f6098e2902b`（1.3.38 / bridge1.1.28，Flow125）、Web `b0404c4042c90d6bf862b54db2b2ff9ee3405bf3`（1.16.98，Flow415）、API `9aa75fcf0ab0f19935c766374b12d809effffc53`（Flow452）。2026-11-03 14:01 +08核实均为远端develop，三端已安装并核验；后续实时状态仍看现行release record。正式验证与发布证据见 `docs/implementation/handoffs/JUYITING-POLLING-20261102.md`。

- 同进程静态工具链发现/摘要测量使用一个共享槽，只保留不可变工具清单，不缓存技能包字节；Agent身份、会话、目录、TLS及运行隔离探测独立，既有执行不热切换工具链。启动日志分开记录静态发现和各Agent原生探测阶段，不能把注册成功当成执行工具就绪。
- 准入前的就绪提示只读声明。会话`currentBinding`可能查询数据库，因此只在原权威准入边界保留它；已验证的技能目录按相同sessionId联接声明，不逐技能重新验证身份。
- 自动首轮沿用原bootstrap意图/退避；手动后续消息在工具未就绪时返回`TYPED_DELIBERATION_RUNTIME_NOT_READY`，表示本次没有受理。Web保留草稿，不自动重发；显式重试原内容沿用原键。与网络丢响应的“受理未知”分开处理。
- 原键已有回执优先；若前置未就绪导致没有准备包，即使事务内刚变就绪，也拒绝本次新准入而不是在持锁期间读取冷包。下一次显式请求重新准备。没有待准入表、新队列或新应用轮询。

- 本次在线日志确认静态base/document/browser发现和最终验证各一次；两个原生执行配置ready，三位Agent通道连续三次新鲜采样正常。真实主机浏览器/文档隔离及完整启动探针通过；没有新建业务任务，不把这些证明称为完整业务任务验收。当前主机并发负载较高，未作受控前后对照，不能据此宣称整体启动加速。
- 外部系统Codex升级可能使已绑定旧引擎的图片认证失效；发布前须用实际引擎和真实合成输入更新认证，不直接改旧摘要或去掉完整性校验。本次实际九种图片的一次组合识别通过，只更新林冲/吴用的认证文件引用，身份/模型/权限不变；备份及配置差异见本次handoff。

### 推荐承办：轻量读取与独立模型配置（2026-11-03源码核对）
- API develop `33da2486eb2587a68ae1de2225bf76f1907e1d3d` / 1.1.17-SNAPSHOT，Flow5260799/453验证；本段是源码基线，不表示当前线上已安装。推荐保持单次模型调用、无工具/记忆，不改HTTP/前端/Runtime。
- 只为推荐准备任务必要字段、候选能力和资料；不装配无关承办/资金详情或Agent历史任务统计。SkillAgentVersions读路径复用保留权限的无统计能力投影；写入事务/锁/CAS不变。推荐每轮技能快照只读一次归属/版本，前后任务/能力/附件一致性检查仍在。
- 2026-11-03按用户最终要求的配置收口源码`b5595c99cd07466489f24c1a51e1bcff50d88e35`：整个主机application.properties的122项配置合入API `starter/src/main/resources/application-prod.properties`并随JAR发布，原ENC凭据保持密文；全局`gpt-6.1-sol`保持原外置值，生产`jia.chat.recommendation.model=gpt-6-luna`、`jia.chat.recommendation.reasoning-effort`留空继承；仅覆盖推荐options副本，连接/凭据/传输仍复用。当前推理选项适配OpenAI，其他类型非空配置显式拒绝，不静默忽略或自动重试；网关支持的模型/参数需实测，不能以配置项存在宣称已换更快模型。
- `assignee_recommendation_timing`分前置/模型/后置及模型外服务耗时，`assignee_recommendation_observe`分候选和证据读取；结合已有HTTP总耗时做端到端验收。目标模型外<3秒不是强制deadline，尚未真实上线验收。完整证据及下一步见JYT-MODEL-RECOMMEND-20261028 handoff和规格evidence-latency-model-config-20261103.json。
- 2026-11-03 16:11线上核验：上述全量配置候选`b5595c99`/1.1.19-SNAPSHOT/Flow457已安装，取代仅模型键方案；原外置文件122项全部逐值核对后已从主机删除，删除后的独立重启健康UP、JAR/进程摘要MATCH，无模型CLI/env覆盖。推荐使用`gpt-6-luna`，全局保持`gpt-6.1-sol`。原始配置备份`/home/isp/baks/cyf-api-config-merge-20261103/application.properties`；回退旧JAR须同时恢复该外置文件。该记录是配置/启动验收，不是推荐端到端性能验收。证据`specs/juyiting-assignee-recommendation/evidence/evidence-config-in-jar-20261103.json`。



### 外部接单Agent的推荐技能摘要（2026-11-04源码核对）
- 源码候选`b71b559fe8527daac7b44e66856c095b70d46e01`，本段描述实现，不代表当前线上已部署。候选发现仍由ExternalServicePolicy统一执行事项归属、同tenant/client、当前有效绑定和接外单开关；推荐通过内部投影取得真实提供方身份，不把调用用户当作外部Agent的owner。
- SkillManagement在既有批量读取中为授权候选提供已安装、已启用、仍公开产品的技能名称/用途/可用状态；认证目录使用真实提供方scope和当前session fence，不冒充提供方Actor，也不开放其技能管理接口。指令型与可执行型继续使用原有可用证据语义，缺证据不宣称可用；无可确认摘要显示“暂无可确认的接单技能”。
- 推荐模型沿用单次`gpt-6-luna`调用；传入技能摘要，不提供外部私有本领、安装标识、技能键/版本或owner。HTTP外部技能依据用本次`public-skill:N`引用，既有接口/Web/Runtime均不变。模型前后重新观察；接单撤回、提供方改变或技能事实变化按既有409使旧结果失效。
- 定向验证覆盖候选SQL权限、提供方目录隔离、停用/退市、脱敏及快照失效；证据和合入/发布状态见`docs/implementation/handoffs/JYT-MODEL-RECOMMEND-20261028.md`，不将测试通过等同于线上真实数据验收。


### 成果即时投影候选（2026-11-03核对，未发布）

API develop `06dc2a725249746eb0a0cc515c2d3601de0817b9` / Flow5260799/455已验证：原生结果/明确失败/撤销提交后提示既有Chat成果处理器，按scope+executionId定向查询，独立投影事务保留授权/摘要/幂等；原5秒扫描改为30秒遗漏补偿。普通文字final仍走已有即时唤醒的FINAL_PERSISTED outbox，不经过asset relay。此候选未安装，没有端到端回复提速实测；不能从Flow成功推导线上已改变。边界、测试与失败保留见handoff JUYITING-POLLING-20261102末节及其result-notify-20261103证据。


### 成果即时投影上线核对（2026-11-03 15:32）

API `06dc2a725249746eb0a0cc515c2d3601de0817b9` / Flow5260799/455 / 1.1.17-SNAPSHOT已安装，取代上节“候选未发布”状态；JAR/进程/健康和原版本备份摘要已核验。Web/Runtime未改动或重启，Runtime自动重连3位Agent恢复ready。成果提交后的定向提示和30秒补偿为当前实现，自然60秒窗口空扫描2次（旧窗12次），无新增表/MQ；即时路径生产端到端延迟尚无新任务样本，不等同普通议事文字回复已提速。稳定机制见API既有native-work-notifications文档；证据与性能边界见`docs/implementation/handoffs/JUYITING-POLLING-20261102.md`的15:32发布记录。

### HTML/Markdown入口补齐（2026-11-03，源码fcbdf0f）
选择资料（PC侧栏、手机预览、已选资料独立弹窗）、私人办事成果固定版本区复用RichDocumentPreview。议事附件由HallMessageMedia接入同一静态渲染器；读取仍走已授权会话资产/资料固定版本接口，保留身份切换与迟到结果隔离。唯一离线原型本地上传读取正文，并可从旧本地data URL恢复原始文档，不把占位文字当正文；资源缓存版本随字节更新。本条为源码覆盖说明，不代表生产已部署；定向和浏览器证据、正式Flow及未验证项见HTML-MD-PREVIEW-20261103 handoff的“入口补漏”节。
- 2026-11-03 16:22同线上b5595c99/457小样本补充：同一事项4候选串行推荐3次，HTTP15.597/11.756/10.143秒，模型外0.691/0.215/0.247秒；前两次READY且识图候选优先，第三次502 CANDIDATE（模型候选标识校验失败，未知/重复细分尚缺证据）。同PID较早自然请求模型外仍出现7.079/4.130秒，故不宣称稳定<3秒或P95达标。性能与成功率须同时观察；当前未追加修复/换模型/部署。证据见/home/isp/state/jyt-recommend-latency-20261103/live-measurement/summary.json及当前推荐handoff。

### 禁止出网探针即时拒绝（2026-11-03 17:14上线核对）

Runtime develop `f6d5c2925aecc81c48f69f6c39925b04dc378a9e` / Flow126 / 1.3.39（bridge1.1.29）已安装到固定app。nft的input/output仍default-drop，仅在既有允许项之后对禁止的出站连接显式REJECT；允许目标、连接超时、真实代理/宿主canary/直接出网探针及进程归属校验不变。不增加队列/定时器，不跨执行缓存隔离状态。

真实候选主机探针和两个线上native profile就绪已验证，新task587的22字节文本成果及认证下载通过；这不是性能达标：普通续聊final SSE11.311秒，文件请求到成果196.946秒，执行准备仍63.936秒；成果提交记录到投影47ms。API已独立升级457，不能把自然样本前后差异都归因此Runtime补丁。约30秒负向探针等待已消除，但其他准备/派发/回复确认仍需分段定位；不通过删持久化、锁或必要隔离校验追求表面缩时。恢复、固定源及完整实测证据见现有JUYITING-POLLING-20261102 handoff的17:14节，当前运行状态仍以release record为准。
- 2026-11-03推荐精简开发：develop4ff35d7b已集成请求内短编号、独立紧凑模型投影及精简Prompt；原完整候选/附件快照与HTTP字段保留，Luna不变。模型直连3组前后样例平均10.60→7.28秒，6次有限断言通过，不能代替线上端到端验收。Flow459验证推荐候选1cfbf741，非合并后的develop整包；当前未部署。完整来源、集成差异与复测证据见推荐handoff和/home/isp/state/jyt-recommend-compact-20261103/。
- 2026-11-03 18:04集成验证补充：上述develop4ff35d7b/1.1.20-SNAPSHOT已由Flow5260799/461完成定向回归/分层/fresh JAR及同Run制品核验，132项全部通过（推荐37、并发技能/岗位/Mapper29）；原460缺测试数据库夹具失败保留，修正云端夹具后461通过，未改应用源码或跳过测试。固定产物在/home/isp/state/jyt-recommend-compact-20261103/integrated/release-fixture/api-artifact.tgz，SHA784c9a1e1f58572aad24075daed8f4429a0e8085e1c961b8925cb1ab3c75b20c；仍未部署。后续授权发布同一候选复用461，不把459旧树包作为集成版，不重跑构建只为安装。
- 2026-11-03 18:46线上增量核验：固定Flow461/4ff35d7b（1.1.20-SNAPSHOT）已安装，PID2780007，健康/摘要/canonical路径通过，包内推荐gpt-6-luna不变。三次事项573推荐分别200/409（候选证据快照变化）/502（CANDIDATE_COVERAGE），耗时20.819/10.211/6.069秒；模型外5.147/4.229/0.972秒。**业务及性能验收未通过，不能声明精简已带来线上提速或稳定<3秒。** 首轮识图技能被标不可用，后续技能只读查询已恢复可引用状态；原因尚须细分，不能仅修改Prompt掩盖证据。当前记录覆盖此时点，不代表后续其他任务发布；详细证据见推荐handoff及/home/isp/state/jyt-recommend-compact-20261103/live-measurement/summary.json。

### 最终回复与原生准备阶段诊断（2026-11-03 19:11上线核对）

Runtime `7ca605e51ec27d6952245b4c55d148471f3e90e2` / Flow5264702/127 / 1.3.40（bridge1.1.30）已安装并完成通道、两native profile及合成task589文字/正式文件核验，取代上节126程序基线；身份、模型配置未改。真实运行及来源以`/home/isp/apps/cyf-agent-runtime-v1/release-records/current.json`为准。

- ACK查找只缓存文件身份与turnId，不缓存正文/技能包；每次仍stat发现变化、权威回读匹配记录，冷启动仍读所有保留记录，不是O(1)索引。
- 既有journal新增`chat-final-storage-timing`（锁/操作/释放）、`chat-final-send-timing`（send返回）、`native-execution-prepare-timing`和`app-server-initialize-timing`。不新增定时任务，不将send返回视为服务器持久确认，不将prepare子阶段视为整条执行请求。
- 589正确性通过但性能未证明改善：文件发送→成果163.798秒，普通续聊final28.925秒；API461/Web417与旧样本不同。原生准备中egress-bind47.987秒、可执行回读6.017秒，模型/MCP/技能发现仅毫秒级；文件最终回复send返回后到确认23.902秒，查找3.46ms不足以解释该间隔。继续沿实际进程归属绑定和final确认链路定位，不取消隔离/幂等/持久化来换表面速度。详细证据与未完成项见既有Juyiting polling handoff及`/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/reply-latency-20261103/retest127/`。
- 2026-11-03 20:20候选核验（源码62ba7b942e，非线上切换）：推荐每轮共享产品/版本、批量读有效安装授权，空技能不查运行目录；不再因目录测量时间/无关技能变化把整批技能置CHANGED。模型前后真实能力/权限/附件变化仍拒绝，单纯显示状态变化使用后置权威状态。模型输出通过严格Schema要求全部候选键，API按模型rank还原原HTTP数组，不自动重试/补造结果。Flow464的145项回归及制品闭包通过，已合develop、未部署；三组合成模型平均6.771秒仅证明样例匹配与覆盖，不是线上3秒验收。交付/复测入口见推荐handoff和evidence-stability-20261103.json，模型仍为Luna。

### 最终回复API计时读法（2026-11-03源码核对，未部署）

源码API `e584b977a5a622ef917311d35abecf463936204a` / Flow466增加每个durable final一条`CHAT_FINAL_TIMING`，不记录正文/凭据、不逐token打点、不新增SQL或后台扫描。`startedAt`是handler入口墙钟；所有`*Us`是同一单调时钟原点的微秒offset，`-1`表示未进入该阶段，不能当零耗时。

- `persistEndUs-persistStartUs`：最终回复的完整fenced事务，包含获取锁及提交；不等于纯SQL执行。
- `hostedEndUs-hostedStartUs`：已持久化后的派发回执事务；本批只观测，未重排/删除此步骤。
- `sendLockUs-sendStartUs`：进入发送同步块前等待；`sendEndUs-sendLockUs`含序列化及send调用。`sendReturned=true`不是Runtime已收到或socket已flush的证明。
- `result`区分PERSISTED/DUPLICATE/REJECTED，失败或断线不伪造成功。ThreadLocal在每条消息结束清理；只使用turnId作关联，不依赖请求正文。

固定新任务实测时结合Runtime既有final send及confirm storage计时；API入口前的排队/传输和发送返回后的网络/Runtime事件循环仍须结合两端时间，不能全算成数据库等待。Flow466的110项定向及制品安全回归通过；此处是源码/观测语义核对，**尚未安装此API候选或证明24秒根因**，当前运行版以安装记录为准。

### 推荐承办线上复核（2026-11-03 20:47）
- 上述候选62ba7b942e已通过固定Flow464制品受控安装；API1.1.21-SNAPSHOT、PID2855106，健康/摘要/canonical核验通过，包内推荐Luna不变。三次真实推荐均READY、4候选完整，无409/502；总耗时17.361/7.375/7.211秒，模型外2.291/0.328/0.317秒，仅说明本组三样本均低于3秒，不代表稳定SLO/P95。
- 推荐语义尚有不足：图片需求均被识别，但2/3次通用分析候选仍排在明确识图候选之前。下一步Prompt需强化读取资料的前置能力与后续分析的区别，不用代码硬编码文件类型，不将本轮记为完整业务验收通过。来源及恢复记录见推荐handoff、evidence-stability-20261103.json与/home/isp/state/jyt-recommend-stability-20261103/release/deployment-verification.json。

### 最终回复计时上线基线（2026-11-03 20:52核验）

API466 / `e584b977a5a622ef917311d35abecf463936204a` 已安装并核验健康、运行JAR摘要与canonical路径（PID2857741），取代上节464运行基线，包含其推荐改动。上文计时语义现可用于线上诊断；安装成功不代表24秒延迟已归因或改善。来源/恢复与核验证据在既有polling handoff及`reply-latency-20261103/ack-api-integrated-ci/api-online.json`。Runtime128仍在独立安装验证中，不能提前当作当前程序。

### Runtime128与消息积压诊断基线（2026-11-03 21:41核验）

Runtime128 / `c68773c6cb23b1ea5c7fa9217c00de0f451d8aea` / 1.3.41（bridge1.1.31）已安装、689 payload摘要与mode核验、三次fresh通道及两native profile通过；程序安装不等于业务/性能验收。共享的是最多两个可执行文件的摘要证据，不是文件内容或技能包。task591文字正确；文件执行遇他人API467部署/502，最终FAILED，无权威outputs，不算文件验收通过。当前API已被其他Owner更新至467（包含466计时代码）；实际版本始终查各组件release record。

本轮96字符的46帧delta持续到finalPrepared后60.118秒；Runtime首次final send返回至API handler入口60.091秒，API最终消息处理1.996秒。主要瓶颈在final handler之前，不能把这60秒都当最终数据库事务。Runtime新执行egress-bind仍47.955秒，摘要优化未证明消除绑定瓶颈。后续诊断优先检查碎片发送/持久处理积压、未确认final重复发送及真实sandbox进程出现等待，不去除身份/隔离/最终持久事实。精确证据、并发安装限制与未完成项见既有polling handoff和retest128/。

### 推荐读取前提Prompt（2026-11-03 22:19源码核对，未部署）
- develop e2e33bc67c：任务确需读取附件内容时，先匹配读取能力，再匹配后续处理；通用统计/文档用途不证明可读任意格式，简单统计又不要求额外专用技能。多附件由同一候选覆盖关键输入，不拼借其他候选证据；只操作文件名/已有足够正文时不强加附件读取。仅依据本次证据，自有优先不弥补关键能力缺口。
- 不改接口、模型、调用次数或服务端排序规则；Prompt由模型解释能力用途，不做文件后缀映射。Flow469的106项回归通过，8组合成真实Luna语义样例通过；未部署、不是线上准确率/性能证明。制品与后续验收入口见推荐handoff及evidence-reading-20261103.json。

- 2026-11-03 22:51部署补充：上述读取前提Prompt版本e2e33bc67c/1.1.23-SNAPSHOT已通过固定Flow469制品受控上线，PID2932716，健康/制品摘要/canonical路径及包内Luna配置通过。保留此前线上467/cd548fa6fa改动；没有重复构建。本次未执行真实推荐或测性能，不将技术部署成功视为完整业务验收。安装/恢复记录见推荐handoff及/home/isp/state/jyt-recommend-reading-20261103/release/deployment-verification.json。

### 回复传输合并与确认重试（2026-11-03源码核对，未部署）

Runtime develop `fa8e2cd51c48dee10cd76b2305a854adb1bdf4b1`（1.3.44 / bridge1.1.34）经Flow133固定源码回归验证。首段用户文字立即发；后续仅在有待发内容时按200ms窗口合并，finalPrepared前立即flush，序号按实际发送帧计。完成/取消/异常释放尾段与定时器，不新增空闲轮询、全文缓存或服务；窗口是初始交互设置，不代表实测最优或强制请求deadline。

final已写入WebSocket但未获API持久化确认时，使用既有最大补偿间隔（默认30秒）；NOT_SENT沿用250ms起步指数退避。真实重连立即恢复，重复ready不能绕过间隔；确认取消定时器，排队恢复前重读持久状态避免已确认消息重放。最终完成权威仍在API，不把写入成功等同确认。

每次egress owner绑定输出一条`egress-owner-bind-timing`聚合，区分进程扫描、祖先判断、可执行文件测量、等待和最终owner检查；不增加扫描或删除隔离校验。只有新版本真实分段记录才能解释此前47.955秒，不从单元测试推导线上提速。Flow133为纯回归证据：842 Node PASS、17 Python PASS、10原有真实宿主探针SKIP；无生产包/安装。当前运行版本始终以release record为准，详细范围及证据见现有polling handoff。


### 2026-11-04 流式预览实现基线（源码已集成，未上线）

核对范围：API develop `81d9c1b1b6`、Web develop `ffb2e56`、Runtime develop `3fbd562`；云效API474/Web422/Runtime134通过，详情见现有JUYITING-POLLING-20261102 handoff。本节不改变历史线上版本。

- Runtime正常用户文字逐段发送；API首段做一次现有身份/任务准入与送达确认，后续只用连接内元数据转发，不写delta日志、不推进业务版本、不逐帧查库或确认派发。
- Web独立接收无SSE id的`conversation.preview`，不推进持久游标；缺帧/晚加入/断线可放弃预览，不触发补帧或执行重放。完整最终回复仍可靠提交、持久化及通知，并替换临时气泡；工具成果和完成事实保持原权威链路。
- 取消依据业务stateVersion，不依赖字符序号；首字观测每请求只记录一次。无新表、新全文缓存、新MQ服务或新补扫任务。
- 移除Runtime200ms合并和固定30秒final等待是配套变更；发布须与新API/Web组合，不独立推到旧逐帧事务API。Runtime134仅回归证据，不是可安装生产制品；部署后再核验真实耗时与资源收益。

### 2026-11-04 流式预览发布状态补充

API474(81d9c1b1)、Web422(ffb2e56)、Runtime135(3fbd562/1.3.45)已受控安装，健康/通道通过；**业务流式验收未通过**：普通浏览器已观察热预览丢帧，首字显示后消失直到最终完整回复。完整final及刷新记录正常，不等于预览体验达标。根因定位和后续边界见`docs/implementation/handoffs/JUYITING-POLLING-20261102.md`“08:00”节。勿将早期“未部署”记录或本次健康成功视为当前完整验收。

### 2026-11-04 08:31 已核验的预览背压修正

API475/509325a971已替换474，Web422、Runtime135不变。API预览连接使用独立有界发送队列吸收MVC写出抖动；不缓存全文、不定时批处理、不修改durable预取或持久化。新事项真实浏览器375帧连续、预览与final一致且刷新后仅一条，覆盖上节已知丢帧失败。实际模型首字仍约7.6秒，本批只证实显示连续性，不承诺总体提速；测试/发布证据见handoff及ephemeral-backpressure/result.json。

- 2026-11-04 08:57外部接单技能摘要发布记录：API `b71b559fe8527daac7b44e66856c095b70d46e01` / 1.1.24-SNAPSHOT / Flow5260799/477已授权安装，JAR/进程MATCH、健康UP、canonical通过；登录及事项列表200。专用账号无open事项，未做真实推荐业务验收。此为当时发布记录，不代表后续当前线上版本；证据见推荐handoff同日部署节。


### 任职 Agent 密议维护技能（核对：2026-11-04）

覆盖API `8da724fecd0949a3245b0f369cbdd3b75febe1c1` / Flow479，Runtime `d4dd804724c49947b9169264defb40c852dc7b4c` / Flow136；两端已安装，独立包`skill-management@1.0.0`已发布并随“技能管理”岗位在吴用安装。

- 使用入口：与已任职、已核验安装该技能的Agent进行**无附件私有密议**，明确要求查询、修改标题/描述、审核发布或下架目标技能。安装包不授予岗位；API每次检查当前任职及会话，不能借其他Owner/事项的执行授权维护平台目录。
- API提供六项技能维护工具和权威回执；bridge通用运输目录/回调并加载已验证SKILL.md，不按技能名编排业务，不给模型用户JWT/Runtime token，也不因业务工具开放本机写入/任意网络。
- 当前真实模型验收为读取→元数据修改→读回：商品修订2→3、包版本不变，请求COMPLETED且独立商品GET一致。发布/下架已有云端回归，但未做生产模型破坏性下架；附件密议不继承维护工具。不要把文字“已完成”或安装READY当作业务提交证据。
- 证据与部署追溯：`docs/implementation/handoffs/REUSABLE-SKILLS-20261102.md`末节及`/home/isp/state/cyf-skill-management-chat-20261104/final-verification.json`。历史2026-11-02“未获得模型通道”仅为旧基线，现行范围以本节为准。

### 2026-11-04核对：议事通用文件输入已部署（限定验收）

API `5b96cd8d6e`（Flow497）及Runtime `f12ab41`（Flow142，1.3.50/bridge1.1.40）已部署；当次真实核验林冲/吴用输入声明保留原生图片，新增LOCAL_FILE：bridge交付授权只读路径，由模型使用既有工具读取，不在bridge按格式解析。TXT、DOCX、XLSX、PDF＋PNG真实页面验收通过，移除材料后仍在同thread/Home追问；不表示扫描PDF/OCR或所有格式均已认证。

当前已知性能限制：沙箱文件名`.input`会导致openpyxl直接按路径读取时因扩展名失败；模型可改用文件流，但实测发生额外交互，四文档＋图一轮53.23秒，不能套用隔离探针17.16秒。功能已发布不等于全部性能优化完成。生产profile引用的Run142 carrier evidence需持久保留，配置引用路径及恢复/源码/业务证据统一见 `docs/implementation/handoffs/JUYITING-POLLING-20261102.md` 22:14收口节。此处为当次发布核验，不代替后续线上版本查询。

#### 2026-11-04 LOCAL_FILE 命名修复（Run143已发布，23:21核验）
Runtime1.3.51 / bridge1.1.41，源码 `ad6dc453fe2a5b338e66c870b0e26e2f7e42e040`，Flow5264702/143制品已安装到固定app并完成健康/业务核验；API497及Web未发布。仅LOCAL_FILE落盘按现有MIME生成 `.xlsx/.docx/.pdf/.txt` 等后缀，未知类型仍`.input`；不信任用户文件名，不转换原文件，不新增解析或缓存。原生产载体证明/配置沿用，其他载体命名及会话策略不变。
真实线上四文档＋图片首次批量读取成功，openpyxl直接使用`.xlsx`路径，无BytesIO绕过或扩展名错误，工具2→1次；单次完成DOM53.227→35.093秒，零附件追问12.085秒（上轮11.939秒）。三轮复用发布前同一thread/Home并核对持久化最终回复。仅单样本，不代表普遍提速或全部优化完成；首条/材料轮约9秒原生turn前准备仍是后续分析线索。
安装备份在`/home/isp/baks/cyf-agent-runtime-v1/20261104-chat-file-extensions-143/`。完整证据见原handoff `JUYITING-POLLING-20261102.md` Run143发布节及`/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/conversation-continuity/local-file-implementation/file-extensions/release/`。原Run142下载tgz已作为本线程过时副本回收，云端/摘要/备份保留；原`release/runtime-install/carrier-certification/`仍被生产profile引用，不得按临时目录删除。

### 沙箱启动事件化（2026-11-05核对：Run145已安装并定向验收）

Runtime develop `c378f5b6210f6926190c6e60d5cf3d7e5f0186f5`（已安装1.3.52/bridge1.1.42），Flow5264702/145已验证并生成固定制品。bridge通过bwrap独立信息管道取得沙箱reaper PID/netns，网络层绑定该稳定进程；现有initialize响应表示应用能处理协议，响应后对本次进程子树作一次可执行文件核验，再继续账户/配置/工具准备。原启动发现全局/proc轮询和沙箱可执行文件等待轮询已删除，无定时扫描fallback；身份、netns、网络允许列表及退出清理仍保留。非沙箱路径未改。

这不改变聚义厅会话映射、材料授权、最终回复落库或模型。2026-11-05已从固定Run145制品安装并核验691个payload文件、三Agent就绪以及普通/材料/移除材料三组新请求，仍复用原thread/Home，最终落库与DOM一致；API仍Run497，profile/模型未改。生产启动窗口内绑定24.472/10.396ms、全局扫描0轮，但initialize仍6.167/5.492秒。旧bind等待app-server、新bind绑定reaper，计时边界不同：准备总耗时仅9.141→8.468秒、9.712→8.806秒，不能把bind差值等同端到端收益。单样本不作普遍提速保证，后续瓶颈定位应针对真实初始化阶段。详情、失败Run144修复及本轮发布/实测证据见现有`JUYITING-POLLING-20261102` handoff。

### 工具链挂载优化候选（2026-11-05核对：已集成，未安装）

Runtime develop `b144d3d67734ef30b81eeb5c6cfdf34acd4f97f9`（1.3.53/bridge1.1.43），Flow5264702/146成功且固定制品已校验。此前日志的initialize等待包含bwrap逐文件准备工具链，不都是app-server内部处理。候选在既有工具链完整性验证时，将精确manifest闭包的依赖目录合为只读挂载；未知文件/链接/空目录阻止该目录合并，保留原逐文件视图。复用既有文件/祖先元数据校验失效计划，不新增轮询、状态表、复制工具树或每帧检查，原文件清单/摘要及CHAT/原生权限不变。

同主机无凭据探针工具链1682文件保持不变，挂载1682→796；初始化原5.315/5.213秒、候选约1.3～1.5秒。CHAT文档、原生文档/浏览器/PDF及37个目录内923文件的集合/SHA验证通过；不是线上耗时或百分位。当前生产仍为上节Run145。用户后续决定由长期固定工具链目录方案替代本候选，不再默认安装Run146；不把develop/Flow成功当上线。完整来源与边界见`JUYITING-POLLING-20261102` handoff。


### 安装期固定工具链目录（2026-11-05，Run147已安装，业务验收部分通过）

Runtime1.3.54/bridge1.1.44，源码`c9b265645910a4ea646e82680b2f890424110643`已合develop，Flow5264702/147通过（940pass/0fail/15skip，276秒），08:19已在固定app安装，新PID4012212。删除Run146动态目录分组：Flow继续供应锁定的Python/browser制品，目标主机在独立安装暂存阶段通过`runtime/lib/prepare-toolchain-image.mjs --root <stage>`一次性生成`codex-bridge/.sandbox-toolchain/rootfs`。必须在依赖展开之后、stage验证和停生产之前调用，不运行源码构建/下载，不在业务请求里复制；系统库取目标主机原依赖闭包，不混入worker libc。

启动仅读取固定manifest并沿原完整性核验；请求共享冻结对象及原元数据漂移检查。只读挂载专用rootfs顶层目录，不暴露宿主/usr。当前同1682文件为3次工具链目录挂载，实际目录集合/字节均已比对；额外磁盘副本约532MiB（不是每会话内存缓存）。新目录纳入原安装manifest及程序归档/恢复，源文件更换不会自动刷新；缺失image明确失败，不回落宿主发现。安装前须核对真实空间与既有锁/备份。

无凭据native/CHAT初始化探针约0.548/0.209秒；进程首次工具链加载及完整性核验另约3.068秒，不能混为线上端到端提速。Run147已安装并核对692个payload文件及新PID的三次通道READY；最终路径10类材料认证已重测，只更新两份profile的派生证明。正式Flow、集成与后续部署状态见`JUYITING-POLLING-20261102`handoff，探针证据在`/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/toolchain-image-20261105/`。

发布注意：现有材料就绪证明的指纹包含工具链物理路径，新image布局不能复用旧指纹。发布须沿既有最终路径certify-installed流程重测并受控更新派生证明，再验证READY（Run147已执行，证据在toolchain-image-20261105/release/runtime-install/carrier-certification，必须保留）；不是新增每请求验证，也不授权自动改模型/业务权限。

Run147实际单样本：普通问答首字/完成7.490/8.583秒，5附件20.145/20.386秒，无附件后续7.812/9.315秒；同原thread，点击→native分别2.709/3.114/2.179秒。前两组准备开销比Run145减少约5.7秒，第三组未改善；不作为P95/稳定提速承诺。进程初始工具链核验另计2.849秒，不隐入请求收益。

**业务未全通过**：TXT/DOCX/XLSX/PDF随机码、原会话连续性及最终文本落库均正确；蓝红双色图两次被答为纯蓝。两个native输入记录的图片字节与上传原件完全一致，图片适配相关源码与Run145相同；仅排除bridge输入损坏，未定位app-server之后的Provider/模型链路根因，不能认定是模型自身或发布回归。保留原始失败、停止同输入重试，不把安装认证通过替代真实识图验收。发布记录维持待业务核验，channelHealth=PASS、businessAcceptance=PARTIAL_IMAGE_SEMANTIC_FAILURE。证据见release/live-acceptance.json、image-semantic-diagnostic.json、startup-timing-comparison.json；诊断脚本首次同步点击移除按钮导致仍带4附件的样本已单列排除，真实无附件样本为sample4，未覆盖失败证据。

### CHAT 上下文增量发送（2026-11-05核对，API505 / Runtime151 已安装及定向验收）

固定源码：API `45440c6e71cf9b6e447e42114e866554f666d2ec`（1.1.33-SNAPSHOT），Runtime `b2d5f5700118dd148017a3db132e13d7e66bc020`（1.3.57 / bridge1.1.46）。后端负责原生CHAT的历史窗口及派发快照：首轮BOOTSTRAP，后续按已完成回执的游标准备DELTA。bridge只绑定原生thread并在正常完整final中附完成回执，不维护第二份历史缓存、不在bridge猜测去重、不新增每段输出落库或RPC。完整最终回复及业务完成事实继续按原事务持久化。当前任务/授权/材料等权威事实仍按合同发送，增量历史不等于把所有业务事实都改成差量。

新测试事项600、会话1760458009355的初始化及四次续聊全部PUBLISHED/COMPLETED，完整final与DOM摘要一致；一个native thread共五轮，数据库确认1个BOOTSTRAP、4个DELTA及连续游标/回执。普通→XLSX材料→移除材料仍同thread；XLSX真实openpyxl读取及前文校验码正确。这是新会话正常路径验收，不包含生产故障注入、历史任务迁移、全材料类型或识图语义验收，不覆盖上节既有识图问题。

四个短样本DOM首段/完成分别8.218/10.331、9.335/10.649、17.100/17.289（XLSX）、6.250/9.099秒；实际模型gpt-6-luna，本轮未改模型。点击到native turn开始1.840～2.446秒，native完成到最终DOM0.232～0.740秒；中段含原生执行/Provider及工具，不能一概称纯模型推理时间。这不是P95、负载测试或可比前后提速结论。测试浏览器无交互的独立60秒窗口未出现网络响应；不推导整个系统没有后台补偿查询。

源码/云端/安装/业务证据分别见原`JUYITING-POLLING-20261102` handoff及`context-incremental-20261105/live/live-acceptance.json`、`database-and-native.json`。缺失thread恢复仍要求明确未执行证明；本轮未在生产注入该异常。当前实时版本仍以安装记录和PID为准，后续发布不由本节自动证明。

### 典籍管理岗位与原生技能（2026-11-05 局部核验）

- 岗位名称“典籍管理”，关联技能“典籍维护”`archive-maintenance@2.0.0`，当前指定任职为chcbz所属吴用；与“技能管理”岗位并存，不扩成全站管理员。岗位配置/任命必须沿既有 `/agent/positions/v1` 和真实自动安装回执，不手工补订单或安装状态。
- 原生技能包源码isp-install `6b7035038b7e4af8a86d449df66d3587ceeef7f0`，Flow5264702/152，6项定向测试通过。只发布技能ZIP，不安装Runtime程序。旧archive-maintenance1.1.x含执行manifest，不是当前原生安装候选；新包保留纯解析脚本，不启用旧runner。
- 本次实测吴用详情5项技能含“典籍维护”，安装核验和RUNTIME_READY均来自服务端真实结果。此项技能安装验收与后续密议发布分别取证；当日后续已完成原生工具接通及《三国演义》120回发布读回，见下节。详见 `docs/implementation/handoffs/ARCHIVE-MANAGEMENT-CHAT-20261105.md`，无关模块沿原基线。

### 典籍阁任职入口（2026-11-05 发布及线上局部核验）

Web 1.16.114（源码 `820755b00c32cbe6224e6c6148c27f934e042f51`，Flow4403172/451）已于用户授权后安装，入口/关键资源摘要及真实浏览器PC/390核验通过。第三页签收口为“任职管理”，保留任命/卸任、技能安装状态/恢复及岗位配置。典籍底本上传、维护任务创建、草稿/发布操作不再由典籍阁页面发起；任职页不另设密议按钮，维护对话从好汉详情原有“密议”进入，既有权限与显式目标选择保持不变。阅读/检索页签保持原行为。

任职读取只依赖 `/agent/positions/v1`，旧 `/archive/admin/v1/jobs` 不再阻断岗位展示；历史维护未决引用不自动删除或重放，历史任职未决引用按原幂等键恢复。此项Web证据仅覆盖页面收口；后续密议业务验收见下节。正式验证、合入与发布状态见上述 handoff。

### 典籍普通密议维护（2026-11-05 发布及全文核验）

API1.1.35-SNAPSHOT（4dc5c51d26b375c411fc8ff4aecee0fc3a1f51ea，Flow5260799/528，178项通过）与Runtime1.3.60/bridge1.1.49（5d7290c92b684c3fbc03120a5ad416d79918e589，Flow5264702/155，967项通过、15项既有环境条件跳过）已独立受控安装，通道及本节业务通过。技能动态发现和工具分发为通用机制，不按技能名、书名或好汉名路由；当前用户请求与不可信引用材料在bridge明确区分，业务授权及提交事实仍由API持有。

已验证入口为好汉详情原有“密议”，在普通会话中引用个人文件库固定fileId/version；带附件材料会话的独立工具视图未由本轮扩展或验收。吴用通过原生source/prepare/publish/read完成sanguoyanyi新版本，服务端PUBLISHED/active=true，120回17462段全部经正常阅读API读回并与固定底本逐段摘要/文本核对；旧版本保留，未重复建书。使用古典原著繁体全文，不由模型生成正文。

部署需存在制品自带的archive_skill_maintenance_job/action记录表；本次从API528 JAR精确DDL，在身份/发布锁和真实目录快照保护下仅创建两张缺失表，无CHECK、无内容DML、未开启旧runner。旧/archive/admin/v1/jobs关闭返回404不代表原生密议工具不可用，不以应用启动自动清库/迁移。

固定来源、快照恢复、请求/版本及测试/安装/全文验收分别见原handoff；证据汇总 `/home/isp/state/cyf-archive-conversation-20261105/acceptance/release-acceptance.json`。本节不重认证其他Runtime能力。

### 阅读器跨书切换失败恢复（2026-11-05 源码核验，未发布）

Web候选1.16.115/f3cd173b42c36fb493724214ac1f324d5646ac7c已合入develop，Flow4403172/452完成337项回归与构建/扫描。本次只修复客户端：上一书进度失败时，切书/“重试保存进度”为显式恢复入口，读回真实CAS版本再单次保存本地位置；重复失败在书架可见，不静默锁死，不循环覆盖服务器状态。并发恢复复用在途请求，身份切换后不提交旧位置；手札草稿按版本保留及未决写入保护不变。

线上当前仍1.16.114/451；本轮“修复”未授权安装，不能将上述候选描述为线上行为。后续发布复用452固定制品；测试/摘要/恢复入口见原ARCHIVE-MANAGEMENT-CHAT-20261105 handoff和 `/home/isp/state/cyf-archive-reader-switch-20261105/acceptance.json`。

2026-11-06实测补充：现网进度保存可能HTTP200/E0但响应body requestId=null，实际CAS已成功，Web拒绝不合规回执后下一次用旧version触发409。根因是API预序列化byte[]绕过公共JsonResult响应关联补全；并非所有409都是多页面并发。上述Web候选仅修复失败恢复/展示，不能单独当作根因修复。实测报文/数据不变证明及API责任边界见同一handoff最新节；本轮未改API/上线。

### 2026-11-06 典籍写回执关联修复（已合入，尚未上线）

API候选1.1.36-SNAPSHOT，commit `b7b4cf7e8ab6b7a39f1e010bb4133b7458e51b17`：典籍个人数据及问答的持久化写回执在HTTP适配层还原成`JsonResult`，由既有`ApiEnvelopeAdvice`填写本次请求的`requestId`；历史null/旧请求编号不作为当前关联信息。幂等业务结果、状态码、存储字节、CAS和权限机制不变，不能通过放宽Web协议校验来掩盖损坏回执。

Flow5260799/539已完成122项测试（0失败/错误/跳过）、分层检查及fresh JAR构建。真实服务+MockMvc覆盖首次保存、同键重放不重复更新、返回版本用于连续保存、真正旧版本仍409；问答202创建/重试覆盖历史空和旧requestId。与前端跨书恢复候选1.16.115为互补修复；两者均未在本轮安装。当前生产状态仍以上节已核实发布为准。完整回执、消费者验证及制品证据见`/home/isp/state/cyf-archive-progress-envelope-20261106`和既有handoff。

2026-11-06 07:27 CST发布核对：上述API539（1.1.36-SNAPSHOT）与Web452（1.16.115）已沿主机受控入口安装，无新增构建Run。API canonical JAR/进程/健康匹配；Web612文件及公网入口/典籍所在JS摘要匹配。新登录会话完成三国连续保存、水浒切入保存、三国切回保存，共7次UI保存200且请求关联正确，两书均“已保存”；另验证同键重放的新requestId与业务幂等。测试后两书阅读位置保持原值，版本按真实保存递增。证据及恢复路径见既有handoff发布完成节与`/home/isp/state/cyf-archive-progress-envelope-20261106/release/business-verification.json`；这次不含生产网络故障注入或其他典籍维护能力验收。

### 2026-11-06 阅读器图标按钮（已合入，未发布）
Web1.16.116 / `f69891f0e34c2d60a8b8788bbb1b17742ce7b34d`已合入develop。阅读命令统一线性图标，保留中文提示/无障碍名称、原事件和禁用/pending；正文、目录章回与定位描述不图标化。页脚同排44px点击区，覆盖嵌入与独立Teleport；不改变API/Runtime或进度写入合同。

Flow4403172/455 SUCCESS，340测试0失败/跳过，构建/扫描/上传成功；固定制品SHA256 `bc94f43d0528b2f35644961bce13f5dfb14e7c765e45db3a228371b2c99758e1`，612个dist文件与来源commit/tree/version完整匹配。此次未授权发布，无主机安装或线上验收；下一次发布可复用455，不重复构建。证据`/home/isp/state/cyf-archive-reader-icons-20261106/release/web-verified.json`及现有handoff。

### 2026-11-06 阅读器图标最终线上核对（替代上述116候选状态）
Web1.16.117 / `ea6f83801b053cec1eef9883048582e93984cb2a`已发布，Flow4403172/457通过340项测试及构建/扫描/上传；612个安装文件、公网入口及典籍资源摘要匹配。116实页发现320视口的222px宿主内容区会溢出，117仅将页脚gap收口为0，保留space-between、单行44px点击区和原业务处理，不引入设备特殊逻辑。

真实生产登录页在1440/390/375/320宽度核验图标、名称、点击区、无横溢出及笔记展开；独立Teleport与横屏仍属于已有fixture证据，不冒充本次生产操作。测试后两书阅读位置/state按最新测试前快照保留，真实版本正常递增，API539及Runtime未变。源码、云端测试、主机安装、线上UI和恢复/清理证据分别见ARCHIVE-MANAGEMENT-CHAT-20261105 handoff最终发布节及`/home/isp/state/cyf-archive-reader-icons-20261106`。

### 2026-11-06 微信嵌入阅读器工具栏修正（已合入，未发布）
核对源码Web `26373d2e01beeff6d0b4a63a3f4ea6fac1853ea8` / 1.16.119。嵌入阅读器由宿主承担胶囊空间，不再给header重复预留112px；独立阅读器仍按现有微信/原生方向标记保护胶囊。引用、继续阅读复用hall-tool，与翻回/书签统一透明底、透明边44px图标；删除旧引用品牌底色覆盖，不改变业务处理。

微信UA/宿主标记/native方向模拟夹具覆盖1440/414/390/375/320窄宿主，header右间距4px、同排44px无溢出；独立竖屏/虚拟横屏胶囊保护通过。Flow461对249cf90的340项及构建通过，最终集成仅额外修改样式回归，定向103项通过；不把旧Run重标成集成HEAD，也不把模拟当微信真机或线上。实际来源/制品、原型、截图和未发布边界见ARCHIVE-MANAGEMENT-CHAT-20261105 handoff与`/home/isp/state/cyf-reader-toolbar-alignment-20261106/integration.json`。

2026-11-06 11:03 CST发布核对：上述微信嵌入阅读工具栏修复已发布Web1.16.119，实际安装来源为Flow4403172/461 / commit249cf90 / treec14734a，未把制品重标成仅追加样式测试的develop26373d2。612安装文件和5项公网资源摘要匹配，真实登录生产网页在模拟微信UA/宿主/原生竖屏入口的1440/414/390/375/320宽度核验靠右、无框、44px和笔记开关；不是微信真机实测。两书位置/state按本轮before快照保留，API564记录未变。本节替代上文未发布状态；固定源码、备份、安装和验收证据见ARCHIVE-MANAGEMENT-CHAT-20261105 handoff最终发布节与`/home/isp/state/cyf-reader-toolbar-alignment-20261106/installation`。

### 议事历史的读取职责（2026-11-06源码核对）

范围仅议事数据模型、消息/成果读取与展示；API `e2cc3230`、Web `93c2a10a`。最终安装/验收状态见现有`JUYITING-POLLING-20261102` handoff；不要把此节当作整个Runtime性能已完成的声明。

- 一个会话有多个请求，一个请求可有多个执行回合；回合绑定好汉，消息保存可见正文，结构化成果保存语义事实，正式交付保存验收版本。当前typed准入仍为单好汉，保留基础1:N不等于支持广播。本次不新建表/服务/队列，也不删除历史完整回复。
- 消息接口`/chat/conversation/messages`每次一个GET返回最多20条及本页request/turn/outcome展示投影。游标向前读，更早页只在用户需要时获取；返回已释放位置按该页重取。Web不逐请求补查、不另发ID集合查询、不为成果标题扫描目录。
- 页面只保留可见窗口及正在交互的正文/投影；远页留游标/高度。DOM与数据释放均需验证，不能用折叠或仅DOM虚拟化替代。媒体高度变化、末页按钮消失用旧滚动锚点恢复。
- 正式验收当前context不含全历史，历史按需20批/页。标题/MIME/大小来自固定artifact版本的页内元数据；正文/预览/下载按需读取固定版本。缺失版本局部显示不可用，不能悄悄换最新版。
- 初始消息读取归loader；本地binding reset不是服务端resync，也不把“消息页还未返回”视为投影失败。翻历史页只adopt展示，不触发当前验收刷新；验收初始读归原composable，更新归现有业务事件和显式操作。真实断线重同步保留，流式delta不触发这些REST读取。
- 新增派生索引的回填由固定JAR显式执行，不能在启动时循环扫历史。wire eventVersion由sequence派生，物理旧列保留；旧JAR回退前需停写/锁保护下修复零version，恢复说明不得理解为用旧整表备份覆盖新业务事实。


### 无资料载体的原生执行就绪（2026-11-09源码及上线核对）

Runtime1.3.68 / `92df9eb8de9abf523dd7224e575c43329139a98b` 已安装。原生执行Owner与资料读取对象解耦：有工作区执行配置即可独立创建/测量/注册原生能力，不以materials/inputCarriers存在为前提；原生运行与详情能力声明使用同一Owner。无资料主体仍须有自身明确的原生Provider绑定；卢俊义已从自身codexHome配置提取gpt/responses绑定并配置既有代理要求的10000ms连接超时，不借其他主体身份/凭据，不改变模型；该值不是模型请求或发布deadline。

Web1.16.129 / `038a571a0604a2ef04041e575cd37c64f8f13a33` 已安装，255个线上入口及JS/CSS摘要一致。保留已核验安装状态，将NATIVE_EXECUTION_NOT_READY展示为“原生执行环境未就绪”；就绪异常不是重装依据，聊天成功也不是技能执行验收。真实ziyue登录只读接口及详情页面确认卢俊义网页操作、文档处理、信息检索三项均“已核验安装、运行就绪”；未触发付费模型/真实技能执行。API JAR未变。

主机Web原安装器以系统`/usr/bin/python3`执行以使用系统CA；不关闭TLS验证。共享依赖可选dependencies元数据仅供追溯，不参与授权或执行。固定制品、备份、安装失败/恢复及验收证据见NATIVE-READINESS-DECOUPLE-20261108 handoff；共享依赖维护见ops/orchestration/README。
