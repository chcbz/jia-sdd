# OD05 independent review — REQUEST_CHANGES

Candidate `3af0c43383d5c5f064830937ea6801d92311ed72`; independent read-only reviewer `/root/od05_review_fallback` reviewed all12 changed files. Existing architect provider failed twice before giving a verdict; this report is from the replacement independent reviewer. No product/root files were changed by the reviewer.

| ID | Priority / location in candidate | Finding / required repair |
| --- | --- | --- |
| R01 | P1 `src/utils/outputDownload.js:34`; `src/composables/useOutputs.js:291` | Real useOutputs→downloadOutput→useHttp plus controlled fetch/identity microtasks gives identity-cleared→create-old-blob-url→save-old-identity-file→AbortError. Caller generation check occurs after saving. Recheck cancellation/context before any Blob URL/save side effect. |
| R02 | P2 `src/composables/useOutputs.js:185` | Refresh always merges old items. An authoritative empty page with null cursor still leaves an old AVAILABLE card/title. Reconcile refresh, revocation/removal and pagination so stale authority is not permanently retained. |
| R03 | P2 `src/composables/useOutputs.js:114` | syncing OR retryable permits5s polling after403 with explicit retryable:false. Nonretryable errors must take precedence over syncing. |
| R04 | P2 `src/components/outputs/OutputList.vue:122` | computed reads nonreactive window.location.search; same /chat instance navigated from v1 to v2 continues requesting/displaying v1. Consume a reactive route request and watch exact outputId/version. |

Additional defensive risk: `useOutputs.js:230` checks source generation but not the version request's own validity. A transport injected to ignore abort can return A after closing A/opening B and overwrite B's versions/loading. Only that injected-transport behavior is demonstrated; no real HTTP/browser leakage claim. A small request-validity fence is recommended with its own regression.

Reproduction script/full observation log/exit archived under `review-3af0c43-counterexamples/`. Exit0 records counterexamples, not product success. The reviewer did not rerun the broad suite; prior145/14/build results do not negate these newly demonstrated cases. Root resumed the same sole critical writer for bounded repairs and final tests/build, then the same independent reviewer must recheck. No OD05 acceptance or OD06 start yet. Actual API/client/browser/Agent-offline/physical-device gates remain OD06.
