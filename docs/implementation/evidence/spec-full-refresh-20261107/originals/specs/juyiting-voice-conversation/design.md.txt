# 聚义厅语音输入与会话 — 设计

分阶段发布：先完成 canonical host 生命周期/运行时交接与 flags-OFF API 交付，再验证认证后的真实 STT/TTS 与 scoped Nginx，最后启用 Web。不能从文本模型可用推断音频能力；不得把 source ACCEPT、build PASS 或离线组合覆盖当作激活证明。

## 契约来源及兼容

以下原始合同为细节权威，本入口为全量盘点时补录，不替代已冻结请求/响应、ACL、事件、错误及版本合同。

- `docs/implementation/handoffs/JVC-OAI-RELEASE-COMPATIBILITY-20260905.md`
- `docs/implementation/handoffs/JVC-OAI-RELEASE-CONTINUATION-R4-CLOSEOUT.md`

无本次代码/Schema/迁移改动；后续实现必须沿现有任务 Owner 与 scoped worktree。

## 音频目标合同入口

`docs/implementation/handoffs/JVC-OAI-SPRING-AI-REFACTOR.md` 冻结 Spring AI 音频架构、admission-before-spool、handle-based 音频处理、身份/缓存隔离、内容类型/大小/时间界限及配置覆盖验收要求。发布合同还受 `JVC-OAI-RELEASE-CONTINUATION-R4-CLOSEOUT.md` 的三阶段边界约束。应建/应验要求来自这些文档；accepted API/Web 源码仅证明现状。HTTP 请求/响应逐字段合同入口尚未集中整理，列为合同追踪补齐项，不能因源码 accepted 自动认定完整语音验收。

## 2026-09-17：1.6.0 开发补充（当前执行规则）

用户授权开始下一版本。现有 HTTP 字段、响应、错误、身份/幂等及生产启用边界集中见 `docs/implementation/V1_6_VOICE_BETA_EXECUTION_20260917.md` 第 3 节。新增语音等待可用性要求：慢回复不因任意总耗时结束；保留用户停止等待、身份切换隔离、实际传输错误；不扩大 Provider/付费授权。历史 release_guard/独立审查不是本版本前置；责任 Owner 自检，正式测试与同 Run 发布沿现行策略。
