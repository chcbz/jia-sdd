# JVC-OAI verification root-cause matrix

Date: 2026-09-03
Exact API commit: `e67747415d29687957150b7817a50e03f7c0aea7`
Exact API tree: `25ead36eb9fbbbba0648a3b5d7266934f12db188`
Status: `blocked_root_cause`; no product test executed in either attributed failure.

## Matrix

| Attempt | Failure boundary | Evidence | Root cause | Product implication | Authorized remediation |
| --- | --- | --- | --- | --- | --- |
| 1 | Gradle build evaluation, before tests | `build/reports/problems/problems-report.html`, SHA-256 `28f6fdbaee2437cbf3e0346df8a4b6e1e268d4b0bee7569694fb7aa14e153ae9` | The effective verifier command omitted `-PrepoUsername=unused`, `-PrepoPassword=unused`, and the intended bounded JVM arguments. | None; voice source/tests were not loaded. | Freeze the complete child argv before a new verifier is authorized. |
| 2 | `argparse`, before Gradle | exact stderr requires `--tree-sha`, `--selector`, and `--fixture-digest`; exit 2; no new XML/log | The main controller placed positional `task_id` before orchestrator options. Because `command` is declared with `nargs=argparse.REMAINDER`, everything after `task_id` became the child command. | None; Gradle did not start. | Put every orchestrator option before `task_id`; place the Gradle child argv after `task_id`. |

## Parser-only proof

No Gradle process was invoked. Importing `build_parser()` and parsing representative argv produced:

- options before `task_id`, no delimiter: `PARSE_OK`; child command begins `./gradlew`; both repository properties are preserved;
- options before `task_id`, `--` delimiter: `PARSE_OK`; `cmd_gradle` strips the delimiter;
- `task_id` before options: `PARSE_FAIL 2`, reproducing attempt 2.

## Frozen fresh-verifier command

```bash
python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle \
  --cwd /home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-api \
  --tree-sha 25ead36eb9fbbbba0648a3b5d7266934f12db188 \
  --selector 'cn.jia.chat.voice.*' \
  --fixture-digest ea3d920fc9dcd8e43f7b86fe2b440acc6812aea4aab195d225981d6b97c108c8 \
  --artifact chat/jia-chat-service/build/test-results/test \
  JVC-OAI -- \
  ./gradlew --no-daemon --max-workers=1 --no-watch-fs \
  -Dorg.gradle.parallel=false \
  '-Dorg.gradle.jvmargs=-Xmx256m -Xms128m -Xss256k -XX:+UseSerialGC -XX:MaxMetaspaceSize=160m -XX:ReservedCodeCacheSize=64m -XX:MaxDirectMemorySize=64m -XX:ActiveProcessorCount=2 -Dfile.encoding=UTF-8' \
  -PrepoUsername=unused -PrepoPassword=unused \
  :chat:jia-chat-service:test --tests 'cn.jia.chat.voice.*'
```

## Stop conditions

- A fresh verifier may run the frozen command once only after `authorize-remediation` binds this matrix and the exact tree.
- Any non-zero result stops without another retry and must be attributed independently.
- No source edit, deployment, Provider activation, OpenAI key access, or production operation is authorized by this matrix.
