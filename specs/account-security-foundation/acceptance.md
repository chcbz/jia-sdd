# Account security foundation and global session revocation acceptance

## Acceptance criteria

### Account and token gate

- [x] fresh/upgrade migration 后 `account_state` 列为 ASCII/`ascii_bin`，每个现有用户精确为 `ACTIVE/0`；repeat 不改已有值。
- [x] ACTIVE 用户新 access token 含 exact `token_kind=user`、canonical `uid`、byte-exact `jiacn` 和数值 `auth_epoch`；非 ACTIVE/缺身份用户不能登录或签发 token。
- [x] 有效用户 JWT 仅在 uid/jiacn 对应同一 DB 行、state ACTIVE 且 epoch 相等时进入 Controller。
- [x] 旧 token 缺 epoch 仅在 DB ACTIVE/0 时有效；首次 revoke 后永远失效。
- [x] 非法 uid/epoch/token_kind 或空白 jiacn fail closed；显式 machine token及严格结构的 legacy machine token保持兼容，普通缺 jiacn token失败。
- [x] stale authorization-code/refresh/HttpSession principal 不能自动升级到当前 epoch；生产 Web client 迁移材料禁用 refresh grant。

### Global revocation and API Key

- [x] `POST /user/me/sessions/revoke-all` 不接受客户端指定用户或 epoch，只使用 Bearer JWT 主体。
- [x] form session、CTX、API Key、machine token、匿名、错误方法均不能执行撤销。
- [x] 单次成功只把 epoch 加 1；两个并发相同 token 最多一次加 1，失败请求不重试到新 epoch。
- [x] 成功提交后原 token 对 `/resource`、`/user/my` 和另一受保护 URI 均为 401。
- [x] 账户非 ACTIVE 时已有 API Key 为 401；账户 ACTIVE 时 revoke-all 不直接禁用 API Key。
- [x] Long.MAX epoch 不回绕；`active`/`Active`/未知 state 的 CAS 均零写入。

### Context and browser

- [x] 同一 servlet 线程的连续请求不会继承前一请求 EsContext。
- [x] JWT claims 覆盖/清空旧 CTX 身份，旧 Cookie 不能冒充 Bearer 主体。
- [x] CTX Cookie 在生产为 HttpOnly/Secure/SameSite=Lax/Path=/。
- [x] prod/grey CORS 仅接受 `https://kit.chaoyoufan.cn`，带 credentials 时无 wildcard origin。
- [x] “退出当前设备”仅清理当前浏览器身份并回首页，不调用 revoke endpoint。
- [x] “退出所有设备”有确认和影响说明；204/401/SESSION_EPOCH_CONFLICT 清理身份，网络/5xx/耗尽错误保留身份并显示可重试错误。
- [x] 身份清理不删除主题、游客体验或其他无关 localStorage；pending OAuth、HTTP、SSE、消息、Chat 与聚义厅异步写回均受 generation/disposal gate 约束。

### Production OAuth client and release

- [ ] 生产 `jiafewnnv58ec2379c` 已实际收敛为 `none + authorization_code + openid + PKCE`，生产 callback 精确，localhost/Postman/secret/client_credentials/refresh 均不可用。
- [ ] 生产 access token TTL 已实际验证为 `PT10M`，authorization code TTL 已实际验证为 `PT5M`。
- [ ] 生产迁移前备份权限 600，包含原 DDL/统计/client 行和可执行的精确 rollback SQL。
- [ ] 独立安全 Review、focused API/Web tests、Gradle layering、定向 lint/build 和线上 smoke 全部通过。（除线上 smoke 外均已通过；全量 Web lint 的 118 个错误为既有基线。）
- [ ] API/Web commit 已推送，root integration pin 可复现，部署证据已记录。（API/Web 已推送；root pin 与部署待完成。）

## Verification evidence

- Architect verdict: `ACCEPTABLE` on 2026-08-24 after uid/token_kind/legacy/rollback and `ascii_bin` state revisions.
- Independent security review: API final `ACCEPT` at `261ee9eb61769c6fd79b1bb1368dde799e1563c8`; Web final `ACCEPT` at `7bc80de75f83d4cb7ca288380c3ed9eab1bc111a`.
- API revision/tree: commit `261ee9eb61769c6fd79b1bb1368dde799e1563c8`, tree `399b9f048f073cc8d47f97d8f71b8e2cc7636129`, pushed to `origin/codex/account-security-foundation`.
- Web revision/tree: commit `7bc80de75f83d4cb7ca288380c3ed9eab1bc111a`, tree `182572ba74399f4feb714706b1310785ed83668e`, pushed to `origin/codex/account-security-foundation-web`.
- API focused Gradle evidence: 30 focused tests across common context/CORS, OAuth login/API-key/resource/revoke, profile contract, user security boundary/service and SQL contract; 30 passed, 0 failed. Every Gradle invocation held `/tmp/cyf-gradle.lock`.
- Web evidence: 102 focused Mocha tests passed; feature-file ESLint passed; `npm run build` passed; `git diff --check` passed. Full `npm run lint` remains red on 118 pre-existing errors outside this feature gate.
- MySQL evidence: isolated MySQL `8.0.46`, networking disabled, production socket never used. User migration/CAS/OAuth body/transaction/concurrency artifact `/tmp/asf-evidence-final-20260825013500`, fixture digest `a99594f55f733ad074807d80027f9270388bcccfa5038558c1d1910451e4f879`; its original preflight harness failures are superseded only for that changed scope by the clean-tree fixed-preflight artifact below.
- Fixed preflight evidence: `/tmp/asf-evidence-preflight-fixed-20260824T180038Z-validated`, API tree `399b9f048f073cc8d47f97d8f71b8e2cc7636129`, fixture digest `39c022e4de6cd37530271d88d41efd4635ce06262c1687554a8f0cd890e19e56`, `ONLY_FULL_GROUP_BY` enabled, 8/8 passed, byte-exact rollback restoration passed, isolated mysqld stopped. Artifact directory names are host-generated labels and are not treated as release timestamps.
- Root integration: immutable commit `c9cf4d800b20c0bd60a12c532300dcecfe1431cf` (tree `6174ad0b070d278fadfceb62d297e8ca5d365199`) pins `api=261ee9eb61769c6fd79b1bb1368dde799e1563c8`, `web=7bc80de75f83d4cb7ca288380c3ed9eab1bc111a`, root base `752b4dfceea2b6d3061d921a426dddba5410b90c`; `./sddw verify` passed.
- Production migration backup/checksum: pending; fixture evidence is not a production backup.
- Production deployment/smoke: pending.
- Result: accepted integration baseline; production release remains pending.
