# PWA-INTEGRATION-WEB-RC R4 verifier root-cause matrix

Approved by the main controller on 2026-08-29 for one final exact-tree verification cycle.

Exact candidate: `d335a6411f4133db9f4da7395803ed13f3be87cc` / tree `fdc5f6de80e09da0e6716bf4f21eb2f4920a74c8`.

| Attempt | Symptom | Root cause | Corrected command/scope |
|---|---|---|---|
| 1 | 2 pass / 9 fail in legacy Juyi tests | Wrong stale selector packet; the same files are byte-identical to accepted O04 and stale exact-string expectations do not represent the integration gate | Use accepted PWA R3 selectors, O04 Gate 12.2, merge identity, and builds |
| 2 | Two liveness tests timed out under Mocha `--grep` | The accepted R3 liveness evidence used Node's test runner, not Mocha; the verifier changed the runner contract | Exact command: `node --test --test-name-pattern='process-tree cleanup polling keeps|CDP close timeout keeps' tests/juyiting-preflight-config.test.js` |

The final cycle must use these exact selectors:

1. `node --test --test-name-pattern='process-tree cleanup polling keeps|CDP close timeout keeps' tests/juyiting-preflight-config.test.js` (expected 2 pass).
2. `node --test tests/juyiting-preflight-config.test.js` (accepted R3 expected 59 pass).
3. `TSX_TSCONFIG_PATH=jsconfig.json node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter spec tests/composables/accountSecuritySession.spec.js tests/public-pwa-beta-entry.test.js tests/pwa-service-worker-localhost.test.js` (expected 15 pass).
4. O04 Gate 12.2 exact ten composable specs (expected 56 pass).
5. Feature-enabled production build to `dist-feature-r4`, then final default production build to `dist`; restore generated tracked files and remove only run-created `dist-feature-r4` after sealing its digest.

No stale legacy selector, production access, credentials, Chromium, or source changes are authorized. Any further failure stops.
