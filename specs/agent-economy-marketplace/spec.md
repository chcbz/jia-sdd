# Agent 银两悬赏结算与技能市场

## Problem

聚义厅已经支持张榜、推荐、显式点将、多 Agent 指派和任务回报，但 `agent_task_meta.reward` 目前只是展示/权重字段，没有真实余额、冻结、结算、退款或对账语义。现有 `point` 模块把余额保存在 `user.point`，`point_record` 只是事后流水，也缺少悬赏交易所需的并发账本、幂等、托管和关联业务单据能力。

同时，Agent 的 `agent_runtime.abilities` 已能反映客户端当前发现的技能，但系统没有技能商品、版本、购买、授权、交付和安装确认流程。直接把“已购买”写进 `abilities` 会把商业授权和运行时事实混为一谈，并可能让未安装代码被误判为可执行能力。

## Goals

- 聚义厅张榜时可设置一笔总悬赏金，并在张榜时将全额银两托管；成功任务的模型成本、平台费和 Agent 所得都从该总额内结算。
- Agent 揭榜前可取得一份有时效、可审计的费用预估，按模型、输入/输出/缓存/推理 token 和版本化价目表计算，并看到预估净所得、最坏净所得与最低收益是否满足。
- 揭榜操作继续显式携带目标 `agentId`，原子校验任务版本、报价、结构化 verified skill requirement、余额托管和 Agent 身份，避免重复揭榜和超卖。
- 每次模型调用前预留费用上限，执行后记录权威用量；验收通过后按“总悬赏金 − 实际模型费 − 平台费”结算 Agent 所得，失败/取消时退回未消费余额。
- Agent 技能可作为带版本的商品上架；MVP 由平台自营销售，购买时显式指定目标 Agent，并仅通过 `command.dispatch/SKILL_INSTALL` 交付；支付成功并完成绑定订单、runtime、版本和摘要的签名安装证明后，该 Agent 获得有效技能授权。
- 所有资金动作具备不可变流水、双边平衡、幂等、乐观锁/行锁、退款、对账和审计能力。
- 保持聚义厅 `/agent/map` 与 `/agent/roster` 分流、显式目标 Agent 指派、canonical Agent identity 和现有任务协作状态机不变。

## Non-goals

- 不把自由文本技能/能力标签当作 ACL、高风险操作授权、资金榜硬门禁或身份凭据；硬要求只能引用已授权且有签名安装证明的结构化技能版本。
- 不在第一版支持法币充值、提现、税务、发票、跨租户交易、第三方卖家分成或真实证券/加密资产；MVP 技能商品只允许平台自营、已审核版本。
- 不直接复用或双写旧 `user.point` 作为新交易账本；旧积分/礼品继续独立运行。
- 不根据聊天正文或模型思维过程自动决定是否揭榜；只返回结构化成本、预算、能力和风险指标。
- 不允许购买后仅靠后端改写 `agent_runtime.abilities` 伪装成“已安装”。
- 不在本 SDD 重做现有成员、work item、lease、artifact 或会话作用域模型。资金化 MVP 只开放单 Agent/单工作项；legacy unfunded 任务继续保留现有多人/auto-assign 行为。

## Scope

### API

- 新增独立 `economy` 域，承载 `SILVER` 账户、双式账本、任务托管、交易单、调用前费用授权、版本化模型价目表和模型用量凭证；不让旧 point 实现成为资金权威。
- 在 `agent` 域扩展悬赏资金契约、报价、揭榜、预算补充、结算查询和技能商品/订单/授权/安装状态；旧 create payload 继续创建 `LEGACY_UNFUNDED`，只有显式资金字段进入新契约。
- 将任务完成/验收、取消、失败与资金结算连接起来，并通过 after-commit 事件发布结果。
- 为托管、揭榜、用量写入、技能购买和安装回执提供幂等键、精确 scope 和事务边界。

### Agent Client

- 在受管 Agent 客户端实现 `command.dispatch/SKILL_INSTALL` 下载、验签、权限/兼容性校验、原子安装、设备签名 attestation、严格递增 `installedSkills` 快照和 ACK/result 恢复。
- Agent 客户端沿用 ADR-004：在现有 `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/` 版本化源中开发和记录 revision，完成后同步到 `/home/isp/apps/codex-ws-agent/` 并执行 smoke；不新增独立仓库，但也不把仅 API/Web 完成视为技能市场完成。

### Web

- 悬赏榜张榜表单增加总悬赏金和费用说明；榜文详情展示该金额在模型成本、平台费和 Agent 净所得之间的预估分配。
- 榜文详情展示已托管金额、预估 token、预估费用、最坏费用、剩余预算和实际结算。
- “揭榜/点将”前先请求报价，明确展示可承接、需谨慎或不可承接原因，再由用户或 Agent 确认。
- 增加银两余额/流水入口和技能集市；购买时使用当前选中 Agent 作为默认目标，但请求必须显式发送 `targetAgentId`。
- 展示技能交付状态：待安装、安装中、已生效、失败已退款。

## Constraints and risks

- 金额使用 `BIGINT` 微银两，API 使用十进制字符串；禁止 JavaScript `Number`、浮点和数据库 `DECIMAL` 隐式舍入参与账本计算。`1 银两 = 1,000,000 微银两`。
- 模型价格不得硬编码在前端或报价代码中；报价和结算必须绑定不可变 `priceBookVersion`。
- 外部模型调用和技能安装不能位于数据库事务内；必须使用托管 + outbox/命令 + 确认/补偿流程。
- 原始 prompt、模型输出、API key、lease token 和技能私密包不得进入资金事件或普通审计日志。
- 技能包属于可执行供应链内容，必须有不可变摘要、发布者、权限声明、签名/审核状态和安装回执；自由文本 `abilities` 不能作为付款或激活证明。
- 当前任务 `reward` 为 `Integer` 且旧 point 余额更新存在并发缺口，不能作为新系统资金真相。
- 这是身份、ACL、交易、并发和迁移 P0 变更；实现必须由 `critical_worker` 所有，独立 `sol_reviewer`/`adversarial_reviewer` 审阅，并通过隔离数据库事务测试。
