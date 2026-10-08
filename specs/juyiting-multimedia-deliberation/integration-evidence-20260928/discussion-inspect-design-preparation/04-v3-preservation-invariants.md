# Controlled image v3 preservation invariants for discussion/inspect closure

Date: 2026-10-01. These invariants prevent the next discussion/clarification package from weakening the already frozen controlled-image authority and source wire.

## Protocol preservation

1. Existing image v1/v2 command, capability, input, result and START fixtures remain byte/semantic compatible. No field is renamed, removed, reinterpreted or silently accepted as v3.
2. Source-aware image v3 remains an independent sibling declaration. At the verified Client baseline it is deliberately:

```json
{"enabled":false,"operations":[]}
```

3. DISCUSSION/AVAILABLE/INSPECT capability must not mutate that declaration or advertise controlled execution readiness.
4. A generic Codex/native executor, CHAT profile, routing label, persona, Web button, local install or managed-host label is not controlled-image v3 readiness.
5. Enabling v3 later requires the exact API/runtime/source/credential/native-poll gates and actual end-to-end evidence; this prep does not enable it.

## Strict operation/source union

- `GENERATE_IMAGE`: only task-linked exact workspace versions, JPEG/PNG, 0–16, purpose `REFERENCE`, in canonical source order/digest required by the frozen contract.
- `EDIT_IMAGE`: exactly one exact current-conversation JPEG/PNG asset revision; server resolves current scope, producer request/step/execution/run/output lineage, MIME/hash/positive length and bytes.
- An EDIT source is not converted into a workspace pseudo-archive and need not be saved before editing.
- A browser URL/path/hash/MIME/producer tuple is never source authority.
- Old and new outputs coexist; editing never overwrites or invalidates the prior asset.
- Discussion reference limits and media types are separate. They must not expand the image v3 source union or change its 16-input bound.

## Per-intent authority

Every later GENERATE/EDIT action is a new intent and has:

- a new stable interaction Idempotency-Key and exact body digest;
- a new request/step/execution-intent identity;
- a current baseline assignment/grant check without mutating baseline operations/version/input scope/derived-asset flag/cost locator;
- a fresh operation-specific owner grant;
- a fresh Provider consent bound to the exact operation, source digest, instruction, provider binding/model/custody/policy and current versions;
- a new execution/run/command;
- one durable pre-call claim and exactly one first START.

The initial GENERATE-only grant cannot authorize EDIT. A consent or operation grant in `CONSUMED`, revoked, superseded, wrong-operation, wrong-source, wrong-parent or wrong-version state cannot authorize another call. A natural-language follow-up, typed proposal, inspection result, displayed preview, workspace save or formal-delivery relation is not a substitute.

## Initial intent versus later intent

- An initial point-and-start generation that is explicit, fully authorized and complete may execute directly; no mandatory CHAT/planner preflight is added.
- If that same initial intent lacks essential information, it may enter durable `WAITING_USER` **before** RESERVED/START. An exact clarification reply may resume the same still-unconsumed intent after currentness revalidation.
- Once the initial authority is consumed/completed/failed with unknown external acceptance, it is never silently reused for “再来一张”, “再鲜艳一点”, “换成黄鹂”, EDIT, or any other later action.
- Each later action follows the frozen preview → explicit current acknowledgement → issue → admit → START chain with independent keys and authority.

## Discussion/inspection isolation

DISCUSSION, CLARIFICATION_REPLY, AVAILABLE and INSPECT:

- never create, reserve, bind, consume, revoke or refresh an image operation grant or Provider consent;
- never create an image execution/run/command/START;
- never consume the initial point-and-start consent;
- never use an image provider endpoint for inspection;
- never translate an answer/proposal into execution without a separately accepted EXECUTE intent;
- never claim image success from model text, a local path, external URL or unverified bytes.

AVAILABLE reads metadata only. INSPECT may read only an exact authorized manifest through a separately proven read capability. Neither mode permits image generation/editing or paid external dispatch.

## Durable single-call and unknown-outcome rules

- The stable pre-call claim key is scoped to authenticated owner/client/tenant plus the exact command/intent; it is not based on temporary run directories, process epoch or random retry IDs.
- Claim persistence, no-follow path checks and required atomic durability complete before the only external fetch/call.
- Concurrent workers, a second Client instance, restart, corrupt claim state, redirect, network unknown, timeout, 429, invalid output or process crash must not cause another Provider call.
- Scratch cleanup never deletes the durable claim.
- No automatic retry, model/account switch, endpoint fallback, multipart fallback or remote output URL download.
- API/Web recovery first uses the original key’s read-only GET. `404` is not proof of absence and cannot authorize a new key or call.
- If actual Provider acceptance is unknown, the operation remains recovery-required/unknown until an authoritative disposition exists. It is not retried under a fresh intent as an automatic recovery tactic.

## START and source binding

The v3 command and START continue to bind the exact operation, normalized source snapshot digest, consent/operation-grant tuple, execution/run, provider binding/account policy and current lease. START remains first-only. Discussion/clarification state cannot manufacture or advance that tuple.

## Required preservation regressions

1. All existing v1/v2 golden fixtures remain byte-exact after schema-3 discussion changes.
2. Runtime registration still reports controlled image v3 disabled with empty operations until separately enabled by its own package.
3. DISCUSSION/AVAILABLE/INSPECT/CLARIFICATION create zero controlled consent/grant/execution/run/command/START rows and zero Provider calls.
4. Initial GENERATE grant plus a new text reply cannot EDIT.
5. Old consent, old command, old START or consumed operation grant cannot serve a later proposal.
6. Same follow-up key with changed operation/source/parent/instruction/version is 409.
7. EDIT accepts one current-conversation asset only; zero/two/workspace/foreign/stale/wrong-MIME sources fail before external call.
8. GENERATE rejects a 17th source without truncation and rejects current-conversation asset source in that union.
9. Concurrent issue/admit/START has one winner and at most one external attempt.
10. Network unknown/restart/corrupt claim/429/invalid output never triggers a second external attempt.
11. Proposal/clarification/inspection events cannot be interpreted as asset-ready or execution-complete events.
12. Reassignment, revoke, requirement/source/capability/provider-binding drift blocks new execution but does not erase already committed readable assets.

## Scope statement

This document preserves controlled-image execution while allowing the next package to close ordinary discussion, exact clarification reply, metadata-only AVAILABLE, truthful INSPECT and typed planning. It does not claim Provider/account availability, runtime enablement, product acceptance, release readiness, full multimedia completion, archive/formal-delivery completion, or permission to spend.
