# OAuth public client hardening tasks

## API (`api/`)

- [x] Add an allowlisted resource identity DTO.
- [x] Replace the null `/resource` response with exact JWT claim projection.
- [x] Add a dedicated stateless JWT-only `/resource` security chain.
- [x] Preserve existing configurable resource URI behavior.
- [x] Add focused controller/security tests.
- [x] Commit and record API revision.

## Web (`web/`)

- [x] Add short-lived one-time OAuth transaction utility in sessionStorage.
- [x] Generate unbiased high-entropy state/verifier and PKCE S256 challenge.
- [x] Validate safe return paths and callback parameter shape.
- [x] Replace inline callback with processing/error UI.
- [x] Validate token responses and remove sensitive logging/offline refresh request.
- [x] Make missing-token/401 reauthentication single-flight without unauthenticated replay.
- [x] Add focused transaction/callback/HTTP tests and preserve public-entry behavior.
- [x] Commit and record Web revision.

## Integration and verification

- [x] Run focused locked Gradle tests/build.
- [x] Run focused frontend tests, lint, and production build.
- [x] Obtain independent read-only security review.
- [x] Push accepted API and Web commits.
- [x] Pin and verify submodule revisions with `./sddw`.
- [x] Record implementation, verification, compatibility, and rollback evidence.
- [x] Record production deployment and online smoke evidence.
