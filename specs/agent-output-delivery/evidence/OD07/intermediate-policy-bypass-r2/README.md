# Intermediate bypass repair round2

Failed batch:114 tests,2 failures,0 errors/skips across nine original XML reports. Root independently parsed the frozen policy-bypass-guards-r2-xml-1789246585 reports and copied them with stdout/exit byte-for-byte. archive.json records hashes. No rerun or cumulative test count.

The funded creation refusal test now passes. Legacy report's remaining failure is UnnecessaryStubbingException. Scope-miss now passes its NOT_FOUND assertion but fails an old WantedButNotInvoked expectation. Writer was asked to remove obsolete test setup/interaction expectations while preserving early rejection and absence of writes, not restore unnecessary access to satisfy old mocks. A passing repaired run is still due.

Scoped adapter5/5, including the release null-omission case, remains separate from the failed batch verdict. Source association, remaining affected HTTP/core checks, new real MySQL gates and independent frozen-candidate review remain pending. Do not use this report to claim OD07 completed.
