# 主流程修复与生产复验（2026-10-20）

## 结论与范围

**文字主流程已打通并上线；不等于全量优化方案验收完成。** 单Agent执行，没有新增页面、状态、全局轮询、数据库迁移、付费权限或无关优化。

原约定07:04—08:04的一小时目标**未达成**；08:07已主动说明逾期。08:22完成三项真实事项的验收回执及刷新核对，后续仅整理证据。不能将本报告改写成按时交付。

## 固定版本和正式证据

| 组件 | 精确源码 | 发布与验证 |
|---|---|---|
| API1.16.15 | `0afd50f70ebd839dc1ac9be1ee71d50e525baf8f` | Flow5260799/191 SUCCESS；2588通过、122跳过；28项真实MySQL、双序bean图等保留；同Run制品与安装JAR摘要匹配，健康UP |
| Web1.16.14 | `38667d01a6beae07cc94b30f7bacc773bcfb3f58` | Flow4403172/247 SUCCESS；3097通过、2pending；366安装文件一致；公网入口和议事JS/CSS一致 |
| Runtime | `f30cb5a18219308393bd175939bc5f56cc89db9d` | 38项定向回归；既有独立制品安装器和配置闭包验证；66个payload与固定源码一致，08:09切换成功。不是前后端Flow证据 |

前后端Flow临时配置均已恢复原值并readback APPLIED。源码已推送对应develop；根工作区其他任务修改未覆盖或批量提交。原失败发布报告保留，未回写为成功。

## 生产真实路径

- **移动471**：真实创建保存为待点将→吴用点将→自动进入议事→文本成果正式提交→验收图标无需刷新出现→普通问答保留原SUBMITTED批次→自然修改15时为16时→原批次变更、独立子请求生成新成果→确认验收COMMITTED/ACCEPTED，事项COMPLETED→刷新仍已完成。
- **PC472**：原澄清回报暴露Runtime模型schema缺口，修复后重发并正式提交、验收完成。中途诊断恢复不能冒充无干预全链路。
- **全新PC473**：在最终Runtime版本上，从创建→吴用点将→CLARIFY→实际CLARIFICATION_REPLY→提交→自然修改15时为16时→修改决定COMMITTED及child提交→界面确认验收→COMPLETED/ACCEPTED→刷新仍已完成。此事项没有人工API恢复或DB修改。
- 两端静置30秒各0个额外请求；本观察窗口未复现原无限SSE重同步，不据此承诺任意长时网络环境。

所有生成、修改、提交均为真实吴用回报，不写假final、不直接改DB、不用模拟结果通过验收。验收由真实页面按钮发起。

## 根因与修复

1. 事项父组件还把task对象当status字符串处理；改用既有统一projectHallTask投影，测试使用真实非空筛选项。
2. 非当前request的合法typed_question_answered事件被拒绝，游标无法推进造成重连循环；同会话合法提示确认消费，保持作用域校验，不放行未知事件。
3. 待验收只读议事上下文错误排除reviewing；仅放开元数据读取，保留执行/付费/图片权限限制。
4. 成果完成未实时通知：提交事务内持久化delivery_submission_completed及settle；事务返回后由既有relay推送，前端按嵌套submission/review版本重取权威状态。
5. 模型schema与语义校验不一致：空text和无合法deliveryParent却生成关联在模型输出层未限制；约束text非空、无父节点时deliveryRelation只能null，不放宽服务端语义/ACL。

## 限制与未收口项

- **模型文案质量仍有一项已知问题**：PC473修改后的文本附带“无法重新提交正式验收”，但其deliverable、同Run提交事件和领域回执证明已实际提交并验收；这句模型自述错误。本次只保证流程链路，未宣称文案质量通过，不因该问题新增流程分支。
- 471/472的首次停止操作被验证浏览器write guard误拦（预授权request取消路径，真实UI使用turn路径）。后以当前登录身份和权威版本调用现有取消API，两个turn均CANCELLED。此为诊断恢复，**不记为这次UI停止完整验收**。473无此恢复。
- 不包含全量页面/图片附件/付费技能/多Agent/异常恢复的整体方案验收；不处理既有workspace命令或Audit遥测错误。
- 制品/状态详情见`verification.json`、`api-flow191.json`、`api-installed.json`、`web-public-assets.json`、`runtime-installed.json`，截图保留本目录。私有原始请求日志在`/var/tmp/cyf-mainflow-20261020/`，未将凭证写入仓库。
