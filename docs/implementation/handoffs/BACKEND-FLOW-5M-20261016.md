# BACKEND-FLOW-5M-20261016

Owner backend-flow-5m-main / codex。用户授权尝试优化与实测；先无部署，未授权任意版本生产重启/资源采购。状态以TASKS.yaml为准。

- 范围：现有5260799，固定源码、原默认测试集合、JDK准备计时、compile-only缓存对照；不创建流水线、不减少测试、不覆写其他Owner修改。
- 根基线e05498ed8f8d67d791ad8d269ae5bbc00b3592e6/tree3e7418605fef2d518aa9b04643c9936dd9a06abc，develop，工作区已有脏修改；本任务只新增独立helper/测试及记录。
- API基线58b4b5f408257c6d5103d915e13c7927c1571e20/tree3e60bd5858735790b7886ef00a9a94614816fb75，2026-10-16只读ls-remote一致。不把当前源码当线上或Run139受测源码。
- 工具/规则：/home/isp/wsps/cyf/AGENTS.md、ops/orchestration/README.md、ops/ci/aliyun-flow/flow-control.cjs；api/docs/interface-standard.md 2026-10-14冻结版，无接口改动/子Agent交接。
- 证据目录 docs/implementation/evidence/backend-flow-5m-20261016；私有配置备份/候选 /var/tmp/cyf-backend-flow-5m-20261016（0700，原值0600）。配置中原triggerEvents为push，只验证无部署；实验临时置空，结束恢复匹配原值，不静默永久修改触发策略。
- 原因新证据：/var/tmp/cyf-ur-flow-r16-20261008/run139-log-read5.json保留实时中间片段；19:28:46准备→19:48:58 RPM完成，共1212秒；41MB headless包6分53秒。常用curl/tar/git/python已存在但dnf还升级，不能把这段耗时归给Gradle缓存。
- 最早验证：bootstrap合成归档安全/缓存回归；Flow固定源码无部署运行，真实worker验证JDK ABI、原selectors、layering/fresh bootJar。随后同SHA新Run测热缓存，不伪造新Run、生产回执或完整发布达标。
- 设计：只缓存固定SHA压缩包、逐次验证并新目录解包；不执行缓存解压目录。JDK选官方Dragonwell Extended21.0.11.0.11+10（与Run139 RPM+21补丁构建不同，显式记录，不能作为单变量纯缓存对照）。首次运行与第二次保持同JDK。
- 云端Gradle通过原orchestrator串行入口；固定控制工具与本任务授权快照传入独立临时目录，快照只作本Run输入，不是可写权威台账。锁与源码清洁检查保留；不复用整轮成功证据。
- 完成口径：构建测试通过不等于部署。端到端300秒要另绑定实际版本、同Run制品和线上核验；排队、冷/热缓存分报，无性能强制deadline。

## 实验进展（2026-10-16）

- Run140：GitHub下载socket timeout，Gradle未开始。改官方Dragonwell OSS镜像（同官方SHA），不重复相同输入。
- Run141：官方OSS冷下载/校验/解包/Java和javac版本检查6.138s；编排器调用参数误放task_id后被REMAINDER吞掉，Gradle未开始。修正为选项→task_id→命令，并调用原parser做无副作用自检。
- Run142：JDK冷准备6.470s，原编排器真实Gradle18.370s，失败于旧Flow引用已删除的chatDeliberation task。源码5d54634a3d在10月15日删除过时suite并迁移保留输入，不重新引入兼容任务。
- 修正映射：现src/mmdRegressionTest/java全部50源文件由7个现行task覆盖，49测试类按类去重，每类仅一个task运行；保留原所有其他selectors，补src/test内迁移的ChatConversationEventsHttpTest、SkillExecutionDeclarationTest。完整映射见私有chat-suite-map.json和chat-suite-dedup-selectors.json。新实验不是Run139原套件的同输入对比。
- 未运行历史Run139专属UR03跨客户端fixture；不据当前默认套件宣称旧UR03失败已修复。
- 只读观察现行本地发布1.16.7、同58b4b5f源码的已有日志：Spring Started56.107s、process-at-Started58.109s。不是本任务安装，Started不是完整installer/业务ready。
- helper合成安全测试12项PASS；真实Gradle/cache/端到端仍待终态。没有生产启动/停止、DDL或本机Gradle执行。

## 本轮收口（不是五分钟目标完成）

- Run143 FAIL：从创建到作业结束134秒；JDK6.697s，Gradle105.118s。JUnit部分任务图实际1086项=978pass/71fail/37skip（86 suites，失败集中10个suite）。agent service子集1000项=71fail/37skip。测试失败后后续测试/layering/bootJar/制品/部署未获验收；不把2分14秒失败当成功发布提速。
- 失败清单`docs/implementation/evidence/backend-flow-5m-20261016/run143-tests.json`来自日志诊断gzip分块，解码后SHA匹配。已见旧JSON path、HTTP状态、反射签名等与现实现不符；SkillMarketplaceRealTransaction等也失败，不把全部71项武断归为只改断言即可，须按2026-10-14冻结规范逐项判断实现或fixture问题，保留ACL/事务。
- 本轮不扩展到10个业务suite的协议迁移/事务修复，不删除测试、不重跑同失败源码，也不伪报热缓存效果。状态`blocked_dependency`，不是accepted/done；下一动作是修复该固定基线失败后，在新精确源码重新进行冷/热对照，再绑定明确版本实测部署。
- 独立工具自检12项、原控制面Python静态7项/Node13项PASS，总32项工具检查；不替代业务测试。初次控制测试文件名未命中、实际0项，没有作为测试证据；后来运行正确文件得到7+13项。
- 21:19:33+08:00恢复前确认无活动Run、当前配置仍为本任务candidate；经原flow-control单次写回原值并readback，原SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a完全一致，见restore-result.json。不保留临时branch默认值或关闭push触发状态，不启动恢复后的Run。
- 私有完整候选/配置/实际调用/日志分别位于/var/tmp/cyf-backend-flow-5m-20261016/{r2,r3,r4,restore}。固定实验远端分支codex/backend-flow-5m-20261016仍指58b4b5f，无API源码改动，不删除证据ref。
- 生产仅执行一次原helper status，只读PID/监听归属/健康和制品证明；本任务没有安装、重启、SQL或修改其他聊天进程。
- 定位/实现/验证/等待未独立计时，不编造开发效率收益。已证明的是JDK准备路径可压到约7秒，不是整条流水线成功或端到端五分钟。

## 十分钟定向修复（2026-10-16 21:50，用户授权）
Owner backend-flow-5m-main；API clean base58b4b5f，隔离worktree `/var/tmp/cyf-flow-testfix-20261016/source`，分支codex/flow-testfix-20261016。仅修测试fixture、保留ACL/真实事务；不修改生产、不部署。最早验证为5个已明确根因的suite及validateLayering；其余不以删除掩盖失败。

21:59十分钟窗口收口：修正候选51a6410ec02e0fcbb82c8516f0b160eaeea1587d覆盖原32项失败（5类），没有改业务源码。真实本地验证经orchestrator串行、既有受限构建cgroup执行，第一次新输出0755被原metadata拒绝，归因后仅修自有目录0700；第二次尚在test阶段，不能声称32项已经PASS。日志与输入 `/var/tmp/cyf-flow-testfix-20261016/{test.log,input.json,result.json}`（result须确认commit和日志对应；首轮失败记录不代表第二轮终态）。
用户最新明确“10分钟修不了就删掉”作为本次删除授权，覆盖之前本任务默认不删测试的范围：第二个隔离候选d70a0f41e6在51a6410之上仅删除其余39个失败测试方法，保留类/辅助方法/其他用例；其中含10个Runtime安全回归，明确存在覆盖缺口，绝不记作修复或验证通过。完整逐例清单`docs/implementation/evidence/backend-flow-5m-20261016/testfix/removed-tests.json`。路径 `/var/tmp/cyf-flow-testfix-20261016/trim-source`，分支codex/flow-testfix-trim-20261016。未合入develop、未push、未部署；删除候选尚未编译/验证，不复用51a6410的测试结果冒充其验收。下一步读取本次既有验证终态，再对最终候选做一次原流程验证；不继续盲目删减或重跑。

## Flow144真实复测（2026-10-16）
用户明确授权删除剩余失败并重跑Flow计时。局部本地51a6410最终72项/71通过/1失败（事件occurredAt字符串断言），并非全绿。新候选aca649bac2383a9054b2891ba930c7fc203d1f61/tree7f36c14ba95bf54b1d20c71583c83d298ec386fd删除该最后方法，累计40项删除，清单testfix/removed-tests-flow144.json。独立分支codex/flow-testfix-trim-20261016已push，未合入develop。复用原工具及JDK方案，无部署；临时配置已备份并readback，Run144已启动，实际source仍需实时核对。私有过程证据`/var/tmp/cyf-backend-flow-5m-20261016/r5`，结束后恢复配置，不将40项删除当修复或原套件等价性能。

Run144终态FAIL：22:07:42创建→22:10:28作业结束，总166秒（2分46）；JDK冷准备6.265秒，Gradle136.439秒。云端压缩诊断SHA fcecc35c156f6d3b6c50ff7d4fa39904551305d788c659b6be37fd07afdb7b30已重算匹配，实际commit aca649bac2383a9054b2891ba930c7fc203d1f61/run144匹配。部分任务图1278项=1224pass/16fail/38skip；agent mapper86全PASS，agent service960项/0fail/37skip，base32全PASS，chat200项/16fail/1skip。新失败位于7个Chat/WebSocket/Voice套件，不是原40项复发。保留授权删除40项的覆盖缺口；不将166秒失败当完整构建/部署达标，未产生成功制品。只启动用户要求的这一次Flow，未再删新失败或重跑。
22:12:21+08:00无活动Run/配置仍为本candidate核对后，原flow-control已恢复原配置并readback，SHA a9f1a63633d75adc2c56e94073dfab4f7c1baa7dc83743c2e5fdc41f42afd33a完全一致；未部署、未改生产。正式摘要与16项失败见testfix/flow144-{timing,tests,restore-result,candidate-proof}.json及flow144-phase-timing.log。独立源码分支已push，不合入develop，任务仍被新测试失败阻塞。下一步需对这16项做明确处置后才有成功完整计时。
