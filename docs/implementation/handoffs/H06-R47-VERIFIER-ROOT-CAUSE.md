# H06 R47 verifier root-cause matrix

Exact candidate: `5643e7d1f05bc645b66eb9eb6e459890da39fb79` / tree `e4d6db9273db6c73ec7c13242fd61e7b59f9fe28`.

| Attempt | Symptom | Root cause | Bounded remediation |
|---|---|---|---|
| 1 | Candidate pin saw root HEAD `752b4dfc` | Relative runner was launched from the root checkout | Use explicit R47 worktree cwd and candidate runner absolute path |
| 2 | API pin expected `8298b027`, actual attached H05A API was `97d046c` | Cwd was corrected but command still invoked the root checkout runner; bootstrap copied stale constants | Invoke only `/home/isp/wsps/cyf/.worktrees/h06-scandir-remediation/ops/release/tests/run-isolated-archive-pavilion-h06.sh` |
| Post-stop observation | Correct R47 runner reached runtime inventory, then Python received `KeyboardInterrupt` | The verifier thread/lifecycle ended while the long synchronous runtime digest was still active | Fresh verifier must keep the command attached and must not return until the runner reaches its own terminal result |

No candidate source change is required. The next run must wait until the API Gradle owner and heavy-resource slot are free, use a new absent evidence root, preserve the 5 GiB gate, and remain offline/non-production. Any further failure stops for attribution.
