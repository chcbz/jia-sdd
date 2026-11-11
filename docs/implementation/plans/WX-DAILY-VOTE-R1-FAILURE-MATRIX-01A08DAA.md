# R1 两项失败归因与有界整改

2026-09-11；保留两个独立失败，不将新树或空测试冒充通过。

| 门禁 | 证据 | 根因 | 有界整改 |
|---|---|---|---|
| 独立SOURCE REVIEW | WX-DAILY-VOTE-REVIEW-R1-01A08DAA.md | 同消息重放用当前Redis题号而非持久receipt题号校验；service修复后controller还须按结果题号清缓存 | 原Writer在隔离R2仅修wx实现及回归测试；原Reviewer差额复审 |
| R1 targeted Gradle/native1 | /var/tmp/cyf-wx-verify-01a08daa-20260911-evening/targeted-gradle.log | root build.gradle:65 在发布配置阶段读取未提供的repoUsername；0测试/0XML | 完整核对必需属性，提供无秘密的发布占位配置，仅运行测试、禁止publish；所有Gradle经orchestrator |

- 两项门禁失败后不盲重跑R1；没有可复用的通过模块证据。最终R2必须执行全部10个定向测试类及新增用例、独占MySQL。
- 本次主控批准的整改范围是上述源码和测试环境配置；不放宽业务断言、不扩展生产操作、不重复失效provider。
- R2源码在原基线验证结束前已被独立授权并隔离；完成后须clean SHA/tree、源码复审、完整命令审查后再给最终一次验证准入。新的第二次连续验证失败同样必须停止归因。
- Verifier自述preflight曾直接gradle --version（无任务）违反every-Gradle规则，记为流程偏差；已明确纠正，后续包括version也必须经根入口。
