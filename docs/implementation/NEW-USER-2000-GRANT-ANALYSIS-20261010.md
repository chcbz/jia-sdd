# 现有用户补款结果与新用户默认 2000 分析

核对日期：2026-10-10（北京时间）。Owner：当前主控。范围：本次授权的生产数据库增发 + 后续方案分析；**不实现、不发布长期迎新规则，不改用户身份数据**。

源码基线：API `36d9e5452ab8beb64b97e5570da6ede10ec38797`；Web `17ecf1c0b581cab1456acff4db097a6a4d335e3d`。这是本地核对基线，不声称本轮已检查远端最新提交。本次没有应用构建、部署或重启。

## 1. 已执行的补款

- 用户明确授权“直接在数据库给所有用户补2000资金”。按每位用户**额外 +2000 SILVER**执行，不覆盖原余额，不改 `user_info.point`。
- 快照有 310 条 `user_info`，均 tenant `0`，client 为 NULL 或 CYF `jiafewnnv58ec2379c`。NULL 是共享登录用户，不能仅按 user_info.client_id 非空筛选，否则会漏掉 chcbz 等用户。
- 现行钱包按 JWT `sub` + 当前 client 记账。第三方登录认证名优先 username，其次 jiacn（OAuth OauthController.java:476–485）。43 位有 username，266 位无 username 但有 jiacn；本次按这一现行映射给 309 位建/补 AVAILABLE 钱包，不给其它 OAuth client、系统收入或托管账户赠款。
- **1 条未发：user_info.id=94，username/jiacn 均缺失。** 钱包 requireSubject 要求有效 jiacn；不为凑齐人数擅自修身份、不把 openid 猜成可用钱包主体。这不是“全体310人已完成”。
- 批次 `ops-all-users-plus2000-20261010`，单人 `2000000000 micro`，总计 **618000 SILVER**。
- 2026-10-10 **08:21:10.528** 数据库提交完成：309 笔 `ISSUE_SILVER`、618 条分录；用户 +2000，对应 SYSTEM/SILVER_ISSUANCE 等额负分录。沿用钱包ID算法、POSTING→POSTED、账户版本递增及确定性幂等身份。
- 单事务执行；固定用户清单并锁定身份，按 SYSTEM→USER 排序锁账户，写前/提交前均做余额与账本核对。提交前校验所有钱包逐一恰好 +2000/version+1，发行账户 -618000/version+309，租金及托管账户余额/版本未被本批改变。
- 提交后独立连接复核：309 笔均 POSTED，618 条分录合计0，全库账本/余额差异0、交易摘要/分录差异0。
- 正常浏览器登录 chcbz 后，线上 GET `/economy/wallet` HTTP200：availableMicro=`2000000000`、heldMicro=`0`、version=`9`；GET ledger HTTP200、5条流水。钱包版本含托管修订，数据库 AVAILABLE 账户 version=`5`，二者不是同一指标。
- 当前生产迎新配置**未改**：enabled=true、amount-micro=1000000000、campaign-ref=hosting-welcome-v1。其他尚未领取的旧用户仍可能按旧规则另领1000；本次补款与该活动独立，不冒充已完成长期规则切换。

证据（目录0700）：`/var/tmp/cyf-all-users-plus2000-20261010-GtEkIc/`

- `users-before.jsonl`、`accounts-before.jsonl`：最小身份/余额快照，无密码/token。
- `ledger-before.sql`、`ledger-before.sha256`：写前复式账本备份。
- `manifest.json`：固定名单、唯一交易/幂等键、SQL SHA及例外。
- `prepare.py`、`grant.sql`：本次操作生成器/实际SQL；重复执行遇已有批次会失败回滚，不重复入账。
- `execution.log`、`execution.err`、`readback.jsonl`：锁内前值、全部断言及提交回读。
- `wallet-online.json`、`ledger-online.json`：生产接口回读；owned Chromium已关闭。

恢复边界：已POSTED流水不可删改。备份不是允许覆盖现网后续交易的恢复指令；若需撤销，应另核对是否已消费，再用可审计冲正事务处理，不能直接恢复全表或修改旧分录。

## 2. 为什么不能只改一个金额

1. `EconomyWalletService.java:109–149`：现行幂等键绑定 scope/actor/campaign，但 request_hash 还含 amount。**同 campaign 从1000改2000，老回执会产生幂等冲突**。
2. 只换 campaign：老用户也能按新活动再领，不等于“仅后续新用户”。
3. `web/src/composables/juyiting/useHostingRent.js:82–92,194–199`：仅 INITIAL 报价且余额不足才触发领取。改金额不会变成“新用户默认到账”。
4. `EconomyWalletService.wallet:64–79` 只查询，`EconomyLedgerMapper.selectUserWalletSnapshot` 将未建钱包视为0。不能把 SQL `balance_micro DEFAULT 0` 改为2000：没有对应发行分录，而且会影响非用户账户。
5. `EconomyWalletController.java:156–173` 使用 JWT sub；密码/短信/微信别名登录与第三方登录的认证名生成规则不完全相同。**单靠 actor/campaign 幂等不足以保证同一自然用户只领一次**。本轮未实测全部用户的所有登录方式，不能把批量入账说成全部身份通道均验收通过。

## 3. 推荐的最小长期方案（待实现）

### 产品语义

建议定义为：**规则启用后创建的新 CYF 用户，首次认证进入聚义厅时自动获得2000；一生一次，不按活动/重新入伙/余额不足补发。** 首次进入时发放能获得真实 client 与已认证身份，也能覆盖第三方登录首次落库。若要求“完成LDAP注册、尚未登录也到账”，则需额外贯通LDAP→user_info落库和明确目标client，不是单改注册Controller即可。

复用现有 POST `/economy/onboarding-grant` 和 treasury ISSUE_SILVER；不新增充值页面、充值接口、第二套悬赏体系或发钱调度框架。GET钱包/流水保持只读。

### 修改位置

| 位置（相对 /home/isp/wsps/cyf） | 改动 |
|---|---|
| `api/economy/.../EconomyOnboardingGrantProperties.java:9–19` | amount-micro设为2000000000；保持金额校验。生产实际配置在 `/home/isp/hosts/cyf/api/application.properties:35–37`，不能只改源码prod默认就声称线上生效。 |
| `api/economy/.../EconomyWalletController.java:90–98,156–173` | 从可信JWT uid并经持久化用户核对取得稳定user_id；调用“一次性新用户初始化”。不接受前端自报用户、金额或campaign。 |
| `api/economy/.../EconomyWalletService.java:109–149` | 先检查用户级资格/已有回执，再用当前金额发放；同一数据库事务中完成资格占位、复式记账、回执绑定。已发则返回原金额/原交易，不用新配置重算旧hash。 |
| `api/economy/jia-economy-mapper` | 增加下述最小领取记录及带scope/用户唯一锁的mapper；复用现有账本，不改单纯余额默认值。 |
| 聚义厅认证完成后的现有初始化调用处（实施时定向确定文件） | 自动调用一次既有POST，成功后GET钱包；不要直到租金不足才发。失败可用同身份重试，不展示虚假的本地2000。 |
| `web/src/composables/juyiting/useHostingRent.js:82–92,194–199` | 去掉把“报价余额不足”作为发放资格的旧逻辑；余额不足只提示缺口，不循环领钱。处理下述不符合资格的明确结果，不把无发放当网络故障。 |

### 最小持久化领取记录建议

建议表 `economy_onboarding_grant_claim`，不是另一套账本：

| 字段 | 类型/约束 | 用途 |
|---|---|---|
| tenant_id | VARCHAR(50) NOT NULL | scope |
| client_id | VARCHAR(50) NOT NULL | scope |
| user_id | BIGINT NOT NULL | 可信uid对应user_info.id |
| status | VARCHAR(16) NOT NULL，POSTING/POSTED/EXCLUDED | 事务内占位/已发/切换前旧用户 |
| actor_id | VARCHAR(100) NULL | 实际入账主体快照；旧用户不发时可空 |
| transaction_id | VARCHAR(100) NULL | POSTED必须有实际交易，不虚构流水 |
| amount_micro | BIGINT NOT NULL DEFAULT 0 | POSTED实际发放数；EXCLUDED为0 |
| campaign_ref | VARCHAR(100) NULL | 审计标签，不参与“终生一次”唯一键 |
| create_time / update_time | BIGINT NOT NULL | 时间戳 |

主键 `(tenant_id,client_id,user_id)`；同scope transaction_id非空唯一；POSTED要求金额>0/交易非空，EXCLUDED要求交易空且金额0。POSTING只能存在于未提交事务中，异常整个事务回滚，不增建异步框架。

- 上线迁移时固定旧用户集合/明确切换点：本次309位补款者回填为POSTED并关联本批真实交易；其余切换前用户（包括异常94及切换前新增用户）标EXCLUDED，避免“没有钱包就是新用户”。金额记录按实际历史回执，不能强写2000覆盖历史。
- 按主键唯一插入/行锁并发控制；已POSTED原样回读，EXCLUDED返回明确不符合新用户资格的业务结果；空记录且属于启用后新用户才能发2000。资格与账本共用数据库事务，失败可安全重试。
- 历史310人的身份和补款清单已固定；未来迁移必须重新读取上线时的用户集合，**不可照抄本次人数/最大ID当未来上线基线**。切换期间的用户创建与资格截点须有一致定义，不能只在应用里比较可能为NULL的create_time。
- 稳定user_id解决领取防重，但不自动修复钱包按不同sub分裂的问题。实施前统一核对Wallet、托管租金及悬赏的付款主体解析，至少保证支持的登录方式落到同一既有canonical钱包；不能仅改wallet接口而让扣款仍用另一身份。确需主体迁移时单独列出受影响数据，不把本次补款当迁移授权。

### 最低验收

- 新用户首次进入到账2000且有平衡分录；普通/第三方新用户入口均覆盖。
- 刷新、重新登录、并发请求、换登录方式、除名重新入伙不再赠款。
- 老用户（有/无历史迎新回执、有/无钱包、本次已补款者）不重复领。
- 发放中途异常全部回滚；响应丢失重试返回原交易；切换后改配置不使原回执冲突。
- 原有租金/悬赏可用余额、付款与流水读取对应同一主体。
- 后端定向测试/分层检查走项目本地受控入口，前端正式测试发布走Flow4403172；本轮仅分析，均尚未执行。

## 4. 下一步

1. 本次补款剩余1条需先确定真实有效身份；不猜、不补造登录身份。
2. 长期规则如采用上面“首次认证进入即到账”语义，再安排实现；**不是改配置已完成**。
3. chcbz测试资金阻塞已解除；此前公孙胜重入伙→免费重整两场景仍未完成，本轮没有绑定、确认租金或REPROVISION请求，不把钱到账当作两场景通过。


## 2026-10-10 方案定稿入口

公孙胜原单/免费重整已在独立handoff验收；新用户资金方案定稿见 `/home/isp/wsps/cyf/docs/implementation/NEW-USER-2000-GRANT-DESIGN-20261010.md`。以定稿中的旧用户统一EXCLUDED、稳定uid防重、资金主体一致及正式资格截点为准；本分析保留历史事实，不代表长期规则已实施。
