# 2026-10-24 职位技能候选证据

结论：候选源码交付、定向诊断通过；**四小时计划整体验收未完成，未部署**。当前候选由 source-inputs.json、component-remotes.json、Root gitlinks 和 integration.yaml 共同固定。

| 文件 | 覆盖 / 边界 |
|---|---|
| api-final-tests.json | 固定API4520d819，113项零失败/错误/跳过；XML时间/用例名/摘要、日志SHA、Client摘要、工作区干净证据 |
| web-final-tests.json | 固定Web45a217ba，100项；8文件与冻结develop对照无新增lint，保留基线142errors/108warnings |
| client-final-tests.json | 固定Clientbade440c，155+6项；源码测试前后摘要、命令、日志SHA |
| client-archive-source-proof.json | 340个conf/systemd输入文件与精确git提交逐字节相同，测试目录摘要一致；不是全仓归档摘要相等 |
| flow-*-safety.json | 00:59+08官方只读查询的分支guard；无本候选Run，不是失败Run或构建结果 |
| component-visual.json / component-*.png | 真Vue组件+明确只读模拟API；桌面/390px窄屏，不是后端或浏览器登录E2E |
| root-structural-checks.json | sddw候选pins、文档导航和空白检查；不是功能验收 |
| *-cleanup.json | 精确任务归属下停止两个临时MySQL和两个预览进程；保留数据/日志，未动生产 |

## API最终执行

入口：测试机 `/mnt/Workspace/aps-20261023/run-regression-eva.py`；脚本精确SHA见api-final-tests.json。通过已存在的 `ops/orchestration/cyf_orchestrator.py gradle` 与 `/tmp/cyf-gradle.lock`，单worker、无daemon、Java21，所有Test强制fresh，允许compile-only复用。selector：

```text
:agent:jia-agent-core:test
:agent:jia-agent-service:positionSkillsTest
:agent:jia-agent-service:positionSecurityTest
:chat:jia-chat-service:archiveMaintenanceTest
:chat:jia-chat-service:archiveReaderRegression
validateLayering
```

最终日志：`/mnt/Workspace/aps-20261023/p4complete/gradle.log`。无失败/错误/跳过，Gradle BUILD SUCCESSFUL；113项构成15+4+41+13+40。native综合测试1项包含多步真实HTTP/安装/发布/撤任断言，不把每个断言虚增为独立用例。数据库测试连接完全隔离，所需credential文件不提交。

Web和Client具体命令在各自JSON。Client日志在 `/mnt/Workspace/aps-20261023/client-final-pinned/`；Web日志在本任务隔离 diagnostics/web-final-pinned.log。原始日志本身不随Root提交，只保留摘要和位置；源代码和最终日志SHA可复查。

## 失败归因与证据注意

首台机器Gradle曾OOM终止；1.1.0包因元数据安装失败、旧轮询撤权事务污染、AUTO发布CAS反复WAITING、reader测试sourceSet缺两个类型、新增3个Web lint问题均已归因修复并复测。此前结果不是当前候选的替代物。

额外证据自检发现：Client测试tar仅含conf/systemd，与全仓git archive的SHA不同属预期范围差异；按文件逐字节核验后全340项一致。聚合hash需使用同一pathlib组件排序，不能把字符串排序输出当成源码变化。历史integration备份保留原工作文件CRLF字节，与Git LF blob仅换行形式不同。14个既有Linux绝对路径Markdown链接改为相对导航后结构检查通过，不改历史验收状态。

## 尚未完成

- API/Web正式Flow与production build：现行guard不接受本候选分支；未修改云配置、未通过合develop绕过。
- 完整已安装Runtime实际WebSocket注册、产品浏览器OAuth/操作/恢复；native fixture使用显式auth.bind，不冒称全流程。
- 计划要求的独立只读复核；Owner自查不等于独立复核。
- 完整《三国演义》底本/整书验收、生产迁移/批准/任命/上架/部署均未执行。

旧D2 84项矩阵不重新分类。本目录是可审查候选证据，不是发布凭证。
