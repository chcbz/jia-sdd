# D3实施工作项

Owner：当前聊天负责本版设计；产品实施尚未启动。下列编号只是设计工作项，不是已登记的编排任务ID；没有向其他聊天派工。

| 项 | 内容 | 验证 |
|---|---|---|
| EX-01 | 固定实际源码；确定平台注册来源、原资料版本覆盖、assignment/grant字段和共享锁顺序；补政策/授权必要迁移 | 写出A/B/C失败用例，身份不可伪造；同主历史与活动记录迁移 |
| EX-02 | 开关与统一候选；扩展原point-and-deliberate，复用自动首轮及原恢复 | 独立开关、关单并发、资料范围、重复提交、离线排队 |
| EX-03 | 统一执行上下文贯穿API/Chat/Runtime | 领取、文件、ACK/receipt/成果/恢复；本人链路同测，无外单runner |
| EX-04 | 同步既有原型，移除待指令/接单后台演示；实现详情开关和原任务选择/确认/继续办理 | PC/移动、公开归属、关单后存量可继续、失败与账号切换 |
| EX-05 | 固定候选、正式回归与发布准备；发布仅按另行实际授权 | API Flow5260799、Web Flow4403172及Runtime所属仓验证；不把本地诊断当正式验收 |

EX-01至03先闭合统一合同，EX-04按同一合同接入；无独立Reviewer或逐阶段人工审批。本轮不执行实现、构建、迁移或发布。

交接必须携带 `/home/isp/wsps/cyf/AGENTS.md`、`/home/isp/wsps/cyf/ops/orchestration/README.md`、本目录D3及 `/home/isp/wsps/cyf/api/docs/interface-standard.md` 1.2（SHA见design.md）、真实任务ID/仓库/基线。Runtime跨仓显式传达规则，不修改全局配置。正式构建/部署统一Flow，develop不自动部署。
