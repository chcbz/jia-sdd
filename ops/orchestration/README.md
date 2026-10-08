# 开工诊断（DEV-FEEDBACK-PILOT-20261008）

在现有 `cyf_orchestrator.py` 增加 `preflight`，不另建台账或准入门禁：

```bash
python3 -B ops/orchestration/cyf_orchestrator.py preflight TASK_ID \
  --cwd /absolute/path/to/task-worktree --component api \
  --baseline origin/develop --selector ':module:test --tests ExampleTest' \
  --fixture path/to/synthetic-fixture.json
```

- TASK_ID 必须存在；cwd 必须是仓库/worktree 根。baseline 显式指定，只读取本地引用，不 fetch，也不宣称远端最新。跨仓任务逐仓核对，台账 SHA 不匹配时先确认它绑定的是哪个组件，不自动改台账。
- JSON 输出 HEAD/tree、分支、是否脏、任务 SHA 是否匹配、基线双方独有提交数、工具是否在 PATH、根构建文件和指定 fixture 是否存在。
- 不执行 java/node/gradle/npm、候选 selector 或 shell；不读取 fixture/凭据内容，不下载依赖、不连接数据库、不修改任务或发通知。文件存在不等于内容/schema/依赖就绪。
- 当前 ledger 不含 owned_paths/worktree 映射，路径冲突明确 UNKNOWN；仅列其他 Writer 作为人工协调线索，不能声称无冲突。锁可用性、数据库和工具版本也未验收。
- Findings 仅建议，正常观察退出0；未知任务、非仓库或无法读取退出2。这不是测试成功、正式构建或发布批准。
- 前端正式验证仍走 Flow4403172；后端在干净精确输入上先读 build.gradle，再经原 gradle 入口串行验证，保留 validateLayering。preflight 不绕过现有锁、授权或失败处理。

隔离测试（只创建并清理自己的临时 Git 仓库）：

```bash
python3 -B -m unittest discover -s ops/orchestration/tests -p 'test_preflight.py' -v
```

共享契约试点见 `specs/juyiting-execution-recovery/contract-pilot/README.md`。它复用实际前端消费者，但完整 Java HTTP/数据库层必须单独验证，不能以替身响应 PASS 替代。
