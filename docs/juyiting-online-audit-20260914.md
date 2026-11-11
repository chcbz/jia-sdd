# 聚义厅线上审计 — 2026-09-14

## 范围与边界

本报告只覆盖**已经发布**的聚义厅登录入口、地图、点将册、悬赏榜、议事与招贤令。经济预览、消息中心、打赏等未发布功能不纳入本次问题清单。

审计时间：2026-09-14 13:04:28 CST。全部操作为只读：浏览器登录、页面加载、接口观察、部署与日志证据复核；未发送聊天、未创建/分配任务、未修改生产数据、未发布或重启服务。

当前线上基线：API Flow `5260799` Run `56`（commit `9fdd2e6a3a8d6e4f53ab2d26be7af1122eeca3ce`），Web Flow `4403172` Run `102`（commit `c3aa00c9dcd5a9f2b8df52cdb998ee639410f453`）。API health 为 `UP`。

## 浏览器验收

使用用户提供的授权测试账号完成真实浏览器密码登录：

1. OAuth 授权页展示用户名/密码表单；
2. 提交后回到 `/oauth2/callback`，`/oauth2/token` 返回 200；
3. `/user/my` 返回 200，浏览器取得登录令牌且 OAuth transaction 被消费；
4. 回到 `/juyiting`，地图 Canvas、地图数据、场景 snapshot/events 均加载成功；页面没有可见错误提示。

因此，**账号密码登录与已登录后的聚义厅主厅当前可用**。本次测试未输出或保存账号密码、访问令牌、授权码或会话内容。

## 已确认问题（仅聚义厅）

### P1：未登录直接进入聚义厅不能稳定跳到登录页

在无登录态浏览器直接打开 `/juyiting` 时，页面发起受保护数据加载后记录 `Authentication is required`，而不是稳定地转到 OAuth 登录页；页面会处于空白/不可用状态。该现象与此前微信小程序“未自动跳转、只提示 Failed to fetch”的用户反馈方向一致。

已登录后主厅可正常打开，故问题位于未认证入口的跳转/并发加载时序，而非密码表单或 OAuth token exchange。本项应优先修复为：第一次发现无令牌即开始一次登录跳转，并使其他并发请求等待或安静退出；不得把认证失败包装成网络失败，也不得增加任意性能拒绝阈值。

### P1：部分历史议事会话可列出但不能打开

线上真实请求已记录为 `POST /chat/conversation/list` 返回 200，随后 `GET /chat/conversation/content` 返回 404；服务日志说明该会话消息中存在不属于已认证 owner scope 的行。前端会把此类错误显示为“这段旧话暂不可取，请重试”。

现有拒绝策略不能弱化：消息读取必须保持 tenant/client/conversation 的精确归属校验。根因候选是历史消息写入/迁移链路仍可产生无 scope 或错 scope 行；当前通用 `ChatMessageDaoImpl.findByConversationId` 仍仅按 `conversation_id` 查询，说明必须沿历史写入、迁移和内存同步链路做受控 fixture 复现，确认行来源后再做最小修复。

### P1：招贤令目录存在运行时 scope 异常

`GET /agent/personas/catalog` 可返回 HTTP 200，但线上应用日志反复记录 `AGENT_FORBIDDEN: Persona catalog runtime escaped the byte-exact requested scope`。这会让前端将目录清空，并显示“招贤令暂无法读取”；点将册、地图和悬赏数据不受此问题直接阻断。

目录投影中，绑定记录、身份注册与 runtime 三者需要保持同一 client/owner/agent 的精确关联；当前 `toCatalogDTO` 先以 binding/identity 确认后再读取 runtime，故应以受控 fixture 检查 runtime 查询及投影字段的一致性。不得以忽略 scope 校验来“修复”目录显示。

## 已验证可用的已发布能力

- 密码 OAuth 登录、token exchange、`/user/my`；
- 聚义厅地图与主厅 Canvas；
- `/agent/map`；
- `/agent/scenes/juyiting-main/snapshot`；
- `/agent/scenes/juyiting-main/events`。

## 建议修复顺序

1. 修复未登录进入 `/juyiting` 的单次 OAuth 跳转，增加对应前端回归用例；
2. 用受控 fixture 定位历史会话的错 scope 消息来源，修复数据/写入路径而不放宽 owner scope；
3. 用受控 fixture 定位招贤令 binding、identity、runtime 投影的不一致来源；
4. 将最小改动合入 `develop` 后，以相应 API/Web Flow 的同 Run 测试、制品和线上浏览器复测作为发布证据。
