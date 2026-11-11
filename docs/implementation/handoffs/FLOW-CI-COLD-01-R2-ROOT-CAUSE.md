# FLOW-CI-COLD-01：第二次云端失败，停止执行循环

**归因已修正（用户提供私仓线索后完成认证核查）：OpenCV在既有私仓且可访问，Run2实际是新CI遗漏私仓/认证，不是制品缺失。用户最新选择复用新流水线5256653，见`../plans/FLOW-CI-20260909-R3-REMEDIATION.md`及独立计划审查；旧1466118/4403172不变。以下两次失败记录保留为历史，计划接受不等于新运行授权。**

2026-09-09 19:05 +08。状态：`blocked_root_cause`，禁止Run3/原样retry/本地补跑。无生产数据库、服务操作或部署；旧流水线不变。

## 根因矩阵

| 尝试 | 精确工具 / 固定API | 第一实质失败 | 已确认范围 | 整改状态 |
|---|---|---|---|---|
| Run1 / job511920863 | tools7599ee83；API6267f3b/tree936d6e | cold-init.gradle23向PluginManagementSpec.includeBuild传File，而API仅接受String | 公开Git取源、fixed detached SHA、JDK21、Wrapper9.3.1冷下载、失败制品上传及最终rc1门禁有效；业务测试0 | 原Owner提交e091630a，absolutePath String + 静态回归，12/12 fake tests PASS，独立ACCEPT后精确集成 |
| Run2 / job511938036 | toolse091630a；API6267f3b/tree936d6e | `:common:jia-common-core:compileJava`无法解析`org.opencv:opencv:4.5.5`，阿里公共Maven镜像及Maven Central均无该坐标 | settings插件已由同一源码在云端编译成JAR，5个Gradle任务执行；业务测试0，应用JAR未生成；失败制品上传成功 | 第二次连续云端失败，STOP；只做归因/只读来源调查，不启动Run3 |

## Run2 认证与完整性

- Run2状态FAIL；started执行11:00:06Z、finished11:02:22Z（19:00:06—19:02:22 +08）；native/bridge rc均1。
- 认证GetPipelineRun返回job511938036、engineTaskSign `cloud_ci-api_ci`、BUILD_NUMBER2。receipt的`cloud_ci.api_ci`是逻辑key，不是数字job ID。
- job params.sources准确记录develop tip `1911a370fbaf8cf705eb1fe85e8d2e9a294ace6d`；receipt实际构建6267f3b16fe7b672a3c8479f058a662d9c75216c/tree936d6e4bcf3d7a4cc23cde62fa0e697be93d659b，前后clean。
- 认证job.params.steps中的两个命令与已审本地build-step-r2和final-gate-r2逐字节匹配（仅终止换行归一）；配置、ticket及四项工具摘要绑定无偏差。
- 运行中的log API返回more=true，不能当完整日志；诊断改从同Run认证GetPipelineArtifactUrl action取得上传包，下载4798字节，SHA256 `a8f0c6373092588c8f31de7327d7da7012e2fa94d2e065a8a47ebf998331ba6f`。
- `/tmp/cyf-flow-ci-download-run2/download-receipt.json`记录认证来源、命令摘要和下载摘要。签名URL未落盘。
- `/tmp/cyf-flow-ci-download-run2/export/receipt.json`；ticket与签发文件逐字节相同，inspect完整性校验通过，正确classified failed / automatically_accepted=false。其rc1是预期结果，不另计新运行失败。

## 有界整改计划（未获新运行放行）

1. 只读确认固定API中OpenCV坐标声明、实际使用路径及既有制品的可信来源。不得把本机Gradle/Maven缓存打包搬到云端冒充可复现依赖。
2. 冻结一种可验证供应方式：官方可获取且兼容的坐标/版本，或有来源、许可证和SHA256证据的固定依赖发布到受控制品仓。不得静默换包、删除功能、跳过测试或注入生产凭证。
3. 若修改API依赖契约，由独立源码Owner在新隔离worktree实现，固定新的API commit/tree，独立复核；不改变当前6267或移动主工作区。
4. 新依赖/工具/fixture均重新固定；提交bounded remediation approval后才可签发新ticket、审查新无部署配置并运行。历史两次失败保留，不能清空账本后盲目循环。

只读复核命令：

```bash
python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py status
```

本阶段证明“真实Gradle工作已转移到云效云端”，**不证明后端CI通过、全量测试通过或构建部署迁移完成**。

## 固定源码只读定位补充

- `api/common/jia-common-core/build.gradle`（固定6267）：第24行compileOnly libs.opencv，第66行testImplementation libs.opencv。
- `api/plugin/jia-gradle-plugin/src/main/java/cn/jia/plugin/gradle/SharedDependencyManagementPlugin.java`（固定6267）：第82行版本4.5.5，第226行坐标org.opencv:opencv。
- 固定tree中可见OpenCvUtil/OpenCvUtilTest及测试图片，未发现随源提交的OpenCV JAR；本次未读取/搬运Gradle缓存、未下载替代依赖或修改API。
