# H06 R46 verifier root-cause matrix

Approved by the main controller on 2026-08-29 for one bounded unchanged-tree retry.

Exact candidate: `5ce3cbfb4120a47eb7a45bc765481eab9ce7fb25` / tree `1d45c20239cd885b5920280fe24b310eeab355d3`.

| Attempt | Symptom | Root cause | Evidence | Remediation |
|---|---|---|---|---|
| 1 | Existing evidence root rejected as not root:root 0711 | Verifier pre-created the root with `mktemp -d` mode 0700; candidate correctly failed closed | attempted root absent after cleanup; no heavy resources started | Pass a unique path that does not exist and let `h06_secure_create_run` allocate it |
| 2 | `WEB ref mismatch ... actual=DETACHED` | The accepted H05W worktree was exact and clean but detached instead of attached to frozen `codex/h05w-archive-question-web` | manifest `b3c5187d...`; no Gradle/MySQL/browser/build started | Main controller reattached the unchanged exact worktree to the preserved branch ref and reverified HEAD/tree/clean status |

The remediation changes no candidate bytes and authorizes only one fresh non-overwriting verifier run. Any recurrence stops without another retry.

## 2026-08-29 control-plane addendum

The next verifier selected the wrong interpreter and invoked the Bash runner with `python3`. It failed at line 2 with `SyntaxError` before candidate bootstrap, evidence-root allocation, Gradle, MySQL, Chromium, build, or runtime execution. The Agent and controller then each recorded the same incident, which raised the ledger counter twice; these are duplicate control-plane records of one command-wrapper incident, not two independent candidate failures.

| Incident | Symptom | Root cause | Safety impact | Final remediation |
|---|---|---|---|---|
| 3 (duplicated in ledger notifications) | Bash `set -Eeuo pipefail` parsed by Python | Verifier command wrapper selected `python3` instead of `/bin/bash --noprofile --norc` | No candidate gate or heavy resource started; no evidence root or source changed | Authorize one final fresh verifier with an explicit canonical Bash argv and a previously absent evidence-root path. Any further invocation or candidate failure stops. |

This addendum authorizes exactly one final unchanged-tree run because the prior command never entered the H06 runner. It does not authorize changing candidate bytes, weakening the 5 GiB gate, overwriting evidence, or repeating after another failure.
