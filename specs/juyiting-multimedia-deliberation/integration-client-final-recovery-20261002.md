# INSPECT 结果持久化及重放：主 Owner 自检补充（2026-10-02）

本补充不改变领域协议、产品验收范围或运行台账。不宣称完整功能完成，也不据此发布。

## 已实际验证

证据见 [便携清单](integration-evidence-20260928/client-final-recovery-main-20261002/manifest.json)。

- v1 保留原始失败：发送返回 false 时误报 completed；发送抛异常时仍释放引擎恢复状态，结果无法重放。
- v2 只证明缺持久化回调时拒绝发送且保留引擎状态；不能当作恢复成功。
- v3 使用真实磁盘 PersistentChatInbox，重新创建实例加载记录，验证 false、throw、true-but-unconfirmed 三种情况。三种都重放相同正文、可信 receipt、outbound ID 和摘要，模型启动计数始终为 1；未收到服务端落库确认时仍为 unconfirmed。
- v3 的引擎和传输是替身，非真实服务端/真实模型验收；证据仅绑定文件摘要，不扩大到后续提交。

## 随后发现及修复接点

Client `3f76d29bd53f136b314f073975fc4772116ab132` 补充 processor recoveryControls 的 markFinalPrepared，并在恢复过程中落盘失败时保留引擎状态。定向测试由原实现 Owner 提供，不用之前探针替代 exact-source 测试。

## 尚未闭合的真实链路

API AgentWebSocketHandler 在 persistFinal 事务提交后发送既有 agent_message_saved；重复 final 也发送该回执。检查 Client 3f76d29 时尚未消费这个回执，成功发送也停留 recovery_required，因此必须补齐可信 socket、精确 profile/turn 绑定的持久终态与重试清理，并覆盖早到回执、丢回执后重复确认、重启及错误绑定。

不能因 WS 写入成功就标记服务端持久化成功；也不能无限重放作为最终产品方案。媒体实际理解、双接应、完整浏览器交付、版本构建发布仍未验收。
