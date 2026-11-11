# 验证准备：provider 路由归因

- Agent 01a08ddd-3b9b-77e2-9bcf-604efdb24fee，profile gpt_test_runner，在首个模型请求返回 HTTP 502 / unknown provider for model gpt-5.4-mini。
- 未读取测试、未运行 Gradle/DB、无源码或测试失败；这是模型路由故障。
- 不对同一路由盲重试，不改 DeepSeek disabled 状态。
- 有界整改：使用已可用 Sol critical_worker profile 作为 verification-only fallback，写权限关闭；仍由主控指派同一证据门禁、独立源码Owner保持不变。
- 只读准备阶段保持无 Gradle/DB；精确候选存在后才转 verifier。

## 第二次准备失败与整改矩阵

- 新Sol fallback首次spawn被agent thread limit拒绝，未创建Agent、未执行测试。
- 两次准备失败分别是provider路由缺失、已完成/失败Agent未关闭占用槽位；均非源码失败。
- 主控已关闭本任务所属的失败Ampere及已完成Raman/Locke，未关闭其他任务Agent。
- 主控授权一次有界整改：现有可用Sol路由 + 已释放本任务槽位；仍仅只读准备，不运行Gradle/DB。若再次失败立即停止，不循环spawn。
