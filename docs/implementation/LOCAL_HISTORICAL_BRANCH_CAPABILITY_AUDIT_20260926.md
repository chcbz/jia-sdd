# 本地历史分支能力审计与归档（2026-09-26）

## 结论

以 Web `origin/develop@d030a200d95eac6cea7fb0d91c0dd915aacf3ada`、API `origin/develop@3873dd6ab18992c70800658102d492c606216d63` 为基准复核：下列九个本地历史分支没有需要继续移植的独有产品能力。能力已经直接合入、以 patch 等价方式合入，或被更严格的新架构替代。

本次未 cherry-pick 历史实现；删除本地 branch ref 前，已在各组件仓库建立 `refs/archive/20260926/...` 精确归档引用。因根文件系统仅余约 39 MiB，bundle 归档首次尝试被 `pack-objects` 以 out-of-disk 拒绝；没有盲目重试，改用不复制对象的 Git archive refs。机器内 manifest：`.evidence/branch-archive-20260926/manifest.json`。

## Web

| 原分支 | Tip | 历史能力 | 当前结论 | 归档 ref |
| --- | --- | --- | --- | --- |
| `release/1.13.4` | `f0c787e19a` | 百宝箱资料/交付工作台 | 已由新版 `PersonalWorkspace` 替代并扩展 | `refs/archive/20260926/web/release-1.13.4` |
| `codex/release-web-features-20260902` | `b6b20d86c1` | 典籍阅读、手札、选文问案卷书吏与恢复 | 当前阅读器与恢复实现已覆盖并扩展 | `refs/archive/20260926/web/release-web-features-20260902` |
| `feat/c06-c07a-task-workspace-state` | `3f92a694c1` | Workspace snapshot/SSE/reducer 与显式 actor | 当前实现保留并增强 | `refs/archive/20260926/web/c06-c07a-task-workspace-state` |
| `feat/c07bcf-task-workspace-surface` | `8cca8d02db` | Workspace/Timeline、a11y、响应式与 build gate | 当前实现保留并演进 | `refs/archive/20260926/web/c07bcf-task-workspace-surface` |
| `feat/m2-web-base-20260803` | `266583f2e5` | C06/C07 累计集成 | 聚合重复，无独有能力 | `refs/archive/20260926/web/m2-web-base-20260803` |

当前权威入口为 `web/src/components/world/JuyiHall.vue`、`web/src/components/workspace/PersonalWorkspace.vue`、`web/src/components/juyiting/TaskWorkspacePanel.vue`、`web/src/composables/juyiting/useTaskWorkspace.js` 和 `web/src/composables/useArchiveReader.js`。生产配置继续显式启用 task workspace。

## API

| 原分支 | Tip | 历史能力 | 当前结论 | 归档 ref |
| --- | --- | --- | --- | --- |
| `feat/a08-identity-runtime` | `eea866ed72` | canonical identity、首次激活、alias 与审核迁移 | 当前 identity runtime 已覆盖并增强 | `refs/archive/20260926/api/a08-identity-runtime` |
| `feat/b07` | `5ea234e1c1` | task thread 与 message byte-exact scope | 已有 patch-id 等价提交 `95484adf`，并有后续增强 | `refs/archive/20260926/api/b07` |
| `feat/b08` | `2794bd4a1a` | identity 锁序、legacy task compatibility、root reservation | 已有 patch-id 等价提交 `4d514790`，owner scope 更严格 | `refs/archive/20260926/api/b08` |
| `feat/m1-integration-20260728` | `c024126ae2` | 聚义厅 relay 只投递 owned roster Agent | 已由 conversation/task-member/hosting ACL 替代并加强 | `refs/archive/20260926/api/m1-integration-20260728` |

A08 的源码能力存在不代表生产 legacy identity migration 已执行；manifest/snapshot/人工审批边界继续保留。`AgentLegacyTaskCompatibilityService`、identity legacy apply SQL 和 task-thread schema/transaction 层仍承载兼容职责，不属于待删除代码。

## 根仓库 SDD

`origin/feature/ui-optimization@aedbfcfc6fe44aa0ecfc9acf8adb5e0be20be8ea` 中的 Web/API 实现均已进入组件 develop；本次只把 `specs/juyiting-ui-optimization/` 文档纳入根仓库 develop，不采用该历史分支中的旧 submodule gitlink。根仓库从现有本地 `master@0bf9799a4a2bc279a7396454c75be7125bfe9db9` 创建同名 `develop`，保留当前工作区及既有本地历史。

## 执行边界

- 已删除上述九个本地历史 branch ref；精确提交由 archive refs 保留。
- 未删除任何远端分支或 tag。
- 未覆盖其他任务 worktree，未 reset/clean，未处理非本次范围的本地改动。
- 本轮为文档与 Git 引用整理，不运行 Gradle、Vite 构建或业务测试。
