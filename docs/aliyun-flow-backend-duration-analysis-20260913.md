# 后端 Flow 构建发布耗时分析（2026-09-13）

截至 16:27:43 CST，直接查询 `5260799 / cyf-api-release` 运行、云端构建日志、主机部署日志，并只读检查发布状态及应用启动日志。未触发新 Run、未改配置/代码/测试、未操作进程。

## 时间分解

| Run | 源码 HEAD | 构建作业 | 部署作业 | 创建到结束 |
| --- | --- | --- | --- | --- |
| 38 | `741cc3f2668b` | 6m55s | 11m48s | 18m44s |
| 39 | `5bfdb2a83d8b` | 6m33s | 12m17s | 18m52s |
| 40 | `564e50fa6bb4` | 7m53s | 13m18s | 21m13s |

作业外主要只有 1–2 秒调度间隔，构建环境/源码准备也计入构建作业。不是长时间排队，也没有人工审查/审批阶段。

## 已证实的原因

1. **生产应用冷启动是正常发布的最大耗时。** Run39/40 输出 `READY_AFTER_SECONDS=527/521`（8m47s/8m41s）。Run40 Spring 日志明确 `Started JiaApplication in 501.951 seconds`；远端包约199MB，下载完成仅耗数秒到十余秒，停止旧进程仅4–5秒。因此不能把12–13分钟部署归因于制品下载。
2. **当前 Run48 叠加真实启动失败及恢复。** `d49a9b2239e8ad8d4f7643414ce22930589a2eb1` 云端构建5m54s，JAR `f9e98e213b233453989b92b5e3d2ad2d0354807e3c12db122d67ba7dc5225ed6`。15:59:51下载完成，16:04:32启动新进程；16:12:13报 `AgentWorkItemReassignmentServiceImpl` 构造参数缺 `AgentCommandTransportWriter` Bean，16:13:26开始恢复旧Run40版本。16:27:43仍为 Flow RUNNING / 本机 rolling_back、candidate_start_failed；health HTTP错误。这不是正常慢，也不是新版本发布成功。
3. **Gradle缓存配置不匹配。** 日志实际归档 `/root/.m2 /root/.npm /root/.yarn /go/pkg/mod /root/.cache`，约47KB，不含 `/root/.gradle`。源码工作区每Run清空，`_cyf_flow_build` 与 `_cyf_project_cache` 为新建目录。Run39/40/48均报告 `243 actionable tasks: 243 executed`，未命中任务输出复用。Run47可见重下Gradle9.3.1；成功Run前部日志被API省略，不能定量分开依赖下载与配置耗时。
4. **所谓Changed-scope目前是固定测试清单。** 16:16读取的当前配置有98个 `--tests`，没有按Git改动选择器。公共/core、agent、chat、oauth、user、wx等测试和整体bootJar同Run执行。该范围支持实际风险回归，但增量改动没有对应增量验证/编译收益；不能直接全删测试。
5. **连续失败放大总交付等待。** Run41–47七次在构建/测试阶段失败，实际运行时间累计29m54s，不含修复与两次Run之间的间隔。这与一次成功发布耗时是两个问题，应分开统计。
6. **主机启动资源争用与应用初始化范围大。** 当前主机2逻辑CPU，16:27 loadavg为33.87/26.57/21.73，短采样CPU idle为0%、运行队列36–43；恢复进程与本机其他工作共享CPU。未发现user.slice CPU quota或throttling，不能误报成硬配额限速。应用starter聚合多个业务模块，并启用MyBatis、Redisson、Camunda、AI等组件；Run40中Spring容器初始化127s，Hikari首次启动约10s，流程引擎相邻日志间隔约52s。日志间隔不等于单Bean耗时，须用启动阶段指标再定位。JVM Xms128m/Xmx384m有GC压力，但GC停顿不足以解释全部八分钟，不能只凭小堆就断言加内存能解决。

## 优化顺序（未执行）

1. 先修Run48生产装配缺Bean，并补同形态、最小范围的云端启动装配回归；不要以缩短健康等待掩盖失败。当前责任台账已在remediating，由原Owner修复，不重复触发。
2. 给云端JavaBuild配置真正的Gradle依赖/Wrapper缓存；随后验证任务build-cache与配置缓存兼容性。只缓存工具/依赖/可验证任务结果，不复用旧Run生产制品或旧测试结论。
3. 优先降低生产冷启动工作量：用阶段观测确认非必需初始化、重复Mapper扫描、AI/流程引擎初始化的实际成本；将生产运行资源与本机控制面/开发工作区隔离。任何资源调整需测量，不停止别人的任务，也不新增任意性能门槛。
4. 将固定98选择器改为组件变更与依赖影响驱动，保留本次功能相关的身份/事务/数据库回归；失败高概率、低成本的装配检查尽量前置。正式测试仍在同Run云端执行。
5. 部署剩余耗时含准备/校验/拷贝/最终核验，日志缺少独立时间戳，先补轻量阶段计时再优化重复I/O，不贸然删制品身份、进程归属、健康或可恢复安装检查。

完整非敏感运行绑定、阶段时间、日志摘要、局限见 `/home/isp/wsps/cyf/docs/aliyun-flow-backend-duration-analysis-20260913.json`；原始查询证据为本任务独立目录 `/var/tmp/cyf-api-flow-timing-20260913-3HlYKb`。Flow API正文包含 omitted-lines 提示，即使more=false也不视为完整日志。

## 深入复核补充（2026-09-13 16:46之后）

Run48最终已FAIL；部署日志证实旧Run40制品恢复健康，不是候选发布成功。同一旧制品恢复时Spring Started耗时724.048秒、进程754.038秒，健康轮询字段851秒。该轮询字段不是exec→ready完整时间，不能直接从日志文件名推算完成时刻。

运行包证实14个Application类；107个Mapper各重复注册10次，共1070条警告，但Run40警告只跨2.928秒，不能把八分钟全归因于重复扫描。恢复启动的启动前GC停顿39.405秒；两个时间点的高/低CPU采样也不支持“持续被其他任务占满CPU”的定论。启动期schema工作与reader READY路径全内容校验已在固定源码中确认，尚需独立阶段计时。

完整证据分级、根治架构、实施顺序和两分钟实际可服务目标见 `/home/isp/wsps/cyf/docs/aliyun-flow-backend-startup-remediation-plan-20260913.md`；该方案尚未实施。
