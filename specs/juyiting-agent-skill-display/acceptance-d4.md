> 2026-10-17 发布收口补充：1.16.8已由API Flow152、Web Flow224部署并完成范围内在线验收。当前结果见 `release-1.16.8.md` 和 `integration.yaml`；下文旧NOT_RUN/阻塞/估算为历史阶段，不代表当前状态。

> 2026-10-17执行规则覆盖：前后端正式测试、构建、制品和部署均走Flow（Web4403172/API5260799），本文旧后端本地交付表述失效。用户已批准D4实施；产品代码已提交并进入正式Flow验证，部署须双端正式验证通过。原型/本机诊断不替代正式证据。

# 验收用例与验证入口 D4

与design-d4.md/plan-d4.md一起使用；全部测试代码同轮写完，之后统一运行，不按用例逐片发布。

状态：Web正式Flow222测试3041 PASS/2 pending、构建通过；真实组件+父CSS浏览器7视口PASS（合成数据，非完整应用/线上）。API全量Flow149失败，修复本次夹具后Flow150定向179项与layering通过（含23项新测试，非全量发布验收）；发布与在线验收NOT_RUN。本文为验收要求，逐项结论须匹配证据，不能整篇视为PASS。

## API服务：AgentProfileCapabilitiesServiceTest / ChatActionCapabilityServiceTest

新增位置：`/home/isp/wsps/cyf/api/chat/jia-chat-service/src/test/java/cn/jia/chat/service/`。

| ID | 输入/动作 | 必须断言 |
|---|---|---|
| S01 | 真实verified descriptor +同scope/fence/hash/runner的READY report | installationVerified=true，RUNTIME_READY，reason=null |
| S02 | 无任何entitlement | 200可投影，目录AVAILABLE/items[]；不调用Provider/下单 |
| S03 | 有ACTIVE权益但缺安装回执 | installationVerified=false，安装未核验；不显示READY |
| S04 | 已验证安装、没有唯一认证proof | 保留安装true；runtime UNAVAILABLE；原因是待核验而非擅自离线 |
| S05 | 已验证安装，Runtime没有该key/version或摘要不匹配 | NOT_DECLARED/BINDING_MISMATCH；不是无技能 |
| S06 | 初始Runtime READY，末尾catalog/fence改变 | 所有原READY变UNAVAILABLE/CHANGED，不显示旧就绪 |
| S07 | descriptor源抛SourceUnavailable | 本领仍返回；skills UNAVAILABLE/items[]，不是AVAILABLE空目录 |
| S08 | 同key/version重复descriptor | 新详情DTO唯一输出项，installationVerified=false，AMBIGUOUS；不重复Vue key。原TaskCatalog重复记录数量及UNAVAILABLE行为不变 |
| S09 | provider readiness reason为任意合法码，descriptor本来verified | 安装仍true；未知码不误判安装失败 |
| S10 | manifest为普通非执行包/损坏包 | NOT_EXECUTABLE或源不可用，绝不推定已就绪 |
| S11 | 无taskId、没有执行grant，用户拥有Agent | 仍能读取安装事实；TaskSkillPolicyService不被调用 |
| S12 | 市场销售开关关闭、Agent busy/offline | 不妨碍owner只读事实；不调用新工作准入 |
| S13 | 安装读期间被撤销 | 复用descriptor现有末尾复读，installationVerified=false或源失败 |
| S14 | 返回前owner/binding改变 | 整体拒绝，不把先前读到的items返回 |

所有测试显式验证：SkillAgentVersions、购买/安装、grant、任务调度、Provider、Runtime dispatch无调用。包含安装真而运行假，不只验证全绿场景。

## HTTP：AgentProfileCapabilitiesControllerTest

新增位置：`/home/isp/wsps/cyf/api/chat/jia-chat-service/src/test/java/cn/jia/chat/api/`。使用真实MVC/公共信封与异常边界，不能只直接调用Java方法而跳过HTTP层。

| ID | 输入/动作 | 必须断言 |
|---|---|---|
| H01 | 无JWT/无效JWT，真实安全过滤链；另测Controller拒绝非用户凭证 | 过滤器拒绝为HTTP401，允许现有空body；前端保留status=401且重认证。Controller产生401时必须统一信封和UNAUTHENTICATED。不能用mock直调Controller冒充过滤器集成验证 |
| H02 | 同client不同owner、同owner不同client、跨tenant | 404同码同安全msg，无目录存在性泄露 |
| H03 | 登录sub不能映射到当前jiacn/账户禁用 | 404，不信任仅JWT文字owner |
| H04 | query、body、Transfer-Encoding、非法agentId | 400；不接受替代owner/taskId等参数 |
| H05 | 正常成功/Controller错误 | 标准信封字段、真实HTTP状态、requestId header/body一致、private no-store；过滤器空401不虚构JSON字段 |
| H06 | 未知agent或系统agent | 404，与越权一致 |
| H07 | DB/认证依赖真正异常 | 503，不误报404或200空目录 |
| H08 | 白名单检查 | 无manifestJson/metadataJson/host/fence/session/凭据/包路径 |
| H09 | lastSeenAt超JS安全整数/内部字段不合约 | 503，禁止截断；合法null正常 |
| H10 | 连续两次GET | 无数据写操作、无CAS版本推进、无安装/Provider外部副作用 |

## 前端投影与异步

新增 `/home/isp/wsps/cyf/web/tests/juyiting-agent-profile-capabilities.test.js`。

1. 合法示例、空数组、partial失败正常；空本领覆盖旧标签。
2. 错agentId、未知字段、错误类型、数值skillVersion、重复skill key/version、READY但安装false/原因非null全部拒绝。
3. 计数使用installationVerified，不用items.length或运行READY数。
4. A请求慢→切B→B成功→A迟到：只保留B；A错误/finally也不能清B loading。
5. 同agent身份代际变化、关页、卸载均abort自己的请求并清投影；没有泄露前用户缓存。
6. 刷新开始清除旧READY；失败显示失败，不显示“暂无已登记技能”。
7. hidden/nonowner/systemAgent不发目录GET，busy/offline owner可读。
8. 开闭/选中变化自动刷新；同ID仅名册对象替换不重复请求；无轮询。

## 组件与浏览器

扩展 `/home/isp/wsps/cyf/web/tests/juyiting-agent-panel-actions.test.js`；所有新增展示断言并入此既有文件，不另建display测试文件。

| ID | 操作 | 可见结果 |
|---|---|---|
| U01 | 选有已核验图片修改技能的测试Agent | 分组标题是“技能”“本领”；显示“图片修改 1.0.0”，不改成图片生成 |
| U02 | 选无安装记录的测试Agent | 暂无已登记技能；有无本领不影响技能结论 |
| U03 | verified安装但Runtime不可用 | 已核验安装 + 运行状态待核验/具体原因，不显示可调用 |
| U04 | 点击刷新后后端返回新本领或[] | 当前详情及列表当前行摘要更新；底层派单名册对象没有被写改 |
| U05 | 点击刷新源失败 | 仅本领成功可更新；技能错误可重试；整体失败本领标上次记录 |
| U06 | 选非拥有者或系统Agent | 显示仅拥有者可查看技能，不发目录请求 |
| U07 | pending点将/密议按钮 | 既有顺序、事件参数、busy/权限控制保持 |
| U08 | 小屏320/390px及390×480短屏、长title/version/reason及多本领 | 无横向溢出，可换行/滚动，刷新和原动作可见可操作 |
| U09 | 键盘和读屏 | 按钮可聚焦，loading/错误有状态文本，不仅以颜色表达 |
| U10 | 从其他页回点将册、切身份/选人 | 自动读对应资料，无旧技能闪现 |

真实在线验收只读当前页面和GET：记录当时Agent ID（受控证据文件）、请求时间/源码版本、返回和截图；不要求吴用一定安装image-generate，不要求林冲一定无技能。技能安装状态若确实为空，也不能为“截图好看”创建订单。

## 验证命令边界

已阅读 `/home/isp/wsps/cyf/api/build.gradle` 与 `/home/isp/wsps/cyf/api/chat/jia-chat-service/build.gradle`。执行时仍须重读受测候选最新文件；本文不启动构建。

后端正式入口Flow5260799；以下选择器实现后在该Flow固定源码上经原编排入口执行：

```text
:chat:jia-chat-service:test --tests cn.jia.chat.service.AgentProfileCapabilitiesServiceTest
:chat:jia-chat-service:test --tests cn.jia.chat.service.ChatActionCapabilityServiceTest
:chat:jia-chat-service:test --tests cn.jia.chat.api.AgentProfileCapabilitiesControllerTest
validateLayering
```

相关已有回归：InstalledSkillDescriptorServiceTest、TaskSkillPolicyServiceTest，以及agent注册/状态更新、本领空数组和taskCatalog原wire测试。若原目录无现成taskCatalog测试，本次在ChatActionCapabilityServiceTest补断言，不声称已存在。

所有Gradle调用必须走 `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle`，使用已登记本任务ID、实际cwd/tree、selector、fixture digest；不复制旧任务示例参数。未登记前不执行。正式后端验证固定干净源码，不在生产安装目录编译。

前端本机诊断可用已有Mocha入口选择新增与既有测试文件；正式测试和生产构建必须Flow4403172，绑定同run制品，不回退本机生产打包。详设验收仅做文档/JSON/路径/源码锚点检查，无需应用构建。


## D4复核追加断言

- 注册回调会采集本领，但统一Runtime普通heartbeat不携带abilities：测试不编造“点击刷新等待下一次心跳自动扫描”。页面GET只读取最近入库值。
- 不调用transport.refreshCapabilities；它会重注册并暂时撤销channelConfirmed，不属于只读刷新。
- 截图16个业务标签不能推导已安装16项技能；image-edit不能改名image-generate。
- 新目录不复制metadataJson；既有任务skill-capabilities的字段、调用授权、重复项处理没有变化。
- 30分钟只评价实际编码记录，不是测试通过条件；不得为达标跳过上面任一安全/契约断言。

## D4追加：接口复用与无副作用边界

| ID | 输入/动作 | 必须断言 |
|---|---|---|
| D401 | 连续调用新GET，市场开启与关闭各一组 | 无SkillRosterProjection、SkillAgentVersions、ForUpdate及数据库写入；旧名册行为不改 |
| D402 | runtime本领非空、空白、字面量[]三组fixture | 与原toRuntimeDTO投影一致；空白才回退persona，不重写解析规则 |
| D403 | 手动刷新当前卡片 | 仅当前Agent一次GET，不调用map/roster/personas/catalog；不变更名册/任务选项 |
| D404 | 新GET网络失败或503 | 名册不清空，选择不丢失；旧本领标上次记录，旧READY撤下 |
| D405 | 原能力索引/任务目录回归 | AgentCapabilityDTO、WebSocket回执、TaskCatalog字段/授权不改；无fence分支及全部SkillCandidate构造可编译 |

复用原AgentServiceImplTest、AgentWebSocketHandlerTest与任务目录相关现有测试；新断言写入本批6个测试文件，不另建测试框架。上述为完整验收要求；逐项实际证据状态见handoff.md，不以本机诊断替代正式Flow。

### 接口职责边界补充

- B01：roster/map/旧Agent详情/能力索引保留原abilities字段与投影，不增加skills目录。
- B02：新详情只复用AgentService返回的abilities；不另查表实现第二套回退、不调用本领写入入口。
- B03：技能市场权益与任务技能目录不新增abilities，权限/任务授权不因面板可见而放宽。
- B04：初始名册之外，打开/刷新当前详情只发新GET，不为本领额外调用旧详情或capabilities；覆盖合法空数组，关闭/身份变化清除覆盖。

以上为完整合同断言；是否已取得正式证据以本次Flow结果为准。

## D4布局与父子导航验收（已做本机组件诊断，线上NOT_RUN）

新增断言分别写入既有AgentPanel动作测试、navigation-presentation测试和新composable测试；不另建框架。静态接线断言不能替代真实Vue/浏览器几何验收。

| ID | 操作 | 必须断言 |
|---|---|---|
| L01 | 390px首次开名册 | 仅名册可见/可聚焦；没有详情挤到列表下方；不预读隐藏详情 |
| L02 | 点Agent进入详情 | 正确Agent身份/技能/本领，名册隐藏且inert；首次可见即读一次GET |
| L03 | 内容远大于视口 | 仅中间内容滚动，底部密议边界始终在可视视口内，正文不被覆盖 |
| L04 | 390×480、320宽，长版本/原因/本领 | 无横向溢出、底部动作可见；双按钮不互相覆盖，安全区不遮挡 |
| L05 | 待任务/busy/无资格 | 密议/点将并议事顺序、事件、禁用条件与原测试一致；不以技能ready取代权限 |
| L06 | 滚动筛选名册→详情→返回 | 筛选/选中/scrollTop保持，焦点回选中行；再点同一Agent仍打开、不取消选中 |
| L07 | 返回/Escape/关闭 | 返回和Escape先回名册；关闭仍退出整个面板；保留语音/草稿等守卫 |
| L08 | 面板堆栈与标题 | Agent详情贡献一个子深度、显示好汉详情/←名册；任务/宝库/藏经阁原返回正常 |
| L09 | 移动与桌面跨720px、窄屏fine pointer | 按宽度切布局；不取消Agent选择、不误发隐藏详情请求，无旧内容闪现 |
| L10 | 1440桌面长列表/详情 | 约43/57分栏，互不带动滚动，底部动作可见 |
| L11 | 刷新中返回、切页、关页、切身份 | 取消自身HTTP，旧结果/异常/finally均不污染新Agent；不取消Runtime任务 |
| L12 | 移动隐藏详情、重新开panel会话 | 隐藏区不能tab进入；重开回名册，不残留旧身份详情或技能READY |
| L13 | 同ID替换名册对象 | 不重复请求，不改变父层非名册selectAgent原toggle语义 |
| L14 | 父deep与子scoped样式共同生效 | 不再存在移动详情flex:0 0 auto撑高、44vh名册占用详情屏的问题；非Agent面板无变化 |
| L15 | 组件生命周期/焦点 | matchMedia监听卸载清理；刷新不重建整块DOM抢焦点；返回nextTick不聚焦已关闭页面 |

浏览器输入至少1440×900、390×844、320×568、390×480。页面渲染后及内容滚动后测动作矩形：top≥0、bottom≤实际视觉视口高度，scrollWidth≤clientWidth；在支持安全区设备再核验底部留白。覆盖触摸与键盘，窗口变化及全屏关闭。只看截图或静态源码不能证明滚动/返回行为。

产品正式通过要求：双端Flow精确候选通过；真实Vue浏览器验证记录输入版本、视口、响应fixture/当前只读响应及截图；发布后只读业务核验通过。既有完整原型23项观测仅证明原型，不充抵上述NOT_RUN条目。

> 2026-10-17执行补充：实际改动6应用＋6测试＋3配置文件。chat/build.gradle增加测试作用域oauth-resource项目依赖以覆盖真实JWT过滤链，无外部/运行时新依赖；Web package/lock升级统一发布版本1.16.8。隔离工作区、候选commit/tree、首轮编码约24分11秒及诊断边界见handoff.md与evidence/coding-candidate.json；后续修复仍计入实际编码，不把此计时称为已验证全部完成。
