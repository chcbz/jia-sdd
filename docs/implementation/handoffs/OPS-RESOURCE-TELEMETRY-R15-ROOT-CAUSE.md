# OPS-RESOURCE-TELEMETRY R15 root-cause matrix

Date: 2026-08-29 CST

Base exact candidate: `13d270b8206264ea4d056d01b5eeef6b0e8c3c76` / tree `634fb7b324fd215978368fce529f728b4682679f`.
Working diff SHA-256 at stop: `806ec8c1893382f4e1c6ef5a3914f1ca810e0078e846096852de3e8020bc5e27`.
Evidence: `/var/tmp/cyf-ops-resource-telemetry-r15-20260829T130727Z-KDfW6D`.

The three new real-path regressions pass. The selected 14-test group was stopped after two consecutive documentation-contract synchronization failures; no full suite, final static gate, commit, host provisioning, Gradle, DB, Rabbit, or production operation occurred.

| Attempt | Symptom | Root cause | Authorized remediation | Required verification |
|---|---|---|---|---|
| Selected 1 | 13/14 PASS; docs contract retained stale broad ordinary-fd wording | Literal-by-literal test synchronization missed an adjacent R14 wording after R15 made the fstat/linkat race precise | Preserve production code/docs; update only the stale assertion to exact R15 wording | Same selected 14 once |
| Selected 2 | 13/14 PASS; docs contract still expected combined `setns(mnt/user)` | The assertion block was not comprehensively audited after the real host probe established separate Linux outcomes: mount setns permission denial, current-user-namespace setns `EINVAL` or permission denial | One bounded test-only change: assert separate `setns(mnt)`, `setns(user)`, and `EINVAL` literals; audit adjacent R15 literals once | Selected 14 once; if PASS, full module once, `py_compile`, `git diff --check`; then commit and fresh host gate/Review |

A third blind selected retry is forbidden without this recorded remediation authorization.

## R15-R1 verification-command stop (2026-08-29 21:35 CST)

- Selected frozen suite passed `14/14` once; full module passed `57/57` once.
- The next static wrapper failed before `py_compile.compile` because it called `ast.parse(..., feature_version=(3, 6))` on the host's actual Python `3.6.8`, whose `ast.parse` has no `feature_version` parameter.
- This is a verifier-command compatibility defect, not source syntax or behavior failure. Passing selected/full evidence remains exact for the unchanged working diff SHA-256 `74a857f8af0294b0663f6c8fc4d5cd554e724105e450c4d8209edd8c8884378c`.
- Bounded continuation: do not repeat selected/full. Run Python 3.6 `py_compile.compile` directly with all `.pyc` outputs under a fresh external evidence root; if PASS, run `git diff --check`, remove only generated pycache, verify exact three-file scope and hashes, commit, then fresh host gate and Review.
