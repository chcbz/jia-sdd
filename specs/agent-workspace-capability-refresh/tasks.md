# Agent workspace capability refresh tasks

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
