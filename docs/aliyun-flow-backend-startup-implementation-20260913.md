# 后端启动优化实施记录（2026-09-13）

## 当前范围与授权

用户已确认t5性能约束模式、CPU积分长期接近0（后读到0.1），并要求落实优化。实施分成两条：
1. 软件首批：拆分模块launcher与生产库运行图，保留业务配置/资源/模块独立启动能力，消除根应用重复装配。现有Flow执行相关云测、bootJar、同Run发布与健康核验。
2. 硬件：查询可变配规格及费用，确定持续算力方案；用户确认具体成本/目标及必要停机后才能变配/迁移。本次不购买实例、不改变计费模式、不重启收集样本。

完整资源归因：`/home/isp/wsps/cyf/docs/aliyun-flow-backend-resource-rootcause-20260913.md`。不再以CPU积分读取权限作为软件优化前置条件。

## 软件首批

- 任务：`API-STARTUP-ASSEMBLY-20260913`；责任Owner自检，无独立Reviewer。
- 独立worktree：`/home/isp/wsps/cyf/.worktrees/startup-assembly-20260913`。
- 起点为已发布远端develop：`feb492406efe849cff46681a93db2e8a274c14e1` / tree `903166bea4aca79b4ce6346fbdb66bb6bcb24983`，不是共享api工作区的其他未发布提交。
- 不修改ChatClient业务实现、鉴权配置、迁移或生产数据；后续批次再依证据处理Tools/MCP/schema/内容核验。
- 云端保持既有测试选择并补装配回归；检查实际生产classpath与Mapper覆盖，不只源码字符串检查。不以全局lazy-init、去掉必要Bean/功能或提前健康来降低数字。
- 发布入口只用 `5260799 / cyf-api-release`。查询时Run51 SUCCESS、无活动Run；发布前重新核对配置、远端SHA及是否已有自动Run。不创建新流水线、不执行本地Gradle/Vite构建。

## 持续CPU供给方案：明确未满足条件，避免盲目变配

目标实例：`i-wz9j3ip2unzhwij0bs30`，`cn-shenzhen`，已确认类型`ecs.t5-lc1m2.large`。

2026-09-13单次只读请求：
- API：`DescribeResourcesModification`，`ResourceId`为该实例，`DestinationResource=InstanceType`，`OperationType=Upgrade`。
- 结果：`Forbidden.RAM`，RequestId `01A09B27-39F6-5FBB-8895-3ECDE08B0FF4`。
- 没有取得可变配列表，不能据此宣称支持原地迁到某个非突发规格，也不能给出未查询的精确费用。原始响应受限保存于`/var/tmp/cyf-startup-assembly-20260913/DescribeResourcesModification-snapshot.json`。未盲目重试。

可执行的下一步：用户提供ECS控制台该实例**变配页可选规格及差价**（包含计费周期），或为当前身份增加该只读查询所需权限。不需要提供新密钥或管理员权限。

得到候选后按以下顺序决定：
1. 是否存在持续算力明确、兼容当前架构/磁盘/网络的非突发规格；若支持原地变配，优先评估以保持依赖地址与数据路径不变。不能仅看“几核几G”，也不假设跨实例族必然可变配。
2. 非突发2vCPU/4GiB作为同容量比较起点；按Java+MySQL+Redis/Rabbit/native与实际负载评估所需容量，不能承诺一定足够。给出实际费用差额、执行方式与停机影响后再获用户确认。
3. 若原地不支持，评估独立运行实例迁移；需要实际数据清单、数据库一致性备份/追平和可恢复切换方案。只迁Java必须把现有loopback依赖改为受ACL限制的私网连接，不能开放公网数据库。
4. 开发Agent/控制面与生产运行负载分离。其他任务进程只由其Owner协调迁移，不抢占或终止。新实例、存储快照及数据迁移涉及费用/生产数据时须明确授权。
5. 沿用现有Flow并更新精确目标，确认同Run制品、版本、服务归属、互斥、健康和恢复能力；不引入重复流水线。对照先在隔离环境验证，避免两份应用同时消费生产队列/调度任务。

优化目标≤120秒只作观测，不设等待超时或资源预留门槛。软件变化和硬件变化分开记录，未实测前不承诺提速倍数。

## 状态

软件实现进行中；硬件可变配清单/费用等待控制台证据或对应只读权限。候选提交、云端测试结果、制品与Run证据将在实际取得后补充，不把Run51旧成功冒充优化发布。


## 进行中状态（2026-09-14 更新）

- 软件首批已完成并推送 `develop`：commit `95dbf79b6f9dfa2f813cfa4b343338f17ce92c51`，tree `fe02d1352e414b18ec52da0c779e4145105aa0ec`，分支 `codex/startup-assembly-20260913`。
- 自检：根生产 main 运行图只保留 `cn.jia.JiaApplication` 一个 `@SpringBootApplication` 与一个 `@MapperScan`；`jia-common-test` 的测试入口仅测试 classpath，不进 bootJar。模块独立入口全部移入 `src/launcher` source set 与 classified jar，独立启动能力保留。
- 旧子 Agent 在实现中达用量上限后，由主控制面接管并完成提交；没有本地 Gradle 构建。
- 推送 develop 后 4 分钟未观察到自动触发（与历史“webhook 交付未验收”一致），使用 flow-control 单次写入启动 `Run53`；结果 `returnedRunId=53/UNKNOWN`，只读复核确认 Run53 已 RUNNING、repo/branch 匹配，没有重发。最终以终端态和源码/制品证据为准。

## 首批软件优化完成与证据（2026-09-14）

- Flow `5260799 / Run53 SUCCESS`，源码 `95dbf79b6f9dfa2f813cfa4b343338f17ce92c51`，tree `fe02d1352e414b18ec52da0c779e4145105aa0ec`。
- CI job `514860129` SUCCESS：`:starter:test`、`validateLayering`、`:starter:bootJar` 全过，`BUILD SUCCESSFUL in 2m 26s`，bootJar 邮件运行时类校验通过。
- 部署 job `514860130` SUCCESS，部署单 `69541831`，1/1 Success/healthy；installed record 同 source/tree/run53。
- JAR SHA256 `5346a76db34ff2535a270785d248fb46e0373b89a4af80460494284e8376c235`；receipt `9ca4663cf0042a1d472398b8797f3622d3ef024daec47f8ea9bc08a1b8a25f1e`；PID `4063696`；health `200/UP`。
- 启动对比（同一诊断口径）：
  - Mapper 重复注册告警 `1090 → 0`。
  - Spring `Started`：`534.026s → 437.961s`，缩短 `96.065s`。
  - `application.run`：`579.014s → 488.013s`。
  - 启动步骤 `1369 → 1330`；GC `181次/31.086s → 157次/26.379s`（完整窗口口径不同，趋势一致）。
- 结论：软件首批已生效并上线；剩余约488秒仍由 t5 性能约束模式、积分近零导致的 CPU 供给不足及既有初始化逻辑主导，未达到120秒目标。下一步仍是持续算力实例方案，不承诺软件继续叠加速优化可补偿。
- 完整证据：`/home/isp/wsps/cyf/docs/aliyun-flow-backend-run53-release-evidence-20260914.json`。

## 第二批软件优化完成（2026-09-14 Run54）

- 提交：`49f983ade3e57256395256276e44d992df14bd76`，tree `dea330db92ce2725debe1e1b44cf724c19942745`，已推送 `develop`。
- 变更：
  1. `application-prod/grey.properties` 增加排除 `McpClientAnnotationScannerAutoConfiguration`，避免 MCP 关闭后仍创建 `clientMcpSync/AsyncHandlersRegistry`。
  2. Camunda `processEngine` 及服务 Bean 加 `@Lazy`，`WorkflowServiceImpl`、`RestListener` 注入点加 `@Lazy`，首次工作流使用时再创建引擎。
  3. `ArchiveContentStore.listAllParagraphs` 一次查询替代逐章 `listParagraphs`，`verifyPersistedContent` 批量核验。
- 主机侧：`/usr/local/sbin/cyf-api-kit` 的 `--spring.autoconfigure.exclude` 增加扫描器排除项；备份 `/usr/local/sbin/cyf-api-kit.bak.20260914_round2_mcp_scanner`，`bash -n` 通过。
- Flow `5260799 / Run54 SUCCESS`：CI job `514914946` `BUILD SUCCESSFUL in 2m 20s`；部署单 `69546567` 1/1 Success/healthy；线上 health `200/UP`，PID `4116315`。
- 制品：JAR SHA256 `ce5ae63bfcc68ba918102b76f349486a16b1214572a48d442307439a2463c0ad`；receipt `ad5f5a8322a1f9150330d457bfa546de319584a94bf04cfbf59b4831bbbc1af6`。
- 启动对比（同口径）：`Started 437.961s → 360.022s`；`application.run 488.013s → 388.129s`。
- 证据：`docs/aliyun-flow-backend-run54-release-evidence-20260914.json`。

## 第三批软件优化与软件侧结论（Run55/Run56）

- `Run55` 提交 `8b522184` 只做注入点 `@Lazy`，Bean 仍是非懒单例，因此 `chatClient` 仍在启动期创建；启动 369.133s，与 Run54 基本持平（CPU 积分噪声内）。
- `Run56` 提交 `9fdd2e6a` 在 `chatClient` Bean、`MemoryRepositoryImpl`、`ChatTools`、`LongTermMemoryServiceImpl`、`DefaultSummaryGenerator` 上加 Bean 级 `@Lazy`。`chatClient` 与 memory repository 不再启动期创建；Run56 `SUCCESS` 且健康，但本机 CPU 积分受限下启动实测 384.906s（慢于 Run54 的 360.022s），说明剩余耗时主要来自 CPU 饥饿，不是这些 Bean。
- 三个 Run 均部署成功：Run54 `360.022s`、Run55 `369.133s`、Run56 `384.906s`，差异与 CPU 积分噪声一致；均 `health 200/UP`。
- 当前 develop 最新：`9fdd2e6a3a8d6e4f53ab2d26be7af1122eeca3ce` / tree `fc048e58c97b7e68bda9b295b5f3e0d10f2f0cdb`。
- 证据：`docs/aliyun-flow-backend-run54/55/56-release-evidence-20260914.json`。

### 软件侧剩余空间（实测，不设门禁）

| 项 | Run54/55/56 self | 类型 | 说明 |
| --- | --- | --- | --- |
| `config-classes.parse` | 54.2 / 50.2 / 57.0s | CPU 类路径/配置解析 | 可用 `spring-context-indexer` 生成索引，但涉及多模块构建改动，收益需在正常 CPU 上重测 |
| `agentSchemaInitializer` | 34.0 / 27.0 / 32.0s | MySQL DDL/元数据 | 已做列/索引/触发器等迁移，批量查询可进一步压缩但风险高 |
| `redisson` self | 14.1 / 14.0 / 18.0s | Redis 客户端创建 | 自动配置，延迟初始化需改动 starter，且锁依赖需核对 |
| archive schema/manifest | 6.2+7.0 / 7.1+7.0 / 11.0+15.8s | DB+清单 | 受 CPU/磁盘影响，Run56 噪声最大 |

结论：软件侧还能做的都是较大重构，且当前 CPU 积分近 0 时测量不占优；继续叠软件优化不划算。按用户决定由用户处理服务器规格，软件侧暂停进一步实验，保持 Flow 云端构建/测试/发布。

## 当前使用与证据

- 后端发布统一走 `5260799 / cyf-api-release`（develop push 自动发布链路，webhook 交付仍以实际 Run 为准；未自动触发时按授权手动启动一次并核对源码）。
- 本机不跑 Gradle/Vite 生产构建；正式测试、bootJar、同 Run 制品上传、安装与健康核验都在云效完成。
- 前端发布统一走 `4403172 / cyf-web-kit`；如未启动，先核对 webhook/源码后单次手动触发，不新增重复流水线。


## 2026-10-22 只读复核与局部候选（不重标历史发布）

核对范围：当天6份启动日志、当前IMDS实例类型、archive manifest源码；源码基线 `7841057b057c012cfa203fb658c1043500be055e`，局部候选 `2c6f894419c2495b48360460b325af1f3f75ae56`。其他模块保留原核对基线。

- 当天Spring Started为60.015～458.031秒；18:28 JVM的Started为306.888秒，且Runner随后仍在执行。该日志不是readiness证明，不能按Started判定60秒验收成功。
- 当前仍为ecs.t5-lc1m2.large（IMDS只读确认）；当前积分余额未取得，不能直接沿用9月零余额判定当下限速。当前线程累计调度等待仅支持继续检查算力/争用，不量化启动窗口贡献。
- 源码局部优化将manifest canonical JSON的每字符串ObjectMapper调用换为同一Jackson库的直接转义，保留所有文件/内部/段落摘要与持久内容核验。轻量等价性探针通过，不是云端正式回归或整机启动收益。
- 用户本轮目标≤60秒，只作真实就绪验收目标，不设杀进程超时、不把必要初始化延后伪装启动完成。当前未达标、未发布。完整边界/证据/后续选择器见 `docs/implementation/handoffs/API-STARTUP-60S-20261022.md`。
