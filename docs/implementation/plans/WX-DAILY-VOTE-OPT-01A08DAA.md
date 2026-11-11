# 微信每日答题优化：冻结实施边界

- 用户授权：落实已诊断的资源、延迟、重复处理优化。此文是契约/证据，不是第二执行台账。
- 唯一执行台账：TASKS.yaml#runtime_ledger_json；任务 WX-DAILY-VOTE-OPT-01A08DAA。
- 基线 API origin/develop=e7da0a435acdff93ae64473223631b3f7d7cbdac；独立 worktree `.worktrees/wx-daily-vote-opt-01a08daa`，branch `codex/wx-daily-vote-opt-01a08daa`。
- 主控仅控制面；critical_worker 唯一实现 Owner，gpt_test_runner 验证，sol_reviewer 独立只读评审。不得修改用户旧 api checkout。

## Owner 路径

- wx/：每日答题相关 controller/service、新的 scoped DTO/entity/DAO/mapper、对应测试及 additive migration。
- material/：MatVoteService 的题目复用/答题写入与原子统计相关接口、实现、mapper和测试。
- point/、user/：答题使用的原子积分增量、必要窄接口/mapper和对应测试；不得触及账户安全、OAuth、认证策略或其他业务重构。
- common/：仅在确有必要时增加 scoped Redis compare-and-delete/安全计时辅助及测试；不得改通用执行器/全局缓存语义。
- starter/src/main/resources/db/ 或现有实际 migration 路径：独立、可重复执行的新增表/索引迁移，不删除/重写旧业务数据。
- 禁止写 api/ops、chat/、agent/、web/、根 docs/implementation 或其他任务工作区；若需扩路径先回报主控。

## 行为与安全要求

1. 保持现有公众号回调地址、正确/错误文字结果和积分语义，不重新设计推题/消息队列/前端。
2. 同一微信消息重试不能重复生成答题、积分或红包副作用；并发相同用户/题目的重复消费需覆盖。必须考虑事务提交后、缓存写入前故障，不能把纯 SETNX 短租约当作持久幂等。
3. 失败不能先删除题目使用户永久失去重试机会；完成旧答题不能误删新题目。重复消息应能返回同一结果，而不是被错误路由到新题。
4. 判题、统计、积分、持久回复/幂等凭证应具有明确事务边界；积分使用原子增量，避免先读再写丢更新。收敛重复查题/查用户和同步数据库往返。
5. 分段耗时覆盖身份查询、Redis、题目/事务处理、回复阶段；慢请求可追踪，不记录正文、签名、凭据或明文openid。
6. 只做有证据的索引：wx_mp_user.open_id，以及未答题查询所需 mat_vote_tick.jiacn 前导索引；按实际租户/应用查询域设计。新增幂等表/约束必须保留历史重复数据，不在生产去重删除。
7. 不新增用户消息重放的线上验证；对真实积分/红包的变更只由真实用户操作触发。该次三条历史记录只审计，不自动冲正。
8. 若现有回调验签/身份边界存在重大缺口，先报告并提出最小兼容处理，不扩大为全站鉴权改造。

## 验证及发布

- 写针对性单测：正确/错误、同消息重试、并发重复、事务失败重试、缓存故障、旧题完成不能删新题、原子积分、分段日志脱敏。迁移/事务必须有有界隔离MySQL证据，不用生产数据做测试。
- 所有Gradle均通过根 ops/orchestration/cyf_orchestrator.py；只由获分配的Verifier运行，全局串行，不启动宽泛全仓测试，不读其他任务私有证据目录。
- independent source ACCEPT及验证完成后自动推进源码；生产部署与DDL另外核验当前SHA-bound发布入口、安全门禁和精确运行Owner，不执行旧unsafe source-to-prod脚本。
- CPU PID4109240 属于其他任务，只用 conflict-alert 协调，不能越权停止/renice或操作其证据。
