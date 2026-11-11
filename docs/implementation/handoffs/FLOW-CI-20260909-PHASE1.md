# Flow CI 第一阶段执行记录

**后续修正：OpenCV已在原流水线私仓中认证核实可访问；新CI未迁移私仓配置是实际遗漏。用户选择优先优化原流水线1466118；原流水线尚未修改/触发。见`../plans/FLOW-CI-20260909-legacy-optimization.md`。**

**最终进度（2026-09-09 19:08 +08）：云端执行链路已建立，但后端冷构建尚未通过。Run2缺少OpenCV依赖，唯一账本`FLOW-CI-COLD-01`已进入`blocked_root_cause`，停止Run3。根因与后续有界整改见`FLOW-CI-COLD-01-R2-ROOT-CAUSE.md`。**

2026-09-09。仅后端云端定向测试/冷构建；无部署、无生产数据库操作。原前端4403172、后端1466118均未修改。

## 已完成

- 新建手动流水线 `5256653 / cyf-api-kit-ci`；18:29 +08 API仍为零运行，当前配置是 fail-closed 占位符。
- 桥源码 `7599ee83cdcd2ca413d66ee2253de88fb97d9beb` / tree `f12eb71603877e3113320d960445b0aba8de0881`，Raman独立ACCEPT，P0/P1/P2=0/0/0。
- 原gpt_test_runner启动时502/unknown provider，未执行测试；替代验证者Herschel独立执行11项fake-wrapper测试全部PASS，native rc0，shell语法和diff检查rc0。没有真实Gradle/npm/数据库操作。
- 证据 `/tmp/cyf-flow-ci-verify-6vm8LceG/SHA256SUMS` 已逐项校验。受唯一账本只读Agent容量约束，Reviewer释放后才接纳验证；未改变其他任务归属或进程。
- 已逐字节集成7个受审文件，原orchestrator hash预检通过；未重置/暂存整个dirty工作区。文件摘要见 `docs/implementation/plans/FLOW-CI-20260909-integration.json`。

## 冻结冷构建

- API实际构建commit `6267f3b16fe7b672a3c8479f058a662d9c75216c` / tree `936d6e4bcf3d7a4cc23cde62fa0e697be93d659b`。
- 源码tip以实际Flow取源为准，云端新checkout显式detach6267；不把移动develop当作固定构建SHA。
- selector `backend-cold-smoke-v1`：SensitiveDataSanitizerTest、validateLayering、starter:bootJar，保留PublicArtifactVerifier。
- ticket `/tmp/cyf-flow-tickets/FLOW-CI-COLD-01-r1.json`，SHA256 `64a99c4158cdc359c97770e8e7a688d89e3ae7ab23c6dfe0aea45fada6ff34a7`，截止21:27:11 +08。
- tool bundle `dd6fda10799f987c440cd176001fe91e66785675f7c5453f77c653bd334ab9c1`。
- 待审配置 `docs/implementation/plans/FLOW-CI-20260909-cold-r1.yaml`，SHA256 `b83edeb71175a4a068551f4739522f157e9da0c20cefb2a32f70571e34ddae2f`。
- 官方内置变量：PIPELINE_ID流水线号、BUILD_NUMBER运行号、CI_COMMIT_SHA源码tip、CI_COMMIT_REF_NAME分支。`cloud_ci.api_ci`仅为逻辑job key，数字job ID必须由主控认证API另外映射。
- JavaBuild记录native rc后上传receipt引用文件/XML及哈希，不上传冷缓存。**最后必需Command门禁**返回native rc并检查receipt；前置“证据收集”成功不代表构建成功。

## 尚未完成

等待精确流水线payload独立审查；通过后update一次、readback、记录触发前上下文，再start一次。请求不明确只读核查，不盲目重发。

冷构建通过也不代表全量API测试、MySQL/Rabbit集成或生产部署通过。root-owned制品安装、联合release tuple、schema门禁、健康/业务验收属于后续阶段。

## Run1 实际结果（18:38:55 +08）

- update/readback/start均成功；readback仅终止换行不同。Run1 / API job511920863，云端build job546257705，LARGE_3C6G。
- Flow源码tip1911a370fbaf8cf705eb1fe85e8d2e9a294ace6d，实际detached构建6267/tree936d；receipt确认前后clean。
- JDK21.0.2、Wrapper9.3.1云端冷下载成功。Gradle native rc1：cold-init.gradle23把File传给仅接受String的pluginManagement.includeBuild；业务测试0、JAR未产出。不是测试通过或部署成功。
- 失败证据上传成功，最终必需门禁rc1正确使Run失败；未原样重试。
- 同Run制品5490字节，SHA256913dd5000339f77cfdb89b12f603c920d45524f9288012a10e1a19fb0ee02624，下载到/tmp/cyf-flow-ci-download-run1/；签名URL未落盘。
- ticket逐字节一致，inspect证据完整性通过且正确返回failed/automatically_accepted=false（inspect rc1为预期失败分类，不是第二次运行失败）；已导入failed证据。
- 已交回原Owner定点修复File-to-String并加静态回归。新工具/新ticket/新配置必须独立审查后才可另启Run2；不复用Run1 nonce。

## Run2 结果与停止点

- 原Owner修复工具commit e091630a50a09dfc7906b5b5d6848844ac910aa1/tree d53d0450995c4c1b14298cb80fcda8495e0f9f77；两文件有界delta、12/12 fake tests PASS、Raman独立ACCEPT。
- 新ticket 0f41e4f8a38dff3b9f16cb44d51924dc56309d504c0d25ca22cc070fee4d9b8c，新bundle5745e0794b0dada73b08d3a5c866eb667d3baeed623e7bbfbe9ef5da86a6a0a7，新nonce/path，YAML134f7b0c9de224bda391d1c46667f2973b395bb8b755a8a750e86ebfe0f51ac7独立delta ACCEPT后update/readback/start各一次。
- Run2 / job511938036，19:02:22 native构建结束rc1；settings插件云端成功编译，common-core编译因org.opencv:opencv:4.5.5无法解析而停止。业务测试0、应用JAR未产出，未部署。
- 从认证Run2 actions下载4798字节失败证据包，SHA256a8f0c6373092588c8f31de7327d7da7012e2fa94d2e065a8a47ebf998331ba6f；ticket一致，工具/命令/源码认证绑定与inspect完整性通过，已导入failed evidence。没有将失败或测试0报为通过。
- 19:07唯一账本累计2次云端失败，owner释放、blocked_root_cause，禁止盲目Run3；源码工具及控制配置ACCEPT不改变业务构建FAIL。完整矩阵见同目录FLOW-CI-COLD-01-R2-ROOT-CAUSE.md。
- 本轮未运行任何真实本地Gradle/npm构建，没有重启/停止服务、推送API/Web分支或变更旧生产流水线。

## R3：源码已接受，配置写入前置校验失败

复用新5256653，旧流水线不变。私仓/OpenCV修复755537/21ac独立ACCEPT及20PASS已集成；创建加密组44254。单次受审配置更新被云效以变量组引用不存在拒绝，回读仍为旧R2，未启动Run3。待控制台变量组ID或服务端定位后另审控制配置，不重跑已通过轻量测试。详见`FLOW-CI-COLD-01-R3-CONTROL-BLOCKER.md`。

## Run3 最终结果

控制台组ID已解决关联问题。云端nativeGradle0、201tasks、4suites/72PASS、bootJar与OpenCV摘要通过；随后bridge制品扫描预算超限返回70，Run3 FAIL、无交付JAR/部署。下一步只做不放松门禁的诊断设计，详见`FLOW-CI-COLD-01-R3-RESULT.md`。
