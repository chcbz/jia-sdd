# Juyi Hall Runbook

This is the short working guide for future 聚义厅/Juyi Hall iterations. Use `docs/juyiting-feature-guide.md` for deeper flow details.
For map masking, prop depth, occluder assets, and future map expansion, use `docs/juyiting-occlusion-system-design.md`.
For the serial implementation order and DeepSeek/GPT Agent allocation, use `docs/juyiting-occlusion-system-execution-plan.md`.
For the current GPT multimodal visual baseline verdict and required contact sheets, use `docs/juyiting-occlusion-visual-review-v0.md`.

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
| Guided onboarding | `web/src/components/juyiting/HallOnboarding.vue`, `web/src/composables/juyiting/useHallOnboarding.js` |
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
- `visibleAgents` should derive from `mapAgents`, not from roster state.
- Bounty assignment should receive the target agent from the clicked row or explicit action payload.
- Chat context should preserve selected agent, mentioned agents, selected task, and `scene: 'juyiting'` metadata.
- Keep map controls and fixed-format UI elements dimensionally stable to avoid layout jumps.
- Onboarding follows the actual `portrait-command` / `landscape-map` experience (including virtual landscape), with separate steps. Keep portrait `data-tour` anchors aligned with their buttons; map steps must use runtime hotspot bounds and canonical map IDs, not fixed screen coordinates. Preserve replay, versioned dismissal, and modal focus restoration.
- Onboarding geometry is isolated in `web/src/components/juyiting/hallOnboardingGeometry.js`; verify it with `web/tests/hall-onboarding.test.mjs` (Node test runner) and `web/tests/juyiting-hall-onboarding-geometry.test.js` (Mocha component tests).

## Mini Program Public Entry

- Cold launch loads `https://kit.chaoyoufan.cn/?nativeOrientation=portrait&entry=direct`; `/` explains the product to guests (valid logged-in sessions follow the existing redirect to `/juyiting`), `/demo` is a local simulation, and `/juyiting` is the authenticated workbench.
- Public links use `web/src/utils/publicEntryNavigation.js` to preserve only portrait context and allowlisted entry markers, never source URL credentials or arbitrary redirects.
- Keep fixed native landscape navigation unchanged. The portrait fallback `entry=fallback` must load `/juyiting`, not the introduction.
- The paired shell is at `C:/Users/Think/WeChatProjects/juyiting`; run paired tests with `MINIPROGRAM_PROJECT` set to that checkout. Release and physical-device acceptance remain separate gates; see `specs/miniprogram-public-entry/acceptance.md`.

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

Formal frontend builds run in the Alibaba Cloud pipeline after pushing the reviewed code to the remote `develop` and `master` branches. Do not treat a local build as a production release or run local production builds by default. Local verification uses targeted tests; update the root `web` gitlink only after the frontend commit is pushed.

For onboarding changes, run the local behavior checks from `web/`:

```bash
node --test tests/hall-onboarding.test.mjs
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter dot --exit tests/juyiting-hall-onboarding-geometry.test.js
```

For behavior changes, also inspect relevant tests under `web/tests/`. Useful search:

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
