# 分工与依赖
- API Owner Turing / critical_worker：独立 worktree `/var/tmp/cyf-api-execution-history-20260921`，执行历史/请求核对与runtime failure路径及作用域测试。
- Web Owner Curie / balanced_worker：独立 worktree `/var/tmp/cyf-web-execution-recovery-20260921`，交付同窗回执/恢复/幂等保护/相关文件入口与回归。
- 主 Owner：本条执行精确只读诊断、契约、集成、orchestrator串行验证、授权范围内发布核验。无独立Reviewer。

API/Web可按冻结合同并行；正式集成依赖各自自检。现有脏主工作区不动。不创建额外生成进行验证；组件测试使用隔离fixture，线上仅查询既有运行和文件。

运行状态唯一登记于 `docs/implementation/TASKS.yaml#runtime_ledger_json` 的 JYT-EXEC-RECOVERY-API-20260921 / JYT-EXEC-RECOVERY-WEB-20260921，不在此复制动态队列。
