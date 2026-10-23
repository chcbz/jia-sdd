# 后端 Flow 端到端五分钟：诊断与实施顺序

核对：2026-10-16 19:42 Asia/Shanghai。Owner：本聊天（backend-flow-5m）。本轮仅只读诊断及记录，不登记开发/发布完成。

## 范围与固定源码

目标：沿用5260799，在保留必要测试、分层/依赖完整性、同批制品、互斥/备份/恢复和真实业务就绪的前提下，评估从Flow Run创建至部署及在线核验完成≤300秒。排队不能隐藏；无排队执行耗时另报。冷缓存、热缓存和源码变化分别报告，不设置300秒强制中断。

非目标：不切换项目后端本地默认策略，不恢复develop自动部署，不新建流水线，不购买资源，不重启/迁移生产，不修改其他Owner的代码或诊断配置。

- 根HEAD e05498ed8f8d67d791ad8d269ae5bbc00b3592e6 / tree 3e7418605fef2d518aa9b04643c9936dd9a06abc；根工作区有大量已有修改，不覆盖。
- API HEAD 58b4b5f408257c6d5103d915e13c7927c1571e20 / tree 3e60bd5858735790b7886ef00a9a94614816fb75；本轮未修改API。
- 19:39左右只读ls-remote：根/API远端develop分别等于上述HEAD。不把这些源码当受测候选或线上版本；未构建/发布。
- 路径 /home/isp/wsps/cyf；工具入口 ops/orchestration/README.md、ops/ci/aliyun-flow/flow-control.cjs、既有aliyun-pipeline只读SDK脚本。
- 若进入跨仓实现，沿用 api/docs/interface-standard.md 的2026-10-14冻结规范，本轮不改变接口。

## 实时查询事实

1. 5260799当前配置只有Backend develop CI / JavaBuild / ArtifactUpload，没有部署阶段。配置SHA见current-config-summary.json。仍留有owner-fixture-diagnostics诊断内容，不能用历史模板整份覆盖共享配置。
2. 最近Run139是2026-10-08 19:28:26创建、FAIL；来源codex/ur02-ci-eac15d-20261008，commit eac15d988445784e9004fa393bdce8671ca96dab。不是当前develop的验收。
3. Job531048271：19:28:27至19:53:30，1503秒；从Run创建到该作业结束1504秒（25分04秒），无部署。
4. 日志显示缓存获取19:28:38→19:28:40，归档500493657字节；恢复至19:28:46成功。恢复插件约8秒，不是本样本20分钟空白的原因。
5. JavaBuild步骤起点19:28:46；19:53:28报告BUILD FAILED in 4m22s。步骤至该报告1482秒，减Gradle自报262秒，剩余约1220秒未归因。不能将差值直接称为依赖下载、JDK安装、排队或Gradle前耗时；缺少真实边界。
6. 平台内容明确省略676行。SDK more=false不代表完整，现有log字段只有content/more，本地tail还发生截断。必须获取控制台原始日志或下一次显式诊断Run补齐。
7. 明确失败项为 :agent:jia-agent-service:ur03RuntimeHttp / Ur03RuntimeHttpDbAcceptanceTest.realRuntimeHttpD06PersistsAcrossApiJvmRestartAndFencesRotatedGeneration，2项中1失败。只有失败位置，不冒充根因。不得删除该回归换取通过；当前develop是否已修复需精确源码验证。

证据：本目录recent-runs.json、current-config-summary.json、run139-timing.json、run139-log.json。原始头部缓存时间和平台省略标记另见run139-log-boundaries.json。

## 可复用但不能冒充Flow验收的历史证据

2026-10-09本地同SHA干净worktree对照：compile-only缓存，207任务中77个编译任务命中；282测试及layering/fresh bootJar实际执行。Gradle115.254秒、打包23.381秒，总138.635秒。另一次默认缓存收尾为156.492秒。见 docs/implementation/handoffs/BACKEND-RELEASE-10M-20261009.md 和同名evidence目录。

历史安装307.357秒来自另一批日志文件起止；既不是当前主机基线，也不能与138.635秒拼成端到端实测。只说明单优化构建不足以证明五分钟。

## 实施优先级

### P0：先找回约20分钟空白，建立成功基线

- 用Run139原始日志确定JavaBuild插件准备、wrapper分发、命令前处理、实际Gradle调用及日志输出边界。若原始日志不可取，在下一次明确授权的无部署诊断Run内记录单调计时并上传完整脱敏日志；复用5260799，不新增runner/流水线，不反复重试旧失败输入。
- 比对当前固定源码是否已修复UR03失败；如未修复，先归因测试及夹具，保留跨JVM重启、代际隔离与数据库语义。
- 若确认慢在每次安装JDK/工具/fixture，才做固定版本工具预置/可信缓存；若慢在依赖解析，按实际请求日志处理仓库与凭据/网络问题。不能在没有证据时盲目换实例。

### P1：将已验证的compile-only策略适配至Flow

- 不是把本地release metadata init直接搬入Flow：它绑定本地build ID与admission。Flow需保持自己的pipeline/run/source和制品证明。
- 缓存依赖及JavaCompile内容寻址输出，保留测试、validateLayering、依赖完整性与fresh bootJar；禁止缓存测试结果和生产JAR。不减少selectors来制造提速。
- 首次检查当前Flow Gradle home/cache包含项与实际命中；不要只增加--build-cache就声称有效。共享缓存只允许可信来源，禁止将配置/密钥/测试数据库或整套build输出打包。
- 最早验证：同一固定源码的填充Run与新工作区热缓存Run，分别记录编译命中、实际测试数量、分层与bootJar fresh状态、JAR摘要和全程时间。含源码改动的候选也必须测，不能只展示同SHA全命中。

### P2：安装与应用启动

- 使用已有CYF_DEPLOY_TIMING / StartupTimeline及diagnostics/startup_timing.py，按精确PID/制品分解下载、验签/摘要、备份、停止、启动、schema和在线检查。先取得当前样本，再决定修改点。
- 当前installed lifecycle有5秒稳定健康观察，不能把历史307秒简单归因为sleep；不删除稳定健康、身份/端口归属或摘要核验。
- 若当前测量仍是初始化瓶颈，优化重复扫描/依赖初始化和数据库往返；保留事务、ACL及schema一致性，不用全局lazy-init把工作推到首请求。
- 若证实CPU调度/算力瓶颈，再评估隔离生产与开发或资源变更；资源费用、生产切换另行明确授权，不操作其他聊天进程。

## 300秒的可行性判断与验收

若Flow也能达到历史本地构建打包的139～156秒，则平台准备、传输、安装及在线核验合计只剩144～161秒。此为必要时间余量，不是已证明的阶段预算；当前20分钟未归因及历史5分钟安装都必须有新实测证明解决。

完成标准：明确发布版本和完整commit/tree；同Run完成必要测试/构建/制品上传及安装；记录不可变制品摘要、目标实体目录、安装恢复边界和线上版本/健康/业务smoke；Run创建至全部核验≤300秒。报告冷/热缓存、排队和不同源码条件，失败不能算快速成功。

本轮结论：已完成瓶颈诊断与实施排序，未修改云端配置、未触发Run、未实现/验收五分钟部署。下一动作优先取得Run139原始日志；实际发布验收还需明确版本与源码，不用任意develop触发生产。

## 2026-10-16 21:16 实验更正/新证据

最初“约20分钟未归因”现已由历史实时快照定位至RPM准备，详见rpm-root-cause.json。固定官方OSS JDK压缩包在新Run141/142/143的**冷缓存**准备分别6.138/6.470/6.697秒；GitHub端点在Run140超时，已换相同SHA的官方OSS，不重试旧失败网络输入。

当前源码的现行生产JVM只读核验：PID1187775、19:51:09启动、canonical JAR attestation MATCH、health UP；对应现有1.16.7本地批次、源码58b4b5f。Spring Started56.107s，但仍不能当成完整安装/业务就绪耗时。原307秒仅历史样本，不应用于当前耗时承诺。

Run142揭示默认Flow与新源码不匹配：仍调用10月15日源码5d54634已删除的chatDeliberation任务。根据现存50文件/49测试类映射到7个维护中的任务，并补2个已迁入默认suite的回归；所有其他原selectors保留，不恢复旧兼容suite、不删除失败测试换取性能。完整实测与热缓存对照尚待本轮运行结果。
