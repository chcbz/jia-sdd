# Live WebSocket diagnosis (in progress)

Accepted API source baseline remains `52cc2aae`. The sole writer has an uncommitted `DefaultSecurityConfig` repair permitting `DispatcherType.ERROR`; ordinary private and `/error` requests remain authenticated. The scoped report `DefaultSecurityWebSocketPermitTest` contains 2 tests, 0 failures/errors/skips (timestamp `2026-09-12T14:36:06.027Z`, SHA-256 `f70d9e497b5823aa368d279caed810248013fffb9e6cfaf09cb3c7fb4d4fa05b`). Root inspected that report; this is not independent repair approval or full-context validation.

Root independently observed r8 startup and anonymous `/ws/chat` Upgrade returning HTTP500 with standard Boot JSON at approximately 22:43–22:44 Asia/Shanghai on 2026-09-12. Before the repair this route returned401. No application message or API key was sent. These observations prove error unmasking, not successful WebSocket handshake.

The writer subsequently reported the original r11 response exception: `BadSqlGrammarException` from `UriAccessLogFilter -> LogServiceImpl.addLog`, with the isolated database missing `CORE_LOG`. The response was not saved; this is the writer's tool-observation summary. The r11 application log does **not** contain that exception stack. Do not describe it as an archived raw trace.

Root read-only schema inspection found112 tables: the inspected user, OAuth and chat entity table names were present exactly, while `LogEntity` requires uppercase `CORE_LOG` and only a lowercase `core_log` fixture existed. The writer owns correction of that empty task fixture using the repository schema. `CORE_DICT` and `CORE_NOTICE` were also absent; they have not been identified as required for this handshake. This is isolated development bootstrap work, not production migration acceptance.

`package-metadata.json` records mixed Boot versions and their differing error configuration prefixes from the actual jar. The missing log table explains the observed request failure; the metadata observation alone does not establish a dependency defect. Temporary diagnostic properties must be removed from the isolated runtime after diagnosis.

Pending: clean-config handshake, repair commit and independent review, trusted dispatch/ticket exchange, actual accepted-client publication, owner download after stopping only the synthetic Agent, and the remaining R1/R2 acceptance matrix.
