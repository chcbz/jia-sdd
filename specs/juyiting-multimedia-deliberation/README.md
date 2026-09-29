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

## 开发注意

- 先处理U0残留与U1合同，不直接启用所有能力开关。
- 明确生成请求可直接进入已授权execution，不强制先调用快速聊天模型。
- CHAT、资料读取、EXECUTE是权限边界，不是三套会话/三次固定模型调用。
- 老 `/chat/stream` 不开放execute hint；新编排器经任务授权调用既有执行链路。
- 未保存到个人空间的会话产物仍持久；试稿、归档、正式交付/验收分开。
- 新API/表逻辑名是拟议设计，不能把接口目录当已经部署的实现。
- 按最新AGENTS/Owner自检政策，使用独立worktree；不覆盖他人脏改、不创建Reviewer、不擅自部署/付费调用。
