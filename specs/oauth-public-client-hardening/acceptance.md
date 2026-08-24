# OAuth public client hardening acceptance

## Acceptance criteria

- [x] State is unpredictable, short-lived, same-tab, configuration-bound, and consumed once.
- [x] Callback-controlled data cannot select an external or protocol-relative destination.
- [x] Missing/mismatched/expired/replayed state performs no token exchange.
- [x] PKCE verifier, authorization code, tokens, and raw provider errors are neither logged nor rendered.
- [x] Callback displays recoverable local error states and uses route replacement on success.
- [x] Malformed token responses are rejected without persisting an access token.
- [x] Missing-token and 401 paths initiate at most one reauthentication and issue no unauthenticated retry.
- [x] `/resource` rejects no-token and form-session-only requests with HTTP 401.
- [x] Valid user and machine JWTs return only allowlisted exact identity fields.
- [x] Malformed required/optional claims fail closed; arbitrary claims are absent.
- [x] Existing `/juyiting`, public landing/demo, and configured resource paths retain their contracts.

## Verification evidence

- API revision: `c4d8aebd77b122100e562576e40a158c26c1dff4` (tree `deb5e0236f9a89520ef2de77265aa14c6c7482b3`).
- Web revision: `0ac7ea756ad59c91c1110e3d635846a4c665ece6` (tree `018b1528dbca31d36e74522e5f910917bffb5c82`).
- Root integration revision: `fcf44b5996cfee38dd289e0b66c2f9b945f6cd12`.
- API verification:
  - `flock /tmp/cyf-gradle.lock ./gradlew :oauth:jia-oauth-resource:test --tests '*ResourceControllerTest' --tests '*ResourceSecurityIntegrationTest' --rerun-tasks` — 13 passing (7 controller, 6 production-shaped security).
  - `flock /tmp/cyf-gradle.lock ./gradlew :oauth:jia-oauth-resource:build -x test --rerun-tasks` — passed.
- Web verification:
  - Focused OAuth callback/transaction/HTTP suite — 36 passing.
  - Standalone OAuth transaction suite — 7 passing.
  - Targeted ESLint — passed.
  - `npm run build` — passed.
- Commit integrity: API/Web whitespace checks passed; both accepted commits are present at `origin/develop`.
- Independent review: final `sol_reviewer` verdict `ACCEPT`; P0 none, P1 none, P2 none, P3 none.
- Compatibility and migration: no database migration; `/`, `/demo`, `/juyiting`, `/user/my`, configured resource paths, and `api_token` storage contract preserved.
- Rollback: restore the previous root `api`/`web` gitlinks, rebuild the API JAR/static bundle, and redeploy; no persisted server-data rollback is required.
- Residual risk: no live provider browser E2E; JWT verification tests use a mock decoder rather than a live issuer/JWK; localStorage access-token exposure to same-origin XSS remains outside this packet.
- Release evidence (August 24, 2026 CST):
  - API deployed from `c4d8aebd77b122100e562576e40a158c26c1dff4`; deployed JAR SHA-256 `31e25956695ffa9df5de3c7488c882e34e04f91d22fc088934fa626fbe8549c1` matches the built artifact.
  - Web deployed from clean detached worktree at `0ac7ea756ad59c91c1110e3d635846a4c665ece6`; deployed `index.html` SHA-256 `e53723e3ca843ea5cf8297c426c74be051373ef659b6bade77be7c6ea7c9d0f0` matches the built artifact.
  - API process started successfully on port `10018`; local `/actuator` returned HTTP 200.
  - Exact GET `/resource` returned HTTP 401 without a token both locally and through `https://api.chaoyoufan.cn/resource`.
  - Added an exact production Nginx `/resource` proxy allowlist entry; `nginx -t` passed and reload succeeded. Rollback backup: `/home/isp/apps/nginx/conf/vhost/api.chaoyoufan.cn.conf.bak_oauth_resource_20260824_140439`.
  - `https://kit.chaoyoufan.cn/`, `/demo`, `/juyiting`, and `/oauth2/callback` returned HTTP 200; deployed manifest and service worker were present.
  - Live provider login/callback remains an explicit residual manual E2E item because no production user authorization was exercised during this release.
- Result: released.
