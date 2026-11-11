# JY-LAYOUT R1 root-cause stop — 2026-09-06

Candidate d4ff7d80ac8089b6cdf24d618b94da3bd2cac9ab / tree 7eac1dd25956f79383904de7871d91840bcbe6db is NOT accepted. Owner report 01a0750e-5b93-7341-9b18-23a11744a900 is failure evidence, not a passing suite receipt.

| Failure | Root cause | Bounded remediation |
|---|---|---|
| New reader CSS-only Chromium fixture ETIMEDOUT at 30s | Owner launched browser outside authorization; copied synchronous cold-start harness has insufficient startup and synthetic DOM does not exercise production reader | Remove newly introduced raw Chromium test; verification-only Agent owns production static/CDP layout checks with separate 180s startup budget |
| Experience existing no-API initialization test fails at listener=null | Presentation viewport now intentionally subscribes while physical orientation remains independent; legacy test asserted old implementation rather than invariant | Retain no-API/keyboard orientation invariant; assert listener registered, live presentation height updates, physical mode unchanged, unmount cleanup even on assertion failure |
| Archive full run interrupted exit130 | Unrequested broad suite; no final total; owner self-terminated own process after pause | No success claim or rerun of broad suite; use exact targeted mode selectors, final static production reader geometry |

No process preemption or foreign evidence access is authorized. Source Owner is paused. Main authorizes one test-only correction commit in the same isolated worktree; production code remains frozen pending independent Sol findings. No browser/build/Gradle runs by Owner. Run only experience-mode mocha file with --timeout 30000 after static correction; capture command/output/exit to own evidence. A further failure is attributed before any retry. Main continues read-only review and verifier harness preparation in parallel.

## Independent Sol addendum (same bounded remediation)

Reviewer Godel 01a07513-02e0-7cb0-b310-647ec43bfae4 REJECT on d4ff7d8 found two additional concrete gaps before retry: chat fullscreen relies on :has() and retains inset overlay padding in unsupported legacy hosts; selected-agent-card.test.js:211 still requires the removed chat top-gap CSS. Main extends existing remediation scope to JuyiHall.vue explicit reactive chat overlay class + direct selector (no :has dependency for chat), remove now-unused top-gap variable, and update that one legacy test contract. Reuse all other production bytes. Owner may additionally run selected-agent-card.test.js in the same bounded targeted mocha invocation; no new browser or broad suites. Review verdict retained and final exact delta requires independent confirmation.

## Bounded correction evidence

Owner returned clean 94f75555acd6ee71b8be8ecbb03b9117ee0c9907 / 08b43439e19b0b4f8b8c4d1eaa5343568f666330. Mode selector natural exit0: 25 PASS (/tmp/cyf-evidence-JY-LAYOUT-UI-20260906-20260906-131624). Selected-agent selector first 10PASS/1FAIL due to test CSS helper not parsing grouped selectors (/tmp/cyf-evidence-JY-LAYOUT-UI-20260906-20260906-131854-selected-agent-card); helper corrected before one bounded rerun, 11PASS natural exit0 (/tmp/cyf-evidence-JY-LAYOUT-UI-20260906-20260906-132043-selected-agent-card-retry). Prior failures remain recorded, not converted to passes. Exact loader used --import ./node_modules/tsx/dist/loader.mjs because bare loader resolution failed in symlink dependency environment. Production build/read-only final review remain separate gates.
