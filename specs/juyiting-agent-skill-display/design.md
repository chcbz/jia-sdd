> 历史D1：已由 `design-d2.md`、`plan-d2.md`、`acceptance-d2.md` 替代，不再作为当前开发计划。

# 点将册技能、本领展示详设 D1

日期：2026-10-16。范围和权限以 `spec.md` 为准。本文区分**已核实事实**与**待开发的目标实现**；下述接口尚不存在，不得报告为已上线。

## 1. 已核实的源码基线

完整 commit/tree、远端查询时间与规范摘要见 `evidence/source-baseline.json`（14:15:56 +08:00 开始查询）。

| 仓库 | 本地 HEAD | 实查远端 develop | 结论 |
|---|---|---|---|
| 根仓库 | e05498ed8f8d67d791ad8d269ae5bbc00b3592e6 | 同左 | 根工作区存在43项已跟踪修改，全部保留 |
| API | fc399976710f5b724916013926be2cbff899af8c | 同左 | 已跟踪工作区干净 |
| Web | 2c8d6703eead623f555029341101cb688b9d448a | 421f628c245b83466cafb70510ff69188180bdee | 本地领先一条“不预填议事草稿”提交，不能回退 |
| Runtime | 6a9d8d3c1219450c19b3edfbef317e615940ab5d | 同左 | 位于 `/home/isp/wsps/chcbz/isp-install`，本期只读 |

源码核对与历史在线证据分开：`/home/isp/wsps/cyf/specs/juyiting-skill-execution/integration.yaml` 记录 Web1.16.1/421f628、API1.16.5/6116a10、Runtime1.2.7/6a9d8d3 的历史发布。本次没有执行生产数据库/API查询，因此不把该记录冒充2026-10-16当前在线观测。本功能不依赖给某个实名 Agent 预填技能。

### 1.1 本领并不是已安装技能

已核对路径：

- Web `/home/isp/wsps/cyf/web/src/components/juyiting/AgentPanel.vue`：当前详情逐项展示 `selectedAgent.abilities`；无技能目录读取。
- Web `/home/isp/wsps/cyf/web/src/composables/juyiting/useHallData.js`：名册使用 `agentApi.search('/roster', {pageNum:1,pageSize:100})`，从 `result.items` 读取；`reconcileSelectedAgent()` 用新名册替换选中对象。
- API `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java`：注册/状态更新保存 abilities；DTO 优先取 runtime 字段，空白才回退 persona；JSON `[]` 不是空白，不触发角色补齐。
- Runtime `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs`：`resolveProfileAbilities = profile => discoverWorkspaceAbilities(profile)`；注册和 presence 均调用它。
- 此版本 `profile.abilities` 会产生 `LEGACY_ABILITIES_IGNORED` 提示；存在 `discoverCodexSkills` 不意味着它参与本领投影。不能按旧文档修改 profile 的 abilities 或 SKILL.md 来刷新本领。
- 数据表：`agent_runtime.abilities` 与 `agent_persona.abilities`；不与技能权益/安装表合并。

扫描按工作区模块映射，截图16个标签恰好对应 CYF 模块：agent→智能体管理/调度，chat→会话消息/多智能体协作，task→任务协作，oauth→身份认证，user→用户体系，kefu→客服系统，point→积分体系，wx→微信生态，sms→短信服务，isp→域名与主机管理，material→内容管理，workflow→工作流编排，dwz→短链接服务；agent+chat+task再加入聚义厅协作。

`evidence/ability-source-diagnostic.json` 保存固定源码中扫描函数对 `/home/isp/wsps/cyf` 的隔离诊断，输出与截图16个标签一致。它不是吴用线上 profile 证明。完整 Runtime 模块导入因本地缺少 ajv 失败，未安装依赖；诊断只执行原扫描函数片段和 Node 内置文件 API，不是正式 Runtime 测试。

**结论：这批标签不应人工“换一批更像技能的标签”。本期刷新服务端最近记录；工作区没变化，本领不变是正确行为。** `docs/codex-ws-agent.md` 中“基础能力/profile/SKILL.md合并”的旧说明与当前源码不符，开发收口时仅定点更正文档，不据旧说明改实现。

### 1.2 现有技能链路的可复用与不可复用部分

| 对象 | 已核实行为 | 本期决定 |
|---|---|---|
| `GET /agent/{agentId}/skill-entitlements` | 只有权益、没有运行目录；经 SkillAgentVersions.requireOwned，可能维护持久版本；受市场开关控制 | 不作为纯展示聚合接口，不从前端拼权益为已安装 |
| `GET /agent/tasks/{taskId}/skill-capabilities` | 检查已指派与当前 grant；无任务授权不列举技能 | 保持不变，不传假 taskId，不提前创建 grant |
| `InstalledSkillDescriptorService.read` | 联查权益、订单、批准版本、安装、成功回执、交付绑定、不可变包摘要；返回 descriptor.verified | 原样复用 |
| `ChatActionCapabilityService.inspectInstalledSkills` | 匹配 live session、安装/host、版本/摘要、runner、READY、toolchain/binding；末尾复查 Runtime | 复用并补纯离线观察分支，不改任务准入 |
| `AgentService.requireApiKeyOwnedAgent` | 非 ForUpdate 分支只读验证身份/绑定，返回 runtime DTO；不要求在线 | 用于拥有者只读边界；禁止使用 ForUpdate 版本 |
| `AgentRuntimeAuthenticationService.currentRegisteredProof` | 返回唯一当前认证 proof；没有或歧义均抛 IllegalArgumentException | 缺 proof 只能标“运行状态待核验”，不得武断标为离线 |

注意历史已验收的是吴用 `image-edit@1.0.0`（图片修改），不能把它显示为“图片生成”。名称来自技能 manifest.title，缺少可信标题时回退 skillKey。

## 2. 固定产品决策

### 2.1 点将册布局

详情头像/姓名之后依次展示：

1. **技能**：`已核验安装 N 项`；逐项名称、版本、安装状态、运行状态、原因。
2. **本领**：保留原标签样式；辅助说明“Agent 本领记录，不等同于已安装技能”。
3. **刷新技能与本领**按钮、最近读取时间；lastSeenAt 显示为“最近联络”，不是技能核验时间。
4. 原“与这位好汉密议”“点将并议事”及其权限/顺序不变。

技能区固定说明：“运行就绪不代表当前任务已获执行授权”。不用“本任务可调用”称呼本界面。

选中自己的非系统 Agent：自动加载新接口。非拥有者/系统 Agent：保留原可见本领，技能区显示“仅拥有者可查看技能”；不请求私有目录，不借任务授权越权展示。

不新增购买/安装按钮，不改变技能市场入口。本期只改点将册详情及其当前行的本领摘要；地图、派单候选和 SelectedAgentCard 不改。

### 2.2 刷新语义

- 自动触发：点将册可见时首次选中、选中 ID 改变、身份代际改变、关闭后重新打开。
- 手动触发：详情“刷新技能与本领”。仅对当前选中 Agent 请求一次聚合 GET。
- 不新增周期轮询；不向 Runtime 发刷新命令，不等待新心跳、不重连、不重启。
- 请求重新读取现有 DTO 和安装/Runtime事实。服务器返回的本领在当前详情立即覆盖旧标签，包括合法空数组。
- 不修改 `allRosterAgents`、派单计算或数据库。列表当前行用同一成功回执的本领作**展示覆盖**；其他行保持名册原投影，点开后各自读取。
- 新一次刷新开始后撤下旧“就绪”断言，显示加载；本领旧值仅作为“上次记录”展示。失败不得保留成功绿色状态。
- 如果业务希望强制所有 Agent 重新扫描/人工修改本领，属于另一项需求；本次不假装做了这种操作。

## 3. 新 HTTP 契约（唯一新增路由）

### 3.1 请求与权限

`GET /agent/{agentId}/profile-capabilities`

- 无 query、无 body；出现未知 query、body 或 Transfer-Encoding 拒绝400；`agentId` 非空、首尾无空白、无控制字符、最多100 code points，保留不透明字符串。
- 登录用户 JWT；`tenant/client/owner` 不允许请求传入。
- 使用 `HostingRentHttp.actor(authentication)` 取得声明，`TenantScopeResolver` 与 `EsContextHolder` 交叉核对 tenant/client/jiacn，固定部署 tenant=`0`。
- 使用 `HostingRentOwnerResolver.requireOwner(actor)` 验证真实登录 subject→用户→jiacn；然后 `AgentService.requireApiKeyOwnedAgent(clientId, owner, agentId)` 读验证。
- `agentId` 必须是返回的 canonical ID；不接受别名跨主体解析，不给系统宋江目录，不因管理员角色绕过 owner。
- 不依赖市场启用开关，不调用 `SkillMarketplaceService.entitlements`、`SkillAgentVersions.requireOwned` 或 `requireHostingNewWork`；停止销售/托管不准新任务不应抹去已拥有者的只读事实。
- 响应前再做一次 owner/绑定只读核验；任一次失败都不返回此前的技能片段。
- HTTP header：`Cache-Control: private, no-store`、`X-Content-Type-Options: nosniff`；requestId遵循公共规范。

### 3.2 完整成功示例

以下全为测试示例，不代表吴用当前线上状态：

```json
{
  "protocolVersion": 1,
  "requestId": "req_profile_demo",
  "code": "E0",
  "msg": "ok",
  "data": {
    "agentId": "agent_demo",
    "observedAt": 1792137600000,
    "abilities": ["内容管理", "工作流编排"],
    "lastSeenAt": 1792137590000,
    "skills": {
      "status": "AVAILABLE",
      "catalogRevision": "1",
      "reasonCode": null,
      "items": [{
        "skillKey": "image-edit",
        "skillVersion": "1.0.0",
        "title": "图片修改",
        "installationVerified": true,
        "runtimeState": "RUNTIME_READY",
        "reasonCode": null
      }]
    }
  }
}
```

所有示例字段必填、DTO封闭，不新增其它字段。规范固定 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2；复用 JsonResult 与已有公共信封边界，不自建包装。

| 字段 | 类型和约束 |
|---|---|
| agentId | 与请求完全相同的canonical字符串 |
| observedAt | 本次读取完成时间；非负安全整数 epoch ms，不是原子数据库/Runtime快照承诺 |
| abilities | string[]；沿用服务端已规范化本领顺序；空必须返回[]，不拼技能名、不根据角色补造 |
| lastSeenAt | 非负安全整数 epoch ms或null；来自Agent DTO |
| skills.status | AVAILABLE（安装目录成功读取，包括空目录）或UNAVAILABLE（安装事实源失败） |
| skills.catalogRevision | 原runtime目录revision的规范非负十进制字符串（`0|[1-9][0-9]*`）或null；不转Number，不接受前导零/浮点/其它字符 |
| skills.reasonCode | AVAILABLE时null；UNAVAILABLE时固定SKILL_DESCRIPTOR_SOURCE_UNAVAILABLE |
| skills.items | SkillItem[]；UNAVAILABLE时只能[]；按skillKey、skillVersion稳定字典序 |
| skillKey / skillVersion | 非空字符串；与权威descriptor一致，版本不转数字 |
| title | 非空显示文字；可信且非空manifest.title，否则skillKey；不渲染HTML |
| installationVerified | boolean；只有descriptor.verified且版本唯一时true |
| runtimeState | RUNTIME_READY或UNAVAILABLE；只有安装已核验且已有核验链全部满足时READY |
| item.reasonCode | READY时必须null；UNAVAILABLE时为`[A-Z][A-Z0-9_]{0,63}`机器码 |

后端在响应序列化前检查长整型时间安全范围；非法内部事实返回503，不截断。前端做闭包/类型/状态组合校验；非法数据整份拒绝，不能把部分READY留下。skillVersion按字符串展示，不自行宣布“最新版本”。

### 3.3 空、部分失败与HTTP失败

- 拥有者存在、无权益记录：200/E0，skills AVAILABLE/items[] →“暂无已登记技能”；不声称 Agent 没有内置问答能力。
- 安装事实完整、Runtime无法唯一确认：200/E0，已核验安装仍true，runtimeState UNAVAILABLE，reason=`SKILL_RUNTIME_UNAVAILABLE` →“运行状态待核验”。
- 已有权益但安装证据失败：保留记录，installationVerified=false，不计入安装数量，文案“安装未核验”。不直接提示重复购买。
- `SKILL_NOT_EXECUTABLE`：显示“非可执行技能包”，不声称未购买。
- 安装目录读取抛 `InstalledSkillDescriptorLookup.SourceUnavailable`：本领仍可返回200/E0；skills UNAVAILABLE/items[]，显示“技能读取失败，可重试”，绝不显示空目录文案。
- Runtime读取发生未分类基础设施异常、revision不符合公共规范：503，不吞成离线；只有明确的无proof异常可走待核验分支。

| HTTP | code | 条件 |
|---|---|---|
| 400 | BAD_REQUEST | path/query/body不合法 |
| 401 | UNAUTHENTICATED | 缺少有效用户认证 |
| 404 | AGENT_PROFILE_NOT_FOUND | owner/租户/client/绑定不匹配、agent不存在、系统agent；统一隐藏存在性 |
| 503 | AGENT_PROFILE_UNAVAILABLE | Agent记录/认证依赖异常、数据完整性异常、无法安全完成读取 |

失败使用统一信封，data=null，安全msg；不返回堆栈、内部路径或配置。不要把SQL/包损坏等故障一律翻译成404。

## 4. API 逐文件实现

根路径 `/home/isp/wsps/cyf/api`，不新增依赖、不新增表。

### 4.1 新 Controller

新增 `chat/jia-chat-service/src/main/java/cn/jia/chat/api/AgentProfileCapabilitiesController.java`。

- 只注册上述GET；参数封闭校验与JsonResult输出模式参照同目录 `TaskSkillCapabilityController.java`。
- 严格认证、tenant/context一致性和owner解析按3.1执行；传递已验证Actor给服务，不把Authentication丢给展示逻辑猜测。
- 捕获明确业务失败映射3.3；未知异常503，日志只带requestId、失败分类，不记录JWT/manifest全文。
- 不依赖taskId，不调用taskCatalog。

### 4.2 新只读聚合服务

新增 `chat/jia-chat-service/src/main/java/cn/jia/chat/service/AgentProfileCapabilitiesService.java`。

依赖：AgentService、HostingRentOwnerResolver、AgentRuntimeAuthenticationService、ChatActionCapabilityService。生产构造器使用Clock.systemUTC()；另设包内测试构造器接收Clock，不假定容器已有Clock Bean。DTO定义为该服务的不可变record：ProfileCapabilities、SkillDirectory、SkillItem，字段严格按3.2。

固定流程：

```text
owner = owners.requireOwner(actor)
agent = agents.requireApiKeyOwnedAgent(actor.clientId, owner, agentId)
assert canonical id / non-system / actor tenant 已通过入口验证
scope = ChatActionCapabilityService.Scope(tenant, owner, client, agentId)
try currentRegisteredProof(tenant, client, agentId)
    若成功：逐项相等校验 proof.scope 的tenant/client/owner/agent
            由proof构造SessionFence(installationId, hostId, runtimeInstanceId, sessionGeneration)
            catalog = capabilities.inspectInstalledSkills(scope, fence)
    仅currentRegisteredProof调用自身抛出的无proof/歧义IllegalArgumentException（catch不得包住后续scope/fence/目录校验）：
            catalog = capabilities.inspectInstalledSkillsWithoutRuntime(scope)
    其它异常：失败503
若descriptor源不可用：skills = UNAVAILABLE，但仍返回本领
将内部catalog白名单映射为SkillDirectory，不返回metadataJson
owner与binding再核验；如果换绑或注销则整体404
返回首次读取的agent.abilities/lastSeenAt + 当前目录 + clock.millis()
```

无长事务、不持有ForUpdate锁、不写version、无外部Provider请求。包读取复用已验证不可变字节路径；不新增任意URL下载或信任模型提供的路径。

### 4.3 最小扩展已有安装观察器

修改 `chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatActionCapabilityService.java`：

1. 内部 `SkillCandidate` record增加 `boolean installationVerified`。这是内部record，不向既有任务HTTP自动序列化该字段；TaskCatalog仍用原白名单构造。
2. 保留现有 `inspectInstalledSkills(Scope, SessionFence)` 的非null fence验证和全部匹配/复查逻辑。
3. 新增 `inspectInstalledSkillsWithoutRuntime(Scope)`，只读同一descriptor；不伪造fence、不调用runtime.lookup。共用private投影函数，禁止另写一份证据匹配算法。
4. `installationVerified = descriptor.verified()` 且同key/version唯一；不可用原因不能从任意Runtime reason字符串倒推出安装真假。
5. 正常分支state与reason保持原判定；无Runtime分支，对有效descriptor附 `SKILL_RUNTIME_UNAVAILABLE`，catalogRevision=null。
6. 重复key/version合并为一个UNAVAILABLE项，installationVerified=false，reason=`SKILL_INSTALLATION_AMBIGUOUS`，title=skillKey；内部manifest metadata=null。此数据本就不应可执行；相关任务目录不放宽行为。
7. Runtime前后读取不一致仍按现有逻辑降为 `SKILL_RUNTIME_CHANGED`，安装核验布尔值保持；不沿用旧READY。
8. 更新现有全部SkillCandidate构造点，包括taskCatalog无fence分支；任务端wire字段、CALLABLE判定、权限及费用规则不变。

不拆新的通用能力平台，不把agent模块反向依赖chat。chat当前build.gradle已依赖agent-service/API，新增类放chat无需改依赖方向。

## 5. 前端逐文件实现

根路径 `/home/isp/wsps/cyf/web`。不改路由、市场页面或全局HTTP协议。

### 5.1 纯投影

新增 `src/composables/juyiting/hallAgentProfileCapabilities.js`：

- 导出 `agentProfileCapabilitiesProjection(raw, expectedAgentId)`：按3.2做精确字段/类型校验；不合法返回null，完整合法则返回只读对象。
- 验证agentId完全相同、数组不重复key/version、READY⇒installationVerified=true且reasonCode=null、UNAVAILABLE⇒reason非空、目录失败不得带items/revision。
- observedAt/lastSeenAt使用Number.isSafeInteger；revision按非负十进制字符串校验且不转数字；技能版本仅验证非空字符串。
- 导出显示函数：安装标签、运行标签、原因文本；所有未知合法reason统一“暂不可用”，可显示机器码供排查，不显示内部详情。
- 已核验安装数量由installationVerified计数，不能使用items.length或Runtime READY数量代替。

### 5.2 异步状态

新增 `src/composables/juyiting/useHallAgentProfileCapabilities.js`：

参数 `{api, getAgent, identityKey, enabled}`。返回 `{projection, loading, error, refresh, reset, dispose}`。参照现有useHallSkillCapabilities，但不要复用任务目录的taskId依赖。

- fingerprint=`[identityKey(), enabled(), agent.agentId, agent.boundToMe, agent.systemAgent]`，不依赖整个Agent对象，避免名册替换对象导致请求风暴。
- enabled只在点将册可见、身份有效、Agent非系统且boundToMe=true时成立；boundToMe只是UI提示，后端仍权威核验。
- GET使用 `agentApi.get('/'+encodeURIComponent(agentId)+'/profile-capabilities', {}, {autoLoading:false,needAuth:true,signal})`；agentApi已有`/agent`前缀，不重复拼前缀。
- 每次开始递增epoch、abort前一个请求、清projection与error；对比发起时指纹和epoch，只有最新且未disposed结果可写入。
- watch使用flush:'sync'；关闭点将册、切换Agent/身份时立即清空，旧成功/失败/finally都不得污染新状态。
- refresh在loading期间按钮disabled；接口仍可被程序触发，epoch负责latest-wins。
- 无定时器、无localStorage、无跨用户缓存；abort只取消自己的HTTP，不取消Agent工作。

### 5.3 组件接线

修改 `src/components/world/JuyiHall.vue`：

- 创建上面composable，identityKey使用已有hallIdentityScope与apiStore.authorizationGeneration；enabled使用renderedPanel==='agents'。
- 传入AgentPanel：`profileCapabilities`、`profileCapabilitiesLoading`、`profileCapabilitiesError`；监听`refresh-profile-capabilities`。
- 在卸载时dispose；不要修改loadAgents、派单推荐或现有taskSkillDirectory。

修改 `src/components/juyiting/AgentPanel.vue`：

- 新增3个props及事件，默认值保持既有使用者可挂载；沿用当前模板，不增加子组件以免现有SFC测试加载器需要额外模块解析。
- section明确`aria-label="技能"`与`aria-label="本领"`；heading使用同名文案。
- 本领展示优先使用匹配当前agentId的成功profileCapabilities.abilities（包括[]），否则使用selectedAgent.abilities并标注“上次记录”；GET失败时不能写“已刷新”。
- 列表仅当前Agent行的abilityText输入可用 `{...agent, abilities: freshAbilities}` 做显示覆盖，仍保留currentTaskTitle优先；不写回传入agent或名册数组。
- 技能空/失败/无权文案按6节；长标题/版本/原因允许换行，保留点将和密议按钮。
- 小屏卡片不可横向溢出；状态不仅靠颜色，提供文字；loading/error用role=status，button可键盘操作。

不修改 `useHallData.js`：新的单Agent详情读取不需要全名册重取、地图重取或目录N+1。

## 6. 状态与文案映射

| 条件 | 技能安装显示 | 运行显示/说明 |
|---|---|---|
| 正在读取 | — | 正在核对技能… |
| 目录AVAILABLE，items=[] | — | 暂无已登记技能 |
| 目录UNAVAILABLE | — | 技能读取失败，可重试 |
| installationVerified=true，RUNTIME_READY | 已核验安装 | 运行就绪 |
| installationVerified=true，UNAVAILABLE | 已核验安装 | 根据reason，默认暂不可用 |
| installationVerified=false | 安装未核验 | 具体reason，不显示绿色就绪 |
| 非拥有者/系统Agent | — | 仅拥有者可查看技能 |
| 整体404 | — | 当前Agent不可访问，请刷新点将册 |
| 整体401 | — | 请重新登录后查看 |
| 网络/503/非法响应 | — | 技能与本领读取失败，请重试 |

原因文案白名单：

- SKILL_RUNTIME_UNAVAILABLE → 运行状态待核验。
- SKILL_RUNTIME_DISCONNECTED → Runtime已断开（仅目录明确给出DISCONNECTED时）。
- SKILL_RUNTIME_NOT_DECLARED → 当前Runtime尚未报告此技能。
- SKILL_RUNTIME_INVALID_DECLARATION / SKILL_RUNTIME_EVIDENCE_INVALID → 运行能力声明未通过核验。
- SKILL_RUNTIME_BINDING_MISMATCH → 技能与当前运行实例不匹配。
- SKILL_RUNTIME_CHANGED / SKILL_RUNTIME_FENCED / SKILL_RUNTIME_AMBIGUOUS → 运行会话变化或不唯一，请刷新。
- SKILL_NOT_EXECUTABLE → 非可执行技能包。
- SKILL_NOT_INSTALLED → 无有效安装权益。
- SKILL_INSTALLATION_EVIDENCE_INVALID / RECEIPT_MISSING / BINDING_INVALID（均带SKILL_INSTALLATION_前缀）→ 安装证据未通过核验。
- SKILL_INSTALLATION_CHANGED / SKILL_INSTALLATION_AMBIGUOUS → 安装记录变化或不唯一，请刷新。
- 其它合法原因 → 暂不可用；追加原机器码，不猜解释。

本领空数组统一“未录本领”，不显示“没有能力”；失联时显示最近记录，不声称实时扫描成功。

## 7. 数据、并发、安全与部署

- 无DDL、无数据库回填；不会清空现有abilities，不会改订单/权益/安装状态。
- GET不会启动安装、技能测量、Provider调用、托管扣费或任务执行，不要求“空闲”才能看详情。
- 用户仅能读取自己拥有的Agent；task grant不是读取其他人完整技能目录的替代权限。
- 不输出manifestJson/metadataJson、包路径、entrypoint、host/installation/session标识、凭证、工具链路径、原生模型参数schema。
- 安装核验与运行观察不是执行准入。实际执行继续使用原TaskSkillPolicyService与原执行链，不信任前端发回的READY。
- 不新增缓存、超时或性能拒绝门槛。后续性能问题用实际观测处理，不以展示预算取消业务请求。
- API先发布、Web后发布，按明确版本固定commit/tree、测试、同批制品、在线核验；本次详设不触发发布。
- develop合入/push不部署；前端Flow4403172，后端固定源码本地经orchestrator。源码未完成时不填写测试PASS或线上成功。
- 接口新增，不保留新旧双解析；既有任务接口不变。不需要Runtime新版本。

## 8. 验证与开发启动条件

具体测试见 `acceptance.md`，切片见 `tasks.md`。没有需要开发者再选择的接口/字段/状态/刷新方案。

已核实但不冒充的边界：生产当前每位Agent的技能和工作区不在本次只读源码核对范围；设计不以这些动态值为前提。上线验收必须读取真实当前值，不把历史“吴用已安装image-edit”或截图中的“林冲未录本领”硬编码进断言。

下一步是按固定基线创建本任务隔离开发工作区、登记ledger并实施；不是再次研究“到底复用哪个接口”。基线若变化只检查本文命中路径的差异并记录，不回退其他聊天提交。
