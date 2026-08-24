# Agent workspace business capability refresh tasks

## Client

- [x] 将 register/presence abilities 改为仅由当前 `codexWorkdir` 动态发现。
- [x] 停止合并 Profile `abilities`、Profile `skills` 和已安装 `SKILL.md`。
- [x] 将输出收敛为固定中文项目业务能力 allowlist。
- [x] 实现 CYF 聚合签名：Gradle settings + `agent/chat/task/oauth/user/kefu/point` 完整核心模块。
- [x] 实现 `jia-*` 模块局部目录识别，避免通用同名目录误判。
- [x] 实现 `weather.py`/`weather.html` 到 `天气查询` 的映射。
- [x] 保留目录项、manifest、symlink、TOCTOU、FIFO 和 descriptor 安全边界。
- [x] 更新 codex-ws-agent 操作文档和覆盖测试。

## API/Web

- [x] 沿用现有 abilities 协议、runtime 存储和调度消费，无代码变更。
- [x] 确认 API 精确匹配旧英文能力的兼容风险不阻塞本次“中文业务能力”目标。
- [ ] 后续按业务需要迁移仍要求 `codex`、`strategy`、`execution` 等旧字符串的任务模板或存量任务。

## Integration and verification

- [x] Client 完整测试 109/109、配置校验、语法检查和 diff 检查通过。
- [x] 独立只读评审最终 ACCEPT；无 P0/P1/P2，一个 package.json 冗余解析 P3 不阻塞发布。
- [x] Client 提交并推送：`d9e966ea1f387d42eb02e2458e7f557dbc16d0d7`。
- [x] 部署 codex-ws-agent，并确认源文件与部署文件 SHA-256 一致。
- [x] 生产验证三个本地 Profile 形成空能力、天气能力和 CYF 中文业务能力三类快照。
- [x] 记录扈三娘、李逵仍由外部旧客户端连接并上报英文通用能力。
- [ ] 在扈三娘、李逵所在主机升级客户端后，复核其 register/presence 快照；不得手工修改数据库 runtime 行。
