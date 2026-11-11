# HOST R6 test-harness correction

First admitted all selector on source-accepted3a31c89b/treec9022a4c returned1 before any PASS. Full owned evidence /tmp/cyf-host-adapt-r5.Ayh40C, empty stdout SHA e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855; stderr SHA c38c1c0809ea767ec16747013306d79209b583fce4368f365485f43ac8a6e5e6. Cache failed4353c63c008fa6322a50284065a372ba7d00b3a1fdebff272a6340155295703b. No passing group/runtime lifecycle/network tests reached.

## Precise attribution (supersedes preliminary call-hardening hypothesis in fail summary)
Embedded Python line5 is `end = text.index('\n\nBUILT_JAR=', start)`. Actual build-api has `assert_clean_candidate api-after-build ...` immediately before BUILT_JAR, so that delimiter is absent. Subsequent task token also encodes literal `\\n` rather than actual line-continuation/newline. The executable selector retained the stale text-shape assumptions despite separately corrected earlier static checker. The production orchestrator invocation itself has correct options-before-task-ID ordering and must not be changed to satisfy this harness.

Bounded original Writer R6: ONLY ops/release/tests/test-api-host-adaptation.sh. Fix real embedded build-contract parser deterministically to inspect actual command boundary and token order, retain every admission/nonpublishing option and metadata assertion; no weakening to a mere substring-presence check. Static source checker may run the pure read-only embedded build-contract assertion itself to prove parser now matches source; this is explicitly permitted bounded local text parsing only, not invoking build-api/orchestrator or whole selector. Preserve rest of selector bytes, source accepted implementation and canonical/common unchanged. Clean test-only commit then independent narrow delta review before one new-tree all.

## Evidence collector defect
Verifier's shell exited on selector failure before after-snapshot. Main independently confirmed same exact HEAD/tree and empty git status afterward; this does not manufacture missing verifier after-file. Next verifier invocation must use explicit `if ...; then rc=0; else rc=$?; fi` or equivalent capture, always save rc/endtime/afteridentity/fullstdout+stderr/hashes, then report original status. No rerun on old tree and no implicit retries. Main handles ledger attribution.

Controller stopped at second threshold before this authorization. All prior evidence preserved. No Gradle/build/npm/production/credentials/runtime changes authorized.
