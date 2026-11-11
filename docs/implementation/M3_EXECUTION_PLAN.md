# M3 RabbitMQ 可靠传输执行计划

> 基线日期：2026-08-23  
> 前置状态：M2 C08 已 GO，但未生产部署、未执行 B09/C01H、未操作生产 RabbitMQ；当前先完成 C09 develop 合流收敛。

## 1. 目标与边界

M3 将 Agent 命令从进程内 mailbox 演进为 MySQL 事实源 + RabbitMQ 至少一次传输：

```text
业务事务
  -> task_event + command_delivery + outbox
  -> Outbox Relay
  -> RabbitMQ
  -> Inbox 幂等 consumer
  -> exact target WebSocket dispatcher
  -> RECEIVED/STARTED/SUCCEEDED ACK
```

源码可在离线隔离环境实施，不以 M2 已生产部署为前提。以下始终需要独立生产授权：B09/C01H apply、D01 DDL、Rabbit vhost/user/topology、部署、开 flag、shadow/canary、DLQ 查询或重放。

## 2. M3-00 启动门禁

D01 前必须先完成 M3-00：

1. M3 基线绑定 C09 accepted 的精确 API HEAD/tree，不从 dirty `api/develop` 直接开发。
2. 测试禁止连接远程 Rabbit、本机固定 `127.0.0.1:5672`、默认 vhost 或生产凭证。
3. Rabbit 集成测试只允许 Testcontainers、随机宿主端口、随机账号和每次唯一 vhost；禁止 host network。
4. 所有 M3 flags 在 dev/grey/prod/test 显式默认 `false`。
5. flag 全关时不得注册协作 Rabbit topology、relay、listener、retry scanner，也不得产生 M3 DB 写入。
6. 非法 flag 组合启动时 fail-fast；基础设施暂时不可用只降级 readiness，不破坏 MySQL 事实写入。
7. 修复或替代固定 Rabbit 3.8 且初始化时序不安全的 `RabbitMqServerLoader`。
8. 隔离 Rabbit/MySQL、Gradle 全量和新大型 worktree 前记录磁盘/内存/swap 快照，但自 2026-08-28 起固定阈值仅作观测，不再作为停止线；重型资源仍串行。

启动状态机：

```text
OFF -> DB_SHADOW -> MQ_SHADOW -> DISPATCH_CANARY -> DISPATCH_SCOPED
```

配置依赖：

```text
publish  => outbox + topology
consume  => topology
dispatch => outbox + topology + publish + consume + non-empty exact-scope allowlist
```

## 3. 依赖链与实施顺序

```text
C09
  -> M3-00
      -> D01
          -> D02
          -> D07
      -> D04

D02 + D04       -> D03
D03 + D04 + D07 + A04 -> D05
D02 + D03 + D05 + A06 -> D06
D01 + D02 + D03 + D05 + D06 + D07 -> D08
D03 + D04 + D06 + D07 -> D09
D01-D09 -> M3-RG
```

推荐执行顺序：

```text
M3-00 -> D01 -> D02 -> D07 -> D04 -> D03 -> D05 -> D06 -> D08 -> D09 -> M3-RG
```

关键重排：D04 必须先于 D03 冻结 topology；D07 必须先于 D05 建立 Inbox 幂等；D02 依赖 C01B 而不是仅 C01；D09 必须等待 delivery/reconnect/inbox 语义稳定。

## 4. 任务级并行 Writer 执行包

| 包 | 任务 | 任务级 Writer | 只读准备 | 验证与 Review |
| --- | --- | --- | --- | --- |
| K0 | M3-00 | `critical_worker` | `explorer` + `fast_query` | `gpt_test_runner` + `sol_reviewer` |
| K1 | D01 | `critical_worker` | schema/initializer + migration matrix | 隔离 MySQL + `sol_reviewer` |
| K2 | D02 -> D07 | `critical_worker` | transaction/crash matrix | targeted tests + transaction Review |
| K3 | D04 -> D03 | `critical_worker` | topology/confirm/retry matrix | 隔离 Rabbit + cross-model Review |
| K4 | D05 | `critical_worker` | WS presence/ACL call chain | consumer + WS integration |
| K5 | D06 -> D08 | `critical_worker` | reconnect/restart/compatibility | API/Agent restart drill |
| K6 | D09 | `critical_worker` | ops ACL/audit/replay matrix | security Review + fault drill |
| RG | M3-RG | 无源码 Writer | evidence index | `release_guard` GO/NO-GO |

每个原任务保留独立 commit、handoff、tree SHA 和微门禁。Reviewer 只读，REJECT 后由原 Writer 修复。DeepSeek 当前按用户指令全部停用，不执行健康探针；Writer、验证和 Review 均固定走 GPT 路由，直到用户明确恢复。

## 5. 关键验收

### D01

- delivery：`tenant+client+commandId` 唯一；outbox：`tenant+client+eventId` 唯一；inbox：`tenant+client+consumerName+messageId` 唯一。
- 完整 status/retry/lease 索引、CAS version、expiry、payload hash。
- fresh/upgrade/repeat/drift 隔离 MySQL 矩阵通过；initializer 不隐式历史回填。

### D02 + D07

```text
domain mutation + task_event + command_delivery + outbox = one REQUIRED MySQL transaction
```

任一失败整体回滚。`commandId` 是业务幂等键，重投不变；`messageId` 是单次运输键，重新投递生成新值。同 messageId 同 hash 幂等；同 messageId 不同 hash 拒绝并告警。

### D04 + D03

- durable topic exchange/queue，persistent message，manual ACK，TTL+DLX retry，不依赖 delayed-message 插件。
- Relay 短事务 claim，网络发布在事务外，confirm 后独立 CAS；mandatory return 和超时进入退避。
- crash-after-confirm 允许重复发布，由 Inbox 幂等消除副作用。
- shadow backlog 必须不可转为真实派发。

### D05

```text
Rabbit receive -> durable Inbox/delivery claim -> WS send -> durable disposition -> Rabbit ACK
```

WS send 只可标记 `SENT`，不能标记 `RECEIVED`。必须 exact 匹配 `tenant+client+task+targetAgent`，禁止广播和 hidden selected state。

### D06 + D08

Agent 离线时写 `WAITING_AGENT + next_retry_at` 后 ACK Rabbit，禁止热循环。重连 CAS 只能一个扫描器生成新 outbox；使用新 messageId、原 commandId。D08 flag-on 后 DB delivery 是唯一 mailbox 事实源，API 重启可恢复。

### D09

- broker redrive：未形成持久 disposition 时保持 messageId/hash。
- 人工 reissue：新 messageId、原 commandId、记录 parent、审批人和原因。
- 禁止重放 SUCCEEDED、跨 scope 重放、编辑 payload 后复用 messageId、无审计直接发布 DLQ payload。

## 6. 证据与资源策略

- 证据键：`Git tree SHA + test selector + DB fixture digest + Rabbit topology manifest digest`。
- 所有 Gradle 命令持 `/tmp/cyf-gradle.lock`，单 worker、低内存、重型验证串行。
- Rabbit/MySQL 集成测试必须记录容器 ID、随机端口/vhost、镜像 digest、cleanup 结果以及生产 PID/listener 未变化证明。
- full suite 每个最终 tree 最多一次；开发阶段只跑 touched/targeted tests。

## 7. 生产激活窗口

1. **R1 M2 落地**：停写/排空 -> 备份恢复门禁 -> B09 -> C01H -> 双签 -> 部署 M2 flags=false -> M1 smoke。
2. **R2 M3 schema-only**：D01 DDL -> schema 验证 -> 部署 M3 artifact，全部 M3 flags=false。
3. **R3 Rabbit 运维**：独立 vhost/user/最小权限 -> topology manifest 声明 -> passive verify，dispatch 仍 false。
4. **R4 分级启用**：DB_SHADOW -> MQ_SHADOW -> exact-scope canary -> restart drill -> scoped dispatch。

源码 `accepted/integrated` 与生产 `not_deployed/not_migrated/not_enabled` 必须分开记录。
