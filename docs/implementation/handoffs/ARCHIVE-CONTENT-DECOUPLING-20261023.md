# ARCHIVE-CONTENT-DECOUPLING-20261023

Owner：本聊天主Agent。用户明确要求：书籍数据与代码解耦，持续新增书籍不再改代码。读取根AGENTS(2026-10-22更新)、api/web组件规则、ops/orchestration/README；接口规范固定 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2/2026-10-14。未调度子Agent。

## 固定范围与基线
- API worktree `/home/isp/wsps/worktrees/archive-decoupling-api-20261023`，branch codex/archive-decoupling-api-20261023，base远端develop实查 `683adf775fafce7ac0cc275cf0584543976149f8`。
- Web worktree `/home/isp/wsps/worktrees/archive-decoupling-web-20261023`，branch codex/archive-decoupling-web-20261023，base远端develop实查 `232a32ffe32d941a8e546db407fc85697b3b6c8c`。
- 原本机api94b4c8a5/web9dbd132及其他任务脏修改不触碰。上一轮2c6f894419仅局部未发布候选，不视为本轮基线或已上线。
- 非目标：生产数据迁移/导入/部署/重启、付费变配、删除个人阅读数据、破坏身份/ACL/幂等/事务/锁归属。源码DDL候选不代表执行迁移。

## 设计与验收
- 在线启动只做必要结构初始化/核验，不读取任何书籍资源、导入或全文逐段对账。
- 书籍资源移出生产classpath，既有整书仅保留为回归fixture。通用外部manifest加载器校验操作者固定的文件SHA、内部摘要、段落字节与结构计数；发布入口显式执行，不能跟随应用启动。
- 数据库 work/edition/blocks/paragraphs 继续为事实数据；READY版本不可原位修改。新增版本经原幂等导入、完整性复验与work→edition锁顺序原子切换。数据源信息来自manifest，不硬编码书名/来源/摘要/回数/段落。
- 去除固定120回与必需引首约束，支持任意正章节数、可选引首；旧库两项CHECK需明确一次性迁移，保留所有FK/唯一性/计数一致性，不自动改生产。
- 书架从数据库列已发布书籍；目录显式指定workId，正文仍editionId/blockId定位；完成阅读由该版本实际末段末字节判断。选文提问显式携带editionId并与选文版本/活动指针核对。
- 前端书架多书、可选引首、动态章数，切书隔离状态/异步回包，保留账户切换generation fencing。接口公共信封不另创。
- 回归至少包括两本合成书（不同章数/无引首）、启动零内容读取、外部manifest篡改失败、幂等/非READY隐藏、跨书选文拒绝、末段判断、前端多书与迟到响应隔离；复用既有archive JUnit/Mocha及Flow5260799/4403172。

状态：开发与云端验证完成，未部署；最终证据见末节。最早轻量反馈为静态常量/生产资源库存与前端定向检查；正式Java/构建在Flow。定位/实现/验证/等待耗时未知留空；60秒整体启动目标仍未验收。

## 2026-10-23 实现/自检接续

- API候选 `ad45628558`；Web候选 `2d14c9e`（完整SHA/tree随后补云端记录）。API生产资源已移至test，通用外部发布命令不注册Spring bean，在线启动只schema；原事务/幂等路径保留。
- 已补通用两书fixture（2章+序、121章无序）、跨书提问/最终段落测试；新增Flow自有MySQL实例测试，沿用`CYF_REVIEW_MYSQLD`模式，只控制本测试创建的Process，无外部JDBC回退。历史H02/H03/H05A外部fixture测试仍保留显式保护，未运行不冒充通过。
- 本机轻量反馈：Mocha阅读专项85/85，Python数据准备3/3，定向ESLint及git diff --check通过。Java尚未编译，本机不跑重型Gradle。
- 云端API默认CI原来不选择阅读器测试。2026-10-23T00:40Z无活动Run（最新236 SUCCESS）；备份真实云端配置，并仅在既有policy增加chat mapper/service `cn.jia.chat.archive.*` selectors，保留原所有测试/分层/bootJar。更新5260799成功且readback canonical SHA `70dabf4cd87f57e88fec5235c0c380485f25c62b47da90966ea202ce11d42a00`。模板同步离线渲染，保留共享根目录其他任务修改；无部署阶段。
- 源码操作指南在API `ops/archive/README.md`。数据库两个CHECK迁移是候选文件，未执行；不保证旧应用可直接回滚新schema。
- 后续补齐切书草稿按edition保存/恢复与失败切书不打开旧书；Web固定 `5cc78184fda6a0b72d2bbf80697bf0e6ce498417` / tree `6bab4db998c6127cf0e7d1a15f548625cb110d67`，本机86项阅读回归与定向ESLint通过。
- API固定 `ad4562855877b7590c64ab19c11a2a4f3a8ed8a7` / tree `0b692775f91b70b47b305605aee9e2ac1bbd601b`。两组件已正常fast-forward推送远端develop（未切换原工作区/覆盖其脏修改），实查无push自动Run后显式启动CI；默认配置无部署。
- 现有flow-control start对超过100条历史会要求reconciliation；这次先完整分页只读全部历史，固定最新候选/配置SHA/远端develop，再用技能SDK单次start（无盲重试，不修改控制工具）。证据`ci-5260799-start-context.json`/`...start-result.json`；API237运行中，日志确认CI_COMMIT_SHA等于候选。不是生产发布。

## 云端第一轮及修复归因

- Web298 SUCCESS，受测`5cc78184...`；完整测试/构建与代码扫描均成功，无部署。API237 FAIL，受测`ad456285...`，编译错误0；239个suite报告已解码保存`api237-diagnostics.json`。
- API失败13项归于3个已定位问题：H03 catalog中的`chk_archive_progress_single_tenant`与生产DDL实际`chk_archive_reader_progress_single_tenant`命名不一致（连带新真实库用例失败）；根profile精确列表测试缺少当前已有`/economy/**`；worker毒性scope测试仍把“另一个合法owner”当作越权，已与现有单租户/全认证用户开放策略不符。**不恢复旧allowlist/tenant=owner限制**，只将负例明确构造为非法client claim，并补合法不同owner可执行正例。
- 已修复catalog期待名，不改该项生产DDL；补齐profile现有URI快照；worker修订保留全部队列边界断言。同时`lockActiveEdition`先非锁读不可变parent，再work→edition精确主键锁定，避免多书时通过active指针全表锁范围；新增真实跨书并发不互锁回归。
- API修复候选`58aaa4dab29c091f8a59db1a5a51993d61cc3ffb` / tree `b814ff74731004b4c7bef16affc0024edb39e8c3`已正常推送develop。下一轮为变更输入后的验证，不是同根因同输入盲重试。
- Web298同Run制品已下载只读核验：发布metadata绑定`5cc78184...`，tree `6bab4db...`，Mocha3258 PASS/2 pending/0失败（release profile），Vite构建及扫描SUCCESS；613个dist文件SHA逐一匹配。tgz SHA `258b3c93b1abacfa0b769dc301684848cd6b89a885a11445b02089be6cb63d29`。完整mochawesome报告压缩保留证据目录，临时109MB下载包核验后已删除释放本机磁盘；未安装到生产。
- API238已启动，固定`58aaa4dab2...`；API237首轮失败已归因和变更输入，无取消他人Run。root模板轻量静态测试6/6通过。

## 最终核验（2026-10-23）

- 实现已集成组件develop；API `58aaa4dab29c091f8a59db1a5a51993d61cc3ffb` / tree `b814ff74731004b4c7bef16affc0024edb39e8c3`；Web `5cc78184fda6a0b72d2bbf80697bf0e6ce498417` / tree `6bab4db998c6127cf0e7d1a15f548625cb110d67`。两任务worktree干净，未覆盖原组件工作区、未更新共享根gitlink。
- API5260799/238 SUCCESS（2026-10-23T01:01:35Z只读确认）：3036次测试执行，2910通过、126跳过、0失败/错误（source set可能重叠，不冒充唯一测试数）；validateLayering与fresh生产JAR构建成功。新 `ArchiveMultiBookMySqlTest` 两项真实MySQL测试全部执行通过，覆盖多书导入/幂等、实际末段完成、owner隔离、跨书选文拒绝、跨书锁互不阻塞及旧CHECK显式迁移。历史环境依赖测试的skip未抹去。
- API同Run tgz 223709025字节，SHA256 `be1088773b93ae7bf3c3b3e942e8972e4758e84fa0cdaa78f24bc9211ef0e925`；JAR 251007294字节，SHA256 `40077623c0816830dbf7d87b58954c004ad021729e6b73083b47d0e04b7ee0dd`。下载实算摘要与metadata/receipt闭包、源码commit/tree全部匹配。逐一检查生产嵌套jia-chat JAR：无archive书籍资源或历史fixture/golden类，存在通用ArchiveContentCommand。
- 本次已验证JAR用PropertiesLauncher独立运行`validate`：由数据准备器生成的新书包成功；错误文件SHA退出1。没有启动Spring/Web、没有数据库发布。此结果补齐API ops/archive/README.md在受测提交时仍标注待验的候选CLI smoke；不使用历史安装包冒充。
- Web4403172/298 SUCCESS：3258通过、2 pending、0失败；构建/扫描成功，613个dist文件摘要全部匹配（详情见上一节）。
- 完整证据目录：`specs/archive-pavilion-reader-mvp/evidence/decoupling-20261023/`。API最终status、summary、metadata、receipt、artifact-verification与cli-smoke分别落盘；日志尾部有截断标记，测试结论来自同Run完整summary而非截断日志。临时下载包/JAR核验后删除释放空间，云端制品保留。
- 结论：新增书籍仅需外部数据准备、校验、显式数据库发布，不需Java/Vue改动或应用重启；这不是新增管理后台页面。内容修订用新edition，已发布正文不直接覆盖。正式上线前需授权执行一次性两项CHECK迁移并部署匹配前后端，再验收线上业务。**本任务未生产迁移、导入、部署或重启；60秒后端启动仍需独立冷/热启动实测。**
- 定位/实现/验证/等待耗时未完整测量，不填推测值；开发验证完成与上线等待分别记录。

## 2026-10-23 继续完成：上线前只读预检

- 用户追加“继续完成”。已继续核对固定候选、线上版本与现行发布入口；尚未把这句泛化为生产DDL或服务重启授权，下一步需一次性明确该生产操作范围，不新增逐阶段审批。
- 09:10–09:18 CST只读ls-remote：API develop仍为`58aaa4dab29c091f8a59db1a5a51993d61cc3ffb`，Web仍为`5cc78184fda6a0b72d2bbf80697bf0e6ce498417`，两任务worktree无未提交改动。
- 线上API安装记录仍为233/`7841057b057c012cfa203fb658c1043500be055e`，实际JAR SHA实算匹配`244f2b6e208bf9794cb5da2ce506903b40acc24aa8483dece30e293c154f5e03`；Web安装记录295/`669bdc9d6439d1bd7eb71df5ed401202a648f419`，尚非解耦版本。后端loopback10018 health/readiness结果保存于`rollout-preflight-production.json`，未启动/停止服务。
- 复用现有startup_timing.py解析上一次生产启动：2026-10-22的Spring Started306.888秒，日志原文进程运行315.851秒；这是旧线上包的历史启动，不是当前候选成绩，Started也不等于Runner/readiness完成。结构化证据`rollout-preflight-existing-startup.json`；已有StartupTimeline和生产helper的CYF_API_STARTUP_DIAGNOSTICS入口可在获授权发布时复用，无需新增观测框架。
- 已核对现行同Run部署适配器；API238/Web298仅为CI，不能直接冒充已授权部署Run。正式上线须固定发布版本与源码，保存现行默认CI配置，保留本次完整测试并使用同Run制品部署，完毕后仅在配置仍属本任务且无活动Run时恢复默认CI。禁止本机直发/绕锁。
- 生产操作待明确：备份archive_edition/archive_chapter表结构及恢复所需数据，执行两项CHECK显式迁移，Flow部署匹配前后端并重启API，核验启动全路径与真实readiness。DDL为隐式提交，应用回退须同时核对schema，不能无条件自动恢复旧约束。迁移未执行，未读取生产正文或用户笔记，未调整收费资源。

## 2026-10-23 生产执行授权

- 用户明确回复“允许”，授权前文所述生产约束迁移、Flow前后端发布与API重启及启动验收；先备份并保留恢复方案。不授权内容导入/个人数据修改、收费变配或操作其他任务。
- 本轮私有控制目录`/var/tmp/archive-rollout-20261023`；证据延续原目录。上一节09:10–09:18为人工估计时间范围，不作为准确时间证据；以JSON queriedAt和本轮命令实际UTC时间为准。

## 2026-10-23 09:29 CST 执行异常与恢复边界

- Web发布升版提交`203e00c7f8d9bb9c3f494349350e24419e0901cc` / tree `25d05af949b8b0636398041d5520d18a7927f38a`已推送develop（只改package/lock版本1.16.44）。API本轮仍固定`58aaa4dab2...`，发布标识计划1.16.30。新Web提交尚未云测，不冒充先前298受测源码。
- 已读取现行Flow配置且全历史确认无活动Run，备份`/var/tmp/archive-rollout-20261023/{5260799,4403172,5264702}-before.yaml`；基于真实默认CI准备同Run显式部署候选，保留所有测试/缓存策略。Web保留线上三个VITE功能开关true；API启用既有CYF_API_STARTUP_DIAGNOSTICS=1。YAML/js-yaml与shell语法验证PASS、canonical路径8项PASS；尚未写Flow配置/启动发布。
- 用户授权后已通过本机MySQL socket进行两项CHECK迁移（不是本机构建/部署）。取得coordinator→release→lifecycle非阻塞锁及专用DB锁，完成root0700备份`/home/isp/baks/archive-content-decoupling-20261023`（表结构、archive_work/edition/chapter数据dump、原CHECK恢复SQL、摘要与每步记录）。2个work、2个edition、242个chapter，正文和个人数据未修改。
- 第一条ALTER完成后，严格SHOW CREATE比对发现MySQL8.0.21将既有`chk_archive_edition_state`中的STAGING/READY字面量字符集从_utf8mb4重写为_ascii（列本身为ascii）；核验暂停，**不是整个事务回滚**。实际只有edition新CHECK生效，chapter旧CHECK尚保留；所有三表行数和数据SHA不变。原文件`migrate.py`不再执行，不能盲重跑。
- 已准备`complete-migration.py`，只允许上述两个ASCII字面量规范化、保留其他DDL/FK/索引精确比较；恢复第二项前核对原备份摘要、实库partial snapshot及第一项精确新谓词。首次纯校验误取DROP CHECK而不是ADD的CHECK子句，已改rindex并用无副作用纯函数自检通过；未执行第二条DDL。随后执行被真实生命周期锁冲突阻止，未抢锁。
- **实际生产故障**：旧API719501发生`OutOfMemoryError: Metaspace`，上限192m，已有SpringApplicationShutdownHook也OOM。系统health monitor于09:23左右对同一个旧PID进入自动restart，TERM后进程未退出，原规范canonical仅等待退出、无强杀。该恢复进程持有现行发布/生命周期锁；不是本任务部署，也没有取消/kill它。
- 按现行ops/health/README维护流程，以O_EXCL创建本任务root0600`/home/isp/state/cyf-juyiting-health/maintenance`，只抑制后续自动恢复，不取消在途恢复。**完成恢复验收后须删除本任务marker（使用--resume且monitor锁可得）；不能遗留暂停。** 未修改monitor state/预算/签名工具。
- 证据`rollout-blocked-recovery.json`、`rollout-migration-partial-inspection.json`；控制目录完整保留。现阶段尚未触发任何发布，health/readiness无法提供服务，不能宣称解耦已上线或60秒达标。
- 下一动作：向用户明确请求允许强制结束已OOM且正常TERM退出失败的旧API719501（保留精确PID/starttime/cwd/JAR/UID核验，不取消monitor或抢锁）。获允许后让既有恢复流程自行终结/释放锁，再执行已校验的仅第二项迁移恢复，按start-release.cjs先API再Web串行发布（无Flow内部配对等待），完成实际启动/业务验证并恢复默认CI与monitor维护状态。如需修改Metaspace上限，须基于本次OOM证据沿用受控helper更新及信任摘要链，不临时覆盖签名工具或启用收费变配。

## 2026-10-23 09:51 CST 接续：保留Metaspace上限并定位

- 用户明确要求不移除Metaspace上限、查明增长原因。取消上限候选已撤回，相关本任务源码/candidate修改已还原；生产canonical SHA仍为`878e2f91f2a557f2c10ca954c438b090cc370d90e99da851053e0190bc04be56`，`MaxMetaspaceSize=192m`保留。禁止执行旧uncapping staging。临时ops5264702/24失败后wrapper已恢复原helper，ops配置恢复APPLIED；不是内存问题已修复。
- 获强停授权时719501已自行退出，未发送kill。monitor启动的旧包1170261于09:39:59输出Started474.849s/process493.968s，随后因旧schema catalog拒绝新CHECK退出；不能以Started宣称服务恢复。维护marker仍属本任务，恢复健康后必须按既有--resume恢复monitor。
- 迁移已于01:41:14Z完成，`migration-result.json`为applied_verified/dataUnchanged=true；三表数据摘要不变，两项CHECK均核验。禁止重跑迁移。备份仍在`/home/isp/baks/archive-content-decoupling-20261023`。
- API显式发布单次start返回239，初始控制器UNKNOWN；01:48:53Z只读确认Run239 RUNNING、构建541383796 RUNNING、部署541383797 INIT，不重复start。候选仍58aaa4d，版本1.16.30，192m cap，启用既有启动诊断。Web尚未发布。
- 新查旧进程GC日志1931条Metaspace样本：约10分钟158.9MiB、1小时179.8MiB、2小时182.4MiB、8小时186.7MiB、14.75小时188.4MiB；首次OOM于09:13:39，实际used约189.66MiB、committed192MiB。并非仅凭日志可断言无限泄漏；需要新进程ClassLoader/类数量增量。第一处OOM栈在微信回调XStream XML解析，后续Lambda失败不能直接认作原因。证据`/var/tmp/archive-rollout-20261023/old-metaspace-gc-analysis.json`。
- 对固定候选生产Java源码定向搜索未发现直接GroovyClassLoader/URLClassLoader/ByteBuddy/ClassPool/JavaCompiler/Enhancer等构造；第三方库动态加载仍未排除，不据此声称无泄漏。待新进程采集VM.classloader_stats/VM.metaspace及重复同路径前后类数量，避免heap dump及强制GC。

### 09:58 CST 发布脚本顺序修正

- API239最终FAIL：构建成功，3036执行/126跳过/0失败错误；部署单71651722在任何安装/移动制品之前被本任务插入的canonical-path测试拦截。准确错误为test_current_process_executes_canonical_jar读取不存在的pid文件；旧进程已退出，故将该只读完整8项检查移至规范deploy完成后，不删测试、不改helper、不绕锁。
- 修正后Run240已单次启动，01:57:25Z只读为RUNNING；仍同一API58aaa4d/source tree，保留全部Flow测试与same-Run制品。控制目录`/var/tmp/archive-rollout-20261023/api-recovery-v2`，完成后用其restore-ci.cjs恢复原默认配置（不是外层239的restore脚本）。首个CONFIG_CHANGED_NO_WRITE仅严格文本/canonical格式不一致，无写入；修正为对比239实际readback canonical SHA后才更新。
- Run239本任务下载包已提取summary并计算SHA留档，失败Run终态后删除本地临时副本以释放213MiB；未删云端制品/其他任务数据/备份。仍有磁盘空间压力，不执行重复下载或heap dump。
- 旧启动前316秒GC暂停合计14.513秒/124次，因此现有证据不足以把约316秒启动全部归因于GC；继续区分类加载、容器装配和资源竞争。

### 10:18 CST Run240启动失败与精确恢复

- Run240构建成功，实际新JAR进程1185868/日志`startlog_20261023_100304.6hLv2h.log`。实际argv仍MaxMetaspaceSize=192m。Spring Started281.908s/process292.017s，但随后reader-data schema校验失败；cyf.application.run295.929s/outcome=failed，退出Metaspace157790KiB/committed160000KiB，**本次失败不是OOM，不是健康上线**。
- 根因：生产实际进度表租户CHECK名是`chk_archive_progress_single_tenant`，而58aaa为修复新建库DDL测试把catalog改成`chk_archive_reader_progress_single_tenant`。先前把源码DDL称为“生产DDL”不准确。现在只读查询真实information_schema并保留`reader-checks-readonly.json`；修正DDL+catalog统一为生产实际名称，保留tenant_id='0'/ENFORCED，新增错误重命名拒绝测试，不修改个人数据或增加生产DDL。
- 新API源码`3a23cfa27cf1ce6921f3192cf890c56cc3d92447` / tree `c3eb5acbed457b3a7a539ce4cf3942e99841ac1f`已推送develop；3文件，尚无新源码Flow验证。其余源码不变。
- 为避免再次到完整启动才发现契约差异，本机轻量probe仅javac编译7个既有schema类和一个临时适配器（96m/64m），使用现有JAR约8MB依赖；Python仅采集18条原源码information_schema SELECT，Java调用原inspect/catalog validate，**不启动Spring、不调用initialize/DDL、不跑Gradle或生产打包**。当时新counts schema与修复reader-data均PASS。question表不存在且生产profile明确archive.question.enabled=false，标注SKIPPED而不是通过。证据`/var/tmp/archive-rollout-20261023/schema-probe`，不是正式Flow验收。
- Run240安装器自动恢复旧233 JAR，但其不接受已迁移counts CHECK，旧进程也退出；record真实状态rolling_back/old_start_failed。不能改record伪造健康、不能让新Run接管未完成事务。
- 按原备份恢复方案，仅将原两项CHECK恢复：先锁coordinator→release→lifecycle及DB锁、核验两本书/版本/章数据摘要与初始备份完全一致、逐旧谓词SELECT验证0无效行，再执行备份原SQL并回读旧谓词。`restore-original-checks-result.json`为original_checks_restored_verified/dataUnchanged=true，未恢复dump、未改reader个人数据、未改发布record。
- 为完成原240事务而非重发失败候选，已单次retry原部署job541391038，API回执success=true；同Run同制品/approval，通过原安装器rolling_back分支只恢复旧服务。由于schema输入已恢复，这是有修复输入的恢复，不是盲重试。原migration-result当前status标注original_checks_restored_for_run240_recovery（历史applied副本另存）。待旧服务健康、record终态failed/restored_healthy后，才可重做已授权两CHECK迁移并发布新源码；不抢锁、不新建流水线。
- 新进程启动诊断：早期加载11321类/Metaspace57.5MiB；稍后104个ClassLoader、23517类，主LaunchedClassLoader17656类占99.5MB块；仅启动样本不能证明泄漏。完整span中config-classes.parse独占43.065s，多个schema/Bean装配仍有秒级成本。GC不是全部启动耗时；60s仍未达到。

### 2026-10-23 接续：启动 schema 解耦范围固定

- Owner仍为本任务；API worktree `/home/isp/wsps/worktrees/archive-decoupling-api-20261023`，branch `codex/archive-decoupling-api-20261023`，base `3a23cfa27cf1ce6921f3192cf890c56cc3d92447` / tree `c3eb5acbed457b3a7a539ce4cf3942e99841ac1f`；本轮只读ls-remote确认develop相同。接口规范保持v1.2，无wire改动。
- 用户明确要求从正常启动移除schema initializer。范围：42个initializer的组件/Bean注册、archive启动调用、typed deliberation运行时就绪依赖；保留完整校验和迁移实现用于显式维护，普通启动不执行DDL、数据修复或全量information_schema扫描。必要版本查询独立于维护器。非目标：执行全模块生产迁移、移除192m Metaspace上限、宣称60s已达成。
- 验收先做轻量源码/配置审计，增加Spring容器隔离回归与版本探针失败关闭测试；正式编译/回归/分层由Flow固定源码执行，不在本机重构建。
- Run240精确恢复已完成：record failed/rollback_recovery/restored_healthy；旧服务1196608恢复后，仅原授权两项CHECK已再次应用且数据摘要未变（`reapply-checks-result.json`）。勿重跑恢复/迁移脚本。
- API241（3a23）FAIL在测试构建阶段，未安装：唯一报告失败为ArchiveReaderDataSchemaResourceTest仍按表名拼接旧CHECK名称；新增生产名称修复遗漏此资源测试，须保留断言强度并修正映射。证据`/var/tmp/archive-rollout-20261023/api241-diagnostics.json`。v3默认CI已恢复APPLIED。
- 本轮本机health实际UP，仍是旧包而不是241上线；本任务维护marker经所有权核验后使用health工具--resume恢复（maintenance_resumed）。旧包与新CHECK的重启不兼容风险仍在，未主动重启。Web尚未发布。

### 启动schema隔离实现候选 / Flow验证中

- API提交 `4a6c6da8c9b7bea6c3bf23aa88c1ace98950b6cf`，tree `3ed16826c80f2300f0e85865ff6bb3fd625ac0c1`，已推送任务分支及develop（普通git push，无覆盖他人变更）。70文件：42个维护器+27个@Bean入口显式schema-maintenance隔离；archive worker启动不再调用schema；typed readiness抽出接口与只读版本探针；Camunda自动schema升级关闭。
- 保留全部维护器原始DDL/约束检查、锁和直接调用入口，不修改任何生产表。显式维护profile不是整个应用的批量迁移命令；只在授权的隔离上下文使用。必要版本3标记查询不能证明后续全部增量DDL已验收，部署覆盖仍需逐模块核实。
- 本机静态审计42类/27工厂通过、git diff --check通过；新增Spring注册隔离测试、版本探针5项场景及Camunda防自动DDL测试，相关安装测试显式opt-in。修复241遗留资源测试的生产CHECK名称映射（保留租户谓词断言）。未运行本机Gradle。
- 本次5260799配置为**CI-only且无自动触发**，保留原完整测试/分层/fresh JAR，并补agent schema、economy config、wx schema、新probe及starter隔离测试。固定commit/tree guards。控制与恢复目录 `/var/tmp/archive-rollout-20261023/schema-startup-ci`；Run结束后只能在配置仍本任务且无活动Run时执行该目录restore-ci.cjs api。本轮不含部署阶段，不能拿构建成功当上线。

### CI242失败归因与修复候选

- 5260799/242固定4a6c6da，FAIL，61份已产出JUnit报告无编译诊断；未完成全套，不当作验收。唯一报告失败是新增覆盖到的WxDailyVoteSchemaInitializerTest把合法外键`ON DELETE CASCADE`误当DELETE语句。原SQL和运行时迁移行为未改。
- 修复提交 `c48d9b0bb1dd8c2808b62992dc8fe5d8c5cecefc` / tree `6dc433989484c9e79d42526fef6712ffa4922d3f`：仅测试，精确剔除既有具名FK的完整批准子句后仍拒绝DELETE，增加直接DELETE、FK后夹带DELETE、外表FK等变异断言，同时将两个建表名称检查收紧为startsWith。不是移除回归或放宽任意SQL。
- 242配置恢复APPLIED后，新输入CI-only Run243已单次启动，控制返回UNKNOWN/returnedRunId=243，须只读协调不重启。控制目录改为`/var/tmp/archive-rollout-20261023/schema-startup-ci-v2`；结束用该目录restore-ci.cjs api。两轮都无部署阶段。

### CI243维护夹具修正

- 243固定c48d9b，FAIL：267份JUnit报告，无编译诊断；新版只读probe 5/5、agent命令开关21/21、WX修复3/3及archive reader校验均通过。SchemaStartupIsolationTest的默认隔离/Camunda两项通过，唯一失败是维护夹具错误地将Spring对JdbcTemplate自身的afterPropertiesSet调用也认作数据库访问。
- 修正提交 `b33b0d29f18a3011c3ec9b9a1b564a164ff1ef1c` / tree `8f2b8b21eaf1621f7c9602988dcf63d7977487d6`：仅断言先verify JdbcTemplate.afterPropertiesSet，再verifyNoMoreInteractions；仍严格禁止SQL/DDL调用。原schema实现未改。
- 243默认CI已恢复APPLIED，新候选控制目录`/var/tmp/archive-rollout-20261023/schema-startup-ci-v3`，只构建/测试，不部署；后续只用该目录restore-ci.cjs api恢复。源报告SHA已由CYF_DIAGNOSTIC_SUMMARY校验，不以已过部分冒充全套验收。
- 最新只读线上health UP，canonical helper SHA仍`878e2f91f2a557f2c10ca954c438b090cc370d90e99da851053e0190bc04be56`，本任务没有更改Metaspace 192m上限，monitor维护marker已撤除。仍是旧包健康，不是本候选上线。

### CI244专项维护回归适配 / 最终候选245

- 244固定b33b0d，FAIL：3187次测试执行、4失败、0错误、180跳过，384份报告。新增普通容器隔离/Camunda 3/3、版本probe 5/5、economy配置5/5、WX 3/3均通过；4失败仅在原ChatSchemaReadinessLifecycleTest仍以普通profile要求自动维护，属于本次行为变更必须更新的维护夹具。
- 修复提交 `b0735f57a7b454fa7a6fb9886fa3914131986779` / tree `63dd9ee15cf074b796fa6af385d31887d85d26e7`：原专项测试显式setAdditionalProfiles(schema-maintenance)，保留全部9项约束/顺序/失败关闭断言，将正向测试命名明确为显式维护上下文。正常启动不恢复任何schema调用。
- 244默认CI恢复APPLIED；245在03:18:28Z单次启动，初始UNKNOWN/returnedRunId=245。最终控制目录 `/var/tmp/archive-rollout-20261023/schema-startup-ci-v4`，仅CI、固定精确源码、全部原回归+新增范围；结束恢复命令为 `node /var/tmp/archive-rollout-20261023/schema-startup-ci-v4/restore-ci.cjs api`。未进行生产安装/重启/新DDL，60秒尚无新实测。

### 2026-10-23 11:27 CST 收口：启动schema解耦源码与CI完成，未发布

- **5260799/245 SUCCESS**，精确源码`b0735f57a7b454fa7a6fb9886fa3914131986779` / tree `63dd9ee15cf074b796fa6af385d31887d85d26e7`，任务分支及develop已推送，API任务worktree干净。
- 3330次测试执行：3119通过、211显式跳过、0失败、0错误（source set可能重叠，不是唯一用例数）；本次三项关键套件均无跳过：普通容器隔离/显式维护注册/Camunda共3项、只读版本probe 5项、显式维护生命周期9项。既有回归、分层和fresh JAR同Run完成。
- 日志API窗口仍有头部截断，未声称全文日志齐全；本次完整诊断payload按Flow发出的SHA验证，再聚合测试结果。Flow报告JAR SHA=`c10379436ba7ce61e43b380c566af8dcc90f780f1ba9248bda3afdd3f04ded48`，receipt SHA=`77557f779c979847e960a79db55f0133ca329b765267a86457f052f632a3c299`；本次没有下载安装制品，不把这些摘要当作线上文件证明。
- v4恢复默认CI为APPLIED，所有本轮CI-only Run均已结束；没有遗留Run内等待，没有更改生产安装器/生产DDL/Metaspace上限，没有暂停monitor。
- 稳定入口：API同提交`ops/schema/README.md`，archive原发布指南已移除“在线启动初始化schema”的旧说明。汇总证据`specs/archive-pavilion-reader-mvp/evidence/decoupling-20261023/schema-startup-flow245.json`；完整控制/诊断仍在`/var/tmp/archive-rollout-20261023/schema-startup-ci-v4`。
- **范围状态**：本次“从正常启动移除schema维护”实现及CI完成；原典籍API/Web版本发布、线上启动60秒目标、Metaspace持续增长根因都未因此标记完成。当前生产仍旧包，本候选未安装/重启，性能没有新实测。下一步须固定已授权发布版本/源码与同Run制品，经Flow发布后再验收启动耗时和业务；不能将本次CI制品直接冒充未来发布Run输入。
- 本轮定位/实现/验证/等待未完整单独计时，留空；Run和查询时间见证据，不虚构提效比例。

### 2026-10-23 用户授权部署并验证 / Run246

- 用户明确授权部署与线上验证。本轮仅发布后端正常启动schema解耦候选，固定`b0735f57a7b454fa7a6fb9886fa3914131986779` / tree `63dd9ee15cf074b796fa6af385d31887d85d26e7`，版本1.16.30；不追加DDL、不发布Web、不取消Metaspace192m上限。
- 03:32–03:34Z只读确认远端develop精确匹配、任务worktree干净；旧PID1196608健康、旧JAR摘要仍为244f2b6e…；Run240恢复记录failed/rollback_recovery/restored_healthy。三个生产helper摘要匹配既有固定值。
- 复用245完整CI与v3修正安装阶段构造新同Run发布配置，语法检查通过；保存默认配置且全历史无活动Run后更新APPLIED，单次启动246，当前RUNNING。控制目录`/var/tmp/archive-rollout-20261023/schema-startup-release`。不复用245制品。
- 保留startup diagnostics、forward-only（旧包与已迁移CHECK不兼容）、身份/摘要/锁/备份；canonical进程路径验证位于安装后，不要求安装前旧进程存活。失败保留候选，不盲重启旧包。
- 本任务03:33:57Z经标准health工具暂停自动恢复，marker此前不存在；发布结束核对所有权后resume。恢复默认CI仅使用本目录restore-ci.cjs并确认无活动Run/配置未被别人改动。

### 2026-10-23 11:47 CST 发布收口：Run246已上线，60秒未达标

- **5260799/246 SUCCESS**，固定b0735f57 / tree63dd9ee1，版本1.16.30，部署单71663006单批单机Success。完整诊断payload摘要核验后聚合3330次执行：3119通过、211跳过、0失败/错误，397套件；本轮同Run新制品安装，不借用245回执。JAR字节与245相同是可重现输出，不等于复用旧Run制品：246独立receipt=`048274b4b9ab6e3b47f791c431127c872597159edb0f6a54e0d214a5b67d9944`。
- 安装文件实算SHA=`c10379436ba7ce61e43b380c566af8dcc90f780f1ba9248bda3afdd3f04ded48`，归档SHA=`73189cae74ba7a66f0765637814af005c9c16747200e527394a7255b6da5895c`，record installed/not_required，versioned-release-246 verified。实际PID1255715、cwd及-jar均canonical实体路径，身份cyf-api；prod profile，**MaxMetaspaceSize=192m保持**。安装后路径合同8项通过，无安装前进程存活门禁。
- 健康/readiness均HTTP200/UP；works/catalog匿名请求401空体，认证边界保持。无现成授权登录会话，**未验证登录后的目录/正文/个人数据业务**；Web本轮未发布，不声明完整阅读端到端验收。
- 完整启动trace1537步、0未闭合/输出失败：未创建SchemaInitializer、ArchiveBootstrap、ChatSchemaReadiness；只读版本probe有注册。安装器既有F06钩子报告两表existing_equivalent，无新增schema对象；E05未准入、未调用runner。此结果不等于全模块DDL完整认证，不因去除启动检查作此承诺。
- 实测：Spring Started134.938秒、当时进程139.836秒；application.run完整成功136.063秒；JVM spawn到application.run返回140.961秒，**spawn到安装器首次确认健康144.850秒，60秒未达标**。安装器健康轮询时刻不是服务首次就绪的精确瞬间。单次开启诊断的启动，不是多次冷/热基准；不以旧失败启动或不同缓存样本推导严格提速比例。
- 剩余独占wall热点：配置类解析19.830秒，mpInfoServiceImpl5.077秒，redisson4.872秒，jwkSource3.828秒；启动前GC暂停合计7.130秒（包含在总耗时内，不叠加）。下一步定向研究配置扫描与上述Bean初始化，不恢复schema维护、不取消内存上限。11:46:53 GC样本Metaspace约159MiB（162813KiB），只是启动后样本，**长期增长根因仍未查明**。
- 默认CI恢复APPLIED，本任务maintenance marker摘要核对后经标准--resume撤除，自动健康监控已恢复。未修改生产helper。旧备份恢复仍需匹配schema，不能无条件重启旧233包。
- 发布汇总：`specs/archive-pavilion-reader-mvp/evidence/decoupling-20261023/schema-startup-flow246-release.json`；完整控制/安装/线上/trace证据`/var/tmp/archive-rollout-20261023/schema-startup-release`。源码完成、发布完成、60秒目标未完成、内存问题未完成分别记录。
