# 点将册技能、本领与响应式布局详设

日期：2026-10-17。任务JYT-AGENT-SKILL-DISPLAY-20261016，唯一Owner为本聊天Owner。本文为当前完整实施合同，替代D1—D3；不依赖旧版互相覆盖的发布指令。历史编码/验证阶段见handoff.md；1.16.8及1.16.9的限定范围发布与验收见对应release文档。本次只整理合同，不重新线上核验。

## 0. 范围与固定源码

目标：已批准完整原型的手机名册/详情分层、常驻动作、桌面分栏，以及真实技能/本领展示和只读刷新。非目标：派单算法、交易、编辑、扫描、Runtime重启、DDL、全局导航重构。

核查时间见 evidence/source-baseline-d4.json（2026-10-17 10:29 +08:00）：

| 组件 | 本地HEAD | 查询到的远端develop/拟实施基线 |
|---|---|---|
| Web | c84c5a2a279b2a662b4b6b2f1b26c4708317b1ab | 同本地；tree 398dfd6c47996facb7fb922e6f3cdf6c88850d21 |
| API | c1e97923bf2325e3ada33b7e2816f203630f020d | 58b4b5f408257c6d5103d915e13c7927c1571e20 |

API拟实施tree：3e60bd5858735790b7886ef00a9a94614816fb75。以上是10:29准备基线，不是当前执行状态。实际已创建隔离worktree并提交双端候选，见handoff.md。API主工作区c1e9792属于另一任务的未推送测试改动（包括删除用例），不覆盖或自动合入；本任务从当时已发布到远端的58b4b5f保留完整测试实施。根脏修改与Web AGENTS.md保持。当前生产记录只读核对为API1.16.7/Web1.16.4，不是本次候选已发布。Runtime仍沿用历史6a9d8d3证据，不冒称本轮重新检查。

统一接口规范：`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2，SHA256 `7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f`。

原型唯一入口：`/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/prototype/index.html#agents`；准确源指纹、截图和批准记录见ui-review.md。原型通过不代表产品通过。

## 1. 数据权威与接口职责

本领沿用AgentService原toRuntimeDTO投影：agent_runtime.abilities，空白字符串才回退agent_persona.abilities，字面量[]保留空。技能来自安装权益/版本/回执/包摘要核验，再核对认证Runtime目录；不从本领、名字、星号或角色推导。

历史源码已确认注册回调采集工作区本领，普通定时heartbeat不带abilities；profile手填abilities被忽略。refreshCapabilities会重注册并影响channelConfirmed，本期绝不调用。页面刷新只读已上报记录，不承诺重新扫描，也不把图片修改改名图片生成。

| 接口 | 唯一职责/本期处理 |
|---|---|
| POST /agent/roster | 名册摘要与现有候选/本领筛选；保留abilities，不加安装技能目录 |
| GET /agent/map | 可见地图投影；保留abilities，不带私有安装事实 |
| GET /agent/{agentId} | 基础详情与原版本投影；保留abilities，不加技能核验 |
| GET /agent/capabilities | 本领协作索引，继续供AI工具/WebSocket等使用；不是安装技能 |
| skill-entitlements | 市场权益/订单关系；不加abilities，不作为详情核验接口 |
| /agent/tasks/{taskId}/skill-capabilities | 任务授权下的CALLABLE目录；不放宽grant |
| 新GET /agent/{agentId}/profile-capabilities | 当前owner单Agent详情/刷新；复用本领投影＋只读安装/运行观察 |

不删除旧接口的本领：相同权威在不同业务投影出现并不是重复存储。旧roster/基础详情经SkillRosterProjection可触发SkillAgentVersions的ForUpdate/CAS维护，权益接口还受市场开关影响；不把这些接口拼装为“无副作用刷新”。新GET走requireApiKeyOwnedAgent，无版本维护；UI不为本领另外调用旧详情/capabilities。

## 2. 确定的布局与交互

### 2.1 框架和视觉

- ≤720px：Agent专用全屏外框，复用--hall-visual-height的真实视口高度，避免只用100vh；保留全局关闭入口。初始只显示名册，点行进入详情，不与名册上下堆叠。
- >720px：约43%/57%双列，minmax(0, …)，列表与详情内容独立overflow:auto；详情未选择时显示选择提示，不自动请求首个Agent。
- 详情结构：身份区/技能/本领/刷新说明位于.agent-detail-scroll；.agent-detail-actions是其同级底部区域、flex:none。详情容器display:flex/flex-direction:column/min-height:0，内容flex:1/min-height:0/overflow:auto。不是把按钮position:fixed盖在正文上。
- 移动底部padding包含env(safe-area-inset-bottom)；长标题、版本、原因和标签overflow-wrap:anywhere/min-width:0；按钮可换行而不横向溢出。320px与390×480必须完整看见动作。
- 保持原型纸色、描边、朱砂本领和原头像；技能状态用文字＋颜色，不只靠颜色。刷新为次级操作，不抢密议主按钮。
- 返回名册保留选中、筛选和列表scrollTop；关闭关闭整个点将册。返回后再次点同一Agent仍进入详情，不取消选择。

### 2.2 详情信息与动作

按身份→技能→本领→刷新时间/说明呈现。技能标题旁显示“已核验安装N项”，只统计installationVerified；读取中、失败、无权不显示假0。每项显示title、version、安装核验、运行状态/原因。展示“运行就绪不代表已获任务调用授权”。本领标签保留原命名，空数组为“未录本领”。

无待处理任务：密议。存在待处理任务：保持现有密议/点将并议事及顺序。完全复用canStartConversation、canPointAndDeliberate、pointAndStartBusy、hasPendingTask及事件参数，不能用RUNTIME_READY替代动作授权。

刷新仅针对当前可见、owned、非system详情；busy/offline不阻止只读。开始刷新撤下旧READY；部分技能源失败仍可更新本领；整体失败显示上次记录，不宣称已刷新。无后台轮询、不新增重注册调用。

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
| 401 | Controller内为UNAUTHENTICATED；安全过滤器可能无JSON/code | 缺少有效用户认证；前端以HTTP status处理 |
| 404 | AGENT_PROFILE_NOT_FOUND | owner/租户/client/绑定不匹配、agent不存在、系统agent；统一隐藏存在性 |
| 503 | AGENT_PROFILE_UNAVAILABLE | Agent记录/认证依赖异常、数据完整性异常、无法安全完成读取 |

Controller产生的失败使用统一信封，data=null，安全msg；不返回堆栈、内部路径或配置。Controller之前的现有安全过滤器空401保留，不称整条认证边界已迁移统一信封；前端按status=401处理。不要把SQL/包损坏等故障一律翻译成404。

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
6. 共用核验器维持原重复记录输出与UNAVAILABLE判定，不改变任务目录数量和顺序。只有新AgentProfileCapabilitiesService投影按key/version分组：重复项合并为一项，installationVerified=false、runtimeState=UNAVAILABLE、reason=`SKILL_INSTALLATION_AMBIGUOUS`、title=skillKey。
7. Runtime前后读取不一致仍按现有逻辑降为 `SKILL_RUNTIME_CHANGED`，安装核验布尔值保持；不沿用旧READY。
8. 更新现有全部SkillCandidate构造点，包括taskCatalog无fence分支；任务端wire字段、CALLABLE判定、权限及费用规则不变。

不拆新的通用能力平台，不把agent模块反向依赖chat。chat当前build.gradle已依赖agent-service/API，新增类放chat无需改依赖方向。

## 5. 前端逐文件实现

根路径 `/home/isp/wsps/cyf/web`。不改路由、市场页面或全局HTTP协议。

### 5.1 唯一新增前端模块：纯投影与文案

新增 `src/composables/juyiting/useHallAgentProfileCapabilities.js`；纯投影、原因映射与composable在同一文件分别命名导出，避免为一次展示拆出额外模块：

- 导出 `agentProfileCapabilitiesProjection(raw, expectedAgentId)`：按3.2做精确字段/类型校验；不合法返回null，完整合法则返回只读对象。
- 验证agentId完全相同、数组不重复key/version、READY⇒installationVerified=true且reasonCode=null、UNAVAILABLE⇒reason非空、目录失败不得带items/revision。
- observedAt/lastSeenAt使用Number.isSafeInteger；revision按非负十进制字符串校验且不转数字；技能版本仅验证非空字符串。
- 导出显示函数：安装标签、运行标签、原因文本；所有未知合法reason统一“暂不可用”，可显示机器码供排查，不显示内部详情。
- 已核验安装数量由installationVerified计数，不能使用items.length或Runtime READY数量代替。

### 5.2 同文件内的异步状态

同上文件导出 `useHallAgentProfileCapabilities`：

参数 `{api, getAgent, identityKey, enabled}`。返回 `{projection, loading, error, refresh, reset, dispose}`。参照现有useHallSkillCapabilities，但不要复用任务目录的taskId依赖。

- fingerprint=`[identityKey(), enabled(), agent.agentId, agent.boundToMe, agent.systemAgent]`，不依赖整个Agent对象，避免名册替换对象导致请求风暴。
- enabled只在点将册实际可见且agentPanelRef.profileVisible为true、身份有效、Agent非系统且boundToMe=true时成立；boundToMe只是UI提示，后端仍权威核验。
- GET使用 `agentApi.get('/'+encodeURIComponent(agentId)+'/profile-capabilities', {}, {autoLoading:false,needAuth:true,signal})`；agentApi已有`/agent`前缀，不重复拼前缀。
- 每次开始递增epoch、abort前一个请求、清projection与error；对比发起时指纹和epoch，只有最新且未disposed结果可写入。
- watch使用flush:'sync'；关闭点将册、切换Agent/身份时立即清空，旧成功/失败/finally都不得污染新状态。
- refresh在loading期间按钮disabled；接口仍可被程序触发，epoch负责latest-wins。
- 无定时器、无localStorage、无跨用户缓存；abort只取消自己的HTTP，不取消Agent工作。

### 5.3 AgentPanel.vue：局部视图状态与组件契约

保留原props/events；新增profileCapabilities、profileCapabilitiesLoading、profileCapabilitiesError、profileReasonText（父组件传文案函数）、active、identityKey、panelSessionKey，均提供安全默认值；新增refresh-profile-capabilities事件。不从子组件引入业务模块，新增import只来自Vue，兼容既有动态SFC测试加载器。

内部状态：isCompactRoster（matchMedia('(max-width: 720px)')）、mobileDetailOpen、listScrollTop、最近选中行的DOM引用。挂载注册media listener，卸载移除；非浏览器测试提供matchMedia fixture。不依赖coarse pointer决定720px分界。

暴露只读computed：canGoBack=active && isCompactRoster && mobileDetailOpen；profileVisible=active && selectedAgent有效 && (!isCompactRoster || mobileDetailOpen)；windowTitle=canGoBack ? '好汉详情' : '点将册'；暴露back()，仅能回退时清mobileDetailOpen并返回true，否则false。

| 事件 | 状态/副作用 |
|---|---|
| 新panelSessionKey、身份改变 | 清移动详情状态、滚动及焦点记忆；默认名册；旧请求由父级禁用/重置 |
| 点名册行 | 保存scrollTop，mobileDetailOpen=true，发原select-agent事件；nextTick只在活动移动详情聚焦详情标题 |
| back() | mobileDetailOpen=false；nextTick恢复scrollTop、选中行焦点；保留筛选/选中 |
| active=false | 不强制重置父级选择；禁止请求和隐藏DOM焦点；真正关闭重开由sessionKey重置 |
| selectedAgent变null或无效 | 回名册，不继续呈现旧详情 |
| 外部改变有效selectedAgent | 已在详情则更新此详情；移动名册不被动跳详情 |
| 跨720px | 保留selection；mobileDetailOpen不因resize置true，手机首次仍名册；桌面显示当前选择，返回手机恢复原移动层级 |

移动名册/详情互斥v-show并设置inert/aria-hidden，隐藏区不得键盘聚焦。详情标题tabindex=-1供进入时聚焦；内容刷新不重建整个详情DOM、不抢焦点；loading/error使用role=status。返回恢复前核对active与当前身份/session。

本领优先取与当前agentId匹配的成功projection.abilities（包括[]），否则取selectedAgent.abilities并标“上次记录”。当前行通过浅拷贝{...agent, abilities:freshAbilities}展示覆盖，保留currentTaskTitle优先，不写回名册/派单对象。返回名册禁用请求并清projection，显示原名册记录；不承诺跨关闭缓存最新覆盖。

### 5.4 JuyiHall.vue：父层接线、返回与布局覆盖

1. 添加agentPanelRef；传入上述props与profile文案函数；composable identityKey由hallIdentityScope＋apiStore.authorizationGeneration组成。enabled同时要求renderedPanel==='agents'、agentPanelRef.profileVisible、有效身份及owner/non-system；初始化ref为空时不请求。
2. panelSessionKey只在agents从不在panelFrames到加入时递增，不因列表/详情、请求、选人改变。卸载dispose；关闭/身份变化同步清投影；重新打开读取当前可见详情，不复用旧READY。
3. AgentPanel的select-agent改绑handleRosterSelectAgent(agent)：若ID等于当前选中，保留选择；否则调用原selectAgent(agent)。不要修改原selectAgent的同ID取消行为，地图等调用保持原语义。
4. 将Agent子层接入panelDepth、panelChildCanReturn、activePanelTitle，与现有tasks/treasure/library子层同模式。移动详情可返回时标题“好汉详情”，返回文案“← 名册”，名册标题“点将册”。不要新增路由或物理浏览器history协议。
5. returnPanel在原语音/离开守卫后、弹panelFrames之前处理agentPanelRef.back()。handleHallReturn优先走已有守卫链中的Agent子层返回，不能被showRootReturn直接closePanel短路；Escape同样先回名册，名册层再沿原退出规则。关闭按钮仍调用原closePanel，不能改成只回名册；不得绕过既有草稿、语音和会话守卫。
6. 只为agents添加紧凑全屏外框class，使用现有视口测量，不改useHallPanels全局分类。保留非Agent页面的高度、按钮和层级行为。
7. 同时修改组件样式与父层Agent专用deep规则：移除/替换移动agent-panel-body整块overflow:auto、agent-list max-height:44vh、detail-card flex:0 0 auto；调整后部桌面grid覆盖。它们是内容挤高和动作滚走的根因，不能只改子组件。生产源直接修这些选择器，不复制冻结原型的!important补丁堆叠。

不修改useHallData.js、全局HTTP、市场页面、任务skill目录或通用导航helper。列表初始加载仍走原流程；详情/刷新每次只有一个新GET，不重取roster/map。

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

## 7. 并发、安全与版本发布

响应是多来源观察值而非原子快照；复用安装/Runtime末尾复读及owner/绑定复查。无长事务、无写锁、不新增后台缓存。身份变化立即清空投影；晚到的成功/异常/finally均不能写当前状态。前端隐藏不是权限控制，后端始终核对owner。

前后端正式测试、构建、制品和部署分别复用Flow4403172/5260799。固定发布版本及每端commit/tree，各端同Run不可变制品及SHA256；不是把两端误说成同一个Run。develop不自动部署。本机仅预览/定向诊断，禁止本地正式打包或源码到生产路径。API先健康再Web；复用发布锁、备份及可恢复安装，不改变Runtime或DB。

## 8. 验证与完成定义

产品测试矩阵见acceptance-d4.md，执行顺序见plan-d4.md。原型证据仅作视觉审核基线；需要真实Vue组件/导航回归、双Flow正式证据与上线后只读几何/接口核验。任务动作在受控测试中验证，线上不为验收发任务、下单或调用Provider。

## 9. 一次编码的精确写集与完成定义

### 9.1 应用代码：6个文件

API根 `/home/isp/wsps/cyf/api`：

| 文件 | 类型 | 本次唯一职责 |
|---|---|---|
| chat/jia-chat-service/src/main/java/cn/jia/chat/api/AgentProfileCapabilitiesController.java | 新增 | 唯一GET、输入/认证上下文、HTTP边界 |
| chat/jia-chat-service/src/main/java/cn/jia/chat/service/AgentProfileCapabilitiesService.java | 新增 | owner只读聚合、proof分支、固定DTO与异常重复项投影 |
| chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatActionCapabilityService.java | 修改 | 内部安装核验布尔值、无Runtime观察分支；原任务wire不变 |

Web根 `/home/isp/wsps/cyf/web`：

| 文件 | 类型 | 本次唯一职责 |
|---|---|---|
| src/composables/juyiting/useHallAgentProfileCapabilities.js | 新增 | 响应闭包校验、状态文案、异步状态、身份/选择竞态 |
| src/components/juyiting/AgentPanel.vue | 修改 | 技能/本领展示、移动层级与返回、独立滚动/常驻操作、原动作保留 |
| src/components/world/JuyiHall.vue | 修改 | 实例化、同ID选择包装、子层导航/视口/父CSS接线、dispose |

不修改依赖文件、全局HTTP客户端、路由、数据表、名册存储、派单、Runtime；不另起通用抽象或框架。

### 9.2 测试代码：6个文件，与功能同轮写完

- API新增 `chat/jia-chat-service/src/test/java/cn/jia/chat/service/AgentProfileCapabilitiesServiceTest.java`。
- API新增 `chat/jia-chat-service/src/test/java/cn/jia/chat/service/ChatActionCapabilityServiceTest.java`。
- API新增 `chat/jia-chat-service/src/test/java/cn/jia/chat/api/AgentProfileCapabilitiesControllerTest.java`。
- Web新增 `tests/juyiting-agent-profile-capabilities.test.js`（纯投影+composable竞态）。
- Web修改 `tests/juyiting-agent-panel-actions.test.js`（保留原按钮回归并增加技能/本领组件断言）；不再新增单独的display测试文件。
- Web修改 `tests/juyiting-navigation-presentation.test.js`（Agent子层返回、深度、标题、同ID包装接线及非Agent回归）。
- 使用测试内固定fixture builder，不新增环境依赖或生产凭证，不按人名写生产期望值。

### 9.3 聚合方法的异常边界（不能留给实现猜测）

- path/query/body验证由Controller显式抛BAD_REQUEST，不把整个方法的IllegalArgumentException都当400。
- HostingRentHttp.actor的401映射Controller401；它的非401身份失败、HostingRentOwnerResolver的明确拒绝映射404。
- AgentServiceImpl.AgentBizException只对AGENT_FORBIDDEN/AGENT_NOT_FOUND映射404；其它业务/基础设施错误503。使用getCode()判断，不匹配异常中文。
- 仅在调用currentRegisteredProof的最小try/catch内将IllegalArgumentException映射为无可信Runtime；proof拿到后的scope不一致为503完整性失败，不允许退回无Runtime分支。
- 仅InstalledSkillDescriptorLookup.SourceUnavailable映射为skills局部UNAVAILABLE；其它异常503，不能将SQL异常冒充空技能。
- owner末尾复查在局部技能失败分支之后仍执行，不以partial success绕过身份变化。
- 框架缺少身份依赖导致既有resolver主动拒绝仍按其明确拒绝处理；未分类依赖/数据访问异常503。不新增全局依赖健康检查。

### 9.4 代码完成不是验证通过

本轮全部功能和测试代码写完、无TODO/空实现、所有接线和fixture齐备、差异仅在写集内，才记CODE_WRITTEN。未编译/未测时状态仍NOT_VERIFIED。

不存在“先写功能，30分钟后再把测试代码或遗漏分支算到部署阶段”的口径。验证发现必须修改代码时，补丁仍计入实际代码工作；记录实际耗时，不能维持虚假的30分钟完成结论。


> 2026-10-17执行补充：实际改动6应用＋6测试＋3配置文件。chat/build.gradle增加测试作用域oauth-resource项目依赖以覆盖真实JWT过滤链，无外部/运行时新依赖；Web package/lock升级统一发布版本1.16.8。隔离工作区、候选commit/tree、首轮编码约24分11秒及诊断边界见handoff.md与evidence/coding-candidate.json；后续修复仍计入实际编码，不把此计时称为已验证全部完成。
