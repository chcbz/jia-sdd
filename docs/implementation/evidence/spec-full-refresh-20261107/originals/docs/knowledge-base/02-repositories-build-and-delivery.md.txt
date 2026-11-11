# 仓库、构建与交付

## 仓库责任

| 仓库/目录 | 责任 | 常用分支 | 根仓如何记录 |
| --- | --- | --- | --- |
| 根 `jia-sdd` | 规格、知识库、运维说明、子仓版本组合 | `master` | 正常 Git 文件 + gitlink |
| `api/` | Java 后端及 Gradle 多模块 | `develop` | submodule `api` |
| `web/` | Vue/Vite 前端与测试/地图工具 | `develop` | submodule `web` |

根 `.gitmodules` 指定两个子模块均跟踪 `develop`，但可复现交付以根提交记录的 gitlink SHA 为准，而不是远端分支的未来状态。

## 构建、测试与发布

当前规则（2026-10-08）：**前端 Flow、后端本地构建部署**，权威策略见 [`docs/aliyun-flow-cicd-strategy.md`](../aliyun-flow-cicd-strategy.md)。

- 前端复用 `4403172`：固定 `web` 发布 commit，Flow 执行扫描、测试、Vite 生产构建及同 Run 制品部署；不要求转 `master`，不运行本机生产打包或 Flow 失败后的本地回退。
- 后端在固定 `api` commit/tree 的干净源码目录或独立 worktree 本地测试、`validateLayering`、`bootJar` 和制品生成；所有 Gradle 经 `python3 ops/orchestration/cyf_orchestrator.py gradle ...`，先读最新相关 `build.gradle`。本地 build ID/日志及制品摘要是后端正式证据，不伪造 Flow Run。
- 两端 `develop` 用于集成，push/合入不自动部署。发布显式绑定版本、源码、同批制品、安装记录及在线核验；测试/构建通过不等于上线。
- 后端本地发布保留统一锁、可信制品安装、备份与恢复；生产目录 `/home/isp/hosts/cyf/api` 只安装已验证 JAR，不编译。现行 Flow 下载适配器不能直接接受本地输入，须适配验证本地制品入口，不恢复旧源码到生产脚本。
- 本机前端开发预览和轻量诊断允许；数据库集成使用隔离 fixture，不触碰生产数据。本次规则修改不触发部署或重启。

## SDD 交付顺序

1. 在根仓 `specs/<feature>/` 维护规格、设计、任务和验收。
2. 在 `api/`、`web/` 分别实现、测试、提交与推送。
3. 用两端已验证 SHA 更新根仓 submodule 指针及知识/验收证据。
4. 提交根仓，形成可重建的集成交付基线。

不要在根仓把子仓文件普通化导入；这会破坏独立历史与 submodule 语义。
