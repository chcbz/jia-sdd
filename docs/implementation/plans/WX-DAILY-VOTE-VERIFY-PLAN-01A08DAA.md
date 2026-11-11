# 每日答题定向验证计划（准备完成，尚未执行）

- Verifier：Sol verification-only fallback 01a08de3-23c9-7223-a49d-1eee62c9659a；原Mini路由和槽位故障已有归因矩阵，不是代码失败。
- JAVA_HOME=/home/isp/apps/jdk21（21.0.8）；Gradle9.3.1，root project jia；主要目标 :wx:jia-wx-service，必要的material/point/user窄回归按最终候选选择。
- --no-daemon --max-workers=1，Gradle堆384MiB、单测试fork；不运行starter或全仓构建。可对本任务新建验证进程设置低优先级，不改变任何既有进程。
- 先最终candidate的定向单测，再一个有界隔离MySQL selector；所有Gradle必须经根orchestrator，证据键=最终tree+selector+fixture digest。
- MySQL8.0.21使用自己新建的临时datadir/随机非3306端口，禁止生产schema/凭据及其他任务实例。初始化/测试/停止均应在获准串行资源窗口内；仅允许清理自己的精确PID/start identity。
- 覆盖迁移fresh/upgrade/repeat、历史数据保留、索引作用域、事务回滚、同消息/同题并发幂等、原子增量、缓存失败/新题保护、日志脱敏。
- 候选尚未提交；只有最终clean SHA/tree + 精确selector + fixture环境契约 + verifier gate后才可执行。
