# SDD 全量状态与重新分配基线 — 2026-09-14

> 文档任务：`SDD-RECONCILE-20260914`。这是静态 SDD 投影，不是调度台账；唯一当前执行事实仍是 `docs/implementation/TASKS.yaml#runtime_ledger_json`。

## 本轮依据与口径

- 快照来源：`docs/implementation/archive/2026-09-14/reassignment-ledger.json`，生成于 2026-09-14，源运行台账更新时间为 `2026-09-14T10:41:34+08:00`。
- 任务总数 **213**：仅 `done`、`deployed_online_verified`、`deployed_verified` 计入“功能闭环”，共 **71** 项；其余 **142** 项均保留为重新分配、配置启用、业务验收或用户授权事项。
- `accepted`、`integration_ready`、`deployed_default_off`、`deployed_business_activation_pending`、模拟 ACK、源码提交及单次健康检查均**不等同**于功能交付完成。
- 本次不重写 SHA 冻结的 `spec.md` / `design.md` / `integration.yaml`，不运行 `sddw pin`，不更改 root gitlink，不执行本地 Gradle/Vite 构建，也不触发生产操作。

## 当前交付结论

| 需求域 | SDD 生命周期 | 已闭环边界 | 未闭环 / 重新分配边界 |
| --- | --- | --- | --- |
| Agent 客户端技能刷新 | released | 历史已发布交付包保留。 | 新的原生客户端安装、当前 API 兼容回归、真实注册 / F01 / E05 ACK 另行推进。 |
| Agent 工作目录能力刷新 | released | 历史已发布交付包保留。 | 后续回归按独立缺陷处理。 |
| OAuth 公共客户端加固 | released | 历史发布记录保留。 | 不扩大为账号安全和公共公测已整体完成。 |
| 案卷阁典籍阅读 | implementing | 已有发布和修复记录保留。 | 真实认证阅读、阅读进度、书签、私密笔记、双身份隔离及业务验收仍待重分配。 |
| 聚义厅横竖屏 | implementing | O00–O04 均有源码 accepted 记录。 | 页面真实交互 / 设备验收不因源码 accepted 自动关闭。 |
| 聚义厅任务协作 / 悬赏榜 | implementing | M3-RG 历史上线记录、D06/D08/D09 等实现证据保留。 | M4/M5、默认关闭能力、真实 Agent 安装 / 激活 / 业务验收尚未完成。 |
| 聚义厅语音会话 | implementing | API/Web/集成候选与部分制品证据保留。 | 真正 STT/TTS/音频 Provider、运行时启用与真实用户验收仍未完成。 |
| 银两交易、技能市场、托管租金 | implementing_preview | V0 已有若干 accepted 切片。 | 真实交易、收费、退款 / 补偿、安装 / 激活及业务验收不得按源码进度关闭。 |
| 公共公测与账号安全 | implementing | PWA 安全候选和部分发布记录保留。 | 托管隔离、任务 ACL、公开可用性、真实身份 / 邮件 / 认证验证仍待收口。 |
| API 可用性 / 性能 / 发布运维 | implementing | API 502 恢复、若干 Flow 发布与启动优化证据保留。 | 真实运行采集、性能优化、邮件认证、自动化健康与当前发布核验按独立任务重分配。 |

## 142 项待办的重分配队列

| 域 | 数量 | 当前主要状态 | 首要重新分配动作 |
| --- | ---: | --- | --- |
| 聚义厅语音会话 | 28 | 27 accepted、1 waiting_user | 先补当前 API/网页运行时兼容性，再在已授权 Provider 环境完成真实语音验证。 |
| 聚义厅任务协作 / 悬赏榜 | 23 | accepted、default-off、业务激活待办并存 | 以功能开关和真实 Agent 业务 ACK 为边界拆分 M4/M5。 |
| 发布与运维 | 22 | accepted、integration_ready、waiting_user/mail_admin 并存 | 将邮件认证、Flow 配置、启动优化和健康监控拆为可独立交付项。 |
| 其他跨域 / 历史 follow-up | 21 | accepted、waiting_user、验证待办并存 | 按具体 task_id 复核依赖和当前源码，不批量宣布关闭。 |
| 经济 / 技能市场 / 租金 | 18 | 7 accepted、11 awaiting_business_acceptance | 先取得收费 / 退款 / 生产数据授权，再做真实交易与补偿闭环。 |
| API 性能治理 | 15 | accepted、targeted_verification、runtime capture 待办 | 记录真实慢请求，按证据优化；性能阈值不作为中断可用性的硬门禁。 |
| 横竖屏体验 | 6 | 全部 accepted | 组织真实设备 / 用户场景验收，未验收前不归档需求。 |
| 公共公测 | 5 | accepted | 完成发布后实际访问与身份隔离验收。 |
| 原生 Agent 兼容 | 4 | integration_ready、activation pending、waiting_user | 针对当前 API 版本重做兼容回归，随后固定客户端安装、readback 与真实 ACK。 |

完整逐项清单（包括 `task_id`、gate、blocker、精确 SHA/tree 和 next_action）只在：

`docs/implementation/archive/2026-09-14/reassignment-ledger.json#reassignmentInventory`

## 已归档的实现环境与证据边界

- 本轮以非强制 `git worktree remove` 清理 **38** 个已完成 / 可复建 worktree，未删除分支、ref 或提交；可见回收约 **4.37GiB**。记录：`archive/2026-09-14/worktree-cleanup.json`。
- 脏目录、submodule worktree、超时目录和三个仍有任务价值的关键 worktree 均被保留；不可把“未强制删除”误写为清理失败或任务完成。
- 仅移除了本轮自身生成的 7 个临时清理文件（32,011 bytes）；其他 `/var/tmp/cyf-*` 证据因仍有 142 项未闭环而保留。记录：`archive/2026-09-14/temporary-cleanup.json`。
- 已归档历史会话“迁移构建部署到阿里云流水线”；主控会话及登录认证会话未归档，因为后者仍有真实登录验收遗留。

## 后续 SDD 工作法

1. 从 `reassignmentInventory` 选择一个明确 task_id，建立路径范围和依赖；不同任务可并行，但同一任务只保留一个实现 Owner。
2. Owner 在对应仓库 `develop` 基线完成最小自检后合入；正式测试、构建、同 Run 制品和部署由阿里云 Flow 执行。
3. 不创建独立 Reviewer 队列；身份 / ACL、事务、迁移、付费与生产数据由 Owner 做风险自检，并保留精确证据和授权边界。
4. 发布成功仅证明该 Run 的源码 / 制品 / 健康核验；default-off、未启用 Provider、未发生真实交易或未完成用户验收的功能继续保持待办。
5. 完成一个需求域后更新本报告的后继版本、`specs/INDEX.md` 和对应 `delivery-status.md` 的**新日期补充**；不得改写冻结合同或历史失败结论。
