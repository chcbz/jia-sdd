# API 3 秒性能治理 acceptance

## Acceptance criteria

### A. 覆盖与分类

- [ ] 当前 API checkout 的全部 Controller mapping 被展开，并生成声明式 framework/management/error surface manifest；每个可发布 profile 的运行时 HandlerMapping 与 management/Actuator mappings 被采集，声明 surface 与运行时清单双向一致并有 exact tree SHA、依赖/profile 配置摘要和内容 hash。
- [ ] 多 method、多 path、继承、条件 Bean、框架/management endpoint 均被分类；Swagger/静态资源/CORS OPTIONS 即使不进业务 SLO 也必须出现在 surface inventory。
- [ ] registry 覆盖率 100%；默认 `SYNC_STANDARD`，显式例外只允许 `ASYNC_ACK`、`STREAM_FIRST_EVENT`、`TRANSFER_TTFB`、`EXTERNAL_REDIRECT`、`OPERATIONAL`。
- [ ] 新增 route 未进入 registry 校验或未提供性能测试时 CI 失败。

### B. 观测

- [ ] 每个规范化 route 可查看 count、p50、p95、p99、max、status/outcome、inflight；标签无 ID/URI 高基数。
- [ ] 每条慢请求可用 request/trace ID 关联网关、Spring、SQL/连接池、缓存和外部依赖主要耗时。
- [ ] 日志不记录 Authorization、Cookie、token、query、请求正文或用户敏感参数；现有逐请求参数 INFO 默认关闭；访问审计写库不再无界阻塞普通请求。
- [ ] Hikari pending/acquire、Tomcat busy、JVM GC pause、process CPU/memory、数据库慢查询/锁等待有可观测证据。

### C. 3 秒性能门禁

- [ ] `SYNC_CRITICAL`：逐 route p95 <= 500ms、p99 <= 1s，1s 内成功或明确失败。
- [ ] `SYNC_STANDARD`：逐 route p95 <= 1s、p99 <= 2.5s、`SLI_3s >= 99%`，有效已授权请求语义成功率 >=99.9%；3s 内完整成功或明确失败，快速失败不计性能成功。
- [ ] `ASYNC_ACK`：p95 <= 1s、p99 <= 2.5s、99% ACK <=3s，且任何请求 3s 内 ACK 或明确失败；符合 operation v1 的提交/查询 method+path、完整 status view、单调 version/state、result/error、404 防存在性侧信道、ACL、幂等、原子性和保留期合同。
- [ ] `STREAM_FIRST_EVENT`：握手 p95 <= 1s，99% 握手及首个应用帧 <=3s；任何连接 3s 未达门禁则明确结束，断线、认证失败和依赖慢场景有界清理/退避。
- [ ] `TRANSFER_TTFB`：请求 body 接收完成后 99% ACK/响应头 <=3s，任何请求 3s 内 ACK/响应头或明确失败；完整传输另有按大小分桶吞吐证据。
- [ ] `EXTERNAL_REDIRECT`：本系统 99% 本地处理 <=3s，任何请求 3s 内重定向或明确失败。
- [ ] 首批核心 route 每档预热后 >=30 分钟、>=10,000 合格样本，连续 3 轮通过；低流量 route >=1,000 合成样本，否则标记 insufficient，不得 PASS。

### D. 正确性与安全

- [ ] 性能优化不改变 ACL、租户/用户隔离、事务原子性、幂等、snapshot/SSE fencing 和现有兼容 contract。
- [ ] 聚义厅 map/roster 继续分别使用 `/agent/map` 与 `/agent/roster`；不重新引入 `/agent/active`；任务分配继续传显式目标 Agent。
- [ ] tenant/client/task/owner 与 identity 按 byte-exact 语义校验；版本为十进制字符串且单调；SSE 保持 live-before-replay、去重、gap/resync、授权重放、有界缓冲和断线清理。
- [ ] Web reducer 幂等并拒绝旧 generation/重复事件覆盖新状态，不引入第二状态源。
- [ ] 缓存键和失效策略使用无歧义编码覆盖 tenant/jiacn、client_id、task/资源 scope、owner/principal、subject、ACL-policy/data version，全部 byte-exact；无跨租户、client、task、owner 或用户数据泄漏。
- [ ] 预算耗尽、依赖断开、连接池耗尽、慢 SQL 和客户端取消不会产生重复写或未知事务；若不可避免则返回可查询 operation ID。
- [ ] 普通读只在剩余 deadline 内最多重试一次；写接口不做无条件自动重试；page size、批量条数和上传大小有统一上限。

### E. 首批热点

固定 100 Agent、1000 Task、约定 persona/scene 数据夹具：

- [ ] `GET /agent/map`
- [ ] `POST /agent/roster`
- [ ] `POST /agent/tasks/search`
- [ ] `POST /agent/tasks/status-counts`
- [ ] `GET /agent/personas/catalog`
- [ ] `GET /agent/scenes/{sceneId}/snapshot`

以上 route 均达到 `SYNC_STANDARD`，且 SQL 次数不随 Agent/Task 返回数量线性增长。

### F. 发布

- [ ] API/Web exact commit、tree SHA、route inventory hash、fixture digest、测试 selector 和结果已记录。
- [ ] API Gradle 通过 `cyf_orchestrator.py gradle` 串行执行；未对 unchanged tree 重复全套验证。
- [ ] 独立 `sol_reviewer` ACCEPT，最终 `release_guard` 放行。
- [ ] 生产发布后低频只读 smoke 和 24 小时 SLO 观察通过；无未经授权的生产压测。
- [ ] 每个例外含精确 method+route、justification、owner、contract reference、compliance 和 review_by；通配例外、pending compliance 或过期 review 一律阻止 accepted。
- [ ] 全部 registry route 达标后才将专题标记 accepted；滚动 28 天观察窗口达标后再讨论对外 SLA。

## Verification evidence

- API revision: pending
- Web revision: pending
- Root revision: pending
- Route inventory count/hash: pending
- Fixture digest: pending
- Environment: pending
- Commands/tests: pending
- Result: pending
- Contract reviewer: sol_reviewer R4 delta ACCEPT P0/P1/P2=0/0/0（R3 两项 P2 已收敛）
- Implementation reviewer: pending
- Release guard: pending

## 2026-09-11 首批源码证据（不勾选整体验收）

- `PERF-A02-LOG`: exact API `014fb7edaa53928aa5ca309ea4c8537889763563` / tree `4de32d4ccdb1efe06dd38ee2ff4009532d5300ab`。独立 `sol_reviewer` source + scoped unit ACCEPT 0/0/0；JDK21 cached-jar javac/JUnit native0，6 found/executed/PASS，0 skipped/failed/aborted。
- 证据 key `13c9ddf4824b54e4260663f540085dde1ed0992e16a8bec73b1ae96563ca3c6c`，目录 `/var/tmp/cyf-perf-verify-20260911-T7Yu/a02-exact-source-junit-r3`；源码/26 jar/终端 manifest 已由 main 和独立 reviewer 验证。
- 干净集成分支 `codex/perf-api-integration-20260911` 已推送，tree 与 accepted candidate byte-exact；不是 develop/部署/整体集成验收。
- 失败历史：CLI 参数顺序 prelaunch rc2；修正后实际 Gradle rc1（root publishing config 缺 repoUsername），未执行模块测试。定向 harness 通过不能改写为 Gradle PASS。
- 清单工具和 histogram 各自仍在有界修复/独立验收中；详见 `../../docs/implementation/handoffs/PERF-FIRST-BATCH-20260911.md`、`../../docs/implementation/handoffs/PERF-VERIFY-R2-ROOT-CAUSE-20260911.md`。全部顶层性能验收仍 pending。

### 同日首批结束补充

- `PERF-A01-HIST`: API `99c820216adaa608e98ff120c7e4fe637fcd8812` / tree `ac02104c1e5a21f52146b92593a2af7a03d680db`，独立 source + cached-JDK21 javac/JUnit 5/5PASS ACCEPT0/0/0；证据 `/var/tmp/cyf-perf-verify-r4-RSmqXQ`，key `ad55b2efab8755434b524dffda6d154e0256ea65728278e94d62f060ccb27c1f`。
- 两项 accepted API 切片已无冲突合入并推送 `5571d183fe7c612f2d5ebb272548aa5bfad77e90` / tree `b993a925464701b5a17c93461cf3f558036f5d13`；6 文件 blob 与对应原候选一致。这里的6+5测试为两个原树的 scoped evidence，不是合并树新跑11项或整体构建证明。
- `PERF-01-TOOLS`: `609cd1c` 的19项独立测试通过，但最终 source REJECT0/2/0；停止认领，保留修复矩阵。CLI对 exact API `014fb7e` 的440条 supported mapping 只是部分静态诊断，返回预期非零，并非 inventory PASS。
- 未发布；完整 Gradle 模块构建、运行时清单、跨链路观测、隔离压测、热点查询优化和全API≤3秒仍 pending。


### 同日 R3 独立验证补充

- `PERF-BUILD-01`: 合并 API `5571d183fe7c612f2d5ebb272548aa5bfad77e90` / tree `b993a925464701b5a17c93461cf3f558036f5d13`，使用明确非敏感占位发布属性，经 orchestrator 单次 offline Gradle 执行 `:common:jia-common-service:test --tests cn.jia.core.interceptor.HttpRequestLogInterceptorTest`，native0、12/12任务执行、6/6测试PASS、零失败/错误/跳过。不是完整模块/starter/metrics测试或启动/性能证据；旧失败历史不改写。
- 证据 `/var/tmp/cyf-perf-build-r3-fDNNWL`，key `d5ebc5886ad7954f3c6202eb268fafb2255c92dfb779ed97f880c5af3973ce43`，manifest `4a93fcf1f3229e9f68c800a4ef8bb1ac0362ec0a6cc7a489bbb6585246c978c9`；main复核15项hash；独立证据审查ACCEPT0/0/0，仅此定向Gradle证据切片验收通过。
- `PERF-01-TOOLS` R3候选 `f2b9e65641c9ac72021666314dcc866568a0dfe4` / tree `414281d47cd0772830dfda1e24464f1416897e90`：独立Python3.6.8 25/25测试PASS、CLIhelp0、零跳过；key `bbbab4da6f2ecfc5f360ccfbff9979c24ec087a2fa6694057e83db4830ee9ff1`，证据 `/var/tmp/cyf-perf-inventory-r3-yLWLnu`，main复核21项hash。源码审查及真实CLI scan→reconcile正例/非Controller注解反例复核待完成；不得提前标为清单或SLO通过。
- 执行合同/归因和后续审查记录：`../../docs/implementation/handoffs/PERF-CONTINUE-R3-20260911.md`。没有发布或生产压测。


### 同日 R4 最终有界验收

- `PERF-01-TOOLS`：最终 `43e0e46f8d9a07797713adb432c3bcab770dd8b0` / tree `e0a9c30fa385c1ff0ae42d2f70f97dd5d87bc3b9`，独立源码/实际测试证据 ACCEPT0/0/0。26 项实际单测PASS、零实际跳过；真实CLI合成 scan/reconcile 正例0/0，自定义注解负例预期2且含 fatal诊断。
- 原始证据 `/var/tmp/cyf-perf-inventory-r4-mkXwWD`；main审计 `/var/tmp/cyf-perf-r4-main-audit-wxj3fs0x`，receipt SHA256 `90342e89d43860a83027ba827e486c70882e6f818210e46367daa1c6ed8362a3`，raw manifest SHA256 `b8fa0f47ce52f056c4e1d5a6dda96106dc3390b32231d3019a78b03c965bcf18`。独立 reviewer 复核原始结果/hash/clean exact identity。
- 验证包装器误处理预期非零、元数据脚本误匹配测试名这两次失败保留；未重跑测试或伪造成功 wrapper/cache HIT。reviewer 将此格式缺口判为有界源码验收的非阻断项，不等于完整流水线成功。
- 工具分支已推送，根专题分支 merge `45f5f07527e70d2fba9cc90f4ace9fdc95333825` 的4个工具文件 blob 与 accepted candidate 完全一致。复用原候选实际测试证据，不宣称新合并树跑过全套。
- 本次新增实际 Gradle6PASS 和工具26PASS分属不同候选/selector，不能相加解释为32个API达标。完整清单、真实profile、registry、隔离压测及所有顶层性能验收继续 pending；未部署。
