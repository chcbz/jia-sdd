# CYF Knowledge Base

> 静态逆向基线：2026-08-15；根协调仓基线为生成时的工作树。
> 子仓固定版本：`a3253ef6432c4c9c1f41a6abec0b8a84d99e176e`（`api`），`b0394ed7910bcc62d09a75d69d6cc74989769479`（`web`）。

本目录是对现有代码的**静态逆向知识库**。它描述已在源代码、构建配置、SQL 资源和现有运维文档中观察到的事实；不把设计草案或运行环境假设写成既成事实。

## 阅读顺序

1. [系统总览](01-system-overview.md)
2. [仓库、构建与交付](02-repositories-build-and-delivery.md)
3. [后端架构与领域](03-backend-architecture.md)
4. [后端 HTTP/SSE 接口清单](04-backend-api-inventory.md)
5. [前端架构与调用边界](05-frontend-architecture.md)
6. [聚义厅端到端链路](06-juyiting-end-to-end.md)
7. [数据、安全与风险边界](07-data-security-and-boundaries.md)
8. [运维、测试与变更指南](08-operations-testing-and-change-guide.md)
9. [静态盘点附录](appendix-static-inventory.md)

## 范围与方法

- 覆盖根协调仓、`api/` 和 `web/` 两个子模块的实现、构建、资源、静态测试/脚本入口。
- 接口清单由所有含 Spring MVC mapping 注解的控制器静态提取；动态路由、网关重写、条件 Bean 和运行时 feature flag 需要以部署环境为准。
- 未执行数据库迁移、未连接生产服务、未运行广泛 Gradle 构建；因此本文不是生产配置审计或安全认证结论。
- 变更实现仍应以子仓源码为准；本知识库在每次跨仓交付时随 submodule 指针一起更新。
