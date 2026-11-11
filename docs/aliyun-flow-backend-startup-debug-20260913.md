# 后端启动 DEBUG / 阶段计时落地记录（2026-09-13）

> 19:07最新：已改为真实Spring步骤BEGIN/END及Runner子步骤计时。Java候选经CI14通过但尚未发布；启动开关及Lifecycle TRACE已由Ops6安装。下文17:54内容为第一阶段历史，当前状态见 `docs/aliyun-flow-backend-startup-exact-spans-20260913.md`。

## 状态

截至2026-09-13 17:54:27 CST：**诊断工具已由现有运维流水线安装，后端发布配置已保存并精确回读；当前JVM未重启，实际DEBUG启动数据尚待下一次正常发布。**

- `5264702 / cyf-ops-manual` Run3 SUCCESS，作业514679069 / 部署单69529100，25项云端测试全部通过。随后原子安装两份固定脚本，线上SHA256与候选一致；未调用应用生命周期、未执行SQL。
- `5260799 / cyf-api-release` 仅修改部署命令的诊断环境前缀，配置readback MATCH；没有启动后端新Run。当前JVM仍使用原日志配置，不会因保存YAML而开启DEBUG。
- 后端Run49整体FAIL，但应用安装已PASS、制品MATCH、health UP，`READY_AFTER_SECONDS=839`。失败在安装后的F06 schema验证：`agent_task_artifact_outcome` 出现 `created_table_not_equivalent`（两项check clause、columns、schema charset、table collation不等价），另一张decision表pending_create。不能称整条发布成功，也不为取日志重复已知失败。

## 实施范围

- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_startup_diagnostics.py`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/auto/install-startup-diagnostics.py`

脚本自身默认关闭；后端发布YAML现默认传入1，可用运行变量0覆盖。只有受控Flow部署环境显式设置 `CYF_API_STARTUP_DIAGNOSTICS=1` 才打开。不读取任意外部日志配置或Java参数，不改变现有授权/健康/事务/锁判断。

### Spring定向DEBUG

仅三类logger：

```text
org.springframework.beans.factory.support.DefaultListableBeanFactory
org.springframework.context.support.DefaultLifecycleProcessor
org.mybatis.spring.mapper.ClassPathMapperScanner
```

用于定位Bean创建、依赖装配、生命周期启动及Mapper注册。保留root与security INFO。不启用全局debug、完整自动装配条件报告、Environment、Hikari配置、SQL/JDBC参数、HTTP wire或AI正文日志。

**DEBUG只补充执行路径，不自动提供每个Bean的独占耗时。** 如果仍出现没有起止的耗时间隙，再通过正式云端构建接入Spring ApplicationStartup，不能把两个DEBUG事件间隔伪称成单个Bean耗时。

日志沿用受限 `/var/log/cyf-api/startlog_*.log`，对外只输出筛选后的阶段摘要。诊断logger随这一JVM的配置保留；下一次正常发布设置 `CYF_API_STARTUP_DIAGNOSTICS=0` 恢复原日志级别；分析结束后移除流水线诊断默认值。不能声称ready后自动关闭，也不为关闭日志额外重启。

### 部署单调时钟标记

格式：`CYF_DEPLOY_TIMING component=... pid=... point=... monotonic_s=... wall=...`

stderr仅固定标记、PID、单调时钟及墙钟时间，不输出argv、环境或secret。失败的日志写入不改变主流程退出结果。

覆盖：
- 发布锁、生命周期锁等待。
- installer解包与候选验证、回退备份、停止核验、原子替换。
- JRE整树验证、启动前JAR哈希、JVM派生、PID/制品身份记录。
- 实际health等待、既有5秒稳定核验及其JAR哈希。
- 两次完整status，以及每次status内JAR哈希和health。
- 最后canonical摘要、安装完成记录与自动授权消费。

按component+pid+point匹配begin/end算时长。阶段有嵌套，不能直接求和；只有begin没有end的失败/截断区间报告未知，不能当0秒。`jvm_spawn`记录进程派生边界，不谎称精确JVM内部exec时刻。下载适配器早期copy/receipt校验尚未加点：其源码有另一个Owner已整合但尚未安装的schema hook，本候选不覆盖它。

## 云端验证与安装证据

`5264702` Run3：

| 项目 | 结果 | 用时 |
| --- | --- | --- |
| 新增诊断夹具 | 14/14 PASS | 38.795s |
| 既有安装策略夹具 | 8/8 PASS | 20.140s |
| 既有安装互斥夹具 | 3/3 PASS | 2.052s |
| 验证命令总耗时（含准备开销） | PASS | 64.052s |

以上是测试耗时，**不是Spring启动耗时**。无本地Gradle/Vite生产构建。运维测试以固定内嵌包为输入而非组件源码提交；包SHA256：`df576c0cc6a9cf2de783adb5d4cc8264934904a2670d06c09175f5ebdd8ffa42`。

安装器在既有自动发布锁、release锁、lifecycle锁内等待后执行基线哈希检查、备份、原子替换和readback。只安装两份固定脚本，不覆盖其他Owner的部署适配器/schema hook。前值及结果保存在 `/var/lib/cyf-api-flow/diagnostic-tooling/<manifest-sha256>/`。

| 脚本 | 安装前SHA256 | 安装后SHA256 |
| --- | --- | --- |
| lifecycle | `d4525dd5e8e34faf5d28a9f635315b54f7cc1b6bf82f9fcf7637670718c4b275` | `9662e166af188603f86c43cd43f0685e09ed9e4cb5f19ea4e0c44849c4e8a215` |
| installer | `10217d0091353b6f103737fc195d4293aa6365bb901914e32397019ee5042733` | `31a433483ecf8d28f2de2795a1154701a323c02ec941f16595146165a24e4ac2` |

后端YAML更新前SHA256：`443b75b5efcee828128b306d74f9691828178c2aa6d2a81cb2caee983548a1f0`；候选及readback：`89198f0b4df526c7385b2bb5ba9abc7680ddca3c7485bcc97dec9db764aca9c4`。只增加诊断环境前缀，不改测试、制品、部署目标、schema行为或健康判断。本地release模板同步同一行，未提交其他Owner的改动。

### 已归因的历史失败

- 本地14项诊断测试曾12通过、2个完整安装夹具触发既有15秒子进程限制。增加超时最后阶段输出后，云端在**相同15秒限制**下14项通过；未放宽限制，不能据此认定历史超时唯一原因是CPU。
- 运维Run2因内嵌包缺少既有策略测试读取的 `cyf-api-flow-deploy` 失败；补齐测试输入后Run3通过。该文件只供测试读取，未安装覆盖。
- 首次候选保存收到1209300 YAML校验错误，嵌套错误未保留；缩短作业名称及调整编码后的新候选保存通过，不能宣称已证明具体平台大小阈值。

## 运维入口与后续执行

- 继续复用 `5264702 / cyf-ops-manual`，无源码push触发，不新增流水线。当前默认 `CYF_OPS_ACTION=verify` 仅执行隔离夹具验证；显式 `verify-and-install` 才在验证后安装固定的两份诊断脚本。两种模式均不重启应用、不执行SQL。旧只读预检YAML前值已留存。
- 下一步由F06责任Owner修正已知schema不等价问题，具备发布条件后按既定develop自动发布流程执行；本任务不改表、不重试Run49、不增加审批门禁。
- 下一次正常后端发布采集同Run的Flow部署日志和受限Spring启动日志，绑定完整源码SHA/JAR摘要，输出锁等待、解包/备份、JRE/JAR校验、JVM启动、Bean/生命周期路径、健康核验的分段耗时。现阶段没有新的启动耗时结论。
- 私有控制证据：`/var/tmp/cyf-startup-debug-20260913/ops-run3.log`、`release-debug-update-result.json`、`release-debug-before.yaml`；完整配置不复制到公开报告。

## 18:12 后续只读分析

新增Run40/Run49原始日志对比：`docs/aliyun-flow-backend-run49-timing-comparison-20260913.md`及同名JSON。Spring由501.951s增至715.974s，增长主要集中在四个初始化观察区间；新增只读算时工具及9个轻量内存测试。尚无新DEBUG启动样本，不将该对比当作诊断开关效果或优化成功。
