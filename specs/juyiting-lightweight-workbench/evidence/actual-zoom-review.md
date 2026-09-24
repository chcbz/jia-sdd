# 正式工作台 · Chromium 原生页签 200% 缩放预检

对象是 Web `8f47a1289bf501616ba234638192a5303d3155d7` 的本地 Vue `/juyiting`，**不是静态 Demo**。在全新隔离浏览器配置中由仅含 `tabs` 权限的临时 MV3 扩展调用 `chrome.tabs.setZoom(tabId, 2)`，再以 `getZoom=2`、页面 `devicePixelRatio=2`、`visualViewport.scale=1` 和 CSS 视口恰为初始视口的一半交叉验证。与先前“半尺寸 CSS 视口 + DPR2”不同，这是 Chromium **实际页签缩放**，没有靠 CSS `zoom`、设备视口模拟或 pinch scale 冒充。首次进入后的对话框入场 `translateY` 动画结束再测量，避免把动画期间 10px 视觉位移误报成底栏遮挡。

|原始浏览器视口（像素）|缩放后 CSS 视口|底栏/展开菜单与页头|空会话消息区高度|消息 28 条合成段落|输入区|
|---|---|---|---:|---|---|
|320×740|160×370|导航不越界；前三项仅图标，末项“典籍阁”保留字|62.05px|滚动高度3355 > 可视62，独立滚动|底缘≤底栏顶缘（抗小数误差 .5px）|
|390×844|195×422|同上|97.05px|3367 > 97，独立滚动|同上|
|844×390|422×195|四项均显示，短菜单内部可滚动|100px|1981 > 100，独立滚动|工作窗可纵向滚动到发送按钮，不能整窗同时呈现|
|1440×900|720×450|四项均显示|129.05px|1288 > 129，独立滚动|底缘≤底栏顶缘（抗小数误差 .5px）|

四种设置下 `document.scrollWidth <= innerWidth`；菜单末项可聚焦，对话框 `aria-labelledby` 为“厅内议事”，极窄宽度的工具条末项可横向滚动后聚焦。数据见 [`actual-zoom-fixture.json`](actual-zoom-fixture.json)，截图：[320×740](actual-zoom-320x740.png)、[844×390](actual-zoom-844x390.png)。表中原始尺寸是 Playwright **视口**像素，不以 Chrome 的 `outerWidth` 为准（headless 浏览器可对窗口外框实施最小宽度）；JSON 同时保存外框尺寸供审查。合成内容通过 DOM 临时插入，**不是用户消息**。

**七个主入口补核（同一隔离脚本/同一 Web SHA，空 API）**：在上述四种真实 200% 缩放视口中，从“全部入口”顺次进入我的事项、点将册、百宝箱、典籍阁、消息通知、厅内议事，并回到办事概览；每项均检查与原业务组件选择器对应且可见的内容容器、对话框可访问标题、`aria-modal=false`、菜单收起、窗口不越底栏且文档不横溢。典籍阁另外切至“案卷检索”页签并核查选中状态。4×6 个顶层面板和 4 次回概览均通过；原始逐项 `primarySurfaces`/`returnToOverview` 在同目录 JSON 中。缩放后 CSS 视口 160×370/195×422/422×195/720×450，每一页的 `document.scrollWidth` 均等于 `innerWidth`；被阻断的同源 API 请求每视口 GET 5、POST 6（全部浏览器内返回空 JSON），另有本机 Vite HMR WebSocket 1 条、非本地握手 0 条，未向服务发写请求。此处仅证明**导航入口、与源码类名一致的 DOM 容器显示和窄屏几何（未单独校验 Vue 组件实例身份）**，不是七个业务流程（例如搜索、交办、上传、消息确认、发送）的通过率；无权限/数据时未渲染的按钮/链接没有尺寸证据。

**复现与安全边界**：在对应 worktree 的 `web/` 执行 `npm run dev -- --host 127.0.0.1 --port 61360 --strictPort`；仓库根运行 `python specs/juyiting-lightweight-workbench/tools/check-browser-zoom.py --url https://127.0.0.1:61360 --out /tmp/cyf-zoom.json --screenshots /tmp/cyf-zoom-screens`。脚本仅接受 loopback、本地 Git SHA 必须匹配，且检查 Vite 开发页的 `/@vite/client` 注入标记；页面启动前禁止应用注册 Service Worker，并断言没有应用 SW controller（临时扩展的 worker 仍可用于调缩放）。浏览器使用临时 profile，页面注入合成 token；同源所有 XHR/fetch（包括 `/chat`、`/agent` 等）均在浏览器拦截为空 JSON，EventSource 明确中止（不以 JSON 冒充 SSE）；跨源 HTTP 资源中止，WebSocket 握手仅放行本机 Vite HMR 根路径、其余在浏览器阻断，不触达真实服务。JSON 记录每视口被拦截请求的 GET/POST 数量，未记录账号/请求体；脚本运行后删除临时扩展与浏览器 profile。上述措施约束此次本地 dev 页，**不能**把未来不同启动配置的 Vite 服务视作已经验证身份。

**仍未通过的完整验收门槛**：本机系统 headless Chromium 142 不是项目锁定的 amd64 Chrome 133；没有实体手机软键盘、刘海/安全区、真实账号长会话与选段、SSE 或候选部署。`A6` 的实际页签缩放布局在本机四视口可预检，但**整项 A6 仍未完成**；更不能由此推出 A1–A5 的业务操作均通过。

仓库根 `web` gitlink 在候选完整门禁前**刻意未 pin**；本证据随特性分支单独提交，不能误当成已纳入可复现的集成 root baseline。
