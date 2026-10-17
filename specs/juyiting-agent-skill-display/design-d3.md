> 历史归档：2026-10-17已由D4同类文档替代。本文不是当前开发/发布指令；后端本地交付、待审核及旧布局表述均不得沿用。

> 2026-10-17执行规则覆盖：前后端正式测试、构建、制品和部署均走Flow（Web4403172/API5260799），本文旧后端本地交付表述失效。当前仅更新UI-2原型，用户明确确认后才开发；不因原型检查通过启动应用构建或部署。

# 点将册技能、本领展示详设 D3

**当前唯一实施详设。D1/D2保留历史，临时“撤回聚合接口”聊天建议不作为执行依据。**

本版按完整改动一次编码、一次集成候选、统一验证发布组织。30分钟是用户要求的整轮编码目标，不是已验证的耗时结论或无条件保证；不以压缩时间为由删身份隔离、安装证据、竞态控制或测试代码。计划见 `plan-d3.md`。

日期：2026-10-16。范围和权限以 `spec.md` 为准。本文区分**已核实事实**与**待开发的目标实现**；下述接口尚不存在，不得报告为已上线。当前实施文件仅为本D3、plan-d3.md及acceptance-d3.md。

## 0. D3接口复用核查与最终决策

核对日期：2026-10-16（Asia/Shanghai）。本节取代聊天中“撤回聚合接口、刷新全名册”的临时建议；该建议没有实施。证据见 `evidence/recheck-d3.json`。

### 0.1 既有接口不是同一职责

| 入口 | 实际返回/消费者 | 副作用或约束 | 本期处理 |
|---|---|---|---|
| GET /agent/capabilities | AgentCapabilityDTO[]：abilities、roles、状态、负载、成功率、协作提示等；服务方法也用于AgentTools.listAgentCapabilities、WebSocket.sendCapabilityIndex和状态发布 | 是协作本领索引，不包含安装/Runtime技能核验；未在本次搜索的Web源码中发现该HTTP路由直接调用，不能据此断言所有外部调用方不存在 | HTTP、服务、DTO与事件均不改，不废弃 |
| POST /agent/roster | 分页AgentRuntimeDTO，点将册和任务本领选项共同消费 | Controller调用SkillRosterProjection；市场开启时requireOwned→ForUpdate→ensureVersion/advanceVersion，可能维护CAS版本 | 保持原初次加载和原刷新入口；不将详情刷新接到此入口 |
| GET /agent/{agentId} | 已有单Agent详情，返回AgentRuntimeDTO，含abilities | 同样调用SkillRosterProjection，不能因为GET就假定没有持久写入；并无已核验安装/运行目录 | 不改已有详情契约和版本投影 |
| GET /agent/{agentId}/skill-entitlements | 市场权益、订单/安装/产品版本ID和grant版本；useSkillMarket消费 | 市场开关、事务及requireOwned版本维护；不是安装与运行事实 | 不改市场API，不将权益ACTIVE等同于技能就绪 |
| GET /agent/tasks/{taskId}/skill-capabilities | 指定任务下的CALLABLE/UNAVAILABLE与费用信息；useHallSkillCapabilities消费 | 必须经过assignment/grant；跨owner任务授权边界不同 | 不放宽权限、不造taskId、不供点将册冒用 |

`GET /agent/{agentId}` 是本轮明确补查的替代项；之前只讨论名册与本领索引是不完整的。

### 0.2 四个方案的影响比较

| 方案 | 刷新请求/影响 | 结论 |
|---|---|---|
| 全部接进现有 /capabilities 或 /roster | 批量Agent目录核验；扩散到协作索引/名册，且名册可能进入版本维护 | 不选：本需求只看当前Agent，不能让全名册承担安装核验成本 |
| 扩展 GET /agent/{id} 返回技能 | 单请求，但要改共享AgentRuntimeDTO和现有详情投影；现有观察器在chat-service，agent-service不能直接反向依赖它 | 不选：要引入跨层接口/实现接线或移动观察器，并处理原有CAS链路；不是“加一个字段” |
| 新增技能GET + 复用roster或单详情刷新本领 | 每次详情刷新两请求、两套成功/失败/身份切换状态；仍可能触发既有版本维护 | 不选：只减少少量返回字段，不减少技能核验实现；名册刷新还会重新推导选择对象和任务本领选项 |
| 新增当前Agent只读详情聚合GET，服务层复用原本领投影和技能观察器 | 当前Agent一次请求；不刷新全名册、不经过SkillRosterProjection、不动现有市场/任务/协作接口 | **选定**：本次限定范围内影响最小；代价是维护一个新增路由和明确的详情DTO |

若调用现有 `loadAgents()`，还会并行读取map、roster、personas/catalog三个入口，而不只是刷新一项本领。若仅调用loadRosterAgents，错误路径会清空allRosterAgents并reconcileSelectedAgent；这也是不将详情按钮接到列表加载器的原因。这里是源码影响分析，不是性能压测结论；没有声称毫秒级收益。

### 0.3 最终方案与复用边界

保留 `GET /agent/{agentId}/profile-capabilities`。它是点将册专用的owner只读聚合视图，不是第二套本领业务：

- 本领复用 `AgentService.requireApiKeyOwnedAgent` → `toRuntimeDTO`，不在新服务中另写persona回退、解析或扫描规则。
- 技能复用 `InstalledSkillDescriptorService.read` 与 `ChatActionCapabilityService` 的现有核验链；新增无可信Runtime观察分支，绝不照抄另一套匹配算法。
- 只构造 `agentId/observedAt/abilities/lastSeenAt/skills` 白名单DTO，不返回整个AgentRuntimeDTO/内部SkillCandidate。
- 新GET不调用SkillRosterProjection、SkillAgentVersions、ForUpdate、taskCatalog或市场entitlements。
- 返回本领字段有表示层重叠，但没有第二份存储、第二套维护规则或旧版兼容分支。列表摘要与详情返回同一字段不等于业务重复。
- 权衡透明：增加一个HTTP入口有维护成本；若未来重构完整Agent详情，可另行统一。当前不以假想重构扩大本次写集。

### 0.4 必须保留的影响边界

1. 协作/派单：旧本领索引、推荐权重、requiredAbilities、TaskCatalog wire和授权保持原样；共享技能观察器改动必须跑原任务回归，不能称“完全不接触任务代码”。
2. 市场/CAS：不改变旧市场或名册的版本维护行为；仅保证**新增详情GET自身**不做持久写入。不是宣称整个页面所有既有请求均无写入。
3. 前端：详情成功回执只覆盖当前选中卡片/当前行的本领展示；不写入allRosterAgents、地图、派单状态。发生身份/选择变化时清空覆盖，避免两套长期缓存。
4. 数据：同一原本领字段、同一技能安装/权益权威链，无DDL、回填或批量更改Agent。
5. 刷新：读取最新入库本领和当前技能观察结果；不是原子数据库+Runtime快照，也不是强制重新扫描。若用户需要“改变当前标签内容”，本方案不完成该动作，不能将读刷新冒称数据更新。
6. 视觉：保持已提供UI-1的技能/本领分区；接口决策不引入新页面/额外按钮。选择了拟调整预览不等于明确批准开发，审核仍待确认。
7. 部署：仅API/Web，无Runtime版本变更；先完整编码、统一正式验证、再按一个发布批次API→Web部署。

### 0.5 D3追加验收（与acceptance-d3.md同时执行）

- 新详情读取禁止触达SkillRosterProjection/SkillAgentVersions/ForUpdate及mapper写操作；连续读取不推进版本。
- 同一固定Agent数据，详情abilities应与原toRuntimeDTO投影一致；分别覆盖runtime非空、runtime空白回退persona、runtime字面量[]不回退。
- 详情刷新仅发当前Agent聚合GET，不调用/roster、/map、/personas/catalog、市场权益或任务目录。
- 原AgentCapabilityDTO字段、WebSocket能力索引与TaskCatalog字段/权限保持；验证共享SkillCandidate构造点，不漏原无fence任务分支。
- 新失败不清空名册、不变更任务本领选项；刷新失败明确为上次本领记录，并撤下旧技能就绪状态。

### 0.6 接口职责与本领字段归属（2026-10-16明确）

**本次不从任何既有接口删除abilities。保留理由是各自业务投影仍有职责，不是为旧版做兼容。** 一个事实可以用于列表、详情、协作索引；唯一性约束放在权威数据和解释规则，而不是“只准一个HTTP响应出现字段”。不将删除旧字段算入本次写集。

| 接口 | 唯一职责/消费者边界 | 本领字段处理 | 不承担的职责 |
|---|---|---|---|
| POST /agent/roster | 我的Agent分页名册；列表摘要及既有任务候选/本领选项 | 保留abilities；页面初始化的详情占位也可用它 | 不逐个核验安装技能；不作为新详情按钮的刷新入口 |
| GET /agent/map | 厅内可见Agent的地图投影；可见范围不等于本人拥有 | 保留现有abilities，不改变可见字段契约 | 不披露其他owner的完整安装目录；不作为详情刷新入口 |
| GET /agent/{agentId} | 已有Agent基础资料/运行状态详情；保留现有权限与版本投影 | 保留abilities；不再添加技能核验字段 | 不承担新的技能面板读取，不冒称纯只读版本查询 |
| GET /agent/capabilities | 本领协作索引：本领、角色、状态、负载等；同服务投影用于AI工具/WebSocket | 保留abilities；此处capabilities指协作本领，不是技能市场安装目录 | 不返回安装包目录，不表示任务技能CALLABLE，不因本领字段匹配而授予执行权限 |
| GET /agent/{agentId}/profile-capabilities（新增） | 当前owner在点将册查看单Agent技能/本领面板；仅此入口刷新该面板 | 从原服务投影读取abilities，不建表、不写库、不另写回退/扫描逻辑 | 不替代名册/地图/协作索引，不刷新全列表，不执行扫描/编辑/交易/派单 |
| GET /agent/{agentId}/skill-entitlements | 市场权益与交易关联事实，供技能市场使用 | 不新增abilities | ACTIVE不等于已安装/运行就绪；不负责本领展示 |
| GET /agent/tasks/{taskId}/skill-capabilities | 指定任务和目标Agent在当前授权下的技能目录 | 不新增abilities | 不作为无任务的个人技能面板，不扩大owner/任务grant边界 |

#### 单一权威与刷新一致性

- 本领唯一权威仍为agent_runtime.abilities及现有agent_persona.abilities回退；新接口复用AgentService原有投影。旧索引也是由AgentRuntimeDTO派生，不新增本领解释器。
- 本领上报写入仍走原注册/状态更新路径。本次没有新增写接口；不从标签反推安装技能，不通过市场购买改写本领。
- 页面首次加载：名册供列表与本领占位；打开拥有者详情后只请求新GET。占位/失败旧值标“上次记录”，成功后当前详情和当前行使用同一回执（包括合法[]）。
- 详情刷新只请求新GET；成功不回写allRosterAgents、任务候选或地图。列表的批次记录与详情的后续记录可能来自不同时间，这不是两个权威；不声称所有区域全局同时刷新。
- 关闭详情、换Agent或换身份，撤销详情覆盖；不保留第二份长期本领缓存。原名册刷新仍由原名册加载流程负责。
- 新响应的observedAt是读取时间；原lastSeenAt是最近联络，不是本领生成时间。不能用两者宣称Runtime刚完成扫描。

#### 明确禁止的职责扩张与验收

- 禁止同时给roster、旧get、capabilities新增skills字段；本次安装/运行事实只增加到新面板DTO。
- 禁止点将册同时调用旧get或capabilities补取同一Agent的本领；初始名册已有资料不再重复发请求。
- 禁止“精简字段”导致列表本领筛选/任务匹配/协作索引回归；删除这些字段必须另立消费者迁移设计，不能夹带在本次中。
- 本次验收增加：旧响应abilities字段仍在、值投影不变；技能市场/任务目录不夹带abilities；详情刷新请求集合及名册/任务状态不被改写。无需新增应用文件。

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
- Runtime `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs`：`resolveProfileAbilities = profile => discoverWorkspaceAbilities(profile)`；注册payload调用它；旧presence辅助函数也调用它，但**当前统一Runtime定时心跳不调用该辅助函数且不携带abilities**。详见下方D2复核。
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

### 1.3 D2复核补齐及上一版纠正

固定17个既有源码锚点文件的SHA均再次核对未变。补查真实调用链、安全过滤器与前端错误解码，详情见 `evidence/recheck-d2.json`。

1. **本领真实上报路径**：`/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs` 的register调用executor.registrationPayload；该回调接到agent-client.mjs的buildAgentRegistrationPayload，才执行工作区扫描。heartbeat直接构造仅带messageId/status/durableStateHealthy的agent.presence，不带abilities。transport.refreshCapabilities会重新注册，并将channelConfirmed置false；它不是无副作用的刷新按钮，**本期不得调用**。因此本领刷新确定为重新读取最新已入库记录，不承诺扫描发生在点击之后，也不承诺下一个普通心跳会更新。
2. **401真实边界**：生产配置已有`/agent/**`认证覆盖，ResourceServerConfig以anyRequest.authenticated保护；未登录可由Spring Security在Controller之前返回空401。useHttp先按HTTP状态解码；即使空体触发PROTOCOL_INVALID_RESPONSE，异常仍保留status=401并触发现有重新认证流程。新功能不得假定所有401均有业务code，不修改全局认证链以迎合本页面。
3. **现有目录核心不去重**：D1将重复安装记录合并写进共用核验器，扩大了任务目录行为影响。D2只在新详情DTO投影中合并异常重复项；原TaskCatalog输出/判断不改。
4. **元数据泄露边界**：现有SkillCandidate.metadataJson包含参数schema等内部字段。新接口只显式构造第3节DTO，不能直接序列化InstalledCatalog/SkillCandidate。
5. **来源范围**：本次核实的是固定源码和可复用链路，不是生产每位Agent此刻的技能清单。历史发布/截图仅作背景，部署验收时才记录当前值。没有证据支持“生产状态都已核实”或“全部代码必然30分钟完成”。

以上不遗留实现方案选择：不新增Runtime扫描命令、不接任务目录凑数、不写库、不改派单、不改全局认证。生产动态事实不作为开发前提。

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

具体测试见 `acceptance-d3.md`，整轮计划见 `plan-d3.md`。接口/字段/状态/刷新方案已固定；视觉审核仍待用户确认。

已核实但不冒充的边界：生产当前每位Agent的技能和工作区不在本次只读源码核对范围；设计不以这些动态值为前提。上线验收必须读取真实当前值，不把历史“吴用已安装image-edit”或截图中的“林冲未录本领”硬编码进断言。

下一步是按固定基线建立本任务隔离开发工作区、登记ledger并一次性完成全量代码；不按文件建立独立任务、不分片验收或发布，也不是再次研究“到底复用哪个接口”。基线若变化只检查本文命中路径的差异并记录，不回退其他聊天提交。


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
| src/components/juyiting/AgentPanel.vue | 修改 | 技能/本领展示、刷新、当前行展示覆盖、原动作保留 |
| src/components/world/JuyiHall.vue | 修改 | 实例化、传参、刷新事件、dispose |

不修改依赖文件、全局HTTP客户端、路由、数据表、名册存储、派单、Runtime；不另起通用抽象或框架。

### 9.2 测试代码：5个文件，与功能同轮写完

- API新增 `chat/jia-chat-service/src/test/java/cn/jia/chat/service/AgentProfileCapabilitiesServiceTest.java`。
- API新增 `chat/jia-chat-service/src/test/java/cn/jia/chat/service/ChatActionCapabilityServiceTest.java`。
- API新增 `chat/jia-chat-service/src/test/java/cn/jia/chat/api/AgentProfileCapabilitiesControllerTest.java`。
- Web新增 `tests/juyiting-agent-profile-capabilities.test.js`（纯投影+composable竞态）。
- Web修改 `tests/juyiting-agent-panel-actions.test.js`（保留原按钮回归并增加技能/本领组件断言）；不再新增单独的display测试文件。
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

## 10. 界面审核 UI-1（2026-10-16补充）

本次包含右侧详情布局变化，必须按用户要求提供视觉审核。稿件与界限见 `ui-review.md`；当前状态是待审核，不等同于已批准实现。维持现有名册外壳/整体列宽/动作语义，新增技能、本领和刷新分区。审核工具的前后对照、状态切换、示例数据均不进入产品。不得用30分钟编码目标跳过用户明确要求的视觉审核。
