# W10 R5 cache isolation attribution — 2026-09-06

Admitted original verifier: session83131 naturally exited92 after installer **92 tests/pass, 0 failures/cancelled/skips** on clean `4bd0c257` / `7600bc8a`. Packaging and client/managed-host selectors did not start. This is wrapper environment/cleanup classification failure, not an installer assertion failure; no repeat of installer is authorized.

- Original directory `/var/tmp/eco-w10-r5-node-OwCmnK`.
- Installer TAP SHA256 `f37f427d23bbb82f8ce1ef9d33bef20834b3f04f944dd48655e9a49d464f8975` (independently checked).
- Fixture digest `02f5af2ec5ba0651f923aa0395dd415bb04a27953ee75735e2cc83956f354f30`.
- Original installer key `fdfc2f5dd158bd449a89b5ec119bcdfcdef6b8a627435c27bac2e6307c73329c`, not previously recorded accepted.

Actual root cause: installed npm `lib/cli.js:2–5` explicitly invokes `node:module.enableCompileCache()`. Dependency setup shares the test TMPDIR, leaving only `node-compile-cache/` (587 regular files, no symlinks). Original wrapper interpreted every TMPDIR entry as leaked test fixtures. Main verified this sole entry, types and original TAP; no other fixture entries and no source changes.

Bounded correction: new continuation wrapper places build cache outside fixture TMPDIR and disables optional Node compile cache, preserves original cache/evidence, verifies exact old TAP/fixture/tree and records installer-only composed proof without rerunning tests. Run only previously unstarted packaging and client/managed-host selectors. Fresh per-selector fixture/cache identities; original wrapper rc92 remains rc92, not full PASS. No delete/relabel of retained compiler cache, no process/runtime/data/log operations. Original verifier independently preflights new wrapper then executes once only after explicit GO; any second failure stops at root-cause matrix.
