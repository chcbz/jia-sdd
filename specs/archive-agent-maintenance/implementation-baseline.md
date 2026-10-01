# M0 实施基线：典籍阁 Agent 任职与内容维护

日期：2026-09-29。状态：M0 已冻结本机可复现源码基线；业务实现、应用发布、Agent 激活与真实典籍上架仍分别验收。

## 1. 可复现版本

| 仓库 | 分支 | commit | tree | 说明 |
| --- | --- | --- | --- | --- |
| Root SDD | `codex/archive-agent-maintenance` | `01f7599ed28e84c1a44d2cc6c3dec13f7ddbeb67` | `f0c798c01a2703f092a87c83b9d2944d1740b5b3` | D2 文档基线 |
| API | `codex/archive-agent-maintenance-api`（基于 `origin/develop`） | `e15e1a9d947e86e5f81a3288948087466a8a879c` | `d72e0473ede839f9809b73705ccbc8a1af4fb500` | 本轮后端实施基线 |
| Web | `codex/archive-agent-maintenance-web`（基于 `origin/develop`） | `9854173f7f409ca2f1c862eb153b0e3574ee58ff` | `ae226fdb1c41d6239906784373a2a18416d209a1` | 本轮前端实施基线 |
| Client | `codex/archive-agent-maintenance-client`（基于远程 `develop`） | `29fda32acca7a4c4f7a66a4188946853086e6dcb` | `455ba7fdab5def6873084e1bf1d1fde1106bb7ad` | `isp-install` 独立 checkout；截至此基线无特性改动 |

Root 原始 gitlink 为 API `564e50fa6bb4889d6f0b7221de57b4c22116a810`、Web `83d6c738b320d119715acfc53e59fcdb49ebcfa8`。本轮组件开发明确前移到上述最新可复现 `origin/develop`，最终只在组件提交已推送并验证后更新 gitlink。

## 2. 当前源码事实与接入点

- 内容表位于 `chat/jia-chat-mapper/src/main/resources/db/archive-schema.sql`；当前 `archive_work/archive_edition/archive_chapter/archive_paragraph` 已具备 work/edition 结构，但 CHECK 仍要求 120 回和卷首。
- 内容写入使用 `ArchiveContentStore` / `JdbcArchiveContentStore`；工作与版本锁已经有 `lockWork`、`lockEdition`，激活通过 `switchActiveEdition` 与 `markActivated`。
- Archive 事务缝是 `ArchiveTransactions`，生产实现 `SpringArchiveTransactions` 包装同一 `PlatformTransactionManager` 的 `TransactionTemplate`；因此授权、作业、草稿、封存和发布应放在同一数据源事务内。
- Reader 当前在 `ArchiveReaderServiceImpl` 中固定水浒 work、摘要、120 回和统计值；个人数据 SQL 与 `ArchiveTextSelectionValidator` 也需要按 edition/work 通用化。
- 用户通道从 JWT 服务端解析 `jiacn` 与 `client_id`；单租户内容 tenant 保持 `0`，不能从请求体接收 owner/client/tenant。
- native runtime principal 是 `AgentRuntimeAuthentication.Scope(tenantId, clientId, ownerJiacn, agentId, runtimeInstanceId)`；`AgentRuntimeAuthenticationFilter` 使用精确 method/path allowlist、拒绝 Origin 和重复/歧义 header。新增 native 路径必须同步修改 filter 及安全测试。
- Chat service 已依赖 `agent-api` 与 `agent-service`，archive 可调用 agent-api 端口；不得增加 agent-service 反向依赖 chat-service。
- 既有市场技能有效性由 `InstalledSkillEntitlementLookup` 结合订单/安装/权益得出；平台配置技能必须使用独立 origin，不写资金表，不把 abilities 标签视为安装证明。
- 统一命令传输由 `AgentCommandCanonicalCodec`、delivery/outbox/transport 维护；新增命令必须作为新 command type/schema，不修改冻结的 `SKILL_INSTALL` 或 workspace payload。

## 3. 锁顺序与事务边界

统一顺序：`collection/manager grant -> appointment slot -> maintenance job -> execution grant/run -> draft -> work -> candidate edition -> publication operation`。所有需要校验当前授权并写内容的操作在取得对应授权/作业行锁后再锁内容行；禁止先锁正文再反查任职。

- 外部来源读取、模型处理、Agent 命令发送不放在数据库事务中。
- 创建维护单、幂等意图映射与业务 outbox 同事务提交。
- 草稿修改使用 revision CAS；修改后旧 validation 失效。
- 发布事务内重验管理授权/任职/作业发布模式/来源用途/validation revision，并原子写 publication、active 指针、job 状态和 outbox。
- 撤任或授权撤销与发布共享授权/作业锁；先提交者决定结果。撤销提交后不得继续写或发布。

## 4. API 与错误合同冻结

管理端基线：`/archive/admin/v1/**`，仅 JWT 管理者；native 基线：`/internal/archive/v1/jobs/{jobId}/runs/{runId}/**`，仅 `AgentRuntimeAuthentication`。请求体不得含 tenant/client/owner/permissions/runtime/origin/Authorization。

稳定错误 JSON：

```json
{"code":"ARCHIVE_FORBIDDEN","message":"Archive management permission is required"}
```

```json
{"code":"ARCHIVE_REVISION_CONFLICT","message":"Archive revision no longer matches","details":{"currentRevision":"2"}}
```

```json
{"code":"ARCHIVE_VALIDATION_REQUIRED","message":"The exact draft revision must be validated before publication"}
```

HTTP 约定：认证不完整 401；不可见资源 404；权限不足 403；CAS/幂等异内容/active 冲突 409；状态不允许 422。写接口使用 `Idempotency-Key`，CAS 使用 `If-Match: \"vN\"`，读取响应暴露 `ETag`。

## 5. 首轮实现切片与当时缺口（历史；当前见 §14）

首轮源码切片按 D2 的最小增量 A+B 接口边界推进：

1. 通用多书/不可变版本 Reader 与旧水浒兼容。
2. 书库管理授权、单岗位任职/撤任、readiness 投影。
3. 维护单、草稿 revision、确定性校验、显式管理者发布与历史 edition 读取。
4. native 精确 scope 的作业查询/草稿写入/校验请求；不让 runtime 任命或扩大权限。
5. Web 典籍书架和管理面板，所有状态来自 API。

M3 平台安装已有 API 与 Client 局部实现：服务端平台 installation/receipt/reconciler 合同和客户端默认关闭的安全安装 manager、durable journal、原子 no-replace 激活均有测试证据；但 `client_entry_wired=false`，尚未接 InstalledSkillResolver/active-slot、`agent-client` 命令路由或真正执行。`ARCHIVE_MAINTENANCE_EXECUTE`、服务端 dispatch、持久 grant、宋江工具、真实《三国演义》底本、生产管理者/吴用任职、业务发布授权和生产上架仍未完成，不能由局部源码提交推导。

## 6. 验证选择

- 文档：`node specs/archive-agent-maintenance/validate-design.cjs`
- API focused：`:chat:jia-chat-mapper:test` 的 archive schema/store tests；`:chat:jia-chat-service:test` 的 archive content/reader/controller/maintenance tests；涉及 native allowlist 时补 `:agent:jia-agent-service:test` 的 runtime security selector。
- 所有 Gradle 必须串行持锁。当前 Windows 实测使用 `C:\tmp\cyf-gradle.lock`；Linux/Flow 环境使用 `/tmp/cyf-gradle.lock` 或 orchestrator 对应锁。证据必须记录实际锁路径，不因平台差异伪造跳过或通过。
- Web：`npm run test -- --grep archive` 或项目现有精确 Mocha selector；最终按仓库要求 `npm run build`。
- 集成证据必须绑定最终 API/Web/root exact commit/tree；mock UI、客户端 ACK、源码测试均不等于生产发布或真实典籍上架。

## 7. 2026-09-29 本机切片验证与未完成边界

> 本节保留 2026-09-29 当日快照；M3 平台安装的后续进度与当前边界以 §10–§14 为准。

- API 定向验证：独占 `C:\tmp\cyf-gradle.lock` 后执行 `:chat:jia-chat-service:archiveMaintenanceMvp :agent:jia-agent-service:archiveMaintenanceSecurity`，成功。来源映射测试覆盖原始 UTF-8、逐段匹配、遗漏、重叠、乱序和半个码点；发布前再次校验。该测试未使用真实 MySQL。
- Web 定向：`node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter dot tests/archive-reader.test.js --timeout 30000`，82 passing；`npm run build` 成功（存在既有 chunk size 提示）。文件读取、摘要计算与网络响应均以身份 epoch 防旧会话回填。
- Client 仅护栏：`node --test --test-name-pattern='new archive and platform commands cannot fall through' test/agent-client.test.mjs`，1 passing；真实平台安装和典籍命令仍明确拒绝，不能称为 Agent 已执行。
- 草稿严格来源合同见 `design.md` §7.5。所有排除文本只有理由和字节区间，缺人工审阅时不能证明未漏章。来源存储默认关闭；真 MySQL、迁移断点/并发、HTTP/E2E、M3 安装证明、M4 事件/outbox、M6 bridge、M7 宋江工具均未完成。四仓尚未提交/推送；不更新 `integration.yaml` pins 或 `accepted/released` 状态。

## 8. 2026-09-29 事件与管理身份隔离增量

- 新增 `archive_event` 的每作业事务内序号与 `GET /archive/admin/v1/jobs/{jobId}/events`；创建作业、草稿修改、校验、人工发布各写事务内追加事件。事件的 `outbox_state` 仅为 `PENDING`，无投递 worker，不能据此宣称可靠通知已收敛；事件页目前仅为管理端轮询。
- 校验通过/失败会将 job 分别推进 `AWAITING_PUBLISH`/`NEEDS_CHANGES`；Web 校验后刷新作业快照且保留本次结果。需要补的 native start/failure/grant、取消/移交、安装与执行 bridge、宋江工具仍不变。
- 管理端对作业单项读写、事件与任职撤回重新核对 tenant/client/owner，列表在 SQL 按同 scope 过滤，避免仅有同书库管理授权便浏览或修改另一 owner 的维护单；新增同书库跨 owner 负向回归。
- 私有来源上传改为先在数据库预留 `PENDING` 幂等操作与 sourceId，再做外部对象写入，最后事务内提交来源/操作。相同 key 的已提交重放不重复写对象；中断后同 key、同摘要可恢复相同 sourceId，异内容在对象写入前冲突。仍缺对长期未恢复的预留对象执行有界清理与真实 MySQL 并发验证。
- 本机独占 `C:\tmp\cyf-gradle.lock` 后 `:chat:jia-chat-service:archiveMaintenanceMvp :agent:jia-agent-service:archiveMaintenanceSecurity` 成功；修改隔离和来源预留后再次单独运行 `:chat:jia-chat-service:archiveMaintenanceMvp` 成功（最后一次 `--quiet`，退出码 0）。Web 定向 Mocha 82 passing 与 `npm run build` 成功，Client 定向护栏测试 1 passing；真实安装/执行未实现。四仓 `git diff --check` 无空白错误（Git 提示未来 LF/CRLF 转换）。本机单元/build 不代替真实 MySQL/HTTP/Client 端到端验收。未提交/推送，也未更新 integration pins。

## 9. 2026-09-30 作业取消与操作读回切片

- 管理端新增 `POST /archive/admin/v1/jobs/{jobId}/cancel`：`job.manage` + `Idempotency-Key` + 作业 `If-Match`，同事务把运行记录置 `FENCED`、作业置 `CANCELLED`、追加 `JOB_CANCELLED` 事件；已发布/已取消拒绝新取消，取消后管理及 native 写入/发布失败。Web 提供明确原因与取消按钮，刷新真实状态。
- 新增 `GET /archive/admin/v1/operations/by-key`（`Idempotency-Key` 请求头），仅当前 JWT actor 和相应书库权限读取规范 admin 操作的 `PENDING/COMMITTED` 状态及目标引用；native 路径不通过此用户入口。查不到返回 404，仍不代表另一个尚在途、未提交的 POST 一定没被受理。来源先预留的 `PENDING` 可读。
- 默认管理 grant 的权限补 `source.prepare,job.manage`；现有已写入 DB 的旧 grant 不因配置默认值改变自动扩权。
- 本机独占 `C:\tmp\cyf-gradle.lock` 执行 `:chat:jia-chat-service:archiveMaintenanceMvp :agent:jia-agent-service:archiveMaintenanceSecurity --quiet` 成功；随后操作读回单独 `:chat:jia-chat-service:archiveMaintenanceMvp --quiet` 成功。Web 权限变更刷新会清理失权后的任职/维护单/草稿缓存；最后一次定向 82 passing 和 build 成功。API 定向 28 tests、0 failures。仍未做真实 MySQL/HTTP、并发/掉线、实际 Agent 安装执行与正式上架；此切片不构成整体验收或推送条件。

## 10. 2026-09-30 当前冻结源码与验证证据

以下均为局部源码测试，不是 84 项业务 acceptance，也不是 release pin。证据原件保存在 [evidence/2026-09-30](/home/isp/wsps/cyf/specs/archive-agent-maintenance/evidence/2026-09-30)。

- API 基于 commit `e15e1a9d947e86e5f81a3288948087466a8a879c`，prospective worktree tree `7d61d50e9a262eeb43bc8cc9ab77763bd9cec27b`，不是 commit。平台 48、native security 6、maintenance 31，合计 85 项定向测试通过。archive regression 最终 195 tests、12 fail、3 skip；12 个失败方法与 exact baseline 集合一致，failure delta 为空，既有失败未隐藏。原 comparison 文件记录加入最终 wiring test 前的 194-test 快照，最终汇总 JSON 为权威计数。
- API Spring 小切片为 `PlatformSkillInstallationService` 与 `ArchiveMaintenanceServiceImpl` 的 production constructor 加入明确注入选择，并用真实 `AnnotationConfigApplicationContext` + mock dependencies 做无 DB bean 装配。Raman 复审 ACCEPT，无 P0/P1。
- Client 当前 base/HEAD `dce79be2d8f919a7a2449c6c576f4e3e0c183a20` 为本地未 push commit，且 worktree 有 dirty；prospective tree `a3ea0078fd11feb1fa25d4ca4109bc4231b57b45` 不是 commit。隔离 Alpine chroot（Node 24.18.1/Python 3.12.14）246/246 tests 通过，0 fail、0 skip；8/8 冻结 source/log digest 已由复审核验。Raman 最终 ACCEPT，无 P0/P1。
- Web 基于 commit `9854173f7f409ca2f1c862eb153b0e3574ee58ff`，prospective tree `e7d4cc80afcccb0acb4c33a209763c7d52052f43`，不是 commit。archive tests 82 通过，`npm run build` 通过；未部署。
- 2026-09-30 根 spec 本轮 validator 已由主线程运行通过；`verification.documentation.status=passed_static_self_check`。validator 生成新的 `documentation-check.json`，但该自检不运行应用测试，只验证文档、冻结源码对象和上述证据声明。

## 11. M3 平台安装 P1 收敛与安全边界

### 11.1 服务端 receipt timeout、扫描与装配

- delivery ACK `SUCCEEDED` 不再被当作 native result。若 result receipt 已 committed，status/reconciler 精确 replay 优先；否则 `REQUESTED + resultSha=null + SUCCEEDED` 在 `expiresAt` 前保持等待，到期后在锁内持久化固定 `PLATFORM_SKILL_RECEIPT_TIMEOUT`。status 与 reconciler 共用同一判定，fencing/结果先提交有定向覆盖。
- terminal delivery reconciliation 使用 bounded keyset cursor。单条坏记录失败仍推进扫描，后续轮次绕回，避免固定头部 100 条饿死后续健康候选。新增普通 `(state, created_at, installation_id)` 扫描索引，schema contract 仍严格检查原 unique/type/prefix/extra。
- `PlatformSkillInstallationService` 和 `ArchiveMaintenanceServiceImpl` 的生产构造选择均由 Spring context 测试覆盖；mock 单测不再是唯一装配证明。尚无真实 DB migration/E2E。

### 11.2 Client durable deadline、恢复与原子激活

- validated command 持久保存 immutable `issuedAt/expiresAt`。fetch、body、result POST 使用 AbortSignal 与 bounded wait；即使注入的 helper 不尊重 signal，manager 也不会永久挂起。下载完成后、PREPARED 前和 rename/激活前重验 deadline，过期禁止新激活。
- 本地 success result 在 POST 前持久化；响应丢失或重启只精确重放原 attempt/epoch/body，不重新下载或安装，也不把旧 success 改写成新 challenge receipt。receipt replay 仅在有限 grace 内尝试；超出期限返回稳定脱敏 `failureCode/recovery_required`，不输出 raw I/O 错误。
- journal create-once 使用同目录 temp、文件 fsync、atomic no-replace 和目录持久化，避免 `wx` 直接写最终 JSON 留半记录。PREPARED 恢复校验真实 regular、非 symlink 的 `SKILL.md` 摘要，并把 expected parent/staging inode identity 传给共享原子 helper；parent/target race 失败关闭。
- 安全解包拒绝路径穿越、symlink、重复项、身份/摘要不符和超限包。Linux 原子激活优先 `libc.renameat2`；musl 无导出时仅对 x86_64 syscall 316、aarch64 syscall 276 精确回退，未知架构仍 `UNSUPPORTED`，不降低 inode/owner/no-replace 检查。
- 物理目录为 `skills/platform-provisioned/<scopeDigest>/archive-maintainer/1.0.0/<installationId>`。同 CODEX_HOME 的新 runtime/scope 或同 scope 的新 installationId 使用独立不可变目录；旧 target/marker/inode 不覆盖，旧 scope proof 不可被新 scope 复用。目录枚举不能作为安装资格。

## 12. 前次冻结缺口、P2 与下一接入（历史；当前见 §14）

- Client 平台 manager 保持默认关闭，`client_entry_wired=false`；没有修改 `agent-client.mjs` 路由或能力声明，没有真正执行安装。服务端平台合同与客户端 manager 之间尚未进行 live HTTP/transport 集成。
- grant、dispatch、`ARCHIVE_MAINTENANCE_EXECUTE`、Client execute、InstalledSkillResolver/active-slot、M7 宋江工具、真实 MySQL/迁移、HTTP/E2E、生产制品/Flow 与业务激活仍缺失。84 项 acceptance 全部 `not_run`，integration pins 全 null，release `not_started`。
- 保留 P2：installationId 物理完整副本目前没有容量配额和受控回收策略。启用入口前必须按安装事实、scope 和引用证明设计有界回收；不得自动覆盖/递归删除旧 scope，也不得用目录扫描推导有效安装。
- 当前 ACCEPT 只覆盖上述 API Spring 小切片与 Client M3 安全切片的 review；不表示完整功能投产、Agent 任职可用、真实内容发布或整体验收通过。


## 13. 2026-09-30 InstalledSkillResolver 首轮测试与 REJECT 快照（已由 §14 收敛）

- 新增统一只读 origin resolver、平台 exact success/pending 查询和任职 additive `skillReadiness`，MARKET 缺 adapter 返回 `UNAVAILABLE`。无 dispatch、状态修改或 scope lock；任职仍 `executable=false / EXECUTION_NOT_WIRED`，作业/native 写门禁未解锁。
- 首次 tree `682a78e75ff56949276c7634a7cb07b45a97177b` 的平台 60/native 6 通过，但 Chat 因测试 import 错误未编译；原始失败日志保留在 `evidence/2026-09-30/resolver-stage2/attempt1/`，没有把旧 XML 记作新通过。
- 仅修正测试 import 后，tree `f88f5125ae99d345a544ef8d1fa929055be1e14a`（prospective tree，不是 commit）真实持锁验证：平台 60/native 6/maintenance 34，全绿共 100；完整 archive 198 项，12 fail、3 skip，失败方法与 exact baseline 完全相同，新增/减少失败集合均为空。19 个切片源文件的 Git blob/bytes/SHA 和 56 个 XML 已保留。
- Raman 独立只读 verdict **REJECT**：历史 fallback 未限定 binding/runtime/registration，可把旧 binding 引用作为当前 REVOKED proof；另有 null 引用校验与历史排序索引两项 P2。原 verdict 保存在 `resolver-stage2/review-attempt2.json`。当时唯一 writer 进入修复；后续重新冻结/验证/复审已记录在 §14；100 项源码测试通过不覆盖该 P1，也不证明真实 MySQL/HTTP/E2E。
- 当前 grant/dispatch、Client entry/execute、M7、业务验收与推送仍未完成。旧 §10–§12 为历史冻结证据；本节记录 resolver 后续切片，不覆盖旧证据或 source-audit。

## 14. 2026-09-30 InstalledSkillResolver exact-proof 修复冻结与局部 ACCEPT

- 最终冻结 tree `67dc1c225a1cc020f5c68b44b992a6f329dc1a01`，仍是 prospective worktree tree，不是 commit/pin。证据保存在 `evidence/2026-09-30/resolver-stage2/attempt3/`，不覆盖首轮编译失败、attempt2 REJECT 或原 stage1 日志。
- 当前 identity/binding/runtime/registration 验证先于任何 store 查询；不能验证则 `UNAVAILABLE` 无 proof。success、pending 和 history 全按 exact ResolutionKey 查询并防御性重验，旧 binding/runtime/hash 不会作为当前 REVOKED 安装引用返回。catalog 撤销只作用于当前 exact 安装事实。
- 显式拒绝 null canonicalAgent/installationRef，补齐 history 等值范围与排序的普通索引；保留严格 unique/type/prefix/extra/schema 合同、success 优先、无 scan 真相裁剪、只读/默认关闭边界。
- 主线程真实独占 `C:/tmp/cyf-gradle.lock` 四个 task：平台 63/native 6/maintenance 34，共 **103 定向测试通过**；完整 archive **198 项，12 fail、3 skip**。失败方法集合与 exact baseline 完全一致，introduced/removed delta 均为空。整体 Gradle 为 `BUILD FAILED`（既有 12 项），不能称为全量构建成功。
- Raman 独立只读局部 **ACCEPT**，原 1 P1/2 P2 已收敛、无新 P0/P1/P2；19/19 当前 Git blob、冻结 tree 和 source proof 一致，独立解析 56 XML 与汇总一致。日志 SHA-256 `8e719d8413a6dc763c20d823beeb76bc01300cef05bbe940fb151f47bb40418f`。该 verdict 仅接受 resolver 切片。
- 旧水浒 manifest/golden 字节摘要仍为 `fe2c1cfd551e29ebc70665b121bf3480d1941728d8fa0cd0fa3f68d584335210` / `a601e36874fa04b5425a391d34d228e7aa2cffbeea6c6db16afcaf88d8696a1d`。Web/Client 此轮未改，旧冻结证据保持。
- 任职 projection 仍 `executable=false / EXECUTION_NOT_WIRED`，原 overall readiness/作业 WAITING_SKILL/native writable gate 不解锁。grant/dispatch、执行 active-slot、Client entry/execute、M7、真实 MySQL DDL/EXPLAIN/迁移、并发换绑、HTTP/E2E 与生产/业务验收仍未完成；84 项 not_run、pins 全 null、release not_started。本轮没有 commit/push 或生产操作。

- Root validator 已加入 attempt3 源码/日志/XML 摘要与计数合同，主线程实际通过；隔离 unchanged control 通过，伪 accepted、隐藏 baseline 失败、篡改 source proof/XML/log 均拒绝。对应 `resolver-stage2/validator-negative-final.json`。这些是静态证据自检，不运行应用测试；Windows 临时文档副本保留在 C:/tmp，本轮未绕过前轮 junction 清理拒绝，也未删除真实 Client 源码。

- Root 后续独立复审指出一项 P2：最终 review 与 integration nested local ACCEPT 尚未由 validator 强制绑定（当前内容本身真实，API 局部 ACCEPT 不变）。原 verdict 见 `resolver-stage2/root-validator-review-attempt1.json`；仅修补静态证据校验，未重写应用测试结果或启用 execution。

- 最终 validator 已强制绑定 review-final SHA、exact local scope/统计、显式 DB/E2E/overall/native=false 与 integration nested verdict/tree/evidence。主线程 8 项隔离控制/负向均完成：控制通过，nested 伪整体 ACCEPT 与 review 整体验收伪造及既有篡改均被拒绝；最终 validator SHA `b057c35b6d743777c7d27d551b7bb5b3ec5eb8b8fe833aa8999bcf0729355db3`。旧 validator 负向记录另存，未改写 API 原始测试结果。

- Raman 最终只读复审确认 Root validator P2 完全收敛，局部 ACCEPT、无新增 P0/P1/P2；脱敏回执见 `resolver-stage2/root-validator-review-final.json`。该结论只覆盖静态 validator，不改变 API resolver 局部范围或整特性状态。

## 15. 2026-09-30 隔离真实 MySQL 首轮验证与执行授权接入中

- 主线程在 `C:/tmp/aam-mysql-20260930` 使用官方 MySQL Community 8.4.5 Windows 可移植包建立仅监听 `127.0.0.1:34061` 的独立测试数据库；没有修改全局服务、Docker 配置或生产数据库。临时测试认证只保存在本机隔离目录，未复制到仓库证据。
- 对冻结 `67dc1c225a1cc020f5c68b44b992a6f329dc1a01` 的内容/维护/平台 DDL，真实执行均 exit 0。随后使用上一轮已编译类和冻结 resource 运行 JDBC probe：**14 checks，11 PASS、3 FAIL、0 skip**；不是 Gradle suite 或 HTTP/E2E。原件见 `evidence/2026-09-30/mysql-stage3/attempt1/`。
- 已证实 exact store 查询：1001 条更新失败不遮蔽旧合法成功；binding/runtime/registrationHash/owner/digest 隔离、历史排序、真实唯一键与 CHECK 强制均通过。
- 三处真实启动缺陷已交给唯一 writer：迁移资源末尾空白 segment 误判语句数；维护表外键 supporting index 由 MySQL 自动生成但严格合同未列入；平台 CHECK metadata 中 escaped quotes 未正确规范化。修复后须重新编译、真实 MySQL 与独立复审，不覆盖 attempt1 失败。
- 唯一 writer 正在接持久 execution grant、既有 command transport 派发及 native 精确授权；尚未冻结/验证。Client execute、M7、业务验收、组件 commit/push 仍未完成。

- 同一隔离库还通过实际 JDBC query builder 执行三条 `EXPLAIN FORMAT=JSON`；success/pending/history 在当前 fixture 均无需 filesort，history 使用新 exact 范围索引。原始 plan 保留在 `mysql-stage3/attempt1/frozen-jdbc-explain.log`；小 fixture 计划不是生产性能承诺。

## 16. 2026-09-30 execution 首轮冻结、源码测试与真实启动残余

- 唯一 writer 已冻结 API prospective tree `aa2e416622d5c758fa121e745b593bf2a7f2303e`（不是 commit/pin），相对 resolver tree 有 31 文件增量；已增加 execution port/Agent adapter、持久 run/grant、管理员 execute、controlled dispatcher、native exact command/attempt/epoch/grant 头校验和撤任/取消 fencing。默认 `archive.maintenance.execution-enabled=false`，Client/M7 未接，不宣称可执行。
- 主线程独占 Gradle 锁，实际编译通过；平台 66、native 6、maintenance 41 共 **113 定向通过**。全 archive **206 tests / 12 fail / 3 skip**，失败方法与此前 exact baseline 一致。整体仍 `BUILD FAILED`；31 Git blobs/SHA、原 XML、日志在 `execution-stage4/attempt1/`。
- 使用新已编译类和该树资源重新执行真实 MySQL probe，**14 checks / 13 PASS / 1 FAIL / 0 skip**。内容 schema 与平台 schema 重复初始化已通过；维护 schema 仍因真实 CHECK 等价渲染不匹配启动失败。四处差异原件在 `mysql-stage3/attempt2/current-jdbc-check-metadata.log`；不得通过删除任意括号或忽略未知约束降低严格校验。
- 另开启旧 H02/H03/H05A 的安全 opt-in MySQL 回归（guard 不改），**206 tests / 15 fail / 0 skip**。三项原先 skipped 的真实测试现暴露失败，不属于已验证的旧 12-failure 集合：H02 fixture 缺维护 schema 的 collection_work 表；H03/H05A reader-data catalog 的 single-tenant CHECK 名与真实 DDL 不一致。原 XML/日志另存 `execution-stage4/attempt1-real-mysql/`，不覆盖默认环境的 12-failure 记录。
- 独立 reviewer 正在只读审查该树；尚无 execution slice ACCEPT。真实跨域锁序、DB/HTTP 执行 E2E、换绑并发、Client execute 和 M7 仍须接入验证。代码未 commit/push；84 业务验收仍 not_run，pins 全 null，release not_started。

- Raman 首轮独立只读 verdict **REJECT**（4 P1 / 2 P2，无 P0）：维护 CHECK metadata、reader-data CHECK 名、跨域 identity/manager 反向锁序、manager revision 未绑定、撤任 RR 旧 snapshot、H02 fixture 初始化依赖。回执在 `execution-stage4/attempt1/review.json`。唯一 writer 已收到集中修复清单；尚未重新冻结/验证，不改变历史 resolver 局部 ACCEPT。

## 17. 2026-09-30 execution 修复复测与真实 MySQL 回归

- 最新冻结 API prospective tree `57fad153289a06d512c53a10cb39d410dee44e44`（不是 commit/pin）。生产实现已拆分 Agent 根锁快照与 transport 写入；持久 job/grant/command 加入 manager authorization revision 并在 native/dispatch 重验；撤任扫描使用锁定 current reads。配置 `seedManagerGrant` 仍是 INSERT IGNORE，配置收敛语义和真实双事务竞争仍待独立复审/后续实现，不能写为全部风险已收敛。
- 维护 CHECK 的四处真实 MySQL 渲染差异、reader-data CHECK 名与三个实库 fixture 的 maintenance schema 前置均已修。对树 `92497fc6f87a027b92dddbbdcf0717b23063bb22` 的新隔离库，content/maintenance/platform create→inspect→repeat、exact resolver 及 DB 约束全部 **14 PASS / 0 FAIL / 0 skip**；原件在 `mysql-stage3/attempt3/`。此 probe 使用当时编译类和冻结 DDL，不冒充最新整树的端到端执行。
- 主线程真实实库继续暴露 `ensureLegacyPublication` 的 SQL 占位符少一项，三个 importer 均报 `Parameter index out of range (7 > number of parameters, which is 6)`，已补第七个占位符；原失败在 `execution-stage4/attempt2-real-mysql/`。不是 fixture 错误，生产路径同样需要此修复。
- Native 撤任单测原先提前命中 default-disabled bridge；现显式配置 enabled、有效 port/root snapshot 与撤任后的空 slot，保持 `ARCHIVE_ASSIGNMENT_CHANGED` 断言，使测试真正走到撤任校验。H03/H05A SQL fixture 改为 tenant=0 **并保留 owner 条件**；H05A 从隔离 DB 取得一次固定测试 clock，避免历史 2026-08-22 固定时刻导致 expiry 早于当前 DB created_at。没有放宽 CHECK 或认证规则。
- 主线程独占 `C:/tmp/cyf-gradle.lock` 在最终树实际运行四 task，平台 **66**、native **6**、maintenance **43** 全绿，合计 **115 定向通过**。完整 archive **208 tests / 11 fail / 0 skip**；H02、H03、H05A 三个真实 MySQL 测试均 PASS。基线失败差异 **introduced=[]**，修复并移除原 reader-data catalog 一项，剩余 11 项为原 baseline；整体仍 `BUILD FAILED`，不称全量回归通过。
- 原源码 Git blob/SHA、完整 XML、日志和失败集合比较在 `execution-stage4/attempt4-real-mysql/`；attempt2 的新增 fixture 失败、attempt2/attempt3 实库失败均单独保留，未覆盖失败证据。115 源码测试与三个旧域实库测试不等于真实 Agent/HTTP/WebSocket/跨组件业务执行。
- 独立 reviewer 正在审最终冻结树；未获该 execution 切片 ACCEPT。Client entry/execute、M7 宋江工具、AUTO 业务发布/恢复、84 项业务验收、组件提交/远程推送与生产发布仍未完成。execution 默认关闭，pins 全 null，release not_started。
- Raman 对 57fad153 树完成独立只读复审：**REJECT，3 P1 / 3 P2，无 P0**。撤权依赖在线目标、manager revoke 无授权先锁 foreign target、配置移除/权限变化不能收敛是 P1；expiry replay、撤权 operation receipt、旧 maintenance schema 升级未验证为 P2。脱敏回执在 attempt4-real-mysql/review.json。已交唯一 writer 集中修复并补真实 RR 双事务测试；源码尚在变更，未复测、未推送。

## 18. 2026-09-30 管理授权生命周期及真实 RR 并发复测

- API 冻结 prospective tree `ae12d17a381976a26e7150f573a80b242005ebed`，测试前后 tree 相同，仍非 commit/pin。新增显式配置 authorizationRevision、删除/变化/受控重新授权收敛和 operation 审计；持久 Agent 根锁与正向 controlled admission 分开；撤权只处理 exact actor scope 的 run；expiry replay 及撤权回执路径补齐。
- 原失败保留：attempt5 的新测试 `SHA` 名称遮蔽导致 Chat 编译失败（不复制旧 Chat XML）；attempt6 的两处未适配新 current-read/补偿行为的 mock 夹具失败。仅修测试夹具后 attempt7 完成持锁复测，日志/XML/source proof/baseline comparison 在 `execution-stage4/attempt7-real-mysql/`。
- 平台 67、native 6、maintenance 52，共 **125 定向测试通过**；archive **217 tests / 11 failures / 0 skips**，introduced=[]。整体 Gradle 因 11 既有 baseline failure 仍 BUILD FAILED。两项真实 MySQL REPEATABLE READ 测试（Agent-root→manager 锁序、ensure 提交后排队撤权 fence 新 grant）及 H02/H03/H05A 均 PASS；并发测试使用 SQL-locking Agent port double，不冒充真实 Agent Runtime/HTTP/WebSocket。
- 配置 v1 所有 manager rows 由配置引导，未新增 API grant 创建入口；旧/同 revision 配置不会复活 API revoke 后授权，更高显式 revision 才能重新授权。此实施从未执行生产部署；任何曾创建早期 maintenance 草案表的环境仍需要发布前单独确认/升级，fresh schema 测试不是旧表升级证明。
- 独立针对先前 3 P1 / 3 P2 的复审仍待回执。Client entry/execute、技能 parser/check/schema、M7、AUTO/lease release、HTTP/WebSocket 集成、84 业务用例及完整提交/推送仍未完成。执行默认关闭，pins null，release not_started。

## 19. 2026-09-30 历史 binding fence 收敛与 M5 开始实施

- 对 ae12d17 的复审指出最后一项 P1：旧 binding 已退休而当前 runtime projection 已迁移时，Adapter root lock 仍拒绝，导致旧 run 无法 fence。仅将持久历史身份校验与当前 projection 正向校验分离并增加回归，最终 tree `b6fb79b46eeafdb55d57fce3d081a954bd71ade3`。
- attempt8 无终态回执，未使用旧 XML；attempt9 隔离 MySQL 进程停止导致五项实库连接拒绝。仅恢复本任务 `C:/tmp/aam-mysql-20260930`、loopback34061，未碰全局服务或其他数据库；两次失败证据分别保留。attempt10 在最终 tree 前后不变时持锁复测：平台68/native6/maintenance52，**126 定向全绿**；archive217/11baselinefail/0skip，introduced=[]，两 RR 加三旧域 MySQL 测试均 PASS。整体仍 BUILD FAILED，不记成全量构建通过。
- Raman 最终独立只读 **ACCEPT local execution slice**，无剩余 P0/P1/P2，回执 `execution-stage4/attempt10-real-mysql/review.json`。不是 HTTP/真实 Runtime/WebSocket/E2E/整体验收；已有草案 maintenance 表的升级仍需发布前另行核实。
- 唯一 source writer 已交接给 Hopper（balanced_worker）实施 **M5 approved deterministic parser/check/schema/fixtures 与固定 ZIP 包**。此前 Shannon handle 已不存在，未启动重复 writer。Main 只维护协调证据，不编辑 API 源码；未 commit/push。下一 M6 仍是现有 WebSocket runtimeAuth + 受控 native bridge，随后 AUTO/lease release、M7、Web 接线及完整集成。

## 20. 2026-09-30 M5 确定性技能包与 Client 测试环境

- M5 已实现固定 `plain-text-v1` UTF8_EXACT_V1 解析/纯字节诊断、精确 BOM/换行/空白排除、章节编号与恶意正文数据化、固定资源 STORED ZIP 和跨 Node/Java golden。首轮真实验证暴露 Catalog 测试字面量换行编译失败；独立复审同时确认本地重复 blockKey 检查与 package schema key/type 合同缺口。失败源码树 `1f9dcf5788f902d3c9cee228b4084af8378deb4c` 和原始日志保留于 `execution-stage4/m5-attempt1-real-mysql/`，未使用旧 platform XML。
- 集中修复后 API prospective tree `889f63ac33251e85c288e945c339c9e4f4a48582` 在测试前后相同。Main 实跑 Node **14/14**；持锁实库 Gradle 平台69/native6/maintenance54，**129 定向全绿**，archive **219/11baselinefail/0skip**，introduced=[]。整体仍 BUILD FAILED/exit1，不称全量构建通过；原件在 `execution-stage4/m5-attempt2-real-mysql/`。
- 实际编译 Catalog 导出的 ZIP **40563 bytes**，SHA `8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081`，与 external approved constant 相同；manifest 无自引用包摘要。1.0.0 尚未发布/激活，最终冻结后资源变化必须走新版本/新安装，不能复用旧 in-flight digest。Raman 最终只读复审关闭原5项发现，无剩余P0/P1/P2（仅M5包），回执 `m5-attempt2-real-mysql/review-final.json`。
- Main 建立本任务专属 Alpine 3.22.6 chroot（Docker Desktop WSL，`/dev/shm/cyf-aam-m6-test-20260930`），仅测试 runtime，未改全局服务。冻结 Client tree `a3ea0078fd11feb1fa25d4ca4109bc4231b57b45` 的四 selector 首轮246/1fail为缺 bash；只在隔离 chroot 安装签名 bash APK后同源复跑 **246/246 PASS，0skip**。两轮原件在 `m6-client-stage5/baseline/`，不冒充入口或 HTTP E2E 验收。
- M6 必须修旧安装器仅接受根 SKILL.md 的限制，改为固定19资源/逐文件证明，再接 server ACK scope、现有 durable inbox 与受控 bridge。Archive runner、AUTO/lease release/重连 epoch、M7、Web 与端到端业务验收仍未完成；未 commit/push，pins null，release not_started。

- M6 下一切片唯一 writer 为 Knuth（critical_worker，01a0f28f-ec2c-7c21-98c0-24b726eced69），只写 Client worktree，先落实完整包证明/server ACK scope/安装入口及断线拒绝，再接 archive runner。Main 保持协调/冻结测试，不与 writer 竞写。
- Client 全量冻结基线额外运行 `npm test`：407tests/398PASS/9FAIL/0skip。隔离环境先补 Git/coreutils 和 task-only entropy mount，原环境失败日志全部保留；最终9失败为1项已有 session-map 测试断言、8项原 Git shell CRLF 导致的 installer失败（含嵌套用例）。不修改基线源码消除失败。当前 writer 必须针对实际安装路径规范 `codex_ws_agent_install.sh`/`common.sh` LF并补新模块打包证明，非全仓换行重写。

## 21. 2026-09-30 M6 Client 安装入口首轮 Linux 冻结实测

- Knuth 已完成本切片 source freeze：完整固定 19 文件安装证明、server ACK native-runtime-v1 scope、process-memory token、真实 Linux atomic bridge 探测、既有 inbox 的注册→恢复→权威重整→drain 接线、socket/generation fencing，以及三个新模块的安装器打包。Archive execute 协议仍不宣告，未启用 shell/Codex fallback。
- Main 使用外部临时 index 冻结 Client prospective tree `93bcb0a29afa5b33607e48469be2fecb2c984470`，git archive 原字节到本任务 Alpine chroot，实际 bash syntax、npm ci 和 full npm test；测试后独立重算 tree 相同。原 source/blob/bytes/SHA、完整 TAP、exit1 与 baseline delta 在 `evidence/2026-09-30/m6-client-stage5/candidate1/`。
- 实测 **425 tests / 415 PASS / 10 FAIL / 0 skip**。原 8 项 installer CRLF 失败已消除，保留原 session-map 断言失败；新增 9 个失败 key（含嵌套父项）涉及 PREPARED/目标竞争/过期的 unknown 对 recovery_required 断言及旧 SKILL.md fixture。不能将失败认作通过；须由唯一 source writer 在独立只读审查集中回执后修复并重新冻结。
- Raman 正在针对实际冻结 patch 作独立只读审查。服务端 registrationHash 轮换拒绝旧命令时仍明确 unknown，未宣称 restart/reconnect 全解锁。Archive runner/start/failure/result/AUTO/lease-release/resume/new-epoch、M7、Web 接线和真实 HTTP/WebSocket/业务集成尚未完成；84 项业务 not_run，pins null，release not_started，未 commit/push 或生产操作。

- Raman 对 candidate1 给局部 **REJECT**：1P1（manager unknown 被 processor 默认 completed/SUCCEEDED，缺 receipt 时错误终结 inbox）与1P2（reconciliation 已 fail-closed 仍可能对外 ONLINE）；旧 SKILL.md literal 另列测试问题。回执 `candidate1/review.json`。Knuth 为唯一 source writer 集中修复 execution-facing nonterminal 状态、processor 状态白名单及注册 readiness，补真实 processor 路由回归；没有将失败测试只改断言伪绿。

- Candidate2 精确冻结 `78b7702171e8d6e7283f871e5863d6e993959952` 实测427/425PASS/2FAIL/0skip，P1 processor 路由及 P2 readiness 回归已通过，残余新增失败为 disabled command-only replay 的陈旧 unknown 断言。随后只改该断言一行；candidate2 后置 tree 检查在授权这项修改后才采集，故如实记录 unchanged=false，不伪造前后相同。
- 最终 candidate3 `273f8e64c5321839671d52a846168d6385aecb55` 由 Main 原 Git archive 在隔离 Linux 完整运行：**427 tests / 426 PASS / 1 FAIL / 0skip，exit1**。前后独立 tree 相同；introduced=[]，保留1项原 config-runtime session-map断言，原8项installer失败消除。原TAP/log/exit/source proof与baseline delta在 `m6-client-stage5/candidate3/`。没有修改无关baseline来造全量通过。
- 最终修复保持仅明确 completed/failed 可终结；unknown/undefined及执行面对的未确认安装进入既有 recovery_required，不产生 SUCCEEDED/work.result。注册仅在 real reconciliation.reconciled=true 且无failClosedCode时ready/ONLINE/drain。Raman正在独立核对candidate1的1P1/1P2收敛（仅四文件delta）；仍不等于HTTP/E2E/整项验收。下一server native lifecycle任务已准备于本机临时目录，须在当前审查闭合后明确转移唯一source writer。

- Raman 最终局部 **ACCEPT** 绑定 candidate3 tree，原1P1/1P2及陈旧SKILL断言均闭合，该四文件修复未见新增P0/P1/P2；原回执 `candidate3/review-final.json`。范围仅M6安装入口及其修复，仍不代表archive runner/new-epoch/M7/真实服务端HTTP/runtime/E2E或整体验收。

## 22. 2026-09-30 native 执行生命周期接入中

- M6安装入口review闭合后，唯一source writer明确转交Knuth到API，Client/Web冻结。下一有界切片为真实native start/failure/result、精确run状态及生产者写权终结、DRAFT_ONLY校验成功后的人工等待/既有执行占用释放；API尚在实施，未冻结/实测，不提前宣称端点可用。
- Main只维护协调/证据并负责持锁Gradle、隔离MySQL验证。仍须继续AUTO发布、显式resume/new epoch及重连fence、Client确定性runner、M7三项受限工具/直达入口、Web接线和真实跨组件验收；无新队列/经济改动或生产激活。组件未commit/push，业务84项not_run、pins null、release not_started。

## 23. native 生命周期首轮真实验证（尚未通过）

- Knuth已SOURCE FREEZE：prospective API tree `a802077d35b9b2c64c7f10f88d5fdeeea52e5a74`，相对M5批准tree为18文件增量。新增精确native start/failure/result、RUNNING/COMPLETED/FAILED与READ_ONLY grant，DRAFT_ONLY成功校验终结生产者并转人工等待；默认execution-disabled。Main前后独立tree一致，没有在验证途中授权改码。
- Main持`C:/tmp/cyf-gradle.lock`强制重新运行四套测试；实际依赖编译通过。platform 69/69、native security 6/6；maintenance 59项/2失败；archive 224项/16失败/0skip、exit1。较M5新增5个失败key，均为真实MySQL初始化`archive_job_run.checks`不匹配；保留原11回归失败。原log/XML/source proof、增量diff及直接M5对照在`evidence/native-lifecycle/native-lifecycle-attempt1/`。
- 在原隔离MySQL的disposable数据库创建、读取、删除本任务CHECK探针，证明新lifecycle DDL未显式给IS NULL/等号谓词加括号，而MySQL metadata自动加括号；现有规范化保留谓词括号，expected/actual不相等。这是新鲜schema检查失败，不能用mock单行parser通过、删除validator或清理旧schema解释为成功。精确clause与比较日志已保存；Raman正在只读有界独立审查，尚未转交writer修复。
- 当前只释放archive run/grant；共享generic active-slot release primitive未发现，未另造archive scheduler/lease。AUTO、resume/reassign/new epoch、Client runner、M7、Web及跨组件验证仍未完成。84业务验收not_run、pins null、release not_started；没有commit/push或生产操作。

- Raman局部REJECT：2P1（新fresh MySQL CHECK元数据不匹配；原deadline阻断已经提交的terminal READ_ONLY result/failure replay），2P2（started message未显式与delivery active message再次比较；新增JDBC lifecycle事务/回滚/撤销竞态缺真实覆盖）。原回执`native-lifecycle-attempt1/review.json`。生产者写仍须deadline；terminal结果只读重放以当前有效身份/任职/命令/epoch/证明约束，不以旧执行deadline阻断已提交回执。下一步由唯一writer集中修复后重新冻结强制测试及局部复审；未跳过失败。

## 24. native 生命周期最终源码测试（局部复审中）

- 修复2P1/2P2后，attempt2实际发现新测试缺`ArchiveRuntimeScope` import，Chat test编译失败，未复用旧Chat XML；attempt3通过编译及fresh schema，但新fixture重复插入initializer已拥有的collection；attempt4真实执行仅剩末尾断言错用appointment.state而非status。每轮原log/失败及before/after tree记录保留，不改写成通过。
- attempt5 exact prospective API tree **`74630fbbf6e0c6b8eddbcca25c6834a8426f2b2a`**，相对M5为19文件；前后独立tree相同，所有XML均晚于freeze。持`C:/tmp/cyf-gradle.lock`强制真实四suite：**platform69/69 + native_security6/6 + maintenance65/65 = focused140/140**；archive **230 tests / 11原baseline失败 / 0skip**，对M5 approved实际failure_set introduced=[]、removed=[]。Gradle exit1/BUILD FAILED为原11项，不伪称全量绿。
- 新真实JDBC/service事务用例执行了start/单一事件重放、failure/READ_ONLY/晚到terminal回执、late start与late FAILED CAS完整回滚、DRAFT_ONLY校验完成且无publication、完成后producer update/validate拒绝且draft/events不变、READ_ONLY撤任fence及原scope结果拒绝。原RR admission/revoke race保留；execution port/private storage仍为test double，不是HTTP/WebSocket/runtime E2E。
- 精确MySQL lifecycle CHECK已通过fresh初始化，严格validator未弱化。Producer deadline保留；terminal READ_ONLY结果重放不被原producer deadline阻断，仍受当前runtime/registration/manager/appointment/skill/command/attempt/epoch/active message约束。升级旧draft maintenance schema未获证明。
- 原始证据`evidence/native-lifecycle/native-lifecycle-attempt5/`，Raman只读核对六文件repair delta与2P1/2P2闭合；尚未转交下一source writer。仍非整体验收，AUTO/resume/new epoch/Client runner/M7/Web/integration未完成，84业务not_run、pins null、无commit/push/deploy/激活。

- Raman最终局部ACCEPT绑定`74630fbbf6e0c6b8eddbcca25c6834a8426f2b2a`：原2P1/2P2闭合，六文件repair未见新增P0/P1/P2。回执`native-lifecycle-attempt5/review-final.json`。范围仅native生命周期，仍未覆盖真实HTTP/registration/WebSocket、实际port/storage组合及旧schema升级；非整体验收。

## 25. 下一API切片：AUTO与显式恢复

- 生命周期freeze/tests/review闭合后，唯一source writer转交Knuth继续API：AUTO native publish复用既有原子publisher；MANUAL即便任职可发布也须终结producer；显式admin resume/reassign/new run+epoch保留历史并隔离旧run；核对受信同实例reconnect/registrationHash renewal，新runtime/binding必须正式恢复。Client/Web继续冻结，Main仍只写协调/验证证据。
- task控制文件在本机`C:/tmp/aam-client-evidence-20261001/next-api-auto-resume-task.txt`。默认execution disabled不变，不新建队列/lease/scheduler，不改经济表、不做生产/付费模型/业务激活；不得以只读回执解除producer deadline。
- 当前新AUTO/resume源码尚未freeze或测试。后续仍须Client approved runner、M7三项request-scoped工具/直达入口、Web接线、真实隔离跨组件与final source audit，再分别commit/push组件、精确pin并commit/push root。84业务验收仍not_run，pins null、release not_started。

## 26. 2026-10-01 AUTO/显式恢复冻结实测

- 两轮真实持锁测试均通过编译、平台69和native security6，但新控制器测试用旧形态 `If-Match: "7"`，先于主体校验被拒绝：attempt1 positive publish、attempt2 body-injection均产生同一个新增失败；原log/XML/tree保留于`evidence/native-lifecycle/auto-resume-attempt1`和`auto-resume-attempt2`。没有改生产header校验或顺序来迁就测试。
- 唯一writer将注入测试改合法`"v7"`，并独立保留合法body+非法header断言。最终prospective API tree `a3a9e24cb9b884a7b86a16fbf8dc62822ab815e2`相对批准native tree为14文件；Main持`C:/tmp/cyf-gradle.lock`强制实库执行四suite，编译完成，before/after tree一致，fresh XML均晚于freeze：**platform69/native6/maintenance70=145/145定向通过**；archive **235/11原baseline失败/0skip**。直接native failure-set introduced=[]、removed=[]。Gradle exit1/BUILD FAILED，未称全量绿。原始证据`evidence/native-lifecycle/auto-resume-attempt3/`。
- 新代码包含native AUTO publish、MANUAL producer释放、admin resume/reassign new run+epoch；当前仍未独立review accepted。Raman开始只读14文件增量审查；重点核对权限/CAS/重放/旧scope隔离，以及publisher源码加载是否在DB事务中执行外部I/O。API/Client/Web均冻结，Main不改源码。
- 同run自动registrationHash renewal未实现；只能显式管理员恢复到new run/epoch，不宣称自动重连已解决。仍需Client确定性runner、M7受限三工具、Web接线、真实跨组件测试及最终commit/push；84业务验收not_run、pins null、release not_started、生产未操作。

- Raman对AUTO/resume局部REJECT：2P1（publishLocked的外部sourceStorage.read在DB事务/授权锁内；已FENCED current run再次fenceRun返回0，导致合法expiry/revoke后恢复失败）及1P2（真实MySQL fixture未走生产expiry/revoke fencing）。回执`auto-resume-attempt3/independent-review.json`。Main已明确转交Knuth唯一API writer集中修复两阶段publication候选/最终短事务复核、一致FENCED history允许new epoch、生产fence后的实库恢复覆盖；Client/Web仍冻结。定向145通过不替代这些已确认生产问题闭合。

- 两P1修复首次冻结tree `7bb9e14d7b268e13ae067f2ff7819707edfc7def`，attempt4实测编译完成且前后tree一致；platform69/native6通过，maintenance72/3fail、archive237/14fail、0skip，新增3项失败。新expiry fixture把expires_at置0违背已有>0 CHECK；两个人类publish fixture未stub两阶段新增的非锁current appointment查询，提前被ACL拒绝，未测到内容candidate。生产revoke→replacement→reassign及事务外storage断言已实跑通过。原log/XML/source proof留存，唯一writer只修这些测试fixture，不改schema/生产ACL/expected错误来伪绿，再冻结复测。

- attempt5最终修复tree `d4e041270b7eed7751c05107ee3f7ac993c6aaf5`前后独立一致，所有fresh XML晚于freeze，持锁强制实库：**69+6+72=147/147定向通过**；archive **237/11原baselinefail/0skip**，直接native failure-set introduced=[] removed=[]。sourceStorage事务外读取断言、committed replay不读storage、production expiry→resume及production revoke→replacement→reassign全部实际执行通过；整体Gradle仍exit1/BUILD FAILED。3文件repair delta已交Raman只读复审，尚未accepted。另已确认Client AUTO revise所需workCAS snapshot不在native context/payload，须局部闭合后有界补exact-job native只读snapshot，不能由Client猜值或借adminJWT绕路。

- Raman最终局部ACCEPT绑定`d4e041270b7eed7751c05107ee3f7ac993c6aaf5`，原2P1/1P2闭合，3文件repair无剩余P0/P1/P2；回执`auto-resume-attempt5/review-final.json`。该范围仍非HTTP/真实Runtime/Client/整体验收。唯一writer继续API最小前置：exact-job native context workId/operation/work revision/active edition只读snapshot，让Client AUTO revise可构造真实CAS请求；Main不写源码，Client/Web冻结。完成该局部source/tests/review后才转Client runner。

## 27. Native context作品CAS前置

- 唯一writer已完成5文件最小增量：native context新增exact-job `workId/operation/expectedWorkRevision/expectedActiveEditionId`，无新任意work route、无包/schema修改；ADD_WORK且work/collection-work均不存在返回0/null，异常关联拒绝，最终publisher仍实时CAS。prospective tree `52f235d2c73e0099cdba5769e018a5098a683b93`。
- Main持锁强制实库`native-work-snapshot-attempt1`实际编译及四suite完成，before/after一致，freshXML全晚于freeze；**platform69/native6/maintenance73=148/148通过**，archive **238/11原baselinefail/0skip**，直接批准AUTO introduced=[] removed=[]。新AUTO revise context→当前workrevision变化→publish冲突fixture实跑通过。整体Gradleexit1/BUILD FAILED为原baseline，不记为全量绿。
- 原log/XML/source proof与direct-auto-comparison在`evidence/native-lifecycle/native-work-snapshot-attempt1/`；5文件只读review进行中。Client执行器、M7、Web接线和真实跨组件fixture/最终交付均未完成；无commit/push/生产操作，84业务not_run、pins null、release not_started。

- Raman5文件局部review最终ACCEPT绑定`52f235d2c73e0099cdba5769e018a5098a683b93`，无剩余P0/P1/P2，原回执`native-work-snapshot-attempt1/review-final.json`。Main已明确将唯一source writer转交Knuth到Client worktree，API/Web源码冻结；下一为真实processor/agent-client入口的approved deterministic Archive runner，任务`C:/tmp/aam-client-evidence-20261001/next-client-archive-runner-task.txt`。Main继续负责fresh Git archive Linux full test与证据，不与writer竞写。尚未commit/push或启用执行。

## 28. Client确定性执行器首轮Linux冻结实测

- Knuth完成SOURCE FREEZE，API/Web未修改；批准包fixture精确40563bytes/SHA不变。新增默认off、Linux native adapter探测后的Archive execute广告、原processor/单inbox-ledger路由、固定origin+当前registration scope、approved纯parser、原生workCAS、MANUAL/AUTO差异、terminal-only closure及generation fence。Main没有把作者Windows机械/部分测试当成Linux或E2E通过。
- Client prospective tree `432ddf9658fb8bcc2cdbafdf01b15e18a7607543`相对批准M6为12文件增量；Main原git archive到隔离Linuxchroot完整npm test：**443tests / 432PASS / 11FAIL / 0skip，exit1**，before/after独立一致。保留原configruntime1failure；新增10项均Archive positive/lostresponse/routedterminal失败，主要`PLATFORM_SKILL_INSTALL_CONFLICT`，未打通执行。原TAP/tree/sourcebytesSHA与baseline delta留存`evidence/client-runner/archive-runner-attempt1/`。
- 新resolveApprovedArchiveInstallation的receipt层级与既有_loadReceipt返回已验证flat View疑似不符；Raman正在只读12文件集中审查并核对marker/currentScope/包证明、人工修改保护和generation negative是否被前置失败短路。源码仍freeze，Main未先授权边测边修。Client runner尚未accepted，M7/Web/实际跨组件和commit/push仍未完成，84业务not_run、pins null、release not_started。

- Raman对Client runner首轮局部REJECT：P1新增resolve误读已验证flat receipt层级；P2两项negative（unknown/human edit）被该前置proof失败短路，PUT0本身不能证明人工修改保护。只读回执`archive-runner-attempt1/review-final.json`。Main已恢复Knuth唯一Client writer，集中修flat receipt访问并补真实路径到达断言，保留marker/currentScope/包/19file/inode/reverify和原baseline；修复后fresh Linux full重新实测再局部review，不接受作者机械检查替代。

- Client receipt/P2路径断言修复后，attempt2 tree `2cc077fcb14380d5803fd8c5fb1ef93063531b25`前后独立一致，真实Linux full **443/440PASS/3FAIL/0skip**。原configruntime1failure保留；10新增中8闭合，MANUAL/AUTO、成功步骤丢响应、human context/source/draft实际GET且PUT0、unknown actual start/result路径均真实通过。剩余2新增为failed/lost-failure HTTP fixture错误期待`ARCHIVE_NO_CHAPTER_HEADING`，实际approved parser对leading正文返回`ARCHIVE_LEADING_BODY_WITHOUT_HEADING`，callback产生unhandledRejection。原rawTAP/proof保留`archive-runner-attempt2/`；Main只授权唯一writer核对approved诊断后修此fixture期望，不改包或生产runner来迁就测试，再freeze/full/review。

- Client最终attempt3 prospective tree `191d8fc8d6285d3f0614a656f729657688a29204`由Main原Gitarchive完整Linux full实跑：**443/442PASS/1原configruntimeFAIL/0skip，exit1**；对批准M6 introduced=[] removed=[]，before/after独立一致。人工修改保护路径、unknown真实路径、MANUAL/AUTO、start/draft/validate/publish/failure丢响应、routed completed/failed、过期terminal读取与socket/cache fence均已执行通过，不借前置proof失败伪绿。2文件repair已交Raman只读复审，原P1/P2尚待最终回执。证据`archive-runner-attempt3/`；默认off和非实际API E2E范围不变。

## 29. Client局部闭合与M7交接

- Raman最终局部ACCEPT绑定Client `191d8fc8d6285d3f0614a656f729657688a29204`，原receipt P1与短路negative P2闭合，2文件repair无剩余P0/P1/P2，回执`client-runner/archive-runner-attempt3/review-final.json`。仅此次受控执行器/修复局部接受，不是实际API/Client E2E或整项验收。
- 唯一source writer已明确转交Knuth回API（批准tree`52f235d2c73e0099cdba5769e018a5098a683b93`），Client/Web冻结。下一M7为fresh request-scoped仅3工具、受信JWT/会话/turn/confirmed policy、同durable request-intent/usecase，以及direct appointedAgent/private不走宋江；任务`C:/tmp/aam-client-evidence-20261001/next-m7-restricted-entry-task.txt`。测试只fake/local ChatModel、不调用付费provider；Main只负责协调、持锁验证和证据。
- M7当前尚未freeze/实测；随后Web安装/execute/resume/卡片接线、真实隔离跨组件fixture、最终审查与组件/根commit-push均未完成。默认off、84业务not_run、pins null、release not_started；本轮未commit/push/生产激活。

## 30. M7结构化入口首轮冻结实测

- M7 SOURCE FREEZE prospective API tree `a2a6031ce94eb33333685ce2ec85915f15f143e1`，相对直接批准native tree `52f235d2c73e0099cdba5769e018a5098a683b93`为17文件增量；Main实际持锁forced真实隔离MySQL四套完成编译与运行，before/after tree相同、全部freshXML晚于freeze。
- platform69/native6通过；maintenance **87/3FAIL/0skip**，archive **252/14FAIL/0skip**，直接批准baseline增加同3项、原11失败不变。新failure为coordinator JWT fixture认证不完整、两项service appointment前置未满足，尚待只读review判断production/fixture边界。Gradleexit1，不能称M7通过。
- 证据`evidence/native-lifecycle/m7-attempt1/`与`direct-native-comparison.json`；Raman正在只读M7集中review。API/Web/Client继续冻结，Main没有边测边授权修改。结构化确认上游签发/UI、Web接线、实际跨组件fixture及commit/push仍未完成；默认off、84业务not_run、pins null、release not_started。

- Raman M7局部REJECT，绑定a2a6031 tree：P1客户端结构化body直接升级confirmed policy/intent/turn，P2模型无工具/非终态文本可宣称成功，回执`m7-attempt1/review-final.json`。3实测新增失败属fixture，生产JWT与锁校验必须保留。Main已授权Knuth唯一API writer集中修server persisted immutable confirmation + exact actor/canonical conversation/turn + opaque ref，以及权威callback/server receipt输出；允许现有Archive store必要最小事实增量，不新独立store/会话框架。修后重新冻结实测/独立审查，Client/Web继续冻结。

## 31. M7持久确认与权威回执修复实测

- 单writer修复已SOURCE FREEZE tree `b05d1eaa5a5a17d018f567eb0fa1f118b0df796e`；相对REJECT a2a6031为17文件repair。Manager入口先ACL+现有operation/store原子写immutable confirmation；chat只opaque ref，首次真正appendOwnedMessage的canonical ID与actor/conversation/generation/contentSHA/entry/target绑定；同ref不能跨宋江/private漂移。模型输出弃置，最终仅callback权威状态生成结构化receipt，无工具UNCONFIRMED。
- Main实际持锁forced实库四套完成编译与运行：**platform69/native6/maintenance90=165/165PASS**，archive **255/11原baselinefail/0skip**；直接批准52f235d2 introduced=[] removed=[]，前后tree同一且fresh XML无stale。整体Gradleexit1，不能声称全量绿。证据`evidence/native-lifecycle/m7-attempt2/`，原attempt1失败与REJECT保留。
- 新confirmation表的catalog/guarded MySQL fixture实测通过，但不证明早期draft schema升级。Raman复审原P1/P2进行中，API/Web/Client冻结；Web与真正跨组件fixture/交付仍待，84业务not_run、pins null、release not_started，无commit/push/生产激活。

- Raman M7修复局部ACCEPT绑定`b05d1eaa5a5a17d018f567eb0fa1f118b0df796e`，原P1/P2闭合、无剩余P0/P1/P2，回执`m7-attempt2/review-final.json`。manager→首次选择chat入口共享durableintent，ref随后禁止跨entry/target迁移属安全收窄。Main将唯一source ownership转Web balanced worker，API/Client冻结。下一Web最终接线及真实隔离跨组件fixture仍必须完成后才commit/push。

### 跨组件fixture环境预检查（不是E2E）

- Main临时Windows loopback HTTP sentinel在127.0.0.1:59290，真实Linux chroot Node fetch同地址得到ECONNREFUSED（WSL NAT不转发host localhost），临时server已仅针对本session停止。故不能假定Windows API与Linux Client跨host127.0.0.1天然互通。
- 后续实际fixture必须明确同Linux API JVM或host-only WSL网络/透明TCP relay拓扑并真实测通，不得为迁就环境使用fake nativeHTTP server替代actual API。此为环境约束，不是Runtime业务缺陷。

- Main实测仅绑定Windows WSL host-only interface `192.168.144.1`的临时sentinel，Linux实际Node fetch返回200精确sentinel，server退出；无需public0.0.0.0/firewall修改/代理。后续可选Windows actualJava API host-onlyWSL + Linux actualClient，JDBC仍Windows127.0.0.1；必须标注此实测拓扑与重观测interface，不能在production硬编码gateway。这仍仅网络可达性，不是组件E2E。

## 32. Web最终接线首轮实测（尚未通过）

- Curie为唯一Web source writer，SOURCE FREEZE before `51c4e3c6d4d26768fe080b6911adf8d425adebf7`。Main运行6file定向archive/JuyiHall suites，root beforeAll在componentBehavior旧SFC loader遇新增import SyntaxError，0实际tests/1hookFAIL；不能把它称为定向通过。
- Main production build exit0，真实generated `src/components.d.ts`增加ReceiptCard一行，after tree `61637ef6027f23d3a970efb8b7908fd35716e9de`不同；如实记录source delta，不伪造冻结前后一致。此after tree对原Web approved e7d4为10file增量。
- 单独隔离除componentBehavior之外的5file真实运行 **142/142PASS**、0skip；仅诊断可运行子集，不能替代失败组件suite。证据`evidence/web-wiring/web-wiring-attempt1/`含两轮JSON、build与source-proof。
- Raman只读review进行中，重点实际panel gateway方法/DTO和原source/draft/publication能力、currentCatalog、ambiguousintent及identity/authority lateResponse。Web/API/Client冻结；无commit/push/production。真实跨组件fixture仍后续，84业务not_run/pinsnull/releasenot_started。

- Web首轮Raman局部REJECT绑定61637e：5P1（缺slot gateway、非canonical宋江target、删除既有source/draft/MANUALpublish/revoke/cancel控制面、refresh改变identityepoch导致busy永久、晚响应身份泄漏），3P2（ReceiptCard无identity/unmount fence、ambiguous改body静默新key、客户端常量冒充currentCatalog）。回执`web-wiring-attempt1/review-final.json`。baseline e7d4独立Gitarchive也有LibraryPanel childimport loader root hook failure，证据`web-component-baseline/`；新ReceiptCard同类缺口，不谎称原suite全绿。
- Main已临时转唯一API writer给Knuth做最小currentCatalog只读metadata prerequisite；Web/Client冻结，不边测边修。准备Web集中修复任务`C:/tmp/aam-client-evidence-20261001/next-web-repair-task.txt`，API新catalog实测/局部review后才激活Curie。已有approved包字节/安装/市场契约不能改。

## 33. Current Catalog前置实测与Git包字节交付缺陷

- 最小6file只读catalog增量SOURCE FREEZE API `67ae414f1964af95794510d0e2038841bfc43ba6`；Main实际forced持锁实库四套 **platform74/native6/maintenance90=170/170PASS**，archive255/11原FAIL/0skip；对M7 b05d1e direct introduced=[] removed=[]，before/after同tree/freshXML。catalog局部readonlyreview进行中，Web/Client冻结。
- Main新增真实交付byte audit发现API core.autocrlf=true且platform包19file未有-text保护；manifest、ordinaryCRLF、malicious3file Gitobject不同于实际buildworktree bytes。Main exactGitarchive67ae包resources前置JavaCP，真实compiled PlatformSkillCatalog + 原approved ExportApprovedPackage helper运行：javacexit0/exportexit1，明确报Approved platform skill bytes changed。因此已有170实测是worktree证据，不证明Git拉取可复现批准ZIP；此P1必须在commit/push前闭合，不忽略/换包版本迁就。
- 证据`evidence/package-reproducibility/package-git-export-attempt1/`含19filebyteSHA、真实Java日志与sourceproof。待review后唯一API writer仅修.gitattributes byte-exact保护包资源（不得改40563bytes/19file/SHA889批准包字节），再freeze逐19file disk/object匹配并exactGitarchive Java重建验证。无commit/push/生产激活，Web8findings/真正跨组件fixture仍待。

- package属性修复SOURCE FREEZE API `9ae02b3164033151dabde3aada87055e90a67999`。Main 19/19资源Gitblob与worktree逐byte一致，exactGitarchive真实JavaCatalog export exit0，ZIP **40563 bytes / SHA8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081**，原批准资源/版本未改；原失败证据保留。重新forced持锁实库170/170PASS、archive255/11原FAIL/0skip，directcatalog delta空、beforeafter同tree/freshXML。证据`native-lifecycle/package-git-attempt2/`；1P1只读复审进行中，之后才转Web集中repair。

- Raman package/catalog最终局部ACCEPT绑定9ae02b3，原byte P1闭合且无P0/P1/P2，回执package-git-attempt2/review-final.json。Main已将唯一source ownership恢复Curie Web修复全部5P1/3P2，任务next-web-repair-task.txt；API/Client冻结。当前catalogactualroute/defaultoff/4字段合同已给Web writer，不能再clientconstant冒充目录。无commit/push/生产，真实跨组件fixture仍后续。

## 34. 文档校验当前状态审计

- Main重跑validate-design.cjs：协调YAML summary中的colon语法错误已修，随后真实静态检查失败`client_source_sha256:test/platform-skill-manager.test.mjs`。该旧checker把历史Client246 source proof hash同已实现runner的当前worktree相比较，不能作为当前文档通过证据。verification.documentation标为pending_refresh，保留原历史documentation-check.json但不声称当前通过。
- 最终交付前需区分历史冻结source/evidence与当前已验证组件pins，并保证历史prospective tree证据可在clean clone中核查或明确提供归档对象；当前源不断变化时不能用删除旧failure/assertion伪绿。此仅协调/证据校验边界，不是application失败或新生产门槛。

## 35. 2026-10-01 Web repair 实测与 mounted test 补齐

- Curie 的生产源码集中修复冻结于 Web prospective tree `9fc1f69513d8d3e3b36b63ad87b6ec211ac3d5c5`（非 commit）；API `9ae02b3164033151dabde3aada87055e90a67999` 与 Client `191d8fc8d6285d3f0614a656f729657688a29204` 保持冻结。Raman 对该生产源码进行独立只读复审。
- Main 首次重跑实际执行 185 tests / 181 PASS / 4 FAIL / 0 skip。原始 `tests-rerun.*` 在 `evidence/web-wiring/web-wiring-attempt2/`。命令中的三个错误文件名被 Mocha 忽略并有明确 warning，故这是三个实际文件而非六文件覆盖；不声称缺失 selectors 已运行。前一中断的 JSON 不完整，仅保留本机，不当作有效结果。
- 三个新增失败为旧 source-string 断言及将 changed-body 检查安排在成功释放 key 之后；第四个为 LibraryPanel 第三维护 tab 的 roving focus 旧二 tab 假设。当前仅授权 Curie 修有依据的测试并补 actual Vue Panel/Receipt mount + real gateway/createApi/fetch 边界，不能删 suite 或把 source-string 认作 runtime 验证；若 mounted test 发现生产问题，集中记录后再修。
- Root historical validator 当前真实失败 `client_historical_source_sha256:agent-client.mjs`。旧 246-test proof 的工作树摘要并非全部与其 Git tree 字节一致（另有两个旧 CRLF 与 Git LF 差异）；不篡改旧 proof 或假称新源码跑过旧测试。最终交付采用后续 exact Git archive 测试与当前 commit pins，历史文档校验不足仍需单独列明。
- 四个仓库远程 refs 已刷新。Root 当前远程仍为 `01f7599ed28e84c1a44d2cc6c3dec13f7ddbeb67`，本地与远程 0/0；远程不存在无前缀 `archive-agent-maintenance`，实际设计分支为 `codex/archive-agent-maintenance`。未 commit/push/生产激活；真正跨组件 fixture 尚待接入。
- 第二轮生产源码只读复审 REJECT（2 P1 / 3 P2）：catalog 默认关闭404不应阻断撤任/取消等既有控制面；仅 job.manage 授权缺少 exact recovery appointment proof；模糊请求恢复未接 UI；客户端固定技能版本；UNCONFIRMED/no-job 卡片空白。原回执 `web-wiring-attempt2/review-final.json`。Web production build 成功，generated declaration 与该 frozen tree 无语义内容差异；不替代行为测试。
- Mounted attempt1 真实测试加载先因 LibraryPanel 测试缺换行而失败，独立 archive suite 又因 Vue import alias `as` 的 loader 转换失败（5/2PASS/3FAIL）；原件保留在 C:/tmp。Curie 修测试 harness 后冻结 e98a89072fac42834bf59b947acd75d268309356，Main 重跑真实存在的六个 selectors。结果待完成；不是已通过。
- 唯一源码 writer 已由 Curie 明确释放并转给 Knuth，只实施受 job.manage 授权的最小 `recovery-context` 读接口，不扩大 appoint ACL。完成后再转 Curie 一次性修五项生产问题；API/Client 默认关闭，生产和真实典籍上架未执行。
- Mounted attempt2 的六个真实 selectors 已执行 241 tests / 237 PASS / 4 FAIL / 0 skip（完整 JSON，非 root hook 零执行）。四个失败均在新的 Panel fixture：没有为真实 authenticated createApi 提供测试 authStore，因此请求在 token 前置被拒绝，fetch 为零。旧 reader/hall suites 通过；不能将新 mounted suite 视为通过。原件 `web-wiring-mounted-attempt2/`，后续在组件 gateway/api 注入现有 authStore 测试 seam，保持 needAuth=true，不 mock 掉生产 gateway/useHttp。
- Main 另确认 gateway 跨 identity race：A 未决 mutation 在 clear 后晚返回，会无条件 delete B 同名 retained intent。UI epoch 只防显示，不能防 B idempotency key 丢失；需 object identity/generation 条件删除并补 A→clear→B deferred 成功/失败回归。已加入下一 Web 集中修复清单，不扩大到其他业务。
- Main 另在真实 Node/Vue `ref` 上复现 resume/reassign gateway 的 `DataCloneError`（fetch calls=0）：`expectedSkill` 是深层 reactive Proxy，原 `structuredClone(body)` 不可克隆。下一同一 Web 集中修复必须按 JSON wire 快照保留不可变正文，补实际 mounted resume/reassign 的 DTO/If-Match/key 请求证明，不能用 plain mock fixture 隐藏问题。

## 36. Least-privilege recovery-context API 实测

- API prospective tree `66061b5bf3bdc8632fae6fb49370289d9ffd10d1` 已新增 scoped recovery-context 与 job.create OR job.manage 的 actor-owned job list/detail/events 只读权限。旧任职 snapshot revision 来自 job，不误用撤任后递增的 row revision；不扩大 appoint/slot/write/publish 权限，候选仅本 actor 当前 ACTIVE 任职。
- Main 独占 Gradle lock 强制真实 MySQL 四套复测：platform74/native6/maintenance93，共 **173/173 PASS**；archive **258/11既有FAIL/0skip**。对直接批准 package9ae树 introduced=[]、removed=[]；before/after exact tree 相同、freshXML 无 stale。整体 Gradle exit1/BUILD FAILED，不能称全量绿。原日志、XML、source proof、direct failure delta 在 `evidence/native-lifecycle/recovery-context-attempt1/`。
- 这仅是组件源码/隔离实库验证，不是 Client/HTTP/WebSocket E2E 或 business publication；API/Client 冻结，独立 scope review 等回执，之后交 Curie 做已集中记录的 Web 修复。
- Recovery-context 最终独立只读 ACCEPT_LOCAL_SCOPE（仅六文件）、P0/P1/P2=0，绑定 `66061b5` 与173实测、原11失败和非一致snapshot由writeCAS重验。回执 `recovery-context-attempt1/review-final.json`。Main已将唯一源码 writer 转 Curie，一次性修 Web catalog/恢复/unknown UI/身份与权限epoch/Proxy克隆/UNCONFIRMED 等集中发现；API/Client冻结，commit/push/生产激活尚未发生。

## 37. 2026-10-01 Web 最终冻结验证与有界跨组件计划

- Curie SOURCE FREEZE 后，Main 用外部 index 冻结 Web tree `fb88081d1be5a971807880a49ea62d2156cf898d`。六个真实存在的 selector 合计 **243/243 PASS、0 pending**，`npm run build` exit 0；构建后 tree 不变。原始 JSON/日志/selector/source-proof 保存于 `evidence/web-wiring/web-final-attempt1/`。这些 mounted SFC → production gateway → createApi/useHttp → fixture fetch 仅验证浏览器 HTTP 边界，不是实际服务端 E2E。
- 独立只读 Web 复审正在进行；Main 另外提醒 operation-by-key 必须尊重实际 PENDING/COMMITTED，以及 authority rebase 不能留下旧 busy token。测试全绿不替代这些并发/状态检查。
- Knuth 提交有界跨组件方案：测试内嵌 Tomcat，真实 Archive admin/native/reader Controller、runtime filter、JDBC store、transaction manager、private artifact、production codec，与冻结 Linux NativeRunner 对接。身份/bootstrap、execution admission/transport 和安装运输为明确 prerequisite doubles；不声称真实 Rabbit/WebSocket Runtime E2E。计划只做 synthetic UTF-8 MANUAL 草稿→显式 publish/readback、AUTO 唯一 publication/replay，未授权 writer 前不得写源码。
- Client 明文固定 origin 只接受真实 loopback；Linux relay 仅用于证据侧 loopback 到 Windows host-only fixture HTTP，不改生产 TLS/origin policy、不开 public 0.0.0.0。84项真实业务验收与部署继续 not_run/not_started。
- Final-attempt1 只读复审 REJECT_LOCAL_WEB_SCOPE（2P1/1P2）：PENDING误判COMMITTED释放原键；mutation内authority rebase遗留busy；catalog/capabilities401未清已加载权限数据。Main已复现PENDING DTO误判并将唯一Web writer转回Curie，仅修这三项与真实mounted negatives。243全绿证据仍保留，不抹除未覆盖路径。

- 最终 Web tree b3d0ac34e4a08a75d1d6420d702d19264126becd：245/245 PASS、0skip、build0、before/after相同；last3及真实operation DTO targetType/targetId均闭合，独立 ACCEPT_LOCAL_WEB_SCOPE、P0/P1/P2=0。原始证据 evidence/web-wiring/web-final-attempt3/，先前REJECT与未覆盖问题保留。Main已将唯一source writer转Knuth实施上述有界API/Client fixture，Web/Client冻结。

## 38. 有界跨组件 fixture 的真实阻塞与修复

- 新5文件test-only tree dad3e24编译成功。Main发现生产artifact storage必须POSIX，未在Windows伪造权限或改生产实现；采用隔离Alpine真实Java25+Node同namespace/loopback，Windows隔离MySQL仅经allowlisted host-only双relay访问，storage实际Linux私有文件系统。
- attempt1真实Tomcat/JDBC/storage启动，但首次Admin source POST401；Client、MANUAL/AUTO/publish/readback未执行。独立review确认fixture单参数JWT未authenticated且未向MVC暴露request principal，P1仅限测试seam。Main停止经pid/mainClass核验的自有fixture Java，保留日志，未操作其他进程/生产。唯一Knuth writer仅修test-token构造与request wrapper/wrong-bearer negative，未放宽生产ACL。
- classpath export后续显式依赖所有runtime buildDependencies，成功轮必须before/after freeze与完整运行证据；失败轮不算跨组件通过。历史documentation checker实跑仍失败client_historical_source_sha256，证据另保存，不篡改旧hash造绿。


## 39. 2026-10-01 有界跨组件实测闭合

- attempt4 实际 approved ZIP 验证和 Linux atomic activation 成功，但 fixture 把对象传给只接受字符串的安装 resolver，故 1/1 FAIL；原始失败证据保留在 `evidence/crosscomponent/crosscomponent-fixture-attempt4/`，不能视为 runner 成功。
- 仅修 fixture 调用参数后，API frozen tree `fbc4a8f9b89c0bb410fcd7df5e3f8590fb17cbb5` 与 after 相同。Main 用此 tree 的 `git archive` 导出新 Node selector；与 Java 编译 tree `4e9598da5599bb3c3ed75adcc5316be1b7b50345` 的唯一差异就是该 Node selector，因此复用 attempt4 的相同 Java blobs/JVM 和冻结 Client tree `191d8fc8d6285d3f0614a656f729657688a29204`，不声称 JVM 由最新 tree 重新编译。
- 实际 Node test **1/1 PASS、0skip**。MANUAL native 草稿/校验/terminal 后由管理员显式发布并 Reader 读回；AUTO native 发布及重放后唯一 publication 和唯一 publication event，实际 Reader 正文相同。最终 `final-result.json` 为 `passed`；证据与精确 source binding 在 `evidence/crosscomponent/crosscomponent-fixture-attempt5/`。
- 真实组件是 Tomcat/DispatcherServlet HTTP、Controller/runtime filter、MaintenanceService、JDBC stores/transaction、POSIX storage、production codec、Client approved ZIP/19-entry proof/atomic activation/NativeRunner。identity/bootstrap/account、registration、execution admission/transport、installation download/result transport 是明确 prerequisite doubles。没有真实 Rabbit/WebSocket 握手及 active-slot/outbox 全链，不外推为 Runtime E2E 或业务验收。
- final-result 完成后核对自有 Java PID/mainClass 再 TERM，仅作资源释放；launcher 退出码不是成功判据，不操作其他任务进程。API/Client default-off 不变；没有部署、生产激活、真实典籍上架或付费模型调用。


## 40. 最终实库回归与组件远程交付

- Main在共享Gradle lock下针对最终API tree fbc4a8f9 强制四套真实隔离MySQL重跑，173/173定向PASS；archive258/247PASS/11既有FAIL/0skip，整体exit1。freshXML、before/after一致、对66061b5 direct introduced=[]/removed=[]；原件 `evidence/native-lifecycle/final-api-regression/`。
- 最新fixture独立 ACCEPT_LOCAL_FIXTURE_SCOPE，最后resolver P2闭合，P0/P1/P2=0。Web/Client重新freeze与批准树不变。
- API/Web/Client均已提交到独立feature分支并普通push，ls-remote核对exactSHA；组件远程证据与提交/tree见delivery.md。Root仅在该核验之后更新gitlinks/Client pin；Root最终push回执在执行后报告。
- 功能default-off、84业务not_run、release not_started不变。历史checker失败和原始失败轮保留；当前交付gate不伪称完整回归绿色或真实Runtime/生产验收。


## 41. 最终source-binding字节核验

- Current交付gate首次拒绝误标的fixture selector SHA。f5e3为Windows磁盘6373 bytes；Git blob为6372 bytes/SHA3c1aa，Git archive导出和实际Linux运行均6488 bytes/SHAc07144。逐字节assert exported CRLF→LF == Git blob，disk同样仅EOL差异，不改变任何源码或批准包。保留原source-binding和review，当前binding分列blob/export/disk，导出tar保留实际字节。
- 修正证据标签后current一致性gate109项PASS，历史checker依然exit1并披露。没有改变运行结果或业务not_run；根仓最终pin与组件已推送exactSHA一致，sddw verify exit0。
