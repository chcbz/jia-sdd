# W05 first full independent source review — 2026-09-06

Original reviewer `01a07116-f22e-7351-9af4-e66dbcee21da` reviewed all 32 W05 delta paths versus source-accepted W04 R3 on `fbee6395611837f3f6a08f4b32d762fa65c96037` / tree `dcef936f4c8a0d5350a06e511fd94ec2ecc77850`: **REJECT P0/P1/P2=0/3/1**. No runtime executed. Prepared W05 noDB script remains NOT authorized.

Paths below relative to `agent/jia-agent-service/src/main/java/cn/jia/agent/`.

| Severity | Finding / reproduction | Bounded closure |
| --- | --- | --- |
| P1 | `service/funding/FundedBountyQuoteClaimServiceImpl.java:65–85`: two constructors, neither injected, no default; real component scan cannot select production constructor. Fixtures use `new`. | Explicit production injection constructor and actual Spring bean creation regression. |
| P1 | same `:131–135,249–265,439–447`: runtime online/same three strings accepted despite null/stale/foreign binding_id. | Under-lock exact canonical identity/binding/runtime consistency as existing assignment; null/stale/foreign reject without claim/member/event changes. |
| P1 | `config/AgentTaskBountyQuoteSchemaInitializer.java:73–124`: names-only column checks, no index uniqueness checks, only two state CHECK expressions/ENFORCED, no arbitrary trigger exclusion. UNIQUE→normal same-name index or INSERT trigger mutating budget_covered passes. | Exact column/index/allCHECK/trigger contract, deny drift without repair; adversarial SQL/catalog source tests. |
| P2 | quote service `:119–124,522–531`: after valid quote then cancel/refund, same actor/key/body quote replay hits current FUNDS_HELD requirement before historical receipt. | Ownership remains required; immutable historical replay precedes new-operation state gates. |

## Ownership / no duplicate writer lease

Original W05 owner now owns W06 in separate `eco-v0-bounty-settlement`; W05 frozen candidate remains immutable. W06's combined source slice is explicitly extended to close these four inherited W05 findings without a second concurrent task lease or edits in W09's active tree. W05 waits for that corrected combined candidate. Record W05/W06 review/promotion separately; neither is accepted by this coordination change. W09 consumes the later corrected quote/claim paths by exact integration, not parallel repairs. Shared posting support stays W06-owned; no runtime until fresh independent review.
