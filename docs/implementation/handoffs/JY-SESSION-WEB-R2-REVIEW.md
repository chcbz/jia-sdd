# Web bounded review remediation

Godel REJECT runtime52686ed / generated-only0d40aaef (generated14-line declaration delta accepted). Existing evidence29 conversation +3 voice tests PASS and production build rc0.

- P1: guard text send while isAwaitingReply as well as isStreaming, including composer disabled state and direct composable invocation; preserve first turn tracking.
- P1: histories older than first100 unreachable. Add real load-more/paging with scope/identity generation guards and duplicate-safe merging. IMPORTANT backend currently wraps filtered list into PageInfo.of(normalList), so totals may collapse to page length. Do not rely only on result.total; use raw-page length and empty-next-page termination if total unreliable. No backend/API redesign.
- P1: selection content failure clears messages but reports success. Expose selected-load error and retry selected ID rather than load latest; return actual failure and prevent sends against unresolved history where appropriate.
- P2: new conversation invalidates pending history fetch but does not clear loading; explicitly reset/invalidate history state on new.

Retain current tests; add focused async boundary tests for these cases, then build changed runtime once and independent delta review. No production until both pass. Prior verifier model502 is infrastructure, not product failure; this matrix is explicit new remediation authorization after two attributed gate failures.

Residual pre-existing backend ownership/Long-serialization/live-only SSE replay limitations are not claimed fixed by this bounded Web/Agent change. Continue existing authenticated adapters and strict scope/ID guards; do not introduce new backend migrations in this slice.
