# 多 Agent 协作实施决策记录

本文件记录已经冻结、会影响多个任务的架构决定。模型不得仅凭聊天内容改变这些决定。

## ADR 模板

```text
## ADR-XXX：标题

- 状态：proposed / accepted / superseded
- 日期：YYYY-MM-DD
- 决策人：
- 关联任务：

### 背景

### 决策

### 影响

### 被否决方案

### 验证方式
```

---

## ADR-001：稳定 Agent 身份模型

- 状态：accepted（首轮 rejected，第二轮 ACCEPT）
- 日期：2026-07-22
- 决策人：A01 Owner `main-gpt-5.6-sol`
- Reviewer：`Lagrange (019f8a43-2c6b-7ee3-8e49-838e46fd56aa)`
- 关联任务：A01、A02、A03、A04、B01、B09
- 详细规范：`docs/implementation/agent-identity-v1.md`

### 背景

现有系统同时存在短 persona ID、`jyt-{clientId}-{personaCode}` 拼接 ID、系统 ID 和 scope 缺失的历史 runtime。部分 ID 字面前缀与真实 client/owner 不一致，任务也存在短 ID 引用；runtime 还可能被重建或清理，因此 ID 字符串和 runtime 都不能单独承担身份事实与授权语义。

### 决策

- 新 Agent ID 只使用 `^agt_[0-9a-f]{32}$`；canonical 集合还包括 registry 显式冻结的 legacy-canonical 和系统特例 `builtin-songjiang`。
- 不通过 ID 前缀或分段推断权限、owner、client 或 persona。
- immutable owner scope 定义为 `(client_id, owner_jiacn)`；协作表中 `tenant_id = owner_jiacn`，两者必须一致；v1 不支持 owner 转移。
- active persona 唯一范围为 `(client_id, owner_jiacn, persona_code)`，允许同一 client 下不同 owner 各自使用相同 persona。
- `agent_persona_binding` 与 A02 建立的 identity registry/alias 是持久身份事实源；binding 历史不可物理删除，agentId 永不复用；runtime 只是可重建在线投影。
- `runtimeInstanceId` 每次客户端进程启动生成一次，进程内 WS 重连保持；`webSocketSessionId` 每次连接生成，断线失效；二者都不能作为业务外键或 ownership 依据。
- 生命周期固定为 `PROVISIONED / ACTIVE / SUSPENDED / RETIRED`：unbind 进入 SUSPENDED，restore 仅限原 owner 显式恢复，RETIRED 为终态。
- 在线兼容 alias 只允许 `legacy_agent_id`；personaCode、profileId、displayName 只能作为迁移证据。
- A02 扩大负责 identity registry/alias Schema、Initializer、约束测试、dry-run 和迁移说明；B01 不负责身份 alias Schema。

### 影响

- A02 估算调整为 3.5 人日，并必须解决 active alias 与 active persona 的可靠唯一约束。
- A03 必须在协议中显式区分 stable agentId、runtimeInstanceId 和 WebSocket session。
- A04 的 WS 授权必须查询持久身份事实源，不能只依赖 runtime 或 ID 前缀。
- B01 协作表使用 canonical agentId 和显式 tenant/client scope，但不创建 identity registry/alias。
- B09 只能消费 A02 已确认映射，不能按 persona/displayName 猜测回填。

### 被否决方案

- 继续使用 personaCode 或 displayName 作为在线身份：跨 owner 冲突且可变。
- 继续拼接 client/persona：泄露业务语义，历史错误前缀会导致身份漂移或越权。
- 把 runtime 或 WebSocket session 当身份事实源：可删除、可重建且生命周期过短。
- unbind 直接 retired：无法安全表达同 owner 暂停后恢复。
- 用 nullable `valid_to` 普通唯一键限制 active alias：MySQL 对 NULL 的唯一语义不能可靠保证单 active 记录。
- 立即全库改写 ID：当前历史引用和 scope 数据不完整，风险过高。

### 验证方式

- 只读盘点 runtime、binding 和 task 引用，确认短 ID、scope 缺失和错误前缀样本。
- Reviewer 独立核对 canonical 集合、owner scope、事实源、生命周期及 alias 阻断规则。
- A02 后续以 Schema 测试和 dry-run 证明 active 唯一性与映射唯一性；冲突项必须人工确认。

## ADR-002：Agent Protocol v1

- 状态：accepted（两轮返工，第三轮 Review ACCEPT）
- 日期：2026-07-22
- 决策人：A03 Owner `Poincare (019f8a40-62f3-71b2-a298-4c99f318a494)`
- Reviewer：`Feynman (019f8a70-35bf-78f3-806e-1273739018aa)`
- 关联任务：A03、A04～A06、B08、D05～D07
- 实现 commits：`d79b5a32e5635531c721382a59a02aa4048ea3fc`、`8a19fc02d7b55af3190e7615cd028567b981ff31`、`99e225db16e082ca4abc39fc73f48ce9f4433369`

### 决策

1. Protocol v1 使用精确整数 `schemaVersion=1` 和小写点分 canonical `messageType`。
2. v1 基础类型包括 `protocol.hello`、`protocol.error`、`agent.register`、`agent.presence`、`chat.message`、`chat.message.delta`、`command.dispatch`、`command.ack`、`work.progress`、`work.heartbeat`、`work.result`、`help.request`、`artifact.publish`、`task.event`。
4. 只有 `command.dispatch` 是执行触发消息；`task.event` 仅描述事实，`chat.message` 不得隐式转为 command/result。
5. v1 canonical 类型必须显式携带 schemaVersion；溢出、小数、字符串、缺失和未知版本全部 fail closed。
6. outer 与 nested payload 的保留 Envelope 字段、字段别名或消息语义冲突时必须拒绝。显式 null、非字符串或空白的 type/messageType 也必须拒绝，不能从另一层补值。
7. `agentId/sourceAgentId/targetAgentId` 是 ADR-001 canonical 身份；`runtimeInstanceId` 是进程实例。v1 在认证或首次注册边界必须提供并固定 runtime，禁止延迟绑定、session 内切换或与认证值冲突。
8. `command.dispatch` 必须携带 `messageId`、`commandId`、`commandType` 和 `targetAgentId`。`messageId/requestId` 作为兼容别名时必须一致。
9. 兼容期可保留旧 transport 外壳，但 `agent_direct_message` 只允许明确的 chat/command；旧客户端已知的 `task_assigned/task_event/task.assign/codex.exec` 不得作为服务端执行下行外壳。
9. legacy `task.report` 只进入兼容 adapter；canonical work result 不调用旧任务级 report。A04/A05/A06/B08 分别负责 scope 隔离、客户端队列、ACK 幂等和多人聚合。
10. WebSocket send 成功只表示服务端已尝试发送，不表示 Agent 已接收或执行。

### 兼容策略

- 普通聊天暂时可保留 `agent_direct_message` 外壳，但必须携带 `messageType=chat.message`；A05 必须按 messageType 分流并停止聊天 task.report。
- legacy `agent.action` 归一化为 `command.dispatch`；legacy `task_event` 归一化为 `task.event`；legacy `task.report` 标记为 legacy result adapter。
- `codex.result` 可识别为 legacy result，但不得自动调用旧 report handler。
- 未实现的 canonical handler返回明确协议错误，禁止回退到 chat、command 或 legacy report 路径。

### 影响

- A04 使用 canonical target/scope 字段实现精准投递。
- A05 只把 `command.dispatch` 放入客户端持久执行队列；chat/event 不执行任务。
- A06 以 commandId 实现 ACK 与幂等，不使用 runtime/session 作为业务键。
- B08 将 legacy task.report 转为成员/工作项状态后再聚合。
- RabbitMQ/Outbox/Inbox 复用同一 Envelope，不另建第二套消息语义。

### 验证方式

- Normalizer 覆盖 schema 溢出/小数/缺失、outer/nested 冲突、alias 冲突和非法类型字段。
- Handler 覆盖唯一执行入口、不可执行下行、runtime 注册固定与切换拒绝。
- Agent service/chat service 全模块测试通过，并经过独立 Reviewer 三轮核验。

### 2026-07-23 兼容修正

- 修复实际 command 下行路径的 `messageId/requestId` 不一致，以及 chat 下行路径的 `sentAt/timestamp` 不一致。
- 生产修复集成 commit：`f1f43a8`；最终 WebSocket JSON 链路测试集成 commit：`b343e2c`。
- `commandId` 继续承载 intent 语义；Normalizer 的 fail-closed 规则未放宽。

## ADR-003：任务协作事实源

- 状态：accepted
- 日期：2026-07-22
- 决策人：架构方案基线
- 关联任务：B01～B09、C01～C07、D01～D09

### 决策

MySQL 是任务状态、成员、工作项、事件、成果和投递状态的唯一事实源。RabbitMQ 是命令运输层；Redis 是在线状态和短期协调；Elasticsearch 是可重建的派生索引。

### 影响

- RabbitMQ 消息不能作为任务完成依据。
- 内存 mailbox 不再承担可靠离线存储。
- 所有可恢复状态必须先落数据库。


## ADR-004：codex-ws-agent 版本化事实源

- 状态：accepted
- 日期：2026-07-22
- 决策人：主控 Agent
- 关联任务：A05～A07

### 决策

- `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/` 是客户端代码、配置模板和 README 的版本化事实源。
- `/home/isp/apps/codex-ws-agent/` 是当前机器的运行部署副本，不作为开发分支或 Review 事实源。
- A05/A06/A07 必须在 `isp-install` 独立 branch/worktree 开发、测试和 Review；accepted 后由主控同步到运行目录并执行 smoke。
- `/home/isp/wsps/cyf/deliverables/**` 是打包产物，不允许直接修改；后续由正式打包流程从版本化源生成。
- `docs/agent-client.mjs` 是历史文档快照，不再作为代码事实源；协议文档需单独同步。

### 验证方式

- 当前运行文件与版本化源除默认 WS URL 外代码一致；运行目录本身不是 Git 仓库。
- A05 任务卡已将运行目录列为 forbidden path，避免未验收代码直接影响在线 Agent。

## ADR-005：协作任务状态机与 CAS 事务边界

- 状态：accepted
- 日期：2026-07-23
- 决策人：B03 Owner + 主控独立 Reviewer
- 关联任务：B03～B05、B08、C01
- 实现 commits：`2fbe6ae755d7c856f8a59415736f10cd283862b0`、`a357bebee1f60ee27d21303ddc122bbc126ef752`
- 集成 commits：`408d029`、`790d282`

### 决策

- Task、member、work item 分别使用独立有限状态机；持久状态必须精确匹配 canonical 小写值，请求 target 可做 trim/lowercase 归一化。
- 所有写入使用显式 `tenant_id + client_id + 业务 ID + expectedVersion` CAS；0 行更新返回版本冲突，不做静默覆盖或无限重试。
- member 报告只改变自身 member/work item，不直接完成整项任务；任务聚合完成规则由 B05 负责。
- member + work item 组合转换必须先完成全部状态、task 归属和 assignee 校验，再在同一 Spring 事务中执行两笔 CAS；第二笔冲突必须回滚第一笔。
- work item 的 `ready <-> claimed`、`claimed -> running/ready/cancelled` 等 claim-sensitive 转换保留给 B04 lease/claim 协议，通用状态服务 fail closed。
- 终态不可恢复；blocked/failed 必须按规则记录 failure reason；submitted 驳回为 ready 时清理提交/完成/成果引用状态。

### 验证方式

- mock 单元测试覆盖非法转换、终态、scope miss、完整快照、持久非 canonical 状态和 assignee 不匹配。
- H2 + MyBatis-Plus `SpringManagedTransactionFactory` + `DataSourceTransactionManager` 集成测试覆盖两笔 CAS 正向提交及第二笔冲突回滚。
- 集成到 `api/develop` 后 agent core/mapper/service 与 chat service 联合测试通过。

## ADR-006：M2 aggregate CAS、event version、snapshot 与 SSE 恢复语义

- 状态：accepted
- 日期：2026-08-03
- 决策人：M2 主控 / GPT-5.6 Sol High
- 关联任务：M2-00、C01、C01B、C01H、C02～C08
- 详设：`docs/implementation/M2_EXECUTION_PLAN.md`

### 背景

现有 `agent_task_meta` 同时有 `task_version` 和 `current_event_version`。前者已用于任务聚合 CAS，后者预留为持久事件游标。若 SSE 把两者混为一个 `taskVersion`，member/work-item/request/artifact 变化时会出现 CAS 语义、事件连续性和历史 baseline 不一致。

### 决策

1. MySQL 中的任务状态与 `agent_task_event` 是唯一事实源；进程内 Broker 只负责本实例低延迟唤醒，RabbitMQ 不承担浏览器事件事实源。
2. `agent_task_meta.task_version` 只表示任务聚合乐观锁版本。仅 task meta 自身按既有状态机/CAS 规则变化时递增；member/work-item 等子聚合事件不得为了 SSE 擅自递增它。
3. `agent_task_meta.current_event_version` 是任务范围内最新持久事件版本。每成功持久化一个 task event，在同一事务中恰好递增一次。
4. `agent_task_event` 使用 `event_version` 字段；插入值必须等于本次更新后的 `current_event_version`。唯一键为 `(tenant_id, client_id, task_id, event_version)`。
5. workspace `currentVersion`、SSE `id`、`sinceVersion`、`Last-Event-ID` 和前端 reducer 游标全部指 event version，不指 aggregate `task_version`。
6. C01B 覆盖 B03～B08 全部成功业务写路径：业务状态写入、event 插入和 `current_event_version` 更新同事务；回滚、CAS 冲突、ACL 拒绝、无变化和幂等重放不得产生伪事件。
7. B09 明确不写 task event。C01H 使用确定性 event ID，为 B09 受影响任务幂等追加 `HISTORICAL_BASELINE_IMPORTED`；同事务分配下一 event version，更新 `current_event_version`，保持 `task_version` 不变。
8. Broker 只能 after-commit 发布已持久事件；回滚事务不得向实时订阅者暴露事件。
9. SSE 固定先订阅 live、再 replay 数据库历史、去重并校验连续性；无法证明连续性时发送 `resync_required`。
10. 前端 event version 全程使用十进制字符串，禁止窄化为 JavaScript `Number`；`event.version <= currentVersion` 幂等忽略，只接受精确下一版本。
11. M2 API/Web feature flag 默认关闭，按获准测试 scope 开启；关闭时保持 M1 旧流程可用。
12. M2 不触碰当前脏 `develop` worktree。所有 accepted commit 累计集成到独立 `feat/m2-api-base-20260803` / `feat/m2-web-base-20260803`，最终合流另立任务。
13. M2 采用一次一个 Writer、跨模型只读 Review；核心任务测试代码由同一 Writer 提交，Flash Test Runner 只运行验证，避免双 Writer。

### 事件版本事务公式

```text
lock scoped agent_task_meta row
oldEventVersion = current_event_version
newEventVersion = oldEventVersion + 1
apply business mutation / CAS
insert agent_task_event(event_version = newEventVersion, deterministic event_id, ...)
update agent_task_meta.current_event_version = newEventVersion
commit
publish persisted event after commit
```

任何一步失败都回滚。若业务入口实际没有产生状态变化，则不得分配 event version。

### 影响

- C02 必须等待 C01B 和 C01H，使 Broker 上线前已有完整事件源和历史基线语义。
- C04 snapshot 返回的 `currentVersion` 必须来自 `current_event_version`。
- C05 SSE 只接受 event version 游标；错误地传 aggregate task version 必须按 contract 处理，不得静默混用。
- C06/C07 必须显示 resync、reconnecting 和 polling degraded 状态。
- M3 RabbitMQ 可传输命令，但不能替代 task event 数据库 replay。

### 被否决方案

- 使用 `task_version` 同时承担 aggregate CAS 和 SSE sequence：子聚合变化会破坏其中一种语义。
- 只使用内存 Broker：API 重启即失去历史。
- 先 replay 再订阅 live：连接窗口可能丢事件。
- 用前端 `Number` 保存 BIGINT version：超过 `2^53` 后比较和去重错误。
- Pro Writer 与 Pro Reviewer 自审：不满足跨模型独立审查。
- 同一核心任务由 Pro 写业务、Flash 再写测试：破坏一个任务/一个 Writer 的责任边界。

### 验证方式

- MySQL 并发 event version、current_event_version 最大值和事务回滚故障注入。
- member/work-item 事件证明 event version 递增但 task_version 不被无故修改。
- C01H baseline 重复执行、部分漂移、失败回滚和 B09 顺序测试。
- live/replay 窗口、重复、gap、cursor ahead、历史截断和 API restart 测试。
- 大于 `2^53` 的 event version contract/reducer 测试。
- 跨 tenant/client/task ACL、feature flag 和 SSE 资源清理测试。


## ADR-007：M2 自适应模型路由与单 Writer 四槽流水线

- 状态：superseded by ADR-012 (2026-08-25)
- 日期：2026-08-15
- 决策人：M2 主控 / GPT-5.6 Sol High
- 关联任务：C01B～C08
- 路由事实源：`docs/implementation/MODEL_ROUTING.yaml` schema v3

### 背景

原 M2 路由把 C01B/C01H 等 P0 事务/迁移任务默认交给 DeepSeek Pro Writer，同时通用策略又要求 P0 由 Sol Critical Writer，存在优先级冲突。C01 的多轮 Review、隔离 MySQL 和事务传播返工还表明：完全串行准备、重复全量测试和 byte-exact 集成重复 Review 是主要等待来源。

### 决策

1. 显式任务路由优先于通用领域路由；P0 identity/ACL/transaction/concurrency/migration/snapshot consistency 由 GPT-5.6 Sol High `critical_worker` 实施，DeepSeek V4 Pro 只读对抗 Review。
2. DeepSeek V4 Pro Writer 聚焦 after-commit、replay、SSE、recovery reducer；GPT-5.6 Terra 负责冻结契约后的普通接入、feature flag 和集成；Flash 只写纯展示 UI，Luna 只做机械质量工作。
3. 全局保持一个源码 Writer，同时使用三个只读槽位：Terra Explorer 准备调用链，GPT-5.4 Mini 生成验收/证据矩阵，DeepSeek Flash 准备测试、fixture、隔离数据库和资源探针。
4. Writer 开发阶段只跑 targeted/touched suites。最终 candidate 由独立 Test Runner 运行一次模块全量；schema/migration/transaction 最终 tree 运行一次隔离 MySQL。
5. 验证证据按 `git tree SHA + test selector + DB fixture digest` 建键；键未变化时 Reviewer 和集成门禁复用证据。
6. 无冲突、无语义修改且 source/integration tree byte-exact 的 no-ff merge 只核对 parent/source/tree SHA，不重复完整代码 Review；冲突、语义修改、tree mismatch 或证据失效时必须复审。
7. 5 GiB 是资源硬下限，6.5 GiB 是 Gradle 全量、npm build、隔离 MySQL 和 integration worktree 的软门禁。低于软门禁先由 DeepSeek Pro 只读盘点，任何破坏性清理仍需明确授权。
8. 用户逐项确认规则不变：只读槽位可以提前准备，但下一任务不得提前 claim 或成为第二个源码 Writer。

### 目标与约束

- P0 首轮 Review 不出现 P0/P1 finding；P0 总评审轮次不超过 2。
- P1/UI 评审轮次不超过 1。
- 每个最终 tree 模块全量测试不超过 1 次；必要的隔离 MySQL 不超过 1 次。
- byte-exact 集成重复完整代码 Review 次数为 0。
- 预计剩余 M2 周期缩短 18%～28%，约节省 2～4 个执行日；该估算不覆盖外部环境和生产审批等待。

### 被否决方案

- 多个 Writer 并行修改强依赖源码：会造成重复实现、契约漂移和 worktree 冲突。
- 继续把所有 M2 核心任务交给同一模型：模型能力与任务风险不匹配，也削弱跨模型 Review 的独立性。
- 每轮 Review 都重跑全量 Gradle/MySQL：成本高，且对相同 tree 不增加有效证据。
- 为追求磁盘门禁自动删除未知文件、stash 或 worktree：不可审计且可能丢失用户数据。


## ADR-007A：取消固定内存与磁盘 Admission Gate

- 状态：accepted
- 日期：2026-08-28
- 决策人：用户 + 主控

### 决策

1. 固定 `MemAvailable`、5 GiB、6.5 GiB 等阈值不再拒绝 Gradle、npm build、隔离 MySQL/Rabbit、integration worktree、smoke 或恢复流程。
2. 资源快照、旧阈值和低资源告警继续写入证据，但仅作 telemetry。
3. Gradle、隔离 MySQL/Rabbit 和重型磁盘操作继续全局串行；不得以取消门禁为由并行抢锁。
4. 真实 OOM、ENOSPC、inode exhausted 或 swap thrashing 必须先归因；连续两次失败仍进入 `blocked_root_cause`。
5. 不得自动终止其他线程进程或删除 worktree、缓存、证据、生产数据来释放资源。


## ADR-008：M2 引入 GPT-5.3 Codex Spark 快速 Writer

- 状态：accepted
- 日期：2026-08-17
- 决策人：用户 + M2 主控
- 关联任务：C05～C08
- 路由事实源：`docs/implementation/MODEL_ROUTING.yaml` schema v5

### 决策

1. 本机 `gpt-5.3-codex-spark` 只读健康探针已返回 `SPARK_OK`。
2. C05～C07F 已冻结且可分包的 Java/Vue 实施和 focused tests 使用 `spark_worker`，保持一个源码 Writer。
3. 新身份/ACL 语义、事务重设计、迁移、破坏性数据变化和最终 GO/NO-GO 仍由 GPT-5.6 Sol High 负责。
4. Spark Writer 不得自审；独立测试使用 GPT-5.4 Mini，独立 Review 和 release guard 使用 Sol High。
5. 已产生候选的 C04 不在中途换模。若 Spark 探针失败或越过冻结合同，停止该包并升级到 Sol，不做保守回退式删减功能。

### 影响

- 减少合同冻结任务的等待时间，同时保留安全、事务和发布门禁质量。
- `.codex/agents/spark-worker.toml` 与 `.codex/config.toml` 注册 durable Agent profile；当前执行可使用显式 `codex exec --model gpt-5.3-codex-spark`。

## ADR-009：案卷阁阅读采用独立版本化事实域

- 状态：accepted
- 日期：2026-08-22
- 决策人：用户 + 主控 Agent
- 关联任务：H01～H06
- 规格：`specs/archive-pavilion-reader-mvp/`

### 决策

1. 完整典籍阅读使用新的 `/archive/v1` 事实域；现有 `/chat/library/search` 继续表示项目案卷和用户记忆检索，二者不得混为同一事实源。
2. 首版固定《水浒传》120 回不可变版本 `shuihuzhuan-zh-120-v1`；正文、章节顺序、段落边界或 hash 变化必须发布新 edition。
3. 阅读进度、书签和私人手札按服务端认证的 `tenantId + clientId + ownerJiacn` 精确隔离，使用 CAS 和幂等写入，不回退 `Anonymous`。
4. 吴用保持普通 Agent；首期选文提问只使用 built-in 降级角色“案卷书吏”，不读取地图选中态，不调用 `/agent/active`。
5. 任职、悬赏和积分报酬不进入本 MVP，待阅读闭环验收后另立 SDD。
6. H01 先冻结可执行内容/契约，H02/H03 处理 P0 schema/ACL/transaction，H04 完成阅读垂直切片，H05A/H05W 分别完成 Agent 问答后端与前端恢复，H06 执行真实环境与发布门禁。

### 影响

- Elasticsearch 故障不得阻塞典籍阅读和私人数据。
- Review 不按按钮逐项进行，但 P0 migration/ACL/transaction/replay 必须即时独立 Review。
- 当前 C08 发布 NO-GO 不阻止规格准备，但新功能不得绕过既有发布门禁上线。


## ADR-010：M2 develop 合流保持协作域 exact tenant scope，M3 增加离线 Rabbit 启动门禁

- 状态：accepted
- 日期：2026-08-23
- 决策人：M2/M3 主控 / GPT-5.6 Sol High
- 关联任务：C09A、C09W、C09、M3-00、D01～D09

### 决策

1. `tenant_id='0'` 的通用 public/default fallback 不适用于协作任务事实域；task/member/work-item/request/artifact/event/task-thread 必须按 tenant/client/task byte-exact 查询、锁定、CAS 和授权。
2. 历史 NULL/`'0'` 协作记录只能通过 B09/C01H 显式审计迁移处理，不得由普通请求隐式跨租户读取或写入。
3. M2 冻结候选只在独立 integration worktree 与当前 develop 收敛；API 语义冲突修复和 Web baseline 债务关闭前，不更新 dirty develop/master 或 root gitlink。
4. M3 在 D01 前新增 M3-00：flag 全关零副作用、非法组合 fail-fast、Rabbit Testcontainers 随机端口/账号/vhost、禁止连接本机 5672/远程 Rabbit/生产凭证。
5. D04 前移至 D03 前，D07 前移至 D05 前；源码 accepted 与生产 not_deployed/not_migrated/not_enabled 分开记录。

### 影响

- C08 r6 GO 仍有效于冻结候选，但不能作为 develop 合流树的测试证据。
- C09 会产生新的 API/Web tree；合流后必须按变更风险重跑 targeted gate。
- M3 可离线实现，但生产 Rabbit、DDL、部署和开 flag 仍需独立变更授权。

## ADR-011：D08 持久 Hall 命令扩展 canonical transport，不伪装 TASK_INVITE

- 状态：accepted
- 日期：2026-08-25
- 决策人：M3 主控 / GPT-5.6 Sol High
- 关联任务：D02、D05～D08
- 预检：`docs/implementation/preflight/D08.md`

### 背景

`HallActionDispatcher` 当前会把 `ask_help`、`request_report`、work-item 和 context refresh 等动作在线直发，离线时写入 JVM `ConcurrentHashMap`。D08 要求数据库 delivery 成为唯一 mailbox 且 API 重启后仍可恢复；但 D02 的 canonical writer 只接受 `TASK_INVITE`，不能把其他 Hall 动作伪装成邀请，也不能继续保留第二套内存事实源。

### 决策

1. D08 正式扩展既有 `agent_command_delivery + agent_outbox_event + agent_consumer_inbox` transport，使其支持 Protocol v1 已有 allowlist 中的 Hall command types；不新建第二套 Hall mailbox 表或旁路 Rabbit transport。
2. 既有 `TASK_INVITE` command ID、TTL、payload 字段顺序和 canonical bytes 必须 byte-exact 不变，D02 accepted evidence 不因 D08 被静默重写。
3. Hall command 使用独立、受限的 canonical payload；禁止持久任意 `Map`。允许字段仅包括 action type、instruction、reason、conversation association、trigger event、autonomy/approval 和经明确 allowlist 的 bounded context scalar/list。认证头、凭证、完整聊天正文、任意嵌套对象和未知字段一律拒绝。
4. Hall `commandId` 由 exact `tenant + client + task + targetAgent + intentId + commandType` 确定性生成；同一 intent 的同字节重试幂等，payload 或身份变化必须 conflict/fail closed。reissue 继续使用新 `messageId`、原 `commandId`。
5. flag-on 路径在写 delivery 前执行 exact tenant/client/task/targetAgent ACL；未授权请求不得形成 delivery/outbox 审计噪声。在线与离线统一先写数据库，不再在线直发绕过事实源。
6. `rabbit-dispatch=false` 或 M3 flags 全关时保持当前 M1 兼容路径且不得访问 M3 三表；进入 dispatch canary 后，获准 exact scope 只走 durable transport，禁止 legacy 与 Rabbit 双发。
7. `/juyiting/agents/{agentId}/mailbox` 在 durable scope 内改为读取数据库 delivery 的有界投影，不返回 raw command payload、hash、内部 lease、replay 审批或跨 scope 存在性。旧 JVM list 不再承担事实职责。
8. D08 必须等待 D06 accepted final HEAD/tree；不得从 D06 dirty worktree 开发。ACK/reissue/provenance 对新增 command type 的扩展必须与 D06 栅栏语义一致，并重新独立 Review。

### 被否决方案

- 把 `REQUEST_RESPOND`/`CONTEXT_REFRESH` 等伪装成 `TASK_INVITE`：改变 Agent 行为且破坏 canonical 幂等身份。
- 只持久 task invite、其他 Hall action 继续内存排队：D08“唯一 mailbox”和重启恢复目标未完成。
- 新建独立 Hall mailbox 表：形成第二事实源，绕过 D03/D05/D06/D07 的 confirm、Inbox、ACK 和 reissue 语义。
- 在数据库事务内做 WebSocket/Rabbit I/O：扩大锁持有并破坏 after-commit/outbox 边界。
- 持久任意 `context` Map：会引入不可控 schema、敏感信息和 canonical byte 漂移。

### 验证方式

- 旧 TASK_INVITE canonical golden bytes/hash 完全不变。
- 每个新增 command type 的 canonical/golden、非法字段、超限、credential-like 内容和 duplicate-key 测试。
- exact ACL 失败时 delivery/outbox/inbox 零写入。
- online/offline 统一 durable 写入；重复 intent 无重复副作用；重连新 messageId/原 commandId。
- API 重启前后从同一 MySQL delivery 恢复；旧 JVM mailbox 不参与恢复。
- flags-off 零 M3 Bean/SQL/Rabbit 副作用；canary exact scope 无 legacy/Rabbit 双发。


## ADR-012：取消全局唯一 Writer，改为任务/路径级并行

- 状态：accepted
- 日期：2026-08-25
- 决策人：用户 + 主控 Agent
- 关联范围：全部实施任务、聚义厅横竖屏 O00～O04
- 路由事实源：`docs/implementation/MODEL_ROUTING.yaml` schema v8

### 决策

1. 取消“全局同时只能有一个源码 Writer”的限制。依赖已满足的独立任务可在独立 worktree 并行实施。
2. 每个任务仍只有一个实现 Owner；claim 前必须冻结 owned paths。不同 Writer 的 owned paths 不得重叠，exact path 冲突只暂停冲突文件并协调交接，不抢占、不回退他人修改。
3. 显式任务依赖不因并行策略取消；例如 O01 仍等待 O00 ACCEPT，D09 仍按其冻结 dependencies 判定。
4. Reviewer、Verifier、Explorer 和准备 Agent 保持只读，不能借并行策略修复或预实现被审任务。
5. `/tmp/cyf-gradle.lock` 继续串行所有 Gradle；隔离 MySQL/Rabbit、browser gate、production build 和重型磁盘任务按资源门禁串行或错峰。
6. `docs/implementation/**` 仍由主控维护；生产部署、迁移、开 flag 和真实环境操作仍需独立授权。

### 影响

- D08 verification、D09 实施、H06 有界 runner 整改和 O00 Web 收敛可在路径无重叠时并行。
- 进展与验收仍按 exact commit/tree、定向测试和独立 Reviewer verdict 统计；并行启动本身不计完成度。
