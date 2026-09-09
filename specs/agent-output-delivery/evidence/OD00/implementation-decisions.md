# OD00 implementation decisions — independent architect, 2026-09-09

## Local build dependency deviation

The user-space included Gradle plugin compiled successfully. Public Aliyun/Central resolution reaches `common:jia-common-core:compileJava`, then cannot resolve legacy `org.opencv:opencv:4.5.5`. This is an unrelated `compileOnly` dependency used by `OpenCvUtil`; the former host’s Gradle bootstrap is absent. The user subsequently identified `/home/chc/.m2/settings.xml` as the authoritative private repository configuration; canonical dependency verification is now being restored from that file without exposing or committing credentials.

The architect permits an **explicit local dependency substitution** to a publicly published package exposing the same OpenCV 4.5.5 `org.opencv.*` Java API, subject to artifact/API verification. The helper verified `org.openpnp:opencv:4.5.5-1` as a local fallback. The fallback is superseded if the user-provided private repository resolves the original artifacts. No stub JAR, relabelled artifact, production catalog edit, or native OpenCV test is allowed to stand in for the canonical dependency.

Evidence must include the separate init script hash, resolved dependency coordinates (`dependencyInsight`), and selected agent/chat test results. Mark such results **local dependency deviation**. OD06 must still build the production candidate using its canonical dependency/repository configuration. The canonical repository currently presents an unverifiable self-signed `comhostnew-proxy / CN=localhost` certificate. No TLS bypass or automatic trust of the fetched certificate is permitted, and no repository credentials were sent past that failed handshake. A user-supplied trusted CA or trusted endpoint is pending. Continue local verification with explicit substitutions; retain canonical packaging as an OD06 gate. The selected agent/chat application build and real MySQL test have now passed with the reviewed local substitutions (see transaction-test-result.xml); canonical production packaging remains unverified.

The architect also approved local-only `com.sun.media:jai_imageio:1.1 → javax.media:jai_imageio:1.1` from the public OSGeo release repository: the helper verified its sole referenced `com.sun.media.imageio.plugins.tiff.TIFFImageWriteParam` API. Record both coordinates in dependency insight. `javax.media:jai_core:1.1.3` is available under its original coordinate from OSGeo. No OCR/TIFF behavior is exercised by the OD00 selector; image-processing compatibility and canonical packaging are not claimed.

## Physical migration sequencing

Logical migration definitions remain as designed; descriptive ordered SQL resources may divide their implementation across serial tasks:

| Task | Physical segment / responsibility |
| --- | --- |
| OD01 | `output-delivery-001-identity-schema.sql`: source/run/access-ticket tables and three nullable runtime capability columns |
| OD02 | `output-delivery-002-object-schema.sql`: quota/upload/object/reference/receipt/verification structures |
| OD03 | `output-delivery-003-publication-schema.sql`: chat output publication schema; nullable task artifact extensions remain logical M002 |

Names are illustrative until implementation, not a new semantic schema version. Follow the existing opt-in MySQL schema initializer style: repeatable DDL, exact catalog validation of column types/index order/collation/engine, rejection of incompatible partial schemas, and no row backfill or tenant=0 fallback. Test fresh and already-upgraded disposable databases. Features remain disabled until every schema segment they require validates; merely applying identity DDL cannot expose file writing or publication. Building/testing does not authorize executing migrations against production.

## Transaction proof boundary

A narrow test may use the production `DataSourceConfig.transactionManager` factory, real `AgentTaskMutationTransactionImpl`, `AgentTaskMetaDaoImpl.updateStatusByVersion`, and `ChatConversationDaoImpl.insert` sharing one MyBatis Spring-managed datasource. Assert commit and deliberate failure rollback across both modules, active/resource-bound transaction, and exact mixed-case scope behavior on real MySQL/InnoDB. This proves the components can enlist in one physical transaction. It does not prove the deployed aggregate uses that topology; deployed datasource routing remains OD06/OD11 evidence.
