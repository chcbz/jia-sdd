# 工作区提交清理 · 2026-11-12

## 范围与结论

Owner：git-cleanup-owner。用户授权检查并提交有用改动、删除无用残留，并明确包含共享 isp-install 仓库中的 new-api。仅清理当前四个主工作区和推送 develop；不部署，不处理其他 worktree/活动进程/生产数据。

| 仓库 | 审计基线/处理 | 最终候选 |
| --- | --- | --- |
| 根仓库 | 原本地积压30个提交已推送至 e06cf74a；补交真实证据缓存、任务收口和组件指针 | 本文所在提交 |
| API | 旧分支516267上的94项展开改动：33项与远端相同，49项为历史原样；其余逐项对照，保留HTTP错误语义及有效规范，删除旧技能/原生/推荐残留，不恢复已退役绑定事务与解绑测试 | e2e2cbe2305608c3bd01d27dcfc07eb40b526fe4（含46f8e47ed0） |
| Web | 旧ca22ac2候选与远端c453e08对照；生产src/tests采用远端，旧银两/直接派发等残留不恢复。离线原型保留独有模块并合并最新租约收尾、报价、原生流程 | 60ddd8a |
| isp-install | 在远端bbf8db0上集成new-api依赖安装器、Python冻结/归档修复及对应文档 | 3897676（含50e79d4、ea60fb3） |

API的业务改动只在HTTP错误响应责任层，保持现行GET/权限路径，不新增解绑兼容层。Web仅离线原型和规则/历史资料，未改生产Vue源代码。原型历史截图和摘要原样保留，README明确不代表本轮通过。

## 验证与限制

证据根：`/home/isp/state/cyf-local-build/tasks/git-cleanup-20261112/`。

- isp-install：35通过、1跳过（new-api 13、freeze 11+1跳过、archive 11），未执行实际安装。
- 根工具：备份范围22项、nginx路由5项通过。首次临时目录夹具失败保留，使用本任务普通磁盘TMPDIR重测。
- API精确e2e2候选：`api-4/test-summary.json`中HTTP错误15项、Controller 11项通过；`validateLayering`通过，72.752秒。仅定向验证，未打包/发布。
- API前次CLI/插件缓存失败原日志保留。默认test源码集因既有`PlatformKnowledgeUsageHttpMySqlTest`无法访问`EconomyMySqlTestFixture`编译失败，见`api-3/gradle.log`；没有关闭原测试，改用既有managedHostingRegression并显式纳入新HTTP测试。**不能声称全量测试通过。**
- Web：所有原型JS及根浏览器工具语法通过，index引用本地资源全部存在；`web-smoke-5/browser-checks.json`为20页×1440/390/320三视口实浏览器检查，含帮助文章返回、拥有者外单开关入口和个人中心入口，零运行异常/外部请求。报告含实际JS/CSS/HTML输入摘要；只是离线合并验证，不是线上验收。
- Web前次失败保留：合并漏入composer辅助函数已修复；帮助返回选择器应为back，外单开关必须先选拥有者Agent，测试夹具据实际交互修正。旧全页样式检查的失败未重标为成功，新增合并冒烟不替代历史视觉矩阵。
- `./sddw check-docs --all-docs`：3个既有“Removed path reappeared”错误，分别为agent-client-skill-refresh、agent-workspace-capability-refresh、oauth-public-client-hardening下delivery-status.md；不在本轮删除历史交付记录。可达性无新增缺口，整体仍FAIL，见docs-check.log。

## 清理与保留

- 修改前逐仓脏文件、patch、blob比较和三方合并审计均保存在上述证据根；删除工作区残留不丢失原内容。
- 根`.evidence/`含诊断配置，移至证据根`root-untracked-evidence`，不提交潜在私密数据。只删除已确认零字节的LIVE/ONE/SAME-OWNER。
- 只清理本轮失败构建的可重建中间目录，保留结果/日志/测试报告；没有清理共享缓存、其他工作区或生产备份。
- 原调度任务按已提交handoff/实际成功证据关闭旧阻塞；扈三娘仍按用户要求延后，task648费用核对仍PENDING_USAGE，不能据此次Git收口声称这些业务已完成。
- 本轮主工作区统一为develop。其他历史分支/worktree未删除；根及组件干净、远端同步以最终逐仓fetch/readback结果为准。
