# JVC-OAI-OPS R9 TMPDIR attribution

Date: 2026-09-04
Failed non-promotable snapshot: `8afe14f4fafbad223b643e0764d1d440b4f809d2` / tree `2dbc858d42edf2a72d570f5da16b8ad3ebf659a1`

The single authorized live-matrix selector did not enter the test matrix. Its environment set `TMPDIR=/tmp/jvc-r9-live-matrix`, but that directory had not been created; Python `tempfile.mkdtemp()` therefore raised `FileNotFoundError` during runner initialization.

The source changes are limited to the previously authorized NUL-safe JSON argv transport and phase-aware `sealed_before_staged` postconditions. They remain unverified. No P1/R7 regression, production, key, flag, deployment, restart, reload, review, or merge action occurred.

A fresh Terra successor may create the dedicated mode-0700 TMPDIR parent, verify ownership/type, then execute the live-matrix selector exactly once on the exact snapshot without changing source. Only a PASS permits focused P1/R7 regressions, pycache cleanup, and a clean candidate commit. Any failure stops for attribution.
