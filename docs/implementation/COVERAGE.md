# 多 Agent 协作实施覆盖矩阵

> 状态：M1 代码集成完成，M2 基线计划已冻结（2026-08-03）  
> 设计依据：`docs/juyiting-multi-agent-collaboration-design.md`

本文件用于防止漏实施。每个里程碑结束时，Audit Agent 必须更新“代码证据、测试证据、状态”三列。

状态取值：`未开始 / 实施中 / 待验收 / 已覆盖 / 有缺口`。

## 1. 核心功能覆盖

| 设计要求 | 设计章节 | 任务 | 预期代码区域 | 测试/证据 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 稳定 Agent 领域 ID | 2.2、17、20 | A01、A02 | `api/agent/**`、Agent 客户端 | A01/A02 已验收并集成；生产审计发现运行时仍使用 legacy ID，A08 正补齐 opaque 签发、registry/alias 解析和授权闭环 | 实施中 |
| 多成员独立状态 | 7.2、8 | B01～B03、B05 | `api/agent/**` | B01～B05 已集成；状态转换、CAS、聚合、parent gate 并发与 MySQL 8.0.21 byte-exact 校验通过 | 已覆盖 |
| 工作项及依赖 | 7.3、7.4 | B01、B02、B04、E03、E04 | `api/agent/**` | B01 Schema、B02 scoped DAO/CAS 已集成；待 claim/依赖测试 | 实施中 |
| claim/lease/heartbeat | 9.5 | B04、E05 | `api/agent/**` | B04 已集成：双 claim、heartbeat/expiry、旧 token、max attempts、迟到结果及 scoped CAS 通过；待 E05 超时重派策略 | 实施中 |
| 诉求协作 | 7.7 | B01、B02、B06、E08 | API + Vue | request Schema 与 B06 服务已集成；ACL 下推、501+ 行、状态与冲突分类测试通过 | 已覆盖 |
| 成果共享与版本 | 7.6、15 | B01、B02、B06、F02、F06 | API + 存储 | artifact Schema 与 B06 服务已集成；版本、ACL、UTF-8 边界及冲突测试通过 | 已覆盖 |
| 任务共享会话 | 7.8 | B07 | `api/chat/**`、`api/agent/**` | B07 实施中：待成员/非成员、跨 scope 和 generic chat 绕过测试 | 实施中 |
| 任务聚合状态 | 8 | B03～B05、B08 | `api/agent/**` | B05 聚合已验收；待 B08 旧 report 兼容层验证多人不误完成 | 实施中 |
| 可解释推荐 | 9.2～9.4 | E01、E02、E07 | API + Vue | 评分和排除原因测试 | 未开始 |
| 自动拆解和依赖调度 | 9、14 | E03～E06、E08 | API + Vue | E2E 工作项流程 | 未开始 |

## 2. 通信和可靠性覆盖

| 设计要求 | 设计章节 | 任务 | 预期代码区域 | 测试/证据 | 状态 |
| --- | --- | --- | --- | --- | --- |
| chat/command/progress/result 分离 | 10 | A03、A06、B08 | `api/chat/**`、Agent 客户端 | A03/A06 服务端与 Agent ACK 队列已集成；待 B08 旧 report/结果闭环 | 实施中 |
| Agent 本地持久队列 | 10.4 | A05、A06 | codex-ws-agent | A05 已集成 isp-install/master：17 tests 覆盖忙碌/重启/FIFO/fsync/权限/非法记录；待 A06 ACK 幂等 | 已覆盖 |
| commandId 和 ACK | 10.1～10.3 | A03、A06、D06、D07 | API + Agent 客户端 | A06 已集成：全局 FIFO、ACK ledger、崩溃恢复、损坏文件 fail-closed 测试通过 | 实施中 |
| 持久 task event | 7.5、13 | C01、C01B、C01H、C02、C03 | `api/agent/**` | 已拆分 Schema/版本、全业务写路径原子事件、B09 baseline、after-commit、replay/gap | 未开始 |
| workspace snapshot | 13.1 | C04 | API | currentVersion=current_event_version；覆盖一致性、ACL 和 BIGINT 字符串 | 未开始 |
| SSE replay/resync | 13 | C03、C05、C06、C08A、C08W | API + Vue | event_version 游标；覆盖连接窗口、重复、gap、重启、降级和可见性恢复 | 未开始 |
| TaskWorkspace/Timeline | 13.3、21.3 | C07A、C07B、C07C、C07、C07F | Vue | 数据接入、纯展示、响应式/可访问性、flag 和前端集成分阶段验收 | 未开始 |
| Outbox 原子性 | 11.1 | D01～D03 | `api/agent/**` | DB/MQ 故障注入 | 未开始 |
| Inbox 幂等 | 11.2 | D01、D07 | `api/agent/**` | 重复消息副作用测试 | 未开始 |
| 离线投递状态 | 11.3、12 | D01、D05、D06、D08 | `api/agent/**`、`api/chat/**` | 离线重连补投测试 | 未开始 |
| Rabbit retry/DLQ | 12 | D03～D05、D09 | Rabbit/Spring AMQP | confirm、return、DLQ 测试 | 未开始 |

## 3. 安全与工程覆盖

| 设计要求 | 设计章节 | 任务 | 预期代码区域 | 测试/证据 | 状态 |
| --- | --- | --- | --- | --- | --- |
| tenant/client/task/agent 隔离 | 17 | A04、B02、B06、B07、G01 | API | A04/B02/B06 已覆盖 scoped ACL；待 B07/G01 跨租户闭环 | 实施中 |
| WebSocket 精准投递 | 17 | A04、D05 | `api/chat/**` | 非目标 Agent 不收消息 | 未开始 |
| 编码 Agent 独立 worktree | 16 | A07 | Agent 客户端/脚本 | 并行修改隔离演练 | 未开始 |
| 历史数据迁移 | 20 | A02、B09、C01H、G06 | SQL/迁移脚本 | A02/B09 代码已独立验证；生产 B09 与 C01H event baseline 仍需维护窗口审批执行 | 实施中 |
| Feature flags 和灰度 | 20、24 | G05 | API 配置 | 逐租户启停测试 | 未开始 |
| 监控、DLQ、告警 | 18 | D09、G07 | API/运维 | Dashboard 和告警演练 | 未开始 |
| 故障恢复 | 19、21 | G02、G04 | 全链路 | Rabbit/API/Agent 重启 | 未开始 |
| ES 任务级 ACL | 15 | F03～F05 | 记忆/索引模块 | 跨任务检索隔离 | 未开始 |
| 单 Agent 旧接口兼容 | 14.4、20 | B08、G01、G04 | API + Vue | 旧 assign/report 回归 | 未开始 |

## 4. 里程碑审计清单

每个里程碑结束前必须回答：

- [ ] 本阶段设计章节是否全部映射到任务？
- [ ] 每个任务是否有唯一 Owner？
- [ ] 每个 accepted 任务是否有 commit 和测试证据？
- [ ] 是否存在实现了但没有任务 ID 的代码？
- [ ] 是否存在标记完成但未进入集成分支的任务？
- [ ] 是否有数据库变更但没有迁移 SQL？
- [ ] 是否有新事件但没有前端 reducer 或兼容策略？
- [ ] 是否有 Rabbit 消息但没有 Inbox/幂等策略？
- [ ] 是否有 Agent 写任务但没有 tenant/client/task ACL？
- [ ] 是否更新了 `DECISIONS.md` 和相关运维说明？
