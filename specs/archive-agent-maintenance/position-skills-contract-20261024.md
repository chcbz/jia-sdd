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


## 2026-10-25 develop 集成修订（目标与已实现分开）

本节用于用户已确认的“仅职位技能、排除 multi-region”集成；优先于上文旧安装接口描述。
公共信封仍固定 `api/docs/interface-standard.md` v1.2。核对源码：API develop
`ff819208a3941c05fe7c2e2e547aa09a4b6d74d6`、Runtime develop
`ec9ac757c40466670f0627a1e5486d8df5a4fce3`；纯职位 API 合并候选 `a24e09976308`。
**本节不是端到端适配、合入 develop 或上线完成证明。**

### 当前落实的 Runtime 合并原则

- 保留 develop 的 `SkillInstallManager` 与其当前管理测试，不用职位分支的旧版安装器覆盖。
- 当前管理协议是 `protocolVersion=1`，data 中 `schemaVersion=2`；共享持久接收、
  PREPARE / ACTIVATE / POLICY / READ、精确结果与服务端回执。不能把旧 flat
  `SKILL_GRANT_INSTALL` 直接传入 `execute`，不能从 HTTP 状态自制 `work.result.receipt`。
- `listInstalledSkills` 同时提供 `installationId` 别名与 `skillInstallationId`，此前关于
  “仅名称不匹配导致找不到”的推断不成立。真实差异是旧安装器的描述不含当前管理事实，
  以及该列表包含已停用安装，不能把“存在条目”当成可执行。
- 典籍作业按 `skillInstallationId` 选中精确安装，要求 `active=true`、`enabled=true`、
  `kind=EXECUTABLE`、包/manifest 摘要与 job 一致且 runner 为 local-script。
  风险：已停用或被替代的包仍留在磁盘，不能为新作业提供执行资格。
  失败范围仅当前作业、不运行脚本、不提交成功；实现 `ArchiveJobReconciler.installed`，
  回归复用 `archive-position-skills.test.mjs` 的原有精确安装测试。
- 获取 source 是异步边界；返回后再检查当前会话和安装资格，避免在换会话/停用后启动脚本。
  后端提交时仍重新检查任职/资源授权；本机检查不替代后端撤权与事务保护。
- 合并候选 Runtime 版本为 1.3.2（未发布），不降到职位分支 1.2.10；固定 app 目录规则不变。

### 尚待完成的跨端适配（不能仅靠解决文本冲突结束）

1. **非付费授权入口**：`SkillManagementService.owned` / `SkillAgentVersions.requireOwned`
   当前依赖 marketplace 开关及购买者上下文。职位来源必须以真实 native proof、任职 grant、
   binding、revision 和审核包授予安装授权，复用管理安装生命周期；不能调用购买入口、
   伪造 quote/order，或为了职位功能取消市场入口原有身份/资金校验。
2. **同一 skill 的并发与来源**：职位 grant revision 与共享 skillRevision 不是同一个计数。
   后端持久关联来源与真实安装，所有来源使用同一个 skill 状态根/单调修订；
   任职、卸任、GENERAL 保留与合法市场来源分别保留事实。撤销某一来源不直接删除包，
   仍有合法来源时保留资格；最后来源撤销关闭新准入，既有任务继续使用冻结安装。
3. **命令/回执**：`PositionSkillRuntimeService.commands/receipt/outcome` 与
   `PositionSkillReconciler` 必须一起切换。命令由后端按真实授权生成并持久化，Runtime
   使用 `handle` 完成持久接收与执行；共享结果通道提交真实 evidence，服务端持久确认
   后返回当前 receipt。不可由 Runtime 自行编造 source、skillRevision、permissions 或成功回执。
   现有 native Java/Node 联合 fixture 仍使用旧协议，必须同时更新，不能以 mock PASS 代替。
4. **锁顺序**：`PositionSkillRuntimeController` 当前在 native fence 内进入职位 scope root；
   管理入口是 actor → Runtime binding → skill root。桥接前必须统一顺序，
   不在持有 position root 后倒序调用市场入口；包 IO 仍在业务锁外准备并在锁内复核。
5. **查询与准入**：`PositionInstalledSkills` 不能仅凭旧 INSTALLED 回执绕过当前
   enabled/admission/READY；查询、归档 job 绑定、新任务准入使用同一真实安装关联。
   API 的 `InstalledSkillDescriptorLookup.Descriptor` 当前仍是九字段，不误加 Runtime DTO 字段。
6. **回归和交付**：复用现有市场安装/升级/启停、重连恢复与职位 native 集成用例，
   核对非付费来源在 marketplace 关闭时可用、多来源撤销不误停和新旧任务边界。
   不新增区域专项、不以旧联合候选的失败或成功冒充当前候选证据。

本次本机检查仅为轻量定向诊断；正式测试/构建与发布仍走已授权 Flow，每 Run 总耗时≤600秒。
后端适配未完成前不以 feature 默认关闭或局部回归通过声明整套职位功能可上线。

### 2026-10-25 共享安装适配候选（待正式验证）

源码候选：API `8047850b1e27488b1ed7f41d2f201d2fea233af5`，Runtime
`88ed1a88b9fe0b0a713845d13489a6daa9092fdd`。以下是已写入候选的契约，
不是已上线事实；上节第1—5项进入验证，第6项仍未关闭。

- `SkillChange` 增加可选、仅由服务端创建的 `authorizationSource`：
  `{type:"POSITION", grantId, grantRevision, bindingId}`，修订号为十进制字符串。
  该来源保存在已有 change JSON；不新增购买订单、资金流水或平行安装器。
  旧市场 change 不要求新增字段，原始命令、结果摘要及历史回执不重写。
- `GET /internal/agent/position-skills` 的 R.data 为已持久化的完整当前管理
  Command 数组，而非旧职位安装行。`ps_` 仅用于客户端通道分类；服务端仍核实
  持久化 change 的 owner、Agent、Runtime 绑定、grant 与绑定身份，不以 ID 前缀代替授权。
- Runtime 经现有 `SkillInstallManager.handle` 完成 PREPARE、ACTIVATE 或 POLICY；
  下载复用 `/internal/agent/skill-installations/{skillInstallationId}/package`。
  原职位专用下载和 POST `/{grantId}/receipt` 不再提供。
- `POST /internal/agent/position-skills/results` 的 Q.data 是完整当前 Result。
  R.data 是共享结果服务提交后生成的 ResultReceipt。Runtime 必须验证真实关联回执
  才清理 durable result；不能自行生成 ACK，不消费市场来源的待回执。
  UNKNOWN 只返回后端持久化的 READ，不重放安装。
- 非付费链路锁序为 native fence → shared skill root → position scope root；
  包 IO 在进入事务前准备，在事务内复核审核包与摘要。市场 actor/funds 锁不反向嵌入
  此链路；既有市场入口的身份、购买和资金约束不变。
- 职位安装事实增加可空 `managedInstallationId`，服务端绑定共享的真实不可变安装。
  descriptor 不重复拼接职位副本；新任务资格要求 live grant 和共享 enabled、
  admission、实测 READY。保留安装字节不等于允许新执行。
- 同版本已有合法市场安装可共享，但不擅自开启用户已停用的技能。撤销职位来源不能
  误停其他有效来源；最后来源撤销通过 POLICY 关闭发现视图，保留在途任务冻结引用。
- 实际 native Java/Node fixture 已改为真实管理安装器、实际包下载、共享 SQL 和真实结果回执；
  catalog 由实际 SkillRegistry/local-script runner 测量后注入 fixture 的现有通道边界，
  不虚构 READY。该边界不声称产品 WebSocket/浏览器验收。

必要保护及失败范围：身份/绑定不符只拒绝当前请求；来源撤销禁止新准入，不回放旧任务；
结果摘要/命令/修订冲突拒绝当前结果且不改变原有安装或资金事实。对应实现为
`SkillManagementService.ownedChange/result/qualifies/reconcilePosition`、
`PositionSkillReconciler`；复用 `ArchiveNativeHttpMySqlTest`、`skillManagementContract`、
`skillManagementWire` 和 `archive-position-skills.test.mjs`，不新增区域专项测试。

### 2026-10-25 非付费合同及原生回传路由修正（候选，未发布）

核对源码：API `8823759d6c28535bbbbd0d1b84cd41379d036827`、Web
`58c4cf8676ba0209e347c4a7f692afc879fc2d9c`、Runtime
`dff55140f6fc273ecf39e01c858eb6fc3dad605f`。

- POSITION 来源的 INSTALL 必须为 `price:null`、`orderId:null`、`fundingStatus:NONE`；
  无 POSITION 来源的市场 INSTALL 仍须真实价格和订单。后端、Web 生产解析器和 Runtime
  使用同步 schema（SHA-256 `b4543c09df8a2681c5a4e4fb95bbf2291c39b9715ac247d67db1dd80d33c2257`）。
- 原生安全路由仅开放 GET 职位命令、GET grant receipt、POST `/results`，
  不保留已撤销的职位专用下载和 POST grant receipt。所有开放路径仍验证当前 Runtime
  身份/会话；浏览器 JWT、旧 API key、旧会话不能作为回传证明。
- API292 实际发现 POST `/results` 未加入 narrow lane 而收到 HTTP403；已修正，
  复用 `AgentRuntimeSecurityIntegrationTest` 验证合法回传、浏览器/旧会话拒绝及旧写入口关闭。
- Web312 已通过 3338 个测试（2 pending）及构建；API293 和 Runtime39 验证在途。
  此记录不表示已合 develop、已部署或完整功能验收。

### 2026-10-25 02:03 验证状态更新

当前API候选 `b9dede8bf88e66d6716033e9631d8aba7d43bd78`。API293/294
已越过回传403，但真实安装依赖探测未就绪。API295确认云效公共worker
拒绝bubblewrap创建namespace（Operation not permitted），在Gradle前停止。
不能用假READY、关闭隔离或删除该验收用例取得绿灯。需要具备namespace权限的
受控执行环境，再执行完整native验收；固定同Run源码/制品，不能用本机轻量probe
替代。Web312与Runtime39制品均已核对摘要；Runtime39的11个skip包含实际
沙箱用例，必须保留此验收边界。尚未合develop、部署、生产DDL或功能启用。

### 2026-10-25 用户授权：local-script 普通子进程（取代前述沙箱前提）

用户在 namespace 阻塞确认后明确要求“不用沙箱”。本次仅调整职位技能复用的
`local-script` runner，不取消其他执行链路的隔离，不纳入多区域功能。

- 通过固定 Node 解释器直接启动已审核安装包的入口；`shell:false`，不接受包提供的
  解释器/argv/环境变量。stdin 为 JSON，输入和输出使用真实绝对路径。
- cwd/HOME 为任务私有输出目录，环境仅 LANG/HOME/PATH，不继承 Provider token。
  **这是普通服务账号子进程，不是安全沙箱**：文件及网络权限与 Runtime 服务账号一致；
  不承诺输入/包只读挂载、主机文件不可见、网络隔离。只可授予可信审核包执行权限。
- READY 仍以实际 Node 启动、读输入、写输出、私有 cwd/HOME 和环境读回测量；
  无解释器/不可运行不发布 READY（`SKILL_LOCAL_PROCESS_UNAVAILABLE`），不是硬编码通过。
- 保留授权/安装准入、包与输入摘要、任务绑定、effect 幂等和真实回执。
  包被替换或输入被篡改时拒绝当前执行；输出必须属于本任务目录，不允许路径逃逸/
  符号链接充当交付。结果结构/MIME 与声明不符拒绝当前结果，不伪造完成或自动重放。
- 实现入口：`skill-runners/local-script.mjs`；回归沿用 `skill-local-script.test.mjs`，
  将隔离断言改为真实普通进程语义，取消依赖 namespace 的跳过，保留错误与恢复覆盖。
  跨端继续使用 `ArchiveNativeHttpMySqlTest` 的真实安装/回传/脚本执行，不替换模拟 READY。

截至本节更新：本机定向 10 项通过、0 跳过（仅诊断）；云端及发布状态另记真实 Run，
不能沿用旧 Runtime39 或 API295 作为新行为通过证据。

### 2026-10-25 08:34 当前交付状态

上述普通进程实现已随Client60ed188合入develop，Runtime41、API296真实native链路通过。
四仓已合入；Web313已发布1.16.45。API297/Runtime42构建通过，但均在旧程序替换/停止前
因磁盘空间不足终止安装，生产Runtime仍1.3.1，普通进程新语义尚未生效。
不取消备份/空间保护；position开关、DDL、角色/包授权及最终统一业务验收尚未完成。
准确Run/摘要/现行版本见上述handoff和partial-release-disk-blocker.json，不将功能目标视为上线事实。
