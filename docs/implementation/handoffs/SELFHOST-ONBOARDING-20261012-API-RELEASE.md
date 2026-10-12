# SELFHOST-ONBOARDING-20261012-API 发布输入

## 固定范围（2026-10-12）
- Owner：SelfhostApiRelease / api-release-owner；经现有 orchestrator claim 本 API task，无 Reviewer。
- 已读接收确认：`/home/isp/wsps/cyf/AGENTS.md`、`ops/orchestration/README.md`、Main handoff、`specs/runtime-self-host-onboarding/design.md`、`/home/isp/AGENTS.md` 及服务器架构相关段落。后端正式本地规则覆盖旧技能双 Flow 说明。
- 目标 API **1.14.11**；只正式后端验证、不可变包、原安装器输入检查。不安装、不重启、不写生产 DB，不生成安装授权，不修改 Main handoff/其他 task/全局工具。
- 固定源码：`0fe830d1ea39b89de89475ef2d1f21dfc7577da2` / tree `b365003e141101350af123185b2bf2ec0e80ec16`；22:54左右本地 develop 干净且实际 ls-remote 一致。线上用户给定 1.14.10/cd1e6d6，待只读核验；不以远端查询代替上线状态。
- Detached 干净 worktree：`/dev/shm/cyf-selfhost-onboarding-api-20261012-source`。
- 私有 scratch / build ID：`/var/tmp/cyf-selfhost-onboarding-api-20261012` / `cyf-selfhost-onboarding-api-20261012`。
- 外部 build root：`/dev/shm/cyf-selfhost-onboarding-api-20261012`。
- 验收：完整 managedHostingRegression（保留8个原类，含新增Provisioning与H2事务/ACL），私有固定init追加 Runtime V1 Controller 与真实 HttpSecurity 集成测试；PublicArtifactVerifier、POI、validateLayering、fresh bootJar 与 OpenCV来源/SHA核验。Test/JAR不复用缓存，只JavaCompile可复用。
- 所有Gradle经原串行入口，固定本task/tree/selector/fixture与实际effective argv；所读构建输入哈希见scratch/build-input-read.json。无源码修改。
- 空间：固定源码约32.4MB；参考原同类JAR约254MB，tmpfs用于源码/编译/JAR，根盘用于单份包与小证据；打包前实际测payload，不清理他人、不设置额外门槛。观测详见scratch/scope.json。

## 进行中
正式验证运行中；未声称通过或上线。完成后补齐真实测试数量、日志、包SHA、原安装器可用性和Main下一步。

## 自然接续 23:07
- 首轮Gradle退出0（265.669s），但175项含1项环境条件跳过：`UnixManagedHostingProvisionerTest.actualJavaAdapterDrivesRuntimeInitialReplayAndFreeNewSessionWithoutCredentialWire`。打包前零跳过检查拒绝，无首轮包。经orchestrator归因缺少显式Runtime fixture输入；首轮完整日志/原XML已持久保留，不能用于发布。
- R2固定干净Runtime fixture `5d2d3f8bec903a87eed684936efc3f3d21e891e2` / tree `2351f07341d1fec59d070aa7d9860f7fbb9fdc0c`，独立worktree `/dev/shm/cyf-selfhost-onboarding-api-20261012-runtime`；Node路径/版本/SHA见R2 `runtime-fixture.json`。仅私有UDS/合成Native API和执行器，不访问生产Runtime/API。
- 正式采用新build ID **`cyf-selfhost-onboarding-api-20261012-r2`**，scratch `/var/tmp/cyf-selfhost-onboarding-api-20261012-r2`，build root `/dev/shm/cyf-selfhost-onboarding-api-20261012-r2`。API源码仍同一0fe/tree，无修源码。
- R2正式Gradle退出0；XML实测 **175 tests，0失败/0错误/0跳过**；完整原hosting8类+追加Runtime Controller/真实HttpSecurity2类均有测试。正式包生成中。
- 只读安装输入核验：现行1.14.10/cd1e6d6与记录一致。4个现行helper与workspace迁移后源码不同；但全部6个现行helper均匹配现行catalog指向的真实Git源码 `6cec87ae1b680bbd4ef9a86ffb3a03c4c77d98bb` / tree `2395e82636922790f5aab9e898fcb5a87f2d3a4d`。所查schema plan/catalog/helper/直接proof引用全匹配；不是递归完整admission或新catalog/DB验收。
- 已在R2 scratch准备本任务专用 `prerequisites/prepare-release-inputs.py`：固定1.14.11/0fe/R2，按已核实历史源码核验**现行helper**（不覆盖现行工具），只保留prepare-only、无授权/decision生成能力。语法和--help通过，尚未执行准备主体，须Main提供本批admission与fresh runtime/schema readback。旧任务ID/授权/测试/发布证据未复用。

## 最终交付（2026-10-12 23:12，取代上文“进行中”）

**本切片完成：正式验证及不可变制品READY，安装/上线未执行。Main负责后续admission、fresh安装前快照、授权与安装决策、安装及在线验收。** 23:10实际ls-remote再核对，API develop仍为以下源码且原组件与受测worktree均干净。

| 项目 | 实际值 |
|---|---|
| 版本 | `1.14.11` |
| commit | `0fe830d1ea39b89de89475ef2d1f21dfc7577da2` |
| tree | `b365003e141101350af123185b2bf2ec0e80ec16` |
| build ID | `cyf-selfhost-onboarding-api-20261012-r2` |
| 完整测试 | **175 / 0 failed / 0 errors / 0 skipped** |
| hosting＋Runtime | 109；其中Provisioning 6、Runtime V1 Service 18、Controller 8、HttpSecurity 30、Unix桥接12（均实跑）、H2事务5；其余原hosting回归完整保留 |
| PublicArtifactVerifier | 64 |
| 生产POI类路径 | 2 |
| `validateLayering` / fresh `bootJar` | 原任务实际执行，非cache/up-to-date；PublicArtifactVerifier原bootJar doLast通过 |
| 编译缓存 | 198 actionable，124 executed、74 from cache；Test/JAR不缓存，正式Gradle耗时169.819s（不含锁等待） |
| OpenCV | `org.opencv:opencv:4.5.5` / 722802 bytes / SHA `323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4`；固定来源、消费前核验 |
| 包大小 | 226678838 bytes |
| 包 SHA-256 | `e31fee595b2d1d9b036d4674ff57ddcf7def2a51a156b08613c6add0388c1d83` |
| JAR大小 / SHA-256 | 253879126 bytes / `abb79efc46b19a0d126852bf37cdc895c8ccf7454a66d7b79053421f3bbe63a4` |
| build evidence SHA-256 | `51153f23ec9bec45f2c96760ef28d20f11a7bc4b65ace8abe4d65932124732fb` |
| log SHA-256 | `6e01cfa0bcede5d23a231a086a7f6f5f1a179978b51d3a87dfa2722b7219732a` |

### 精确路径
- 不可变包（0400，原producer生成、独立流式复核全部5个payload）：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/package/cyf-api-1.14.11-cyf-selfhost-onboarding-api-20261012-r2.tgz`
- 原构建日志：`/dev/shm/cyf-selfhost-onboarding-api-20261012-r2/local-build-sanitized.log`
- 持久日志：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/durable-build-evidence/001-local-build-sanitized.log`
- 原build evidence：`/dev/shm/cyf-selfhost-onboarding-api-20261012-r2/local-build-evidence.json`
- 持久build evidence：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/durable-build-evidence/000-local-build-evidence.json`
- 原XML及输入/日志/proof的逐文件持久副本与映射：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/delivery-readback.json`；`durable-build-evidence/`。保持原始引用路径与证据字节不改写；Main应先通过admission快照引用，再退役本任务tmpfs。
- 测试逐类计数：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/test-summary.json`
- 实际effective/requested argv、cache policy、Runtime/Node固定输入：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/source-validation-input.json`、`local-controller-build-input.json`、`runtime-fixture.json`。
- 无新schema操作的源码/JAR字节证据：`/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/schema-source-continuity.json`，**218个SQL/SchemaInitializer成员与现行JAR字节一致**；只证明字节连续性，不是实时生产DB catalog/DDL验收。
- 现行helper目录与引用：R2 `prerequisites/helper-catalog.json`、`installed-input-audit.json`、`installed-prerequisite-ref-readback.json`。全部绑定实际installed字节，未覆盖dirty默认路径迁移源码，未生成安装授权。

### Main下一条既有入口与未完成条件
1. 先处理真实空间需求（不擅清他人）：23:09:47根盘可用 **404217856 bytes**；原admission仅“再写package＋5payload”至少 **480566253 bytes**，差 **76348397 bytes**，另需证据快照/目录/控制记录及后续安装incoming、candidate、备份。空间有并发变化，应重读实际值；这不是新增硬门槛。当前尚未执行admission，未写共享发布状态。
2. Main基于本批实际证据生成新的protected controller/trusted-record/batch-authority（制品准入，不是生产安装授权），调用原 **`/usr/local/sbin/cyf-api-local-admit --opt-in ...`**；不能复用旧任务authority/receipt。wrapper `--describe`只读已核实。旧capture脚本可按本批结构适配，但不能复制旧ID/授权/证明。
3. `prerequisites/prepare-release-inputs.py` 已按本批源码/版本/ID适配，**仅prepare-only**，语法/--help已核实；主体未执行，需要Main本批admission和fresh runtimeGeneration、identity/inflight、F06/E05 schema只读快照。现行helper来源固定到与installed一致的历史Git源码，而非dirty workspace。无安装decision或maintenance-authority输出能力。
4. Main补实际用户授权快照和本批完整决策后，原安装入口（下面占位符不是现成决策）：
   ```text
   /usr/local/sbin/cyf-api-flow-deploy --local-inspect --decision <本批install-decision.json绝对路径> --decision-sha256 <本批decision SHA256>
   /usr/local/sbin/cyf-api-flow-deploy --local-install --decision <同一精确决策绝对路径> --decision-sha256 <同一SHA256>
   ```
   API最终安装位置仍为 `/home/isp/hosts/cyf/api/cyf-api-kit.jar`。Main安装前复核现行JAR/record/process generation，原统一锁/身份/备份/恢复/健康/业务验收不可跳过；不得整文件安装他人dirty helper。

### 收口边界与耗时
- 没有源码修复、生产配置改动、维护/重启/安装、DB读写连接、真实Runtime登记或Provider调用；原生产JAR仅只读比较。
- 本任务API验证/制品交付完成，不代表Main跨组件发布完成或API1.14.11已上线。
- 定位/实现/等待：未独立精确计时，留空；正式Gradle首轮265.669s（1 skipped，不可发布），R2 169.819s（175全过）。不将两轮缓存效果推为整体开发缩时承诺。

## Main安装准备补充（23:19后）
- Main真实新授权已读取并按字节绑定：`/var/tmp/cyf-selfhost-release-20261012/authorization-evidence.json`，SHA `27628ed2e670c61448787bff4a9f4e7940ca0c2a665b895e0cc018c4906b8621` / 955 bytes；用户逐字“那就都更新”与Main解释明确区分。未执行安装授权生成。
- R2 scratch新增Main执行用 `capture-actual-controller-proof-main.py`（写本批protected artifact证据，不安装）和 `prerequisites/prepare-release-inputs-main.py`（支持Main `--finalize`，固定上述真实授权SHA）。两者已语法核验，后者--help通过；**均未运行主体**，原prepare-only脚本保留。Main版重新绑定1.14.11/0fe/R2/现行installed helper；不是使用旧任务授权。
- 原脚本链：Main运行capture→原`cyf-api-local-admit`→原admission只读`--verify-published`→fresh runtime/schema readback→Main版prepare `--finalize`→原local-inspect/install。当前没有admission或install-decision可直接执行。
- 分阶段空间详见R2 `space-plan.json` / `space-plan-latest.json`：controller snapshot已知917145 bytes；admission新增481483398 bytes＋authority/admission JSON；incoming临时副本226678838 bytes，正常原子覆盖旧incoming后净增3157 bytes；解包＋旧JAR备份507764314 bytes。目录/块分配、尚未生成的JSON和并发增长另计，不加人为配额。
- 推荐少改路径方案：保留原producer包直到原admission发布且`--verify-published`完整通过，然后仅退役本任务原包 `/var/tmp/cyf-selfhost-onboarding-api-20261012-r2/package/cyf-api-1.14.11-cyf-selfhost-onboarding-api-20261012-r2.tgz`（226678838 bytes），记录退役证据与admitted package的新精确引用；保留全部源码、fresh JAR、日志、XML、proof、所有旧恢复备份。admitted package＋payload均在引用闭包内，不可删除任何一个。该方案从“当前已持有producer包”的基线起，整链额外峰值下界为 **763489176 bytes / 728.12 MiB**（已含两份snapshot，另需上述未定元数据/分配）。不能把可退役包算作提前已有空闲。
- 若admission前空间不足，可先将仅本任务producer包复制至私有tmpfs、逐字节SHA/size验证、fsync/readback，新建relocation记录并让Main在authority生成前绑定新`--package`路径，再删除唯一根盘副本；不可symlink/hardlink，不改原producer回执和制品字节。这只是移动同一包，整链净空间收益相同，不解决所有不足。当前未实施任何搬移或删除。
- 原installed admission固定输出保护根；installer候选须同canonical文件系统以原子replace，不能挪到tmpfs或删除/链接已发布payload绕过。只清本任务编译classes/generated/tmp仅释放tmpfs，不释放根盘；不触碰共享缓存、其他任务、runtime-path-unify备份。
- **最新空间纠正：23:20:33实测根盘可用2616651776 bytes / 2495.43 MiB**（本API任务未清理或搬移任何文件）。已足以覆盖不退役producer包的整链新增下界 **990168014 bytes / 944.30 MiB＋元数据**；建议当前不删除任何副本，Main执行前再读空间。上面低容量观测仅为历史时间点，不继续声称当前空间阻塞。
