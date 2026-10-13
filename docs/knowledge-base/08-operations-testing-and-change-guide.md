# 运维、测试与变更指南

## 运行配置线索

`common:jia-common-starter` 的 `application.properties` 给出默认 profile、Hikari、Tomcat、MyBatis、PageHelper、Redis session、Jackson、Swagger/Knife4j 等共性参数。各 starter 的 `application-dev.properties` / `application-prod.properties` 补充环境值；这些值及外部环境变量才是实际运行配置来源。

前端 Vite dev server 默认 8080 并使用本地 TLS 文件；Flow 生产构建输出 `web/dist/`。构建/测试/部署策略见 [`docs/aliyun-flow-cicd-strategy.md`](../aliyun-flow-cicd-strategy.md)，部署运行细节见 [`docs/DEPLOYMENT.md`](../DEPLOYMENT.md)。

## 验证选择

| 改动范围 | 最小验证 | 补充验证 |
| --- | --- | --- |
| 根仓知识/规格 | Markdown 链接、路径、git status | 审阅子模块 SHA 是否正确 |
| Web 一般改动 | Flow Web CI-only：`npm ci`、相关测试、Vite build | 对应 Mocha/组件测试摘要与制品 SHA |
| 聚义厅 UI/逻辑 | Flow Web CI-only + 相关 `web/tests/` | 地图、遮挡、scene/SSE、public beta smoke 脚本 |
| 后端领域改动 | 本地 orchestrator：固定 commit/tree 的目标 Gradle 模块 test | `validateLayering`、`bootJar`、本地 build ID/日志与制品摘要，必要时隔离集成/数据库验证 |
| 身份、ACL、迁移、事务 | 前端 Flow / 后端本地专项测试及数据恢复计划 | Owner 自检，保留隔离 fixture、原子性及授权；不另设 Reviewer，生产动作按实际授权 |

## 变更落点速查

- 任务/Agent API：`api/agent/jia-agent-service`，契约/DTO：`api/agent/jia-agent-{api,core}`，持久化：`api/agent/jia-agent-mapper`。
- 聚义厅页面：`web/src/components/world/JuyiHall.vue`；组件：`web/src/components/juyiting/`；逻辑：`web/src/composables/juyiting/`；场景：`web/src/game/`。
- Chat stream/会话：`api/chat/jia-chat-service` 与 `web/src/composables/juyiting/useHallConversation.js`。
- 全局 HTTP/OAuth：`web/src/composables/useHttp.js`、`web/src/stores/api.js`、`api/oauth/**`。

## 更新本知识库

功能变更若影响接口、模块、数据边界或运维命令，必须同步更新对应 KB 文档。接口变化需同时更新 [`04-backend-api-index.md`](04-backend-api-index.md) 与 [`04-backend-api-inventory.md`](04-backend-api-inventory.md)；重新生成后更新 [`BASELINE.yaml`](BASELINE.yaml) 的日期、api/web SHA 和计数。应保留生成方法，避免把手工摘要与自动提取清单混淆。
