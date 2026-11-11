# 每日答题发布准备结论（只读）

Release guard Locke 独立结论：当前仅允许源码/验证准备，生产操作 NO-GO；此文不代替执行台账。

- 已知生产JAR ff801061d43f5f972b30d61312ab5d352d0d7ea66997b2547a451729b591d5d0，对应源码f1426d9ba6a6ba973ceee641b0e5a4a0d645029c/tree e02f39cebaee84574323b8fada1310766e8b497c。
- 可信生命周期入口/usr/local/sbin/cyf-api-kit不是制品安装器；不可执行无参数默认restart。
- 根ops/release/build-api.sh仍直接Gradle，deploy-api.sh仍旧路径/kill/nohup；禁止用于本次execute，不能绕过orchestrator、canonical降权、runtime身份和monitor handback。
- docs/DEPLOYMENT.md的c024为历史M1约束，不能当成新树发布许可，也不能回退当前生产到旧源码。
- 本次需要最终candidate commit/tree、不可变JAR/metadata、additive迁移及备份/审批、独立Source/Test/isolated-MySQL证据、新task专属SHA-pinned root-owned发布控制包和exact runtime Owner。
- 新DDL只能在隔离fixture证明二次执行幂等/旧数据保留/并发约束后，按独立生产迁移计划执行。禁止回放真实历史答题做smoke。
- 未来运行窗口必须fresh绑定当前JAR/PID/start-ticks、canonical/carrier/monitor完整SHA及锁，不读取/复用其他任务私有receipt作为授权。
- Locke检查时尚无最终candidate；源码Owner随后已登记。发布仍没有独占运行Owner，未做生产操作。
