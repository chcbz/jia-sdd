# 聚义厅功能说明与持续优化指南

> 目标：把聚义厅当前功能、前后端边界、关键数据流和后续优化入口沉淀下来，避免后续迭代时重新摸索页面结构。

## 1. 功能定位

聚义厅是面向 Agent 协作的可视化调度页面，核心体验是：

- 在地图舞台上观察当前可参与协作的好汉 Agent。
- 在好汉名册中按状态查看和选择 Agent。
- 在悬赏榜中筛选任务、查看任务详情，并指派给合适 Agent。
- 在厅内传令中围绕当前 Agent 和任务发起会话，并接收实时回话。

页面入口位于：

- `web/jia-web-kit/src/components/world/JuyiHall.vue`

聚义厅相关前端组件位于：

- `web/jia-web-kit/src/components/juyiting/`
- `web/jia-web-kit/src/composables/juyiting/`
- `web/jia-web-kit/src/constants/juyiting.js`

聚义厅相关后端模块位于：

- `api/agent/`

## 2. 当前页面结构

### 2.1 JuyiHall.vue

`JuyiHall.vue` 是聚义厅的页面编排层，负责：

- 挂载地图舞台 `HallStage`。
- 管理当前选中的 `selectedAgent` 和 `selectedTask`。
- 根据 `activePanel` 打开好汉名册、悬赏榜、厅内传令三个浮层。
- 组装状态展示、任务展示、指派任务、传令草稿等页面级逻辑。
- 调用 `useHallData` 取得 Agent 和任务数据。
- 调用 `useHallConversation` 处理会话、流式消息和轮询。
- 调用 `useHallScene` 生成场景 Agent 数据，并由 melonJS 的 `HallScene`/`HallAgent` 处理地图人物渲染和巡逻移动。

### 2.2 HallStage.vue

`HallStage.vue` 是地图舞台组件，负责：

- 渲染聚义厅地图和房间热点。
- 渲染地图上的 `AgentToken`。
- 支持地图拖拽和平移复位。
- 展示地图上超出可见数量的提示入口。
- 触发打开名册、悬赏榜、传令面板等事件。

注意：地图舞台只消费 `visibleAgents`，不直接管理名册筛选。

### 2.3 AgentPanel.vue

`AgentPanel.vue` 是好汉名册浮层，负责：

- 展示名册 Agent 列表。
- 按状态触发名册筛选。
- 展示选中 Agent 的能力、状态、当前任务等详情。
- 发出 `select-agent` 和 `set-agent-filter` 事件。

名册状态切换只影响名册列表，不应改变地图上的人物。

### 2.4 BountyPanel.vue

`BountyPanel.vue` 是悬赏榜浮层，负责：

- 展示任务列表。
- 支持任务状态、能力、关键字筛选。
- 展示任务详情弹层。
- 展示推荐 Agent。
- 对推荐 Agent 发出明确的 `assign-task`、`brief-selected-task` 和 `select-agent` 事件。

任务指派的目标 Agent 由事件参数显式传入，不依赖隐藏的当前选中状态。

### 2.5 ChatPanel.vue

`ChatPanel.vue` 是厅内传令浮层，负责：

- 展示会话消息。
- 展示当前目标上下文。
- 提供命令模板入口。
- 支持提及指定 Agent。
- 发出 `send-message`、`mention-agent`、`apply-template` 等事件。

## 3. 数据与接口边界

### 3.1 前端数据分层

`useHallData` 中当前有两组 Agent 数据：

- `mapAgents`：地图专用人物列表。
- `agents`：好汉名册、推荐 Agent、能力选项等列表业务使用。

关键派生数据：

- `visibleAgents = mapAgents.slice(0, 12)`：地图最多直接展示 12 位。
- `hiddenAgentCount = mapAgents.length - visibleAgents.length`：地图隐藏人数提示。
- `filteredAgents = agents`：名册数据已由后端独立接口筛选，前端不再二次按地图数据过滤。
- `recommendedAgents`：从名册数据中筛选在线 Agent 并按任务能力匹配度排序。

### 3.2 后端接口

聚义厅使用的主要后端接口如下：

| 场景 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| 地图人物 | `GET` | `/agent/map` | 返回地图可见运行时 Agent，当前排除离线 Agent |
| 好汉名册 | `POST` | `/agent/roster` | 独立名册查询，支持 `status`、`ability`、分页 |
| Agent 详情 | `GET` | `/agent/{agentId}` | 获取单个 Agent 运行时详情 |
| Agent 状态更新 | `PUT` | `/agent/{agentId}/status` | Agent 运行时状态更新，会影响地图状态事件 |
| 悬赏搜索 | `POST` | `/agent/tasks/search` | 查询悬赏任务 |
| 指派悬赏 | `POST` | `/agent/tasks/{taskId}/assign` | 将任务指派给指定 Agent |
| 回报悬赏 | `POST` | `/agent/tasks/{taskId}/report` | 回报任务状态，并同步 Agent 运行状态 |
| 会话发送 | `POST` | `/chat/stream` | 发送聚义厅会话消息 |
| 会话事件 | `GET` | `/chat/conversation/events` | 接收会话实时事件流 |

### 3.3 重要隔离规则

名册状态切换不影响地图人物。

实现约束：

- 名册筛选必须调用 `/agent/roster`。
- 地图人物必须调用 `/agent/map`。
- 聚义厅前端不应再调用 `/agent/active`。
- `/agent/{agentId}/status` 仍然是 Agent 运行态更新接口，不能用于名册筛选。

这个规则已有契约测试覆盖：

- `web/jia-web-kit/tests/juyiting-collaboration-flow.test.js`

相关断言包括：

- `useHallData` 不包含 `'/active'`。
- `useHallData` 包含 `agentApi.get('/map'`。
- `useHallData` 包含 `agentApi.search('/roster'`。
- `visibleAgents` 来自 `mapAgents`。
- 名册面板通过 `setAgentFilter` 更新名册。

## 4. 关键用户流程

### 4.1 进入聚义厅

1. `JuyiHall.vue` mounted。
2. 调用 `refreshHall()`。
3. 并行加载：
   - `loadAgents()`：内部并行加载地图人物和名册人物。
   - `loadTasks()`：加载悬赏任务。
4. `HallStage.vue` 挂载 melonJS 场景后同步 `sceneAgents` 与 `sceneHotspots`。
5. melonJS 的 `HallAgent` 根据 `patrolRoute` 在地图上巡逻移动。
6. 启动随机台词气泡：
   - `startDialogueBubbles()`。

### 4.2 切换好汉名册状态

1. 用户在 `AgentPanel.vue` 点击状态筛选。
2. 组件发出 `set-agent-filter`。
3. `JuyiHall.vue` 调用 `setAgentFilter(status)`。
4. `useHallData` 更新 `agentFilter`，调用 `loadRosterAgents()`。
5. 前端请求 `/agent/roster`。
6. 只更新 `agents`。
7. `mapAgents` 和 `visibleAgents` 不变，地图人物不受影响。

### 4.3 选择 Agent

1. 用户点击地图上的 `AgentToken`，或点击名册里的 Agent 行。
2. `JuyiHall.vue` 调用 `selectAgent(agent)`。
3. 更新 `selectedAgent`。
4. 选中 Agent 卡片和传令上下文随之更新。

### 4.4 指派悬赏

1. 用户打开悬赏榜。
2. 选择任务，弹出任务详情。
3. 在推荐 Agent 行点击指派。
4. `BountyPanel.vue` 发出 `assign-task`，参数包含 `selectedTask` 和目标 `agent`。
5. `JuyiHall.vue` 调用 `assignTask(task, agent)`。
6. 前端请求 `/agent/tasks/{taskId}/assign`，请求体包含 `agentId`。
7. 成功后本地更新任务和目标 Agent 的状态展示。

### 4.5 厅内传令

1. 用户打开传令面板。
2. 输入消息或套用命令模板。
3. `useHallConversation` 调用 `/chat/stream`。
4. 消息 metadata 携带聚义厅上下文：
   - `scene: 'juyiting'`
   - `selectedAgentId`
   - `mentionAgentIds`
   - `selectedTaskId`
5. 前端通过 `/chat/conversation/events` 接收 Agent 回话事件。
6. 在事件中处理增量消息、完成消息和投递状态。

## 5. 状态模型

### 5.1 Agent 状态

当前前端识别的 Agent 状态：

| 状态 | 含义 | 前端展示类别 |
| --- | --- | --- |
| `online` | 在线候命 | `is-idle` |
| `busy` | 忙碌/执行中 | `is-busy` |
| `offline` | 离线 | `is-offline` |
| `error` | 异常 | `is-error` |

后端常量位于：

- `api/agent/jia-agent-core/src/main/java/cn/jia/agent/common/AgentConstants.java`

### 5.2 任务状态

当前前端识别的任务状态：

| 状态 | 含义 | 前端展示类别 |
| --- | --- | --- |
| `open` | 待接取 | `task-state-open` |
| `assigned` | 已指派 | `task-state-assigned` |
| `running` | 进行中 | `task-state-running` |
| `completed` | 已完成 | `task-state-done` |
| `failed` | 失败 | `task-state-failed` |

## 6. 代码索引

### 6.1 前端

| 文件 | 职责 |
| --- | --- |
| `web/jia-web-kit/src/components/world/JuyiHall.vue` | 页面编排、选中态、任务指派、传令模板 |
| `web/jia-web-kit/src/components/juyiting/HallStage.vue` | 地图舞台、房间热点、地图拖拽、AgentToken 列表 |
| `web/jia-web-kit/src/components/juyiting/AgentPanel.vue` | 好汉名册与 Agent 详情 |
| `web/jia-web-kit/src/components/juyiting/BountyPanel.vue` | 悬赏列表、任务详情、推荐 Agent 和指派入口 |
| `web/jia-web-kit/src/components/juyiting/ChatPanel.vue` | 厅内传令消息面板 |
| `web/jia-web-kit/src/components/juyiting/AgentToken.vue` | 地图人物头像令牌 |
| `web/jia-web-kit/src/components/juyiting/SelectedAgentCard.vue` | 当前选中 Agent 快捷卡片 |
| `web/jia-web-kit/src/composables/juyiting/useHallData.js` | 地图/名册/任务数据加载与派生状态 |
| `web/jia-web-kit/src/composables/juyiting/useHallConversation.js` | 聚义厅会话、事件流、轮询和消息归一化 |
| `web/jia-web-kit/src/composables/juyiting/useHallScene.js` | 场景 Agent、热点、反馈状态与巡逻路线生成 |
| `web/jia-web-kit/src/game/scenes/HallScene.js` | melonJS 聚义厅舞台、地图层、热点和 Agent 同步 |
| `web/jia-web-kit/src/game/entities/HallAgent.js` | melonJS 地图人物实体、动画和巡逻移动 |
| `web/jia-web-kit/src/composables/juyiting/useWaterMarginRoles.js` | 水浒人物画像和角色映射 |
| `web/jia-web-kit/src/constants/juyiting.js` | 状态筛选项和角色台词 |

### 6.2 后端

| 文件 | 职责 |
| --- | --- |
| `api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentController.java` | Agent REST API |
| `api/agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentService.java` | Agent 服务接口 |
| `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java` | Agent 业务实现 |
| `api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/AgentRuntimeDao.java` | Agent 运行态 DAO 接口 |
| `api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/AgentRuntimeDaoImpl.java` | Agent 运行态查询实现 |
| `api/agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentRosterSearchDTO.java` | 名册查询请求 DTO |
| `api/agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentRuntimeDTO.java` | 前端使用的 Agent 运行态 DTO |

### 6.3 测试

| 文件 | 关注点 |
| --- | --- |
| `web/jia-web-kit/tests/juyiting-collaboration-flow.test.js` | 聚义厅协作流程与数据隔离契约 |
| `web/jia-web-kit/tests/juyiting-component-behavior.test.js` | 子组件交互行为 |
| `web/jia-web-kit/tests/juyiting-selected-agent-card.test.js` | 选中 Agent 卡片行为 |
| `api/agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentServiceImplTest.java` | Agent 服务行为 |

## 7. 后续优化建议

### 7.1 短期优化

- 修复页面中历史编码乱码文案，优先处理 `JuyiHall.vue`、`HallStage.vue`、`BountyPanel.vue`、`ChatPanel.vue`。
- 给 `/agent/roster` 增加能力筛选入口，并在 `AgentPanel` 上提供能力筛选控件。
- 增加名册加载中、空状态、错误状态。
- 指派任务成功后重新拉取 `/agent/map` 和 `/agent/roster`，减少本地乐观更新造成的状态偏差。
- 将 `pageSize: 100` 提取为常量，避免散落在 composable 内。

### 7.2 中期优化

- 给地图人物提供更明确的位置分区，例如候命区、执行区、异常区。
- 将 `statusText`、`taskStatusText`、面板标题等文案迁移到 i18n。
- 把任务推荐逻辑从纯前端匹配升级为后端评分接口，便于纳入历史完成率、失败率、平均耗时。
- 为聚义厅会话增加“会话上下文摘要”，让用户能看到当前发令绑定了哪个 Agent 和哪项任务。
- 补充端到端测试，覆盖“名册切状态，地图人物不变”的真实 DOM 行为。

### 7.3 长期优化

- 将聚义厅升级为多 Agent 协作工作台，支持一个任务分派多个 Agent。
- 增加 Agent 事件时间线，展示上线、离线、接令、回报、异常等状态变更。
- 增加任务编排视图，支持任务依赖、阶段、子任务和回滚。
- 引入实时状态订阅，让 `/agent/map` 和 `/agent/roster` 的更新从手动刷新改为事件驱动。
- 建立聚义厅可观测指标，如在线人数、任务吞吐、平均响应时长、失败率。

## 8. 变更守则

后续优化聚义厅时，建议遵守以下规则：

1. 地图数据和名册数据保持独立。
2. 名册筛选不得调用 `/agent/{agentId}/status` 或旧的 `/agent/active`。
3. 任务指派必须显式传入目标 Agent。
4. 会话消息必须保留 `conversationType: 'juyiting'` 和聚义厅 metadata。
5. 涉及数据边界的改动必须更新 `juyiting-collaboration-flow.test.js`。
6. 涉及后端 Agent 行为的改动必须补充或更新 `AgentServiceImplTest`。

## 9. 推荐验证命令

前端聚义厅契约测试：

```bash
cd web/jia-web-kit
npx.cmd mocha --require @babel/register --require ./tests/setup.js --timeout 10000 --reporter spec tests/juyiting-collaboration-flow.test.js
```

前端构建：

```bash
cd web/jia-web-kit
npm.cmd run build
```

后端 Agent 服务测试：

```bash
cd api
./gradlew :agent:jia-agent-service:test --tests cn.jia.agent.service.impl.AgentServiceImplTest
```

检查聚义厅是否仍引用旧 active 接口：

```bash
rg -n "/active" -S web/jia-web-kit/src api/agent --glob '!**/build/**'
```
