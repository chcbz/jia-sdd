# 长期融合实施计划 v2

日期：2026-09-28。本轮已授权的是 feature 整合与设计；后续业务包仍是计划。运行状态只在主工作区 `/home/isp/wsps/cyf/docs/implementation/TASKS.yaml#runtime_ledger_json` 登记，本文件不是第二套运行 ledger。

## 1. 分支与实施策略

四仓统一分支 `codex/juyiting-multimedia-deliberation`，以各自精确远端 develop 为第一亲合入 fast 的精确提交。保留 develop 修复和 fast 基础，不强制覆盖任何一边，不更新 develop/release，不触发部署。

组件的真实 merge commit 保留两个父提交。SDD 仅引入 fast feature 文档目录，保留 develop 的其他文档与新多媒体规格；历史无关文档变化不顺带传播，api/web gitlink 在组件已推送后固定。原 fast 分支不改写、不删除，后续工作集中在新分支。

[M0 源码表/端点映射与待冻结项](m0-source-mapping-and-contract.md)是U1/U2实现的施工对照，尚不是迁移通过或新接口上线证明。

## 2. 后续工作包与依赖

| 包 | 责任建议/路径边界 | 交付内容 | 依赖 | 通过证据 |
| --- | --- | --- | --- | --- |
| U0-A | API Owner；chat admission/relay、身份、上下文 | 收口F1–F3：可信身份、逐目标协商、可重建历史/宋江快照；兼容machine JWT/迁移 | 本轮整合基线 | final tree的相关Java回归、实际schema/认证夹具；未测不标通过 |
| U0-R | Client Owner；chat-runtime/app-server/agent-client | 真实能力声明、read-only-constrained隔离、INSPECT固定manifest；保留START/恢复 | 冻结wire，与U0-A并行 | 默认/新版Profile、双接应、隔离/能力负向、冷恢复 |
| U1-A | API Owner；task授权/交互准入/执行协调 | grant、steps/link、统一入口、direct execute、澄清/撤权、事务outbox/CAS | U0合同确定 | FD01–FD10的服务级夹具；DDL和source mapping固定 |
| U1-W | Web Owner；会话交互/状态/reducer | 同一UI提交意图、授权状态、明确取消目标、请求聚合，不强制第二次开始 | U1合同，可mock并行 | 主状态、旧消息、晚到媒体、身份切换回归 |
| U2-A | API Owner；会话asset/workspace/delivery | CONVERSATION用途、未归档可读、精确输入、媒体读取、选定成果晋升/验收 | U1-A | ACL/摘要/保存与交付分阶段、producer身份/幂等 |
| U2-R | Client Owner；workspace-file-bridge | 精确参考/上一稿输入、outputs提交、execution-part关联 | U2合同，与API并行 | 真实字节/input digest/START/output commit；旧PRIVATE/TASK |
| U2-W | Web Owner；需求资料/图片卡/归档/验收 | 无参考/有参考画鸟、直接修改、放大/下载/保存与最终清单 | U1-W、U2合同 | 浏览器图片纵切，不能用mock图代替最终验收 |
| U3 | 各组件格式Owner | 音频播放/Range/保存，文本选区，普通文件和混排，双接应/断线恢复 | U2 | AC全部范围 + FD11/FD12；不冒充音频生成能力 |
| U4 | 集成Owner/gpt_test_runner | exact pair联调、实际MySQL、迁移/旧新协议、Provider已授权端到端；兼容退出评估 | U0–U3 | AC01–AC22 与 FD01–FD12 共34项实际状态，构建/部署/业务验收分开 |

U0不是新的独立Reviewer队列；Owner自检后按真实证据推进。

## 3. 与 v1 工作包的映射

- F0 拆为本轮 merge conflict 整理与后续 U0 能力/上下文/隔离收口；不把冲突已解决等同缺陷全部关闭。
- M0 由长期方案、详设v2建立决策基线；具体DDL、DTO和wire夹具仍须U1冻结。
- B1/B2/B3 对应 U1-A/U2-A；R1 对应 U0-R/U2-R；W1/W2/W3 对应 U1-W/U2-W/U3。
- I1 是图片纵切，不代表整体完成；I2 扩展为 AC01–AC22 + FD01–FD12。
- 原R0发布包只在真实上线条件和授权成立后执行，本轮没有release/deploy授权。

## 4. 变更边界与退出要求

每个Owner只写自己的worktree和已分配路径；相邻API grant/asset/delivery由同Owner或显式交接处理，不能多人争用一文件。不同仓/模块可并行，不设置无依据的全局串行源代码队列。

每包交付：exact commit/tree、冲突/合同变化说明、最小selector、实际结果及日志、DB fixture digest（涉及数据库时）、未完风险。不在SDD中用未经测试的源码pin冒充accepted基线；开发pin明确标研发基线。

兼容adapter退出需有目标客户端迁移与在途请求处理证据；默认目标不可假定已升级。收窄能力声明可以作为安全过渡，不能按此标“功能已完成”。存储复制字节可长期保留，不为去重做无关大迁移。

## 5. 核心风险专项

- 撤权/重新点将与START/下载/上传竞态：检查grant/assignment/run版本，不能仅前端按钮禁用。
- 用户资料注入：C1元数据不冒充C2真实读取，附件不能授予工具/费用权限。
- 多Agent与多owner：目标能力和上下文独立，不能广播私有结果或共享模型线程。
- 部分完成：text_final、asset.ready、archive.saved、delivery.submitted、decision.accepted、task.completed分开恢复。
- Provider结果未知：承认未知并对账；不能宣称网络级exactly-once，也不能自动重跑导致重复收费。
- 功能开关不代替数据库/认证风险检查；新schema与machine JWT变更需实际夹具证据。

## 6. 本轮验证范围

按实际整合树进行冲突标记/whitespace/语法、Web与Client相关定向测试；API检查最近build.gradle后通过orchestrator进行必要验证，实际执行范围和失败归因以 `integration-baseline-20260928.md` 为准。

本轮不会为了文档中的未来功能跑付费模型、浏览器生成、真实库迁移或生产构建。没有实测的事项保持NOT_RUN；性能慢只记观测，不新增任意数值硬门槛。无Reviewer，未修改其他任务进程/服务。

## 2026-09-30 入口闭环增量

新增[ENTRY-A/ENTRY-W/ENTRY-I施工包](point-and-start-entry-design-v1.md#5-最小开发包与验证)：从权威当前requirement snapshot读接口接通真实v2点将和自动议事。可以与独立finalization/schema-readiness路径并行，但组件pin须基于已测试候选。此处仅任务定义，不是第二套运行ledger，不改变现有Owner写集或产品验收状态。
