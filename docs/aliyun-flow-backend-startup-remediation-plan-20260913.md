# 后端启动与 Flow 发布的长期整改方案（2026-09-13）

> 资源层最新结论（2026-09-13）：本文件早期的“缺完整trace/资源未归因”状态由Run50及后续排查更新；当前实施优先级、t5基线、CPU计数限制和监控权限缺口以 `/home/isp/wsps/cyf/docs/aliyun-flow-backend-resource-rootcause-20260913.md` 为准。以下历史故障与设计保留，不当作当前待办全已完成。

> 20:02更新：真实计时已由Run50正常发布完成，1369个步骤全部配对；新证据与按贡献排序见 `docs/aliyun-flow-backend-run50-exact-timings-20260913.md`。旧INFO相邻区间不再作组件归因；新的application.run579.014s，不是已优化至2分钟。

## 结论与范围

这是诊断和实施设计，不是已完成优化的发布报告。本次只读查询 Flow、生产启动日志、运行制品目录及固定 SHA 源码；没有本地构建、启动 Run、修改线上配置或操作进程。

两分钟作为用户提出的 **JVM exec → 实际可服务** 优化目标，不能承诺未测量的收益，也不成为超时取消、假健康或跳过功能的门槛。当前已确认重复装配、启动期数据工作、构建缓存缺失和生产装配测试缺口；**没有完整启动 trace，尚不能把全部 500–724 秒准确分摊到各 Bean、CPU 调度和外部等待**。

## 1. 证据基线：先分清四种时间

源提交：
- Run40：`564e50fa6bb4889d6f0b7221de57b4c22116a810`，成功制品 SHA256 `20625639587936a543bdbe1fdadef65f4d478bebe0227475937ae2b85105716e`。
- Run48：`d49a9b2239e8ad8d4f7643414ce22930589a2eb1`，失败候选 SHA256 `f9e98e213b233453989b92b5e3d2ad2d0354807e3c12db122d67ba7dc5225ed6`。
- 流水线：`5260799 / cyf-api-release`。2026-09-13 16:44:34 CST 查询 Run48 为 FAIL；16:46:29 部署单 `69526810` 为 Failed，部署日志证实恢复旧版本后 HEALTH=UP、ARTIFACT_ATTESTATION=MATCH。随后本机 health 返回 HTTP200/UP。**恢复成功不是 Run48 新版本发布成功。**

| 指标 | Run40 正常发布 | Run48 恢复同一 Run40 制品 |
| --- | --- | --- |
| Spring `Started` 报告 | 501.951s | 724.048s |
| 同行 `process running for` | 513.112s | 754.038s |
| 启动脚本 `READY_AFTER_SECONDS` | 521s | 851s |
| `Started` 前 GC 停顿 | 168次 / 29.213s | 167次 / 39.405s |
| `Started` 时刻 | 13:13:43.359 | 16:26:01.290 |
| main线程后续启动日志示例 | 13:13:58.363 SpringDoc | 16:27:55.432 SpringDoc |

注意：`READY_AFTER_SECONDS` 的起点在启动进程、校验 JAR 和写运行记录之后，取值在健康探测和最终核验之前；**不是完整 exec→ready 的秒表**，也不能直接加到日志文件名时间得出精确完成时刻。此前口头按851秒推算的“约16:27:38”不作为实际完成时间证据；原日志表明16:27:55之后才输出启动完成，部署命令16:28:43结束。

Run40 总计21m13s：构建7m53s、部署13m18s，作业外约2s；部署内约8–9分钟是启动，剩余约4分钟含准备、身份/完整性校验、拷贝、最终核验，不能全部算成健康等待。199MB左右下载仅数秒到十余秒，旧进程停止4–5秒。

## 2. 已确认的结构问题与归因边界

### A. 生产包混入多个应用入口，重复全域扫描（确定存在，收益待测）

在固定源码和恢复后的 `/opt/cyf/service/api/cyf-api-kit.jar` 中均确认：
- 根 starter 依赖13个子 starter；运行包包含 **14个 Application 类**，包括本不应进生产运行图的 `SimpleTestApplication`。
- 其中11处相同 `@MapperScan({"cn.jia.*.mapper"})`，根入口处于 `cn.jia`，其他入口也在这个包。
- Run40启动日志：**107个 Mapper，每个重复注册告警10次，共1070条**；另有10条“未发现 Mapper”告警。恢复启动完全相同。
- 这不是14个 JVM，也不意味着这些类的 `main()` 被调用；问题是可执行入口与库配置混用、重复参与配置扫描。
- Run40重复告警出现于13:06:48.344–13:06:51.272，仅约2.928s。前期配置解析成本未单独记录，**不能声称消除1070条警告就能省六分钟**。

源码定位（须用上述 SHA 的 git show，不以工作区当前文件替代）：
- `/home/isp/wsps/cyf/api/starter/build.gradle`
- `/home/isp/wsps/cyf/api/starter/src/main/java/cn/jia/JiaApplication.java`
- `/home/isp/wsps/cyf/api/base/jia-base-starter/src/main/java/cn/jia/SimpleTestApplication.java`
- `/home/isp/wsps/cyf/api/workflow/jia-workflow-starter/src/main/java/cn/jia/JiaWorkflowApplication.java`

### B. 可选能力的装配边界不完整（Run48失败的确定原因）

`AgentCommandTransportWriterConfiguration` 按 `AgentCommandOutboxEnabledCondition` 注册 Writer，而 `AgentWorkItemReassignmentServiceImpl` 构造器必需该依赖。Run48直到启动后段才报缺Bean并退出，随后再付一次旧版本冷启动成本。

需要修复整个功能图的启停语义，并在云端验证与生产相同的配置组合、runtime classpath。不能通过总开关全部开启、伪造 no-op Writer 或全局懒加载让容器表面启动成功。原功能 Owner 已在处理该装配问题，本方案不重复启动发布。

### C. 启动线程承担数据初始化和内容完整性工作（工作存在；分钟级贡献未测）

固定 Run40 源码证实：
- `ChatSchemaInitializer` 是无条件 ApplicationRunner，逐列检查、补列、检查/调整索引，且有必需的身份/会话字段校验。
- `ArchiveBootstrap` 在 reader启用时同步执行 schema初始化、manifest加载和导入/激活。实际生产启动参数启用了 reader。
- `ArchiveContentImporter.activateExistingReady()` **已有READY快路径，并不是每次都重复插入**；但仍在work/edition锁定事务内调用 `verifyPersistedContent()`，按block查询并比较完整内容，核验3677段。
- 部分 Agent schema初始化在 `afterPropertiesSet()` 内，但有功能条件；不能认为所有初始化器都在生产执行。
- `Started` 后恢复日志仍有约114秒的 main线程启动日志间隔；这不是114秒已经归因给Archive。须给每个Runner、SQL组、锁等待独立计时。

源码重点：
- `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatSchemaInitializer.java`
- `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveBootstrap.java`
- `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveContentImporter.java`

### D. 运行耗时波动明显，但“内存不够/别的任务抢CPU”尚不足以作总归因

同一Run40制品两次Spring启动相差222.097秒（约44%）。可能涉及负载、缓存、SQL/锁、配置或数据状态；不是受控对照试验。

- 主机2逻辑CPU/约3.7GiB；JVM识别2可用CPU、2个并行GC worker、1个并发worker，不存在已证实的CPU识别膨胀。
- Xms128MiB、Xmx384MiB、Metaspace上限192MiB。Run40的GC停顿约占Spring启动时间5.8%，不是八分钟的主要直接停顿来源；并发GC、分配和JIT还需采样。
- 16:27恢复期间CPU idle为0%、runqueue36–43；16:45附近采样idle92–95%、无实时swap-in/out。繁忙不是恒定基线，不归咎于未归属的其他任务。
- 已查CPU cgroup未见硬quota或throttling。生产进程落在用户会话资源域，不是独立服务资源域。
- Run40 Hikari首次建立连接约9.9秒；容器中间初始化日志127秒；其他空白间隔数十秒。它们可能嵌套，**不可相加或把相邻日志间隔等同某个Bean执行时间**。

### E. 云端构建反复冷执行（确定存在）

缓存归档路径未含实际Gradle用户缓存，归档只有约47KB；Run39/40/48均243任务全部执行；Run47重新下载Wrapper。当前98个固定 `--tests` 不是按变更动态选择。Run41–47七次失败累计运行29m54s，属于返工成本而非单次启动成本。

## 3. 目标架构与具体改法

### 第一批：修装配结构，同时补可归因的观测

1. **一个生产启动入口**：拆清普通library/autoconfiguration与独立launcher。根starter依赖业务库和显式配置，不再依赖包含其他Boot入口的可执行模块；各模块独立启动能力若仍需保留，移至不进入根runtime的launcher source set/module。SimpleTestApplication移至测试源集。不是仅用打包exclude临时遮住类。
2. **一次、明确范围的Mapper扫描**：根装配负责一份明确的业务mapper集合，或模块各自负责互不重叠范围。保留所有现用Mapper，验证事务代理、授权和计划任务注册不重不漏。
3. **整图条件装配**：定义transport off/on支持矩阵；关闭时依赖该能力的入口与服务遵守明确“不支持”语义，而不是构造器强依赖缺失Bean；开启时真实Writer、schema和安全约束齐全。修正BPP过早拉起普通Bean的依赖路径，不把警告统一隐藏成基础设施角色。
4. **测量随正常发布走，不另外开审批或预检流水线**：Spring启动步骤采集（候选BufferingApplicationStartup/FlightRecorderApplicationStartup，按项目Boot4版本核验API），为Bean、Runner、schema/manifest/engine/init输出起止与结果；发布脚本统一单调时钟阶段计时。
5. 下一次获授权的正常发布由服务自身启用一次受控启动JFR/CPU采样，不对别人的进程临时attach。证据带Run/SHA/JAR digest，受限目录留存；不公开actuator startup/env，不采集密钥、SQL参数或用户内容。

必须得到的分类：应用CPU（扫描/类加载/JIT/解密）、GC、文件IO、socket/DNS/TLS、SQL/锁等待、线程park/调度等待。StartupStep可能嵌套，用独占时间/关键路径分析，不能将耗时简单相加。

### 第二批：把启动工作改成“版本变更才执行”，不把问题推到首请求

1. **schema版本化**：把现有逐次DDL转为审计过的版本化迁移，建立已有库baseline与兼容策略。仅有schema变更时，Flow同Run在切换前执行允许的增量迁移；普通重启只检查版本与本功能必需的不变量。生产DDL、索引调整和数据导入按实际授权执行，本方案未执行任何数据库操作。
2. **内容发布与进程启动分离**：reader内容版本更新时完成加载、全量验证和原子激活；不让普通代码重启承担内容发布。当前READY路径先优化为批量读取、消除按block往返，并保留锁顺序与等价完整性校验。只有建立不可变版本存储、写权限约束及可验证内容摘要后，才能采用版本级证明减少重复全量读取；不能仅凭一行READY记录跳过真实完整性。
3. **可选组件按业务事实启用**：盘点Camunda、Redis/Redisson、LDAP、Elasticsearch、Rabbit、AI等实际生产功能依赖；确实不用的能力不创建连接/扫描/后台线程。正在使用的工作流、消息和模型能力不能为了计时关闭。必要依赖仍完成真实就绪校验；真正可选的预热移至后台并报告自身状态，不挤占关键启动路径。
4. **不做全局lazy-init**，不以提前返回HTTP200移走成本。必要Runner完成、真实readiness、端口/PID/制品身份正确及关键业务首请求均需要被观测。全局health与readiness不能凭名称当作等价，须验证当前自定义health包装和安全配置。

### 第三批：按测量调整资源与发布生命周期

- 将生产API迁入专属、归属清楚的systemd service/resource domain，Flow只控制该服务并核验同Run制品。不默认引入K8s/微服务或新流水线；不停止其他任务，不用低硬CPU限额制造新的启动阻塞。
- 堆预算依据启动/稳定期live-set、分配峰值和吞吐目标；整机预算包含heap、metaspace、direct/native、线程栈、JIT、MySQL及其他常驻服务。先消掉无用装配再做受控JVM参数对照，不直接猜1G/2G，不把更大Xmx当根治。
- 如果采样证明2核共享环境无法满足目标，再提出独立运行主机/扩容的实际成本方案并获授权。迁走构建能减少本机构建负担，但不自动减少生产运行自身初始化。
- 部署阶段细分为：队列、下载、验收、锁等待、备份/安装、停止、JVM exec、context、runners、readiness、稳定核验、最终回执。大文件在跨信任边界时验证；同一受控不可变文件可复用本事务的已验证结果，不能删除签名/哈希/归属检查。先测出多余约4分钟，再删重复I/O和重复完整树校验。
- 非破坏性下载/验证尽量在停止旧服务前完成，发布互斥仍等待。双JVM蓝绿仅在实测容量、端口、后台调度/消费和锁隔离均满足时评估，**不在3.7GiB主机上默认并跑两套服务**。

### 第四批：让云端构建真正增量化

- 确认实际 `GRADLE_USER_HOME`，恢复Wrapper与依赖缓存；按OS/架构/JDK/Gradle及依赖配置隔离/失效，凭证不进缓存。
- 开启并验证支持任务的Gradle build-cache，固定可信写入来源；审计自定义任务输入、输出及路径可迁移性。configuration-cache单独验证插件兼容性，不一键全开。
- 将98个固定选择器改为变更模块+反向依赖影响；build/dependency/根装配变更扩大覆盖，未知映射不能漏测。外部状态相关集成测试不可依赖不完整缓存键跳过。
- 最小生产形态装配回归覆盖真实runtime图与实际开关，DB/Rabbit使用云端隔离依赖，不能被test专用Boot入口、mock Writer或H2差异掩盖。复用现有测试作业，不额外强制CI-only重建。
- 最终bootJar只产生一次，测试/构建/制品/部署绑定同Run；测试证据同时绑定tree、selector和fixture摘要。不把旧Run测试结果或生产包冒充当前发布。

## 4. 实施顺序与验收（无新增人工队列）

| 顺序 | 交付物 | 完成证据 |
| --- | --- | --- |
| 1 | 原Owner修transport装配；生产形态回归与计时 | off/on有效组合通过；精确候选在既有Flow中成功，不再发生缺Bean才恢复 |
| 2 | 单入口/单次Mapper扫描、配置边界 | 运行包无测试/其他launcher；1070条重复注册消失；原功能和事务代理保留 |
| 3 | 按trace排名修初始化/数据库往返/运行争用 | 相同功能集下关键路径实际缩短，不只日志变少 |
| 4 | Gradle缓存+影响选择、部署重复IO消除 | 缓存restore/hit与任务状态可见；阶段耗时对照；同Run制品身份和健康有效 |

缓存修复与启动诊断可由同一Owner分步交付或由不同Owner持有不重叠路径推进，不等全部架构整改完成才让普通功能发布。ready代码合入develop→既有流水线云测、构建、发布，不创建Reviewer/新门禁/临时流水线。

验收口径：
- **启动目标≤120秒**：从JVM exec到必要初始化完成、readiness和关键业务可服务；同步记录首次关键请求，不能将耗时挪到首请求。超过只记录和继续优化，不因性能目标自行取消可用服务。
- 同一候选固定JAR/SHA、JDK、生产开关与依赖版本，对照明确的CPU/内存环境、数据库/内容状态与缓存冷暖条件；尽量在云端同规格隔离环境采样，线上利用正常发布验证，不反复重启生产刷分。
- 报告每次样本与范围，不能用少量启动虚构P95。正常发布和失败恢复分开；Spring Started、实际ready、部署完成分开。
- 缓存/扫描/迁移优化只按实测贡献结算，暂不承诺总发布固定几分钟；所有功能、身份/事务/实际健康和可恢复安装继续保留。

## 5. 证据与未解决的测量缺口

原时序报告：`/home/isp/wsps/cyf/docs/aliyun-flow-backend-duration-analysis-20260913.md`。
本次结构化补充：`/home/isp/wsps/cyf/docs/aliyun-flow-backend-startup-evidence-20260913.json`。
本任务查询目录：`/var/tmp/cyf-api-flow-timing-20260913-3HlYKb`。

现有Flow日志有omitted-lines，不能声称已取得完整构建日志。现有启动日志没有Bean级CPU/IO/锁时间；官方文档网页检索本次也未返回可读内容，因此具体诊断API/插件兼容性在实施时需按项目锁定版本核验。本报告不使用未获取的文档充当证据，也不将设计建议称为已验证优化。
