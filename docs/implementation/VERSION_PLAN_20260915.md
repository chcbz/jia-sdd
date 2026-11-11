# CYF 完整版本计划（2026-09-15）

> 状态：产品路线图；不是运行台账，也不直接触发发布。动态任务 Owner、精确 SHA、Flow Run 和阻塞项以 `docs/implementation/TASKS.yaml#runtime_ledger_json` 为准。
>
> 本版替代 `docs/implementation/REQUIREMENT_RELEASE_PLAN_20260914.md` 中“下一个版本为悬赏榜协作 Alpha”的排序：新增的 Agent 产物交付需求先形成独立 R1 版本，避免用户仍无法领取 Agent 实际产物。

## 1. 版本身份与通用规则

1. 一个发布版本是一个不可变的 release manifest：固定根仓集成提交、API/Web/客户端精确提交、Flow Run、同 Run 制品摘要、启用开关、迁移及线上 readback；不是单一仓库的 `package.json` 或 Gradle 版本号。
2. 已有源码、历史 accepted、默认关闭代码、健康检查或模拟 ACK 均不等于产品交付。产品交付需要：范围已合入 `develop`、对应 Flow 成功发布、最小真实业务 readback 通过。
3. 普通代码由责任 Owner 自检后合入 `develop`；不设置独立 Reviewer 队列。API 使用 Flow `5260799`，Web 使用 Flow `4403172`；客户端按 `isp-install` 的版本化源发布。
4. `1.0.x` 永远只承载线上 BUG、可用性、安全补丁和运维修复，不夹带新需求。功能列车可并行开发，但按实际依赖、文件范围和 Flow 资源安排发布。
5. 后端 develop 在北京时间 06:00–24:00 只构建/产物，统一在每日 00:00 发布；前端 patch/相邻 minor 可即时发布，跨两个 minor 或 major 的大版本在每日 00:30 发布。

## 2. 已交付能力与不再作为新版本范围的内容

| 能力域 | 当前产品口径 | 后续处理 |
| --- | --- | --- |
| 案卷阁基本阅读、阅读位置恢复、两身份两客户端隔离 | 用户已验收通过；阅读 UX 已按“书目列表 → 沉浸阅读、目录默认收起”调整 | 后续仅走 `1.0.x` 缺陷修复；不重复纳入新功能版本 |
| 聚义厅横竖屏切换与地图交互 | 用户已验收通过 | 后续仅修真实设备回归，不重做 O00–O04 |
| OAuth 公共客户端、客户端技能刷新、工作目录能力刷新 | 已有 released/归档记录 | 后续仅独立 BUG |
| M1/M2/M3 基础身份、任务、事件、可靠投递源码 | 是 M4/M5 的技术前提；是否启用以当前 release manifest/feature flag 为准 | 不拆成单独产品版本，作为协作能力的底座 |
| 经济 V0 技术切片 | 已有部署与页面基础，但未获得真实资金、安装 ACK、租金业务验收 | 保持“预览/默认关闭”，不能标记为交易上线 |

## 3. 完整版本列车

| 顺序 | 版本 | 面向用户的能力 | 主要需求来源 | 完成定义 | 明确不包含 |
| --- | --- | --- | --- | --- | --- |
| 0 | `1.0.x` | 稳定性与安全补丁 | 线上 BUG、可用性、账号/ACL 回归 | 精确修复提交 + Flow + 健康与故障路径 readback | 新功能、资金、Provider 调用 |
| 1 | `1.3.0` | **Agent 产物交付 R1**：用户可在聊天和悬赏中查看、预览、下载 Agent 已显式分享的文件 | `agent-output-delivery` 的 OD00–OD06 | 真实 Agent 上传、离线后取件、跨身份拒绝、聊天/悬赏两个入口、桌面/移动浏览器下载 | 正式验收、返工、多人协作、资金结算 |
| 2 | `1.4.0` | **悬赏正式交付 R2**：单 Agent 的冻结批次、提交、人工验收、要求修改和返工 | `agent-output-delivery` 的 OD07–OD11 | lease/CAS/冻结版本、提交与验收幂等、返工新 run、批次 UI 的端到端 readback | 多 Agent 联合验收、自动审核、资金结算 |
| 3 | `1.5.0` | **悬赏榜协作 Alpha**：组队建议、工作项拆解/确认、依赖解锁、可解释重派和协作看板 | M4：E01–E08、F01、F06 | 受控多 Agent 从推荐/确认到工作项、成果和人工完成的闭环 | ES 检索平台、真实扣款、无限自动调度 |
| 4 | `1.6.0` | **聚义厅语音会话 Beta**：受控 STT/TTS、录音、取消、错误恢复和会话回写 | `juyiting-voice-conversation` | allowlist 身份与额度内的真实 Provider 调用、审计回执、Web/API readback | 默认全量开放、无限额度、经济结算 |
| 5 | `1.7.0` | **经济与技能市场预览**：不收费的钱包/悬赏/技能目录/安装状态/托管租金展示与试用 | `agent-economy-marketplace` V0 | 所有界面/API 可读回、无真实扣款、默认关闭/灰度边界清晰 | 发银、扣费、退款、真实托管开通 |
| 6 | `1.8.0` | **协作平台增强与运营基础**：检索、ACL 索引、索引重建、协作测试/开关/仪表盘 | M5：F03–F05、G01–G07 | 受控 ES/Rabbit 环境下的索引、恢复、观测和操作 readback | 未授权生产压测、把观测当作 SLO 达标 |
| 7 | `2.0.0` | **经济交易正式版**：真实资金、技能交付、托管租金与补偿 | 经济生产 SDD、W04–W14、R01–R03 | 每一类资金/Provider 操作有明确授权、幂等账本、审计、回滚和真实 Agent ACK | 无授权自动扣款或批量试运行 |
| 8 | `2.1.0` | **性能与生产成熟化**：慢请求治理、启动/依赖优化、容量与安全演练 | `api-performance-3s-slo`、G08 | 真实观测数据驱动的优化收益、受控容量与安全结果 | 以任意 3 秒阈值拒绝可用请求 |

`1.1.0`（阅读/公测可用性）与 `1.2.0`（Agent Runtime v1）是已在当前发布与验收链路中处理的历史列车编号；本计划不把已验收的阅读/双身份/横竖屏需求重新排入待开发版本。若其 release manifest 缺失，仅补发布记录，不重做功能。

## 4. 1.3.0 Agent 产物交付 R1：首个待排版本

### 4.1 R1 已冻结的产品边界

- 用户可在**普通聊天**和**悬赏详情**查看、预览或下载 Agent 对本次运行显式分享的文件；页面必须显示“已分享，不等于正式验收”。
- R1 复用当前 `develop` 的 `AgentTaskArtifactStorage`、`agent_task_artifact`、`artifact-outcomes`、`ArtifactTransferPanel` 与 `ArtifactOutcomePanel`；前两者仍是文件/版本与正式裁决的既有事实源。
- Agent 只能发布本次 `outputs/<runId>/manifest.json` 明示的普通文件。客户端先做安全快照再传输；服务端以短期、run-bound ticket 推导身份、scope、任务和会话，不信任请求中提交的这些字段。
- 私有文件系统成果库继续默认关闭；R1 仍采用现有的 **16 MiB 单文件上限**，只在私有目录、备份/恢复和真实读写准入完成后对受控范围开启。
- R1 不实现悬赏的正式提交、人工验收、返工、多人协作、对象存储、恶意软件扫描器、分片/大文件或资金结算。这些需求按后续版本独立排期。

实现细节、最小数据模型、接口、风险和验收矩阵以
`docs/implementation/V1_3_AGENT_OUTPUT_DELIVERY_DETAILED_DESIGN_20260915.md` 为准。

### 4.2 基线与旧候选处理

| 组件 | 当前事实 | R1 决策 |
| --- | --- | --- |
| 根仓规格 | `origin/codex/agent-output-delivery` = `e2ea0c22`；其中 `latest-baseline-replan.md` 晚于旧方案 | `latest-baseline-replan.md` 覆盖旧 `detailed-design.md` 的实现选型；旧文件仅保留安全/并发测试案例参考 |
| API | `origin/develop` = `bff69fb8`；已有受控文件系统 artifact storage 与 task artifact 路径 | 从最新 develop 重新实现 R1 的 run ticket、自动发布、conversation 映射与用户只读入口；不得整体移植旧 27 提交候选 |
| Web | `origin/develop` = `a9c5224a`；已有聚义厅工作台成果面板 | 从最新 develop 新建入口和共用只读列表；不得以旧 Web 候选覆盖 35 个 develop 后续提交 |
| 客户端 | 规格提到 `29aa70da8bb9f0476379dd6bd9e41731c5219457`，但当前 `isp-install` 本地/远端均不可达 | 另一台电脑必须推送该提交或等价完整分支；在可达前不宣告客户端交付完整 |
| 旧 output-delivery | 旧候选包含 MinIO、ClamAV、独立 output 表及 R1/R2 混合逻辑 | 禁止整体 merge/cherry-pick，也不把 Bucket/扫描器作为 R1 上线前置；不能形成第二套文件事实源 |

### 4.3 R1 并行执行包

1. **RB00/RB01：API 基线与存储准入**：冻结现有 artifact ACL/迁移差异；验证私有目录权限、实际读写、内容哈希和备份恢复。未通过时保持 feature flag 关闭。
2. **RB02：客户端安全导出**：在版本化 `isp-install` 源中实现 manifest 校验、no-follow 快照、私有持久队列和 ACK 丢失恢复；不直接改运行目录。
3. **RB03/RB04：API 自动发布与映射**：实现 run-bound ticket、专用发布桥、conversation deliverable 映射与悬赏 owner 的只读入口；复用既有 artifact 服务的 ACL、事务和版本语义。
4. **RB05：Web 入口**：普通聊天与悬赏详情使用共用成果列表、预览和精确下载；身份/会话切换取消请求并清缓存。
5. **RB06–RB08：集成、发布与核验**：每位 Owner 自检后合入组件 `develop`；API/Web 由 Flow `5260799`/`4403172` 做同 Run 测试、构建、制品与部署。重型资源按实际互斥等待，不设置独立 Reviewer 队列。

### 4.5 范围修订（2026-09-15）

用户已明确 `isp-install` 不在当前需求范围。因此 1.3.0 当前只交付 API/Web 的**成果目录与用户取件 R1**：展示服务端已经正确发布到 `agent_task_artifact` 的 task 成果，并在可证明 task/conversation 归属时映射至聊天。

- 不要求推送、拉取或修改客户端 `29aa70da…`；它不再是本版本 blocker。
- 不把 manifest、客户端安全快照、私有队列、run ticket、Agent 自动上传或 Runtime 发布视为当前 1.3.0 范围；这些是后续独立的 Agent Runtime 输出协议版本。
- `artifact.publish` 目前只是协议常量且服务器入站处理仍 deferred，不能被描述为已可用的自动导出能力。
- 当前 R1 的完成定义改为：已有可信 task artifact 在悬赏/任务和可证明关联的聊天中可被授权用户列出、预览/下载，跨身份/来源拒绝，API/Web Flow 与线上 readback 通过。若没有可信聊天关联，聊天入口保持稳定空态，不伪造映射。

实现基线以 `docs/implementation/V1_3_AGENT_OUTPUT_DELIVERY_DETAILED_DESIGN_20260915.md#16-范围修订isp-install-不属于当前版本2026-09-15优先级最高` 为准。

### 4.4 R1 发布完成定义

- 真实 Agent 可仅从受控 manifest 发布文本、图片或 ZIP；中断后用同一安全快照恢复，不重跑 Agent、不过量生成新版本。
- 聊天和悬赏两个入口的授权用户可读取精确版本；跨身份、伪造 run/source、过期或撤销 ticket 一律拒绝且不泄露元数据。
- 文件 hash 与登记版本一致；页面清楚区分“已分享”和“已正式验收”。
- 私有 storage 的开关、根目录配置、备份/恢复证据、API/Web/client 精确 SHA、Flow Run、同 Run 制品摘要和线上 readback 进入 release manifest。
- 客户端等价提交在 `isp-install` 远端可达并完成版本化发布；此前 R1 只能视为 API/Web 准备完成，不能视为完整产品发布。

## 5. 1.4.0 悬赏正式交付 R2

R2 不与 R1 混发。它复用 R1 的成果版本，范围严格限于**单 Agent、单 required work item**：

1. 任务 claim/start/heartbeat/release 与旧完成入口的服务端拒绝；
2. 事务性提交：lease CAS、冻结 delivery batch、delivery pin、submitted 事件/receipt 同一事务；
3. 人工 `accept`、`request_changes` 与显式 rework；旧批次不可再次验收；
4. 悬赏页面显示交付要求、批次、验收意见、409 冲突与结果未知恢复；
5. MySQL 竞争、响应丢失、重复提交/验收、旧版本验收、返工新 run 的 Flow 验证。

当前 OD07 已有候选，OD08 最新候选为 `28c1c371` 但尚未被视为完成；OD09–OD11 未开始。因此本版本的实现顺序是：OD08 收口 → OD09 → OD10 → OD11。OD10 可提前冻结 UI 契约，但不得在 OD09 事务语义未固定前合入业务调用。

## 6. 后续版本的详细拆包与依赖

### 6.1 1.5.0 悬赏榜协作 Alpha

| 包 | 内容 | 前置 |
| --- | --- | --- |
| C1 | E01 候选约束/评分，E02 组队建议与解释 | 现有身份、ACL、任务状态机 |
| C2 | E03 工作项分解和人工确认，E04 依赖/ready 调度 | B04 lease、任务领域模型 |
| C3 | E05 超时/失败的显式目标重派，E06 风险与自主等级 | D06 可靠补投、E01–E05 |
| C4 | E07 团队确认 UI、E08 工作项看板 | 现有协作事件/前端路径 |
| C5 | F01 Context Pack、F06 accepted/superseded 成果状态 | B06/B07/C01；R1 产物读取可复用但不绑定正式验收 |

发布时默认仅开放低风险、可解释、可人工确认的操作；自动执行与重派不得绕过目标 Agent、租约、ACL 和幂等。

### 6.2 1.6.0 语音会话 Beta

- 完成运行时 host/客户端/前端的 exact develop 收敛；
- 对受控身份启用 STT/TTS，支持录音、取消、错误、会话回写；
- 每次真实 Provider 调用必须记录额度、身份、审计与结果；
- 未提供 Provider 授权、音频样本或额度时，只保留源码/开关准备，不声称 Beta 上线。

### 6.3 1.7.0 经济与技能市场预览

- 收口 W04–W14、R01–R03 的源码、Web、客户端和无扣费 readback；
- 显示钱包、报价、悬赏、技能目录、安装状态、托管租金的预览状态；
- 所有价格、周期、开关和“未实际扣款”状态必须明确；
- 真实钱包发放、结算、退款、技能安装 ACK、租金开通仍留给 2.0.0。

### 6.4 1.8.0 平台增强与运营基础

- F03 Elasticsearch 可部署性与配置；F04 严格 tenant/client/task ACL 索引；F05 可重建派生索引；
- G01–G07 的状态机/ACL/幂等、Rabbit 故障恢复、前端协作流、E2E、flags、迁移手册、仪表盘告警；
- G08 容量和安全演练移动到 2.1.0，以真实样本安排，不成为普通页面发布阻断。

### 6.5 2.0.0 与 2.1.0

- **2.0.0**：在逐项商业授权后，提供真实资金账本、显式认领、结算/取消/退款/补偿、六技能真实安装 ACK、托管租金的开通/续费/补偿。每种资金动作独立设定额度、身份、回滚与审计。
- **2.1.0**：性能仅依据真实慢请求与运行证据排序，完成指标采集、热点优化、启动/依赖优化、容量/安全演练与运营告警；不得把未测算 SLO 变成中断用户请求的硬门槛。

## 7. 执行顺序、并行度与发布节奏

### 7.1 现在开始的并行工作

- **稳定性 lane**：继续独立处理线上 P0/P1 BUG，只发布 `1.0.x`；它优先于任何功能上线。
- **1.3.0 API/Web/客户端/基础设施四包**：路径独立则并行；API 的 schema/事务修改按一个 Owner 串行，重型 Flow 验证按资源等待。
- **1.4.0 设计准备**：可并行冻结 OD09/OD10 契约和测试矩阵，但不在 R1 API 整合路径上写入 R2 业务代码。
- **1.5.0/1.8.0 准备**：可分别做 E01/E03/F03 的契约与路径盘点，不与 1.3.0 争用 API output 路径。
- **语音/经济**：仅进行无 Provider、无资金副作用的源码收敛与测试准备，真实调用等待各自授权。

### 7.2 必须串行的边界

- 同一 API transaction/schema/ACL 路径只有一个实现 Owner；
- API Flow、隔离 MySQL/Rabbit、生产迁移和发布按实际资源互斥等待；
- 同一钱包/Agent 的真实资金或 Provider 操作串行，且不能互相复用授权；
- R1 发布完成前，不启用 R2 提交/验收入口；R2 完成前，不把“文件已分享”显示为“悬赏已验收”。

### 7.3 版本完成与归档

每个版本发布后更新对应 spec 的 `delivery-status.md`、根仓 release manifest 和 SDD 索引。只归档已满足发布完成定义的版本；候选分支、历史证据、未推送客户端提交和默认关闭开关不得被误归档为已交付。

## 8. 当前决策与下一步

- 新的首要功能版本确定为 **`1.3.0 Agent 产物交付 R1`**；原“悬赏榜协作 Alpha”顺延为 `1.5.0`。
- 当前 1.3.0 不依赖 `isp-install` 或客户端候选提交；首个实施动作是盘点现有可信 artifact 生产路径及 task/conversation 精确关联。
- 从最新 API/Web `develop` 创建独立 worktree 收敛当前 R1；不直接合并旧 output-delivery 分支，也不覆盖当前脏工作区。

### 4.6 Day1 技术发布记录（任务/悬赏成果目录）

Day1 已按“已有可信服务端 task artifact”这一收敛范围发布：API `36acfb55b4bd1743b280a48864b77bd931c1dc2c` 经 Flow `5260799` Run `76` 测试、bootJar、同 Run 安装和健康核验成功；Web `4afab07d3d1b52749dcaa179cb2ceeda0dce1257`（包含成果 UI 的父提交 `e7035db8…`）经 Flow `4403172` Run `111` 完整测试、Vite 构建、扫描、同 Run 安装和健康核验成功。Web 同 Run 制品 SHA-256 为 `ead6dc3e3335ad9c008dddc6df9120d47f49548e2ecc265a29be0515befc2bc3`，线上入口及聚义厅入口包已回读到成果目录路由和空态标记。

这只关闭 Day1 的**技术发布**：任务/悬赏详情可列出、预览和精确下载可信 artifact；无可信聊天绑定时聊天保持空态；不包含 Agent 自动上传、客户端改造、正式验收/返工或资金。尚差一项业务验收：由授权用户使用一条已有可信 artifact 的 task，完成同身份读取/下载与第二身份或 client 的拒绝 readback。未提供该受控 fixture 前，不创建生产数据、不读取任何用户 token，也不把匿名拒绝误写为 ACL 业务验收。精确证据见 `docs/implementation/handoffs/OUTPUT-DELIVERY-DAY1-RELEASE-20260915.json`。


## 2026-09-17 1.7.0 启动修订（优先于旧排期）

用户延期1.6语音验收，两个语音任务deferred但不作完成。下个版本为1.7.0经济与技能市场**只读预览**；既有钱包/技能/租金实现复用，新增独立读取能力与无落库试算，不借预览开启真实交易。详设见`specs/economy-readonly-preview-v1-7/`与`docs/implementation/V1_7_ECONOMY_PREVIEW_DETAILED_DESIGN_20260917.md`。

本轮仅API/Web，`isp-install`与客户端改造不在范围；上文6.3“收口W04–W14/R01–R03及客户端”改为只映射本轮只读展示切片，真实资金/安装ACK/托管开通继续留给2.0。旧文档中的Reviewer/云端唯一构建要求服从当前Owner自检与云效不可用期间本地发布授权。1.6已冻结release不动，当前未发布1.7。当前首个policy轻量实现已分派，其余开发/集成包在唯一台账登记，不能将计划Owner当成运行Agent。

## 2026-09-17 下一版本方案修订：个人中心入口闭环

1.7.0已部署且授权12表修复及本轮限定回归通过，用户最终验收待回执，前文“尚未发布1.7”不再是现状。用户确认下一版增加聚义厅个人中心入口。当前提出1.8.0「个人中心与导航闭环」：复用profile与economy-preview，只补可发现入口、双向导航和相关安全/布局回归；详设 `/home/isp/wsps/cyf/docs/implementation/V1_8_PERSONAL_CENTER_DETAILED_DESIGN_20260917.md`。

此为规划方案，未启动实现。建议原1.8平台增强F03–F05/G01–G07后移独立列车、版本号待定，不删除原需求；模型治理仍draft、语音延期、交易2.0与性能2.1范围保留。既有1.7两张hosting表缺口单列，不自动取得迁移权限。预计Web-only，不重发未变API；云效不可用期间继续用户已授权本地测试/构建/release流程，不新增Reviewer。

## 1.8/1.9统一候选最新回执（覆盖早期draft排期）

- `personal-center-navigation-v1-8`：integration-ready，聚义厅个人中心及经济预览导航已完成；按用户要求不单独部署，release/1.8.0保持冻结。
- `command-observability-v1-9`：integration-ready，协作运行只读看板/安全能力发现已完成；已包含1.8并合入两个组件develop、冻结release/1.9.0，未部署。Web308+策略7、API10+制品64、生产bundle隔离浏览器99通过。
- 详设与回执：`specs/command-observability-v1-9/`、`docs/implementation/V1_9_RELEASE_READY_20260917.md`。本轮只通知候选可发布；不开启特权读取/权限，不将整体M5/G07、语音或交易标为完成。
