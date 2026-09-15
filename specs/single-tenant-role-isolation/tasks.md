# 工作项

- [ ] API：所有认证入口固定 JWT 派生 tenant 为 `0`，并保留真实 owner。
- [ ] API：用户资料、典籍/书签、聊天、任务的 owner 谓词与旧行兼容读取；补充交叉 owner 拒绝测试。
- [ ] API：Agent binding、identity、alias、runtime、hosting 的 `(0, client, owner)` 约束与无泄漏全局角色目录。
- [ ] API：任务根/子表增加 `owner_jiacn`；所有用户入口按 `(0, client, owner, task)` 授权；角色只能作为执行者。
- [ ] DB：生产只读盘点生成完整 tenant 表清单；加法 DDL、私有快照、临时 DML、读回和回滚脚本分离。受控 owner 参数不落库日志或 Git。
- [ ] DB：按用户确认的重复角色规则，退役另一 binding，并仅迁移恰好两个实时任务的 Agent 引用。
- [ ] Test：两个用户、同 client 的角色唯一性；目录不泄漏 foreign binding 信息；资料/Archive/Chat/Task 交叉 owner 拒绝；重复角色和两个任务迁移。
- [ ] Release：兼容版本 Flow、生产迁移快照/读回、严格版本 Flow、线上 smoke。
