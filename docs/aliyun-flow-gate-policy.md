# Flow 门禁依据与精简（2026-09-13）

用户指令：**把没有依据的检查去掉，后面遇到问题了，有依据再增加。** 历史脚本常量、重复文档和“测试证明常量生效”都不能替代依据。

## 本次删除

- 安装器的固定 5GiB 额外预留，以及启动器的默认 5GiB 磁盘/1GiB 可用内存硬门槛。资源指标仅输出观测值。
- 固定压缩包、解压体积、单成员/清单大小和 JAR 条目数等未经测算的上限。
- 因发布锁被占用而立即失败、或等待 60 秒后失败。保留互斥与锁顺序，排队后再次核对是否已被更新 Run 超越。
- 停止请求后的固定 60 秒自动强杀、启动等待超过 20 分钟自动判败。等待真实进程退出或健康；进程提前退出立即报错，Flow 作业提供取消出口，不以年龄代替失败证据。

## 保留及依据

- 按 2026-10-08 最新规则：前端云端测试与同 Flow Run 制品，后端本地测试与同 build ID 制品；两端均绑定精确 commit/tree、制品摘要及线上核验。保留历史云端证据，不将其当成本地发布证据。
- 制品摘要、来源、路径/权限、进程身份、端口归属：防止发布错误字节、越界写入或操作其他进程。
- 停机前按实际解压字节和回退副本大小检查可用空间；不足会使必要写入无法完成，不加固定运行预留。
- 备份、原子替换、持久化状态与恢复：处理已经开始的部署中断，不将此扩展为日常独立审查或手工审批。
- 健康与功能验收分开。HTTP 200/health UP 不代表登录成功。

## 后续增加规则

先记录实际问题及证据，再增加能针对该问题的最小检查；数值须有测量和推导，不以“保险起见”自设阻断项。调整等待行为不代表可以假报成功：没有健康证明就保持运行中/未验收。

当前维护源：
- `ops/ci/aliyun-flow/host/cyf-api-flow-deploy`
- `ops/ci/aliyun-flow/host/cyf-api-flow-install`
- `ops/ci/aliyun-flow/host/cyf-api-kit`（本次将现行生命周期脚本纳入版本管理）

验证：`python3 -m unittest discover -s ops/ci/aliyun-flow/tests -p 'test_api*.py' -v`。这些是隔离临时目录中的控制面测试，不调用生产生命周期，不替代正式应用回归（前端 Flow、后端本地）。


### F06 发布结构兼容（2026-10-25，API develop b9dede8bf88e66d6716033e9631d8aba7d43bd78）

仅覆盖 `agent_task_artifact_outcome` / `agent_task_artifact_outcome_decision` 的发布后置结构检查，不改应用授权或自动迁移。
- 保留 owner/client/tenant 列、精确唯一键和索引、列类型/空值/排序规则、`chk_artifact_outcome_supersession`。风险分别为跨主体访问、重复裁决/并发覆盖以及替代成果指向不一致；缺失或表达式漂移仅阻止本次 schema 验证，不改写已有结果。
- `chk_artifact_outcome_state`、`chk_artifact_outcome_versions`、`chk_artifact_outcome_digest`、`chk_artifact_outcome_decision_versions`、`chk_artifact_outcome_decision_digest` 是服务层已实施规则的重复数据库表达；不再要求已有表必须补齐这五个 CHECK 才能发布。存在时仍核对原表达式/ENFORCED，未知 CHECK 或改义 CHECK 不放行，防止额外约束导致写入失败。新建表沿用固定 SQL；不因兼容读取就 ALTER/DROP 已有表，不改历史 SQL 摘要。
- 完整性不是取消：`AgentTaskArtifactOutcomeServiceImpl.normalizeDecision/requireRef` 规范版本并生成 SHA-256；`now` 生成正时间；`requireOutcomeState/requireOutcomeVersion/requireOutcomeAudit/requireOutcomeShape` 拒绝损坏读取；`requireExactReplay` 校验主体、版本、摘要及幂等记录。保留 Mapper 的 owner 条件、唯一键、事务与 CAS。错误请求/损坏记录仍在当前操作范围内失败，不猜测补全或自动重放。
- 回归入口：`ops/ci/aliyun-flow/tests/test_api_additive_schema.py` 既有结构保留用例，覆盖旧表缺重复 CHECK、必需替代关系 CHECK 缺失、存在但表达式漂移与 owner 索引漂移；应用既有 ArtifactOutcome 服务/事务回归不删除。本节不代表上线完成。生产只读盘点两表目前0行；无法证明缺失约束由哪次历史操作造成，不编造历史原因。
