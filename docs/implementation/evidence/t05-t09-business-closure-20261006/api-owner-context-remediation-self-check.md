# T05–T09 / 后台任务事实读取身份上下文修复自检

候选：API `4e0091ea16959885d0ba13316a094ea6cb37fae1`，tree `b23ed800895f7870938d5082c8a8ebd4f34845d6`，parent 为线上 Run112 commit。独立工作树，仅变更 ChatDeliberationService 与其测试；未改主仓脏文件。

## 根因校正

09:46 的真实错误为 typed runtime unavailable。客户端 measured readiness 重新注册修复后，09:51、09:56 以及后续实际失败已经变为 `ChatDeliberationService.taskFacts` 的 `Chat request is unavailable`；外层错误码仍是 BOUNTY_ADMISSION_UNAVAILABLE，不能据此断言同一根因。10:11:43 原生身份只读 GET 返回200，未消费或执行队列命令。

AgentService.getTask 及 toTaskDTO 内嵌的成员/资金等读取依赖 EsContextHolder；后台 bootstrap 不经过浏览器身份过滤器。修复从已校验的 ServerResolvedSender 与已加锁的精确 owner/client/tenant 会话派生独立上下文，只覆盖既有任务事实读取，并在 finally 恢复原上下文对象。不从客户端正文、资料或当前线程残留身份选择 owner。

## 安全与事务

- 先由 requireHumanSender / requireLockedConversation 校验身份、租户、Owner、Client、会话和 generation，再进入任务读取。其他 Owner 的 sender 不能获得本任务上下文。
- 调用现有 AgentService.getTask 的严格 owner 查询和投影校验；仍核对返回 taskId/tenant/client。不削弱原任务、grant、会话、typed readiness 或当前 runtime binding 校验。
- 原始 EsContext 对象不修改；成功、读取异常、投影不一致均 finally 恢复。非任务会话直接返回，不安装上下文。
- 未改事务边界、锁、幂等 key、原 intent、START、数据库数据或迁移；未改 API/Web 进程。
- 测试增加：空/错误线程上下文的后台准入；读失败、错 tenant/client/task 投影不落请求且恢复上下文；跨 Owner sender 拒绝。正式执行以 Flow113 的实际结果为准，不以本地静态检查代替。

## 正式验证与恢复

- remote develop 已精确 readback；Flow113 为单次启动。原控制工具在分页历史预检处拒绝、未执行写；经只读完整两页112条历史核对，冻结配置哈希、来源与 Run 列表后由 SDK 单次启动。没有重复 start。
- 正式测试/构建/制品通过既有5260799，不进行本地 Gradle/Vite 构建。
- 已只读确认实际安装的 deploy adapter 无 exact backend-nightly intent 时返回 DEFERRED；下一正常定时发布为2026-10-07 00:00 Asia/Shanghai。未伪造夜间 intent 或绕发布时段。
- 恢复边界：如候选有缺陷，修正源码再经正常 Flow；若已发布后须恢复，也沿正式制品/发布互斥与健康流程。此记录不自行授权即时部署、API重启或生产 DML。
- 保留原任务423，部署后继续同一原 intent；T05–T09 未完成真实验收，不记 PASS。
