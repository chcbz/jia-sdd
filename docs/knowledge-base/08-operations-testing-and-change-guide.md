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

## 图片技能与统一接口交付的运行边界（2026-10-16）

覆盖API6116a104、Web421f628c、Runtime6a9d8d3的2026-10-15实际发布，不是新部署。整体链路见[聚义厅SDD](06-juyiting-end-to-end.md#image-skill-contract)。

- 正式工具继续使用[编排索引](../../ops/orchestration/README.md)：Web绑定Flow4403172的同Run制品，API绑定固定干净源码的本地build/log/JAR SHA；原安装器保留锁、身份、备份、制品校验、健康与业务核验。不得把本轮临时`install-after-prepare`/`finish-tested-cutover`脚本当长期部署接口或恢复已弃用的源码直发方式。
- Runtime版本化安装只替换制品及其systemd路径，实际配置使用`/home/isp/conf/cyf-agent-runtime-v1`；静态HOME位于`/home/isp/state/cyf-agent-runtime-v1/unified/agents/{角色}/codex-home`。本轮未修改Provider密钥、身份、HOME、资料ACL或费用策略。构建Python须使用已验证3.11工具链；系统python3.6无法安装固定Pillow10.4，不能为过构建而放宽锁定依赖。
- 先区分安装SUCCEEDED、目录CALLABLE、action接纳、Provider等待、RESULT_COMMITTED、可下载及内容正确六个事实。目录不可用先查认证回执、代际类型、权益和绑定，不重复购买；Provider在途不重复发新动作；下载必须比对manifest的output SHA/byteLength，不能误用result manifest的SHA。
- 已发生的失败与证据见[验收](../../specs/juyiting-skill-execution/acceptance.md)及其原字节副本索引；OCR仍失败，正式发布不等于全部验收。临时脚本清理保留可恢复备份及摘要清单，不删除原始回执或正式`ops/`工具。
