# CYF Knowledge Base

本目录是对现有代码的**静态逆向知识库**。它描述已在源码、构建配置、SQL 资源和运维资料中观察到的静态状态；不把设计草案或运行环境假设写成既成事实。实现细节以当前 checkout 的源码为准，知识条目对应的生成版本见 [`BASELINE.yaml`](BASELINE.yaml)。

## 最短检索路径

不要默认串行读取全部文档。先按问题选择一个入口，再用标题或关键词缩小范围：

| 问题类型 | 首选入口 | 常用关键词 |
| --- | --- | --- |
| 系统组成、模块边界、跨仓关系 | [系统总览](01-system-overview.md) | `submodule`、`领域`、`边界` |
| 构建、分支、集成交付 | [仓库、构建与交付](02-repositories-build-and-delivery.md) | `Gradle`、`npm`、`gitlink` |
| 后端分层和领域依赖 | [后端架构与领域](03-backend-architecture.md) | `service`、`mapper`、`starter` |
| Controller、HTTP/SSE 路由 | [API 快速索引](04-backend-api-index.md) | Controller 名、基础路径、领域名 |
| API 的逐方法静态清单 | [API 完整清单](04-backend-api-inventory.md) | 方法名、mapping、权限 |
| Vue、路由、store、HTTP 边界 | [前端架构](05-frontend-architecture.md) | `Vue`、`Pinia`、`useHttp` |
| 聚义厅 Agent/任务/对话/场景链路 | [聚义厅端到端](06-juyiting-end-to-end.md) | `map`、`roster`、`SSE`、`scene` |
| 数据、租户、安全和高风险边界 | [数据与安全](07-data-security-and-boundaries.md) | `JWT`、`API Key`、`schema`、`ACL` |
| 测试、运维、改动落点 | [运维测试指南](08-operations-testing-and-change-guide.md) | `build`、`test`、`deploy` |
| 文件数量和静态统计 | [静态盘点附录](appendix-static-inventory.md) | `count`、`inventory` |

## 定向检索

```bash
# 摘要知识搜索；默认跳过体积最大的 API 完整清单
./docs/knowledge-base/kb-search.sh 'agent|roster|map'

# 必要时搜索包括 API 完整清单在内的全部 Markdown
./docs/knowledge-base/kb-search.sh --all 'auto-assign|PreAuthorize'

# 只提取某个 Controller 的完整清单段落
./docs/knowledge-base/kb-search.sh --api AgentController

# 检查 root 工作树、api/web SHA 与工作树、生成索引；发现异常时返回非零
./docs/knowledge-base/kb-search.sh --freshness
```

也可直接使用 `rg -n '<关键词>' docs/knowledge-base`。查接口时先看 API 快速索引，仅在需要逐方法 mapping 或权限时读取完整清单的对应段落。

## Agent 读取约定

1. 先读本页，只加载与任务匹配的一至两个主题文件。
2. 大文件优先用 `rg`、`--api` 或行区间读取，不整库拼接到上下文。
3. 知识库只用于定位和建立当前状态假设；凡涉及实现、接口契约、行为、安全或验收结论，**无论基线是否匹配，都必须检查相关源码或运行证据**。
4. 稳定规则、目录和路由放在文档前部；日期、SHA、扫描计数等易变信息集中在 [`BASELINE.yaml`](BASELINE.yaml) 或生成清单中。
5. 先执行新鲜度检查；若落后或工作树不干净，应降低对摘要的信任，只更新受影响的知识条目，不得用摘要覆盖源码事实。
6. 不在知识库复制密钥、生产配置值或大段源码。

## Token 与缓存边界

这种布局首先降低无关上下文和检索 token：稳定入口保持短小，详细清单按需读取，易变基线与稳定说明分离。它只能**间接**提高重复前缀的一致性，不能仅靠仓库文件保证模型侧 prompt cache 命中；实际命中还取决于调用方是否保持模型、工具定义、消息顺序和静态 prompt 前缀一致，并把动态内容放在后部。

## 范围与方法

- 覆盖根协调仓、`api/` 和 `web/` 两个子模块的实现、构建、资源、静态测试/脚本入口。
- 接口清单由含 Spring MVC mapping 注解的 Controller 静态提取；动态路由、网关重写、条件 Bean 和运行时 feature flag 需以部署环境为准。
- 未执行数据库迁移、未连接生产服务、未运行广泛 Gradle 构建；本知识库不是生产配置审计或安全认证结论。
- 变更实现仍以子仓源码为准；知识库应在跨仓交付时随 submodule 指针更新。
