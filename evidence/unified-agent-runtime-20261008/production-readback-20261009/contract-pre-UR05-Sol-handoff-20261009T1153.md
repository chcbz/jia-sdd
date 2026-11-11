# UR-00 统一 Runtime 实施契约

2026-10-08，主控依据 UR-01/02/03 源码调查冻结实施边界。允许离线源码开发，不代表线上切换授权已覆盖共享服务全部身份。

## 固定基线与单Owner

- 客户端：`/home/isp/wsps/chcbz/isp-install` commit `0d80e588be271891348e38b8892d9b9a9b0bb436`。
- 服务端：`/home/isp/wsps/cyf/api` commit `ce047c43e0f275d1ad427c484b8919213be36fa4`。
- Knuth 为 UR-01 唯一客户端Owner，独立 worktree `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008`，分支 `codex/ur01-unified-agent-runtime-20261008`。
- Turing 为 UR-02 唯一服务端Owner，独立 worktree `/home/isp/wsps/worktrees/ur02-unified-agent-runtime-api-20261008`，分支 `codex/ur02-unified-agent-runtime-api-20261008`。
- Curie 当前为唯一只读辅助，不占用第三源码Writer；Hopper原UI尾项未核实完毕前不加第四Writer。主控独占根仓控制文档。
- 不切换脏主工作区，不覆盖未提交字节，不自动部署。每位Owner直接实施、自检、报告提交及路径，无独立Reviewer。

## 已冻结的共同语义

1. 一个 Runtime 主入口复用现有多profile执行器，不重写正常执行模块。主实例可有隔离执行子进程。宿主配置 `agents[]` 引用每个 sealed manifest/profile，各Agent使用自己的安装授权、队列和可写根；拒绝重复完整主体/installation及路径相同、嵌套、symlink别名重叠。
2. 完整主体是 `tenantId + clientId + canonicalAgentId`。持久宿主ID与每次启动实例ID分开，启动ID不能作为持久队列键；persona不参与授权。执行子进程环境按所需变量构造，不继承其他Agent/宿主凭据。目录隔离不宣称同UID的恶意代码强安全边界。
3. 唯一授权来源为安装授权。保留安装级 Bearer 管理接口；执行WS和native HTTP使用由安装授权派生、绑定安装/完整主体/当前会话代际的会话凭据，保留native `AgentRuntime <token>`格式，不保留旧API key认证回退。敏感会话返回必须用独立响应DTO，禁止把token放进可被UI读取的InstallationView、URL或日志。
4. 同一完整主体同时只有一个获准执行宿主。服务端必须使用可跨重连/重启验证的现有归属及代际机制；旧代际消息不得更新当前执行。禁止仅用本地map或广播匹配session来证明互斥。若现有持久归属不足，UR-02先回报最小schema/mapper增补路径及恢复方案，不擅改生产schema；其余不依赖部分继续实施。
5. 保留既有业务事件和工作键、ACL、租约、事务、锁序。不新增业务命令。所有投递、进度、成果及ACK校验相同安装/主体/工作上下文与会话归属。取消精确绑定原request/turn/dispatch及代际。
6. 命令ACK统一以Runtime HTTP ACK端点及D06事务结果作为提交确认，既有成熟checkpoint为唯一持久队列；不再维护第二份pending-acks权威状态。`ADVANCED`/`PRIOR`及匹配status/deliveryVersion才是提交结果；本地WS send成功不是提交。非命令的CHAT/成果回执保留其业务语义及既有专用确认，不误套D06。
7. 接收与指纹持久化后才允许RECEIVED；业务副作用前先确认执行归属并持久化STARTED且取得所需服务端确认。终态本地持久化后可靠提交；成果服务端确认前不能报成功或删唯一恢复材料。重复ID不同payload必须拒绝，不仅按messageId去重。
8. 命令过期只约束新执行准入，不拒绝已执行工作的补报。未知执行结果标记recovery-required，不自动重跑，不清队列。重启可重发回执/查询既有结果，不能凭重连重执业务。
9. 健康心跳不等于可执行。就绪依赖授权有效、当前定向通道确认、持久状态健康及对应真实adapter可用；单项多媒体不可用不一刀切影响其他能力。单Agent撤销只隔离其自身，不能关闭其他Agent。
10. 单制品覆盖Runtime、执行模块、现有Python交付工具与依赖闭包；固定Node版本并验证干净目标安装，不能在生产回退旧二进制配新ACK格式。

## Wire精确化的责任和先后

上述语义现已冻结；不假称尚未编码的JSON字段已由两端验证。UR-02第一实施里程碑：提交 session请求/独立session响应、WS认证握手、代际绑定、HTTP ACK扩展的**精确字段和脱敏JSON fixture**，连同既有fence可复用证据，发送给主控与Knuth。新增字段保持身份可验证，不从body信任权限。

UR-01可立即实施配置校验、宿主生命周期、依赖闭包和适配注入边界；wire部分收到上述fixture再实施，禁止两端各猜一套。Turing可立即实施认证/投递边界与测试。发现契约冲突发具体差异，暂停冲突切片而非整个任务。主控维护后续wire附录。

## 源码归属

UR-01获准其调查回报中的精确客户端文件：codex-ws-agent下agent-client.mjs/chat-runtime.mjs/managed-host.mjs/registration-ack.mjs/report-outbox.mjs/workspace-file-bridge.mjs/skill-install-manager.mjs/package.json/package-lock.json；Runtime下agent-runtime.mjs、lib/manifest.mjs/runtime-client.mjs/security.mjs及新runtime-host.mjs/execution-adapter.mjs、manifest.example.json/runtime.env.example/package.json/install.sh/validate.sh/systemd模板；shell中两个现有客户端安装入口和顶层Runtime systemd模板；调查所列Owner单测文件。不包含现有模型执行器、workspace锁或ACK离线迁移工具，新增必要文件先报精确路径。

UR-02获准调查所列Runtime Controller/Security/Service/DTO、AgentServiceImpl、WS Interceptor/WebSocketConfig/AgentWebSocketHandler/ActiveAgentController及对应Owner测试；新session DTO和新握手测试属于本次合同必需，创建时回报完整路径。schema/mapper另行协调。

UR-03不修改上述源码/Owner单测；只读维护跨端验收建议并在交付后执行已授权、隔离、低成本测试。新增测试fixture待第三Writer槽释放后再明确独立路径。

## 跟进与验收

- 回报用实际状态：已接单、实施中、待具体依赖、已提交、已云验、已发布、已实测，不能互相替代。
- 每个Owner在开始实施、精确wire就绪、发生阻塞、源码交付时回报；不要求无变化刷屏。主控每次接续先核验状态，接到阶段结果即给下一步，不让已完成调查停在无人接续。
- 当前没有成功创建的周期自动化，不声称半小时定时巡检已生效。
- 三Agent真实业务、在线重启/撤销/网络注入须明确目标与恢复边界；离线fixture不能充当线上实测证据。共享服务动态身份与在途任务核对是切换门禁，不阻塞离线开发。

## Wire r1接续及精确增补（2026-10-08，阶段回报核实后）

主控已核实UR-01到ad7f47fb、UR-02到87c894dc阶段提交，均非全任务完成。此前没有及时转达fixture和确认范围，现解除这两个实施阻塞。

- 唯一当前wire fixture为API commit `87c894dc297145ee2da338107727087ac74e81b1` 中 `agent/jia-agent-service/src/test/resources/ur02/unified-runtime-wire-v1.redacted.json`。替代82aed54的首次ACK版本预测说明。session使用安装Bearer；WS/native/HTTP命令ACK使用安装派生AgentRuntime会话凭据和fixture定义的五个X-Agent证明头。不得把敏感响应写入InstallationView或日志。
- ACK请求deliveryVersion为最后已确认值，首次null，不预测CAS；响应必须为匹配状态的ADVANCED/PRIOR和合法单调版本；凭据/会话证明在发送时绑定当前代际，不写入不可变业务checkpoint。既有业务来源/租约检查不能因换会话略过。
- 注册readyCommandTypes只能来自真实adapter支持的既有命令类型；空列表不可接令。不修改chat profiles.EXECUTE固定不可用语义。durableStateHealthy下降立即撤销就绪，但允许合法既有终态补报。
- UR-02增补源码授权（不是生产DDL授权）：agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentRuntimeEntity.java；agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/AgentRuntimeDao.java、dao/impl/AgentRuntimeDaoImpl.java、mapper/AgentRuntimeMapper.java；agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql；agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSessionFenceSchemaInitializer.java；上述新增类的对应schema/mapper测试。只增runtime_installation_id/runtime_host_id/runtime_instance_id/runtime_session_generation四个nullable列，不重写业务键、不清数据。空归属执行not-ready；同安装同host可受控轮换代际，另一host/安装拒绝无授权抢占。锁序installation→完整scope runtime→D06，事务/租约原要求保留。初始化器源码不得通过开发/测试连接生产执行DDL。
- UR-02增补D06 service/impl/AgentCommandAckServiceImpl.java及对应AgentCommandAckServiceImplTest.java：保留已STARTED证据下的过期终态补报及所有主体、来源、租约、锁验证。不得放开已过期命令的新执行。
- 若正式Flow确遇既有default-test编译债，允许仅在agent/jia-agent-service/build.gradle和chat/jia-chat-service/build.gradle增补UR Owner独立测试源集；先给具体失败证据，不预先隔离或跳过相关回归，不改生产依赖。
- UR-01追加conf/cyf-agent-runtime-v1/README.md文档同步。现有checkpoint适配若需新增精确文件，请在实施前明确路径，主控及时确认。
- 三个Agent停止意味着本阶段结束，不等于全任务验收。UR-01/02恢复实施，UR-03准备跨端fixture（下一里程碑才转测试Writer）。

## M3b接续范围（2026-10-08）

已读UR01交接e4379147及UR02 c92ba1b2/outbox。没有独立Reviewer或逐阶段人工审批：Owner自检继续，主控只协调真实路径冲突和契约分歧，不将每个小阶段设为review等待。

- UR01追加4个native模块及实际对应测试：conf/codex-ws-agent/{conversation-native,conversation-controlled-image,conversation-controlled-image-v3,typed-inspection-runtime}.mjs；test/{conversation-native,controlled-image-http-runtime,controlled-image-v3-runtime,typed-inspection-runtime}.test.mjs。仅做安装派生会话格式、proof传输边界及原功能回归，不新增模型能力。原任务内终态确认后清理、取消与重连闭环继续。UR03 a383efac候选可由Knuth合入其客户端worktree并在新tree自检，不复用旧tree证据作新证据。
- UR02追加原申请native控制器PersonalWorkspaceRuntimeFileController/PersonalWorkspaceConversationRuntimeController/AgentTaskContextPackController/AgentWorkItemReassignmentController（agent服务api包）、AgentInspectionInputController（chat服务api包）及对应测试；将fence验证纳入已有业务提交事务，不持DB锁等待外部模型/网络，不改变原ACL和任务归属。
- UR02追加skill包SkillInstallDispatchService/SkillInstallResultService/SkillMarketplaceService，api/SkillPackageController，config/SkillPackageSecurityConfiguration，agent-api的service/AgentManagedSessionLookup及对应测试。必须迁移精确调用点，不允许保留旧API-key旁路或把安装ID伪装apiKeyId。
- UR02同时负责economy SkillDeliveryBindingEntity、EconomySkillApplicationMapper、EconomySkillApplicationSchemaInitializer和对应定向测试的最小安装归属迁移设计/源码。约束：商品技能installation与Runtime installation区分命名；保留tenant/client/canonicalAgentId、escrowVersion、任务/付费ACL及不可变业务绑定；当前sessionGeneration只是可轮换传输证明，不能每次重连重写历史不可变绑定。旧api_key_id/registration_hash仅历史审计，不能继续授权；历史记录只有存在可验证唯一映射时才允许显式迁移，不能凭角色名回填或自动重投/重新扣费。新记录使用明确Runtime安装归属而非旧字段假身份。若不能唯一迁移需保留记录并阻止该项交付，标明待人工映射，不清业务数据。此为源码/隔离测试授权，非生产DDL/扣费/撤销授权。Owner先给精确新增字段及回填可证明性，不得擅自选不可逆策略。
- UR02第一接续输出为command.dispatch精确合成fixture（包括canonical身份、payloadReference、既有lease/source上下文，取自真实canonical codec，不手写猜字段），直接交Knuth和主控。若canonical codec确实缺合同要求字段，立即给精确差异，协调同一wire修正而非客户端默默补造。
- Owner工作范围内必要调用点/测试同步可继续，不因每个同模块文件都等审批；新增跨组件/数据契约仍须报告具体差异并继续其他不冲突切片。不得因此增加产品功能或广泛重写。

## Canonical dispatch投影 r2（2026-10-08）

经主控读取真实E05 fixture，采用既有canonical业务wire，不新增或伪造payloadReference/Runtime installation字段。

- 原始command.dispatch保持tenantId/clientId/targetAgentId精确匹配可信manifest完整主体。canonicalAgentId是ACK的规范化字段，值只能在该匹配成功后取可信manifest；不是从body另选身份。Runtime installation/host/boot/generation始终来自当前认证transport，不从业务frame的installationId取值。
- SKILL_INSTALL原始installationId仅为商品安装，原样保留业务payload，不参与Runtime授权；其他业务字段、source/reference/binding/reassignment/lease保持真实codec原语义。lease沿既有接口获取，不补造leaseToken。
- 原始expiresAt使用安全整数epoch毫秒；校验合法范围后投影为ACK现有ISO字符串。保留原值于immutable业务上下文/指纹，不因为投影而改变原消息字节。过期只限制新执行，已STARTED终态补报不受其阻断。
- ACK payloadReference设为可空（真实wire不存在则null），不生成虚构引用。权限与D06命令关联由已有持久message/command/task/workItem及主体/来源/lease验证承担，不用该空字段代替来源证明。不能因其为空跳过现有真实payload.context验证。
- 服务端Owner更新独立wire fixture与DTO注释/投影测试，客户端Owner更新投影和负例，同一真实codec fixture必须能够进入持久接收与ACK，错主体/商品安装混淆/非法时间必须拒绝。测试使用冻结假时钟，旧epoch fixture不得靠修改生产expiry绕过。
- 原始帧fingerprint与ACK投影一致性分别验证，重复ID不同payload仍拒绝。nullable workItemId沿原DTO/codec，不强造空字符串工作键。
- 同意此前economy三稳定归属字段方案，仅新记录源码与历史fail-closed：旧记录保留审计/escrow，不自动映射、重扣或重投。生产schema/历史迁移仍未授权执行。

## TASK最后源码接续及时间范围裁决

UR02追加AgentTaskArtifactService.java、AgentTaskCollaborationServiceImpl.java及对应Owner/RealTransaction/prepare-fence测试，内部opaque prepared publication拆分既有storage与row事务，不改外部业务wire/DDL。原ACL/version/source/lease/幂等必须在最后短fence事务复验。不得持Runtime fence调用外部storage。
r2合法时间为安全整数epoch且Date可表示范围，不额外设positive格式门槛；0/负值仍不得作为当前新工作执行，已STARTED历史终态按既有D06补报证据处理。

## 旧provisioning源码收敛（仅源码，非线上退役）

主控核实旧入口仍在install.sh、shell/sh_list.txt、bin/codex_ws_agent.sh以及systemd/codex-ws-agent.service和systemd/codex-ws-agent@.service。UR01追加上述精确路径及skills/codex-ws-agent-install/SKILL.md、conf/codex-ws-agent/install-candidate/INSTALL-CANDIDATE.md和必要注册/安装测试归属，收敛到统一Runtime安装入口。不得整文件回退其他安装修复，不能把旧名字alias继续指向旧认证执行实现。共享只读引擎模块不等于旧认证服务入口，可保留有用的底层代码。

这不授权删除、停用或重启任何已部署服务；线上动态身份、任务、凭据及状态迁移仍由精确版本发布/维护核对控制。不得将源码入口删除视为线上旧服务已退役。

## 安装profile指南收敛增补（2026-10-08 14:30）

UR01原Owner Knuth追加精确文档路径`skills/install-profile/SKILL.md`：移除旧codex-ws-agent入口/OPENCLAW_API_KEY推荐，采用当前统一Runtime安装来源与会话契约，保留无关安装说明。仅源码文档同步，不新增功能或线上操作，不是新任务或阻塞其他自检。

## 失效旧认证测试任务清理（2026-10-08 14:33）

UR02原Owner Turing追加精确路径`chat/jia-chat-service/build.gradle`，仅收敛仍引用已删除ApiKeyHandshakeInterceptorManagedOnboardingTest/ManagedRefundTest的managedHostingHandshake旧source-set/task及旧key说明；如存在实际调用方须报告并转为同一最新Runtime安装授权合同。不可通过此项跳过default/chatDeliberation或相关回归，不改生产依赖或恢复旧认证。此为源码清理非新版云验已通过。

## E05特定执行闭环实测前缺口（2026-10-08 14:45）

Curie只读链路证据`/var/tmp/ur03-task-closure-readonly-20261008.md`确认：普通TASK已有Codex/workspace/report适配，不能将普通任务强制改成reassignment。仅bindingVersion=e05-reassignment-v1的重派WORK_ITEM_EXECUTE缺客户端lease/start/heartbeat及可调用的既有结果commit入口。D06 ACK不等于业务成果提交。此为原办事闭环接线，不增加用户功能/命令。

UR01原Owner在agent-client.mjs与lib/runtime-client.mjs内继续原E05最小适配准备和前置拒绝负例；native path仅允许精确已存在的reassignment lease[/start|/heartbeat]形状，同origin/当前session proof/actorAgentId精确manifest主体。不得全放行/agent/**或猜结果URL，不得凭Codex版本可用就无lease执行E05。普通命令不能一刀切禁用。contextVersion与expectedWorkItemVersion的来源/版本转换须由真实服务端receipt及DTO先证明；leaseToken不写普通checkpoint/日志/ACK。

UR02先核实既有ResultCommitService调用入口及prepared storage/短fence事务、lease/version锁顺序。确无Controller/WS调用时给最小内部接线方案及精确JSON，复用既有DTO/service/业务语义，主控冻结后两端实现；不擅自发明外部契约或持fence访问storage。调查和缺口切片不阻塞当前7chat失败修复或已授权入口收敛。现有E05 fixture/分立单测不是串联HTTP/DB跨端实测证据，结果闭环仍NOT_RUN。

## UR03真实HTTP持久化fixture授权（2026-10-08 14:56）

Curie恢复原Agent并转第三Writer，独立API worktree `/home/isp/wsps/worktrees/ur03-runtime-http-db-20261008`，branch `codex/ur03-runtime-http-db-20261008`，基线5ec39870。独占五个新增路径（模块前缀agent/jia-agent-service/src/ur03RuntimeHttp）：`java/cn/jia/agent/acceptance/Ur03RuntimeHttpDbAcceptanceTest.java`、`java/cn/jia/agent/acceptance/Ur03RuntimeHttpFixture.java`、`resources/ur03/runtime-http-db-h2.sql`、`resources/ur03/runtime-v1-http-client.mjs`、`ur03-runtime-http.init.gradle`。不修改Owner源码/build.gradle/既有测试，init只云端显式新sourceSet和测试级依赖。实际Node默认fetch→localhost Tomcat/Spring→生产filter/controller/service/MyBatis/D06→私有H2文件，双JavaJVM串行重启/代际轮换/ACK ADVANCED PRIOR/独立JDBC rollback证明。主控准备paired固定源码SHA/Node20.20.2并走Flow，无本机Gradle。合成ACTIVE安装起步，不证明enroll/E05/WS/MySQL/Provider或线上三Agent业务；无数据库输入env，无继承宿主凭据，密钥仅私有管道，不上传DB/private state。

## Enrollment真实wire对齐（2026-10-08 14:57）

Curie发现当前client.enroll读取顶层installationId，而Java现行AgentRuntimeV1EnrollmentResult为 `{installation: InstallationView, runtimeAuthorization}`。采用现行Java嵌套合同唯一格式，不保留顶层兼容。UR01原Owner同步真实response字段/完整manifest主体与安装状态验证、authorization私有原子保存及Owner负例；UR02原Owner给实际record/Controller序列化fixture证明并同步已有wire fixture（如必要）。API已经消耗一次性enrollment secret后客户端解析失败不得盲重试一次性secret或假成功；保留恢复-required事实。此为既有安装契约修复，无新功能/生产enroll/凭据撤销授权；UR03此次从ACTIVE合成安装起步不等待此slice也不假称enroll通过。

## E05内部结果与恢复wire冻结（2026-10-08 14:58）

采用Turing `/var/tmp/ur02-e05-task-wiring-handoff-20261008.md` 最小接线，属于既有E05办事流程修复，不新增产品命令/功能。UR02所列5源码路径、2新Owner测试及既有相关测试、`e05-runtime-lease-result.redacted.json`归原Owner；必要精确DTO/service增补只承担内部接线，不改既有对外DTO字段或schema。精确路径：

- POST `/internal/agent/tasks/{taskId}/work-items/{workItemId}/reassignments/{reassignmentId}/commands/{commandId}/result-commit`；body仅既有AgentWorkItemResultCommitDTO，producer/path workItem与认证完整主体/原E05 receipt严格一致。200 raw AgentWorkItemResultCommitViewDTO（非JsonResult），status=submitted，仅真实业务事务commit或可唯一证明的原commit结果可返回；重放返回原version/submittedAt/artifact，不改事件/行/扣费或造新artifact。
- GET 同result-commit路径：当前Runtime完整主体原command/receipt的只读原结果回读，无query/body或caller actor选择。200同原View；只有receipt+exact workItem resultArtifact+artifact version/hash/producer+确定性WORK_ITEM_SUBMITTED event可唯一证明原命令结果时返回，否则明确404未找到或409恢复歧义。客户端还须与已持久原结果material/body校验，不把404/409/D06 ACK当成功或允许自动重跑。该GET使进程重启无需把旧leaseToken写checkpoint恢复原结果。
- GET `/internal/agent/tasks/{taskId}/work-items/{workItemId}/reassignments/{reassignmentId}/commands/{commandId}/lease`：只读原receipt/command及当前精确活跃lease，200 raw AgentWorkItemReassignmentLeaseDTO（含当前已持久workItemVersion），不改lease或版本；用于read/start/heartbeat响应丢失后的可证读回。必须确认同原receipt/current assignee/token fence/active binding/session，无宽泛版本探测/放宽旧POST expectedVersion。不可证明当前原lease返回404/409，不能猜版本、自动重新claim或重执未知业务。现有3个POST lease路径/query/body保持不变。

共同HTTP约束：仅AgentRuntime current-session/five proof，不JWT/API-key fallback；同origin精确method/path许可，Cache-Control private,no-store，禁止URL秘密。400 BAD_REQUEST；主体/producer/query非法403 WORK_ITEM_RESULT_FORBIDDEN；隐藏目标404 WORK_ITEM_RESULT_NOT_FOUND（lease用现有WORK_ITEM_REASSIGNMENT_NOT_FOUND）；真实版本/lease/source冲突409 WORK_ITEM_RESULT_STALE；不可唯一恢复409 WORK_ITEM_RESULT_RECOVERY_REQUIRED；真实运行依赖不可用503 WORK_ITEM_RESULT_UNAVAILABLE。当前filter更早401/403/503沿其既有AGENT_RUNTIME_UNAUTHENTICATED代码；客户端不得把503当撤销。HTTP结果真实反映commit；不自造kind=PRIOR替代业务receipt。

实现必须复用原任务根/身份/member/receipt/lease/source/CAS/event语义：短fence预检→释放锁→opaque preparePublication（NEVER、无外部I/O持锁）→当前session安装/runtime/task-root原锁序下全部重新验证→publishPrepared+原lease CAS/submitted/event同事务。prepared object不得上wire；材料保留供恢复，不能单靠DTO/fingerprint猜提交。读回/重放证明缺少持久predicate时先报告精确缺口，不擅改生产DDL；该项保持fail-closed而非降低唯一证明。Owner先提供真实序列化脱敏fixture/精确字段类型与错误回执给两端，然后Knuth复用原执行器闭合E05 lease/成果/恢复链路。schema/生产数据/在途执行/付费/停机均未扩权。


## E05同模块精确调用点与UR03 source transport（2026-10-08 15:20）

UR02 AgentWorkItemReassignmentService.java同模块接口精确路径已纳入原Owner范围：复用receipt/source/当前lease读回，不注入Impl绕代理、不复制业务ACL，暂无生产DDL授权。772c1c9的已有event_json allowlisted唯一成果proof不得存原lease/session秘密。新wire给Knuth实际发送成功，不继续等待主控冻结。

UR03只云端显式测试源集。paired client为固定commit72a4abf/tree10136645的两个模块runtime-client.mjs/security.mjs，主控用git-show非秘密archive运入Flow；客户端根带ur03-client-source.json {format:ur03-git-archive-v1,commit,tree,files:{精确模块路径:sha256}}。Flow先硬校验archive和manifest SHA/精确成员/常规文件才解包，fixture核commit==输入、完整tree、实际模块hash及目录归属。API仍真实git HEAD/tree/clean证明。不得伪造.git或称archive做过checkout diff，不增加秘密env/SCM访问，也不是产品旧契约兼容。四个UR03非敏感env及五文件归属不变。


## UR01云端clean-target安装验收接续（2026-10-08 16:03）

原Owner Knuth 已resume且send_input实际成功01a11a88-11a9-7c22-967f-6c2910a09ce0。新增唯一独占路径 `conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs`；独立显式opt-in云端harness，不加入默认*.test或新增skip掩盖未实测。真实Node20.20.2/npm/Python在全新私有canonical target执行原install/npmci/venv/pip/stage发布/final validate/import原engine/ws/yauzl；target解释器health并真实create/validate/reopen PNG/JPEG/PDF/DOCX/XLSX/PPTX。记录prefix/base_prefix/stdlib/distributions/pyvenv.cfg/shebang搬迁证据；不虚称stdlib已全部artifact内闭包。主控从固定完整git源码制作显式payload archive和云端前置，不改活动Run130配置。禁止本机真实npm/pip/install/Gradle、服务/enroll/Provider/生产state、无证据资源/性能硬门禁；本机仅syntax/static。先回报精确env/receipt/archive清单，云端实际失败才将原install/validate/execution-adapter的精确必要修复另纳入原Owner，不预改Pythonpin或双轨版本。原E05d8源码集成不等于此验收或部署。


## UR04完整E05独立验收源码授权（2026-10-08 18:16）

原UR03仅session/HTTP ACK/持久fence重启链；不得用它替代完整E05。主控将已有只读设计/var/tmp/ur04-e05-http-acceptance-next-20261008.md中的六独立新文件实际授权给原Knuth/critical_worker，继续同UR04任务，不重复派单、不创建Reviewer。唯一Writer在新独立API worktree `/home/isp/wsps/worktrees/ur04-e05-http-20261008`，分支`codex/ur04-e05-http-20261008`，固定API基线4c5875b5bed143c793d7812143d60deab8d65674/tree81e9275b46d07648cfa925de1b822fdeffa370ec。该任务与Curie当前UR03原两文件诊断路径无重叠，因此不等待其启动根因收敛才实施。

唯一owned根 `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/`，限下列六文件：
- java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java
- java/cn/jia/agent/acceptance/ur04/Ur04E05HttpFixture.java
- resources/ur04/e05-http-db-h2.sql
- resources/ur04/e05-runtime-http-client.mjs
- resources/ur04/nonpaid-execution-child.mjs
- ur04-e05-http.init.gradle

不改UR03五文件、生产源码、build.gradle、客户端生产/test文件或根控制文档；真实源码缺陷回原Owner。采用上述完整设计的真实Spring/安全filter/native localhost WS/真实handler注册、原Runtime与engine/executor及lease/result/D06、真实MyBatis/H2-file/事务/独立JDBC/独立JVM和Node重启，保留六正负故障selector。禁止Supplier/DAO/mock权限和`bind(...,()->true)`、HTTP fake server、造result/D06成功、只重建JS对象冒充重启、Provider/收费/生产请求。受控非付费OS子进程必须明示synthetic，既不能冒称实际模型，也不能省略原workspace/spawn/output/result链。

固定client输入更新为修复payload3746043947888a6b727be88527695d1edf3587c3/treeddc3c0b3355eb77cd0be080f8fc4b734c901cab7/285文件/tarSHA55ffef55075cf802a1a090114c5a3be6dd933dc8925b80d3403f9404e5fe9781，而非将新源伪称d8。完整干净artifact须由Flow产生并固定来源/摘要；当前Run138尚未通过，不能由源码archive替代完整安装闭包。程序允许在云端输入已证明匹配后测试，不本机Gradle/真实npm/pip/安装，不操作Flow/生产。主控负责immutable来源、云端配置与正式验证。未运行部分保留NOT_RUN；enroll/MySQL/旧状态迁移/实际模型/线上三Agent/版本发布仍单独验收，不因本fixture省掉原要求。若client新云缺陷到达先安全交回Knuth原Owner，主控协调本任务路径/Owner状态，不覆盖未提交fixture。

## Run138真实安装失败最小归因与Owner接续（2026-10-08 19:31）

UR04原Knuth六个新增文件已提交34d9e2d6c5b9915c8bb259d14a4761d2ff782e89/tree8d625893abd35fbadb1a9cf40e271c59660c1b4a、remote一致、WT clean，源码阶段转awaiting_cloud_fixture且释放Owner。不是Java编译/真实链路已过。主控将同原Agent实际send接回UR01，ledger已claim；不得同时声明两个源码任务Owner。

Run138完整压缩诊断JSON SHA7793c53272f1ef3427e64cac740a20737b52f5bbc8c67797cbd132fcdd1bb710及58dependency log内容摘要核验。C1/C2 PASS，C3因final venv launcher残留已删除stage引用FAIL（helper health.ok=true不替代搬迁），C4 PPTX create/validate后重开原instruction断言FAIL；其余五格式实测PASS。PPTX底层原因尚未知，先区分fixture与原producer，不猜依赖版本。原rawlog more=false但outputTruncated=true，不能声称原日志全部取得。

原UR01 Owner仅最小既有install.sh/validate.sh/clean-target-install.acceptance.mjs与必要原Owner测试；若原helper确证相关生产源码缺陷，追加唯一精确源路径conf/codex-ws-agent/toolchain/delivery_tool.py与其目录既有相关测试。新增文件先报路径再确认。完整六格式语义验证、最终stage零引用/CLI及原C1-C4断言不放宽、不skip/pinrollback或恢复旧入口。不本机真实安装/npm/pip/Gradle、Flow或生产操作。修改payload与harness采用独立commit防自引用；主控负责下一固定来源候选与云验。Run138独占云root已清理，仅留回执日志，仍无持久完整Runtime制品，不冒称可直接用于UR04或已部署。

## UR01同Run干净制品消费测试钩子冻结（2026-10-08 19:48）

原Knuth Run138缺陷修复已交付payload7594fd72251d38b6e1d23a1a3cca184ae0d085e7/tree0827ce904179862ab55648fe99b780cea94faf98/285/tar3594240/f4dcd014e409b5a0e32f7419cd9500bf1f3e0022492f533736b366cd325f0106，独立harness13aaec39c0567c049fad63d99b0a32d3e7af237c/tree107b2b9544012201588d7290b3c3eca860443732/SHA789a1fe56086a5172407ea8fce07da8bedfb7188636ec2bbdf7aa4e1540e75ae。主控核完整archive/所有memberblob/mode/PAX/log及候选YAML/shell；新C1-C4仍NOT_RUN，等139实际终态恢复后独立r4云验，不覆盖活动Run。

主控接受Owner报告/tmp/ur01-clean138-fix-handoff-20261008.md的内部consumer设计并追加唯一测试源码范围：原conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs与原runtime-host.test.mjs。仍同UR01原Owner、独立原WT；不修改生产install/validate、runtime/engine/lib、API/UR04六文件或rootdocs。实施`acceptance(env = process.env, { consumeArtifact } = {})`，仅显式函数参数，不从env加载代码/执行任意命令或保留默认root。callback类型先于副作用核验；最多调用一次；原C1-C4全部真PASS与fixed SOURCE最终tree/archive readback、canonical target身份和localNode blob再次核对后、finally前执行。未达到四门通过或callback缺省不得消费，原清理与四检查结果不变。

冻结的deeply frozen allowlisted projection：`{format:'ur01-accepted-clean-target-v1',cloudRun,target,nodeBin,nodeSha256,source:{commit,tree,files,archiveSha256,finalReadbackTree},harnessSha256,checks:{C1:'PASS',C2:'PASS',C3:'PASS',C4:'PASS'},acceptedSnapshotSha256}`。snapshot hash是explicit ordered JSON（不含该hash自身），不是finally后的receipt文件hash。无秘密、env、宿主配置、业务状态或任意错误对象。target为callback期间借用，禁止延后后台消费/保留/复制/mv/rebase。callback只允许独立明确成功/失败回执，错误/不完整结果必须让overall lane FAIL，同时保持真实C1-C4原PASS，consumer结果独立；不得将callback原exception消息/秘密放receipt。finally始终先核专属root inode/归属再清理，包括consumer失败。原installedpayload成员不得被consumer悄改，必要完整性复验沿已有hash，不发明硬资源/性能门槛。

新增必要低成本测试覆盖类型拒绝、allchecks未过零调用、snapshot冻结/摘要与秘密缺席、最多一次/await完成再cleanup、consumer抛错或错误结果overallFAIL且四门保持原PASS、默认调用行为不变。测试仅源码片段/私有合成文件，不在本机真实install/npm/pip/venv/Gradle/Java或生产运行。新的hook commit仍以payload7594固定SOURCE，独立harness防自引用；主控负责新harnesshash/Flow候选，不把该hook单测视为实际制品消费或E05通过。UR04 SOURCEpin从374更新到7594是其下一原Owner checkpoint，不在本slice同时实施。

## 项目交付规则调整与 Run139 终态接续（2026-10-08 20:08）

用户已明确规则只适用于CYF项目，前端继续Flow，后端正式测试/构建/部署改为本地固定源码输入；Codex全局/服务器级/共享技能改动已撤回。具体以项目AGENTS.md和docs/aliyun-flow-cicd-strategy.md为准。既有冻结条款中Java后端“仅云端/不本机Gradle”执行地点由此次明确授权替代，不能据此恢复脏源码发布或生产目录构建；所有Gradle仍由主控经orchestrator串行，并保持fixedcommit/tree/selector/fixture证据。本文客户端clean-target仅Node/Python安装验收仍沿已有独占云端范围，非Java后端构建或发布，不自动扩大为主机真实npm/pip/安装授权。生产操作、切流、在途/动态身份维护授权边界未变。

Run139已终态FAIL并恢复原配置readback：固定APIeac15d/tree07223，341reports/3070tests/1failure/0errors/101skipped，RealTx16全过；真实UR03 child main已进入，唯一失败为BOOT_MYBATIS_SPRING的UnsatisfiedDependencyException，根NoSuchBeanDefinitionException/bean=runtimes，具体缺失类型仍需证据。诊断压缩SHA499efe8763779f26654859a416bd8349b0f14c446e52c7ff385d3d9defca00d6全核验；rawlog被截断，不称完整原日志。无制品/部署，不能将回归绿灯当HTTP启动成功。

Curie原UR06只读seam报告已真正完成并checkpoint于evidence/unified-agent-runtime-20261008/ur06-source-seams，实测执行0，enroll/MySQL仍NOT_RUN。释放support后转回原UR03唯一Writer，原独立WT和两Java路径不变：先证明缺失bean类型及真实注入链，只修原fixture实际接线/必要安全诊断，保留真实MyBatis/DAO/auth/事务和全部原用例，不mock、不放宽、不猜删依赖。源码交付后主控在固定新commit本地正式复验；不重跑同输入139。Knuth仍UR01消费钩子唯一Writer，交付前不重复分配UR04 Owner。全部原UR05/06迁移、真实三Agent业务与文档收尾目标未缩小。

### UR03 本地正式验证入口的必要最小适配（2026-10-08 20:11）

主控实读发现原 `agent/jia-agent-service/src/ur03RuntimeHttp/ur03-runtime-http.init.gradle` 仍硬要求 `CYF_FLOW_GRADLE_ACTIVE=1` 并抛 `UR03_FLOW_ONLY_NOT_RUN_LOCALLY`。不能伪造Flow身份绕过新项目本地规则。将该唯一原fixture init路径追加给原UR03 Curie Writer：移除旧“只云端”地点门禁，改为明确本地fixture opt-in `UR03_LOCAL_ACCEPTANCE=1`；保留四既有pairedsource输入白名单、sourceSet含依赖、settings/include-build绑定、真实socket/双JVM/精确断言、maxParallelForks=1及禁用跨pairedsource cache。不得给默认test挂fixture、改production/build.gradle/cold-init或增加第二兼容入口。主控只经orchestrator在固定新commit上正式运行，Owner仍不自行执行Gradle。其余源码范围仍原两Java，实际新safe诊断字段如需先报告。

### UR04 新来源与本地后端入口接续（2026-10-08 20:17）

Knuth原UR01消费钩子20742bc1848fdb8ecfb8c90af753ec7f4917bcf7/tree da3a31a5e489213134a6f02bd2e83e3104855e6a的两既有测试路径与日志/hash/remote/clean已readback，Owner54static/9selectedPASS；实际新payload C1-C4/consumer/E05仍NOT_RUN。源码阶段checkpoint后释放UR01，原Knuth仅接回UR04六既有独占文件，不同时拥有两任务。

本次仅原六文件来源/地点和同类真实fixture接线修复：CLIENT/SOURCE与全部commit/tree/count/archive绑定由374更新为7594fd72251d38b6e1d23a1a3cca184ae0d085e7/tree0827ce904179862ab55648fe99b780cea94faf98/285/3594240/f4dcd014e409b5a0e32f7419cd9500bf1f3e0022492f533736b366cd325f0106；不同时接受双来源。原UR04 init的Flow-only gate改为唯一明确本地fixture opt-in `UR04_LOCAL_ACCEPTANCE=1`，保留五非敏感输入白名单/真实WS-E05/六原selector/no-cache/sourceSet。检查原fixture中真实DAO继承@Inject的mapper依赖，显式提供实际SqlSessionTemplate代理bean而非手工赋值后绕Spring；只修此文件的真实接线，不改生产/权限/其余Owner路径。

完整artifact仍必须来源真实四C全PASS与全成员/Node/toolchain来源证明，不允许因为改成本地就捏造manifest、cloudRun或用源码代替安装闭包。本checkpoint只做源码/低成本自检、不运行本机安装/Gradle/云写/生产，不复制或保留待清理artifact。后端本地正式验证如何同批消费客户端完整fixture由主控继续明确执行与来源契约；该缺口不能由本checkpoint冒称已验收。来源修复后仍保留原真实enroll/MySQL/状态迁移/真实模型/三Agent上线/旧服务退役完整目标。

## 本地后端同批完整 Runtime fixture 消费合同（2026-10-08 20:32）

用户指定后端本地正式验证后，Java不得继续云端正式构建，也不能用假cloudRun借用旧云端钩子。正式本地后端跨端验收需要在同主机消费真实完整安装fixture；这是同一测试批次独占私有根中的依赖fixture，不是客户端生产安装或发布，不写宿主全局packages/现有服务/config/state/生产目录，不enroll生产身份、不Provider/付费，不扩大原生产维护和切流授权。主控负责执行；原Owner仅实现源码/低成本自检。

先将原Knuth接回UR01原两个既有测试路径（clean-target-install.acceptance.mjs与runtime-host.test.mjs），不接UR04同时Owner，不改生产installer/validator/pins/helper/runtime或API。固定payload仍7594/0827/285/3594240/f4dcd；harness独立新commit防自引用。将该backend-fixture lane改为唯一最新真实本地输入：必需env `CYF_CLEAN_INSTALL_BUILD_ID` 取代旧CLOUD_RUN，不接双轨输入；保留原显式opt-in `CYF_CLEAN_INSTALL=1`及所有来源/工具/路径校验，safe错误名不伪称CLOUD。root receipt format为 `ur01-clean-target-local-fixture-v1`，记录buildId及localBackendFixtureOnly=true，不含cloudRun/cloudOnlyOptIn或虚构Flow身份。工具origin允许明确的 `local-host:`、`fixed-input:` 及原无凭据公开HTTPS来源，拒绝旧flow-input前缀；不得复制环境或凭据到receipt。

单次await/四门真实PASS/原Source与完整artifact前后readback/目标inode/Nodeblob/严格六格式语义/独占finally清理全部保持。回调快照按显式顺序为 `{format:'ur01-accepted-local-target-v1',buildId,target,nodeBin,nodeSha256,source:{commit,tree,files,archiveSha256,finalReadbackTree},harnessSha256,checks:{C1:'PASS',C2:'PASS',C3:'PASS',C4:'PASS'},acceptedSnapshotSha256}`；deepfreeze与hash不含自身算法不变。callback成功与失败schema、safe code枚举及四C独立结果不变，不允许默认消费/保留/复制/mv/rebase artifact或未await后台子进程。更新原低成本测试覆盖新字段/旧输入拒绝、快照顺序摘要、源/工具/目录守卫、清理、callback一次和失败归因；不自己执行真实安装/Gradle。

主控callback在四C实际PASS后、原finally前建立唯一受控 `ur04-clean-artifact.json`（原hook唯一允许新增manifest），只从实际全成员/内部symlink inventory和frozen快照生成，cleanRun字段真实取本地buildId，不伪造四C或工具证明。UR04完整源码证明用同7594 archive在**另一个固定source输入目录**准备，不修改harness被最终tree readback保护的sourceRoot，也不复制安装artifact。真实E05六selector及之后真实enroll/MySQL在同canonical target生命周期内经orchestrator串行完成，所有Java/Node/DB owned子进程须已停止/await后才能callback返回；细分安全证据留在目标外。本callback严格不得启动生产、实际模型或借宿主npm/sitepackages替代fixture闭包。

UR03真实本地d6209a7/tree766c617已终态PASS：19tests/0fail/0error/0skip，包括真实HTTP/Spring/MyBatis/H2双JVM/代际与ACK、两诊断和RealTx16，validateLayeringPASS。不是全回归、完整E05、真enroll/MySQL、版本制品/三Agent线上验收通过。全部原最终要求继续保留，Goal仍active。

## UR06 真实 enroll / MySQL fixture 源码实施接续（2026-10-08 20:36）

Curie原只读seam报告已checkpoint，不重复只读调查。原服务端Owner Turing接UR06此独立源码阶段，基线fcac494a5103a7bc1175c96e9df50d2fcc35c182/tree6a21c9e61539268d20514db8f80c02f8ce23b043，新WT `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008`；唯一owned根 `agent/jia-agent-service/src/ur06EnrollMysql/`，仅报告已有四建议路径：java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java、java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java、resources/ur06/enroll-mysql-client.mjs、ur06-enroll-mysql.init.gradle。若确需其他路径先报告，不修改UR03/UR04/production/defaulttests/build.gradle/client/rootdocs。

本阶段按 `/var/tmp/ur06-enroll-mysql-acceptance-seams-20261008.md` 实现真实E1-E5、M1-M3：原service创建PENDING/原enroll一次性secret CAS消耗和nested响应/原客户端defaultfetch与未知结果不自动重放/真实session与native WS ready/原auth DAO及D06/Java A-B重启后独立JDBC durability/旧代际或撤销拒绝和sibling隔离。真实MySQL 8.0.21（只读已核本机binary版本）私有新datadir/schema，原MySQL DDL/真实initializers及重复执行和四nullable fence列/engine/collation/hash/unique/CHECK/真实行锁事务；不使用H2、小表替代MySQL或Supplier/mock DAO/权限。真实完整E05 M4仍是本任务最终验收的一部分；本source阶段暂不重复UR04六例，实现前置E1-E5/M1-M3不等于M4或UR06整体完成，保留后续真实MySQL E05与三Agent线上/文档要求。

使用与UR04同7594固定全源码及真实完整四C已通过的同canonical artifact，主控只在20:32 callback lifecycle内正式运行；源码archive不冒充安装artifact。fixture opt-in `UR06_LOCAL_ACCEPTANCE=1`，非敏感输入白名单至少API_COMMIT、CLIENT_ROOT、CLIENT_COMMIT、NODE_BIN、ARTIFACT_ROOT、MYSQLD_BIN（UR06_前缀）；源码/工具/制品readback必须精确，缺输入失败而不是skip。现阶段Owner只源码/低成本自检、精确提交/推送/readback，不自己Gradle/安装/启动MySQL/云写或生产。

私有MySQL bootstrap/停止是测试fixture代码，主控后续执行前核验：`--no-defaults`在首位、不读生产my.cnf，唯一新datadir/socket/pidfile/日志在owned私有根；仅loopback、非3306/33060端口；每次数据写入前核真实server version/port/datadir，进程与inode精确归属。不能用localhost生产3306/既有datadir/服务，不能stop未知进程/借生产schema。合成凭据仅私有pipe与内存，不能argv/env/日志/report，不给其他Agent；Node和Java子进程环境白名单，无生产datasource/Flow/Provider secrets。重启只owned API JVM；整个批次结束await精确owned Node/Java/MySQL再清理私有根，不按年龄判定失败或强杀未知进程。不新增无依据资源/大小/性能硬门禁。

## UR04 真实编译缺陷修复的消费前固定新输入（2026-10-08T21:18:31+08:00）

主控已核原Owner2314单fixture路径、remote/clean/hash及原六selector全部不变。旧fcac真实编译2error/0test已归因保留，不改写失败、不重复旧输入。将2314集成到另一个干净WT /home/isp/wsps/worktrees/ur04-compilefix-consumer-integration-20261008，固定commit dba2eadafe9c815a49d94b73cdbce29ce4423b10 / tree c279c78f01cb067b1406b99a5bbe516cc4177e3c；先经orchestrator实际新编译，再实际完整六E05。正在运行的原C1-C4仍仅测试固定7594安装源码及原工具，未进入consumer；其sourceRoot/target/harness/archive全部不改。Java消费方独立固定consumer-preparation.json仅在消费前选择此次新API，保留最初preparation.json/失败证据；不是把旧结果重标新commit或绕过原四C。callback只在原四C真PASS及全readback后await实际新源码测试，缺陷仍FAIL，所有owned子进程退出后finally删除独占target，不复制/保留/搬迁artifact。无生产、Provider或维护授权扩大。

## UR05 后端本地同批制品 producer 源码切片（2026-10-08T21:26:48+08:00）

Curie只读报告已实际完成，26文件snapshot均主控readback匹配，报告checkpoint在evidence/unified-agent-runtime-20261008/ur05-source-seams；安装事务/schema/producer缺口未通过验收。主控仅追加只读metadata核实历史backups是指向/home/isp/baks/flow-api的root软链接，实体root:root0700；未迁移记录/备份，已安装五脚本与source SHA不同仍不推断实现等价。原Knuth已交UR04单文件2314，集成dba2/treec279实际编译EXIT0/validateLayeringPASS、0tests，UR04回到主控verifier；可接UR05非重叠源码，不同时拥有两任务。

UR05本阶段独立root worktree /home/isp/wsps/worktrees/ur05-local-backend-package-20261008，base 2690fbbf040017083c6783a3cc65ce2eb631e136 / tree 5ca30834e19b11ddb457f3231546175e83bf1e55，已由主控固定最新项目规则而非Codex全局规则。仅三个新增路径：ops/ci/aliyun-flow/auto/package-api-local.py、ops/ci/aliyun-flow/local-release-metadata.init.gradle、ops/ci/aliyun-flow/tests/test_api_local_package.py。Owner只源码/stdlib私有合成单测、syntax、精确commit/push/hash/readback；不Gradle/bootJar/npm/pip/实际安装/MySQL/Flow/生产，不修改既有helper或API/Web/client/defaulttests及rootdocs/ledger。其它必要路径先报告。此阶段不是本地安装入口已完成；后续root admission/统一事务/schema来源和断点恢复、维护授权/切流/三Agent真实业务仍全部必须完成。

唯一local producer不调用package-api.py的Flow main、不假BUILD_NUMBER/CYF_FLOW身份、不接受Flow receipt作为本地证明。CLI显式固定source-root、commit/tree、version、build-id、build-root、evidence、output；source canonical clean前后检查，external build root/unique output/noaliases。绑定真实同批Gradle command/input/exit/log SHA、required tests XML摘要与selector/fixture、validateLayering与fresh bootJar实际路径/摘要及固定依赖provenance；仅cached tests不能冒称本批bootJar产生，JSON自报/仅干净checkout不能认证外来JAR。精确schema/证据字段由Owner首先给出实际可校验输入方案供主控冻结，不能无证据填PASS或虚构执行。保留实际mail runtime、公有制品安全与原OpenCV pin/digest，不新增无依据大小/性能门禁、Provider或secret输出。

新唯一local release receipt/metadata/sidecar/source identity绑定version/buildId/commit/tree/JAR/provenance，schema不得伪装旧Flow numericRun；包仍精确五payload，包自身摘要保留外部避免自引用。root admission稍后独立消费并认证package/receipt/JAR/证据，不以producer JSON+checksum自动获准生产。新增init只在主控固定干净API输入的真实bootJar构建期写公开CYF-Release-Version/CYF-Source-Commit/CYF-Source-Tree/CYF-Local-Build-Id（保留真实module Implementation-Version，不重写/后改已构建JAR）。绑定API settingsRoot，不作用included-build/Test/其他task，不导入秘密；声明release metadata输入摘要进build证据。Owner先核真实BootJar manifest及现行任务接口，缺实际来源字段须报告，不猜API。没有实际构建/真实证据时producer必须失败而非成功/skip。

单测仅私有temp root、合成Boot ZIP/日志/证据用于证明parser/边界/篡改/原子导出，必须明确不是实际构建或发布。覆盖missing/failed/stale/foreign evidence、dirty/wrong commit/tree、JAR/version/build-id/provenance/mail/security mismatch、aliases/unsafe outputs/重复输出/自引用摘要、假Flow混入及secret-bearing字段；不得把这些unitfixture当C1-C4/E05/真MySQL/生产证据。完整安装/恢复/schema接线在后续同UR05原Owner阶段冻结，不复制第二套事务状态机、不恢复pull/build/restart脚本。


## UR06 实际源码前置问题：原 UR02 Owner 接续（2026-10-08 21:41）

主控核收 Turing 的 UR06 四文件 commit732558494ee082413f8f8e30ad448cc3c6fb7bbc/tree95e5409268f9aaee871c3e6d812c3ad61722fbc7，remote/clean/hash 均匹配，Owner源码阶段已释放；主控独立集成 db0c1628cea6f13123eca5fbcb55914b4834062b/treeeecf145b2d2a2a482a43594a996a7d7ad371e671 的真实 compileUr06EnrollMysqlJava/validateLayering 正在经串行编排执行，七例及M4未验收。

实读原完整schema hosted有 chk_hosted_single_tenant，但原AgentSchemaInitializer的CREATE和严格expectedChecks仅三项，确定源码契约冲突。另原ACK拒绝类型AgentCommandAckRejectedException不在RuntimeController的ExceptionHandler列表，403边界静态缺口，未伪报运行HTTP500。原UR02唯一Writer Turing接续独立WT /home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008，base db0c/eecf；仅以下四既有路径可写：
- agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java
- agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentSchemaInitializerTest.java
- agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentRuntimeV1Controller.java
- agent/jia-agent-service/src/test/java/cn/jia/agent/api/AgentRuntimeV1ControllerTest.java

统一最新唯一契约：保留完整baseline单tenant约束，将initializer新建DDL及严格四CHECK集合与原schema一致，仍拒绝missing/extra/wrong-expression，不接受三CHECK旧兼容、不删约束、不改fixture缩表或绕初始化。仅源码变更，不对生产执行DDL。Runtime ACK原拒绝异常以原Controller安全403/no-store/通用响应处理，不能泄露reason、body、token，保持400与其他权限边界及D06原事务校验。Owner在原测试补精确正反回归，源码/static/push/clean交付，不自行Gradle/MySQL/安装/生产/付费。无mock测试可替代主控实际MySQL/HTTP验收；失败后只回同Owner精确修复，不新增Reviewer。


### UR05 producer 字段冻结（2026-10-08 21:45）

主控实读原Owner第一方案 /var/tmp/ur05-producer-checkpoint-20261008.md，SHA256 a64dc74f0072f26c518febf3bef864dec1747f9c4a39e64e9fb1583a5a87b2a8；原字节checkpoint于evidence/unified-agent-runtime-20261008/ur05-producer-contract。冻结其local-build-evidence-v1、local-bootjar-proof-v1、release-receipt-v1、application-metadata-v1/sidecar-v1、external package-v1和CLI完整字段；同批源码/真实freshBootJar/原publicArtifactVerifier/日志+XML/依赖来源/五payload/无Flow身份/无包自引用/保留真实Implementation-Version均不变。tests列表由主控实际任务范围决定并绑定精确selector/fixture，非空并保留starter publicArtifactVerifierTest/poiProductionRuntimeClasspathTest；producer只检查一致性不能认证builder或扩大生产授权。原Owner仅原三个新文件自检、commit/push/readback和交接，不实际Gradle/包构建/安装。根准入、完整原安装事务/schema/恢复/动态维护授权、整体正式回归和三Agent实测继续列入完整UR05后续，30个private fixture unit通过不能替代这些步骤。


## UR01 Python 安装归因及全局默认源接续（2026-10-08 22:03）

Curie只读报告实际完成，checkpoint在evidence/unified-agent-runtime-20261008/install-pip-diagnosis-20261008T2142。已证同PID固定fd下载Pillow49368411字节约16KB/s观察片段，无compiler children；完整Pillow已由主控读全字节SHA匹配官方声明 b8e2f83c56e141920c39464b852de3719dfbfb6e3c99a2d8da0edf4fb33176ed，随后转reportlab下载。慢下载已证，具体链路限速原因和源码编译不兼容未证；旧pins无cp311 wheels属元数据事实，不等于安装失败，不因此重启/杀进程或借宿主包。候选Pillow10.4/reportlab3.6.13仅metadata建议，未冻结/实施/验收，保留现有pins与完整依赖验收。

用户已纠正为本机全局pip默认源（不是项目专用配置，不升级Python）：侧聊已授权写/etc/pip.conf root0644 SHA ff94b7680551d9774340869e51c11347b5e0588423d76ca033d16ab21fdc7f27，root用户pip配置对应 cb86e7b3a90485abb9eed649e8cc20d4c32ef8845969e34a7c53ff3bf11fef00。主控只读实核；项目源env已由原侧聊精确删除，主控刚新增而未提交的项目source-reader/8unit测试也保存前字节后撤回，不再引用删除配置。主控actual pip install option parser(isolated=True)/空HOME/显式无PIP环境继承解析到HTTPS清华源，无extra-index/trusted-host；未来新批次显式CYF_CLEAN_INSTALL_PIP_INDEX_URL映射及配置SHA准备结果在evidence/unified-agent-runtime-20261008/global-pip-source-handoff/next-batch-explicit-input.json，准备脚本/var/tmp/prepare-next-runtime-global-pip-input-20261008.py不安装包。必须在下一NEW批次重读全局默认、固定URL/configSHA到该批prep/env白名单，不能把这份准备结果宣称已启动新安装。

当前same83600/ur04-local-20261008T205238仍固定旧pypi.org输入；主控实读686606进程env PIP_INDEX_URL=https://pypi.org/simple、PIP_CONFIG_FILE=/dev/null，全局配置变更不能重标其来源或提前PASS。无生产/解释器/pip升级/服务控制授权扩大。


### UR05 原Owner接续 root admission 源码切片（2026-10-08 22:05）

主控核收producer最终ba88d4ed7c635ad4c916d6a9eb2aec97933d6ae3/tree36c1e64447f0b24cf9a43b90e6207c5162e4bc66，三路径hash/remote/clean/33privateunit log均匹配；不是实际包/构建/安装成功。原Knuth已释放producer再接同UR05后续，在原独立rootWT baseba88继续，仅允许新增ops/ci/aliyun-flow/auto/admit-api-local.py、ops/ci/aliyun-flow/tests/test_api_local_admission.py、ops/ci/aliyun-flow/host/cyf-api-local-admit；先回明确trusted-input/CLI/admitted-output字段与原唯一安装事务/schema接点，主控冻结后范围内实现与privateunit。不得修改旧5脚本/producer/实际主机文件、实际构建、安装或生产。

root admission必须从root控制的显式可信批次输入认证package/source/version/buildId/tree/receipt/JAR/provenance/evidence绑定，不以producer JSON+checksum认证builder/扩大生产授权，不fakeFlowRun。不创建第二套发布事务/锁/lifecycle、不兼容旧Runtime协议或pull/build/restart。只准入字节+输出原共享installer未来所需的明确typedlocal输入，不能在本阶段执行完整安装或宣称切流；原installer/schema适配、恢复与动态维护身份/在途检查仍需接续。已安装五helper与source hash差异仍UNKNOWN，不把源码fixture通过报成已安装实现验收。对全局pip源只采用新批次显式输入，不改same83600。


### UR01 原安装真实终态失败后的唯一Owner修复（2026-10-08 22:08）

session83600实际EXIT1，receipt endedAt2026-10-08T14:02:46.491Z（22:02:46+08:00），主控22:06收终态；C1原install失败，C2-C4 NOT_RUN、consumer calls0、六E05 NOT_RUN。所有stdout/stderr与receipt逐SHA核验，证据evidence/unified-agent-runtime-20261008/ur01-install-final-failure；exclusive root正常finally removed，未发布target/保留制品。原stderr明确Pillow8.4 setup RequiredDependencyException:jpeg缺headers/library；这次已证构建依赖失败，不说成未经证实的Python3.11内在不兼容。更换index不能单独修此错误；不盲重跑旧输入/补宿主包/安装系统libjpeg/compiler。

原Knuth暂停刚开始的UR05 rootadmission proposal，Producerba88保留，UR05 Owner已释放而非完成；同原clientWT /home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008，base f3d39592d3991032246fa400ec6095241c39e1df/tree269e4a80bb92875d4cb96bb01b6d6cb060683f1e接UR01源码修复。仅四既有路径可写：conf/codex-ws-agent/toolchain/requirements.txt、conf/cyf-agent-runtime-v1/README.md、conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs、conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs。

冻结最小候选pins Pillow10.4.0/reportlab3.6.13（Curie原JSON真实cp311/Linux轮子metadata/hash），保留其余四直接pins、完整sixdeps及实际PNG/JPEG/PDF/DOCX/XLSX/PPTX create/reopen、执行链路与所有隔离/来源/C1-C4/callback/finally语义。先第一payload commit只更新requirements及必要当前Python3.11.13验收目标说明，不声称未执行的ABI/API通过；不改pip<22/bootstrap/Node/Provider/生产，不全局only-binary错误排除pure-python docx。第一commit后读取准确tree/files/rawgitarchiveBytes/SHA/PAX完整285blobmode，第二harness commit在原两个test路径把唯一SOURCE(commit/tree/count)和archive摘要断言绑定第一payload。payload和harness不可同一自引用snapshot，不同时接受旧7594双契约、不降低完整校验，不把harness新commit当payload。

原Ownersource/static+相关Node低成本fixtureunit自检、两个commit/push/readback交付，不能自己实际安装/pip/Gradle/生产。主控随后新独占批次全局镜像defaults实际parse并显式映射URL/configSHA，再执行完整真实C1-C4+同target await6E05及真MySQL7/M4后续；API旧硬编码source证明须由原各Owner精确同步后才消费，不伪造旧结果。全局pip配置、原失败source/log和清理事实不重标。

### UR01 新依赖源码核收与 UR02 正式复验接续（2026-10-08 22:25）

UR01 原Knuth交付两个独立commit：payload A d91ebbf436911eac20ffb70cb92192a65c742e11/tree b2e3f17ff57e21e2482c0fc54e71dbf4b92dbd82（两pin及README），harness B 2533381cc79e79d124d8c8630914790f48d3619e/tree739f25ca5e7759ab427a7694d9cc55dc51d46732（原两个test文件、唯一绑定A）。主控独立git archive3624960bytes/SHA3c826b9e78db3bc4ca5a9eef1e9026ebeb0e34626e214a6b1b2d8bd532169b36、PAX/全285blobmode、四文件/Owner日志摘要/remote MATCH/WTclean实核。Owner14Node scopedpass/0fail/42selector excluded是低成本源码证据，不是56全测试或新install/C1-C4/六E05/真MySQL。证据evidence/unified-agent-runtime-20261008/ur01-cp311-source-readback；实际新批次尚未启动，需原API Owner先精确同步UR04/UR06 paired source proofs。旧失败批次不重标。Knuth源码阶段释放，原UR05 ba88原WT rootadmission proposal恢复，仍仅3newpaths、不改原5host脚本/实际主机/构建/生产；精确trustedinput/CLI/output字段须先交主控冻结。

UR02 9966f4a6817ef322e82bdcc1379cb5810e943ba8/tree0091449092568c3486cb7a2cf0b96a33270dfcc9新独立WT实际session96963 EXIT1：原56tests54PASS/2FAIL/0error/0skip（Controller8PASS、Initializer46PASS2FAIL），compileUr06EnrollMysqlJava PASS、validateLayering因test失败NOT_RUN、sourceclean。证据evidence/unified-agent-runtime-20261008/ur02-corrected-prereqs-local-result。13旧失败已消退到2个新暴露归因，但未宣称整体通过：原test tableDefinition在quoted COMMENT分号处误截断导致四CHECK空集合；另原完整identity baseline systemtenant NULL与initializer最新tenant0有真实DDL漂移。原Turing原两路径接续，修quoted SQL语句抽取不降低oracle/负例；identity先查最新strictvalidator/migration/统一tenant合同，需额外canonicalbaseline路径先报告冻结，不能盲回退latest或忽略约束。全部原48+8方法保留；不重跑相同输入、无Reviewer/生产。原M4只读计划由Curie继续，原WriterTuring完成本切片后接续，不重复派单。

### UR02 剩余identity baseline最小范围冻结（2026-10-08 22:30）

主控实读原Owner /var/tmp/ur02-identity-canonicalbaseline-minimal-proposal-20261008.md，实核现行single-tenant-role-isolation与initializer CREATE/validateIdentityChecks一致：所有身份tenant=0，SYSTEM仅client/owner为NULL，不回退SYSTEM tenant=NULL。允许原Turing原WT base9966在已授权原test路径外，仅追加agent/jia-agent-mapper/src/main/resources/db/schema.sql三行：registry tenant注释、SYSTEM scope tenant='0'谓词、alias tenant注释，精确与initializer一致；其余字段/CHECK/FK/触发器和权限均不改。原initializer/Controller保持9966字节；原56方法保留，SQL helper识别quoted COMMENT内分号与转义/注释而不删parity/assertions。源码静态自检与任务branch push/readback后由主控新输入完整56+compileUR06/layering，不将static作为PASS。

更宽agent-identity-schema.sql原CREATE/ALTER/owner-tenant升级规则仍有旧契约漂移，只读发现单列待收敛，不假称本三行已经统一完整migration。当前不授权执行migration/生产DDL或任意扩大源码；后续原Owner独立精确范围接续，保留最新唯一契约。真实freshMySQL完整baseline/严格初始化及整体实测依然待验收。

### UR04/UR06 最新payload来源证明同步切片（2026-10-08 22:36）

原Turing UR02 64d445a6a76fbe4a7f527fe914bdce6b5c6105da/treec0e486cb63f7293682a4400bfd41fa39bf363bee sourcehandoff已主控核收，新的完整56+compileUR06/layering正式复验session65727在独立fixedWT进行。原Writer释放后在另一独立WT base64d接UR04 pairedproof同步。实读hardcodes不仅两Node SOURCE对象，还有两Java CLIENT及UR04 tree期望，故本次唯一允许四原路径：
- agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs
- agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java
- agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs
- agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java
仅来源commit/tree/archiveSHA/bytes常量与Java对应CLIENT/tree期望同步到payloadA d91ebbf/b2e3/285/3624960/SHA3c826b9e；不把harnessB当payload，不双来源兼容、不改变完整校验/权限/原6E05与7enroll断言、不增加业务实现。源码/static/nodecheck/独立commit/push/readback由原Owner完成，实际Gradle/安装/真业务由主控固定输入。Curie M4只读计划无写入交叠；源码同步不等于M4实现或实际结果。

### UR05 root admission精确接口冻结（2026-10-08 22:36）

主控核收原Knuth精确提案/var/tmp/ur05-root-admission-checkpoint-20261008.json SHAe775649622b22f0161322bab1436095aa9113016affc5e361774dddc08b1f3ec及MD SHA200b0a82b0c7c8b789eed02641290d000e11dcefb7bc20815eed086a61fcd6ae；完整字节/冻结回执在evidence/unified-agent-runtime-20261008/ur05-root-admission-contract。冻结其trusted-record-v1、independent batch-authority-v1/controller-verification-v1、CLI/固定wrapperroots与helper、admitted-input-v1/外部stdout摘要/allowlistedfailure及exact5payload/evidence closure字段。仅独立root保护的主控实际观测凭据认证batch，producer JSON/hash证明一致性不能认证执行/授权生产；不存在实际观测则拒绝，不自行造PASS。固定source身份、原日志/XML/selector/fixture/实际freshBootJar/publicVerifier/manifest/mail/OpenCV证据不可省略。

原Owner原ba88WT仅新增admit-api-local.py、test_api_local_admission.py、cyf-api-local-admit三文件，范围内继续实现/private synthetic unit/commit/push/readback，无独立Reviewer或额外逐步审批。实际host/root目录/installedhelper/install/Gradle/生产全不操作。稳定FD/保护owner-mode-ancestry/singlelink/无alias、exactstrictJSON/五member/无自引用、recheck/fsync/atomic-no-overwrite及精确stage cleanup保持提案；不第二事务/锁/lifecycle、不fakeFlowRun、不将Artifact-only admission变成维护/schema/部署授权。原唯一installer/两schema/恢复/动态维护与在途检查接点仍待后续准确适配，source与installed五helper差异仍UNKNOWN，privateunit不冒称旧installer已验收。

### UR06 M4原四路径实现冻结与主控新批次（2026-10-08 22:47）

Curie只读报告完成：JSON SHA4ce0d09e1c7b46bd3f64b01fe2e32f65c438f6a93ad05b2d5e2fc00ebe5ac18e、MD SHA95fcf68e8e0747b6b268fd1d640b2ecd83da6827dc36f5fadeec10c55a55ac99，29源码引用主控全部readback一致，checkpoint ur06-m4-source-plan。报告旧时点96963RUNNING/来源待核状态由主控真实后来事实替代，不改Owner原字节：64d/c0e新session65727 EXIT0全部56PASS0fail/error/skip、compileUR06/layeringPASS；A/B/285archive3624960/SHA3c826已核；UR04最新pairedsource b125d70c79471be0fc9f306cc0f2e9cd85890ee4/tree4b875b456573f65865096fb34be7b25544897e46已核exact4file仅来源literal、remote/clean。

原Turing UR04源码阶段释放后，原UR06唯一Writer在新独立WT baseb125实施M4，仅四既有test-only路径：Ur06EnrollMysqlAcceptanceTest.java、Ur06EnrollMysqlFixture.java、resources/ur06/enroll-mysql-client.mjs、ur06-enroll-mysql.init.gradle（均在agent/jia-agent-service/src/ur06EnrollMysql）。冻结原报告四路径方案、完整原六E05所有多lane/正负/持久/再启动断言，不替换为心跳/native404/原M3子集。复用原ownedMySQL/guardedDataSource、真实Spring/Tomcat/auth/MyBatis/DAO/result/D06/事务，完整agent+user baseline/account security/四原initializer；freshM4接续整份原E05 SQL再整份ownerPhaseA DDL同guardedconnection，避免缺reassignment表/owner列，不抄H2DDL/缩schema或改constraint，不执行obsolete owner-as-tenant A02迁移。M4三subject隔离、真实HTTP丢响应/opaque prepared boundary、genuineMySQL失败trigger+透明观察、独立JDBC、Java+Node双重启同DB/state不reseed；保留原七foundation/真enroll方法，M4只合成ACTIVE不冒称enroll/Rabbitpublish/JWT创建reassignment/生产迁移已验收。原tracked nonpaid-child仅hash/read/copy/shebang到ownedroot，不新增child或业务实现；无真实Provider。

同UR06 sourceSet新增ur06M4MysqlE05精确六方法task，原ur06EnrollMysql明确保持七foundation，不defaulttest或隐式skip；原7非秘密env/onefork/noncache/真实classpath/settingsroot与ownedcleanup不变。架构检查使用真实根任务validateLayering（不沿报告未验证的agent子模块同名task）。来源统一最新A/B角色，不引旧7594兼容。Owner仅源码/static/低成本检查/commit/push/readback，主控固定candidate先实际compile再未来NEW同acceptedtarget单awaitedcallback串行七基础+六M4。不得修改主控当前批次/复制借用target或把sourceplan视为结果。

主控新批次ur04-cp311-local-20261008T222833已真实启动session13826（22:45），完整C1-C4/六format与一个awaited原六HTTP/H2 E05 callback，来源A/harnessB/pairedAPIb125/全局pip实际parser显式HTTPS URL+configSHA固定。新批次当前未终态、未证PASS；与旧83600FAIL区分，仍无生产/系统包/Python升级/服务操作。此批是H2六E05，不假称真MySQL七/M4已执行。完整MySQL及更宽正式回归/包/唯一installer/切流/真实三Agent/退役/图文仍待后续。

### UR01 全局源实际生效及新pyvenv.cfg缺陷归因/最小修复（2026-10-08 22:56）

新batchur04-cp311-local-20261008T222833/session13826已真实EXIT1，endedAt22:46:07+08；原install步骤22.277秒。实际stdout两次Looking in indexes及所有包下载URL均为固定HTTPS清华，pip在私有venv中successfully installed全部9依赖，含Pillow10.4/reportlab3.6.13 wheels，不再发生旧JPEG sourcebuild。此证明来源与包安装阶段事实，不等于包摘要/ABI/六format验收；不把wheel和源变化共同结果单归镜像、不承诺稳定速度。

新失败发生在预发布validate.sh：VENV_STALE_STAGE_LAUNCHER_OR_ACTIVATION；C1FAIL、C2-C4/consumer/六E05NOT_RUN，target未发布/独占root正常清理。日志/receipt全部SHA核验在ur01-cp311-install-final-failure，旧7594失败不重标。主控额外以现有3.11纯stdlib --copies --without-pip私有临时venv、原payloadA relocator/validator真实复现：pyvenv.cfg新增command审计字段含stage路径，原relocator只改bin脚本/activation未处理cfg；严格validator首先查cfg并拒绝。证据ur01-py311-venv-config-diagnosis，无包下载/安装/宿主包借用/系统升级，诊断root已清理。原失败cfg被合法清理未读回，不能把新probe字节冒称旧cfg原字节。

两批输入/两不同根因矩阵two-input-root-cause-matrix.json已按orchestrator authorize-remediation释放累计2失败gate，只允许原Owner源码修复，不盲重跑任何安装。原Knuth暂停UR05自己三新文件WIP并保留精确checkpoint，再原clientWT baseB253338/739f，ONLYinstall.sh、原runtime-host.test.mjs及clean-target-install.acceptance.mjs三路径。第一payloadC仅install.sh已识别currentPython3.11 cfg command provenance改为最终venv审计路径，保留home/base executable/include-system-site-packages=false/原完整字段，不删cfg/command、不generic剔除stage marker、不放松validate.sh、未知stale仍拒绝；原launcher/RECORD/长路径/quote/隔离及pins10.4/3.6.13等保持。第二harnessD两个test路径加currentcfg正负回归且唯一SOURCE/archive摘要绑定C，285/fullblobmode/PAX/tree/rawarchiveSHA读取，不自引用/双来源，不把D当payload。Owner仅static/现有低成本Node/privatefixture自检/两个commit/push/remote/clean，不pip/完整install/Gradle/MySQL/生产。主控随后原API Owner精确更新最新C来源，再NEW完整C1-C4/六format/同target单awaited消费者；本批target不保留。

Turing原UR06 M4四路径独立源码接续不取消，但新payloadC证明必须待核收后同步；不得继续将A artifact当已接受或自行改未知来源。原UR05 sourceWIP暂停不是取消/完成，不派第二Writer、不覆盖，修完UR01后原Knuth恢复。生产、所有旧服务和凭据未改，无新的生产或global Python/pip版本操作授权。


## 生产实测后的原 Owner 源码接续（2026-10-09 S01）

用户切换为真实生产验收，不再启动新隔离安装/Java/MySQL验收。task432原需求与指派保留。主控已核收 `/var/tmp/ur01-production-single-runtime-plan-20261009.{json,md}` 并核对22个固定源码blob SHA；生产未发布候选。

原UR01源码授权内，Knuth继续同worktree `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008`，base commit `c8be411be9819e6139628ac3cd12f040eeb171d9` / tree `324128ac043d1a7db5d1140b04b0482073f648c4`。唯一修改范围为 `conf/cyf-agent-runtime-v1/agent-runtime.mjs` 和既有 `conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs`。修复CLI给现行`loadWorkspacePolicies(env)`传路径字符串导致空Map的接线错误，以显式env-shaped file对象调用；不得继承宿主inline策略或建立兼容/第二入口，保留绝对路径/no-symlink/内容校验及正常默认行为。使用无网络/无模型/无服务/无真实安装的定向源码单测，证明显式CLI文件、CYF文件环境输入、CLI优先级、非法路径/内容拒绝、无配置行为，旧输入复现/新输入修复。不要为可测性改engine或loader；如必须超出两文件先报精确原因。

本slice允许原Owner连续实现、自检、提交干净唯一新候选；不允许npm/pip安装、Gradle/build、新隔离验收、生产配置/enroll/session/数据库/outbox修改、服务动作或发布。不要改API/harness的配对pin或宣称新候选已部署；源码交付后由主控接续唯一配对，不将既有E整制品证据归新字节。原UR05的059已实现producer/admission/published verifier不重复实现；剩余唯一安装事务接点另冻结。

原Turing只读接续UR04，核三主体identity/installation/持久host fence及三个旧服务全部scope/inflight；仅白名单投影，未知保留UNKNOWN，不清fence、不读取/输出凭据、不停进程、不重发432。该只读核查并非生产切流或转移授权。


## UR05 原唯一事务源码接续：先保留对齐（2026-10-09）

主控核收 `/var/tmp/ur05-shared-local-installer-contract-20261009.{json,md}`（JSON fc764e44dedd15b88929e7224f82aa609e3d7af8ff76cac4728677421265fcdb；MD 293d28cc5257c8d2c74d5c5f34d9ae3c3c22c4ff9635c6a06c66f536c837ea43），读过唯一事务、typed接口、恢复与差异保留设计，并实核20份literal文件SHA。原Knuth在新独立WT `/home/isp/wsps/worktrees/ur05-shared-local-installer-20261009` / branch `codex/ur05-shared-local-installer-20261009` 从05951ae7b467c1464f4906ae6c44e86f77926325/tree197d18f80308bbee868a1ea3f54f90b20c0c4889接续，先完成源码保留对齐，不直接实施未冻结的生产授权字段/动作。

唯一允许相对源码为：ops/ci/aliyun-flow/host/cyf-api-flow-deploy、cyf-api-flow-install、cyf-api-additive-schema、cyf-api-e05-additive-schema；对应tests/test_api_flow_deploy.py、test_api_e05_flow_deploy.py、test_api_gate_policy.py、test_api_flow_install_lock.py、test_api_canonical_path.py、test_api_additive_schema.py、test_api_e05_additive_schema.py（全在ops/ci/aliyun-flow）。四helpers合并已核root版本回执/诊断与installed最新安全修复，逐hunk保留备份严格alias、tar路径/重复/报告只读、forward-only恢复、当前SQLowner/catalog；最后E05 runner bytes与parent pin准确配对，不放宽摘要。kit不在可写范围，生产最小方案pin复用现行installed字节；producer/admission/verifier/orchestrator和实际rootdirty/installed均不改。保存原四helper三方SHA/每hunk归属、原测试/oracle，不能整文件旧版覆盖。

允许低成本既有source-unit/static/diff-check/独立commit与任务分支push/readback；无真实Java/DB/服务/npm/pip/clean安装、无新隔离业务验收、无配置/DB/outbox/进程或生产写入。测试合成文件/假lifecycle结果不是生产验收，不借历史PASS归新字节。新增文件/超11路径先报。此为原项目修复的离线源码范围确认，不新增安装/维护许可。

LOCAL完整接线仍按原唯一状态机/锁，不建第二installer或伪Flow；但其SchemaPlan precondition精确清单暂未冻结：Turing最新审计已经发现D06五表均缺、hosted-profile必需CHECK缺、CHAT migration存在DDL/DML条件，不能只用四nullable fence/两CREATE资源代表完整启动副作用。原Owner完成对齐后保留干净可追溯checkpoint并报告；主控收到最终审计后再冻结同批schema preconditions/authority引用及LOCAL接线，阶段结束不等于发布/总体完成。


## 生产前源码收口与 LOCAL 接线冻结（2026-10-09 11:30）

范围：Main已核 UR04 最小方案 JSON `7cab0207f29ad690c96736f89089489d07afd44bf698e5b58e6964a715de1287` 的126个固定源码摘要、11次只读查询和API24cb干净基线；UR05 oracle checkpoint7245df/tree750b5已核26文件/3blob，133例132PASS/1FAIL。此节仅冻结原Owner的源码实现，不授予生产写入、发布、服务或队列权限，不把历史查询冒作当前生产就绪。用户要求直接生产验收，不再开新clean-install/Java/MySQL隔离验收；轻量源码自检不当生产验收。

### API 原Owner Turing：六路径

新WT `/home/isp/wsps/worktrees/ur04-production-schema-contract-20261009`，branch `codex/ur04-production-schema-contract-20261009`，base24cb046e58424c1d999940b518ca0d1d96e34f59/tree1492e399eb717bc7d9bb809bab1dc3416d9b7dfa。仅以下六既有路径，按原最小方案逐hunk：

- `agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java`
- `agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql`
- `agent/jia-agent-mapper/src/test/java/cn/jia/agent/schema/AgentIdentitySchemaTest.java`
- `agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentSchemaInitializerTest.java`
- `agent/jia-agent-mapper/src/main/resources/db/agent-work-item-reassignment-e05.sql`
- `agent/jia-agent-mapper/src/test/java/cn/jia/agent/dao/AgentWorkItemReassignmentMapperContractTest.java`

binding唯一最终CHECK为chk_agent_binding_single_tenant/tenant_id='0'、VARCHAR50 NOT NULL DEFAULT0；initializer严格核name/clause/enforced/nullability/default，拒绝旧名、双CHECK、弱谓词或nullable，不自动归一数据。hosted原四CHECK严格校验保持。E05 canonical CREATE补owner_jiacn NOT NULL及有序mandatory ownerindex；保留原scope/unique/lease/arithmetic/CAS，旧表不凭CREATE自动变更。原5+48+4方法/负例保持，必要正fixture和源码parity随真实合同同步，不skip或放宽。资源新字节/hash先回Main及Knuth，未编译部分真实NOT_RUN。

### UR05 原Owner Knuth：原11路径的唯一状态机接线

沿用WT `/home/isp/wsps/worktrees/ur05-shared-local-installer-20261009`、branch同名、base7245df47bce3205da44cf10ae3861ca00a8e0519/tree750b5fbf7b0be5e564971e3636baf4f88a9c2841。仅原四helper与七test（原方案minimalFutureSourceScope列出的11路径）。producer/admission/published verifier/wrapper/orchestrator/kit/root dirty/installed保持不改。actual LOCAL installDecision、maintenance authority、approval/record v3、bindingSHA、原CLI和恢复/锁/来源界面，以 `/var/tmp/ur05-shared-local-installer-contract-20261009.json` 为类型及唯一状态机基线；以下完整schema前置明确替换其旧“只有owner/fence两resource”的提案，不再沿用不完整SchemaPlan。

- `SchemaPlan.format=cyf-api-local-schema-plan-v1`，`entries`仍精确有序[F06,E05]。其runner/resource/sqlSha/expectedCatalogSha须来自最终同批API+helper字节，不能将da1ce旧E05 SQL或旧parent pin归新资源。
- `resourcePreconditions`精确有序十项：identity-baseline、identity-migration、runtime-installation-v1、runtime-session-fence-v1、command-transport-d06、execution-report-d02、owner-phase-a、chat-base、chat-migration-v2、chat-typed-v1。对应schema.sql、agent-identity-schema.sql、agent-runtime-v1-schema.sql、agent-runtime-session-fence-v1.sql、agent-command-transport-schema.sql、agent-execution-report-v1.sql、single-tenant-task-owner-ddl.sql、chat-deliberation-schema.sql、chat-deliberation-v2-migration.sql、chat-typed-deliberation-schema-v1.sql；每项保留原ResourcePrecondition字段并要求`expectedCatalogSha256`及独立`actualSchemaProof`。实际nested resource与该批JAR逐字节匹配，不只git源码/hash匹配。
- SchemaPlan增加必需FileRef：`startupCatalogProof`（实际启用initializer的完整所需catalog及原输入/后置证据）、`effectiveConfiguration`（同批白名单配置输入/来源/precedence/profile/hash）、`applicationPrincipalProof`（该批预期app账户和实际权限来源及启动后真实principal核验安排）、`boundedSchemaReceipt`（同批明确授权的有界schema前置操作及重读；无操作的精确equivalent verification也须真实来源）。类型、来源及binding严核；缺失/UNKNOWN必要合同不伪报成功。这些是前置证明，不新增generic SQL runner。
- 需要的已知生产变更是hosted第四CHECK、binding已知旧契约的原子收紧、四nullable fenceADD、D06五CREATE/两缺失triggerCREATE，共13statement提案。此源码接线不执行这13条、不执行整个identity/owner/CHAT脚本，不能把文本或root文件创建当实际数据库回执。前置由后续独立、明确授权、同批维护动作完成并提供可核证明；partial DDL保留历史并按原同plan recovery处理，不能重启原输入求绿。
- 核全部hosted四CHECK、binding最终契约/原11行无转换、fourfence精确nullable且不reset、D06五表/两immutable trigger、D02/Runtime安装、F06/E05当前owner合同、CHAT base/typed及conversation/thread完整catalog。APPLIED/presence不等于相等；未来active initializer范围按实际同批flags绑定，不把38个源码类全部假设自动启用，也不只核十个资源就泛称所有startup安全。
- 同批配置目标：D06 enabled=true、typed enabled=true、两个CHAT additive migration=false；必须在授权配置切换与完整catalog证明后使用，不改现有生产配置或开启付费/marketplace。当前配置输入true/false与running Spring最终值未知分别记录。pre-start证明是固定可信配置来源/预期principal及当前catalog/权限，启动后另核实际principal/会话/READY；不循环要求尚未启动的新进程提供现成PID。
- admission保持artifact-only/productionAuthorized=false。生产权限只能来自独立维护authority+明确用户授权；inspect只读、不建目录/换incoming/approval/record、不运行Java/kit/service/SQL。缺新权限/构建证据不能签发approved或调用installer。
- 共用原coordinator/installer、唯一incoming/approval/record/实体JAR、原mutex/FD8→FD9和schema hooks；父coordinator不跨子installer持另一FD8自死锁，installer退出后父重取原release锁。不新增第二installer或伪FlowRun。历史真实Flow仅原精确历史诊断/恢复，不是最新LOCAL功能的永久双轨兼容。
- E05四companion路径按UR04新资源最终字节同步embedded SQL/hash、runner-parent pin与原test；旧ownerless负例冻结独立输入，原freshCREATE正例按真实新CREATE得到scope，不伪造SHOW。实际API commit/hash未到则不得猜测；非依赖部分连续推进。

仅源码静态/轻量private unit、commit/taskbranchpush/readback。需新路径或变更producer/kit/控制工具先回Main报告真实必要性，不自行扩框架。正式后端测试/构建按AGENTS经原orchestrator在最终干净固定源码运行；本节不启动其构建或任何生产动作。最终三Agent业务、隔离/恢复/撤销、旧全scope维护与退役、在线版本/成果及文档架构图仍单独未验收。
