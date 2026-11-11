# API 登录重定向复核与风险分析（2026-09-21）

## 结论与更正

此前将“Spring 混包 → PathPattern matcher 整体失效”认定为根因，证据不足，撤回该归因。
线上日志、已部署字节码与同 runtime 隔离复现共同支持的故障链是：

`访问日志写库失败 → 单消费者无限重试同一事件 → 内存队列满 → 安全链前的 UriAccessLogFilter 抛 AuditAdmissionException → Tomcat ERROR 转发 → 默认安全链要求认证 → 跳登录页 → 再次被审计队列拒绝`。

`.formLogin().permitAll()` 不能解除前置审计阻断，也不能放行 `/error`；不是本故障的独立止血方案。

## 线上证据

- 源 commit：`2d23f6e8d56f0cddbf25ef95e584b75b1b089382`。
- JAR SHA-256：`e92e0d5f741a84d42f19ec6a2fb12495c9d47f456479b435fc6585d6f5f8c7a7`。
- PID 417805，自 2026-09-20 11:16:01 +08:00 运行；复核未重启或修改生产。
- `/var/log/cyf-api/startlog_20260920_111602.KKoARR.log`：
  - 第 5344 行，2026-09-20 19:09:32.568：访问审计首次记录 `DataIntegrityViolationException, queued=2`。
  - 第 10034 行，2026-09-20 22:59:07.794：首次记录 `queued=1024`，随后一直满。
  - 第 10045 行起对应鉴权异常栈包含 `StandardHostValve.throwable → custom → ApplicationDispatcher.forward`：鉴权错误发生在容器错误处理阶段，不能据此断言原请求 matcher 失效。
- 2026-09-21 10:28 左右直连匿名请求：登录页、health 均 302；favicon 200。favicon 恰在审计排除列表。
- 尚未获得首个坏事件的 SQLState、vendor code、具体列。不能将字段超长、字符集、非空/唯一约束中的任一个写成已确认原因；当前重试日志只打印异常类，丢失必要归因信息。

## 代码与变更归因

- `api/base/jia-base-service/src/main/java/cn/jia/base/config/UriAccessLogConfig.java:40-43`：`/*`，REQUEST，安全链之前，仅排除静态扩展名及 druid。
- `api/base/jia-base-service/src/main/java/cn/jia/base/filter/UriAccessLogFilter.java:43-46`：审计入队成功才执行下游。
- `api/common/jia-common-service/src/main/java/cn/jia/core/audit/BoundedAuditDispatcher.java:56-65,101-138`：队满抛错；单消费者对所有 RuntimeException 无限顺序重试。
- 上述异步审计行为来自 `ea3a2bc4d7e5e43b91fa42fe8b144b2728fb742d`（2026-09-12 12:53:29 +08:00）。登录业务代码不必变化，一条不能落库的日志即可在之后触发故障。
- `DefaultSecurityConfig` 未单独处理内部 ERROR 渲染。返回 JSON 的 entry point 又依赖请求 Content-Type 精确等于 application/json；GET、multipart、带 charset 等请求可能走 HTML 登录重定向。

## 隔离对照结果

诊断目录：`/var/tmp/cyf-login-recheck-20260921-pI3US5`；`evidence.json`、`AuditRedirectProbe.java`、`probe.log`。
已逐一核对 442 个提取 runtime JAR 与线上包字节一致。使用随机 loopback 端口、真实 Tomcat/Security/UriAccessLogFilter/BoundedAuditDispatcher；持久化用合成失败，不连接生产数据库，不启动完整业务应用。

| 场景 | 登录页 | health | 观察 |
|---|---:|---:|---|
| 审计正常，原有路径 permitAll，无 form permitAll | 200 | 200 | 原规则在混合 runtime 中可正常匹配 |
| 审计队列满，原配置 | 302 | 302 | REQUEST → ERROR:/error:AuditAdmissionException |
| 审计队列满，仅加 form permitAll | 302 | 302 | 候选补丁不能修复该故障 |
| 审计队列满，允许 ERROR 渲染 | 500 | 500 | 消除重定向但业务仍不可用 |

8 项状态断言符合预期；诊断服务已停止，遗留的自有诊断 JVM 已清理。此为轻量本地诊断，不是完整应用回归、Flow 或发布证据。ERROR 全放行仅用于对照，生产应限制为内部错误渲染路径/分发类型。

## 风险与实施顺序

1. **P0 访问日志与可用性解耦**：普通访问遥测不能成为所有业务的前置准入。捕获/入队/写入故障采用可观测降级；隔离不能自动重试成功的坏事件，保留脱敏摘要和失败原因。不能把整个 filterChain 放进 catch 后重放，否则可能重复扣费/创建任务。只处理明确的日志故障，下游仍恰好执行一次。
2. **P0 错误响应保持语义**：仅允许容器内部 ERROR 到错误呈现路径；保持原 4xx/5xx，禁止错误处理进入登录回跳/保存请求。不全放开 FORWARD，不放开业务路径，不向客户端泄露 SQL/堆栈/token。
3. **P0 区分访问日志与强审计**：不可将新降级策略推广到账号、ACL、交易、钱包、订单等强审计。需要可靠留痕的操作使用同事务 outbox/持久队列和幂等投递，保留真实失败；不能把未落库写成“审计成功”。
4. **P1 修复坏事件来源**：只读核对实际 CORE_LOG DDL、约束与字符集；记录脱敏 SQLState/vendor code/列名/实际长度而非参数原文。按真实 schema 定义可验证的长度/编码策略，JSON 截断必须保持结构；DDL/DML 另核授权。
5. **P1 健康与监测**：健康探测不依赖普通访问日志队列；liveness、readiness、审计降级分别报告。监测成功写入停滞、坏事件、队列深度、拒绝数、内部 ERROR、登录自循环。不能用进程在或 favicon 200 代替业务健康。
6. **P1 精确回归**：坏事件后下一条可处理；满队列时 GET/登录/上传行为符合策略；下游至多一次；错误派发不变 302；匿名受保护资源仍 401/403；登录/PKCE/state/会话/auth_epoch/跨租户不退化；微信支付回调不得在未完成业务时返回成功 ACK。
7. **P2 依赖统一单独交付**：Boot/Framework 混合版本事实仍成立，但不是已证明的触发原因。统一受支持 BOM、锁定依赖，另跑 OAuth、MVC、multipart、WebSocket、AI/MCP、序列化、数据库回归；不要与紧急审计修复捆绑成大升级。

## 其他方案风险

- 放大队列只推迟耗尽并增加内存；盲目重启会丢失未持久化访问日志，坏事件再来仍复发。
- `ResourceServerConfig.jwkSource()` 源码启动时生成密钥：发布前核对实际密钥与会话持久化，避免意外令牌/会话失效，不能承诺无感重启。
- 短信 `/login/sms/gen` 当前为 GET，不是 POST；改方法需同步客户端，属于另项契约变更，不放进紧急修复。
- 缩小 `/oauth/**`、`/ws/**` 公开面需核对现有回调、consent 和握手认证，不能只改白名单。
- TXT 400/JPG 415 仍应单独以响应体、MIME、multipart 和配置回归归因；当前审计阻断会掩盖真实错误，不代表原上传故障已解决。

## 发布边界

本次未改应用源码、线上配置、数据库或部署。现有 `9262aeb4` 只增加 form permitAll，不足以解决本故障。
后续最小修复先针对访问日志隔离与错误派发，用 exact SHA 做正式回归，再依当前授权发布：Flow 可用时复用 5260799；不可用时按 2026-09-17 本地授权例外执行，Gradle 经 orchestrator，冻结 release 分支并记录 local_user_authorized、测试与制品哈希。不伪报流水线成功，不用旧候选或健康单点冒烟代替验证。
