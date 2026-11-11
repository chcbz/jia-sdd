# W09 bounded implementation packet

Full V0 implementation remains required, not just catalog API. Upstream working interfaces: W03 accepted ledger/wallet; W07 source accepted `b4614bd5` (noDB10PASS, MySQL in flight); W08 seed/package candidate `086a9dde` (unreviewed). Promotion waits accepted dependencies. Claim a clean separate API worktree after source owner admission; source-only phase, no live DML/install/Gradle. Critical transactional/ACL owner, ordinary later HTTP/UI slices may use Terra after exact freeze.

## Deliver one working source slice

- Exact-JWT-scope `GET /economy/capabilities` object (not `/agent/capabilities` list): flags and opaque server-derived stable scope fingerprint; private/no-store; default-off preview.
- Existing POST roster compatibility with canonical string version and true `boundToMe`/`canOperate` from trusted actor→owner mapping. Runtime/registry source currently has no general version field: implement/prove durable CAS token and all relevant lifecycle invalidation, never fake `1`, Number coercion, or timestamps. Monetary actor remains JWT `sub`, tenant `jiacn`, client `client_id`; legacy owner mapping is a separate verified lookup.
- Catalog/detail with exact server `canPurchase`, permissions, admin restriction; skill quote, actor-scoped immutable order-create receipt and current order GET per `v0-api-contract.md`. Target Agent explicit/scoped/current and version checked under transaction. Zero price still creates installation/order/entitlement but no fake ledger references.
- Purchase reserve + durable SKILL_INSTALL command/installation/PENDING entitlement in one real transaction, aftercommit dispatch. Use W08 frozen package bytes and IDs, W07 state/mapper contract. No network/filesystem inside money transaction.
- Exact authenticated Agent package GET `/internal/agent/skill-installations/{installationId}/package`, same-origin transport/current deliverable scoped command identity; no arbitrary path/download, no secrets in logs.
- Existing durable `work.result` handling needs a dedicated SKILL_INSTALL_RESULT branch, exact command/attempt/fence/epoch/Agent/order/package checks. Verified install result activates entitlement and captures once in same transaction; confirmed preactivation failure refunds once. Unknown/ambiguous result does not infer safe refund. Persistent GET must expose pending/ACTIVE/REFUNDED current state, no UI-only entitlement.
- W05 extension `FundedBountySkillEntitlementLookup` must use exact installed-and-ACTIVE scoped skill versions, never self-reported runtime ability strings. Integrate after W05 accepted-parent candidate, no edits to its active tree.

## Focused proofs

Actual transactional rollback/conservation and exactly-once reserve/capture/refund; insufficient funds; cross-scope/nonowner/stale Agent; quote/permission/admin tampering; concurrent/replayed purchase and result; free skill; package access and exact digest/size; install success active skill available to target Agent only; terminal conflict/unknown safe state. Source tests first, independent review then owned fixtures through orchestrator. No full production KMS/PoP/signature/isolation suite expansion.

## Ownership coordination

R01 rental writer owns its separate API worktree and hosting sources. Shared AgentController/AgentServiceImpl/identity/ledger touched paths require explicit integration handoff, no overwrite or silent branch merge. W08 seed resources remain immutable. W10 Agent candidate remains separate existing repository; reuse its frozen protocol, do not make a new repo in the deployed app directory.

## 2026-09-06 source readiness / ownership handoff

W03 ledger is accepted and W07 production schema is source-accepted (runtime retry remains pending); W08 package interfaces are frozen in clean `086a9dde`. These satisfy **source implementation** dependencies now; W07/W08 runtime/independent acceptance still blocks W09 promotion and release. Start W09 in new `eco-v0-skill-purchase` at `086a9dde`, not in the immutable seed/schema trees. R01 original critical owner takes W09 after handing off API `aa81221b` / runner `af40adbe`; prior R01 worktrees are immutable during this task. Merge the R01 API checkpoint into the W09 worktree first, preserving exact source where conflict-free and reporting any conflict, so existing roster/AgentService rental guards are retained. Own only W09 economy/skill, capabilities, durable Agent-version projection/lifecycle invalidation, exact package transport, result routing and matching tests. No R01 implementation redesign, Web/runner/installer changes, or ledger/schema foundation weakening.

W05 nullable-CHECK correction is finishing in a different worktree. Consume its final frozen source by coordinated integration before adding the installed-and-ACTIVE entitlement lookup; do not edit its owned funding paths or invent a duplicate interface. Source tests only; runtime starts only under a separate admitted verifier. Report a clean bounded checkpoint rather than silently omitting purchase/install/activation/refund success paths. Production KMS/PoP remains out of scope.

## Shared posting / non-rent credential closure — 2026-09-06

W09 removed its temporary shared posting edits; W06 exclusively owns the minimal shared posting extension. W09 requests `CAPTURE_SKILL` / `REFUND_SKILL` through existing `EconomyEscrowSettlement(SKILL_ORDER, ORDER/ESCROW, destination, amount, expectedEscrowVersion, reserveTransactionId)`: capture to `SYSTEM/SKILL_STORE/SKILL_STORE`, refund to original `USER/AVAILABLE`. W09 owns its order/facade transaction; no parallel edits to `EconomyPostingServiceImpl.java`.

Legacy owner/client-shared API keys cannot prove exact Agent identity. Approved narrow V0 correction, not a new identity platform: unique per-Agent delivery key association; exact-JWT owner + current canonical binding check; NEW key via existing `ApiKeyService` and association atomically; one-time private/no-store secret response with explicit lost-response recovery and manual supported-client profile setup. No live credential creation or filesystem/profile actions in source phase. Package security only for the frozen `/internal/agent/.../package` path; installer `X-API-Key` protocol unchanged. R01 `ManagedHostingCredentials` already creates fresh `hosting:<intentId>` keys; adopt those only after exact scope/name/current-binding verification and a unique W09 keyId association, never keyId-reference trust alone. Skill purchase must not silently require paying rent. Send exact setup DTO/status contract before Web wiring. No production PoP/KMS/general key-management expansion.

## Durable delivery/result recovery boundary

The existing Rabbit task-member ACL cannot authorize a skill order as a fake task. W09 owns a dedicated persisted order/installation authorization branch and exact delivery-key session send, leaving ordinary task dispatch unchanged. Same-wire WAITING/SENT recovery may reuse the original persisted outbox/message/command/attempt/fence/epoch after commit; no invented attempt or generic task retry refactor.

A persisted successful result may retain its original runtimeInstanceId after client reconnect. Acceptance must still prove the same canonical binding, unique installation delivery key, exact command/attempt/fence/epoch/order/package and a currently authenticated registered same-key session; do not reject sound durable replay solely because registration refreshed an ephemeral token. Purchase/new work still requires current readiness. Rotation while pending/unknown installation remains denied; no unsafe refund from mere reconnect/disappearance.

Hosted-key rotation may be explicitly unsupported to preserve R01 free reprovision. Enabled hosted purchase nevertheless requires a working verified adoption of the existing fresh R01 key into the unique Agent association, without manual server-profile changes or a new charge. If an explicit adoption HTTP action is needed, freeze its DTO first; perpetual fail-closed hosted purchase is not a completed success path.
