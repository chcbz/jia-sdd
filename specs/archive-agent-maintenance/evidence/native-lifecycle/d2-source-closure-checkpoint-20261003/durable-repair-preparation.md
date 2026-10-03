# Read-only design preparation — NOT_IMPLEMENTED / NOT_ACCEPTED

Date: 2026-10-03. Reviewer: Leibniz (`01a100e0-8707-7210-a247-5165db243567`). This is a proposal for original D2 requirements, not source/test/Runtime closure. Native exact-contract repair must freeze and be independently reviewed first; its final block API is consumed, not separately redesigned.

## Durable chapters and publication

- Reuse the existing private `AgentTaskArtifactStorage` root and exact scope. Add immutable chapter payload references/digests and a versioned draft storage marker; old JSON remains readable until exact-content migration proves equivalence.
- Persist a scoped artifact intent before upload. Perform immutable object I/O outside the DB transaction; repeat current manager/runtime/appointment/install/run/grant/epoch authorization and draft CAS before registering references. No caller-chosen paths or storage URI.
- Client checkpoints live under the existing platform manager stateRoot `archive-runs`, not a second inbox/scheduler. Atomic immutable context, per-block committed facts and terminal facts bind full command/run/source/package identity. On restart, authoritative result/context/draft wins; local records never authorize a write or skip by themselves.
- Publication reserves one stable publication/edition/import identity and seals the exact candidate. STAGING creation is committed before copying; each bounded batch commits exact rows and its cursor together. Duplicate rows must compare exactly, never overwrite mismatches.
- Extract only reusable exact-insert/reread machinery from the existing content importer; preserve its legacy public activation behavior. Persisted complete reread precedes READY. READY is unreadable until a separate final activation transaction.
- Final activation repeats all current authority and expectedWorkRevision/active CAS, then commits publication/readback, active pointer, revision, job/run/grant, operation/import and event/outbox atomically. Revocation before activation blocks it; post-commit readback failure never republishes. Human takeover records current human authority rather than reusing revoked Agent credentials.
- Schema upgrade must recognize the exact predecessor, add block/import/artifact-intent structures and fail closed for unknown partial drift. External object-store migration never runs in a schema initializer.

## Quota and cleanup

- Installation aggregate count/committed bytes/staging bytes must be finite and enforced before download/staging. Current package-size limits are not aggregate quota. Quota may fail closed rather than auto-delete; reclamation requires exact terminal/unreferenced proof and a journal. Current/in-flight/recoverable/foreign-scope installations cannot be reclaimed by filesystem enumeration.
- Add deletion of one exact owned scoped digest, not recursive roots/arbitrary URIs. A bounded keyset reconciler considers only stale RESERVED intents after rechecking noncommitted operation and absence of source/block references. Exact retry may restore an object and reference it; collectors must not race active upload/registration.
- Production cadence, retention values, credentials, actual deletions/real-book publication, deployment, paid calls and 84 business cases remain separately gated. Missing source APIs, quota enforcement and reference-proof cleanup cannot be waived as production-only work.

## Required finite probes

1. Fresh schema, exact predecessor upgrade, fail-closed malformed predecessor and exact legacy content migration.
2. Upload-before-reference crash recovery; same-key same-payload replay vs changed payload conflict; authorization fence after upload leaves draft unchanged.
3. Client restart after chapter N writes only missing chapters; tamper/symlink/scope/package mismatch and server-digest disagreement produce no producer write.
4. Advice/Jackson retains exact content and authoritative block digest facts.
5. SEALED/STAGING and batch crash/lost-response resume with same IDs and one cursor; persisted row mismatch stays inactive; full reread required for READY.
6. READY invisible before publication; revoke/fence before final activation; concurrent work CAS and all-or-none failure injection.
7. Readback failure retains one publication; human takeover uses new authority.
8. Quota rejection before download/write; exact unreferenced terminal reclaim vs referenced/current/in-flight/foreign/symlink/race rejection.
9. Artifact RESERVED/REFERENCED/reclaimed transitions and bounded exact-scope collection leave other tasks untouched.

No source edits, Git, builds, tests, services, production access or publication were performed by this reviewer for this preparation.
