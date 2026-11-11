# Account security foundation and global session revocation tasks

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

Cookie 修复包已在运行台账行政收口，但只记录 manifest 校验，缺 exact Git 绑定与 credentialed 生产验收；不能把整个账号安全需求标为完成。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：未归档。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 当前执行动作

补齐 auth_epoch/撤销、生产 OAuth client 与迁移的逐项验收及实际版本映射。

以下原始清单为合同/历史记录；当前完成状态采用 delivery-status 的任务映射，不能据旧未勾选项重新派工。
<!-- END SDD delivery reconciliation -->

## API (`api/`)

- [ ] 新增 ASCII/`ascii_bin` `account_state` 与 `auth_epoch` 实体映射、枚举/安全快照、按 uid 与 byte-exact jiacn 的 DAO 查询及 CAS，并提供 additive/repeat-safe migration、preflight 和 rollback 材料。
- [ ] 用窄 `user-api` 接口实现账户状态读取和 `revoke-all` CAS，保持 Gradle layering 无环。
- [ ] 扩展 `CustomUserDetails(userId, jiacn, loginAuthEpoch)`，更新密码/短信/第三方登录构造点，拒绝非 ACTIVE 或缺稳定身份账户。
- [ ] JWT 签发显式 `token_kind`、`uid`、`auth_epoch`，严格兼容 legacy machine/user token，并阻断 stale authorization-code/refresh/HttpSession principal。
- [ ] 为 `/resource` 和 `oauth.resource.uris` 安装组合 JWT validator，严格处理旧/非法 epoch 和数据库失败。
- [ ] 在 `oauth-resource` 实现 Bearer-user-only `POST /user/me/sessions/revoke-all`，主体只来自 `JwtAuthenticationToken`，成功 204、CAS 冲突 409。
- [ ] API Key 认证增加 ACTIVE 用户 gate，验证 revoke-all 不直接禁用 API Key。
- [ ] 修复 `EsContextHolder` 生命周期、JWT/API Key 覆盖 CTX、CTX Cookie 属性、prod/grey CORS 键和错误响应 wildcard header。
- [ ] 增加 focused tests：登录/签发、validator、endpoint ACL/CAS/concurrency、API Key、CTX/CORS、migration。

## Web (`web/`)

- [ ] 在 API/global store 增加精确身份清理和 `revokeAllSessions()`，不得清空无关 localStorage。
- [ ] 个人中心增加“退出当前设备”“退出所有设备”、影响说明、确认、忙碌、错误与无障碍状态。
- [ ] 成功/已失效后 `router.replace('/')`；网络/5xx 保留身份并允许重试。
- [ ] 增加 store 与 `UserProfile` 定向测试，运行 ESLint 和 production build。

## Integration and verification

- [ ] 独立 `sol_reviewer`/`adversarial_reviewer` 审查身份来源、依赖环、JWT validator、refresh、CAS race、migration 和数据泄漏。
- [ ] 所有 Gradle 命令使用 `flock /tmp/cyf-gradle.lock`；记录 tree SHA、test selector 与 DB fixture digest。
- [ ] 在 production-shaped MySQL 验证 fresh/upgrade/repeat、rollback prerequisite、Long.MAX、未知 state 和双并发 CAS。
- [ ] 对生产 OAuth client 原行做权限 600 字节级备份，生成精确 rollback SQL，并完成目标字段迁移。
- [ ] 验证 PKCE authorization-code 登录、10 分钟 token、5 分钟 code、`client_credentials`/refresh/secret/Postman callback 拒绝。
- [ ] API/Web 分别提交并推送；执行 `./sddw pin account-security-foundation` 与 `./sddw verify account-security-foundation`。
- [ ] 精确提交根 SDD 与 api/web gitlinks，不包含并行 control-plane 或 E13 改动。
- [ ] 按 schema → API → Web → OAuth client/smoke 顺序部署，记录备份、部署和线上 revoke 证据。
- [ ] 创建下一阶段 `account-self-service-closure` SDD，不复用危险的通用 delete endpoint。
