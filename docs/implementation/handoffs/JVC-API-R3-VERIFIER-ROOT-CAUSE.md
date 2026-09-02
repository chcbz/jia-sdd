# JVC-API R3 verifier root-cause matrix — 2026-09-02

## Scope and terminal state

- Task: `JVC-API`
- Candidate: commit `492adc7e8ff386013264c4eef4c0bf67adf34add`, tree `ef888807fb3b190b65d813286a0733795763b411`
- Selector: `JVC-API-R3-all-voice-focused`
- Fixture digest: `44547c9e422ad0ca70123edffbd5261030d502644048693f1d77aae7df1384b9`
- Gate: `blocked_root_cause` after two consecutive verifier failures
- No production deployment or voice Provider activation is authorized.

## Consecutive verifier failures

| Attempt | Evidence | Root cause | Outcome |
| --- | --- | --- | --- |
| R3 verifier 1 | Orchestrator denied before Gradle; exact tree matched; ignored `.gradle/` and module `build/` directories remained | Exact-tree clean guard includes ignored task-local build outputs left by the preceding focused run | Attributed; only the dry-run-enumerated ignored build outputs were removed (20,885,328 bytes); source stayed clean. |
| R3 verifier 2 | Evidence key `a442e9be86fd1dcf6037fdc3b8dd40e8e0c94e0936c78b143bcd39aae97c72fd`; kernel at `2026-09-02 23:02:42 +08:00` logged `oom-kill ... task=java,pid=3435519` and killed the Gradle daemon; no test XML | The single-use Gradle daemon overlapped a default 512 MiB test worker under host memory pressure; no Java assertion, Java OOME stack, or orchestrator-parent exit occurred | Second consecutive verifier failure; stop and require matrix-bound low-memory execution. |

## Authorized successor boundary

The only permitted successor is one fresh `gpt_test_runner` executing the same exact candidate and selector once with these controls:

1. Confirm no active Gradle/Vite heavy process. Remove only ignored paths enumerated by `git clean -ndX` inside the JVC API task worktree, then prove `git status --short --ignored` is empty before Gradle.
2. Use committed init script `docs/implementation/handoffs/JVC-API-R3-LOWMEM.init.gradle`, SHA-256 `49838b5598d6779b35c8407bc6be9b623d319d008d185fd1d59a5288ad0088fb`.
3. The script enforces test heap 64–256 MiB, metaspace 160 MiB, direct memory 64 MiB, one fork at a time, and `forkEvery=1` so Spring/Redis/Graal state is released between classes.
4. The Gradle single-use daemon must use at most 256 MiB heap, 160 MiB metaspace and 64 MiB direct memory; use `--no-daemon --max-workers=1` and do not add `--rerun-tasks` after the pre-run cleanup.
5. Run only `:chat:jia-chat-service:test --tests 'cn.jia.chat.voice.*'` through `cyf_orchestrator.py gradle`. Confirm all 11 voice test classes from XML with zero failures/errors/skips.
6. Any failure is terminal for this successor and must be attributed without retry. Do not stop production services, other threads, or unrelated processes to free memory.

## Promotion gate

After a successful low-memory selector, assign one fresh `sol_reviewer` to exact commit/tree. Only a `0/0/0 ACCEPT` may promote JVC-API to accepted and unblock integration pinning.

## CLI addendum after the pre-Gradle schema failure

The first authorized low-memory successor did not invoke Gradle: it invented `--tree`, `--gradle-args`, and `--tasks` options. A fresh successor must execute this shell command shape byte-for-byte, changing no option names or ordering:

```bash
python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle \
  --heavy \
  --cwd /home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-api \
  --tree-sha ef888807fb3b190b65d813286a0733795763b411 \
  --selector JVC-API-R3-all-voice-focused-lowmem \
  --fixture-digest 44547c9e422ad0ca70123edffbd5261030d502644048693f1d77aae7df1384b9 \
  JVC-API \
  ./gradlew --no-daemon --max-workers=1 \
  -I /home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-integration/docs/implementation/handoffs/JVC-API-R3-LOWMEM.init.gradle \
  "-Dorg.gradle.jvmargs=-Xmx256m -XX:MaxMetaspaceSize=160m -XX:MaxDirectMemorySize=64m -Xss256k -Dfile.encoding=UTF-8" \
  :chat:jia-chat-service:test --tests 'cn.jia.chat.voice.*'
```

All orchestrator options precede `JVC-API`; everything after `JVC-API` is the positional Gradle command. No pseudo-options are permitted. This addendum does not authorize a retry by the failed successor.

## Publishing-placeholder addendum after root evaluation failure

The byte-explicit command reached Gradle but omitted repository-local non-secret placeholders required by the root `publishing` block. The next matrix-bound successor must use the same command with exactly these additional Gradle project properties before the task path:

```text
-PrepoUsername=unused -PrepoPassword=unused
```

These are the established non-secret test placeholders used by repository scripts such as `agent/jia-agent-service/src/test/scripts/run-d09-isolated-mysql.sh`; they do not authorize publication and no publish task is invoked. The fully corrected tail is:

```bash
JVC-API ./gradlew --no-daemon --max-workers=1 \
  -I /home/isp/wsps/cyf/.worktrees/juyiting-voice-conversation-integration/docs/implementation/handoffs/JVC-API-R3-LOWMEM.init.gradle \
  "-Dorg.gradle.jvmargs=-Xmx256m -XX:MaxMetaspaceSize=160m -XX:MaxDirectMemorySize=64m -Xss256k -Dfile.encoding=UTF-8" \
  -PrepoUsername=unused -PrepoPassword=unused \
  :chat:jia-chat-service:test --tests 'cn.jia.chat.voice.*'
```

The failed successor is not authorized to retry. A fresh successor may execute the fully corrected command once after task-local ignored outputs are removed and exact clean state is re-established.
