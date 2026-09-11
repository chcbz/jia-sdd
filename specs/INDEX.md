# SDD Feature Index

Each cross-repository feature has one directory: `specs/<feature-id>/`.

| Status | Meaning | Required gate |
| --- | --- | --- |
| [api-performance-3s-slo](api-performance-3s-slo/delivery-status.md) | implementing | 已建立并独立审查通过全 API 3 秒性能治理 SDD：普通同步接口完整响应 3 秒，SSE/AI/文件/异步任务按首帧、TTFB 或 ACK 3 秒；尚未进入运行台账、实现、验证或发布。 |
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
