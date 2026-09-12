# Binary request-body preservation candidate

Candidate f1978b09ac7d567a53923f7c7e5c1bc3667e6a13, parent43e6bb94. Real TASK publication exposed binary corruption before the upload controller: PNG source, snapshot and Node request body were109 bytes with equal SHA, but the global log wrapper decoded/re-encoded the body as text.

The exact output PUT route now passes the original stream through a metadata-only wrapper. The real log service records sanitized metadata without calling servlet parameter parsing on that wrapper. Ordinary cached requests replay original byte[]; textual audit/reader conversion uses the declared charset or UTF8 fallback. Authentication, upload verification and limits are unchanged.

Affected tests: UriAccessLogFilterTest4 and LogServiceImplTest26, total30, all passed. The new cases exercise the actual filter and log service with a mocked DAO, including binary bytes, no-query form mislabeling, Chinese JSON and route/context/method boundaries. This is component evidence, not yet restarted-server HTTP evidence.

Root verified clean frozen source, preserved raw XML/r5 Gradle stdout, checked source hashes and three compiled classes against the bootJar. Development bootJar is228808922 bytes, SHA2561438fa8d59e8de9e1ab8ab65c5c19698725d5b59e1031b7654f8b232e6a71f6d. Command confirmed by the writer; the same execution produced tests and bootJar in4m29s. Earlier failed dependency attempts are not counted as tests.

Independent review is pending at this evidence commit. Actual binary upload/publication/offline retrieval and fresh browser smoke remain pending; canonical dependency/package and production gates are separate.
