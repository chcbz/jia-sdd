# Output-to-asset archive verification remediation

2026-09-30. Exact API candidate 194ec91a596c28f9575a64aef47a5bf7b9fb6778/tree 10d312e61057b1a83da1485238c2f3acf63e5361.

1. Initial configuration: missing repoUsername/repoPassword before any test. Changed invocation supplies inert unused properties, stays offline and does not publish. Evidence: gradle-194ec91a.log.
2. Subsequent invocation: kernel global OOM killed exact owned daemon PID 1785125, anon-rss 690020KiB and file-rss 10640KiB; no Java test terminal. Evidence: exact-daemon-oom.log and gradle-194ec91a-attempt2.log. This is not the preceding configuration root cause.
3. New bounded remediation: restrict this invocation's JVM ActiveProcessorCount to 2 and UseSerialGC, including its test child, to reduce parallel JVM native/collector/compiler overhead; preserve the 384m heap/256m metaspace and single-worker Gradle settings. Already compiled dependency outputs are reused. Observe actual terminal and XML; no foreign process/daemon operation, resource preemption, arbitrary admission gate or outcome invention.

Self-approved scoped main-controller remediation under current user local-test authorization; no Provider, production build, DB migration or deployment.
