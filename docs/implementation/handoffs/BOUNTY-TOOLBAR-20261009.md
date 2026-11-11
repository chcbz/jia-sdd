# 事项表头整理与移除重复需求入口 · 2026-10-09

- 本次请求标识：BOUNTY-TOOLBAR-20261009；唯一 Owner：本聊天。局部实现/诊断记录，不作为正式 accepted 或发布状态。
- 规则入口：/home/isp/wsps/cyf/AGENTS.md、ops/orchestration/README.md、docs/sdd-workflow.md。无子 Agent。
- 目标：截图事项表头去掉“提出需求”及其专用代码；搜索、筛选、刷新紧凑同排，保留查询语义和可访问性。
- 非目标：其他创建入口、共享创建表单、身份隔离、原请求恢复、资金逻辑、后端和生产发布。
- 固定基线：web develop /home/isp/wsps/cyf/web；HEAD 5eb117fa3f7a68e9af26ea62d33e5329d603634e；tree f6f2f4bf35055b1bc88eb2d09b2d11274dd03cdf。2026-10-09 ls-remote 核对远端 develop 同 SHA；线上未查，不能混同。
- 共享工作区已有其他任务修改（含 JuyiHall.vue 和 collaboration-flow 测试）；只局部编辑，不重置、不批量提交。前一轮 AgentPanel 修复保留。
- 源码范围：BountyPanel.vue、BountyActionIcon.vue、JuyiHall.vue。删除详情之外的表头创建按钮/切换表达式、唯一 plus 图标分支及无效 start-private-draft 分支/事件绑定；其他非嵌入式草稿入口保留并重命名动作组。
- 样式根因：搜索 input/select 与 task-material-picker 被意外合在 grid-column:1/-1 的规则中，输入样式规则也被分断。拆分恢复查询/表单输入样式；表头三列 minmax(0,1fr) / minmax(0,.8fr) / 44px；统一44px控件、高度/描边/焦点与现有主题一致。
- 共享创建路径仍为 JuyiHall.openDefaultRequirementCreate → BountyPanel.openCreateRequirement，因此 showCreateForm、submitCreateTask 和原请求恢复不属于死代码，不能随按钮移除。已有测试改经真实暴露方法开启表单，保留材料、幂等、身份/迟到回执回归。
- 最早定向验证：juyiting-bounty-toolbar.test.js（工具栏控件、筛选/刷新事件、无创建按钮/副作用、共享入口、CSS）；同批加入 requirement-reference-intake、requirement-reference-integration、funded-bounty-public-contract-r7。最终56 passing。
- 追加组件定向回归：juyiting-component-behavior.test.js --grep 'emits create, multi-assign|legacy formal draft route|stale funded acknowledgement'，6 passing；collaboration-flow 的 task management case 1 passing。所有命令在 web 目录运行，涉及 TS 依赖时加 node --import tsx。
- 首轮新静态断言匹配过宽、包装组件暴露方法读取方式不正确，修正测试后通过；旧组件回归初次缺少 tsx 导致 TS 模块解析失败，改用项目现有加载器通过。一次根目录执行 tsx 无法解析依赖，改回 web 目录通过。不是产品运行故障，也未盲目重复同输入。
- Chromium：实际 BountyPanel/BountyActionIcon + JuyiHall 全量 scoped CSS，在320/390/768/1440 viewport 同排、高44px、无横向溢出、仅1个刷新按钮通过；使用合成事项，非整站/OAuth/线上验收。
- 证据：docs/implementation/evidence/bounty-toolbar-20261009/，含3份测试日志、browser.json、browser-check.cjs、preview.html、preview-390.png。
- git -C web diff --check 通过。候选仍为 dirty working tree，未登记正式 accepted evidence；未生产打包、触发 Flow、部署、重启。
- 下一步：固定干净候选后经前端 Flow 4403172 正式验证，再按版本化授权发布；当前本地实现完成与发布等待分开。
- 定位/实现/验证/等待耗时未单独测量，不作收益承诺。

## 提交推送核对（2026-10-09）

- 用户明确授权提交推送后，两轮 UI 修复合为 web develop commit `16263d2b3602830a04055edaa4ced45cf5d43a42`，tree `7b85ea07613affed9a3737fdaf7e468df9def610`；push 成功，随即 ls-remote 核对远端 develop 同 SHA。
- 共11个文件；共享 JuyiHall 的登录 token 修改与 collaboration-flow 的其他修改未暂存/未提交，原样留在工作区；其他无关改动未覆盖。
- 从暂存 tree 导出隔离候选（复用现有 node_modules）执行轻量诊断：59 + 7 = 66 passing。初次导出缺少 hall.tmx fixture，补充同 tree 文件后通过；未修改产品源码。证据：`docs/implementation/evidence/bounty-toolbar-20261009/committed-candidate-tests.log` 与 `committed-candidate-regressions.log`。
- 本次仅代码提交推送，不触发正式 Flow、生产打包或部署；不将远端提交报告为上线。根仓历史文档/证据及 gitlink 未随本次代码推送提交。下一步仍为正式前端 Flow 验证与按版本授权发布。

## 2026-10-11 独立需求页跟进（本聊天唯一 Owner）
- 目标：所有默认“提出需求”入口打开现有独立 HallDraftEditor 页面；事项列表移除创建表单、创建按钮及暴露的创建方法。非目标：不改草稿提交契约、资金/身份/幂等逻辑，不发布；原请求恢复入口保留。
- 基线：Web `/home/isp/wsps/cyf/web`，develop，本地clean HEAD `954980812ab1aa37bf05064f81acdd9edfc82db5` / tree `639a6871bfd8096af86ba3d0b5170be7c1ab8f30`（含同聊天上一项取消布局改动）；2026-10-11 本轮ls-remote返回远端develop `621b87a1b977e5c8fd0ef9cd22b068d7d0622b42`；线上未查询。根仓无关修改保留。
- 入口已读：AGENTS.md、ops/orchestration/README.md、项目地图、sdd-workflow、BountyPanel/JuyiHall/HallDraftEditor 与相关测试。
- 验收：宽屏点击顶部按钮显示独立draft浮层，返回恢复事项列表；窄屏入口同一路径；事项无创建表单/暴露创建方法；搜索、详情、原请求恢复继续可用；保持草稿离开保护。
- 最早定向验证：现有Mocha实际挂载组件、toolbar、reference-intake、funded recovery；本机低成本诊断，不代替Flow正式验证。
- 实现提交：Web develop `f96342c69b8ea007308831e2c0638aba87e60f2f` / tree `0478c148754e575911fa8de77aa06699f48b023d`。所有默认入口委托 `openPrivateDraft()`；移除Bounty内创建/草稿按钮、表单、状态、submit/expose、父事件接线与残余CSS。原普通/资金请求恢复仍可核对，不移除核心恢复与身份隔离。
- Owner本机定向检查：9个相关测试文件 **236 passing (17s)**，`targeted-r3.log`。覆盖横/竖屏×多媒体开关开/关的实际JuyiHall点击→draft浮层→返回原事项/保留搜索；原资金恢复和旧身份迟到结果、独立HallDraftEditor与草稿控制器、导航/详情均回归。最终仅清理测试中的无用Picker桩/注释，再跑intake **42 passing (1s)**，`final-intake.log`。diff check通过、组件工作区clean。以上非正式Flow验收。
- 浏览器：复用既有toolbar诊断入口，按当前源码实际编译BountyPanel/BountyActionIcon并加载JuyiHall scoped CSS；合成任务在320/390/768/1440宽度均无创建表单，筛选/刷新单排且无横向溢出。当前输出 `browser.json`、`browser-r3.log`、`preview-390.png`、`preview-1440.png`；已查看1440截图。仅组件合成场景，非整站/OAuth/线上验收，独立页跳转由上述实际挂载测试覆盖。
- 归因记录：R1测试loader只匹配旧双函数import，修为兼容当前真实import语法；R2 picker/controller测试改为直接调用时未剥离展示元数据，被原合同正确拒绝，补精确fileId/version投影后通过。原Bounty表单专属测试随删除功能更新为无表单断言，核心资金/幂等恢复和选材controller回归保留。浏览器首轮旧fixture缺少新取消helper，补真实helper；第二轮截图发现旧preview壳缺floating-panel，补正确父容器并核验宽度后R3通过，不当产品缺陷、不放宽业务断言。
- 所有证据：`docs/implementation/evidence/requirement-page-20261011/`。无push/正式Flow/版本变更/部署，线上状态未修改；本地提交仍包含上一项取消区布局。后续按明确版本固定源码→Flow4403172验证/同批制品→部署→在线核验，不以本地结果称上线。

## 2026-10-11 两项UI合并发布（用户明确授权）
- 授权：用户“都推送到develop并发布”；仅本聊天两项前端UI修改及版本号，不发布其他任务/后端/数据变更。
- 发布版本1.14.9，固定Web commit `d079c548947a24ae9d2affcb41f97bbb9108e469` / tree `b19c302211fa2e6aa572d331723ed08d998cc06f`；含9549808取消布局及f96342c独立需求页。已push develop，ls-remote同SHA；组件clean。发布前线上record为1.14.8/Flow201/621b87a，流水线最近201成功无活动Run，配置只cloud_ci且source triggerEvents为空。
- 复用原版本化前端prepare-candidate及Flow控制入口，保存实时4403172-before.yaml；固定本版commit/tree/version、原测试/构建flag与installed helper SHA，备份目录 `/home/isp/baks/cyf-web-1.14.9-20261011`；发布结束恢复本次保存的验证配置，不恢复自动部署。
- 控制面首次复制辅助脚本因系统python3.6不接受subprocess text参数失败，未写云配置/触发构建；改用universal_newlines且后续shell set -e，不盲重试相同输入。push成功单独核对，不当发布成功。
- 本批发布证据位于 `docs/implementation/evidence/requirement-page-20261011/release/`。状态以实际Flow/制品/线上回读为准。
- Flow202失败且未部署：2919 passing/2pending/4failing。根因1：本轮移除表单时误删资金展示formatMoney仍需的isCanonicalMicroAmount导入；根因2：3条旧source-contract断言仍强制保留已按需求移除的表单/选材。恢复必要import，旧表单断言改为无内嵌创建+保留资金恢复/Overview中性选材；补资金金额、撤榜CTA和事件实际挂载断言，不跳过测试/放宽金额校验。新定向65passing，修复提交 `a3bceafb53b4bea2545ad3065af058c48400605e` / tree `669d93bf781ac55aee60acfb01bff375c9601c69` 已push；版本仍1.14.9（此前未发布）。失败日志与诊断在release/；Flow202后已恢复原验证配置readback，然后以新固定候选在release-r2/继续同流水线，不重复同输入。
- **发布完成（2026-10-11 21:48 +08:00）**：Web **1.14.9** / `a3bceafb53b4bea2545ad3065af058c48400605e` / tree `669d93bf781ac55aee60acfb01bff375c9601c69`；develop远端同SHA、组件clean。Flow4403172/**203 SUCCESS**，正式2923passing/2既有pending/0fail，扫描/构建/上传/部署均成功；失败Run202不改写为成功。
- 同Run制品106609127bytes / SHA-256 `fed37f2bc977cf61ff53e0edfe1fcc1e5ab395c6df5707749d4765daed5c8182`。部署单70903004、主机组28833，一批一台Success/healthy；record状态online_verified，版本/commit/tree/归档相符，364个安装文件与manifest逐字节匹配，11公网关键JS/CSS/入口哈希匹配，/juyiting入口匹配同包index。编译产物取消区间距/等宽及移除旧表单断言通过。
- 未执行登录后的生产业务点击/创建/取消，不把组件交互测试写成线上业务实测。后端/数据库/Runtime均未修改。完整证据在release-r2/的release-summary.json、formal-test-report.json、run203-status-final.json、run203-deploy.json、online-verification.json、ui-artifact-smoke.json；同Run完整构建日志已保存more=false。
- 已按无活动Run/无配置冲突检查恢复本轮保存的CI-only配置，readback canonical SHA `390998968e302677f3be6dc525036ff352506b14e81ff56e3f29e38cb9133c10`；无source自动触发/部署阶段。生产回退入口与原index/record备份保留 `/home/isp/baks/cyf-web-1.14.9-20261011`。不改共享根仓其他任务的提交/脏文档；本聊天应用代码已全部推送Web develop。
