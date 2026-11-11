# CYF 实施与交接入口

现行导航核对：2026-11-10。继承[根AGENTS](../../AGENTS.md)，业务合同从[specs索引](../../specs/INDEX.md)进入。历史M1/M2/M3、旧版本计划、路由和Reviewer安排不作为新任务执行链。

## 当前责任与唯一事实源

| 内容 | 唯一入口 | 边界 |
| --- | --- | --- |
| 当前Agent角色与使用方式 | [项目角色说明](../../.codex/README.md) | 角色按需，不是每次五阶段审批；文档不重复模型配置 |
| 模型/容量路由 | [MODEL_ROUTING](MODEL_ROUTING.yaml) | 配置不是实际spawn/模型可用性证明，不热切换其他活动会话 |
| 活动任务Owner/状态 | [TASKS](TASKS.yaml)中的runtime_ledger_json | 唯一动态任务台账；历史tasks保留来源，不从旧未勾选重开 |
| 操作/定向验证工具 | [编排说明](../../ops/orchestration/README.md) | 复用现有工具，Gradle串行；默认本地，不自动付费Flow |
| 交接内容 | [handoff模板](handoffs/TEMPLATE.md) | 记范围、精确源码、证据、根因/下一步，不是第二任务台账 |
| 验证证据复用 | [SDD流程](../sdd-workflow.md) | 精确tree/selector/fixture/完整证据匹配才复用，不凭旧accepted放行新输入 |
| 全局业务回归 | [119项长期用例](../../specs/juyiting-unified-experience/global-regression.md) | 用例定义、原17历史通过、当轮结果严格分开 |

## 实施顺序

固定实际任务/Owner与验收 → 核对本地及目标基线、真实调用链和责任合同 → 复用工作区实现最小相关改动 → 定向反馈及影响回归 → 自检集成与交接。无需为每阶段另建worktree/Reviewer/审批；有实际并发写冲突才最少量隔离。不覆盖其他脏修改，不改派或停他人进程。

默认本地测试/构建/打包与获授权安装；源码、测试、制品、安装/健康和真实业务验收分别记录。单次单测/构建发布600秒，异常重试经归因重新计时，回归不限时；不按阶段拆分规避、不向业务下传deadline。

没有实际生产操作授权不执行迁移、收费、技能/典籍发布或主机清理。历史任务工具若与现行规则存在差异，先核实真实入口和允许的处理方式，不伪改ledger/计数绕过。

## 历史资料怎么找

旧MASTER_PLAN、M2/M3、COVERAGE、DECISIONS、日期handoff及receipt均是原范围来源，可能含尚未完成的目标，但不自动代表今天的Owner、实现状态或执行授权。按责任专题提供的链接定向追溯，或使用`kb-search.sh --project-all`。全目录角色见[文档总入口](../README.md)，不要默认通读历史总计划。

## 历史来源

本页已按2026-11-10现行责任入口收敛；旧实施记录、状态和被取代规则保留在[原文快照](archive/2026-11-10-documentation/docs__implementation__README.md)，按原位置解释相对引用，不作为今天执行指令。文档更新不等于全量源码/线上复验。
