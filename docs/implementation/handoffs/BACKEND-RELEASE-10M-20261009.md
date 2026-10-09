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
