# Owned backend verification OOM — 2026-10-16

| Input | Evidence | Result |
|---|---|---|
| 07cb1c164a, default JVM, default workers | api-verification-1.log, api-oom-evidence.log | Kernel killed owned daemon1157396, anon RSS931356KiB; no test conclusion |
| same source, daemon heap512m, worker1 | api-verification-2.log, api-oom-second.log | Kernel killed owned daemon1158877, anon RSS817004KiB at test startup; no test conclusion |

Host physical RAM 3724MiB. Observation before second kill: available288MiB, daemon RSS800396KiB, test RSS204108KiB, existing application RSS784276KiB, shared memory871MiB. Other services/processes untouched. Both owned JVMs have exited (PID checks). This is kernel global OOM, not a failed business assertion.

Runtime is Oracle GraalVM21.0.8; second kernel report names JVMCI-native compiler as OOM invoker. Heap-only cap does not bound native/compiler/metaspace overhead. Native JIT's causal share is not measured; disabling it is a scoped diagnostic remediation, not a claim of measured savings.

New input: clean API2fa70d8d6b, added conversation grant assertion + seven claim-scope tests; same production source. Owned JVMs use C2 (`-XX:-UseJVMCICompiler`), ActiveProcessorCount2, Gradle heap384m, worker1. Test JVM heap384m with fresh tests; unchanged compilation outputs may be reused by Gradle exact inputs. No performance/request gate, no test removal, no change to production JVM, no shared process termination. Use existing orchestrator authorize-remediation; evaluate new output before further action.

## Distinct fixture blockers after OOM remediation

- verification3: v1131Acceptance passed; compileExecutionHistoryHttpJava lacks oauth-resource. Restored only the test source-set's exact production resource-chain dependencies; no product dependency change.
- verification4: v1131Acceptance passed; empty DB bootstrap raises unknown execution_protocol_version inside base initializer. This exists at ab379ba8 baseline (verifyTaskExecution references the column unconditionally before v3 provisioning). Production cold-bootstrap repair is explicitly outside this patch; no application initializer was changed.
- Candidate4a22e3c904 provisions the test DB from ten exact production SQL resources, then current ControlledImageFollowupV3SchemaInitializer, then base initializer verification. It tests provisioned current-catalog behavior, not cold-bootstrap installation. No handmade nullable column, skipped SQL assertion, modified FK/check or stub SQL result.
- verification5 was rejected by the orchestrator gate before Gradle; it is not a test run. Request authorization for changed test input and then run verification6. The two fixture failures have distinct roots, though both were categorized test_fixture. All logs retained.

- verification6: duplicate ALTERs already folded into current base DDL; removed from fixture only.
- verification7: 107 unit tests and real MySQL assertions pass; real browser rejects duplicate X-Request-Id with fixture spring-web7.0.2. Next action is read-only starter runtimeClasspath resolution, not global-header editing or same-input retry.
