# 开发计划与拆分

> 当前用户交互以 [普通请求与统一动作合同](ordinary-request-actions-v3.md) 为准：四步完成，不设图片专用“受控请求”或确认链。历史冻结合同不作为新界面流程；完整发布验收仍未完成。

> **2026-10-04 新方案源码进展**：[通用点将合同](generic-point-and-deliberate-contract-20261003.md)。Webe3ceaec已取消新请求绘图前置并自动接入CHAT；API78f61531 / Client1ab2b66已统一INPUT/REFERENCE32资料查阅及回执。Web287定向+14组件、API64、Client32自检通过；仅特性分支，未发布。按需查阅/执行自动编排、失败恢复和完整验收仍待完成。

> **2026-10-03 最新实施指令**：用户明确“无需做太多兼容补丁，一切都按新方案实施”。新入口、新请求统一走通用资料与按需议事；不新增旧生图入口、双轨产品流程或回退适配工程。只保留身份隔离、幂等、未完成请求及既有内容保护，不以历史兼容覆盖率阻塞新方案。

> **2026-10-03 用户纠偏（当前优先）**：[通用资料详设增量v3](unified-materials-correction-20261003.md)取代独立参考图入口及图片限定业务流程。唯一“添加资料（可选）”须支持图片/文档/音频等；Agent判断用途，通用会话、输出、保存与交付保持完整范围。不是文案改名；绘图专用wire仅作为执行适配，不扩展旧产品入口，原34项需补UM01–UM10。API6a855通用创建30定向PASS；Web43645已统一Overview/Bounty资料选择与v2创建104定向PASS。通用点将前后端/首轮分派和资料查阅协议已完成本轮源码自检；自动查阅/执行编排、失败终态、恢复与整体验收仍待完成，未发布。

> **2026-09-28 最新计划**：[融合实施计划v2](fusion-implementation-plan-v2.md) 优先于本文的未开始/外部F0等待描述。本轮已启动feature代码整合，后续多媒体业务包仍待实施；唯一运行台账不变。

日期：2026-09-27。状态：planned / not started；本次仅计划，不派发 Writer、不创建独立 Reviewer、不修改运行台账。以下 Owner 为建议职责，不代表已领取；实际执行仍只登记 `/home/isp/wsps/cyf/docs/implementation/TASKS.yaml#runtime_ledger_json`。

## 1. 推进策略

当前先冻结通用资料与按需意图合同，统一需求/议事资料入口及真实服务端快照，再完成跨类型Agent处理、终态/媒体/归档/交付联调；工作包以增量v3的M1–M5为准。保留已有图片适配器，不再以“先做画鸟、以后补通用资料”作为产品发布顺序。不承诺未经实施基线测算的人天、版本号或发布日期；M0 依据已复用代码和所需迁移给出估算。

### 依赖图

```text
F0 原分支整改 ─────────────┐
                         ↓
M0 合同 → B1 资产存储 → B2 点将/执行 → B3 归档/验收 ─┐
   ├──── R1 Runtime ──────┘                         ├→ I1 图片纵切
   └──── W1 素材入口 → W2 混排/保存/验收 ────────────┘
                                  W3 音频/文本补齐 ─→ I2 完整回归 → R0 发布准备
```

F0 和 M0 可并行沟通；W1/W2 可在候选合同下做 mock，B1 可独立开发；真实 B2/I1 联调必须使用已修复基础。不同 worktree/路径归属可以并行，不做全局写锁。

## 2. 工作包

| ID | 建议 Owner / 仓库与路径边界 | 工作内容与交付 | 依赖 | 最小自检与完成条件 |
| --- | --- | --- | --- | --- |
| F0 | 原开发；API/Web/Client | 解 6/2/1 内容冲突、F1–F4、MySQL 与 JWT 兼容；交回 exact commit/tree | 独立外部依赖 | 身份、逐目标能力、冷线程/宋江、INSPECT、START/重连回归；不只消文本冲突 |
| M0 | API Owner（critical_worker）+ 各组件合同代表；SDD 本 feature | 冻结 DTO/wire/events、schema/索引、任务会话映射、晋升授权、格式矩阵、测试夹具；补合同案例 | 当前文档 | design.md 第 10 节关闭；接口方法/错误/幂等与旧兼容清楚，确认最小 DDL |
| B1 | API Owner（critical_worker）；agent workspace/storage | 会话资产用途、输入精确授权、内容读/Range、output commit 与保留引用 | M0 | 不自动创建个人文件或正式交付；跨 owner/版本/路径穿越/重复提交和迁移测试 |
| B2 | API Owner（critical_worker）；task/chat/执行桥接 | 点将 outbox/唯一议事/首条投递、上下文快照、turn-execution-part、模型意图授权、事件恢复 | M0、B1、F0 | 点将局部失败/重复、冷线程/资料、文本 final 后媒体、重指派/取消竞态测试 |
| R1 | Client Owner（balanced_worker，合同冻结后）；`conf/codex-ws-agent/` | CONVERSATION wire、未归档资产输入、工作目录提示/校验、输出回传关联、能力广告 | M0；B1 可 mock | server/local 共用夹具；native START 先于 Provider；声明外文件不可读写/上传；旧 PRIVATE/TASK 回归 |
| B3 | API Owner（critical_worker）；归档与正式交付协调 | 文字选区/资产保存、CAS 新版本、选定集合晋升、正式提交/用户验收/领域完成 | M0、B1、B2 | 保存失败不重生成；保存与验收独立；受信生产者/用户身份、事务及部分成功恢复 |
| W1 | Web Owner（balanced_worker）；需求入口/空间选择器 | 统一添加资料（可选）、显式目标、通用点将自动导航及真实 bootstrap 状态 | M0 | 无参考资料可提交，资料版本/移除/草稿保留；地图与名册数据流不混淆 |
| W2 | Web Owner（balanced_worker）；议事消息/reducer/操作面板 | parts 混排、图片预览/下载、执行状态、同会话引用、归档与最终清单 | M0、W1；B1–B3 可 mock | 乱序去重、旧消息、认证过期/身份切换、取消、晚到媒体、不误报完成 |
| W3 | Web + API 格式负责人；媒体组件/格式策略 | 音频播放/Range/下载/保存、文本选区、普通文件预览降级、混排与移动端 | B1、B3、W2 | 不以图片通过替代音频；MIME/鉴权/保存真实字节；不把播放能力冒充生成能力 |
| I1 | 集成 Owner + gpt_test_runner | 浏览器“无参考画鸟→改蓝色→保存/不保存均可验收”及“有参考”纵切 | F0、B1–B3、R1、W1–W2 | AC01–07、AC10、AC12–17、AC22 的图片范围；真实目标 Agent，完整 ID/摘要证据 |
| I2 | 集成 Owner + gpt_test_runner | 全 AC 覆盖：双接应、媒体、隔离、冷恢复、多端并发、离线读取、旧协议 | I1、W3 | acceptance.md 22 项记录实际结果；未完成不标 accepted |
| R0 | 实施 Owner | 当前发布政策下准备精确版本、迁移/兼容顺序、测试及制品摘要、线上验收 | I2 及实际发布授权 | 不伪造 Flow；当前文档阶段不触发；源码/部署/用户验收分别记录 |

M0/B1/B2/B3 有相邻 Java 路径时由同一 Owner 或显式串行交接避免交叉写；Web W1/W2/W3 默认同 Owner，只有文件归属不重叠才并行。不调度 DeepSeek，不恢复 sol_reviewer 独立审查。

## 3. 影响范围与保护项

| 区域 | 规模判断 | 必须保护 |
| --- | --- | --- |
| API chat/task | 中到大 | 服务器身份、可信材料、durable request/turn、既有任务规则/宋江 |
| API agent/workspace/delivery | 大，关键路径 | owner/client/tenant ACL、内容校验、run/lease/producer、PRIVATE/TASK、正式提交/验收 |
| Web | 中 | 普通聊天兼容、地图/名册分离、显式点将目标、身份切换清理、移动端草稿 |
| Client | 中 | 山寨安顿/自家接应、native START、独立 cwd、受控输入/输出、旧协议 |
| DB | 中，增量迁移 | 唯一键/CAS、重入与存量数据兼容，不历史文件大搬迁 |
| 运维 | 有限配置与验收 | 不换发布系统、不操作其他任务进程、不凭本机 profile 推断远端 |

## 4. 验证层级与证据

- 文档阶段：仅结构、引用、合同一致性与 diff 检查，不构建/部署。
- 实施单元层：DTO/wire 夹具、schema/事务/ACL、reducer、runtime 文件桥接；选最小相关集，证据绑定 tree SHA/selector/DB fixture digest。
- 集成层：实际 MySQL、API/Client 配对、旧新协议混用、授权和异步恢复。Gradle 一律经 `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py` 串行。
- 浏览器层：记录实际部署版本、任务/会话/消息/part/执行/run/asset/file/正式交付/验收标识，验证图片解码、音频播放、下载摘要。
- 发布层：遵循用户最新政策。2026-09-17 云效不可用时的本地授权覆盖历史 Flow-only；若本地构建须记录 build_origin=local_user_authorized、exact commit/tree/测试/制品 SHA-256，冻结 release 只在真实上线条件满足后执行。本次文档提交不创建 release。
- 生产数据、扣费、外部资料传输仅在明确已授权范围；历史测试账号凭据不写入仓库、日志或截图。

## 5. 主要风险与消解

1. 原分支未整改：可以做合同和独立切片，不分叉第二套 durable 引擎；F0 回填是联调前置。
2. 旧 PRIVATE 自动归档/TASK 自动交付：用显式新用途隔离，回归老语义，避免试稿误交付。
3. 正式提交生产者授权：M0 冻结最小受信适配器，不能通过删鉴权加快交付。
4. 冷线程缺上下文：数据库快照与精确资产领取，不能以 warm thread 一次成功作证明。
5. 音频/文本白名单及媒体鉴权：逐格式验证，不靠扩展名或裸 URL；不支持格式如实降级。
6. 重试重复收费/重复验收：稳定意图键、状态查询、分阶段恢复；404 不证明未受理。
7. 未归档产物误清理：引用生命周期明确前不新增自动 GC；已保存/正式成果不受会话删除牵连。

## 6. 交付出口

每包回填：变更范围、exact commit/tree、命令与结果、合同差异、风险/剩余项。完成功能后才更新 integration pins，不能拿 dirty checkout 运行 pin。当前所有包为计划，具体执行状态只在唯一运行台账登记，本表不是第二套运行 ledger。
