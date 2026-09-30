# 受控图像桥：实际验证进展与未关闭缺口

文档日期：2026-09-30。只读状态补充，不改冻结 wire、详设或运行台账。原始日志/快照按采集主机时钟保存（部分为 2026-10-01），不作为当前日期或发布日期。

## 分支与详设交付

本次独立 `ls-remote` + `merge-base --is-ancestor` 重新确认 SDD/API/Web/Client 四仓 `codex/juyiting-multimedia-deliberation` 与当前远端 feature HEAD 一致，且都包含当前 fast HEAD；无需重复建分支/合并。SDD及Client没有develop独有提交，API/Web分别仍有4个；发布前须收敛，不能将fast合入当作develop融合。

当前远端源码核验点：SDD `493b1187`、API `083f9846`、Web `1ceb48d`、Client `5548052`。SDD为本文提交前核验点；原始 SHA/tree/readback 见[证据快照](integration-evidence-20260928/controlled-bridge-verification-progress/latest-branch-and-design-readback.json)。研发 pins 不因候选编译或文档提交而提前提升。

长期方案继续是[统一议事与受控执行](long-term-fusion-plan-20260928.md)：fast 为 CHAT 轻量策略，按需 INSPECT/EXECUTE，不预加载全部资料/工具。主合同为[融合详设v2](fusion-detailed-design-v2.md)，[媒体/存储详设](design.md)和[实施计划](fusion-implementation-plan-v2.md)继续有效。

## API：已越过编译内存问题，但真实测试失败

- 候选 `d3baf9b0` / tree `bdf04ddb` **未合入API feature**。
- v9：正常图中 javac worker成功，Gradle daemon增量classpath snapshot耗尽heap，0测试/0XML。历史失败不改PASS。
- v10：仅两个bounded fixture JavaCompile设 `options.incremental=false`，所有11个测试源、正常依赖图、AP、production/default-full-test配置与heap不变；实际完整javac已通过并进入agent测试。
- 实际38项：30通过、5失败、3跳过，5份JUnit XML；45 actionable tasks（17 executed/28 up-to-date）。4个Controller失败缺JsonPath运行类，1个真实CGLIB事务夹具缺H2 JDBC driver。chat selector尚未执行。MySQL3为真实跳过，继续NOT_RUN，不当通过。
- 下一步由原API Owner提交最小scoped runtime依赖修复；固定新commit/tree/matrix/input后串行重测。禁止原输入盲重跑、禁AP/排测试或借baseline class覆盖。普通通过后再执行当前线程自有隔离MySQL3。

原stdout artifact未生成，不伪造stdout；保留实际daemon日志及XML。完整摘要/压缩原始日志摘要见[manifest](integration-evidence-20260928/controlled-bridge-verification-progress/manifest.json)。

## Web：组件成功不等于原会话已采用

候选 `cb65ebfa` / tree `4ed8dadf` **未提升Web feature**。Owner6项动态和69项已有回归不覆盖全部页面组合。Main从该commit导出12个精确Git blob，真实Vue + 两个composable、假HTTP实际重现：

1. issue与bridge POST成功，但页面委托旧core `checkOriginal` 被费用意图拒绝：自动采用计数0、投影GET0；不能以BOUND或 `onBound++` 代替进入原议事。
2. 显式恢复GET延迟404，在context失效后仍发出bridge POST1；应为0。
3. issuer响应丢失且尚无wrapper时，两个恢复动作HTTP0；须接原issuerkey只读核对及显式精确继续，不能改新key或转legacy。

另须补新offer/需求修订/modal关闭的同意checkbox重置、实际页面采用与恢复动态证据。原Web Owner在原写集修复；Main不修改Owner源文件。初次在途工作树探针不属于immutable证据，仅精确Git blob结果列入本补充。[重现结果](integration-evidence-20260928/controlled-bridge-verification-progress/findings-cb65-immutable.json)和[源码manifest](integration-evidence-20260928/controlled-bridge-verification-progress/immutable-cb65-source-manifest.json)可复核。

## 交付边界

分支创建、fast代码合入、长期方案及详设已交付；上述是实际验证与原Owner修复，不是产品完成。Client v2已有源码证据，API/Web桥仍未完整联通。澄清/上一稿EDIT、完整多媒体、正式验收/完成、develop语音收敛、双接应浏览器34项及精确版本发布仍要完成。

本次未调用真实Provider/付费、未选真实账户、未部署/启用或迁移生产数据库。34产品用例仍NOT_RUN，29共同桥fixture也不据这些局部测试改PASS。唯一运行台账仍是 `docs/implementation/TASKS.yaml#runtime_ledger_json`。
