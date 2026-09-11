# API 3 秒性能治理

## Problem

CYF 当前后端是单体 Spring Boot 多模块工作区，当前 checkout 静态扫描覆盖 42 个 Controller、约 401 条方法级 mapping。历史接口审计只覆盖 381 个文档端点，知识库基线覆盖 38 个 Controller / 393 条 mapping，因此性能专题必须先建立“全部现役路由可枚举、可分类、可度量”的统一清单，不能只优化聚义厅的几个热点接口。

2026-09-08 的只读生产诊断已观测到聚义厅普通接口存在秒级至数十秒长尾，例如 `/agent/map`、`/agent/roster`、`/agent/tasks/search`、`/agent/tasks/status-counts`、`/agent/personas/catalog`、`/agent/scenes/{sceneId}/snapshot`。当前代码同时存在 60 秒 RestTemplate/Ribbon/Elasticsearch/MCP 等依赖超时、30 秒数据库连接获取超时、默认 `Integer.MAX_VALUE` 的分页大小，以及按请求打印参数和 JVM 内存信息的日志拦截器。另有 `UriAccessLogFilter` 在业务处理前同步写访问审计库；这些机制可能放大排队、日志 I/O、无界列表和依赖故障，却不能形成按规范化路由统计的 P95/P99 闭环。

## Goals

1. **普通同步 API 全部进入 3 秒 SLO：** 固定验收环境和负载下，每个规范化路由 `p95 <= 1s`、`p99 <= 2.5s`，`99%` 的合格请求在 `3s` 内得到完整成功响应；失败请求仍必须在 `3s` 内明确结束，但快速失败不能计作性能成功。
2. **所有现役 API 100% 分类：** 声明 surface（Controller 展开 + framework/management/error manifest）与每个可发布 profile 的运行时 HandlerMapping/management mappings 双向核对；新增路由默认进入普通同步 3 秒门禁。SSE、AI 流式、文件传输、异步任务和外部授权回调必须以精确 method + route 显式登记，不能通过条件 Bean、框架端点、通配例外或漏记规避门禁。
3. **端到端可观测：** Nginx、Spring、SQL/连接池、缓存和外部依赖使用同一 request/trace 标识，可按 route、status、outcome、依赖类型查看直方图、并发和错误。
4. **优先消除根因而非加长超时：** 批量查询替代 N+1，数据库分页/聚合替代内存分页，缓存具有授权边界和失效策略，长任务改为 3 秒内 ACK 后异步执行。
5. **性能回归成为发布门禁：** 新增或修改 API 必须有分类、预算、固定数据集和可重复的性能证据；未达标不得宣称本专题完成。

## Non-goals

- 不承诺所有 AI 回答、SSE 连接、文件完整上传/下载或长任务在 3 秒内完成；这些接口承诺的是 ACK、响应头或首个应用数据帧在 3 秒内到达。
- 不以统一强杀 3 秒代替事务、幂等、补偿和取消设计；已开始的写事务不得因客户端断开而产生未知提交状态。
- 不在生产环境直接做未经授权的压测，也不通过盲目增大 JVM、Tomcat、Hikari 或代理超时掩盖排队。
- 不在本专题中重写所有业务模块；按观测到的长尾和用户旅程分批优化。
- 不把一次 curl、少量样本、HTTP 200 或健康检查等同于全部 API 已达标。

## Scope

### API

- 路由清单与 SLO 分类注册表，默认普通同步 API 适用 3 秒门禁。
- Spring Boot / Actuator / Micrometer 请求指标、慢请求结构化日志、request-id/trace-id 透传。
- Hikari、Tomcat、JVM、SQL、Redis、RabbitMQ、LDAP、Elasticsearch、AI/SMS/微信等外部依赖的耗时和超时预算。
- 聚义厅首批热点链路：map、roster、persona catalog、task search/counts、scene snapshot。
- 列表批量查询、数据库分页/聚合、缓存、索引、事务缩短、长任务异步 ACK。
- 统一性能测试夹具、分位数计算、路由覆盖检查和发布前门禁。

### Web

- 普通请求总预算、AbortController 取消、幂等读取的剩余 deadline 重试。
- 聚义厅地图必要数据优先，roster/catalog/counts 按需加载，分模块 loading/error。
- SSE/AI 流式单独计算连接、首帧、重连，不套用完整响应 3 秒规则。
- RUM 上报用户侧请求耗时，并与后端 route/request-id 关联；不得上报 token、Cookie、正文或用户敏感数据。

### Operations

- Nginx 记录安全的 upstream connect/header/response 时间和规范化 URI。
- 在隔离预发环境执行 1、5、10、20 并发阶梯和持续测试；生产只运行低频、受控、只读合成探针。
- 建立 SLO 看板、慢路由清单、错误预算和发布阻断规则。

## Constraints and risks

- 当前 root、api、web checkout 都存在大量其他任务状态；实施必须使用任务/worktree/path 级 Owner，不能覆盖现有改动。
- 每次 Gradle 调用必须通过 `python3 ops/orchestration/cyf_orchestrator.py gradle`，并复用 exact tree/selector/fixture evidence。
- 生产与开发/构建资源争用会污染基线；容量结论只能来自资源隔离、数据固定的环境。
- Micrometer route 标签必须使用 Spring 模板路径，禁止原始 URI、用户 ID、task ID 等高基数标签。
- 缓存必须包含租户/用户/ACL 边界并有版本或失效策略，不能为性能牺牲权限正确性。
- 3 秒失败必须保留可重试性、幂等和明确错误语义；不能让超时变成重复扣款、重复任务或未知事务结果。

## Existing evidence

- `docs/implementation/handoffs/JY-PERF-SLA-20260908.md`：2026-09-08 生产只读诊断、聚义厅长尾样本和资源边界。
- `docs/project-api-endpoint-audit.md`：2026-07-18 的 381 个文档端点审计。
- `docs/knowledge-base/04-backend-api-inventory.md`：2026-08-15 的 38 Controller / 393 mapping 静态基线。
- 本专题 2026-09-11 当前 checkout 只读复核：42 Controller / 401 方法 mapping；最终数字以 PERF-01 exact-tree inventory 为准。
