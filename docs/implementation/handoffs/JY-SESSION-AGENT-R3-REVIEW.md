# Agent source review remediation

Independent Leibniz REJECT on 96d765ae549225ecbe97e2f4885d80560e343bfa / 91286f1a4d1bad615c18e828443187f9b5d167f2 despite 28 passing tests:

- P1: force-new managed commands may carry conversationId; unconditional session capture overwrites the chat mapping with an isolated command session. Restrict persistence to eligible resume-mode chat runs; runtime tests must prove commands neither create nor replace a map entry.
- P2: atomicWriteText renames before later chmod/fsync. A post-rename error can leave the new disk map while memory is old. Reconcile the committed map safely or fail closed; add injected post-rename failure coverage, retaining prior pre-rename failure coverage.

Original critical_worker owns bounded fixes in existing three files and new focused tests only. No deployment until exact corrected tree and independent delta ACCEPT. Release must clone byte-exact full baseline siblings/dependencies then overlay accepted runtime changes; validate staged entry with APP cwd before activation.
