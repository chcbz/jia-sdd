# UR05 未完成内容收口详设（2026-10-09）

仅整理未完成开发与未完成交付，不重列已完成实现，不将局部发布回执等同整项UR05/双端业务验收完成。已重读 [AGENTS.md:1–63](/home/isp/wsps/cyf/AGENTS.md#L1)、[README.md:1–37](/home/isp/wsps/cyf/ops/orchestration/README.md#L1)。本文只描述未完成项；已完成安装、13DDL和配置的回执单列于 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/versioned-production-release-readback.json`，不新增Reviewer、框架、协议或旧版兼容。

## 1. 固定来源与状态边界

| 固定组件 | 源码commit | tree / 用途 |
|---|---|---|
| root | `5be8cf501acdf20a7d5fa696017437c0355181e8` | 协调/安装源码基线；本文修改由Main统一提交 |
| API | `1e9111028fbdff1ae5452f64aec843e85e81ad59` | `0416b722d735c58af4653892b6ee269e8f9d1498` |
| Web | `c6ae76010c43153659cc6d55c902a1765c620932` | `f82ac5739135e6e7fe0f2e4f0edbcb17dbb06fa2`，冻结不改 |
| Runtime | `5489c0e946114ec601e246a4eb93a0bff3b57c24` | `66424e5e9063f316869b00c952a3859625ece77f` |

统一候选版本 `1.14.0-consolidated.20261009`。以上为首轮主目录核对的冻结来源记录，不冒称后续root HEAD、远端或全部组件当前线上版本。源码完成、正式验证、制品安装、配置/DDL交付、业务实测分开记录。

- 原文已先备份至 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/UR05_PRODUCTION_CLOSEOUT_DETAILS_20261009.before-unfinished-only-20261009T164319.md`；SHA-256 `df4bb755b9c898a2497e73220155cd85863aad138b7c04b30f6457d9c8f7bab8`。已完成代码inventory保留在备份，不再列为待开发。
- 工作区接续：原UR01/UR03/UR06历史工作区不再需要；后续仅主develop `/home/isp/wsps/cyf/api`、`/home/isp/wsps/cyf/web`、`/home/isp/wsps/chcbz/isp-install` 与保全patch。paid-lease详设已收口，dirty工作区是否删除由Main核完整保全后处理，本Owner不执行清理。
- 决策来源：`/home/isp/baks/cyf-develop-consolidation-20261009T1558/api-integration-decisions.json` 的 `unfinished`、`/home/isp/baks/cyf-develop-consolidation-20261009T1558/web-integration-decisions.json` 的 `unresolved`、`/home/isp/baks/cyf-develop-consolidation-20261009T1558/runtime-integration-decisions.json` 的未适配 `decisions`；另纳入Main刚核实的MQ启动接线缺口。
- **真实缺源码：§2 MQ provision启动接线；§3 paid-lease跨端恢复；§4 F01 Runtime context-pack适配；§5 Workspace File固定结果durable report恢复。** 已实现E05 lease/start/result恢复、原HTTP ACK/auth/fence、最新installer不列为待开发。
- **待交付（Main正在处理，非缺源码）：§6 仅保留完整Runtime目标安装/精确subject切流及当前auth业务恢复阻塞。前后端发布、原13DDL与配置已完成，删除其待交付项。** 配置不能代替§2源码接线，发布完成不能代替业务恢复；auth根因已由原Owner定向定位，见§6.1；不写为单纯等待。

## 2. 未完成开发：MQ canonical provision启动/受控接线

### 2.1 已证缺口；撤回“仅缺配置”结论

| 真实调用链 | 固定源码与行号 | 判定 |
|---|---|---|
| 仅构造独立Rabbit设施 | [AgentRabbitTopologyConfiguration.java:35–58](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyConfiguration.java#L35) | 39设置RabbitAdmin autoStartup=false；50–58创建provisioner Bean，未执行provision |
| Readiness起始/成功来源 | [AgentRabbitTopologyReadiness.java:11–33](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyReadiness.java#L11)、[AgentRabbitTopologyReadiness.java:78–81](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyReadiness.java#L78) | 初始NOT_CHECKED/NONE/NONE；canonical要求READY/PROVISION/CANONICAL_TOPOLOGY |
| 显式canonical声明 | [AgentRabbitTopologyProvisioner.java:32–49](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyProvisioner.java#L32) | exchange→queue→binding全部成功才markProvisioned；失败markFailed并抛脱敏异常 |
| passive存在验证 | [AgentRabbitTopologyProvisioner.java:53–77](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyProvisioner.java#L53) | 不能证明参数/binding，EXISTENCE_CONFIRMED不等于canonical READY |
| Publisher依赖Ready | [AgentConfirmedRabbitPublisherImpl.java:96–106](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentConfirmedRabbitPublisherImpl.java#L96) | 102取snapshot，103要求canonical且manifest/request digest一致，否则TOPOLOGY_NOT_CANONICAL_READY |
| Relay自动启动但不claim | [AgentOutboxRelayScheduler.java:69–79](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentOutboxRelayScheduler.java#L69)、[AgentOutboxRelayScheduler.java:123–127](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentOutboxRelayScheduler.java#L123)、[AgentOutboxRelayScheduler.java:166–174](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentOutboxRelayScheduler.java#L166) | autoStartup=true，phase=MAX_VALUE−100；未canonical则不discover/claim |
| Consumer无provision顺序保证 | [AgentRabbitTopologyConfiguration.java:60–72](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyConfiguration.java#L60)、[AgentCommandRabbitConsumer.java:102–145](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandRabbitConsumer.java#L102) | 本组factory/listener存在，无显式autoStartup=false/provision前置；process先验dispatch scope |

固定API全仓 `src/main/**/*.java` 检索 `AgentRabbitTopologyProvisioner`、`agentRabbitTopologyProvisioner`、`.provision(`：类型/Bean创建以外无生产调用，test中的显式调用不等于生产启动接线。**五开关全true、外部预建队列、broker连通、passiveVerify成功，均不能把本JVM内存Ready变真。** 原publisher/consumer/ACK无需另造，但canonical lifecycle确实缺源码；此前“只缺配置”结论撤回。

Main现场新证据（本Owner未操作broker）：只有vhost `/`、无Agent专用用户；5672实际beam PID7747监听，systemctl inactive不等于broker停止。该输入不能满足 [AgentRabbitSafetyGate.java:133–140](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitSafetyGate.java#L133) 的专用broker/vhost准入；临操作由Main重核实际身份/归属，不据此停broker或借其他主体凭据。

### 2.2 最小待实现方案、初始化顺序与失败行为

1. **一个启动调用方，不恢复自动声明。** 后续原API Owner拟在主目录新增 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyLifecycle.java` 最小专用topology lifecycle（详设拟新增路径，当前不存在），由现有TopologyConfiguration注册、沿原TopologyEnabledCondition生效，仅注入本组named manifest/admin/connectionFactory/readiness/provisioner。Bean构造与OFF/DB_SHADOW零broker副作用，保留admin autoStartup=false/explicitDeclarationsOnly，不替换默认/SMS Rabbit Bean、不新增公网provision接口。
2. **原manifest唯一。** 使用 [AgentRabbitTopologyManifest.java:158–186](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitTopologyManifest.java#L158) 的两exchange、五queue、bindings/TTL/DLX与digest；启动只调用原 `provision()`，不维护第二拓扑清单，不调用purge/delete/全局admin.initialize。
3. **初始化先后。** SafetyGate先验证开关依赖、精确scope/专用broker；相关schema initializer完成DDL/catalog；本组Bean构造完成后，lifecycle在relay和dispatch listener之前执行一次provision。只有 `READY + PROVISION + CANONICAL_TOPOLOGY + 本manifestSha256` 才开放本组消费者/relay。显式设置本组listener autoStartup=false，用原RabbitListenerEndpointRegistry的精确 `AGENT_COMMAND_DISPATCH_V1` ID启动；不能仅靠Bean依赖或ApplicationReadyEvent（容器可能先启动）。relay保留原readiness guard；lifecycle phase/容器启动时点与停机逆序用测试证明，不能未经验证猜phase常量。
4. **受控provision/重启。** 必须在本API JVM调用同一个provisioner/readiness，外部预建资源不能冒充READY。topology-only可沿原显式开关声明但不启动业务consume/dispatch；每次API重启NOT_CHECKED重新成功provision后才能放行。复用原operationLock/幂等声明；首切片只接启动链，不扩成运维框架/定时重试/新deadline。若未来受控重provision确需支持，先关闭本组入场，再调用同实例，失败不得继续沿用旧READY。
5. **失败fail closed。** 连接/auth/声明权限、queue参数/TTL/DLX漂移或任一binding失败，沿原FAILED/PROVISION_FAILED；不启consumer、不claim/publish、不写成功回执、不把passive覆盖当ready、不删除/改名迁就漂移。显式要求enabled的启动/激活应失败并保留诊断，不静默宣称dispatch已启用；发布disabled候选不依赖未接线MQ。安全诊断只固定stage/status/digest与允许的异常类型，不输出原异常、AMQP URL、凭据/消息正文。
6. **停止边界。** 先关本组dispatch/relay入场，再按既有在途settlement收口，不停默认/SMS消费者或未知归属broker/共享Agent，不新增业务重放。最小修改接点为TopologyConfiguration＋新增lifecycle，必要relay启动接线限原config/scheduler；原publisher、ACK/CAS、DAO/auth不替换。本轮不实施、不更改冻结源码、不盲启生产MQ。

### 2.3 必补定向测试与判定证据

- 复用 [AgentRabbitTopologyProvisionerTest.java:45–123](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentRabbitTopologyProvisionerTest.java#L45) 无构造副作用/声明顺序/成功/脱敏失败；[AgentRabbitTopologyConfigurationTest.java:80–97](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentRabbitTopologyConfigurationTest.java#L80) 明确断言构造后NOT_CHECKED，新增测试必须区分构造与启动，不删旧断言来掩盖接线。
- 拟新增主目录 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentRabbitTopologyLifecycleTest.java`；最小后端selector为 `:agent:jia-agent-service:test --tests cn.jia.agent.config.AgentRabbitTopologyLifecycleTest --tests cn.jia.agent.config.AgentRabbitTopologyConfigurationTest --tests cn.jia.agent.config.AgentRabbitTopologyProvisionerTest validateLayering`（后续Owner实现后由Main编排执行，本轮NOT_RUN）。输入/期望：OFF/DB_SHADOW零broker调用；topology-only一次provision、零业务消费；dispatch先canonical成功再container start/claim/send；仅外部存在/passive成功仍拒绝；重复start不重复激活；重启各自重新provision。
- 连接/权限/参数/binding失败：FAILED/Coverage.NONE、consumer未start、零claim/send、固定错误无秘密；partial声明受控重试无purge/delete；停机顺序、default/SMS隔离、scope外拒绝保留。后端原Owner经本地orchestrator定向验证＋validateLayering，精确新SHA/tree/selector绑定。
- 真实专用broker声明及生产业务闭环由Main依授权执行，替身不当生产证据；本轮新增接线/测试均未实现、未跑。这一缺口未收口前全UR05不能称完成。

## 3. 未完成开发：paid-lease悬停恢复与persona读取

### 3.1 精确缺口，不重写已有免费reprovision

已有persona quote POST/agentId lease GET在 [AgentHostingRentController.java:61–82](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentHostingRentController.java#L61)，缺owner-scoped `GET /agent/personas/{personaCode}/hosting-lease`。现lookup按真实owner/registry并在207要求active binding：[HostingRentApplicationService.java:201–224](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentApplicationService.java#L201)，不能alias新路由或放宽原guard来充作合法悬停恢复。

已有REPROVISION在 [HostingRentApplicationService.java:228–277](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentApplicationService.java#L228)，包含immutable receipt优先、intent→lease→binding→request事务、paidThrough/版本与免费请求；缺的是SUSPENDED binding+registry成对恢复接线。[HostingRentApplicationService.java:318–329](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentApplicationService.java#L318) 仍只接受ACTIVE，不是另收费/续期/另跑Provider的需求。

API保全patch `/home/isp/baks/cyf-develop-consolidation-20261009T1558/dirty-api-4/unstaged.patch`（SHA-256 `49a5b6e6d1fef7de39ef4f1e0db928f39273e1a4f24324fc928d3d5203edd19e`）删仍被 [HostingRentApplicationService.java:308–315](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentApplicationService.java#L308) 调用的lockBindings，不能直接应用；当前方法在 [AgentHostingRentBindingMapper.java:16–22](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentHostingRentBindingMapper.java#L16)，exact/resume提案无accepted调用方。[AgentIdentityRegistryMapper.java:10–35](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentIdentityRegistryMapper.java#L10) 只有activateProvisioned/suspendUsable，无悬停恢复接线。

Web [useHostingRent.js:34–43](/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js#L34)、[useHostingRent.js:169–176](/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js#L169) 对未绑定目标发现paid lease前可开放INITIAL并先读wallet；[useHostingRent.js:205–215](/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js#L205) 的accepted receipt/unknown mutation原语义必须保留。保全 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/web-owner-paid-lease-readonly.patch`（SHA-256 `bb78f5cd0a9e07cd471fbc5229fe1ef354208bf4b5ad7205c36fadbba45f6d75`）待原合同适配，其persona响应harness替换不能充当真实HTTP证明。

### 3.2 真实字段与最小跨端详设

| 原表与源码 | 必须核对/更新的字段 | 不可扩大 |
|---|---|---|
| `agent_persona_binding`：[schema.sql:55–90](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/schema.sql#L55) | `id,jiacn,persona_code,agent_id,tenant_id,client_id,status,update_time`；合法status0→1 | owner_jiacn/lifecycle_status/active_persona_code/active_agent_id是生成列不可DML；保留83–84唯一激活约束 |
| `agent_identity_registry`：[schema.sql:92–140](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/schema.sql#L92) | `canonical_agent_id,binding_id,owner_jiacn,tenant_id,client_id,lifecycle_status,suspended_at,update_time`；成对SUSPENDED→ACTIVE | 不换identity/owner；suspended_at清/留由原Owner冻结语义，RETIRED不得复活 |
| `economy_hosting_lease`：[economy-v0-hosting-rent.sql:63–88](/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/economy-v0-hosting-rent.sql#L63) | `lease_id,principal_type,principal_id,persona_code,agent_id,binding_id,status,paid_from,paid_through,latest_intent_id,version,tenant_id,client_id` | 原paid lease/intent准入；不延paidThrough、不新charge/lease |
| `economy_hosting_reprovision`：[economy-v0-hosting-rent.sql:193–217](/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/economy-v0-hosting-rent.sql#L193) | `request_id,lease_id,intent_id,agent_id,persona_code,principal_id,idempotency_key,request_hash,lease_version,paid_through,status,version,tenant_id,client_id` | 保留原幂等字节、receipt/版本链，不另发请求“恢复”未知操作 |

1. 原API Owner定义可证明的authenticated principal→owner→persona→binding/registry→原lease/intent读取合同，认证scope＋canonical persona为输入；复用原LeaseView/admission/decimal-string版本，private/no-store。403/scope不符/读取失败不能默认为NOT_MANAGED再开放INITIAL。
2. 原REPROVISION事务/锁顺序中补exact-scope成对CAS、唯一激活检查，核tenant/client/owner/persona/agent/binding、原paid期/lease/intent/version；任一步失败完整rollback。并发收租/撤销/retire后不得恢复，原receipt replay仍先于后续有效期/供应商状态，不重复charge/续期/Provider执行。
3. Web未绑定打开先canonical owner-paid lookup再决定INITIAL/REPROVISION；免费恢复不以wallet/余额为前置。沿原agentId/leaseId/expectedLeaseVersion/idempotency请求，保留generation/signal、身份切换隔离、unknown operation原样重读、accepted receipt、quote失效/单调版本，不用发现另一lease丢原操作。
4. 最小源码接点：上述Controller/service/两mapper；`/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js`、[hostingRentContract.js:29–47](/home/isp/wsps/cyf/web/src/composables/juyiting/hostingRentContract.js#L29)、[HostingRentPanel.vue:39–42](/home/isp/wsps/cyf/web/src/components/juyiting/HostingRentPanel.vue#L39)及原[hosting-rent.test.js:33](/home/isp/wsps/cyf/web/tests/hosting-rent.test.js#L33)/[hosting-rent-ui.test.js:36](/home/isp/wsps/cyf/web/tests/hosting-rent-ui.test.js#L36)。合同固定后移植保全六文件patch，不在冻结候选盲合。
5. 必保：cross-owner/tenant/client/persona、revoked/RETIRED拒绝、唯一激活冲突、晚失败rollback、并发CAS、重复idempotency原receipt、paid期不变/无新扣款；真实persona读安全前置、Web身份切换/丢响应恢复。现有UI通过不证明新路由/悬停恢复。

[agent-identity-schema.sql:467–470](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql#L467) 只禁止RETIRED复活，不禁止SUSPENDED→ACTIVE；**无新增DDL必要性证据，不删除保护trigger**。

## 4. 未完成开发：F01 context-pack最新Runtime适配

### 4.1 后端已有，客户端缺接入

- 原GET `/agent/tasks/{taskId}/context-pack` 在 [AgentTaskContextPackController.java:43–95](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskContextPackController.java#L43)，仅expectedVersion query、不接受actor覆盖，65–66核当前Runtime proof，84–85交付re-fence；[AgentTaskContextPackController.java:139–147](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskContextPackController.java#L139) 已支持真实RuntimeAuthentication，不能写成仅旧JWT/缺auth。
- [AgentTaskContextPackServiceImpl.java:80–110](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskContextPackServiceImpl.java#L80) 已REPEATABLE_READ只读快照、ACL/currentVersion、accepted artifacts与SHA256摘要；[AgentTaskContextPackMapper.java:9–29](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentTaskContextPackMapper.java#L9) 读真实 `task_plan.id,jiacn,client_id,name,description` 安全列，不新增pack表。
- 原字段 [schema.sql:208–236](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/schema.sql#L208) 的 `agent_task_meta.owner_jiacn,task_version,current_event_version,tenant_id,client_id`，原member239–262/work_item265–296继续提供成员/任务版本事实；不另表伪造provenance。
- [runtime-client.mjs:82–106](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs#L82)、[runtime-client.mjs:202–216](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs#L202) 仅许可internal与精确E05 lease路径，**现在context-pack被拒绝**；[agent-client.mjs:5526–5544](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L5526) 有E05/Workspace File/SKILL/普通TASK分流但无F01 adapter。[agent-client.mjs:5359–5412](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L5359) 原command-bound E05适配已完成，不重建。

### 4.2 最小适配/验收

1. RuntimeV1Client只增原context-pack GET的规范taskId/expectedVersion许可，固定same origin/路径/单值query、无credentials/hash/redirect；沿当前subject session proof与generation取消，不开放所有 `/agent/` 或恢复direct JWT/API key。
2. 原F01 schema/digest/provenance校验接当前TASK binding/prompt：核task/actor/scope/currentVersion/安全字段，轮换后的pack不得进入执行prompt，无跨Agent凭据；读取失败不得假称上下文完整。保留原普通TASK和E05 lease/start/result/ACK链，不建第二lease引擎。
3. 主目录接点为上述runtime-client/agent-client；如需独立解析模块由原Owner固定新增路径并同步最新standalone打包清单/测试，不能把未合入旧模块当已安装文件。
4. 待补测试：合法session GET摘要一致快照；错task/actor/owner/version、tampered digest/schema、跨origin/多余query拒绝；session轮换/撤销pack不得入prompt；原E05/ACK/安装清单不变。Node桩不冒称API/DB/生产验收。

保全 `9e8d78dd459aae1c8e28003eebfdc107945f6f5b` / `a0ad68e36c0f5fe97689d8e3424b5f96e4d1921e`：`/home/isp/baks/cyf-develop-consolidation-20261009T1558/pending-runtime-9e8d78dd4.patch`（SHA-256 `00ad68a8d2a6f0df2c959de00641dc377243d0edb7e192fadc47d8233e7a2bb3`）、`/home/isp/baks/cyf-develop-consolidation-20261009T1558/pending-runtime-a0ad68e36.patch`（SHA-256 `8ee8a9a0f3849f6e50bbea2b83f295a49d361e4a6b9dee7a142b1a8a98df16b5`）。其旧installer/auth/E05不复活，只向最新Runtime精确适配F01。

## 5. 未完成开发：Workspace File固定结果durable report恢复

### 5.1 不是“全部durable recovery未实现”

[agent-client.mjs:5211–5255](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L5211) 已私有输入materialize/Provider前canonical start；[agent-client.mjs:5256–5295](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L5256) 已结果提交、unknown start/upload/commit保留recovery_required与terminal cleanupProof；[workspace-file-bridge.mjs:651–689](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/workspace-file-bridge.mjs#L651) 一次start未知不执行Provider；[workspace-file-bridge.mjs:804–830](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/workspace-file-bridge.mjs#L804) cleanup沿原path/fingerprint/device/inode，不重materialize。

原E05已有不含leaseToken的原结果持久保存再提交，丢响应GET-only恢复：[agent-client.mjs:5466–5474](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L5466)、[agent-client.mjs:5509–5520](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L5509)。processor durable checkpoint/HTTP ACK与subject隔离已有：[execution-adapter.mjs:28–43](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L28)、[execution-adapter.mjs:88–100](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L88)、[runtime-host.mjs:115–158](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-host.mjs#L115)，不能列为待开发。

真实缺口：Workspace File bridge内存 `#runs`/当次outputs尚未形成与最新per-Agent checkpoint、native start、D06 terminal/cleanupProof一致的**跨重启固定结果report-only恢复**。[workspace-file-bridge.mjs:743–801](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/workspace-file-bridge.mjs#L743) 当前固定文件hash/length及幂等upload/commit，不证明旧durable patch已整合。

### 5.2 真实原表字段（不新建结果表/DDL）

| 原事实与源码 | 必须保留的字段/状态 |
|---|---|
| `agent_personal_workspace_execution`：[agent-personal-workspace-v1_11-executions.sql:2–40](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-personal-workspace-v1_11-executions.sql#L2) | `execution_id,owner_jiacn,task_id,run_id,target_agent_id,execution_state,grant_revision,idempotency_key,request_hash,tenant_id,client_id`；状态QUEUED/INPUTS_REVOKED/OUTPUT_COMMITTED/FAILED，不能杜撰STARTED/REPORT_PENDING写入此列 |
| `..._execution_input`：[agent-personal-workspace-v1_11-executions.sql:42–70](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-personal-workspace-v1_11-executions.sql#L42) | `input_ref,execution_id,file_id,file_version,byte_length,content_hash,storage_uri,grant_state`及scope；沿原授权/版本，不重授权来重跑 |
| `..._execution_output`：[agent-personal-workspace-v1_11-executions.sql:72–99](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-personal-workspace-v1_11-executions.sql#L72) | `output_id,execution_id,byte_length,content_hash,storage_uri,output_state,workspace_file_id,workspace_file_version,staged_at,committed_at`及scope；STAGED/COMMITTED，manifestId不是此表新列 |
| D06 delivery/inbox：[agent-command-transport-schema.sql:6–42](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L6)、[agent-command-transport-schema.sql:90–124](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L90) | delivery `command_id,target_agent_id,owner_jiacn,status,active_message_id,active_attempt,version`；inbox `consumer_name,message_id,command_id,status,result_status,active_attempt,processed_at,version`及scope；保存结果不等于终态ACK已确认 |

### 5.3 最小状态/恢复适配与测试

1. 旧tip `e0fb44c92ecd87c52e3b0f5e87d6c3e1fd71ecc3` 保全于 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/pending-runtime-e0fb44c92.patch`（SHA-256 `7a5f632a89b26de03b7cb3e949a6c1e860f83d9a1f44bebafd75351ead4cbf06`），删除最新startExecution/cleanupProof/onCommandTerminalConfirmed并用进程全局instance identity，不能直接合入。
2. 原Owner在结果产生后、首次报告前沿原原子checkpoint机制持久固定output声明/hash/length、原upload/commit idempotency、失败code或结果body、subject/command fingerprint/run/API身份与cleanupProof。不存session/leaseToken/其他Agent秘密；拟议RUNNING/RESULT_READY/REPORT_PENDING只能是本地checkpoint态，不改原业务表ENUM。
3. 重启核scope/fingerprint/原目录所有权/固定文件未变，取得合法当前session/fence；仅有原结果才report-only/原幂等upload恢复，丢响应沿原权威读取/receipt确认。unknown STARTED/无原结果不得重跑Provider/任务，不复制业务实现；401/403/rebind/撤销/身份冲突fail closed，不能作为网络可重试。
4. native业务终态＋D06终态ACK均确认后，沿 [agent-client.mjs:3688–3700](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L3688) terminal callback和原bridge inode proof清理；ACK/报告未知或目录被替换保留原记录，不清账/重materialize/删除其他subject目录。
5. 最小接点：主目录agent-client的runWorkspaceFileCommand/checkpoint/terminal callback、workspace-file-bridge的固定output报告/恢复，复用原processor/runtime-host，不新增队列/状态服务。必补重启无结果不重跑、文件改变、subject/API切换、partial upload、commit丢响应、终态ACK丢响应、cleanup中断/改inode；保留原E05 prepared result/GET恢复全部断言。本轮不实现/不运行。

## 6. 仅余Runtime切流与真实auth业务恢复阻塞

后端发布已由Main核销：原installer `status=verified`、exit0，回执为 `/var/tmp/cyf-consolidated-api-20261009T1632-878Opf/local-install.stdout` 最后JSON；JAR摘要前缀 `15d3456e`、PID1248394、start15009554，F06/E05均PASS，原13DDL/strict postcheck与配置完成。前端Run186已发布并在线核验。以上仅作为从待交付清单删除的边界说明（Main回报，本Owner未读取安装stdout或重复操作生产），不重列为待开发、准备installer或等待发布。

### 6.1 已定位的认证断点与尚未执行的恢复步骤

真实公网浏览器登录、432详情/成果列表均HTTP200，但432无交付；原bootstrap为`RETRY / BOUNTY_RUNTIME_AWAITING`，采样`attempt_count=10,version=20,admitted_conversation_id=NULL,admitted_request_id=NULL`。新relay正在重试，并非旧进程PENDING0或仅需继续等待。原需求/指派/任务版本未改，无新增/重复点将或手动发消息。

| 已确认断点 | 当前源码行 / 实际字段 | 最小未完成处置 |
|---|---|---|
| 旧WS四profile仍以`X-API-Key`连新native链，握手401 | [AgentRuntimeSecurityConfiguration.java:38](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSecurityConfiguration.java#L38)；[AgentRuntimeAuthenticationFilter.java:99–118](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationFilter.java#L99) 明确拒绝旧key，要求`Authorization: AgentRuntime ...`及五identity headers | 交付现有统一Runtime，不恢复旧auth fallback，不关闭鉴权。当前影响吴用/林冲/卢俊义及共享managed公孙胜，不能只报API健康 |
| 旧HTTP sidecar请求缺`hostId/runtimeInstanceId`；新PID观察到吴用session400 | [AgentRuntimeAuthenticationService.java:55–58](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationService.java#L55)；[runtime-client.mjs:169–177](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs#L169) | 配置真实持久hostId与独立boot instance，经现有session接口取得证明；日志没有具体异常分支，不能把另外两unit历史failed说成新400 |
| 三原installation ACTIVE且manifest匹配；当前fence全NULL | `agent_runtime_v1_installation.installation_id,canonical_agent_id,status,manifest_sha256,runtime_authorization_hash`；`agent_runtime.runtime_installation_id,runtime_host_id,runtime_instance_id,runtime_session_generation,token_hash`；[AgentRuntimeAuthenticationService.java:84–104](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationService.java#L84) | 复用三原逐主体0600authorization文件（有效性仍待真实session验证），不重放已消费enrollment secret。正常事务从NULL首次绑定并generation+1，无需SQL reset/转移fence；`CHANNEL_PENDING`须继续WS注册至真实READY |
| managed公孙胜没有该canonical的native installation | 原只读snapshot，不能借用三角色installation/credential | 单独确认其manifest/enrollment/owner和在途接续，保留共享进程其他profile；不能把三Agent恢复称四profile全恢复 |

现成CLI入口是 [agent-runtime.mjs:38–59](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L38) 的单host生命周期与 [agent-runtime.mjs:62–85](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L62) 的`validate/enroll/run`。此项是**匹配客户端的安装、配置、状态接续和切流尚未完成**，不是API缺schema或需要重写认证。固定最新Runtime commit见§1，不能部署诊断报告引用的历史tip充数。

受控安装后依次验证`session → native WS → agent.register/receipt → protected executor typed READY`，然后只续原432，核同一bootstrap入会话/请求与最终交付。保留原checkpoint/ledger/inbox/ACK/未知STARTED；不重放、不伪造READY。只读归因和生产实测分别在 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/runtime-auth-diagnosis/ur04-production-runtime-auth-diagnosis-20261009.md` 与 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/production-browser/production-acceptance-report.md`。

### 6.2 Runtime切流待交付边界

Main候选目标 `/home/isp/apps/cyf-agent-runtime-v1/unified`、unit `cyf-agent-runtime-v1@unified.service`、`/etc/cyf-agent-runtime-v1/unified.host.json`/`unified.conf`；host state `/home/isp/state/cyf-agent-runtime-v1/unified/host`，subjects为同级 `agents/<完整subjectSHA>/` 独立目录。以上为交付设计，不断言现场存在；manifest/installation/hash与固定payload匹配，无token正文/旧直连身份。

| 入口 | Main仍需核对/处置 | 不得混同 |
|---|---|---|
| `codex-ws-agent@wuyong-local.service`＋`cyf-agent-runtime-v1@wuyong.service` | 吴用同subject旧WS/HTTP sidecar，临切流精确PID/cgroup/session/checkpoint/在途及维护权限，按原优雅退出/新session合同切入 | 心跳sidecar不是统一执行Runtime；停进程不是state交接 |
| `codex-ws-agent.service` | 林冲/卢俊义direct与managed公孙胜共享；核subject在途及定向停止/保留路径，现路径若不能安全拆分由原Owner另列具体缺口 | 不整停影响不同owner/公孙胜/RECOVERY_REQUIRED，不假称共享进程切流只需配置 |
| 新三subject | 原动态授权、manifest/installation/host一致、CLI/profile/schema真实READY、独立credential/env/root、registration与HTTP ACK/fence、每subject唯一执行入口 | 不SQL revoke/transfer/清fence，不重跑unknown STARTED，不共token |

非零在途区分未admit/RECEIVED/durably STARTED/WAITING_AGENT/终态，不强制清零/kill/reset/replay；旧账本矛盾保留，不改账推成功。installation/host不符沿原拒绝，缺转移授权交Main，不猜新接口。

## 7. 其他保全提案与收口判据

Web `E13_OLD_REASON_SUBSET` 是旧快照提案与Python `collision`诊断不一致：[juyiting-e13-offline-validator-contract.test.js:10–10](/home/isp/wsps/cyf/web/tests/juyiting-e13-offline-validator-contract.test.js#L10)、[validate.py:22–22](/home/isp/wsps/cyf/web/scripts/juyiting/e13/offline_pixel_renderer/validate.py#L22)、[world-model.mjs:305–305](/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/world-model.mjs#L305)。若后续采纳更窄集合由原E13 Owner统一JS/Python生产诊断及测试；**不是本次新增发布功能/强制阻塞，不删测试/覆盖现安全OAuth/E13**。

### 7.1 历史ops-resource-telemetry-r3：未完成独立接入，不扩框架

依据 `/home/isp/baks/cyf-develop-consolidation-20261009T1558/root-tip-decisions-final.json`，历史tip `d136cb7abf76a8f87b367a11d16165591d1e162c` 的controller/evidence-envelope贡献未证明已接入；不能整包恢复，因为该tip删除当前README、execution_history_check、preflight等编排入口。

- 精确旧源码接点（仅历史tip可读，当前主目录两文件不存在）：`/home/isp/wsps/cyf/ops/orchestration/cyf_controller_executor.py` 的历史180–243行校验config/capability/原orchestrator源码摘要、275–318行入口与加载；`/home/isp/wsps/cyf/ops/orchestration/cyf_evidence_envelope.py` 的历史195–240行request/replay identity、308行起证据生成/注册。以上行号绑定历史tip，不能当作当前已交付文件链接。
- 待补的是原用途下最小controller调用/证据封装合同与可信输入：精确task/操作、源码commit/tree/selector/fixture digest、controller-config/capability来源/权限、证据目标与幂等冲突处理；当前没有足以宣称部署/配置完成的输入或真实接入证据。不是因此另造一套runner/ledger/准入框架。
- 保留现有 [cyf_orchestrator.py:718–737](/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py#L718) 的窄Flow remote dispatch及既有gradle/preflight/execution-history入口；原Owner若后续承接只移植独立贡献，不删除当前工具。测试须证明原CLI/锁/任务身份不变、源码/输入摘要漂移拒绝、同输入重放与不同输入冲突可判定、证据原子落盘不泄密。此历史提案未接入，不算应用业务功能或本次发布阻塞，本轮不开发/不执行。

### 7.2 旧health脚本：保留最新生产修复并校准信任输入的交付缺口

旧health tip已是root祖先，不代表其中脚本适合重新安装。当前主目录 `/home/isp/wsps/cyf/ops/health/` 的旧payload与已安装monitor/carrier不等价，**待完成是运维脚本源码整合/可信pin校准与受控交付，不是新增应用功能**。

| 精确差异/已存在修复 | 主目录或已安装安全代码证据 | 未完成处置 |
|---|---|---|
| 旧monitor不调用carrier只读check | [旧health.py:789–804](/home/isp/wsps/cyf/ops/health/cyf-juyiting-health.py#L789)；最新修复 [maintenance health.py:789–811](/home/isp/wsps/cyf/ops/maintenance/health_monitor/cyf-juyiting-health.py#L789)，已安装 `/usr/local/libexec/cyf-juyiting-health.py:800` 同样调用 `--check` | 合并保留预留恢复次数前的真实check；pin错误不耗次数/不伪装未知终态，不把已完成修复列为待发明 |
| 旧carrier无 `--check` 分支 | [旧carrier.py:152–159](/home/isp/wsps/cyf/ops/health/cyf-juyiting-recovery-carrier.py#L152)；已有 [maintenance carrier.py:152–173](/home/isp/wsps/cyf/ops/maintenance/health_monitor/cyf-juyiting-recovery-carrier.py#L152)，installed carrier156行也有该分支 | 保留只读验证、不spawn Java/scope、不写状态的接口，不以旧三参数入口覆盖 |
| SMTP认证失败仅泛化helper_failed | [旧health.py:1069–1074](/home/isp/wsps/cyf/ops/health/cyf-juyiting-health.py#L1069)；已有 [maintenance health.py:1079–1089](/home/isp/wsps/cyf/ops/maintenance/health_monitor/cyf-juyiting-health.py#L1079)，installed1086行同样分类 | 保留 `smtp_authentication_failed_<数字状态>` 脱敏分类，不输出原SMTP报文/地址/秘密；SMTP接受不等于收件箱送达 |
| canonical目录/物理日志路径修复不能退回 | [旧health.py:1055](/home/isp/wsps/cyf/ops/health/cyf-juyiting-health.py#L1055) 仍用兼容 `/opt/cyf/service/api`；已有 [maintenance health.py:1065](/home/isp/wsps/cyf/ops/maintenance/health_monitor/cyf-juyiting-health.py#L1065) 使用 `/home/isp/hosts/cyf/api`；当前 [cyf-api-kit:34–35](/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit#L34)、[182–184](/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit#L182)、[838–840](/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit#L838) 保留物理 `/var/log/cyf-api-flow` 与权限校验 | Main已把kit source两处恢复为installed字节一致，kit该修复不再列缺源码；旧monitor/安装包整合须保留这些现行修复，不恢复旧目录/日志别名 |
| 三层信任摘要尚未校准 | [旧carrier.py:11–12](/home/isp/wsps/cyf/ops/health/cyf-juyiting-recovery-carrier.py#L11) pin为 `63a7ba180603d021666af77e9535b93bdbdcedf0ce799d0b5e09e7718e8d0bcd`；maintenance carrier12行pin `94de2c8af2745d25a9cec82276d54e52c85a63ae7349f4204b36ba5f5f5b930f`；installed carrier12行pin `6f217a43cfcca224da722e72987b54f418aebf792ce3fa4cf348fe2e247186ac` | 本轮只读hash核得kit source及 `/usr/local/sbin/cyf-api-kit` 均为 `9685c35b8bff293f474d5f1684312ecff4f88d0cd6f87450ae6b433a992356c2`；这些carrier pin均不等于当前kit，不能直接启动新cron/恢复调用或自动信任磁盘新值 |

本轮只读已安装摘要：monitor `5a93dbd93939c0bea727547559fb12bd0731f1d5fca2b94f4dc8c3804ffcced2`、carrier `b1c28771e7cd19b514a2d261d9eb8638beccd7b58c0bc6cf391f9de55b20860f`；旧ops/health payload分别 `74e93f804cd12b5bae37f416d332485df0d698ea9bc8088e4b5f0b307e4cff45` / `440e82ab992b88778b26542e176c8f7da14c62c66e6bad32b3dcb941e908c321`。这是源码/文件摘要差异，不声称当前cron状态或实际恢复/邮件成功；没有运行monitor/check/carrier、读取秘密配置或操作生产。

后续原Owner最小动作：先保全source/installed各自增量，在最新生产修复之上整合唯一候选；核当前合法canonical kit后固定carrier `CANONICAL_SHA256` → 新carrier摘要 → monitor `RECOVERY_CARRIER_SHA256` → 安装器candidate摘要/回执，不能仅改一个pin。保留 [maintenance README:8–12](/home/isp/wsps/cyf/ops/maintenance/health_monitor/README.md#L8) 的root ownership、monitor.lock、备份/原子替换/readback及失败仅恢复本次写入；旧 [install.sh:123–136](/home/isp/wsps/cyf/ops/health/install.sh#L123)/[157–172](/home/isp/wsps/cyf/ops/health/install.sh#L157) 固定的是旧payload，不可直接install/install-cron覆盖生产。复用 [test_juyiting_health_recovery.py:26–40](/home/isp/wsps/cyf/ops/maintenance/tests/test_juyiting_health_recovery.py#L26)、[162–175](/home/isp/wsps/cyf/ops/maintenance/tests/test_juyiting_health_recovery.py#L162) 的只读check/pin/SMTP脱敏与原health测试，不在本轮重跑或试发邮件。真实交付需Main明确维护授权后实施，不能借此次文档收口扩权。

### 7.3 历史PhaseA与当前bounty严格schema不一致（真实未完成适配）

Main已确认当前 `agent_task_bounty_quote`、`agent_task_bounty_claim_operation`、`agent_task_bounty_settlement` 三表**均无owner_jiacn**。这与当前正式表资源/initializer一致，不能当作本次13DDL遗漏；真正未完成的是历史 `single-tenant-task-owner-ddl.sql` 三段owner扩列/索引与当前严格schema契约的统一。

| 具体冲突 | 历史PhaseA实际片段 | 当前真实严格契约 |
|---|---|---|
| quote额外owner列/owner_scope索引 | [single-tenant-task-owner-ddl.sql:166](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql#L166) 的166–179行加nullable `owner_jiacn VARCHAR(50)`；[single-tenant-task-owner-ddl.sql:383](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql#L383) 的383–394行建 `idx_agent_task_bounty_quote_owner_scope(tenant_id,client_id,owner_jiacn,task_id,id)` | [AgentTaskBountyQuoteSchemaInitializer.java:88](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskBountyQuoteSchemaInitializer.java#L88) 的88–95行按ordinal_position读取全部物理列，93行以 `spec.columns().equals(...)` 全列表严格相等，额外owner列必拒绝；[AgentTaskBountyQuoteSchemaInitializer.java:104](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskBountyQuoteSchemaInitializer.java#L104) 的104–124行也严格比完整索引集合，不只核必需索引 |
| claim_operation同类冲突 | [single-tenant-task-owner-ddl.sql:180](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql#L180) 的180–193行加同owner列；[single-tenant-task-owner-ddl.sql:397](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql#L397) 的397–408行建 `idx_agent_task_bounty_claim_owner_scope(tenant_id,client_id,owner_jiacn,task_id,id)` | 同quote initializer，[AgentTaskBountyQuoteSchemaInitializer.java:22](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskBountyQuoteSchemaInitializer.java#L22) 的22–24行TABLES明确包含两表；正式 [agent-task-bounty-quote-v0.sql:2](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-task-bounty-quote-v0.sql#L2) 的2–74行两表无owner_jiacn，按principal_type/principal_id及原scope定义 |
| settlement列及非唯一索引也冲突 | [single-tenant-task-owner-ddl.sql:194](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql#L194) 的194–207行加同owner列；[single-tenant-task-owner-ddl.sql:411](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql#L411) 的411–422行建 `idx_agent_task_bounty_settlement_owner_scope(tenant_id,client_id,owner_jiacn,task_id,id)` | **实际类为AgentTaskSettlementSchemaInitializer，不是AgentTaskBountySettlementSchemaInitializer**：[AgentTaskSettlementSchemaInitializer.java:67](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskSettlementSchemaInitializer.java#L67) 的67–78行、尤其71行按物理列完整有序列表严格相等，[AgentTaskSettlementSchemaInitializer.java:111](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskSettlementSchemaInitializer.java#L111) 的111–118行expected columns无owner；[AgentTaskSettlementSchemaInitializer.java:80](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskSettlementSchemaInitializer.java#L80) 的80–91行要求索引non_unique=0及仅原PRIMARY/两个unique完整集合，额外非唯一owner_scope索引也拒绝。正式 [agent-task-bounty-settlement-v0.sql:2](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-task-bounty-settlement-v0.sql#L2) 的2–31行亦无owner列 |

- **实际启动影响。** [AgentTaskFundingSchemaConfiguration.java:17](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L17) 的17–26行在 `economy.preview.enabled=true` 注册quote与settlement initializer；settlement [AgentTaskSettlementSchemaInitializer.java:35](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskSettlementSchemaInitializer.java#L35) 的35–39行对已存在表直接validateCatalog。因此盲执行完整旧PhaseA后，在这组initializer启用的启动/重启中会因额外列/索引失败，不能用“nullable/additive”或“只加owner”宣称安全。
- **调用边界已定向核实。** 全生产 `src/main` 未发现该SQL资源的调用；生产initializer引用各自正式quote/settlement资源，而非PhaseA。UR06 fixture [Ur06EnrollMysqlFixture.java:258](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java#L258) 的258–267行 `initializeM4()` 在同一JDBC连接依次执行原E05 SQL及整个PhaseA；另默认测试仅注释提及PhaseA。fixture引用不能替代生产调用/当前严格catalog兼容证明，也不能把该旧片段自动扩入生产迁移范围。
- **最小待补，仍只详设。** 原Owner需以当前冻结bounty表契约统一历史脚本、对应initializer/schema资源和UR06消费片段，明确哪些owner扩列/索引不适用；不能先加生产列再宽松放过strict检查，不能猜principal_id等于owner并回填历史数据。补定向合同回归：当前正式三表strict通过；额外owner列/额外owner_scope索引分别明确拒绝；适配后的PhaseA/fixture执行后再启动原initializer保持strict通过。保留ACL/幂等/主键唯一及列类型/顺序完整校验，不扩新DDL/协议/第二实现。
- **本轮不执行未适配旧片段，不改源码/生产。** 它不属于已全部执行且strict postcheck PASS的原13DDL；Main配置已写且后端installer verified exit0，此处仅保留真实schema不一致备忘，不把已完成13DDL再次标为待交付。

前后端发布、原13DDL与配置已完成，不再列为待交付；仍不等于Runtime切流/真实auth与生产命令链恢复、§2–5或全UR05完成，MQ未接线不盲启。待开发按新source及原合同断言收口，待交付按本批版本/commit/tree/制品SHA/安装配置/catalog/在线业务证据核销；已由Main核销的前后端发布、原13DDL/strict postcheck、配置与kit source恢复不重新记为待开发/待发布，不用历史回执填当前PASS；文档整理不增加发布硬门槛。
