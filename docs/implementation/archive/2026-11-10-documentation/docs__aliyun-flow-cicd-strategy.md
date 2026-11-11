> **2026-11-06 现行规则：** 用户告知云效额度用完，CYF 默认改为本地测试、构建、打包和受控部署；不自动启动 Flow。正式证据绑定真实本地构建批次、完整 commit/tree、必要测试与制品 SHA-256，不伪造 Run/CI 身份。保留发布授权、身份/ACL、锁、备份、可恢复安装与线上验收；develop 不自动部署。Gradle 仍先读构建文件并经现有编排器串行执行。下文冲突的 Flow-only/禁止本地构建说明仅作历史，完整规则见根 `AGENTS.md`“本地构建与部署（2026-11-06 用户最新决定）”。2026-11-07已完成API/Web原安装器LOCAL来源适配与同批完整发布实测；当前默认快速路径、适用范围和持久化/清理状态见下节。

## 本地快速构建发布长期策略（2026-11-07）

本节登记为 **CYF Web/API 后续本地发布的默认快速路径**，不是本轮计时专用命令；下方冲突的历史 Flow-only、未适配及未实测描述不代表当前状态。不扩展为 Runtime 已经达标，不恢复付费 Flow 自动触发。

### 默认入口和优化配置

| 范围 | 长期采用的方式 | 不得误读为 |
| --- | --- | --- |
| 统一执行 | `ops/orchestration/local_release.py --install`；固定任务、版本、两端commit/tree、工具链、干净源码、新输出、包外证据 | 自动部署develop或任意脏工作区 |
| 后端工具链 | 已验证Dragonwell21用于构建；短生命周期构建/测试JVM使用C1；Gradle内部parallel、workers2，仍经原orchestrator/共享锁 | 修改生产Temurin/JVM或无限并发 |
| 后端缓存 | 持久、已验证的依赖与JavaCompile缓存；缓存齐备时显式offline；测试/validateLayering/fresh bootJar均当批执行 | 复用旧测试结果或旧最终JAR冒充新构建 |
| 后端测试 | 105项发布基线，源码切片只编译该基线；业务改动用`--api-regression-arg`加入受影响回归 | 只用`--tests`就能避免全部测试编译；快速绿可覆盖已知业务失败 |
| 前端构建 | npm ci、47项通过/2pending的发布基线、原源码Vite配置；`--web-regression-test`补业务回归 | 已完成全量前端回归或业务回归自动选取 |
| 前端打包 | public原样流式归档，避免dist重复复制；gzip level1；归档后释放自有生成dist；全部文件size/SHA校验 | 漏打public、只校验主页或删生产资源 |
| 主机调度 | 两端重型构建串行；只在单次Gradle内部有限并行 | 前后端高内存构建同时争抢主机资源 |
| 安装与重试 | 复用已适配LOCAL的原事务helper；锁、前代摘要、备份、恢复、健康、在线资源校验；精确同包可恢复不重编 | 绕过TLS、锁、授权或用失败测试包发布 |
| 工具预检 | Web helper用其原定系统Python `/usr/bin/python3 -I -B`；安装前验证同解释器TLS信任链 | 使用控制器Python替代，或关闭证书验证 |

### 计时与停止规则

完整同批默认上限600秒，预计或实际超限须向用户申请明确范围/总时限的例外，未获批不延长或绕过（2026-11-07最新决定）。准备、锁等待、测试、构建、打包、安装、健康/必要smoke及收尾都计入。构建的task-owned systemd unit采用**剩余共同预算**，到点停止本批构建，保留日志并优化，不原样盲等/重跑。失败和修复间隔不扣除，不跨批拼接成绩。

生产安装/启动必须在限时构建cgroup之外；不能为凑时间强杀生产JVM，原恢复保护保持。无法在预算内完成就记未达标，不因目标放过必要回归。冷缓存、依赖变更和新增业务回归须重新实测；offline缺依赖应先定位并受控补齐，不反复盲跑。

### 已验证范围及持久化/清理状态

- 2026-11-07同批 `cyf-full-local-20261107-01` **435.314秒**完整发布；包含TLS解释器故障与恢复，非扣除失败后的净耗时。固定生产同源API `7bb82c526e4ba4345ca8e88711067ed23dfcdbbc`、Web `f1234a0a083b5f38c2677886e89d98fc95aed21c`，热缓存快速基线；API105项无失败/跳过，Web47通过/2pending；前端255个线上index/JS/CSS摘要匹配。Web内容与原生产一致、changedFiles=0，不是新业务版本差异发布性能证明。
- 修正解释器后的通用控制器已做4项隔离回归；相同调用由当批真实恢复验证，未再次完整部署。结果不是冷启动、全量回归、任意后续提交必≤600秒的保证。
- **2026-11-07持久化已完成并回读核验：** 构建JDK为`/home/isp/apps/dragonwell-21.0.11.0.11+10-GA`；已验证Gradle缓存为`/home/isp/state/cyf-local-build/gradle-home`。当前API、API回退和当前Web包的逐字节镜像位于`/home/isp/pkgs/cyf/cyf-local-archive-20261107-{api-current,api-rollback,web-current}/package/`；原历史安装记录未改写，仍绑定的内存盘原包继续保护。新批输出使用持久任务目录，不再依赖内存盘归档。
- **受控保留已实际启用：** 已安装现有维护工具的artifact登记及API LOCAL schema4/Web LOCAL schema2适配，4个完成任务已登记到原台账；原每30分钟cron继续消费，不新增任务。最新两批/组件、完成24小时、当前及回退绑定、进程/锁/未知状态均保护。只允许显式任务根或其`api/web/runtime`组件子根登记，不泛扫历史目录。
- 已清理明确过期/废弃的2个API备份、3个未发布构建中间JAR、2个Web历史载荷及1个孤儿stage，回收**1,591,824,384 allocated bytes（约1.48GiB）**；证据/日志和当前、必要回退保持。持久化同时占用磁盘，净余量约1GiB，仍低于自动清理5GiB触发值；实际cron入口退出3表示无合规候选但容量目标未达，不能强删数据库/Runtime/未知备份来凑8GiB。
- 维护工具253项隔离回归通过；真实自动入口已执行，末尾改为轻量`df`，不再以递归`du`长持锁。安装摘要、登记及清理证据见`docs/implementation/evidence/local-release-closure-20261107/`。版本化收口记录见同目录`version-control.json`（以实际生成及远端回读为准）；共享技能未修改，不声称已全局同步。

操作参数见 `ops/orchestration/README.md`“本地快速构建与受控发布”；原临时源码worktree已收口，下一批必须选用/准备真实干净源码路径，不照抄历史已删路径。完整计时、失败及工具/制品摘要见 `docs/implementation/handoffs/LOCAL-BUILD-TIMING-20261106.md` 与 `docs/implementation/evidence/local-release-fast-20261106/full-01/release.json`。

## 2026-11-06 本地完整发布耗时与历史包收口

本地同批必要准备、测试、构建、打包、授权安装及健康/必要业务冒烟目标 **600秒以内**。记录各阶段、排队/阶段间等待和完整墙钟；此处原“仅目标、不限时”已由2026-11-07决定替代：保留工具600秒限时，超限须向用户申请例外；不减免回归与安全保护，不强杀生产服务或业务请求。2026-10-09的156.492秒构建打包及463.849秒估算不可作为当前完整发布达标；此为2026-11-06规则更新时状态；2026-11-07已取得同批435.314秒实测，见下方长期策略与包外证据。

本地包复用现有 `rebuildable_cache_cleanup.py` / `completed-tasks.json`；Owner 明确完成后登记最终输出，既有每30分钟低磁盘清理消费，保留最近两批及权威当前/回退绑定。不自动导入未知历史目录，不重建已退役本地准入。具体风险、条件、失败范围、回归与主机安装状态见 `ops/maintenance/LOCAL_ARTIFACT_RETENTION.md` 和 `docs/implementation/handoffs/LOCAL-BUILD-RETENTION-10M-20261106.md`。

# CYF 云效 Flow 资源分工与版本化部署策略

更新：2026-10-22。用户明确：Flow用于减少本机Node.js、Gradle等高内存任务，不是机械地“只做构建部署、不能测试”；轻量任务可在本机执行。本次覆盖当前分工和Run生命周期规则，根仓基线commit `5e6ab2b6f1a156c320189f17d76941fbe623738a`，既有脏修改保留。不修改全局、其他项目或共享技能。**规则更新后，按用户授权已切换两端默认CI模板与云端配置，并各执行一次；本任务未部署、未改生产安装器。下方旧实现/运行事实保留原日期。**

## 2026-10-29 当前分工覆盖

用户明确：Flow 用于减轻当前主机内存负担，并按运行时间控制成本。**当前交付路径改为：固定源码/授权 → Flow 必要测试、构建、打包、上传 → Flow 结束 → 主机主动拉取固定 Run 制品 → 独立受控安装和线上验收。** 不从 Flow 调用/监听生产主机，不添加 VMDeploy、SSH 安装、主机健康等待或发布用运维 Run。不得将高内存任务移回本机。

“同 Run”指制品及其测试/源码来源一致，不再要求安装与构建处于同一 Run。版本化适配器的 `PIPELINE RUN COMMIT VERSION ARTIFACT_SHA256` 中 Run 是真实构建来源，不能伪造；Runtime 旧 Flow-only 安装器须显式适配本机来源输入。保留权限、摘要、路径、锁、备份、可恢复安装；主机安装仅在已有授权范围执行。精确有效制品优先复用，不因安装/验收/规则变更重复付费构建。旧 Run 仅部署阶段失败时须核对完整成功构建链与制品后才能复用，并保留原失败状态。

Flow 总上限600秒仍覆盖云端全 Run；独立主机安装/验收不占 Flow 等待。旧文档中的 Flow 授权部署/安装同 Run 口径仅作历史，以上文及根 AGENTS 2026-10-29规则为准。模板/云端配置实际符合情况须另行 readback，不能由本段推断已上线。

### 2026-10-29 当前配置与已验证安装边界

10:46 CST只读readback确认4403172、5260799、5264702均为worker测试/构建/上传，无主机调用或等待。Web fa8d7f1793392918bd0d1531c6f029cbaff8daeb（371）与Runtime c3f973c2e5ca2990dd3e775b42f6bf02f7e0a060（93成功build）已复用固定制品在主机独立安装；本次接续新增Run为0。Runtime显式本机来源输入和6项来源/7项恢复检查已验证，当前任务安装器仍为任务专用入口，不宣称已成为通用适配器。API80739ebb0d25be5e713bd1c82209cfea089d3600本次仅复核，不重复安装。旧93 FAIL、API362 CANCELED保持原状态。

**后续复核更新：部署已完成，生产验收尚未完成。** 岗位缺表已于2026-10-29 11:34按用户明确授权补齐三表；固定线上80739ebb SQL经隔离DDL验证，真实认证查询HTTP200/E0，无业务数据/权限改写、无重启或新Flow。吴用通道重连仍存在，并观察到API binding/runtime反向锁序死锁（与重连因果关系待核实）；11:04全ready仅是时点证据，不能据此宣称持续健康。详见同任务handoff末节。

主机安装不占Flow等待，但仍存在服务停机窗口：本次Runtime备份、独立compare及启动耗时较长，不能把解耦描述成零停机；保留完整备份/锁/恢复，不以删保护换速度。当前核验覆盖字节/版本、API健康、三个Agent通道就绪、Web登录和既有事项/成果只读展示，不含灰度或付费模型端到端。配置、安装和验证证据索引：`docs/implementation/handoffs/MINIMAL-TENANT-GRAY-MERGE-CHECK-20261028.md`末节；私有证据位于`/home/isp/state/cyf-gray-safe-integration-20261029/`。历史段落不再作为新发布指令。

## 2026-10-22 交付路径（已由上节覆盖）

- **Flow负责重任务**：前端 `4403172`、后端 `5260799`，承载高内存测试、编译、生产构建、打包与授权部署，复用原流水线。保留必要测试，不按“检查”这个名称删除测试或把重任务移回本机。
- **本机负责轻任务**：文档/静态检查、低开销定向验证、配置准备、API查询、日志分析、发布条件确认、跨端协调及部署后健康/业务核验。按实际负载而非node/java/gradle命令名称划分；不设无依据内存阈值，不把全量编译/测试藏进本机检查。禁止本机生产打包/源码直发或Flow失败后本机兜底发布。
- **Run完成即结束**：本轮测试、构建及已授权部署执行完即按真实结果结束。不添加ready文件轮询、等待另一条Flow、人工确认、发布配对或上线验收的挂起作业。条件不齐在本机协调；仅验证/构建Run也直接结束。结束不代表线上验收通过，核验结果由本机另记。
- **develop不自动部署**：合入/push/验证只用于开发集成，不自动或定时发布。版本、授权和依赖条件在启动发布前确认，不启动后占住Run等待。
- **发布顺序**：本机准备与确认 → 固定commit/tree → Flow测试/构建 → 同Run不可变制品 → Flow授权部署 → Run结束 → 本机健康/业务核验。构建、安装、Run终态和上线验收四类事实不混用。

## 固定入口与执行边界

| 入口 | 当前职责 |
| --- | --- |
| `4403172` / `5260799` | 前端/后端重型测试、构建及授权版本部署；非等待/协调器 |
| `ops/orchestration/cyf_orchestrator.py gradle ...` | 所有Gradle操作串行入口；重任务在Flow，轻量诊断可本机；先读相关build.gradle |
| `/home/isp/hosts/cyf/api/cyf-api-kit.jar` | 后端实体安装目标，只安装本次固定制品，不原地编译 |
| `5263690` / `5263692` | 既有CI-only按需诊断，不默认重复运行，不新增流水线 |
| `5264702` | 临时运维默认只读；复用不增加授权，不覆盖活动Run配置 |

## 制品安装契约

- 真实Flow Run、完整commit/tree、版本及同Run归档SHA-256仍绑定；复用既有版本化部署适配器，归档摘要与JAR/dist摘要分别记录。若要分离构建/部署Run，先明确来源契约与适配器支持，不伪造同Run证据。
- 保留身份/ACL、依赖与制品完整性、路径/权限、统一发布锁及锁顺序、备份与可恢复安装。这些是执行安全边界，不是可删除的重复检查，也不授权新增等待步骤。生产数据和迁移仍依实际授权执行。
- 发布条件和互斥冲突在本机控制面协调，未准备好不启动；执行中冲突不抢占、不绕锁、不假报成功，不以无依据超时强杀。现有安装器中的长等待需要单独适配，文档修改不代表已改造。
- 后端固定干净源码构建，正式回归、validateLayering、PublicArtifactVerifier、fresh bootJar及compile-only缓存约束保留。不得为本机轻量检查额外触发重型构建图。
- 发布前核对当前配置、helper/制品接口与恢复路径；结束后按归属恢复非部署默认配置。Flow写入前确认无活动Run，保存前值、固定候选并readback；不覆盖或取消他人任务。
- 生产JAR/cwd为 `/home/isp/hosts/cyf/api`，兼容链接、状态路径及未完成迁移以根AGENTS为准；不因规则修改重写历史回执。

## 构建与验收证据

- 本机轻量验证与云端重型测试分别记录固定源码、selector/fixture、环境、结果和证据路径；精确匹配才能复用，不冒充彼此。测试/分层结果和生产JAR不能以编译缓存替代。
- 发布记录保留版本、源码、各Flow Run/日志、测试和制品摘要、安装结果、恢复信息；健康与业务检查在本机完成并另记，不延长Run，也不能把缺失核验写为成功。
- 同根因同输入连续失败两次停止盲重试，先归因/修复。不新增独立Reviewer、重复构建、无依据阈值或“等文件放行”的控制循环。
- 源码/模板、云端配置、真实Run与线上状态分别报告。2026-10-22规则更新后已执行默认CI切换与观测（下节）；维护入口仍在 `ops/ci/aliyun-flow/`，版本化部署适配器改造仍须另行核验，不以CI成功代替。

## 默认CI新规则实测（2026-10-22）

在原入口保存前值、确认空闲后更新并readback，各执行一次，不部署生产：

| 组件/Run | 固定源码 | 结果与用时 | 测试 |
| --- | --- | --- | --- |
| Web4403172/294 | `669bdc9d6439d1bd7eb71df5ed401202a648f419` | SUCCESS，177秒（2分57） | 3252通过，2pending，0失败 |
| API5260799/234 | `7841057b057c012cfa203fb658c1043500be055e` | SUCCESS，337秒（5分37） | 2828次，122跳过，0失败/错误 |

两端均保留必要重型测试、构建及制品上传，无外部等待/部署阶段，完成后正常结束。Web测试40.101秒、Vite10.74秒；API Gradle151.364秒，其余为环境准备、打包上传等流水线开销，不冒充编译耗时。18:47前后实时readback两端canonical配置均匹配已测候选。Web613个dist文件、API receipt/元数据/JAR与来源摘要均本机流式核验；不在本机执行应用构建。证据见 `docs/implementation/evidence/flow-resource-split-20261022/results.json`，任务边界见同名handoff。上述是CI结果，不是生产部署验收或主机内存降幅实测；不与旧含配对等待的27分钟作等范围提速比较。部署安装器仍须单独核验新生命周期，不由此删除安全保护。

## 默认CI耗时优化续验（2026-10-22，Run296/235）

覆盖与上节相同固定源码Web669bdc9d/API7841057b；非生产部署。两端维护入口及实际云端配置已更新并readback：

- **前端默认浅克隆**：官方`sources.repo_0.cloneDepth: 1`，API解析字段与实际两作业`git clone --depth=1`均已核验。release profile测试范围未改；assets/all需历史provenance时先`git fetch --unshallow`并保持HEAD等于CI_COMMIT_SHA，隔离Git夹具已验证，不冒充完整assets云测。未知profile不静默退回release。
- **Web296 SUCCESS 127秒（2分07）**，对照同SHA的294为177秒，本轮少50秒；构建作业克隆93→21秒，扫描克隆30→13秒，扫描总118秒。3252通过/2pending/0失败，与294计数一致，测试49.686秒、Vite14.05秒反而比294慢，说明不能把总差值全当稳定收益或承诺每轮127秒。613个dist文件及同Run/commit/tree/版本绑定独立核验通过。
- **后端仅补准备计时，不更改执行策略**：既有`test-results/summary.json`新增`flowPreparationPhases`与白名单`jdkBootstrap`；保留原policy/compile-only缓存、所有测试和fresh bootJar。API235 SUCCESS 293秒（4分53），与234相比少44秒不是计时改动的优化收益。316 suites/2828次/122跳过/0失败错误，逐suite计数与234完全相同，JAR SHA仍`244f2b6e208bf9794cb5da2ce506903b40acc24aa8483dece30e293c154f5e03`。
- 后端准备实测：JDK5.24秒（归档命中，校验0.561秒）、字体依赖37.76秒、MySQL4.62秒；Gradle命令147.789秒（shell包络148.06秒）。下个候选优先针对字体依赖安装环境，不再用前段缺日志的差额猜测JDK慢，也不盲目撤缓存/减回归。预装依赖的固定构建镜像仍需另行来源、完整性、渲染回归与实际收益验证，本轮未实现。
- 默认canonical配置：Web`d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd`，API`f56903cab42385c8b2967fdd5b592f6be4fdd331c5612309a7283582300129ef`。该记录不替代未来运行前实时查询。

证据：`docs/implementation/evidence/flow-resource-split-20261022/duration-optimization-results.json`及同目录duration前缀验证/summary；完整过程见既有handoff。下载归档核验后仅删除本任务临时副本，Flow仍保留制品。未提交/push应用源码、未生产部署，不声明长期SLO或安装器改造完成。

## 以下为既有实现与历史核验记录

下列段落保留当时的测试、缓存与运行事实，不覆盖上述资源分工和Run生命周期，也不代表当前云端配置已符合新规则。

## 后端 Flow 最近核验边界（2026-10-17）

API `c1e97923bf2325e3ada33b7e2816f203630f020d` / tree `f192948af6ff27b4e78f6f1585aca9bd8a6b4968`，`5260799 / Run147` CI SUCCESS，258秒，2288通过/0失败/95跳过，Gradle209.346秒。仅此固定候选测试/构建/上传成功，未部署；此前按用户授权累计删除84个方法的覆盖缺口仍在，不视为原套件等价或持续五分钟保证。

Run147临时JDK/compile-only优化配置已恢复原值，不能据规范更新声称默认云端模板已永久提速或已包含部署阶段。后续使用时须核对当前任务映射、固定工具与配置，再按版本发布契约执行。证据见 `docs/implementation/evidence/backend-flow-5m-20261016/testfix/flow147-*`；详细过程与恢复见 `docs/implementation/handoffs/BACKEND-FLOW-5M-20261016.md`。

## 后端五分钟优化增量（核对：2026-10-20）

固定 API commit `9ca2776c27ce3270efa0ea4c366b7de0e68e8dbb` / tree `847927f2fc9d76ca09cee79dc7aa987a627450c5`，覆盖 Run195 原全部 302 个 suite / 2728 次测试执行，0失败、0错误、122跳过（与 Run195 逐 suite 次数核对一致）。本轮不删测试，不将既有跳过或历史84方法删除写成覆盖恢复；不改生产代码/JVM，不部署。

- Run195：完整版本发布547秒（9分07）；构建375秒、部署171秒。Gradle264.071秒，已有101个编译任务缓存命中，不能归因成“没开缓存”。
- Run196：仅对短生命周期 Test JVM 启用 C1，CI365秒，Gradle242.079秒；未达五分钟。
- Run197：同一 Gradle 进程增加 `--parallel --max-workers=3`（实测3核6GB worker），CI SUCCESS **283秒（4分43）**，Gradle160.853秒；原全部测试、真实MySQL、layering、PublicArtifactVerifier及fresh bootJar保留。103个编译任务命中；不并行启动多条Gradle、不改变单task fork数。
- 同 Run 完整制品独立下载重算 SHA-256 `5129d497791befb3a87e72846eb8bce1740f06cababa1f7d0a385a02f75e1f01`；内嵌 receipt 的 Run/commit/tree/clean绑定核对通过，JAR SHA `a71821bea7caed3ae1d37d9dadb5accde4e4f6cebc7081b0c96a32e64851c6c3` 与Run195一致。不是历史制品冒充本轮结果。

复用方式：固定新任务和源码，在现有可信工具 bundle 中纳入 `ops/ci/aliyun-flow/flow-compile-cache.init.gradle`，原 compile-only opt-in 基础上显式设 `CYF_FLOW_SHORT_LIVED_TEST_JVM=1`，经原 orchestrator 单进程传入上述并行参数。C1只改 `Test.jvmArgs`，性能/JIT基准不启用此选项；不改生产JVM。不要照搬Run197的旧任务快照、commit、fixture或私有payload作为新任务授权。

**边界：283秒只证明此固定输入的一次 CI，不是整条版本发布五分钟或持续SLO。** 已知Run195旧进程停止33秒，Spring Started56.656秒（不等于完整healthy），部署其余阶段尚缺完整计时；不靠缩短请求deadline、强杀进程、懒初始化掩盖失败或跳过完整性/健康来换时间。下一步需对授权版本发布拆解安装/实际ready与业务核验。

Run196/197实验结束时在无活动Run/配置归属核对后恢复原云端配置，readback SHA `a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a`；当时默认云端模板尚未永久切换；2026-10-20后续固化状态见下方“后端默认提速配置维护”，不把历史恢复动作视为当前配置。可复用profile源码已收口，默认CI已固化，正式发布Owner仍须把已核验参数纳入其固定版本候选；无部署默认不提供上线授权。详细证据 `docs/implementation/evidence/backend-flow-5m-20261020/`，接续 `docs/implementation/handoffs/BACKEND-FLOW-5M-20261016.md`。

## 历史：后端本地构建缓存提速（2026-10-09）

> 自2026-10-17起不再是正式发布路径。以下仅保留当时实现、验收与恢复记录，不授权新本地构建部署。

正式本地后端构建通过既有 `cyf_orchestrator.py gradle` **默认**复用受控私有Gradle依赖缓存，并启用compile-only输出缓存：识别本地release opt-in与匹配的固定metadata init，无缓存参数即可选择 `/var/cache/cyf-gradle-local` 并加入 `--build-cache`；显式诊断/隔离参数可覆盖，Flow和普通诊断不变。仅在干净固定commit/tree及新输出目录执行。compile-only策略：仅JavaCompile按内容指纹复用，其余任务禁用输出缓存，测试禁止up-to-date；仍执行同批定向测试、`validateLayering`、依赖来源/SHA与fresh bootJar完整性检查，不缓存测试结果/生产JAR、不删除安全回归。home信任边界与参数冲突检查见 `ops/orchestration/README.md`。

2026-10-09授权收尾已按既有锁、备份与原子安装同步主机admission白名单（当前SHA `49ff62e470beadf5c5c570b007d1d30a6dd18b1f32df217274d89121ff77728b`）；cached/skipped测试、分层和bootJar仍拒绝。应用未发布/重启，历史helper catalog与authority/receipt不改写，后续发布生成新批次catalog。默认策略实现源码 `638777ed`，证据与恢复原值见原handoff。

10分钟是“测试/构建/安装核验执行时间”的优化目标，不是强制超时或减免安全门禁。历史安装约307秒来自日志文件起止，未包含排队与批次中间等待；本次没有授权/触发生产安装，因此新构建加历史安装仅用于评估，不冒充完整发布达标。固定输入、实测结果与证据见 `docs/implementation/handoffs/BACKEND-RELEASE-10M-20261009.md`。冷缓存和其它源码/selector不作无实测承诺。

## 后端 Flow 提速实验（2026-10-16）

覆盖范围：`5260799`无部署诊断；API源码固定`58b4b5f408257c6d5103d915e13c7927c1571e20`。当时采用前端Flow、后端本地分工；该默认已于2026-10-17被上文双端Flow规则取代。本节保留当时实验范围，不启用自动部署。

- `prepare-backend-jdk.py`用于Flow Linux x86_64 worker：官方Dragonwell Extended21.0.11.0.11+10压缩包，固定SHA-256，仅缓存归档、每次重验并新私有目录解包。不运行yum/dnf，不执行缓存解压目录；拒绝损坏归档、链接逃逸/特殊成员，校验java/javac版本。官方OSS与GitHub发布摘要一致；云端GitHub下载曾socket timeout，实际使用官方OSS镜像，不回退系统安装。
- 参数：`--cache "$HOME/.cache/cyf-backend-jdk-archives" --destination "$CYF_EXPERIMENT/jdk"`。destination必须全新；结果最后一行是JAVA_HOME，之前的`CYF_JDK_TIMING`为单调耗时。主机生产JRE不使用此入口，不在安装目录执行。
- `flow-compile-cache.init.gradle`仅在`CYF_FLOW_GRADLE_ACTIVE=1`与`CYF_FLOW_COMPILE_CACHE_OPT_IN=1`时使用；需显式`--build-cache`。仅允许JavaCompile输出缓存；其余任务禁用输出缓存，Test、validateLayering、bootJar强制fresh。仍同时使用原cold-init的依赖完整性/凭据剥离规则，不能把本地release metadata init搬到Flow。
- 云端也经既有orchestrator串行入口；注意argparse REMAINDER要求`gradle --cwd ... --tree-sha ... --selector ... --fixture-digest ... TASK_ID -- ./gradlew ...`，选项必须在TASK_ID之前。控制工具与单任务授权快照放源码之外并固定摘要，云端快照不是权威台账；源码工作区必须干净，build和project-cache用独立目录。
- 实测：Run141/142/143的冷JDK准备6.138/6.470/6.697秒，证明避开历史Run139约1212秒的RPM准备路径；不是相同JDK补丁构建的严格单变量对比。Run143仍在业务测试处失败：部分执行1086项，978通过/71失败/37跳过；无成功制品，尚无热编译缓存成功对照、完整部署或300秒验收。
- 原Flow引用的chatDeliberation已在API提交5d54634a3d删除。实验把保留的50源文件/49测试类映射到7个现行task并补2个迁移回归；不得恢复旧兼容suite或删失败测试换速度。实际映射和剩余失败清单见本次handoff。
- 实验结束已readback恢复原配置SHA`a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a`，没有应用部署/重启。候选只有在新固定源码测试成功后才能用于正式版本化发布，不将失败Run快速结束当达标。

隔离工具自检：`python3 -B -m unittest discover -s ops/ci/aliyun-flow/tests -p test_backend_jdk.py -v`（12项）。完整过程/恢复/下一步见`docs/implementation/handoffs/BACKEND-FLOW-5M-20261016.md`，证据在同任务evidence目录。

## 历史控制面与适配器记录（截至 2026-10-06，非当前执行规范）

以下原记录保留不改写；历史适配器和发布证据不能证明当前配置、制品或线上版本已验收，执行以上文现行规范为准。

2026-10-06 经用户授权完成控制面调整：前端单次 Update/readback 移除部署阶段；后端当前配置原已仅验证，未写入。两端 develop push 保留测试、构建与制品，不部署；两个旧 nightly timer 均 disabled/inactive，无下一触发时刻。本地 develop 模板同步移除部署阶段，7 项静态测试通过。实际证据见 `docs/aliyun-flow-versioned-deployment-switch-20261006.json`。

版本发布需先准备绑定明确版本、完整 commit 的固定发布候选配置，复用上述入口；发布完成后恢复 develop 仅验证配置。2026-10-06 已通过 `5264702 / Run13` 安装版本化部署适配器，移除午夜 intent 与旧分时版本限制；运维配置已恢复。36 项本地定向测试通过，Flow 安装器执行固定的 15 项回归后完成安装；日志接口未返回测试明细，依据固定测试摘要与安装回执核验。证据见 `docs/aliyun-flow-versioned-adapter-migration-20261006.json`。本次只更新部署工具，未发布、重启应用或执行数据库变更，不能视为应用版本端到端验收。

初次审计把后端历史 Run 的部署阶段误当作当前配置，已纠正；当前 YAML 才是自动部署配置证据。

## 版本发布适配器契约

- 前后端统一调用：`/usr/local/sbin/cyf-{api|web}-flow-deploy PIPELINE RUN COMMIT VERSION ARTIFACT_SHA256`。版本与完整 commit 必须固定；旧三参数调用不再有效，不创建 nightly intent。
- `ARTIFACT_SHA256` 是该 Run 完整下载归档的 SHA-256，不是单独 JAR、dist 文件或目录的摘要。仍须校验 Run、commit、manifest/receipt 与文件完整性；前端 `VERSION` 必须等于制品 manifest 的 `package_version`。
- 发布候选必须同步更新制品内嵌适配器及 helper 升级调用的接口和哈希，不能复用旧模板中冻结的三参数 helper。当前 develop 模板仅 CI，不因安装新适配器恢复部署。
- 后端记录版本/commit/Run/制品绑定，安装与既有 schema 检查成功后才标记 verified；前端保留互斥等待、分阶段发布与实际在线核验。

## 历史证据（非当前执行规范）

以下保留历史 Run、迁移与部署记录；其中 develop 自动发布、旧本机例外及定时安排已不作为当前发布依据。历史事实不能代替当前版本的 Run 与在线核验。

## 2026-09-12 CI-only 验收证据

### 后端 Run 1

- Pipeline：`5263690 / cyf-api-kit-develop-ci`
- 状态：`SUCCESS`
- commit：`a9d3e7417447a9f5f59a12523e582a8e8f1818f6`
- tree：`3352d0049871b588108eba0af990091a80fd965c`
- 门禁：定向测试、`validateLayering`、`:starter:bootJar`、OpenCV 私仓来源与摘要校验、`ArtifactUpload` 全部成功
- JAR SHA-256：`bbb6006e9abf611cea8168820d62558b2ebfef0d9d6f14a6987291edacb33fc9`
- 配置 canonical SHA-256：`0d63636ee01976630e0b51bf63fe9b82c4793967a0049ad12ab1c68d783f646b`

### 前端 Run 7

- Pipeline：`5263692 / cyf-web-kit-develop-ci`
- 状态：`SUCCESS`
- commit：`c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`
- tree：`2f82fca468197608cdaa7061d58d11785c6ca7ef`
- 运行时：Node `20.20.2`；Chrome for Testing `133.0.6943.141`；固定 WebP `1.2.0` 来源、ABI 与 SHA 校验成功
- E14：五项 gate 全通过；固定 10 秒 warmup、60 秒 sample，total p95 `0.8000000119 ms`、p99 `0.9000000060 ms`
- Mocha：`2118` tests，`2116` passing，`2` pending，`0` failures；mochawesome HTML/JSON 已上传
- Vite：`6.4.3` production build 成功，`8.84s`
- 制品：`104195319` bytes，SHA-256 `c62e9b9c4a3fea77b51e026bce10431844599b03d5250760f1fb216001c0dc37`
- 制品内部绑定同一 commit/tree，包含 `dist/`、`mochawesome-report/`、`source-commit.txt`、`source-tree.txt`
- 配置 canonical SHA-256：`1707fbf7191de5b4028063ee41c752e13c56eef1bb45b1d9ab554c82de71dfbf`

这些证据只证明各自固定 Run 的云端测试、构建和制品，不表示已生产部署。旧验收不能作为新自动发布配置已跑通的证据。

## 2026-09-12 当前生产验收证据

以下两个生产 Run 由其它执行者触发；本次流水线优化只做只读关联和产物核验，不将其归因于本线程，也没有重复触发生产。

### 后端 Run 18

- Pipeline：`5260799 / cyf-api-kit-ci`；状态 `SUCCESS`
- commit：`a8489561586400af049eee625d90b6e98e834f04`；tree：`1fd1cb7f60e279e4e934239434d4a3a7c8c59cdc`
- 构建 Job `513927230`：74 tests，0 failures/errors/skipped；`validateLayering`、`:starter:bootJar`、PublicArtifactVerifier、OpenCV provenance 与制品上传成功
- 发布 JAR：`220206485` bytes，SHA-256 `aa64ddf1be41147156236aa3d4f70121e2b95918d8dd2024d0cd3d0fec4df090`
- 下载包：`198144927` bytes，SHA-256 `2c04f7b03f37fc70fc7d673c486f0cc2f97813e0b7ba790c168c68a69ef12ffd`；内部 receipt SHA-256 `52afc26bee8438202ca45b9f986e74756ff79fe803465b1efff2d75752519286`
- 部署 Job `513935436`；部署单 `69495567`；主机组 `28833`；一批一台 `Success / healthy`
- 部署机日志确认 `ARTIFACT_ATTESTATION=MATCH`、运行用户 `cyf-api`、端口 `10018` 由目标 PID 监听、loopback `HEALTH=UP`，最终 `CYF_API_FLOW_INSTALL=PASS`
- 公网 `https://api.chaoyoufan.cn/actuator/health` 在本次核验中返回空响应，未独立证明公网反向代理 health；这不改变部署机 loopback health 已通过的结论
- 当前配置 canonical SHA-256：`919eb67be40c379507306633f224ce291f7338e216125df4dc7a956403672da3`

### 前端 Run 91

- Pipeline：`4403172 / cyf-web-kit`；状态 `SUCCESS`
- commit：`c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`，与前端 CI-only Run 7 相同
- 扫描、单测、构建、部署全部成功；Mocha `2118` tests，`2116` passing，`2` pending，`0` failures；Vite `6.4.3` build `9.77s`
- 生产包：`102898255` bytes，SHA-256 `da53366b2f302eb50cc1f63cd17783447aa36a7fe529787bc272fe28d8ce59b4`，Flow 日志 MD5 `e11298669fa2f73ae75697afaf81463e`
- 部署单 `69495496`；主机组 `28833`；一批一台 `Success / healthy`
- 包内 410 个文件全部存在于部署目录且逐文件字节一致；无缺失、无差异。部署目录另有 143 个不属于本次包的历史文件，当前入口不引用它们，但后续应改为 staging + 原子切换或按 manifest 清理
- 首页、`/juyiting` 均 HTTP 200；入口 HTML、主 JS/CSS、聚义厅懒加载 JS/CSS 共 5 个关键文件与同 Run 制品逐字节一致
- 当前配置 canonical SHA-256：`6feb2c10d5609b93f9e19fca8a09905ef3db91ba2ddba74d6693014c54c5c718`

完整非敏感机器可读摘要见 `docs/aliyun-flow-cicd-evidence-20260912.json`。


## 2026-09-12 18:54 CST 增量

- Web `4403172 / Run92`：develop `1ac5cb1e4973919bacf054e961b43ff24d47e832`，2117 passing / 2 pending / 0 failures；部署单 `69505789`，410 文件及 9 个线上响应哈希匹配。制品 SHA-256 `ab289e2791709f70202e161b57db2a35e24e55271148a67114019d5ec1285741`。手动发布已实成；自动 push 尚未启用。
- API Run22：58 类范围的测试/构建成功，但启动缺 `javax.mail.MessagingException`，发布器已自动恢复旧 Run18 JAR，health UP；不是新功能上线成功。
- 新候选 `688a3e65` 将 SMS mail 从 compileOnly 改为 implementation，新增隔离主运行 classpath 回归。Run23 已单次启动；59 类范围和 bootJar 实际 mail/activation/provider 类检查在制品导出前执行。未取得新运行健康证明前，不标后端发布完成。
- 安装保留锁与回退；仅将瞬时锁冲突改为固定 60 秒等待。同 Run 下载副本在验证身份及完整摘要后回收，保留 incoming、云端制品和回退 JAR，当时保留 5GiB 运行余量；该固定阈值已按 2026-09-13 用户指令取消。

## 2026-09-12 19:24 CST 发布闭环与并行推进

- API `5260799 / Run23 SUCCESS`：develop `688a3e6546dcacba116f76cbec7e1d91f72764f4` / tree `608e799ad81ab3c4876b376119af322901a903ef`；59 类 selector 范围、bootJar 实际 mail/activation/provider 检查通过。Build `514133208` 复用，未重复构建；部署 Job `514138578` / order `69507020` 单机 Success/healthy。
- JAR `a5cc9db17022291bc129b0536d5b8c785dac9efec4bf437ea503f3e183be721d` 与 canonical 文件一致；receipt `c9559c37aec9b1010d17e54a577e0eb5079b38377cb3abd32367129602819c08`；PID `2607082` 监听 10018，loopback `UP`。公开 `/agent/map` 命名只读探针获未登录 401；默认 curl 被既有 Nginx 规则拒绝，公网 actuator 未暴露，不能宣称已验证登录业务。
- 原 Run23 deploy 在 installer 前因协调 FD 继承失败。修复父 coordinator 持有 v2 mutex、installer `close_fds=True`；17 项控制测试通过，单次只重试部署 Job，新 JVM 无协调 mutex FD。未解除旧锁或手动终止服务；生命周期由 Flow 安装器完成。helper SHA `d3c7bb4fa94c5628068bdac3b9ecb2b332031811c42dfd15a8b48e1113ccd311`。
- 19:24 只读云端配置确认两组件均为 Gitee/develop/push/^develop$，webhook 已存在；此前“前端 push 未启用”描述已过时。配置存在不等于实际 push 自动触发已验收，下一次真实 push 先对账，不重复手动 Start。
- API 发布包、A03/A16 只读增量及 mail 运行依赖修复已闭环；完整 A16、M4/M5、案卷阁登录验收及付费业务仍未完成。A16/E01/F03 已分别派给并行 Owner，无独立 Reviewer。邮件监控已观察 SUCCESS，但三次邮件 helper 未接受，不能宣称邮件已发达。
- 完整精确证据：`/home/isp/wsps/cyf/docs/implementation/handoffs/FLOW-API-RUN23-DEPLOYED-20260912.json`。

## 2026-09-12 20:36 CST 增量

- API Run25 SUCCESS：develop `ef1a9659`，JAR `ea9de1bd`，order69508149，PID2659818/healthUP。63类范围测试构建成功；E01评分及顺序修复已发布，F03仅增加默认健康隔离测试。完整证明见 `docs/implementation/handoffs/FLOW-API-RUN25-DEPLOYED-20260912.json`。
- Web Run93 **Flow FAIL / installed+online verified**：develop `b58d3727`，2119pass/2pending；410安装文件及9线上哈希全部匹配。原20:23:23首页校验不匹配，之后同请求已匹配，原因尚未知；不改写失败、不重复部署。实际自动push触发已证实。详见 `docs/implementation/handoffs/FLOW-WEB-RUN93-ONLINE-WITH-FAILURE-20260912.json`。
- Web安装器反复gzip随机seek的独立性能问题由Owner改为有界顺序staging，并补最终只读重验诊断；不降低制品、路径或身份校验。A16异步受理基础 `9672b4bc` 已push，保持default-off，不声称执行器已完成。


## 2026-09-12 23:00 CST 增量

- Run31/f6554168 已 SUCCESS，初次容量拒绝发生在停机前，same-artifact retry69510726部署成功。canonical JAR/record/healthUP 已复核；API push 自动触发仍未证明。
- 后端配置当前66selectors，canonical05d595b2；云端显示名并发变为cyf-api-release，ID5260799与YAML未变。E02 develop00db已提交，单次Run32观察中；Web develop1b3自动Run94观察中。仅云端终态+制品+在线证据可更新发布gitlink。


## 2026-09-13 登录修复与门禁精简验收

- 删除无测算依据的固定资源/大小阈值及本地超时判败，24 项相关控制面回归通过；三个线上 helper 的候选摘要与 readback 一致，未清理历史备份。
- API Run36 SUCCESS，commit `5ece9141e66f27aa2d5443dada1ea816e44ca95c`，deploy order `69520177`；JAR SHA-256 `1c073e3bf7928bf9f057d81d33265fe8323384247a112ab5cd2111df811925b9`，PID3257882/health UP，包含 `80383a07` 登录表单与 CORS 修复。
- 公网预检明确包含 x-request-id，未登录 map 返回可读401，无效 code 的 token 表单返回400 invalid_grant而非302登录页；真实账号及第三方/微信交互仍需用户重试确认。
- 精确证据：`docs/implementation/handoffs/FLOW-AUTH-GATE-FOLLOWUP-VERIFIED-20260913.json`。


## 前端发布验证范围与缓存（2026-10-09 核验）

核验源码：Web `81f49518c3f23f794f9d37f4ac0be024d65d9f55` / tree `5595dab02479b49b3ef803eda6c84c67ef22ecb9`；Flow4403172 Run188 SUCCESS，普通验证总176秒（2分56秒），2790通过/2pending/0失败、Mocha72.298秒，Vite11.28秒，制品及并行JS扫描成功。**本次未部署/未在线核验**；不据此宣称完整版本发布或所有候选均在5分钟内。

按用户追加授权，默认release profile保留业务/身份/ACL/幂等/交付/恢复及实际游戏运行时回归；16个离线资产作者工具/E13重算/E14性能验收文件单列assets/all。涉及`public/juyiting`、资产生成器、renderer、E13/E14或其fixture/验收工具修改，Owner必须在固定SHA选择`CYF_TEST_PROFILE=all`的Flow，不得用release成功代替资产验收。assets/all保留原签名/SHA及10秒预热/60秒采样。覆盖以同Run `ci-profile.json`为准（旧job标签含full tests不代表all-profile）。不改版本化发布、制品来源/摘要、部署互斥/恢复/健康或develop不自动部署规则。

只读清单确认旧缓存10份历史runtime提取目录总4.145GB（未压缩），npm下载缓存仅43.73MB。新提取目录移出Flow缓存，仅清理当前独占worker恢复的旧实体目录、不跟随链接。Run188缓存归档355.91MB，归档与上传约5秒且成功；旧Run186归档2.011GB、76秒并因平台2GB上限未上传。删6个无消费者直接开发依赖，lock减少95项，保留包版本及完整性未变；删除脚手架测试并合并重复正向重算，负向篡改测试在assets/all保留。

Run187的manifest原只接受x.y.z，拒绝合法既有prerelease；已保存前值、修正严格SemVer校验并单次update/readback，根模板同步，Run188证明该配置候选成功。Flow SHA `719b28019ba51985a11a60dd2af99ed3a336d4de760004301dd0c2336e2a65a3`。详细scope/失败/授权及未验证项：`docs/implementation/handoffs/FRONTEND-RELEASE-5M-20261009.md`；正式摘要：`docs/implementation/evidence/frontend-release-5m-20261009/summary.json`。

### 后端CI分支不作白名单（2026-11-02核对）

- 按用户明确要求，`cyf_orchestrator.py`、`backend-ci-run.sh`及制品封装不再用历史分支名单决定是否可运行；policy删除`branches`，分支名只记录来源。保留真实Flow身份、固定commit/tree、干净源码、策略argv/fixture摘要、fresh输出与制品完整性，不授予部署权限。
- 默认模板为手动触发（`triggerEvents: []`）、`branchesFilter: .*`、单job10分钟；不因允许任意候选分支开启push自动运行。整体Run600秒上限及本机监控责任不变。
- 2026-11-02已在无活动Run时备份并更新后端5260799，readback canonical SHA `a3c41b0195a62f9d226f77e07d992baee358863afa209939d771c52c06d307ad`；本机16项工具回归通过，未为配置变更另开付费构建，未部署。此处覆盖下方历史三分支/push口径；后续修改仍须核对实时配置。
- 基于当前root工作区增量修改并保留原有未提交内容，尚无本次独立源码commit。变更前值、task-only patch、测试和云端回读见 `docs/implementation/handoffs/JUYITING-PERFORMANCE-20261102.md`；不将配置落地当作技能缓存应用回归全部完成。

## 后端默认提速配置维护（核对：2026-10-20，工具源码39ba13ee）

- 默认CI维护入口仍是 `ops/ci/aliyun-flow/templates/backend-develop-release.yaml`（名称不代表部署）。`backend-ci-run.sh`维护云端步骤，`backend-ci-policy.json`维护精确Gradle argv；修改后运行 `python3 ops/ci/aliyun-flow/prepare-backend-ci.py --output /absolute/candidate.yaml` 离线渲染，再按原控制工具无活动Run/备份/单次写/readback流程固化。不得直接保留旧版本候选的固定commit/任务snapshot作为默认。
- 既有orchestrator的 `gradle --flow-ci` 仅用于5260799默认CI；固定配置授权只验证原分支，逐Run绑定真实commit/tree、策略SHA、完整argv、干净源码及fresh输出目录，保留原Gradle互斥。该上下文不是人类任务Owner、不读写共享ledger、不接受整轮EVIDENCE_HIT，不提供版本部署权限；正常任务入口仍按原ledger准入。
- 默认启用Run197已验证的 `--parallel --max-workers=3`、compile-only缓存及Test-only C1；不增加每task fork、不复用Test/layering/JAR。生产JVM与JIT/性能基准不套用Test C1 profile。缓存冷启动与worker波动仍会影响耗时，单次283秒CI不是发布总耗时保证。

- 首次固化的历史基线：14:46 readback canonical SHA `cc7d7b7d429092a78193fa3a08a5846ff72fffb4bba474399c42c04a4359641b`；原push/分支过滤保留、无部署。`Run199 SUCCESS`：**284秒（4分44）**，Gradle161.942秒，2728项/0失败/0错误/122跳过，302套件与Run195独立XML逐项计数一致，32个指定任务全部fresh。制品独立下载核验229027426bytes/SHA `d194f08eb94bf9d859d7fde0586c2ff7a2040f1886b19601c39ec474316dee75`，Run/完整源码/clean绑定及JAR摘要均匹配。证据 `docs/implementation/evidence/backend-flow-5m-20261020/default-*`。
- 这是默认CI实测达标并固化，不代表包含生产部署的整条发布已≤300秒。Run195发布日志仅知停止33秒、健康等待61秒及稳定核验；尚缺完整部署阶段计时。后续实际版本候选应携带已验证profile，并按当前helper契约启用已有观测，不能把默认无部署CI或旧Run回执当成新版本上线证据。

#### 避免重复工具链准备与缓存观测（2026-10-20）

- 保留 `JavaBuild`，仅平台 bootstrap 设为预装 `jdkVersion: "1.8"`；执行 Gradle 前仍由固定 SHA 的 `prepare-backend-jdk.py` 校验、fresh解包 Dragonwell21 并强制替换 `JAVA_HOME/PATH`。这不是将编译/测试降到Java8。原argv、compile-only策略、Test C1及单task fork均不变。
- 固定API `9ca2776c27ce3270efa0ea4c366b7de0e68e8dbb` / tree `847927f2fc9d76ca09cee79dc7aa987a627450c5`，Run200 SUCCESS **216秒（3分36）**，Gradle114.116秒；独立下载解析302份XML，2728项/0失败/0错误/122跳过与Run195逐suite一致，32个指定任务fresh，JAR摘要仍为上述 `a71821be...`。与Run199相比总计少68秒，其中Gradle自身少47.826秒，不能把全部差值归因于平台JDK准备，也不作固定节省承诺。 同配置不改源码复测Run201 SUCCESS **228秒（3分48）**、Gradle123.419秒，测试和fresh任务再次一致；两次均在5分钟内，仍不是长期SLO或冷缓存保证。
- 缓存只做观测、不删除。Run200固定标签数值库存：Gradle缓存约1032MB（modules-2约495MB、compile cache约145MB），Maven约447MB，JDK归档约218MB，MySQL归档约48MB；这些是目录占用，**不是压缩归档贡献量**，总计不能与913MB归档直接相减。库存嵌入既有 `test-results/summary.json`，无新增installer不支持的归档成员，无文件内容/凭证输出，观测错误不作为构建门禁。
- 约447MB Maven目录是阶段内库存，不能推定其远端压缩贡献；15:55后续Run202—206没有证实缓存路径/移动/排除/快压缩带来可复现的额外缩时，均已撤回，见下节。Gradle实际版本9.3.1，实验库存约382.7MB；最终恢复的原默认仍有旧8.14.3=0标签，不能把该0解释为当前版本无缓存。固定JDK/MySQL归档及每次SHA校验保持不变。

- 本轮保留新默认 canonical SHA `9671c967564668b0e94bdc956db2248175c78a8f65a803187e55f4d5567ae3e2`，无部署阶段，原push和分支过滤不变。Run200/201独立制品/XML、候选及最终readback证据见 `docs/implementation/evidence/backend-flow-5m-20261020/further-*`；源码实现、CI历史和当前线上版本分开记录，本轮未发布或重启生产，完整发布五分钟仍待授权版本的同Run实际验收。

#### 缓存继续压缩的实测边界（2026-10-20 15:55核对）

固定同API源码，Run202/203/204/205/206均CI SUCCESS，分别280/244/279/255/276秒，Gradle163.062/139.551/165.353/147.819/165.732秒。原2728项/0失败/0错误/122跳过与302suite不变；Run205/206另独立下载制品、解析XML逐suite对比Run195，并核验32个fresh任务及相同JAR摘要。源集计数可能重叠，不能累计当作独立用例。全批4分04—4分40；此前216/228秒是较快样本，不是稳定SLO，Gradle波动来源尚未单独定位。

- `cacheDirs`追加JavaBuild默认目录，不覆盖默认.m2等路径；设置成功不等于有效范围变小，Run202不接受。
- Maven仓库与/tmp、HOME均跨设备；两次原子rename候选由安全分支跳过，未复制/移动/删除缓存文件；不继续猜测目的路径、不跨盘复制或清目录。
- GNU tar排除在隔离工具测试有效，但Run205实际缓存仍约913MB，未证实平台缓存插件上下文中的收益；撤回TAR_OPTIONS，不把库存447MB写成可节省447MB。
- Run206的GZIP=-1确实进入构建环境，同Run制品gzip头XFL=4；但缓存打包到size仍约18秒，与Run205相同，缓存约913.46→929.04MB（增约1.7%），制品229.03→230.24MB。未获得足以接受的缩时收益，且该GNU gzip环境接口有遗留维护成本，撤回，不永久化。

15:55无活动Run、配置归属核对后已单次恢复并readback原**9671c967...**默认；原push/三分支/Java21来源与SHA/并行/C1/compile-only/fresh门禁和无部署保持。运行脚本/模板/默认工具测试恢复与Run200/201相同字节，所有实验helper及其专属测试退出当前默认；只保留历史提交与证据，不删除应用测试。最终26项相关工具隔离复核通过；恢复后未为重复计时额外触发Flow。当前缓存文件可能仍为上轮快压缩格式，标准gzip可读，不单独清理或跑构建来重写。

证据 `docs/implementation/evidence/backend-flow-5m-20261020/cache-investigation-*`、`slim-*`及`fast-gzip-*`。后续优先定位同源码Gradle耗时波动，或在明确授权版本发布中分段观测历史171秒部署开销；没有新版本部署/重启/在线验收，不把CI SUCCESS当完整发布五分钟达标。

### Gradle续调查：只保留可核验计时（2026-10-20，诊断源码63ed6b21）

覆盖范围仅5260799无部署CI、固定API `9ca2776c` / tree `847927f2`。不修改API业务、测试选择器/fixture、fork/worker数量、依赖完整性或fresh JAR规则，不含生产部署/重启验收。

- 已有Run199/200/201/205/206的302份XML显示，快慢轮次的case累计时间和多个模块及bootJar同步变化，不是只有Gradle启动阶段变慢。suite/case/task累计都是并行任务的累计wall time，不是CI耗时或CPU时间，不能相加后当关键路径，也不能无证据归因worker。
- Run207额外给Gradle自身JVM加C1：CI229秒、Gradle126.770秒，未显示明确收益，已撤回；原Test-only C1保持。Run208把最重Chat回归完整argv块提前，测试/选择器块多重集合不变：任务确实提前，但自身44.76→71.56秒，CI244秒、Gradle136.394秒，没有净收益，也已撤回。不能把“提前启动”当作“更快完成”；MySQL的具体慢因尚未拆出，不调整事务/持久性语义或等待限制来换数字。
- 默认恢复原policy字节及任务顺序，只在既有diagnostics增加阶段elapsed/JVM uptime/进程CPU累计/处理器数和Gradle C1布尔readback，任务增加start offset；`rootBuild`区分主build和included plugin build。offset相对各自init起点，不同build不能直接相减；JVM uptime为另一锚点。所记录进程CPU仅Gradle JVM，不含Test JVM/MySQL，不能冒充整机CPU或整轮CPU耗时。
- Flow最终日志可能省略Gradle开头，即使`more:false`也不完整。阶段与任务数值记录写入既有`test-results/summary.json`，不新增installer不支持的成员，不输出原始环境/全部JVM参数；原JUnit XML仍逐份保留。优先下载同Run制品核对，不以日志缺失断言任务没执行。观测不增加性能门槛、不授权部署。

实验和精简证据见 `docs/implementation/evidence/backend-flow-5m-20261020/gradle-*`、`early-heavy-*`；原始日志/制品仍在原私有目录。当前无新增可复现缩时结论；216/228秒等历史快样本不是长期保证，也不是完整版本发布<=300秒的证明。

最终原profile+计时候选 **e0e87d84...** 已通过Run209：CI **272秒（4分32）**、Gradle164.751秒，独立下载同Run制品核验302份XML，2728项/0失败/0错误/122跳过及32个指定fresh任务不变，JAR仍`a71821be...`。主build taskGraphReady为自身init后10.356秒、JVM uptime15.501秒；它们不是整轮CI/Gradle命令耗时，进程CPU也不含测试/数据库。全部453条任务计时保存在summary，补足API日志开头缺失；主/嵌套阶段标识已实测。16:28:15+08只读readback配置一致、无活动Run、原push/三分支及无部署保持。此Run是最终诊断配置验收，不宣称新增缩时；旧9671c967基线仍保留可恢复，完整发布五分钟目标未完成。


### 已发布议事开关的生产默认值（2026-10-25）

Web1.16.46 / develop321f358f0d8289292c90374d7cce21a3423a27c3将既有多媒体议事、typed议事和follow-up执行的三个VITE开关固定在`.env.production`为true。它们此前已通过发布命令启用，不能在新版本构建时因遗漏命令行环境变量而回落旧`/chat/stream`。生产构建不再依赖某次临时Flow配置携带这些已发布默认值；显式候选覆盖仍保留，不自动开启职位技能/多区域或任何其他功能。复用`tests/production-build-flags.test.js`验证默认值。浏览器续聊验收需确认实际进入typed请求且资料/可用动作进入冻结上下文，首轮点将识图和HTTP200都不足以证明续聊链路。


## 已恢复的中断安装：复用原制品重试（2026-10-30）

源码核对：`jia-sdd develop 2072aac3`，范围仅`cyf-api-flow-install`的主机重试边界；不是应用构建/灰度能力变更。Flow必要测试与制品成功后，主机安装因中断恢复到旧JAR，不要求再开付费Run。

- 仅接受既有失败记录`status=failed`、`phase=activating_candidate_recovery`、`recovery=restored_healthy`（或`restored_healthy_after_stop_error`）；完整source/Run/receipt/candidate绑定、旧JAR摘要和真实健康仍由原安装器核验。测试失败、未知恢复、其他候选、启动失败不能用此入口绕过。
- 已授权Owner在原coordinator→release→lifecycle锁序下核对现状，保存失败/恢复证据，创建状态根内root-owned、0600、单链接普通文件`retry-authorization.json`。仅有三个字段：`schema_version:1`、`failed_record_sha256:原record.json完整字节SHA-256`、`reason:本次明确恢复后重试原因`。这是异常安装的新执行决定，不新增正常发布审批或云端Run。
- 原下载/安装入口仍使用相同不可变制品。安装器在原release锁中将失败记录原字节和一次性授权归档至`retry-history/<failed-record-sha256>/`；授权消费后才进入原prepared/backup/stop/install/health/commit流程。不删除失败记录、不将历史失败改成成功、不跳过锁/备份/摘要、不伪造CI身份。相同授权不可重复消费，异常中断须检查真实状态再决定恢复。
- 定向回归入口：`ops/ci/aliyun-flow/tests/test_api_flow_restored_retry.py`（6例）及`test_api_flow_install_lock.py`（5例），均为本机轻量隔离fixture，不构建应用、不访问生产服务。
- CYF本次安装器新增边界已备份并部署，具体helper前后SHA与记录见`/home/isp/state/cyf-full-tenant-gray-20261029/verify-release-20261030/retry-adapter-change.json`。首次安装TERM来源未归因，不把重试支持误写为已修复外部信号来源。

### 目录归位补记（2026-11-07）

按用户要求，构建JDK已原子迁至`/home/isp/apps/dragonwell-21.0.11.0.11+10-GA`，540项文件/权限清单完整核验，旧工具链目录已移除；不保留旧路径软链接，不改生产Temurin或重启服务。缓存仍归state；API/Web压缩包是受控安装输入、恢复及来源追溯副本，不是服务运行目录，服务不从压缩包直接运行。当前包归档暂保持原位，未借目录整理删除或改写当前/回退绑定。历史持久化证据中的旧JDK路径保留为当时事实，后续命令使用新路径。迁移凭证：`docs/implementation/evidence/local-release-closure-20261107/jdk-layout-20261107.json`。

### 主机目录职责归位（2026-11-07后续更新）

安装包镜像现位于`/home/isp/pkgs/cyf`；本地构建任务/缓存归`/home/isp/state/cyf-local-build`；旧维护档案归`/home/isp/baks/private-maintenance`，不再使用wsps存放运维归档。工作树按所属项目的`.worktrees`归属；空`cyf-worktrees`已删除，旧共享worktrees的15个任务目录保留待各Owner逐项收口。精确迁移与保留边界见`ops/maintenance/HOST_DIRECTORY_LAYOUT.md`，不将历史安装记录字符串重写成新执行证据。
