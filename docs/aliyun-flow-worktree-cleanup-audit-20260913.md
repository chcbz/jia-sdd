# 工作树空间回收核对（2026-09-13）

## 原始只读核对范围与结论（12:18 快照）

仅核对 `/home/isp/wsps/cyf/.worktrees`，不扫描任务证据内容，不调用 Reviewer，不执行构建、发布、进程控制或删除。

- 本轮包含 **103 个已登记工作树**及一个普通 `tests` 目录；普通目录未当作 Git 工作树处理。
- 工作树目录汇总约 **7.52 GiB**，不是全部可回收空间。
- 首批筛出 **8 个候选，共 895524864 字节，约 854 MiB / 0.83 GiB**。截至该核对时点均未删除；后续实际执行见文末。
- 首批最终核验时间：**2026-09-13T12:18:50+0800**；责任状态来自当时 `TASKS.yaml#runtime_ledger_json`（更新时间 `2026-09-13T12:16:57+08:00`）。
- 4 个工作树发现未提交/未跟踪改动，已排除：`account-security-foundation-integration`、`final-release-prep-r1`、`prod-api-recovery-502-r1`、`release-web-features-20260902`。

## 首批候选（按依赖顺序）

以下目录前缀均为 `/home/isp/wsps/cyf/.worktrees/`。

| 工作树 | 占用 MiB | 核对 HEAD | 完结任务 |
| --- | ---: | --- | --- |
| `jy-roster-archive-web-20260908` | 242.25 | `d59b97a5b2e7` | `JY-ROSTER-ARCHIVE-WEB-20260908` |
| `home-login-20260907` | 242.29 | `567e95378a18` | `JY-MAP-CONTROLS-20260908` |
| `web-production-flags-p1-knuth-l1ItRZ` | 242.86 | `223981d0eb13` | `WEB-PRODUCTION-FLAGS-P1` |
| `final-api-cumulative-r1` | 29.38 | `7f7360e3f65a` | `M3-RG` |
| `flow-ci-cors-gate-20260911` | 35.25 | `4b94cc252cfa` | `FLOW-CI-BACKEND-R4-RUN` |
| `h06-r48-api-concurrency` | 24.56 | `66f30bc530f9` | `H06` |
| `jy-session-agent-20260910` | 1.76 | `9888214d00e5` | `JY-SESSION-AGENT-20260910` |
| `wx-daily-vote-api-integration-20260912` | 35.68 | `8fe0e096735f` | `WX-DAILY-VOTE-OPT-01A08DAA`, `PERF-RELEASE-01` |

这 8 项的共同证据：

- 当前登记为 linked worktree，具备可保留的本地分支；HEAD 精确匹配责任台账，任务 `done`、Owner 已释放、无 blocker。
- HEAD 已是实时查询的对应远端发布分支祖先。前后端核对 `develop`；`isp-install` 组件按其既有 `master` 核对，不把所有仓库都套成 develop。
- 无跟踪文件改动、无普通未跟踪文件；未发现进程 cwd/打开文件或挂载/工作树锁阻止本轮候选。
- 三个前端候选只有被 Git 忽略的 `node_modules` **符号链接**，没有把真实依赖目录当垃圾删除；其余五个没有被忽略的载荷。
- 完整 commit、分支、远端快照、逐目录字节数见同名 JSON；它是只读快照，不是永久删除白名单。

## 必须保留的依赖与未完结任务

- `m4-f02-transfer-web-20260913/node_modules` 指向 `perf-w04-web-20260912/node_modules`。后者仍是依赖提供目录，不能仅因名称旧或某项功能曾发布就删除。
- `web-a1-97cc912-knuth-bhoecj5s/node_modules` 被两个 ECO 夹具工作树和 `web-production-flags-p1-knuth-l1ItRZ` 引用。本轮保留真实 donor 目录。
- `jy-roster-archive-web-20260908/node_modules` 经由 `home-login-20260907/node_modules` 引用外部目录。因此若执行首批，先移除 roster，再移除 home-login；只移除各自链接，不沿链接删除目标。
- `M4-E05` 等仍在云端验证；`M4-F06` 仍有实施 Owner；E08/F02 还有启用/验收事项。本轮不因 Git clean 或代码已合入就将其工作树当作结束。
- PERF W03/W04 等原分支 HEAD 未由当前发布分支的 Git ancestry 证明包含。可能经过 cherry-pick/重新集成；这不等于功能未发布，也不构成直接删除原工作树的证明。

## 当时拟定的执行方式

只对首批明确路径重新核对 HEAD、任务状态、未提交/忽略内容、实际使用及反向依赖，再使用对应仓库的 `git worktree remove <精确路径>`，**不加 `--force`，不删分支、不清 Git 对象、不删依赖目标**。若任何候选变化，只保留该项，不扩大范围或要求重新构建应用。

原始只读核对没有执行上述删除，也没有把工作树删除加入 `/home/isp/bin/clear_disk.sh` 的定时清理。该脚本继续只去重后端的已证实重复备份。

## 实际执行结果（2026-09-13 12:36 CST）

用户确认后，12:36:05–12:36:46 对以上 8 个精确路径重新核对并逐项执行。

- **7 项已移除并验证，1 项跳过**：除 `h06-r48-api-concurrency` 外，表中其余工作树均已移除。
- 移除目录原分配空间 **869773312 字节，约 829.48 MiB**；执行窗口根盘可用空间净增加 **871768064 字节**。两者口径不同，全盘还受并发写入影响。
- `h06-r48-api-concurrency` 仍被 12 个 `/etc/systemd/system/cyf-h06-r48-focused-verifier*.service` 配置引用，因此保留约 24.56 MiB；未停止、修改或删除这些服务，未重试删除。精确配置清单见执行 JSON。
- 全部实际删除均为不带 `--force` 的 `git worktree remove`；逐项验证目录/登记已移除、原分支及提交树保留。未删除真实共享依赖、其他工作树、证据或数据库。
- 前两个前端候选的外部依赖目标在删除前已不存在（记录 `identity: null`），本次未处理该目标；第三个候选的真实依赖 donor 身份验证未变。不能把链接核对理解为所有开发依赖均可用。
- 12:38 CST 复查根盘 `df` 使用率 **90%**，可用约 **5.2 GiB**；后端 loopback 当时为 `UP`。随后 curl 连接被拒绝，12:41:26 的 `ss` 确认 10018 无监听；部署记录为 `status=activating / phase=activation / recovery=ready`。当前不能声称后端健康，需由发布责任方核验激活结果。本任务未执行本地构建、发布、进程操作或服务重启。
- 持久化执行记录：`/home/isp/wsps/cyf/docs/aliyun-flow-worktree-cleanup-execution-20260913.json`；原始候选 JSON 保留为历史核对快照。

工作树删除未加入定时脚本。剩余项下一步仅核对引用服务是否退役及其责任归属；本次不扩大删除或服务操作范围。
