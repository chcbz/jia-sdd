# 1.13.1 实施任务与工作量初估

日期：2026-09-19。W00–W09 已合并为实现候选；W10 验收和 W11 发布仍未执行。表格保留原始实施拆分与估算，不是第二运行台账；实际 Owner、exact SHA/tree、gate、blocker、next_action 只进 `docs/implementation/TASKS.yaml#runtime_ledger_json`。不新增 Reviewer。

## 任务拆分

| ID | 责任路线/路径边界 | 交付物 | 依赖 | 初估人时 |
| --- | --- | --- | --- | --- |
| W00 | 主 Owner；API/chat/runtime 只读盘点及规格 | exact 调用图、会话 ACL、初始 lease/producer、内容映射、迁移及协议冻结；真实测试资源清单 | 无 | 6–10 |
| W01 | critical_worker；api/agent/core、mapper、service；明确 chat scope 接口 | 任务/会话双向关联、源版本关系、作用域与 contextRevision、事务及迁移测试 | W00 | 18–28 |
| W02 | critical_worker；api/agent 执行编排/租约接入 | 私人/任务两模式、唯一派发、快照授权、run/workItem/lease、幂等、状态查询和取消边界 | W00、W01合同 | 18–30 |
| W03 | critical_worker；api/chat 与 agent adapter | 无 Provider 会话创建/解析、文件消息持久化、可靠事件与会话 ACL；不重复模型调用 | W00、W01合同、W02合同 | 12–20 |
| W04 | critical_worker；api/agent output/artifact/formal mapping | 原字节复用、三处成果投影、正式提交、派生版本、恢复同步、不重复收费 | W02、W03合同 | 20–32 |
| W05 | balanced_worker；web 共享文件/关联组件与 composable | 统一选择器、版本/多资料/来源卡片、身份切换清理 | W01合同 | 12–20 |
| W06 | balanced_worker；web 工作空间与 BountyPanel 接入 | 双向关联、执行历史、任务议事导航、三处预览下载与状态 | W05、W01/W04合同 | 12–18 |
| W07 | balanced_worker；web ChatPanel/useHallConversation/useOutputs | 议事附件、显式文件模式、执行/成果卡、真实会话成果查询、重连恢复 | W05、W02/W03/W04合同 | 16–26 |
| W08 | API/Web 各路径实施 Owner 自检；不跨写 | 继续修改/分支版本、正式验收/返工、私人采用与统一状态；不绕过 R2 | W04、W06、W07 | 12–20 |
| W09 | critical_worker（runtime）+ balanced_worker（预览，独立路径） | 真实格式处理缺口、能力实测、图片对照、PPT/PDF逐页和Excel分表预览接线 | W00；最终依赖W02/W04 | 12–20 |
| W10 | gpt_test_runner；测试/证据路径 | A/B完整验收、故障注入、双身份双任务、跨入口两轮修改；仅获授权才跑Provider | W01–W09 | 24–40 |
| W11 | 发布 Owner；发布证据与文档 | exact develop候选、API/Web/必要runtime测试制品、冻结release/1.13.1、发布后回归及验收通知 | W10通过、发布授权/窗口 | 6–10 |

涉及同一 implementation 文件的 W01/W02/W04 写入按 Owner/路径串行整合；冻结接口后的 UI 可并行。表里的“合同依赖”允许 mock 先行开发，但验收必须连真实服务。多 Owner 任务实施前进一步拆成不重叠写入子任务；不得以表格为共同写权限。

## 估算口径

- 基础 **168–274 人时**，是按上表拆分的工程初估，不是已测得 Agent 耗时或确定交付日期。
- 风险准备 **24–48 人时**：租约/正式交付适配 8–16、内容存储/迁移 8–16、真实多格式工具与预览 8–16。总计 **192–322 人时**。
- W09 估算假设现有运行环境可复用工具；若实际缺失图片编辑 Provider、Office渲染或PDF处理工具，W00/W09产出具体缺口再重估，不能在这个范围内假称必能完成。
- 若 API/Web 两线各每天6小时有效投入，理论容量下界约16–27工作日（总人时÷12向上取整）；**不是日历承诺**，任务依赖、串行Gradle、授权等待和发布窗口额外影响。
- W00结束及首个真实DOCX任务闭环后用实际耗时重估。真实Provider费用独立统计；未知不估为免费，不用人时替代token/工具账单。

## 推进顺序和每段完成标准

1. **合同与真实边界**：W00，先把无任务会话和任务运行的区别定清楚。
2. **选材/授权/导航闭环**：W01、W05、W06前半，不触发模型；证明同文件固定版本可在任务和会话选中，跨用户拒绝。
3. **真实单格式纵向闭环**：W02–W04、W07，以DOCX跑“任务→议事→实际Agent→自动成果→正式验收”；验证后不宣称多格式全完成。
4. **返工与恢复**：W06剩余/W08，两轮修改、并发版本、断线、索引恢复、私人转任务。
5. **逐格式补齐**：W09/W10，图片生成/编辑、PPT新建/修改、Excel/PDF和全部预览；未通过的项目逐项修复。
6. **候选与发布验收**：W11，技术成功与业务通过分别记录，发布后不能只测200和上传。

## 自检、测试与发布

- A类场景无需Provider；正式相关测试选择必须覆盖个人空间、task file links、conversation scope、执行、artifact、formal delivery、Web身份/回放/版本。
- API相关Gradle先读对应build.gradle，再经 `python3 ops/orchestration/cyf_orchestrator.py gradle ...` 串行运行；实施时记录准确selector、tree SHA、fixture digest，复用未变树证据。
- Flow可用时复用5260799/4403172；目前沿用2026-09-17本地临时授权时必须标 `build_origin=local_user_authorized`，不伪造Flow Run。服从用户最新授权及版本发布时间安排。
- 自检后合入组件develop，取经过验证的exact SHA冻结 **release/1.13.1**；已有同名分支先readback，不覆盖1.13.0或已有release。
- 数据迁移列出真实目标/恢复方案/授权，runtime发布列出版本源码和制品摘要。无权操作不得从发布需求推导授权。
- 线上发布顺序：兼容性DB/API增量 → 必需runtime升级与握手 → Web。保留旧客户端读写兼容和既有私有文件访问；逐项记录实际健康/权限/进程归属/互斥与可恢复安装。
- 1.13.1完整发布前A/B均通过；发布后C回归覆盖三入口，Provider线上抽检仍需授权。未获线上付费授权则候选/部署状态与未验证项分开报告，不发“全部验收通过”。
