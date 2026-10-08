# Juyi Hall Runbook

This is the short working guide for future 聚义厅/Juyi Hall iterations. Use `docs/juyiting-feature-guide.md` for deeper flow details.
For map masking, prop depth, occluder assets, and future map expansion, use `docs/juyiting-occlusion-system-design.md`.
Historical occlusion implementation sequencing is recorded in `docs/juyiting-occlusion-system-execution-plan.md`; current execution and model routing follow `AGENTS.md` and `docs/implementation/MODEL_ROUTING.yaml`.
Historical occlusion visual findings are recorded in `docs/juyiting-occlusion-visual-review-v0.md`; they do not add a separate Reviewer or release approval gate.

## 开发规范入口

遵循 `AGENTS.md`：聚义厅低于 `2.0.0` 均为内测版本，不考虑旧版本兼容，以最新契约为准；Owner 自检，无独立 Reviewer。下列数据边界是当前实现契约，变更时同步更新实现、测试与文档；安全、数据操作授权和 Flow 验证不因内测而取消。

## Primary Files

| Area | Files |
| --- | --- |
| Page composition | `web/src/components/world/JuyiHall.vue` |
| Map stage | `web/src/components/juyiting/HallStage.vue` |
| Map character token | `web/src/components/juyiting/AgentToken.vue` |
| Roster panel | `web/src/components/juyiting/AgentPanel.vue` |
| Bounty/task panel | `web/src/components/juyiting/BountyPanel.vue` |
| Chat/command panels | `web/src/components/juyiting/ChatPanel.vue`, `web/src/components/juyiting/CommandPanel.vue` |
| Selected agent summary | `web/src/components/juyiting/SelectedAgentCard.vue` |
| Data loading | `web/src/composables/juyiting/useHallData.js` |
| Conversation/events | `web/src/composables/juyiting/useHallConversation.js` |
| Movement/positioning | `web/src/composables/juyiting/useHallScene.js`, `web/src/game/scenes/HallScene.js`, `web/src/game/entities/HallAgent.js` |
| Role portraits | `web/src/composables/juyiting/useWaterMarginRoles.js` |
| Constants and role metadata | `web/src/constants/juyiting.js` |
| Visual assets | `web/src/assets/juyiting/` |

## Current Data Boundaries

- `mapAgents` is for the map stage and comes from `GET /agent/map`.
- `agents` is for roster, recommendations, ability options, and selected-agent detail surfaces.
- Roster filtering calls `POST /agent/roster`.
- Task search calls `POST /agent/tasks/search`.
- Task assignment calls `POST /agent/tasks/{taskId}/assign` with an explicit `agentId`.
- 宋江首领自动协同 uses `GET /agent/capabilities`, `POST /agent/tasks/{taskId}/recommend`, and `POST /agent/tasks/{taskId}/auto-assign`; recommendation results should remain explainable and manual assignment remains the fallback.
- Runtime abilities are client-owned snapshots: `agent.register` and `agent.presence` may refresh `agent_runtime.abilities`; persona abilities are fallback defaults only.
- Juyi Hall chat sends through `POST /chat/stream` and receives events from `GET /chat/conversation/events`.
- 招贤令 binding calls `POST /agent/personas/{personaCode}/bind`; `mode=server` provisions `/home/isp/apps/codex-ws-agent` and `/home/isp/hosts/cyf/agent-clients/{agent}`, while `mode=local` returns user-side install/config guidance.
- Do not use `/agent/active` for Juyi Hall.

## Role Portrait Rules

- Role matching is done by `portraitRole(agent)` in `useWaterMarginRoles.js`.
- Role metadata is in `portraitRoles` inside `web/src/constants/juyiting.js`, covering all 108 Water Margin prototypes with rank, star name, name, nickname, palette, and motif.
- If an agent has `agent.avatar`, that wins.
- Per-role assets live under `web/public/juyiting-portraits/`: all 108 prototypes have static SVG fallback portraits, plus realistic PNG portraits as 4 single images and 26 `water-margin-atlas-*.png` 2x2 sheets. Do not place static files under `web/public/juyiting/`, which collides with the `/juyiting` route.
- `useWaterMarginRoles.js` prefers explicit agent avatars, then custom generated SVG for `visualConfig`, then realistic PNG/atlas portraits for matched roles, and finally the static SVG fallback. Do not reintroduce the old 3x2 sprite-grid fallback.

## UI Invariants

- Map filtering and roster filtering are separate. Changing roster status should not remove map agents.
- 厅中实景浮动点将列表用未筛选 `/agent/roster` 的当前用户可操作投影，不用 `mapAgents`；角色型 Agent 还需persona catalog 正向绑定确认，缺失/失败不能把残留 runtime 当作有效绑定。刷新后选中对象按 ID 替换为新 roster/map 对象，不保留旧权限或状态字段。
- `visibleAgents` should derive from `mapAgents`, not from roster state.
- Bounty assignment should receive the target agent from the clicked row or explicit action payload.
- Chat context should preserve selected agent, mentioned agents, selected task, and `scene: 'juyiting'` metadata.
- Keep map controls and fixed-format UI elements dimensionally stable to avoid layout jumps.
- 横屏白屏排查先检查 `JuyiHallEntry` 的 entry/background 明确高度链；反复进入地图时，melonJS 缓存 `loader.load() === 0` 不触发回调，必须处理缓存资源状态并清理等待监听，不能只验证首次横屏。
- melonJS 15 的 `video` 无 `destroy()`：重复挂载还需核对全局 renderer/run loop、当前容器 resize 与输入坐标，不能只测 loader 缓存命中。
- 弹框尺寸由常驻 `useHallExperienceMode.js` 更新，`--hall-visual-height` 仅绑定在 `JuyiHall.vue` 根节点；不要恢复 `HallStage.vue` 的 document 全局高度写入，否则退地图后会残留横屏高度。
- 厅前议事需同时验证 visualViewport-only 键盘缩高与恢复（不改变物理方向）；高度 ≤320px 使用紧凑头部，不能只缩 overlay 而让固定内容遮住输入框。典籍正文、手札各自有界滚动。
- 微信 CSS 全景旋转不是宿主原生横屏；系统键盘方向需在小程序宿主工程处理，不能以 UA 仿真结果宣称真机已修复。
- 典籍从书架进入阅读可复用同实例、身份隔离的目录；必须先读取服务端进度再选取续读章节，不能并发打开卷首并让自动保存覆盖旧断点。
- 典籍进度写入 `PUT /archive/v1/me/progress/{editionId}` 携带 `Idempotency-Key`；跨域排查先验证生产 OPTIONS 的 Allow-Headers。reader 单测必须覆盖真实 `createApi → useHttp → fetch` 边界，不能仅 mock `api.put`。

- 百宝箱执行回执与历史恢复：GET `/agent/personal-workspace/executions` 为 owner/client/tenant 隔离的只读分页，GET `/executions/request` 用原 `Idempotency-Key` 核对；404 不证明在途 POST 未受理。未知意图不能因查看另一条终态记录而被清除，刷新不能自动重复生成。
- Runtime 的精确 `/internal/agent/tasks/{taskId}/runs/{runId}/failure` POST 必须同时具备 Controller 与 native filter 允许路径；客户端 inbox `completed` 不等于交付成功，须看 outcome/服务端终态/可验证产物。见 `specs/juyiting-execution-recovery/`。
- PRIVATE `WORKSPACE_FILE_EXECUTE` 的成功事实是 `OUTPUT_COMMITTED`、owner results manifest 与 owner-safe 文件版本/摘要验证；D03 不发送 legacy `work.result` / `work.result.receipt`，验收不得伪造或要求该回执。

## Backend Areas

| Concern | Backend path |
| --- | --- |
| Agent runtime/persona/task meta | `api/agent/` |
| Juyi Hall conversation type and messages | `api/chat/` |
| General task domain | `api/task/` |

Start backend searches with:

```bash
rg -n "map|roster|tasks/search|assign|AgentRuntime|AgentPersona" api/agent
rg -n "juyiting|conversation_type|chat/stream|conversation/events" api/chat
```

## Verification Checklist

For source changes under `web/`, select the relevant `web/tests/` and run the authoritative test/build on Alibaba Cloud Flow for the exact remote commit. Do not run a local Vite production build by default and do not use local success as release evidence. Develop changes are verified without deployment. Use `4403172 / cyf-web-release` for explicit versioned releases, binding version, commit and same-Run artifact; develop push/merge does not deploy. CI-only is optional for diagnosis, not a required prerequisite; see `AGENTS.md` for build and release policy.

Useful search:

```bash
rg -n "juyiting|JuyiHall|agent/map|agent/roster|agent/active|assign-task" web/tests web/src
```

For visual changes, start the dev server when useful:

```bash
cd web && npm run dev -- --host 0.0.0.0
```

## Documentation Hygiene

- Keep this runbook short and operational.
- Put detailed flow diagrams or long explanations in `docs/juyiting-feature-guide.md`.
- When fixing a repeated issue, add one sentence here under the relevant section so future sessions do not rediscover it.

## 交付与语音诊断

- TASK 正式 PDF 交付依赖显式启用 `agent.personal-workspace-storage`、`agent.task-artifact-storage` 与独立私有根目录；验收看正式交付列表/manifest及内容下载，不以本地 PDF 或上传 201 替代。
- 语音最新契约见 `specs/juyiting-voice-realtime/design.md`；录音实现路径以对应交付 commit 为准，不将历史候选路径当作当前 checkout 的入口。保留明确 Agent/会话、发送与回复关联，网关凭据不进入浏览器；能力证明、发布、生产启用和设备验收分开报告。
- 转写立即返回 `VOICE_UNAVAILABLE/503` 时检查 Redis 准入；已复现的 Redis4 Lua 限制及隔离回归方法见 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`，不操作生产 Redis 数据。STT/TTS 的原生事件、音频终态与 fidelity 要求按最新语音契约验证。
- 历史启用/测试/发布回执见 `docs/implementation/VOICE_REALTIME_ACTIVATION_20260930.md` 和 `docs/implementation/VOICE_SEMANTIC_FIX_20261001.md`；这些是历史证据，不代表当前线上 commit 或真实设备已验收。当前状态须核对精确 commit、实际 Flow Run 和在线证据。
