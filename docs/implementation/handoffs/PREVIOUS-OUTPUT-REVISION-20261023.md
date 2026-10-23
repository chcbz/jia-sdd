# PREVIOUS-OUTPUT-REVISION-20261023

2026-10-23，唯一 Owner：当前会话，单 Agent。承接用户“继续”，定向修复事项518复核发现的上一版成果无法作为二次修改输入；不是重新执行Runtime性能发布。

## 固定范围与源码

- API独立worktree：`/home/isp/wsps/worktrees/previous-output-revision-api-20261023`，branch `codex/previous-output-revision-api-20261023`；fetch基线 `b0735f57a7b454fa7a6fb9886fa3914131986779`。
- Runtime当前生产1.2.8：isp-install `3c993e58033d901622c24126028199cdf4e2c76f`；Flow5264702/26已完成。Web远端基线`638084d26ec9a193240566bf45b33602cef8e0e0`；本轮不改UI/Runtime性能代码，不动共享脏工作区。
- 已读根AGENTS、API AGENTS、orchestration索引、SDD流程；公共接口固定`api/docs/interface-standard.md` v1.2。Flow正式测试/构建，develop不自动授权部署。
- 非目标：517历史状态、图片精确尺寸/逐像素履约、PDF、Provider/模型/账号/收费调整、成果替换状态机和多Agent扩展。

## 根因与最小修复设计（源码已实现，未上线）

1. admission现行代码先冻结TASK_DEFAULT输入目录，再计算deliveryTargets；已有输出虽展示为保留成果，却没有可用于技能的sourceRefId。518第二轮实际inputReceipt仍为初始蓝图SHA。
2. 在原事务、幂等重放检查之后，先从精确deliveryParent及其有效保留链得到deliveryTargets。不全量搜历史、不推断“最后一张”、不新增状态或强制APPEND改REPLACE。
3. 仅TASK_DEFAULT将这些保留媒体成果加入本轮有效来源，复用CURRENT_CONVERSATION_ASSET。NONE/EXPLICIT不扩大授权；EXPLICIT中已选成果仍可提供精确来源关联。仍遵守既有32来源限制，溢出明确要求显式选择。
4. 输出→资产为只读定位：精确tenant/owner/client/conversation/generation/request/step/output/SHA；再复用现有asset授权join、执行提交状态、当前任务和单一目标校验。资产异步投影未就绪或已失效时不能静默回到初始图片，不在admission/GET运行projector或保存到workspace。
5. 冻结上下文附上`retainedOutputSources`（outcomeId/finalDigest/outputSource/sourceRefId）说明已有成果与真实输入的关系；availableSources仍为原四字段，不扩大技能授权，不改action-v5/正式reviewBasis/revision语义。Runtime现有完整facts透传，不新增执行协议；需定向核验消费者。
6. 来源快照进入原requestDigest；重复key沿用已冻结目录。后续执行/下载仍复验身份/代际/摘要，撤销或换账号不能继续用旧资料。

## 验收

- API：单/多输出映射、去重、NONE/EXPLICIT、澄清继承、来源上限、异步未就绪、错误SHA/代际/任务/目标/账户与幂等重放；保留原正式返工和提交链。
- 最早反馈：定向源码/合同检查；正式测试使用Flow5260799固定源码，包含新增用例及validateLayering，不本机Gradle编译。
- 线上：获对应版本发布授权并部署后，用ziyue/吴用及带可辨识细节的图进行连续修改；断言第二次inputReceipt SHA=第一次成果SHA，不能仅以颜色/能验收代替来源正确。
- 当前状态：源码已合入API develop并由Flow249发布为API1.16.31；安装及健康通过，生产多轮图片验收被共享Codex升级导致的Runtime执行文件漂移阻塞。下列19:14等条目为历史进度，不代表当前待办。分段耗时尚未独立测量。

## 2026-10-23 19:14进度

- API候选与develop普通快进push/readback：`12e25f94726e913b0670f831b9fe4a1ff5ff0b26` / tree `810a6dc63e8f283079a823b7117257fced32b6b3`。9个文件，新增两组定向单测及真实MySQL授权回归；未部署。
- 正式CI复用5260799，仅增加两组定向selector，保留原测试、分层和fresh JAR。临时配置取消push触发并固定精确commit/tree，无部署作业；前值已保存。Run247已创建，初查INIT，等待实际source/run/test证据，不把空commits当已核对。
- flow-control的start因已有246次历史、超过100条拒绝，源码确认发生在任何start写入前；只读确认无新Run后复用现有分页single-start helper，未盲重试。其后仅一次start返回247。任务证据`/var/tmp/cyf-previous-output-revision-20261023/`，Run结束后按前值恢复配置。
- 现行Runtime1.2.8的真实buildContextEnvelope轻量检查2/2：冻结的retainedOutputSources完整透传，篡改关联触发CONTEXT_HASH_MISMATCH；不修改Runtime，不是模型/生产业务验收。

## 数据库验证补齐

- Run247 SUCCESS，精确12e25f9；同Run制品223717594B/SHA`f847defb523256b2762dc29777b5f87fe41c8764dd9ad5bb0809754a813cba84`。报告3047项，failures/errors均0，127项skip；新增两组单测10/10通过，但原外部MySQL可选套件未启用，不能算SQL已验证。
- 新SQL用例已移到现行默认启用的`JuyitingWorkflowMySqlTest`，复用其自有临时mysqld/临时schema生命周期，不增加本机数据库或绕过安全guard。生产查询同时保留精确BINARY复验并增加原唯一键前缀等值谓词，避免新增整表定位。
- 最新API候选/develop为`041548f601385a3463fbba06b929991371d93d9c` / tree`1bc5ae21325d9763e8325f31f4cc88a53317a5f3`。Flow248绑定该源码，复跑原套件及定向用例；新源码尚不以247结果冒充。尚未发布API，Runtime仍为既有1.2.8。

## 2026-10-23最终CI核验与收尾

- 续接已读取用户提供的2026-10-23项目规则，维持单Agent；本轮不改角色注册、共享规则或无关脏工作区。
- Flow5260799/248，job541850449，SUCCESS，固定API `041548f601385a3463fbba06b929991371d93d9c` / tree `1bc5ae21325d9763e8325f31f4cc88a53317a5f3`；2026-10-23 19:43前后远端develop回读一致，API候选工作区干净。
- 同Run报告3047项：2921通过、126跳过、0失败/错误。来源单测8项、admission单测2项及真实MySQL授权查询1项全部非skip通过；MySQL所属套件34/34通过。跳过明细保存在证据中，不声称其余可选集成场景已验证。
- `validateLayering`、fresh `bootJar`实际执行未跳过，BUILD SUCCESSFUL。归档223718001B/SHA `14f1584a36b1d78f832b3cb246c50f956c7110026092c592f6f75666e701a8b4`；内含JAR251014243B/SHA `679751080beec4f482ba3c0fa494727a981f819875ad3b25b1d1b36e94490871`已按成员只读核对。不是安装证明。
- 2026-10-23 19:43临时Flow配置恢复：先核对仍为本任务候选且近期无活动Run，再恢复前值；update APPLIED且readback SHA `a0c800ec81833a9251f60bb2b32cfe0e2b6e3d559b4112c499feaedfb48e0dcd`一致。未取消/修改他人Run，无部署。
- 紧凑证据见[本轮证据](../../../specs/juyiting-skill-execution/evidence/previous-output-revision-20261023/README.md)。原始日志/制品在本任务私有目录，不复制进Git。
- 本轮未部署API/Web/Runtime；Runtime1.2.8既有发布与此次API修复分开。下一步需确认这次API固定版本的生产发布授权，再按同Run制品契约发布，用ziyue/吴用核验二次输入SHA等于上一版输出SHA、预览与最终验收。不能把Run248 CI-only制品回执当部署回执。

## 后续授权：发布并完成多轮图片验证（2026-10-23）

用户明确“那就上线，然后完成验证”。仅发布固定API041548f6/tree1bc5ae2，发布版本1.16.31；Runtime/Web不变，不发布后续其他develop改动。复用5260799，同Run完整原CI+新增来源测试、制品及授权安装，无外部等待作业；不拿248的CI-only包作本次发布。

生产基线为b0735f57/API1.16.30/Run246，当前schema启动隔离已生效。本修复无DDL/数据迁移，前一版本仍与数据库兼容，因此使用现行安装器正常备份/失败恢复，不沿用上一轮跨schema变更的forward-only限制。安装器现行摘要已固定，不覆盖他人维护的工具；启动诊断沿用现行设置。发布互斥预检通过，标准health工具临时pause并记录本任务marker，收尾核对所有权后恢复。控制证据：`/var/tmp/cyf-previous-output-release-20261023/`。

业务范围：ziyue/吴用，带可辨识细节的上传图多轮识别/改图、纯文字生图及后续识别/改图、连续两轮修改的逐轮inputReceipt来源SHA、PC/移动预览与最终验收。PDF仍不验，尺寸/字符错误如实记录，不自动扩展修复。

## 发布完成及新阻塞（2026-10-23 20:30前后）

- API1.16.31/Flow5260799 Run249 SUCCESS，部署单71707194单机Success；固定041548f6/tree1bc5ae2。3047项中2921通过、126跳过、0失败/错误；本次11项测试实际执行通过。归档SHA `72b2cd6fd11cebae03f1cd52b692fa0c85e2bdd0ca94d63951b98742fbc77c52`，JAR SHA `679751080beec4f482ba3c0fa494727a981f819875ad3b25b1d1b36e94490871`，receipt SHA `d21b8418c2e10de1af76e398c49be83a4884cdf4bd25c33dc421878219fa6e7d`；与安装记录、实际文件匹配。health/readiness UP；临时Flow配置已恢复且监控已resume。
- ziyue/吴用创建测试519（会话1760458007097），上传/刷新/自动选中、手机预览、创建与指派通过；首轮识图在模型启动前失败，未继续生图/改图调用。
- 根因：共享Codex于2026-10-23北京时间19:20–19:21被替换为0.164.0，Runtime1.2.8仍绑定原0.161.0测量，抛`CODEX_APP_SERVER_CONFIGURED_EXECUTABLE_DRIFT`。现行Runtime合同未包含0.164.0；仅重启不足以解决版本合同不匹配。没有证据确定哪个操作者执行了升级；本次API部署不改该包。
- 519已准备资料但无engineThreadId/runningAt，Runtime为RECOVERY_REQUIRED；后端最后回读仍RUNNING/DISPATCHED。首次停止点击被浏览器写保护拦截，未抵达后端，未冒充取消成功；不直接改数据库或重放。
- 当前结论为 **DEPLOYED / BUSINESS_REGRESSION_BLOCKED**，非完整验收通过。后续需处理Runtime对现用Codex的适配与项目专属依赖隔离，再执行完整多轮矩阵及519状态闭合；不擅自降级共享Codex、重启其他任务或关闭完整性校验。
- 发布、截图及根因证据见[上线回归](../../../specs/juyiting-skill-execution/evidence/previous-output-release-20261023/README.md)。之前“未部署”条目仅为其记录时点的历史事实。
