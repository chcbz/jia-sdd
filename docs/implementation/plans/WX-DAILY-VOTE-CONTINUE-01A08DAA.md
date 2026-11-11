# 微信答题优化续接入口（2026-09-11）

唯一执行台账：`/home/isp/wsps/cyf/docs/implementation/TASKS.yaml#runtime_ledger_json`。本文件是交接证据，不是第二台账。

## 已完成

- 诊断：9月11日07:31的三次回调分别约85/80/75秒，Nginx约4–5秒499；重叠GC暂停约41.75秒。历史答题三条已证实，不能声称同用户净增三倍积分。
- CPU旧进程4109240已由其所属任务清理；本任务没有操作该进程。实际答题延迟改善尚无新真实消息证据。
- 优化源码已提交并独立SOURCE ACCEPT：`7d043c311a97e412a34eb10883712d57c8113bdc` / tree `10d1d95d413ce96c759efedb723356000aa0b841`。
- 工作区：`/home/isp/wsps/cyf/.worktrees/wx-daily-vote-opt-r2-01a08daa`，branch `codex/wx-daily-vote-opt-r2-01a08daa`，最后确认clean。
- 原用户旧`/home/isp/wsps/cyf/api`未修改；候选尚未push/develop合并，没有生产DDL/部署。
- 持久回执/别名、幂等判题与原子积分/计数、索引迁移、旧题缓存保护、事务回滚后一次持久重放和脱敏分段耗时已实现。详情见`WX-DAILY-VOTE-SOURCE-ACCEPT-01A08DAA.md`。

## 实测事实与唯一小修

- 首次最终unit离线运行：native1，2PASS，70因缺3个runtime依赖未启动。
- 获准联网续跑：native1，5任务执行/83UP-TO-DATE；结合原2项，72覆盖/70PASS/2FAIL/0SKIP。MySQL尚未启动。
- 仅失败`WxMpControllerDailyVoteTest`中的`originalAccountMismatchFailsBeforeIdentityOrDailyVoteSideEffects`和`invalidSignatureFailsBeforeXmlParsingOrIdentityLookup`：Mockito.afterEach报UnnecessaryStubbingException，指向setUp69/70/72行共享stub。
- 已有明确一文件整改授权：只改`wx/jia-wx-service/src/test/java/cn/jia/wx/api/WxMpControllerDailyVoteTest.java`，将账户/身份stub移到需要它的用例/helper。保持strict Mockito，不删断言、不改生产/依赖/迁移。尚未实施，因为Owner路由失效。
- 归因/授权范围：`WX-DAILY-VOTE-VERIFY-SECOND-FAILURE-01A08DAA.md`。

## 保存的证据

- 完整失败证据根：`/var/tmp/cyf-wx-final-verify-01a08daa-20260911-retry-network/unit/`。
- `failure-raw-junit/`：10份原始XML；清单`failure-raw-junit-sha256.txt` SHA256=`b6a1c129616151a045cf22fbe21943754474b3dad325fa7745f6f0945793da87`。
- `composite-common2-reuse-proof.json`：common2的前后XML字节一致/UP-TO-DATE，原XML SHA256=`ea87e02c936689a4a97d023e2ea5700676fc643427b2d7ae2abbd4bdb0a3de49`。
- `passed-63-test-blob-manifest.tsv`与`candidate-task-delta-blob-manifest.tsv`用于只修controller测试时的未变源码/测试复用证明。
- `terminal-custody-sha256.txt` SHA256=`d9db8a6c4f8509631697595f0dc6d21689afd63e65164a4326e9256d9605807d`。
- 构建/隔离脚本在`/var/tmp/cyf-wx-verify-01a08daa-20260911-evening/`。最后已执行的是联网续跑版本；新候选必须重新绑定SHA/tree及脚本pins，不原样执行旧候选常量。

## 工具阻断与恢复后的下一步

- 原Writer、Reviewer、Verifier目前均返回agent-not-found，替补spawn返回thread limit。详见`WX-DAILY-VOTE-OWNER-ROUTING-BLOCK-01A08DAA.md`；不继续盲试、不操作未知槽位或其他任务。
- 工具恢复后，先按矩阵authorize-remediation并认领一个精确、可达的测试文件Owner，再做上述一文件修正和独立微差额评审。
- 验证保留已通过证据及编译输出；不得再加`--rerun-tasks`或冷编译。可重新执行WX模块33项并复用其他39项，或精确证明63旧PASS+controller9新PASS；总覆盖仍须72/0失败/0跳过。
- 然后在同一根orchestrator串行资源窗口运行独占MySQL SQLprobe和`cn.jia.wx.api.WxDailyVoteCallbackMySqlTransactionTest`的3个实际事务用例。所有Gradle都经根`ops/orchestration/cyf_orchestrator.py`；不直接运行gradle --version。
- 真实MySQL环境变量：`WX_DAILY_VOTE_MYSQL_URL/USER/PASSWORD`（PASSWORD可空但必须显式set）、`WX_DAILY_VOTE_MYSQL_ISOLATED_FIXTURE=true`、`WX_DAILY_VOTE_MYSQL_DATABASE_PREFIX`、`WX_DAILY_VOTE_MYSQL_EXPECTED_PORT/DATADIR`。仅新隔离MySQL8.0.21、非3306/33060，禁止生产库。
- 源码接受≠实测完成≠上线。最终过测后fresh fetch remote（上次origin/develop为4b94cc25，只有ops差额），保持字节精确合并；生产需要独立迁移/备份/制品/runtime Owner/安全发布包。旧deploy脚本仍NO-GO，不用真实用户回调重放做smoke。
