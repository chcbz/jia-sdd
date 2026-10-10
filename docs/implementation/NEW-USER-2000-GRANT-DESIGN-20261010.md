# 新用户自动赠送2000积分：最小闭环方案

修订日期：2026-10-10。Owner：主控（方案）；开发未派发。状态：**范围收敛后的待实施方案，未改业务代码、未迁移、未发布**。本版替代前版把完整多区域/跨客户端钱包改造并入赠款的工作范围；历史方案保留在Git，不并行实施。

## 1. 本次只完成什么

沿用前文资金语义：“2000积分”指聚义厅现有可支付租金/悬赏的钱包资金，即 **2000 SILVER = 2,000,000,000 micro**，不另改`user_info.point`，不增加另一种积分或兑换系统。

1. 新用户完成认证，首次进入聚义厅或钱包，自动获得2000可用资金，无需点击领取、报价或先付租金。不是LDAP注册即发钱，也不是余额补齐至2000。
2. 新用户仍定义为本次启用截点后首次在CYF落库的`user_info`用户；截点前已有用户不再获赠，不以无钱包、余额0或第一次进入页面判断。旧309位补款及异常身份94不重做。
3. `tenant_id`代表业务区域。领取按`(tenant_id,user_id)`防重，client不增加领取次数。本次仅发布到当前已有、明确配置且已完成资格基线的业务区域/接入客户端；具体tenant/client值不写入Java业务常量。
4. **暂不承诺同一区域多client共用钱包。** 现账本tenant/client键不改、不合并余额；当前发布保持现有接入范围，领取记录保存实际钱包client。其他client不能自动重新发放或被映射到一个伪造的固定client。扩开第二个client之前需另做共享钱包设计，不属于本次交付。
5. 多区域的钱包/赠款规则不在本次完整实现；不新增区域切换、区域管理、跨区转账、多端钱包迁移、OAuth多租户签发重构、历史钱包整理或新的定时任务。
6. 不重复赠送、赠款与实际扣款使用同一钱包、账本完整和旧用户不误领属于本次必做，不因收范围而删除。

## 2. 已核对源码与最早验证

2026-10-10本轮只读核对本地HEAD：API `33e2344a2af02bb908a20bec1125ab7c23e8d00d`；Web `17ecf1c0b581cab1456acff4db097a6a4d335e3d`。本轮未查询远端或当前线上版本，不声称这些就是最新线上。工作目录分别为`/home/isp/wsps/cyf/api`、`/home/isp/wsps/cyf/web`；实施前按项目规则重新固定branch/tree及各Owner，不覆盖已有修改。

- `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletController.java:88–101`：已有`POST /economy/onboarding-grant`，请求{}；156–173的钱包scope硬编码tenant为0。
- `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletService.java:109–149`：现领取按scope/actor/campaign幂等，金额参与hash，不能仅把1000改成2000，否则旧活动冲突或换活动后旧用户再领。61–72的钱包查询只读，156–172的账户初始化余额为0。
- `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyOnboardingGrantProperties.java`已有开关/金额/活动配置；`EconomyPreviewGate`已有精确tenant/client授权。
- `/home/isp/wsps/cyf/api/common/jia-common-core/src/main/java/cn/jia/core/security/TenantClaimPolicy.java`提供规范tenant名称与校验，但旧resolve有单租户兜底，赠款入口不得直接继承该兜底。
- `/home/isp/wsps/cyf/api/oauth/jia-oauth-service/src/main/java/cn/jia/oauth/security/AccountSecurityTokenCustomizer.java`已有tenant_id、client_id、uid等签发代码；实际受测token及用户归属还需实施时确认。
- `/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js:47–48,82–92,194–199,282–294`：当前是初租不足才触发赠款，必须删除该触发方式。
- agent中仍有多处tenant必须为0的校验，涉及托管、悬赏和其他服务；本次不全量替换后声称多区域已完成。只保证当前发布范围闭环，其他区域保持未启用。

**最早定向验证：**真实认证身份能取得合法uid/规范tenant/client并核对持久用户；当前钱包、赠款、租金和悬赏付款主体一致；原安装步骤能承接旧用户基线初始化。三项不成立须针对实际缺口修复并更新估时，不能以默认tenant、按sub多发或忽略迁移代替。

## 3. 后端最小实现

### 3.1 只新增领取记录表

`economy_onboarding_grant_claim`，沿用经济表字符集/排序规则和版本化schema核验，不增加第二账本。

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| tenant_id | VARCHAR(50) NOT NULL | 来自可信认证上下文的业务区域 |
| user_id | BIGINT NOT NULL，>0 | 持久稳定用户id |
| client_id | VARCHAR(50) NULL | 实际发款钱包的client，审计和交易定位；不是防重维度；EXCLUDED可空 |
| actor_id | VARCHAR(100) NULL | 已绑定的钱包付款主体；EXCLUDED可空 |
| status | VARCHAR(16) NOT NULL | POSTING / POSTED / EXCLUDED |
| transaction_id | VARCHAR(100) NULL | 原复式账本真实交易id |
| amount_micro | BIGINT NOT NULL DEFAULT 0 | 实际已发金额，不是钱包余额 |
| campaign_ref | VARCHAR(100) NULL | 固定用途审计标签，不决定领取次数 |
| reason_code | VARCHAR(32) NULL | EXCLUDED为PREEXISTING_USER |
| create_time / update_time | BIGINT NOT NULL | 服务端毫秒时间 |

- 主键`(tenant_id,user_id)`；交易引用唯一键`(tenant_id,client_id,transaction_id)`，匹配当前账本scope。
- POSTING：client/actor/campaign非空、amount=2000000000、transaction/reason为空，仅在同一未提交事务中存在。
- POSTED：client/actor/campaign/transaction非空、amount>0、reason为空；回放返回原实际金额。
- EXCLUDED：amount=0，client/actor/transaction/campaign为空，reason=PREEXISTING_USER；不伪造零金额交易。
- 不改现有account/transaction/entry/escrow主键，不复制旧309笔补款为新的POSTED。

### 3.2 复用原POST及记账服务

请求仍为`POST /economy/onboarding-grant {}`；用户、金额、tenant/client不接受body指定。

1. 校验用户token（拒绝machine）、规范tenant、可信client、uid与持久用户/归属；缺tenant不默认0。通过现有scope授权，确认本次配置及该区域旧用户基线已生效。
2. 读取/占位并锁定`(tenant_id,user_id)`。EXCLUDED返回NOT_ELIGIBLE；POSTED返回原回执。已有记录client与当前client不符时返回明确scope不匹配，不发第二笔、不虚构该client钱包已经到账。
3. 在同一个REQUIRED事务中初始化原钱包/发行账户（余额0）、调用原treasury.issue，并写POSTED/真实transaction。记账仍为用户AVAILABLE +2000000000、系统SILVER_ISSUANCE -2000000000。
4. 固定用途`new-user-initial-grant`，确定性请求键以tenant+stable uid+固定用途生成，不随活动版本、金额、登录别名或client变化。读取已POSTED时不拿新配置重算旧hash。
5. 原posting为REQUIRED，不独立提交；失败整体回滚。锁序保持claim → 原交易幂等占位 → 原排序账户锁。并发插入冲突须通过数据库支持的占位/锁定方式收敛，不能在已被标记回滚的事务内假装继续。
6. 领取按uid防重，但现钱包按actor记账：为领取过的新用户固定claim.actor_id。钱包/流水、租金、悬赏付款入口通过共享资金身份解析回用该actor；仅解析资金主体，不改业务owner/ACL、不重写历史钱包。EXCLUDED且未绑定主体者沿用已有钱包身份；已有多主体归属冲突明确报错，不自动搬钱。
7. 金额配置2000000000；现有旧1000业务实现同步替换，不同时保留两个活动入口。GET wallet/ledger继续只读，不直接更新余额字段。

响应（金额、时间十进制字符串）：
- `POSTED`：transactionId、amountMicro、campaignRef、postedAt、replayed；重放原回执不反复弹到账提示。
- `NOT_ELIGIBLE`：reasonCode=PREEXISTING_USER、amountMicro="0"、transactionId=null。
- 未登录401；身份/scope不符403；暂不可用明确报错。失败不显示假2000，重试不会重复发放。

实现落点：原WalletController/WalletService、grant配置；新增claim entity/mapper/事务服务；共用资金身份接口复用user-api核验，不跨模块直连user mapper。接入WalletController、HostingRentHttp、托管admission、FundedBountyActor构造及经济预览钱包读取的实际资金主体调用点。Owner先列实际diff，避免全局字符串替换。仅改必要调用点，不做完整多区域改造。

## 4. 前端最小实现

- 聚义厅`/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue`与钱包`/home/isp/wsps/cyf/web/src/components/Wallet.vue`共用一个自动初始化方法：认证就绪 → POST赠款 → GET真实钱包。
- 同一tenant/client/用户和authorizationGeneration合并在途请求；刷新可重试，由后端防重。身份切换/卸载取消或丢弃迟到结果，不拿localStorage领取标记作权威。
- POSTED仅首次成功显示2000到账；NOT_ELIGIBLE正常加载钱包。失败复用现有错误/重试区域，不阻止浏览，不增加循环后台任务。
- 删除`/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js`的初租不足领1000调用及`/home/isp/wsps/cyf/web/src/components/juyiting/HostingRentPanel.vue`对应领取UI。租金不足只提示，不自动充值、不自动确认租约。

## 5. 老用户处理与发布

- 原发布窗口内协调实际user_info创建写入，固定启用前旧用户集合，按当前发布区域写EXCLUDED并记录集合摘要。不能沿用历史309/310人数、最大ID或可空create_time；共享登录用户不能因client_id为空漏掉。
- 只处理当前明确的业务区域；不把旧用户集合向所有tenant广播。未来新增区域怎样定义新用户另议，不成为这次赠款前置开发。
- 基线、表结构和配置验证完成才启用POST；缺基线不能因查不到claim而直接发。复用原迁移记录/安装步骤，不新建长期基线管理平台。原安装hook接线尚需确认；发布锁不能替代注册写入互斥。
- 按固定版本/源码/制品发布：前端Flow4403172，后端本地原编排器/安装器；保留发布锁、制品摘要、备份与账本恢复边界。develop合入不自动部署。
- 本方案不执行迁移或补款。生产测试采用授权新测试用户，不能给旧账号再发一笔当验收。

## 6. 必要验收

1. 新用户首次入厅与直接入钱包各自可获得2000，并能被现租金/悬赏链路使用；余额不是只在前端显示。
2. 刷新、并发、响应丢失后重试、不同登录方式：同一tenant/uid仅一笔赠款且落入同一资金主体。
3. 老用户含已补款/旧1000/无钱包/空时间/修复异常身份，不再额外领取，原流水不动。
4. 当前配置以外的tenant/client、缺tenant、伪造uid均不获赠；合成非生产tenant值验证代码无固定0依赖，不据此宣称全站多区域可用。
5. 任一步故障回滚，无半笔余额或持久POSTING；真实MySQL验证并发/事务，复用已有测试设施。
6. 改金额/活动标签不重发；租金不足/重新入伙/免费重整不再触发旧赠款；前端切身份无串账。

## 7. 工作量与分工估算

这是对上述**最小方案**的工程估算，不是实测耗时或两小时完成承诺。前后端各一位Owner并行，无新增Reviewer，尚未派发。

| 工作 | 估计投入 |
|---|---|
| 后端：领取记录、事务、防重、资格、资金身份接线及定向测试 | 2–3小时 |
| 前端：自动领取、删除旧触发、身份切换及测试 | 0.5–1小时，可与后端并行 |
| 旧用户迁移接线、真实MySQL并发/回滚、联调 | 1–1.5小时 |
| 制品构建、发布、线上验收 | 0.5–1小时，排队/冷缓存另计 |

总投入约4–6.5人时；双端并行安排下，**开发与定向自测按3–4小时，发布及最终验收再预留1–2小时，总历时按4–6小时规划**。实际等待单记，不把开发完成报告成已发布。

执行拆分继续以20–30分钟检查点推进：契约/身份核对 → DDL/mapper → 领取事务 → 防重/回滚测试 → 资金主体接线（必要时拆两个切片）；前端初始化与旧触发删除独立并行；其后基线/并发/联调/发布分别留回执。检查点不是到点强停或保证每片不超时。

主要不确定性：真实登录别名与钱包主体、安装前置基线接线、真实MySQL及构建环境。若发现已有多钱包需要数据合并或用户创建写入无法协调，明确列出受影响范围和新增工时，不借收范围放任错账，不扩成全量多租户工程。
