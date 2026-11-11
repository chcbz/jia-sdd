# 招贤令角色本领占位值（2026-10-29）

- Owner 当前任务；仅处理角色内置目录的批量占位本领，不根据文学人设虚构真实技能，不改变已入伙 Agent 的 runtime 本领、技能、身份或授权。宋江系统职责保留。能力字段同时用于匹配评分，清空后基于这些占位标签的匹配分会变化；空不表示已验证无能力。
- 生产数据库只读核对：`jia.agent_persona` 108行，其中35行 strategy/execution/battle、72行 support/execution/scouting 均为排名生成的默认值；宋江1行独立。`agent_runtime` 有5行同样的占位值，未修改。现有公开内置目录也从源码生成同样的值，不同租户可能使用代码投影。
- 已按用户“想不到默认留空”将目标 tenant 0/client 的107行精确占位值事务更新为 `[]`；锁内固定身份、逐行条件更新并事务回读，宋江、已入伙 runtime 记录和其他内容不变。旧值私有备份及条件恢复说明见 `/home/isp/state/cyf-persona-abilities-20261029/`。直接数据库操作不触发应用缓存失效；已核源码目录缓存默认一分钟有效期，未以此声称线上页面已验收。
- API 新候选：`/tmp/cyf-persona-abilities-20261029`，基线远端 develop `ffc5f52b7462c7bab23302f5a8481e7fbfc5640c` tree `f0bfa1f5689986a6b8440272a87e8010692aae9a`。更改 `agent/jia-agent-core/src/main/java/cn/jia/agent/common/WaterMarginPersonaCatalog.java` 和相邻测试，使非系统内置角色默认空；未提交、未合入、未 Flow 测试、未部署。`git diff --check` 通过。该源码修复未上线，其他租户代码投影和后续源码启动仍可能产生占位标签；不得将数据库更新等同全部修复。
- 下一步：固定候选，按 `api/build.gradle` 和 `ops/orchestration/README.md` 走 Flow 定向测试及必要回归，发布须单独授权；验收目录与匹配影响，并独立决定已入伙 Agent 记录是否需处理，不覆盖真实运行能力。

## 好汉详情本领维护交互原型（待用户确认）
- 2026-10-29：只更新现有原型 `web/prototypes/juyiting/`，入口 `/index.html#agents`；本人好汉详情本领区提供就地编辑，每行一项，可清空、保存和取消；其他人的好汉只读。明确能力介绍不代表已安装技能。交互仅在浏览器会话保存离线示例，不访问生产 API、数据库或 Runtime。
- 变更 `ability-edit.js`、`ability-edit.css`、`index.html` 和原型规格，任务方案追加至 `specs/juyiting-ui-baseline-20261006/optimization/spec.md`。沿用原工作区并保留先前脏改动，Web HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`，原型与线上版本不等同。
- 验证：`node --check`、`git diff --check` 通过；现有 `serve-preview.py --port 18786` 进程归属正确、HTTP 200。Chromium 390×800 与1280×800 模拟视口验证吴用编辑保存、重新打开、取消未保存修改、清空、其他好汉只读，均通过，无横向溢出。未做全站回归。浏览器打开请求已发送给 Codex，返回 queued；不声称已在用户端看到页面。
- 用户明确要求先确认；等待用户确认后再开展接口/源码实现及验证，不进行生产发布。
- 用户反馈保存按钮灰底白字：原因是原型通用 `.mmd button:hover` 和基础按钮样式覆盖局部主按钮背景。已限定修复本领编辑保存按钮的普通、悬停、键盘聚焦样式，并更新预览 CSS 缓存标识；未改产品源码。Chromium 390/1280 两视口分别核对普通、悬停、focus-visible 和悬停+聚焦的实际计算颜色与轮廓通过。仍待用户确认原型。

## 用户确认并授权实施（2026-10-29）
Owner当前任务；范围为本人好汉本领维护、空默认与必要回归，非本人只读，保存失败保留草稿，不修改技能/任务状态；用户授权完成后版本化部署。Web develop 3236adc8bbe08b9b436cbcef5cfa3dadd52e2bba；API 远端 develop 7c4fb10624e0918ddbde81c7408afe09ddaadedc（已查询），API已有候选 worktree 基于 ffc5f52b，保留后调整基线。既有工作区均有其他未提交修改，不覆盖。跨端公共协议遵循 `api/docs/interface-standard.md`（固定版本1.4，待源码设计时核对）；先进行最小合同及并发/ACL回归，再固定源码走Flow，部署与线上核验分开。

## 实施基线和进一步核对（2026-10-29）
- API 任务 worktree 已安全切换至已 fetch 的 develop `7c4fb10624e0918ddbde81c7408afe09ddaadedc`，原非系统角色空默认修改及其测试仍保留；`git diff --check` 通过。Web 基线 `3236adc8bbe08b9b436cbcef5cfa3dadd52e2bba` 曾建立干净隔离 worktree 定向核查，检查后已移除。两个主工作区的无关修改未覆盖。此为本地固定基线，不代表其后远端未变化。
- 精确核对 `AgentServiceImpl`：`requireOwnedAgentForUpdate` 在事务内锁定身份与 runtime 并校验租户、客户端、所有者及绑定，可作为保存接口身份控制的参考；`updateStatus` 会额外写任务、错误、心跳及技能观察，不能直接用于此需求。注册时 `resolveRuntimeAbilities` 优先采用上报的 abilities，状态上报也可覆盖该字段；因此仅增加保存接口仍会导致用户编辑在后续上报时消失。必须明确并实现持久化字段权威关系与兼容、能力匹配影响以及旧值处理，再验证注册/上报交互，不应仅修改 UI 或直接复用状态接口发布。
- 产品详情通过 `useHallAgentProfileCapabilities.js` 投影 `profile-capabilities`，严格检查响应字段并使用身份隔离；`AgentPanel.vue` 显示的本领有名册回退。保存/读回实现须同时处理刷新失败、身份切换和旧投影，不能仅更改卡片显示。
- 状态：本轮尚无可发布的跨端实现，无正式测试、构建或部署；用户部署授权仍有效，不代表允许发布不完整候选。

## 用户明确运行信息职责（2026-10-29）
- 请上梁山时初始化基本资料和默认本领，本领此后由本人维护；注册和状态上报不应覆盖基本资料或用户本领，仅保留必要身份、运行声明及动态状态。动态在线/任务/错误、能力声明及身份验证不可一并删除；现有能力匹配消费者和旧客户端兼容需覆盖。
- 已同步原型及优化规格。API `bindPersona` 新绑定时通过 `createRuntimeFromBinding` 初始化资料、本领，已存在 runtime 的重复绑定返回现有值；当前 `register` 和 `updateStatus` 仍会写入本领，产品尚未修改。后续应在服务端保障旧客户端携带字段也不覆盖，不能仅停止新客户端上报；保存接口采用本人身份及绑定校验、并发防覆盖、权威读回。保持已授权部署目标，完成实现及验证之前不发布。

## 用户取消旧客户端兼容要求（2026-10-29）
用户决定相关组件同时部署，不要求保留旧客户端协议兼容。仍需维持现有身份/ACL、运行时会话防护、并发、制品完整性和可恢复发布；不应推断所有线上实例都可原子切换，部署顺序、短暂混合期和版本确认须核实。

API 候选 `/tmp/cyf-persona-abilities-20261029` 在 develop `7c4fb10624e0918ddbde81c7408afe09ddaadedc` 上开始实施：注册不再写名称、头像、角色信息或本领，状态上报不再写本领；租户身份绑定校验、连接地址、动态状态及现有声明处理尚保留。此修改尚不完整且未经编译测试，原有 `AgentServiceImplTest` 中预期注册/状态覆盖本领及对上报本领校验的旧测试需要按新合同调整；旧 `resolveRuntimeAbilities`/`normalizeRuntimeAbilities` 尚未清理或重新用于编辑。继续实现独立本领保存（本人 ACL、并发防覆盖、空值、权威读回）及配套测试，审查前端和 Runtime 声明及真实消费者，再做正式 Flow 构建和跨组件部署。仅 `git diff --check` 通过，不能作为功能测试证据，不提交或发布该未完成候选。

## 继续实施快照（2026-10-29）
- 再次查询远端：Web develop `3236adc8bbe08b9b436cbcef5cfa3dadd52e2bba`，API develop 已前进到 `a5f28ec1dd84c33217e30ff748de898bc50c2f07`（相对旧基线仅 chat WebSocket handler 及其测试）；API 候选 worktree 已在不覆盖任务改动的前提下切换该基线。Web 干净 worktree `/tmp/cyf-persona-web-20261029` 已建立。查询仅代表当时状态。
- API 候选初步增加 `AgentAbilitiesUpdateDTO`、`PUT /agent/{agentId}/abilities` 和事务内持锁、本人归属、期望值比对、空列表归一化和提交后快照发布，并添加两个初步服务测试；原注册/状态更新本领逻辑已移除。代码尚未完成自检，不能认为并发/异常/身份语义已验收；以值比较不识别 ABA，须根据实际风险和合同评估。原先按状态上报更新本领的测试尚未调整，正式测试预期不能通过。
- Web 候选初步加入本人详情内编辑、保存和草稿保护、身份切换隔离及保存后读回；尚未运行组件、浏览器或正式测试。须审查响应冲突码、请求未知结果、切换/读回竞态、样式及状态 UX；不得作为可发布实现。
- Runtime 源码修改、两端必要回归、Flow 制品、安装和线上核验均未完成；未部署。两候选仅执行 `git diff --check`，不代表编译或功能通过。下一步完善合同及测试、审查并修复候选，再按用户授权和当前 Flow 分工交付，避免部署半成品。

## 连续实施及发布准备（2026-10-29，Owner 本任务）
- 目标/非目标：只实现本人详情本领维护、空默认、注册/presence不覆盖资料；不把本领当技能就绪，不改任务/身份/技能授权，不做旧客户端双轨，不清理既有真实本领。用户已明确授权三端实施和部署。
- API 隔离工作区 `/tmp/cyf-persona-abilities-20261029` 已刷新到远端 develop de6776fb3092a3e71aa5004d115c1280b742f2aa（tree e20dea6b8ac5610064d37fe1774bbf3ecb6e0ae0），保留前任务64K传输修复；Web `/tmp/cyf-persona-web-20261029` base 3236adc8bbe08b9b436cbcef5cfa3dadd52e2bba；Runtime复用 `/home/isp/wsps/chcbz/isp-install` base a4940cbb21342e9acfbc7904e4bc48e4241c097e，不包含无关 specs/。主工作区原有脏内容未覆盖。
- 公共接口标准固定 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4；职责 RB-1。API 增加 PUT abilities（本人身份/绑定/行锁、当前值CAS、提交后快照），HTTP400/403/409/500按真实结果返回。CAS防覆盖不同当前值，不跟踪ABA或编辑历史；不新增迁移。注册/状态DTO去掉资料/本领；保留运行声明和会话fence。相同compact fixture跨API/Runtime同步。
- Web实现每行一项/去重/可清空，保存后权威读回；冲突/网络未知保留草稿并显式核对，不自动重试。切换身份/好汉/面板隔离旧响应；红色保存按钮+键盘轮廓，编辑焦点/返回焦点。原型任务相关文件和规格单独收入候选，不带无关原型改动。
- 最早轻量反馈：Web编辑器+profile测试16通过；Runtime registration-footprint 3通过；仅本机诊断，不替代Flow正式证据。Java未在本机编译。测试/构建/制品、安装执行、线上业务验收各自记录，不将源码完成当上线。
- 安装前观测基线：API Run365 ab7b8b647e8b2a8980308b27c187bcc13cb3d269；Runtime1.3.22/Run95 33d78accc491ecb7db513ee2d49f3c0cec210634；Web1.16.73/Run372。此为当时磁盘记录，安装前还须重核实际PID/锁/维护归属。
- Flow/制品/安装控制证据放 `/home/isp/state/cyf-persona-abilities-20261029/release/`；此前API370失败为Tomcat测试夹具缺少servlet映射，de6776已修复，不原样重试失败源码。本任务新候选须独立验证。


## 最终交付（2026-10-29，核验至18:01 CST）
- 用户授权范围已完成：本人好汉详情就地维护本领，可空/取消/权威读回；并发冲突及未知结果保留草稿、显式核对，不自动重试。请上梁山初始化资料，此后注册和presence不写名称/头像/人设/本领；必要运行声明、动态状态和会话防护保留。不做旧客户端双轨，本领不作为技能、就绪或授权证明。
- API **1.17.15**，commit `648d644bc2fcc27c3ea7d67d49d6f541370c55eb` / tree `1b129103f880fcf159cd24e82aba381b4c1a2c77`，Flow **5260799/372 SUCCESS**：3295测试、0失败/0错误、159跳过，含真实64K边界/资料防覆盖/ACL/CAS；validateLayering与fresh JAR完成。JAR SHA256 `4683e8d17aabf97aad62160979485b5d498a510bc45ac5675e4bba54200f2bb0`。主机安装exit0，canonical路径/实际PID1881603/摘要/healthUP及8项路径检查通过。
- Web **1.16.74**，commit `ef8a2254348262960384772bf4203dccb0c53e9b` / tree `6e07308aa0b7bc1d12050860aa5efa6a34b51236`，Flow **4403172/375 SUCCESS**：3524通过、2pending、0失败；构建/扫描/上传通过。制品SHA256 `beacac32b5c6f9ffc03d0d4c951d7c93751aaad3aed4b8b21ffcd7f4641cf3cb`。主机安装exit0，公网index及实际引用入口/聚义厅JS/CSS共8资源字节一致。
- Runtime **1.3.24** / bridge **1.1.15**，commit `b74612c610457651b5fa2a4abb59e01de3f73529` / tree `a04d3845532b14dfe95cd8aebcecfa9aa676c840`，Flow **5264702/97 SUCCESS**：684通过、7跳过、0失败。制品SHA256 `1f13e0f7a2be66b9d483bd9aedb7efc14c0a5c35525771bf27903dd45fd465f8`。受控安装exit0、固定app/PID1898683/逐文件摘要核对，三个本机Agent连续3个新PID通道快照健康，current记录已标verified-active。
- 三组件候选已各自提交并推送develop。主工作区无关脏内容保留；API/Web任务隔离worktree及依赖链接已移除，未清理共享依赖或其他任务内容。主组件checkout仍含其他任务修改，根gitlink未强行切换以免覆盖。

### 真实失败及执行分工
- Web373因47处旧Hall夹具缺少新增composable失败；374修复后仍有5处旧夹具/提示预期失败；补齐全部相关loader及mounted交互回归后375通过。失败证据原样保留，不跳过失败用例、不重标旧Run。API370为前任务Tomcat fixture，正式候选继承de6776修复。
- 三条Flow只完成worker测试/构建/打包/上传，没有调用/等待主机，原云端配置均已恢复并readback。Run createTime→updateTime：API371秒、Web226秒、Runtime115秒，均未超过600秒；主机备份/启动时间另计，未另开付费安装Run。
- 实际主机顺序：API372安装/健康 → Runtime候选准备与停写备份（期间Web375已安装）→ Runtime97启动/通道核验 → 浏览器业务核验。保留短暂混合期事实，不宣称原子同时切换。
- Runtime首次安装在获取发布锁时发现其他维护任务正在持锁，未写生产、未抢锁；保存失败记录，待持锁进程自然结束后复核原1.3.23基线，复用同Run97制品安装。未重跑构建。

### 业务验收、恢复与边界
- 真实已认证公网Web：1280×900/390×844验证本人详情编辑焦点、取消返回焦点、红底白字保存及focus-visible、去重保存/权威读回、清空持久化、无横向溢出；实际并发PUT后409保留草稿并阻止自动重试，显式核对后可保存。非法本领400、系统/范围外403、未认证401。所有测试本领经期望值CAS恢复原16项，无付费模型/新任务执行。
- 另在新Runtime注册就绪后写临时本领，等待真实新presence ACK跨越35秒，再读确认未被覆盖并CAS恢复原值。此前启动中的“35秒未变”和首读不作为真实心跳/重注册证明，解释见browser/verification-scope.json；未专门重启/伪造注册来做自定义本领E2E，注册防覆盖依赖同候选Flow回归与已安装源码闭包。
- API旧JAR备份由现行安装器记录；Web已验证备份 `/home/isp/baks/cyf-web-flow/20261029-persona-abilities/`；Runtime程序与状态备份 `/home/isp/baks/cyf-agent-runtime-v1/20261029-persona-abilities-host/`（state SHA256 `d6b30d54e56753671543034ddc8b7fe3bfb3b88739bb854ceddcbf976a14bdf1`）。不得恢复旧状态覆盖新ACK/会话/业务事实；后续回退先评估兼容，按相同锁和恢复流程。
- **监控边界**：安装前已存在由其他任务创建的maintenance标记（2026-10-29T08:42:35Z），本任务未写/删除/恢复该标记；截至最终核对仍存在且摘要未变。API/Agent手动健康和业务检查已通过，但自动巡检仍受外部维护暂停影响，须由原持有人收尾，不冒称已恢复监控。
- 完整私有证据 `/home/isp/state/cyf-persona-abilities-20261029/release/`：candidates、run/restore/readback、各测试摘要、install-api/web日志与exit、api-online.json、web-public-resources.json、runtime-install/{installation,runtime-online}.json、browser/{business-smoke,verification-scope,presence-preserves-profile}.json。源码/Flow、安装、健康、定向业务分别记录；不外推全站或付费任务E2E。


## 原型视觉偏差修正（2026-10-29，Owner延续本任务）
用户指出1.16.74编辑入口/输入框/按钮排列与已确认原型不一致，已确认是产品只实现最简样式的遗漏，不能归因浏览器。授权“继续”沿当前范围修正、验证并部署Web；API/Runtime不重建不重启。基线远端develop与线上均ef8a2254348262960384772bf4203dccb0c53e9b，tree6e07308aa0b7bc1d12050860aa5efa6a34b51236；API648d644/Runtimeb74612不变。主Web工作区有其他任务脏文件且HEADca22ac2，无法安全切换，使用唯一隔离worktree /tmp/cyf-abilities-alignment-web-20261029（codex/abilities-prototype-alignment-20261029），不覆盖无关内容。先固化原型既有视觉验收，不改变已确认设计，再还原组件；资料身份/CAS/未知结果保护不变。公共协议v1.4、RB-1沿前基线。最早验证为组件mounted回归+Chromium原型/完整应用计算样式对照，正式测试/构建走Flow4403172，固定制品主机安装。证据 /home/isp/state/cyf-persona-abilities-20261029/style-alignment/。


### 原型偏差修正已交付（2026-10-29，核验至19:03 CST）
- 根因：前轮只完成编辑功能和最简局部样式，漏了完整原型的输入框/说明/操作区，不是浏览器缓存导致。先补充唯一原型规格与优化方案的视觉验收条款，再实施AgentPanel；完整原型主题实际覆盖编辑/取消为44px浅灰绿控件，不按孤立CSS的36/40px或朱红入口误还原。原型设计未另改。
- Web **1.16.75**，commit `f4737815d31e0d23fd43544bff594c2264d49ddd` / tree `e26136b3d256918aeb0a9e2a9ac7b05e54023462`，组件develop已推送。Owner延续本任务；范围仅本领编辑样式、提示及匹配回归，保留原ACL/CAS/未知结果处理。API/Runtime未重建、未重启，实际旧PID1881603/1898683仍在。
- Flow **4403172/376 SUCCESS**，3527通过、2pending、0失败，完整测试、Vite生产构建、扫描及上传成功。createTime→updateTime108秒，小于600秒。只有一次Run；start初始UNKNOWN因源码元数据未就绪，随后只读核对固定Run及完整commit，未盲重发。worker只构建上传；云端配置已恢复原值并readback。制品SHA256 `cfac8bff9ced93d6980232940306ab4c66422c126d2effaac71b4eca5eeece17`。
- 主机独立安装exit0、612份文件摘要绑定；先核对375基线并持发布锁制作备份 `/home/isp/baks/cyf-web-flow/20261029-abilities-prototype-alignment`（归档SHA256 `5cfef167b6c6e60859b05b9f4c2ca60d400aa5b78fcaaddea82683de94c232ca`），随后既有安装器assets-first/index-last发布。安装后公网index、实际入口和引用的聚义厅JS/CSS等8资源字节与本次制品一致，不以HTTP200代替版本核验。
- 正式产物安装前在本任务私有Chromium中仅拦截静态GET提供固定dist，API仍真实；安装后关闭拦截并重载真实公网页面，两轮均通过1280/390与原型完整计算样式逐项比对，并覆盖1440/320/720/721共用样式/排布和无溢出。验证编辑入口、label/说明/placeholder、输入框尺寸/色值/内边距/圆角、取消在前保存在后/右对齐、保存hover及键盘focus-visible保持朱红底白字、取消焦点返回。截图与computed JSON落盘；非实体设备软键盘、非全站视觉验收。
- 公网行为增量：更改本地草稿后取消不写服务端、重新编辑无残留；以原值保存，一次PUT200且expectedAbilities==abilities，不植入临时业务数据。空值/冲突/未知结果仍由同候选完整回归覆盖，前轮真实业务验收保留原证据，不借样式修复重复付费模型或新任务。
- 诊断脚本曾因残留焦点/已打开编辑态取样及嵌套换行未转义失败，纠正脚本后通过；未修改产品以迁就断言。前两次save smoke为表达式语法错误，未发写请求；离线校验后才重跑修正版。详见browser/diagnostic-scope.md。不得混同产品测试失败或隐藏失败记录。
- 本轮只读检查发现其他任务原maintenance文件已不存在；本任务未删除/恢复该标记，不宣称由本任务恢复监控。未覆盖主Web/root无关脏内容，根gitlink仍不强行切换。稳定知识已回写runbook。证据 `/home/isp/state/cyf-persona-abilities-20261029/style-alignment/`（delivery-summary、web-run、artifact、restore、backup、install、public-resources、browser/*comparison及public-save-smoke）。
- 收口：本轮唯一隔离Web worktree及其共享依赖链接已移除；私有候选dist预览目录已删除，固定制品、备份、截图和测试/安装证据保留。未清理其他任务目录或备份。


## 管理技能右对齐补修（2026-10-29，Owner延续）
用户指出生产管理技能仍居中；继续既有视觉修正及发布授权。范围仅技能标题栏：原h3/button/small三项space-between使数量占右，调整h3/small/button及操作margin-left:auto；不改管理权限、安装协议或API/Runtime。原型先保留安装数量在左、按钮靠右并同步规格，再改产品。固定Web base f4737815d31e0d23fd43544bff594c2264d49ddd/tree e26136b3d256918aeb0a9e2a9ac7b05e54023462，远端develop当次查询一致，主checkout ca22ac2及无关脏内容不覆盖；唯一隔离工作区 /tmp/cyf-skill-heading-web-20261029（codex/skill-heading-right-20261029）。协议v1.4/RB-1不变；先定向mounted回归，完整原型与实际构建浏览器定向对照，正式测试/构建走Flow4403172，主机独立固定制品安装。证据 /home/isp/state/cyf-skill-heading-20261029/。


### 管理技能右对齐已交付（核验 2026-10-29T11:37:26.423726+00:00）
- Web **1.16.76**，commit `1fdc94ac152e07091016fb9d3d898acf37551a6c` / tree `31bd0b50e6cf3338006397c3f5bd165de72f49f3`，develop已推送；修改限标题栏DOM顺序及按钮局部样式、对应原型/规格和三条回归。不改变技能管理权限、业务调用与安装语义。主工作区及其他任务内容保留。
- Flow **4403172/377 SUCCESS**：3530通过、2pending、0失败；正式测试/构建/扫描/打包/上传完成，createTime→updateTime 126秒，小于600。仅一次Run；初始start UNKNOWN元数据随后只读核对完整source，未重发。worker没有调用或等待主机；云端配置已恢复/readback。制品SHA256 `0bc9589e425fd63af77a62496c8edf82c6c590aac84e19fa80250ad462074540`。
- 安装前核对376/f473781基线并持发布锁备份 `/home/isp/baks/cyf-web-flow/20261029-skill-heading-right`，归档SHA256 `7e58181c7d5e3ad22a1c9ac34df46d752799543828c3bb2bdd1264a058fccef0`；主机固定Run制品独立受控安装exit0，保留旧哈希资源、assets-first/index-last。线上index、实际引用入口和聚义厅功能JS/CSS等8资源与本次制品字节一致。
- 原型先改、浏览器先核对，再改产品。固定制品安装前用本任务私有浏览器仅拦截静态GET提供候选dist；随后完全移除拦截、安装并重载真实公网应用。两轮均按1280/390/1440/320/720/721逐项验证按钮为标题栏最后控件、与右边缘对齐、标题及安装数量在左、无溢出、按钮完整计算样式与原型一致。PC1280和手机390真实管理入口打开/关闭/返回焦点均通过，0 API写请求，不操作购买/安装或付费模型。截图及JSON位于本任务browser目录；非全站/实体软键盘验收。
- 源码/云端构建、独立安装、公网字节、真实浏览器结果分开保留。原型实际预览复用18786服务，不停止他人进程；此前setup因候选原型缺少独立skill-management.css而终止，在既有受跟踪interaction-completion.css追加局部布局规则后继续，未复制其他任务整套未提交样式、未影响产品测试。
- API/Runtime不重建不重启。稳定知识回写既有runbook；证据 `/home/isp/state/cyf-skill-heading-20261029/`，含delivery-summary、tests、run/start/reconcile、restore、artifact、backup/install/public-resources及browser对照。
- 补充真实诊断：候选首次取样早于profile数量GET完成（button已出现而small未出现），修正取样等待后通过；未改产品或重复Flow。安装器首读命中已知旧index，既有只读重试第2次一致后成功，未重新安装。证据报告变量重名修正仅重写文档，说明见browser/diagnostic-scope.md。唯一任务worktree/依赖链接和候选静态预览目录已清理，保留真实制品/备份/截图；无关工作区未动。
