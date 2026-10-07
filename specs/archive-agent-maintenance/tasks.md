# 实施工作包与推进计划（D2）

日期：2026-09-28。状态：**D2 历史 WBS；当前 implementing / NOT_COMPLETE，源码补缺见 completion-audit.md，上一轮局部 pins 与验证范围见 delivery.md / integration.yaml**。本文件保留工作包和依赖设计，不作为实时执行台账。当前局部源码、测试证据与剩余缺口见 [implementation-baseline.md](/home/isp/wsps/cyf/specs/archive-agent-maintenance/implementation-baseline.md)，机器状态见 [integration.yaml](/home/isp/wsps/cyf/specs/archive-agent-maintenance/integration.yaml)，原始证据见 [evidence/2026-09-30](/home/isp/wsps/cyf/specs/archive-agent-maintenance/evidence/2026-09-30)。84 项业务验收仍全部未执行。

## 1. 工作包

| ID | 产物 / 责任建议 | 范围与主要文件 | 依赖 | Owner 自检/验证 | 粗估人日 |
| --- | --- | --- | --- | --- | --- |
| M0 | 基线与合同 / 主 Owner | 冻结 API/Web/Client exact SHA；真实 schema、runtime 身份模式、锁/事务边界；统一执行/安装适配映射与平台安装 proof；API DTO/JSON 测试向量；共享 Owner 接口确认 | 无 | 数据源/锁顺序/模块依赖明确；不从 dirty checkout pin | 1–2 |
| M1 | 通用内容与兼容迁移 / critical_worker | archive core/api/mapper/service；schema 版本桥接、通用 manifest、published resolver、旧种子不夺指针、私人数据/提问通用化 | M0 | 旧版全部摘要不变；非 120 回/无序言 fixture；旧 API 契约 | 4–6 |
| M2 | 任职/权限 / critical_worker | archive 管理授权/appointment；agent-api 身份 port 与 agent-service 适配；native 方法路径 ACL | M0 | owner/client/tenant/binding/runtime/Agent 隔离；撤任竞态 | 3–5 |
| M3 | 平台技能配置 / critical_worker | agent 平台安装记录与命令；安装器安全复用、包目录与证明；不写经济资金表 | M0 | 新旧安装 origin 隔离、摘要/回执/重放、市场关闭也可配置 | 2–4 |
| M4 | 维护作业与发布事务 / critical_worker | archive job/执行关联/draft/operation/publication/业务 outbox；管理/native API；幂等/恢复/发布 CAS | M1、M2 | 宕机点/数据库事务、撤权/并发、READY 不公开 | 3–5 |
| M5 | 来源与内容处理 / balanced_worker（涉及 ACL 归 critical Owner） | 来源快照/固定适配器、技能脚本和 schema、服务端校验规则；不任意抓取 | M0、M1；接入 M4 合同 | 源字节→段落完整映射、跨语言摘要测试向量、恶意文本 | 2–4 |
| M6 | Client 典籍执行 bridge / balanced_worker | `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/`；新命令、安装事实、固定 origin、断点恢复 | M2、M3、M4、M5 的合同 | 伪造上下文/跨 job、重复命令、重连、老客户端行为 | 3–5 |
| M7 | 宋江与直达入口 / critical_worker + bounded integration | ChatClient 工具装配、可信协调上下文、三项工具、直达受理、唯一请求意图 | M2、M4 合同 | 无管理员用户不能借工具发布；shell/URL 旁路不可用 | 2–3 |
| M8 | Web 书架/维护 / balanced_worker | 指定基线 reader/LibraryPanel；新增任职、维护单、草稿、版本页；独立管理面板与会话卡（不改 ItemRef） | M0 API 冻结后 mock 开发；M1/M2/M4/M7 联调 | 真实 createApi→fetch，CORS/ETag/幂等；身份切换、横竖屏 | 3–5 |
| M9 | 全链路/故障验收 / gpt_test_runner，Owner 修复 | acceptance 矩阵、隔离 DB、API/Web/Client 合同、授权真实底本 E2E | M1–M8 | exact tree+selector+fixture digest；不把 mock 结果当生产闭环 | 3–5 |
| M10 | 集成/发布/授权激活 / 主 Owner | 升级桥接/迁移/Client/API/Web 顺序、同来源制品、首任管理员/任职/来源固定/上架 | M9；必要业务授权 | 实际健康、版本/摘要、在线阅读/私人数据/角色隔离 | 1–2 |

合计 **27–46 研发人日**，按 1 人日 6 小时有效投入为 162–276 小时，仅用于比较工作量，不是 Agent 持续运行时间或上线承诺。估算假设：复用已有存储/传输/阅读器，第一版只一种明确文本底本，不新增支付与 OCR，平台安装 proof 不需另建认证平台；M0 发现假设不成立时按具体差距重估，不以此数值设任务时限。

## 2. 最小可用增量

### A：先把内容域打通（M0/M1 + M2 管理授权子集 + M4 内容部分 + M5）

管理者可通过受控管理 API 完成一部 fixture 书的导入、发布、阅读和私人数据；没有 Agent 任职时不宣称“宋江已能办”。用于验证通用化不是只有书架改 UI。

### B：打通吴用实际执行（M2/M3/M4/M6）

真实安装、任职、精确 runtime、作业恢复；先 DRAFT_ONLY 交付，再验证显式 AUTO 授权。平台收费开关关闭时仍可验证平台配置技能，不做真实扣费。

### C：打通宋江/直达与聚义厅体验（M7/M8）

自然语言意图 → 唯一维护单 → 吴用执行 → 回执 → 阅读入口；权限不足/来源缺失/离线均有真实状态和单一下一步。

### D：授权《三国演义》实际上架（M9/M10）

来源、管理者、目标 Agent 和发布范围必须明确；源码测试通过不替代这些业务授权。用户验收包括新增书与旧水浒阅读、进度/书签/手札/选文、撤任与断线恢复。

## 3. 并行及路径所有权

- 并行度由可分离路径、显式依赖和当前资源决定，不新增任意两个 Writer 上限；不以工作包数量机械派发同等数量 Agent。
- 建议后端 P0 Owner 串行处理相互耦合的 M1/M2/M4，另一 Writer 在合同冻结后做 M8 或独立 client/技能脚本；同一时段不可修改重叠 `ChatClientConfig`、native filter、schema/init 或同 client 核心入口。
- M3 和 M6 都涉及 client 安装/命令入口，按文件划界或明确交接，不在同一工作树竞写。
- M5 scripts/fixtures 可与后端事务层并行；服务端输入权限不能由普通脚本 Writer擅自实现新认证方案。
- 每个工作包一个 implementation Owner 自检，不创建独立 Reviewer/release_guard，不等待历史审查队列。
- 当前工作区已有修改，不从此处直接实施；启动时先检查聊天附件，复用适合的干净/已妥善处理工作树，必要时使用 managed create_worktree。不得覆盖用户或其他任务成果。

## 4. 验证与证据要求

- D2 设计交付轮只做 L0 文档检查；此后已产生局部组件测试/build 证据，当前结果以 implementation-baseline.md 与 evidence/2026-09-30 为准，仍不等于业务验收。
- 实施时测试选择以 nearest build.gradle 为准，所有 Gradle 经 `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py`，不得并行 Gradle。
- 正式测试/构建优先既有 Flow；本地授权例外有效期间遵守 `build_origin=local_user_authorized`、组件 develop 自检合入、exact SHA 冻结 release 分支、制品摘要与健康要求；不创建新 Flow 链路或伪 Run；应用部署仍遵守当前有效的 Asia/Shanghai 版本发布排期，普通内容上架不是应用重建部署。
- 测试证据按 tree SHA + selector + fixture digest 复用；原始结果/未通过项保持真实，不把“未执行”改成 PASS。
- 只有源实现与验证实际完成后才填 integration.yaml pins；只在用户授权的实际生产操作完成后记录 released。

## 5. 下一步可执行动作

源码实现、组件测试与有界 HTTP/JDBC/POSIX/Client fixture 的当前事实见 delivery.md / integration.yaml，历史 WBS 不改写成业务 PASS。当前先补独立审计确认的源码缺口：API 下架/版本/校验恢复 → 等待输入与任职/resolve-input及精确管理接口 → Web 完整管理体验 → 隔离 Runtime/真实 HTTP 开发验证 → 完整逐要求复核。当前有效串行 Writer 与独立只读复审安排以 AGENTS/MODEL_ROUTING.yaml 为准，不沿用本文件历史“不创建 Reviewer”安排。具体生产管理者、吴用身份、底本与公共发布用途/自动发布权限必须在业务激活前精确核对。不得因源码推送擅自部署或上架真实典籍。


## 6. 可执行的交接与依赖 DAG

```text
M0 → M1 ───────────┐
 ├→ M2 ───────────┼→ M4 → M6 → M9 → M10
 ├→ M3 ───────────┤       ↑
 ├→ M5（依赖 M1）─┘───────┘
 ├→ M8 DTO/mock → M1/M2/M4 集成 ─→ M9
 └→ M7 合同准备 → M2/M4 接线 → M8 会话卡 ─→ M9
```

合同冻结允许准备并行，不等于跳过运行依赖。M0 输出到本目录新增 `implementation-baseline.md`：API/Web/Client/root commit+tree、实际 schema/事务管理器、既有 execution/grant/transport/installer 映射、逐目标能力验证方法、锁顺序、API DTO/错误 JSON fixtures、共享路径 Owner 与接入提交、风险对应测试 selector。不要在本文记录会过期的任务执行状态。

| 检查点 | 必须具备的产物 | 可继续的范围 |
| --- | --- | --- |
| C0 / M0 | 可复现源码及上述映射；未接通能力如实标注 | M1–M5/M8 独立范围；聊天 adapter 缺口只约束 M7/有关 M6 |
| C1 / 内容域 | 旧 reader 回归；fixture 多书导入/校验/发布/读回；管理 ACL | 安装/任职/真实 Agent bridge 集成 |
| C2 / Agent 草稿 | 精确技能、runtime、grant；DRAFT_ONLY 到 AWAITING_PUBLISH；恢复不重跑 | 宋江和直达同意图接线；AUTO 负向/正向验证 |
| C3 / 端到端 | 双入口不重复；撤任/换绑/隐私发布/多客户端回归 | M9 总体验证与 M10 技术发布准备 |
| C4 / 发布及业务激活 | 测试制品绑定、兼容迁移/健康；真实管理员/来源/任职/付费边界授权 | 有权范围内激活和真实《三国演义》验收 |

每包交付最小内容：路径范围、exact commit/tree、增量 API/迁移合同、测试 selector+fixture digest+结果、已知缺口、下一依赖的接入点。后端 ACL/事务/迁移由 critical_worker Owner 自检；前端/客户端按冻结合同由 balanced_worker，机械文档/fixtures 可 routine_worker，验证 gpt_test_runner；不启用 DeepSeek、不创建 Reviewer。

M8 的 mock 不能冒充 API 集成；M6 的 ACK 不能冒充草稿完成；M9 的 fixture 不能冒充真实书上架。M10 的生产数据或模型开销超出已有授权时仅等待该操作授权，不阻塞可独立源码工作。27–46 人日仍为可复用现有底座前提下的粗估，共享底座缺陷修复按 M0 实际证据另列依赖，不自动归入本功能或承诺日历工期。


## 当前交付顺序覆盖说明（2026-10-03）

用户最新指令以 `delivery-order.md` 为准：保持原D2范围，先功能源码与文档完整收口、必要定向自检、协调特性分支提交/push，再在服务端全面验证。本文历史 Runtime/全链验证安排不得继续解释为首次完整源码push前的全面本地门禁；技术发布与真实业务激活授权仍是独立边界。

## 2026-10-07 最新接续（覆盖历史当前状态）

原D2源码与文档已收口，全部局部源码包独立接受。API5722e7fa / Web6dd4553c / Client9426030；最后生命周期Client Linux104PASS，API同树Chat76PASS及Agent17Windows环境失败原件保留。完整远程提交回执以evidence/delivery/resume-20261007/为准，组件→Root推送后再做隔离服务端全面验证。生产发布/迁移/真实任职与上架/付费调用未执行，84业务用例仍not_run；源范围接受不是whole-feature accepted。
