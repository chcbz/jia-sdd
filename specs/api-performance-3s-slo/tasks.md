# API 3 秒性能治理 tasks

任务执行状态只进入 `docs/implementation/TASKS.yaml#runtime_ledger_json`；本文件定义工作分解和依赖，不构成第二份运行台账。

## Phase 0：合同与基线

- [ ] `PERF-00`（main_orchestrator，root docs）：冻结 SLO、route 分类、固定负载、数据夹具、异常口径和证据格式。
- [ ] `PERF-01`（routine_worker，root tooling）：生成 Controller 展开清单 + 声明式 framework/management/error surface manifest，并在 grey/prod-like exact candidate 上采集运行时 HandlerMapping/management mappings；双向比对、校验 registry，输出 profile/count/hash。
- [ ] `PERF-02`（gpt_test_runner，只读）：在隔离环境建立未优化基线；禁止生产压测，记录 exact API tree、fixture digest、JDK/DB/CPU/内存和缓存冷热。
- [ ] `PERF-03`（sol_reviewer，只读）：独立审查 SLO 是否可测、例外是否被滥用、样本数与分位数是否足够。

## API (`api/`)

### Phase 1：观测与预算

- [ ] `PERF-A01`（balanced_worker）：加入低基数 Micrometer route histogram、inflight、deadline/slow counters 和 Hikari/Tomcat/JVM 暴露；owned paths 预计为 common starter/service 与 starter 配置。
- [ ] `PERF-A02`（balanced_worker）：安全 request ID/trace ID filter 和慢请求结构化日志；替换默认参数 INFO 日志，不记录敏感值。
- [ ] `PERF-A02B`（critical_worker）：将同步访问审计写库从普通请求关键路径移出，冻结 after-commit/outbox/失败降级与审计不丢失边界。
- [ ] `PERF-A03`（critical_worker）：实现剩余 deadline 传播和统一 timeout/error contract；写事务、幂等和取消边界需独立 P0 审查。
- [ ] `PERF-A04`（balanced_worker）：为 DB、Redis、LDAP、Elasticsearch、Rabbit、外部 HTTP/AI/SMS/微信建立分层预算；移除普通链路 30–60 秒无差别等待，并禁止业务代码临时无 timeout HTTP client。

### Phase 2：聚义厅热点

- [ ] `PERF-A10`（critical_worker）：`/agent/map`、`/agent/roster` 的 persona/task/status 批量读取，保持 map/roster 分流、byte-exact identity 与 tenant/client/owner ACL，SQL 次数固定上界。
- [ ] `PERF-A11`（critical_worker）：`/agent/tasks/search` 过滤、授权、分页下推 SQL；保持请求/响应、排序、显式目标 Agent 和 ACL 兼容。
- [ ] `PERF-A12`（critical_worker）：`/agent/tasks/status-counts` 数据库聚合；与 search 使用同一 byte-exact 授权范围。
- [ ] `PERF-A13`（critical_worker）：persona catalog 版本化缓存；缓存 scope/失效 after-commit，用户绑定态不进入共享缓存。
- [ ] `PERF-A14`（critical_worker）：scene snapshot 一致性和查询降本，不破坏十进制版本、单调 generation、snapshot/SSE fencing。
- [ ] `PERF-A15`（critical_worker）：Chat/Agent SSE 有界缓冲、首帧 deadline、断线/慢消费者清理、live-before-replay、gap/resync 和授权语义。
- [ ] `PERF-A16`（critical_worker）：统一 operation v1、幂等、ACL、原子 outbox、状态查询和保留期；逐 endpoint 审计后才允许 `ASYNC_ACK` compliance=pass。

### Phase 3：全模块批次

- [ ] `PERF-A20`（explorer，只读）：按 p99 × 流量 × 错误预算生成 user/material/isp/task/chat/wx/sms 等模块的优化排序；输出 acceptance -> paths -> tests -> dependencies 矩阵。
- [ ] `PERF-A21-USER`（critical_worker；依赖 A01-A04）：owned paths 限 `common` 分页合同与 `user` list/service/mapper/test；统一 page size 上限，消除 `/user/list` 3N 查询并保持全部 ACL/排序兼容。
- [ ] `PERF-A22-EXTERNAL`（critical_worker；依赖 A03-A04）：owned paths 限 `sms`、`oauth` 外部回调/client/test；统一剩余预算、幂等和明确失败，禁止事务内网络调用。
- [ ] `PERF-A23-LONGOPS`（critical_worker；依赖 A16）：owned paths 限 `task/job`、`material/news`、`wx` 长同步操作及 operation/outbox adapter/test；逐 route 版本化迁移为 `ASYNC_ACK`，不得静默改变旧接口。
- [ ] `PERF-A24-<MODULE>-<SEQ>`（默认 critical_worker）：后续每批必须在唯一运行台账展开为独立 ID、exact base、依赖和不重叠 owned paths；仅当只涉及冻结合同下的机械投影/mapper 修改且无 ACL/事务/缓存/异步风险时，才可由 main_orchestrator 经 sol_reviewer 预审后改派 balanced_worker。

## Web (`web/`)

- [ ] `PERF-W01`（balanced_worker）：普通 JSON 请求 5 秒总预算、AbortController、剩余 deadline 和错误分类；SSE/上传下载显式排除。
- [ ] `PERF-W02`（balanced_worker）：聚义厅 map/snapshot 优先，roster/catalog/tasks/counts 按需加载和独立 loading/error。
- [ ] `PERF-W03`（balanced_worker，冻结合同）：SSE/AI 流式指数退避、jitter、连接去重、隐藏页暂停、认证失败停止重连；reducer 保持 generation fencing、去重、gap/resync 和幂等。
- [ ] `PERF-W04`（balanced_worker）：安全 RUM request timing 与 request ID 关联，默认采样且不含敏感数据。

## Operations / deployment

- [ ] `PERF-O01`（runtime Owner）：Nginx 增加安全 upstream connect/header/response timing、request ID 和规范化 URI；保留配置语法和回滚证据。
- [ ] `PERF-O02`（runtime Owner）：生产运行与构建/测试/Agent 资源隔离；不跨线程终止进程。
- [ ] `PERF-O03`（release_guard）：建立 SLO dashboard、慢路由榜、错误预算和告警；低流量使用最小样本门槛。
- [ ] `PERF-O04`（release_guard）：每批发布前 exact SHA/fixture/selector gate，发布后只读 smoke；生产压测另行授权。

## Integration and verification

- [ ] 声明 surface（Controller + framework/management/error manifest）与每个发布 profile 的运行时 HandlerMapping/management mappings 双向一致；全部 surface 均已分类，未知、动态未展开或 profile 差异 = 0。
- [ ] 聚义厅六个热点 route 在固定数据集下 p95 <= 1s、p99 <= 2.5s、3s 内完整响应/明确失败。
- [ ] 全部 `SYNC_*` route 逐模块具备足量样本；不能用总体平均值替代逐 route 证据。
- [ ] SSE/AI 首帧、异步 ACK、文件 TTFB 使用专用门禁并有异常场景。
- [ ] 数据库查询次数、连接等待、GC、外部依赖耗时和错误可通过 request/trace ID 关联。
- [ ] gpt_test_runner 验证后由 sol_reviewer 独立审查；最终 release_guard 只读放行。

## 2026-09-11 首批实施切片（不改变原验收合同）

- `PERF-01-TOOLS`：离线扫描/严格输入校验/运行时导出对账工具及负例测试；不包含真实 grey/prod 采集、完整 YAML registry 校验。父任务 `PERF-01` 在这些缺口关闭前仍未完成。
- `PERF-A01-HIST`：已有 HTTP observation 的 histogram/SLO buckets 与 URI 标签上限；不包含 exporter/dashboard、inflight/deadline 或生产指标验收。父任务 `PERF-A01` 保留剩余工作。
- `PERF-A02-LOG`：MVC interceptor 请求内单调计时与无敏感参数慢日志；不等于完整入口 filter、跨网关/SQL trace 关联或完整网络响应耗时。父任务 `PERF-A02` 保留剩余工作。
- `PERF-REVIEW-01`：首批独立只读 Review。切片 source/unit acceptance 与模块构建、跨仓集成、部署、3 秒达标分开记录。
