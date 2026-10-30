> **2026-10-30 23:04本批已闭环**：已开发API候选`5c2a2e45d4`合develop，Flow409 SUCCESS（4260通过、186跳过、0失败），生产安装并核验通过，PID415368/JAR摘要匹配/HEALTH=UP；登录、资料、积分及Agent读链通过。安装中断已恢复后复用409制品完成，主机最小重试修复合根仓develop `2072aac3`。未实施灰度项仍按用户决定冻结，不把下方历史库存重新计作本批待办。最终证据见主handoff §24。

> **2026-10-30 22:10续授权进展**：用户要求将已开发代码完成验证并部署，旧停止发布决定已被覆盖；未实施功能仍冻结。已正常合入develop `5c2a2e45d4`；Flow407的6失败均已消除，408仅新增跨租户测试的错误码断言失败（认证层提前正确拒绝）；该断言已修，Flow409运行中。未安装候选，当前生产仍403，详情见主handoff §23。

> **2026-10-30 21:23最终冻结**：已合develop `66be871f3d`；Flow406验证FAIL（4458测试、55失败、186跳过）。本轮不继续开发或重跑，不部署。17个失败测试类及55个精确方法见同目录`FULL-TENANT-GRAY-20261030-ANALYSIS.md` §22；下方旧库存不构成继续实施承诺。

# 全量租户灰度：当前代码未完成明细（2026-10-30）

> **2026-10-30 20:35用户最终范围冻结**：一小时内收最后一版，未实施项停止扩改；本报告旧待办不再是本批交付承诺。已有候选已合入develop `166897f98f`，Flow5260799/404验证中；未部署。最终边界及证据见主handoff §21。

> **2026-10-30 20:16 分析核实**：最新API develop已`dec6e285`，Runtime已`d0c3527`；API脏候选未合入新主线。公共插件的显式INSERT跳过、UPDATE可修改tenant及三个InterceptorIgnore责任已核实；确定AbilityEvaluation/Comparison DAO不逐个改，旧persona绑定tenant0联接必须收口，membership全局身份删除不能误套普通隔离。具体保留/撤回/必改位置及测试见主handoff **§20**。本轮仅分析文档/证据，无应用源码修改；表/语句分类与剩余独立入口证据未闭合，**未宣称全量分析完成**。

> **2026-10-30 18:50 更新**：公共policy已删除legacy/default0模式，各生产入口统一注入；Chat恢复发现和relay双路径已收敛，删除无tenant自动查询0的便利接口。增量69文件（21生产、48测试），生产净删230行；编译/应用测试仍未执行。旧生产配置不能直接启动此候选，必须显式配置业务tenant；主机配置未改、未发布。`/user/my`旧投影分支与公共SQL覆盖等仍未完成，详见[主handoff §19](/home/isp/wsps/cyf/docs/implementation/handoffs/FULL-TENANT-GRAY-20261030-ANALYSIS.md)。下方历史统计不自动代表当前剩余量。

> **2026-10-30 18:07 实施进度更新**：技能版本6处owner误当tenant已修；技能恢复发现SQL已在LIMIT前按process tenant/client分区，恢复入口tenant0门已删除；原Task进程policy Bean已移入common供Task/恢复共用（legacy配置语义尚未清除）。本次12文件+192/-51，测试源码已同步但编译/应用测试/EXPLAIN未执行。公共SQL覆盖仍仅Task，其他未完项不变。逐文件证据及剩余边界见[主handoff §18](/home/isp/wsps/cyf/docs/implementation/handoffs/FULL-TENANT-GRAY-20261030-ANALYSIS.md)。下方旧行表中这两项保留作发现记录，不再表示尚未编码。

> **2026-10-30用户后续收口：本文93文件仅保留为源码问题/依赖排查记录，不是93个必改文件或当前剩余交付量。** 实施按 `/home/isp/wsps/cyf/AGENTS.md`“分层职责与最小联动”重新归类：优先公共机制；已覆盖的主键调用不改；前端契约不变则仅回归，不纳入灰度必改；未核实联动与无关改进不计入必改。下面代码证据保留，不据此批量改造。

Owner：FULL-TENANT-GRAY-20261029。当前已按v2开始候选源码精简，旧93文件部分为此前只读排查；无Flow、安装、重启、DDL、模型调用。

## 实施方案 v2：最小职责与性能（2026-10-30 17:40起复核）

本节是当前实施口径，覆盖下面旧93文件清单的“逐文件必须修改”解释。目标不变：身份全局、环境租户隔离、公共定义不冒充生产tenant0、生产流程不串数据；不新增前端租户能力或全项目安全框架。API基线当次远端复查仍为`16a769bd727cebaa636cb18d55f238e80aa44d8f`，复用原未提交候选，不重置其他任务修改。

### 一、按职责重新分组，不按调用链层数扩展代码

| 责任位置 | 本次必须处理 | 不再做/撤回 | 完成证据 |
|---|---|---|---|
| 环境准入与上下文 | 环境租户唯一来源，入口确认身份和环境一致；全局user/OAuth不存业务租户；复用现有可信上下文 | 不为了灰度更换完整认证协议；不让每个Controller/Service重复构造准入策略；不把无缺口的接口重写 | 公共准入测试，必要HTTP/WS入口集成；旧凭据切换影响单列 |
| 公共持久化 | 在现有MyBatis能力扩展明确业务表范围；全局表排除；主键/批量保持现有API；原生SQL只在未覆盖边界补分区 | 不逐个DAO追加tenant形参，不逐行二次过滤SQL已限定的数据，不再“本租户OR生产0” | 真实SQL覆盖读写/主键/批量/分页，证明生产与灰度双向隔离 |
| 现有业务与Schema | 移除实际阻止配置租户的写死0，修正tenant/owner传错，活跃CHECK与索引同步；权限、状态、CAS/幂等继续由原业务负责 | 不为每个方法新造scope类型、校验器和状态机；金额0/owner保留值不批量替换；不恢复旧执行协议 | 同候选修真实调用方/约束/fixture，定向业务回归 |
| 后台与独立存储 | 查询在LIMIT/排序/领取前分区；队列vhost、文件根、ES/缓存绑定环境；异步不借HTTP上下文 | 不读全表后过滤，不以关闭HTTP路由代替后台隔离；不无依据新增缓存和调度器 | owned fixture混合租户发现/claim/CAS，文件/消息/索引互不污染 |
| Runtime | 复用已有带scope协议；独立正式app根、unit、config/state/identity/HOME/ACK/端口，保留生产默认路径 | 不新建一套Runtime，不修改不受影响的业务协议，不复制API业务授权 | 现有安装及session/ACK并存测试，mock Provider |
| Web | 保持既有API契约，做必要兼容回归 | 移出灰度必改：PersonalWorkspace身份helper重构；目前本线程没有Web源码修改需要撤回 | 确认后端投影契约不变后无需前端代码变更；如出现真实契约变化只联动对应消费者 |

这些是责任范围，不是六个互相独立的新框架。原生SQL未覆盖、消息入口与授权/并发边界不是“重复防御”；公共覆盖尚未完成前，不先删除唯一保护。普通查询不增加“先查是否属于租户，再查业务”的额外往返。

### 二、已实际撤回/精简的候选代码

| 文件 | 本轮动作 |
|---|---|
| [AgentServiceImpl.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java) | 撤掉catalog列表逐行重复scope检查及requireScopedCatalogPersona；单条目录读取直接使用已限定SQL结果。保留业务绑定、owner、状态和不存在处理。 |
| [AgentHostedBindingTransaction.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentHostedBindingTransaction.java) | 撤掉新增的persona读取后再比一遍tenant/client/active/code；SQL过滤和托管事务授权保留。 |
| [AgentPersonaDaoImpl.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentPersonaDaoImpl.java) | 名称查询不再二次校验整个目录每一行，也不先重复校验scope；复用findCatalogProjection边界；保留名称覆盖/歧义语义。 |
| [AgentPersonaPublicScopeTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentPersonaPublicScopeTest.java) | 把“伪造DAO返回跨域行，要求Service再次过滤”的测试改为服务映射、单次查询及不存在处理。隔离在真实SQL测试验证。 |
| [AgentPersonaDaoCacheInvalidationTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/test/java/cn/jia/agent/dao/AgentPersonaDaoCacheInvalidationTest.java) | 移除名称读取中依赖损坏Mapper mock的重复过滤断言；保留事务提交/回滚缓存和写入边界用例，新增查询次数断言。 |
| [TenantActorAdaptersTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/security/TenantActorAdaptersTest.java) | 不再在14个adapter各复制7种claim格式/alias/version负例；完整矩阵留在TenantClaimPolicyTest，adapter保留scope映射、缺权限与Runtime窄身份边界。 |
| [schema.sql](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/schema.sql) | 将候选唯一索引顺序调整为tenant+code/name+client key，不加索引数量、不改变唯一性语义。 |
| [agent-persona-private-scope-20261030.sql](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/agent-persona-private-scope-20261030.sql) | 同步候选索引创建和形状核对顺序；没有执行迁移，旧线上结构未变。 |
| [AgentPersonaSchemaScopeContractTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/test/java/cn/jia/agent/dao/AgentPersonaSchemaScopeContractTest.java) | 同步索引文本合同；明确文本检查不能替代真实MySQL执行计划。 |
| [AgentPersonaTenantInterceptorRealDatabaseTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/test/java/cn/jia/agent/dao/AgentPersonaTenantInterceptorRealDatabaseTest.java) | 在原H2/MyBatis测试集中补inactive与NULL归属排除，证明移除Service重复过滤后责任仍在SQL，而不是删除隔离要求。 |

仅本轮增量：10个候选文件（5个Java测试、3个Java实现、2个SQL文件），新增47行、删除63行。原字节与独立差异已备份；不是把207个既有变更文件整体回退，也不是宣称全部过度开发已撤完。

### 三、保留与暂缓撤回的边界

- 已确定的user/OAuth全局化、point拆表、公共persona与生产租户分离、严格tenant准入、不回落0等目标及对应既有改动保留；“简化”不推翻用户已明确要求。
- **暂不恢复persona旧通用CRUD**：当前公共机制还仅覆盖task表，直接恢复裸写会重新暴露未隔离入口。新增private写接口与维护脚本是否能进一步收敛，须与公共机制覆盖和真实写调用方一起处理；无调用不继续增加功能，不以批量回滚制造中间安全空洞。
- AgentService内重复process policy、Controller重复claims解析、其他列表返回后scope校验仍需按覆盖证据收敛；不是本轮已经全部删除。保留任务/绑定/执行身份一致性等不同业务规则，不能把它们机械等同tenant过滤。
- TaskTenantConfiguration目前范围仍不足；80个BaseDao继承实现是表分类影响范围，不是80个逐文件改造任务。未发生改动的主键方法无需“还原”。
- 旧93文件中的Web优化、潜在改善和未确认后台可达性不再计入必改；实际写死0、错误tenant/owner、无分区的后台发现仍是本次需求内问题，不以收缩范围掩盖。
- 先完成公共覆盖与真实绕过点，再收掉已被覆盖的重复校验；不为这轮梳理另开Flow、添加审批、发布或重启。

### 四、性能处理与验证方式

| 路径 | 当前观察/风险 | 处理及验证，不新增硬门槛 |
|---|---|---|
| persona单条目录查询 | 条件含tenant+persona_code，SQL没有用catalog_client_key条件；旧候选索引将该列放在中间 | 本轮改成(tenant,code,clientKey)。唯一性不变，意图是使可用索引前缀匹配查询；是否实际使用及扫描量需owned MySQL EXPLAIN验证，不宣称已提速。name索引同序调整；当前名称Java合并路径不会因该索引自动提速。 |
| persona列表/托管 | SQL限定后又在Service/DAO逐行重复核对；目录合并仍有必要 | 本轮去掉重复遍历中的防御判断，不新增SQL。保留已有批量补充，不改成N+1，不缓存用户绑定/运行状态；现有metadata缓存继续使用。 |
| 名称查询 | 当前会加载并合并公共108定义与本域私有覆盖，而非索引点查 | 这是新增适配的待测成本；先核对调用频度与查询计数，不为了猜测热点新增缓存/索引/复杂SQL。需要优化时在目录责任层统一处理覆盖/同名语义，不每个调用方实现一遍。 |
| 公共SQL拦截 | 全局无差别SQL解析、重复注入可增加开销并误伤全局表 | 复用现有机制，静态确定适用statement/table；不每次请求查information_schema、不增加存在性查询、不叠第二套全域拦截器；比较最终SQL及查询次数。 |
| 后台发现 | LIMIT25/100前未分区会跨环境扫描/饥饿；仅加WHERE不证明计划有效 | 根据真实WHERE/排序/游标/claim SQL复用或调整联合索引；owned fixture检查执行计划/扫描量及外租户置前场景；不盲目给每张表加tenant单列索引。 |
| byte-exact谓词 | 现有等值+CAST/OCTET_LENGTH组合可能增加逐行计算，但也承担实际排序规则/尾空格语义 | 不仅因“看起来重复”就全删。保留可索引等值前置；核对真实列collation与执行计划后，才能移除确实冗余部分。 |
| 缓存/ES/文件/Runtime | 串域风险与资源开销不能靠SQL一处解决 | 复用已有环境分区；保留缓存有效性、批量获取和连接复用，不重复部署服务/构建制品来凑隔离；模型/embedding回归用替身。 |

性能结果：未跑真实数据库执行计划、负载测试或基准；不报告虚构百分比、毫秒收益或“生产不受影响”。本轮静态确认没有新增查询；具体行为和查询次数以应用测试为准。

### 五、验证状态与后续顺序

1. 本轮`git diff --check`及定向源码检查通过；已核对SQL tenant/client/active过滤仍在、共享claim负例仍在、DDL/维护索引顺序一致。
2. Java编译、H2/MySQL测试、完整回归均未执行。新增测试只是源码，不能计为PASS；正式重型验证仍在Flow worker固定候选执行，不本机启动Gradle。
3. 下一步按“公共覆盖→实际原生/后台绕过点→必要业务写死值/Schema→删剩余重复防御→定向集成与性能验证”推进，不默认改Web、不动生产。
4. 原字节、独立补丁与摘要：`/home/isp/state/cyf-full-tenant-gray-20261029/scope-simplification-20261030/before/`、`simplification-only.diff`、`result.json`。当前没有合入develop，没有Flow/安装/重启/DDL或付费模型调用。

---

## 口径与固定源码

- API候选：`/home/isp/wsps/worktrees/full-tenant-gray-api-20261029`，HEAD / 当次远端develop `16a769bd727cebaa636cb18d55f238e80aa44d8f`，候选含未提交修改。
- Runtime：`/home/isp/wsps/chcbz/isp-install`，当前HEAD / 当次远端develop `adac2c828646fd9e8dd04af226546e8ae0f01afe`。旧分析66e896f不是最新，不能覆盖其后修复。
- Web：读取远端develop固定对象 `1fdc94ac152e07091016fb9d3d898acf37551a6c`，不修改本地另一Owner脏工作区。
- 远端查询时间2026-10-30 17:02–17:03 +08:00；逐文件SHA与行号保存在 `/home/isp/state/cyf-full-tenant-gray-20261029/analysis-20261030/code-remainder-1702.json`。
- 本清单确认 **93 个不同源码/SQL文件**涉及确认未完成点（API 90、Runtime 2、Web 1）。这是已确认文件数，不是剩余提交数/工时，也不包含所有需要联动修改的测试和调用方。
- **不能把该数字称为穷尽后的总修改文件数**：其中公共方案可能一次修复多个文件，不要求逐文件复制修改。公共DAO有80个当前继承实现需要按表分类核对，另有schema/配置/后台消费者依赖项；不能把依赖命中都报作缺陷，也不能假装这些核对已完成。
- 上次“8个代码工作包+1个验证”是粗分组，不能用来回答代码剩余量，本报告替代该计数口径。
- 已改HTTP actor、strict claim、persona目录/私有写入不重新计入“尚未改”；仍需编译/测试。业务金额0、owner保留值0、历史golden中的0不是自动缺陷。

## 确认未完成的源码/SQL

| 范围 | 不同文件数 |
|---|---:|
|01 公共DAO和进程准入|3|
|02 SYSTEM运行身份与预置定义拆分|3|
|03 托管与场景及Agent旧重载|8|
|04 创建任务、需求确认与协作|5|
|05 Hall创建、草稿、私有案例与标记|6|
|06 成果、正式交付与返工|6|
|07 资金业务和预览scope|4|
|08 能力评估持久化|2|
|09 技能安装、回执和版本|5|
|10 后台发现、领取和状态转换|5|
|11 Chat会话及任务线程|10|
|12 WS、讨论与完成事实|10|
|13 长期记忆和内部工具调用|8|
|14 归档scope、HTTP和后台|5|
|15 活跃DDL与Schema校验|10|
|16 Runtime与Web|3|

### 01 公共DAO和进程准入

现状：BaseDao按ID/批量/全量方法没有租户谓词，selectByEntity在tenant为空时不加条件；task拦截器只覆盖task mapper的3个表；进程策略仍分legacy/fixed双模式。

修复：沿已有MyBatis能力按业务表分类扩展进程租户隔离；全局身份排除；JDBC显式谓词；统一显式环境配置，禁止缺省回落0，不把全局表机械加tenant。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[BaseDaoImpl.java:107](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/common/jia-common-mapper/src/main/java/cn/jia/common/dao/BaseDaoImpl.java#L107)|L107 `return baseMapper.deleteById(id);`；L112 `return baseMapper.deleteBatchIds(idList);`；L118 `return baseMapper.updateById(entity);`|已有局部修改，仍未收口|
|[TaskTenantConfiguration.java:31](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/task/jia-task-service/src/main/java/cn/jia/task/config/TaskTenantConfiguration.java#L31)|L31 `@Value("${cyf.security.legacy-single-tenant-id:0}") String legacyTenant,`；L43 `private final Set<String> tables = Set.of("task_plan", "task_item", "v_task_item");`；L57 `return statement.getId().startsWith("cn.jia.task.mapper.");`|已有局部修改，仍未收口|
|[FixedTenantAdmissionPolicy.java:14](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/common/jia-common-core/src/main/java/cn/jia/core/security/FixedTenantAdmissionPolicy.java#L14)|L14 `public FixedTenantAdmissionPolicy(String legacyTenantId, boolean enabled,`；L21 `if (this.legacyTenantId.equals(this.tenantId)) {`；L31 `public String tenantForClient(String registeredClientId) {`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [BaseDaoTenantQueryTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/common/jia-common-mapper/src/test/java/cn/jia/common/dao/BaseDaoTenantQueryTest.java)
- [FixedTenantAdmissionPolicyTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/common/jia-common-core/src/test/java/cn/jia/core/security/FixedTenantAdmissionPolicyTest.java)

待补测试：补真实SQL的按ID/批量/空条件/insertOrUpdate/分页count和异步线程双向隔离；global user/OAuth不加tenant；任意合法环境值、无配置拒绝。

### 02 SYSTEM运行身份与预置定义拆分

现状：SYSTEM身份查询和身份DDL仍把全局SYSTEM表达为业务tenant0，独立DDL的普通身份/alias/binding仍存在单租户形状。

修复：源码公共定义不绑定业务tenant；实际运行、绑定和会话绑定环境tenant；同步registry读写与新建/维护DDL，移除旧形状执行入口，不删除历史事实。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[AgentIdentityRegistryDaoImpl.java:81](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentIdentityRegistryDaoImpl.java#L81)|L81 `&& !"0".equals(tenantId)) {`|此文件未修改|
|[agent-identity-business-tenant-20261030.sql:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/agent-identity-business-tenant-20261030.sql#L10)|L10 `AND client_id IS NULL AND owner_jiacn IS NULL AND tenant_id = '0')`；L22 `DROP CHECK chk_agent_binding_single_tenant,`；L23 `ADD CONSTRAINT chk_agent_binding_single_tenant CHECK (tenant_id IS NOT NULL AND CHAR_LENGTH(tenant_id)>0 AND OCTET_LENGTH(tenant_id)=OCTET_LENGTH(TRIM(tenant_id)));`|已有局部修改，仍未收口|
|[agent-identity-schema.sql:47](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/agent-identity-schema.sql#L47)|L47 `AND client_id IS NULL AND owner_jiacn IS NULL AND tenant_id = '0')`；L51 `AND tenant_id = '0')`；L87 `CONSTRAINT chk_identity_alias_scope CHECK (tenant_id = '0'),`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [WaterMarginPersonaCatalogTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-core/src/test/java/cn/jia/agent/common/WaterMarginPersonaCatalogTest.java)
- [AgentPersonaCatalogCacheTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/test/java/cn/jia/agent/cache/AgentPersonaCatalogCacheTest.java)

待补测试：补SYSTEM定义共享只读、各环境runtime/identity独立、禁止灰度修改全局及生产绑定；保留私有覆盖隔离。

### 03 托管与场景及Agent旧重载

现状：仍有默认0重载、requireLegacyHostedTenant、非0拒绝、场景写0和usesLegacyTaskStats生产分支。persona元数据已改不等于整个托管链路已改。

修复：删除无scope业务重载，同步调用方；从准入/运行绑定传tenant/client/owner到托管事务、发布、场景和统计；保留身份、锁顺序和租金条件。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[AgentRuntimeDao.java:20](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/AgentRuntimeDao.java#L20)|L20 `return findRosterByOwner("0", clientId, jiacn, status, ability);`；L25 `return findCandidateRosterByOwner("0", clientId, jiacn);`；L32 `default List<AgentRuntimeEntity> findMapVisible(String clientId) { return findMapVisible("0", clientId); }`|此文件未修改|
|[AgentHostedProfileDaoImpl.java:65](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentHostedProfileDaoImpl.java#L65)|L65 `if (!"0".equals(tenantId) \|\| "0".equals(ownerJiacn)) {`|此文件未修改|
|[AgentHostedBindingTransaction.java:73](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentHostedBindingTransaction.java#L73)|L73 `scope.requireLegacyHostedTenant();`；L150 `scope.requireLegacyHostedTenant();`；L180 `scope.requireLegacyHostedTenant();`|已有局部修改，仍未收口|
|[AgentHostedProfilePublisher.java:404](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentHostedProfilePublisher.java#L404)|L404 `scope.requireLegacyHostedTenant();`|此文件未修改|
|[AgentPersonaProvisioningService.java:34](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentPersonaProvisioningService.java#L34)|L34 `scope.requireLegacyHostedTenant();`；L40 `scope.requireLegacyHostedTenant();`；L60 `scope.requireLegacyHostedTenant();`|此文件未修改|
|[AgentSceneEventBroker.java:109](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentSceneEventBroker.java#L109)|L109 `if (!"0".equals(tenantId)) {`|此文件未修改|
|[AgentSceneServiceImpl.java:711](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentSceneServiceImpl.java#L711)|L711 `String tenantId = "0";`|此文件未修改|
|[AgentServiceImpl.java:117](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java#L117)|L117 `private static final String SINGLE_TENANT_ID = "0";`；L119 `new cn.jia.core.security.FixedTenantAdmissionPolicy("0", false, null, null);`；L655 `SINGLE_TENANT_ID, clientId, jiacn, agentId), clientId, jiacn);`|已有局部修改，仍未收口|

相关测试源码（均未执行，不是已覆盖证明）：
- [AgentHostedBindingTransactionTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/AgentHostedBindingTransactionTest.java)
- [AgentHostedProfilePublisherTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/AgentHostedProfilePublisherTest.java)
- [AgentSceneEventBrokerTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/AgentSceneEventBrokerTest.java)
- [AgentServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentServiceImplTest.java)
- [AgentHostedProfileMySqlTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentHostedProfileMySqlTest.java)

待补测试：补非数字tenant的托管/恢复/解绑/场景/统计；同owner跨环境互拒；保留事务回滚和已修改persona fixture。

### 04 创建任务、需求确认与协作

现状：各服务scope条件仍要求tenant为0。

修复：改为可信准入scope并逐层比对任务根、owner/client和授权；不简单删除安全条件；幂等键按环境分区。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[AgentTaskCreationOperationServiceImpl.java:523](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskCreationOperationServiceImpl.java#L523)|L523 `if (scope == null \|\| !"0".equals(scope.tenantId())`|此文件未修改|
|[AgentTaskRequirementSnapshotServiceImpl.java:269](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskRequirementSnapshotServiceImpl.java#L269)|L269 `if (!"0".equals(scope.tenantId()))`|已有局部修改，仍未收口|
|[AgentCollaborationRequestServiceImpl.java:156](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentCollaborationRequestServiceImpl.java#L156)|L156 `if (scope == null \|\| !"0".equals(scope.tenantId()) \|\| !isExact(scope.clientId(), 50)`|此文件未修改|
|[AgentTaskDeliberationOperationReadServiceImpl.java:471](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskDeliberationOperationReadServiceImpl.java#L471)|L471 `if (scope == null \|\| !"0".equals(scope.tenantId())) {`|此文件未修改|
|[AgentTaskPointAndStartPolicyServiceImpl.java:69](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskPointAndStartPolicyServiceImpl.java#L69)|L69 `if (scope == null \|\| !"0".equals(scope.tenantId())) throw new IllegalArgumentException();`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [AgentTaskCreationOperationServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskCreationOperationServiceImplTest.java)
- [AgentTaskCreationOperationMySqlTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskCreationOperationMySqlTest.java)
- [AgentTaskCreationOperationRealTransactionTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskCreationOperationRealTransactionTest.java)

待补测试：补创建/重试/重确认/协作同域成功、跨域失败、各环境幂等互不影响；需要把同组其余服务测试一起纳入既有入口。

### 05 Hall创建、草稿、私有案例与标记

现状：DAO和服务仍拒绝非0；控制器tenant解析已改，服务链仍未完成。

修复：DAO、草稿提交、案例/标记和Hall任务创建共同传scope；当前租户查/写/锁/CAS；保留ACL及版本冲突。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[HallPrivateCaseDaoImpl.java:87](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/HallPrivateCaseDaoImpl.java#L87)|L87 `if (!"0".equals(tenant)) throw new IllegalArgumentException("tenantId");`|此文件未修改|
|[HallRequestDraftDaoImpl.java:130](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/HallRequestDraftDaoImpl.java#L130)|L130 `if (!"0".equals(tenant)) throw new IllegalArgumentException("tenantId");`|此文件未修改|
|[HallPrivateMarkServiceImpl.java:151](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/HallPrivateMarkServiceImpl.java#L151)|L151 `if (scope==null \|\| !"0".equals(scope.tenantId()) \|\| "0".equals(scope.ownerJiacn())) throw failure(Reason.BAD_REQUEST);`|此文件未修改|
|[HallReadServiceImpl.java:251](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/HallReadServiceImpl.java#L251)|L251 `if (scope == null \|\| !"0".equals(scope.tenantId()) \|\| !id(scope.clientId(), 50)`|此文件未修改|
|[HallRequestDraftServiceImpl.java:1217](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/HallRequestDraftServiceImpl.java#L1217)|L1217 `if (scope == null \|\| !"0".equals(scope.tenantId())) throw failure(Reason.BAD_REQUEST);`|此文件未修改|
|[HallTaskCreationServiceImpl.java:126](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/HallTaskCreationServiceImpl.java#L126)|L126 `if (scope == null \|\| !"0".equals(scope.tenantId())`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [HallReadServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/HallReadServiceImplTest.java)
- [HallRequestDraftServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/HallRequestDraftServiceImplTest.java)
- [HallTaskCreationServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/HallTaskCreationServiceImplTest.java)
- [HallRequestDraftSubmissionMySqlTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/HallRequestDraftSubmissionMySqlTest.java)
- [HallReadTaskCreateMySqlTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/HallReadTaskCreateMySqlTest.java)

待补测试：补双环境草稿/提交/私有case/mark隔离、并发提交、同业务键跨租户、mapper与真实MySQL。

### 06 成果、正式交付与返工

现状：服务scope仍限定0，虽然HTTP actor解析已改。

修复：贯通成果来源、任务根、决策、finalization及rework租户；历史成果只读校验不重算摘要、不重放执行。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[ConversationDeliverableReadAdapter.java:172](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/conversation/ConversationDeliverableReadAdapter.java#L172)|L172 `if (scope == null \|\| !"0".equals(scope.tenantId())) throw new Failure(Reason.BAD_REQUEST);`|此文件未修改|
|[AgentSelectedOutputFinalizationServiceImpl.java:712](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentSelectedOutputFinalizationServiceImpl.java#L712)|L712 `if(s==null\|\|!"0".equals(s.tenantId()))throw notFound();`|此文件未修改|
|[AgentTaskFormalDeliveryDecisionServiceImpl.java:407](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskFormalDeliveryDecisionServiceImpl.java#L407)|L407 `if (!"0".equals(tenant) \|\| "0".equals(client) \|\| "0".equals(owner)) {`|此文件未修改|
|[AgentTaskFormalDeliveryReadServiceImpl.java:170](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskFormalDeliveryReadServiceImpl.java#L170)|L170 `if (!"0".equals(tenantId) \|\| !exact(clientId, 50) \|\| "0".equals(clientId)`|此文件未修改|
|[AgentTaskFormalDeliveryServiceImpl.java:541](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskFormalDeliveryServiceImpl.java#L541)|L541 `if (!"0".equals(tenantId) \|\| "0".equals(clientId) \|\| "0".equals(ownerJiacn)`|此文件未修改|
|[AgentTaskReworkExecutionServiceImpl.java:135](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskReworkExecutionServiceImpl.java#L135)|L135 `if (scope == null \|\| !"0".equals(scope.tenantId())) throw badRequest();`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [AgentTaskFormalDeliveryServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskFormalDeliveryServiceImplTest.java)
- [AgentTaskFormalDeliveryDecisionServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskFormalDeliveryDecisionServiceImplTest.java)
- [AgentTaskReworkExecutionServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskReworkExecutionServiceImplTest.java)
- [AgentTaskFormalDeliveryMapperContractTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/test/java/cn/jia/agent/dao/AgentTaskFormalDeliveryMapperContractTest.java)

待补测试：补同域交付/读取/采纳/返工及跨域拒绝；保留幂等、版本、成果摘要和历史只读。

### 07 资金业务和预览scope

现状：创建/claim/结算仍显式tenantId must be 0；preview构造Principal使用owner及多个0，不可把金额0/owner保留值混同tenant。

修复：统一环境业务scope贯穿quote、claim、预留、结算；逐字段核对钱包历史owner-as-tenant语义后同步读写，禁止机械替换数字。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[FundedBountyQuoteClaimServiceImpl.java:603](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/funding/FundedBountyQuoteClaimServiceImpl.java#L603)|L603 `if (!"0".equals(actor.tenantId())) throw badRequest("tenantId must be 0");`|此文件未修改|
|[FundedBountyServiceImpl.java:530](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/funding/FundedBountyServiceImpl.java#L530)|L530 `if (!"0".equals(actor.tenantId())) throw badRequest("tenantId must be 0");`|此文件未修改|
|[FundedBountySettlementServiceImpl.java:256](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/funding/FundedBountySettlementServiceImpl.java#L256)|L256 `if (!"0".equals(actor.tenantId())) throw bad("tenantId must be 0");`|此文件未修改|
|[EconomyReadOnlyPreviewController.java:166](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/api/EconomyReadOnlyPreviewController.java#L166)|L166 `return new Principal(ownerJiacn, "0", "0", "0", clientId, ownerJiacn, actorId);`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [FundedBountyQuoteClaimServiceTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/funding/FundedBountyQuoteClaimServiceTest.java)
- [FundedBountyQuoteClaimRealTransactionTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/funding/FundedBountyQuoteClaimRealTransactionTest.java)
- [FundedBountyServiceRealTransactionTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/funding/FundedBountyServiceRealTransactionTest.java)
- [FundedBountySettlementRealTransactionTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/funding/FundedBountySettlementRealTransactionTest.java)

待补测试：同owner不同环境钱包/quote/结算互不影响，幂等、余额和事务不回归；仅替身资金，不真实扣费。

### 08 能力评估持久化

现状：evaluate新写已带scope；history/latest按名称、stats全量、delete按裸ID；comparison写入未设tenant/client。

修复：评估和比较的全部读写使用环境scope，禁止借同名persona/裸ID跨域读取删除；接口、DAO和实体字段一起收口。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[AbilityEvaluationServiceImpl.java:41](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AbilityEvaluationServiceImpl.java#L41)|L41 `public AbilityEvaluationDTO evaluate(AbilityEvaluationRequestDTO request) {`；L44 `abilityEvaluationDao.insert(entity);`；L50 `public AbilityCompareResultDTO compare(AbilityCompareRequestDTO request) {`|已有局部修改，仍未收口|
|[AbilityEvaluationDaoImpl.java:16](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AbilityEvaluationDaoImpl.java#L16)|L16 `public List<AbilityEvaluationEntity> findByAgentName(String agentName) {`；L17 `return baseMapper.selectList(new LambdaQueryWrapper<AbilityEvaluationEntity>()`；L18 `.eq(AbilityEvaluationEntity::getAgentName, agentName)`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [AbilityEvaluationServiceImplTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AbilityEvaluationServiceImplTest.java)

待补测试：覆盖history/latest/stats/delete/compare，而不止evaluate；两环境同名Agent、不相等tenant和owner、跨域ID。

### 09 技能安装、回执和版本

现状：安装/下载/回执仍只接受0，roster有LEGACY_SKILL_TENANT分支；SkillAgentVersions向Mapper tenantId参数传ownerJiacn，find/ensure/lock/advance均涉及。

修复：命令、proof、installation、delivery逐一比对真实环境；版本记录将tenant与owner分离，沿现有CAS和事务，不新增版本表双轨。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[SkillInstallCommandWriter.java:23](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillInstallCommandWriter.java#L23)|L23 `public boolean allows(String tenant,String client) { return "0".equals(tenant) && preview.allows(tenant,client); }`|此文件未修改|
|[SkillInstallRecoveryService.java:41](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillInstallRecoveryService.java#L41)|L41 `require("0".equals(hint.getTenantId()) && preview.allows(hint.getTenantId(),hint.getClientId()),403,"SKILL_DELIVERY_FENCED");`|此文件未修改|
|[SkillInstallResultService.java:53](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillInstallResultService.java#L53)|L53 `require(proof!=null && "0".equals(proof.scope().tenantId()),403,"SKILL_RESULT_REJECTED");`；L135 `require(proof!=null && "0".equals(proof.scope().tenantId()),403,"SKILL_DOWNLOAD_FORBIDDEN");`；L163 `require(d!=null && "0".equals(i.getTenantId()) && "0".equals(d.getTenantId())`|此文件未修改|
|[SkillRosterProjection.java:22](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillRosterProjection.java#L22)|L22 `private static final String LEGACY_SKILL_TENANT = "0";`；L40 `if (scope != null && LEGACY_SKILL_TENANT.equals(scope.tenantId())) {`；L63 `AgentRuntimeDTO trusted = LEGACY_SKILL_TENANT.equals(scope.tenantId())`|已有局部修改，仍未收口|
|[SkillAgentVersions.java:50](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillAgentVersions.java#L50)|L50 `var state=mapper.findVersion(actor.ownerJiacn(),actor.clientId(),agentId);`；L62 `mapper.ensureVersion(row.getOwnerJiacn(),row.getClientId(),row.getAgentId(),hash);`；L63 `var state=mapper.lockVersion(row.getOwnerJiacn(),row.getClientId(),row.getAgentId());`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [SkillInstallRecoveryServiceTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillInstallRecoveryServiceTest.java)
- [SkillInstallResultContractTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillInstallResultContractTest.java)
- [SkillInstallTransportMySqlTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillInstallTransportMySqlTest.java)
- [AgentGetSkillRosterProjectionTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/AgentGetSkillRosterProjectionTest.java)
- [SkillAgentVersionsTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillAgentVersionsTest.java)

待补测试：tenant与owner不同的fixture；同owner/client/agent版本分区；安装/下载/ACK跨域拒绝及重复回执不重复生效。

### 10 后台发现、领取和状态转换

现状：技能恢复candidates无进程tenant且LIMIT25；租金两条pending扫描无tenant且LIMIT100；状态monitor全局扫描、transition限定0；deliberation仍legacy配置。

修复：SQL在排序/LIMIT前按进程tenant过滤，领取/CAS再核对同域；后台显式注入scope，不依赖HTTP ThreadLocal；不能跨环境领取后过滤。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[AgentSkillInstallRecoveryMapper.java:22](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/mapper/AgentSkillInstallRecoveryMapper.java#L22)|L22 `ORDER BY d.update_time,d.id LIMIT 25`；L24 `List<AgentCommandDeliveryEntity> candidates(@Param("now") long now,@Param("before") long before);`|此文件未修改|
|[AgentStatusMonitor.java:37](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentStatusMonitor.java#L37)|L37 `for (AgentRuntimeEntity candidate : agentRuntimeDao.findHeartbeatTimedOut(cutoffTime)) {`；L59 `List<AgentRuntimeEntity> candidates = agentRuntimeDao.findByStatusAndAbility(null, null);`|此文件未修改|
|[AgentStatusTransitionWorker.java:161](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentStatusTransitionWorker.java#L161)|L161 `&& "0".equals(binding.getTenantId())`；L171 `&& "0".equals(identity.getTenantId())`|此文件未修改|
|[EconomyHostingRentMapper.java:314](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/economy/jia-economy-mapper/src/main/java/cn/jia/economy/mapper/EconomyHostingRentMapper.java#L314)|L314 `+ " AND id>#{afterId} ORDER BY id LIMIT 100")`；L315 `java.util.List<EconomyHostingProvisioningIntentEntity> selectPendingIntents(@Param("afterId") long afterId);`；L403 `@Select("SELECT * FROM economy_hosting_reprovision WHERE live_slot=1 AND id>#{afterId} ORDER BY id LIMIT 100")`|此文件未修改|
|[ChatDeliberationOutboxService.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatDeliberationOutboxService.java#L21)|L21 `private String legacyTenantId = "0";`；L28 `requireExact(legacyTenantId, 50);`；L29 `return dao.findDueOutboxInTenant(legacyTenantId, now, Math.max(1, Math.min(limit, 32)));`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [SkillInstallTransportMySqlTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillInstallTransportMySqlTest.java)
- [AgentStatusMonitorTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/service/AgentStatusMonitorTest.java)
- [HostingRentReconcilerTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/hosting/HostingRentReconcilerTest.java)

待补测试：把外租户记录排在LIMIT前，验证不饥饿、不领取、不修改；租金pending/reprovision、超时状态和outbox均覆盖。

### 11 Chat会话及任务线程

现状：默认0重载、消息发现固定0、task thread及capability入口固定0/拒绝非0。

修复：删除默认业务scope重载，统一准入上下文贯穿会话读取/删除、成员授权、memory发现和任务线程；不改全局ID规则。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[ChatConversationService.java:26](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-api/src/main/java/cn/jia/chat/service/ChatConversationService.java#L26)|L26 `return getOwned("0", ownerJiacn, clientId, conversationId);`；L35 `return isLiveGeneration("0", ownerJiacn, clientId, conversationId, expectedGeneration);`；L44 `return findOwnedMessages("0", ownerJiacn, clientId, conversationId);`|此文件未修改|
|[ChatConversationDao.java:11](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/ChatConversationDao.java#L11)|L11 `return findScopedById("0", ownerJiacn, clientId, conversationId);`；L17 `return lockScopedById("0", ownerJiacn, clientId, conversationId);`；L23 `return lockScopedByIdIncludingDeleted("0", ownerJiacn, clientId, conversationId);`|此文件未修改|
|[ChatMessageDao.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/ChatMessageDao.java#L18)|L18 `return findOwnedByConversationId("0", ownerJiacn, clientId, conversationId);`；L24 `return findOwnedByConversationIdWithLimit("0", ownerJiacn, clientId, conversationId, limit);`；L31 `return deleteExactOwnedConversationMessages("0", ownerJiacn, clientId, conversationId);`|此文件未修改|
|[ChatMessageDaoImpl.java:22](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/impl/ChatMessageDaoImpl.java#L22)|L22 `private static final String SINGLE_TENANT = "0";`；L102 `wrapper.eq(ChatMessageEntity::getTenantId, SINGLE_TENANT)`；L132 `wrapper.eq(ChatMessageEntity::getTenantId, SINGLE_TENANT)`|此文件未修改|
|[ChatMessageMapper.java:51](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/mapper/ChatMessageMapper.java#L51)|L51 `WHERE c.deleted_at IS NULL AND c.tenant_id = '0'`|此文件未修改|
|[AgentTaskPointAndStartCapabilityController.java:101](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/api/AgentTaskPointAndStartCapabilityController.java#L101)|L101 `return new AgentTaskExecutionGrantService.Scope("0", clientId, ownerJiacn);`|此文件未修改|
|[AgentTaskThreadController.java:96](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/api/AgentTaskThreadController.java#L96)|L96 `return new Scope("0", context.getClientId(), context.getJiacn());`|此文件未修改|
|[TaskSkillCapabilityController.java:35](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/api/TaskSkillCapabilityController.java#L35)|L35 `if(!"0".equals(tenant)\|\|sender==null\|\|!ServerResolvedSender.USER_TYPE.equals(sender.type())\|\|!exact(taskId)\|\|!exact(targetAgentId))throw missing();`|此文件未修改|
|[AgentTaskThreadServiceImpl.java:271](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/impl/AgentTaskThreadServiceImpl.java#L271)|L271 `if (!"0".equals(tenantId)) {`|此文件未修改|
|[ChatConversationServiceImpl.java:181](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/impl/ChatConversationServiceImpl.java#L181)|L181 `if (!"0".equals(context.getTenantId())) {`；L196 `if (task == null \|\| !taskId.equals(task.getId()) \|\| !"0".equals(task.getTenantId())`；L219 `if (bound == null \|\| bound.getDeletedAt() != null \|\| !"0".equals(bound.getTenantId())`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [ChatMessageScopedQueryTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/test/java/cn/jia/chat/dao/ChatMessageScopedQueryTest.java)
- [ChatConversationTaskThreadGuardTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/service/ChatConversationTaskThreadGuardTest.java)

待补测试：补会话/消息读取删除、任务线程、成员校验和capability两环境隔离；所有旧签名fixture同步。

### 12 WS、讨论与完成事实

现状：WS、bootstrap、discussion、completed source及finalization仍有0限定/默认0调用。

修复：按已认证session/runtime/task根scope验证；历史final事实保留原摘要；不得为灰度恢复退役写协议。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[AgentWebSocketHandler.java:633](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java#L633)|L633 `return payload.containsKey("tenantId") && !"0".equals(strictString(payload.get("tenantId")))`；L1987 `Set<String> memberAgentIds = "0".equals(task.getTenantId())`；L2723 `boolean ownerScopedTask = taskScope != null && "0".equals(taskScope.tenantId());`|此文件未修改|
|[ChatActionFinalValidator.java:124](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatActionFinalValidator.java#L124)|L124 `if (value == null \|\| !value.keySet().equals(BINDING_KEYS) \|\| !"0".equals(value.get("tenantId"))`|此文件未修改|
|[ChatBountyBootstrapAdmissionService.java:89](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapAdmissionService.java#L89)|L89 `if (claim == null \|\| !"0".equals(claim.tenantId())`|此文件未修改|
|[ChatBountyConversationService.java:38](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyConversationService.java#L38)|L38 `if (scope==null \|\| !"0".equals(scope.tenantId())`|此文件未修改|
|[ChatBountyDiscussionAdmissionService.java:52](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyDiscussionAdmissionService.java#L52)|L52 `if (!"0".equals(tenantId) \|\| sender == null \|\| !ServerResolvedSender.USER_TYPE.equals(sender.type())`|此文件未修改|
|[ChatBountyRequestIndexService.java:80](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyRequestIndexService.java#L80)|L80 `if (!"0".equals(tenantId)) throw notFound();`|此文件未修改|
|[ChatCompletedMessageSourceService.java:91](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatCompletedMessageSourceService.java#L91)|L91 `if(owner==null \|\| !"0".equals(owner.tenantId())) throw unavailable();`|此文件未修改|
|[ChatSelectedOutputFinalizationService.java:461](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatSelectedOutputFinalizationService.java#L461)|L461 `if(s==null\|\|!"0".equals(s.tenantId())\|\|!safeId(s.clientId(),50)\|\|!safeId(s.ownerJiacn(),50)`|此文件未修改|
|[ChatTypedDiscussionAdmissionService.java:90](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatTypedDiscussionAdmissionService.java#L90)|L90 `if(!"0".equals(tenantId)\|\|sender==null\|\|!ServerResolvedSender.USER_TYPE.equals(sender.type())`|此文件未修改|
|[HallActionDispatcher.java:305](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/HallActionDispatcher.java#L305)|L305 `if (!"0".equals(caller.tenantId())) {`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [AgentWebSocketHandlerSecurityTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/handler/AgentWebSocketHandlerSecurityTest.java)
- [AgentWebSocketRuntimeAuthenticationTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/handler/AgentWebSocketRuntimeAuthenticationTest.java)
- [AgentWebSocketExecutionReportTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/juyitingExecutionReportTest/java/cn/jia/chat/handler/AgentWebSocketExecutionReportTest.java)

待补测试：两环境WS/session/任务成员、final/ACK绑定；生产golden不变；历史记录仅同域读取、不自动重放。

### 13 长期记忆和内部工具调用

现状：文档缺tenant/client；检索主要按jiacn，清理/统计接口未带环境；服务、advisor/job/tool链仍调用该接口，部分会话条件限定0。

修复：文档/序列化/检索/摘要/删除/count及job均显式scope；topK之前过滤；环境索引隔离；内部tool不得绕开服务隔离；不迁无归属旧数据。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[MemoryDocument.java:26](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/memory/MemoryDocument.java#L26)|L26 `private String jiacn;`|此文件未修改|
|[MemoryRepository.java:42](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/memory/MemoryRepository.java#L42)|L42 `List<MemoryDocument> searchWithConversationBoost(String jiacn, String userMessage, String currentConversationId, int topK, double similarityThreshold);`；L52 `List<MemoryDocument> search(String jiacn, float[] queryVector, int topK);`；L61 `List<String> findConversationSummariesByJiacn(String jiacn, long sinceTime);`|此文件未修改|
|[MemoryRepositoryImpl.java:107](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/memory/MemoryRepositoryImpl.java#L107)|L107 `public List<MemoryDocument> searchWithConversationBoost(String jiacn, String userMessage,`；L124 `.filter(f -> f.term(t -> t.field("jiacn").value(jiacn)))`；L176 `public List<MemoryDocument> search(String jiacn, float[] queryVector, int topK) {`|此文件未修改|
|[LongTermMemoryService.java:31](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-api/src/main/java/cn/jia/chat/service/LongTermMemoryService.java#L31)|L31 `void syncOwnedConversation(String ownerJiacn, String clientId, String conversationId);`|此文件未修改|
|[LongTermMemoryServiceImpl.java:93](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/service/impl/LongTermMemoryServiceImpl.java#L93)|L93 `public void syncConversation(String conversationId) {`；L111 `public void syncOwnedConversation(String ownerJiacn, String clientId, String conversationId) {`；L114 `syncOwnedSnapshot(ownerJiacn, clientId, conversationId);`|此文件未修改|
|[LongTermMemoryAdvisor.java:87](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/advisor/LongTermMemoryAdvisor.java#L87)|L87 `memoryRepository.searchWithConversationBoost(`|此文件未修改|
|[MemoryJobHandler.java:113](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/job/MemoryJobHandler.java#L113)|L113 `longTermMemoryService.syncPendingConversations();`；L118 `longTermMemoryService.generateDailySummary();`；L124 `longTermMemoryService.generateWeeklySummary();`|此文件未修改|
|[ChatTools.java:77](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/tool/ChatTools.java#L77)|L77 `longTermMemoryService.syncOwnedConversation(`；L84 `longTermMemoryService.generateDailySummary();`；L90 `longTermMemoryService.generateWeeklySummary();`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [MemoryRepositoryIsolationTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/memory/MemoryRepositoryIsolationTest.java)
- [LongTermMemoryTaskThreadIsolationTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/service/LongTermMemoryTaskThreadIsolationTest.java)

待补测试：同owner跨tenant/client的search/summary/count/delete；mock embedding，无付费provider；后台无HTTP上下文。

### 14 归档scope、HTTP和后台

现状：ArchiveOwnerScope构造器把入参覆盖成SINGLE_TENANT=0；HTTP显式0；SQL发现固定0，worker验证也固定0。

修复：scope保留并校验准入tenant；HTTP/reader/question/outbox/worker全链传递；私有笔记和问题隔离，公共出版内容只读，不能以私有表隔离放开全局维护。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[ArchiveOwnerScope.java:5](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-core/src/main/java/cn/jia/chat/archive/model/ArchiveOwnerScope.java#L5)|L5 `public static final String SINGLE_TENANT = "0";`；L12 `tenantId = SINGLE_TENANT;`|此文件未修改|
|[JdbcArchiveQuestionStore.java:254](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/archive/store/JdbcArchiveQuestionStore.java#L254)|L254 `WHERE tenant_id='0'`；L278 `WHERE tenant_id='0'`；L298 `WHERE o.tenant_id='0'`|此文件未修改|
|[ArchivePersonalDataController.java:200](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/http/ArchivePersonalDataController.java#L200)|L200 `return new Authorization(new ArchiveOwnerScope(ArchiveOwnerScope.SINGLE_TENANT, clientId, jiacn), null);`|此文件未修改|
|[ArchiveQuestionController.java:132](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/http/ArchiveQuestionController.java#L132)|L132 `return new Authorization(new ArchiveOwnerScope(ArchiveOwnerScope.SINGLE_TENANT, clientId, ownerJiacn), null);`|此文件未修改|
|[ArchiveQuestionWorker.java:561](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/service/ArchiveQuestionWorker.java#L561)|L561 `&& ArchiveOwnerScope.SINGLE_TENANT.equals(owner.tenantId())`；L562 `&& !ArchiveOwnerScope.SINGLE_TENANT.equals(owner.ownerJiacn())`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [JdbcArchiveQuestionStoreTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/test/java/cn/jia/chat/archive/store/JdbcArchiveQuestionStoreTest.java)
- [ArchiveQuestionControllerTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/http/ArchiveQuestionControllerTest.java)
- [ArchiveQuestionWorkerTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/service/ArchiveQuestionWorkerTest.java)
- [ArchiveQuestionMySqlIntegrationTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/service/ArchiveQuestionMySqlIntegrationTest.java)
- [ArchiveReaderDataMySqlIntegrationTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/service/ArchiveReaderDataMySqlIntegrationTest.java)

待补测试：构造scope不覆写；进度/bookmark/note/幂等/question/event/outbox跨域互拒；发现和领取真实SQL。

### 15 活跃DDL与Schema校验

现状：14张活跃表仍有tenant=0 CHECK；源DDL与initializer/catalog必须同步，不能只改Java放行。

修复：改为明确合法scope约束，维护脚本与新建DDL一致；覆盖唯一键、外键、现存行、重复执行及部分失败；不得启动时自动灰度DDL。

| 文件及当前行 | 当前源码证据（截取） | 工作区状态 |
|---|---|---|
|[agent-command-transport-schema.sql:40](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/agent-command-transport-schema.sql#L40)|L40 `CONSTRAINT chk_delivery_single_tenant CHECK (tenant_id = '0'),`|此文件未修改|
|[agent-skill-execution-v1.sql:25](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/agent-skill-execution-v1.sql#L25)|L25 `CONSTRAINT chk_skill_execution_scope CHECK (tenant_id='0' AND owner_jiacn<>'0'),`|此文件未修改|
|[hall-private-case-v1.sql:15](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/hall-private-case-v1.sql#L15)|L15 `CONSTRAINT chk_hall_case_tenant CHECK (tenant_id='0'),`；L36 `CONSTRAINT chk_hall_case_execution_tenant CHECK (tenant_id='0'),`|此文件未修改|
|[hall-private-mark-v1.sql:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/hall-private-mark-v1.sql#L21)|L21 `CONSTRAINT chk_hall_private_mark_tenant CHECK (tenant_id='0'),`|此文件未修改|
|[hall-request-draft-v1.sql:39](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/resources/db/hall-request-draft-v1.sql#L39)|L39 `CONSTRAINT chk_hall_draft_tenant CHECK (tenant_id = '0'),`|此文件未修改|
|[SkillExecutionSchemaInitializer.java:71](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/main/java/cn/jia/agent/config/SkillExecutionSchemaInitializer.java#L71)|L71 `"chk_skill_execution_scope","((tenant_id = '0') and (owner_jiacn <> '0'))",`|此文件未修改|
|[archive-question-schema.sql:27](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/resources/db/archive-question-schema.sql#L27)|L27 `CONSTRAINT chk_archive_question_single_tenant CHECK (tenant_id = '0'),`；L66 `CONSTRAINT chk_archive_question_mutation_single_tenant CHECK (tenant_id = '0'),`；L94 `CONSTRAINT chk_archive_question_event_single_tenant CHECK (tenant_id = '0'),`|此文件未修改|
|[archive-reader-data-schema.sql:19](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/resources/db/archive-reader-data-schema.sql#L19)|L19 `CONSTRAINT chk_archive_progress_single_tenant CHECK (tenant_id = '0'),`；L51 `CONSTRAINT chk_archive_bookmark_single_tenant CHECK (tenant_id = '0'),`；L83 `CONSTRAINT chk_archive_note_single_tenant CHECK (tenant_id = '0'),`|此文件未修改|
|[ArchiveQuestionSchemaCatalog.java:54](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveQuestionSchemaCatalog.java#L54)|L54 `"chk_archive_question_single_tenant", "tenant_id = '0'",`；L89 `"chk_archive_question_mutation_single_tenant", "tenant_id = '0'",`；L116 `"chk_archive_question_event_single_tenant", "tenant_id = '0'",`|此文件未修改|
|[ArchiveReaderDataSchemaCatalog.java:43](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/config/ArchiveReaderDataSchemaCatalog.java#L43)|L43 `"chk_archive_progress_single_tenant", "tenant_id = '0'",`；L75 `"chk_archive_bookmark_single_tenant", "tenant_id = '0'",`；L107 `"chk_archive_note_single_tenant", "tenant_id = '0'",`|此文件未修改|

相关测试源码（均未执行，不是已覆盖证明）：
- [ArchiveQuestionSchemaResourceTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/test/java/cn/jia/chat/archive/schema/ArchiveQuestionSchemaResourceTest.java)
- [ArchiveReaderDataSchemaResourceTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/test/java/cn/jia/chat/archive/schema/ArchiveReaderDataSchemaResourceTest.java)
- [ArchiveQuestionSchemaInitializerTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/config/ArchiveQuestionSchemaInitializerTest.java)
- [ArchiveReaderDataSchemaInitializerTest.java](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/config/ArchiveReaderDataSchemaInitializerTest.java)

待补测试：owned MySQL fresh/旧库形状/二次执行/错误恢复/跨租户重复业务键；检查SQL而不是仅字符串测试。

### 16 Runtime与Web

- [shell/cyf_agent_runtime_v1_install.sh](/home/isp/wsps/chcbz/isp-install/shell/cyf_agent_runtime_v1_install.sh)：固定cyf-agent-runtime-v1子目录且灰度独立根只有TEST入口；增加正式可选应用根，生产默认不变。
  - L8 `APP_ROOT="${ISP_APPS:-/home/isp/apps}/cyf-agent-runtime-v1"`
  - L11 `APP_ROOT="$CYF_RUNTIME_V1_TEST_APP_ROOT/cyf-agent-runtime-v1"`
- [systemd/cyf-agent-runtime-v1@.service](/home/isp/wsps/chcbz/isp-install/systemd/cyf-agent-runtime-v1@.service)：程序根固定生产路径，实例名只改变配置；生成/配置独立灰度unit，分开app/config/state/HOME/identity/session/ACK/端口。
  - L9 `WorkingDirectory=/home/isp/apps/cyf-agent-runtime-v1/app`
  - L12 `ExecStartPre=/home/isp/apps/cyf-agent-runtime-v1/app/runtime/validate.sh --root /home/isp/apps/cyf-agent-runtime-v1/app --config /home/isp/conf/cyf-agent-runtime-v1/%i.host.json`
  - L13 `ExecStart=/home/isp/apps/cyf-agent-runtime-v1/app/node/bin/node /home/isp/apps/cyf-agent-runtime-v1/app/runtime/agent-runtime.mjs run --config /home/isp/conf/cyf-agent-runtime-v1/%i.host.json`
- [src/components/workspace/PersonalWorkspace.vue](/home/isp/wsps/cyf/web/src/components/workspace/PersonalWorkspace.vue)：executionIdentityScope在缺tenant时仍能拼出client+owner；复用完整identityScope helper，未就绪不请求，切换清理/取消旧请求。
  - L230 `const executionIdentityScope = computed(() => {`
  - L234 `return owner && client ? [tenant, client, owner].filter(Boolean).join('\u0000') : ''`
  - L237 `const execution = usePersonalWorkspaceExecution({ identityEpoch, identityScope: executionIdentityScope })`

Runtime不是重写一套协议：先复用现有带tenant的manifest/session/ACK绑定，仅补独立正式安装入口与并存回归。内层install.sh已有--target，不算“完全未支持”，但需联动核对不可变制品安装和unit生成。

对应测试：
- [install-entry-convergence.test.mjs](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/install-entry-convergence.test.mjs)：补双根、双身份、双state、双端口、错误session拒绝；模拟Provider。
- [runtime-host.test.mjs](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs)：补双根、双身份、双state、双端口、错误session拒绝；模拟Provider。
- [runtime-v1.test.mjs](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/runtime-v1.test.mjs)：补双根、双身份、双state、双端口、错误session拒绝；模拟Provider。
- [ack-checkpoint.test.mjs](/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/test/ack-checkpoint.test.mjs)：补双根、双身份、双state、双端口、错误session拒绝；模拟Provider。
- [chat-runtime.test.mjs](/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/test/chat-runtime.test.mjs)：补双根、双身份、双state、双端口、错误session拒绝；模拟Provider。
- [identity-scope.test.js](/home/isp/wsps/cyf/web/tests/identity-scope.test.js)：缺tenant不可请求、切换取消旧请求/恢复、缓存不跨环境；以远端固定版本为准。
- [personal-workspace-execution-component.test.js](/home/isp/wsps/cyf/web/tests/personal-workspace-execution-component.test.js)：缺tenant不可请求、切换取消旧请求/恢复、缓存不跨环境；以远端固定版本为准。
- [personal-workspace-execution.test.js](/home/isp/wsps/cyf/web/tests/personal-workspace-execution.test.js)：缺tenant不可请求、切换取消旧请求/恢复、缓存不跨环境；以远端固定版本为准。
- [formal-task-execution-scope.test.js](/home/isp/wsps/cyf/web/tests/formal-task-execution-scope.test.js)：缺tenant不可请求、切换取消旧请求/恢复、缓存不跨环境；以远端固定版本为准。

## 已改但未验证：不应继续说成“没改”的项

- 严格TenantClaimPolicy、EsSecurityContextFilter/TenantScopeResolver和13个HTTP/actor文件已改；缺canonical tenant不再默认0，相关测试未跑。
- BaseDao显式tenant查询的“OR0”已移除；未完成的是ID/批量/空scope等，不能混称整个BaseDao都没改。
- WaterMargin公共定义不再tenant0；persona scoped查询/私有overlay写入/提交后cache失效已改；SQL和事务测试未执行。
- 能力评估evaluate路径已改，未完成的是history/latest/stats/delete/compare，本报告逐方法区分。
- 取消/执行报告tenant测试已移入已有sourceSet；不是仍未接入，但未编译执行。
- identity/user/OAuth/point前期候选保留；未把未提交候选冒充develop或线上。

## 尚须核对的联动项：不伪装成已确认缺陷数

1. 通用DAO当前继承实现见下表。逐表区分全局身份、私有业务、公共定义；拦截器覆盖不是给每个DAO复制tenant代码。JDBC、工具调用和异步线程需另核对。
2. AgentCommandTransportSchemaInitializer / Hall schema initializer与资源源文件的所有生成/比对路径需联动；已确认14张活跃表限制，不把已退役controlled-image/provider-consent表加入活跃迁移。
3. ChatTypedInspectionContextService、TypedDeliberationFinalValidator、TypedInspectionFinalValidator：仍有旧tenant0协议，按当前调用可达性区分历史只读与待删除执行，不直接改为允许灰度以免复活旧能力。
4. ChatBountyAssetProjector、SMS队列、Task JobExecutor、材料/客服内部Tools、UserRole关联查询：公共隔离影响及后台可达性必须核对；不能因HTTP守卫存在声称内部调用安全。退役ChatBountyExecutionRelay不恢复。
5. Redis/Rabbit vhost/ES/文件根、短信/支付/WX/SSH外部资源：独立环境配置与启动保护需核对；未支持外部副作用继续禁止，不能把关闭功能宣称为全量支持。
6. persona维护SQL：generation_expression的MySQL规范化比对、旧/新形状、二次执行、部分失败恢复未验证；不是DDL已可用。
7. Runtime内层install、enrollment和宿主安装适配器与新unit/根参数联动；不得调用源码构建脚本在主机生产打包。
8. 默认test和专用sourceSet、方法过滤同步；现有nativeSkillResultRegression/skillManagementWire等选择器需复核，不把编入测试类当作执行用例。

## 受公共DAO影响的当前继承实现（不是逐文件缺陷列表）

- [point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointReferralDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointReferralDaoImpl.java#L12)
- [point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointSignDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointSignDaoImpl.java#L12)
- [point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointGiftUsageDaoImpl.java:16](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointGiftUsageDaoImpl.java#L16)
- [point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointGiftDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointGiftDaoImpl.java#L18)
- [point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointRecordDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/point/jia-point-mapper/src/main/java/cn/jia/point/dao/impl/PointRecordDaoImpl.java#L10)
- [base/jia-base-mapper/src/main/java/cn/jia/base/dao/impl/LogDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/base/jia-base-mapper/src/main/java/cn/jia/base/dao/impl/LogDaoImpl.java#L18)
- [base/jia-base-mapper/src/main/java/cn/jia/base/dao/impl/NoticeDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/base/jia-base-mapper/src/main/java/cn/jia/base/dao/impl/NoticeDaoImpl.java#L18)
- [base/jia-base-mapper/src/main/java/cn/jia/base/dao/impl/DictDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/base/jia-base-mapper/src/main/java/cn/jia/base/dao/impl/DictDaoImpl.java#L18)
- [kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMsgSubscribeDaoImpl.java:20](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMsgSubscribeDaoImpl.java#L20)
- [kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMsgLogDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMsgLogDaoImpl.java#L18)
- [kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuFaqDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuFaqDaoImpl.java#L18)
- [kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMessageDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMessageDaoImpl.java#L18)
- [kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMsgTypeDaoImpl.java:20](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/kefu/jia-kefu-mapper/src/main/java/cn/jia/kefu/dao/impl/KefuMsgTypeDaoImpl.java#L20)
- [oauth/jia-oauth-mapper/src/main/java/cn/jia/oauth/dao/impl/OauthApiKeyDaoImpl.java:15](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/oauth/jia-oauth-mapper/src/main/java/cn/jia/oauth/dao/impl/OauthApiKeyDaoImpl.java#L15)
- [oauth/jia-oauth-mapper/src/main/java/cn/jia/oauth/dao/impl/OauthClientDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/oauth/jia-oauth-mapper/src/main/java/cn/jia/oauth/dao/impl/OauthClientDaoImpl.java#L21)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentIdentityRegistryDaoImpl.java:13](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentIdentityRegistryDaoImpl.java#L13)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/DialogueTemplateDaoImpl.java:13](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/DialogueTemplateDaoImpl.java#L13)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AbilityEvaluationDaoImpl.java:13](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AbilityEvaluationDaoImpl.java#L13)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentTaskNoteDaoImpl.java:13](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentTaskNoteDaoImpl.java#L13)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentIdentityAliasDaoImpl.java:13](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentIdentityAliasDaoImpl.java#L13)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentRuntimeDaoImpl.java:15](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentRuntimeDaoImpl.java#L15)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentTaskEventDaoImpl.java:15](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentTaskEventDaoImpl.java#L15)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AbilityComparisonDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AbilityComparisonDaoImpl.java#L10)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentHostedProfileDaoImpl.java:11](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentHostedProfileDaoImpl.java#L11)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentRuntimeV1InstallationDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentRuntimeV1InstallationDaoImpl.java#L12)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentTaskMetaDaoImpl.java:23](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentTaskMetaDaoImpl.java#L23)
- [agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentPersonaBindingDaoImpl.java:15](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentPersonaBindingDaoImpl.java#L15)
- [chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/impl/ChatConversationDaoImpl.java:16](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/impl/ChatConversationDaoImpl.java#L16)
- [chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/impl/ChatMessageDaoImpl.java:20](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-mapper/src/main/java/cn/jia/chat/dao/impl/ChatMessageDaoImpl.java#L20)
- [dwz/jia-dwz-mapper/src/main/java/cn/jia/dwz/dao/impl/DwzRecordDaoImpl.java:19](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/dwz/jia-dwz-mapper/src/main/java/cn/jia/dwz/dao/impl/DwzRecordDaoImpl.java#L19)
- [task/jia-task-mapper/src/main/java/cn/jia/task/service/impl/TaskItemDaoImpl.java:19](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/task/jia-task-mapper/src/main/java/cn/jia/task/service/impl/TaskItemDaoImpl.java#L19)
- [task/jia-task-mapper/src/main/java/cn/jia/task/service/impl/TaskPlanDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/task/jia-task-mapper/src/main/java/cn/jia/task/service/impl/TaskPlanDaoImpl.java#L18)
- [task/jia-task-mapper/src/main/java/cn/jia/task/service/impl/TaskDetailDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/task/jia-task-mapper/src/main/java/cn/jia/task/service/impl/TaskDetailDaoImpl.java#L18)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDnsZoneDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDnsZoneDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspServerDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspServerDaoImpl.java#L10)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CmsTableDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CmsTableDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDnsRecordDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDnsRecordDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspFileDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspFileDaoImpl.java#L10)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CmsColumnDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CmsColumnDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDnsRecordHistoryDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDnsRecordHistoryDaoImpl.java#L10)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandAudiDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandAudiDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CmsConfigDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CmsConfigDaoImpl.java#L10)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandMfDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandMfDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspSmbVDirDaoImpl.java:10](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspSmbVDirDaoImpl.java#L10)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDomainDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/IspDomainDaoImpl.java#L12)
- [isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandVersionDaoImpl.java:12](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/isp/jia-isp-mapper/src/main/java/cn/jia/isp/dao/impl/CarBrandVersionDaoImpl.java#L12)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserMsgDaoImpl.java:19](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserMsgDaoImpl.java#L19)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserGroupDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserGroupDaoImpl.java#L21)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserPermsDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserPermsDaoImpl.java#L18)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserOrgRelDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserOrgRelDaoImpl.java#L21)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserGroupRelDaoImpl.java:22](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserGroupRelDaoImpl.java#L22)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserInfoDaoImpl.java:26](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserInfoDaoImpl.java#L26)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserRoleDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserRoleDaoImpl.java#L21)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserRoleRelDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserRoleRelDaoImpl.java#L21)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserOrgDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserOrgDaoImpl.java#L21)
- [user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserPermsRelDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/user/jia-user-mapper/src/main/java/cn/jia/user/dao/impl/UserPermsRelDaoImpl.java#L21)
- [wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/MpTemplateDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/MpTemplateDaoImpl.java#L18)
- [wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/MpInfoDaoImpl.java:20](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/MpInfoDaoImpl.java#L20)
- [wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/PayInfoDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/PayInfoDaoImpl.java#L18)
- [wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/PayOrderDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/PayOrderDaoImpl.java#L18)
- [wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/MpUserDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/wx/jia-wx-mapper/src/main/java/cn/jia/wx/dao/impl/MpUserDaoImpl.java#L21)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatNewsDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatNewsDaoImpl.java#L21)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteItemDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteItemDaoImpl.java#L21)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatMediaDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatMediaDaoImpl.java#L18)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatPhraseDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatPhraseDaoImpl.java#L18)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteTickDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteTickDaoImpl.java#L21)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatTipDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatTipDaoImpl.java#L18)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteQuestionDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteQuestionDaoImpl.java#L21)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatPhraseVoteDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatPhraseVoteDaoImpl.java#L18)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatPvLogDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatPvLogDaoImpl.java#L18)
- [material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/material/jia-material-mapper/src/main/java/cn/jia/mat/dao/impl/MatVoteDaoImpl.java#L18)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsMessageDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsMessageDaoImpl.java#L18)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsBuyDaoImpl.java:21](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsBuyDaoImpl.java#L21)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsSendDaoImpl.java:22](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsSendDaoImpl.java#L22)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsReplyDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsReplyDaoImpl.java#L18)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsPackageDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsPackageDaoImpl.java#L18)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsConfigDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsConfigDaoImpl.java#L18)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsTemplateDaoImpl.java:18](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsTemplateDaoImpl.java#L18)
- [sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsCodeDaoImpl.java:20](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/sms/jia-sms-mapper/src/main/java/cn/jia/sms/dao/impl/SmsCodeDaoImpl.java#L20)

## 测试与交付状态

- 本文列出的49个API测试文件为具体修复入口，另有Runtime/Web测试；所有正式应用编译/回归均NOT_RUN，不是仅差线上验收。
- 既有完整测试依赖索引 `/home/isp/state/cyf-full-tenant-gray-20261029/analysis-20261030/api-test-matrix.json` 的481条是历史依赖范围，不是剩余失败数；需结合本次已移位测试及当前build.gradle，不沿用过期路径报数。
- 后续统一编译、真实SQL、回归、validateLayering走已授权Flow worker固定候选，600秒总上限；测试/打包/上传结束即停止，不SSH生产或等待主机。当前没有启动Run。
- 未合并、未发布、未执行数据库维护；旧缺tenant凭据在新严格方案下需重新认证，不能承诺生产无感。

## 可机读证据

`/home/isp/state/cyf-full-tenant-gray-20261029/analysis-20261030/code-remainder-1702.json`

## 测试代码中的具体剩余点（非仅测试名称）

| 文件位置 | 现在的代码 | 修改方案 |
|---|---|---|
| [SkillAgentVersionsTest:29–30](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillAgentVersionsTest.java#L29) | lockVersion / advanceVersion期望第一参数为`owner`，跟随了业务代码的错误tenant语义 | fixture显式区分tenant、client、owner；verify真实tenant参数；同owner双环境独立CAS。 |
| [SkillInstallRecoveryServiceTest:25–43](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillInstallRecoveryServiceTest.java#L25) | delivery/outbox/wire/lock固定生产0场景 | 保留0正例并参数化合法环境；增加外租户候选排在LIMIT之前及不得claim的真实SQL回归。 |
| [MemoryRepositoryIsolationTest](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/memory/MemoryRepositoryIsolationTest.java) | 当前隔离主要按owner；没有完整tenant/client接口 | 随MemoryRepository签名改fixture；补topK前tenant/client过滤、同owner跨域拒绝、delete/count不跨域。 |
| [ArchiveQuestionControllerTest:130](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/src/test/java/cn/jia/chat/archive/http/ArchiveQuestionControllerTest.java#L130) | 该“valid”JWT fixture只给jiacn/client_id | 正例显式canonical tenant；另保留缺tenant负例；捕获实际传入ArchiveOwnerScope，断言未改写为0。 |
| [chat build.gradle:466](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/build.gradle#L466) | nativeSkillResultRegression仅选一个方法 | 新tenant方法必须被实际selector选中，而非只编译类。 |
| [chat build.gradle:497–506](/home/isp/wsps/worktrees/full-tenant-gray-api-20261029/chat/jia-chat-service/build.gradle#L497) | skillManagementWire按具体方法白名单执行 | 同步包含新增隔离方法；保留原幂等、身份、fence、回滚用例；不因本次无关死锁议题额外扩展修复范围。 |

这些是已看到的测试修复点；并非宣称其他49个入口均已逐断言核查，也不把历史481个依赖文件全算作待改测试。
