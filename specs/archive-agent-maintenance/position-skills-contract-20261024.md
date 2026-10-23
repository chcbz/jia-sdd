# 典籍维护：职位技能修订合同（2026-10-24）

状态：已实现并推送候选，定向诊断通过，**未整体验收、未部署**。本修订承接用户确认与 `implementation-plan-4h-20261023.md`，优先于下面保留的 D2 目标；不是历史 D2 84 项已通过的声明。统一信封仍为 API `docs/interface-standard.md` v1.2。

## 模型与职责

- 技能类型仅 POSITION / GENERAL；同一 key 的类型及审核包版本不可原地替换，后续包升级需明确版本迁移方案。无专属技能。
- 职位与技能多对多；一个 Agent 可任多职，名额是职位配置。任职只建立期望状态，收到当前 native Runtime 的有效安装回执后才就绪。
- POSITION 在最后一个有效来源撤销后停用、回收；GENERAL 获得独立保留事实，卸任或删除职位默认项不删除它，仍有合法安装资格，可单独卸载。
- 职位新增默认项向现任者补装；显式卸载 GENERAL 后，无关配置变化不擅自重新安装。
- backend 拥有身份、任职、资源范围、发布许可和撤权；Runtime 只安装和执行。文件、skill key、提示词和 OAuth token 均不能冒充 Agent 权限。
- Scope 来自用户 JWT 或 native proof，不接受客户端传 tenant/client/owner。管理者还须具有 DB 中精确 scope/resource 的 `MANAGE_POSITIONS` / `ARCHIVE_WRITE` / `ARCHIVE_PUBLISH` 授权。普通登录用户不能自行获得公共书库权限。
- 原维护包/历史 fixture/历史 pins 不改写。新表独立命名为 `archive_skill_maintenance_job`、`archive_skill_maintenance_action`，不冒用 D2 的 `archive_maintenance_job`，不自动转换旧任职/作业。

## HTTP 合同

所有 JSON 使用既有 Q/R 信封，整数版本/绑定 ID 在 wire 上用十进制字符串；mutation 采用 `Idempotency-Key`。业务拒绝返回真实 400/403/404/409；资源/协议故障不报成功。包下载保留二进制响应，不包 JSON。

| 方法与路径 | 作用 / 主体 |
|---|---|
| GET `/agent/positions/v1` | 本人 scope 的职位/技能/任职/安装状态 |
| GET `/agent/positions/v1/operations/request` | 用原幂等键恢复任职操作 |
| POST `/agent/positions/v1/skills` | `{skillKey,type,productVersionId}`，必须引用已审核可信包 |
| POST `/agent/positions/v1/definitions` | `{positionId,title,capacity,resource,allowPublish,skillKeys,expectedRevision}` |
| POST `/agent/positions/v1/appointments` | `{positionId,agentId}`，显式指定真实 Agent |
| POST `/agent/positions/v1/appointments/{id}/resign` | 撤任；立即撤销对应业务授权 |
| POST `/agent/positions/v1/installations/{id}/uninstall` | 仅 GENERAL 显式卸载 |
| POST `/agent/positions/v1/installations/{id}/retry` | FAILED 重试，或 INSTALLED 显式重新验证；新 generation，不复用旧回执 |
| GET `/internal/agent/position-skills` | 当前 native proof 的安装/卸载期望 |
| GET `/internal/agent/position-skills/{id}/revisions/{revision}/package` | 同源固定路径、审核包和精确摘要 |
| GET/POST `/internal/agent/position-skills/{id}/receipt` | 精确 grant/revision/physical installation 安装结果与丢失响应恢复 |
| GET/POST `/archive/admin/v1/jobs` | 查询/创建作业，用户 JWT + 后端业务授权 |
| GET `/archive/admin/v1/jobs/operations/request` | 原键恢复创建或人工发布操作 |
| GET `/archive/admin/v1/jobs/{id}` / `/{id}/draft` | 元数据/只读版本内容；正文不放列表 |
| POST `/archive/admin/v1/jobs/{id}/retry` | `{}`；FAILED 作业的固定来源重交办，新作业/版本，原失败不覆盖 |
| POST `/archive/admin/v1/jobs/{id}/publish` | `{}`；显式发布 DRAFT，重新检查当前发布许可，共用 importer/CAS |
| GET `/internal/archive/v1/jobs` | 仅返回当前 Agent 仍有权执行的 WAITING 作业 |
| GET `/internal/archive/v1/jobs/{id}/source` | 原作业绑定的固定 UTF-8 来源 |
| GET/POST `/internal/archive/v1/jobs/{id}/result` | 当前 native proof 提交/恢复结果，不支持用户 OAuth 或旧 API key |
| GET `/archive/v1/works/{workId}/editions/{editionId}/catalog` | 已发布历史版本目录，沿既有 reader 数据源 |

创建作业 data：`appointmentId,agentId,skillKey,workId,title,author,sourceName,sourceRights,sourceText,mode`。`mode` 为 DRAFT_ONLY（UI 默认）或 AUTO。`sourceText` 是内容数据，不当作执行指令；source/edition/package/grant 固定后不能原地换内容。

结果 data 为 `{manifestJson,manifestFileSha256}`，或失败 `{manifestJson:null,manifestFileSha256:null,errorCode}`；Runtime 可报告的失败代码只接受 `ARCHIVE_SCRIPT_FAILED` / `ARCHIVE_SCRIPT_RESULT_INVALID`。AUTO 发布 CAS 不匹配由后端生成 `ARCHIVE_EDITION_CONFLICT` 终态，保留结果摘要，原作业不覆盖；显式重交办才建立基于当前版本的新作业，其他书籍继续处理。日志不记录底本、凭据或子进程原始错误。状态为 WAITING → DRAFT / PUBLISHED / FAILED；人工发布只允许 DRAFT → PUBLISHED。

## 安装、执行与一致性

- 复用 SkillPackageStore / SkillPackages、现有 durable SkillInstallManager、RuntimeV1Client 会话/同源传输及精确 native 白名单；不创建商城订单、不产生付费调用。
- 职位安装使用 grant/revision 而非伪造 orderId。移除采用已有原子文件操作，REMOVING → REMOVED 日志可恢复；旧包退出 CODEX_HOME 后保留在受控隔离目录，不删除用户陌生目录。
- 新包 `archive-maintenance` 1.1.1 是通用确定性 local-script：UTF-8、中文章回或 Markdown 标题、可选引首；至少两个结构不同的仓外样本验证。无 OCR/PDF/EPUB/任意 URL 抓取。
- 1.1.0 包因 SKILL.md identity 元数据不符合安装器而未通过真实安装；保留原字节作为失败准备记录。1.1.1 改正格式，以新版本/摘要交付，仍仅 prepared。
- Runtime 心跳仅在 native channel 已确认后顺序执行技能收敛、典籍作业。安装失败不伪装就绪；解析失败持久化为 FAILED，不阻塞下一个书籍；未决结果以原 job/grant 查询恢复。
- 同 scope 的状态根锁串行任职、撤权、安装变化和业务提交。native 提交另受现有身份/账户/session fence 保护。拒绝轮询中的撤权作业不能污染外层事务为 rollback-only。
- 发布共用现有 ArchiveContentImporter，在同事务中锁 work、检查原 active edition CAS、写不可变正文和切 active 指针；失败回滚无半成品。人工草稿发布使用同一入口、固定 edition、独立幂等审计。
- 历史版本要求 READY + activated_at，未发布 READY 不扩大公开面；作品下架（无 active）仍拒绝读。书签/手札仍绑定 owner + edition。
- 浏览器仅保存身份隔离的原操作键、元数据与请求摘要，不保存底本/令牌。首次明确的业务拒绝释放表单；网络不确定或重试被拒绝不能清除原请求键。

## 受控测试迁移 / 后续发布前提

1. 固定 API/Web/Client candidate SHA 和备份；确认仅操作明确的隔离测试库、停止旧候选写入者。此文不授权生产操作。
2. 已有 native identity/runtime、economy approved catalog/package store 和 archive reader schema 必须存在。marketplace 交易开关可以关闭，但复用目录及安装资格查询仍依赖对应已有表，不允许把缺表伪装成空目录。
3. 在新测试库执行 API `agent/jia-agent-mapper/src/main/resources/db/agent-position-skills.sql` 与 `chat/jia-chat-mapper/src/main/resources/db/archive-maintenance-jobs.sql`。无启动 DDL；已有同名表不能仅凭 IF NOT EXISTS 当成迁移成功，须核对列/约束与当前脚本。
4. 由有权运维单独提供测试 scope 精确权限与批准包记录；包存储目录不得 group/other writable，摘要对象不可覆盖。源码与 README 不自动批准/分发包。
5. API 显式启用 `agent.position-skills.enabled=true`，提供已有 `economy.skill.marketplace.package-store-root`；Runtime 使用当前 native manifest/session 和启用的持久安装器。未安装成功不能创建维护作业。
6. Web 进入典籍阁“任职与维护”，登记审核包、配置职位、明确选择 Agent 任命；等待实际回执，再上传固定 UTF-8 来源。先草稿检查，再明确发布，或具有发布许可时选择 AUTO。
7. 若 Runtime 更换/旧本地状态缺失，必须显式重装并获得新回执；本轮不自动迁移身份、恢复损坏安装器状态或把旧作业重新授权。
8. 停止测试后，仅清理本任务拥有的临时进程/测试库；保留证据和历史包。不执行生产迁移、服务重启、真实林冲任命或正式上架。

## 验证边界与未完成

详见本轮独立证据文件及 handoff。真实 MySQL + Spring/MyBatis + native HTTP + Node 安装器/脚本已通过本轮定向诊断；该 fixture 显式绑定 channel liveness，**不是实际 WebSocket 注册、已安装完整 Runtime、产品浏览器 E2E 或完整《三国演义》验收**。管理入口已补真实签名 JWT、生产 ResourceServerConfig/账户校验和 HTTP Controller 覆盖（任命、草稿、人工发布、卸任及越权负例），不是浏览器登录链路验收。

Flow5260799 与 4403172 的现行分支 guard 不允许本候选；未修改流水线、未为了 CI 合入 develop。前端正式 production build、精确候选正式 Flow、完整 Runtime/browser E2E、计划要求的独立只读复核仍是未关闭门槛。没有将 Owner 自查冒充独立复核，也没有因 4 小时目标缩减必选验收。

旧 D2 中宋江自然语言工具、全量旧矩阵/升级迁移等不因此完成；本轮可操作入口为任职与维护面板。权限/安装与典籍内容已解耦，但并非通用任意业务权限平台。
