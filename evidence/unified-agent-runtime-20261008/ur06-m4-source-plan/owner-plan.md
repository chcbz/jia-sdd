# UR06 M4 genuine MySQL 原六 E05 源码桥接（只读交接）

**READONLY_PLAN_COMPLETE；M4六项均NOT_RUN；非Reviewer/Writer。**

## 结论与已证明的源码缺口

本次是只读source plan，不是Reviewer/Writer；所有M4真实运行均NOT_RUN。原六完整测试[R01]及其全部多lane分支要保留，不能换成native404/心跳/UR06 M3子集。UR06已有genuineMySQL进程归属、GuardedDataSource、真实Spring/Tomcat/auth/defaultDAO/MyBatis/result/D06 beans[R06/R07]；缺测试backend桥接，不缺第二业务实现。
最新实际原前置为9966f4a6817ef322e82bdcc1379cb5810e943ba8/tree0091449092568c3486cb7a2cf0b96a33270dfcc9，读取时clean且引用字节与commit一致；主控说session96963正跑56+compileUR06+layering，本报告不把RUNNING报PASS。UR06四文件与该API的对应四文件SHA逐项同值。
具体SQL缺口：完整baseline+四initializer链未建agent_work_item_reassignment；原E05 DDL[R17]无owner_jiacn，而真实Mapper[R19]SELECT/INSERT必须该列；原ownerPhase-A DDL[R18]提供列/索引，不能只跑E05 SQL后宣称ready，也不能搬H2表掩盖。
旧83600由主控核为EXIT1/Pillow8.4缺JPEGheaders/lib；C1FAIL、C2-C4/consumer/六E05NOT_RUN，root已删除。新A不是已安装target，必须等新C1-C4真实PASS。

## 最小原Owner四路径

仅扩展原Turing UR06四个test-only文件，具体变更表见下。现有Lane/MySql/source是private[R06]，不能假定直接跨测试类继承；在原class内加purpose最少，不另复制MySQLowner。FOUNDATION/M4是私有fixture控制参数，不是产品wire/授权。
原UR04 Node main有路径guard[R04:319]，并非import必启动；但prepare/runtime不export，唯一SOURCE静态7594，不能假定import即可参数化完整E05。只移植原测试管道/观察，不复制业务。原7方法/语义保留，原task精确排除新六method，M4新task选六；全套UR06统一采用最新A，不留7594兼容双轨。
原nonpaid-child[R05]仍读clean固定API原tracked路径；Java核filehash+APIcommit/tree后拷入ownedroot，再与原测试一样仅改shebang为acceptedNode，无新增资源路径、不更改UR04源文件。

- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java`
  - Add exact original six methods/all branches/assertion helpers; explicit Lane FOUNDATION/M4 purpose reuses private inner MySql/process cleanup; three M4 subjects, dual Java/Node restart and independent parent JDBC. Single CLIENT pin to new A for whole suite; preserve original seven foundation methods.

- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java`
  - Factor full baseline/four initializers from eight-foundation seed; M4 original E05+ownerPhaseA resources then threeACTIVE/canonical work/transport DML. Add original private SEED/DISPATCH/ALTERED_DISPATCH/MUTATE/RELEASE_PREPARED, snapshots, container response-cut and real preparedBoundary; genuineMySQL trigger + transparent SQL attempt observations. No mock auth/DAO/transaction/business implementation.

- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs`
  - One source verifier updated exact newA fullarchive tuple; M4-purpose threeAgent PREPARE/HOST/private operations from originalUR04 while foundation8/enroll unchanged. Execute real installed runtime/adapter/engine/defaultfetch/ws; original tracked API nonpaid-child is read/copied/hashbound, no new child file. No product wire or compatibility branch.

- `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle`
  - Same sourceSet/test-only deps/root selector/7env/classpath. New ur06M4MysqlE05 Test filters exact6 methods; existing ur06EnrollMysql excludes these six and retains original7. Both onefork/no-cache/no up-to-date, UR06_LOCAL_ACCEPTANCE1. No production/defaulttest/build.gradle/globalconfig edits.

## 原完整MySQL初始化/SQL复用顺序

1. 原MySql[R06:346-378]启动自己的8.0.21，归属核验后创建ur06_fixture；所有initialize SQL都经真实guard[R07:344-410]。
2. 按explicit FileSystemResource加载完整原agent baseline[R10]、完整原user test baseline[R11]、原accountsecurity升级[R12]，不裁掉非六方法表。执行原AgentSchemaInitializer/RuntimeV1/RuntimeSessionFence/CommandTransport[R13-R16]，保留原legacy nullownership/timestamps保护；抽取初始化公共部分，foundation后续8persona seed不用于M4。禁止obsolete owner-as-tenant A02迁移。
3. 仅freshM4私有schema接续整份原E05 SQL[R17]，再整份原single-tenant-task-owner-ddl.sql[R18]。SET/PREPARE/EXECUTE/DEALLOCATE保持同guardedConnection/session；用原ResourceDatabasePopulator读取原资源，不新造DDL/截片重写。原Phase-A无业务DML，但owner列仍nullable；不能声称生产Phase-B NOT_NULL/backfill已实现。真实资源执行仍NOT_RUN，遇DDL失败按原path/固定语句序号+SQLState归因，不删constraint/缩schema。
4. M4私有syntheticACTIVE三installation/user/account/identity/binding，sealedmanifest+随机rta只通过pipe送入真实授权hash验证；M4不声称enroll。沿用UR06原user700/tenant0/client原scope（Node/manifest/canonical codec/gate都一致），只给该exact scope，不拓ACL。persona id1000+/rank200+避开真initializer108persona seeds[R13:2510]，不能原样抄UR04id1/2/3撞主键。foundation8subjects仍走原模式。
5. 复用原seedWork/seedTransport[R02:210-247]的DML和真实AgentCommandCanonicalCodec，映射上述owner/client：task/member/work claimed5、attempt2/max3；predecessor/successor business/wire/hash；SENT7delivery、PUBLISHED confirmedoutbox、PROCESSEDdispatchinbox、immutable reassignment(4→5/task7/source/fencehash)。这是合成已存在历史receipt，不冒充真实JWT创建reassignment或Rabbitpublish已跑。
6. snapshot runtime范围限定精确三subject，排除legacy row；原businessFingerprint仍原六业务表排序/binary规范化，不打印材料/SQL/params。Java B initializefalse，重连同DB/state，无baseline/DDL/reseed。原H2DDL[R03]、H2JavaTrigger/SHUTDOWN/.mv.db/IFEXISTS不用于M4。MySQL进程保持存活，证明Java+Node双重启持久，不声称mysqldcrashrestart/生产schema迁移。
F06 outcome资源非本六方法调用链，保留独立未证项；完整baseline/四initializer不等于声称整个生产迁移历史/PhaseB都验收。

## 真实beans/方法/调用接点

沿用R07:444-512真实DataSourceTransactionManager/SqlSessionFactory/InfoMapper productionXML/UserInfoDao/AccountSecurityService/AgentRuntimeAuthenticationService/controller/filter/nativeWS；不mockDAO/auth/fixedSupplierproof，原注入链不删除。
lease/start/heartbeat：AgentWorkItemReassignmentController.readLease/startLease/heartbeatLease[R20]，actorAgentId唯一query仅确认已认证subject；nativeCommit→withNativeFence原lease/reassignment业务事务。
result：AgentWorkItemRuntimeResultController.commit[R21:51-67] withNativeFence(preflight)→results.prepareRuntimeResult→withNativeFence(commitPreparedRuntimeResult)。prepare NEVER、realopaqueissuer/scope/source token/rollback原实现[R22]；results bean已setRuntimeResultRecovery(reassignments,events)[R07:574-581]，不是自己另实现result。
GET原结果：readResult→withNativeFence(results.readRuntimeResult)[R21/R22]，原持久proof/material校验，businessFingerprint不改。最终ACK由真实HTTPRuntimeV1Controller→AgentCommandAckServiceImpl真实DAO/transaction[R24]返回ADVANCED/PRIOR。
原testRuntimeOnly MySQLdriver[R25]和UR06test级deps[R09]足够来源接点，无新增生产依赖。保留hosting/schemafalse、skillmarketplacefalse实际bean/原未启用路径[R28/R29]，非hosted未付费Agent；不能用mock绕过或宣称托管/SKILLinstallation/付费已验。

## H2特定fault与durable回读的精确替换

原H2 SqlProbe[R02:342-365]不可CALL到MySQL。在现有透明guard JDBC加固定原表/语句allowlist观察：真正execute成功后按rowcount计artifactInsert/workUpdate/ACKadvance；event参数仅在内存识别WORK_ITEM_SUBMITTED、执行前计submittedAttempt，提交/回滚仍真实委托。batch只在实际执行按结果统计，不能以addBatch/methodcall冒充SQL成功；seed/fixturemutation/SELECT不冒充业务ACK更新。PRIOR原DAO不advance[R24]，新JVM应ackUpdates0。观察counter不rollback，持久rows独立查才是终态证据。
ROLLBACK lane仅在本privateMySQL原agent_task_event建真实BEFORE INSERT触发器：NEW.event_type='WORK_ITEM_SUBMITTED'→SIGNAL SQLSTATE45000，固定无秘密message。真实artifact/work已执行后由MySQL拒绝event并使原业务事务rollback；禁止DAO前主动throw/mock。保留原artifactAttempt>=1/work>=3/submitted>=1与持久0/running/noresult/events==eventVersion/GET404/noSuccess/重启不重跑全部原断言。
PREPARED沿用R02:756-769原observer：call.proceed先完成realopaqueprepare、确认无activeTx，再privatepipehold；真实Node sessionrotate后release，controller重fence401，原issuer对象不替换。
RESULT_LOSS/ACK_LOSS沿用原Tomcat responseCut[R02:367-436]：原controller事务先commit、独立DB证实后hold尚未发送的真实200响应，parent停止exactownedJava令真实TCP响应丢失；不是fakefetch、删除ACK记录或凭空造异常。
原persisted()[R01:403-407]改parent新GuardedDataSource(mysql.spec)独立connection；JavaA已退出、B尚未启动时同真实MySQL查询，不复用child事务，不H2SHUTDOWN。JavaB/NodeB新PID复用同DB/state，原session/WS轮换generation，不能SQL伪改generation。

## 单C1-C4accepted callback与新A绑定

新payloadA固定d91ebbf436911eac20ffb70cb92192a65c742e11/treeb2e3f17ff57e21e2482c0fc54e71dbf4b92dbd82，git只读tree已核；count候选285[R26:14-15]。rawarchive SHA/bytes、manifestSHA由主控固定gitarchive后提供，目前UNKNOWN，不沿用旧7594/f4dc。JavaCLIENT/NodeSOURCE/boot树/所有sourceproof同步单一A；API绑定含9966+最终桥接的clean不可变commit/tree。
观察到本地新harness候选snapshot（附录），不是主控已核收B；payloadA与harnessB是两独立来源角色。固定Bcommit/tree/harnessfileSHA并核B声明A，不能把Btree当payloadTREE。主控最新尚未核收B/新安装target，本报告无安装实测。
现成acceptance(env,{consumeArtifact})[R26:488-543]在C1-C4确实PASS、source/payload/target/node/hash验证后，冻结ordered ur01-accepted-local-target-v1 snapshot，await回调一次，不由env加载代码，不silent重试install/consumer。主控现成wrapper[R27]只允许在借用target加ur04-clean-artifact.json，inventory/mode/link/hash绑定A/source/tree/archive/C1C4PASS/node/harness/buildId/acceptedSnapshotSHA。manifest原cleanRun字段按既有接点填本地buildId；buildId不是FlowRun，不能伪造云验回执。
同一次callback内串行运行完整M4六selector，共用同一个acceptedARTIFACT_ROOT/NODE_BIN/CLIENT_ROOT；每fault只新建自己privateMySQL/Java/Node/state，不每casepip/npm/重装、借宿主包或改acceptedvenv。默认原runtime/adapter/engine从acceptedtarget加载，完整enginepayload/deps和实际hash映射到A；全部source树重建、noalias/onlyattestedin-targetvenvlink守卫保留。
callback等所有selector/ownedchildcleanup结束才返回固定allowlisted结果；harness随后source/artifact/harness完整readback，再finally删它自己的installroot。fixture只删自己的ur06root，不删source/target/Producerroot，不私拷借用target留下假acceptedartifact。旧83600未到consumer，不可用已删target。

## selector任务/非秘密env/ownership/安全cleanup

新task建议:agent:jia-agent-service:ur06M4MysqlE05，same ur06EnrollMysql sourceSet、精确六methodfilter；原taskexclude新增六而保留原7。不是默认test selector，也不假定跨sourceSet能--tests到。init保留APIsettingsroot/sourcefile selector、忽略includedplugin/buildlogic/buildSrc、mainmissingagentfailclosed、test-onlydeps、ur06.fixture.classpath正确runtimeClasspath、onefork/no-cache/noup-to-date。
launcher optin UR06_LOCAL_ACCEPTANCE=1；testenv严格原七UR06_API_COMMIT UR06_CLIENT_ROOT UR06_CLIENT_COMMIT UR06_NODE_BIN UR06_ARTIFACT_ROOT UR06_MYSQLD_BIN UR06_CODEX_BIN。不新增DATABASE_URL/宿主config/proxy凭据/token。UR06_CODEX_BIN继续原输入证明，不放宽tools/sourceguard；M4profile必须指向原syntheticchild，绝不实际模型/Provider调用。
主控在固定APIclean cwd通过 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle 串行调度，接点参数见JSON。task尚未实施，命令不是执行回执。完整backendtest+layering既有保留，不由本support重复全套。
JVM/Node child env清空后PATH HOME TMPDIR LANG TZ，Node仅加UR06_PRIVATE_CHILD=1；执行child固定PATH LANG LC_ALL TZ TMPDIR HOME CODEX_HOME CYF_WORKSPACE_FILE_TOOLCHAIN_PYTHON CYF_WORKSPACE_FILE_DELIVERY_TOOL[R05]，其他Agent凭据禁止。DBpassword/authorization/manifests/privatepaths只pipe传输，public只固定stage/class/rootclass/status/count/hash，不rawmessage/SQL/params/body/token/privatepaths。
MySQL沿用原8.0.21/server属性proof、--no-defaultsfirst、private0700root/datadir/mysqlfiles/socket/pid/log、loopback非3306/33060随机port、mysqlx0/general/slowlogOFF/skiplogbin，绝不读取外部datasource/config或借共享server。随机rootadmin仅私有bootstrap/归属证明，fixtureuser仅ur06_fixture.*，无全局PROCESSgrant/secret inenv。新connection与execute/batch/commit持续PID/start/inode/serverproof。
cleanup保留exactProcess handles与已观察syntheticchildren PID/start/parent校验；Node及执行child→Java→ownedMySQL，失败仍尝试全部ownedhandles，alive则不删ownedroot。rootinode/canonical/noFOLLOWLINKS，禁止进程名kill/共享service/借用target删除。真实NodeHTTP/WS和MySQLloopback net权限必需；不fakefetch/server、不隐性skip。
本六测试真实执行原engine OSchild和结果提交，但合成0cost输出不是Codexmodel能力证明、CLIprobe不是工具链完整安装验收。

## 依赖/未证项与交接状态

源接点已证但M4尚未实现/编译/运行：四test路径可做，不需生产dependency/newwire/第二业务实现/新schema。Turing接片前由主控集成原9966前置最终结果，固定APIcleancommit/tree；主控核收B与Aarchive/manifest，然后实际C1-C4PASS单callbacktarget。缺任何前置标NOT_RUN，不能fallback旧target/H2/mockauth/mockDAO。
原六全部输入/期望/证据见下表及JSON。保留unknownSTARTED不重跑、pending material/proof、三Agent隔离/撤销、prepared refence/rollback/response loss/ACK PRIOR原全部断言；不是只迁移happy path。原7enroll/foundations保持原矩阵归属，不重复调查或拿syntheticACTIVE替代真enroll证明。
本次无Gradle/Nodefixture/MySQL/pip/npm/真实安装/Flow/生产动作，无Owner源码/rootdoc更改。所有M4NOT_RUN；Rabbitpublish、JWT创建reassignment、productionmigration/PhaseB、mysqldcrashrestart、F06/Provider付费业务及全Goal不声称验收。候选新A/B与源码存在不是运行ready。

## 原完整六selectors：输入/期望/证据 — 全NOT_RUN

### M4-1 `e05ActualClientHttpCommitsOriginalResultAndTerminalAck` — NOT_RUN
- selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05ActualClientHttpCommitsOriginalResultAndTerminalAck`；原R01:28–50。
- 输入：真实dispatch→RECEIVED/STARTED→lease/start/heartbeat→原engine真实合成OS子进程→原prepared result事务→原GET→D06终态；重复ACK/重复与异fingerprint投递。
- 期望：D06 8/9/10，actor和每步expectedVersion匹配；work submitted/leaseCleared，一artifact/submittedEvent/child；GET业务hash不变；重复ACK PRIOR10；一次真实冲突审计且不增ACK更新/child/业务hash；唯一inbox/ledger，pending0；停children后独立JDBC同终态。
- 证据：exact-method complete JUnit XML；allowlisted real HTTP category/status/version/actor receipts；independent guarded JDBC persisted rows/business hash；Java/Node A+B PID/start identity and private MySQL ownership；original child counts/ledger/inbox/pending/credentialsAbsent；source/archive/artifact pre/post hashes and owned cleanup。

### M4-2 `e05LostResultReadbackSurvivesJavaAndNodeRestart` — NOT_RUN
- selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05LostResultReadbackSurvivesJavaAndNodeRestart`；原R01:52–67。
- 输入：原result事务已commit但真实HTTP200响应hold，parent停止owned Java A，Node保存material后停；同DB/state启动Java B/Node B。
- 期望：丢响应时delivery STARTED9且业务已持久；新PID/generation2；material recovery_required/凭据不入checkpoint；仅原GET恢复，无lease/start/heartbeat/resultPOST；最终SUCCEEDED10，相同业务digest与一个child。
- 证据：exact-method complete JUnit XML；allowlisted real HTTP category/status/version/actor receipts；independent guarded JDBC persisted rows/business hash；Java/Node A+B PID/start identity and private MySQL ownership；original child counts/ledger/inbox/pending/credentialsAbsent；source/archive/artifact pre/post hashes and owned cleanup。

### M4-3 `e05TerminalAckLostResponseReplaysPriorWithoutWorkRerun` — NOT_RUN
- selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05TerminalAckLostResponseReplaysPriorWithoutWorkRerun`；原R01:69–83。
- 输入：原D06 SUCCEEDED事务commit后hold真实ACK响应，精确owned双进程重启，保留原ACKoutbox。
- 期望：持久SUCCEEDED10；重发PRIOR10；新JVM ackUpdates0；相同业务hash/onechild；唯一checkpoint、pending清零；无新执行/结果POST。
- 证据：exact-method complete JUnit XML；allowlisted real HTTP category/status/version/actor receipts；independent guarded JDBC persisted rows/business hash；Java/Node A+B PID/start identity and private MySQL ownership；original child counts/ledger/inbox/pending/credentialsAbsent；source/archive/artifact pre/post hashes and owned cleanup。

### M4-4 `e05PreparedCommitRefencesAndRollbackIsDurable` — NOT_RUN
- selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05PreparedCommitRefencesAndRollbackIsDurable`；原R01:85–111。
- 输入：先真实opaque prepare完成且无outer tx，再rotate session至generation2、release；另lane真实MySQL event BEFORE INSERT SIGNAL45000，在原artifact/work已SQL执行后拒绝WORK_ITEM_SUBMITTED。
- 期望：refence401且artifact/submitted0，独立JDBC同状态；rollback artifactAttempt>=1/workUpdate>=3/submittedAttempt>=1但持久artifact/submitted0，workrunning/noresult/events==eventVersion/noSucceeded，原GET404；durable hash相同；重启pending material仅readback不重跑。
- 证据：exact-method complete JUnit XML；allowlisted real HTTP category/status/version/actor receipts；independent guarded JDBC persisted rows/business hash；Java/Node A+B PID/start identity and private MySQL ownership；original child counts/ledger/inbox/pending/credentialsAbsent；source/archive/artifact pre/post hashes and owned cleanup。

### M4-5 `e05SourceAndOriginalResultProofStayFailClosed` — NOT_RUN
- selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05SourceAndOriginalResultProofStayFailClosed`；原R01:113–151。
- 输入：在真正STARTED/lease/heartbeat之后改successor/predecessor hash/source target；另lane改已commit proof/material并丢响应/双重启；真实actor/producer/scope/old-session/unregistered HTTP。
- 期望：409/409/404且artifact/submitted/success0；corrupted proof/material不能恢复success，保留原被损坏businesshash、仅GET、onechild；actor/producer403，scope/oldsession/unregistered401；各negative前后DB不变。
- 证据：exact-method complete JUnit XML；allowlisted real HTTP category/status/version/actor receipts；independent guarded JDBC persisted rows/business hash；Java/Node A+B PID/start identity and private MySQL ownership；original child counts/ledger/inbox/pending/credentialsAbsent；source/archive/artifact pre/post hashes and owned cleanup。

### M4-6 `e05UnknownStartedNeverRerunsAndSiblingRemainsReady` — NOT_RUN
- selector `cn.jia.agent.acceptance.ur06.Ur06EnrollMysqlAcceptanceTest.e05UnknownStartedNeverRerunsAndSiblingRemainsReady`；原R01:153–177。
- 输入：真实STARTED/child进入但尚无material时停owned Node A/Java A；B同原state/DB启动、显式RECOVER；撤销subject+断开重连，sibling执行完整E05。
- 期望：unknown recovery_required且无material/持久artifact/event0，总child始终1即使RECOVER；revoked GET401、subject隔离，另外两Agent ready；sibling完整E05提交成功，第三Agent不启动child；checkpoint credentialsAbsent。
- 证据：exact-method complete JUnit XML；allowlisted real HTTP category/status/version/actor receipts；independent guarded JDBC persisted rows/business hash；Java/Node A+B PID/start identity and private MySQL ownership；original child counts/ledger/inbox/pending/credentialsAbsent；source/archive/artifact pre/post hashes and owned cleanup。

## 待实现task的最小启动参数（NOT_RUN）

仅主控正式调度使用，source/env/callback前置满足后；非本次执行命令。
```
--init-script
agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle
:agent:jia-agent-service:ur06M4MysqlE05
--no-daemon
--max-workers=1
-Dorg.gradle.parallel=false
--rerun-tasks
:agent:jia-agent-service:validateLayering
```

## source snapshot / path / line / SHA256

- original_ur04 `/home/isp/wsps/worktrees/ur04-e05-http-20261008` commit `2314c261eec5695fb791af8b0559fba13952ad4c` tree `d03f8b3ac31cff4216752bcbe4df5d2a61b7e167` clean=True；源码快照不是实测通过。

- original_ur06 `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008` commit `732558494ee082413f8f8e30ad448cc3c6fb7bbc` tree `95e5409268f9aaee871c3e6d812c3ad61722fbc7` clean=True；源码快照不是实测通过。

- latest_api_prerequisite `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008` commit `64d445a6a76fbe4a7f527fe914bdce6b5c6105da` tree `c0e486cb63f7293682a4400bfd41fa39bf363bee` clean=True；源码快照不是实测通过。

- observed_harness_b_candidate `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008` commit `2533381cc79e79d124d8c8630914790f48d3619e` tree `739f25ca5e7759ab427a7694d9cc55dc51d46732` clean=True；源码快照不是实测通过。

- **R01** `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java`，line 28–177,223–270,272–344,398–465；SHA256 `a84288fdfe51c402cbefaa6a086d9c2599e9ede670eb6cd469d35b4091909f12`；Original complete six tests/assertions; private Lane; H2 readback; fixed7594。

- **R02** `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpFixture.java`，line 130–247,256–298,342–436,587–601,735–769；SHA256 `5f33c08c6ef1aad9c6f1bb8c1781460268c765a42e526f06f96f40bc5cefbd4f`；Synthetic ACTIVE/canonical seeds; H2 probes; genuine HTTP loss/prepared boundary。

- **R03** `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-http-db-h2.sql`，line 1–30,304–354；SHA256 `fa38bd92200e7293716591fea25db12a9cf5c4dec02978e9fda7855a73c55dbc`；Reduced H2 schema/Java triggers; not MySQL。

- **R04** `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs`，line 10–13,37–105,109–172,200–281,304–321；SHA256 `36e0cc7d8e9c2ffb6b6872623b8515f40a52f221d8b76caf895025acf35dbf37`；Three-Agent original real runtime/adapter/engine/defaultfetch/WS protocol; fixed SOURCE。

- **R05** `/home/isp/wsps/worktrees/ur04-e05-http-20261008/agent/jia-agent-service/src/ur04E05Http/resources/ur04/nonpaid-execution-child.mjs`，line 1–36；SHA256 `bd5c7a113efeeb5eabb00d2623065c62da3bab09f47bcedf825f3348e22c3805`；Original real OS synthetic child, no Provider/model。

- **R06** `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java`，line 244–281,295–316,321–344,346–409；SHA256 `3b361a8bd055be3c07d53c7c311b3bb95b90728690218d7a2f93d2c392df6220`；Real MySql owner/Lane/source proof/independent JDBC/cleanup; M4 NOT_RUN。

- **R07** `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java`，line 136–200,202–233,344–410,444–512,519–581；SHA256 `2974ac2c004f28b5f046f2453ec760cea1259244b2fb6d847cebff770be6b7a7`；Original full baseline/four initializers; guarded MySQL/real auth/DAOs/MyBatis/result。

- **R08** `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/resources/ur06/enroll-mysql-client.mjs`，line 10–12,37–104,110–145,263–300；SHA256 `f595ed8725d170c193ec087597d2bc3e19fbed5db692c70d941426dd71874bde`；Existing shared source verifier; eight enroll subjects; no M4 host。

- **R09** `/home/isp/wsps/worktrees/ur06-enroll-mysql-20261008/agent/jia-agent-service/src/ur06EnrollMysql/ur06-enroll-mysql.init.gradle`，line 5–57,59–93；SHA256 `67f3c4ebf0830c5f3225f02931bf4b202393fce2a2b515f4378e575591f433ad`；Root/sourceSet/test dependencies/7env/real child classpath/one fork。

- **R10** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-mapper/src/main/resources/db/schema.sql`，line 208–263,265–307,495–517,616–653；SHA256 `f4bd5c7884263b935fd710669922340dfe06b283323e391a1cc81d37fd014977`；Complete original agent InnoDB baseline。

- **R11** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/user/jia-user-mapper/src/test/resources/db/schema.sql`，line 1–15；SHA256 `b17d06fa2ca4cd165769ae769f3f3047a7c0d2f790e792bc4b243fc1c78d5ddd`；Complete original user module test baseline。

- **R12** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/user/jia-user-mapper/src/main/resources/db/account-security-foundation-upgrade.sql`，line 1–14；SHA256 `817e25cb0125c22ce597be0bd5832d22c6626e1ed2bfa6385a841b5766da93d0`；Original account security baseline upgrade。

- **R13** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentSchemaInitializer.java`，line 24–36,70–105,2331–2356,2510–2527；SHA256 `a66b67356f71b3d6de184fd8326fabed87d5d3ee95d4273a1c8a594592b27e6c`；Latest9966 real initializer/identity/event constraints/original persona seeds。

- **R14** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeV1SchemaInitializer.java`，line 23–53；SHA256 `78a66cf5eba2cd0375fba3092e8026cd2ba275d32a160cd4a8e7f9b2d5a53c2e`；Original initializer, run unchanged。

- **R15** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentRuntimeSessionFenceSchemaInitializer.java`，line 25–55；SHA256 `501664e2264662c111ceb1f4d8270c7446e18450595bfa0ad463f905dc954a34`；Original initializer, run unchanged。

- **R16** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/config/AgentCommandTransportSchemaInitializer.java`，line 44–74；SHA256 `6df0a0482796fda488cc2ea21311d41a48c4000266716f2c45b67d6cc9056e69`；Original initializer, run unchanged。

- **R17** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-mapper/src/main/resources/db/agent-work-item-reassignment-e05.sql`，line 1–49；SHA256 `da1ceedd4bfad55f141613d9acdfccb7ee604127360f65f59e5bb053009dcda1`；Original E05 DDL lacks owner_jiacn。

- **R18** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-mapper/src/main/resources/db/single-tenant-task-owner-ddl.sql`，line 1–24,208–220,424–436；SHA256 `a6a065babe303e2771bef3f45dba4b915ebb0d7a49a08b62df395d8b0c6964bf`；Original additive owner Phase-A column/index; no business DML。

- **R19** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentWorkItemReassignmentMapper.java`，line 11–35,90–110；SHA256 `31c4aeeac3d386727caab5476bb4ec4ddbe8801dd1c3f1a2d99ac1345ac74522`；Real SELECT/INSERT requires owner_jiacn。

- **R20** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentWorkItemReassignmentController.java`，line 80–136,212–229；SHA256 `866ad358b75327bc8fa1f66c6e48f8094b876fd954d203c2785a8d7790f7f905`；Real readLease/start/heartbeat actor/nativeFence。

- **R21** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentWorkItemRuntimeResultController.java`，line 51–89,141–160；SHA256 `105ef193ef58a3ee9892c9bd41168396ab52aefdf612ad8b76442f326f83ba5b`；Real preflight -> opaque prepare -> refenced commit; original GET。

- **R22** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentWorkItemResultCommitServiceImpl.java`，line 211–259,262–283；SHA256 `24e5f54421413a552320e10ade33dae8793681a240f0cae8f66bd9ba09617cfa`；NEVER prepare; transactional source-locked commit/read/proof。

- **R23** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationService.java`，line 140–161,187–190；SHA256 `a882fe167eeaf7b30b6903b31a88e1c2a6c2bffc84bb05551af6fe4f8360ec7b`；Real DB auth/nativeFence/WSbinding。

- **R24** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCommandAckServiceImpl.java`，line 45–105；SHA256 `f05c0d3c248e2b50c30e924ea31035d6b7512de1f1c20e69fa81dd55698ba856`；Real D06 transaction, ADVANCED/PRIOR。

- **R25** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/build.gradle`，line 35–48；SHA256 `3729afac0b8ce7e7e644fb027207926232fb102a31fa3609288f5434c12c0093`；Existing testRuntimeOnly MySQL driver。

- **R26** `/home/isp/wsps/worktrees/ur01-unified-agent-runtime-20261008/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs`，line 14–18,488–543,729–755,776–781；SHA256 `d2b4e0f3bf8538846559d4685ca6e114fa58d3e17fd07784c9a64ffaae65e2a0`；Observed B candidate binds A; awaited one-shot callback; not main-accepted B。

- **R27** `/var/tmp/cyf-ur04-local-20261008T205238/run-acceptance.mjs`，line 14–43；SHA256 `14ccc4b8fe85376a9ff08ba4d738b19b5ed1f77560ff5bda4093f4ba3d1fb493`；Main-owned prior consumer wrapper; borrow target/allowed manifest/await backend。

- **R28** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentWorkAdmission.java`，line 12–24；SHA256 `d32f0f4b841ecfeb4a00c45f7d918cbe970c5b92d88b70df7a1650897881cda3`；Original schema-disabled non-hosted path。

- **R29** `/home/isp/wsps/worktrees/ur02-original-source-prereqs-20261008/agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillAgentVersions.java`，line 25–34,48–51；SHA256 `80290e25a4cd568581fa356e2e81fe19e0c2ffde9dccec9f2750ee36ab93691c`；Original marketplace-disabled path。

每个repo引用hash均与记录commit的gitblob比较通过；不对其他Owner随后移动HEAD作保证。仅报告自检，不是测试/构建/安装/发布证明。
