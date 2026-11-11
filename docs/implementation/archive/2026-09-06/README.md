# 2026-09-06 交付归档

归档动作已记录；不移除源码、分支、worktree、原始 handoff/验证材料，不更改运行任务 owner/gate。

截止 2026-09-06T09:21:00.295553+08:00；源 TASKS.yaml SHA-256 `e90988c19a0b2ec0aa24834d9e143fa3e17ac63b89648fbe8f7aba160db66705`。

## 归档范围

| 归档 ID | 交付包 | 证据边界 | 保留事项 |
| --- | --- | --- | --- |
| AR-20260906-01 | 消息可靠传输历史发布记录 | 只归档 accepted 源码及 M3-RG API 上线记录；API health 不证明 Rabbit 已激活、生产端到端或全部 DLQ/redrive 场景通过。D09 仅 R8-2，R8-3/4 不得据此开放。 | 保留生产 Rabbit 激活/端到端验证缺口；不关闭 M4/M5。 |
| AR-20260906-02 | API/Web 发布与历史 502 恢复 | 实际发布记录已 done；旧离线 fault-injection/R39 因用户发布优先决策被替代，不标记为测试通过。 | OPS-API-RECOVERY-20260905-1932 为后续独立恢复任务，不能跟随旧事故关闭。 |
| AR-20260906-03 | API 恢复与监控激活 | 原恢复自然结束、监控源码 accepted、安装/cron tick 激活 done。 | 监控继续运行；真实收件箱投递未确认，归档不代表邮件已送达。 |
| AR-20260906-04 | 聚义厅屏幕与阅读旧修复发布 | Web 101ac4c6a2b49d04771dedef52af893c72f98c09 已推送/发布，57 screen +55 reader、build、独立源码审查有记录；没有真实设备循环 PASS。 | JY-FOLLOWUP-SCREEN-20260906、JY-FOLLOWUP-READER-20260906、JY-FOLLOWUP-VERIFY-20260906 保持活动。 |
| AR-20260906-05 | 案卷阁 H06 原始发布里程碑 | 只归档 H06 实际 API 发布记录，原重型离线 importer 门禁未完成，由用户风险接受替代。 | CORS 补丁已上线且预检通过；authenticated adapter、进度/书签/手札实际闭环、设备交互未全部验收，整个案卷阁不归档。 |
| AR-20260906-06 | Agent 客户端技能自动刷新 | specs/agent-client-skill-refresh/spec.md 保留最终契约；API108、Client97、独立 Review 与 2026-08-23 部署证据见该专题 integration.yaml/evidence。 | 不包括技能市场购买/安装/资金结算；旧交付不是本次实时重验。 |
| AR-20260906-07 | Agent 工作目录能力自动刷新 | specs/agent-workspace-capability-refresh/spec.md 保留最终契约；Client119、独立 Review 与 2026-08-23 三 Profile 发布 smoke 证据见该专题 integration.yaml/evidence。 | 能力标签不是 ACL 或已购买/已安装技能证明；无新增运行操作。 |
| AR-20260906-08 | OAuth 公共客户端加固 | specs/oauth-public-client-hardening/spec.md 保留最终契约；独立 ACCEPT、2026-08-24 部署与 artifact/revision 证据见该专题 integration.yaml。 | 只关闭该 OAuth 契约；账号生命周期、全局撤销、托管密钥与整体验证不随之关闭。 |

## 尚不归档

- ASF-COOKIE-P1：done 只证明候选清单校验；credentialed smoke 未执行、commit/tree 未绑定。不把它标成安全功能已验证发布。
- O01-LANDSCAPE-HEIGHT-RELEASE：仍有代码合入记录缺口；后续 Web 发布存在不能自动替代 ancestry 验证。
- PWA 全量公开发布、语音实际启用、SILVER/技能市场/托管租金，以及 M4/M5 规划范围未完成。
- 当前恢复与 JY follow-up 继续由各自 Owner 执行；归档不解除资源约束、不终止服务或监控。

## 证据与规则

- `release-records.json`：本次实际归档登记，区分功能归档和仅历史发布记录归档。
- `execution-snapshot.json`：只读审计快照，不是第二运行台账；更新执行必须使用 orchestrator 和原唯一台账。
- `manifest.sha256`：归档文件与本次 SDD 文档摘要；后续状态变化需新批次，不能回写该快照。
- 当前源码 checkout、remote candidate、已发布 artifact 和根 gitlink 不是同一概念；未将健康检查提升成业务验收。
