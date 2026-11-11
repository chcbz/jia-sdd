# INSPECT transport serialization Owner self-check

Candidate: `0fd5aed5585d9f0714d246d0bcbb94de757a99f4`, tree `b1f5c5b4825b64ea446e9a280f9ad9814c541e99`.

## Verified scope

- Only AgentWebSocketHandler and its capability-negotiation regression suite changed.
- Existing three-argument sendEvent delegates with preservation disabled; all existing ordinary-event callsites keep JsonUtil.toSafeJson.
- Only admitted typed INSPECT dispatch uses preservation=true, after exact tenant/owner/client/Agent registry selection, live session and manifest profile validation. No fallback to unsupported session, no ACL/capability/profile relaxation.
- Complete authenticated protocol facts are serialized with JsonUtil.toJson, without logging the wire. A log sanitizer is not a protocol serializer: depth truncation or DATA redaction changes aliases and integrity-bound context.
- New regression reproduces the actual sanitizer root/nested depth difference, captures the sent frame, checks both complete context snapshots, independently recalculates SHA256 canonical context hash and preserves literal DATA. Separate ordinary-event test retains sensitive-field sanitization.
- Production cause evidence is read-only persisted outbox shape + production depth reproduction; not intercepted actual network frame. Client journal independently reports contextSnapshot alias conflict.
- git diff --check passed before commit. No local Gradle/build/test claim; authoritative tests are Flow5260799/115 and must be independently read from same-run reports.

## Runtime safety

Run114 remains installed. Run115 develop configuration contains only cloud CI/tests/build/artifact, no deploy stage. No API restart, DML, cancellation, new task creation, assignment or duplicate task424 request performed for this candidate. New version installation requires its own exact authorization. task423 remains completed and must not be replayed.
