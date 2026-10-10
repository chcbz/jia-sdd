# 新用户自动赠送2000积分：最小闭环方案

修订日期：2026-10-10。Owner：主控（方案）；开发未派发；本文件内任务编号是设计编号，不是已创建/已运行的Agent任务。状态：**范围收敛后的待实施方案，未改业务代码、未迁移、未发布**。本版替代前版把完整多区域/跨客户端钱包改造并入赠款的工作范围；历史方案保留在Git，不并行实施。

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

2026-10-10核对公共字段依据：`/home/isp/wsps/cyf/api/common/jia-common-core/src/main/java/cn/jia/core/entity/BaseEntity.java`含tenantId/clientId/createTime/updateTime；`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/economy-v0-foundation.sql`的account/transaction表另有自增id，scope和时间均NOT NULL。领取表按该经济模块风格补齐，不自行增加无用途的deleted/version/create_by/update_by字段。

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| id | BIGINT NOT NULL AUTO_INCREMENT | 技术主键，沿用经济表风格 |
| tenant_id | VARCHAR(50) NOT NULL，无SQL默认值 | 来自可信认证上下文的业务区域；迁移取已批准目标配置 |
| user_id | BIGINT NOT NULL，>0 | 持久稳定用户id |
| client_id | VARCHAR(50) NOT NULL，无SQL默认值 | POSTING/POSTED为真实接入及发款钱包client；EXCLUDED为本次基线初始化的目标client，不声称是用户注册client |
| actor_id | VARCHAR(100) NULL | 已绑定的钱包付款主体；EXCLUDED可空 |
| status | VARCHAR(16) NOT NULL | POSTING / POSTED / EXCLUDED |
| transaction_id | VARCHAR(100) NULL | 原复式账本真实交易id |
| amount_micro | BIGINT NOT NULL DEFAULT 0 | 实际已发金额，不是钱包余额 |
| campaign_ref | VARCHAR(100) NULL | 固定用途审计标签，不决定领取次数 |
| reason_code | VARCHAR(32) NULL | EXCLUDED为PREEXISTING_USER |
| create_time | BIGINT NOT NULL，无SQL默认值 | 服务端创建毫秒时间，插入时明确填写，之后不改 |
| update_time | BIGINT NOT NULL，无SQL默认值 | 插入时与create_time一致；状态实际变更时由服务端更新 |

- 技术主键`PRIMARY KEY (id)`；业务防重唯一键`uk_onboarding_grant_user (tenant_id,user_id)`；交易引用唯一键`uk_onboarding_grant_transaction (tenant_id,client_id,transaction_id)`，匹配当前账本scope。client保留为公共字段，**不进入领取次数唯一键**。
- “默认字段”指公共字段，不等于赋固定默认值：tenant/client不写`DEFAULT '0'`或具体client，不能缺值回退；空白值在服务边界拒绝。时间由服务端明确赋值，原生mapper插入不能假设BaseEntity注解一定触发填充。
- claim资格查询/占位按tenant+uid，不能因公共client过滤而看不到其他client已存在的领取记录。通过当前请求ACL后使用明确的claim mapper SQL（不全局取消client隔离），检查原记录client再决定回执可见性；其他client不能覆盖原client/actor/transaction或新发一笔。EXCLUDED先按tenant+uid生效，不因其记录的初始化client不同失效。
- POSTING：client/actor/campaign非空、amount>0（本期配置2000000000）、transaction/reason为空，仅在同一未提交事务中存在。金额由服务规则决定，DDL只约束合法正值，不把业务金额写成不可变schema常量。
- POSTED：client/actor/campaign/transaction非空、amount>0、reason为空；回放返回原实际金额。
- EXCLUDED：client为批准的基线目标client，amount=0，actor/transaction/campaign为空，reason=PREEXISTING_USER；不伪造零金额交易或用户注册来源。
- 不改现有account/transaction/entry/escrow主键，不复制旧309笔补款为新的POSTED。

### 3.2 复用原POST及记账服务

请求仍为`POST /economy/onboarding-grant {}`；用户、金额、tenant/client不接受body指定。

1. 校验用户token（拒绝machine）、规范tenant、可信client、uid与持久用户/归属；缺tenant不默认0。通过现有scope授权，确认本次配置及该区域旧用户基线已生效。
2. 按`(tenant_id,user_id)`读取资格；新建时严格INSERT获得行写锁，冲突回读使用FOR UPDATE，详见3.4。EXCLUDED先返回NOT_ELIGIBLE；POSTED先核对记录client与当前client相符，再返回原回执。不符则返回明确scope不匹配，不发第二笔、不虚构该client钱包已经到账。
3. 在同一个REQUIRED事务中初始化原钱包/发行账户（余额0）、调用原treasury.issue，并写POSTED/真实transaction。记账仍为用户AVAILABLE +2000000000、系统SILVER_ISSUANCE -2000000000。
4. 固定用途`new-user-initial-grant`，确定性请求键以tenant+stable uid+固定用途生成，不随活动版本、金额、登录别名或client变化。读取已POSTED时不拿新配置重算旧hash。
5. 原posting为REQUIRED，不独立提交；失败整体回滚。锁序保持claim INSERT写锁 → 原交易幂等占位 → 原排序账户锁。claim唯一冲突退出原事务，由非事务入口在独立代理的新事务中回读，详见3.4；不能在已被标记回滚的事务内假装继续。
6. 领取按uid防重，但现钱包按actor记账：为领取过的新用户固定claim.actor_id。钱包/流水、租金、悬赏付款入口通过共享资金身份解析回用该actor；仅解析资金主体，不改业务owner/ACL、不重写历史钱包。EXCLUDED且未绑定主体者沿用已有钱包身份；已有多主体归属冲突明确报错，不自动搬钱。
7. 金额配置2000000000；现有旧1000业务实现同步替换，不同时保留两个活动入口。GET wallet/ledger继续只读，不直接更新余额字段。

响应（金额、时间十进制字符串）：
- `POSTED`：transactionId、amountMicro、campaignRef、postedAt、replayed；重放原回执不反复弹到账提示。
- `NOT_ELIGIBLE`：reasonCode=PREEXISTING_USER、amountMicro="0"、transactionId=null。
- 未登录401；身份/scope不符403；暂不可用明确报错。失败不显示假2000，重试不会重复发放。

实现落点：原WalletController/WalletService、grant配置；新增claim entity/mapper/事务服务；共用资金身份接口复用user-api核验，不跨模块直连user mapper。接入WalletController、HostingRentHttp、托管admission、FundedBountyActor构造及经济预览钱包读取的实际资金主体调用点。Owner先列实际diff，避免全局字符串替换。仅改必要调用点，不做完整多区域改造。

### 3.3 可直接翻译为迁移的DDL

以下是设计SQL，不代表已创建表。新资源定位见第8节N01；字符集、字段顺序、默认值、唯一键、CHECK同步进入schema核验。没有DDL级tenant/client默认值，没有软删除。

```sql
CREATE TABLE IF NOT EXISTS economy_onboarding_grant_claim (
    id BIGINT NOT NULL AUTO_INCREMENT,
    tenant_id VARCHAR(50) NOT NULL,
    user_id BIGINT NOT NULL,
    client_id VARCHAR(50) NOT NULL,
    actor_id VARCHAR(100) NULL,
    status VARCHAR(16) NOT NULL,
    transaction_id VARCHAR(100) NULL,
    amount_micro BIGINT NOT NULL DEFAULT 0,
    campaign_ref VARCHAR(100) NULL,
    reason_code VARCHAR(32) NULL,
    create_time BIGINT NOT NULL,
    update_time BIGINT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_onboarding_grant_user (tenant_id, user_id),
    UNIQUE KEY uk_onboarding_grant_transaction (tenant_id, client_id, transaction_id),
    CONSTRAINT chk_onboarding_grant_user CHECK (user_id > 0),
    CONSTRAINT chk_onboarding_grant_scope CHECK (
        OCTET_LENGTH(tenant_id) > 0 AND OCTET_LENGTH(client_id) > 0),
    CONSTRAINT chk_onboarding_grant_state CHECK (
        (status='POSTING' AND actor_id IS NOT NULL AND OCTET_LENGTH(actor_id)>0
         AND campaign_ref IS NOT NULL AND OCTET_LENGTH(campaign_ref)>0
         AND amount_micro>0 AND transaction_id IS NULL AND reason_code IS NULL)
        OR
        (status='POSTED' AND actor_id IS NOT NULL AND OCTET_LENGTH(actor_id)>0
         AND campaign_ref IS NOT NULL AND OCTET_LENGTH(campaign_ref)>0
         AND amount_micro>0 AND transaction_id IS NOT NULL
         AND OCTET_LENGTH(transaction_id)>0 AND reason_code IS NULL)
        OR
        (status='EXCLUDED' AND amount_micro=0 AND actor_id IS NULL
         AND transaction_id IS NULL AND campaign_ref IS NULL
         AND reason_code IS NOT NULL AND reason_code='PREEXISTING_USER')
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;
```

CHECK不能代替身份/字符串校验。含空白、非法长度、非法uid仍在服务入口拒绝；校验失败不得进入mapper。MySQL的NULL CHECK语义不能用作放行漏洞，EXCLUDED显式要求reason非NULL。

### 3.4 Mapper合同与事务伪代码

新建独立claim mapper，不给原不可变账本mapper加通用CRUD。方法均为设计新增，N02/N03见第8节：

| 方法 | SQL及返回约定 |
|---|---|
| `selectByUser(tenantId,userId)` | 精确tenant+uid读取；tenant含OCTET_LENGTH匹配；不附加client筛选；无FOR UPDATE，用于资金主体读取 |
| `insertPosting(row)` | 普通严格INSERT，显式填写公共字段；成功才取得本次新行所有权。唯一冲突立即抛出并退出整个事务，不使用INSERT IGNORE或依赖affectedRows猜归属 |
| `selectByUserForUpdate(tenantId,userId)` | 同一精确键`SELECT ... FOR UPDATE`；事务锁序首位 |
| `markPosted(...)` | `UPDATE ... WHERE tenant_id=? AND user_id=? AND client_id=? AND actor_id=? AND status='POSTING'`；只改status/transaction_id/update_time，影响行数必须1 |
| `selectExcludedUserIds(tenantId)` | 只读取EXCLUDED的uid，按数值升序；用于启用基线核验，不供前端查询 |

运行时mapper不提供删除、改client、改actor或POSTED→其他状态的方法。基线EXCLUDED插入只在版本化迁移中提供，不暴露HTTP接口。

`EconomyWalletService`保留非事务入口，委托独立Spring bean `EconomyOnboardingGrantService.claim(verifiedIdentity)`的公开REQUIRED事务方法。唯一冲突必须在该代理事务**完成回滚后**才由非事务入口转入另一公开REQUIRED方法`replayAfterConflict`；禁止同类self-invocation。简化顺序：

```text
非事务入口：校验认证/持久用户/当前scope授权和baseline ready
调用独立bean的claim，BEGIN REQUIRED
  selectByUser(tenant,uid)          // 非锁读，避免不存在行的gap锁升级
  若EXCLUDED：返回NOT_ELIGIBLE
  若POSTED：核对client和真实账本回执，返回replayed=true
  若读到已提交POSTING：报数据异常，不接管/补发
  若不存在：insertPosting(本次scope、uid、认证actor、2000)
            插入成功即取得本次claim行写锁；唯一冲突则抛出专用异常并ROLLBACK
  provision原AVAILABLE及发行账户，余额初值0
  treasury.issue(确定性key，实际scope/actor/amount/campaign的hash)
  markPosted，affectedRows必须1
  返回真实transactionId/postedAt，replayed=false
COMMIT

仅在claim INSERT唯一冲突、上述事务已回滚后：
  非事务入口调用同一独立bean的replayAfterConflict，BEGIN新的REQUIRED事务
  selectByUserForUpdate(tenant,uid)
  POSTED核对scope/真实回执后返回；EXCLUDED返回不符合资格
  行不存在或已提交POSTING：明确报错，不在此分支补发
  COMMIT
```

只把claim INSERT冲突标记为可回读冲突；发行账户/账本的其他异常按原逻辑处理，不能一律吞成“已领取”。内部捕获重复键仅可立即重抛专用运行时异常用于回滚，不能在rollback-only事务内继续SQL。调用入口不得已有外层事务；B06通过Spring集成测试确认调用边界。真实死锁/连接中断回滚后返回现有可重试错误，由同一幂等请求重试，不新增无限重试循环。整个成功领取始终只有一个REQUIRED事务，不使用REQUIRES_NEW把账本独立提交。

### 3.5 资金身份接口与调用边界

N04定义普通Java值对象，不使economy-api依赖Spring Security或agent-service：

```java
record MoneyIdentityInput(String tenantId, String clientId, long userId,
                          String jiacn, String authenticatedActorId) {}
record ResolvedMoneyIdentity(EconomyScope scope, long userId,
                             String payerId, String ownerJiacn) {}
interface EconomyMoneyIdentityResolver {
    ResolvedMoneyIdentity resolve(MoneyIdentityInput input);
}
```

- 这些输入只由已验证JWT适配器产生，不绑定HTTP body；`token_kind=user`、规范tenant_id、client_id、uid、jiacn、sub逐项校验，uid用合法正long解析。
- N05经user-api核对uid/jiacn及所属区域，不能只凭前端uid；经济服务显式依赖`:user:jia-user-api`，不依赖user-service或agent-service。具体用户归属判定由A01核对当前模型，NULL client不能当跨区授权。
- 无claim/EXCLUDED：保留当前已认证actor及原历史行为；POSTED且client一致：使用claim.actor_id，防止登录别名导致赠款和扣款走不同钱包；其他client拒绝；已提交POSTING报数据异常。
- grant事务直接使用已核验身份，不在同事务把刚写的POSTING当成外部污染记录再次走resolve；避免身份解析器和赠款服务循环调用/循环注入。
- E05–E08只替换**付款主体**构造，ownerJiacn、Agent归属、订单授权保持原值；未属于资金的`sub`不全局改。任何发现已有订单资金主体与新绑定不一致，先报受影响范围，不自动迁移。

### 3.6 启用配置及基线完成判定

补齐原先“基线完成”过于抽象的实现：沿用E03配置类，新增`scopes`列表，每项包含`tenantId/clientId/baselineUserCount/baselineUsersSha256`。当前部署只填一个已批准的scope，Java没有生产标识常量。

- `enabled=false`：不发放；`enabled=true`：amountMicro为本期2000000000，scope字段均必填，必须同时满足原EconomyPreviewGate。相同tenant暂不配置多个client（本期未交付共享钱包）。
- 启动时N07校验DDL后，读取各配置tenant下EXCLUDED uid列表；按`十进制uid + LF`逐行、升序、UTF-8计算SHA256，并比较固定count/hash。空名单只允许明确配置count=0和空字节摘要，不能缺配置当空名单。禁止GROUP_CONCAT摘要以免截断。
- count/hash来自受控发布窗口内的真实旧用户快照，在DML提交/逐行核验后写入当前发布配置并留回执；不是手填一个ready=true。基线校验失败时赠款不可用，不能用空表表示“所有人都是新用户”。
- 后续重启只核验固定EXCLUDED，不重新扫描并排除全部user_info；新增POSTED不改变旧名单摘要。实际列/索引/CHECK、已排除uid及配置证据一起固定。
- 原安装器E12在本次读到的stop→start路径中未见可直接套用的业务DML hook，**不声称现成支持**。A02必须先固定迁移执行位置、实际注册写入协调方式及锁/回执归属；M02只做本次最小接线。如需要增加安装器能力，须列准确diff和测试，不把“继续等”当完成、不临时执行任意shell绕开原安装器。

### 3.7 精确HTTP合同（前后端共用fixture）

- 请求：认证`POST /economy/onboarding-grant`，Content-Type为JSON，body仅`{}`；不接受query或多余字段。本轮补核对MicroSilver.format仅执行Long.toString，现OnboardingGrantResponse.amountMicro已是整数micro字符串；直接沿用该单位和字符串格式，仅补本方案状态/回执字段，不做单位转换，GET钱包单位也不改。
- 首次200：`{"status":"POSTED","transactionId":"<真实ID>","amountMicro":"2000000000","campaignRef":"new-user-initial-grant","postedAt":"<服务端毫秒>","replayed":false}`。
- 重放200：上述transactionId/金额/postedAt保持原值，replayed=true；真实postedAt从同笔账本交易取，不用重试当前时间冒充。
- 老用户200：`{"status":"NOT_ELIGIBLE","reasonCode":"PREEXISTING_USER","amountMicro":"0","transactionId":null,"campaignRef":null,"postedAt":null,"replayed":false}`。
- 401未认证；403身份/scope不符或赠款关闭；400非空请求体/非法字段；503基线未就绪/数据不一致/暂不可用；可重试的并发冲突沿用现有409错误形状。不返回其他client的transaction详情。
- 沿用现错误体`code/message/retryable/currentVersion`（currentVersion为NULL时现注解省略），不新增第二错误包装；F01从Controller实定义复制fixture，不按聊天猜响应壳。缺真实回执/基线时不得返回POSTED。

## 4. 前端最小实现

- 聚义厅`/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue`与钱包`/home/isp/wsps/cyf/web/src/components/Wallet.vue`共用一个自动初始化方法：认证就绪 → POST赠款 → GET真实钱包。
- 同一tenant/client/用户和authorizationGeneration合并在途请求；刷新可重试，由后端防重。身份切换/卸载取消或丢弃迟到结果，不拿localStorage领取标记作权威。
- POSTED仅首次成功显示2000到账；NOT_ELIGIBLE正常加载钱包。失败复用现有错误/重试区域，不阻止浏览，不增加循环后台任务。
- 删除`/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js`的初租不足领1000调用及`/home/isp/wsps/cyf/web/src/components/juyiting/HostingRentPanel.vue`对应领取UI。租金不足只提示，不自动充值、不自动确认租约。

## 5. 老用户处理与发布

- 原发布窗口内协调实际user_info创建写入，固定启用前旧用户集合，按当前发布区域写EXCLUDED并记录集合摘要。不能沿用历史309/310人数、最大ID或可空create_time；共享登录用户不能因user_info.client_id为空漏掉；领取表的client_id从本次批准的目标配置显式传入，不复制该空值、不猜用户历史来源。
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
7. 公共字段完整写入且无固定scope默认值；技术id自增、tenant/uid唯一；跨client请求不会被隐式过滤误判为未领取；EXCLUDED的client来自固定基线配置，重放不改原client/actor/create_time。

## 7. 半小时任务单与完成规则

### 7.1 时间规则及Owner

- 每项**主动工作计划10–25分钟**，最长预估不超过30分钟；这不是对未知故障/构建队列/生产等待作虚假必达保证。第20分钟仍有明显剩余时，在既有handoff记录具体剩余diff、失败证据和后续切片，不把整个任务重新跑一遍。
- 超过30分钟仍未满足完成标准则保留`进行中/阻塞`，拆剩余工作并更新预计完成时间；不得改标已完成、跳测试或按时间强杀构建/数据库事务/发布进程。没有额外新增全项目硬deadline规则。
- 同一Owner连续推进，不等逐项人工确认；只有真实权限/数据归属/发布阻塞才请求用户。每项输出文件diff或证据路径；代码片“实现完成”、批量测试“验证完成”、安装“已发布”分开。
- Owner角色：**后端Owner**负责同一个API worktree全部后端源码；**前端Owner**负责Web worktree；**主控**负责根仓方案、基线/发布接线与集成。当前仅规划，未创建任务、未派发Agent，不能以此表宣称后台已经运行。
- 下表时间包含本切片实现及轻量自检；Gradle/Flow/MySQL等待单列。各切片先补对应测试，依赖齐备后按受影响范围合批验证，不每个20分钟切片全量构建。没有实际PASS证据的测试只能标“已补用例”。

### 7.2 具体任务（路径代号展开见第8节）

| ID | Owner/计划 | 输入与依赖 | 唯一交付、改动边界 | 完成标准/最早验证 |
|---|---|---|---|---|
| A01 | 主控/15分 | 本文、本地/远端/候选/线上基线 | 固定各仓branch/worktree/HEAD/tree；只读核验JWT规范claim、持久用户归属及资金actor；记录允许scope | handoff有实际身份路径和源码值来源，不含token原文；未知写UNKNOWN；用户归属无法证明则记录阻塞，禁止默认0 |
| A02 | 主控/20分 | A01、E12 | 固定旧用户写入来源、停写位置、基线DML执行点、配置落点及原installer接线方案 | 精确文件/方法/锁和恢复顺序已列；确认是否需要E12补接线；只做设计/只读，不停服务 |
| B01 | 后端/20分 | A01、§3.3 | N01 DDL + N02 entity，字段/索引/CHECK逐项一致 | diff与§3.3匹配；id主键、tenant/uid唯一，scope无固定默认值；补非法NULL/重复uid用例 |
| B02 | 后端/20分 | B01 | N03五个mapper方法，仅claim表SQL | 所有写入显式公共字段；无通用delete/update；跨client可查同uid但不能改原client；补mapper用例 |
| B03 | 后端/20分 | B01、A02 | N07 schema/baseline核验及E03/E04配置注册 | 精确schema/count/hash检查用例齐；默认禁用，缺基线不可发，不扫描新用户重建基线 |
| B04 | 后端/20分 | A01 | N04值对象/接口、N05认证用户核验部分；E11加user-api依赖 | 合法用户与缺tenant/machine/uid不符用例齐；没有agent-service依赖环或默认scope |
| B05 | 后端/20分 | B02、B04 | N05绑定资金主体的读取分支 | 无claim/EXCLUDED/POSTED/错client/已提交POSTING五分支用例齐；不改变业务owner；无写副作用 |
| B06 | 后端/25分 | B02–B05 | N06单事务占位→issue→markPosted；E02提供受控账户初始化复用 | 首次一笔两条分录、异常整体回滚用例齐；普通INSERT成功才获行所有权，唯一冲突回滚后新事务回读；无自调用事务失效 |
| B07 | 后端/20分 | B06 | N06重放/老用户/并发错误处理、固定幂等key/hash | POSTED用原回执；改金额/标签不重发；不接管外部POSTING；不在rollback-only事务继续记账 |
| B08 | 后端/20分 | B07、F01 | E01接线N05/N06，E02删除旧campaign决定领取次数的分支 | §3.7成功/老用户/错误响应及空body校验用例齐；wallet/ledger仍只读，无两个赠款实现 |
| B09 | 后端/20分 | B05 | E05和E06托管付款身份适配 | claim绑定payer贯穿报价/确认/续租；owner/租约ACL不改；admission和实际付款scope一致 |
| B10 | 后端/20分 | B05 | E07/E08/E09悬赏与预览资金主体适配 | 同一用户别名变化不分裂新赠款钱包；两处悬赏Actor入口均覆盖；原owner值不被替换 |
| B11 | 后端/25分 | B08–B10 | N08及既有wallet/hosting/bounty测试；E11接入现有定向source set | 列明实际测试类/selector，新增用例确实在source set内；无未配置MySQL就把skip报PASS |
| F01 | 前端/15分 | §3.7，可与B01并行 | N09共享响应fixture及前端解析断言，与后端Owner确认同一合同 | POSTED/重放/NOT_ELIGIBLE/错误四类样例齐；micro用字符串不失精度，不改旧GET钱包单位 |
| F02 | 前端/20分 | F01 | N10共享自动领取composable，N11用例 | 同身份合并在途、主动刷新可重试、身份/区域变更丢迟到结果；不localStorage防重、不循环请求 |
| F03 | 前端/20分 | F02 | E13/E14初始化接N11，沿用现有提示/重试UI | 入厅/直达钱包均先POST后读真实余额；旧用户继续显示原钱包；失败不假显示2000 |
| F04 | 前端/20分 | F03 | E15/E16删除初租领1000及按钮，更新E17 | 租金不足/重整/重入伙无赠款调用；新手初始化之外无遗留触发；仅定向本地诊断非正式Flow证据 |
| M01 | 主控/25分 | A02、B01 | N12迁移SQL/固定旧uid输入格式、count/hash及核验步骤 | 只插EXCLUDED、不改余额；重放仅接受同原uid集合；已POSTED不可覆盖；无历史人数/最大ID捷径 |
| M02 | 主控/25分 | M01、B03、A02 | 按A02核定位置做本次原installer/配置最小接线，新增受影响工具测试 | 固定配置接收迁移真实count/hash；接线失败不启动赠款；原锁/备份/回执不绕开。若需超出本次补丁范围，明确拆子片而非标完成 |
| V01 | 后端/25分 | B11、M01、MySQL可用 | 真实MySQL并发领取与跨client防重回归 | 多请求同tenant/uid仅一个claim、一笔ISSUE；真实交易平衡，报告测试数和无skip证据 |
| V02 | 后端/20分 | V01 | 回滚、旧用户基线、别名变更及租金/悬赏受影响回归 | 注入异常无半笔资金；新余额可供原付款链路使用；旧余额不动；失败精确归因不重跑无关测试 |
| V03 | 主控/10分主动操作 | V02、M02、固定候选 | 经原编排器提交后端正式测试/validateLayering/制品构建，记录build ID/日志 | 提交回执不等于构建成功；最终所需任务PASS及fresh JAR SHA由W01回收；等待不占30分承诺 |
| V04 | 前端/10分主动操作 | F04、后端HTTP合同固定 | 提交前端4403172正式测试/构建，记录Run/commit | Flow触发按实际配置核查是否含部署，未到发布顺序不提前让新前端调用旧接口；不得本机生产打包；等待由W02记录 |
| R01 | 主控/20分主动操作 | W01/W02制品PASS、M02、原生产授权 | 锁/备份下按A02顺序固定旧uid、执行基线、核验配置、原installer部署后端，再部署配套前端 | 有实际迁移摘要和同批安装回执才能标已发布；服务等待由W03记录，不抢锁/不强杀 |
| R02 | 主控/25分 | W03安装/健康成功 | 授权真实新账号自动到账/刷新防重/钱包和账本核对；已有账号不再领 | 截图/API/SQL证据对应当前版本；若测试实际消费须覆盖授权，不擅自下单/再补旧账号 |
| R03 | 主控/10分 | R02 | 回写本文状态、现handoff及稳定知识入口 | 分别列源码、测试、制品、部署、线上验收；未完成项有Owner/下一动作，不用阶段总结代替继续推进 |

所有任务的“补用例”都须在V01/V02及正式构建中取得对应执行证据才能完成整体开发验收。A02/M02为已知不确定项，不能用尚未核验的安装能力承诺30分钟必达。

### 7.3 异步等待不是伪造的半小时任务

| 等待项 | 对应操作 | 关闭条件 | 期间如何推进 |
|---|---|---|---|
| W01 | V01/V02测试及V03后端构建 | 先有对应真实测试结果，后有同build ID测试/分层/依赖检查通过、fresh制品和SHA齐 | 同Owner跟踪真实日志；前端/迁移文档可继续，不重复启动Gradle |
| W02 | V04前端Flow | 同Run测试/构建产物通过且源码匹配；部署阶段按R01顺序处理 | 查原Run，不新建流水线、不取消他人任务；失败按根因修复 |
| W03 | R01生产安装/健康 | 原installer最终回执及版本/健康一致 | 按原恢复协议处理，不按30分钟强杀；无回执不标发布完成 |

没有在本次新建定时监控或启动等待任务。真正执行时沿用既有跟进方式，完成/失败/需用户操作时通知；不承诺无自动化支撑的后台定时监测。

### 7.4 总量与依赖

- **26个主动工作切片，每项10–25分钟，共510分钟（8.5人时）**。其中后端275分钟、前端85分钟、主控150分钟。该值是实现/定向核验/发布操作的规划投入，不包含不可预知的外部排队、构建运行及异常修复。
- 后端链：A01 → B01/B04 → B02/B05 → B03/B06 → B07/B08 → B09/B10 → B11 → V01/V02 → V03。同一API Owner串行；依赖表达允许先补接口，不声称依赖未就绪的集成已通过。
- 前端链：F01 → F02 → F03 → F04 → V04，与后端并行。迁移链A02 → M01/M02由主控并行准备，生产动作仅R01执行。
- 汇合：V03/W01 + V04/W02 + M02 → R01/W03 → R02 → R03。
- **按前后端各一位Owner、主控并行准备迁移，总历时暂按6–8小时规划**，实际外部等待另记。前版4–6小时偏乐观：细拆后明确计入schema/基线核验、共享资金身份接线及原installer适配，不是新增多区域功能。A01/A02发现无需某接线时可删除对应工作并下调，不能为了保持旧估时省掉必做项。

## 8. 文件与方法落点（现有/拟新增严格区分）

现有行号绑定第2节API/Web基线，开发后按方法名定位；未标现有行号的新类均是**拟新增**，不虚构已存在实现。

| 代号 | 绝对路径及落点 |
|---|---|
| E01 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletController.java`：88–101领取；156–173 requireSubject；wallet/ledger共用资金解析 |
| E02 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletService.java`：109–149旧grant/幂等辅助；156–172账户初始化；61–86钱包/流水 |
| E03 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyOnboardingGrantProperties.java`：record/构造校验；新增scopes，不留旧活动可多领分支 |
| E04 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyConfiguration.java`：10–25配置/初始化bean接线；不把原五表initializer改成缺六表自动重建 |
| E05 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentHttp.java`：35–55 Actor/actor；改为可注入适配或由调用方传已解析payer，不静态取Spring容器 |
| E06 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentHostingRentController.java`：68–96调用及126–136 requirePrincipal；与E07:204 bind入口一致 |
| E07 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentController.java`：204托管bind；620–632 requireMoneyActor |
| E08 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/funding/AgentBountySettlementController.java`：60–67 actor |
| E09 | `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/EconomyReadOnlyPreviewController.java`：146–168 principal，保留业务owner/其他scope字段语义 |
| E10 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyPostingServiceImpl.java`：107 post；只复用原事务记账，不新造第二记账器 |
| E11 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/build.gradle`：模块依赖及已有economyHostingRegression；`/home/isp/wsps/cyf/api/agent/jia-agent-service/build.gradle`：受影响测试source set先核对再补 |
| E12 | `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install`：1280–1316备份/stop/切换/start；当前只读定位，不等于拥有现成DML hook或本机安装副本与源码一致 |
| E13 | `/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue`：1877身份监听、2695初始化代次附近，实际以生命周期函数定位 |
| E14 | `/home/isp/wsps/cyf/web/src/components/Wallet.vue`：74–102 loadWallet/onMounted；补身份监听/取消而非仅mount一次 |
| E15 | `/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js`：47–48、82–92、194–199、282–294旧赠款分支 |
| E16 | `/home/isp/wsps/cyf/web/src/components/juyiting/HostingRentPanel.vue`：旧needsOnboardingGrant/claimOnboardingGrant相关模板与事件 |
| E17 | `/home/isp/wsps/cyf/web/tests/hosting-rent.test.js`、`/home/isp/wsps/cyf/web/tests/hosting-rent-ui.test.js`、`/home/isp/wsps/cyf/web/tests/economy-wallet-bounty.test.js` |
| N01 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/economy-onboarding-grant.sql` |
| N02 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-core/src/main/java/cn/jia/economy/entity/EconomyOnboardingGrantClaimEntity.java` |
| N03 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/java/cn/jia/economy/mapper/EconomyOnboardingGrantClaimMapper.java` |
| N04 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-api/src/main/java/cn/jia/economy/service/EconomyMoneyIdentityResolver.java`（§3.5 records可嵌套定义，避免无用文件拆分） |
| N05 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyMoneyIdentityResolverImpl.java` |
| N06 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyOnboardingGrantService.java` |
| N07 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyOnboardingGrantSchemaInitializer.java`，复用原schema解析规范，仅该表和固定基线校验 |
| N08 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/test/java/cn/jia/economy/service/impl/EconomyOnboardingGrantMySqlTest.java`与`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/test/java/cn/jia/economy/service/impl/EconomyMoneyIdentityResolverTest.java`；复用现`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/test/java/cn/jia/economy/config/EconomyMySqlTestFixture.java` |
| N09 | 拟新增`/home/isp/wsps/cyf/web/tests/fixtures/onboarding-grant.json`，作为前后端一致的响应例子，后端测试按同合同断言，不让API生产依赖Web仓文件 |
| N10 | 拟新增`/home/isp/wsps/cyf/web/src/composables/useOnboardingGrant.js` |
| N11 | 拟新增`/home/isp/wsps/cyf/web/tests/onboarding-grant.test.js` |
| N12 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/migration-onboarding-grant-baseline.sql`，绑定固定旧uid输入；真实凭据/用户清单只放受控发布证据，不提交Git |

## 9. 验证入口及证据要求

- 文档本次仅做路径/行号/合同/依赖及任务时间检查，不执行应用测试、DDL、构建或发布。
- 实施沿用`/home/isp/wsps/cyf/ops/orchestration/README.md`，所有Gradle操作先读当前相关build.gradle，经`/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle ...`串行执行；真实任务ID先在现ledger登记，不拿A01/B01设计编号假冒运行任务。
- B11明确把N08及原WalletController等必要测试纳入实际source set；现`:economy:jia-economy-service:economyHostingRegression`仅含原列出的测试，新文件不自动被执行。依赖编译/validateLayering/原账本保护均保留。
- 真实MySQL fixture/凭据按已有说明复用；未连接时的skip不是并发PASS。正式前端测试/生产打包/制品使用4403172；本地test只作诊断。
- 一份输入匹配的成功证据可复用，必要键包括源码tree、selector、fixture、工具链；没有证据不靠“应当通过”报完成。前端版本实际记录，不恢复Node精确版本门禁。
- 每项在现handoff记四栏：`输出或commit | 验证命令/结果或待验证 | 主动耗时/等待 | 下一动作/阻塞Owner`；不另建监控平台或重复台账。
