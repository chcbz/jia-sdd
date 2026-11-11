# OPS-RESOURCE-TELEMETRY R5 authoritative-review root-cause matrix

Date: 2026-08-29 CST

Exact rejected candidate: `fc425328c5e73e3c43dbc421c8f9aeaeb4f132d1` / tree `1473cc18b08dc716fe7693f81f8d113b259cd0cb`.
Authoritative verdict: REJECT P0/P1/P2=`0/3/1`.

| Finding | Observable failure | Root cause | Bounded R6 remediation | Required adversarial proof |
|---|---|---|---|---|
| Owner/controller identity | A same-uid process can copy the ledger Owner strings and perform an otherwise legal transition; trust tooling and paths remain writable by shared root | Actor identity is self-asserted and the proposed signature verifier is not an enforceable boundary on this host | Do not claim shared-root cryptographic isolation. Remove or fail closed for unauthenticated cross-process owner/controller mutation; bind mutations to a controller-created, one-shot external capability whose trusted verifier/material is provisioned outside shared writable roots, or explicitly reduce the contract to alert-only with no false authority claim | Cross-task Owner impersonation, writable-verifier substitution, absent/unprovisioned trust-root denial |
| Terminal state machine | Normal unchanged-tree `accepted -> done` fails digest matching; `accepted -> integrated` can replace reviewed SHA/tree | Grant request digest is reconstructed from mutable post-review gate/owner state, and integrated is outside terminal reviewed-tree enforcement | Bind promotion authorization to immutable reviewed request identity carried across terminal states; apply exact reviewed-tree equality to accepted/done/integrated and test normal legal progressions | review→accepted→done unchanged-tree PASS; accepted→integrated unchanged-tree PASS; any SHA/tree swap DENY before mutation |
| Approval consume TOCTOU | Path swap after descriptor verification can create a wrong consumed hardlink; ledger mutation is denied but nonce is poisoned | Verification uses an fd, consumption links by pathname, and mismatch cleanup is incomplete | Consume the verified inode atomically or use fail-closed rename/openat2-style semantics; on mismatch leave neither consumed nor mutated state | Deterministic path-swap race: DENY, consumed path absent, active original recoverable, ledger unchanged |
| Contract/tests | Docs still describe profile-only observation/atomic move; tests mock signature checks and omit legal terminal transitions/impersonation | Implementation, durable contract, and executable attack matrix diverged | Synchronize docs and add non-mocked end-to-end probes for every authority boundary and normal terminal route | Full unittest plus explicit four R5 findings and all new R6 probes PASS |

R6 is limited to these findings. It must not add process termination/preemption, restore a global Writer queue, operate Gradle, or touch production. A fresh independent reviewer must attack the same matrix before acceptance.
