# OPS-RESOURCE-TELEMETRY R6 authoritative-review root-cause matrix

Date: 2026-08-29 CST

Exact rejected candidate: `7b244b4785d34c644e9f9d5e8f09371b1328a657` / tree `28e7dc2875d120dfd74aa0668f896471aeb72e8f`.
Authoritative verdict: REJECT P0/P1/P2=`0/3/1`.

| Finding | Reproduction | Root cause | Bounded R7 remediation | Required proof |
|---|---|---|---|---|
| Reviewed request identity can change | accepted uses evidence K1; done uses different same-tree K2; `done rc=0` | Review identity is rebuilt from each transition call and is not durably bound across terminal states | Persist/bind one immutable reviewed-request identity outside mutable call arguments and require exact equality for accepted/integrated/done | K1→K1 legal routes PASS; K1→K2 denied before mutation; SHA/tree swaps denied |
| Approval race poisons active nonce | Path replacement between initial load and consume leaves active replacement; rollback hardlink leaves original nlink=2 and retry denied | Initial verification fd is closed before consume; pathname is reopened; rollback validates inode but does not restore single-link retriable state | Keep verified descriptor/inode through atomic consume, or use a controller-owned atomic protocol; on any race restore original active path with nlink=1, no consumed path, no backup link, ledger unchanged | Deterministic path-swap: DENY and exact retriable original; immediate clean retry succeeds |
| Legal authority evidence remains mocked | Terminal and TOCTOU tests mock signature/mutation guards; stock CLI only demonstrates unconditional denial | No executable isolated controller boundary exists for legal-path tests | Provide an actual isolated controller executor/capability boundary and run end-to-end legal mutations plus denial attacks without mocking authority/consume primitives | Non-mocked review→accepted→done/integrated PASS; impersonation/path-swap DENY |
| Docs conflict with executable contract | Docs call repository CLI the mutation/Gradle entry while code unconditionally rejects stock CLI | Operational contract was only partially updated | Make docs identify the actual isolated controller executor and the read-only/shared CLI boundary; remove impossible commands | Byte-exact docs/tests/CLI catalog agreement |

R7 is limited to these findings. No Gradle, process termination, preemption, global Writer queue, production action, or unrelated refactor. Fresh independent review is mandatory.
