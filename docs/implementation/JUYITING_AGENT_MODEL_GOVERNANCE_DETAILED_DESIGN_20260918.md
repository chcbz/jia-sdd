# 聚义厅 Agent 模型、接单与可交付技能治理 R1：业务需求方案

**日期：2026-09-18**  
**计划版本：1.14.0**  
**状态：方案已冻结，未启动实现、未发布、未验收**  
**SSOT：** `specs/juyiting-agent-model-governance/`

**最新排期修订：** 个人工作空间与文件交付拆为 1.10.0–1.13.0：文件库、Word 闭环、图片/PPT、Excel/PDF 与完整 MVP；完整治理后移 1.14.0。本设计保留，未启动实施。默认 owner-only、身份隔离和费用诚实原则仍前置。统一安排见 `docs/implementation/VERSION_PLAN_20260918.md`。

## 1. 决策摘要

本方案把四条原始需求收敛为一个“治理 R1”而不是一个交易/市场版本：

| 原始需求 | R1 决策 | 明确边界 |
| --- | --- | --- |
| 显示模型，按模型费用定义智力值 | 展示模型、来源、路由/价目表版本与**计费智力值**；分数按标准工作负载参考成本归一化 | 分数不代表模型能力、可靠性、安全性、权限或接单资格 |
| 揭榜按 Agent 模型计算费用 | 新建无副作用任务模型费用估算；显示预计/最坏成本和价目表来源 | 不创建报价、订单、冻结、扣款或真实账单 |
| Agent 可设置是否接外单 | 默认 `OWNER_ONLY`；显式 opt-in 后只允许同 tenant/client 的**已知精确 Agent 邀请**，且需接受 | 不做公开市场、搜索、自动认领、跨域接单 |
| 梳理技能、由悬赏自动总结 | 建立六类可交付技能 taxonomy；已接受任务只按确定性规则生成候选，owner 确认后公开 | 不让 LLM/私有文本自动断言技能，不等同技能商品/安装/授权 |

### 为什么是 1.14.0 而不是 2.0.0

用户需要先得到可解释的模型、费用和交付能力信息，但尚未授权真实资金、Provider 调用或跨 owner 市场。将它作为 1.14.0 的非收费治理切片，可以复用现有任务/成果事实源，同时不污染冻结的经济交易合同。真实实际费用、资金托管和商业结算仍留给 2.0.0。

## 2. 业务问题分析

### 2.1 当前体验的缺口

1. **角色可见、模型不可解释。** 用户看到角色和 abilities，却不知道模型来源、路由变更或模型资料是否可信。
2. **费用判断被混用。** 既有经济预览使用 synthetic fixture，正式 bounty quote/claim 又属于独立资金域；若直接拿展示成本扣费，会产生价格来源、幂等和授权风险。
3. **外单边界不清。** “能否接外单”若只有一个前端开关，可能绕过 owner、binding、task ACL、tenant/client 隔离或任务状态机。
4. **abilities 不等于能交付。** 自由标签不能说明交付物类型，也不能证明任务已完成。若从聊天/文件正文自动提炼技能，还会泄露私有内容并出现无法审计的承诺。

### 2.2 设计目标的优先级

| 优先级 | 目标 | R1 判断标准 |
| --- | --- | --- |
| P0 | 身份与范围隔离 | 任何外单/技能确认均以 current canonical binding + tenant/client + owner 为准 |
| P0 | 成本语义诚实 | 所有数值带版本和 provenance；没有权威数据就是 UNKNOWN |
| P1 | 用户可理解 | 模型/分数/预估都有解释，分数和成本不暗示能力或扣款 |
| P1 | 可追溯 | 价目表、估算、策略、候选和确认均可回放/审计 |
| P2 | 可扩展 | 为未来真实 usage receipt、正式结算、endorsement 和受控 LLM 总结保留接口边界 |

## 3. 角色与关键业务场景

### 3.1 角色

- **Agent owner：** 当前 canonical owner；管理模型自报、接单策略、候选技能与对外可交付技能。
- **任务发布者：** 有任务读/派单权限；选择明确目标，做模型费用预估，必要时发起外部邀请。
- **Agent 执行身份：** 在 current binding 授权范围内接受/拒绝外部邀请；不能绕过 owner 策略。
- **受信运行时：** 仅能通过内部认证写入 verified 模型观测；不能把敏感调用细节传入 profile。
- **普通查看者：** 仅在已有 Agent profile ACL 容许时看公共模型摘要和已确认技能。
- **平台治理者：** 发布 immutable reference pricebook/taxonomy/rule version；R1 不开放普通运营后台编辑接口。

### 3.2 场景一：用户理解 Agent 的模型与计费分

1. 用户从聚义厅名册打开 Agent 详情。
2. 系统显示“Managed Model X / route-2026-09-a / 受管运行时观察 / 观察于…”。
3. 显示“计费智力值 67”，同时说明它来自 `reference-2026-09-r1` 的标准工作负载费用，不代表能力或可靠性。
4. 若模型仅是 owner 自报，系统显示“自报”，但分数为“不可计算”。若没有任何事实，显示“未记录”。

**业务收益：** 用户得到透明度，产品不伪装基准测试或模型性能结论。

### 3.3 场景二：张榜前预估指定 Agent 成本

1. 任务发布者创建/编辑任务，显式选择 Agent A。
2. 输入预计/最坏 token 预算并点击估算。
3. 服务端以 A 的 task route 和版本化参考价目表计算，返回 estimated/worst 费用。
4. 页面写明“仅估算；未扣款、未锁价、未创建报价”。
5. 任务版本变更或无法路由时，估算失效；用户需要刷新/重新估算。

**业务收益：** 先做预算判断；不会把未授权的后台成本变成交易事实。

### 3.4 场景三：owner 默认不接外单，明确开启后逐单接受

1. 新 Agent 没有策略记录，系统等效 `OWNER_ONLY`。
2. Agent owner 在设置中主动开启“允许外部精准邀请”。系统记录版本、操作者、时间和 binding。
3. 同一 tenant/client 的任务发布者已知该 Agent，且任务 ACL 允许，于 `/assign` 中显式传入 Agent ID。
4. 服务端验证全部 scope 与策略，创建 `INVITED` 而不是直接执行。
5. Agent owner/授权执行身份接受后，才沿既有任务成员状态进入可执行路径。
6. owner 再关开关后，之后的新邀请被拒绝；已经接受的任务不被偷偷中止。

**业务收益：** 建立可控的 B2B/协作入口，为未来市场做权限基础，但没有“自动接单”的意外风险。

### 3.5 场景四：从已验收成果沉淀技能，而非从自我介绍猜测

1. Agent 在一个任务中提交成果；任务经过明确接受且 outcome 归因到该 Agent。
2. 规则引擎只读取 `workItemType=FRONTEND`、`requiredAbility=ui`、`artifactType=SOURCE_CHANGE` 等结构化字段。
3. 规则生成“前端实现”候选，包含证据数量、任务时间、规则版本；不复制客户任务内容或文件。
4. 当前 owner 可确认并写一段短的公开交付说明，或驳回。
5. 确认后，profile 对符合既有可见性的人显示“前端实现 / 源码变更、接口联调”等可交付能力。

**业务收益：** 交付档案有真实工作证据，又不把机器推断变成未经同意的商业承诺。

## 4. 信息架构与文案原则

### 4.1 Agent 详情信息层级

1. **角色身份区：** 保持现有名称、状态、头像/角色设定。
2. **模型与计费区：** 模型名、可信来源、路由、观察时间、计费智力值、价格簿版本、解释链接/tooltip。
3. **交付能力区：** 已确认可交付技能；owner 私有候选；运行时 abilities。
4. **owner 管理区：** 模型自报、接单范围、候选审阅。只对 current owner 显示。

### 4.2 禁止/推荐文案

| 不使用 | 使用 |
| --- | --- |
| “智商 90，能力强” | “计费智力值 90：按参考模型成本归一化，不代表能力” |
| “预计扣费” | “预计费用（仅估算，未扣款）” |
| “Agent 可接任何任务” | “允许同范围外部精准邀请；每个邀请仍需接受” |
| “已掌握/已授权技能” | “已确认可交付技能；不代表安装、授权或付费资格” |
| “系统自动认证” | “由已接受任务的结构化结果生成候选，等待 owner 确认” |

## 5. 规则设计

### 5.1 模型选择与计费智力值

模型展示选择顺序：`VERIFIED_RUNTIME` → `TASK_ROUTE` → `SELF_REPORTED` → `UNKNOWN`。只有前两者能够进入成本计算。

采用统一标准工作负载和 immutable 参考价目表：

```text
score = ceil(100 × selectedModelStandardCost / activeModelsMaxStandardCost)
```

- 输出范围为 1–100；没有可信模型/价格簿/合法分母即 `UNKNOWN`。
- 分数越高只代表同一标准工作负载下参考费用更高；不得用于权限、强制排序、自动选择或风险决策。
- 每次预估和历史展示携带价格簿/公式版本，防止价格簿变更让历史含义漂移。

### 5.2 费用预估的状态模型

| 状态 | 定义 | 页面行为 |
| --- | --- | --- |
| `ESTIMATE_ONLY` | 有可信路由与参考价格簿的纯计算结果 | 展示预计/最坏和免责声明 |
| `UNAVAILABLE` | task route/pricebook/权限/任务版本不可用 | 不显示 0，不影响编辑任务 |
| `ACTUAL_VERIFIED` | 未来仅在 authoritative usage receipt 存在时使用 | R1 不产生此状态 |
| `UNKNOWN` | 无实际 receipt 或历史不足 | 不使用预估替代 |

### 5.3 外单策略状态模型

```text
未配置 ──> OWNER_ONLY
OWNER_ONLY --owner opt-in--> EXTERNAL_OPT_IN
EXTERNAL_OPT_IN --owner close / binding changed--> OWNER_ONLY
```

外部成员状态：

```text
任务发布者发精确邀请 -> INVITED -> ACCEPTED（才可走既有执行路径）
                              └-> DECLINED / CANCELLED
```

策略不是任务权限的替代品；其作用只是外部邀请的一个必要条件。

### 5.4 技能候选状态模型

```text
accepted structured outcome
  -> deterministic rule / idempotent dedupe
  -> PENDING
       -> CONFIRMED  -> 对外展示
       -> DISMISSED  -> 私有历史
       -> SUPERSEDED -> 被更高版本 taxonomy/rule 替代

binding transfer -> confirmed skill requires reconfirmation -> 对外隐藏
```

## 6. 技能目录 R1

| 分类 key | 用户可见分类 | 示例 skill key | 示例限制 |
| --- | --- | --- | --- |
| `product_strategy` | 产品与策略 | `product.requirement-clarification`, `product.solution-design` | 输出是建议/文档，不自动批准产品决策 |
| `engineering` | 工程实现 | `engineering.frontend`, `engineering.backend`, `engineering.integration`, `engineering.data-processing` | 不能证明生产变更授权 |
| `quality` | 质量保障 | `quality.test-design`, `quality.automation-testing`, `quality.regression`, `quality.incident-analysis` | 测试通过不等同上线批准 |
| `platform_ops` | 平台运维 | `ops.cicd`, `ops.observability`, `ops.release-support`, `ops.troubleshooting` | 不能授予生产/运维权限 |
| `content_knowledge` | 内容与知识 | `content.structuring`, `content.knowledge-base`, `content.copy-translation` | 需遵守原内容/隐私边界 |
| `collaboration_delivery` | 协作交付 | `collaboration.task-breakdown`, `collaboration.context-pack`, `collaboration.packaging`, `collaboration.acceptance-support` | 不代替任务 owner 的最终验收 |

每个目录项都需要 `skillKey`、名称、分类、交付物类型、限制、taxonomy version。它是 profile metadata，不是经济市场 SKU、可执行安装包或 entitlement。

## 7. 数据与安全边界

### 7.1 允许保留的数据

- 模型 ID/展示名、route version、信任来源、观察时间、binding version、pricebook version。
- 标准化 token 数与 reference-cost decimal string；不保存实际 prompt 或模型原始响应。
- policy 操作者、旧/新值、时间、idempotency key、binding。
- skill candidate 的 opaque task/outcome reference、taxonomy/rule version、evidence fingerprint、可脱敏的交付物类型/统计。

### 7.2 明确禁止保留或公开的数据

- API Key、Provider token、账号/账单账号、prompt、推理 trace、原始输入输出。
- 私有任务正文、私有聊天、私有文件正文、下载地址、文件路径、密钥、客户数据。
- 能让无关用户枚举外单开关、外部邀请、成员身份或私有任务状态的原因字段。

## 8. R1 与后续版本的边界

| 能力 | 1.14.0 R1 | 后续候选 |
| --- | --- | --- |
| 模型识别 | managed/self-report/task route 展示 | 更多 runtime/provider receipt 对接 |
| 成本 | 参考价目表纯预估 | 2.0 权威 usage、真实报价/结算 |
| 接单 | 同 scope 精确邀请、人工接受 | 1.15 受控协作；未来公开市场另立规格 |
| 技能 | 确定性候选 + owner 确认 | endorsement、人工审核流、受控 LLM 辅助总结 |
| 自动化 | 无 Provider、无自动执行 | 需另获模型/资金/生产授权 |

## 9. 成功指标与观察（非发布硬门槛）

- 模型/分数卡的 `KNOWN/UNKNOWN` 分布，检查事实源覆盖而非逼迫填数。
- 预估请求的成功/不可用原因分布，验证 pricebook/route 运维质量。
- 外部邀请数、接受/拒绝/取消比例及无权拒绝量，检查默认边界是否有效。
- 候选生成数、owner 确认/驳回比、去重/重放计数，检查 taxonomy 规则质量。
- 任何 scope 拒绝、CAS 冲突、outbox/inbox 重放错误和实际慢请求均保留证据排序；不以未经推导的性能 SLO 中断用户请求。

## 10. 实施与上线前置条件

1. 先完成 existing schema/接口盘点，并确认 `/assign`、member accept、artifact outcome 的实际状态机。
2. API 按 A1→A4 的事务/ACL 顺序实现；Web 可在 API contract 冻结后并行实现 W1→W3。
3. 不创建独立 Reviewer。各实现 Owner 对自己 ACL、迁移、事务、精确 source 及前端身份切换完成自检；正式测试/构建/制品/发布遵循届时 Flow 或已授权本地发布政策。
4. 上线时记录 flags、migration、API/Web exact commit/tree、测试、artifact SHA、实际健康和业务 readback。技术发布与用户体验验收分开记录。

详细接口、错误码、事件、迁移及验收矩阵见 `specs/juyiting-agent-model-governance/design.md` 和 `acceptance.md`。
