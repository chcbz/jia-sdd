# CYF multi-model agents

Project-scoped Codex agent roles are defined in `.codex/agents/*.toml` and registered by `.codex/config.toml`.
Model routing and the serial execution policy are recorded in `docs/implementation/MODEL_ROUTING.yaml`.
The active M2 plan is `docs/implementation/M2_EXECUTION_PLAN.md`.

Current policy:

- one active task and one active writer at a time;
- one writer per task/worktree;
- writer and reviewer are separate agents;
- use a different reviewer model for M2 implementation;
- reviewers are read-only and never repair reviewed code;
- Gradle is serialized with `/tmp/cyf-gradle.lock`;
- no production DML/deployment without an explicit deployment task and confirmation.

M2 defaults:

- DeepSeek V4 Pro High: C01/C01B/C01H and C02-C07A core implementation;
- DeepSeek V4 Flash Medium: read-only test/probe runner for core tasks, and Writer only for C07B/C presentation UI;
- GPT-5.6 Sol High: architecture freeze, Pro implementation review, integration and release gates;
- DeepSeek V4 Pro High reviewer: Flash-written UI/test review;
- GPT Image 2: optional C07 visual assets only, never a critical-path dependency.

General defaults remain available:

- Sol High: architecture, P0 implementation, and final release gates;
- Terra Medium: normal implementation and repository exploration;
- Luna Medium: bounded mechanical work;
- GPT-5.4 Mini Medium: narrow fast queries.
