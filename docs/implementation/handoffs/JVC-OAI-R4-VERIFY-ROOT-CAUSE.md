# JVC-OAI R4 verification root-cause matrix

Date: 2026-09-04
Exact candidate commit/tree: `e180458fa0783f9e20e754f2e4230a55dbd61f70` / `087cffcd55f8c48b4eb9e91babfea8fcb470d70d`
Previous reviewed candidate: `027bccc6d406705620039de9608b48709f4657f2` / `f53511028f7ed0b888a8fd663655ef04af6a84a9`
Status at creation: `blocked_root_cause`; no R4 Gradle command has run.

| Attempt | Boundary | Root cause | Product implication | Matrix-bound action |
| --- | --- | --- | --- | --- |
| R3 review | Static independent security review of `027bccc6` | Post-unlink cleanup still deleted by stale pathname; admission happened after spool/parse/hash; only the first response `Content-Type` was checked; a shared core `Path` API was replaced by `FileChannel` without compatibility. | R3 was unsafe and cannot merge. | R4 source commit `e180458f` moves post-unlink lifetime to the handle, moves admission before upload materialization, rejects ambiguous headers, and restores the public `Path` record while keeping the handle-only provider path internal. It remains unverified. |
| R4 verification dispatch | Before any Gradle/selector execution | Assigned `gpt_test_runner` received `HTTP 503 auth_unavailable` from the Codex verification provider. No child command, XML, evidence key, source mutation, deployment, key operation, or flag operation occurred. | This is an infrastructure/auth failure, not a passing or failing product test. The exact R4 candidate has no runtime evidence yet. | One fresh GPT verification agent may run the frozen commands once each on the unchanged R4 tree. Any command failure must stop and be attributed; no source edit is authorized by this matrix. |

## Frozen verification contract

Preconditions:

- clean worktree at `e180458f` / `087cffcd`;
- all orchestrator options precede task ID;
- no concurrent Gradle invocation; and
- no production/key/voice-flag action.

1. Voice selector:

```bash
python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle \
  --cwd /home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-api \
  --tree-sha 087cffcd55f8c48b4eb9e91babfea8fcb470d70d \
  --selector JVC-OAI-R4-voice \
  --fixture-digest R4-087cffcd \
  --artifact chat/jia-chat-service/build/test-results/test \
  JVC-OAI -- \
  ./gradlew --no-daemon --max-workers=1 --no-watch-fs \
  -Dorg.gradle.parallel=false \
  '-Dorg.gradle.jvmargs=-Xmx256m -Xms128m -Xss256k -XX:+UseSerialGC -XX:MaxMetaspaceSize=160m -XX:ReservedCodeCacheSize=64m -XX:MaxDirectMemorySize=64m -XX:ActiveProcessorCount=2 -Dfile.encoding=UTF-8' \
  -PrepoUsername=unused -PrepoPassword=unused \
  :chat:jia-chat-service:test --tests 'cn.jia.chat.voice.*'
```

2. Only if selector 1 passes, ChatController selector with the same child JVM/repository constraints, selector `JVC-OAI-R4-chat`, fixture digest `N/A`, and `--tests 'cn.jia.chat.api.ChatControllerTest'`.

Each selector must be copied into its own new immutable `/tmp/cyf-evidence/jvc-oai-r4-{voice|chat}-087cffcd.../` directory with `SHA256SUMS`; report the orchestrator evidence key, manifest hash, test count and resource snapshot.

## Mandatory post-verification review scope

A fresh reviewer must check that the runtime results cover the four prior findings and inspect the resulting exact tree for:

- any reintroduced pathname open/delete after unlink;
- admission acquire/release correctness across reject, upload failure, digest failure, provider failure, replay and success;
- zero/multiple/comma-delimited/charset-conflicting content-type responses; and
- public core ABI compatibility without restoring provider path reopen.

Only `ACCEPT P0/P1/P2=0/0/0` may authorize fast-forward to `api/origin/develop`. Production activation remains separately forbidden.
