# OD05 implementation handoff

Start only after OD04 independent repair approval. Sole product writer: balanced_worker in `/home/chc/wsps/cyf-worktrees/output-web`; root owns evidence/ledger. Do not switch the original checkout or edit API/client. Other tasks share the repositories: preserve their history/session/ACL work and all unrelated changes.

Read `preparation.md`, root `detailed-design.md` sections 3 and 10, `openapi.yaml`, `acceptance.md`, and the project runbook before editing. API development candidate is `4c292cc35e4d82a23620a85296b721569ff59bd5`.

## Baseline

Feature Web is clean at `77666e8fc1b2060ff3db8374b5de4539a5e5e53d`; observed `origin/develop` is `b31565f8741fdc6f986763dd86442a2c2a4345b0` (conversation history/deletion). Verify ancestry, clean status and committed tip, then fast-forward the dedicated feature branch before edits; record actual base. Do not infer release from branch names. Dependencies already installed; avoid reinstall unless lockfile changed.

## Delivery

- Shared `OutputList`, `OutputCard`, bounded `OutputPreview`, `useOutputs`, and authenticated download utilities.
- Cover Hall ChatPanel (reuse explicit conversationId), standalone Chat.vue, and bounty details in BountyPanel.vue. Retrieval must remain reachable without a selectable or connected Agent and when legacy workspace is disabled. Reuse the shared list in the workspace when appropriate.
- User/source lifecycle cancels requests, clears list/pagination/preview and revokes object URLs. Old replies must not populate the new identity/source. Preserve history switch/delete behavior and separate map/roster flows.
- Consume exact API envelopes and version strings. Detail is `data.item`. Preserve `retryable` and `requestId`; correctly handle expired/revoked/conflict/network states and fixed-snapshot pagination. Download uses UserJwt Blob mode integrated with useHttp's existing identity lifecycle; no token URLs.
- Poll only while needed with visibility handling and bounded backoff; explicit refresh and pagination remain available. Show R1 shared files without presenting them as formal acceptance.
- Text preview <=1 MiB, escaped or sanitized Markdown; bounded decoded raster images. PDF/Office/ZIP are download only. Enforce blob cleanup and safe filenames. WeChat guidance links to a token-free same-account browser resource route; actual device acceptance remains OD06.

## Verification / freeze

Meaningful tests: identity/source changes with late responses and downloads, version pagination/error recovery, supported/unsupported previews, offline Agent retrieval, both chat surfaces and bounty wiring; include affected history/workspace/session regressions. Run `npm run build` as required by user AGENTS (overrides old runbook build preference). Capture actual commands, full log/exit, commit and source hashes; no secrets in evidence. Tests must run independently of absolute root-spec paths.

Freeze a clean candidate and return changed files, base/candidate, test/build results, limitations and evidence paths. Stop product writes for independent read-only review; do not self-approve or start OD06.
