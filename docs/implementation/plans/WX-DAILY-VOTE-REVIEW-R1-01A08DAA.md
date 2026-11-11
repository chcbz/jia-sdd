# R1 独立评审：REJECT（2026-09-11）

- Reviewer Godel；候选7a846a3e4feeff895075c2d3456e87295c6b83cb/tree65e8cdd24fd19029e52864dd7a35224775a4b5f1。
- P1：旧消息M1首次replay查询发生在原事务提交前，随后读取到用户新领Q2；answer以M1/Q2 claim得到M1/Q1 receipt，却先按Q2校验而报错，不能重放Q1结果。
- 归因：事务内重放身份检查绑定了不稳定的Redis题目指针，而非已持久消息对应题号。仅增加一次controller查询不能消除竞态。
- 最小整改：answer优先识别同消息持久receipt，用其题号验证用户/消息fingerprint，返回已存结果，不追加投票/积分/计数。controller cleanup必须使用返回结果的questionId，而不能继续使用Redis读到的新题号。
- 测试：旧M1/Q1加现Q2指针仍返回Q1、零新业务副作用、Q2保留；还须覆盖不同消息alias重放、双冲突及payload篡改不被放过。
- 基础候选Gradle已获得锁并在运行，不改其worktree、不终止；原Writer在新隔离worktree作限定整改，完成后做差额复审与定向验证。旧树结果不冒充最终树结果。
- 原生产compatibility、best-effort红包等剩余事项维持前记录。
