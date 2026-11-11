# Final integration topology — 2026-08-29

This file records the exact source-promotion and cumulative-release order. It does not authorize production deployment.

## Remote baselines

- API `origin/develop`: `828ef2e2f35ce249246a8da059fd5b9cfcedd1d5` / tree `f7e53c955734f9a166ac3480a34b0bec0b0bfa0f` (M3 accepted and promoted).
- Web `origin/develop`: promoted on 2026-08-29 from `7bc80de75f83d4cb7ca288380c3ed9eab1bc111a` to accepted cumulative RC `9d205884aaaa07b34aebe5aa6e4191d7dde2aa7e` / tree `9bd0051f85b0ec412088b8155fd9e6d2f04e0fe6`.
- Root SDD `origin/master`: `df766f03af60c504be339bb5fb101a41aa1b75d8`; final pin must use a fresh clean worktree.

## Product candidates

1. Web final source is the already-promoted `9d205884…`; it contains PWA preflight/onboarding and O00-O04. H04/H05W archive reader blobs are already byte-converged and must not be merged again.
2. PWA API cumulative R19 is `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a` / tree `bad28da5c05d6448d805f88c4e88457f0f657a5e`, with parents `828ef2e2…` and `f9baf0b2…`. It contains accepted HOSTED/ACL and M3 but remains unaccepted until its static verifier/review completes.
3. H06 archive API candidate is `66f30bc530f9dc2c96960998bc9e089d1220eed7` / tree `56cc82235e51409bea320c3f4cf931448267a366`. It contains H02/H03/H05A/H06 and must be accepted before integration, but must not be promoted directly.

## Required API cumulative merge

After both API R19 and H06 are accepted, create one new semantic merge commit with exact parents in this order:

1. first parent `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`;
2. second parent `66f30bc530f9dc2c96960998bc9e089d1220eed7`.

Known textual conflicts:

- `chat/jia-chat-service/build.gradle`
- `starter/src/main/resources/application-dev.properties`
- `starter/src/main/resources/application-grey.properties`
- `starter/src/main/resources/application-prod.properties`

Resolution invariants:

- preserve `/archive/**` OAuth resource ACL;
- keep `archive.reader.enabled=false` and `archive.question.enabled=false` by default;
- preserve all M3 task-event/Rabbit/read/redrive/reissue fail-closed flags;
- preserve PWA hosted/security configuration;
- preserve current approved version-catalog dependency form plus H06 test/runtime requirements.

Because these are semantic conflicts, the resulting tree requires fresh exact-tree verification and independent review. No byte-exact review exemption applies.

## Final promotion/pin order

1. Complete H06 isolated exact verification and review; do not promote.
2. Complete API R19 static verification and review.
3. Fast-forward API `origin/develop` from `828ef2e2…` to accepted R19 `2599de3c…` with an exact lease.
4. Build/review the cumulative API merge above, then fast-forward API `origin/develop` from `2599de3c…` to that accepted merge with an exact lease.
5. In a fresh root worktree based on `df766f03…`, pin Web to `9d205884…` and API to the final cumulative merge; independently review the root tree.
6. Build final Web/API/H06 artifacts and a new SHA-bound final manifest; do not reuse any draft manifest.
7. Run a fresh release guard. Production still requires one explicit authorization bound to the final manifest SHA and manifest-root SHA.

## Control-plane exclusions

`OPS-RESOURCE-TELEMETRY`, runtime evidence roots, systemd verifier units, H06 restore drills, and ASF-COOKIE-P1 approval metadata do not enter API JAR/Web bundles. They remain release/control-plane evidence.

## Provisional cumulative API preparation (2026-08-29 18:53 CST)

A conflict-resolved preparation candidate now exists, but remains non-promotable until both exact parents are independently ACCEPTED:

- Worktree: `/home/isp/wsps/cyf/.worktrees/final-api-cumulative-r1`
- Branch: `codex/final-api-cumulative-r1-20260829`
- Commit: `ca1c4ae53d1a90f8e729044f100c58d63d1a8e76`
- Tree: `7cd51c94611f3d75eefaf2a529105e1fe42a502d`
- First parent: `2599de3c2bdf5f1c3cf6e4faa8dcbb4048dffa4a`
- Second parent: `66f30bc530f9dc2c96960998bc9e089d1220eed7`

The actual divergent overlap was exactly the four predicted files. Lightweight checks passed: clean worktree, zero unmerged entries, `git diff --check`, no duplicate profile keys, all three archive ACL/default-off assertions, all three M3 fail-closed matrices, Gradle dependency assertions, and byte identity for every second-parent-only path. This is preparation evidence only; the semantic merge still requires fresh exact-tree Gradle verification and fresh independent Review after both parents are ACCEPTED.


## Provisional cumulative API bounded precheck (2026-08-29 23:07 CST)

Fresh read-only `sol_reviewer` `01a04e10-58f2-7461-9145-b97ad81e658c` reported `PRECHECK_PASS`, with no P0/P1/P2 findings, on exact provisional commit `ca1c4ae53d1a90f8e729044f100c58d63d1a8e76` / tree `7cd51c94611f3d75eefaf2a529105e1fe42a502d`. The four semantic conflict resolutions preserve archive OAuth ACL/default-off settings, all nine M3 fail-closed flags, PWA hosted/security settings, approved catalog dependencies, and H06 requirements; worktree is clean with no conflict markers or duplicate profile keys. This is not final ACCEPT: exact-tree Gradle verification and a fresh authoritative Review remain mandatory after both parents are accepted.
