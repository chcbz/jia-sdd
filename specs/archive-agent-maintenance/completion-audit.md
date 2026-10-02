# 源码完成审计：尚未闭合的 D2 需求

日期：2026-10-01。审计对象：root68a34ed7 / API62223001 / Webbdff4786 / Clientbc035b37。
该基线已提交并推送，但**不构成完整特性开发完成**。上一轮109项检查仅覆盖提交、tree、远程与证据一致性，不覆盖每一产品要求；现继续按原D2规格补缺，不缩减目标。

## 已确认或待独立核对的源码缺口

1. **下架与默认版（CONTENT-11）**：design§7.2 POST `/works/{wid}/editions/{eid}/withdraw`、§12.1管理者下架。当前Admin Controller/service/Web gateway无withdraw；publication schema虽有WITHDRAWN，尚无可操作事务。Reader仅按PUBLISHED查询，未区分已下架410与不存在404。需要精确withdraw ACL、work CAS、显式替代版本、active置空、旧私人数据保留和真实MySQL/HTTP负向验证。
2. **缺输入/缺任职维护单与resolve-input**：design§5.2/§7.2要求WAITING_INPUT/WAITING_ASSIGNEE和resolve-input。当前createJob先要求当前任职及READY source，schema将appointment/source非空；缺项无法形成可补全的持久维护单。需要按原权限/不可变来源及唯一意图推进，不用“先到表单填齐”替代需求。
3. **完整管理接口**：draft block GET/PUT、draft PATCH/validation/publish、operations/{oid}等精确合同路由尚缺；部分有job-aggregate等价操作，但是否满足合同尚需逐项核对，不能以现有实现倒改规格。原件 `evidence/completion-audit/admin-route-observation.json`。
4. **Web完整维护体验**：当前有任职/维护单/草稿sections，但design§12.1三个页签、版本与记录/修订差异/下架及显式书目scope输入尚需源码和行为核验。现有245组件测试不自动证明这些需求。
5. **开发集成验证**：目前有界HTTP/JDBC/POSIX/Client fixture替代了identity/registration/admission/transport/install transport；不能证明真实共享执行/安装及双聊天入口全链。完整源码完成审计正在独立只读核查；后续补隔离Runtime/真实HTTP开发验证，不调用付费模型或生产。

## 必须保留的事实

- 已完成组件提交/push、245 Web PASS+build、173定向API PASS、MANUAL/AUTO有界fixture通过仍有效；原始失败/复审和scope不改写。
- API11与Client1既有失败不假称全绿。历史文档checker仍报旧Client source hash，不用current gate伪替代。
- 84真实业务验收全部not_run；生产管理员/底本/公共发布用途/生产任命/付费/部署仍需另行授权。
- 后续源码单Writer串行，Reviewer只读；不覆盖原工作区、不同任务分支或批准技能包字节。完整goal保持active，不能以已推送的部分源码标complete。

## 独立只读审计阶段结论

Reviewer于2026-10-01明确返回 **NOT_COMPLETE**：未发现P0，确认4项P1——下架链路缺失、等待输入/任职与resolve-input不可表达、刷新/合法接管后无法GET恢复完整validation facts、Web缺版本/预览/下架及EXPLICIT_WORKS选择。最后一项恢复问题来自openJob清空validation且只读job/events/draft/recovery，发布按钮却依赖内存validation.outcome；不是仅缺一个界面标签。

独立阶段未裁定draft block/PATCH与whole-draft PUT等价、operations/{oid}替代、全部84项/M0-M8/U1-U9或真实Runtime/浏览器全链。不得把该局部审计说成全面需求PASS。

下一源码包已授权唯一critical_writer：API withdraw/版本可见性/独立ACL与事务、版本history与当前validation GET；随后Main持锁隔离实库验证，再独立只读复审。WAITING_INPUT/ASSIGNEE/resolve-input、Web完整管理路径和其他精确接口仍需后续补齐。原完整goal保持active。
## API 补缺包一：候选与实库验证

2026-10-01：唯一 critical_writer 已补新增管理端下架、版本列表/详情、当前 revision 校验 GET 与 Reader 410。候选 source tree 为 `8b8c4665c5eb43b1c0a34b54c9093ab8dff0f424`，组件 HEAD 仍为原 `62223001`；**本候选尚未提交/推送，独立只读复审进行中，不宣布全特性完成**。

Main 全程持共享 Gradle 锁执行四套真实隔离 MySQL：platform74/native6/maintenance104 全 PASS（定向184/184）；archive270/259PASS/11既有FAIL/0skip，Gradle exit1。与 fbc4a8f9 基线直接逐失败比较 introduced=[] / removed=[]，前后同 tree、XML 全部 fresh。原件 `evidence/native-lifecycle/withdraw-api-attempt4/`。

前轮 attempt1 编译错误、attempt2 新 CHECK 单项 IN 的 MySQL 实际等号表达差异、attempt3 测试 FK 初始化顺序/精确断言错误均已保存，未删除失败轮或放宽约束。旧 schema 升级 fixture 的前15表 DDL 逐字节等于62223001的 Git blob，绑定见 `previous-schema-binding.json`；真实升级和畸形断点 fail-closed selector 已运行。

当前范围边界：withdraw audit/outbox 持久 PENDING，未新增 dispatcher；HTTP 此轮为 Controller 合同测试 + 实际 Service/JDBC，不是 live HTTP/Runtime E2E；Web 尚未接入新增合同。后续仍须补等待输入/任职与 resolve-input、剩余精确管理接口、Web 版本/预览/差异/下架/显式范围及 validation 刷新恢复、隔离共享 Runtime 和真实浏览器验证。84业务验收仍全部 not_run，不擅自生产激活。

独立首轮复审结果为 REJECT_LOCAL_API_SCOPE（P0=0/P1=1/P2=1）：editionHistory 非同事务的三段读取可产生旧版本列表与新 workRevision/active 的混合快照，已交回唯一 Writer 补原子读取和实库并发测试。P2 为持久 PENDING 尚无投影 dispatcher，不破坏直接 DB 可见性，但不得声称通知最终收敛。原回执摘要见 attempt4/review.json；其他下架/权限/校验/升级局部项已认可，尚不宣布第一包通过。

首包修复后的 attempt5：tree `16fbbff2e0df67d042142e51ec3c107e802ee0bf`，focused185/185PASS；archive271/260PASS/11既有FAIL/0skip，Gradle exit1，failure delta空、fresh XML、前后同tree。独立复审 **ACCEPT_LOCAL_API_SCOPE，P0/P1=0**，history 混合快照已通过锁定读取和有效 latch 实库测试闭合；outbox P2 边界保持不变。原件 `evidence/native-lifecycle/withdraw-api-attempt5/`。

Main 已保存本地 API commit `05875268c0c8cc991951f2dcb3fef9d29204e702`，其 tree 精确等于 tested/reviewed tree，提交后工作树 clean。**未 push 首包增量、未更新根仓 gitlink/pinned SHA 为未推送提交，不宣称特性完成。** 当前唯一 Writer 已继续第二包 durable WAITING_INPUT/WAITING_ASSIGNEE、resolve-input 与必要 schema/最小聊天接线；剩余精确 draft/operation 接口、Web 和完整开发集成仍在其后串行补齐。

## API 补缺包二：真实等待维护单

2026-10-01：durable WAITING_INPUT/WAITING_ASSIGNEE、resolve-input、精确 direct target 和最小 Chat 接线候选已冻结为 tree `0e8e8b7ca39119759812a0b4004058f6892da7b5`，父提交为 `05875268`。无完整候选时不创建 run/draft/grant/lease/command；来源及作品冻结后不原地替换。第二包源码尚未提交/推送，独立只读审查进行中。

Main 全程持共享锁执行四套真实隔离 MySQL：platform74/native6/maintenance113，定向 **193/193PASS**；archive279/268PASS/11既有FAIL/0skip，Gradle exit1。相对首包 attempt5 的逐失败比较 introduced=[] / removed=[]，XML 全 fresh、前后 tree 相同。原件 `evidence/native-lifecycle/waiting-api-attempt3/`。attempt1 编译失败与 attempt2 的5项新测试失败均保留，修复未放宽 source/target/授权/CHECK/FK；attempt3 相对 attempt2 仅修测试合法 fixture 与正确负向断言。

本结果仅为局部源码实库组件验证，不是 live HTTP/共享 Runtime 全链或业务验收。六条精确 draft/operation 管理路由、管理作品枚举、Web 完整维护体验与开发集成继续按 D2 补齐，不以本包 PASS 宣称 whole-feature complete。
第二包 attempt3 独立只读裁定 **REJECT_LOCAL_API_SCOPE**（P0=0/P1=2/P2=2）：resolve-input 的已提交 receipt 未在 by-key allowlist；manager-first 等待单跨 direct 入口重放未冻结 exact target。另发现 waiting/cancelled nullable CHECK 不够精确，及 resolve 对撤权/换任缺真实双连接 latch 证据。已回交唯一 Writer 窄修；原件摘要 attempt3/review.json。本轮193PASS只证明现有选择器，不能抵消上述审查缺陷。

第二包 review 窄修候选 c035e8b 的 attempt4 编译通过，但新增 CHECK selector 的 appointment 缺 slot FK fixture、by-key foreign waiting 负例 helper 将 nullable appointmentRevision 拆箱，导致定向117/2FAIL与archive283/13FAIL（11既有+2新增）。原始XML/日志及前后同tree/failure delta已保留 attempt4/。唯一Writer仅修两个测试文件：合法slot→appointment、明确CHECK名称断言、29参nullable构造保留target/null；新tree d15130e3 的 attempt5 实库验证正在执行，未预先宣称PASS。

修复后 attempt5：tree d15130e3，platform74/native6/maintenance117，定向 **197/197PASS**；archive283/272PASS/11既有FAIL/0skip，Gradle exit1。相对首包直接 failure delta空，前后同tree、XML fresh。CHECK负向测试已确认约束名称（不是FK假绿），两项真实latch撤权排序已运行。独立只读窄复审进行中，未提交/推送第二包，整项goal仍active。

第二包最终窄复审 **ACCEPT_LOCAL_API_SCOPE，P0/P1/P2=0**。Main已保存本地API commit **a1c39dcf04f91102879c1a73bb9e0a44ffb2a851**，tree精确等于tested/reviewed d15130e3，提交后clean；尚未push、Root gitlink与pinned SHA保留远程62223001。原件 attempt5/review-final.json。当前唯一Writer继续第三包六条精确draft/operation接口、管理作品枚举（active=null仍可管理历史）及D2管理者以新human授权接管撤任Agent合法草稿；Web和开发Runtime全链仍在其后。整项不宣布complete。

## API 补缺包三：精确管理合同候选

唯一 Writer 已冻结第三包 tree `b90e85b59bb51fc9ea1f1471ac6a6b6f4b8f715d`（base a1c39dcf）：六条精确 draft/operation 路由、当前管理作品枚举、同事务不可变 operation receipt，以及以当前 human manager 授权接管撤任 Agent 合法草稿。Main attempt1 实库编译通过，platform74/native6PASS；maintenance121/1FAIL，archive287/12FAIL（11既有+1新增），前后同tree/fresh XML。新增失败来自旧 job-aggregate `VALIDATION_FINISHED` 被重命名为 human 前缀，而非 source 校验被放宽。已回交 Writer 保留旧事件类型并仅追加 human 审计事实；不改旧负例来假绿。原件 `evidence/native-lifecycle/exact-admin-api-attempt1/`。

### 逐 D2 收口中额外确认的源码缺口

2026-10-01 源码只读观察：`ArchiveMaintenanceServiceImpl.publicationDto` 仍将 `readbackState` 固定为 PENDING；maintenance schema 尚无持久 readback 结果、检查项及核验时间。历史跨组件 fixture 曾真实 GET Reader 成功，但不能替代 D2§10.2 要求的 publication/operation 独立持久读回事实。后续须补“提交后服务读回成功/失败均可查询，失败不撤销已提交发布/不重复激活”链，不以生产未授权掩盖该源码缺口。

另需按完整管理合同复核固定来源上传状态：D2§7.2 列为202 source operation，当前 Controller 为201同步READY source DTO且无operationId。保留当前源码/设计事实，后续明确实现一致性，不能只检查方法和路径便当整个合同PASS。尚不宣布所有管理接口/整体API或完整特性开发完成。
第三包兼容性窄修后的 attempt2：tree **f50f84630c6eeddd659f69102eff070a2f5195aa**，platform74/native6/maintenance121，定向 **201/201PASS**；archive287/276PASS/11既有FAIL/0skip，Gradle exit1。Main 已独立 snapshot XML、前后 source freeze 和直接失败集合比较：XML fresh、source unchanged、introduced=[] / removed=[]。原件 `evidence/native-lifecycle/exact-admin-api-attempt2/`。当前独立只读复审正在进行；本包尚未提交/推送，不宣称完整合同或整项特性完成。发布读回与来源202合同仍作为下一串行源码包。
第三包 attempt2 独立只读审查 **REJECT_LOCAL_API_SCOPE，P0=0/P1=1/P2=2**。P1：validate 幂等摘要依赖当前可变草稿内容，首次校验成功→合法编辑→原 key/原 revision 重试会错误冲突而非回放原 receipt。P2：exact validate 事件前缀与标准类型分歧；managed works 将 CANCELLED 维护单当作 pendingJobId。原件摘要 `exact-admin-api-attempt2/review.json`。已交唯一 Writer 窄修及新增真实实库负例，尚未激活 readback/source202 或 Web 包。201PASS不抵消此次发现，不提交/推送被拒候选。
第三包三个审查项窄修的 attempt3：tree **4a236e61e27c2062e1a3f6807f0774cd92dfa70b**，platform74/native6/maintenance123，定向 **203/203PASS**；archive289/278PASS/11既有FAIL/0skip，Gradle exit1。XML fresh、前后source tree相同、相对第二包逐失败 introduced=[] / removed=[]。新真实MySQL验证校验成功→编辑→原key/revision回放原operationId/结果、changed request/stale新key回滚、当前撤权拒绝；并确认取消作业不再成为pending、FAILED显式恢复候选保留。原件 `evidence/native-lifecycle/exact-admin-api-attempt3/`。独立只读窄复审进行中，尚未提交/推送第三包；剩余包次序不变。
第三包窄复审 **ACCEPT_LOCAL_API_SCOPE，P0/P1/P2=0**。Main本地API commit **eb31260f372be78f82ac78ad8d47d178cf71b215**，tree精确等于tested/reviewed **4a236e61e27c2062e1a3f6807f0774cd92dfa70b**，提交后clean。原件 attempt3/review-final.json。未push此增量，Root gitlink/pinned API仍为远程62223001；下一串行包将补持久发布readback与Source202，之后Web完整管理路径及真实隔离开发联调。整项goal保持active。

## API 补缺包四：发布读回与 Source202 候选

唯一 Writer 已交 tree **7f12c9dfcd13583139cdfc396c24d823ffc41a52**（base eb31260f）。候选新增持久 publication readback PENDING/PASSED/FAILED、事务后真实 Reader 目录/章节/段落摘要核验与短事务 CAS；operation 原 result snapshot 与 current verification 分离。Source 返回202及真实可查询operationId/Location，复用持久 source operation，不创建假job/draft。尚未审核/提交/推送。

Main attempt1 编译通过，platform74/native6/maintenance127，定向 **207/207PASS**；archive293/13FAIL（11既有+2新增），Gradle exit1。XML fresh、前后同tree，failure delta确认2项新增。新失败来自 Question/ReaderData MySQL fixture setUp 的部分maintenance表集：清理名单遗漏既有confirmed_request/withdrawal，严格schema initializer正确拒绝。已回交唯一Writer核对并只修隔离fixture清理，不放宽生产partial/drift规则、不skip测试或删除失败原件。原件 `evidence/native-lifecycle/readback-source-api-attempt1/`。Main也已从eb31260f Git blob独立核对前代schema LF SHA256 c398de55，binding仅证明源对应，真实升级结果以XML为准。
第四包 fixture 清理窄修后的 attempt2：tree **e2a0f060bfca60b3969abeae2f3b844c2ceca4e2**，platform74/native6/maintenance127，定向 **207/207PASS**；archive293/282PASS/11既有FAIL/0skip，Gradle exit1。对第三包直接失败集合比较 introduced=[] / removed=[]；XML fresh、前后同tree。仅四处隔离fixture完整drop名单修复，生产schema严格部分集合/drift拒绝保持。原件 `evidence/native-lifecycle/readback-source-api-attempt2/`。当前独立只读审查进行中，不提前提交/推送本包或宣称Source/readback完整验收；Web、真实共享Runtime和浏览器开发联调及D2逐要求闭合仍未完成。
第四包 attempt2 独立只读 **REJECT_LOCAL_API_SCOPE，P0=0/P1=1/P2=1**：旧schema已有publication和fresh legacy Bootstrap未创建持久readback，缺行被硬编码PENDING且核验直接返回；另外核验未分别比较前言/章节段落数，分类数漂移但总数不变可漏检。207PASS没有覆盖这些路径。已交唯一Writer窄修Bootstrap/精确升级backfill与当前授权后的版本核验、分类计数及真实实库负例。Source202当前权限/可查询回执、新发布三入口事务外Reader核验、CAS和snapshot分离已在局部认可。maintenance schema实际18表，交接19表为口误不改DDL配口误。原件 attempt2/review.json；旧outbox PENDING无dispatcher仍为后续缺口，不宣称整体完成。
第四包旧出版/Bootstrap与分类计数窄修的 attempt3：tree **ea9dffa9dfe91b77290d97aafd67e01ef207e88a**。Main持锁真实隔离MySQL：platform74/native6/maintenance128，定向 **208/208PASS**；archive294/283PASS/11既有FAIL/0skip，Gradle exit1。XML fresh、前后同tree、与第三包逐失败比较 introduced=[] / removed=[]。实际运行 legacy Bootstrap 持久PENDING→PASSED、前言/章节分类总数不变漂移FAILED、已有publication升级补readback且私人/receipt摘要不变、Reader依赖失败publication/active不动及授权查询重试PASSED。原件 `evidence/native-lifecycle/readback-source-api-attempt3/`。当前独立只读窄复审进行中，尚未提交/推送第四包；withdrawal/job事件投影dispatcher、Web和真实开发Runtime/浏览器链仍待后续串行完成。
第四包 attempt3 窄复审 **REJECT_LOCAL_API_SCOPE，P0=0/P1=1/P2=0**。前两项legacy/backfill/Bootstrap和分类计数已闭合，但新Reader-I/O路径暴露P1：edition/history在首锁定快照后释放锁核验，直接用旧publication/work/授权和新verification拼返回；IO期间撤权可能仍返回管理数据，撤版可能混旧active/PUBLISHED与新FAILED。已交唯一Writer增加IO后最终短事务重授权和原子重读，并以精确IO窗口双连接latch验证revoke与withdraw；ReaderIO仍不得进长事务或持Agent lease。原件 attempt3/review.json。208PASS有效但不覆盖此新竞态，未提交/推送第四包、未激活Web。原outbox缺口继续明示。
第四包 IO后授权/原子快照窄修 attempt4：tree **58ebf2f5c2ec56a99c909adf8119f3b240c26e17**，编译通过；platform74/native6PASS，maintenance131/1FAIL，archive297/12FAIL（11既有+同1新增）。前后同tree/XML fresh。新增3个真实MySQL精确Reader-I/O窗口latch通过（edition撤权拒绝、history撤版新原子快照、operation撤权拒绝）；唯一新增失败是旧unit editionHistoryExposes... 在edition最终锁定重读返回404，已交Writer核对并只修合法锁定fixture/stub，不降低生产最终重授权或删负例。原件 `evidence/native-lifecycle/readback-source-api-attempt4/`；失败轮原件保留，整项和本包仍未验收/提交/推送。
第四包单元fixture锁定publication读取窄修后的 attempt5：tree **30f0c7c641c3b7c14ef6afe180541ab95dfa1cc1**。Main持锁真实隔离MySQL：platform74/native6/maintenance131，定向 **211/211PASS**；archive297/286PASS/11既有FAIL/0skip，Gradle exit1。XML fresh、前后同tree、与第三包逐失败 introduced=[] / removed=[]。三个精确Reader-I/O窗口实库latch全部运行（版本撤权拒绝、history撤版后原子快照、operation撤权拒绝）；attempt4唯一unit404通过补合法locked publication stub修复，生产最终重核未放宽。原件 `evidence/native-lifecycle/readback-source-api-attempt5/`。独立只读窄复审进行中，尚未提交/推送第四包、未激活Web；outbox和真实开发Runtime/浏览器及D2完整逐项闭合仍待后续。
第四包最终窄复审 **ACCEPT_LOCAL_API_SCOPE，P0/P1/P2=0（本包scope）**。Main已本地API commit **18d664193c40ca82246694f2b5fa5249d07c57d8**，tree精确等于tested/reviewed **30f0c7c641c3b7c14ef6afe180541ab95dfa1cc1**，提交后clean。原件 attempt5/review-final.json。未push本包，Root gitlink/pinned API仍为远程62223001；既有outbox dispatcher缺口未被此接受消除，Web完整管理和真实Runtime/浏览器开发联调仍待完成。整项goal仍active，不宣称特性开发完成。

## Web 完整维护补缺：首轮候选

Curie 首轮候选 Web tree **6582f330e2060125048a08d4c6fada4503a0669a**，base bdff4786、API合同冻结18d66419。Main 六个 archive/JuyiHall selector **246/246PASS/0pending**，`npm run build` exit0；前后tree相同，原件 `evidence/web-wiring/web-complete-maintenance-attempt1/`。本候选含三tabs、worksScope枚举、等待补输入、exact block/PATCH/operation与版本下架入口、Source202查询及Reader410提示。源码/行为是否满足完整任务仍在独立只读审查；新mounted UI覆盖、缺任职补全、非JSON-only章节编辑、修订差异及当前身份/operation收敛需逐项核对，不以246旧/新混合测试等价Web完成。Web尚未提交/推送，业务outbox和真实Runtime/浏览器链仍在后续。
Web首轮独立只读 **REJECT_LOCAL_WEB_SCOPE，P0=0/P1=5/P2=2**：历史/下架capability错配；resolve-input未提供exact任职/skill与缺newWork；validation合法404阻断新草稿；JSON-only编辑和真实修订diff仍缺；202成功过早释放key且bykey不hydrate结果，无法PENDING/lostGET恢复。P2为tab真实焦点/tabpanel关联与新UI mounted覆盖缺失。已交唯一Curie修完整scope和mounted负例，不改API/Client。246PASS+build0只证明现有selectors，不能抵消这些源码缺口；原件 web-complete-maintenance-attempt1/review.json。API四补缺包保持已review本地提交，Web候选不提交/推送，goal继续active。
Web修复首个checkpoint（非SOURCE FREEZE）：Curie报告部分gateway/结构化表单/capability/validation404已改，但完整版本diff及newmounted覆盖仍缺；Main未将该partial树冻结/测试/审核。只读diff还发现首轮actualcreateApi PATCH/withdraw/source202回归selector被删、fixture draftId/exact202响应回退旧shape，已明确要求恢复并增强真实冻结合同，不以删测试后的10PASS为完成证据。唯一Curie继续同scope，API/Client保持冻结；Main准备新增mounted selector runner，收到真正SOURCE FREEZE及selector清单后才运行完整tests/build/独立review。
Web 完整补缺候选 attempt2：tree **ce702e1c4630a5885dc093738a45a8fc1eb2a186**。Main 六 selector **255/215PASS/40FAIL/0pending**，前后同 tree；40 项失败均为旧 Reader SFC 测试 harness 只删除字面 `defineExpose({ back })`，新增真实 `openEdition` 导出后产生 duplicate defineExpose。生产 build 尚未启动，不把 Curie 的20项自检当作六套通过。已交回唯一 Writer 最小更新合法 harness，保留全部旧编辑/阅读测试与新精确版本入口，不 skip、不删除失败轮。原件 `evidence/web-wiring/web-complete-maintenance-attempt2/`；既有第一轮 REJECT 和源码缺口继续保留，整项 NOT_COMPLETE。

Web harness 窄修后的 attempt3：tree **5435f01df857a16cf2443b816b7af92fbd5aca1f**。Main 六 selector **255/255PASS/0pending**，`npm run build` exit0，前后同 tree；原件 `evidence/web-wiring/web-complete-maintenance-attempt3/`。40 项失败只通过单一 macro 合并合法 Reader test seam 修复，旧测试全部保留。独立只读审查已按原完整 Web 任务及首轮5P1/2P2激活，包括真实 Edition DTO 差异、operation 消费与读回、WAITING_ASSIGNEE、各路径撤权 fence；测试绿色不替代这些需求。尚未 Web commit/push，业务 outbox 与 Runtime/浏览器链未激活，整项仍 NOT_COMPLETE。

Web attempt3 独立复审 **REJECT_LOCAL_WEB_SCOPE，P0=0/P1=5/P2=2**：ALL_WORKS 与实际 API COLLECTION 枚举错配；差异 UI/test 假造 Edition DTO 不存在的 content；openEdition 仅加载未打开正文；大多数读写401/403不清旧权限数据；同work版本晚响应可覆盖当前选择并错撤版。P2：阅读按钮需 PUBLISHED+PASSED，任职摘要需当前binding/scope/skill事实。原件 attempt3/review.json，255PASS与build0不能抵消这些缺陷。首轮部分 structured PUT/PATCH、validation404、current appointment snapshot、Source202 recovery、withdraw DTO及焦点已局部认可；真实版本diff/Reader入口/撤权/延迟版本及410私人数据 mounted覆盖仍须补齐。当前 Curie 已freeze idle，下一唯一Writer按 ACL/竞态路由转 critical_writer Knuth；业务outbox尚不激活。

critical Writer 合同修复后的 Web attempt4：tree **0039bcce0a93e8f50f895c34f28a279756fb9b66**。Main 六 selector **264/264PASS/0pending**，build exit0，前后同 tree；原件 `evidence/web-wiring/web-complete-maintenance-attempt4/`。新增真实 Reader DTO 对比、组合历史版本正文打开/焦点、410私人数据不写、直接读写401/403清理、同work/ABA/比较晚响应、COLLECTION/EXPLICIT_WORKS、PUBLISHED+PASSED与任职摘要、冻结work的WAITING_ASSIGNEE与validate202消费等覆盖。测试和fetch夹具只证明局部 Web 源码行为，当前独立完整复审仍进行中，尚未提交/推送 Web，不宣称实际浏览器/共享 Runtime 全链或业务验收。之前 attempt2 失败和 attempt3 REJECT 原件继续保留。

Web attempt4 独立只读 **REJECT_LOCAL_WEB_SCOPE，P0=0/P1=2/P2=1**。先前5P1/2P2及冻结work waiting/validation已闭合，但发布202仍在 accepted=COMMITTED且权威GET404/5xx时提前丢原键，readbackPENDING可再发布且无明确operation刷新；publicationOperation未绑定job/draft，切job/晚返回会串结果/阅读入口与禁用状态。P2为任职exact requiredSkill包SHA摘要显示缺失。原件 attempt4/review.json，264PASS与build0真实但未覆盖此窗口。已交回唯一critical Writer最小修复及新增完整mounted负例，未commit/push Web、outbox仍未激活，整项 NOT_COMPLETE。

Web 发布恢复窄修 attempt5：tree **13d4b42eac1acc1ae279151fc2c3973bec2f3387**。Main 六 selector **267/267PASS/0pending**，build0、前后同 tree；原件 `evidence/web-wiring/web-complete-maintenance-attempt5/`。新增202 accepted COMMITTED后operation缺失保原键、权威完整receipt匹配消费、明确刷新当前verification与禁止第二POST、跨job A/B/A迟到POST/GET/bykey、不可人工丢弃未知publish key和任职精确包SHA等覆盖。当前独立窄复审进行中，不预先提交/推送Web；旧两轮REJECT及40宏注入失败原件不改写。真实业务outbox、共享Runtime及浏览器开发验证与完整D2审计仍在后续，整项 active/NOT_COMPLETE。

Web attempt5 独立 **REJECT_LOCAL_WEB_SCOPE，P0=0/P1=1/P2=0**。此前202未知保键/明确刷新核验/第二POST防止、跨job发布epoch隔离与精确skillSHA已闭合。剩余P1：所谓完整权威publication判断接受原不可变result.readback PASSED/FAILED、缺nested初始verification及current verification只有state的畸形形状，且先显示后判断，可能非权威DTO出现阅读链接。需按实际 ArchivePublicationDTO/VerificationDTO 精确验证 immutable PENDING snapshot 与独立current facts、统一以同predicate显示/消费，并补畸形DTO保key/无readlink/无二次POST负例。原件 attempt5/review.json；已交同唯一critical Writer最小窄修，267PASS/build0保留但不提交/推送被拒候选，outbox仍待后续。

Web publication exactDTO 窄修 attempt6：tree **000572b3ab6f1901d344fb1e246219f41636eb95**。Main 六 selector **268/268PASS/0pending**，build0、前后同 tree；原件 `evidence/web-wiring/web-complete-maintenance-attempt6/`。相对attempt5仅Panel与maintenance tests，验证 immutable初始PENDING snapshot、完整currentVerification、共用权威predicate的UI/阅读/保key消费和畸形DTO负例原key恢复。独立最后1P1窄复审已激活，不提前本地commit/push Web；原失败和REJECT保持，后续outbox/真实Runtime/浏览器与D2审计未消失。

Web 完整补缺最终窄复审 **ACCEPT_LOCAL_WEB_SCOPE，P0/P1/P2=0/0/0**。Main本地Web commit **a3066e0c63dc45c40e4b51c90c490908b8c685c1**，tree精确等于tested/reviewed **000572b3ab6f1901d344fb1e246219f41636eb95**，提交后clean；原件 attempt6/review-final.json。本轮Web已局部闭合，不是live API/浏览器/Runtime或全特性验收；未push该增量，Root gitlink/pinned Web仍保留远程bdff4786。下一唯一critical Writer串行业务outbox实际投影/重投/幂等CAS与扫描索引，基于API18d66419，不准扫描即DELIVERED或新增平行聊天状态机。后续真实共享Runtime+浏览器开发验证、完整D2审计与组件/Root远程提交仍须完成，goal继续active/NOT_COMPLETE。

## 2026-10-02 业务 outbox 进行中的只读合同观察

Main 保持单 Writer Knuth，不测试或冻结其 partial API 源码。已据当前源确认并通知同一 Writer：新 business claim/dedup CHECK 的 JOB_EVENT nullable sequence 必须显式非空，不能让 SQL UNKNOWN 放行；新投影 payload 只有 jobRef 而冻结 Web `ArchiveMaintenanceReceiptCard.vue` 只解析 `archiveMaintenance.jobId`，须保持既有 v1 输入兼容。派生 claim 表不存复制业务正文/聊天日志，真正投影与 existing event/withdrawal ack 仍须同短事务/CAS和实库验证；上述观察不是本包验收。

另外，原 D2§12.2 不是仅保留安全的未核验 jobRef：要求结构化办理事实、查看维护单、仅 PUBLISHED+读回正常的打开典籍。当前冻结卡片只有 ref 和手动 GET job 按钮，没有两个跳转/阅读动作；当前 GET job DTO 也无完整 publication/verification（不能从消息或 Agent 字段补造）。D2§12.1 的实际完成章数/总数目前也未在维护单展示，须在后续逐要求审计中补真实 server progress facts（未知总数明确未知，不虚构）。Web a3066e0 的局部 ACCEPT 继续有效，但不等价这两节全部完成。准备在 API outbox 通过后串行补最小服务端事实/聊天卡与进度，再进行真实 Runtime/浏览器开发联调，不并行改冻结 Web、不倒改 D2。

## Business outbox 补缺：源码冻结与第一轮实际验证

2026-10-02：唯一 Writer 交回 tree `a5a4726b2495a3becee8bbae00cd8f9e25c22b33`，包含真实共享聊天持久投影、源 ack/CAS、claim fencing、19表迁移及后续 readback 状态通知；默认 business-outbox 开关仍关闭。Main 已持锁运行四 selectors，platform74/native6全PASS；maintenance/archive测试均因新增 MySQL 并发测试的 `ExecutorService.submit` 重载歧义编译失败，**二者没有执行，不复用旧 XML 造绿**。原件 `evidence/native-lifecycle/business-outbox-api-attempt1/`，前后同 tree，保留编译失败及仅实际执行的两套 fresh XML。

已交回同一 Writer 仅修测试180/181行的 Callable 类型；不改变生产实现、断言或候选范围。该包未通过实库/独立复审、未提交/推送。此前 Web 局部 ACCEPT 不变；聊天办理事实、显式导航/阅读入口、实际章节进度及真正共享 Runtime/browser 开发验证仍待串行补齐，原完整 D2 范围保持。

第二轮 tree `0591c2a5635009c38046dd16ca828b5bc3f3fd3f` 编译通过；四套真实 MySQL实测platform74/native6全PASS，maintenance145/135PASS/10新FAIL，archive311/291PASS/20FAIL（11既有+9新），0skip。Main已核对 fresh XML、前后同 tree 和直接 failure delta；原件 `evidence/native-lifecycle/business-outbox-api-attempt2/`。

实际缺陷分离：bootstrap publication无 job 时新 outbox强NOTNULL插入导致三个已有下架/历史测试回归；新增projection fixture未调用既有two-step绑定所以拿到合法NO_TARGET、没有真实消息；同名application.properties的测试资源冲突；旧readback升级fixture留下新增business outbox表形成不支持partial。已将这四类交回唯一Writer，要求修真实回归/合法fixture，不弱化ACL、CHECK或接受任意partial。新增两类projection测试本轮确实运行，失败不是未选中。局部候选仍不通过、不提交/推送，D2其他缺口保持。

第三轮 tree `2ef3eff637b0514a0f0220b96b4e845be26a36aa`：四套真实 MySQL，platform74/native6全PASS；maintenance145/144PASS/1新FAIL；archive311/299PASS/12FAIL（11既有+同1新），0skip。新增Dispatcher/MySQL投影测试均实际PASS，包含真实共享聊天持久化、ack回滚重投、竞争claim、readback FAILED→PASSED后续通知；这只是组件验证，不是共享 Runtime/browser。

此前四类问题已收敛，剩下实际返回回执一致性：无jobBootstrap withdrawal持久落NO_TARGET，首次DTO却仍返回内存PENDING，同键replay返回NO_TARGET（其他字段一致），因此原`assertEquals(first,replay)`正当失败。已交同一Writer窄修真实首次返回事实，并要求零outbox断言绑定真实withdrawalId，不以operationKey作不匹配查询假绿。前后同tree、fresh XML与直接failure delta已保存 `evidence/native-lifecycle/business-outbox-api-attempt3/`；本包仍未提交/推送/独立复审。

第四轮最终候选 `fef50a52019c2ac1c6ce2e17ca7373fa65318c53`：Main全程持锁四套真实MySQL，platform74/native6/maintenance145，定向 **225/225PASS**；archive311/300PASS/11既有FAIL/0skip，Gradle exit1，直接 introduced=[] / removed=[]，前后同tree与全fresh XML。真实首次Bootstrap NO_TARGET与same-key replay已一致；零outbox断言使用真实withdrawalId。19表schema与精确18表前代Gitblob已重新绑定；新增两类projection测试的真实执行名单及XML摘要已独立核对。原件 `evidence/native-lifecycle/business-outbox-api-attempt4/`。

候选已交独立只读Reviewer，复核实际持久化/幂等ack/fencing/授权/通知收敛/迁移与锁顺序；源码冻结，无其他Writer活动。**当前只是定向组件PASS，尚未独立ACCEPT、未提交/推送该源码，不外推fullD2或Runtime/browser。** 后续API办理与章节进度facts桥及串行Web/真正Runtime开发验证任务仍NOT ACTIVATED。

第四轮独立只读复审 **REJECT_LOCAL_API_SCOPE，P0=0/P1=1/P2=1**，原件 attempt4/review.json。确认实际聊天persist+ack、fencing/回放/权限/通知/迁移局部链与225PASS证据真实；P1是新增job FK造成跨合法manager下架与dispatcher的确定publication↔job反向锁环，不能以同manager行锁作泛化串行保证；P2是旧claim索引中间available列未约束，不能有效范围限制过期lease，加CASE排序仍可能在LIMIT前全扫描。已交唯一Writer锁序与有证据的最小indexed bounded分队列扫描窄修，并要求真实跨manager latch、MySQL执行计划/深future-lease队列证明。没有提交/推送未接受源码，整体仍NOT_COMPLETE。

第五轮窄修实际验证完成：API tree **db4f974657afea99f382bd4e6c3d56d6b2ad93f6**，Main 持锁真实隔离 MySQL 四套 selectors：platform74/native6/maintenance147，定向 **227/227PASS**；archive313/302PASS/11既有FAIL/0skip，Gradle exit1。前后同 tree、全 fresh XML、相对 readback-source-api-attempt5 的 introduced=[] / removed=[]。两个新用例跨合法不同 manager 的 job-root 锁顺序与 bounded queues + 深层未来 LEASED backlog 均实际执行 PASS；原 XML 的三条 EXPLAIN 分别命中 available/lease 索引、type=range、rows=1，原件和绑定见 `evidence/native-lifecycle/business-outbox-api-attempt5/repair-case-and-explain-proof.json`。

本轮 schema 已独立绑定候选 Git blob 035c1379 / LF SHA256 782a64f1 和前代18d66419的18表 Git blob 255a2cd4 / LF SHA256 5f358f3c，未复制 Writer 摘要中前代 SHA 的笔误。独立只读窄复审已激活（此前1P1/1P2），尚未提交/推送本包，不能以227PASS代替复审或整项收口。当前待补聊天办理事实、明确维护单/阅读导航、实际章节进度及共享 Runtime/browser 验证保持不变。

第五轮独立只读窄复审 **ACCEPT_LOCAL_API_SCOPE，P0/P1/P2=0/0/0**：跨不同 manager 的 job→publication 锁顺序与真实阻塞 latch 证明、独立三队列范围索引和稳定有界归并均闭合。Main 已保存本地 API commit **24590693f31c2b2b9c602252689471f318772ab6**，tree 精确等于 tested/reviewed db4f9746，提交后 clean；原件 attempt5/review-final.json。尚未 push 该增量，Root gitlinks/pins 不变。下一串行唯一 critical Writer 补最小合法 GET job 办理事实/实际章节进度/current publication-reading facts，API冻结验证复审后再转 Web 聊天卡与导航；真实共享 Runtime/browser 与完整 D2 收口仍未完成，goal保持 active。

## API 聊天办理/真实进度 facts bridge 候选

2026-10-02：API-only 七路径候选 tree **128b1bef132b6fca5f18d84c4a20aa701ba1e495**（base24590693）为原 GET job 添加向后兼容的 handling、实际 persisted chapter progress、不可变 receipt 与 current verification 分离、current readerTarget，以及 private/no-store。Main 持锁四套真实 MySQL attempt1：platform74/native6PASS；maintenance152/150PASS/2新FAIL；archive318/305PASS/13FAIL（11既有+同2新），0skip、前后同tree、全fresh XML。五个新增facts selectors实际PASS，包括三个真实MySQL/撤权latch；但整体候选仍失败。

两个新引入失败位于旧confirmedIntent/三入口重放ServiceImplTest，新的getJob锁定读取在findJob(...,true)得到mock null而404；不能把五项新增PASS替代回归。已交回唯一Knuth最小修正确durable mock两种lock读取，保持生产锁/ACL、原单一intent/job/replay断言及全部测试，不skip。原件 `evidence/native-lifecycle/chat-facts-api-attempt1/`。本包尚未review/commit/push，Web/Client仍冻结，后续完整scope不变。

API facts bridge 的最小合法 mock 修复后 attempt2 tree **5c8b8a28550d437855e5155f381b5e4d6346d0cb**：platform74/native6/maintenance152，定向 **232/232PASS**；archive318/307PASS/11既有FAIL/0skip，Gradleexit1。相对 accepted outbox tree db4f9746 直接 introduced=[]/removed=[]，前后同tree、全fresh XML。五个新facts与两个原confirmedIntent/三入口重放selector均实际PASS，原件 `evidence/native-lifecycle/chat-facts-api-attempt2/actual-facts-selector-proof.json`。相对失败attempt1只有一个测试文件25新增/2删除，支持同一durable job的锁定/非锁定读取并捕获真实insertDraft，生产锁/ACL/事实投影未改。独立只读完整API facts复审已激活，尚未本包commit/push；Web/Client冻结、全特性与真实Runtime/browser仍未收口。

API facts attempt2 独立只读 **REJECT_LOCAL_API_SCOPE，P0=0/P1=1/P2=1**：任职撤销只fence run/清slot，job保留历史assignee/permission/waitReason；直接投影会把已撤销指派当作current并给出错误CLIENT_UPDATE_REQUIRED。另强ETag只含jobrevision，而新增readback/readerTarget随核验改变却不改jobrevision，representation validator失真。原件 attempt2/review.json。已交同一Knuth最小区分历史/当前任职事实并保持slot/appointment先于job锁序、真实appointment-revoke/read竞态，以及表示级ETag与原mutation revision/If-Match分离并保旧写合同；不以232PASS抵消审查项。本包不commit/push，Web/Client保持冻结，原进度/sourcecoverage/reader权限局部认可不变。

API facts P1/P2 源码窄修的 attempt3 tree **c54b6a2852845d4bb2a4bad9b96b96c1d7f4f4e8**：Main 持锁四套真实MySQL，platform74/native6/maintenance153，定向 **233/233PASS**；archive319/308PASS/11既有FAIL/0skip，Gradleexit1，introduced=[]/removed=[]、前后同tree、全fresh XML。当前任职从锁定slot/appointment事实投影，历史appointmentId/revision/assignee/permission单列assignmentSnapshot；撤任后current assignee/permission为null，REVOKED/REASSIGNMENT_REQUIRED，不误用历史snapshot。合法同actor-owned scope的两连接appointment-revoke/GET race实际PASS（不制造跨owner授权来强求不同grant）。GET完整JSON representation ETag为r-sha256，bodyrevision保留vN写precondition；同jobrevision核验改变与原写合同测试实际运行。原件 `evidence/native-lifecycle/chat-facts-api-attempt3/`，9个相关selectors实际PASS。独立只读P1/P2窄复审已激活，暂不本包commit/push，Web/Client仍冻结；完整scope继续。

API facts attempt3 独立复审确认原appointment-revoke P1和representation-ETag P2闭合，但补充裁定 **REJECT_LOCAL_API_SCOPE，P0=0/P1=1/P2=0**：slot/appointment/job snapshot仍ACTIVE时，合法共享identity解绑/owner-binding变化只暂停identity/binding并清runtime，未改archive任职行；新GET会错误显示current ACTIVE/assignee/profile，虽然native写路径实际正确fence。这是原currentfacts同类遗漏，不是写ACL绕过。原件 attempt3/review.json，代码事实指向AgentHostedBindingTransaction282-307和currentJobAssignment3544-3591。已交同一Knuth复用既有persistedidentity-root锁（identity先于manager/slot/job）及currentactive binding/owner核验，失效投影BINDING_CHANGED/nullcurrent字段/REASSIGNMENT_REQUIRED、保留历史和独立Reader资格，并补真实共享identity/MySQL并发证据，不造新身份平台/在线或安装门槛。本包不commit/push、Web仍冻结，233PASS保留但不等于接口收口。

API facts shared identity 极窄修复 attempt4（2026-10-02）：tree **fc23281749387d8b009ee243072f5d19a2fe93a8**，Main全程持锁四套真实MySQL，platform76/native6全PASS；maintenance155/153PASS/2新增FAIL；archive321/308PASS/13FAIL（11既有+同2新），0skip、Gradleexit1。前后同tree、全fresh XML，14个相关selector中12PASS/2FAIL。新增共享identity port边界与基础设施异常测试实际PASS；真实暂停并发测试因JDBC-backed fixture的Mockito泛型varargs错误Long→Object[]失败，旧replacement/reassign用例因新fixture漏配agent-b/binding8返回null失败。原件及逐失败比较保存 `evidence/native-lifecycle/chat-facts-api-attempt4/`，未弱化生产锁/ACL、未skip、未提交/推送源码。已交同一Knuth只修合法fixture与类型明确的JDBC调用；源码通过前Web保持冻结，不以12项PASS抵消两项新增失败。

第五轮仅修一个测试fixture文件后的候选 **fec2d8448ce9b33c151f8b88e5b68547ad1fb654**：Main持锁真实隔离MySQL四套platform76/native6/maintenance155，定向 **237/237PASS**；archive321/310PASS/11既有FAIL/0skip、Gradleexit1，前后同tree、全fresh XML、相对已接受business-outbox-api-attempt5/db4f的introduced=[]/removed=[]。14个相关selector实际全部PASS，包括replacement/reassign旧回归、真实生产IdentityService+Spring事务代理/JDBC-backed adapter的binding suspension/GET线性化和历史读取不rollback-only；DAO适配器及latch仍属于明确的组件fixture，不宣称完整Runtime/生产链。原件 `evidence/native-lifecycle/chat-facts-api-attempt5/`；独立只读复审已激活，目前无源码Writer/Gradle活动，尚未源码提交/推送、未激活Web或真实Runtime/browser包。

第五轮独立只读复审 **ACCEPT_LOCAL_API_SCOPE，P0/P1/P2=0**：共享binding→scoped identity→manager/slot/job锁序、正常历史读不rollback-only、基础设施异常传播及current/historical/Reader分离闭合；原appointment revoke与r-sha表示ETag/vN写合同无回归。Main本地API commit **2e4888ff35a2d2137a6679fdd3f0439f73207420**，tree精确等于tested/reviewed **fec2d8448ce9b33c151f8b88e5b68547ad1fb654**，提交后clean；原件 attempt5/review-final.json。未push增量、Root pins/gitlinks不变。已激活唯一Curie Web Writer按冻结DTO补聊天办理卡/章节进度与明确维护单和Reader导航；真实共享Runtime/browser及完整D2逐要求收口仍未完成，goal保持active。
