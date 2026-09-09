# OD00 local build execution — PASS with dependency deviations

- API commit: `f418e3f5bf7afcdbddf9c1ecec1b293f657c977c`.
- MySQL: actual isolated 8.0.45, loopback port 13306.
- Selector: `:chat:jia-chat-service:test --tests cn.jia.chat.service.AgentOutputAggregateMySqlTransactionTest`.
- Result: BUILD SUCCESSFUL in 10m21s; 1 test, 0 failures, 0 errors, 0 skips, 4.711s; report timestamp `2026-09-09T12:49:02.558Z`.
- JUnit XML SHA-256: `ba6397dd5e5bd680ae43356c420901271defd4383c39dcb2c49b10e6589cb554` (archived `transaction-test-result.xml`).
- Init SHA-256: `20060f26083e1ae3c61c5e70f3d0157f805b95ad9e6b1900318879ca263e6058` (archived `gradle-development.init.gradle`; host/worktree-specific verification configuration, not production build configuration).
- Independent source reviewer: architect, APPROVE; see transaction-review.md. Test writer: critical_worker. Environment/test execution: balanced_worker fallback because the configured DeepSeek Flash provider was unavailable.

## Reproduction on this host

`/home/chc/.local/share/cyf-output-tools/od00-run-chat-transaction-development.sh` (mode 0700, SHA-256 `53434f8a13b92bf4582d95be1a2fd371be11c3a632d6008a544bac2b98b7fcc8`) reads private disposable-MySQL credentials internally and runs:

```bash
flock -w 120 /tmp/cyf-gradle.lock ./gradlew --no-daemon --max-workers=1 \
  '-Dorg.gradle.jvmargs=-Xmx512m -Dfile.encoding=UTF-8' \
  -I /home/chc/.local/share/cyf-output-tools/od00-development-opencv-substitution.init.gradle \
  :chat:jia-chat-service:test --tests cn.jia.chat.service.AgentOutputAggregateMySqlTransactionTest
```

The wrapper sets the isolated MySQL environment and user-space JDK. Do not paste credentials into command lines or logs. All Gradle commands held the global lock. The operator confirmed no Gradle build process remained before handing build ownership to OD01.

## Dependency evidence and limits

The archived dependency insight logs verify `org.opencv:opencv:4.5.5 → org.openpnp:opencv:4.5.5-1` and `com.sun.media:jai_imageio:1.1 → javax.media:jai_imageio:1.1`. These same-API public packages enable targeted compilation and transaction tests; they are not declared equivalent for native/OpenCV/OCR/TIFF runtime behavior or production packaging. Canonical `javax.media:jai_core:1.1.3` resolves from OSGeo.

The user identified `/home/chc/.m2/settings.xml` for private repository settings. Its endpoint failed TLS verification with a self-signed `comhostnew-proxy / CN=localhost` certificate; no credentials were sent past that failed handshake, TLS verification was not disabled, and fetched certificates were not automatically trusted. Canonical packaging requires a trusted CA/endpoint or separately reviewed dependency changes and remains an OD06 gate.

A subsequent credential-free direct-socket check with the system CA store also rejected `repo.rdc.aliyun.com` as self-signed, while `maven.aliyun.com` verified successfully. No HTTP(S)/ALL proxy environment variables were set for that check. The failure is therefore not limited to the Gradle/Java trust store; changing Java alone is not an evidenced fix.
