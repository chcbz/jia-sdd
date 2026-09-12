# OD05 exact-resource repair review — REQUEST_CHANGES

Candidate `07d20ea72a8f18e00c3a184f801f16e34022b5ed`, same independent read-only reviewer `/root/od05_review_fallback`.

Confirmed repaired: empty list followed by exact-detail404 clears the precise card; a valid historical version absent from latest list is revalidated and retained. Prior download cancellation, nonretryable polling, version navigation and stale-history response probes continue to pass.

Remaining P2 R02: `useOutputs.js:211` only records the error after list403, retaining items, pagination and historical state. `OutputList.vue:241` clears only the requested-resource cache/preview. Initial authorized list followed by source403/retryable:false refresh still shows the previous title and downloadable card next to Source forbidden.

Required: invalidate this source's primary and exact/version caches plus active requests/generation on explicit authority denial, while preserving the visible error and request ID. Do not immediately auto-repopulate via a focus watcher. Keep explicit refresh/recovery available and preserve the previously repaired cases. Test denial statuses and already-active detail/download responses as a complete source lifecycle, rather than another isolated card patch.

Counterexample script/log/exit archived under `review-07d20ea-counterexamples/`; controlled combination evidence is not live API E2E. Reviewer left product/root untouched and did not rerun full tests. Root resumed the same sole writer for this remaining repair. OD06 remains unstarted.
