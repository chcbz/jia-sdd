# CYF Workspace Guidance

This repository is a multi-module workspace with a Vue frontend under `web/`, Java/Gradle backend modules under `api/`, and project notes under `docs/`.

## Read First

- For a compact project map, read `docs/codex-project-map.md`.
- For Juyi Hall work, read `docs/juyiting-runbook.md` first, then use `docs/juyiting-feature-guide.md` for deeper flow details.
- Prefer targeted `rg` searches over broad file reads.

## Fast Iteration Principle

- 快速迭代阶段不以稳定为首要目标；一切优先往前推进。有问题就继续修问题，修不了就优化技术栈，不做保守回退作为默认选择。

## Key Commands

- Frontend build: `cd web && npm run build`
- Frontend dev server: `cd web && npm run dev -- --host 0.0.0.0`
- Frontend tests: `cd web && npm run test`
- Backend build/test commands vary by module; inspect `api/build.gradle` and module `build.gradle` files before running broad Gradle tasks.

## Frontend Notes

- Main frontend source is `web/src/`.
- Juyi Hall route/page composition is in `web/src/components/world/JuyiHall.vue`.
- Juyi Hall components live in `web/src/components/juyiting/`.
- Juyi Hall composables live in `web/src/composables/juyiting/`.
- Juyi Hall constants live in `web/src/constants/juyiting.js`.
- Juyi Hall visual assets live in `web/src/assets/juyiting/`.

## Juyi Hall Invariants

- Map agents and roster agents are intentionally separate data flows.
- Map agents come from `/agent/map`; roster agents come from `/agent/roster`.
- Do not reintroduce `/agent/active` for Juyi Hall.
- Task assignment must pass the explicit target agent, not rely on hidden selected state.
- Role portraits are resolved in `useWaterMarginRoles.js`; role metadata is in `constants/juyiting.js`.

## Verification

- For frontend changes, run `cd web && npm run build` unless the change is documentation-only.
- For Juyi Hall behavior changes, also inspect or run the relevant tests under `web/tests/` when present.
- Keep documentation updates short and path-accurate; prefer updating these guide files over rediscovering the same structure in future tasks.

## Editing Discipline

- Do not revert unrelated user changes.
- Keep changes scoped to the requested module.
- Avoid broad refactors unless the request explicitly asks for them.
- If generated image assets are added for frontend use, store final project assets under `web/src/assets/` and verify the production build can import them.

## Multi-Model Agent Routing

- Project Agent profiles are registered in `.codex/config.toml` and defined under `.codex/agents/`.
- Use `docs/implementation/MODEL_ROUTING.yaml` as the durable model-routing policy.
- Current execution is serial: one active task at a time, followed by an independent review and user confirmation.
- Prefer `critical_worker` for P0 identity/ACL/transaction/migration work, `balanced_worker` (Terra Medium) for normal implementation, `explorer` (Terra Medium) for repository analysis, `fast_query` (GPT-5.4 Mini Medium) for narrow lookups, `routine_worker` for bounded mechanical work, and `adversarial_reviewer` for cross-model review.
- Reviewers are read-only and must not repair the code they review.
- Every Gradle command must hold `/tmp/cyf-gradle.lock`; never run parallel Gradle builds on this host.
