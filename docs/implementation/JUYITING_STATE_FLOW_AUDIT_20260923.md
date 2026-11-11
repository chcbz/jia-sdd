# 聚义厅状态与流转审计（2026-09-23）

## 范围与证据边界

本轮为现状梳理及优化建议，未改业务代码、未构建部署、未写线上业务状态、未调用外部 Provider。

- 前端检查使用此前发布所用 worktree `.worktrees/fix-juyiting-private-entry-20260922`，而非较旧的 `web/` checkout。
  - HEAD `03c8d95fcfcfb76f0ed5a8ce6a0445370f4b409b`，tree `ba28e4e4456c16b7f72c36d84bf15a17fbf5c386`。
- API 检查目录 `api/`：HEAD `12c6884062d879bbe11344261f85d5cc3285bb94`，tree `de8387d6b504b39e7b2f1564a37a667a70787586`。
- 上述为源码定位，非本轮重新部署或移动浏览器验收证据；源码存在不等于线上链路已经实测通过。
- 前序只读查询：正式悬赏 #394「移动竖屏全流程测试-20260923021001」为 `assigned`，负责人扈三娘，startedAt/completedAt 均为空。
- 私人交办「移动竖屏全流程测试-20260923021001-需求」是另一对象，执行者吴用，已有 `OUTPUT_COMMITTED` 与 PDF、已查看/收入案卷标记。名称相近不能证明业务关联。
- 因而此前“悬赏全流程闭环”结论不成立；#394 停留点将阶段的具体运行时原因尚未定位，不推断为一定没有派发代码。

## 1. 正式悬赏主状态：后端 10 个，悬赏榜只映射 6 个

| 原始状态 | 当前榜单文案 | 建议文案 | 语义/注意点 |
| --- | --- | --- | --- |
| open | 待点将 | 待点将 | 已张榜，等待安排负责人；不是未提交草稿 |
| planning | 缺失，回落为待点将 | 筹划中 | 状态机声明存在；具体可达入口需进一步验证 |
| assigned | 已点将 | 待开工（已点将） | 已安排负责人，不证明开始执行 |
| running | 在办 | 办理中 | 当前聚合也包含 claimed、返工待领取，并不等于模型正在运行 |
| reviewing | 缺失，回落为待点将 | 待验收 | 正式提交后等待用户决定 |
| blocked | 缺失，回落为待点将 | 受阻 | 可恢复阻塞，需显示原因和下一步，不应只显示失败 |
| completed | 交令 | 已完成 | 必须额外展示完成依据；兼容路径并不一定有正式验收 |
| failed | 失手 | 失败 | 不与可恢复阻塞混淆 |
| cancelled | 缺失，回落为待点将 | 已取消 | 不是成功，也不等于归档 |
| archived | 入档 | 已归档 | 当前是主状态终态；应保留归档前结局 |

直接证据：前端 `src/constants/juyiting.js:17`、`src/components/world/JuyiHall.vue:959`；后端 `agent/jia-agent-core/src/main/java/cn/jia/agent/state/AgentTaskStatus.java`。

统计接口虽然只预置 6 个零值，但会把实际查询到的其他状态加入 counts，不能说后端只统计 6 个。前端需统一覆盖全部状态及零计数。

## 2. 声明状态图与实际写入路径不能混为一谈

### 枚举声明

```text
open → planning / assigned / cancelled
planning → assigned / cancelled
assigned → running / blocked / cancelled
running → reviewing / blocked / failed / cancelled
blocked → running / failed / cancelled
reviewing → running / completed / failed / cancelled
completed / failed / cancelled → archived
```

这不是所有写入入口共同强制执行的一张图：聚合器、正式提交/验收、legacy report、资金结算分别有写路径。

### 正式交付链路（已读实现，目前 submit 限 exactly one required work item）

```text
任务 running + 工作项 running + 有效执行 lease
  → 提交固定成果版本/摘要
  → delivery=submitted，工作项=submitted，任务=reviewing
  → 用户验收通过
  → delivery=accepted，工作项=completed，任务=completed

用户要求修改
  → delivery=changes_requested，工作项=ready，任务=running
  → 明确创建返工/重新领取执行（不是点击要求修改就自动调用模型）
  → 新 delivery，revision + 1，supersedesDeliveryId 指向旧交付
  → 再次 reviewing → accepted/completed
```

前端已有“查看正式成果与验收”，有“验收通过”“要求修改”和满足固定版本条件的“明确交给 Agent 返工”。不能再说没有验收入口。入口存在不代表 #394 已经到达该节点。

### 聚合实际规则

- 保留 operational terminal。
- 无必需工作项时，可选项 claimed/running/submitted 可触发 running；否则保留。
- 必需项 failed/blocked 且次数耗尽：failed。
- 全部必需项 completed 且有 resultArtifactId、有效 completedAt：completed。
- 全部必需项 submitted/completed：reviewing。
- 有可恢复的必需项 blocked：blocked。
- 有 claimed/running/submitted/completed 项：running。
- 返工 ready 阶段可保留/回到 running；assigned 保留；已有成员可归为 assigned。

聚合器并未在此写入位置调用主状态枚举的 canTransitionTo。其“已验收完成”判断实际检查的是工作项字段，不是逐项查询正式验收记录。

### 两条兼容/特殊完成路径

1. legacy report 支持 running/completed/failed。completed 可把兼容工作项从 ready/running 直接设 completed，生成 legacy result 标记并聚合；不能把该标记当作真实可下载成果或正式验收凭证。submitted、非 legacy lease 等仍受协议隔离，不能绕过。
2. funded preview 的结算入口允许满足资金/认领/报价等校验的 assigned/running 任务在 capture 成功后直接 completed，同时 funding=SETTLED。这是特殊结算路径，不代表全部悬赏采用正式验收完成。

建议最终统一“完成事实”规则，但先做各入口契约盘点和回归，不能直接把 canTransitionTo 硬塞到所有写路径导致兼容功能失效。

## 3. 必须区分的状态维度

| 层级 | 当前状态/标记 | 不能推导出的结论 |
| --- | --- | --- |
| 主任务 | 上述 10 态 | completed 不能无条件宣称正式验收通过 |
| 工作项 | pending → ready → claimed → running → submitted → completed；另有 blocked/failed/cancelled、返工与租约回收分支 | claimed 不是模型已开始；submitted 不是已验收 |
| 成员 | invited / accepted / working / done / blocked / rejected / failed / left | 点将/邀请不是执行完成 |
| 正式交付批次 | submitted → accepted / changes_requested | 分享文件不是正式交付；要求修改不是自动重跑 |
| 私人执行 | QUEUED / OUTPUT_STAGED / OUTPUT_COMMITTED / FAILED / INPUTS_REVOKED（各投影覆盖尚需核对） | 私人输出提交不能自动更新正式悬赏 |
| 个人整理 | 已查看、收入案卷 | 不等于验收，不等于停止执行，不等于主任务 archived |
| 资金 | 如 FUNDS_HELD / SETTLED | 不应仅凭任务文案推断支付/结算事实 |

工作项精确转移：pending→ready/cancelled；ready→claimed/cancelled；claimed→running/ready/cancelled；running→blocked/submitted/failed/cancelled；blocked→ready/failed/cancelled；submitted→completed/ready/cancelled；其余终态。

主任务归档接口目前只允许 completed/failed/cancelled→archived，重复归档幂等；不能把 assigned 归档当作闭环补救。

## 4. 已确认的展示问题

1. 缺失状态回落为“待点将”，把流程后段显示为起点，属优先修复项。
2. completed 名为“交令”，混淆提交动作、待验收、验收完成；建议“交令/提交成果”留作动作名。
3. assigned/running 太粗：用户看不出等待领取、已领取、实际执行、返工待启动及下一步责任人。
4. 私人事项头部只要存在 execution 就固定显示“已受理，尚未取得成果。”，OUTPUT_COMMITTED 时也如此。
5. OUTPUT_COMMITTED 显示“已有已归档输出”，把技术持久化与用户“收入案卷”混淆，建议改“成果已生成”，整理标记另列。
6. 聚合支持多工作项，但正式提交当前限制一个必需项；不能宣称多人多交付验收已完整跑通。未来多项执行时，局部待验收应显示独立待办，不能只等主状态 reviewing。

## 5. 建议优化顺序（尚未实施）

### P0：纠正事实展示，不改存量业务状态

- 状态文案/样式/筛选共用一份完整映射；未知值显示“状态待核对”，不回落 open。
- 显示办理中、待验收、已完成；历史 completed 根据证据另标“正式验收通过/历史兼容完成/预览结算完成/完成依据待核对”。不能伪造历史验收。
- 私人执行头部与明细共用状态解释；OUTPUT_COMMITTED 与个人归档分开。
- 明确标识“正式悬赏/私人交办”，详情展示真实 ID，仅通过显式关联键跳转，不按同名拼接闭环。

### P1：让用户知道在等谁、下一步做什么

- 主用户流：待点将 → 待开工 → 办理中 → 待验收 → 已完成；筹划、受阻、失败、取消为对应分支。
- 不必增加一堆主状态：卡片增加子阶段、等待对象、最近真实事件、下一步动作。
- 点将后核对派发→接收→领取→开工→产物→正式提交→验收；#394 用已有 ID 排查，不先制造另一条同名任务。
- 要求修改后明确提示“已退回，尚未启动返工”，启动付费执行保持明确动作和幂等核对。
- 运行很久只提示耗时/最近进展，不按任意 SLO 自动失败或取消。
- 移动竖屏采用“全部/进行中/待我处理/已结束”分组及次级筛选；个人案卷单列，主状态仍完整可见。“待我处理”是待办视图，可与主状态交叉，不新增伪主状态。

### P2：收敛领域契约

- 在 owner/tenant/client、事务、CAS、lease、幂等边界内统一完成依据和事件，兼容路径显式标记来源。
- 资金状态独立显示；是否以正式验收作为结算前置需专项确认，不能只改标签。
- 评估把归档移为独立属性、保留完成/失败/取消结局；涉及迁移分阶段设计，本轮不修改历史数据。

## 6. 后续验收标准

实施后在 430×932 移动竖屏真实 UI 验证：

- 10 态及未知态展示、筛选/统计完整一致。
- 同一正式 taskId 点将→领取/开工→固定版本交付→待验收→验收通过→已完成；另测要求修改→明确返工→新 revision→再验收。
- 下载/预览可验证交付件；时间线与服务端状态一致；刷新/重进仍保留事实。
- 覆盖受阻恢复、失败、取消与终态归档；不绕过 lease、跨用户权限或资金授权。
- 私人交办另测成果已生成→已查看→收入案卷，绝不替代正式悬赏验收。
- 源码/发布证据与 UI 证据分开记录；没有上述同一任务证据不得报告“正式悬赏全流程已跑通”。

## 源码索引

前端路径均相对于本次检查 worktree：
- `src/constants/juyiting.js`
- `src/components/world/JuyiHall.vue`
- `src/components/juyiting/BountyPanel.vue`
- `src/components/juyiting/HallDraftEditor.vue`
- `src/components/deliveries/FormalDeliveryList.vue`

后端主状态位于 `api/agent/jia-agent-core/src/main/java/cn/jia/agent/state/`。
后端实现位于 `api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/`：
- `AgentTaskAggregationCalculator.java` / `AgentTaskAggregationServiceImpl.java`
- `AgentTaskFormalDeliveryServiceImpl.java` / `AgentTaskFormalDeliveryDecisionServiceImpl.java`
- `AgentLegacyTaskCompatibilityService.java`
- `AgentServiceImpl.java`（统计、点将、report、归档）

资金特殊路径：`api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/funding/FundedBountySettlementServiceImpl.java`。


## 7. 自动触发核验补充（2026-09-23T15:48:36+08:00）

用户追问“Agent／系统是否确定能正常触发”后，本轮仅做线上只读查询与源码追踪，未发送执行命令、未调用 Provider、未改任务状态。

- GET `/agent/tasks/394`：HTTP 200，status=assigned，startedAt/completedAt 均 null，taskVersion="0"，actionDispatchResults=null。
- 任务描述原文：“移动竖屏功能测试：验证非资金悬赏的点将与议事入口；无实际业务执行要求。”这条任务不能作为真实执行和验收全链路的成功证据；该描述也不能单独解释为什么未执行。
- GET `/agent/tasks/394/formal-deliveries`：HTTP 200，items=[]。
- 负责人只读详情显示 online，但 currentTaskId/currentTaskTitle 为空；在线不证明领取或执行成功。
- 携带正确 actorAgentId 的 GET `/agent/tasks/394/workspace`：HTTP 503，TASK_WORKSPACE_UNAVAILABLE。
- 携带正确 actorAgentId 的 GET `/agent/tasks/394/events`：HTTP 503，TASK_EVENTS_UNAVAILABLE。
- 首次 events 查询因缺少必填 actorAgentId 得到 400，属于本次诊断请求错误；读取 Controller 契约补齐参数后才得到上述 503。不可把首次 400 当产品故障。
- 源码存在点将后的 TASK_INVITE 派发、客户端命令处理及回报实现；是否走持久 outbox 受 gate 控制。源码存在不能证明 #394 命令已送达、被领取或完成回写。

结论：此前“Agent／系统触发”只是实现职责说明，不是线上可用性保证。目前没有证据确认正式悬赏自动流转正常，也不能据此断言所有自动流转都坏了。由于事件和工作空间查询不可用，尚未定位 #394 的具体断点。下一步先定位这两个 503 并恢复可观察证据，再核验同一正式任务的命令送达→领取/开工→成果提交→用户验收，不能手动改状态伪造通过。


## 8. 测试 Agent 范围调整（2026-09-23 用户指令）

- 后续正式悬赏执行测试仅使用吴用或林冲；用户说明这两者的 codex-ws-agent 才是最新版本。测试前核对实际运行版本与对应 Agent ID。
- 主测选吴用，必要时用林冲对照；不再向扈三娘发送测试任务、重新派发或调用 Provider。
- #394 保留为历史观察记录，不将其在扈三娘上的结果用于判断最新版客户端是否可用，也不擅自改派、取消或归档。
- 继续沿用 430×932 移动竖屏真实 UI 验证；正式悬赏与私人交办分别记录，不混用完成证据。


## 9. 吴用正式任务复测与 bugfix 需求

2026-09-23 已按用户指令改用吴用，移动竖屏真实 UI 新建正式悬赏 #395「吴用竖屏闭环复测-0923-1600」。指派记录成功但派发 queued，榜文议事两种会话入口均 404；资料上传仅完成个人文件入库，workspace/events 503，无正式交付。未闭环、未改应用代码/发布。六项需求与验收矩阵见 `specs/juyiting-formal-flow-bugfix-20260923/`，证据见 `deliverables/verification/juyiting-formal-flow-wuyong-20260923/manifest.json`。该复测替代以 #394 判断新版客户端的做法，不删除或改写旧失败证据。
