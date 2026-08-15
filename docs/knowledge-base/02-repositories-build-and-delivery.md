# 仓库、构建与交付

## 仓库责任

| 仓库/目录 | 责任 | 常用分支 | 根仓如何记录 |
| --- | --- | --- | --- |
| 根 `jia-sdd` | 规格、知识库、运维说明、子仓版本组合 | `master` | 正常 Git 文件 + gitlink |
| `api/` | Java 后端及 Gradle 多模块 | `develop` | submodule `api` |
| `web/` | Vue/Vite 前端与测试/地图工具 | `develop` | submodule `web` |

根 `.gitmodules` 指定两个子模块均跟踪 `develop`，但可复现交付以根提交记录的 gitlink SHA 为准，而不是远端分支的未来状态。

## 后端构建

- 根工程：[`api/settings.gradle`](../../api/settings.gradle)；公共编译和发布规则：[`api/build.gradle`](../../api/build.gradle)。
- 后端使用 Java library / Maven publishing；所有子工程启用 JUnit Platform。
- `validateLayering` 是根 Gradle 校验任务，检查 mapper 不依赖 service、API 不依赖 service、DAO 所属层等边界。
- 广泛 Gradle 命令前必须读取目标模块构建文件；本主机上每一个 Gradle 命令都需要持有 `/tmp/cyf-gradle.lock`，不得并行执行。

示例（按目标模块调整）：

```bash
flock /tmp/cyf-gradle.lock bash -lc 'cd api && ./gradlew validateLayering'
flock /tmp/cyf-gradle.lock bash -lc 'cd api && ./gradlew :agent:jia-agent-service:test'
```

## 前端构建

- Node 要求：`>=18.19.0`；npm 要求：`>=9.0.0`（见 [`web/package.json`](../../web/package.json)）。
- 开发：`cd web && npm run dev -- --host 0.0.0.0`
- 生产构建：`cd web && npm run build`
- 默认单元测试：`cd web && npm run test`
- 聚义厅另有地图、sprite、遮挡、SSE/公开 Beta smoke 等定向脚本，脚本清单以 `web/package.json` 为准。

## SDD 交付顺序

1. 在根仓 `specs/<feature>/` 维护规格、设计、任务和验收。
2. 在 `api/`、`web/` 分别实现、测试、提交与推送。
3. 用两端已验证 SHA 更新根仓 submodule 指针及知识/验收证据。
4. 提交根仓，形成可重建的集成交付基线。

不要在根仓把子仓文件普通化导入；这会破坏独立历史与 submodule 语义。
