# Agent workspace capability refresh

## Problem

客户端只根据基础能力、Profile 配置和已安装 Skill 上报 abilities，宋江无法区分 Agent 当前工作目录中已有的项目类型、技术栈和模块范围。

## Goals

- 每次注册和 presence 心跳根据 Profile `codexWorkdir` 重新识别项目能力。
- 将安全、稳定的工作区标签合并进现有 runtime abilities，直接供能力名册和宋江调度使用。
- 不上传绝对路径、任意文件名、依赖版本、文件内容或未知目录名称。
- 宽泛 home/host 目录没有项目 manifest 或源码标记时不推断项目能力。

## Non-goals

- 工作区标签不是 ACL、生产权限或可执行性证明。
- 不递归索引源代码，不构建语义代码搜索或向量库。
- 不修改 API/WebSocket schema、数据库字段或任务事务模型。

## Scope

- Client：`codex-ws-agent` 工作目录能力发现、注册/心跳快照和测试。
- API/Web：沿用现有 `abilities` 合同，无源代码变更。

## Constraints and risks

- 扫描必须有目录条目、深度和 manifest 大小上限，并拒绝 symlink workdir。
- 只输出固定 allowlist 标签，避免将客户名、仓库名或秘密文件名传播到服务端。
- 推断能力仍然只是调度 hint；API key、绑定、身份和 workspace policy 保持独立校验。
