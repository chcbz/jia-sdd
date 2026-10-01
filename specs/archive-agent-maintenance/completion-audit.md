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
