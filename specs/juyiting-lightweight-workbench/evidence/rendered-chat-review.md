# 厅内议事内容态复核（正式 Vue，合成数据）

对象：2026-09-24 Web `8f47a1289bf501616ba234638192a5303d3155d7`。脚本 `../tools/check-browser-zoom.py --rendered-history` 在浏览器内拦截 `/api/chat/conversation/list` 和 `/api/chat/conversation/content?id=19001`，仅返回一个**虚构公议**和 28 条虚构 Markdown 消息；真实 `ChatPanel` 通过原会话 API 路径渲染 `.hall-message`，**不直接插入 DOM**。SSE 在 fixture 中本地返回 403，不模拟发送或流式服务。按源 `web` SHA 和 loopback origin 限制，跨域 HTTP、业务 WebSocket 中止；本地 fake token、数据和临时扩展均不写入项目源码。带 `--zoom-factor 1` 测手机原始 CSS 尺寸；默认 `--zoom-factor 2` 用隔离的浏览器扩展调用 `chrome.tabs.setZoom(2)` 并读回 zoom/DPR/CSS 视口，不把 DPR 模拟当成真实缩放。

|原始视口 / 缩放|实际 CSS 视口|消息区高度 / 内容 scrollHeight (CSS px)|已渲染内容及判定|
|---|---|---:|---|
|320×740 / 100%|320×740|330.52 / 5272|28 个气泡、28 个加粗与列表、代码块及锚点；消息容器纵向独立滚动；无横溢|
|390×844 / 100%|390×844|434.52 / 5272|同上；输入区在底栏上方|
|320×740 / 200%|160×370|62.05 / 9608|同上；前三个底栏条目仅图标，末项“典籍阁”字样保留|
|390×844 / 200%|195×422|97.05 / 8527|同上；内容换行后仍有独立滚动|
|844×390 / 200%|422×195|100 / 5272|同上；整窗可纵向滚到发送按钮，不能同时看到全部内容|
|1440×900 / 200%|720×450|129.05 / 3970|同上；输入区在底栏上方|

两批结果每个视口均记录 `renderedHistoryFixtureRequests: {list:1,content:1,events:1}`；28 条 `.hall-message`、至少 28 个 `<strong>` 和 `<ul>`、一个 `<pre>`，代码块内部 `scrollWidth > clientWidth`（超出 1106–1591px），消息容器自身 `scrollWidth == clientWidth`、28 个气泡左右均未越消息内边界，页面 `scrollWidth <= innerWidth`。验证脚本也从“全部入口”核对六个业务表面、典籍“案卷检索”页签和回到概览，不等于这些业务有数据时的所有操作可用。

**可复核的具体 CSSOM（390×844，100%）**：消息区 434.515625px 高、左右各 16px 内边距；第一条用户气泡 W×H=358×205.9375px，padding=10px 12px、font-size=15px；正文 `15px/23.25px`，Markdown 示例链接 `15px/23.25px`、`rgb(127,74,34)`、下划线、underline-offset 2px；示例锚点 `href="#local-fixture"`，无 target/rel；代码块宽 334px，`overflow-x:auto`。这个 href 是脚本构造的本地片段，**不是服务端消息或可分享深链**。200%/160px CSS 视口时正文仍 15px/23.25px，气泡 144px 宽，代码块宽 120px 并自行横滚，不强制缩小聊天文字。其他视口全部字段见原始 JSON `renderedStyle`/`renderedBounds`。

脚本对记录的正文 `15px/23.25px`、链接计算颜色/下划线/offset/target/rel 和代码块 `overflow-x:auto` 增加 fail-closed 断言；增量脚本复跑 100%/200% 和不带 `--rendered-history` 的旧模式均通过，100%/200% 完整 JSON 与保存证据逐字段相等。独立只读审查先前复产六视口 JSON 与三张截图逐字节一致、无 P0/P1；指出的两项脚本断言不足已补强。

证据：[100% JSON](rendered-chat-native-fixture.json)、[200% JSON](rendered-chat-actual-zoom-fixture.json)、[390×844 100% 截图](rendered-chat-zoom1-390x844.png)、[320×740 200% 截图](rendered-chat-zoom2-320x740.png)、[844×390 200% 截图](rendered-chat-zoom2-844x390.png)。源内无真实账号/密码或实际聊天记录。

复现：以本 worktree `web/` 运行 `npm run dev -- --host 127.0.0.1 --port 61360 --strictPort`，在根目录分别运行 `python specs/juyiting-lightweight-workbench/tools/check-browser-zoom.py --url https://127.0.0.1:61360 --rendered-history --zoom-factor 1 --out /tmp/cyf-chat-native.json` 和相同命令但 `--zoom-factor 2 --out /tmp/cyf-chat-zoom.json`。需要已安装 Playwright Python 模块、系统 Chromium 和本地 Vite HTTPS；不会与线上 API 建联。浏览器为本机 Chromium 142，非项目规定的 amd64 Chrome 133；没有真机软键盘/安全区/读屏、真实长会话、发送/流式回复、固定版本引用或授权读写验证。这些仍是验收阻断，不能把合成消息的布局通过当成业务功能全量通过。
