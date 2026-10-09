# UR05 生产收口详设：代码、配置、数据库与切流分别说明

核对时间：2026-10-09T15:48:12.903669+08:00（Asia/Shanghai）。任务 UR-05-20261008；唯一收口 Owner：Main。
本文件响应用户“具体到表字段和代码行”的要求，不是新框架/台账/验收成功回执。冻结功能范围，不新增Agent、不重复构建、不重建/点将/重放432、不操作433。

## 1. 结论与未完成项

**API功能修复、固定源码本地测试及制品已完成；整套单Runtime生产交付未完成。不能把尚未部署都叫“代码未开发完”，也不能凭单元测试宣布执行链已通。**
本次没有证据支持立即安排一套新产品功能开发。真正未闭合的是生产配置接线、有界schema应用、完整目标安装及精确切流；若沿既有路径发现必须修源码，回原Owner最小修改，不扩建检查框架。

| 项目 | 当前真实状态 | 剩余动作 / Owner |
|---|---|---|
| API功能源码/制品 | 固定118d；原正式XML统计见下；fresh bootJar/package完成 | Main复用精确证据，不再构建 |
| 本地准入与原installer | c58f修复系统解释器合法硬链接误拒；91准入单测PASS；六helper installed/source bytes一致 | 复用原入口，不另换installer |
| 制品准入 | 原installed wrapper真实发布 + 独立published verifier PASS | admission保持productionAuthorized=false；另立真实maintenance authority/decision |
| 命令生产接线 | **未完成**；只开outbox会是DB_SHADOW；ACK服务仍受Rabbit dispatch注册条件控制 | Main固定专用broker、五必要开关、精确allowed scope和在途影响范围 |
| 数据库 | **未应用**原13DDL；F06两表/E05一表已有只读等价证据 | Main真实备份、写排除、逐条应用/readback，禁止整库SQL重放 |
| 统一Runtime完整目标 | 801源码tar保留；不是生产安装制品 | Main走原完整installer和validator，不借宿主包 |
| 三Agent同host配置/切流 | **未实施**；本次读取unified目标/config不存在 | Main固定三subject独立凭据/状态，精确处理共享服务公孙胜及不同owner |
| 原432实测 | 未在候选生产版本执行 | 真发布后续验原432；结果/产物持久化与UI正确才算通过 |

### 固定基线

- API commit `118d909685c3c27d7ebb4ff16028e8b89ab8260c` / tree `c63106eaf53282d2bf11a4c094ed22bfeead58dd`。
- Root/helper commit `c58f13571ff19e40f7b9a91adc53e843e0fb1cd6` / tree `6dbabed4708b7a083ff7c6576f076d2f7ebcad5b`。
- Runtime commit `801087a8d7776f5d9ee72e9b35a8ddd2d014d721` / tree `594f63efe93403531bcd60160f5a326ceef39e39`。
- 版本 `1.14.0-ur05.20261009`；build ID `ur05-api-local-20261009T1345-cbnrgvam`。
- 原正式测试：`{'tests': 277, 'failures': 0, 'errors': 0, 'skipped': 0}`；不把排除/未执行测试记PASS。
- 候选JAR SHA `011dbb31b0f4352d16bf759d63e961a17038c0e3216e64eded2895e7d8b9ff42`。
- 包 `/var/tmp/cyf-ur05-api-local-20261009T1345-cbnrgvam/package/cyf-api-1.14.0-ur05.20261009-ur05-api-local-20261009T1345-cbnrgvam.tgz`；SHA `827327e62a3c014181f10bd3ae00938ad4c14d221ff3483d015bed3ee9cfcdcd`。
- 生产仍为canonical JAR SHA `54e6150b6cd6a3f0c72c9b1d495b60d9018a05d687f4fabbdb628d6643fe86b6`；PID225620 live；runtime record start_ticks2888023。没有停启/换JAR/DDL。
- 读取`cyf-api-kit.service`的inactive不能判API已停；它不是本次归属判据，以原kit runtime record/PID/cwd/-jar为准。

## 2. 命令接线详设：仅outbox=true不够

### 2.1 源码已实现链与行号

| 环节 | 固定代码行 | 实际行为 |
|---|---|---|
| writer/mailbox注册 | [AgentCommandTransportWriterConfiguration.java:18–38](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandTransportWriterConfiguration.java#L18) | outbox启用才有writer和mailbox查询；mailbox不是领取/执行接口 |
| assignment捕获 | [AgentCommandTransportCapture.java:57–105](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandTransportCapture.java#L57) | 认证owner写命令；缺writer报错；返回dispatch允许状态 |
| writer admission | [AgentCommandTransportWriterImpl.java:267–275](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandTransportWriterImpl.java#L267) | DB_SHADOW/MQ_SHADOW不可执行；精确scope才eligible |
| gate依赖 | [AgentRabbitSafetyGate.java:75–110](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitSafetyGate.java#L75) | dispatch要求outbox/topology/publish/consume与非空allowedScopes |
| 原consumer | [AgentCommandRabbitConsumer.java:41](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandRabbitConsumer.java#L41)、[AgentCommandRabbitConsumer.java:102–145](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandRabbitConsumer.java#L102) | Rabbit listener，拒绝scope外命令 |
| ACK Bean | [AgentCommandRecoveryConfiguration.java:17–50](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandRecoveryConfiguration.java#L17) | agent.rabbit-dispatch.enabled=true才注册原ACK/reissue/reconnect |
| Runtime HTTP ACK | [AgentRuntimeV1ServiceImpl.java:156–190](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentRuntimeV1ServiceImpl.java#L156) | session/fence后找ACK Bean；缺失报Runtime v1 command ACK is unavailable |
| ACK权限/持久化 | [AgentCommandAckServiceImpl.java:50–105](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandAckServiceImpl.java#L50) | gate先验dispatch scope，事务锁+CAS推进；挪Bean也不能绕gate |
| Runtime执行回报 | [execution-adapter.mjs:23–50](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L23)、[execution-adapter.mjs:86–100](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L86) | session WS接命令、HTTP ACK提交；心跳sidecar不是执行完成 |

**以上是源码静态链证据，不是已经实测该配置下的生产ACK。** 原逻辑具备，不证明需要新增dispatcher/ACK实现；先补现有配置输入。没有合法专用broker输入则明确缺它，不借spring.rabbitmq、其他owner凭据或绕gate。

### 2.2 具体配置（设计，尚未写入）

外部文件：`/home/isp/hosts/cyf/api/application.properties`；原before字节保存在same-JAR证据操作目录。
候选prod defaults：[application-prod.properties:215–222](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/starter/src/main/resources/application-prod.properties#L215)。

| 属性 | 当前已知输入 | 执行目标 / 边界 |
|---|---|---|
| agent.command-outbox.enabled | 候选prod216=false，外部无覆盖 | true，只开此项是DB_SHADOW |
| agent.rabbit-topology.enabled | 候选默认false | 现有命令链目标true；必须绑定专用broker和topology |
| agent.rabbit-publish.enabled | 候选默认false | 目标true |
| agent.rabbit-consume.enabled | 候选默认false | 目标true |
| agent.rabbit-dispatch.enabled | 候选默认false | 目标true，需精确allowed-scopes |
| agent.rabbit-dispatch.allowed-scopes[0].tenant-id | 未固定 | 字符串0，无通配 |
| agent.rabbit-dispatch.allowed-scopes[0].client-id | 未固定 | jiafewnnv58ec2379c；同client其他主体也受gate影响，须纳入在途边界，不宣称只影响三Agent |
| agent.rabbit-broker.host/port/username/password/virtual-host | 本轮未固定/验证 | M3独立broker，vhost不得为/；合法来源、权限和topology核实；password不进文档/日志 |
| agent.rabbit-operations.read.enabled | 候选默认false | 保持false，不新增管理入口 |
| agent.rabbit-operations.redrive.enabled | 候选默认false | 保持false，不手工redrive/reissue432 |
| chat.typed-deliberation.enabled | 外部100=true | 保持true |
| cyf.chat.deliberation-schema.allow-additive-migration | 外部99=true | false，先完整catalog核对，不能以关闭迁移藏漂移 |
| cyf.chat.typed-deliberation-schema.allow-additive-migration | 外部101=true | false，先typed完整catalog/ACTION_REQUEST核对 |
| chat.bounty-bootstrap.enabled | 外部106=true | 保持true；原relay租约/重试真观察，不另发432 |

键名用源码`agent.rabbit-dispatch`，不改成`agent.rabbit.dispatch`。属性/独立broker合同：[AgentRabbitSafetyProperties.java:7–23](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitSafetyProperties.java#L7)、[AgentRabbitSafetyProperties.java:75–86](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRabbitSafetyProperties.java#L75)。
步骤：原值备份+SHA → 固定候选所有必要输入 → 核CLI/env/secret优先级 → 发布沿原外部配置安装 → 实际startup/gate/consumer/ACK/readiness readback。写了true、broker连通或class存在都不等于运行READY。

## 3. 数据库：原13条有界DDL，表字段全部列在附录A

原真实全catalog采集：219表、3404列、2082索引、853约束、354 CHECK、71 FK、37 trigger，MySQL8.0.21。采集≠全库等价≠写排除≠备份。
F06两表/E05一表由原installed helper真实catalog比较equivalent；root只读查询不是application principal已执行CREATE证明。

### 3.1 六条既有表调整

| 对象 | 已观测生产状态 | 目标 | 源码行 |
|---|---|---|---|
| agent_hosted_profile | tenant已NOT NULL，现3 CHECK | 加chk_hosted_single_tenant (tenant_id='0')，最终四CHECK | [AgentSchemaInitializer.java:221–255](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java#L221) |
| agent_persona_binding.tenant_id | VARCHAR(50)，nullable，default0；旧chk_agent_binding_tenant_owner | VARCHAR(50) NOT NULL DEFAULT '0'；同一ALTER DROP旧CHECK、收紧列、ADD chk_agent_binding_single_tenant | [schema.sql:55–90](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/schema.sql#L55)、[AgentSchemaInitializer.java:123–169](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java#L123) |
| agent_runtime.runtime_installation_id | 列ABSENT，非行NULL | VARCHAR(100) NULL | [agent-runtime-session-fence-v1.sql:2](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql#L2) |
| agent_runtime.runtime_host_id | 列ABSENT | VARCHAR(100) NULL | [agent-runtime-session-fence-v1.sql:3](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql#L3) |
| agent_runtime.runtime_instance_id | 列ABSENT | VARCHAR(100) NULL | [agent-runtime-session-fence-v1.sql:4](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql#L4) |
| agent_runtime.runtime_session_generation | 列ABSENT | BIGINT NULL | [agent-runtime-session-fence-v1.sql:5](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql#L5) |

不owner推断/业务DML回填，不SQL清fence；新增后的旧行NULL是执行未就绪，走原session事务建立真实fence。

### 3.2 D06五表/两trigger（实际均ABSENT）

| 表 | 完整字段/索引定义源码 | 必须保留的约束 |
|---|---|---|
| agent_command_delivery | [agent-command-transport-schema.sql:6–42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L6) | owner_jiacn VARCHAR(50) NOT NULL；uk_delivery_command=(tenant_id,client_id,owner_jiacn,command_id)；tenant/owner CHECK |
| agent_outbox_event | [agent-command-transport-schema.sql:44–88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L44) | MEDIUMBLOB wire + BINARY(32) SHA；原event/message/delivery/command索引 |
| agent_consumer_inbox | [agent-command-transport-schema.sql:90–124](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L90) | uk_consumer_message=(tenant_id,client_id,consumer_name,message_id)；原lease/active_attempt/version |
| agent_command_operation_audit | [agent-command-transport-schema.sql:126–157](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L126) | append-only REQUEST/RESULT，唯一(operation_id,phase)，两不可变trigger |
| agent_command_redrive_operation | [agent-command-transport-schema.sql:164–196](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L164) | 两STORED生成列，guard唯一索引、CAS version、原ENUM |

生成列：disposition_guard=IF(outcome_state='PENDING',1,NULL)；redrive_guard=IF(settlement_state IN ('SOURCE_REQUEUED','NOT_ACQUIRED'),NULL,1)，源184–185。
owner_jiacn并非五表都有；不虚构给outbox/inbox/audit/redrive加owner。原delivery/scope校验保留。
两CREATE trigger见[agent-command-transport-schema.sql:201–211](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L201)；**禁止执行**资源[agent-command-transport-schema.sql:198–199](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L198)的两DROP TRIGGER。
D06 initializer表集合/完整catalog：[AgentCommandTransportSchemaInitializer.java:44–78](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandTransportSchemaInitializer.java#L44)；trigger缺失才CREATE、漂移拒绝：[AgentCommandTransportSchemaInitializer.java:459–480](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandTransportSchemaInitializer.java#L459)。

### 3.3 迁移和失败恢复的实际步骤

1. 固定同JAR资源/SQL SHA；临维护复核binding非法tenant/duplicate、hosted tenant和受影响完整catalog，不用DML“修成可过”。
2. 原发布互斥+精确写排除；备份schema/data、外部config、oldJAR、安装记录。文件锁不自动排除DB/旧Agent写。
3. 原13条按授权顺序，每条缺失才应用、已存在必须精确等价；保存statementSHA/执行结果/catalog readback。DDL不能宣称13条整体事务可回滚。
4. 部分失败保留真实结果，归因后只恢复未完成项；不DROP新增表、不清业务行、不重置fence/队列。
5. binding收紧后旧JAR会重加旧CHECK，不能盲退旧JAR。固定发布采取forward-only，原处理[cyf-api-flow-install:1110–1117](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-install#L1110)保留candidate/失败record，向前修复。
6. AgentSchemaInitializer有DROP trigger方法，但本次已有identity表/保护trigger条件决定分支；[AgentSchemaInitializer.java:894–899](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java#L894)。不能只因方法存在就称启动必DROP，也不能未经catalog核实忽略它。

## 4. 原发布入口已实现，Main仍需补真实输入

原source/installed一致，不能再建runner或伪造proof：schemaPlan [cyf-api-flow-deploy:1329–1365](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-deploy#L1329)；authority/decision [cyf-api-flow-deploy:1382–1424](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-deploy#L1382)；四proofrefs [cyf-api-flow-deploy:1186–1187](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-deploy#L1186)；read-only inspect [cyf-api-flow-deploy:1856–1909](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-deploy#L1856)；generation实证 [cyf-api-flow-deploy:1945–1971](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-deploy#L1945)；local install [cyf-api-flow-deploy:2396–2458](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-deploy#L2396)；原installer顺序 [cyf-api-flow-install:1278–1319](/home/isp/wsps/worktrees/ur05-root-develop-integration-20261009T1413/ops/ci/aliyun-flow/host/cyf-api-flow-install#L1278)。

| 必须输入 | 已有材料 | 未完成动作（Main） |
|---|---|---|
| startupCatalogProof | 同JAR10资源、38候选startup类和registrar/条件；全metadata | 按真实启用initializer/callsite核对受影响catalog/副作用；38存在不等于38启用或PASS，不给无关类扩门禁 |
| effectiveConfiguration | 外部原字节、候选defaults | 冻结§2完整配置输入/优先级/合法broker及scope，实际发布readback，不把推导写成live值 |
| applicationPrincipalProof | 原PID-owned JDBC socket/processlist对应jia；元数据grant含CREATE/ALTER/INDEX/TRIGGER等 | 绑定候选真实datasource/权限/trigger definer；root SHOW/用户名存在不是实际应用连接DDL成功 |
| boundedSchemaReceipt | 原13SQL+摘要；尚无应用结果 | 按§3备份/执行/readback形成真实回执，不能写假PASS JSON |
| identity/inflight/schemaInventory | 历史精确scope图、较新DB投影 | 临切流更新并处理非零在途/公孙胜共享scope；数据库计数不是内存/broker排空 |
| maintenance authority/install decision | 用户已直接授权固定API/helper/13DDL/备份恢复 | 上述实情闭合后按原结构固定root保护输入；admission保持false，不扩大其他owner转移权限 |

`local-inspect`只核输入完整性，不自己queryDB/配置/Runtime；Main不得用其exit0替代真正维护前置。
满足事实后用原入口，以下为命令模板而非已执行记录：

```text
/usr/local/sbin/cyf-api-flow-deploy --local-inspect --decision <actual-root-protected-decision> --decision-sha256 <actual-sha>
/usr/local/sbin/cyf-api-flow-deploy --local-install --decision <same-decision> --decision-sha256 <same-sha>
```

完成要求installed record、canonical候选SHA、新PID/-jar/cwd、健康和schema结果匹配；installer成功不是原432业务成功。

## 5. 单Runtime三Agent的具体交付配置

### 5.1 目录/进程（设计，未安装/启用）

- 单artifact：`/home/isp/apps/cyf-agent-runtime-v1/unified`；单unit `cyf-agent-runtime-v1@unified.service`。
- host config：`/etc/cyf-agent-runtime-v1/unified.host.json`；env `/etc/cyf-agent-runtime-v1/unified.conf`。
- host state：`/home/isp/state/cyf-agent-runtime-v1/unified/host`。
- subject sibling roots：`/home/isp/state/cyf-agent-runtime-v1/unified/agents/<subjectSHA>/{state,codex-home,work,chat-work}`。
- 每subject manifest/profile：`/etc/cyf-agent-runtime-v1/agents/<subjectSHA>/{manifest.json,profile.json}`。
- subjectSHA由原[manifest.mjs:44–46](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L44)对stableJson(tenantId,clientId,canonicalAgentId)取完整SHA，不persona简称/hash截断。
- 单host lifetime、多独立executor/session/socket/credential/checkpoint：[agent-runtime.mjs:38–58](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L38)。同进程不等于凭据合并。
- 原unit validate/run：[cyf-agent-runtime-v1@.service:8–15](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/systemd/cyf-agent-runtime-v1@.service#L8)。永久错误78不启动重启循环。

host文件只允许以下keys，所有paths必须绝对、规范、无symlink、跨subject可变root不重叠；[manifest.mjs:100–131](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L100)：

```json
{
  "configVersion": 1,
  "hostId": "<explicitly-fixed-host-id>",
  "stateRoot": "/home/isp/state/cyf-agent-runtime-v1/unified/host",
  "agents": [
    {"manifestPath": "<wuyong-absolute>", "profilePath": "<wuyong-absolute>", "stateRoot": "<wuyong-state>"},
    {"manifestPath": "<linchong-absolute>", "profilePath": "<linchong-absolute>", "stateRoot": "<linchong-state>"},
    {"manifestPath": "<lujunyi-absolute>", "profilePath": "<lujunyi-absolute>", "stateRoot": "<lujunyi-state>"}
  ]
}
```

### 5.2 身份（历史inventory，临切流重新核实）

| 主体 | canonicalAgentId | installationId | binding / owner边界 |
|---|---|---|---|
| 吴用 | `jyt-jiafewnnv58ec2379c-wuyong` | `rti_c75650221caf8b339602a0ad010a2e5b` | 1 / 原本人owner |
| 林冲 | `jyt-jiafewnnv58ec2379c-linchong` | `rti_1afdba9aa03d1d9fc42df7dff3ae5b5a` | 2 / 与吴用同owner |
| 卢俊义 | `jyt-jiafewnnv58ec2379c-lujunyi` | `rti_82d08529b37084c6b9399414b5d0061b` | 5 / 不同于吴用owner |

三subject tenant=0 / client=jiafewnnv58ec2379c。复用真实manifest并核绑定：required runtimeProtocolVersion、manifestVersion、installationId、tenantId、clientId、canonicalAgentId、manifestSha256；原digest排除自己，[manifest.mjs:4–30](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L4)。不造hash、不SQL清fence/revoke/transfer。
每profile固定profileId/agentId/codexBin/codexHome/codexWorkdir/chatWorkdir/workspacePolicyId；每主体原合法model/provider权限独立。
CHAT目标：typedDeliberationEnabled=true、appServerEnabled=true、fastChatEnabled=true、chatEngine=app-server、chatSandbox=read-only、chatToolPolicy=read-only-constrained；真实CLI/schema须匹配，原READY条件 [juyiting-typed-outcome.mjs:191–212](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/codex-ws-agent/juyiting-typed-outcome.mjs#L191)。
TASK workspacePolicyId命中原policyMap，工作区真实创建 [agent-client.mjs:6092–6099](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/codex-ws-agent/agent-client.mjs#L6092)。S01 policyFile→env型loader已修 [agent-runtime.mjs:78–79](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L78)，不是待开发。
profile禁止legacy API key/runtime凭据明文 [manifest.mjs:59–65](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L59)；授权状态/enrollment沿原受控通道，禁止三个subject共享token。

### 5.3 完整安装 / Python状态纠正

- 原唯一installer wrapper [cyf_agent_runtime_v1_install.sh:13–15](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/shell/cyf_agent_runtime_v1_install.sh#L13)；原installer [install.sh:35–61](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/install.sh#L35)；validator [validate.sh:18–35](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/validate.sh#L18)。
- Node20.20.2、Python3.11.13；npmci、release-local venv和全requirements不删。pins：python-docx0.8.11/python-pptx0.6.23/openpyxl3.1.3/Pillow10.4.0/PyPDF2 1.28.6/reportlab3.6.13；保留完整import/ABI/六格式验证，不借宿主包。
- 原7594安装已结束FAIL：Pillow8.4源码build缺jpeg；不是仍live，也不能说换镜像就修复。后续pyvenv.cfg staging provenance修复已在源码 [install.sh:78–106](/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/install.sh#L78)，不把旧cfg失败说成801缺代码。
- 5666批次core C1–C4实际PASS但consumer总体FAIL，fixture root已清；不是801生产安装已完成。021133 install-receipt本次为空，只能记无有效finalreceipt，不能推测进程状态。
- 801 retained源码tar SHA `8e350395752f1d4163efa1eba84f18537d459bdebda739e058c930acb0d0570a`，不当已安装制品。后续沿原installer装真实目标及原validator，不重复用户拒绝的额外隔离业务验收。
- 当前global pip源是用户授权HTTPS清华；项目专用env已删除。新batch实际解析默认、固定URL/configSHA，显式安装env映射；不声称旧在途输入换源，保持TLS/隔离venv-cache，不trusted-host、不混extra-index。

## 6. 旧服务切流与在途详设

| 旧入口 | scope | 未完成处置 |
|---|---|---|
| codex-ws-agent@wuyong-local.service | 吴用旧WS | 切流前核精确PID/cgroup/队列/在途；有该主体明确权限才优雅停旧入口，保留ledger/checkpoint |
| cyf-agent-runtime-v1@wuyong.service | 吴用旧HTTP-only sidecar | 与吴用WS同subject纳入切流，不把它报成新统一执行runtime |
| codex-ws-agent.service | 林冲/卢俊义direct + managed公孙胜 | **不能整停**；先原可用定向停止/保留公孙胜方案，或另有准确授权的scope拆分；不影响433/RECOVERY_REQUIRED。若原路径不能完成，回原Owner最小scope拆分详设，不假称配置够用 |

非零在途不是强制清零：区分未admit、RECEIVED、durably STARTED、WAITING_AGENT、终态，按原幂等/sessionfence/恢复合同处理，不kill/reset/replay。
原吴用同command root ledgerFAILED与instance SUCCEEDED矛盾保留，不改账，也不据此断言必然重复执行。
新session若发现既有installation/host不一致按原拒绝路径停该主体激活，明确缺转移权限/支持路径；不预先开发未证明必要的新转移接口或SQL清fence。
新host每subject唯一ACTIVE执行入口，registration ACK、durable state和实际CLI/schema ready成立，才可报切流成功。

## 7. Main连续执行次序与完成标准

1. 冻结§2真实配置/合法专用broker/allowed scope和旧共享服务影响范围；不等已完成子Agent。
2. 复用同JAR与匹配catalog证据，定向补启用initializer/callsite/principal事实；不扩framework或每切片跑全套。
3. 原锁/备份/写排除下原13DDL逐项执行/readback，产出真实有界结果。
4. 真authority/decision→原local-inspect→原local-install；同batch候选installed、新PID/-jar/cwd/SHA/健康正确；失败forward-only。
5. 原801完整目标安装/原validator/真CLI-schema-profile验证，非tar存在或pip成功即可。
6. 按精确subject方案切入三Agent单host；旧重复入口退役，公孙胜/433与不同owner不越权。
7. 真发布后续验原432，typed真实READY、原relay推进、命令RECEIVED→STARTED→终态提交、业务结果/产物持久化、UI不残留错误出征；不新建任务冒充通过。

开发完成、安装完成、健康通过、业务实测通过四个状态分开；本文件不把任何一个待执行项标为已完成。
本次没有可比生产耗时数据，不给“再等十分钟”虚假保证。真正阻塞要列缺输入、Main/原Owner与下一动作，不用巡检替代开发。

## 8. 原证据入口

- handoff：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/main-handoff.json`。
- 同批package/正式XML：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-actual-local-package-main-readback.json`；旧NOT_ADMITTED状态由后续真实证据推进，不改旧回执。
- 真实admission：`/var/lib/cyf-api-local-admission/admitted/ur05-api-local-20261009T1345-cbnrgvam/admission.json`；SHA `ef65572d7de7311ef8756dc6d7144974967bcb5474ea560f94d772bdd505da79`。
- verifier：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-actual-published-admission-verification-output.json`。
- 全catalog/F06E05：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-actual-full-catalog-existing-f06-e05-readback.json`。
- 同JAR/startup/config：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-same-jar-resource-startup-config-input-readback.json`。
- 用户已授权：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-user-explicit-operation-authorization-20261009T1421.json`；旧request的not-approved历史名不能覆盖已授权事实。
- 原13SQL plan：`/var/tmp/ur04-production-schema-minimal-plan-20261009.json`。

本轮补充只读实证：2026-10-09 15:49（Asia/Shanghai），canonical PID225620/start_ticks2888023及旧JAR摘要未变；进程相关env/CLI与外部application.properties未见显式Rabbit/outbox输入（不推定其他import绝对不存在）；unified目标/config仍不存在；D06五表/两trigger及runtime四fence列仍ABSENT，binding旧CHECK及nullable状态、hosted三CHECK保持。证据：

- `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-command-wiring-targeted-config-input-readback.json`
- `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/production-readback-20261009/UR05-closeout-fresh-minimal-schema-readback.json`

## 附录A：原13条完整SQL（尚未执行）

从原plan逐字提取；每条SHA与原授权request及118d对应resourceSHA已核对。包含五表全部字段类型/null/default/索引/CHECK/生成列及两trigger。不直接批量执行跳过逐条前后置/备份。

### A.1 hosted-fourth-check

Statement SHA-256：`7af08350f0ee84d75ccd8f2938357f97ff96e67910a2d5185b31020937bb78ae`

```sql
ALTER TABLE agent_hosted_profile ADD CONSTRAINT chk_hosted_single_tenant CHECK (tenant_id = '0');
```

### A.2 binding-single-contract

Statement SHA-256：`0f6a727b8c35a2e36c0034eb078ff840b4840371a6bf0da104d53f86a6645084`

```sql
ALTER TABLE agent_persona_binding DROP CHECK chk_agent_binding_tenant_owner, MODIFY COLUMN tenant_id VARCHAR(50) NOT NULL DEFAULT '0' COMMENT 'Single tenant scope; always 0', ADD CONSTRAINT chk_agent_binding_single_tenant CHECK (tenant_id = '0');
```

### A.3 nullable-fence-add-1

Statement SHA-256：`d7eeb776b8ce0a0c941f148256939cd36c51559db7d49df3f5bcc918f65999c2`

```sql
ALTER TABLE agent_runtime ADD COLUMN runtime_installation_id VARCHAR(100) NULL;
```

### A.4 nullable-fence-add-2

Statement SHA-256：`25f3ba0af6966554f27a9a7cd87a0190208a7b3a0c9f493d3768e432c000564e`

```sql
ALTER TABLE agent_runtime ADD COLUMN runtime_host_id VARCHAR(100) NULL;
```

### A.5 nullable-fence-add-3

Statement SHA-256：`fe4e6a15df1db18f55c2968cfc0af20e91f4f0ac4fc3d648567e0047fef3f5c9`

```sql
ALTER TABLE agent_runtime ADD COLUMN runtime_instance_id VARCHAR(100) NULL;
```

### A.6 nullable-fence-add-4

Statement SHA-256：`dc4394cdd191c0a4ebc2d205972d9ef3a1c1b2dcf6caceb682033f13efd951dc`

```sql
ALTER TABLE agent_runtime ADD COLUMN runtime_session_generation BIGINT NULL;
```

### A.7 d06-agent_command_delivery

Statement SHA-256：`c80705456d83963a2dc1d5ddac75fa7de60f64314e11df028cb797d1a7055f23`

```sql
CREATE TABLE IF NOT EXISTS agent_command_delivery (
    id                          BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    command_id                  VARCHAR(100) NOT NULL COMMENT 'Stable business intent idempotency key',
    owner_jiacn                 VARCHAR(50) NOT NULL COMMENT 'Authenticated command owner; never inferred from task or Agent identity',
    task_id                     VARCHAR(100) NOT NULL COMMENT 'Scoped task ID',
    work_item_id                VARCHAR(100) DEFAULT NULL COMMENT 'Optional scoped work item ID',
    target_agent_id             VARCHAR(100) NOT NULL COMMENT 'Exact canonical target Agent ID',
    command_type                VARCHAR(64) NOT NULL COMMENT 'Frozen Agent command type',
    command_payload             MEDIUMBLOB NOT NULL COMMENT 'Canonical business command payload bytes',
    command_payload_hash        BINARY(32) NOT NULL COMMENT 'SHA-256 of command_payload bytes',
    status                      VARCHAR(32) NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING/PUBLISHED/CONSUMED/SENT/RECEIVED/STARTED/SUCCEEDED/WAITING_AGENT/RETRY/FAILED/EXPIRED/DEAD',
    attempt_count               INT NOT NULL DEFAULT 0 COMMENT 'Transport issue/reissue attempt count',
    next_retry_at               BIGINT DEFAULT NULL COMMENT 'Next eligible retry epoch millis',
    lease_owner                 VARCHAR(100) DEFAULT NULL COMMENT 'Current scanner/dispatcher lease owner',
    lease_until                 BIGINT DEFAULT NULL COMMENT 'Lease expiry epoch millis',
    active_message_id           VARCHAR(100) DEFAULT NULL COMMENT 'Current transport message fence',
    active_attempt              INT NOT NULL DEFAULT 0 COMMENT 'Current transport attempt fence',
    expires_at                  BIGINT NOT NULL COMMENT 'Command expiry epoch millis',
    last_error                  VARCHAR(2000) DEFAULT NULL COMMENT 'Last bounded transport error',
    version                     BIGINT NOT NULL DEFAULT 0 COMMENT 'CAS version',
    replay_parent_message_id    VARCHAR(100) DEFAULT NULL COMMENT 'Parent transport message for controlled replay',
    replay_requester_id         VARCHAR(100) DEFAULT NULL COMMENT 'Replay requester identity',
    replay_approver_id          VARCHAR(100) DEFAULT NULL COMMENT 'Replay approver identity',
    replay_reason               VARCHAR(1000) DEFAULT NULL COMMENT 'Audited replay reason',
    tenant_id                   VARCHAR(50) NOT NULL COMMENT 'Single tenant literal 0',
    client_id                   VARCHAR(50) NOT NULL COMMENT 'OAuth/API client scope',
    create_time                 BIGINT DEFAULT NULL COMMENT 'Create time',
    update_time                 BIGINT DEFAULT NULL COMMENT 'Update time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_delivery_command (tenant_id, client_id, owner_jiacn, command_id),
    KEY idx_delivery_retry (status, next_retry_at, expires_at, id),
    KEY idx_delivery_lease (status, lease_until, id),
    KEY idx_delivery_agent (tenant_id, client_id, owner_jiacn, target_agent_id, status, next_retry_at, id),
    KEY idx_delivery_active_message (tenant_id, client_id, owner_jiacn, active_message_id, active_attempt),
    CONSTRAINT chk_delivery_single_tenant CHECK (tenant_id = '0'),
    CONSTRAINT chk_delivery_owner_nonempty CHECK (OCTET_LENGTH(owner_jiacn) BETWEEN 1 AND 50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin COMMENT='Durable Agent command mailbox and business intent state';
```

### A.8 d06-agent_outbox_event

Statement SHA-256：`02cd0fb8ebed7ac7161bb6d646211a314a286dc8feb5b521c6f2c651ee0386a1`

```sql
CREATE TABLE IF NOT EXISTS agent_outbox_event (
    id                          BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    event_id                    VARCHAR(100) NOT NULL COMMENT 'Stable identity of this outbox row',
    message_id                  VARCHAR(100) NOT NULL COMMENT 'Transport key; preserved for broker redrive and replaced for reissue',
    command_id                  VARCHAR(100) NOT NULL COMMENT 'Stable business intent idempotency key',
    delivery_id                 BIGINT NOT NULL COMMENT 'Related delivery row ID without database FK',
    aggregate_type              VARCHAR(30) NOT NULL COMMENT 'Source aggregate type',
    aggregate_id                VARCHAR(100) NOT NULL COMMENT 'Source aggregate ID',
    destination                 VARCHAR(100) NOT NULL COMMENT 'Logical exchange/destination',
    routing_key                 VARCHAR(100) NOT NULL COMMENT 'Exact Rabbit routing key',
    wire_payload                MEDIUMBLOB NOT NULL COMMENT 'Byte-exact broker wire payload',
    wire_payload_hash           BINARY(32) NOT NULL COMMENT 'SHA-256 of wire_payload bytes',
    status                      VARCHAR(32) NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING/CLAIMED/PUBLISHED/RETRY/FAILED/EXPIRED/DEAD',
    attempt_count               INT NOT NULL DEFAULT 0 COMMENT 'Publish attempt count',
    next_retry_at               BIGINT DEFAULT NULL COMMENT 'Next eligible publish epoch millis',
    lease_owner                 VARCHAR(100) DEFAULT NULL COMMENT 'Current relay lease owner',
    lease_until                 BIGINT DEFAULT NULL COMMENT 'Relay lease expiry epoch millis',
    active_attempt              INT NOT NULL DEFAULT 0 COMMENT 'Current transport issue/reissue attempt fence',
    expires_at                  BIGINT NOT NULL COMMENT 'Wire message expiry epoch millis',
    publisher_confirm_status    VARCHAR(20) NOT NULL DEFAULT 'NONE' COMMENT 'NONE/PENDING/ACK/NACK/TIMEOUT',
    confirmed_at                BIGINT DEFAULT NULL COMMENT 'Publisher confirm completion epoch millis',
    confirm_error               VARCHAR(2000) DEFAULT NULL COMMENT 'Publisher confirm failure detail',
    mandatory_return_status     VARCHAR(20) NOT NULL DEFAULT 'NONE' COMMENT 'NONE/PENDING/RETURNED/NOT_RETURNED',
    returned_at                 BIGINT DEFAULT NULL COMMENT 'Mandatory return epoch millis',
    return_reply_code           INT DEFAULT NULL COMMENT 'Rabbit mandatory return reply code',
    return_reply_text           VARCHAR(1000) DEFAULT NULL COMMENT 'Rabbit mandatory return reply text',
    published_at                BIGINT DEFAULT NULL COMMENT 'Durable published disposition epoch millis',
    last_error                  VARCHAR(2000) DEFAULT NULL COMMENT 'Last bounded relay error',
    version                     BIGINT NOT NULL DEFAULT 0 COMMENT 'CAS version',
    replay_parent_message_id    VARCHAR(100) DEFAULT NULL COMMENT 'Parent transport message for controlled replay',
    replay_requester_id         VARCHAR(100) DEFAULT NULL COMMENT 'Replay requester identity',
    replay_approver_id          VARCHAR(100) DEFAULT NULL COMMENT 'Replay approver identity',
    replay_reason               VARCHAR(1000) DEFAULT NULL COMMENT 'Audited replay reason',
    tenant_id                   VARCHAR(50) NOT NULL COMMENT 'Owner jiacn scope',
    client_id                   VARCHAR(50) NOT NULL COMMENT 'OAuth/API client scope',
    create_time                 BIGINT DEFAULT NULL COMMENT 'Create time',
    update_time                 BIGINT DEFAULT NULL COMMENT 'Update time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_outbox_event_id (tenant_id, client_id, event_id),
    KEY idx_outbox_publish (status, next_retry_at, expires_at, id),
    KEY idx_outbox_lease (status, lease_until, id),
    KEY idx_outbox_message (tenant_id, client_id, message_id),
    KEY idx_outbox_delivery (tenant_id, client_id, delivery_id, status, id),
    KEY idx_outbox_command (tenant_id, client_id, command_id, create_time, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin COMMENT='Transactional Agent command outbox with byte-exact wire payload';
```

### A.9 d06-agent_consumer_inbox

Statement SHA-256：`a1acce86c05e6b4092f5db11194bfd0181dfbf3e5c3f0663876be40b8e36a6a2`

```sql
CREATE TABLE IF NOT EXISTS agent_consumer_inbox (
    id                          BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    consumer_name               VARCHAR(100) NOT NULL COMMENT 'Stable logical consumer name',
    message_id                  VARCHAR(100) NOT NULL COMMENT 'Transport idempotency key',
    event_id                    VARCHAR(100) NOT NULL COMMENT 'Source outbox row identity',
    command_id                  VARCHAR(100) NOT NULL COMMENT 'Stable business intent idempotency key',
    delivery_id                 BIGINT NOT NULL COMMENT 'Related delivery row ID without database FK',
    wire_payload                MEDIUMBLOB NOT NULL COMMENT 'Byte-exact consumed wire payload',
    wire_payload_hash           BINARY(32) NOT NULL COMMENT 'SHA-256 of wire_payload bytes',
    status                      VARCHAR(32) NOT NULL DEFAULT 'RECEIVED' COMMENT 'RECEIVED/PROCESSING/PROCESSED/WAITING_AGENT/RETRY/FAILED/EXPIRED/DEAD',
    result_status               VARCHAR(32) DEFAULT NULL COMMENT 'Durable prior processing result for duplicate delivery',
    attempt_count               INT NOT NULL DEFAULT 0 COMMENT 'Consumer processing attempt count',
    next_retry_at               BIGINT DEFAULT NULL COMMENT 'Next eligible processing epoch millis',
    lease_owner                 VARCHAR(100) DEFAULT NULL COMMENT 'Current consumer lease owner',
    lease_until                 BIGINT DEFAULT NULL COMMENT 'Consumer lease expiry epoch millis',
    active_attempt              INT NOT NULL DEFAULT 0 COMMENT 'Current consumer attempt fence',
    expires_at                  BIGINT NOT NULL COMMENT 'Wire message expiry epoch millis',
    processed_at                BIGINT DEFAULT NULL COMMENT 'Durable processing completion epoch millis',
    last_error                  VARCHAR(2000) DEFAULT NULL COMMENT 'Last bounded consumer error',
    version                     BIGINT NOT NULL DEFAULT 0 COMMENT 'CAS version',
    replay_parent_message_id    VARCHAR(100) DEFAULT NULL COMMENT 'Parent transport message for controlled replay',
    replay_requester_id         VARCHAR(100) DEFAULT NULL COMMENT 'Replay requester identity',
    replay_approver_id          VARCHAR(100) DEFAULT NULL COMMENT 'Replay approver identity',
    replay_reason               VARCHAR(1000) DEFAULT NULL COMMENT 'Audited replay reason',
    tenant_id                   VARCHAR(50) NOT NULL COMMENT 'Owner jiacn scope',
    client_id                   VARCHAR(50) NOT NULL COMMENT 'OAuth/API client scope',
    create_time                 BIGINT DEFAULT NULL COMMENT 'Create time',
    update_time                 BIGINT DEFAULT NULL COMMENT 'Update time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_consumer_message (tenant_id, client_id, consumer_name, message_id),
    KEY idx_inbox_retry (status, next_retry_at, expires_at, id),
    KEY idx_inbox_lease (status, lease_until, id),
    KEY idx_inbox_command (tenant_id, client_id, command_id, status, id),
    KEY idx_inbox_processed (tenant_id, client_id, consumer_name, result_status, processed_at, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin COMMENT='Idempotent Agent command consumer inbox with byte-exact wire payload';
```

### A.10 d06-agent_command_operation_audit

Statement SHA-256：`7d94ea6a536852ada00a389dcc65a39df61f1c7d5e10ca7fa841145c9a995540`

```sql
CREATE TABLE IF NOT EXISTS agent_command_operation_audit (
    id                          BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    operation_id                VARCHAR(100) NOT NULL COMMENT 'Stable privileged operation id',
    phase                       VARCHAR(16) NOT NULL COMMENT 'REQUEST or RESULT append-only phase',
    operation_type              VARCHAR(32) NOT NULL COMMENT 'BROKER_REDRIVE or MANUAL_REISSUE',
    tenant_id                   VARCHAR(50) NOT NULL COMMENT 'Owner jiacn scope',
    client_id                   VARCHAR(50) NOT NULL COMMENT 'OAuth/API client scope',
    task_id                     VARCHAR(100) NOT NULL COMMENT 'Exact scoped task id',
    target_agent_id             VARCHAR(100) NOT NULL COMMENT 'Exact target Agent id',
    command_id                  VARCHAR(100) DEFAULT NULL COMMENT 'Validated durable business command id',
    source_message_id           VARCHAR(100) NOT NULL COMMENT 'Requested source transport message id',
    new_message_id              VARCHAR(100) DEFAULT NULL COMMENT 'New transport id for manual reissue',
    delivery_id                 BIGINT NOT NULL COMMENT 'Validated or requested delivery id',
    source_attempt              INT DEFAULT NULL COMMENT 'Validated source transport attempt',
    new_attempt                 INT DEFAULT NULL COMMENT 'New manual reissue attempt',
    wire_hash                   BINARY(32) DEFAULT NULL COMMENT 'Validated SHA-256 only; no payload bytes',
    requester_id                VARCHAR(100) NOT NULL COMMENT 'Trusted authenticated requester subject',
    approver_id                 VARCHAR(100) DEFAULT NULL COMMENT 'Trusted distinct approver subject',
    reason                      VARCHAR(1000) NOT NULL COMMENT 'Bounded operational reason',
    ticket_reference            VARCHAR(200) NOT NULL COMMENT 'Bounded approval/change reference',
    requested_at                BIGINT NOT NULL COMMENT 'Request epoch millis',
    completed_at                BIGINT DEFAULT NULL COMMENT 'Terminal result epoch millis',
    outcome                     VARCHAR(32) NOT NULL COMMENT 'REQUESTED/SUCCEEDED/REJECTED/FAILED',
    error_code                  VARCHAR(200) DEFAULT NULL COMMENT 'Sanitized bounded error code',
    created_by                  VARCHAR(100) NOT NULL COMMENT 'Immutable creator identity',
    created_at                  BIGINT NOT NULL COMMENT 'Immutable creation epoch millis',
    PRIMARY KEY (id),
    UNIQUE KEY uk_command_operation_phase (operation_id, phase),
    KEY idx_command_operation_scope (tenant_id, client_id, id),
    KEY idx_command_operation_source (tenant_id, client_id, delivery_id, source_message_id, id),
    KEY idx_command_operation_outcome (tenant_id, client_id, operation_type, outcome, created_at, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin COMMENT='Append-only privileged Agent command operation audit';
```

### A.11 d06-agent_command_redrive_operation

Statement SHA-256：`4c16d737d285d0391adca200bea2ab19b4eb238a7f5932b4d8093909be954030`

```sql
CREATE TABLE IF NOT EXISTS agent_command_redrive_operation (
    id                          BIGINT NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    operation_id                VARCHAR(100) NOT NULL COMMENT 'Stable privileged broker-redrive operation id',
    delivery_id                 BIGINT NOT NULL COMMENT 'Reserved durable delivery row id',
    task_id                     VARCHAR(100) NOT NULL COMMENT 'Exact scoped task id',
    target_agent_id             VARCHAR(100) NOT NULL COMMENT 'Exact target Agent id',
    command_id                  VARCHAR(100) NOT NULL COMMENT 'Validated durable business command id',
    source_event_id             VARCHAR(100) NOT NULL COMMENT 'Validated source outbox event id',
    source_message_id           VARCHAR(100) NOT NULL COMMENT 'Byte-exact source transport message id',
    source_attempt              INT NOT NULL COMMENT 'Validated source transport attempt',
    wire_hash                   BINARY(32) NOT NULL COMMENT 'Validated source wire SHA-256 only; no payload bytes',
    requester_id                VARCHAR(100) NOT NULL COMMENT 'Trusted authenticated requester subject',
    reason                      VARCHAR(1000) NOT NULL COMMENT 'Bounded operational reason',
    ticket_reference            VARCHAR(200) NOT NULL COMMENT 'Bounded approval/change reference',
    outcome_state               ENUM('PENDING','SUCCEEDED','FAILED') NOT NULL DEFAULT 'PENDING' COMMENT 'Exact pending-to-terminal operation outcome',
    settlement_state            ENUM('PENDING','SOURCE_ACKED','SOURCE_REQUEUED','NOT_ACQUIRED','UNKNOWN') NOT NULL DEFAULT 'PENDING' COMMENT 'Exact source DLQ settlement proof',
    error_code                  VARCHAR(200) DEFAULT NULL COMMENT 'Sanitized bounded terminal error code',
    requested_at                BIGINT NOT NULL COMMENT 'Reservation epoch millis',
    completed_at                BIGINT DEFAULT NULL COMMENT 'Terminal persistence epoch millis',
    version                     BIGINT NOT NULL DEFAULT 0 COMMENT 'One-way terminal CAS version',
    disposition_guard           TINYINT GENERATED ALWAYS AS (IF(outcome_state='PENDING',1,NULL)) STORED COMMENT 'Non-null while Inbox disposition must fail closed',
    redrive_guard               TINYINT GENERATED ALWAYS AS (IF(settlement_state IN ('SOURCE_REQUEUED','NOT_ACQUIRED'),NULL,1)) STORED COMMENT 'Non-null after active, successful, or ambiguous redrive',
    tenant_id                   VARCHAR(50) NOT NULL COMMENT 'Owner jiacn scope',
    client_id                   VARCHAR(50) NOT NULL COMMENT 'OAuth/API client scope',
    create_time                 BIGINT NOT NULL COMMENT 'Immutable reservation creation epoch millis',
    update_time                 BIGINT NOT NULL COMMENT 'Last state CAS epoch millis',
    PRIMARY KEY (id),
    UNIQUE KEY uk_redrive_operation_id (tenant_id, client_id, operation_id),
    UNIQUE KEY uk_redrive_operation_guard (tenant_id, client_id, delivery_id, source_message_id, source_attempt, redrive_guard),
    KEY idx_redrive_operation_disposition (tenant_id, client_id, delivery_id, source_message_id, source_attempt, disposition_guard),
    KEY idx_redrive_operation_recovery (tenant_id, client_id, outcome_state, requested_at, id),
    KEY idx_redrive_operation_scope (tenant_id, client_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin COMMENT='Durable privileged broker-redrive reservation and recovery state';
```

### A.12 d06-trg_command_operation_audit_no_update

Statement SHA-256：`1df90b5cc820f1346d9136c754a7ce885d664039c826181f6e53f7cbf1cf5d03`

```sql
CREATE TRIGGER trg_command_operation_audit_no_update
BEFORE UPDATE ON agent_command_operation_audit
FOR EACH ROW
SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'D09: operation audit rows are immutable after insert';
```

### A.13 d06-trg_command_operation_audit_no_delete

Statement SHA-256：`925f8ec73e1ad59bb51932363eb74383bf05483466bd6628615a9a696ae2cc27`

```sql
CREATE TRIGGER trg_command_operation_audit_no_delete
BEFORE DELETE ON agent_command_operation_audit
FOR EACH ROW
SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'D09: physical delete of operation audit rows is forbidden';
```

## 附录B：原38类startup inventory（存在不等于启用或catalog通过）

沿用原清单，仅列源码和原注解/注册条件位置，不新增38项硬门禁。

| 类源码 | 条件位置 | 已证明 / 未证明 |
|---|---|---|
| [AgentCommandTransportSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandTransportSchemaInitializer.java#L1) | [AgentCommandTransportSchemaConfiguration.java:12](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandTransportSchemaConfiguration.java#L12) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentExecutionReportSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentExecutionReportSchemaInitializer.java#L1) | 无直接conditional证据，按原registrar/callsite核对 | JAR有class；不推定live Bean/全catalog等价 |
| [AgentRuntimeSessionFenceSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSessionFenceSchemaInitializer.java#L1) | [AgentRuntimeSessionFenceSchemaInitializer.java:16](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSessionFenceSchemaInitializer.java#L16) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentRuntimeV1SchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeV1SchemaInitializer.java#L1) | 无直接conditional证据，按原registrar/callsite核对 | JAR有class；不推定live Bean/全catalog等价 |
| [AgentSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java#L1) | [AgentSchemaInitializer.java:18](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java#L18) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentSelectedOutputFinalizationSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSelectedOutputFinalizationSchemaInitializer.java#L1) | [AgentSelectedOutputFinalizationConfiguration.java:13](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSelectedOutputFinalizationConfiguration.java#L13) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskBountyBootstrapOutboxSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskBountyBootstrapOutboxSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskBountyQuoteSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskBountyQuoteSchemaInitializer.java#L1) | [AgentTaskFundingSchemaConfiguration.java:12](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L12)；[AgentTaskFundingSchemaConfiguration.java:18](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L18)；[AgentTaskFundingSchemaConfiguration.java:24](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L24) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskCreationOperationSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskCreationOperationSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskExecutionGrantSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskExecutionGrantSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskFormalDeliverySchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFormalDeliverySchemaInitializer.java#L1) | [AgentTaskFormalDeliveryConfiguration.java:12](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFormalDeliveryConfiguration.java#L12) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskFundingSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaInitializer.java#L1) | [AgentTaskFundingSchemaConfiguration.java:12](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L12)；[AgentTaskFundingSchemaConfiguration.java:18](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L18)；[AgentTaskFundingSchemaConfiguration.java:24](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L24) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskProviderCostConsentSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskProviderCostConsentSchemaInitializer.java#L1) | [ControlledImageProviderConfiguration.java:15](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L15)；[ControlledImageProviderConfiguration.java:16](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L16)；[ControlledImageProviderConfiguration.java:22](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L22)；[ControlledImageProviderConfiguration.java:23](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L23)；[ControlledImageProviderConfiguration.java:29](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L29)；[ControlledImageProviderConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L30) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskRequirementSnapshotSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskRequirementSnapshotSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [AgentTaskSettlementSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskSettlementSchemaInitializer.java#L1) | [AgentTaskFundingSchemaConfiguration.java:12](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L12)；[AgentTaskFundingSchemaConfiguration.java:18](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L18)；[AgentTaskFundingSchemaConfiguration.java:24](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentTaskFundingSchemaConfiguration.java#L24) | JAR有class；不推定live Bean/全catalog等价 |
| [ControlledImageBridgeSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageBridgeSchemaInitializer.java#L1) | [ControlledImageProviderConfiguration.java:15](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L15)；[ControlledImageProviderConfiguration.java:16](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L16)；[ControlledImageProviderConfiguration.java:22](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L22)；[ControlledImageProviderConfiguration.java:23](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L23)；[ControlledImageProviderConfiguration.java:29](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L29)；[ControlledImageProviderConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L30) | JAR有class；不推定live Bean/全catalog等价 |
| [ControlledImageExecutionSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageExecutionSchemaInitializer.java#L1) | [ControlledImageProviderConfiguration.java:15](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L15)；[ControlledImageProviderConfiguration.java:16](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L16)；[ControlledImageProviderConfiguration.java:22](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L22)；[ControlledImageProviderConfiguration.java:23](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L23)；[ControlledImageProviderConfiguration.java:29](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L29)；[ControlledImageProviderConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageProviderConfiguration.java#L30) | JAR有class；不推定live Bean/全catalog等价 |
| [ControlledImageFollowupV3SchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageFollowupV3SchemaInitializer.java#L1) | [ControlledImageFollowupV3SchemaInitializer.java:26](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageFollowupV3SchemaInitializer.java#L26)；[ControlledImageFollowupV3SchemaInitializer.java:27](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/ControlledImageFollowupV3SchemaInitializer.java#L27) | JAR有class；不推定live Bean/全catalog等价 |
| [HallPrivateCaseSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/HallPrivateCaseSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [HallPrivateMarkSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/HallPrivateMarkSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [HallRequestDraftSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/HallRequestDraftSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [PersonalWorkspaceConversationLinkSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceConversationLinkSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [PersonalWorkspaceExecutionSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceExecutionSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [PersonalWorkspaceSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [PersonalWorkspaceTaskLinkSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceTaskLinkSchemaInitializer.java#L1) | [PersonalWorkspaceStorageConfiguration.java:30](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L30)；[PersonalWorkspaceStorageConfiguration.java:36](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L36)；[PersonalWorkspaceStorageConfiguration.java:42](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L42)；[PersonalWorkspaceStorageConfiguration.java:49](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L49)；[PersonalWorkspaceStorageConfiguration.java:55](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L55)；[PersonalWorkspaceStorageConfiguration.java:61](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L61)；[PersonalWorkspaceStorageConfiguration.java:67](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L67)；[PersonalWorkspaceStorageConfiguration.java:74](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L74)；[PersonalWorkspaceStorageConfiguration.java:81](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L81)；[PersonalWorkspaceStorageConfiguration.java:88](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L88)；[PersonalWorkspaceStorageConfiguration.java:95](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/PersonalWorkspaceStorageConfiguration.java#L95) | JAR有class；不推定live Bean/全catalog等价 |
| [ArchiveQuestionSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveQuestionSchemaInitializer.java#L1) | [ArchiveQuestionSchemaInitializer.java:20](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveQuestionSchemaInitializer.java#L20)；[ArchiveQuestionSchemaInitializer.java:21](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveQuestionSchemaInitializer.java#L21) | JAR有class；不推定live Bean/全catalog等价 |
| [ArchiveReaderDataSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveReaderDataSchemaInitializer.java#L1) | [ArchiveReaderDataSchemaInitializer.java:19](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveReaderDataSchemaInitializer.java#L19) | JAR有class；不推定live Bean/全catalog等价 |
| [ArchiveSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveSchemaInitializer.java#L1) | [ArchiveSchemaInitializer.java:19](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveSchemaInitializer.java#L19) | JAR有class；不推定live Bean/全catalog等价 |
| [ChatConversationArchiveSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatConversationArchiveSchemaInitializer.java#L1) | [ChatConversationArchiveSchemaInitializer.java:21](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatConversationArchiveSchemaInitializer.java#L21)；[ChatConversationArchiveSchemaInitializer.java:22](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatConversationArchiveSchemaInitializer.java#L22) | JAR有class；不推定live Bean/全catalog等价 |
| [ChatDeliberationSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatDeliberationSchemaInitializer.java#L1) | [ChatDeliberationSchemaInitializer.java:25](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatDeliberationSchemaInitializer.java#L25) | JAR有class；不推定live Bean/全catalog等价 |
| [ChatSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatSchemaInitializer.java#L1) | [ChatSchemaInitializer.java:21](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatSchemaInitializer.java#L21) | JAR有class；不推定live Bean/全catalog等价 |
| [ChatSelectedOutputFinalizationSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatSelectedOutputFinalizationSchemaInitializer.java#L1) | [ChatSelectedOutputFinalizationSchemaInitializer.java:21](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatSelectedOutputFinalizationSchemaInitializer.java#L21)；[ChatSelectedOutputFinalizationSchemaInitializer.java:22](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatSelectedOutputFinalizationSchemaInitializer.java#L22) | JAR有class；不推定live Bean/全catalog等价 |
| [ChatTypedDeliberationSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatTypedDeliberationSchemaInitializer.java#L1) | [ChatTypedDeliberationSchemaInitializer.java:24](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatTypedDeliberationSchemaInitializer.java#L24) | JAR有class；不推定live Bean/全catalog等价 |
| [EconomyHostingRentSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyHostingRentSchemaInitializer.java#L1) | [EconomyConfiguration.java:18](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyConfiguration.java#L18)；[EconomyConfiguration.java:24](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyConfiguration.java#L24) | JAR有class；不推定live Bean/全catalog等价 |
| [EconomySchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomySchemaInitializer.java#L1) | [EconomyConfiguration.java:18](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyConfiguration.java#L18)；[EconomyConfiguration.java:24](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyConfiguration.java#L24) | JAR有class；不推定live Bean/全catalog等价 |
| [EconomySkillApplicationSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomySkillApplicationSchemaInitializer.java#L1) | [SkillMarketplaceConfiguration.java:8](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/agent/jia-agent-service/src/main/java/cn/jia/agent/config/SkillMarketplaceConfiguration.java#L8) | JAR有class；不推定live Bean/全catalog等价 |
| [EconomySkillSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomySkillSchemaInitializer.java#L1) | [EconomySkillMarketplaceConfiguration.java:14](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomySkillMarketplaceConfiguration.java#L14) | JAR有class；不推定live Bean/全catalog等价 |
| [WxDailyVoteSchemaInitializer.java:1](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/wx/jia-wx-service/src/main/java/cn/jia/wx/config/WxDailyVoteSchemaInitializer.java#L1) | [WxDailyVoteSchemaInitializer.java:22](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/wx/jia-wx-service/src/main/java/cn/jia/wx/config/WxDailyVoteSchemaInitializer.java#L22)；[WxDailyVoteSchemaInitializer.java:23](/home/isp/wsps/worktrees/ur05-api-local-release-20261009T1320/wx/jia-wx-service/src/main/java/cn/jia/wx/config/WxDailyVoteSchemaInitializer.java#L23) | JAR有class；不推定live Bean/全catalog等价 |
