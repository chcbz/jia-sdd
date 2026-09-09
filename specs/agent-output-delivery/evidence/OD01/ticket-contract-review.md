# OD01 narrow ticket contract clarification — APPROVE

Independent architect approved this clarification on 2026-09-09 while the sole OD01 writer continued implementation. It changes no HTTP shape or bearer capability.

The sole unscoped authentication-bootstrap lookup is exact `BINARY(32)` SHA-256 of the presented opaque bearer. The persisted ticket row establishes the principal; request-provided tenant/client/run/source/binding values do not. All subsequent resource/business queries use persisted row-derived byte-exact scope and dynamic expiry, revocation, source, producer and binding authorization. Current-runtime checks must preserve the already-approved same-unrevoked-binding recovery rule; the original runtime is not a permanent identity fence, and capability freshness remains a dispatch gate rather than substitute authorization.

The non-unique `(tenant_id,client_id,binding_id,created_at)` index is an approved physical optimization. Ticket issuance serializes on the same exact binding lock, validates the current issuer, counts the window and inserts in one transaction. Schema validation must check index order/non-uniqueness on fresh and repeated upgrades.

Test boundaries: valid bearer resolves; wrong/one-bit token returns unauthorized; expiry/revocation fails; request scope variants cannot redirect the principal; ordinary resource IDs receive no global lookup exception; post-auth source/binding revocation fails; concurrent N+1 issuance commits at most N tickets, rollback consumes no quota, and invalid case variants cannot share another binding's count.
