# Web inspection verification closeout — 2026-10-02

## Exact candidates and immutable archives

- Original: `1496f486e361cc4f9515c8840bc459c0adb78e38`, tree `006e7e88d3bacaa3f05e81d5c09e2eaebfd53d9e`; `git archive` stream SHA-256 is recorded in `git-archive-stream.sha256` (`dfd59b8a2baa9d46d97e9827623549f7024af2ff4a7ae515254f9432b3c1d3ae`).
- Verified child: `5e72cd8b5f22c21d80b4d3a349b6f3f6b44a56bc`, tree `08774d4f80a9df7806580bc2485bdfb48dacba99`; `git archive` stream SHA-256 is recorded in `git-archive-5e72-stream.sha256` (`478a2e82036d8610bbf3e043af16a64abc668bf7392c857f4c16abf9e252c14c`).
- Both probe runs imported the composable from their respective immutable archive, and the cold-recovery fixture passed its actual `entries[].request.turns[].route = INSPECT` catalog page through `catalogPage()`.

## Preserve original source result (do not relabel as child evidence)

`raw-probe-result-1496-final.json` is the final real-composable result for exact `1496`: all three checks FAIL.

1. Cold recovery called `.../typed-outcome` rather than `.../inspection-outcome`, and displayed no projection.
2. READY INSPECT explicit confirmation returned `false`; `onProposalCalls=0`.
3. A READY INSPECT ANSWER left the accepted/waiting status visible.

These are source behavior results, distinct from the old preliminary empty artifacts `raw-probe-result.json` and `raw-probe-result-v2.json`. Those files are zero-byte, so they contain no execution trace or source verdict; they are historical harness/collector empty-output artifacts and are not used for attribution.

## Child result

`raw-probe-result-5e72.json` is the final real-composable result for exact `5e72`: all three checks PASS.

1. Cold no-storage catalog recovery called `.../inspection-outcome` and displayed READY/INSPECT/ANSWER.
2. READY INSPECT explicit confirmation returned `true` and invoked the existing proposal callback exactly once with the GENERATE_IMAGE payload.
3. Submitted INSPECT followed by READY ANSWER produced `inspectionStatus=""`; trace retains the expected inspection POST and inspection-outcome GET.

The child probe harness is `inspection-behavior-probe-5e72.mjs`; its SHA-256 is in `5e72-harness.sha256`. The explicit pending-INSPECT CHAT continuation is covered by the targeted interaction suite.

## Targeted tests (already executed once; no repeat)

Command (against exact child archive with existing read-only dependencies):

```sh
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter spec tests/juyiting-typed-deliberation-interaction.test.js tests/juyiting-typed-deliberation-page-routing.test.js tests/juyiting-typed-deliberation-wire.test.js
```

Observed command exit: `0`. Evidence: `5e72-targeted-tests.stdout`, `5e72-targeted-tests.stderr`. Result: **28 passing** (11 interaction + 10 page-routing + 7 wire). Stderr contains only non-failing pre-existing Vue component-resolution warnings; no test failure.

## Lightweight static checks

- First scoped lint launch exited `2` before evaluating rules because the exact archive’s dependency copy lacked `@eslint/js`. This is recorded as **NOT_RUN_ENV_DEPENDENCY**, not a source lint result, in `5e72-scoped-lint-initial.status` with raw stdout/stderr retained.
- A single materially changed-input retry used archive-local symlinks only to the existing read-only `/home/isp/wsps/cyf/web/node_modules`; no package installation, app-source change, build, or production action. `5e72-scoped-lint-repaired.status` records exit `0`; stdout/stderr are empty, so scoped lint PASS for the three changed files.
- `5e72-sfc-compile-four.status` records exit `0`. `@vue/compiler-sfc` parsed/compiled these four exact-child SFCs successfully: `BountyDiscussionPanel.vue`, `ChatPanel.vue`, `BountyTypedOutcomeCard.vue`, and `JuyiHall.vue`. Details are in `5e72-sfc-compile-four.stdout`.

## Source binding

The nine actual exact-child archive source hashes are recorded in `5e72-nine-source-hashes.sha256`; this includes the four compiled SFCs, `useHallTypedDeliberation.js`, its frozen wire/catalog dependencies, and the relevant targeted tests.

No browser, Gradle, full build, application-source write, ledger operation, or remote service action occurred in this closeout.
