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

## 1.8/1.9统一候选最新回执（覆盖早期draft排期）

- `personal-center-navigation-v1-8`：integration-ready，聚义厅个人中心及经济预览导航已完成；按用户要求不单独部署，release/1.8.0保持冻结。
- `command-observability-v1-9`：integration-ready，协作运行只读看板/安全能力发现已完成；已包含1.8并合入两个组件develop、冻结release/1.9.0，未部署。Web308+策略7、API10+制品64、生产bundle隔离浏览器99通过。
- 详设与回执：`specs/command-observability-v1-9/`、`docs/implementation/V1_9_RELEASE_READY_20260917.md`。本轮只通知候选可发布；不开启特权读取/权限，不将整体M5/G07、语音或交易标为完成。
