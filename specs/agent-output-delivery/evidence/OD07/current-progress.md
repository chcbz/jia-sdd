# OD07 current checkpoint

2026-09-13: active, not accepted. Sole product writer `/root/od01_source_auth` owns API worktree. OD06 development ACCEPT remains in ../OD06/accepted-r1-development-review.md; R1 release gaps stay open. Web212bfe4 and client714b4aa are unchanged.

- API3343342b committed M003A strict schema/entity/mapper preparation. Later uncommitted work corrects feature-off migration and adds run-bound lease core. Do not reset or cherry-pick over the writer's working tree.
- Writer reported the first targeted `:agent:jia-agent-service:compileJava` passed for lease-core work. This is compile evidence reported by the operator, not business tests or a final-candidate association; actual command/log will accompany the frozen handoff. No broad suite is counted as passing.
- Current implementation: HTTP lease request/public-response DTOs, transaction adapter and same-transaction receipt, then Controller/security and scoped tests. Still due: real dispatch writes dispatched_run_id, policy1 admission, all legacy/direct/aggregation/funded guards, actual MySQL adversarial/feature-off policy0 regression, and independent final API review. Client lease lifecycle follows frozen API acceptance.
- Root prepared lease-fixtures.json, preserving R1 fixture bytes. Root helper8a908ae is independently accepted for synthetic controls only (seven methods); see accepted-lease-probe-8a908ae.md. No live lease request or new API service startup has occurred.

Existing API10018 still runs the immutable accepted R1 package; the previous synthetic Agent and fault proxy are stopped, its persona intentionally unbound. New trusted live operations require one explicitly designated operator and a new disposable binding; no user Agent or original checkout is touched. Every Gradle invocation holds /tmp/cyf-gradle.lock and uses the existing OD development wrapper. No push, deploy, pipeline trigger or gitlink pin is authorized by these local checks.
