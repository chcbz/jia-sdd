# JVC-OAI-OPS R17 edit-tooling stop matrix

2026-09-05. No new candidate or runtime execution. Prior protocol/root-cause scope is unchanged from `JVC-OAI-OPS-R17-STARTUP-ABORT-ROOT-CAUSE.md`.

Base remains clean `0c07d43335601ce680ab16412639cad2b212e4db`, tree `4bd17202f4ef86eca0933b606e367bfbb9598a74`, source SHA256 `b2dd9b146eb28ce248bdbe2f8cd230fa6d97243f2e18573b5afc8bdf62654222`. Controller independently checked clean/HEAD/tree. Writer `01a070bb-0ab8-7d93-a258-2587749f3843` stopped after two implementation-command failures.

| Attempt | Exact evidence | Attribution | Correction |
| --- | --- | --- | --- |
| Inline replacement script | `{"event":"failure","failure_type":"IndexError","message":"list index out of range","namespace_init_pid":null,"protocol":2,"supervisor_pid":703352}` | Nested triple-quote delimiters collided; embedded definitions/main ran in edit helper. Missing argv failed before supervise, Popen, fork, namespace or signals. No target write. | Never execute replacement target text as an editing program. Use direct patch mechanism. |
| Compound snippet replacement | `exec_command failed: CreateProcess ... rejected: rm -f style commands are not permitted. Use a safer approach` | Entire command was rejected before execution; intended `/tmp/jvc-r17-protocol.snippet` and `/tmp/jvc-r17-owner.snippet` were not created. Not a product or runtime failure. | No temp snippet deletion command; direct patch-only editing. Separate static AST parse from editing. |

## Bounded authorized successor plan

After matrix-bound `authorize-remediation`, the same owner may implement only the existing R17 startup-timeout/abort fix in `tests/self_test.py` using direct patches. No new helper framework, alternate product path, temporary deletion, source-evaluating replacement script, namespace, selector, signal, Gradle, production, flag or key action. Static parse must parse source/embedded string **without executing either**. Record exact new commit/tree and fresh independent review before ONE staged lifecycle test. Preserve all previous attribution and cleanup/route/count/digest contracts.
