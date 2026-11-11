# W07 R3 lifecycle verification — 2026-09-06

Exact `d56e205c558fb2370c80921ce9ca4e9d2aea07a7` / tree `0a6b87991f20079103fae4a9b52360d13b4c25a9`, clean. Independent source delta ACCEPT0/0/0 plus actual noDB lifecycle **6 tests / 0 failures / 0 errors / 0 skipped**. Session23605 naturally exited0; one Gradle invocation, 42m21s,23tasks(2executed/21up-to-date), no databases allocated. Slow startup was not treated as a hang or restarted.

- Evidence key `3c5763d8341911b66066df749cb9f121d1d9530c255b298ab1c078c9daa1026b`, accepted cache HIT verified.
- Log `/var/tmp/eco-w07-r3-lifecycle-nodb-mbSFY6/gradle.log`, SHA256 `84bf602dd9582cb70a3f3fa2da36d9031dd74c27e73364f9da9b788e9ef2913b`.
- Saved lifecycle XML SHA256 `0b42de1e3d0230a05f72936e71d631480a7cc1599bc42fbdf0ff6cc3fa883e9b`.
- Fixture digest `968111f0f91ea57b64087fadfb2e6bcb3cca929c628b7e36a7a612fa3a0be5f3`.

These six cases are mock JDBC/worker lifecycle proofs, not real MySQL completion. Earlier production-source/noDB10PASS/MySQL4PASS keep their original scopes; two original failed MySQL cases remain to retry.

## Control preflight correction

Verifier accepted the new r3 wrapper's cache-before-allocation, exact two selectors/XML2/0/0/0, failed/unknown retention, owned-session-zero and scope-only cleanup design, but rejected CREATE USER password passed in process argv. Main generated `/var/tmp/cyf-eco-control-w07/run-w07-r3b-mysql.sh`, SHA256 `0db3fba4b295a64eace0e2cad0283745fcc7660aaaf9cde2a0f5c52e58232710`: CREATE USER through stdin, explicit tracing-off before secrets. New selector/log identity. Syntax check passed; cleanup function byte-exact SHA256 `82b317d8c220140b3073503d762ae931a9c943ba73c26bed04aa8936503b0a2c` retains the seven earlier stub-branch proofs. No MySQL has been run through this corrected wrapper by the main.

Next: original verifier independently checks exact stdin/tracing delta; conditional GO only if clean. Any preflight failure stops before allocation. Actual selector execution must use its canonical ledger verifier admission and orchestrator; accepted complete evidence only after actual two-case pass and owned cleanup0/0. No source acceptance/deployment inferred from wrapper syntax or stub checks.
