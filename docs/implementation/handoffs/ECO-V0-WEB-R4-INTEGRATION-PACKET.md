# WEB R4 — frozen claim contract integration

Main read-only integration inspection of clean `e48246732d5bd0a72025609627cc542a353b882e` / tree `095d548fbe581accf4dac47c8e8a2fe7ace4fed3`. This is a bounded implementation packet, not an independent acceptance or a second ledger.

## Required fixes before review/build

1. `src/composables/juyiting/useHallTaskActions.js#claimFundedTask` currently obtains a quote and immediately submits claim. User requested deciding whether to claim **after seeing estimated expense**. Split preview from explicit confirmation, or expose a confirmation sheet with actual server quote before sending claim. Cancel must send no claim. Expired/mismatched quote must require fresh preview, never silently replace and charge. Show four token categories, price book, estimated/worst costs and payout, platform fee, reasons, expiry; keep exact target Agent and task version.
2. Same function currently `Object.assign(task, claimed)` but W05 receipt is `{taskId,agentId,quoteId,status,taskVersion,claimedAt}`, **not** `AgentTaskDTO`. Strictly validate matching receipt and refresh canonical task via existing task GET/search interface. Do not let successful receipt + failed readback appear to be a failed claim/re-enable duplicate mutation; show confirmed assignment with pending refresh, retain correctness of idempotent retry and canonical string versions. Do not regress a newer task snapshot when delayed receipt/readback arrives.
3. Add focused regressions for quote preview/no confirmation, explicit confirm, cancel, expiry/mismatch, immutable receipt success plus failed snapshot refresh, and newer snapshot ordering. Reuse existing test helpers.

## Scope

Terra original combined Web owner, existing combined worktree (clean before writes). Own narrowly scoped Hall task action/composition/quote UI plus focused tests. No API/Agent changes, no main Web edits, no Gradle/npm/build until clean source handoff; independent review then serialized test/build. R01/R02 rent UI paths must be coordinated before overlap.
