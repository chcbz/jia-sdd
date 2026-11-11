# 1.13.19｜聚义厅正式悬赏闭环修复方案

日期：2026-09-23，Asia/Shanghai。版本类型：**1.13 系列 patch / bugfix**。

状态：**implementation candidate_verified / release prepared / business acceptance pending**。2026-09-23 19:11 CST 已完成组件 develop 非覆盖式合入、冻结 release/1.13.19、本地定向测试与制品核验；**尚未部署，不可验收**。历史复现及验收 FAIL 保留。

规格：`specs/juyiting-formal-flow-bugfix-20260923/`；版本登记：同目录 `version-plan.yaml`。这是方案与版本登记，不是第二份运行台账。

## 1. 版本与基线

2026-09-23 本轮只读检查安装记录、前轮健康回读及远端 release refs：

| 对象 | 已核对基线 | 本版要求 |
| --- | --- | --- |
| API 安装 | 1.13.17；commit `12c6884062d879bbe11344261f85d5cc3285bb94`；tree `de8387d6b504b39e7b2f1564a37a667a70787586` | 保留当前 CORS 等线上修复 |
| Web 安装 | 1.13.16；commit `03c8d95fcfcfb76f0ed5a8ce6a0445370f4b409b`；tree `ba28e4e4456c16b7f72c36d84bf15a17fbf5c386` | 源码定位采用对应 worktree，不以旧 web checkout 作为实现基线 |
| 已占用版本 | 1.13.18；Web 身份恢复候选 `fc950fbdca9d2aaf0e68daaa3d38d354c3c495f7` | 已有三个带后缀 release 分支（含本轮新观察到的 r3），不复用、不覆盖；不据此声称已上线 |
| 新增计划 | **1.13.19** | 查询 API/Web `release/1.13.19*` 均为空，定向计划/制品检索未见占用；本文件登记，冻结前再查并发占用 |

特别注意：1.13.18 候选 release-input 的 API 为较旧的 1.13.15，**不能直接拷贝为本版发布组合**。实施开始时重新读取线上、远端 develop 和并发修改；保留 1.13.17 修复，并核对集成 1.13.18 身份恢复改动，不能覆盖式发布。

本轮只登记版本，不填写不存在的新 commit/tree/artifact，也不将健康 UP 等同业务验收。

## 2. 事实、目标与范围

真实复现任务：**#395「吴用竖屏闭环复测-0923-1600」**。430×932 Chromium 移动竖屏触控仿真（非真机）；吴用指派记录成功，但派发 queued/未送达，议事 404，workspace/events 503；主任务 assigned，正式交付为空。证据见 `deliverables/verification/juyiting-formal-flow-wuyong-20260923/manifest.json`。

本版目标：在**同一个正式 taskId** 上完成提出需求、固定版本资料关联、点将、议事、明确执行、真实 PDF 正式交付、验收/返工及归档。只做单 Agent、单必需工作项，优先吴用，备选林冲；不使用扈三娘。

不包含：资金冻结/支付/结算、多 Agent 编排、历史任务批量回填、统一所有 legacy 完成路径、新建平行状态机。PDF/正式提交/返工目前是 **BLOCKED_NOT_REACHED**，不是已证明全部缺实现；必须实测，失败后按证据补修。

## 3. 六项修复方案

| ID / 优先级 | 已有证据 | 修复位置与做法 | 必须验收 |
| --- | --- | --- | --- |
| BF-01 / P1 | assign 200 + assigned，但 queued、dispatchedAt=null；详情回读派发结果丢失 | API AgentServiceImpl 与 Chat AgentWebSocketHandler：逐项核对 ownerJiacn/tenantId/clientId、成员和注册连接。修合法范围解析，拒绝结果分类；复用可持久化命令/事件事实，补足缺失持久化及回读。Web 分开显示已指派、待送达、已接收、执行阶段 | 同一 commandId 可回查，断线恢复不重复执行；跨身份/非成员仍拒绝。未持久化的拒发不能显示“可靠排队” |
| BF-02 / P1 | 榜文议事两次 404 CONVERSATION_NOT_FOUND，新话头无效 | ChatController/JuyitingConversationScopeService：定位真实授权分支，统一三维身份。优先修既有任务会话路径；若采用受保护 task-thread，必须同时打通 conversationId、参与者和实际 Agent 路由，不只追加消息。Web 正确恢复/新建会话 | 首次、新话头、刷新恢复都绑定原 taskId，并收到吴用/林冲实际回复；跨身份仍不可读写 |
| BF-03 / P1 集成缺口 | 上传成功但正式任务没有固定版本关联与执行授权 | HallDraftEditor/JuyiHall/PersonalWorkspace：需求入口明确私人或正式；复用 file-links 和 TASK executions，完成选材→预览→关联→明确确认执行。复用正式交付、decision、rework-executions，不以私人结果替换 | 同 taskId 固定输入版本、真实 TASK 执行和可下载 PDF；未选文件不可读，修改最新文件版本不改变本次输入 |
| BF-04 / P2 | 第三级百宝箱全部“查看”禁用 | JuyiHall/PersonalWorkspace：同层文件详情或局部子视图替代机械 panelDepth 限制；恢复任务来源、选择、滚动位置 | 430×932 从详情上传→查看→返回原任务可操作，无无限嵌套及遮挡 |
| BF-05 / P1 | 正确 actorAgentId 下 workspace/events 都 503 | AgentTaskEventsGate 与 workspace/events Controller：追踪实际失败分支、依赖、开关及 allowlist；恢复授权范围的快照/事件。能力投影说明 TASK 是否就绪及原因，不能把通用执行可用等同正式链路可用 | 有效身份读到真实快照并游标回放；断网恢复不触发新执行；禁用与真实故障区分，不吞错为空列表 |
| BF-06 / P1 | 后端 10 态，前端 6 态，completed 显示“交令” | juyiting 常量、榜单、详情共用十态映射/筛选/计数；保留子阶段及完成依据。“交令”是提交动作，不是已完成文案 | 十态+未知态表驱动测试；legacy completed 不冒称 accepted；已查看/收入案卷不改变正式验收 |

身份混用只是 BF-01/02 的优先排查假设，尚非最终根因。通过关联日志确认拒绝分支；不得删 ACL、放开通配 allowlist 或手动改主状态来“修通”。对外保持防枚举，诊断细节仅在授权内部日志可见。

## 4. 复用接口与最小合同

以下是源码存在的接口，不等于已通过线上验收；实现 Owner 应核对 exact SHA 并补相关合同测试。

| 阶段 | 既有接口与关键字段 | 本版接线/校验 |
| --- | --- | --- |
| 创建 | POST `/agent/hall/drafts`，POST `/agent/hall/drafts/{draftId}/submit` | TASK_CREATE 只创建，不隐式付费执行；返回的原 taskId 贯穿后续 |
| 选材关联 | GET/POST `/agent/tasks/{taskId}/file-links` | POST `{fileId, version, role}`，role 为 INPUT/REFERENCE，带 Idempotency-Key；返回 relationId/relationRevision/ETag。关联不是 runtime 读权限 |
| 撤销关联 | DELETE `/agent/tasks/{taskId}/file-links/{relationId}` | If-Match + Idempotency-Key；解绑不等于撤销既有执行快照授权，UI 明确区别 |
| 点将 | POST `/agent/tasks/{taskId}/assign` | 显式 agentId；指派、briefing 通知和执行是不同事实。未知回执先查询原意图，不另发新命令 |
| 议事 | POST `/chat/stream`；受保护 `/chat/task-threads/{taskId}/team` 及 `/messages` | 选择一条正确授权并真正送达的路径，保留会话恢复。task-thread 消息追加成功不能证明 Agent 执行 |
| 能力/执行 | GET `/agent/personal-workspace/executions/capabilities`；POST `/agent/personal-workspace/executions` | 请求含 conversationId、targetAgentId、taskId、instruction、outputContentMimeType、inputs[{fileId,version}]，带 Idempotency-Key。正式任务禁止遗漏 taskId 或回退 PRIVATE |
| 原意图恢复 | GET `/agent/personal-workspace/executions/request`，GET `/agent/personal-workspace/executions/{executionId}` | 用原 Idempotency-Key 核对；404 不证明在途 POST 未受理。刷新/轮询不重新收费执行 |
| 正式交付 | GET/POST `/agent/tasks/{taskId}/formal-deliveries` | 复用 TASK runtime 输出提交桥接 artifact/version/hash→正式 submitted；浏览器不伪造 lease 或再造重复交付 |
| 验收/返工 | POST `/agent/tasks/{taskId}/formal-deliveries/{deliveryId}/decision`、`/{deliveryId}/rework-executions` | 沿既有 decision/version/幂等合同；要求修改不立即调用 Provider，明确启动后形成新 revision 并保留历史 |
| 恢复 | GET `/agent/tasks/{taskId}/workspace`、`/events` | 显式 actorAgentId；快照与事件版本一致，sinceVersion/Last-Event-ID 回放，权限不降级 |

源码补充：`PersonalWorkspaceExecutionServiceImpl.beginTaskExecution` 已要求可访问的 conversationId 与 taskId/目标一致，恰好一个 ready 必需工作项，并通过有效 CAS/lease 领取和 start。输出提交已有 TASK artifact 与 formal-delivery 桥接。因此重点是**正式会话、必需工作项和授权的正确接线及能力启用**，不是仅给现有 POST 多传 taskId。

- 对 TASK_CREATE/点将产生的工作项做幂等核对：已有合法项则复用，缺失时仅通过受权业务入口建立单个必需项；多项冲突应明确提示，不能随便选第一项、写 DML 或跳过 CAS。
- 服务端 start 可能先于 Agent/Provider 实际运行；running 下必须显示“已建立执行/待客户端接收”等真实子阶段。不要凭开始时间宣称模型已工作。
- 能力返回若仅表达通用 executionAvailable，应兼容增补 TASK 就绪状态/不可用原因；实现前冻结具体字段，不虚构已存在字段。
- 事件携带可关联的 taskId、commandId/executionId/runId/workItemId、版本、结果/错误分类；敏感 lease/storage URI 不给浏览器。复用现有实体，是否需要 schema migration 由持久化差距核对决定。
- 保存/撤销授权、领取、产物提交、验收保持事务和锁顺序；过期 lease、旧版本 CAS、不同请求体复用幂等键必须拒绝。提交网络失败只恢复提交，不再次调用 Provider。

## 5. 用户触发与系统触发

| 主状态/动作 | 触发者与事实 | 展示原则 |
| --- | --- | --- |
| open 待点将 | 用户确认创建正式任务，系统保存 | 草稿不是 open |
| planning 筹划中 | 既有计划入口的真实写入；本版先覆盖显示，不强造必经节点 | 未核实入口不放假按钮 |
| assigned 待开工（已点将） | 用户点将/授权分配，系统记录负责人 | 不证明通知送达或开始执行 |
| running 办理中 | 用户“开始办理/确认交办”后，服务端正式执行桥接领取/start；或既有工作项聚合/返工就绪事实 | 区分待接收、已领取、执行中、返工待启动，不把 busy/聊天当依据 |
| reviewing 待验收 | Agent 提交真实输出，服务端验证并正式 submitted 后自动更新 | “交令/提交成果”属于动作 |
| completed 已完成 | 本版正式路径由用户验收通过，服务端落 accepted/completed | 展示验收依据；兼容完成单独标记 |
| blocked 受阻 | 合法工作项阻塞报告/聚合 | 显示真实原因、等待谁处理及恢复动作，不凭等待时长判定 |
| failed 失败 | 有效失败报告及领域规则 | 与可恢复阻塞区别，保留失败证据 |
| cancelled 已取消 | 用户明确取消，经受权业务命令处理 | 不能由刷新、慢请求或身份 UI 切换伪造 |
| archived 已归档 | 用户对已完成/失败/取消的终态确认归档 | 保留归档前结局，不能用归档制造成功 |

正常路径：`open → assigned → running → reviewing → completed → archived`。返工：用户要求修改后 `reviewing → running（返工待启动）`，用户明确启动新执行，Agent 新版本正式提交后再次 reviewing。不同层次的 delivery=changes_requested 与主任务 running 同时存在，不新增伪主状态。

## 6. 工作顺序与验证

1. **T0 基线与合同**：核对远端 develop/并发路径，固定 Owner 与目标 SHA；完成身份、命令持久化、正式会话/工作项及能力差距核对。需写运行状态时只使用既有 TASKS.yaml 指向的唯一 ledger；无独立 Reviewer。
2. **T1/T2 阻断链路**：BF-01/02/05，先同范围合法成功，再跨身份拒绝、离线/游标重放。不要在 404/503 未解除时反复付费测试。
3. **T3/T4 展示导航**：BF-06 与 BF-04 可不重叠路径并行；派发子状态接 T1 冻结合同。
4. **T5/T6 正式接线**：BF-03 复用接口，核对吴用 runtime 的实际版本、workspace 能力和有效 lease；不改动无关 Agent 服务。
5. **T7 整体验收**：移动竖屏 UI 连续完成同一正式任务。失败归因后修复再测，不把中途换 PRIVATE 或另一个 taskId 当成功。

测试层次：API/Chat 身份隔离与合法派发、文件关联/授权撤销、任务执行幂等/CAS/租约、正式提交/验收/返工及事件回放；Web 十态与未知态、深层文件查看/返回、刷新与未知意图恢复；runtime 收到真实执行并输出可验证成果。Gradle 仅通过 `python3 ops/orchestration/cyf_orchestrator.py gradle ...` 串行，先读对应 build.gradle 选取最小相关测试；代码树未变的有效证据可复用。

## 7. 业务完成标准（全部待执行）

- 430×932 移动竖屏触控 UI，吴用或林冲之一，记录实际运行版本。需真机时另留真机证据，不把仿真冒充真机。复测包含正常登录/刷新身份恢复，凭证不写入文档或截图。
- 新建明确命名的 1.13.19 验收任务，或在原命令/执行事实核对后恢复 #395；**各自使用原 taskId 全程追踪**，不得以新任务通过宣称 #395 已完成。#394 不动，#395 历史失败证据保留。
- 附件使用新的随机独有标记，只写在获授权输入文件内，不能复制到榜文、聊天或 instruction。原复现素材标记为 MATERIAL-WY-395-A，若正文已被复制到其他输入，不足以证明此次读取附件。记录 fileId/version/hash、relationId 和执行授权快照。
- 点将、议事实际回复、明确执行都有对应事实；取得 executionId/runId/workItemId→artifact/version/hash→deliveryId/revision 的同任务证据。
- 下载**真实 PDF**，验证格式/摘要、可打开与内容包含附件独有标记；聊天大纲、私人 result.pdf、本地路径均不算正式交付。
- 至少一次要求修改→明确启动返工→新 revision/supersedes→再次 reviewing→用户 accepted/completed→归档，原交付仍可追溯。接受必须针对最终 revision。
- 刷新/断网重连不重复执行或重复收费；跨身份、未选文件、撤销授权、旧 lease/CAS 负例通过。聊天成功、HTTP200、进程健康均不能替代这些证据。

## 8. 本地发布与恢复

本版采用用户授权的**本地测试、构建、部署**，不触发阿里云 Flow，不虚构 Run；计划 build_origin=`local_user_authorized`，未构建时不填制品摘要。

1. Owner 自检和相关测试通过后合入组件 develop；从验证过的 exact SHA 创建不覆盖现有 ref 的冻结 `release/1.13.19`（如需后缀按既有约定，出现占用先核对，不 force）。记录 API/Web commit/tree，runtime 如修改另记源版本与摘要。
2. 本地正式构建、记录测试选择器/结果、制品 SHA-256 与版本。保留当前安装与可恢复副本；资源仅观测并按实际新旧制品测算，不加任意磁盘/时限门槛。
3. 安装前在发布互斥内重新核对目标版本、制品和进程归属；等待锁，不抢占、不控制 foreign 进程。遵守既有发布时段；本方案不是立即部署命令。
4. 兼容增量按 **API 健康 → runtime（仅确有变更且由合法 Owner 操作）→ Web** 推进；未改 runtime 不重启它。数据库若需迁移先补事务/恢复方案，不因本版登记获得任意生产 DML 权限。
5. 记录安装/健康和同 taskId 业务验收；真实安装失败按可恢复安装规程处理，功能问题优先修复，不用回退掩盖未通过结果。

发布条件：六项问题对应验收通过，正式闭环与返工取得真实证据，必要安全负例通过；不得仅以构建成功或健康 UP 标记 released/accepted。费用授权仅用于已同意的外部 Provider 测试，不涉及资金结算；实际用量无法核实时如实写未知。

**历史计划步骤（已执行）：T0，固定实施基线并定位 BF-01/BF-02/BF-05 的真实失败分支。当前实际下一步见文末候选实施记录。**

## 2026-09-23 19:11 CST 候选实施记录（非上线、非验收）

- API：develop/release/1.13.19 均为 `86b76f70db2c9a16c8c32058ac3219046432fcb9`，tree `002f1da40a6fc58cea6bbd1c28895bc71a7f1e80`；BF-01/02/05 定向测试通过。第一次 bootJar 写包后于 18:50:31 被内核 OOM 杀掉，**不能算成功**；补足本任务临时 swap 后第二次同 tree `BUILD SUCCESSFUL`，证据 `deliverables/verification/juyiting-formal-flow-1.13.19/api-bootjar-swap-remediation-20260923.log`。API JAR SHA-256 `cb485047f7aadb0889ee4a8c8d4c94cf1f28cca767c00663f1c9dc20f22e4c0f`。第二次构建专用 2GiB swap 已关闭移除。
- Web：develop/release/1.13.19 均为 `a23df27de5842665b692f0f306eb54dde5eca8c5`，tree `9c40c403abbc321358548f711bb8a6cd63bee336`；定向 18 PASS，Vite 本地正式构建成功；归档 SHA-256 `8d15eca1e8caf53f2cdb895eba961ffdc00cae5587fc27dddba73ef24a30a724`。扩大选择器的历史失败不抹除、不称全套通过。
- `build_origin=local_user_authorized`，Flow Run 不存在；联合校验 `PASS`、API 与 Web **dry-run 均 PASS**，完整清单与原始日志在 `deliverables/releases/v1.13.19-formal-flow-local-20260923/`。无数据库操作、未消费 Provider、本次未产生额外资金结算。未操作线上进程，现网仍为旧版本；**此处仅代码/制品就绪，不是正式业务验收**。
- 下一步按已约定后端北京时间 2026-09-24 00:00 发布窗口，在锁内复核线上版本、SHA、确切进程及制品后按 API 健康 → Web 执行。若线上或 develop 发生并发变化，先非覆盖式重新归因；不得盲目用旧制品覆盖。之后以 430×932 竖屏、吴用或林冲真实同 taskId 的 PDF→返工→再交付→接受→归档作验收。

### 发布时段单次例外（2026-09-23 19:22 CST）

用户在本任务中明确允许本次 **1.13.19 现在例外发布**；该授权仅覆盖原约定的后端 00:00 发布时间，不扩展至生产 DML、资金结算或其它任务进程控制。仍须由 exact 发布 Owner 核对当前进程/制品归属并在互斥下 API→Web 健康部署，然后再做 430×932 吴用或林冲同任务正式业务验收。授权本身不代表已部署或验收通过。

## 2026-09-24 最终交付补充
原1.13.19计划及中途失败保留；实际最终组合为API1.13.27 + Web1.13.28 + runtime1.13.23。用户改版最新e53b3c3已合入Web a7a3b58并发布。#397吴用的r2六页PDF核验、正式验收、完成、归档及刷新后下载已通过；用户可在“办事概览→案卷”验收。当前结果见`specs/juyiting-formal-flow-bugfix-20260923/acceptance.md`顶部，剩余优化见同目录`remaining-bugfixes.md`。测试为相关定向而非全仓，浏览器为430×932触控仿真而非实体手机；费用未知，不冒充Flow结果。
