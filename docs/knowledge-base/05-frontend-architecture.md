# 前端架构与调用边界

## 技术组成

前端是 Vue 3 单页应用：Vite 构建、Vue Router 路由、Pinia 状态、Varlet UI、vue-i18n、PWA 工具链；聚义厅场景使用 MelonJS。Vite 使用 `@` 指向 `web/src`，生产构建按 `melonjs`、Vue、UI、Markdown、utilities 分 chunk，并可按环境变量启用压缩、旧浏览器构建与 bundle 分析。

## 页面与状态

- 路由定义：[`web/src/router/index.js`](../../web/src/router/index.js)。根路径重定向 `/juyiting`。
- App shell：[`web/src/App.vue`](../../web/src/App.vue)，负责 app bar、侧菜单、PWA 更新/安装提示和 `router-view`。
- Pinia stores：`api`（令牌及 OAuth 回调）、`agent`（Agent/任务数据）、`global`（UI shell）、`message`、`i18n`、`util`。
- 页面域：chat、Juyi Hall、通用任务、礼品/支付/订单、个人资料、消息、帮助、投票、短语、短链、微信公众号管理。

## HTTP 边界

[`web/src/composables/useHttp.js`](../../web/src/composables/useHttp.js) 是请求单入口：

1. `VITE_API_BASE_URL` 存在时为相对 URL 加前缀。
2. 默认 JSON 请求、超时 AbortSignal、可选流式读取。
3. 默认请求认证；从 `api` store 取 token 并发送 `Authorization: Bearer ...`。
4. HTTP 401 会清令牌并尝试一次重新取令牌/重试。
5. `createApi(basePath)` 生成 `taskApi`、`agentApi`、`chatApi` 等按根路径的门面。

开发服务器仅代理 `/api/**`（以及 OAuth/login 子路径）并剥离 `/api` 前缀；非 `/api` 的相对请求如何到达后端取决于部署反向代理或 `VITE_API_BASE_URL`。

## 游戏与聚义厅

`web/src/components/world/JuyiHall.vue` 是页面编排点；它组合数据、任务、会话、场景、声音、面板、命令队列、后端场景状态等 composable。`web/src/game/` 将场景划分为相机、输入、地图/TMX、遮挡、实体、模拟、sprite 与 debug 子域；`HallScene.js` 为核心场景之一。

角色肖像解析集中在 `useWaterMarginRoles.js`，角色元数据集中在 `constants/juyiting.js`。这两处是人物显示/名称/风格变更的稳定入口。
