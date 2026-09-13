# OD07 API repair independent read-only review

# ACCEPT

候选：`ed2ada849cd7f06eac4e217641c70dafffaca54e`

- **P0：无**
- **P1：无**
- **P2：无**

旧候选的三个拒绝项均已关闭：

1. policy1 分配在写入前检查 exact-scope Rabbit dispatch、outbox、writer、run service 和 work-item DAO；不可用即失败，且禁止 legacy fallback。见 `AgentCommandTransportCapture.java:117-192`、`AgentServiceImpl.java:1014-1060`、`:2280-2293`。
2. release/expiry 未耗尽 attempts 时，在同一根事务保留 assignee、增加 attempt、写事件、创建 fresh run、CAS 绑定并写 fresh command/outbox。旧 run 因 `dispatched_run_id` 已切换而无法 claim。见 `AgentWorkItemLeaseServiceImpl.java:242-307`、`:395-445`，`AgentCommandTransportCapture.java:194-222`。
3. claim/heartbeat/start/recover 均使用服务端可信 `recoveryUntil`；越界在 CAS 前拒绝，已持久化越界租约也 fail closed。见 `OutputLeaseServiceImpl.java:84-155`、`AgentWorkItemLeaseServiceImpl.java:198-239`、`:271-290`、`:325-367`、`:489-535`。
4. attempt 达 `maxAttempts` 后进入 `FAILED`，清理 assignee/run 且不创建第四个 run。实际 MySQL 覆盖见 `OutputDeliveryPolicy1MySqlIntegrationTest.java:339-356`。
5. 旧 ticket 的原 key/body 可重放原 receipt；改变 body 冲突，新 key 的旧 run claim 返回 409，新 run 可正常 claim。见该测试 `:242-310`、`:293-337`。
6. run `origin_id`、commandId、causation event 和 workItem 使用同一确定性身份。见 `AgentCommandTransportCapture.java:157-179`、`:299-329`，`AgentTaskMutationEventSupport.java:13-40`。
7. work item、event、run、command delivery、outbox、receipt 都加入同一个 `PROPAGATION_REQUIRED` 事务。实际 MySQL 的 release 重派后 receipt 注入失败验证全部回滚，见测试 `:548-584`。
8. 自动重派仅由 lease release/expiry 触发；未接入 `CHANGES_REQUESTED` 路径，OD09 的显式返工边界保持不变。

证据核验：

- 实际 MySQL 8：4/4，0 failures/errors/skips。
- MySQL 日志 SHA-256：`9356b10794604d208c8227e35c265b25da4d71da7f593389e140ac6a3162f343`
- MySQL XML SHA-256：`2cbb3303efc8776e30678dd8cbccfad34635058c7f4a13cd89bb78e9a5381069`
- 受影响套件：29 suites，442/442，0 failures/errors/skips。
- 套件日志 SHA-256：`859480e1c6fde59473ebf2d3372961470a2c6e5ade21150df93d2e7148c6fa3e`
- 候选关联文件 SHA-256：`d2b79bdc1d5b6ce5264ed118c45a9449137b51f5321311e2a373a99ba071452e`
- 独立复算候选 repair patch SHA-256：`37ef8b6985e5f64636e46dc9a41cd16d8398735a83392cc89d96aff83602e54c`，与关联文件一致。
- `git diff --check` 通过。
- 工作树干净，HEAD 精确为候选 SHA。

证据限制：442 套件完成后仅强化了实际 MySQL 测试代码，生产源码未再变化；更新后的 MySQL 测试随后实际执行并通过 4/4。当前 starter 配置仍默认关闭 command outbox，policy1 会按设计失败关闭，后续发布配置必须显式启用 exact scope。复审过程中未重跑 Gradle、未修改文件、未执行 DML、部署或重启。
