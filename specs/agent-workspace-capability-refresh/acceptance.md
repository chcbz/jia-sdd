# Agent workspace business capability refresh acceptance

## Acceptance criteria

1. register/presence 的 `abilities` 仅来自当前 `codexWorkdir`，即使 Profile 显式配置 abilities/skills 或安装 `SKILL.md` 也不能混入结果。
2. 输出只包含固定中文项目业务能力，不出现 Codex、Shell、调试、编程语言或框架等通用能力。
3. CYF 聚合目录只有同时具备 Gradle settings 与 `agent/chat/task/oauth/user/kefu/point` 完整签名时，才识别精确业务模块。
4. `jia-*` 局部模块目录可映射对应业务能力；普通项目中的无前缀 `agent/chat/task` 不会误判为 CYF。
5. `weather.py` 或 `weather.html` 工作目录可识别 `天气查询`。
6. `/home/isp` 等宽泛目录不能证明具体项目业务时返回 `[]`。
7. 新增、移除 marker/module/source 文件或切换 workdir 后，下一次 register/presence 重建能力快照。
8. symlink、TOCTOU、FIFO、超限或损坏输入 fail closed，且不上传原始路径、未知文件名、版本或文件内容。
9. API schema、身份、ACL 和任务事务语义保持不变；旧英文能力要求不自动兼容新中文能力。

## Verification evidence

- Client repository: `/home/isp/wsps/chcbz/isp-install`
- Client revision: `d9e966ea1f387d42eb02e2458e7f557dbc16d0d7`
- Client tree: `378d2930f5a684d3c871e7e07fbfea5a291f901e`
- Client tests: `npm test` — 109/109 PASS
- Client config: `OPENCLAW_API_KEY=test node agent-client.mjs --validate` — PASS
- Static checks: 两个 `.mjs` 文件均通过 `node --check`；`git diff --check` — PASS
- Independent review: `sol_reviewer` 最终 ACCEPT；P0/P1/P2 均无。一个非阻塞 P3：受限 `package.json` 解析结果已不参与 abilities，可后续清理。
- Source/deployed SHA-256: `458186745240b41a200ff99f28772fc15bd7b74ee2e783e0602c1122d12d88cf`

## Production smoke — 2026-08-24T23:36:36Z

- 安装命令已执行并启动服务：`START_CODEX_WS_AGENT=y bash /home/isp/wsps/chcbz/isp-install/shell/codex_ws_agent_install.sh`
- `codex-ws-agent.service`: active；验证时 Main PID `1472095`
- 三个本地 Profile WebSocket 均已连接 `127.0.0.1:10018`
- API health: HTTP 200
- Public site: HTTP 200
- 部署文件 hash 与 client revision 源文件一致

本地 Profile runtime 快照：

- 林冲：`[]`
- 卢俊义：`["天气查询"]`
- 吴用：

```json
[
  "聚义厅协作",
  "智能体管理",
  "智能体调度",
  "会话消息",
  "多智能体协作",
  "任务协作",
  "身份认证",
  "用户体系",
  "客服系统",
  "积分体系",
  "微信生态",
  "短信服务",
  "域名与主机管理",
  "内容管理",
  "工作流编排",
  "短链接服务"
]
```

## Mixed-client residual

扈三娘、李逵通过外部/public WebSocket endpoint 连接，不属于本机三个 Profile 的 `codex-ws-agent.service` 进程。其旧客户端仍上报：

```json
["codex", "shell", "code-edit", "debug", "deploy-assist"]
```

这不代表新逻辑失效；需在两者实际客户端主机升级后才能刷新。不得通过手工修改 `agent_runtime` 数据掩盖旧客户端状态。
