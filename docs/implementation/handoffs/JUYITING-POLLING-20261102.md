# JUYITING-POLLING-20261102

Owner：本聊天；2026-11-02用户要求全面排查Web/API/Runtime轮询，去掉不必要轮询或提出优化策略。

## 范围与边界

- 全仓扫描定时器/调度/递归重试，沿真实网络/数据库调用区分数据轮询、事件驱动补读、连接保活/租约、动画/计时器、后台可靠任务。
- 先盘点频率、触发/停止、可见性、在途串行、失败退避、身份取消、已有推送；只对确认冗余点做局部修复，不把大范围排查扩为全项目重构。
- 不删除身份/撤销/fence/幂等、租约与恢复，不以关闭后台任务/丢事件/屏蔽真实错误换性能，不自动重放旧任务。不新增统一框架、性能拒绝阈值或业务deadline。
- 本任务未授权新的生产发布/数据迁移，不接管其他任务安装和锁；重型测试构建仍走Flow，各Run<=600s，worker-only。不在本机编译/打包应用。
- 规则：/home/isp/wsps/cyf/AGENTS.md；RB-1 /home/isp/wsps/cyf/specs/juyiting-skill-execution/responsibility-boundaries.md；接口规范在固定API aa6ecf935343caed76f6d0c657f9847025de4600的docs/interface-standard.md。外部Runtime本任务显式遵守上述CYF职责与分层规则，但不修改其他项目/共享技能规则。

## 固定基线（16:18 fetch成功）

- Web origin/develop `339f3be8af09e09ba46e0b29a8e68d8fc30d8576`；本地HEAD ca22ac29、有其他任务脏改动，不能当当前源码。
- API origin/develop `aa6ecf935343caed76f6d0c657f9847025de4600`；本地HEAD516267bf、有大量其他任务改动，保留。
- Runtime `/home/isp/wsps/chcbz/isp-install` HEAD及origin/develop `32416ed5bbde7ee25ba199ad586dbd0e4386e89c`，主仓当前干净。审查仅CYF相关conf/codex-bridge及conf/cyf-agent-runtime-v1。
- 实际线上记录：Web401/1.16.90/5470363fc33d7689890763a54eb0ee23ac8d84d2；API439/8ad42be7815e499077c6a97439f0f13c96c7650e；Runtime RELEASES记载116/1.3.33/32416ed。源码盘点与线上版本分别核对，不将最新develop行为冒充已上线。
- 轻量入口：ops/orchestration/README.md；用git show/grep读取固定源码，暂不创建worktree或修改共享脏源文件。
- 证据：/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/，baseline.json、各层timer命中和定向源码快照。命中数量不是轮询数量，排除测试/历史证据/资源生成物后人工分类。

## 验收

交付按层/功能的轮询清单与处理建议；实现范围明确，定向验证覆盖在途不重叠、隐藏/卸载/身份切换、断连恢复、终态与失败语义；源码修改/测试/集成/上线分别记录，不以源码静态搜索代替生产流量测量。

## 本轮实施

- 审计报告：`JUYITING-POLLING-AUDIT-20261102.md`，覆盖Web网络读/恢复、API持久发现/SSE后台扫、Runtime双命令lane及心跳派生对账；timer文本命中不当作请求数。
- 共享Web源在旧branch且有本任务相关脏改动，已最小隔离到 `/home/isp/wsps/worktrees/juyiting-polling-web-20261102`，branch `codex/juyiting-polling-20261102`，base339f3be8。继承本任务根规则与Web AGENTS；不覆盖原工作区。
- 仅内部无界面/协议改变：场景singleflight+隐藏页跳过；回复poll在途保护+停止回调隔离；修正正文出现但请求仍busy时提前停核对。
- 两个既有测试文件定向75项通过（轻量Mocha、无build）。首轮暴露旧停止条件，已归因修复，不跳过测试。正式Flow未运行；API/Runtime未修改、未部署。
- 待验候选commit：`5eaf8e1191abc859043953bdc4e01f53a9e2cb79`，tree：`8ac2352b615d58fe1fe63ec33d7b4c9b61aae9ed`；仅提交本任务4文件，未push/合入/发布。工作树保留供后续Flow与集成使用，未清理他人工作树。
- 定向ESLint返回2项错误；对固定base用stdin重跑确认两项均原有（scene未使用parseVersion、conversation属性简写），未新增规则豁免或顺手清理。详见证据web-eslint.log和web-eslint-baseline.log；不能宣称lint全绿。git diff --check通过。

## 用户收口：先完成前端（2026-11-02）

- 用户明确先落地前端，后端/Runtime方案再讨论；本轮不修改两端源码、调度、参数或服务。前述“唤醒+退避”仅候选讨论，不是已采纳设计。
- 复用原Web worktree，fetch后将本任务首批commit rebase至远端develop `4ea31bb`（1.16.92），保留其他任务议事图片/工具栏修复。最终完整SHA以候选回执为准。
- 本轮范围：技能市场无待办停timer，活跃操作只查原change且终态合并目录刷新；打开/返回前台/匹配跨页签存储通知重新读取权威目录；不自动重放未知写入。补技能结果、议事、成果目录、验收、个人执行、点将等待、案卷问答的页面可见性/在途/停止代次保护。
- 不改界面布局、控件、操作路径、报价确认或展示语义；沿用现有刷新按钮和错误展示。本轮为内部网络生命周期优化，不新增无关交互原型或新轮询框架。权限仍由服务端核对，展示结果不做跨身份全局缓存。
- 技能结果仅在本轮后台tick跳过已终态引用；手动刷新/返回前台/作用域改变仍全量重新核验。完成正文和持久request终态仍区分。
- 必要降级/未知结果核对/失败重连保留，不以性能预算取消执行、不新增业务等待截止时间；PWA更新与本地动画/倒计时不是本次高频业务网络轮询整改目标。

## 前端集成与正式验证（2026-11-02，17:41 CST）

- 最终基线更新至Web develop `98f7682c9928ec7d1f91b50519b0a20263a1049c`，保留其他Owner同期修复。Web1.16.95，候选 `362f2fc094e89eff853d81c0e3c2b9f086356b55`，tree `ecf667b7a2e083119821af211709ee1cd4b0470f`；task branch与develop均已push成功。此前5eaf8e1/4ea31状态仅历史，不是最终候选。
- 正式Flow `4403172/407` SUCCESS；固定上述SHA，安装依赖/完整测试/Vite构建/制品上传及代码扫描作业成功，Run创建至更新终态134秒（17:38:05—17:40:19 CST）。扫描成功不表示无告警，不能宣称全仓ESLint全绿。没有Flow SSH/VMDeploy/主机等待，没有安装或线上业务验收。
- 控制面保留原配置备份，只更新已有expected SHA；readback一致。原flow-control start因历史分页在写请求之前拒绝；随后按SDK文档完整分页只读核对所有历史及无活动Run，核对原配置摘要，再单次启动返回407。没有对模糊启动盲重试，未改公共控制工具。证据flow-full-history.json、web-start-context-reconciled.json、flow-start-sdk.json。
- 本机轻量回归：frontend-core-final.log 184通过；demand-tests.log 133通过（与前者重叠，不相加）；market-component-final.log实际组件2通过；archive-visibility-tests.log实际组件1通过；scene-final-tests.log最终scene20通过。后者命令同时指定不存在的workspace测试文件，只有scene真正执行，不能声称workspace通过。正式覆盖以407制品内报告为准。
- JS生产源码定向ESLint未报错；两Vue文件既有155错误/131警告按rule/message与基线一致。追加检查测试文件发现14项风格/既有诊断，保留js-eslint-final.log与test-eslint-baseline.json，不声称所有测试文件lint通过。git diff --check通过。
- 后端/API与Runtime仅保留审计建议；未实施唤醒、退避、队列或缓存改造，方案须另行讨论。尚无生产请求量/CPU改善实测。

### 制品与收口

- 407同Run不可变制品读取核验：commit/tree/version/run均匹配；完整Mocha报告3686 passing / 2 pending / 0 failing，508 suites，61.275秒。制品109696700字节，SHA-256 `9841368e2fcae537e6f7e566d547d7acc5bd9095dcb00f97896b01d3593b2bbb`，612个dist文件；仅验证来源和报告，不安装。证据 `frontend-final-evidence.json`、`flow407-test-report.json`、`flow407-release.json`。下载首次网络超时，按同一不可变对象Range续传并核对完整大小/归档/来源，无重复构建。
- 补充lint边界：测试文件14诊断中基线已有9项，本轮新增5处多余空行风格提示；生产JS无错误。保留真实结果，不将云端scan SUCCESS宣称全仓无诊断，不为纯风格追加付费构建。
- 17:47 CST只读远端核对develop与task branch均为362f2fc；本任务worktree干净且只有共享node_modules符号链接，保存证据后移除链接并删除本任务worktree，保留已推送commit。未动共享Web/API脏工作区、他人进程/工作树、生产安装及身份状态。
- 稳定知识追加至docs/juyiting-runbook.md“前端后台观察生命周期”；该文档既有其他任务改动未整体提交，根gitlink保持不动。后端/Runtime方案等待后续讨论；前端已集成及正式验证，未部署、无生产性能改善百分比。

## 用户授权部署（2026-11-02 18:32 CST）

- 用户明确“部署”，只部署本轮Web1.16.95；复用Flow4403172/407固定362f2fc及原SHA-256制品，无新增构建/运维Run。安装前实时查询407仍SUCCESS，线上原Web406/1.16.94/98f7682。
- 在现行deploy.lock下备份原612文件与record，tar compare成功。备份 `/home/isp/baks/cyf-web-flow/20261102-polling-web407`；归档SHA-256 `c84da377cfe02e1efb60d00a052f1cd45091a3663b063201a4502b3aea9ec47d`，RECOVERY.md保留恢复说明。固定来源复制至现行downloads/407/package.tgz并复核摘要；未本机源码构建。
- 原受控 `/usr/local/sbin/cyf-web-flow-deploy` 安装exit0，record为407/362f2fc/online_verified。公网首页最初两次返回已知旧入口，第三次匹配新摘要；未绕过验证或重新构建。
- 独立只读核验612个安装文件全部匹配；公网首页/入口资源/聚义厅/技能管理及市场路由共11项HTTP200、长度/SHA-256匹配，并核实相关JS从当前入口依赖图可达。证据 `/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/deployment/deployment-verification.json` 与web-public-resources.json。
- API/Runtime未修改或重启；没有数据库操作。该结果为安装与线上资源核验，不冒充登录业务全流程或生产请求量/CPU收益测试。已打开旧页面需刷新加载新版本。本节替代本任务此前“未部署”的当前状态，历史CI记录保持原貌。

## 后端/Runtime实施开始（2026-11-02，用户授权先复核再实施）

- Owner仍本聊天。API固定ef702265c2aee075ab077f8e94b9963a4ef58ed9/tree d9ac51fa9fafd3b408a47fda25b30d5b92d16085，Runtime固定9ac44c2fdeb390202497d4bff6e7de36078cc3c1；fetch成功。API生产record442来源同上述API；Runtime安装package1.3.33，不将源码9ac44c当线上。
- 共享API旧分支大量脏修改，Runtime主工作区属另一任务且有未提交specs；最少隔离为/home/isp/wsps/worktrees/juyiting-event-api-20261102和/home/isp/wsps/worktrees/juyiting-event-runtime-20261102。显式遵守本项目AGENTS、RB-1、分层职责及固定运行目录；接口规范使用API上述commit的docs/interface-standard.md。无子Agent，无部署/迁移/启用Rabbit授权扩张。
- 现场修正：外置/生产默认合并读取agent.rabbit-dispatch.enabled=false、archive.question.enabled=false，chat.bounty-bootstrap.enabled=true。因此不把未启用模块列为线上热点，不为本次优化启用Rabbit。自然60.8秒采样API单核CPU15.05%、Runtime47.09%，公网日志21条但无命令发现端点，不能当Runtime空闲或请求数为0；SQL性能schema查询1045未取得数据，不绕过认证。5分钟Runtime日志87条native poll partial，3306次SKILL_COMMAND_INVALID、174次绑定冲突（是日志出现次数，不是任务数）。证据implementation-review/。
- 第一批闭环限于已启用bootstrap：提交后事件唤醒、合并单次调度、已知重试到期唤醒、保留集中恢复查找与原领取/fence/失败语义。恢复间隔候选5秒复用现有执行协调5秒发现量级，只影响漏通知补偿、不改变业务deadline/租约；须测试说明最大额外发现延迟。Runtime先把每轮全部历史扫描收敛为启动/重连扫描加未完成ID索引，持久命令/结果仍权威，不缓存技能包。
- 本轮不会先删Runtime3秒HTTP发现：新WS通知、重连握手、跨实例路由和本地UNKNOWN恢复覆盖仍待实现；SSE共享补偿和其余relay也不冒充完成。最早验证：bootstrap调度/提交与回滚/过期生命周期回归，Runtime历史/未完成/权限与重连定向轻量测试；Java正式构建回归走Flow。

### 第一批源码与验证进展（2026-11-02 20:46 CST）

- API候选 `2723bdc37576eed2cb490c6b240638d1159d8445` / tree `0d0099ed2ce23f9c9ae63a69b99c18b762ea5aa2`，已推任务分支；未合develop。新增bootstrap事务提交后进程内通知，relay单次定时器合并通知、领取后继续排空，空队列5秒恢复扫描；原事务、作用域领取、CAS/fence、租约及重复永久失败停止规则不变。通知不携带授权或任务正文，不作为领取凭证。数据库瞬时故障按原1秒起指数退避的准确到期时间调度，不被5秒补偿周期拖后。回滚不通知；通知失败不把已提交写入报成失败。
- API定向回归新增提交/回滚/无事务/通知失败4项、通知风暴/在途尾沿/未来重试/旧生命周期等调度回归及两个生产者注册断言；本机仅diff检查，未运行Gradle。正式Flow5260799/443正在执行，沿用原无部署云端配置（配置摘要2cb56d7b90a37b1ef1c6d03044ec281784b59ef663c217f7dab40dfbfd7b0f14），既有mmdU1BootstrapOutbox与mmdControlledImageBridge选择器已覆盖新增测试。无改配置/删回归/启用Rabbit。Run参数指定任务分支，不使用未测试develop或重复构建。
- Flow启动单次成功返回443；初次监视器把早期API未提供commit误判为不匹配，退出的是本机监视器，不是Run。只读核实同一443后恢复只监视，不重复start。服务返回sources只有branch/repo，无commint；不能用该接口宣称完整SHA已核实，须最终制品确认。独立监视器保留600秒总预算（含取消传输裕量），不等待主机验收、不取消他人Run。证据 `implementation-review/api-ci-*` / `api443-*`。
- Runtime候选 `1230924` 已在原9ac44c上自检并快进push develop；Runtime1.3.34 / bridge1.1.24，未打生产包、未安装。平时只维护未完成executionId集合，每次仍核验磁盘command/attempt/receipt；第一次及认证重连全量发现。新执行在store成功绑定后加入索引，终态下次检查移出；不缓存技能包/正文、不改业务授权或UNKNOWN外部效果处置。源代码核对本目录仅SkillConversationLane创建SkillExecutionStore；外部历史写入不冒充实时任务入口。
- Runtime本机轻量回归：conversation44 + store12 = final56通过，agent-client native poller2通过，共58项；无跳过/失败。覆盖空API页恢复、UNKNOWN退避、持久记录身份冲突、失效历史只发现时报告、认证启动/重连重扫。脚本语法与两组件git diff --check通过。不是云端打包、线上业务验收或全量Runtime测试。
- 文件夹具测量（非生产数据）：65条历史（53完成/6失败/6未完成），20轮全扫打开文件6380次、4782.998ms；索引后480次、84.564ms，仅保存6个ID。耗时含缓存/验证预热差异，不推导线上CPU收益；文件打开次数由真实fs.openSync计数。夹具使用临时目录并清理，不读取/复制生产业务正文。证据 `implementation-review/history-scan-benchmark.{mjs,json}` 与runtime-*-tests.log。
- 剩余范围：Runtime3秒HTTP命令发现仍保留，尚未实施WS工作提示、重连补领与多实例通知路由；SSE共享补偿及其他relay未改。不能称后端/runtime整体去轮询完成。日志中的现存有效执行绑定冲突仍按原错误处理，不由本次性能改造伪造绑定或重放。

### 第一批正式验证与集成（2026-11-02 20:54 CST）

- Flow5260799/443 SUCCESS，启动请求至终态更新410.608秒，未触发取消。Gradle327.151秒，日志BUILD SUCCESSFUL；398个suite汇总3348次测试执行、150跳过、0失败/0错误（存在同类在不同sourceSet重复执行，不称3348个独立用例）。云端必要测试/validateLayering/bootJar/上传完成，无主机安装动作。
- 从最终日志提取CYF_DIAGNOSTIC_CHUNK并校验完整base64长度及解压数据SHA-256，得到398份报告、编译诊断0。新增Publisher4项、relay12项均无跳过/失败；grant43项、outbox12项及其嵌套16项通过。证据 `implementation-review/api443-diagnostics.json`、`api443-verification.json`；API当前候选已fetch核对后快进push develop，仍为2723bdc375。
- CYF_API_ARTIFACT日志固定Run443、commit2723bdc37576eed2cb490c6b240638d1159d8445、tree0d0099ed2ce23f9c9ae63a69b99c18b762ea5aa2；云端报告JAR SHA-256为2a3f9f7345efc3dc077e145ad5f9c281f22bccb5a5ebf0181f22a7bd0c6fa7b5。控制API未返回commint的问题不猜填，来源核验使用云端构建输出和摘要校验后的测试诊断。
- 额外制品下载在180秒传输超时后保留179211660字节为`api443-artifact.partial`，不能用于安装、不冒充完整制品摘要核验。此次不部署，测试证据已从云端完整诊断取得，不为下载失败重复构建；如后续授权部署，复用443不可变对象续传并核验归档/完整摘要后安装。
- Runtime完整源码 `1230924707b678fed3857f68266e3de53228e203` / tree `4c8dc6a43824ea6863e97fc4ae149a3e3928b664`。两组件源码已集成，线上仍旧API442与Runtime1.3.33；本轮没有重启服务或变更数据库。整体事件化仍未完成，现有任务工作区保留用于尚未接入的WS/恢复链路，不复制新阶段工作树。

## 第二批：原生CONVERSATION工作通知（2026-11-02，继续授权）

- Owner本聊天；复用原两工作区，基线API2723bdc375、Runtime1230924，fetch后origin/develop一致。RB-02保持API授权/状态机，RB-03只调整执行发现/本地恢复；Web、workspace-file旧lane及SSE不在本批修改范围。跨边界统一接口使用API2723bdc375的docs/interface-standard.md，通知沿既有WS信封。
- 正常路径：原生执行入队事务提交后提示本机WS会话；Runtime收到提示后通过原HTTP发现/领取。通知无命令正文、无授权、无持久接手ACK。注册回执确认通知版本后才停3秒发现；旧服务端仍原周期兼容。先确认订阅再启动补读，在途提示置dirty并在尾沿补读；断连、换身份、旧调度器隔离。
- 丢通知/提交后崩溃/跨API节点：每WS节点一个集中补偿周期，查询配置tenant/client和当前订阅目标中的QUEUED原生工作，仅通知本节点当前有效会话；不引入Rabbit/Redis/CDC。候选周期30秒沿现有Runtime心跳量级，跨节点/漏通知可能额外等待约30秒+处理，并非零延迟或高可用保证。空目标不查DB，无工作不发客户端HTTP提示。
- 本地UNKNOWN/上传/提交恢复独立于发现HTTP：按既有重试到期调度，只处理持久未完成记录；无通知也不能让执行卡死。租约/心跳不删。测试重点：注册竞态、在途唤醒、丢通知补偿、旧会话/跨环境不通知、空队列静默、已知UNKNOWN到期、分页排空、新旧混合。尚未实施/验证/部署，不把此段当完成证据。

### 第二批实现/验证进展（2026-11-02 21:41 CST）

- API候选 `94ab8bf2a69bf7c099406afc74a3a80cf7c62fbf` / tree `b34bef3cabe3d4850db8c76980eac0fb1989fbc3` 已push本任务分支，Flow5260799/444正在验证；未合入develop、未安装。复用443原云端worker-only配置，无配置写入；控制脚本只监控本次Run，570秒发取消预留600秒总上限传输余量。
- 已实现after-commit提示、注册协商、本节点订阅/当前持久会话栅栏检查、单30秒补偿查询；Runtime拆开HTTP发现与本地UNKNOWN恢复、在途合并/尾沿补读、旧API3秒兼容。共享wire fixture位于API `chat/jia-chat-service/src/mmdRegressionTest/resources/contracts/native-work-hint-v1.json` 与Runtime `conf/cyf-agent-runtime-v1/test/fixtures/`；合同详见API `docs/interface-catalog/native-work-notifications.md`。
- 复查发现补偿SQL原无目标队列索引，新增**显式运维安装**非唯一covering index脚本 `db/agent-personal-workspace-native-work-index-v1.sql`，不加CHECK、不自动启动DDL、不因缺性能索引拒绝启动。独占MySQL夹具增加10,000历史行EXPLAIN前后核验，正式结果待444；线上索引/规模性能尚未验证，未执行生产迁移，部署前需固定目录真实快照与授权。
- Runtime轻量定向：lane/scheduler52项通过，agent-client poller2项通过，adapter/共享wire/安装清单12项通过。首次扩大runtime-host诊断发现新模块未加入`EXECUTION_PAYLOAD_FILES`，导致9个清单/导入关联失败；修正后重跑全部9个失败项+新增3个wire/协商项共12通过（不是全量最终重跑）。中间fixture误传object而非JSON文本已修复；原失败日志保留，不抹除或当通过。
- Runtime候选升为1.3.35/bridge1.1.25，未打生产包/未安装；证据路径 `native-notifications/`。workspace-file、SSE及其他relay仍不在本批完成范围。阶段记录不等于正式Java测试通过或发布成功。

### 第二批正式验证与源码集成（2026-11-02 21:50 CST）

- Flow5260799/444 **SUCCESS**；实际Run起始至终态更新370秒（21:39:43—21:45:53 CST），启动请求至终态370.672秒，符合600秒上限。必要测试/validateLayering/fresh bootJar/上传完成，无部署作业、主机调用或等待。401个suite，3359次测试执行、150跳过、0失败/0错误（不称独立用例数）；正式诊断gzip解码长度与SHA-256已核验。
- 新增 `NativeConversationWorkDiscoveryMySqlTest`2项、`NativeConversationWorkDiscoveryTest`4项、`ChatBountyBootstrapRelayRecoveryTest$NativeWorkNotifications`4项均无跳过通过；实际生产者`SkillExecutionServiceTest`58项、WS目标/共享wire测试所在class4项、既有bootstrap relay12项均通过。10,000历史行MySQL EXPLAIN断言证实该合成分布由全表扫描转为`idx_pwex_native_work`访问；没有将此推导为线上延迟/CPU收益，未测生产多订阅规模。
- API固定源码保持 `94ab8bf2a69bf7c099406afc74a3a80cf7c62fbf` / tree `b34bef3cabe3d4850db8c76980eac0fb1989fbc3`，最终Flow来源与日志/诊断一致，JAR云端SHA-256 `3bd3c04cbcd7f0b2bcee4710b8e83564240479c0850da4fd57c483af8dde01e1`。本轮未下载归档、未验证本地安装文件，不因已知云端hash声称已安装。
- Runtime固定源码 `4a89d638ac4beac52843204ad5ebb446428b3949` / tree `46336ffbda82623f51e6ea265eafe3682ab50f4d`，Runtime1.3.35 / bridge1.1.25。最终选择的本机定向回归合计66项通过（52 lane/scheduler、2 poller、12 adapter/fixture/payload）；未做最终全量Runtime重跑/云端生产打包。两端共享wire fixture SHA-256均为 `61b43808b06ccd13215ede01aa81fd4e5b4ded30d78a89f3f0f782ddcc1ff30a`。
- 两组件重新fetch确认远端develop仍分别为本批基线后，均已**正常快进push develop**，无force、不覆盖共享主工作区的未提交内容。API94ab8bf2a6、Runtime4a89d63为本批集成版本，**不代表线上版本**。没有重启服务、安装包或生产DDL；此前线上API442/Runtime1.3.33是历史观察，本次未重新核验线上版本。
- 证据 `native-notifications/api444-{diagnostics,verification,final-full-log}.json`、`runtime-verification.json`及相应测试日志。下一步授权发布时须先核验生产索引/固定真实目录快照，受控执行显式索引迁移，再消费444不可变API制品；Runtime仍需既有Flow制品验证/打包流程，不能拿本机源码测试冒充发布包。旧API/Runtime兼容策略允许分步安装；跨节点漏提示仍可能30秒加处理等待。
- 本批范围已集成；workspace-file每3秒发现、SSE每订阅补读及其他relay仍待后续，不宣布整体去轮询完成。当前两个工作树用于连续专项，未新增临时worktree；根gitlink因共享主组件工作区存在其他未提交改动未机械切换，准确源码以上述固定SHA为准。
