# JVC-OAI-OPS R9 live-cell attribution

Date: 2026-09-04
Exact candidate: `8afe14f4fafbad223b643e0764d1d440b4f809d2` / tree `2dbc858d42edf2a72d570f5da16b8ad3ebf659a1`

## Observed failure

The one authorized execution of `r8.entrypoint.live_sensitive_input_every_durable_phase` ran from `2026-09-04T10:11:25Z` through `10:26:36Z` and failed after 15:09 at:

`phase=sealed_before_staged`, `input=files:nginx_http_snippet`.

The dedicated TMPDIR precondition passed (real directory, owner UID 0, mode 0700, not a symlink). The NUL-safe JSON argv transport therefore progressed beyond the prior R9 initialization issue.

The wrapper suppressed the underlying bare assertion detail and the fixture was removed in `finally`. The remaining possible postconditions are the pre/post journal emptiness and old-selector identity checks. No exact failed post-state was retained, so this evidence does not distinguish a product state-machine defect from a test-observability defect.

## Bounded next action

A fresh Terra owner may modify only the live-matrix test harness under `ops/juyiting-voice-production/**` to:

1. give each precondition/postcondition a unique message containing phase, input, return code, journal names and selector;
2. retain a deterministic diagnostic receipt outside the disposable fixture for a failed cell, without secret/config contents;
3. preserve the unchanged production entrypoint/module and all real live mutations.

Then run the full live-matrix selector exactly once. A PASS may proceed to focused P1/R7 regressions; a failure is the second consecutive post-attribution failure and must stop with its exact retained post-state. No full inventory or production operation is authorized.
