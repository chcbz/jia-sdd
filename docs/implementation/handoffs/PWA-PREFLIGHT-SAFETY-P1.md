# Task Handoff: PWA-PREFLIGHT-SAFETY-P1 离线预检安全收敛

> 当前状态以 `docs/implementation/TASKS.yaml#runtime_ledger_json` 为唯一事实源；本文件仅保存跨 tree 的权威 Review 失败矩阵。

## 1. 唯一台账快照

```yaml
owner: null
exact_sha_tree:
  commit_sha: 9fa58c791262d7d787ad5f4e91b4fb74df37766d
  tree_sha: cef2a66a2baf68656ad8fa3b9d6bf7aa9fe95d77
current_gate: blocked_root_cause
blocker: two consecutive authoritative review failures; see section 6
next_action: authorize one bounded Writer remediation for the two remaining P1s
```

## 2. 实现范围

- Branch：`codex/pwa-preflight-safety-p1`
- Worktree：`/home/isp/wsps/cyf/.worktrees/pwa-preflight-safety-p1`
- 允许文件：
  - `tests/juyiting-preflight-safety.mjs`
  - `tests/juyiting-public-beta-preflight.mjs`
  - `tests/juyiting-public-beta-ui-smoke.mjs`
  - `tests/juyiting-preflight-config.test.js`
  - `tests/juyiting-ui-smoke-config.test.js`
- 禁止：网络、凭据、Chromium、OAuth/API/health、生产、部署。

## 3. 关键设计决定

- 安全 PASS 前必须建立终局 CDP/session barrier：等待全部 tracked handlers settled，并在最后浏览器动作后再次 drain terminal errors。
- 已 resolve 的 WebSocket open Promise 不能吞掉迟到 `error/close`；session terminal state 必须传播到最终结果。
- 进程树退出确认、SIGKILL escalation 与 CDP close timeout 必须使用保持 Node event loop 存活的 referenced timer，直至确认或显式失败。
- Reviewer/Writer 分离；Writer 不得自接受。

## 4. 验证证据

- Successor `9fa58c791262d7d787ad5f4e91b4fb74df37766d` / tree `cef2a66a2baf68656ad8fa3b9d6bf7aa9fe95d77`：dependency-free `node:test` 39/39 PASS，clean，`git diff --check` PASS。
- 该 39/39 未覆盖 late-CDP terminal error 与真实 unref event-loop liveness，因此不能晋级。

## 5. 验收条件逐项核对

- [x] OAuth POST / frontend HEAD manual redirect + approved-origin fail closed。
- [ ] 导航/frame/token/Bearer/API origin 的终局 late-event fail closed。
- [x] ambient `process.env` TLS bypass 不能被 `options.env` 隐藏。
- [x] direct UI-smoke 第三方模块加载位于 termination guard 内。
- [ ] Chromium/CDP/npm TERM/KILL 后退出确认与 close timeout 保持 event loop 存活。

## 6. 失败归因

| 连续轮次 | Exact tree | Reviewer | 结论 | 根因 | 有界整改 |
| ---: | --- | --- | --- | --- | --- |
| 1 | `3ffe9bbca0710a0e0db12d18f8f97a010a52fc11` / `9d0f737c48d38a9784ca1445a7238729970ca01f` | `01a039b5-3c58-7ac0-923d-3f1650c8ebd7` | REJECT `0/5/0` | redirect/origin、browser token/API binding、ambient TLS、pre-guard module load、best-effort cleanup 未 fail closed | 形成 `9fa58c7/cef2a66a`，39/39 offline PASS |
| 2 | `9fa58c791262d7d787ad5f4e91b4fb74df37766d` / `cef2a66a2baf68656ad8fa3b9d6bf7aa9fe95d77` | `01a039dd-fbb6-7bb2-b886-f14aa67a6cec` | REJECT `0/2/0` | 最终检查后迟到的 CDP/socket/handler 错误仍可能被吞；cleanup 使用 unref timer，Node 可在 survivor confirmation 前 exit 0 | 仅修终局 handler barrier/error drain 和 referenced cleanup timers；补 late-error + real event-loop-liveness 离线回归 |

> 第二轮后进入 `blocked_root_cause`。只有引用本矩阵的 `authorize-remediation` 可恢复一个 bounded Writer；不得无界重试。

## 7. Reviewer 结论

- First reviewer：REJECT `P0/P1/P2=0/5/0`
- Second reviewer：REJECT `P0/P1/P2=0/2/0`
- 当前 remaining：2 个 P1
- 残余风险：真实 Chromium/CORS 不在本离线整改授权范围内，后续仍需独立受控门禁。

## 8. 主动通知

- Event：`abnormality`
- Summary：连续两个 exact-tree 权威 Review 均 REJECT，已停止普通循环并形成矩阵。
- Executable next action：授权原 Writer 仅修两项 remaining P1，补离线回归，形成新 clean commit/tree 后 fresh review。
- Recorded at：`2026-08-25T17:16:02+00:00`
