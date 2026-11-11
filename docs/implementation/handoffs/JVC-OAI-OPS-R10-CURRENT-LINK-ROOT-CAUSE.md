# JVC-OAI-OPS R10 current-link live-race root-cause matrix

Date: 2026-09-04
Non-promotable diagnostic snapshot: `a543e644c2fc738de34332c339d4c2c8d557dbea` / tree `a0f2d196b6a3cdac520a7b907b54f4269f25a718`
R10 failed receipt: `/tmp/jvc-oai-ops-r10-live.SQoGDT/jvc-oai-ops-r10-live-matrix-post-state.json`, SHA-256 `5ecbbdc7588fe3451b6e650b0a63a80f6bc99b71b794fc0c9b0f116fdfa47b44`.

## Consecutive failures

| Attempt | Exact evidence | Root cause/status |
| --- | --- | --- |
| R9 | Exact `8afe14f4` / tree `2dbc858d`; full live matrix failed after 15:09 at `sealed_before_staged × files:nginx_http_snippet`; bare assertion and unconditional fixture deletion hid the actual journal/selector post-state. | Harness observability was insufficient. R10 added non-secret assertion diagnostics and retained post-state receipts. |
| R10 | Exact `a543e644` / tree `a0f2d196`; the same full selector failed at `sealed_before_staged × symlinks:current_link`, assertion `post_selector_unchanged`; initial rc=1, journal=[], selector remained the deliberately injected `.r8-raced` target. The previously failing Nginx HTTP cell passed every labelled assertion in this run. | The test mutates `current.jar` itself and then incorrectly requires the selector to equal its pre-mutation target before the harness restores it. The entrypoint correctly rejected the changed sealed state before any durable phase; it did not and should not silently overwrite an externally raced pre-durable selector using stale assumptions. |

## Frozen semantic question

Before remediation, a fresh read-only reviewer must confirm the safe pre-durable contract for `current_link`. The proposed contract is:

1. while the adversarial symlink mutation is present: activation returns nonzero, creates no durable phase record, never selects the candidate on its own, and leaves the externally observed raced selector untouched rather than racing an automatic rollback;
2. after the harness restores the original selector: same sealed transaction remains fail-closed if receipt-parent ctime no longer matches, with no durable phase record and old selector intact;
3. only a new independently sealed generation may proceed after such a pre-durable selector race.

The reviewer must reject this proposal if it could authorize unsafe availability loss, stale-path restoration, unrelated selector acceptance, or replay across a changed receipt generation.

## Stop and next gate

- No writer, rerun, full inventory, review acceptance, merge, or deployment is authorized until the semantic review resolves the contract.
- If accepted, a matrix-bound fresh Terra writer may change only the live-matrix harness/postconditions and tests under `ops/juyiting-voice-production/**`; production scripts/modules remain unchanged.
- The next full live-matrix execution is exactly once. Any failure stops for a new attribution.
- No key read/install, feature flag, host apply, deployment, restart, or reload.

## Independent Terra semantic review resolution

Read-only reviewer `01a06eeb-44b5-7a52-8458-cf65f0a82db1` conditionally accepted the proposed safety model with one mandatory terminology and evidence correction:

- “no durable record” is forbidden wording because activation ID reservation and the transaction directory are durably created before live receipt validation;
- the enforceable claim is **no durable phase record** and no controller-driven selector publication;
- while the mutation exists, exact raced selector retention is expected; after restoring the old selector, the same txid/full `activate-release.sh --activate` invocation must remain nonzero because the sealed working-directory receipt generation changed;
- phase records remain empty throughout, the old selector remains after restoration, and only a distinct txid with a freshly sealed snapshot may activate.

The matrix-bound successor must encode all eight reviewer assertions, including full-entrypoint final return codes and explicit distinction between ID reservation and phase records. It must not weaken or change production implementation.
