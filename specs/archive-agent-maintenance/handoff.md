# Agent 实施交接：典籍阁 Agent 任职与内容维护

- **特性名称**：典籍阁 Agent 任职与内容维护
- **Feature ID**：`archive-agent-maintenance`
- **设计版本**：D2，2026-09-28；2026-10-07源码与文档已完成并推送，服务端全面验证 BLOCKED，未整体验收。当前接续先读 delivery.md / integration.yaml 及最新 server-validation-status.json；completion-audit.md 保留历史补缺过程。
- **文档交付分支**：根仓 `codex/archive-agent-maintenance`。
- **根仓工作分支**：`codex/archive-agent-maintenance`；组件提交核验后由根仓 pin；不是部署发布。
- **组件实施状态**：API/Web/Client 的提交/tree、测试和远程回执统一记录在 delivery.md 与 integration.yaml。历史 prospective tree 证据保留；release 仍 not_started。

## 1. 给接手 Agent 的任务

按 D2 实现：聚义厅中由宋江协调或直接交办已任职吴用，通过典籍维护技能和受控 API 新增/修订典籍；先草稿、确定性校验，再按显式授权发布不可变版本并读回。以《三国演义》为真实业务验收目标，但不预设底本、章数、生产身份或付费权限。

**源码交付与实际验证的当前事实见 [implementation-baseline.md](/home/isp/wsps/cyf/specs/archive-agent-maintenance/implementation-baseline.md) 和 [integration.yaml](/home/isp/wsps/cyf/specs/archive-agent-maintenance/integration.yaml)。不要从局部测试推断功能已接线、已上线或 84 项业务验收已通过，也不要把旧 D1 当作接口合同。**

建议阅读顺序：

1. [需求与范围](/home/isp/wsps/cyf/specs/archive-agent-maintenance/spec.md)
2. [D2 详细设计](/home/isp/wsps/cyf/specs/archive-agent-maintenance/design.md)，尤其 §2/§3/§7/§10/§13/§18
3. [开发计划与依赖](/home/isp/wsps/cyf/specs/archive-agent-maintenance/tasks.md)
4. [验收矩阵](/home/isp/wsps/cyf/specs/archive-agent-maintenance/acceptance.md)及机器用例
5. [集成状态](/home/isp/wsps/cyf/specs/archive-agent-maintenance/integration.yaml)
6. [原 D1 风险记录](/home/isp/wsps/cyf/specs/archive-agent-maintenance/impact-assessment.md)和源码观察（仅供定位，不是最新上线基线）

## 2. 必须保持的边界

- Agent 不直连 DB，不持用户 JWT；安装、任职、任务 grant、公共发布用途授权分离。
- 首期典籍管理面板 + 原会话卡；不扩旧 ItemRef/OVERVIEW-v1、不伪装 TASK/PRIVATE、不自动创建收费悬赏。
- 复用现有命令/执行/安装/存储能力；archive job/run 是内容业务与关联记录，不是第二套 scheduler/lease/聊天队列或文件系统。
- 显式 @/密议直达目标，不强制经过宋江；两入口共同幂等受理，不重复执行。
- legacy AgentRuntime 与独立 Runtime v1 区分；逐目标协商能力，不全局 cutover，不从“已安装 Runtime”推导“可执行”。
- 保留旧水浒正文/ID/hash/anchor、私人数据、续读与选文；内容 schema 桥接不恢复旧 tenant 身份兼容。
- 私人资料读取不授予公开发布权；发布成功依据 publication + 实际读回，不依据模型回复、ACK 或 inbox completed。
- 已提交相邻特性为 `juyiting-multimedia-deliberation`；它的设计状态不代表底座代码已合入。共享接口接线先核对实际组件，不整文件覆盖其他任务。

## 3. D2 历史启动清单与当前接续点

以下 1–5 项保留为 D2 启动历史，不是当前尚未派发声明；当前接续以 delivery.md 和 implementation-baseline.md 最后章节为准。

1. 阅读当前工作区 AGENTS、项目地图、聚义厅 runbook、唯一运行台账；检查聊天附件，选择路径归属明确的工作树。不操作其他任务进程、服务或 evidence。
2. 核对 root/API/Web/Client 最新可复现 develop SHA/tree，不用 dirty checkout pin；记录实际 schema、模块依赖和事务管理器。
3. 按 design.md §18 映射身份/安装/执行/传输接口，登记尚缺适配；给出锁顺序、DTO/错误 fixtures、共享热点 Owner 交接范围和测试 selector。
4. 在本目录产出 `implementation-baseline.md`，作为 M0 结果。实际执行状态只在 TASKS.yaml 的 runtime_ledger_json 通过 orchestrator 维护，本目录不另建状态台账。
5. 按 tasks.md §6 开始内容域、权限、安装适配和独立 Web 合同开发；有显式依赖才等待，不因某个聊天候选未就绪停止所有独立工作。

## 4. 完成与授权

D2 原交接的“每包 Owner 自检，不创建 Reviewer”为历史安排。当前依照 AGENTS 与 MODEL_ROUTING.yaml：唯一 Writer 串行实施，SOURCE FREEZE 后由 Main 全程持共享 Gradle 锁验证，再独立只读复审；Reviewer 不修代码。测试/构建/发布按执行时有效政策（包括尚有效的本地授权例外），记录 exact SHA/tree、selector、fixture digest、制品摘要与真实健康，不伪造 Flow Run。

当前局部实施未启动生产操作。接手后允许的动作仍由用户授权及项目政策决定；真实首任管理员、任职吴用、来源与公共发布用途、额外付费操作必须精确核对。未获生产激活授权时可继续源码与隔离 fixture 工作，不能新增真实典籍后再补授权。

完成回报需区分：源码完成、验证完成、应用发布、Agent 就绪、真实典籍上架；只报告实际达到的层级及一个可执行下一步。

## 2026-10-07 最新接续（覆盖历史当前状态）

原D2源码与文档已收口并普通推送，全部局部源码包独立接受。API `5722e7fa2ee0d1f6a5eeb84ccf18dcfe009ae4e7` / Web `6dd4553c276c34a1d694a06a3daf11849dca0e64` / Client `9426030d4a9411429bbc1ad2bd154356a0287e3b`；Root源码交付提交 `8d77bcd325bd3cb4e6d589bc6add8071a3ceb09b` 已核对远端。最后生命周期Client Linux104PASS，API同树Chat76PASS及Agent17Windows环境失败原件保留。

**服务端全面验证 BLOCKED，尚未完成。** 独占工作区已检出上述精确源码；attempt1–3配置失败且tests=0，attempt4主动停止本任务JVM，attempt5最后观察到compileJava，其后退出码/XML/结果与自有进程、MySQL关闭和Gradle锁释放均未确认。前次SSH曾公钥认证成功但session open超时，本次只读重试仍exit255/连接超时；不据此认定认证错误或唯一资源根因。完整回归、实库迁移/并发selector、真实Runtime/浏览器结果不可标PASS，远端原始attempt日志尚未取回。

原件 `evidence/delivery/resume-20261007/{root-source-remote-receipt.json,server-validation-status.json,ssh-resume-readonly-20261007.log}`；恢复后先只读核本任务进程parent/cwd/argv、独占datadir及锁，不能按旧PID盲目kill或重启生产。准备脚本不是已完成验证，运行前须重新绑定真实完成尝试与精确源码。生产发布/迁移/真实任职与上架/付费调用未执行，84业务用例仍not_run/evidence=null；whole-feature accepted=false。

## 2026-10-08 develop 合入验证（覆盖历史当前状态）

本轮方向为四仓冻结 `origin/develop` → 现有 `codex/archive-agent-maintenance*` 特性分支，不合回 develop/master，不 force-push；原 D:\workspace\chaoyoufan\project\cyf-web-kit 不动。准确提交与远端回执见 `evidence/merge-develop/20261008/`；历史 10-07 源码及验证记录不改写。

本地合并候选：Web 18 个 selectors **476/476 PASS**、production build exit0。Windows API 五套产生新 XML：platform141/121PASS/17环境FAIL/3skip；security10/10PASS；maintenance237/149PASS/88skip；archive390/288PASS/11既有FAIL/91skip；typed91/90PASS/1黄金夹具CRLF环境FAIL。archive失败方法集合与已有基线完全相同 introduced=[]；typed Git index blob 与 develop 原字节一致，未改黄金hash。MySQL skip不是PASS，须在 Linux 隔离库实跑。

SSH现已恢复；已只读观察旧任务已知进程不存在、34061关闭、Gradle锁可获取；没有旧attempt5自然退出/关闭回执，仍不能追认旧验证完成。独立审查首次因 DeepSeek provider 不可用失败；改用独立只读 Sol 实例，明确不是跨模型审查。新源码审查、普通提交/push和隔离服务端验证结果将另留真实回执。

未进行生产部署/迁移/真实任职或上架/付费模型调用；84业务用例仍not_run/evidence=null，whole-feature accepted=false。服务端、Runtime及浏览器状态以新的 merge evidence 为准，不把组件测试等同真实业务验收。

### 合并源码收口（2026-10-08）

独立源码复审 `ACCEPT_MERGE_SOURCE_SCOPE`：初轮 P1（不完整 SSE replay 游标提前推进）已修，新增9回归；最终 focused task **16/16PASS/0skip/exit0**，fresh XML且冻结树不变。attempt3/4缺失Redis/JSONPath测试运行依赖的原失败保留；只补新测试task runtimeOnly，不改断言/生产权限。Windows原五suite用FREEZE3真实结果，最后两次只有该task runtime依赖增量，复用边界另证；Linux须全部六suite实跑。

组件普通merge提交均有旧特性和冻结develop两个parents，且远端exact核验：API `73c303e1213ee55a0ce20e7382e5ce9a4a440112`、Web `4a1e35eaba74b1581a15117b71b311b02c7796e5`、Client `02e131412901a9402abd5d0856aa57c0c35967c1`。源码审查是独立Sol实例，不是跨模型或全功能验收。Root同步新gitlinks/pins；服务端验证尚待新Root提交后执行。证据见 `evidence/merge-develop/20261008/review-final.json`、`component-merge-remotes.json`。84业务用例状态不变，生产操作未执行。
