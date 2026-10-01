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