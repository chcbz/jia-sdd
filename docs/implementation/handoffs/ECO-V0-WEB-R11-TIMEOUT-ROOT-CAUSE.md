# Final Web focused run: controller-authorized timeout — 2026-09-06

Input38cf586e7f866671e745bb493eabb4c4c4a273c1/treec66750ef692cd3744f718c390afdf96fab2789a0; prepared one-shot wrapperSHA30f53be30b4627f8602123407ed3ae1d2d2afc720b72c499660868815d5bb433. Actualsingle run session41540, wrapper started19:46:09, Node19:46:13. Previous19:44freshAPIhealth200/resourceobservation and monitorwindow authorization were real. No Vite/Gradle/DB/second Node was admitted.

At21:30exactowner Curie verified wrapper1742200→bwrap1742308→Node1742309, Nodestartticks3026771582, elapsed6251s andCPU01:04:15. Bothreport/stderr had stayed0bytes since19:46:14, no exit/status. Main interrupted only the Agent's lengthy reasoning to request a factual handoff; no host process was signalled by main. Main subsequently explicitly authorized the exactowner to conditionally sendSIGTERM only to its confirmed own hungNode. Curie did so at21:30:26; no name/group signals, noSIGKILL, no foreignprocess/daemon/service/monitor/donoroperation. Session41540then terminated. `exit-status.txt` records testchild143; finalouterwrappercode is not yet independently confirmed. Its subsequent attempt to parse emptyJSON failed, a secondary control-reporting error, not Mocha test results.

Evidence in `.evidence/eco-w11-r10-38cf/`, explicitly read-only handed off to main:
- controller-timeout-exact-identity.txt SHA66c97e895c60ffd6c498e2b63ddbdd03afad66ece7e187193fa7771660324d79
- controller-timeout-signal.txt SHA215fae11a6abf495ab336fabfd5e95463de75dc2566d117e51299a45ef6fbd83
- exit-status.txt SHA9d9b18720961e9b4689fd763b85e7b6f36160ccd3a8a1c9ddc5103bb0f66c396
- Originalemptyreport/stderr preserved; **no testcase/pass/fail/skip totals exist**. No tests may be called passed, failed or skipped from theseemptyfiles.
- Sourceclean38cf/c667; donor dev64769/inode2626877 andlockSHA0b73dab31d80a337585c5b8cb6e1de0dbc9183fc717aef1b3b9de92de244927e unchanged perownerpostcheck.

## Root-cause matrix / stop

| Finding | Attribution / remaining work |
|---|---|
| CPU-active run >100min with zero output | Stage and offendingmodule/case UNKNOWN. CPUactivity does not prove memorypressure/OOM or a productioncommerce defect. |
| Mocha timeout10000 did not end process | Per-testtimeouts do not establish an outer bound for moduleloading or event-loop-starving work; no stage evidence exists to select a sourcefix yet. |
| JSON-only terminal reporter | No progress markers survived because final report never materialized; need incremental phase/case output alongside final JSON. |
| Wrapper no total deadline / emptyJSON postprocessing | Control gap: next isolated diagnostic must have finite outer runtime and preserve original childstatus even if finalJSON is absent; never erase/reuse thisrun'soutputpaths. |
| PriorR10one-lineassertion sourcefailure + currentactualtimeout | W11 second consecutive failure requires blocked_root_cause. Sourceacceptance remains source-only; earlier48c79146passes stay historical, not thisrunPASS. |

No runtime/source/diagnostic GO follows this matrix. Next bounded preparation: identify entry/module loading versus test execution using a lightweight progress harness and one small selectedfile group under an exactowned watchdog; retain all actual commerce/Hall assertions. Freeze newwrapper/fixture/selector pins and independent review before one diagnostic execution with fresh APIhealth/resourcehandshake. Do not rerun unchanged11filewrapper or infer success from namespaceprecheck. Exactowners alone control their processes. AllECOconsumers are now ended, so release donorloan and heavywindow explicitly; any laterdependency use requires renewedidentity/loan confirmation.

## 2026-09-07 read-only localization (not a rerun or proven runtime cause)

Original Curie completed static inspection only; main independently checked the source excerpts. Frozen38cf/c667 `tests/juyiting-component-behavior.test.js:808-817` implements queued RAF callbacks in a Map; line831 synchronously drains `while (frames.size) runNextFrame()` without a bound. Global RAF forwarding at33-34 now reaches the overridden window RAF. A callback that requeues while waiting for a layout/observer condition can therefore starve the event loop and prevent a per-case timeout from firing.

Concrete candidate producer: `src/components/juyiting/HallStage.vue:280-337` (`settleFinalViewport`) schedules inspection repeatedly while the container has no positive viewport or a ResizeObserver has not reported. This test does not establish these conditions locally before its drain. Whether this was the callback active during the sealed run remains UNKNOWN; there is no runtime stack/progress evidence. Do not blame a production commerce loop or OOM from this static finding.

Smallest proposed follow-up: only `tests/juyiting-component-behavior.test.js`, grep `throttles return refresh, polls reset completion, and cancels callbacks on unmount`, with a new 45–60s outer bound, timestamped load/case progress and incremental output retained if no final JSON is produced. A bounded, observable frame pump and explicit geometry/observer fixture may be needed as test-only remediation, preserving all original throttle/reset/unmount assertions; it is not implemented or authorized by this note. Any watchdog process control stays with the exact runtime owner.

Voice release controller subsequently confirmed that the current priority is integrating completed source and releasing with existing bug evidence retained; ECO must not open additional API/DB/Gradle probes that compete with release work. No Node/dependency use, source write, test rerun or build occurred for this localization. Follow-up diagnosis belongs to a separately admitted defect task; old donor loan remains released.
