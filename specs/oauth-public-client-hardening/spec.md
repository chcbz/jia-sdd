# OAuth public client hardening

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

- One source Writer operates across both submodules; commits remain independent.
- All Gradle commands hold `/tmp/cyf-gradle.lock`.
- Existing unrelated dirty changes in `api/`, `web/`, and root must not be staged or reverted.
- Production refresh-token behavior is unverified and remains disabled.
- Existing localStorage access-token exposure to same-origin XSS is a residual risk outside this packet.
