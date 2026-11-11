# WEB-DEPENDENCY-SETS-20261109

Owner：sol-owner/developer（本会话）。授权来源：用户对按锁文件/工具链共享完整node_modules方案答复“好，处理吧”。范围为既有本地Web构建工具及其定向回归；不启动Flow、不发布、不改生产/主工作区依赖、不清理他人缓存。

## 源码与边界
根工作区 `/home/isp/wsps/cyf`，本地HEAD `c311a4dfb439c88e7ea61aa4aa25064be6ce6ac4`；复用现有脏工作区，不覆盖他人改动。本任务仅改 `ops/orchestration/{web_dependencies.py,local_web_build.py,local-web-build.mjs,tests/test_web_dependencies.py}` 及README本节说明。后两个已有工具是前任务遗留未跟踪文件，不声称新建或整文件归本任务所有；测试前按实际文件SHA固定输入。未查询远端，不声称HEAD为远端最新；本任务无应用源码/接口合同变化。

首轮依赖共享工具测试与此前技能修复分开记账，累计17.632/600秒；原技能批次约592.928秒历史与失败保留。后续用户“继续”后按此前申请原批次900秒接续，真实安装/构建及补充工具回归全部计回原批次，未重置。详见NATIVE-READINESS-DECOUPLE-20261108续作节。

## 方案与验收
- 既有 `local_web_build.py` 默认按manifest/lock、Node版本/ABI/平台/架构/二进制摘要、npm版本和有效安装配置共享完整依赖集。不同输入不同目录；不把现有不完整node_modules当缓存种子。
- per-key锁、独立暂存npm ci及npm ls、成功后原子发布；失败不出现可复用集合。不覆盖已有不同依赖目录/链接。
- 普通磁盘；共享目录权限只读，记录全文件摘要/模式/内部链接，复用及完成构建后核对；这是防误写约束，不宣称能阻止同属主/root恶意修改。
- 本工具明确支持CYF当前integrity锁定的registry依赖；root安装生命周期/workspaces/本地链接依赖需单独适配，不猜测可共享。
- 定向验证涵盖复用、输入隔离、安装失败/不完整/损坏拒用、已有目录保护、并发原子发布、外链和内存盘拒绝；另用极小合成包的loopback tarball运行真实npm ci/ls与第二源码目录复用。首轮不运行Web生产构建；续作已按原批次执行真实Web构建，始终不运行付费模型。

## 当前状态
工具源码、真实Web锁完整安装/复用及生产构建均通过；共享集合be17a094...已启用供同输入本地构建使用。Web的ESM配置兼容修复038a571和Runtime92df9eb已合入各自远端develop；根工具仍未提交/合入，未部署。主工作区旧node_modules保持未动，任务临时依赖已受控替换/收尾。

证据：`/home/isp/state/cyf-local-build/tasks/web-dependency-sets-20261109/evidence/`：verification.json按次保留输入SHA、命令、日志摘要与耗时，source/保留首轮工具快照，source-final/固定续作最终工具快照，current-status.json区分代码、验证与实际集合状态。根工作区含既有未跟踪工具和他人修改，本任务只接入指定工具，不整包提交混入他人内容。

- 首轮14项通过5.101秒；补实际Vite冒烟后15项通过5.980秒；最终依赖工具17项通过5.715秒。
- 既有存储测试误用系统Python3.6，0.145秒失败（其测试使用capture_output/text，并非依赖实现失败）。原日志test-03保留，未改测试降级；按已有README要求用Python3.11重新执行，7项通过0.521秒。
- 既有发布控制器5项通过0.170秒；包括仅构建计预算、不把deadline下传安装等约束。
- 首轮有效定向验收为17+7+5=29项通过；本工具独立范围累计测试/小型fixture打包构建（含首轮、失败和重跑）共 **17.632秒**。后续补充ESM alias fixture的17项再次通过，5.660秒及真实Web安装/生产构建计入原技能批次。日志中的recordedAt为UTC完成时间，对应北京时间2026-11-09。
- 真实npm冒烟以loopback提供的自建极小tarball验证npm ci完整性、npm ls、只读发布、第二源码目录免重装以及实际Node require。另以已有Vite运行极小独立HTML/JS项目，使用runner加载原配置、输出到独立批次目录，核对现有node_modules/.vite-temp逐文件状态未改变。不是CYF完整生产构建/端到端验收。

## 真实集合与后续（2026-11-09核对）
真实共享集合：`/home/isp/state/cyf-local-build/web-dependencies/be17a0949f5e5802a8bc6d46ec3b326f0b27068e615c8a6737abd978fe108c08/`，receipt SHA-256 `5ab3292119f2572ba189d46392240e9bc701aac95616abce95eee9bdfab6a95e`。Node24.22.1/npm11.19.1/linux-x64，来源Web manifest/lock摘要见对应receipt和真实producer result。第二次构建dependencies.reused=true，未再npm ci；reuse核验3.802秒。Vite原配置需显式ESM目录，Web038a571已修复并对六个alias/LESS路径真实runner加载回归。不能用极小fixture通过替代真实Web构建证据；两类均已分别保留。

原技能批次最终681.191/900秒（含1秒保守前置），Web113通过/2 pending及生产归档逐文件校验通过；Runtime保留721通过/15 opt-in跳过的精确输入复用证据。未启动Flow、未部署/重启/改生产数据或付费模型调用。最终Web包已按既有完成登记收口；复用前mark-active，真实包位置见原任务artifact-retention-location.json。本工具自身无独立发布包；测试临时目录与两个已合入的应用任务worktree已删除，包外证据与共享集保留。工作树收尾时磁盘约198MiB，最终00:32读回约1.3GiB；不对同期全主机空间变化归因，未清理他人文件/缓存。

根工具本身留在已有脏工作区，未将先前未跟踪builder或他人README内容夹带提交；正式使用按文件SHA绑定。后续发布须另有明确授权，不因共享集准备或develop合入自动发布。
