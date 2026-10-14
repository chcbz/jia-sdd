# OAuth public client hardening tasks

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

按原 SDD 中独立审查与 2026-08-24 发布记录归档；不扩大为所有账号安全/公共公测需求已完成。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：AR-20260906-08。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 当前执行动作

后续回归按独立缺陷单追踪，保留原 SHA 与部署证据。

以下原始清单为合同/历史记录；当前完成状态采用 delivery-status 的任务映射，不能据旧未勾选项重新派工。
<!-- END SDD delivery reconciliation -->

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
