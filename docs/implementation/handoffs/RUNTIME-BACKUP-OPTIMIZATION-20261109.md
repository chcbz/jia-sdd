# Runtime 备份体积优化（2026-11-09）

## 范围与固定输入

- Owner：本会话；任务标识 `RUNTIME-BACKUP-OPTIMIZATION-20261109`。
- 用户授权：继续实现备份优化策略。首项只实现旧程序无损压缩、隔离恢复与既有清理入口适配；不发布应用、不重启、不改状态备份范围、不转换任何既有实际恢复点。
- CYF 工作区 `/home/isp/wsps/cyf`，branch `develop`，基线 commit `c311a4dfb439c88e7ea61aa4aa25064be6ce6ac4` / tree `eae38803fd39dc44599bf6876d60802d91ed5139`。工作区已有大量无关脏修改和未跟踪维护文件，按文件摘要绑定本次候选，不冒充干净基线。远端 develop 本次未查询，不声称最新。
- 外部 Runtime 常规源码入口 `/home/isp/wsps/chcbz/isp-install`，本地 HEAD `c1fc18174b256c90051874485c8c77967efad62a`；已读该仓 AGENTS 及 CYF 根规则。本次不修改外仓，不变更接口合同。
- 初始追溯入口为 `/home/isp/state/cyf-local-build/tasks/image-usage-20261108/runtime/install/install-local-artifact.py` 和 `apply-prepared-runtime.py`；最终主机回读发现当前已是Runtime1.3.68，实际最近入口为 `/home/isp/state/cyf-local-build/tasks/cyf-native-readiness-20261108/runtime/install/install-local-artifact.py` / `apply-prepared-runtime.py`。已只读核对新入口同样保留old-program原子rename和完整state_paths。这些脚本是历史精确输入，prepared.json绑定摘要，不能原地改成未来通用模板。
- 当前恢复点以 `/home/isp/apps/cyf-agent-runtime-v1/release-records/current.json` 为准；本次不改记录。既有 `ops/maintenance/runtime_backup_cleanup.py` 已识别 `old-program.tar.gz`，但没有归档、校验和恢复命令。

## 职责及最小联动

备份存储适配器负责无损归档/校验、元数据与硬链接闭包、互斥和可恢复移除目录（RB-1）；不负责业务状态回退、服务控制或应用授权。复用现有维护入口、host→Runtime release 锁及逐文件 unlink，不新增服务、台账、审批或全链路改造。Web/API 不受影响。

必要防护的风险：压缩失败/磁盘满时先保留原程序；先独立恢复并对字节、链接、权限、所有者、时间及扩展属性复核，再允许移除原目录；拒绝源漂移、外部硬链接、挂载、占用与归档路径逃逸。新恢复只写全新磁盘暂存目录，不写固定 app/state，不启动备份、不自动覆盖新事实。状态压缩包和历史发布证据保持原样。

## 计划验收

在普通磁盘临时 fixture 中覆盖真实 GNU tar/gzip 归档→隔离恢复、内部硬/软链接、ACL/xattr/执行位/所有者、压缩/校验失败不删源、篡改/漂移/占用/锁冲突、部分移除可重入，以及已有 Runtime 保留回归。测试/打包累计预算600秒，完整交付墙钟另记；不执行真实应用构建或历史备份转换。用真实 fixture 与工具链日志、候选文件 SHA-256 记录结果。

## 实施状态

首项源码及主机维护入口安装完成，结果如下。工具链跨批共享和状态范围分类仍是后续独立实现，不在本项中猜测排除日志数据库/会话。完整备份优化策略尚未全部实施；未执行下一次应用发布或真实恢复点转换。

## 实现与回归结果

- 改动：在现有 `ops/maintenance/runtime_backup_cleanup.py` 新增显式 `compact-program` / `restore-program`，原plan/clean/cron行为不改。新增 `ops/maintenance/tests/test_runtime_program_archive.py`，稳定操作合同写入现有 `ops/maintenance/RUNTIME_BACKUP_RETENTION.md`。
- 归档流程：pinned manifest＋源树核验 → PAX/gzip1（保留硬链接/稀疏文件/ACL/xattr）→ tar compare＋独立暂存恢复全树核验 → 归档及receipt持久发布 → 原安全unlink逐文件移除目录。中断后剩余子集可接续，完整归档可独立恢复。临时恢复不激活，不回放业务状态。
- 首轮发现根目录mtime未恢复：GNU tar的 `--keep-old-files`跳过已创建暂存根的元数据。修复为只在独占新建、成员路径核验后的空暂存根恢复全部元数据，未放宽内容/时间比较。
- 后续最终防漂移编辑引入过一次缩进错误；同时发现既有Flow测试脚本读取位置参数helper，不能被通用unittest discovery调用。保留batch03失败；修复本次缩进后按原Flow脚本入口调用，不修改其源文件，不原样重试。
- 最终batch04：Runtime **64项**（旧41＋新增23）、Flow维护 **61项**、可回收缓存/包 **69项**、监控离线 **15项**，共 **209项通过**。Python3.6.8、GNU tar1.30；普通磁盘fixture，无生产安装/SQL/模型调用。包括真实进程扫描、硬/软链接、ACL/xattr/gid/执行位/纳秒mtime、压缩失败/磁盘满receipt失败/源漂移不删源、篡改/锁/挂载/keep/占用拒绝、部分目录移除恢复和重入、路径逃逸/链接子路径拒绝及原保留规则兼容。
- 证据：`docs/implementation/evidence/runtime-backup-optimization-20261109/batch01-{input,result}.json`、`batch01-tests.log`、`batch01-diagnosis.log`；batch02/03/04对应result与完整日志，原失败不重标。batch04绑定所有命令、测试文件及所用已安装安全模块的摘要，`inputUnchanged=true`。不是应用功能全量验收或源包构建。

## 主机维护工具安装与回读

- 2026-11-09 07:15:53 +08:00，在既有host cleanup→Runtime release锁下，保存旧helper并原子安装测试字节，未改其他helper/cron/环境。
- 安装目标 `/usr/local/libexec/cyf/runtime_backup_cleanup.py`：旧SHA-256 `7cf018f8fe61a92c14a7888d0b5f424a8d1e170e68a03a7e98aee42ef6df904b`；新SHA-256 **`8923aaffab572043b55a3903f6016728b41fd1c511e2fe7ad7cb8cbc4d4fb5d4`**，与batch04受测候选及readback完全一致。旧字节为证据目录 `installed-helper.before.py`（0600）。恢复工具仅需在相同锁下原子恢复旧字节，不涉及应用或状态回退。
- 安装前后Runtime1.3.68、current record SHA `be58c79a93f4268fdca427430fac3107e801e9ad1ad236f3c3ab8cc70b36a669`、MainPID3607269、NRestarts0、ActiveState active及被观测备份顶层文件身份/时间均不变；详见 `tool-installation.json`。此为安装期间只读观测，不冒充完整通道/业务验收。
- 已安装路径实际执行一个完整fixture归档→恢复→幂等冒烟通过；`installed-fixture.log` / `installed-fixture-result.json`。其余源码回归按相同字节复用，不重复应用构建。
- 已安装原plan只读验证：`installed-retention-plan.json`，删除0，current pin为 `20261109-native-readiness-local`。未知旧布局继续保护，不按本次任务扩为清理整改。
- **时间区分：** 已记录测试命令累计21.110秒（含前述失败＋最终维护回归＋已安装fixture）；另有一次短定向诊断及AST解析未单独计时，不能把21.110秒宣称为所有操作或完整交付墙钟。无排队/人工审批/重型构建，受限工作明显未接近600秒。完整交付墙钟从本轮07:04:40计，最终closeout另记录；安装/只读核验不下传构建预算。
- **空间归因：** 本任务没有转换真实程序/状态备份，不能声称已释放实际备份空间。更早20261107/20261108批次的PAYLOAD_RETIRED.json记载它们于2026-11-09 02:00:51/02:00:37被既有保留流程退休，早于本轮开始；不得归功于新工具。07:16根盘可用约2.9GiB仅是主机当前观测。

## 后续接续（不冒充本轮完成）

1. 后续Runtime发布Owner在新进程/通道验证完成、current verified-active且退出原安装事务后，复用已安装显式compaction入口；同步实际恢复说明。不能更改历史prepared/installer摘要，不能在pre-start恢复仍需原子rename时先移除old-program。当前新命令可用，不等于历史或未来所有一次性脚本已经自动调用。
2. 按固定内容及manifest设计跨批工具链复用，连同被保留恢复点的引用保护及独立恢复回归一起实现，不先建共享引用再允许GC误删。本项未实现、不把当前单包内hardlink保真当跨批去重。
3. 沿真实状态读写/恢复链路分类恢复必需与诊断副本；无证明不排除SQLite/完整HOME、身份、授权、会话、ACK或幂等事实。不自动缩减状态包，不恢复旧状态覆盖新业务事实。
4. 本任务无最终JAR/tgz交付包需mark-complete，无新worktree。保留日志/候选字节摘要及旧工具恢复证据；不清理其他任务目录。
