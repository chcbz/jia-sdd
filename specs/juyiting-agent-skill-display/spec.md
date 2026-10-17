> 2026-10-17 发布收口补充：1.16.8已由API Flow152、Web Flow224部署并完成范围内在线验收。当前结果见 `release-1.16.8.md` 和 `integration.yaml`；下文旧NOT_RUN/阻塞/估算为历史阶段，不代表当前状态。

# 点将册：技能、本领展示与响应式布局

日期：2026-10-17；任务JYT-AGENT-SKILL-DISPLAY-20261016（执行ledger未登记）；唯一Owner：本聊天Owner。
当前版本：**D4**。用户已认可完整原型优化方向；本轮交付方案/详设/计划，产品实现未开始、正式测试未运行、未发布。

## 目标

- 移动端名册→详情，返回保留列表上下文，密议/点将底部常驻；桌面约43/57分栏、独立滚动。
- 明确展示实际“技能”与原“本领”，安装核验与运行就绪分开，不把就绪当任务授权。
- 详情及刷新读取当前owner单Agent最新已入库信息；不触发Runtime扫描或重注册。
- 原接口保留本领投影；新只读GET复用原权威，不增表、不复制回退、不改派单。

## 当前交付入口

- optimization-d4.md：优化方案、范围、UI证据。
- design-d4.md：完整API、逐文件实现、UI状态/导航/CSS/异步、安全与精确写集。
- plan-d4.md：一次完整编码，之后统一双Flow验证及版本发布；全部编码30分钟目标，无无条件保证。
- acceptance-d4.md：产品用例，当前均NOT_RUN。
- ui-review.md：已认可完整原型、截图及源指纹；不是产品完成证明。
- handoff.md、integration.yaml、evidence/source-baseline-d4.json：接续与真实状态。

非目标：技能交易/安装、本领编辑、Runtime重启、DB迁移、任务筛选/分配算法。未来技能＋本领派单另行设计。

统一规范：/home/isp/wsps/cyf/AGENTS.md；/home/isp/wsps/cyf/api/docs/interface-standard.md v1.2。前后端正式测试/构建/制品/部署均为Flow4403172/5260799；develop不自动部署。D1—D3仅历史来源，不是现行执行计划。
