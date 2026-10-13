# AAM-MERGE-DEVELOP-20261013 Writer handoff

## Final Client freeze

- Repository: `C:\Users\Think\.codex\worktrees\archive-agent-maintenance\isp-install`
- `HEAD`: `38edf9c9a299d0ee3cec92421867cfaaf39c491d`
- `MERGE_HEAD`: `6325af1d858bf6e35b3e7046bf967f2c85ba7d5b`
- Exact staged tree: `a36a452dc5666f3661d304cc3c3c229cac3efd5c`
- Staged files: 10
- Unmerged files: 0
- Unstaged files: 0
- Commit/push/deploy: not performed
- Task-scoped Node/npm processes after verification: 0. The three interrupted a39 test runs are excluded and are not reported as results.

## Staged files

1. `conf/codex-ws-agent/package-lock.json`
2. `conf/codex-ws-agent/package.json`
3. `conf/codex-ws-agent/schemas/skill-manifest-v1.schema.json`
4. `conf/codex-ws-agent/skill-install-manager.mjs`
5. `conf/codex-ws-agent/skill-manifest.mjs`
6. `conf/codex-ws-agent/test/fixtures/skill-manifest-contract-v1.json`
7. `conf/codex-ws-agent/test/skill-install-manager.test.mjs`
8. `conf/codex-ws-agent/test/skill-manifest.test.mjs`
9. `conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs`
10. `conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs`

## Conflict choices and required merge wiring

- `conf/codex-ws-agent/skill-install-manager.mjs:749,1786-1818`: retained the hardened `extractSkillArchive` implementation and archive-safe extraction checks; also retained the incoming manifest/schema result, manifest SHA binding, marker validation, durable result, and replay checks. The incoming schema work therefore does not replace or weaken archive traversal/symlink/device/limit defenses.
- `conf/codex-ws-agent/skill-manifest.mjs:1-16`: retained Ajv 2020 schema compilation through `ajv/dist/2020.js` and the new JSON schema.
- `conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:203-250`: the unified payload includes archive-maintenance modules, platform-skill modules, the production `module-import-scanner.mjs`, `skill-manifest.mjs`, and `schemas/skill-manifest-v1.schema.json`. Duplicate manifest/schema entries that caused `EEXIST` were removed.
- `conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:5,281-321`: payload closure scanning uses the production scanner rather than the deleted installer's old regex, avoiding false imports from runner string literals such as `from './parse-text.mjs'`; Ajv subpaths resolve through the root `ajv` dependency.
- `conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:90-99` and `conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs:759-780`: `PLATFORM_SKILL_INSTALL` business `installationId` stays nested in `payload`; it is not confused with Runtime installation proof. A forged top-level installation ID remains rejected.
- `conf/cyf-agent-runtime-v1/lib/runtime-client.mjs:121-136,230+`: the native transport keeps an exact archive route matcher and session-derived Runtime authorization. No arbitrary `/internal` route or API-key fallback was introduced.

## Feature-gate classification

- **Default closed:** `conf/cyf-agent-runtime-v1/README.md:81-92` states both `platformSkillInstallEnabled` and `archiveMaintenanceEnabled` default to `false`.
- **Source has an explicit unified Runtime entry:** `conf/codex-ws-agent/agent-client.mjs:4880-4887` validates controlled Runtime identity/owner configuration; `conf/codex-ws-agent/agent-client.mjs:6132-6143` wires the two profile flags into the single `PlatformSkillRuntime` entry.
- **Not equivalent to real enablement:** actual host profile values, nginx/gateway route allowlists, Linux atomic behavior, and live Runtime registration/session proof were not configured or accepted in this round. This is an environment/acceptance gap, not evidence that the Runtime source lacks an entry.

## Narrow verification

Passed:

- `npm ci --ignore-scripts --no-audit --no-fund` (8 packages added)
- Ajv 2020 subpath import: PASS
- module-import-scanner tests: 7/7 PASS
- skill-manifest non-symlink selectors: 56/56 PASS
- unified execution-payload catalog: 1/1 PASS
- platform native/runtime selectors: 22 PASS, 1 Linux-only SKIP
- relevant `node --check`: PASS
- `git diff --check`: PASS
- `git diff --cached --check`: PASS

Windows-only environment blocks, not product PASS/FAIL claims:

- Skill-manifest symlink selector: Windows `EPERM` creating a symlink (56 pass, 1 blocked).
- Skill installer archive/SE2 selectors: 23 selectors reached Windows directory `fsync` `EPERM` before business logic.
- Runtime proof/native-route Linux selectors: Windows has no `process.getuid`.

## Protected bytes

`conf/codex-ws-agent/test/fixtures/archive-maintainer-1.0.0-approved.zip` remains 40,563 bytes with SHA-256 `8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081`.

## Remaining gaps (do not expand this merge into full product completion)

1. Main should run the Linux-only unified Runtime/session/native-route/archive-install selectors. No application deployment was performed.
2. Real nginx/gateway allowlists for archive/platform routes are not deployed or accepted. Keep route matching exact; do not open arbitrary `/internal`.
3. Real Runtime installation, session proof, HTTP ACK/dispatch, Agent appointment, archive content maintenance/publish, and the 84 business acceptance cases remain open.
4. API has parse evidence only in this round, not formal typecheck/compile; old API-key/session test migration remains open. Historical five MySQL failures must not be called fixed.
5. Web 19 selectors were reported 531/531 PASS by Main, but the default Windows test command has a path issue and the incoming test scope excludes historical occlusion files; historical 39 failures must not be called fixed.

## Latest-source note

This freeze is the second Client merge from `6325af1d858bf6e35b3e7046bf967f2c85ba7d5b`, on top of Main's first a39 merge commit `38edf9c9a299d0ee3cec92421867cfaaf39c491d`. It includes the new skill-manifest module/schema, Ajv dependency/lock changes, execution payload closure additions, and runtime-host regressions.
