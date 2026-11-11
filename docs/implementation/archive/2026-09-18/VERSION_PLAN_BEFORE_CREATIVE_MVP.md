# CYF 最新版本计划（2026-09-18）

> **状态：产品路线图，不是运行台账，也不自动启动实现或发布。** 动态 Owner、精确 SHA、当前 gate、blocker 和 next action 的唯一来源仍是 `docs/implementation/TASKS.yaml#runtime_ledger_json`。
>
> 本计划替代 `docs/implementation/VERSION_PLAN_20260915.md` 的**未来版本排序**；历史发布记录、失败归因和旧计划本身不被改写。版本状态以截至 **2026-09-18** 的实际 release records 为准。

## 0. 2026-09-18 认证体验后的 MVP 修订建议（优先阅读）

详见 `docs/implementation/MVP_VALUE_GAP_ASSESSMENT_20260918.md` 及 `docs/implementation/evidence/mvp-audit-20260918/summary.json`。

**重要纠正：不能再用“到 1.11.0 才新建正式交付”判断 MVP。** 本轮认证读取看到线上已有正式交付入口，发布基线也已包含提交/验收/要求修改；未闭环证明的是实际任务执行、成果生成回传、非空交付、取件和真实返工。只读体验没有运行新任务，不能据此宣称整条链已成功或必然不可用。

因此建议用业务闭环重排：

| 版本 | 本次建议的范围 | 与下文旧排序的差异 |
| --- | --- | --- |
| `1.10.0` | **受控实用 MVP**：自己的一个真实 Agent、一个有用任务模板、真实执行、成果持久化/领取、最小修改/验收、任务找回/失败恢复、身份隔离 | 必要交付接线前移；复用现有 formal delivery，不先做全套模型治理 |
| `1.11.0` | 模型/费用透明、技能沉淀、接单治理与复用增强 | 保留原四项需求，完整计费分/外部邀请/候选总结后置；不重复开发已存在的 R2 |
| `1.12.0` / `1.13.0` | 单 Agent 闭环跑通后，按实际需要交付多 Agent 协作/平台增强 | 不以协作展示或运维组件数量代替用户效益 |
| `2.0.0` | 独立授权的商业交易 | 不作为非交易 MVP 前置；真实执行的底层 Provider 成本仍需授权 |

MVP 的验收不是版本号：真实用户提供材料→Agent 真执行→自动保存成果→用户领取→修改新版本→确认完成→回来仍可取件，全程不靠开发者搬文件/改数据库。首个建议动作是盘点现有 Agent 到 artifact producer 的真实链路，然后在明确用量和业务写入授权后做“黄金任务”验收。

这是一份基于新增证据的**重排建议**，不自动启动实施，不修改唯一运行台账，不自动扩大先前排除的客户端改造范围。下文第 3–5 节保留本轮体验前的排期快照；不再将其“治理优先、R2 全量待建”的前提当作当前能力事实。正式启动前按本节业务目标重新冻结版本切片。

## 1. 当前基线与未结验收

| 项目 | 当前事实 | 后续动作 |
| --- | --- | --- |
| 最新线上版本 | `1.9.6` 已于 2026-09-18 发布：Web `737506e7af06bb4ea4ec2386dc507ec745297481` / tree `05f1c965cd07bb02ef5caaf551f5ab4c87fbfc21`；API 未变，仍为 `e15f7020bf77153912aafce15fc11c67b2f06e11` / tree `551c452f1a81bbc6f6b198452891d2189b967fd8` | 用户刷新实际横屏环境，确认个人中心纯头像入口视觉；该确认不阻塞下一功能设计/开发 |
| `1.9.2` 联合回归 | 已发布；API 46 PASS、浏览器 113 PASS 的技术回归已记录 | 用户侧个人中心、经济预览和实际设备体验验收仍待回执；不能写成已用户验收 |
| 经济只读预览 | 仅预览/无扣款能力已在此前列车交付；真实经济合同仍未完成 | 保持与 2.0 真实资金域隔离 |
| 语音 Beta | 源码/发布准备不等于真实 Provider 启用；用户延期实际启用/验收 | 仅在提供 Provider、额度与音频测试授权后进入独立 release train |

`1.9.6` 为 Web-only 视觉补丁，发布记录为 `build_origin=local_user_authorized`。它不是对未来 1.10.0 功能范围的授权，也不改变真实资金、Provider、生产数据或跨 scope 操作边界。

## 2. 排期原则

1. 每个版本是含 API/Web exact commit/tree、测试、制品、开关、迁移、部署和 readback 的不可变 release manifest，不是单一 package/Gradle 版本。
2. 普通代码由实施 Owner 自检后合入组件 `develop`，不创建独立 Reviewer；正式测试/构建/制品/部署遵循当前云效策略，云效不可用期间仅在已授权的本地发布例外内执行。
3. 版本号 `1.0.x` 仅承载线上缺陷、安全和可用性修复；新功能按下表列车交付。用户验收、技术发布、功能开关启用和“设计完成”必须分别记录。
4. 不因任意性能阈值取消可用请求。性能版本只按照真实慢请求、资源证据和可验证收益排序。
5. 所有跨 owner、ACL、事务、迁移、实际资金和 Provider 操作必须在实施时由责任 Owner 精确核验；路线图不自动授予生产 DML、扣费或第三方调用权限。

## 3. 最新功能列车

| 顺序 | 版本 | 面向用户的能力 | 主要依赖/规格 | 发布完成定义 | 明确不包含 |
| --- | --- | --- | --- | --- | --- |
| 0 | `1.0.x` | 稳定性、安全、可用性补丁 | 真实线上缺陷 | 精确修复 + 测试/健康/readback | 新功能、资金、Provider |
| 1 | `1.10.0` | **Agent 模型、接单与可交付技能治理 R1**：模型/计费智力值、无副作用揭榜成本估算、默认 owner-only 外部精准邀请、任务驱动技能候选 | `juyiting-agent-model-governance` | API/Web 合入、迁移/ACL/CAS/outbox 自检、同版本发布及模型/估算/外单/候选 readback | 真实收费、Provider 调用、公开市场、跨 scope 外单、LLM 自动确认技能 |
| 2 | `1.11.0` | **悬赏正式交付 R2**：单 Agent 冻结交付、提交、人工验收、要求修改和返工 | `agent-output-delivery` OD08–OD11 | delivery batch/lease CAS、验收幂等、返工新 run、端到端 readback | 多 Agent 自动验收、真实结算 |
| 3 | `1.12.0` | **悬赏榜协作 Alpha**：组队建议、工作项、依赖、显式重派、协作看板 | `juyiting-task-collaboration` M4 | 人工可解释的多 Agent 协作闭环；不越过显式 Agent/ACL/租约 | 公开市场、无限自动调度、资金扣款 |
| 4 | `1.13.0` | **协作平台增强与运营基础**：检索、ACL 索引/重建、事件恢复、协作可观测性与开关 | M5 F03–F05、G 系列 | 可重建派生索引、隔离证明、故障恢复/观测 readback | 未授权压测、任意 SLO 作为拒绝条件 |
| P | 语音 Beta（独立列车，版本待授权时冻结） | 受控 STT/TTS、录音、取消、错误恢复、会话回写 | `juyiting-voice-conversation` | Provider/额度/身份 allowlist/审计回执与真实 readback | 默认全量开放、无限额度、经济结算 |
| 5 | `2.0.0` | **经济交易正式版**：权威 usage、真实报价/账本、技能交付、托管与补偿 | 冻结经济生产 SDD + 1.10 事实源 | 分项商业授权、幂等账本、审计、回滚、真实 Agent ACK | 未授权自动扣费或批量试运行 |
| 6 | `2.1.0` | **性能与生产成熟化**：真实慢请求治理、依赖/启动优化、容量与安全演练 | `api-performance-3s-slo`、运营证据 | 真实观测驱动优化和受控演练结果 | 用任意门槛中断可用请求 |

### 排序修订说明

- `1.10.0` 插入在当前 `1.9.6` 之后，优先解决用户已提出的模型透明度、揭榜预算、外单边界和交付技能沉淀；这四项是协作规模化之前的治理基础。
- 原历史计划中的输出交付 R1/R2、协作 Alpha、平台增强没有被删除；对已经技术发布/历史编号的内容保留其 release record，未来未完成的正式交付部分在本计划中继续以 `1.11.0` 排期。
- 语音不是 1.10.0 的 blocker；没有 Provider 与额度授权时只保留独立准备，不以源码存在宣称 Beta 启用。
- 真实费用和真实经济结算不提前到 1.10.0。模型参考成本与 synthetic preview 均不能代替 Provider 实际 usage 或资金授权。

## 4. 1.10.0 详细范围与交付顺序

### 4.1 交付边界

| 子域 | 交付 | 不交付 |
| --- | --- | --- |
| 模型档案 | model/route/source/observedAt、版本化价目表、计费智力值、未知空态 | Provider 密钥/账单、模型实时调用、性能排名 |
| 成本估算 | 任务+显式 Agent 的 estimated/worst 参考成本 RPC 和 UI | quote/order/hold/ledger、锁价、实际扣费 |
| 接单范围 | `OWNER_ONLY` 默认、`EXTERNAL_OPT_IN`、精准邀请和接受、审计 | 公开发现、搜索、自动认领、跨 tenant/client |
| 技能档案 | taxonomy、accepted outcome 确定性候选、owner confirm/dismiss | 私有正文挖掘、LLM 自动确认、商品/安装 entitlement |

### 4.2 API/Web 工作包和依赖

1. **GOV-A0：事实盘点与迁移裁决。** 盘点 current binding、member 状态、outcome、route、pricebook；先证明不改冻结经济 bundle。
2. **GOV-A1：模型/价格簿/分数。** 追加观测、声明、reference pricebook 和 profile read；模型必须对 current binding 可解释。
3. **GOV-A2：无副作用成本估算。** 基于 A1 的 route/pricebook，新 RPC 严格零经济写入。
4. **GOV-A3：接单 policy/外部邀请。** 这一路径涉及 ACL、CAS、成员状态和 binding reset；由一个 API Owner 串行负责。
5. **GOV-A4：taxonomy/候选引擎。** 消费 accepted outcome，走 outbox/inbox 去重；与 A3 可在不重叠表/路径时并行。
6. **GOV-W1/W2/W3：档案、估算、设置/邀请。** 在合同冻结后按前端路径并行；保持 map/roster 分流和显式 target。
7. **GOV-I1：集成发布与 readback。** 先 API 后 Web，记录 flags、迁移、精确 SHA、制品和线上 owner/external/skill 业务回读。

### 4.3 1.10.0 发布门槛

- 不存在模型/价格簿时为 `UNKNOWN`；self-report 不进入权威成本/分数。
- estimate 确实不写经济/任务状态；无 receipt 绝不出现“实际费用”。
- 默认外单拒绝、opt-in 后也只形成 `INVITED`；跨 scope/binding/ACL 均不能绕过。
- 技能候选只来自 accepted structured evidence，需 owner 确认后才公开。
- map/roster 分流、显式 Agent 指派、既有 artifact/经济流程不回归。

## 5. 后续版本依赖

### 5.1 1.11.0 悬赏正式交付 R2

继续完成冻结批次、人工验收、返工和 delivery outcomes。1.10 的 skill candidate 只能消费已接受 outcome，不能反过来替代 1.11 的正式验收状态机；R2 仍是候选证据质量的重要前置。

### 5.2 1.12.0 悬赏榜协作 Alpha

外单 policy 为协作提供最小 owner 同意基础，但不自动带来团队搜索/推荐或自动调度。M4 仍须独立保证任务成员、work item、依赖、重派和 lease/ACL 的正确性。

### 5.3 1.13.0 平台增强

候选技能、外部邀请和模型观测会增加需要可观测/可重放的事件，但不提前把 ES、索引重建或全量运营平台塞进 1.10。仅最小 outbox/inbox/replay 正确性属于 R1。

### 5.4 2.0.0 真实经济

2.0 才能在明确商业、资金、Provider、回滚和生产授权后，将 authoritative usage receipt 与真实报价、扣费/结算结合。`1.10.0` 的 `REFERENCE_PRICE_BOOK_NOT_PROVIDER_BILLING` 和 `ESTIMATE_ONLY` 是安全隔离，不是临时省略。

## 6. 当前无需启动的事项

- 不创建 `TASKS.yaml` 活动项，不指定运行 Owner，不创建独立 Reviewer。
- 不修改 API/Web 生产代码、数据库、价格、经济 quote、Provider 配置或 feature flag。
- 不构建、不部署、不运行 Flow；本次交付是业务设计、SDD ready 化和计划重排。

当用户决定启动 1.10.0 时，首个可执行动作是按 `specs/juyiting-agent-model-governance/tasks.md#0-实施前共同冻结项` 进行只读基线盘点并在唯一运行台账创建有界任务。
