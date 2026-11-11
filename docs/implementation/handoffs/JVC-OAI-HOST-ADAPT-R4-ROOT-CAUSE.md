# HOST R4 narrow recovery-boundary correction — 2026-09-05

Independent R3 REJECT0/1/0 on be41be7f75499b1b176fef887aa72eb33926beac/tree67ab694be80c03730d17aef5fbab4ca644893356, reviewer01a07199. Controller stopped at threshold before this new authorization. R3 Python/curl/proxy/CA/sharedcommon/fixture safety positives remain valid; do not redo them.

Sole finding: helper api-host-transaction.sh448–482 publishes STOP_ATTEMPTED via replace474, then may fail475–479. Deploy88–90, rollback109–111, activation106–107 assign PHASE only after successful record call. EXIT handlers therefore still choose PREPARED and try ABORTED_BEFORE_STOP, forbidden from visible STOP_ATTEMPTED by helper459–467, suppress that error, then finalize0444 a nonterminal record485–505. Actual canonical stop has not run.

Bounded original Writer correction: coordinate shell phase and record publication/recovery at this boundary so failure always leaves truthful terminal result or explicitly recoverable/manual state, never an immutable nonterminal falsely representing completed recovery. Cover all three independent handlers and before-replace plus after-replace/fsync windows; explicitly assert actual stop calls, selected bytes/config and terminal record. Avoid gratuitous transaction redesign. Existing R3 positive guarantees and isolated realcurl fixture remain unchanged.

Owned edits: original HOST worktree, narrowly deploy-api.sh/rollback-api.sh/activate-api-voice.sh, shared api-host-transaction.sh only if necessary, and test-api-host-adaptation.sh. common/canonical must remain unchanged unless a concrete finding requires otherwise; no Web six paths. Direct apply_patch; absolute MAIN docs/controller paths. Static-only clean R4 candidate, fresh delta review, then one all selector at reviewer-approved clean env. Do not run old be41 selector, builds, production, credentials or network.

R3 SAFETY_ADMISSION=PASS is side-effect scope only, not source acceptance; reviewer must bind updated exact tree before verifier run. Preserve all prior failures and artifact/test evidence.
