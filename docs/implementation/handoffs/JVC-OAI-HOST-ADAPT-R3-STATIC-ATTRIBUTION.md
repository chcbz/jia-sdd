# HOST R3 static harness attribution — 2026-09-05

Retrospective original Writer report for clean be41be7f/tree67ab694b; evidence identifiers below are that Writer's own tool output chunks, not independently replayed logs. Main has not rerun checks.

1. chunk2d212c: JSON_PINS_DIGEST passed, then build admission checker ValueError substring not found. Cause: checker encoded newline/backslash incorrectly. Corrected independent complete check BUILD_ADMISSION_STATIC passed in b29428.
2. Subsequently chunk0bf0be: CURL_STATIC_CONTRACT passed, transaction checker incorrectly expected a loop variable instead of two explicit deploy STARTED_HEALTHY/COMMITTED assertions. Corrected TRANSACTION_MATRIX_STATIC and R3_SCOPE passed in4890a1.
3. Final combined static checks passed in f770e1/a2d212 per Writer. Runtime selectors never run.

These were two distinct checker defects separated by complete successful corrected check, not two consecutive product/selector failures. Writer attributed immediately in its messages but made no controller entry. Main records this consolidated historical tooling attribution through controller without relabeling it as runtime/source test failure or recreating build evidence. No replay or source edit authorized; clean candidate remains under independent source/safety review.
