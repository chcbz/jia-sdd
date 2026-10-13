# BACKEND-RELEASE-10M-20261009

核对日期：2026-10-09；Owner：backend-release-10m-main。

## 范围与固定输入
- 用户目标：后端也优化，测试/构建/安装核验执行时间目标总计10分钟以内。目标不是强制deadline，不因超时中断构建。
- 本次不部署/重启/迁移，不调整生产参数、不删除身份/ACL/幂等/事务/锁回归，不复用旧JAR。
- API develop/远端develop：`1e9111028fbdff1ae5452f64aec843e85e81ad59` / tree `0416b722d735c58af4653892b6ee269e8f9d1498`，查询2026-10-09；组件tracked干净。根基线8bfbd375；根已有无关untracked不动。
- 历史同输入：本地Gradle15m36s，282pass；安装日志文件17:31:43.608–17:36:50.965约307.357s，不等同installer精确计时或本次发布。
- 最早有效验证：固定同API SHA、新私有worktree/输出，同282项定向测试、validateLayering与fresh bootJar；依赖缓存只读取历史可信本地批次复制到本任务home，后续复用本任务home。
- 改动仅根既有orchestrator的可选受控缓存与测试、既有策略/本handoff；不扩建runner、流水线或Reviewer。
- 源码完成、构建PASS与生产上线分别记录；完整部署10分钟尚未实测。

## 实施与自检（2026-10-09）
- 控制工具源码提交：`369f303c`（完整SHA见summary.json）；API源码没有修改，仍固定`1e9111028fbdff1ae5452f64aec843e85e81ad59` / tree`0416b722d735c58af4653892b6ee269e8f9d1498`。三个新独立worktree位于`/var/tmp/cyf-backend-release-10m{,-seed,-cached}-20261009/source`，未使用生产安装目录。
- 复用既有orchestrator，新增可选`--dependency-cache-home`：安全/私有home、隐式配置与环境/CLI冲突校验；不改串行锁、身份、源码核验和证据键，增加monotonic执行计时，排队等待另算。没有新增runner/Flow、自动部署、deadline、资源门禁或Reviewer。
- 本机缓存`/var/cache/cyf-gradle-local`，root0700；首次仅读取可信历史批次的modules-2/9.3.1/jars-9数据复制（非硬链接），未复制Gradle属性、init、daemon或项目编译输出，未清理其他聊天缓存。Gradle自然管理的依赖/脚本缓存约842MiB，编译输出缓存本轮约13MiB；不因目录大小盲删业务依赖。
- compile-only策略位于既有local metadata init：JavaCompile采用Gradle内容指纹；其他任务禁用输出缓存、Test额外禁用up-to-date，fresh bootJar原规则保持。producer/admission仅允许显式`--build-cache`参数，所需测试/layering/bootJar日志仍必须真实fresh，cached/skipped/up-to-date一律拒绝。
- 工具自检213项通过：orchestration80（含缓存策略13），producer36，admission92，安装锁5；均为隔离测试，不是生产安装。两处新增测试最初因Python3.6 mock属性/成功fixture残留归因修复后通过，不是Gradle源码失败，无盲重试。

## 同SHA实测
1. 原历史批次：Gradle15m36s、282pass，空隔离home。
2. 本轮依赖缓存对照：`/var/tmp/cyf-backend-release-10m-20261009`；Gradle4m49s，207任务全部重新执行，282pass/0fail/0skip，`--no-build-cache`。
3. 首次编译缓存填充：`/var/tmp/cyf-backend-release-10m-seed-20261009`；Gradle4m45s，编排子进程286.554s，207任务全部重新执行。填充成本不是每批都必须重跑，不计入热缓存候选的耗时，也不承诺冷缓存10分钟。
4. 新干净worktree/空buildRoot的热缓存候选：`/var/tmp/cyf-backend-release-10m-cached-20261009`；Gradle1m54s，编排真实115.254s；207任务=130执行/77缓存命中，命中仅compile*Java。282pass/0fail/0error/0skip，原6组定向测试、validateLayering和fresh bootJar全部实际执行。4038个.class与第2组无输出缓存编译逐字节一致。未使用EVIDENCE_HIT跳过整轮。
5. 同批原producer校验/证据组装/打包23.381s，实际构建+打包138.635s（约2分19秒）。JAR `efa4cd2a71aee199586733fbbf9f095ed77c9fca82545e3fa90965012af01e3a`；归档SHA `17086620394673d4d698dcfe7886c0689999af4e293c8e597ec809859d3a4574`，226628431 bytes，version`1.14.0-consolidated.20261009`，build ID`cyf-backend-release-10m-cached-20261009`。

## 发布边界与下一步
- 本轮未安装工具/应用、未启停服务、未执行DDL/真实DB业务验收、未建立生产授权记录。
- 138.635s构建/打包 + 历史安装307.357s = **445.992s，约7分26秒**；只是执行时间估算，不是新版本完整发布实测。队列/中间等待、controller/admission输入准备、首次缓存填充及不同候选/selector不包含；10分钟完整发布尚未验收。
- 只读核对：当前安装的`/usr/local/libexec/cyf-api-local/admit-api-local.py`尚不支持`--build-cache`。后续授权版本发布须正常同步并核验本次控制工具版本/摘要，之后消费对应固定新批次制品；不能绕过旧工具拒绝或伪造回执。旧工具仍可接受`--no-build-cache`依赖缓存路径，但4m49s+23s打包+历史安装约10分19秒，不声称满足目标。
- 热缓存同SHA候选已构建/制品通过、源码可集成；生产和端到端目标仍待授权发布。日志/原始fixture/制品保持上述task私有目录，小型摘要位于`docs/implementation/evidence/backend-release-10m-20261009/summary.json`。稳定用法回写既有README和交付策略，不将实施流水账写入架构。
- 分段定位/实现/验证/等待的完整同质时长没有完整埋点，未知不补写；仅引用真实Gradle/包装计时，未承诺整体开发周期缩短。

## 用户授权收尾：BACKEND-CACHE-DEFAULTS-CLOSEOUT-20261009

- Owner：backend-cache-closeout-main；2026-10-09。根branch develop/base`d01a9683`，API本地/远端develop固定`1e9111028fbdff1ae5452f64aec843e85e81ad59`/tree`0416b722d735c58af4653892b6ee269e8f9d1498`，只读远端核对。当前根/API tracked干净（收尾改动前），原untracked不动。
- 用户授权把默认路径及安装校验工具收尾；不发布应用、不重启/停止服务、不写生产数据/DDL、不修改历史批次authority/catalog/receipt。
- 范围：既有orchestrator只针对`CYF_LOCAL_RELEASE_OPT_IN=1`+local context默认缓存；metadata固定hash校验防旧策略启用测试缓存。正式调用没有显式cache flag时默认`--build-cache`，没有home参数时默认身份专属私有home；显式诊断参数保留。未绑定匹配metadata拒绝，不作用于Flow或普通专项诊断。
- 实际effective argv与缓存policy存入原证据记录，fixture/producer应记录effective argv；cache命中同时核对policy，不能复用不同策略的旧整轮证据。
- 安装变更候选只比当前root-owned helper多`--build-cache`白名单，准备原值快照、既有coordinator→release→lifecycle锁、原子替换与恢复；不改wrapper/应用/JAR或历史helper catalog。
- 最早验证：默认策略隔离测试、旧/新admission grammar/fresh任务拒绝回归、只读canonical path8项；正式默认路径候选按同API SHA在新的私有worktree验证，不复制项目输出，保留原282测试/layering/fresh bootJar。

### 收尾已核验（2026-10-09）
- 默认策略源码commit `638777ed61029e4d94369b18d7026e5044644786`；功能在正式local release上下文自动启用，不依赖本聊天记忆。已回写项目AGENTS、既有工具README与交付策略，不修改共享skill/其它项目。
- 新固定API worktree `/var/tmp/cyf-backend-cache-closeout-20261009/source`：调用未传`--dependency-cache-home`/`--build-cache`且未设置GRADLE_USER_HOME；命令实际补默认flag、选择受控home，effective argv与policy已在原证据cache绑定。207任务130执行/77编译命中，282pass/0fail/0error/0skip；所有原测试、layering与fresh bootJar仍实际执行。Gradle子进程134.142s，原producer核验/打包22.350s，合计156.492s（约2分36秒），不是应用发布。
- **上一节“安装工具尚不支持新flag”的限制已经解除**：19:09:25+08:00，仅将root-owned `/usr/local/libexec/cyf-api-local/admit-api-local.py`的argv白名单增加`--build-cache`，安装前值严格匹配，不覆盖并发修改。已按既有coordinator→release→lifecycle锁，保存0700目录/0600原值备份后原子替换与回读。SHA `49ff62e470beadf5c5c570b007d1d30a6dd18b1f32df217274d89121ff77728b`与固定源码一致。
- 安装后直接调用实际installed模块的纯校验器：接受新flag及fresh任务，12种required-task cached/up-to-date/skipped/no-source情况仍拒绝；192项隔离回归通过（orchestration92、admission92、canonical path8）。首次安装脚本把健康status对象误当字符串，在写入前停止；确认真实HTTP200/status.code=UP后修正解析，未伪报故障、未重复相同输入盲试。
- 安装前后canonical PID1248394/startTicks15009554/JAR15d3456e全摘要/healthUP一致，应用未部署/启停、无DDL、历史catalog/authority/receipt未修改。没有伪造Flow回执或新版本发布记录。
- 原helper备份 `/home/isp/baks/cyf-backend-cache-closeout-20261009/admit-api-local.py.before`，before SHA `a5d4f89693e02903001f148c5fdac1613d2756c26d334fd78702df054a16c32b`。若需恢复旧精确批次，先按同锁顺序检查当前helper仍归本次候选并恢复已核验原值；下一次新发布绑定当前工具生成新catalog，不能改写历史绑定。
- 收尾证据：`docs/implementation/evidence/backend-release-10m-20261009/closeout-summary.json`及`closeout-installed-helper.json`；日志/fixture/制品在本任务私有scratch。开发/默认入口/工具同步均完成；完整应用发布10分钟目标仍未实测。新156.492s+历史307.357s=463.849s（约7分44秒）仅估算，cold/changed-source和等待不承诺。
