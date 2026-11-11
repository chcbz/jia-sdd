# 典籍管理技能展示与任职 Agent 密议上架

## 目标与边界
- 用户请求：聚义厅好汉详情按“技能管理”的真实安装/运行投影显示“典籍管理”；在任职 Agent 的密议中完成《三国演义》上架。
- Owner：本聊天，2026-11-05（Asia/Shanghai）。任务标识 ARCHIVE-MANAGEMENT-CHAT-20261105。
- 不硬编码就绪卡片，不将后台直接代发伪称为模型密议执行，不恢复旧 runner，不覆盖其他任务脏改。不自动赋予全站管理员权限。
- 适用根 AGENTS.md、api/docs/interface-standard.md（2026-10-14冻结及其现有兼容补充）、specs/juyiting-skill-execution/responsibility-boundaries.md（RB-01/02/03/05/06及10-30责任层要求）、原生详设v3.1。

## 固定源码（本次只读）
- API主目录：516267bf7b19bfc03581ae580704af9246ffb622，codex/architecture-convergence-api，有大量其他任务未提交修改。
- 本轮fetch后 origin/develop：45440c6e71cf9b6e447e42114e866554f666d2ec，tree fb2da32e93a602d9cd8c9256dad92d8bd2dabf94；只读取远端引用，不重置主目录。
- Web主目录：ca22ac29de657971b12a71f3a99d2d9ecfc67c1c，有其他任务修改；未声称它是当前远端或线上版本。
- Runtime源码：/home/isp/wsps/chcbz/isp-install，d4dd804724c49947b9169264defb40c852dc7b4c，tree e214fe4656807ba43c3fef7dc30f2c0f63bfa79c；有无关untracked specs。
- 线上应用制品身份尚未重新核对；下列是实际HTTP现状，不以历史发布记录冒充当前安装证据。

## 2026-11-05真实只读核验
复用已有浏览器辅助工具，在本任务独立profile正常OAuth登录已有测试账号chcbz；不打印凭据、不修改其他聊天浏览器。证据 `/home/isp/state/cyf-archive-management-20261105/online-readback-private.json`（含查询时间，私有访问权限）。
- GET /agent/positions/v1：200。仅一个技能管理岗位/任命（吴用）；没有典籍岗位、典籍任职或典籍技能关联。
- GET /agent/skill-products：200，共7个技能，无archive-maintenance。
- 吴用profile-capabilities：200，图片编辑/生成/识别、技能管理共4项，均真实installationVerified/RUNTIME_READY；与用户截图一致。不是Web漏渲染一个已有安装。
- GET /archive/admin/v1/jobs：404/E404。未将404断言为唯一根因；仍需核对实际配置与安装字节。
- 原2026-10-26核验是历史证据，不能照抄“全部五表不存在”为当前事实，本轮未查生产schema。

## 实际调用链缺口与责任层
1. API `agent/.../api/SkillConversationToolAdapter.java`当前目录限定skill-management；Controller→SkillConversationTools为六项技能维护工具。Runtime `conversation-tools.mjs`已支持服务端工具目录、真实已安装包匹配和指令装载，应复用这条通用通道，不在bridge增加典籍名业务分支。
2. `chat/.../archive/service/ArchiveMaintenanceService.java`仍要求安装manifestSha256非空；当前原生INSTRUCTION合同恰不含旧执行manifest。这是旧执行合同缺口，不能只改中文标题或发布旧1.1.1包宣称可用。
3. `conf/skills/archive-maintenance-1.1.1`及`archive-job-reconciler.mjs`仍为EXECUTABLE/local-script；agent-client中仍有专用reconcileArchiveJobs。应按单轨规则收口受影响旧执行入口，保留历史读取和新方案自身恢复，不开启旧配置走捷径。
4. RB-02：任职/源授权、维护单、幂等、发布及active版本读回由原业务服务持有；RB-05/06：确定性文本解析继续属于技能脚本/工具，不把原著交由模型补写，不将整本正文穿入聊天上下文；RB-03：隔离执行与通用工具承载，不编排典籍流程。
5. Web现有真实安装投影可复用；仅当工具/维护结果合同实际改变时联动具体消费者，不默认重构整个前端。

## 待用户明确的业务输入
- 当前没有典籍任职。是否任命截图中的吴用兼任典籍管理；授予的公共典籍写入/发布范围需明确，不从技能管理岗位推导典籍权限。
- 《三国演义》具体底本/来源尚未提供。可请用户提供全文文件/指定版本，或明确授权Owner选择可公开使用的完整底本并冻结来源、章回数、权利说明与SHA；不能预设120回、抓取未批准来源或用模型补全。

## 下一步与验收
业务输入确认后：在不覆盖脏目录的最少隔离候选中补原生技能/密议工具和旧入口收口，沿已有岗位自动安装生命周期发布/关联/任职。先定向验证目录、授权、撤职/代次/取消、幂等与确定性导入，再Flow执行正式受影响回归与打包（单Run≤600秒，主机独立受控安装），复用输入一致制品。
验收须同时取得：实际“典籍管理”卡片及真实安装就绪、指定任职Agent密议的实际工具调用、维护单/发布提交、书架active版本与章节实际读回及来源摘要。聊天“已上架”、ACK、单元测试或截图不能代替发布事实。

本轮只有诊断工具和handoff；未改应用源码、未赋权/任命、未发布技能或典籍、未运行Flow/构建、未重启、未调用模型。不能标记开发或上线完成。

## 2026-11-05 18:32 +08 用户明确任命后的交付

用户明确：“增加典籍管理岗位，关联典籍维护技能，然后任命吴用”。本轮据此完成岗位配置，不把这条任命指令当作《三国演义》具体底本授权。

- 复用isp-install主工作区，先确认无tracked/index脏改，仅保留他人untracked specs；从实时origin/develop `b2d5f5700118dd148017a3db132e13d7e66bc020` 切本任务分支 `codex/archive-position-20261105`，未增加worktree。CYF AGENTS/RB/接口边界显式用于该外部仓库本次改动，未修改共享技能或其他项目规则。
- 原生包源码 `6b7035038b7e4af8a86d449df66d3587ceeef7f0` / tree `71ceacc30c97c1fcadcdfb5b6f5036e29a73594d` 已非强制FF推develop并readback。新增 `conf/skills/archive-maintenance/{SKILL.md,scripts/build-archive.mjs,test/archive.test.mjs}`；脚本与旧1.1.1逐字节相同，仅保留纯解析，不启用旧runner。包升2.0.0，无manifest.json、无依赖新增、无Runtime程序改动；未把仅安装称作密议工具已接通。
- Flow5264702/152 SUCCESS，真实worker定向6/6，打包上传后结束；createTime→终态updateTime约20秒。使用同Run包，校验commit/tree、ZIP/文件SHA、文件集合和源字节。ZIP SHA `d272bc3f1bd24fb215e1f23323ceb985a16cf3f756029ff0ca196a083e8f31a2`，3783字节。控制面原配置CAS恢复APPLIED，不动他人Run，没有API/Web/Runtime应用构建、安装、重启或本机生产打包。
- 真实chcbz OAuth确认tenant/client/owner，再通过现有技能管理岗位代办发布“典籍维护”2.0.0，产品 `sp_position_archive_maintenance`，版本 `spv_position_archive_maintenance_2_0_0`；发布HTTP200且返回包摘要匹配。
- 授权前只读快照实际数据库身份、DDL、owner权限、吴用binding和岗位state；受控release锁+既有数据库互斥+identity→position事务锁，仅补该owner的ARCHIVE_WRITE/ARCHIVE_PUBLISH对archive:public两行。无DDL、无全站ROLE_ADMIN、未改旧技能管理权限。恢复边界见私有证据目录recovery.md，不能用旧state覆盖后续事实。
- 通过正常HTTP定义POSITION技能→创建“典籍管理”岗位（archive-management，容量1，archive:public，允许发布，关联archive-maintenance）→任命吴用；固定幂等键与每步回执均保存。任命 `ps_d5653e189cb648b48bda8641d70d25a9`，岗位安装 `ps_c6619ded72c1422a8c5577676cbdb98f`。未伪造订单/权益/安装回执，未重复任命或手动触发安装重试。
- 自动安装由INSTALL_PENDING推进至INSTALLED/usable=true；profile-capabilities新增“典籍维护”2.0.0，installationVerified=true、RUNTIME_READY。真实手机宽度390页面显示5项技能，典籍维护和原技能管理均正常，截图 `/home/isp/state/cyf-archive-management-20261105/browser/wuyong-archive-skill-mobile.png`。UI无需源码修改。
- 最终证据 `/home/isp/state/cyf-archive-management-20261105/final-verification.json`，发布/岗位/任命/安装/profile及精确Flow制品同目录。浏览器只使用本任务profile，收尾关闭并清理；必要证据保留。
- 仍未完成：密议典籍维护工具接线、受控实际上架链和《三国演义》来源冻结/发布读回。此前jobs404仍是已观察的缺口，本轮不启用旧条件配置。岗位创建/安装成功不等于该业务链已可执行。当前任命请求已完成，原完整上架目标尚未完成。

## 2026-11-05 典籍阁仅保留任职：开工基线
用户要求去掉典籍阁维护功能，仅保留任职；内容维护统一在与任职Agent密议中处理。Owner仍本聊天，任务标识ARCHIVE-POSITION-UI-20261105。范围限Web入口、任职读取/幂等恢复、密议导航与定向回归；不改变API业务授权/数据库/Runtime，不因删除表单宣称密议上架已打通。

主Web有共享JuyiHall.vue等未提交修改，且已有隔离工作区属于其他任务，故仅创建一个必要worktree `/home/isp/wsps/worktrees/archive-position-ui-20261105`，分支codex/archive-position-ui-20261105。fetch固定origin/develop `54418fe5bddee1805d5d03d030a54c326dad172a` / tree `619013131f3ef6b84b3d6f9ba8b22987d2901041`。显式遵循根AGENTS、Web AGENTS、接口规范2026-10-14冻结及RB-01/02/03/10-30最小联动边界。

已定位：原useArchiveMaintenance.reload将岗位GET和旧维护GET放在Promise.all；后者404导致岗位数据不展示。修复责任在Web取消该页面无关维护读取，不绕后端权限、不恢复旧接口。保留岗位幂等/身份切换；旧维护未决引用只保留，不查询/自动重放。新岗位操作与历史维护引用分开存储，旧岗位未决操作沿原键恢复。

先更新唯一原型 `/home/isp/wsps/cyf/web/prototypes/juyiting/interaction-completion.js`、对应CSS及specs/prototype-spec.md：第三页签“任职管理”，任命/卸任、已任职吴用密议入口、空/加载/失败离线状态，无内容维护表单。使用既有18786预览服务（HTTP200），不启动/关闭其他任务服务。正式实现与验证后续补记，原型不代表上线。

### 任职管理 UI 实施与轻量反馈
- 原型已先行：`web/prototypes/juyiting/index.html#library`，1440/390 截图位于 `/home/isp/state/cyf-archive-position-ui-20261105/browser/prototype-{desktop,mobile}.png`；点击吴用密议进入独立私聊，无自动发消息。
- Web 拆出 `ArchivePositions` / `useArchivePositions`：不再访问 archive jobs API；保留任职、岗位配置、安装恢复，接入 JuyiHall 既有密议权限判定/选择入口（RB-1 Web 展示层，无 API/Runtime 合同变化）。旧 job intent 保留、不查询/重放；旧 position intent 按原键恢复。
- 本机轻量测试：任职15项、LibraryPanel4项通过；新组件/composable lint；LibraryPanel 既有搜索 SVG 行 lint 问题未扩修。
- 执行偏差：首次 Mocha 命令漏 `--no-config`，误加载默认测试列表，发现后精确终止本任务 PID432518；不作为正式证据。后续均显式 `--no-config` 定向，重型正式验证走 Flow。
- 本次只调整典籍阁 UI 与密议导航。维护工具实际执行/三国演义上架仍未完成，不以入口存在冒充执行通过。

### 任职管理 UI 正式验证与合入（2026-11-05 18:55 +08:00）
- Web `1.16.113`，commit `ccefcc08e516b256ec2495d66cf4d8781f8f45fa`，tree `9ba57536deab11a56f241d731e209ea94ed6203b`。固定候选已非强推快进合入远端 develop；未覆盖主Web脏工作区，也未改变其本地分支/gitlink。
- Flow `4403172/450` SUCCESS：任职/恢复、阅读、LibraryPanel/聚义厅组件、私聊、身份和经济幂等共299项通过，0失败/跳过；Vite生产构建、扫描、上传均成功。终态于启动后约110秒内观测到；无Flow主机调用/外部验收等待。初次start响应UNKNOWN携带唯一Run450，后续只查询该Run，实际source与候选一致，未重发start。
- 固定同Run制品SHA-256 `2ce3853841503cf0cb4fb28e23d44bb8ba46bc6f7b885b4f2e8ca6b372523b9c`，612个dist文件完整性已比对manifest；真实commit/tree/version/Run匹配。云端原配置已CAS恢复并readback。
- 证据：`/home/isp/state/cyf-archive-position-ui-20261105/release/web-{verified,restore,role-ui-bundle-check}.json`，同目录保留不可变制品、测试报告和Run/日志；截图含桌面/移动/空态/错误态。
- **未安装、未宣称线上页面已切换**：页面修改请求未明确授权本次前端版本发布，按develop不自动部署规则留存已验证制品，待发布授权后复用Run450受控安装，无需重复构建。未改生产配置、API/Runtime程序、任命或书籍数据。
- 《三国演义》密议维护工具接线、明确底本及实际上架仍未完成；本次验收是页面收口与私聊导航，不作为内容维护执行证明。

- 收尾：远端develop读回为上述候选；本任务唯一隔离worktree及临时编辑脚本已清理，保留源码提交、原型和验证/制品证据。主Web未提交修改和其他任务预览服务未动。

### 2026-11-05 用户纠正：任职页不重复密议入口
- 用户指出好汉详情已有密议按钮；当前范围仅移除上轮额外新增的任职行按钮、其专属props/emits/转发接线及测试假设，保留好汉详情既有密议和典籍阁任职功能。不修改API/Runtime或生产数据，不追加发布授权。
- Owner仍本聊天；实时fetch origin/develop `ccefcc08e516b256ec2495d66cf4d8781f8f45fa` / tree `9ba57536deab11a56f241d731e209ea94ed6203b`。主Web JuyiHall.vue仍有他人脏改，故在上轮已清理的同一路径重建唯一必要隔离worktree，分支 `codex/archive-position-no-chat-20261105`，不复用/改写其他任务工作区。
- 原型先移除任职页重复按钮和处理函数，提示明确转向好汉详情原有“密议”；遵循根/Web AGENTS、RB-1及10-30最小联动规则。证据使用原任务目录的 `no-duplicate-chat/`，原Run450仅代表旧候选，不充当本次验证。
- 修正源码 `820755b00c32cbe6224e6c6148c27f934e042f51` / tree `523d7fc5278b889a510ea9c3d1d845d7c5f5e6a7`，Web候选1.16.114。删除ArchivePositions的按钮/目标解析/props/emits、LibraryPanel透传及JuyiHall仅LibraryPanel的两行接线，AgentPanel已有的密议绑定和权限处理原样保留。
- 本机15项任职/恢复/SFC定向测试通过，ArchivePositions lint通过。更新挂载测试验证无密议按钮且卸任仍提交原任职ID；正式Flow回归增加既有agent-panel-actions、pending-requirement-roster、selected-agent-card套件，不改测试以掩盖入口丢失。
- 原型1440/390任职页无重复按钮；从吴用详情原有private-chat进入#private且目标吴用，无自动发送。截图和辅助日志在 `no-duplicate-chat/browser/`，这是离线原型验证，不是生产验收。
- 正式验证：Flow `4403172/451` SUCCESS（启动后约102秒内观察到终态），333/333测试通过、0失败/跳过，生产构建、JS扫描及上传成功。初次start UNKNOWN携带唯一Run451后仅核查，未重发；source精确匹配修正候选。完整测试报告来自同Run制品；单独控制台日志查询遇ECONNRESET，不影响Run/制品测试证据，不声称控制台日志全部取得。
- 制品SHA-256 `af26a213c7e91c607e5af7f749ff71e71b73e634d89983e2f5e6984d21e70f2a`，612文件及commit/tree/version/Run摘要闭包核验通过。`no-duplicate-chat/release/web-verified.json`、`web-role-ui-bundle-check.json`、`web-restore.json`为证据；云端配置已CAS恢复并readback。
- `820755b00c32cbe6224e6c6148c27f934e042f51` 已非强推快进合入origin/develop。版本1.16.114取代1.16.113为当前本任务待发布候选；不得部署旧Run450以免重新引入重复按钮。此次仍未发布、未修改生产数据、API/Runtime或好汉详情密议实现，维护执行链/三国演义上架结论不变。

- 修正收尾：已清理本任务隔离worktree与浏览器临时profile/进程，验证和不可变制品保留；没有关闭共享原型预览服务或改动他人工作区。

### 2026-11-05 19:38 +08:00 用户明确授权发布后的线上核验
- 用户“发布”授权对应修正版Web1.16.114；复用Flow4403172/451同Run制品，复核SUCCESS、333项测试及完整commit/tree/612文件摘要，没有新开流水线/本机构建。
- 发布前记录线上Run449/version1.16.112/commit54418fe5。在既有deploy.lock保护下备份旧record及将被覆盖的旧index.html，旧hash资源保留；备份与恢复说明 `/home/isp/baks/cyf-archive-position-ui-20261105-run451/`。按既有受控安装器执行，制品放于固定downloads/451/package.tgz，身份、制品校验、安装互斥及index-last保持不变。
- 安装exit0，主机612文件匹配，线上初期缓存返回已知旧index，既有核验在第11次读取到新摘要后PASS；未因此重建/重装。现行record为Run451、commit820755b、version1.16.114、online_verified；另核对线上入口及聚义厅关键JS/CSS等6资源与同Runmanifest逐字节摘要一致。
- 新浏览器profile正常登录后核验PC/390页面：页签“典籍阅读/案卷检索/任职管理”；无内容维护表单、文件上传、重复密议按钮；任职接口200，吴用兼任典籍管理/技能管理及两技能已就绪；无旧jobs请求/资源不存在错误。通过好汉详情原有“与这位好汉密议”实际进入吴用普通密议，输入为空，未发消息、未任命/卸任/重装技能。
- 完整证据 `/home/isp/state/cyf-archive-position-ui-20261105/no-duplicate-chat/release/final-verification.json`、`web-installer-result.json`、`online-assets.json`，截图/DOM读回/脱敏路径网络日志在同级 `online-browser/`。安装、资源和业务UI核验分开记录。
- 本次只发布Web页面收口；没有API/Runtime安装或服务重启，没有生产书籍/任命数据变更。密议维护工具接线及《三国演义》实际上架仍未完成，不能以进入密议冒充业务执行验收。

### 2026-11-05 接通原生密议维护（进行中）
- Owner本聊天，用户目标：通过吴用现有密议新增《三国演义》。不恢复维护页面、不增加重复入口；底本/版权来源尚待用户选择，不下载或编造全文。
- API主工作区有重叠脏改，唯一隔离工作区 `/home/isp/wsps/worktrees/archive-conversation-api-20261105`，branch `codex/archive-conversation-20261105`；创建时origin/develop `45440c6e71cf9b6e447e42114e866554f666d2ec` / tree `fb2da32e93a602d9cd8c9256dad92d8bd2dabf94`。主HEAD516267b不是受测候选。Runtime已读源码1ad3a9b，尚未修改/安装。
- 责任：API具体典籍工具复用岗位权限、内容导入和私聊当前turn fence；bridge现有通用catalog/POST适配不增加典籍业务分支（RB-1）。全文通过个人文件库owner-scoped固定版本读取、摘要校验，不经模型重写；明确来源和权限后，先草稿后显式发布，读回权威状态。旧manifest执行与重放不能作为新链路。
- 接口基线：API docs/interface-standard.md；新工具无新Web契约。需覆盖旧技能工具不回归、当前turn/任职/安装撤销、owner文件隔离、幂等输入冲突、版本CAS及真实内容摘要。重型验证仅Flow；当前未测试、未发布、未上架。

### 原生维护候选与验证推进（2026-11-05 20:32 +08:00）
- API候选1.1.34-SNAPSHOT：`7d9746a1f97fa5a725af1f01be829cc873832a3e` / tree `fa9e13fb49202fb0a00283e3e48d11080de1d130`，已推任务分支，尚未合入develop/安装。核心新增ConversationToolProvider/Extensions，仅组合业务目录并复用native/current-turn fence；典籍工具只经Agent API `PositionArchiveAccess`使用任职/安装权威，未增加跨域service依赖或修改分层基线。工具闭包为source/prepare/publish/read/recover，原生INSTRUCTION包兼容。
- 具体文本工具ArchiveTextCompiler与现有2.0.0脚本以固定自写Unicode fixture逐字/摘要对照；固定源文件由已有PersonalWorkspaceService按owner/file/version读取，不由模型传入/重写全文。原ArchiveMaintenanceService改为历史只读，旧create/retry/commands/source/result-submit/publish路径删除，注册声明固定archiveJobDiscovery=0。无DDL、无生产数据操作。
- Flow5260799/521 FAIL（约121秒终态观测）：分层检查发现新类直接跨域service，且测试源glob过宽。已通过新增Agent API职责入口和精确测试文件选择修复，没有添加分层豁免或删必要回归。Run522 FAIL（约145秒）：编译/分层通过，原生SQL fixture误把逻辑installation ID当physical ID导致7项被正确拒绝；已改为实际physical映射并补工具目录/回调wire测试，非放松生产校验。证据在`/home/isp/state/cyf-archive-conversation-20261105/release/`及`corrected/diagnostics.json`；两次失败均保持真实FAIL并已CAS恢复云端配置。Run523当前验证上述新候选，不能把旧Run作为成功证据。
- Runtime复用既有干净源码工作区，显式遵循CYF AGENTS、RB-1/单轨删除、固定app目录及接口规范；未使用/修改无关untracked specs。候选Runtime1.3.58/bridge1.1.47，源码`1b296af7b5fc442d9a8730a2e4ba511acf2c2bc4` / tree `f69ef2934071176cec0d98dc97f95b0b39bdbd73`，已推原任务分支`codex/archive-position-20261105`，未合入/打包/安装。删除archive-job-reconciler及其导入、定时调用、制品清单项和旧HTTP执行fixture；保留岗位安装对账和既有通用conversation tools，不增加技能名业务分支。
- Runtime本机轻量验证：13项（解析/岗位安装与恢复/通用工具/典籍+技能目录组合）+2项定向宿主注册/旧标志不得复活轮询，全部通过；两处源码语法检查通过。日志`runtime-light-tests.log`、`runtime-host-light-tests.log`。均为低开销测试（约1.7秒和0.4秒），不是Flow打包或线上验证；未触动运行中的程序、状态、锁、安装目录。
- 当前未确定《三国演义》底本，未下载、上传、构造生产维护单或发送真实Agent请求；Web1.16.114历史发布不构成本轮API/Runtime发布授权。下一步：完成Run523与制品证据、源码集成；用户确认底本/本轮发布后复用固定制品安装并通过吴用现有密议实测。历史截图/岗位安装/模型口头答复不能代替真正PUBLISHED和阅读器首末章读回。

### 2026-11-05 用户纠正：通用技能发现，不逐技能接密议
- 用户明确要求长期通用方案，拒绝为解决典籍个案在密议增加技能白名单/特殊编排。上一候选的技能目录按业务provider筛选技能，且Controller保留技能管理专路，不作为最终架构或上线候选。
- 本轮收口：技能发现统一使用当前安装事实，与业务工具目录分离；所有业务工具经同一个provider入口，业务域保留岗位权限、事务和幂等。安装技能不自动授予shell/网络/业务权限；不增加按技能名执行分支。
- 继续使用原API隔离工作区和Runtime工作区；不覆盖他人修改、不发布。Runtime旧轮询删除提交1b296af已快进远端develop，尚未打包/安装；前段“未合入”仅为当时状态。Run523是旧候选测试证据，不是本次通用调整验证。

### 通用方案源码与最小反馈（2026-11-05 20:55 +08:00）
- API `4dc5c51d26b375c411fc8ff4aecee0fc3a1f51ea` / tree `74e8120282812b6b78eeebc1f209797726c55960`，1.1.35-SNAPSHOT，已推原任务分支，未合入develop。技能目录统一读取InstalledSkillDescriptorLookup；Controller删除技能管理专用分流，所有工具统一provider；典籍岗位关联实际配置技能，不硬编码名称。接口基线`api/docs/interface-standard.md` SHA256 `7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f`，遵循RB-01/08/09与10-30分层责任规则。
- Runtime `c023239b494baa619ba1f8b745b5502e26401c94` / tree `20116032ade9e5081b10ac5000a85afe60805d02`，1.3.59/bridge1.1.48，仅推原任务分支，未合入develop/打包/安装。目录支持技能和工具独立为空；指导型技能无需业务工具也进入现有隔离app-server。没有增加shell/网络授权，没有新技能名分支。附带材料会话仍使用原独立执行能力，本次未扩大其文件/工具视图。
- Runtime轻量15+19=34项通过，日志`/home/isp/state/cyf-archive-conversation-20261105/runtime-generic-{tools,adapter}-tests.log`，分别约2秒/0.34秒；初次新增测试中的提示词断言和闭包fixture错误已定位修正，不是业务保护放宽。没有本机构建/生产打包。
- 原Run523已核验174项通过、0失败/跳过；JAR SHA `94eb52e94436f6ab0c3a1dda9b5bc2a19013436eeb8aedbb68a8402b62bc3768`，制品SHA `b5ea7035b9f46a3d9999ea888d8d3a0e9223c549da90046159ed9547232abe9f`。证据`release/native-fixture/api-verified.json`。只证明旧候选，不用于通用修改。
- 本轮新Flow候选文件放`release/generic-discovery/`；准备时发现其他Owner Run526 RUNNING，未改云端配置、未取消或抢占。发布和三国演义实际内容操作尚未执行，底本及使用权待明确。
- 20:59 +08:00再次只读查询：API流水线现为其他任务Run527 RUNNING；云端source仍是`codex/beta-wen-billing-20261105`，并非本任务/已恢复默认配置。本任务不能覆盖其配置，正式API回归尚未启动。仅本地YAML/source静态核对通过；没有新Run、没有安装、没有将34项Runtime轻量测试替代API编译/数据库测试。
- 接续：等现有Owner完成并释放/恢复共享Flow配置，再使用`release/generic-discovery/control.cjs`的prepare/update/start及watch入口验证固定API4dc5c51候选，最终CAS恢复配置。若源码变动必须更新固定source；不得复用Run523结果冒充本次。API/Runtime均暂留任务分支，唯一API worktree因待验证继续保留；两个本任务临时编辑脚本已删除。
- `./sddw check-docs archive-agent-maintenance`导航检查通过；仅文档反馈，不是正式应用验证。新增普通技能不改密议代码的边界及空集合兼容语义已回写原spec；真正业务上架验收仍待正式验证/发布与明确底本。

### 2026-11-05 用户授权发布并完成《三国演义》上架
- 用户本轮明确授权本功能API/Runtime发布及通过吴用密议完成新增。Owner将选取原著公版完整底本并固定原始来源与摘要；不编造正文、不绕过Agent密议执行，不新增维护UI或技能名分支。
- 当前线上基线只读核对：API Run505/45440c6，Runtime Run151/1.3.57/b2d5f57；组件远端develop仍为API45440c6、Runtime1b296af（2026-11-05 21:45 +08）。其他任务Run527已终态，云端配置恢复develop后启动本任务API528。
- API528 SUCCESS，约179秒观测终态，178项测试通过/0失败/0跳过，分层/全新JAR/上传成功。固定4dc5c51/tree74e8120；制品f0815e4e145e23e5cd8a661a048f19047c637d089deae16057c0b0ea751fc3f9，JAR3d9a1c264405ebf68f9f8d6a374ec234fc723fdfd1a6f66d44902cc5799fff96。云端配置CAS恢复并readback。证据release/generic-discovery/api-verified.json。尚未安装。
- Runtime153 FAIL（约311秒），982项中966通过、1失败、15现有环境条件跳过：最后一条宿主heartbeat回归仍预期已退役archive轮询。真实代码没有调用旧轮询，符合RB单轨删除。修正为连续注册及后续heartbeat均不得复活旧runner，保留整个场景，新增本机3项定向通过；源码6740af33862ddd949544ca337db6d7d2704a08bb/tree37245a258023d45232e4a468b739ed6ccd34035f（payload仍1.3.59，仅测试修正）。Run153原FAIL保留，已恢复配置，不发布其产物；新验证放release/runtime-retirement。
- 22:19 +08续：Runtime154 SUCCESS（327秒观测终态），982项967通过/0失败/15既有环境条件跳过；实际宿主3项namespace/browser/document probe和启动readiness另在安装前通过。制品49f22bde8603742e57d067f810a9113e0a049908be5a4b99e6937f6f3f8ad520，完整文件/依赖/源码核验通过。配置CAS恢复原值，API4dc5c51与Runtime6740af均快进推到develop，无重复构建。
- Runtime先装，固定app已切至1.3.59/Run154；旧程序和停写后状态备份`/home/isp/baks/cyf-agent-runtime-v1/20261105-archive-conversation/`，身份/config保持；安装exit0，service active/PID522381。API528随后由既有受控主机入口安装中，未以Flow成功冒充应用健康。健康monitor维护标记由本任务创建，归属证据`runtime-install/maintenance-owner.json`，待两端健康后恢复。
- 公版完整底本取自PG23950原著繁体电子文本（目录标记USA public domain），多次不完整传输未使用；改curl HTTP2逐段精确Content-Range下载并复用已核验片段，最终1863656字节/raw SHA ed422e10c16c19af7ca7b09ca0320012e60776b3d7cb054769b8f7d9a19aea7d、完整END及1..120连续章节核对通过。私有保留来源和完整许可；公开正文去掉PG前后说明及署名尾注，按许可1.C不保留品牌，120个原样标题仅加Markdown `# `标记（原文100回以上用○编号），没有改写或生成正文。
- 正常owner上传201/COMMITTED：file pws_e26f49be63e84847923f2b92883c02d4/version1，1844049字节/SHA 3ff98c1e70f60d0348c57a6d4e3116ca03b9899031ae76a6c374ea1397f95d94。第一上传认证包装解析错误无有效回执；修正读取token.data后沿用同一幂等key成功。未调用典籍写接口。
- 上架前只读发现已有sanguoyanyi/edition sanguoyanyi-zh-120-v1书目，catalog HTTP500，日志确认为既有active chapter metrics drift。计划由正常密议工具在同workId准备/发布新完整版本并保留历史，不重复建书、不直接修SQL、不把旧书目误报为本次上架。底本/上传/旧书目证据`source/`；实际密议尚未发送。
- API528受控安装exit0，JAR与Run摘要一致，PID525324/HEALTH=UP/ARTIFACT_ATTESTATION=MATCH；启动实际46秒，canonical-path测试通过。既有F06安装hook仅回读existing_equivalent，无新增表；E05未获授权故未执行，未扩大本任务迁移。两端运行后按inode/dev/SHA核对本任务maintenance标记并resume，未重置监控熔断。
- API重启后旧浏览器token失效，第一次点击发送仅到chat/capabilities401即转登录，未生成discussion请求、未执行典籍写入。重新正常登录后继续同一底本与固定幂等键；不能将点击按钮当作已进入执行。
- 22:27真实普通密议请求6810e207-dee3-44df-b8c2-a2177a69f7b5/turn_8dc235d658447443355709241e4fc1414a6bffc1已执行archive_source，返回固定文件版本/摘要一致；archive_prepare503进入RECOVERY_REQUIRED。定位不是技能发现问题：原生模型已获得并选择典籍工具，生产缺archive_skill_maintenance_job/action两表；前述“既有表已存在”的接续假设错误，已用真实SHOW TABLES纠正。API admin旧jobs404是关闭历史入口，不代表原生工具不可用。
- 用户发布范围内补齐安装制品自带的精确CREATE-only迁移：API528 JAR抽取db/archive-maintenance-jobs.sql与4dc5c51源码逐字一致/SHA3ded9421aaa4e3aef621c796fdc06c29315535a23c97e764b32375244102e037。coordinator→release锁+既有position数据库锁，固定server_uuid/database/identity，先在真实目录`/home/isp/baks/cyf-archive-conversation-schema-20261105/`备份现有8张archive表一致性快照及DDL；只创建缺失的两张记录表（无CHECK），没有典籍内容DML、没有开启旧runner、无需重建/重启。readback通过，证据schema-installation.json及恢复说明。
- 原失败请求通过原UI“停止本轮回复”结束，服务端CANCELLED已读回；同一吴用普通密议发恢复消息，明确先recover原准备/发布键，再NOT_FOUND情况下同键/同参数继续，没有重放旧任务或更换业务幂等键。仍待实际发布回执与全文读回。
- 22:39续：恢复消息48a3e3ee-1bc8-446a-aa4c-b1a7bf7f409b虽然CHAT回复COMPLETED，但Agent明确拒绝把Context Envelope.currentUserMessage当指令，**没有典籍工具调用/发布**。发现通用bridge policy错误将当前用户请求与附件统列untrusted DATA；不是本次用户缺授权，不靠提示词绕过或技能专用分支解决。
- 通用修正Runtime1.3.60/bridge1.1.49：5d7290c92b684c3fbc03120a5ad416d79918e589/tree6e7d6cbccb27ff435e8cab0b46f0846d362f10fa。共享静态CHAT_CONTEXT_INSTRUCTIONS把顶层currentUserMessage.content委托为用户级请求，参考资料/引用文档/附件/日志/代码/历史Agent动作仍不授予策略/权限；API权限与工具回执保持权威。已有instructionSourceHash使新策略不复用旧线程，无API/Web源码变动。轻量两项生产Fast CHAT路径/附件隔离回归通过；原任务分支推送后启动Runtime155正式验证（22:44:51+08），同一600秒watcher生效。无新worktree，未覆盖外部repo specs脏目录。
- Runtime155 SUCCESS（311秒观测终态），982项967通过/0失败/15既有环境条件跳过，source/tree/692个payload文件、依赖归档和真实XLSX probe核验通过。制品SHA49e8b9ec52f92f17ece0c83b9a77bbc73ae31f589ac7effea5020ea2c145dacf；云端配置CAS恢复默认，候选5d7290c快进到develop。当前按新固定Run155安装1.3.60，复用API528及已核验底本，不再次构建API。证据release/request-boundary与runtime-request-install；未将chat COMPLETED误作上架。

### 2026-11-05 最终发布及业务验收完成
- Runtime155已安装1.3.60/bridge1.1.49，PID554010，通道/吴用online与API528健康通过；本任务维护标记按归属恢复。版本记录在原发布锁下核对当前commit/run/PID后更新为本任务范围verified-active/business PASS，不重认证无关能力。此前154仅为历史阶段。
- 真实吴用普通密议request `01ad2493-fd1f-4f68-a662-d49516c09d60` / turn `turn_85fc7dadace6db85f2ff93d5a508916f43954864` / finalMessage2106109：先recover原幂等键NOT_FOUND，再source/prepare/publish/read；服务端COMPLETED、PUBLISHED。job `ac_7a028b9bac894e0e846eed5638f04411`，edition `edition-ac_7a028b9bac894e0e846eed5638f04411`，sanguoyanyi active=true。没有直接写库上架、没有技能/书名专用路由。
- 正常认证阅读API逐章读回120回、17462段、1772055 UTF-8字节；所有段落文本/摘要/长度与固定底本一致。旧edition sanguoyanyi-zh-120-v1保留，同work新活动版本消除旧catalog metrics drift，不重复建书。全文证据acceptance/reader-verification.json，独立只读事实authoritative-publication.json，真实工具记录online-browser/publication-tools-evidence.json及最终回复截图wuyong-publication-completed.png。
- 汇总acceptance/release-acceptance.json；当前release-record前后快照同目录。Runtime备份/home/isp/baks/cyf-agent-runtime-v1/20261105-archive-request-boundary；表结构变更快照/home/isp/baks/cyf-archive-conversation-schema-20261105。来源、旧程序、状态/身份备份和不可变制品保留。API和Runtime候选均已快进develop，云端配置CAS恢复，无新增构建/安装。
- 稳定知识回写原runbook/spec。范围限制：普通密议引用owner文件固定版本已验证，带附件材料会话工具视图未扩展；不以此验收其他Runtime功能。记录更新初次遇本机Python3.6不支持subprocess text参数，在写生产记录前失败；改用universal_newlines后完成，无应用重启或业务重放。

- 收口：文档导航检查DOCUMENT_NAVIGATION_PASS；已核对远端develop为4dc5c51，任务API worktree干净且HEAD在origin/develop，随后移除本任务worktree。其他脏工作区、备份和证据未清理。

### 2026-11-05 跨书切换修复接续（Owner：当前会话）
- 目标：恢复进度失败后的显式重试和跨书切换，书架显示真实失败及可用恢复入口，不丢手札/书签或绕CAS。非目标：新增维护入口、修改API/Runtime合同、直接改生产阅读进度；本轮“修复”不视为发布授权。
- 本机Web为较旧ca22ac2且有大量其他任务脏文件；无法安全切换到线上源码，故仅新增一个必要隔离worktree `/home/isp/wsps/worktrees/archive-reader-switch-20261105`，分支codex/archive-reader-switch-20261105。远端develop于本轮fetch核对为820755b00c32cbe6224e6c6148c27f934e042f51，与线上1.16.114/Flow451一致。base tree通过git记录在任务证据。保留其他任务工作区。
- 责任层：Web useArchiveReader串行进度/CAS状态及ArchiveReader错误展示。线上23:18—23:19四次进度PUT409；源码确认错误态flushProgress不再次保存、openBook永久拒绝切书，错误只在已关闭阅读窗口显示。409具体冲突来源未额外推定。
- 先更新现有原型library/reader失败与重试状态，再实现；原型路径为该worktree下prototypes/juyiting。最早定向验证tests/archive-reader.test.js；重型回归/构建走Flow4403172，API/Runtime不联动。统一接口规范api/docs/interface-standard.md固定SHA256 7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f；RB-1及10-30责任层规则不变。

- 修复候选Web1.16.115 commit f3cd173b42c36fb493724214ac1f324d5646ac7c / tree3e083f6c96e7501750db451dfae4e76e524c2b8d，已推任务分支。只改Web局部进度恢复、书架错误与原型/测试，无API/Runtime修改。错误态仅显式动作核对服务端版本后重试一次，失败保持原书，不绕CAS；并发恢复共享、身份变化拒绝晚到写入。
- 原生产实现运行新增两项回归均失败；候选完整阅读器93项通过（约6秒轻量运行），含四项新增、既有逐书草稿保留。首轮DOM测试点击发生于仍在保存、按钮禁用期间，修正等待真实error状态后通过，不放宽产品保护。ESLint composable零问题；SFC保留基线87 errors/23 warnings（既有紧凑SVG格式），逐条规则/消息集合对比零新增，未顺手格式化无关图标。
- 原型1440/390/320实浏览器错误可见、无水平溢出，重试示例正常；截图及prototype-checks.json保留任务browser目录。原型预览仅离线，未访问生产阅读接口。
- Flow4403172/452于23:36固定该commit启动，首次回执runId452但source尚未就绪，未重复启动；现有600秒watcher持续核对本任务run。CI仅测试/构建/上传，不安装；本轮尚未发布。证据根/home/isp/state/cyf-archive-reader-switch-20261105。

- 最终Flow4403172/452 SUCCESS，约122秒观测终态；337项通过/0失败/0跳过，四个新增回归均在同Run报告中为passed，构建与JavaScript扫描成功。固定f3cd173/tree3e083f6；制品SHA a8ec578b43999a64ffd446d63e4f58a642f027596ab892207f6fca42e922bcb1，108202165字节、612个dist文件摘要逐项核对通过。制品保留供后续获授权发布复用，不再因安装重复构建。
- 云端配置按候选hash CAS恢复并readback到任务前原值（原source为codex/clarification-empty-facts-20261104、triggerEvents空，不误称默认develop）。已快进push develop并只读回查完整commit为f3cd173。无安装/重启/生产进度写入；线上仍1.16.114/Run451。验收汇总/home/isp/state/cyf-archive-reader-switch-20261105/acceptance.json。
- 已关闭本任务离线预览服务/浏览器并删除其临时profile；原型截图/回归/构建/摘要证据保留。其他任务源码脏文件和历史备份未动。该修复无需API或Runtime发布。

- 文档导航检查通过；任务worktree内容已提交/推送且干净，移除其依赖软链接后删除该唯一任务worktree，未清理其他工作区。

### 2026-11-05 进度失败实测定位（用户要求查明首次冲突来源）
- Owner当前会话；仅在线真实阅读诊断和只读源码/日志/数据库查询。不部署候选、不清空/直接修数据库进度。沿正常UI/认证接口记录progress GET、PUT的请求体/版本/幂等key和完整错误响应（不记录token/cookie）。测试前后快照保护现有阅读状态，同根因最多两次，不无限重试。
- 线上Web仍820755b/1.16.114/451，未使用f3cd173候选来掩盖错误。复用既有CDP浏览器工具，独立归属证据目录/home/isp/state/cyf-archive-progress-cause-20261105；未开worktree，无重型构建。

### 2026-11-06 00:03 +08 实测根因确认（不是仅凭409推测）
- 新建独立正常登录浏览器，从“我的→典籍阁→三国演义”进入原生产Web1.16.114/451。未部署f3cd173、未模拟网络、未调用内部业务写接口。测试前真实GET：三国进度version8，chapter-1-p-70/offset0；水浒version207。
- 两次点击同一已保存段落，保持原阅读位置：第一次request68d30440-1e1e-4056-8098-49c81c762752，expectedVersion8，真实HTTP200/E0，服务端写成version9；header X-Request-Id正确，但JSON body requestId=null。页面显示“未保存”。使用线上820755b的原decodeHttpResponse对捕获报文独立重放，确认PROTOCOL_INVALID_RESPONSE/status200，客户端不会应用返回的version9。
- 第二次request5570110b-ba36-43bf-9140-e5c2352044b8仍提交expectedVersion8（幂等key与前次不同），服务端409/VERSION_CONFLICT，明确currentVersion9；此错误返回JsonResult而非bytes，requestId正常，前端随即GET同步version9。说明409是上一次已成功但回执不合规的次生冲突，不需要多标签页或并发写入才能复现。
- 固定线上API4dc5c51源码路径：ArchiveWriteJson.success提前序列化JsonResult.success(data)成byte[]；ArchivePersonalDataController.mutate直接body(result.body())；公共ApiEnvelopeAdvice只处理JsonResult对象，故无法注入当前requestId。当前PID525324仍在。相同bytes路径用于该Controller其他维护写回执及ArchiveQuestionController（源码受影响范围，未在生产制造手札/书签/提问写入）。不要把局部问题扩大成放松Web协议校验或为书名添加例外。
- 原始无凭据报文browser/archive-wire.jsonl、正文不含private notes，仅progress请求/响应；独立解析证据cause-verification.json和verify-cause.mjs、生产parser快照、线上错误截图均保留/home/isp/state/cyf-archive-progress-cause-20261105。前后GET证明三国location/state不变，仅成功CAS递增8→9及更新时间；水浒进度完全不变。不回滚版本、不清空记录、不改数据库。
- 修复范围纠正：此前Web1.16.115/452仅解决错误态无恢复/不可见，不能根治“成功回执requestId为空”；不得把其单独发布作为本问题端到端修复。根治应在API领域原始回执→HTTP信封适配边界，使用公共requestId责任层，保持已提交业务事实与幂等结果，覆盖首次成功及重放请求关联、真实前端解析和连续保存/跨书回归。本轮按用户要求完成实测定位，未修改API/发布任何候选。

### 2026-11-06 保存回执修复（实施中，未发布）
- Owner：本任务 Codex；范围：典籍 HTTP 写回执恢复为 JsonResult，交由既有 ApiEnvelopeAdvice 绑定当前请求；幂等存储、CAS、授权不变，不修改 Web/Runtime 或线上数据。
- API 工作区 `/home/isp/wsps/worktrees/archive-progress-envelope-20261106`，分支 `codex/archive-progress-envelope-20261106`，base `4dc5c51d26b375c411fc8ff4aecee0fc3a1f51ea`（已核对 origin/develop）。主 API 工作区存在其他任务修改，不覆盖。
- 接口规范 `api/docs/interface-standard.md` SHA256 `7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f`；责任归 HTTP 适配边界，公共响应关联机制不变。
- 验收：首次保存、相同幂等键重放、新请求关联、连续保存和真实旧版本冲突；既有跨书 Web 回归复用 Flow452，重型 API 验证走 Flow5260799，不安装。
- 证据目录 `/home/isp/state/cyf-archive-progress-envelope-20261106`。

### 2026-11-06 保存回执修复完成（已合入，未发布）
- API `1.1.36-SNAPSHOT` / commit `b7b4cf7e8ab6b7a39f1e010bb4133b7458e51b17` / tree `b78580146b3157228bb7aba51fc639b71267de1c`，已快进推送远端develop。只改典籍HTTP适配器及对应回归/版本；统一Advice、业务幂等收据和CAS未改，不按书名增加逻辑。
- `ArchiveMutationResponses`同时用于个人进度/书签/手札和问答创建/重试，将存储回执还原为JsonResult并清除历史传输关联，再由公共Advice绑定当前requestId；状态码/业务结果/Cache-Control保留，存储字节不变。
- Flow5260799/539 SUCCESS：14个测试套件122项全部通过，0失败/错误/跳过；`archiveReaderRegression`、`ApiEnvelopeBoundaryTest`、`validateLayering`及fresh `bootJar`均实际执行；仅JavaCompile缓存复用。Run createTime→updateTime 135秒，监视器从启动上下文起观测153秒，均低于600秒。流水线原配置已CAS恢复并readback。
- 真实服务+MVC回归输出：首次保存v1；同键不同requestId重放仍v1且不重复写；下一次用返回版本保存成功v2；真正旧版本请求409且currentVersion=2。四份实际回执再经生产Web同版解码器全部符合预期；将成功回执requestId改回null的负对照仍被拒绝。证据 `http-envelopes.json`、`consumer-verification.json`、14份JUnit XML；这是固定候选测试边界，不是线上验收。
- 问答202创建/重试覆盖历史null和旧请求编号，复用同一HTTP适配器；已有授权、输入语法、幂等/版本等回归保留。跨书UI恢复沿用Web452精确源码证据，本轮未改Web、不重复构建。
- 同Run不可变制品 `/home/isp/state/cyf-archive-progress-envelope-20261106/api-artifact.tgz`，224028830 bytes，SHA256 `226ba60c2593f755ce9465e815b3fedea0f2cc7a61e7547b7fb7656df3252ea6`；内含JAR SHA256 `34f03604e089fed64431743e0daf174e462aeddd1894e8cc9d845a017b504e7a`。receipt/source/metadata/provenance摘要闭包已验证，见`artifact-verified.json`。
- 发布边界：本轮没有安装、重启或数据库写入；后端候选和前端1.16.115均待用户发布授权。授权后复用API539/Web452制品，不因下载/安装再构建。根仓/API主工作区的其他任务修改保持原样；仅清理本任务干净worktree，远端源码和证据保留。
- 稳定知识回写 `docs/juyiting-runbook.md` 与 `specs/archive-pavilion-reader-mvp/design.md`；根文档保留工作区修改，不混入根仓既有其他任务改动提交。

### 2026-11-06 用户授权发布（执行中）
- 用户明确“发布”，固定API539 / 1.1.36-SNAPSHOT / b7b4cf7e8a与Web452 / 1.16.115 / f3cd173b42c3；实时查询两Run仍SUCCESS，复用已验证制品，不新建Flow Run。
- 发布前核对API现行528、Web现行451，保存前值及前端入口备份；先API事务安装/健康，再Web资源与入口，随后真实登录会话核验保存/切书。只沿已安装受控工具，不本机源码构建、不改数据库业务规则或Runtime。
- 本次安装及验收证据 `/home/isp/state/cyf-archive-progress-envelope-20261106/release`；API恢复沿安装器backup/record，Web旧入口备份 `/home/isp/baks/cyf-archive-progress-release-20261106`，旧哈希资源由安装器保留。

### 2026-11-06 发布及线上验收完成（07:27 CST核对）
- API539 / 1.1.36-SNAPSHOT / `b7b4cf7e8ab6b7a39f1e010bb4133b7458e51b17`与Web452 / 1.16.115 / `f3cd173b42c36fb493724214ac1f324d5646ac7c`已由主机受控安装器顺序安装成功；未新建Flow Run、未本机源码构建。API PID709211，canonical JAR SHA256 `34f03604e089fed64431743e0daf174e462aeddd1894e8cc9d845a017b504e7a`，健康UP，canonical路径8项检查通过。
- API安装器保留旧JAR备份 `/var/lib/cyf-api-flow/backups/20261105T231351Z-34f03604e089fed64431743e0daf174e462aeddd1894e8cc9d845a017b504e7a-708335.jar`（文件名绑定本次candidate，不代表备份内容为candidate）；record.previous_sha256为旧JAR摘要。既有F06安装钩子核验两张表均existing_equivalent，无本任务手工DDL/业务数据迁移；E05未启用，Runtime未重启。
- Web 612个安装文件逐个摘要匹配；公网index及入口/含典籍代码的JuyiHallEntry JS/CSS共5资源HTTP200且字节摘要匹配。前值和可恢复入口保留在本次release目录与`/home/isp/baks/cyf-archive-progress-release-20261106`。
- 真实全新登录浏览器：三国连续点击保存、关闭、切水浒保存、再切回三国保存/关闭，共7次UI PUT全部200/E0；每个body/header requestId均匹配本次请求，返回version=expectedVersion+1；两书均实际显示“已保存”、无错误，正文和切书正常。
- 关闭三国阅读器时既有可视段落捕获将位置落至p68，本次测试结束后核对无并发写入，通过标准CAS API恢复原p70，未直接SQL回写/回滚版本；同键新requestId重放验证返回相同业务结果且不重复更新。两书最终位置/state与测试前完全一致，三国version9→15、水浒207→209（保留真实保存事实）。无书签/手札修改。
- 证据：`release/installed-verification.json`、`business-verification.json`、`location-restore-and-replay.json`、`progress-*-before/final.json`、`browser/archive-wire.jsonl`及截图。测试浏览器/profile已清理；根仓其他任务修改保持不动。本节替代前述“未发布”作为本次版本的当前线上状态，不改写历史验证边界。

### 2026-11-06 阅读界面文字操作改图标（实施中）
- Owner本任务Codex；范围仅Web阅读命令及工具栏布局/可访问性，目录章节名称、书签定位信息和书架主动作保留内容文字；API/Runtime/进度/笔记业务不改，不授权发布。
- Web base/source origin/develop `f3cd173b42c36fb493724214ac1f324d5646ac7c` / tree `3e083f6c96e7501750db451dfae4e76e524c2b8d`（实时fetch核对），生产Web452同源码；API线上539。主Web工作区旧HEAD ca22ac2且存在无关dirty文件，无法安全混合基线，使用最少独立worktree `/home/isp/wsps/worktrees/archive-reader-icons-20261106` / `codex/archive-reader-icons-20261106`。
- 原型先行：唯一入口 `/home/isp/wsps/cyf/web/prototypes/juyiting/index.html#reader`，定向更新现有renderReader及reader CSS/规格；不覆盖原型其他脏改，候选只带同范围改动。复用18786正确原型服务，HTTP可达；桌面/窄屏/禁用/手札预览后改产品。
- 最早验证：现有archive-reader.test.js的真实组件夹具与93项基线测试，新增图标名称/操作触发/状态回归；正式测试构建Flow4403172，总Run≤600s。证据 `/home/isp/state/cyf-archive-reader-icons-20261106`。

#### 图标实现自检（2026-11-06 09:28 CST）
- 09:26重新fetch发现远端develop已前进至`a01d7eb3529a17f2e3f2f49939041215e8278eab`，保留其议事历史修改后rebase，候选Web1.16.116 / `ab54067`。无发布/主机安装操作，不以07:27线上基线推定当前其他任务状态。
- 实际ArchiveReader组件定向95项通过（93基线+2新回归），覆盖5个页脚图标、中文名称/提示、禁用、引用、翻回、书签跳转、继续阅读与笔记保存pending。更新原布局断言及引用按钮定位，不修改业务处理。新旧组合依赖下重跑95项仍通过。
- 真实SFC+CSS轻量Vite fixture预览（仅注入现有测试makeApi，无生产读写），375×812与320×640全部5按钮44×44同排、无横溢出；1440×1000截图已保存。唯一原型reader页同步，修正原型装饰器会移除显式引用/保存图标的问题；main原型既有semantic-controls.js保留自身归属，仅增加显式reader-icon-button不重装饰一行。
- 证据：`/home/isp/state/cyf-archive-reader-icons-20261106/local-tests-integrated.log`、`prototype-browser/product-{mobile,320,desktop}.png`。fixture只验证界面与现有消费者，不当作真实保存业务验收；临时源文件与服务收尾清理。
- 本机ESLint存在基线压缩SVG格式/既有测试风格报错，未全文件重排或扩大修改；正式测试/构建尚待Flow。准备Flow时检测他人4403172/454 RUNNING，未覆盖其配置、未取消其Run；等待其终态后复查再触发本任务固定候选。

#### 固定候选与云端验证（2026-11-06 09:33 CST）
- 最终候选`f69891f0e34c2d60a8b8788bbb1b17742ce7b34d` / tree `f21610248927b7aeffe295f14c194860cf3d91c6` / Web1.16.116。两处新增button属性缩进/顺序已收口；ESLint当前/基线均87 errors、23 warnings（组件），测试均2个既有错误，无新增lint问题；不宣称全量lint通过。
- 发现独立Teleport阅读器不保留.archive-reader祖先，图标尺寸责任选择器改为实际.fullscreen内控件，避免只在嵌入模式生效。正式前最后定向测试95项通过；实际fixture浏览器分别核对嵌入5按钮和Teleport独立4按钮（原独立模式无引用起草），1440/390/375/320/844横屏均44px同排、无横溢出，手札展开仍可达。证据`prototype-browser/product-layout-checks.json`、`product-standalone-checks.json`，不代表真实账号业务验收。
- 他人Run终态且原develop配置恢复后，CAS备份/更新/回读，仅CI的4403172/455于09:32启动；start返回UNKNOWN因source commit未就绪，保留真实returnedRunId455，只读核验，不重复启动。watch.cjs监视本任务Run并按570s预留受控取消、600s总上限执行；正式结论待终态与制品。
- 临时实际组件预览源保存在证据product-fixture，Vite18789与本任务浏览器/profile已清理；原18786服务归属其他任务，未停止。文档导航check-docs archive-agent-maintenance通过。

#### 图标改造完成，未发布（2026-11-06 09:37 CST）
- Web1.16.116，完整commit `f69891f0e34c2d60a8b8788bbb1b17742ce7b34d` / tree `f21610248927b7aeffe295f14c194860cf3d91c6`；实际最终集成父提交为`ea52a9e92d8e33b4ea5e104ace69aaa16e73b8cd`（含其他Owner现有fixture接线修复），前述a01d仅为中途fetch记录。正式测试后正常快进push develop，无force或覆盖其他修改。
- Flow4403172/455 **SUCCESS**：340测试全部通过，0失败/跳过；Vite生产构建、JavaScript扫描、上传均成功。API记录createTime→updateTime为112s，watch观察到终态约123s，均低于600s。start UNKNOWN已通过返回Run455、分支及完整源码只读匹配消歧，证据`release/web-start-reconciled.json`，未重复启动。
- 同Run制品108212804 bytes，SHA256 `bc94f43d0528b2f35644961bce13f5dfb14e7c765e45db3a228371b2c99758e1`；下载后核对commit/tree/version/Run及全部612个dist文件摘要，测试报告340PASS。证据`release/web-verified.json`、`web-mochawesome.json`、`web-artifact.json`及原始tgz，状态verified_not_deployed。流水线原develop/无自动触发配置已CAS恢复并readback。
- 稳定实现说明同步reader设计与juyiting-runbook；本次无API/Runtime变动，无业务数据写入、安装或重启，未发布。后续获发布授权可复用455制品，不因下载/安装再构建。主Web旧HEAD/脏改及根gitlink不强制同步，以免覆盖无关任务；本任务干净worktree完成后清理，源码已在远端develop保存。

#### 阅读图标用户授权发布（2026-11-06 09:42 CST，执行中）
- 用户明确“发布”，固定已验证Web455 / 1.16.116 / commit f69891f0e34c2d60a8b8788bbb1b17742ce7b34d、tree f21610248927b7aeffe295f14c194860cf3d91c6，实时查询455仍SUCCESS，重新完整核验原制品/340PASS/612文件。仅Web，不动API539/Runtime，不新增构建Run。
- 当前Web record452/1.16.115、develop仍为本候选，锁未见占用；安装沿/usr/local/sbin/cyf-web-flow-deploy，备份旧入口/静态文件与record到本任务独立备份，资产优先/index最后，旧哈希资源不清理。证据installation/；安装、线上字节和真实阅读页核验分别记录。

#### 发布实页发现窄容器溢出，定向修正（2026-11-06，执行中）
- 116/455已安装且612文件及公网5资源摘要匹配，API record未变；真实登录页在1440/390/375宽度均图标正确，320px视口下父浮层仅238px，内部可用222px：原最小gap4加五个44px按钮需要236px，最后书签右缘溢出6px。此前全视口fixture没覆盖该宿主宽度，不将其通过当作真实界面全通过。
- 按职责仅收口reader toolbar gap=0，让既有space-between分配余量；保持44px点击区和宿主布局，不新增设备特殊分支。原型先同步；补实际嵌入最小容器回归断言。该源码变化需要新的固定Flow候选117，不是因安装/缓存等待重复构建。
- 实页检查仅打开/缩放/返回三国、未写笔记/书签/问答；视口捕获产生2次正常进度保存（17→19，均200），按本任务原位置/当前版本做标准CAS恢复，不SQL回滚、不覆盖其他并发保存。水浒214未变。正式验收待117，不把116安装成功宣称全项完成。
- 117候选`ea6f83801b053cec1eef9883048582e93984cb2a` / tree `79d8f76fce46a7b14ababa495b08931c8fa3a1a4`，本机95项通过；Flow4403172/457固定源码，仅CI测试/构建/上传，原配置已备份/CAS回读。UNKNOWN start保留returnedRunId457，只读跟踪，不重复启动。首次实页捕获后的三国位置已用标准API恢复，version19→20；水浒未写入。

#### 2026-11-06 阅读器图标发布与验收完成（10:02 CST后收口）
- 最终线上Web1.16.117 / commit `ea6f83801b053cec1eef9883048582e93984cb2a` / tree `79d8f76fce46a7b14ababa495b08931c8fa3a1a4`，Flow4403172/457 SUCCESS，340项测试通过，构建/扫描/上传完成，观测约129秒（低于600秒）。正常快进合入远端develop；UNKNOWN启动已按returnedRun457只读核对，无重复启动，流水线原develop配置CAS恢复并回读。
- 用户“发布”授权下，主机受控安装117成功；制品SHA256 `30f98cea2917f3b39166939cb699b805957538b64144a4f153e3ddc3572d8e04`。全部612个安装文件及公网入口/典籍JS/CSS共5项摘要匹配，现行record为457/1.16.117/online_verified。API539记录未变，未发布API/Runtime。116为中间安装，不是最终版本。
- 真实登录生产UI复核1440/390/375/320宽度：5个页脚图标44×44同排，reader frame无横溢出；320视口实际222px内容区以gap=0、space-between分配余量。中文名称/title、空文字/SVG、笔记展开及保存图标均通过。关闭全局新手引导后重拍并目视检查320截图；不是仅凭被遮盖页面的DOM断言验收。
- 最终117验收以before117快照为准：正常UI进度保存均200，关闭后核对自身连续CAS链与最新GET，再经标准API恢复测试前阅读位置，三国version20→24，水浒214未变；两书最终location/state完全一致，不回滚真实版本、不SQL写入，未写笔记/书签/问答。
- 最终证据：`/home/isp/state/cyf-archive-reader-icons-20261106/release-117`、`installation-117/installed-verification.json`、`installation/browser/ui-verification.json`、`final-business-verification.json`及清晰截图。117前值备份`/home/isp/baks/cyf-reader-icons-narrow-release-20261106`，保留116/115历史证据与恢复资料。
- 本任务浏览器/profile及干净worktree已清理，其他任务18786原型服务与主工作区脏改未动。此节替代前述候选/待验收状态；没有为安装、截图或收口重复构建。

### 2026-11-06 微信嵌入阅读器工具栏一致性（实施中）
- Owner本任务Codex；目标仅嵌入阅读器目录/笔记靠右及引用/继续阅读去旧框，非目标为API/Runtime、业务保存或独立阅读器胶囊保护。用户本轮未授权新版本安装。
- 实时fetch origin/develop为ea6f83801b053cec1eef9883048582e93984cb2a / tree79d8f76fce46a7b14ababa495b08931c8fa3a1a4；生产record457/1.16.117。主Web工作区仍有无关dirty，复用隔离策略，唯一worktree `/home/isp/wsps/worktrees/archive-reader-toolbar-alignment-20261106` / `codex/archive-reader-toolbar-alignment-20261106`。
- 根因：嵌入frame错误继承has-reader-capsule的112px header padding；引用/继续阅读漏接hall-tool，保留旧背景/边框。责任在阅读器展示，不联动API/宿主壳或修改全局控件。
- 原型先行：唯一入口web/prototypes/juyiting/index.html#reader，显式工具按钮统一透明底/透明边，header actions右对齐；产品仅限制胶囊保护用于独立阅读器并补hall-tool。最早回归既有archive-reader.test.js胶囊矩阵/图标动作；浏览器需带微信UA/宿主标记和真实hall-controls CSS，不能仅全视口几何代替视觉验收。

- 10:47 CST复查远端develop已更新至da86067（他人历史投影刷新改动，版本118）；本任务rebase保留其变化并升119，固定249cf90，非覆盖旧develop。原型18786 HTTP200，414px离线页已核验5按钮透明底/透明边；产品真实SFC+hall-controls CSS夹具以微信UA、miniprogram标记及nativeOrientation路线，1440/414/390/375/320（额外窄宿主）检查目录/笔记距header右边4px、5按钮44px同排无框无溢出；独立竖屏/虚拟横屏仍112px胶囊保护。非真机/生产验收。
- 本机95项通过（含扩展既有18场景胶囊矩阵的嵌入断言与图标hall-tool回归）。Flow只读发现他人Run460 RUNNING，未覆盖配置/未取消。候选已推送本任务分支，源码集成验证及Flow准备继续，不使用他人证据冒充本候选。

- 集成候选Web1.16.119 / `249cf90e6289af90012d92ffed6d6645f94e1823` / tree `c14734a705fadda37f612451fd3cda7bec775617`；保留da86067基线，无API/Runtime联动。既有引用品牌底色局部覆盖一并删除，不继续堆叠失效样式。
- 他人Run460终态且develop配置恢复后，本任务CAS保存/更新/回读，Flow4403172/461于10:50 CST启动，仅测试/构建/扫描/上传。UNKNOWN返回保留returnedRun461并只读监控，不重复启动；600秒上限沿既有watch执行。
- 集成候选本机95项再次通过；最终SFC夹具带真实公共工具样式重跑通过，414/320截图已目视核对（无引导遮盖），测量header右间距4px，5按钮均透明边/透明底、44px。微信UA/标记模拟不是微信真机或线上验收，本轮未登录/读写生产业务数据。临时浏览器/profile和18789服务已停止，其他任务18786保持运行。证据`/home/isp/state/cyf-reader-toolbar-alignment-20261106`。

#### 微信阅读工具栏修复完成，未发布（2026-11-06 10:55 CST收口）
- Flow4403172/461 SUCCESS，340项测试0失败/跳过，构建/扫描/上传通过，启动上下文至终态观测约138秒。配置已CAS恢复原develop/no-autotrigger并回读。612个制品文件摘要及来源闭包匹配；SHA256 `3113f6f0561e0e65357231fe5f136e2fcd62dd0fd45df26eaae7dbe9a7a4a0da`，绑定源码249cf90（不是后续集成HEAD）。
- 合入前远端新增4a49441，仅修改既有babao样式测试，仍把引用品牌底色视为约定，现已按用户无框要求更新两条实际受影响断言。保留该他人提交、正常merge并自检103项通过，最终集成`26373d2e01beeff6d0b4a63a3f4ea6fac1853ea8` / tree `5ccabb9ab69813714a66ecd00ab94e9311608c0c`已正常push develop。与Flow461的程序源文件完全相同，仅`tests/juyiting-babao-hall-style.test.js`不同，详见`integration.json`。103项为轻量本机定向反馈，不冒充新HEAD的云端构建证明。
- 未重复付费构建测试文件整合，也未安装/重启Web/API/Runtime。461制品始终标识249cf90；若后续授权选用该固定候选，可按其真实来源核对复用，不将其重标为26373d2制品或自动发布最新develop。生产现状本任务没有改动。
- 修复保留独立阅读器微信竖屏/旋转胶囊避让，只移除嵌入阅读器重复预留；引用/继续阅读直接接入既有hall-tool，删除无效品牌色覆盖，无微信专用CSS补丁或全局控件改造。原型、夹具、云端、集成、线上状态分开记录；真机和发布后验证不在本轮证据范围。
- 证据根`/home/isp/state/cyf-reader-toolbar-alignment-20261106`；本任务临时预览/浏览器/profile清理完成，必要夹具快照归档，源码已推送后移除本任务干净worktree。主工作区dirty、其他任务服务及原生产备份未动。

#### 2026-11-06 微信阅读工具栏发布完成（11:03 CST核对）
- 用户明确“发布”，复用真实Flow4403172/461 SUCCESS固定制品，不新建Run、不本机源码构建。安装版本Web1.16.119 / commit `249cf90e6289af90012d92ffed6d6645f94e1823` / tree `c14734a705fadda37f612451fd3cda7bec775617` / SHA256 `3113f6f0561e0e65357231fe5f136e2fcd62dd0fd45df26eaae7dbe9a7a4a0da`。远端develop26373d2仅额外改样式测试，未将461制品重标其源码。
- 发布前实时核对461仍SUCCESS，340项测试/构建/扫描/上传及完整612文件来源摘要闭包通过。主机受控安装器exit0，record=461/1.16.119/online_verified；612个安装文件及公网index/入口/典籍JS/CSS共5项摘要匹配。备份前值1.16.117/457共612文件与record，恢复目录`/home/isp/baks/cyf-reader-toolbar-alignment-release-20261106`；旧哈希资源保留。API现行564记录发布前后未变，本次无API/Runtime安装或重启。
- 真实登录生产页，无网络mock，以微信UA/miniprogram宿主标记/nativeOrientation=portrait模拟入口：1440/414/390/375/320宽度下目录/笔记距header右边4px、不重复112px避让；5页脚按钮均透明底/透明边、44×44同排无横溢出。中文名称与图标保留，笔记展开/关闭正常，414截图已目视核对，无新手引导遮盖。此为生产网页+模拟微信环境，不冒充微信真机验收；独立阅读器胶囊保护沿既有定向/夹具证据。
- 本次只打开/缩放/关闭三国、展开/关闭笔记，未点引用/创建书签/保存笔记/发问答。3次UI进度保存均HTTP200/E0且requestId正确、version递增；关闭后核对本任务连续写链和fresh GET，再以标准CAS恢复原位置，追加1次200保存。三国version30→34，水浒241不变，最终两书location/state与本轮最新before快照一致；不SQL回滚或覆盖并发更新。
- 安装/校验/业务证据`/home/isp/state/cyf-reader-toolbar-alignment-20261106/installation`，含install-plan/result/log、installed-verification、browser/ui-verification、final-business-verification和截图；浏览器/profile已清理，无新增worktree，其他任务服务/dirty内容未动。本节替代前述“未发布”，不改写各阶段源码/测试证据边界。
