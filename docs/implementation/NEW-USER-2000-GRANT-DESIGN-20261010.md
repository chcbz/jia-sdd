# 新用户自动赠送2000积分：最小闭环方案

修订日期：2026-10-10。Owner：主控（方案）；开发未派发；本文件内任务编号是设计编号，不是已创建/已运行的Agent任务。状态：**待完成（2026-10-10用户要求先保存，暂不启动实施）；A01/A02及下述职责收口尚未闭合；未改业务代码、未迁移、未发布**。本版替代前版把完整多区域/跨客户端钱包改造并入赠款的工作范围；历史方案保留在Git，不并行实施。

## 待完成事项与恢复入口（2026-10-10保存）

- 用户本轮要求：先保存详设作为待完成事项，当前转向聚义厅流程缺口分析；本文件不构成新的开发、派单、迁移或发布指令。
- 已确认目标：新用户自动赠送2000 SILVER；钱包与领取隔离键均为`client_id + tenant_id + user_id`；不改`user_info.point`。
- 领取表建议保留为资格/一次性领取约束/真实交易关联表，不是第二账本，也不只是审计日志；金额事实仍以原账本为准。
- **恢复实施前须修订的职责问题**：本文§3.2/§3.5及B05/B09/B10仍描述用claim.actor_id驱动通用付款主体解析。该部分是尚未收口的设计，不可直接照搬编码。钱包身份应由统一钱包架构确定，不应依赖用户是否领取过赠款；claim.actor_id若保留应记录发放主体，不充当钱包身份注册表。先核定既有稳定user_id→payer解析落点及必要改动，再同步接口、用例、任务依赖和估时，不借本功能扩建身份系统。
- A01实际认证/区域授权与A02旧用户基线/原installer接线仍待核验；27切片/525分钟仅是此前方案估算，职责修订前不作为新交付承诺。
- 恢复顺序：收口上述职责与A01/A02 → 更新本详设任务单 → 在既有ledger登记真实实施任务 → 经用户要求继续实现。当前Owner为主控（文档保管），无已派发开发Agent。

## 0. 本轮完整复核结论（2026-10-10）

**用户最新确认：钱包遵循统一架构，以`(client_id,tenant_id,user_id)`作为业务隔离身份。** 本版同步修订钱包身份解析、领取资格、唯一键、幂等键、SQL、旧用户基线及测试，不保留“tenant+uid跨client共用领取资格”的例外。不同client或tenant是不同钱包和独立资格；仅在各自scope获准启用且满足新用户条件时各发一次，不代表切换任意client即可领钱。本轮仍只改详设，未修改数据库或业务实现。


**结论：不能把此前版本直接当成全部落地条件已齐的开发合同。** 本轮核对源码、设计SQL、身份/事务依赖、前端状态与发布DAG，仅改本文，不执行应用或生产操作。

| 问题 | 本轮处理 | 验证/剩余事项 |
|---|---|---|
| 账户初始化在记账前执行，实际已持有账户锁；原文却只写“交易幂等→账户锁” | §3.4明确初始化锁阶段，按原AccountKey.LOCK_ORDER排序；不改原账本核心 | B12/V01验证多个新用户与现付款并发，允许真实死锁回滚重试，不承诺无死锁 |
| WalletService委托grant，grant又复用WalletService私有初始化，可能形成bean依赖环 | 抽取只依赖mapper的N13初始化组件，两者单向依赖它 | 独立B12切片，Spring wiring测试 |
| 关闭赠款、schema初始化及已赠用户身份绑定的关系未定义 | §3.6区分schema必需、资金身份持续读取、赠款开关仅控制POST | 关闭开关后已有钱包/租金/悬赏仍用同payer |
| “改金额/活动不重发”与启动强制金额等于2000冲突；空表但旧账本已有grant的处理不明 | 配置校验合法正数、本期发布值2000；固定用途不允许随意换；查真实回执一致性 | 不迁移旧活动；新用途已有账本却缺claim按异常处理，不能自动恢复成成功 |
| 前端赠款失败会不会阻止钱包读、共享请求由谁取消、谁弹提示不清 | §4增加独立grant状态、共享请求所有权、按transaction去重提示 | F02/F03测试失败仍显示真实钱包、卸载不误取消其他组件 |
| 前端Flow是否可停在部署前未确认，却被当成先决条件 | §5/§7改成后端安装健康后启动前端4403172，再统一验收；不假设云端暂停能力 | 查询真实Flow与触发配置后执行，不把历史模板当当前配置 |
| F03错指测试文件N11；新异常未接各Controller错误包装 | 修正F03→N10；§3.7列出统一原因码及适配要求 | B08–B10验证HTTP状态，无关接口错误体不全局改 |

**仍须先闭合两项，不靠猜测补成“完成”：**
1. A01：用实际受测身份确认uid/jiacn/区域授权关系、统一filter在目标路由确实执行。UserService.findByJiacn只是DAO查询，不能据此声称user_info.tenant_id天然等于资金tenant；共享登录用户也不能因此误拒绝。
2. A02：真实user_info写入源如何协调、固定旧用户名单的执行点、原installer消费迁移/配置的具体接线。当前未核验存在通用业务DML hook。

金额口径继续沿用前文**聚义厅钱包资金**，不是user_info.point；若产品实际要改用户资料积分，必须先改目标和本方案，不能两边同时加2000。上述前置闭合后，按第7节进入实现；本次没有派发开发。

## 1. 本次只完成什么

沿用前文资金语义：“2000积分”指聚义厅现有可支付租金/悬赏的钱包资金，即 **2000 SILVER = 2,000,000,000 micro**，不另改`user_info.point`，不增加另一种积分或兑换系统。

1. 新用户完成认证，首次进入聚义厅或钱包，自动获得2000可用资金，无需点击领取、报价或先付租金。不是LDAP注册即发钱，也不是余额补齐至2000。
2. 新用户仍定义为本次启用截点后首次在CYF落库的`user_info`用户；截点前已有用户不再获赠，不以无钱包、余额0或第一次进入页面判断。旧309位补款及异常身份94不重做。
3. `tenant_id`代表业务区域。钱包及领取资格统一按`(client_id,tenant_id,user_id)`隔离，同一三元组只赠一次；不同client、不同tenant或不同user均不共用余额、资格或回执。本次仅发布到当前已有、明确配置且已完成资格基线的scope；具体tenant/client值不写入Java业务常量。
4. **不做跨client共享钱包或跨client领取互斥。** 同一user在client A的余额/领取记录不影响client B；B只有通过自身授权、配置和基线校验后才可按自身资格领取。未启用B时拒绝来自B的赠款，不读取A记录冒充B结果。沿用现账本scope及账户类型，不合并余额、不映射到固定client、不新增多客户端管理功能。
5. 多区域的钱包/赠款规则不在本次完整实现；不新增区域切换、区域管理、跨区转账、跨客户端钱包迁移、OAuth多租户签发重构、历史钱包整理或新的定时任务。
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

- 技术主键`PRIMARY KEY (id)`；业务防重唯一键`uk_onboarding_grant_user (client_id,tenant_id,user_id)`；交易引用唯一键`uk_onboarding_grant_transaction (tenant_id,client_id,transaction_id)`，匹配当前账本scope。client既是公共字段，也是**领取唯一键及钱包隔离身份的必需组成部分**。
- “默认字段”指公共字段，不等于赋固定默认值：tenant/client不写`DEFAULT '0'`或具体client，不能缺值回退；空白值在服务边界拒绝。时间由服务端明确赋值，原生mapper插入不能假设BaseEntity注解一定触发填充。
- claim查询、占位、状态更新及回放必须精确绑定client+tenant+uid；不跨client探查/复用资格，不使用tenant OR 公共0。其他scope存在同uid不构成本scope已领取或被排除；本scope仍须通过授权和基线校验。EXCLUDED仅在其三元组内生效，不覆盖、阻止或泄露其他scope的记录。
- POSTING：client/actor/campaign非空、amount>0（本期配置2000000000）、transaction/reason为空，仅在同一未提交事务中存在。金额由服务规则决定，DDL只约束合法正值，不把业务金额写成不可变schema常量。
- POSTED：client/actor/campaign/transaction非空、amount>0、reason为空；回放返回原实际金额。
- EXCLUDED：client为批准的基线目标client，amount=0，actor/transaction/campaign为空，reason=PREEXISTING_USER；不伪造零金额交易或用户注册来源。
- 不改现有account/transaction/entry/escrow主键，不复制旧309笔补款为新的POSTED。

### 3.2 复用原POST及记账服务

请求仍为`POST /economy/onboarding-grant {}`；用户、金额、tenant/client不接受body指定。

1. 校验用户token（拒绝machine）、规范tenant、可信client、uid与持久用户/归属；缺tenant不默认0。通过现有scope授权，确认本次配置及该client/tenant的旧用户基线已生效。
2. 按`(client_id,tenant_id,user_id)`读取资格；新建时严格INSERT获得行写锁，冲突回读使用同一三元组FOR UPDATE，详见3.4。EXCLUDED返回NOT_ELIGIBLE；POSTED核对完整scope/user及真实账本后返回原回执。其他scope的同uid记录不参与本次判定。
3. 在同一个REQUIRED事务中初始化原钱包/发行账户（余额0）、调用原treasury.issue，并写POSTED/真实transaction。记账仍为用户AVAILABLE +2000000000、系统SILVER_ISSUANCE -2000000000。
4. 固定用途`new-user-initial-grant`，确定性请求键由client+tenant+stable uid+固定用途生成，不随活动版本、金额或登录别名变化；client或tenant变化必定改变身份输入。编码固定为UTF-8 JSON数组`[clientId,tenantId,十进制uid字符串,"new-user-initial-grant"]`（标准JSON转义、无额外空白），对规范编码取SHA-256，沿用E02.deterministicUuid既有转换规则（前16字节、相同version/variant位设置、UUID.toString）得到36字符key，不直接存64字符hex；原economy_transaction.idempotency_key为VARBINARY(36)，CHECK要求36字节。request_hash仍为独立32字节摘要，不与key混用；不用裸分隔符拼接产生歧义。读取已POSTED时不拿新配置重算旧hash。
5. 原posting为REQUIRED，不独立提交；失败整体回滚。实际锁序为claim INSERT写锁 → 按AccountKey.LOCK_ORDER的零余额账户初始化锁 → 原交易幂等占位 → 原排序账户读取/CAS，不能省略初始化锁阶段。claim唯一冲突退出原事务，由非事务入口在独立代理的新事务中回读，详见3.4；不能在已被标记回滚的事务内假装继续。
6. 业务钱包身份为client+tenant+uid，现账本仍以scope+actor作为物理账户寻址：为领取过的新用户在同一三元组记录中固定claim.actor_id，将稳定uid映射为该scope的账本payer。actor不是第四个可由调用方选择的钱包维度，不跨scope复用绑定。钱包/流水、租金、悬赏付款入口通过共享资金身份解析回用该actor；仅解析资金主体，不改业务owner/ACL、不重写历史钱包。EXCLUDED且未绑定主体者沿用已有钱包身份；已有多主体归属冲突明确报错，不自动搬钱。
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
    UNIQUE KEY uk_onboarding_grant_user (client_id, tenant_id, user_id),
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
| `selectByUser(clientId,tenantId,userId)` | 精确client+tenant+uid读取；两个字符串均含OCTET_LENGTH匹配；无FOR UPDATE，用于资金主体读取 |
| `insertPosting(row)` | 普通严格INSERT，显式填写公共字段；成功才取得本次新行所有权。唯一冲突立即抛出并退出整个事务，不使用INSERT IGNORE或依赖affectedRows猜归属 |
| `selectByUserForUpdate(clientId,tenantId,userId)` | 同一精确键`SELECT ... FOR UPDATE`；事务锁序首位 |
| `markPosted(...)` | `UPDATE ... WHERE tenant_id=? AND user_id=? AND client_id=? AND actor_id=? AND status='POSTING'`；只改status/transaction_id/update_time，影响行数必须1 |
| `selectExcludedUserIds(clientId,tenantId)` | 精确绑定client+tenant，只读取该scope下EXCLUDED的uid，按数值升序；用于启用基线核验，不供前端查询 |

运行时mapper不提供删除、改client、改actor或POSTED→其他状态的方法。基线EXCLUDED插入只在版本化迁移中提供，不暴露HTTP接口。

**初始化与依赖方向必须明确：**当前E02.provisionIssuanceAccounts先用户账户、后系统发行账户；原`/home/isp/wsps/cyf/api/economy/jia-economy-api/src/main/java/cn/jia/economy/service/EconomyAccountKey.java`的LOCK_ORDER却按ownerType排序（SYSTEM在USER前）。将零余额初始化抽到N13，按同一LOCK_ORDER排列两个账户后调用原insertAccountIfAbsent；claim事务内调用时参与同一事务，不能REQUIRES_NEW。E02测试发行入口也复用N13，保留其原dev/test授权条件。N13不调用钱包/赠款服务、不发钱，避免WalletService↔GrantService循环依赖。

原E10的journal→sorted accounts锁序在其内部保持不变；新领取外层先初始化账户会更早取得账户锁，所以不能声明整个链路仍是原锁序。V01/V02必须覆盖多个新用户同时初始化同一个系统发行账户、已有账户发放与现有租金/悬赏并发；真实死锁只能整体回滚并给可重试响应，不能吞掉或部分提交。

`EconomyWalletService`保留非事务入口，委托独立Spring bean `EconomyOnboardingGrantService.claim(verifiedIdentity)`的公开REQUIRED事务方法。唯一冲突必须在该代理事务**完成回滚后**才由非事务入口转入另一公开REQUIRED方法`replayAfterConflict`；禁止同类self-invocation。简化顺序：

```text
非事务入口：校验认证/持久用户/当前scope授权和baseline ready
调用独立bean的claim，BEGIN REQUIRED
  selectByUser(client,tenant,uid)          // 非锁读，避免不存在行的gap锁升级
  若EXCLUDED：返回NOT_ELIGIBLE
  若POSTED：核对完整三元组和真实账本回执，返回replayed=true
  若读到已提交POSTING：报数据异常，不接管/补发
  若不存在：insertPosting(本次scope、uid、认证actor、2000)
            插入成功即取得本次claim行写锁；唯一冲突则抛出专用异常并ROLLBACK
  核对该固定用途账本key尚无交易；若已有交易但此前无claim，报错并ROLLBACK
  N13按原AccountKey.LOCK_ORDER初始化发行/AVAILABLE账户，余额初值0
  treasury.issue(确定性key，实际scope/actor/amount/campaign的hash)
  markPosted，affectedRows必须1
  返回真实transactionId/postedAt，replayed=false
COMMIT

仅在claim INSERT唯一冲突、上述事务已回滚后：
  非事务入口调用同一独立bean的replayAfterConflict，BEGIN新的REQUIRED事务
  selectByUserForUpdate(client,tenant,uid)
  POSTED核对scope/真实回执后返回；EXCLUDED返回不符合资格
  行不存在或已提交POSTING：明确报错，不在此分支补发
  COMMIT
```

只把claim INSERT的真实唯一冲突标记为可回读冲突（Spring DuplicateKeyException/明确MySQL重复键原因）；CHECK/NOT NULL、连接异常不能统统捕获成已领取。发行账户/账本的其他异常按原逻辑处理，不能一律吞成“已领取”。

POSTED回读须验证关联交易的tenant/client、USER principal/payer、ISSUE_SILVER、业务用途、金额及POSTED状态，并用原postedAt；取不到或不一致返回数据异常。并发不同登录别名请求在current()取快照时可能尚无claim，回读时须以**已提交claim.actor_id**核对账本，不拿竞争前快照中的旧payerId否定同client/tenant/uid的合法回执；认证uid/client/owner校验仍保留，不重读可变ThreadLocal。对“claim不存在但**本方案固定用途**的确定性账本key已存在”明确报错，不使用treasury的旧交易回放去伪造一条新claim（该状态违背同事务写入前提）；查询既有交易采用E18新增只读方法selectOnboardingTransactionsByKey：按精确client+tenant、包含同scope及uid的确定性idempotency_key、ISSUE_SILVER及固定business_id查询，不限定当前登录actor，以免漏掉同一三元组下不同登录别名的孤立记录；禁止省略client跨scope扫描，其他scope同uid的合法交易不构成冲突。仅内部核验，任何命中均报不一致，不向调用方暴露其他client回执；不使用FOR UPDATE，不新增通用写权限或全局唯一索引。它与旧1000活动用途不同，不能把旧活动转换成新活动。此检查在claim取得新行锁后、初始化账户之前执行。内部捕获重复键仅可立即重抛专用运行时异常用于回滚，不能在rollback-only事务内继续SQL。调用入口不得已有外层事务；B06通过Spring集成测试确认调用边界。真实死锁/连接中断回滚后返回现有可重试错误，由同一幂等请求重试，不新增无限重试循环。整个成功领取始终只有一个REQUIRED事务，不使用REQUIRES_NEW把账本独立提交。

### 3.5 统一租户上下文：业务入口不传tenantId，内部记账保留明确scope

**本版修正：统一复用已有请求上下文，不让各Controller自行拼tenant/client/uid，也不新增一套ThreadLocal。** 前版`MoneyIdentityInput(tenantId,...)`是内部设计参数，不是前端body；但放在业务入口容易造成重复解析和调用方自行选区域，现从公开资金身份接口删除。

#### 已核对的现有机制（2026-10-10，第2节API基线）

- `/home/isp/wsps/cyf/api/common/jia-common-service/src/main/java/cn/jia/core/context/EsContextHolder.java`已有ThreadLocal请求上下文；`EsContext`包含tenantId/clientId/jiacn/username，但没有uid和JWT sub。
- `/home/isp/wsps/cyf/api/common/jia-common-service/src/main/java/cn/jia/core/filter/EsContextFilter.java`先清上下文、读取CTX cookie，finally再清理；不能仅因为EsContext有值就当成已认证身份。
- `/home/isp/wsps/cyf/api/oauth/jia-oauth-resource/src/main/java/cn/jia/oauth/filter/EsSecurityContextFilter.java`从已认证JWT覆盖tenant/client/jiacn等字段。其注册配置`/home/isp/wsps/cyf/api/oauth/jia-oauth-resource/src/main/java/cn/jia/oauth/config/EsSecurityContextConfig.java`顺序为2；真实路由的过滤顺序及覆盖效果仍需用本功能集成测试验证。
- 该安全filter当前调用的TenantClaimPolicy仍有单租户legacy fallback；资金入口必须统一要求规范tenant_id存在，并核对上下文与JWT一致，不能仅读取回退生成的tenant=0。
- `/home/isp/wsps/cyf/api/common/jia-common-core/src/main/java/cn/jia/core/mybatis/TenantScopeHelper.java`及`/home/isp/wsps/cyf/api/common/jia-common-mapper/src/main/java/cn/jia/common/dao/BaseDaoImpl.java`部分查询采用“指定tenant OR 公共0”。**不能把该公共数据规则用于钱包/领取表**；资金中的tenant=0只能是一个明确业务区域，不能自动对所有区域可见。
- `/home/isp/wsps/cyf/api/common/jia-common-mapper/src/main/java/cn/jia/common/handler/FieldFillHandler.java`只自动填创建/更新时间。本次源码搜索未找到能保证全部SQL精确租户隔离的TenantLine拦截器；因此不能仅删除mapper参数就宣称数据库已自动过滤。

#### 业务调用方式（拟实现）

N04只暴露无参的当前资金身份接口和普通Java返回对象，不让economy-api依赖Spring Security：

```java
record ResolvedMoneyIdentity(EconomyScope scope, long userId,
                             String payerId, String ownerJiacn) {}
interface EconomyMoneyIdentityResolver {
    ResolvedMoneyIdentity current();
}

// 业务入口：统一取得当前身份，不接受调用方指定tenant/client/userId。
var identity = moneyIdentityResolver.current();
return walletService.claimOnboardingGrant(identity);
```

上例是设计，不是现有方法签名；E02的旧`claimOnboardingGrant(scope, actorId)`入口由此替换，不保留可由HTTP任意选scope的旁路。

- N05集中读取`SecurityContextHolder`中已认证的用户JwtAuthenticationToken和`EsContextHolder`。要求token_kind=user、规范tenant_id/client_id/uid/jiacn/sub合法；uid解析为正long；上下文tenant/client/jiacn必须与认证JWT一致。cookie-only、无上下文、未认证、machine、缺规范tenant、上下文与JWT冲突均拒绝，不能默认0。
- uid/sub从认证JWT取得，因为EsContext当前没有这两个字段；不为本功能扩大共享EsContext结构。经user-api核对持久uid/jiacn，并按A01确认的真实授权关系核对区域；不得未经确认直接断言user_info.tenant_id必须等于资金tenant。经济服务显式依赖`:user:jia-user-api`，不依赖user-service/agent-service。具体用户区域归属由A01核对，NULL client不是跨区授权。
- 同一个N05按完整client+tenant+uid查询并解析付款主体：本scope无claim/EXCLUDED沿用已认证actor；POSTED使用本记录claim.actor_id；已提交POSTING报数据异常；查出scope/user不匹配属于数据异常，不接受其他scope绑定。其他client有记录不影响本scope解析，未授权scope则在查询前拒绝。该接口纯读取，不发钱、不改账。
- 每个请求在进入资金事务前取得一次不可变identity快照；claim/重放/记账均使用该快照，不在事务中反复读取可变ThreadLocal。grant内部不再次调用current而把自己未提交的POSTING误认为污染，也不循环注入身份解析器和赠款服务。
- E05–E09统一调用该无参入口或接收其只读解析结果，删除各Controller重复拼装资金身份的代码；只替换付款主体，owner/订单/Agent授权不改，不全局替换所有sub。

#### 为什么mapper和后台仍保留tenant参数

| 层级 | 是否由业务调用方传tenantId | 设计 |
|---|---|---|
| 前端/HTTP DTO | 否 | POST仍为{}，不能自报区域或uid |
| 当前请求身份解析 | 否 | N05.current()统一校验认证和已有EsContext |
| 事务/记账命令 | 不传零散字符串；内部传已解析identity/scope | 固定本次tenant/client/payer，复用原EconomyScope；不让记账器隐藏依赖ThreadLocal |
| 底层claim/ledger mapper | 保留内部绑定参数 | 参数来自固定identity；SQL精确client+tenant，claim防重client+tenant+uid，不自动并入公共0 |
| schema/旧用户基线迁移 | 保留显式配置client+tenant | 没有用户请求上下文，必须绑定已批准配置及批次，不能伪造登录上下文 |
| 异步任务/后台扣款 | 不读取上一个HTTP线程的上下文 | 沿用持久订单/受信执行任务中的scope及授权；本赠款仍同步执行，不新增异步框架 |

“统一获取身份”和“全局SQL自动注入”是两件事。本次选择前者并保留现记账SQL的明确隔离，不扩成全项目ORM拦截改造。若以后全局统一SQL租户处理，必须覆盖手写SQL、插入、更新、join、批处理、后台任务及公共数据例外，另设范围，不能在本次顺手移除已有WHERE条件。

新增必要用例并入B04/B05/B11，不新增并行任务：JWT和cookie tenant冲突时以认证覆盖后的可信上下文为准；仅cookie无JWT拒绝；缺规范tenant即使旧filter回退0也拒绝；上下文与JWT仍冲突拒绝；同线程前后两次不同tenant请求无残留；异步无认证上下文调用current失败。请求退出清理复用现EsContextFilter，不能把ThreadLocal自动继承到线程池。

### 3.6 启用配置及基线完成判定

补齐原先“基线完成”过于抽象的实现：沿用E03配置类，新增`scopes`列表，每项包含`tenantId/clientId/baselineUserCount/baselineUsersSha256`。当前部署只填一个已批准的scope，Java没有生产标识常量。

- 发布配置amountMicro=2000000000；配置类只校验合法正long，不把必须等于2000000000写成启动常量。活动用途统一为new-user-initial-grant，删除外部可切换campaignRef的运营语义；旧配置项从本次配置中清理，不保留双活动实现。已有POSTED永远回原金额；测试模拟金额调整只能影响尚未领取者，不能重新发已领取用户。
- `enabled=false`只关闭赠款POST，不关闭claim表读取、已绑定payer解析或原钱包/租金/悬赏。POST返回专门GRANT_DISABLED；钱包读仍按原经济能力授权运行。旧用户以及已POSTED不因关开开关重新取得资格。
- N07表结构核验绑定现economy.preview启用条件，在E04显式确定初始化顺序（原五表schema → claim表schema → 基线readiness）；不能仅因赠款开关关闭而不创建claim表，却让所有钱包读去查不存在的表。N05先通过现经济scope授权，经济功能未启用时不访问claim表。schema缺失/不匹配是实际存储错误，不能当“未领取”。
- grant开启时scopes和固定基线证据必填，并同时满足原EconomyPreviewGate；配置以(clientId,tenantId)唯一，重复scope启动校验报错；允许同tenant下不同client独立配置，不增加一tenant仅一client的限制。当前生产仍只启用已批准scope，不自动扩大范围。基线readiness失败只使新赠款不可用，已有合法scope的资金读取/扣款不依赖grant ready；不以缺名单重跑全体排除。
- 启动时N07校验DDL后，按每个配置client+tenant分别读取EXCLUDED uid列表，并逐行校验完整scope及reason=PREEXISTING_USER；按`十进制uid + LF`逐行、升序、UTF-8计算SHA256，并比较该scope固定count/hash；摘要必须与client/tenant一同存储和校验，相同uid名单不代表两个scope共用资格。空名单只允许明确配置count=0和空字节摘要，不能缺配置当空名单。禁止GROUP_CONCAT摘要以免截断。
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
- 统一原因至少包括UNAUTHENTICATED→401、IDENTITY_OR_SCOPE_MISMATCH→403、GRANT_DISABLED→403、BASELINE_NOT_READY→503、CLAIM_OR_JOURNAL_INCONSISTENT→503、CONCURRENCY_CONFLICT→409。基线/数据不一致不标自动可重试，真实瞬时冲突才retryable=true；前端不自动循环。
- N04可在接口内定义轻量原因枚举/异常（无HTTP框架依赖）。E01显式转成本模块EconomyError，E05/E06转HostingRentApplicationException，E07/E08转FundedBountyException，E09按原预览接口约定转换；不能让新身份异常落入通用catch后全部变503。各接口保留原响应外壳，不新增全局ControllerAdvice影响无关业务。

## 4. 前端最小实现

- 聚义厅E13与钱包E14共用N10自动初始化：认证就绪 → 尝试POST赠款 → **无论赠款成功、旧用户或失败，身份仍有效时都继续GET真实钱包/流水**。grantError与walletError分开，赠款失败不能把已有余额变0或遮住可读取的钱包；401/身份切换则丢弃旧请求，不用旧身份继续读取。
- 同一client/tenant/稳定user_id/authorizationGeneration共享在途POST；不以localStorage领取标记作权威。每个组件有自己的订阅/代次检查；组件卸载只取消自身订阅，不直接abort其他组件共用的POST。共享请求仅在身份代次切换或无订阅者时可取消；取消不代表服务端一定未记账。
- Promise结算时仅当inflight.get(key)仍等于本次Promise才删除，防止旧请求finally清掉新请求。重入/刷新使用相同业务幂等，由服务器确认是否已经到账，不生成新活动key。
- 提示由共享方法按identity+transactionId合并，只对POSTED且replayed=false显示一次；两个组件拿同一结果不能各弹一次。文案金额从amountMicro精确格式化，当前应为2000，不硬编码到账金额；重试回放不弹重复到账。
- NOT_ELIGIBLE正常读取原钱包；GRANT_DISABLED只表示当前不发放，不显示“钱包不可用”。其他失败使用现有提示区域说明“赠款结果未确认”，允许显式重试，不新增定时器/无限循环。前端刷新保持所有金额为字符串/BigInt转换，不用浮点微积分。
- 删除E15初租不足领1000调用及E16领取UI；租金不足只提示，不自动充值、不自动确认租约。初始自动POST与租约动作解耦，不创建新租约/悬赏。
- F02/F03最低用例：双组件共享POST只一次；卸载其一另一仍可完成；任一client/tenant/user_id变化后的迟到POST/GET均丢弃，提示及钱包缓存亦按完整三元组隔离；POST失败但GET成功显示真实余额；关闭赠款后已有余额可读；相同transaction只提示一次。

## 5. 老用户处理与发布

### 5.1 基线与失败恢复（A02核定接线后实施）

1. 原发布锁/备份下协调实际user_info写入源停写；锁本身不阻止LDAP/OAuth/其他服务创建记录。不能停写或无法证明写入互斥时，此处阻塞，不能先扫描后任由用户在截点附近漂移。
2. 捕获启用前旧uid全集，先将**固定排序名单、count/hash、目标tenant/client、源码/批次**持久化到受控发布证据，再执行DML。共享登录用户不能因user_info.client_id为空漏掉；claim.client_id来自批准配置，不猜历史注册client。
3. 单事务插入EXCLUDED：只在本批批准client+tenant下按固定uid名单补缺；已有同三元组行须精确符合相同EXCLUDED记录，出现POSTED或不一致则失败调查，不覆盖。其他scope同uid行不构成冲突，也不更新它们。逐行核对后提交；绝不直接修改钱包余额。不能照搬309/310人数、最大ID或可空create_time。
4. 由已提交结果生成配置count/hash，并回读与固定名单一致。中断恢复必须使用第2步固定名单；不能重新扫描当前user_info而把上线后新用户排除。名单/提交状态无法确认则赠款保持不可用，不猜测“完成”。
5. 只初始化本次批准client+tenant，不广播其他scope。未来新增client或tenant须独立批准配置及资格基线，不自动从其他scope继承POSTED/EXCLUDED，也不把“首次进入新scope”当成新注册用户；其启用截点规则需明确后再发布。A02/M02必须列出上述步骤嵌入原installer的真实位置和恢复入口，当前未证明已具备。

### 5.2 单向发布依赖，不假设Flow可暂停

- 源码/制品准备阶段只固定后端build ID、候选前端commit、迁移及配置；develop合入/push不等于授权部署。发布前查询真实4403172配置及触发器，不能因仓内历史模板仍带push或固定Node就认定当前线上配置如此，也不能照抄恢复旧策略。
- **后端测试/制品PASS → 执行固定基线/配置并用原installer安装后端 → 后端最终回执及健康确认 → 启动前端4403172测试/构建/同Run制品部署 → 双端真实验收。** 不以“尚未拿到前端制品”为理由阻塞后端并同时又要求先发布后端才允许前端Flow。
- 若实际4403172仅产制品不含部署，仍用现授权部署入口消费该Run不可变制品；若含部署则让原Run完成。两者都不新增流水线、不本机生产打包、不重复构建。
- 后端完成但前端Flow失败时状态是“后端已发布、前端未完成”，不是整项成功；保留证据修复同前端范围。不反复发布未变化的后端，也不为回退页面而恢复旧1000赠款逻辑。新账本已入账时禁止回滚数据库/恢复旧发款活动造成二次领取；必要时关闭后续赠款并前向修复，已有余额/绑定主体继续可用。
- 新后端切换后旧缓存页面可能继续调用同POST：服务端必须执行新资格/幂等规则，不保留旧活动旁路。页面自动触发要等新前端上线；过渡阶段不宣称“新用户首次入厅自动到账”已完成。
- 本方案不执行迁移或补款。生产验收使用授权新测试用户；实际租金/悬赏消费需对应授权，不能擅自给旧账号再补一笔或新建订单。

## 6. 必要验收

1. 新用户首次入厅与直接入钱包各自可获得2000，并能被现租金/悬赏链路使用；余额不是只在前端显示。
2. 刷新、并发、响应丢失后重试、不同登录方式：同一client/tenant/uid仅一笔赠款且落入同一资金主体。
3. 老用户含已补款/旧1000/无钱包/空时间/修复异常身份，不再额外领取，原流水不动。
4. 当前配置以外的tenant/client、缺tenant、伪造uid均不获赠；合成非生产tenant值验证代码无固定0依赖，不据此宣称全站多区域可用。
5. 任一步故障回滚，无半笔余额或持久POSTING；真实MySQL验证并发/事务，复用已有测试设施。
6. 调整金额时已有POSTED回原金额；固定活动用途不能通过配置切成第二活动；租金不足/重新入伙/免费重整不再触发旧赠款；前端切身份无串账。
7. 公共字段完整写入且无固定scope默认值；技术id自增、client/tenant/uid唯一；同uid不同client、同client/uid不同tenant、同client/tenant不同uid三类隔离均验证：已授权且基线齐备的独立scope可以各领一次、各自记账，同一三元组重试只回原回执。某scope的EXCLUDED/POSTED不影响另一scope，未授权scope仍拒绝；重放不改原client/actor/create_time。
8. 统一current入口拒绝无认证/上下文不一致/缺规范tenant；CTX cookie不能选资金区域；请求清理无串租户，资金查询不使用tenant OR 公共0。身份错误在各资金Controller保持准确401/403而非泛化503。
9. 关闭grant仍能读原余额并沿原payer扣款；缺基线不发新钱、缺表不被当新用户。两个新用户竞争系统发行账户、赠款与付款交叉并发，锁冲突回滚无半笔账。
10. 基线DML前后/配置写入前后中断均可用固定原名单恢复，不扩大EXCLUDED。前端失败不影响读取已有钱包；共享请求卸载/迟到/提示去重符合§4。

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
| B01 | 后端/20分 | A01、§3.3 | N01 DDL + N02 entity，字段/索引/CHECK逐项一致 | diff与§3.3匹配；id主键、client/tenant/uid唯一，scope无固定默认值；补非法NULL/同三元组重复及不同三元组可并存用例 |
| B02 | 后端/20分 | B01 | N03五个mapper方法，仅claim表SQL | 所有写入显式公共字段；无通用delete/update；全部SQL绑定client+tenant，同uid跨scope不可互查或更新；补mapper用例 |
| B03 | 后端/20分 | B01、B02、A02 | N07 schema/baseline核验及E03/E04配置注册 | schema→baseline初始化顺序及count/hash用例齐；grant关闭不影响已绑定钱包；缺基线不发，不重建名单 |
| B04 | 后端/20分 | A01 | N04无参current接口、N05统一认证/EsContext核验；E11加user-api依赖 | 合法用户、缺tenant/machine/uid不符、cookie-only及上下文冲突用例齐；复用EsContext，无第二ThreadLocal或默认scope |
| B05 | 后端/20分 | B02、B04 | N05.current绑定资金主体的读取分支 | 无claim/EXCLUDED/POSTED/已提交POSTING及scope隔离用例齐；不改变业务owner；无写副作用 |
| B12 | 后端/15分 | B02 | N13按LOCK_ORDER零余额账户初始化，E02改为复用；不依赖WalletService/GrantService | 系统/用户初始化排序与原AccountKey一致；仅零余额建户；Spring依赖图无环，原测试发行授权不变 |
| B06 | 后端/25分 | B02–B05、B12 | N06单事务占位→N13初始化→issue→markPosted，校验无孤立固定用途交易 | 首次一笔两条分录、异常整体回滚用例齐；普通INSERT成功才获行所有权，唯一冲突回滚后新事务回读；无自调用事务失效 |
| B07 | 后端/20分 | B06 | N06重放/老用户/并发错误处理、固定幂等key/hash；E18只读固定用途key核验 | POSTED核对原交易用途/主体/金额/状态；金额调整不重发；固定用途不能改；不接管外部POSTING；不在rollback-only事务继续记账 |
| B08 | 后端/20分 | B07、F01 | E01接线N05/N06，E02删除旧campaign决定领取次数的分支 | §3.7成功/老用户/错误码及空body用例齐；无权不是503；wallet/ledger只读且统一current，无两个赠款实现 |
| B09 | 后端/20分 | B05 | E05和E06托管付款身份适配 | claim绑定payer贯穿报价/确认/续租；owner/租约ACL不改；admission/付款scope一致；身份异常映射原托管错误体 |
| B10 | 后端/20分 | B05 | E07/E08/E09悬赏与预览资金主体适配 | 同一用户别名变化不分裂新赠款钱包；两处悬赏Actor入口均覆盖；原owner不变；身份异常映射原各自错误体 |
| B11 | 后端/25分 | B08–B10 | N08及既有wallet/hosting/bounty测试；E11接入现有定向source set | 列明实际测试类/selector，新增用例确实在source set内；无未配置MySQL就把skip报PASS |
| F01 | 前端/15分 | §3.7，可与B01并行 | N09共享响应fixture及前端解析断言，与后端Owner确认同一合同 | POSTED/重放/NOT_ELIGIBLE/错误四类样例齐；micro用字符串不失精度，不改旧GET钱包单位 |
| F02 | 前端/20分 | F01 | N10共享自动领取composable，N11用例 | 共享请求订阅/取消归属及transaction提示去重明确；迟到finally不删新请求；无localStorage防重/循环请求 |
| F03 | 前端/20分 | F02 | E13/E14初始化接N10，grantError与walletError分开，沿用现UI | 入厅/直达钱包尝试POST后均读真实余额；POST失败/关闭仍能显示已有钱包；不假显示2000 |
| F04 | 前端/20分 | F03 | E15/E16删除初租领1000及按钮，更新E17 | 租金不足/重整/重入伙无赠款调用；新手初始化之外无遗留触发；仅定向本地诊断非正式Flow证据 |
| M01 | 后端/25分 | A02、B01 | N12迁移SQL/固定旧uid输入格式、count/hash及核验步骤 | 名单先持久化再DML；提交/配置中断仅用原名单恢复；EXCLUDED只补缺、POSTED不覆盖；无人数/最大ID捷径 |
| M02 | 主控/25分 | M01、B03、A02 | 按A02核定位置做本次原installer/配置最小接线，新增受影响工具测试 | 固定配置接收迁移真实count/hash；接线失败不启动赠款；原锁/备份/回执不绕开。若需超出本次补丁范围，明确拆子片而非标完成 |
| V01 | 后端/25分 | B11、M01、MySQL可用 | 真实MySQL同三元组并发防重及跨client/tenant/user隔离回归 | 同client/tenant/uid仅一笔，独立已启用scope互不影响；不同uid竞争发行账户及赠款/付款并发有回归；真实账平，报告无skip证据 |
| V02 | 后端/20分 | V01 | 回滚、旧用户基线、别名变更及租金/悬赏受影响回归 | 注入异常无半笔资金；新余额可供原付款链路使用；旧余额不动；失败精确归因不重跑无关测试 |
| V03 | 主控/10分主动操作 | V02、M02、固定候选 | 经原编排器提交后端正式测试/validateLayering/制品构建，记录build ID/日志 | 提交回执不等于构建成功；最终所需任务PASS及fresh JAR SHA由W01回收；等待不占30分承诺 |
| V04 | 前端/10分主动操作 | F04、W03后端已安装健康 | 按核验后的当前配置提交前端4403172测试/构建/同Run制品部署，记录Run/commit | 不假设能暂停部署；后端先就绪；不得本机生产打包；等待和实际部署结果由W02记录 |
| R01 | 主控/20分主动操作 | W01后端制品PASS、M02、原生产授权 | 锁/备份下按§5.1固定旧uid、执行基线、核验配置并用原installer部署后端 | 仅后端发布步骤；实际迁移/同批回执由W03确认，然后V04前端发布；不抢锁/不强杀 |
| R02 | 主控/25分 | W03后端健康、W02前端部署成功 | 授权真实新账号自动到账/刷新防重/钱包和账本核对；已有账号不再领 | 截图/API/SQL证据对应当前版本；若测试实际消费须覆盖授权，不擅自下单/再补旧账号 |
| R03 | 主控/10分 | R02 | 回写本文状态、现handoff及稳定知识入口 | 分别列源码、测试、制品、部署、线上验收；未完成项有Owner/下一动作，不用阶段总结代替继续推进 |

所有任务的“补用例”都须在V01/V02及正式构建中取得对应执行证据才能完成整体开发验收。A02/M02为已知不确定项，不能用尚未核验的安装能力承诺30分钟必达。

### 7.3 异步等待不是伪造的半小时任务

| 等待项 | 对应操作 | 关闭条件 | 期间如何推进 |
|---|---|---|---|
| W01 | V01/V02测试及V03后端构建 | 先有对应真实测试结果，后有同build ID测试/分层/依赖检查通过、fresh制品和SHA齐 | 同Owner跟踪真实日志；前端/迁移文档可继续，不重复启动Gradle |
| W02 | V04前端Flow及原部署入口 | 同Run测试/制品/部署成功且源码匹配；后端已由W03确认 | 查原Run，不新建流水线、不取消他人任务；失败按根因修复 |
| W03 | R01后端安装/健康 | 后端原installer最终回执及版本/健康一致，随后允许V04 | 按原恢复协议处理，不按30分钟强杀；无回执不标发布完成 |

没有在本次新建定时监控或启动等待任务。真正执行时沿用既有跟进方式，完成/失败/需用户操作时通知；不承诺无自动化支撑的后台定时监测。

### 7.4 总量与依赖

- **27个主动工作切片，每项10–25分钟，共525分钟（8.75人时）**。其中后端315分钟、前端85分钟、主控125分钟。B12仅拆出原来漏算的共享账户初始化工作，不增加新业务功能；本次三元组修订纳入原B01–B07/M01/V01/F02–F03切片，不新增跨client共享钱包工程，估时仍为规划值。该值是实现/定向核验/发布操作的规划投入，不包含不可预知的外部排队、构建运行及异常修复。
- 后端链：A01 → B01/B04 → B02/B05 → B03/B12 → B06/B07/B08 → B09/B10 → B11 → V01/V02 → V03。同一API Owner串行；依赖表达允许先补接口，不声称依赖未就绪的集成已通过。
- 前端链：F01 → F02 → F03 → F04与后端实现并行；V04必须等W03后端安装健康。迁移链A02 → M01 → M02：M01属API源码，由后端Owner在其worktree写迁移SQL；主控只负责A02设计及根仓E12安装接线，不与后端共写同一API工作区。生产动作仅R01执行。
- 汇合：V03/W01 + M02 → R01/W03 → V04/W02 → R02 → R03；没有R01等W02、V04又等R01的循环。
- **按前后端各一位Owner、主控并行准备安装接线，主动工作及集成暂按6–8小时规划**；前端正式Flow在后端就绪之后串行执行，其运行/排队时长另外记录，因此本数不再表述为保证6–8小时全部上线。前版4–6小时偏乐观：细拆后明确计入schema/基线核验、共享资金身份接线及原installer适配，不是新增多区域功能。A01/A02发现无需某接线时可删除对应工作并下调，不能为了保持旧估时省掉必做项。

## 8. 文件与方法落点（现有/拟新增严格区分）

现有行号绑定第2节API/Web基线，开发后按方法名定位；未标现有行号的新类均是**拟新增**，不虚构已存在实现。

| 代号 | 绝对路径及落点 |
|---|---|
| E01 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletController.java`：88–101领取；156–173 requireSubject改为委托统一current；wallet/ledger共用资金解析 |
| E02 | `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletService.java`：109–149旧grant/幂等辅助；156–172账户初始化抽到N13；61–86钱包/流水 |
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
| E18 | `/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/java/cn/jia/economy/mapper/EconomyLedgerMapper.java`：新增仅用于固定用途幂等key完整性核验的只读查询，原账本写保护不改 |
| N01 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/economy-onboarding-grant.sql` |
| N02 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-core/src/main/java/cn/jia/economy/entity/EconomyOnboardingGrantClaimEntity.java` |
| N03 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/java/cn/jia/economy/mapper/EconomyOnboardingGrantClaimMapper.java` |
| N04 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-api/src/main/java/cn/jia/economy/service/EconomyMoneyIdentityResolver.java`（§3.5无参current接口及嵌套只读结果，不暴露MoneyIdentityInput） |
| N05 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyMoneyIdentityResolverImpl.java` |
| N06 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyOnboardingGrantService.java` |
| N07 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyOnboardingGrantSchemaInitializer.java`，复用原schema解析规范，仅该表和固定基线校验 |
| N08 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/test/java/cn/jia/economy/service/impl/EconomyOnboardingGrantMySqlTest.java`与`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/test/java/cn/jia/economy/service/impl/EconomyMoneyIdentityResolverTest.java`；复用现`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/test/java/cn/jia/economy/config/EconomyMySqlTestFixture.java` |
| N09 | 拟新增`/home/isp/wsps/cyf/web/tests/fixtures/onboarding-grant.json`，作为前后端一致的响应例子，后端测试按同合同断言，不让API生产依赖Web仓文件 |
| N10 | 拟新增`/home/isp/wsps/cyf/web/src/composables/useOnboardingGrant.js` |
| N11 | 拟新增`/home/isp/wsps/cyf/web/tests/onboarding-grant.test.js` |
| N12 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-mapper/src/main/resources/db/migration-onboarding-grant-baseline.sql`，绑定固定旧uid输入；真实凭据/用户清单只放受控发布证据，不提交Git |
| N13 | 拟新增`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/service/impl/EconomyIssuanceAccountProvisioner.java`；仅mapper依赖、原LOCK_ORDER、零余额初始化；供E02/N06复用 |

## 9. 验证入口及证据要求

- 文档本次仅做路径/行号/合同/依赖及任务时间检查，不执行应用测试、DDL、构建或发布。
- 实施沿用`/home/isp/wsps/cyf/ops/orchestration/README.md`，所有Gradle操作先读当前相关build.gradle，经`/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle ...`串行执行；真实任务ID先在现ledger登记，不拿A01/B01设计编号假冒运行任务。
- B11明确把N08及原WalletController等必要测试纳入实际source set；现`:economy:jia-economy-service:economyHostingRegression`仅含原列出的测试，新文件不自动被执行。依赖编译/validateLayering/原账本保护均保留。
- 真实MySQL fixture/凭据按已有说明复用；未连接时的skip不是并发PASS。正式前端测试/生产打包/制品使用4403172；本地test只作诊断。
- 一份输入匹配的成功证据可复用，必要键包括源码tree、selector、fixture、工具链；没有证据不靠“应当通过”报完成。前端版本实际记录，不恢复Node精确版本门禁。
- 每项在现handoff记四栏：`输出或commit | 验证命令/结果或待验证 | 主动耗时/等待 | 下一动作/阻塞Owner`；不另建监控平台或重复台账。
