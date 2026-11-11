# R3 评审：生产修复无新阻断，测试夹具P2需修正

- Godel独立审查522e14b7957ba7cee53fd72636f0d768ee5c5dd6/treee0fce9271d20632d373cd3caf343f8590a3f46f0：P0=0/P1=0/P2=1，整体尚不接受。
- 生产controller的rollback后单次新replay已关闭R2两项P1；原异常保留、result题号清理、重放不发红包均获源码确认。未因此宣称实测或已上线。
- P2在WxDailyVoteCallbackMySqlTransactionTest:507-515：用INSERT ... ON DUPLICATE KEY UPDATE id=id的返回行数==1判断新插入。JDBC found-rows模式会令重复no-op也返回1，导致合法双receipt用例出现假失败。
- 最小整改仅限该测试文件：在同一个实际事务连接上查精确appid/message/Q2/processor token的真实行状态，判断本事务是否插入；不再依赖affected-row连接模式，不放宽断言、不改生产代码、不引入新运行依赖。
- 原Writer可直接修正并提交这一个测试差额；Reviewer只复核字节差额及观察连接确与事务绑定。最终unit与MySQL计数、fixture hash随新tree重新冻结；至今没有执行通过的业务用例。
