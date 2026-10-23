# 冻结契约

## Agent

映射键保持 `agentId:conversationId`；`resume` 只使用当前 profile Home 内存在的准确映射会话。无映射/无 conversationId 使用新 exec；禁止 `resume --last --all`。映射指向丢失会话时明确报错，不恢复其他会话。显式 `new` 和隔离 command workspace 的 forceNew 语义保持。识别当前 CLI thread/session 事件，避免用 Home 最新文件猜测本轮归属。不删除用户 sessions 或 session-map。

## Web/API（复用，无新增后端发布）

- 现有 `POST /chat/conversation/list` 经 chatApi.list，分页 `pageNum/pageSize/orderBy`，search 含 `conversationType=juyiting` 与当前 `conversationScopeType/conversationScopeKey`；沿用服务端认证/归属过滤和前端严格 scope 校验。
- 复用现有会话内容读取与 `GET /chat/conversation/events` 认证 SSE。
- 继续发送 `POST /chat/stream` 保留选中的 conversationId；新话头清空 ID，下次发送 forceNewConversation=true。
- 历史入口提供标题、当前选择、时间、加载/空/错误状态；不在不同用户、私聊/群聊/任务范围之间复用列表。
- 切换取消/失效化旧请求与事件回调；身份/范围变化清空历史选择，不能让迟到响应覆盖新页面。
- 保留既有 voice、reserved task-thread、发送中保护；不改变鉴权、数据库结构、WebSocket schema、事件重放版本。

## 发布

源码必须来自 versioned isp-install 与 web 独立 worktree，经独立 Sol review 与针对性测试。当前主 web checkout 落后远端且有无关未提交变更，不覆盖或直接 git pull；使用新候选制品发布需要精确 source/tree/制品哈希证据。Agent 配置/Home/队列不覆盖；只在确认空闲后由指定发布 Owner 操作目标服务。
