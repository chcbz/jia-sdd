# MMD API acceptance-to-test freeze — 2026-09-28

| Acceptance/invariant | Planned evidence on merged exact tree |
| --- | --- |
| Six expected conflicts resolved without whole-file ours/theirs; merge commit has both parents | `git status`, conflict resolution record, `git rev-list --parents -n1`, `git diff --check` |
| HTTP sender spoof cannot enter durable user row/event/wire (F1) | Add adversarial durable service/controller regression; retain `HumanSenderIdentityResolverTest`, `ChatControllerTest` |
| Agent final/delta spoof cannot enter durable final row/event | Add/adjust durable WebSocket regression using authenticated runtime identity; retain `AgentSenderIdentityResolverTest`, `AgentWebSocketHandlerTest` |
| Exact tenant/owner/client/generation/callback binding and idempotency | `chatDeliberation` tests: service, transaction contract, router, tenant, replay, outbox |
| Durable outbox ACK/retry/reconnect semantics remain | `chatDeliberation` outbox/relay tests plus touched WebSocket tests |
| Trusted taskMaterials and builtin SongJiang prompt boundary remain | existing `ChatControllerTest` / `JuyitingAgentRelayServiceTest` targeted regressions; static diff inspection |
| Managed multi-owner/first-registration authorization remains | `managedHostingHandshake` plus touched compile/static inspection; no deployment |
| Native START semantics remain | source diff confirms no semantic replacement; use existing focused test only if touched/required, no heavy suite |
| Schema is additive/fail-closed | `ChatDeliberationSchemaContractTest`; no production DDL and no isolated MySQL claim |
| F2 capability negotiation, F3 full reconstructable context, F4 INSPECT execution | Report as NOT FIXED; tests may demonstrate existing behavior but cannot be marked accepted |

Gradle, if assigned at `targeted_verification`, will run only through `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle`, on a committed exact tree, with no paid provider/model invocation.
