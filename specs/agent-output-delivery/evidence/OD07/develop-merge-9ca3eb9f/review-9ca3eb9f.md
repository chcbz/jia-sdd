**ACCEPT**

候选提交：`9ca3eb9fd9167d9f0650bcca054645185628e7ed`

- P0：无
- P1：无
- P2：无

关键结论：

- JWT 旧制发布使用 `/artifacts`，run-ticket 发布已隔离到 `/output-publications`；FilterChain 和 Spring 映射一致且无冲突。
- Policy 1 在规划、依赖调度、团队推荐、自动分配、旧制协作和 artifact 发布中，均在子表查询、runtime 访问、CAS、事件或存储写入前失败关闭。
- OD artifact 在旧制读取路径进入 DTO 构造或存储读取前按 `runId != null` 隐藏。
- roster/candidate SQL 不返回 `token_hash`、capability runtime ID 等内部字段；公开 DTO 转换采用字段白名单。
- JWT artifact 发布响应不会泄露 `storageUri` 或私有 metadata。

证据复算结果：

- Agent service：10 suites，277 tests，全部通过。
- Agent mapper：2 suites，7 tests，全部通过。
- Base/User 合并回归：38 tests，全部通过。
- bootJar：229,672,448 bytes。
- SHA-256：`c72b0bf2bd8a2b2f71246dce250832f79e54eb21a3bcc15ecacfe940906588bb`
- Gradle 证据脚本通过 `flock /tmp/cyf-gradle.lock` 串行执行。
- HEAD 精确匹配候选；工作树干净；`git diff --check` 和冲突标记扫描通过。

残余风险：

- 后续客户端必须将 run-ticket 任务发布地址切换到 `/agent/tasks/{taskId}/output-publications`。
- 旧制列表在 DAO 限流后过滤 OD 行；只有出现不合法的 OD/legacy 混合数据时才可能少返回旧制记录，不会暴露 OD 内容。
- 本次复审检查了候选提交前生成的冻结证据，没有重新运行 Gradle。

