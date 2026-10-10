# 新用户默认2000资金：实施方案

修订日期：2026-10-10。Owner：主控（方案）；开发尚未派发。状态：**已纠正硬编码方案；多业务区域的资金共享/领取边界待确认，DDL尚不可直接实施；未实现、未迁移、未发布**。

## 1. 业务规则（资金作用域见1.1，尚未全部冻结）

1. 赠送 **2000 SILVER = 2,000,000,000 micro**，进入用户可用钱包；不是把余额重置为2000，也不是2000元现金，不改user_info.point。
2. 新用户定义为：规则正式启用、旧用户基线固定后，首次在CYF落库的user_info用户。已有登录账号但首次在CYF落库者按新CYF用户处理；不是仅凭“没有钱包/余额0/第一次租用”判断新用户。
3. 发放时机：用户完成认证首次进入聚义厅，或直接进入钱包时，客户端自动调用既有POST。无需领取按钮、报价或先付租金。仅完成LDAP注册、未进入CYF，不提前发放。
4. 同一稳定用户在确认后的赠款作用域内仅一次，不能将OAuth client天然当作赠款作用域。tenant/client由可信认证上下文取得，允许范围由服务端配置提供；`tenant=0 / client=jiafewnnv58ec2379c`仅是当前部署实例值，不是Java业务常量、默认兜底或通用迁移常量。原“每个client领一次”的规则撤回，主键待1.1中的业务语义确认。
5. 已存在用户不因本次规则再得一笔钱；已批量补过2000的309位保持原余额与流水。旧用户即使没有钱包也不领；异常身份94不猜身份、不补款，修复身份后也不自动变成新用户。
6. 刷新、重新登录、换登录方式、余额花完、再请好汉、除名重入伙、免费重整均不重复赠送。费用仍分别由用户确认，不自动替用户租赁或下单。
7. 删除旧“初租不足自动领1000”逻辑。只保留一个初始化赠款入口，不并行运行新旧活动；不新增充值、运营活动、定时发钱或后台管理功能。

## 1.1 多业务区域：身份边界与待确认项

**本次明确修正，不扩建区域管理平台：**

- `tenant_id`是认证与数据隔离边界；`client_id`是OAuth接入应用身份；业务区域是产品概念，三者不自动等同。同一区域可能有Web/App多个client；一个client也可能服务多个区域。
- 后端统一从已验证用户JWT读取规范`tenant_id`和可信`client_id`，并校验用户对目标作用域的权限。请求body保持{}；不能通过请求参数/前端存储自报tenant或区域绕过权限，缺失tenant不默认成`0`。
- 复用`EconomyPreviewProperties.allowedScopes`及`EconomyPreviewGate`对认证tenant/client的精确授权；启用赠款还需匹配其资格基线。开放另一个client不能自动创建新赠款资格。无配置、缺资格基线或未授权scope明确失败，不以多区域为由取消隔离。
- 复用`TenantClaimPolicy`的规范claim名称及合法性校验，但资金路径必须要求规范claim存在，不调用带单租户兜底的旧解析方式。现有`resolve`接受别名/单租户回退，因此不能原样调用后声称已消除回退。
- 当前OAuth签发器可由构造参数给定租户，但也保留默认单租户构造；尚未证明它能按请求可信地签发多个租户。未来多租户须同时核验签发端、资源端和用户租户归属，不能仅替换钱包里的字符串就宣称完成。

**唯一待确认的产品决定：不同业务区域共享钱包及一次赠款，还是各区独立钱包、各领一次？** 同一区域多接入端不应因client变化重复领取。

- 若各区独立：建议用稳定`business_scope_id`标识区域，赠款防重候选键为`(tenant_id,business_scope_id,user_id)`；client只参与接入授权/审计，由可信服务端上下文及受控映射选择区域。若一个client覆盖多个区域，区域选择协议及授权必须另行明确，不能猜一个默认区域。
- 若各区共享：按确认的共享资金域防重，不能把区域/client放进主键导致重复赠款。跨租户不自动共享资金。
- 现有账本仍以`(tenant_id,client_id)`隔离，单改领取表为区域键不能实现钱包共享。若选择多client共用资金域，须同步明确账户、交易、托管及悬赏scope解析，评估字段/迁移改动后才能冻结DDL；本次不擅自合并已有钱包，不静默将账本client重新解释为区域ID。
- 第3节保留原表结构以供差异评审，**不是批准继续按client维度建表**；第4、7、8节涉及scope的处理/迁移/测试均以最终确认的资金域为准。新增区域时旧用户是否重新算新用户也须随上述规则冻结，不能由“新scope没有claim”自动推导可领取。

## 2. 核验基线与问题

2026-10-10 11:05 CST真实ls-remote：API develop `33e2344a2af02bb908a20bec1125ab7c23e8d00d`；Web develop `17ecf1c0b581cab1456acff4db097a6a4d335e3d`，与本地HEAD一致。本次仅源码/历史证据核对，未重新执行生产资金查询。

- `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletService.java:109–149`：已有POST对应发放服务及确定性幂等；键含campaign，hash含amount。同campaign改金额会冲突；换campaign会允许旧用户再领。
- 同文件61–72、156–172：钱包读取与发行账户创建分开；账户初值0，必须经现有复式记账增加余额，不能改DEFAULT或GET偷偷发钱。
- `/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletController.java:88–101,156–173`：现有POST只收{}；钱包身份目前用JWT sub，需要新增uid持久用户核验。
- `/home/isp/wsps/cyf/api/oauth/jia-oauth-service/src/main/java/cn/jia/oauth/security/AccountSecurityTokenCustomizer.java:45–53`：用户token已有uid/jiacn；不能信任前端localStorage.userId。
- `/home/isp/wsps/cyf/web/src/composables/juyiting/useHostingRent.js:47–48,82–92,194–199,286–293`：现在仅初租报价不足才领；必须从租赁流程移出。
- 历史补款证据与身份例外保留 `/home/isp/wsps/cyf/docs/implementation/NEW-USER-2000-GRANT-ANALYSIS-20261010.md`，不把旧补款当本方案已实现。

## 3. 数据设计草案：原client维度待修订，禁止直接执行DDL

以下为修订前单client草案；主键、交易引用scope及基线维度须依1.1确认后一起更新，不能只替换字段名。

表：`economy_onboarding_grant_claim`，InnoDB、utf8mb4_0900_bin，与现行经济表一致。它只记录资格及真实交易引用，不形成第二套账本。

| 字段 | 类型/约束 | 含义 |
|---|---|---|
| tenant_id | VARCHAR(50) NOT NULL | 可信租户 |
| client_id | VARCHAR(50) NOT NULL | 可信客户端 |
| user_id | BIGINT NOT NULL，>0 | user_info.id；不能用可变登录别名作防重键 |
| status | VARCHAR(16) NOT NULL | POSTING / POSTED / EXCLUDED |
| actor_id | VARCHAR(100) NULL | 发放钱包的固定payer主体；EXCLUDED可空 |
| transaction_id | VARCHAR(100) NULL | 原ISSUE_SILVER真实交易ID |
| amount_micro | BIGINT NOT NULL DEFAULT 0 | 已发金额，绝非当前余额 |
| campaign_ref | VARCHAR(100) NULL | 审计标签，不参与终生一次主键 |
| reason_code | VARCHAR(32) NULL | EXCLUDED固定PREEXISTING_USER |
| create_time | BIGINT NOT NULL | 服务端毫秒时间 |
| update_time | BIGINT NOT NULL | 服务端毫秒时间 |

主键 `(tenant_id,client_id,user_id)`；唯一键 `(tenant_id,client_id,transaction_id)`，允许多个NULL。状态CHECK：
- POSTING：actor非空、amount=2000000000、campaign非空、transaction为空、reason为空；只在未提交事务内存在。
- POSTED：actor/transaction/campaign非空、amount>0、reason为空；重放返回存储的真实金额。
- EXCLUDED：amount=0、transaction/campaign为空、reason=PREEXISTING_USER；不虚构“0元POSTED”交易。

**旧用户统一写EXCLUDED，不复制/重写309笔旧补款为新赠款。** 历史资金继续由原账本证明，减少一次性映射与兼容分支。与早期分析建议的“309位回填POSTED”相比，这一版明确选择更小的排除基线方案。

新增表由版本化迁移创建、验证精确catalog；不改变现有economy_account、transaction、entry、escrow字段和余额。

## 4. 服务端处理顺序

复用 `POST /economy/onboarding-grant`、请求body严格{}。用户、金额、活动、scope均不允许客户端指定；GET wallet/ledger继续只读。

1. 校验用户JWT、现有scope/ACL/开关；解析合法uid，通过UserService核对持久用户id/jiacn/租户，拒绝machine token、缺身份/串身份。user_info.client_id为空的共享用户不能仅因此被拒绝，但必须依据可信身份核验租户/作用域归属，不能从NULL推导其属于任意租户。请求tenant/client必须匹配配置允许范围和已初始化的赠款资金域。
2. 身份与钱包必须一致：新增共享资金身份解析接口，返回stable userId与canonical payerId。新用户第一次发放时固定payerId到claim.actor_id；后续登录别名变化回用该payerId。钱包读取/流水、托管租金及悬赏付款共同消费该解析结果。只归一经济付款主体，不改业务owner/权限及用户登录sub，不自动合并历史钱包或搬迁在途订单。
3. 在一个REQUIRED事务里读取/占位claim并锁行：EXCLUDED直接返回不符合资格；POSTED直接回读原回执，不使用新配置重算旧hash；不存在才创建POSTING。
4. 创建原AVAILABLE/发行账户（余额0），调用原EconomyTreasuryPostingService.issue。固定新发放campaign `new-user-initial-grant`；确定性请求键按scope+stable userId+固定用途生成，不随版本、金额或登录别名改变。
5. ISSUE_SILVER沿用现模板：USER/AVAILABLE +2000000000，SYSTEM/SILVER_ISSUANCE -2000000000；两条分录及余额/version一起提交。
6. claim改POSTED并绑定同一真实transaction；任一步失败整体回滚，包括账户初始化。已有posting使用REQUIRED（EconomyPostingServiceImpl.java:101–104），不能改为独立提交或异步发钱。
7. 并发只允许一个claim获胜；其他请求等行锁后回读。锁序：claim → 原交易幂等占位 → 原有排序账户锁；不得先锁钱包再反向锁claim。
8. 发现已提交POSTING、claim/交易不一致、多个历史钱包主体归属不清时返回明确错误并调查，不自动再次赠送、补差或迁移。不能以“只保证不重复赠送”为由放任新用户赠款与扣款进入不同钱包。

响应统一HTTP200业务结果（金额和时间用十进制字符串）：
- `status=POSTED`：transactionId、amountMicro、campaignRef、postedAt、replayed；原POSTED返回同transactionId/金额，replayed=true。
- `status=NOT_ELIGIBLE`：reasonCode=PREEXISTING_USER、amountMicro="0"、transactionId=null，不当网络故障。
- 身份403、未登录401；配置/服务暂不可用维持明确失败。不返回“假成功、稍后肯定到账”。

`economy.onboarding-grant.amount-micro=2000000000`；固定用途标签不再可作为绕过一次性领取的运营开关。修改金额不会重发已有claim；本次不增加可变活动系统。

## 5. 前端触发与删减

- 新增一个小型共享初始化composable；挂接 `/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue` 现身份就绪/authorizationGeneration生命周期，以及 `/home/isp/wsps/cyf/web/src/components/Wallet.vue:74–102` 钱包初始化。
- 已认证且能力允许后自动POST，随后GET真实钱包；多个组件同身份合并在途请求。重新载入可再次POST，由服务器防重；不把localStorage已领标记当权威。
- 身份切换、退出、卸载取消旧请求并丢弃迟到响应；必须在新身份下重新核对。
- POSTED显示一次“启动资金2000已到账”（回读旧回执不反复弹）；NOT_ELIGIBLE正常继续读取原钱包。
- 失败不妨碍浏览聚义厅；钱袋使用现有错误/重试区域提示“启动资金尚未确认到账”，不伪造余额、不自动循环请求。
- 删除useHostingRent的needsOnboardingGrant、claimGrantForQuote、claimOnboardingGrant及报价后的赠款调用；删除 `/home/isp/wsps/cyf/web/src/components/juyiting/HostingRentPanel.vue:54,56` 对应自动领钱/重试领钱UI。租赁余额不足只提示，不补钱、不换为免费local、不自动确认报价。
- 钱包与流水现有页面继续使用，无新页面/新公共发放API/定时器。

## 6. 实现落点

后端Owner一次性负责：
- economy-core/mapper：claim entity/mapper/DDL/精确schema验证；现有ledger mapper保持原写保护。
- economy-api/service：共享资金身份接口与实现（用户核验复用user-api，不跨模块直连user mapper）、独立claim事务服务、WalletController响应/uid校验、WalletService委托、原grant配置及测试更新。
- 资金身份调用点：WalletController、HostingRentHttp.actor及托管admission principal、FundedBountyActor的付款主体构造、EconomyReadOnlyPreviewController的钱包主体；逐个保留现owner/client/tenant授权，不全局替换actor字符串。正式实现需列出实际调用点diff，不能只改wallet读路径。
- 必改已确认硬编码：`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/api/EconomyWalletController.java:156–173`中的`new EconomyScope("0", client)`；`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/hosting/HostingRentHttp.java:31–55`的`tenantId must be 0`校验及actor构造中的`"0"`。统一改为可信规范tenant解析，并保留client/owner权限校验；其余资金调用点仍需定向核对，不声称已查全。
- 已核对可复用入口：`/home/isp/wsps/cyf/api/common/jia-common-core/src/main/java/cn/jia/core/security/TenantClaimPolicy.java`；配置入口为`/home/isp/wsps/cyf/api/economy/jia-economy-service/src/main/java/cn/jia/economy/config/EconomyPreviewProperties.java`。本次仅文档修订，未改这些源码。
- 不更改OAuth签名机制，不新造第二身份体系，不为历史分裂钱包进行自动重写；签发端租户选择能力未核验完整，不列为已具备。

前端Owner只负责上一节路径与相应测试，双方共享响应fixture；不增设Reviewer。

## 7. 旧用户基线与发布顺序

- 本轮没有执行以下步骤。实施时按固定版本/源码/制品、原发布锁及备份进行，前端Flow4403172、后端本地原安装器；不建设新发布框架。
- 基线迁移显式接收已批准的资金域及认证scope配置并记录摘要；脚本不得写死当前tenant/client，也不得向全部租户批量广播EXCLUDED。第1.1未确认之前不执行建表/基线迁移。
- **资格截点必须与实际用户创建写入串行**：使用原API停止到新API启动之间的发布窗口，确认其他user_info写入源也已协调停止；固定此时全部旧uid，在同一数据库事务写入EXCLUDED并记录集合摘要。含本次补款后至上线前新增的用户；绝不照抄310/309人数、旧最大ID或只看可为空的create_time。
- 发布锁本身不锁数据库注册写入；如其他创建源不能暂停，必须实现并核验数据库级一致快照/写入互斥后再激活，不能宣称只靠发布锁消除了竞态。该安装前置步骤需接在原安装流程，未核实其现有hook可用性，不冒称已具备。
- 固定排除基线成功后才允许新POST逻辑服务；旧1000实现不再提供服务，再上线同步前端。不存在则新建claim的前提是这份初始化证据已校验；空表/基线未完成不得放行赠款。
- 失败按原回执处理，禁止重新扫描全部用户覆盖claim；只允许对固定原基线幂等补齐缺行，已POSTED不可改成EXCLUDED。后续正常升级不重建旧用户基线。
- 必须保留一次性版本迁移SQL及审计证据；它是部署必需迁移，不新增长期运行的历史兼容分支/后台补款功能。
- 不回滚已POSTED账本、不恢复数据库快照覆盖新交易；开关关闭只暂停后续发放。直接切换新契约，不做双写/兼容层。

## 8. 验收及交付切片

最低验收：
1. 普通及第三方新CYF用户首次入厅/直达钱包获得2000；同一用户不同登录方式看同一钱包，赠款能走原租金/悬赏路径。
2. 并发、刷新、重复登录、请求已提交但响应丢失：一个claim、一笔ISSUE_SILVER、两条平衡分录；返回同原交易。
3. 老用户含已补2000/已领旧1000/无钱包/NULL时间/修复异常身份：均不额外发；原余额/旧流水不改变。
4. 改活动标签/应用版本/金额不导致已有用户再领或旧hash冲突；前端自报uid/金额/未经授权的跨client均拒绝；合法的不同client按配置授权，不能一概拒绝。
5. 领取任一步故障回滚无半笔资金；未生效基线不放行；真实MySQL并发证明事务/唯一锁，不仅H2替身。
6. 重新入伙/免费重整/租金不足均无赠款POST；新资金初始化不自动创建租约/事项/悬赏。
7. 前端身份切换丢迟到数据；失败可重试、界面不显示本地捏造2000；现wallet/hosting受影响回归通过。

8. 使用不同于生产值的两个tenant/client配置验证无业务常量依赖；缺规范tenant、伪造/越权tenant、未授权client不得落入默认租户。按最终资金域规则覆盖同一区域多端不重复领取、不同区域共享或隔离钱包、基线不串域；既有赠款/钱包/租金/悬赏使用一致scope。

拆分为单项不超过30分钟的**工作目标**，不是未实测工期承诺：
- A：先确认1.1的资金域规则，再冻结DTO/DDL/共享fixture，验证现身份入口、硬编码移除范围及原安装前置hook。资金域未确认不进入建表实现，不沿用旧client主键。
- B：claim mapper/事务/一次性幂等与单元测试。
- C：资金身份解析与wallet/hosting/bounty一致接线。
- D（可与B/C并行）：前端初始化及删除旧赠款分支。
- E：真实MySQL并发/回滚/旧用户基线与联调回归。
- F：版本化制品/迁移/发布/真实新用户验收，耗时另记，不把开发完成当上线。

实现前若A发现历史身份归属冲突，只报告精确受影响账户及处理方案；不扩成本轮全量身份/历史流程重构。生产新用户及资金验收使用明确授权的测试账号，不擅自给老账号再次加钱。
