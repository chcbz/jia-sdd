# 1.3.0 成果交付 R1 — RB01 Day3 私有存储准入静态审计

**日期：**2026-09-15
**源码基线：**API `origin/develop` `36acfb55b4bd1743b280a48864b77bd931c1dc2c`（tree `d6951e59687a8830f5a524e33824e1fdb48ccd38`）
**范围：**源码和现有测试的静态审计；不读取生产配置、生产文件、用户令牌或业务数据；不运行 Gradle 或部署。

## 结论

私有文件系统 storage 的**源码安全合同已具备**，但它默认 fail-closed，且当前没有获得经授权的环境配置、受控 fixture 或备份恢复证据。因此不能把“代码存在”写成“线上 private storage 已准入”。本次不修改生产开关，也不启用新 artifact 写入。

Day1 读取已发布的可信 task artifact 仍不受影响；RB01 只决定未来对 managed filesystem artifact 的运行准入与完整性证据，不得影响聊天、任务终态或既有人工 artifact。

## 已验证的源码控制

- `AgentTaskArtifactStorageConfiguration` 在 `agent.task-artifact-storage.enabled` 未明确为 true 时返回 `DisabledAgentTaskArtifactStorage`；默认不会创建 storage root。
- 显式启用时要求绝对、非空 root、正数大小上限和非空 MIME allowlist；缺任一项启动失败。
- `FileSystemAgentTaskArtifactStorage` 对 root/object directory/file 使用 no-follow 属性检查、root file-key identity 检查、owner-only POSIX 权限、bounded read、内容 SHA-256/长度核验、scope-bound URI，并在对象路径/目录异常时 fail closed。
- managed bytes 在 task member ACL 和版本锁之后才写入；content read 在 member ACL 之后才访问 storage；未受管的外部 URI 不会被服务端读取。
- 已有单测覆盖 scope mismatch、symlink 篡改、重复 digest 并发写、数据库失败后不可寻址 immutable orphan、ACL/版本失败不触发文件写、内容 hash/长度一致性等。

## 尚缺的运行证据（不能由源码代替）

1. 受控非生产或已授权目标的**精确** `enabled/root-directory/max-content-bytes/allowed-mime-types` 配置 readback；不得展示或写入无关秘密。
2. 已有可信 task member fixture 的 list → exact-version content download → SHA/length 比对证据；不得新造生产 artifact。
3. second identity/client 的拒绝 readback；拒绝不能泄露 artifact metadata。
4. 备份/恢复或可证明的 root 可恢复性证据；以及临时 `.upload-*.tmp` 残留的受控清理记录（若确有残留）。
5. 通过 Flow `5260799` 对**同一候选 API commit**运行的相关测试、构建、制品和（如有后端变更）发布 evidence。

上述输入缺失时，正确行为是维持 disabled 或维持现有已验证状态，而不是猜测路径、创建目录、开启写入或向 production 发送探针。

## Day3 完成状态与 Day4 前置

- **静态 admission 审计：完成。** 未发现需要在本版本重复实现的 storage 代码缺口。
- **运行 admission/readback：等待受控 fixture 与精确目标授权。**
- **RB06A 集成：仅在运行 evidence 到位后执行。** 需要同身份成功、跨身份/跨 client 拒绝、映射缺失空态和可用性隔离；不能用无效 token 或匿名 403 代替业务 ACL 验收。
