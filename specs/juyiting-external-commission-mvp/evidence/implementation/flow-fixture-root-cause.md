# Flow219→220 fixture root-cause matrix (2026-10-21)

Owner external-main, single Agent. Not a repeat of unchanged input; no waived assertions.

- Run219 / cbfd347a62: 12 failures; two duplicate-suite Mockito calls came from when-restubbing invoking previous Answer, five legacy identity tests supplied owner as tenant, three funded guard tests lacked exact scoped task, two PWE call-count assertions counted delegating fixture authorization lookup. 58dbc72bb3 corrects fixture data and uses independent doReturn mapper stubs. Run220 proves these pass except the deeper legacy registration precondition below.
- Run220 / 58dbc72bb3: 2887 tests, 1 failure, 122 skips, compiler 0. Remaining legacy identity test assumed registration minted a token; current production requires an existing unified runtime session. 664b2576b4 adds a synthetic persisted session fixture, asserts pre-session registration denied/activation rolled back, and asserts registration/repeat never mint or rotate token. No production authentication weakened or tests removed.
- New policy real MySQL 12, HTTP8, Skill execution27, Skill policy11, Chat authority14 all passed at Run220. Not a whole-release pass.
- New exact candidate 664b2576b49f277b3289c52e4eacf9d67f5d62ba / tree35c696b8706c67de47f1789002469414e7adb0f9 must rerun full retained policy before same-Run deployment. Evidence /var/tmp/cyf-external-flow-20261021/r3/diagnostic.json and r4/diagnostic.json.
