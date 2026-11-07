> **2026-11-06 现行规则：** 用户告知云效额度用完，CYF 默认改为本地测试、构建、打包和受控部署；不自动启动 Flow。正式证据绑定真实本地构建批次、完整 commit/tree、必要测试与制品 SHA-256，不伪造 Run/CI 身份。保留发布授权、身份/ACL、锁、备份、可恢复安装与线上验收；develop 不自动部署。Gradle 仍先读构建文件并经现有编排器串行执行。下文冲突的 Flow-only/禁止本地构建说明仅作历史，完整规则见根 `AGENTS.md`“本地构建与部署（2026-11-06 用户最新决定）”。2026-11-07已完成Web/API原安装器LOCAL适配与同批实测；默认快速路径见本文末节，长期策略见 docs/aliyun-flow-cicd-strategy.md 的2026-11-07节。

> 下方旧Flow-only说明保留作历史；当前入口见本文末节。

# 当前交付入口（2026-10-17）

前后端正式测试、构建、制品与版本部署统一走云效 Flow：前端 `4403172`，后端 `5260799`。本地工具用于控制面和定向诊断，不替代正式 Flow 验收，不执行本地生产打包/部署。develop 不自动部署；发布绑定固定源码、同 Run 制品和在线核验。规范见根 `AGENTS.md` 与 `docs/aliyun-flow-cicd-strategy.md`；本次仅改文档，不变更工具或云端配置。

## 后端默认 Flow CI（2026-10-20）

`5260799` 默认配置的源码为 `ops/ci/aliyun-flow/backend-ci-run.sh` 和 `backend-ci-policy.json`；离线渲染使用 `prepare-backend-ci.py --output /absolute/candidate.yaml`，仍通过既有 flow-control 固化，不在本机运行Gradle。细节见 `docs/aliyun-flow-cicd-strategy.md` 的默认提速维护节。

云端仍用本编排器的 `gradle --flow-ci`：精确Flow身份/策略argv/当前干净commit/tree、新输出和原Gradle锁；不读写人类任务ledger、不复用整轮结果、不授权部署。普通任务不要使用此模式，原task guard保持不变。

2026-10-20续调查（诊断源码63ed6b21）只增加可核验数值计时：同Run制品的既有`test-results/summary.json`含`gradlePhases`与`taskTimings`；用`rootBuild`区分主/嵌套build，各自offset不混算，JVM uptime另列。Flow日志可能省略开头，优先查同Run summary/XML。Gradle JVM C1和重任务优先实验均无明确净收益，已撤回，原policy/顺序及Test-only C1不变；没有新增缩时保证，不部署。

# 开工诊断（DEV-FEEDBACK-PILOT-20261008）

在现有 `cyf_orchestrator.py` 增加 `preflight`，不另建台账或准入门禁：

```bash
python3 -B ops/orchestration/cyf_orchestrator.py preflight TASK_ID \
  --cwd /absolute/path/to/task-worktree --component api \
  --baseline origin/develop --selector ':module:test --tests ExampleTest' \
  --fixture path/to/synthetic-fixture.json
```

- TASK_ID 必须存在；cwd 必须是仓库/worktree 根。baseline 显式指定，只读取本地引用，不 fetch，也不宣称远端最新。跨仓任务逐仓核对，台账 SHA 不匹配时先确认它绑定的是哪个组件，不自动改台账。
- JSON 输出 HEAD/tree、分支、是否脏、任务 SHA 是否匹配、基线双方独有提交数、工具是否在 PATH、根构建文件和指定 fixture 是否存在。
- 不执行 java/node/gradle/npm、候选 selector 或 shell；不读取 fixture/凭据内容，不下载依赖、不连接数据库、不修改任务或发通知。文件存在不等于内容/schema/依赖就绪。
- 当前 ledger 不含 owned_paths/worktree 映射，路径冲突明确 UNKNOWN；仅列其他 Writer 作为人工协调线索，不能声称无冲突。锁可用性、数据库和工具版本也未验收。
- Findings 仅建议，正常观察退出0；未知任务、非仓库或无法读取退出2。这不是测试成功、正式构建或发布批准。
- 前后端正式验证分别走 Flow4403172/5260799；后端在云端干净精确输入上先读 build.gradle，再经原 gradle 入口串行验证，保留 validateLayering。preflight 不绕过现有锁、授权或失败处理。

隔离测试（只创建并清理自己的临时 Git 仓库）：

```bash
python3 -B -m unittest discover -s ops/orchestration/tests -p 'test_preflight.py' -v
```

共享契约试点见 `specs/juyiting-execution-recovery/contract-pilot/README.md`。它复用实际前端消费者，但完整 Java HTTP/数据库层必须单独验证，不能以替身响应 PASS 替代。

## 执行历史：单命令定向验证

`execution_history_check.py --task-id TASK_ID --api /absolute/clean-api --web /absolute/pinned-web`

- 加 `--check-only` 仅预检；不自动创建/接管任务或改基线。cache miss运行要求该任务已在现有验证阶段。
- 先语法/合同检查和廉价消费者回归，再经原编排入口运行真实HTTP/MySQL测试及分层检查。无自动重试、安装、发布或前端本机生产打包。
- 命中精确输入并核验完整证据时返回 `REUSED`，不启动Gradle/MySQL；缺失或损坏的证据不能复用。根目录普通文档变化不触发重建。
- 一次性环境准备、凭据来源、完整命令、证据边界仍以 `specs/juyiting-execution-recovery/contract-pilot/README.md` 为唯一详细说明。
- 工具本身的隔离测试：`python3 -B -m unittest discover -s ops/orchestration/tests -p 'test_execution_history_check.py' -v`。这些工具测试不是实际跨端验收证据。

- 执行历史可追加 `--browser`：在同一Java/MySQL存活窗口驱动生产组件Chromium页面；非整站、非正式前端Flow。源码/辅助桩/浏览器指纹/截图证据边界见同一contract-pilot README。

## 历史后端本地构建：受控持久依赖缓存（2026-10-09）

> 2026-10-17起此节仅记录历史实现，不是当前发布入口。保留工具与证据供追溯，不授权本地生产构建或部署，不把本地 metadata init 直接移入 Flow。

**2026-10-09当时的正式本地发布默认启用**：既有 `gradle` 入口识别 `CYF_LOCAL_RELEASE_OPT_IN=1` + `CYF_LOCAL_GRADLE_ACTIVE=1`，核验显式metadata init的内容与固定compile-only策略一致后，无home参数默认 `/var/cache/cyf-gradle-local`（委托身份使用UID后缀），无cache flag默认加入 `--build-cache`。无需每次手传缓存参数；源码与build输出仍逐批隔离。Flow和普通专项诊断不受影响，显式 `--no-build-cache`、显式 `--dependency-cache-home` 保留诊断/隔离用途。与默认home冲突的旧 `GRADLE_USER_HOME` 需在调用端移除或明确绑定匹配home，不静默降级。

- 参数设置子进程 `GRADLE_USER_HOME` 并输出路径readback；目录必须canonical、无符号链接、由实际Gradle身份持有且0700。首次仅创建该目录，不自动创建父路径、不复制历史配置/daemon、不清缓存或他人目录。
- home不得有隐式 `gradle.properties`、`init.gradle(.kts)` 或非空 `init.d`；仓库/消费凭据仍由固定显式init配置管理，不将凭据写入home。冲突的环境/CLI user-home拒绝，不能悄悄落到另一个目录。
- 第一组对照仅复用依赖/解析/脚本缓存，`--no-build-cache`下仍重新执行207任务。正式本地候选默认 `--build-cache`（可保留 `--no-daemon`），配合本仓固定 `local-release-metadata.init.gradle` 的compile-only策略：只允许JavaCompile按Gradle输入指纹复用（包括测试类编译），所有非JavaCompile禁用输出缓存，Test额外禁止up-to-date；不复用测试报告或旧JAR。原定向测试、`validateLayering`、OpenCV来源/SHA、PublicArtifactVerifier、POI运行类路径和fresh bootJar仍执行。
- 默认策略不改基础证据键、源码核验、串行锁、身份或发布授权；接受旧整轮证据还须策略对象匹配。工具新增 `GRADLE_EXECUTION_TIMING` 实测子进程耗时，计时不含获取互斥锁的等待；没有deadline/资源门禁。
- 完整调用仍须固定任务、commit/tree、selector、fixture和工具链，逐批记录新输出/日志/制品SHA；不要直接套其它任务的示例选择器。构造fixture前可调用 `local_release_cache_defaults(args, requested_argv)`取得实际参数和策略，绑定effective argv及policy。原证据记录保存 `effective_argv`/`release_cache_policy`；producer证据必须写实际argv，不能把未补默认flag的requested argv冒充实际命令。正式发布只消费同批核验的制品。

本轮测量及边界见 `/home/isp/wsps/cyf/docs/implementation/handoffs/BACKEND-RELEASE-10M-20261009.md`；不是生产安装入口，不因此重启服务。

- 本地producer/admission的argv白名单允许 `--build-cache`，但不放宽所需测试/分层/bootJar任务的fresh日志要求，`FROM-CACHE`/`UP-TO-DATE`仍拒绝。`invocation.cacheHit=false`指整个验证未被EVIDENCE_HIT跳过，不表示JavaCompile未命中；实际命中以逐任务日志为准。
- 2026-10-09用户授权收尾已同步安装 `/usr/local/libexec/cyf-api-local/admit-api-local.py`；回读SHA `49ff62e470beadf5c5c570b007d1d30a6dd18b1f32df217274d89121ff77728b`，新flag可用且cached required tasks仍拒绝。原值备份 `/home/isp/baks/cyf-backend-cache-closeout-20261009/admit-api-local.py.before`。安装使用既有coordinator→release→lifecycle锁和原子替换，应用PID/start/JAR/health未变，无应用发布或DDL。
- 工具更新不改写历史批次的helper catalog/authority/receipt。下一次发布按当前固定工具重新生成对应批次的helper catalog；若恢复旧的精确批次且其catalog绑定旧工具，按同锁顺序先验证/恢复原helper（before SHA `a5d4f89693e02903001f148c5fdac1613d2756c26d334fd78702df054a16c32b`），不得绕过工具摘要或把旧回执重标新批次。


## SDD文档链路（轻量只读）

文档整理后复用 `./sddw check-docs [feature-id]`，全目录默认覆盖规则、当前索引和特性主文档，检查范围及历史例外见 [SDD说明](../../docs/sdd-workflow.md#sdd-document-check)。该命令不执行应用测试/构建、不修改pin/台账、不比较历史SHA与当前checkout；不能作为发布验收。既有 `sddw verify` 保留模板候选核验语义。工具自身定向回归：`python3 -B -m unittest discover -s ops/orchestration/tests -p test_sdd_docs.py -v`。
## 本地快速构建与受控发布（2026-11-07）

- API 构建入口 `local_build.py` 委托现有 orchestrator、跨任务锁和 Gradle；Web 构建入口 `local_web_build.py` 执行 npm ci、定向基线、原源码 Vite 配置与完整 public 打包。两个 builder **不安装**；新输出必须在干净源码和生产目录之外。
- 完整同批入口 `local_release.py --install`：显式固定任务、两端完整 commit、版本、工具链、缓存、全新输出与包外 evidence-dir。串行 Web/API 构建，再由已安装的原 helper 执行 LOCAL 受控事务，核对前代摘要、备份、健康、签名、安全边界和全部线上入口/JS/CSS 摘要。没有伪造 Flow Run，未恢复旧准入。
- 同批 600 秒从入口开始，包含准备、锁等待、测试、打包、安装和收尾；构建单元 `RuntimeMaxSec` 使用**剩余共同预算**，超时停止本批自有构建后定位，不原样盲重试。生产安装/JVM 必须在限时构建 cgroup **之外**，不能以到点为由强杀已切换的生产进程；原安装恢复保护保留，超时如实记未达标。
- API 热缓存仅复用已验证工具/依赖及 JavaCompile 产物；测试、validateLayering、fresh bootJar 均当批新执行。构建采用 Dragonwell21、C1 与 workers2/内部 parallel，不改生产 Temurin/JVM 参数，不带 `CYF_API_STARTUP_DIAGNOSTICS`。公共 artifact/POI 与认证/运行类路径/启动基线共105项，不是全功能回归。`--plan-only` 可查完整输入/实际命令而不构建。
- Web 保留生产 Vite 配置，public 原样流式打包而非复制两份；gzip1 和归档后释放自有 dist 控制峰值，逐文件验证完整包。基线47通过、2 pending，不能说全量测试通过。两端改业务仍须通过 `--api-regression-arg` / `--web-regression-test` 加入实际受影响回归；已知失败候选不能仅凭快速基线发布。
- API 正式 LOCAL producer/receipt 与 Web LOCAL v2 manifest 绑定来源、工具、测试报告和逐文件摘要；原 API/Web helper 已适配 LOCAL，保留旧 Flow 来源兼容、锁、原件备份与恢复。安装路径仍是固定实体目录。原始失败、取消和历史诊断均保留，不重标成功。
- 实测与可复用命令见 `docs/implementation/handoffs/LOCAL-BUILD-TIMING-20261106.md`；包外证据在 `docs/implementation/evidence/local-release-fast-20261106/`。热缓存实测不是冷构建或未来每次的时间保证。`/dev/shm` 输出是临时内存盘，不是持久归档；当前/回退绑定制品不能为腾空间直接删除。

完整入口参数（用真实任务/新批次替换占位符，`--install` 有实际生产副作用）：

```bash
/root/.local/bin/python3.11 -u /home/isp/wsps/cyf/ops/orchestration/local_release.py \
  --task-id TASK --batch-id NEW_BATCH \
  --api-source /ABS/CLEAN/API --web-source /ABS/CLEAN/WEB \
  --expected-api-commit FULL_API_COMMIT --expected-web-commit FULL_WEB_COMMIT \
  --api-version VERSION \
  --jdk /home/isp/apps/dragonwell-21.0.11.0.11+10-GA \
  --cache-home /home/isp/state/cyf-local-build/gradle-home \
  --output /home/isp/wsps/private-maintenance/cyf-NEW_BATCH --evidence-dir /ABS/NEW/EVIDENCE --install
```

### 持久化与完成后保留（2026-11-07落地）

- 上述JDK和缓存已从临时路径迁入持久目录并核验；当前API/回退/Web包另有持久、摘要一致的镜像，历史安装record未改写。不要清理仍绑定的内存盘原件。干净源码须重新准备，历史计时worktree已删除。
- 完整批次结束并保存包外证据后，由Owner显式登记，不能仅凭构建成功推断任务结束；统一输出的组件子目录已受控支持：

```bash
/usr/bin/python3 -I -B /usr/local/libexec/cyf/rebuildable_cache_cleanup.py mark-complete \
  --task-root /home/isp/wsps/private-maintenance/cyf-NEW_BATCH/api \
  --artifact package/api.tgz --component api \
  --source-commit FULL_API_COMMIT --source-tree FULL_API_TREE \
  --payload-sha256 ACTUAL_APPLICATION_JAR_SHA256
# Web：使用同批 /web、package/web.tgz、component web及真实Web commit/tree，不传API payload参数。
```

- 最近两批/组件、24h及当前/回退引用均保护，沿用原30分钟cron和锁；重新使用任务目录前先mark-active。详见`ops/maintenance/LOCAL_ARTIFACT_RETENTION.md`。根盘约1GiB仍偏紧，不能据此保证冷构建/新增回归或后续任意批次达600秒。

构建JDK目录已于2026-11-07按用户要求统一到`/home/isp/apps/dragonwell-21.0.11.0.11+10-GA`；此为目录原子迁移，不重下载、不另存一份、不改生产JRE。API包包含应用JAR及来源/测试/依赖证明，Web包包含静态资源及逐文件manifest；均为原安装事务输入，不是常驻运行依赖。历史安装记录和当前/回退绑定包本次不改动。
