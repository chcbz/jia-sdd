# 本轮复测结果与修复后验收

## 当前结论（2026-09-24 14:54 CST）

**用户指定的同任务主流程已闭环，可开始用户验收。** 最新改版 `e53b3c315a4541c3c8e8ef28eb9cf5608f776251` 已无冲突合入 Web `a7a3b58c7f78bb4c152ade72160cdb6b12eaf58d`（tree `fd719e3886d3ae1b3b74796cbd75139dcca7480f`），发布 `release/1.13.28`；API 保留 `release/1.13.27` / `391869b45e4621b63fc751e2a790a4087aea01d9`，runtime 保留 `1.13.23` / `a79709fe7f5f2e64f583f873f249ee0005d2ee92`，没有随改版回退组件。

- 真实对象：#397 **吴用正式闭环验收-1.13.20-0056**，吴用 `jyt-jiafewnnv58ec2379c-wuyong`，会话 `1760458004739`。全程只续办本任务，不测试扈三娘。
- 需求/附件固定版本/明确点将/议事/实际开工/r1 PDF/要求修改/r2 PDF/验收/完成/归档均有真实证据。它是跨修复版本继续完成的同一任务，**不是所有步骤在 Web28 上从零重跑**。
- r2 为6页，原5页预览正文逐页一致，附件独有校验码匹配；追加应急职责、联系顺序、前一天/当天检查和雨天室内方案。下载 SHA-256 `a770482e646eb1d05dcfb2468309697c26796be9132acfe40c933df5c4cb2cc0` 与正式artifact一致；校验码未注入聊天/返工说明。
- 14:50:19 服务端接受 r2：单次UI验收POST 200，`expectedTaskVersion=4`、`expectedDeliveryVersion=0`；回执 `accepted`、taskVersion5、workItemVersion14，概览刷新为已完成。
- 14:51:32 服务端正式归档：单次UI `/agent/tasks/397/archive` POST 200，taskVersion6。整页刷新后案卷显示已归档，r2仍已验收，r1仍要求修改且原文件保留。归档后再次真实下载摘要不变。
- 最终页面为 430×932 竖屏触控仿真，实际 OAuth 重登录成功；新入口 `index-CZdQwKSY.js`，页面无横向溢出。不是实体手机/软键盘或全产品验收。
- 最新合并树18份相关测试 **268 PASS /0 FAIL/0 SKIP**，正式Vite构建PASS（1m22s）；API27相关测试48 PASS、runtime23相关测试163 PASS复用各自不变SHA证据，不汇总冒称全仓全量。首轮测试未带仓库原有`exit:true`导致断言后进程滞留，已保留失败归因并使用`--exit`重跑exit0。
- `build_origin=local_user_authorized`，无Flow Run。仅本任务API在无在途Provider时通过canonical入口停启以避免同机OOM；恢复原API27 JAR与配置、健康UP后发布Web。保留全部旧安装/制品，用自有不可变同字节文件硬链接去重腾出实际空间；未删除他人资料。
- 最终浏览器初始旧会话401后正常OAuth登录；本次验收/归档请求均成功，未手工DML、未重复未知POST、未进行钱包扣款操作。已授权真实Provider的实际费用仍未知。

验收入口：**聚义厅 → 办事概览 → 案卷 → 吴用正式闭环验收-1.13.20-0056 → 查看进展 → 查看正式成果与验收**；PDF可在百宝箱查看/下载。

证据：`deliverables/verification/juyiting-formal-flow-1.13.22/mobile-portrait-web28-final-20260924/closure-summary.json`、`deliverables/verification/juyiting-formal-flow-1.13.22/mobile-portrait-web28-final-20260924/pdf-r2-verification.json`、`deliverables/releases/v1.13.28-workbench-latest-local-20260924/release-outcome.json`。

范围限制：后续BF15–18、BF24–25及实体设备/全产品验收未冒称完成，见本目录 `remaining-bugfixes.md`；下面保留旧版本失败/待验的历史，不代表当前#397状态。


日期：2026-09-23（Asia/Shanghai）。环境：线上 kit/api；Chromium **430×932 竖屏触控仿真，非真机**；复用已授权登录，不包含本轮登录验收。主测吴用；林冲仅只读核对在线/配置，不宣称其执行链路通过。扈三娘未用于本轮测试。

## 实测矩阵

| 步骤 | 结果 | 证据/说明 |
| --- | --- | --- |
| 首页提出需求 | GAP | 默认进入私人交办，没有直接转正式悬赏的同事项完整路径 |
| 起草正式任务、保存、确认创建 | PASS | taskId=395，draftId=hdr_95c7f957c2a5470db56419ad7d1dcbcf；只创建，不执行 |
| 上传合成 TXT | PASS_UPLOAD_ONLY | fileId=pws_56597b2fe5a84cbcace77ac4d2eafe91 v1；不算关联/授权成功 |
| 在任务中选材、预览、确认关联 | BLOCKED/GAP | 详情查看禁用；未关联 #395 |
| 明确点将吴用 | PASS_ASSIGN_ONLY | 已指派，不等于派发/执行 |
| 命令送达、领取/开工 | FAIL_DELIVERY / BLOCKED_EXECUTION | queued，dispatchedAt=null，未取得 receipt/run 证据 |
| 榜文议事首次发送 | FAIL | HTTP 404 CONVERSATION_NOT_FOUND |
| “另起话头”后发送 | FAIL | 改变会话入口后仍同 404；停止重复 |
| 查询工作空间/事件 | FAIL | 符合查询契约的请求返回两个 503 |
| 正式交付列表读取 | PASS_READ_EMPTY | HTTP 200，items=[]；不是交付成功 |
| Provider 执行、PDF、正式提交 | BLOCKED_NOT_REACHED | 无本任务成果、无 submitted 证据；不确定是否发生任何 Provider 用量 |
| 用户验收/返工/完成/归档 | BLOCKED_NOT_REACHED | 不手工造状态；未点击未满足前置的验收/归档 |
| 普通密议连接对照 | INCONCLUSIVE_FINAL_REPLY | UI 先显示已递到，后显示通用传令失败，无可验证最终回复；不得替代正式链路 |

16:20:43–16:20:46 +08:00 只读核对：#395 仍 assigned，startedAt/completedAt=null，吴用 online/canOperate，formal-deliveries 空，workspace/events 503。

截图 01–25 的正式主流程保持竖屏触控仿真；后续独立 CDP 诊断未能取回请求体，且影响 coarse pointer 仿真，故后续对照图未纳入移动验收证据，未把该测试工具影响归为产品 bug。

## 修复后必须执行（全部未执行）

- AC01 吴用/林冲中明确一个最新运行版本可核对的 Agent；只向选定目标派发；保留入口身份与作用域。
- AC02 同一正式 taskId：草稿 → 张榜 → 固定资料版本关联/授权 → 点将 → 已接收 → 实际开工 → submitted/reviewing → accepted/completed → 终态归档。
- AC03 下载本任务 PDF 并校验文件摘要、PDF结构及仅存在于本次附件中的新随机独有标记（历史标记 MATERIAL-WY-395-A 不作为新验收读附件的充分证据）；聊天大纲/本地路径/私人 result.pdf 均不能替代。
- AC04 要求修改 → 返工待启动 → 用户明确启动 → 新 deliveryId/revision 且 supersedes 指向旧交付 → 再验收；历史成果保留，不自动重复付费。
- AC05 10 个主状态和未知态显示/筛选/计数一致；已领取与实际开工分开；legacy 完成不冒称 accepted。
- AC06 断网、重新打开、刷新、回放不能重复派发/执行；原意图可核对；未启用功能有清晰能力说明。
- AC07 跨 owner/client、非成员、撤销输入、旧 lease/CAS 冲突仍拒绝；不扩授权文件范围。
- AC08 自任务详情进入百宝箱后可查看/返回且保留任务；竖屏无控件遮挡。林冲普通命令所需 workspace 配置须明确校验，不能用 online 当可执行保证。
- AC09 受阻/失败/取消/归档真实分支有原因与下一步；慢请求只记录，不按任意耗时门槛强制失败。

当前验收结论：**FAIL / 上游阻塞，未跑通正式悬赏全流程**。本轮没有修复、测试构建或新发布。

## 1.13.19 验收补充（计划，未执行）

- 修复/发布方案见 `docs/implementation/V1_13_19_FORMAL_FLOW_BUGFIX_PLAN_20260923.md`，本页历史 FAIL 不因新增版本而变成 PASS。
- 新验收的输入使用只存在于附件内的新随机标记；不得把标记复制到榜文、聊天或执行 instruction。旧标记 MATERIAL-WY-395-A 仅作历史复现定位，若已暴露在其他输入则不能证明读过附件。
- 新任务通过不等于 #395 已修复闭环；每个用例记录其自己的完整 taskId 关联链。
- TASK 执行创建时的服务端 claim/start 不等于 Provider 已运行，需追加实际 runtime 接收/执行及正式产物证据。

## 2026-09-23 19:11 CST 修复候选进度（仍不可验收）

BF-01/02/05 API 与 BF-03/04/06 Web 源码已合入各自 develop、冻结 release/1.13.19；定向测试和本地生产构建已有记录。联合制品验证、双组件 dry-run 均 PASS。详见 `deliverables/releases/v1.13.19-formal-flow-local-20260923/`。**尚未部署，AC01–AC09 尚无新版线上同任务业务证据；本页历史 FAIL 不变。**

下一步：在北京时间 2026-09-24 00:00 后端发布窗口完成锁内安装核验，再用吴用或林冲进行 430×932 触控竖屏同一 taskId 真实 PDF/返工/验收/归档测试；未通过前不得通知“可以验收”。

## 2026-09-23 21:25 CST 上线后竖屏复测（#396，未通过）

1. 原 1.13.19 API/Web 制品于 19:33/19:41 上线，exact SHA、部署记录与健康读回见 `deliverables/releases/v1.13.19-formal-flow-local-20260923/evidence/final-online-health-20260923T194739+0800.log`；本节是新的业务验收，不修改前述 #395 失败事实。
2. Chromium 430×932 竖屏触控仿真（非真机）以测试身份新建 #396，上传只存于附件的独有标记文件；POST `/agent/tasks/396/file-links` 返回 201，但页面因未读到跨域 `ETag` 提示“关联回执无效”。**没有重复 POST**。21:09 后续新登录的只读 GET 200 确认唯一 ACTIVE INPUT 关系 `pwtl_dba197bc94984db996e265a2bd2eb44a` → `pws_46267e17e4fb45bfb1477787367b8309` v1；仅此时才认定关联已持久化，不等于 runtime 读授权。
3. 点将仅选吴用；POST `/agent/tasks/396/assign` 200。榜文议事 POST `/chat/stream` 200，后续 HTTP/2 流与 events 出现 `net::ERR_HTTP2_PROTOCOL_ERROR`，UI 最终为“传令未达”；**没有可核对的 Agent 最终回话**，未重复发议事请求。
4. 只读 GET `/agent/tasks/396/workspace` 200 返回事件 `MEMBER_DONE`、`WORK_ITEM_COMPLETED`、`TASK_COMPLETED`；业务主状态已为 `completed`，legacy 工作项 `wi_legacy_aa1f9a3b1b404e956431f741bd2e2583` completed、无 startedAt。与此同时正式 `/formal-deliveries` 200 `items=[]`。**不得把 legacy completed 当作正式 PDF、submitted、accepted 或闭环**；没有点击正式执行/返工/验收/归档，不可对 #396 再自动重复付费。
5. 20:51 本机测试与 Chromium 并行造成全局 OOM，内核杀掉本任务 1.13.19 API PID 2241547（亦杀掉部分浏览器进程），登录曾 502；已停止并行重负载，用原制品 SHA `cb485047f7aadb0889ee4a8c8d4c94cf1f28cca767c00663f1c9dc20f22e4c0f` 经既有生命周期脚本恢复 API，21:00 后 PID 2270919 健康 UP。未切换 JAR/版本，无生产 DML；此事件不算验收通过。

证据：`deliverables/verification/juyiting-formal-flow-1.13.19/mobile-portrait-20260923-r4/task-396-read-only-state.json`、同目录网络摘要与截图，以及 `deliverables/verification/juyiting-formal-flow-1.13.19/production-api-recover-oom-20260923.log`。附件独有标记未抄入议事、需求或执行 instruction。当前结论仍为 **FAIL：正式任务被 legacy 自动完成而无正式交付，议事未取得最终回复**。付费 Provider 是否实际调用和费用未知，不能宣称 0。

后续新增 BF-07：正式悬赏的 legacy report/默认工作项不得越过正式执行/交付/用户决策自动聚合为 completed；同时区分旧任务 legacy 完成与正式 accepted，保留既有 ACL/CAS/lease/审计，不对 #396 伪造回滚/重开。BF-08：议事流 HTTP/2 中断的原会话恢复与最终回复可核验，禁止无脑重发或把 200 视为交付。需在新候选 exact SHA 与新测试 taskId 上重测，#396 保留失败证据。

21:31 CST 修复候选补充：API ETag 跨域暴露 `CorsConfigTest` 通过（本地 Gradle 19m39s；修复前一次漏传 Gradle nonpublishing 参数的失败保留）；Web 缺 ETag 只读回查/不重复提交的定向 Mocha 7 PASS。均为**未部署候选**，不得改写上述业务 FAIL。并行重负载引发过 OOM，后续构建必须与线上登录/浏览器验收串行且重新核验健康、内存/磁盘实况；不按主观性能 SLO 中断业务流程。

## 2026-09-23 22:34 CST 增量修复候选（**未发布、未验收**）

- BF-07 API 候选 `a357883b80240597af3efce43e0235d9472b30b1`：在 owner/client/tenant 精确锁住 task root 后，根据同 owner 范围内已提交 `TASK_CREATE` 草稿的持久关联证明阻止全部 legacy report，原 legacy 任务保持旧流程；新建了前置拦截/无写入的负例。**本地 Gradle 两次均被内核 OOM 杀掉（22:02 Java RSS 865252 KiB、22:30 722436 KiB），测试没有 PASS；停止同根因重试。**日志 `deliverables/verification/juyiting-formal-flow-1.13.19/bf07-hall-legacy-guard-test{,-r2}.log`，台账 `V1-13-20-BF07-20260923` 的 gate=`blocked_root_cause`。API 线上仍是 1.13.19 旧版；#396 已 completed 的历史结果不被自动纠正。
- BF-08 Web 候选 `332c16e31c37a5e6eebe7da5b513c5cd6925d608`：HTTP/2 断流后不自动重发；有原 conversationId 才以该 ID 只读回查并等待本轮新 final，无 ID 只显示结果未知。`juyiting-hall-conversation.test.js` 定向 45 PASS；**此测试不证明线上恢复，也不证明吴用真的回话。**
- BF-08 新实证：21:22 线上 API 日志 `AgentWebSocketHandler.resolveTaskMemberAgentIds` 对 #396 Agent 回话使用 session 的 owner/jiacn 作为 task tenant，`AgentServiceImpl` 抛 `tenantId must be 0`；任务成员 ACL 无法验证，原回话被拒绝。Chat API 候选 `43113dabc34a7792d37edcdb8c15c66b545f1454` 在校验会话目标、作用域和 authenticated session 后，以 task tenant=`0`、原 owner/client 上下文重新读成员，失败仍拒绝；待本地正式测试构建。HTTP/2 协议错误还需独立定位服务端/代理断流，不能归因于这一个 ACL 错误。
- 先前 ETag CORS `bc8a0797` 与 Web file-link readback `a689b2d3` 均是上述候选的祖先；尚未组装/部署新联合制品。正式 430×932 竖屏触控仿真、PDF、返工、验收、归档 **仍未通过**，不得发“可以验收”。

22:42 CST 补充：Chat 候选现在还在流式回复前发送**只含持久 conversationId 的引用帧**，以便 HTTP/2 中断后 Web 只读回查；该帧不是“已送达”或“Agent 已回复”，其单测未运行。最终 API 候选 `3ff35ad32fd6fea448fdaf634b9b0e57c0240d9b` / tree `1a25bcfebed6fd23382c5ef84ca14cb94eff84be`，尚无正式测试/生产构建/部署。服务端和浏览器根因应分开验证，不能拿本地 Mocha 代替线上触控验收。

## 2026-09-23 23:21 CST 本机构建整改继续（不是线上验收）

用户确认暂无其他构建机器，继续本机。已形成低内存整改矩阵并通过 orchestrator 解锁有变化的方案：SerialGC、288MiB heap、单worker、编译/测试分阶段、复用本任务原工作树增量缓存，浏览器不并行运行。未停止/修改线上API，未清理其他任务tmpfs或进程。

- Stage1：`3ff35ad3` / tree `1a25bcfe…` 上 chat生产代码+common-test依赖 **BUILD SUCCESSFUL（7m49s）**，不算测试PASS；API PID2270919实际health仍UP。
- 增加正式来源SQL绑定/精确owner谓词以及会话成员查询成功/失败后的context恢复回归，提交 `37ee998e170a95e748cd28446ea7bae83e8d042b` / tree `03638ee47b0ea0b594fb31e73a6f5ff0a3d6ff40`；添加有明确范围的`bf08FormalFlow`定向source sets，不改默认test，不隐藏历史默认suite编译债务。正在独立编译/运行，尚未PASS。
- 证据与整改矩阵：`deliverables/verification/juyiting-formal-flow-1.13.20/local-low-memory/`；原#396失败、1.13.19线上状态与未知Provider费用结论保持不变。

23:43 CST：低内存 Stage2 首次在测试夹具编译失败（旧 aggregate 签名缺 owner），不是OOM；夹具迁移后 `6c413fac` **编译成功6m36s**。Stage3真实执行Agent suite **60项：55 PASS/5 FAIL/0 skip**，Chat尚未执行。失败归因：legacy夹具仍用历史非0 tenant；Controller golden ID保留旧tenant输入；formal service fixture用真实换行但既有持久摘要域前缀用literal backslash+n。修正均只改夹具，不更改生产ACL/摘要协议、不移除断言。新候选 `183b8cda352c19c7e0427cfca7b0cc433cede06e` / tree `1de9baf1d2ed64ea297280ccf34dfa381df3a543`，已形成failure matrix、orchestrator授权新候选重测；原失败XML单独保留。不把55项PASS合计成整个suite PASS。

## 2026-09-24 00:15 CST 定向验证通过、source冻结（未部署）

- API最终 `0e25fa32a532686b73e235cdea9c5c43d0fce36b` / tree `60fd98e8e2bda3b61245b8f910715efb8890574c`：`bf08FormalFlow` Agent60 + Chat58均通过；独立 `CorsConfigTest`5通过，合计 **123 PASS/0 FAIL/0 SKIP**。Agent60在后续仅Chat夹具变化时由Gradle UP-TO-DATE复用；不是全workspace suite。
- Web最终 `b0564c7be0bbd4fa908d0497dc03a38d32bb1938` / tree `d729dc1ca69cd6ca5d12f59e95fd6ea5b0c1701e`：7个相关测试文件 **101 PASS/0 FAIL/0 SKIP**。首轮100/1是独立挂载时缺jsdom SVGElement；仅在该组件suite补齐/恢复DOM构造器，不改生产代码与断言。node_modules为既有共享依赖，只读核验当前lock所有已安装包version/integrity及非optional包完整性，0不一致；未删除或重新安装他人依赖。
- 两个组件均非force fast-forward到remote develop，新增冻结`release/1.13.20`且远端readback一致；没有覆盖`release/1.13.19`。证据`local-low-memory/component-promotion-and-freeze.log`。
- 生产构建继续同机SerialGC/单worker分阶段；已启动`:starter:classes`，**尚无本次bootJar、Web dist、安装或新移动验收**。线上仍1.13.19 PID2270919 health UP，不把相关测试通过称为全流程通过。
- 新联合输入`deliverables/releases/v1.13.20-formal-flow-local-20260924/release-input.json`；新旧制品/恢复备份按实际大小测算，前次例外发布授权不被伪造成新版例外。

## 2026-09-24 00:43 CST 本地构建完成（业务验收尚未开始）
- API bootJar成功9m33s；构建附带POI classpath 2项与public-artifact-verifier64项均PASS，无skip。此前定向123项另计，不称全仓全量。
- Web初轮384MiB堆上限失败exit134（非kernel OOM），归因并保留日志；根据实测余量改为768MiB/semispace8MiB后成功2m3s，101项定向回归证据仍绑定同tree。未停止线上服务，未并行Chromium/Gradle，未删除共享tmpfs。
- 双工作树切至已冻结release/1.13.20，未改变SHA/tree；本地制品及联合校验通过。API SHA256 `422963cf18f3d49e1e423cc20232349bb46f84ad0bc7fd06849683cc8cec2ab1`；Web archive `e1caccbcd7a549a64c89f37f376fc0a5502f430d342085de7911876bc6e67f97`，dist tree `594b2954c688808f4cc2f21028153c0930985337d92cb963187b9e74eb3e585a`。
- 发布私有入口只将发布互斥改为等待，并在锁内增加精确旧API PID/start_ticks/JAR与Web tree保护；diff与实际工具摘要在release evidence/runtime-entry，不改共享工具、不抢占其他任务。新暂存+旧API恢复副本+Web暂存按实际612047015 bytes测算，观测可用2446802944 bytes，无额外预留。
- 使用既有本地发布授权，在2026-09-24夜间验证就绪后进行当日一次发布，不冒用1.13.19白天例外。此时尚未实际部署，仍不能宣布验收通过。

## 1.13.20 实测 #397 与 BF-09 增量（2026-09-24服务器CST时间）
- 1.13.20部署PASS：API2352949健康UP，Web资源摘要匹配；结果`deliverables/releases/v1.13.20-formal-flow-local-20260924/release-outcome.json`。部署成功不等于业务验收通过。
- 新task397「吴用正式闭环验收-1.13.20-0056」由正式TASK_CREATE草稿创建；新附件`pws_0d0d84b1a1974e06a3c6cb48c502ff6d`v1通过UI上传/预览/关联INPUT，单次POST201，未再误报ETag。标记只在附件。
- 仅点吴用；TASK_INVITE已dispatch，旧简报Provider占用期间第一次议事得到明确busy终态（不是未知结果）；等待简报完成后新发一次议事，原conversation1760458004739得到“已递到”和真实最终确认。未自动重发未知请求。业务状态assigned/required workItem ready，未被legacy自动完成；尚未发起正式PDF执行。
- BF09复现：合法快照200已读取，事件流空闲约30秒后200空体，UI一直loading而拒绝正式开始。已新增独立snapshot_ready状态（不谎报live），同scope/唯一ready工作项/服务器ACL-CAS不放宽。
- Web1.13.21定向**108 PASS/0 FAIL/0 SKIP**；第一轮旧expected loading断言失败证据保留，改单一预期并保留真实streamOpen、错误和身份切换断言。新SHA`ba373f3d4aa609a6b0d2fc96cec9c16d20138695`/tree`f681eee9f9374ddfbba5895917ab82d455b14829`已推develop与新release/1.13.21。API冻结20不改，不再重启后端。本时点Web21在串行生产构建，尚未部署。


## Web1.13.21 上线后同 #397 复测与1.13.22候选

- Web21已真实部署，API仍20且没有因Web补丁重启；`release-outcome.json`位于 `deliverables/releases/v1.13.21-snapshot-ready-local-20260924/`。108项Web定向测试及1m31s生产构建PASS。
- 430×932触控浏览器中恢复原会话后，“确认开始正式办理（PDF）”已可用；只点一次，得到 TASK execution `pwe_f1a9ac087da946bea28256d63a81333e` / run `pwe_run_94bc1d9615b74f849317fec8423b2a2e`。**这是执行受理，不是交付通过。**
- 服务器北京时间01:48:37只读核对：原执行QUEUED；workItem running，leaseUntil=1790185704282（01:48:24.282）已过期；主任务assigned/startedAt=null；formal-deliveries仍items=[]。证据 `deliverables/verification/juyiting-formal-flow-1.13.21/mobile-portrait-task397/05-lease-expired-readback.json`；未重发POST/变更状态/追加付费调用。
- BF10候选 runtime commit `faf8d1dc257ce97d0ff9ee5bd942b2d87a7eac51`，tree `1c69bdc268946f61464a830826e216349d1f336a`，已推送/readback feature分支 `codex/formal-flow-bf10-registration`，未合入/冻结/部署。
- BF10定向：修复前12项中4 FAIL（已归因），修复后12/12 PASS；与agent-client队列/去重等回归合跑 **110 PASS、0 FAIL、0 SKIP**。包含迟到精确ACK恢复队列GET、错误身份/旧attempt/断线拒绝、拒绝后不可恢复与token日志隔离；测试mock Provider，不冒充线上执行验证。
- 测试日志 `deliverables/verification/juyiting-formal-flow-1.13.22/bf10-{red,green,runtime-regression}.log`。BF11/BF12仅方案，未声称测试通过。浏览器已按串行策略关闭；共享服务未重启。
- **整体验收：NOT PASSED**。缺正式PDF下载与附件随机码核对、要求修改、新revision及supersedes、用户验收、完成、归档；费用仍未知，不能报零。


## 2026-09-24 09:53 继续实施（未达到用户验收）

- 用户本次“是”已明确授权共享 `codex-ws-agent.service` 空闲接管。09:07 已部署 runtime 1.13.22；锁内旧PID/启动标识/配置哈希和空队列/无子进程校验通过，旧安装保留，三个注册 ACK 到达。API/Web 未变。证据：`deliverables/releases/v1.13.22-runtime-local-20260924/deployment-result.json`。
- 430×932触控模拟浏览器只读复查同任务#397，吴用/林冲online，原执行仍QUEUED、主任务assigned、正式交付0；没有新执行/Provider调用，不能宣称全流程通过。
- BF11 后端精确租约回收单测55/0；Web撤销确认、持久未知意图、身份隔离、精确执行恢复及相关工作台/交付回归103/0。扩大测试中暴露的旧mock/断言合同漂移已修，失败日志保留。
- BF12 增加独立native start POST；现有普通命令ACK链路不能接纳工作区派生命令，不再据此伪称自动开工。API单测/真实HTTP安全链77/0；新增真实H2 task/event事务用例已跑，原member fixture占位符缺失引起扩展回归失败，已修并复验中。Runtime Provider前确认、未知结果不重发不执行、原注册回归合计163/0。
- 候选未部署，不覆盖冻结runtime22；新增runtime23。后续先完成H2/构建、按发布授权/窗口部署，再从#397显式恢复；实际PDF、返工revision、验收、完成和归档均仍待浏览器验收。


### 09:58 验证与冻结读回

- API `abfb441f1aa28141393760ed547f6a818dc6c1df`：修复测试fixture后86 PASS/0 FAIL/0 SKIP，其中9项真实H2事务测试（2项新增native开工的状态/startedAt/事件持久化、幂等与回滚）。不是生产DB测试，也不是全仓测试。生产bootJar成功，2分钟。
- Web `d37cfa5bc65e755d5b7dc8f29e60df18c22d3f64`：103 PASS/0 FAIL/0 SKIP；Runtime `a79709fe7f5f2e64f583f873f249ee0005d2ee92`：163 PASS/0 FAIL/0 SKIP。源码均已正常fast-forward组件develop，并新建冻结API/Web release/1.13.22及runtime release/1.13.23，远端读回一致。
- 本机串行构建中，无Chromium/Provider运行。白天API例外发布授权不从上一版本推导；构建/准备不等于已经部署。


### 10:05 发布准备完成，仍未部署/未验收

三组件制品已封装，exact SHA/tree及摘要见 `deliverables/releases/v1.13.22-bf11-bf12-local-20260924/release-outcome.json`；前后端联合制品verify及两项只读deploy dry-run均PASS，runtime私有候选配置/toolchain health通过。封装首轮因detached ref、相对input路径、toolchain CLI拼写分别停止，均已归因并修正准备操作，未重建/篡改已验证源码，无生产进程操作。

线上仍API20/Web21/runtime22；当前09月24日白天，API22例外发布尚未获得本版本明确授权。收到确认后按API22→runtime23（重新核对无在途工作）→Web22部署相同制品，再继续吴用#397的430×932触控浏览器验收；PDF、返工、验收、完成、归档未完成，不能通知可验收。已按实际API备份+暂存、Web暂存、runtime候选记录空间计划，无任意预留阈值。

### 2026-09-24 10:43 例外发布与线上新进展（仍未完成验收）
- 用户明确“允许例外发布”后按 API22 → runtime23 → Web22 完成；API PID2534279 健康UP，runtime PID2535803 三注册ACK，配置未改、切换前无在途，旧安装保留。证据分别见 `deliverables/releases/v1.13.22-bf11-bf12-local-20260924/` 和 `deliverables/releases/v1.13.23-runtime-start-local-20260924/`。
- 同#397 UI单次撤销成功：旧execution INPUTS_REVOKED，工作项ready、assignee=null、事件WORK_ITEM_REQUEUED。因此复现BF13前端ready过滤与后端领取合同不一致。
- Web23新增BF13修复，2项新增回归在旧代码失败、修复后相关55/0/0，生产构建25.75s；commit `244f944713e1195f2305816f20e1f7dcace192ec` / tree `fd55b9bd6fd29b2757b39236b71ab065a0ce8027`，正常FF develop及新冻结release/1.13.23并readback。归档SHA `2079d27d9010fd6ae9df8d073d810dade9bd2f54343d2e7866580c3e166726fc`；联合verify和Web部署PASS，API/runtime未重启。将同盘已验证dist移入stage避免再分配108MB，冻结archive和旧安装均保留。
- 浏览器430×932触控模拟，不是真机。一轮Chromium Target crashed；/tmp低空间相关性未证明唯一根因，后续用可用/dev/shm。一次测试harness等待回执超时导致退出，已只读完整查询历史确认无新execution，不盲重试未知POST；追加request级记录并移除harness回执硬截止。
- 最终新正式请求只获一次202：execution `pwe_11fc8a88438f478e86dc354d35bf8632`，run `pwe_run_72baec1ceefd4621b1ab8774ce5c5c65`。线上工作台已真实显示主任务running、startedAt=1790217671572，TASK_STARTED事件version10（不是仅客户端inbox STARTED）。Provider进程运行中，正式交付尚无。后续PDF/返工/验收/归档仍待完成。

## 2026-09-24 10:45 后续真实失败与 BF14
- #397 精确新执行已真实 TASK_STARTED / running，Provider生成PDF并上传201；output-commit503、failure200，runtime FAILED_COMMIT_FAILED，正式交付仍空。旧版本发布健康不等于闭环通过。
- 生产正式成果存储缺开关，默认Disabled；1.13.24采用配置修复，独立私有根目录与默认限制，复用API22精确JAR。定向存储16项通过，不声称已证实503唯一原因或业务恢复。
- 后续只从UI读回终态、交付列表后决定新执行，禁止重发未知提交/手改状态。正式PDF内容、返工新版、用户验收、完成归档仍需真实通过。

### 2026-09-24 1.13.24 → 1.13.25 实测接续
- 改版已真实合并、Web1.13.24健康上线；#397新执行 `pwe_c1360e7d54b641b89aa68bc924e31a87` 上传201、正式提交200，r1五页PDF17,306bytes，SHA256 `a27477f61037d07b8eca8a4536019037348a0a26f7c7dae30198c40a1c99076f` 与正式artifact一致。
- 430×932触控浏览器逐页读取：目标、分工、时间表、300元预算、风险、验收清单及仅存在附件中的校验码均通过；不公开校验码。旧PyPDF2字体解码失败不作内容失败依据。
- 单次点击“要求修改”返回400，刷新仍submitted；未重发未知请求，未DML改状态。新增BF19/BF20/BF21。
- API `bd4842037a3d35deda9c89617c0da4546c2fa673` / tree `8d0a81673f2b2a75c2a58b7dd61a318da9a48f2b`：8项HTTP真实包装器/验收服务测试通过。
- Web `e005159948ca96038efe0e8189b64c7a25aeed38` / tree `361f0eee81e60b34fe3b9f7c3d73f9eb0f594739`：12份定向测试205 PASS/0 FAIL/0 SKIP，含真实面板接线、身份/任务/Agent隔离与旧响应失效。Mocha完整报告后残余timer使runner未退出，已记录并仅终止本任务已完成runner；不将该退出方式当作测试失败或假称exit0。
- 两组件已FF合入develop并冻结release/1.13.25；构建部署进行中，全流程验收尚未通过。

## BF22/23 实测与定向验证（2026-09-24）
- Web26（1bff9ca/tree53223ba）26 PASS，上线入口index-CFfbdhaR.js；430×932触控浏览器读取#397原正式交付，r1要求修改权威回执decisionVersion=1。BF22后源PDF v1返工表单可达。
- 13:21:36首次单次真实返工POST404，无重复发送、无Provider执行。源PDF可见但file-links未有该PDF的INPUT/REFERENCE；记录BF23。
- API27（391869b/tree0bb3ac6）48 PASS/0 FAIL/0 ERROR/0 SKIP，Gradle exit0：HTTP5、返工6、执行队列32、资料关联5。新增Rework→真实ExecutionService（未预设INPUT）链路，以及真实Spring注解事务+H2写入回滚夹具。H2夹具只核验事务边界，不冒称生产MySQL已验证。
- 首次测试预检因台账仍指向Web26而被orchestrator拒绝，Gradle未运行；纠正候选SHA/tree后运行成功。没有跳过测试或编造云效Run。
- API27已推进远端develop并冻结release/1.13.27，构建/部署及#397新PDF、验收、归档待完成。

- API27实际上线健康UP（PID2656694/JAR3880bd61），Web26/runtime23不变。14:05:42同#397移动UI返工POST202；execution=pwe_680409f9006547f897e05595c39b8bfb/run=pwe_run_170fd20fa6b34dfdab47addf9674ca15，固定源PDF v1/17,306字节/SHA=a27477f6。14:06:36 runtime进入STARTED；未重复POST。202和STARTED尚不算r2正式交付通过。
