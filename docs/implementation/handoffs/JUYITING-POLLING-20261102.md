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

## 第三批：任务SSE集中补偿（2026-11-02，继续授权）

Owner本聊天，复用API工作树，fetch后HEAD/origin/develop均为94ab8bf2a69bf7c099406afc74a3a80cf7c62fbf。统一接口基线同该commit的docs/interface-standard.md；RB-1及分层规则：持久层负责批量SQL分区，ReplayService只做调度；Controller原有授权不复制、不变Web/Runtime合同。workspace-file核实仍有真实HTTP命令入口，本批不删除或改其执行语义。重型验证复用API5260799，单Run≤600秒，不部署。

目标：每订阅5秒定时/高水位查询→每实例单5秒定时、订阅完整scope去重并按tenant批量查持久版本；只有版本不同/未完成唤醒才调用原独立回放。订阅首读、事件hint、游标/缺页/保留期/背压、关闭/取消及业务授权不变；不共享事件正文、授权结果或游标，不新增长期高水位缓存。无订阅零timer/SQL。最早反馈为定向静态及已有Replay/DAO回归；真实批量SQL与隔离/索引访问在独占MySQL夹具验证。此段为计划，不是完成证据。

### 第三批候选与验证入口

- API候选604e8d15a65144183adf3839d0fa5569ad8a4f70 / tree2b4ac362e1c3c118140286556cbba148a94d19d8已push本任务分支；Flow5260799/445已单次启动验证，沿用444原云端配置并readback对比，无共享Flow/root policy写入。无部署动作。控制监控仅对应本Run，570秒受控取消预留600秒总上限。
- 批量接口采用完整scope和同tenant查询；回放依旧各自从权威数据库重建，不共享客户端游标。新后台查询复用现有task-meta作用域唯一索引，无生产DDL。单flight批量扫描使用原有catch-up线程池，不在timer线程读DB。
- 静态检查通过；服务级新回归包含6同scope订阅/20补偿轮次仅20次批量查询、独立tenant/缺失高水位、批量失败回原处理、慢扫描不叠加及最后取消中断。已有完整Replay生命周期/游标/背压测试与DAO测试加入既有unfiltered mmdU1BootstrapOutbox slice，避免修改其他Owner的共享CI配置；独占MySQL测试覆盖真实SQL和现有索引。正式结果待445，不将编写测试当通过。
- workspace-file实际入口仍为PersonalWorkspaceRuntimeFileController→runtimeQueuedCommands→listQueuedByTarget/queuedCommand，排除CONVERSATION但仍生产WORKSPACE_FILE_EXECUTE；本批未删其能力或3秒发现。它需后续独立完整通知/本地恢复闭环，不能因为原生lane已切换就直接关闭。

### 第三批正式验证与集成（2026-11-02 23:05 CST）

- Flow5260799/445 SUCCESS，启动请求至终态311.609秒（终态23:01:52 CST），无取消、无主机安装/等待。固定commit604e8d15a65144183adf3839d0fa5569ad8a4f70 / tree2b4ac362e1c3c118140286556cbba148a94d19d8，来源同时由最终Flow日志和SHA校验后的诊断核对。404 suites，3433次测试执行、150跳过、0失败/0错误；必要validateLayering/fresh bootJar/上传成功。JAR云端SHA-256 d7e3f2ce563632a04b0de258d2af349d627a8958ff1d9b1e77742030a6139c9a；未下载归档或验证本机安装文件，不冒充上线。
- 受影响集中回归74项全部通过且无跳过：AgentTaskEventReplayServiceImplTest67、AgentTaskEventReplayDaoTest6、AgentTaskEventHeadMySqlTest1。6同scope连接/20补偿轮次仅20次批量metadata调用是受控service夹具实测，不是线上SQL流量；原实现每连接独立补查的120次是由代码路径推导的同场景对比。真实独占MySQL另证实批量映射、tenant/client/owner/task大小写/重音/尾空格隔离，以及1000历史任务下复用uk_agent_task_meta_scope且不走全表扫描，无需生产DDL。
- 复查远端develop仍为94ab8bf2a6后，已正常快进push develop至604e8d15a6，未force、未覆盖共享主工作区。Runtime/Web本批无修改。规则/合同细节回写API docs/minimal-tenant-grey.md“任务SSE集中补偿候选”，候选指未上线；实现与本次正式验证以此记录为准。
- 证据 `sse-compensation/api445-{diagnostics,verification,final-full-log}.json` 和控制面记录。没有部署/重启/生产数据库修改，没有声称线上CPU、GC或请求量已改善。现有两个工作树保留用于后续范围，不新增隔离目录；本批临时编辑脚本完成后删除。
- 剩余workspace-file独立lane3秒命令发现尚未事件化；其他relay按实际启用范围与职责继续审视，心跳/续租/撤权等必要时间驱动不属于可机械删除项。本批只完成任务SSE集中补偿，不声称全系统零轮询。

## 第四批前置修复：workspace-file发现饥饿（2026-11-02，继续授权）

- Owner仍本聊天；复用API工作树`/home/isp/wsps/worktrees/juyiting-event-api-20261102`，fetch后HEAD/origin/develop同为604e8d15a65144183adf3839d0fa5569ad8a4f70 / tree2b4ac362e1c3c118140286556cbba148a94d19d8。Runtime工作树干净、基线4a89d63，本批暂不修改。接口规范使用该API commit的docs/interface-standard.md，RB-1/分层规则随外部Runtime范围显式继承；无新worktree、无部署授权。
- 沿真实调用链发现：PersonalWorkspaceRuntimeFileController→runtimeQueuedCommands→listQueuedByTarget先取混合队列16条，再在service排除CONVERSATION。16条更老对话记录可持续挡住文件任务，单纯增加WS提示无效。当前先把PRIVATE/TASK/历史NULL文件通道筛选下推至SQL排序/LIMIT前；唯一生产调用方是该文件队列入口，原生队列用另一查询，不扩大修改范围。授权、TASK租约、事务/幂等不变，无wire变更，无新增DDL或CHECK。
- 新增独占MySQL夹具WorkspaceFileQueueMySqlTest，复现旧SQL16条全CONVERSATION与修复后真实映射、排序/分页、完成后推进、未知mode/终态排除、精确tenant/client/owner/agent隔离；进入既有unfiltered mmdU1BootstrapOutbox切片。重型验证待固定候选后走5260799，≤600秒；未把测试编写当通过。
- Runtime已核实：processor.start恢复持久inbox；resume独立drain；HTTP发现只是持久接收而非立即执行/领取，重复页不能立即无限重取。此修复**尚未停掉3秒轮询**。另外TASK租约失效仍可能在LIMIT后被业务层排除，需继续解决该真实依赖后再接事件通知；不把此次通道筛选称为全部文件队列饥饿已解决。下一阶段需独立文件通知协商、完整分页推进和无进展退让，不复用native1确认冒充文件lane支持。

### 第四批前置候选验证中

API候选189da86d622a37254f31fd5828bf96b7bc01bbbe / tree6111c9f86f453d6ba7b36ea90c7de64c28572ea7已push任务分支；Flow5260799/446于2026-11-02 23:21:59 CST单次启动。复用445原worker-only配置，逐字readback一致，无云端配置/root CI policy写入。静态diff检查通过；本机没有Gradle或生产包构建。控制器只监控自己的446，570秒请求受控取消预留600秒总限；正式测试、集成待终态及诊断核验，不安装。

### 第四批前置修复正式验证与集成（2026-11-02 23:30 CST）

- Flow5260799/446 **SUCCESS**，终态23:27:49 CST，启动请求至终态350.604秒，低于600秒。首次本机监控进程返回143后，仅恢复对同一446的只读查询/监控，未重触发、未取消其他Run；成功终态发生在恢复查询之前。没有主机安装或等待作业。
- 固定源码189da86d622a37254f31fd5828bf96b7bc01bbbe / tree6111c9f86f453d6ba7b36ea90c7de64c28572ea7；终态API返回的源码、Flow制品来源与解码诊断一致，gzip/base64长度及解压内容SHA-256核验通过。405 suites，3436次测试执行、150跳过、0失败/0错误。新增WorkspaceFileQueueMySqlTest三项均无跳过通过，真实MySQL验证旧SQL16条全对话、修复后PRIVATE/TASK/NULL文件可见、完成后的页推进和精确分区；非线上耗时/请求量数据。原生CONVERSATION测试11项在两个既有slice分别通过，不将重复执行称为独立用例。没有宣称默认Flow未选择的PersonalWorkspaceExecutionServiceImplTest已运行。
- 云端JAR SHA-256 `632964d857565b8f6724778ba877fcd05c9246ad65331eaaa20aac30d33116ab`；本批未下载归档、安装或修改生产数据库。重新fetch确认develop仍604e8d15a6，正常快进push至189da86d62；无force、未覆盖共享主API脏工作区。Runtime仍4a89d63，本批没有修改/升版或打包；Web不受影响。
- 证据：`workspace-discovery/api446-{diagnostics,verification,final-full-log}.json`及控制记录。规则与调用边界回写API既有`docs/interface-catalog/native-work-notifications.md`前置修复节。本批仅解决**混合lane抢占LIMIT**；文件通知、独立协商、租约/不可派发候选的分页推进、执行中重复页退让仍待实施，3秒文件轮询保留，不宣称整体事件化完成或线上性能已改善。

## 第四批事件闭环：workspace-file（2026-11-02，继续授权）

Owner本聊天，复用两现有工作树，重新fetch核对基线API189da86d622a37254f31fd5828bf96b7bc01bbbe、Runtime4a89d638ac4beac52843204ad5ebb446428b3949。统一接口固定为该API commit的docs/interface-standard.md，RB-1和根AGENTS分层/Flow/固定目录规则显式用于外部Runtime；未新建worktree，不改Web，不部署。目标为失效租约等候选挡页、重复满页及独立通知协商；非目标是重放UNKNOWN、修改租约/业务授权、清理历史队列或新增MQ。

实现候选：文件GET内部按created_at+binary execution_id逐页检查既有业务资格，响应仍最多16条且不改wire。文件入队提交后提示，复用原单worker/30秒集中SQL扫描，target增加lane，不新增独立扫描timer；文件能力单独offer/ACK workspaceFileWorkNotifications:1，与native1互不推断。Runtime启动/重连补读，提示尾沿合并；通过现有processor drain完成唤醒下一页，重复满页不忙循环，不修改持久执行/ACK/UNKNOWN恢复。复用现有调度模块无新增安装依赖，候选Runtime1.3.36/bridge1.1.26。

边界：集中补偿只识别候选，不复制TASK授权，因此非空但全失效的队列仍可能每30秒提示一次；单次HTTP可以遍历多个有界页，不人为丢弃候选或新增等待上限。没有新DDL；前批idx_pwex_native_work显式迁移尚未生产执行。最早本机定向Node/static反馈已取得，真实Java/SQL待固定候选Flow验证，不将源码实现当发布。

### 第四批事件闭环验证与源码集成（2026-11-03 00:15 CST）

- 本轮跨过午夜，以下时间为**2026-11-03**。API源码 `192a590b2c8b690337818606a6180fca6f99a600` / tree `2aca1409d0612ec69d8c7faf3539ac28541fbda9`；Flow5260799/447 SUCCESS，00:02:42单次启动、00:10:11终态，启动请求至终态449.598秒。沿用原worker-only云端配置且readback一致，无配置修改、部署、主机调用或等待。自有监控独立进程结束，未触发超时/取消，不接管其他Run。
- Flow最终来源、制品及SHA校验解码诊断一致；406 suites，3480次测试执行、150跳过、0失败/0错误。相关61项无跳过通过：文件service38、文件真实MySQL4、通知真实MySQL3、通知service5、共享notifier5、真实WS/fence6。实际注册回执测试证明conversation开关关闭时文件通知仍可独立协商，再注册不再声明文件能力会移除订阅；共享SQL在10,000条合成历史中双lane复用idx_pwex_native_work且不走全表扫描。业务层回归越过16条真实失效租约候选和16条不支持输出候选，后续有效文件仍可发现，不改状态/授权。均为受控夹具，不是生产数据/性能验收。
- 云端JAR SHA-256 `3a4749fadecdf42e684572c6a01ef07969c2b3fe0b337bc5a6edecde4911491a`；未下载完整归档或安装。证据 `workspace-events/api447-{diagnostics,verification,final-full-log}.json`。首次重型验证通过，无盲重试。重新fetch确认develop仍189da86d62后正常快进push至192a590b2c，无force、未改共享主API工作区。
- Runtime最终源码 `125729f8291da2dc89048bc41850beb12c15a9ab` / tree `89b2e8051f54549a9930af1b491e45109b7a6269`（1.3.36 / bridge1.1.26）。复查补上停止/替换后的在途HTTP响应处置：旧响应在解码前释放body，逐项接收前再看调度器当前归属；不允许旧查询向新会话继续接收命令，不释放旧在途owner guard。没有回滚已持久接收的命令或改UNKNOWN恢复。对应独立补丁125729f已包含在最终候选。
- Runtime最终轻量定向**86项通过**：24项文件发现/实际持久inbox/去重/在途/会话及原native poller，10项adapter协商/共享wire/安装payload闭包，52项调度器和原生lane恢复。实际持久夹具16条文件命令只执行各一次；重复满页不增长pending、不立即循环，drain完成后再发现；属于本机合成I/O验证，非线上吞吐。不是Runtime全量suite/云端生产打包，尚无本候选可安装Runtime制品。固定日志/汇总见 `runtime-verification.json` 和三个 `*-final*.log`（最终poller为`runtime-poller-final-session-fence.log`）。重新fetch确认develop仍4a89d63后正常快进push至125729f。
- 两端共享文件hint fixture SHA-256 `af4469b313aed93a5254ae649734d1e1669078360fcf6419e13af42d129e36e3`。稳定合同回写API既有通知文档，Runtime接线/运维边界回写self-host指南2026-11-03候选节。无新增模块导入，沿原EXECUTION_PAYLOAD_FILES闭包。
- **未部署、未重启、未执行生产DDL，也未重新测量线上版本/CPU/GC/HTTP量。** 前批显式目标索引生产迁移仍待获授权、固定真实快照和实际schema/plan核验；若授权发布，API可复用447固定制品，Runtime仍需既有Flow5264702固定候选测试/打包。不能用本机测试充当安装包证据，不因下载/安装重试重复构建。
- 文件事件化源码范围已集成：协商成功后移除正常空闲3秒HTTP轮询，旧API兼容/网络错误重试、重连补读、本地恢复保留；native/file共享每WS节点30秒候选补偿。全失效但未终结的QUEUED候选仍可能每30秒提示/读多页，未宣称“零扫描”或解决历史队列生命周期；其他relay/position/archive等按实际启用与职责仍需后续核对。现有两干净工作树为未完的整体轮询专项复用，未新增工作树；本轮临时编辑脚本删除，不清他人证据/备份。

## 2026-11-03 用户授权部署：固定来源与执行中记录

- 本轮用户明确“部署并完成后续任务”。Owner仍本聊天；API固定447/192a590b2c/tree2aca1409，Runtime固定125729f/tree89b2e805，复用原两工作区，不覆盖主工作区其他Owner脏改。唯一新重型Run为Runtime5264702/120；API不重复构建，Web不重复部署。
- Runtime120 SUCCESS，观察终态约318秒，worker仅测试/打包/上传；806 Node pass、10 skipped、0 fail，另Python15、browser artifact2通过。归档253006913字节，SHA256 `6a60080f252579b0a61bddd58e54e5d68d01a2cf8a86ed14f4d8133a616545e4`；689个payload成员/摘要/权限与来源核验通过。云端配置已按CAS恢复原值；不取消其他Run。跳过的真实sandbox能力由受控安装器在停旧服务前做原有主机probe，不声称云端完成这部分。
- API447归档224068966字节，SHA256 `b78e4298f71f93733dbe7e5e81d007fc1c1fc697fa105124dccbb2fe042f2247`；同Run receipt/source/tree/3480项测试/61项相关回归及JAR SHA `3a4749fa...91491a`均一致。首次任务侧回归选择器误用Java嵌套类点号，核对真实报告后改为`$`，未改测试/重建或放松断言。
- 安装前真实版本为API442、Runtime116/1.3.33。API沿现行`cyf-api-flow-deploy`锁/备份/恢复调用，Runtime复用现行固定app安装器，只替换本任务固定来源、前版本、备份与暂存路径，不修改身份/配置或回放历史。安装执行由本机systemd任务承载，不伪造Flow身份，也不把Flow600秒限制下传应用启动。
- 00:32 CST生产`jia.agent_personal_workspace_execution`显式添加非唯一`idx_pwex_native_work`；数据库UUID/datadir均固定核对，目标表一致性逻辑快照及DDL落真实目录`/home/isp/baks/cyf-native-work-index-20261103/`（不是活跃datadir物理复制）。前后65行、旧索引保持；不改数据/主键/唯一键/CHECK。实际混合双lane EXPLAIN选择该索引range、覆盖7个key parts，估计7行；不是万级生产压测。恢复不得覆盖新的业务事实。
- 证据统一`/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/release/`，包括Flow120/config恢复、两制品验证、index-migration/production-index-plan、API安装与Runtime安装子目录。**本节写入时安装/启动仍在进行，尚不能宣称部署或业务验收完成。** API新PID2157405正在冷启动，Runtime候选正在真实host probe；最终状态须见后续补充。

### 部署中发现的后置工具缺口与恢复（01:10 CST，尚在执行）

API应用安装与初次健康UP已成功，但F06后置schema runner仍将receipt.source.branch写死为develop；447实际固定候选分支为codex/juyiting-event-api-20261102，故在任何SQL前报receipt_release_identity_mismatch。E05同样存在该限制，正在以**现行已安装工具字节**为基线仅移除分支名单，保留真实Run/完整commit/tree/clean/identity digest/制品/目录/权限/发布锁及schema核验；依赖的E05 runner摘要同步更新。root源码含其他Owner修改，另外只补同一局部差异，不把root脏工具整份部署。

本次API安装承载用了临时systemd service默认KillMode，后置失败使service退出并连带终止其cgroup内已启动的JVM（2157405）；这是本任务发布执行配置错误，**不是应用代码回归或OOM**。现行健康守护已按原锁自动启动同一447 JAR，PID2163667/healthmon scope；没有重复构建/安装、改源码或取消恢复任务。不得将00:52初次UP冒充最终持续健康。以后API安装承载须明确保留被启应用生命周期（既有scope或受控RemainAfterExit/KillMode设置），不以默认临时service包裹派生生产JVM。本次额外停机如实保留。

后续只在守护释放现行发布锁后安装定向修复并核验已装447的后置schema，不重启API、不重建制品，不覆盖原失败回执。专项证据`release/schema-branch-repair/`；root广泛83项helper检查中73项通过、10项旧LOCAL fixture导入退役类失败，与已知旧suite问题相同；精确现行工具候选独立94项回归正在进行，首轮暂存候选漏执行位导致PermissionError，已修候选mode后重跑，不能把该首轮称为通过。

### 2026-11-03 01:53 CST 安装、核验与实际剩余项

- **安装完成**：API447/192a590b2c（JAR 3a4749fadecdf42e684572c6a01ef07969c2b3fe0b337bc5a6edecde4911491a）与Runtime120/125729f（1.3.36、bridge1.1.26）。API恢复后PID2163667、canonical cwd/JAR及health UP核验；Runtime01:34:41启动PID2177405，01:46—01:47三个连续新鲜样本中3个Agent均connected/registered/ready，689个payload文件/模式及版本核验。配置/身份保持，备份和固定来源保留。未新增模型/付费业务验收任务。
- Runtime停旧服务01:23:48，状态备份327秒、tar compare134秒，01:34:41启新服务；首次全ready观察在01:46。停机/冷启动耗时没有隐藏在Flow统计中。两个原有能力检查均耗约17分钟，实际未引入新门禁；不能称作低耗时检查。本机CPU竞争显著、available memory约4GiB，磁盘余5.2GiB。启动慢的进一步优化未在本次擅改能力/隔离合同。
- API后置schema故障已于01:24:06完成定向恢复：F06 plan/apply及E05只读plan均existing_equivalent，无新增表/数据修改，无E05功能激活。三个主机helper按已安装字节修复并readback；原失败回执、停机事件保留，单独`versioned-release-447-reconciliation.json`关联恢复，不重跑安装。现行安装候选94项回归通过。root仅本任务差异提交`8b01bbf0`，未整份提交他人CHECK/目录修改；暂存版本对应73项F06/E05主类和21项E05 deploy通过。暂存广泛85项suite有6项旧LOCAL fixture的15秒安装超时（79通过），保留真实失败，不称全量通过；不再次盲跑。
- 两个约一分钟自然窗口01:47:16—01:48:21、01:49:28—01:50:30：native发现SQL4/5次（旧00:31窗口46）；bootstrap12/12（旧71）；双lane集中补偿2/2；文件发现3/3（旧采样过滤器未含plain file SQL，前值未知）；未优化议事outbox59/59（旧71）。这是performance_schema digest计数，不是完整HTTP计数；Nginx不覆盖内网直连。符合事件发现+集中补偿，非全系统零扫描。
- CPU自然窗API18.5%/32.6%、Runtime20.1%/24.7%单核，旧29.3%/24.7%；负载未隔离、冷启动/宿主竞争存在，不声称CPU/GC/用户体验达标或因果百分比收益。证据`release/polling-observation.json`与两原始采样目录，当前Runtime记录只标CHANNEL_VERIFIED_PASSIVE_POLLING_OBSERVED_WITH_OPEN_FINDINGS。
- **未完成项明确保留**：ChatDeliberationOutboxRelay500ms扫描尚未事件化；岗位/归档等非native/file链路继续按真实合同审视。当前API日志证实`/internal/archive/v1/jobs`重复404，不把该协调器视为成功/必要请求；需要功能可用性协商或禁用未开启链路，不能据一次404永久吞掉有效任务。历史TYPED_INSPECTION_ENGINE_STATE_BINDING_CONFLICT在旧Runtime已存在；新窗口另有SKILL_API_RESPONSE_UNCONFIRMED与一条decoder AGENT_MESSAGE_INVALID（290字节，有wire摘要），尚未完整归因。不改状态强行成功、不自动重放UNKNOWN，不把连接ready冒充业务无错。对应`runtime-install/warning-comparison.json`与API日志窗口。
- 发布所需Flow/安装/通道/被动观察已完成，**整体轮询专项与真实业务无错验收未全部完成**。下一实现范围为议事relay及已证实archive无效发现；先沿现有生产者/恢复责任层核对，不全链重写。两干净任务worktree保留供该未完专项复用，未新增工作区；已结束的任务测试暂存目录收口，正式证据/制品/备份保留。

根仓同步边界（2026-11-03 01:57 CST查询）：fetch得到origin/develop `d000cb4356f11cf3e48b7ac7782b53d9a2bacb60`，与本地既有文档提交链分叉；主工作区另有大量其他Owner未提交修改。本轮root工具修复8b01bbf0和发布文档77a668f2保留本地，不在脏共享目录强行merge/rebase/force push。两组件固定源码早已集成；该根仓同步未完成不改变本次已核验安装来源，后续须在保留他人修改的条件下协调集成。
