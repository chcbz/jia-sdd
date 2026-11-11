# JVC-OAI release compatibility preparation — 2026-09-05

Read-only repository preparation; **not deployment approval**. Current execution ownership/gates remain solely in `TASKS.yaml#runtime_ledger_json`.

## Reusable accepted inputs

- API `92c5ec3ffb89fa58e5d44c94a2d63c794b19016c`, tree `fa067814f1236f85de687e0b6b7e3f1976875214`: Spring AI voice 81/81 and chat 9/9, independent 0/0/0; see `JVC-OAI-SPRING-R6-ACCEPT.md`. Do not rerun unchanged-tree suites.
- Web `ce45b898cd19f2b823a08242a030b255757b0953`, tree `25cdcab21e71b6acf4db70e56b70b2c769b276d0`: accepted 23/23 and build. These are feature candidates, not proof of deployed content.
- OPS R15 diagnostic candidate `2fb39b5c476b00c73b73871c8a6f59610609389f`, tree `570d916855dc698f64fad0f46bc5275a045e0a0e`, parent `a543e644c2fc738de34332c339d4c2c8d557dbea`; three-file scope and clean worktree confirmed. Binary diff SHA256 `e41b8d9100fc82615a2a34962b19c755805910b0483edd2aa2eef02cabed1cf5`. Not runtime acceptance.

## Release integration requirements found in current source

| Area | Concrete mismatch | Required closure before production |
| --- | --- | --- |
| Service identity/path | Voice packet `lib/common.sh` pins `cyfapi`, `/opt/cyf/api`, and `current.jar`; current `docs/DEPLOYMENT.md` requires `cyf-api`, `/opt/cyf/service/api`, canonical root lifecycle command `/usr/local/sbin/cyf-api-kit` | Freeze one host contract, adapt in separately owned paths, independent review and isolated verification. Do not create a parallel service/account or overwrite installed lifecycle scripts. |
| Process control | Voice packet explicitly stops at on-disk selection and never restarts a JVM; legacy `ops/release/deploy-api.sh` identifies/signals and starts Java directly | Integrate only through accepted canonical lifecycle and shared locking/attestation contract. Passing selector tests is insufficient evidence of deployment or health. |
| Build admission | `ops/release/build-api.sh` invokes Gradle with `flock` directly | Route every future Gradle invocation through `cyf_orchestrator.py gradle`, preserve exact clean input and immutable JAR digest, and avoid nested lock acquisition. No existing script execution authorized by this note. |
| API source lineage | Local `api/develop` is `dc039b34d9d24a46714724d5937f2c098f6c6d87`; merge-base with accepted voice is `828ef2e2f35ce249246a8da059fd5b9cfcedd1d5` | Integrate in a clean separate worktree while retaining the login-origin fix. Never reset local develop or force-push over it. |
| Profile merge | Login fix touches prod/grey application properties and two security tests | Review integrated profile values with voice configuration; run only changed-tree relevant security/voice contracts, not stale-tree duplicate suites. |
| Workspace state | Primary API/Web/root contain unrelated work | No broad staging, checkout/reset, dirty source build, or shortcut deployment. Root integration gitlinks need reproducible pushed source commits. |
| Provider activation | Packet is intentionally flags-off and contains no provider secret | After host and release gates, assess existing Spring AI configuration without printing secrets; actual transcription/synthesis smoke is separate from text-model compatibility. Never infer audio support from text success. |

## Dependency order (not an additional ledger)

1. Independent R15 cleanup/containment review; only 0/0/0 permits one staged lifecycle focus.
2. Separate failed-terminal reachability validation, then complete OPS evidence/inventory gate under exact candidate and controller manifest.
3. Freeze/adapt new host deployment contract and API/Web integration candidates; preserve accepted unrelated fixes.
4. Independent release review and immutable-artifact verification, then authorized deployment using canonical lifecycle.
5. Verify application/public health, authenticated voice input, auto-send behavior, speech output and landscape interruption behavior before claiming voice live.

No production credentials, installed files, services, Nginx, database, or other task evidence were accessed or modified for this preparation.
