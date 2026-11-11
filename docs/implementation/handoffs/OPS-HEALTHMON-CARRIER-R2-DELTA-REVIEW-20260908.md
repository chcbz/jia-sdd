# Independent carrier R2 delta review — 2026-09-08 CST

Reviewer: non-author main `01a02e65-990c-7e81-b574-96a41cfe8222`.
Candidate: `98adbe030a142cf69b8ac81b3ece426467691e7e`, tree `2c926a780a350c4da0e94769f20ac4e45eba28a9`; clean worktree verified.

**REJECT 0/1/0, bounded P1 recovery-budget refund race.** Reuse actual 72/72 offline PASS and benign host scope survival/swappiness proof; these remain valid, not production recovery evidence.

- Helper `run()` invokes canonical through Popen before emitting/flushing NATIVE_INVOKED. Termination/output error between these operations can leave a real recovery without its marker.
- Parent `_run_recovery_carrier()` interprets all missing markers as definitely not invoked. `recover()` also converts OSError/SubprocessError from anywhere in the carrier run into native_invoked=false. The caller then refunds the durably reserved attempt. Consequently an uncertain post-dispatch failure can erase an actual attempt and violate the user's three-attempt stop rule.
- Correct only this boundary: establish an invocation/dispatch fence before canonical launch after preconditions; missing output after dispatched carrier or transport failure is UNKNOWN and retains reservation. Only an explicitly proven pre-invocation failure may refund. Do not falsely label unknown as definitely invoked or definitely not invoked. Preserve truth in durable result and alert text.
- Add bounded offline fault cases: post-dispatch missing marker, stream/wait error, definitive preflight failure, third-attempt unknown latching/no fourth call. Update installer digest pins and clean commit. No new full-project/host probe or canonical execution.

Original Knuth remains implementation and sole production runtime owner. One bounded correction and focused verification is authorized; no install/API lifecycle until this delta is accepted and the API A3 heavy window ends. Incident I000056 has externally proven used1/3,remaining2; reconcile durable state before monitor activation, do not reset it. Prefer final new-JAR deployment/start rather than another old-JAR coldstart immediately before replacement.
