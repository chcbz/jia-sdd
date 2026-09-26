# 用户名编码完整性与聊天发送者身份治理任务

## 执行规则

- 状态：API/Web 源码实现已完成并推送组件 `develop`；exact-tree 云端/正式构建与生产发布仍待证据，数据治理仍待单独授权。
- 不创建独立 Reviewer；每个 Owner 完成风险自检后进入组件 `develop`，正式测试/构建/制品/部署优先由云效 exact-SHA Run 证明；云效不可用期间按 2026-09-17 本地发布授权绑定 exact SHA、本地测试、生产构建、制品摘要和实际健康。
- 身份/ACL/生产数据任务使用 `critical_worker`；Web 合约冻结后使用 `balanced_worker`；验证使用 `gpt_test_runner`。
- 不覆盖当前脏工作树；实现应使用任务/路径隔离工作树。
- 数据写任务必须在应用新污染阻断上线且获得用户明确生产写授权后执行。

## API（`api/`）

### UNE-A01 OAuth strict UTF-8

- [x] Owner：`critical_worker`
- [x] 路径：`oauth/jia-oauth-service/**/OauthExternalHttpClient.java`、OAuth provider callback tests。
- [x] 将 provider JSON 响应改为 `byte[]`，去可选 UTF-8 BOM，使用 fatal decoder，再解析 JSON。
- [x] 保留事务外调用、明确传输超时、非 2xx 安全失败；不引入普通 API deadline interceptor。
- [x] 日志不包含 body/token/secret URL。
- [x] 覆盖无 charset 中文/emoji、BOM、malformed UTF-8、非 2xx、空 body。
- 依赖：无。
- 风险：P0 外部认证可用性与敏感信息。

### UNE-A02 外部显示名策略

- [x] Owner：`critical_worker`
- [x] 路径：`oauth/jia-oauth-service`、必要的 `user/jia-user-api|service` 窄接口与测试。
- [x] 新增 source-aware nickname decision；合法 Unicode 保留，control/超长/高置信 mojibake 拒绝。
- [x] 已有用户异常昵称保留旧 MySQL/LDAP 值；新用户使用 username/jiacn 展示 fallback。
- [x] 验证重复第三方登录不会重写已修复昵称。
- [x] 不在通用资料编辑路径做无条件转码。
- 依赖：UNE-A01。
- 风险：P0 身份主数据、LDAP 协调。

### UNE-A03 认证人类发送者解析器

- [x] Owner：`critical_worker`
- [x] 路径：`chat/jia-chat-service`、`chat/jia-chat-service/build.gradle` 及相关测试。
- [x] 新增 `ServerResolvedSender` / `HumanSenderIdentityResolver`，只接受 `EsContext` 身份。
- [x] 添加 `user:jia-user-api` 依赖并验证无依赖环。
- [x] `/chat/stream` 对 request `senderName/senderType` 兼容接收、完全忽略。
- [x] Normal chat、内建宋江、Advisor、Juyiting relay、Agent payload、消息列和 metadata 复用同一 resolver 结果。
- [x] 从客户端 metadata allowlist 移除 sender 字段；服务器在最后组装可信字段。
- [x] 高置信可逆旧 nickname 仅内存恢复；不可逆值 fallback，不在请求路径写库。
- 依赖：可与 UNE-A02 部分并行，合入前需冻结共享显示名规则。
- 风险：P0 身份/ACL、跨模块依赖。

### UNE-A04 Agent WebSocket sender authority

- [x] Owner：`critical_worker`
- [x] 路径：`AgentWebSocketHandler`、Agent runtime resolver、WebSocket/security tests。
- [x] 根据已认证 session agentId 解析 runtime.name → personaName → agentId。
- [x] final、delta、持久化和 metadata 使用同一权威名称。
- [x] payload `senderName/agentName` 兼容接收但忽略，spoof 不得进入事件或数据库。
- [x] 与 `AgentTaskThreadCreationTransaction.trustedSenderName()` 收敛为共享规则。
- 依赖：UNE-A03 的 sender contract。
- 风险：P0 Agent 身份与会话隔离。

## Web（`web/`）

### UNE-W01 共享显示名工具

- [x] Owner：`balanced_worker`
- [x] 新增 `src/utils/displayName.js` 与单元测试。
- [x] 顺序固定为 percent decode → raw mojibake strict repair → control strip → trim。
- [x] 替换 UserProfile、JuyiHall、Hall conversation、普通 Chat 的重复 helper。
- [x] 覆盖中文、emoji、合法西文名、percent encoded、raw mojibake、malformed 和已截断不可逆值。
- 依赖：显示名算法契约冻结。

### UNE-W02 自己消息与历史身份

- [x] Owner：`balanced_worker`
- [x] 乐观 USER 消息标记 `isSelf: true` 并显示“你”。
- [x] 停止发送 `senderName/senderType`。
- [x] 历史响应保留服务器稳定 `jiacn`/owner identity，以精确比较判定本人。
- [x] 其他用户/Agent 只显示服务器 senderName；不可逆空值按类型 fallback。
- [x] 覆盖发送、SSE final/delta、刷新恢复、切换身份和旧客户端兼容。
- 依赖：UNE-A03 API contract。

## 数据治理

### UNE-D01 生产只读审计

- [ ] Owner：`critical_worker`
- [ ] 仅在明确授权的只读入口执行 `SHOW CREATE TABLE`、connection charset/collation、nickname/sender_name 的 HEX 审计。
- [ ] 按 A raw reversible、B percent reversible、C irreversible、D normal 分类。
- [ ] 生成受限明细 manifest 与不含 PII 的公开摘要，并固定 SHA-256。
- [ ] 不做 DML、不回读 token/provider secret。
- 依赖：应用候选规则可执行为离线 dry-run。

### UNE-D02 MySQL/LDAP 主数据修复

- [ ] Owner：`critical_worker`
- [ ] 前提：UNE-A01/A02/A03 已发布且验证无新污染；用户明确授权生产写。
- [ ] `user_info.nickname` 按主键 + `BINARY before` CAS。
- [ ] LDAP 使用 assertion/等价条件写；无原生 CAS 时使用精确 read-before/write/readback 和补偿状态机。
- [ ] C 类不可逆项只接受 provider 回读、用户确认或可信身份映射，不自动猜测。
- [ ] 每批 readback；冲突停止该记录；回滚同样 CAS。
- 依赖：UNE-D01、应用发布。

### UNE-D03 聊天历史修复

- [ ] Owner：`critical_worker`
- [ ] 只修 `sender_type='user'` 且 owner/client/旧值精确匹配的记录。
- [ ] `sender_name` CAS；metadata 仅在 `JSON_VALID` 且 `$.senderName` 精确等于 before 时更新。
- [ ] Agent/system 消息排除；不可逆 C 类按已确认主数据映射修复，否则保留并依赖 UI fallback。
- [ ] 记录冲突、readback 和条件回滚结果。
- 依赖：UNE-D02 或已确认的身份映射 manifest。

## 集成与验证

### UNE-I01 exact-SHA 云端验证与发布证据

- [x] Owner：`gpt_test_runner`（验证），组件 Owner（发布结论）。
- [ ] API：OAuth、User、Chat、Agent WebSocket 相关测试；正式 Gradle 构建由云效执行，或在云效不可用期间按本地发布授权经 orchestrator 串行执行。
- [x] Web：共享 helper、Chat/Juyiting reducer 与 UI 定向回归已通过（83 + 5）；正式 Vite 构建仍须由云效执行，或在云效不可用期间完成 exact-final-tree 本地生产构建。
- [ ] 验证普通聊天、聚义厅 relay、Advisor、Agent final/delta、刷新历史、身份切换。
- [ ] 记录 Flow Run、exact source commit/tree、测试摘要、artifact SHA-256、部署顺序和实际健康。当前 CI-only API Run 17/Web Run 9 预执行失败且无 source commit/log，不能勾选。
- [ ] 发布失败即停止，不用本地成功替代云端证据。
- 依赖：UNE-A01~A04、UNE-W01~W02。

### UNE-I02 存量治理验收

- [ ] Owner：`gpt_test_runner` + 数据任务 Owner 自检。
- [ ] 对 manifest SHA、CAS 数、conflict 数、LDAP readback、chat readback、rollback 演练做一致性检查。
- [ ] 抽样不得泄露 PII；公开报告只含分类和计数。
- [ ] 确认数据修复后再次 OAuth 登录、发送新消息不会复发。
- 依赖：UNE-D01~D03。

## 推荐依赖图

```text
UNE-A01 -> UNE-A02 ----┐
                       ├-> UNE-I01 -> UNE-D01 -> UNE-D02 -> UNE-D03 -> UNE-I02
UNE-A03 -> UNE-A04 ----┤
    └----> UNE-W02 ----┤
algorithm -> UNE-W01 --┘
```
