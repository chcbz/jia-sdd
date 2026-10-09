# OAuth public client hardening

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

按原 SDD 中独立审查与 2026-08-24 发布记录归档；不扩大为所有账号安全/公共公测需求已完成。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：AR-20260906-08。原文合同及历史验收材料保留，不把发布例外标成 PASS。
<!-- END SDD delivery reconciliation -->

## Problem

The browser OAuth2 authorization-code flow uses the callback `state` value as a navigation path without validating a locally bound transaction. PKCE verifier material is stored in localStorage and logged, callback failures silently return home, authenticated request retries can continue without a token, and the OAuth resource module exposes `GET /resource` with a null body and no exact JWT-only security boundary.

## Goals

- Bind every browser authorization callback to one unpredictable, short-lived, same-tab transaction.
- Keep post-login navigation separate from provider-controlled callback parameters.
- Consume PKCE material once, remove secret logging, and fail closed on malformed token responses.
- Provide a recoverable callback status/error page without rendering raw provider errors.
- Prevent missing-token and 401 paths from issuing or replaying unauthenticated requests.
- Make `GET /resource` a stateless Bearer-JWT identity projection with an allowlisted response.

## Non-goals

- Refresh-token issuance, storage, rotation, revocation, or logout.
- Account deletion, provider unlinking, or tenant deletion.
- General redesign of every OAuth resource matcher or user profile endpoint.
- Migration away from the existing `api_token` access-token storage key.

## Scope

- API: `api/oauth/jia-oauth-resource` controller, identity DTO, exact security chain, and focused tests.
- Web: OAuth transaction utility, API store, callback page/route, authenticated HTTP retry behavior, and focused tests.

## Constraints and risks

- One implementation Owner per task; independent tasks may write concurrently in separate worktrees with non-overlapping owned paths. API/Web commits remain independent.
- All Gradle commands hold `/tmp/cyf-gradle.lock`.
- Existing unrelated dirty changes in `api/`, `web/`, and root must not be staged or reverted.
- Production refresh-token behavior is unverified and remains disabled.
- Existing localStorage access-token exposure to same-origin XSS is a residual risk outside this packet.
