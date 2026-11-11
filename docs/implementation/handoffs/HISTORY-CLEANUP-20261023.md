# 历史工作区与分支清理（2026-10-23）

- 授权：用户要求清理历史worktree、代码分支和Codex历史会话。单Owner，本轮不发布、不重启。
- 仅删除已核对远端develop包含、工作区无tracked/untracked改动、无进程cwd/exe/FD引用的历史checkout；未使用worktree remove --force。忽略项仅历史依赖/Gradle缓存及依赖符号链接，不跟随符号链接删除目标。
- 完成：12个历史worktree、23个本地已合并分支。未修改远端分支。实际净释放约1.17GiB（磁盘存在其他并发写入）；结束可用约1.5GiB。
- 保留：主工作区、未合并提交、脏工作区、典籍阁待改造工作区、后端启动优化候选、PPT预览移除待部署候选、PDF Runtime技能包/安装产物，以及生产数据/备份/活动制品。
- Codex历史会话未改动：调用官方set_thread_archived清理已完成PDF会话时返回“Thread read state is unavailable for this account and host”；不直接修改state/session_index/rollout或SQLite数据库。当前及未完成会话保留。
- 结束核对统一Runtime仍active/PID856671，无服务操作。
- 完整只读盘点、原分支SHA及操作回执：/var/tmp/cyf-history-cleanup-20261023/{inventory.json,cleanup-result.json}。原提交仍可从已核对远端develop历史恢复，无git gc/reflog expire。

## 已移除worktree

- `/home/isp/wsps/worktrees/pdf-agent-skill-20261022/api` @ `7841057b057c012cfa203fb658c1043500be055e`
- `/var/tmp/cyf-common-image-api-20261022` @ `29bd0b302a2fef33b4a573c2b16d90e61354f0c9`
- `/var/tmp/cyf-delivery-acceptance-api-20261022` @ `6dc75fc632ad697bbe29c60a8a257c637ba937d6`
- `/var/tmp/cyf-flow-testfix-20261016/source` @ `51a6410ec02e0fcbb82c8516f0b160eaeea1587d`
- `/var/tmp/cyf-flow-testfix-20261016/trim-source` @ `c1e97923bf2325e3ada33b7e2816f203630f020d`
- `/var/tmp/cyf-unrestricted-api-20261022` @ `1d05101d267bc0e0cf50678fb6d80cb967136d34`
- `/home/isp/wsps/cyf-worktrees/frontend-tmx-timing-20261020` @ `8ece5a25a850ca5bf85a6ce91a0e6be30ab20edd`
- `/home/isp/wsps/worktrees/pdf-agent-skill-20261022/web` @ `669bdc9d6439d1bd7eb71df5ed401202a648f419`
- `/var/tmp/cyf-unrestricted-web-20261022` @ `ddda0d34647074b973d6b95e869c8fb6ad4434b1`
- `/var/tmp/cyf-common-image-runtime-20261022` @ `0e96676d80e1c10917376a99ce2322ce7951c968`
- `/var/tmp/cyf-external-chat-runtime-20261021` @ `c11a078e0fc365c09706d569e0c668bcdb230d9f`
- `/var/tmp/cyf-material-read-runtime-20261022` @ `7dd120f5d3a61559ebf4347aa63b638f7e6a4153`

## 已删除本地分支（恢复标识）

- `/home/isp/wsps/cyf/api` / `codex/common-image-input` @ `29bd0b302a2fef33b4a573c2b16d90e61354f0c9`
- `/home/isp/wsps/cyf/api` / `codex/delivery-acceptance` @ `6dc75fc632ad697bbe29c60a8a257c637ba937d6`
- `/home/isp/wsps/cyf/api` / `codex/flow-testfix-20261016` @ `51a6410ec02e0fcbb82c8516f0b160eaeea1587d`
- `/home/isp/wsps/cyf/api` / `codex/flow-testfix-trim-20261016` @ `c1e97923bf2325e3ada33b7e2816f203630f020d`
- `/home/isp/wsps/cyf/api` / `codex/pdf-agent-skill-20261022` @ `7841057b057c012cfa203fb658c1043500be055e`
- `/home/isp/wsps/cyf/api` / `codex/unrestricted-file-upload-20261022` @ `1d05101d267bc0e0cf50678fb6d80cb967136d34`
- `/home/isp/wsps/cyf/web` / `codex/frontend-tmx-timing-20261020` @ `8ece5a25a850ca5bf85a6ce91a0e6be30ab20edd`
- `/home/isp/wsps/cyf/web` / `codex/pdf-agent-skill-20261022` @ `669bdc9d6439d1bd7eb71df5ed401202a648f419`
- `/home/isp/wsps/cyf/web` / `codex/unrestricted-file-upload-20261022` @ `ddda0d34647074b973d6b95e869c8fb6ad4434b1`
- `/home/isp/wsps/chcbz/isp-install` / `codex/common-image-input` @ `0e96676d80e1c10917376a99ce2322ce7951c968`
- `/home/isp/wsps/chcbz/isp-install` / `codex/external-commission-chat-runtime` @ `c11a078e0fc365c09706d569e0c668bcdb230d9f`
- `/home/isp/wsps/chcbz/isp-install` / `codex/material-read-contract-20261022` @ `7dd120f5d3a61559ebf4347aa63b638f7e6a4153`
- `/home/isp/wsps/cyf/api` / `codex/agent-profile-d4-20261017` @ `b76a1d0aeda572767a6d4734d050121d985bd9c9`
- `/home/isp/wsps/cyf/api` / `codex/api-startup-recovery-20261016` @ `ab379ba8f27a3b1481fc426d6d007ae76b096b2e`
- `/home/isp/wsps/cyf/api` / `codex/juyiting-ui-workflow` @ `510b2937696495b54a9203729784660e62c65082`
- `/home/isp/wsps/cyf/api` / `codex/workspace-remaining-api-20261016` @ `58b4b5f408257c6d5103d915e13c7927c1571e20`
- `/home/isp/wsps/cyf/web` / `codex/agent-profile-d4-20261017` @ `da59a4b8e98920386e7ab52a77463613c2ae5a92`
- `/home/isp/wsps/cyf/web` / `codex/common-image-input` @ `7c7a00897bd87418932cb7c757bce2741fd2ad7c`
- `/home/isp/wsps/cyf/web` / `codex/delivery-acceptance` @ `5ec7e2096f838136ae71b6d4a66e148756aad54d`
- `/home/isp/wsps/cyf/web` / `codex/external-commission-web` @ `44aa9c7159a7e9d0604c606776b790507e411932`
- `/home/isp/wsps/cyf/web` / `codex/workspace-acceptance-fixes-20261016` @ `c84c5a2a279b2a662b4b6b2f1b26c4708317b1ab`
- `/home/isp/wsps/cyf/web` / `codex/workspace-essential-20261016` @ `828460c9c1ce90d083ef9f82f9ce7622bdf4830d`
- `/home/isp/wsps/cyf/web` / `codex/workspace-remaining-web-20261016` @ `3a6b2ba7398459cc8e82e0360e201f451d946edc`
