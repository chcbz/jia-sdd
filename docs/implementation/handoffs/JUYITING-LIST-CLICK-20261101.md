# 聚义厅列表全区域点击 · 2026-11-01

## 范围和基线
- Owner：当前聊天；任务ID：JUYITING-LIST-CLICK-20261101。复用现有工作区，不建worktree，不覆盖已有修改。
- 目标：延续事项列表全区域点击，将聚义厅资料页列表统一为整行查看；先更新原型，再同步产品。
- 非目标：选材器多操作行、上传/回收/恢复/授权和接口合同修改、构建及生产安装。
- Web：`/home/isp/wsps/cyf/web`，branch `codex/juyiting-ui-workflow`；HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`，tree `962e513205e4805a601022285bdff557c71f37ac`。该工作区原有多处脏修改，本任务只作局部增量，不能将整个工作区提交或当固定受测候选。
- 本地 origin/develop 引用：`04c5240018eb4402194c84eb64f03e2f02192cbc`；2026-11-01本轮只读 `ls-remote origin refs/heads/develop` 返回相同SHA；当前线上版本未查询。
- 接口规范：`/home/isp/wsps/cyf/api/docs/interface-standard.md`，版本1.4（2026-10-24修订）；当前字节SHA-256 `2d36ffac1dc52c6db8d54b860695edd845b6688ea0808528c53218e39aec7a08`；本任务不改变接口。

## 责任与执行入口
Web负责交互展示，复用原来的 `openTreasureFile → openFile → workspace.select` 和禁用状态，不在行点击重复认证/业务校验，不联动API/Runtime。遵守RB-1及根AGENTS分层要求。

已读工具索引 `ops/orchestration/README.md`；先验证静态离线原型，后用既有 `personal-workspace-execution-component.test.js` 组件桩做轻量定向验证，不在本机生产构建。重型正式验证仍需Flow固定候选。

## 原型先行
- 唯一入口：`/home/isp/wsps/cyf/web/prototypes/juyiting/index.html#workspace`。
- 先改 `prototype.js` 的资料查看按钮和 `interaction-completion.css`，同步 `specs/prototype-spec.md` 与既有优化方案。
- 全部/资料/成果/回收站复用同一行模板；不改变详情内管理及版本语义。
- 检查脚本、截图和结果：`docs/implementation/evidence/juyiting-list-click-20261101/`。初次浏览器检查因现有全局Chromium包装器引用已不存在的临时二进制而未启动；不改共享包装器，改用本任务临时包装器调用已安装Chromium并清理。

## 状态
原型先完成更新并通过真实Chromium检查后，才修改产品 `PersonalWorkspace.vue` 及既有组件测试。原生查看按钮使用相对列表行的扩展命中区，复用原禁用/打开逻辑，无行级重复事件。标题、类型版本、留白、右侧按钮一致；保留长名换行与含文件名的可访问标签、聚焦整行描边。

### 验证与限制
- 离线原型：1440/390/320宽度共18项检查通过（每宽度标题、说明、留白、原按钮真实坐标点击，Enter和禁用）；长名无页面横向溢出；3张截图已生成并核看390px。结果 `prototype-results.json`。不属于生产浏览器验收。
- 原型诊断曾发现语义图标按钮的 `position:relative` 覆盖整行定位，已以资料行专用选择器修正；CSS优先级问题修正后再跑通过，不修改共享按钮系统。一次Enter测试缺少原生回车文本/页面稳定等待，补齐CDP输入与双帧等待后通过；没有为测试增加产品键盘事件。
- 产品既有轻量组件suite：`personal-workspace-execution-component.test.js`，6 passing，包含新增精确fileId单次打开、详情禁用及loading-detail禁用回归；保留内嵌/非内嵌音频及原资料导航用例。`component-tests.log`。它不是Flow正式测试，也不证明生产CSS浏览器已验收。
- `git diff --check` 通过。定向ESLint未全通过：HEAD基线6项既有属性换行错误，本次格式化所改列表行后剩余5项均在未改区域，无新增问题；保留 `lint-baseline.log` 与 `lint.log`，不顺手全文件清理。未做本机生产构建。
- 未提交、未合入、未运行Flow、未安装生产；工作区其他修改保留。下一步如需交付固定候选，先按归属抽取本任务增量，避免夹带当前脏工作区其他任务改动，再走Flow正式验证；不自动部署。

### 耗时
定位/实现/验证/等待未做独立计时，留空，不作缩时承诺。

## 用户截图反馈补正（2026-11-01，同Owner）
用户指出资料行尾应为右箭头，且办事原型整行点击未生效。本轮沿用上述源码基线/工作区，不修改其他任务内容。

- 根因：原型的 `semantic-icon-only` 将事项箭头按钮设为 `position:relative`，先前事项列表扩展伪元素因而以按钮而非整行为定位基准。上一轮18项浏览器结果只覆盖资料页，不能作为办事页已修复的证据；原结论范围在此补正。
- 原型先改：在事项行责任范围覆盖按钮定位为static；资料页 `complete-file` 分类为行级导航，复用chevronRight，不改真实预览动作的眼睛图标。原型资源查询版本同步更新，便于已打开页面刷新获取新交互。
- 新浏览器检查 `check-feedback.mjs` 明确覆盖home及workspace、1440/390/320、标题/说明/状态/上下右留白/箭头、原生Enter/Space及禁用。使用window捕获统计实际点击，避免现有document处理器的stopImmediatePropagation影响计数；同文档hash切页时移除旧测试监听器后再装，防止测试自身重复计数。不向产品增加点击处理。
- 原型回归、产品增量和测试结果随后续记；未部署。

### 截图反馈补正结果
- 先完成原型两页面真实Chromium回归：**57项通过**，1440/390/320，所有点位均命中原生行入口并只触发一次精确ref；资料箭头为chevronRight，Enter/Space、禁用及无横向溢出通过，0未捕获JS异常。截图 `feedback-home-*.png` / `feedback-workspace-*.png`，已核看两张390图；结果 `feedback-results.json`。这是离线原型验证，不是生产验收。
- 原型通过后同步本地产品：PersonalWorkspace将行尾“查看”视觉替换为右箭头SVG，保留含文件名aria-label；HallOverview显式把行入口置为static，补全整行focus/hover，原事项信息展开独立。没有复制业务认证、授权或变更API/Runtime合同。
- 两个既有轻量组件suite **35 passing**，日志 `feedback-component-tests.log`。SVG只做属性换行格式化后，再对最终源码运行两项新增/受影响定向测试，结果见 `feedback-final-targeted.log`；不复用旧源码作为Flow证据。
- `node --check` 和定向 `git diff --check` 通过。ESLint未全通过，仍有两个文件的既有属性换行/缩进/未使用变量问题（本轮不作全文件格式清理），日志 `feedback-lint.log`；不声称lint通过。
- 请求在用户当前转发地址 `localhost:61274` 用新的查询参数重新打开办事原型，工具状态queued；不把请求打开当作用户浏览器已完成加载的证明。
- 保留其他工作区改动，未提交/合入/Flow验证/生产安装。最终变更文件字节摘要见 `feedback-source-sha256.txt`。

### 原型预览服务恢复（2026-11-01）
用户反馈页面打不开：只读检查确认18786无监听，原静态预览进程已退出。未改页面/业务服务；用独立会话后台启动同一serve-preview.py，端口仍为18786，日志写入本任务 `preview-server.log`。重启后index、交互CSS、语义控件JS均HTTP200。重新通过open_in_codex请求打开源端18786地址，由应用处理转发，不复用桌面临时61274作为固定地址；工具返回queued，未据此声称用户浏览器已加载成功。

## 产品实施与集成（2026-11-01，用户“好，实施吧”授权）

### 固定范围、隔离理由和候选
- Owner：当前聊天；仅Web列表交互，无API/Runtime合同变化。用户已确认原型，继续保留原型及57项离线浏览器证据；未把原型通过当作产品正式验收。
- 原Web工作区位于旧基线且有大量重叠未提交内容，不能安全checkout/rebase或整文件搬运。为这次集成仅创建一个隔离worktree `/home/isp/wsps/worktrees/juyiting-list-click-web-20261101`，基于只读核对远端develop的 `04c5240018eb4402194c84eb64f03e2f02192cbc`，不携带旧分支独有提交或无关脏改动。
- 端点当前版本已经包含共享 `hall-row-link`、右箭头及可访问标签；保留这些现行约定，仅补全整行命中、focus/hover和独立事项信息展开。不重复替换成旧界面文本/图标，不改既有响应式布局。
- 候选/远端develop：`de927e16edb24943b285e74435570202bc6df2ea`；tree `167a1516d1d55c934999e089da83b029edfacf14`；版本 `1.16.84`。2026-11-01 21:16后push，随后的只读ls-remote核对一致。六个提交文件：两个组件、对应两个测试、package.json/package-lock.json。
- 原工作区及唯一原型的其他未提交内容均保留，没有全量暂存/覆盖；本轮没有将尚未归属清晰的原型其他改动夹带进产品提交。

### 轻量验证
- 当前develop集成候选的两个既有组件suite **41 passing**，`integration-component-tests.log`；包含新增整行入口结构、精确资料ID单次选择、禁用/loading-detail、事项信息独立操作。
- `git diff --check`通过。只复用现有node_modules做定向诊断，未在本机生产构建、全量测试或打包；没有宣称历史lint问题已修复。

### Flow正式验证及实际失败
- 实时读回配置：`flow-config.json`/`flow-safety.json`，canonical SHA-256 `98e50315734c7b25c7d01be457e660fc8d71935c6e240915855a5680facdfa73`。源develop、`triggerEvents: []`、测试作业timeout9分钟、只测试/构建/上传和代码扫描；无主机部署步骤。未改云端配置、未安装生产。
- 现有flow-control的start CLI对超过100项历史直接拒绝，未调用这个已知会拒绝的CLI路径。任务级脚本 `start-flow.cjs` 只补全SDK历史分页，再调用原导出的 `commandStart`；完整历史、配置hash、精确来源、单次写及readback校验均保留，不伪造CI身份，不丢弃旧Run。一次启动请求，`flow-start-attempt.json` 防重复；没有重发。
- 真实Run：**4403172 / 390**。开始后INIT尚未返回commit时原控制器正确记录UNKNOWN；随后只读`flow-390-status.json`确认来源为develop及完整候选SHA，最终 **FAIL**。代码扫描作业547145482 SUCCESS；测试/构建作业547145481 FAIL。
- 构建日志确认已克隆精确候选，随后自定义环境执行步骤21:19:15返回BUILD ERROR，未出现实际 `CYF_FLOW_PHASE runtime.begin`、npm测试或Vite构建输出。**明确根因尚未获得**，不能认定产品测试失败或断言具体云端故障。日志中的脚本文本是环境变量回显，不是执行成功证据。已保存脱敏 `flow-390-build-log-full.json`，没有盲重试、没有取消他人Run。
- 本Run很快失败，在600秒内结束；未产出经核验制品，正式测试/构建尚未通过，未生产部署/验收。原型57项和本机41项只按各自范围报告。

### 收口与下一步
- 产品实现已提交并合入远端develop；正式云端验证受构建步骤失败阻塞，下一步应先获得自定义环境步骤的明确错误，再决定修复/重试，不重复付费盲跑。
- 必要源码已在远端提交，本任务临时worktree在保存证据后清理；原脏工作区、其他任务worktree、预览服务和生产状态不动。根仓gitlink不借本次失败验证强制切换。
- 耗时未独立计量，留空；开发集成完成与云端验证失败分别记录。

## 后续原型请求：待确认承办去除所属筛选（2026-11-01）
- 用户截图要求仅优化原型：事项详情待确认承办选择Agent时，不需要“全部 / 我的 / 外部”过滤。Owner仍为本聊天；不延伸为产品实施、流水线修复或生产发布。
- 默认复用唯一原型及当前脏工作区，无新增worktree。Web本地HEAD仍为ca22ac29de657971b12a71f3a99d2d9ecfc67c1c（旧产品基线），本轮不查询/宣称远端最新；原型含前序独立增量，以任务前后文件摘要绑定，不冒充HEAD原型字节。
- `external-commission.js`删除所属筛选控件、过滤计算和事件；直接列举现有commissionEligible的全部候选，忽略历史commissionFilter。保留归属标签、准入、排序、当前选择、独立确认及资料说明。
- `assignee-recommendation.js`的另选承办演示同步去除筛选状态/控件/事件，保留逐人推荐、等待禁用、空候选和显式确认。index仅更新两脚本缓存参数；规格同步既有prototype-spec与优化方案。不改产品src/API/Runtime，不清理其他任务未提交改动。
- 现有预览18786复用、入口及脚本HTTP200；使用已有CDP harness真实Chromium检查默认详情及推荐演示，覆盖1440/390/320共6组：无筛选、本人及开放外部均显示、关闭接单的外部不出现、旧筛选不生效、切换当前候选不派单、等待禁用、空候选禁止确认、详情无横向溢出。0未捕获JS异常。390px截图人工核看通过。
- 证据 `docs/implementation/evidence/juyiting-assignee-no-filter-20261101/`：before-sha256.json、source-sha256.json、check-prototype.mjs、results.json、detail-*.png。node --check及定向diff --check通过；只是原型验证，不是产品/真实后端验收。
- 通过open_in_codex请求打开带新缓存参数的原型详情，返回queued；不声称用户浏览器已加载。未提交、未构建/部署产品。

## 原型后续：事项按承接Agent筛选及“待承办”（2026-11-02）
- 用户连续两项请求：事项列表筛选不要按技能，按实际承接Agent；原“待确认承办”统一显示“待承办”。Owner当前聊天，仅唯一原型，不扩到产品/API/Runtime或云效故障修复。
- 复用原脏工作区，无worktree/构建/发布。Web本地HEAD仍ca22ac29de657971b12a71f3a99d2d9ecfc67c1c，原型为独立未提交增量；不查询或宣称远端/生产最新。精确前后字节见 `docs/implementation/evidence/juyiting-task-agent-filter-20261102/{before-sha256,source-sha256}.json`。
- 原型interaction-completion在事项列表按实际ctx.agent.id生成全部承接Agent下拉选项，字符串ID去重/匹配，支持数字0；不按姓名或技能匹配。名称/编号、状态与Agent组合，清除筛选复位；历史taskAbility不再参与筛选。全部条件保留未承办事项，推荐人不算实际承接人。
- 原型prototype.js、interaction-completion.js、assignee-recommendation.js统一面向用户的“待承办”命名，保留一处旧状态筛选值兼容映射（不显示旧标签），不改确认后才交办的语义。index更新上述三份资源缓存参数。既有规格和优化方案同步新目标，不改写历史发布事实。
- 预览18786复用，HTTP200；node --check与定向diff --check通过。浏览器检查复用现有CDP harness、1440/390/320，证据同目录check-prototype.mjs、results.json、tasks-*.png；390图已核看。覆盖精确Agent ID、同名不同ID、数字0/字符串0去重、技能不再过滤、搜索/状态联动、刷新保留、清除、未承办可见、旧标签迁移、列表/详情/概览/推荐演示新名称及确认前不派单。初次检查最后错误要求推荐演示默认展开候选，实际已有收起规则；修正测试为等待推荐区域，不改产品/原型展开策略。
- 以上仅离线原型验证，非产品或真实账号API验收；不提交夹带其他脏改动，不重跑Flow、不安装生产。最终浏览器结果见results.json；若无该文件不作通过结论。
- 最终浏览器结果：1440/390/320三组全通过、推荐演示新名称通过、0未捕获JS异常，results.json已落盘。检查脚本两次等待失败均为对推荐READY展示的错误假设：候选默认收起，推荐状态卡仅LOADING/ERROR/STALE出现；读回实际源码后使用始终存在的data-model-confirm作就绪条件，不修改既有简洁展示规则。此处补正上述“等待推荐区域”的中间记录。通过open_in_codex请求打开新原型事项地址，返回queued，不当作用户端已加载证明。

## 产品实施：承接Agent筛选 / 待承办（2026-11-02）
- 用户“开始实施”授权；Owner当前聊天。范围：Web筛选/文案，API新增可选assignedAgentId并在分页前统一筛选列表/total/状态计数；不改Runtime、不部署、不迁移数据库。候选所属过滤在当前产品已不存在，保留。
- 主工作区旧且有重叠脏修改，仅本任务两份最小隔离worktree：`/home/isp/wsps/worktrees/task-agent-filter-web-20261102`（base5470363fc33d7689890763a54eb0ee23ac8d84d2）、`/home/isp/wsps/worktrees/task-agent-filter-api-20261102`（base8ad42be7815e499077c6a97439f0f13c96c7650e）；branch均codex/task-agent-filter-20261102。基线已fetch/ls-remote核对，不覆盖原工作区。
- 公共接口规范：API候选docs/interface-standard.md v1.2（主脏工作区更新单独保留）；本次只加业务查询字段，不改变信封/身份来源。责任：公共持久化查询负责筛选，业务服务复用认证scope；Web不本地过滤30条冒充全量。
- 已确认原型及证据沿用上节；最早验证Web toolbar/useHallData定向suite，API mapper SQL绑定及service转发回归在Flow。实现/合入/正式验证/线上分别报告。

### 产品实现、轻量验证与develop集成
- 当前规则入口实际为主工作区 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4，SHA256 `2d36ffac1dc52c6db8d54b860695edd845b6688ea0808528c53218e39aec7a08`；前节v1.2只描述候选仓内旧文档，不替代当前规范。本次新增可选查询字段，保留原信封、认证、owner scope及phase枚举；不夹带公共文档其他未提交修订。
- API `90901b55ae9b8134a701ee9b515e846b6cb9b482` / tree `82a15e4833a7c68ede26e8ea35712dbb7987bb4b`，starter1.1.16-SNAPSHOT；Web `339f3be8af09e09ba46e0b29a8e68d8fc30d8576` / tree `7781527722e3923d5648ef25436f722e9ec40d02`，1.16.91。均已非强制push到develop并ls-remote核对，原主工作区未切换/覆盖。
- API列表total、普通/资金页及状态计数共用可选assignedAgentId谓词，成员记录权威（排除left/rejected，不回退旧主承接人），无成员才兼容标量/JSON数组/CSV。SQL参数绑定/精确ID/原scope/分页前筛选；旧ability参数为其他调用方保留。补service/DAO定向回归，并复用现有TaskLinkedMaterialReaderMySqlTest隔离MySQL fixture验证真实SQL，包含35条前置干扰任务、翻页/计数一致、大小写、退出/拒绝及跨scope成员；未在本机运行Gradle。
- Web替换全部真实props/v-model/mock接口，不再发ability；按ID传assignedAgentId到列表/计数。选项复用未被名册状态过滤的roster及当前会话已读取的真实历史/外部承接者，保留已选项，不把推荐人当承接事实；非全量历史承接者目录。身份/授权代际变化清选项和筛选，忽略旧列表/计数/名册响应。
- 本机轻量：初次五个suite153 passing；增加三项筛选回归后toolbar/hall-data26 passing，最后hall-data/状态/文案28 passing。前述结果覆盖范围不相加冒充全量；日志 `docs/implementation/evidence/juyiting-task-agent-product-20261102/`。diff --check/node --check通过；ESLint三个既有问题（空行及两个response未使用），不宣称lint通过、不做无关清理。
- 实时Flow配置两端均triggerEvents[]，仅worker测试/构建/上传，无主机部署。Web canonical SHA `0e738b29638713e653a0b3114329adb95c332d23b901237b17d16258bf2313eb`；API `a3c41b0195a62f9d226f77e07d992baee358863afa209939d771c52c06d307ad`。先前Web390失败不复用为证据；现有后续401等成功，当前候选单次验证另记。
- API已单次启动Run440，返回INIT暂缺source时按UNKNOWN记录，没有重发。任务级分页适配复用原控制器；仅本任务返回Run的总时限watchdog，核实source后才可受控结束，保留600秒内传输余量，不取消他人Run。正式结果尚待。

### 首轮Flow结果与已定位修正
- API440 / Web402均FAIL，均在600秒内结束；source随后读回与各自固定SHA一致。没有制品/生产安装。source从INIT到采集完成前无commit为真实暂缺，不重发启动。
- API440根因：跨模块 `chat/jia-chat-service/src/mmdRegressionTest/.../JuyitingWorkflowMySqlTest.java` 7处Mapper查询实参漏补（前期定向扫描仅agent模块范围不足，此处补正）；已全仓git grep核对并只补这7处null，不变业务。修正提交 `aa6ecf935343caed76f6d0c657f9847025de4600` / tree `911617a8e68dc9666a9b1d24d19e30d4aea15374` 已push develop，版本不另升（同候选测试适配）。必要重验只启动新输入一轮，未盲重试旧commit。
- API440实际已运行受影响suite：AgentTaskMetaScopedDaoTest11、AgentServiceImplTest155、TaskLinkedMaterialReaderMySqlTest6，全0失败/0跳过（包含新增真实MySQL查询测试）。从同Run诊断payload解码，精确范围见api/targeted-results.json；不把局部通过或初始commit当作修正后整体Flow成功。
- Web402日志more=false，克隆耗时约120秒，随后CustomEnvironmentBuild16:02:16直接BUILD ERROR；未出现实际runtime.begin/npm test/Vite执行输出，环境回显中的脚本文本不算执行。代码扫描SUCCESS。已核实CI_COMMIT_REF_NAME/CI_COMMIT_SHA正确，尚无明确错误细节；不认定产品测试失败/不伪报通过/不盲重跑或擅改共享云端配置。

### Web402明确根因与最小配置修复
- 后续定向提取实际CustomEnvironmentBuild.with.run发现首行固定 `test "$CI_COMMIT_SHA" = 5470363...`（上一批候选），位于runtime.begin之前；本次source339f3be正确，因此被旧pin拒绝。补正“尚未获得根因”，不是npm/产品测试错误。
- 只读全分页确认Web无活动/未知Run后，备份原flow YAML；通过既有flow-control.commandUpdate **仅将该一处旧pin改为339f3be完整SHA**。不删除来源保护、不改必要测试/构建/上传/超时/triggerEvents，不改生产安装器。单次写APPLIED并readback，canonical SHA更新为 `6d1b668d2f016596418b0f37cb110e83c01feb9b6882499bda1b9a772bdaf68a`。备份/候选/diff/回执在web/flow-before.yaml、flow-candidate.yaml、config-update-result.json。恢复配置须再次核对活动Run及归属，不覆盖他人后续变更。
- 配置已修复是实写/readback事实；本次验证新Run单独记录，不把配置更新当测试通过或上线。

### 最终云端验证（2026-11-02）
- API **5260799/441 SUCCESS**，source `aa6ecf935343caed76f6d0c657f9847025de4600` / tree `911617a8e68dc9666a9b1d24d19e30d4aea15374`。实际启动记录 **08:07:38Z（北京时间16:07:38）**，08:14:11Z已读回SUCCESS，保守上界394秒（包含轮询余量），未触发取消。397个JUnit suite合计3339 tests、0 failures/errors、150 skipped；不是3339条全执行。四个直接相关suite分别11/155/6/33条，全0失败/0跳过（含真实MySQL及修正后的跨模块workflow）。validateLayering、fresh bootJar和同Run上传通过；JAR SHA256 `5b8a202fc0ffa44bcdba44e725bf13d3803b77e0e928e77656f4b94ac8e16979`，receipt SHA256 `b4d4cd874fc098f6252dfe10fafb4c51572e3fe51a62c98a12a109d0d3e71006`。
- Web **4403172/403 SUCCESS**，source `339f3be8af09e09ba46e0b29a8e68d8fc30d8576`。08:13:07Z启动，08:15:06Z已读回SUCCESS，保守上界119秒。**3672 passing / 2 pending**，Vite build、612个站点文件导出和同Run上传通过；代码扫描SUCCESS。保留Browserslist/包体大小等既有提示，不宣称无warning。
- 两端最终日志more=false。精确终态、日志、API汇总见 `docs/implementation/evidence/juyiting-task-agent-product-20261102/{api-recheck,web-recheck}/`；此前440/402仍保留FAIL事实，不重标、不作为最终制品来源。
- 本次完成产品实现、自检、develop集成及云端验证；**没有下载/安装到生产，没有重启/迁移/生产业务验收**。主脏工作区及根gitlink未切换；公共规则/其他任务修改不夹带提交。稳定知识仅定向回写既有juyiting-feature-guide筛选段落，注明源码/范围/线上未切换，其余旧基线保留。
- 最终远端只读核对及两份task-owned worktree/临时文件清理随后完成；耗时未分阶段独立计量，不作效率承诺。

- 收口确认：最终ls-remote核对两端仍为本次SHA；确认task分支为origin/develop祖先后，已移除仅本任务的两份worktree、依赖软链接和临时编辑脚本，删除已集成task分支。原工作区、其他任务worktree、唯一原型预览及生产状态不动。规则/原型、产品源码、Flow配置及验证事实分别记录完毕。

## 用户授权部署接续（2026-11-02 16:38 +08）
- 用户“部署”授权仅发布上述固定API441/aa6ecf9353与Web403/339f3be；不跟随最新develop、不新建Flow/运维Run、不本机源码构建。Owner当前聊天。
- 实时API441/Web403均SUCCESS且完整source一致；主机主动下载后全包摘要分别`5241b1ef803ce494de51d73a6593dfe36b653f0456d4f5fc5c1c2715c70fd1ff`（224040496 bytes）、`ec8672087ffc146a95789fdafda13ef34a739b3bf444b4a296e458e8643f6d05`（109685417 bytes）。流式核验API receipt/JAR/commit/tree/测试及Web全部612文件/manifest/版本/测试通过；不是本机生产打包。
- 安装前生产API439/8ad42be781，HEALTH=UP/ATTESTATION=MATCH；Web401/1.16.90。固定API候选是439祖先后的增量，未覆盖更高Run。发布锁空闲，helpers前值摘要已保存，未改其他Owner工具。
- Web旧612文件在既有deploy.lock内备份并tar compare通过：`/home/isp/baks/cyf-web-flow/20261102-task-agent-filter/`，archive SHA`51beec3cd3d96216fe0ca60239e23f19a77e006118039b653d3b6d69e24f0b8b`。API沿现行受控安装器保留备份/锁/恢复。
- API独立主机安装在途：`cyf-task-agent-api441-install.service`，KillMode=process/RemainAfterExit=yes，私有drop-in TimeoutStartSec=infinity。首次systemd-run传0被本机systemd解释成立即超时，控制器在installer日志创建前终止；保存诊断、修正本任务unit并核对生产前值后接续同制品，不重建。此unit不得按默认组杀停止，避免影响派生JVM。Web尚未切换；健康及业务验收未完成。
- 证据位于既有product evidence的`deployment/`。无生产业务写入/数据库迁移授权延伸；既有schema hook保留，预计仅等价目录核验，不实施全库CHECK或新schema方案。

### 部署完成（2026-11-02 16:52 +08）
- **安装与技术核验完成**：API441/aa6ecf935343caed76f6d0c657f9847025de4600（tree911617a8e68dc9666a9b1d24d19e30d4aea15374），starter1.1.16-SNAPSHOT；Web403/339f3be8af09e09ba46e0b29a8e68d8fc30d8576（tree7781527722e3923d5648ef25436f722e9ec40d02），1.16.91。两安装器exit0；没有新增Flow Run、重复构建或Runtime重启。
- API安装器最终PASS，PID1977282，HEALTH=UP、ARTIFACT_ATTESTATION=MATCH；JAR SHA`5b8a202fc0ffa44bcdba44e725bf13d3803b77e0e928e77656f4b94ac8e16979`。实际进程cwd/实体JAR及canonical-path回归通过。旧PID1946296已受控停止，真实冷启动存在不可用窗口；本次主机启动独立、不计入Flow时限，不加应用deadline。安装完成16:49:46，后续独立核验16:50:33。
- API旧JAR备份实体`/home/isp/baks/flow-api/20261102T083931Z-5b8a202fc0ffa44bcdba44e725bf13d3803b77e0e928e77656f4b94ac8e16979-1976100.jar`，重新计算匹配原439 JAR SHA`3e1fb1d77e471915b73c1cd540bbe08ac915c2e91dd5a4f7f989586b22e26422`；恢复须走既有受控安装流程，不自动回滚业务状态。schema hook F06两表existing_equivalent，无DDL；E05无本Run激活、not_admitted、未执行。未实施数据库迁移/CHECK清理/生产业务写入。
- Web现行record403/online_verified，612文件逐一匹配；公网入口及当前入口实际引用的JS/CSS、聚义厅懒加载资源共8项HTTP200且字节SHA一致，16:51:54确认。安装最初读到已知401旧入口缓存，既有轮询随后匹配403，最终成功；未以首个HTTP200冒充成功。旧哈希资源保留给已打开客户端。
- 安装/健康/制品/资源验证见`deployment/{api-install-result,api-installed-verification,web-install-result,web-public-resources,release-result}.json`及日志；真实登录用户的筛选、分页/计数和点击业务操作**本次生产未复测**，保留此前固定源码Flow回归证据，不宣称生产业务全量验收。
- 稳定说明仅定向更新既有feature-guide§2.4生产安装事实与验收边界，其他旧基线/脏文件/根gitlink不动。Task-owned unit保持active/exited及KillMode=process/RemainAfterExit=yes，避免停止unit影响派生JVM；不清理其他任务进程、锁、备份或worktree。

## 承接Agent选项去掉括号ID（2026-11-02）
- 用户新截图仅要求选项不显示括号内容；Owner本聊天。范围仅Web显示，不改API/筛选ID/同名去重/身份，不沿用前一批“部署”授权自动发布新候选。
- 唯一原型原已只显示姓名：先补规格/既有优化方案明确不拼接ID，再复用18786及现有CDP harness验证1440/390/320显示姓名、同名不同option value、选择按ID精确过滤；全部通过。请求打开同原型返回queued，不当用户加载成功。初次工具失败为默认Chrome wrapper指向已清理的旧二进制，指定现有可用wrapper；后续脚本全局const与原型变量冲突，改IIFE，均未改原型业务行为。证据`docs/implementation/evidence/juyiting-agent-name-only-20261102/`。
- 主Web旧基线及BountyPanel/useHallData均有重叠脏改动，不能安全复用；仅创建一个隔离worktree`/home/isp/wsps/worktrees/task-agent-name-only-web-20261102`，branch codex/task-agent-name-only-20261102，fetch核对base74d53da9962201ae59d0b0ec6eab17f771c6f409/tree18442fba6889d2617cc35d5ee4be9ffb6baabd2a。不操作其他任务worktree。
- 责任在BountyPanel option显示层：只移除`（agentId）`，value/key仍实际Agent ID。现有toolbar suite补精确名称及同名不同ID回归、选择仍发agent-b；4 passing，diff --check通过，保留既有var-dialog stub warning。版本候选1.16.96；无接口契约变化，API/Runtime不联动。本机仅轻量定向suite，未执行生产构建、Flow或上线。
- 集成结果：`d091940a22dadc670fbc954f797ba100f7a098e4` / tree`dba66595bf1ceeda9a22283fec89459d25aa10bd`（Web1.16.96）已非强制FF推送develop，ls-remote核对一致。推送前实时核对4403172全部triggerEvents为空，无自动部署；未更改云端配置、未启动Flow、未安装线上。该增量只完成源码/定向自检，不能把旧403制品当作本次正式构建或上线证据。
- 保存原型3尺寸结果、产品4项suite日志、触发条件只读结果后清理本任务最小worktree/依赖软链接及已合入task分支；不清理其他任务或旧生产备份，主工作区保持原样。初次触发条件查询脚本错误引用未安装yaml包/顶层字段，修正为现有js-yaml及source内字段后只读成功，未发写API。
