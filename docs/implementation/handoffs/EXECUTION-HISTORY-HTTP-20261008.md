# EXECUTION-HISTORY-HTTP-20261008

唯一 Owner：execution_history_http_owner；真实执行历史跨端链路 PASS，已合入本地 API develop；未push/部署。状态以 TASKS.yaml 内嵌台账为准。

## Scope / baseline

- API 独立 worktree `/home/isp/wsps/worktrees/cyf-execution-history-http-20261008`，base `ce047c43e0f275d1ad427c484b8919213be36fa4`。
- root 测试资产 worktree `/home/isp/wsps/worktrees/cyf-dev-feedback-pilot-20261008`，独占 `specs/juyiting-execution-recovery/contract-pilot/`。
- Web 只读固定源 `/home/isp/wsps/worktrees/cyf-contract-consumer-20261008`，`75766a3b78c2e552ef448e924a813ed2dfc7ecd4`；已有依赖仅复用，不修改产品源码/不本机生产打包。
- API allowed_paths：`agent/jia-agent-service/build.gradle`（仅追加独立测试sourceSet/task）和 `agent/jia-agent-service/src/executionHistoryHttp/`。不改生产Controller/service/DAO/mapper，不修改他人分支或服务。
- 完成目标：共享JSON → 实际JWT认证/Tomcat HTTP → 生产Controller/service/DAO/MyBatis → 本任务独占MySQL8 → 生产前端createApi/useHttp/fetch与Vue状态消费；验证分页、错误、scope隔离、无写副作用。
- 本轮只读接口验收不包括生产OAuth登录、真实浏览器渲染、发布或业务生成；前端本地为低成本诊断，不能替代Flow正式验证。

## 重要发现

原模拟样例 limit=20 但items只有1条且nextCursor非空，不能由真实limit+1分页实现生成。改为首批20条/末批1条，以同一JSON种子和期望值驱动两端；不改生产分页行为。

## 执行边界

所有正式Gradle经主编排器、固定干净commit/tree、全局锁。测试在独占临时datadir启动自己的MySQL8与loopback随机端口Tomcat；应用连接用户只授SELECT。终止只针对本测试直接创建并持有的Process，不触碰共享数据库、其他聊天PID或生产配置。
完整日志放 `/var/tmp/cyf-history-http-20261008`；阶段/失败只摘首根因。本轮一次工具链路径诊断误将只读 gradle --version 直接执行（无构建）；已纠正，后续全部Gradle调用都走编排器，不把它当正式证据。

## 验收完成（2026-10-08）

- 完整链路：共享JSON → 合成签名JWT/真实Spring Security → loopback Tomcat HTTP → 生产Controller/事务service/DAO/MyBatis → 独占MySQL8；Node直接加载生产createApi/useHttp/fetch和Vue composable进行消费。
- Java：5个共享wire响应逐字段相等，认证/缺scope拒绝不触及SQL；JUnit 1项通过，无失败/跳过；validateLayering通过。
- 前端真实HTTP：8次请求，17条断言通过，状态码200×6/503/400；首20条+末1条、身份切换清空、scope大小写隔离、错误不是空列表、私有禁缓存均通过。
- 11次真实mapper查询，应用SELECT-only，禁止调用计数0，全表读前后快照相同。测试finally关闭自建Tomcat/MySQL，未操作共享/生产服务。
- 修正分页fixture后，原注入式消费者30条断言也通过；它的Java NOT_RUN只描述该独立诊断，不否认本次真实链路证据。

## 精确源码与安全集成

- 初始真实通过API：f04c5cc793f377c4d711309886bc99222d0e4ed5，root输入338df4eb，Web 75766a3b78c2e552ef448e924a813ed2dfc7ecd4。
- 初始API基线并非当前develop祖先，包含其他任务未合入业务；**没有整分支merge**。
- 在独立integration worktree从develop 3873dd6ab18992c70800658102d492c606216d63只移植本任务2个测试文件增量，固定新候选重新验证后ff合入本地develop；不修改生产实现，不夹带其他任务。
- 最终通过/已合入commit：`033f200e4a732d4f44b62af1cad794bd9f029ac7`；tree：`661f6ab0599427889b3bd6fde66aa172c791057c`。
- fixtureDigest：`0915145192b1f0f4679f05809f160a1acd488103259202671217cb372b8e27be`；JSON SHA-256：`155716096768978ee49483389fd89bd0fe5907036c07c1790907ddf3f7d3a7ad`。
- 持久化证据：`specs/juyiting-execution-recovery/contract-pilot/evidence/20261008-http.json`及同目录两次成功manifest/result/JUnit/完整Gradle日志，摘要均记录。源输入commit固定，后续root提交仅增加文档/证据。
- 工作证据/失败归因/本机无密钥runner保留在 `/var/tmp/cyf-history-http-20261008`。runner读取既有Maven消费凭据但不打印、不写入输出；传入Test/Node前剥离Maven环境凭据。所有正式Gradle均经编排器锁。

## 失败归因（已修复，不隐去）

1. 首轮测试源缺mybatis-spring和properties构造参数，修复依赖/调用，提交新API候选。
2. Node脚本adapter/authStore重复作用域声明；修复独立变量名，node --check通过后提交新root输入。编排器累计两次失败触发归因停止，Owner填写remediation-matrix并通过authorize-remediation恢复，没有相同输入盲重试。
3. 两个成功候选分别保存证据；集成验证是源tree变化所需验证，不是同tree重复构建。

## 明确边界与后续

本次只证明执行历史只读接口，不是所有聚义厅功能的完整验收。JWT/安全链是测试专用配置，不证明生产OAuth；前端Vue状态在Node而非浏览器，复用node_modules未证明安装完整性。未执行前端正式Flow、全量产品回归、远端push或部署；不得宣称已上线。

后续如推进发布，按版本化发布流程另跑精确版本前端Flow并补浏览器/OAuth验收；不要重复创建计划文档或复跑不变tree的后端证据。
