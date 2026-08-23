# Agent workspace capability refresh design

## Discovery contract

每次 `agent.register` 和 `agent.presence` 构建 abilities 时，调用 `discoverWorkspaceAbilities(profile)`：

1. 打开前拒绝 symlink workdir/祖先路径，打开后再以 `fstat` 的 device/inode 和 `/proc/self/fd` canonical path 核对根目录身份；
2. 以目录 descriptor 为锚点扫描工作目录根，以及 `api/backend/client/frontend/packages/server/service/services/src/ui/web` 这些项目容器的下一层；
3. 根与容器共享最多 512 个目录项；`package.json` 最多读取 8 个、单文件 64 KiB、合计 128 KiB，并使用 no-follow/non-blocking 打开和 regular-file 校验；
4. 只有发现项目 manifest 或源码扩展名时才启用推断；宽泛 home/host 目录否则返回空列表；
5. 输出固定顺序的 canonical labels，不输出原始路径、未知文件名、版本和内容。

## Recognized signals

- 项目 manifest：Git/linked worktree、Node/package、Gradle/Maven、Python、Go、Rust、Docker/Compose、CI/Make。
- 前端依赖：Vue、React、Vite、TypeScript。
- 常用模块：web/api/tests/docs/ops/infra/scripts/database/assets。
- 源码扩展：JavaScript/TypeScript/Vue/Java/Kotlin/Python/Go/Rust/C/C++/PHP/Ruby/SQL/Shell/HTML/CSS 等。

示例：

- CYF 根目录可推断 `frontend/backend/vue/java/gradle/testing/documentation` 等标签；
- 仅包含 `weather.py`、`weather.html` 的隔离目录可推断 `python/frontend`；
- `/home/isp` 这类没有项目 manifest 或直接源码标记的宽泛目录不追加标签。

## Existing protocol and scheduling

工作区标签与基础能力、Profile `abilities`/`skills`、动态 Skill 合并后继续通过现有 `abilities` 字段上报。工作区标签在 128 项协议上限中预留槽位，不会被大量 Skill 挤掉。API 无需变更，现有 `/agent/capabilities`、recommend、auto-assign 和 assignment validation 自动读取刷新后的 `agent_runtime.abilities`。

标签仅是调度 hint，不扩大文件系统、API、身份或命令执行权限。

## Compatibility and rollout

- 旧 API 可直接接收新增字符串标签。
- 客户端回滚只会停止工作区标签刷新，不影响 Skill 和基础能力。
- 部署客户端后等待两个 30 秒心跳周期，再核对生产 runtime 快照。
