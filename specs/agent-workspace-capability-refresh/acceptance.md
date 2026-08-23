# Agent workspace capability refresh acceptance

## Acceptance criteria

1. CYF 工作目录可识别前端、后端、Vue、Java、Gradle、测试和文档等固定能力标签。
2. 仅含 Python/HTML 文件的隔离工作目录可识别 `python` 与 `frontend`。
3. 宽泛 home/host 目录在没有项目 manifest 或直接源码标记时不产生推断能力。
4. 新增或移除 marker/source 文件后，下一次 presence 重建能力快照。
5. symlink/TOCTOU、FIFO、超限或损坏 manifest fail closed，且不上传原始路径、未知文件名或文件内容。
6. 现有 Skill、显式 Profile abilities、API 身份和任务事务语义保持兼容。

## Verification evidence

- Client revision: `90de939a10877a68fa7188b33a3181b7b16f0eb8`
- Client tree: `88c6794142595b406c42fdac6282f6c0da33169f`
- Client tests: `npm test` — 119/119 PASS
- Client config: `OPENCLAW_API_KEY=test node agent-client.mjs --validate` — PASS
- Static checks: both changed `.mjs` files passed `node --check`; `git diff --check` — PASS
- Independent review: `sol_reviewer` ACCEPT; P0/P1/P2/P3 均无；祖先替换和 package symlink 攻击探针均为 0 次越界，5000 次扫描无 FD 泄漏。
- Deployed client SHA-256: source and `/home/isp/apps/codex-ws-agent/agent-client.mjs` both `b44c8276dc117351d170ff52ff666bcdaf216b6ed67a3166273faa269911fd8a`.

## Production smoke — 2026-08-23

等待两个 30 秒心跳周期后：

- `codex-ws-agent.service`: active
- WebSocket connections to `127.0.0.1:10018`: 3 established
- Local API `/actuator/health`: HTTP 200, status UP
- Public site `https://kit.chaoyoufan.cn/`: HTTP 200
- `jia.agent_runtime.abilities`:
  - 林冲 `/home/isp`: `["codex","shell","code-edit","debug","deploy-assist"]`，无工作区项目标签；
  - 卢俊义隔离目录: 基础能力 + `source-code/frontend/python`；
  - 吴用 `/home/isp/wsps/cyf`: 基础/Skill 能力 + `git/source-code/workspace-guidance/frontend/backend/nodejs/javascript/typescript/vue/vite/java/gradle/deployment/automation/testing/documentation/assets`。

发布验证时发现 API 已于 2026-08-23 20:24:11 CST 被主机 OOM killer 杀死，早于本次客户端发布。为完成验证，仅重新启动现有 `/home/isp/hosts/cyf/api/cyf-api-kit.jar`，未拉取、构建或部署 API 源码。
