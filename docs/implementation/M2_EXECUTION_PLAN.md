# M2 可恢复实时协作执行计划

> 版本：1.3（2026-08-17 引入 GPT-5.3 Codex Spark 快速 Writer）
> 初始冻结日期：2026-08-03；本次策略更新：2026-08-17
> 范围：M2 持久任务事件、workspace snapshot、SSE replay/resync、前端 TaskWorkspace/Timeline
> 设计依据：`docs/juyiting-multi-agent-collaboration-design.md` 第 7.5、13、21、22 节
> 任务账本：`docs/implementation/TASKS.yaml`
> 模型路由：`docs/implementation/MODEL_ROUTING.yaml`

## 1. 执行结论

M2 改为**健康门控、任务/worktree/路径级并行 Writer 流水线**。原始任务 ID、独立 commit、验收项和状态全部保留，但把高耦合任务放入同一 Writer/worktree，减少重新探索、worktree 创建、merge、全量测试和 Reviewer 交接。

```text
源码槽 A：当前任务独占其 worktree/owned paths 的 Writer
只读槽 B：Explorer 准备下一微阶段调用链/冲突
只读槽 C：Fast Query 准备 acceptance -> path -> test -> evidence
只读槽 D：GPT Test Runner 或独立 Reviewer
```

执行包和硬依赖：

```text
BE1: C02 -> C03
  -> BE2: C04
  -> BE3: C05 -> C05F
  -> FE1: C06 -> C07A
  -> FE2: C07B -> C07C -> C07 -> C07F
  -> WG: C08W

BE3 accepted 后：AG/C08A 只读累计门禁可与 FE1/FE2 并行
AG + WG accepted -> RG/C08 最终 GO/NO-GO
```

- 独立任务允许并行源码 Writer；必须使用独立 worktree，并在开始前冻结不重叠的 owned paths。
- C08A 默认是只读累计门禁；若发现 API 必须修复，可在独立 worktree 并行 claim，仅在路径重叠时协调交接。
- 重型 Gradle、隔离 MySQL、npm full test/build 全局串行。
- 每个原始任务仍有独立微阶段验收；ACCEPT 后主控自动推进，不再逐项等待用户确认。任务正常自动推进；每次完成、异常或需要用户处理时主动汇报并给出可执行下一步。
- `docs/implementation/**` 仅由主控修改，代码 Writer 不争用控制面文件。

### 当前模型健康降级

2026-08-23 起按用户指令执行 OpenAI-only 路由；不再派发 DeepSeek 或运行其健康探针。2026-08-17 本机 Codex 对 `gpt-5.3-codex-spark` 的只读健康探针返回 `SPARK_OK`。为兼顾速度和门禁：

- 已开始的 C04 保持 `critical_worker / GPT-5.6 Sol High`，不在候选中途换模。
- C05～C07F 的冻结契约、分包实施与 focused tests 使用 `spark_worker / GPT-5.3 Codex Spark Medium`。
- 新身份/ACL 语义、事务重设计、迁移或破坏性数据修改必须升级给 `critical_worker / GPT-5.6 Sol High`。
- 验证统一使用独立 `gpt_test_runner / GPT-5.4 Mini Medium`；Review 和最终门禁继续使用只读 Sol High。
- Writer 与 Reviewer 必须分离；Spark 不自验收、不修改控制面、不部署。

## 2. 为什么这是当前更优分配

| 决策 | 依据 | 提效/避险 |
| --- | --- | --- |
| C02+C03 合并为 BE1 | 同一 broker/replay runtime、DAO 和连续性状态机 | 保留 C02 微门禁，减少一次 worktree/上下文重建和中间集成 |
| C04 单独保留 P0 门禁 | snapshot 事务、浏览器 ACL 和一致版本边界独立且高风险 | 避免 SSE/UI 需求掩盖快照一致性问题 |
| C05+C05F 合并为 BE3 | flag 直接包裹新 endpoint，路径和测试高度重叠 | C05 先 ACCEPT，再追加默认关闭策略，省去一次 Writer/branch 交接 |
| C06+C07A 合并为 FE1 | composable/reducer 与页面状态接入共同拥有唯一前端状态源 | 防止第二套 workspace 状态和重复恢复逻辑 |
| C07B/C07C/C07/C07F 合并为 FE2 | 组件、JuyiHall、测试和 flag 路径重叠 | 同一 Spark Writer 严格顺序实施，消除多 Writer 冲突 |
| C08A 只读门禁与 Web 实施重叠 | API 在 BE3 后已冻结，C08A 通常只做累计证据 | 节省等待；若需源码修复则在独立 worktree 并行 claim，路径冲突时协调 |
| OpenAI-only 路由 | 用户已暂停 DeepSeek；Spark 本机探针通过 | 由 Spark/Terra/Luna 加速冻结契约实施，Sol 保留高风险与最终门禁 |
| 最终 tree 才跑全量 | 多轮开发阶段重复全量测试收益低、耗时高 | targeted 开发验证 + 最终一次 full/isolated gate |

剩余账面复杂度约 20 人日；执行包合并和只读门禁重叠预计节省 **3～4 个执行日**，目标约 **16～17 个复杂度日**。这是边界估算，不包含多轮 P0 驳回、基础设施故障或生产审批时间。

## 3. M2 不可变设计约束

1. MySQL 是 task state、task event、workspace version 的唯一事实源。
2. `agent_task_meta.task_version` 仅用于任务聚合 CAS；只在 task meta 自身发生业务变化时按既有状态机规则递增。
3. `agent_task_meta.current_event_version` 是任务级持久事件游标；每成功插入一个 task event 恰好递增一次。
4. `agent_task_event.event_version` 等于该事件分配后的 `current_event_version`；唯一键为 scope + task + event_version。
5. snapshot 的 `currentVersion`、SSE `id`、`Last-Event-ID` 和前端 reducer 游标全部使用 event version，不使用 aggregate `task_version`。
6. B03～B08 的所有协作成功写路径必须与对应 event 插入、`current_event_version` 更新在同一事务；不得遗漏 legacy assign/report。
7. B09 不写 task event；C01H 使用确定性 event ID 为受影响任务追加幂等 `HISTORICAL_BASELINE_IMPORTED`，保持 `task_version` 不变。
8. after-commit 才允许向进程内 Broker 发布已持久事件；回滚事务不得产生实时唤醒。
9. SSE 先订阅 live，再 replay 数据库历史，避免连接窗口丢事件。
10. 检测到历史清理、版本缺口、游标超前或无法证明连续性时，发出 `resync_required`，不得猜测补齐。
11. workspace snapshot 必须在一个可解释的一致性边界内返回数据及 `currentVersion`。
12. 前端版本值按十进制字符串处理，禁止把 Java `Long` 窄化为 JavaScript `Number`。
13. reducer 幂等规则：`event.version <= currentVersion` 直接忽略；只接受恰好下一版本，否则 resync。
14. SSE 多次失败后降级轮询；页面恢复可见时重新校验版本。
15. tenant/client/task ACL 全链路 fail closed；跨 scope 不返回 snapshot、event 或存在性侧信道。
16. Juyi Hall 的 `/agent/map` 与 `/agent/roster` 数据流保持分离，不得重新引入 `/agent/active`。
17. M2 API/Web feature flag 默认关闭，只能按获准测试 scope 开启。
18. RabbitMQ 可在 M3 运输命令，但不得替代 M2 的数据库 replay。

## 4. 完整任务与 Agent 分配表

| 包/顺序 | 原任务 | 执行方式 | 当前 Writer/Executor | 只读 Support | Reviewer | 预估 |
| --- | --- | --- | --- | --- | --- | ---: |
| 已完成 | M2-00、C01、C01B、C01H | 已 accepted/integrated | 历史 Owner | 已有证据 | 已 ACCEPT | 7.5 日 |
| BE1-1 | C02 | 同一 worktree 微阶段 1 | **Sol High critical_worker** | Terra Explorer + Mini Matrix + GPT Test | Sol High independent reviewer | 2 日 |
| BE1-2 | C03 | C02 ACCEPT 后微阶段 2 | **同一 Sol Writer** | Terra + Mini + GPT Test | Sol High independent reviewer | 3 日 |
| BE2 | C04 | 独立 P0 包 | **Sol High critical_worker** | Terra + Mini + GPT Test | Sol High independent reviewer | 2.5 日 |
| BE3-1 | C05 | 同一 worktree 微阶段 1 | **GPT-5.3 Codex Spark Medium** | Terra + Mini + GPT Test | Sol High independent reviewer | 2 日 |
| BE3-2 | C05F | C05 ACCEPT 后微阶段 2 | **同一 Spark Writer** | Mini + GPT Test | Sol High independent reviewer | 0.5 日 |
| FE1-1 | C06 | 同一 Web worktree 微阶段 1 | **GPT-5.3 Codex Spark Medium** | Explorer + Mini + GPT Test | Sol High independent reviewer | 3 日 |
| FE1-2 | C07A | C06 ACCEPT 后微阶段 2 | **同一 Spark Writer** | Mini + GPT Test | Sol High independent reviewer | 1.5 日 |
| FE2-1 | C07B | 展示 UI | **GPT-5.3 Codex Spark Medium** | Explorer | Sol High independent reviewer | 1.5 日 |
| FE2-2 | C07C | C07B 后 responsive/a11y/tests | **同一 Spark Writer** | Mini + GPT Test | Sol High independent reviewer | 1 日 |
| FE2-3 | C07 | 集成/Juyi Hall 回归 | **同一 Spark Writer** | GPT Test | Sol High independent reviewer | 0.5 日 |
| FE2-4 | C07F | 默认关闭和 M1 降级 | **同一 Spark Writer** | Mini + GPT Test | Sol High independent reviewer | 0.5 日 |
| AG | C08A | BE3 后只读累计 API gate | **GPT Test Runner**；冲突才由 Sol 修复 | Mini evidence | Sol High reviewer | 0.75 日 |
| WG | C08W | FE2 后最终 Web gate | **GPT Test Runner**；冲突才由 Terra 修复 | Mini evidence | Sol High reviewer | 0.75 日 |
| RG | C08 | 双仓最终 GO/NO-GO | 主控 Sol High | Mini evidence | Sol reviewer + release_guard | 0.5 日 |

> 当前 C05～C07F 已冻结为 Spark 路由；除非 Spark 健康探针失败或触发 P0 升级条件，否则不在包中途换 Writer。

## 5. 每项任务详设、路径与验收

### M2-00：基线收敛

**执行内容**

1. 锁定 `api/develop`、`web/develop` 的基线 SHA 和远端同步状态。
2. 对 `api/` 主工作树全部 dirty 路径记录 owner、用途和 SHA-256；禁止 reset、clean、checkout/switch 或覆盖。
3. 按对象哈希冻结两个 stash：`75a3458d8a25faa9d70deb01c53ae185d7d9f7cc`、`12f0b4e6149e904e92082bb8642d3086cad033ec`；不得仅依赖会漂移的 `stash@{0,1}`，不得 apply/pop/drop。
4. 检查 Agent 日志中是否仍有 `MESSAGE_TYPE_REQUIRED`；若有，建立独立兼容修复任务，不夹带进 C01。
5. 确认 B09 状态为“代码已验收、生产回填未执行”；M2 开发不得隐式执行 B09 DML。
6. 不接触被脏主树占用的 `develop`：从精确 SHA 创建 `feat/m2-api-base-20260803` 与 `feat/m2-web-base-20260803` 两个累计 clean base 及独立 integration worktree。
7. 后续任务只能从对应累计 base 的最新 accepted/integrated HEAD 分支，不从脏 `develop` 或文件系统复制。
8. 建立 API 与 Web 基线构建/测试证据；测试数据库必须隔离，禁止生产 DML。
9. 记录 B07/B08/B09 的“双状态”：源码已进入锁定 API 基线；生产迁移/回填未 apply。
10. 资源观测：记录磁盘、inode、内存和 swap，但自 2026-08-28 起不再以固定内存或磁盘阈值拒绝 Gradle、npm build、隔离 MySQL/Rabbit 或 integration worktree。资源不足导致的真实 OOM/ENOSPC 仍按失败归因处理，重型资源继续串行。
11. 在 M2-00 handoff 生成控制面 SHA-256 清单，并将摘要写入 C01 首个 Git commit trailer，弥补仓库根目录不是 Git repo 的追踪缺口。

**退出门槛**

- 基线 SHA、两个累计 base branch/worktree、dirty checksum、stash object SHA、M1 双状态、资源观测和测试证据写入 handoff。
- 所有用户未提交修改仍原样存在。
- 若协议日志异常存在，已有独立任务 ID、Owner 和验收条件。
- 不设固定可用空间或 MemAvailable admission gate；执行前仍记录资源快照。不得自动删除未知文件、stash、活跃 worktree、证据或生产数据。

### C01：task event 表和版本分配

**主要产物**

- `agent_task_event` Schema、Initializer、Entity/DTO/DAO/Mapper。
- `current_event_version` 原子分配机制和同事务事件写入入口；`task_version` 保持独立 CAS 语义。
- `agent_task_event.event_version` 唯一约束：scope + task + eventVersion；另有 scope + eventId。

**关键测试**

- 并发写入无重复 `event_version`，且 `current_event_version = MAX(event_version)`。
- 事务回滚不保留状态或事件。
- scope 错误、task 不存在、版本溢出 fail closed；仅 member/work-item 变化不擅自改 `task_version`。
- MySQL 迁移重复执行与 Schema drift 检测。

### C01B：全部业务写路径原子事件接入

**写前冻结包（C01B-0，只读）**

- 补齐 heartbeat、release、thread/message、archive 等 `TaskEventType` 目录缺口。
- 冻结多 aggregate 事件固定顺序、全入口统一 task-root 锁序和事务传播边界。
- 冻结 `event_json` payload allowlist；禁止 lease token、认证头、完整聊天正文等敏感信息。
- 冻结 no-op、ACL 拒绝、CAS 冲突均为 0 event，以及 acceptance -> path -> test -> evidence 矩阵。

**同一 Sol Writer 的微阶段**

```text
C01B-1 event catalog、payload allowlist、统一锁序、测试骨架
C01B-2 B03 状态机 + B04 lease
C01B-3 B05 aggregation + B06 request/artifact/result
C01B-4 B07 thread + B08 legacy/create/assign/report/archive
C01B-5 全入口覆盖、隔离 MySQL、联合回归
```

不得把微阶段拆给多个 Writer；每个阶段只跑 targeted tests，最终候选才由 Flash 独立跑一次模块全量和一次隔离 MySQL。

**必须盘点并覆盖**

- B03 task/member/work-item 状态转换。
- B04 claim/lease/heartbeat/expire/reassign。
- B05 任务聚合状态变化。
- B06 request/artifact 创建和状态变化。
- B07 task-thread 关键协作事实。
- B08 legacy assign/report 兼容入口，以及 task create/assign/archive 等存量入口。

**退出门槛**

- 每条成功业务写入都有规范化 event type、actor、aggregate、payload allowlist。
- 状态写入与 event/version 更新同事务；任一失败全部回滚。
- 无变化、幂等重放、CAS 冲突和权限拒绝不得产生伪事件。
- 建立“业务入口 -> event type -> 测试 -> evidence key”的完整覆盖矩阵。
- 承接 C01 follow-up：隔离 MySQL writer 并发/回滚、真实 Spring `@Transactional` proxy 外层回滚、duplicate event ID 失败后下一次成功 append 无版本洞。

### C01H：B09 历史任务 event baseline

**执行内容**

- 为每个 B09 受影响任务使用确定性 event ID 追加幂等 `HISTORICAL_BASELINE_IMPORTED`。
- 在同一迁移事务内分配下一 `event_version`、插入事件并更新 `current_event_version`；`task_version` 保持不变。
- 冻结维护窗口顺序：停写 -> B09 approved apply -> baseline dry-run/review/approve/apply -> 一致性核验 -> 恢复写入。
- baseline 不伪造历史逐步事件，只表达可审计的“迁移后协作快照基线”。
- 迁移必须可重复执行、可检测漂移、可统计缺失/冲突，并继续遵循 DBA/人工审批边界。

**关键测试**

- B09 未执行、已执行、重复执行、部分漂移和失败回滚。
- member/work-item/current_event_version/baseline event 计数一致。
- 隔离 MySQL 新库、旧库升级和重复迁移。

### C02：TaskEventBroker 和 after-commit 唤醒

**主要产物**

- 按 tenant/client/task 隔离的进程内 Broker。
- `TransactionSynchronization` 或等价 after-commit 钩子，只接收 C01/C01B/C01H 已持久事件。
- C02 不新增业务事件写入；无事务、回滚、嵌套事务、重复唤醒有明确语义。

**关键测试**

- commit 前订阅者不可见。
- rollback 后永不发布。
- commit 后只发布一次。
- 慢订阅者/取消订阅不会阻塞业务事务。

### C03：replay、连续性和 resync

**主要产物**

- 数据库按版本分页 replay；`findAfterVersion` 必须有明确 page size/cursor，禁止一次性无界读取。
- “先 live 后 replay”的桥接算法。
- gap、历史截断、cursor ahead、并发新事件处理。
- `resync_required` 规范及 reason code。

**关键测试**

- 连续历史、重复 live/history、连接窗口新事件。
- replay 分页边界、历史清理、游标超前。
- API 重启后仅靠数据库恢复。
- 内存 Broker 丢失不造成持久事件丢失。

### C04：workspace snapshot API

**接口**

```http
GET /agent/tasks/{taskId}/workspace
```

**返回最小字段**

```text
task, members, workItems, openRequests, recentArtifacts,
conversationId, currentVersion
```

**关键测试**

- 同一 scope 下 snapshot 与 `currentVersion` 一致。
- 跨 tenant/client/task ACL fail closed。
- 空集合、历史任务、已终止成员、分页/截断策略。
- `currentVersion` 以精确十进制字符串输出。

### C05：task events SSE API

**接口**

```http
GET /agent/tasks/{taskId}/events?sinceVersion=123
Last-Event-ID: 123
Accept: text/event-stream
```

**关键测试**

- query/header 游标解析、优先级和非法值。
- SSE `id` 为版本字符串。
- replay 后切 live 无丢失、无重复。
- timeout/cancel 清理订阅。
- ACL、gap、resync_required、API restart。

### C05F：后端 feature flag

- M2 workspace/SSE 默认关闭，按获准 tenant/client 或配置范围开启。
- 关闭状态不暴露半成品实时入口，不影响 M1 旧接口。
- 覆盖默认值、开启、关闭、非法配置和重启后的行为。

### C06：前端事件流和恢复 reducer

**主要产物**

- `useTaskWorkspace()`：单一 workspace 状态。
- `useTaskEventStream()`：连接、重连、replay、降级、visibility 恢复。
- 版本字符串比较工具，禁止 `Number(version)`。

**关键测试**

- 连续事件、重复事件、乱序/gap、resync。
- snapshot 与连接窗口竞态。
- 重连退避、轮询降级、页面恢复。
- task 切换时旧连接和旧请求被正确取消。

### C07A：数据接入和状态集成

- 接入 C04/C06，不自行复制第二套 workspace 状态。
- 明确 loading/live/reconnecting/degraded/resync/error 状态。
- 任务切换、ACL 错误和 snapshot 重载可观察。

### C07B：纯展示 UI

- 展示成员、工作项、诉求、成果、Timeline。
- 不新增业务写 API，不修改 reducer、ACL 或版本算法。
- 若需新视觉资产，先复用现有设计系统；确需图片时由 `gpt-image-2` 生成到 `web/src/assets/juyiting/`。

### C07C：质量收敛

- 响应式布局、键盘操作、语义标签、空状态和长文本处理。
- 组件级测试与 `npm run build`。
- 回归 `/agent/map`、`/agent/roster` 分流和显式目标 Agent 分派。

### C07：前端集成门禁

- 只做子阶段集成、冲突处理、回归和验收，不夹带新特性。
- GPT-5.6 Sol High 可以修复集成冲突，但任何业务语义变化必须回到对应子任务复审。

### C07F：前端 feature flag

- 默认不展示/连接 M2 工作台和 SSE；关闭时继续使用 M1 稳定页面。
- 与 C05F 的 scope/配置语义一致，覆盖动态切换、刷新和降级。

### C08A：API 累计基线门禁

- 在 `/home/isp/wsps/cyf/.worktrees/m2-api-base` 的累计 clean base 上验证所有 accepted API commit。
- Sol integration Writer 只处理集成；任何语义性冲突修复产生独立 commit，并由 Pro Reviewer 审查。
- 迁移、新库/旧库/重复执行、事件原子性、replay/SSE、ACL、flag 和 rollback 全部通过。

### C08W：Web 累计基线门禁

- 在 `/home/isp/wsps/cyf/.worktrees/m2-web-base` 验证所有 accepted Web commit。
- 执行 test/build、版本精度、恢复 reducer、flag、Juyi Hall 回归和资源清理测试。

### C08：M2 部署候选最终门禁

- C08A/C08W 均 accepted，记录两个 base branch、worktree、base SHA 和最终 SHA。
- API 联合测试、Web test/build、SSE 断线恢复 smoke、跨 scope 探针通过。
- Schema 迁移步骤可重跑、可检测漂移；不在本任务执行生产 DML。
- M2 feature flag 默认关闭；明确测试租户开启、烟测、关闭和旧栈回滚步骤。
- 输出 GO/NO-GO、部署步骤、回滚步骤和残余风险。

## 6. Worktree 与分支分配

| 执行包/任务 | Repo | Branch | Worktree |
| --- | --- | --- | --- |
| 累计 API base / AG | api | `feat/m2-api-base-20260803` | `/home/isp/wsps/cyf/.worktrees/m2-api-base` |
| BE1 / C02+C03 | api | `feat/c02-c03-task-event-core` | `/home/isp/wsps/cyf/.worktrees/m2-c02c03-api` |
| BE2 / C04 | api | `feat/c04-task-workspace` | `/home/isp/wsps/cyf/.worktrees/m2-c04-api` |
| BE3 / C05+C05F | api | `feat/c05-c05f-task-event-edge` | `/home/isp/wsps/cyf/.worktrees/m2-c05-api` |
| 累计 Web base / WG | web | `feat/m2-web-base-20260803` | `/home/isp/wsps/cyf/.worktrees/m2-web-base` |
| FE1 / C06+C07A | web | `feat/c06-c07a-task-workspace-state` | `/home/isp/wsps/cyf/.worktrees/m2-c06c07a-web` |
| FE2 / C07B+C07C+C07+C07F | web | `feat/c07bcf-task-workspace-surface` | `/home/isp/wsps/cyf/.worktrees/m2-c07bcf-web` |
| RG / C08 | 控制面 | N/A | `/home/isp/wsps/cyf` |

**创建与集成规则**

- 执行包从对应累计 base 的最新 accepted/integrated HEAD 创建，不从 dirty `develop` 复制。
- 一个执行包只有一个 Writer；包内每个原始任务使用独立 commit、handoff 和验收状态。
- 前一微阶段 ACCEPT 后可在同一 worktree 继续下一微阶段，无需创建新 branch/worktree。
- 执行包最终 accepted 后一次性 byte-exact no-ff merge 到累计 base；核对 parent/source/tree SHA，不重复完整 Review。
- 发生冲突、语义编辑或 tree mismatch，相关证据失效并重新 Review。
- C08A/C08W 默认由 Test Runner 执行只读累计门禁；发现必须修复时可 claim 独立任务 Writer，只有 owned paths 重叠才协调。
- 控制面文档只由主控修改，代码 Writer 不修改 `docs/implementation/**`。

## 7. 标准执行协议

### Runtime ledger / dispatch（唯一入口）

- 当前执行事实只存在于 `TASKS.yaml` 的 `runtime_ledger_json`；历史 `tasks` 和 handoff 不参与调度判断。
- 主控按显式依赖分派；同一 active Agent 不得占两个任务，但不同 ready 任务可在独立 worktree/owned paths 由不同 Writer 并行。
- `owner.mode=support/reviewer` 始终只读，不得调用 Gradle；任一任务的 Writer/Verifier 在本任务 `current_gate` 为 verification 时均可排队获取全局 Gradle 锁。
- accepted evidence 只按 tree SHA + exact selector + fixture digest 复用；任一变化均 MISS 并只重跑相关 selector。
- `ops/orchestration/cyf_orchestrator.py` 是 transition、failure attribution、evidence cache、Gradle 与通知的单一可执行入口。
- `critical_path` 仅表达依赖和晋级顺序，不构成全局 Writer 或 Gradle 准入；绝不授权终止或抢占已经运行的任务；`/tmp/cyf-gradle.lock` 的持有者和等待者都只能由 exact owner 自主管理。
- 跨线程冲突只允许通过 `conflict-alert` 产生 `coordination_required` 告警，不得操作其他任务的进程、Gradle daemon、systemd unit 或证据目录。
- 任何进程控制都必须同时具备 exact thread ownership 与用户/主控显式授权；协调线程本身保持 alert-only，不因获得冲突信息而取得执行权限。

### Prepare（只读并行）

当前执行包 Writer 工作时，主控可提前启动最多三个只读槽位：

1. Explorer：下一任务调用链、依赖、allowed-path 和冲突地图。
2. Fast Query：acceptance -> path -> test selector -> evidence 矩阵。
3. Test Runner preparation：只读整理测试命令、selector、fixture digest 与已有 evidence key；未切到 verifier owner/gate 前不得启动 Gradle、隔离数据库或重型资源探针。

准备成果只能由主控写入 handoff/preflight；只读 Agent 不得 claim、修改源码或改变冻结契约。

### Claim

主控只通过统一入口更新 `TASKS.yaml#runtime_ledger_json`；`planned_*` 和历史 `tasks` 不是 claim：

```text
owner={agent, profile, mode}
exact_sha_tree={commit_sha, tree_sha}
current_gate=claimed|implementing|targeted_verification|verifying|review|blocked_*|accepted
blocker=null|{category, summary, consecutive_failures, attempts}
next_action=<one executable action>
```

Claim 前必须确认显式依赖、独立 worktree、任务级唯一 Owner、路径所有权和证据缓存；资源快照仅作观测，不再因固定内存/磁盘阈值拒绝重型验证。`blocked_root_cause` 不允许普通 claim/transition，必须先冻结根因矩阵并通过 `authorize-remediation --matrix-ref ...` 显式开启有界整改。

### Implement

Writer 必须：

1. 阅读任务卡、直接依赖 handoff、只读准备包和最近 build.gradle/package.json。
2. 写前冻结契约/锁序/验收矩阵；只修改 allowed paths，不回滚他人修改。
3. 先加失败测试，再实现；每个微阶段只运行 targeted/touched suites。需要登记可复用 evidence 时，先形成 clean commit/tree，再从该 exact worktree 运行。
4. Gradle 只能经 `python3 ops/orchestration/cyf_orchestrator.py gradle <task>` 运行；入口校验任务 owner/current_gate、clean worktree exact commit/tree、证据缓存、磁盘和 `/tmp/cyf-gradle.lock`；不再要求任务位于 critical-path 首项。
5. commit message 带任务 ID；handoff 记录 tree SHA 和 evidence key。
6. 不部署、不重启生产、不执行生产 DML；提交到 `review` 后停止，不能自行 accepted。

### Verify / Review

- 最终 candidate 由当前可用 Test Runner 独立运行一次模块全量；事务/迁移 tree 运行一次隔离 MySQL。
- 证据键固定为 `git tree SHA + test selector + DB fixture digest`；tree、selector、fixture 未变化时复用证据。
- Reviewer 只读检查 acceptance、diff、代码和证据，不运行 Gradle；证据无效或覆盖缺口时，退回主控并由独立 verifier 在新 gate 补跑。
- Reviewer 输出 `ACCEPT`/`REJECT` 和 P0/P1/P2；REJECT 后仍由原 Writer 在同一 worktree 修复。
- ACCEPT 后主控自动更新账本并推进包内下一微阶段或下一执行包；无需等待逐项用户确认，但必须主动汇报。

### Integrate

- 包内微阶段 accepted 后继续在同一 source worktree；执行包全部 accepted 后再合入对应 `feat/m2-*-base-20260803`，不触碰 dirty develop。
- 无冲突、无语义修改且 source/integration tree byte-exact：只核对 parent/source/tree SHA，不重复完整代码 Review。
- 有冲突、语义修改、tree mismatch 或 evidence 失效：必须重新 Review/验证。
- C08 GO 后才建立 base -> develop 的独立合流任务；本计划不自动部署或执行生产迁移。

## 8. 防重复、防漏实施机制

| 风险 | 控制措施 |
| --- | --- |
| 两个 Agent 重复写同一功能 | `TASKS.yaml` 每任务唯一实际 Owner + 独立 worktree/path ownership；只读 Agent 不得改源码 |
| 接口由前后端分别猜测 | C04/C05 accepted 后冻结 contract，C06 只消费冻结接口 |
| Writer 声称完成但缺测试 | handoff 必填 commit/tree SHA、changed_files、evidence key、commands/results、residual_risks |
| Reviewer 顺手修代码造成责任不清 | Reviewer read-only；REJECT 后原 Writer 修复 |
| 重复跑全量测试拖慢周期 | targeted 开发验证 + 最终 tree 一次全量/一次隔离 MySQL + evidence key 复用 |
| byte-exact 集成重复审查 | 只核对 parent/source/tree SHA；冲突、语义修改或 tree mismatch 才复审 |
| 子任务完成但主任务漏集成 | C07、C08A、C08W 和 C08 显式作为分层集成门禁 |
| task_version 与事件游标混用 | ADR-006 明确 task_version=aggregate CAS，event_version/current_event_version=SSE 游标 |
| Java Long 前端精度丢失 | contract 要求 event version 字符串；C04/C05/C06/C08W 均有精度验收 |
| 业务状态变化没有对应事件 | C01B 建立 B03～B08 全入口覆盖矩阵和同事务回滚测试 |
| B09 历史协作数据无时间线基线 | C01H 独立幂等 baseline 迁移和维护窗口顺序 |
| SSE 漏事件但普通测试通过 | C03/C05/C06/C08A/C08W 均执行连接窗口、gap、重启和重复事件故障注入 |
| 脏主树污染 M2 | M2-00 checksum/stash manifest + 独立累计 base；M2 全程不触碰 develop worktree |
| RabbitMQ 与 SSE 重复建设事实源 | ADR-003：M2 数据库 replay；M3 RabbitMQ 仅运输命令 |
| UI 任务越权修改状态机 | C07B/C07C allowed paths/acceptance 明确禁止改 reducer、ACL 和 API 语义 |

## 9. 验证命令基线

### API

以下命令只作为最终候选/累计门禁基线。开发阶段先跑 task card 指定的 targeted tests；`<task/tree/selector/fixture>` 必须与唯一运行台账和 evidence key 完全一致：

```bash
python3 ops/orchestration/cyf_orchestrator.py gradle <task> \
  --heavy --tree-sha <40-char-tree> \
  --selector 'agent-core+mapper+service module gate' \
  --fixture-digest <digest-or-N/A> -- \
  ./gradlew :agent:jia-agent-core:test \
  :agent:jia-agent-mapper:test :agent:jia-agent-service:test \
  --no-daemon --max-workers=1
```

涉及 chat 再使用一个独立 exact selector/evidence key：

```bash
python3 ops/orchestration/cyf_orchestrator.py gradle <task> \
  --heavy --tree-sha <40-char-tree> \
  --selector 'chat-service module gate' --fixture-digest <digest-or-N/A> -- \
  ./gradlew :chat:jia-chat-service:test --no-daemon --max-workers=1
```

### Web

开发阶段运行受影响测试；最终 Web candidate 由 Test Runner 运行一次：

```bash
cd web && npm run test
cd web && npm run build
```

证据键为 `git tree SHA + test selector + DB fixture digest`。C08A/C08W 承担累计全量回归；普通 Reviewer 默认复用有效证据。

### 必须有的故障注入

- 状态已写但事务回滚。
- commit 与 Broker 发布边界。
- live 订阅与 replay 之间写入新事件。
- replay 分页边界和历史缺口。
- SSE 重连、重复事件、乱序事件、API 重启。
- task 切换和页面 visibility 恢复。
- 跨 tenant/client/task 读取尝试。

## 10. 风险清单与处置

| 风险 | 等级 | 处置 |
| --- | --- | --- |
| API 主工作树大量未提交修改被覆盖 | P0 | M2-00 建 checksum manifest；按对象 SHA 冻结 stash；只从 commit 创建 worktree；禁止 reset/clean |
| event version 分配出现并发重复或死锁 | P0 | C01 原子更新 current_event_version 并插入 event_version；并发 MySQL 测试；Sol Review |
| task_version 与 event_version 混用 | P0 | ADR-006/C01 contract；snapshot/SSE 只用 event version，aggregate CAS 只用 task_version |
| B03～B08 只有状态、没有持久事件 | P0 | C01B 全入口清单、同事务写入和失败回滚测试 |
| B09 回填后 current_event_version 无定义 | P0 | C01H baseline 迁移、精确顺序、计数和幂等验证 |
| after-commit 误在 rollback 发布 | P0 | C02 事务故障注入；无事务语义 fail closed |
| snapshot 与 currentVersion 不一致 | P0 | C04 明确事务/读取边界；并发写快照测试 |
| subscribe/replay 窗口丢事件 | P0 | C03 先 live 后 replay；去重、连续性检查、gap resync |
| SSE 跨租户泄露 | P0 | C05 scope ACL 测试；不存在性侧信道审查 |
| Java Long 在 JS 丢精度 | P0 | 全链路字符串；大于 `2^53` 的 contract/reducer 测试 |
| 慢 SSE 客户端拖垮服务 | P1 | 有界缓冲/断开策略、超时和资源清理测试 |
| 前端无限重连造成请求风暴 | P1 | 指数退避、抖动、失败阈值和轮询降级 |
| Flash/Luna/Terra 越界改架构 | P1 | 只接冻结契约任务；P0 语义升级给 Sol critical_worker；跨模型只读 Review |
| B09 尚未生产执行影响历史任务 | P1 | M2 不隐式回填；snapshot 对缺失历史数据 fail closed/显式降级 |
| 磁盘不足导致构建/集成中断 | P0 | 固定空间阈值不再阻断；保留资源快照、串行执行和 ENOSPC 根因归档，禁止自动删除未知数据 |
| gpt-image-2 资产拖慢主线 | P2 | 默认不使用；仅 C07B 可选且必须经过 build 引用验证 |

## 11. 汇报策略

- 原始任务 ID 仍在 `TASKS.yaml`、handoff 和 evidence 中逐项记录，但不逐项打扰用户。
- 主控只更新 `TASKS.yaml` 内嵌 `runtime_ledger_json`；每项仅保留 `owner`、`exact_sha_tree`、`current_gate`、`blocker`、`next_action`。
- 任务 ACCEPT 后自动推进；任务完成、验证/Review 异常、连续失败两次或需要用户动作时主动通知，并附一条可执行下一步。
- 资源/Writer 冲突只主动发送 `coordination_required`，不得将 stale ledger、critical-path 顺序或 Gradle 锁等待解释为跨线程终止授权。
- 每次失败先用统一入口登记 evidence/root cause/remediation；连续第二次失败转 `blocked_root_cause` 并输出根因矩阵；普通 claim/transition 被拒绝，必须用 `authorize-remediation` 绑定批准后的矩阵才能开启下一轮。
- 内部进度继续按既有权重计算，不以“已开始”计入完成度。

## 12. 当前状态与下一项

- 已完成并集成：M2-00、C01、C01B、C01H。
- 当前累计 API base：`71e243df4d06e787c3aa6cdbf0f3bc243a6f56a2`，tree `1e0b78183719d55402b1854f3942bc6eaebe5ca8`，worktree clean。
- 当前累计 Web base：`2424f51f375814f403ca70a9a6e9948728e595b1`，worktree clean。
- C02 的架构/事实 preflight 已完成；RabbitMQ 明确不进入 C02。
- 当前执行 OpenAI-only 路由，BE1 直接路由到 `critical_worker / GPT-5.6 Sol High`，不等待或探测 DeepSeek。
- 根分区空间仅作为观测记录，不作为 admission gate；所有 Gradle/DB/npm 重型验证仍串行。
- 下一步：创建 BE1 worktree `m2-c02c03-api`，先实施 C02；C02 独立 Review ACCEPT 后同一 Writer 继续 C03。
- C04 claim 前必须冻结两个契约：浏览器访问 TaskWorkspace 的 ACL subject；Timeline 使用 bounded `recentEvents` 还是仅会话后事件。当前推荐 `recentEvents` 有界连续后缀。
- 未推送、未合 dirty `develop`、未部署、未执行生产迁移。
