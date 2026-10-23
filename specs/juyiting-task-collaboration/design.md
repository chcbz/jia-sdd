# 聚义厅悬赏榜与可靠多 Agent 协作 — 设计

已有详细架构合同继续有效：canonical scope/Agent、状态机/CAS/lease、decimal-string 版本、live/replay/resync、DB outbox/inbox、Rabbit confirm/manual ACK 与幂等。地图 /agent/map、名册 /agent/roster 分流，派单必须显式 Agent，禁止 /agent/active 回流。生产 Rabbit 激活不从 API 健康推断。

## 契约来源及兼容

以下原始合同为细节权威，本入口为全量盘点时补录，不替代已冻结请求/响应、ACL、事件、错误及版本合同。

- `docs/juyiting-multi-agent-collaboration-design.md`
- `docs/implementation/M2_EXECUTION_PLAN.md`
- `docs/implementation/M3_EXECUTION_PLAN.md`

无本次代码/Schema/迁移改动；后续实现必须沿现有任务 Owner 与 scoped worktree。
