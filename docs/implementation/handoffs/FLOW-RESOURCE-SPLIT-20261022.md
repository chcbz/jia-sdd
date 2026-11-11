# FLOW-RESOURCE-SPLIT-20261022

## Scope / ownership

- 用户授权：按2026-10-22资源分工规则更新前后端Flow并各执行一次观测。唯一Owner为本聊天，不新建Reviewer。前置只读核对、候选/前值保存与回读；本次执行默认CI，不顺带生产部署/重启。
- 已读AGENTS.md、ops/orchestration/README.md、Flow工具README与现行部署策略。接口规范api/docs/interface-standard.md v1.2沿用，无应用契约变更。
- 目标：Flow保留重型测试/构建/打包，Run执行结束即终止；本机轻量检查/查询/协调；无配对ready/人工/跨流水线等待。既有依赖与制品完整性、锁、回归不删。
- 非目标：不接管PDF Owner源码/发布/Node升级，不取消其他聊天Run，不新增流水线，不本机构建，不改生产安装器。部署阶段不在本次CI效果验证范围。
- Root develop HEAD5e6ab2b6f1a156c320189f17d76941fbe623738a/tree9e1221b3aa7c70ca7f80670ec5ce7ef695af05f2（本地引用）；现有脏修改逐文件快照，不覆盖、不整仓提交。
- 2026-10-22 18:06左右实查：Web293已由其他执行者取消；API232仍RUNNING，构建SUCCESS、部署71622333运行中。本聊天不取消、不覆盖其配置，先处理空闲组件。远端develop已实际ls-remote：Web669bdc9d6439d1bd7eb71df5ed401202a648f419；API1d05101d267bc0e0cf50678fb6d80cb967136d34；启动前再次核对，不把其视为永久最新。
- 工作区与证据：/home/isp/wsps/cyf；/var/tmp/cyf-flow-resource-run-20261022/（0600原配置和候选）；源码修改前快照source-before/。正式输入/Run/摘要和结果续记于本文件，尚未启动本聊天Run。
- 最早验证：模板结构/无外部等待、npm完整测试/构建与后端原policy回归、shell语法；本机仅控制面轻量测试。计时：定位进行中；实现/云端验证/外部占用等待分别记录，不承诺总耗时。

## PDF 联合发布 Owner 协调备注（18:23 +08:00）

PDF Owner 已在自然接续点读取10-22资源分工新规则；此前API233于18:18启动（develop7841057b，完整同Run构建部署），当前仍执行中，请勿覆盖其配置/取消。其已冻结旧配置带配对ready loop；此次将已具备的发布条件提前准备，使部署不再实际等待其他Run；后续候选删除外部等待，不放宽安装器同Run/develop要求。Runtime1.2.5已上线，三通道健康。

Web294（本任务同一develop669bdc9）只做CI，线上仍1.16.42；PDF发布需复用既有4403172再启动一次同Run构建+部署，不能把294 CI当部署。将基于你本次保存的resource-offloaded当前配置追加本次显式版本部署（无ready循环），保留phase/Node24/制品格式，显式保留当前生产三个VITE功能开关true。完成后恢复你已核验的CI-only配置（仅在无活动Run且readback仍属本任务时）。不会恢复旧Node20模板，也不删除你的工作。若你后端观测需要5260799，等待本次发布结束后使用；本备注不是夺取你的任务。

## 已执行与证据（2026-10-22；查询时间以结果JSON为准）

- 本地仅静态模板/控制面检查：新增资源分工合同3项、既有模板6项全部通过；两份候选YAML解析与bash -n通过。系统python3无PyYAML，改用仓库已有js-yaml解析，没有安装依赖或本机应用构建。
- 前端模板仅新增阶段计时与资源卸载名称，保留Node24/固定SHA、npm ci、完整测试、Vite构建、报告/manifest/ArtifactUpload、原JS扫描。后端模板新增职责注释与阶段名称，沿用prepare-backend-ci.py渲染；backend-ci-run.sh及policy相对本任务前值完全未改，保留原Owner字体修复及全部原测试选择器。
- Web云端旧配置含PDF_PAIR_WAIT和deploy阶段；在全历史无活动Run/源码/前值一致检查后更新为默认无部署CI，readback canonical SHA baa047f7626f14747cad1687c0411bb127aae1fe80918e26d7beb31119bce379。实际仅启动Run294一次，初始source未填全返回UNKNOWN，随后只读核对真实develop669bdc9与SUCCESS，没有重复触发。
- Web294：18:15:44—18:18:41共177秒（2分57）；测试构建作业177秒，并行扫描144秒；3252通过/2pending/0失败，测试报告40.101秒、Vite阶段10.74秒。真实制品109478032bytes/SHA f4104a94dda94f9a6e63dde90c8764bddcb52d1a97480374d5da765485e7e817；manifest绑定4403172/294/669bdc9/1.16.43，tree07e73d0e8ed69b6556e7ea67ee7172fe1c09ec8b，613个dist文件按流式读取逐一验证摘要/大小。下载URL仅内存使用，未入报告。
- 本机核验已改为单遍流式归档读取，未展开归档/执行制品；最初随机seek核验效率低，仅精确停止本任务持有该归档的python reader后改为单遍读取。无他人进程/生产服务操作。
- API232自行FAIL后，远端develop已前移为7841057b057c012cfa203fb658c1043500be055e（1.16.29），已重读固定源码相关build.gradle并更新候选上下文。第一次更新前预检发现云端前值变化，CONFIG_CHANGED_NO_WRITE，未写API配置/未启动。原Owner更新为develop发布配置并启动Run233，不能覆盖；API本任务候选仍未应用，不把其233当作本任务验证。
- 结果：docs/implementation/evidence/flow-resource-split-20261022/results.json；原配置/候选/脱敏日志与归档保留/var/tmp/cyf-flow-resource-run-20261022/。Web效果是正常完成Run、无配对等待；未部署，不拿旧Run293含等待的总时长冒充同范围编译提速，未实测本机整体内存降幅。
- 下一动作：等待原Owner API233真正结束/释放配置后，重新查询来源/活动Run/当前配置，保存新前值、保留其有效工具变更，再单写readback并仅启动本任务API CI一次。未授权取消/接管其他任务，不恢复含无限配对等待的旧配置。

- 本任务109478032字节Web临时下载在完整核验后已删除，释放本机空间；真实不可变制品仍在Flow，摘要与核验报告保留，结果标记localCopyRetained=false，不称本机归档仍可读。API233已通过配对进入真实安装/服务启动等待，本聊天只等待其退出，不操作其服务或配置。

### PDF Owner 释放流水线窗口（2026-10-22 18:40 +08:00）

API233已SUCCESS，部署71624603/目标主机Success，安装记录run233 verified；Web295已SUCCESS，部署71624824/目标主机Success，线上记录1.16.43/295。Web295基于你本次resource-offloaded CI保留Node24/phase/现行manifest格式，增加显式同Run部署且无ready等待；生产VITE三个开关显式true。Web已在无活动Run且配置摘要仍属本任务时恢复启动前的资源分工CI-only配置，readback APPLIED，证据`/var/tmp/cyf-pdf-skill-20261022/release/continued/r7/web-restore-result.json`。不再写Web配置。

API本次旧冻结Run233已结束；不再写5260799配置，你可继续自己的后端分工观测与默认CI恢复。注意本任务为真实POI回归补了签名安装freetype/fontconfig/DejaVu及`LD_LIBRARY_PATH=$JAVA_HOME/lib/server:$JAVA_HOME/lib`的ldd检查，`ops/ci/aliyun-flow/backend-ci-run.sh`新增块是本任务修复，请保留，不恢复缺字体的旧环境。API测试包络断言修复已在develop7841057b。无新应用构建/部署授权因此转移给你的任务。

## 最终收口（2026-10-22 18:51 +08:00）

- 上述“API未应用/等待233”是历史中间状态，现已解除：原Owner233在18:39查询为SUCCESS，本任务重新保存当前配置、确认全历史无活动Run及远端develop固定7841057b后，单次更新readback并仅启动API234。启动返回INIT/UNKNOWN后只读核对同Run，不重发；18:47查询SUCCESS、来源匹配。
- API234：18:40:31—18:46:08，337秒（5分37）；唯一构建作业336秒，Gradle151.364秒。316 suites、2828次测试（2706通过、122跳过、0失败/错误），原policy/validateLayering/fresh bootJar保留。Run无部署阶段和外部等待。
- API同Run归档225154779字节，SHA256 a98967ea1622fe69667683e7f47c786770e5198a9bd68de2562da5dd131546b6；单遍流式校验receipt/metadata/sidecar/依赖证明与JAR（252466294字节，SHA244f2b6e208bf9794cb5da2ce506903b40acc24aa8483dece30e293c154f5e03）。receipt固定7841057b057c012cfa203fb658c1043500be055e/tree57b0add0c4bf89c313f179d6a365508cf58f9b62/develop/clean。summary绑定同Run与源码；完整summary及验证报告保留仓库证据目录。
- 18:47前后重新查询两端实时配置：Web canonical baa047f7626f14747cad1687c0411bb127aae1fe80918e26d7beb31119bce379；API canonical b7e6cbec46029fa3a115407075a725f2b04eeb15ec30f4d6c291fd89add2b2e0，均匹配本任务已测CI候选。Web期间由原发布Owner临时追加授权部署，结束后已恢复本任务CI默认；本任务没有抢写恢复，也不将其发布记为本任务成果。
- 两份已核验的本机临时归档均已删除释放空间；Flow保留真实制品，摘要/报告保留。未实测主机整体内存下降；没有把原含等待的27分钟与CI-only时长当作等范围构建提速。
- 验收：两端默认CI配置已应用且各实跑成功，重任务在云端、本机仅轻量控制和完整性核验。生产部署及安装器生命周期改造未在本任务测试；不宣称完整发布链路验收完成。本任务没有应用源码提交/push或生产服务操作；当前脏工作区其他Owner改动保留，模板/文档未整仓提交。
- 结果与稳定说明已回写results.json、Flow策略与工具入口。无本任务后续重试/等待Run。

## 耗时续查（2026-10-22 20:10 +08:00；仅只读）

- 用户追加“继续检查流水线耗时是否能压缩”。复用本任务Run294/234固定源码与已验证制品summary，不重复构建。唯一Owner与原非目标不变；当前组件HEAD已前移（Web9dbd132e/API94b4c8a5，仅本地引用），不把新源码与旧实测当同输入对照。本轮不执行Gradle、不写云端、不部署。
- 20:10:32/33实时读取两端配置canonical均与已测候选一致，近期5条记录均终态（Web最新295、API234 SUCCESS）；未全量分页，此查询不作为写配置授权/完整活动Run排除证据。私有readback：/var/tmp/cyf-flow-duration-audit-20261022/。
- Web294构建作业18:15:48—18:17:21是git clone全量取源，93秒，占177秒约53%；同Run并行扫描取源18:16:16—18:16:46为30秒，说明取源耗时有显著差异，尚不能直接归因网络或缓存。测试40.101秒、Vite10.74秒；缓存恢复4秒、制品上传步骤5秒、缓存回存6秒。并行扫描总144秒，不能与177秒相加；即使只优化构建作业取源，扫描仍可能成为总耗时下界。首选核验平台取源深度能力及固定源码是否依赖历史，再单变量浅克隆实测；未核实字段，不猜写YAML，不承诺节省63秒/93秒。
- API234：环境/工作区到取源步骤26秒，取源步骤11秒，缓存恢复15秒，构建步骤248秒（18:41:23—18:45:31），其中Gradle151.364秒，差额约96.636秒是准备/收尾的合计推导，并非字体/JDK/MySQL单项实测。制品上传步骤10秒，缓存回存24秒，其余转换/收尾3秒。103个compile缓存已命中；缓存恢复+回存39秒不等于可直接删除的开销，禁用会让编译/依赖变冷。
- API重任务：agent:test55.838秒、chat:mmdU3Finalization49.138秒、chat:test25.898秒、agent:mmdU1Grant24.119秒、bootJar16.851秒，存在并行重叠，不把累计任务wall time当关键路径。现有API日志缺失前段runtime/JDK/Gradle begin数值（more:false仍有缺段），不能据差额断言包管理器慢。下个最小实验应先将准备阶段数值写入既有summary，拆出JDK校验/解包、字体包安装、MySQL准备，再选择优化。
- 已读既有Runs202—208缓存与JVM实验结论：cacheDirs追加而非替换默认路径、Maven移动跨设备未执行、TAR_OPTIONS未显示实际收益、GZIP=-1无净收益，Gradle C1/重任务提前也未确证收益；不重复这些盲试，不移除必要回归、制品校验或fresh JAR。本机目录库存不能直接当远端可节省传输量。
- 当前结论：有优先级明确的优化候选，尚无新的缩时实测。证据：docs/implementation/evidence/flow-resource-split-20261022/duration-audit.json。外部官方文档检索未返回可确认的浅克隆字段，因此本轮不更改云端取源配置。下一步为前端取源能力/契约确认、后端准备阶段持久化计时，而非重复全量构建碰运气。

## 耗时优化续行（2026-10-22，用户“继续”授权）

- 沿用本Owner/任务，工作区/home/isp/wsps/cyf；继续前端取源能力验证及后端准备阶段计时。无生产部署，不新增流水线、不接管其他Owner。私有候选/前值/source-before位于/var/tmp/cyf-flow-duration-opt-20261022/。
- 本轮ls-remote确认远端develop仍为Web669bdc9d/API7841057b，与Run294/234相同；本地HEAD虽已前移，不拿本地源码作云测输入。固定tree/版本沿用release-input.json，启动前再次ls-remote。已重读固定API build.gradle/starter/build.gradle；Gradle仍仅在Flow原orchestrator入口执行。
- 后端只增加数值计时落入既有test-results/summary.json：JDK归档校验/解包、字体依赖、MySQL准备及Gradle边界；不改policy、测试选择器、缓存、生产JAR、安装器。保留字体修复及其他Owner工作。最早验证为既有renderer/summary fixture测试、shell语法；观察字段不可用不影响原测试结果。
- 首次编辑遇本机磁盘瞬时ENOSPC，命令未写runner但后续未受保护复制使本任务后端模板临时为空；立即从本轮source-before完整恢复并cmp确认，再以set -e、非空候选检查重做。未写云端、未改其他文件/删除他人数据。后续避免下载大制品到空间不足的本机。
- 前端官方SDK/API schema确有isCloneDepth/cloneDepth，但YAML映射仍须官方说明或有效回读证实，不能仅添加未识别字段就宣称浅克隆。未确认时不重复跑Web。
- 已从阿里云官方“流水线源 sources”说明确认 `sources.<source_id>.cloneDepth`，0为全历史，正整数为最近提交数；官方页https://help.aliyun.com/zh/yunxiao/user-guide/pipeline-sources，HTML仅私有证据保存。前端候选depth1，启动前额外核对API解析后的source.data.cloneDepth==1；不能仅凭保存YAML成功认定生效。
- 固定源码release profile的历史资产测试本来即单列，不删除任何测试。assets/all仍在浅仓时fetch --unshallow并再次核对HEAD，保留历史Git provenance；隔离两提交Git fixture验证release浅仓、assets/all完整历史且HEAD不变、未知profile失败。真实JS扫描保留，浅克隆兼容性以新Run实际结果验收。
- 后端235已单次创建，初始source未填全返回UNKNOWN/returnedRunId235；只读核对，不重启。启动上下文与APPLIED回读已保存。

### 耗时优化本轮收口（2026-10-22）

- API235真实SUCCESS，21:47:14—21:52:07总293秒；实际源码7841057b、tree57b0add0与234一致；新准备计时成功进入同Run summary。JDK5.24秒、字体37.76秒、MySQL4.62秒、Gradle shell包络148.06秒，orchestrator命令147.789秒。316 suites逐项计数与234相同，2828次/122跳过/0失败错误。只加观测未改策略，44秒差值不归因优化。
- Web296真实SUCCESS，21:51:56—21:54:03总127秒；实际源码669bdc9d/tree07e73d0与294一致。API source.cloneDepth=1且两作业日志均真实--depth=1；构建取源21秒、扫描取源13秒（原93/30）；扫描总118秒。3252通过/2pending，测试49.686秒、Vite14.05秒；相同源本轮总时长少50秒，单次结果不保证每轮相同。
- 两端归档本机流式核验，无展开或运行制品。Web归档SHA be6cef5c87c10e4c79eb14fa7f474dd7c28875d072f7ce68c8c972fa5c55102b，109477848字节，613个dist摘要/大小及manifest/tree/version均匹配；API归档SHA2fdb2b50f9c59b29fc46a88a95c57a2552fa99b88903f30acfa653972276cd68，225154272字节，receipt/metadata/sidecar/JAR/依赖摘要和source clean全部核验。JAR与234完全相同。只删除本任务已验证临时归档释放空间，Flow制品保留。
- 最终回读Web canonical d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd、API f56903cab42385c8b2967fdd5b592f6be4fdd331c5612309a7283582300129ef，均匹配本轮已测候选。未取消他人Run、未发布或服务重启；既有脏改动与应用工作区保持，不整仓提交。
- 本地检查：backend default5、资源合同3、模板6、浅克隆隔离fixture1全部通过；shell语法/YAML解析/diff whitespace通过，无本机应用构建。assets/all仅验证历史恢复机制，不声称完整云端assets验收。
- 稳定说明回写Flow策略与工具README；证据duration-optimization-results.json及duration-api-235-test-summary.json。前端已落地；后端字体37.76秒是下一优化对象，尚未引入预装字体镜像或声称已压缩该阶段。无本任务仍在运行的Run。
