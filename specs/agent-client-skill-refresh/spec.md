# Agent client skill refresh

## Problem

聚义厅运行时把 `agent_persona.abilities` 当成 Agent 能力事实，覆盖接入客户端上报值，导致宋江推荐和自动分配无法反映客户端当前已安装技能。

## Goal

- Persona 能力仅作旧客户端/首次注册默认值。
- 已认证并绑定的客户端在注册和心跳中上报当前能力快照。
- 宋江推荐、自动分配和手动能力校验直接使用最新 `agent_runtime.abilities`。
- Codex WebSocket 客户端自动发现 profile 对应 `CODEX_HOME` 与工作区内的 `SKILL.md`。

## Non-goals

- 能力标签不作为 ACL 或高风险操作授权。
- 不修改 Agent canonical identity、persona binding 或任务事务模型。
- 不新增数据库表或字段。
