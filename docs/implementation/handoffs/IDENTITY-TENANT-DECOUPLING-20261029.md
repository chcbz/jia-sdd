# 身份与业务租户解耦：全库盘点与迁移设计

> 最新状态：代码已于2026-10-29合入develop（bff21501a3），定向云端回归实际222项通过；制品已下载核验，生产迁移/安装/删列尚未执行。正式证据与剩余动作见文末最新节；下方早期状态保留追溯。

## 基线与状态

- 日期：2026-10-29，Asia/Shanghai。Owner：本线程主Agent；任务ID：IDENTITY-TENANT-DECOUPLING-20261029。
- 用户目标：删除 `user_info.client_id`、`user_info.tenant_id`、`oauth_client.tenant_id`；全量分析现有表，区分身份、应用注册、业务分区，不建设动态多租户平台。
- 本轮远端develop核对：API `a5f28ec1dd84c33217e30ff748de898bc50c2f07`，tree `f4d74ad8eddbae0d4029b972305441a6d74432d2`。不是前轮ffc5。本地HEAD仍516267bf且有其他Owner大量未提交内容，分析读取固定Git对象，不覆盖工作树。
- 约束：`/home/isp/wsps/cyf/AGENTS.md`、`/home/isp/wsps/cyf/ops/orchestration/README.md`、接口规范v1.4、RB-1；Flow仅worker重型测试/构建/上传，主机独立安装，每Run600秒，不重复计费。本轮未启动Flow。
- 当前状态：**全量结构盘点及重点依赖分析完成；应用代码改造、迁移回归、实际删列均未完成。** 未改数据库、未发布/重启；没有把灰度测试要求加回给用户。
- 不在本轮范围：死锁/重连、恢复旧runner、全项目取消client作用域、删除历史审计或备份。

## 盘点覆盖

本机MySQL业务库 `jia` 244张基表+1个视图，`jia_dev` 107张基表+1个视图，总353个对象。读取全部列、索引、外键、触发器/存储例程/事件和视图定义，并建立固定源码主代码/资源中的精确表名引用索引。系统库未列入，其他主机未扫描。

逐表清单：`/home/isp/wsps/cyf/docs/implementation/handoffs/IDENTITY-TENANT-DECOUPLING-20261029-INVENTORY.md`。
私有证据：`/home/isp/state/cyf-identity-decoupling-20261029/`，包含 `inventory.json`、`columns.tsv`、`indexes.tsv`、`foreign-keys.tsv`、`database-programs.tsv`、`all-table-source-references.txt`、`identity-data-aggregates.tsv`。

**全量结构覆盖不等于所有运行链路已审完。** 逐表分类明确标记待核范围；未发现精确表名引用不等于表已退役，ORM/外部服务可能间接使用。没有以行数估计值或表名推断线上流量。

## 已确认的直接影响

### A. 目标三列不能先从运行库删除

- `UserEntity`、`OauthClientEntity`均继承`common/jia-common-core/.../BaseEntity.java`，父类持久化tenantId/clientId。单改DDL仍可能由MyBatis通用SELECT/INSERT/UPDATE访问被删列。
- `user/jia-user-mapper/.../UserInfoDaoImpl.java:105-117`用户列表仍追加user_info的tenant/client条件。不能简单删过滤条件扩大列表权限；全局身份管理员与业务成员查询须分开，后者通过同域关系表关联。
- `oauth/jia-oauth-service/.../AuthorizationServerConfig.java:131`读取client.getTenantId，交给`AccountSecurityTokenCustomizer.ClientTenantLookup`签发令牌。先删列会破坏登录/刷新链路。
- `/user/my`当前租户0返回UserEntity，灰度返回含环境上下文的CurrentUserIdentityDTO。需分离用户资料与当前会话的业务scope，兼容前端identityScope缓存键，不能因去列导致换环境复用生产缓存。
- 基类DAO `BaseDaoImpl.selectByEntity/applyTenantScope`存在`tenant_id = requested OR tenant_id = '0'`语义。这里的0同时被历史代码当作公共目录、又是生产分区。不得将该通用逻辑用于灰度业务查询；公共目录共享必须显式限定，不能自动把生产行当公共行。
- 历史`migration-tenant-default-zero.sql`仍引用目标列。历史脚本保留追溯但须从新库安装/当前迁移入口排除或由新基线取代；不得重跑旧脚本把列加回来。

### B. user_info混入业务状态，不是纯身份表

只读汇总：jia.user_info共311行，tenant全为0，其中7行client_id非空；201行point非零。没有输出账号、电话、密码或令牌。

`InfoMapper.xml.incrementPoint/selectPointByJiacn`按jiacn操作user_info.point；UserServiceImpl、PointServiceImpl、GiftServiceImpl及WxMpController有相关调用。删除分区列不解决积分隔离，灰度若直接写共享账号表会影响生产业务。

目标模型：全局账号保留id/jiacn、登录资料、account_state/auth_epoch；业务积分从身份表分离到现有积分域的租户化余额模型（不能未经语义核对直接并入economy货币账本）。现有point_record是流水，不可假设可无损重算余额；迁移生产现值到tenant0，tenant1不得复制生产积分。referrer、订阅/通知设置及组织职位等字段需逐项核对后决定是否迁出，不随三列删除机械移动。完成迁移前，灰度保持这些共享写入口关闭，生产路径继续使用原数据，不做不受控双写。

### C. oauth_client保留协议client_id

jia.oauth_client共6行，5行tenant0、1行非0。client_id当前无重复，但数据库只有PRIMARY(id)，无client_id唯一索引；user_info.jiacn生产已有唯一索引，jia_dev没有同等唯一索引，两个库不能盲套同一迁移结果。

目标是全局应用注册，不删除client_id/密钥/回调/scope。实例配置决定业务tenant，客户端认证、合法回调、issuer、audience/适用范围及实例允许客户端仍保留。去tenant列不能让生产实例接受灰度专用客户端，也不能让灰度替换成任意客户端。现有非0客户端的准入映射先转入配置并验证，而不是丢弃其含义。

本次metadata未发现目标两表的外键关联或提及目标表的库内触发器/存储例程；不是外部程序无依赖的证明。已知依赖集中在应用ORM、DAO、令牌签发及历史SQL。用户名/手机号等唯一性规则未在本轮擅自更改；新增client_id唯一性约束须匹配现有精确比较语义与空值规则，不把一个校对规则扩大为数据清洗。

## 其他表处置结论

| 类别 | 处置 |
|---|---|
| user_group/org/role/perms及各rel（8张） | 保留tenant/client。全局user_id挂在租户化成员/权限关系上；JOIN、列表、授权、修改均同域，不因身份共享共享权限。 |
| user_auth | 没有tenant/client，本轮主源码表名检索未见引用。先查是否为旧关系表及外部消费者；若仍生效，校验角色/权限父记录同域或迁至现行关系表，不能直接删除。 |
| oauth_api_key | 保留执行凭据tenant/client，和全局OAuth应用注册不是一回事。 |
| agent运行身份、绑定、任务、工作区、outbox/inbox、chat、hall、economy、point等业务表 | 保留租户；client的应用授权/幂等意义先保留。需要修复scope贯穿、唯一键及后台消费，不是去列。 |
| agent_persona、dialogue_template、core_dict等目录 | 公共只读定义与租户定制分开核对，暂不删列；禁止用tenant0兜底分享生产业务。 |
| archive_work/edition/chapter/paragraph、core_action、oauth_action/resource、schema版本表 | 现无业务tenant列；作为共享元数据候选保留，灰度编辑/发布不可写生产共享内容。个人阅读进度、笔记、书签仍隔离。 |
| wx_daily_vote_receipt/message_receipt | 无tenant列，按appid等外部维度幂等。需确保灰度使用独立appid/回调；否则补环境分区并迁移幂等范围，不能直接认定现状已隔离。 |
| 短信、微信、支付配置/发送/订单 | 保留现有分区；独立凭据、外部商户/应用和回调边界。tenant隔离不能阻止真实费用和短信副作用。 |
| 49张act_*引擎表 | 不删引擎TENANT_ID_、不自改引擎关系；从引擎租户/API及job executor配置隔离，未验证前灰度不启动共享消费。 |
| 迁移审计9张、备份3张（jia） | 保留原结构和防篡改触发器；不改写历史，不随活动表批量删列。 |
| v_task_item | 两库都有；核对底表作用域与视图访问路径，不因视图无显式控制就开放。 |

## 实施顺序（不新增审批阶段）

1. 固定目标和并发工作区：下次实现前重查远端develop；当前工作区大量其他Owner修改，若写路径/基线不能安全复用，仅建一个最小隔离worktree。交接本记录，不覆盖其他任务。
2. 先改应用兼容：目标实体不再持久化三列（优先局部映射/身份模型调整，不全项目删除BaseEntity字段）；移除客户端数据库租户查询，采用固定实例业务scope；保持客户端准入和令牌兼容约束。身份信息与业务scope分离，角色/成员查询不放宽ACL。后台也使用同一固定业务scope。
3. 新库schema、相关fixture、ORM元数据测试、登录/刷新/撤销auth_epoch、用户资料/列表/成员、生产0与灰度1拒绝互用、Runtime执行凭据及前端身份切换一起改。实际迁移至少覆盖有列→无列两种schema，防止兼容版本仍生成旧SQL。
4. 积分等业务状态迁出按现行积分域实现；不把它变成两张表永久双写。若本批只删身份scope列，继续关闭灰度共享业务写入口，不能因此宣布全功能灰度完成。
5. Flow固定候选完成必要测试/构建/上传后结束。主机拉不可变制品，先部署兼容目标列存在/不存在的应用，再迁移；构建可复用，不为下载/安装重试重跑。
6. 删除前在受控锁及必要停写下保存两表恢复备份、被删列按主键映射、SHOW CREATE、摘要与版本；不把元数据快照当数据备份。确认无旧实例/后台仍依赖列，再执行下述目标DDL。迁移jia_dev前单独核对实际用途及基线，不因名字含dev自动修改。
7. MySQL DDL不能假装事务回滚：两个ALTER可能部分成功，安装/恢复记录逐表标记；幂等续办只跳过已经达到目标的列，遇非预期schema停止。不恢复整表旧快照覆盖新账户/安全状态；不能直接回滚到依赖已删列的旧JAR。必要恢复新增列并按主键恢复元数据，新注册行按已定义兼容策略处理，不猜测旧租户。

目标DDL（**设计展示，尚未执行；不是可直接在线运行的完整迁移器**）：

```sql
ALTER TABLE user_info DROP COLUMN client_id, DROP COLUMN tenant_id;
ALTER TABLE oauth_client DROP COLUMN tenant_id;
```

## 当前尚未交付

应用修复、完整权限链语义核对、积分迁出设计细节、受控迁移器/数据备份恢复实测、Flow候选回归、安装及真实删列尚未完成。当前证据只支持“必须解耦且不能先删生产列”的结论，不支持“生产已完成解耦”或“全业务灰度可用”。

### 16:27 +08:00 远端再次核对

远端develop前进至 `de6776fb3092a3e71aa5004d115c1280b742f2aa`（Tomcat WebSocket测试fixture修复）。已比较a5f28ec1→de6776fb：全部`*/src/main/*`无变化，common/user/oauth/point/wx无变化；上述结构与主源码依赖结论适用于该查询时点最新develop。原证据保留a5固定对象来源，不把两版测试证据混用。后续实现基线应使用de6776fb或实施时重新核对后的提交。

### 后续用户决定与实现开始：积分归point模块

用户明确要求point模块另建积分表并继续。Owner仍为本线程；采用`point_account(tenant_id,jiacn)`，不按OAuth客户端重复发放同一用户余额；旧余额只迁tenant0，灰度独立从0开始。此决定替代前文“积分归属待定”。

因主工作区落后远端且与多个活动Owner存在大量修改，创建本任务唯一隔离工作区`/home/isp/wsps/worktrees/identity-tenant-decoupling-api-20261029`，分支`codex/identity-tenant-decoupling-20261029`，base `de6776fb3092a3e71aa5004d115c1280b742f2aa`；未覆盖/清理其他工作区。任务尚未合入或终止，工作区保留接续。

本轮已新增point账户Service/API/DAO/Mapper、建表与一次性导入脚本、定向Java测试、隔离SQL测试，详见该工作区`docs/point-account-identity-decoupling.md`。**当前为基础候选，原有调用方尚未切换，不能部署为完成版。** 正式Java测试/构建等完整切换后集中走Flow，不为半成品重复计费；没有修改生产表、删除列或启动灰度验收。

当前固定develop里的接口规范文件头实际为v1.2（前一记录中的v1.4是旧工作区/摘要记录，不能当成该提交文件版本）；实现期间以固定文件内容及用户最新兼容规则为准，本批新增内部Java接口，无wire变更。RB-1及根AGENTS已读取。新增源码只在本任务工作区，不操作其他Owner用户/积分源码。

基础候选已本地提交 `433d190e7a3867a5a2eb30b408aa886ed1f45635`，tree `28815ad10ef84d88ba6865a62a8fdc312cc726ed`；10个新增文件，无现有业务代码切换。最终SQL隔离测试9/9通过，日志`/home/isp/state/cyf-identity-decoupling-20261029/point-account-sql-test-final.log`（70.080秒）；Python语法/暂存diff空白检查通过。10项Java测试尚未执行，未跑Gradle/Flow，未push/合develop/安装。只读确认jia/jia_dev中point_account仍不存在，生产表未被迁移。测试库按随机任务前缀创建并在各测试结束清理，不操作他人库。

下一条动作：在同一工作区接入PointService/GiftService/UserService旧积分适配器与用户/微信余额读投影，统一余额与流水事务；处理用户列表/搜索的point条件，不能仅删除旧SQL或悄悄丢弃过滤语义。再覆盖现有签到/推荐/兑换取消并发与作用域，完成调用方切换后集中Flow验证。当前无用户输入阻塞，仍是未完成任务，不把本次基础提交当最终发布。

### 2026-10-29 继续：积分业务读写候选接入（尚未发布）

本轮再次只读查询远端develop为648d644bc2fcc27c3ea7d67d49d6f541370c55eb，已合入本任务分支，merge HEAD为732c70547d；没有覆盖主API脏工作区。当前本地候选 `44f070fadd0fd6b32224ffe765609f382434a645`，tree `9450142af119b50312acbac54ad94adfb2728c59`；实现提交42b38a7004，列表谓词收口4001a92e48，成员条件绑定修复44f070fadd。均未push/合远端develop。

已接入PointService全部积分变更、GiftService扣减/退款、UserService兼容方法；余额取point_account权威返回值，流水/订单状态与余额同事务。签到/推荐先锁账户并同域当前读，礼品/订单使用同tenant行锁与更新。用户point改只读非持久化投影，移除旧incrementPoint/selectPoint SQL，通用写入口清除point输入。用户get/list/search/生产my及微信余额读取接新账户；列表/搜索保持积分条件、point排序及成员/精确身份过滤。额外修复UserVOWrapper既有成员EXISTS的%s参数占位为MyBatis绑定{0}，没有去掉成员条件。

自检发现自定义customSqlSegment会遗漏QueryWrapper实体条件，且u别名会破坏成员user_info.id引用，已撤回该实现：列表仍走BaseMapper.selectList，仅增加参数化余额select投影，保留原WHERE渲染。新增实际Mapper回归覆盖该风险，尚待Flow运行。

轻量MySQL检查12/12通过（103.985秒），日志 `/home/isp/state/cyf-identity-decoupling-20261029/point-account-integration-sql-final.log`；XML/Python语法与diff空白检查通过。新增排序检查运行真实XML表达式。最后两次用户列表修复后，已比较SQL测试抽取片段及账户mapper/DDL/导入/测试源码与受测42b提交完全相同，复用该SQL证据；不把它当成最后两次Java修复已验证。精确摘要见 `/home/isp/state/cyf-identity-decoupling-20261029/point-business-candidate.json`。

生产只读积分业务聚合：jia签到1313、推荐2、礼品7、兑换9行全部tenant0，无NULL/非0；证据 `/home/isp/state/cyf-identity-decoupling-20261029/point-business-scope-aggregates.tsv`。这些表原索引只有主键，新增签到tenant/jiacn/time与推荐tenant/referral的索引脚本，尚未执行。没有改生产数据/列/服务，也没有启动灰度验收或Flow计费Run。

仍未完成：OAuth/user身份scope解耦及权限成员全链审计；签到位置/推荐人共享资料写入、礼品调用者ACL等完整灰度边界保持原白名单关闭；初始化/运维SQL消费者分类及迁回最新余额的受控恢复实测；Java/MyBatis/Spring事务、跨端回归、validateLayering和Flow固定候选构建；正式迁移/安装/删列。当前不能宣称生产行为已验证不受影响。

下一动作：沿当前候选完成user_info.client_id/tenant_id与oauth_client.tenant_id非持久化/去依赖，固定后端环境scope并保留成员/角色/凭据授权；核对Token创建/刷新/历史兼容与Runtime执行身份，不因全局身份共享放宽权限。完成连贯候选后集中Flow测试构建上传，再按停写/备份/迁移/安装恢复流程交付。Owner无外部输入阻塞；本任务未完成，不清理工作区或启动半成品发布。

### 2026-10-29 接续：身份字段解耦与业务成员候选（未提交/未部署）

在44f070候选之上继续实现：user_info的tenant/client及oauth_client的tenant改为不参与持久化，OAuth签发环境由进程配置确定，签名tenant声明仅保留环境绑定兼容。生产签发必须配置明确的issuer-client-ids；已导出原5个生产/1个灰度客户端配置候选（私有证据oauth-issuer-client-config-candidate.json），未应用。配置缺失会拒绝启动，因此当前不可直接发布。

只读聚合发现311用户中191有角色/组/组织关系，7个非空client用户全部没有等价同域关系。新增user_business_membership保存原业务归属，不授角色/权限；避免删除身份列后丢失筛选依据。注册/upsert在原用例事务内写入进程tenant及已准入调用者client，旧NULL client以空字符串表达仅环境成员。DDL和显式导入程序尚未执行生产迁移。权限关系仍独立保留；未支持路由仍按最小灰度白名单阻断。

本接续优先补充删列后的真实ORM回归及隔离SQL迁移测试；旧12项积分SQL结果不覆盖新成员迁移/OAuth改动。Java/Flow仍未运行，未push/部署/改生产库。

本接续候选已本地提交 `8dfd51b01846982994bde1f11c57be9c71fc4a8a`，tree `430d28254262ac27c61e55184476b8fedd2d3104`；远端develop再次只读核对仍为648d644（没有push/远端合并）。已补充用户/OAuth删列实际ORM测试、成员Service范围/事务声明测试；修复OAuth查询修改调用者tenant字段的副作用，以及通用用户查询静默丢弃point条件的问题（要求显式业务scope）。测试profile提供合成OAuth准入值，生产清单尚未配置。

隔离MySQL成员测试5/5通过，17.658秒；日志 `/home/isp/state/cyf-identity-decoupling-20261029/membership-sql-test.log`，精确输入摘要 `/home/isp/state/cyf-identity-decoupling-20261029/identity-membership-candidate.json`。Python/XML语法和diff空白检查通过。未运行Java/Flow/应用启动；未变更生产数据、配置和进程。

剩余动作：初始化/历史SQL消费者清理（旧tenant-default-zero仍含两个身份表，不能套用删列后库）；角色/组/组织权限链与全局身份删除后成员清理策略；受控迁移/最新余额恢复演练；完整候选Java/分层/启动回归及Flow构建，再受控安装与删列。当前最小灰度路由限制保留，不能据本地提交宣称全业务隔离或生产验证完成。

### 2026-10-29 18:34 +08:00 收口与首轮正式Flow

候选`bff21501a3abb72368a4c5bf3105f86076faa942`已push本任务分支（未合develop）。在8dfd候选上增加全局用户删除的同事务成员清理，保留财务历史；当前可执行tenant-default-zero脚本排除两个身份表；补充只导出最新tenant0余额的财务恢复步骤及实际Mapper/Spring事务回归。权限链审计结论及限制已写入候选设计文档，不扩改原权限ID映射。成员SQL6/6（5.358秒）和余额恢复2/2（1.660秒）通过；两类日志在私有证据目录。其余原12项积分SQL仅精确未变输入可以复用，未重新宣称全部Java通过。

Flow5260799原配置读取/备份后，确认无活动Run；本任务临时配置仅本任务分支、关闭push触发、25个定向测试类+validateLayering+fresh bootJar+上传，worker超时10分钟，另本机控制面留30秒取消余量以约束600秒总上限。不包含生产SSH/VMDeploy/健康等待。原配置含60分钟作业时限，不能直接沿用。原默认配置备份flow-config-before.yaml（SHA83846448...）；本候选config SHA19034760f7dbd15e5e9e8b0a773185974b8005876ecc21ad9d6e8ae5e3c8da82，更新readback APPLIED。

现有flow-control start遇到历史分页未尽会拒绝（当前372条Run），因此复用工具的私有快照，仅把listRuns改为完整分页且拒绝重复token，不删除来源/配置/历史快照核对；主工具未改。已保存完整历史及启动上下文。一次start明确返回373；初始INIT无sources使工具报UNKNOWN，不再次start。随后只读确认373 RUNNING且来源为本任务分支；精确commit仍以worker固定SHA检查/最终制品闭包核实。

当前正式Run：5260799/373，job545896204，18:33:25发起。控制面watch仅处理已回执373；证据flow-start.json、flow-373-status.json、flow-373-watch.jsonl。Run终态后需在确认无他人活动Run且配置仍是本任务候选时恢复原默认配置，不以恢复重触发构建。生产数据库/配置/进程未改动，本Run也不安装。


### 2026-10-29 正式回归、制品核验与develop集成（当前最新状态）

- 远端develop在集成前再次核对仍为648d644bc2fcc27c3ea7d67d49d6f541370c55eb；已安全快进到`bff21501a3abb72368a4c5bf3105f86076faa942`，tree `b57d8e09b4c493c1e06d9baad18353350839dfaa`。主API脏工作区未切换、未覆盖；本任务工作区干净，仍保留处理未完成迁移阶段，不创建第二套worktree。
- Run373真实FAIL：旧编排器在函数内重复硬编码branch list，外层白名单修改仍不足。失败发生在Gradle前，无应用测试证据。修复只在本任务冻结工具bundle显式增加该分支，并保持实际Flow身份/commit/tree/argv/digest/锁校验，不伪装develop。
- Run374 SUCCESS，创建至终态更新时间190秒。25个指定测试类加JAR安全/运行类路径测试，报告共222项，其中219执行通过、3跳过；validateLayering和fresh bootJar实际执行通过。构建制品下载到 `/home/isp/state/cyf-identity-decoupling-20261029/flow-374-artifact.tgz`，223754486字节，SHA256 `0fac108dca86c2eaf57c108b8532b01fa451bf28a9231bfea2e7201817eb9124`。包内JAR251236521字节、SHA256 `f28fe7d6a1b68dabb6886977e72e9b102a94e78a62ce36c29fc1fd288122e11f`；receipt摘要`9429fcf1c734d82351ed5b44d5cdd03fa66c5f44e57400f5d2d40f377865be54`。已流式核对包内JAR/依赖摘要、receipt/metadata、源码commit/tree、目录安全和实际Gradle任务证据，不把只有Run绿灯当验收。
- 3个跳过项为WxDailyVoteCallbackMySqlTransactionTest，原因是旧默认worker只有MySQL二进制，没有该fixture要求的URL/port/datadir环境。没有把跳过当通过。Run375只补这3项：同一bff源码，worker独立MySQL8.0.21/随机非标准端口/唯一datadir，保留测试自带身份检查；清理仅自己的socket实例。3/3执行通过，0跳过，创建至终态82秒。不重新bootJar、不重新执行已完成范围，不拆Run绕过600秒；仅上传verification-only报告。Run374原跳过记录保留，222项累计实际通过来自219+3。报告制品SHA256 `b6ea6741e4e4cdb10dad61d9921f2e3201bfa279a06d3e2e596625fb74fa1003`。
- 补跑期间保持临时配置无push触发，故同一bff代码快进develop未触发重复付费构建；最新Run仍375 SUCCESS。随后确认无活动Run且配置归本任务，恢复原流水线配置并readback APPLIED，SHA与最初备份完全相同；未取消他人Run。原默认配置中的历史60分钟作业设置未被本次恢复宣称为全局时限改造，本任务各Run有10分钟worker上限及本机受控超时保护，实际均低于600秒。
- 汇总证据 `/home/isp/state/cyf-identity-decoupling-20261029/combined-verification.json`；完整单次测试报告flow-374-summary.json/flow-375-summary.json；控制配置、启动上下文、readback及watch日志同目录。签名制品下载URL未落盘。共享工具/共享技能未在本轮修改，分页修复仅为私有工具快照。

**未执行生产数据库或应用变更。** 没有创建生产point_account/成员表，没有修改生产issuer配置、停启服务、安装JAR或删除旧列。代码合develop不等于最新代码已部署，也不声称生产全流程已在线验收。

下一阶段直接复用374制品：核对生产部署协调锁/身份与所有旧写入者；准备并实测完整身份/资金恢复方案（已测试的point导出仅是财务恢复步骤，不是完整回退器）；停写备份并导入point账户与业务成员，应用明确的生产issuer-client-ids后受控安装；生产登录/刷新/积分/回调等健康与业务核验通过、确认无旧二进制依赖后才删旧列。灰度仍保持最小路由白名单，不要求用户验灰度、不扩大旧权限修复。不可因成功制品而跳过迁移前置，也不为下载/安装/文档重复构建。

### 2026-10-29 19:20 +08:00 接续：主机交付准备与恢复演练（尚未安装）

远端develop重新只读核对仍为bff21501a3。现行生产为Flow372 / 648d644bc2，JAR SHA `4683e8d17aabf97aad62160979485b5d498a510bc45ac5675e4bba54200f2bb0`，实际PID1881603、canonical cwd/JAR匹配，现行生命周期入口报告HEALTH=UP。程序目录旧pid文件205187已陈旧，当前权威PID在/run/cyf-api，不因旧文件判定停机。

已完成7项独立合成MySQL恢复演练（31.040秒）：删列后恢复scope与最新积分、保留最新auth_epoch/资料/客户端secret、保留灰度余额和新用户、拒绝多重/缺失成员的有损降级、新OAuth客户端必须显式指定环境、拒绝按复用id猜client归属、不复活删除身份且不丢弃孤立资金。证据及操作说明位于 `/home/isp/state/cyf-identity-decoupling-20261029/recovery-rehearsal/`。这是SQL恢复验证，不是生产回滚实测；多成员等旧模型不可表示时选择前向修复，不承诺任意时点可回旧版。

发现当前deploy及install两层均硬编码仅接受develop分支回执，实际Run374回执为已合入develop的任务分支，不能直接交给旧适配器。准备了仅准入**精确Run374回执摘要+原分支+commit/tree**的局部适配候选，不允许任意codex分支，不改回执/原身份/制品/审批/锁校验；每层12项分支检查及现有38项发布/schema/锁回归通过（7.096秒）。候选路径 `/home/isp/state/cyf-identity-decoupling-20261029/host-admission-candidate/`，未替换生产helper；真实制品离线安装与幂等/篡改拒绝验证仍在进行。前两次夹具失败分别为缺少fixture锁和120秒测试驱动超时；未触及生产安装，后者有本机I/O等待现象，不能宣称应用启动慢或成功。串行化后重验，保留真实结果。

真实Run374制品已校验并暂存到 `/home/isp/state/cyf-api-flow/downloads/374/package.tgz`，记录host-artifact-staging.json。已备份两个身份表及五个point业务表、现行JAR/config/helpers/release record到 `/home/isp/baks/cyf-identity-decoupling-20261029-preparation/`（0600/目录0700；manifest绑定摘要）。此为运行中准备快照，**不能替代切换停写后的最新备份**。未新增Flow计费运行。

用户最新明确“忽略其他连接”：不再将其他连接作为协调/审批前置，不操作或断开它们。其是否运行旧字段SQL仍未验证，不把用户决定当成兼容性证据。本机API的停写、迁移前备份、积分一致性、配置准入、锁归属和可恢复安装保护仍保留。生产迁移/配置/安装/删列尚未执行；继续本机发布准备，不要求用户灰度验收。

#### 19:28 +08:00 本轮验证结果补充

串行运行的真实Run374制品离线安装通过：候选installer完成完整包/回执/权限/备份/原子替换/记录流程，第二次返回PASS_ALREADY_INSTALLED；篡改approval的JAR摘要被拒绝且已安装夹具JAR未变化。测试使用/tmp独立目录及模拟生命周期，**没有启动真实Java、没有生产部署**。结果 `host-admission-candidate/real-artifact-install-verification.json`；先前超时/缺锁失败保持历史事实。7项恢复SQL、两层各12项分支准入、38项既有回归与真实包安装验证分别记录，不叠加冒充新的云端应用测试。

重新只读核对生产OAuth准入仍为原5个client，已生成仅新增issuer-client-ids的私有配置候选，`production-config-preparation.json`记录原配置/候选摘要，`applied:false`；配置内容含原有秘密，仅留0600私有文件，不写入版本库或对话。生产helper、配置、表结构、应用进程均未修改。

下一动作：将已验证的精确制品准入改动沿既有coordinator→release→lifecycle锁、前值备份及原子写入安装（当前安装helper与根工作区source不相同，严禁整文件覆盖丢失现行修复；源码只作局部补丁）；固定切换时配置/旧JAR/schema/data备份；停止本机API、一次性导入新表、逐行对账、应用准入配置，再从已暂存Run374制品安装，使用现有forward-only避免自动恢复不兼容旧二进制。用户已要求忽略其他连接，不再因此等确认。全部上线/删列实际结果仍待执行，当前不声称生产已完成解耦。

### 2026-10-29 20:23 +08:00 接续纠正及历史记录策略

**覆盖前文“生产未改动”的历史状态。** develop已前进到502bd06fa9a9290152330e8e094b9ff05b8ad0ee（包含本任务及其他Owner的chat修复）。真实Run378全量构建成功285秒，3247执行通过/159跳过；本任务Run379补充187项实际通过、零跳过，116秒；378不是本任务触发，不修改其归属。随后已恢复原Flow配置。两者均不含当前待提交历史身份兼容修复。

首次真实切换停止旧API并备份至`/home/isp/baks/cyf-identity-cutover-20261029T200529/`；创建point_account/user_business_membership后，积分导入因1条无jiacn历史记录被拒绝。该记录积分为0；没有导入余额、没有写issuer配置、没有安装新JAR、没有删列。旧API恢复成功，20:21复核PID1973166、制品MATCH、HEALTH=UP。两张新表均为0行，旧导入过程保留，不能声称数据库没变更。证据`/home/isp/state/cyf-identity-decoupling-20261029/latest-develop-release/cutover-events.jsonl`、`cutover.log`。

用户最新明确历史无jiacn不迁：本次修复将NULL/空身份排除积分导入/导出，原用户/角色及旧值保留，不要求补造身份；有效身份资金和写权限保护不变。补充详情/列表投影兼容，修复NULL键访问不可变Map风险。16项轻量SQL回归通过，日志`identityless-point-sql-v2.log`（同证据目录）；本次Java及新制品待Flow，不复用378冒充新修复。其他连接继续忽略，不操作其进程或连接。下一步提交到最新develop、单次定向Flow测试/构建、预检及安全恢复空表迁移后再安装。

### 2026-10-29 20:33 +08:00 修复正式证据（安装前）

修复`d8f9672f1ed24ef8cdc2796773259f98feed5c41` / tree `e5df6ed36c4d9196a949fad19a400158bd2d9121`已快进远端develop，保留502基线的其他Owner修改。先临时关闭push触发再推送，仅启动一次Run380；Flow worker29个选定类及制品回归共255项实际通过，0失败/0跳过，3项WX真实MySQL与2项无身份兼容回归均执行；validateLayering及fresh bootJar通过。Run SUCCESS，创建到终态141秒，原配置已恢复readback APPLIED。未调用或等待生产主机，没有额外下载/安装Run。

制品223754737字节、SHA `d81734e30717eb61d35098b2be07a128741c977cdac8cb629e862609c5376719`；JAR SHA `2b26eb37b9e79f96474a3c0f6c378bced431d58120268bbffe99a3accd6238d1`；receipt SHA `f642134fa61a32e2e2f3f3d7a6ba4a179097f8e7c4da14cf78668117ff3c911c`。已验证develop真实回执/完整源码、包安全、摘要及测试方法，无需替换安装helper。

空表定义与旧过程已在自有合成库按502源码比对，一致且生产目标仍空；只读源预检311用户、1条无身份跳过、310有效积分身份。迁移协调器补充停机前预检及精确空表续跑，不覆盖已导入目标；4项合成hook验证通过（首次/残留空表续跑/非法余额恢复/配置失败恢复），新版导出7项恢复SQL也通过46.091秒。本轮仍未开始安装，后续状态单独记录。

### 2026-10-29 20:40 +08:00 实际迁移完成，等待主机启动

本轮已于20:35:46停止旧API，停写后备份`/home/isp/baks/cyf-identity-cutover-20261029T203533/`；精确核验并复用两张空表，替换本任务旧导入过程。310条有效jiacn积分账户及311条成员关系导入成功，逐行余额/归属不匹配均0，积分汇总2889一致；无身份用户未建立积分账户，用户/角色原记录未删除。资格查询两个索引已创建，导入过程已清理；仅issuer-client-ids配置新增已应用。其他连接未操作。

现行安装器已接受真实develop Run380并替换候选JAR，20:36:38启动新PID1992253，正在等待实际健康；此时record为prepared，**尚不能记installed或健康通过**。使用forward-only，候选可写后不会自动恢复旧JAR。旧四列仍保留。完整日志`latest-develop-release/fix-cutover.log`；这是主机独立安装等待，Flow早已结束，不产生额外Flow等待费用。在线删列已通过当前生产表定义的自有克隆库验证，但生产删列尚未执行。

### 2026-10-29 20:51 +08:00 本轮完成：生产已安装并完成身份旧列退役

- **当前生产**：Flow5260799/380，源码`d8f9672f1ed24ef8cdc2796773259f98feed5c41`，tree `e5df6ed36c4d9196a949fad19a400158bd2d9121`，JAR SHA `2b26eb37b9e79f96474a3c0f6c378bced431d58120268bbffe99a3accd6238d1`。安装器20:41:58报告PASS，实际PID1992253；20:50再次确认canonical目录、ARTIFACT_ATTESTATION=MATCH、HEALTH=UP。版本仍为组件现有1.1.2-SNAPSHOT，精确发布以commit/tree/Run/SHA绑定。没有替换两个现行部署helper。
- **数据库完成状态**：20:49新备份后在线删除`user_info.client_id/tenant_id/point`及`oauth_client.tenant_id`，剩余旧列计数0。311用户、310积分账户、311成员关系；1条无jiacn历史用户原记录保留，不创建积分账户，未删除角色。OAuth协议自身client_id保留；业务表tenant/client不机械删除。生产issuer清单已应用，仍按进程配置业务环境。
- **生产验证**：删列前后均用既有专用测试账号完成真实HTTPS PKCE登录、获取token、读取`/user/my`；生产tenant/client绑定正确，个人积分与point_account实时查询一致；未做付费/积分变更/任务重放。公共客户端未签发refresh token，因此不声称实测刷新。canonical-path只读8项检查通过。没有验证灰度、不要求用户验灰度；线上未发现本范围回归，不等于全项目全部生产业务均实测。
- **诊断边界**：HTTP验证最初因自带Python未找到系统CA、随后测试驱动没有携带登录表单redirect_uri而失败；改用系统CA且按真实表单参数后通过，未关闭TLS验证、未改生产认证代码。首次删列前置探针只接受字符串UP，而实际健康为status.code=UP，修正探针后通过；失败发生在备份/DDL之前，没有将应用健康误记DOWN。上述失败日志保留。
- **恢复与证据**：迁移前停写备份`/home/isp/baks/cyf-identity-cutover-20261029T203533/`；删列前当前数据备份`/home/isp/baks/cyf-identity-column-retirement-20261029T204926/`。`latest-develop-release/release-binding.json`标记installed=true，`fix-cutover.log`、`retire-columns.log`、`production-smoke.json`、`final-production-status.log`、`final-db-aggregates.tsv`分别保存安装/DDL/业务/健康证据。全部位于`/home/isp/state/cyf-identity-decoupling-20261029/`，敏感配置与数据备份不进Git。旧回退必须重新导出**当前**余额与可唯一表示的成员归属，不能恢复旧全行快照；多重成员等情况前向修复。当前已删列，严禁直接启动旧372 JAR。
- **成本/其他范围**：本轮仅一次付费Run380，141秒；下载、迁移、启动等待及验收均在主机，云效不调用或监听本机。原配置已恢复；旧378/379未冒充本修复。安装器既有F06检查返回existing_equivalent，E05未获本Run激活授权且未执行，不声称由此激活其他功能。未处理其他连接、其他Owner工作区、runtime或旧锁序问题。
- **仍保持的既有边界**：灰度最小路由白名单不变；角色/组织权限、支付/短信等外部副作用以及共享用户业务资料的全功能隔离不是本次身份解耦完成声明。全库库存分类仍见同目录INVENTORY；只有上述生产jia表变更得到本轮现场证明，其他库/表不能重标为已迁移。

本任务源码已推送develop且工作区干净，收口删除本任务worktree；迁移/恢复SQL的固定源码快照与摘要另存`latest-develop-release/source-migration-resources/`供后续恢复取用。原私有脚本内SRC路径作为历史执行位置保留，不应在其他源码目录上未经固定commit直接重跑。本轮不清理生产备份、发布记录或其他任务文件。
