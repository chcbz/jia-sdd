# OD03 claim — publication and authenticated retrieval

- Sole API writer: critical_worker `/root/od01_source_auth`.
- Worktree/branch: `/home/chc/wsps/cyf-worktrees/output-api`, `codex/agent-output-delivery`.
- Base: `a04c2feb634643fc7e52289aa2b4a98ddf61bbb3`; upstream approval is `../OD02/accepted-review-a04c2feb.md`.
- Ownership: Agent artifact extensions/M002, Chat output persistence/services, publication/receipt/reference transactions, capabilities, exact UserJwt read/download routes and RunTicket publication routes, associated tests. Root owns coordination/evidence; preserve other worktrees and unrelated edits.

Execute `implementation-handoff.md` and `../OD02/next-task-handoff.md` against the frozen root contracts. All eleven OD03 HTTP operations are required. First verify the shared real-byte publication/download slice for both task and conversation, then privacy/version/pagination/replay/GC races. Authenticated owner reads must survive Agent disconnection and write pause, without relying on selectable Agent or the legacy workspace gate. No Agent → Chat implementation dependency or fake storage URI.

Every Gradle command holds `/tmp/cyf-gradle.lock`; reuse installed development dependencies and retain their release limitations. Freeze a tested candidate for independent read-only review before OD04 begins. No OD03 endpoint or end-to-end acceptance is claimed at task start.
