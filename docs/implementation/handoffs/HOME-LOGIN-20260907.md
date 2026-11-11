# HOME-LOGIN-20260907 delivery evidence

User request: visiting `/` with an existing local login should enter `/juyiting` without another button click; guests keep the public landing page.

- Source worktree: `/home/isp/wsps/cyf/.worktrees/home-login-20260907`.
- Parent: `d30dd6e76be8ab2b3ab91beb0a185148ca6ad327`.
- Candidate: `9266d58a0db2d5f59154c515449704633c59c4fc`; tree `ff179ae44fc422ba6c2aabfb91bdfe91dc504d8a`.
- Scope: `web/src/router/index.js`, `web/src/router/homeLoginRedirect.js`, `web/tests/home-login-redirect.test.js` only. Existing expiration-aware util read; no OAuth launch, auth/backend change, or redirect of demo/callback. Root guard replaces history and preserves query/hash.
- Owner: balanced_worker `01a07992-a30a-7041-b546-3b2e8fe12403`; independent reviewer `01a0799a-6bd3-70b1-9ec3-870f0fd77a08`.
- Owner targeted test: 4 passing. Independent verification receipts to follow.
- Verification Mini startup returned provider502 unknown model before execution; attributed provider availability, routed once to inherited-model verification-only Agent `01a0799b-cee1-7ee0-ab42-49bfb5cc4298`, not retried.
- Task evidence: `/var/tmp/cyf-home-login-20260907`. Main dirty web status/diff captured for preservation.
- Default deployment script hardcodes dirty main checkout plus pull/install. Task-local adapter retains backup/copy/permissions tail, substitutes isolated verified dist and adds exact HEAD, clean tree, remote parent, and artifact digest gates. No main checkout pull/reset/stash or shared dependency install permitted.
- Cross-thread notification: JVC-OAI-WEB-PINS-D30 owner advised of forthcoming independent frontend SHA; orchestrator conflict-alert is alert-only, no process/evidence operations.

This file is evidence, not a runtime ledger. Current gate is solely `TASKS.yaml#runtime_ledger_json`.

## Root-cause matrix and bounded remediation

| Finding | Attribution | Remediation |
| --- | --- | --- |
| Related suite 20 pass / 1 fail | Pre-existing source-string assertion expects `<JuyiHall />`; unchanged entry includes onboarding event attribute. Reviewer verified parent/candidate identical test blob d39525f and entry blob 68bde50. | Nonblocking scoped baseline waiver; do not rerun/repair unrelated files. |
| Reviewer rejects malformed expiration | Existing util treats missing/nonnumeric expiration as not expired; new root guard must not interpret such envelope as a valid local login. | Owner validates finite numeric expiry and string token in helper only, tests malformed envelope and exact expiry; no shared auth changes. |

Main authorizes this narrowly diagnosed remediation, not a blind retry. Final candidate requires new exact review and targeted verification; prior candidate must not deploy.

## Corrected integration candidate

- Expiration fix: `d8ab13c1831a84f7ea50452b8431dbec1080491d`, tree `ae3bf505be43eeaed8558249155499c5d7904255`; Owner6 focused tests pass.
- During review another frontend task published `4538fa515002e3b746507a9656bc44a569f791dc` (native Mini Program orientation; 4 non-overlapping files), changing live index from `354162f...` to `3dbba1d8c6ee5c6d9eafaa99f102453b7650cb14bf1d89bf21c53dec943fd583`.
- Main conflict-free merged that new origin into our candidate: `bc24a4cc4d890cab96e3ac73d1834aa2b670f648`, tree `93cf42aff29cae969c441e804cf707000e15f81e`. Our three files byte-identical to d8, all remaining files byte-identical to 4538. No prior release is rolled back.
- Old candidate build rc0 is NONRELEASE; final build runs exact merged candidate, and its artifact must be used instead.
- Deployment adapter superseded original copy tail: full staging/permissions/digest, shared nonblocking `/tmp/cyf-release-web.lock`, live baseline compare, atomic Linux `renameat2(RENAME_EXCHANGE)`, old-live backup, and pre-switch cleanup. It preserves/reports old-live stage if backup move fails. SHA `13b05a0ebffc274b52661ec943ffa84cfe581102a0f863288514341702bb47e1`.
- Independent Sol final source ACCEPT on bc24/tree93cf; HOME-LOGIN P0/P1/P2 none, prior6 focused tests reusable by identical blobs. Ops adapter ACCEPT on SHA13b05a0e; residual narrow post-exchange/pre-flag signal cleanup window noted but nonblocking (new live intact).
- Final exact-tree targeted + actual memory-router verification: 31 passing / rc0 (`verify/final-bc24a4cc/tests.log`), including history replacement, query/hash, malformed envelope/expiry, exact expiry boundary and demo/callback noninterference.

## Released

- Exact final native-loader production build PASS rc0; source identity and working tree unchanged. Build config semantics independently accepted; wrapper-only runner failure attributed and corrected once.
- Final dist digest `7a788da8d9c6b4fe16f78b76ed29ba3d66bc4db40cc556a8c106c15e3245db55` uses explicit `LC_ALL=zh_CN.UTF-8` sorting. Initial deployment aborted before mutation because C collation produces `1ce0b906...`; both reproduced from unchanged files. Explicit locale corrected the guard without rebuild/artifact change.
- Reviewed adapter deployed bc24 rc0; backup `/home/isp/hosts/cyf/web/bak/kit_bak_20260907_105526_home_login`.
- Public index HTTP200/2907bytes and all five index-linked JS/CSS HTTP200, exact dist byte matches (`public-smoke.json`). Asset-check wrapper Python3.6 keyword failure was corrected before any asset request; no redeployment.
- Non-force push `4538fa5..bc24a4c` to origin/develop successful.
- Main dirty checkout status and tracked diff digest unchanged before/after. No backend/nginx/service changes, no real credentials used in tests.
