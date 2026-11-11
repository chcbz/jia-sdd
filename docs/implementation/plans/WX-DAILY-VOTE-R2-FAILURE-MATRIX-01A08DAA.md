# R2 连续第二次源码评审失败：停止与有界整改

Reviewer Godel 对953eaab456a46aeff1f969e5080f59c4c8c3c75d/treefbe836a47926b452a460eafe50b14611e8493b87作第二次REJECT。

| P1 | 根因 | 后果 |
|---|---|---|
| 晚提交alias | selectMessage未命中后，M2→Q1 alias提交；当前M2/Q2临时receipt与持久alias不一致，claimAndValidateMessage抛错 | 事务安全回滚，但当前回调仍不给用户旧结果 |
| 合法双receipt | M1/Q1与M2/Q2都是合法已完成答题，旧M1重试读取Q2，lockConflicts两行却被当成身份损坏 | size!=1先抛错，未优先返回M1结果；原mock双同题fixture不符合真实唯一约束 |

已有R1稳定canonical重放和按result题号清理已修好；不回退。原SOURCE第一失败、构建配置失败以及未执行测试事实全部保留。

## Main明确批准的唯一有界整改

- 不引入新锁表、不扩大鉴权或计分重构。沿Reviewer认可方案：transactional answer通过Spring代理抛错、完成rollback后，controller最多一次新的findReplay。
- 仅返回appid/message/user/fingerprint严格校验的COMPLETED持久结果；查不到或二次查询出错时抛回原始异常对象，可附suppressed，不吞异常、不循环重试。
- replay仅清理返回结果题号，不发红包；失败时不误删新题。
- 原Writer在已独占R2 worktree增加最小controller修复、mock回归及真正Spring事务+独占MySQL并发证据fixture。须证明两种竞争均在本次回调返回Q1，临时Q2写入已rollback，Q2指针保留，积分/投票/统计不变，身份/正文篡改仍失败。
- 数据库执行仍归Verifier、经同一个orchestrator串行窗口；Writer只写测试不运行。修改测试harness的缺陷先静态校验，不能将没有通过证据的64用例省略。
- 这是矩阵授权的定向整改，不是对第二次REJECT的盲目重试；最终clean候选仍需原Reviewer独立接受及实际验证。没有生产操作准入。
