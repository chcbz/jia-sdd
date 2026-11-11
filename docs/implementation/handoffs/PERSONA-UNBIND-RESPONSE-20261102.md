# 招贤令移除异常 — 2026-11-02

- Owner：当前修复聊天。目标：修复移除请求业务拒绝被误报为协议错误；非目标：强制解绑、清理在办任务、修改租约、生产发布、全项目错误迁移。
- 复用工作区 `/home/isp/wsps/cyf/api`，branch `codex/architecture-convergence-api`，HEAD `516267bf7b19bfc03581ae580704af9246ffb622`，tree `32d2a425652337b7bf138417b5736e185007740f`。工作区已有大量他任务改动，AgentController 已有推荐接口调整，保留原改动。
- Web只读基线 `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`，tree `962e513205e4805a601022285bdff557c71f37ac`；无UI/原型改动。
- 2026-11-02远端只读查询：API develop `ab3da7286f140e32c45e542e9638d2bb5efff2e7`，Web develop `5470363fc33d7689890763a54eb0ee23ac8d84d2`。并非当前工作区HEAD，亦非受测/线上版本证明。
- 规范：`api/docs/interface-standard.md` v1.4 §§2.2、5；RB-1接口入口负责错误HTTP状态，业务服务保留资源状态/事务；Web使用公共decodeHttpResponse，不放宽成功校验。无Runtime联动。

## 已确认

生产日志 `/home/isp/hosts/cyf/api/logs/root.log` 2026-11-02 14:48:43.572 +08:00：`/agent/personas/gongsunsheng/bind` 被拒绝，`AGENT_BUSY`，`Agent cannot be unbound while it has durable active work`。未读取用户任务正文、未改数据库/生产状态。

AgentController本地异常处理返回裸JsonResult错误信封、默认HTTP200；Web公共解析器明确拒绝2xx与非E0组合，因而真实业务拒绝被显示为PROTOCOL_INVALID_RESPONSE。页面只有DELETE成功后才刷新列表/提示成功，该流程不应放宽。

业务保护位于AgentHostedBindingTransaction.requireNoActiveTask：存在当前执行投影或持久化活动分派则拒绝，避免孤立在办工作；保留现有事务、锁及SQL。日志证明有活动分派命中，尚未检查其任务ID/状态是否应终结，不推断为脏数据。

## 验收计划

最早轻量反馈：运行现有Web信封定向测试，验证200/AGENT_BUSY拒绝、409/AGENT_BUSY正确传播。后端新增真实MVC DELETE回归：200成功空data、409忙碌、403权限、404缺失、400输入错误、500内部错误，核验信封与requestId；正式Java执行必须走Flow固定候选，不本机构建。

## 状态

定位完成；实现与验证见后续补记。尚未合入、Flow验证或部署，不把日志调查标为线上修复。定位/实现/验证/等待时长未计量。

## 实现与本机轻量验证

- 已修改AgentController既有异常边界，业务失败映射真实4xx/5xx；参数失败400，内部失败500且不暴露异常原文。保留Controller既有他任务推荐接口调整，未整文件回退。
- AgentHostedBindingTransaction只替换两处忙碌提示为中文及下一步，未改状态判断/SQL/锁/事务。当前接口目录定向补记，其他未核定内容保持。
- 新增 `api/agent/jia-agent-service/src/test/java/cn/jia/agent/api/AgentPersonaUnbindHttpTest.java`：15项MVC测试执行（包含11项参数化映射），覆盖成功空data、忙碌、状态映射、安全错误及请求关联。尚未编译/执行，不宣称通过。
- 本机 `node --test web/tests/interface-envelope.test.mjs`：23/23通过（约975ms）；额外以当前真实decodeHttpResponse和合成信封验证：HTTP200/AGENT_BUSY复现PROTOCOL_INVALID_RESPONSE，HTTP409/AGENT_BUSY正确抛出原错误码/中文消息，非线上请求证据。
- `git diff --check` 定向通过。未运行本机Gradle/生产构建，未启动Flow、未安装、未操作真实解绑/任务。
- 后续：固定不夹带其他任务修改的API候选，Flow5260799执行 `:agent:jia-agent-service:test --tests cn.jia.agent.api.AgentPersonaUnbindHttpTest --tests cn.jia.agent.api.AgentControllerTest --tests cn.jia.agent.service.AgentHostedBindingTransactionTest` 与受影响验证/validateLayering（project路径已按settings.gradle核对），600秒Run上限；发布须另有授权。工作区多人未提交修改及与远端develop分叉尚未协调，不自动整体提交/推送/部署。
- 线上API/Web安装版本尚未核验；生产日志足以证实该次业务拒绝，不等于已核对部署源码摘要。此次修改不意味着已有活动任务已结束，用户仍需先处理任务才能安全解绑。
