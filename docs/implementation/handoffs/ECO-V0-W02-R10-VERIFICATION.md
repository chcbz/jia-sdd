# ECO-V0-W02 R10.1 verification evidence

Current execution state remains solely in `TASKS.yaml#runtime_ledger_json`.

- Candidate: `70ec1dfb1fb7c613a66441dd8b046e17eeaf0920`
- Tree: `354f06b70be22dba3bf823f579d6b4d820278c9b`
- R10 implementation: `515d45eda2bacb83e55f5f5bae8c87995efc3673`; R10.1 only corrects fixture suffix `trigger-race` to `trigger_race`.
- No-DB selector: `economy-r10_1-no-db-review-remediation`, BUILD SUCCESSFUL; mapper task UP-TO-DATE, service test executed. Evidence `8ad6088fdfdac4a1299e4b2990f82bbad42ac45ec76066652cb2f38e57114c93`.
- Isolated MySQL selector: `economy-r10_1-mysql-review-remediation-100-concurrency`, BUILD SUCCESSFUL. Fresh XML: schema initializer **6/0/0/0**, posting concurrency **5/0/0/0** (tests/skipped/failures/errors). Includes concurrent initializer and 100-request debit conservation. Evidence `c75ef1fc18566afd073610fa2afc576d19f8c46239790182a8c275eaa776e9ef`.
- Artifact SHA-256: no-DB `3ab8efb25490f1b38e9416cb248ca0bb20206a6c099abb9f9f16ceece63cb15f`; MySQL `1f1404cba62c1704d566d72e72c9c2d51db7c7c8136db5a3bcb37276eaa182d2`.
- Main-controller read-only cleanup audit on 2026-09-05: databases with exact prefix `eco_w02_verify_` = **0**; loopback users with prefix `eco_w02v_` = **0**. Queried `LEFT(name,CHAR_LENGTH(prefix))`, without modifying any database/user.
- Worktree clean; no deployment. Successful Gradle evidence is not independent review acceptance.

Attribution retained: R10 MySQL test failed solely because its new suffix used a hyphen disallowed by the existing fixture safety grammar. R10.1 changed that test input, not the safety grammar or production code. Earlier verifier Python `time.time_ns` setup failed before Gradle; fixed literal fixture digests avoided that unsupported Python 3.6 API.

## Independent review

Reviewer `01a07051-2528-7c23-9a12-e64ea94365c6` (`sol_reviewer`) returned **ACCEPT, P0/P1/P2=0/0/0** on the exact candidate above. All six prior findings closed within the frozen V0 scope. Treasury HTTP authentication/non-production enforcement belongs to W03; task/funding root lock and ACL composition belongs to W04. No production-hardening scope was added.
