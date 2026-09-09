# OD00 transaction prerequisite review

Independent read-only architect reviewed the uncommitted API worktree diff on 2026-09-09. Final source verdict: **APPROVE; local MySQL execution passed**.

Reviewed files:

- `chat/jia-chat-service/src/test/java/cn/jia/chat/service/AgentOutputAggregateMySqlTransactionTest.java` — SHA-256 `2eed4bede76d4fe8c5301656433d4e58fae9a432671a0b8f3247071bf8183e41`.
- `chat/jia-chat-service/build.gradle` — adds only `testRuntimeOnly libs.mysql`.

The initial cleanup blocker was repaired: the test uses a UUID32 database name, sets an ownership boolean only after successful CREATE, and drops only when that boolean and exact name pattern match. A failed CREATE cannot trigger deletion of an existing database.

The fixture uses production Agent/Chat DAOs and MyBatis mappers, `AgentTaskMutationTransactionImpl`, the transaction manager returned by `DataSourceConfig`, and `SpringManagedTransactionFactory`. It asserts successful commit of both module writes, deliberate-exception rollback of both, an active resource-bound transaction, exact mixed-case scope checks, and a loopback/port/MySQL-version fence. No mocks, H2, or explicit secret logging substitute for the real database proof.

This is a component slice on one physical datasource. It does not establish deployed starter configuration, dynamic datasource routing, or AOP/proxy wiring. Those remain downstream release gates. The subsequent lock-held Gradle execution passed: 1 test, 0 failures, 0 errors, 0 skips, 4.711 seconds. See transaction-test-result.xml. This run used the separately reviewed local dependency substitutions, not canonical production packaging. Reviewed code is committed as `f418e3f5bf7afcdbddf9c1ecec1b293f657c977c`.

The reviewer also approved the final lowercase task-ID negative assertion; this document hashes that frozen reviewed version.
