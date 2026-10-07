# 典籍阁 Agent 任职与内容维护：开发与恢复运维

## 状态与授权

源码与验证状态以 `../specs/archive-agent-maintenance/integration.yaml` 为准。2026-10-07原D2源码与文档已收口，所有局部源码包已独立接受；最终生命周期candidate5为API a0e42a / Client b3f72d，Client Linux104/104PASS、Chat同树76PASS、Agent55PASS+17Windows环境FAIL明确保留。组件提交完成，完整远程交付与服务端全面验证按下列顺序进行。源码接受不代表84项业务验收、生产部署或真实典籍上架通过。

开发交付顺序见 `../specs/archive-agent-maintenance/delivery-order.md`：完整源码与文档 → 必要定向自检/独立只读源码审查 → API/Web/Client 普通 push 并核对远程 SHA → Root 更新 gitlinks/Client pin 后 push → 服务端开发环境全面验证。不要合并 master/develop 或 force-push。生产部署、生产数据库迁移、真实任职/激活/上架和付费调用均需另行授权。

## 配置与入口

- API 内容管理：`/archive/admin/v1`，权限来自当前认证管理者，不接受表单传入 owner/client/runtime 授权。
- Native 执行：`/internal/archive/v1/jobs/{jobId}/runs/{runId}`，身份来自认证注册与当前 run/epoch，不使用用户 JWT。
- `archive.maintenance.execution-enabled` 默认 false；平台安装/目录由 `agent.platform-skills.enabled` 独立控制。
- Client `AGENT_PLATFORM_SKILL_INSTALL_ENABLED`、`AGENT_ARCHIVE_MAINTENANCE_ENABLED` 默认关闭。能力集合与安装/任职/发布授权是不同事实。
- `archive.maintenance.manager-grants` 的 collection/tenant/client/owner/permissions/authorizationRevision 必须匹配显式授权；不能靠角色名字或前端按钮授予权限。启用或改授权属于另行授权的操作。
- 批准技能包 `archive-maintainer@1.0.0` 固定 40563 bytes、SHA256 `8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081`；不能为迁就 Client 自行重打包改摘要。

## 管理者使用流程

1. 典籍阁管理面板读取当前目录与本人授权；安装、任职和撤任是独立动作，已有撤任/取消控制不能因 catalog 暂时不可用而隐藏。
2. 受控上传固定底本，登记版本、权利依据与声明 SHA256；此步骤不等于公开发布用途授权。
3. 创建明确 scope、明确目标 Agent 的维护任务。地图 Agent 与 roster Agent 不混用；不要让隐藏 selected state 决定目标。
4. 草稿按 revision 编辑，章节 sourceRanges 与原文一起保存。确定性校验只适用于 exact draftRevision，改稿后旧 validation 失效。
5. 管理者明确发布或已明确授权的 Agent 自动发布，均需当前授权、验证摘要、workRevision 与 expectedActiveEditionId。提交后阅读核验异常应显示“发布已提交，阅读核验异常”，不能重复激活。
6. 版本下架与替代 active 是显式动作；私有资料读取权不包含公开发布权。

## 章节持久断点与重启

- 服务端不可变章节对象写入、实际回读在 DB 事务外；短事务再验权限、job scope、draft snapshot/revision 与执行 epoch 后登记引用。DTO 仅投影 blockKey/draftRevision/digest/byteLength，不返回 storageURI。
- Client checkpoint 使用独立稳定目录，绑定 canonical API origin、profile、tenant、client、owner、agent、job/run/epoch；真实进程 runtimeInstanceId 变化不能让旧断点消失，但安装 stateRoot 仍按实例隔离。
- Client 记录是恢复线索，不授予执行权。重启必须先读服务端当前事实；本地损坏、目录替换、symlink/hardlink、owner/权限异常或服务端摘要不一致时拒绝继续，不自动覆盖人类修改。
- 未确认请求保留原 operationKey 与 expected revision，先查原操作回执。新的 executionEpoch 不复用旧 key。收到畸形 202 回执属于协议错误，不当成网络丢响应去降级查询。
- 同输入同根因第二次失败阻断后，先核对受信 Runtime/安装/来源/配置的真实修复事实，或确实改变语义输入；retryable 标签、workIds 重排不能解除阻断。

## 发布 STAGING 恢复

- 同一个已验证、已封存候选逐块写入 STAGING；崩溃后按持久事实恢复，实际DB完整读回后才标 READY。STAGING/未发布候选不能被Reader当作可读版本，旧active版本持续可读。
- publication/active/work revision/job-run-grant/operation/audit/outbox在最终短事务内重查当前权限、精确revision与active CAS后原子提交，不能把已经写入章节视为已发布。
- publication-specific PENDING回执可在同一原key下由当前合法publish授权恢复；保留首次receipt authorizationRevision，另记当前授权与operationId。其他回执规则不放宽。
- 提交后的阅读核验分别保存PENDING/PASSED/FAILED及检查事实。核验异常不能回滚已提交发布或再次切active；重新查询当前operation/版本核验，而不是重新发布。

## 存储生命周期（源码已独立接受）

- 来源对象登记在维护域 durable registry，状态为PENDING/REFERENCED/DELETE_PENDING/DELETED；写入后DB回滚或过时PENDING均从登记行恢复，不从磁盘目录推断资格。最终提交携带本次reservation revision，不能借当前revision通过ABA；DELETED重试创建新sourceId/独立物理URI，旧代tombstone永久保留重扫，处理旧上传在清理后才落盘的情况，迟到删除不得触及新代。明确缺少尚未创建的父目录视为对象不存在；symlink/非目录/其他IO错误仍拒绝。
- `archive.maintenance.source-cleanup-enabled`默认false；启用后按`source-cleanup-stale-millis`（默认24小时）、`source-cleanup-batch-size`（默认32）、`source-cleanup-delay-ms`（默认60000）有界轮询。时间只用于已登记未引用对象的候选筛选，不证明对象可删；短事务CAS确认删除状态后，事务外核对exact owner scope/storage URI/digest并删除，再持久完成。
- 安装配额使用真实已验证包文件与marker字节。Client `AGENT_PLATFORM_SKILL_MAX_RETAINED_COPIES`默认2；允许一份当前安装的切换空间，默认byte预算按这三份真实包+marker字节推导，也可明确设置`AGENT_PLATFORM_SKILL_MAX_INSTALLATION_BYTES`。受保护副本超过可容纳范围时拒绝新安装，不能无凭据删旧副本。
- 仅当前成功安装的服务端回执给出`reclaimableInstallationIds`，候选先持久RECLAIMABLE fence，阻止新grant继续引用；ACTIVE/READ_ONLY grant引用受保护。Client只在exact scope内核验旧成功回执、command、marker、inode/父目录及批准包proof后回收，不回收当前或in-flight安装，不扫描其他scope。
- 目标目录已删、registry仍在的崩溃窗口，以授权此次回收的durable server receipt及候选ID完成registry清理；候选自身receipt响应丢失不额外阻断，但candidate command/result/prepared/scope/parent proof仍必验。未知对象、替换目录、缺proof或授权不可验证时保留现场，不自行推断安全。
- 服务端`reclaim_batch_json`持久绑定同一结果的有界授权批次/内部cursor，receipt重放名单不变；优先尚未fence的有效副本，再推进旧RECLAIMABLE tombstone，避免最早32项永久占满。HTTP receipt形状和32上限不变。
- command发布前崩溃：合法空registry或完整已fsync的command临时文件保留unknown，仅从成功副本计数排除，不删除、不授予执行资格。名称/scope/record/owner/权限/NOFOLLOW/nlink/inode/parent proof仍必验；异常残留保留并拒绝新安装。

## 数据库迁移与服务端验证

当前章节新增 `archive_draft_block_checkpoint`，维护域从精确前代 20 表升级为 21 表。前代测试 fixture 位于 API `chat/jia-chat-service/src/test/resources/db/archive-maintenance-schema-0d2a6e6.sql`（38408 bytes，SHA256 `b17881687dd423d15fd3f73156a991f4c176ae4c0b71f87b8d515b69790832ce`）。部分新表或 schema drift 必须 fail-closed；不得通过 drop/recreate 或宽泛 ALTER 修生产库。

章节本地必要自检为 API 77/77、Client 80/80 PASS，独立源码接受；新增 MySQL selectors仅编译，未执行。服务端完整验证须使用任务独立 checkout/隔离设施，保留其他任务 dirty 工作区与服务，所有 Gradle 命令全程持共享 `/tmp/cyf-gradle.lock`。结果同时记录 exact commit/tree、原始失败、introduced delta，不能把 fixture PASS 写成生产验收 PASS。

生命周期增加来源对象registry，维护域精确21→22表升级；前代fixture为API `chat/jia-chat-service/src/test/resources/db/archive-maintenance-schema-f7811da.sql`（Git blob LF为40311 bytes，SHA256 `f814993101130aa9185c89ccba1ba134378a2c1139c098df8fd70782f54e3e6b`；历史Windows CRLF副本40820 bytes的摘要不作为Linux Git制品摘要）。Agent平台schema以一次atomic ALTER从精确前代增加`reclaim_batch_json`和RECLAIMABLE CHECK，partial/drift拒绝。前代fixture `chat/jia-chat-service/src/test/resources/db/agent-platform-skills-schema-f7811da.sql`为原Git blob LF2775 bytes，SHA256 `c86b77b0047b772cc8d1b49cf773c6ce9568ab4dc69ba67e40b33938e9542e42`，单路径`-text`；原EOF空行保留以维持字节绑定。维护域新增`idx_archive_execution_installation`（tenant/client/owner/agent/installation/status）以支撑安装行锁后的grant当前锁定读；精确21→22迁移允许仅该索引已提交的中断点恢复，拒绝错误索引或22表缺索引。candidate5已完成必要定向自检和独立只读接受，Linux storage/MySQL实跑仍留服务端；生产迁移和清理未启用。禁止任意目录递归扫描推导安装资格，禁止按磁盘阈值清理其他任务或未核对引用的对象。
