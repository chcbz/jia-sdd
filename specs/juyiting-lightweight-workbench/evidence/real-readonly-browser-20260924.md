# 候选 Vue + 真实服务只读浏览器核对（局部，不是部署验收）

执行时间：2026-09-23 23:45 至 2026-09-24 00:02 Asia/Shanghai。候选前端 SHA `fe43ebc5bece2fd2e6e78e765cd523d9fb6001a5`，本机 HTTPS Vite `https://127.0.0.1:8890/juyiting`；Playwright 驱动本机 Chromium 142，**非** CI 固定 Chrome 133。原生生产 OAuth 从 `https://kit.chaoyoufan.cn/juyiting` 发起，授权测试身份在 `https://api.chaoyoufan.cn/login/index.html` 页面输入（密码不写入脚本、仓库、URL、截图或日志），回到 kit 后取得有效 session；认证态仅在同一浏览器进程内传入本地候选。`GET /user/my` 返回 200。未经 OAuth 的**直接**访问登录页返回 403，不能据此断言账号不可用。

## 取证边界

为使本地候选而非生产前端可读取生产服务，在 Playwright 进程中拦截候选同源 `/api/**`，按原路径转发至真实 `api.chaoyoufan.cn`，使用仅驻留进程内的授权态；**允许 GET/HEAD 和已确认的只读 POST** `/agent/roster`、`/chat/conversation/list`，其余 POST/PATCH/DELETE 等拒绝（405）；本次记录中拦截写调用 **0**。未保存 token、个人事项标题/消息正文或含账号的截图。引导“稍后”只更改该浏览器 sessionStorage，不写后端。会话和隐私状态均随临时浏览器关闭而丢弃。此代理绕过了实际候选部署的 CORS/路由，**不等于部署环境真实登录回调验收**。

## 已观测结果（不含个人数据）

|步骤|浏览器/网络证据|结论限制|
|---|---|---|
|390×844 首屏|正式 Vue `home-overview` 可见、`HallOverview` 渲染；`GET /agent/map`、`GET /agent/personas/catalog`、`POST /agent/roster`、`GET /agent/hall/overview` 均 200，实际事项已呈现|真实账号只读渲染；未提交任何事项|
|典籍阁右下入口|移动导航进入原 `LibraryPanel`，典籍阅读/案卷检索两页签可切；`GET /archive/v1/catalog` 200|未查询案卷关键词，也未增删书签/笔记|
|进入原文|`GET /archive/v1/me/progress/...`、`/archive/v1/me/bookmarks`、`/archive/v1/me/notes` 与某个章回 GET 均 200；真实 `ArchiveReader` 全屏可见，30 个正文段落节点，返回书架|仅阅读；未测试写入阅读进度/书签/笔记/选段提问|
|厅内议事|原 `ChatPanel` 顶层进入；只读 `POST /chat/conversation/list` 200。消息区高度 390×844=434.52、320×740=330.52、844×390=129.06、1440×900=492.52 CSS px；四视口 `document.documentElement.scrollWidth===innerWidth`|未发送、流式 SSE、删除/创建会话或软键盘；空/已选会话状态不能代替长真实聊天核查|
|厅中实景|概览地图卡进入原 Stage；`GET /agent/scenes/juyiting-main/snapshot` 200；Stage 和 canvas 各 1；从 Stage“办事概览”返回再入地图，比较 DOM 引用**同一 Stage**|实时模拟、声音、场所/人物点击及所有贴图像素未此轮证明；`img` 标签计数不适用于 canvas 纹理解码|

只读路由共 11 次成功（9 GET、2 只读 POST；全部 HTTP 200），未知或写 POST **0**；这验证了候选导航与真实数据读取的一部分，并推翻了“此机完全无法认证”的旧推论。严格保留：没有候选部署、没有写入型业务 E2E、没有项目固定 amd64 浏览器全量门禁，A1–A7 **尚不能整体判为通过**。下次实际部署验收仍按 `real-service-qa.md`，会话中任何令牌不得复制进版本库或报告。
