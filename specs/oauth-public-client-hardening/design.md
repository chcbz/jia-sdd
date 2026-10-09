# OAuth public client hardening design

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

按原 SDD 中独立审查与 2026-08-24 发布记录归档；不扩大为所有账号安全/公共公测需求已完成。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：AR-20260906-08。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 本次设计边界补充

保留 sessionStorage 一次性配置绑定 state/PKCE、JWT-only GET /resource、401 fail-closed。源码 Owner 按任务/worktree/路径隔离，不再采用跨项目唯一 Writer。
<!-- END SDD delivery reconciliation -->

## User flow

1. An authenticated operation without a valid access token begins one authorization transaction.
2. The browser stores a 10-minute same-tab transaction containing random `state`, PKCE verifier, safe return path, client ID, redirect URI, and authorization-server identity.
3. The authorization callback scrubs its query, validates and consumes the matching transaction once, then handles either provider denial or one code-exchange attempt.
4. A valid token response is committed before `/user/my` loads identity; success replaces the callback route with the stored return path.
5. Failures render safe local messages with “重新登录” and “返回首页” actions.

## API and data contract

### `GET /resource`

- Authentication: exact stateless OAuth2 Resource Server JWT chain; a form-login session alone is insufficient.
- Request: no body.
- Success: HTTP 200 with the project response envelope and data fields:
  - `subject`: exact JWT `sub`, required nonblank string.
  - `clientId`: exact JWT `client_id`, required nonblank string.
  - `username`: exact optional string claim.
  - `jiacn`: exact optional string claim.
  - `scopes`: deterministic sorted copy of string scope values; empty when absent.
- Failure: missing, invalid, expired, tampered, or structurally malformed JWT returns HTTP 401.
- The response must not serialize the raw JWT, bearer token, authorities, arbitrary claims, email, phone, provider IDs, roles, or permissions.
- Compatibility: configured resource URI chains retain existing behavior; `/resource` receives its own higher-priority exact matcher.

### Browser transaction `cyf.oauth.pending.v1`

- `version`: `1`.
- `state`: 32 WebCrypto bytes encoded as 43-character unpadded base64url.
- `codeVerifier`: 64 WebCrypto bytes encoded as 86-character unpadded base64url.
- `returnTo`: validated same-origin app-relative pathname/query/hash; fallback `/`.
- `createdAt` / `expiresAt`: integer epoch milliseconds with an exact 10-minute lifetime.
- `clientId`, `redirectUri`, `authorizationServer`: must match current runtime configuration on consume.
- Storage: `sessionStorage`; one pending transaction per browser tab.

## Frontend behavior

- `state` is never interpreted as a route.
- A matching transaction is removed before provider-error handling or token exchange.
- Missing, duplicate, malformed, mismatched, expired, or replayed callbacks perform no exchange.
- Callback query data, code, state, verifier, token, and raw provider description are never logged or rendered.
- Token commit requires nonblank `access_token`, Bearer `token_type`, and finite positive `expires_in`; returned refresh tokens are ignored.
- Missing-token and 401 paths start at most one reauthentication and do not send/replay an unauthenticated request.

## Compatibility and rollout

- `/juyiting`, public landing, guest demo, `/user/my`, OAuth endpoint paths, and `api_token` remain compatible.
- No database migration is required.
- API and Web commits are independently reviewable and pinned together by the root integration commit.
- Rollback is a submodule revision rollback; no persisted server data changes are introduced.

## Decisions

- Refresh tokens remain out of scope until production-client grant, rotation, revocation, and replay behavior are proven.
- Identity claims remain distinct and byte-exact; no fallback or normalization maps one field to another.
- Independent read-only identity/security review is mandatory before integration acceptance.
