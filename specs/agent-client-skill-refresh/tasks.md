# Tasks

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

已交付并归档原 2026-08-23 功能；原验收记录 API108、Client97 与运行 smoke，未在本次重复执行。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：AR-20260906-06。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 当前执行动作

仅对新增回归另立缺陷单，技能市场交付继续独立实施。

以下原始清单为合同/历史记录；当前完成状态采用 delivery-status 的任务映射，不能据旧未勾选项重新派工。
<!-- END SDD delivery reconciliation -->

- [x] API：注册时客户端能力优先，缺失时兼容已有 runtime/persona。
- [x] API：presence 支持刷新 abilities，并统一规范化与大小写无关校验。
- [x] API：已绑定 persona catalog 优先展示 runtime abilities。
- [x] Client：动态发现 Codex/profile/workspace skills，注册和心跳均上报。
- [x] Tests：服务层、WebSocket 转发和客户端动态发现覆盖。
- [x] Integration：提交并固定 API、isp-install 与 root revision。
- [x] Release：部署 API 与 codex-ws-agent 后验证能力名册和推荐结果。
