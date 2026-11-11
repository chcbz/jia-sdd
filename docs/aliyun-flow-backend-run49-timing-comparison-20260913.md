# 后端Run49启动对比与诊断接续（2026-09-13）

## 本轮实际推进

- 18:04 CST重新查询近期运行、18:09/18:12再核对Run49：后端5260799最新仍为Run49 FAIL，尚无诊断配置生效后的新启动。未重试/新建后端Run，未重启应用、未改SQL、未覆盖其他Owner文件。
- 重新解析两份原始应用日志，增加可复用只读日志算时工具，生成16个可对齐区间。**两次都是旧INFO日志，不是新增DEBUG效果。** 新工具的9个内存算术测试本地通过（0.027s），无JVM/DB/网络；不是正式云端构建或发布验收。
- 当前执行账本将F06失败归因为校验器的元数据契约与可见性：CREATE-only账号从COLUMNS读到0列、schema默认字符集错误代替显式table字符集比较，以及MySQL CHECK转义表示。已有责任Owner修复F06/E05 runner与测试。本任务不据此改表、扩权或移除校验；也不把账本中的修复计划当作已发布成功。

## 整体结果

| 指标 | Run40 | Run49 |
| --- | ---: | ---: |
| 云端测试与构建作业 | 473s | 379s |
| 部署作业（含最终失败步骤） | 798s | 1189s |
| Spring报告启动耗时 | 501.951s | 715.974s |
| Started时进程已运行 | 513.112s | 740.860s |
| 重复Mapper告警数 | 1070 | 1090 |
| 重复告警首末跨度 | 2.928s | 4.053s |
| Spring窗口内完成的GC pause合计 | 29.142s | 39.012s |

Run49云端构建反而快94s，慢的是部署/启动方向。Spring比Run40多 **214.023s（约42.64%）**。Run49从17:05:21创建到最后作业17:31:31结束约1570s，不能将整个26分10秒都称为Spring启动。

Run49安装后health UP、JAR匹配，但随后F06 schema步骤失败；部署作业1189s不能当成功发布时长。`READY_AFTER_SECONDS=839`是安装器健康轮询口径，不是JVM exec到ready的精确时长，也不等于Spring715.974s。

## Spring内部区间对比

单位：秒。**相邻里程碑的墙钟区间，非组件独占CPU/IO/Bean/SQL时长。** 两个样本不是同一JAR、同一负载的受控对照，不把增加值全归因于源码变化。

| 区间 | Run40 | Run49 | 增加 |
| --- | ---: | ---: | ---: |
| Spring内部计时起点（反推） → Starting主应用日志 | 10.908 | 24.116 | +13.208 |
| Starting主应用日志 → Spring Data扫描开始 | 64.060 | 89.976 | +25.916 |
| Spring Data扫描开始 → Spring Data扫描结束 | 2.936 | 4.052 | +1.116 |
| Spring Data扫描结束 → 首条Mapper重复告警 | 9.032 | 7.920 | -1.112 |
| 首条Mapper重复告警 → 最后一条Mapper重复告警 | 2.928 | 4.053 | +1.125 |
| 最后一条Mapper重复告警 → Web上下文初始化里程碑 | 49.110 | 66.935 | +17.825 |
| Web上下文初始化里程碑 → ChatClient MCP配置确认 | 57.939 | 111.103 | +53.164 |
| ChatClient MCP配置确认 → Redisson版本日志 | 47.002 | 72.937 | +25.935 |
| Redisson版本日志 → Redisson连接完成日志 | 17.967 | 20.935 | +2.968 |
| Redisson连接完成日志 → Hikari开始 | 17.098 | 33.054 | +15.956 |
| Hikari开始 → Hikari完成 | 9.907 | 15.987 | +6.080 |
| Hikari完成 → MyBatis insert检查 | 57.965 | 42.025 | -15.940 |
| MyBatis insert检查 → Camunda事务隔离检查 | 34.011 | 31.933 | -2.078 |
| Camunda事务隔离检查 → Camunda引擎创建完成 | 52.096 | 67.944 | +15.848 |
| Camunda引擎创建完成 → Tomcat started | 66.929 | 112.068 | +45.139 |
| Tomcat started → Spring Started | 2.063 | 10.936 | +8.873 |

最大的四个增长区间合计 **150.154s，占净增长约70.16%**：Web上下文→ChatClient配置、Camunda引擎完成→Tomcat启动、ChatClient配置→Redisson版本、Starting→Spring Data扫描。优先用定向Bean/lifecycle DEBUG解释这些区间，不能按区间末尾组件的名字直接归责。

Run49 GC pause占Spring约5.45%，比Run40仅多9.870s；重复Mapper告警首末跨度仅多1.125s。**它们不能单独解释214秒增长。** GC与区间墙钟时间重叠，不能再加到总时长中。Mapper注册工作不止告警输出，这里不估算全部扫描成本。

重新解析使用日志中最早Bootstrapping事件，Run40 Spring Data开始比旧手工表早4ms，因此相邻两个区间各修正4ms，总耗时不变。GC统计明确区分Spring窗口和整个进程窗口：旧报告168次/29.213s对应进程窗口；本表164次/29.142s对应Spring窗口。Run49分别为182次/39.077s和178次/39.012s。

## 资源方向的新增旁证（不是启动专属时长）

只读采样PID3598374的`/proc/.../task/.../schedstat`。采样时间：2026-09-13T10:13:22.411190+00:00。

| TID / 系统线程名 | 累计CPU秒 | 累计runqueue等待秒 |
| --- | ---: | ---: |
| 3598413 / C2 CompilerThre | 323.211 | 607.678 |
| 3598380 / java | 202.706 | 424.950 |
| 3598415 / C1 CompilerThre | 41.714 | 258.527 |

这些计数覆盖线程从创建到采样（包括启动后的运行），**不能把某一行的等待秒数直接从715.974s扣除，也不能将线程等待相加当总启动时间**。系统线程名`java`不足以证明它就是Spring main线程；本任务未attach/JVM线程转储。该旁证支持在下一次正常启动期间同步比较CPU争用，而非只盯SQL或GC；没有证据指定哪个其他任务造成启动延迟。

采样时JVM允许CPU为0-1；CPU控制组为`/user.slice`。根与该组`cpu.cfs_quota_us=-1`、`nr_throttled=0`，当前没有观测到CFS带宽节流记录。不能由此排除宿主机争用、调度等待、历史配置变化或虚拟化层影响，更不能推导已证明硬CPU配额根因。不调整/终止其他任务进程，不以资源读数新增发布门禁。

## 工具与下一次正常发布

工具：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/diagnostics/startup_timing.py`

```bash
python3 /home/isp/wsps/cyf/ops/ci/aliyun-flow/diagnostics/startup_timing.py \
  --run 49 \
  --source-sha 4be112cdde8397590760292eb04eb823ad88299d \
  --jar-sha256 dcab9c7105d5b9d30a8c3f37642dbb06259eb1b2a16a9b9f00ab574399cc3933 \
  --spring-log /var/log/cyf-api/startlog_20260913_171457.AM8vtq.log \
  --deploy-log /var/tmp/cyf-startup-debug-20260913/run49-deploy.log
```

- 只读快照，输出固定事件标签、摘要和时间，不复制日志正文/SQL/环境/密钥。源码/JAR身份由调用方传入，必须另外与Flow回执核对；参数存在本身不是身份验证。
- 新部署日志的`CYF_DEPLOY_TIMING`按component+pid+point配对，用单调时钟求差；嵌套区间不求和，缺失/失败/时钟倒退区间保留unknown。每次只处理同一机器、同一个Run；不能拼接不同主机/Run。
- 旧Run49没有新标记，工具正确输出`no_complete_spans`，不生成虚构的解包/JRE/健康细项数字。DEBUG Bean路径仍需结合新日志逐段解释；本工具不伪造Bean独占耗时。
- F06修复按原Owner的同制品受控运维路径完成，不为它重建/重启当前健康应用。下一次普通功能develop发布自然取得新启动样本；本任务不设等待队列，不为刷数据重启生产。
- 后续优化顺序：先根据四个最大增长区间的DEBUG细分初始化/依赖等待，再按实测决定初始化拆分和部署重复IO优化；CPU/GC/DB贡献分别报告。启动120秒仍为优化目标，不作为阻断上线的新增门禁。

完整数值、日志快照SHA256、精确源码/JAR绑定、资源原始计数和校验范围见同名JSON。该报告是新增测量和定位进展，**不是启动性能已达标或后端流水线已全绿的声明**。
