# 微信答题优化：续接核验记录（2026-09-11 晚间）

此文仅记录证据，不替代 `TASKS.yaml#runtime_ledger_json`。

- Writer 已提交候选 `7a846a3e4feeff895075c2d3456e87295c6b83cb` / tree `65e8cdd24fd19029e52864dd7a35224775a4b5f1`。独立 worktree `/home/isp/wsps/cyf/.worktrees/wx-daily-vote-opt-01a08daa` clean，51 个改动路径全部在冻结的 common/material/point/user/wx 范围内，`git diff --check` 通过；不代表测试或评审已通过。
- 20:08 fetch 后 origin/develop=`4b94cc252cfaac239c734d96ddcb1370290588e4`，相对实施基线仅 `ops/orchestration/flow_remote.py` 增加5行。候选验证期间不改树；合并时需再次核对远端与字节一致性。
- 原验证准备 Agent 在续接后返回 not_found；复用已批准的 Sol verification-only fallback，未重试失效的 Mini provider。定向 Java 测试与独占隔离 MySQL 由 Knuth 执行，独立只读评审由 Godel 执行；源码整改仍属 Shannon。
- 20:01 live runtime record PID=`1569373`，JAR SHA=`ff801061d43f5f972b30d61312ab5d352d0d7ea66997b2547a451729b591d5d0`；优化候选没有部署证据，未执行生产 DDL/生命周期操作。
- 旧 CPU 进程 `4109240` 已不存在，所属任务 `OPS-LEDGER-CPU-4109240` 的共享台账为 done，记载精确 Owner 已完成清理。本任务没有操作该进程或读取其私有清理证据。
- 20:10 资源观察：负载9.55/9.29/10.55，MemAvailable1286MiB，swap使用932MiB，磁盘可用6.3GiB。非性能基准；不能据此声称答题已达到时限。
- 生产 access log 使用 `api_safe` 格式（`$request_method $uri $server_protocol`），主动隐藏 query。三次旧回调 URL 不带 query 的日志表现，不能用来判断真实请求是否含 appid/signature/timestamp/nonce。

## 发布前仍须核对

- 候选定向测试、实际隔离 MySQL、独立源码评审及最终合并差额。
- 严格 POST 验签及 ToUser 与账户 original 的兼容性；不输出秘密、签名、原始正文或 openid。
- 新增 receipt/message-alias 表及两条索引的迁移、备份和生产准入；只读审计历史重复，不自动冲正。
- 本任务专属不可变制品、SHA-pinned安全发布控制包、精确 runtime Owner、维护锁与监控交回。旧部署脚本仍不可 execute。
- 红包仅对新成功答题提交后 best-effort 异步发送，提交后调度前崩溃的漏发窗口及 receipt 无清理周期是显式剩余事项，不虚称 exactly-once delivery。
