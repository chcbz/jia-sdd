# Public beta dependency hardening tasks

- [ ] Upgrade DOMPurify to a non-vulnerable release and add adversarial Markdown/Chat sanitizer tests.
- [ ] Resolve PostCSS and nanoid advisories without force upgrades and verify no runtime bundle exposure.
- [ ] Run focused/full relevant tests, lint/build, production `npm audit --omit=dev`, and static artifact diff.
- [ ] Obtain independent security review and complete SDD pin/verify before the next dependency-bearing public-beta release.
