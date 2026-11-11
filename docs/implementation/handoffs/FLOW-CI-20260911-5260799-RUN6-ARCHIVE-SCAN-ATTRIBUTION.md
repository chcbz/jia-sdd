# Flow 5260799 Run 6 post-build bridge attribution

**Queried:** 2026-09-10T23:04:46Z  
**Run/job:** pipeline `5260799`, Run `6`, Job `512770431`  
**Source recorded by Flow:** tip `07f5140c11078942efdb7486e0db7e8c235443c2`; ticket-built commit `903c24edb69ebbd2b126fa3cb620e47114bf30e9`.

Run 6 is not a current-source candidate. It reused the expired old ticket SHA `edc3e2bf…ff5` and its exact old source/tree/tool bundle/fixture. The cloud Gradle execution itself completed: `BUILD SUCCESSFUL in 4m 30s`, 201 tasks, four XML suites / 72 tests, zero failures/errors/skips. The mandatory receipt gate correctly failed with bridge rc `70`, `status=bridge_failed`, and no application JAR.

The Run 6 inspect output did not expose `receipt.error`, so it cannot independently name the archive dimension. However, it used the exact same immutable ticket, source tree, fixture and tool bundle as the previously preserved Run 3 receipt whose concrete error is `artifact archive inspection limit exceeded`; that run also proved clean source and valid OpenCV provenance. Therefore Run 6 is attributed to the same old bridge archive-budget failure, not to Gradle, tests, private Maven/OpenCV resolution, or Flow context initialization. The old tool emits only the common message and cannot distinguish `declared_size` from `entry_count`.

Do not retry Run 6 or reuse its ticket. The bounded remediation is to run the latest source `07f5140c…` with the already-versioned diagnostic bridge that retains all scan limits and reports only the failing numeric dimension/counters. Use a fresh controller ticket and the 8.5KB ticket-only Flow configuration; no deployment occurs in this diagnostic CI run.
