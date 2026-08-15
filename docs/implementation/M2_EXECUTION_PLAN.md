# M2 可恢复实时协作执行计划

> 版本：1.0（独立 release_guard 第三轮复核：PLAN-GO）  
> 冻结日期：2026-08-03  
> 范围：M2 持久任务事件、workspace snapshot、SSE replay/resync、前端 TaskWorkspace/Timeline  
> 设计依据：`docs/juyiting-multi-agent-collaboration-design.md` 第 7.5、13、21、22 节  
> 任务账本：`docs/implementation/TASKS.yaml`  
> 模型路由：`docs/implementation/MODEL_ROUTING.yaml`

## 1. 执行结论

M2 采用**数据库优先、严格串行、一个 worktree 一个 Writer、跨模型只读 Review**的执行方式：

```text
M2-00
  -> C01 -> C01B -> C01H -> C02 -> C03 -> C04 -> C05 -> C05F -> C06
  -> C07A -> C07B -> C07C -> C07 -> C07F -> C08A -> C08W -> C08
```

- `deepseek-v4-pro high`：负责 C01、C01B、C01H、C02～C07A，以及 C05F/C07F 的核心实现。
- `deepseek-v4-flash medium`：以只读 Test Runner 执行核心任务验证；只在 C07B/C 作为 Writer 负责纯展示工作。
- 主控 `gpt-5.6-sol high` 负责 M2-00 控制面、架构冻结和进度账本；独立 Sol Reviewer 审查 DeepSeek Pro；独立 Sol integration Writer 负责 C07/C08A/C08W。
- `deepseek-v4-pro high` Reviewer：审查 Flash 编写的 C07B/C，并交叉审查 Sol 执行的 C07/C08A/C08W 及控制面证据；不审查自己编写的核心任务。
- `gpt-image-2`：只在 C07 确有插画、空状态图、视觉稿或图片识别需求时使用，不进入关键路径；架构图优先 Mermaid。

不允许 Flash 独立承担事务、ACL、版本分配、snapshot 一致性、SSE 竞态或 reducer 状态机设计。核心任务的测试代码也由同一 Pro Writer 提交；Flash 只读运行测试和故障探针，避免同一任务出现第二个 Writer。

## 2. 为什么这是当前最优分配

| 决策 | 依据 | 避免的风险 |
| --- | --- | --- |
| 核心链路交给 DeepSeek V4 Pro High | C01～C06 涉及迁移、事务、CAS、连续版本、subscribe/replay 竞态、ACL、断线恢复 | 低成本模型局部实现正确但系统语义不闭环 |
| Pro Writer 由 GPT-5.6 Sol High Review | 写审模型不同，Reviewer 不继承 Writer 结论 | 自审盲区、事务边界和恢复算法遗漏 |
| Flash 只做机械任务和纯展示 UI | 任务边界可验证、失败影响有限 | Flash 擅自决定架构或放宽安全规则 |
| 串行 Writer | C01～C06 强依赖，API 主工作树当前有大量未提交修改 | 重复实现、接口漂移、worktree 冲突和 Gradle 内存竞争 |
| MySQL 为唯一事实源 | 已冻结 ADR-003；内存 Broker 只做本实例唤醒 | API 重启后事件丢失、RabbitMQ 被误当业务事实源 |
| RabbitMQ 不进入 M2 关键路径 | RabbitMQ 可靠命令传输属于 M3/D01～D09 | M2 被消息中间件拓扑拖慢，恢复语义重复建设 |

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

| 顺序 | ID | 交付目标 | Writer | Support / Test | Reviewer | 预估 |
| ---: | --- | --- | --- | --- | --- | ---: |
| 0 | M2-00 | 控制面、脏树、stash、累计 clean base、资源证据 | 主控 GPT-5.6 Sol High | Explorer / Flash Test Runner（只读） | DeepSeek V4 Pro High | 0.5～1 日 |
| 1 | C01 | event Schema、Entity/DAO、event_version 分配 | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 2 日 |
| 2 | C01B | B03～B08 全部业务写路径原子产生 event | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 3 日 |
| 3 | C01H | B09 历史任务 event baseline 幂等迁移 | DeepSeek V4 Pro High | Flash Test Runner / 隔离 MySQL | GPT-5.6 Sol High | 2 日 |
| 4 | C02 | TaskEventBroker 和 after-commit 唤醒 | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 2 日 |
| 5 | C03 | replay、连续性检查、gap/resync | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 3 日 |
| 6 | C04 | 一致版本 workspace snapshot API | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 2～2.5 日 |
| 7 | C05 | task event SSE API、Last-Event-ID、ACL | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 2 日 |
| 8 | C05F | 后端 M2 feature flag 默认关闭 | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 0.5 日 |
| 9 | C06 | useTaskWorkspace/useTaskEventStream、恢复 reducer | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 3 日 |
| 10 | C07A | TaskWorkspace 数据接入、状态和恢复提示 | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 1～1.5 日 |
| 11 | C07B | 成员/工作项/诉求/成果/Timeline 纯展示 UI | DeepSeek V4 Flash Medium | — | DeepSeek V4 Pro High | 1～1.5 日 |
| 12 | C07C | 响应式、可访问性、组件测试、build | DeepSeek V4 Flash Medium | — | DeepSeek V4 Pro High | 1 日 |
| 13 | C07 | 前端子阶段集成和 Juyi Hall 回归 | 独立 GPT-5.6 Sol High | Flash Test Runner | DeepSeek V4 Pro High；Sol release_guard 终审 | 0.5 日 |
| 14 | C07F | 前端 M2 feature flag 与 M1 安全降级 | DeepSeek V4 Pro High | Flash Test Runner | GPT-5.6 Sol High | 0.5 日 |
| 15 | C08A | API 累计基线联合回归 | 独立 GPT-5.6 Sol High | Flash Test Runner | DeepSeek V4 Pro High | 0.75 日 |
| 16 | C08W | Web 累计基线 test/build/回归 | 独立 GPT-5.6 Sol High | Flash Test Runner | DeepSeek V4 Pro High | 0.75 日 |
| 17 | C08 | 双仓部署候选最终 GO/NO-GO | 主控 GPT-5.6 Sol High | Flash Test Runner | DeepSeek V4 Pro High；独立 Sol release_guard 最终门禁 | 0.5 日 |

> 任务估算沿用“人日复杂度”，不是模型运行时承诺。严格串行且含 Review/返工时，目标机器执行周期为 12～18 个执行日；遇到多轮驳回、MySQL 环境或资源阻塞时顺延。

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
10. 资源门禁：开始 Gradle、npm 全量构建或创建集成 worktree 前，根分区可用空间必须至少 5 GiB；记录 inode、内存和 swap。2026-08-03 复核时仅约 3.0 GiB，当前不满足该门禁。
11. 在 M2-00 handoff 生成控制面 SHA-256 清单，并将摘要写入 C01 首个 Git commit trailer，弥补仓库根目录不是 Git repo 的追踪缺口。

**退出门槛**

- 基线 SHA、两个累计 base branch/worktree、dirty checksum、stash object SHA、M1 双状态、资源门禁和测试证据写入 handoff。
- 所有用户未提交修改仍原样存在。
- 若协议日志异常存在，已有独立任务 ID、Owner 和验收条件。
- 可用空间达到至少 5 GiB 后才能退出 M2-00；不得通过删除未知文件、stash 或 worktree 绕过。

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
- 建立“业务入口 -> event type -> 测试”的完整覆盖矩阵。

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

- 数据库按版本分页 replay。
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

| 任务 | Repo | Branch | Worktree |
| --- | --- | --- | --- |
| M2-00 | 控制面证据 | N/A（根目录非 Git repo） | `/home/isp/wsps/cyf` |
| 累计 API base | api | `feat/m2-api-base-20260803` | `/home/isp/wsps/cyf/.worktrees/m2-api-base` |
| C01 | api | `feat/c01-task-event-schema` | `/home/isp/wsps/cyf/.worktrees/m2-c01-api` |
| C01B | api | `feat/c01b-task-event-mutations` | `/home/isp/wsps/cyf/.worktrees/m2-c01b-api` |
| C01H | api | `feat/c01h-historical-event-baseline` | `/home/isp/wsps/cyf/.worktrees/m2-c01h-api` |
| C02 | api | `feat/c02-task-event-broker` | `/home/isp/wsps/cyf/.worktrees/m2-c02-api` |
| C03 | api | `feat/c03-task-event-replay` | `/home/isp/wsps/cyf/.worktrees/m2-c03-api` |
| C04 | api | `feat/c04-task-workspace` | `/home/isp/wsps/cyf/.worktrees/m2-c04-api` |
| C05 | api | `feat/c05-task-event-sse` | `/home/isp/wsps/cyf/.worktrees/m2-c05-api` |
| C05F | api | `feat/c05f-m2-backend-flag` | `/home/isp/wsps/cyf/.worktrees/m2-c05f-api` |
| 累计 Web base | web | `feat/m2-web-base-20260803` | `/home/isp/wsps/cyf/.worktrees/m2-web-base` |
| C06 | web | `feat/c06-task-event-stream` | `/home/isp/wsps/cyf/.worktrees/m2-c06-web` |
| C07A | web | `feat/c07a-task-workspace-state` | `/home/isp/wsps/cyf/.worktrees/m2-c07a-web` |
| C07B | web | `feat/c07b-task-workspace-ui` | `/home/isp/wsps/cyf/.worktrees/m2-c07b-web` |
| C07C | web | `feat/c07c-task-workspace-quality` | `/home/isp/wsps/cyf/.worktrees/m2-c07c-web` |
| C07 | web | `feat/c07-task-workspace-integration` | `/home/isp/wsps/cyf/.worktrees/m2-c07-web` |
| C07F | web | `feat/c07f-m2-frontend-flag` | `/home/isp/wsps/cyf/.worktrees/m2-c07f-web` |
| C08A | api | `feat/m2-api-base-20260803` | `/home/isp/wsps/cyf/.worktrees/m2-api-base` |
| C08W | web | `feat/m2-web-base-20260803` | `/home/isp/wsps/cyf/.worktrees/m2-web-base` |
| C08 | 控制面证据 | N/A | `/home/isp/wsps/cyf` |

**创建规则**

- M2-00 从精确 commit `c49d148...`、`2424f51...` 创建两个累计 base；不 checkout/switch 当前脏 `develop`。
- 任务 worktree 从对应累计 base 的最新 HEAD 创建，绝不从当前脏 `api/` 文件系统复制。
- accepted 后由独立 Sol integration Writer 将 commit 合入累计 base；Pro Reviewer 审查 merge/conflict commit。下一任务再从更新后的累计 base 创建。
- 每个 worktree 只有一个 Writer；Reviewer 直接读取 diff 和测试证据，不修改该树。
- 控制面文档由主控更新，避免代码 Writer 在错误 repo 中修改任务账本。

## 7. 标准执行协议

### Claim

主控在 `TASKS.yaml` 原子写入：

```text
status=claimed
owner=<agent + model>
reviewer=<independent agent + model>
claimed_at / lease_until
branch / worktree
allowed_paths
```

### Implement

Writer 必须：

1. 阅读任务卡、直接依赖 handoff 和最近 build.gradle/package.json。
2. 只修改 allowed paths；不得回滚他人修改。
3. 先加失败测试，再实现，再运行最小验证。
4. Gradle 命令必须持有 `/tmp/cyf-gradle.lock`，单 worker、低内存。
5. commit message 带任务 ID；不得部署、重启生产或执行生产 DML。
6. 提交 handoff 后把状态推进到 `review`，不能自行 accepted。

### Review

Reviewer 必须：

- 只读检查任务卡、完整 diff、代码、测试和故障注入证据。
- 输出 `ACCEPT` 或 `REJECT`，标注 P0/P1/P2、精确路径/行号及复现命令。
- 不直接修代码；驳回后由原 Writer 在同一任务/worktree 修复。

### Integrate

- accepted 后由独立 integration Writer 合入对应 `feat/m2-*-base-20260803`，不触碰当前脏 `develop`。
- Pro Reviewer 审查累计 base 的集成 commit；通过后状态从 `accepted -> integrated`。
- C08 最终 GO 后才制定 base -> develop 的独立合流任务；本计划不自动操作脏 develop。
- 集成失败不得绕过测试；回到原任务修复并重新 Review。

## 8. 防重复、防漏实施机制

| 风险 | 控制措施 |
| --- | --- |
| 两个 Agent 重复写同一功能 | `TASKS.yaml` 唯一 Owner + 串行 active task + 一个 worktree 一个 Writer |
| 接口由前后端分别猜测 | C04/C05 accepted 后冻结 contract，C06 只消费冻结接口 |
| Writer 声称完成但缺测试 | handoff 必填 commit、changed_files、commands、results、residual_risks |
| Reviewer 顺手修代码造成责任不清 | Reviewer read-only；REJECT 后原 Writer 修复 |
| 子任务完成但主任务漏集成 | C07、C08A、C08W 和 C08 显式作为分层集成门禁 |
| task_version 与事件游标混用 | ADR-006 明确 task_version=aggregate CAS，event_version/current_event_version=SSE 游标 |
| Java Long 前端精度丢失 | contract 要求 event version 字符串；C04/C05/C06/C08W 均有精度验收 |
| 业务状态变化没有对应事件 | C01B 建立 B03～B08 全入口覆盖矩阵和同事务回滚测试 |
| B09 历史协作数据无时间线基线 | C01H 独立幂等 baseline 迁移和维护窗口顺序 |
| SSE 漏事件但普通测试通过 | C03/C05/C06/C08A/C08W 均执行连接窗口、gap、重启和重复事件故障注入 |
| 脏主树污染 M2 | M2-00 checksum/stash manifest + 独立累计 base；M2 全程不触碰 develop worktree |
| RabbitMQ 与 SSE 重复建设事实源 | ADR-003：M2 数据库 replay；M3 RabbitMQ 仅运输命令 |
| UI 任务越权修改状态机 | C07B/C allowed paths/acceptance 明确禁止改 reducer、ACL 和 API 语义 |

## 9. 验证命令基线

### API

实际模块以任务变更为准，所有 Gradle 命令必须串行持锁：

```bash
flock /tmp/cyf-gradle.lock ./gradlew \
  :agent:jia-agent-core:test \
  :agent:jia-agent-mapper:test \
  :agent:jia-agent-service:test \
  --no-daemon --max-workers=1
```

涉及 chat 再追加：

```bash
flock /tmp/cyf-gradle.lock ./gradlew \
  :chat:jia-chat-service:test \
  --no-daemon --max-workers=1
```

### Web

```bash
cd web && npm run test
cd web && npm run build
```

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
| Flash 越界改架构 | P1 | profile 明确升级条件；Pro/Sol 只读 Review |
| B09 尚未生产执行影响历史任务 | P1 | M2 不隐式回填；snapshot 对缺失历史数据 fail closed/显式降级 |
| 磁盘不足导致构建/集成中断 | P0 | M2-00 要求至少 5 GiB；2026-08-03 当前约 3.0 GiB，未达门禁 |
| gpt-image-2 资产拖慢主线 | P2 | 默认不使用；仅 C07B 可选且必须经过 build 引用验证 |

## 11. 里程碑与主动汇报点

每完成一项，主控必须主动向用户汇报一次，不等待追问，固定格式：

```text
[任务 ID] 状态：ACCEPT / REJECT / BLOCKED
完成：<具体交付>
证据：<commit + tests>
风险：<剩余风险>
下一项：<ID + Writer + Reviewer>
M2 总进度：<按验收权重计算百分比>
```

进度只按 accepted 权重计算，不按“已开始”计入：

| 任务 | 权重 |
| --- | ---: |
| M2-00 | 5% |
| C01 | 5% |
| C01B | 8% |
| C01H | 6% |
| C02 | 7% |
| C03 | 11% |
| C04 | 9% |
| C05 | 8% |
| C05F | 3% |
| C06 | 10% |
| C07A | 5% |
| C07B | 4% |
| C07C | 4% |
| C07 | 3% |
| C07F | 3% |
| C08A | 4% |
| C08W | 3% |
| C08 | 2% |

## 12. 启动条件与第一项

第一项固定为 **M2-00**。在其 ACCEPT 前，不创建 C01 写入 worktree，不修改 API/Web 业务代码。当前已知阻塞是 2026-08-03 根分区仅约 3.0 GiB 可用，需安全释放到至少 5 GiB。

M2-00 完成并创建累计 clean base 后，C01 由 `deepseek_pro_worker` 领取，`sol_reviewer` 独立审查；测试探针由 Flash `test_runner` 只读执行，不成为第二个 Writer。
