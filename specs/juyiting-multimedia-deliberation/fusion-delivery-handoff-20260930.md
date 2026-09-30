# 多媒体议事长期融合详设：交接与实施入口

日期：2026-09-30。特性名称：**聚义厅统一多媒体议事与受控交付**；feature ID：`juyiting-multimedia-deliberation`。

本文件是本次分支/文档交付的只读状态补充，不改变冻结的 API、wire 或验收合同，不是运行台账。完整详设以[融合详设 v2](fusion-detailed-design-v2.md)为主，[UI/媒体/存储详设](design.md)补充，冲突时 v2 优先。**分支建立与 fast 代码融合已完成；完整产品尚未验收。**

## 1. 分支交付及远端核验

四仓均使用 `codex/juyiting-multimedia-deliberation`。本次重新 fetch 远端精确分支，以 `merge-base --is-ancestor` 核验当前 fast HEAD；四仓均已包含，无需重复 merge、重置或改写原 fast 分支。

| 仓库 | 本次核验 feature HEAD | 当前远端 fast HEAD | fast 已合入 | 当前 develop 独有提交数 |
| --- | --- | --- | --- | --- |
| SDD | `c880d56c0d4e6e0ba0b1d79030ac8550c7af1f7f` | `9f47e63e456a7965d954e6d1e645a083920d784e` | 是 | 1 |
| API | `b1e7b06817f041804f1e1d613ff4aa280641e904` | `caee54fc27a08146f9cc57219cf86c763e41c531` | 是 | 3 |
| Web | `7ac3bbc3fd21bfb1b053a8fbe249cc2b17d42a1d` | `96838f17fc24fbf21781be39476aa9723dee3a2c` | 是 | 4 |
| Agent Client | `0d4224e2dbbe52788a69be0cb0844f0ad743c6b2` | `68dbe8992a56c8e1041056a9123b1156d1d2b35e` | 是 | 0 |

完整 tree、远端 develop SHA、核验时间见[可复核快照](fusion-branch-handoff-verification-20260930.json)。SDD SHA 是本次文档提交前的核验点，包含本文的提交另由 Git 历史确定。

**已合入 fast 不表示已包含最新 develop。** develop 独有提交须在后续集成前按实际差异补齐及定向回归；本次不顺带合 develop、不改组件研发 pin、不发布。历史融合冲突处理与测试范围保留在[初始整合回执](integration-baseline-20260928.md)，不把旧结果改写成新测试通过。

## 2. 长期架构：一个产品、多个受控运行策略

```text
需求原文 + 可选精确资料版本
       ↓ 显式目标 Agent / 点将并办理
assignment + grant + 唯一 bootstrap/outbox
       ↓ 同一悬赏议事 / 同一 durable request、turn、事件体系
权威上下文 + 按需路由
       ├─ 进度查询：读事实，不生成
       ├─ CHAT：讨论/澄清，轻量上下文，不挂载执行目录
       ├─ INSPECT：本轮指定资料，受权只读
       └─ EXECUTE：本次授权操作、输入、run/lease、输出提交
                     ↓
            持久 conversation asset + message parts
                     ↓
          实时展示 / 预览下载 / 继续讨论和修改
                     ├─ 用户选择 → 保存个人空间
                     └─ 精确成果集合 → 正式交付 → 验收 → 任务完成
```

- `fast-deliberation` 长期保留为 CHAT 运行策略，不作为独立聊天产品；`multimedia-deliberation` 是同一会话的媒体/办理能力。
- 每轮不默认加载全部资料、全部工具；附件目录元数据不等于已读图片。分别记录 availableRefs 和 materializedRefs。
- 已明确且已授权的“画一只鸟”可直接执行；必要时才澄清，不强制先问 fast 模型，再问执行模型。
- 旧 `/chat/stream`、fast-v1 EXECUTE=false 保持边界。新的 native 执行声明与服务端准入另行证明，不借聊天提示词或 execute hint 提权。
- 同一会话不等于同一模型线程：线程按身份/目标/profile隔离，平台持久快照为事实源。严格 no-tools 必须有实际引擎证据，不能仅由 sandbox/approval 配置推断。

这是长期领域设计；只有 legacy 协议适配是过渡措施。退出适配须证明支持客户端迁移、旧在途请求处理及回放恢复，不按任意日期删除。

## 3. 用户流程与实现职责

| 用户动作 | 权威实现 | 不可混淆的事实 |
| --- | --- | --- |
| 提“画一只鸟”，可选参考图 | 固定需求 revision、空间文件版本/摘要和任务资料关联 | 选择资料不是全空间读取授权 |
| 点将并办理 | 目标能力协商 + task/grant/assignment + outbox | grant 不是 TaskDTO；允许操作集合不是首轮动作 |
| 自动新增/进入悬赏议事 | 采用服务端确切 conversation/initial request，加载历史与事件 | 不由浏览器再发一遍首轮需求 |
| 生成或澄清 | 服务端授权/费用/资料检查；执行或保存澄清关联 | 能力 READY 不等于已获费用许可 |
| 实时看图片/音频/文件 | 文本增量、执行状态；完整媒体提交验证后 part.ready | 不承诺逐像素生图；本机路径不是交付件 |
| 不满意继续补充/修改 | 同会话新明确意图，绑定上一稿 asset/revision | 重试/刷新不创建第二次收费执行 |
| 保存到工作空间 | 源读取权 + 个人空间写权限，精确快照幂等归档 | 未保存成果仍持久可读；归档不自动验收 |
| 确定完成并验收 | 固定最终集合；正式提交/验收/完成分阶段恢复 | OUTPUT_COMMITTED 不等于 task.completed |

完整用户验收保持图片、音频、文本、文件范围，不因当前图片纵切而缩窄。照片式鸟图须按需求实际生成/提交，可预览且下载真实字节；不能以 mock 图、Markdown 外链、生成成功自述代替。

## 4. 一份内容，三种用途与双接应目录

**共享的是不可变内容身份与来源，不是三种用途的权限，也不是要求共享一个物理挂载。**

```text
不可变内容引用（摘要/MIME/长度/实际私有字节）
  ├─ 会话 asset/message part：会话 ACL
  ├─ 个人 WorkspaceFileVersion：用户主动保存，个人 ACL
  └─ 正式 ArtifactVersion：用户选定，任务/验收 ACL
```

复用现有 `workspace-private` 与 `task-artifacts-private` 两个私有存储根；必要的正式交付复制校验同一摘要，不新增第三套文件系统、不做跨 owner 物理去重。示例部署路径和配置原则见原详设第3节；实际位置以运行配置为准，不由文档硬编码。

山寨安顿/自家接应每个 Agent 都保留自己的配置根；每次执行另建 run 隔离的 `inputs/outputs/scratch`。平台下发精确受权 manifest，客户端领取、验摘要并物化 inputs；提示词说明本次可读路径及输出约定，客户端/服务端负责权限、START fence、上传及 commit，**提示词不是授权和成果提交机制**。不向 Agent 暴露平台绝对私有目录，不扫描客户端全部工作目录认领产物。

双接应使用同协议，各自声明真实能力；一个客户端就绪不能推断另一个也就绪。执行目录只是临时加工区，平台资产才是可跨客户端预览、下载与归档的持久事实。

## 5. 详设施工入口及影响范围

| 内容 | 权威文档/合同 |
| --- | --- |
| 整体长期决策及适配退出 | [长期融合方案](long-term-fusion-plan-20260928.md) |
| admission、grant、路由、上下文、状态/恢复 | [融合详设 v2](fusion-detailed-design-v2.md) |
| UI、多媒体 parts、资产、存储、归档、验收 | [媒体详设](design.md) |
| 现有码/表/端点映射 | [M0 源码映射](m0-source-mapping-and-contract.md) |
| 页面点将与首轮采用 | [入口详设](point-and-start-entry-design-v1.md)、[原操作只读恢复](assignment-operation-read-contract-v1.md) |
| 首轮动作与多操作 grant | [初始动作合同](initial-operation-contract-v1.md) |
| 原生声明、当前session与只读协商 | [原生能力合同](native-bounty-capability-contract-v1.md) |
| 精确成果与验收恢复 | [finalization 合同](finalization-contract-v1.md) |
| Owner工作包、依赖、验证 | [融合开发计划](fusion-implementation-plan-v2.md) |
| 34项产品验收 | [验收 AC01–AC22](acceptance.md) + [详设 FD01–FD12](fusion-detailed-design-v2.md) |

影响四仓：SDD 定义合同/基线；API 的 task、chat、agent、workspace、delivery 负责领域协同；Web 的需求/点将/会话/媒体/归档/验收组件负责体验；Client 负责能力、精确输入、执行和上传。属于跨仓功能增量，不是整个聚义厅重写。不更改 map/roster 分流、显式 Agent 点将不变量，不顺带重构资金榜、多Agent流程、钱包或另建存储服务。

## 6. 开发顺序与给 Agent 的指令

1. 在冻结 native 合同下完成 API/Web/Client 能力协商及实际点将页面接线；原键恢复永不 legacy 降级。
2. 补真实参考图选择/任务关联/精确版本回读，以及合法费用授权桥；无授权不调用付费 Provider，不挪用悬赏 escrow/hosting/skill 等用途凭据。
3. 补同会话澄清续办、上一稿引用/EDIT/派生资产；仅广告实际支持的操作。
4. 完成保存、正式提交/验收/领域完成真实联调，以及文本、音频、文件和混排。
5. 补齐当前 develop 独有改动，按 exact SHA/tree/selector/fixture 验证双接应、恢复、迁移及全部产品范围；达到条件后再按发布政策推进。

可直接交给实施 Agent：

> 在本仓 `codex/juyiting-multimedia-deliberation` 的独立 worktree 上，先阅读本 feature README、融合详设v2及对应冻结合同。只领取一个有明确路径边界和依赖的工作包，保留 fast 轻量权限边界及既有 PRIVATE/TASK。实现时复用持久请求/事件和平台资产，固定身份、资料版本、原幂等键、grant/assignment/lease；不得重发首轮或以提示词授予权限。Owner自检并交付 exact commit/tree、实际定向测试、DB fixture digest（适用时）与剩余缺口。Gradle 经 orchestrator；不创建 Reviewer，不改他人脏文件，不部署、不迁移真实库、不调用未获授权的付费 Provider。

性能目标只作观测及优化排序，不依据时延SLO拒绝/取消下一步。真实鉴权、事务、幂等、锁归属、明确传输超时和用户取消仍保留。

## 7. 本次交付结论与未完成事项

- **已完成**：四仓同名 feature 分支、fast ancestry 与远端 HEAD 重新核验、长期方案/详设/实施计划及本交接入口。复用此前精确源码的定向证据，本次不重复跑未变源码测试。
- **尚未完成产品验收**：native能力/真实页面组合、完整参考图、合法费用授权、澄清/EDIT/派生输入、双接应/真实 Provider、完整浏览器流程与发布。能力声明或局部schema/单测通过不能关闭这些项。
- **本次未执行**：develop合入、生产构建、部署、生产数据库迁移、付费调用或画鸟浏览器验收。34项产品状态不改 PASS。

状态详见[集成清单](integration.yaml)。运行推进仍只使用 `docs/implementation/TASKS.yaml#runtime_ledger_json`；本文不新增 Owner/运行门禁台账。
