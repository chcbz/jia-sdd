# Affected regression execution notes

Working directory: `/home/chc/wsps/cyf-worktrees/output-api`. The writer used the prepared Java 21 environment and the reviewed local dependency substitution init. These are local development results, not canonical packaging or production acceptance.

## Agent service

The root parsed `AgentServiceImplTest`'s actual JUnit XML at `2026-09-09T18:02:01.793261Z`: 74 tests, zero failures/errors/skips, suite timestamp `2026-09-09T17:54:37.205Z`. The following fixture task replaced that XML before archival. The observed attributes are retained in `observation.json`; there is no archived raw XML for this suite.

Writer-reported execution: exit 0, `BUILD SUCCESSFUL in 1m 24s`, with this command:

```bash
flock /tmp/cyf-gradle.lock ./gradlew --include-build plugin --init-script /home/chc/.local/share/cyf-output-tools/od00-development-opencv-substitution.init.gradle --no-daemon --max-workers=1 -Dorg.gradle.jvmargs='-Xmx512m -XX:MaxMetaspaceSize=256m' :agent:jia-agent-service:test --tests 'cn.jia.agent.service.impl.AgentServiceImplTest'
```

No rerun was requested solely to replace the overwritten archive.

## Chat protocol, security and dispatch

Six raw JUnit XML reports are archived here: 33 tests, zero failures/errors/skips. The writer reported exit 0 and `BUILD SUCCESSFUL in 1m 19s`, using the same Gradle parameters with `:chat:jia-chat-service:test` and selectors for the six classes listed in `observation.json`.

Before further Gradle test tasks, copy each completed task's XML to a distinct local evidence path. Root credential scanning and archival can then happen without racing Gradle's report replacement.
