# OD07 serial claim

Status: active API slice after independent OD06 development ACCEPT; product writer released under this claim.

- Sole product writer: existing critical_worker `/root/od01_source_auth`; Root owns only control-plane/evidence.
- First slice: API `/home/chc/wsps/cyf-worktrees/output-api`, branch `codex/agent-output-delivery`, base `f1978b09ac7d567a53923f7c7e5c1bc3667e6a13`. Implement HTTP lease recovery/mutations and all policy1 entry guards, additive strict schema, real MySQL proof and policy0 regressions; freeze and independently review before client edits.
- Second slice: client `/home/chc/wsps/cyf-worktrees/output-client`, base `714b4aa73b474b37ec6348d045b653a3ca273cf2`. Connect ticket-bound lease lifecycle, bounded renewal and serialized heartbeat/terminal handoff; preserve output recovery. Freeze and independently review before accepting OD07.
- Web `/home/chc/wsps/cyf-worktrees/output-web` remains `212bfe4f9441cc82262d98e7b0723d6c0800e3d9` until its assigned task. No original checkout modifications, push, deployment or gitlink pin.
- Reviewer: independent read-only reviewer under project routing; never repairs its own findings. Existing provider fallback and scope must be recorded if reused.

Use implementation-handoff.md plus detailed-design section9, OpenAPI and schema contract. API proof must start positive cases through the real authenticated creation service; manual rows alone missed a real source authorization integration seam in OD06. All claim/start/heartbeat/release and recovery paths derive Agent identity from ticket and match dispatched/execution run; wrong run and old runtime never recover a lease token. Atomic receipt/body matching and root lock order must survive concurrent reassignment.

Portable examples: `../../lease-fixtures.json`, SHA256 `a6be57af7411d4d1a14e158a0be86f5552e117cd19adbb0bc7abd96f8e94fdb4`. Root Python jsonschema Draft202012Validator loaded the existing OpenAPI LeaseRequest: four valid action requests passed, three malformed requests were rejected, and four action-semantic negative requests passed the base schema as expected (their business rejection still requires API tests). This is static contract validation, not runtime lease evidence. Keep existing R1 fixtures.json and its accepted digest unchanged; API/client copy and consume the applicable new snapshot independently.

Policy1 remains closed to ordinary users while downstream submit/review is incomplete. Reject unsupported capability, multiple agents/required items, legacy/direct/result/funded completion and unsupported policy1+funded creation before any financial mutation; preserve policy0 funding. Record unchanged task/funding/event rows on failure in actual MySQL. Contract/schema adjustments go to Root with concrete rationale, not silent drift.

Every Gradle command holds `/tmp/cyf-gradle.lock`; reuse `/tmp/cyf-od02-evidence/run-gradle-with-od-env.py` and its existing development dependency configuration, with task-scoped tests. Check disk before packaging. Archive raw reports immediately; do not sum repeated/overlapping suites or rerun unaffected checks merely for freshness. Canonical packaging and residual R1 coverage stay open and do not become accepted when OD07 starts.
