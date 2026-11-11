# 公共公测发布与安全整合 — 设计

Hosted 使用精确身份 scope 隔离且 fail closed；任务搜索/计数 scope 下推 DAO/SQL，拒绝 legacy tenant=0 自动归属；preflight 无默认凭证、非 loopback 要 SHA-bound 批准、TLS fail closed、统一 deadline/清理。具体 API 路由/错误合同引用原任务与 handoff，不放宽凭证或访问边界。

## 契约来源及兼容

以下原始合同为细节权威，本入口为全量盘点时补录，不替代已冻结请求/响应、ACL、事件、错误及版本合同。

- `docs/implementation/handoffs/PWA-PREFLIGHT-SAFETY-P1.md`
- `specs/account-security-foundation/design.md`
- `specs/oauth-public-client-hardening/design.md`

无本次代码/Schema/迁移改动；后续实现必须沿现有任务 Owner 与 scoped worktree。
