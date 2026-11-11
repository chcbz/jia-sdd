# 后端真实启动步骤计时（2026-09-13）

## 20:02 CST 最新结果：已发布并取得完整实际样本

**后端5260799 / Run50 SUCCESS**，develop `1f89f109`，同Run JAR83a449137 / receipt b1154747，部署单69531195，PID3702039、canonical摘要和HTTP200/UP已核验。新增两个测试纳入原生产Run，103类选择范围、Gradle175秒成功。

**1369个真实启动步骤全部配对，另有33个部署配对、8个Lifecycle配对。**application.run579.014秒；Spring框架Started报告534.026秒；JVM创建到稳定健康623.100秒。配置解析93.118秒、chatClient依赖包络133.993秒、阅读器Runner41.011秒已落实到实际BEGIN/END，不再用相邻日志推断。

完整起止表、父子扣除和优化排序：`/home/isp/wsps/cyf/docs/aliyun-flow-backend-run50-exact-timings-20260913.md`；全量CSV/JSON同名。schema依赖由Ops7完成，本次release的F06既有两表等价核验也已通过。自动push Run仍未观察到，核对后只补启一次Run50。

## 历史准备状态（已由以上Run50结果取代）

此前Run40/49的“相邻日志区间”不能确定每个组件从何时开始、何时完成，不再将其作为步骤耗时归因。现改用**实际调用边界的BEGIN/END**，并保留父子关系。

截至19:07 CST：
- 源码提交 `1f89f109e4a8c8565755f298ac10c1df94124031`，tree `0ce7ecc69b23d44a278a94a37d6f7c953f02c769`，已推送 `codex/startup-exact-spans-20260913`。**尚未合入develop/发布，不是线上运行版本。**
- 现有后端CI `5263690` Run14 SUCCESS：新增原生Bean/失败语义/嵌套/并发/关闭/无敏感输出等测试类、最小Boot+Runner测试类，以及4个阅读器/聊天schema既有回归类均被命令选中，对应test任务与bootJar成功；Gradle142s。未取得JUnit XML计数，不虚报整次测试方法总数。
- CI制品JAR `83a449137fdfa2344e3849ef94d1893c44093a0037aa9515e8922a1260e57627`，221177024 bytes；只在云端构建，没有安装此CI制品。手动CI已恢复原develop默认配置，未留下诊断分支作为共享入口默认值。
- 运维 `5264702` Run6 SUCCESS / 作业514703256 / 部署单69530406：41项夹具通过，总验证36.045s；安装了下一次启动所需的明确开关及Lifecycle TRACE。线上helper摘要与候选一致。**未重启应用、未执行SQL。**
- 尚无包含该Java提交的生产启动样本。不得把代码/采集器测试成功、旧INFO间隔或测试夹具时间冒充线上步骤计时。仍需在不破坏F06基于Run49同制品修复的前提下，将候选合入develop正常发布并采样。

## 19:42 CST 实际发布推进

- 已读取Ops7实际部署日志：`schema-complete` SUCCESS，F06既有表等价、缺失决策表创建后等价，E05创建后等价，未重启应用。此前Run49制品绑定修复依赖已完成；不重复执行schema修复。
- 计时代码已fast-forward合入远端develop `1f89f109`，未改动其他源码。原release YAML仅增加core/starter两个新增测试选择，保存/readback SHA256 `213e3d06bdd10686ed6793ac464f18427051520429638b669085162a2c1ce108`，保留所有原测试、制品、安装和schema逻辑。
- 本次push后多次只读核对未出现自动Run；19:41只补启一次正常生产Run50，构建Job514711922，部署Job514711923。截至19:42 RUNNING。自动触发仍未验收，不宣称webhook工作正常。
- 等待Run50实际新JVM日志；尚不能报告本次真实步骤耗时。无本地Gradle构建、无本地安装/重启、无新增流水线。

## 记录什么，起止在哪里

| 范围 | 开始 | 完成 | 归属 |
| --- | --- | --- | --- |
| 原生Spring启动步骤 | 框架调用 `ApplicationStartup.start()` | 同一步骤 `StartupStep.end()` | 唯一ID、父ID、线程ID、步骤名 |
| Bean创建/初始化 | `spring.beans.instantiate`开始 | 同一Bean的框架步骤结束 | beanName；包含初始化/依赖的包络，不冒充单个构造函数或SQL时长 |
| 原生配置/后处理/SmartInitializing步骤 | 框架已有步骤开始 | 同一步骤结束 | 框架步骤名及安全元数据tag |
| 四个Runner | 原有run方法入口 | 原方法返回或抛异常 | archive、archive-question、chat-schema、permissions-refresh |
| 阅读器schema/清单/导入 | 实际方法调用前 | 返回/抛异常后的finally | schema、reader-schema、manifest-load、import-activate |
| READY重启事务/内容校验 | 原有事务方法入口、原有校验调用前 | 对应方法返回/抛异常 | ready-restart-transaction、persisted-content-verification；不改锁/事务边界 |
| 问答初始化 | schema调用前、worker.start调用前 | 各自返回/抛异常 | question-schema、question-worker-start；start返回不等于异步工作全部完成 |
| Lifecycle Bean启动 | `Starting bean` **TRACE** | `Successfully started bean` DEBUG | 同Bean配对；只开DEBUG缺少开始事件 |
| 部署阶段 | 既有 `CYF_DEPLOY_TIMING *.begin` | 对应 `*.end` | installer/lifecycle+PID+阶段；覆盖锁等待、解包、备份、停止、激活、JRE/JAR核验、健康、两次status、安装提交 |

运行包实际依赖为Spring Boot4.1.0 / Framework7.0.8，不以Gradle Boot插件声明4.0.1代替实际运行版本。已从当前JAR提取官方类，使用javap核对接口及Lifecycle调用边界；未做本地编译、未attach JVM。Framework7.0.8的`doStart`确实在调用bean.start之前使用TRACE、返回后使用DEBUG。

## 数据格式与判读

`CYF_STARTUP_STEP`每条包含：`event / id / parent / thread / name / wall / monotonic_ns`。

- BEGIN是实际步骤入口；TAG只记录白名单元数据；END包含实际结束时间、`duration_ns`、`outcome`。没有结束就报告“尚未结束/日志不完整”，不能当0秒，不能用下一条日志补结束。
- `outcome=ended`仅表示框架关闭了scope，不代表业务成功；显式Runner/子步骤保留success/failed，原异常照常传播。
- 总耗时采用单调时钟差；UTC墙钟保留给人阅读与跨日志对照。Lifecycle TRACE/DEBUG本身只有墙钟，不能假称单调纳秒精度。
- 有完整summary、事件数量/父子关系均匹配时，才能计算“本层墙钟=包络墙钟−已记录直接子步骤的区间并集”。这仍包括调度/IO等待和未细分工作，**不是纯CPU时间或Bean独占业务执行时间**。
- 同线程父子关系真实配对；并发线程独立root，不虚构跨线程父关系。多个并发步骤不能直接相加。
- `CYF_STARTUP_SUMMARY`记录steps/open及输出耗时观测；日志截断、输出异常、缺失父步骤时不计算本层时间。输出耗时只统计sink调用，不假称覆盖全部埋点开销。
- 应用run返回后停止采集新运行期步骤，不持续记录请求。尚未结束的已有异步scope可以保留真实结束；不是强制结束后台工作。

不记录SQL正文/参数、环境、配置值、异常正文、请求体或密钥；不开放新actuator端点、不代理Bean、不变更Runner顺序/条件、权限/事务/迁移行为，不新增时限/资源/性能发布门禁。

## 开关与代码

- 显式参数：`--cyf.startup-tracing.enabled=true`。缺省关闭，false关闭。
- Flow既有 `CYF_API_STARTUP_DIAGNOSTICS=1` 由受控生命周期脚本转成此参数，并将仅Lifecycle logger调整到TRACE；root/security保持INFO。不要依赖被子进程环境清理掉的环境变量直接进入JVM。
- 新Java代码必须实际进入发布JAR后才有Bean/Runner步骤；安装启动参数本身不会给旧JAR补代码，也不会改变当前运行JVM。
- 源码在 `/home/isp/wsps/cyf/.worktrees/startup-exact-spans-20260913/common/jia-common-core/src/main/java/cn/jia/core/diagnostics/`；入口为该工作树的 `starter/src/main/java/cn/jia/JiaApplication.java`。
- 只读解析器：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/diagnostics/startup_timing.py`。输出 `actualStartupSteps` 和 `lifecycleSteps`；旧`spring.intervals`仅历史辅助，不用来替代实际配对。
- 解析器16项云端夹具覆盖实际起止、嵌套扣除、缺失/截断、负单调时钟epoch、失败仍有耗时、跨线程误归属及Lifecycle必须有TRACE开始。

## 运维下发修复与证据

原运维YAML后来追加了另一个Owner的schema-plan/schema-complete逻辑。本次保留其脚本字节，仅更新本任务诊断包。合并后的145140字节内联YAML虽然保存成功，Run5在下发约1秒内失败，没有机器/作业命令日志，未进入安装。另一次Run4也在同一入口前失败；不将它归因到应用初始化。

现在用1547字节Flow配置校验并执行**完全相同的固定脚本**：
- 受限目录 `/var/lib/cyf-api-flow/startup-diagnostic-command-bundles/`，root:root目录0700，文件0600，SHA256寻址；本地只保存候选字节，不执行测试/安装/SQL。
- Flow检查固定文件的非链接、root归属、单链接、权限及SHA256，才执行。所有schema/diagnostic动作字节保留，选择仍受`CYF_OPS_ACTION`控制。
- 固定命令SHA256：`d806aea7dc3337961a9284139563a4900afd56bd8e110a4493811dd50bbabf5a`。
- 缩短下发配置后同一脚本Run6通过。平台未返回具体拒绝原因/阈值，不能虚构一个已证明的长度上限；这次修复不跳过测试或业务校验。固定文件是该主机运维入口的配置依赖，换主机必须先按摘要准备，缺失时失败而非伪成功。
- 当前`verify`只跑隔离夹具；`verify-and-install`验证后只安装诊断helper；schema-plan/schema-complete仍由其责任Owner按既定授权和Run49绑定执行，本次没有调用这些动作。

已安装lifecycle：`5b1a1851478aa37d0628c897cad34e944bf38a9cb286342dc59fce92508ed89c`；installer未改变：`31a433483ecf8d28f2de2795a1154701a323c02ec941f16595146165a24e4ac2`。

私有证据：`/var/tmp/cyf-startup-spans-20260913/ci14-status.json`、`ci14-job-scoped.log`、`ops-run6.log`、`ops-compact-intent.json`、`ci-restored.json`。同名JSON为结构化摘要。

历史计划（现已完成，勿重复执行）：保留当时Run49制品供原Owner完成F06修复；在正常develop发布中集成1f89f109，并把两个新增测试类加入该Run测试选择。发布后取同Run部署日志和新JVM原始启动日志，按实际BEGIN/END导出每步开始/结束/耗时/父子关系，届时再判断具体慢步骤；不为了提供数字而编造历史开始时间。
