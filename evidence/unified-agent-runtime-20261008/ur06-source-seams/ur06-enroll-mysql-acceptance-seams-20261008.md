# UR06：真实 enroll / MySQL 云验最小接点（只读支持）

日期：2026-10-08（Asia/Shanghai）。角色：原 UR06 explorer/support；非 Reviewer，未接 Writer。
本轮仅定向读取固定源码并新增本报告；未运行 Gradle/npm/pip、安装、HTTP/数据库请求、Flow 查询/写入或生产操作，未读取输出凭据。下列云验均 **NOT_RUN**，源码存在不等于实测通过。

## 1. 固定输入与证据边界

- API 父候选：`eac15d988445784e9004fa393bdce8671ca96dab`，tree `07223f7fcdce7af0321b1ae021e1f5150c01e03f`。
- 当前检查 worktree：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008`，HEAD `544e83910ddefa600b5510f62635a5379c8bf32e`，tree `2fbefddad76ec93ba507e9f8eb1630ee498bda76`；检查时 clean。相对父候选只增加六个 UR04 测试文件，无生产差异。
- client：`3746043947888a6b727be88527695d1edf3587c3`，tree `ddc3c0b3355eb77cd0be080f8fc4b734c901cab7`；从 `/home/isp/wsps/chcbz/isp-install` 用固定 `git show` 读取，非当前工作目录内容。
- 原 UR04 完整 source archive 绑定：285 tracked files、3,573,760 bytes、SHA256 `55ffef55075cf802a1a090114c5a3be6dd933dc8925b80d3403f9404e5fe9781`。不是 UR03 两模块 archive。
- 交接输入：`/tmp/ur04-e05-http-handoff-20261008.json`。six selectors 全部 NOT_RUN：`e05ActualClientHttpCommitsOriginalResultAndTerminalAck`、`e05LostResultReadbackSurvivesJavaAndNodeRestart`、`e05TerminalAckLostResponseReplaysPriorWithoutWorkRerun`、`e05PreparedCommitRefencesAndRollbackIsDurable`、`e05SourceAndOriginalResultProofStayFailClosed`、`e05UnknownStartedNeverRerunsAndSiblingRemainsReady`。
- 按主控输入：Flow139/job531048271 RUNNING，无终态原因；安装138 C1/C2 PASS、C3/C4 FAIL，无完整 artifact。本报告不补推终态、不重跑或改活动 Run。
- 下一安装 fix 必须重新绑定完整 client commit/tree/archive、manifest/file hashes 和同源干净依赖 artifact；不能只替换 commit env 或继续引用374的旧 archive/artifact。由原 Owner/主控更新，不在本任务改其 fixture。

## 2. enroll 的真实调用接点与尚未证明的边界

### 2.1 原服务 / DAO / wire（源码存在）

1. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentRuntimeV1Controller.java:65-80,129-142`：真实 POST `/agent/runtime/v1/enroll` → `runtime.enroll(request, now)`；session 是 POST `/agent/runtime/v1/session`、安装 Bearer。bootstrap 禁止 Origin、X-API-Key、query，成功是 `JsonResult.success(data)`、`private, no-store`。
2. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentRuntimeV1EnrollmentResult.java`：record 两字段 `installation`、`runtimeAuthorization`。实际 HTTP 是 **JsonResult.data 内嵌此 record**，不是顶层 installationId，也不是新增 `enrollmentResult` wrapper。
3. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentRuntimeV1ServiceImpl.java:54-76,101-141`：`create` 原事务代理校验 canonical scope，插入 PENDING/version0/secret digest；`enroll` 原事务内锁安装、完整 manifest/主体匹配、PENDING/unconsumed/unexpired、constant-time digest，生成真实随机 rta1，activate 后 ACTIVE/consumedAt/issuedAt/version+1；`session` 用真实安装 credential hash 再锁安装并调用 `sessions.issue`。不预置 ACTIVE 或自造 rta 代替此步骤。
4. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentRuntimeV1InstallationMapper.java:11-18,45-57`：原 `FOR UPDATE` 和精确 binary/octet ID；activation CAS 同时限定 version/PENDING/unconsumed/unexpired。默认 DAO 是 `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentRuntimeV1InstallationDaoImpl.java`，应通过真实 MyBatis mapper/SqlSessionTemplate 使用，不 mock。
5. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSecurityConfiguration.java:24-53`：order0 bootstrap permitAll 只是选择安装认证 lane，仍须原 controller/service 实际 secret/Bearer 校验；order1 原 `AgentRuntimeAuthenticationFilter` 负责 native 权限。不得把 permitAll 解释为免安装认证。

### 2.2 固定 client 与真实 WSready 接点（源码存在，闭环 NOT_RUN）

- `/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs:109-177` @374：默认 `globalThis.fetch`，unwrap `json.data`；严格两字段 record、九字段 installation、完整 manifest、ACTIVE、epoch/null heartbeat、真实格式 rta1；`client.enroll(secret)` 先独占持久 attempt marker，再发真实 HTTP，0600 私有 authorization 写入/读回后才成功。public return 仅 installationId。
- 返回不确定/解析失败/写盘失败统一 `RUNTIME_ENROLLMENT_RECOVERY_REQUIRED`、nonretryable；成功后再次 enroll 是 `RUNTIME_ENROLLMENT_AUTHORIZATION_EXISTS`。旧 marker 跨进程阻止 secret 重放；不能新增自动 reissue/rebind/retry。
- `session()` 从私有安装文件取得实际 rta，通过真实 Bearer 换独立 rts1/generation；session token 仅内存。manifest 本地 `sha256:` 前缀经原 identityOf 处理，fixture 必须使用原 manifest sealing/identity，不能假定 wire 也带前缀。
- `/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:12-24,42-95` @374：默认 import 原 `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs`、真实 `loadWebSocketClient`、原 RegistrationAckObserver；`client.session` → `new Socket(client.websocketUrl(), client.websocketOptions())` → 原 `agent.register` → matched `agent_registered`/proof/generation 才 channelConfirmed/activated。不注入假 loadEngine/socketFactory/clientFactory。
- `/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs` @374：显式 enroll CLI 是独立阶段；host run 不自动 enroll。验收需先调用真实 client.enroll，再启动原 host/adapter，不能运行 host 就宣称已消费 secret。
- `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/chat/jia-chat-service/src/main/java/cn/jia/chat/config/AgentRuntimeHandshakeInterceptor.java:22-40`：真实 servlet headers → 原 authentication.verify；无 query token。`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java:843,871-873`：原 auth fence 中实际 AgentService.register，bind 使用 **session::isOpen**，真正发送 agent_registered；不能手工返回 ACK 或固定 connected Supplier。
- “WS 注册/传输 ready”只证明真实连接、身份与 registration receipt，不自动证明所有 TASK/CHAT/SKILL 工具 ready；没有可执行命令类型时不得上报全功能 ready，也不得用注册成功抵消 UR04 E05 sixselectors NOT_RUN。

### 2.3 最小增量输入 / 期望 / 非秘密证据

以下均为拟实施验收，非本轮执行结果。每例私有数据独立，manifest/identity 正常使用原 API/client 校验。

| ID / 状态 | 实际输入 / 接点 | 必须判定的期望与证据 |
|---|---|---|
| E1 / NOT_RUN | 原服务 create 事务代理准备 PENDING；随机一次性 secret 仅 private pipe；实际 Node client.enroll → Tomcat/Spring/controller/service/default MyBatis DAO | 真200/nested shape/Cache-Control；实际安装变 ACTIVE/version0→1、consumed/issued 非null；独立 JDBC 比较安装文件 rta 的 digest 与 DB 相等、secret digest 未变，仅输出布尔/版本/计数；私有文件0600、无 alias，marker 与 public return 不含 secret/rta/rts。禁止向诊断上传 response/raw文件/hash凭据。 |
| E2 / NOT_RUN | E1 发出的真实 rta → client.session；启动原 host/adapter/engine/socket，原 handshake/filter/auth/AgentService 注册 | 真 session/generation、真实 agent_registered 对应原 messageId/主体/proof；DB 当前 runtime verifier 是实际会话摘要而非原始 token；WS绑定真实 isOpen，旧证明不能冒充 ready。Java A→B、Node重启后沿同一私有数据重新 session，generation 增长，旧 session/native/WS注册拒绝且无业务变更；安装凭据保持。完整 artifact C1–C4 是此闭环前置。 |
| E3 / NOT_RUN | 各新PENDING：错误 secret / 已到期（create时未来，待真实时钟越过）/ valid格式但错误manifest或主体；真实 default fetch，不伪造响应 | server403；原 installation version/status/consumed/authHash不变；client.enroll 对网络后的拒绝按原契约 recovery-required 而不是保证暴露403。实际状态可由脱敏 servlet status观察或独立真实fetch负例观察；不改 client 错误契约。 |
| E4 / NOT_RUN | 同一安装/secret，两个独立私有stateDir同时真实 HTTP；成功后第三个新state请求同一secret | MySQL行锁/CAS：只能一次激活/发放，恰一个成功，其余真实403、version只+1/credential digest不换。同一stateDir原marker挡在HTTP前另做计数，不能将该本地拒绝冒充server并发消耗证明。 |
| E5 / NOT_RUN | 真实 /enroll 事务提交后、响应到客户端前，透明 servlet buffering 仅扣住此响应；独立JDBC确认ACTIVE后终止**本fixture拥有的Java A** | default fetch 真实TCP失败；state仅含attempt marker、无可用安装auth；重启Node/Java B后 enroll不发第二次HTTP，仍recovery-required；DB消费时间/version/authDigest不变。不自动重建授权或删除marker；无响应内容/child secret stdout上传。 |

准备 PENDING 通过原 service create 不等于安装管理 HTTP/JWT 已验：`/installations` 管理接口的原 scoped JWT、真实 installer CLI secret输入通路若未单独跑，保留 NOT_RUN。私有 ACTIVE user/registry/binding 是授权fixture数据，**不是 ACTIVE Runtime installation preseed**。rta 必须是 E1 原 enroll 发出，不接受 REDACTED marker 或合成 rta 作为 E1/E2输入。

## 3. 默认真实权限/DAO来源及最小私有数据

可复用装配设计（不改 Owner 文件）：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpFixture.java:436-455,596-683,715-748`：真实 Tomcat/WsSci/AnnotationConfigWebApplicationContext/security chain/事务代理/原 mapper。保留真实 UserInfoDaoImpl、AccountSecurityServiceImpl、AgentIdentityServiceImpl、RuntimeV1ServiceImpl、AgentRuntimeAuthenticationService、AgentServiceImpl、D06 AckService。

- `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationService.java:53-146,188-215,224-268`：真实 registry/binding/account authority、runtime锁/代际递增、随机rts1与urs1摘要/account id/authEpoch；`withFence` 锁 installation 和 runtime，scope/ACTIVE/generation/boot/verifier/account一致才执行原 joined业务/D06事务。不用 mockDAO、auth stub、替代 Supplier 作为跨端证明。
- 原 account SQL 必须注册 `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/user/jia-user-mapper/src/main/resources/cn/jia/user/mapper/InfoMapper.xml:124-129` 的 `selectSecurityByExactJiacn`，由原 UserInfoDaoImpl/AccountSecurityServiceImpl查询真实 ACTIVE user/authEpoch，包含 exact binary/octet 和至多两行唯一性判定。
- 最小私有数据：tenant字符串 `0`、本run独立 synthetic client/owner、有效 canonical opaque Agent IDs/Runtime installation IDs；真实 persona、binding、ACTIVE registry、ACTIVE user/authEpoch；通过 service create 的 PENDING 安装及完整sealed manifest。必要 runtime 行由原 session/注册路径维护。使用独立 sibling主体做旧代际/撤销对照时，凭据各自独立且不得进入别的Agent env。
- D06在原 gate的已授权 synthetic scope 中运行原 RecoveryDaoImpl/AgentCommandRecoveryMapper；预置与实际codec一致的 delivery/outbox/inbox 数据，保留原消息关联、ACK version/ADVANCED/PRIOR，不发Rabbit消息。gate启用不等于broker已实测；真实Rabbit仍NOT_RUN。
- 子进程env严格白名单；只给本fixture私有路径/工具链/public source binding；MySQL连接凭据仅Java私有pipe，不给Node或其他Agent，不继承生产datasource/Flow secrets/provider配置。secret、rta、rts不得进argv/env/report；Node由Java pipe获得本Agent合成secret，在内存调用原client。日志仅固定stage/status/计数/allowlisted类型。

## 4. MySQL 的最小真引擎接点（不是改UR04的URL）

### 4.1 原DDL和依赖

- Agent baseline：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-mapper/src/main/resources/db/schema.sql`；identity原加法/约束：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql`。identity upgrade不是空库全量baseline替代；以原MySQL语法和执行顺序装载，只处理隔离schema。
- 安装表：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-v1-schema.sql`：原 InnoDB/utf8mb4_0900_bin、BINARY(32) secret/auth摘要、安装和授权唯一键、scope/identity索引、status CHECK、version/消费时间。
- 四列fence：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql`：runtime_installation_id/runtime_host_id/runtime_instance_id VARCHAR(100) NULL，runtime_session_generation BIGINT NULL；不backfill旧行。
- 真实 initializer：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeV1SchemaInitializer.java`、`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSessionFenceSchemaInitializer.java`：真实 JDBC metadata 必须 MySQL；前者安装表existence检查不等于完整DDL一致性检查，后者真实 information_schema核四列type/nullability/length并处理并发add race。
- user baseline输入可复用 `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/user/jia-user-mapper/src/test/resources/db/schema.sql`（明确是原测试baseline），再按需执行原 `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/user/jia-user-mapper/src/main/resources/db/account-security-foundation-upgrade.sql` 的真实MySQL additive安全列脚本；同一连接的SET/PREPARE/EXECUTE语义需保持。不要复制UR04 H2 user小表再声称生产DDL跑过。无关OAuth/client迁移不纳入此最小fixture。
- `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/build.gradle:48` 已有 `testRuntimeOnly libs.mysql`；`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/plugin/jia-gradle-plugin/src/main/java/cn/jia/plugin/gradle/SharedDependencyManagementPlugin.java:27,217` 固定 Connector/J8.3.0。新opt-in sourceSet继承原 testImplementation/testRuntimeOnly 和 main.output即可复用driver；真实WS/user/chat的test-only依赖装配见原UR04 init38-64，不增加生产依赖/Provider模型bean。
- 现有 common-test为Testcontainers junit/rabbitmq，不存在已声明的MySQLContainer依赖或已证明可用Docker授权；不得假定直接用MySQLContainer就能跑。

### 4.2 真MySQL输入 / 期望 / 证据

| ID / 状态 | 真实接点 | 最小判定 |
|---|---|---|
| M1 / NOT_RUN | 私有真实MySQL baseline → 原 Runtime V1/fence initializers首次与重复执行 | JDBC metadata为MySQL，原安装表engine/collation/BINARY32/unique/CHECK由真实information_schema和负例证明；四nullable列精确匹配，预存synthetic legacy runtime行与NULL ownership保持；第二次初始化catalog/行不变。DDL有隐式提交，不能把DDL失败称为应用事务rollback。 |
| M2 / NOT_RUN | E1–E5在同一私有MySQL运行；Node defaultfetch → 原Spring/controller/auth/defaultDAO/mapper | 真实行锁消耗、生成安装授权、真实session和WS注册、Java A/B重启后DB连续性与旧代际拒绝。独立JDBC连接做committed状态对照，不用同事务连接读取冒充durability。 |
| M3 / NOT_RUN | 实际native filter → authentication.withFence → 原业务/D06 transaction；真实ACK重复/旧代际/撤销 | 原ADVANCED/PRIOR/lastConfirmedVersion不变；generation或authorization被拒绝时无业务/ACK变更；single-agent变更不影响sibling。原AgentCommandAckServiceImpl的TransactionTemplate与原Recovery DAO锁操作必须跑在同一真实MySQL事务。 |
| M4 / NOT_RUN（保持完整E05目标） | 原 prepared result、fresh commit fence、真实 lease/start/heartbeat → result提交 → GET原结果 → terminal ACK → Java/Node重启 | 不缩成只测auth/ACK；最终仍须原producer/material/checkpoint/lease proof、持久结果readback、结果未知不重跑、终态ACK PRIOR、prepared后代际变化拒绝及独立JDBC rollback。复用UR04原六例目标而非重做Owner全量。真SQL失败可在私有schema加仅synthetic范围的test-only BEFORE INSERT agent_task_event探针，对WORK_ITEM_SUBMITTED执行固定SIGNAL SQLSTATE45000，使原event DAO真实失败；无mockDAO/Supplier，不改生产DDL。比对work_item/artifact/event/ACK原行与版本，确认前序写入已rollback。该MySQL探针尚未实现/执行，不把H2 Trigger直接搬过去。 |

原事务接点：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandAckServiceImpl.java:45-60`；E05两次auth fence和真实GET：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentWorkItemRuntimeResultController.java:61-88`；原提交事务：`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentWorkItemResultCommitServiceImpl.java`。实际MySQL业务表须由原Agent schema和原transport/任务DDL建表，不能只建installation表就声称完成M4。

现有UR04 `Ur04E05HttpFixture.java:193-206` 预置ACTIVE和人工rta hash，`:582-590` 硬绑定H2-file，`:341-363` 使用org.h2.api.Trigger。其H2 SQL、SHUTDOWN、文件重启均不是MySQL证明。复用真实Tomcat/bean/private-pipe/透明response-cut设计可以；更换URL env不可以。MySQL不执行H2 SHUTDOWN；A/B仅重启owned Java，私有mysqld保持，若加DB重启只操作核验归属的私有进程。

## 5. 现成MySQL云入口：有selector，未核到可直接复用的私有Runtime入口

| 现有来源 | 能复用什么 / 不能声称什么 |
|---|---|
| `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentCommandTransportSchemaInitializerMySqlTest.java` | default test selector `cn.jia.agent.config.AgentCommandTransportSchemaInitializerMySqlTest`，D01_MYSQL_URL条件启用，原transport DDL/MySQL8.0.21、expected port/datadir guards；不是Runtime enroll/fence/WS闭环。 |
| `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentCommandOperationsMySqlTest.java` | default test selector `cn.jia.agent.service.impl.AgentCommandOperationsMySqlTest`；D09_MYSQL_URL/USER/PASSWORD/EXPECTED_PORT/DATADIR/VERSION；严格loopback、非3306/33060、真实server port和精确datadir。原mapper/DAO/事务场景可用作引擎guard参考，不是本次跨端认证fixture。 |
| `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentIdentityRuntimeMySqlTest.java` | default test selector `cn.jia.agent.service.impl.AgentIdentityRuntimeMySqlTest`；A08_MYSQL_URL、8.0.21，真实identityDAO；实例隔离guard弱于D09，不能直接指向共享DB。本报告不建议重跑这批旧基线。 |
| `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/scripts/run-d03-isolated-mysql.sh` | 已有owned mysqld/private datadir/socket/非host port及identity校验的源码设计；但自动本地Gradle并general-log=ON/复制原始日志，**不可直接用于含真enrollment credential的云验**。未执行。 |
| `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/scripts/run-d09-isolated-mysql.sh` | 较新的私有mysqld、严格实例guard、general-log=OFF、orchestrator/cache/selector契约；仍是本地Gradle runner、默认本机MySQL binaries/私有实例全库权限，不是已就绪Flow bootstrap。不将D03日志策略误说成D09也开启general log。未执行。 |
| `/home/isp/wsps/cyf/ops/ci/aliyun-flow/templates/backend-develop-release.yaml`、`/home/isp/wsps/cyf/ops/ci/aliyun-flow/templates/backend-develop-ci.yaml` | root固定HEAD `cd2c6ef361f6cccee9a83b2a678dac7d19f9320a` 的release模板83行已有D09 selector；工作文件已有他人未提交差异（selector在86行），未更改。定向检查tracked Flow ops/templates没有找到D01/D09/A08_MYSQL_*私有实例配置或mysqld provisioning。未查询实际云配置，不能排除主控另有外部资源。 |

**结论：当前无已核验、可直接复用的真实Runtime enroll/MySQL云端启动入口。** 有测试selector与本地私有启动源码，不等于云端MySQL实例/授权已准备好；env未提供时这些条件测试会skip，普通Run绿色和H2结果均不能抵扣MYSQL NOT_RUN。

主控补齐的最小前置（尚未授权本support操作）：固定私有MySQL8二进制/容器来源及版本与artifact证明、可启动环境、owned private datadir/socket/loopback端口、独立synthetic schema和限定凭据；父fixture先核server product/version/port/datadir归属后才建私有schema。可按既有8.0.21输入复用guard，不自创新资源硬门槛；不回落本机3306、jia/jia_dev、应用properties或共享DB。禁SQL/general/auth请求日志，证据只输出server version、port、datadir-verified布尔、DDL/source hash、阶段/计数；不上传私有paths/SQL/params/credential。结束仅清理本fixture实例/schema，不影响服务或他人任务。

## 6. 下一步接线边界（建议，未创建/claim/执行）

可由主控授权后另设独立opt-in测试族，不编辑两Owner文件或默认build.gradle：

1. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java`：parent identity/source/artifact/DB guards、E1–E5/M1–M3、owned Java A/B、独立JDBC证据。
2. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java`：私有MySQL连接、原production beans/DDL、PENDING准备、真实HTTP/WS、透明响应截断、安全private协议；如后续扩M4保留完整E05原链，另行明确非重叠归属。
3. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs`：实际RuntimeV1Client.enroll/defaultfetch/私有凭据读回、原host/adapter/engine/socket，完整paired source/C1–C4校验；不自造auth或替代executor。
4. `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle`：仅主API opt-in sourceSet继承test级依赖，实际runtimeClasspath交owned child、白名单env、无缓存复用；included plugin/buildSrc不注册。**此四路径不存在，selector/task尚未实现，不是可立即执行命令。**

拟任务 `:agent:jia-agent-service:ur06EnrollMysql` / selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest` 只能在主控提供固定paired source、干净完整artifact和私有MySQL前置、Writer实现后由正式Flow执行。当前可运行的原UR04任务来自 `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/ur04E05Http/ur04-e05-http.init.gradle`，任务 `:agent:jia-agent-service:ur04E05Http`，**不属于default test，且是H2不是MySQL**；主控原六selector保留，不被本报告替换。

前置未齐时可用真实两模块client默认fetch与MySQL先证明E1/E3/E4/E5，但只报阶段通过，E2真实WSready与完整E05/M4仍NOT_RUN；不得把最终整体验收目标缩成两模块或mock子集。当前完整artifact因C3/C4失败未获得；MySQL云入口未获得；本轮实际新增测试通过数 **0（未执行）**。

## 7. 与已有测试证据的严格区别

- `/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/runtime-v1.test.mjs` @374 的nested enrollment/private persistence/lost response/exclusive marker用例（270、299、313、353行等）是fake fetch单测，仅复用输入断言，不能证明server消费或defaultfetch。
- `/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/fixtures/unified-runtime-wire-v2.redacted.json` @374 可复用嵌套shape；REDACTED字段不得作为原服务issued authorization。
- `/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentRuntimeV1ServiceImplTest.java:30-37` mock安装/identity/sessionDAO；`/home/isp/wsps/worktrees/ur04-runtime-ci-integration-20261008/agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentRuntimeSessionFenceSchemaInitializerTest.java:20-28` mock JDBC metadata为MySQL：都不是本次真MySQL proof。
- 保持尚未跑的 ENROLL、MYSQL、真实installer管理JWT、真实Rabbit、Provider/Codex业务质量、production部署、原UR04未覆盖crash window/IO竞争各自未证，不因为本报告提出接点就变为通过。本任务不重复Owner全量，也不向上述lane发送真实请求。
