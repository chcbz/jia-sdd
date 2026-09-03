# Account self-service closure

## Problem

`account-security-foundation` provides account-state enforcement and global session revocation, but it intentionally does not implement user-requested account closure, retention, restoration, PII erasure, API-key revocation, or related-data cleanup. The existing generic administrator `DELETE /user/delete?id=...` endpoint is not a safe self-service contract.

## Goal

Design and implement a dedicated, authenticated self-service account-closure lifecycle with explicit confirmation, authorization, auditability, retention/erasure policy, all-credential revocation, transactional boundaries, idempotency, recovery rules and production rollback.

## Non-goals

- Do not expose or wrap the generic delete-by-id endpoint for end users.
- Do not hard-delete data before legal, product and dependency-retention rules are frozen.
- Do not weaken `account-security-foundation` token, epoch, API-key or account-state gates.

## Scope

- API/Web contracts for request, confirm, status, cancel/recover when allowed, and finalization.
- Account/API-key/session/authorization invalidation semantics.
- Dependency inventory across SQL, LDAP, Elasticsearch, files, Agent, Chat and Task data.
- PII anonymization/deletion, legal hold, audit evidence and operator runbook.
- Independent P0 identity/ACL/transaction/migration review and production verification.
