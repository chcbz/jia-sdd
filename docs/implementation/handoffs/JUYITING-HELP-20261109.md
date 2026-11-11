# JUYITING-HELP-20261109

Owner：本聊天。2026-11-09用户已确认交互原型并授权实施，随后明确授权“部署”；当前Web 1.16.134（含帮助入口卡片一致性修正）已安装并通过线上资源核验。

## 固定范围与基线
- 目标：独立帮助首页、分类与同义词检索、文章阅读/返回、原有新手引导重播、既有反馈接口、真实页面导航与必要定向回归。
- 非目标：AI客服、CMS、业务执行、API/Runtime改造、部署或真实反馈提交。
- 仓库：`/home/isp/wsps/cyf/web`，复用分支`codex/juyiting-ui-workflow`；HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c` / tree `962e513205e4805a601022285bdff557c71f37ac`。工作区有其他任务脏修改，本任务不覆盖；共享JuyiHall修改前快照在既有专题evidence/help-implementation-20261109/before。
- 开工时未查询远端；实施中已fetch并核对远端develop为`038a571a0604a2ef04041e575cd37c64f8f13a33`，原工作HEAD与其1/257分叉。为避免覆盖活动修改，只在`/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-20261109/source`建立一个干净候选，基于该develop移入本任务差异；无重复worktree。未查询当前线上，不声明已上线。原型唯一入口`web/prototypes/juyiting/index.html#help`。
- 接口规范：`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4；RB-1及2026-10-30分层：Web只导航与展示，身份/业务授权仍由现有入口/API负责。

## 责任层与验证
- 帮助内容随前端版本维护，不新增后台接口。现有Hall面板负责层级、焦点、关闭；保留现有引导记录语义。
- 反馈复用现有`kefuApi.post('/message/create', FormData)`字段合同，不自动带上会话、资料、凭据。仅真实响应成功才报告成功；失败保留草稿，未知结果不自动重放。身份变化清理草稿并隔离迟到响应。
- 最早验证：内容检索纯函数、挂载帮助/反馈组件，随后既有导航/引导回归、SFC编译与定向lint。正式测试/构建固定精确源码；本批测试/构建/打包累计600秒，安装验收不在本任务授权中。
- 状态：当前帮助入口卡片修正已随Web 1.16.134部署；72项定向测试通过、2项既有pending，613文件安装核验和256项线上资源核验通过。未做已登录业务写入验收。

## 实现与集成
- Web 1.16.130：主实现`4f344db2a8dd0ce6af8234b1cd69244c44c9a2d3`；最终导航修复`1c942b0a822392a78df582949d6a07032d0d9e0f`，tree `8048bc8d1466a91033fd064db81a19252a7ae5d6`。push结果分别见证据目录push.log/final-push.log。
- 新增`src/components/juyiting/HallHelpCenter.vue`、`src/content/hallHelp.js`及共享`src/composables/useHelpFeedback.js`。原通用HelpCenter使用同一提交适配器，避免重复合同；既有FAQ查询保持。
- 帮助是原面板栈中的二级入口，使用Hall负责的返回/焦点/层级；文章/反馈返回由组件提供back结果。跳往已有来源时restore，跳往新业务入口时打开该入口根，避免占用业务详情层级。重播引导仅临时隐藏帮助浮层、保留所有frame和草稿，复用最新引导及既有身份记录。
- 新旧基线差异只适配本任务：保留远端待办提醒文案、新引导导航显示规则及其他代码；未回退远端新增能力。
- 原活动工作区仅逆向撤销本任务差异，恢复之前JuyiHall的7增9删和其他任务修改；本任务新增旧基线文件移存证据before/moved-owned-files。没有checkout/reset旧工作区。已更新远端引用，不擅改本地旧develop分支或其他聊天工作区。

## 验证与真实失败
- 最终固定源码正式本地基线：89项，87通过、0失败、2项既有pending；Vite生产构建成功（25.672秒，内部报告23.38秒）。原生引导专项25项通过；初轮新帮助/导航/引导挂载38项通过。组件浏览器390/1440均通过，使用真实SFC及反馈适配器，身份/服务/父导航为明确离线替身，不是全站OAuth或生产验收。
- 新增内容/反馈/帮助组件及通用HelpCenter定向lint通过。旧大文件JuyiHall/HallMine整文件lint有既有风格问题（完整日志保留），没有宣称全仓lint通过或顺手全文件格式化。
- 初步整合时现有导航测试fixture未提供新增的helpReplayVisible等依赖，5项失败；同步真实fixture后通过。原始失败日志保留。
- 首个构建器执行测试及Vite成功，但依赖链接node_modules被本地.gitignore目录模式漏掉，末尾洁净检查失败。仅在干净候选.git/info/exclude补忽略，源码未改；同批第二次构建完成（53.667秒）并产生旧候选4f344db包。该包不代表最终导航修复，不能用于最终版本验收。
- 最终导航修复后再次使用原构建器；排队40.548秒、依赖22.789秒、测试8.606秒、Vite25.672秒，剩余阶段受119秒剩余预算终止；最终status为STOPPED_BEFORE_COMPLETION，不重标成功，不把前一个源码包当本候选包。

## 时限例外申请与恢复
- 同任务未重置预算：首轮含实现/等待的保守测试构建窗口480.150秒，最终阶段118.904秒，保守累计599.054秒。阶段外的实现、自检阅读、push、文档/登记时间不混入受限阶段，完整墙钟另记timing.json。
- 申请额外180秒：固定任务JUYITING-HELP-20261109、最终commit/tree如上；原因是最终收口导航问题后共享锁排队消耗40.548秒。所需工作是复核保留的测试/构建证据及依赖、完成最终打包/完整性核验，优先复用精确候选已有dist，不盲重跑已通过测试与编译。不新增部署授权。
- 用户随后明确“继续完成”，按前述额外180秒申请继续；未增加生产部署授权。首次恢复预检因系统Python3.6不支持text参数失败（0.026秒）；改用现有Python3.11后成功（16.741秒，锁等待0秒）。累计保守测试/构建/打包615.821秒，在已批准例外范围内；原失败/超时receipt保持不变。
- 原构建器流式打包已删除自有dist，不能把空dist直接重包。任务专用finish-package.py核对精确commit/tree、工具/Node/依赖完整性及原测试报告，按原manifest从中断归档恢复503个完整且摘要一致的文件，其余110个从固定源码public核对补入；无缺失编译输出。复用已通过测试/编译，不重复执行；新包613个文件逐一核验通过，包内manifest与原manifest字节相同。
- 最终包`/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-20261109/package/web.tgz`，SHA-256 `a0626f78468e60c024b0aad13cc933c87882920127df47de438ec01d6f60e292`，绑定最终1c942b0/tree8048bc8。旧4f344db包移存`/home/isp/pkgs/cyf/JUYITING-HELP-20261109-superseded/package/web.tgz`，仅历史候选，不能代替最终版本。
- 完整证据：`specs/juyiting-ui-baseline-20261006/evidence/help-implementation-20261109/`，本次结果见finish-package/result.json，迁移位置见final-artifact-locations.json；原build-final/result.json仍为STOPPED_BEFORE_COMPLETION。本次成功是恢复核验，不改写旧批次状态。包外保存日志、报告、manifest及两个集成commit补丁；完成登记与自有临时目录清理另见closeout.json。不清理共享依赖、其他任务或生产内容。

## 部署授权与兼容候选（2026-11-09）
- 用户明确“部署”，授权本功能Web发布，不涉及API/Runtime/数据操作。
- 部署前查询生产record：1.16.132/4e0c17347444dea2841426b586df5d51e450a34b，online_verified。原1.16.130包会回退已上线成果读取修复，不安装。
- fetch核对develop为af8fe8542bb0c93f0561ce4599bf8dd6829fbc0e，版本1.16.133；同时包含生产4e0c173和本任务1c942b0。相对当前生产的差异仅帮助功能及版本字段；复用现成合并，不新增业务改动。重新建立已清理的同一任务source用于固定候选验证，不额外创建平行worktree。
- 沿本任务原600秒及已批准180秒例外，前序保守累计615.821秒；此次测试/构建/打包限剩余163秒（不重置预算）。新增帮助/导航/引导及现网成果读取相关回归。安装/线上验收不消耗构建预算。结果以deploy-build/result.json为准。

### 部署结果
- 候选af8fe8542bb0c93f0561ce4599bf8dd6829fbc0e/tree95cb90b15de0c6c313329fc8220f7cf1b50b5231，Web1.16.133。原构建器72.278秒完成（锁等待0）；165项测试中163通过、2既有pending。累计保守构建688.099秒，低于原600+已批准180=780秒；无重复预算、无Flow。
- 首次安装descriptor位于组可写源码父目录，被原安装器以unsafe LOCAL parent拒绝，未进入安装。保留失败结果，将同字节descriptor移到root持有的任务目录后使用原入口重试；不修改权限保护，不重构建。
- 原受控事务43.946秒成功：613文件本地摘要核验、256个线上index/JS/CSS精确摘要验证，实际变更32个文件，record为online_verified。备份前代record摘要与descriptor一致。安装/浏览器验收耗时独立于构建预算。
- 当前包`/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-20261109/package/web-1.16.133.tgz`，SHA256 `67de6a49d3eab8e891708d6c757796d1e5fefe40dc8e23d554154173501b9820`。备份`/var/lib/cyf-web-flow/backups/5938af7db274a31f5b32e1cd024cb4389ada6635a2debe23abc8848ab4665ed4`；恢复须沿原受控安装事务，不手工复制旧index。1.16.130旧包移至`/home/isp/pkgs/cyf/JUYITING-HELP-20261109-v130/package/web.tgz`，仅历史候选。
- 真实Chromium访问生产/juyiting正确进入登录页（HTTP200，无pageerror），未使用用户凭据、未提交反馈；登录后帮助完整流程尚未线上实测。此前390/1440真实SFC离线交互证据仍保留，不冒充生产已登录验收。
- 证据位于原证据目录deployment/：build/、install.log（原拒绝）、install-retry.log、first-install-result.json、result.json、record-before/after.json、browser-smoke.json、production-entry.png。本次不改API/Runtime、不做数据库操作。最终保留登记与临时目录清理见deployment/closeout.json。

## 帮助入口样式修正（用户截图，2026-11-09）
- 目标：将“我的”中使用帮助改为与上方相同的第六张入口卡片；仅Web模板/必要回归和既有原型，不改API/Runtime或帮助业务。
- 原因：帮助放在mine-grid之外的mine-help nav，未命中既有卡片CSS，独立样式导致透明背景、字号/图标/间距不同。责任层为HallMinePage布局，复用原mine-grid规则，不新增第二套卡片样式。
- Owner本聊天；原活动web HEAD ca22ac2且有无关修改，保持不动。远端develop与生产均为af8fe8542bb0c93f0561ce4599bf8dd6829fbc0e / tree95cb90b15de0c6c313329fc8220f7cf1b50b5231 / 1.16.133。唯一干净候选`/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-CARD-20261109/source`基于该commit，非按阶段重复worktree。
- 接口规范`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4，契约不变；先更新原型mine状态及规格，再修改产品。验收：390/1440等宽高/背景/圆角/边框/字号/图标/间距及整卡点击事件保留；定向帮助/导航回归。
- 此轮测试/构建/打包600秒累计上限，记录实际源码/工具/报告和包SHA。修复完成时未扩展此前发布授权；用户随后再次明确“部署”，授权安装固定1.16.134候选。

### 样式修正结果
- 已合入Web develop `8b1b77cc0d600f67e55861b39926034cb583bf3f` / tree `d41262ba807a859f094edf92a5656d7cac4f7734`，版本1.16.134；保留1.16.133的全部生产修复，只将帮助按钮移入mine-grid并删除旧mine-help CSS。移除右箭头，help事件仍携带currentTarget用于焦点恢复；个人中心禁用状态不影响帮助。
- 原型390/1440点击及卡片计算样式一致性通过；真实SFC/scoped CSS在369/390/1440均验证卡片背景、边框、圆角、宽高、padding、间距、标题/说明/图标字号颜色一致，手机1列/PC2列，无水平溢出、无pageerror。真实SFC浏览器的图标/父事件是明确离线fixture，不是线上已登录验收。
- 正式本地基线74项：72通过、2既有pending；生产Vite及613文件完整包核验通过，最终builder57.252秒，前次失败31.638秒。首次缺本clone Git作者身份导致未提交，builder在干净源码预检0.022秒拒绝；补已有仓库身份后首轮回归发现另一行旧mine-help CSS未清，保留失败、修正后再测通过。没有使用必要测试失败的旧包。
- 最终包`/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-CARD-20261109/package/web.tgz`，SHA256 `287b036be0c88eec32bf457c1cb99688e12cc59b6dd130e1b91c73fddf980953`。推送、日志、报告、补丁、原型/组件截图及计时在`specs/juyiting-ui-baseline-20261006/evidence/help-card-20261109/`。包外证据保留后通过既有清理器登记，清理本任务source/中间目录，不动原活动web工作区或共享依赖。
- 修复合入阶段未操作生产；后续用户明确授权的1.16.134部署结果如下。

### 样式修正部署（2026-11-09）
- 用户明确“部署”，固定授权Web1.16.134 / `8b1b77cc0d600f67e55861b39926034cb583bf3f` / tree `d41262ba807a859f094edf92a5656d7cac4f7734`。部署前实查线上1.16.133/af8fe85、远端develop8b1b77c，无倒退风险；使用已验证的原包，不重新构建、不启动Flow。
- 保留身份/目录权限与原发布锁，root私有任务目录descriptor调用现有`/usr/local/sbin/cyf-web-flow-deploy --source-local`，原受控事务13.622秒成功、控制面14.179秒；record为online_verified。613个本地文件逐一摘要相符，256个线上index/JS/CSS精确摘要验证通过。
- 生产包仍为前述`package/web.tgz`，SHA256不变；原前代备份`/var/lib/cyf-web-flow/backups/b6e4e48cec434098dcfe8c8aca8989cc9f6b53db113c89175669956024db16a0`，其中record-before摘要与descriptor完全匹配。恢复沿既有受控事务，不手工覆盖index或删除新状态。未操作API/Runtime或数据库。
- 证据在`specs/juyiting-ui-baseline-20261006/evidence/help-card-20261109/deployment/`：authorization、install-descriptor、record-before/after、install.log、result.json、browser-smoke及retention。安装/线上核验与构建耗时分别记录；原构建与失败证据不重标。
- 部署后真实Chromium访问/juyiting进入正常登录页，HTTP200、无pageerror；未使用用户凭据或提交反馈，登录后卡片交互仍以先前真实SFC离线回归为边界，不冒充线上已登录验收。完成包已重新登记，未产生源码/构建临时目录，无其他任务清理。
