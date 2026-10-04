# 典籍阁 Agent 任职与内容维护：开发与恢复运维

## 状态与授权

源码与验证状态以 `../specs/archive-agent-maintenance/integration.yaml` 为准，当前仍 implementing / NOT_COMPLETE。最新章节断点已本地保存和定向验证，但发布 STAGING 恢复及存储生命周期尚未收口。历史组件 PASS 不表示 Runtime 全链、84 项真实业务验收、生产部署或真实典籍上架通过。

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

## 数据库迁移与服务端验证

当前章节新增 `archive_draft_block_checkpoint`，维护域从精确前代 20 表升级为 21 表。前代测试 fixture 位于 API `chat/jia-chat-service/src/test/resources/db/archive-maintenance-schema-0d2a6e6.sql`（38408 bytes，SHA256 `b17881687dd423d15fd3f73156a991f4c176ae4c0b71f87b8d515b69790832ce`）。部分新表或 schema drift 必须 fail-closed；不得通过 drop/recreate 或宽泛 ALTER 修生产库。

章节本地必要自检为 API 77/77、Client 80/80 PASS，独立源码接受；新增 MySQL selectors仅编译，未执行。服务端完整验证须使用任务独立 checkout/隔离设施，保留其他任务 dirty 工作区与服务，所有 Gradle 命令全程持共享 `/tmp/cyf-gradle.lock`。结果同时记录 exact commit/tree、原始失败、introduced delta，不能把 fixture PASS 写成生产验收 PASS。

发布恢复与生命周期的具体配置/迁移/运维动作待本轮源码收口后补充，当前不得据本页认定其已实现或已启用。禁止任意目录递归扫描推导安装资格，禁止按磁盘阈值清理其他任务或未核对引用的对象。
