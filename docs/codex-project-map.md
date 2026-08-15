# Codex Project Map

This file is a compact orientation map for future Codex sessions. It should stay short and stable; detailed feature notes belong in focused runbooks.

## Top-Level Layout

| Path | Purpose |
| --- | --- |
| `web/` | Vue frontend app, Vite build, UI components, frontend assets, frontend tests |
| `api/` | Java backend workspace with Gradle modules for common, agent, chat, task, and ISP domains |
| `docs/` | Project guides, implementation plans, operational notes |
| `deliverables/` | Packaged deployment artifacts and generated packages |

## Git Layout

- The workspace root is the `jia-sdd` coordinating Git repository.
- `api/` and `web/` are independent Git repositories registered as submodules and pinned by the root commit.
- Use `git status` for the coordinated delivery baseline, and `git -C api ...` or `git -C web ...` for implementation history.

## Frontend Layout

| Path | Purpose |
| --- | --- |
| `web/src/main.js` | Frontend bootstrap |
| `web/src/router/index.js` | Route registration |
| `web/src/components/` | Vue components grouped by feature |
| `web/src/components/world/JuyiHall.vue` | Current Juyi Hall page composition |
| `web/src/components/juyiting/` | Juyi Hall panels, map stage, tokens, command/chat surfaces |
| `web/src/composables/` | Shared and feature-specific frontend logic |
| `web/src/composables/juyiting/` | Juyi Hall data, conversation, physics, sound, and portrait logic |
| `web/src/constants/juyiting.js` | Juyi Hall filters, role metadata, map anchors, obstacles, walk bounds |
| `web/src/stores/` | Pinia stores and demo data |
| `web/src/assets/` | Frontend static assets imported by source code |
| `web/tests/` | Frontend contract and smoke tests when available |

## Backend Layout

| Path | Purpose |
| --- | --- |
| `api/agent/` | Agent runtime, persona, task metadata, roster/map/task APIs |
| `api/chat/` | Chat conversations, messages, Juyi Hall conversation type support |
| `api/task/` | General task planning and execution modules |
| `api/common/` | Shared backend infrastructure, utilities, base entities, test support |
| `api/isp/` | ISP/domain/CMS related modules |

Backend modules are split into `*-core`, `*-api`, `*-mapper`, `*-service`, and `*-starter` style Gradle projects. Inspect the nearest `build.gradle` before choosing a build or test command.

## Common Frontend Commands

Run from `web/`:

```bash
npm run build
npm run dev -- --host 0.0.0.0
npm run test
```

## Common Search Targets

- Juyi Hall UI: `rg -n "JuyiHall|聚义厅|juyiting" web/src`
- Agent APIs: `rg -n "/agent|Agent" api/agent web/src`
- Chat stream/events: `rg -n "chat/stream|conversation/events|juyiting" api/chat web/src`
- Task assignment: `rg -n "assign|悬赏|tasks/search|tasks/.*/assign" api/agent web/src`

## Documentation Entry Points

- `docs/juyiting-runbook.md`: compact guide for ongoing Juyi Hall changes.
- `docs/juyiting-occlusion-system-design.md`: extensible full-map occlusion, world sorting, TMX schema, migration, validation, and Agent execution plan.
- `docs/juyiting-occlusion-system-execution-plan.md`: serial implementation backlog, DeepSeek/GPT allocation, handoff gates, verification, and release sequence for occlusion v2.
- `docs/juyiting-feature-guide.md`: deeper Juyi Hall behavior and data-flow documentation.
- `docs/juyiting-collaboration-implementation-plan.md`: historical implementation plan for collaboration flow work.
- `docs/juyiting-multi-agent-collaboration-design.md`: target architecture, detailed design, backlog, migration, and phased rollout plan for reliable multi-Agent bounty collaboration.
- `docs/implementation/README.md`: execution control center for multi-model implementation, including the task ledger, coverage matrix, decisions, and handoff rules.
- `docs/codex-ws-agent.md`: Codex websocket agent operational notes.
- `docs/project-feature-implementation-checklist.md`: cross-project feature completeness and optimization checklist.
- `docs/project-markdown-coverage-matrix.md`: one-to-one coverage record for every audited source Markdown file.
- `docs/project-api-endpoint-audit.md`: endpoint-level mapping from interface documentation to Controllers.
- `docs/project-plan-task-audit.md`: Task/Phase-level implementation audit for project plans.

## Maintenance Rule

When a future task uncovers stable project knowledge that would save repeated exploration, update this file or the relevant runbook in the same change.
