# 验收进度（截至 2026-09-23，本地候选，**未完成**）

|编号|必须观察的结果|当前证据/状态|
|---|---|---|
|A1|直接进入 `/juyiting` 首屏工作台；地图可达，Stage 不因再次切换重建|**本地候选已观察**：只读空API浏览器四视口首屏；390×844 经工作台地图卡进入真实 Stage 后，从 Stage 的“办事概览”返回仍同一 DOM Stage 实例；`juyiting-component-behavior` 组件回归覆盖懒挂载后返回。另在授权测试账号的真实后端只读代理浏览器（详见 `evidence/real-readonly-browser-20260924.md`）看到 `/agent/map` 和实景 snapshot 200、Stage+canvas 各1且工作台→地图→工作台→地图同一实例；真实场所/人物交互、游戏事件和实际部署仍待验证。曾观察到 `drawImage` 破图：Playwright 捕获为 `/juyiting/images/occluders/east-upper-v2.png` 返回 Vite HTML 兜底（`naturalWidth=0`），服务启动时间 20:56 早于资源写入 21:39；另起同工作树的全新 Vite 服务（22:25）后 PNG 返回 `image/png`、浏览器解码为 534×425，地图 Stage+canvas 各1、来回同实例、无 pageerror。已定位为旧 dev server 静态目录缓存/热更新假象，**仅空API地图素材 smoke 可视为通过，真实场景事件仍待测**。|
|A2|桌面侧栏/手机底栏到实际模块；右下角典籍阁直达真实阅读/案卷检索|**本地候选已观察**：真实 Vue 典籍阁 `LibraryPanel` 的“典籍阅读/案卷检索”页签、桌面侧栏、手机四项底栏，手机“全部入口”在顶层议事后仍能进入百宝箱；随后借授权账号的真实后端只读代理验证目录、阅读进度/笔记/书签读取和章回 200，正文实际可见 30 段；写入和部署登录回调仍未验。|
|A3|消息区扩展并独立滚动；真实新建/历史/引用不退化；输入/底栏不相互遮挡|**布局可观察，业务待验证**：空话头消息区（1440×900 / 390×844 / 320×740 / 844×390）分别 492.52 / 434.52 / 330.52 / 129.06 CSS px；底栏实际62与overlay底距一致；元件调用仍复用原会话 API。另在实际 Vue 组件渲染内注入 28 条合成 Markdown 测试消息，四视口+720×450 证实消息独立溢出、输入区与底栏无重叠且无水平溢出（`evidence/long-chat-fixture.json`）；**这不是服务端长会话或系统软键盘验证**，授权账号下原会话列表 `/chat/conversation/list` 的只读 POST 返回 200，四视口实际组件消息高度与既有测量一致；真实发送/SSE、键盘及失败恢复仍待实测。|
|A4|正式创建未指派/30+200；私人固定版本/显式授权；消息/结果已查看/个人归档/正式验收不混同|**静态合同/针对性测试，待真实回归**：`HallDraftEditor` / `HallPrivateMark` / `FormalDeliveryList` 未替换为原型模拟；未进行实际创建、验收、文件授权等写操作。|
|A5|真实榜文、点将册、百宝箱、典籍阁、招贤令、个人中心及条件能力保留原动作/错误/权限/返回|**挂载链已核对，服务待测**：逐组核对见 `feature-integration-audit.md`，逐条 F01–F63 的静态链路和未验状态见 `functional-trace-63.md`；mock 浏览器全部顶层入口可达且请求仍命中原端点；真实账号读取概览/目录/原文/会话列表及地图快照现已走通；条件权限、协作读写与全部写流程仍未走通。|
|A6|320×740/390×844/844×390/1440×900 无横溢、焦点可用；前端构建/适用测试通过|**部分通过**：28 个本地浏览器布局采样（四视口×七表面）`document.scrollWidth=innerWidth`，见 `evidence/computed-live-fixture.json`/PNG；生产构建另采 28 份、660 条控件 CSS/aria/href 样本，当前视口内 1440px/390px 控件去重 68/56 条（`ui-control-attributes.md` 与 `evidence/computed-controls-live-fixture.json`），空数据不等于全业务状态；另 `evidence/long-chat-fixture.json` 有五视口合成消息布局复测；`npm run build` 已在新增焦点代码后重跑通过（仅提示既有超650KB chunk，生产 dist 遮挡图与 public PNG SHA256 一致）；定向 `juyiting-component-behavior` 在主机空闲后 87 passing；账号离厅/语音/协作 mock 集成 34 passing；其他历史定向 317 passing / 1 个在主机高负载下 melonJS 生命周期超时，随后空闲复验已包含在 87 passing。本次新增焦点回退用例后七份相关组件测试 144 passing / 0 failing（`--timeout 20000`，详见下方复现命令）；早前全量 `npm run test` 得 2331 passing / 47 failing（浏览器工具缺失、基线陈旧断言/桩、本机高负载超时）：其中离厅/SelectedAgentCard断言与3条协作/语音桩已更正并经定向复验；地图 E9A/E9B 浏览器解码工具 `/usr/local/bin/chromium-headless-smoke` 不在本机；查明本机为 aarch64，项目固定 Chrome 133 包为 x86-64：已从 Google 官方下载并验证压缩包 SHA256=`cec67d7e4baf84814a8602ea59aa07a669f31d95e63e935b5e7b39e5986895a2`，本机运行报 `Exec format error`，**不能靠系统 Chromium 142 冒充固定 Chrome 133 全量回归**；E13/TMX 高耗时用例也曾超时，需在项目规定的 amd64 流水线受控环境重跑。实机软键盘/安全区/200% 缩放和读屏待测。|
|A7|独立只读审查无剩余问题；Git/交付状态清楚|**独立只读审查复核完成（P2已修，仍待验收）**：`adversarial_reviewer` 无 P0/P1，提出的根页焦点回退、顶部消息/好汉 root 切换、旧 CSS 断点冲突均已修复；原型文档作用域也已澄清；独立复核旧改动 143 passing、无 P0/P1、新增阻断为零；新增菜单首次回焦后另经只读复核确认无新 P0/P1/P2。随后补上手机“全部入口”首次打开百宝箱、菜单卸载后的焦点回退：捕获常驻“全部入口”按钮作为返回目标，并新增实际 JuyiHall 挂载回归。最终只读原型审计补查仅指出 F07 行锚不实，已把 `docs/ui-workbench/feature-coverage.md` 修正到实际查榜输入行 13；该修正不改变功能覆盖判定。web 候选 `fe43ebc5` 已推送至 `cyf-web-kit` 的 `codex/juyiting-lightweight-workbench`，并以远端 `ls-remote` 核对一致；root 规格/复核文档特性分支已推送，API 未改。尚未纳入 root gitlink、未触发候选 CI、未部署或获得线上核验证据。|

## 来源与限制

- 本地演示浏览器用临时 Playwright 驱动实际 HTTPS Vite `/juyiting`（**不是静态 Demo**），`/api` 由空数据/空目录/假本地会话 token 应答，**不曾把该 token/响应写入正式前端源码、后端或提交文档**，没有调用真实创建/支付/解绑/验收。
- 先前未经 OAuth 的登录页直接 GET 为 HTTP 403、旧 Vite OAuth 代理因本机 10018 无服务出现 502。**现已纠正判断**：完整生产 OAuth 经浏览器从 kit 发起后，授权测试账号可登录且真实 `/user/my` 200；借进程内只读转发，本地候选成功读取真实厅内业务数据（证据见 `evidence/real-readonly-browser-20260924.md`）。仍无部署本候选的可用集成环境，代理成功不能代替候选同源 CORS、真实回调和写操作验收；示意空API错误文案也不能认作正式服务故障。
- **只读 Flow 状态（2026-09-23 23:19–23:21 CST）**：前端流水线 `4403172` 最近运行 `147`（2026-09-20 11:36 CST 开始）为 FAIL，来源 `develop`，运行源提交元数据为 null，构建/扫描作业均 FAIL，日志 API 返回空内容；这既不能诊断失败原因，也与未触发的 `fe43ebc5` **无关**。当前流水线源码触发过滤器 `^(develop|codex/v1-6-voice-availability-20260917)$`，不含本次特性分支；推送后 23:26 CST 再查询最新仍为 Run 147，没有候选的 amd64 全量 CI/部署。要验收须在授权的无部署 amd64 受控作业针对完整候选 SHA 执行门禁；不能用旧 Run 147 成败替代。
- 历史原型 63 条覆盖结论属于 Demo；新正式组件接入和仍需实际验证的差异分别见 `feature-integration-audit.md`、`ui-detail.md`。`docs/ui-workbench/ui-detail.md` 是原型属性详设，**实现态以本目录及 live fixture 样本为准**。验收完成前不得将 `integration.yaml` 标为 accepted；`./sddw pin` 会提前改成 integration-ready，真实服务/受控浏览器门禁通过前不要执行。Web 提交已推至非发布特性分支，但 root 的 `web` gitlink 仍保持原值。

真实服务与受控浏览器的逐项操作、证据和先决条件见 [`real-service-qa.md`](real-service-qa.md)；无部署候选全量 CI 执行检查单见 [`no-deploy-amd64-qa.md`](no-deploy-amd64-qa.md)。

## 本地复核边界与待办（2026-09-23）

- 当前 63 项是有界的**聚义厅 Demo 对比清单**；正式页每组仍挂载旧组件的路径见 `feature-integration-audit.md`，并不代表真实账户所有服务端行为已验证。后续以实际授权账户对正式/私人事项、文件版本/权限、议事 SSE、典籍章节、地图素材等逐流程取证。
- 页面外壳的 CSS 算法和断点见 `ui-detail.md`，实现态采样表见 `ui-computed-attributes.md`；实际顶层按钮/输入/链接逐项清单见 `ui-control-attributes.md`，四视口完整原始数据见 `evidence/computed-live-fixture.json` 与 `evidence/computed-controls-live-fixture.json`；旧 Demo 的 180 种控件登记只限 Demo。
- **隔离复测（2026-09-23 23:29–23:31 CST）**：只跑此前全量中的 E1 基线重定向、TMX 编辑 CLI、TMX 快照/预览三条，E1 27.48 秒通过；TMX 编辑内设 60 秒及快照/预览内设 20 秒均仍超时（测试退出码 2，原始日志 `/tmp/cyf-wb-target-tmx-e1-20260923.log`，未写入仓库）。这证明 E1 曾经的 60 秒超时受本地全量执行条件影响；TMX 两条在隔离环境仍未过，**不能简单归因“只是 Chromium 缺失”或放松断言/超时充作通过**。项目锁定的 amd64 门禁仍需重跑这三条，并区分平台性能与真实回归。
- 144 passing 是本轮七份相关组件测试单次运行结果；与早前全量运行的 2331/47 不是同一次测试批次，不可相加为全量通过。复现命令（从 `web/` 运行）：

```bash
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter dot --timeout 20000 --exit \
  tests/hall-account-navigation.test.js tests/juyiting-component-behavior.test.js \
  tests/juyiting-conversation-material-links.test.js tests/juyiting-selected-agent-card.test.js \
  tests/juyiting-task-workspace-integration.test.js tests/juyiting-ux-w01.test.js \
  tests/juyiting-voice-conversation.test.js
```

历史一次以默认 2 秒超时执行时出现 before-all 初始化超时，未计为业务断言失败。固定 Chromium 与本机架构不兼容、地图高耗时测试仍列为待受控环境复核；早前地图 pageerror 已按 A1 定位并在新实例复验消失。
