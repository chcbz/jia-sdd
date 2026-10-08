# SDD Feature Index

Each cross-repository feature has one directory: `specs/<feature-id>/`.

| Status | Meaning | Required gate |
| --- | --- | --- |
| `draft` | Problem and scope are being clarified. | `spec.md` exists. |
| `ready` | Contract and per-repo tasks are agreed. | `design.md` and `tasks.md` specify API/Web ownership. |
| `implementing` | One or both submodules are changing. | Commits/tests are recorded in `integration.yaml`. |
| `integration-ready` | Candidate API/Web SHAs are pinned. | `./sddw verify <feature-id>` passes. |
| `accepted` | Acceptance criteria and evidence are complete. | Root integration commit is recorded. |
| `released` | A released delivery baseline exists. | Release/deployment evidence is recorded. |

Create a feature with:

```bash
./sddw new <feature-id> "<feature title>"
```

Do not create a feature directory for local-only refactors unless it changes a published contract, shared behavior, release baseline, or both repositories.

## 历史：2026-09-27 多媒体悬赏议事流程优化（当前见2026-10-07补录）

- [juyiting-multimedia-deliberation](juyiting-multimedia-deliberation/spec.md)：draft / design-only。点将自动议事，支持可选参考资料、多媒体回复与持续修改、主动保存、选定成果验收；复用现有存储及修正后的 fast-deliberation，不建设第三套文件系统。包含详设、开发计划与 22 项待执行验收；未派发、未修改组件 gitlink、未构建/部署。

## 典籍阁 Agent 任职与内容维护方案

- `archive-agent-maintenance`：integration-ready / D2 源码集成候选；API/Web/Client 精确提交、远程回执与验证边界见 `specs/archive-agent-maintenance/delivery.md` / `integration.yaml`。Web245PASS、有界跨组件1PASS；API/Client既有失败保留。84 项业务验收仍 `not_run`，未部署或生产激活。

## 2026-10-07 多媒体议事实际状态补录

- [juyiting-multimedia-deliberation](juyiting-multimedia-deliberation/delivery-status.md)：implementing / NOT_COMPLETE。API117、Web177已版本化发布；纯文字、图文理解、原图片生成、可选保存有真实子集证据。新task426最短纯文字完整闭环通过，存在四项确定UI缺口；混合关联/验收、附件-only/澄清、音频、第二账号及Client集成仍见[剩余任务](juyiting-multimedia-deliberation/remaining-tasks-20261007.md)。历史worktree/分支已按范围清理；Codex历史子会话34个已原生删除，当前及Owner主会话保留。本轮未新增构建或部署。

## 2026-10-08 典籍维护合入 develop

原D2源码交付已完成；当前将四仓本次冻结的develop合入既有特性分支。组件合并验证、远端提交及后续服务端结果见 specs/archive-agent-maintenance/delivery.md / integration.yaml，原多媒体实际状态和两份特性入口均保留；未生产部署或激活，84业务用例仍not_run。
