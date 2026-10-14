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
- 前端正式验证仍走 Flow4403172；后端在干净精确输入上先读 build.gradle，再经原 gradle 入口串行验证，保留 validateLayering。preflight 不绕过现有锁、授权或失败处理。

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

## 后端本地构建：受控持久依赖缓存（2026-10-09）

**正式本地发布现在默认启用**：既有 `gradle` 入口识别 `CYF_LOCAL_RELEASE_OPT_IN=1` + `CYF_LOCAL_GRADLE_ACTIVE=1`，核验显式metadata init的内容与固定compile-only策略一致后，无home参数默认 `/var/cache/cyf-gradle-local`（委托身份使用UID后缀），无cache flag默认加入 `--build-cache`。无需每次手传缓存参数；源码与build输出仍逐批隔离。Flow和普通专项诊断不受影响，显式 `--no-build-cache`、显式 `--dependency-cache-home` 保留诊断/隔离用途。与默认home冲突的旧 `GRADLE_USER_HOME` 需在调用端移除或明确绑定匹配home，不静默降级。

- 参数设置子进程 `GRADLE_USER_HOME` 并输出路径readback；目录必须canonical、无符号链接、由实际Gradle身份持有且0700。首次仅创建该目录，不自动创建父路径、不复制历史配置/daemon、不清缓存或他人目录。
- home不得有隐式 `gradle.properties`、`init.gradle(.kts)` 或非空 `init.d`；仓库/消费凭据仍由固定显式init配置管理，不将凭据写入home。冲突的环境/CLI user-home拒绝，不能悄悄落到另一个目录。
- 第一组对照仅复用依赖/解析/脚本缓存，`--no-build-cache`下仍重新执行207任务。正式本地候选默认 `--build-cache`（可保留 `--no-daemon`），配合本仓固定 `local-release-metadata.init.gradle` 的compile-only策略：只允许JavaCompile按Gradle输入指纹复用（包括测试类编译），所有非JavaCompile禁用输出缓存，Test额外禁止up-to-date；不复用测试报告或旧JAR。原定向测试、`validateLayering`、OpenCV来源/SHA、PublicArtifactVerifier、POI运行类路径和fresh bootJar仍执行。
- 默认策略不改基础证据键、源码核验、串行锁、身份或发布授权；接受旧整轮证据还须策略对象匹配。工具新增 `GRADLE_EXECUTION_TIMING` 实测子进程耗时，计时不含获取互斥锁的等待；没有deadline/资源门禁。
- 完整调用仍须固定任务、commit/tree、selector、fixture和工具链，逐批记录新输出/日志/制品SHA；不要直接套其它任务的示例选择器。构造fixture前可调用 `local_release_cache_defaults(args, requested_argv)`取得实际参数和策略，绑定effective argv及policy。原证据记录保存 `effective_argv`/`release_cache_policy`；producer证据必须写实际argv，不能把未补默认flag的requested argv冒充实际命令。正式发布只消费同批核验的制品。

本轮测量及边界见 `/home/isp/wsps/cyf/docs/implementation/handoffs/BACKEND-RELEASE-10M-20261009.md`；不是生产安装入口，不因此重启服务。

- 本地producer/admission的argv白名单允许 `--build-cache`，但不放宽所需测试/分层/bootJar任务的fresh日志要求，`FROM-CACHE`/`UP-TO-DATE`仍拒绝。`invocation.cacheHit=false`指整个验证未被EVIDENCE_HIT跳过，不表示JavaCompile未命中；实际命中以逐任务日志为准。
- 2026-10-09用户授权收尾已同步安装 `/usr/local/libexec/cyf-api-local/admit-api-local.py`；回读SHA `49ff62e470beadf5c5c570b007d1d30a6dd18b1f32df217274d89121ff77728b`，新flag可用且cached required tasks仍拒绝。原值备份 `/home/isp/baks/cyf-backend-cache-closeout-20261009/admit-api-local.py.before`。安装使用既有coordinator→release→lifecycle锁和原子替换，应用PID/start/JAR/health未变，无应用发布或DDL。
- 工具更新不改写历史批次的helper catalog/authority/receipt。下一次发布按当前固定工具重新生成对应批次的helper catalog；若恢复旧的精确批次且其catalog绑定旧工具，按同锁顺序先验证/恢复原helper（before SHA `a5d4f89693e02903001f148c5fdac1613d2756c26d334fd78702df054a16c32b`），不得绕过工具摘要或把旧回执重标新批次。
