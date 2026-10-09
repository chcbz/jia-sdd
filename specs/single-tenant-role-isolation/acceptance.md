# 验收

1. 任意已认证用户的业务 tenant 均为 `0`；用户无法提供 tenant 参数覆盖该值。
2. 同一 `(0, client_id, persona_code)` 只能有一条 active persona binding；并发申领只成功一次。
3. 非 owner 仅能看到角色“已绑定”，不能操作或重复申领，也看不到 owner、binding id、agent id、identity、runtime 或 endpoint。
4. 两个不同用户仍能各自读取和修改自己的用户资料、典籍进度、书签、手札、聊天和任务；互相读取、更新、删除均失败且不泄露资源存在性。
5. 指定重复角色迁移后：受控保留 owner 持有角色，另一 binding/identity 已退役；恰好两条任务的实时 Agent 引用都转向保留 Agent；任务 owner 与历史事件未改写。
6. 迁移/删除后生产库业务表不存在非 `0` tenant 行；可迁移行和不可迁移删除集的行数、范围哈希、唯一组检查均与迁移前快照一致。
7. Flow 对精确提交完成测试、构建、同 Run 制品和授权范围内的部署/线上 smoke；记录 run、提交、制品摘要、迁移快照摘要和读回结果。
