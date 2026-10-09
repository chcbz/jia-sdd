# Tenant-only implementation and local verification

Scope authority: scope-closeout-20261009.md. Develop is integrated; independent merge review accepted the four pinned repositories. This is not business acceptance. Historical R4 failures remain historical and must not gate this task.

## Ownership and execution

Sole writer: existing r4_recovery_finalize, fresh actual gpt-6.1-sol/high verified by main before work. No subagents, model fallback or phase confirmation. You are not alone in the workspace; preserve unrelated edits and the main-owned integration.yaml changes. Do not touch the original /home/chc/wsps/cyf worktree. API/Web feature worktrees own the necessary source/tests; Root owns short feature handoff records. Runtime is already merged and is not an implementation target for this tenant-only task.

Implement the minimum runnable tenant1 business test area, not a platform. Preserve existing owner/client permissions; removing an unnecessary platform dependency must not remove resource ACL or trust client-provided tenant values.

## Known gaps to close

1. Local profile only exposes conversation and requires deployment/data-domain registration tables; the legacy route gate denies most tenant1 Hall/task APIs. Establish the tenant-only mode with trusted authentication and explicit allowed tenants; keep unrelated platform mode separate and intact. Reuse develop identity/account security rather than creating another login protocol.
2. Propagate the authenticated tenant through opened Hall map/roster, conversation including public/private/task scopes, library/material/file and task create/assign/report flows. Replace relevant hardcoded tenant0 with explicit trusted scope. A resource ID, header, body, persisted event or async callback cannot override that scope.
3. JuyitingConversationScopeService admission overload passes ownerJiacn into a misleading tenant-named parameter; the merged body still queries fixed tenant0. Make the owner/tenant contract explicit and support trusted tenant1, with regressions where owner differs from tenant and cross-owner/tenant access is denied. The premerge owner-as-tenant query defect is historical, not a new merge regression.
4. Frontend fixed tenant1 login/recovery/cache must work without unrelated data-domain lifecycle/revision claims. Preserve tenant/client/user namespacing, cancellation, stale response rejection and develop return navigation/draft behavior. An old tenant0 token must not silently become tenant1.
5. Enable the tested ordinary Hall/business flows. Keep schema installation, real payment, production hosting/provider actions and production Rabbit publication/consumption off in the test process. Do not claim success by disabling all business. Map remains /agent/map and roster /agent/roster.

Before modifying a path, trace its actual caller/ACL and keep the edit bounded. Shared schema is not to be migrated automatically. If an existing business column genuinely is missing, report the exact evidence and smallest required migration instead of inventing a domain platform.

## Build and test

- First verify merged code types and fix actual compile issues. All Gradle commands hold /tmp/cyf-gradle.lock. Place new caches, project cache, outputs and logs under a task-specific mktemp directory on /mnt/Workspace; root disk is nearly full. Do not clean unrelated caches or processes.
- Run frontend build and targeted tenant identity/cache/HTTP/SSE/Hall regressions. Run relevant backend scope/auth/controller/DAO tests, including tenant0 compatibility and negative tenant0/1 read/write checks. Tests must show usable authorized paths, not just rejection.
- Preflight the existing configured shared database with read-only metadata checks, credentials kept in process memory and never printed. Do not reuse the other economy task MySQLs on 33307/33630, create a second long-term database, copy tenant0 production data or seed unknown tenant1 ownership.
- Launch own feature services on distinct ports, then perform actual frontend/API tenant1 positive flows and cross-tenant negative checks including stale browser state and relevant file/event/async boundaries. Initially no shared-DB DDL/DML; once tenant1/test identity ownership is established, only API-created task-owned test resources may be exercised. Preserve IDs and cleanup scope; do not delete existing data.
- Keep source edits and commands/results concise. No new giant pin/collector/approval protocol. On an actual environmental blocker, exhaust safe scoped checks and report the exact missing authority/configuration; never claim READY from unit tests alone.

Stop source writes for independent read-only review after the runnable candidate and verification evidence are ready. Main coordinates review and sends the authorized acceptance email to chcbz@sina.com only after READY, recording SMTP acceptance accurately. No push, production deployment or email send by writer in this task.
