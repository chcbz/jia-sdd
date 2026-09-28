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

## 2026-09-28 长期融合研发分支

- [juyiting-multimedia-deliberation 长期融合方案](juyiting-multimedia-deliberation/long-term-fusion-plan-20260928.md)：统一议事与受控执行；fast作为轻量策略，不建设第二套聊天系统。四仓 `codex/juyiting-multimedia-deliberation` 是代码整合/设计基线，不是已实现完整媒体闭环。详设v2、实施计划和34项待执行验收位于同目录。
