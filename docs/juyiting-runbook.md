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

For source changes under `web/`:

```bash
cd web && npm run build
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

## Archive Agent maintenance (development branch)

- Feature contract and delivery evidence: `specs/archive-agent-maintenance/`; implementation is isolated on the `codex/archive-agent-maintenance*` branches. Deployment, privileged activation and real-book publication are separate operations, not implied by a Git push.
- Admin HTTP lane: `/archive/admin/v1`; native execution lane: `/internal/archive/v1/jobs/{jobId}/runs/{runId}`. Admin scope comes from JWT, native scope from the authenticated WebSocket registration. Do not pass owner/client/runtime authority from Web forms or chat text.
- API execution stays default-off (`archive.maintenance.execution-enabled=false`); platform installation/catalog is independently gated by `agent.platform-skills.enabled`. Client installation/execution flags are `AGENT_PLATFORM_SKILL_INSTALL_ENABLED` and `AGENT_ARCHIVE_MAINTENANCE_ENABLED`, both default-off. Catalog unavailability must not disable existing manager revoke/cancel controls.
- Maintenance UI: `web/src/components/juyiting/archive/ArchiveMaintenancePanel.vue`; authorization-rechecked conversation card: `ArchiveMaintenanceReceiptCard.vue`; gateway: `web/src/composables/juyiting/useArchiveMaintenance.js`.
- Chat entry carries only `archiveMaintenanceIntent: { schemaVersion: 1, confirmationRef }`. Songjiang uses canonical `builtin-songjiang`; private entry uses the exact persisted appointed Agent and must not fall back to Songjiang.
- Byte-addressed package resources and existing archive content use API `.gitattributes` `-text`; never normalize approved package bytes to make an installation check pass. Package v1.0.0 is 40,563 bytes, SHA-256 `8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081`.
- Run the existing real selectors (not similarly named nonexistent files): `archive-reader.test.js`, `archive-maintenance.test.js`, `juyiting-component-behavior.test.js`, `juyiting-hall-chat-context.test.js`, `juyiting-hall-conversation.test.js`, `juyiting-conversation-material-links.test.js`. The new panel/card tests compile and mount their actual SFCs; their explicit authStore seam still uses the production gateway, createApi and useHttp.
- Backend focused tasks: `:agent:jia-agent-service:archivePlatformContracts`, `:agent:jia-agent-service:archiveMaintenanceSecurity`, `:chat:jia-chat-service:archiveMaintenanceMvp`, `:chat:jia-chat-service:archiveRegression`. Hold the shared Gradle lock for the entire command; actual isolated-MySQL opt-in tests use `ArchiveMySqlTestGuard`, never a production DB.
- Do not relabel preserved baseline failures, skipped/absent selectors, source-string assertions, mock transport, or a package/install receipt as full regression success or actual publication. See the latest source-bound evidence and remaining boundaries in the feature acceptance file.

- Maintenance development/recovery guide: `docs/archive-agent-maintenance-runbook.md`; exact pending source and validation boundaries remain in the feature integration record.
