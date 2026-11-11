# API-STARTUP-60S-20261022

- Owner：当前聊天主 Agent；目标：JVM 创建至必要初始化和 readiness 完成 ≤60s（观测验收目标，不设超时杀进程/降级健康）；非目标：部署/重启、变配计费、削弱 schema/内容完整性、全局 lazy、终止其他任务。
- 已读取 `/home/isp/wsps/cyf/AGENTS.md`、`api/AGENTS.md`、`ops/orchestration/README.md`、`ops/ci/aliyun-flow/README.md`。接口固定规范 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2/2026-10-14；不改 wire。
- 本地 api HEAD `94b4c8a5e5b1402ef44097b5a337a75431a0ec1b`/tree `ba133c85ae1d3f456d4c3c3f39bd0a41380744c9`，分支属于其他任务，不更改。
- 2026-10-22 18:37 CST 远端 develop 实查 `7841057b057c012cfa203fb658c1043500be055e`，独立工作区 `/home/isp/wsps/worktrees/api-startup-60s-20261022`，branch `codex/api-startup-60s-20261022`；base 为该 commit（后续远端可变化）。根工作区已有大量无关修改，保留。
- 基线证据 `/home/isp/wsps/cyf/evidence/api-startup-60s-20261022/baseline-timings.json`，复用 `ops/ci/aliyun-flow/diagnostics/startup_timing.py`，不是新建 runner。今天六次 Spring Started 为319.012/60.015/336.943/370.994/458.031/306.888s；Started 不含 Runner，最短实例的 job 注册还晚4.019s。
- 最新日志 `/var/log/cyf-api-flow/startlog_20261022_182819.YksHnO.log`，PID719501；GC暂停14.513s/124次，非分钟级主因。日志跨阶段一起变慢，不能把相邻里程碑差值当单Bean耗时。当前 IMDS 只读确认 `ecs.t5-lc1m2.large`；CPU积分当前值未知，历史零积分不作当下实测。`thread-counters.json` 是进程累计 CPU/调度等待，不是启动独占窗口。
- 最早验证：保留目录和字符串转义/摘要字节等价；正式 Java 回归与 validateLayering 经 Flow5260799。18:41 CST 查询 Run234 RUNNING，归属其他任务，不覆盖配置、不取消、不新建流水线。
- 优化候选范围：阅读器 manifest canonical JSON 热路径重复创建序列化器；所有文件摘要/内部摘要/逐段校验与数据库 READY重读、锁、事务保持原样。预计收益必须实测，不能以此承诺整体60秒。
- 定位/实现/验证/等待实际耗时：未完整计量；开发完成与上线等待分开记录。

## 2026-10-22 18:56 CST 进展（未完成60秒目标）

- 候选本地 commit `2c6f894419c2495b48360460b325af1f3f75ae56`，tree `0059c1ded11d32d96e8a584d08e402481183418d`；仅2个文件，尚未推送/合入 develop。使用 Jackson2 原生 `JsonStringEncoder` 直接写入既有 StringBuilder，避免每个字符串走 ObjectMapper；不改摘要格式、锁、数据库读取或启动顺序。新增转义/Unicode、键排序及嵌套格式回归，原完整fixture与坏摘要测试保留。
- 本机仅轻量诊断：用生产包中已存在且记录SHA的3个Jackson库，javac编译6个独立内容类、改名基线与临时Probe；不启动Spring、不连数据库、不调用Gradle、不打生产包。全量fixture摘要验证、ASCII控制字符/中文/emoji转义等价、篡改拒绝 PASS。探针 `/home/isp/wsps/cyf/evidence/api-startup-60s-20261022/Probe.java`；源/依赖/证据摘要见 `result.json`、`probe-libraries.json`。
- 探针计数：整树26739个字符串访问（canonical实际排除manifestSha256键值对，即26737次）。交替顺序四组载入，baseline 18136/2985/1869/2053ms、candidate 9869/4142/1078/1893ms。共享JVM预热与主机争用影响明显，其中一组候选更慢，不能声称稳定提速比例，不能用首次8.27秒差值充当生产收益。
- 既有时间解析器16项单测 PASS；`git diff --check` PASS。正式Java JUnit、validateLayering、Flow精确候选测试、整体启动和生产发布均未完成。不得复用Run234作为本候选验证。
- 18:53 CST复查Run234已SUCCESS；18:55 CST详情确认其源码是base7841057b、只有资源卸载CI作业。本候选无Run。当前已无该活动Run阻塞，但默认CI测试选择器未含ArchiveManifestLoader/Bootstrap/Importer；共享policy/template已有其他任务修改，本任务未覆盖配置。后续须协调现有5260799的精确候选与定向选择器，并保留既有回归/validateLayering。
- 安装记录（非独立制品闭包复验）指向Run233/base7841057b/tree57b0add0c4bf89c313f179d6a365508cf58f9b62，candidate_sha256=244f2b6e208bf9794cb5da2ce506903b40acc24aa8483dece30e293c154f5e03。不把Run234 CI成功冒充新安装。
- 下一步：完成Flow定向回归并集成；在明确授权的版本化发布窗口保留既有StartupTimeline逐步计时及JVM至readiness完整口径，取得同窗口CPU积分/调度指标；再决定是否需要持续算力或进一步削减装配成本。当前未部署/重启、未启用收费性能模式、未修改生产配置；60秒未验收。
