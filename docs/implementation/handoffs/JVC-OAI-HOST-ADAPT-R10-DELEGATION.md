# HOST R10 test-only delegation contract — 2026-09-06

R9 once-all naturally ended rc1 in22m24s, exact b0f797cf9ee9c32ebc88054b61a6cc60d3842cec/tree09948de0d0e9b4af3b84b244fd693303d3330709 before/after clean. Evidence /tmp/cyf-host-adapt-r9.D0sM5l; failed cache dbcfc5573f5c0063396d7834fb0ee30937c6387bf278307c4f234012a3fd31a6. build-contract, locks, transactions PASS; activation reached stale assertion at line873, installer tail not reached. No allPASS, no production.

## Second-failure root-cause matrix (loop stopped)
| Failure | Cause | Bounded remedy | Gate |
| --- | --- | --- | --- |
| R8 unavailable rg | mandatory fixedPATH excludes ripgrep | accepted R9 trustedgrep and error distinction | R9 three groups now pass |
| R9 orchestrator delegation | test requires literal canonical path in build-api.sh; real builder calls ORCHESTRATOR_PATH loaded by api-host-transaction.sh, whose input parser pins exact absolute path | replace stale duplicate assertion with canonical path-definition/load + parsed build argv checks, fail before expensive fixtures | independent testdelta review + remaining selector |

Original HOST Writer only edits ops/release/tests/test-api-host-adaptation.sh in original worktree. Do not change production sources or weaken canonical delegation. Existing build shlex argv check is valid and already passed. Add pure static path pin/load/build-contract validation including negative mutated in-memory inputs (wrong path, missing pin/load, wrong call). Reuse validation at start of activation-installer-nginx so its standalone invocation cannot skip the contract; avoid redundant costly fixtures. Audit remaining static assertions in this one test for similarly stale source-location assumptions. Direct patch, Bash4.4/Python3.6; no guessed filenames/heredoc-generator.

Authorized Writer verification: syntax/AST and pure validation microprobe only, no selector/all/Gradle/network/production. Freeze clean candidate for independent source/safety review. After acceptance, independent Verifier first runs build-contract and activation-installer-nginx once on new tree; locks/transactions production+fixture bytes unchanged may be reused only with explicit delta/equivalence evidence, not fabricated new-tree all cache. Any further failure must be attributed before retry. Preserve previous evidence, no repeated22minute all by default.
