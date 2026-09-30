# 聚义厅多媒体悬赏议事：融合开发入口

当前研发分支：SDD / API / Web / Agent Client 四仓 `codex/juyiting-multimedia-deliberation`。

**2026-09-30 本次交付入口**：[长期融合详设交接](fusion-delivery-handoff-20260930.md)汇总精确远端分支核验、完整详设合同导航与开发顺序。fast已合入不等于最新develop已合入，更不等于产品已验收；下文旧切片限制保留对应日期的历史含义。

**本分支合入 fast-deliberation 作为开发基础，不表示完整多媒体业务已完成或可以直接部署。** 精确源码、实际测试、未关闭风险见 [整合回执](integration-baseline-20260928.md) 与 [U1增量证据](integration-u1-20260929.md)。

## 最新源码整合补充（2026-09-30）

[原生能力协商四仓源码整合](integration-u1-native-capability-source-20260930.md)已同步 API `5668c747` / Web `ab317fa` / Client `1812e5b` 的研发 pin 与远端证明：API 83、Web 144、Client Owner 172 项定向通过。旧交接/切片中的“协商施工中、页面未接线”保留其历史含义，最新状态以此补充和 `integration.yaml` 为准。引用入口仍 EMPTY_ONLY，合法费用授权及完整澄清/EDIT、双接应/Provider/浏览器/版本发布未完成，**不表示可验收**。

## 阅读顺序

1. [需求方案](spec.md)：用户流程及不做什么。
2. [长期融合方案](long-term-fusion-plan-20260928.md)：统一议事，不保留两个独立聊天系统。
3. [融合详细设计 v2](fusion-detailed-design-v2.md)：统一入口、授权、路由、上下文、状态机、兼容。
4. [原 UI / 媒体 / 归档与验收详设](design.md)：未被v2覆盖的合同继续有效。
5. [融合实施计划 v2](fusion-implementation-plan-v2.md)：U0–U4工作包及Owner/依赖/验证。
6. [分版本交付与验收计划](versioned-delivery-plan-20260928.md)：候选 1.13.45–1.13.47 的出厂条件与通知标准。
7. [验收](acceptance.md)：AC01–AC22，另加详设v2的FD01–FD12；共34项产品用例。
8. [集成状态](integration.yaml) 与 [便携证据](integration-evidence-20260928/README.md)。
9. [2026-09-29 轻量议事与 Agent 基础整合](integration-u2-chat-agent-convergence-20260929.md)、[受权媒体读取候选](integration-u2-media-read-20260929.md)、[U2会话执行lease集成](integration-u2-lease-20260929.md)、[U2受权输出清单](integration-u2-output-catalog-20260929.md)：均默认关闭，不等同上线。

- [受权媒体 HEAD / 音频 Range 验证](integration-u3-media-range.md)：API 单段字节范围、无正文 HEAD、416/If-Range；仍需浏览器和正式发布。
- [回复流内多媒体片段回归](integration-u2-web-reply-stream-parts.md)：`part.ready` 不再被请求状态处理吞掉；仅验证 Web 接收端，不是后端生成 `part.ready` 的证明。
- [待确认保存操作的恢复](integration-u3-archive-pending-reconcile-20260930.md)：服务端仍 pending 时用户显式复用原键 POST；后端归档接口仍未联通。
- [工作空间归档服务端原语](integration-u3-workspace-archive-primitive-20260930.md)：可信会话字节及来源校验后可创建 owner-scoped 文件版本；Chat 资产绑定/归档接口尚未接通。
- [会话成果归档的刷新恢复](integration-u3-archive-resume-20260930.md)：Web 同身份会话内保留原保存幂等键与操作ID；服务端归档仍未实现，不能将本切片视为归档验收。
- [议事会话内成果展示证据](integration-u2-web-inline-transcript.md)：受权成果组件进入同一聊天滚动区；仍未持久化 `part.ready`，未做浏览器验证。
- [2026-09-30 多轮媒体成果持续展示证据](integration-u2-web-live-gallery-20260930.md)：首稿后继续发现后续 EXECUTE 的已提交成果，尚无浏览器验收。
- [2026-09-30 客户端参考图+生图单次接应组合证据](integration-u2-client-references-20260930.md)：开发分支已整合，仍默认关闭、未付费/未部署。

## 2026-09-30 当前增量状态

[持久会话资产整合证据](integration-u3-durable-assets-20260930.md)：已提交输出可投影为持久消息/parts/事件，刷新历史可恢复；私有资产读取复用受权内容接口。默认关闭，未部署。

长期合同仍以详设 v2 为准；上述旧切片中的“未持久化/归档接口未实现”是对应切片当时的限制，不是本次最新状态。[成果区保存合同映射](integration-u3-output-asset-archive-20260930.md)现已源码接通，复用已有归档客户端及服务端 assetRef；**仍缺正式验收/完成编排及真实全流程验收，不能宣布可验收。**

[正式验收界面与原操作恢复](integration-u3-finalization-web-20260930.md)已完成Web源码切片，57项定向通过；[finalization冻结合同](finalization-contract-v1.md)是跨仓实现合同，API尚未整合/验证。UI完成不代表正式提交、领域验收或需求完成已真实联通。

[验收完成后的任务投影刷新](integration-u3-finalization-completion-refresh-20260930.md)已补齐Web联动，61项定向通过；只读刷新，不本地伪造任务完成。后端正式验收与schema启动依赖仍在开发，不通知可验收。

[原点将意图与只读恢复组件](integration-u1-web-point-and-start-20260930.md)已推送Web `7ac3bbc`，182项定向回归通过；实际页面/服务端能力协商仍未接通，不把恢复组件当点将全流程完成。

## 开发注意

- 先处理U0残留与U1合同，不直接启用所有能力开关。
- 明确生成请求可直接进入已授权execution，不强制先调用快速聊天模型。
- CHAT、资料读取、EXECUTE是权限边界，不是三套会话/三次固定模型调用。
- 老 `/chat/stream` 不开放execute hint；新编排器经任务授权调用既有执行链路。
- 未保存到个人空间的会话产物仍持久；试稿、归档、正式交付/验收分开。
- 新API/表逻辑名是拟议设计，不能把接口目录当已经部署的实现。
- 按最新AGENTS/Owner自检政策，使用独立worktree；不覆盖他人脏改、不创建Reviewer、不擅自部署/付费调用。

## 点将入口的真实闭环补充（2026-09-30）

[四仓远端分支与fast ancestry重新核验](integration-evidence-20260928/branch-reverification-20260930.json)已通过，且均与远端feature readback一致；这不是当前develop融合、构建或发布证明。[点将即办理入口详设 v1](point-and-start-entry-design-v1.md)记录实码缺口：页面普通点将仍走legacy，权威当前requirementRevision没有浏览器读接口。下一包按ENTRY-A/ENTRY-W/ENTRY-I接通原键v2点将、canonical投影及自动进入同一悬赏议事；不得猜revision=1、将grant当task、重发首轮或据UI单测宣称业务闭环。

## 原点将操作的只读恢复合同（2026-09-30）

[原点将操作只读投影合同 v1](assignment-operation-read-contract-v1.md)固定浏览器以**原幂等键**核对 grant / bootstrap / 当前 assignment 的响应、权限和恢复语义。该接口仍是施工合同，不能将文档链接或 `ADMITTED` 回执当作已生成媒体、已交付或已验收。

- `GET` 不 claim outbox、不创建消息或执行、不调用 Provider；404 不证明原 POST 没有被受理。
- 自动进入议事必须读取确切 conversation / initial request，验证 task、assignment、显式目标 Agent，再加载历史/事件；不从列表猜测、不补发首轮。
- grant 的允许操作集合与首轮 `initialOperation` 必须区分；“允许生成并修改”不等于首轮同时执行两次。当前接口实现缺口仍需独立代码包处理。
- [本次远端复核](integration-evidence-20260928/branch-followup-verification-20260930.json)只证明四仓分支与 fast ancestry；API 本地 schema-readiness 候选尚未验证/推送，不替换已记录的远端研发 pin。

## 真实首轮会话采用切片（2026-09-30）

[首轮采用与native成果终态源码证据](integration-u1-web-bootstrap-adoption-20260930.md)：Web `0e9be06`，130定向通过（新增35）。已受理首轮可精确挂入同一议事，原生媒体本轮终态只读核对后解除忙碌，领域任务完成不被混淆。**页面点将连接、后端候选验证及真实画鸟流程仍未闭环。**

[首轮动作与完整授权集合合同 v1](initial-operation-contract-v1.md)固定可选selector、旧请求hash兼容、单bootstrap与原键只读恢复；两个独立Owner正在按不重叠写集实现，不把允许操作集合当同时执行的动作清单。

## 当前schema验证与原生能力施工补充（2026-09-30）

[旧弱CHECK识别与真实Java/MySQL证据](integration-u3-schema-check-truth-20260930.md)已验证API `b1e7b068`：正常84项报告（42本次、42复用）及真实6项JDBC/Spring全部通过；不是整套启动、迁移或产品验收。

[原生悬赏能力/点将协商冻结合同](native-bounty-capability-contract-v1.md)新增独立native声明，保留fast-v1 EXECUTE=false；API、Web页面与Client分别施工。task引用/澄清/EDIT/合法费用桥、双接应与真实浏览器仍必须完成。候选版本号按版本计划末尾的远端占用补充重新核实。


## 需求前可选参考图施工（2026-09-30）

[需求创建与可选参考图原子受理合同 v1](requirement-reference-intake-contract-v1.md)已冻结：普通榜文由一个持久原操作创建真实task和精确REFERENCE关联，刷新只读查询，明确继续才原键/原正文重放；旧普通/funded接口不扩大权限。Web候选已接真实Bounty草稿、原请求恢复及页面路由，组件选择器与API事务实现分别独立施工；候选尚未成为跨仓生产基线。选择参考图不会放开当前native EMPTY_ONLY或费用授权；后续必须接真实task-file回读与执行输入、合法费用桥、澄清/EDIT及最终浏览器发布验收。


本次参考图施工期间再次核实[四仓当前远端分支](integration-evidence-20260928/branch-reference-intake-verification-20260930.json)，均已包含当前fast；[交接第8节](fusion-delivery-handoff-20260930.md#8-需求参考图施工期间的远端复核2026-09-30)保留候选与产品验收区别，以及确定拒绝原意图的安全处置待办。Web候选仍需修复选择器异步替换竞态并验证组合树，不将两项夹具组合测试视为真实画鸟通过。


## 2026-10-01 参考图入口Web整合

[Web精确组合源码证据](integration-u1-reference-intake-web-20261001.md)：远端`84b14a5`，213定向通过，scoped ESLint通过；真实需求表单、真实选择器和真实创建composable已组合验证，选择器异步替换竞态已修复。上文旧候选/施工限制保留对应日期含义。API仍独立验证，不把此Web研发pin当成跨仓联调、资料执行或可验收；native仍EMPTY_ONLY、费用未授权，完整34产品用例NOT_RUN。
