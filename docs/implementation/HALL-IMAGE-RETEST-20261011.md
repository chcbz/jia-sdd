## 2026-10-11 正常图片流程最终结果：已发布、事项445验收完成

核对时间：2026-10-11T21:23:05.881231+08:00。本段为当前结果，下文分时记录保留为历史证据，不再作为待办。按用户收紧范围，只闭合新事项正常流程，不扩旧440/444恢复。

- **真实链路通过**：本人chcbz → 新建普通事项445 → 点将本人吴用 → 会话1760458005654生成蓝鸟PNG → 同会话以首图asset/revision改成红鸟 → 两图真实鉴权预览/下载与摘要核验 → 红图正式验收 → 刷新重进仍“验收完成”。生图/改图实际在API1.14.6/Web1.14.7完成；最后必要修复发布后，API1.14.7/Web1.14.8验收及两图重新读取通过，不冒称修复后再次调用Provider。
- 最后唯一正常验收POST HTTP200：operation `fin_5b5ce702081da3c4d5317f92a859ea3cc6f3434634d996562fc77e13cea6daea`，`completed / stateVersion5 / TASK_COMPLETED`；delivery `finalization_delivery_e8954765d72d203ece34bcaeab01283aebbd5e857e5a26a6c6ff9279698822d0`，`accepted`；任务GET为`completed / taskVersion4`。selectedOutputs仅红图，SHA `e067236a626a0fdc412fa6e50d4e712f197c688c1d37270e4ba60c48e043323e`。旧失败operation终态及无delivery事实保留，不复活、不改DB。
- 页面真实“确认验收”点击成功；一次整页刷新后从“已完成”事项→“查看历史成果”重新进入，自动GET恢复同回执，仍显示“验收完成”，无重复POST，验收按钮不可再次提交。新浏览器唯一获准业务写就是该验收，无重新创建/点将/Provider调用；鉴权下载证明为GET实际PNG字节，不冒充点击下载按钮。
- **发布对应**：API1.14.7 `cf1402727466e1e51db0860200dc178eab2096c4` / tree `136ebfbcf3d4e354d5a82bc3598f035da4ddb676`，原本地build `cyf-hall-finalization-api-release-20261011-xe4w6ge8`，正式97PASS、分层及fresh JAR通过。原capture/admit/inspect/installer顺序安装verified/exit0/healthUP；canonical JAR SHA `333d525e2aa4a9cbde138ccb7507d1d55f264190d09332863a35f277624b8c57`，PID2436355/start33601049/cwd实体目录，F06/E05三表existing_equivalent，无新DDL。Web1.14.8 `621b87a1b977e5c8fd0ef9cd22b068d7d0622b42` / tree `7fd5366e083af414738cd7c06dd323a13556601e`，Flow4403172/201正式2921PASS/2既有pending/0fail，同Run制品与线上匹配，Flow已恢复无触发CI-only。统一Runtime PID2341655未变。
- **内容质量保留项**：红鸟替换蓝鸟、构图与树枝保留；红图背景实际透明（Canvas边角alpha0），没有严格保留要求的白底。结论是管线与验收闭环通过，不是所有视觉约束完全通过；按用户要求不为此扩修或再生图。
- 发布仅回收本线程关闭使用且已逐SHA/size核实的raw冗余和Owner明确白名单编译目录，保留完整admitted制品、测试XML/日志/输入/证明/备份/incoming和共享缓存；未清他人文件。Main控制面复用preparer时仅更新当前固定source pins；健康JSON实际是status.code=UP，最初诊断按字符串断言不匹配，修正读取后通过，非应用健康失败。

最终证据：`/var/tmp/cyf-image444-edit-fix-20261011-hER21X/business-acceptance-final.json`。同目录`api-finalization-online-readback.json`、`api-finalization-install.stdout.json`、`web-finalization-release/online-verification.json`；UI与请求回执见`browser-finalization/task445-successful-finalization.json`、`task445-refresh-finalization-restored.json/.png`、`task445-after-completion-images-readable.json`、`task445-accepted-red-preview.png`。首次生图/改图证据仍在同目录`browser/`。主机路径契约8PASS；仅验本账号吴用事项445，不将本结果扩为所有角色/账号/异常恢复通过。

## 2026-10-11 21:00 最小修复发布进展（业务仍未完成）

Web1.14.8/621b87a1/tree7fd5366已实际发布：Flow201全套2921PASS/2既有pending/0fail，部署70901852一批一台healthy，364安装文件及11公网关键资源摘要一致；流水线已恢复原CI-only配置。Main只修改媒体验收回执null槽位读取，保持原请求严格。API原Owner修复cf140272/tree136ebfbc已push，正式固定构建成功，尚在制品交付，不冒称后端新版本已上线。

本机空间通过同线程已accepted的HALL-ROUND-API-RELEASE-20261011中两份已消费raw副本定向回收480521793bytes：逐SHA/size核对完整admitted及tar内JAR、确认无Owner/无运行引用，保留全部admitted/证据/测试/源码/备份/incoming/共享缓存；不是清理其他聊天文件。原本批Web201消费缓存106610046bytes也已在完整线上核验后回收，云端同Run原制品及manifest留存。证据位于本轮主目录closed-own-round-raw-cleanup-result.json和web-finalization-release/consumed-download-cleanup.json。

## 正常验收末端断点与最小补齐（2026-10-11 20:42）

事项445生图、基于首图编辑、前后两张PNG鉴权预览下载均通过。编辑图保持原构图且蓝鸟改为红色，1370×1148，1345192bytes，SHA e067236a626a0fdc412fa6e50d4e712f197c688c1d37270e4ba60c48e043323e；`replaces`精确指首图。内容质量另记：改图背景实际透明（真实Canvas边角alpha=0），未严格保留白底；不将此内容偏差报告为完全符合要求，不为此重投Provider或扩修。

正常UI最终一次POST失败：HTTP404/FINALIZATION_SOURCE_UNAVAILABLE，operation fin_9c1a75fe76874a1459af99dd87e661462c666b1e7c982a0218ddc45c9d83d867，failed/PROMOTING/retryable=false，无delivery，事项仍assigned/version1。只读恢复已确定终态，无盲重试。

冻结本次唯一正常路径修复：
- API原Owner Turing：基线1e24e63/tree d52aa623，原独立worktree。`ChatSelectedOutputFinalizationService.resolve`仍要求link RUNNING，与request/step及资产投影均OUTPUT_COMMITTED矛盾。Main实际精确scope只读查询证实OUTPUT_COMMITTED唯一行/旧RUNNING零行。只统一此消费终态并完善现有回归，保留所有scope/grant/hash/事务约束；不做旧失败恢复、状态回写或schema改动。计划API1.14.7。
- Web唯一Owner Main：基线d2c5e5d/tree bf51fbc9，web/develop干净。`useHallBountyFinalization.js`媒体回执读取拒绝实际serializer的messageSource:null（已用真实回执定向复现）。在既有回执union支持这一null槽位，非null混合/未知字段仍拒绝，请求体仍严格；现有finalization测试覆盖真实nullable序列化、摘要/身份拒绝、成功/只读恢复。计划Web1.14.8，不改接口/其他UI。
- 正式验证/版本化发布沿用原前端Flow4403172、后端固定本地制品。发布后使用445已有可读红鸟成果从全新登录会话正常UI发起一次新的验收意图（原失败operation保留且已证实无delivery），不复活原终态、不重复生图/扣费；若该路径不成立先核原因，不用DB绕过。

证据入口：同批browser/task445-finalization-ui-writes.json、task445-finalization-readback.json、task445-finalization-source-committed.sql/.tsv、task445-finalization-source-old-running-predicate.sql/.tsv、task445-frontend-receipt-contract.json。本文阶段不是业务完成。

## 当前正常流程验收（2026-10-11 20:30）

用户收紧后不再扩展旧444失败恢复。前端1.14.7（d2c5e5d/Flow200，2919通过）和后端1.14.6（1e24e63/本地build，99通过）已通过原入口实际发布；Main回读canonical JAR摘要匹配，新API PID2411451/start33301737，F06/E05三表existing_equivalent，Runtime仍PID2341655。本次没有新DDL。

真实UI新建唯一普通事项 **445**（HTTP201），一次点将本人吴用（HTTP200）。新会话 **1760458005654**；初轮CHAT已发布ACTION_REQUEST，generate-image子EXECUTE已RUNNING。此时还不能称生图/改图/业务验收通过。没有操作旧444或其他用户事项。

证据仍沿用 `/var/tmp/cyf-image444-edit-fix-20261011-hER21X`（目录名不是当前受测事项号），主入口 `release-intent.json`、`api-online-readback.json`、`web-release/online-verification.json`、`browser/task445-ui-writes.json`、`browser/task445-generate-outcome.json`。下一步：首图真实PNG与鉴权读取→同会话基于首图改红鸟→最终成果验收。

# 当前版本图片流程复验（2026-10-11）

## 2026-10-11 20:04 用户收紧范围：优先新事项正常流程

用户明确不再处理边缘恢复场景，允许新事项验收。后端仅完成正常生图/改图必需的源图OUTPUT_COMMITTED授权及typed read锁定读取事务修复，保留必要回归，不扩旧DEAD恢复。已经启动的Web1.14.7/Flow200正常收尾，不再追加前端改动。发布后新建一个普通事项，单张生图→基于原图改图→真实预览/鉴权下载→最终验收。旧444及首图/失败记录保留，不重投、不复活；下文旧444继续编辑计划已被本段替代。新事项尚未创建，正常流程尚未验收。

## 2026-10-11 19:43 新事项444实测结果：首图通过，改图未通过

**发布已完成，不是等待发布。端到端尚未通过，不验收完成事项。**

### 已通过
- API1.14.5原installer exit0，`CYF_API_FLOW_INSTALL=PASS`、HEALTH=UP，线上PID2386561/start32959402，JAR SHA `8819346db25bd7952a96226bdc3ec777cf280cf19e81b4049fc79fd53d1d07b4`与同批制品一致。F06/E05三表均existing_equivalent，无新建表；18项发布后只读投影退出0，当前应用自有JDBC principal回读通过。路径契约8项通过。统一Runtime未重启，Web仍1.14.6/Run199。
- 发布后测试浏览器原JWT尚未到期但GET返回401，已通过正常登录重建本人测试会话；没有将此现象归因为过期或确定的密钥问题。只操作独占浏览器。
- 真实UI事项444点将吴用一次，HTTP200；原key `19b26068-3815-47dd-9156-ccd92d6e8d0e`。bootstrap ADMITTED，conversation `1760458005641`。首轮CHAT返回generate-image ACTION_REQUEST，经既有ORDINARY_ACTION通道创建EXECUTE。
- 首图request `cf72507bdeaff60023698fe91e9048fb9e82910ff23b106601c06ad1cbeb9ce4` / step `1ebdd22e3e6c847c6033270e618000d6c3d50d564be9c7ae6fcf397efc691ba0` / execution `pwe_28cb0c083618093cdc8b914adb0dd0b1f260bb31e8d7730d81e10f0434d9`均OUTPUT_COMMITTED；asset `ast_31207f6fd9021381eb0265388dbfb1a6` revision1。
- PNG1374×1145、2045835bytes、SHA `27f4925e8211bb77fc30d34e7cc37978740426f86946b4ba98484c6e03acbe8c`；浏览器真实预览可见白底蓝鸟停树枝，无文字。本人鉴权previewUrl/downloadUrl均200、PNG签名及实际解码通过、字节/摘要与output/asset一致。下载验证为真实鉴权GET，不冒充下载按钮点击；没有独立调用Provider/image_gen。

### 改图受理与断点
- 首次UI点击发送在HTTP写入前提示“当前成果索引尚未核对”；无discussion POST。索引读取完成后再次点击，产生唯一固定body/key，引用上述首图asset/revision及首轮delivery parent。Main对该原UI请求核定单次许可后原样发送，未修改body/替换响应。
- 唯一改图POST202，key `mmd-typed-discussion-b12ce495-23b0-444b-9ca8-04e82facc479`；request `mmd-typed-request_aa94d17729c7999d1eb64dc7aaf7ae0422bfa940`，turn `turn_5e5c3cc1af0c63f2ac34e59dcd763bcf4ab18279`。CHAT PUBLISHED，持久ACTION_REQUEST=edit-image，sourceRef绑定首图；不是模型没理解改图。
- 该action `act_11e731895cb30471f97deafa853896232278c7d1`只尝试一次，DEAD / `ACTION_REQUEST_CHANGED`；无edit EXECUTE子请求/改图图片。typed-outcome GET返回503 `TYPED_DELIBERATION_UNAVAILABLE`。未重投、未强行改DB恢复DEAD、未换旧接口绕过；task仍assigned/version1，无finalization写。

### 已实证根因与后续修复落点（尚未编码）
1. **已完成首图被旧状态谓词排除。** API `chat/jia-chat-mapper/src/main/java/cn/jia/chat/archive/conversation/JdbcChatConversationArchiveStore.java:198`仍要求`l.state='RUNNING'`，但首图link已OUTPUT_COMMITTED。Main复用原查询的完整scope/身份/会话/asset/revision/target条件，仅执行READ ONLY查询：原谓词0行，仅换OUTPUT_COMMITTED谓词后精确1行，其余字段一致。`ChatConversationAssetSourceResolver.resolveAction:49–53`因此拿不到源，`ChatActionExecutionService.prepare`转Rejected，原dispatch标DEAD。应统一现行OUTPUT_COMMITTED语义并补真实JDBC状态回归，不增加RUNNING兼容OR、不改业务数据凑状态。
2. **503暂只定位到代码调用链，不能宣称实际异常已抓到。** `ChatTypedDeliberationService.java:105`只读事务→`ChatActionFinalService.verifyDeliveryRelation/deliveryTargets`→`PersonalWorkspaceExecutionServiceImpl.java:553–568`锁根/执行/产物的读取。与需要锁定读取的事务语义冲突是强候选；需真实Spring事务回归核实并保留权限/锁顺序，不简单删锁或伪造FAILED响应。Turing已接回只读诊断，不擅自启动新发布。
3. 首次改图发送被索引并发读取挡住：`useHallBountyRequestCatalog.js:17`在loading时直接返回false，`useHallTypedDeliberation.js:223–225`将其视为准备失败。当前实测第二次点击受理；记录为需定向复现的并发体验缺口，尚不把本次具体竞争时序当作已全量证明。另EXECUTE请求被读取typed-outcome返回404，但现有适配将404处理为非typed；不将该404冒充本次改图失败根因。

独占测试浏览器已关闭，未取消任何服务端执行、未操作用户in-app页面。最终结构化回执`business-result.json`：3个请求（首轮CHAT、唯一生图EXECUTE、改图CHAT），唯一改图discussion POST202，无改图执行子请求。

### 证据
统一目录 `/var/tmp/cyf-image440-generate-edit-20261011-Xvd8n9`：`api-online-readback.json`、`api-install.stdout.json`、`api-postinstall/`；`browser/point444-write-and-ui.json`、`point444-current.json`、`task444-generate-completed-catalog.json`、`task444-generate-completed-outcome.json`、`task444-generated-outputs.json`、`task444-generated-asset.json`、`task444-generated-bytes.json`、`task444-generated.png`、`task444-first-image.png`；`task444-edit-held.json/held2.json`、`task444-edit-write.json`、`task444-edit-readonly.tsv`、`task444-edit-source-readonly.tsv`、`source-state-readback.json`与两份READ ONLY SQL、`task444-final-catalog.json`、`task444-final-task.json`、`task444-edit-blocked.png`。下文按时间保留旧结论，不取代本段当前状态。

## 2026-10-11 19:24 发布接续（业务尚未验收）

- API1.14.5：commit `37e97f8579474c64865551e51a8d2b4906e66ebe` / tree `7afae96140342893b5a7187a840be3a8b3361575`，同批本地130测试通过、分层/fresh JAR通过，原admission成功。未重复构建。
- prepare首次失败已归因：上一批配置回执采用`currentApiConfig`，复制的准备脚本却读取`appliedConfigurationFiles`。当前API配置SHA仍`298d5a260665c1374d1154dbfe8f0861c30f5e066bc19b1ce973b6876ad0a046`，与已安装1.14.4及其已校验前任1.14.3证明完全一致；不是线上配置漂移。仅修本批临时preparer读取；沿原安装记录的checked ref链核对启动属性/进程override/旧新JAR默认配置，不更改线上配置、不伪造历史回执。
- 新r2 decision SHA `28b9968e7fe98d4d7914faf199e6c24bd7d6ad64ad5e89f1a69f994e77a5ea6f`；原`--local-inspect`已通过，`--local-install`进行中，尚未宣称上线。保留首次失败现场。
- Owner书面关闭原副本使用后，Main逐SHA/size校验admitted不可变副本，仅清本批producer tgz与build JAR两份冗余，释放480523300bytes；保留唯一admitted源及全部日志/证明，无历史或他人清理。回执`redundant-copy-cleanup.json`。

## 验收事项调整（2026-10-11 19:04）

19:12:19 已真实UI创建新事项444，creation-operations/v2 HTTP201；只创建一次，task open/version0，吴用尚未点将。API仍1.14.4，创建并不算1.14.5发布后验收。独占浏览器已选中吴用，等待已验证新制品部署后再点击“点将并议事”；其他用户新建441–443不是本轮事项，不操作。

用户允许“新起一个办事跑流程”。因此后续改为发布修复后新建一个普通无悬赏资金事项，由本人吴用生成首图，再基于该首图改图一次，最后验收；下方“续跑原440”的计划已被本段替代，不再执行。API修复范围/Owner保持不变。

为防止修复发布后新旧事项同时生图，Main先核440仍无executionId、consent BOUND/version2，再经正式owner费用撤销接口一次POST成功，回读consent REVOKED/version3。未取消事项/重写数据库/重启或重投原请求，440历史证据保留。证据为本轮browser/old-consent-revoke-request.json、old-consent-revoke.json、old-consent-revoked-readback.json。后续新事项号以真实创建回执为准；新一轮生图+一次基于当前会话asset的EDIT_IMAGE授权来自本次连续指令，不额外生成第二组。

进一步源码核对：当前正常页面采用point-and-deliberate→CHAT typed ACTION_REQUEST→受控GENERATE_IMAGE/EDIT_IMAGE，后端admitOrdinaryAction按已有operator policy记录ORDINARY_ACTION授权，不能仅因旧controlled bridge.start/旧followup composable未接UI就断言当前正常页面无图片入口。新事项优先真实UI创建/吴用点将/自然语言改图；只有实际失效时才记录当前路径缺口，不把旧接口缺入口归为普通流程缺陷。前文18:31的纯UI尚未验证事实保留，但其“入口缺口”不是正常UI当前已确认故障。

## 修复及追加改图验收范围（2026-10-11 19:02）

用户已同意上文修复发布，并明确要求先生成图片再改图一次。API源码/正式本地制品Owner Turing（01a12aa0-9d7f-7f01-b0df-65fe4cd3fca9），Main负责生产安装与业务验收；基线fb8a43b0c1b8774582e520a809e5f52337198c25，计划API1.14.5。Web暂不变更；不将接口验收冒充UI全流程通过。

新增验收步骤（待执行，不代表通过）：
1. 固定源码修复生产/核验统一拼接；equal/distinct/null/empty、真正篡改拒绝；保留身份、事务、输入摘要回归及validateLayering。
2. 原installer版本化发布，续消费440原request/step/executionIntent，禁止新generate POST、另建事项或重写历史数据库内容。
3. 首图必须真实PNG，核对文件签名/可解码尺寸/摘要、产物/asset登记与执行OUTPUT_COMMITTED，验证预览和本人鉴权下载。不在改图前终结事项。
4. 同conversation1760458005623，引用首图固定assetId/revision和原requestId/stepId；改图要求：“把蓝色小鸟改为红色，保持白色背景、树枝和整体构图不变，只输出一张PNG”。现行preview→精确一次费用同意→EDIT_IMAGE受理，持久化各key/body/receipt，未知响应仅只读恢复。
5. 检查一次改图真实调用、首图作为输入的来源关系、新output/asset版本、新PNG摘要不同且视觉符合修改、原图仍可读取、新图预览和鉴权下载；成功后再做适当单图成果验收。
6. 任一层失败按真实阶段定位，不用重新生图/直接工具生图替代改图，不把CHAT回复算交付成功，不自动重复付费调用。

本轮证据目录：`/var/tmp/cyf-image440-generate-edit-20261011-Xvd8n9`。工作进行中。

## 精确费用授权后的实测（2026-10-11 18:25–18:31）

**本轮：授权/受控点将成功，图片执行未通过；根因已定位，非继续等用户授权。**

- 用户本轮明确“同意授权”，限原事项440、本人吴用一次外部生图。当前Web index SHA与1.14.6/Run199一致，API JAR SHA与1.14.4/fb8a43b0c1b8774582e520a809e5f52337198c25一致；Runtime仍PID2341655 active。未再次发布/迁移/重启，未新建事项、充值或操作其他账号。
- 当前UI只接普通point-and-deliberate；JuyiHall.vue:2290–2311仅引用controlled bridge恢复入口、未接start/费用确认。因此本次通过登录本人浏览器的正式API写入，不宣称纯UI端到端通过。
- `POST /agent/tasks/440/point-and-start-cost-consents` 201，consent `consent_d4c8223680f84832a7f1c7c4b7cbf69c`；受控point-and-start POST201，grant `grant_e1d8915e197041f0925e82817196d4b6`，consent BOUND/version2。两次写各一次，精确body/key已持久化；assignmentKey `443ff181-a20e-412a-af84-05f5d1189ee4`，没有重放或换key。
- 原任务assigned给吴用；bootstrap ADMITTED；conversation `1760458005623`，request `15be63e54ae2307a12484044e3f20b9577b1a978120279aa30cff93afdc5c668`，step `df59ee80357c1be59424313372c68607592a31948cd16d367b3036d53e6834d3`。最后读取仍PLANNING/step ADMITTED/link WAITING_ADMISSION，executionId=null。未创建Provider执行、未产生新PNG、未进行成果验收；不能报告生图成功。

### 已定位断点及最小修复落点

API `chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapAdmissionService.java:105–108`写入首轮内容时，title==description则去重。`ChatBountyExecutionCoordinator.java:121–128`核对时未去重，仍拼title+两个换行+description。实际440 requirement revision1的title==description，持久消息1784599长58字符，执行校验却要求118字符；requirementHash与快照完全相同。不是用户修改需求，也不是图片Provider超时或配置失效。

生产日志18:28:32、18:28:37两次`Exact requirement snapshot changed`，随后`Bounty execution relay halted on unchanged failure`。该relay停的是后台图片执行协调器，不是API/Runtime服务整体宕机；新的待入场图片步骤可能因此不再推进。Runtime日志另有generation mismatch，未将其归因为本次校验前阻塞。

后续修复：统一需求消息的唯一拼接规则供生产者/校验者使用，保留scope/hash/immutable snapshot核验；补title==description、不同、空/null以及真实篡改拒绝回归。不得改DB正文凑校验、关闭校验或重提付费请求。按项目后端本地固定源码发布修复后，原relay应续消费440同一个executionIntent；继续核对Provider单次调用、PNG、产物登记、预览和鉴权下载。当前仅诊断与证据落盘，尚未修改应用源码/发布修复，前端确认入口另列缺口。

证据：`/var/tmp/cyf-image440-consent-20261011-ltbWI5`，包含精确请求/回执、原key只读恢复、root-cause-proof.json、relay-failure.log、页面截图；本轮独占浏览器已关闭，未取消服务端任务。

## 发布后复核（2026-10-11 18:11）

Web1.14.6/Flow199、API1.14.4正式发布后，原task440真实能力GET再次HTTP200/E0，吴用GENERATE_IMAGE仍READY；`CONSENT_REQUIRED`、`newStart.eligible=false`，唯一门禁`OWNER_EXACT_CONSENT_REQUIRED`。本轮只读核对，没有额外任务、点将、同意写入或Provider调用。证据 `/var/tmp/cyf-hall-round-release-20261011-og8uDc/image-capability-440-after-release.json`。连续问答普通密议验收通过不能替代图片执行/PNG/下载验收。

## 后续处理（2026-10-11 17:35，区别于下文16:13初轮记录）

用户授权迁移配置并启用图片能力后，已将唯一配置根迁至`/home/isp/conf/cyf-agent-runtime-v1`，通过原installer安装Runtime1.0.2（源码`5b902c1bcd3efced9720e015e3b8240d39ce0738`）。静态subject的图片凭据读取入口已接通，按完整subject隔离；仅吴用启用。

原事项440的真实能力接口目前：`controlledExecution.state=READY`，`supportedOperations=[GENERATE_IMAGE]`，现行binding匹配。原`CONTROLLED_EXECUTION_DISABLED/OFFLINE`阻塞已解除；`executionAuthorization.state=CONSENT_REQUIRED`、`newStart.eligible=false`，唯一剩余业务门禁`OWNER_EXACT_CONSENT_REQUIRED`。本次授权用于主机迁移/能力启用，未替用户写入该事项的外部模型费用精确同意；没有实际Provider调用、新图片或产物验收。

证据：`/var/tmp/cyf-runtime-conf-image-20261011/capability-ready.json`、`final-readback.json`；实施/恢复见`handoffs/RUNTIME-CONF-IMAGE-20261011.md`。下文保留初轮事实，不再作为当前配置路径或当前能力状态的指令。

## 初轮结论与边界

**本轮结果：BLOCKED_PRECONDITION，不是生图成功，也不是Provider报错。**

2026-10-11 16:13–16:19 CST，用用户授权账号登录真实线上Web，UI仅新建一个普通、无悬赏资金事项 **440**（“生图复验20261011：…蓝色小鸟…PNG…”）。未重放task424或其他旧事项。新事项未点将、未调用模型/图片Provider、未产生新图片或验收。

实测版本：Web **1.14.5 / Flow4403172 Run197 / 21ded98d9b642eefa683403fd6068933186d7865**，API **1.14.3 / 33e2344a2af02bb908a20bec1125ab7c23e8d00d**，运行中的统一Runtime实体目录 **jyt-control-receipts-20261011-aa6b96aa983f**（PID2069517）。后续开发候选不冒充此次受测版本。

## 真实接口结果

对新task440，使用浏览器真实owner JWT读取：

`GET /agent/tasks/440/point-and-start-controlled-image-capability?targetAgentId=<本人Agent>`

吴用、林冲、公孙胜三位当前online本人Agent均HTTP200、业务E0，且均返回：

```json
{
  "serverLane": {"state":"READY","blockingReasons":[]},
  "controlledExecution": {"state":"UNAVAILABLE","transport":null,"schemaVersion":null,"supportedOperations":[]},
  "providerBinding": null,
  "executionAuthorization": {"state":"UNAVAILABLE","paidExecutionAuthorized":false},
  "newStart": {"eligible":false,"blockingReasons":["CONTROLLED_EXECUTION_DISABLED","OPERATOR_POLICY_UNAVAILABLE"]},
  "requestedOperations": []
}
```

该接口只读，不授权执行。既然前置声明disabled，不能绕过检查直接调用外部生图工具“证明产品跑通”。`OPERATOR_POLICY_UNAVAILABLE`此时不能单独解释为服务端没有配置：源码仅在Runtime声明READY时才读取operator policy；当前吴用的既有operator policy仍存在。

## 已确认根因范围

1. 实际进程所在release具有controlled-image执行模块，不是“模块文件根本没打包”。
2. `/etc/cyf-agent-runtime-v1/unified-profiles/wuyong.json` 没有controlled-image启用/endpoint/key-env/model/binding/ledger字段；SHA256为`a04618f09c2ec10fff78c44441c434fa410e4567c4122b6d41c76879508fcb5f`。
3. 用**安装release内的纯配置解析模块**读取该profile，实际解析为`controlledImageHttpEnabled:false`，其他上述字段空；`resolveControlledImageHttpConfig`返回`{"enabled":false}`。未读取/输出密钥、未实例化执行器、未调用网络Provider。
4. 源码链：`conf/cyf-agent-runtime-v1/lib/manifest.mjs:123`读取精确profile；`conf/codex-ws-agent/agent-client.mjs:6423`以isolated模式标准化，没有其他Agent旧配置fallback；同文件`:5757`在图片开关非true时返回unavailable；`controlled-image-bounty-v3-capability.mjs:46–53`不声明生图/改图；API `ChatActionCapabilityService.java:72–95`只有真实声明与现行绑定都READY才暴露`generate-image/edit-image`。
5. 因而当前已证实的断点是**统一Runtime吴用的图片执行配置/能力未接上**。不能将其描述为网络慢、Provider模型不可用、生成后上传失败或验收失败——本轮没走到这些层。

林冲、公孙胜有相同线上DISABLED现象；未读取其私有Provider配置，故不宣称三者每个深层根因都已独立查清。卢俊义属于另一账号，本轮不查、不用。

## 最小后续修复方案（本轮未执行配置写入/重启）

优先恢复**一个本人Agent（吴用）**的既有受控图片链，不新建接口/第二Runtime/绕身份或新付款通道：

1. 在现行统一Runtime profile中明确`controlledImageHttpEnabled`、`controlledImageHttpEndpoint`、`controlledImageHttpApiKeyEnv`、`controlledImageHttpModelId`、`controlledImageHttpBindingId`、`controlledImageHttpBindingEpoch`、`controlledImageHttpLedgerRoot`；沿用现行scope和正式批准的provider binding，不能只开一个boolean。模型名必须来自实际可用Provider与匹配operator policy，不从聊天模型名推断。
2. 核对`nativeConversationHttpPollEnabled`、`workspaceFileApiOrigin`、subject独立`workspaceFileRootDir`，及该subject的Provider环境映射/凭据可用性（只回读存在性，不复制个人HOME/auth给其他账号）。若选HTTP执行器，不顺手引入CLI备用链；现有代码可否满足以实际配置验证为准。
3. 使用现行配置生效/单subject能力刷新路径；若只能共享Runtime重启，明确影响范围、保持已有安装/锁/恢复边界，另行在授权范围执行。当前用户授权“开发连续问答+图片复验”未被扩大为共享服务重启或Provider配置改动。
4. 同一task440再次只读能力检查：执行声明READY、binding精确匹配、操作包含GENERATE_IMAGE，明确owner consent后才受理**一次**。不创建重复事项。
5. 经现行UI受理→action child EXECUTE→真实Provider单次调用→asset/output→PNG实际字节/摘要→预览/鉴权下载→单图验收。失败按确切层补修；不把CHAT完成当OUTPUT_COMMITTED。
6. 本次新蓝鸟成功后再另验改图；历史task424混合独立根问题不重列必做。

配置接通前不承诺Provider/上传/验收必定成功。以上是下一步方案，不是配置已修改或端到端已通过。

## 证据

本轮独占headless浏览器已关闭，未操作用户in-app标签页。证据目录：
`/var/tmp/cyf-image-retest-20261011-main/`

- `new-task.json`：新建task440，open、version0、funding null、无assignedAgent。
- `controlled-capability-440.json`：吴用真实GET响应。
- `other-owned-online-capabilities-440.json`：林冲、公孙胜真实GET响应。
- `installed-config-readback.json`：已安装模块真实纯配置解析、profile及模块摘要。
- `server-and-release-readback.json`：服务端开关、吴用既有非秘密operator policy及线上记录摘要。
- `network.jsonl` / `mutation-summary.json`：仅一个业务写请求，为task创建；无点将/action/执行/验收写。
- `new-scene.png` / `wuyong-detail.png`：真实页面。页面只证明创建/候命/点将入口存在，**没有实际弹出图片不可用提示**，不能把API结论伪称UI已提示。
- `flow-current-list.json` / `flow-config-readback.json`：当前Run197 SUCCESS；16:19核对当前配置仍CI-only摘要719b2801…，本轮未改Flow/发布。

2026-10-07历史PNG和下载PASS保留原证据；不拿旧成功覆盖本轮前置阻塞。

## 2026-10-11 19:56 修复接续范围（尚未发布）

- 用户“继续”承接后端修复与原444改图验收。Turing为API唯一Owner；Main管理安装、前端最小恢复投影和业务实测，不新增Reviewer。
- Web唯一Writer Main，仓库/worktree `/home/isp/wsps/cyf/web`，branch develop，固定base `7b14dffd5d9d259df720f84e57a8453424fb0a65`，工作区干净，19:54远端develop实时一致。允许路径：bountyOutputCatalog.js、两份既有explicit-execution/typed-interaction测试、发布版本元数据；不改全局规则/接口/兼容/费用/自动重试。
- 本机生产源码+既有synthetic fixture复现：FAILED且无child的APPEND动作仍产生stepId=null交付节点，阻塞currentDeliveryProjection及继续发送。仅将服务端验证为FAILED且child三个字段全部null的请求排除出成果投影，保留失败卡片与历史；QUEUED/有child失败/未知状态/任何不合法scope继续拒绝。没有用模拟数据冒充线上验收。
- 最早验证：existing explicit-execution-delivery + typed-deliberation-interaction（失败无child不阻止基于原媒体发起新的合法消息，原失败不自动重试；pending/已创建child失败仍阻止）；然后受影响gallery/finalization。正式前端测试/构建/发布仍Flow4403172；后端原本地精确制品installer。
- Main新证据 `/var/tmp/cyf-image444-edit-fix-20261011-hER21X`。实际503日志仅有HTTP503记录，controller吞掉异常栈；不把异步审计异常当本503根因。真实Spring/JDBC复现由API Owner完成。
