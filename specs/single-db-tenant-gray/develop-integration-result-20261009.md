# Develop 合并结果 · 2026-10-09

状态：四仓已合并指定 develop，待独立只读审查；功能仍 **NOT_READY**。本任务仅整合，未构建、启动、改数据库、push 或发送验收邮件。

## 可恢复基线

备份：`/mnt/Workspace/cyf-develop-integration-20261009-7aS7ey`（权限700）。四仓 dirty.tar 已在变更前逐一 tar --compare（exit0），本次 SHA256SUMS 再校验均 exit0。原 HEAD、状态、全部 dirty bytes、删除记录、index/worktree binary patches 和 index.before 均保留；没有 stash。完整路径/决策与命令结果见同目录 JSON。

| 仓 | 原 HEAD | WIP checkpoint | develop 合并基线 |
| --- | --- | --- | --- |
| root | `3e3735624f320cd58748ec4ddeee5a5848ecee80` | `00ef7add4c06a37c199428d3c6ac5b4bae827322` | `c82c2a08f11f59042a6bb11034e4fb64bb866756` |
| api | `c080b23c5030e3892249b11043c930d3385bf94f` | `d371ae0ce2fd644ccc480ffa6240bb3c3f676620` | `dafb920cd919efaa535bf2a92cc3557b7e7e5160` |
| web | `c19ac8183a6c51b78f401bb1b633ecb3155898bb` | `7602df03900d3d0f87585b5ce3b00eadc17449b0` | `419b52debf6485901d446c5c6faf0cdbfb197767` |
| runtime | `a2519deed5e79b306b1e52157d528e46f5af147d` | `cacae237211e82838e759b9490d0e945ad85daef` | `cbec7c9db778355236f8dca59492391504c2bf60` |

Root 合并前指针 checkpoint：`6d8db6eb22dc505cde5363d3a8a8d208f12caad0`。API/Web gitlinks 分别为上表合并 SHA；四个指定 upstream 的 `merge-base --is-ancestor` 均 exit0，merge parent 保留确切 upstream。结果文档将另作本地提交，不将合并冒充功能验收。

## 冲突决定

- Root（1）：INDEX 同时保留 feature 与上游独立条目，更新当前 tenant-only 范围；AGENTS 两侧规则保留。
- API（19）：保留上游持久化议事、多媒体、可信 sender、重放/幂等和现行身份合同，并显式传递 feature admission/tenant 范围。保留签名 TenantClaimPolicy，去掉重复 raw tenant 覆盖；TenantScopeHelper 仍精确匹配，0 是普通区域，无 OR tenant0 兜底。调度保持 profile-gated；测试适配上游持久化路线，未证明类型/业务正确。
- Web（5）：保留上游草稿恢复/OAuth 返回导航，并保留 tenant 缓存命名空间与取消 ledger；旧身份键使用完整 tenant/client/owner，缺 tenant 不落入不完整键。锁文件保留上游依赖及 feature fake-indexeddb。
- Runtime（3）：保留上游统一入口、可执行验证、受控图片/检查、inode cleanup、subject profiles 与确认关闭，结合 feature effect/cleanup 控制。未恢复上游退役 managed-host、旧 API-key websocket/bootstrap；保留 V2 helper 的依赖收敛待后续，不激活或验收。

## 实际轻量核验

API Java parse：534 文件/0 syntax errors（exit0；最后一处简单 mock 构造适配在其后，未做类型检查）；Web：37 Vue parse/compileScript、155 JS node --check、lock/package 一致（exit0）；Runtime：84 JS/MJS node --check 及变更 shell bash -n（exit0）。没有构建、测试套件、模块 import 或服务执行。

四仓 unresolved index 均空，tracked dirty 均0；API/Web/Runtime 最终 diff checks exit0。Root 完整 staged diff check exit2：6 份上游历史 Markdown 共12处行尾空格，逐文件确认与 upstream 完全相同（exit0），保留原文；本次解决路径 staged check 与 unstaged check exit0。Root marker rg exit1 表示无匹配，早先 xargs 包装 exit123 同样是无匹配。初始 merge exit1 是预期冲突，不是验收结果。

## 保留项与交接

Root 315 个历史/私有 untracked 不批量入库，均备份保留；4份含 secret-shaped token 的历史 JSON 未提交，未输出值。API/Web 当前干净。Runtime 仅3项未提交：native binary、cost3-existing-stage 和 renewal-digest 私有 diagnostics，完整路径见 JSON。

Root retired DeepSeek、API poiProductionRuntimeClasspathTest/publicArtifactVerifier*、Web build/build.js/build/logo.png 的既有删除保留并可从原 HEAD/patch 恢复；Runtime 上游旧平台删除不复活。旧 R4 证据目录 `/mnt/Workspace/cyf-r4-current-engine-overlay-20261008-7uA4e5` 未动，原 COST3 FAIL 保持 FAIL，未重跑 collector。

结果提交后 STOP-WRITE，由主控串行启动独立只读合并审查。tenant1 聚义厅/任务正常通路、平台前置收敛、构建及同库正向/跨区负向实际验证属于下一阶段；本次未顺手扩范围。
