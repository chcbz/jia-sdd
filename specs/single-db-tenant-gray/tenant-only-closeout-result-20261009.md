# Tenant-only 实际进展 · 2026-10-09

当前 **IMPLEMENTING / NOT_READY**；已审查的局部修复已形成本地 checkpoint，正在串行收敛固定 tenant1 的前端认证与缓存。未启动服务、未改共享数据库；不是可运行候选交付。

局部 checkpoint（未 push，非新的可复现集成 pin）：API `932ca9733d12b95ba9c18ac3684317d5710cbfd1`（9路径）；Web `8502d3421cd9f3c58f6b775ac03845c810372486`（2测试路径）。Root 合并基线 gitlinks 暂不改写。

主控追加（2026-10-09 13:56）：本轮9个API路径与2个Web测试harness路径的独立只读审查ACCEPT，P0/P1/P2新增缺陷0；42后端、86+31前端及编译证据已独立检查。接受只适用于局部修复，非完整功能验收。审查另确认既有DAO/relay仍限制tenant0，后续源码收敛不能纯归因于数据库连接失败。下一批继续可离线验证的固定tenant1前端认证/缓存收敛；实际共享库/测试身份/可信issuer配置仍待落实。

构建/诊断目录：`/mnt/Workspace/cyf-tenant-only-20261009-fHiVv5`。所有 Gradle 使用 `/tmp/cyf-gradle.lock`，新 Gradle cache、project cache、build outputs/logs 均在该目录。

- 已复用现有 Gradle 私有插件配置（未输出凭据），没有改项目 dependency-management 配置。
- 真实合并后编译发现 EsContext 重复 tenantId 字段，已保留单一定义；重新编译发现 AgentWebSocketHandler 重复 sessionTenantId 方法，已保留单一实现。两轮失败 log 保留，未逐个盲修 Lombok cascade。
- 已修正 Juyiting scope 的 owner/tenant 契约：按可信 tenant/client/owner 查询任务可写成员，新增实际服务 ACL 与 wrapper 的 tenant0/1、跨 owner/client/tenant 回归。尚未放开固定0的 Hall/任务路由或宣称通路可用。
- 前端原配置 production build 已完成（1m1s）；tenant ledger/tab/namespace/OAuth 定向回归31通过。产物/log均在上述目录，未部署。
- 共享 DB 安全只读连接使用 feature 已有 application-dev.properties：`SQLException / SQLState 28000 / MySQL error 1045`。连接被拒绝，尚未执行SQL，tenant1与测试身份归属未证明。prod/grey配置目标均不同于dev，未将它们当同库替代或尝试连接；未重用33307/33630实例。
  Java Properties 实际读取的是存在且非空、无环境占位符的 `spring.datasource.url/username/password`；dev没有 `spring.datasource.db-url`。这不是CONFIG_MISSING或误读字段，确实已到达MySQL认证阶段；未打印连接目标或凭据。

仍需现有共享数据库的可用只读连接授权，以及本地测试入口的可信issuer/JWKS与tenant1测试身份。环境没有对应CYF/VITE/SPRING变量。不能因配置缺失而自动迁移共享schema、复制tenant0数据或伪造tenant1身份。

`:starter:compileJava` 已真实成功（4m40s）。任务成员ACL 4测试和对话20测试已通过。backend首轮1个新增ACL测试异常类型预期与既有`require`契约不符；拒绝已生效，修正为IllegalArgumentException并保留精确拒绝消息断言。

Web HTTP/SSE/Hall首轮83通过3失败；单独复现显示visibility用例通过，另两项为测试harness：Vue缺少全局Document/ShadowRoot、EOF断言只等待5次Promise。已补DOM类、等待真实事件循环、把3个stream用例dispose移到finally，原业务断言不变。按项目既有`node --import tsx`执行后HTTP/SSE/Hall **86通过**（15s），tenant/恢复/cache **31通过**（1s）。生产Web组件未改。所有失败与错误命令log仍保留，不改写原失败。

OAuth定向回归发现真实机器身份问题：统一TenantClaimPolicy把合法无tenant machine token拒绝，并把显式tenant机器claim当用户tenant写入EsContext。已在EsSecurityContextFilter对机器/legacy machine显式清除cookie用户字段与用户tenant/domain，只保留machine client；恢复原assertNull断言并新增合法无tenant两类machine回归。最终 `:starter:compileJava` 与完整backend定向任务 **BUILD SUCCESSFUL**（1m57s），XML共 **42 tests / 0 failures / 0 errors / 0 skipped**：Agent4、Chat20、OAuth18（`backend-scope-tests-machine-fix.log`）。Agent4使用本轮前次通过的UP-TO-DATE结果；Chat/OAuth本次实际重跑。此前失败保留。

最终证据：`web-http-sse-hall-tests-final-tsx.log`（86）、`web-tenant-tests-final-tsx.log`（31）、`web-build-original-config.log`（production build）、`shared-database-readonly-final.log`（1045，SQL未执行；Java进程exit0是已捕获异常，不是DB连接成功）。API/Web `git diff --check`均通过。

**尚未完成的源码工作不能归为纯环境问题**：local-test-area仍为conversation-only平台注册profile；认证/resolver仍依赖domain/revision bundle；Hall/map/roster/task与部分relay/DAO仍固定tenant0；前端固定tenant1认证尚未去除平台revision依赖。继续完成可离线验证的源码收敛，不以数据库配置缺失阻止该部分工作。实际共享库联调另需取得可用只读授权并核实测试身份/可信issuer/JWKS，保留现有AccountSecurity auth_epoch与tenant/client/user/issuer绑定，不能伪造身份或把旧tenant0 token当tenant1。未做路由解锁、未启动Spring（自定义SchemaInitializer可能DDL），未声称tenant1真实入口已可用。

Runtime与旧R4没有修改或重跑。main-owned integration.yaml未改。
