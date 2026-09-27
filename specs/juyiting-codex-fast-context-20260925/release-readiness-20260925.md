> 2026-09-27 更新：请先读 [合并评估](merge-assessment-20260927.md) 和 [开发交接](developer-handoff-20260927.md)。当前不可直接合入；本文历史 Reviewer、未测算资源门槛及逐次审批要求不作为现行门禁。以下保留历史记录。

# 聚义厅 Codex 快速议事发布前置条件

日期：2026-09-25
状态：Blocked；本文是发布门禁，不是已执行证据。

## 1. 宿主资源门禁

发布、迁移或再次构建前，运维必须确认根分区与 `/tmp` 有足够的构建、备份和回滚空间，且 swap 未耗尽。当前开发宿主不满足该条件，因此禁止在本机执行部署或 MySQL migration。

## 2. 机器令牌分阶段切换

新资源端会拒绝缺少 `tenant_id` / `tenant_claim_version` 的机器 JWT。不得把授权服务器和资源服务器作为一次无等待的全量切换：

1. 先仅部署会签发 `tenant_id=0`、`tenant_claim_version=1`、`token_kind=machine` 的 OAuth 授权服务器制品。
2. 对每个 client-credentials 客户端签发 canary token，解码确认上述 claims；不记录 token 正文。
3. 从实际 RegisteredClient 配置读取 access-token TTL，列出所有机器客户端并轮换凭证或等待旧 token 的最晚过期时间；没有清退清单不得继续。
4. 先对一个低风险资源服务启用新 filter，验证新 token 成功、旧无 tenant token fail closed，再逐服务发布。
5. 最后发布 chat API；任何 Agent 仍使用旧 token 时停止 rollout，不放宽 tenant 校验。

## 3. MySQL 8 备份、演练与恢复

migration 前必须停止 chat relay/写入或进入经验证的维护窗口，并使用实际数据库账号在受控备份目录执行等价于：

```bash
mysqldump --single-transaction --quick --routines --triggers \
  "$MYSQL_DATABASE" \
  chat_dispatch_outbox chat_turn chat_context_snapshot chat_request chat_message \
  chat_conversation_event chat_deliberation_schema_version \
  > "$BACKUP_DIR/chat-deliberation-v2-pre.sql"
sha256sum "$BACKUP_DIR/chat-deliberation-v2-pre.sql" \
  > "$BACKUP_DIR/chat-deliberation-v2-pre.sql.sha256"
```

如果旧库尚无后两张表，备份命令应按 `information_schema.tables` 的实际结果生成表清单。备份必须先恢复到隔离 MySQL 8 实例并校验行数、主键/唯一键、活跃 outbox 状态与 payload digest；仅生成 dump 不算通过。

migration 后必须读取：

- `chat_deliberation_schema_version.version=2, stage=APPLIED`；
- 新列定义与两个 outbox 索引；
- `chat_conversation_event` replay 索引；
- active `DISPATCH/CANCEL_REQUESTED/FINAL_PERSISTED` 均为合法 JSON；
- 被标记 `DEAD` 的 legacy 行数和原因，并由人工确认。

失败恢复流程：停止新版本 API/relay，保留失败现场 dump，恢复上述 pre-migration 备份到隔离库验证后再恢复生产库，并回退到旧 API/Runtime。由于 migration 会规范化 payload、生成事件并将不可恢复行标记 `DEAD`，没有 pre-migration 备份时禁止声称可逆，也禁止执行 migration。

## 4. 发布证据

只有以下证据齐全后，`integration.yaml` 的 release 状态才可改为 ready/released：

- 宿主磁盘、`/tmp`、内存、swap readback；
- 机器 token 清退清单、最大 TTL、canary claims 和分阶段部署时间；
- MySQL 8 备份 SHA-256、隔离恢复演练与 migration 前后查询结果；
- 真实 Profile 的 app-server auth/model/tool negative prompts、额度/成本和资源采样；
- 用户对合入发布分支或部署的明确授权及线上低风险验证；仅推送 feature 分支不构成发布授权。
