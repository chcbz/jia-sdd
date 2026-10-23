# Account security foundation and global session revocation acceptance

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

Cookie 修复包已在运行台账行政收口，但只记录 manifest 校验，缺 exact Git 绑定与 credentialed 生产验收；不能把整个账号安全需求标为完成。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：未归档。原文合同及历史验收材料保留，不把发布例外标成 PASS。

源码验收、生产发布、真实用户/设备验收分开。已有测试仅复用记录；本次为文档核对，无新增业务测试。未证明项保留未验证。
<!-- END SDD delivery reconciliation -->

## Acceptance criteria

### Account and token gate

- [ ] fresh/upgrade migration 后 `account_state` 列为 ASCII/`ascii_bin`，每个现有用户精确为 `ACTIVE/0`；repeat 不改已有值。
- [ ] ACTIVE 用户新 access token 含 exact `token_kind=user`、canonical `uid`、byte-exact `jiacn` 和数值 `auth_epoch`；非 ACTIVE/缺身份用户不能登录或签发 token。
- [ ] 有效用户 JWT 仅在 uid/jiacn 对应同一 DB 行、state ACTIVE 且 epoch 相等时进入 Controller。
- [ ] 旧 token 缺 epoch 仅在 DB ACTIVE/0 时有效；首次 revoke 后永远失效。
- [ ] 非法 uid/epoch/token_kind 或空白 jiacn fail closed；显式 machine token及严格结构的 legacy machine token保持兼容，普通缺 jiacn token失败。
- [ ] stale authorization-code/refresh/HttpSession principal 不能自动升级到当前 epoch；生产 Web client 不支持 refresh grant。

### Global revocation and API Key

- [ ] `POST /user/me/sessions/revoke-all` 不接受客户端指定用户或 epoch，只使用 Bearer JWT 主体。
- [ ] form session、CTX、API Key、machine token、匿名、错误方法均不能执行撤销。
- [ ] 单次成功只把 epoch 加 1；两个并发相同 token 最多一次加 1，失败请求不重试到新 epoch。
- [ ] 成功提交后原 token 对 `/resource`、`/user/my` 和另一受保护 URI 均为 401。
- [ ] 账户非 ACTIVE 时已有 API Key 为 401；账户 ACTIVE 时 revoke-all 不直接禁用 API Key。
- [ ] Long.MAX epoch 不回绕；`active`/`Active`/未知 state 的 CAS 均零写入。

### Context and browser

- [ ] 同一 servlet 线程的连续请求不会继承前一请求 EsContext。
- [ ] JWT claims 覆盖/清空旧 CTX 身份，旧 Cookie 不能冒充 Bearer 主体。
- [ ] CTX Cookie 在生产为 HttpOnly/Secure/SameSite=Lax/Path=/。
- [ ] prod/grey CORS 仅接受 `https://kit.chaoyoufan.cn`，带 credentials 时无 wildcard origin。
- [ ] “退出当前设备”仅清理当前浏览器身份并回首页，不调用 revoke endpoint。
- [ ] “退出所有设备”有确认和影响说明；204/401/SESSION_EPOCH_CONFLICT 清理身份，网络/5xx/耗尽错误保留身份并显示可重试错误。
- [ ] 身份清理不删除主题、游客体验或其他无关 localStorage。

### Production OAuth client and release

- [ ] `jiafewnnv58ec2379c` 仅 `none + authorization_code + openid + PKCE`，生产 callback 精确，localhost/Postman/secret/client_credentials/refresh 均不可用。
- [ ] access token TTL 为 `PT10M`，authorization code TTL 为 `PT5M`。
- [ ] 迁移前备份权限 600，包含原 DDL/统计/client 行和可执行的精确 rollback SQL。
- [ ] 独立安全 Review 为 ACCEPT，focused API/Web tests、Gradle layering、lint/build 和线上 smoke 全部通过。
- [ ] API/Web commit 已推送，root integration pin 可复现，部署证据已记录。

## Verification evidence

- Architect verdict: ACCEPTABLE on 2026-08-24 after uid/token_kind/legacy/rollback and ascii_bin state revisions
- Independent security review: pending
- API revision: pending
- Web revision: pending
- Root integration revision: pending
- Migration backup/checksum: pending
- Commands/tests: pending
- Production deployment/smoke: pending
- Result: pending
