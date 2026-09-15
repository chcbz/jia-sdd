# 设计：租户与个人所有者分离

## 1. 作用域模型

服务端从认证上下文派生三元组，客户端不得传入并覆盖：

```text
tenantId   = "0"
clientId   = JWT client_id
ownerJiacn = JWT jiacn
```

| 域 | 租户键 | 个人/授权键 | 唯一性与访问规则 |
|---|---|---|---|
| 用户资料 | `tenant_id='0'` | 用户表自身 `jiacn`/用户主键 | 所有个人资料读写必须带认证 owner；`tenant_id` 不能代替 owner。 |
| Agent persona binding / identity / runtime / hosting | `tenant_id='0'` | `owner_jiacn` | 活跃角色 `(tenant_id, client_id, active_persona_code)` 唯一；托管、注册、解绑仍须匹配 owner。 |
| Archive progress/bookmark/note/question/idempotency | `tenant_id='0'` | `owner_jiacn` | 所有读取/写入精确匹配 `(tenant_id, client_id, owner_jiacn)`。 |
| Chat conversation/message | `tenant_id='0'` | `jiacn` | 读取、写入、删除精确匹配 `(tenant_id, client_id, jiacn, conversation_id)`。 |
| Agent task root and children | `tenant_id='0'` | `owner_jiacn` | 用户发起的任务精确匹配 `(tenant_id, client_id, owner_jiacn, task_id)`。角色可以被选作执行者，但不能替代 task owner 过滤。 |
| 公共 persona/典籍元数据 | `tenant_id='0'` | 无 | 公开数据不带用户所有者。 |

## 2. Agent 角色

### 2.1 目录

角色目录在 `(0, client_id)` 读取全部活跃绑定投影：

- 无绑定：`bound=false, canBind=true`。
- 当前用户拥有：`bound=true, boundToMe=true, canOperate=true, canBind=false`。
- 其他用户拥有：`bound=true, boundToMe=false, canOperate=false, canBind=false`。

非 owner 投影不得返回 owner、binding id、agent id、identity、runtime、endpoint 或任务信息。再次申领已由他人持有的角色返回 `PERSONA_BOUND`（HTTP 409）；数据库唯一键是并发裁决的最终边界。

### 2.2 身份与托管

`agent_identity_registry`、`agent_identity_alias` 的非系统行要求：

```text
tenant_id = '0'
client_id is nonblank
owner_jiacn is nonblank
```

不再要求 `tenant_id = owner_jiacn`。身份、runtime、hosting profile 的读取仍使用完整 `(0, client_id, owner_jiacn, binding/agent)`，因此角色控制权不转移给其他用户。

## 3. 任务隔离与指定重复角色处理

任务 owner 与 Agent owner 是两个不同概念：

- `owner_jiacn` 表示发起、读取和修改该任务的用户；根表和每个可读/可写子表都必须保存它。
- `assigned_agent_id`、成员、工作项等表示执行者；迁移执行 Agent 不改变任务 owner。
- 用户入口先以 `(0, client, owner, task)` 锁定/读取 root，再访问成员、工作项、事件、请求、成果、资金、报价、结算、线程和附件。任务 ID 不能成为授权能力。
- Agent 身份只能验证“该 Agent 是否可执行已授权任务”，不能代替用户 owner 过滤。

指定重复角色的迁移只做以下动作：保留受控输入指定 owner 的 binding；另一 binding/identity/runtime/hosting 退役；恰好两个实时任务的当前执行 Agent 引用改为保留 canonical Agent；历史 task event 保留原样，并按每个任务追加一条 `AGENT_ASSIGNMENT_MIGRATED` 审计事件。任务归属和任意其他用户数据都不迁移。

任务表根/子表索引从仅 tenant/client/task 扩展为 tenant/client/owner/task；所有二级 task 查询也必须携带 owner。需要覆盖的业务表由生产盘点和代码引用共同确定，至少包括 task meta、member、work item、event、request、artifact、note、artifact outcome/decision、funding/operation、quote/claim/settlement 及 work-item reassignment。

## 4. 聊天、典籍与用户资料

- Archive controller 构造 `(0, clientId, claim.jiacn)`；存储层保留三元精确谓词。
- Chat conversation 与 message 均写入 tenant `0`；`jiacn + client_id` 继续参与精确筛选、消息一致性和删除围栏。
- 用户资料的 existing owner 谓词必须保留；不能为 `tenant_id='0'` 增加跨用户宽松查询。
- 不提供旧 `tenant_id=owner_jiacn` 行的应用兼容读取。维护窗口内先完成受控迁移或删除，再部署严格版本；严格版本只读取和写入 `tenant_id='0'`，且保留 owner 谓词。

## 5. 数据迁移顺序

### Phase A — 维护窗口与加法 DDL

1. 进入维护窗口并阻断会产生业务写入的入口；不得依赖应用层旧格式兼容。
2. 以生产盘点生成完整 tenant 表清单、行数、主键哈希、外键/父子关系和 owner 来源。每一行只能被分类为“可迁移”或“不可迁移后删除”。
3. 所有任务根/子表加 `owner_jiacn`，新严格代码的写入从认证 owner 或已锁定 root 复制。可迁移历史行仅可从 `task_plan.jiacn`、已锁定任务根或现有明确 owner 字段回填；来源不一致、缺失或孤儿记录列入删除集。
4. 建立携带 owner 的查询索引，并准备 `(tenant_id, client_id, active_persona_code)` 唯一键；旧重复 persona 在 tenant 改为 `0` 前先按本设计处理。
5. identity/alias 约束与严格版本同步收紧为 `tenant_id='0'`；不存在“旧 owner-tenant 或新 0”的兼容期。

### Phase B — 受控生产迁移/删除

每次执行使用受控变量 `CLIENT_ID`、`KEEP_OWNER`、`PERSONA_CODE`，不得把个人标识写入代码库或日志。

1. 只读快照：`information_schema` 的完整 tenant 表清单、每表范围行数与主键哈希、重复 persona 组、两个任务根及当前执行 Agent 引用哈希；同时生成不可迁移记录的精确主键删除清单。
2. 锁定指定保留 binding 与另一条 active duplicate；断言一个冲突组、一个保留 binding、一个退役 binding、恰好两个待迁移实时任务，且 identity/runtime/hosting 投影完整。
3. 仅把这两个任务的实时执行引用迁至保留 canonical Agent，追加迁移事件；不修改原 event，不修改 `owner_jiacn`。
4. 退役非保留 binding、identity、runtime 与 hosted profile；不物理删除。
5. 对每个可迁移行，按父子依赖顺序写入 owner 并将 tenant 更新为 `0`；每条更新使用快照主键范围、旧值和预期影响行数。
6. 对无法确定 owner、owner 来源冲突或父子关系无法验证的记录，按已生成的精确主键清单从叶子到根删除；不得使用无条件全表删除，且删除数必须等于快照删除集。
7. 提交后读回：所有业务表无非 `0` tenant；不存在活跃重复 persona；两任务都指向保留 Agent；资料/Archive/Chat/Task 的 owner 精确读取成功，交叉 owner 不泄露存在性；迁移/删除行数与快照完全一致。

DDL 自动提交，DML 事务不跨 DDL。生产 DML 与删除 SQL 在盘点完成后临时生成，连同私有快照、逆向 SQL（仅适用于迁移记录）和 post-hash 一起保存在受控运行环境，不进 Git。

### Phase C — 严格版本

Phase B 读回成功后部署严格版本：所有业务读写固定 `tenant_id='0'`；读取、更新和删除继续带 owner 谓词。任何残余非 `0` tenant 或未分类记录均阻止版本切换。
## 6. 回滚

- Phase A：退出维护窗口前回滚 DDL 以外的未提交变更；新增 owner/索引可保留。
- Phase B：未提交即回滚事务；已提交的可迁移记录仅按私有快照、主键与 post-hash 执行一次受控逆向恢复，不根据猜测恢复重复 binding。经本次授权删除的不可迁移记录不承诺自动恢复。
- Phase C：只在 Phase B 结果和线上 smoke 都成功后执行；否则不进入。
