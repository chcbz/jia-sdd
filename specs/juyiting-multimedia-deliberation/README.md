# 聚义厅多媒体悬赏议事：融合开发入口

当前研发分支：SDD / API / Web / Agent Client 四仓 `codex/juyiting-multimedia-deliberation`。

**本分支合入 fast-deliberation 作为开发基础，不表示完整多媒体业务已完成或可以直接部署。** 精确源码、实际测试、未关闭风险见 [整合回执](integration-baseline-20260928.md) 与 [U1增量证据](integration-u1-20260929.md)。

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

## 开发注意

- 先处理U0残留与U1合同，不直接启用所有能力开关。
- 明确生成请求可直接进入已授权execution，不强制先调用快速聊天模型。
- CHAT、资料读取、EXECUTE是权限边界，不是三套会话/三次固定模型调用。
- 老 `/chat/stream` 不开放execute hint；新编排器经任务授权调用既有执行链路。
- 未保存到个人空间的会话产物仍持久；试稿、归档、正式交付/验收分开。
- 新API/表逻辑名是拟议设计，不能把接口目录当已经部署的实现。
- 按最新AGENTS/Owner自检政策，使用独立worktree；不覆盖他人脏改、不创建Reviewer、不擅自部署/付费调用。
