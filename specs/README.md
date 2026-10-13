# SDD Specifications

## 先区分意图、实现与历史

- 想了解系统如何工作：先读 [架构与模块知识入口](../docs/knowledge-base/README.md)，不是逐个遍历历史 SDD。
- 想了解准备做什么：读对应 feature 的 spec/design；冻结提案不等于最终实现，须查目录导航和版本证据。
- 已完成范围的稳定知识按 [收口流程](../docs/sdd-workflow.md#feature-documentation-closeout)进入架构/模块/runbook；原合同和验收留原路径取证，不继续作为当前执行步骤。
- [INDEX.md](INDEX.md)中的日期段落是历史投影，不能当作实时状态台账；Owner/gate 仍以唯一运行台账为准。


<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量索引

完整需求见 [INDEX.md](INDEX.md)，跨全部运行/原始规划任务的证据矩阵见 `docs/implementation/SDD_STATUS_20260906.md`。每个 feature 的 delivery-status.md 区分已交付、源码接受、剩余验收。冻结合同只新增补充材料，不能为更新状态破坏 SHA 绑定。归档是历史登记，当前执行只在唯一运行台账。
<!-- END SDD delivery reconciliation -->

This directory is the cross-repository source of truth for feature intent, design, execution, and acceptance.

Create one directory per cross-cutting feature from `_template/`. Keep implementation in the `api/` and `web/` submodules; record the tested submodule revisions in the coordinating root-repository commit.

## Suggested lifecycle

1. Write `spec.md` before implementation.
2. Record cross-service and UI decisions in `design.md`.
3. Split the work by repository in `tasks.md`.
4. Validate the agreed behavior in `acceptance.md`.
5. Commit the relevant submodule pointers together with the specification update.
