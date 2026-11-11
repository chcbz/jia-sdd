# 2026-10-20 上线与真实流程验证

**结论：已部署，统一验收未通过；不能标记需求完成。**

## 已核验发布

|组件|当前版本/源码|正式Flow|核验|
|---|---|---|---|
|API|1.16.12 / `a7b7270b5e6bbce80acfb1f037f75977af96d9aa`|5260799/189 SUCCESS|2584通过、122跳过；MySQL28项、真实bean图2项通过；安装JAR与同Run摘要一致，健康UP|
|Web|1.16.13 / `27b0f06631736babd7db36c91a6c57f69f7c044d`|4403172/246 SUCCESS|3095通过、2pending；366安装文件与同Run清单一致，公网入口和实际加载聚义厅JS/CSS摘要一致|
|Runtime|`8a9742a7a3339d1c36b64bede61880b085be35d3`|既有Runtime安装路径|unified服务active，吴用真实澄清及文字交付已完成|

原API/Web流水线配置均恢复APPLIED。API/Web版本号不同是本轮Web定向补丁，不将API189冒充1.16.13。前端246前，245已部署1.16.12；246新增导航及内部actor清空的回执保护修复。新增3项定向挂载测试通过，但自动点将完整入口仍受下述空白页阻塞，不能宣称实机闭环已过。静态lint与原基线同为135 errors/92 warnings，本轮未扩范围清理；正式Flow结果单独列出。

## 真实业务覆盖

- PC事项468：真实UI创建 → 指定吴用 → 后端ADMITTED → 手动从首页重新进入原议事 → 吴用提问 → 用户补充时间地点 → 吴用输出通知 → 系统提交正式批次。刷新后待验收、固定文本成果及验收页面可查看。初次自动跳转和自动验收入口更新未过。
- 待验收普通询问：上下文GET409，未发送讨论POST；因此自然修改、新批次及最终确认验收**未通过/未执行**，不因前端按钮存在算通过。未擅自修改数据库或补造验收回执。
- 移动390×844：真实UI创建事项469，推荐接口200，但事项页空白，未点将，后续未执行。320/完整文件预览/软键盘/真机流程本轮未完成。
- 测试工具最初拦截PC推荐POST是验证工具限制，不计作产品后端故障；移动端已按只读推荐语义放行，推荐200仍空白。测试过程错误定位到消息文本textarea的两次填写没有发送接口；最终澄清使用`.composer-textarea`且真实受理。

## 未通过项及下一步

### LIVE-01 交付提交完成后议事页验收入口不自动出现

事项468初次deliverable final读取到submissionProgress=PENDING；outbox稍后SENT，当前议事停止读取，没有自动出现验收入口。刷新后首页待验收且正式成果页可读。

下一步：核对交付/修改outbox结算与已有会话事件日志通知，提交后发只读刷新提示；前端监听真实提交进度版本刷新review context，不复用模型回话终态推断交付、不新增全局轮询。

### LIVE-02 待验收继续议事上下文GET409阻断普通询问及自然修改

GET /chat/conversations/1760458006509/interactions/context返回BOUNTY_FOLLOWUP_V3_CONFLICT，普通询问仍在草稿，未发送新讨论POST。

源码定位：`api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskExecutionGrantServiceImpl.java:431 currentFollowupContext仅允许assigned/running；ChatBountyInteractionV3PreviewService.context调用此入口。`。

下一步：区分待验收下只读议事上下文与执行授权，依既有review basis约束自然修改；不得直接扩宽付费/技能执行的共用grant资格。

### LIVE-03 移动端创建后事项容器空白

390×844浏览器，事项469创建201、推荐200、review context200；floating-panel panel-tasks存在但内容为空。通过首页/事项导航重进仍复现，无全页横向溢出不代表通过。

下一步：定位实际生产构建的事项导航/渲染生命周期；用真实编译组件及PC/移动浏览器补回归，不能以mock挂载通过替代。

### LIVE-04 恢复议事后重复只读重同步

PC页01:32分钟内会话events100次、content91次、requests91次、首轮typed-outcome91次；尚未证明根因，不能归咎模型或宣称是SSE正常单连接。

下一步：核对bootstrap恢复、scope/context generation与resync反馈环；保留版本单调与身份fence，停止重复挂接首轮，不靠新增超时或关闭保护止漏。

## 证据与运行边界

- 完整摘要：同目录 `production-release-20261020.json`。
- 原始发布/浏览器证据：`/var/tmp/cyf-ui-workflow-release-20261020/`。
- PC正式成果页：`browser/pc-formal-acceptance-page.png`；移动空白页：`browser-mobile/mobile-pending-assignment.png`。
- 已停止本任务拥有的两页浏览器的持续请求；未停止或重启生产API/Runtime。没有删除测试事项468/469，便于修复后沿原请求验证。
- 上线失败历史184–188保留原证据，不能将历史构建成功或自动回滚算成正式上线成功。最终线上是API189、Web246。
