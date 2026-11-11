# 最终验证第二失败：根因矩阵与定向整改

最终源码7d043c311a97e412a34eb10883712d57c8113bdc/tree10d1d95d413ce96c759efedb723356000aa0b841保持SOURCE ACCEPT；以下实测失败并未通过。

| 运行 | 真实结果 | 归因 |
|---|---|---|
| 首次最终unit（离线） | native1；common Redis 2PASS，其余70未启动，MySQL0 | 本地缺jaxen1.1.6、jaxb-api2.2.12、LatencyUtils2.0.3，强制offline阻断runtime依赖解析 |
| 有界联网续跑 | native1；88任务中5执行、83UP-TO-DATE；结合原2项共覆盖72，70PASS/2FAIL/0SKIP，MySQL0 | WxMpControllerDailyVoteTest的两个提前拒绝用例在Mockito.afterEach因setUp未使用stub失败；未发现新的业务断言失败 |

失败方法：`originalAccountMismatchFailsBeforeIdentityOrDailyVoteSideEffects`、`invalidSignatureFailsBeforeXmlParsingOrIdentityLookup`。错误为UnnecessaryStubbingException，指向该测试setUp的69/70/72行。

- 第二失败已进入blocked_root_cause，不能原样重跑；Verifier先保存全部10份原始XML、SHA和混合复用证明。
- Main仅批准原Writer修改该一个测试文件：将只适用于已验证账户/身份的stub移入真正需要的用例或显式helper，不关闭Mockito全局strictness，不删除业务断言，不改生产代码、依赖版本或迁移。
- 新候选必须保持生产blob不变、独立小差额复审。保持全部72项覆盖，复用未变模块已通过证据和编译输出；不使用rerun-tasks，不重复冷编译。
- 最终允许同一WX测试任务重新执行其33项并复用其他39项，或用等价的精确selector证明其他63项+新controller9；报告须区分实际本次执行与跨运行复用，不冒称全新72次执行。
- Unit总覆盖通过后才继续原获准的隔离MySQL迁移/SQLprobe+3个真实Spring事务用例；仍未授权生产变更。
