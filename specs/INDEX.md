# SDD 文档索引

- [架构收敛方案与代码级实施边界](architecture-convergence/spec.md)（2026-10-26：一期候选实施及正式验证中；未发布）。

2026-10-23全目录整理。这里记录文档归属/承接关系，不复制容易过期的生命周期；实际代码、测试、安装、线上健康和业务验收分别查精确证据。根基线 `5e6ab2b6f1a156c320189f17d76941fbe623738a`，本轮未fetch、构建或登录生产。

## 优先入口

- [最新界面原型规格](../web/prototypes/juyiting/specs/prototype-spec.md) → [体验优化规格/详设/待办/验收](juyiting-ui-baseline-20261006/optimization/README.md)。
- [点将册展示](juyiting-agent-skill-display/spec.md) · [技能执行](juyiting-skill-execution/design.md) · [接外单与成果选择验收](juyiting-external-commission-mvp/design.md)。
- [当前实现知识](../docs/knowledge-base/README.md) · [SDD规则](../docs/sdd-workflow.md) · [历史会话接续](codex-history-closeout-20261023/spec.md)。
- [清理映射/备份/保留理由](../docs/sdd-document-map.json)。旧证据中的原文件名/摘要不改写，通过映射或备份追溯。

## 阅读规则

文档导航检查使用 `./sddw check-docs`，命令范围、历史快照与旧源码引用例外见 [SDD检查说明](../docs/sdd-workflow.md#sdd-document-check)。导航通过不等于源码/发布/业务验收通过。

原需求仍保留不等于需要重做；旧版本发布不等于当前线上。互相覆盖的UI提案退出现行入口；分层合同、未完成需求、数据修复计划、证据和工具不按日期或v1/v2命名删除。当前执行遵守根AGENTS：单Owner自检、重任务Flow、develop不自动部署；旧本地生产构建/独立Reviewer/硬SLO中断要求不恢复。

## 账号与权限

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [account-security-foundation](account-security-foundation/spec.md) | 保留独立安全合同及撤销/迁移未完成验收；不因Cookie修复收口整项。 |
| [oauth-public-client-hardening](oauth-public-client-hardening/spec.md) | 保留OAuth独立安全合同和原发布证据，不扩大到全部账号/公测安全完成。 |
| [single-tenant-role-isolation](single-tenant-role-isolation/spec.md) | 保留精确租户/owner隔离及迁移范围；文档整理不授权重跑旧生产数据迁移。 |
| [username-encoding-integrity](username-encoding-integrity/spec.md) | 保留编码/身份合同、源码审计及未授权数据修复方案；它不是可删除的已完成临时修复。 |

## Agent与运行端

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [agent-client-skill-refresh](agent-client-skill-refresh/spec.md) | 保留技能刷新契约和既有发布证据；不是安装/交易或技能执行的替代文档。 |
| [agent-workspace-capability-refresh](agent-workspace-capability-refresh/spec.md) | 保留工作目录能力刷新契约及原发布记录，与资料文件库不同。 |
| [juyiting-agent-model-governance](juyiting-agent-model-governance/spec.md) | 保留模型/价格簿/技能治理未交付目标；旧外部邀请规则的同范围实现以接外单D3.1为准。 |
| [juyiting-agent-skill-display](juyiting-agent-skill-display/spec.md) | D1–D4收敛为稳定spec/design/tasks/acceptance；发布/视觉审计原证据保留。 |
| [juyiting-skill-execution](juyiting-skill-execution/spec.md) | SE-2收敛至design.md并合并澄清；SE-1不再作为实施入口，fixtures/实际结果不改。 |
| [runtime-self-host-onboarding](runtime-self-host-onboarding/spec.md) | 保留自托管文书/登记合同及E2E未验；CYF程序路径遵循固定app规则，不恢复旧releases/current安装。 |

## 任务与议事

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [juyiting-codex-fast-context-20260925](juyiting-codex-fast-context-20260925/spec.md) | 保留上下文/恢复/性能约束与未证实范围；普通议事与执行融合入口看多媒体及技能执行，不重建第二聊天引擎。 |
| [juyiting-conversation-sessions](juyiting-conversation-sessions/spec.md) | 保留业务会话到各Agent会话隔离合同；旧Reviewer/分配安排不是当前执行规则。 |
| [juyiting-execution-recovery](juyiting-execution-recovery/spec.md) | 保留执行回执只读核对合同、contract-pilot工具及证据，不清未知执行。 |
| [juyiting-external-commission-mvp](juyiting-external-commission-mvp/spec.md) | 上一轮已合并旧D2.1/D3和成果验收临时方案；保留当前D3.1与跨账号证据。 |
| [juyiting-flow-repair-20261008](juyiting-flow-repair-20261008/spec.md) | 保留有界既有链路修复和协调证据，不把其他UI发布当本包验收。 |
| [juyiting-formal-flow-bugfix-20260923](juyiting-formal-flow-bugfix-20260923/spec.md) | 保留真实缺陷/修复/剩余项和版本回执；版本计划含追踪证据，不批量删除。 |
| [juyiting-task-collaboration](juyiting-task-collaboration/spec.md) | 保留通讯协作详设与M4/M5未交付目标，单承办UI不是多Agent整体完成。 |

## 多媒体与资料

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [juyiting-creative-delivery-mvp](juyiting-creative-delivery-mvp/spec.md) | 合并1.10实施/验收临时文档；保留文件库合同/未验格式；PPT在线预览已取消，生成下载保留。 |
| [juyiting-multimedia-deliberation](juyiting-multimedia-deliberation/spec.md) | 删除旧任务快照/过期版本预留；保留分层合同、增量约束和不可变证据，不误删基础+补充契约。 |
| [juyiting-voice-conversation](juyiting-voice-conversation/spec.md) | 保留语音基础合同/历史发布与未验边界，Realtime增量单列，不重复建旧STT/TTS接入。 |
| [juyiting-voice-realtime](juyiting-voice-realtime/spec.md) | 保留Realtime适配及启用证据；真实麦克风/扬声器验收不因离线通过而完成。 |

## 知识库

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [archive-agent-maintenance](archive-agent-maintenance/spec.md) | 保留D2数据/权限/版本与待核项；后续通用Runtime/技能解耦方向不等于已实现。 |
| [archive-pavilion-reader-mvp](archive-pavilion-reader-mvp/spec.md) | 保留阅读器、进度/书签/私人手札和内容样本；不因旧pending重复判定后续已测场景。 |

## 界面与导航

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [juyiting-dual-orientation-experience](juyiting-dual-orientation-experience/spec.md) | 保留方向/资源生命周期和真实设备回归；旧布局目标不覆盖最新原型。 |
| [juyiting-lightweight-workbench](juyiting-lightweight-workbench/spec.md) | 保留63条功能追踪、组件/控件定义和已发布证据；旧布局仅回归参考，不是当前UI方案。 |
| [juyiting-live-map-preview](juyiting-live-map-preview/spec.md) | 保留动态地图适配P2合同与P1/P2源码检查点；地图/名册数据流不合并。 |
| [juyiting-ui-baseline-20261006](juyiting-ui-baseline-20261006/optimization/README.md) | 当前入口为optimization；旧原型快照/审计/代码差异只作证据，实际原型在web。 |
| [juyiting-ui-optimization](juyiting-ui-optimization/spec.md) | 保留软键盘/导航/可访问性约束和发布测试；当前样式/流程以最新原型为准。 |
| [juyiting-unified-experience](juyiting-unified-experience/spec.md) | 删除过期工期估算；DRAFT/SUBMISSION/RESULTS冻结契约与发布证据保留，旧调度/本地构建不生效。 |
| [personal-center-navigation-v1-8](personal-center-navigation-v1-8/spec.md) | 保留个人中心/身份导航合同与随1.9.2发布证据；旧1.8未部署是历史阶段。 |

## 经济与市场

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [agent-economy-marketplace](agent-economy-marketplace/spec.md) | 保留冻结bundle及V0独立合同，不按v0/v1命名删除；真实收费/安装/结算仍按原证据边界。 |
| [economy-readonly-preview-v1-7](economy-readonly-preview-v1-7/spec.md) | 保留只读预览独立范围；不能与真实交易合同合并为已上线付费功能。 |

## 性能与交付

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [api-performance-3s-slo](api-performance-3s-slo/spec.md) | 保留性能观测/热点治理和证据；不把3秒目标恢复成拒绝/截流门禁。 |
| [command-observability-v1-9](command-observability-v1-9/spec.md) | 保留独立只读运维看板合同；1.9.2发布及用户验收边界查acceptance。 |
| [public-beta-release](public-beta-release/spec.md) | 保留跨功能公测安全与实际onboarding未完成验收，不当作单次版本发布临时稿。 |

## 历史来源

| 特性入口 | 整理结果与保留边界 |
|---|---|
| [codex-history-closeout-20261023](codex-history-closeout-20261023/spec.md) | 保留已删除会话的唯一摘要/来源索引与清理回执，不再删除。 |

## 已合并删除的独立旧提案

- `juyiting-mobile-flow-ux-v2-20260924` / `juyiting-conversation-first-v4-20260924`：旧交互目标由当前体验规格取代；原实页观察/限定发布声明已并入体验优化acceptance，原文备份可追溯。
- 点将册D1–D4、技能执行SE-1/SE-2收敛到稳定文件名；文件名不再决定哪个是最新。
- 文件库1.10临时计划/验收、旧多媒体任务快照/候选版本预留、统一体验人日估算已合并或删除；关键风险和未覆盖项保留。

## 模板与专项工具

[_template](_template/spec.md) 是创建新跨仓特性的模板，不是业务特性。执行历史 [contract-pilot](juyiting-execution-recovery/contract-pilot/README.md) 和既有tools/fixtures只服务各自范围，清理没有删除或重写这些工具。历史原型快照作为证据保留，不作为Web最新原型入口。
