## 2026-10-07 14:43 CST：Web1.0.5 已上线，发送刷新修复实际通过；原两独立成果根仍阻塞

**整体 NOT_COMPLETE；当前 API117 / Web177（1.0.5）。**

- Flow4403172/177 精确9020f382…/tree27013565…成功：3180PASS、2pending、0failure，scanSUCCESS；6项catalog/身份/歧义/refresh-flight回归均实际PASS。原包SHA256 2d32be6059d7cffd234cc3820be646902718b35e9d3b9d050b38338e189390ef。
- 经既有5264702/19、job530217409、order70677736，Success/healthy发布1.0.5。364项manifest安装与公网字节逐项核验；浏览器index-3XclUIVb及JuyiHallEntry-kI0iUqn9实际字节同manifest。运维原配置精确恢复/readbackMATCH，没有develop自动部署。
- 仅在新版本实际上线后复验原未受理红鸟草稿一次：读取catalog及typed-outcome、原图片outputs后，明确触达“本次交付范围尚不明确；未发送消息，请先核对原成果关联”。CDP实际网络0POST；服务端catalog前后全等/through53，草稿保留；没有新intent、生成或验收。刷新准备及歧义拒绝真实PASS，不等于混合改单项业务PASS。
- 阻塞已定位到原图和已受理多行文字的两个不可变独立根，而不是读取竞态。现有wire只有单parentOutcomeId，严格投影无显式多根恢复入口。下一步须支持用户明确选择原成果的持久化恢复，不能手改原outcome、历史自动union、重生成图片/文字或绕过验收。
- 附件-only/自然澄清、音频及T09第二认证账号仍未闭环；第二账号凭据尚缺。423已completed不重放，API/吴用/共享Client不操作。

证据：web177-artifact-verification.json、web177-online-verification.json、versionedweb177-flow-config-restored.json、task424-original-draft-after177-once-20261007.json、task424-independent-roots-after177-root-cause-20261007.json。

---

## 2026-10-07 14:28 CST：Web1.0.4 已上线；真实发送核对仍阻塞，新刷新合并修复云测中

**整体 NOT_COMPLETE。API当前Run117、Web当前Run176/version1.0.4；1.0.5尚未上线。**

- Flow4403172/Run176精确e31396a…/treeb3a9a4ec…成功：3179PASS、2pending、0failure、scanSUCCESS；5项新catalog/身份/歧义回归实际PASS。同Run原包62b36037…，经5264702/Run18/job530210480/order70677338 Success/healthy发布1.0.4。364项dist安装与公网字节逐项匹配，浏览器新index-DwYPcj8o/Hall-D4ZyZz20字节同manifest。运维配置恢复精确前值/readback，无自动部署。
- 原task424重开后资料答复及新文字原用户消息恢复显示。仅对未受理原红鸟改稿草稿做两次UI核对尝试；第一次资料尚在刷新，第二次明确提示“当前成果索引尚未核对；未发送消息”。CDP真实Network记录仅GET/OPTIONS、0POST，session没有新intent，草稿保留。没有生成红鸟、替换蓝图或验收，不能把0POST安全防护当混合业务通过，也未独立触达歧义集合guard。
- 新明确根因：catalog刷新后触发typed refresh，发送准备再次调用refresh，旧实现把在途刷新当false返回。两次同输入已停止重试，矩阵通过orchestrator记录；不继续点旧版本。
- 最小长期修复9020f382…/tree27013565…/version1.0.5已push branch/develop：同一个原投影读取Promise合并等待，精确拥有者finally释放，保留身份/上下文fence及queued新hint，不放宽source/输出关系。新增in-flight真实Promise回归；165项本机定向诊断PASS（不是正式云测/上线）。正式Flow177正在测试/构建/制品验证，尚无发布。
- 原独立文字/图片root仍需支持明确业务恢复，不能DML、补写不可变outcome、自动历史union、重生成或重放423验收。混合改单项保留其他项/精确验收、附件-only/自然澄清、音频与第二认证账号仍未闭环；第二账号凭据尚缺。

下一步：精确Flow177同Run核验→版本1.0.5发布→线上字节→已确认0POST原草稿复验；不得在changed候选实际部署前第三次点同一原输入。证据：web176-artifact-verification.json、web176-online-verification.json、task424-original-ready-draft-after176-once-20261007.json、task424-refresh-join-root-cause-20261007.json、flow-web177-current-status.json。

---

## 2026-10-07：API117/Web1.0.3 已上线，多行正文通过；新成果索引竞态进入修复

**整体仍 NOT_COMPLETE，不把正文完成写成混合集合验收通过。**

- 后端5260799/Run117精确49fe947d…/tree26f43324…正式成功；2678执行项、0failure/0error、101skip（selector可能重叠）。新增4项投影/原资产保真修复/未知状态拒绝/真实事务回滚回归实际PASS。原包035a2b89…，JAR b04bafe1…。
- 经5264702/Run16/job530198562/order70676752，固定版本1.1.2-SNAPSHOT+flow.117.sha.49fe947安装成功，PID2311363/attestation MATCH/listenerowned/healthUP/versionrecordverified、回退Run116JAR摘要匹配。原图片executionLink自然OUTPUT_COMMITTED，原asset/output/hash/字节不变，没有重复生成、DML或伪造终态。吴用1145032/Client2216170未动，运维配置恢复前值/readback。
- 前端4403172/Run175精确47eb6c58…/tree0283bc84…：3174PASS、2pending、0fail，scanSUCCESS；原包22b72b87…。5264702/Run17/job530199594/order70676830版本1.0.3安装成功；364项dist安装文件和公网HTTPS字节全manifest逐项匹配。真实浏览器当前index与Hall bundle摘要也与175一致，不凭缓存猜测根因。运维配置已恢复，没有develop自动部署。
- 先确认原草稿无受理记录，修复后仅一次真实UI提交多行需求POST202：mmd-typed-request_1c7dbae8…/message1736463/COMPLETED，精确两行ANSWER deliverable=true。但该POST parentOutcomeId=null/sourceSelectors=[]，产生独立文字root而非APPEND；严格混合集合投影报“本次交付范围尚不明确”。失败留存，不删除历史、不手改metadata、不重发已受理文字/图片，task424仍assigned。
- 新源代码回归稳定复现：上下文generation变化使在途catalog scan失效，旧finally未清自身loading，UI reset watcher遗漏durable activeRequest generation；实际发送未查询原图片output/basis与此一致，未抓实时槽位，不能称唯一live根因已完全证明。已修精确scan owner释放/不清新scan、补durable-generation reset、发送前先核对catalog和typed读且保留身份fence；集合有歧义时不创建无关联POST。
- 新Web e31396a…/treeb3a9a4ec…版本1.0.4已push branch/develop，164项定向诊断PASS（非正式云测）。正式Flow176验证中；尚未上线，不称其解决原两root关联。下一步同Run制品→固定版本发布→原任务真实UI复验；原独立roots仍需受支持的明确业务恢复，不能凭历史union或latest选择绕过。
- 仍缺混合定项修改/保留其他项/精确验收、附件-only/自然澄清、音频与第二认证账号。第二账号需不同于chcbz的合法测试凭据，匿名不能代替。

证据：api117-artifact-verification.json、api117-installed-runtime-verification.json、web175-online-verification.json、browser-actual-loaded-bytes-after175-20261007.json、task424-mixed-text-after175-send-once-20261007.json、task424-current-mixed-catalog-readonly-20261007.json、task424-catalog-race-root-cause-20261007.json。

---

## 2026-10-07：API116 已上线，真实图片与保存恢复通过；后续改稿缺陷正在修复

**T05–T09 整体仍 NOT_COMPLETE。**

- API版本 `1.1.2-SNAPSHOT+flow.116.sha.ae6eca6` 已通过5264702/Run15/job530188274/order70676267单主机Success/healthy安装。runtimePID2295608、10018 owned、attestation MATCH、healthUP、JAR ce57c796… 与Run116一致，versioned record verified；Run115回退副本hash匹配。吴用1145032、客户端2216170未动。运维配置已恢复前值/readback，没有恢复develop自动部署。
- 原media request未重发，action自然COMPLETED，child99775595…OUTPUT_COMMITTED。真实蓝鸟图1370×1148 PNG1513954bytes，asset ast_55c726d77f452bca372b806095f2696e，SHA256 faff63bfb5b87edfbc9d49a91ab114ea2fd52d6da4a7dcb9d7af962d568f1c5a；放大UI视觉核对为白背景一只蓝鸟站细枝、无文字，不用文字描述冒充图片。
- 单次真实UI可选保存arc_6366c78c2d864e52b83e961bd3f2c6b7 → pws_3833ebc2f58748c39eefc880f77cde95 v1；空间真实重开预览及鉴权下载原字节同hash/长度。保存不是验收前置，历史图片不替换；T07产图、T08媒体保存恢复子集PASS。
- 混合文字追加草稿含换行被前端ISO-control校验拒绝；network无POST、session无新intent，未受理，不盲点重试。另外媒体step已OUTPUT_COMMITTED但executionLink仍RUNNING，阻断后续精确causal basis。未手工DML/假终态/重生成。
- API49fe947d…/tree26f43324…最小修复：原事务中精确owner/step/execution CAS终态link；已有terminal projection仅在native committed状态与全部原asset/run/hash/generation一致后修复link，无新消息/文件/事件/provider。新增保真修复/未知状态拒绝与事务link失败回滚回归。正式Flow117验证中，无本机Gradle/build。
- Web47eb6c58…/tree0283bc84…版本1.0.3候选：只允许正文LF/CR，ID及其他禁用控制仍拒绝；只跳过同上下文INSPECT-only历史，不放宽CHAT/EXECUTE/身份来源。43项本机定向诊断PASS（非正式云测）；正式Flow175验证中。所有候选已push develop，尚未上线，不把构建当验收。
- 仍待混合成果改一项保留其他项/精确验收、附件-only/自然澄清、音频、第二认证账号隔离。无重复业务POST；原423保持completed。

证据：api116-installed-runtime-verification.json、versioned116-flow-config-restored.json、task424-media-after116-terminal-20261007.json、task424-media-image-expanded-20261007.png、task424-media-save-once-20261007.json、task424-media-saved-image-reopen-20261007.json、task424-media-saved-image-download-20261007.json、task424-media-followup-root-cause-20261007.json。

---

## 2026-10-07 13:20 CST：媒体阻塞根因修复云测通过；多行保存闭环通过

**整体仍 NOT_COMPLETE；API116 正在部署，不能当作已上线。**

- task424 新目的媒体请求只提交一次：`mmd-typed-request_7fb9a3ecd57d607565a879d20733add3a00d1cb7`。CHAT 已完成，但 action `act_3a788789068755ca6d5aae2657126230d3359c9a` 原为 QUEUED，尚无图片；不得用 CHAT 终态冒充媒体成功。
- 真实 SQL 根因为 `pwe_` + 64hex 共68字符超出 execution_id VARCHAR64。最小修复 ae6eca6e778dd0381d01ed8221e6ea220b762be3 / tree95ece0268baf6fea54a58738eb3eea8dd09834a5 采用64字符确定性execution ID，完整intent/run/绑定不变，无DB迁移/DML。
- Flow5260799/Run116/job530185441 SUCCESS，sources/同Run receipt 精确 commit/tree 匹配。原制品独立读取 JUnit：2676执行项，0failure/0error、101skip（selector可能重叠，skip不算PASS）；新增 identity/replay 与真实H2/JDBC持久化两回归实际PASS。原包226551015bytes/SHA256 affc86f4e1b3faf835ef2509b4dfb54b1ff98d4fe3a3eea0c19e43713edd84ba，JAR ce57c79687fcf4ac13e6cae8d7613d2598347804730ead3c1afeecd247fdc931。
- 固定版本 `1.1.2-SNAPSHOT+flow.116.sha.ae6eca6` 经既有运维5264702/Run15/order70676267安装同Run原件，当前 RUNNING；五参数新版adapter hash固定，前值已保存/readback，不走本机build。不重复发绘图请求，待原action自然恢复。
- message1734362完整多行51codepoints通过真实UI可选保存/百宝箱重开，file `pws_abbfe80855e147e9be1e6893fc00de83` v1。鉴权content原字节下载HTTP200、111bytes/SHA256 cbe4d59ff0e2f44e9238ca147a53cbf83a488ca00484a656064573f6533e2e28，与预览/保存原文相同，T08该子集PASS。
- 剩余媒体产出/改一项保留其他项/精确验收、附件-only/自然澄清、音频与第二认证账号隔离仍未全部闭环。历史失败保留。

证据：api116-artifact-verification.json、api116-new-execution-identity-regressions.json、flow-ops-versioned116-start.json、task424-multiline-saved-answer-download-20261007.json。

---

## 2026-10-07：图文真实闭环已持久化，刷新界面可恢复（本轮更新）

**T07 图片+文本理解子集通过；T05–T09 整体尚未完成。下方旧记录仅为历史。**

- 客户端固定 commit `f29c2ad3693229e14a7cd279cb86d9e7293166ff` / tree `6ad2637daf67d4d24ab26fdc69065c971c3d51eb`。修复 INSPECT 多行 content 被禁止控制字符的通用 nonblank 校验误拒；允许 LF/CR、仍拒绝其他禁用控制字符。将 `chat_dispatch_acknowledged` 纳入 legacy 控制通知，不再误入业务消息校验。定向诊断 agent-client 131 PASS，mixed-material-api-wire-v3 4 PASS；不是前后端 Flow 或全业务验收。
- 本地 client installer 用于已授权控制面恢复验证：release `20261007102637-2215064`，服务正常运行。仅客户端安装，不代表 API/Web 新版本发布；源码分支已 push 并通过远端精确 commit readback（尚未合入 Client develop）。API/Web 沿用既有版本证据，不把 develop 或本地测试写成已上线。
- task424 原保留会话 `1760458004867`：parent `mmd-typed-request_2502196aeba31a18770e1ed99764f2c5457211ce` COMPLETED，actionProgress COMPLETED；child `action-inspect_3b984649450f9d1509627c3d3f5da45777769ea9` COMPLETED / PUBLISHED；inspection-outcome READY / ANSWER / action=null。persistedMessageId `1734362`，finalDigest `sha256:f7797c82f2b08dff408bf86c8d46ad9b6e9fbcaeabf52840d0d477b41f1a287b`。
- 实际图片 2127 bytes 与文本 39 bytes 摘要和原输入一致；答案正确列出红色正方形、蓝色圆形、绿色三角形，并引用 `Quartz river 729.`。这是阅读输入，不是生成媒体成果。第二 recovery 消息 `1734363` 同样持久化；没有重跑原模型或伪造终态。
- 本轮独立只读浏览器重新打开 task424，页面显示上述两份答案且保留多行换行；原失败历史仍保留。截图及 UI JSON 已归档。不重发原 dispatch、不重放 task423 验收 POST、不 DML。
- 仍待：真实媒体产出/定项修改/验收/保存重开；附件-only、自然澄清等代表场景；音频能力此前失败未启用；第二认证账号隔离缺证据。可复用纯文字 T05/T06、文字保存及同 owner 私密 scope 有效证据，不重复验证已通过主流程。

证据：`task424-fixed-send-child-terminal-20261007.json`、`task424-terminal-ui-20261007.json`、`task424-terminal-ui-20261007.png`、`client-f29c2ad-install.log`。

---

## 2026-10-06 22:17 CST：长期修复已安装；真实资料读取通过，原模型结果契约失败未闭环

**T05–T09尚未全部完成。下方22:03及更早状态已被本条更新，不再把原任务描述成仍等待资料读取。**

- 当前固定客户端302eb554c392e7f3bfb1195206bad70b5569fcb6/treed710077115330c5f3e7cfa5e2cd58b65847c47e8，release20261006221436-1856322，PID1857444 active。57payload逐SHA/manifest/provenance均核对；原scope单一原生API来源不变，旧release保留；PID1/API1809106/吴用1145032的startTicks、mountinfo/cgroup仍MATCH。本轮未动API/Web/nginx或业务数据库。
- 原child已经真实取得PNG2127bytes与text39bytes，两文件SHA256与原输入一致、mode0400。注册ACK等待后不再出现原资料读取拒绝。此前竞态归因有代码证据，旧失败没有HTTP状态，不能补写确定401。
- 原模型thread01a11188-89b0-7ee2-9195-d1fe95197b7a/turn01a11188-8ae1-7bd2-8cd0-4aa78e3258b6已经受理并返回；22:05:34严格成果关联校验报ACTION_DELIVERY_PARENT_INVALID。没有最终消息持久记录；旧2bb589c的finally在该校验失败后删除了唯一私有引擎目录。因此真实读取PASS不等于语义/业务闭环PASS，不能伪造终态或原模型重跑。
- 长期修复已安装：INSPECT v3原生schema固定deliverable=false、deliveryRelation=null，CHAT契约不变；任何模型返回后的严格校验异常保留原引擎状态；恢复若原目录/精确marker缺失，必须在创建目录、复制凭据或spawn前失败。45pass/0fail/1skip定向Client诊断验证这些边界；不是API/Web Flow或业务PASS。
- 22:17:20实际恢复明确报TYPED_INSPECTION_RECOVERY_STATE_MISSING；原引擎目录仍0、原engine identity不变，未重新启动模型、未新发业务请求、未DML/手工改inbox。原child GET仍RUNNING/DISPATCHED、typedoutcome404，父actionProgressRUNNING，因此不能标完成。
- 下一步需在保留task424的前提下安排一条新的独立浏览器验证请求验证已安装修复；原失败作为证据保留，不重发原dispatch，不重建task/点将，不触碰task423 completed或重放验收POST。之后继续附件-only、澄清/工具与媒体成果保存替换；音频真实carrier和第二认证账号仍未通过。

证据：task424-real-input-read-terminal-contract-failure.json、client-terminal-safe-installed-verification.json、client-terminal-safe-diagnostics-summary.json、task424-terminal-safe-original-record-readonly.json、task424-terminal-safe-final-readonly.json、task424-terminal-contract-rejected-ui.png。

---

## 2026-10-06 22:03 CST：长期单一原生地址与持久恢复已安装，原task424重验中

**T05–T09仍未全部完成。下方21:11及更早条目为历史，旧b4临时方案/待授权/旧PID均不代表当前状态。**

- 已执行用户“用长期方案，继续”授权：不为INSPECT硬编码localhost:10018或保留独立配置。所有原生HTTP lane采用既有操作员workspaceFileApiOrigin；scope.inspection.apiOrigin及旧独立override明确移除/拒绝，不改nginx、provider或身份/完整性契约。2c05bdd已实际安装；当前scope SHA e23a077927aadfaef0ddc84dedeb3456a025d6b31108e44903e5925e1ad19c57。b4e3a16仅历史候选、未安装。
- 原child的服务端outbox已经SENT，但客户端RECOVERY_REQUIRED没有preparation/engine/final，旧scheduler直接跳过。长期恢复修复7d48dd1在profile lock内核对原key/fingerprint，只对明确模型启动前失败重新读取；已有准备/引擎、未知acceptance或final绝不重跑模型。原child已真实沿原identity回到STARTING，未新建/重派dispatch、未DML或手工挪inbox，模型尚未启动。
- 21:55:39资料GET仍被服务端拒绝（当时旧错误没记录HTTP状态，不能写成确定401）。测量完成会刷新注册，代码允许资料读取先于新ACK，是明确的竞态窗口；是否为本次拒绝的唯一根因仍待核实。已补当前注册ACK等待及仅数字HTTP状态诊断，不落token/错误正文，不新增业务deadline或盲重试。
- 当前已安装固定客户端2bb589c7eb7dcf690b93595e3550cb797cee00ae/tree208e42a1231c58e6b7fadf95fc65e8cfe6b805c7，release20261006220202-1851030，PID1852091 active，57payload逐SHA匹配。旧release/scope可恢复。PID1/API1809106/吴用1145032的startTicks、mountinfo/cgroup仍全部MATCH，仅正常重启共享客户端；不重启API/吴用/nginx。
- 本地Client诊断：统一地址153执行项152pass/0fail/1skip；durable恢复330执行项329pass/0fail/1skip；真实materializer失败模型零启动20pass；ACK等待及现有回归230pass/0fail/0skip。selector重叠不累计为去重总数，skip不算pass，这不是API/Web Flow或业务验收证据。
- 当前仅只读原task424/原child重验；task423保持已完成且不重放验收POST。音频仍未通过/未启用；第二认证账号、附件-only、澄清/工具、媒体成果保存替换及其他真实业务仍待完成，不标accepted。

证据：client-unified-native-installed-verification.json、client-preengine-installed-verification.json、task424-preengine-resumed-content-failure.json、client-inspection-ack-installed-verification.json、client-longterm-diagnostics-summary.json、task424-inspection-ack-first-readonly.json。

---

## 2026-10-06 21:11 CST：Run115实际上线核验通过；真实原child暴露资料读取origin错误

**T05–T09尚未全部完成。当前线上API已是Run115；此前“待安装115”记录为历史。**

- 用户本轮精确授权已执行：版本1.1.2-SNAPSHOT+flow.115.sha.0fd5aed，经Flow5264702/Run12、job529789991、部署单70663152单主机healthy安装。API PID1809106，JAR SHA256141a229a783062e64d4eac08236d05aa1f9c6aced660e5399d4adba2bf9815ac与原Run115制品一致；commit0fd5aed5585d9f0714d246d0bcbb94de757a99f4/treeb1f5c5b4825b64ea446e9a280f9ad9814c541e99绑定，owned10018 listener、attestation MATCH、healthUP。回退JAR实际摘要匹配Run114，不按备份文件名判断内容。
- 吴用1145032、共享客户端1727606未变。临时ops YAML/精确版本adapter/marker已匹配候选并恢复前值/readback；5260799 develop仅cloudCI配置保留，不恢复旧自动deploy，不修改hosttimers。
- API重启后浏览器回到登录，使用用户测试凭据真实输入/单次登录恢复；凭据/token未写文件。仅重新打开原task424查看进展、不create/assign/START/验收POST。原child自动重派，turn stateVersion1→3；客户端已推进至真实materializer，不再是旧contextSnapshot冲突，但21:01:36的原输入GET在公共nginx返回444，客户端TYPED_INSPECTION_RUNTIME_ERROR/fetch failed，typedoutcome仍未完成。
- 新根因已用实际accesslog和nginx配置确认：scope.inspection.apiOrigin指向https://api.chaoyoufan.cn，而publicproxy有意不暴露/internal，最终location/返回444。既有同host原生API使用http://127.0.0.1:10018；原path无认证GET在public是UND_ERR_SOCKET、loopback是401。401证明到达认证边界，不等于授权读取成功。未修改nginx/公开internal/伪造runtime身份。
- 客户端最小修复b4e3a1674f8f61f28634d1cbd1a65cdbd67d3601/treedfe48149be4142ebe09fc15d3528efbad44b058c已自检推送独立分支。仅scopeparser额外允许literal http://127.0.0.1:10018；拒绝loopback别名、DNS、其他port、凭据、query/path/hash及远端HTTP；provider仍HTTPS，六维identity/carrier/profile/长度hash/redirect验证不放宽。33项Client定向诊断实际PASS、0fail0skip（不是API/Web Flow测试或真实业务PASS）。
- 固定单scope候选SHA e82402832387d4ee40dc03a2270adc59e24a4155b03073db13bc76388de67852，只有精确测试Agent的inspection.apiOrigin变化。已保存前值并静态parsePASS，未应用live配置、未安装新客户端或重启。当前同意仅覆盖API115发布，不能扩大到共享客户端或nginx。
- 下一步需明确授权：安装客户端b4e3a16、应用上述单scope候选，核对无活动工作后仅正常重启共享客户端，保留旧release/scope恢复；不动API/吴用/nginx/其他服务，不DML，不重发task424业务请求。随后验证原child恢复及真实图片/文本语义和UI持久恢复。音频、第二认证账号及剩余媒体/工具仍未全验。

证据：api115-installed-runtime-verification.json、flow-ops12-terminal-status.json、flow-ops12-deploy-order.json、versioned115-flow-config-restored.json、versioned115-host-controls-restored.json、task424-after115-original-child-readonly.json、task424-run115-inspection-origin-root-cause.json、client-loopback-origin-regressions.json、client-loopback-origin-config-candidate.json。

## 2026-10-06 20:55 CST：Run115云测与原制品核验通过，等待精确新版本安装授权

**T05–T09仍未全部通过；当前线上API仍Run114。Run115未安装。**

- Flow5260799/Run115、job529785337 SUCCESS；Flow sources绑定0fd5aed5585d9f0714d246d0bcbb94de757a99f4，同Run receipt绑定tree b1f5c5b4825b64ea446e9a280f9ad9814c541e99。
- 原制品独立JUnit读取：2674执行项、0fail/0error、101skip，跨selector执行项可能重叠，skip不算PASS。新增深层context alias/hash/DATA保真与普通事件脱敏两方法均实际PASS。
- 原包226551056bytes，SHA256 391035ffd18a3d99a94db960f869e3673eb913663d545bdf80da669915dd3bfb；JAR SHA256 141a229a783062e64d4eac08236d05aa1f9c6aced660e5399d4adba2bf9815ac。签名URL仅内存；只读tar校验、不解包安装。Run115只有CI stage，没有deploy。
- 当前API1797173 attestation MATCH、owned10018 listener、healthUP；原child12:52Z读回仍RUNNING/DISPATCHED/outcome404。不新建task、不再次点将、不重发图文请求。
- 拟发布标识1.1.2-SNAPSHOT+flow.115.sha.0fd5aed（不伪称源码semver增长）。只读空间/当前Run114摘要预检完成，无安装/配置写入/重启。需精确授权经既有Flow5264702安装Run115原件，仅正常重启API，保留Run114备份/失败恢复，不动吴用、共享客户端、其他服务或业务数据。不能挪用Run114授权。
- 实际安装后优先原child自动重派恢复并验证语义与UI持久恢复；音频、第二认证账号及剩余媒体/工具子集未通过，整体不标accepted。

证据：flow-api115-current-status.json、api115-original-artifact-download.json、api115-artifact-verification.json、api115-new-serialization-regressions.json、release115-readonly-preflight.json。

## 2026-10-06 20:49 CST：Run114已实际安装；新协议修复进入Run115（仅云测/构建）

**T05–T09整体未完成。当前线上API是Run114，不是下方历史Run113；没有自动/午夜发布承诺。**

- 已按精确授权完成Run78唯一下载副本删除，199106859bytes；云端原件全字节/hash已匹配。保留回退JAR、数据及其他下载，没有执行宽范围clean。
- 版本1.1.2-SNAPSHOT+flow.114.sha.fba46c6通过既有Flow5264702/Run11、job529778108、部署单70662818安装，健康UP，API PID1797173/10018；源码fba46c6073d5366633d94756cefc78271ad4107e/tree6f949918045bad4e99e09c0392420cc500c8cb3f和同Run114 JAR摘要匹配。吴用1145032、共享客户端1727606未变。临时版本发布控制与ops配置均精确恢复前值。
- 原task424只发送一条新候选图文请求mmd-typed-request_4f276c93911438d7d5225e596049f1e7c751d0fb，自然ACTION_REQUEST后生成原child action-inspect_dae0e37778d00470519fb09aa759f450be971008。旧TARGET_PROFILE_UNSUPPORTED已解除；最新只读20:38为RUNNING/DISPATCHED，outcome404，客户端拒绝ENVELOPE_FIELD_CONFLICT/contextSnapshot。随后不新增业务请求、不重建或再次点将。task423仍completed且不重放验收POST。
- 根因证据来自只读真实outbox结构和production sanitizer depth=8复现，不是网络frame抓包：根/payload相同contextSnapshot在不同深度被截断，selectors和inputMediaTypes变null，完整性hash/DATA也受影响。
- 修复0fd5aed5585d9f0714d246d0bcbb94de757a99f4/treeb1f5c5b4825b64ea446e9a280f9ad9814c541e99已自检并推送develop。仅在精确typed registry/admission profile/session校验后INSPECT使用完整协议JSON，普通事件仍脱敏；不放宽ACL、profile或strictparser。新增2项回归：深层facts/alias/hash/DATA保真，以及普通事件仍脱敏。未本机Gradle/生产构建。
- 遵循新AGENTS，5260799已单次保存前值、移除唯一自动deploy stage并readback（候选配置SHA aac42945ae2687cd000bab1860ffc72c26a6a67ab3328558759ba0b2ba7d00a4）。正式tests/build/artifact保留；不修改host timers，不恢复旧自动部署。全历史114run无活动后单次启动Run115，当前云测构建进行中，早期source commits尚空，不能宣称精确源码/新增回归已PASS。Run115没有部署动作，也没有挪用Run114发布授权。
- 下一步：独立核对Run115同Run测试/制品与精确commit，成功后请求精确新版本安装授权；实际安装后优先原child自然重派恢复，不再发新图文请求。音频仍FAIL/未启用，第二账号凭据缺失，媒体成果保存替换与其他真实业务子集仍待验证。

证据：api114-installed-runtime-verification.json、run78-authorized-download-removal.json、task424-run114-inspection-wire-depth-root-cause.json、api-develop-no-deploy-config.json、flow-api-inspection-wire-start-full-history.json、flow-api115-current-status.json。

**以下为历史记录，仅其记录时间有效；旧发布时段和等待清理陈述均已被上述当前状态替代。**

## 2026-10-06 20:16 CST：Run114 发布已授权，实际空间预检不足，尚未启动部署

**T05–T09 尚未全部通过，API仍Run113。新AGENTS已替换旧自动/定时发布规则。**

- 用户本轮明确授权：通过既有Flow运维入口安装Run114原制品，仅正常重启API，保留现有备份/失败恢复，不操作其他服务或业务数据。固定发布版本标识1.1.2-SNAPSHOT+flow.114.sha.fba46c6；实际JAR内Implementation-Version为1.1.2-SNAPSHOT，并未伪称源码版本已增长。
- 只读容量预检：可用191016960bytes；adapter临时包拷贝226551012bytes，安装器候选253756837bytes+原JAR恢复副本253753673bytes=507510510bytes。考虑既有adapter替换incoming并回收已验证download后，仍缺89944501bytes（约86MiB）。这是实际制品/恢复副本计算，不新增任意资源预留。未启动Flow安装、未重启API、未修改adapter/运维配置。
- 最小候选回收目标仅为旧Run78下载副本/var/lib/cyf-api-flow/downloads/78/package.tgz，199106859bytes（约190MiB）。云端原制品完整流式下载SHA256与本地一致：6ccf81da87777eca1c40c2fcf6508f08b0ac5719628c4cf67a0fea396a22fd4c。已证明可取回，不落签名URL。当前安装记录与恢复JAR不是该下载包。
- 删除旧下载副本超出本轮明确安装边界，等待精确一次性清理授权；不删除任何回退JAR、证据、工作树、缓存或业务数据。已执行旧clear_disk.sh plan仅只读，实际脚本含旧资源目标及按年龄扫描输出，与指南不同；没有执行clean、不复用其宽清理范围。
- 授权后先重新核对文件身份/摘要、当前record与锁归属，再仅删该下载副本；随后使用Run114既有云测/制品，版本化发布并在线核验后继续424。不存在旧“等待午夜自动上线”的承诺。

证据：release114-authorized-preflight.json、run78-download-cloud-recoverability.json。原423已完成，继续保持不重放；图文/音频/第二账号等缺项不能用云测通过替代。

## 2026-10-06 19:15 CST：Run114 云端验证通过，未实际安装，等待精确发布授权

**T05–T09 尚未全部通过，线上 API 仍 Run113。**

- Flow5260799 Run114 SUCCESS，精确源码fba46c6073d5366633d94756cefc78271ad4107e/tree6f949918045bad4e99e09c0392420cc500c8cb3f由实际Flow sources、CI checkout和同Run receipt交叉绑定。
- 独立读取原制品JUnit：2672执行项、0fail/0error/101skip；不是去重用例数，skip不算通过。新增两个INSPECT派发回归方法实际执行PASS，包含精确Owner正常派发与六个拒绝场景。
- 同Run114制品SHA256 b9414a53953b0c9a9217045fcd3e8c6c7f50f441041c1720f1ad98b7389fee9b；JAR SHA256 b8f93805ebb256342a5d7bb8fdb84309da2e7a9e47e5aad0fc869f1bd30809ff。仅流式读取tar，不本机构建或解包安装。
- deployOrder70661835/单主机SUCCESS不代表安装。作业日志为空；实际adapter要求精确nightly intent，Run114 intent不存在，installed record仍113。API1635406、吴用1145032、shared1727606均存活，未操作服务。
- 既有提前安装授权仅用于113，不能挪用114。下一正常发布窗口2026-10-07 00:00（Asia/Shanghai），是否成功须实际Run/安装/健康证据。若立即继续业务，需明确授权经既有Flow运维入口安装Run114原制品、仅正常重启API，并保留既有备份/失败恢复范围；不改发布时段策略、不操作吴用/共享客户端/其他服务、不DML。
- task424保留原创建、点将和两条失败请求，不发第三次相同输入；新修复实际安装及health核验后再开始新轮。原423已完成且不重复验收。第二账号、音频和其余媒体/工具子集仍未全验。

证据：api114-artifact-verification.json、api114-new-inspection-dispatch-regressions.json、flow-api114-terminal-status.json、api114-deployment-readback.json。

## 2026-10-06 19:08 CST：真实图文业务阻塞于后端派发，修复进入 Flow114

**T05–T09 尚未全部通过。当前线上 API 仍 Run113；后端候选未上线。**

- 客户端16b490f4ef7e6c9b833bcbe4be69e3d088eb4e15/tree2ba32607961a69ffbc04e389d473361b88305f86已安装，共享PID1727606 active，57payload hash通过；主机原12cgroup hierarchy持续保留，API1635406、吴用1145032未变。新网络policy在相同服务gid1000下真实单modelturn图文语义PASS，严格carrier摘要sha256:9b7302af08ffccc761b225ef37ded270f9016bab52c2c3e61a3a30ee770e1552。音频未启用。
- DOM真实上传自己的PNG2127bytes与文本39bytes，固定v1；只创建一次独立task424、只点公孙胜一次，conversation1760458004867。原423completed，不重新创建/点将/验收POST。
- 自动bootstrap CHAT与显式两资料续问均自然返回inspect-materials ACTION_REQUEST；两个真实child INSPECT均FAILED/TARGET_PROFILE_UNSUPPORTED。不是实际图片读取PASS。第二同根因失败后已停止重复发送。
- 源码定位：typedInspection独立registry已有声明，但sendNegotiatedChatMessageToAgent仍调用不可用的旧U0 INSPECT profile决策。修复只对INSPECT选精确tenant/owner/client/Agent且唯一当前READY的session，并再次匹配admission manifest profile；旧CHAT capability解析不放宽。
- API候选fba46c6073d5366633d94756cefc78271ad4107e/tree6f949918045bad4e99e09c0392420cc500c8cb3f已Owner自检、合入develop；新增2测试方法覆盖1正常精确派发及6拒绝场景。未本机Gradle/生产构建。
- 原release Flow5260799 Run114已单次启动（读取全部113历史run且无活动Run后）；目前正式测试/构建RUNNING。起始INIT无source，保持UNKNOWN后只读核验，没有重复Start。源码最终绑定、测试、制品和部署均须实际Run证据，不能写成PASS。
- 实际deploy adapter保留00:00 nightly intent要求。API113的历史提前授权不挪用至新Run114；不改host intent/配置、不DML、不清数据。云端通过后，需按授权发布安排推进，再以新候选业务继续424。
- 第二认证账号凭据缺失、音频失败及其他媒体/工具子集仍待验证，不用已通过的纯文字/图文carrier覆盖这些缺项。

## 2026-10-06 18:47 CST：挂载隔离验证通过，服务INSPECT仍未READY

- 原5d8d0fe真实单modelturn图文carrier通过，新profile为mmd-image-text-understanding-5d8d0fe-01600-v1，carrier SHA sha256:97ed42cda8ddf15f28ea926f66bd55cd374ffae5249f2d8362015ce493714e74。预检及真实carrier前后PID1/API/吴用/原共享客户端完整mountinfo与cgroup/startticks未变，12hierarchy保留。
- 发现并用失败→通过定向回归证明collectChild在exit时过早结束导致stdout/stderr丢失；改为close。slirp失败也等stdio关闭，且仅输出本地网络诊断，绝不输出provider凭据/任意provider错误。
- 新客户端27553344277d3ccfe44ea87355fa56e2daf4b3f4/tree55f6dfb7ba6237cf014be76b7bd602fa972b470a已通过既有installer安装；30定向PASS/1SKIP/0FAIL。当前共享PID1722858 active，CHAT注册READY/nativeHTTP200，**INSPECT实际失败：setns(CLONE_NEWNET): Operation not permitted**。未绕过或伪报INSPECT READY。
- 历史摘要关于slirp0.4的推测不准确：主机实际slirp4netns **1.2.3**/commitc22fde291bb35b354e6ca44d13be181c76a0a432/libslirp4.4.0。未取得上游源码，挂载传播根因仍为假设；隔离修复的实际保护效果已验证。
- 图文业务尚未创建新task/点将/请求；仅真实上传自己的2127-bytePNG与37-byte文本并DOM选择固定v1。原423不动。正进行与共享服务相同uid0/gid1000的guarded无模型预检定位权限差异。

## 2026-10-06 18:33 CST：主机恢复、INSPECT隔离修复进行中

- 已按用户授权恢复原12 cgroup hierarchy挂载，仅重启共享客户端；当前CHAT运行PID1707848，API1635406、吴用1145032未变。
- INSPECT预检与主机挂载再次丢失高度相关，因此精确测试Agent的inspection对象已临时暂停，CHAT授权保留。不宣称INSPECT READY或T05–T09全通过。
- 新候选5d8d0fe402b2cad33f321737f78247d6d8a81d5f/tree bbc20c047da1e0fe77aa8325ee4ca2bc1c6de1de已推送独立分支；slirp仅经 `/usr/bin/unshare --mount --propagation private --` 启动，保留sandbox/seccomp/default-drop/精确owner检查，失败无直接启动兜底。
- 网络policy增加挂载隔离契约，旧carrier摘要不复用；29定向测试通过、1跳过、0失败。宿主已安装util-linux 2.32.1的手册声明propagation递归设置；子namespace实测全部挂载无shared/master标记。
- guarded native预检进行中，将比对PID1及三个保护进程完整mountinfo、namespace、startticks和cgroup membership。候选未安装；待预检与新policy真实图文carrier通过才恢复单Agent INSPECT。
- 根因仍为slirp sandbox挂载传播假设；上游源码获取失败，未写成已证实。原任务423保持completed且不重复验收POST。

# T05–T09 真实业务闭环验证：尚未全部完成

## 当前结论（2026-10-06 18:13 Asia/Shanghai）

**T05–T09 整体尚未完成。下方早期条目均为历史记录，不是当前线上状态。**

- Web `4403172/172` commit `fe6d4d542079bdf07f5b5fcf2ff96e7f217be33e` / tree `a8e42ded0fbec8a26d6e4aa9f719473cc165e524`：3167pass/2pending/0fail。首次部署磁盘满，保存完整主机日志；仅删除本任务已dispose的临时measurement binary snapshot（不是其他任务数据/证据/发布副本），然后只重试同Run部署，不重建。实际新作业529712028/部署70660502SUCCESS；同Run制品SHA d88e467b45821acb94425786ae55be8ce0d1b1fb639663cc59fde38741bae49b与全部364安装/公网HTTPS文件字节匹配。
- 原任务423刷新已显示“已完成”。真实验收页保留156字节改稿和72字节星光问候，无checkbox；实际点击“查询验收状态”，用原key GET200恢复原fin completed，UI显示“验收完成/需求已完成”。没有重复finalizationPOST、创建任务或点将；后续status-counts/searchPOST仅为查询接口，不算业务写入。
- 真实公孙胜密议入口创建独立conversation1760458004866，单次CHAT request690e5758完成，实际回复“密议隔离验证已收到”；密议UI没有原榜文成果。同真实privateconversation取榜文typedoutcome404、取bountyindex404；正确bountyconversation取相同outcome200。证明同Owner榜文/密议scope隔离，不证明第二认证账号隔离。
- 当前CLI0.160、原有gpt-5.6-luna真实单modelturn完成图片+textfile语义验证。严格2case evidence SHA sha256:82a92c643df57096f07ad91c8ac4127bc6a09e829f4feb5db637ebad5c309754，绑定真实profile/policy/nativeattestation。不修改历史probeprofileID；scope使用同固定ID。audio此前实测unavailable，仍FAIL、不启用，不套用旧证据。
- 客户端4597e99b91ba95cefef2cf08d1eeedfb35cc049c/treeab234723264ed1e7f2faceac71fb156b21d59397：55定向诊断PASS，scope仅精确oneAgent。32inbox全空/DB活动lease0后备份前值，固定candidateSHA单次写入+readback，再调用既有installer。57payload摘要全部匹配，release已安装但**运行时激活失败**。
- 新阻塞：systemd在Node执行前报stepCGROUP/219；PID1和本会话均没有/sys/fs/cgroup挂载，/sys/fs/cgroup/systemd不存在。unit与安装前字节相同，不能归因应用代码或伪称READY。sharedMainPID0后仅停止该失败服务的自动重试，当前inactive；未重启API/wuyong或他人服务。API PID1635406健康UP，wuyong PID1145032仍活。
- 需要新增明确授权：只恢复主机cgroup挂载拓扑、随后仅重启codex-ws-agent；不重启主机/API/wuyong/其他服务，不绕过systemd。恢复后实测READINESS，再进行新的独立媒体目的任务（原423已完成，不重建/重放）。图文carrierPASS不是浏览器T07PASS。

| 项目 | 当前真实结论 |
|---|---|
| T05 | 纯文字多成果/早期定项替换/保留历史与兄弟成果PASS；媒体子集仍待验证 |
| T06 | 纯文字精确清单/无checkbox/下载同字节/保存非前置/原keyGET恢复验收完成PASS |
| T07 | 真实文字与密议CHATPASS；混合/附件-only/澄清/工具/媒体浏览器未完成；audio载体FAIL |
| T08 | 文字保存重开同字节、匿名与错误scope、真实private隔离PASS子集；第二认证账号和媒体待验 |
| T09 | API113/Web172发布证据PASS；client4597安装摘要PASS但激活失败，完整业务NOT_COMPLETE |

关键证据：web172-online-verification.json、web172-original-finalization-get-completed.json、real-private-task-outcome-isolation.json、inspection-current-01600-image-text-carrier-probe.json、client-4597-installed-activation-cgroup-failure.json。

---

# T05–T09 真实业务闭环验证：当前未完成

发布证据核对时间：2026-10-06T08:29:20.184226+08:00；业务状态更新：2026-10-06T10:28:12.907654+08:00（Asia/Shanghai）。任务定义来自当前 SDD 特性工作树，而非主工作区的旧 api/web checkout。

## 已实际验证

- API Flow `5260799 / Run112`，源码 `329d44fd7f8d0b2402853f5eac4cf47c99fcbed9` / tree `69d2cb5448aa165b35ead9794bac0971736f1a7d`；构建、部署成功，部署单 `70646647` 单主机 healthy。独立读取同 Run 制品回执/JUnit XML，安装 JAR 与制品摘要一致，进程归属监听与健康 UP。
- Web Flow `4403172 / Run168`，源码 `f6b81b40ee4a579c579af4cb7ab1e0e76e362173` / tree `3f70c8a345ef09359b0169785ec66d5f8cdf5102`；测试、扫描、构建、部署成功，部署单 `70646814` 单主机 healthy。独立复核制品全部 364 个 dist 文件和实际公网 HTTPS 字节/摘要，一一匹配。
- Web 云测 3146 PASS / 2 pending / 0 fail；API XML 共 2667 条执行项 / 0 fail / 0 error / 101 skipped，跨 selector 可重叠，不能作为去重后的用例数，skipped 不算通过。
- 当前 Web 源码已移除验收多选，包含完成文字来源、明确成果关联和冻结验收引用。此项是源码事实，不是浏览器业务验收。
- 本任务专属浏览器以测试身份成功登录。真实创建任务 **423**（201）并点将公孙胜一次（200），未重建任务、重复点将或重放 START。Bootstrap 仍 RETRY；没有已持久化会话/初始请求或 Agent 成果，不能把 HTTP200 算成闭环通过。
- 用户已授权继续修复。客户端修复已安装：仅测试 Agent 的精确七维 managed CHAT scope、真实0.160.0版本/协议信任测量、READY转变后的 acknowledged registration，以及全 managed identity 的 CHAT目录隔离。新模块与57文件制品摘要已核对；wuyong-local PID1145032 未变化；未操作 API/Web 进程或直接生产 DML。
- 当前客户端 commit `62a556dfbe7f9004349790c460b5f4c6ca87809c` / tree `14b2dfcf02d056b66eaa4e6d255f97bec60418aa`，共享 PID1479890。10:11:43 收到实际 READY 回执；仅测试身份的一次只读原生 GET 返回200，未读回任务正文、消费或执行队列命令。这证明原生身份校验当时通过，不是产品验收。

## 未完成范围

| 任务 | 真实业务状态 | 下一步 |
|---|---|---|
| T05 | NOT_RUN | 纯文字直接验收；真实多成果改一项后保留其他项，刷新仍一致 |
| T06 | NOT_RUN | 用户所见精确清单直接验收、继续修改，不要求先保存 |
| T07 | 已尝试，Agent 回复前阻塞 | 真实 Agent 无资料/混合资料/附件-only、自然澄清、工具执行与实际媒体 |
| T08 | NOT_RUN | 保存重开同字节、刷新不重生成、跨账号/任务及密议隔离 |
| T09 | 发布基础核验 PASS；产品闭环 BLOCKED，未通过 | 已发布候选的登录后浏览器业务验证 |

## 新根因与正式修复（尚未上线）

客户端 READY 重新注册修复后，**09:51:02 起真实错误已变为 `ChatDeliberationService.taskFacts` 的 `Chat request is unavailable`**。09:56及后续失败也是该站点。先前把未变化的外层 BOUNTY_ADMISSION_UNAVAILABLE 当成 registry 持续失败的判断已纠正，详见 `api-bootstrap-owner-context-root-cause.json` 与完整真实堆栈。

后台 bootstrap 不经过浏览器身份过滤器，而 AgentService.getTask 及其嵌套投影读取依赖 EsContextHolder 的 owner/client。议事准入已从 ServerResolvedSender 和精确加锁会话获得可信身份，但任务读取没有安装该身份。最小修复仅在任务事实读取期间派生独立可信上下文，finally 恢复原对象；保留所有身份、scope、事务、grant、幂等与 runtime readiness 检查。覆盖空/错误线程上下文、失败恢复、错投影、跨 Owner 拒绝；未扩大权限或新增数据操作。

API 修复 `4e0091ea16959885d0ba13316a094ea6cb37fae1` / tree `b23ed800895f7870938d5082c8a8ebd4f34845d6` 已合入远端 develop。正式 Flow **5260799 / Run113 SUCCESS**；Flow sources、checkout 和同 Run 回执均确认精确 commit/tree。报告2670条执行项，0 fail / 0 error / 101 skipped（跨 selector 可重叠）；新增3项上下文回归全部实际执行通过。制品SHA256 `409eb4820030a6ea1865baab77587f7684f06795bdb3d43413d7e6aa3c31dcd6`。候选未部署。

已只读核对实际 deploy adapter：没有精确 backend-nightly intent 即返回 DEFERRED。正常下一发布为 **2026-10-07 00:00（Asia/Shanghai）**。未伪造夜间 intent、绕时段、重启 API/Web 或本机构建。不能把白天 Flow SUCCESS（如后续成功）写成已上线修复或业务通过。部署后必须沿原任务423继续业务验证。

当前仍未产生可验收 Agent 成果。T05/T06/T08 为 NOT_RUN；T07 真实尝试在 Agent 回复前阻塞；T09 已核对原发布基础，但产品闭环尚未通过。INSPECT/混合输入、实际媒体、自然澄清、工具执行、成果替换/验收、保存同字节及隔离均仍需真实运行证据。

自检与恢复范围见 `api-owner-context-remediation-self-check.md`、`remediation-scope.md`。稳定发布事实与候选、云端验证、生产激活、业务验收分开记录。

原始查询、独立校验和分层结论见同目录 `summary.json` 与各验证 JSON/脚本。日志查询存在 `outputTruncated=true`，未以末尾日志推断测试总量；测试摘要来自同 Run 制品报告。

## 最终只读核对 2026-10-06T10:33:53.855402+08:00

Run113 部署作业与部署单70652679为 Success，但作业日志正文为空，未取得实际DEFERRED输出，不能伪称已读到该标记。实际adapter要求精确夜间intent；Run113 intent不存在，安装记录仍Run112，实际JAR仍旧摘要，API PID1229757不变。证据见 `api113-deployment-readback.json`。任务423仍RETRY（30次），未产生会话或请求。

实际夜间controller会为届时remote develop启动**新Run**，不是直接安装Run113；必须另行核验新Run精确源码、云测、同Run制品及健康，不能保证定时发布成功。本次不绕过发布窗口。

等待授权期间已关闭本任务专属浏览器并停止精确task423只读observer；未停止API、共享Agent或其他聊天进程。重新验证需再次登录，继续原任务423。

## 用户授权提前发布（2026-10-06 16:24北京时间核验）

用户明确“同意授权”本次通过现有Flow提前发布及API正常重启。Run113原成功部署作业一次retry请求被接受，但状态/部署单/安装记录未发生实际重执行；没有盲重试。随后复用既有 `5264702/cyf-ops-manual Run10`，仅调用原事务installer安装原release Run113精确制品，不做构建或SQL。提前授权使用独立 `user-authorized-early-release` 精确Run/源码/制品/旧版本绑定，不伪造nightly intent。

运维Run10与部署单70658650成功；独立核验安装记录Run113、commit4e0091/treeb23、JAR9a6abaa一致；实际PID1635406、监听归属与健康UP。运维Flow原配置和部署adapter原摘要均已恢复，唯一临时授权文件已删除。wuyong PID1145032未变化。业务仍需原任务423自动intent继续验证，发布成功不等于T05–T09通过。

## 2026-10-06 16:46 真实首轮完成与前端续办修复

原任务423的原bootstrap在第101次自动尝试ADMITTED，唯一会话1760458004865、原请求mmd-typed-request_e4eb2dfe122aa387c8423e807ba662597cf26afe。客户端误将targetCapability.runtimeVersion不透明协议声明当SQL Long；精确字段分类修复fe2583e4278d276ef2a60936c29aaad8a062f868已安装，40项定向诊断通过、57文件payload匹配，共享PID1645227。原dispatch自动重送，实际Agent交付两句欢迎语；消息1723448及最终摘要ea47c139049078a84f4703d4e6e39c9d606b8b86fc6249d0df113e7cd020b00e，deliverable=true，steps=[]，无伪造工具执行。

真实验收面板已显示text/plain159字节和原文字、零复选框、下载/确认验收/继续修改；保存不是前置。继续修改回到原会话。但新增第二份文字的发送点击未产生POST，草稿保留。根因：真实TaskDTO根本无assignmentRevision，Web从不存在的字段取版本而静默拒绝。

隔离Web候选89b7cfafca161ff9367553b93db875cb5e27b494/tree17d71245c5137a42acde00b8aeda1d603614c965已经合入develop，仅使用当前鉴权ATTACHED点将投影、精确task/target/conversation与canonical taskVersion核对，绝不把taskVersion充当assignmentRevision或修改TaskDTO。丢失绑定时仅GET核对原点将，身份/会话/草稿变化阻止发送，缺失上下文明确报错。105项轻量定向诊断通过；正式4403172 Run169正在测试构建发布，不冒充上线通过。

T05/T06只部分实测通过；多成果APPEND/定项REPLACE、确认验收、T07真实媒体与T08保存隔离尚未完成。另观察到共享测试Agent native队列401，尚未确定根因，不默认禁用或绕过认证。

## 2026-10-06 16:57 真实文字可选保存；云端失败已定向修复

实际选取原assistant消息1723448全部53字符，UI一次POST archive-operations200，operation arc_65476f30a87d4df9937215889e7ef03f，file pws_f73f8168c22c445080ea3281011f7d97 v1。经百宝箱真实“查看”重新打开，GET固定v1预览200且显示相同原文；真实“下载”GETcontent200，捕获下载Blob159字节/SHA256 4681f060466688de3114b4984e2a92e34ae1baae1e37b737656670d2eca8cd7e，与原选区和版本元数据完全相同。未生成新Agent请求。

Web Run169 FAIL（3160passing/2pending/1failing），仅另一份抽取实际handleSendHallMessage函数的测试夹具缺少新增typedAssignmentRevision依赖。失败完整日志more=false/outputTruncated=false已记录，未跳过测试、重试同输入或本机构建。夹具修复6117332543cb551a1388865b6075b39901ecff2b/tree0b9c1cb1e3b1e62908e1f8c1b4ccdfc6a7ec5ea7，112项相关定向诊断通过，已合入develop并启动现有release Run170。Run169没有构建制品或上线；当前线上仍Run168。

## 2026-10-06 17:34 续办：真实多成果改稿与服务端验收

Web170已SUCCESS，3161pass/2pending/0fail，同Run制品及全部364个安装/公网HTTPS文件摘要独立核对通过。不是仍RUNNING；线上6117332。

客户端ACK新根因：持久ACK绕过正常协议封装，没有runtimeInstanceId，触发服务端精确会话身份拒绝并disconnect，后续native401和typed503。保持服务端校验，635431fda9ea53e3defd90949a1b6bcc4bda3f8e/tree6ad004ac49ee846b4844ffc266d44cb1cae76f66在实际发送时绑定当前进程身份；42诊断PASS。核对32个共享inbox均空、数据库活动lease均0，经既有installer安装57文件全部摘要匹配，实际PID1669046。测试CHAT scope摘要不变；API1635406、wuyong1145032未改变。READY和nativeGET200实测，随后两次CHAT真实完成，未出现旧native401。

原503 intent先用原key GET核对404（404本身不证明未受理），再由实际“刷新处理状态”按钮显式恢复同key/body，一次202。追加成果f80cfd6a真实ANSWER/APPEND；实际“继续修改”后另一次用户操作仅改第一份，afb22ebb真实REPLACE，明确target=原e9edc1a/outcome及原digest，causal parent=星光第二份63b273ad。刷新历史保留旧稿；验收清单仍恰好新第一份156字节+未变第二份72字节，0checkbox。两个实际下载Blob SHA与selectedOutputs完全一致。

实际“确认验收”一次POST200，operation fin_32ddd2fab9426b1f5645fe3e0b4bd1e9f544c55d967ab6c729d01b8b6f0a32a9，TASK_COMPLETED/accepted/taskVersion4。未保存新稿，未伪造工具run。服务端验收成功，但浏览器提示UNKNOWN：实际text receipt带stepId:null/outputId:null，严格前端仅接受请求形状。最小修复只验证这些明确null槽，不接受伪造ID/未知字段/错摘要/顺序；38定向诊断PASS。保留另一Owner已合入的446cfbe界面修改，非重叠变基后1e5b21c8f95b619af2ea012df2bbcaf48d6e2400/tree269c3858401431779841a359b795d106f24183d1合develop，现有release Flow171正在运行，未本机构建。后续只通过原key GET恢复已完成验收，不能再次POST或创建新验收。

只读真实API再次核对原fin completed200；相同fin错误task424返回404，typed outcome错误conversation返回404。不是第二认证账号/已验证密议隔离证明。最新0.160精确managed模型gpt-5.6-luna的隔离/受限网络/TLS测量PASS，但contractReady=false/carrierEvidence=null，未据此启用INSPECT；旧0.159.2/Terra载体证明不可套用。

T05服务端文字闭环通过，T06最终浏览器完成状态待修复上线复验。T07真实媒体/附件/动作、T08媒体及第二认证账号/密议、T09完整业务仍待验证；不得全部写PASS。
