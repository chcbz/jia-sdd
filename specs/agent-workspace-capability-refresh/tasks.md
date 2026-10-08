# Agent workspace capability refresh tasks

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

历史 acceptance 与 release 均有依据，统一原顶层 accepted 与 release.released 的陈旧状态，归档 2026-08-23 交付。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：AR-20260906-07。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 当前执行动作

后续 marker/工作目录识别问题按独立缺陷处理。

以下原始清单为合同/历史记录；当前完成状态采用 delivery-status 的任务映射，不能据旧未勾选项重新派工。
<!-- END SDD delivery reconciliation -->

## Client

- [x] 实现受限、allowlist 化的工作目录项目能力发现。
- [x] 将工作区能力合并到 register/presence abilities 快照。
- [x] 覆盖项目 marker、宽泛 home、symlink/TOCTOU/FIFO、动态增删和 manifest 精确边界测试。
- [x] 更新 codex-ws-agent 操作文档。

## API/Web

- [x] 沿用现有 abilities 协议、runtime 存储和调度消费，无代码变更。

## Integration and verification

- [x] 独立只读评审通过。
- [x] Client 完整测试和配置校验通过。
- [x] 提交、推送并部署 codex-ws-agent。
- [x] 生产验证三个 Profile 根据各自 workdir 形成差异化快照。
