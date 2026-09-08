# Acceptance evidence

Verification and source push on 2026-09-08. Cloud build/deployment outcome is unverified; Mini Program upload and device acceptance remain pending.

## Automated
From `web/`, PowerShell:
```powershell
$env:MINIPROGRAM_PROJECT='C:\Users\Think\WeChatProjects\juyiting'
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter spec tests/public-entry-navigation.test.js tests/public-pwa-beta-entry.test.js tests/juyiting-mini-program-orientation.test.js tests/juyiting-experience-mode.test.js tests/home-login-redirect.test.js tests/juyiting-hall-onboarding-geometry.test.js
node --test tests/hall-onboarding.test.mjs
```
- Post-sync focused suite: 54 passing. Includes actual SFC rendering, all three templates through four steps, focus/scroll, ordinary routes, portrait query continuity, rejected arbitrary queries, cold launch and fallback.
- Post-sync onboarding: 23 passing. Integrated remote Web `fe670bf` and root `62836c3`; preserved the new logged-in root redirect and upstream onboarding assertions.
- Pre-sync local build passed (exit 0), with 44 focused + 19 onboarding tests. That build is not evidence for the subsequently integrated upstream changes. Log: `D:/tmp/miniprogram-public-entry-build.log`. The updated runbook delegates formal builds to the cloud pipeline after source push.
- Mini Program JavaScript syntax check passed.

## Browser evidence
Local Vite on `http://127.0.0.1:8088/`: home 390x844 and 1280x800; demo content template through four steps; result at 320x740 without visible horizontal overflow; workbench link retains template + portrait; new heading receives focus. This is desktop-browser viewport emulation, not device acceptance.

## Review
Independent read-only review: ACCEPT, no blocking findings. Reviewer independently reran 44 focused + 19 onboarding tests and both Mini Program page syntax checks. Generated declaration noise was removed; the suggested PWA workbench short label was aligned to “工作台” with an assertion and a fresh focused-suite/build rerun. Pre-sync build and post-sync scoped regressions passed; `git diff --check` passed.

## Outstanding
No real login/production task execution tested. Release both packages, verify the configured business domain and real Android/iOS WeChat route stack, login return, and repeated landscape entry/portrait return before marking accepted.

## Source publication
- Web commit `fce21d20a5a3ba761365a8eb411f1519bdc47099` pushed atomically to `origin/develop` and `origin/master`; both remote refs verified.
- Root integration pins the pushed Web SHA; see `integration.yaml`. Git Bash exited 49 without output, so native Python performed the equivalent `sddw pin/verify` checks: five nonempty required artifacts, exact 40-character API/Web pins matching both checkouts, and root base SHA.
- External Mini Program directory is not a Git repository. Its `pages/index/index.js` remains local, fingerprinted in `integration.yaml`; it is not included in either Git push.
