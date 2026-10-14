# SELFHOST-ONBOARDING-20261012 自家接应补全

任务状态以 TASKS.yaml 为准。Main负责isp-install与集成；Faraday负责API；Hopper负责Web。范围、源码和验收以 specs/runtime-self-host-onboarding/ 为准，三个独立组件工作区均develop、开工干净。父仓无关脏文件不覆盖。

- 交接入口：AGENTS.md、ops/orchestration/README.md、冻结design已给两位Owner。API Owner已明确读完并发现旧Scope限制；Web待确认。
- API Scope原有限制tenant0不在本轮放宽，避免把文书修复扩成权限重构。
- Main最早验证：node --test /home/isp/wsps/chcbz/isp-install/tests/cyf-runtime-enrollment-prepare.test.mjs，7项通过；覆盖真实manifest摘要/登记摘要格式、非默认scope、私密文件权限、不覆盖、symlink、CLI不泄漏。工作区诊断，未登记正式accepted证据。
- 当前磁盘仅78MiB，正式Gradle/构建不得冒险启动；没有清理他人文件或旧制品。阶段通知不停止源码落实。
- 本任务不执行真实installation登记、付费调用、服务停止或发布。

## 自然接续 2026-10-12
- isp-install e3d7b30aeba7b9b36f49bf6372956d78254a3ca2 / tree86b19e3d7871d47b66e5c63fda3f7c2ce225952d 已推远端develop并ls-remote核实。8项离线测试通过，新增第8项从完整指南提取实际profile/host生成片段并交真实Runtime readers校验；无网络/enroll/服务操作。证据 evidence/selfhost-onboarding-20261012/installer-tests.log。
- API原Owner在Scope冲突裁定后继续，完成da4d4bf与9eb150d两提交；修正local不再虚构旧安装目录。Gradle因实际磁盘容量未运行，不能标accepted。
- Web第一版ba97098有2项定向失败，已回原Owner修复（不新增Reviewer）。Main发现真实useHttp双层JsonResult与测试mock不符、文件读取跨scope回包防护不足，已给原Owner同slice补齐，不以假mock通过代替真实契约。
- 磁盘一度降至1.3MiB后自行恢复约70MiB，本任务未清理其他进程/文件；主机容量不足仍阻塞大型验证/制品构建。

## 最终自然接续点（源码完成，正式验证待办）
- API最终0fe830d1ea/tree b365003e，已推develop；将原有Provisioning测试纳入既有managedHostingRegression，不新建验证框架。原Owner工作已交付，无后台开发等待。
- Web最终3d0e9ef/tree f0ca2607，已推develop。原Owner完成真实JsonResult/身份与文件异步防护、shell quoting、可移植fixture，Main补匹配查询后禁重复create及复制失败反馈。133项定向诊断PASS/exit0，证据见source-status.json和web-targeted-tests.log。正式Flow尚未跑。
- 本任务实际未修改生产配置、数据库、安装登记、服务或版本；新UI尚未上线。目标机可取isp-install develop新工具/指南，不需要为仅新增仓内prepare工具重复构建既有1.0.3制品。
- 真实阻塞：主机根盘约59MiB空闲；正式API Gradle与制品构建未运行，不以低成本源码/前端测试替代。下一步在明确归属和恢复要求下处理磁盘容量，然后由Main经现有编排器运行managedHostingRegression + validateLayering；前端Flow4403172验证候选；版本发布须另行实际执行，不自动发生产。
- 初次Main测试未带项目常用--exit，132个测试已完成但留事件句柄；精确停止本任务PID后，修正最终源码并以--exit完整重跑133项退出0。没有按耗时强杀生产/其他任务。
- optional技能quick_validate缺宿主PyYAML而未执行，未装新依赖、未冒称该校验通过；产品prepare工具的8项测试真实通过。

## 用户授权统一更新与版本发布（2026-10-12 22:53）
- Main Owner selfhost-unify-main（聊天01a13076-049a-75f2-a84f-7d53194ffe9e），继续原任务；用户“那就都更新”授权在上一回复明确范围内同步isp-install与自家接应、完成正式验证和版本化发布。不新增生产角色/installation、不付费调用，不扩大为旧协议队列迁移或远端机器批量升级。
- 本轮起点：API本地/远端develop 0fe830d1ea39b89de89475ef2d1f21dfc7577da2/tree b365003e141101350af123185b2bf2ec0e80ec16；Web 3d0e9effc76f6035e0a1de37373873cb14882de3/tree f0ca26079d76c46a6e046aed7bfa101e8c43e756；isp-install 5d2d3f8bec903a87eed684936efc3f3d21e891e2/tree2351f07341d1fec59d070aa7d9860f7fbb9fdc0c。2026-10-12 22:48–22:51实际ls-remote核对一致，三个组件tracked干净，根无关脏区保留。
- 线上只读记录：API1.14.10/cd1e6d6e、本地批次cyf-likui-progress-api-20261012-lrxcyfv2；Web1.14.10/235048e6/Flow4403172 Run205。Flow查询205成功，无新在途Run；查询不是新发布。Runtime本机仍1.0.2原制品，本轮安装器/接入文书更新不自动升级各目标机器Runtime。
- 安装/目录增量：默认程序apps、配置conf、状态state/<instance>/agents/<subject>/codex-home；既有Runtime目录收口不重复登记，需完整HOME+SQLite路径索引+policy/catalog+历史数据保留；不自动迁移/重放旧协议队列，内嵌执行库不改名。
- Main负责isp-install和Web；API子任务Noether（01a1309a-9708-7933-b790-4d19b7a56282）负责精确API正式构建/打包与安装准备，已显式交付最新AGENTS、工具README、原handoff和固定源码；待其确认已读。未建独立Reviewer。API子任务记录在SELFHOST-ONBOARDING-20261012-API-RELEASE.md，Main决定并执行真正安装。
- 目标Web/API版本1.14.11，各自固定源码和同批制品；不沿用历史Run/授权证明。本轮Frontend走Flow4403172，Backend本地；前端不得本机生产打包。容量当前根约893MiB、tmpfs约1.7GiB，复用既有输出路径并评估实际需求，不删旧备份/他人任务。

### 23:10 自然接续
- isp-install `a39c0856b0d68ae931b592420e283255668eca45`已push并ls-remote核对；README/AGENTS/安装入口提示/Skill/指南统一目录与升级边界，真实指南片段和安装入口19项测试PASS，Bash语法PASS。证据 `/var/tmp/cyf-selfhost-release-20261012/installer-tests-final.log`。
- Web `aad2ae915ec8315091ab916d5d53fbd3bac00905` / tree `60fa60e85dfdcc6f4b4bdf3febbf4756324fc836` 已push并ls-remote核对，版本1.14.11。仅提交本任务4文件，未stage其他聊天新增的JuyiHall/bounty/typed-deliberation文件。115项相关本机测试PASS仅为低成本诊断；正式Flow另记。
- Noether已在API独立handoff明确确认读过规则；API固定0fe830d1ea，正式本地验证进行中，不是已发布。
- Flow备份/候选/更新readback在 `/var/tmp/cyf-selfhost-release-20261012/`；23:09确认无活动Run后单次update已APPLIED。原配置CI-only且无push trigger；候选显式commit/tree/version，保留完整测试、构建flag和同Run安装。控制工具start不支持200条分页历史，复用已验收的paginated `start-verified.cjs`，先固定当前全部Run/远端/配置再单次start，未知响应不重发。
- 主机部署helper源码存在其他任务未提交的路径迁移。未覆盖；本轮使用root仓HEAD已提交Web helper与installed完全相同摘要 `fba8d49564946f381a02b7aee0bdfaeab48091be7ca5eb871f7dc4ac2eeeff6b`，现行绑定挂载仍是实际部署入口，不将未提交默认路径当作现行迁移完成。首次候选准备因dirty-source不匹配而停止，未写云端；改为已核验固定HEAD字节后成功。

### 23:30 正式验证、异常恢复与安装
- Web **1.14.11 / Flow4403172 Run206 SUCCESS**，2932 passing、2 pending、0 failing，扫描/正式生产构建/同Run部署均成功；commit/tree与固定候选一致。归档SHA `58e6b7ba41f2be5c48e3d0bc23cc3a37e14eddaaef61074ed57917073a589d40`，364份安装文件逐字节匹配，11份公网入口/引用JS/CSS匹配。23:18原CI-only配置已恢复并readback，未留下自动部署。详细证据 `online-verification.json` / `run206-status-final.json` / `run206-build-log-full.json` / `restore-result.json`。
- API首轮175项有1项Runtime fixture环境跳过，未用于发布；R2补固定Runtime fixture后175项全过，原分层/依赖完整性/fresh bootJar完整执行。无源码重改，确切批次 `cyf-selfhost-onboarding-api-20261012-r2`，API子handoff给出所有摘要/原始路径。Main已完成新的protected controller证明、原admission、完整published verification和实际授权绑定。
- 容量实际波动：23:19约480MiB不足，23:20后恢复约2.5GiB，足够原安装器测得约944.30MiB新增峰值＋元数据；本任务未清理任何历史备份或他人文件，未删除本任务制品副本，未新设人为阈值。
- **运行异常**：23:23新鲜PID快照失败，发现现行API已停止；kernel journal证明 **23:08:35主机OOM杀死现行API PID2690144**（同时杀死Chromium），不是本次installer停服。OOM发生于并发工作/构建打包时间段，未独立归因单一进程，不掩盖为正常发布。Main在可用内存恢复后通过原canonical生命周期 `start` 恢复原1.14.10同JAR；PID3156194，72秒ready/healthUP。日志 `api-oom-recovery.log` 与 `kernel-oom-evidence.log`。Runtime service PID3127402/NRestarts0未变。
- 恢复后重新采集本批fresh runtime/identity/inflight和F06/E05只读快照；18条只读投影exit0，catalog全部existing_equivalent。Main新决策 `/var/lib/cyf-api-flow/local-inputs/selfhost-1.14.11-20261012/install-decision.json` SHA `ba13a432b49f059fde9776dc6f42fbda807eb7a022efa331be21fdf27a499b46`；原local-inspect退出0，local-install已开始，尚未把开始视为上线。

### 23:38 完成
- API原安装器exit0 / summary verified，**1.14.11**，JAR SHA `abb79efc46b19a0d126852bf37cdc895c8ccf7454a66d7b79053421f3bbe63a4`，包SHA `e31fee595b2d1d9b036d4674ff57ddcf7def2a51a156b08613c6add0388c1d83`，binding `b9ab087efa5f25dae354d644b925e64493fddedf0deda713918d6b6889d22dc9`。实际PID3160131、canonical cwd/JAR/receipt同批匹配、healthUP。两原schema runner所有表existing_equivalent，没有新DDL。
- 只读发布核验：新runtimeSetup/指南投影字节存在于安装JAR；loopback与公网安装查询均拒绝未登录GET（401）；线上同Run JuyiHall脚本含canonical HOME、目标机不自动更新、prepare命令。没有调用POST bind/registration/enroll、未创建生产角色、未付费，**不是全新用户生产接入E2E**。
- 前端与后端均1.14.11；isp-install更新已push。Runtime本机二进制仍1.0.2，服务PID3127402/NRestarts0，目录收口沿用前次事实，不把仓库文档更新当作远端批量升级。
- 公开安全证据汇总：`docs/implementation/evidence/selfhost-onboarding-20261012/unified-release-status.json`。私有完整包/授权/DB投影仍留受保护原目录，不提交凭据或私有inventory。新包和原始tmpfs尚保留，无副本退役。
- 发布时Web共享工作区HEAD已由另一任务推进至667ca7a，未覆盖其工作区/改动；本轮只声明受测上线aad2ae9，不把新HEAD冒充已验证。根集成固定发布组合时使用aad2ae9 gitlink，不checkout/reset共享Web。
- 定位/实现等待未独立精确计时；正式API首轮265.669s（skip，不验收）、R2 169.819s；Web实际Flow时间见Run206。容量阻塞随后自然解除，OOM恢复属于额外运维，不归入无实测提效承诺。
