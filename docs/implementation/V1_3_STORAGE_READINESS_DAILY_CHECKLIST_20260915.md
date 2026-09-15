# 1.3.0 storage/readiness lane：每日切片与准入证据模板

> **范围（2026-09-15）**：仅文档化与非生产静态准备；不修改 `TASKS.yaml`、API、Web、流水线、生产配置或 `isp-install`。本模板以既有 `AgentTaskArtifactStorage` 为对象，供责任 Owner 自检和后续 `gpt_test_runner`/Flow 取证使用；填写模板不等于启用或发布。
>
> **当前产品边界**：1.3.0 只读取服务端已经可信写入的 `agent_task_artifact`，并在可证明 task↔conversation 关联时提供聊天映射。不能把 `artifact.publish`、Agent 工作区扫描、浏览器上传或客户端改造写成当前能力。

## 1. 不可变安全与可用性合同

1. 私有 storage 的失败只允许暂停**新成果写入**（以及尚未开始的新写入准入），不得阻塞或回滚聊天回复、任务终态、既有人工 artifact、已发布 artifact 的授权读取或下载。
2. 不删除已发布文件、不删除待恢复证据、不重跑任务、不伪造成功；记录精确错误类别、对象 scope、artifact 版本和恢复动作。
3. `agent.task-artifact-storage.enabled` 默认保持 `false`。准入证据未齐全时，不扩大写入 scope；已有授权读路径仍按原合同工作。
4. 不使用任意磁盘容量、内存、包大小或性能数字作为门禁。空间证据只记录本次测试制品、备份副本和恢复过程的实际字节需求；性能只记录实际观察值和待办。
5. 私有 root、文件内容、storage URI、凭据和生产路径不进入普通日志、页面 DTO 或 release manifest 的明文敏感字段；证据中只保留脱敏标识、hash 和受控引用。

## 2. `AgentTaskArtifactStorage` 实测准入清单

每一项都要有 `status`、`observed_at`、`environment`、`scope`、`fixture_ref`、`evidence_ref`、`failure_class` 和 `next_action`。`PASS` 只能表示实际执行过；`NOT_RUN`、`FAIL`、`BLOCKED` 都不得推进新写入。

| ID | 必须实测项目 | 最小证明 | 失败处置（只影响新写入） |
| --- | --- | --- | --- |
| ST-01 | **root 与运行身份权限** | 记录绝对 root 的脱敏 ID、API 运行 UID/GID、root/中间目录/对象文件的实际 owner 和 POSIX mode；以 API 运行身份完成创建目录、临时文件、最终对象、读取；确认其他非授权身份不能列出/读取/替换 | 关闭新写入；不改变聊天、任务和既有读路径；记录 `permission`/`io` 错误 |
| ST-02 | **根目录与路径组件不可为符号链接** | root 初始化前后均用 no-follow 属性检查；逐级检查 `v1/<scope-prefix>/<scope-key>/<hash-prefix>/<hash>` 的目录组件；对象必须是 regular file，不能是 symlink、目录、FIFO 或外部路径 | 标记 `corrupt`/`root-identity`；停止新写入和扩大 scope，不跟随链接、不清理未知对象 |
| ST-03 | **写入、幂等与不可覆盖** | 用固定非生产 fixture 调用 `store(scope, bytes, mime)`；记录首次 `newlyCreated`、重复写 URI/版本、同 bytes 不产生第二对象；验证临时 `.upload-*.tmp` 不可被 URI 读取 | 只暂停新写入；保留已发布对象和可审计 orphan，不把重复请求升级成新版本 |
| ST-04 | **hash readback 与长度/MIME** | 记录输入 SHA-256、返回 `StoredObject` 的 `sha256/byteLength/mimeType/storageUri`，再用同 scope 和期望值 `read`；对篡改 bytes、错误 hash、错误长度、错误 MIME 分别证明拒绝 | 标记完整性失败；不提供疑似损坏对象的新下载，不影响其他已验证对象的读取 |
| ST-05 | **精确 scope 隔离** | 至少使用两个 tenant/client/task scope；验证 URI 不泄露本地 root/业务标识，错误 scope、错误 hash、伪造 URI、跨 scope 读取均拒绝；`owns`/`matches` 结果与实际 scope 一致 | 只拒绝受影响对象/新写入；不得放宽 ACL 或把 403 伪装成“无成果” |
| ST-06 | **备份与恢复** | 对非生产 fixture 记录备份前对象清单、每个对象 hash/长度、备份介质/引用、恢复后 root identity、对象 no-follow 属性和逐对象 hash readback；恢复后再次按精确 URI 读取 | 恢复不通过则不启用新写入；已发布读路径按原存储继续服务，不覆盖原 root |
| ST-07 | **错误隔离** | 在非生产隔离 fixture 中注入权限拒绝、root identity 变化、对象 symlink/篡改、I/O 失败或 disabled 状态；确认错误归类为 `INVALID_REQUEST`/`DISABLED`/`IO_FAILURE`/`CORRUPT_CONTENT`，并观察聊天/任务/既有读路径的独立结果 | 仅暂停新写入/准入 scope；不得取消聊天、任务、已发布读取或删除队列/对象 |
| ST-08 | **默认关闭与启动安全** | 未设置 enabled 时实例为 disabled 且不会创建候选 root；显式启用仅接受绝对、非 root、非 symlink 目录和非空 MIME allowlist；记录配置 readback，不写生产配置 | 保持 disabled；不通过静态配置猜测可用，不部署 |

### 2.1 建议的非生产 fixture 组合

- `scope-a = (tenant-a, client-a, task-a)`、`scope-b = (tenant-a, client-a, task-b)`，另加一个不同 tenant 或 client 的负向 scope。
- 至少一种小型文本/JSON fixture；若后续产品要覆盖图片或 ZIP，分别记录 MIME、字节数和 hash，不扩大当前存储实现边界。
- 每个 fixture 的 `fixture_digest` 必须是 fixture 文件或规范化内容的 SHA-256；不得只写“已测试”。
- 破坏性用例只作用于临时/隔离 root；不对生产 root、生产对象、生产备份或运行中的其他 Owner 进程做 chmod、删除、替换或 symlink 操作。

## 3. 每日一个可用版本：1.3.0 四日切片

“可用版本”是当日切片在非生产证据中可独立演示、失败可隔离、已有读路径不退化的候选；不是自动生产发布，也不是把静态准备写成上线完成。每一天均保留上一日可用路径，新增项失败时回到该稳定边界。

| 日切片 | 当日可用结果 | 必须完成的静态/非生产准备 | 明确不做 |
| --- | --- | --- | --- |
| **Day1：task/bounty 成果目录** | 授权用户可在 task/bounty 详情列出既有可信 `agent_task_artifact`，读取精确版本并下载；无成果显示稳定空态 | 冻结来源、task ACL、精确 version/hash/长度/MIME DTO；准备 ST-01–ST-08 的 evidence slots；证明 storage 关闭时旧读路径不变 | 不新增 Agent 自动写入；不做聊天映射；不改 `isp-install` |
| **Day2：可信聊天映射** | 仅当 task↔conversation 关联可由可信服务端事实证明时，聊天成果目录显示同一精确 artifact version；无法证明时保持空态 | 形成 mapping fixture、正向/跨身份负向 readback 选择器；证明映射只引用 artifact version，不复制 bytes、URI 或可改写版本；补齐 API/Web DTO 字段草案 | 不依据聊天文本猜测来源；不把无关联 artifact 展示到聊天 |
| **Day3：UX / 隔离** | task 与聊天入口均有明确 loading/empty/error/forbidden 状态；身份或来源切换不串缓存；下载失败只影响成果面板 | 准备桌面/移动静态验收清单；验证 403/不存在/存储失败的非泄露文案、取消旧请求、重新登录后重查 ACL；保留聊天正文和任务终态回归项 | 不内嵌不受支持内容；不把“已分享”显示为“已验收”；不增加性能硬门槛 |
| **Day4：小范围启用** | 在明确、可回收的非生产/受控 scope 中，既有可信 artifact 读路径与新成果入口可演示；新写入仍以准入证据和授权为前提 | ST-01–ST-08 全部 PASS；记录 flag readback、scope、API/Web exact Flow evidence、同一 manifest 关联、真实列表/下载/跨身份拒绝证据；失败演练后确认仅暂停新写入 | 本任务不执行生产启用、部署、迁移、流水线更新或 `isp-install` 操作 |

### 3.1 Day4 启用前后边界

- 启用前：`enabled=false` 或受控 scope 未获准入时，新成果写入必须被拒绝/暂停；task、聊天、已发布成果读取保持可用。
- 启用后：任何 ST 项失败、root identity 变化、hash readback 不一致、备份恢复失败或错误隔离不成立，都只触发“暂停新写入”处置；不自动扩大范围，不删除已发布对象。
- 恢复后：用新的 `evidence_id`、观测时间、exact commit/tree 和 Flow Run 重新记录；不能用旧 PASS 覆盖新失败。

## 4. Exact Flow / release manifest evidence 字段

以下字段是**证据记录合同**，不是本地启动或部署命令。API/Web 正式证据分别绑定既定 Flow：API `5260799`，Web `4403172`。本任务只准备字段和模板，不触发 Run、不部署。

### 4.1 Root release manifest 必填字段

```json
{
  "manifest_schema": "cyf.release-evidence.v1",
  "evidence_id": "1.3.0-storage-readiness-YYYYMMDD-<nonce>",
  "release_train": "1.3.0",
  "lane": "storage-readiness",
  "scope": "non-production-static-preparation",
  "generated_at": "<RFC3339 with timezone>",
  "root_repository": {
    "repository_path": "<repo identity, no local secret path>",
    "source_commit": "<40-hex or null>",
    "source_tree": "<40-hex>",
    "parent_commits": ["<40-hex>"]
  },
  "components": {
    "api": {
      "repository": "api",
      "commit": "<40-hex or null>",
      "tree": "<40-hex or null>",
      "flow_pipeline_id": "5260799",
      "flow_pipeline_name": "cyf-api-release",
      "flow_run_id": "<exact run id or null>",
      "flow_run_source_commit": "<40-hex or null>",
      "flow_run_source_tree": "<40-hex or null>",
      "test_summary_ref": "<controlled evidence ref or null>",
      "artifact_manifest_ref": "<same-run artifact ref or null>",
      "artifact_digest": "<sha256 or null>",
      "deployment_ref": null,
      "online_readback_ref": null
    },
    "web": {
      "repository": "web",
      "commit": "<40-hex or null>",
      "tree": "<40-hex or null>",
      "flow_pipeline_id": "4403172",
      "flow_pipeline_name": "cyf-web-release",
      "flow_run_id": "<exact run id or null>",
      "flow_run_source_commit": "<40-hex or null>",
      "flow_run_source_tree": "<40-hex or null>",
      "test_summary_ref": "<controlled evidence ref or null>",
      "artifact_manifest_ref": "<same-run artifact ref or null>",
      "artifact_digest": "<sha256 or null>",
      "deployment_ref": null,
      "online_readback_ref": null
    }
  },
  "feature_flags": {
    "agent.task-artifact-storage.enabled": "false|true|not-set",
    "agent.output-delivery.r1.enabled": "false|true|not-set",
    "effective_scope": "<explicit non-production scope or null>"
  },
  "storage_admission": {
    "implementation": "AgentTaskArtifactStorage",
    "root_identity_ref": "<redacted evidence ref>",
    "runtime_identity_ref": "<redacted evidence ref>",
    "checks": [
      {
        "check_id": "ST-01",
        "status": "PASS|FAIL|NOT_RUN|BLOCKED",
        "observed_at": "<RFC3339 with timezone>",
        "environment": "<non-production environment id>",
        "scope": "<fixture scope id>",
        "fixture_ref": "<fixture ref>",
        "fixture_digest": "<sha256>",
        "evidence_ref": "<controlled evidence ref>",
        "failure_class": "<none|permission|symlink|integrity|backup-restore|io|isolation>",
        "next_action": "<one executable action>"
      }
    ],
    "backup_restore_evidence_ref": "<controlled evidence ref or null>",
    "space_observation_ref": "<actual measured bytes only, or null>"
  },
  "readiness": {
    "day_slice": "Day1|Day2|Day3|Day4",
    "task_artifact_readback_ref": "<controlled evidence ref or null>",
    "conversation_mapping_readback_ref": "<controlled evidence ref or null>",
    "ux_isolation_readback_ref": "<controlled evidence ref or null>",
    "cross_identity_denial_ref": "<controlled evidence ref or null>",
    "failure_isolation_ref": "<controlled evidence ref or null>",
    "status": "PREPARED|CANDIDATE|BLOCKED|RELEASED"
  },
  "artifacts": {
    "same_run_binding": "required when flow_run_id is present",
    "artifact_manifest_ref": "<same-run manifest ref or null>",
    "artifact_digest": "<sha256 or null>",
    "fixture_digests": ["<sha256>"],
    "evidence_files": ["<controlled relative ref>"]
  },
  "deployment": {
    "performed": false,
    "deployment_order_ref": null,
    "health_readback_ref": null,
    "online_readback_ref": null
  },
  "decision": {
    "new_writes": "PAUSED|NON_PRODUCTION_SCOPE_ONLY|AUTHORIZED_BY_OWNER",
    "existing_reads": "UNCHANGED|VERIFIED",
    "blockers": ["<exact unresolved question or empty>"],
    "owner_next_action": "<one executable action>"
  }
}
```

### 4.2 Flow Run 与同 Run 制品绑定规则

- `flow_run_source_commit` 必须等于被验证的组件 commit；`flow_run_source_tree` 用于防止只凭分支名认定来源。
- `artifact_manifest_ref` 和 `artifact_digest` 必须来自同一 `flow_run_id`；缺任一项只能记录为准备证据，不能记录为发布证据。
- `test_summary_ref` 至少指向测试选择器、结果、执行时间、fixture digest（如适用）和失败归因；“Flow 成功”单独一行不够。
- `deployment_ref`、`online_readback_ref` 在本任务必须为 `null`，因为本任务不部署；后续发布 Owner 填写 exact deployment/readback 证据。
- `space_observation_ref` 只能保存实际观察到的制品/备份字节需求和来源，不得演变为任意空间阈值或拒绝门禁。
- 根仓 `source_tree`、API/Web `tree`、Flow source tree、同 Run artifact digest、fixture digest 和证据文件引用共同构成可复现绑定；任一不一致时暂停新写入并提出精确阻塞问题。

## 5. 本文完成定义与静态检查

- [ ] 只新增/更新 `docs/implementation` 文档；未触碰 `TASKS.yaml`、API、Web、流水线、生产配置和 `isp-install`。
- [ ] ST-01–ST-08 已列出权限、符号链接、hash readback、备份恢复和错误隔离的实测要求。
- [ ] 明确失败只暂停新成果写入，不影响聊天、任务、已发布读取。
- [ ] Day1–Day4 每日切片可独立说明可用边界，且没有任意磁盘/性能阈值。
- [ ] Flow pipeline/run/source tree/same-run artifact/test/flag/storage/readback/deployment 字段齐全。
- [ ] 未把文档准备、默认关闭或模拟结果写成部署/上线证据。
