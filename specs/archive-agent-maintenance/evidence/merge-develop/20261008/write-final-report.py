import pathlib,json,re
r=pathlib.Path(r'C:\Users\Think\.codex\worktrees\archive-agent-maintenance\cyf-web-kit');f=r/'specs/archive-agent-maintenance';e=f/'evidence/merge-develop/20261008';d=json.loads((e/'final-validation-summary.json').read_text(encoding='utf-8'))
rows='\n'.join('| {task} | {tests} | {pass} | {failures} | {skipped} |'.format(**x) for x in d['api']['suites'])
text=f'''# develop 合入与功能验证：2026-10-08

## 结论

**四仓 develop 已合入现有特性分支并普通推送；功能验证未全部通过，不能标为完整特性完成或可发布。**

- Root分支：`codex/archive-agent-maintenance`，受测源码根提交 `{d['tested_server_root']}`。最终证据提交不自嵌SHA，另以远端回执验证。
- API：`{d['current_remote_delivery_before_final_evidence_commit']['api']['commit']}`。
- Web：`{d['current_remote_delivery_before_final_evidence_commit']['web']['commit']}`。
- Client：`{d['current_remote_delivery_before_final_evidence_commit']['client']['commit']}`。
- 原 `D:/workspace/chaoyoufan/project/cyf-web-kit` 未由本任务改动；源码在隔离worktree实施。未合回develop/master、未force-push。

## 当前真实结果

后端Linux六套均强制执行、fresh XML、0skip，同树before/after；独占MySQL 8.0.46关闭及Gradle共享锁释放有回执。**Gradle exit1**。

| suite | tests | PASS | FAIL | skip |
| --- | ---: | ---: | ---: | ---: |
{rows}

MVP的5项失败同样出现在archiveRegression；后者另外11项是已观察过的回归失败集合。不能把未知实库失败自动归为合并新增：前次Windows跳过该MySQL lane，原完整实库基线被schema初始化阻断。这里只报告当前失败，不伪造可运行旧基线。

Web：本地19 selectors **480/480PASS**；Linux full **3240/3199PASS/39FAIL/2pending**，build exit0。39项失败与同环境冻结develop四个受影响文件的失败集合完全相同，introduced=[]；依赖缺失的固定Chromium执行路径阻断相关校验，不当作PASS或真实浏览器E2E。

Client：Linux full **962/952PASS/0FAIL/10skip**，exit0；执行环境umask022。旧umask077掩蔽了目录权限负例所需的755权限；另有单独022回执证明生产ledger未放宽。两个误扫描技能内部import字符串的合并组合失败已修复；新增7个scanner用例及实际42-module闭包检查通过。

## 已修复并复审

- 不完整SSE replay不提前推进游标，16/16专项PASS。
- 当前DDL SHA CHECK与MySQL canonical REGEXP_LIKE一致，严格比较、wrong-pattern及额外列拒绝保留；原四历史fixture及批准ZIP字节未改。
- 实库测试夹具补清理、合法command/message/digest、共享存储、合法关联；加入18d66419/eb31260f精确Git blob资源。MVP失败从37降至5，仍非全绿。
- Web真实receipt predicate挂载兼容；Client真实import扫描，不通过修改生产字符串逃避依赖证明。首次复审P2（ASI/block漏依赖）REJECT及真实复现保留，修闭后限定ACCEPT。
- 独立review为独立Sol实例，**不是跨模型审查**；所有ACCEPT均限源码包/测试harness，不外推成真实业务验收。lexer不是完整JS parser或安全沙箱。

## 待修/待验收

当前5个实库失败：
1. `realJdbcKeysetsPageAppointmentsJobsManagedWorksAndPublishedReaderShelf`：edition夹具违反`chk_archive_edition_counts`。
2. `repeatableReadRealPublishWinsBeforeWithdrawalAndStaleWorkCasLeavesEditionPublished`：发布暂存时active edition变化。
3. `draftOnlyValidationCompletesAndReadOnlyRevocationFencesWithoutPublication`：execution proof不再current。
4. `checkpointObjectFailureRollbackAndLateAclLeaveNoReferencedChapter`：预期`ARCHIVE_ACTION_FORBIDDEN`，实际`ARCHIVE_FORBIDDEN`。
5. `dependencyRepairRequiresFailedBaselineAndSuccessfulPrivateSourceReadback`：private source readback未证明blocked failure恢复。

上述仍需区分夹具构造与真实业务问题，不能仅放宽断言造绿。另有11项已知archive回归、39项固定浏览器环境校验失败待处理。真实Runtime/browser、生产部署/迁移/任职/上架/付费调用均未执行；84业务用例全部not_run/evidence=null，whole_feature_accepted=false。

## 原件与一致性

`evidence/merge-develop/20261008/final-validation-summary.json`记录准确组件提交/tree、远端、pins/gitlinks、fresh XML digest、保护资源、失败与未执行边界；source_consistency_checks_passed不是功能验收PASS。原attempt1–4、Node develop baseline/final、失败和REJECT全部保留；原始字节stage审核另存。最终Root证据提交仅更新文档/原件，不改受测组件源码。
'''
(f/'merge-validation-20261008.md').write_text(text,encoding='utf-8',newline='\n')
with (f/'delivery.md').open('a',encoding='utf-8',newline='\n') as out:
 out.write('\n\n### 最终验证结果（2026-10-08，覆盖此前待复测状态）\n\n四仓源码合入并普通push完成。服务端attempt4全部六套fresh XML/0skip：platform141PASS、security10PASS、MVP245/240PASS/5FAIL、archive398/382PASS/16FAIL、typed91PASS、replay16PASS，Gradle exit1。5个维护实库失败同时在archive中出现，另11项已知回归保留；不能归为纯环境或任意称合并引入。Client full962/952PASS/0FAIL/10skip；Web本地480PASS，Linux full3240/3199PASS/39同develop失败/2pending，build0。Source/pin/remote/raw-byte一致性通过不是功能全绿。\n\n当前整体功能验证**未通过/未接受**，5项实库问题、已知回归和浏览器环境校验待处理；真实Runtime/browser与84业务验收未执行，生产操作为false。精确当前结果及待修方法见[merge-validation-20261008.md](merge-validation-20261008.md)及evidence/merge-develop/20261008/final-validation-summary.json。此前原失败/REJECT/历史记录不改写。\n')
p=f/'integration.yaml';s=p.read_text(encoding='utf-8');s=re.sub(r'^status: integration-ready$','status: implementing',s,count=1,flags=re.M)
s=s.replace('develop_merged_postmerge_repairs_pushed_server_retest_pending','develop_merged_pushed_server_validation_completed_with_remaining_failures')
s=s.replace('merged_source_pushed_postmerge_mysql_and_test_harness_repairs_pushed_retest_pending','merged_and_pushed_verified_with_unresolved_live_mysql_and_environment_failures')
s=s.replace('server_validation: attempt3_failed_repaired_source_pending_attempt4','server_validation: attempt4_completed_fresh_0skip_failed_5_maintenance_plus_11_known_archive')
s=s.replace('status: source_reviewed_components_pushed_server_retest_pending','status: source_reviewed_components_pushed_server_retest_completed_not_all_passed')
s+='''
current_merge_validation_20261008:
  status: completed_not_all_passed_not_accepted
  report: merge-validation-20261008.md
  evidence: evidence/merge-develop/20261008/final-validation-summary.json
  api_gradle_exit: 1
  api_mysql_skipped: 0
  maintenance_tests: 245
  maintenance_pass: 240
  maintenance_fail: 5
  archive_tests: 398
  archive_pass: 382
  archive_fail: 16
  known_archive_failure_methods: 11
  unknown_live_mysql_failure_methods: 5
  unknown_mysql_merge_regression_classification: not_proven_premerge_lane_not_runnable
  web_local_pass: 480
  web_linux_tests: 3240
  web_linux_pass: 3199
  web_linux_fail: 39
  web_linux_pending: 2
  web_failure_delta_vs_frozen_develop_affected_files: 0
  web_build_exit: 0
  client_tests: 962
  client_pass: 952
  client_fail: 0
  client_skip: 10
  source_pin_remote_raw_byte_consistency: passed_not_functional_acceptance
  real_runtime_browser: not_run
  business_acceptance: not_run_84_cases
  production_changes: false
  whole_feature_accepted: false
'''
p.write_text(s,encoding='utf-8',newline='\n');print('Report and current manifest written; historical SHAs unchanged.')