# Web release build — bounded OOM remediation (2026-09-08)

Main consumed original Web Sol's read-only native terminal after two failures. This is a new attributed remediation, not an unchanged third build.

| Attempt | Observed failure | Supported cause | Remaining uncertainty |
| --- | --- | --- | --- |
| R1 | rc137, kernel global OOM, Node heap512MiB | Host-wide memory exhaustion; not ENOSPC | Exact internal peak phase unproven |
| R2 | rc134, V8 heap exhaustion, Node heap384MiB, workers1 | Heap cap exhausted after1187 transforms, before reporter rendering message/index.html | Rollup chunk graph vs pre-reporter render/minifier allocation not distinguished; Terser is not a proven sole cause |

Retain both failure directories and their matrices. R2 matrix SHA `459fa47ee2c8692cf080351036d1569b914a2e546dd2e581663d2b9c9ad51f6d`.

## Authorized bounded source remediation
Original Sol owns only `vite.config.js` (or the existing equivalent config filename) and a narrowly scoped offline build-config regression in his clean release worktree. Base `dcfbc93814e1d5287ab779cb1b5ab1a2d06999c9` / tree `436883f4066c0bff94469112294aefd4d12f2770`.
- Use already-locked esbuild instead of Terser; production must still remove console calls including argument side effects and debugger statements. Nonproduction must retain prior console behavior and drop debugger.
- Commit the configuration change for reproducibility; no untracked-only substitute for the shipped config. Preserve plugins, route/resources, manualChunks, source maps/feature defaults and no dependency install/lock change.
- Keep worker concurrency bounded and compressed-size reporting disabled. Verify configuration and a tiny real transformation regression if a separately approved dependency loan is available; no full suite or heavy build during API window.
- Submit new clean exact commit/tree for independent Godel delta review, then normal develop push.

## Build authorization boundary
One new build may run only after exact config-delta ACCEPT, explicit fresh read-only donor loan, and actual release of API heavy window. Node heap512MiB is the new trial, not a guaranteed fit; do not raise it blindly or kill processes. Preserve source, production and failure evidence on failure. If successful, original Sol may publish with existing exact-artifact procedure and verify public identity without another per-stage main acknowledgement. Main will provide window handoff. Build/runtime failures retain truthful attribution; no failed partial dist deployment.
