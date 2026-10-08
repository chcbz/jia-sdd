# 桥接合同证据（不是功能通过）

- `branch-readback-before-contract.json`：合同提交前四仓remote feature HEAD与本地一致，remote fast为祖先；报告日期与host采集时钟分开，不是发布日期。
- `../../fixtures/controlled-image-bridge-v1.json`：五组29项**预期**，全部NOT_RUN；不等于原34项产品用例。
- 静态检查：`python3 specs/juyiting-multimedia-deliberation/fixtures/validate-controlled-image-bridge-fixture.py`，检查字段、fixture SHA、现有assignment/input hash域、identity、v1/v2容量和无真实费用授权。
- Node只读调用当前Web core的`providerConsentIssueBody`/`providerConsentReceipt`，确认fixture issue正文与BOUND回执兼容；未执行桥接POST/START、Provider、浏览器、迁移或发布。
- 后端core `acab3411` 未提升研发pin；normal graph javac环境失败保留，不写业务测试通过。后续真实来源以Owner stdout/XML/隔离事务回归为准。
