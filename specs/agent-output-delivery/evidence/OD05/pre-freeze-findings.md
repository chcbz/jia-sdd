# OD05 pre-freeze implementation findings

Root contract/coverage check on the uncommitted OD05 working tree. This is not independent acceptance review and must not be attributed to a frozen candidate. Original sole writer remains responsible for fixes.

1. OutputList receives a plain object containing refs and reads nested properties in its template. Verify actual mount with the real useOutputs return value; helper/source-string tests do not establish correct unwrapping, list rendering or button states.
2. OutputList retains previewItem when source/identity changes. OutputPreview watches only that item; existing text/image state can survive a source/account switch. Its unmount cleanup revokes only an existing URL, without invalidating an in-flight request. Require clear/cancel/generation fences and late-response tests.
3. Accepted API downloads always return application/octet-stream. Rejecting a Blob unless blob.type is image/* makes every real image preview fail. Use the strictly allowed authenticated item MIME and decoded dimension/pixel bounds. Byte-size limits alone do not bound decoded images.
4. List refresh aborts the same controller supplied to downloads. Unconditional five-second polling can interrupt long downloads and replaces previously appended history pages. Separate source-level operation cancellation from list request cancellation; implement specified polling lifecycle/backoff and preserve pagination.
5. Download errors are currently uncaught event callback promises; display actionable retryable/requestId errors.
6. Detail payload.item needs exact source/outputId/version matching. Source helper checks alone do not validate this path.

Required behavioral evidence before acceptance: mount the real list; deferred list/download/preview responses across source/identity switches and unmount; actual application/octet-stream image response; decoded image bound; download failure and long download surviving refresh; pagination/history persistence; malformed/mismatched detail; polling completion/backoff.

Existing broad npm test was stopped during unrelated E13 pixel/nav recomputation and is explicitly incomplete. The separate component run used a too-short default timeout; preserve its failure evidence and rerun affected cases using the project configuration. No passing full-regression claim is allowed. These repairs require updated scoped tests and build associated with the final candidate.

## Resource navigation follow-up

During repair inspection, resourceRoute appended outputSourceType/outputSourceId/outputId/outputVersion to the current URL, but there was no page consuming them. A token-free string alone is not a usable resource route. Require an actual same-account page/navigation consumer that requests the exact source/output/version without Agent selection, plus a navigation behavior test. Construct the URL from a controlled origin/path and allowlisted routing fields; do not preserve arbitrary original query parameters with only a token-name blacklist. The independent candidate review must verify this repair too.
