# Account security foundation and global session revocation tasks

## API (`api/`)

- [x] 新增 ASCII/`ascii_bin` `account_state` 与 `auth_epoch` 实体映射、枚举/安全快照、按 uid 与 byte-exact jiacn 的 DAO 查询及 CAS，并提供 additive/repeat-safe migration、preflight 和 rollback 材料。
- [x] 用窄 `user-api` 接口实现账户状态读取和 `revoke-all` CAS，保持 Gradle layering 无环。
- [x] 扩展 `CustomUserDetails(userId, jiacn, loginAuthEpoch)`，更新密码/短信/第三方登录构造点，拒绝非 ACTIVE 或缺稳定身份账户。
- [x] JWT 签发显式 `token_kind`、`uid`、`auth_epoch`，严格兼容 legacy machine/user token，并阻断 stale authorization-code/refresh/HttpSession principal。
- [x] 为 `/resource` 和 `oauth.resource.uris` 安装组合 JWT validator，严格处理旧/非法 epoch 和数据库失败。
- [x] 在 `oauth-resource` 实现 Bearer-user-only `POST /user/me/sessions/revoke-all`，主体只来自 `JwtAuthenticationToken`，成功 204、CAS 冲突 409。
- [x] API Key 认证增加 ACTIVE 用户 gate，验证 revoke-all 不直接禁用 API Key。
- [x] 修复 `EsContextHolder` 生命周期、JWT/API Key 覆盖 CTX、CTX Cookie 属性、prod/grey CORS 键和错误响应 wildcard header。
- [x] 增加 focused tests：登录/签发、validator、endpoint ACL/CAS/concurrency、API Key、CTX/CORS、migration。

## Web (`web/`)

- [x] 在 API/global store 增加精确身份清理和 `revokeAllSessions()`，不得清空无关 localStorage。
- [x] 个人中心增加“退出当前设备”“退出所有设备”、影响说明、确认、忙碌、错误与无障碍状态。
- [x] 成功/已失效后 `router.replace('/')`；网络/5xx 保留身份并允许重试。
- [x] 增加 store、HTTP/SSE、Chat/聚义厅生命周期和 `UserProfile` 定向测试，运行定向 ESLint 和 production build。

## Integration and verification

- [x] 独立 `sol_reviewer`/`adversarial_reviewer` 审查身份来源、依赖环、JWT validator、refresh、CAS race、migration、异步身份写回和数据泄漏；API/Web 最终 verdict 均为 `ACCEPT`。
- [x] 所有 Gradle 命令使用 `flock /tmp/cyf-gradle.lock`；记录 API tree SHA、test selector 与 DB fixture digest。
- [x] 在隔离、禁网、production-shaped MySQL 8.0.46 验证 fresh/upgrade/repeat、rollback prerequisite、Long.MAX、未知 state、双并发 CAS、OAuth 原子迁移/重跑/失败回滚和 MySQL 8 `ONLY_FULL_GROUP_BY` preflight。
- [ ] 对生产 OAuth client 原行做权限 600 字节级备份，生成精确 rollback SQL，并完成目标字段迁移。
- [ ] 在线验证 PKCE authorization-code 登录、10 分钟 token、5 分钟 code、`client_credentials`/refresh/secret/Postman/localhost callback 拒绝。
- [x] API/Web 分别提交并推送；执行 `./sddw pin account-security-foundation` 与 `./sddw verify account-security-foundation`。
- [x] 精确提交根 SDD 与 api/web gitlinks，不包含并行 control-plane、E13 或 `.bak` 改动；不可变集成提交为 `c9cf4d800b20c0bd60a12c532300dcecfe1431cf`。
- [ ] 按备份 → production preflight → user schema → API → Web → OAuth client → smoke 顺序部署，记录备份、部署和线上 revoke 证据。
- [x] 创建下一阶段 `account-self-service-closure` SDD，不复用危险的通用 delete endpoint。
