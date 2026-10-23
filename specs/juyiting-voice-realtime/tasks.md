# 实施任务

- API Owner：`VOICE-REALTIME-API-20260930`，独立 API worktree，owned paths chat voice main/test sources plus narrowly necessary starter voice config. Existing chat/Agent routing is out of scope.
- Web Owner：`VOICE-REALTIME-WEB-20260930`，独立 Web worktree，owned paths voice composable/controls, new PCM recorder/worklet, targeted voice tests. Existing shared main checkout stays untouched.
- Integration Owner：本聊天，合同、台账、相关验证、精确 SHA 合入、版本发布证据。无独立 Reviewer；Gradle 串行走 orchestrator。

运行进度仅以 docs/implementation/TASKS.yaml#runtime_ledger_json 为准。
