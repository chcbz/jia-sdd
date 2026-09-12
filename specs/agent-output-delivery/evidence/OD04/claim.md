# OD04 claim — Agent automatic output delivery

Sole product writer: critical_worker `/root/od01_source_auth`. Client worktree: `/home/chc/wsps/cyf-worktrees/output-client`; branch `codex/agent-output-delivery`. Upstream API `4c292cc35e4d82a23620a85296b721569ff59bd5` passed independent development review. Existing user authorization covers continued serial implementation.

Before editing, verify clean worktree and fast-forward to existing client master `f8c731d0cef38956bb3dabaa628c6188c0040bed` so conversation-session persistence fixes are preserved. Original analysis baseline remains recorded separately. Confirm actual base in handoff.

Own output modules, client execution/protocol/queue integration, installer staging, direct regression tests and client documentation. Follow `preparation.md` and frozen contracts. Snapshot and durable queue inside workspace/output-root lock; network after release; terminal report only after publication; restart resumes snapshot and pending terminal intent without invoking the model again. Trusted context must survive adapters/fingerprints; tickets remain bridge-memory-only. Cover command and chat, manifest-designated code artifacts, path/link/change attacks, interrupted transfer/ACK loss/restart, session regression and installer syntax/staging.

Do not change original checkouts, install host services, deploy, begin OD05 or self-accept. Freeze a verified candidate and provide real commands/exits/results for independent read-only review. Root owns control-plane evidence; preserve concurrent user changes.
