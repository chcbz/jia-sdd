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

## 2026-09-27 多媒体悬赏议事流程优化

- [juyiting-multimedia-deliberation](juyiting-multimedia-deliberation/spec.md)：draft / design-only。点将自动议事，支持可选参考资料、多媒体回复与持续修改、主动保存、选定成果验收；复用现有存储及修正后的 fast-deliberation，不建设第三套文件系统。包含详设、开发计划与 22 项待执行验收；未派发、未修改组件 gitlink、未构建/部署。

## 典籍阁 Agent 任职与内容维护方案

- `archive-agent-maintenance`：ready / D2，可交接其他 Agent 从 M0 实施。宋江协调或直达任职 Agent，经技能与受控 API 完成多书/不可变版本、草稿校验及授权发布；保留旧阅读、身份隔离和共享执行/存储合同，不扩旧 ItemRef。入口：[实施交接](/home/isp/wsps/cyf/specs/archive-agent-maintenance/handoff.md)、[详设](/home/isp/wsps/cyf/specs/archive-agent-maintenance/design.md)、[开发计划](/home/isp/wsps/cyf/specs/archive-agent-maintenance/tasks.md)。84 项业务验收均未执行；仅文档提交，无派发、组件 gitlink/运行台账修改、构建部署或生产激活。
